"""Typed records shared across the library. Optional numbers are None when missing, never 0."""

from __future__ import annotations

from typing import Any, Literal

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


class Criteria(BaseModel):
    """What the scientist asked for, in typed form. Produced by a DecisionProvider, then clamped by policy."""

    weights: dict[str, float]
    min_band_gap: float | None = None  # eV, hard filter on the primary gap
    max_e_hull: float | None = None  # eV/atom, hard filter
    max_elements: int | None = None
    exclude_elements: list[str] = Field(default_factory=list)
    allow_extra_anions: bool = False
    shortlist_size: int | None = None
    style: Literal["pi", "audit"] | None = None
    matched: list[str] = Field(default_factory=list)  # phrases the parser understood, with effect
    unparsed: list[str] = Field(default_factory=list)  # phrases it did not understand
    clamped: list[str] = Field(default_factory=list)  # what policy changed, and why
    provider: str = "rules"


class CrossCheck(BaseModel):
    status: Literal["agree", "disagree", "unavailable", "not_found", "not_run"]
    match_type: Literal["same_phase", "formula_level"] | None = None
    oqmd_stability: Evidence | None = None
    delta_ev: float | None = None
    icsd_id: str | None = None
    detail: str = ""


class Confidence(BaseModel):
    level: Literal["High", "Medium", "Low"]
    points: int
    reasons: list[str]


class Refusal(BaseModel):
    category: str
    matched_text: str
    message: str


class RankedCandidate(BaseModel):
    rank: int
    tied: bool = False  # same suitability (to displayed precision) as a neighbour
    candidate: Candidate
    suitability: Suitability
    confidence: Confidence
    cross_check: CrossCheck
    rationale: str
    caveats: list[str]
    citations: list[Evidence]


class TraceStep(BaseModel):
    step: str
    detail: str
    ms: float


class TriageResult(BaseModel):
    request: str
    criteria: Criteria
    refusals: list[Refusal]
    ranked: list[RankedCandidate]
    review_list: list[Candidate]
    standing_caveats: list[str]
    notes: list[str]  # run-level notes, e.g. "OQMD unreachable"
    filter_counts: dict[str, Any]
    manifest: dict[str, Any]
    settings: dict[str, Any]
    trace: list[TraceStep]
    created_at: str


class CheckResult(BaseModel):
    id: str
    severity: Literal["fail", "warn", "report"]
    passed: bool
    summary: str
    rationale: str
    details: list[dict] = Field(default_factory=list)
