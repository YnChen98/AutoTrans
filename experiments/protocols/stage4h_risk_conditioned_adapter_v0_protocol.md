# Stage 4-H Risk-Conditioned Command Adapter v0 Protocol

## Purpose

Stage 4-H adds a conservative online adapter that uses early risk predictions
from exported LogisticRegression JSON models to reduce planner command scale.
The v0 adapter is a soft experimental policy. It is not a hard safety guard and
must not be used to claim final robustness.

## Architecture

The adapter is an external ROS node in:

```bash
experiments/command_adaptation/scripts/risk_conditioned_command_adapter.py
```

It publishes the existing planner-side command adaptation topics and never
modifies planner, controller, simulator, or logger internals.

The launch file is:

```bash
experiments/command_adaptation/launch/risk_conditioned_command_adapter.launch
```

Default launch behavior is safe: `enable_risk_conditioning=false` and
`policy_mode=wind_level`.

## Topics

Subscribed:

- `/visual_slam/odom` (`nav_msgs/Odometry`)
- `/payload_odom` (`nav_msgs/Odometry`)
- `/wind_force` (`geometry_msgs/Vector3Stamped`)
- `/move_base_simple/goal` (`geometry_msgs/PoseStamped`)
- `/planning/trajectory` as an optional has-trajectory signal

Published:

- `/command_adaptation/speed_scale` (`std_msgs/Float64`)
- `/command_adaptation/acceleration_scale` (`std_msgs/Float64`)
- `/command_adaptation/risk_score_3s` (`std_msgs/Float64`)
- `/command_adaptation/risk_score_5s` (`std_msgs/Float64`)
- `/command_adaptation/risk_scale_selected` (`std_msgs/Float64`)
- `/command_adaptation/risk_target_scale_raw` (`std_msgs/Float64`)

## Required Diagnostics

Risk-score logging is required before evaluating the v0 policy. A run that only
records `command_speed_scale` and `command_acceleration_scale` can prove that
the adapter was active, but it cannot show whether the LogisticRegression model
predicted risk early enough or whether the risk-to-scale rule was too weak.

`autotrans_logger` should record these CSV columns for every Stage 4-H run:

- `command_risk_score_3s`
- `command_risk_score_5s`
- `command_risk_scale_selected`
- `command_risk_target_scale_raw`

Analyze the log with target-error arguments so the risk diagnostics can be read
together with `valid_run_suggested`, `first_nan_time`, and final target errors:

```bash
python3 experiments/autotrans_logger/scripts/analyze_log.py \
  --csv <log.csv> \
  --target_x <x> \
  --target_y <y> \
  --target_z <z> \
  --payload_target_z <payload_z> \
  --target_xy_tolerance 0.5
```

Use `first_finite_command_risk_score_3s_time`,
`first_finite_command_risk_score_5s_time`,
`first_command_risk_score_3s_ge_0p5_time`,
`first_command_risk_score_5s_ge_0p5_time`,
`first_command_risk_score_5s_ge_0p7_time`,
`first_swing_angle_ge_30_time`,
`first_swing_angle_ge_60_time`,
`first_payload_speed_ge_4_time`,
`first_uav_speed_ge_4_time`,
`first_command_scale_below_0p85_time`, and
`first_command_scale_below_0p75_time`,
`first_command_risk_target_scale_raw_below_0p85_time`,
`first_command_risk_target_scale_raw_below_0p75_time`, and
`first_command_risk_target_scale_raw_below_0p65_time` to diagnose timing:

- If `first_nan_time` occurs before the first finite risk-score time, the model
  did not produce a usable risk estimate before the failure.
- If risk scores are finite before `first_nan_time` but command scale drops late
  or not far enough, inspect `command_risk_target_scale_raw`,
  `command_risk_scale_selected`, and the threshold parameters before changing
  the policy.
