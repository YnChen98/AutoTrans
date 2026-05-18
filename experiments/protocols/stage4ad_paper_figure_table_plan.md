# Stage 4-AD Paper Figure Table Plan

## Executive Summary

Stage 4-AD freezes the paper figure and table plan for the reframed Stage 4
paper before drafting the main Results section.

Stage 4-AE builds on this plan by creating the paper outline and section
skeleton:
`experiments/protocols/stage4ae_paper_outline_section_skeleton.md`.
Stage 4-AF now drafts the Abstract and Introduction, and the figures/tables in
this plan should support those AF claims:
`experiments/protocols/stage4af_abstract_introduction_draft.md`.

The paper should use four evidence layers:

- protocol-split strict-valid success counts
- balanced robustness and protocol regret
- invalid-only failure groups
- representative trace case studies

The main protagonist is `risk_adapter_v1` as the balanced learned /
risk-conditioned execution governor. `risk_adapter_v21` should be presented as
a strong nominal / single-goal variant or ablation, not as the final method.

The figure plan should make the protocol split explicit. It should show why
`windlevel_s085` is a single-goal specialist, why `fixed_s080` is a
goal-reissue stress specialist, and why `risk_adapter_v1` is the best current
balanced learned / risk-conditioned method by mean valid count,
worst-protocol valid count, and total regret.

## Main Paper Figure/Table Plan

### Table 1: Protocol-Split Success And Balanced Robustness

Likely placement: Results.

Columns:

- method
- single-goal strict-valid
- goal-reissue stress strict-valid
- mean valid
- worst-protocol valid
- total regret
- method role

Planned table:

| method | single-goal strict-valid | goal-reissue stress strict-valid | mean valid | worst-protocol valid | total regret | method role |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `original` | `21/30` | `18/30` | `19.5/30` | `18/30` | `11` | unadapted baseline |
| `fixed_s085` | `22/30` | `18/30` | `20.0/30` | `18/30` | `10` | fixed static baseline |
| `windlevel_s085` | `26/30` | `16/30` | `21.0/30` | `16/30` | `8` | single-goal specialist heuristic |
| `fixed_s080` | `21/30` | `24/30` | `22.5/30` | `21/30` | `5` | goal-reissue stress specialist static frontier |
| `risk_adapter_v1` | `25/30` | `23/30` | `24.0/30` | `23/30` | `2` | balanced learned / risk-conditioned governor |
| `risk_adapter_v21` | `25/30` | `20/30` | `22.5/30` | `20/30` | `5` | strong nominal / single-goal learned variant |

`risk_adapter_v2` may be included as a single-goal-only appendix note because
its single-goal result is `21/30` and its goal-reissue stress result is
missing from the complete cross-protocol matrix.

Supported claim: `risk_adapter_v1` is the most balanced learned /
risk-conditioned method in the current evaluation.

Caveat: the table gives descriptive repeated-run counts, not statistical
significance or a safety guarantee.

Draft caption: Table 1. Protocol-split strict-valid success and balanced
robustness metrics under strong wind. `risk_adapter_v1` has the best mean
valid count, best worst-protocol count, and lowest total regret, while
`windlevel_s085` and `fixed_s080` specialize to different protocols.

### Figure 1: System Architecture

Likely placement: Method.

Show:

- AutoTrans-like planner / payload MPC / SO3 controller stack
- external learned risk-conditioned execution governor
- `speed_scale` / `acceleration_scale` interface
- risk input and command adaptation output

Supported claim: the learned governor is an external execution-layer
adaptation module, not a planner/controller rewrite.

Caveat: the diagram explains the interface and information flow; it does not
itself validate robustness.

Draft caption: Figure 1. Execution-governor architecture. The learned
risk-conditioned governor observes risk-related inputs and publishes
`speed_scale` and `acceleration_scale` commands to adapt execution while
leaving the AutoTrans-like planning and control stack intact.

### Figure 2: Protocol Split Diagram

Likely placement: Experimental Setup.

Show:

- single-goal mission protocol, `goal_repeat=1`
- goal-reissue stress protocol, `goal_repeat=10`
- why the two protocols test different deployment regimes

Supported claim: the two protocols expose different robustness properties and
should not be collapsed into one mixed-protocol aggregate.

Caveat: the diagram defines evaluation regimes; it does not rank methods.

Draft caption: Figure 2. Dual-protocol evaluation design. The single-goal
mission protocol tests one commanded mission, whereas the goal-reissue stress
protocol repeatedly republishes the same goal and stresses post-arrival and
reference-update behavior.

### Figure 3: Balanced Robustness / Pareto Plot

Likely placement: Results.

Use Stage 4-AC output:

- x-axis: single-goal valid count
- y-axis: goal-reissue stress valid count
- highlighted Pareto frontier:
  - `windlevel_s085`
  - `fixed_s080`
  - `risk_adapter_v1`

Supported claim: `risk_adapter_v1` lies on the Pareto frontier and provides
the best learned / risk-conditioned balance across the two protocols.

Caveat: Pareto-frontier status is relative to the current evaluated methods and
protocol counts.

Draft caption: Figure 3. Balanced robustness across the protocol split.
`windlevel_s085`, `fixed_s080`, and `risk_adapter_v1` form the observed Pareto
frontier; `risk_adapter_v21` is dominated by `risk_adapter_v1`, which has the
same single-goal count and a higher stress count.

### Figure 4: Protocol Regret Bar Chart

Likely placement: Results.

Use Stage 4-AC output:

- single-goal regret
- stress regret
- total regret

Emphasize that `risk_adapter_v1` has the lowest total regret (`2`) relative to
the protocol oracles.

