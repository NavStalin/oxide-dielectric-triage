from triage import config
from triage.candidates import build_candidates, primary_gap
from triage.models import MaterialRecord

CC = config.load("candidates")
HC = config.load("hazards")


def rec(jid, formula, elements, e_hull, gap_mbj=None, gap_optb88=5.0, icsd=(), spg="P1"):
    return MaterialRecord(
        jid=jid,
        formula=formula,
        elements=sorted(elements),
        n_elements=len(set(elements)),
        spg_symbol=spg,
        e_hull=e_hull,
        gap_mbj=gap_mbj,
        gap_optb88=gap_optb88,
        formation_energy_peratom=-3.0,
        icsd_ids=list(icsd),
    )


def test_primary_gap_prefers_tbmbj_and_flags_fallback():
    assert primary_gap(rec("s1", "XO", ["Mg", "O"], 0, gap_mbj=6.0, gap_optb88=4.0)) == (
        6.0,
        "TBmBJ",
    )
    assert primary_gap(rec("s2", "XO", ["Mg", "O"], 0, gap_mbj=None, gap_optb88=4.0)) == (
        4.0,
        "OptB88vdW",
    )


def test_filters():
    recs = [
        rec("s1", "MgO", ["Mg", "O"], 0.0),
        rec("s2", "MgOH", ["Mg", "O", "H"], 0.0),  # excluded anion
        rec("s3", "ThO2", ["Th", "O"], 0.0),  # no stable isotopes
        rec("s4", "TiO", ["Ti", "O"], 0.0, gap_optb88=0.0),  # metal
        rec("s5", "Mg", ["Mg"], 0.0),  # not an oxide
    ]
    cands, report = build_candidates(recs, CC, HC)
    assert [c.formula for c in cands] == ["MgO"]
    assert report.dropped == {
        "contains H, C, N, S or halogen": 1,
        "element with no stable isotopes": 1,
        "metal (no band gap)": 1,
        "not an oxide": 1,
    }


def test_zero_gap_with_correlated_element_goes_to_review_not_dropped():
    recs = [
        rec("y", "Yb2O3", ["Yb", "O"], 0.0, gap_optb88=0.0),
        rec("t", "TiO", ["Ti", "O"], 0.0, gap_optb88=0.0),
    ]
    cands, report = build_candidates(recs, CC, HC)
    assert [(c.formula, c.status) for c in cands] == [("Yb2O3", "needs_review")]
    assert "D-030" in cands[0].review_reason
    assert report.needs_review == 1 and report.formulas_out == 0
    assert report.dropped == {"metal (no band gap)": 1}


def test_representative_tie_prefers_icsd_and_note_names_known_phase():
    recs = [
        rec("a", "ZrO2", ["Zr", "O"], 0.0000, spg="Pbca"),
        rec("b", "ZrO2", ["Zr", "O"], 0.0005, spg="P2_1/c", icsd=["1"]),  # within 1 meV tie
        rec("c", "ZrO2", ["Zr", "O"], 0.0200, spg="P4_2/nmc", icsd=["2"]),
    ]
    (cand,), _ = build_candidates(recs, CC, HC)
    assert cand.representative.jid == "b"
    assert cand.known_phase_note is None


def test_known_phase_note_when_icsd_polymorph_is_close():
    recs = [
        rec("a", "MgO", ["Mg", "O"], 0.000, spg="I4/mmm"),
        rec("b", "MgO", ["Mg", "O"], 0.029, spg="Fm-3m", icsd=["1"]),
    ]
    (cand,), _ = build_candidates(recs, CC, HC)
    assert cand.representative.jid == "a"
    assert "b (Fm-3m)" in cand.known_phase_note
