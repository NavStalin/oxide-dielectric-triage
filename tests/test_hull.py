"""Hand-built synthetic A-O system with a known answer."""

import pytest

from triage.hull import Entry, HullBuilder


def comp(a, o):
    n = a + o
    return {k: v / n for k, v in {"A": a, "O": o}.items() if v}


@pytest.fixture
def builder():
    return HullBuilder(
        [
            Entry("syn-AO", comp(1, 1), -2.0),
            Entry("syn-AO-poly", comp(1, 1), -1.99),
            Entry("syn-AO2", comp(1, 2), -1.0),
            Entry("syn-A", comp(1, 0), 0.0),
        ]
    )


def test_ground_state_on_hull(builder):
    assert builder.e_hull(Entry("syn-AO", comp(1, 1), -2.0)).e_hull == pytest.approx(0.0, abs=1e-9)


def test_polymorph_above_ground_state(builder):
    assert builder.e_hull(Entry("syn-AO-poly", comp(1, 1), -1.99)).e_hull == pytest.approx(0.01)


def test_decomposes_into_mixture(builder):
    # AO2 = 2/3 AO + 1/3 O  ->  2/3 * -2.0 = -1.3333 ; AO2 at -1.0 is 0.3333 above
    res = builder.e_hull(Entry("syn-AO2", comp(1, 2), -1.0))
    assert res.e_hull == pytest.approx(1 / 3)
    assert res.decomposition == ["element:O", "syn-AO"]


def test_competing_composition_count(builder):
    # compositions in A-O: A, O, AO, AO2 -> 3 besides the target's own
    assert builder.e_hull(Entry("syn-AO", comp(1, 1), -2.0)).n_compositions == 3
