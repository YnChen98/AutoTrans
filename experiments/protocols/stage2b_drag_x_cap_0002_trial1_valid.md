# Stage 2-B Drag Wind Trial 1 Valid Result

## Basic Information

- Date: 2026-04-30
- Branch: wind-dynamics-experiment
- Commit SHA: 09096bcfd4e2f5fb43208965752250ca297d1d28
- Trial name: stage2b_drag_x_cap_0002_trial1
- Wind model: velocity-relative linear drag
- Valid run: yes

## Wind Settings

- enable_wind: true
- wind_model: drag
- wind_velocity_x: 0.5
- wind_velocity_y: 0.0
- wind_velocity_z: 0.0
- wind_drag_linear: 0.004
- wind_drag_quad: 0.0
- wind_max_force: 0.002
- wind_apply_to: quadrotor

## Metrics

- sample_count: 1862
- duration_sec: 93.049978
- effective_log_rate_hz: 20.000005
- valid_run_suggested: true
- has_nan_state: false
- final_row_has_nan: false
- mean_swing_angle_deg: 0.980346
- max_swing_angle_deg: 16.540037
- p95_swing_angle_deg: 8.745914
- max_uav_speed: 2.408148
- mean_uav_speed: 0.173970
- max_payload_speed: 2.590742
- mean_payload_speed: 0.181668
- uav_path_length: 16.195165
- payload_path_length: 16.910694
- final_uav_position: (-0.000000, -1.200000, 1.468415)
- final_payload_position: (-0.000000, -1.200000, 0.799970)
- mean_wind_force_norm: 0.002000
- max_wind_force_norm: 0.002000

## Validity Decision

- Valid run: yes
- Reason:
  - no NaN or Inf state was detected
  - final UAV and payload positions are physically reasonable
  - max speed stayed in the baseline range
  - max swing angle stayed moderate
  - wind annotation was recorded correctly

## Note

The /wind_force topic is currently an annotation signal from wind_signal_publisher, not the simulator-computed drag force. It was configured to match the force cap used in this trial.
