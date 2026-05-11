# Stage 4-N Command NaN Guard Diagnostic Design

## Executive Summary

Stage 4-N proposes a diagnostic command guard for SO3 command NaN events. The
guard should mark invalid command events and prevent NaN `so3_thrust` or
`so3_bodyrate` values from being forwarded into the simulator command path.

The guard must be disabled by default. It must not be used to claim improved
robustness unless it is separately evaluated and clearly described as a guarded
condition. The first goal is root-cause diagnosis, not performance improvement.

Any NaN command event should still make the run invalid. The guard is intended
to test whether teleport-like fly-away is caused by NaN command propagation
polluting simulator state, not to hide failures.

Stage 4-N3 is the detection/logging-first step. It adds logger/analyzer
diagnostics for SO3 command invalidity, finite saturation, sustained
saturation, and guarded-command status without changing the command path.

Stage 4-N4 is now implemented as an active C++ diagnostic guard in
`uav_simulator/so3_quadrotor/src/so3_quadrotor_nodelet.cpp::cmd_callback()`.
It is disabled by default through `enable_command_nan_guard: false`. When
enabled, it blocks NaN/Inf SO3 commands from being copied into simulator
command state, publishes `/so3_command_guard/guarded_command_applied`, and
optionally holds the last finite command. Guarded runs are diagnostic-only
runs, and NaN command events remain invalid safety events.

The latest timing-aware divergence audit narrows the expected scope of this
guard. It targets `command_nan_before_state_divergence` and
`command_saturation_before_nan` cases, but it may not prevent
`state_divergence_before_command_nan` cases.

## Motivation

Stage 4 divergence/root-cause analysis found that many invalid runs are
associated with SO3 command saturation, then command NaN, then state
divergence. A motivating example is original Trial 6 repeat10:

| Time | Observation |
| ---: | --- |
| `14.900` | saturated SO3 command: `so3_thrust=60.0`, `so3_bodyrate_x=-3.0`, `so3_bodyrate_y=3.0`, `so3_bodyrate_z=1.2` |
| `14.950` | `so3_thrust`/`so3_bodyrate` became NaN |
| `15.250` | UAV speed `> 4` and swing `> 30` |
| `15.299` | swing `> 60` |
| `15.849` | UAV position jump `> 1m` |

The latest corrected divergence audit shows mixed timing patterns:

| Classification | Count |
| --- | ---: |
| `rows_inspected` | 184 |
| `command_nan_before_state_divergence` | 1 |
| `command_saturation_before_nan` | 35 |
| `command_saturation_without_divergence` | 94 |
| `no_divergence_detected` | 7 |
| `state_divergence_before_command_nan` | 20 |
| `strict_safety_no_nan` | 21 |
| `target_error_only` | 6 |

Transient command saturation alone is not a failure. The audit includes many
`command_saturation_without_divergence` rows, and Stage 4-M smoke tests also
showed valid runs with transient saturation. The guard-relevant pattern is
saturation followed by SO3 command NaN and then state divergence, or command
NaN before state divergence.

The `state_divergence_before_command_nan` class is significant enough that an
active command NaN guard should not be presented as a complete failure fix. It
is a diagnostic protection against NaN command propagation, not a general
closed-loop robustness solution.

NaN command propagation can pollute simulator state because a nonfinite thrust
or bodyrate may enter integration, attitude, or force update logic. Once a NaN
or nonfinite command contaminates state variables, downstream logs can show
teleport-like fly-away, large speed spikes, large swing angle, and position
jumps. A diagnostic guard can block this propagation while still recording the
run as invalid.

Stage 4-M root-cause smoke results add two constraints:

- `goal_repeat=10` reproduced `command_saturation_before_nan` in 1/4 runs.
- `goal_repeat=1` also reproduced `command_saturation_before_nan` in 1/4 runs.
- Repeated goal publishing is not a necessary condition.
- Reference logging did not show `ref_pos`/`ref_vel` nonfinite values or jumps
  in the failed smoke runs.
- `ref_acc` remains unavailable or NaN, so acceleration-reference discontinuity
  is not fully ruled out.

## Candidate Guard Location

The exact command path should be inspected before implementation. Likely guard
locations include:

- SO3 command publisher.
- Controller output before simulator input.
- `uav_simulator` SO3 command callback.
- Logging layer only for detection if command path modification is too risky.

Preferred implementation should minimize behavioral surface and keep the guard
off by default. If command-path modification is too risky for the first pass,
the logging layer can provide detection-only metrics before an active guard is
introduced.

## Guard Behavior

The guard should treat NaN/Inf command values differently from finite
saturation.

If `so3_thrust` or any `so3_bodyrate` component is NaN/Inf:

- Mark `command_invalid_event`.
- Mark the run as diagnostic-invalid.
- Do not forward the NaN command.
- Optionally hold the last finite command for one control cycle, or publish a
  safe neutral command.

If the command is finite but saturated:

- Log `command_saturation_event`.
- Do not automatically fail the run.

If the command remains saturated for longer than a threshold:

