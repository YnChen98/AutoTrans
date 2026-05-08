# Stage 4-E Trial 5 Expansion Summary

Stage 4-E Trial 5 strong-wind expansion added 15 completed runs for `original`, `fixed_s085`, and `windlevel_s085`.

## Validity Summary

| Method | Trial | Valid runs |
| --- | --- | --- |
| `original` | Trial 5 | 4/5 `valid_run_suggested`, 3/5 strict-valid |
| `fixed_s085` | Trial 5 | 2/5 |
| `windlevel_s085` | Trial 5 | 3/5 |

For `original`, repeat 4 has `valid_run_suggested=true` from the analyzer, but it should be treated as strict-invalid because `max_swing_angle_deg=73.283943` exceeds the swing safety threshold.

Trial 5 includes NaN failures, target-error failures, and swing/safety failures. Future Stage 4 risk prediction should use `label_strict_invalid` for Trial 5 analysis because it captures the stricter target, speed, swing, and safety labels beyond the legacy `label_invalid`.

## Manifest Update

These runs should be used with the existing strong-wind Trial 1, Trial 2, Trial 3, and Trial 4 rows to expand `experiments/datasets/stage4_risk_dataset.csv` from 60 rows to 75 rows.
