# Stage 4-Q1 Main Run Audit Protocol

## Purpose

Stage 4-Q1 builds one formal run-level audit table for the completed Stage 4-J
balanced strong-wind Trial 4/5/6 comparison.

The audit consolidates strict-valid metrics, raw analyzer validity,
divergence-inspector labels, command diagnostics, reference diagnostics,
trajectory-update diagnostics, and manual path/collision annotations when they
are available.

The builder is offline only. It does not run ROS, simulation, RViz, or
`catkin_make`.

## Formal Main-Repeat Filter

Only formal main repeats are included:

- methods: `original`, `fixed_s085`, `windlevel_s085`, `risk_adapter_v1`
- trials: `trial4`, `trial5`, `trial6`
- repeats: `repeat1` through `repeat10`

The accepted metrics summary filename is exact:

```text
stage4_<method>_strong_<trial>_repeat<repeat>_metrics_summary.txt
```

Diagnostic and exploratory files are excluded by construction, including:

- `stage4n3_*`
- `stage4n4_*`
- `stage4o3_*`
- `stage4_rootcause_*`
- `stage4_risk_adapter_v0_*`
- `resetcheck*`
- `smoke*`
- files that do not match the formal main-repeat pattern

## Strict-Valid Metric

Paper-facing success uses strict-valid / `label_strict_invalid`, not raw
`valid_run_suggested` alone.

For each run, strict-valid is computed from the metrics summary as:

- `valid_run_suggested=true`
- `has_nan_state=false`
- `max_swing_angle_deg < 60`
- `max_uav_speed < 4`
- `max_payload_speed < 4`
- `final_uav_xy_error <= target_xy_tolerance`

If `target_xy_tolerance` is missing, the default tolerance is `0.5`.

## Divergence Labels

The audit calls `experiments/scripts/inspect_stage4_log_divergence.py` on the
CSV log referenced by each metrics summary. The joined inspector fields are:

- `failure_mode_guess`
- `first_command_nan_time`
- `first_state_divergence_time`
- `first_reference_jump_time`
- `reference_jump_after_divergence`

These are heuristic run-level diagnostic labels. They help organize evidence
around timing, but they do not prove a final physical root cause by themselves.

## Manual Annotation Join

Manual annotations are loaded from:

```bash
experiments/protocols/stage4o_manual_failure_annotations.json
```

Rows are matched by `run_name` or normalized `csv_path`. When present, the
audit includes:

- `manual_collision_observed`
- `manual_path_infeasible`
- `manual_obstacle_stop_observed`
- `manual_teleport_after_collision`
- `path_through_obstacle_observed`
- `path_feasibility_unknown`
- `annotation_confidence`
- `manual_failure_note`

Manual annotations are incomplete and are used only when visual evidence
exists. Missing manual fields do not prove that a path was feasible or
collision-free.

## `earliest_failure_group`

`earliest_failure_group` is a coarse audit grouping for paper diagnostics:

- `valid_or_warning` if `strict_valid=true`
- `planner_reference_upstream` if `failure_mode_guess` includes
  `reference_jump_before_command_nan`, or if
  `manual_path_infeasible=true` / `manual_collision_observed=true`
- `command_control_upstream` if `failure_mode_guess` is
  `command_saturation_before_nan` or `command_nan_before_state_divergence`
- `state_task_upstream` if `failure_mode_guess` is
  `state_divergence_before_command_nan`, `strict_safety_no_nan`, or
  `target_error_only`
- `unknown` otherwise

This grouping is intentionally conservative. It should be used as an audit
summary, not as definitive causal attribution.

## Outputs

Default generated outputs are under ignored `experiments/results/` and should
not be committed:

```bash
experiments/results/stage4_main_run_audit/stage4_main_run_audit.csv
experiments/results/stage4_main_run_audit/stage4_main_run_audit_summary.md
```

The Markdown summary reports:

- total rows
- strict-valid table by method/trial
- aggregate strict-valid by method
- `failure_mode_guess` counts
- `earliest_failure_group` counts
- manual annotation counts
- caveat on incomplete manual annotations

## How To Run

From the repository root:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/build_stage4_main_run_audit.py \
  --metrics-dir experiments/figures \
  --manual-annotations experiments/protocols/stage4o_manual_failure_annotations.json \
  --output-csv experiments/results/stage4_main_run_audit/stage4_main_run_audit.csv \
  --output-md experiments/results/stage4_main_run_audit/stage4_main_run_audit_summary.md \
  --print-summary
```

Generated outputs under `experiments/results/` should not be committed.
