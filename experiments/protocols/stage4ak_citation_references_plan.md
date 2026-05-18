# Stage 4-AK Citation References Plan

## Executive Summary

This document is the citation / reference planning document for the assembled
Stage 4 paper draft:
`experiments/protocols/stage4aj_full_paper_assembly_draft.md`.
Stage 4-AM now defines the practical citation collection and bibliography
insertion workflow:
`experiments/protocols/stage4am_citation_collection_plan.md`.
Stage 4-AM2 now provides candidate verified citations for the TODO citation
slots:
`experiments/protocols/stage4am2_verified_citation_collection_result.md`.
Stage 4-AL now defines the final figure/table generation plan; final
citations, figure captions, and paper claims should be checked together:
`experiments/protocols/stage4al_final_figure_generation_plan.md`.

It does not finalize the bibliography, does not provide BibTeX entries, and
does not replace TODO citation placeholders with unverified references. Its
purpose is to map each paper section and claim to the required citation
categories so the final manuscript can be checked without fabricating sources.

The current paper framing remains:

- risk-conditioned execution governance for suspended-payload UAV transport
  under strong wind
- protocol-split robustness evaluation
- balanced robustness / protocol regret analysis
- failure-mode-aware diagnosis

`risk_adapter_v1` remains the tentative balanced learned / risk-conditioned
protagonist. `risk_adapter_v21` remains an ablation / strong nominal variant,
not the final method.

## Citation Slots By Paper Section

### Abstract / Introduction

Citation needs:

- suspended-payload UAV transport as a challenging aerial manipulation /
  transport problem
- coupled UAV-load dynamics and payload swing
- wind disturbance effects on tracking, swing, and arrival behavior
- importance of payload-aware planning, MPC, and low-level control
- motivation for runtime execution governance or command adaptation
- evaluation protocol design / stress testing as a robustness issue

Current placeholders to preserve until verified:

- `[TODO: suspended-payload UAV planning]`
- `[TODO: payload-aware MPC]`
- `[TODO: SO3 / geometric quadrotor control]`
- `[TODO: stress testing for autonomous systems]`

Internal evidence support:

- Stage 4 protocol-split counts
- Stage 4-AC balanced robustness / protocol regret result
- Stage 4-Z2 invalid-only failure groups
- Stage 4-AA3 representative trace review

### Related Work

Citation needs are organized by subsection in the Related Work citation map
below. The final manuscript should use topic-synthesis paragraphs, not a
paper-by-paper citation dump.

Current placeholders to preserve until verified:

- `[TODO: AutoTrans]`
- `[TODO: suspended-payload UAV planning]`
- `[TODO: payload-aware MPC]`
- `[TODO: SO3 / geometric quadrotor control]`
- `[TODO: reference governor]`
- `[TODO: runtime safety filter]`
- `[TODO: action governor]`
- `[TODO: command filtering for robotics]`
- `[TODO: learning-enhanced UAV control]`
- `[TODO: learned disturbance or risk prediction]`
- `[TODO: data-driven robustness in aerial robotics]`
- `[TODO: robotics benchmarking]`
- `[TODO: stress testing for autonomous systems]`
- `[TODO: failure analysis / taxonomy]`

### Method

Citation needs:

- AutoTrans-like planner / payload MPC / SO3 controller stack
- command/reference governor concepts that motivate execution-layer command
  shaping
- learned risk prediction or risk-conditioned adaptation concepts
- geometric / SO3 control background if the low-level controller is named

Internal details still needed before final manuscript:

- exact source of `risk_score_3s` and `risk_score_5s`
- risk model training set, features, horizons, inference rate, and calibration
- exact command-adaptation implementation path and interface description

### Experimental Setup

Citation needs:

- simulator / AutoTrans-like stack source citation
- strong-wind simulation or disturbance-model precedent if making broader wind
  claims
- repeated-run robustness evaluation / benchmarking precedent

Internal details still needed:

