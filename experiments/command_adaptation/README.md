# Stage 3-B Heuristic Command Adapter

`command_adaptation` provides the first heuristic runtime command adaptation node for AutoTrans Stage 3-B. It publishes planner-side speed and acceleration scale commands for the existing runtime topic interface.

## Topics

Published:

- `/command_adaptation/speed_scale` (`std_msgs/Float64`)
- `/command_adaptation/acceleration_scale` (`std_msgs/Float64`)

Subscribed:

- `/visual_slam/odom` (`nav_msgs/Odometry`)
- `/payload_odom` (`nav_msgs/Odometry`)
- `/wind_force` (`geometry_msgs/Vector3Stamped`)
- `/planning/trajectory` (`quadrotor_msgs/PolynomialTraj`)

`/wind_force` is an annotation signal and must match the selected Stage 2-B drag-wind level.

## Build

```bash
cd ~/projects/autotrans_ws
source /opt/ros/noetic/setup.bash
source devel/setup.bash 2>/dev/null || true
catkin_make -DCMAKE_BUILD_TYPE=Release
```

## Launch Adapter

```bash
roslaunch command_adaptation heuristic_command_adapter.launch
```

Default `policy_mode` is `wind_level`, which selects scale only from `/wind_force` level and is the current recommended mode for formal strong-wind repeated validation.

The previous reactive v1 behavior is still available as an experimental option:

```bash
roslaunch command_adaptation heuristic_command_adapter.launch policy_mode:=risk_reactive
```

## Echo Scale Topics

```bash
rostopic echo /command_adaptation/speed_scale
rostopic echo /command_adaptation/acceleration_scale
```

## Logged Diagnostics

`autotrans_logger` records the latest command adaptation values in each CSV row:

- `command_speed_scale`
- `command_acceleration_scale`
- `command_risk_score_3s`
- `command_risk_score_5s`
- `command_risk_scale_selected`
- `command_risk_target_scale_raw`

`analyze_log.py` summarizes these columns when finite data is available and generates:

- `command_speed_scale.png`
- `command_acceleration_scale.png`
- `command_risk_score_3s.png`
- `command_risk_score_5s.png`
- `command_risk_scale_selected.png`
- `command_risk_target_scale_raw.png`

For Stage 4-H diagnostics, use the risk-score summaries to decide whether an
invalid run failed before risk activation or after risk activation:

- `first_finite_command_risk_score_3s_time`
- `first_finite_command_risk_score_5s_time`
- `first_command_risk_score_3s_ge_0p5_time`
- `first_command_risk_score_5s_ge_0p5_time`
- `first_command_risk_score_5s_ge_0p7_time`
- `first_swing_angle_ge_30_time`
- `first_swing_angle_ge_60_time`
- `first_payload_speed_ge_4_time`
- `first_uav_speed_ge_4_time`
- `first_command_scale_below_0p85_time`
- `first_command_scale_below_0p75_time`
- `first_command_risk_target_scale_raw_below_0p85_time`
- `first_command_risk_target_scale_raw_below_0p75_time`
- `first_command_risk_target_scale_raw_below_0p65_time`

If `first_nan_time` is earlier than the first finite risk-score time, the model
did not produce a usable online risk estimate before failure. If risk scores are
finite before `first_nan_time` but scale reduction is late or weak, inspect
`command_risk_target_scale_raw`, `command_risk_scale_selected`, and the
risk-to-scale thresholds before changing planner, controller, or simulator code.
`command_risk_target_scale_raw` is the policy's immediate target before rate
limiting. `command_risk_scale_selected` is the rate-limited selected scale that
is actually published to the planner as `/command_adaptation/speed_scale`. If
the raw target drops early but the selected scale crosses late, the rate limit
is likely too slow for the observed failure timing. If the raw target itself
drops only after `first_swing_angle_ge_30_time`, `first_swing_angle_ge_60_time`,
`first_payload_speed_ge_4_time`, or `first_uav_speed_ge_4_time`, treat the
prediction or threshold trigger as too late before changing the policy.

Current strong-wind trial evidence is summarized in `experiments/protocols/stage3b_heuristic_strong_trial_summary.md`; the current `policy_mode=wind_level` strong-wind summary is in `experiments/protocols/stage3b_windlevel_strong_trial_summary.md`.

## Stage 4-H Risk-Conditioned Adapter v0

`risk_conditioned_command_adapter.py` is the first Stage 4-H online adapter. It
keeps the existing planner topic interface and adds soft risk-conditioned scale
selection from exported LogisticRegression JSON models. It does not use
`sklearn`, does not command thrust/bodyrate, and does not modify planner,
controller, or simulator code.

Published:

