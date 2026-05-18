# Stage 4-AM3 Citation Insertion Draft

## Executive Summary

Stage 4-AM3 is a citation insertion draft for the assembled Stage 4 paper. It
maps citation keys recorded in Stage 4-AM2 into the current full paper assembly
draft, without final manuscript formatting.

This document uses only citation keys already recorded in
`experiments/protocols/stage4am2_verified_citation_collection_result.md`.
Final BibTeX is still pending. Entries with incomplete metadata remain
conditional and should be used only after the stated metadata checks are
completed.

This stage does not generate BibTeX entries, does not fabricate references,
and does not insert final citations into the manuscript body. It is a section-
level guide for later citation insertion and claim audit.

The paper framing remains:

- risk-conditioned execution governance for suspended-payload UAV transport
  under strong wind,
- protocol-split robustness evaluation,
- balanced robustness / protocol regret analysis,
- failure-mode-aware diagnosis.

`risk_adapter_v1` remains the tentative balanced learned / risk-conditioned
protagonist. `risk_adapter_v21` remains an ablation / strong nominal variant,
not the final method. Do not create `risk_adapter_v22`.

## Citation Key Readiness

### A. Ready-To-Use Citation Keys

These keys have complete enough metadata in Stage 4-AM2 for insertion planning.
Final BibTeX still remains pending.

- `Li2023AutoTrans`
- `Sreenath2013DifferentiallyFlatHybrid`
- `Son2020ObstacleAvoidanceSuspendedLoad`
- `UrbinaBrito2021PredictivePayloadTransport`
- `Lee2010GeometricTrackingSE3`
- `GuerreroSanchez2017SwingAttenuation`
- `Garone2017ReferenceCommandGovernorsSurvey`
- `Garone2016ExplicitReferenceGovernor`
- `Nicotra2016UAVRobustERG`
- `Li2021ActionGovernor`
- `Hsu2024SafetyFilterUnifiedView`
- `Andersson2017RiskAwareActiveLearning`
- `Bauersfeld2021NeuroBEM`
- `Torrente2021DataDrivenMPC`
- `Saviolo2022PITCN`
- `Lee2024HybridDisturbancePrediction`
- `Muller2019MeasureTargetConfusion`
- `Koren2018AdaptiveStressTesting`
- `Nalic2020StressTestingScenarioBasedADS`
- `Cameron2024DomesticRobotFailureOutcomes`

### B. Conditional Citation Keys Pending Metadata Verification

Use these only after verification:

- `Barikbin2019WindPayloadTracking`: use after venue/year verification.
- `Wabersich2021PredictiveSafetyFilter`: use after DOI / Automatica metadata
  verification.
- `Jin2025NeuralPredictorPayload`: use after final metadata verification.
- `Monteleone2023BalanceResilienceBenchmark`: use after complete author-list
  verification.
- `Dogga2023AutoARTS`: use after official USENIX URL verification.

### C. Internal-Result References

Use these as internal evidence references rather than external citations:

- Table 1
- Figure 1
- Figure 2
- Figure 3
- Figure 4
- Figure 5
- Figure 6
- Stage 4 protocol split assets
- Stage 4 balanced robustness / protocol regret assets
- Stage 4 failure-mode assets

## Abstract Citation Plan

Many IROS/ICRA/RA-L style abstracts use few or no citations, depending on
format and venue style. Keep the abstract citation-free if the target format
discourages citations.

If citations are allowed, cite only the broad suspended-payload transport
context and execution-governor concept sparingly. Candidate keys:

- `Li2023AutoTrans`
- `Sreenath2013DifferentiallyFlatHybrid`
- `Garone2017ReferenceCommandGovernorsSurvey`

Do not cite all method details in the abstract. The quantitative Stage 4
results should be supported by internal references to Table 1 and Figures 3-6
in the main text.

## Introduction Citation Insertion Draft

### Paragraph 1: Suspended-Payload Transport Under Wind

Claim being supported:

- Suspended-payload UAV transport has coupled vehicle-load dynamics and is
  sensitive to payload swing, tracking error, and wind/task disturbances.

Recommended citation keys:

- `Li2023AutoTrans`
- `Sreenath2013DifferentiallyFlatHybrid`
- `Son2020ObstacleAvoidanceSuspendedLoad`
- `GuerreroSanchez2017SwingAttenuation`

Suggested insertion point:

