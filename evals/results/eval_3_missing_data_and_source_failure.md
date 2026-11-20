# Eval 3: missing data and source failure

Request: "oxides, binaries only, top 25"

Parser: rules. Cross-check: down. Run at 2026-11-20T22:03:52+00:00.

## Expected

- Candidates with no TBmBJ gap carry the fallback caveat and lower confidence than TBmBJ ones.
- With the cross-check source unreachable the run still succeeds and the failure is named in the output.
- No cross-check value is shown, and no cross-check citation appears.
- The client gives up after one retry rather than hammering a down server.

## Checks

| Check | Result | Detail |
|---|---|---|
| run includes fallback-gap candidates | PASS | 10 fallback, 15 TBmBJ |
| fallback gap flagged on every one | PASS |  |
| fallback lowers confidence | PASS | max points: fallback vs TBmBJ |
| run succeeds with the cross-check source down | PASS | 25 ranked |
| failure named in the output | PASS | Alexandria cross-check failed: Alexandria unreachable (ConnectionError). Affected candidates are marked; no Alexandria values shown. |
| no cross-check value or citation shown | PASS | offending: [] |
| gives up after one retry | PASS | 2 HTTP attempts |

## What the parser understood

- 'binaries only' -> filter: binary compounds only
- 'top 25' -> shortlist size 25
- not understood: 'oxides'

Full outputs: `eval_3_missing_data_and_source_failure_pi.md`, `eval_3_missing_data_and_source_failure_audit.md`.
