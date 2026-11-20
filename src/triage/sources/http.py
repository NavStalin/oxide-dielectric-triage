"""Shared HTTP fetch for cross-check sources: allowlisted host, short timeout, one retry.

Every failure becomes a named SourceFailure, never a crash and never a made-up value.
"""

from __future__ import annotations

import time
from typing import Any
from urllib.parse import urlparse

import requests


class SourceFailure(Exception):
    """A cross-check source could not be reached or returned something unusable."""


def get_json(
    url: str, timeout_s: float, allowed_hosts: list[str], name: str, session: Any = requests
) -> dict[str, Any]:
    host = urlparse(url).hostname or ""
    if host not in allowed_hosts:
        raise SourceFailure(f"host {host} not in allowlist")
    last_err = "unknown error"
    for attempt in range(2):
        try:
            resp = session.get(url, timeout=timeout_s)
            if resp.status_code != 200:
                last_err = f"HTTP {resp.status_code}"
            else:
                return resp.json()
        except requests.Timeout:
            last_err = f"timeout after {timeout_s} s"
        except (requests.RequestException, ValueError) as e:
            last_err = type(e).__name__
        if attempt == 0:
            time.sleep(1.0)
    raise SourceFailure(f"{name} unreachable ({last_err})")
