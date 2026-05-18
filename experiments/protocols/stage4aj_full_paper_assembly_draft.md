# Stage 4-AJ Full Paper Assembly Draft

## Executive Summary

This document is the current full paper assembly draft for the reframed Stage 4
paper. It is not final manuscript formatting; it is a coherent IROS/ICRA/RA-L
style system-method draft plan with section text, figure/table placeholders,
and claim boundaries.

The current narrative is:

- `risk_adapter_v1` is the balanced learned / risk-conditioned execution
  governor and tentative paper protagonist.
- `windlevel_s085` is the single-goal mission protocol specialist.
- `fixed_s080` is the goal-reissue stress protocol specialist.
- `risk_adapter_v21` is a strong nominal / single-goal variant or ablation, not
  the final cross-protocol method.

No `risk_adapter_v22` should be created before this full-paper draft is
reviewed. A future variant should only be attempted if later evidence supports
a reusable phase-aware, reference-aware, risk-health-aware, or failure-aware
mechanism.

Stage 4-AK now defines citation slots and reference needs for this assembled
draft:
`experiments/protocols/stage4ak_citation_references_plan.md`. Do not replace
TODO citation placeholders with unverified or fabricated references.

## Paper Title

Recommended title:

Risk-Conditioned Execution Governance for Balanced Robustness in Windy
Suspended-Payload UAV Transport

Alternatives:

1. Protocol-Split Robustness Evaluation of Risk-Conditioned Execution
   Governors for Suspended-Payload UAVs
2. Balanced Execution Governance for Suspended-Payload UAV Transport Under
   Strong Wind

## Abstract

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
balanced robustness analysis under the tested protocols while making no
statistical significance claim, no formal safety guarantee, and no broad
real-world deployment claim.

## Keywords

- UAV suspended-payload transport
- execution governor
- risk-conditioned control
- strong wind robustness
- failure-mode analysis
- protocol-split evaluation

## 1. Introduction

Suspended-payload UAV transport enables aerial systems to move objects that
cannot be rigidly attached to the vehicle, but the suspended load also makes
the task sensitive to coupled vehicle-load dynamics. Under strong wind, small
tracking errors, payload swing, and transient speed changes can interact with
the cable-suspended payload and produce qualitatively different outcomes across
repeated runs. Robust transport in this setting therefore requires not only
feasible motion generation and tracking, but also careful control of how
aggressively the planned motion is executed.

Payload-aware planning, MPC, and low-level control provide the core stack for
generating and tracking feasible trajectories. However, improving these
components alone does not fully address the runtime execution-aggressiveness
problem. A fixed execution setting can be effective for one mission protocol or
wind/task phase while becoming too aggressive, too conservative, or poorly
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
and repeated-command behavior. Because these protocols expose different failure
modes and method rankings, collapsing them into a mixed-protocol aggregate
would obscure the trade-offs that matter for evaluated robustness.

Our completed strong-wind evaluation shows that no current learned variant
dominates both protocols. `windlevel_s085` is the single-goal specialist,
achieving `26/30` strict-valid runs under `goal_repeat=1`, while `fixed_s080`
is the goal-reissue stress specialist, achieving `24/30` strict-valid runs
under `goal_repeat=10`. The learned / risk-conditioned governor
`risk_adapter_v1` is the most balanced current method, with the best mean valid
count (`24.0/30`), best worst-protocol valid count (`23/30`), and lowest total
regret (`2`). By contrast, `risk_adapter_v21` remains a strong nominal /
single-goal variant, but it is weaker under stress and should not be framed as
the overall best method.

This paper makes four contributions:

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

## 2. Related Work Skeleton

### 2.1 Suspended-Payload UAV Transport and Control

This subsection should position the work relative to suspended-payload UAV
planning, payload-aware MPC, geometric control, and integrated aerial transport
systems. It should describe why payload swing, wind disturbance, and tracking
coupling make the task harder than rigid-body waypoint flight.

Citation placeholders:

