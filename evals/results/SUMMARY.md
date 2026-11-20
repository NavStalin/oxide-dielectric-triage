# Eval results

Run 2026-11-20T21:25:51+00:00. Parser: rules. Snapshot built 2026-11-18T22:23:34+00:00.

| Eval | Case | Result | Details |
|---|---|---|---|
| 1 | normal | 5/5 pass | [eval_1_normal.md](eval_1_normal.md) |
| 2 | adversarial | 6/6 pass | [eval_2_adversarial.md](eval_2_adversarial.md) |
| 3 | missing data and source failure | 7/7 pass | [eval_3_missing_data_and_source_failure.md](eval_3_missing_data_and_source_failure.md) |
| 4 | face validity | report | [eval_4_face_validity.md](eval_4_face_validity.md) |
| 5 | second request capacitors | 6/6 pass | [eval_5_second_request_capacitors.md](eval_5_second_request_capacitors.md) |

A live cross-check run is recorded in [live_crosscheck.md](live_crosscheck.md).

Re-run with `make evals`. Assertions are in `evals/run_evals.py`; cases in `evals/cases.yaml`.
