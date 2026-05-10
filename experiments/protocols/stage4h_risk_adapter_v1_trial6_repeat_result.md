# Stage 4-H3 Risk Adapter v1 Trial 6 Repeat Result

## Executive Summary

`risk_adapter_v1` achieved `4/5` valid runs on strong-wind Trial 6.

This matches `risk_adapter_v0` on Trial 6 and improves over the historical
Trial 6 baselines, where `original`, `fixed_s085`, and `windlevel_s085` each
achieved `2/5` valid runs.

Across Trial 5 and Trial 6, `risk_adapter_v1` achieved `9/10` valid runs. This
is the strongest current limited-repeat result, but it is not a final
robustness claim.

The `risk_adapter_v1` policy used:

- `soft_scale_3s=0.75`
- `soft_scale_5s=0.65`
- `hard_scale_5s=0.60`
- `risk_threshold_3s=0.5`
- `risk_threshold_5s=0.5`
- `hard_threshold_5s=0.7`
- `scale_rate_limit_per_sec=0.5`

## Baseline Comparison Table

| Method | Trial 6 valid runs | Notes |
| --- | ---: | --- |
| `original` | `2/5` valid | Historical strong-wind Trial 6 baseline. |
| `fixed_s085` | `2/5` valid | Historical fixed XML scale `0.85` baseline. |
| `windlevel_s085` | `2/5` valid | Historical `policy_mode=wind_level` scale `0.85` baseline. |
| `risk_adapter_v0` | `4/5` valid | Prior risk-conditioned adapter result on Trial 6. |
| `risk_adapter_v1` | `4/5` valid | New limited repeat result; repeat1 was invalid with NaN. |

## Repeat-Level Result Table

| Repeat | `has_nan_state` | `valid_run_suggested` | `first_nan_time` | `max_swing_angle_deg` | `max_payload_speed` | `final_uav_xy_error` | `first_command_risk_score_3s_ge_0p5_time` | `first_command_risk_score_5s_ge_0p5_time` | `first_command_risk_score_5s_ge_0p7_time` | `first_swing_angle_ge_30_time` | `first_payload_speed_ge_4_time` | `min_command_speed_scale` |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| repeat1 | `true` | `false` | `25.099965` | `97.513452` | `32.251507` | `59.839374` | `7.699993` | `9.700228` | `29.900020` | `11.049988` | `11.699972` | `0.600000` |
| repeat2 | `false` | `true` | `nan` | `14.692509` | `2.866861` | `0.384165` | `7.749992` | `9.749985` | `nan` | `nan` | `nan` | `0.650000` |
| repeat3 | `false` | `true` | `nan` | `13.053983` | `2.555509` | `0.011844` | `7.599989` | `9.599980` | `nan` | `nan` | `nan` | `0.650000` |
| repeat4 | `false` | `true` | `nan` | `23.965220` | `2.848312` | `0.157350` | `7.650614` | `9.650040` | `nan` | `nan` | `nan` | `0.650000` |
| repeat5 | `false` | `true` | `nan` | `24.376142` | `2.943338` | `0.000000` | `7.650024` | `9.650015` | `nan` | `nan` | `nan` | `0.650000` |

## Failure Timing Interpretation

repeat1 had early risk activation before the safety-threshold violations. The
`3s` threshold crossed at `7.699993`, and the `5s` `0.5` threshold crossed at
`9.700228`. The swing threshold crossed later at
`first_swing_angle_ge_30_time=11.049988`, and the payload-speed threshold
crossed at `first_payload_speed_ge_4_time=11.699972`.

The soft intervention did not prevent the severe late failure in repeat1. The
run eventually reached `max_swing_angle_deg=97.513452`,
`max_payload_speed=32.251507`, `final_uav_xy_error=59.839374`, and a NaN at
`first_nan_time=25.099965`.

The `5s` hard threshold was too late for this failure. It crossed at
`first_command_risk_score_5s_ge_0p7_time=29.900020`, after the NaN at
`25.099965`. The logged `min_command_speed_scale=0.600000` therefore should
not be interpreted as a successful pre-failure hard intervention for repeat1.

## Combined Trial 5 + Trial 6 Summary

| Method | Trial 5 + Trial 6 valid runs | Notes |
| --- | ---: | --- |
| `original` | `5/10` strict-valid | Historical combined Trial 5 and Trial 6 baseline. |
| `fixed_s085` | `4/10` valid | Historical fixed XML scale `0.85` combined result. |
| `windlevel_s085` | `5/10` valid | Historical `policy_mode=wind_level` scale `0.85` combined result. |
| `risk_adapter_v0` | `6/10` valid | Prior risk-conditioned adapter combined result. |
| `risk_adapter_v1` | `9/10` valid | Current strongest limited-repeat candidate. |

## Research Decision

`risk_adapter_v1` is the current strongest candidate based on the Trial 5 and
Trial 6 limited repeat evaluations.

Proceed to `risk_adapter_v1` Trial 4 limited repeat evaluation before making
broader claims.

Do not tune further before Trial 4. Keeping the same policy avoids overfitting
the adapter to the Trial 5 and Trial 6 observations.

## What Not To Claim

- Do not claim statistical significance.
- Do not claim a safety guarantee.
- Do not claim final online robustness.
- Do not hide the repeat1 failure.
