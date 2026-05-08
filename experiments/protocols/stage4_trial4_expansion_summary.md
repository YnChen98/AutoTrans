# Stage 4-E Trial 4 Expansion Summary

Stage 4-E Trial 4 strong-wind expansion added 15 completed runs for `original`, `fixed_s085`, and `windlevel_s085`.

## Validity Summary

| Method | Trial | Valid runs |
| --- | --- | --- |
| `original` | Trial 4 | 4/5 |
| `fixed_s085` | Trial 4 | 5/5 |
| `windlevel_s085` | Trial 4 | 1/5 |

Trial 4 is a strong target-method interaction case. `fixed_s085` performs best on Trial 4. `windlevel_s085` performs poorly on Trial 4 despite being strong on some earlier targets.

This supports the need for target diversity and risk prediction instead of fixed method ranking.

## Manifest Update

These runs should be used with the existing strong-wind Trial 1, Trial 2, and Trial 3 rows to expand `experiments/datasets/stage4_risk_dataset.csv` from 45 rows to 60 rows.
