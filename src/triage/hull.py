"""Energy above the convex hull, recomputed from formation energies (D-013).

For a target entry: find the lowest-energy mix of entries in its chemical system (and all subsystems)
with exactly the target's composition. Energy above hull = target energy - that minimum.
Pure elements are added as virtual references at 0 eV/atom, the definition of formation energy.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass, field

import numpy as np
from scipy.optimize import linprog

ROUND = 6  # composition key precision


@dataclass(frozen=True)
class Entry:
    id: str
    composition: dict[str, float]  # fractional, sums to 1
    energy: float  # formation energy, eV/atom


@dataclass
class HullResult:
    e_hull: float
    n_compositions: (
        int  # competing compositions in the phase table (incl. elements), excl. target's
    )
    decomposition: list[str] = field(default_factory=list)  # ids of the lowest-energy mix


class HullBuilder:
    def __init__(self, entries: list[Entry]):
        self._by_system: dict[frozenset[str], list[Entry]] = {}
        for e in entries:
            self._by_system.setdefault(frozenset(e.composition), []).append(e)
        self._tables: dict[frozenset[str], tuple[list[str], dict[tuple, Entry]]] = {}

    def _table(self, system: frozenset[str]) -> tuple[list[str], dict[tuple, Entry]]:
        """Lowest-energy entry per composition across the system and its subsystems."""
        if system in self._tables:
            return self._tables[system]
        els = sorted(system)
        best: dict[tuple, Entry] = {}
        for el in els:  # virtual elemental references at 0
            key = tuple(1.0 if e == el else 0.0 for e in els)
            best[key] = Entry(id=f"element:{el}", composition={el: 1.0}, energy=0.0)
        for k in range(1, len(els) + 1):
            for sub in itertools.combinations(els, k):
                for e in self._by_system.get(frozenset(sub), []):
                    key = tuple(round(e.composition.get(x, 0.0), ROUND) for x in els)
                    if key not in best or e.energy < best[key].energy:
                        best[key] = e
        self._tables[system] = (els, best)
        return els, best

    def e_hull(self, target: Entry) -> HullResult:
        els, best = self._table(frozenset(target.composition))
        phases = list(best.values())
        a_eq = np.array([[p.composition.get(el, 0.0) for p in phases] for el in els])
        b_eq = np.array([target.composition.get(el, 0.0) for el in els])
        cost = np.array([p.energy for p in phases])
        res = linprog(cost, A_eq=a_eq, b_eq=b_eq, bounds=(0, None), method="highs")
        if not res.success:
            raise RuntimeError(f"hull LP failed for {target.id}: {res.message}")
        e_above = max(0.0, target.energy - float(res.fun))
        target_key = tuple(round(target.composition.get(x, 0.0), ROUND) for x in els)
        n_comp = len(best) - (1 if target_key in best else 0)
        decomp = [p.id for p, x in zip(phases, res.x) if x > 1e-6]
        return HullResult(e_hull=e_above, n_compositions=n_comp, decomposition=sorted(decomp))