- [TODO: AutoTrans]
- [TODO: suspended-payload UAV planning]
- [TODO: payload-aware MPC]
- [TODO: SO3 / geometric quadrotor control]

Avoid claiming that prior planner/controller work is insufficient in a general
sense. The narrower claim is that even strong planner/MPC/controller stacks can
remain sensitive to runtime execution aggressiveness under strong wind and
different mission protocols.

### 2.2 Runtime Governors / Reference Governors / Safety Filters

This subsection should connect the proposed execution governor to runtime
governance ideas such as reference governors, action governors, command
filters, and safety filters. The distinction is that this work uses an
empirical `speed_scale` / `acceleration_scale` execution interface rather than
a certified constraint-enforcing controller.

Citation placeholders:

- [TODO: reference governor]
- [TODO: runtime safety filter]
- [TODO: action governor]
- [TODO: command filtering for robotics]

Claim boundary: do not describe the proposed governor as a formal safety
filter, because no formal invariance, stability, or certification result is
provided.

### 2.3 Learning-Enhanced Aerial Robustness

This subsection should discuss learned risk prediction, learning-enhanced
control, disturbance-aware adaptation, and data-driven robustness in aerial
robotics. The paper should emphasize that learned risk signals are used to
modulate execution aggressiveness through a stack-compatible interface.

Citation placeholders:

- [TODO: learning-enhanced UAV control]
- [TODO: learned disturbance or risk prediction]
- [TODO: data-driven robustness in aerial robotics]

Avoid suggesting that learning uniformly outperforms heuristics. The current
result is that `risk_adapter_v1` is the most balanced learned /
risk-conditioned method in the tested protocol split.

### 2.4 Benchmarking, Stress Testing, and Failure Analysis

This subsection should frame the protocol split and failure-mode analysis as
part of evaluation rigor. It should connect to robotics benchmarking, repeated
trials, stress testing, and failure taxonomy / diagnostic analysis.

Citation placeholders:

- [TODO: robotics benchmarking]
- [TODO: stress testing for autonomous systems]
- [TODO: failure analysis / taxonomy]

The paper's contribution is not only a governor, but also an evaluation
structure showing that single-protocol success can hide specialist trade-offs
and heterogeneous failure modes.

## 3. Method

### 3.1 System Stack and Problem Setting

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
the nominal command is executed.

### 3.2 Execution-Governor Interface

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

Figure placeholder:

```text
Figure 1. Stack-compatible risk-conditioned execution governance.
Show the AutoTrans-like planner / payload MPC / SO3 controller stack, the
external learned risk-conditioned execution governor, the `speed_scale` /
`acceleration_scale` interface, risk input, and command adaptation output.
```

### 3.3 Risk-Conditioned Governor

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

### 3.4 Current Protagonist: `risk_adapter_v1`

The current paper protagonist is `risk_adapter_v1`, the balanced learned /
risk-conditioned execution governor. Its policy settings are:

- `risk_threshold_3s=0.5`
- `risk_threshold_5s=0.5`
- `hard_threshold_5s=0.7`
- `soft_scale_3s=0.75`
- `soft_scale_5s=0.65`
- `hard_scale_5s=0.60`
- `scale_rate_limit_per_sec=0.5`

`risk_adapter_v1` is selected as the tentative balanced protagonist because it
gives the best cross-protocol balance in the current evaluation. It achieves
`25/30` strict-valid runs in the single-goal mission protocol and `23/30` in
the goal-reissue stress protocol, yielding the best mean valid count
(`24.0/30`), best worst-protocol valid count (`23/30`), and lowest total
regret (`2`) relative to the observed protocol oracles.

The later `risk_adapter_v21` variant remains important, but it should not be
presented as the final method. It ties `risk_adapter_v1` in the single-goal
mission protocol at `25/30`, but it drops to `20/30` under goal-reissue stress.
It is therefore a strong nominal / single-goal variant or ablation.

### 3.5 Baselines and Method Variants

