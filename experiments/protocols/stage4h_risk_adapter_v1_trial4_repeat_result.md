# Stage 4-H3 Risk Adapter v1 Trial 4 Repeat Result

## Executive Summary

`risk_adapter_v1` achieved `4/5` valid runs on strong-wind Trial 4.

This matches the historical `original` Trial 4 baseline, is worse than
`fixed_s085`, and is much better than `windlevel_s085`.

Trial 4 repeat5 failed because risk prediction triggered after the failure and
safety-violation window. The NaN appeared at `first_nan_time=24.900021`, while
the first `3s` risk threshold crossing did not appear until `27.599985`.

Across Trial 4, Trial 5, and Trial 6, `risk_adapter_v1` achieved `13/15` valid
runs. This is the strongest current limited-repeat result, but it is not a
final robustness claim.

The `risk_adapter_v1` policy used:

- `soft_scale_3s=0.75`
- `soft_scale_5s=0.65`
- `hard_scale_5s=0.60`
- `risk_threshold_3s=0.5`
- `risk_threshold_5s=0.5`
- `hard_threshold_5s=0.7`
- `scale_rate_limit_per_sec=0.5`

## Baseline Comparison Table

| Method | Trial 4 valid runs | Notes |
| --- | ---: | --- |
| `original` | `4/5` valid | Historical strong-wind Trial 4 baseline. |
| `fixed_s085` | `5/5` valid | Historical fixed XML scale `0.85` baseline. |
| `windlevel_s085` | `1/5` valid | Historical `policy_mode=wind_level` scale `0.85` baseline. |
| `risk_adapter_v1` | `4/5` valid | New limited repeat result; repeat5 was invalid with NaN. |

## Repeat-Level Result Table

| Repeat | `has_nan_state` | `valid_run_suggested` | `first_nan_time` | `max_swing_angle_deg` | `max_payload_speed` | `final_uav_xy_error` | `max_command_risk_score_3s` | `max_command_risk_score_5s` | `first_swing_angle_ge_30_time` | `first_payload_speed_ge_4_time` | `first_command_risk_score_3s_ge_0p5_time` | `first_command_risk_score_5s_ge_0p5_time` | `first_command_risk_score_5s_ge_0p7_time` | `min_command_speed_scale` |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| repeat1 | `false` | `true` | `nan` | `17.998654` | `2.499334` | `0.000000` | `0.229419` | `0.203179` | `nan` | `nan` | `nan` | `nan` | `nan` | `0.850000` |
| repeat2 | `false` | `true` | `nan` | `13.779706` | `2.610758` | `0.029931` | `0.226456` | `0.208583` | `nan` | `nan` | `nan` | `nan` | `nan` | `0.850000` |
| repeat3 | `false` | `true` | `nan` | `16.645079` | `2.771085` | `0.071210` | `0.235192` | `0.215664` | `nan` | `nan` | `nan` | `nan` | `nan` | `0.850000` |
| repeat4 | `false` | `true` | `nan` | `18.741379` | `2.513542` | `0.000000` | `0.224391` | `0.189652` | `nan` | `nan` | `nan` | `nan` | `nan` | `0.850000` |
| repeat5 | `true` | `false` | `24.900021` | `134.956542` | `32.810948` | `157.854930` | `n/a` | `n/a` | `25.150046` | `25.200054` | `27.599985` | `29.599997` | `29.599997` | `0.600000` |

## Failure Timing Interpretation

repeat1 through repeat4 were low-risk valid runs. Their maximum risk scores
stayed below the `0.5` threshold for both horizons, and the selected command
scale stayed at `0.85` for all four repeats.

repeat5 failed before the risk trigger. The NaN appeared at
`first_nan_time=24.900021`, followed by the swing threshold at
`first_swing_angle_ge_30_time=25.150046` and the payload-speed threshold at
`first_payload_speed_ge_4_time=25.200054`. The first `3s` risk threshold
crossing came later at `27.599985`, and the first `5s` threshold crossings
came at `29.599997`.

This is a model timing and detection limitation, not only a scale policy
limitation. Even though the logged `min_command_speed_scale=0.600000`, the risk
intervention happened after the critical failure window had already started.

## Combined Trial 4 + Trial 5 + Trial 6 Summary

| Method | Trial 4 + Trial 5 + Trial 6 valid runs | Notes |
| --- | ---: | --- |
| `original` | `9/15` | Historical combined Trial 4, Trial 5, and Trial 6 baseline. |
| `fixed_s085` | `9/15` | Historical fixed XML scale `0.85` combined result. |
| `windlevel_s085` | `6/15` | Historical `policy_mode=wind_level` scale `0.85` combined result. |
| `risk_adapter_v1` | `13/15` | Current strongest limited-repeat candidate. |

## Research Decision

`risk_adapter_v1` is the current strongest candidate based on the Trial 4,
Trial 5, and Trial 6 limited repeat evaluations.

The next step should be an aggregate `risk_adapter_v1` comparison document.

Do not tune further before documenting the aggregate result. The repeat5
failure should be preserved as evidence of a timing and detection limitation.

## What Not To Claim

- Do not claim statistical significance.
- Do not claim a safety guarantee.
- Do not claim final online robustness.
- Do not hide the repeat5 failure.