- If `command_risk_target_scale_raw` crosses below `0.85`, `0.75`, or `0.65`
  early but `command_risk_scale_selected` crosses late, the risk trigger likely
  fired but `scale_rate_limit_per_sec` was too slow for the failure timing.
- If `command_risk_target_scale_raw` does not drop until after
  `first_swing_angle_ge_30_time`, `first_swing_angle_ge_60_time`,
  `first_payload_speed_ge_4_time`, or `first_uav_speed_ge_4_time`, diagnose a
  late prediction or high threshold before changing the rate limit.
- If risk scores stay low before an invalid run, treat it as model prediction
  evidence, not as a planner/controller conclusion.

## Parameters

Core parameters:

- `enable_risk_conditioning`, default `false`
- `policy_mode`, default `wind_level`
- `model_json_3s`
- `model_json_5s`
- `model_json_15s`
- `target_z`, default `1.468415`
- `payload_target_z`, default `0.799970`
- `publish_rate`, default `5.0`
- `scale_rate_limit_per_sec`, default `0.5`
- `publish_same_acceleration_scale`, default `true`
- `same_goal_position_tolerance`, default `0.05`
- `episode_idle_timeout_sec`, default `3.0`
- `same_goal_new_episode_timeout_sec`, default `10.0`
- `reset_scale_on_new_episode`, default `true`
- `reset_on_new_distinct_goal`, default `true`
- `reset_on_first_trajectory_after_goal`, default `false`

Risk policy parameters:

- `risk_threshold_3s`, default `0.5`
- `risk_threshold_5s`, default `0.5`
- `hard_threshold_5s`, default `0.7`
- `soft_scale_3s`, default `0.85`
- `soft_scale_5s`, default `0.75`
- `hard_scale_5s`, default `0.65`
- `min_scale`, default `0.4`
- `max_scale`, default `1.0`

Wind-level fallback parameters match `heuristic_command_adapter.py`:

- `weak_wind_norm`, default `0.002`
- `moderate_wind_norm`, default `0.005`
- `strong_wind_norm`, default `0.0075`
- `boundary_wind_norm`, default `0.010`
- `no_wind_scale`, default `1.0`
- `weak_scale`, default `0.95`
- `moderate_scale`, default `0.90`
- `strong_scale`, default `0.85`
- `boundary_scale`, default `0.70`

## Feature Computation

The episode buffer resets on an accepted `/move_base_simple/goal`. Repeated
`/move_base_simple/goal` messages with the same 3D position inside one active
trial do not reset the buffer. Two goals are treated as the same when their 3D
position distance is below `same_goal_position_tolerance`, default `0.05` m.
This prevents repeated baseline-trial goal publication from clearing the early
odometry window.

Repeated run loops must still start clean episodes. The same goal after
`same_goal_new_episode_timeout_sec`, default `10.0` s, is accepted as a new
episode and resets the online buffers, cached risk scores, raw/selected risk
scale state, and rate-limit previous scale when `reset_scale_on_new_episode=true`.
If finite `/visual_slam/odom` stops for `episode_idle_timeout_sec`, default
`3.0` s, the adapter treats the gap as a cross-trial boundary, clears stale
episode state in the timer loop, clears cached risk scores, resets the raw
risk target scale to the wind-level base scale, and makes the next goal start a
new episode.

For a new distinct goal, `reset_on_new_distinct_goal=true` keeps the default
behavior of starting a fresh episode. `/planning/trajectory` is used only to
mark `has_trajectory=true` by default. It does not reset the episode unless
`reset_on_first_trajectory_after_goal=true`, and it should never reset on every
trajectory publication.

The v0 features are computed from the first 3 seconds and first 5 seconds after
the current episode start. In a normal run with stable odometry, the first finite
3s risk score should appear after about 3 seconds of episode history, and the
first finite 5s risk score should normally appear about 2 seconds after the 3s
score. A 5s score appearing tens of seconds later is evidence to inspect episode
reset diagnostics before changing risk-to-scale thresholds.

