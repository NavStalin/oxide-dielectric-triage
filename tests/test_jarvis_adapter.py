import json
from pathlib import Path

from triage.sources import jarvis as jv

FIX = json.loads((Path(__file__).parent / "fixtures" / "synthetic_jarvis_records.json").read_text())


def test_missing_values_become_none_not_zero():
    r = jv.to_record(FIX[0])
    assert r.gap_mbj is None
    assert r.kappa_total is None
    assert r.icsd_ids == []
    assert r.dimensionality is None
    assert r.gap_optb88 == 4.0


def test_zero_is_a_real_value():
    r = jv.to_record(FIX[1])
    assert r.gap_mbj == 0.0
    assert r.gap_optb88 == 0.0


def test_parsing_details():
    r = jv.to_record(FIX[1])
    assert r.icsd_ids == ["123", "456"]
    assert r.spg_number == 225
    assert r.elements == ["O", "Ti"]
    assert r.n_elements == 2
    assert jv.num("nan") is None
    assert jv.num(True) is None


def test_fractional_composition():
    comp = jv.fractional_composition(FIX[0])
    assert abs(comp["O"] - 2 / 3) < 1e-12
    assert abs(sum(comp.values()) - 1) < 1e-12
