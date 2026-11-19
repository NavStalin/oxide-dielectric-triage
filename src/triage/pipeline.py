"""run_triage: request text in, TriageResult out. The single code path for CLI, app and evals.

Order: policy gate -> parse -> clamp -> candidates and filters -> score -> rank (ties by confidence)
-> OQMD cross-check on the shortlist -> confidence -> caveats, citations, rationale.
"""

from __future__ import annotations

from datetime import UTC, datetime
from functools import cache
from pathlib import Path
from typing import Any

import requests

from triage import confidence, config, hazards, policy, scoring
from triage.candidates import build_candidates, primary_gap
from triage.models import (
    Candidate,
    Confidence,
    CrossCheck,
    Evidence,
    RankedCandidate,
    Suitability,
    TriageResult,
)
from triage.providers.llm import LLMProvider, LLMUnavailable, number_check
from triage.providers.llm import rationales as llm_rationales
from triage.providers.rules import RulesProvider
from triage.snapshot import load_records
from triage.sources import oqmd
from triage.trace import Trace

LEVEL_ORDER = {"High": 0, "Medium": 1, "Low": 2}


@cache
def _records(snapshot_dir: str) -> tuple:
    recs, manifest = load_records(Path(snapshot_dir))
    return tuple(recs), manifest


def _settings() -> dict[str, dict]:
    return {
        n: config.load(n)
        for n in [
            "ranking",
            "candidates",
            "hazards",
            "sources",
            "policy",
            "confidence",
            "output",
            "terminology",
        ]
    }


# ---------- per-candidate text ----------------------------------------------------------------


def _phrase(name: str, cand: Candidate) -> str:
    r = cand.representative
    if name == "stability":
        return (
            "on the convex hull"
            if (r.e_hull or 0) < 0.0005
            else f"{r.e_hull * 1000:.0f} meV/atom above the hull"
        )
    if name == "band_gap":
        g, m = primary_gap(r)
        return f"band gap {g:.2f} eV ({m})" if g is not None else "band gap missing"
    if name == "hazard":
        return "no flagged elements"
    if name == "simplicity":
        return f"{r.n_elements} elements"
    if name == "dielectric":
        return (
            f"dielectric constant {r.kappa_total:.1f}" if r.kappa_total is not None else "κ missing"
        )
    return name


def template_rationale(cand: Candidate, suit: Suitability, haz_cfg: dict) -> str:
    present = [c for c in suit.criteria if c.score is not None and c.effective_weight > 0]
    top = sorted(present, key=lambda c: -c.contribution)[:2]
    parts = [_phrase(c.name, cand) for c in top]
    weak = [c for c in present if c.score < 0.5]
    text = f"Strongest: {'; '.join(parts)}."
    if weak:
        w = min(weak, key=lambda c: c.score)
        if w.name == "hazard":
            flagged = ", ".join(
                f.element for f in hazards.flags_for(cand.representative.elements, haz_cfg)
            )
            text += f" Held back by hazard flags ({flagged})."
        else:
            text += f" Held back by {_phrase(w.name, cand)}."
    return text


def caveats_for(cand: Candidate, suit: Suitability, xc: CrossCheck, s: dict) -> list[str]:
    r = cand.representative
    out: list[str] = []
    _, method = primary_gap(r)
    if method == "OptB88vdW":
        out.append(
            "Band gap is the OptB88vdW fallback (no TBmBJ value): probably an underestimate."
        )
    if xc.status == "disagree":
        out.append(f"OQMD disagrees on stability: {xc.detail}.")
    corr = sorted(set(r.elements) & set(s["candidates"]["unreliable_zero_gap_elements"]))
    if corr:
        out.append(
            f"Contains {', '.join(corr)}: DFT energies and gaps are less reliable for these "
            "elements, so stability and gap may be wrong."
        )
    if cand.known_phase_note:
        out.append(cand.known_phase_note)
    for f in hazards.flags_for(r.elements, s["hazards"]):
        out.append(
            f"Element flag {f.element}: {'; '.join(f.wording)}." + (f" {f.note}" if f.note else "")
        )
    note = hazards.compound_note(cand.formula, s["hazards"])
    if note:
        out.append(
            f"Compound-form hazard not captured by element flags: IARC '{note['source_wording']}'. {note['note']}"
        )
    if (r.e_hull or 0) >= 0.0005:
        out.append(f"Metastable: {r.e_hull * 1000:.0f} meV/atom above the recomputed hull.")
    if not r.has_icsd and not xc.icsd_id:
        out.append("No ICSD experimental structure reference found for this polymorph.")
    if suit.missing:
        out.append(f"Missing data: {', '.join(suit.missing)} (weights renormalised over the rest).")
    if xc.status in ("unavailable", "not_found", "not_run"):
        out.append(f"Stability not cross-checked: {xc.detail}.")
    if (
        r.hull_n_compositions is not None
        and r.hull_n_compositions < s["confidence"]["sparse_hull_below"]
    ):
        out.append(
            f"Hull built from only {r.hull_n_compositions} competing compositions; stability may be overstated."
        )
    return out


