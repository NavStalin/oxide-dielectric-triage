# Verified facts (checked live on 2026-11-17)

Everything here was observed by running code or fetching a page, not recalled. Re-run the
scripts in `scripts/` to reproduce. Where something was not verified, it says so.

## 1. JARVIS-DFT `dft_3d`

Reproduce: `uv run python scripts/inspect_jarvis.py data/raw`

| Item | Value |
|---|---|
| Loader | `jarvis.db.figshare.data("dft_3d", store_dir="data/raw")` |
| File | `jdft_3d-9-24-2025.json` (46 MB zip, cached in `data/raw/`, git-ignored) |
| Figshare file URL | `https://ndownloader.figshare.com/files/64391379` |
| Dataset DOI | `https://doi.org/10.6084/m9.figshare.6815699` |
| Paper DOI given by the loader | `https://doi.org/10.1016/j.commatsci.2025.114063` |
| Records | 93,902 total; 25,194 contain O; 15,671 unique O-containing formulas |
| Per-record page | `https://www.ctcms.nist.gov/~knc6/static/JARVIS-DFT/<jid>.xml` (HTTP 200 for JVASP-9147) |

`jarvis.db.figshare.get_db_info()["dft_3d"]` returns the file URL, filename and DOIs. Read the
manifest values from it at snapshot time; don't hard-code them.

### Fields we use (real names, confirmed)

| Field | Type and meaning | Present in O-containing records |
|---|---|---|
| `jid` | `"JVASP-9147"` | 100% |
| `formula` | reduced formula string, e.g. `"HfO2"`, `"SrTiO3"` | 100% |
| `atoms` | dict; `atoms["elements"]` is the per-site element list | 100% |
| `spg_symbol`, `spg_number` | `"P2_1/c"`, `"14"` (number is a **string**) | 100% |
| `formation_energy_peratom` | float, eV/atom, OptB88vdW | 100% |
| `ehull` | float, **do not use, see section 2** | 100% |
| `optb88vdw_bandgap` | float, eV | 100% |
| `mbj_bandgap` | float eV, or `"na"` | **5,174 / 25,194 (20.5%)** |
| `hse_gap` | float eV, or `"na"` | 13 (ignore) |
| `icsd` | comma-separated string of ICSD IDs, `""` when none | 6,325 (25%) |
| `dfpt_piezo_max_dielectric` | float (total κ, max component), or `"na"` | 1,734 (6.9%) |
| `dfpt_piezo_max_dielectric_electronic` / `_ionic` | float or `"na"` | 1,770 |
| `epsx`, `epsy`, `epsz` | OptB88vdW optical (electronic-only) dielectric; **not** static κ | 14,273 |
| `dimensionality` | `"3D-bulk"`, `"intercalated ion"`, others, or `"na"` | 25,042 |
| `reference` | origin structure ID, e.g. `"mp-352"` | 100% |
| `func` | `"OptB88vdW"` | 100% |

Gotchas:
- Missing is the **string `"na"`** (and `""` for `icsd`), not `None`. Map both to `None` in the adapter.
- `mbj_bandgap == 0.0` is a real value (a metal), not missing.
- The brief's guesses `mbj_bandgap`, `optb88vdw_bandgap` and `ehull` are all real field names.

### Face-validity materials, as they sit in the raw data

Lowest formation-energy polymorph per formula (jid, space group, TBmBJ gap, OptB88vdW gap, has ICSD):

| Formula | Polymorphs | Lowest-energy entry | TBmBJ | OptB88vdW | ICSD |
|---|---|---|---|---|---|
| HfO2 | 13 | JVASP-9147, P2_1/c | 5.664 | 4.123 | yes |
| ZrO2 | 16 | JVASP-145794, Pbca (P2_1/c JVASP-113 is 3 meV higher) | `na` (JVASP-113: 4.213) | 3.759 | no (JVASP-113: yes) |
| Al2O3 | 14 | JVASP-32, R-3c | 7.571 | 6.430 | yes |
| Y2O3 | 6 | JVASP-20793, Ia-3 | **`na`** | 4.307 | yes |
| SiO2 | 94 | JVASP-41 / JVASP-58349, quartz | 8.097 | 5.985 | yes |
| La2O3 | 4 | JVASP-154699, P-3m1 | **`na` for all 4** | 3.876 | no |

So with the brief's rules as written, Y2O3 and La2O3 get the fallback gap and lower confidence,
and ZrO2's representative is an un-ICSD'd Pbca cell instead of the familiar monoclinic phase.
These are findings for the talk, not bugs to hide.

## 2. The JARVIS `ehull` field cannot be used as an absolute stability metric

Reproduce: `uv run python scripts/inspect_ehull.py data/raw`

Observed:
- Known ground states have huge values: HfO2 P2_1/c **1.778**, Al2O3 corundum **1.596**,
  SiO2 quartz **1.385**, Y2O3 **2.007**, Ta2O5 **3.719**, SrTiO3 **1.551** eV/atom.
- Only 328 of 25,194 O-containing records have `ehull <= 0.1`. The median is 2.21 eV/atom.
- MgO, CaO, ZnO, SrO are at 0. The offset is not constant within a formula either
  (HfO2: `ehull - ΔE_f` ranges from -1.81 to +1.78), so subtracting a per-formula constant doesn't rescue it.