The evaluation compares the governor against no-op, fixed, heuristic, and
learned / risk-conditioned variants:

- `original`: unadapted baseline with no command scaling.
- `fixed_s085`: fixed static baseline using a `0.85` scale.
- `windlevel_s085`: wind-level heuristic and single-goal specialist.
- `fixed_s080`: tuned static scale and goal-reissue stress specialist.
- `risk_adapter_v1`: balanced learned / risk-conditioned governor.
- `risk_adapter_v2`: single-goal-only note in the complete cross-protocol
  comparison because its goal-reissue stress result is missing.
- `risk_adapter_v21`: strong nominal / single-goal learned variant, but weaker
  under goal-reissue stress.

### 3.6 Notation Block

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

### 3.7 Claim Boundary

The execution governor is an empirical runtime adaptation layer. It is not a
formal safety filter, does not provide a safety guarantee, and does not replace
the planner, payload MPC, or SO3 controller. Its claim is limited to improving
balanced protocol-level behavior under the tested strong-wind evaluation.

The paper also does not claim that learned methods uniformly dominate heuristic
or fixed baselines. The completed evaluation shows strong protocol specialists:
`windlevel_s085` leads the single-goal mission protocol and `fixed_s080` leads
the goal-reissue stress protocol.

## 4. Experimental Setup

### 4.1 Simulator and System Stack

The evaluation uses an AutoTrans-like ROS1 simulation stack for suspended
payload transport. The stack includes a payload-aware planner, a payload MPC,
and an SO3 controller. The proposed governor is evaluated as an external
execution layer that publishes command-adaptation scales without modifying the
core planner/MPC/controller implementation.

### 4.2 Strong Wind Setting and Task

All Stage 4 paper-facing comparisons use the strong-wind setting. The task is
to transport a cable-suspended payload to a target while avoiding invalid
tracking, swing, speed, target-error, or log-health outcomes. The current paper
uses Trial 4, Trial 5, and Trial 6 as strong-wind task instances.

### 4.3 Protocol Definitions

The single-goal mission protocol uses `goal_repeat=1`. It tests one commanded
mission and is closest to nominal single-goal execution.

The goal-reissue stress protocol uses `goal_repeat=10`. It repeatedly
republishes the same goal and stresses reference-update, post-arrival, and
repeated-command behavior.

Figure placeholder:

```text
Figure 2. Dual-protocol evaluation design.
Show `goal_repeat=1` as the single-goal mission protocol and `goal_repeat=10`
as the goal-reissue stress protocol. Explain why they test different execution
regimes.
```

### 4.4 Metrics and Repeated Runs

The paper-facing metric is strict-valid count over repeated runs. Strict-valid
evaluation uses `label_strict_invalid` and associated target-error, speed,
swing, NaN/log-health, and manual diagnostic conditions where available.

Each method is evaluated over Trial 4, Trial 5, and Trial 6 with 10 repeats per
trial in each completed protocol cell, yielding `30` runs per complete method
per protocol.

### 4.5 Method List

The complete cross-protocol balanced table includes:

- `original`
- `fixed_s085`
- `windlevel_s085`
- `fixed_s080`
- `risk_adapter_v1`
- `risk_adapter_v21`

The single-goal protocol also includes `risk_adapter_v2`, but its
goal-reissue stress result is missing. It should therefore be handled as an
appendix or single-protocol-only note rather than as part of the complete
balanced ranking.

### 4.6 Diagnostic Logging

Diagnostic logging supports failure-mode-aware analysis. The paper should use
invalid-only failure groups for failure-analysis figures and should treat
`failure_group` as diagnostic, not as exact physical root-cause proof.
Representative traces are used as qualitative case studies for mechanism
interpretation.

## 5. Results

### 5.1 Protocol-Split Success Rates

The strong-wind evaluation separates single-goal mission execution from
goal-reissue stress. We therefore report strict-valid counts separately for the
single-goal mission protocol (`goal_repeat=1`) and the goal-reissue stress
protocol (`goal_repeat=10`), rather than collapsing the two settings into a
mixed aggregate.

