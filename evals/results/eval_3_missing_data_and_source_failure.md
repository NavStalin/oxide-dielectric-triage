# Eval 3: missing data and source failure

Request: "oxides, binaries only, top 25"

Parser: rules. OQMD: down. Run at 2026-11-19T19:13:04+00:00.

## Expected

- Candidates with no TBmBJ gap carry the fallback caveat and lower confidence than TBmBJ ones.
- With OQMD unreachable the run still succeeds and the failure is named in the output.
- No OQMD value is shown, and no OQMD citation appears.
- The OQMD client gives up after one retry rather than hammering a down server.

## Checks

| Check | Result | Detail |
|---|---|---|
| run includes fallback-gap candidates | PASS | 10 fallback, 15 TBmBJ |
| fallback gap flagged on every one | PASS |  |
| fallback lowers confidence | PASS | max points: fallback vs TBmBJ |
| run succeeds with OQMD down | PASS | 25 ranked |
| failure named in the output | PASS | OQMD cross-check failed: OQMD unreachable (ConnectionError). Affected candidates are marked; no OQMD values shown. |
| no OQMD value or citation shown | PASS | offending: [] |
| gives up after one retry | PASS | 2 HTTP attempts |

## What the parser understood

- 'binaries only' -> filter: binary compounds only
- 'top 25' -> shortlist size 25
- not understood: 'oxides'

Full outputs: `eval_3_missing_data_and_source_failure_pi.md`, `eval_3_missing_data_and_source_failure_audit.md`.
