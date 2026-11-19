"""Eval 4: where the well-known gate dielectrics land on default settings. A report, not pass/fail.

Every position is explained from the stored per-criterion contributions and record values. Nothing
here is tuned: if a familiar material ranks low, the report says why, and that is the finding.

Run: uv run python -m evals.face_validity
"""

from __future__ import annotations

import json
from pathlib import Path

from triage import config, scoring
from triage.candidates import build_candidates, primary_gap
from triage.pipeline import _records, _settings, rank_offline

TARGETS = ["HfO2", "ZrO2", "Al2O3", "Y2O3", "SiO2", "La2O3"]
RESULTS = Path(__file__).parent / "results"


def _lost_points(su) -> list[tuple[str, float]]:
    """Suitability lost per criterion: effective weight x (1 - score), largest first."""
    out = [
        (c.name, c.effective_weight * (1 - c.score))
        for c in su.criteria
        if c.score is not None and c.effective_weight > 0
    ]
    return sorted([x for x in out if x[1] > 0.0005], key=lambda x: -x[1])


def _why(cand, su, conf, rank: int, top_score: float, n_top: int) -> str:
    r = cand.representative
    g, method = primary_gap(r)
    parts: list[str] = []
    if rank <= n_top:
        parts.append(
            f"Scores the maximum suitability ({top_score:.3f}) along with {n_top - 1} others"
        )
    lost = _lost_points(su)
    if lost:
        parts.append(
            "Loses "
            + ", ".join(f"{v:.3f} on {k.replace('_', ' ')}" for k, v in lost)
            + f" (total {su.total:.3f})"
        )
    if method == "OptB88vdW":
        alt = [p for p in cand.polymorphs if p.gap_mbj is not None]
        txt = f"Representative {r.jid} has no TBmBJ gap, so the OptB88vdW fallback ({g:.2f} eV) is scored"
        if alt:
            best = min(alt, key=lambda p: p.e_hull if p.e_hull is not None else 9.0)
            txt += (
                f"; the lowest-energy polymorph that has one, {best.jid} ({best.spg_symbol}, "
                f"{(best.e_hull or 0) * 1000:.0f} meV/atom above hull), has TBmBJ {best.gap_mbj:.2f} eV"
            )
        parts.append(txt)
    if cand.known_phase_note:
        parts.append(cand.known_phase_note)
    parts.append(f"Confidence {conf.level} (points: {conf.points})")
    return ". ".join(p.rstrip(".") for p in parts) + "."


def report(snapshot_dir: Path | None = None) -> dict:
    s = _settings()
    recs, manifest = _records(str(snapshot_dir or config.SNAPSHOT_DIR))
    cand_cfg = dict(s["candidates"], allow_extra_anions=False)
    cands, _ = build_candidates(list(recs), cand_cfg, s["hazards"])
    by_formula = {c.formula: c for c in cands}
    weights = dict(s["ranking"]["weights"])
    ranked_pool = [c for c in cands if c.status == "ranked"]
    ranked = rank_offline(
        [(c, scoring.score_candidate(c, weights, s["ranking"], s["hazards"])) for c in ranked_pool],
        s,
    )
    top_score = round(ranked[0][1].total, 3)
    n_top = sum(1 for _, su, _ in ranked if round(su.total, 3) == top_score)
    pos = {c.formula: (i, c, su, conf) for i, (c, su, conf) in enumerate(ranked, 1)}

    rows = []
    for f in TARGETS:
        if f in pos:
            i, c, su, conf = pos[f]
            r = c.representative
            g, method = primary_gap(r)
            rows.append(
                {
                    "formula": f,
                    "rank": i,
                    "of": len(ranked),
                    "suitability": round(su.total, 3),
                    "confidence": conf.level,
                    "representative": f"{r.jid} {r.spg_symbol}",
                    "e_hull_meV": round((r.e_hull or 0) * 1000),
                    "band_gap_eV": round(g, 2) if g is not None else None,
                    "gap_method": method,
                    "has_icsd": r.has_icsd,
                    "contributions": {
                        x.name: round(x.contribution, 3)
                        for x in su.criteria
                        if x.effective_weight > 0
                    },
                    "why": _why(c, su, conf, i, top_score, n_top),
                }
            )
        elif f in by_formula:
            c = by_formula[f]
            rows.append({"formula": f, "rank": None, "why": f"Not ranked: {c.review_reason}"})
        else:
            rows.append(
                {"formula": f, "rank": None, "why": "Not a candidate: removed by the filters"}
            )
    return {
        "settings": "default weights, no request filters, rank by suitability then confidence",
        "weights": weights,
        "ranked_formulas": len(ranked),
        "top_score": top_score,
        "formulas_at_top_score": n_top,
        "snapshot_built_at": manifest.get("snapshot_built_at"),
        "rows": rows,
    }


def to_markdown(rep: dict) -> str:
    lines = [
        "# Eval 4: face validity (report, not pass/fail)",
        "",
        f"Settings: {rep['settings']}. Weights: {rep['weights']}.",
        (
            f"{rep['ranked_formulas']} formulas ranked; {rep['formulas_at_top_score']} share the top "
            f"score of {rep['top_score']:.3f}. Snapshot built {rep['snapshot_built_at']}."
        ),
        "",
        "| Formula | Rank | Suitability | Confidence | Representative | Hull (meV/atom) | Gap (eV) | ICSD |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in rep["rows"]:
        if r["rank"] is None:
            lines.append(f"| {r['formula']} | not ranked | | | | | | |")
            continue
        gap = (
            "missing" if r["band_gap_eV"] is None else f"{r['band_gap_eV']:.2f} ({r['gap_method']})"
        )
        lines.append(
            f"| {r['formula']} | {r['rank']} of {r['of']} | {r['suitability']:.3f} | {r['confidence']} "
            f"| {r['representative']} | {r['e_hull_meV']} | {gap} | {'yes' if r['has_icsd'] else 'no'} |"
        )
    lines += ["", "## Why each one lands where it does", ""]
    for r in rep["rows"]:
        lines.append(f"- **{r['formula']}**: {r['why']}")
    lines += [
        "",
        "Weights were not changed to move any of these. A low rank is reported as a finding.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    rep = report()
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "eval_4_face_validity.json").write_text(json.dumps(rep, indent=2))
    md = to_markdown(rep)
    (RESULTS / "eval_4_face_validity.md").write_text(md)
    print(md)


if __name__ == "__main__":
    main()
