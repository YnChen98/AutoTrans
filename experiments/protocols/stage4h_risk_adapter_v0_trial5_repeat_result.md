# Stage 4-H3 Risk Adapter v0 Trial 5 Repeat Result

## Executive Summary

`risk_adapter_v0` achieved only `2/5` valid runs on strong-wind Trial 5.

This does not improve over the historical Trial 5 baselines. The historical
results were `original` at `3/5` strict-valid, `fixed_s085` at `2/5` valid,
and `windlevel_s085` at `3/5` valid.

Trial 5 exposes that the v0 response is too weak or too late for fast
failures. Three repeats failed, and all three invalid repeats produced NaN or
extreme failure behavior that the current policy did not prevent.

## Baseline Comparison Table

| Method | Trial 5 valid runs | Notes |
| --- | ---: | --- |
| `original` | `3/5` strict-valid | Historical strong-wind Trial 5 baseline. |
| `fixed_s085` | `2/5` valid | Historical fixed XML scale `0.85` baseline. |
| `windlevel_s085` | `3/5` valid | Historical `policy_mode=wind_level` scale `0.85` baseline. |
| `risk_adapter_v0` | `2/5` valid | New limited repeat result; repeat2, repeat4, and repeat5 were invalid. |

## Repeat-Level Result Table

| Repeat | `has_nan_state` | `valid_run_suggested` | `first_nan_time` | `max_swing_angle_deg` | `max_payload_speed` | `final_uav_xy_error` | `first_swing_angle_ge_30_time` | `first_payload_speed_ge_4_time` | `first_command_risk_score_3s_ge_0p5_time` | `first_command_risk_score_5s_ge_0p5_time` | `first_command_risk_score_5s_ge_0p7_time` | `min_command_speed_scale` |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| repeat1 | `false` | `true` | `nan` | `22.240001` | `2.621284` | `0.006026` | `nan` | `nan` | `7.799989` | `nan` | `nan` | `0.850000` |
| repeat2 | `true` | `false` | `6.049739` | `170.489513` | `16.109815` | `26.001601` | `5.999697` | `5.999697` | `7.599702` | `nan` | `nan` | `0.850000` |
| repeat3 | `false` | `true` | `nan` | `21.592017` | `2.773138` | `0.000093` | `nan` | `nan` | `nan` | `nan` | `nan` | `0.850000` |
| repeat4 | `true` | `false` | `12.554876` | `142.533715` | `32.446463` | `156.723993` | `12.554876` | `nan` | `7.699954` | `19.804990` | `19.804990` | `0.650000` |
| repeat5 | `true` | `false` | `10.225462` | `177.348596` | `36.638958` | extremely large | `10.225462` | `nan` | `7.499975` | `9.625458` | `19.825544` | `0.650000` |

## Failure Timing Interpretation

repeat2 failed before risk activation. The first NaN appeared at
`first_nan_time=6.049739`, while the first `3s` risk threshold crossing was
later at `first_command_risk_score_3s_ge_0p5_time=7.599702`. The v0 adapter
therefore had no useful early intervention window for this failure.

repeat4 and repeat5 had `3s` warning before failure, but the v0 policy did not
intervene strongly enough early enough. repeat4 crossed the `3s` threshold at
`7.699954` and failed at `12.554876`. repeat5 crossed the `3s` threshold at
`7.499975` and failed at `10.225462`. Both runs still reached very large swing
and payload-speed values.

The `5s` hard threshold often triggered too late. repeat4 did not cross the
`5s` `0.5` or `0.7` thresholds until `19.804990`, after the NaN at
`12.554876`. repeat5 crossed the `5s` `0.5` threshold at `9.625458`, less than
one second before the NaN at `10.225462`, and crossed the `5s` `0.7` threshold
only at `19.825544`, after failure. repeat2 never crossed the `5s` threshold
before failure.

## Research Decision

Do not claim robust improvement from `risk_adapter_v0`.

Do not continue large v0 evaluation. Trial 5 is a useful negative test case and
shows that spending more runs on the same policy is unlikely to answer the
main research question.

Design `risk_adapter_v1` with stronger early intervention. The next version
should react earlier to `3s` risk evidence and should not wait for the `5s`
hard threshold when fast Trial 5 failures are already developing.

## What Not To Claim

- Do not claim final robustness.
- Do not claim a safety guarantee.
- Do not hide the Trial 5 failures.