At the start of every repeated run, `command_risk_score_3s` and
`command_risk_score_5s` should remain `-1` until enough fresh 3s/5s data has
been collected. High finite risk scores or a selected scale already below the
wind-level base scale near time 0 indicate stale episode state and should be
treated as a bug in reset handling. A stale risk score at about time 0 means the
adapter failed to reset; it is not possible evidence from a fresh 5s online
feature window. The expected fresh repeat behavior is `risk_score=-1` until the
3s and 5s windows are available, with timer-based idle reset clearing cached
risk scores before the next trial starts.

Online features follow the JSON `feature_names` order and names:

- `max_uav_speed`
- `max_payload_speed`
- `mean_uav_speed`
- `mean_payload_speed`
- `max_swing_angle_deg`
- `p95_swing_angle_deg`
- `mean_swing_angle_deg`
- `max_wind_force_norm`
- `mean_wind_force_norm`
- `target_distance_end`
- `target_progress`

Target fields are:

- `target_x` and `target_y` from the latest `/move_base_simple/goal`
- `target_z` from ROS param
- `payload_target_z` from ROS param

If no goal has been received, the adapter publishes fallback scale and risk
score `-1`.

## Risk-To-Scale v0

Let `base_scale` be the wind-level fallback scale.

The adapter publishes two scale diagnostics:

- `risk_target_scale_raw` is the raw policy target after risk thresholding and
  clamping, before rate limiting.
- `risk_scale_selected` is the rate-limited selected scale and should match the
  scale actually published through `/command_adaptation/speed_scale`.

If `enable_risk_conditioning=false`, publish `base_scale`.

If risk conditioning is enabled:

- before 3 seconds of usable history, publish `base_scale`
- after 3 seconds, compute `risk_score_3s`
- after 5 seconds, compute `risk_score_5s`

Scale rule:

- start with `selected_scale = base_scale`
- if `risk_score_3s >= risk_threshold_3s`, use `min(selected_scale, soft_scale_3s)`
- if `risk_score_5s >= risk_threshold_5s`, use `min(selected_scale, soft_scale_5s)`
- if `risk_score_5s >= hard_threshold_5s`, use `min(selected_scale, hard_scale_5s)`
- clamp to `[min_scale, max_scale]`; this is published as
  `/command_adaptation/risk_target_scale_raw`
- rate-limit both decreasing and increasing scale changes; this is published as
  `/command_adaptation/risk_scale_selected`

The same value is published to `speed_scale` and `acceleration_scale` in v0.

## Safety Rules

- No-op/fallback by default.
- No hard stop.
- Never publish NaN.
- Never publish outside `[min_scale, max_scale]`.
- Ignore non-finite odometry or wind input and keep the previous safe value.
- If a required online feature cannot be computed, fall back safely.
- If a model file is missing or invalid, log `ROS_WARN` and use wind-level
  fallback.
- If model output is non-finite, keep the previous safe scale.
- Never command thrust or bodyrate.
- Do not run `catkin_make`, `roslaunch`, RViz, simulation, or long trial
  commands from Codex for this task.

## First Tests

Static check:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 -m py_compile experiments/command_adaptation/scripts/risk_conditioned_command_adapter.py
git diff --check
git status --short
```

Manual no-risk regression, run by the user when ready:

```bash
roslaunch command_adaptation risk_conditioned_command_adapter.launch enable_risk_conditioning:=false
```

Confirm that `/command_adaptation/speed_scale` and
`/command_adaptation/acceleration_scale` match wind-level fallback behavior
before any risk-conditioned experiment.

## What Not To Claim

- Do not claim online robustness improvement before repeated closed-loop
  evaluation.
- Do not claim RL.
- Do not claim real-world robustness.
- Do not claim a hard safety guarantee.
- Do not hide invalid runs.
- Do not claim `risk_conditioned_v0` is better than `windlevel_s085` until
  repeated comparisons support that conclusion.
