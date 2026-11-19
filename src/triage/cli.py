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


@app.command("query")
def query(
    request: str = typer.Argument(..., help="Free-text request, e.g. the example in the README."),
    style: str = typer.Option(None, help="pi or audit (default from config/output.yaml)."),
    fmt: str = typer.Option("md", "--format", help="md or json."),
    out: str = typer.Option(None, help="Write to this file instead of stdout."),
    provider: str = typer.Option("rules", help="rules (default) or llm (needs ANTHROPIC_API_KEY)."),
    top: int = typer.Option(None, help="Shortlist size."),
    offline: bool = typer.Option(False, help="Skip the OQMD cross-check."),
) -> None:
    """Scientist: run a triage request and print the PI summary or audit view."""
    from triage.pipeline import run_triage
    from triage.render import render, to_json

    overrides = {}
    if style:
        overrides["style"] = style
    if top:
        overrides["shortlist_size"] = top
    result = run_triage(
        request, provider=provider, overrides=overrides, oqmd_enabled=False if offline else None
    )
    text = to_json(result) if fmt == "json" else render(result, style)
    if out:
        from pathlib import Path

        Path(out).write_text(text)
        typer.echo(f"wrote {out}")
    else:
        typer.echo(text)


@app.command("config-show")
def config_show() -> None:
    """Admin/field engineer: print the active configuration files and their hashes."""
    for name in [
        "ranking",
        "candidates",
        "hazards",
        "sources",
        "policy",
        "confidence",
        "output",
        "terminology",
        "checks",
    ]:
        typer.echo(f"--- config/{name}.yaml ({config.file_hash(name)})")
        typer.echo((config.CONFIG_DIR / f"{name}.yaml").read_text())


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
