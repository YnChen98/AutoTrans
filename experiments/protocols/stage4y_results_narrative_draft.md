# Stage 4-Y Results Narrative Draft

## Executive Summary

Stage 4 results are now interpreted with an explicit protocol split:

- single-goal mission protocol: `goal_repeat=1`
- goal-reissue stress protocol: `goal_repeat=10`

The completed protocol-split comparison does not support a universal winner
claim. `windlevel_s085` is strongest in the single-goal mission protocol,
`fixed_s080` is strongest in the goal-reissue stress protocol, and no current
learned variant dominates both protocols.

## Paper-Ready Results Subsection

We evaluated command-adaptation strategies under two protocol-labeled
strong-wind benchmarks using strict-valid rate as the paper-facing metric. In
the single-goal mission protocol (`goal_repeat=1`), each method was evaluated
over Trial 4, Trial 5, and Trial 6 with 10 repeats per trial. The wind-level
heuristic adapter `windlevel_s085` achieved the highest aggregate strict-valid
rate, with `26/30` successful runs. The learned/risk-conditioned variants
`risk_adapter_v1` and `risk_adapter_v21` each achieved `25/30`, while
`fixed_s085` achieved `22/30` and `original`, `fixed_s080`, and
`risk_adapter_v2` each achieved `21/30`.

The goal-reissue stress protocol (`goal_repeat=10`) produced a different
method ordering. In this protocol, the tuned static frontier `fixed_s080`
achieved the highest strict-valid rate with `24/30` successful runs, followed
by `risk_adapter_v1` at `23/30`. The later `risk_adapter_v21` variant achieved
`20/30`, above `original` and `fixed_s085` (`18/30` each) and
`windlevel_s085` (`16/30`), but below both `fixed_s080` and
`risk_adapter_v1`.

These results show that the evaluation protocol materially affects the
relative ranking of adaptation strategies. A simple wind-level heuristic is
strongest for single-goal execution, whereas a tuned static scale is strongest
under goal-reissue stress. The learned governors remain competitive, but the
current `risk_adapter_v21` result does not support a claim that it dominates
both protocols or beats all baselines.

Therefore, the Stage 4 result should be interpreted as evidence for
protocol-dependent robustness and for the value of evaluating learned
execution governors against strong heuristic and static frontiers. The current
counts do not establish statistical significance, do not provide a safety
guarantee, and should not be mixed into a single cross-protocol aggregate.

## Chinese Explanation

这个结果仍然有价值，因为它把 Stage 4 从“找一个绝对赢家”推进到了更清楚的
protocol-dependent robustness 分析。`goal_repeat=1` 和 `goal_repeat=10` 测的不是同一件事：前者更接近单次任务执行，后者会反复发布同一个 goal，暴露 goal-reissue / post-arrival replan stress 下的弱点。因此两个 protocol 分开报告，能更准确地说明方法在不同执行条件下的表现。

`risk_adapter_v21` 不能被称为 overall best，因为它在 single-goal mission protocol 里是 `25/30`，低于 `windlevel_s085` 的 `26/30`；在 goal-reissue stress protocol 里是 `20/30`，低于 `fixed_s080` 的 `24/30` 和 `risk_adapter_v1` 的 `23/30`。它仍然是有竞争力的 learned/risk-conditioned variant，但不是跨 protocol 的最终赢家。

`windlevel_s085` 和 `fixed_s080` 都是很强的 baseline。`windlevel_s085` 说明简单的 topic-based wind-level heuristic 在单次任务执行中非常有效；`fixed_s080` 说明 tuned static frontier 在 goal-reissue stress 下仍然很强。这两个 baseline 抬高了论文的证据标准：learned governor 不能只和原始系统比较，还必须和强 heuristic/static frontier 比较。

因此论文更适合被定位为 learned risk-conditioned execution governor +
dual-protocol evaluation + strong baseline comparison + failure-mode-aware
analysis，而不是“一个 learned method 在所有条件下统一获胜”。这种定位更稳妥，也更能突出平台和评价框架的贡献。

## Safe Claims Table

| claim | status | supporting result | caveat |
| --- | --- | --- | --- |
| Under the single-goal mission protocol, `windlevel_s085` achieved `26/30` strict-valid. | safe | `windlevel_s085` is highest in `goal_repeat=1`. | This does not imply superiority under `goal_repeat=10`. |
| Under the single-goal mission protocol, `risk_adapter_v1` and `risk_adapter_v21` each achieved `25/30`. | safe | Both learned/risk-conditioned variants tie in `goal_repeat=1`. | They are below `windlevel_s085` by one strict-valid run. |
| Under goal-reissue stress, `fixed_s080` achieved `24/30` strict-valid. | safe | `fixed_s080` is highest in `goal_repeat=10`. | This is a tuned static frontier, not a safety guarantee. |
| No current learned variant dominates both protocols. | safe | `risk_adapter_v21` is `25/30` single-goal and `20/30` stress; `risk_adapter_v1` is `25/30` single-goal and `23/30` stress. | Dominance may change only after new method design and evaluation. |
| The protocol split exposes protocol-dependent robustness. | safe | Single-goal leader is `windlevel_s085`; stress leader is `fixed_s080`. | Do not collapse the two protocols into one aggregate. |

## Claims To Avoid Table

| claim to avoid | reason |
| --- | --- |
| `risk_adapter_v21` beats all baselines. | False after Stage 4-X2: `windlevel_s085` is higher in single-goal, and `fixed_s080` / `risk_adapter_v1` are higher under stress. |
| `risk_adapter_v21` is overall best. | No single current method wins both protocols. |
| Learned methods uniformly dominate heuristic/fixed baselines. | `windlevel_s085` and `fixed_s080` are the protocol leaders. |
| Mixed-protocol aggregate claims. | `goal_repeat=1` and `goal_repeat=10` test different system properties. |
| Statistical significance. | The current repeated-run counts support descriptive comparison, not formal significance. |
| Safety guarantee. | Strict-valid rates in simulation do not prove safety. |
| All NaN/divergence failures are caused by command adaptation. | Diagnostic labels are not perfect root-cause proof. |

## Suggested Paper Framing

Frame the paper as:

- learned risk-conditioned execution governor
- dual-protocol evaluation
- strong heuristic/static frontier comparison
- failure-mode-aware analysis

Do not frame the paper as:

- a single method universally winning all conditions

## Next Recommended Work

- Build a failure-mode summary table or figure.
- Inspect Trial 4 stress failures and Trial 6 bottlenecks.
- Design a dynamic heuristic or ablation only after the failure-mode table is
  stable.
- Do not create `risk_adapter_v22` immediately.
