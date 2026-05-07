# Stage 4-C Risk Dataset Expansion Plan

## Executive Summary

Stage 4-C expands the Stage 4 risk dataset from the current 15 rows to at least 45 rows by adding strong-wind Trial 1 and Trial 3 repeats for the same three method groups already used in Trial 2.

The goal is to support early failure-risk prediction and later risk-conditioned command adaptation. The current 15-row dataset is useful for validating the pipeline, but it is too small for final learning claims, final model selection, or method superiority claims.

## Current Dataset

The current Stage 4-A dataset contains:

- Trial 2 only.
- Methods: `original`, `fixed_s085`, `windlevel_s085`.
- 5 repeats per method.
- Total rows: 15.
- Invalid count: 7.

These rows should be reused. Do not rerun Trial 2 unless a specific log is later found to be corrupted or mislabeled.

## Target Expansion

Add Trial 1 and Trial 3 for the same three methods while keeping Trial 2 in the manifest.

| Trial | Target `(x, y)` | Role |
| --- | --- | --- |
| Trial 1 | `(0.0, -1.2)` | Shorter target for additional non-Trial-2 coverage. |
| Trial 2 | `(-7.5, 1.5)` | Existing strong-wind stress target; reuse existing repeats. |
| Trial 3 | `(8.0, 1.5)` | Long target for additional non-Trial-2 coverage. |

Use `target_z=1.468415` and `payload_target_z=0.799970` for target-error analysis and manifest metadata unless a later protocol explicitly changes the planner target height.

## Method Groups

### A. original AutoTrans

- `enable_command_adaptation=false`
- `adaptation_mode=none`
- No command adapter.
- Expected command scale in manifest: `1.0`.

### B. fixed_s085

- `enable_command_adaptation=true`
- `adaptation_mode=fixed`
- `speed_scale=0.85`
- `acceleration_scale=0.85`
- No command adapter.
- Expected command scale in manifest: `0.85`.

### C. windlevel_s085

- `enable_command_adaptation=true`
- `adaptation_mode=topic`
- `require_adaptation_topic_ready=true`
- Run command adapter with `policy_mode=wind_level`.
- Strong scale: `0.85`.
- Expected command scale in manifest: `0.85`.

## Wind Setting

Stage 4-C uses strong wind only. Before each batch, set the simulator drag-wind config:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/set_drag_wind_config.py --level strong
```

Run `wind_signal_publisher` as an annotation/logging signal with:

- `wind_force_x=0.0075`
- `wind_max_force=0.0075`

Example annotation command:

```bash
roslaunch autotrans_logger wind_signal_publisher.launch enable_wind:=true wind_mode:=constant wind_force_x:=0.0075 wind_max_force:=0.0075
```

After wind runs, restore no wind:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/set_drag_wind_config.py --level none
```

## Repeats

Use 5 repeats per method-target condition.

Existing Trial 2 repeats should be reused:

- `original` Trial 2: 5 existing repeats.
- `fixed_s085` Trial 2: 5 existing repeats.
- `windlevel_s085` Trial 2: 5 existing repeats.

New runs needed:

- Trial 1 `original` x 5.
- Trial 1 `fixed_s085` x 5.
- Trial 1 `windlevel_s085` x 5.
- Trial 3 `original` x 5.
- Trial 3 `fixed_s085` x 5.
- Trial 3 `windlevel_s085` x 5.

This adds 30 new rows. Together with the existing 15 Trial 2 rows, the expanded dataset should contain at least 45 rows.

## Analyzer Commands

Use target-specific `analyze_log.py` commands after each run. Replace `<CSV_PATH>` with the actual log path, usually under `experiments/logs/`.

Trial 1:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/autotrans_logger/scripts/analyze_log.py \
  --csv <CSV_PATH> \
  --target_x 0.0 \
  --target_y -1.2 \
  --target_z 1.468415 \
  --payload_target_z 0.799970 \
  --target_xy_tolerance 0.5
```

Trial 2:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/autotrans_logger/scripts/analyze_log.py \
  --csv <CSV_PATH> \
  --target_x -7.5 \
  --target_y 1.5 \
  --target_z 1.468415 \
  --payload_target_z 0.799970 \
  --target_xy_tolerance 0.5
```

Trial 3:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/autotrans_logger/scripts/analyze_log.py \
  --csv <CSV_PATH> \
  --target_x 8.0 \
  --target_y 1.5 \
  --target_z 1.468415 \
  --payload_target_z 0.799970 \
  --target_xy_tolerance 0.5
```

Interpret `valid_run_suggested` together with final target-error metrics. Invalid runs must be recorded, not filtered out.

## Naming Convention

Use:

```text
stage4_<method>_strong_trial<id>_repeat<k>
```

Examples:

- `stage4_original_strong_trial1_repeat1`
- `stage4_fixed_s085_strong_trial3_repeat4`
- `stage4_windlevel_s085_strong_trial1_repeat5`

Use the same naming pattern for trial runner names, manifest `run_id` values, result notes, and any manual experiment logbook entries.

## Manifest Update Rule

After each completed batch, update:

```bash
experiments/protocols/stage4_risk_manifest.json
```

Each new manifest entry must include:

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
- optional `notes`

The manifest should be committed because it is the reproducibility index for generated logs. Generated dataset CSV files should not be committed.

## Generated Files Rule

Do not commit generated experiment outputs:

- `experiments/logs/*.csv`
- `experiments/figures/*.png`
- `experiments/figures/*.txt`
- `experiments/datasets/*.csv`
- `experiments/results/`

Before committing the manifest or protocol updates, check `git status --short` and stage only allowed source/protocol files.

## Safety Checklist

Before each batch:

- Kill fake odom publishers and manual `rostopic` publishers from earlier tests.
- Confirm `git status --short` has no temporary XML/YAML changes.
- Set the correct wind config with `python3 experiments/scripts/set_drag_wind_config.py --level strong`.
- Set the correct planner adaptation mode for the selected method group.
- Confirm `wind_signal_publisher` uses `wind_force_x=0.0075` and `wind_max_force=0.0075`.

After each batch:

- Restore wind level with `python3 experiments/scripts/set_drag_wind_config.py --level none`.
- Restore planner no-op params:
  - `enable_command_adaptation=false`
  - `adaptation_mode=none`
  - `speed_scale=1.0`
  - `acceleration_scale=1.0`
  - `require_adaptation_topic_ready=false`
- Run `git status --short`.
- Record invalid runs explicitly instead of deleting or replacing them.

## Next Step After Expansion

After the manifest reaches at least 45 rows:

1. Regenerate `experiments/datasets/stage4_risk_dataset.csv`.
2. Rerun `experiments/scripts/train_stage4_risk_predictor.py`.
3. Compare `basic` vs `early` feature sets.
4. Report AUROC, AUPRC, Brier score, and F1.
5. Do not claim final model performance until the dataset grows beyond 45 rows and has enough diversity for more stable validation.
