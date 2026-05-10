# Stage 4-H3 Risk Adapter v0 Trial 6 Repeat Result

## Executive Summary

`risk_adapter_v0` achieved `4/5` valid runs on strong-wind Trial 6 after fixing
stale episode state.

This is better than the historical Trial 6 baselines, where `original`,
`fixed_s085`, and `windlevel_s085` each achieved `2/5` valid runs.

Cross-repeat stale risk state appears fixed. The risk triggers appeared at
fresh repeat times instead of carrying stale state from previous episodes.

The result is still not a robustness claim. `risk_adapter_v0` failed on
repeat5 with a NaN at `first_nan_time=40.599974`, so the failure remains
important negative evidence.

## Result Table

### Baseline Comparison

| Method | Trial 6 valid runs | Notes |
| --- | ---: | --- |
| `original` | `2/5` | Historical strong-wind Trial 6 baseline. |
| `fixed_s085` | `2/5` | Historical fixed XML scale `0.85` baseline. |
| `windlevel_s085` | `2/5` | Historical `policy_mode=wind_level` scale `0.85` baseline. |
| `risk_adapter_v0` | `4/5` | New limited repeat result; repeat5 was invalid with NaN. |

### Repeat-Level Result

| Repeat | `has_nan_state` | `valid_run_suggested` | `first_nan_time` | `max_swing_angle_deg` | `max_payload_speed` | `final_uav_xy_error` | `first_command_risk_score_3s_ge_0p5_time` | `first_command_risk_score_5s_ge_0p5_time` | `max_command_risk_score_5s` | `first_command_risk_score_5s_ge_0p7_time` | `min_command_speed_scale` |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| repeat1 | `false` | `true` | `nan` | `13.514923` | `2.485310` | `0.001097` | `7.599982` | `9.599978` | `n/a` | `nan` | `0.750000` |
| repeat2 | `false` | `true` | `nan` | `13.383052` | `2.533115` | `0.010784` | `7.500031` | `9.500150` | `n/a` | `nan` | `0.750000` |
| repeat3 | `false` | `true` | `nan` | `13.418304` | `2.532991` | `0.005353` | `7.750073` | `9.750046` | `n/a` | `nan` | `0.750000` |
| repeat4 | `false` | `true` | `nan` | `13.308680` | `2.546976` | `0.015925` | `7.550044` | `9.550022` | `n/a` | `nan` | `0.750000` |
| repeat5 | `true` | `false` | `40.599974` | `142.072964` | `15.238584` | `2.754164` | `7.649931` | `9.649935` | `0.591692` | `nan` | `0.750000` |

## Adapter Behavior

The `3s` risk trigger appeared around `7.5s` in all five repeats:
`7.599982`, `7.500031`, `7.750073`, `7.550044`, and `7.649931`.

The `5s` risk trigger appeared around `9.5s` in all five repeats:
`9.599978`, `9.500150`, `9.750046`, `9.550022`, and `9.649935`.

The selected command scale dropped to `0.75` in every repeat, matching the v0
soft intervention path.

The hard threshold `0.7` did not trigger. In the invalid repeat5 case,
`max_command_risk_score_5s=0.591692` and
`first_command_risk_score_5s_ge_0p7_time=nan`, so the model did not classify
that run as hard risk.

## Interpretation

The v0 soft intervention appears promising on Trial 6 because it improved the
limited-repeat result from the historical `2/5` baseline level to `4/5`.

repeat5 shows that scale `0.75` is not sufficient for all Trial 6 failures.
The run still reached `max_swing_angle_deg=142.072964`,
`max_payload_speed=15.238584`, and then produced a NaN at
`first_nan_time=40.599974`.

The risk model did not identify repeat5 as hard-risk. This is model evidence,
not proof that the planner or controller is robust under that failure mode.

## Research Decision

Proceed to Trial 5 limited repeat evaluation.

Do not tune the policy yet. Trial 6 gives useful positive evidence for
`risk_adapter_v0`, but the failed repeat5 should be preserved before changing
thresholds or scale levels.

Do not claim final improvement yet. This is a limited repeat result and should
be compared with additional targets before making broader claims.

## What Not To Claim

- Do not claim statistical significance.
- Do not claim a safety guarantee.
- Do not hide the repeat5 failure.