In the single-goal mission protocol, the strongest method in the evaluated set
is the heuristic `windlevel_s085`, which achieves `26/30` strict-valid runs.
The learned / risk-conditioned methods `risk_adapter_v1` and
`risk_adapter_v21` are both competitive in this setting, each achieving
`25/30` strict-valid runs. `fixed_s085` achieves `22/30`, while `original`,
`fixed_s080`, and `risk_adapter_v2` each achieve `21/30`.

In the goal-reissue stress protocol, the ranking changes. The tuned static
baseline `fixed_s080` is strongest with `24/30` strict-valid runs.
`risk_adapter_v1` follows with `23/30`, while `risk_adapter_v21` drops to
`20/30`. The remaining baselines achieve `18/30` for `original`, `18/30` for
`fixed_s085`, and `16/30` for `windlevel_s085`.

### 5.2 Balanced Robustness and Protocol Regret

Balanced robustness is evaluated using the complete cross-protocol matrix. The
protocol oracles are the best observed method in each protocol:
`windlevel_s085` with `26/30` in the single-goal mission protocol and
`fixed_s080` with `24/30` in the goal-reissue stress protocol.

Under this view, `risk_adapter_v1` has the strongest balanced performance. It
achieves a mean valid count of `24.0/30`, the best worst-protocol count of
`23/30`, and the lowest total regret of `2`. This is the main reason for
centering `risk_adapter_v1` as the paper's balanced learned /
risk-conditioned execution governor.

The observed Pareto frontier contains `windlevel_s085`, `fixed_s080`, and
`risk_adapter_v1`. `risk_adapter_v21` is not on the frontier because it has the
same single-goal count as `risk_adapter_v1` (`25/30`) but a lower stress count
(`20/30` versus `23/30`).

Table placeholder:

| method | single-goal strict-valid | stress strict-valid | mean valid | worst-protocol valid | total regret | role |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `original` | `21/30` | `18/30` | `19.5/30` | `18/30` | `11` | unadapted baseline |
| `fixed_s085` | `22/30` | `18/30` | `20.0/30` | `18/30` | `10` | fixed static baseline |
| `windlevel_s085` | `26/30` | `16/30` | `21.0/30` | `16/30` | `8` | single-goal specialist heuristic |
| `fixed_s080` | `21/30` | `24/30` | `22.5/30` | `21/30` | `5` | goal-reissue stress specialist static frontier |
| `risk_adapter_v1` | `25/30` | `23/30` | `24.0/30` | `23/30` | `2` | balanced learned / risk-conditioned governor |
| `risk_adapter_v21` | `25/30` | `20/30` | `22.5/30` | `20/30` | `5` | strong nominal / single-goal learned variant |

```text
Table 1. Protocol-split strict-valid success and balanced robustness metrics
under strong wind. `risk_adapter_v1` has the best mean valid count, best
worst-protocol count, and lowest total regret, while `windlevel_s085` and
`fixed_s080` specialize to different protocols.
```

### 5.3 Failure-Mode-Aware Diagnosis

Protocol-split success counts explain which methods are stronger, but they do
not explain how invalid runs occur. We therefore use invalid-only failure
groups as a diagnostic view. These labels should be read as failure-analysis
categories, not exact physical root-cause proof; the paper-facing success
metric remains strict-valid count.

In the single-goal protocol, the invalid runs for `windlevel_s085` are
concentrated in `state_task_upstream=4`. For `risk_adapter_v1`, the invalid
groups are `command_control_upstream=2` and `state_task_upstream=3`. For
`risk_adapter_v21`, they are `command_control_upstream=1` and
`state_task_upstream=4`.