- `/command_adaptation/speed_scale` (`std_msgs/Float64`)
- `/command_adaptation/acceleration_scale` (`std_msgs/Float64`)
- `/command_adaptation/risk_score_3s` (`std_msgs/Float64`)
- `/command_adaptation/risk_score_5s` (`std_msgs/Float64`)
- `/command_adaptation/risk_scale_selected` (`std_msgs/Float64`)
- `/command_adaptation/risk_target_scale_raw` (`std_msgs/Float64`)

Subscribed:

- `/visual_slam/odom` (`nav_msgs/Odometry`)
- `/payload_odom` (`nav_msgs/Odometry`)
- `/wind_force` (`geometry_msgs/Vector3Stamped`)
- `/move_base_simple/goal` (`geometry_msgs/PoseStamped`)
- `/planning/trajectory` as an optional has-trajectory signal

Episode timing is anchored to an accepted `/move_base_simple/goal`. Repeated
goal messages with the same position inside one active trial do not reset the
feature buffer. This is important because `run_baseline_trial.sh` republishes
`/move_base_simple/goal`; those repeated messages are ignored so they do not
clear the early odometry window. A goal is treated as the same when its 3D
position is within `same_goal_position_tolerance`, default `0.05` m. The same
goal after `same_goal_new_episode_timeout_sec`, default `10.0` s, is treated as
a new episode and resets stale online state. Repeated run loops also require
odom idle-gap handling: if finite `/visual_slam/odom` stops for
`episode_idle_timeout_sec`, default `3.0` s, the adapter clears the episode
buffers, cached risk scores, and risk scale diagnostics in the timer loop before
the next trial begins. The next goal then starts fresh. `/planning/trajectory`
does not reset the episode by default; it only marks `has_trajectory=true` and
can initialize timing only if no active episode exists.

Default launch settings are conservative:

```bash
roslaunch command_adaptation risk_conditioned_command_adapter.launch
```

By default `enable_risk_conditioning=false` and `policy_mode=wind_level`, so the
node behaves like the wind-level fallback and publishes risk scores as
unavailable (`-1`) until risk conditioning is explicitly enabled. Missing or
invalid model JSON files do not crash the node; the adapter logs `ROS_WARN` and
falls back to wind-level scale selection.

Useful episode timing parameters:

- `same_goal_position_tolerance`, default `0.05`
- `episode_idle_timeout_sec`, default `3.0`
- `same_goal_new_episode_timeout_sec`, default `10.0`
- `reset_scale_on_new_episode`, default `true`
- `reset_on_new_distinct_goal`, default `true`
- `reset_on_first_trajectory_after_goal`, default `false`

With stable odometry and one active episode, the first finite
`/command_adaptation/risk_score_3s` should appear after about 3 seconds of
episode history, and `/command_adaptation/risk_score_5s` should normally appear
about 2 seconds later. If the 5s score appears much later, check for episode
reset logs before changing the risk thresholds or planner settings. At the
start of a repeated run, both risk scores should publish `-1` until enough fresh
3s/5s data exists. A finite or high stale risk score at about time 0 indicates
a failed reset, not a valid model prediction from a fresh online feature window.
The timer-based idle reset is expected to clear cached risk scores before the
next trial, so `/command_adaptation/risk_score_3s` and
`/command_adaptation/risk_score_5s` remain unavailable (`-1`) until their
windows are available.

Generated model JSON files live under:

```bash
experiments/models/stage4_risk_logreg_3s.json
experiments/models/stage4_risk_logreg_5s.json
experiments/models/stage4_risk_logreg_15s.json
```

These files are generated artifacts and are ignored by git. Do not commit them
unless the project policy changes explicitly.

First use should be a no-risk regression check: start with
`enable_risk_conditioning=false`, confirm the published scale matches the
existing `wind_level` behavior, and only then enable risk conditioning for a
limited trial. The v0 policy is a soft candidate for repeated validation, not a
hard safety guard and not final evidence of robustness.

## Strong Wind Experiment

Set the simulator drag-wind level:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/set_drag_wind_config.py --level strong
```

Launch the wind annotation signal with the same cap:

```bash
roslaunch autotrans_logger wind_signal_publisher.launch enable_wind:=true wind_mode:=constant wind_force_x:=0.0075 wind_max_force:=0.0075
```

Launch the heuristic adapter:

```bash
roslaunch command_adaptation heuristic_command_adapter.launch
```

Use planner topic mode with readiness enabled:

- `manager/enable_command_adaptation=true`
- `manager/adaptation_mode=topic`
- `manager/require_adaptation_topic_ready=true`

Then run the baseline trial:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
bash experiments/scripts/run_baseline_trial.sh --name stage3b_heuristic_strong_trial2 --x -7.5 --y 1.5 --z 0.0 --duration 75
```

Restore no wind after wind experiments:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/set_drag_wind_config.py --level none
```
