import pytest

from triage import config, scoring
from triage.models import CriterionScore

RC = config.load("ranking")


@pytest.mark.parametrize(
    "e_hull, expected",
    [(0.0, 1.0), (0.025, 0.8), (0.0625, 0.4), (0.100, 0.0), (0.5, 0.0), (-0.001, 1.0)],
)
def test_stability_breakpoints(e_hull, expected):
    assert scoring.stability_score(e_hull, RC["stability"]) == pytest.approx(expected)


@pytest.mark.parametrize(
    "gap, expected", [(0.0, 0.0), (2.0, 0.0), (4.0, 0.5), (6.0, 1.0), (9.0, 1.0)]
)
def test_band_gap_breakpoints(gap, expected):
    assert scoring.band_gap_score(gap, RC["band_gap"]) == pytest.approx(expected)


@pytest.mark.parametrize("n, expected", [(2, 1.0), (3, 0.7), (4, 0.4), (5, 0.1), (8, 0.1)])
def test_simplicity(n, expected):
    assert scoring.simplicity_score(n, RC["simplicity"]) == expected


def test_hazard_floor():
    assert scoring.hazard_score(0, 0.5) == 1.0
    assert scoring.hazard_score(1, 0.5) == 0.5
    assert scoring.hazard_score(3, 0.5) == 0.0


def _c(name, score, weight):
    return CriterionScore(name=name, raw=None, score=score, weight=weight)


def test_missing_criterion_renormalises_and_is_recorded():
    s = scoring.combine([_c("a", 1.0, 0.5), _c("b", None, 0.3), _c("c", 0.5, 0.2)])
    # present weights 0.5 + 0.2 -> effective 5/7, 2/7
    assert s.total == pytest.approx((5 / 7) * 1.0 + (2 / 7) * 0.5)
    assert s.missing == ["b"]
    assert sum(c.effective_weight for c in s.criteria) == pytest.approx(1.0)


def test_missing_is_neutral_not_zero():
    full = scoring.combine([_c("a", 0.8, 0.5), _c("b", 0.8, 0.5)]).total
    one_missing = scoring.combine([_c("a", 0.8, 0.5), _c("b", None, 0.5)]).total
    assert one_missing == pytest.approx(full)


def test_zero_weight_criterion_ignored_and_not_reported_missing():
    s = scoring.combine([_c("a", 1.0, 1.0), _c("d", None, 0.0)])
    assert s.total == pytest.approx(1.0)
    assert s.missing == []


def test_contributions_sum_to_total():
    s = scoring.combine([_c("a", 0.3, 0.35), _c("b", 0.9, 0.30), _c("c", 0.5, 0.35)])
    assert sum(c.contribution for c in s.criteria) == pytest.approx(s.total)
