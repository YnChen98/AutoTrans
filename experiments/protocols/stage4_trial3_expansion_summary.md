# Stage 4-C Trial 3 Expansion Summary

Stage 4-C Trial 3 strong-wind expansion added 15 completed runs for `original`, `fixed_s085`, and `windlevel_s085`.

## Validity Summary

| Method | Trial | Valid runs |
| --- | --- | --- |
| `original` | Trial 3 | 2/5 |
| `fixed_s085` | Trial 3 | 0/5 |
| `windlevel_s085` | Trial 3 | 3/5 |

Trial 3 is a strong stress case. `fixed_s085` fails badly on Trial 3. `windlevel_s085` is currently the best of the three on Trial 3, but still has invalid runs.

## Expected Overall 45-Run Counts

After adding Trial 3 to `experiments/protocols/stage4_risk_manifest.json`, the expected overall counts are:

| Method | Valid runs |
| --- | --- |
| `original` | 9/15 |
| `fixed_s085` | 7/15 |
| `windlevel_s085` | 11/15 |

These runs should be used with the existing strong-wind Trial 1 and Trial 2 rows to expand `experiments/datasets/stage4_risk_dataset.csv` from 30 rows to 45 rows.
