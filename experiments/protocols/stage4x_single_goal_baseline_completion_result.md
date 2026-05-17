# Stage 4-X2 Single-Goal Baseline Completion Result

## Executive Summary

Stage 4-X2 completed the missing single-goal baseline matrix for the
single-goal mission protocol.

Under strong wind with `goal_repeat=1`, Trial 4/5/6, repeat1 through repeat10,
and strict-valid as the paper-facing metric, `windlevel_s085` achieved the
highest completed single-goal aggregate at `26/30`.

`risk_adapter_v1` and `risk_adapter_v21` each achieved `25/30`. Therefore
`risk_adapter_v21` remains competitive, but it is not the completed
single-goal aggregate winner. This changes the Stage 4-W paper-facing claim:
future Results must not describe `risk_adapter_v21` as the best single-goal
method or as beating all baselines.

## Protocol

- protocol: single-goal mission protocol
- `goal_repeat=1`
- wind: `strong`
- trials: Trial 4, Trial 5, Trial 6
- repeats: repeat1 through repeat10
- primary metric: strict-valid / `label_strict_invalid`

## Completed Single-Goal Table

| Method | Trial 4 | Trial 5 | Trial 6 | Aggregate |
| --- | ---: | ---: | ---: | ---: |
| `original` | `6/10` | `8/10` | `7/10` | `21/30` |
| `fixed_s085` | `5/10` | `9/10` | `8/10` | `22/30` |
| `windlevel_s085` | `8/10` | `9/10` | `9/10` | `26/30` |
| `fixed_s080` | `7/10` | `6/10` | `8/10` | `21/30` |
| `risk_adapter_v1` | `9/10` | `9/10` | `7/10` | `25/30` |
| `risk_adapter_v2` | `9/10` | `6/10` | `6/10` | `21/30` |
| `risk_adapter_v21` | `10/10` | `9/10` | `6/10` | `25/30` |

For `windlevel_s085`, command adaptation was confirmed active: mean, minimum,
and maximum command scale were all `0.85`.

For `risk_adapter_v1`, the aggregate mean of per-run mean scale was
`0.751218`.

## Ranking

| Rank | Method | Strict-valid count |
| ---: | --- | ---: |
| 1 | `windlevel_s085` | `26/30` |
| 2 | `risk_adapter_v1` | `25/30` |
| 2 | `risk_adapter_v21` | `25/30` |
| 4 | `fixed_s085` | `22/30` |
| 5 | `original` | `21/30` |
| 5 | `fixed_s080` | `21/30` |
| 5 | `risk_adapter_v2` | `21/30` |

## Key Findings

- `windlevel_s085` is a strong non-learning heuristic baseline under the
  completed single-goal mission protocol.
- `risk_adapter_v1` and `risk_adapter_v21` are competitive learned/adaptive
  variants, but they are not first in aggregate.
- `risk_adapter_v21` improves Trial 4 strongly with `10/10`, but Trial 6
  remains weak at `6/10`.
- `windlevel_s085` is particularly strong on Trial 5 and Trial 6, with `9/10`
  on both.
- The completed result argues for stronger ablations and clearer baseline
  framing rather than immediate additional variant tuning.
- `fixed_s085` and `windlevel_s085` both use `0.85`-like scaling, but they use
  different execution paths. `fixed_s085` is XML/static scaling, while
  `windlevel_s085` is topic-based command adaptation and must be treated as a
  separate method.

## Claim Updates

Future paper Results must no longer claim:

- `risk_adapter_v21` is the best single-goal method.
- `risk_adapter_v21` beats all baselines.
- a learned governor dominates simple heuristic baselines.

Safe claim:

`risk_adapter_v21` is competitive with `risk_adapter_v1` and improves over
`original`, `fixed_s080`, `fixed_s085`, and `risk_adapter_v2` in the completed
single-goal aggregate, but `windlevel_s085` is strongest in the completed
single-goal aggregate.

## Relationship To Goal-Reissue Stress

Current goal-reissue stress protocol results remain separate:

| Method | Strict-valid count |
| --- | ---: |
| `fixed_s080` | `24/30` |
| `risk_adapter_v1` | `23/30` |
| `risk_adapter_v21` | `20/30` |
| `original` | `18/30` |
| `fixed_s085` | `18/30` |
| `windlevel_s085` | `16/30` |

No single current learned variant dominates both protocols. `risk_adapter_v1`
is stronger than `risk_adapter_v21` under goal-reissue stress, while both are
below `fixed_s080` in that protocol. `windlevel_s085` leads the completed
single-goal aggregate but is weakest in the current goal-reissue stress
aggregate.

## Research Decision

- Do not create `risk_adapter_v22` immediately.
- First update protocol-split paper assets with the completed single-goal table
  and corrected goal-reissue stress table.
- Then decide between option A, learned governor analysis with a strong
  heuristic frontier, and option B, a new phase-aware final method after
  failure analysis.

## What Not To Claim

- Do not claim statistical significance.
- Do not claim a safety guarantee.
- Do not create a mixed-protocol aggregate.
- Do not claim `risk_adapter_v21` is the overall winner.
- Do not claim a learned method uniformly dominates heuristic or fixed
  baselines.
- Do not treat diagnostic labels as perfect root-cause proof.
