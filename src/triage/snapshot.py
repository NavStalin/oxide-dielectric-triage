"""Build data/snapshot/: oxygen-containing JARVIS records with recomputed hull, a manifest and a checks report.

The snapshot is written to a temporary directory and only replaces the live one if no `fail` check fails,
so a bad refresh never overwrites a good snapshot.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import time
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlparse

import pandas as pd

from triage import checks, config
from triage.candidates import build_candidates
from triage.hull import Entry, HullBuilder
from triage.models import MaterialRecord
from triage.sources import jarvis as jv

RECORDS_FILE = "oxides.parquet"


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _git_rev() -> str | None:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=config.ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        return out.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def _iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, UTC).isoformat(timespec="seconds")


def load_raw(raw_dir: Path, dataset: str, allowed_hosts: list[str]) -> tuple[list[dict], dict]:
    from jarvis.db.figshare import data, get_db_info

    url, filename, *rest = get_db_info()[dataset]
    host = urlparse(url).hostname or ""
    if host not in allowed_hosts:
        raise PermissionError(f"{host} is not in config/sources.yaml allowed_hosts")
    raw_dir.mkdir(parents=True, exist_ok=True)
    records = data(dataset, store_dir=str(raw_dir))
    zip_path = raw_dir / f"{filename}.zip"
    info = {
        "dataset": dataset,
        "file_name": filename,
        "file_url": url,
        "references": [
            s.strip()
            for s in "\n".join(rest[1:]).replace("Other versions:", "\n").split("\n")
            if s.strip().startswith("http")
        ],
        "raw_file_sha256": _sha256(zip_path) if zip_path.exists() else None,
        "raw_file_retrieved_at": _iso(zip_path.stat().st_mtime) if zip_path.exists() else None,
    }
    return records, info


def build(raw_records: list[dict], out_dir: Path, source_info: dict) -> dict:
    t0 = time.time()
    entries = [
        Entry(
            id=r["jid"],
            composition=jv.fractional_composition(r),
            energy=jv.num(r["formation_energy_peratom"]),
        )
        for r in raw_records
        if jv.num(r.get("formation_energy_peratom")) is not None
    ]
    builder = HullBuilder(entries)
    by_id = {e.id: e for e in entries}

    oxy = [r for r in raw_records if "O" in r["atoms"]["elements"]]
    recs: list[MaterialRecord] = []
    for r in oxy:
        rec = jv.to_record(r)
        if rec.jid in by_id:
            h = builder.e_hull(by_id[rec.jid])
            rec.e_hull, rec.hull_n_compositions, rec.hull_decomposition = (
                h.e_hull,
                h.n_compositions,
                h.decomposition,
            )
        recs.append(rec)
    hull_s = time.time() - t0

    df = pd.DataFrame([r.model_dump() for r in recs])
    df["has_icsd"] = df["icsd_ids"].map(bool)

    # invariant: one formula string per composition
    out_dir.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out_dir / RECORDS_FILE, index=False)

    manifest = {
        "source": "JARVIS-DFT (NIST)",
        **source_info,
        "snapshot_built_at": _iso(time.time()),
        "code_version": _git_rev(),
        "config_hashes": {
            n: config.file_hash(n)
            for n in ["ranking", "candidates", "hazards", "sources", "checks"]
        },
        "counts": {
            "records_total": len(raw_records),
            "records_with_formation_energy": len(entries),
            "records_oxygen": len(oxy),
            "formulas_oxygen": int(df["formula"].nunique()),
        },
        "hull": {
            "method": "LP over all JARVIS entries in each chemical system (D-013)",
            "runtime_s": round(hull_s, 1),
        },
    }
    return {"df": df, "records": recs, "manifest": manifest}


def run_checks(df: pd.DataFrame, recs: list[MaterialRecord]) -> list:
    ccfg = config.load("checks")
    cand_cfg, haz_cfg = config.load("candidates"), config.load("hazards")
    cands, frep = build_candidates(recs, cand_cfg, haz_cfg)
    results = [
        checks.c1(df, ccfg),
        checks.c2(df, ccfg),
        checks.c3(df, ccfg),
        checks.c4(df, ccfg),
        checks.c5(cands, cand_cfg, haz_cfg, ccfg),
    ]
    return results, frep


def snapshot(raw_dir: Path | None = None, out_dir: Path | None = None) -> tuple[bool, dict, list]:
    src = config.load("sources")
    raw_dir = raw_dir or config.ROOT / src["jarvis"]["raw_dir"]
    out_dir = out_dir or config.SNAPSHOT_DIR
    raw, info = load_raw(raw_dir, src["jarvis"]["dataset"], src["allowed_hosts"])

    tmp = out_dir.with_name(out_dir.name + ".tmp")
    shutil.rmtree(tmp, ignore_errors=True)
    built = build(raw, tmp, info)
    results, frep = run_checks(built["df"], built["records"])
    manifest = built["manifest"]
    manifest["candidates_default_config"] = {
        "formulas_in": frep.formulas_in,
        "dropped": dict(frep.dropped),
        "needs_review": frep.needs_review,
        "formulas_out": frep.formulas_out,
    }
    failed = [r.id for r in results if r.severity == "fail" and not r.passed]
    manifest["checks"] = {
        r.id: {"passed": r.passed, "severity": r.severity, "summary": r.summary} for r in results
    }
    (tmp / "manifest.json").write_text(json.dumps(manifest, indent=2))
    (tmp / "checks_report.json").write_text(
        json.dumps([r.model_dump() for r in results], indent=2, default=str)
    )

    if failed:
        return False, manifest, results  # leave tmp for inspection; live snapshot untouched
    keep = out_dir / "oqmd_cache"
    if keep.exists():
        shutil.move(str(keep), str(tmp / "oqmd_cache"))
    shutil.rmtree(out_dir, ignore_errors=True)
    tmp.rename(out_dir)
    return True, manifest, results


def load_records(snapshot_dir: Path | None = None) -> tuple[list[MaterialRecord], dict]:
    d = snapshot_dir or config.SNAPSHOT_DIR
    df = pd.read_parquet(d / RECORDS_FILE)
    df = df.drop(columns=["has_icsd"])
    recs = []
    for row in df.to_dict(orient="records"):
        row = {k: (None if isinstance(v, float) and pd.isna(v) else v) for k, v in row.items()}
        for k in ("elements", "icsd_ids", "hull_decomposition"):
            row[k] = list(row[k]) if row[k] is not None else []
        recs.append(MaterialRecord(**row))
    manifest = json.loads((d / "manifest.json").read_text())
    return recs, manifest
