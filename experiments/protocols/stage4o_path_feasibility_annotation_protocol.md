# Stage 4-O Path Feasibility Annotation Protocol

## Executive Summary

Stage 4-O introduces manual path-feasibility and obstacle-collision
annotation for invalid Stage 4 runs. This is needed because some failures
appear to involve a planned path passing through an obstacle, obstacle
contact, or blocking behavior before later state divergence or SO3 command
NaN.

These mechanisms should not be collapsed into command-adaptation failure or
command-NaN failure. Stage 4-O is annotation/protocol only: planner,
controller, simulator, and logger behavior remain unchanged unless a later
task explicitly requests implementation work.

## Motivation

Stage 4-N4 guard-enabled smoke3 showed that the active SO3 command NaN guard
can diagnose later NaN command propagation: `guarded_command_applied_count`
became positive when SO3 command NaN appeared. However, the divergence
inspector classified that smoke as `state_divergence_before_command_nan`.

Manual visual observation during that run suggested an upstream path or
obstacle mechanism: the planned path appeared to pass through an obstacle, the
UAV appeared to pause at obstacle contact or blockage, a new path appeared to
be planned through another obstacle, and a later obstacle interaction was
followed by teleport-like fly-away.

Therefore the command NaN guard can help diagnose later NaN propagation, but
it cannot explain failures that start with obstacle/path/state divergence
before command NaN.

## Current System Coverage

### Obstacle / Map Representation

`/map_generator/global_cloud` is published from
`uav_simulator/map_generator/src/map_generator.cpp` as obstacle point cloud
data. `local_sensing_node` receives the global cloud, downsamples it, builds a
KD tree, and publishes a local rendered cloud. The planner map in
`planner/plan_env` maintains occupancy, inflated occupancy, and ESDF through
`grid_map`.

### Planned Trajectory Representation

`planning/trajectory` is published from
`planner/plan_manage/src/replan_fsm.cpp`. Its message type is
`quadrotor_msgs::PolynomialTraj`, which contains polynomial pieces and
coefficients rather than directly sampled path points.

The controller subscribes to `planning/trajectory` and also publishes
`mpc/all_ref_data`, `mpc/reference_trajectory`, and
`mpc/trajectory_predicted`. `mpc/all_ref_data` is current reference-like data,
not full planned path geometry.

### Existing Collision / Feasibility Checks

A* checks occupancy and ESDF. The trajectory optimizer checks collision by
sampling with `dt=0.01`, but only over part of the trajectory. A runtime
collision check exists in `planner/plan_manage/src/replan_fsm.cpp` and may
trigger replan or emergency stop.

These failure states are not currently published as structured logger fields.
They may appear only as planner state transitions or ROS log messages.

### Current Logger Limitations

`experiments/autotrans_logger/scripts/state_logger.py` logs UAV/payload state,
SO3 command diagnostics, `guarded_command_applied`, swing angle,
`has_trajectory`, wind, command adaptation, risk scores, and current reference
position/velocity.

It does not log full planned path/control points, obstacle clearance,
collision/contact flags, replan count, goal publish count, or path feasibility
flag.

Stage 4-O3 adds low-risk trajectory publish / replan-proxy diagnostics in
`experiments/autotrans_logger/scripts/state_logger.py`. The logger now records
`trajectory_publish_count`, `trajectory_update_count`,
`trajectory_last_update_time`, `trajectory_time_since_last_update`, and
`first_trajectory_time` from the `planning/trajectory` stream. For now,
`trajectory_update_count` is the same as `trajectory_publish_count` because
there is no reliable duplicate-vs-new-trajectory discriminator.

These fields are not proof of a replan and do not prove path infeasibility.
They can indicate trajectory updates near obstacle pauses, state divergence,
SO3 command NaN, or swing threshold crossings. Path infeasibility still
requires manual annotation or a later automatic path/ESDF checking pipeline.

