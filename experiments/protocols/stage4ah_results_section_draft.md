# Stage 4-AH Results Section Draft

## Executive Summary

This document records the current Results section draft for the reframed Stage
4 paper.

The Results should be organized by protocol split and balanced robustness, not
by a single mixed-protocol aggregate. The single-goal mission protocol
(`goal_repeat=1`) and the goal-reissue stress protocol (`goal_repeat=10`)
expose different method rankings and failure patterns.

`risk_adapter_v1` is the current balanced learned / risk-conditioned
protagonist. It does not win every protocol, but it has the best mean valid
count, best worst-protocol valid count, and lowest total regret in the
completed two-protocol evaluation.

No learned method uniformly dominates heuristic or fixed baselines. The paper
should explicitly respect `windlevel_s085` as the single-goal specialist and
`fixed_s080` as the goal-reissue stress specialist.

## Results Section Draft

### 4.1 Protocol-Split Success Rates

The strong-wind evaluation separates single-goal mission execution from
goal-reissue stress. This protocol split is important because the same method
can behave differently when the system receives one goal command versus repeated
post-arrival or reference-update stimuli. We therefore report strict-valid
counts separately for the single-goal mission protocol (`goal_repeat=1`) and
the goal-reissue stress protocol (`goal_repeat=10`), rather than collapsing the
two settings into a mixed aggregate.

In the single-goal mission protocol, the strongest method in the evaluated set
is the heuristic `windlevel_s085`, which achieves `26/30` strict-valid runs.
The learned / risk-conditioned methods `risk_adapter_v1` and
`risk_adapter_v21` are both competitive in this setting, each achieving
`25/30` strict-valid runs. The fixed and unadapted baselines are lower:
`fixed_s085` achieves `22/30`, while `original`, `fixed_s080`, and
`risk_adapter_v2` each achieve `21/30`.

In the goal-reissue stress protocol, the ranking changes. The tuned static
baseline `fixed_s080` is strongest with `24/30` strict-valid runs.
`risk_adapter_v1` follows closely with `23/30`, while `risk_adapter_v21`
drops to `20/30`. The remaining baselines achieve `18/30` for `original`,
`18/30` for `fixed_s085`, and `16/30` for `windlevel_s085`.

These results show that the protocols test different robustness properties.
`windlevel_s085` is the single-goal winner, whereas `fixed_s080` is the stress
winner. Among learned / risk-conditioned methods, `risk_adapter_v1` is the
most balanced across the two protocols, while `risk_adapter_v21` is strong in
single-goal execution but weaker under goal-reissue stress.

### 4.2 Balanced Robustness and Protocol Regret

Balanced robustness is evaluated using the complete cross-protocol matrix from
Stage 4-AC. The protocol oracles are the best observed method in each protocol:
`windlevel_s085` with `26/30` in the single-goal mission protocol and
`fixed_s080` with `24/30` in the goal-reissue stress protocol. Protocol regret
measures how far each method falls below these observed oracles.

Under this view, `risk_adapter_v1` has the strongest balanced performance. It
achieves a mean valid count of `24.0/30`, the best worst-protocol count of
`23/30`, and the lowest total regret of `2`. This is the main reason for
centering `risk_adapter_v1` as the paper's balanced learned /
risk-conditioned execution governor.

The specialist baselines expose the trade-off that a single protocol would
hide. `windlevel_s085` reaches the single-goal oracle with `26/30`, but falls
to `16/30` under stress, producing a large protocol gap. Conversely,
`fixed_s080` reaches the stress oracle with `24/30`, but achieves only
`21/30` in the single-goal mission protocol. These methods are important
baselines because they show that simple policies can be very strong when
matched to one protocol.

The observed Pareto frontier contains `windlevel_s085`, `fixed_s080`, and
`risk_adapter_v1`. `risk_adapter_v21` is not on the frontier because it has
the same single-goal count as `risk_adapter_v1` (`25/30`) but a lower stress
count (`20/30` versus `23/30`). Thus, in the two-protocol plane,
`risk_adapter_v21` is dominated by `risk_adapter_v1`.

### 4.3 Failure-Mode-Aware Diagnosis

