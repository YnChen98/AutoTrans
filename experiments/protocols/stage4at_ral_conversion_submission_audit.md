# Stage 4-AT RA-L Conversion And Submission Readiness Audit

## Executive Summary

Paper 1 target is RA-L. Stage 4-AT audits the conversion path from the current
IROS / ICRA-like scaffold to RA-L-oriented manuscript preparation.

No template conversion is performed in this task. The existing manuscript
source under `paper/stage4_governor/` is inspected as the current source
scaffold, but `main.tex`, `sections/*.tex`, `refs.bib`, `figures/*`, and
`tables/*` are not rewritten here.

No `risk_adapter_v22` should be created before Paper 1 RA-L submission unless
explicitly overridden. Paper 1 remains centered on `risk_adapter_v1` as the
balanced learned / risk-conditioned execution governor. `risk_adapter_v21`
remains a strong nominal / single-goal variant or ablation, not the final
method.

Paper 2 remains separate. It should be a later mechanism-driven extension
track rather than a lightly enlarged duplicate of Paper 1.

## Current Scaffold Inventory

Current scaffold root:

```text
paper/stage4_governor/
```

Current manuscript files:

- `paper/stage4_governor/main.tex`
- `paper/stage4_governor/refs.bib`
- `paper/stage4_governor/sections/01_intro.tex`
- `paper/stage4_governor/sections/02_related_work.tex`
- `paper/stage4_governor/sections/03_method.tex`
- `paper/stage4_governor/sections/04_experiments.tex`
- `paper/stage4_governor/sections/05_results.tex`
- `paper/stage4_governor/sections/06_discussion.tex`
- `paper/stage4_governor/sections/07_conclusion.tex`
- `paper/stage4_governor/supplementary/README.md`

Current figure assets:

- `paper/stage4_governor/figures/fig1_architecture.png`
- `paper/stage4_governor/figures/fig1_architecture.svg`
- `paper/stage4_governor/figures/fig2_protocol_split.png`
- `paper/stage4_governor/figures/fig2_protocol_split.svg`
- `paper/stage4_governor/figures/fig3_pareto.png`
- `paper/stage4_governor/figures/fig4_protocol_regret.png`
- `paper/stage4_governor/figures/fig5_invalid_failure_groups.png`
- `paper/stage4_governor/figures/fig6a_trial4_stress_v21_failure.png`
- `paper/stage4_governor/figures/fig6b_trial4_stress_comparison_fixed_s080.png`
- `paper/stage4_governor/figures/fig6c_trial4_stress_comparison_risk_adapter_v1.png`
- `paper/stage4_governor/figures/fig6d_trial6_single_goal_windlevel_s085.png`
- `paper/stage4_governor/figures/fig6e_trial6_single_goal_risk_adapter_v21_failure.png`

Current table assets:

- `paper/stage4_governor/tables/table1_protocol_balanced_robustness.tex`

Current scaffold status:

- The scaffold is under `paper/stage4_governor/`.
- The scaffold is IROS / ICRA-like.
- The scaffold is not yet RA-L template-specific.
- Stage 4-AT does not rewrite the scaffold; it records conversion and
  submission readiness gaps.

## RA-L Conversion Needs

RA-L conversion needs:

- Obtain the official/current RA-L template or IEEE journal template guidance.
- Decide whether to convert the current `ieeeconf`-style scaffold to a
  RA-L / `IEEEtran`-style journal manuscript.
- Adapt title, author, affiliation, abstract, and keyword structure to the
  target template.
- Check the current RA-L page limit and any supplementary / multimedia rules
  before deciding what stays in the main paper.
- Decide main-paper versus supplementary content for full run tables, extra
  traces, diagnostic audits, launch settings, and risk-score documentation.
- Check all figure widths and two-column layout behavior, especially Figures
  1-6.
- Convert Table 1 formatting if needed for RA-L / IEEE journal style.
- Confirm bibliography style, citation commands, and BibTeX compatibility with
  the official template.
- Remove conference-only assumptions, including `ieeeconf`-specific commands,
  conference submission wording, and any page-layout assumptions inherited from
  the IROS / ICRA-like scaffold.

## Paper 1 Must-Fix Before RA-L Submission

Must-fix items:

- Compile with the official RA-L / IEEE template.
- Finalize citation verification and BibTeX cleanup.
- Verify conditional citation metadata:
  - `Barikbin2019WindPayloadTracking`
  - `Wabersich2021PredictiveSafetyFilter`
  - `Jin2025NeuralPredictorPayload`
  - `Monteleone2023BalanceResilienceBenchmark`
  - `Dogga2023AutoARTS`
- Document `risk_score_3s` and `risk_score_5s` source, training data, feature
  windows, inference assumptions, inference rate, and calibration caveats.
  Stage 4-AU now addresses the adapter interface, logged fields, unavailable
  score behavior, governor usage, and metric boundary. Stage 4-AU2 now
  partially addresses model metadata by auditing the local generated JSONs,
  dataset row count, class counts, and feature schemas. Remaining TODOs are
  final artifact freezing / checksum, calibration method or no-calibration
  caveat, confidence / OOD behavior, and inference-latency measurement if
  claimed.
