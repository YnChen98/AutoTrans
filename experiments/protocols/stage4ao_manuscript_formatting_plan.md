# Stage 4-AO Manuscript Formatting Plan

## Executive Summary

Stage 4-AO is the manuscript formatting / source-scaffold plan for converting
the assembled Stage 4 paper draft into a future manuscript source tree. This
stage defines the intended directory layout, source inputs, section placement,
figure/table placement, citation handling, and claim boundaries before any
manuscript files are created.

This task does not create LaTeX files, BibTeX files, a `paper/` directory, a
`manuscript/` directory, or any final figure/table files. It prepares for a
later Stage 4-AP manuscript source scaffold.

The current paper framing remains:

- risk-conditioned execution governance,
- suspended-payload UAV transport under strong wind,
- protocol-split robustness evaluation,
- balanced robustness / protocol regret analysis,
- failure-mode-aware diagnosis.

`risk_adapter_v1` remains the tentative balanced learned / risk-conditioned
protagonist. `risk_adapter_v21` remains an ablation / strong nominal variant,
not the final method. Do not create `risk_adapter_v22`.

## Target Venue Format Options

The final venue target is not locked yet. The manuscript scaffold should keep
the following options open:

- IROS / ICRA conference-style LaTeX.
- RA-L journal style.
- A conference-first draft that can later be expanded toward RA-L if the paper
  needs additional space for method details, failure analysis, or appendices.

Recommended starting point:

- Use an IROS / ICRA-like conference skeleton for initial drafting.
- Keep section files modular so the same text can later be adapted to RA-L.
- Avoid venue-specific formatting decisions that are hard to reverse until the
  final target is confirmed.

## Proposed Manuscript Directory Layout

Future scaffold example:

```text
paper/stage4_governor/
  main.tex
  sections/
    01_intro.tex
    02_related_work.tex
    03_method.tex
    04_experiments.tex
    05_results.tex
    06_discussion.tex
    07_conclusion.tex
  figures/
  tables/
  refs.bib
  supplementary/
```

Notes:

- Do not create this layout in Stage 4-AO.
- Before Stage 4-AP, confirm that no existing `paper/` or `manuscript/`
  directory would be overwritten.
- Keep `figures/`, `tables/`, and `supplementary/` separate so generated
  assets can be copied intentionally from `experiments/results/` without
  committing raw experiment outputs.

## Source Inputs

| manuscript component | source documents / assets | use |
| --- | --- | --- |
| Abstract / Introduction | `experiments/protocols/stage4af_abstract_introduction_draft.md`, `experiments/protocols/stage4aj_full_paper_assembly_draft.md` | Seed `main.tex` abstract and `sections/01_intro.tex`. |
| Method | `experiments/protocols/stage4ag_method_section_draft.md`, `experiments/protocols/stage4aj_full_paper_assembly_draft.md` | Seed `sections/03_method.tex`. |
| Results | `experiments/protocols/stage4ah_results_section_draft.md`, `experiments/protocols/stage4aj_full_paper_assembly_draft.md` | Seed `sections/05_results.tex`. |
| Discussion / Limitations | `experiments/protocols/stage4ai_discussion_limitations_draft.md`, `experiments/protocols/stage4aj_full_paper_assembly_draft.md` | Seed `sections/06_discussion.tex`. |
| Figure package | `experiments/results/stage4_paper_figure_package/` | Source final paper figures and tables after a deliberate copy into the manuscript scaffold. |
| Citation keys | `experiments/protocols/stage4am4_bibtex_draft.md` | Provisional source for ready-to-use BibTeX blocks. |
| Figure plan | `experiments/protocols/stage4al_final_figure_generation_plan.md` | Figure/table placement and caveat alignment. |

## Main Paper Section Plan

### Abstract

- Use the Stage 4-AF / AJ abstract as the initial source.
- Keep the abstract concise and citation-light or citation-free depending on
  target venue style.
- State balanced robustness under tested protocols, not broad real-world
  deployment robustness.

### 1. Introduction

- Convert Stage 4-AF / AJ introduction paragraphs into `sections/01_intro.tex`.
- Preserve the contribution bullets:
  - drop-in learned / risk-conditioned execution governor,
  - protocol-split robustness evaluation,
  - balanced robustness / protocol regret analysis,
  - failure-mode-aware diagnostic workflow.
- Add citations using the Stage 4-AM3 insertion guidance and AM4 keys.

### 2. Related Work

- Convert the AJ Related Work skeleton into a concise section.
- Use four subsections:
  - Suspended-payload UAV transport and control.
  - Runtime governors / reference governors / safety filters.
  - Learning-enhanced aerial robustness.
  - Benchmarking, stress testing, and failure analysis.
- Keep conditional citations out until their metadata is verified.

### 3. Method

- Use Stage 4-AG / AJ as the source.
- Focus on the stack-compatible execution-governor interface.
- Include `speed_scale` and `acceleration_scale`.
- Keep the claim boundary clear: empirical governor, not certified safety
  filter, not planner/MPC/controller replacement.

### 4. Experimental Setup

- Define the simulator / AutoTrans-like stack, strong wind setting, suspended
  payload task, Trials 4/5/6, strict-valid metric, protocol definitions,
  method list, repeated-run design, and diagnostic logging.
