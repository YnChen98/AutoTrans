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
Because no active guard exists yet, `guarded_command_applied` is currently
expected to remain `0` for all rows. An active C++ guard remains future
Stage 4-N4 work.

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

The corrected divergence audit also supports this pattern:

| Classification | Count |
| --- | ---: |
| `rows_inspected` | 177 |
| `command_saturation_before_nan` | 57 |
| `command_saturation_without_divergence` | 90 |
| `no_divergence_detected` | 7 |
| `strict_safety_no_nan` | 17 |
| `target_error_only` | 6 |

Transient command saturation alone is not a failure. The audit includes many
`command_saturation_without_divergence` rows, and Stage 4-M smoke tests also
showed valid runs with transient saturation. The failure-relevant pattern is
saturation followed by SO3 command NaN and then state divergence.

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

Stage 4-N3 logger/analyzer diagnostics should log or summarize:

- `command_invalid_event`
- `command_invalid_reason`
- `command_saturation_event`
- `command_saturation_reason`
- `sustained_command_saturation_event`
- `guarded_command_applied`

`guarded_command_applied` is currently false because Stage 4-N3 does not
modify controller or simulator command behavior. Future active guard work
should additionally log:

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

## What Not To Claim

- Do not claim the guard improves controller robustness.
- Do not claim final safety.
- Do not claim root cause is fully proven from one or two smoke runs.
- Do not replace unguarded main results with guarded diagnostic results.

## Next Coding Task

Stage 4-N3 detection/logging-first edit:

1. Add SO3 command diagnostic columns to `state_logger.py`.
2. Add analyzer support for `command_invalid_event`,
   `command_saturation_event`, `sustained_command_saturation_event`, and
   `guarded_command_applied`.
3. Run `python3 -m py_compile` for the edited Python scripts.

Recommended future Stage 4-N4 edit:

1. Inspect the SO3 command publication/subscription path.
2. Implement the guard disabled by default.
3. Add command guard logging.
4. Add analyzer support for `command_invalid_event` metrics.
5. Run `python3 -m py_compile` only before any ROS test.

Do not run `catkin_make`, `roslaunch`, RViz, simulation, or long-running trial
commands during the initial static edit unless explicitly requested.
