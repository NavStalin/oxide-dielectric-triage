from types import SimpleNamespace

import pytest

from triage import config
from triage.providers.llm import LLMCriteria, LLMProvider, LLMUnavailable, number_check
from triage.providers.rules import RulesProvider

W = config.load("ranking")["weights"]


def test_example_request_keeps_defaults_and_understands_everything():
    c = RulesProvider().parse(
        "Find promising oxide dielectric candidates for thin-film experiments. Prefer thermodynamically "
        "stable materials, wide band gaps, non-toxic elements, simple compositions, and public evidence. "
        "Return a ranked shortlist with caveats.",
        W,
    )
    assert c.weights == W
    assert c.unparsed == []
    assert c.min_band_gap is None and c.max_e_hull is None


def test_capacitor_request_changes_weights():
    c = RulesProvider().parse(
        "High-k oxides for capacitors. I can accept a smaller band gap and ternaries are fine.", W
    )
    assert c.weights["dielectric"] == 0.25
    assert c.weights["band_gap"] == 0.15
    assert c.weights["simplicity"] == 0.05


def test_thresholds_and_exclusions():
    c = RulesProvider().parse(
        "Band gap above 5 eV, within 50 meV of the hull, lead-free, no Cd, top 7, detailed view", W
    )
    assert c.min_band_gap == 5.0
    assert c.max_e_hull == pytest.approx(0.05)
    assert set(c.exclude_elements) == {"Pb", "Cd"}
    assert c.shortlist_size == 7
    assert c.style == "audit"


def test_unknown_phrases_are_reported():
    c = RulesProvider().parse("Prefer materials my advisor likes", W)
    assert c.unparsed


def test_number_check():
    allowed = [5.664, 0.0, 2.0, 1.0]
    assert number_check(
        "HfO2 has a 5.66 eV TBmBJ gap and sits on the hull with 2 elements.", allowed
    )
    assert not number_check("HfO2 has a 6.1 eV gap.", allowed)
    assert not number_check("Its dielectric constant is 25.", allowed)


class _FakeMessages:
    def __init__(self, parsed, stop="end_turn"):
        self._r = SimpleNamespace(parsed_output=parsed, stop_reason=stop)

    def parse(self, **kwargs):
        assert kwargs["output_format"] is LLMCriteria
        return self._r


def test_llm_provider_maps_to_criteria_without_network():
    fake = SimpleNamespace(
        messages=_FakeMessages(
            LLMCriteria.unchanged(
                dielectric_weight=0.3,
                min_band_gap_ev=4.0,
                max_e_hull_mev=40,
                exclude_elements=["Pb", "not-an-element"],
                understood=["high-k"],
            )
        )
    )
    c = LLMProvider(client=fake).parse("high-k please", W)
    assert c.weights["dielectric"] == 0.3 and c.weights["stability"] == W["stability"]
    assert c.min_band_gap == 4.0 and c.max_e_hull == pytest.approx(0.04)
    assert c.exclude_elements == ["Pb"]
    assert c.provider.startswith("llm")


def test_llm_refusal_raises_for_fallback():
    fake = SimpleNamespace(messages=_FakeMessages(None, stop="refusal"))
    with pytest.raises(LLMUnavailable):
        LLMProvider(client=fake).parse("x", W)
