"""Evidence confidence: a points rubric from config/confidence.yaml (D-019). Separate from suitability."""

from __future__ import annotations

from typing import Any

from triage.candidates import primary_gap
from triage.models import Candidate, Confidence, CrossCheck, Suitability


def assess(
    cand: Candidate,
    suit: Suitability,
    xc: CrossCheck,
    cfg: dict[str, Any],
    correlated_elements: list[str],
) -> Confidence:
    p = cfg["points"]
    pts, reasons = 0, []

    def add(n: int, why: str) -> None:
        nonlocal pts
        pts += n
        reasons.append(f"{n:+d} {why}")

    r = cand.representative
    _, method = primary_gap(r)
    if method == "TBmBJ":
        add(p["gap_tbmbj"], "band gap from TBmBJ")
    else:
        add(p["gap_fallback"], "band gap from OptB88vdW fallback (probable underestimate)")

    if r.has_icsd:
        add(p["icsd_reference"], "experimental structure reference (ICSD, via JARVIS)")
    elif xc.icsd_id:
        add(
            p["icsd_reference"],
            f"experimental structure reference (ICSD {xc.icsd_id}, via {xc.source})",
        )
    else:
        reasons.append("+0 no ICSD reference found")

    if xc.status == "agree":
        add(
            p["crosscheck_agree"],
            f"{xc.source} agrees on stability ({xc.match_type.replace('_', ' ')})",
        )
    elif xc.status == "disagree":
        add(
            p["crosscheck_disagree"],
            f"{xc.source} disagrees on stability by {xc.delta_ev * 1000:.0f} meV/atom",
        )
    else:
        add(p["crosscheck_unavailable"], f"no stability cross-check ({xc.status}: {xc.detail})")

    if not suit.missing:
        add(p["all_criteria_present"], "all weighted criteria have values")

    if r.hull_n_compositions is not None and r.hull_n_compositions < cfg["sparse_hull_below"]:
        add(
            p["sparse_hull"], f"hull built from only {r.hull_n_compositions} competing compositions"
        )

    corr = sorted(set(r.elements) & set(correlated_elements))
    if corr:
        add(
            p["correlated_element"],
            f"contains {', '.join(corr)}: DFT energies and gaps less reliable",
        )

    level = next(
        name for name, floor in sorted(cfg["levels"].items(), key=lambda kv: -kv[1]) if pts >= floor
    )
    return Confidence(level=level, points=pts, reasons=reasons)
