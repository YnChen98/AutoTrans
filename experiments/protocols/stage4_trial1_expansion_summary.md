# Stage 4-C Trial 1 Expansion Summary

Stage 4-C Trial 1 strong-wind expansion added 15 completed runs for `original`, `fixed_s085`, and `windlevel_s085`.

## Validity Summary

| Method | Trial | Valid runs |
| --- | --- | --- |
| `original` | Trial 1 | 4/5 |
| `fixed_s085` | Trial 1 | 5/5 |
| `windlevel_s085` | Trial 1 | 5/5 |

The `original` group had one invalid NaN run: `stage4_original_strong_trial1_repeat3`.

The `windlevel_s085` group had all Trial 1 runs valid, but its mean target error was larger than `original` and `fixed_s085` for this batch.

These runs should be used with the existing 15 strong-wind Trial 2 runs to expand `experiments/datasets/stage4_risk_dataset.csv` from 15 rows to 30 rows.
