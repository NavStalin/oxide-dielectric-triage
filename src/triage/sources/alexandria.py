"""Alexandria (PBE) stability cross-check for shortlisted formulas, via its OPTIMADE API (D-044).

Fields verified live 2026-11-20 (docs/VERIFIED_FACTS.md section 3a): no key, CC BY 4.0,
`_alexandria_hull_distance` in eV/atom, `_alexandria_space_group` as a number, and
`chemical_formula_reduced` with elements in alphabetical order ("O2Si", not "SiO2").

One request per candidate in the usual case: the representative's own space group first, then
the formula's lowest-hull entry if Alexandria has no entry in that space group.

A space group that has a mirror-image partner is queried together with it. Left- and right-handed
quartz (152 and 154) are the same material with the same energy, and a database usually stores
only one of them.
"""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from functools import reduce
from math import gcd
from pathlib import Path
from typing import Any
from urllib.parse import quote

import requests

from triage.models import Candidate, CrossCheck, Evidence
from triage.sources.http import SourceFailure, get_json

__all__ = ["NAME", "SourceFailure", "cross_check", "fetch"]

NAME = "Alexandria"
FIELDS = "chemical_formula_reduced,_alexandria_hull_distance,_alexandria_space_group,_alexandria_xc_functional"

# The 11 enantiomorphic (mirror-image) space-group pairs, International Tables numbers.
_PAIRS = [(76, 78), (91, 95), (92, 96), (144, 145), (151, 153), (152, 154)]
_PAIRS += [(169, 170), (171, 172), (178, 179), (180, 181), (212, 213)]
MIRROR = {a: b for a, b in _PAIRS} | {b: a for a, b in _PAIRS}


def optimade_formula(formula: str) -> str:
    """'SiO2' -> 'O2Si': OPTIMADE reduced formula, elements alphabetical, counts divided by their GCD."""
    counts: dict[str, int] = {}
    for el, n in re.findall(r"([A-Z][a-z]?)(\d*)", formula):
        counts[el] = counts.get(el, 0) + (int(n) if n else 1)
    if not counts:
        raise ValueError(f"cannot parse formula {formula!r}")
    g = reduce(gcd, counts.values())
    return "".join(f"{el}{c // g if c // g > 1 else ''}" for el, c in sorted(counts.items()))


def query_url(formula: str, base_url: str, spg_number: int | None = None) -> str:
    flt = f'chemical_formula_reduced="{optimade_formula(formula)}"'
    if spg_number in MIRROR:
        flt += (
            f" AND (_alexandria_space_group={spg_number}"
            f" OR _alexandria_space_group={MIRROR[spg_number]})"
        )
    elif spg_number is not None:
        flt += f" AND _alexandria_space_group={spg_number}"
    return (
        f"{base_url}/structures?filter={quote(flt)}"
        f"&sort=_alexandria_hull_distance&page_limit=1&response_fields={FIELDS}"
    )


def _rows(data: dict[str, Any]) -> list[dict[str, Any]]:
    out = []
    for r in data.get("data", []):
        a = r.get("attributes", {})
        if a.get("_alexandria_hull_distance") is not None:
            out.append({"id": r["id"], **a})
    return out


def fetch(
    cand: Candidate,
    cfg: dict[str, Any],
    allowed_hosts: list[str],
    cache_dir: Path,
    session: Any = requests,
) -> dict[str, Any]:
    """Return {'url', 'retrieved_at', 'rows', 'match_type'}; cached on disk. Raises SourceFailure."""
    spg = cand.representative.spg_number
    cache = cache_dir / f"{cand.formula}_{spg or 'any'}.json"
    if cache.exists():
        return json.loads(cache.read_text())

    rows: list[dict[str, Any]] = []
    url, match_type = "", "formula_level"
    if spg is not None:
        url = query_url(cand.formula, cfg["base_url"], spg)
        rows = _rows(get_json(url, cfg["timeout_s"], allowed_hosts, NAME, session))
        match_type = "same_phase"
    if not rows:
        url = query_url(cand.formula, cfg["base_url"])
        rows = _rows(get_json(url, cfg["timeout_s"], allowed_hosts, NAME, session))
        match_type = "formula_level"
    payload = {
        "url": url,
        "retrieved_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "rows": rows,
        "match_type": match_type,
        "record_url_template": cfg["record_url_template"],
    }
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(payload))
    return payload


def cross_check(cand: Candidate, payload: dict[str, Any], tol: float) -> CrossCheck:
    want = optimade_formula(cand.formula)
    rows = [r for r in payload["rows"] if r.get("chemical_formula_reduced") == want]
    if not rows:
        return CrossCheck(
            status="not_found",
            source=NAME,
            detail=f"Alexandria has no entry with a hull distance for {cand.formula}",
        )
    rep = cand.representative
    best = min(rows, key=lambda r: r["_alexandria_hull_distance"])
    val = float(best["_alexandria_hull_distance"])
    delta = abs(val - (rep.e_hull or 0.0))
    match_type = payload["match_type"]
    return CrossCheck(
        status="agree" if delta <= tol else "disagree",
        source=NAME,
        match_type=match_type,
        ref_stability=Evidence(
            value=val,
            unit="eV/atom",
            method="Alexandria PBE hull distance",
            source="Alexandria",
            record_id=best["id"],
            url=payload["record_url_template"].format(id=best["id"]),
            retrieved_at=payload["retrieved_at"],
        ),
        delta_ev=delta,
        detail=(
            f"Alexandria entry {best['id']} (space group {best.get('_alexandria_space_group')}): "
            f"{val * 1000:.0f} meV/atom vs JARVIS-derived {(rep.e_hull or 0) * 1000:.0f} meV/atom "
            f"({match_type.replace('_', ' ')})"
        ),
    )
