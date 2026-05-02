# Stage 2-B Drag Wind 0.01 N Target Trials Summary

## Basic Information

- Date: 2026-05-02
- Branch: wind-dynamics-experiment
- Wind model: velocity-relative linear drag
- Wind setting:
  - enable_wind: true
  - wind_model: drag
  - wind_velocity_x: 0.5
  - wind_velocity_y: 0.0
  - wind_velocity_z: 0.0
  - wind_drag_linear: 0.02
  - wind_drag_quad: 0.0
  - wind_max_force: 0.01
  - wind_apply_to: quadrotor

## Trial 2 Wind - First Run

- CSV: experiments/logs/autotrans_log_20260430_235540.csv
- Target: (-7.5, 1.5)
- Valid run: no
- valid_run_suggested: false
- has_nan_state: true
- first_nan_time: 11.349843
- final_row_has_nan: true
- max_swing_angle_deg: 117.386571
- max_uav_speed: 57.744483
- max_payload_speed: 224.971502
- final_uav_position: (-75.683978, 194.235662, 13.548875)
- final_payload_position: (-76.405263, 197.360814, 13.812819)
- mean_wind_force_norm: 0.010000
- max_wind_force_norm: 0.010000
- Interpretation: invalid run, likely collision/obstacle-triggered instability followed by NaN state.

## Trial 2 Wind - Second Run

- CSV: experiments/logs/autotrans_log_20260502_211227.csv
- Target: (-7.5, 1.5)
- Valid run: yes
- valid_run_suggested: true
- has_nan_state: false
- final_row_has_nan: false
- mean_swing_angle_deg: 1.113461
- max_swing_angle_deg: 20.953037
- p95_swing_angle_deg: 7.106357
- max_uav_speed: 2.527259
- max_payload_speed: 2.651338
- final_uav_position: (-7.432070, 1.615500, 1.524676)
- final_payload_position: (-7.432069, 1.615500, 0.856231)
- mean_wind_force_norm: 0.010000
- max_wind_force_norm: 0.010000
- Interpretation: valid repeat, final position is close to the target region.

## Trial 3 Wind

- CSV: experiments/logs/autotrans_log_20260502_211519.csv
- Target: (8.0, 1.5)
- Valid run: yes
- valid_run_suggested: true
- has_nan_state: false
- final_row_has_nan: false
- mean_swing_angle_deg: 1.325853
- max_swing_angle_deg: 18.321411
- p95_swing_angle_deg: 9.768105
- max_uav_speed: 2.502938
- max_payload_speed: 2.559216
- final_uav_position: (8.000000, 1.500000, 1.468415)
- final_payload_position: (8.000000, 1.500000, 0.799970)
- mean_wind_force_norm: 0.010000
- max_wind_force_norm: 0.010000
- Interpretation: valid run.

## Conclusion

The 0.01 N cap drag-wind setting is stable on Trial 1 and Trial 3, and it can succeed on Trial 2. However, Trial 2 produced one collision/NaN failure, so 0.01 N should be treated as a usable but not fully robust wind setting until more repeated trials are collected.

Recommended next step:
- Repeat Trial 2 at 0.01 N at least two more times.
- If both repeats are valid, keep 0.01 N as the current strong wind benchmark.
- If either repeat is invalid, use 0.0075 N or 0.005 N as the safer benchmark.
