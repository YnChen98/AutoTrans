# Stage 3 Fixed Scale 0.85 Strong Wind Trial Summary

## Basic Information

- Date: 2026-05-06
- Branch: high-level-command-adaptation
- Commit SHA: ff22643ba201042ed860c10113db2f2736e6d815
- Method: planner-side fixed speed/acceleration scaling
- speed_scale: 0.85
- acceleration_scale: 0.85
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
- mean_swing_angle_deg: 1.506468
- max_swing_angle_deg: 17.920952
- p95_swing_angle_deg: 10.794141
- max_uav_speed: 2.379647
- max_payload_speed: 2.488511
- uav_path_length: 18.099297
- payload_path_length: 20.357726
- final_uav_position: (0.000000, -1.200000, 1.468415)
- final_payload_position: (-0.000000, -1.200000, 0.799970)

## Trial 2

- Target: (-7.5, 1.5)
- Valid run: yes
- valid_run_suggested: true
- has_nan_state: false
- final_row_has_nan: false
- mean_swing_angle_deg: 0.389789
- max_swing_angle_deg: 13.200232
- p95_swing_angle_deg: 1.748844
- max_uav_speed: 2.507191
- max_payload_speed: 2.510607
- uav_path_length: 8.342412
- payload_path_length: 8.523151
- final_uav_position: (-7.500000, 1.500000, 1.468415)
- final_payload_position: (-7.500000, 1.500000, 0.799970)

## Trial 3

- Target: (8.0, 1.5)
- Valid run: yes
- valid_run_suggested: true
- has_nan_state: false
- final_row_has_nan: false
- mean_swing_angle_deg: 1.145759
- max_swing_angle_deg: 17.267788
- p95_swing_angle_deg: 8.695593
- max_uav_speed: 2.521214
- max_payload_speed: 2.660007
- uav_path_length: 24.483364
- payload_path_length: 25.198384
- final_uav_position: (8.000000, 1.500000, 1.468415)
- final_payload_position: (8.000001, 1.500000, 0.799970)

## Conclusion

Fixed planner-side scaling with speed_scale=0.85 and acceleration_scale=0.85 is stable under the strong drag-wind benchmark across Trial 1, Trial 2, and Trial 3.

Compared with original strong-wind runs, the result is mixed: Trial 2 and Trial 3 are reasonable, but Trial 1 does not show a consistent swing reduction. Therefore fixed 0.85 scaling should be treated as a fixed-scaling baseline, not the final proposed method.

Next step: implement runtime / heuristic risk-aware command adaptation using the same planner-side speed_scale and acceleration_scale interface.