def citations_for(cand: Candidate, xc: CrossCheck, s: dict, manifest: dict) -> list[Evidence]:
    r = cand.representative
    src = s["sources"]
    out = [
        Evidence(
            value=r.jid,
            source="JARVIS-DFT",
            record_id=r.jid,
            method="JARVIS-DFT dft_3d record",
            url=src["jarvis"]["record_url_template"].format(jid=r.jid),
            retrieved_at=manifest.get("raw_file_retrieved_at"),
        ),
        Evidence(
            value=manifest.get("file_name"),
            source="JARVIS-DFT",
            method="dataset (figshare)",
            record_id=manifest.get("file_name"),
            url=src["jarvis"]["dataset_doi"],
            retrieved_at=manifest.get("raw_file_retrieved_at"),
        ),
    ]
    if xc.oqmd_stability is not None:
        out.append(xc.oqmd_stability)
    for f in hazards.flags_for(r.elements, s["hazards"]):
        for key in f.sources:
            hs = s["hazards"]["sources"][key]
            out.append(
                Evidence(
                    value=f.element,
                    source="config",
                    method=hs["title"],
                    url=hs["url"],
                    retrieved_at=hs["checked"],
                )
            )
    return out


def _facts(rc: RankedCandidate) -> dict:
    r = rc.candidate.representative
    g, m = primary_gap(r)
    return {
        "formula": rc.candidate.formula,
        "rank": rc.rank,
        "suitability": round(rc.suitability.total, 3),
        "confidence": rc.confidence.level,
        "e_hull_meV_per_atom": round((r.e_hull or 0) * 1000),
        "band_gap_eV": round(g, 2) if g is not None else None,
        "gap_method": m,
        "n_elements": r.n_elements,
        "has_icsd": r.has_icsd,
        "flagged_elements": [f for f in r.elements if f in config.load("hazards")["flags"]],
    }


def _allowed_numbers(f: dict) -> list[float]:
    vals = [v for v in f.values() if isinstance(v, (int, float)) and not isinstance(v, bool)]
    return [float(v) for v in vals] + [float(f["n_elements"])]


# ---------- main ------------------------------------------------------------------------------


