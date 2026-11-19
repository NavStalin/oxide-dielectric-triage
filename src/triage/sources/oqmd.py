"""OQMD REST cross-check for shortlisted formulas (D-005, D-017, D-018).

Fields verified live 2026-11-17 (docs/VERIFIED_FACTS.md section 3). The API is slow and returns
intermittent 502s (observed 2026-11-18), so: allowlisted host, short timeout, one retry, on-disk cache,
and every failure becomes a named SourceFailure, never a crash and never a made-up value.
"""

from __future__ import annotations

import json
import re
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlencode, urlparse

import requests

from triage.models import Candidate, CrossCheck, Evidence

FIELDS = "name,entry_id,icsd_id,stability,delta_e,spacegroup,band_gap"


class SourceFailure(Exception):
    """OQMD could not be reached or returned something unusable."""


def parse_formula(formula: str) -> dict[str, float]:
    """'SrTiO3' -> {'Sr': 1, 'Ti': 1, 'O': 3}, reduced to fractions."""
    counts: dict[str, float] = {}
    for el, n in re.findall(r"([A-Z][a-z]?)(\d*\.?\d*)", formula):
        counts[el] = counts.get(el, 0.0) + (float(n) if n else 1.0)
    total = sum(counts.values())
    return {k: round(v / total, 6) for k, v in counts.items()}


def query_url(formula: str, base_url: str) -> str:
    params = {
        "composition": formula,
        "fields": FIELDS,
        "sort_by": "stability",
        "limit": 50,
        "format": "json",
    }
    return f"{base_url}?{urlencode(params)}"


def fetch(
    formula: str,
    cfg: dict[str, Any],
    allowed_hosts: list[str],
    cache_dir: Path,
    session: Any = requests,
) -> dict[str, Any]:
    """Return {'url', 'retrieved_at', 'rows'}; cached on disk. Raises SourceFailure."""
    url = query_url(formula, cfg["base_url"])
    host = urlparse(url).hostname or ""
    if host not in allowed_hosts:
        raise SourceFailure(f"host {host} not in allowlist")
    cache = cache_dir / f"{formula}.json"
    if cache.exists():
        return json.loads(cache.read_text())

    last_err = "unknown error"
    for attempt in range(2):
        try:
            resp = session.get(url, timeout=cfg["timeout_s"])
            if resp.status_code != 200:
                last_err = f"HTTP {resp.status_code}"
            else:
                data = resp.json()
                payload = {
                    "url": url,
                    "retrieved_at": datetime.now(UTC).isoformat(timespec="seconds"),
                    "rows": data.get("data", []),
                }
                cache_dir.mkdir(parents=True, exist_ok=True)
                cache.write_text(json.dumps(payload))
                return payload
        except requests.Timeout:
            last_err = f"timeout after {cfg['timeout_s']} s"
        except (requests.RequestException, ValueError) as e:
            last_err = type(e).__name__
        if attempt == 0:
            time.sleep(1.0)
    raise SourceFailure(f"OQMD unreachable ({last_err})")


def _norm_spg(s: str | None) -> str:
    return (s or "").replace("_", "").replace(" ", "")


def cross_check(cand: Candidate, payload: dict[str, Any], tol: float) -> CrossCheck:
    target = parse_formula(cand.formula)
    rows = [
        r
        for r in payload["rows"]
        if r.get("stability") is not None and parse_formula(r.get("name", "")) == target
    ]
    if not rows:
        return CrossCheck(
            status="not_found", detail=f"OQMD has no entry with stability for {cand.formula}"
        )

    rep = cand.representative
    same = [r for r in rows if _norm_spg(r.get("spacegroup")) == _norm_spg(rep.spg_symbol)]
    pool, match_type = (same, "same_phase") if same else (rows, "formula_level")
    best = min(pool, key=lambda r: r["stability"])
    oqmd_val = max(
        0.0, float(best["stability"])
    )  # negative = below hull of other phases, i.e. stable
    delta = abs(oqmd_val - (rep.e_hull or 0.0))
    status = "agree" if delta <= tol else "disagree"
    icsd = best.get("icsd_id")
    return CrossCheck(
        status=status,
        match_type=match_type,
        oqmd_stability=Evidence(
            value=float(best["stability"]),
            unit="eV/atom",
            method="OQMD stability (hull distance)",
            source="OQMD",
            record_id=f"oqmd-entry-{best['entry_id']}",
            url=payload["url"],
            retrieved_at=payload["retrieved_at"],
        ),
        delta_ev=delta,
        icsd_id=str(icsd) if icsd else None,
        detail=(
            f"OQMD {best.get('spacegroup')} entry {best['entry_id']}: "
            f"{float(best['stability']) * 1000:.0f} meV/atom vs JARVIS-derived "
            f"{(rep.e_hull or 0) * 1000:.0f} meV/atom ({match_type.replace('_', ' ')})"
        ),
    )
