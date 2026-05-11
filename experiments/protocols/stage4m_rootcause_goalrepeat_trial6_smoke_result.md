# Stage 4-M Trial 6 Goal-Repeat Root-Cause Smoke Result

## Executive Summary

This document records Stage 4-M root-cause smoke diagnostics for original
Trial 6 under strong wind after reference logging was added.

- `goal_repeat=10` reproduced command-saturation-before-NaN divergence in 1
  out of 4 total root-cause smoke runs.
- `goal_repeat=1` also reproduced command-saturation-before-NaN divergence in
  1 out of 4 total root-cause smoke runs.
- The failed smoke runs did not show reference nonfinite data or reference
  position/velocity jumps in the logged `ref_pos`/`ref_vel` fields.
- The observed sequence supports command saturation / command NaN propagation
  as the proximate failure mechanism.
- Repeated goal publishing is not a necessary condition for this divergence.
  Repeated goal / replanning remains possible, but it is no longer the primary
  supported explanation.
- `ref_acc` remains unavailable or NaN, so acceleration-reference discontinuity
  is not fully ruled out.

## Test Setup

- method: `original`
- wind: `strong`, `wind_force_norm=0.0075`
- target: Trial 6, `target_x=0.0`, `target_y=1.5`
- command adaptation: none
- reference logging: enabled

## Test Table

| Run | goal_repeat | csv_path | valid_run_suggested | has_nan_state | first_nan_time | max_swing_angle_deg | max_uav_speed | max_payload_speed | final_uav_xy_error | has_reference_ratio | first_ref_nonfinite_time | first_ref_pos_jump_gt1m_time | first_ref_vel_jump_gt2mps_time | max_ref_speed | Divergence inspector classification |
| --- | ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | ---: | --- |
| `goal_repeat=1` smoke1 | 1 | not recorded | true | false | nan | 16.991189 | 2.493061 | 2.700187 | 0.000000 | 1.000000 | nan | nan | nan | not recorded | `command_saturation_without_divergence` |
| `goal_repeat=1` smoke2 | 1 | not recorded | true | false | nan | 21.079570 | 2.613695 | 3.040810 | 0.000000 | 1.000000 | nan | nan | nan | not recorded | `command_saturation_without_divergence` |
| `goal_repeat=1` smoke3 | 1 | not recorded | true | false | nan | 17.024791 | 2.448333 | 2.671744 | 0.000006 | 1.000000 | nan | nan | nan | not recorded | `command_saturation_without_divergence` |
| `goal_repeat=1` smoke4 | 1 | not recorded | false | true | 18.850118 | 155.687849 | 39.811251 | 40.331750 | 43.325351 | 1.000000 | nan | nan | nan | 2.507824 | `command_saturation_before_nan` |
| `goal_repeat=10` smoke1 | 10 | not recorded | not recorded | not recorded | not recorded | not recorded | not recorded | not recorded | not recorded | not recorded | not recorded | not recorded | not recorded | not recorded | not recorded |
| `goal_repeat=10` smoke2 | 10 | `/home/cccyn2004/projects/autotrans_ws/src/AutoTrans/experiments/logs/autotrans_log_20260510_232309.csv` | true | false | nan | 14.473151 | 2.409328 | 2.687449 | 0.000000 | 1.000000 | nan | nan | nan | not recorded | `command_saturation_without_divergence` |
| `goal_repeat=10` smoke3 | 10 | `/home/cccyn2004/projects/autotrans_ws/src/AutoTrans/experiments/logs/autotrans_log_20260510_232555.csv` | false | true | 19.850035 | 151.662901 | 41.344307 | 42.631983 | 389.140344 | 1.000000 | nan | nan | nan | 2.438584 | `command_saturation_before_nan` |
| `goal_repeat=10` smoke4 | 10 | `/home/cccyn2004/projects/autotrans_ws/src/AutoTrans/experiments/logs/autotrans_log_20260510_232856.csv` | true | false | nan | 13.112674 | 2.515147 | 2.559920 | 0.000000 | 1.000000 | nan | nan | nan | not recorded | `command_saturation_without_divergence` |

