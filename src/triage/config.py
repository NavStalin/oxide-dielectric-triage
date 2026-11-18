"""Load config/*.yaml. Plain dicts validated at the edges that matter; files are the source of truth."""

from __future__ import annotations

import hashlib
from functools import cache
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = ROOT / "config"
SNAPSHOT_DIR = ROOT / "data" / "snapshot"


@cache
def load(name: str, config_dir: str | None = None) -> dict[str, Any]:
    path = Path(config_dir or CONFIG_DIR) / f"{name}.yaml"
    with path.open() as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise TypeError(f"{path} must contain a mapping")
    return data


def file_hash(name: str, config_dir: str | None = None) -> str:
    path = Path(config_dir or CONFIG_DIR) / f"{name}.yaml"
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]
