# Milestone log

Short status for each milestone: what was built, what we found, what's still open. The details are in
`docs/PLAN.md` (the checklist), `DECISIONS.md` (the reasons) and `docs/TALK_NOTES.md` (the talk
material). Add a section when each milestone closes.

| Milestone | Planned date | Status | Commit |
|---|---|---|---|
| 1. Data and scoring | Wed 18 Nov | Done | `de1ee57` |
| 2. Policy, cross-check, views, interfaces | Thu 19 Nov | Done (finished early, 18 Nov) | pending |
| 3. Evals and README | Fri 20 Nov | Not started | |
| 4. Design note and final review | Sat 21 Nov | Not started | |

---

## Milestone 1: data and scoring (done 2026-11-18)

**Built**
- A JARVIS-DFT snapshot of 25,194 oxygen-containing records, written to `data/snapshot/` along with
  a manifest that gives the source URL, DOI and file hashes.
- Energy above hull recomputed from JARVIS formation energies over all 93,902 records. This replaces
  the broken `ehull` field (D-013). The rebuild takes 15 s.
- Candidate filters (no metals, non-oxide anions or radioactive elements) and a choice of one
  polymorph per formula, with a note when that isn't the commonly grown phase.
- Scoring across stability, band gap, hazard and simplicity. Weights live in `config/ranking.yaml`.
  A missing criterion is dropped and the rest are reweighted, so it doesn't count against the
  material.
- Hazard flags from cited RoHS and IARC sources.
- Sanity checks C1–C5 on every snapshot. A snapshot that fails a check never replaces the current
  one.

**Results**
- Sanity checks:
  - C1: 6/6 known ground states sit on the recomputed hull.
  - C2: 1/6 known ground states sit on the hull using the raw JARVIS field (only MgO), which
    confirms that field is broken.
- Funnel: 15,671 formulas → 5,369 candidates.
- First ranking: Al2O3 #1, SiO2 #4, HfO2 #6, Y2O3 #286, La2O3 #431, ZrO2 #473. The low three
  have no TBmBJ gap and fall back to the OptB88vdW gap. That was predicted, and the weights were
  not tuned to move them.

**Findings**
- DFT gets f-electron and some 3d oxides wrong:
  - It puts Yb2O3 at 355 meV above the hull and says it is metallic.
  - It says NiO is metallic.
  - In reality both are insulators.
  - Zero-gap formulas containing these elements go to a review list rather than being ranked
    (D-030).
- The top of the list is effectively a tie: 67 formulas score ≥ 0.95 (D-031).
- Crystalline silica is a carcinogen, but a rule that looks only at elements can't flag SiO2.
- Li2O and B2O3 rank near the top but react with moisture. The tool doesn't model that.

**Decisions:** D-025 to D-032 (D-030 and D-031 approved by Nav).

---

## Milestone 2: policy, cross-check, views, interfaces (done 2026-11-18)

**Built**
- **Policy gate:** six categories of prohibited request.
  - Each prohibited part gets a one-line refusal and the rest of the request still runs.
  - Refusals are logged to `logs/audit.jsonl`.
  - A clamp stops a request from loosening policy.
- **Request parsers:**
  - Keyword rules, the default: offline and deterministic.
  - Claude Opus 5.5, optional: works live in about 5 s and falls back to the rules parser on any
    error.
- **OQMD cross-check** on the shortlist: one retry, and if it fails, the rest of the shortlist is
  marked skipped.
- **Evidence confidence** (High/Medium/Low), kept separate from suitability. Ties are broken by
  confidence and labelled "(tie)".
- **Outputs:**
  - Two views, a PI summary and an audit view, exportable as Markdown or JSON.
  - CLI: `triage query`.
  - Streamlit app: sliders, an OQMD toggle, a κ-vs-band-gap plot and downloads.
- **Model explanations** are shown only if every number in them matches the data.
- **Tests:** 84 pass, lint is clean, and the app is tested headlessly.

**Results**
- On the example request, Al2O3, SiO2, Li2O and B2O3 tie at 1.000. Confidence orders them: High,
  High, Medium, Low.
- For the adversarial request:
  - Five refusals.
  - The rest of the request runs and returns the default shortlist with citations.

**Findings**
- OQMD returned HTTP 502 most of the day.
  - The app said so, stopped after one retry and showed no OQMD values.
  - The path where JARVIS and OQMD agree or disagree has only been tested against simulated
    responses.
- YbO ranks #5, but Yb2O3 is the oxide that actually forms. Its DFT warning now comes first in its
  list of caveats and its confidence is lowered (D-033).
- The model parser said plainly that it has no criterion for "thin film" and didn't guess.
- The API rejected the first model schema as "too complex". The model now fills a flat form, and
  validation stays in code (D-036).

**Decisions:** D-033 to D-039.

**Open:** retry a live OQMD cross-check before the talk. The Materials Project adapter (optional in
the brief) wasn't built.

---

## Milestone 3: evals and README (planned Fri 20 Nov)

To fill in when done: eval results 1–5, the face-validity table and the README.

## Milestone 4: design note and final review (planned Sat 21 Nov)

To fill in when done: the design note, the diagram, the requirement-by-requirement check against
section 0 of `PLAN.md` and a test from a clean clone.
