# Stage 2-B Drag Wind Benchmark Freeze Summary

## Basic Information

- Date: 2026-05-05
- Branch: wind-dynamics-experiment
- Commit SHA: 759a2d862742d42675ef3b5aae71259ddc8bfe73
- Wind model: velocity-relative linear drag
- Formal strong wind benchmark selected: 0.0075 N cap

## Frozen Wind Benchmark Levels

| Level | wind_velocity_x | wind_drag_linear | wind_max_force | Status | Notes |
|---|---:|---:|---:|---|---|
| weak | 0.5 | 0.004 | 0.002 | valid | stable on Trial 1 |
| moderate | 0.5 | 0.010 | 0.005 | mostly valid | one invalid run occurred, later repeats valid |
| strong stable | 0.5 | 0.015 | 0.0075 | valid | selected as formal strong benchmark |
| boundary | 0.5 | 0.020 | 0.010 | not frozen | repeated Trial 2 invalid runs occurred |

## 0.0075 N Trial 2 Repeat Result

- CSV: experiments/logs/autotrans_log_20260505_224953.csv
- Target: (-7.5, 1.5)
- Valid run: yes
- valid_run_suggested: true
- has_nan_state: false
- final_row_has_nan: false
- mean_swing_angle_deg: 0.541737
- max_swing_angle_deg: 12.544424
- p95_swing_angle_deg: 4.125954
- max_uav_speed: 2.509646
- max_payload_speed: 2.530020
- final_uav_position: (-7.500000, 1.500000, 1.468415)
- final_payload_position: (-7.500000, 1.500000, 0.799970)
- mean_wind_force_norm: 0.007500
- max_wind_force_norm: 0.007500

## 0.0075 N Trial 3 Repeat Result

- CSV: experiments/logs/autotrans_log_20260505_225236.csv
- Target: (8.0, 1.5)
- Valid run: yes
- valid_run_suggested: true
- has_nan_state: false
- final_row_has_nan: false
- mean_swing_angle_deg: 2.393279
- max_swing_angle_deg: 33.149323
- p95_swing_angle_deg: 12.950840
- max_uav_speed: 2.496692
- max_payload_speed: 2.780401
- final_uav_position: (8.000000, 1.500000, 1.468415)
- final_payload_position: (7.999999, 1.500000, 0.799970)
- mean_wind_force_norm: 0.007500
- max_wind_force_norm: 0.007500

## Decision

The 0.0075 N cap setting is selected as the current formal strong wind benchmark for Stage 2-B. It is valid on Trial 1, Trial 2, Trial 3, and additional Trial 2/Trial 3 repeats.

The 0.01 N cap setting should be treated as a boundary or stress-test setting, not as a stable benchmark, because Trial 2 produced repeated invalid runs with NaN states.

## Next Step

Freeze the Stage 2-B benchmark matrix and stop increasing wind magnitude for now. The next engineering task should be to make wind experiment configuration reproducible, preferably by adding a documented protocol or helper script rather than manually editing YAML each time.
