# Oxide dielectric triage: audit view

**Request:** Find promising oxide dielectric candidates for thin-film experiments. Prefer thermodynamically stable materials, wide band gaps, non-toxic elements, simple compositions, and public evidence. Return a ranked shortlist with caveats.
**Run:** 2026-11-20T21:25:48+00:00 · parser `rules` · style `pi` · shortlist 5 · rank by `suitability`

## Refusals and notes
No part of the request was refused.

## How the request was read
- 'Find promising oxide dielectric candidates for thin-film experiments' -> scope: oxide dielectric triage (default)
- 'Find promising oxide dielectric candidates for thin-film experiments' -> thin-film context: film caveats included (always on)
- 'Prefer thermodynamically stable materials' -> stability preference (default weight)
- 'wide band gaps' -> wide band gap preference (default weight)
- 'non-toxic elements' -> hazard preference (default weight)
- 'simple compositions' -> simplicity preference (default weight)
- 'and public evidence' -> public evidence and citations (always on)
- 'Return a ranked shortlist with caveats' -> caveats (always on)
- 'Return a ranked shortlist with caveats' -> ranked shortlist (default)

## 1 (tie). Al2O3: Suitability 1.000, Evidence confidence High (5 pts)

Strongest: on the convex hull; band gap 7.57 eV (TBmBJ).

**Representative:** [JVASP-32](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-32.html) · space group R-3c · origin mp-1143 · retrieved 2026-11-17T20:56:28+00:00

| Value | Raw | Unit | Method / source |
|---|---|---|---|
| Energy above hull | 0 | meV/atom | recomputed hull from JARVIS formation energies, 9 competing compositions (D-013) |
| JARVIS `ehull` field | 1.5963 | eV/atom | not used (failed known-answer check C2, D-013) |
| Formation energy | -3.313 | eV/atom | JARVIS-DFT, OptB88vdW |
| Band gap, TBmBJ | 7.571 | eV | JARVIS-DFT |
| Band gap, OptB88vdW | 6.430 | eV | JARVIS-DFT |
| κ total (DFPT) | 11.97 | – | JARVIS-DFT, max component |
| κ electronic / ionic | 3.20 / 8.80 | – | JARVIS-DFT |
| ICSD references | 80 | – | 60419, 160901, 160902, 160903, 160904 |
| Dimensionality label | 3D-bulk | – | JARVIS (not filtered on, D-029) |

| Criterion | Input | Score | Weight | Effective weight | Contribution |
|---|---|---|---|---|---|
| Stability | 0 eV/atom (recomputed hull (D-013)) | 1.000 | 0.35 | 0.350 | 0.350 |
| Band gap | 7.57 eV (TBmBJ) | 1.000 | 0.30 | 0.300 | 0.300 |
| Element hazard | none  (element-level flags (config/hazards.yaml)) | 1.000 | 0.20 | 0.200 | 0.200 |
| Simplicity | 2 elements (count of distinct elements) | 1.000 | 0.15 | 0.150 | 0.150 |
| Dielectric constant (κ) | 12  (DFPT total, max component) | 0.379 | 0.00 | 0.000 | 0.000 |
| **Total** | | | | | **1.000** |

**Confidence:** +2 band gap from TBmBJ; +2 experimental structure reference (ICSD, via JARVIS); +0 no stability cross-check (not_run: cross-check turned off); +1 all weighted criteria have values.

**Cross-check:** not_run. cross-check turned off
**Caveats:**
- Stability not cross-checked: cross-check turned off.

**Polymorphs** (14 in JARVIS; first 5 by energy):

| JARVIS ID | Space group | Energy above hull (meV/atom) | TBmBJ gap | OptB88vdW gap | ICSD |
|---|---|---|---|---|---|
| JVASP-32 | R-3c | 0 | 7.57 | 6.43 | yes |
| JVASP-10076 | C2/m | 17 | 6.23 | 4.94 | yes |
| JVASP-49931 | C2/m | 30 | 6.34 | 4.85 | no |
| JVASP-49866 | R-3 | 81 | 7.49 | 6.19 | no |
| JVASP-50026 | P2_1/c | 85 | 6.04 | 4.62 | no |

