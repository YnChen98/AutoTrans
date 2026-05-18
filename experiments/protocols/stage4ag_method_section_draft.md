# Stage 4-AG Method Section Draft

## Executive Summary

This document drafts the paper Method section for the reframed Stage 4 paper.

The method is a stack-compatible execution governor for suspended-payload UAV
transport under strong wind. It adapts execution aggressiveness through the
existing command-adaptation interface rather than replacing the planner,
payload MPC, or SO3 controller.

`risk_adapter_v1` is the current balanced learned / risk-conditioned
protagonist because it has the best mean valid count (`24.0/30`), best
worst-protocol valid count (`23/30`), and lowest total regret (`2`) in the
completed protocol-split evaluation.

`risk_adapter_v21` remains a strong nominal / single-goal variant or ablation,
not the final method.

Stage 4-AH now drafts the Results section using the same `risk_adapter_v1`
centered balanced robustness framing:
`experiments/protocols/stage4ah_results_section_draft.md`.
Stage 4-AI expands the Method claim boundaries in the Discussion and
Limitations draft:
`experiments/protocols/stage4ai_discussion_limitations_draft.md`.

## Method Section Draft

### 2.1 System Stack and Problem Setting

We consider suspended-payload UAV transport under wind, where the vehicle must
move a cable-suspended load to a target while limiting tracking degradation,
payload swing, and arrival failures. The suspended payload couples the UAV
motion to load dynamics, so execution aggressiveness can change the effective
difficulty of the same nominal trajectory. Under strong wind, a command that is
feasible in one run can become too aggressive or poorly timed in another.

The underlying system follows an AutoTrans-like stack composed of a
payload-aware planner, a payload MPC, and an SO3 controller. The planner
generates nominal motion references, the payload MPC tracks these references
while accounting for the load, and the SO3 controller provides the low-level
vehicle control interface. In this paper, these core stack components are kept
unchanged.

The method objective is to adapt runtime execution scale, not to redesign the
planner or controller. We treat execution aggressiveness as an online
governance problem: given risk-related signals and the current execution
context, the governor selects speed and acceleration scales that modulate how
the nominal command is executed. This setting lets the same planner/MPC/SO3
stack be evaluated with no-op execution, fixed static scaling, heuristic
scaling, and learned / risk-conditioned scaling.

### 2.2 Execution-Governor Interface

The execution governor publishes two scalar adaptation signals:
`speed_scale` and `acceleration_scale`. These signals are consumed by the
command-adaptation interface and modify the aggressiveness of the executed
motion command. A scale near `1.0` preserves the nominal command more closely,
whereas smaller scales reduce the commanded speed or acceleration and make the
executed motion more conservative.

This interface is intentionally stack-compatible. The planner continues to
produce the nominal reference, the payload MPC continues to solve the tracking
problem, and the SO3 controller remains the low-level controller. The governor
only changes the execution scale exposed through the command-adaptation
interface. This design makes it possible to compare learned, heuristic, fixed,
and no-op policies while holding the core planning and control stack fixed.

The interface also makes the paper's claim boundary explicit. A governor can
improve balanced protocol-level results by changing execution aggressiveness,
but it is not a replacement for feasibility checking, payload-aware control, or
low-level stabilization. The evaluation therefore measures empirical behavior
under repeated strong-wind protocols rather than proving closed-loop safety.

### 2.3 Risk-Conditioned Governor

The learned governor uses risk-conditioned decision logic to choose execution
scales. At a high level, the governor receives short-horizon and long-horizon
risk estimates, denoted here as `r_3` and `r_5`, together with execution
context such as the active method mode and command-adaptation state. The
short-horizon risk captures imminent instability or tracking stress, while the
long-horizon risk captures a broader upcoming window where conservative
execution may be useful.

The governor maps these signals to a pair of scale values. In low-risk
conditions, it keeps execution less conservative so that the system can
continue progressing toward the goal. When risk increases, it reduces the
speed and acceleration scales to avoid overly aggressive execution. When the
long-horizon risk is high enough, the governor may apply a stronger reduction.
The scale output is rate-limited so that the command does not switch abruptly
between aggressive and conservative modes.

