import json
from pathlib import Path

import pytest
import requests
import responses

from triage import confidence, config
from triage.models import Candidate, CrossCheck, MaterialRecord, Suitability
from triage.sources import oqmd

SRC = config.load("sources")
CONF = config.load("confidence")
CORR = config.load("candidates")["unreliable_zero_gap_elements"]
FIX = Path(__file__).parent / "fixtures" / "synthetic_oqmd_response.json"


def cand(formula="HfO2", spg="P2_1/c", e_hull=0.0, mbj=5.0, icsd=("1",), els=("Hf", "O"), ncomp=8):
    r = MaterialRecord(
        jid="syn-1",
        formula=formula,
        elements=sorted(els),
        n_elements=len(els),
        spg_symbol=spg,
        e_hull=e_hull,
        gap_mbj=mbj,
        gap_optb88=4.0,
        icsd_ids=list(icsd),
        hull_n_compositions=ncomp,
    )
    return Candidate(formula=formula, representative=r, polymorphs=[r])


def test_parse_formula():
    assert oqmd.parse_formula("SrTiO3") == oqmd.parse_formula("TiSrO3")
    assert oqmd.parse_formula("Al2O3") == {"Al": 0.4, "O": 0.6}


@responses.activate
def test_fetch_caches_and_cross_check_agrees(tmp_path):
    url = oqmd.query_url("HfO2", SRC["oqmd"]["base_url"])
    responses.get(url, json=json.loads(FIX.read_text()))
    p1 = oqmd.fetch("HfO2", SRC["oqmd"], SRC["allowed_hosts"], tmp_path)
    p2 = oqmd.fetch("HfO2", SRC["oqmd"], SRC["allowed_hosts"], tmp_path)  # from cache
    assert len(responses.calls) == 1 and p1 == p2
    xc = oqmd.cross_check(cand(), p1, SRC["oqmd"]["agreement_tolerance_ev"])
    assert xc.status == "agree" and xc.match_type == "same_phase"
    assert xc.oqmd_stability.source == "OQMD" and xc.oqmd_stability.url == url


def test_cross_check_disagree_and_formula_level():
    payload = {
        "url": "u",
        "retrieved_at": "t",
        "rows": [
            {"name": "HfO2", "entry_id": 9, "icsd_id": None, "stability": 0.2, "spacegroup": "Pbca"}
        ],
    }
    xc = oqmd.cross_check(cand(), payload, 0.05)
    assert xc.status == "disagree" and xc.match_type == "formula_level"
    assert xc.delta_ev == pytest.approx(0.2)


@responses.activate
def test_fetch_failure_is_named_not_raised_as_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(oqmd.time, "sleep", lambda s: None)
    url = oqmd.query_url("HfO2", SRC["oqmd"]["base_url"])
    responses.get(url, status=502)
    responses.get(url, status=502)
    with pytest.raises(oqmd.SourceFailure, match="HTTP 502"):
        oqmd.fetch("HfO2", SRC["oqmd"], SRC["allowed_hosts"], tmp_path)
    assert not (tmp_path / "HfO2.json").exists()


@responses.activate
def test_fetch_timeout(tmp_path, monkeypatch):
    monkeypatch.setattr(oqmd.time, "sleep", lambda s: None)
    url = oqmd.query_url("HfO2", SRC["oqmd"]["base_url"])
    responses.get(url, body=requests.Timeout())
    responses.get(url, body=requests.Timeout())
    with pytest.raises(oqmd.SourceFailure, match="timeout"):
        oqmd.fetch("HfO2", SRC["oqmd"], SRC["allowed_hosts"], tmp_path)


def test_host_not_on_allowlist_is_refused(tmp_path):
    cfg = dict(SRC["oqmd"], base_url="https://evil.example.com/api")
    with pytest.raises(oqmd.SourceFailure, match="allowlist"):
        oqmd.fetch("HfO2", cfg, SRC["allowed_hosts"], tmp_path)


def suit(missing=()):
    return Suitability(total=0.9, criteria=[], missing=list(missing))


def test_confidence_levels():
    agree = CrossCheck(status="agree", match_type="same_phase", delta_ev=0.0)
    hi = confidence.assess(cand(), suit(), agree, CONF, CORR)
    assert hi.level == "High" and hi.points == 6

    down = CrossCheck(status="unavailable", detail="OQMD unreachable (HTTP 502)")
    weak = confidence.assess(cand(mbj=None, icsd=()), suit(["dielectric"]), down, CONF, CORR)
    assert weak.level == "Low" and any("unavailable" in r for r in weak.reasons)


def test_confidence_penalties():
    agree = CrossCheck(status="agree", match_type="same_phase", delta_ev=0.0)
    c = confidence.assess(cand(els=("Yb", "O"), ncomp=2), suit(), agree, CONF, CORR)
    assert c.points == 6 - 2
    assert any("Yb" in r for r in c.reasons) and any("only 2" in r for r in c.reasons)


def test_icsd_via_oqmd_counts():
    xc = CrossCheck(status="agree", match_type="same_phase", delta_ev=0.0, icsd_id="27313")
    c = confidence.assess(cand(icsd=()), suit(), xc, CONF, CORR)
    assert any("via OQMD" in r for r in c.reasons)
