# Oxide dielectric triage: PI summary

**Request:** oxides, binaries only, top 25

> Alexandria cross-check failed: Alexandria unreachable (ConnectionError). Affected candidates are marked; no Alexandria values shown.

| # | Formula | Suitability | Evidence confidence | Why | Key caveat | Sources |
|---|---|---|---|---|---|---|
| 1 (tie) | Al2O3 | 1.000 | High | Strongest: on the convex hull; band gap 7.57 eV (TBmBJ). | Stability not cross-checked: Alexandria unreachable (ConnectionError). | [JVASP-32](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-32.html), [jdft_3d-9-24-2025.json](https://doi.org/10.6084/m9.figshare.6815699) |
| 2 (tie) | SiO2 | 1.000 | High | Strongest: on the convex hull; band gap 8.10 eV (TBmBJ). | Compound-form hazard not captured by element flags: IARC 'Silica dust, crystalline, in the form of quartz or cristobalite'. Group 1 as respirable crystalline dust. Si is not flagged at element level. | [JVASP-41](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-41.html), [jdft_3d-9-24-2025.json](https://doi.org/10.6084/m9.figshare.6815699) |
| 3 (tie) | Li2O | 1.000 | Medium | Strongest: on the convex hull; band gap 7.59 eV (TBmBJ). | No ICSD experimental structure reference found for this polymorph. | [JVASP-118614](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-118614.html), [jdft_3d-9-24-2025.json](https://doi.org/10.6084/m9.figshare.6815699) |
| 4 (tie) | B2O3 | 1.000 | Low | Strongest: on the convex hull; band gap 6.54 eV (OptB88vdW). | Band gap is the OptB88vdW fallback (no TBmBJ value): probably an underestimate. | [JVASP-152827](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-152827.html), [jdft_3d-9-24-2025.json](https://doi.org/10.6084/m9.figshare.6815699) |
| 5 | YbO | 0.985 | High | Strongest: on the convex hull; band gap 5.80 eV (TBmBJ). | Contains Yb: DFT energies and gaps are less reliable for these elements, so stability and gap may be wrong. | [JVASP-1291](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-1291.html), [jdft_3d-9-24-2025.json](https://doi.org/10.6084/m9.figshare.6815699) |

85 more formulas are listed for review, not ranked: DFT gives them zero gap, but for their elements that is unreliable. Listed in the audit view.

**Caveats (always shown)**
- Values are DFT calculations for perfect bulk crystals, not measurements on thin films. Many deposited films are amorphous or strained.
- DFT band gaps are approximate; the OptB88vdW fallback usually underestimates the gap.
- Energy above hull is thermodynamic stability at 0 K, recomputed from JARVIS formation energies. It says nothing about kinetics, deposition conditions or reactions with the substrate.
- Hazard flags are element-level (RoHS, IARC). They are not compound toxicology and do not assess oxidation state or exposure route.
- This is a triage shortlist to support a scientist's judgment. It is not a recommendation to run any experiment.

<sub>Data: JARVIS-DFT (NIST), file jdft_3d-9-24-2025.json, retrieved 2026-11-17T20:56:28+00:00; snapshot built 2026-11-18T22:23:34+00:00. Ranked by suitability; ties broken by evidence confidence. Parser: rules.</sub>
