# Stage 4-AF Abstract Introduction Draft

## Executive Summary

This document drafts the paper Abstract and Introduction for the reframed
Stage 4 paper.

It follows the Stage 4-AE paper outline / section skeleton:
`experiments/protocols/stage4ae_paper_outline_section_skeleton.md`.
Stage 4-AG now provides the current Method section draft:
`experiments/protocols/stage4ag_method_section_draft.md`.

`risk_adapter_v1` remains the current tentative balanced learned /
risk-conditioned protagonist. `risk_adapter_v21` remains a nominal /
single-goal variant or ablation, not the final method.

The wording is intentionally bounded: the paper should claim balanced or
protocol-level robustness under the tested protocols, not broad real-world
robustness, statistical significance, or a formal safety guarantee.

Title and framing language should continue to prefer "balanced robustness" or
"protocol-level robustness" over broader robustness wording.

## Candidate Final Title

Recommended title:

Risk-Conditioned Execution Governance for Balanced Suspended-Payload UAV
Transport in Strong Wind

Alternative titles:

1. Balanced Robustness Evaluation of Risk-Conditioned Execution Governors for
   Suspended-Payload UAVs
2. Protocol-Split Robustness for Risk-Conditioned Suspended-Payload UAV
   Transport in Strong Wind

## Abstract Draft

Suspended-payload UAV transport in strong wind is sensitive to runtime
execution aggressiveness: even with payload-aware planning, MPC, and low-level
control, the same planned motion can become too aggressive or overly
conservative under different wind and mission conditions. We propose a drop-in
risk-conditioned execution governor that adapts command execution through the
existing `speed_scale` and `acceleration_scale` interface, leaving the
planner/MPC/controller stack unchanged. To avoid a misleading single aggregate,
we evaluate strong-wind behavior under two protocols: a single-goal mission
protocol (`goal_repeat=1`) and a goal-reissue stress protocol
(`goal_repeat=10`). The results reveal strong protocol specialists:
`windlevel_s085` is best in the single-goal protocol with `26/30`
strict-valid runs, whereas `fixed_s080` is best in the stress protocol with
`24/30` strict-valid runs. Among the evaluated learned / risk-conditioned
methods, `risk_adapter_v1` is the most balanced, achieving the best mean valid
count (`24.0/30`), best worst-protocol count (`23/30`), and lowest total
regret (`2`) relative to the protocol oracles. Invalid-only failure groups and
representative traces further show that aggregate success hides distinct
failure modes, motivating failure-aware interpretation. These results support
protocol-split evaluation of learned execution governors while making no
statistical significance claim and providing no formal safety guarantee.

## Introduction Draft

Suspended-payload UAV transport enables aerial systems to move objects that
cannot be rigidly attached to the vehicle, but the suspended load also makes
the task sensitive to coupled vehicle-load dynamics. Under strong wind, small
tracking errors, payload swing, and transient speed changes can interact with
the cable-suspended payload and produce qualitatively different outcomes
across repeated runs. Robust transport in this setting therefore requires not
only feasible motion generation and tracking, but also careful control of how
aggressively the planned motion is executed.

Payload-aware planning, MPC, and low-level control provide the core stack for
generating and tracking feasible trajectories. However, improving these
components alone does not fully address the runtime execution-aggressiveness
problem. A fixed execution setting can be effective for one mission protocol
or wind/task phase while becoming too aggressive, too conservative, or poorly
timed in another. This creates a practical gap between trajectory feasibility
and balanced protocol-level robustness under repeated strong-wind evaluation.

We study execution governance as a drop-in layer on top of an AutoTrans-like
suspended-payload UAV stack. The governor modifies execution through
`speed_scale` and `acceleration_scale`, so it can be attached externally
without rewriting the planner, payload MPC, or SO3 controller. In the learned
variant, risk-conditioned signals are used to choose conservative or less
conservative execution scales, turning runtime aggressiveness into an
interface-level adaptation problem rather than a planner/controller redesign.

The evaluation also requires a protocol split. A single-goal mission protocol
(`goal_repeat=1`) tests one commanded mission and is closest to nominal
single-goal execution. A goal-reissue stress protocol (`goal_repeat=10`)
repeatedly republishes the goal and stresses reference-update, post-arrival,
and repeated-command behavior. Because these protocols expose different
failure modes and method rankings, collapsing them into a mixed-protocol
aggregate would obscure the trade-offs that matter for evaluated robustness.

