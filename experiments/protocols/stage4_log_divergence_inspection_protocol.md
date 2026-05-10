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

## What The Tool Computes

For each CSV log, the tool reports timing for:

- evidence flags for nonfinite values, command saturation, high speed,
  position jump, and swing threshold crossing
- first nonfinite value and its column
- first SO3 thrust/bodyrate NaN
- first SO3 thrust/bodyrate saturation
- first UAV/payload speed thresholds at `4 m/s` and `10 m/s`
- first swing thresholds at `30 deg` and `60 deg`
- first UAV/payload position jump above `1 m`
- first `has_trajectory` time
- last finite UAV/payload position before the first nonfinite value when
  available

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
commands, UAV/payload high speed, swing threshold crossing, or position jump.
It should not be treated as an invalid divergence label.

`command_saturation_without_divergence` means SO3 thrust or bodyrate reached
the configured saturation threshold, but no NaN/nonfinite state, high-speed
divergence, position jump, or swing threshold crossing was detected. Transient
command saturation alone is a diagnostic signal, not necessarily a failure.
Valid runs may still receive this label when saturation is transient and no
invalid evidence follows.

`command_saturation_before_nan` should be used only when command saturation
precedes a nonfinite SO3/state value, or precedes high-speed/position-jump
divergence when no NaN is available.

Command NaN before state divergence is possible. In those cases, the first
visible fly-away may be downstream of an earlier command failure.

`unknown_invalid` should be reserved for cases where analyzer metrics indicate
`valid_run_suggested=false` or `has_nan_state=true`, but the inspector cannot
classify the failure from available CSV evidence.

Failure-mode guesses are heuristic labels. They should be paired with
strict-valid / `label_strict_invalid` when preparing paper-facing result
tables.

Obstacle collision and path infeasibility remain manual annotations unless
they are explicitly logged. Visual inspection is still required for cases
where the UAV appears to contact an obstacle or where the planned path appears
to pass through an obstacle.

Historical logs without `ref_*` columns do not include the full reference
trajectory. Therefore planner trajectory discontinuity or planned
path-through-obstacle behavior cannot be proven from those CSVs alone.
