"""Print real JARVIS dft_3d field names and coverage for oxides. Evidence for DECISIONS.md."""
import sys, collections
from jarvis.db.figshare import data, get_db_info

store = sys.argv[1] if len(sys.argv) > 1 else "data/raw"
info = get_db_info()["dft_3d"]
print("DB_INFO:", info)
d = data("dft_3d", store_dir=store)
print("N records:", len(d))
print("FIELDS:", sorted(d[0].keys()))
e = d[0]
print("SAMPLE:", {k: (v if not isinstance(v, (dict, list)) else type(v).__name__) for k, v in e.items()})

def has(v):
    return v not in ("na", None, "", [])

ox = [x for x in d if "O" in x["atoms"]["elements"]]
print("N with O:", len(ox))
keys = ["mbj_bandgap", "optb88vdw_bandgap", "hse_gap", "ehull", "formation_energy_peratom",
        "icsd", "epsx", "epsy", "epsz", "mepsx", "dfpt_piezo_max_dielectric",
        "dfpt_piezo_max_dielectric_electronic", "dfpt_piezo_max_dielectric_ionic",
        "spg_symbol", "spg_number", "formula", "jid", "reference", "search", "dimensionality", "nat", "func"]
for k in keys:
    if k not in d[0]:
        print(f"  {k}: FIELD ABSENT"); continue
    n = sum(has(x[k]) for x in ox)
    print(f"  {k}: {n}/{len(ox)} present; example={next((x[k] for x in ox if has(x[k])), None)!r}")
print("icsd value types:", collections.Counter(type(x.get("icsd")).__name__ for x in ox).most_common(4))
for f in ["HfO2", "ZrO2", "Al2O3", "Y2O3", "SiO2", "La2O3"]:
    rows = sorted((x for x in d if x["formula"] == f), key=lambda x: x["ehull"] if has(x["ehull"]) else 9)
    print(f, len(rows), [(x["jid"], x["spg_symbol"], x["ehull"], x["mbj_bandgap"], x["optb88vdw_bandgap"], x.get("icsd")) for x in rows[:3]])
