"""Check whether JARVIS `ehull` is usable as an absolute stability metric for oxides."""
import sys, collections, statistics
from jarvis.db.figshare import data
d = data("dft_3d", store_dir=sys.argv[1])
ox = [x for x in d if "O" in x["atoms"]["elements"]]
eh = sorted(x["ehull"] for x in ox)
q = lambda p: eh[int(p * (len(eh) - 1))]
print("oxide ehull quantiles min/1%/10%/50%/90%/max:", [q(p) for p in (0, .01, .1, .5, .9, 1)])
for t in (0.0, 0.025, 0.1, 0.5, 1.0):
    print(f"  oxides with ehull <= {t}: {sum(e <= t for e in eh)}")
alle = [x["ehull"] for x in d]
print("ALL records ehull<=0:", sum(e <= 0 for e in alle), " <=0.1:", sum(e <= 0.1 for e in alle), "of", len(alle))
low = sorted(ox, key=lambda x: x["ehull"])[:12]
print("lowest-ehull oxides:", [(x["jid"], x["formula"], x["ehull"], x["formation_energy_peratom"]) for x in low])
nel = collections.defaultdict(list)
for x in d: nel[len(set(x["atoms"]["elements"]))].append(x["ehull"])
for k in sorted(nel): print(f"  n_elements={k}: n={len(nel[k])} median ehull={statistics.median(nel[k]):.3f} min={min(nel[k]):.3f} frac<=0.1={sum(e<=0.1 for e in nel[k])/len(nel[k]):.2f}")
print("known ground states (jid, formula, spg, ehull, Ef/atom, ref):")
for j in ["JVASP-9147", "JVASP-113", "JVASP-32", "JVASP-58349", "JVASP-20793"]:
    x = next(x for x in d if x["jid"] == j)
    print("  ", j, x["formula"], x["spg_symbol"], x["ehull"], x["formation_energy_peratom"], x["reference"])
# within-formula relative energy: does min-ehull polymorph == min formation energy polymorph?
by = collections.defaultdict(list)
for x in ox: by[x["formula"]].append(x)
multi = {f: v for f, v in by.items() if len(v) > 1}
agree = sum(min(v, key=lambda x: x["ehull"])["jid"] == min(v, key=lambda x: x["formation_energy_peratom"])["jid"] for v in multi.values())
print(f"unique oxide formulas: {len(by)}; multi-polymorph: {len(multi)}; argmin(ehull)==argmin(Ef): {agree}")
# is ehull - (Ef - min Ef within formula) constant per formula? i.e. ehull = offset + relative energy
import random; random.seed(0)
for f in ["HfO2", "SiO2", "Al2O3", "TiO2"]:
    v = by[f]; m = min(x["formation_energy_peratom"] for x in v)
    offs = [round(x["ehull"] - (x["formation_energy_peratom"] - m), 3) for x in v]
    print(f"  {f}: n={len(v)} offset(ehull - dEf) min/max = {min(offs)}/{max(offs)}; min Ef={m}")
# binary oxides: offset vs oxygen fraction
print("binary-oxide ground states: formula, x_O, ehull_min")
for f in ["MgO", "CaO", "Li2O", "TiO2", "SiO2", "Al2O3", "HfO2", "ZnO", "Ta2O5", "WO3", "SrTiO3", "BaTiO3", "LaAlO3"]:
    if f in by:
        g = min(by[f], key=lambda x: x["ehull"]); el = g["atoms"]["elements"]
        print(f"  {f}: xO={el.count('O')/len(el):.3f} ehull={g['ehull']} Ef={g['formation_energy_peratom']}")