Protocol-split success counts explain which methods are stronger, but they do
not explain how invalid runs occur. We therefore use the Stage 4-Z2
invalid-only failure groups as a diagnostic view. These labels should be read
as failure-analysis categories, not exact physical root-cause proof; the
paper-facing success metric remains strict-valid count.

In the single-goal protocol, the invalid runs for `windlevel_s085` are
concentrated in `state_task_upstream=4`. For `risk_adapter_v1`, the invalid
groups are `command_control_upstream=2` and `state_task_upstream=3`. For
`risk_adapter_v21`, they are `command_control_upstream=1` and
`state_task_upstream=4`. This suggests that even strong single-goal methods
can fail through different upstream pathways, and that learned governors do
not eliminate the state/task-related failure family.

In the goal-reissue stress protocol, the specialist `fixed_s080` has
`command_control_upstream=4` and `state_task_upstream=2` invalid groups.
`risk_adapter_v1` has `command_control_upstream=3`,
`planner_reference_upstream=1`, and `state_task_upstream=3`. By contrast,
`risk_adapter_v21` has `command_control_upstream=5`,
`planner_reference_upstream=3`, and `state_task_upstream=2`. The larger
planner-reference and command/control components in the `risk_adapter_v21`
stress failures are consistent with its weaker stress-protocol result.

This diagnostic view supports the reframed paper claim: aggregate strict-valid
counts alone are insufficient for interpreting robustness. The failure groups
show heterogeneous invalid-run patterns across methods and protocols, which
motivates pairing success-rate tables with failure-mode-aware analysis.

### 4.4 Representative Trace Analysis

Representative traces from Stage 4-AA2 and the Stage 4-AA3 human review add a
case-study view of the same trade-offs. In Trial 4 under goal-reissue stress,
several `risk_adapter_v21` failures occur before arrival rather than only
after post-arrival goal republishes. These traces point to early pre-arrival
vulnerability and risk availability or timing issues, not merely a
goal-reissue artifact.

Trial 6 under the single-goal protocol shows a different pattern. A
`risk_adapter_v21` invalid run reaches arrival first and then diverges later
under `goal_repeat=1`, indicating delayed post-arrival divergence even without
goal reissue. The same trace set also shows that lower command scale is not
automatically safer: conservative scaling can help some runs arrive, but it
can also contribute to target/no-arrival style failures or fail to prevent
later state divergence.

The successful traces for `windlevel_s085` and `fixed_s080` show stable
arrival and hold behavior in their respective favorable settings.
`windlevel_s085` supports the single-goal specialist interpretation, while
`fixed_s080` supports the conservative stress-specialist interpretation.
These trace-level observations motivate caution before introducing
`risk_adapter_v22`: the current evidence points to multiple generic mechanism
questions rather than one obvious threshold patch.

### 4.5 Summary of Findings

- Simple baselines are strong protocol specialists: `windlevel_s085` leads the
  single-goal protocol and `fixed_s080` leads the goal-reissue stress protocol.
- `risk_adapter_v1` is the most balanced current learned / risk-conditioned
  method by mean valid count, worst-protocol valid count, and total regret.
- `risk_adapter_v21` improves nominal / single-goal behavior but is weaker
  under goal-reissue stress and is dominated by `risk_adapter_v1` in the
  two-protocol plane.
- Protocol split and invalid-only failure groups are necessary to interpret
  robustness; a single mixed aggregate would hide specialist trade-offs.
- The current evidence does not support a safety guarantee, statistical
  significance claim, or learned-method uniform domination claim.

## Main Table Draft

Table 1 should be the main paper table for protocol-split success and balanced
robustness.

| method | single-goal strict-valid | stress strict-valid | mean valid | worst-protocol valid | total regret | role |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `original` | `21/30` | `18/30` | `19.5/30` | `18/30` | `11` | unadapted baseline |
| `fixed_s085` | `22/30` | `18/30` | `20.0/30` | `18/30` | `10` | fixed static baseline |
| `windlevel_s085` | `26/30` | `16/30` | `21.0/30` | `16/30` | `8` | single-goal specialist heuristic |
| `fixed_s080` | `21/30` | `24/30` | `22.5/30` | `21/30` | `5` | goal-reissue stress specialist static frontier |
| `risk_adapter_v1` | `25/30` | `23/30` | `24.0/30` | `23/30` | `2` | balanced learned / risk-conditioned governor |
| `risk_adapter_v21` | `25/30` | `20/30` | `22.5/30` | `20/30` | `5` | strong nominal / single-goal learned variant |