- `formation_energy_peratom` is sound: HfO2 -3.810, Al2O3 -3.313, SiO2 -2.901 eV/atom, in line
  with OQMD (HfO2 P21/c `delta_e` -3.839) and experiment.

With the brief's scoring (0 at ≥ 100 meV/atom) every classic dielectric would score 0 on stability.
I have not found the cause; it's reported here as an observation.

### Recomputed hull works

Reproduce: `uv run python scripts/prototype_hull.py data/raw`

Energy above hull recomputed by linear programming over all JARVIS entries in the chemical system
(using `formation_energy_peratom`, elements at 0):

| Formula | Lowest polymorph | JARVIS `ehull` | Recomputed | Competing compositions |
|---|---|---|---|---|
| HfO2 | P2_1/c | 1.778 | 0 meV (next: Pbca +10, +12) | 9 |
| ZrO2 | Pbca | 1.467 | 0 meV (P2_1/c +3) | 9 |
| Al2O3 | R-3c | 1.596 | 0 meV (C2/m +17) | 10 |
| Y2O3 | Ia-3 | 2.007 | 0 meV | 5 |
| SiO2 | quartz | 1.385 | 0 meV | 9 |
| La2O3 | P-3m1 | 1.709 | 0 meV | 9 |
| Ta2O5 | C2/c | 3.719 | 0 meV | 10 |
| SrTiO3 | I4/mcm | 1.551 | 0 meV (Pm-3m +1) | 37 |
| HfSiO4 | I4_1/amd | 2.808 | 0 meV | 25 |

One oddity to carry as a caveat: for MgO, JARVIS has an I4/mmm entry (JVASP-115229, no ICSD) 30 meV
below rock salt (JVASP-116). A lowest-energy entry is not always the phase people grow.

## 3. OQMD REST API

Checked: `GET https://oqmd.org/oqmdapi/formationenergy?composition=HfO2&limit=3&format=json` returned
HTTP 200, no key, 24 entries available for HfO2.

- Response shape: `{"links": {"next": ...}, "data": [...], "meta": {"data_available": 24, "more_data_available": true, ...}}`.
  It paginates; follow `links.next` or set `limit`.
- Fields confirmed on each entry: `name`, `entry_id`, `calculation_id`, `icsd_id` (int), `formationenergy_id`,
  `duplicate_entry_id`, `composition` (`"Hf1 O2"`), `composition_generic`, `prototype`, `spacegroup` (`"P21/c"`),
  `volume`, `ntypes`, `natoms`, `unit_cell`, `sites`, `band_gap`, `delta_e` (eV/atom), `stability` (eV/atom),
  `fit`, `calculation_label`.
- `fields=` works to trim the payload.
- HfO2 values: P21/c entry 5299 `stability` 0.0079, ICSD 27313; P42/nmc entry 22054 `stability` 0.0610.
- Space-group notation differs: JARVIS `P2_1/c` vs OQMD `P21/c`. Strip underscores before comparing.
- API docs: `https://static.oqmd.org/static/docs/restful.html` (HTTP 200).
- **Not verified:** the human-readable entry page `https://oqmd.org/materials/entry/<entry_id>` timed out
  at 25 s. Until it's confirmed, cite the API query URL that produced the value. The site is slow, so
  use timeouts and cache responses.

### OQMD update (2026-11-18)

- `sort_by=stability` is a documented parameter (API docs page); used with `limit=50`.
- SiO2 query returned 204 entries, all named `SiO2`; lowest stability 0.0 (I-42d).
- SrTiO3 and Y2O3 queries, and later HfO2, returned **HTTP 502** ("temporary error, try again in
  30 seconds") repeatedly through the afternoon. Treat OQMD as unreliable; the app must work without it.
- 2026-11-19: still failing (HTTP 502 and timeouts on three full runs about 40 s apart).

## 4. Hazard sources (URLs resolve; list contents not yet read line by line)

| Source | URL | Status |
|---|---|---|
| RoHS Directive 2011/65/EU | `https://eur-lex.europa.eu/eli/dir/2011/65/oj` | 200 |
| RoHS consolidated text (2025-01-01) | `https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02011L0065-20250101` | 200 |
| Delegated Directive (EU) 2015/863, which replaced Annex II | `https://eur-lex.europa.eu/eli/dir_del/2015/863/oj` | 200 |
| IARC agents classified | `https://monographs.iarc.who.int/agents-classified-by-the-iarc/` | 200 |
| IARC list of classifications | `https://monographs.iarc.who.int/list-of-classifications` | 200 |

A search summary of 2015/863 reports Annex II limits of lead 0.1%, mercury 0.1%, cadmium 0.01% and
hexavalent chromium 0.1% by weight. **Before writing `config/hazards.yaml`, open the Annex II text and the
IARC list and confirm each entry (As, Be, Cd, Cr(VI), Ni compounds) word for word.** Record the page's
"last updated" date in the YAML.

## 5. Environment

- `~/lila-triage`, git initialised on `main`, nothing committed yet.
- Python 3.12 via `uv` (`.python-version`), `src/` layout, package `triage`.
- Installed: jarvis-tools, pydantic 2.14, pandas, pyarrow, scipy, numpy, pyyaml, jinja2, typer, requests,
  streamlit 1.67, plotly; dev: pytest, ruff, responses.
- `make setup | snapshot | test | lint | app | evals | check`.
- `pytest` deselects tests marked `network` by default.
