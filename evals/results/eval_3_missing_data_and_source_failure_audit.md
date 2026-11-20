# Oxide dielectric triage: audit view

**Request:** oxides, binaries only, top 25
**Run:** 2026-11-20T22:03:52+00:00 · parser `rules` · style `audit` · shortlist 25 · rank by `suitability`

## Refusals and notes
No part of the request was refused.
- Alexandria cross-check failed: Alexandria unreachable (ConnectionError). Affected candidates are marked; no Alexandria values shown.

## How the request was read
- 'binaries only' -\> filter\: binary compounds only
- 'top 25' -\> shortlist size 25
Not understood (ignored): "oxides"

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

**Confidence:** +2 band gap from TBmBJ; +2 experimental structure reference (ICSD, via JARVIS); +0 no stability cross-check (unavailable: Alexandria unreachable (ConnectionError)); +1 all weighted criteria have values.

**Cross-check (Alexandria):** unavailable. Alexandria unreachable (ConnectionError)
**Caveats:**
- Stability not cross-checked: Alexandria unreachable (ConnectionError).

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

**Confidence:** +2 band gap from TBmBJ; +2 experimental structure reference (ICSD, via JARVIS); +0 no stability cross-check (unavailable: skipped after earlier failure: Alexandria unreachable (ConnectionError)); +1 all weighted criteria have values.

**Cross-check (Alexandria):** unavailable. skipped after earlier failure: Alexandria unreachable (ConnectionError)
**Caveats:**
- Compound-form hazard not captured by element flags: IARC 'Silica dust, crystalline, in the form of quartz or cristobalite'. Group 1 as respirable crystalline dust. Si is not flagged at element level.
- Stability not cross-checked: skipped after earlier failure: Alexandria unreachable (ConnectionError).

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

**Confidence:** +2 band gap from TBmBJ; +0 no ICSD reference found; +0 no stability cross-check (unavailable: skipped after earlier failure: Alexandria unreachable (ConnectionError)); +1 all weighted criteria have values.

**Cross-check (Alexandria):** unavailable. skipped after earlier failure: Alexandria unreachable (ConnectionError)
**Caveats:**
- No ICSD experimental structure reference found for this polymorph.
- Stability not cross-checked: skipped after earlier failure: Alexandria unreachable (ConnectionError).

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

**Confidence:** +0 band gap from OptB88vdW fallback (probable underestimate); +0 no ICSD reference found; +0 no stability cross-check (unavailable: skipped after earlier failure: Alexandria unreachable (ConnectionError)); +1 all weighted criteria have values.

**Cross-check (Alexandria):** unavailable. skipped after earlier failure: Alexandria unreachable (ConnectionError)
**Caveats:**
- Band gap is the OptB88vdW fallback (no TBmBJ value): probably an underestimate.
- Representative JVASP-152827 (P3_121) has no ICSD reference; JVASP-14147 (P3_121) is 5 meV/atom higher and has one.
- No ICSD experimental structure reference found for this polymorph.
- Stability not cross-checked: skipped after earlier failure: Alexandria unreachable (ConnectionError).

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

**Confidence:** +2 band gap from TBmBJ; +2 experimental structure reference (ICSD, via JARVIS); +0 no stability cross-check (unavailable: skipped after earlier failure: Alexandria unreachable (ConnectionError)); +1 all weighted criteria have values; -1 contains Yb: DFT energies and gaps less reliable.

**Cross-check (Alexandria):** unavailable. skipped after earlier failure: Alexandria unreachable (ConnectionError)
**Caveats:**
- Contains Yb: DFT energies and gaps are less reliable for these elements, so stability and gap may be wrong.
- Stability not cross-checked: skipped after earlier failure: Alexandria unreachable (ConnectionError).

