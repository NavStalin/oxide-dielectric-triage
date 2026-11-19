# Decision log

One entry per choice: the decision, the alternatives, and why. Keep each rationale to a line or two
that can be said out loud. Status is **Accepted** (from the brief or agreed with Nav), or
**Proposed** (made during planning; Nav should confirm or overrule).

Evidence for anything marked "verified" is in `docs/VERIFIED_FACTS.md`.

---

## Accepted (from the brief)

**D-001 Code decides, the model only handles language.** Filtering, scoring, policy and citations are
deterministic code. Alternative: an LLM agent that calls tools and ranks. Why: a ranking a scientist
can't reproduce can't be argued with, and the app must run with no API key.

**D-002 Python only: one library, a CLI and a Streamlit app.** Alternative: FastAPI plus React.
Why: one code path to test and explain; the design note says where an API layer would go.

**D-003 JARVIS-DFT `dft_3d` as the primary source.** Alternative: Materials Project. Why: public, no
key, one versioned file, so a snapshot is reproducible offline.

**D-004 TBmBJ gap first, OptB88vdW as a flagged fallback, no scissor correction.** Alternative: apply
an empirical shift to the fallback. Why: a correction would be an invented number; a flagged
underestimate is honest.

**D-005 OQMD cross-check for the shortlist only.** Alternative: cross-check every candidate. Why: the
API is slow and the shortlist is where a disagreement changes a decision.

**D-006 The app reads only a local snapshot with a manifest.** Alternative: live queries. Why:
reproducible results, offline use, and refresh becomes an auditable admin action.

**D-007 Pure oxides by default; group by reduced formula; show polymorphs.** Alternative: one row per
entry. Why: scientists think in compounds, and thin films often grow metastable phases.

**D-008 Hazards are element-level penalties from cited lists; no-stable-isotope elements are excluded.**
Alternative: compound toxicology. Why: no public compound-level source covers the set; the caveat
says so on every result.

**D-009 Suitability and evidence confidence are two separate numbers.** Alternative: one blended
score. Why: "good match, thin evidence" and "poor match, solid evidence" need different actions.

**D-010 Missing criteria renormalize the weights; missing is neutral for suitability and bad for
confidence.** Alternative: treat missing as zero or impute. Why: zero punishes unmeasured materials,
imputation invents data.

**D-011 Partial refusal.** Refuse prohibited parts in a line each, run the safe remainder, log the
attempt. Alternative: refuse the whole request. Why: the scientist still gets their shortlist, and
the refusal is visible.

**D-012 The main safety control is absent capability.** No tools exist for private drives, paywalled
papers, instruments or arbitrary URLs. Alternative: rely on prompt instructions. Why: a model can't
be talked into using a tool that isn't there.

---

## Proposed during planning (need Nav's confirmation)

**D-013 Recompute energy above hull; don't use the JARVIS `ehull` field.** *Changes brief decision 2.*
**Accepted by Nav 2026-11-17.**
Verified: ground-state HfO2, Al2O3 and SiO2 carry `ehull` of 1.4 to 1.8 eV/atom and only 328 of 25,194
O-containing records are within 0.1 eV, so the field would zero out every classic dielectric. A hull
recomputed from JARVIS `formation_energy_peratom` over all 93,902 records puts those ground states at
0 meV. Alternatives: (a) use the field as is (unusable); (b) rank on formation energy alone (not a
stability measure); (c) use OQMD stability as primary (needs thousands of slow API calls, breaks
offline use). Why this one: single functional, fully offline, every input is a fetched record, and the
value is labelled "derived" with the number of competing phases shown. The raw field is kept in the
snapshot and shown in the audit view, never scored.

**D-014 Representative polymorph is the lowest recomputed hull, with a "known phase" note.** If the
representative has no ICSD reference and another polymorph within 30 meV/atom (configurable) does, the
row names that polymorph too. Verified cases: ZrO2 (Pbca at 0 vs ICSD P2_1/c at +3 meV) and MgO
(I4/mmm 30 meV below rock salt). Alternative: prefer ICSD entries outright. Why: keeps the rule simple
and thermodynamic, while not hiding the phase people actually grow.

**D-015 The fallback gap is scored as is.** Only 20.5% of O-containing records have a TBmBJ gap, so
the fallback is the common case. The OptB88vdW value is scored without adjustment, which under-ranks
those materials on band gap; the row says "probable underestimate" and confidence drops. Alternative:
score fallback gaps on a shifted scale (an invented correction), or drop materials without TBmBJ (loses
Y2O3 and La2O3). Why: conservative and honest, and the audit view lets a scientist filter to TBmBJ only.

**D-016 Use `dfpt_piezo_max_dielectric` for κ, never `epsx/y/z`.** The `eps*` fields are optical,
electronic-only values and would understate κ badly. DFPT κ exists for 6.9% of O-containing records,
which is why its default weight is 0.

