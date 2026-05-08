# Stage 4 Trial 6 Expansion Summary

Stage 4-E Trial 6 adds a shared strong-wind stress target at `target_x=0.0`, `target_y=1.5`, `target_z=1.468415`, and `payload_target_z=0.799970`.

## Result Summary

| Method | Valid runs | Notes |
| --- | ---: | --- |
| `original` | 2/5 | Repeats 2, 3, and 4 were invalid NaN runs. |
| `fixed_s085` | 2/5 | Repeats 1, 2, and 3 were invalid NaN runs. |
| `windlevel_s085` | 2/5 | Repeats 1, 2, and 4 were invalid NaN runs. |

Trial 6 is a shared stress target where all methods show the same 2/5 valid rate. The invalid runs are mostly NaN or failure-to-complete cases.

This target helps the Stage 4 dataset represent target-level difficulty rather than method ranking alone. After adding these 15 rows, `experiments/protocols/stage4_risk_manifest.json` should contain 90 manifest rows.