## Manual Annotation Fields

- `manual_collision_observed`: boolean. True when visual observation shows
  obstacle contact or clear physical blocking.
- `manual_path_infeasible`: boolean. True when the planned path visibly passes
  through an obstacle or into occupied space.
- `manual_obstacle_stop_observed`: boolean. True when the UAV pauses or stalls
  at obstacle contact or apparent blockage.
- `manual_teleport_after_collision`: boolean. True when teleport-like fly-away
  follows an observed obstacle/collision interaction.
- `path_feasibility_unknown`: boolean. True when no visual evidence is
  available to judge path feasibility.
- `collision_observed_time`: number or null. Approximate observation time in
  seconds when obstacle contact/blocking was first observed.
- `path_through_obstacle_observed`: boolean. True when the displayed planned
  path appeared to pass through an obstacle.
- `manual_failure_note`: string. Short free-form explanation of the observed
  path/collision evidence and timing.
- `annotation_source`: string. Source of the annotation, such as manual visual
  observation, screen recording, screenshot review, or RViz replay.
- `annotation_confidence`: string. Recommended values are `low`, `medium`, and
  `high`.

## Annotation Rules

Set `manual_collision_observed=true` only when visual observation shows
obstacle contact or clear physical blocking.

Set `manual_path_infeasible=true` when the planned path visibly passes through
an obstacle or into occupied space.

Set `manual_obstacle_stop_observed=true` when the UAV pauses or stalls at
obstacle contact or apparent blockage.

Set `manual_teleport_after_collision=true` when teleport-like fly-away follows
an observed obstacle/collision interaction.

Set `path_feasibility_unknown=true` when no visual evidence is available. Do
not infer collision solely from NaN, high speed, swing threshold crossing, a
large final error, or command saturation.

If visual evidence is ambiguous, keep the confidence at `low` or `medium` and
write the uncertainty in `manual_failure_note`.

## Relationship To Failure-Mode Labels

`command_saturation_before_nan` remains a timing label for finite command
saturation followed by command NaN. A manual path/collision annotation can
coexist with it when obstacle interaction appears before or near the command
failure.

`state_divergence_before_command_nan` should be paired with manual
path/collision annotation when visual evidence shows path infeasibility or
obstacle interaction before SO3 command NaN.

`command_nan_before_state_divergence` should not be reinterpreted as collision
without direct visual or logged obstacle evidence.

`strict_safety_no_nan` may still receive manual path/collision annotations if
the run violates safety through obstacle contact, blocking, excessive swing,
or target failure without NaN.

`target_error_only` means the available CSV evidence primarily shows target
miss. If visual evidence shows path infeasibility or obstacle blocking, record
that separately in the manual annotation fields.

## Use In Paper-Facing Results

Success/failure should still use strict-valid / `label_strict_invalid`.
Manual annotations explain failure cause; they do not replace success metrics.

Failure-mode distribution should be reported alongside success rates when
there is enough evidence. Do not claim all failures are control-policy
failures. Do not claim all `risk_adapter` failures are risk model false
negatives when path infeasibility, obstacle interaction, or unlogged planner
behavior may be involved.

Guarded diagnostic runs remain diagnostic only and should not be mixed into
unguarded baseline success-rate claims.

## Future Automatic Feasibility Checks

Possible future work:

- sample `quadrotor_msgs::PolynomialTraj` against ESDF
- compute `min_path_obstacle_distance`
- log `path_collision_flag`
- use a proximity heuristic from UAV/payload position to obstacle point cloud
- refine `trajectory_publish_count` into a stronger `replan_like_trajectory_count`
  if a reliable duplicate-vs-new-trajectory discriminator becomes available
- defer planner behavior modification until manual annotations show this
  failure mode is frequent enough to justify deeper integration

Automatic checks should start as logging or offline post-processing. Planner
behavior changes and simulator contact-sensor modifications should be treated
as higher-risk follow-up work.
