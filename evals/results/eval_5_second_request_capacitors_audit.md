# Oxide dielectric triage: audit view

**Request:** High-k oxides for capacitors. I can accept a smaller band gap and ternaries are fine.
**Run:** 2026-11-20T22:03:53+00:00 · parser `rules` · style `pi` · shortlist 5 · rank by `suitability`

## Refusals and notes
No part of the request was refused.

## How the request was read
- 'High-k oxides for capacitors' -\> dielectric constant criterion on \(weight 0\.25\)
- 'I can accept a smaller band gap' -\> band gap weight lowered to 0\.15
- 'ternaries are fine' -\> simplicity weight lowered to 0\.05 \(ternaries fine\)

## 1. NaSmO2: Suitability 0.972, Evidence confidence Medium (2 pts)

Strongest: on the convex hull; dielectric constant 32.8.

**Representative:** [JVASP-50889](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-50889.html) · space group I4_1/amd · origin mp-754027 · retrieved 2026-11-17T20:56:28+00:00

| Value | Raw | Unit | Method / source |
|---|---|---|---|
| Energy above hull | 0 | meV/atom | recomputed hull from JARVIS formation energies, 16 competing compositions (D-013) |
| JARVIS `ehull` field | 0.6757 | eV/atom | not used (failed known-answer check C2, D-013) |
| Formation energy | -2.929 | eV/atom | JARVIS-DFT, OptB88vdW |
| Band gap, TBmBJ | 5.660 | eV | JARVIS-DFT |
| Band gap, OptB88vdW | 3.987 | eV | JARVIS-DFT |
| κ total (DFPT) | 32.76 | – | JARVIS-DFT, max component |
| κ electronic / ionic | 3.86 / 28.90 | – | JARVIS-DFT |
| ICSD references | 0 | – | none |
| Dimensionality label | intercalated ion | – | JARVIS (not filtered on, D-029) |

| Criterion | Input | Score | Weight | Effective weight | Contribution |
|---|---|---|---|---|---|
| Stability | 0 eV/atom (recomputed hull (D-013)) | 1.000 | 0.35 | 0.350 | 0.350 |
| Band gap | 5.66 eV (TBmBJ) | 0.915 | 0.15 | 0.150 | 0.137 |
| Element hazard | none  (element-level flags (config/hazards.yaml)) | 1.000 | 0.20 | 0.200 | 0.200 |
| Simplicity | 3 elements (count of distinct elements) | 0.700 | 0.05 | 0.050 | 0.035 |
| Dielectric constant (κ) | 32.8  (DFPT total, max component) | 1.000 | 0.25 | 0.250 | 0.250 |
| **Total** | | | | | **0.972** |

**Confidence:** +2 band gap from TBmBJ; +0 no ICSD reference found; +0 no stability cross-check (not_run: cross-check turned off); +1 all weighted criteria have values; -1 contains Sm: DFT energies and gaps less reliable.

**Cross-check:** not_run. cross-check turned off
**Caveats:**
- Contains Sm: DFT energies and gaps are less reliable for these elements, so stability and gap may be wrong.
- No ICSD experimental structure reference found for this polymorph.
- Stability not cross-checked: cross-check turned off.

**Polymorphs** (2 in JARVIS; first 5 by energy):

| JARVIS ID | Space group | Energy above hull (meV/atom) | TBmBJ gap | OptB88vdW gap | ICSD |
|---|---|---|---|---|---|
| JVASP-50889 | I4_1/amd | 0 | 5.66 | 3.99 | no |
| JVASP-50348 | R-3m | 27 | 5.74 | 4.28 | no |

