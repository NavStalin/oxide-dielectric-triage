"""Known-answer sanity checks (D-022). Deterministic; expected values come from config/checks.yaml."""

from __future__ import annotations

from typing import Any

import pandas as pd

from triage import hazards
from triage.models import Candidate, CheckResult


def _lowest_phase(df: pd.DataFrame, formula: str, spgs: list[str], col: str):
    rows = df[(df["formula"] == formula) & (df["spg_symbol"].isin(spgs)) & df[col].notna()]
    if rows.empty:
        return None
    return rows.sort_values(col).iloc[0]


def known_states(
    df: pd.DataFrame, cfg: dict[str, Any], col: str, cid: str, severity
) -> CheckResult:
    tol = cfg["tolerance_ev"]
    details, ok = [], True
    for formula, spgs in cfg["materials"].items() if "materials" in cfg else []:
        row = _lowest_phase(df, formula, list(spgs), col)
        if row is None:
            details.append({"formula": formula, "status": "not found", "spg": spgs})
            ok = False
            continue
        val = float(row[col])
        passed = val <= tol
        ok &= passed
        details.append(
            {
                "formula": formula,
                "jid": row["jid"],
                "spg": row["spg_symbol"],
                "value_ev": round(val, 4),
                "passed": passed,
            }
        )
    n_pass = sum(1 for d in details if d.get("passed"))
    return CheckResult(
        id=cid,
        severity=severity,
        passed=ok,
        summary=f"{n_pass}/{len(details)} known ground states within {tol * 1000:.0f} meV/atom ({col})",
        rationale=cfg["rationale"],
        details=details,
    )


def c1(df, cfg) -> CheckResult:
    return known_states(df, cfg["C1_known_ground_states"], "e_hull", "C1", "fail")


def c2(df, cfg) -> CheckResult:
    c = dict(cfg["C2_raw_ehull_field"])
    c["materials"] = cfg["C1_known_ground_states"]["materials"]
    return known_states(df, c, "jarvis_ehull_raw", "C2", "report")


def c3(df, cfg) -> CheckResult:
    c = cfg["C3_gap_method_order"]
    both = df[df["gap_mbj"].notna() & df["gap_optb88"].notna()]
    bad = both[both["gap_mbj"] < both["gap_optb88"] - c["slack_ev"]]
    return CheckResult(
        id="C3",
        severity="warn",
        passed=bad.empty,
        summary=f"{len(bad)}/{len(both)} records have TBmBJ gap below OptB88vdW gap by > {c['slack_ev']} eV",
        rationale=c["rationale"],
        details=[
            {"jid": r.jid, "formula": r.formula, "gap_mbj": r.gap_mbj, "gap_optb88": r.gap_optb88}
            for r in bad.itertuples()
        ],
    )


def c4(df, cfg) -> CheckResult:
    c = cfg["C4_coverage"]
    cols = {
        "mbj_bandgap": "gap_mbj",
        "icsd": "has_icsd",
        "dfpt_piezo_max_dielectric": "kappa_total",
    }
    details, ok = [], True
    for raw_name, (lo, hi) in c["bands"].items():
        col = cols[raw_name]
        frac = (
            float(df[col].astype(bool).mean())
            if col == "has_icsd"
            else float(df[col].notna().mean())
        )
        passed = lo <= frac <= hi
        ok &= passed
        details.append(
            {"field": raw_name, "fraction": round(frac, 4), "band": [lo, hi], "passed": passed}
        )
    return CheckResult(
        id="C4",
        severity="fail",
        passed=ok,
        summary="; ".join(f"{d['field']} {d['fraction']:.1%}" for d in details),
        rationale=c["rationale"],
        details=details,
    )


def c5(cands: list[Candidate], cand_cfg, haz_cfg, cfg) -> CheckResult:
    bad = []
    for cand in cands:
        els = cand.representative.elements
        if any(hazards.is_excluded_element(e, haz_cfg) for e in els):
            bad.append({"formula": cand.formula, "reason": "no-stable-isotope element"})
        if not cand_cfg["allow_extra_anions"] and set(els) & set(
            cand_cfg["excluded_anion_elements"]
        ):
            bad.append({"formula": cand.formula, "reason": "excluded anion element"})
        if "O" not in els:
            bad.append({"formula": cand.formula, "reason": "no oxygen"})
    return CheckResult(
        id="C5",
        severity="fail",
        passed=not bad,
        summary=f"{len(bad)} candidates violate the element filters ({len(cands)} checked)",
        rationale=cfg["C5_no_excluded_elements"]["rationale"],
        details=bad,
    )