**D-017 OQMD is called live for the shortlist, with a 10 s timeout and an on-disk cache.** Failure
degrades to "cross-check unavailable", named in the output, with confidence lowered. Alternative:
pre-fetch OQMD into the snapshot (thousands of calls). Why: keeps snapshots fast; the cache makes
repeat runs and evals offline.

**D-018 Match JARVIS to OQMD by reduced formula, then space group; fall back to the lowest OQMD
stability for that formula.** The comparison type (same phase or formula-level) is shown. Why: the two
databases label cells differently, and a formula-level check is still informative.

**D-019 Confidence is a points rubric in `config/confidence.yaml`.** See `docs/PLAN.md` section 5.
Alternative: a learned or continuous score. Why: three levels a PI can read, with the arithmetic shown.

**D-020 Python 3.12, `uv`, `src/` layout.** Why: a lockfile gives site IT a one-command install.

**D-021 Commit `data/snapshot/` to the repo; ignore `data/raw/`.** Why: a reviewer can run the app
without a 46 MB download; the manifest says exactly what they're looking at.

**D-022 Known-answer sanity checks, as code, run on every snapshot and query.** Agreed with Nav
2026-11-17. The `ehull` problem was caught by testing the data against materials whose answer is known;
this makes that habit permanent (`docs/PLAN.md` section 9a). Alternative: rely on a reviewer noticing.
Why: the same class of error is caught next time automatically, and a refreshed dataset that changes
silently stops the snapshot.

**D-023 No memory or RAG that learns from past runs in this submission; describe a staged learning
loop as a next step instead.** Agreed with Nav 2026-11-17. Alternative: an LLM that distils lessons
from previous runs into a self-updating checklist. Why: without experimental feedback it learns from
its own outputs, it breaks reproducibility (the same query could change answer week to week), its
lessons can't be cited, and a learning memory can be poisoned by users. The roadmap (checks as code →
model proposes checks, scientist approves → lab results calibrate confidence) is in
`docs/TALK_NOTES.md` and the design note.

**D-024 Keep scope to oxide dielectrics; show flexibility inside it.** Agreed with Nav 2026-11-18.
Alternative: support other materials classes (batteries, catalysts). Why: each class needs its own
science, checks and caveats; depth gives a defensible story in four days. A second eval request with
different preferences shows the tool isn't tied to the example sentence, and the design note says what
extending to another class would take.

## Milestone 1 (2026-11-18)

**D-025 Snapshot keeps all 25,194 O-containing records; candidate filters run at query time.** Why: the
admin toggle for extra anions must work without rebuilding. Hull competitors come from all 93,902 records.
Runtime 15 s, so no caching needed.

**D-026 A failed `fail` check never replaces a good snapshot.** Built in `data/snapshot.tmp/`, swapped in
only if C1, C4 and C5 pass. Why: a bad refresh must not silently change rankings.

**D-027 Representative = lowest recomputed hull; ties within 1 meV prefer ICSD, then TBmBJ, then lower
formation energy, then jid.** Why: 1 meV is far below DFT error, so among equals pick the best-evidenced
entry. SiO2 has three quartz entries at 0 meV.

**D-028 Metal filter: a formula is dropped when its representative's gap (TBmBJ, else OptB88vdW) is ≤ 0.**
Drops 5,639 formulas. **Open: see D-030.**

**D-029 No dimensionality filter.** JARVIS labels 3,097 of 5,369 candidate representatives as
"intercalated ion" and only 2,046 as "3D-bulk"; the labels don't map to anything a thin-film scientist
would filter on. Shown in the audit view only.

**D-030 (proposed) Zero gaps for f-electron and open-shell 3d oxides are unreliable.** Found in real data:
Yb2O3 has OptB88vdW gap 0.0 and sits 355 meV above the hull, so it is dropped as a metal, while YbO appears
on the hull. NiO has gap 0.0 with both methods. Both are insulators experimentally. 33 of 56 lanthanide
binary oxides are dropped as metals. Proposal: for compounds containing Ce–Yb or V, Cr, Mn, Fe, Co, Ni, Cu,
treat a zero gap as missing (not as metal), add a caveat, and lower confidence. Alternative: keep dropping
them (silently loses real insulators). **Accepted by Nav 2026-11-18.**
Implementation detail: a missing gap can't simply be renormalised away, or real metals like Fe3O4 would
score 1.0 on stability, hazard and simplicity alone. So these formulas are **listed for review, not
ranked**: 3,520 formulas, shown as a count plus a collapsible list in the audit view. Element list is in
`config/candidates.yaml` (`unreliable_zero_gap_elements`).

**D-031 (proposed) Break suitability ties by evidence confidence, and show ties explicitly.** Found: 67
formulas score ≥ 0.95 and 4 score exactly 1.0, so the top of the list is ordered alphabetically today.
Alternative: stretch the scoring scales so fewer saturate (tuning to make the list look different). Why:
ties are honest; among equals, the better-evidenced material should come first. **Accepted by Nav
2026-11-18; implemented in Milestone 2 with the confidence rubric.**

