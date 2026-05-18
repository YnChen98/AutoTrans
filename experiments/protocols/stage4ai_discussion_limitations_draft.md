# Stage 4-AI Discussion Limitations Draft

## Executive Summary

This document records the current Discussion and Limitations draft for the
reframed Stage 4 paper.

The paper should argue for balanced robustness under the tested protocol split,
not universal learned-method dominance. The central interpretation is that
`risk_adapter_v1` is the current balanced learned / risk-conditioned execution
governor, while `windlevel_s085` and `fixed_s080` are strong protocol
specialists.

The current evidence does not justify introducing `risk_adapter_v22`. Stage
4-AA3 trace review points to multiple mechanism questions, including phase,
risk availability, reference health, and command/state health, rather than a
simple threshold patch.

Stage 4-AJ now assembles the current full paper draft:
`experiments/protocols/stage4aj_full_paper_assembly_draft.md`.

## Discussion Draft

### 5.1 Why Protocol Split Matters

The main empirical lesson from Stage 4 is that robustness depends on the mission
protocol. The single-goal mission protocol (`goal_repeat=1`) and the
goal-reissue stress protocol (`goal_repeat=10`) expose different method
rankings because they stress different parts of the execution stack. A single
goal primarily tests nominal goal-directed transport under strong wind, whereas
repeated goal publication stresses reference-update behavior, post-arrival
holding, and the interaction between replanning-like stimuli and command
adaptation.

This distinction changes the interpretation of the results. Under the
single-goal protocol, `windlevel_s085` is the strongest method with `26/30`
strict-valid runs. Under the goal-reissue stress protocol, `fixed_s080` is the
strongest method with `24/30` strict-valid runs. If the two protocols were
collapsed into one mixed aggregate, this specialist structure would be
obscured. The paper should therefore treat the protocol split as part of the
scientific result, not just as an evaluation detail.

The protocol split also clarifies the role of learned execution governance. No
current learned method is the absolute winner in both protocols. Instead, the
learned / risk-conditioned method `risk_adapter_v1` provides the best balance
across the two settings. This makes the correct paper claim narrower and more
useful: learned risk-conditioned execution governance can improve balanced
protocol-level behavior, but it does not remove the need to evaluate against
strong protocol-specific baselines.

### 5.2 Why Strong Simple Baselines Matter

The strong performance of simple baselines is not a weakness of the paper. It
is evidence that execution governance is a difficult and practically relevant
problem. A fixed or heuristic scale can be well matched to a specific protocol,
wind condition, and task phase. When this happens, a simple baseline can be very
hard to beat on its preferred regime.

This is exactly what the Stage 4 results show. `windlevel_s085` is a strong
single-goal specialist, while `fixed_s080` is a strong goal-reissue stress
specialist. These baselines prevent the paper from making an easy comparison
against weak alternatives. They also make the balanced robustness claim more
meaningful: `risk_adapter_v1` is not presented as winning every individual
protocol, but as maintaining high performance across protocols where different
simple baselines specialize.

For an IROS/ICRA/RA-L style system-method paper, this framing is stronger than
dismissing heuristics as crude. The contribution is not that every learned
variant dominates every static policy. The contribution is a stack-compatible
governor, a protocol-split evaluation, and a balanced robustness analysis that
reveals when adaptive execution is useful and when simple operating points
remain competitive.

### 5.3 Balanced Robustness as Deployment-Oriented Criterion

Within the tested protocols, balanced robustness is more informative than
single-protocol winning. A real execution governor should avoid being narrowly
optimized for one evaluation regime if that optimization creates a large
performance drop in another. The Stage 4 balanced metrics operationalize this
idea through mean valid count, worst-protocol valid count, and total regret
relative to the observed protocol oracles.

`risk_adapter_v1` is the current balanced protagonist under this criterion. It
achieves the best mean valid count (`24.0/30`), the best worst-protocol valid
count (`23/30`), and the lowest total regret (`2`). These metrics explain why
`risk_adapter_v1` should be centered in the paper even though the per-protocol
oracles are `windlevel_s085` for single-goal execution and `fixed_s080` for
goal-reissue stress.

