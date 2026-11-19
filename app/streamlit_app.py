"""Streamlit front end. A thin layer over triage.pipeline.run_triage; no logic of its own."""

from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from triage import config
from triage.candidates import build_candidates, primary_gap
from triage.pipeline import _records, run_triage
from triage.providers import llm
from triage.render import render, to_json

EXAMPLE = (
    "Find promising oxide dielectric candidates for thin-film experiments. Prefer thermodynamically "
    "stable materials, wide band gaps, non-toxic elements, simple compositions, and public evidence. "
    "Return a ranked shortlist with caveats."
)

st.set_page_config(page_title="Oxide dielectric triage", layout="wide")
st.title("Oxide dielectric triage")
st.caption(
    "Narrows public DFT data to a cited shortlist and shows its working. Code does the filtering, "
    "scoring and citations; a language model (optional) only reads your request."
)

rank_cfg = config.load("ranking")
out_cfg = config.load("output")

with st.sidebar:
    st.header("Settings")
    has_llm = llm.available()
    provider = st.radio(
        "Read the request with",
        ["rules", "llm"],
        format_func=lambda p: (
            "Keyword rules (offline)" if p == "rules" else "Claude (needs API key)"
        ),
        disabled=not has_llm,
        help="Both produce the same typed criteria. Policy limits apply either way.",
    )
    oqmd_on = st.toggle(
        "Cross-check stability with OQMD (online)",
        value=False,
        help="Off = fully offline. Failures are reported, never hidden.",
    )
    manual = st.toggle(
        "Adjust ranking manually",
        value=False,
        help="When on, these values override what was read from the request.",
    )
    w = rank_cfg["weights"]
    weights = {
        "stability": st.slider(
            "Stability weight", 0.0, 1.0, float(w["stability"]), 0.05, disabled=not manual
        ),
        "band_gap": st.slider(
            "Band gap weight", 0.0, 1.0, float(w["band_gap"]), 0.05, disabled=not manual
        ),
        "hazard": st.slider(
            "Element hazard weight", 0.0, 1.0, float(w["hazard"]), 0.05, disabled=not manual
        ),
        "simplicity": st.slider(
            "Simplicity weight", 0.0, 1.0, float(w["simplicity"]), 0.05, disabled=not manual
        ),
        "dielectric": st.slider(
            "Dielectric constant (κ) weight",
            0.0,
            1.0,
            float(w["dielectric"]),
            0.05,
            disabled=not manual,
        ),
    }
    min_gap = st.number_input(
        "Minimum band gap (eV, 0 = none)", 0.0, 10.0, 0.0, 0.5, disabled=not manual
    )
    max_hull = st.number_input(
        "Max energy above hull (meV/atom, 0 = none)", 0, 500, 0, 5, disabled=not manual
    )
    max_el = st.selectbox(
        "Max elements",
        [None, 2, 3, 4],
        disabled=not manual,
        format_func=lambda x: "no limit" if x is None else str(x),
    )
    top = st.slider("Shortlist size (audit view)", 3, 25, int(out_cfg["shortlist"]["audit"]))

request = st.text_area("Request", EXAMPLE, height=110)
run = st.button("Run triage", type="primary")

if run:
    overrides: dict = {"shortlist_size": top, "style": "audit"}
    if manual:
        overrides.update(
            weights=weights,
            min_band_gap=min_gap or None,
            max_e_hull=(max_hull / 1000) if max_hull else None,
            max_elements=max_el,
        )
    with st.spinner("Running triage..."):
        st.session_state["result"] = run_triage(
            request, provider=provider, overrides=overrides, oqmd_enabled=oqmd_on
        )

res = st.session_state.get("result")
if res is not None:
    if res.refusals:
        st.warning("**Not done:**\n" + "\n".join(f"- {r.message}" for r in res.refusals))
    for n in res.notes:
        st.info(n)

    tab_pi, tab_audit, tab_plot, tab_json = st.tabs(
        ["PI summary", "Audit view", "κ vs band gap", "JSON"]
    )
    pi_md, audit_md = render(res, "pi"), render(res, "audit")
    with tab_pi:
        st.markdown(pi_md)
        st.download_button("Download PI summary (.md)", pi_md, "triage_pi_summary.md")
    with tab_audit:
        st.markdown(audit_md)
        st.download_button("Download audit view (.md)", audit_md, "triage_audit.md")
    with tab_plot:
        recs, _ = _records(str(config.SNAPSHOT_DIR))
        cands, _ = build_candidates(list(recs), config.load("candidates"), config.load("hazards"))
        pts = [
            (c.formula, *primary_gap(c.representative), c.representative.kappa_total)
            for c in cands
            if c.status == "ranked" and c.representative.kappa_total is not None
        ]
        short = {rc.candidate.formula for rc in res.ranked}
        fig = go.Figure()
        bg = [p for p in pts if p[0] not in short]
        fg = [p for p in pts if p[0] in short]
        fig.add_trace(
            go.Scatter(
                x=[p[1] for p in bg],
                y=[p[3] for p in bg],
                mode="markers",
                name="All candidates with DFPT κ",
                text=[p[0] for p in bg],
                marker={"size": 5, "opacity": 0.35},
            )
        )
        fig.add_trace(
            go.Scatter(
                x=[p[1] for p in fg],
                y=[p[3] for p in fg],
                mode="markers+text",
                name="Shortlist",
                text=[p[0] for p in fg],
                textposition="top center",
                marker={"size": 11},
            )
        )
        fig.update_layout(
            xaxis_title="Band gap (eV; TBmBJ, else OptB88vdW)",
            yaxis_title="κ total (DFPT, max component)",
            yaxis_type="log",
            height=520,
        )
        st.plotly_chart(fig, width="stretch")
        st.caption(
            f"{len(pts)} ranked candidates have a DFPT κ (about 7% of oxides). High κ usually "
            "comes with a smaller gap. Shortlisted materials without κ are not shown."
        )
    with tab_json:
        js = to_json(res)
        st.download_button("Download JSON", js, "triage_result.json")
        st.code(js[:20000], language="json")
