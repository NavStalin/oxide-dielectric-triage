import pandas as pd
import pytest

from triage import checks, config
from triage.models import Candidate, MaterialRecord
from triage.snapshot import load_records

CK = config.load("checks")


def _df(rows):
    base = {
        "jarvis_ehull_raw": None,
        "gap_mbj": None,
        "gap_optb88": 5.0,
        "kappa_total": None,
        "has_icsd": False,
    }
    return pd.DataFrame([{**base, **r} for r in rows])


def _known(e_hull, raw=1.5):
    rows = []
    for f, spgs in CK["C1_known_ground_states"]["materials"].items():
        rows.append(
            {
                "jid": f"syn-{f}",
                "formula": f,
                "spg_symbol": spgs[0],
                "e_hull": e_hull,
                "jarvis_ehull_raw": raw,
            }
        )
    return _df(rows)


def test_c1_passes_and_c2_reports_raw_field_failure():
    df = _known(0.0, raw=1.5)
    assert checks.c1(df, CK).passed
    c2 = checks.c2(df, CK)
    assert not c2.passed and c2.severity == "report"


def test_c1_fails_when_ground_state_off_hull():
    assert not checks.c1(_known(0.2), CK).passed


def test_c1_fails_when_material_missing():
    assert not checks.c1(_known(0.0).iloc[1:], CK).passed


def test_c3_warns_on_reversed_gap_methods():
    df = _df(
        [
            {"jid": "s1", "formula": "XO", "gap_mbj": 3.0, "gap_optb88": 4.0},
            {"jid": "s2", "formula": "YO", "gap_mbj": 6.0, "gap_optb88": 4.0},
        ]
    )
    r = checks.c3(df, CK)
    assert not r.passed and r.severity == "warn" and r.details[0]["jid"] == "s1"


def test_c4_fails_when_coverage_collapses():
    df = _df(
        [
            {
                "jid": f"s{i}",
                "formula": "XO",
                "gap_mbj": None,
                "kappa_total": None,
                "has_icsd": False,
            }
            for i in range(10)
        ]
    )
    assert not checks.c4(df, CK).passed


def test_c5_fails_on_leaked_excluded_element():
    r = MaterialRecord(jid="s", formula="ThO2", elements=["O", "Th"], n_elements=2)
    cand = Candidate(formula="ThO2", representative=r, polymorphs=[r])
    res = checks.c5([cand], config.load("candidates"), config.load("hazards"), CK)
    assert not res.passed


@pytest.fixture(scope="module")
def real():
    if not (config.SNAPSHOT_DIR / "oxides.parquet").exists():
        pytest.skip("no snapshot; run `make snapshot`")
    return load_records()


@pytest.mark.parametrize(
    "formula, spg", [("HfO2", "P2_1/c"), ("Al2O3", "R-3c"), ("SiO2", "P3_221")]
)
def test_real_snapshot_known_ground_states_on_hull(real, formula, spg):
    recs, _ = real
    best = min(
        (r for r in recs if r.formula == formula and r.spg_symbol == spg), key=lambda r: r.e_hull
    )
    assert best.e_hull == pytest.approx(0.0, abs=0.001)