This risk-conditioned logic should be interpreted as an empirical execution
policy, not as a formal safety filter. The Stage 4 trace review showed that
lower scale is not automatically safer and that different protocols expose
different failure patterns. For this reason, the governor is evaluated through
protocol-split success, balanced robustness, protocol regret, and
failure-mode-aware diagnostics rather than through a formal safety proof.

### 2.4 Current Protagonist: `risk_adapter_v1`

The current paper protagonist is `risk_adapter_v1`, the balanced learned /
risk-conditioned execution governor. Its policy settings are:

- `risk_threshold_3s=0.5`
- `risk_threshold_5s=0.5`
- `hard_threshold_5s=0.7`
- `soft_scale_3s=0.75`
- `soft_scale_5s=0.65`
- `hard_scale_5s=0.60`
- `scale_rate_limit_per_sec=0.5`

In this policy, risk above the short-horizon threshold activates a moderate
scale reduction, risk above the long-horizon threshold activates a stronger
soft reduction, and high long-horizon risk activates the hard reduction. The
rate limit constrains how quickly the command scale can change over time.

`risk_adapter_v1` is selected as the tentative balanced protagonist because it
gives the best cross-protocol balance in the current evaluation. It achieves
`25/30` strict-valid runs in the single-goal mission protocol and `23/30` in
the goal-reissue stress protocol, yielding the best mean valid count
(`24.0/30`), best worst-protocol valid count (`23/30`), and lowest total
regret (`2`) relative to the observed protocol oracles.

The later `risk_adapter_v21` variant remains important, but it should not be
presented as the final method. It ties `risk_adapter_v1` in the single-goal
mission protocol at `25/30`, but it drops to `20/30` under goal-reissue stress.
It is therefore a strong nominal / single-goal variant or ablation, while
`risk_adapter_v1` is the current balanced learned / risk-conditioned
protagonist.

### 2.5 Baselines and Method Variants

The evaluation compares the governor against no-op, fixed, heuristic, and
learned / risk-conditioned variants:

- `original`: unadapted baseline with no command scaling.
- `fixed_s085`: fixed static baseline using a `0.85` scale.
- `windlevel_s085`: wind-level heuristic, best interpreted as the single-goal
  specialist heuristic.
- `fixed_s080`: tuned static scale and current goal-reissue stress specialist
  static frontier.
- `risk_adapter_v1`: balanced learned / risk-conditioned execution governor
  and current paper protagonist.
- `risk_adapter_v2`: single-goal-only note in the complete cross-protocol
  comparison because its goal-reissue stress result is missing.
- `risk_adapter_v21`: strong nominal / single-goal learned variant, but weaker
  under goal-reissue stress.

This role assignment is central to the paper framing. `windlevel_s085` is the
single-goal specialist because it achieves `26/30` strict-valid runs under
`goal_repeat=1`. `fixed_s080` is the stress specialist because it achieves
`24/30` under `goal_repeat=10`. `risk_adapter_v1` does not win each protocol
as the absolute oracle, but it has the best balanced robustness and lowest
protocol regret among complete learned / risk-conditioned methods.

### 2.6 Claim Boundary

The execution governor is an empirical runtime adaptation layer. It is not a
formal safety filter, does not provide a safety guarantee, and does not replace
the planner, payload MPC, or SO3 controller. Its claim is limited to improving
balanced protocol-level behavior under the tested strong-wind evaluation.

The paper also does not claim that learned methods uniformly dominate
heuristic or fixed baselines. The completed evaluation shows strong protocol
specialists: `windlevel_s085` leads the single-goal mission protocol and
`fixed_s080` leads the goal-reissue stress protocol. The appropriate claim is
that `risk_adapter_v1` is the most balanced current learned /
risk-conditioned method by mean valid count, worst-protocol valid count, and
total regret.

