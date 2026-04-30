# Stage 2-B Drag Wind 0.01 N Valid Result

## Basic Information

- Date: 2026-04-30
- Branch: wind-dynamics-experiment
- Commit SHA: 2d11ab60125f3ea551a0470139912c0425357667
- Trial name: stage2b_drag_x_cap_001_trial1
- Wind model: velocity-relative linear drag
- Valid run: yes

## Wind Settings

- enable_wind: true
- wind_model: drag
- wind_velocity_x: 0.5
- wind_velocity_y: 0.0
- wind_velocity_z: 0.0
- wind_drag_linear: 0.02
- wind_drag_quad: 0.0
- wind_max_force: 0.01
- wind_apply_to: quadrotor

## Metrics

- sample_count: 1864
- duration_sec: 93.149973
- effective_log_rate_hz: 20.000006
- valid_run_suggested: true
- has_nan_state: false
- final_row_has_nan: false
- nan_count_total: 0
- mean_swing_angle_deg: 1.015839
- max_swing_angle_deg: 20.029216
- p95_swing_angle_deg: 7.797072
- max_uav_speed: 2.498574
- mean_uav_speed: 0.179804
- max_payload_speed: 2.689931
- mean_payload_speed: 0.190982
- uav_path_length: 16.755470
- payload_path_length: 17.796514
- final_uav_position: (0.000000, -1.200000, 1.468415)
- final_payload_position: (0.000000, -1.200000, 0.799969)
- mean_wind_force_norm: 0.010000
- max_wind_force_norm: 0.010000

## Validity Decision

- Valid run: yes
- Reason:
  - no NaN or Inf state was detected
  - final UAV and payload positions are physically reasonable
  - max UAV and payload speeds stayed close to baseline range
  - max swing angle remained moderate
  - wind annotation was recorded correctly

## Interpretation

This first 0.01 N cap run is valid. Because previous 0.005 N tests showed one invalid run before later valid repeats, this setting should be repeated before being treated as a stable benchmark condition.
