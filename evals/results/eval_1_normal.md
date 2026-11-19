# Eval 1: normal

Request: "Find promising oxide dielectric candidates for thin-film experiments. Prefer thermodynamically stable materials, wide band gaps, non-toxic elements, simple compositions, and public evidence. Return a ranked shortlist with caveats."

Parser: rules. OQMD: offline. Run at 2026-11-19T19:13:02+00:00.

## Expected

- Every ranked formula contains O and no excluded anion or element.
- Every candidate has at least one citation, and every citation URL is on an allowlisted host.
- Both views (PI summary, audit view) render, with the standing caveats.
- At least one missing field is shown as missing, not as a number.
- Every number in the PI summary traces to a stored value or a computed score.

## Checks

| Check | Result | Detail |
|---|---|---|
| oxides only, no excluded element | PASS | violations: [] |
| every candidate cited on an allowlisted host | PASS | bad URLs: []; uncited: [] |
| both views render with standing caveats | PASS | pi 3143 chars, audit 18182 chars |
| missing data shown as missing | PASS | 'missing' appears 19 times in the audit view |
| every PI-summary number traces to data | PASS | untraceable: [] |

## What the parser understood

- 'Find promising oxide dielectric candidates for thin-film experiments' -> scope: oxide dielectric triage (default)
- 'Find promising oxide dielectric candidates for thin-film experiments' -> thin-film context: film caveats included (always on)
- 'Prefer thermodynamically stable materials' -> stability preference (default weight)
- 'wide band gaps' -> wide band gap preference (default weight)
- 'non-toxic elements' -> hazard preference (default weight)
- 'simple compositions' -> simplicity preference (default weight)
- 'and public evidence' -> public evidence and citations (always on)
- 'Return a ranked shortlist with caveats' -> caveats (always on)
- 'Return a ranked shortlist with caveats' -> ranked shortlist (default)

Full outputs: `eval_1_normal_pi.md`, `eval_1_normal_audit.md`.
