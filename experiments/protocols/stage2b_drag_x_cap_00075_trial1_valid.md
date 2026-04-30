# Stage 2-B Drag Wind 0.0075 N Valid Result

## Basic Information

- Date: 2026-04-30
- Branch: wind-dynamics-experiment
- Commit SHA: a9ddb7f2702ecfbad59ebef6d8086466cc855c34
- Trial name: stage2b_drag_x_cap_00075_trial1
- Wind model: velocity-relative linear drag
- Valid run: yes

## Wind Settings

- enable_wind: true
- wind_model: drag
- wind_velocity_x: 0.5
- wind_velocity_y: 0.0
- wind_velocity_z: 0.0
- wind_drag_linear: 0.015
- wind_drag_quad: 0.0
- wind_max_force: 0.0075
- wind_apply_to: quadrotor

## Metrics

- sample_count: 1866
- duration_sec: 93.249961
- effective_log_rate_hz: 20.000008
- valid_run_suggested: true
- has_nan_state: false
- final_row_has_nan: false
- nan_count_total: 0
- mean_swing_angle_deg: 0.908961
- max_swing_angle_deg: 16.306677
- p95_swing_angle_deg: 6.663061
- max_uav_speed: 2.529105
- mean_uav_speed: 0.184430
- max_payload_speed: 2.522765
- mean_payload_speed: 0.196494
- uav_path_length: 17.206607
- payload_path_length: 18.330963
- final_uav_position: (0.000000, -1.200000, 1.468415)
- final_payload_position: (0.000000, -1.200000, 0.799970)
- mean_wind_force_norm: 0.007500
- max_wind_force_norm: 0.007500

## Validity Decision

- Valid run: yes
- Reason:
  - no NaN or Inf state was detected
  - final UAV and payload positions are physically reasonable
  - max UAV and payload speeds stayed close to baseline range
  - max swing angle remained moderate
  - wind annotation was recorded correctly