- Place Figure 2 near the protocol definition.
- Avoid a mixed-protocol aggregate.

### 5. Results

- Use Stage 4-AH / AJ as the source.
- Organize around protocol-split success, balanced robustness / regret,
  invalid-only failure groups, and representative traces.
- Place Table 1 and Figures 3-6 here.

### 6. Discussion And Limitations

- Use Stage 4-AI / AJ as the source.
- Emphasize why protocol split matters, why strong baselines matter, why
  balanced robustness is the correct criterion, and why `risk_adapter_v22` is
  not introduced.
- Include simulation-only, no safety guarantee, no statistical significance,
  and diagnostic-label limitations.

### 7. Conclusion

- Use the AJ conclusion draft as the seed.
- Restate the risk-conditioned execution-governor framing.
- Summarize protocol-specialist vs balanced-governor findings.
- Avoid overclaiming learned dominance or certified safety.

## Figure / Table Placement Plan

| item | manuscript placement | source / package path | purpose |
| --- | --- | --- | --- |
| Figure 1 architecture | Method | `experiments/results/stage4_paper_figure_package/main/fig1_architecture.png` / `.svg` | Explain stack-compatible governor interface. |
| Figure 2 protocol split | Experimental Setup | `experiments/results/stage4_paper_figure_package/main/fig2_protocol_split.png` / `.svg` | Explain `goal_repeat=1` vs `goal_repeat=10`. |
| Table 1 protocol + balanced robustness | Results | `experiments/results/stage4_paper_figure_package/main/table1_protocol_balanced_robustness.md` | Support `risk_adapter_v1` as balanced protagonist and baselines as specialists. |
| Figure 3 Pareto frontier | Results | `experiments/results/stage4_paper_figure_package/main/fig3_pareto.png` | Show observed two-protocol Pareto frontier. |
| Figure 4 protocol regret | Results | `experiments/results/stage4_paper_figure_package/main/fig4_protocol_regret.png` | Show `risk_adapter_v1` lowest total regret. |
| Figure 5 invalid-only failure groups | Results / Failure Analysis | `experiments/results/stage4_paper_figure_package/main/fig5_invalid_failure_groups.png` | Show heterogeneous invalid-run diagnostic groups. |
| Figure 6 representative traces | Results / Failure Analysis | `experiments/results/stage4_paper_figure_package/main/fig6*.png` | Illustrate Trial 4 stress and Trial 6 bottleneck mechanisms. |

Figure placement caveats:

- Figure 1 is not a certified safety-filter claim.
- Figure 2 is explanatory and not a result plot.
- Figures 3-4 are based on tested protocols only.
- Figure 5 labels are diagnostic, not exact physical root-cause proof.
- Figure 6 is qualitative case evidence, not proof of general causality.

## Supplementary Plan

Future supplementary material should include:

- full run tables,
- full protocol split summaries,
- all representative trace plots,
- failure mode tables,
- launch settings,
- strict-valid definition,
- `risk_adapter_v1` parameters,
- `risk_adapter_v2` single-goal-only note,
- duplicate CSV audit notes if included.

Supplementary content should preserve the same claim boundaries as the main
paper and should not introduce `risk_adapter_v22`.

## Citation / BibTeX Plan

- Use ready-to-use BibTeX draft blocks from
  `experiments/protocols/stage4am4_bibtex_draft.md` as the provisional source.
- Do not insert conditional entries until their metadata is verified.
- Resolve conditional entries before submission:
  - `Barikbin2019WindPayloadTracking`,
  - `Wabersich2021PredictiveSafetyFilter`,
  - `Jin2025NeuralPredictorPayload`,
  - `Monteleone2023BalanceResilienceBenchmark`,
  - `Dogga2023AutoARTS`.
- Check the final venue style before creating `refs.bib`.
- Compile with the target venue template later, not in Stage 4-AO.

## Manuscript Claim Boundaries

The manuscript scaffold should preserve these boundaries:

- no `risk_adapter_v21` overall-best claim,
- no mixed-protocol aggregate as the main result,
- no statistical significance claim,
- no safety guarantee,
- no real-world deployment claim,
- failure groups are diagnostic only,
- no learned uniform domination over heuristic / static baselines,
- no `risk_adapter_v22`.

## Stage 4-AP Readiness Checklist

Before creating the actual manuscript scaffold:

- Push latest commit if the team wants the scaffold based on a remote-visible
  branch state.
- Confirm target manuscript directory, defaulting to
  `paper/stage4_governor/` only if no conflict exists.
- Confirm no existing `paper/` or `manuscript/` directory will be overwritten.
- Confirm target style, defaulting to an IROS / ICRA-like draft skeleton.
- Confirm generated figures are present in
  `experiments/results/stage4_paper_figure_package/`.
- Confirm draft BibTeX from Stage 4-AM4 is acceptable as provisional.
- Confirm whether conditional citations should be verified first through
  Stage 4-AM5.

## Next Step Recommendation

Recommended next step:

- Stage 4-AP: create manuscript source scaffold.

Alternative next step:

- Stage 4-AM5: verify remaining conditional citations before creating or
  finalizing `refs.bib`.

Do not recommend new simulation, new experimental runs, or `risk_adapter_v22`.
