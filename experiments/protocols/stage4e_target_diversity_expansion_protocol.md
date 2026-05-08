# Stage 4-E Target Diversity Expansion Protocol

## Executive Summary

Stage 4-E expands the Stage 4 risk dataset from 45 rows to 90 rows by adding three new target points: Trial 4, Trial 5, and Trial 6.

The motivation is the weak leave-one-target-out generalization observed in Stage 4-D group-CV and feature-ablation results. LOO and leave-one-method-out checks are useful pipeline diagnostics, but the current model is not ready for risk-conditioned policy learning because held-out target performance is still weak.

Stage 4-E is a data-diversity expansion step, not an online policy-learning step. The result should be used to test whether target generalization improves after adding more target diversity.

## New Targets

| Trial | `target_x` | `target_y` | Role |
| --- | ---: | ---: | --- |
| Trial 4 | -3.5 | -1.2 | Additional left-side target with lower `y`. |
| Trial 5 | 3.5 | 0.8 | Additional right-side target with moderate `y`. |
| Trial 6 | 0.0 | 1.5 | Center `x` target with upper `y`. |

Use `--z 0.0` in `experiments/scripts/run_baseline_trial.sh` because `payload_planner_node` overrides the planner altitude internally from the launch/config parameters. This matches the existing RViz-style 2D Nav Goal behavior.

For target-error analysis and manifest metadata, keep:

- `target_z=1.468415`
- `payload_target_z=0.799970`
- `target_xy_tolerance=0.5`

## Feasibility Screening

Before large repeats, screen each new target once with:

- `original` AutoTrans
- strong wind
- target-error analyzer

Use the same target-error analyzer arguments listed below for Trial 4, Trial 5, and Trial 6.

If a target is consistently invalid because of an obvious map, reachability, or trajectory issue, replace that target before the full expansion. Do not spend 15 repeated runs on a target that is invalid for a deterministic geometry/configuration reason rather than stochastic risk under strong wind.

Screening rows should only be added to `experiments/protocols/stage4_risk_manifest.json` if they follow the final naming convention, use the final method configuration, and are intended to count as one of the five repeats. Otherwise keep them as scratch logs and do not commit generated outputs.

Interrupted scratch logs should not become training examples. If an interrupted run is kept in the manifest for traceability, set `exclude_from_training=true` and write a short `exclude_reason`; otherwise do not add it. The interrupted 4.7-second short log from Stage 4-E should remain outside the training dataset unless it is explicitly requested later.

## Full Expansion Matrix

For each of Trial 4, Trial 5, and Trial 6, run:

| Method | Repeats per trial | New rows per trial |
| --- | ---: | ---: |
| `original` | 5 | 5 |
| `fixed_s085` | 5 | 5 |
| `windlevel_s085` | 5 | 5 |

Totals:

- 3 new trials
- 3 methods per trial
- 5 repeats per method-target condition
- Total new rows: 45
- Dataset size after expansion: 90 rows

## Method Configurations

### original

- `enable_command_adaptation=false`
- `adaptation_mode=none`
- No command adapter.
- Expected command scale in manifest: `1.0`.

### fixed_s085

- `enable_command_adaptation=true`
- `adaptation_mode=fixed`
- `speed_scale=0.85`
- `acceleration_scale=0.85`
- No command adapter.
- Expected command scale in manifest: `0.85`.

### windlevel_s085

- `enable_command_adaptation=true`
- `adaptation_mode=topic`
- `require_adaptation_topic_ready=true`
- Run command adapter with `policy_mode=wind_level`.
- Expected scale under strong wind: `0.85`.
- Expected command scale in manifest: `0.85`.

## Wind Configuration

Stage 4-E uses strong wind only.

Before each Stage 4-E batch, set the simulator drag-wind config:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/set_drag_wind_config.py --level strong
```

Run `wind_signal_publisher` as the annotation/logging signal with `wind_force_x=0.0075` and `wind_max_force=0.0075`:

```bash
roslaunch autotrans_logger wind_signal_publisher.launch enable_wind:=true wind_mode:=constant wind_force_x:=0.0075 wind_max_force:=0.0075
```

After Stage 4-E wind runs, restore no wind:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/set_drag_wind_config.py --level none
```

## Trial Runner Targets

Use `--z 0.0` for the runner target because the planner overrides altitude internally.

Trial 4:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
bash experiments/scripts/run_baseline_trial.sh --name stage4_original_strong_trial4_repeat1 --x -3.5 --y -1.2 --z 0.0 --duration 75
```

Trial 5:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
bash experiments/scripts/run_baseline_trial.sh --name stage4_original_strong_trial5_repeat1 --x 3.5 --y 0.8 --z 0.0 --duration 75
```

