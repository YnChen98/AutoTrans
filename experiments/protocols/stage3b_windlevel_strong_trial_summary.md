# Stage 3-B Wind-Level Policy Strong-Wind Trial Summary

## Executive Summary

`policy_mode=wind_level` is the current stable default candidate for Stage 3-B strong-wind evaluation. Under the current strong wind setting, it keeps both planner command scales fixed at `0.85`.

Trial 1 and Trial 3 are valid under target-error checks. Trial 2 is mixed: the first run was invalid with a NaN failure, then `repeat2` and `repeat3` were valid. This method is promising, but it is not final. More repeated trials are needed before making strong claims about robustness or superiority.

## Method Snapshot

- Adapter node: independent `heuristic_command_adapter`
- Policy mode: `policy_mode=wind_level`
- Planner adaptation:
  - `manager/enable_command_adaptation=true`
  - `manager/adaptation_mode=topic`
  - `manager/require_adaptation_topic_ready=true`
- Readiness gate: enabled
- Controller: unchanged
- Simulator: unchanged
- Command scale source: selected from `wind_force_norm` only
- Swing/speed reactive overrides: not applied in `policy_mode=wind_level`
- `target_xy_tolerance: 0.5`

Wind setting:

- wind level: strong
- `wind_velocity_x: 0.5`
- `wind_drag_linear: 0.015`
- `wind_max_force: 0.0075`
- `wind_force_norm` annotation: `0.007500`

Scale setting observed in valid `wind_level` runs:

- `command_speed_scale: 0.85`
- `command_acceleration_scale: 0.85`

## Trial Result Table

| trial | target | valid | max_swing_angle_deg | p95_swing_angle_deg | max_uav_speed | max_payload_speed | final_uav_xy_error | final_uav_position_error_3d | command_scale | interpretation |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Trial 1 target-check repeat | `(0.0, -1.2)` | yes | 35.203489 | 13.179278 | 2.380580 | 2.710545 | 0.166338 | 0.180072 | 0.850000 | Valid target-check run with bounded speed and acceptable final target error. |
| Trial 2 first run | `(-7.5, 1.5)` | no | 155.988127 | 38.811179 | 68.417234 | 69.774368 | 196.263063 | 204.941099 | 0.850000 | Invalid run with NaN state and severe divergence despite fixed wind-level scale. |
| Trial 2 repeat2 | `(-7.5, 1.5)` | yes | 24.068409 | 7.459533 | 2.501396 | 2.515504 | 0.423067 | 0.426715 | 0.850000 | Valid repeat; final error is within `target_xy_tolerance` but close to the threshold. |
| Trial 2 repeat3 | `(-7.5, 1.5)` | yes | 16.812274 | 3.193015 | 2.394652 | 2.523169 | 0.010671 | 0.010674 | 0.850000 | Valid repeat with very accurate final target convergence. |
| Trial 3 target-check repeat | `(8.0, 1.5)` | yes | 21.016220 | 9.392263 | 2.515794 | 2.652960 | 0.060867 | 0.060867 | 0.850000 | Valid target-check run with low final error and bounded strong-wind response. |

## Detailed Metrics

### Trial 1 Target-Check Repeat

- Target: `(0.0, -1.2)`
- `valid_run_suggested: true`
- `has_nan_state: false`
- `final_row_has_nan: false`
- `mean_swing_angle_deg: 1.949270`
- `max_swing_angle_deg: 35.203489`
- `p95_swing_angle_deg: 13.179278`
- `max_uav_speed: 2.380580`
- `max_payload_speed: 2.710545`
- `uav_path_length: 18.080414`
- `payload_path_length: 23.820243`
- `final_uav_position: (-0.035925, -1.362412, 1.399439)`
- `final_payload_position: (-0.035925, -1.362412, 0.730994)`
- `final_uav_xy_error: 0.166338`
- `final_payload_xy_error: 0.166338`
- `final_uav_position_error_3d: 0.180072`
- `final_payload_position_error_3d: 0.180072`
- `mean_command_speed_scale: 0.850000`
- `min_command_speed_scale: 0.850000`
- `max_command_speed_scale: 0.850000`
- `final_command_speed_scale: 0.850000`

### Trial 2 Target-Check First Run

- Target: `(-7.5, 1.5)`
- `valid_run_suggested: false`
- `has_nan_state: true`
- `first_nan_time: 9.899776`
- `final_row_has_nan: true`
- `mean_swing_angle_deg: 5.196064`
- `max_swing_angle_deg: 155.988127`
- `p95_swing_angle_deg: 38.811179`
- `max_uav_speed: 68.417234`
- `max_payload_speed: 69.774368`
- `uav_path_length: 213.920534`
- `payload_path_length: 215.024030`
- `final_uav_position: (-49.167820, -190.288901, -57.537215)`
- `final_payload_position: (-48.894636, -189.541536, -57.630194)`
- `final_uav_xy_error: 196.263063`
- `final_payload_xy_error: 195.474766`
- `final_uav_position_error_3d: 204.941099`
- `final_payload_position_error_3d: 204.020755`
- `mean_command_speed_scale: 0.850000`
- `min_command_speed_scale: 0.850000`
- `max_command_speed_scale: 0.850000`
- `final_command_speed_scale: 0.850000`

