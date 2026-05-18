# Stage 4-AL Final Figure Generation Plan

## Executive Summary

Stage 4-AL is the final paper figure and table generation plan for the
assembled Stage 4 paper draft. It maps the current paper claims to the
figure/table assets, source generators, formatting expectations, and review
risks needed before producing final paper-ready figure files.

Stage 4-AL2 now implements the copy/check paper figure package generator:
`experiments/scripts/create_stage4_paper_figure_package.py`.
The protocol for that package generator is
`experiments/protocols/stage4al_paper_figure_package_protocol.md`.

No figures are generated in this task. No figure-generation scripts should be
run here, and no generated PNG/PDF/SVG/CSV/TXT/MD outputs should be created or
staged.

The paper remains framed around risk-conditioned execution governance for
suspended-payload UAV transport under strong wind, protocol-split robustness
evaluation, balanced robustness / protocol regret analysis, and
failure-mode-aware diagnosis.

`risk_adapter_v1` remains the balanced learned / risk-conditioned protagonist.
`risk_adapter_v21` remains a strong nominal / single-goal variant or ablation,
not the final cross-protocol method. `risk_adapter_v22` is not part of this
figure plan and should not be introduced before a mechanism-driven justification
exists.

## Main Paper Figure/Table Inventory

### Table 1: Protocol-Split Success And Balanced Robustness

Source assets:

- `experiments/results/stage4_balanced_robustness_assets/stage4_balanced_robustness_table.md`
- `experiments/results/stage4_balanced_robustness_assets/stage4_protocol_regret_table.md`

Source generator:

- `experiments/scripts/generate_stage4_balanced_robustness_assets.py`

Purpose:

- Support `risk_adapter_v1` as the balanced learned / risk-conditioned
  protagonist.
- Show `windlevel_s085` as the single-goal specialist.
- Show `fixed_s080` as the goal-reissue stress specialist.
- Keep `risk_adapter_v21` as a strong nominal / single-goal variant that is
  weaker under stress.

Caveat:

- These are descriptive repeated-run counts, not statistical significance
  results and not safety guarantees.

Main-paper content:

| method | single-goal strict-valid | goal-reissue stress strict-valid | mean valid | worst-protocol valid | total regret | method role |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `original` | `21/30` | `18/30` | `19.5/30` | `18/30` | `11` | unadapted baseline |
| `fixed_s085` | `22/30` | `18/30` | `20.0/30` | `18/30` | `10` | fixed static baseline |
| `windlevel_s085` | `26/30` | `16/30` | `21.0/30` | `16/30` | `8` | single-goal specialist heuristic |
| `fixed_s080` | `21/30` | `24/30` | `22.5/30` | `21/30` | `5` | goal-reissue stress specialist static frontier |
| `risk_adapter_v1` | `25/30` | `23/30` | `24.0/30` | `23/30` | `2` | balanced learned / risk-conditioned governor |
| `risk_adapter_v21` | `25/30` | `20/30` | `22.5/30` | `20/30` | `5` | strong nominal / single-goal learned variant |

### Figure 1: System Architecture Schematic

Type:

- Manually drawn / future generated schematic.

Content:

- AutoTrans-like planner.
- Payload MPC.
- SO3 controller.
- External risk-conditioned execution governor.
- `speed_scale` / `acceleration_scale` interface.
- Risk input.

Purpose:

- Explain the stack-compatible governor interface.
- Show that the governor is external to the planner, payload MPC, and SO3
  controller.

Caveat:

- The architecture is an empirical execution-governor interface, not a formal
  safety filter and not a certified runtime assurance layer.

Preferred paper-ready name:

- `fig1_architecture`

### Figure 2: Protocol Split Schematic

Type:

- Manually drawn / future generated schematic.

Content:

- Single-goal mission protocol, `goal_repeat=1`.
- Goal-reissue stress protocol, `goal_repeat=10`.
- Visual explanation that the two protocols test different system behavior and
  should be reported separately.

Purpose:

- Justify protocol-split reporting.
- Prevent a misleading mixed-protocol aggregate.

Caveat:

- The schematic defines evaluation regimes; it does not rank methods by
  itself.

Preferred paper-ready name:

- `fig2_protocol_split`

### Figure 3: Balanced Robustness / Pareto Frontier

Source asset:

- `experiments/results/stage4_balanced_robustness_assets/stage4_balanced_robustness_pareto.png`

Source generator:

- `experiments/scripts/generate_stage4_balanced_robustness_assets.py`

Purpose:

- Show the observed Pareto frontier:
  - `windlevel_s085`
  - `fixed_s080`
  - `risk_adapter_v1`
- Show that `risk_adapter_v21` is dominated by `risk_adapter_v1` because both
  have `25/30` single-goal strict-valid runs, while `risk_adapter_v1` has
  `23/30` stress strict-valid runs and `risk_adapter_v21` has `20/30`.

Caveat:

- Pareto-frontier status is relative to the tested methods and the two tested
  protocols only.

Preferred paper-ready name:

- `fig3_pareto`

### Figure 4: Protocol Regret Bar Chart

Source asset:

- `experiments/results/stage4_balanced_robustness_assets/stage4_protocol_regret_bar.png`

Source generator:

- `experiments/scripts/generate_stage4_balanced_robustness_assets.py`

Purpose:

- Show that `risk_adapter_v1` has the lowest total regret (`2`).
- Make the trade-off between protocol specialists visible.

Caveat:

- Protocol oracle means observed best method in the current evaluation, not a
  theoretical optimum.

Preferred paper-ready name:

- `fig4_protocol_regret`

### Figure 5: Invalid-Only Failure Group Stacked Bar

Source asset:

- `experiments/results/stage4_failure_mode_paper_assets/stage4_failure_group_invalid_only_stacked_bar.png`

Source generator:

- `experiments/scripts/generate_stage4_failure_mode_paper_assets.py`

Purpose:

- Show heterogeneous invalid-run patterns.
- Support failure-mode-aware evaluation.
- Keep the paper's failure analysis focused on invalid-only diagnostic groups.

Caveat:

- `failure_group` labels are diagnostic categories, not exact physical
  root-cause proof.

Preferred paper-ready name:

- `fig5_invalid_failure_groups`

### Figure 6: Representative Trace Case Study

Source assets:

- `experiments/results/stage4_representative_traces/plots/*.png`

Source generator:

- `experiments/scripts/plot_stage4_representative_failure_traces.py`

Suggested panels:

- Trial 4 goal-reissue stress: `risk_adapter_v21` failed run compared with
  `fixed_s080` and `risk_adapter_v1` successes.
- Trial 6 single-goal: `windlevel_s085` / `fixed_s080` successes compared
  with `risk_adapter_v1` / `risk_adapter_v21` bottleneck traces.

Purpose:

- Illustrate mechanism hypotheses from Stage 4-AA3.
- Show that Trial 4 stress `risk_adapter_v21` failures include early
  pre-arrival vulnerability and possible risk availability/timing issues.
- Show that lower scale is not automatically safer in the Trial 6 single-goal
  bottleneck.

Caveat:

- Representative traces are qualitative case studies, not proof of general
  causality.

Preferred paper-ready name:

- `fig6_representative_traces`

## Appendix / Supplementary Asset Inventory

Include these assets outside the main paper body:

- Full protocol-split success tables.
- Full per-trial success tables.
- Full balanced robustness tables.
- Failure-mode count tables.
- All-run failure group table.
- Invalid-only failure group table.
- Representative trace index.
- Additional representative traces.
- Method hyperparameter table.
- Launch settings.
- Strict-valid metric definition.
- Duplicate CSV audit notes if needed.
- `risk_adapter_v2` single-goal-only note.

These supplementary assets should support auditability without moving long raw
diagnostic tables into the main paper.

## Figure Generation Order

Do not execute these steps in this task. This order is for Stage 4-AL2 or a
manual figure package pass.

1. Regenerate protocol-split and balanced robustness assets.
2. Regenerate failure-mode assets.
3. Regenerate representative trace assets.
4. Create paper-ready copies under a future output directory such as
   `experiments/results/stage4_paper_figure_package`.
5. Create manual schematic drafts for Figure 1 and Figure 2.
6. Check captions and claim alignment against the assembled paper draft,
   citation plan, and claim audit.

## Formatting Requirements

- Use consistent figure/table naming:
  - `fig1_architecture`
  - `fig2_protocol_split`
  - `fig3_pareto`
  - `fig4_protocol_regret`
  - `fig5_invalid_failure_groups`
  - `fig6_representative_traces`