Finally, the repeated-run counts are descriptive. They should not be described
as statistically significant unless a separate significance analysis is
performed.

## Notation / Formula Block

Let `u_ref(t)` denote the nominal reference or command produced by the
planner/MPC stack. The execution governor outputs a speed scale `s_v` and an
acceleration scale `s_a`, with:

```text
s_v in (0, 1]
s_a in (0, 1]
```

The executed command is modulated by these scale factors through the
command-adaptation interface:

```text
u_exec(t) = A(u_ref(t), s_v(t), s_a(t))
```

where `A` denotes the existing command-adaptation operation. The
risk-conditioned governor is written abstractly as:

```text
g(r_3(t), r_5(t), c(t)) -> (s_v(t), s_a(t))
```

where `r_3` and `r_5` are short-horizon and long-horizon risk signals, and
`c(t)` is execution context. This notation describes the interface only; it
does not imply formal safety, stability, or optimality guarantees.

## Method Figure Description

Draft Figure 1 caption:

Figure 1. Stack-compatible risk-conditioned execution governance. The
AutoTrans-like stack keeps the payload-aware planner, payload MPC, and SO3
controller unchanged. An external execution governor receives risk-conditioned
signals and execution context, then publishes `speed_scale` and
`acceleration_scale` through the command-adaptation interface. The governor
modulates execution aggressiveness while preserving the underlying planning
and control stack.

## Chinese Explanation

Method 部分应该聚焦 execution-governor interface，而不是写成 controller
replacement，因为当前实现和论文证据都支持“外部调节执行尺度”这个贡献。这样写
可以清楚说明 `speed_scale` / `acceleration_scale` 如何接入现有 AutoTrans-like
stack，同时避免暗示我们改写了 planner、payload MPC 或 SO3 controller。

`risk_adapter_v1` 是 protagonist，因为它不是单个 protocol 的绝对赢家，而是当前
dual-protocol 评价中 balanced robustness 最好的 learned / risk-conditioned
方法：mean、worst-protocol 和 total regret 都最好。这个角色比声称某个方法
“overall best” 更稳妥。

`risk_adapter_v21` 应该作为 ablation / nominal variant，因为它在 single-goal
mission protocol 很强，但 goal-reissue stress 下弱于 `risk_adapter_v1` 和
`fixed_s080`。把它写成 final method 会和当前 protocol-split 结果冲突。

这种 framing 对 IROS/ICRA/RA-L 更安全：它把贡献放在 stack-compatible
execution governance、强 baseline 比较、protocol-split evaluation 和 claim
boundary 上，而不是把论文包装成一个 learned method 全面胜出的故事。

## Claim Audit

| method statement | supported wording | avoid wording | reason |
| --- | --- | --- | --- |
| drop-in governor | The governor is stack-compatible and uses the existing `speed_scale` / `acceleration_scale` interface. | The governor redesigns the AutoTrans stack. | Planner, payload MPC, and SO3 controller remain unchanged in this framing. |
| risk-conditioned | The governor uses short-horizon and long-horizon risk-conditioned signals to choose execution scales. | The governor guarantees safe behavior from risk estimates. | The risk logic is empirical and evaluated by repeated-run outcomes. |
| balanced protagonist | `risk_adapter_v1` is the current balanced learned / risk-conditioned protagonist. | `risk_adapter_v1` is universally best. | It has best mean, worst-protocol count, and total regret, but not every protocol oracle. |
| no formal safety | The method is not a formal safety filter and gives no safety guarantee. | The method is a safety-certified governor. | No formal proof or certification is provided. |
| no low-level controller replacement | The low-level controller remains the SO3 controller. | The method replaces the controller. | The method changes execution scale through command adaptation only. |
| `risk_adapter_v21` not final method | `risk_adapter_v21` is a strong nominal / single-goal variant or ablation. | `risk_adapter_v21` is the final cross-protocol method. | It is weaker under goal-reissue stress and is dominated by `risk_adapter_v1` in the two-protocol comparison. |
