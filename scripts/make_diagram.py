"""Generate docs/architecture.svg (the design note's one diagram). Run: uv run python scripts/make_diagram.py"""

from pathlib import Path

W, H = 1110, 600
BW, BH = 180, 64
COL = [270, 480, 690, 900]
ROW = {"A": 70, "B": 235, "C": 400}

STYLE = {
    "code": ("#eef2f8", "#3b5b8c", ""),
    "model": ("#fff4e6", "#c46a00", "6 4"),
    "source": ("#ecf6ee", "#2f7a45", ""),
    "optsource": ("#ecf6ee", "#2f7a45", "6 4"),
    "out": ("#f3eefa", "#6b4a9b", ""),
}

parts: list[str] = []


def box(x, y, lines, kind="code", w=BW, h=BH):
    fill, stroke, dash = STYLE[kind]
    d = f' stroke-dasharray="{dash}"' if dash else ""
    parts.append(
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="1.6"{d}/>'
    )
    n = len(lines)
    for i, ln in enumerate(lines):
        ty = y + h / 2 + (i - (n - 1) / 2) * 15 + 4.5
        weight = ' font-weight="600"' if i == 0 else ""
        size = 13 if i == 0 else 11.5
        parts.append(
            f'<text x="{x + w / 2}" y="{ty}" text-anchor="middle" font-size="{size}"{weight}>{ln}</text>'
        )


def arrow(pts, dashed=False, label=None, lx=None, ly=None):
    d = " ".join(f"{'M' if i == 0 else 'L'}{x},{y}" for i, (x, y) in enumerate(pts))
    da = ' stroke-dasharray="5 4"' if dashed else ""
    parts.append(
        f'<path d="{d}" fill="none" stroke="#444" stroke-width="1.4"{da} marker-end="url(#a)"/>'
    )
    if label:
        parts.append(f'<text x="{lx}" y="{ly}" font-size="11" fill="#444">{label}</text>')


def right(c, r):
    return (COL[c] + BW, ROW[r] + BH / 2)


def left(c, r):
    return (COL[c], ROW[r] + BH / 2)


# lanes
parts.append('<rect x="10" y="40" width="225" height="420" rx="10" fill="#fafafa" stroke="#bbb"/>')
parts.append('<text x="122" y="32" text-anchor="middle" font-size="13" font-weight="700">Admin: snapshot refresh (offline)</text>')
parts.append('<rect x="250" y="40" width="850" height="455" rx="10" fill="#fcfcfc" stroke="#bbb"/>')
parts.append('<text x="675" y="32" text-anchor="middle" font-size="13" font-weight="700">Per request: run_triage() — one code path for CLI, Streamlit app and evals</text>')

# admin column
box(32, 58, ["JARVIS-DFT dft_3d", "figshare file + DOI", "93,902 records"], "source", w=180, h=62)
box(32, 145, ["Recompute hull", "LP over formation energies", "(raw ehull kept, not scored)"], w=180, h=62)
box(32, 232, ["Sanity checks C1–C5", "known ground states on hull", "fail → keep old snapshot"], w=180, h=62)
box(32, 340, ["data/snapshot/", "oxides.parquet + manifest", "+ checks report"], "out", w=180, h=62)
arrow([(122, 120), (122, 145)])
arrow([(122, 207), (122, 232)])
arrow([(122, 294), (122, 340)])

# row A
box(270, ROW["A"], ["Request text", "free English"], "out")
box(480, ROW["A"], ["Policy gate", "regex categories", "partial refusal"])
box(690, ROW["A"], ["Parse to typed Criteria", "rules (default)", "Claude (optional, language only)"], "model")
box(900, ROW["A"], ["Clamp", "policy limits; request can't", "loosen rules"])
arrow([right(0, "A"), left(1, "A")])
arrow([right(1, "A"), left(2, "A")])
arrow([right(2, "A"), left(3, "A")])
parts.append(f'<text x="600" y="{ROW["A"] + BH + 18}" text-anchor="middle" font-size="11" fill="#444">refusals → output + logs/audit.jsonl; safe remainder → parser</text>')

# A -> B connector
arrow([(990, ROW["A"] + BH), (990, 175), (360, 175), (360, ROW["B"])])

# row B
box(270, ROW["B"], ["Candidates + filters", "pure oxides; metals out", "unreliable DFT → review list"])
box(480, ROW["B"], ["Score suitability 0–1", "weighted; missing renormalised", "(requested criterion needs data)"])
box(690, ROW["B"], ["Rank", "ties broken by", "evidence confidence"])
box(900, ROW["B"], ["Alexandria cross-check", "shortlist only; 1 retry;", "failure named, never filled"], "optsource")
arrow([right(0, "B"), left(1, "B")])
arrow([right(1, "B"), left(2, "B")])
arrow([right(2, "B"), left(3, "B")])
# snapshot -> candidates
arrow([(212, 371), (245, 371), (245, ROW["B"] + 50), (270, ROW["B"] + 50)], label="read-only", lx=176, ly=330)

# B -> C connector
arrow([(990, ROW["B"] + BH), (990, 340), (360, 340), (360, ROW["C"])])

# row C
box(270, ROW["C"], ["Confidence + caveats", "points rubric; citations", "on every value"])
box(480, ROW["C"], ["Explanations", "template wording; optional", "Claude, every number checked"], "model")
box(690, ROW["C"], ["Render", "PI summary · audit view", "Markdown · JSON"], "out")
box(900, ROW["C"], ["Scientist", "argues with the working,", "decides what to run"], "out")
arrow([right(0, "C"), left(1, "C")])
arrow([right(1, "C"), left(2, "C")])
arrow([right(2, "C"), left(3, "C")])

# config note
parts.append('<rect x="270" y="478" width="810" height="0" fill="none"/>')
parts.append(
    '<text x="675" y="485" text-anchor="middle" font-size="11.5" fill="#333">'
    "config/*.yaml (sources, hazards, policy, ranking, confidence, checks, output, terminology) parameterises every step; no request can edit it."
    "</text>"
)

# legend
lx, ly = 20, 520
items = [("code", "deterministic code"), ("model", "model: language only, optional"), ("source", "public data source"), ("optsource", "optional / network"), ("out", "input, artifact or output")]
for kind, label in items:
    fill, stroke, dash = STYLE[kind]
    d = f' stroke-dasharray="{dash}"' if dash else ""
    parts.append(f'<rect x="{lx}" y="{ly}" width="26" height="16" rx="4" fill="{fill}" stroke="{stroke}" stroke-width="1.5"{d}/>')
    parts.append(f'<text x="{lx + 34}" y="{ly + 12.5}" font-size="12">{label}</text>')
    lx += 34 + len(label) * 6.6 + 30
parts.append(
    '<text x="20" y="572" font-size="11.5" fill="#333">Production: an HTTP API layer would wrap run_triage() with auth and a job queue; '
    "the library, config and snapshot stay as they are. The app runs with no network and no API key once a snapshot exists.</text>"
)

svg = (
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    'font-family="Helvetica, Arial, sans-serif" fill="#1a1a1a">'
    '<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
    '<path d="M0,0 L10,5 L0,10 z" fill="#444"/></marker></defs>'
    '<rect width="100%" height="100%" fill="white"/>' + "".join(parts) + "</svg>"
)
out = Path(__file__).resolve().parents[1] / "docs" / "architecture.svg"
out.write_text(svg)
print(out)
