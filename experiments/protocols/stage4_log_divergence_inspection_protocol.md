# Stage 4 Log Divergence Inspection Protocol

## Purpose

Stage 4 invalid runs include several sudden fly-away or teleport-like failures
after apparently stable flight. These failures need separate classification
because a simple valid/invalid label does not explain whether the run failed
from target error, strict safety violation, command saturation, command NaN,
state divergence, obstacle contact, or path feasibility.

`experiments/scripts/inspect_stage4_log_divergence.py` is an offline CSV
inspection helper. It does not run ROS, simulation, RViz, or `catkin_make`.

## Motivating Example

A detailed inspection of original Trial 6 repeat10 showed:

- first nonfinite value: `so3_thrust` at `t=14.950161`
- at `t=14.900`, SO3 commands were saturated:
  - `so3_thrust=60.0`
  - `so3_bodyrate_x=-3.0`
  - `so3_bodyrate_y=3.0`
  - `so3_bodyrate_z=1.2`
- `first_uav_speed_gt4` occurred later at `t=15.250058`
- `first_payload_speed_gt4` occurred later at `t=15.350023`
- `first_uav_position_jump_gt1m` occurred later at `t=15.849978`

This ordering suggests that command saturation or command NaN can precede
state divergence. The inspection tool is intended to make that timing
repeatable instead of relying on ad hoc manual checks.

## Reference Logging

Stage 4 root-cause diagnosis now requires desired/reference command logging in
addition to state and SO3 command logging. In the current `simple_run.launch`
flow, `payload_mpc_controller` publishes current MPC reference data on
`/mpc_controller_node/mpc/all_ref_data` as `nav_msgs/Path`; pose 0 stores
reference position and pose 1 stores reference velocity. `autotrans_logger`
uses this topic by default when `enable_reference_logging=true`.

The logger also supports `quadrotor_msgs/PositionCommand` on `/position_cmd`
by setting `reference_message_type=position_command` and
`reference_topic=/position_cmd` for launch flows that publish that command
topic.

The CSV records available fields as:

- `ref_pos_x`, `ref_pos_y`, `ref_pos_z`
- `ref_vel_x`, `ref_vel_y`, `ref_vel_z`
- `ref_acc_x`, `ref_acc_y`, `ref_acc_z`
- `ref_yaw`
- `ref_yaw_dot`
- `ref_msg_ros_time`
- `ref_available`

For `/mpc_controller_node/mpc/all_ref_data`, acceleration and yaw-rate are not
available and remain blank. For `quadrotor_msgs/PositionCommand`, position,
velocity, acceleration, yaw, and yaw-rate are logged directly.

Without these reference columns, planner reference discontinuity cannot be
proven from CSV logs alone. `has_trajectory` only confirms that a trajectory
message was seen; it does not expose the desired position, velocity, or
acceleration being tracked by the controller.

When analyzing new logs, inspect reference metrics such as
`first_ref_pos_jump_gt1m_time`, `first_ref_vel_jump_gt2mps_time`,
`first_ref_acc_gt5_time`, and `first_ref_acc_gt10_time`. A reference position
jump or acceleration spike before SO3 saturation would support a reference or
trajectory discontinuity hypothesis. SO3 saturation before any reference
spike would point away from a simple logged-reference discontinuity and toward
controller saturation, simulator/contact interaction, numerical instability,
or an unlogged planner/controller mechanism.

## SO3 Command Validity Diagnostics

Stage 4-N3 adds logger-level SO3 command diagnostics to `autotrans_logger`.
These fields are derived from the raw `/so3cmd`
`mavros_msgs/AttitudeTarget` stream and do not modify the command path:

- `command_invalid_event`
- `command_invalid_reason`
- `command_saturation_event`
- `command_saturation_reason`
- `sustained_command_saturation_event`
- `guarded_command_applied`

`command_invalid_event` is set when `so3_thrust` or any
`so3_bodyrate_*` field is NaN/Inf. `command_saturation_event` is set when a
finite SO3 command reaches the diagnostic threshold:
`so3_thrust >= 59.9`, `abs(so3_bodyrate_x/y) >= 2.99`, or
`abs(so3_bodyrate_z) >= 1.19`. `sustained_command_saturation_event` is set
when the saturation condition remains true for at least `0.2s` by default.

For unguarded runs, or when `/so3_command_guard/guarded_command_applied` is
absent, `guarded_command_applied` remains `0`. Stage 4-N4 adds an optional
active diagnostic guard, disabled by default, that publishes this topic as
`std_msgs/Bool`. A value of `1` means the guard actively blocked/replaced a
NaN/Inf SO3 command before it was copied into simulator command state.

`guarded_command_applied=1` must be interpreted as a diagnostic-invalid safety
event, not as a successful robustness correction. It can help test whether a
teleport-like fly-away was caused by NaN command propagation, but it does not
explain or solve `state_divergence_before_command_nan` cases. These fields help
distinguish transient finite saturation from saturation that is followed by
command NaN and state divergence.

## What The Tool Computes

For each CSV log, the tool reports timing for:

- evidence flags for nonfinite values, command saturation, high speed,
  position jump, `swing_angle_deg >= 30` warning, and strict safety violation
- first nonfinite value and its column
- first SO3 thrust/bodyrate NaN
- first SO3 thrust/bodyrate saturation
- first UAV/payload speed thresholds at `4 m/s` and `10 m/s`
- first swing thresholds at `30 deg` and `60 deg`
- first UAV/payload position jump above `1 m`
- first `has_trajectory` time
- last finite UAV/payload position before the first nonfinite value when
  available
- logger-level command invalidity and sustained saturation metrics when the
  Stage 4-N3 columns are available