- After the first sentence that introduces suspended-payload UAV transport and
  coupled vehicle-load dynamics.

Caveat:

- Use `Barikbin2019WindPayloadTracking` only after venue/year verification if
  the paragraph makes a broader wind-presence claim beyond the tested setup.

### Paragraph 2: Planner / MPC / Controller Stacks And Runtime Aggressiveness

Claim being supported:

- Payload-aware planning, MPC, and low-level control are important foundations,
  but runtime execution aggressiveness remains a separate interface-level
  concern.

Recommended citation keys:

- `Li2023AutoTrans`
- `Son2020ObstacleAvoidanceSuspendedLoad`
- `UrbinaBrito2021PredictivePayloadTransport`
- `Lee2010GeometricTrackingSE3`

Suggested insertion point:

- After the sentence naming planning, MPC, and low-level control as the core
  stack.

Caveat:

- Do not imply prior work is generally insufficient. Frame the paper as
  complementary to planner/MPC/controller methods.

### Paragraph 3: Execution Governance As A Drop-In Layer

Claim being supported:

- External command/reference modulation has conceptual precedent, and the
  proposed execution governor adapts `speed_scale` and `acceleration_scale`
  without replacing the inner stack.

Recommended citation keys:

- `Garone2017ReferenceCommandGovernorsSurvey`
- `Garone2016ExplicitReferenceGovernor`
- `Li2021ActionGovernor`

Suggested insertion point:

- After introducing execution governance as a drop-in layer.

Caveat:

- Do not cite safety-filter references here in a way that implies formal
  guarantees.

### Paragraph 4: Protocol Split And Stress Evaluation

Claim being supported:

- Evaluation regimes should be reported separately when they test different
  operational behavior; stress testing can expose failures hidden by nominal
  testing.

Recommended citation keys:

- `Koren2018AdaptiveStressTesting`
- `Nalic2020StressTestingScenarioBasedADS`
- `Muller2019MeasureTargetConfusion`

Suggested insertion point:

- After explaining the single-goal mission protocol and goal-reissue stress
  protocol as distinct evaluation regimes.

Caveat:

- Do not use these citations to justify a mixed-protocol aggregate. They should
  support the opposite: protocol-conditioned interpretation.

### Paragraph 5: Core Empirical Findings

Claim being supported:

- The specific findings about `windlevel_s085`, `fixed_s080`,
  `risk_adapter_v1`, and `risk_adapter_v21` are internal Stage 4 results.

Recommended references:

- Table 1
- Figure 3
- Figure 4

Suggested insertion point:

- Use internal figure/table references near the quantitative claims.

Caveat:

- No external citation can establish the Stage 4 result ranking. Do not add
  citation keys as substitutes for internal evidence.

### Paragraph 6: Contributions

Claim being supported:

- Contributions summarize the method, protocol-split evaluation, balanced
  robustness metrics, and failure-mode-aware diagnostic workflow.

Recommended references:

- Figure 1 for the stack-compatible interface.
- Figure 2 for the protocol split.
- Table 1 / Figures 3-4 for balanced robustness and regret.
- Figure 5 / Figure 6 for failure-aware analysis.

Suggested insertion point:

- Use figure/table references only if the venue style permits references in
  contribution bullets.

Caveat:

- Avoid over-citing contribution bullets. They should point to the evidence
  locations, not repeat the full Related Work.

## Related Work 2.1 Draft: Suspended-Payload Transport Stack And Control Backbone

Draft paragraph:

Suspended-payload UAV transport has been studied through coupled-load
trajectory generation, integrated planning and control stacks, online optimal
trajectory generation, predictive payload control, and geometric quadrotor
control. Differential-flatness and hybrid-system formulations provide an early
foundation for cable-suspended load trajectory generation
[`Sreenath2013DifferentiallyFlatHybrid`], while integrated frameworks such as
AutoTrans combine planning and control for autonomous payload transportation
[`Li2023AutoTrans`]. Real-time optimal trajectory generation has also been
used for obstacle avoidance with suspended loads
[`Son2020ObstacleAvoidanceSuspendedLoad`], and predictive control has been
applied to aerial payload transport with swing-related constraints
[`UrbinaBrito2021PredictivePayloadTransport`]. Low-level quadrotor tracking is
commonly grounded in geometric SE(3) / SO(3) control
[`Lee2010GeometricTrackingSE3`], and swing attenuation remains an important
transport-performance concern [`GuerreroSanchez2017SwingAttenuation`]. Work on
wind-present cable-suspended payload tracking may further motivate the strong-
wind setting after metadata verification
[`Barikbin2019WindPayloadTracking`, use after verification]. In contrast to
replacing these planner, MPC, or controller components, the present paper
studies a complementary execution-governance layer that modulates runtime
aggressiveness through `speed_scale` and `acceleration_scale`.

