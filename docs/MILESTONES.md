# Milestone log

Short status for each milestone: what was built, what we found, what's still open. The details are in
`docs/PLAN.md` (the checklist), `DECISIONS.md` (the reasons). Add a section when each milestone closes.

| Milestone | Planned date | Status | Commit |
|---|---|---|---|
| 1. Data and scoring | Wed 18 Nov | Done | `2d8d8a6` |
| 2. Policy, cross-check, views, interfaces | Thu 19 Nov | Done (finished early, 18 Nov) | `98292be` |
| 3. Evals and README | Fri 20 Nov | Done (finished early, 19 Nov) | `cf8ee5a` |
| 4. Design note and final review | Sat 21 Nov | Done (finished early, 19 Nov) | `14e3f6f` |

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

## Milestone 3: evals and README (done 2026-11-19)

**Built**
- **Eval suite:** `make evals` runs five cases through the same code path as the app and writes
  verdicts plus both rendered views to `evals/results/`. Cases are in `evals/cases.yaml`.
  - Options: `--provider llm` runs the cases through Claude; `--live-oqmd` tries the real OQMD.
- **Face-validity report** (`evals/face_validity.py`): uses the pipeline's own ranking, and explains
  each position from the score arithmetic.
- **README:** a scientist quick start, a site IT section (install, snapshot, config, offline,
  optional key, logs), the "who changes what" table and the eval table.
- **Tests:** 88 pass (4 new), and lint is clean.

**Results**
- Evals 1, 2, 3 and 5: 24/24 checks pass. Eval 4 is a report.
- Face validity: Al2O3 #1, SiO2 #2, HfO2 #6, Y2O3 #288, La2O3 #434, ZrO2 #474 of 5,369.
  - The low three lose all their points on band gap, because all three use the fallback gap.
  - This was predicted, and the weights were not tuned.

**Findings**
- **Eval 5 first passed for the wrong reason.** For "High-k oxides for capacitors", none of the top 5
  had any κ data. "Missing is neutral" let no-data materials win.
  - Fix (D-040): a criterion the request turns on requires data. 8,430 formulas without κ are
    dropped and counted.
  - New shortlist, each with a cited κ: NaSmO2, LuTaO4, NaPrO2, TeO2, SnB4O7.
- **HfO2 can't be ranked on κ:** its stable form has no DFPT value in JARVIS. We don't borrow values
  from other polymorphs (D-042).
- **κ outliers:** 133 values are above 100 (largest 1,176). LuTaO4 (277) now carries a caution
  caveat (D-041).

**Decisions:** D-040 to D-043. D-040 accepted by Nav.

**Open:** OQMD was still timing out on 2026-11-19, so a live cross-check remains for before the talk.

## Milestone 4: design note and final review (done 2026-11-19)

**Built**
- **Design note** (`docs/DESIGN_NOTE.md` and `.pdf`): 3.75 pages including the diagram, following
  the brief's six sections.
  - It opens with the suitability/confidence split and the `ehull` catch.
  - Section 6 has the learning roadmap and a sentence on extending to another class of materials.
- **Diagram** (`docs/architecture.svg` / `.png`): generated by `scripts/make_diagram.py`. `make note`
  rebuilds the diagram and the PDF.
- **README:** new table proving each requirement (R1–R6, L1–L4) with a file or test name.

**Clean-clone test**
- Setup: a fresh copy of exactly the shippable files (no `.env`, `data/raw` or logs), then
  `make setup`.
- With outbound network blocked by a macOS sandbox and no API key set:
  - 88/88 tests pass.
  - 24/24 eval checks pass.
  - The Streamlit server starts and serves its page (health check returns 200).
- The first test run took 74 s, which was one-time startup cost; the repeat run took 15 s.

**Open**
- ~~A live OQMD cross-check before the talk.~~ Replaced on 2026-11-20: see "After milestone 4" below.
- Public GitHub repo or zip.
- Sunday buffer: Nav reads the note and the README.

## After milestone 4 (2026-11-20): cross-check source changed

- **Why:** OQMD failed or took about 30 s per query on 18, 19 and 20 November, so the live cross-check
  had never run.
- **What changed:** Alexandria (public, no key, CC BY 4.0) is the default cross-check. OQMD is still
  selectable in `config/sources.yaml` (D-044). Mirror-image space groups are treated as one phase
  (D-045). The design note no longer says Lila's brief named the `ehull` field (D-046).
- **Live result:** the example request cross-checked in a few seconds. Al2O3, SiO2, Li2O and B2O3 agree.
  YbO disagrees by 294 meV/atom and now carries that caveat. See `evals/results/live_crosscheck.md`.
- **Tests:** 96 pass. Evals: 24/24 offline checks pass.
