"""Typed records shared across the library. Optional numbers are None when missing, never 0."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class Evidence(BaseModel):
    """One displayed value and where it came from."""

    value: float | str | None
    unit: str | None = None
    method: str | None = None  # e.g. "TBmBJ", "OptB88vdW", "DFPT", "recomputed hull"
    source: Literal["JARVIS-DFT", "OQMD", "derived", "config"]
    record_id: str | None = None
    url: str | None = None
    retrieved_at: str | None = None
    derived_from: list[str] = Field(default_factory=list)  # for source == "derived"


class MaterialRecord(BaseModel):
    """One JARVIS entry (one structure), normalised. Field names are ours, not JARVIS's."""

    jid: str
    formula: str
    elements: list[str]  # sorted, unique
    n_elements: int
    spg_symbol: str | None = None
    spg_number: int | None = None
    formation_energy_peratom: float | None = None  # eV/atom, OptB88vdW
    e_hull: float | None = None  # eV/atom, recomputed (D-013)
    hull_n_compositions: int | None = None  # competing compositions in the hull, incl. elements
    hull_decomposition: list[str] = Field(default_factory=list)  # jids (or element:X) below it
    jarvis_ehull_raw: float | None = None  # kept for audit, never scored (D-013)
    gap_mbj: float | None = None  # eV, TBmBJ
    gap_optb88: float | None = None  # eV, OptB88vdW
    kappa_total: float | None = None  # DFPT, max component
    kappa_electronic: float | None = None
    kappa_ionic: float | None = None
    icsd_ids: list[str] = Field(default_factory=list)
    dimensionality: str | None = None
    origin_reference: str | None = None  # JARVIS `reference`, e.g. "mp-352"

    @property
    def has_icsd(self) -> bool:
        return bool(self.icsd_ids)


class Candidate(BaseModel):
    """A reduced formula: its representative polymorph plus the others."""

    formula: str
    representative: MaterialRecord
    polymorphs: list[MaterialRecord]  # all entries for the formula, representative first
    known_phase_note: str | None = None  # D-014
    status: Literal["ranked", "needs_review"] = "ranked"
    review_reason: str | None = None  # why it is listed but not ranked (D-030)


class CriterionScore(BaseModel):
    name: str
    raw: Evidence | None
    score: float | None  # None when the input is missing
    weight: float  # configured
    effective_weight: float = 0.0  # after renormalisation over present criteria
    contribution: float = 0.0
    note: str | None = None


class Suitability(BaseModel):
    total: float
    criteria: list[CriterionScore]
    missing: list[str] = Field(default_factory=list)


class CheckResult(BaseModel):
    id: str
    severity: Literal["fail", "warn", "report"]
    passed: bool
    summary: str
    rationale: str
    details: list[dict] = Field(default_factory=list)