For batch mode, it reads `*_metrics_summary.txt` files, extracts the referenced
`csv_path`, and combines analyzer summary fields with the same CSV divergence
inspection.

## Usage

Inspect one CSV around a suspected divergence window:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/inspect_stage4_log_divergence.py \
  --csv experiments/logs/autotrans_log_20260510_190453.csv \
  --window-start 13.5 \
  --window-end 16.5 \
  --print-summary
```

Scan all metrics summaries and write an ignored report:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/inspect_stage4_log_divergence.py \
  --metrics-glob "experiments/figures/*_metrics_summary.txt" \
  --output-csv experiments/results/stage4_log_divergence_report.csv \
  --print-summary
```

Generated reports under `experiments/results/` should not be committed.

## Failure Mode Caveats

The `failure_mode_guess` field is best-effort. It is intended for triage and
manifest annotation, not as a definitive physical diagnosis.

`no_divergence_detected` means the CSV did not show nonfinite state/SO3
commands, UAV/payload high speed, strict swing threshold crossing, position
jump, target-error evidence, or `swing_angle_deg >= 30` warning. It should not
be treated as an invalid divergence label.

`command_saturation_without_divergence` means SO3 thrust or bodyrate reached
the configured saturation threshold, but no NaN/nonfinite state, high-speed
divergence, position jump, strict swing threshold crossing, or `swing_angle_deg
>= 30` warning was detected. Transient command saturation alone is a diagnostic
signal, not necessarily a failure. Valid runs may still receive this label when
saturation is transient and no invalid or warning evidence follows.

`swing_warning_no_nan` means the run crossed `swing_angle_deg >= 30` without
NaN/nonfinite values, without strict safety violation, and without target-error
failure evidence. This is a diagnostic warning, not a paper-facing strict
invalid label by itself.

`strict_safety_no_nan` is reserved for stronger no-NaN safety evidence:
`swing_angle_deg >= 60`, UAV/payload speed `>= 4 m/s`, UAV/payload position
jump `> 1 m`, or target-error failure evidence tracked separately as
`target_error_only`. The strict-valid / `label_strict_invalid` fields remain
the paper-facing metric for success-rate tables.

`command_saturation_before_nan` should be used only when command saturation
precedes command NaN and command NaN occurs before or near state divergence.
It should not be used for transient finite saturation that never develops
into NaN or state divergence.

The inspector now reports aggregate timing fields for root-cause ordering:

- `first_command_nan_time`
- `first_state_divergence_time`
- `first_reference_jump_time`
- `first_swing_warning_time`
- `first_strict_safety_violation_time`
- `first_reference_nonfinite_time`
- `first_command_saturation_time`
- `reference_jump_after_divergence`

`first_swing_warning_time` is the first `swing_angle_deg >= 30` event.
`first_strict_safety_violation_time` is the first high-speed, position jump,
or `swing_angle_deg >= 60` event. `first_state_divergence_time` follows the
strict safety timing and does not treat `swing_angle_deg >= 30` alone as state
divergence for warning-only runs; when a run later has command NaN or strict
safety violation, the `swing_angle_deg >= 30` time is retained as early
state-divergence timing for ordering. `first_command_nan_time` is the
earliest nonfinite SO3 thrust/bodyrate value. `first_reference_jump_time` is
the earliest reference position jump, reference velocity jump, or finite
reference acceleration spike when those fields are available.

Command NaN before state divergence is possible. In those cases, the first
visible fly-away may be downstream of an earlier command failure. Command NaN
and state divergence may also be coincident within one logger sample period,
especially when the log rate is too low to resolve the exact ordering.

State divergence before command NaN is also possible. In those cases, the
first detected high-speed, `swing_angle_deg >= 60`, position-jump, or early
`swing_angle_deg >= 30` warning that precedes a later strict/NaN failure
appears before any logged SO3 command NaN. Those runs should not be explained
solely as command NaN propagation.

Late reference jumps must not be over-interpreted. If a reference jump occurs
after command NaN or after state divergence, the inspector sets
`reference_jump_after_divergence=true` and does not classify the run as
`reference_jump_before_command_nan`.

`unknown_invalid` should be reserved for cases where analyzer metrics indicate
`valid_run_suggested=false` or `has_nan_state=true`, but the inspector cannot
classify the failure from available CSV evidence.

Failure-mode guesses are heuristic labels. They provide timing-based triage,
not definitive physical causality. They should be paired with strict-valid /
`label_strict_invalid` when preparing paper-facing result tables.

Current batch-audit labels include:

- `command_nan_before_state_divergence`
- `command_saturation_before_nan`
- `command_saturation_without_divergence`
- `no_divergence_detected`
- `state_divergence_before_command_nan`
- `strict_safety_no_nan`
- `swing_warning_no_nan`
- `target_error_only`

Additional labels may appear for targeted single-log diagnostics when evidence
supports them:

- `command_nan_coincident_with_state_divergence`
- `reference_jump_before_command_nan`
- `reference_jump_after_divergence`
- `unknown_invalid`

Obstacle collision and path infeasibility remain manual annotations unless
they are explicitly logged. Visual inspection is still required for cases
where the UAV appears to contact an obstacle or where the planned path appears
to pass through an obstacle.

When such visual evidence exists, combine the divergence label with the
Stage 4-O manual path/collision annotations in
`experiments/protocols/stage4o_manual_failure_annotations.json`. For example,
`state_divergence_before_command_nan` plus `manual_path_infeasible=true` and
`manual_collision_observed=true` should be interpreted as a path/collision
failure candidate before later SO3 command NaN, not as pure command NaN
propagation.

Historical logs without `ref_*` columns do not include the full reference
trajectory. Therefore planner trajectory discontinuity or planned
path-through-obstacle behavior cannot be proven from those CSVs alone.