### Trial 2 Repeat2

- Target: `(-7.5, 1.5)`
- `valid_run_suggested: true`
- `has_nan_state: false`
- `final_row_has_nan: false`
- `mean_swing_angle_deg: 1.062653`
- `max_swing_angle_deg: 24.068409`
- `p95_swing_angle_deg: 7.459533`
- `max_uav_speed: 2.501396`
- `max_payload_speed: 2.515504`
- `uav_path_length: 8.658915`
- `payload_path_length: 12.740577`
- `final_uav_position: (-7.845590, 1.255965, 1.412739)`
- `final_payload_position: (-7.845590, 1.255965, 0.744294)`
- `final_uav_xy_error: 0.423067`
- `final_payload_xy_error: 0.423067`
- `final_uav_position_error_3d: 0.426715`
- `final_payload_position_error_3d: 0.426715`
- `mean_command_speed_scale: 0.850000`
- `min_command_speed_scale: 0.850000`
- `max_command_speed_scale: 0.850000`
- `final_command_speed_scale: 0.850000`

### Trial 2 Repeat3

- Target: `(-7.5, 1.5)`
- `valid_run_suggested: true`
- `has_nan_state: false`
- `final_row_has_nan: false`
- `mean_swing_angle_deg: 0.709515`
- `max_swing_angle_deg: 16.812274`
- `p95_swing_angle_deg: 3.193015`
- `max_uav_speed: 2.394652`
- `max_payload_speed: 2.523169`
- `uav_path_length: 11.017747`
- `payload_path_length: 11.767564`
- `final_uav_position: (-7.491871, 1.493087, 1.468164)`
- `final_payload_position: (-7.493055, 1.494099, 0.799721)`
- `final_uav_xy_error: 0.010671`
- `final_payload_xy_error: 0.009114`
- `final_uav_position_error_3d: 0.010674`
- `final_payload_position_error_3d: 0.009117`
- `mean_command_speed_scale: 0.850000`
- `min_command_speed_scale: 0.850000`
- `max_command_speed_scale: 0.850000`
- `final_command_speed_scale: 0.850000`

### Trial 3 Target-Check Repeat

- Target: `(8.0, 1.5)`
- `valid_run_suggested: true`
- `has_nan_state: false`
- `final_row_has_nan: false`
- `mean_swing_angle_deg: 2.266949`
- `max_swing_angle_deg: 21.016220`
- `p95_swing_angle_deg: 9.392263`
- `max_uav_speed: 2.515794`
- `max_payload_speed: 2.652960`
- `uav_path_length: 25.705630`
- `payload_path_length: 26.473062`
- `final_uav_position: (7.948750, 1.467165, 1.468243)`
- `final_payload_position: (7.964194, 1.477043, 0.800049)`
- `final_uav_xy_error: 0.060867`
- `final_payload_xy_error: 0.042534`
- `final_uav_position_error_3d: 0.060867`
- `final_payload_position_error_3d: 0.042534`
- `mean_command_speed_scale: 0.850000`
- `min_command_speed_scale: 0.850000`
- `max_command_speed_scale: 0.850000`
- `final_command_speed_scale: 0.850000`

## Trial 2 Interpretation

Trial 2 is mixed evidence and should be recorded rather than deleted. One early NaN failure occurred even though `command_speed_scale` stayed at `0.85` throughout the run. The first NaN appeared at `first_nan_time: 9.899776`, and the final position diverged far from the target.

The two clean repeats were valid. `repeat2` finished within `target_xy_tolerance` but close to the threshold, while `repeat3` finished with very small final target error. This suggests stochastic or initialization sensitivity, or run-to-run simulator variability, under the same strong-wind `wind_level` policy setting.

## Current Conclusion

`policy_mode=wind_level` is a better default than `policy_mode=risk_reactive` v1 for formal strong-wind evaluation. The `risk_reactive` v1 policy can react too late and should remain experimental.

The current candidate method for strong-wind evaluation is therefore `policy_mode=wind_level`, with scale selected from `wind_force_norm` only. It is not yet a final proven method.

## Next Recommended Experiments

1. Run another full repeat set: Trial 1, Trial 2, and Trial 3.
2. Compare original strong wind, fixed `0.85`, and `policy_mode=wind_level`.
3. Add an aggregate success-rate and target-error table.
4. Consider boundary wind only after strong wind is stable.

## What Not To Claim Yet

- Do not claim fully solved strong-wind transport.
- Do not claim strict superiority over baseline.
- Do not claim RL results.
- Do not hide the invalid Trial 2 run.
