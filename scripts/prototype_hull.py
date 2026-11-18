"""Prototype: recompute energy above hull from JARVIS formation_energy_peratom via LP. De-risking only."""
import sys, collections, itertools
import numpy as np
from scipy.optimize import linprog
from jarvis.db.figshare import data
d = data("dft_3d", store_dir=sys.argv[1])

def comp(x):
    c = collections.Counter(x["atoms"]["elements"]); n = sum(c.values())
    return {k: v / n for k, v in c.items()}
recs = [(x["jid"], x["formula"], comp(x), x["formation_energy_peratom"], x["ehull"], x["spg_symbol"]) for x in d
        if isinstance(x["formation_energy_peratom"], (int, float))]
bysys = collections.defaultdict(list)
for r in recs: bysys[frozenset(r[2])].append(r)

def ehull(target, exclude_self=False):
    els = sorted(target[2]); pool = []
    for k in range(1, len(els) + 1):
        for s in itertools.combinations(els, k): pool += bysys.get(frozenset(s), [])
    # keep lowest-energy entry per composition
    best = {}
    for r in pool:
        key = tuple(round(r[2].get(e, 0), 6) for e in els)
        if key not in best or r[3] < best[key][3]: best[key] = r
    pts = list(best.values())
    A = np.array([[r[2].get(e, 0) for r in pts] + [1 if e == el else 0 for el in els] for e in els])  # + elemental refs at Ef=0
    cost = np.array([min(r[3], 0) if len(r[2]) == 1 else r[3] for r in pts] + [0.0] * len(els))
    b = np.array([target[2].get(e, 0) for e in els])
    res = linprog(cost, A_eq=A, b_eq=b, bounds=(0, None), method="highs")
    return target[3] - res.fun, len(pts)

for f in ["HfO2", "ZrO2", "Al2O3", "Y2O3", "SiO2", "La2O3", "TiO2", "Ta2O5", "MgO", "SrTiO3", "BaTiO3", "LaAlO3", "HfSiO4"]:
    rows = sorted((r for r in recs if r[1] == f), key=lambda r: r[3])[:3]
    out = []
    for r in rows:
        e, n = ehull(r); out.append((r[0], r[5], f"jarvis_field={r[4]}", f"recomputed={e*1000:.0f} meV", f"hull_pts={n}"))
    print(f, out)
