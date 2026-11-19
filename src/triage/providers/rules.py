"""Default provider: keyword and regex rules. Deterministic, no network, no key.

Starts from the site's default weights and adjusts only for phrases it recognises. Every phrase it
uses is recorded in `matched` with its effect; clauses it can't use go to `unparsed`, shown to the user.
"""

from __future__ import annotations

import re

from triage.models import Criteria
from triage.policy import split_clauses

ELEMENT_NAMES = {
    "lead": "Pb",
    "cadmium": "Cd",
    "mercury": "Hg",
    "arsenic": "As",
    "chromium": "Cr",
    "nickel": "Ni",
    "beryllium": "Be",
    "cobalt": "Co",
    "lanthanum": "La",
    "hafnium": "Hf",
}
SYMBOL = r"[A-Z][a-z]?"


class RulesProvider:
    name = "rules"

    def parse(self, text: str, default_weights: dict[str, float]) -> Criteria:
        c = Criteria(weights=dict(default_weights), provider=self.name)
        for clause in split_clauses(text):
            hits = self._clause(clause, c)
            if not hits:
                c.unparsed.append(clause)
            c.matched.extend(hits)
        return c

    def _clause(self, s: str, c: Criteria) -> list[str]:
        low = s.lower()
        hits: list[str] = []

        def hit(msg: str) -> None:
            hits.append(f"'{s}' -> {msg}")

        # scope words: understood, no change (pure oxides and dielectric triage are the tool's scope)
        if re.search(
            r"\b(oxides?|dielectrics?|insulators?|candidates?|materials?)\b", low
        ) and re.search(r"\b(find|search|identify|list|suggest|show|give|promising)\b", low):
            hit("scope: oxide dielectric triage (default)")
        if re.search(r"\bthin[- ]?films?\b", low):
            hit("thin-film context: film caveats included (always on)")

        # stability
        m = re.search(r"(?:hull|e_?hull)[^0-9]{0,25}(\d+(?:\.\d+)?)\s*mev", low) or re.search(
            r"(\d+(?:\.\d+)?)\s*mev(?:/atom)?\s*(?:of|from|above)?\s*(?:the\s+)?hull", low
        )
        if m:
            c.max_e_hull = float(m.group(1)) / 1000
            hit(f"filter: energy above hull <= {m.group(1)} meV/atom")
        elif re.search(r"\b(thermodynamically )?stable\b|\bstability\b", low):
            hit("stability preference (default weight)")

        # band gap
        m = re.search(r"(?:band ?gaps?|gaps?)[^0-9]{0,25}(\d+(?:\.\d+)?)\s*ev", low)
        if m and re.search(r"(above|over|at least|>=?|greater|more than|min)", low):
            c.min_band_gap = float(m.group(1))
            hit(f"filter: band gap >= {m.group(1)} eV")
        elif re.search(
            r"(accept|ok with|fine with|tolerate|allow).{0,20}(smaller|lower|narrower).{0,10}gap"
            r"|(smaller|lower) (band )?gaps? (is|are) (fine|ok|acceptable)",
            low,
        ):
            c.weights["band_gap"] = 0.15
            hit("band gap weight lowered to 0.15")
        elif re.search(r"\b(wide|large|big|high)\b.{0,10}\b(band ?)?gaps?\b", low):
            hit("wide band gap preference (default weight)")

        # dielectric constant
        if re.search(
            r"high[- ]?(k|κ|kappa)\b|high (dielectric|permittivity)|capacitors?\b|dielectric constant",
            low,
        ):
            c.weights["dielectric"] = 0.25
            hit("dielectric constant criterion on (weight 0.25)")

        # hazards
        if re.search(r"\bnon[- ]?toxic|low[- ]toxicity|safe elements|avoid toxic|hazard", low):
            hit("hazard preference (default weight)")
        for word, sym in ELEMENT_NAMES.items():
            if re.search(
                rf"\b(no|without|avoid|exclude|free of)\b.{{0,15}}\b{word}\b|\b{word}[- ]free\b",
                low,
            ):
                c.exclude_elements.append(sym)
                hit(f"exclude element {sym}")
        for sym in re.findall(rf"\b(?:no|without|exclude|avoid)\s+({SYMBOL})\b", s):
            if sym not in c.exclude_elements and sym[0].isupper() and sym not in {"I", "A"}:
                c.exclude_elements.append(sym)
                hit(f"exclude element {sym}")

        # composition
        if re.search(r"\bbinar(y|ies)( oxides?)? only\b|\bonly binar", low):
            c.max_elements = 2
            hit("filter: binary compounds only")
        elif re.search(
            r"\bternar(y|ies)\b.{0,15}\b(fine|ok|okay|acceptable|allowed|welcome)\b", low
        ):
            c.weights["simplicity"] = 0.05
            hit("simplicity weight lowered to 0.05 (ternaries fine)")
        elif re.search(
            r"\bsimple (compositions?|chemistr(y|ies)|oxides?)\b|\bsimplicity\b|\bfew(er)? elements\b",
            low,
        ):
            hit("simplicity preference (default weight)")
        if re.search(
            r"\b(hydroxides?|nitrides?|oxynitrides?|carbonates?|halides?|sulfates?)\b", low
        ):
            c.allow_extra_anions = True
            hit("request to include non-oxide anions (subject to admin policy)")

        # evidence and output
        if re.search(r"\bpublic (evidence|data|sources)|\bcit(ed|ations?)\b|\bsources?\b", low):
            hit("public evidence and citations (always on)")
        if re.search(r"\bcaveats?\b", low):
            hit("caveats (always on)")
        m = re.search(
            r"\btop[- ](\d+)\b|\b(\d+) (candidates|materials|options)\b|\bshortlist of (\d+)\b", low
        )
        if m:
            c.shortlist_size = int(next(g for g in m.groups() if g))
            hit(f"shortlist size {c.shortlist_size}")
        elif re.search(r"\b(ranked|shortlist|rank)\b", low):
            hit("ranked shortlist (default)")
        if re.search(r"\b(pi summary|summary|brief|concise|short)\b", low):
            c.style = "pi"
            hit("style: PI summary")
        if re.search(r"\b(detailed|audit|technical|full|in depth)\b", low):
            c.style = "audit"
            hit("style: audit view")
        return hits
