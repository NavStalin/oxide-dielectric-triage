"""The eval suite itself runs green (offline, rules parser) and writes its results."""

import pytest

from triage import config

pytestmark = pytest.mark.skipif(
    not (config.SNAPSHOT_DIR / "oxides.parquet").exists(), reason="no snapshot"
)


def test_evals_pass_and_write_results(monkeypatch, tmp_path):
    from evals import run_evals
    from triage.sources import oqmd

    monkeypatch.setattr(oqmd.time, "sleep", lambda s: None)
    monkeypatch.setattr(run_evals, "RESULTS", tmp_path)
    assert run_evals.main([]) == 0
    assert (tmp_path / "SUMMARY.md").exists()
    assert (tmp_path / "eval_4_face_validity.md").exists()
