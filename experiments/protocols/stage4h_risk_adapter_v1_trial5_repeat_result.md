# Stage 4-H3 Risk Adapter v1 Trial 5 Repeat Result

## Executive Summary

`risk_adapter_v1` achieved `5/5` valid runs on strong-wind Trial 5.

This improves over the historical Trial 5 baselines: `original` at `3/5`
strict-valid, `fixed_s085` at `2/5` valid, `windlevel_s085` at `3/5` valid,
and `risk_adapter_v0` at `2/5` valid.

`risk_adapter_v1` uses stronger early intervention than `risk_adapter_v0`.
The policy uses:

- `soft_scale_3s=0.75`
- `soft_scale_5s=0.65`
- `hard_scale_5s=0.60`
- `risk_threshold_3s=0.5`
- `risk_threshold_5s=0.5`
- `hard_threshold_5s=0.7`
- `scale_rate_limit_per_sec=0.5`

This is a positive limited-repeat result, but it is not a final robustness
claim.

## Baseline Comparison Table

| Method | Trial 5 valid runs | Notes |
| --- | ---: | --- |
| `original` | `3/5` strict-valid | Historical strong-wind Trial 5 baseline. |
| `fixed_s085` | `2/5` valid | Historical fixed XML scale `0.85` baseline. |
| `windlevel_s085` | `3/5` valid | Historical `policy_mode=wind_level` scale `0.85` baseline. |
| `risk_adapter_v0` | `2/5` valid | Prior risk-conditioned adapter result on Trial 5. |
| `risk_adapter_v1` | `5/5` valid | New limited repeat result; all five repeats were valid. |

## Repeat-Level Result Table

| Repeat | `has_nan_state` | `valid_run_suggested` | `max_swing_angle_deg` | `max_payload_speed` | `final_uav_xy_error` | `first_command_risk_score_3s_ge_0p5_time` | `first_command_risk_score_5s_ge_0p5_time` | `min_command_speed_scale` |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| repeat1 | `false` | `true` | `23.159190` | `2.791168` | `0.003420` | `7.749986` | `nan` | `0.750000` |
| repeat2 | `false` | `true` | `16.691308` | `2.630746` | `0.101737` | `7.649955` | `9.649980` | `0.650000` |
| repeat3 | `false` | `true` | `25.391163` | `2.858002` | `0.236939` | `7.549923` | `9.549944` | `0.650000` |
| repeat4 | `false` | `true` | `18.319548` | `2.601703` | `0.000000` | `7.499808` | `nan` | `0.750000` |
| repeat5 | `false` | `true` | `18.315144` | `2.525418` | `0.036781` | `7.649948` | `nan` | `0.750000` |

## Adapter Behavior

The `3s` risk trigger appeared around `7.5s` to `7.75s` in all five repeats:
`7.749986`, `7.649955`, `7.549923`, `7.499808`, and `7.649948`.

The `5s` risk trigger appeared in repeat2 and repeat3 at `9.649980` and
`9.549944`. It did not cross the `0.5` threshold in repeat1, repeat4, or
repeat5.

The selected command scale dropped to `0.75` in all five repeats. It dropped
further to `0.65` in repeat2 and repeat3 when the `5s` risk threshold was
crossed.

No repeat crossed the swing or payload-speed safety thresholds used in prior
Trial 5 analysis. The largest observed `max_swing_angle_deg` was `25.391163`,
and the largest observed `max_payload_speed` was `2.858002`.

## Interpretation

`risk_adapter_v1` appears effective on strong-wind Trial 5 in this limited
repeat evaluation.

The stronger `3s` intervention likely addressed the Trial 5 failures observed
with `risk_adapter_v0`, where early warning either arrived too late or did not
reduce command scale strongly enough before failure development.

This result should still be treated as Trial 5 evidence only. `risk_adapter_v1`
must be tested on Trial 6 before making broader claims about online robustness.

## Research Decision

Proceed to `risk_adapter_v1` Trial 6 limited repeat evaluation.

Do not tune further before Trial 6. Preserving the current policy through the
next target keeps the comparison cleaner and avoids overfitting to Trial 5.

## What Not To Claim

- Do not claim statistical significance.
- Do not claim a safety guarantee.
- Do not claim final online robustness.