Supported claim: protocol regret makes the specialist trade-off visible and
identifies `risk_adapter_v1` as the balanced protagonist.

Caveat: regret is relative to observed protocol oracles, not a theoretical
optimum.

Draft caption: Figure 4. Protocol regret relative to observed protocol
oracles. `risk_adapter_v1` has the lowest total regret, while
`windlevel_s085` and `fixed_s080` trade off performance across protocols.

### Figure 5: Invalid-Only Failure Group Stacked Bar

Likely placement: Failure Analysis.

Use Stage 4-Z2 invalid-only output, not the all-run view.

Show failure groups such as:

- `command_control_upstream`
- `planner_reference_upstream`
- `state_task_upstream`

Supported claim: invalid-only failure analysis explains why aggregate success
alone is insufficient and motivates failure-mode-aware interpretation.

Caveat: `failure_group` is diagnostic and should not be described as perfect
root-cause proof.

Draft caption: Figure 5. Invalid-only failure-group distribution. The
diagnostic failure groups reveal distinct invalid-run patterns across methods
and protocols, supporting failure-mode-aware interpretation without replacing
strict-valid success as the main metric.

### Figure 6: Representative Trace Case Study

Likely placement: Failure Analysis or Results.

Use Stage 4-AA2 / Stage 4-AA3 traces.

Planned panels:

- Figure 6a: Trial 4 goal-reissue stress `risk_adapter_v21` failure compared
  with `fixed_s080` and `risk_adapter_v1` successes.
- Figure 6b: Trial 6 single-goal bottleneck comparing `risk_adapter_v21` /
  `risk_adapter_v1` against `windlevel_s085` / `fixed_s080`.

Supported claim: representative traces show mechanisms behind the balanced
robustness result, including early pre-arrival vulnerability, risk signal
availability/timing issues, and post-arrival delayed divergence.

Caveat: selected traces are qualitative case studies and cannot prove
population-level causality.

Draft caption: Figure 6. Representative trace case studies. Trial 4
goal-reissue stress traces illustrate why `risk_adapter_v21` weakens under the
stress protocol, while Trial 6 single-goal traces show that lower scale is not
automatically safer and that protocol-specialist baselines can avoid some
failure patterns.

## Appendix / Supplementary Figure Plan

Include:

- full protocol-split per-trial success table
- full failure-mode count table
- all-run failure group table
- representative trace index
- additional trace plots
- full method variant details
- exact hyperparameters / launch settings
- duplicate CSV and audit caveats if needed

These materials should support auditability without making the main paper read
like an experiment log.

## Figure Captions Draft

Short captions to carry forward:

- Table 1: Protocol-split strict-valid success and balanced robustness metrics
  under strong wind.
- Figure 1: Learned risk-conditioned execution-governor architecture.
- Figure 2: Dual-protocol evaluation design separating `goal_repeat=1` from
  `goal_repeat=10`.
- Figure 3: Balanced robustness / Pareto plot across single-goal and
  goal-reissue stress protocols.
- Figure 4: Protocol regret relative to observed protocol oracles.
- Figure 5: Invalid-only diagnostic failure-group distribution.
- Figure 6: Representative trace case studies for stress weakness and
  single-goal bottleneck behavior.

## Paper Placement

| item | likely section |
| --- | --- |
| Figure 1 | Method |
| Figure 2 | Experimental Setup |
| Table 1 | Results |
| Figure 3 | Results |
| Figure 4 | Results |
| Figure 5 | Failure Analysis |
| Figure 6 | Failure Analysis or Results |
| supplementary per-trial tables | Appendix |
| supplementary trace index and extra traces | Appendix |
| method variant details and launch settings | Appendix |

## Claim Supported By Each Figure

| item | supported claim | caveat |
| --- | --- | --- |
| Table 1 | `risk_adapter_v1` is the current balanced learned / risk-conditioned protagonist. | Descriptive counts only; no statistical significance. |
| Figure 1 | The governor adapts execution through `speed_scale` / `acceleration_scale` without rewriting the core stack. | Architecture alone does not validate robustness. |
| Figure 2 | The protocol split evaluates different deployment regimes. | Protocol design does not rank methods by itself. |
| Figure 3 | `risk_adapter_v1` is Pareto-frontier and `risk_adapter_v21` is dominated by `risk_adapter_v1`. | Frontier is limited to evaluated methods. |
| Figure 4 | `risk_adapter_v1` has the lowest observed protocol regret. | Regret is relative to observed protocol oracles. |
| Figure 5 | Failure groups expose diagnostic patterns hidden by aggregate success. | Failure groups are diagnostic, not root-cause proof. |
| Figure 6 | Trace case studies explain stress weakness and single-goal bottlenecks. | Case studies are qualitative examples. |

## What Not To Put In Main Paper

- long raw diagnostic tables
- all individual run logs
- debug history
- unfiltered variant timeline
- mixed-protocol aggregate
- overclaim that a learned method dominates all baselines

## Next Writing Step

Stage 4-AE recorded the paper outline / section skeleton.

Stage 4-AE drafted:

- abstract claim
- intro contribution bullets
- method section skeleton
- experiment section skeleton
- results section skeleton

The outline should center `risk_adapter_v1` as the balanced learned /
risk-conditioned governor, present `windlevel_s085` and `fixed_s080` as strong
protocol specialists, and keep `risk_adapter_v21` as a strong nominal variant
/ ablation.

Stage 4-AE is recorded in
`experiments/protocols/stage4ae_paper_outline_section_skeleton.md`, and Stage
4-AF is recorded in
`experiments/protocols/stage4af_abstract_introduction_draft.md`. The next
writing step after AF is Stage 4-AG Method section draft or Stage 4-AH Results
section draft.
