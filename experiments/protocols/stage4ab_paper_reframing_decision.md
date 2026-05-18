# Stage 4-AB Paper Reframing Decision

## Executive Summary

The Stage 4 paper should be reframed away from a `risk_adapter_v21`-as-winner
story. The completed protocol-split comparison and failure-mode analysis do
not support a final cross-protocol winner claim for `risk_adapter_v21`.

The tentative paper protagonist should be `risk_adapter_v1` as the most
balanced learned / risk-conditioned execution governor among the current
evaluated variants. It does not dominate every protocol, but it has the best
cross-protocol balance in the completed dual-protocol comparison.

`risk_adapter_v21` should be treated as a strong nominal variant / ablation:
it is strong in the single-goal mission protocol, but weaker under
goal-reissue stress and should not be framed as the final cross-protocol
method.

The strong heuristic/static baselines should be framed as protocol
specialists:

- `windlevel_s085`: single-goal mission specialist.
- `fixed_s080`: goal-reissue stress specialist.

## Current Evidence

The protocol oracle is the best observed strict-valid count in each protocol:

- single-goal mission protocol (`goal_repeat=1`): `26/30`, achieved by
  `windlevel_s085`
- goal-reissue stress protocol (`goal_repeat=10`): `24/30`, achieved by
  `fixed_s080`

For methods evaluated in both protocols:

`total_regret = (26 - single_goal_count) + (24 - stress_count)`

The mean and worst-protocol columns use strict-valid counts out of `30`.
`risk_adapter_v2` does not have a completed goal-reissue stress cell in the
current protocol-split table, so dual-protocol balance metrics are not
assigned for it.

| method | single-goal | stress | mean | worst protocol | total regret relative to protocol oracle |
| --- | ---: | ---: | ---: | --- | ---: |
| `original` | `21/30` | `18/30` | `19.5/30` | stress `18/30` | `11` |
| `fixed_s085` | `22/30` | `18/30` | `20.0/30` | stress `18/30` | `10` |
| `windlevel_s085` | `26/30` | `16/30` | `21.0/30` | stress `16/30` | `8` |
| `fixed_s080` | `21/30` | `24/30` | `22.5/30` | single-goal `21/30` | `5` |
| `risk_adapter_v1` | `25/30` | `23/30` | `24.0/30` | stress `23/30` | `2` |
| `risk_adapter_v2` | `21/30` | n/a | n/a | n/a | n/a |
| `risk_adapter_v21` | `25/30` | `20/30` | `22.5/30` | stress `20/30` | `5` |

This table supports a balanced-governor framing for `risk_adapter_v1`, not a
`risk_adapter_v21` final-winner framing. It also shows why the strong
heuristic/static baselines should be discussed as protocol specialists rather
than weak baselines.

## Paper Claim Reset

Safe claims:

- Learned governors are competitive with strong heuristic/static baselines.
- `risk_adapter_v1` is the most balanced learned / risk-conditioned governor
  among the current evaluated variants.
- The protocol split reveals specialization: `windlevel_s085` is strongest in
  the single-goal mission protocol, while `fixed_s080` is strongest in the
  goal-reissue stress protocol.
- Failure-mode analysis explains why aggregate success alone is insufficient
  for interpreting robustness.

Claims to avoid:

- `risk_adapter_v21` is overall best.
- Learned methods dominate heuristic/static baselines.
- A single mixed-protocol aggregate is the main result.
- The current counts establish statistical significance.
- The current counts or failure labels provide a safety guarantee.

## Method Framing

Frame the paper around:

- learned risk-conditioned execution governor
- protocol-split robustness evaluation
- balanced robustness / regret analysis
- failure-mode-aware diagnosis

This framing keeps the contribution focused on evaluation discipline and
balanced governor behavior, while still acknowledging that simple
protocol-specialist baselines are strong.

## Immediate Next Steps

- Stage 4-AA2 representative trace inspection:
  inspect representative Trial 4 stress failures and Trial 6 bottlenecks before
  any new method design.
- Stage 4-AC balanced robustness asset generator:
  generate paper assets for mean performance, worst-protocol performance, and
  total regret relative to the protocol oracle.
- Do not create `risk_adapter_v22` before Stage 4-AA2 and balanced robustness
  metrics are complete.

## Decision Rule For v22

Create `risk_adapter_v22` only if Stage 4-AA2 reveals a generic phase-aware or
failure-aware mechanism that can plausibly improve both protocol balance and
failure behavior.

Do not create a Trial-4-specific or target-specific patch. A new variant must
address a reusable mechanism, not one observed cell in the evaluation table.

If no generic mechanism appears, proceed with a `risk_adapter_v1`-centered
paper narrative and use `risk_adapter_v21` as a strong nominal variant /
ablation rather than as the final method.