- exact strong-wind parameter values and config path
- simulator version / stack commit / branch
- strict-valid metric definition
- repeat naming / seed / run convention
- generated figure/table asset paths

### Results

Citation needs:

- Mostly internal experimental result citations / references to generated
  tables and figures, not external literature.
- Use external citations only when interpreting evaluation methodology, such as
  benchmarking, stress testing, or failure taxonomies.

Internal evidence support:

- Table 1 protocol-split success and balanced robustness
- Figure 3 Pareto frontier
- Figure 4 protocol regret
- Figure 5 invalid-only failure groups
- Figure 6 representative traces

### Discussion / Limitations

Citation needs:

- runtime governance / safety-filter literature for conceptual comparison
- benchmarking / stress-testing literature for protocol split
- failure taxonomy / diagnostic-analysis literature for caveated failure labels
- learning-enhanced robustness literature for future-work positioning

Claims that should remain internally bounded:

- no formal safety guarantee
- no statistical significance claim
- no real-world deployment claim
- diagnostic labels are not exact physical root cause

## Related Work Citation Map

### A. Suspended-Payload UAV Transport And Control

Need citations for:

- AutoTrans-like suspended-payload transport stack
- payload-aware trajectory planning
- payload MPC / nonlinear MPC for suspended loads
- geometric / SO3 quadrotor control
- wind-disturbance or load-swing robust UAV transport

Citation slots:

- `[TODO: AutoTrans]`
- `[TODO: suspended-payload UAV planning]`
- `[TODO: payload-aware MPC]`
- `[TODO: SO3 / geometric quadrotor control]`
- `[TODO: wind-disturbance suspended-payload UAV transport]`

Use in manuscript:

- Establish that suspended-payload transport has coupled load dynamics and
  swing-sensitive execution.
- Position this paper as complementary to planner/MPC/controller work because
  it studies runtime execution aggressiveness through an external governor.

### B. Runtime Governors / Reference Governors / Safety Filters

Need citations for:

- reference governor / explicit reference governor
- action governor / command filtering
- runtime safety filters
- safety filters for learned control
- distinction between certified safety filters and the empirical governor here

Citation slots:

- `[TODO: reference governor]`
- `[TODO: explicit reference governor]`
- `[TODO: action governor]`
- `[TODO: command filtering for robotics]`
- `[TODO: runtime safety filter]`
- `[TODO: safety filters for learned control]`

Use in manuscript:

- Provide conceptual precedent for modifying commands at runtime.
- Clearly state that the proposed governor is empirical and not certified; it
  does not provide formal invariance, stability, or safety guarantees.

### C. Learning-Enhanced Aerial Robustness

Need citations for:

- learned risk prediction
- learning-enhanced UAV control
- disturbance-aware learning
- hybrid learning + model-based control

Citation slots:

- `[TODO: learned risk prediction]`
- `[TODO: learning-enhanced UAV control]`
- `[TODO: learned disturbance or risk prediction]`
- `[TODO: disturbance-aware learning for UAVs]`
- `[TODO: hybrid learning + model-based control]`
- `[TODO: data-driven robustness in aerial robotics]`

Use in manuscript:

- Place `risk_adapter_v1` in the broader category of learning-enhanced
  execution adaptation.
- Avoid implying that learning uniformly dominates fixed or heuristic
  baselines.

### D. Benchmarking, Stress Testing, And Failure Analysis

Need citations for:

- robotics benchmarking
- stress testing autonomous systems
- repeated-run evaluation
- failure taxonomy / failure log analysis
- diagnostic labels versus physical root-cause caveat

Citation slots:

- `[TODO: robotics benchmarking]`
- `[TODO: stress testing for autonomous systems]`
- `[TODO: repeated-run robotics evaluation]`
- `[TODO: failure analysis / taxonomy]`
- `[TODO: failure log analysis]`

Use in manuscript:

- Justify protocol-split evaluation and repeated runs.
- Support the idea that failure labels help diagnosis but should be caveated as
  diagnostic, not definitive root-cause proof.

