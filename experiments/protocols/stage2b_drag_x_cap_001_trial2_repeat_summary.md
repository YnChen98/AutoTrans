# Stage 2-B Drag Wind 0.01 N Trial 2 Repeat Results

## Basic Information

- Date: 2026-05-02
- Branch: wind-dynamics-experiment
- Commit SHA: 627937bbeb7da7b9625c3e00d0bbb2401ca38c33
- Wind model: velocity-relative linear drag
- Wind setting: wind_velocity_x=0.5, wind_drag_linear=0.02, wind_max_force=0.01, apply_to=quadrotor

## Trial 2 Repeat 3

- CSV: experiments/logs/autotrans_log_20260502_213101.csv
- Target: (-7.5, 1.5)
- Valid run: yes
- valid_run_suggested: true
- has_nan_state: false
- final_row_has_nan: false
- mean_swing_angle_deg: 0.463672
- max_swing_angle_deg: 13.377811
- p95_swing_angle_deg: 2.466608
- max_uav_speed: 2.450659
- max_payload_speed: 2.499570
- final_uav_position: (-7.500000, 1.500000, 1.468415)
- final_payload_position: (-7.500000, 1.500000, 0.799970)
- mean_wind_force_norm: 0.010000
- max_wind_force_norm: 0.010000

## Trial 2 Repeat 4

- CSV: experiments/logs/autotrans_log_20260502_213424.csv
- Target: (-7.5, 1.5)
- Valid run: no
- valid_run_suggested: false
- has_nan_state: true
- first_nan_time: 9.949938
- final_row_has_nan: true
- nan_count_total: 25128
- max_swing_angle_deg: 12.668662
- max_uav_speed: 32.274055
- max_payload_speed: 32.273042
- final_uav_position: (-23.097321, -18.472280, 156.618029)
- final_payload_position: (-23.031883, -18.402435, 155.956471)
- last_row_uav_position: (nan, nan, nan)
- last_row_payload_position: (nan, nan, nan)
- mean_wind_force_norm: 0.010000
- max_wind_force_norm: 0.010000

## Conclusion

The 0.01 N cap setting is not robust enough for Trial 2. It can succeed, but repeated runs still produce NaN failures. Do not use 0.01 N as the current formal stable benchmark.

Next step: test 0.0075 N cap on Trial 2 and Trial 3 with repeated runs. If 0.0075 N remains valid, use it as the current strong wind benchmark. If it fails, fall back to 0.005 N or lower.