Claim boundary:

- This paragraph should not claim prior stack/control work is insufficient in
  general. It should state that the present paper studies a different interface
  layer.

## Related Work 2.2 Draft: Runtime Governors And Safety-Filter Boundary

Draft paragraph:

Runtime governance methods provide a conceptual precedent for modifying
references or commands around an existing controller. Reference and command
governors are commonly framed as add-on schemes for constrained or
pre-stabilized systems [`Garone2017ReferenceCommandGovernorsSurvey`], with
explicit reference governors extending this idea to constrained nonlinear
systems [`Garone2016ExplicitReferenceGovernor`]. Robust explicit reference
governors have also been studied in UAV settings [`Nicotra2016UAVRobustERG`],
and action governors provide another supervisory view of modifying nominal
control signals [`Li2021ActionGovernor`]. Safety-filter literature gives a
stronger certified-control boundary for runtime intervention
[`Hsu2024SafetyFilterUnifiedView`], with predictive safety filters for
learning-based constrained nonlinear systems available as a conditional
comparison after metadata verification
[`Wabersich2021PredictiveSafetyFilter`, use after verification]. The governor
in this paper is empirical: it adapts execution scales through the existing
command-adaptation interface and does not provide formal invariance,
stability, or safety guarantees.

Claim boundary:

- Do not describe the Stage 4 governor as a certified reference governor or
  safety filter.

## Related Work 2.3 Draft: Learning-Enhanced Aerial Robustness

Draft paragraph:

Learning has been used to improve aerial robustness through risk-aware control,
hybrid aerodynamic modeling, data-driven model predictive control, temporal
learning of dynamics, and disturbance prediction. Risk-aware active learning
has been explored for quadcopter control [`Andersson2017RiskAwareActiveLearning`],
while hybrid aerodynamic models and data-driven MPC show how learned models
can complement model-based aerial control [`Bauersfeld2021NeuroBEM`,
`Torrente2021DataDrivenMPC`]. Physics-inspired temporal learning has also been
integrated with MPC for trajectory tracking [`Saviolo2022PITCN`], and hybrid
model-based / data-driven disturbance prediction has been used for precise
quadrotor tracking [`Lee2024HybridDisturbancePrediction`]. Payload-specific
learned prediction may provide additional context after final metadata
verification [`Jin2025NeuralPredictorPayload`, use after verification]. The
present work follows this broader learning-enhanced robustness direction but
uses learned risk information in a lightweight execution-governor layer rather
than replacing the planner, MPC, or low-level controller.

Claim boundary:

- Do not use learning citations to imply learned methods uniformly dominate
  heuristic or fixed baselines. The Stage 4 result is balanced robustness under
  tested protocols.

## Related Work 2.4 Draft: Benchmarking / Stress Testing / Failure Analysis

Draft paragraph:

Robotics evaluation depends on the choice of measurement target and protocol:
benchmark scores can become misleading when they are treated as general
capability rather than context-dependent evidence
[`Muller2019MeasureTargetConfusion`]. Stress testing provides a complementary
way to expose failures that may not appear under nominal evaluation
[`Koren2018AdaptiveStressTesting`, `Nalic2020StressTestingScenarioBasedADS`].
Repeatable perturbation protocols for robustness can further motivate
protocol-conditioned evaluation after complete author-list verification
[`Monteleone2023BalanceResilienceBenchmark`, use after verification]. Failure
taxonomies can organize observed failures and their consequences
[`Cameron2024DomesticRobotFailureOutcomes`], and incident root-cause labeling
offers a related diagnostic perspective after official URL verification
[`Dogga2023AutoARTS`, use after verification]. In this paper, protocol-split
success counts and invalid-only failure groups are used as diagnostic evidence
under the tested protocols, not as proof of exact physical root cause.

Claim boundary:

- Use these citations to justify protocol-split and failure-aware evaluation,
  not to justify a mixed-protocol aggregate or root-cause certainty.

## Method Section Citation Insertion Plan