This claim should remain descriptive and bounded. The results do not show that
`risk_adapter_v1` is statistically significantly better, universally best, or
safe by construction. They show that, among the currently evaluated complete
cross-protocol methods, `risk_adapter_v1` is the most balanced learned /
risk-conditioned governor under the tested strong-wind protocols.

### 5.4 Failure-Mode-Aware Interpretation

The failure analysis adds a second layer of interpretation beyond strict-valid
counts. The invalid-only failure groups separate failures into diagnostic
families such as `command_control_upstream`,
`planner_reference_upstream`, and `state_task_upstream`. These labels help
identify whether invalid runs are more associated with command/control
signals, reference or trajectory behavior, or state/task-level outcomes.

These groups should not be overinterpreted as exact root causes. They are
diagnostic labels derived from available logs and heuristics, and they should
be used to guide interpretation rather than to prove physical causality. The
paper-facing success metric remains strict-valid count, while failure groups
explain why aggregate success alone is insufficient.

Representative traces support this diagnostic interpretation. The Stage 4-AA3
review showed that Trial 4 goal-reissue stress failures for `risk_adapter_v21`
include early pre-arrival vulnerability and risk availability or timing issues,
not only post-arrival artifacts. Trial 6 single-goal traces also show that
lower scale is not automatically safer: conservative scaling can help some
runs, but it can also fail to resolve target/no-arrival behavior or delayed
post-arrival divergence. These observations motivate mechanism-aware future
work rather than a purely numerical threshold change.

### 5.5 Why `risk_adapter_v22` Is Not Introduced Yet

The current evidence does not justify adding `risk_adapter_v22` as the next
paper method. Stage 4-AA3 did not reveal a simple threshold correction that
would plausibly solve both the Trial 4 stress weakness and the Trial 6
single-goal bottleneck. The observed failures point to multiple interacting
mechanisms, including phase timing, risk signal availability, reference-update
health, and command/state divergence.

Introducing a new variant now would risk producing a trial-specific patch
rather than a reusable execution-governance mechanism. A future governor should
therefore be attempted only if the trace review and balanced metrics identify a
generic mechanism, such as phase-aware scaling, reference-health-aware
fallback, risk-confidence fallback, or command/state-health-aware intervention.
Until then, the paper should proceed with the `risk_adapter_v1`-centered
balanced robustness story and treat `risk_adapter_v21` as a strong nominal /
single-goal variant or ablation.

## Limitations Draft

The current evidence is simulation-only. The paper should not claim real-world
deployment performance, hardware robustness, or transfer to unmodeled vehicle,
payload, wind, or sensing conditions.

The execution governor is empirical and does not provide a formal safety
guarantee. It modulates `speed_scale` and `acceleration_scale` through the
command-adaptation interface, but it is not a certified safety filter and does
not replace feasibility checking, payload MPC, or low-level SO3 control.

The repeated-run counts are descriptive. The current evaluation does not make
a statistical significance claim, and the paper should not use language such as
"significantly better" unless a separate statistical analysis is added.

The failure groups are diagnostic rather than definitive root-cause labels.
Categories such as `command_control_upstream`,
`planner_reference_upstream`, and `state_task_upstream` help interpret invalid
runs, but they cannot by themselves prove the physical source of a failure.

The evaluated task set is limited to Trial 4, Trial 5, and Trial 6 under the
current strong-wind setting. These trials are useful stress cases, but they do
not cover the full space of wind profiles, payload masses, cable lengths,
obstacle arrangements, or mission commands.

No `risk_adapter_v22` final method is introduced. The paper should present
`risk_adapter_v1` as the current balanced protagonist and `risk_adapter_v21` as
a strong nominal / single-goal variant, while leaving future mechanism-driven
extensions for later work.

The risk score source, training set, calibration behavior, and online
confidence properties need clearer future documentation. This is especially
important because the trace review suggests that risk availability and timing
may affect stress-protocol failures.

