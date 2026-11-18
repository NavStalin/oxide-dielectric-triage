"""Command line: `triage snapshot`, `triage preview` (Milestone 1). `query` arrives in Milestone 2."""

from __future__ import annotations

import typer

from triage import config, scoring
from triage.candidates import build_candidates, primary_gap
from triage.snapshot import load_records, snapshot

app = typer.Typer(no_args_is_help=True, add_completion=False)


@app.command("snapshot")
def snapshot_cmd() -> None:
    """Admin: fetch JARVIS (or use the cached file), recompute hull, run checks, write data/snapshot/."""
    ok, manifest, results = snapshot()
    for r in results:
        mark = "PASS" if r.passed else ("FAIL" if r.severity == "fail" else r.severity.upper())
        typer.echo(f"[{mark}] {r.id}: {r.summary}")
    typer.echo(f"counts: {manifest['counts']}")
    typer.echo(f"candidates (default config): {manifest['candidates_default_config']}")
    typer.echo(f"hull runtime: {manifest['hull']['runtime_s']} s")
    if not ok:
        typer.echo("Snapshot NOT replaced: a fail-severity check failed. See data/snapshot.tmp/.")
        raise typer.Exit(1)
    typer.echo("Snapshot written to data/snapshot/")


@app.command("preview")
def preview(top: int = 20) -> None:
    """Dev: default ranking, no cross-check or confidence yet."""
    recs, _manifest = load_records()
    rank_cfg, cand_cfg, haz_cfg = (
        config.load("ranking"),
        config.load("candidates"),
        config.load("hazards"),
    )
    cands, frep = build_candidates(recs, cand_cfg, haz_cfg)
    cands = [c for c in cands if c.status == "ranked"]
    typer.echo(f"ranked: {frep.formulas_out}  needs review (D-030): {frep.needs_review}")
    scored = [
        (scoring.score_candidate(c, rank_cfg["weights"], rank_cfg, haz_cfg), c) for c in cands
    ]
    scored.sort(key=lambda t: (-t[0].total, t[1].formula))
    typer.echo(
        f"{'#':>3} {'formula':<14}{'suit':>6} {'e_hull meV':>10} {'gap':>6} {'method':<10} {'icsd':<5} spg"
    )
    for i, (s, c) in enumerate(scored[:top], 1):
        r = c.representative
        gap, method = primary_gap(r)
        typer.echo(
            f"{i:>3} {c.formula:<14}{s.total:>6.3f} {r.e_hull * 1000:>10.0f} "
            f"{gap if gap is not None else float('nan'):>6.2f} {method or '-':<10} "
            f"{'yes' if r.has_icsd else 'no':<5} {r.spg_symbol}"
        )