`risk_adapter_v2` should be treated as a single-goal-only appendix note in the
current complete cross-protocol paper table because its goal-reissue stress
result is missing.

## Figure Reference Draft

Table 1 reports the protocol-split strict-valid counts and balanced robustness
metrics. It should be the first numerical anchor in the Results section.

Figure 3 should plot the two-protocol Pareto plane with single-goal valid
count on the x-axis and goal-reissue stress valid count on the y-axis. The text
should point out that `windlevel_s085`, `fixed_s080`, and `risk_adapter_v1`
form the observed Pareto frontier, while `risk_adapter_v21` is dominated by
`risk_adapter_v1`.

Figure 4 should show protocol regret relative to the observed protocol
oracles. The Results text should use this figure to explain why
`risk_adapter_v1` is the balanced protagonist even though it is not the
absolute winner in either individual protocol.

Figure 5 should show invalid-only failure groups. The text should emphasize
that this is a diagnostic view of invalid runs, not a replacement for
strict-valid success or a root-cause proof.

Figure 6 should present representative trace case studies. The Results text
should connect Trial 4 stress traces to `risk_adapter_v21` early pre-arrival
vulnerability and Trial 6 single-goal traces to the observation that lower
scale is not automatically safer.

## Chinese Explanation

Results 部分应该先讲 protocol split，因为现在的核心发现不是某一个方法在所有
条件下全面胜出，而是不同 protocol 暴露了不同的强项和弱点。single-goal
mission protocol 里 `windlevel_s085` 最强，goal-reissue stress protocol 里
`fixed_s080` 最强；如果把两个 protocol 混成一个 aggregate，会掩盖这个关键
trade-off。

`risk_adapter_v1` 仍然应该是 protagonist，因为它的优势是 balanced robustness：
mean valid count、worst-protocol valid count 和 total regret 都最好。它不需要
赢下每一个 protocol 才能成为论文主角；论文主张应该是它在当前测试 protocol
下最平衡，而不是它“全面最好”。

`windlevel_s085` 和 `fixed_s080` 必须被认真对待为 strong specialists。这样写
更符合数据，也会让 reviewer 看到论文没有回避简单而强的 baseline。

现在还不应该引入 `risk_adapter_v22`，因为 AA3 traces 显示问题不是单一阈值能
解决的：Trial 4 stress 有 early pre-arrival vulnerability 和 risk timing 问题，
Trial 6 single-goal 还存在 delayed post-arrival divergence，而且 lower scale
并不自动更安全。下一步应该先写 Discussion / Limitations 或组装论文，而不是
立刻做新 variant。

## Claim Audit

| results claim | supported wording | avoid wording | supporting table/figure |
| --- | --- | --- | --- |
| `risk_adapter_v1` most balanced | `risk_adapter_v1` is the most balanced current learned / risk-conditioned method by mean valid count, worst-protocol count, and total regret. | `risk_adapter_v1` is universally best. | Table 1, Figure 3, Figure 4 |
| `windlevel_s085` single-goal specialist | `windlevel_s085` is the single-goal specialist with `26/30` strict-valid runs. | `windlevel_s085` is the overall best method. | Table 1, Figure 3 |
| `fixed_s080` stress specialist | `fixed_s080` is the goal-reissue stress specialist with `24/30` strict-valid runs. | `fixed_s080` solves robust transport. | Table 1, Figure 3 |
| `risk_adapter_v21` dominated by `risk_adapter_v1` | `risk_adapter_v21` is dominated by `risk_adapter_v1` in the two-protocol plane because both have `25/30` single-goal, while `risk_adapter_v1` has higher stress performance. | `risk_adapter_v21` is the final cross-protocol method. | Table 1, Figure 3 |
| no learned uniform domination | No current learned method uniformly dominates the heuristic/static specialists. | Learned governors dominate all baselines. | Table 1, Figure 3 |
| no statistical significance | The repeated-run counts are descriptive under the tested protocols. | The improvement is statistically significant. | Table 1 |
| no safety guarantee | The governor is evaluated empirically and is not a formal safety filter. | The method guarantees safe execution. | Figure 1, Table 1, Figure 5, Figure 6 |
