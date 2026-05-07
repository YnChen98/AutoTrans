# Stage 3-C Original AutoTrans Strong-Wind Trial 2 Repeated Validation

## Executive Summary

Original AutoTrans under strong wind Trial 2 is unstable in this repeated validation batch. The setting disables command adaptation:

- `enable_command_adaptation=false`
- `adaptation_mode=none`
- no `heuristic_command_adapter`
- strong drag wind enabled
- `wind_force_norm` annotation: `0.007500`
- Target: `(-7.5, 1.5)`
- `target_xy_tolerance: 0.5`

Only 1 of 3 repeats is valid, while 2 of 3 repeats are invalid with NaN state failures. This means Stage 3 evaluation should use repeated success rate, not single-run metrics.

## Result Table

| repeat | valid | has_nan_state | first_nan_time | final_row_has_nan | max_swing_angle_deg | p95_swing_angle_deg | max_uav_speed | max_payload_speed | final_uav_xy_error | final_uav_position_error_3d | interpretation |
| --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| repeat1 | no | true | 34.899964 | true | 22.469828 | 10.347303 | 32.334157 | 32.349150 | 14.120674 | 157.092334 | Invalid run; late NaN failure and large final 3D position error. |
| repeat2 | no | true | 9.900357 | true | 109.526961 | 37.083406 | 377.059532 | 375.944487 | 219.374642 | 227.782610 | Invalid run; early NaN failure with severe speed and swing growth. |
| repeat3 | yes | false | n/a | false | 21.188573 | 6.942290 | 2.438925 | 2.484804 | 0.000000 | 0.000000 | Valid run; target check passes exactly in this repeat. |

## Interpretation

Trial 2 is a stress case for original AutoTrans under strong drag wind. Two invalid repeats appear even without command adaptation, which means failures observed in `policy_mode=wind_level` should not automatically be attributed to the adaptation layer.

The result also shows why single-run metrics are not enough for Stage 3. A single valid repeat can hide baseline instability, while a single invalid repeat can overstate failure. Future comparison should use equal-repeat success-rate tables across methods.

## Next Recommended Experiment

Run a 5-repeat comparison for:

- original AutoTrans strong wind
- fixed `0.85`
- `policy_mode=wind_level` with strong-wind scale `0.85`

Report success rate, target-error statistics, NaN count, swing statistics, and speed statistics using the same target and `target_xy_tolerance: 0.5`.
