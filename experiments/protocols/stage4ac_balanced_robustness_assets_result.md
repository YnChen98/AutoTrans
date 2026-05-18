# Stage 4-AC2 Balanced Robustness Result

## Executive Summary

Stage 4-AC balanced robustness / protocol regret result is complete.

`risk_adapter_v1` has the best mean valid count (`24.0/30`), the best
worst-protocol valid count (`23/30`), and the lowest total regret (`2`) among
complete cross-protocol methods. It should be the tentative balanced learned /
risk-conditioned protagonist for the paper.

`windlevel_s085` and `fixed_s080` are strong protocol specialists:
`windlevel_s085` is best under the single-goal mission protocol, while
`fixed_s080` is best under goal-reissue stress. `risk_adapter_v21` remains a
strong nominal / single-goal variant, but it is weaker under stress and should
not be the final protagonist.

Balanced robustness / protocol regret is the correct paper-facing framing for
the current Stage 4 result.

Stage 4-AD defines the paper figure/table placement that should carry these
metrics into the main Results and Failure Analysis sections:
`experiments/protocols/stage4ad_paper_figure_table_plan.md`.

## Protocol Oracle Definition

- Single-goal mission oracle: `windlevel_s085`, `26/30`.
- Goal-reissue stress oracle: `fixed_s080`, `24/30`.

Protocol regret is measured relative to these two protocol-specific oracles.

## Balanced Robustness Table

| method | single | stress | mean | worst | gap | total regret | role |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `original` | `21/30` | `18/30` | `19.5/30` | `18/30` | `3` | `11` | unadapted baseline |
| `fixed_s085` | `22/30` | `18/30` | `20.0/30` | `18/30` | `4` | `10` | fixed static baseline |
| `windlevel_s085` | `26/30` | `16/30` | `21.0/30` | `16/30` | `10` | `8` | single-goal specialist heuristic |
| `fixed_s080` | `21/30` | `24/30` | `22.5/30` | `21/30` | `3` | `5` | stress specialist static frontier |
| `risk_adapter_v1` | `25/30` | `23/30` | `24.0/30` | `23/30` | `2` | `2` | balanced learned / risk-conditioned governor |
| `risk_adapter_v21` | `25/30` | `20/30` | `22.5/30` | `20/30` | `5` | `5` | strong nominal / single-goal learned variant |

`risk_adapter_v2` has a completed single-goal result (`21/30`) but no completed
goal-reissue stress result in the current protocol-split matrix, so it is
excluded from complete cross-protocol balanced ranking.

## Pareto Frontier

Pareto-frontier methods:

- `windlevel_s085`
- `fixed_s080`
- `risk_adapter_v1`

`risk_adapter_v21` is not on the Pareto frontier because `risk_adapter_v1` has
the same single-goal count (`25/30`) and a higher stress count (`23/30` versus
`20/30`).

## Paper-Facing Interpretation

Safe claims:

- `risk_adapter_v1` is the most balanced learned / risk-conditioned method in
  the current evaluation.
- Heuristic/static baselines specialize to one protocol:
  `windlevel_s085` for single-goal mission and `fixed_s080` for goal-reissue
  stress.
- Balanced robustness and protocol regret expose trade-offs hidden by
  single-protocol success.

Claims to avoid:

- `risk_adapter_v1` is statistically significantly best.
- A learned method dominates all heuristic/static baselines.
- `risk_adapter_v21` is overall best.
- A single mixed-protocol aggregate is the main result.

## Research Decision

Do not create `risk_adapter_v22` yet.

Use the Stage 4-AD paper figure/table plan for Results writing with the Stage
4-AC assets. A future `risk_adapter_v22` should be considered only if later
work requires a clearly mechanism-driven extension.

Stage 4-AD records that figure/table plan and sets Stage 4-AE as the next
writing step: paper outline / section skeleton.

## What Not To Claim

- Do not claim statistical significance.
- Do not claim a safety guarantee.
- Do not claim learned methods uniformly dominate heuristic/static baselines.
- Do not use a mixed-protocol aggregate as the main result.
- Do not claim `risk_adapter_v21` is the final method.
