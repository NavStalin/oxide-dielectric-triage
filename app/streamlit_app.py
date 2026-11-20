"""Streamlit entry point. Two areas: the triage page scientists use, and "Under the hood" for the trace.

A thin layer over triage.pipeline.run_triage; no filtering, scoring or policy logic lives here.
"""

from __future__ import annotations

import streamlit as st

st.set_page_config(
    page_title="Oxide dielectric triage", page_icon=":material/science:", layout="wide"
)

page = st.navigation(
    [
        st.Page("views/triage.py", title="Triage", icon=":material/science:", default=True),
        st.Page(
            "views/under_the_hood.py",
            title="Under the hood",
            icon=":material/account_tree:",
            url_path="under-the-hood",
        ),
    ]
)
page.run()