`risk_adapter_v2` is not included in the complete balanced robustness table
because its goal-reissue stress result is missing. It can be mentioned as a
single-goal-only or historical variant, but it should not be used for complete
cross-protocol ranking.

## Future Work Draft

Future method work should be driven by representative traces rather than by
single-trial threshold tuning. A phase-aware governor could distinguish
pre-arrival, arrival, post-arrival hold, and repeated-goal phases before
selecting scale behavior.

Risk availability and confidence should be modeled explicitly. If short- or
long-horizon risk scores are unavailable, stale, delayed, or inconsistent, the
governor may need a fallback mode that is conservative in a structured way
rather than simply reusing the last scale.

The fixed-scale and wind-level frontier should be characterized more broadly.
Additional sweeps could test whether `fixed_s080`, `fixed_s085`, and
`windlevel_s085` remain specialists under other wind profiles, payload masses,
cable lengths, and target layouts.

Risk calibration and timing ablations would strengthen the learned-governor
claim. Useful checks include calibration curves, delayed-risk ablations,
shuffled-risk ablations, horizon-specific ablations, and comparisons between
risk-conditioned and risk-disabled versions of the same governor.

The command-adaptation interface should be ablated by channel. Speed-only,
acceleration-only, and combined `speed_scale` / `acceleration_scale` policies
would clarify whether the observed gains come from one channel, both channels,
or their interaction.

Broader evaluation should include additional wind profiles, payload masses,
cable lengths, and mission geometries. Hardware-in-the-loop or real hardware
validation would be needed before making claims about real-world deployment.

## Claim-Safety Table

| risky claim | safer wording | why |
| --- | --- | --- |
| Learned methods dominate heuristic/static baselines. | No current learned method uniformly dominates the strong heuristic/static specialists. | `windlevel_s085` wins single-goal and `fixed_s080` wins stress. |
| `risk_adapter_v1` is statistically best. | `risk_adapter_v1` has the best mean valid count, best worst-protocol count, and lowest total regret in the current descriptive evaluation. | No statistical significance analysis is claimed. |
| `risk_adapter_v1` guarantees safety. | `risk_adapter_v1` is an empirical execution governor and does not provide a formal safety guarantee. | The method is not a certified safety filter. |
| A failure group proves the root cause. | Failure groups provide diagnostic labels that guide interpretation. | The labels come from log-derived heuristics and are not physical proof. |
| Stress failures are all post-arrival. | Stage 4-AA3 shows that `risk_adapter_v21` stress failures include early pre-arrival failures as well as later failures. | Trial 4 stress traces include pre-arrival vulnerability. |
| `risk_adapter_v22` is necessary. | `risk_adapter_v22` should only be attempted if a reusable phase-aware, reference-aware, risk-health-aware, or failure-aware mechanism is established. | Current traces do not justify a simple threshold patch. |

## Chinese Explanation

Discussion 应该强调 balanced robustness，因为当前数据不是“learned method 全面胜
出”的故事，而是“不同 protocol 有不同 specialist，`risk_adapter_v1` 在两个
protocol 之间最平衡”的故事。这样写更符合 Table 1、Pareto plot 和 protocol
regret 的证据链。

强 baseline 不是尴尬点，反而是论文可信度来源。`windlevel_s085` 和
`fixed_s080` 说明简单策略在某些 protocol 下可以非常强，因此 `risk_adapter_v1`
的价值不是击败所有 baseline，而是在强 baseline 存在时仍然保持最好的 balance。

`risk_adapter_v22` 应该等待，因为 AA3 trace review 没有指出一个简单阈值修改就
能解决的问题。当前现象涉及 pre-arrival vulnerability、risk availability /
timing、reference health、post-arrival divergence 和 lower scale 不一定更安全。
如果现在直接做 v22，很容易变成 Trial-specific patch。

这种 Discussion 更适合 IROS/ICRA/RA-L：它承认 strong baseline，清楚限定 claim，
解释为什么 protocol split 和 failure analysis 必要，并把 future work 放在可复用
mechanism 上，而不是过度包装一个新 variant。