- Log `sustained_command_saturation_event`.
- Optionally mark a diagnostic warning.

The guard must never silently convert an invalid run into a valid run. A NaN
command event is an invalid safety event even if the guard prevents simulator
state pollution.

## Safety and Claim Limits

- Guard must be off by default.
- Guarded runs should not be mixed with unguarded baseline runs.
- Guarded runs should be reported as diagnostic runs.
- Guard should never convert an invalid run into a valid run silently.
- Any NaN command event should remain an invalid safety event.
- Guarded results must not replace unguarded main success-rate results.

## Proposed Parameters

| Parameter | Default | Purpose |
| --- | --- | --- |
| `enable_command_nan_guard` | `false` | Enables the diagnostic guard. |
| `command_nan_guard_mode` | `mark_and_hold` | Marks invalid command events and holds/replaces NaN commands. |
| `command_nan_guard_hold_last_finite` | `true` | Uses the last finite SO3 command when a NaN/Inf command appears. |
| `command_saturation_log_only` | `true` | Logs finite saturation without marking the run invalid. |
| `thrust_saturation_threshold` | `59.9` | Diagnostic threshold near observed `so3_thrust=60.0` saturation. |
| `bodyrate_xy_saturation_threshold` | `2.99` | Diagnostic threshold near observed `so3_bodyrate_x/y=+-3.0` saturation. |
| `bodyrate_z_saturation_threshold` | `1.19` | Diagnostic threshold near observed `so3_bodyrate_z=1.2` saturation. |
| `sustained_saturation_duration_sec` | `0.2` | Duration threshold for sustained saturation warning. |

## Logging Requirements

Stage 4-N3/Stage 4-N4 logger/analyzer diagnostics should log or summarize:

- `command_invalid_event`
- `command_invalid_reason`
- `command_saturation_event`
- `command_saturation_reason`
- `sustained_command_saturation_event`
- `guarded_command_applied`

`guarded_command_applied` is read from
`/so3_command_guard/guarded_command_applied` when the Stage 4-N4 guard is
enabled. If that topic is absent, the logger keeps `guarded_command_applied=0`
for backward-compatible unguarded runs. A `1` value means the guard actively
blocked/replaced a nonfinite SO3 command. It does not make the run valid.

Future logging extensions may additionally log:

- `command_invalid_time`
- `last_finite_so3_thrust`
- `last_finite_so3_bodyrate_x`
- `last_finite_so3_bodyrate_y`
- `last_finite_so3_bodyrate_z`

The analyzer should preserve the distinction between:

- finite saturation without divergence,
- finite saturation followed by NaN command,
- NaN command blocked by the guard,
- state divergence despite finite commands.

## Root-Cause Test Plan

After implementation:

1. Rerun original Trial 6 strong wind `goal_repeat=1` smoke diagnostics.
2. Rerun original Trial 6 strong wind `goal_repeat=10` smoke diagnostics.
3. Compare unguarded behavior against guarded diagnostic behavior.
4. If teleport-like fly-away disappears after NaN command blocking, classify
   the fly-away as NaN-propagation-driven simulator pollution.
5. If fly-away still happens despite valid commands, investigate simulator,
   contact, or state integration behavior.

Guarded runs should be labeled explicitly and kept separate from main
unguarded baseline results.

The primary expected diagnostic value is in runs classified as
`command_nan_before_state_divergence` or `command_saturation_before_nan`. If a
run is classified as `state_divergence_before_command_nan`, the guard may still
record command validity, but it should not be expected to prevent the initial
divergence.

## What Not To Claim

- Do not claim the guard improves controller robustness.
- Do not claim final safety.
- Do not claim root cause is fully proven from one or two smoke runs.
- Do not replace unguarded main results with guarded diagnostic results.
- Do not claim the guard can prevent failures where state divergence precedes
  command NaN.

## Implementation Status

Stage 4-N3 detection/logging-first edit:

1. Add SO3 command diagnostic columns to `state_logger.py`.
2. Add analyzer support for `command_invalid_event`,
   `command_saturation_event`, `sustained_command_saturation_event`, and
   `guarded_command_applied`.
3. Run `python3 -m py_compile` for the edited Python scripts.

Stage 4-N4 active diagnostic guard edit:

1. Implemented the guard disabled by default in
   `uav_simulator/so3_quadrotor/src/so3_quadrotor_nodelet.cpp::cmd_callback()`.
2. Added `/so3_command_guard/guarded_command_applied` as a
   `std_msgs/Bool` diagnostic topic when the guard is enabled.
3. Updated `experiments/autotrans_logger/scripts/state_logger.py` so
   `guarded_command_applied` reflects the topic when present and remains `0`
   when absent.
4. Kept finite saturation as log-only behavior. Saturation alone does not
   trigger the active guard and should not be treated as invalid by itself.
5. Kept the guard scoped to NaN/Inf command propagation. It does not solve
   `state_divergence_before_command_nan` cases.

Do not run `catkin_make`, `roslaunch`, RViz, simulation, or long-running trial
commands during the initial static edit unless explicitly requested.
