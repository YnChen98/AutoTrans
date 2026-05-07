# Stage 4-A Risk Dataset Protocol

## Purpose

Stage 4-A turns repeated AutoTrans stress-case logs into a compact supervised dataset for early failure-risk prediction. The immediate target is Stage 3-C strong Trial 2, where repeated runs showed stochastic validity and simple fixed or wind-level command scaling was not clearly better than original AutoTrans.

This dataset is the first step toward calibrated early failure-risk prediction and later risk-conditioned command adaptation. It is not yet a learned controller or a final policy.

## Manifest Format

The manifest is a JSON object with a `runs` list. Each run describes one log file and its experiment metadata:

- `run_id`
- `csv_path`
- `method`
- `policy_mode`
- `adaptation_mode`
- `command_scale_expected`
- `wind_level`
- `wind_force_norm`
- `target_x`
- `target_y`
- `target_z`
- `payload_target_z`
- `trial_name`
- `repeat_id`
- `notes` optional

The initial manifest is:

```bash
experiments/protocols/stage4_risk_manifest.json
```

It includes the known Stage 3-C strong Trial 2 repeats for original AutoTrans, fixed XML scale `0.85`, and `policy_mode=wind_level` scale `0.85`.

## Dataset Schema

The builder writes one CSV row per manifest run. Each row preserves the manifest metadata, then adds run-level features:

- `sample_count`
- `duration_sec`
- `effective_log_rate_hz`
- `has_nan_state`
- `first_nan_time`
- `final_row_has_nan`
- `valid_run_suggested`
- `nan_count_total`
- `final_uav_xy_error`
- `final_payload_xy_error`
- `final_uav_position_error_3d`
- `final_payload_position_error_3d`
- `mean_swing_angle_deg`
- `max_swing_angle_deg`
- `p95_swing_angle_deg`
- `max_uav_speed`
- `max_payload_speed`
- `mean_uav_speed`
- `mean_payload_speed`
- `uav_path_length`
- `payload_path_length`
- `mean_wind_force_norm`
- `max_wind_force_norm`
- `mean_command_speed_scale`
- `min_command_speed_scale`
- `max_command_speed_scale`
- `final_command_speed_scale`

Missing numeric inputs are written as `nan`. Older CSV logs without `wind_force_norm` or `command_speed_scale` columns are handled without crashing.

## Labels

The builder creates binary labels:

- `label_invalid`: `1` when `valid_run_suggested` is false.
- `label_nan`: `1` when any key state field becomes `nan` or `inf` after finite data has appeared.
- `label_target_fail`: `1` when `final_uav_xy_error > target_xy_tolerance`.
- `label_speed_fail`: `1` when `max_uav_speed > 4.0` or `max_payload_speed > 4.0`.
- `label_swing_fail`: `1` when `max_swing_angle_deg > 60.0`.

The default `target_xy_tolerance` is `0.5`.

## Early-Window Features

Early windows are measured from the first `has_trajectory` row when available. If that is unavailable, the builder falls back to the first finite state row.

For each requested window `w`, the builder adds:

- `early_{w}s_max_uav_speed`
- `early_{w}s_max_payload_speed`
- `early_{w}s_mean_uav_speed`
- `early_{w}s_mean_payload_speed`
- `early_{w}s_max_swing_angle_deg`
- `early_{w}s_p95_swing_angle_deg`
- `early_{w}s_mean_swing_angle_deg`
- `early_{w}s_max_wind_force_norm`
- `early_{w}s_mean_wind_force_norm`
- `early_{w}s_min_command_speed_scale`
- `early_{w}s_mean_command_speed_scale`
- `early_{w}s_target_distance_end`
- `early_{w}s_target_progress`

`early_{w}s_target_distance_end` is the UAV distance to `(target_x, target_y, target_z)` at the end of the window. `early_{w}s_target_progress` is start distance minus end distance, so positive values mean the UAV moved closer to the target.

## Dry Run

Use dry-run before generating a dataset:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/build_stage4_risk_dataset.py --manifest experiments/protocols/stage4_risk_manifest.json --output experiments/datasets/stage4_risk_dataset.csv --dry-run --print-summary
```

This reads the manifest and CSV logs, prints planned rows and aggregate counts, and does not write `experiments/datasets/stage4_risk_dataset.csv`.

## Generate Dataset Locally

Generate the dataset only after checking the dry-run summary:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/build_stage4_risk_dataset.py --manifest experiments/protocols/stage4_risk_manifest.json --output experiments/datasets/stage4_risk_dataset.csv --print-summary
```

Generated dataset outputs under `experiments/datasets/` should not be committed. The committed artifact is the manifest and protocol, not the generated CSV dataset.