In the goal-reissue stress protocol, the specialist `fixed_s080` has
`command_control_upstream=4` and `state_task_upstream=2` invalid groups.
`risk_adapter_v1` has `command_control_upstream=3`,
`planner_reference_upstream=1`, and `state_task_upstream=3`. By contrast,
`risk_adapter_v21` has `command_control_upstream=5`,
`planner_reference_upstream=3`, and `state_task_upstream=2`.

```text
Figure 5. Invalid-only failure-group distribution.
Use the invalid-only stacked bar, not the all-run view. Emphasize that
`failure_group` is diagnostic and does not prove exact root cause.
```

### 5.4 Representative Trace Analysis

Representative traces add a case-study view of the same trade-offs. In Trial 4
under goal-reissue stress, several `risk_adapter_v21` failures occur before
arrival rather than only after post-arrival goal republishes. These traces
point to early pre-arrival vulnerability and risk availability or timing
issues, not merely a goal-reissue artifact.

Trial 6 under the single-goal protocol shows a different pattern. A
`risk_adapter_v21` invalid run reaches arrival first and then diverges later
under `goal_repeat=1`, indicating delayed post-arrival divergence even without
goal reissue. The same trace set also shows that lower command scale is not
automatically safer.

```text
Figure 6. Representative trace case studies.
Use Trial 4 goal-reissue stress traces for `risk_adapter_v21` failure versus
`fixed_s080` / `risk_adapter_v1` successes, and Trial 6 single-goal traces for
the learned-governor bottleneck versus `windlevel_s085` / `fixed_s080`.
```

### 5.5 Summary of Findings

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

## 6. Discussion and Limitations

### 6.1 Why Protocol Split Matters

The main empirical lesson from Stage 4 is that robustness depends on the
mission protocol. The single-goal mission protocol and the goal-reissue stress
protocol expose different method rankings because they stress different parts
of the execution stack. A single goal primarily tests nominal goal-directed
transport under strong wind, whereas repeated goal publication stresses
reference-update behavior, post-arrival holding, and repeated-command behavior.

This distinction changes the interpretation of the results. `windlevel_s085`
is the single-goal specialist, while `fixed_s080` is the stress specialist. If
the two protocols were collapsed into one mixed aggregate, this specialist
structure would be obscured.

### 6.2 Why Strong Simple Baselines Matter

The strong performance of simple baselines is not a weakness of the paper. It
is evidence that execution governance is a difficult and practically relevant
problem. A fixed or heuristic scale can be well matched to a specific protocol,
wind condition, and task phase.

These baselines make the balanced robustness claim more meaningful:
`risk_adapter_v1` is not presented as winning every individual protocol, but as
maintaining high performance across protocols where different simple baselines
specialize.

### 6.3 Balanced Robustness as a Deployment-Oriented Criterion

Within the tested protocols, balanced robustness is more informative than
single-protocol winning. The Stage 4 balanced metrics operationalize this idea
through mean valid count, worst-protocol valid count, and total regret relative
to the observed protocol oracles.

`risk_adapter_v1` is the current balanced protagonist under this criterion. It
achieves the best mean valid count (`24.0/30`), the best worst-protocol valid
count (`23/30`), and the lowest total regret (`2`). This claim remains
descriptive and bounded; it does not imply statistical significance, universal
optimality, or safety by construction.

### 6.4 Failure-Mode-Aware Interpretation

The failure analysis adds a second layer of interpretation beyond strict-valid
counts. The invalid-only failure groups separate failures into diagnostic
families such as `command_control_upstream`,
`planner_reference_upstream`, and `state_task_upstream`. These labels guide
interpretation but do not prove physical root cause.

Representative traces support this diagnostic interpretation. Trial 4
goal-reissue stress failures for `risk_adapter_v21` include early pre-arrival
vulnerability and risk availability or timing issues, while Trial 6 single-goal
traces show that lower scale is not automatically safer.

### 6.5 Why `risk_adapter_v22` Is Not Introduced

The current evidence does not justify adding `risk_adapter_v22` as the next
paper method. Stage 4-AA3 did not reveal a simple threshold correction that
would plausibly solve both the Trial 4 stress weakness and the Trial 6
single-goal bottleneck.

A future governor should only be attempted if later evidence identifies a
generic mechanism, such as phase-aware scaling, reference-health-aware fallback,
risk-confidence fallback, or command/state-health-aware intervention. Until
then, the paper should proceed with the `risk_adapter_v1`-centered balanced
robustness story.

### 6.6 Limitations

The current evidence is simulation-only. The paper should not claim real-world
deployment performance, hardware robustness, or transfer to unmodeled vehicle,
payload, wind, or sensing conditions.

The execution governor is empirical and does not provide a formal safety
guarantee. It modulates `speed_scale` and `acceleration_scale` through the
command-adaptation interface, but it is not a certified safety filter and does
not replace feasibility checking, payload MPC, or low-level SO3 control.

The repeated-run counts are descriptive and do not support a statistical
significance claim. The evaluated task set is also limited to Trial 4, Trial 5,
and Trial 6 under the current strong-wind setting.

The failure groups are diagnostic rather than definitive root-cause labels.
The risk score source, training set, calibration behavior, and online
confidence properties need clearer future documentation. `risk_adapter_v2` is
not included in the complete balanced robustness table because its
goal-reissue stress result is missing.

### 6.7 Future Work

Future method work should be driven by representative traces rather than by
single-trial threshold tuning. A phase-aware governor could distinguish
pre-arrival, arrival, post-arrival hold, and repeated-goal phases before
selecting scale behavior.

Risk availability and confidence should be modeled explicitly. Future work
should also test risk calibration, delayed-risk ablations, shuffled-risk
ablations, horizon-specific ablations, and risk-disabled versions of the same
governor.

The command-adaptation interface should be ablated by channel. Speed-only,
acceleration-only, and combined `speed_scale` / `acceleration_scale` policies
would clarify whether the observed gains come from one channel, both channels,
or their interaction.

Broader evaluation should include additional wind profiles, payload masses,
cable lengths, and mission geometries. Hardware-in-the-loop or real hardware
validation would be needed before making claims about real-world deployment.

## 7. Conclusion Draft

This paper studies risk-conditioned execution governance for suspended-payload
UAV transport under strong wind. The proposed governor adapts runtime execution
through the existing `speed_scale` and `acceleration_scale` interface while
leaving the planner, payload MPC, and SO3 controller unchanged.

The protocol-split evaluation shows that simple baselines are strong
specialists: `windlevel_s085` leads the single-goal mission protocol, and
`fixed_s080` leads the goal-reissue stress protocol. Across the completed
two-protocol comparison, `risk_adapter_v1` provides the best balanced learned /
risk-conditioned performance, with the best mean valid count, best
worst-protocol count, and lowest total regret. Failure-mode analysis and
representative traces further show why aggregate success alone is insufficient
for interpreting robustness.

The current evidence supports a bounded claim: protocol-split and
failure-aware evaluation can identify a balanced risk-conditioned execution
governor under the tested strong-wind protocols. It does not establish a formal
safety guarantee, statistical significance, real-world deployment robustness,
or learned-method uniform domination.

## Main Figure / Table Checklist

| item | status / intended content |
| --- | --- |
| Figure 1 system architecture | Show AutoTrans-like planner / payload MPC / SO3 controller stack plus external execution governor and `speed_scale` / `acceleration_scale` interface. |
| Figure 2 protocol split | Show single-goal mission protocol (`goal_repeat=1`) and goal-reissue stress protocol (`goal_repeat=10`). |
| Table 1 protocol-split success + balanced robustness | Use the main table in Section 5.2. |
| Figure 3 Pareto frontier | Plot single-goal valid count versus stress valid count; highlight `windlevel_s085`, `fixed_s080`, and `risk_adapter_v1`. |
| Figure 4 protocol regret | Show single-goal regret, stress regret, and total regret relative to observed protocol oracles. |
| Figure 5 invalid-only failure groups | Use invalid-only failure groups, not all-run accounting. |
| Figure 6 representative traces | Use Trial 4 stress and Trial 6 single-goal representative trace cases. |