**Sources:**
- JARVIS-DFT dft_3d record: [JVASP-32](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-32.html), retrieved/checked 2026-11-17T20:56:28+00:00
- dataset (figshare): [jdft_3d-9-24-2025.json](https://doi.org/10.6084/m9.figshare.6815699), retrieved/checked 2026-11-17T20:56:28+00:00

---
## 2 (tie). SiO2: Suitability 1.000, Evidence confidence High (5 pts)

Strongest: on the convex hull; band gap 8.10 eV (TBmBJ).

**Representative:** [JVASP-41](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-41.html) · space group P3_221 · origin mp-6930 · retrieved 2026-11-17T20:56:28+00:00

| Value | Raw | Unit | Method / source |
|---|---|---|---|
| Energy above hull | 0 | meV/atom | recomputed hull from JARVIS formation energies, 8 competing compositions (D-013) |
| JARVIS `ehull` field | 1.3850 | eV/atom | not used (failed known-answer check C2, D-013) |
| Formation energy | -2.901 | eV/atom | JARVIS-DFT, OptB88vdW |
| Band gap, TBmBJ | 8.097 | eV | JARVIS-DFT |
| Band gap, OptB88vdW | 5.986 | eV | JARVIS-DFT |
| κ total (DFPT) | 4.88 | – | JARVIS-DFT, max component |
| κ electronic / ionic | 2.51 / 2.37 | – | JARVIS-DFT |
| ICSD references | 91 | – | 41472, 41473, 41474, 41475, 41476 |
| Dimensionality label | 3D-bulk | – | JARVIS (not filtered on, D-029) |

| Criterion | Input | Score | Weight | Effective weight | Contribution |
|---|---|---|---|---|---|
| Stability | 0 eV/atom (recomputed hull (D-013)) | 1.000 | 0.35 | 0.350 | 0.350 |
| Band gap | 8.1 eV (TBmBJ) | 1.000 | 0.30 | 0.300 | 0.300 |
| Element hazard | none  (element-level flags (config/hazards.yaml)) | 1.000 | 0.20 | 0.200 | 0.200 |
| Simplicity | 2 elements (count of distinct elements) | 1.000 | 0.15 | 0.150 | 0.150 |
| Dielectric constant (κ) | 4.88  (DFPT total, max component) | 0.042 | 0.00 | 0.000 | 0.000 |
| **Total** | | | | | **1.000** |

**Confidence:** +2 band gap from TBmBJ; +2 experimental structure reference (ICSD, via JARVIS); +0 no stability cross-check (not_run: cross-check turned off); +1 all weighted criteria have values.

**Cross-check:** not_run. cross-check turned off
**Caveats:**
- Compound-form hazard not captured by element flags: IARC 'Silica dust, crystalline, in the form of quartz or cristobalite'. Group 1 as respirable crystalline dust. Si is not flagged at element level.
- Stability not cross-checked: cross-check turned off.

**Polymorphs** (94 in JARVIS; first 5 by energy):

| JARVIS ID | Space group | Energy above hull (meV/atom) | TBmBJ gap | OptB88vdW gap | ICSD |
|---|---|---|---|---|---|
| JVASP-41 | P3_221 | 0 | 8.10 | 5.99 | yes |
| JVASP-58349 | P3_121 | 0 | 8.10 | 5.99 | yes |
| JVASP-34219 | P3_221 | 0 | 8.10 | 5.99 | yes |
| JVASP-91213 | C2/c | 2 | missing | 6.01 | yes |
| JVASP-164673 | P2_1/c | 9 | missing | 5.63 | yes |

**Sources:**
- JARVIS-DFT dft_3d record: [JVASP-41](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-41.html), retrieved/checked 2026-11-17T20:56:28+00:00
- dataset (figshare): [jdft_3d-9-24-2025.json](https://doi.org/10.6084/m9.figshare.6815699), retrieved/checked 2026-11-17T20:56:28+00:00

---
## 3 (tie). Li2O: Suitability 1.000, Evidence confidence Medium (3 pts)

Strongest: on the convex hull; band gap 7.59 eV (TBmBJ).

**Representative:** [JVASP-118614](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-118614.html) · space group C2/m · origin JQE-571885 · retrieved 2026-11-17T20:56:28+00:00

| Value | Raw | Unit | Method / source |
|---|---|---|---|
| Energy above hull | 0 | meV/atom | recomputed hull from JARVIS formation energies, 6 competing compositions (D-013) |
| JARVIS `ehull` field | 0.4279 | eV/atom | not used (failed known-answer check C2, D-013) |
| Formation energy | -2.088 | eV/atom | JARVIS-DFT, OptB88vdW |
| Band gap, TBmBJ | 7.590 | eV | JARVIS-DFT |
| Band gap, OptB88vdW | 5.255 | eV | JARVIS-DFT |
| κ total (DFPT) | missing | – | JARVIS-DFT, max component |
| κ electronic / ionic | missing / missing | – | JARVIS-DFT |
| ICSD references | 0 | – | none |
| Dimensionality label | intercalated ion | – | JARVIS (not filtered on, D-029) |

| Criterion | Input | Score | Weight | Effective weight | Contribution |
|---|---|---|---|---|---|
| Stability | 0 eV/atom (recomputed hull (D-013)) | 1.000 | 0.35 | 0.350 | 0.350 |
| Band gap | 7.59 eV (TBmBJ) | 1.000 | 0.30 | 0.300 | 0.300 |
| Element hazard | none  (element-level flags (config/hazards.yaml)) | 1.000 | 0.20 | 0.200 | 0.200 |
| Simplicity | 2 elements (count of distinct elements) | 1.000 | 0.15 | 0.150 | 0.150 |
| Dielectric constant (κ) | missing | missing | 0.00 | 0.000 | 0.000 |
| **Total** | | | | | **1.000** |

**Confidence:** +2 band gap from TBmBJ; +0 no ICSD reference found; +0 no stability cross-check (not_run: cross-check turned off); +1 all weighted criteria have values.

**Cross-check:** not_run. cross-check turned off
**Caveats:**
- No ICSD experimental structure reference found for this polymorph.
- Stability not cross-checked: cross-check turned off.

**Polymorphs** (6 in JARVIS; first 5 by energy):

| JARVIS ID | Space group | Energy above hull (meV/atom) | TBmBJ gap | OptB88vdW gap | ICSD |
|---|---|---|---|---|---|
| JVASP-118614 | C2/m | 0 | 7.59 | 5.25 | no |
| JVASP-1360 | Fm-3m | 40 | 5.92 | 5.45 | yes |
| JVASP-50312 | Pnma | 125 | missing | 5.99 | no |
| JVASP-118616 | Cmmm | 519 | 4.84 | 2.99 | no |
| JVASP-118617 | Pmmm | 680 | missing | 0.06 | no |

**Sources:**
- JARVIS-DFT dft_3d record: [JVASP-118614](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-118614.html), retrieved/checked 2026-11-17T20:56:28+00:00
- dataset (figshare): [jdft_3d-9-24-2025.json](https://doi.org/10.6084/m9.figshare.6815699), retrieved/checked 2026-11-17T20:56:28+00:00

---
## 4 (tie). B2O3: Suitability 1.000, Evidence confidence Low (1 pts)

Strongest: on the convex hull; band gap 6.54 eV (OptB88vdW).

**Representative:** [JVASP-152827](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-152827.html) · space group P3_121 · origin auid-56800889451c7945 · retrieved 2026-11-17T20:56:28+00:00

| Value | Raw | Unit | Method / source |
|---|---|---|---|
| Energy above hull | 0 | meV/atom | recomputed hull from JARVIS formation energies, 10 competing compositions (D-013) |
| JARVIS `ehull` field | 2.9392 | eV/atom | not used (failed known-answer check C2, D-013) |
| Formation energy | -2.537 | eV/atom | JARVIS-DFT, OptB88vdW |
| Band gap, TBmBJ | missing | eV | JARVIS-DFT |
| Band gap, OptB88vdW | 6.540 | eV | JARVIS-DFT (used as fallback) |
| κ total (DFPT) | missing | – | JARVIS-DFT, max component |
| κ electronic / ionic | missing / missing | – | JARVIS-DFT |
| ICSD references | 0 | – | none |
| Dimensionality label | 3D-bulk | – | JARVIS (not filtered on, D-029) |

| Criterion | Input | Score | Weight | Effective weight | Contribution |
|---|---|---|---|---|---|
| Stability | 0 eV/atom (recomputed hull (D-013)) | 1.000 | 0.35 | 0.350 | 0.350 |
| Band gap | 6.54 eV (OptB88vdW) | 1.000 | 0.30 | 0.300 | 0.300 |
| Element hazard | none  (element-level flags (config/hazards.yaml)) | 1.000 | 0.20 | 0.200 | 0.200 |
| Simplicity | 2 elements (count of distinct elements) | 1.000 | 0.15 | 0.150 | 0.150 |
| Dielectric constant (κ) | missing | missing | 0.00 | 0.000 | 0.000 |
| **Total** | | | | | **1.000** |

**Confidence:** +0 band gap from OptB88vdW fallback (probable underestimate); +0 no ICSD reference found; +0 no stability cross-check (not_run: cross-check turned off); +1 all weighted criteria have values.

**Cross-check:** not_run. cross-check turned off
**Caveats:**
- Band gap is the OptB88vdW fallback (no TBmBJ value): probably an underestimate.
- Representative JVASP-152827 (P3_121) has no ICSD reference; JVASP-14147 (P3_121) is 5 meV/atom higher and has one.
- No ICSD experimental structure reference found for this polymorph.
- Stability not cross-checked: cross-check turned off.

**Polymorphs** (7 in JARVIS; first 5 by energy):

| JARVIS ID | Space group | Energy above hull (meV/atom) | TBmBJ gap | OptB88vdW gap | ICSD |
|---|---|---|---|---|---|
| JVASP-152827 | P3_121 | 0 | missing | 6.54 | no |
| JVASP-154389 | P3_121 | 0 | missing | 6.54 | no |
| JVASP-14147 | P3_121 | 5 | 9.19 | 6.54 | yes |
| JVASP-62678 | P3_121 | 5 | 9.19 | 6.54 | no |
| JVASP-63235 | P3_121 | 5 | 9.19 | 6.54 | no |

**Sources:**
- JARVIS-DFT dft_3d record: [JVASP-152827](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-152827.html), retrieved/checked 2026-11-17T20:56:28+00:00
- dataset (figshare): [jdft_3d-9-24-2025.json](https://doi.org/10.6084/m9.figshare.6815699), retrieved/checked 2026-11-17T20:56:28+00:00

---
## 5. YbO: Suitability 0.985, Evidence confidence High (4 pts)

Strongest: on the convex hull; band gap 5.80 eV (TBmBJ).

**Representative:** [JVASP-1291](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-1291.html) · space group Fm-3m · origin mp-1216 · retrieved 2026-11-17T20:56:28+00:00

| Value | Raw | Unit | Method / source |
|---|---|---|---|
| Energy above hull | 0 | meV/atom | recomputed hull from JARVIS formation energies, 5 competing compositions (D-013) |
| JARVIS `ehull` field | 0.0000 | eV/atom | not used (failed known-answer check C2, D-013) |
| Formation energy | -3.614 | eV/atom | JARVIS-DFT, OptB88vdW |
| Band gap, TBmBJ | 5.803 | eV | JARVIS-DFT |
| Band gap, OptB88vdW | 3.581 | eV | JARVIS-DFT |
| κ total (DFPT) | 15.60 | – | JARVIS-DFT, max component |
| κ electronic / ionic | 3.86 / 11.74 | – | JARVIS-DFT |
| ICSD references | 2 | – | 151764, 77710 |
| Dimensionality label | 3D-bulk | – | JARVIS (not filtered on, D-029) |

| Criterion | Input | Score | Weight | Effective weight | Contribution |
|---|---|---|---|---|---|
| Stability | 0 eV/atom (recomputed hull (D-013)) | 1.000 | 0.35 | 0.350 | 0.350 |
| Band gap | 5.8 eV (TBmBJ) | 0.951 | 0.30 | 0.300 | 0.285 |
| Element hazard | none  (element-level flags (config/hazards.yaml)) | 1.000 | 0.20 | 0.200 | 0.200 |
| Simplicity | 2 elements (count of distinct elements) | 1.000 | 0.15 | 0.150 | 0.150 |
| Dielectric constant (κ) | 15.6  (DFPT total, max component) | 0.552 | 0.00 | 0.000 | 0.000 |
| **Total** | | | | | **0.985** |

**Confidence:** +2 band gap from TBmBJ; +2 experimental structure reference (ICSD, via JARVIS); +0 no stability cross-check (not_run: cross-check turned off); +1 all weighted criteria have values; -1 contains Yb: DFT energies and gaps less reliable.

**Cross-check:** not_run. cross-check turned off
**Caveats:**
- Contains Yb: DFT energies and gaps are less reliable for these elements, so stability and gap may be wrong.
- Stability not cross-checked: cross-check turned off.

**Sources:**
- JARVIS-DFT dft_3d record: [JVASP-1291](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-1291.html), retrieved/checked 2026-11-17T20:56:28+00:00
- dataset (figshare): [jdft_3d-9-24-2025.json](https://doi.org/10.6084/m9.figshare.6815699), retrieved/checked 2026-11-17T20:56:28+00:00

---

## κ vs band gap (shortlist)
| Formula | Band gap (eV) | Method | κ total |
|---|---|---|---|
| Al2O3 | 7.57 | TBmBJ | 12.0 |
| SiO2 | 8.10 | TBmBJ | 4.9 |
| Li2O | 7.59 | TBmBJ | missing |
| B2O3 | 6.54 | OptB88vdW | missing |
| YbO | 5.80 | TBmBJ | 15.6 |
High κ usually comes with a smaller gap; the app plots this trade-off across all candidates with DFPT κ.

## Listed for review, not ranked (3520)
DFT gives these a zero gap, but they contain f-electron or open-shell 3d elements where that is often wrong (D-030). Not ranked; gap unknown. First 25:
Al2Co3GeO8, Al2Cr2O7, Al2CrO5, Al2CuO4, Al2Fe2O7, Al2FeO4, Al3Cr3Sb2O16, Al4Cu2O7, AlCoO, AlCoO2, AlCr2O4, AlCr3O8, AlCr4Cu3O12, AlCrFeO4, AlCrW2O8, AlCu2O4, AlCu7O12, AlCuO, AlFe2O4, AlFe4Cu3O12, AlFeO, AlFeO2, AlFeO4, AlInCuO4, AlNi2O4

## Configuration and filters applied
- Weights: stability 0.35, band_gap 0.3, hazard 0.2, simplicity 0.15, dielectric 0.0
- Filters: min_band_gap=None, max_e_hull=None, max_elements=None, exclude_elements=[], allow_extra_anions=False
- Stability cross-check (Alexandria) enabled: False
- Config file hashes: ranking dc0c5a1dab49, candidates 39061fedf98a, hazards fdfa6b01c897, sources d662beaac648, policy 89afc674c1f7, confidence c6b5f9bd9548, output c55f3669d194, terminology 79179a30262d

| Filter step | Formulas |
|---|---|
| formulas | 15671 |
| dropped: contains H, C, N, S or halogen | 4156 |
| dropped: metal (no band gap) | 2119 |
| dropped: element with no stable isotopes | 506 |
| dropped: not an oxide | 1 |
| needs review (not ranked) | 3520 |
| ranked | 5369 |

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
| policy gate | 0 refusal(s): []; remainder: 'Find promising oxide dielectric candidates for thin-film experiments. Prefer thermodynamically stable materials. wide band gaps. non-toxic elements. simple compositions. and public evidence. Return a ranked shortlist with caveats' | 2.3 |
| parse request | provider=rules; matched=9; unparsed=[] | 2.5 |
| apply settings and clamp | weights={'stability': 0.35, 'band_gap': 0.3, 'hazard': 0.2, 'simplicity': 0.15, 'dielectric': 0.0}; clamped=[] | 0.1 |
| load snapshot | 25194 records; built 2026-11-18T22:23:34+00:00 | 526.5 |
| candidates and filters | {'formulas': 15671, 'dropped: contains H, C, N, S or halogen': 4156, 'dropped: metal (no band gap)': 2119, 'dropped: element with no stable isotopes': 506, 'dropped: not an oxide': 1, 'needs review (not ranked)': 3520, 'ranked': 5369} | 170.4 |
| score | 5369 candidates scored | 357.1 |
| rank (ties by offline confidence) | shortlist pool 5 of 5369 | 41.5 |
| Alexandria cross-check | Al2O3:not_run, SiO2:not_run, Li2O:not_run, B2O3:not_run, YbO:not_run | 0.0 |
| confidence, caveats, citations | 5 ranked | 0.2 |
