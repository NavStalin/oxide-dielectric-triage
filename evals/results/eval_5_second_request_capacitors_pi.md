# Oxide dielectric triage: PI summary

**Request:** High-k oxides for capacitors. I can accept a smaller band gap and ternaries are fine.

| # | Formula | Suitability | Evidence confidence | Why | Key caveat | Sources |
|---|---|---|---|---|---|---|
| 1 | NaSmO2 | 0.972 | Medium | Strongest: on the convex hull; dielectric constant 32.8. | Contains Sm: DFT energies and gaps are less reliable for these elements, so stability and gap may be wrong. | [JVASP-50889](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-50889.html), [jdft_3d-9-24-2025.json](https://doi.org/10.6084/m9.figshare.6815699) |
| 2 | LuTaO4 | 0.961 | High | Strongest: on the convex hull; dielectric constant 276.9. | DFPT dielectric constant 277 is unusually large (above 100); often a sign of a soft polar mode near an instability. Treat κ with caution. | [JVASP-4492](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-4492.html), [jdft_3d-9-24-2025.json](https://doi.org/10.6084/m9.figshare.6815699) |
| 3 | NaPrO2 | 0.957 | High | Strongest: on the convex hull; dielectric constant 31.1. | Contains Pr: DFT energies and gaps are less reliable for these elements, so stability and gap may be wrong. | [JVASP-2829](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-2829.html), [jdft_3d-9-24-2025.json](https://doi.org/10.6084/m9.figshare.6815699) |
| 4 | TeO2 | 0.949 | High | Strongest: on the convex hull; dielectric constant 28.8. | Stability not cross-checked: OQMD cross-check disabled. | [JVASP-57128](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-57128.html), [jdft_3d-9-24-2025.json](https://doi.org/10.6084/m9.figshare.6815699) |
| 5 | SnB4O7 | 0.947 | High | Strongest: on the convex hull; dielectric constant 27.8. | Stability not cross-checked: OQMD cross-check disabled. | [JVASP-49166](https://www.ctcms.nist.gov/~knc6/jsmol/JVASP-49166.html), [jdft_3d-9-24-2025.json](https://doi.org/10.6084/m9.figshare.6815699) |

16 more formulas are listed for review, not ranked: DFT gives them zero gap, but for their elements that is unreliable. Listed in the audit view.

**Caveats (always shown)**
- Values are DFT calculations for perfect bulk crystals, not measurements on thin films. Many deposited films are amorphous or strained.
- DFT band gaps are approximate; the OptB88vdW fallback usually underestimates the gap.
- Energy above hull is thermodynamic stability at 0 K, recomputed from JARVIS formation energies. It says nothing about kinetics, deposition conditions or reactions with the substrate.
- Hazard flags are element-level (RoHS, IARC). They are not compound toxicology and do not assess oxidation state or exposure route.
- This is a triage shortlist to support a scientist's judgment. It is not a recommendation to run any experiment.

<sub>Data: JARVIS-DFT (NIST), file jdft_3d-9-24-2025.json, retrieved 2026-11-17T20:56:28+00:00; snapshot built 2026-11-18T22:23:34+00:00. Ranked by suitability; ties broken by evidence confidence. Parser: rules.</sub>
