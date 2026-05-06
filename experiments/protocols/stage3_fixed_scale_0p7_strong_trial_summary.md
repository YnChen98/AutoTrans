# Stage 3 Fixed Scale 0.7 Strong Wind Trial Summary

## Basic Information

- Date: 2026-05-06
- Branch: high-level-command-adaptation
- Commit SHA: cd3b09e3ed967ec5ace24c42552099d695f5068b
- Method: planner-side fixed speed/acceleration scaling
- speed_scale: 0.7
- acceleration_scale: 0.7
- Wind level: strong
- wind_velocity_x: 0.5
- wind_drag_linear: 0.015
- wind_max_force: 0.0075

## Trial 1

- Target: (0.0, -1.2)
- Valid run: yes
- valid_run_suggested: true
- has_nan_state: false
- final_row_has_nan: false
- mean_swing_angle_deg: 1.020966
- max_swing_angle_deg: 15.696825
- p95_swing_angle_deg: 8.379088
- max_uav_speed: 2.430344
- max_payload_speed: 2.473289
- final_uav_position: (-0.000000, -1.200000, 1.468415)
- final_payload_position: (-0.000000, -1.200000, 0.799970)

## Trial 2

- Target: (-7.5, 1.5)
- Valid run: no
- valid_run_suggested: false
- has_nan_state: true
- first_nan_time: 9.949974
- final_row_has_nan: true
- mean_swing_angle_deg: 2.881653
- max_swing_angle_deg: 130.906648
- p95_swing_angle_deg: 23.342916
- max_uav_speed: 2442.709717
- max_payload_speed: 2442.709717
- final_uav_position: (77.512641, -47.595075, 117.629015)
- final_payload_position: (78.016485, -47.558133, 118.066732)
- last_row_uav_position: (nan, nan, nan)
- last_row_payload_position: (nan, nan, nan)

## Trial 3

- Target: (8.0, 1.5)
- Valid run: yes
- valid_run_suggested: true
- has_nan_state: false
- final_row_has_nan: false
- mean_swing_angle_deg: 1.440977
- max_swing_angle_deg: 29.200390
- p95_swing_angle_deg: 10.409209
- max_uav_speed: 2.507144
- max_payload_speed: 3.495131
- final_uav_position: (8.000000, 1.500000, 1.468415)
- final_payload_position: (7.999999, 1.500000, 0.799970)

## Conclusion

Fixed planner-side scaling with speed_scale=0.7 and acceleration_scale=0.7 is not reliable enough to be used as the proposed method. Trial 2 produced NaN divergence under the strong wind benchmark. This result should be treated as a fixed-scaling baseline failure and motivates risk-aware or state-dependent command adaptation instead of constant scaling.
