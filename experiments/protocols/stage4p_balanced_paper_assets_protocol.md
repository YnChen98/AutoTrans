# Stage 4-P Balanced Paper Assets Protocol

## Purpose

Stage 4-P generates paper-ready tables and one aggregate success-rate figure
for the balanced Stage 4-J strong-wind Trial 4/5/6 comparison.

The generator is offline only. It does not run ROS, simulation, RViz, or
`catkin_make`.

## Inputs

Primary manifest:

```bash
experiments/protocols/stage4h_adapter_limited_eval_manifest.json
```

Metrics summaries:

```bash
experiments/figures/*_metrics_summary.txt
```

Only formal balanced main repeats are used:

- methods: `original`, `fixed_s085`, `windlevel_s085`, `risk_adapter_v1`
- trials: `trial4`, `trial5`, `trial6`
- repeats: `repeat1` through `repeat10`

The script looks for exact filenames of the form:

```text
stage4_<method>_strong_<trial>_repeat<repeat>_metrics_summary.txt
```

## Outputs

The default output directory is ignored and should not be committed:

```bash
experiments/results/stage4_balanced_paper_assets
```

Generated files:

- `stage4_balanced_success_table.csv`
- `stage4_balanced_success_table.md`
- `stage4_balanced_aggregate_table.csv`
- `stage4_balanced_aggregate_table.md`
- `stage4_balanced_failure_mode_table.csv`
- `stage4_balanced_failure_mode_table.md`
- `stage4_balanced_paper_summary.md`
- `stage4_balanced_success_rates.png`

If `matplotlib` is unavailable, the script prints a warning and skips only the
PNG figure. CSV and Markdown outputs are still generated.

## Metric Convention

Paper-facing success uses strict-valid / `label_strict_invalid`, not raw
`valid_run_suggested` alone.

For repeat-level failure-mode rows, strict-valid is computed from metrics as:

- `valid_run_suggested=true`
- `has_nan_state=false`
- `max_swing_angle_deg < 60`
- `max_uav_speed < 4`
- `max_payload_speed < 4`
- `final_uav_xy_error <= target_xy_tolerance`

The script verifies that repeat-level strict-valid counts match the committed
manifest counts before writing final outputs.

## Diagnostic Smoke Exclusion

Diagnostic smoke and root-cause files are not part of the paper-facing
balanced comparison. The generator uses exact formal repeat filenames and does
not scan broad globs for result rows.

Excluded diagnostic families include:

- `stage4n3_*`
- `stage4n4_*`
- `stage4o3_*`
- `stage4_rootcause_*`
- `stage4_risk_adapter_v0_*`
- `resetcheck*`
- `smoke*`

## Run-Level Diagnostic Label Caveat

The failure-mode table is better interpreted as a run-level diagnostic-label
table. It uses
`experiments/scripts/inspect_stage4_log_divergence.py` to classify timing
evidence from the CSV referenced by each metrics summary.

Some labels correspond to valid or warning-only runs rather than failures.
`command_saturation_without_divergence` is not a failure by itself,
`no_divergence_detected` is not a failure, and `swing_warning_no_nan` is
warning-only.

Diagnostic labels explain mechanisms; they do not replace strict-valid /
`label_strict_invalid` success accounting. NaN/divergence failures should be
counted as invalid, but they should not automatically be attributed to command
adaptation or to any single method.

Manual path/collision annotations should be joined later when visual evidence
exists.

## How To Run

From the repository root:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/generate_stage4_balanced_paper_assets.py \
  --manifest experiments/protocols/stage4h_adapter_limited_eval_manifest.json \
  --metrics-dir experiments/figures \
  --output-dir experiments/results/stage4_balanced_paper_assets \
  --print-summary
```

Generated outputs under `experiments/results/` should not be committed.
