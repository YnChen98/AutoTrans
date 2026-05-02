# Stage 2-B Drag Wind 0.0075 N Target Trial Summary

## Basic Information

- Date: 2026-05-02
- Branch: wind-dynamics-experiment
- Commit SHA: 0253cfe45a1099cefadde011e25edc08ec162e12
- Wind model: velocity-relative linear drag
- Wind setting: wind_velocity_x=0.5, wind_drag_linear=0.015, wind_max_force=0.0075, apply_to=quadrotor

## Trial 2 Wind

- CSV: experiments/logs/autotrans_log_20260502_213933.csv
- Target: (-7.5, 1.5)
- Valid run: yes
- valid_run_suggested: true
- has_nan_state: false
- final_row_has_nan: false
- mean_swing_angle_deg: 1.298061
- max_swing_angle_deg: 13.083459
- p95_swing_angle_deg: 5.665885
- max_uav_speed: 2.350236
- max_payload_speed: 2.499938
- final_uav_position: (-7.555464, 1.429504, 1.468240)
- final_payload_position: (-7.551094, 1.438933, 0.799876)
- mean_wind_force_norm: 0.007500
- max_wind_force_norm: 0.007500

## Trial 3 Wind

- CSV: experiments/logs/autotrans_log_20260502_214147.csv
- Target: (8.0, 1.5)
- Valid run: yes
- valid_run_suggested: true
- has_nan_state: false
- final_row_has_nan: false
- mean_swing_angle_deg: 1.535995
- max_swing_angle_deg: 19.580464
- p95_swing_angle_deg: 10.634558
- max_uav_speed: 2.517506
- max_payload_speed: 2.829189
- final_uav_position: (8.000000, 1.500000, 1.468415)
- final_payload_position: (8.000000, 1.500000, 0.799970)
- mean_wind_force_norm: 0.007500
- max_wind_force_norm: 0.007500

## Conclusion

The 0.0075 N cap drag-wind setting is valid on Trial 1, Trial 2, and Trial 3. Since 0.01 N produced repeated invalid runs on Trial 2, 0.0075 N is the current best candidate for the formal strong wind benchmark. Repeat Trial 2 and Trial 3 once more before freezing it.
