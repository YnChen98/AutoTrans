# Stage 4-N4 Command NaN Guard Smoke Result

## Executive Summary

Stage 4-N4 command NaN guard diagnostic logging works. In guard-enabled
smoke3, `guarded_command_applied_count` became positive when the SO3 command
became NaN, with `guarded_command_applied_count=2043` and
`first_guarded_command_applied_time=26.400036`.

Guard-enabled smoke3 still failed, but the earliest failure mode was
`state_divergence_before_command_nan`. The first state divergence was at
`16.000039`, while the first command NaN and first guarded command event were
both at `26.400036`.

This means the guard can block and log later NaN command propagation, but it
cannot solve failures that begin with obstacle/path/state divergence before
command NaN. Guarded runs remain diagnostic-only and should not be used as main
evaluation baselines.

Stage 4-O records the path-feasibility / obstacle-collision interpretation in
`experiments/protocols/stage4o_path_feasibility_annotation_protocol.md`.
Smoke3 has an initial manual annotation entry in
`experiments/protocols/stage4o_manual_failure_annotations.json`.
Future reruns can use Stage 4-O3 `trajectory_publish_count` and trajectory
update timing to correlate obstacle pauses, apparent path changes, state
divergence, and later SO3 command NaN.

## Guard-disabled Smoke Summary

Configuration: original Trial 6, strong wind, `goal_repeat=10`,
`enable_command_nan_guard=false`.

- `csv_path=/home/cccyn2004/projects/autotrans_ws/src/AutoTrans/experiments/logs/autotrans_log_20260511_224658.csv`
- `valid_run_suggested=true`
- `has_nan_state=false`
- `max_swing_angle_deg=16.740599`
- `max_uav_speed=2.349563`
- `max_payload_speed=2.597483`
- `final_uav_xy_error=0.030583`
- `command_invalid_count=0`
- `command_saturation_count=15`
- `first_command_saturation_time=4.999977`
- `sustained_command_saturation_count=3`
- `first_sustained_command_saturation_time=5.200064`
- `guarded_command_applied_count=0`

This run stayed valid despite finite command saturation. It is another example
that transient saturation alone is a diagnostic signal, not a failure by
itself.

## Guard-enabled Smoke Summary Table

Configuration: original Trial 6, strong wind, `goal_repeat=10`,
`enable_command_nan_guard=true`.

| Run | Classification | Nonfinite | Saturation | High speed | Position jump | Swing threshold | First saturation time | Guarded count | Failure mode guess |
| --- | --- | --- | --- | --- | --- | --- | ---: | ---: | --- |
| smoke1 | `command_saturation_without_divergence` | false | true | false | false | false | `4.949995` | not reported | `command_saturation_without_divergence` |
| smoke2 | `command_saturation_without_divergence` | false | true | false | false | false | `4.900143` | not reported | `command_saturation_without_divergence` |
| smoke3 | `state_divergence_before_command_nan` | true | true | true | not primary | true | `5.049952` | `2043` | `state_divergence_before_command_nan` |

Smoke1 and smoke2 showed command saturation without divergence. Smoke3 showed
a later NaN command that activated the guard, but the divergence timing points
to an earlier state/path/obstacle problem.

## Smoke3 Timing Analysis

Guard-enabled smoke3 CSV:

- `csv_path=/home/cccyn2004/projects/autotrans_ws/src/AutoTrans/experiments/logs/autotrans_log_20260511_225654.csv`
- `valid_run_suggested=false`
- `has_nan_state=true`
- `first_nan_time=26.400036`
- `max_swing_angle_deg=175.229225`
- `max_uav_speed=20.494427`
- `max_payload_speed=23.781416`
- `final_uav_xy_error=112.415650`

Command diagnostics:

- `command_invalid_count=2043`
- `first_command_invalid_time=26.400036`
- `first_command_invalid_reason=so3_thrust,so3_bodyrate_x,so3_bodyrate_y,so3_bodyrate_z`
- `command_saturation_count=131`
- `first_command_saturation_time=5.049952`
- `sustained_command_saturation_count=96`
- `first_sustained_command_saturation_time=5.249984`
- `guarded_command_applied_count=2043`
- `first_guarded_command_applied_time=26.400036`

Divergence inspector timing:

- `classification=state_divergence_before_command_nan`
- `first_state_divergence_time=16.000039`
- `first_reference_jump_time=22.049979`
- `first_command_nan_time=26.400036`
- `reference_jump_after_divergence=true`
- `first_so3_thrust_saturation_time=26.349984`
- `first_so3_thrust_nan_time=26.400036`
- `first_so3_bodyrate_nan_time=26.400036`

The state divergence and swing threshold crossing appeared before command NaN.
The reference jump happened after divergence, so this smoke does not prove a
planner reference discontinuity as the root cause. The command NaN and
`guarded_command_applied` happened together at `26.400036`, after the run was
already divergent.

Therefore smoke3 is not a pure `command_nan_before_state_divergence` case. It
is better interpreted as state divergence first, followed by later command NaN
that the guard correctly logged and blocked from direct command-state copying.

## Manual Obstacle / Path Feasibility Observation

Manual observation for guard-enabled smoke3:

- The planned path appeared to pass through an obstacle.
- The UAV contacted or was blocked by the obstacle and paused.
- A new path appeared to be planned.
- The new path also appeared to pass through another obstacle.
- After another obstacle interaction or pause, the UAV suddenly teleported or
  flew away and became unstable.

This supports a path infeasibility / obstacle interaction interpretation. The
observed behavior is consistent with obstacle interaction followed by state
divergence, with command NaN occurring later rather than initiating the
failure. Under Stage 4-O, this smoke should be treated as
path/collision/state divergence before command NaN, not as a pure command NaN
failure.

## Research Decision

- Keep the command NaN guard as a diagnostic tool.
- Do not use guarded runs as main evaluation baselines.
- Do not claim the guard improves robustness.
- Add path-feasibility / collision annotation before using this smoke as
  evidence about controller quality.
- Next work should inspect path feasibility or add collision/path annotations.

## What Not To Claim

- Do not claim the active guard solves Trial 6 failures.
- Do not claim smoke3 failure was caused by command NaN.
- Do not claim planner reference discontinuity is proven solely by the
  reference jump, because the reference jump occurred after divergence.
- Do not treat guarded diagnostic runs as comparable to unguarded baselines.