## Claim-To-Citation Table

| claim | section | citation type needed | current placeholder | status | notes |
| --- | --- | --- | --- | --- | --- |
| Suspended-payload UAV transport is challenging due to coupled load dynamics. | Abstract / Introduction, Related Work | suspended-payload transport and control literature | `[TODO: suspended-payload UAV planning]` | TODO | Needs external citation before submission. |
| Strong wind affects tracking and swing. | Abstract / Introduction, Experimental Setup | wind-disturbance or robust aerial transport literature | `[TODO: wind-disturbance suspended-payload UAV transport]` | TODO | Internal results support tested setting only; broader statement needs citation. |
| Existing planner/MPC/controller stacks are important but execution aggressiveness remains a runtime issue. | Introduction, Method | AutoTrans-like stack plus runtime governor precedent | `[TODO: AutoTrans]`, `[TODO: reference governor]` | TODO | Keep wording complementary, not dismissive. |
| Reference/runtime governors provide conceptual precedent. | Related Work, Method | reference governor / runtime safety filter literature | `[TODO: reference governor]`, `[TODO: runtime safety filter]` | TODO | Also caveat that this method is empirical. |
| Learned risk signals can support adaptive execution. | Related Work, Method | learned risk prediction / learning-enhanced control literature | `[TODO: learned risk prediction]`, `[TODO: learning-enhanced UAV control]` | TODO | Do not claim uniform learned dominance. |
| Benchmarking should separate operational regimes. | Introduction, Experimental Setup, Discussion | robotics benchmarking and stress testing literature | `[TODO: robotics benchmarking]`, `[TODO: stress testing for autonomous systems]` | TODO | Internal protocol-split result supports this paper's tested case. |
| Failure taxonomy can support system diagnosis. | Results, Discussion | failure taxonomy / log analysis literature | `[TODO: failure analysis / taxonomy]` | TODO | Must remain diagnostic, not root-cause proof. |
| No formal safety guarantee is claimed. | Method, Discussion / Limitations | safety filter / reference governor distinction | `[TODO: runtime safety filter]`, `[TODO: safety filters for learned control]` | TODO | This is primarily a claim-boundary statement; citations help contrast certified methods. |
| `risk_adapter_v1` is the most balanced current learned / risk-conditioned method. | Results | internal experimental evidence | Table 1, Figure 3, Figure 4 | internally supported | No external citation needed, but no statistical claim. |
| `windlevel_s085` and `fixed_s080` are protocol specialists. | Results, Discussion | internal experimental evidence | Table 1, Figure 3 | internally supported | No external citation needed. |

## Missing Technical Details Table

| missing detail | needed for | current status | notes |
| --- | --- | --- | --- |
| source of risk scores | Method reproducibility | TODO | Define where `risk_score_3s` and `risk_score_5s` come from. |
| risk model training data | Method and limitations | TODO | Identify dataset rows, labels, splits, and exclusions. |
| risk features / horizons | Method reproducibility | TODO | Document feature groups and `3s` / `5s` horizon definitions. |
| inference rate | Method reproducibility | TODO | State how often the governor receives or computes risk. |
| calibration / confidence | Method and limitations | TODO | Important because AA3 suggests risk availability / timing issues. |
| command adaptation implementation details | Method reproducibility | partial | Need exact interface, topics, and how scales modify execution. |
| exact strong-wind setup | Experimental Setup | partial | Record config values and config path used for paper runs. |
| simulator version / stack commit / branch | Experimental Setup | TODO | Needed for reproducibility. |
| method hyperparameters | Method / Appendix | partial | `risk_adapter_v1` parameters are listed; verify all variants. |
| strict-valid metric definition | Experimental Setup | partial | Must state target-error, speed, swing, NaN/log-health, and manual criteria. |
| repeated-run seed / repeat convention | Experimental Setup | TODO | Record repeat naming and whether seeds are controlled or implicit. |
| generated figure paths | Results / Appendix | TODO | Link final Figure 3-6 and table asset paths once frozen. |

