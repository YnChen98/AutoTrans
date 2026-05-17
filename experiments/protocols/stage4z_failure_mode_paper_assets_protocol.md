# Stage 4-Z Failure-Mode Paper Assets Protocol

## Purpose

Stage 4-Z generates paper-ready failure-mode tables and stacked-bar figures
for the completed protocol-split Stage 4 results.

The goal is to support the Stage 4-Y Results narrative with diagnostic
failure-group evidence before any new `risk_adapter_v22` tuning is considered.

The generator is offline only. It does not run ROS, simulation, RViz, or
`catkin_make`.

## Protocols And Methods

Single-goal mission protocol:

- `goal_repeat=1`
- wind: `strong`
- trials: Trial 4, Trial 5, Trial 6
- repeats: repeat1 through repeat10
- methods: `original`, `fixed_s085`, `windlevel_s085`, `fixed_s080`,
  `risk_adapter_v1`, `risk_adapter_v2`, `risk_adapter_v21`

Goal-reissue stress protocol:

- `goal_repeat=10`
- wind: `strong`
- trials: Trial 4, Trial 5, Trial 6
- repeats: repeat1 through repeat10
- methods: `original`, `fixed_s085`, `windlevel_s085`, `risk_adapter_v1`,
  `fixed_s080`, `risk_adapter_v21`

## Input Metrics

Default metrics directory:

```bash
experiments/figures
```

The generator reads `*_metrics_summary.txt` files and their linked CSV logs.
It uses the same protocol/method file patterns as Stage 4-W3 and calls
`experiments/scripts/inspect_stage4_log_divergence.py` for diagnostic timing
and `failure_mode_guess` fields.

Generated outputs go under:

```bash
experiments/results/stage4_failure_mode_paper_assets
```

Generated CSV, Markdown, and PNG outputs under `experiments/results/` are
ignored and should not be committed.

## Strict-Valid Vs Diagnostic Labels

Strict-valid remains the paper-facing success metric. A run is strict-valid
only when:

- `valid_run_suggested=true`
- `has_nan_state=false`
- `max_swing_angle_deg < 60`
- `max_uav_speed < 4`
- `max_payload_speed < 4`
- `final_uav_xy_error <= 0.5`

Diagnostic labels and `failure_group` values are not perfect root-cause proof.
They are used to organize failure evidence and guide follow-up analysis.

Important interpretation rules:

- `command_saturation_without_divergence` is not a failure by itself.
- `no_divergence_detected` can still coincide with target/no-arrival
  strict-invalid runs.
- Strict-valid overrides label interpretation for paper-facing success.

## Failure-Group Mapping

The generator maps `failure_mode_guess` plus run-level metrics into:

| failure_group | Mapping logic |
| --- | --- |
| `valid_or_warning` | Any strict-valid run, including runs with warning-style diagnostic labels such as `command_saturation_without_divergence`, `no_divergence_detected`, `swing_warning_no_nan`, or `position_or_reference_jump_warning_no_nan`. |
| `command_control_upstream` | `command_saturation_before_nan`, `command_nan_before_state_divergence`, or `command_nan_coincident_with_state_divergence`. |
| `planner_reference_upstream` | `reference_jump_before_command_nan`, or goal-reissue stress failure after arrival with `first_failure_after_arrival_flag=true`. |
| `state_task_upstream` | `state_divergence_before_command_nan`, `strict_safety_no_nan`, `target_error_only`, target/no-arrival failure, or strict-invalid no-NaN final XY error above `0.5`. |
| `unknown` | Anything not mapped above. |

Stage 4-Z2 replaces the earlier `warning_only` group with
`valid_or_warning` because strict-valid runs should not be presented as
failures in paper-facing figures. Warning-style labels can still be reviewed in
the run table and failure-mode count table, but strict-valid remains the
paper-facing success metric.

The invalid-only view excludes strict-valid runs and is the recommended view
for paper failure analysis. It prevents successful runs with warning-style
diagnostics from visually dominating or confusing the failure distribution.

The grouping is deliberately conservative. It should support paper discussion
and ablation planning, not replace manual failure analysis.

## Outputs

The generator writes:

- `stage4_failure_mode_run_table.csv`
- `stage4_failure_mode_run_table.md`
- `stage4_failure_mode_count_table.csv`
- `stage4_failure_mode_count_table.md`
- `stage4_failure_group_table.csv`
- `stage4_failure_group_table.md`
- `stage4_failure_group_invalid_only_table.csv`
- `stage4_failure_group_invalid_only_table.md`
- `stage4_failure_mode_summary.md`
- `stage4_failure_group_stacked_bar.png`
- `stage4_failure_group_invalid_only_stacked_bar.png`

If `matplotlib` is unavailable, the script skips only
`stage4_failure_group_stacked_bar.png` and
`stage4_failure_group_invalid_only_stacked_bar.png`; it still writes the tables
and summary.

## How To Run

From the repository root:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/generate_stage4_failure_mode_paper_assets.py \
  --metrics-dir experiments/figures \
  --output-dir experiments/results/stage4_failure_mode_paper_assets \
  --print-summary
```

## How To Use In The Paper

Use the generated invalid-only failure-group table and invalid-only stacked-bar
figure to support the Stage 4-Y Results narrative:

- single-goal: `windlevel_s085` is strongest overall, while
  `risk_adapter_v1` and `risk_adapter_v21` remain competitive learned /
  risk-conditioned variants.
- goal-reissue stress: `fixed_s080` remains strongest, `risk_adapter_v1` is
  second, and `risk_adapter_v21` underperforms both.
- `risk_adapter_v21` Trial 4 stress weakness and Trial 6 bottleneck require
  diagnosis before any new variant.

The all-run failure-group table remains useful for accounting because it shows
where strict-valid runs are grouped as `valid_or_warning`, but it should not be
the primary paper failure-analysis figure.

Do not claim:

- statistical significance
- a safety guarantee
- mixed-protocol aggregate superiority
- `risk_adapter_v21` as a cross-protocol winner
- diagnostic labels as exact root-cause proof
