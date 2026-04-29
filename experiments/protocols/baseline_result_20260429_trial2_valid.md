# Baseline Trial 2 Valid Result

## Basic Information

- Date: 2026-04-29
- Branch: autotrans-deploy
- Commit SHA: 8cc237e55cce89364269dc079a8ccc7b6dfe6ef1
- Trial name: trial2
- Run type: non-interactive terminal runner
- Valid run: yes

## Target Point

- target_x: -7.5
- target_y: 1.5
- target_z: 0.0

## Metrics

- sample_count: 1881
- duration_sec: 93.999974
- effective_log_rate_hz: 20.000006
- has_trajectory_ratio: 0.944710
- mean_swing_angle_deg: 0.505330
- max_swing_angle_deg: 12.296728
- p95_swing_angle_deg: 4.312139
- max_uav_speed: 2.495637
- mean_uav_speed: 0.092891
- max_payload_speed: 2.629185
- mean_payload_speed: 0.097504
- uav_path_length: 8.623168
- payload_path_length: 9.012220
- final_uav_position: (-7.500000, 1.500000, 1.468415)
- final_payload_position: (-7.500000, 1.500000, 0.799970)

## Validity Decision

- Valid run: yes
- Reason:
  - final UAV position matches the target
  - final payload position is physically reasonable
  - max UAV and payload speeds are reasonable
  - swing angle remains moderate
  - trajectory was received for most of the run