## Citation Risk Audit

### Claims That Require Citations Before Submission

- Suspended-payload UAV transport is difficult because of coupled load
  dynamics and payload swing.
- Strong wind or wind disturbance affects tracking, payload swing, and
  transport robustness.
- Payload-aware planning, MPC, and SO3 / geometric control are established
  components for this type of aerial transport stack.
- Reference governors, action governors, command filters, and runtime safety
  filters are relevant conceptual precedents.
- Learning-enhanced control or learned risk prediction is relevant to adaptive
  aerial robustness.
- Robotics benchmarking, stress testing, and repeated-run evaluation are
  appropriate for robustness claims.
- Failure taxonomy or failure-log analysis can support diagnosis.

### Claims Already Supported By Internal Experimental Results

- `windlevel_s085` is the single-goal specialist in the completed Stage 4
  single-goal protocol (`26/30`).
- `fixed_s080` is the goal-reissue stress specialist in the completed Stage 4
  stress protocol (`24/30`).
- `risk_adapter_v1` has the best mean valid count (`24.0/30`), best
  worst-protocol valid count (`23/30`), and lowest total regret (`2`) in the
  complete cross-protocol table.
- `risk_adapter_v21` is dominated by `risk_adapter_v1` in the two-protocol
  plane because both have `25/30` single-goal strict-valid runs, while
  `risk_adapter_v1` has higher stress performance (`23/30` versus `20/30`).

### Claims That Must Remain Caveated

- The governor improves balanced robustness only under the tested protocols.
- Failure groups are diagnostic labels, not definitive physical root-cause
  proof.
- Representative traces support mechanism hypotheses but do not prove
  population-level causality.
- The evaluation is simulation-only.
- The repeated-run counts are descriptive and do not imply statistical
  significance.
- The method is not a formal safety filter and provides no safety guarantee.

### Claims To Remove If Citations Are Not Found

- Any broad statement that suspended-payload UAV transport is important across
  specific application domains unless cited or reframed as motivation.
- Any general statement that wind disturbance is a dominant failure source in
  suspended-payload UAV transport unless cited or limited to this evaluation.
- Any claim that reference governors or safety filters are the direct ancestor
  of this method unless supported by appropriate citations.
- Any claim that learned risk prediction is established for this exact task
  unless specific supporting work is found.
- Any claim that protocol-split evaluation is standard practice unless
  supported by benchmarking / stress-testing references.

## Current Placeholder Inventory

Keep these as explicit TODO slots until exact references are verified:

- `[TODO: AutoTrans]`
- `[TODO: suspended-payload UAV planning]`
- `[TODO: payload-aware MPC]`
- `[TODO: SO3 / geometric quadrotor control]`
- `[TODO: wind-disturbance suspended-payload UAV transport]`
- `[TODO: reference governor]`
- `[TODO: explicit reference governor]`
- `[TODO: runtime safety filter]`
- `[TODO: action governor]`
- `[TODO: command filtering for robotics]`
- `[TODO: safety filters for learned control]`
- `[TODO: learning-enhanced UAV control]`
- `[TODO: learned risk prediction]`
- `[TODO: learned disturbance or risk prediction]`
- `[TODO: disturbance-aware learning for UAVs]`
- `[TODO: hybrid learning + model-based control]`
- `[TODO: data-driven robustness in aerial robotics]`
- `[TODO: robotics benchmarking]`
- `[TODO: stress testing for autonomous systems]`
- `[TODO: repeated-run robotics evaluation]`
- `[TODO: failure analysis / taxonomy]`
- `[TODO: failure log analysis]`

## Next Citation Work

Stage 4-AM should collect exact references and insert verified citation keys or
BibTeX entries. Until then, keep citation placeholders explicit and do not
fabricate author names, titles, venues, years, DOIs, or BibTeX.
