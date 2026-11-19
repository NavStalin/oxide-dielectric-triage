"""Optional provider: Claude turns free text into the same typed Criteria. Used only when a key is set.

The model touches language only (D-001). It never sees the snapshot, never ranks, and its output is
clamped by policy like any other criteria, so it can't loosen a rule. Any error or refusal raises
LLMUnavailable and the pipeline falls back to RulesProvider, saying so in the trace.
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

from triage.models import Criteria

MODEL = "claude-opus-5-5"

SYSTEM = """You translate a materials scientist's request into ranking settings for an oxide \
dielectric triage tool. You do not know or state any material property values.

Criteria and defaults (weights 0 to 1):
- stability (energy above hull), default 0.35
- band_gap, default 0.30
- hazard (element-level toxicity flags), default 0.20
- simplicity (fewer elements), default 0.15
- dielectric (dielectric constant kappa), default 0.0, i.e. off

Only change a setting when the request clearly asks for it. Use -1 for any weight or threshold you
keep at its default, 0 for max_elements and shortlist_size to keep the default, and style "default".
Hard filters only when the user gives an explicit threshold (band gap in eV, energy above hull in meV/atom).
List each phrase you used in `understood` (with its effect) and anything you could not map in
`not_understood`. Never add requirements the user did not state."""

KEEP = -1.0  # sentinel for "keep the default"


class LLMCriteria(BaseModel):
    """All fields required, no unions: the API rejected optional/nullable fields as 'Schema is too
    complex' (verified 2026-11-18), so "no change" is a sentinel value instead."""

    stability_weight: float
    band_gap_weight: float
    hazard_weight: float
    simplicity_weight: float
    dielectric_weight: float
    min_band_gap_ev: float
    max_e_hull_mev: float
    max_elements: int
    exclude_elements: list[str]
    allow_extra_anions: bool
    shortlist_size: int
    style: Literal["pi", "audit", "default"]
    understood: list[str]
    not_understood: list[str]

    @classmethod
    def unchanged(cls, **kw) -> LLMCriteria:
        base = {
            "stability_weight": KEEP,
            "band_gap_weight": KEEP,
            "hazard_weight": KEEP,
            "simplicity_weight": KEEP,
            "dielectric_weight": KEEP,
            "min_band_gap_ev": KEEP,
            "max_e_hull_mev": KEEP,
            "max_elements": 0,
            "exclude_elements": [],
            "allow_extra_anions": False,
            "shortlist_size": 0,
            "style": "default",
            "understood": [],
            "not_understood": [],
        }
        return cls(**{**base, **kw})


class LLMUnavailable(Exception):
    pass


def api_key() -> str | None:
    if os.environ.get("ANTHROPIC_API_KEY"):
        return os.environ["ANTHROPIC_API_KEY"]
    env = Path(__file__).resolve().parents[3] / ".env"
    if env.exists():
        try:
            from dotenv import dotenv_values
        except ImportError:
            return None
        return dotenv_values(env).get("ANTHROPIC_API_KEY") or None
    return None


def available() -> bool:
    if not api_key():
        return False
    try:
        import anthropic  # noqa: F401
    except ImportError:
        return False
    return True


class LLMProvider:
    name = "llm"

    def __init__(self, client=None, timeout_s: float = 90.0):
        self._client = client
        self._timeout = timeout_s

    def _get_client(self):
        if self._client is None:
            import anthropic

            key = api_key()
            if not key:
                raise LLMUnavailable("no ANTHROPIC_API_KEY")
            self._client = anthropic.Anthropic(api_key=key, timeout=self._timeout, max_retries=1)
        return self._client

    def parse(self, text: str, default_weights: dict[str, float]) -> Criteria:
        try:
            resp = self._get_client().messages.parse(
                model=MODEL,
                max_tokens=4000,
                output_config={"effort": "low"},
                system=SYSTEM,
                messages=[{"role": "user", "content": text}],
                output_format=LLMCriteria,
            )
        except Exception as e:  # any SDK, network or validation error -> deterministic fallback
            raise LLMUnavailable(f"{type(e).__name__}: {e}") from e
        if resp.stop_reason == "refusal" or resp.parsed_output is None:
            raise LLMUnavailable(f"model returned no criteria (stop_reason={resp.stop_reason})")
        out: LLMCriteria = resp.parsed_output

        weights = dict(default_weights)
        for k in ("stability", "band_gap", "hazard", "simplicity", "dielectric"):
            v = getattr(out, f"{k}_weight")
            if v >= 0:
                weights[k] = v
        return Criteria(
            weights=weights,
            min_band_gap=out.min_band_gap_ev if out.min_band_gap_ev >= 0 else None,
            max_e_hull=out.max_e_hull_mev / 1000 if out.max_e_hull_mev >= 0 else None,
            max_elements=out.max_elements or None,
            exclude_elements=[e for e in out.exclude_elements if re.fullmatch(r"[A-Z][a-z]?", e)],
            allow_extra_anions=out.allow_extra_anions,
            shortlist_size=out.shortlist_size or None,
            style=None if out.style == "default" else out.style,
            matched=[f"(model) {u}" for u in out.understood],
            unparsed=out.not_understood,
            provider=f"llm:{MODEL}",
        )


class RationaleItem(BaseModel):
    formula: str
    sentence: str


class Rationales(BaseModel):
    items: list[RationaleItem]


RATIONALE_SYSTEM = """You write one plain-English sentence per candidate explaining its rank for a \
materials scientist. Use only the values given in the JSON for that candidate; do not add any other \
number, property, claim or citation. Max 30 words per sentence. Do not recommend running experiments."""


def rationales(facts: list[dict], client=None) -> dict[str, str]:
    """Model-worded rationales. Callers must pass each sentence through number_check."""
    import json

    prov = LLMProvider(client=client)
    try:
        resp = prov._get_client().messages.parse(
            model=MODEL,
            max_tokens=4000,
            output_config={"effort": "low"},
            system=RATIONALE_SYSTEM,
            messages=[{"role": "user", "content": json.dumps(facts)}],
            output_format=Rationales,
        )
    except Exception as e:
        raise LLMUnavailable(f"{type(e).__name__}: {e}") from e
    if resp.stop_reason == "refusal" or resp.parsed_output is None:
        raise LLMUnavailable(f"no rationales (stop_reason={resp.stop_reason})")
    return {i.formula: i.sentence for i in resp.parsed_output.items}


# A number not glued to a letter: skips subscripts like the 2 in HfO2.
NUMBER = re.compile(r"(?<![A-Za-z0-9_.])-?\d+(?:\.\d+)?")


def number_check(sentence: str, allowed: list[float], rel_tol: float = 0.005) -> bool:
    """True only if every number in a model-written sentence matches a value from the cited records.

    Values are compared at the precision written in the sentence (e.g. 5.66 matches 5.664).
    """
    for tok in NUMBER.findall(sentence):
        x = float(tok)
        decimals = len(tok.split(".")[1]) if "." in tok else 0
        ok = any(
            round(a, decimals) == x or abs(a - x) <= rel_tol * max(1.0, abs(a)) for a in allowed
        )
        if not ok:
            return False
    return True
