"""Under the hood: the path the last run took, where each number came from, and the fixed site rules.

Read-only. Nothing on this page changes a result or a setting.
"""

from __future__ import annotations

import json

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from triage import config

DOCS = config.ROOT / "docs"
res = st.session_state.get("result")

st.title("Under the hood")
st.caption(
    "How a result was produced. Read-only: nothing here changes a result, a setting or a rule."
)
st.page_link("views/triage.py", label="Back to triage", icon=":material/arrow_back:")

tab_run, tab_num, tab_flow, tab_rules, tab_log = st.tabs(
    ["This run", "Where each number came from", "Data flow", "Site rules", "Refusal log"]
)

# ---------- the path of the last run -------------------------------------------------------------

with tab_run:
    if res is None:
        st.info("Run a triage first. This tab then shows every step that run took.")
    else:
        st.markdown(f"**Request as read:** `{res.request.replace('`', "'")}`")
        st.caption(
            f"Run at {res.created_at} · parser {res.settings['provider']} · "
            f"cross-check ({res.settings['crosscheck_source']}) "
            f"{'on' if res.settings['crosscheck_enabled'] else 'off'}"
        )

        st.subheader("Steps, in order")
        steps = pd.DataFrame(
            [
                {"#": i, "Step": t.step, "Time (ms)": t.ms, "What it did": t.detail}
                for i, t in enumerate(res.trace, 1)
            ]
        )
        total_ms = float(steps["Time (ms)"].sum())
        st.dataframe(
            steps,
            hide_index=True,
            width="stretch",
            column_config={
                "#": st.column_config.NumberColumn(width="small"),
                "Time (ms)": st.column_config.ProgressColumn(
                    min_value=0.0, max_value=max(total_ms, 1.0), format="%.1f"
                ),
                "What it did": st.column_config.TextColumn(width="large"),
            },
        )
        st.caption(f"Total {total_ms:,.0f} ms. Every run records these steps in its JSON export.")

        st.subheader("How the list narrowed")
        fc = res.filter_counts
        stages, values = ["Formulas containing oxygen"], [fc["formulas"]]
        left = fc["formulas"]
        for k, v in fc.items():
            if k.startswith("dropped"):
                left -= v
                stages.append("after removing: " + k.removeprefix("dropped: "))
                values.append(left)
        stages += ["Ranked (rest set aside for review)", "Shortlist shown"]
        values += [fc["ranked"], len(res.ranked)]
        fig = go.Figure(
            go.Funnel(
                y=stages,
                x=values,
                texttemplate="%{x:,}",
                marker={"color": "#3b5b8c"},
            )
        )
        fig.update_layout(height=90 + 46 * len(stages), margin={"t": 10, "b": 10, "l": 10})
        st.plotly_chart(fig, width="stretch")
        st.caption(
            f"{fc['needs review (not ranked)']:,} formulas are set aside for review, not ranked: "
            "DFT gives them a zero gap, but for their elements that is unreliable."
        )

        with st.expander("Settings and config versions this run used"):
            st.json(res.settings)

# ---------- provenance of each displayed value ---------------------------------------------------

with tab_num:
    if res is None or not res.ranked:
        st.info("Run a triage first. This tab then traces each number back to its record.")
    else:
        pick = st.selectbox(
            "Material", [rc.candidate.formula for rc in res.ranked], key="lineage_formula"
        )
        rc = next(x for x in res.ranked if x.candidate.formula == pick)
        rows = []
        for k in rc.suitability.criteria:
            e = k.raw
            rows.append(
                {
                    "Used for": f"score: {k.name.replace('_', ' ')}",
                    "Value": "missing" if e is None or e.value is None else str(e.value),
                    "Unit": e.unit if e else None,
                    "Method": e.method if e else None,
                    "Source": e.source if e else None,
                    "Record": e.record_id if e else None,
                    "Link": e.url if e else None,
                    "Derived from": "; ".join(e.derived_from) if e else None,
                }
            )
        if rc.cross_check.ref_stability is not None:
            e = rc.cross_check.ref_stability
            rows.append(
                {
                    "Used for": "confidence: cross-check",
                    "Value": str(e.value),
                    "Unit": e.unit,
                    "Method": e.method,
                    "Source": e.source,
                    "Record": e.record_id,
                    "Link": e.url,
                    "Derived from": f"retrieved {e.retrieved_at}",
                }
            )
        for c in rc.citations:
            rows.append(
                {
                    "Used for": "citation",
                    "Value": str(c.value),
                    "Unit": c.unit,
                    "Method": c.method,
                    "Source": c.source,
                    "Record": c.record_id,
                    "Link": c.url,
                    "Derived from": f"retrieved {c.retrieved_at}" if c.retrieved_at else None,
                }
            )
        st.dataframe(
            pd.DataFrame(rows),
            hide_index=True,
            width="stretch",
            column_config={"Link": st.column_config.LinkColumn(display_text="open")},
        )
        st.caption(
            'Source "derived" means the tool computed the value from the records named in '
            '"Derived from". Source "config" means a cited list kept by the site admin.'
        )
        st.markdown(f"**Cross-check:** {rc.cross_check.status.replace('_', ' ')}. ")
        st.text(rc.cross_check.detail)

# ---------- the diagrams ---------------------------------------------------------------------------

with tab_flow:
    which = st.segmented_control("View", ["Simple", "Detailed"], default="Simple", key="flow_view")
    name = "dataflow_detailed" if which == "Detailed" else "dataflow_simple"
    png = DOCS / f"{name}.png"
    if png.exists():
        st.image(str(png), width="stretch")
        c1, c2, _ = st.columns([1, 1, 4])
        c1.download_button("Download PNG", png.read_bytes(), png.name, "image/png")
        dot = DOCS / f"{name}.dot"
        if dot.exists():
            c2.download_button("Download editable .dot", dot.read_text(), dot.name, "text/plain")
        st.caption(
            "Blue = code, which always gives the same answer. Dashed orange = the optional AI "
            "model, language only. Green = public data. Red = site rules and safety. "
            "Rebuild with `make diagrams`."
        )
    else:
        st.info("Diagram not found. Build it with `make diagrams` (needs Graphviz).")

# ---------- what a request can never change ------------------------------------------------------

with tab_rules:
    st.markdown(
        "These come from `config/*.yaml`, which only the site admin edits. "
        "**No request, slider or model output can change them.**"
    )
    src, pol, haz, cand = (config.load(n) for n in ("sources", "policy", "hazards", "candidates"))
    a, b = st.columns(2)
    with a:
        st.markdown("**Hosts the tool may fetch from**")
        st.markdown("\n".join(f"- `{h}`" for h in src["allowed_hosts"]))
        st.markdown("**Hosts a citation link may point to**")
        st.markdown("\n".join(f"- `{h}`" for h in src["citation_hosts"]))
    with b:
        st.markdown("**Limits**")
        st.markdown(
            f"- Largest shortlist: {pol['limits']['max_shortlist']}\n"
            f"- Longest request: {pol['limits']['max_request_chars']:,} characters\n"
            f"- Extra anions (H, C, N, S, halogens) on request: "
            f"{'allowed' if pol['limits']['allow_user_extra_anions'] else 'never'}\n"
            f"- Excluded anion elements: {', '.join(cand['excluded_anion_elements'])}\n"
            f"- Elements flagged as hazards: {', '.join(haz['flags'])}\n"
            f"- Stability cross-check source: {src['cross_check']['source']}"
        )
    st.markdown("**What gets refused, and what the user is told**")
    st.dataframe(
        pd.DataFrame(
            [
                {
                    "Category": name.replace("_", " "),
                    "Reply": spec["message"],
                    "Patterns": len(spec["patterns"]),
                }
                for name, spec in pol["categories"].items()
            ]
        ),
        hide_index=True,
        width="stretch",
    )
    st.markdown("**Config versions in force**")
    st.dataframe(
        pd.DataFrame(
            [
                {"File": f"config/{n}.yaml", "Hash": config.file_hash(n)}
                for n in (
                    "sources",
                    "policy",
                    "hazards",
                    "candidates",
                    "ranking",
                    "confidence",
                    "output",
                    "terminology",
                )
            ]
        ),
        hide_index=True,
    )
    st.caption(
        "Every result records these hashes, so a result can be tied to the rules that made it."
    )

# ---------- refusals on record -------------------------------------------------------------------

with tab_log:
    log = config.ROOT / config.load("policy")["audit_log"]
    if not log.exists():
        st.info("No refusals have been logged yet.")
    else:
        lines = [json.loads(x) for x in log.read_text().splitlines() if x.strip()]
        st.caption(
            f"{len(lines)} refusals on record in `{log.relative_to(config.ROOT)}`. Newest first; "
            "last 50 shown. The request itself is stored only as a hash."
        )
        st.dataframe(
            pd.DataFrame(lines[::-1][:50]).rename(
                columns={
                    "ts": "When (UTC)",
                    "request_sha256_16": "Request hash",
                    "category": "Category",
                    "matched_text": "Text that triggered it",
                }
            ),
            hide_index=True,
            width="stretch",
        )