| method claim | recommended citation keys | insertion point | caveat |
| --- | --- | --- | --- |
| AutoTrans-like stack | `Li2023AutoTrans` | First paragraph that names the underlying stack. | Cite as stack context, not as the new method. |
| Suspended-payload planning/control context | `Sreenath2013DifferentiallyFlatHybrid`, `Son2020ObstacleAvoidanceSuspendedLoad`, `UrbinaBrito2021PredictivePayloadTransport` | System stack and problem setting paragraph. | Keep discussion concise; avoid turning Method into Related Work. |
| SO3/geometric controller | `Lee2010GeometricTrackingSE3` | Sentence naming the SO3 controller or geometric tracking background. | Cite the controller backbone only. |
| Governor concept | `Garone2017ReferenceCommandGovernorsSurvey`, `Garone2016ExplicitReferenceGovernor`, `Li2021ActionGovernor` | Execution-governor interface subsection. | State conceptual relation, not formal equivalence. |
| Safety-boundary caveat | `Hsu2024SafetyFilterUnifiedView`, `Wabersich2021PredictiveSafetyFilter` after verification | Claim-boundary subsection. | Do not imply certified safety; use `Wabersich2021PredictiveSafetyFilter` only after metadata verification. |

## Experimental Setup Citation Insertion Plan

| setup claim | recommended citation keys | insertion point | caveat |
| --- | --- | --- | --- |
| Benchmark / stress protocol motivation | `Muller2019MeasureTargetConfusion`, `Koren2018AdaptiveStressTesting`, `Nalic2020StressTestingScenarioBasedADS` | Protocol definitions paragraph. | Use to motivate separate protocols, not a mixed aggregate. |
| Repeated robustness / perturbation protocol | `Monteleone2023BalanceResilienceBenchmark` after verification | Repeated-run design paragraph. | Conditional until complete author list is verified. |
| Strong wind / suspended payload background | `Li2023AutoTrans`, `GuerreroSanchez2017SwingAttenuation`, `Barikbin2019WindPayloadTracking` after verification | Strong-wind task paragraph. | Use `Barikbin2019WindPayloadTracking` only after venue/year verification. |
| Internal result counts and metric definitions | Table 1, Figure 2, Stage 4 protocol-split assets | Strict-valid metric and protocol assets paragraphs. | Internal evidence; external citations are not substitutes for experiment assets. |

## Discussion / Limitations Citation Insertion Plan

| discussion claim | recommended citation keys | insertion point | caveat |
| --- | --- | --- | --- |
| No certified safety / boundary | `Hsu2024SafetyFilterUnifiedView`, `Wabersich2021PredictiveSafetyFilter` after verification | Limitations paragraph on safety guarantees. | Do not imply the method is a safety filter. |
| Failure labels are diagnostic | `Cameron2024DomesticRobotFailureOutcomes`, `Dogga2023AutoARTS` after verification | Failure-mode-aware interpretation paragraph. | Use `Dogga2023AutoARTS` only after official URL verification. |
| Learning-enhanced future work | `Torrente2021DataDrivenMPC`, `Saviolo2022PITCN`, `Lee2024HybridDisturbancePrediction`, `Jin2025NeuralPredictorPayload` after verification | Future work paragraph on risk calibration / learned prediction. | Do not imply learned domination or current hardware validation. |
| Protocol-conditioned interpretation | `Muller2019MeasureTargetConfusion`, `Koren2018AdaptiveStressTesting` | Discussion paragraph on protocol split. | Keep claims limited to tested protocols. |

## Conditional Citation TODOs

- Verify `Barikbin2019WindPayloadTracking` venue/year.
- Verify `Wabersich2021PredictiveSafetyFilter` DOI / Automatica metadata.
- Verify `Jin2025NeuralPredictorPayload` final metadata.
- Verify `Monteleone2023BalanceResilienceBenchmark` complete author list.
- Verify `Dogga2023AutoARTS` official USENIX URL.

## What Not To Do

- Do not insert fabricated BibTeX.
- Do not cite conditional entries as final before verification.
- Do not over-cite every sentence.
- Do not use safety-filter citations to imply a certified safety guarantee.
- Do not use learning citations to imply learned dominance.
- Do not use benchmarking citations to justify a mixed-protocol aggregate.
- Do not use citation keys as a replacement for Table 1 / Figures 1-6 when
  supporting internal Stage 4 results.
- Do not create or introduce `risk_adapter_v22`.