def run_triage(
    request: str,
    provider: str = "rules",
    overrides: dict[str, Any] | None = None,
    oqmd_enabled: bool | None = None,
    oqmd_session: Any = requests,
    snapshot_dir: Path | None = None,
    llm_client: Any = None,
) -> TriageResult:
    s = _settings()
    trace = Trace()
    notes: list[str] = []
    overrides = overrides or {}

    with trace.step("policy gate") as t:
        refusals, remainder = policy.check(request, s["policy"])
        policy.log_refusals(refusals, request, config.ROOT / s["policy"]["audit_log"])
        t["detail"] = (
            f"{len(refusals)} refusal(s): {[r.category for r in refusals]}; remainder: {remainder!r}"
        )

    with trace.step("parse request") as t:
        defaults = dict(s["ranking"]["weights"])
        crit = None
        if provider == "llm":
            try:
                crit = LLMProvider(client=llm_client).parse(remainder or "(no request)", defaults)
            except LLMUnavailable as e:
                notes.append(f"Model parser unavailable ({e}); used the rules parser instead.")
        if crit is None:
            crit = RulesProvider().parse(remainder, defaults)
        if not crit.matched:
            notes.append(
                "No usable criteria in the safe part of the request; ran the site's default triage."
            )
        t["detail"] = (
            f"provider={crit.provider}; matched={len(crit.matched)}; unparsed={crit.unparsed}"
        )

    with trace.step("apply settings and clamp") as t:
        for k, v in overrides.items():
            if k == "weights":
                crit.weights.update(v)
            elif hasattr(crit, k):
                setattr(crit, k, v)
        crit = policy.clamp(crit, s["policy"], s["candidates"])
        if not crit.weights:
            crit.weights = defaults
        t["detail"] = f"weights={crit.weights}; clamped={crit.clamped}"

    snap = str(snapshot_dir or config.SNAPSHOT_DIR)
    with trace.step("load snapshot") as t:
        recs, manifest = _records(snap)
        t["detail"] = f"{len(recs)} records; built {manifest.get('snapshot_built_at')}"

    with trace.step("candidates and filters") as t:
        cand_cfg = dict(s["candidates"], allow_extra_anions=crit.allow_extra_anions)
        cands, frep = build_candidates(list(recs), cand_cfg, s["hazards"])
        counts: dict[str, Any] = {
            "formulas": frep.formulas_in,
            **{f"dropped: {k}": v for k, v in frep.dropped.items()},
        }
        kept, review = [], []
        extra: dict[str, int] = {}

        def drop(why: str) -> None:
            extra[why] = extra.get(why, 0) + 1

        for c in cands:
            r = c.representative
            if crit.exclude_elements and set(r.elements) & set(crit.exclude_elements):
                drop(f"excluded by request: {','.join(crit.exclude_elements)}")
                continue
            if crit.max_elements and r.n_elements > crit.max_elements:
                drop(f"more than {crit.max_elements} elements")
                continue
            if crit.max_e_hull is not None and (r.e_hull is None or r.e_hull > crit.max_e_hull):
                drop(f"energy above hull > {crit.max_e_hull * 1000:.0f} meV/atom")
                continue
            if c.status == "needs_review":
                review.append(c)
                continue
            g, _ = primary_gap(r)
            if crit.min_band_gap is not None and (g is None or g < crit.min_band_gap):
                drop(f"band gap < {crit.min_band_gap} eV")
                continue
            kept.append(c)
        counts.update({f"dropped: {k}": v for k, v in extra.items()})
        counts["needs review (not ranked)"] = len(review)
        counts["ranked"] = len(kept)
        t["detail"] = str(counts)

    with trace.step("score") as t:
        scored = [
            (c, scoring.score_candidate(c, crit.weights, s["ranking"], s["hazards"])) for c in kept
        ]
        t["detail"] = f"{len(scored)} candidates scored"

    style = crit.style or s["output"]["default_style"]
    n = crit.shortlist_size or s["output"]["shortlist"][style]
    corr_els = s["candidates"]["unreliable_zero_gap_elements"]
    no_xc = CrossCheck(status="not_run", detail="OQMD cross-check runs on the shortlist only")

    with trace.step("rank (ties by offline confidence)") as t:
        prelim = [
            (c, su, confidence.assess(c, su, no_xc, s["confidence"], corr_els)) for c, su in scored
        ]
        prelim.sort(
            key=lambda x: (
                -round(x[1].total, 3),
                LEVEL_ORDER[x[2].level],
                -x[2].points,
                x[0].formula,
            )
        )
        pool = prelim[: n * 2 if s["ranking"]["rank_by"] == "confidence_adjusted" else n]
        t["detail"] = f"shortlist pool {len(pool)} of {len(prelim)}"

    use_oqmd = s["sources"]["oqmd"]["enabled"] if oqmd_enabled is None else oqmd_enabled
    with trace.step("OQMD cross-check") as t:
        xcs: dict[str, CrossCheck] = {}
        failed: str | None = None
        cache_dir = Path(snap) / "oqmd_cache"
        for c, _, _ in pool:
            if not use_oqmd:
                xcs[c.formula] = CrossCheck(status="not_run", detail="OQMD cross-check disabled")
                continue
            if failed:
                xcs[c.formula] = CrossCheck(
                    status="unavailable", detail=f"skipped after earlier failure: {failed}"
                )
                continue
            try:
                payload = oqmd.fetch(
                    c.formula,
                    s["sources"]["oqmd"],
                    s["sources"]["allowed_hosts"],
                    cache_dir,
                    session=oqmd_session,
                )
                xcs[c.formula] = oqmd.cross_check(
                    c, payload, s["sources"]["oqmd"]["agreement_tolerance_ev"]
                )
            except oqmd.SourceFailure as e:
                failed = str(e)
                xcs[c.formula] = CrossCheck(status="unavailable", detail=str(e))
        if failed:
            notes.append(
                f"OQMD cross-check failed: {failed}. Affected candidates are marked; no OQMD values shown."
            )
        t["detail"] = ", ".join(f"{k}:{v.status}" for k, v in xcs.items())

    with trace.step("confidence, caveats, citations") as t:
        final: list[tuple[Candidate, Suitability, Confidence, CrossCheck]] = []
        for c, su, _ in pool:
            xc = xcs[c.formula]
            final.append((c, su, confidence.assess(c, su, xc, s["confidence"], corr_els), xc))
        mult = s["ranking"]["confidence_multiplier"]
        if s["ranking"]["rank_by"] == "confidence_adjusted":
            final.sort(
                key=lambda x: (
                    -round(x[1].total * mult[x[2].level], 3),
                    LEVEL_ORDER[x[2].level],
                    x[0].formula,
                )
            )
        else:
            final.sort(
                key=lambda x: (
                    -round(x[1].total, 3),
                    LEVEL_ORDER[x[2].level],
                    -x[2].points,
                    x[0].formula,
                )
            )
        final = final[:n]
        ranked: list[RankedCandidate] = []
        for i, (c, su, conf, xc) in enumerate(final, 1):
            ranked.append(
                RankedCandidate(
                    rank=i,
                    candidate=c,
                    suitability=su,
                    confidence=conf,
                    cross_check=xc,
                    rationale=template_rationale(c, su, s["hazards"]),
                    caveats=caveats_for(c, su, xc, s),
                    citations=citations_for(c, xc, s, manifest),
                )
            )
        totals = [round(x.suitability.total, 3) for x in ranked]
        for rc in ranked:
            rc.tied = totals.count(round(rc.suitability.total, 3)) > 1
        t["detail"] = f"{len(ranked)} ranked"

    if crit.provider.startswith("llm") and ranked:
        with trace.step("model-worded rationales (number-checked)") as t:
            try:
                facts = [_facts(rc) for rc in ranked]
                words = llm_rationales(facts, client=llm_client)
                kept_n = 0
                for rc, f in zip(ranked, facts, strict=True):
                    sent = words.get(rc.candidate.formula)
                    if sent and number_check(sent, _allowed_numbers(f)):
                        rc.rationale = sent
                        kept_n += 1
                t["detail"] = (
                    f"{kept_n}/{len(ranked)} model sentences passed the number check; rest use template"
                )
            except LLMUnavailable as e:
                t["detail"] = f"skipped: {e}"

    settings = {
        "provider": crit.provider,
        "style": style,
        "shortlist_size": n,
        "weights": crit.weights,
        "filters": {
            "min_band_gap": crit.min_band_gap,
            "max_e_hull": crit.max_e_hull,
            "max_elements": crit.max_elements,
            "exclude_elements": crit.exclude_elements,
            "allow_extra_anions": crit.allow_extra_anions,
        },
        "rank_by": s["ranking"]["rank_by"],
        "oqmd_enabled": use_oqmd,
        "config_hashes": {k: config.file_hash(k) for k in s},
    }
    return TriageResult(
        request=request,
        criteria=crit,
        refusals=refusals,
        ranked=ranked,
        review_list=sorted(review, key=lambda c: c.formula),
        standing_caveats=s["output"]["standing_caveats"],
        notes=notes,
        filter_counts=counts,
        manifest=manifest,
        settings=settings,
        trace=trace.steps,
        created_at=datetime.now(UTC).isoformat(timespec="seconds"),
    )
