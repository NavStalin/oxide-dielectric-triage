"""Write the two data-flow diagrams: a simple one to learn from and a detailed one that maps to the code.

Run: make diagrams   (needs Graphviz `dot` on the PATH)

Outputs, all in docs/:
    dataflow_simple.dot / .svg / .png      eight boxes, plain words
    dataflow_detailed.dot / .svg / .png    every stage, its file, and the real counts

The .dot files are plain text. Edit one and re-run `dot -Tpng file.dot -o file.png` to build on it.
Counts come from the committed snapshot and the default request (see docs/DESIGN_NOTE.md section 2).
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

DOCS = Path(__file__).resolve().parents[1] / "docs"

# One colour per kind of thing, the same in both diagrams and in docs/architecture.svg.
CODE = 'fillcolor="#eef2f8" color="#3b5b8c"'  # deterministic code
MODEL = 'fillcolor="#fff4e6" color="#c46a00" style="rounded,filled,dashed"'  # optional model
DATA = 'fillcolor="#ecf6ee" color="#2f7a45"'  # public data
NET = 'fillcolor="#ecf6ee" color="#2f7a45" style="rounded,filled,dashed"'  # optional, online
OUT = 'fillcolor="#f3eefa" color="#6b4a9b"'  # input, file or output
RULES = 'fillcolor="#fdecec" color="#a33a3a"'  # site rules and safety

HEAD = """digraph dataflow {{
  graph [rankdir={rankdir} fontname="Helvetica" fontsize=13 labelloc=t pad=0.3 nodesep=0.35 ranksep=0.5
         label=<{title}>];
  node  [shape=box style="rounded,filled" fontname="Helvetica" fontsize=11 margin="0.14,0.08" penwidth=1.4];
  edge  [fontname="Helvetica" fontsize=9.5 color="#444444" arrowsize=0.7];
"""

LEGEND = f"""
  subgraph cluster_legend {{
    label="Key" fontsize=10 color="#bbbbbb" style=rounded;
    k1 [label="code (always the same answer)" {CODE}];
    k2 [label="AI model (optional, language only)" {MODEL}];
    k3 [label="public data" {DATA}];
    k4 [label="site rules and safety" {RULES}];
    k5 [label="what goes in or comes out" {OUT}];
    k1 -> k2 -> k3 -> k4 -> k5 [style=invis];
  }}
"""

SIMPLE = (
    HEAD.format(
        rankdir="TB",
        title="<b>How a request becomes a shortlist</b><br/><font point-size='10'>simple view</font>",
    )
    + f"""
  db      [label="Public database\\nJARVIS-DFT (NIST)" {DATA}];
  snap    [label="Checked local copy\\n(made once by the site admin)" {OUT}];
  ask     [label="Scientist types a request\\nin plain English" {OUT}];
  gate    [label="1. Safety gate\\nrefuses what isn't allowed,\\nkeeps the rest" {RULES}];
  read    [label="2. Understand the request\\nkeyword rules, or Claude if switched on" {MODEL}];
  rank    [label="3. Filter, score and rank\\nstability, band gap, hazard, simplicity" {CODE}];
  second  [label="4. Second opinion\\nAlexandria database (online, optional)" {NET}];
  conf    [label="5. Confidence, caveats, citations\\nhow far to trust each row" {CODE}];
  report  [label="6. Two reports\\nPI summary and audit view" {OUT}];
  person  [label="Scientist decides\\nwhat to run" {OUT}];
  rules   [label="Site rules\\n(config files; a request\\ncan't change them)" {RULES}];
  log     [label="Refusal log" {OUT}];

  db -> snap [label=" download, recompute stability,\\n sanity-check"];
  ask -> gate -> read -> rank -> second -> conf -> report -> person;
  snap -> rank [label=" read-only"];
  gate -> log [label=" refused parts"];
  rules -> gate [style=dashed];
  rules -> rank [style=dashed];
  {{ rank=same; snap; rank; }}
  {{ rank=same; gate; log; rules; }}
"""
    + LEGEND
    + "}\n"
)

DETAILED = (
    HEAD.format(
        rankdir="TB",
        title=(
            "<b>Data flow in detail</b><br/><font point-size='10'>each box: what happens, "
            "the file that does it, and the counts on the default request</font>"
        ),
    )
    + f"""
  subgraph cluster_admin {{
    label="A. Snapshot refresh — site admin, offline, `triage snapshot`" color="#bbbbbb" style=rounded fontsize=11;
    a1 [label="JARVIS-DFT dft_3d file\\nfigshare download + DOI\\n93,902 records" {DATA}];
    a2 [label="Keep records containing oxygen\\nsources/jarvis.py\\n25,194 records" {CODE}];
    a3 [label="Recompute energy above hull\\nhull.py (linear programme over\\nall 93,902 formation energies)" {CODE}];
    a4 [label="Sanity checks C1–C5\\nchecks.py + config/checks.yaml\\nknown stable oxides must sit on the hull" {RULES}];
    a5 [label="data/snapshot/\\noxides.parquet, manifest.json,\\nchecks_report.json" {OUT}];
    a1 -> a2 -> a3 -> a4;
    a4 -> a5 [label=" pass"];
    a4 -> a4x [label=" a blocking check fails"];
    a4x [label="Keep the previous snapshot" {RULES}];
  }}

  subgraph cluster_req {{
    label="B. Reading the request — every run" color="#bbbbbb" style=rounded fontsize=11;
    r0 [label="Request text" {OUT}];
    r1 [label="Normalise text\\npolicy.normalise()\\nfold look-alike letters, strip hidden\\ncharacters, cut at 2,000 characters" {RULES}];
    r2 [label="Policy gate\\npolicy.check() + config/policy.yaml\\n6 refusal categories, clause by clause" {RULES}];
    r3 [label="Parse to typed Criteria\\nproviders/rules.py (default)\\nproviders/llm.py (Claude, optional)" {MODEL}];
    r4 [label="Clamp to site limits\\npolicy.clamp()\\na request can tighten, never loosen" {RULES}];
    rlog [label="logs/audit.jsonl\\none line per refusal" {OUT}];
    r0 -> r1 -> r2;
    r2 -> r3 [label=" safe remainder"];
    r3 -> r4;
    r2 -> rlog [label=" refused clauses"];
  }}

  subgraph cluster_rank {{
    label="C. Deciding — code only, `run_triage()` in pipeline.py" color="#bbbbbb" style=rounded fontsize=11;
    c1 [label="Group by formula, pick the\\nlowest-energy polymorph\\ncandidates.py · 15,671 formulas" {CODE}];
    c2 [label="Filters\\n−4,156 non-oxide anions\\n−2,119 metals · −506 radioactive · −1 not an oxide" {CODE}];
    c2r [label="Set aside for review: 3,520\\nrare-earth and some 3d oxides,\\nDFT gap not trustworthy" {OUT}];
    c3 [label="Score suitability 0–1\\nscoring.py + config/ranking.yaml\\n5,369 formulas · missing data left out,\\nweights rescaled" {CODE}];
    c4 [label="Rank\\nties broken by evidence confidence\\nkeep the top N" {CODE}];
    c5 [label="Cross-check stability\\nsources/alexandria.py (or oqmd.py)\\nshortlist only · cached · one retry" {NET}];
    c5x [label="Source down: rows marked\\n'not cross-checked',\\nno value filled in" {RULES}];
    c6 [label="Confidence High / Medium / Low\\nconfidence.py + config/confidence.yaml\\npoints for method, ICSD, agreement" {CODE}];
    c7 [label="Caveats and citations\\npipeline.py\\nevery value keeps its record ID and URL" {CODE}];
    c1 -> c2 -> c3 -> c4 -> c5 -> c6 -> c7;
    c2 -> c2r;
    c5 -> c5x [style=dashed];
  }}

  subgraph cluster_out {{
    label="D. Reporting" color="#bbbbbb" style=rounded fontsize=11;
    o1 [label="Wording\\ntemplate sentences, or Claude if on:\\nevery number checked, no links allowed" {MODEL}];
    o2 [label="Render\\nrender/templates/*.j2\\ntyped-in text is escaped;\\ncaveats can't be switched off" {CODE}];
    o3 [label="PI summary · Audit view\\nMarkdown · JSON · execution trace" {OUT}];
    o4 [label="Scientist\\nargues with the working" {OUT}];
    o1 -> o2 -> o3 -> o4;
  }}

  cfg [label="config/*.yaml\\nsources · hazards · policy · candidates · ranking\\nconfidence · checks · output · terminology\\n(hashes recorded in every result)" {RULES}];
  alex [label="Alexandria OPTIMADE API\\npublic, no key, CC BY 4.0" {DATA}];

  a5 -> c1 [label=" read-only"];
  r4 -> c1 [label=" weights and filters"];
  c7 -> o1;
  alex -> c5 [style=dashed label=" only allowlisted hosts"];
  cfg -> r2 [style=dashed];
  cfg -> c3 [style=dashed];
  cfg -> c6 [style=dashed];
"""
    + LEGEND
    + "}\n"
)


def main() -> None:
    dot = shutil.which("dot")
    for name, src in (("dataflow_simple", SIMPLE), ("dataflow_detailed", DETAILED)):
        path = DOCS / f"{name}.dot"
        path.write_text(src)
        print(path)
        if not dot:
            print("  Graphviz `dot` not found; wrote the .dot file only.")
            continue
        for fmt, extra in (("svg", []), ("png", ["-Gdpi=160"])):
            out = DOCS / f"{name}.{fmt}"
            subprocess.run([dot, f"-T{fmt}", *extra, str(path), "-o", str(out)], check=True)
            print(out)


if __name__ == "__main__":
    main()
