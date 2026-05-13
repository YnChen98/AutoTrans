# Stage 4-Q1 Formal Main-Run Audit Result

## Executive Summary

The Stage 4-Q1 formal main-run audit is complete for the 120 formal main
repeats from the Stage 4-J balanced strong-wind comparison.

`risk_adapter_v1` remains the aggregate-best method with `23/30` strict-valid
runs. `original` and `fixed_s085` are tied at `18/30`, and
`windlevel_s085` is `16/30`.

The audit table is now the canonical source for failure-mode-aware analysis of
the formal main repeats. The generated audit outputs are:

```text
experiments/results/stage4_main_run_audit/stage4_main_run_audit.csv
experiments/results/stage4_main_run_audit/stage4_main_run_audit_summary.md
```

These files are generated under `experiments/results/` and are not committed.

## Audit Scope

This audit includes only the paper-facing formal main repeats:

- trials: `trial4`, `trial5`, `trial6`
- methods: `original`, `fixed_s085`, `windlevel_s085`, `risk_adapter_v1`
- repeats: `repeat1` through `repeat10`

It excludes root-cause diagnostic smokes, Stage 4-N3 / Stage 4-N4 /
Stage 4-O3 diagnostic smokes, `risk_adapter_v0`, `resetcheck*`, `smoke*`, and
generated diagnostic files.

This is the paper-facing main-repeat audit. Diagnostic and exploratory runs
should not be mixed into this 120-row comparison.

## Strict-Valid Result

Paper-facing success uses strict-valid / `label_strict_invalid`, not raw
`valid_run_suggested` alone.

Aggregate strict-valid by method:

| method | strict_valid | total | strict_invalid | strict_valid_rate |
| --- | --- | --- | --- | --- |
| `original` | 18 | 30 | 12 | 0.600 |
| `fixed_s085` | 18 | 30 | 12 | 0.600 |
| `windlevel_s085` | 16 | 30 | 14 | 0.533 |
| `risk_adapter_v1` | 23 | 30 | 7 | 0.767 |

Strict-valid by method and trial:

| trial | method | strict_valid | total | strict_invalid | strict_valid_rate |
| --- | --- | --- | --- | --- | --- |
| `trial4` | `original` | 8 | 10 | 2 | 0.800 |
| `trial4` | `fixed_s085` | 9 | 10 | 1 | 0.900 |
| `trial4` | `windlevel_s085` | 4 | 10 | 6 | 0.400 |
| `trial4` | `risk_adapter_v1` | 7 | 10 | 3 | 0.700 |
| `trial5` | `original` | 7 | 10 | 3 | 0.700 |
| `trial5` | `fixed_s085` | 5 | 10 | 5 | 0.500 |
| `trial5` | `windlevel_s085` | 6 | 10 | 4 | 0.600 |
| `trial5` | `risk_adapter_v1` | 9 | 10 | 1 | 0.900 |
| `trial6` | `original` | 3 | 10 | 7 | 0.300 |
| `trial6` | `fixed_s085` | 4 | 10 | 6 | 0.400 |
| `trial6` | `windlevel_s085` | 6 | 10 | 4 | 0.600 |
| `trial6` | `risk_adapter_v1` | 7 | 10 | 3 | 0.700 |

## Diagnostic Label Summary

`failure_mode_guess` labels are run-level diagnostic labels from
`experiments/scripts/inspect_stage4_log_divergence.py`. They help explain
possible mechanisms and timing, but they do not replace strict-valid success
metrics.

| `failure_mode_guess` | count |
| --- | --- |
| `command_nan_before_state_divergence` | 1 |
| `command_saturation_before_nan` | 19 |
| `command_saturation_without_divergence` | 67 |
| `no_divergence_detected` | 4 |
| `reference_jump_before_command_nan` | 1 |
| `state_divergence_before_command_nan` | 14 |
| `strict_safety_no_nan` | 5 |
| `swing_warning_no_nan` | 4 |
| `target_error_only` | 5 |

`command_saturation_without_divergence` and `swing_warning_no_nan` are not
strict failures by themselves. They are diagnostic or warning labels and should
be interpreted together with strict-valid status and the run-level metrics.

## Earliest Failure Group Summary

`earliest_failure_group` is a coarse audit grouping for formal main-repeat
diagnostics:

| `earliest_failure_group` | count |
| --- | --- |
| `command_control_upstream` | 20 |
| `planner_reference_upstream` | 1 |
| `state_task_upstream` | 24 |
| `valid_or_warning` | 75 |

Group meanings:

- `command_control_upstream`: command saturation or command NaN related
  upstream signal.
- `planner_reference_upstream`: reference jump or path-planner related
  upstream signal.
- `state_task_upstream`: state divergence, strict safety, or target-error
  related signal.
- `valid_or_warning`: strict-valid or warning-only runs.

These groups are audit summaries, not definitive causal proof.

## Manual Annotation Summary

Manual annotations are currently incomplete. No formal main repeat currently
has a matched manual annotation.

| manual annotation metric | count |
| --- | --- |
| `rows_with_any_annotation` | 0 |
| `manual_collision_observed_true` | 0 |
| `manual_path_infeasible_true` | 0 |
| `manual_obstacle_stop_observed_true` | 0 |
| `manual_teleport_after_collision_true` | 0 |
| `path_through_obstacle_observed_true` | 0 |
| `path_feasibility_unknown_true` | 0 |
| `annotation_confidence_blank` | 120 |

The known manual path/collision annotation belongs to Stage 4-N4 `smoke3`,
which is excluded from this formal audit. Empty manual annotation fields should
not be interpreted as evidence of collision-free or path-feasible execution.

## Research Decision

Use this audit table before adding new baselines. It is the current
failure-mode-aware reference for the formal Stage 4-J main repeats.

The next experimental step should be a static-scale frontier, not more
`risk_adapter_v1` tuning. Do not tune `risk_adapter_v2` before fixed-scale and
simple heuristic baselines are stronger.

## What Not To Claim

- Do not claim statistical significance.
- Do not claim a safety guarantee.
- Do not claim all NaN/divergence failures are command-adaptation failures.
- Do not treat manual annotations as complete.
- Do not treat diagnostic labels as replacements for strict-valid metrics.
