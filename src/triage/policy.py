"""Deterministic request gate and criteria clamp (D-011, D-012).

The gate runs before any parsing or model call. Prohibited clauses are refused one line each and
removed; the rest of the request still runs. Every refusal is appended to the audit log.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from triage.models import Criteria, Refusal

CLAUSE_SPLIT = re.compile(
    r"(?<=[.!?;])\s+|,\s+|\s+\band\b\s+(?=[a-z])|\s+\bthen\b\s+", re.IGNORECASE
)


def split_clauses(text: str) -> list[str]:
    return [c.strip(" .") for c in CLAUSE_SPLIT.split(text) if c and c.strip(" .")]


def check(text: str, cfg: dict[str, Any]) -> tuple[list[Refusal], str]:
    """Return (refusals, safe_remainder). One refusal per category; matched clauses are removed."""
    refusals: dict[str, Refusal] = {}
    keep: list[str] = []
    for clause in split_clauses(text):
        hit = False
        for cat, spec in cfg["categories"].items():
            if any(re.search(p, clause, re.IGNORECASE) for p in spec["patterns"]):
                hit = True
                if cat not in refusals:
                    refusals[cat] = Refusal(
                        category=cat, matched_text=clause, message=spec["message"]
                    )
        if not hit:
            keep.append(clause)
    # A single phrase can trip a category even when the clause split is coarse; check the whole text too.
    for cat, spec in cfg["categories"].items():
        if cat not in refusals:
            m = next(
                (
                    re.search(p, text, re.IGNORECASE)
                    for p in spec["patterns"]
                    if re.search(p, text, re.IGNORECASE)
                ),
                None,
            )
            if m:
                refusals[cat] = Refusal(
                    category=cat, matched_text=m.group(0), message=spec["message"]
                )
    return list(refusals.values()), ". ".join(keep)


def log_refusals(refusals: list[Refusal], request: str, log_path: Path) -> None:
    if not refusals:
        return
    log_path.parent.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256(request.encode()).hexdigest()[:16]
    now = datetime.now(UTC).isoformat(timespec="seconds")
    with log_path.open("a") as f:
        for r in refusals:
            f.write(
                json.dumps(
                    {
                        "ts": now,
                        "request_sha256_16": digest,
                        "category": r.category,
                        "matched_text": r.matched_text,
                    }
                )
                + "\n"
            )


def clamp(c: Criteria, policy_cfg: dict[str, Any], cand_cfg: dict[str, Any]) -> Criteria:
    """User criteria may tighten filters and change weights; they may never loosen admin policy."""
    out = c.model_copy(deep=True)
    lim = policy_cfg["limits"]
    if out.allow_extra_anions and not (
        lim["allow_user_extra_anions"] or cand_cfg["allow_extra_anions"]
    ):
        out.allow_extra_anions = False
        out.clamped.append("Extra anions (H, C, N, S, halogens) stay excluded: admin setting.")
    if out.shortlist_size is not None and out.shortlist_size > lim["max_shortlist"]:
        out.clamped.append(f"Shortlist capped at {lim['max_shortlist']} (admin limit).")
        out.shortlist_size = lim["max_shortlist"]
    if out.shortlist_size is not None and out.shortlist_size < 1:
        out.shortlist_size = 1
    for k, v in list(out.weights.items()):
        nv = min(1.0, max(0.0, float(v)))
        if nv != v:
            out.clamped.append(f"Weight '{k}' clipped to {nv} (allowed range 0 to 1).")
        out.weights[k] = nv
    if sum(out.weights.values()) == 0:
        out.clamped.append("All weights were zero; site defaults restored.")
        out.weights = {}
    return out
