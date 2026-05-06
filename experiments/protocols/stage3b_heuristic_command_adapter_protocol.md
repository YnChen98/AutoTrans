# Stage 3-B Heuristic Command Adapter Protocol

## Purpose

Stage 3-B introduces a learning-compatible high-level command adaptation framework. The first implementation is a heuristic policy node that publishes runtime planner scale commands. It is not an RL policy.

## Method

The node `heuristic_command_adapter.py` observes odometry, payload state, wind annotation, and trajectory availability. It publishes speed and acceleration scale commands to the planner runtime adaptation interface.

The first version uses the same value for `speed_scale` and `acceleration_scale` so results can be compared against fixed-scale baselines such as `0.85`.

## Topic Interface

Published:

- `/command_adaptation/speed_scale` (`std_msgs/Float64`)
- `/command_adaptation/acceleration_scale` (`std_msgs/Float64`)

Subscribed:

- `/visual_slam/odom` (`nav_msgs/Odometry`)
- `/payload_odom` (`nav_msgs/Odometry`)
- `/wind_force` (`geometry_msgs/Vector3Stamped`)
- `/planning/trajectory` (`quadrotor_msgs/PolynomialTraj`)

`/wind_force` is an annotation signal. It must be configured to match the selected drag-wind cap.

## Logged Diagnostics

`autotrans_logger` records command adaptation values when the topics are available:

- `command_speed_scale`
- `command_acceleration_scale`

`analyze_log.py` computes mean/min/max/final metrics for both scale columns when finite data exists. It also generates:

- `command_speed_scale.png`
- `command_acceleration_scale.png`

## Parameters

Default policy parameters:

- `policy_mode: wind_level`
- `publish_rate: 5.0`
- `min_scale: 0.4`
- `max_scale: 1.0`
- `weak_wind_norm: 0.002`
- `moderate_wind_norm: 0.005`
- `strong_wind_norm: 0.0075`
- `boundary_wind_norm: 0.010`
- `no_wind_scale: 1.0`
- `weak_scale: 0.95`
- `moderate_scale: 0.90`
- `strong_scale: 0.85`
- `boundary_scale: 0.70`
- `swing_warn_deg: 20.0`
- `swing_critical_deg: 35.0`
- `swing_warn_scale: 0.65`
- `swing_critical_scale: 0.50`
- `speed_warn: 3.2`
- `speed_critical: 4.0`
- `speed_warn_scale: 0.65`
- `speed_critical_scale: 0.50`
- `recent_speed_window_sec: 3.0`
- `scale_rate_limit_per_sec: 0.5`
- `publish_same_acceleration_scale: true`

## Policy Modes

`policy_mode=wind_level` is the current default and recommended mode for formal strong-wind repeated validation. It selects scale only from `/wind_force` thresholds:

- no wind: `1.0`
- weak: `0.95`
- moderate: `0.90`
- strong: `0.85`
- boundary: `0.70`

This mode still computes swing angle and recent max speed for diagnostics, but it does not use them to reduce scale.

`policy_mode=risk_reactive` preserves the original Stage 3-B v1 behavior. It starts from the same wind-level base scale and then applies swing/speed overrides that can reduce scale to `0.65` or `0.50`.

The risk-reactive v1 policy produced mixed strong-wind results and should be treated as experimental until further tuning.

## Safety Behavior

- If no odometry has been received, publish `1.0`.
- If no `/wind_force` has been received, treat it as no wind and publish `1.0`.
- If an input contains NaN or Inf, ignore that input and keep the previous safe value.
- Always clamp output to `[min_scale, max_scale]`.
- Rate-limit scale changes using `scale_rate_limit_per_sec`.
- Publish both scale topics every timer tick so planner topic readiness can be satisfied.

## Test Sequence

1. Compile the Python node:

   ```bash
   python3 -m py_compile experiments/command_adaptation/scripts/heuristic_command_adapter.py
   ```

2. Build the workspace:

   ```bash
   cd ~/projects/autotrans_ws
   source /opt/ros/noetic/setup.bash
   source devel/setup.bash 2>/dev/null || true
   catkin_make -DCMAKE_BUILD_TYPE=Release
   ```

3. Launch the adapter alone and echo outputs:

   ```bash
   roslaunch command_adaptation heuristic_command_adapter.launch
   rostopic echo /command_adaptation/speed_scale
   rostopic echo /command_adaptation/acceleration_scale
   ```

4. Verify wind-level behavior with `/wind_force`:

   - no wind: expected scale `1.0`
   - strong wind norm `0.0075`: expected target scale `0.85`
   - boundary wind norm `0.010`: expected target scale `0.70`

5. Run strong wind Trial 2 with planner topic readiness enabled.

## Validity Criteria

- No NaN/Inf is published on either command adaptation topic.
- Published scale is always within `[0.4, 1.0]` by default.
- Logged command scale plots should be inspected when a run becomes invalid or drops below the wind-level base scale.
- In no wind with no motion, scale remains `1.0`.
- In strong wind annotation, `policy_mode=wind_level` target scale reaches `0.85`.
- In boundary wind annotation, `policy_mode=wind_level` target scale reaches `0.70`.
- Strong wind Trial 2 should be compared against fixed `0.85` and topic fixed-publisher `0.85` baselines.

## What Not To Do

- Do not modify planner, controller, simulator, logger, analyzer, or baseline runner for the first heuristic policy.
- Do not implement RL in Stage 3-B first pass.
- Do not treat `/wind_force` as simulator-computed drag force; it is an annotation topic.
- Do not run boundary wind as a default benchmark. Use it as a stress test.
