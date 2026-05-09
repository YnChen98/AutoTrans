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

`analyze_log.py` summarizes these columns when finite data is available and generates:

- `command_speed_scale.png`
- `command_acceleration_scale.png`
- `command_risk_score_3s.png`
- `command_risk_score_5s.png`
- `command_risk_scale_selected.png`

For Stage 4-H diagnostics, use the risk-score summaries to decide whether an
invalid run failed before risk activation or after risk activation:

- `first_finite_command_risk_score_3s_time`
- `first_finite_command_risk_score_5s_time`
- `first_command_scale_below_0p85_time`
- `first_command_scale_below_0p75_time`

If `first_nan_time` is earlier than the first finite risk-score time, the model
did not produce a usable online risk estimate before failure. If risk scores are
finite before `first_nan_time` but scale reduction is late or weak, inspect
`command_risk_scale_selected` and the risk-to-scale thresholds before changing
planner, controller, or simulator code.

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

Subscribed:

- `/visual_slam/odom` (`nav_msgs/Odometry`)
- `/payload_odom` (`nav_msgs/Odometry`)
- `/wind_force` (`geometry_msgs/Vector3Stamped`)
- `/move_base_simple/goal` (`geometry_msgs/PoseStamped`)
- `/planning/trajectory` as an optional has-trajectory signal

Default launch settings are conservative:

```bash
roslaunch command_adaptation risk_conditioned_command_adapter.launch
```

By default `enable_risk_conditioning=false` and `policy_mode=wind_level`, so the
node behaves like the wind-level fallback and publishes risk scores as
unavailable (`-1`) until risk conditioning is explicitly enabled. Missing or
invalid model JSON files do not crash the node; the adapter logs `ROS_WARN` and
falls back to wind-level scale selection.

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
