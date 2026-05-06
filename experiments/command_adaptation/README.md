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

## Echo Scale Topics

```bash
rostopic echo /command_adaptation/speed_scale
rostopic echo /command_adaptation/acceleration_scale
```

## Logged Diagnostics

`autotrans_logger` records the latest command adaptation values in each CSV row:

- `command_speed_scale`
- `command_acceleration_scale`

`analyze_log.py` summarizes these columns when finite data is available and generates:

- `command_speed_scale.png`
- `command_acceleration_scale.png`

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