- Define the strict-valid metric clearly, including `label_strict_invalid`,
  target-error checks, speed/swing/log-health checks, and manual-invalid
  boundaries. Stage 4-AU now documents the Paper 1 strict-valid predicate and
  distinguishes it from diagnostic `failure_group` / `failure_mode_guess`
  labels.
- Polish Figure 6 as a readable multi-panel layout.
- Finalize captions for Table 1 and Figures 1-6.
- Run a final claim audit:
  - no statistical significance claim;
  - no formal safety guarantee;
  - no broad real-world deployment claim;
  - no learned-method uniform domination claim;
  - no `risk_adapter_v21` overall-best claim;
  - no mixed-protocol aggregate as the main result.
- Finalize supplementary plan.
- Resolve author and affiliation placeholders.

## Paper 1 Should-Fix If Time Allows

These items are optional for RA-L timing, but useful for stronger review:

- Paired or block statistical analysis over the repeated-run design.
- Fixed-scale frontier sweep summary beyond the current `fixed_s080` frontier
  reference.
- Channel ablation:
  - speed-only;
  - acceleration-only;
  - combined `speed_scale` / `acceleration_scale`.
- Risk ablation:
  - no-risk;
  - delayed-risk;
  - shuffled-risk.
- Efficiency metrics:
  - arrival time;
  - mission time;
  - peak swing;
  - peak speed;
  - time under low scale.
- `goal_repeat` curve for `1/3/5/10` if time allows.

These should-fix items should not delay Paper 1 indefinitely. If they cannot be
completed cleanly before RA-L timing, record them as limitations or future work
rather than creating `risk_adapter_v22`.

## Paper 2 Boundary

Paper 2 must not be a lightly extended duplicate of Paper 1.

Paper 2 needs a new central mechanism, such as:

- phase-aware final governor;
- failure-aware final governor;
- risk-health-aware final governor;
- reference-health-aware final governor;
- command-state-health-aware final governor.

Paper 2 should include:

- broader protocol family;
- wind / payload / cable / mission generalization;
- calibration and lead-time analysis;
- speed / acceleration / no-risk / delayed-risk / shuffled-risk ablations;
- optional HIL or minimal hardware if it supports the mechanism story.

Paper 2 should cite Paper 1 if Paper 1 is submitted or published. In Paper 2,
`risk_adapter_v1` can become the predecessor, reference method, or baseline
governor.

## Risk Register

| risk | why it matters | mitigation |
| --- | --- | --- |
| Simulation-only risk | Paper 1 cannot claim real-world deployment robustness. | Keep claims bounded to tested simulation protocols; frame hardware as future work or optional extension evidence. |
| Strong heuristic baseline risk | `windlevel_s085` and `fixed_s080` are strong protocol specialists. | Emphasize balanced robustness / protocol regret rather than universal learned-method domination. |
| Risk score source unclear | Reviewers may question `risk_score_3s` / `risk_score_5s` provenance and online meaning. | Stage 4-AU documents the adapter interface and metric boundary; Stage 4-AU2 audits local generated model metadata and feature schemas. Artifact freezing / checksum, calibration caveat, confidence / OOD behavior, and latency still need completion if claimed. |
| No statistical significance | Current repeated-run counts are descriptive. | Avoid significance wording; optionally add paired/block analysis if time allows. |
| No formal safety guarantee | The governor is empirical, not a certified safety filter. | Keep safety-filter wording out; state no formal safety guarantee. |
| Template/page-limit risk | RA-L conversion may force cuts or supplementary moves. | Audit page budget early and move detailed tables/traces to supplementary material. |
| Related work citation risk | Missing or conditional citation metadata can weaken positioning. | Complete BibTeX cleanup and conditional metadata verification before submission. |
| Paper 1 / Paper 2 overlap risk | A later extension could look like a duplicate if it lacks a new mechanism. | Require a mechanism-driven final governor and broader evaluation for Paper 2; cite Paper 1. |

## Recommended Next Stage

Recommended order after Stage 4-AU2:

1. Stage 4-AV: RA-L template acquisition and conversion.
2. Stage 4-AU3: risk calibration / lead-time plan, if the final RA-L claim
   needs calibration, confidence, OOD, or latency evidence.

Rationale: Stage 4-AU documents the current risk-score interface and
strict-valid metric, and Stage 4-AU2 documents the available local generated
model metadata. RA-L conversion will now expose formatting and page-budget
issues. If final risk documentation needs calibration, confidence, OOD, or
latency claims, add Stage 4-AU3 before making those claims.

Do not create `risk_adapter_v22` in Stage 4-AU2, Stage 4-AU3, or Stage 4-AV
unless there is an explicit override before Paper 1 RA-L submission.
