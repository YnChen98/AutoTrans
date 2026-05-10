# Stage 4-J Trial 5 10-Repeat Fair Comparison

## Executive Summary

Trial 5 10-repeat fair comparison is complete for `original`, `fixed_s085`,
`windlevel_s085`, and `risk_adapter_v1`.

`risk_adapter_v1` is strongest on Trial 5 with `9/10` valid runs.

`original` is `7/10` strict-valid, although its raw `valid_run_suggested`
count is `9/10`. `fixed_s085` is `5/10`, and `windlevel_s085` is `6/10`.

`risk_adapter_v1` improves over all baselines on Trial 5. Do not claim final
robustness yet.

## Trial 5 Method Comparison Table

| Method | `valid_run_suggested` count | Strict-valid count | Invalid / strict-invalid summary |
| --- | ---: | ---: | --- |
| `original` | `9/10` | `7/10` | repeat1 was a NaN/safety failure; repeat4 was a strict swing failure; repeat8 was a strict payload-speed failure. |
| `fixed_s085` | `5/10` | `5/10` | repeats 2, 3, 4, 8, and 9 were invalid. |
| `windlevel_s085` | `6/10` | `6/10` | repeats 2, 3, 7, and 8 were invalid. |
| `risk_adapter_v1` | `9/10` | `9/10` | repeat6 was a NaN/safety failure. |

## Failure Mode Analysis

`original` includes one NaN failure and two strict safety failures. repeat1
had `first_nan_time=19.900014`, `max_swing_angle_deg=143.527962`,
`max_payload_speed=31.673372`, and `final_uav_xy_error=129.089176`. repeat4
was a strict swing failure despite `valid_run_suggested=true`, with
`max_swing_angle_deg=73.283943`. repeat8 was a strict payload-speed failure
despite `valid_run_suggested=true`, with `max_payload_speed=4.265458`.

`fixed_s085` includes NaN, swing/speed, and target-related failures. repeat2
had no NaN but reached `max_swing_angle_deg=129.240894`,
`max_payload_speed=13.473145`, and `final_uav_xy_error=6.600781`. repeat3
failed with `first_nan_time=16.399960`, repeat4 with
`first_nan_time=19.349965`, and repeat8 with `first_nan_time=25.099269`.
repeat9 was swing/target-related invalid with no NaN,
`max_swing_angle_deg=75.074686`, and `final_uav_xy_error=0.682215`.

`windlevel_s085` includes target-error and NaN failures. repeat2 was a
target-error failure with no NaN and `final_uav_xy_error=0.714966`. repeat3
failed with `first_nan_time=5.150022`, repeat7 with
`first_nan_time=25.457492`, and repeat8 with `first_nan_time=12.602702`.

`risk_adapter_v1` has one NaN/safety failure. repeat6 failed with
`first_nan_time=27.216400`, `max_swing_angle_deg=171.354989`,
`max_payload_speed=39.965828`, and `final_uav_xy_error=421.913262`.

## Interpretation Caveat

`valid_run_suggested` is not enough for safety-aware comparison. Some runs pass
target/NaN checks but violate swing or payload-speed safety thresholds.

`label_strict_invalid` / strict-valid should be used for paper-facing
safety-risk comparison.

`risk_adapter_v1` is strongest on Trial 5, but it still has one failure.

## Updated Aggregate Interpretation

With Trial 4 and Trial 5 expanded to 10 repeats and Trial 6 still at 5
repeats, the weighted available-repeat aggregate is:

| Method | Current weighted aggregate |
| --- | ---: |
| `original` | `17/25` strict-valid |
| `fixed_s085` | `16/25` valid |
| `windlevel_s085` | `12/25` valid |
| `risk_adapter_v1` | `20/25` valid |

`risk_adapter_v1` is strongest in the current weighted available-repeat
aggregate at `20/25`. This is not a final balanced comparison because Trial 6
remains 5-repeat.

## Research Decision

Proceed to Trial 6 repeat expansion to 10 repeats before final Stage 4-H
comparison.

Do not tune `risk_adapter_v2` yet.

Do not claim statistical significance.

## What Not To Claim

- Do not claim a safety guarantee.
- Do not claim final online robustness.
- Do not use `valid_run_suggested` alone for paper safety conclusions.
- Do not hide the `risk_adapter_v1` repeat6 failure.