Trial 6:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
bash experiments/scripts/run_baseline_trial.sh --name stage4_original_strong_trial6_repeat1 --x 0.0 --y 1.5 --z 0.0 --duration 75
```

Replace the `--name` method and repeat fields for `fixed_s085`, `windlevel_s085`, and repeats 1 through 5.

## Analyzer Commands

Use target-specific `analyze_log.py` commands after each run. Replace `<CSV_PATH>` with the actual CSV log path, usually under `experiments/logs/`.

Trial 4:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/autotrans_logger/scripts/analyze_log.py \
  --csv <CSV_PATH> \
  --target_x -3.5 \
  --target_y -1.2 \
  --target_z 1.468415 \
  --payload_target_z 0.799970 \
  --target_xy_tolerance 0.5
```

Trial 5:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/autotrans_logger/scripts/analyze_log.py \
  --csv <CSV_PATH> \
  --target_x 3.5 \
  --target_y 0.8 \
  --target_z 1.468415 \
  --payload_target_z 0.799970 \
  --target_xy_tolerance 0.5
```

Trial 6:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/autotrans_logger/scripts/analyze_log.py \
  --csv <CSV_PATH> \
  --target_x 0.0 \
  --target_y 1.5 \
  --target_z 1.468415 \
  --payload_target_z 0.799970 \
  --target_xy_tolerance 0.5
```

Interpret `valid_run_suggested` together with final target-error metrics and visual transport evidence. `valid_run_suggested` is not the only learning label: it can miss obstacle collisions or other observed transport failures when the log has no NaN and final target error is within tolerance.

For collision-observed runs, keep the run and set `manual_invalid=true` plus a concise `manual_invalid_reason` in `experiments/protocols/stage4_risk_manifest.json`. The dataset builder will preserve the legacy `label_invalid` value and set `label_strict_invalid=1` through the manual annotation. Record invalid runs explicitly; do not delete, hide, or replace them after the target passes feasibility screening.

## Naming Convention

Use:

```text
stage4_<method>_strong_trial<id>_repeat<k>
```

Examples:

- `stage4_original_strong_trial4_repeat1`
- `stage4_fixed_s085_strong_trial5_repeat3`
- `stage4_windlevel_s085_strong_trial6_repeat5`

Use the same naming pattern for trial runner names, manifest `run_id` values, result notes, and manual experiment logbook entries.

## Manifest Update Rule

After each completed batch, update:

```bash
experiments/protocols/stage4_risk_manifest.json
```

Each new manifest entry must include `csv_path` and metadata consistent with the existing manifest schema, including:

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
- optional `manual_invalid` and `manual_invalid_reason` for observed transport failures such as obstacle collision
- optional `exclude_from_training` and `exclude_reason` for interrupted or scratch logs that should not become training examples

The manifest is committed because it is the reproducibility index for generated logs. Generated dataset CSV files under `experiments/datasets/` are ignored and should not be committed.

## Safety Checklist

Before each batch:

- Kill fake odom publishers and manual `rostopic` publishers from earlier tests.
- Confirm `git status --short` has no XML/YAML temporary changes.
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
- Confirm there are no XML/YAML temporary changes.
- Record invalid runs explicitly instead of deleting or replacing them.
- Mark collision-observed runs with `manual_invalid=true`.
- Leave interrupted short logs out of the manifest, or mark them with `exclude_from_training=true` if explicit traceability is needed.

## Next Step After Expansion

After Stage 4-E reaches 90 manifest rows, rebuild the dataset:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/build_stage4_risk_dataset.py --manifest experiments/protocols/stage4_risk_manifest.json --output experiments/datasets/stage4_risk_dataset.csv --print-summary
```

For future risk prediction, prefer `label_strict_invalid` over the legacy `label_invalid` because it includes target, speed, swing, and manual collision annotations.

Use the dedicated Stage 4 sklearn environment for predictor runs:

```bash
source ~/venvs/autotrans-stage4/bin/activate
```

Rerun LOO:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/train_stage4_risk_predictor.py --dataset experiments/datasets/stage4_risk_dataset.csv --feature-set early --cv loo --print-summary
```

Rerun leave-one-target-out:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/train_stage4_risk_predictor.py --dataset experiments/datasets/stage4_risk_dataset.csv --feature-set early --cv leave-one-target-out --print-summary
```

Rerun leave-one-method-out:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/train_stage4_risk_predictor.py --dataset experiments/datasets/stage4_risk_dataset.csv --feature-set early --cv leave-one-method-out --print-summary
```

Rerun the combined ablation:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/train_stage4_risk_predictor.py --dataset experiments/datasets/stage4_risk_dataset.csv --feature-set early --cv leave-one-target-out --drop-command-scale-features --drop-method-features --print-summary
```

Compare whether leave-one-target-out improves after adding target diversity. Do not move to risk-conditioned policy learning until the expanded dataset shows more credible held-out target behavior.