Our completed strong-wind evaluation shows that no current learned variant
dominates both protocols. `windlevel_s085` is the single-goal specialist,
achieving `26/30` strict-valid runs under `goal_repeat=1`, while `fixed_s080`
is the goal-reissue stress specialist, achieving `24/30` strict-valid runs
under `goal_repeat=10`. The learned / risk-conditioned governor
`risk_adapter_v1` is the most balanced current method, with the best mean
valid count (`24.0/30`), best worst-protocol valid count (`23/30`), and lowest
total regret (`2`). By contrast, `risk_adapter_v21` remains a strong nominal /
single-goal variant, but it is weaker under stress and should not be framed as
the overall best method.

This paper makes four contributions. First, it presents a drop-in learned /
risk-conditioned execution governor for suspended-payload UAV transport that
adapts speed and acceleration scaling through an external interface. Second,
it introduces a protocol-split strong-wind evaluation separating single-goal
mission execution from goal-reissue stress. Third, it uses balanced robustness
and protocol regret to compare learned governors against strong heuristic and
fixed baselines. Fourth, it adds a failure-mode-aware diagnostic workflow using
invalid-only failure groups and representative traces. The resulting claims
are deliberately bounded: the evaluation supports balanced robustness under
the tested protocols, not statistical significance, learned-method uniform
domination, or a formal safety guarantee.

## Contribution Bullets

- We introduce a drop-in learned / risk-conditioned execution governor for
  suspended-payload UAV transport that adapts `speed_scale` and
  `acceleration_scale` without replacing the planner, payload MPC, or SO3
  controller.
- We define a protocol-split strong-wind evaluation that separates the
  single-goal mission protocol (`goal_repeat=1`) from the goal-reissue stress
  protocol (`goal_repeat=10`), avoiding a mixed-protocol aggregate as the main
  result.
- We report balanced robustness and protocol regret metrics showing that
  `risk_adapter_v1` is the most balanced current learned / risk-conditioned
  method, while `windlevel_s085` and `fixed_s080` are strong protocol
  specialists.
- We provide a failure-mode-aware diagnostic workflow based on invalid-only
  failure groups and representative traces, clarifying why aggregate
  strict-valid counts alone are insufficient for interpreting robustness.

## Claim Audit For Abstract/Intro

| claim | acceptable wording | avoid wording | reason |
| --- | --- | --- | --- |
| `risk_adapter_v1` most balanced | `risk_adapter_v1` is the most balanced current learned / risk-conditioned method under the tested protocols. | `risk_adapter_v1` is proven best or universally robust. | It has best mean, worst-protocol count, and total regret, but no statistical proof or universal guarantee. |
| `windlevel_s085` single-goal specialist | `windlevel_s085` is the single-goal specialist with `26/30` strict-valid runs. | `windlevel_s085` is the best method overall. | It leads `goal_repeat=1` but is weaker in the stress protocol. |
| `fixed_s080` stress specialist | `fixed_s080` is the goal-reissue stress specialist with `24/30` strict-valid runs. | `fixed_s080` solves robust transport. | It leads `goal_repeat=10` but is weaker in single-goal evaluation and is not a safety guarantee. |
| no learned uniform domination | No current learned variant dominates both protocols. | Learned methods dominate heuristic/static baselines. | Strong heuristic/static baselines are per-protocol leaders. |
| no safety guarantee | The governor improves balanced/protocol-level results in the tested evaluation but is not a formal safety filter. | The governor guarantees safety. | The method is empirical and does not provide formal safety proof. |
| no statistical significance | The counts support descriptive repeated-run comparison. | The gains are statistically significant. | No formal significance test is claimed. |

## Chinese Explanation

这个 abstract/introduction framing 比 “`risk_adapter_v21` 是赢家” 更安全，
因为现在的证据已经显示不同 protocol 的赢家不同：`windlevel_s085` 在
single-goal mission protocol 最强，`fixed_s080` 在 goal-reissue stress protocol
最强，而 `risk_adapter_v1` 的优势是 balanced robustness 和 total regret。这样写
能正面承认强 baseline 的存在，同时把论文贡献放在 risk-conditioned execution
governor、protocol-split evaluation 和 failure-aware analysis 上，避免把
`risk_adapter_v21` 过度包装成 final method。
