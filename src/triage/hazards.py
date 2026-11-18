"""Element-level hazard flags and hard exclusions from config/hazards.yaml (brief decision 6)."""

from __future__ import annotations

from dataclasses import dataclass
from functools import cache
from typing import Any

from jarvis.core.specie import Specie


@cache
def atomic_number(symbol: str) -> int:
    return int(Specie(symbol).Z)


@dataclass(frozen=True)
class HazardFlag:
    element: str
    sources: tuple[str, ...]
    wording: tuple[str, ...]
    note: str | None


def flags_for(elements: list[str], cfg: dict[str, Any]) -> list[HazardFlag]:
    out = []
    for el in elements:
        entry = cfg["flags"].get(el)
        if entry:
            out.append(
                HazardFlag(
                    element=el,
                    sources=tuple(entry["sources"]),
                    wording=tuple(entry["source_wording"]),
                    note=entry.get("note"),
                )
            )
    return out


def is_excluded_element(el: str, cfg: dict[str, Any]) -> bool:
    ex = cfg["excluded"]
    return el in ex["elements_explicit"] or atomic_number(el) >= ex["min_atomic_number"]


def compound_note(formula: str, cfg: dict[str, Any]) -> dict[str, Any] | None:
    return (cfg.get("compound_notes") or {}).get(formula)
