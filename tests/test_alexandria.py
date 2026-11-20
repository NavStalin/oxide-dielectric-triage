"""Alexandria cross-check adapter (D-044). Network is mocked; the fixture is synthetic."""

import json
from pathlib import Path

import pytest
import responses

from triage import config
from triage.models import Candidate, MaterialRecord
from triage.sources import alexandria

SRC = config.load("sources")
CFG = SRC["alexandria"]
TOL = SRC["cross_check"]["agreement_tolerance_ev"]
FIX = json.loads(
    (Path(__file__).parent / "fixtures" / "synthetic_alexandria_response.json").read_text()
)
EMPTY = {"data": [], "meta": {}}


def cand(formula="HfO2", spg=14, e_hull=0.0):
    r = MaterialRecord(
        jid="syn-1",
        formula=formula,
        elements=["Hf", "O"],
        n_elements=2,
        spg_number=spg,
        e_hull=e_hull,
    )
    return Candidate(formula=formula, representative=r, polymorphs=[r])


def test_optimade_formula_is_alphabetical_and_reduced():
    assert alexandria.optimade_formula("SiO2") == "O2Si"
    assert alexandria.optimade_formula("Y2O3") == "O3Y2"
    assert alexandria.optimade_formula("Al2O3") == "Al2O3"
    assert alexandria.optimade_formula("Hf2O4") == "HfO2"
    assert alexandria.optimade_formula("SrTiO3") == "O3SrTi"


def test_mirror_image_space_groups_are_queried_together():
    url = alexandria.query_url("SiO2", CFG["base_url"], 154)
    assert "154" in url and "152" in url
    assert "OR" not in alexandria.query_url("HfO2", CFG["base_url"], 14)


def test_default_source_is_allowlisted():
    assert SRC["cross_check"]["source"] == "alexandria"
    assert "alexandria.icams.rub.de" in SRC["allowed_hosts"]
    assert "alexandria.icams.rub.de" in SRC["citation_hosts"]


@responses.activate
def test_same_phase_agrees_caches_and_cites_the_record(tmp_path):
    responses.get(alexandria.query_url("HfO2", CFG["base_url"], 14), json=FIX)
    p1 = alexandria.fetch(cand(), CFG, SRC["allowed_hosts"], tmp_path)
    p2 = alexandria.fetch(cand(), CFG, SRC["allowed_hosts"], tmp_path)  # from cache
    assert len(responses.calls) == 1 and p1 == p2
    xc = alexandria.cross_check(cand(), p1, TOL)
    assert xc.status == "agree" and xc.match_type == "same_phase" and xc.source == "Alexandria"
    assert xc.delta_ev == pytest.approx(0.012)
    assert xc.ref_stability.record_id == "syn-agm-1"
    assert xc.ref_stability.url == CFG["record_url_template"].format(id="syn-agm-1")


@responses.activate
def test_falls_back_to_formula_level_and_can_disagree(tmp_path):
    responses.get(alexandria.query_url("HfO2", CFG["base_url"], 61), json=EMPTY)
    responses.get(alexandria.query_url("HfO2", CFG["base_url"]), json=FIX)
    c = cand(spg=61, e_hull=0.09)
    xc = alexandria.cross_check(c, alexandria.fetch(c, CFG, SRC["allowed_hosts"], tmp_path), TOL)
    assert len(responses.calls) == 2
    assert xc.status == "disagree" and xc.match_type == "formula_level"


@responses.activate
def test_not_found_is_named_not_filled(tmp_path):
    responses.get(alexandria.query_url("HfO2", CFG["base_url"], 14), json=EMPTY)
    responses.get(alexandria.query_url("HfO2", CFG["base_url"]), json=EMPTY)
    xc = alexandria.cross_check(
        cand(), alexandria.fetch(cand(), CFG, SRC["allowed_hosts"], tmp_path), TOL
    )
    assert xc.status == "not_found" and xc.ref_stability is None


@responses.activate
def test_http_error_is_a_named_failure_after_one_retry(tmp_path, monkeypatch):
    monkeypatch.setattr("time.sleep", lambda s: None)
    responses.get(alexandria.query_url("HfO2", CFG["base_url"], 14), status=503)
    with pytest.raises(alexandria.SourceFailure, match="Alexandria unreachable \\(HTTP 503\\)"):
        alexandria.fetch(cand(), CFG, SRC["allowed_hosts"], tmp_path)
    assert len(responses.calls) == 2


def test_host_not_on_allowlist_is_refused(tmp_path):
    cfg = dict(CFG, base_url="https://evil.example.com/pbe/v1")
    with pytest.raises(alexandria.SourceFailure, match="allowlist"):
        alexandria.fetch(cand(), cfg, SRC["allowed_hosts"], tmp_path)
