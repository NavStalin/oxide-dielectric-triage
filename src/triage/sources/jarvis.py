"""JARVIS-DFT dft_3d adapter. The only module that knows raw JARVIS field names.

Field names and missing-value conventions verified 2026-11-17 (docs/VERIFIED_FACTS.md section 1):
missing values are the string "na" (and "" for `icsd`), never None.
"""

from __future__ import annotations

import math
from typing import Any

from triage.models import MaterialRecord

MISSING = ("na", "", None)


def num(value: Any) -> float | None:
    """A finite float, or None. 0.0 is a real value (e.g. a metal's gap), not missing."""
    if value in MISSING or isinstance(value, bool):
        return None
    try:
        x = float(value)
    except (TypeError, ValueError):
        return None
    return x if math.isfinite(x) else None


def to_int(value: Any) -> int | None:
    x = num(value)
    return int(x) if x is not None else None


def icsd_ids(value: Any) -> list[str]:
    if value in MISSING:
        return []
    return [s.strip() for s in str(value).split(",") if s.strip()]


def to_record(raw: dict[str, Any]) -> MaterialRecord:
    elements = sorted(set(raw["atoms"]["elements"]))
    dim = raw.get("dimensionality")
    ref = raw.get("reference")
    return MaterialRecord(
        jid=raw["jid"],
        formula=raw["formula"],
        elements=elements,
        n_elements=len(elements),
        spg_symbol=raw.get("spg_symbol") or None,
        spg_number=to_int(raw.get("spg_number")),
        formation_energy_peratom=num(raw.get("formation_energy_peratom")),
        jarvis_ehull_raw=num(raw.get("ehull")),
        gap_mbj=num(raw.get("mbj_bandgap")),
        gap_optb88=num(raw.get("optb88vdw_bandgap")),
        kappa_total=num(raw.get("dfpt_piezo_max_dielectric")),
        kappa_electronic=num(raw.get("dfpt_piezo_max_dielectric_electronic")),
        kappa_ionic=num(raw.get("dfpt_piezo_max_dielectric_ionic")),
        icsd_ids=icsd_ids(raw.get("icsd")),
        dimensionality=None if dim in MISSING else str(dim),
        origin_reference=None if ref in MISSING else str(ref),
    )


def fractional_composition(raw: dict[str, Any]) -> dict[str, float]:
    sites = raw["atoms"]["elements"]
    n = len(sites)
    out: dict[str, float] = {}
    for el in sites:
        out[el] = out.get(el, 0.0) + 1.0 / n
    return out


def record_url(jid: str, template: str) -> str:
    return template.format(jid=jid)
