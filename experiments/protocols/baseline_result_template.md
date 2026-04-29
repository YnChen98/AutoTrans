# AutoTrans Baseline Result Template

## Run Metadata

- date:
- branch:
- commit SHA:
- run label:
- operator:

## Commands

- launch command:

```bash
cd ~/projects/autotrans_ws
source /opt/ros/noetic/setup.bash
source devel/setup.bash
roslaunch payload_planner simple_run.launch
```

- logger command:

```bash
cd ~/projects/autotrans_ws
source /opt/ros/noetic/setup.bash
source devel/setup.bash
roslaunch autotrans_logger state_logger.launch
```

- analyze command:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/autotrans_logger/scripts/analyze_log.py --csv <CSV filename>
```

## Trial Setup

- CSV filename:
- target point:
- planned run duration:
- actual run duration:
- notes before run:

## Metrics

- sample_count:
- duration_sec:
- effective_log_rate_hz:
- has_trajectory_ratio:
- mean_swing_angle_deg:
- max_swing_angle_deg:
- p95_swing_angle_deg:
- max_uav_speed:
- mean_uav_speed:
- max_payload_speed:
- mean_payload_speed:
- uav_path_length:
- payload_path_length:
- final_uav_position:
- final_payload_position:

## Qualitative Notes From RViz

- planning response:
- trajectory shape:
- obstacle avoidance behavior:
- payload swing visual impression:
- hover/settling behavior:
- abnormal events:

## Validity Decision

- whether the run is valid:
- reason:
- include in baseline comparison:

## Follow-Up Notes

- comparison target:
- suspected issue if invalid:
- recommended next run:
