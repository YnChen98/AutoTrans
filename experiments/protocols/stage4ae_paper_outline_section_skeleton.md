# Stage 4-AE Paper Outline Section Skeleton

## Executive Summary

This document is the current paper-level outline after Stage 4-AD froze the
main figure/table plan.

Target style: IROS/ICRA/RA-L system-method paper. The paper should read as a
robotics system and method contribution, not as a raw experiment log or a
single-variant tuning story.

The tentative protagonist is `risk_adapter_v1` as the balanced learned /
risk-conditioned execution governor. `risk_adapter_v21` should be presented as
an ablation or strong nominal / single-goal variant, not as the final method.

No `risk_adapter_v22` should be created before the paper skeleton, abstract,
Introduction, and claim audit are written and reviewed. The current evidence
supports a balanced-governor paper, not another trial-specific policy patch.

## Candidate Titles

1. Risk-Conditioned Execution Governance for Wind-Robust Suspended-Payload UAV
   Transport
2. Balanced Robustness Evaluation of Risk-Conditioned Execution Governors for
   Suspended-Payload UAVs
3. Protocol-Split Robustness for Suspended-Payload UAV Transport in Strong
   Wind
4. Learning a Drop-In Execution Governor for Suspended-Payload UAV Transport
   Under Strong Wind
5. Risk-Conditioned Speed and Acceleration Governance for Robust
   Suspended-Payload UAV Transport
6. From Protocol Specialists to Balanced Execution Governance in
   Suspended-Payload UAV Transport

## Core Thesis

Suspended-payload UAV transport under strong wind is sensitive to execution
aggressiveness and to the mission protocol used during evaluation. This paper
shows that a drop-in execution governor can improve deployment robustness by
adapting speed and acceleration commands without rewriting the planner, MPC, or
low-level controller. Strong heuristic/static baselines specialize to different
protocols: `windlevel_s085` is strongest in the single-goal mission protocol,
whereas `fixed_s080` is strongest in the goal-reissue stress protocol. Among
the currently evaluated learned / risk-conditioned methods, `risk_adapter_v1`
provides the best balanced robustness, while failure-mode analysis explains why
no single method uniformly dominates all protocols.

## Abstract Skeleton

Draft abstract:

Suspended-payload UAV transport in strong wind is difficult because small
changes in execution aggressiveness can alter tracking, swing, and arrival
behavior. Existing planner and controller improvements are important, but they
do not by themselves address runtime decisions about how aggressively a
planned motion should be executed under changing risk. We study a drop-in
risk-conditioned execution governor that adapts command speed and acceleration
scales through the existing command-adaptation interface, leaving the
AutoTrans-like planner, payload MPC, and SO3 controller stack intact. To avoid
overstating single-protocol performance, we evaluate under a protocol split:
a single-goal mission protocol (`goal_repeat=1`) and a goal-reissue stress
protocol (`goal_repeat=10`). In the completed strong-wind evaluation,
`windlevel_s085` is the single-goal specialist with `26/30` strict-valid runs,
whereas `fixed_s080` is the goal-reissue stress specialist with `24/30`
strict-valid runs. The learned governor `risk_adapter_v1` is the most balanced
current learned / risk-conditioned method, with the best mean valid count
(`24.0/30`), best worst-protocol valid count (`23/30`), and lowest total
regret (`2`) relative to the protocol oracles. Invalid-only failure groups and
representative traces further show that aggregate success hides distinct
failure modes, including command/control divergence, reference-related issues,
and state/task failures. These results support protocol-split and
failure-aware evaluation of learned execution governors, while not claiming
statistical significance, formal safety guarantees, or uniform learned-method
dominance over strong heuristic/static baselines.

## Introduction Skeleton

Paragraph 1: motivation. Suspended-payload UAV transport is useful for aerial
delivery, construction support, and operation in environments where direct
rigid grasping is impractical. The suspended load introduces coupled UAV-load
dynamics, and strong wind further stresses tracking, swing, and arrival
behavior.

Paragraph 2: limitation of only improving planner/controller. Payload-aware
planning and MPC can produce feasible references and stabilize the vehicle-load
system, but deployment robustness also depends on how aggressively the planned
motion is executed at runtime. A fixed execution policy can be too aggressive
in some wind/task phases and too conservative in others.

Paragraph 3: execution aggressiveness as runtime governance. This paper treats
speed and acceleration scaling as an execution-governance problem. A governor
can be attached through `speed_scale` and `acceleration_scale` without
rewriting the planner, payload MPC, or SO3 controller.

Paragraph 4: protocol split. Robustness conclusions depend on evaluation
protocol. The single-goal mission protocol (`goal_repeat=1`) tests one
commanded mission, while the goal-reissue stress protocol (`goal_repeat=10`)
stresses repeated goal publication, reference updates, and post-arrival
behavior. These protocols should not be collapsed into a single aggregate.

Paragraph 5: main empirical finding. Strong baselines specialize:
`windlevel_s085` leads the single-goal mission protocol and `fixed_s080` leads
the goal-reissue stress protocol. `risk_adapter_v1` does not win every
protocol, but it provides the best current balance by mean valid count,
worst-protocol valid count, and total regret.

Paragraph 6: contributions. Close the Introduction by stating the drop-in
governor, dual-protocol evaluation, balanced robustness / regret analysis, and
failure-mode-aware diagnostic framework.

## Contribution Bullets

- We introduce a drop-in risk-conditioned execution governor for
  suspended-payload UAV transport that adapts `speed_scale` and
  `acceleration_scale` through an external command-adaptation interface,
  without replacing the planner, payload MPC, or SO3 controller.
- We define a dual-protocol strong-wind evaluation that separates the
  single-goal mission protocol (`goal_repeat=1`) from the goal-reissue stress
  protocol (`goal_repeat=10`), avoiding a misleading mixed-protocol aggregate.
- We report balanced robustness and protocol regret metrics that compare
  learned governors against strong heuristic/static protocol specialists and
  identify `risk_adapter_v1` as the most balanced current learned /
  risk-conditioned method.
- We provide a failure-mode-aware diagnostic workflow using invalid-only
  failure groups and representative traces to explain why aggregate success
  alone is insufficient for interpreting robustness.

## Related Work Skeleton

### Suspended-Payload UAV Transport And Control

Emphasize: suspended payload transport creates coupled vehicle-load dynamics,
payload swing, and tracking constraints that motivate payload-aware planning
and control. Position this paper as complementary to planner/MPC/controller
development because it studies execution governance on top of an existing
AutoTrans-like stack.

Avoid: claiming that existing payload-control work is inadequate in general, or
that this paper replaces payload-aware planning and control.

### Runtime Safety / Reference Governor / Action Governor Ideas

Emphasize: runtime governors, reference governors, and action-scaling ideas
share the principle that execution commands can be modified online to respect
operational constraints or risk. The paper should connect to this conceptual
line while being clear that the current governor is empirical and
risk-conditioned.

Avoid: calling `risk_adapter_v1` a formal safety filter, control barrier
function, or certified reference governor.

### Learning-Enhanced UAV Robustness

Emphasize: learning can provide risk estimates or adaptive policies that help
handle disturbances and operating-condition changes. The key distinction here
is the execution-layer interface and the comparison against strong simple
baselines under protocol-split evaluation.

Avoid: claiming learned methods uniformly outperform classical or heuristic
methods. The current results show strong protocol specialists.

### Benchmarking, Stress Testing, And Failure Analysis

Emphasize: robotics robustness claims depend on evaluation protocol, repeated
runs, strict metrics, and failure analysis. This paper contributes a
protocol-split and failure-aware view of strong-wind suspended-payload
transport.

Avoid: presenting diagnostic labels as perfect root causes or using failure
taxonomy in place of strict-valid success metrics.

## Method Section Skeleton

### System Stack And Execution-Governor Interface

Describe the AutoTrans-like stack as planner, payload MPC, and SO3 controller.
Introduce the governor as an external module that publishes command adaptation
signals through `speed_scale` and `acceleration_scale`.

### Risk-Conditioned Governor Formulation

Define the governor at a high level: inputs are risk-related observations or
risk scores; outputs are execution scale commands. Keep the formulation
interface-level unless the final paper includes full model/training detail.

### Speed/Acceleration Scaling Outputs

Explain how lowering `speed_scale` and `acceleration_scale` changes execution
aggressiveness. State that lower scale is not automatically safer, as shown by
Stage 4-AA3 trace review, so the governor must be evaluated empirically.

### Current Protagonist: `risk_adapter_v1`

Present `risk_adapter_v1` as the current balanced learned /
risk-conditioned governor. Record its paper-facing policy settings in the
Method or Appendix:

- `soft_scale_3s=0.75`
- `soft_scale_5s=0.65`
- `hard_scale_5s=0.60`
- `risk_threshold_3s=0.5`
- `risk_threshold_5s=0.5`
- `hard_threshold_5s=0.7`
- `scale_rate_limit_per_sec=0.5`

### Method Variants And Baselines

Include `original`, `fixed_s085`, `windlevel_s085`, `fixed_s080`,
`risk_adapter_v1`, `risk_adapter_v21`, and the single-goal-only note for
`risk_adapter_v2`. Present `risk_adapter_v21` as a strong nominal /
single-goal variant or ablation, not as the final method.

### Claim Boundary

State explicitly that the governor is not a formal safety filter, does not
replace the low-level controller, and does not provide a safety guarantee. It
is an empirical execution-governance layer evaluated under repeated
strong-wind protocols.

## Experimental Setup Skeleton

- Simulator / stack: AutoTrans-like suspended-payload UAV stack with planner,
  payload MPC, SO3 controller, and command-adaptation interface.
- Strong wind setting: use the established strong-wind benchmark setting.
- Suspended payload task: evaluate transport to target goals with payload and
  UAV state logging.
- Trials: Trial 4, Trial 5, and Trial 6.
- Metric: strict-valid count using the paper-facing strict-valid /
  `label_strict_invalid` metric, not raw `valid_run_suggested` alone.
- Protocols:
  - single-goal mission protocol: `goal_repeat=1`
  - goal-reissue stress protocol: `goal_repeat=10`
- Method list: `original`, `fixed_s085`, `windlevel_s085`, `fixed_s080`,
  `risk_adapter_v1`, `risk_adapter_v21`; note `risk_adapter_v2` as
  single-goal-only in the complete cross-protocol comparison.
- Repeated-run design: 10 repeats per Trial 4/5/6 cell, giving `30` runs per
  method per completed protocol.
- Diagnostic logging: record command scales, risk scores when available,
  arrival timing, NaN/divergence timing, failure groups, and representative
  traces.

## Results Section Skeleton

The Results section should follow the Stage 4-AD figure/table plan.

### Table 1: Protocol-Split Success And Balanced Robustness

Open with the dual-protocol success table. Report single-goal strict-valid,
goal-reissue stress strict-valid, mean valid count, worst-protocol valid count,
total regret, and method role.

### Figure 3: Pareto Frontier

Use the balanced robustness / Pareto plot with single-goal valid count on the
x-axis and stress valid count on the y-axis. Highlight `windlevel_s085`,
`fixed_s080`, and `risk_adapter_v1` as the observed Pareto frontier.

### Figure 4: Protocol Regret

Use the protocol regret bar chart to show single-goal regret, stress regret,
and total regret relative to the observed protocol oracles. Emphasize
`risk_adapter_v1` with total regret `2`.

### Figure 5: Invalid-Only Failure Groups

Use the invalid-only failure group stacked bar from Stage 4-Z2. Discuss
diagnostic patterns such as `command_control_upstream`,
`planner_reference_upstream`, and `state_task_upstream`.

### Figure 6: Representative Trace Case Study

Use Stage 4-AA2 / Stage 4-AA3 representative traces. Compare Trial 4
goal-reissue stress `risk_adapter_v21` failures against `fixed_s080` /
`risk_adapter_v1` successes, and Trial 6 single-goal bottlenecks against
`windlevel_s085` / `fixed_s080`.

## Paper-Ready Results Paragraph Draft

In the single-goal mission protocol (`goal_repeat=1`), the strongest completed
method was the wind-level heuristic `windlevel_s085`, which achieved `26/30`
strict-valid runs across Trial 4, Trial 5, and Trial 6. The learned /
risk-conditioned variants `risk_adapter_v1` and `risk_adapter_v21` each
achieved `25/30`, followed by `fixed_s085` at `22/30` and `original`,
`fixed_s080`, and `risk_adapter_v2` at `21/30`. These results show that a
simple topic-based wind-level heuristic remains a strong single-goal
specialist and that the learned variants are competitive but do not dominate
the single-goal protocol.

The goal-reissue stress protocol (`goal_repeat=10`) produced a different
ranking. The tuned static scale `fixed_s080` achieved the highest stress
strict-valid count, `24/30`, followed by `risk_adapter_v1` at `23/30`.
`risk_adapter_v21` achieved `20/30`, above `original` and `fixed_s085`
(`18/30` each) and `windlevel_s085` (`16/30`), but below both `fixed_s080` and
`risk_adapter_v1`. This reversal supports the protocol-split framing: the
single-goal leader is not the stress-protocol leader, and results from one
protocol should not be treated as generic mission robustness.

Balanced robustness and protocol regret identify `risk_adapter_v1` as the most
balanced current learned / risk-conditioned method. Relative to the observed
protocol oracles, `windlevel_s085` at `26/30` single-goal and `fixed_s080` at
`24/30` stress, `risk_adapter_v1` has the best mean valid count (`24.0/30`),
best worst-protocol valid count (`23/30`), and lowest total regret (`2`).
`risk_adapter_v21` ties `risk_adapter_v1` in single-goal success but is lower
under stress, so it is dominated by `risk_adapter_v1` in the current
two-protocol comparison.

The invalid-only failure analysis provides context for these rankings. Rather
than treating every invalid run as the same type of failure, the Stage 4-Z2
assets separate diagnostic groups such as `command_control_upstream`,
`planner_reference_upstream`, and `state_task_upstream`. These labels are not
root-cause proof, but they show that aggregate strict-valid counts hide
different failure patterns across methods and protocols.

Representative traces further support the claim boundary. Stage 4-AA3 review
showed that some Trial 4 goal-reissue stress `risk_adapter_v21` failures occur
early and before arrival, while a Trial 6 single-goal `risk_adapter_v21`
failure appears as post-arrival delayed divergence rather than a
goal-reissue-only artifact. The traces also show that lower scale is not
automatically safer. These observations motivate the current paper framing:
`risk_adapter_v1` is the balanced learned / risk-conditioned protagonist, while
`windlevel_s085` and `fixed_s080` should be treated as strong protocol
specialists.

## Discussion Section Skeleton

### Strong Simple Baselines Matter

Discuss why `windlevel_s085` and `fixed_s080` raise the evidence standard. The
paper should not compare learned methods only against `original`; it should
show where learned governance adds balanced value beyond strong
heuristic/static operating points.

### Protocol Split Matters

Explain that `goal_repeat=1` and `goal_repeat=10` probe different deployment
regimes. The protocol split prevents overclaiming from a single favorable
condition.

### Balanced Robustness Is Deployment-Relevant

Argue that a method with slightly lower peak performance but better
worst-protocol behavior may be more useful than a protocol specialist. This is
the main reason to center `risk_adapter_v1`.

### Diagnostic Labels Have Limits

State that `failure_group` labels organize evidence and guide inspection, but
they should not be interpreted as complete root-cause identification.

### Simulation-Only Evidence Has Limits

State that the current evidence is simulation-based and strong-wind benchmark
based. Hardware transfer, broader wind fields, additional targets, and formal
uncertainty analysis would be needed for stronger claims.

### Path Toward A Stronger ICRA/T-RO Extension

A stronger extension would need broader trials, possibly hardware validation,
more rigorous statistical analysis, formalized safety or reference-governor
properties, richer disturbance variation, and a mechanism-driven future policy
variant only if the paper audit reveals a generalizable gap.

## Limitations

- The evaluation is simulation-only.
- The repeated-run counts do not establish statistical significance.
- The execution governor is not a formal safety filter and provides no safety
  guarantee.
- `failure_group` labels are diagnostic and do not prove root cause.
- No current learned variant dominates both protocols as the absolute
  per-protocol winner.
- `risk_adapter_v22` is not yet justified by the current AA3/AC/AD evidence.

## Appendix / Supplementary Plan

Include:

- full per-run tables
- full failure-mode tables
- all representative traces
- launch parameters
- duplicate CSV audit notes
- protocol generator scripts
- optional ablation plans

Suggested appendix grouping:

- Appendix A: protocol definitions and launch settings
- Appendix B: full per-trial and per-run success tables
- Appendix C: failure-mode tables and diagnostic caveats
- Appendix D: representative trace index and additional trace plots
- Appendix E: method variants, hyperparameters, and ablation notes

## Claim Audit Table

| proposed claim | supported? | supporting evidence | caveat |
| --- | --- | --- | --- |
| `risk_adapter_v1` is the most balanced current learned / risk-conditioned method. | yes | Best mean valid count (`24.0/30`), best worst-protocol valid count (`23/30`), and lowest total regret (`2`). | Descriptive repeated-run result, not statistical significance. |
| `risk_adapter_v21` is overall best. | no | It is `25/30` single-goal but `20/30` stress, below `risk_adapter_v1` and `fixed_s080` under stress. | It remains a strong nominal / single-goal variant or ablation. |
| Learned methods dominate heuristic/static baselines. | no | `windlevel_s085` leads single-goal at `26/30`; `fixed_s080` leads stress at `24/30`. | Learned governors remain competitive and `risk_adapter_v1` is best balanced. |
| Protocol split exposes trade-offs hidden by single-protocol success. | yes | Single-goal and stress protocols have different leaders and different method orderings. | Applies to current protocol definitions and evaluated methods. |
| Failure taxonomy proves root cause. | no | Invalid-only groups organize failures into diagnostic categories. | `failure_group` labels are diagnostic, not complete causal proof. |
| No current learned variant dominates both protocols. | yes | `risk_adapter_v1` is balanced but not a per-protocol oracle; `risk_adapter_v21` is weaker under stress. | Future method design and evaluation could change this. |
| `risk_adapter_v1` should be the tentative paper protagonist. | yes | It has the strongest balanced robustness and lowest protocol regret among complete learned / risk-conditioned methods. | It should not be described as uniformly best or statistically significant. |
| `risk_adapter_v22` should be created immediately. | no | AA3 trace review and AC/AD framing do not reveal a generic mechanism requiring a new variant before writing. | Revisit only after claim audit or later mechanism-driven evidence. |

## Next Writing Step

Recommended Stage 4-AF: paper Abstract and Introduction draft.

Stage 4-AF should turn this skeleton into a concise abstract and a full
Introduction draft with contribution bullets. It should not recommend new
simulation or `risk_adapter_v22` yet.
