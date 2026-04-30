# Stage 2-B Drag Wind 0.005 N Valid Repeat Result

## Basic Information

- Date: 2026-04-30
- Branch: wind-dynamics-experiment
- Commit SHA: 284acb8acd0dcb2156a88d0bdd40b07c9e32c7be
- Trial name: stage2b_drag_x_cap_0005_repeat_valid
- Wind model: velocity-relative linear drag
- Valid run: yes

## Wind Settings

- enable_wind: true
- wind_model: drag
- wind_velocity_x: 0.5
- wind_velocity_y: 0.0
- wind_velocity_z: 0.0
- wind_drag_linear: 0.01
- wind_drag_quad: 0.0
- wind_max_force: 0.005
- wind_apply_to: quadrotor

## Metrics

- sample_count: 1866
- duration_sec: 93.249954
- effective_log_rate_hz: 20.000010
- valid_run_suggested: true
- has_nan_state: false
- final_row_has_nan: false
- nan_count_total: 0
- mean_swing_angle_deg: 1.769865
- max_swing_angle_deg: 24.968412
- p95_swing_angle_deg: 10.997162
- max_uav_speed: 2.503634
- mean_uav_speed: 0.204297
- max_payload_speed: 2.523190
- mean_payload_speed: 0.233565
- uav_path_length: 19.057325
- payload_path_length: 21.784858
- final_uav_position: (-0.000000, -1.200000, 1.468415)
- final_payload_position: (-0.000000, -1.200000, 0.799970)
- mean_wind_force_norm: 0.005000
- max_wind_force_norm: 0.005000

## Validity Decision

- Valid run: yes
- Reason:
  - no NaN or Inf state was detected
  - final UAV and payload positions are physically reasonable
  - max speed stayed close to baseline range
  - max swing angle stayed below the invalid threshold
  - wind annotation was recorded correctly

## Interpretation

This repeat run shows that 0.005 N cap is not deterministically unstable. However, because a previous 0.005 N run produced NaNs, this disturbance level should be treated as a boundary case requiring repeated trials before being used as a stable benchmark setting.
