"""Render a TriageResult as Markdown (PI summary or audit view) or JSON. Labels come from config."""

from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from triage import config
from triage.candidates import primary_gap
from triage.models import TriageResult

TEMPLATES = Path(__file__).parent / "templates"


def _env() -> Environment:
    env = Environment(
        loader=FileSystemLoader(TEMPLATES),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    env.filters["mev"] = lambda ev: "missing" if ev is None else f"{ev * 1000:.0f}"
    env.filters["num"] = lambda x, d=2: "missing" if x is None else f"{x:.{d}f}"
    env.filters["val"] = lambda x: f"{x:.3g}" if isinstance(x, float) else str(x)
    env.filters["cell"] = lambda s: str(s).replace("|", "/").replace("\n", " ")
    env.globals["primary_gap"] = primary_gap
    return env


def render(result: TriageResult, style: str | None = None) -> str:
    style = style or result.settings["style"]
    out = config.load("output")
    ctx = {
        "r": result,
        "L": config.load("terminology")["labels"],
        "out": out,
        "n": out["shortlist"]["pi"] if style == "pi" else len(result.ranked),
    }
    return _env().get_template(f"{style}.md.j2").render(**ctx)


def to_json(result: TriageResult) -> str:
    return result.model_dump_json(indent=2)