**D-032 Hazard sources confirmed word for word (2026-11-18).** RoHS Annex II wording from EUR-Lex 2015/863;
IARC Group 1 wording from the IARC list's own data file. IARC lists crystalline silica dust (quartz) as
Group 1, which the element rule cannot catch; it is a compound-level caveat for SiO2, not a penalty.
Th and U exclusion is cited via IARC; Pa is excluded by admin policy without an external citation
(CIAAW gives Th, Pa, U standard atomic weights).

## Milestone 2 (2026-11-18)

**D-033 Confidence −1 for f-electron and open-shell 3d elements, even with a positive gap.** Same
elements as D-030. Found: YbO ranks #5 on default settings (on the hull, TBmBJ gap 5.80 eV, ICSD) while
Yb2O3, the oxide that actually forms, is mis-described. The penalty and a top-priority caveat flag it
without hiding it. Alternative: exclude these elements (too blunt; many are fine).

**D-034 Ties are broken by confidence computed without OQMD, for every candidate.** OQMD runs on the
shortlist only (D-005), so the tie-break must use evidence available offline for all tied candidates;
OQMD then refines confidence on the shortlist. Ties are labelled "(tie)" in both views.

**D-035 OQMD client: `sort_by=stability`, limit 50, 10 s timeout, one retry, then stop for the run.**
OQMD returned HTTP 502 for most of 2026-11-18. After the first failure the remaining shortlist is marked
"skipped after earlier failure" instead of waiting about 20 s per formula. The failure is named in a run
note and on every affected row, and no OQMD value is shown. Successful responses are cached on disk.

**D-036 Model output uses a flat schema with "keep default" sentinels.** The API rejected the first
schema (optional and nullable fields) with "Schema is too complex" (verified 2026-11-18). All fields
are now required; −1 / 0 / "default" mean "no change". The model's criteria pass through the same policy
clamp as the rules parser, and any error or refusal falls back to the rules parser with a note.

**D-037 Model-worded rationales only with the Claude parser, and only if every number passes the
check.** Each sentence is checked against the candidate's own values (rounded to the precision written);
a failing sentence is replaced by the template wording. Live test: 4/4 sentences passed.

**D-038 Hazard compound notes are caveats, not penalties.** SiO2 shows the IARC crystalline-silica
note as its key caveat; its hazard score stays 1.0 because the element rule is the stated method.

**D-039 Citation hosts are listed separately from fetch hosts.** The app fetches only from
`allowed_hosts` (figshare, OQMD); citation links may point to `citation_hosts` (NIST JARVIS pages, DOI,
EUR-Lex, IARC). Keeps "what the app can reach" distinct from "where a scientist can click".

## Milestone 3 (2026-11-19)

**D-040 A criterion that's off by default requires data once a request turns it on.** Found by
eval 5. With "missing is neutral" (D-010), the request "High-k oxides for capacitors" returned Li2O,
B2O3, HfO2, AlBO3 and Ca3B2O6. None of the five has a DFPT κ, so all five beat oxides that do. Now,
when a criterion has weight 0 in `ranking.yaml` and the request or a slider raises it, candidates
without that value are dropped from ranking and counted in the funnel (8,430 dropped for κ).
Configured in `ranking.yaml` `require_data_when_enabled`.
- Alternatives considered:
  - Score missing κ as 0: hides the reason.
  - Keep it neutral: the result answers a different question from the one asked.
- The default request is unchanged. Accepted by Nav 2026-11-19.

**D-041 Very large DFPT κ gets a caution caveat, not a different score.** In the snapshot:
- 133 of 1,734 κ values are above 100, and the largest is 1,176.
- LuTaO4 (277) reached the eval 5 shortlist.

Very large ionic contributions usually mean a soft polar mode near an instability. The score already
saturates at κ = 25, so the outlier doesn't dominate. It is now flagged above
`dielectric.caveat_above` (100). The threshold is a judgment call and lives in config.

**D-042 Only the representative polymorph's own κ is used; no borrowing from other polymorphs.**
Monoclinic HfO2, the stable form, has no κ. Four other HfO2 polymorphs do (e.g. P4_2/nmc 141, Pca2_1
24). Using them would score a phase different from the one whose stability and gap are scored. So
HfO2 can't be ranked on κ. Reported as a data-coverage finding, not patched.

**D-043 The face-validity report uses the pipeline's own ranking function.** `rank_offline` was pulled
out of `run_triage` so the report places all 5,369 formulas with exactly the same ordering as the
app. Where a representative has no TBmBJ gap, the report names the lowest-energy polymorph that has
one. It doesn't pick the polymorph with the largest gap, which would be cherry-picking.

---

## Open questions for Nav

1. ~~Confirm D-013 (recomputed hull).~~ Accepted 2026-11-17.
2. ~~Which LLM key?~~ Anthropic, set up 2026-11-18 in `.env` (git-ignored). Model `claude-opus-5-5`.
3. Public GitHub repo or a zip for the recruiting coordinator?
