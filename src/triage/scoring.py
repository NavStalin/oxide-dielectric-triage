"""Suitability: weighted per-criterion scores, renormalised over criteria that have a value (D-010).

Every function here is pure. Breakpoints come from config/ranking.yaml.
"""

from __future__ import annotations

import itertools
from typing import Any

from triage import hazards
from triage.candidates import primary_gap
from triage.models import Candidate, CriterionScore, Evidence, Suitability

ORDER = ["stability", "band_gap", "hazard", "simplicity", "dielectric"]


def piecewise(x: float, points: list[list[float]]) -> float:
    """Linear interpolation through (x, y) points; flat beyond the ends."""
    pts = sorted(points)
    if x <= pts[0][0]:
        return pts[0][1]
    for (x0, y0), (x1, y1) in itertools.pairwise(pts):
        if x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return pts[-1][1]


def ramp(x: float, zero_at: float, full_at: float) -> float:
    return piecewise(x, [[zero_at, 0.0], [full_at, 1.0]])


def stability_score(e_hull: float, cfg: dict[str, Any]) -> float:
    return piecewise(e_hull, cfg["points"])


def band_gap_score(gap: float, cfg: dict[str, Any]) -> float:
    return ramp(gap, cfg["zero_at"], cfg["full_at"])


def dielectric_score(kappa: float, cfg: dict[str, Any]) -> float:
    return ramp(kappa, cfg["zero_at"], cfg["full_at"])


def simplicity_score(n_elements: int, cfg: dict[str, Any]) -> float:
    key = "5+" if n_elements >= 5 else str(n_elements)
    if key not in cfg:
        raise ValueError(f"no simplicity score configured for {n_elements} elements")
    return float(cfg[key])


def hazard_score(n_flagged: int, penalty: float) -> float:
    return max(0.0, 1.0 - penalty * n_flagged)


def combine(criteria: list[CriterionScore]) -> Suitability:
    """Renormalise weights over present, non-zero-weight criteria; missing ones are recorded."""
    active = [c for c in criteria if c.weight > 0]
    present = {c.name for c in active if c.score is not None}
    missing = [c.name for c in active if c.score is None]
    total_w = sum(c.weight for c in active if c.name in present)
    total = 0.0
    for c in criteria:
        if c.name in present and total_w > 0:
            c.effective_weight = c.weight / total_w
            c.contribution = c.effective_weight * c.score
            total += c.contribution
        else:
            c.effective_weight = 0.0
            c.contribution = 0.0
    return Suitability(total=total, criteria=criteria, missing=missing)


def score_candidate(
    cand: Candidate,
    weights: dict[str, float],
    ranking_cfg: dict[str, Any],
    haz_cfg: dict[str, Any],
    record_url: str | None = None,
    retrieved_at: str | None = None,
) -> Suitability:
    r = cand.representative

    def ev(value, unit, method, source="JARVIS-DFT", derived_from=None):
        return Evidence(
            value=value,
            unit=unit,
            method=method,
            source=source,
            record_id=r.jid,
            url=record_url,
            retrieved_at=retrieved_at,
            derived_from=derived_from or [],
        )

    out: list[CriterionScore] = []

    # stability
    if r.e_hull is None:
        out.append(
            CriterionScore(name="stability", raw=None, score=None, weight=weights["stability"])
        )
    else:
        out.append(
            CriterionScore(
                name="stability",
                raw=ev(
                    r.e_hull,
                    "eV/atom",
                    "recomputed hull (D-013)",
                    "derived",
                    [f"formation_energy_peratom of {len(r.hull_decomposition)} phase(s) in system"],
                ),
                score=stability_score(r.e_hull, ranking_cfg["stability"]),
                weight=weights["stability"],
            )
        )

    # band gap
    gap, method = primary_gap(r)
    note = None
    if method == "OptB88vdW":
        note = "TBmBJ gap missing; OptB88vdW fallback is a probable underestimate (not corrected)."
    out.append(
        CriterionScore(
            name="band_gap",
            raw=ev(gap, "eV", method) if gap is not None else None,
            score=band_gap_score(gap, ranking_cfg["band_gap"]) if gap is not None else None,
            weight=weights["band_gap"],
            note=note,
        )
    )

    # hazard
    flags = hazards.flags_for(r.elements, haz_cfg)
    out.append(
        CriterionScore(
            name="hazard",
            raw=Evidence(
                value=",".join(f.element for f in flags) or "none",
                source="config",
                method="element-level flags (config/hazards.yaml)",
            ),
            score=hazard_score(len(flags), haz_cfg["penalty_per_flagged_element"]),
            weight=weights["hazard"],
            note="; ".join(f.note for f in flags if f.note) or None,
        )
    )

    # simplicity
    out.append(
        CriterionScore(
            name="simplicity",
            raw=ev(r.n_elements, "elements", "count of distinct elements"),
            score=simplicity_score(r.n_elements, ranking_cfg["simplicity"]),
            weight=weights["simplicity"],
        )
    )

    # dielectric (optional; weight 0 by default)
    k = r.kappa_total
    out.append(
        CriterionScore(
            name="dielectric",
            raw=ev(k, None, "DFPT total, max component") if k is not None else None,
            score=dielectric_score(k, ranking_cfg["dielectric"]) if k is not None else None,
            weight=weights.get("dielectric", 0.0),
        )
    )
    return combine(out)
