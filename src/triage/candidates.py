"""From snapshot records to candidates: hard filters, grouping by formula, representative polymorph.

Hard filters remove what cannot do the job (not an oxide, excluded element, metal). Everything else is
a preference and belongs in scoring.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Any

from triage import hazards
from triage.models import Candidate, MaterialRecord


@dataclass
class FilterReport:
    records_in: int = 0
    formulas_in: int = 0
    dropped: Counter = field(default_factory=Counter)  # reason -> number of formulas
    needs_review: int = 0  # kept but not ranked (D-030)
    formulas_out: int = 0  # ranked


def primary_gap(r: MaterialRecord) -> tuple[float | None, str | None]:
    """TBmBJ if present, else OptB88vdW (a probable underestimate). Never corrected (D-004)."""
    if r.gap_mbj is not None:
        return r.gap_mbj, "TBmBJ"
    if r.gap_optb88 is not None:
        return r.gap_optb88, "OptB88vdW"
    return None, None


def formula_exclusion(
    elements: list[str], cand_cfg: dict[str, Any], haz_cfg: dict[str, Any]
) -> str | None:
    if "O" not in elements or len(elements) < 2:
        return "not an oxide"
    if any(hazards.is_excluded_element(e, haz_cfg) for e in elements):
        return "element with no stable isotopes"
    extra = set(elements) & set(cand_cfg["excluded_anion_elements"])
    if extra and not cand_cfg["allow_extra_anions"]:
        return "contains H, C, N, S or halogen"
    return None


def _rep_sort_key(r: MaterialRecord, best_e: float, tol: float) -> tuple:
    tied = r.e_hull is not None and r.e_hull <= best_e + tol
    return (
        0 if tied else 1,
        r.e_hull if not tied and r.e_hull is not None else 0.0,
        0 if r.has_icsd else 1,
        0 if r.gap_mbj is not None else 1,
        r.formation_energy_peratom if r.formation_energy_peratom is not None else 0.0,
        r.jid,
    )


def pick_representative(
    polys: list[MaterialRecord], cand_cfg: dict[str, Any]
) -> list[MaterialRecord]:
    """Order polymorphs: representative first. Lowest hull; near-ties prefer ICSD, then TBmBJ."""
    with_hull = [p for p in polys if p.e_hull is not None]
    best_e = min((p.e_hull for p in with_hull), default=0.0)
    tol = cand_cfg["tie_tolerance_ev"]
    ordered = sorted(with_hull, key=lambda r: _rep_sort_key(r, best_e, tol))
    ordered += sorted((p for p in polys if p.e_hull is None), key=lambda r: r.jid)
    return ordered


def known_phase_note(ordered: list[MaterialRecord], cand_cfg: dict[str, Any]) -> str | None:
    rep = ordered[0]
    if rep.has_icsd or rep.e_hull is None:
        return None
    window = cand_cfg["known_phase_window_ev"]
    for p in ordered[1:]:
        if p.has_icsd and p.e_hull is not None and p.e_hull - rep.e_hull <= window:
            dmev = (p.e_hull - rep.e_hull) * 1000
            return (
                f"Representative {rep.jid} ({rep.spg_symbol}) has no ICSD reference; "
                f"{p.jid} ({p.spg_symbol}) is {dmev:.0f} meV/atom higher and has one."
            )
    return None


def build_candidates(
    records: list[MaterialRecord], cand_cfg: dict[str, Any], haz_cfg: dict[str, Any]
) -> tuple[list[Candidate], FilterReport]:
    rep = FilterReport(records_in=len(records))
    groups: dict[str, list[MaterialRecord]] = {}
    for r in records:
        groups.setdefault(r.formula, []).append(r)
    rep.formulas_in = len(groups)

    out: list[Candidate] = []
    for formula, polys in groups.items():
        reason = formula_exclusion(polys[0].elements, cand_cfg, haz_cfg)
        if reason is None and cand_cfg.get("allowed_dimensionality"):
            polys = [p for p in polys if p.dimensionality in cand_cfg["allowed_dimensionality"]]
            if not polys:
                reason = "dimensionality not allowed"
        review = None
        if reason is None:
            ordered = pick_representative(polys, cand_cfg)
            gap, _ = primary_gap(ordered[0])
            if cand_cfg["exclude_metals"] and gap is not None and gap <= 0.0:
                if zero_gap_unreliable(ordered[0].elements, cand_cfg):
                    review = UNRELIABLE_GAP_REASON
                else:
                    reason = "metal (no band gap)"
        if reason:
            rep.dropped[reason] += 1
            continue
        if review:
            rep.needs_review += 1
        out.append(
            Candidate(
                formula=formula,
                representative=ordered[0],
                polymorphs=ordered,
                known_phase_note=known_phase_note(ordered, cand_cfg),
                status="needs_review" if review else "ranked",
                review_reason=review,
            )
        )
    rep.formulas_out = sum(1 for c in out if c.status == "ranked")
    return out, rep


UNRELIABLE_GAP_REASON = (
    "DFT gives zero band gap, but the compound contains an f-electron or open-shell 3d element, "
    "where these methods often wrongly predict a metal (D-030). Not ranked; gap unknown."
)


def zero_gap_unreliable(elements: list[str], cand_cfg: dict[str, Any]) -> bool:
    return bool(set(elements) & set(cand_cfg.get("unreliable_zero_gap_elements", [])))
