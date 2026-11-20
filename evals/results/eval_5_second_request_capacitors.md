# Eval 5: second request capacitors

Request: "High-k oxides for capacitors. I can accept a smaller band gap and ternaries are fine."

Parser: rules. Cross-check: offline. Run at 2026-11-20T22:03:53+00:00.

## Expected

- The parser turns the dielectric criterion on and lowers the band-gap and simplicity weights.
- The shortlist differs from eval 1.
- Every shortlisted candidate with a dielectric score shows its DFPT κ with a citation.
- No code change between eval 1 and eval 5; only the request text differs.

## Checks

| Check | Result | Detail |
|---|---|---|
| dielectric criterion turned on | PASS | 0.0 -> 0.25 |
| band-gap weight lowered | PASS | 0.3 -> 0.15 |
| simplicity weight lowered | PASS | 0.15 -> 0.05 |
| shortlist differs from eval 1 | PASS | eval 1 ['Al2O3', 'SiO2', 'Li2O', 'B2O3', 'YbO'] / eval 5 ['NaSmO2', 'LuTaO4', 'NaPrO2', 'TeO2', 'SnB4O7'] |
| every shortlisted candidate has a cited κ | PASS | NaSmO2 κ=32.8; LuTaO4 κ=276.9; NaPrO2 κ=31.1; TeO2 κ=28.8; SnB4O7 κ=27.8 |
| no-κ candidates dropped and counted | PASS | {'dropped: no dielectric data (criterion turned on by request)': 8430} |

## What the parser understood

- 'High-k oxides for capacitors' -> dielectric constant criterion on (weight 0.25)
- 'I can accept a smaller band gap' -> band gap weight lowered to 0.15
- 'ternaries are fine' -> simplicity weight lowered to 0.05 (ternaries fine)

Full outputs: `eval_5_second_request_capacitors_pi.md`, `eval_5_second_request_capacitors_audit.md`.
