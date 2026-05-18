# Stage 4-AC Balanced Robustness Assets Protocol

## Purpose

Stage 4-AC generates paper assets for balanced robustness and protocol regret
after the completed protocol-split Stage 4 comparison and Stage 4-AA3
representative trace review.

The completed Stage 4-AC2 result is recorded in
`experiments/protocols/stage4ac_balanced_robustness_assets_result.md`.

This is an offline paper-support step. It does not run ROS, simulation, RViz,
or `catkin_make`.

## Input Counts

Single-goal mission protocol (`goal_repeat=1`):

| method | strict-valid |
| --- | ---: |
| `original` | `21/30` |
| `fixed_s085` | `22/30` |
| `windlevel_s085` | `26/30` |
| `fixed_s080` | `21/30` |
| `risk_adapter_v1` | `25/30` |
| `risk_adapter_v2` | `21/30` |
| `risk_adapter_v21` | `25/30` |

Goal-reissue stress protocol (`goal_repeat=10`):

| method | strict-valid |
| --- | ---: |
| `original` | `18/30` |
| `fixed_s085` | `18/30` |
| `windlevel_s085` | `16/30` |
| `risk_adapter_v1` | `23/30` |
| `fixed_s080` | `24/30` |
| `risk_adapter_v21` | `20/30` |

`risk_adapter_v2` has no completed goal-reissue stress cell in the current
protocol-split table. It is included only in the single-protocol-only table and
excluded from complete cross-protocol balanced ranking.

## Protocol Oracle Definition

The protocol oracle is the best observed method in each protocol:

- single-goal oracle: `windlevel_s085`, `26/30`
- goal-reissue stress oracle: `fixed_s080`, `24/30`

Protocol regret is measured relative to these protocol oracles.

## Balanced Metrics Definitions

For each method with complete results in both protocols:

- `single_goal_success_rate = single_goal_valid / 30`
- `stress_success_rate = stress_valid / 30`
- `mean_valid_count = (single_goal_valid + stress_valid) / 2`
- `mean_success_rate = (single_goal_success_rate + stress_success_rate) / 2`
- `worst_protocol_valid = min(single_goal_valid, stress_valid)`
- `worst_protocol_success_rate = min(single_goal_success_rate, stress_success_rate)`
- `protocol_gap_valid_count = abs(single_goal_valid - stress_valid)`
- `protocol_gap_rate = abs(single_goal_success_rate - stress_success_rate)`
- `single_goal_regret = 26 - single_goal_valid`
- `stress_regret = 24 - stress_valid`
- `total_regret = single_goal_regret + stress_regret`
- `normalized_total_regret = total_regret / (26 + 24)`

## Pareto Frontier Definition

Method A dominates Method B if A has at least as many single-goal strict-valid
runs and at least as many stress strict-valid runs, with at least one protocol
strictly better.

The expected Pareto frontier is:

- `windlevel_s085`
- `fixed_s080`
- `risk_adapter_v1`

`risk_adapter_v21` is not expected to be Pareto-frontier because
`risk_adapter_v1` has the same single-goal count (`25/30`) and higher stress
count (`23/30` versus `20/30`).

## Outputs

Generated outputs go under:

```bash
experiments/results/stage4_balanced_robustness_assets
```

The generator writes:

- `stage4_balanced_robustness_table.csv`
- `stage4_balanced_robustness_table.md`
- `stage4_protocol_regret_table.csv`
- `stage4_protocol_regret_table.md`
- `stage4_pareto_frontier_table.csv`
- `stage4_pareto_frontier_table.md`
- `stage4_single_protocol_only_table.csv`
- `stage4_single_protocol_only_table.md`
- `stage4_balanced_robustness_summary.md`
- `stage4_balanced_robustness_pareto.png`
- `stage4_protocol_regret_bar.png`

Generated CSV, Markdown, and PNG outputs under `experiments/results/` are
ignored and should not be committed.

The committed result interpretation is recorded separately in
`experiments/protocols/stage4ac_balanced_robustness_assets_result.md`.

## How To Run

From the repository root:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/generate_stage4_balanced_robustness_assets.py \
  --output-dir experiments/results/stage4_balanced_robustness_assets \
  --print-summary
```

If `matplotlib` is unavailable, the generator skips PNG plots with a warning
and still writes CSV/Markdown tables.

## How To Use In The Paper

Use Stage 4-AC assets to support:

- balanced governor framing
- protocol-specialist baseline discussion
- protocol regret analysis
- Pareto-frontier visualization

Paper-facing interpretation:

- `risk_adapter_v1` has the best mean valid count, best worst-protocol valid
  count, and lowest total regret among complete cross-protocol methods.
- `windlevel_s085` is the single-goal specialist.
- `fixed_s080` is the goal-reissue stress specialist.
- `risk_adapter_v21` is a strong nominal / single-goal variant but is
  dominated by `risk_adapter_v1` in the two-protocol plane.

## Claim Limits

- Do not claim statistical significance.
- Do not claim a safety guarantee.
- Do not collapse the two protocols into a single mixed-protocol aggregate as
  the main result.
- Do not claim learned methods dominate heuristic/static baselines.
- Do not claim `risk_adapter_v21` is overall best.
- Do not create `risk_adapter_v22` before reviewing Stage 4-AC outputs.