Observed command-saturation-before-NaN reproduction counts:

- `goal_repeat=1`: 1 out of 4 total smoke runs.
- `goal_repeat=10`: 1 out of 4 total smoke runs.

## Failure Timing Analysis

For failed `goal_repeat=10` smoke3, the timing sequence was:

1. Reference data was available and finite:
   `has_reference_ratio=1.000000`, `first_ref_nonfinite_time=nan`,
   `first_ref_pos_jump_gt1m_time=nan`, and
   `first_ref_vel_jump_gt2mps_time=nan`.
2. `so3_thrust` saturation appeared at `19.800008`.
3. `so3_thrust` and `so3_bodyrate` became NaN at `19.850035`.
   The first nonfinite column was `so3_thrust`.
4. Swing and speed thresholds occurred after `20.2s`:
   `first_swing_ge30_time=20.200154`,
   `first_swing_ge60_time=20.450036`,
   `first_uav_speed_gt4_time=20.400007`, and
   `first_payload_speed_gt4_time=20.600024`.
5. Position jumps occurred after `22.5s`:
   `first_uav_position_jump_gt1m_time=22.499977` and
   `first_payload_position_jump_gt1m_time=22.549998`.

This timing makes the command saturation / command NaN path the nearest
observed failure mechanism in smoke3. The reference stream did not provide
evidence of a nonfinite value or a large reference jump before the command NaN.

For failed `goal_repeat=1` smoke4, the timing sequence was:

1. Reference data was available and finite:
   `has_reference_ratio=1.000000`, `first_ref_nonfinite_time=nan`,
   `first_ref_pos_jump_gt1m_time=nan`, and
   `first_ref_vel_jump_gt2mps_time=nan`.
2. `so3_bodyrate` saturation appeared at `4.949898`.
3. `so3_thrust` and `so3_bodyrate` became NaN at `18.850118`.
   The first nonfinite column was `so3_thrust`.
4. UAV speed, payload speed, swing, and UAV position jump thresholds were all
   first detected at `18.850118`.

The failed `goal_repeat=1` smoke4 run shows that repeated goal publishing is
not a necessary condition for this divergence pattern.

## Interpretation

Transient command saturation can occur without divergence, as shown by valid
`goal_repeat=1` smoke1/smoke2/smoke3 and valid `goal_repeat=10` smoke2/smoke4.
Therefore, saturation alone is not sufficient to classify a run as failed in
these smoke diagnostics.

The failure-relevant pattern observed in the failed smoke runs is command
saturation followed by SO3 command NaN and state divergence. The downstream
high swing, high speed, and position jumps appeared after or together with the
command NaN event.

Because `goal_repeat=1` and `goal_repeat=10` each reproduced
`command_saturation_before_nan` in 1 out of 4 total smoke runs, repeated goal
publishing is not a necessary condition for this divergence. Repeated goal /
replanning remains possible as a contributing factor, but it is no longer the
primary supported explanation from these smoke results.

The evidence now points more toward an inherent strong-wind Trial 6 closed-loop
vulnerability involving SO3 command saturation / NaN propagation. Reference
logging did not show `ref_pos`/`ref_vel` nonfinite values or jumps in the
failed smoke runs. However, `ref_acc` remains unavailable or NaN, so
acceleration-reference discontinuity is not fully ruled out.

## Research Decision

- Do not resume Trial 6 fair expansion until this root-cause note is recorded.
- Repeated goal / replanning remains possible but is no longer the primary
  supported explanation.
- Next diagnostic should consider command NaN guard or improved SO3 command
  validity checks.
- Keep root-cause wording cautious.

## What Not To Claim

- Do not claim repeated goal is proven root cause.
- Do not claim planner reference discontinuity is proven.
- Do not claim all NaN failures are controller failures.
- Do not use these smoke tests as main success-rate results.