## Appendix / Supplementary Plan

- Full per-run tables.
- Full protocol-split tables.
- Full failure-mode tables, including all-run and invalid-only views.
- Representative trace index.
- Additional trace plots beyond the main case studies.
- Launch settings and protocol definitions.
- `risk_adapter_v1` parameters.
- Claim audit and wording boundary table.
- Duplicate CSV audit notes if needed.
- Single-goal-only `risk_adapter_v2` note.

## Master Claim Audit

| claim | allowed wording | forbidden wording | supporting section/table/figure |
| --- | --- | --- | --- |
| `risk_adapter_v1` most balanced | `risk_adapter_v1` is the most balanced current learned / risk-conditioned method under the tested protocols. | `risk_adapter_v1` is universally best. | Abstract, Section 5, Table 1, Figure 3, Figure 4 |
| `windlevel_s085` single-goal specialist | `windlevel_s085` is the single-goal specialist with `26/30` strict-valid runs. | `windlevel_s085` is the best method overall. | Section 5, Table 1, Figure 3 |
| `fixed_s080` stress specialist | `fixed_s080` is the goal-reissue stress specialist with `24/30` strict-valid runs. | `fixed_s080` solves robust transport. | Section 5, Table 1, Figure 3 |
| no learned uniform domination | No current learned method uniformly dominates the heuristic/static specialists. | Learned governors dominate all baselines. | Section 5, Section 6, Table 1 |
| no safety guarantee | The governor is empirical and is not a formal safety filter. | The governor guarantees safety. | Method claim boundary, Limitations |
| no statistical significance | The repeated-run counts are descriptive under the tested protocols. | The gains are statistically significant. | Abstract, Results, Limitations |
| failure labels diagnostic only | Failure groups guide interpretation but do not prove exact root cause. | Failure groups prove root cause. | Section 5.3, Section 6.4, Figure 5 |
| simulation-only limitation | The current evidence is simulation-only and does not establish real-world deployment performance. | The method is deployable in real wind based on these results. | Limitations |

## Paper Readiness Checklist

- Required citations are still missing and should be filled before manuscript
  conversion.
- Final figure generation is still needed for Figures 1-6.
- Final table formatting is still needed, likely with `booktabs` style for a
  conference paper.
- Possible ablations remain optional, including speed-only /
  acceleration-only, delayed-risk, shuffled-risk, and calibration checks.
- Video or supplementary material is not yet prepared.
- A final claim audit should be performed before submission.
- No `risk_adapter_v22` should be introduced unless mechanism-driven evidence
  is later added.

## Chinese Summary

这个 full paper draft 已经 coherent，因为它把 AF 的 Abstract / Introduction、AG
的 Method、AH 的 Results、AI 的 Discussion / Limitations 串成同一条证据链：
stack-compatible risk-conditioned execution governor，dual-protocol evaluation，
balanced robustness / regret，再到 failure-mode-aware diagnosis。

`risk_adapter_v1` 是 protagonist，因为它不是某一个 protocol 的绝对赢家，而是当前
complete cross-protocol matrix 中 mean valid count、worst-protocol valid count
和 total regret 都最好的 learned / risk-conditioned governor。

`risk_adapter_v21` 不是 final method，因为它虽然在 single-goal protocol 很强，
但 goal-reissue stress 下弱于 `risk_adapter_v1`，并且在 two-protocol plane 中被
`risk_adapter_v1` dominate。把它写成 final winner 会和当前数据冲突。

这种 draft 对 IROS/ICRA/RA-L 更安全：它承认 `windlevel_s085` 和 `fixed_s080`
这些 strong specialist baseline，避免 mixed-protocol aggregate 和 learned
uniform domination 叙事，同时把贡献放在 governor interface、protocol-split
evaluation、balanced robustness 和 failure-aware interpretation 上。