**Sources:**
- JARVIS-DFT dft_3d record: [JVASP-1291](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-1291.html), retrieved/checked 2026-11-17T20:56:28+00:00
- dataset (figshare): [jdft_3d-9-24-2025.json](https://doi.org/10.6084/m9.figshare.6815699), retrieved/checked 2026-11-17T20:56:28+00:00

---
## 6. HfO2: Suitability 0.975, Evidence confidence High (5 pts)

Strongest: on the convex hull; band gap 5.66 eV (TBmBJ).

**Representative:** [JVASP-9147](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-9147.html) · space group P2_1/c · origin mp-352 · retrieved 2026-11-17T20:56:28+00:00

| Value | Raw | Unit | Method / source |
|---|---|---|---|
| Energy above hull | 0 | meV/atom | recomputed hull from JARVIS formation energies, 8 competing compositions (D-013) |
| JARVIS `ehull` field | 1.7776 | eV/atom | not used (failed known-answer check C2, D-013) |
| Formation energy | -3.810 | eV/atom | JARVIS-DFT, OptB88vdW |
| Band gap, TBmBJ | 5.664 | eV | JARVIS-DFT |
| Band gap, OptB88vdW | 4.123 | eV | JARVIS-DFT |
| κ total (DFPT) | missing | – | JARVIS-DFT, max component |
| κ electronic / ionic | missing / missing | – | JARVIS-DFT |
| ICSD references | 7 | – | 172165, 173158, 60903, 57385, 173964 |
| Dimensionality label | 3D-bulk | – | JARVIS (not filtered on, D-029) |

| Criterion | Input | Score | Weight | Effective weight | Contribution |
|---|---|---|---|---|---|
| Stability | 0 eV/atom (recomputed hull (D-013)) | 1.000 | 0.35 | 0.350 | 0.350 |
| Band gap | 5.66 eV (TBmBJ) | 0.916 | 0.30 | 0.300 | 0.275 |
| Element hazard | none  (element-level flags (config/hazards.yaml)) | 1.000 | 0.20 | 0.200 | 0.200 |
| Simplicity | 2 elements (count of distinct elements) | 1.000 | 0.15 | 0.150 | 0.150 |
| Dielectric constant (κ) | missing | missing | 0.00 | 0.000 | 0.000 |
| **Total** | | | | | **0.975** |

**Confidence:** +2 band gap from TBmBJ; +2 experimental structure reference (ICSD, via JARVIS); +0 no stability cross-check (unavailable: skipped after earlier failure: Alexandria unreachable (ConnectionError)); +1 all weighted criteria have values.

**Cross-check (Alexandria):** unavailable. skipped after earlier failure: Alexandria unreachable (ConnectionError)
**Caveats:**
- Stability not cross-checked: skipped after earlier failure: Alexandria unreachable (ConnectionError).

**Polymorphs** (13 in JARVIS; first 5 by energy):

| JARVIS ID | Space group | Energy above hull (meV/atom) | TBmBJ gap | OptB88vdW gap | ICSD |
|---|---|---|---|---|---|
| JVASP-9147 | P2_1/c | 0 | 5.66 | 4.12 | yes |
| JVASP-43367 | Pbca | 10 | 5.60 | 4.03 | no |
| JVASP-18984 | Pbca | 12 | 5.90 | 4.32 | yes |
| JVASP-52653 | Pca2_1 | 18 | 6.01 | 4.44 | no |
| JVASP-43519 | P4_2/mnm | 39 | 5.58 | 3.95 | no |

**Sources:**
- JARVIS-DFT dft_3d record: [JVASP-9147](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-9147.html), retrieved/checked 2026-11-17T20:56:28+00:00
- dataset (figshare): [jdft_3d-9-24-2025.json](https://doi.org/10.6084/m9.figshare.6815699), retrieved/checked 2026-11-17T20:56:28+00:00

---
## 7. P2O5: Suitability 0.955, Evidence confidence Medium (3 pts)

Strongest: on the convex hull; band gap 5.40 eV (OptB88vdW).

**Representative:** [JVASP-60626](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-60626.html) · space group Pnma · origin mp-2173 · retrieved 2026-11-17T20:56:28+00:00

| Value | Raw | Unit | Method / source |
|---|---|---|---|
| Energy above hull | 0 | meV/atom | recomputed hull from JARVIS formation energies, 7 competing compositions (D-013) |
| JARVIS `ehull` field | 2.6475 | eV/atom | not used (failed known-answer check C2, D-013) |
| Formation energy | -2.006 | eV/atom | JARVIS-DFT, OptB88vdW |
| Band gap, TBmBJ | missing | eV | JARVIS-DFT |
| Band gap, OptB88vdW | 5.397 | eV | JARVIS-DFT (used as fallback) |
| κ total (DFPT) | missing | – | JARVIS-DFT, max component |
| κ electronic / ionic | missing / missing | – | JARVIS-DFT |
| ICSD references | 4 | – | 654026, 79698, 16611, 29045 |
| Dimensionality label | 2D-bulk | – | JARVIS (not filtered on, D-029) |

| Criterion | Input | Score | Weight | Effective weight | Contribution |
|---|---|---|---|---|---|
| Stability | 0 eV/atom (recomputed hull (D-013)) | 1.000 | 0.35 | 0.350 | 0.350 |
| Band gap | 5.4 eV (OptB88vdW) | 0.849 | 0.30 | 0.300 | 0.255 |
| Element hazard | none  (element-level flags (config/hazards.yaml)) | 1.000 | 0.20 | 0.200 | 0.200 |
| Simplicity | 2 elements (count of distinct elements) | 1.000 | 0.15 | 0.150 | 0.150 |
| Dielectric constant (κ) | missing | missing | 0.00 | 0.000 | 0.000 |
| **Total** | | | | | **0.955** |

**Confidence:** +0 band gap from OptB88vdW fallback (probable underestimate); +2 experimental structure reference (ICSD, via JARVIS); +0 no stability cross-check (unavailable: skipped after earlier failure: Alexandria unreachable (ConnectionError)); +1 all weighted criteria have values.

**Cross-check (Alexandria):** unavailable. skipped after earlier failure: Alexandria unreachable (ConnectionError)
**Caveats:**
- Band gap is the OptB88vdW fallback (no TBmBJ value): probably an underestimate.
- Stability not cross-checked: skipped after earlier failure: Alexandria unreachable (ConnectionError).

**Polymorphs** (4 in JARVIS; first 5 by energy):

| JARVIS ID | Space group | Energy above hull (meV/atom) | TBmBJ gap | OptB88vdW gap | ICSD |
|---|---|---|---|---|---|
| JVASP-60626 | Pnma | 0 | missing | 5.40 | yes |
| JVASP-20766 | Fdd2 | 12 | missing | 5.60 | yes |
| JVASP-164385 | R3c | 44 | missing | 5.49 | yes |
| JVASP-36714 | Pmmm | 629 | missing | 0.00 | no |

**Sources:**
- JARVIS-DFT dft_3d record: [JVASP-60626](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-60626.html), retrieved/checked 2026-11-17T20:56:28+00:00
- dataset (figshare): [jdft_3d-9-24-2025.json](https://doi.org/10.6084/m9.figshare.6815699), retrieved/checked 2026-11-17T20:56:28+00:00

---
## 8. Nd2O3: Suitability 0.948, Evidence confidence High (4 pts)

Strongest: on the convex hull; band gap 5.32 eV (TBmBJ).

**Representative:** [JVASP-8020](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-8020.html) · space group P-3m1 · origin mp-2763 · retrieved 2026-11-17T20:56:28+00:00

| Value | Raw | Unit | Method / source |
|---|---|---|---|
| Energy above hull | 0 | meV/atom | recomputed hull from JARVIS formation energies, 6 competing compositions (D-013) |
| JARVIS `ehull` field | 1.6286 | eV/atom | not used (failed known-answer check C2, D-013) |
| Formation energy | -3.584 | eV/atom | JARVIS-DFT, OptB88vdW |
| Band gap, TBmBJ | 5.315 | eV | JARVIS-DFT |
| Band gap, OptB88vdW | 3.960 | eV | JARVIS-DFT |
| κ total (DFPT) | 21.38 | – | JARVIS-DFT, max component |
| κ electronic / ionic | 4.70 / 16.68 | – | JARVIS-DFT |
| ICSD references | 6 | – | 32514, 96199, 169442, 160208, 28180 |
| Dimensionality label | 3D-bulk | – | JARVIS (not filtered on, D-029) |

| Criterion | Input | Score | Weight | Effective weight | Contribution |
|---|---|---|---|---|---|
| Stability | 0.00018 eV/atom (recomputed hull (D-013)) | 0.999 | 0.35 | 0.350 | 0.349 |
| Band gap | 5.32 eV (TBmBJ) | 0.829 | 0.30 | 0.300 | 0.249 |
| Element hazard | none  (element-level flags (config/hazards.yaml)) | 1.000 | 0.20 | 0.200 | 0.200 |
| Simplicity | 2 elements (count of distinct elements) | 1.000 | 0.15 | 0.150 | 0.150 |
| Dielectric constant (κ) | 21.4  (DFPT total, max component) | 0.827 | 0.00 | 0.000 | 0.000 |
| **Total** | | | | | **0.948** |

**Confidence:** +2 band gap from TBmBJ; +2 experimental structure reference (ICSD, via JARVIS); +0 no stability cross-check (unavailable: skipped after earlier failure: Alexandria unreachable (ConnectionError)); +1 all weighted criteria have values; -1 contains Nd: DFT energies and gaps less reliable.

**Cross-check (Alexandria):** unavailable. skipped after earlier failure: Alexandria unreachable (ConnectionError)
**Caveats:**
- Contains Nd: DFT energies and gaps are less reliable for these elements, so stability and gap may be wrong.
- Stability not cross-checked: skipped after earlier failure: Alexandria unreachable (ConnectionError).

**Polymorphs** (5 in JARVIS; first 5 by energy):

| JARVIS ID | Space group | Energy above hull (meV/atom) | TBmBJ gap | OptB88vdW gap | ICSD |
|---|---|---|---|---|---|
| JVASP-8020 | P-3m1 | 0 | 5.32 | 3.96 | yes |
| JVASP-20113 | Ia-3 | 0 | missing | 3.84 | yes |
| JVASP-34661 | C2/m | 2 | missing | 3.77 | yes |
| JVASP-13971 | P6/mmm | 270 | 3.14 | 1.58 | yes |
| JVASP-8766 | Pm-3m | 929 | 1.41 | 0.92 | no |

**Sources:**
- JARVIS-DFT dft_3d record: [JVASP-8020](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-8020.html), retrieved/checked 2026-11-17T20:56:28+00:00
- dataset (figshare): [jdft_3d-9-24-2025.json](https://doi.org/10.6084/m9.figshare.6815699), retrieved/checked 2026-11-17T20:56:28+00:00

---
## 9. CaO: Suitability 0.947, Evidence confidence High (5 pts)

Strongest: on the convex hull; band gap 5.29 eV (TBmBJ).

**Representative:** [JVASP-1405](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-1405.html) · space group Fm-3m · origin mp-2605 · retrieved 2026-11-17T20:56:28+00:00

| Value | Raw | Unit | Method / source |
|---|---|---|---|
| Energy above hull | 0 | meV/atom | recomputed hull from JARVIS formation energies, 8 competing compositions (D-013) |
| JARVIS `ehull` field | 0.0000 | eV/atom | not used (failed known-answer check C2, D-013) |
| Formation energy | -3.273 | eV/atom | JARVIS-DFT, OptB88vdW |
| Band gap, TBmBJ | 5.290 | eV | JARVIS-DFT |
| Band gap, OptB88vdW | 3.742 | eV | JARVIS-DFT |
| κ total (DFPT) | 14.85 | – | JARVIS-DFT, max component |
| κ electronic / ionic | 3.75 / 11.10 | – | JARVIS-DFT |
| ICSD references | 13 | – | 60704, 619461, 180198, 60199, 28905 |
| Dimensionality label | intercalated ion | – | JARVIS (not filtered on, D-029) |

| Criterion | Input | Score | Weight | Effective weight | Contribution |
|---|---|---|---|---|---|
| Stability | 0 eV/atom (recomputed hull (D-013)) | 1.000 | 0.35 | 0.350 | 0.350 |
| Band gap | 5.29 eV (TBmBJ) | 0.823 | 0.30 | 0.300 | 0.247 |
| Element hazard | none  (element-level flags (config/hazards.yaml)) | 1.000 | 0.20 | 0.200 | 0.200 |
| Simplicity | 2 elements (count of distinct elements) | 1.000 | 0.15 | 0.150 | 0.150 |
| Dielectric constant (κ) | 14.9  (DFPT total, max component) | 0.517 | 0.00 | 0.000 | 0.000 |
| **Total** | | | | | **0.947** |

**Confidence:** +2 band gap from TBmBJ; +2 experimental structure reference (ICSD, via JARVIS); +0 no stability cross-check (unavailable: skipped after earlier failure: Alexandria unreachable (ConnectionError)); +1 all weighted criteria have values.

**Cross-check (Alexandria):** unavailable. skipped after earlier failure: Alexandria unreachable (ConnectionError)
**Caveats:**
- Stability not cross-checked: skipped after earlier failure: Alexandria unreachable (ConnectionError).

**Polymorphs** (6 in JARVIS; first 5 by energy):

| JARVIS ID | Space group | Energy above hull (meV/atom) | TBmBJ gap | OptB88vdW gap | ICSD |
|---|---|---|---|---|---|
| JVASP-1405 | Fm-3m | 0 | 5.29 | 3.74 | yes |
| JVASP-91565 | I4/mmm | 12 | 5.21 | 3.65 | no |
| JVASP-114728 | P6_3/mmc | 90 | 5.30 | 3.17 | no |
| JVASP-79248 | P6_3/mmc | 110 | 5.68 | 3.36 | yes |
| JVASP-79526 | I4/mmm | 276 | 5.01 | 2.01 | no |

**Sources:**
- JARVIS-DFT dft_3d record: [JVASP-1405](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-1405.html), retrieved/checked 2026-11-17T20:56:28+00:00
- dataset (figshare): [jdft_3d-9-24-2025.json](https://doi.org/10.6084/m9.figshare.6815699), retrieved/checked 2026-11-17T20:56:28+00:00

---
## 10. Pr2O3: Suitability 0.941, Evidence confidence High (4 pts)

Strongest: on the convex hull; band gap 5.21 eV (TBmBJ).

**Representative:** [JVASP-7982](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-7982.html) · space group P-3m1 · origin mp-2063 · retrieved 2026-11-17T20:56:28+00:00

| Value | Raw | Unit | Method / source |
|---|---|---|---|
| Energy above hull | 0 | meV/atom | recomputed hull from JARVIS formation energies, 7 competing compositions (D-013) |
| JARVIS `ehull` field | 1.6339 | eV/atom | not used (failed known-answer check C2, D-013) |
| Formation energy | -3.539 | eV/atom | JARVIS-DFT, OptB88vdW |
| Band gap, TBmBJ | 5.214 | eV | JARVIS-DFT |
| Band gap, OptB88vdW | 3.895 | eV | JARVIS-DFT |
| κ total (DFPT) | 21.64 | – | JARVIS-DFT, max component |
| κ electronic / ionic | 4.72 / 16.92 | – | JARVIS-DFT |
| ICSD references | 5 | – | 75481, 61179, 154588, 96198, 160207 |
| Dimensionality label | 3D-bulk | – | JARVIS (not filtered on, D-029) |

| Criterion | Input | Score | Weight | Effective weight | Contribution |
|---|---|---|---|---|---|
| Stability | 0 eV/atom (recomputed hull (D-013)) | 1.000 | 0.35 | 0.350 | 0.350 |
| Band gap | 5.21 eV (TBmBJ) | 0.804 | 0.30 | 0.300 | 0.241 |
| Element hazard | none  (element-level flags (config/hazards.yaml)) | 1.000 | 0.20 | 0.200 | 0.200 |
| Simplicity | 2 elements (count of distinct elements) | 1.000 | 0.15 | 0.150 | 0.150 |
| Dielectric constant (κ) | 21.6  (DFPT total, max component) | 0.840 | 0.00 | 0.000 | 0.000 |
| **Total** | | | | | **0.941** |

**Confidence:** +2 band gap from TBmBJ; +2 experimental structure reference (ICSD, via JARVIS); +0 no stability cross-check (unavailable: skipped after earlier failure: Alexandria unreachable (ConnectionError)); +1 all weighted criteria have values; -1 contains Pr: DFT energies and gaps less reliable.

**Cross-check (Alexandria):** unavailable. skipped after earlier failure: Alexandria unreachable (ConnectionError)
**Caveats:**
- Contains Pr: DFT energies and gaps are less reliable for these elements, so stability and gap may be wrong.
- Stability not cross-checked: skipped after earlier failure: Alexandria unreachable (ConnectionError).

**Polymorphs** (3 in JARVIS; first 5 by energy):

| JARVIS ID | Space group | Energy above hull (meV/atom) | TBmBJ gap | OptB88vdW gap | ICSD |
|---|---|---|---|---|---|
| JVASP-7982 | P-3m1 | 0 | 5.21 | 3.90 | yes |
| JVASP-34449 | C2/m | 4 | missing | 3.69 | yes |
| JVASP-22772 | Ia-3 | 5 | missing | 3.79 | yes |

**Sources:**
- JARVIS-DFT dft_3d record: [JVASP-7982](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-7982.html), retrieved/checked 2026-11-17T20:56:28+00:00
- dataset (figshare): [jdft_3d-9-24-2025.json](https://doi.org/10.6084/m9.figshare.6815699), retrieved/checked 2026-11-17T20:56:28+00:00

---
## 11. SrO: Suitability 0.922, Evidence confidence High (5 pts)

Strongest: on the convex hull; band gap 4.96 eV (TBmBJ).

**Representative:** [JVASP-1390](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-1390.html) · space group Fm-3m · origin mp-2472 · retrieved 2026-11-17T20:56:28+00:00

| Value | Raw | Unit | Method / source |
|---|---|---|---|
| Energy above hull | 0 | meV/atom | recomputed hull from JARVIS formation energies, 8 competing compositions (D-013) |
| JARVIS `ehull` field | 0.0000 | eV/atom | not used (failed known-answer check C2, D-013) |
| Formation energy | -3.026 | eV/atom | JARVIS-DFT, OptB88vdW |
| Band gap, TBmBJ | 4.958 | eV | JARVIS-DFT |
| Band gap, OptB88vdW | 3.405 | eV | JARVIS-DFT |
| κ total (DFPT) | 17.53 | – | JARVIS-DFT, max component |
| κ electronic / ionic | 3.78 / 13.76 | – | JARVIS-DFT |
| ICSD references | 10 | – | 180194, 181061, 28904, 163625, 105548 |
| Dimensionality label | intercalated ion | – | JARVIS (not filtered on, D-029) |

| Criterion | Input | Score | Weight | Effective weight | Contribution |
|---|---|---|---|---|---|
| Stability | 0 eV/atom (recomputed hull (D-013)) | 1.000 | 0.35 | 0.350 | 0.350 |
| Band gap | 4.96 eV (TBmBJ) | 0.740 | 0.30 | 0.300 | 0.222 |
| Element hazard | none  (element-level flags (config/hazards.yaml)) | 1.000 | 0.20 | 0.200 | 0.200 |
| Simplicity | 2 elements (count of distinct elements) | 1.000 | 0.15 | 0.150 | 0.150 |
| Dielectric constant (κ) | 17.5  (DFPT total, max component) | 0.645 | 0.00 | 0.000 | 0.000 |
| **Total** | | | | | **0.922** |

**Confidence:** +2 band gap from TBmBJ; +2 experimental structure reference (ICSD, via JARVIS); +0 no stability cross-check (unavailable: skipped after earlier failure: Alexandria unreachable (ConnectionError)); +1 all weighted criteria have values.

**Cross-check (Alexandria):** unavailable. skipped after earlier failure: Alexandria unreachable (ConnectionError)
**Caveats:**
- Stability not cross-checked: skipped after earlier failure: Alexandria unreachable (ConnectionError).

**Polymorphs** (4 in JARVIS; first 5 by energy):

| JARVIS ID | Space group | Energy above hull (meV/atom) | TBmBJ gap | OptB88vdW gap | ICSD |
|---|---|---|---|---|---|
| JVASP-1390 | Fm-3m | 0 | 4.96 | 3.40 | yes |
| JVASP-49752 | P6_3/mmc | 92 | 4.77 | 3.08 | no |
| JVASP-49935 | P6_3/mmc | 102 | 5.37 | 2.75 | no |
| JVASP-36407 | Pm-3m | 382 | 3.89 | 2.78 | no |

**Sources:**
- JARVIS-DFT dft_3d record: [JVASP-1390](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-1390.html), retrieved/checked 2026-11-17T20:56:28+00:00
- dataset (figshare): [jdft_3d-9-24-2025.json](https://doi.org/10.6084/m9.figshare.6815699), retrieved/checked 2026-11-17T20:56:28+00:00

---
## 12. MgO: Suitability 0.914, Evidence confidence Low (1 pts)

Strongest: on the convex hull; band gap 4.85 eV (OptB88vdW).

**Representative:** [JVASP-115229](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-115229.html) · space group I4/mmm · origin JQE-593437 · retrieved 2026-11-17T20:56:28+00:00

| Value | Raw | Unit | Method / source |
|---|---|---|---|
| Energy above hull | 0 | meV/atom | recomputed hull from JARVIS formation energies, 6 competing compositions (D-013) |
| JARVIS `ehull` field | 0.0000 | eV/atom | not used (failed known-answer check C2, D-013) |
| Formation energy | -3.035 | eV/atom | JARVIS-DFT, OptB88vdW |
| Band gap, TBmBJ | missing | eV | JARVIS-DFT |
| Band gap, OptB88vdW | 4.852 | eV | JARVIS-DFT (used as fallback) |
| κ total (DFPT) | missing | – | JARVIS-DFT, max component |
| κ electronic / ionic | missing / missing | – | JARVIS-DFT |
| ICSD references | 0 | – | none |
| Dimensionality label | 3D-bulk | – | JARVIS (not filtered on, D-029) |

| Criterion | Input | Score | Weight | Effective weight | Contribution |
|---|---|---|---|---|---|
| Stability | 0 eV/atom (recomputed hull (D-013)) | 1.000 | 0.35 | 0.350 | 0.350 |
| Band gap | 4.85 eV (OptB88vdW) | 0.713 | 0.30 | 0.300 | 0.214 |
| Element hazard | none  (element-level flags (config/hazards.yaml)) | 1.000 | 0.20 | 0.200 | 0.200 |
| Simplicity | 2 elements (count of distinct elements) | 1.000 | 0.15 | 0.150 | 0.150 |
| Dielectric constant (κ) | missing | missing | 0.00 | 0.000 | 0.000 |
| **Total** | | | | | **0.914** |

**Confidence:** +0 band gap from OptB88vdW fallback (probable underestimate); +0 no ICSD reference found; +0 no stability cross-check (unavailable: skipped after earlier failure: Alexandria unreachable (ConnectionError)); +1 all weighted criteria have values.

**Cross-check (Alexandria):** unavailable. skipped after earlier failure: Alexandria unreachable (ConnectionError)
**Caveats:**
- Band gap is the OptB88vdW fallback (no TBmBJ value): probably an underestimate.
- Representative JVASP-115229 (I4/mmm) has no ICSD reference; JVASP-116 (Fm-3m) is 30 meV/atom higher and has one.
- No ICSD experimental structure reference found for this polymorph.
- Stability not cross-checked: skipped after earlier failure: Alexandria unreachable (ConnectionError).

**Polymorphs** (14 in JARVIS; first 5 by energy):

| JARVIS ID | Space group | Energy above hull (meV/atom) | TBmBJ gap | OptB88vdW gap | ICSD |
|---|---|---|---|---|---|
| JVASP-115229 | I4/mmm | 0 | missing | 4.85 | no |
| JVASP-116 | Fm-3m | 30 | 6.80 | 5.13 | yes |
| JVASP-79569 | P6_3/mmc | 85 | 5.64 | 3.67 | no |
| JVASP-119011 | Ibam | 112 | missing | 3.18 | no |
| JVASP-34228 | P6_3mc | 125 | 5.72 | 3.80 | yes |

**Sources:**
- JARVIS-DFT dft_3d record: [JVASP-115229](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-115229.html), retrieved/checked 2026-11-17T20:56:28+00:00
- dataset (figshare): [jdft_3d-9-24-2025.json](https://doi.org/10.6084/m9.figshare.6815699), retrieved/checked 2026-11-17T20:56:28+00:00

---
## 13. KO: Suitability 0.913, Evidence confidence High (5 pts)

Strongest: on the convex hull; band gap 4.83 eV (TBmBJ).

**Representative:** [JVASP-2190](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-2190.html) · space group Cmce · origin mp-2672 · retrieved 2026-11-17T20:56:28+00:00

| Value | Raw | Unit | Method / source |
|---|---|---|---|
| Energy above hull | 0 | meV/atom | recomputed hull from JARVIS formation energies, 6 competing compositions (D-013) |
| JARVIS `ehull` field | 0.0581 | eV/atom | not used (failed known-answer check C2, D-013) |
| Formation energy | -1.261 | eV/atom | JARVIS-DFT, OptB88vdW |
| Band gap, TBmBJ | 4.834 | eV | JARVIS-DFT |
| Band gap, OptB88vdW | 2.696 | eV | JARVIS-DFT |
| κ total (DFPT) | 5.82 | – | JARVIS-DFT, max component |
| κ electronic / ionic | 2.71 / 3.26 | – | JARVIS-DFT |
| ICSD references | 3 | – | 36641, 180559, 25527 |
| Dimensionality label | intercalated ion | – | JARVIS (not filtered on, D-029) |

| Criterion | Input | Score | Weight | Effective weight | Contribution |
|---|---|---|---|---|---|
| Stability | 0 eV/atom (recomputed hull (D-013)) | 1.000 | 0.35 | 0.350 | 0.350 |
| Band gap | 4.83 eV (TBmBJ) | 0.708 | 0.30 | 0.300 | 0.213 |
| Element hazard | none  (element-level flags (config/hazards.yaml)) | 1.000 | 0.20 | 0.200 | 0.200 |
| Simplicity | 2 elements (count of distinct elements) | 1.000 | 0.15 | 0.150 | 0.150 |
| Dielectric constant (κ) | 5.82  (DFPT total, max component) | 0.087 | 0.00 | 0.000 | 0.000 |
| **Total** | | | | | **0.913** |

**Confidence:** +2 band gap from TBmBJ; +2 experimental structure reference (ICSD, via JARVIS); +0 no stability cross-check (unavailable: skipped after earlier failure: Alexandria unreachable (ConnectionError)); +1 all weighted criteria have values.

**Cross-check (Alexandria):** unavailable. skipped after earlier failure: Alexandria unreachable (ConnectionError)
**Caveats:**
- Stability not cross-checked: skipped after earlier failure: Alexandria unreachable (ConnectionError).

**Polymorphs** (2 in JARVIS; first 5 by energy):

| JARVIS ID | Space group | Energy above hull (meV/atom) | TBmBJ gap | OptB88vdW gap | ICSD |
|---|---|---|---|---|---|
| JVASP-2190 | Cmce | 0 | 4.83 | 2.70 | yes |
| JVASP-37017 | P-62m | 13 | 4.24 | 2.31 | no |

**Sources:**
- JARVIS-DFT dft_3d record: [JVASP-2190](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-2190.html), retrieved/checked 2026-11-17T20:56:28+00:00
- dataset (figshare): [jdft_3d-9-24-2025.json](https://doi.org/10.6084/m9.figshare.6815699), retrieved/checked 2026-11-17T20:56:28+00:00

---
## 14. NdO2: Suitability 0.910, Evidence confidence High (4 pts)

Strongest: on the convex hull; band gap 4.80 eV (TBmBJ).

**Representative:** [JVASP-4152](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-4152.html) · space group C2/m · origin mp-31049 · retrieved 2026-11-17T20:56:28+00:00

| Value | Raw | Unit | Method / source |
|---|---|---|---|
| Energy above hull | 0 | meV/atom | recomputed hull from JARVIS formation energies, 6 competing compositions (D-013) |
| JARVIS `ehull` field | 0.9765 | eV/atom | not used (failed known-answer check C2, D-013) |
| Formation energy | -3.071 | eV/atom | JARVIS-DFT, OptB88vdW |
| Band gap, TBmBJ | 4.797 | eV | JARVIS-DFT |
| Band gap, OptB88vdW | 3.604 | eV | JARVIS-DFT |
| κ total (DFPT) | 14.10 | – | JARVIS-DFT, max component |
| κ electronic / ionic | 4.46 / 9.64 | – | JARVIS-DFT |
| ICSD references | 1 | – | 62228 |
| Dimensionality label | 3D-bulk | – | JARVIS (not filtered on, D-029) |

| Criterion | Input | Score | Weight | Effective weight | Contribution |
|---|---|---|---|---|---|
| Stability | 8.88e-16 eV/atom (recomputed hull (D-013)) | 1.000 | 0.35 | 0.350 | 0.350 |
| Band gap | 4.8 eV (TBmBJ) | 0.699 | 0.30 | 0.300 | 0.210 |
| Element hazard | none  (element-level flags (config/hazards.yaml)) | 1.000 | 0.20 | 0.200 | 0.200 |
| Simplicity | 2 elements (count of distinct elements) | 1.000 | 0.15 | 0.150 | 0.150 |
| Dielectric constant (κ) | 14.1  (DFPT total, max component) | 0.481 | 0.00 | 0.000 | 0.000 |
| **Total** | | | | | **0.910** |

**Confidence:** +2 band gap from TBmBJ; +2 experimental structure reference (ICSD, via JARVIS); +0 no stability cross-check (unavailable: skipped after earlier failure: Alexandria unreachable (ConnectionError)); +1 all weighted criteria have values; -1 contains Nd: DFT energies and gaps less reliable.

**Cross-check (Alexandria):** unavailable. skipped after earlier failure: Alexandria unreachable (ConnectionError)
**Caveats:**
- Contains Nd: DFT energies and gaps are less reliable for these elements, so stability and gap may be wrong.
- Stability not cross-checked: skipped after earlier failure: Alexandria unreachable (ConnectionError).

**Polymorphs** (3 in JARVIS; first 5 by energy):

| JARVIS ID | Space group | Energy above hull (meV/atom) | TBmBJ gap | OptB88vdW gap | ICSD |
|---|---|---|---|---|---|
| JVASP-4152 | C2/m | 0 | 4.80 | 3.60 | yes |
| JVASP-95049 | I4/mmm | 226 | missing | 0.00 | no |
| JVASP-50921 | Fm-3m | 238 | missing | 0.00 | no |

**Sources:**
- JARVIS-DFT dft_3d record: [JVASP-4152](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-4152.html), retrieved/checked 2026-11-17T20:56:28+00:00
- dataset (figshare): [jdft_3d-9-24-2025.json](https://doi.org/10.6084/m9.figshare.6815699), retrieved/checked 2026-11-17T20:56:28+00:00

---
## 15. BeO: Suitability 0.900, Evidence confidence Medium (3 pts)

Strongest: on the convex hull; band gap 8.04 eV (OptB88vdW).

**Representative:** [JVASP-20778](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-20778.html) · space group P6_3mc · origin mp-2542 · retrieved 2026-11-17T20:56:28+00:00

| Value | Raw | Unit | Method / source |
|---|---|---|---|
| Energy above hull | 0 | meV/atom | recomputed hull from JARVIS formation energies, 6 competing compositions (D-013) |
| JARVIS `ehull` field | 0.0000 | eV/atom | not used (failed known-answer check C2, D-013) |
| Formation energy | -3.031 | eV/atom | JARVIS-DFT, OptB88vdW |
| Band gap, TBmBJ | missing | eV | JARVIS-DFT |
| Band gap, OptB88vdW | 8.040 | eV | JARVIS-DFT (used as fallback) |
| κ total (DFPT) | 7.67 | – | JARVIS-DFT, max component |
| κ electronic / ionic | 3.09 / 4.58 | – | JARVIS-DFT |
| ICSD references | 31 | – | 15620, 62726, 62727, 62728, 62729 |
| Dimensionality label | intercalated ion | – | JARVIS (not filtered on, D-029) |

| Criterion | Input | Score | Weight | Effective weight | Contribution |
|---|---|---|---|---|---|
| Stability | 0 eV/atom (recomputed hull (D-013)) | 1.000 | 0.35 | 0.350 | 0.350 |
| Band gap | 8.04 eV (OptB88vdW) | 1.000 | 0.30 | 0.300 | 0.300 |
| Element hazard | Be  (element-level flags (config/hazards.yaml)) | 0.500 | 0.20 | 0.200 | 0.100 |
| Simplicity | 2 elements (count of distinct elements) | 1.000 | 0.15 | 0.150 | 0.150 |
| Dielectric constant (κ) | 7.67  (DFPT total, max component) | 0.175 | 0.00 | 0.000 | 0.000 |
| **Total** | | | | | **0.900** |

**Confidence:** +0 band gap from OptB88vdW fallback (probable underestimate); +2 experimental structure reference (ICSD, via JARVIS); +0 no stability cross-check (unavailable: skipped after earlier failure: Alexandria unreachable (ConnectionError)); +1 all weighted criteria have values.

**Cross-check (Alexandria):** unavailable. skipped after earlier failure: Alexandria unreachable (ConnectionError)
**Caveats:**
- Band gap is the OptB88vdW fallback (no TBmBJ value): probably an underestimate.
- Element flag Be: Beryllium and beryllium compounds.
- Stability not cross-checked: skipped after earlier failure: Alexandria unreachable (ConnectionError).

**Polymorphs** (4 in JARVIS; first 5 by energy):

| JARVIS ID | Space group | Energy above hull (meV/atom) | TBmBJ gap | OptB88vdW gap | ICSD |
|---|---|---|---|---|---|
| JVASP-20778 | P6_3mc | 0 | missing | 8.04 | yes |
| JVASP-22522 | F-43m | 6 | 9.23 | 7.29 | yes |
| JVASP-58368 | P4_2/mnm | 17 | 9.01 | 7.61 | yes |
| JVASP-57665 | Fm-3m | 494 | 9.69 | 8.76 | yes |

**Sources:**
- JARVIS-DFT dft_3d record: [JVASP-20778](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-20778.html), retrieved/checked 2026-11-17T20:56:28+00:00
- dataset (figshare): [jdft_3d-9-24-2025.json](https://doi.org/10.6084/m9.figshare.6815699), retrieved/checked 2026-11-17T20:56:28+00:00
- IARC Monographs: Agents Classified by the IARC Monographs (List of Classifications), Group 1: [Be](https://monographs.iarc.who.int/list-of-classifications), retrieved/checked 2026-11-18

---
## 16. TeO2: Suitability 0.898, Evidence confidence High (5 pts)

Strongest: on the convex hull; no flagged elements.

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
| Band gap | 4.64 eV (TBmBJ) | 0.661 | 0.30 | 0.300 | 0.198 |
| Element hazard | none  (element-level flags (config/hazards.yaml)) | 1.000 | 0.20 | 0.200 | 0.200 |
| Simplicity | 2 elements (count of distinct elements) | 1.000 | 0.15 | 0.150 | 0.150 |
| Dielectric constant (κ) | 28.8  (DFPT total, max component) | 1.000 | 0.00 | 0.000 | 0.000 |
| **Total** | | | | | **0.898** |

**Confidence:** +2 band gap from TBmBJ; +2 experimental structure reference (ICSD, via JARVIS); +0 no stability cross-check (unavailable: skipped after earlier failure: Alexandria unreachable (ConnectionError)); +1 all weighted criteria have values.

**Cross-check (Alexandria):** unavailable. skipped after earlier failure: Alexandria unreachable (ConnectionError)
**Caveats:**
- Stability not cross-checked: skipped after earlier failure: Alexandria unreachable (ConnectionError).

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
## 17. Y2O3: Suitability 0.873, Evidence confidence Medium (3 pts)

Strongest: on the convex hull; no flagged elements.

**Representative:** [JVASP-20793](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-20793.html) · space group Ia-3 · origin mp-2652 · retrieved 2026-11-17T20:56:28+00:00

| Value | Raw | Unit | Method / source |
|---|---|---|---|
| Energy above hull | 0 | meV/atom | recomputed hull from JARVIS formation energies, 4 competing compositions (D-013) |
| JARVIS `ehull` field | 2.0073 | eV/atom | not used (failed known-answer check C2, D-013) |
| Formation energy | -3.861 | eV/atom | JARVIS-DFT, OptB88vdW |
| Band gap, TBmBJ | missing | eV | JARVIS-DFT |
| Band gap, OptB88vdW | 4.307 | eV | JARVIS-DFT (used as fallback) |
| κ total (DFPT) | missing | – | JARVIS-DFT, max component |
| κ electronic / ionic | missing / missing | – | JARVIS-DFT |
| ICSD references | 28 | – | 23811, 16394, 77081, 153500, 86813 |
| Dimensionality label | 3D-bulk | – | JARVIS (not filtered on, D-029) |

| Criterion | Input | Score | Weight | Effective weight | Contribution |
|---|---|---|---|---|---|
| Stability | 0 eV/atom (recomputed hull (D-013)) | 1.000 | 0.35 | 0.350 | 0.350 |
| Band gap | 4.31 eV (OptB88vdW) | 0.577 | 0.30 | 0.300 | 0.173 |
| Element hazard | none  (element-level flags (config/hazards.yaml)) | 1.000 | 0.20 | 0.200 | 0.200 |
| Simplicity | 2 elements (count of distinct elements) | 1.000 | 0.15 | 0.150 | 0.150 |
| Dielectric constant (κ) | missing | missing | 0.00 | 0.000 | 0.000 |
| **Total** | | | | | **0.873** |

**Confidence:** +0 band gap from OptB88vdW fallback (probable underestimate); +2 experimental structure reference (ICSD, via JARVIS); +0 no stability cross-check (unavailable: skipped after earlier failure: Alexandria unreachable (ConnectionError)); +1 all weighted criteria have values.

**Cross-check (Alexandria):** unavailable. skipped after earlier failure: Alexandria unreachable (ConnectionError)
**Caveats:**
- Band gap is the OptB88vdW fallback (no TBmBJ value): probably an underestimate.
- Stability not cross-checked: skipped after earlier failure: Alexandria unreachable (ConnectionError).

**Polymorphs** (6 in JARVIS; first 5 by energy):

| JARVIS ID | Space group | Energy above hull (meV/atom) | TBmBJ gap | OptB88vdW gap | ICSD |
|---|---|---|---|---|---|
| JVASP-20793 | Ia-3 | 0 | missing | 4.31 | yes |
| JVASP-57843 | C2/m | 28 | 5.25 | 4.09 | yes |
| JVASP-49913 | R-3c | 44 | 5.87 | 4.67 | no |
| JVASP-7765 | P-3m1 | 49 | 5.37 | 4.21 | yes |
| JVASP-43789 | P2_1/m | 67 | missing | 2.87 | no |

**Sources:**
- JARVIS-DFT dft_3d record: [JVASP-20793](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-20793.html), retrieved/checked 2026-11-17T20:56:28+00:00
- dataset (figshare): [jdft_3d-9-24-2025.json](https://doi.org/10.6084/m9.figshare.6815699), retrieved/checked 2026-11-17T20:56:28+00:00

---
## 18. RbO: Suitability 0.871, Evidence confidence High (5 pts)

Strongest: on the convex hull; no flagged elements.

**Representative:** [JVASP-8148](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-8148.html) · space group Immm · origin mp-7895 · retrieved 2026-11-17T20:56:28+00:00

| Value | Raw | Unit | Method / source |
|---|---|---|---|
| Energy above hull | 0 | meV/atom | recomputed hull from JARVIS formation energies, 7 competing compositions (D-013) |
| JARVIS `ehull` field | 0.2362 | eV/atom | not used (failed known-answer check C2, D-013) |
| Formation energy | -1.207 | eV/atom | JARVIS-DFT, OptB88vdW |
| Band gap, TBmBJ | 4.277 | eV | JARVIS-DFT |
| Band gap, OptB88vdW | 2.177 | eV | JARVIS-DFT |
| κ total (DFPT) | 6.08 | – | JARVIS-DFT, max component |
| κ electronic / ionic | 2.88 / 3.20 | – | JARVIS-DFT |
| ICSD references | 2 | – | 25528, 180560 |
| Dimensionality label | intercalated ion | – | JARVIS (not filtered on, D-029) |

| Criterion | Input | Score | Weight | Effective weight | Contribution |
|---|---|---|---|---|---|
| Stability | 0 eV/atom (recomputed hull (D-013)) | 1.000 | 0.35 | 0.350 | 0.350 |
| Band gap | 4.28 eV (TBmBJ) | 0.569 | 0.30 | 0.300 | 0.171 |
| Element hazard | none  (element-level flags (config/hazards.yaml)) | 1.000 | 0.20 | 0.200 | 0.200 |
| Simplicity | 2 elements (count of distinct elements) | 1.000 | 0.15 | 0.150 | 0.150 |
| Dielectric constant (κ) | 6.08  (DFPT total, max component) | 0.099 | 0.00 | 0.000 | 0.000 |
| **Total** | | | | | **0.871** |

**Confidence:** +2 band gap from TBmBJ; +2 experimental structure reference (ICSD, via JARVIS); +0 no stability cross-check (unavailable: skipped after earlier failure: Alexandria unreachable (ConnectionError)); +1 all weighted criteria have values.

**Cross-check (Alexandria):** unavailable. skipped after earlier failure: Alexandria unreachable (ConnectionError)
**Caveats:**
- Stability not cross-checked: skipped after earlier failure: Alexandria unreachable (ConnectionError).

**Polymorphs** (3 in JARVIS; first 5 by energy):

| JARVIS ID | Space group | Energy above hull (meV/atom) | TBmBJ gap | OptB88vdW gap | ICSD |
|---|---|---|---|---|---|
| JVASP-8148 | Immm | 0 | 4.28 | 2.18 | yes |
| JVASP-103016 | Cmcm | 347 | 0.00 | 0.01 | no |
| JVASP-102149 | C2/m | 419 | 0.00 | 0.00 | no |

**Sources:**
- JARVIS-DFT dft_3d record: [JVASP-8148](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-8148.html), retrieved/checked 2026-11-17T20:56:28+00:00
- dataset (figshare): [jdft_3d-9-24-2025.json](https://doi.org/10.6084/m9.figshare.6815699), retrieved/checked 2026-11-17T20:56:28+00:00

---
## 19. Ta2O5: Suitability 0.870, Evidence confidence High (5 pts)

Strongest: on the convex hull; no flagged elements.

**Representative:** [JVASP-10674](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-10674.html) · space group C2/c · origin mp-10390 · retrieved 2026-11-17T20:56:28+00:00

| Value | Raw | Unit | Method / source |
|---|---|---|---|
| Energy above hull | 0 | meV/atom | recomputed hull from JARVIS formation energies, 9 competing compositions (D-013) |
| JARVIS `ehull` field | 3.7188 | eV/atom | not used (failed known-answer check C2, D-013) |
| Formation energy | -3.043 | eV/atom | JARVIS-DFT, OptB88vdW |
| Band gap, TBmBJ | 4.273 | eV | JARVIS-DFT |
| Band gap, OptB88vdW | 3.177 | eV | JARVIS-DFT |
| κ total (DFPT) | missing | – | JARVIS-DFT, max component |
| κ electronic / ionic | missing / missing | – | JARVIS-DFT |
| ICSD references | 1 | – | 280396 |
| Dimensionality label | 3D-bulk | – | JARVIS (not filtered on, D-029) |

| Criterion | Input | Score | Weight | Effective weight | Contribution |
|---|---|---|---|---|---|
| Stability | 0 eV/atom (recomputed hull (D-013)) | 1.000 | 0.35 | 0.350 | 0.350 |
| Band gap | 4.27 eV (TBmBJ) | 0.568 | 0.30 | 0.300 | 0.170 |
| Element hazard | none  (element-level flags (config/hazards.yaml)) | 1.000 | 0.20 | 0.200 | 0.200 |
| Simplicity | 2 elements (count of distinct elements) | 1.000 | 0.15 | 0.150 | 0.150 |
| Dielectric constant (κ) | missing | missing | 0.00 | 0.000 | 0.000 |
| **Total** | | | | | **0.870** |

**Confidence:** +2 band gap from TBmBJ; +2 experimental structure reference (ICSD, via JARVIS); +0 no stability cross-check (unavailable: skipped after earlier failure: Alexandria unreachable (ConnectionError)); +1 all weighted criteria have values.

**Cross-check (Alexandria):** unavailable. skipped after earlier failure: Alexandria unreachable (ConnectionError)
**Caveats:**
- Stability not cross-checked: skipped after earlier failure: Alexandria unreachable (ConnectionError).

**Polymorphs** (10 in JARVIS; first 5 by energy):

| JARVIS ID | Space group | Energy above hull (meV/atom) | TBmBJ gap | OptB88vdW gap | ICSD |
|---|---|---|---|---|---|
| JVASP-10674 | C2/c | 0 | 4.27 | 3.18 | yes |
| JVASP-9650 | Pmmn | 28 | 3.50 | 2.34 | no |
| JVASP-103135 | Cmmm | 28 | missing | 2.22 | no |
| JVASP-110736 | C2/m | 42 | 3.36 | 2.24 | no |
| JVASP-42248 | Cm | 69 | missing | 3.10 | no |

**Sources:**
- JARVIS-DFT dft_3d record: [JVASP-10674](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-10674.html), retrieved/checked 2026-11-17T20:56:28+00:00
- dataset (figshare): [jdft_3d-9-24-2025.json](https://doi.org/10.6084/m9.figshare.6815699), retrieved/checked 2026-11-17T20:56:28+00:00

---
## 20. Lu2O3: Suitability 0.867, Evidence confidence Medium (3 pts)

Strongest: on the convex hull; no flagged elements.

**Representative:** [JVASP-20150](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-20150.html) · space group Ia-3 · origin mp-1427 · retrieved 2026-11-17T20:56:28+00:00

| Value | Raw | Unit | Method / source |
|---|---|---|---|
| Energy above hull | 0 | meV/atom | recomputed hull from JARVIS formation energies, 3 competing compositions (D-013) |
| JARVIS `ehull` field | 1.3173 | eV/atom | not used (failed known-answer check C2, D-013) |
| Formation energy | -3.963 | eV/atom | JARVIS-DFT, OptB88vdW |
| Band gap, TBmBJ | missing | eV | JARVIS-DFT |
| Band gap, OptB88vdW | 4.224 | eV | JARVIS-DFT (used as fallback) |
| κ total (DFPT) | missing | – | JARVIS-DFT, max component |
| κ electronic / ionic | missing / missing | – | JARVIS-DFT |
| ICSD references | 6 | – | 642477, 151762, 96211, 168341, 40471 |
| Dimensionality label | 3D-bulk | – | JARVIS (not filtered on, D-029) |

| Criterion | Input | Score | Weight | Effective weight | Contribution |
|---|---|---|---|---|---|
| Stability | 0 eV/atom (recomputed hull (D-013)) | 1.000 | 0.35 | 0.350 | 0.350 |
| Band gap | 4.22 eV (OptB88vdW) | 0.556 | 0.30 | 0.300 | 0.167 |
| Element hazard | none  (element-level flags (config/hazards.yaml)) | 1.000 | 0.20 | 0.200 | 0.200 |
| Simplicity | 2 elements (count of distinct elements) | 1.000 | 0.15 | 0.150 | 0.150 |
| Dielectric constant (κ) | missing | missing | 0.00 | 0.000 | 0.000 |
| **Total** | | | | | **0.867** |

**Confidence:** +0 band gap from OptB88vdW fallback (probable underestimate); +2 experimental structure reference (ICSD, via JARVIS); +0 no stability cross-check (unavailable: skipped after earlier failure: Alexandria unreachable (ConnectionError)); +1 all weighted criteria have values.

**Cross-check (Alexandria):** unavailable. skipped after earlier failure: Alexandria unreachable (ConnectionError)
**Caveats:**
- Band gap is the OptB88vdW fallback (no TBmBJ value): probably an underestimate.
- Stability not cross-checked: skipped after earlier failure: Alexandria unreachable (ConnectionError).

**Polymorphs** (3 in JARVIS; first 5 by energy):

| JARVIS ID | Space group | Energy above hull (meV/atom) | TBmBJ gap | OptB88vdW gap | ICSD |
|---|---|---|---|---|---|
| JVASP-20150 | Ia-3 | 0 | missing | 4.22 | yes |
| JVASP-91449 | C2/m | 37 | missing | 4.36 | yes |
| JVASP-7771 | P-3m1 | 74 | 6.33 | 4.46 | yes |

**Sources:**
- JARVIS-DFT dft_3d record: [JVASP-20150](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-20150.html), retrieved/checked 2026-11-17T20:56:28+00:00
- dataset (figshare): [jdft_3d-9-24-2025.json](https://doi.org/10.6084/m9.figshare.6815699), retrieved/checked 2026-11-17T20:56:28+00:00

---
## 21. Tm2O3: Suitability 0.865, Evidence confidence Medium (2 pts)

Strongest: on the convex hull; no flagged elements.

**Representative:** [JVASP-20193](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-20193.html) · space group Ia-3 · origin mp-1767 · retrieved 2026-11-17T20:56:28+00:00

| Value | Raw | Unit | Method / source |
|---|---|---|---|
| Energy above hull | 0 | meV/atom | recomputed hull from JARVIS formation energies, 4 competing compositions (D-013) |
| JARVIS `ehull` field | 1.3295 | eV/atom | not used (failed known-answer check C2, D-013) |
| Formation energy | -3.924 | eV/atom | JARVIS-DFT, OptB88vdW |
| Band gap, TBmBJ | missing | eV | JARVIS-DFT |
| Band gap, OptB88vdW | 4.194 | eV | JARVIS-DFT (used as fallback) |
| κ total (DFPT) | missing | – | JARVIS-DFT, max component |
| κ electronic / ionic | missing / missing | – | JARVIS-DFT |
| ICSD references | 4 | – | 647581, 78582, 61270, 90669 |
| Dimensionality label | 3D-bulk | – | JARVIS (not filtered on, D-029) |

| Criterion | Input | Score | Weight | Effective weight | Contribution |
|---|---|---|---|---|---|
| Stability | 0 eV/atom (recomputed hull (D-013)) | 1.000 | 0.35 | 0.350 | 0.350 |
| Band gap | 4.19 eV (OptB88vdW) | 0.548 | 0.30 | 0.300 | 0.165 |
| Element hazard | none  (element-level flags (config/hazards.yaml)) | 1.000 | 0.20 | 0.200 | 0.200 |
| Simplicity | 2 elements (count of distinct elements) | 1.000 | 0.15 | 0.150 | 0.150 |
| Dielectric constant (κ) | missing | missing | 0.00 | 0.000 | 0.000 |
| **Total** | | | | | **0.865** |

**Confidence:** +0 band gap from OptB88vdW fallback (probable underestimate); +2 experimental structure reference (ICSD, via JARVIS); +0 no stability cross-check (unavailable: skipped after earlier failure: Alexandria unreachable (ConnectionError)); +1 all weighted criteria have values; -1 contains Tm: DFT energies and gaps less reliable.

**Cross-check (Alexandria):** unavailable. skipped after earlier failure: Alexandria unreachable (ConnectionError)
**Caveats:**
- Band gap is the OptB88vdW fallback (no TBmBJ value): probably an underestimate.
- Contains Tm: DFT energies and gaps are less reliable for these elements, so stability and gap may be wrong.
- Stability not cross-checked: skipped after earlier failure: Alexandria unreachable (ConnectionError).

**Polymorphs** (3 in JARVIS; first 5 by energy):

| JARVIS ID | Space group | Energy above hull (meV/atom) | TBmBJ gap | OptB88vdW gap | ICSD |
|---|---|---|---|---|---|
| JVASP-20193 | Ia-3 | 0 | missing | 4.19 | yes |
| JVASP-34569 | C2/m | 32 | missing | 4.26 | yes |
| JVASP-7770 | P-3m1 | 60 | 6.13 | 4.49 | yes |

**Sources:**
- JARVIS-DFT dft_3d record: [JVASP-20193](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-20193.html), retrieved/checked 2026-11-17T20:56:28+00:00
- dataset (figshare): [jdft_3d-9-24-2025.json](https://doi.org/10.6084/m9.figshare.6815699), retrieved/checked 2026-11-17T20:56:28+00:00

---
## 22. Er2O3: Suitability 0.860, Evidence confidence Medium (2 pts)

Strongest: on the convex hull; no flagged elements.

**Representative:** [JVASP-20325](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-20325.html) · space group Ia-3 · origin mp-679 · retrieved 2026-11-17T20:56:28+00:00

| Value | Raw | Unit | Method / source |
|---|---|---|---|
| Energy above hull | 0 | meV/atom | recomputed hull from JARVIS formation energies, 3 competing compositions (D-013) |
| JARVIS `ehull` field | 1.3435 | eV/atom | not used (failed known-answer check C2, D-013) |
| Formation energy | -3.890 | eV/atom | JARVIS-DFT, OptB88vdW |
| Band gap, TBmBJ | missing | eV | JARVIS-DFT |
| Band gap, OptB88vdW | 4.138 | eV | JARVIS-DFT (used as fallback) |
| κ total (DFPT) | missing | – | JARVIS-DFT, max component |
| κ electronic / ionic | missing / missing | – | JARVIS-DFT |
| ICSD references | 15 | – | 39521, 630897, 94888, 180843, 96210 |
| Dimensionality label | 3D-bulk | – | JARVIS (not filtered on, D-029) |

| Criterion | Input | Score | Weight | Effective weight | Contribution |
|---|---|---|---|---|---|
| Stability | 0 eV/atom (recomputed hull (D-013)) | 1.000 | 0.35 | 0.350 | 0.350 |
| Band gap | 4.14 eV (OptB88vdW) | 0.534 | 0.30 | 0.300 | 0.160 |
| Element hazard | none  (element-level flags (config/hazards.yaml)) | 1.000 | 0.20 | 0.200 | 0.200 |
| Simplicity | 2 elements (count of distinct elements) | 1.000 | 0.15 | 0.150 | 0.150 |
| Dielectric constant (κ) | missing | missing | 0.00 | 0.000 | 0.000 |
| **Total** | | | | | **0.860** |

**Confidence:** +0 band gap from OptB88vdW fallback (probable underestimate); +2 experimental structure reference (ICSD, via JARVIS); +0 no stability cross-check (unavailable: skipped after earlier failure: Alexandria unreachable (ConnectionError)); +1 all weighted criteria have values; -1 contains Er: DFT energies and gaps less reliable.

**Cross-check (Alexandria):** unavailable. skipped after earlier failure: Alexandria unreachable (ConnectionError)
**Caveats:**
- Band gap is the OptB88vdW fallback (no TBmBJ value): probably an underestimate.
- Contains Er: DFT energies and gaps are less reliable for these elements, so stability and gap may be wrong.
- Stability not cross-checked: skipped after earlier failure: Alexandria unreachable (ConnectionError).

**Polymorphs** (4 in JARVIS; first 5 by energy):

| JARVIS ID | Space group | Energy above hull (meV/atom) | TBmBJ gap | OptB88vdW gap | ICSD |
|---|---|---|---|---|---|
| JVASP-20325 | Ia-3 | 0 | missing | 4.14 | yes |
| JVASP-9124 | C2/m | 28 | 5.76 | 4.21 | yes |
| JVASP-7769 | P-3m1 | 52 | 5.99 | 4.42 | yes |
| JVASP-102769 | R3m | 135 | 4.92 | 2.92 | no |

**Sources:**
- JARVIS-DFT dft_3d record: [JVASP-20325](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-20325.html), retrieved/checked 2026-11-17T20:56:28+00:00
- dataset (figshare): [jdft_3d-9-24-2025.json](https://doi.org/10.6084/m9.figshare.6815699), retrieved/checked 2026-11-17T20:56:28+00:00

---
## 23. Ho2O3: Suitability 0.857, Evidence confidence Medium (2 pts)

Strongest: on the convex hull; no flagged elements.

**Representative:** [JVASP-20339](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-20339.html) · space group Ia-3 · origin mp-812 · retrieved 2026-11-17T20:56:28+00:00

| Value | Raw | Unit | Method / source |
|---|---|---|---|
| Energy above hull | 0 | meV/atom | recomputed hull from JARVIS formation energies, 5 competing compositions (D-013) |
| JARVIS `ehull` field | 1.5465 | eV/atom | not used (failed known-answer check C2, D-013) |
| Formation energy | -3.860 | eV/atom | JARVIS-DFT, OptB88vdW |
| Band gap, TBmBJ | missing | eV | JARVIS-DFT |
| Band gap, OptB88vdW | 4.094 | eV | JARVIS-DFT (used as fallback) |
| κ total (DFPT) | missing | – | JARVIS-DFT, max component |
| κ electronic / ionic | missing / missing | – | JARVIS-DFT |
| ICSD references | 10 | – | 44516, 639525, 80038, 152458, 33655 |
| Dimensionality label | 3D-bulk | – | JARVIS (not filtered on, D-029) |

| Criterion | Input | Score | Weight | Effective weight | Contribution |
|---|---|---|---|---|---|
| Stability | 0 eV/atom (recomputed hull (D-013)) | 1.000 | 0.35 | 0.350 | 0.350 |
| Band gap | 4.09 eV (OptB88vdW) | 0.524 | 0.30 | 0.300 | 0.157 |
| Element hazard | none  (element-level flags (config/hazards.yaml)) | 1.000 | 0.20 | 0.200 | 0.200 |
| Simplicity | 2 elements (count of distinct elements) | 1.000 | 0.15 | 0.150 | 0.150 |
| Dielectric constant (κ) | missing | missing | 0.00 | 0.000 | 0.000 |
| **Total** | | | | | **0.857** |

**Confidence:** +0 band gap from OptB88vdW fallback (probable underestimate); +2 experimental structure reference (ICSD, via JARVIS); +0 no stability cross-check (unavailable: skipped after earlier failure: Alexandria unreachable (ConnectionError)); +1 all weighted criteria have values; -1 contains Ho: DFT energies and gaps less reliable.

**Cross-check (Alexandria):** unavailable. skipped after earlier failure: Alexandria unreachable (ConnectionError)
**Caveats:**
- Band gap is the OptB88vdW fallback (no TBmBJ value): probably an underestimate.
- Contains Ho: DFT energies and gaps are less reliable for these elements, so stability and gap may be wrong.
- Stability not cross-checked: skipped after earlier failure: Alexandria unreachable (ConnectionError).

**Polymorphs** (4 in JARVIS; first 5 by energy):

| JARVIS ID | Space group | Energy above hull (meV/atom) | TBmBJ gap | OptB88vdW gap | ICSD |
|---|---|---|---|---|---|
| JVASP-20339 | Ia-3 | 0 | missing | 4.09 | yes |
| JVASP-57815 | C2/m | 23 | 5.66 | 4.14 | yes |
| JVASP-7768 | P-3m1 | 44 | 5.89 | 4.34 | yes |
| JVASP-52660 | Pn-3m | 506 | missing | 0.00 | no |

**Sources:**
- JARVIS-DFT dft_3d record: [JVASP-20339](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-20339.html), retrieved/checked 2026-11-17T20:56:28+00:00
- dataset (figshare): [jdft_3d-9-24-2025.json](https://doi.org/10.6084/m9.figshare.6815699), retrieved/checked 2026-11-17T20:56:28+00:00

---
## 24. Dy2O3: Suitability 0.856, Evidence confidence Medium (2 pts)

Strongest: on the convex hull; no flagged elements.

**Representative:** [JVASP-34497](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-34497.html) · space group C2/m · origin mp-555574 · retrieved 2026-11-17T20:56:28+00:00

| Value | Raw | Unit | Method / source |
|---|---|---|---|
| Energy above hull | 0 | meV/atom | recomputed hull from JARVIS formation energies, 4 competing compositions (D-013) |
| JARVIS `ehull` field | 1.3773 | eV/atom | not used (failed known-answer check C2, D-013) |
| Formation energy | -3.813 | eV/atom | JARVIS-DFT, OptB88vdW |
| Band gap, TBmBJ | missing | eV | JARVIS-DFT |
| Band gap, OptB88vdW | 4.084 | eV | JARVIS-DFT (used as fallback) |
| κ total (DFPT) | missing | – | JARVIS-DFT, max component |
| κ electronic / ionic | missing / missing | – | JARVIS-DFT |
| ICSD references | 1 | – | 160228 |
| Dimensionality label | 3D-bulk | – | JARVIS (not filtered on, D-029) |

| Criterion | Input | Score | Weight | Effective weight | Contribution |
|---|---|---|---|---|---|
| Stability | 0 eV/atom (recomputed hull (D-013)) | 1.000 | 0.35 | 0.350 | 0.350 |
| Band gap | 4.08 eV (OptB88vdW) | 0.521 | 0.30 | 0.300 | 0.156 |
| Element hazard | none  (element-level flags (config/hazards.yaml)) | 1.000 | 0.20 | 0.200 | 0.200 |
| Simplicity | 2 elements (count of distinct elements) | 1.000 | 0.15 | 0.150 | 0.150 |
| Dielectric constant (κ) | missing | missing | 0.00 | 0.000 | 0.000 |
| **Total** | | | | | **0.856** |

**Confidence:** +0 band gap from OptB88vdW fallback (probable underestimate); +2 experimental structure reference (ICSD, via JARVIS); +0 no stability cross-check (unavailable: skipped after earlier failure: Alexandria unreachable (ConnectionError)); +1 all weighted criteria have values; -1 contains Dy: DFT energies and gaps less reliable.

**Cross-check (Alexandria):** unavailable. skipped after earlier failure: Alexandria unreachable (ConnectionError)
**Caveats:**
- Band gap is the OptB88vdW fallback (no TBmBJ value): probably an underestimate.
- Contains Dy: DFT energies and gaps are less reliable for these elements, so stability and gap may be wrong.
- Stability not cross-checked: skipped after earlier failure: Alexandria unreachable (ConnectionError).

**Polymorphs** (4 in JARVIS; first 5 by energy):

| JARVIS ID | Space group | Energy above hull (meV/atom) | TBmBJ gap | OptB88vdW gap | ICSD |
|---|---|---|---|---|---|
| JVASP-34497 | C2/m | 0 | missing | 4.08 | yes |
| JVASP-7767 | P-3m1 | 18 | 5.82 | 4.28 | yes |
| JVASP-106085 | P-4m2 | 250 | 3.83 | 1.58 | no |
| JVASP-53340 | Pn-3m | 476 | missing | 0.00 | no |

**Sources:**
- JARVIS-DFT dft_3d record: [JVASP-34497](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-34497.html), retrieved/checked 2026-11-17T20:56:28+00:00
- dataset (figshare): [jdft_3d-9-24-2025.json](https://doi.org/10.6084/m9.figshare.6815699), retrieved/checked 2026-11-17T20:56:28+00:00

---
## 25. NaO: Suitability 0.855, Evidence confidence High (5 pts)

Strongest: on the convex hull; no flagged elements.

**Representative:** [JVASP-9119](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-9119.html) · space group P-62m · origin mp-2340 · retrieved 2026-11-17T20:56:28+00:00

| Value | Raw | Unit | Method / source |
|---|---|---|---|
| Energy above hull | 0 | meV/atom | recomputed hull from JARVIS formation energies, 7 competing compositions (D-013) |
| JARVIS `ehull` field | 0.1496 | eV/atom | not used (failed known-answer check C2, D-013) |
| Formation energy | -1.261 | eV/atom | JARVIS-DFT, OptB88vdW |
| Band gap, TBmBJ | 4.065 | eV | JARVIS-DFT |
| Band gap, OptB88vdW | 1.937 | eV | JARVIS-DFT |
| κ total (DFPT) | 6.92 | – | JARVIS-DFT, max component |
| κ electronic / ionic | 2.80 / 4.12 | – | JARVIS-DFT |
| ICSD references | 4 | – | 109276, 180558, 25526, 26575 |
| Dimensionality label | intercalated ion | – | JARVIS (not filtered on, D-029) |

| Criterion | Input | Score | Weight | Effective weight | Contribution |
|---|---|---|---|---|---|
| Stability | 0 eV/atom (recomputed hull (D-013)) | 1.000 | 0.35 | 0.350 | 0.350 |
| Band gap | 4.07 eV (TBmBJ) | 0.516 | 0.30 | 0.300 | 0.155 |
| Element hazard | none  (element-level flags (config/hazards.yaml)) | 1.000 | 0.20 | 0.200 | 0.200 |
| Simplicity | 2 elements (count of distinct elements) | 1.000 | 0.15 | 0.150 | 0.150 |
| Dielectric constant (κ) | 6.92  (DFPT total, max component) | 0.139 | 0.00 | 0.000 | 0.000 |
| **Total** | | | | | **0.855** |

**Confidence:** +2 band gap from TBmBJ; +2 experimental structure reference (ICSD, via JARVIS); +0 no stability cross-check (unavailable: skipped after earlier failure: Alexandria unreachable (ConnectionError)); +1 all weighted criteria have values.

**Cross-check (Alexandria):** unavailable. skipped after earlier failure: Alexandria unreachable (ConnectionError)
**Caveats:**
- Stability not cross-checked: skipped after earlier failure: Alexandria unreachable (ConnectionError).

**Polymorphs** (7 in JARVIS; first 5 by energy):

| JARVIS ID | Space group | Energy above hull (meV/atom) | TBmBJ gap | OptB88vdW gap | ICSD |
|---|---|---|---|---|---|
| JVASP-9119 | P-62m | 0 | 4.07 | 1.94 | yes |
| JVASP-135519 | Amm2 | 13 | missing | 1.57 | no |
| JVASP-78469 | Pm-3m | 319 | missing | 0.00 | no |
| JVASP-106478 | Pbcm | 352 | missing | 0.00 | no |
| JVASP-126245 | P-6m2 | 422 | missing | 0.00 | no |

**Sources:**
- JARVIS-DFT dft_3d record: [JVASP-9119](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-9119.html), retrieved/checked 2026-11-17T20:56:28+00:00
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
| HfO2 | 5.66 | TBmBJ | missing |
| P2O5 | 5.40 | OptB88vdW | missing |
| Nd2O3 | 5.32 | TBmBJ | 21.4 |
| CaO | 5.29 | TBmBJ | 14.9 |
| Pr2O3 | 5.21 | TBmBJ | 21.6 |
| SrO | 4.96 | TBmBJ | 17.5 |
| MgO | 4.85 | OptB88vdW | missing |
| KO | 4.83 | TBmBJ | 5.8 |
| NdO2 | 4.80 | TBmBJ | 14.1 |
| BeO | 8.04 | OptB88vdW | 7.7 |
| TeO2 | 4.64 | TBmBJ | 28.8 |
| Y2O3 | 4.31 | OptB88vdW | missing |
| RbO | 4.28 | TBmBJ | 6.1 |
| Ta2O5 | 4.27 | TBmBJ | missing |
| Lu2O3 | 4.22 | OptB88vdW | missing |
| Tm2O3 | 4.19 | OptB88vdW | missing |
| Er2O3 | 4.14 | OptB88vdW | missing |
| Ho2O3 | 4.09 | OptB88vdW | missing |
| Dy2O3 | 4.08 | OptB88vdW | missing |
| NaO | 4.07 | TBmBJ | 6.9 |
High κ usually comes with a smaller gap; the app plots this trade-off across all candidates with DFPT κ.

## Listed for review, not ranked (85)
DFT gives these a zero gap, but they contain f-electron or open-shell 3d elements where that is often wrong (D-030). Not ranked; gap unknown. First 25:
Ce2O3, Ce3O, Ce5O9, Ce7O12, CeO, Co2O3, Co5O8, Co7O12, CoO, CoO2, Cr3O, Cr3O2, Cr3O4, Cr3O5, Cr3O7, Cr3O8, CrO, CrO2, CrO7, Cu3O, Cu3O2, Cu3O4, Cu4O3, Cu8O, Cu8O7

## Configuration and filters applied
- Weights: stability 0.35, band_gap 0.3, hazard 0.2, simplicity 0.15, dielectric 0.0
- Filters: min_band_gap=None, max_e_hull=None, max_elements=2, exclude_elements=[], allow_extra_anions=False
- Stability cross-check (Alexandria) enabled: True
- Config file hashes: ranking dc0c5a1dab49, candidates 39061fedf98a, hazards fdfa6b01c897, sources d662beaac648, policy 7fb95e8f8b03, confidence c6b5f9bd9548, output c55f3669d194, terminology 79179a30262d

| Filter step | Formulas |
|---|---|
| formulas | 15671 |
| dropped: contains H, C, N, S or halogen | 4156 |
| dropped: metal (no band gap) | 2119 |
| dropped: element with no stable isotopes | 506 |
| dropped: not an oxide | 1 |
| dropped: more than 2 elements | 8651 |
| needs review (not ranked) | 85 |
| ranked | 153 |

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
| normalise request text | 29 characters in, 29 read; no change | 0.0 |
| policy gate | 0 refusal\(s\)\: \[\]; remainder\: 'oxides. binaries only. top 25' | 0.1 |
| parse request | provider\=rules; matched\=2; unparsed\=\['oxides'\] | 0.1 |
| apply settings and clamp | weights\=\{'stability'\: 0\.35, 'band\_gap'\: 0\.3, 'hazard'\: 0\.2, 'simplicity'\: 0\.15, 'dielectric'\: 0\.0\}; clamped\=\[\] | 0.0 |
| load snapshot | 25194 records; built 2026-11-18T22\:23\:34\+00\:00 | 0.0 |
| candidates and filters | \{'formulas'\: 15671, 'dropped\: contains H, C, N, S or halogen'\: 4156, 'dropped\: metal \(no band gap\)'\: 2119, 'dropped\: element with no stable isotopes'\: 506, 'dropped\: not an oxide'\: 1, 'dropped\: more than 2 elements'\: 8651, 'needs review \(not ranked\)'\: 85, 'ranked'\: 153\} | 100.4 |
| score | 153 candidates scored | 4.3 |
| rank (ties by offline confidence) | shortlist pool 25 of 153 | 1.0 |
| Alexandria cross-check | Al2O3\:unavailable, SiO2\:unavailable, Li2O\:unavailable, B2O3\:unavailable, YbO\:unavailable, HfO2\:unavailable, P2O5\:unavailable, Nd2O3\:unavailable, CaO\:unavailable, Pr2O3\:unavailable, SrO\:unavailable, MgO\:unavailable, KO\:unavailable, NdO2\:unavailable, BeO\:unavailable, TeO2\:unavailable,\.\.. | 1005.8 |
| confidence, caveats, citations | 25 ranked | 2.3 |