**Sources:**
- JARVIS-DFT dft_3d record: [JVASP-50889](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-50889.html), retrieved/checked 2026-11-17T20:56:28+00:00
- dataset (figshare): [jdft_3d-9-24-2025.json](https://doi.org/10.6084/m9.figshare.6815699), retrieved/checked 2026-11-17T20:56:28+00:00

---
## 2. LuTaO4: Suitability 0.961, Evidence confidence High (5 pts)

Strongest: on the convex hull; dielectric constant 276.9.

**Representative:** [JVASP-4492](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-4492.html) · space group P2/c · origin mp-5489 · retrieved 2026-11-17T20:56:28+00:00

| Value | Raw | Unit | Method / source |
|---|---|---|---|
| Energy above hull | 0 | meV/atom | recomputed hull from JARVIS formation energies, 16 competing compositions (D-013) |
| JARVIS `ehull` field | 2.6821 | eV/atom | not used (failed known-answer check C2, D-013) |
| Formation energy | -3.536 | eV/atom | JARVIS-DFT, OptB88vdW |
| Band gap, TBmBJ | 5.360 | eV | JARVIS-DFT |
| Band gap, OptB88vdW | 4.119 | eV | JARVIS-DFT |
| κ total (DFPT) | 276.93 | – | JARVIS-DFT, max component |
| κ electronic / ionic | 275.64 / 1.29 | – | JARVIS-DFT |
| ICSD references | 3 | – | 415461, 155662, 20261 |
| Dimensionality label | 3D-bulk | – | JARVIS (not filtered on, D-029) |

| Criterion | Input | Score | Weight | Effective weight | Contribution |
|---|---|---|---|---|---|
| Stability | 0 eV/atom (recomputed hull (D-013)) | 1.000 | 0.35 | 0.350 | 0.350 |
| Band gap | 5.36 eV (TBmBJ) | 0.840 | 0.15 | 0.150 | 0.126 |
| Element hazard | none  (element-level flags (config/hazards.yaml)) | 1.000 | 0.20 | 0.200 | 0.200 |
| Simplicity | 3 elements (count of distinct elements) | 0.700 | 0.05 | 0.050 | 0.035 |
| Dielectric constant (κ) | 277  (DFPT total, max component) | 1.000 | 0.25 | 0.250 | 0.250 |
| **Total** | | | | | **0.961** |

**Confidence:** +2 band gap from TBmBJ; +2 experimental structure reference (ICSD, via JARVIS); +0 no stability cross-check (not_run: cross-check turned off); +1 all weighted criteria have values.

**Cross-check:** not_run. cross-check turned off
**Caveats:**
- DFPT dielectric constant 277 is unusually large (above 100); often a sign of a soft polar mode near an instability. Treat κ with caution.
- Stability not cross-checked: cross-check turned off.

**Polymorphs** (2 in JARVIS; first 5 by energy):

| JARVIS ID | Space group | Energy above hull (meV/atom) | TBmBJ gap | OptB88vdW gap | ICSD |
|---|---|---|---|---|---|
| JVASP-4492 | P2/c | 0 | 5.36 | 4.12 | yes |
| JVASP-91215 | C2/c | 3 | 5.34 | 4.08 | yes |

**Sources:**
- JARVIS-DFT dft_3d record: [JVASP-4492](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-4492.html), retrieved/checked 2026-11-17T20:56:28+00:00
- dataset (figshare): [jdft_3d-9-24-2025.json](https://doi.org/10.6084/m9.figshare.6815699), retrieved/checked 2026-11-17T20:56:28+00:00

---
## 3. NaPrO2: Suitability 0.957, Evidence confidence High (4 pts)

Strongest: on the convex hull; dielectric constant 31.1.

**Representative:** [JVASP-2829](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-2829.html) · space group I4_1/amd · origin mp-8470 · retrieved 2026-11-17T20:56:28+00:00

| Value | Raw | Unit | Method / source |
|---|---|---|---|
| Energy above hull | 0 | meV/atom | recomputed hull from JARVIS formation energies, 18 competing compositions (D-013) |
| JARVIS `ehull` field | 0.7424 | eV/atom | not used (failed known-answer check C2, D-013) |
| Formation energy | -2.826 | eV/atom | JARVIS-DFT, OptB88vdW |
| Band gap, TBmBJ | 5.264 | eV | JARVIS-DFT |
| Band gap, OptB88vdW | 3.624 | eV | JARVIS-DFT |
| κ total (DFPT) | 31.05 | – | JARVIS-DFT, max component |
| κ electronic / ionic | 3.93 / 27.13 | – | JARVIS-DFT |
| ICSD references | 1 | – | 61682 |
| Dimensionality label | intercalated ion | – | JARVIS (not filtered on, D-029) |

| Criterion | Input | Score | Weight | Effective weight | Contribution |
|---|---|---|---|---|---|
| Stability | 0 eV/atom (recomputed hull (D-013)) | 1.000 | 0.35 | 0.350 | 0.350 |
| Band gap | 5.26 eV (TBmBJ) | 0.816 | 0.15 | 0.150 | 0.122 |
| Element hazard | none  (element-level flags (config/hazards.yaml)) | 1.000 | 0.20 | 0.200 | 0.200 |
| Simplicity | 3 elements (count of distinct elements) | 0.700 | 0.05 | 0.050 | 0.035 |
| Dielectric constant (κ) | 31.1  (DFPT total, max component) | 1.000 | 0.25 | 0.250 | 0.250 |
| **Total** | | | | | **0.957** |

**Confidence:** +2 band gap from TBmBJ; +2 experimental structure reference (ICSD, via JARVIS); +0 no stability cross-check (not_run: cross-check turned off); +1 all weighted criteria have values; -1 contains Pr: DFT energies and gaps less reliable.

**Cross-check:** not_run. cross-check turned off
**Caveats:**
- Contains Pr: DFT energies and gaps are less reliable for these elements, so stability and gap may be wrong.
- Stability not cross-checked: cross-check turned off.

**Sources:**
- JARVIS-DFT dft_3d record: [JVASP-2829](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-2829.html), retrieved/checked 2026-11-17T20:56:28+00:00
- dataset (figshare): [jdft_3d-9-24-2025.json](https://doi.org/10.6084/m9.figshare.6815699), retrieved/checked 2026-11-17T20:56:28+00:00

---
## 4. TeO2: Suitability 0.949, Evidence confidence High (5 pts)

Strongest: on the convex hull; dielectric constant 28.8.

**Representative:** [JVASP-57128](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-57128.html) · space group P4_12_12 · origin mp-561224 · retrieved 2026-11-17T20:56:28+00:00

| Value | Raw | Unit | Method / source |
|---|---|---|---|
| Energy above hull | 0 | meV/atom | recomputed hull from JARVIS formation energies, 7 competing compositions (D-013) |
| JARVIS `ehull` field | 1.3228 | eV/atom | not used (failed known-answer check C2, D-013) |
| Formation energy | -1.118 | eV/atom | JARVIS-DFT, OptB88vdW |
| Band gap, TBmBJ | 4.645 | eV | JARVIS-DFT |
| Band gap, OptB88vdW | 3.041 | eV | JARVIS-DFT |
| κ total (DFPT) | 28.84 | – | JARVIS-DFT, max component |
| κ electronic / ionic | 6.45 / 22.39 | – | JARVIS-DFT |
| ICSD references | 1 | – | 34423 |
| Dimensionality label | 3D-bulk | – | JARVIS (not filtered on, D-029) |

| Criterion | Input | Score | Weight | Effective weight | Contribution |
|---|---|---|---|---|---|
| Stability | 0 eV/atom (recomputed hull (D-013)) | 1.000 | 0.35 | 0.350 | 0.350 |
| Band gap | 4.64 eV (TBmBJ) | 0.661 | 0.15 | 0.150 | 0.099 |
| Element hazard | none  (element-level flags (config/hazards.yaml)) | 1.000 | 0.20 | 0.200 | 0.200 |
| Simplicity | 2 elements (count of distinct elements) | 1.000 | 0.05 | 0.050 | 0.050 |
| Dielectric constant (κ) | 28.8  (DFPT total, max component) | 1.000 | 0.25 | 0.250 | 0.250 |
| **Total** | | | | | **0.949** |

**Confidence:** +2 band gap from TBmBJ; +2 experimental structure reference (ICSD, via JARVIS); +0 no stability cross-check (not_run: cross-check turned off); +1 all weighted criteria have values.

**Cross-check:** not_run. cross-check turned off
**Caveats:**
- Stability not cross-checked: cross-check turned off.

**Polymorphs** (12 in JARVIS; first 5 by energy):

| JARVIS ID | Space group | Energy above hull (meV/atom) | TBmBJ gap | OptB88vdW gap | ICSD |
|---|---|---|---|---|---|
| JVASP-57128 | P4_12_12 | 0 | 4.64 | 3.04 | yes |
| JVASP-9137 | P4_32_12 | 0 | 4.64 | 3.04 | yes |
| JVASP-9161 | P4_12_12 | 0 | 4.64 | 3.04 | yes |
| JVASP-18990 | Pbca | 3 | 3.77 | 2.18 | yes |
| JVASP-12071 | Pbca | 3 | missing | 2.19 | yes |

**Sources:**
- JARVIS-DFT dft_3d record: [JVASP-57128](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-57128.html), retrieved/checked 2026-11-17T20:56:28+00:00
- dataset (figshare): [jdft_3d-9-24-2025.json](https://doi.org/10.6084/m9.figshare.6815699), retrieved/checked 2026-11-17T20:56:28+00:00

---
## 5. SnB4O7: Suitability 0.947, Evidence confidence High (5 pts)

Strongest: on the convex hull; dielectric constant 27.8.

**Representative:** [JVASP-49166](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-49166.html) · space group Pmn2_1 · origin mp-13252 · retrieved 2026-11-17T20:56:28+00:00

| Value | Raw | Unit | Method / source |
|---|---|---|---|
| Energy above hull | 0 | meV/atom | recomputed hull from JARVIS formation energies, 26 competing compositions (D-013) |
| JARVIS `ehull` field | 3.3797 | eV/atom | not used (failed known-answer check C2, D-013) |
| Formation energy | -2.387 | eV/atom | JARVIS-DFT, OptB88vdW |
| Band gap, TBmBJ | 4.992 | eV | JARVIS-DFT |
| Band gap, OptB88vdW | 3.754 | eV | JARVIS-DFT |
| κ total (DFPT) | 27.78 | – | JARVIS-DFT, max component |
| κ electronic / ionic | 3.93 / 23.85 | – | JARVIS-DFT |
| ICSD references | 1 | – | 249206 |
| Dimensionality label | 3D-bulk | – | JARVIS (not filtered on, D-029) |

| Criterion | Input | Score | Weight | Effective weight | Contribution |
|---|---|---|---|---|---|
| Stability | 0 eV/atom (recomputed hull (D-013)) | 1.000 | 0.35 | 0.350 | 0.350 |
| Band gap | 4.99 eV (TBmBJ) | 0.748 | 0.15 | 0.150 | 0.112 |
| Element hazard | none  (element-level flags (config/hazards.yaml)) | 1.000 | 0.20 | 0.200 | 0.200 |
| Simplicity | 3 elements (count of distinct elements) | 0.700 | 0.05 | 0.050 | 0.035 |
| Dielectric constant (κ) | 27.8  (DFPT total, max component) | 1.000 | 0.25 | 0.250 | 0.250 |
| **Total** | | | | | **0.947** |

**Confidence:** +2 band gap from TBmBJ; +2 experimental structure reference (ICSD, via JARVIS); +0 no stability cross-check (not_run: cross-check turned off); +1 all weighted criteria have values.

**Cross-check:** not_run. cross-check turned off
**Caveats:**
- Stability not cross-checked: cross-check turned off.

**Sources:**
- JARVIS-DFT dft_3d record: [JVASP-49166](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-49166.html), retrieved/checked 2026-11-17T20:56:28+00:00
- dataset (figshare): [jdft_3d-9-24-2025.json](https://doi.org/10.6084/m9.figshare.6815699), retrieved/checked 2026-11-17T20:56:28+00:00

---

## κ vs band gap (shortlist)
| Formula | Band gap (eV) | Method | κ total |
|---|---|---|---|
| NaSmO2 | 5.66 | TBmBJ | 32.8 |
| LuTaO4 | 5.36 | TBmBJ | 276.9 |
| NaPrO2 | 5.26 | TBmBJ | 31.1 |
| TeO2 | 4.64 | TBmBJ | 28.8 |
| SnB4O7 | 4.99 | TBmBJ | 27.8 |
High κ usually comes with a smaller gap; the app plots this trade-off across all candidates with DFPT κ.

## Listed for review, not ranked (16)
DFT gives these a zero gap, but they contain f-electron or open-shell 3d elements where that is often wrong (D-030). Not ranked; gap unknown. First 25:
BaYFeCuO5, Co3TeO8, Co5O8, FeSbO4, HoBi2O6, K3CrO4, Li3CrO4, Li4V3SiO10, LiCoGeO4, LiFe2P2O8, LiMn4O8, Mg2FeWO6, Mn3CoO8, NdO3, TiFeBi2O6, TiVO4

## Configuration and filters applied
- Weights: stability 0.35, band_gap 0.15, hazard 0.2, simplicity 0.05, dielectric 0.25
- Filters: min_band_gap=None, max_e_hull=None, max_elements=None, exclude_elements=[], allow_extra_anions=False
- Stability cross-check (Alexandria) enabled: False
- Config file hashes: ranking dc0c5a1dab49, candidates 39061fedf98a, hazards fdfa6b01c897, sources d662beaac648, policy 7fb95e8f8b03, confidence c6b5f9bd9548, output c55f3669d194, terminology 79179a30262d

| Filter step | Formulas |
|---|---|
| formulas | 15671 |
| dropped: contains H, C, N, S or halogen | 4156 |
| dropped: metal (no band gap) | 2119 |
| dropped: element with no stable isotopes | 506 |
| dropped: not an oxide | 1 |
| dropped: no dielectric data (criterion turned on by request) | 8430 |
| needs review (not ranked) | 16 |
| ranked | 443 |

## Snapshot manifest
- Source: JARVIS-DFT (NIST), dataset `dft_3d`, file jdft_3d-9-24-2025.json ([download](https://ndownloader.figshare.com/files/64391379))
- Raw file retrieved 2026-11-17T20:56:28+00:00, sha256 f9e0a3309f0000d5…; snapshot built 2026-11-18T22:23:34+00:00
- References: https://doi.org/10.1016/j.commatsci.2025.114063, https://doi.org/10.6084/m9.figshare.6815699
- Sanity checks: C1 pass, C2 report, C3 warn, C4 pass, C5 pass

## Caveats (always shown)
- Values are DFT calculations for perfect bulk crystals, not measurements on thin films. Many deposited films are amorphous or strained.
- DFT band gaps are approximate; the OptB88vdW fallback usually underestimates the gap.
- Energy above hull is thermodynamic stability at 0 K, recomputed from JARVIS formation energies. It says nothing about kinetics, deposition conditions or reactions with the substrate.
- Hazard flags are element-level (RoHS, IARC). They are not compound toxicology and do not assess oxidation state or exposure route.
- This is a triage shortlist to support a scientist's judgment. It is not a recommendation to run any experiment.

## Execution trace
| Step | Detail | ms |
|---|---|---|
| normalise request text | 85 characters in, 85 read; no change | 0.0 |
| policy gate | 0 refusal\(s\)\: \[\]; remainder\: 'High-k oxides for capacitors. I can accept a smaller band gap. ternaries are fine' | 0.2 |
| parse request | provider\=rules; matched\=3; unparsed\=\[\] | 0.1 |
| apply settings and clamp | weights\=\{'stability'\: 0\.35, 'band\_gap'\: 0\.15, 'hazard'\: 0\.2, 'simplicity'\: 0\.05, 'dielectric'\: 0\.25\}; clamped\=\[\] | 0.0 |
| load snapshot | 25194 records; built 2026-11-18T22\:23\:34\+00\:00 | 0.0 |
| candidates and filters | \{'formulas'\: 15671, 'dropped\: contains H, C, N, S or halogen'\: 4156, 'dropped\: metal \(no band gap\)'\: 2119, 'dropped\: element with no stable isotopes'\: 506, 'dropped\: not an oxide'\: 1, 'dropped\: no dielectric data \(criterion turned on by request\)'\: 8430, 'needs review \(not ranked\)'\: 16, 'ranked'\: 443\} | 94.3 |
| score | 443 candidates scored | 107.3 |
| rank (ties by offline confidence) | shortlist pool 5 of 443 | 2.8 |
| Alexandria cross-check | NaSmO2\:not\_run, LuTaO4\:not\_run, NaPrO2\:not\_run, TeO2\:not\_run, SnB4O7\:not\_run | 0.0 |
| confidence, caveats, citations | 5 ranked | 0.1 |
