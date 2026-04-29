# Baseline Trial 3 Valid Result

## Basic Information

- Date: 2026-04-29
- Branch: autotrans-deploy
- Commit SHA: f0aba235b56d86ce5b5cc20daace486b5ff46cff
- Trial name: trial3_retry_target_8_1p5
- Run type: non-interactive terminal runner
- Valid run: yes

## Target Point

- target_x: 8.0
- target_y: 1.5
- target_z: 0.0

## CSV File

- CSV filename: experiments/logs/autotrans_log_20260429_214826.csv

## Metrics

- sample_count: 1866
- duration_sec: 93.250107
- effective_log_rate_hz: 19.999977
- has_trajectory_ratio: 0.946945
- mean_swing_angle_deg: 1.161237
- max_swing_angle_deg: 14.561213
- p95_swing_angle_deg: 9.055607
- max_uav_speed: 2.500430
- mean_uav_speed: 0.270821
- max_payload_speed: 2.528286
- mean_payload_speed: 0.277163
- uav_path_length: 25.253174
- payload_path_length: 25.854523
- final_uav_position: (8.000000, 1.500000, 1.468415)
- final_payload_position: (8.000000, 1.500000, 0.799970)

## Qualitative Notes

Trial 3 is a valid baseline run. The UAV converged to the intended target (8.0, 1.5), and the payload settled below the UAV at the expected relative height. The transient swing is moderate and does not indicate divergence.

This valid retry confirms that the previous Trial 3 invalid result was likely caused by command input pollution or insufficient argument validation rather than an inherent failure of the target point.

## Validity Decision

- Valid run: yes
- Reason:
  - final UAV position matches the intended target
  - final payload position is physically reasonable
  - final altitude is consistent with other valid baseline trials
  - max UAV and payload speeds are reasonable
  - swing angle remains within a usable baseline range
  - trajectory was received for most of the run
