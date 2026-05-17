# Stage 4-Z2 Failure-Mode Paper Asset Result

## Executive Summary

Stage 4-Z2 failure-mode paper assets are complete for the completed
protocol-split Stage 4 results.

The paper-facing failure-analysis view should use the invalid-only failure
groups, especially `stage4_failure_group_invalid_only_stacked_bar.png`. The
all-run table is retained for accounting, but it includes `valid_or_warning`
rows for strict-valid runs and should not be used as the primary
failure-analysis figure.

These results support a failure-mode-aware evaluation contribution alongside
the protocol-split success-rate tables. The `failure_group` labels are
diagnostic labels only; they are not proof of exact physical root cause.

## Protocol Scope

- single-goal mission protocol: `goal_repeat=1`
- goal-reissue stress protocol: `goal_repeat=10`
- total run rows: `390`
- strict-invalid runs: `110`
- paper-facing success metric: strict-valid
- diagnostic grouping: invalid-only `failure_group`

Generated assets under ignored
`experiments/results/stage4_failure_mode_paper_assets/` include:

- `stage4_failure_mode_run_table.csv`
- `stage4_failure_mode_count_table.csv`
- `stage4_failure_mode_count_table.md`
- `stage4_failure_group_table.csv`
- `stage4_failure_group_table.md`
- `stage4_failure_group_invalid_only_table.csv`
- `stage4_failure_group_invalid_only_table.md`
- `stage4_failure_mode_summary.md`
- `stage4_failure_group_stacked_bar.png`
- `stage4_failure_group_invalid_only_stacked_bar.png`

## Invalid-Only Failure Groups

Single-goal mission protocol:

| method | command_control_upstream | planner_reference_upstream | state_task_upstream | total strict-invalid |
| --- | ---: | ---: | ---: | ---: |
| `original` | 3 | 0 | 6 | 9 |
| `fixed_s085` | 4 | 1 | 3 | 8 |
| `windlevel_s085` | 0 | 0 | 4 | 4 |
| `risk_adapter_v1` | 2 | 0 | 3 | 5 |
| `fixed_s080` | 3 | 1 | 5 | 9 |
| `risk_adapter_v2` | 3 | 2 | 4 | 9 |
| `risk_adapter_v21` | 1 | 0 | 4 | 5 |

Goal-reissue stress protocol:

| method | command_control_upstream | planner_reference_upstream | state_task_upstream | total strict-invalid |
| --- | ---: | ---: | ---: | ---: |
| `original` | 3 | 0 | 9 | 12 |
| `fixed_s085` | 8 | 0 | 4 | 12 |
| `windlevel_s085` | 6 | 0 | 8 | 14 |
| `risk_adapter_v1` | 3 | 1 | 3 | 7 |
| `fixed_s080` | 4 | 0 | 2 | 6 |
| `risk_adapter_v21` | 5 | 3 | 2 | 10 |

## Main Observations

Single-goal mission:

- `windlevel_s085` is the strongest aggregate method and has only
  `state_task_upstream` invalids in the invalid-only grouping.
- `risk_adapter_v1` and `risk_adapter_v21` remain competitive learned /
  risk-conditioned variants.
- `risk_adapter_v21` reduces `command_control_upstream` invalids relative to
  `risk_adapter_v1`, but still has `state_task_upstream` failures.

Goal-reissue stress:

- `fixed_s080` remains strongest and has fewer invalid groups than the other
  stress methods in the completed comparison.
- `risk_adapter_v21` has more `command_control_upstream` and
  `planner_reference_upstream` invalids than `fixed_s080`.
- The `risk_adapter_v21` stress weakness is not purely post-arrival; it
  includes command/control and planner/reference diagnostic signals.

## Paper Usage

- Use the protocol-split success table as the main result table.
- Use `stage4_failure_group_invalid_only_stacked_bar.png` as the
  failure-analysis figure.
- Use the all-run failure-group table only for accounting.
- Keep strict-valid as the main paper-facing metric.

## Research Decision

Do not create `risk_adapter_v22` yet.

The next step should be targeted diagnosis:

- Trial 4 goal-reissue stress failures for `risk_adapter_v21`.
- Trial 6 bottleneck across single-goal and stress.

Decide whether a phase-aware or failure-aware ablation is justified only after
this diagnosis is stable.

## What Not To Claim

- Do not claim learned governors uniformly dominate heuristic/static
  baselines.
- Do not claim `risk_adapter_v21` is a cross-protocol winner.
- Do not claim statistical significance.
- Do not claim a safety guarantee.
- Do not claim diagnostic labels prove exact root cause.