- Prefer vector PDF/SVG for schematic figures if possible.
- Use high-resolution PNG for plots if vector output is unavailable.
- Keep font sizes readable for IROS/ICRA/RA-L two-column format.
- Avoid excessive raw diagnostic labels in main figures.
- Put long tables in the appendix.
- Ensure all plots have explicit protocol labels.
- Keep method colors and labels consistent across Table 1 and Figures 3-6.
- Preserve source-data traceability from every paper-ready figure to its
  generated asset or protocol document.

## Claim Mapping Table

| figure_or_table | supported claim | caveat | source asset | paper section |
| --- | --- | --- | --- | --- |
| Table 1 | `risk_adapter_v1` is the most balanced learned / risk-conditioned method in the current two-protocol evaluation. | Descriptive counts only; no statistical significance or safety guarantee. | `experiments/results/stage4_balanced_robustness_assets/stage4_balanced_robustness_table.md` and `experiments/results/stage4_balanced_robustness_assets/stage4_protocol_regret_table.md` | Results |
| Figure 1 | The method is a stack-compatible execution governor using `speed_scale` and `acceleration_scale`. | Not a formal safety filter or planner/controller replacement. | Future schematic | Method |
| Figure 2 | The single-goal and goal-reissue stress protocols test different behavior and require separate reporting. | Does not rank methods by itself; no mixed-protocol aggregate. | Future schematic | Experimental Setup |
| Figure 3 | `windlevel_s085`, `fixed_s080`, and `risk_adapter_v1` form the observed Pareto frontier; `risk_adapter_v21` is dominated by `risk_adapter_v1`. | Frontier is limited to evaluated methods and protocols. | `experiments/results/stage4_balanced_robustness_assets/stage4_balanced_robustness_pareto.png` | Results |
| Figure 4 | `risk_adapter_v1` has the lowest total regret relative to observed protocol oracles. | Observed oracle is not a theoretical optimum. | `experiments/results/stage4_balanced_robustness_assets/stage4_protocol_regret_bar.png` | Results |
| Figure 5 | Invalid-only failure groups reveal heterogeneous invalid-run patterns. | Diagnostic labels are not exact physical root-cause proof. | `experiments/results/stage4_failure_mode_paper_assets/stage4_failure_group_invalid_only_stacked_bar.png` | Failure Analysis |
| Figure 6 | Representative traces illustrate the mechanism hypotheses behind stress weakness and single-goal bottlenecks. | Qualitative case study only; not general causal proof. | `experiments/results/stage4_representative_traces/plots/*.png` | Failure Analysis or Results |

## Missing Asset / Risk Table

| missing asset or risk | impact | planned handling |
| --- | --- | --- |
| Figure 1 architecture schematic not yet generated | Method interface may remain abstract. | Create schematic in Stage 4-AL2 or manual figure package pass. |
| Figure 2 protocol schematic not yet generated | Protocol split may be harder to understand quickly. | Create schematic before final paper assembly. |
| Figure 6 needs manual multi-panel selection / layout | Trace figure could become too large or unfocused. | Select one Trial 4 stress contrast and one Trial 6 single-goal contrast. |
| Final captions need polishing | Captions may overclaim or repeat text. | Audit captions against the claim mapping table. |
| Citation placeholders still unresolved by Stage 4-AM | Figure-supported claims may lack external framing citations. | Run Stage 4-AM2 verified citation collection in parallel. |
| Final paper image directory not created | Paper-ready assets may remain scattered across result directories. | Use a future directory such as `experiments/results/stage4_paper_figure_package`. |
| No final LaTeX/Word paper yet | Final sizing and figure order may shift. | Treat this plan as a package contract before manuscript formatting. |

## What Not To Do

- Do not generate new experimental runs.
- Do not run figure generation scripts in this planning task.
- Do not create or introduce `risk_adapter_v22`.
- Do not use mixed-protocol aggregate figures.
- Do not put giant raw failure tables in the main paper.
- Do not claim statistical significance from plots.
- Do not claim failure groups prove root cause.
- Do not frame `risk_adapter_v21` as the final cross-protocol method.
- Do not replace citation placeholders with unverified references.

## Next Step Recommendation

Recommended next step:

- Stage 4-AL2: paper figure package generation script or manual figure package
  checklist. This is now implemented by
  `experiments/scripts/create_stage4_paper_figure_package.py`.

Alternative parallel step:

- Stage 4-AM2: verified citation collection.

Do not recommend new simulation, new experimental runs, or `risk_adapter_v22`
before the paper figure package and citation slots are reviewed.
