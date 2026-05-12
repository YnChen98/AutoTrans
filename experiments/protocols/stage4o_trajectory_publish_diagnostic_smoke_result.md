# Stage 4-O3 Trajectory Publish Diagnostic Smoke Result

## Executive Summary

Stage 4-O3 trajectory publish / replan-proxy logging works. The diagnostic
smoke logs recorded `trajectory_publish_count_final`,
`trajectory_update_count_final`, `first_trajectory_time`, and related
trajectory timing fields.

All three O3 diagnostic smoke runs were valid. They did not reproduce NaN or
teleport-like divergence. O3 does not prove path feasibility; it only records
trajectory update timing so future failure analysis can compare trajectory
updates against strict-valid metrics, divergence labels, and manual
path/collision annotations.

## Test Setup

- method: `original`
- wind: `strong`
- target: Trial 6, `x=0.0`, `y=1.5`
- `goal_repeat=10`
- command guard: disabled
- purpose: diagnostic only, not main success-rate evaluation

## Smoke Result Table

| Run | `valid_run_suggested` | `has_nan_state` | `max_swing_angle_deg` | `max_uav_speed` | `max_payload_speed` | `final_uav_xy_error` | `trajectory_publish_count_final` | `trajectory_update_count_final` | `first_trajectory_time` | `trajectory_updates_before_first_swing_ge_30` | `command_invalid_count` | `command_saturation_count` | `failure_mode_guess` |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| smoke1 | `true` | `false` | `14.558318` | `2.465875` | `2.615684` | `0.008815` | `19` | `19` | `4.879453` |  | `0` | `1` | `command_saturation_without_divergence` |
| smoke2 | `true` | `false` | `46.740986` | `2.479898` | `2.871543` | `0.122258` | `14` | `14` | `4.932055` | `10` | `0` | `18` | `swing_warning_no_nan` |
| smoke3 | `true` | `false` | `17.652202` | `2.497194` | `2.527261` | `0.111052` | `16` | `16` | `4.806906` |  | `0` | `27` | `command_saturation_without_divergence` |

## Detailed Smoke Metrics

### smoke1

- `csv_path=/home/cccyn2004/projects/autotrans_ws/src/AutoTrans/experiments/logs/autotrans_log_20260512_104605.csv`
- `final_trajectory_time_since_last_update=83.427264`
- `max_trajectory_time_since_last_update=83.427264`
- `first_command_saturation_time=5.350061`
- `sustained_command_saturation_count=0`
- `guarded_command_applied_count=0`
- `has_reference_ratio=1.000000`
- `first_ref_nonfinite_time=nan`
- `first_ref_pos_jump_gt1m_time=nan`
- `first_ref_vel_jump_gt2mps_time=nan`

### smoke2

- `csv_path=/home/cccyn2004/projects/autotrans_ws/src/AutoTrans/experiments/logs/autotrans_log_20260512_104851.csv`
- `final_trajectory_time_since_last_update=108.129911`
- `max_trajectory_time_since_last_update=108.129911`
- `first_command_saturation_time=4.949995`
- `sustained_command_saturation_count=10`
- `guarded_command_applied_count=0`
- `has_reference_ratio=1.000000`
- `first_ref_nonfinite_time=nan`
- `first_ref_pos_jump_gt1m_time=nan`
- `first_ref_vel_jump_gt2mps_time=nan`

### smoke3

- `csv_path=/home/cccyn2004/projects/autotrans_ws/src/AutoTrans/experiments/logs/autotrans_log_20260512_105136.csv`
- `final_trajectory_time_since_last_update=94.118523`
- `max_trajectory_time_since_last_update=102.322837`
- `first_command_saturation_time=4.849939`
- `sustained_command_saturation_count=14`
- `guarded_command_applied_count=0`
- `has_reference_ratio=1.000000`
- `first_ref_nonfinite_time=nan`
- `first_ref_pos_jump_gt1m_time=nan`
- `first_ref_vel_jump_gt2mps_time=nan`

## Interpretation

The trajectory publish / update counters are now usable for diagnostic logs.
The three O3 smoke runs did not reproduce the obstacle/path/divergence event
seen in N4 smoke3.

smoke2 had a swing warning but not a strict failure: `max_swing_angle_deg`
exceeded `30 deg` but stayed below `60 deg`, UAV/payload speed stayed below
`4 m/s`, and no NaN occurred. Its corrected divergence inspector label is
`swing_warning_no_nan`, not `strict_safety_no_nan`.

Transient command saturation can occur in valid runs. `trajectory_update_count`
alone does not prove replanning root cause or path infeasibility because it is
only a weak replan proxy for the `planning/trajectory` stream.

## Taxonomy Note

`swing_angle_deg >= 30` is now warning-only. `strict_safety_no_nan` is reserved
for stronger violations such as `swing_angle_deg >= 60`, UAV/payload speed
`>= 4 m/s`, position jump, or other strict invalid conditions. Paper-facing
results should continue to use strict-valid / `label_strict_invalid`.

Latest divergence-inspector batch taxonomy after the swing-warning fix:

| Failure-mode guess | Count |
| --- | ---: |
| rows inspected | `191` |
| `command_nan_before_state_divergence` | `1` |
| `command_saturation_before_nan` | `35` |
| `command_saturation_without_divergence` | `99` |
| `no_divergence_detected` | `7` |
| `state_divergence_before_command_nan` | `21` |
| `strict_safety_no_nan` | `7` |
| `swing_warning_no_nan` | `14` |
| `target_error_only` | `7` |

## Research Decision

O3 logging is ready for future diagnostic runs. Do not use these O3 smokes as
main success-rate evidence.

Future failure analysis should join:

- strict-valid metrics
- divergence `failure_mode_guess`
- trajectory update counts
- manual path/collision annotations

## What Not To Claim

- Do not claim no path infeasibility exists based on these three valid smokes.
- Do not claim trajectory update count proves replanning root cause.
- Do not claim command saturation alone indicates failure.
- Do not treat diagnostic smokes as final balanced comparison.
