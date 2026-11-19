# Eval 4: face validity (report, not pass/fail)

Settings: default weights, no request filters, rank by suitability then confidence. Weights: {'stability': 0.35, 'band_gap': 0.3, 'hazard': 0.2, 'simplicity': 0.15, 'dielectric': 0.0}.
5369 formulas ranked; 4 share the top score of 1.000. Snapshot built 2026-11-18T22:23:34+00:00.

| Formula | Rank | Suitability | Confidence | Representative | Hull (meV/atom) | Gap (eV) | ICSD |
|---|---|---|---|---|---|---|---|
| HfO2 | 6 of 5369 | 0.975 | High | JVASP-9147 P2_1/c | 0 | 5.66 (TBmBJ) | yes |
| ZrO2 | 474 of 5369 | 0.832 | Low | JVASP-145794 Pbca | 0 | 3.76 (OptB88vdW) | no |
| Al2O3 | 1 of 5369 | 1.000 | High | JVASP-32 R-3c | 0 | 7.57 (TBmBJ) | yes |
| Y2O3 | 288 of 5369 | 0.873 | Medium | JVASP-20793 Ia-3 | 0 | 4.31 (OptB88vdW) | yes |
| SiO2 | 2 of 5369 | 1.000 | High | JVASP-41 P3_221 | 0 | 8.10 (TBmBJ) | yes |
| La2O3 | 434 of 5369 | 0.841 | Low | JVASP-154699 P-3m1 | 0 | 3.88 (OptB88vdW) | no |

## Why each one lands where it does

- **HfO2**: Loses 0.025 on band gap (total 0.975). Confidence High (points: 5).
- **ZrO2**: Loses 0.168 on band gap (total 0.832). Representative JVASP-145794 has no TBmBJ gap, so the OptB88vdW fallback (3.76 eV) is scored; the lowest-energy polymorph that has one, JVASP-113 (P2_1/c, 3 meV/atom above hull), has TBmBJ 4.21 eV. Representative JVASP-145794 (Pbca) has no ICSD reference; JVASP-113 (P2_1/c) is 3 meV/atom higher and has one. Confidence Low (points: 1).
- **Al2O3**: Scores the maximum suitability (1.000) along with 3 others. Confidence High (points: 5).
- **Y2O3**: Loses 0.127 on band gap (total 0.873). Representative JVASP-20793 has no TBmBJ gap, so the OptB88vdW fallback (4.31 eV) is scored; the lowest-energy polymorph that has one, JVASP-57843 (C2/m, 28 meV/atom above hull), has TBmBJ 5.25 eV. Confidence Medium (points: 3).
- **SiO2**: Scores the maximum suitability (1.000) along with 3 others. Confidence High (points: 5).
- **La2O3**: Loses 0.159 on band gap (total 0.841). Representative JVASP-154699 has no TBmBJ gap, so the OptB88vdW fallback (3.88 eV) is scored. Confidence Low (points: 1).

Weights were not changed to move any of these. A low rank is reported as a finding.
