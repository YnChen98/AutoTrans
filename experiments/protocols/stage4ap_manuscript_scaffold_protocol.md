# Stage 4-AP Manuscript Scaffold Protocol

## Purpose

Stage 4-AP creates the first manuscript source scaffold for the reframed Stage
4 paper. The scaffold converts the Stage 4-AJ assembled draft, the Stage 4-AL3
figure package, and the Stage 4-AM4 ready-to-use BibTeX draft into a local
IROS / ICRA-like manuscript source tree.

This stage does not run LaTeX compilation, does not run simulation, does not
run figure-generation scripts, and does not introduce `risk_adapter_v22`.

## Created Files

The scaffold is created under:

`paper/stage4_governor/`

Created source files:

- `paper/stage4_governor/README.md`
- `paper/stage4_governor/main.tex`
- `paper/stage4_governor/refs.bib`
- `paper/stage4_governor/sections/01_intro.tex`
- `paper/stage4_governor/sections/02_related_work.tex`
- `paper/stage4_governor/sections/03_method.tex`
- `paper/stage4_governor/sections/04_experiments.tex`
- `paper/stage4_governor/sections/05_results.tex`
- `paper/stage4_governor/sections/06_discussion.tex`
- `paper/stage4_governor/sections/07_conclusion.tex`
- `paper/stage4_governor/tables/table1_protocol_balanced_robustness.tex`
- `paper/stage4_governor/supplementary/README.md`

Created asset directories:

- `paper/stage4_governor/figures/`
- `paper/stage4_governor/tables/`
- `paper/stage4_governor/supplementary/`

## Source Inputs

- Full paper assembly:
  `experiments/protocols/stage4aj_full_paper_assembly_draft.md`
- Manuscript formatting plan:
  `experiments/protocols/stage4ao_manuscript_formatting_plan.md`
- Figure package:
  `experiments/results/stage4_paper_figure_package/main/`
- Ready-to-use BibTeX draft:
  `experiments/protocols/stage4am4_bibtex_draft.md`
- Citation insertion guidance:
  `experiments/protocols/stage4am3_citation_insertion_draft.md`

## Copied Assets

The scaffold copies these main-paper figure assets into
`paper/stage4_governor/figures/`:

- `fig1_architecture.png`
- `fig1_architecture.svg`
- `fig2_protocol_split.png`
- `fig2_protocol_split.svg`
- `fig3_pareto.png`
- `fig4_protocol_regret.png`
- `fig5_invalid_failure_groups.png`
- `fig6a_trial4_stress_v21_failure.png`
- `fig6b_trial4_stress_comparison_fixed_s080.png`
- `fig6c_trial4_stress_comparison_risk_adapter_v1.png`
- `fig6d_trial6_single_goal_windlevel_s085.png`
- `fig6e_trial6_single_goal_risk_adapter_v21_failure.png`

No files under `experiments/results/` should be staged or committed by this
stage.

## Claim Boundaries

The scaffold preserves the Stage 4 claim boundaries:

- no `risk_adapter_v21` overall-best claim,
- no mixed-protocol aggregate as the main result,
- no statistical significance claim,
- no safety guarantee,
- no real-world deployment claim,
- failure groups are diagnostic only,
- no learned uniform domination over heuristic / static baselines,
- no `risk_adapter_v22`.

## Citation Boundary

`paper/stage4_governor/refs.bib` contains only ready-to-use BibTeX blocks from
Stage 4-AM4. Conditional citation keys remain TODO comments and are not active
BibTeX entries:

- `Barikbin2019WindPayloadTracking`
- `Wabersich2021PredictiveSafetyFilter`
- `Jin2025NeuralPredictorPayload`
- `Monteleone2023BalanceResilienceBenchmark`
- `Dogga2023AutoARTS`

## No Compile Was Run

Stage 4-AP does not run LaTeX compilation. The scaffold is expected to need a
later compile/check pass after the template, packages, figure sizing, and table
formatting are confirmed.

Stage 4-AQ attempted the first LaTeX compile/check pass, but the local
environment did not provide `latexmk`, `pdflatex`, or `bibtex`, so compilation
could not start:
`experiments/protocols/stage4aq_latex_compile_check_result.md`.

## Next Steps

Recommended next step:

- Stage 4-AQ2 or Stage 4-AR: rerun LaTeX compile/check in an environment with
  the required LaTeX tools installed, then fix manuscript-formatting issues.

Alternative next step:

- Stage 4-AM5: conditional citation verification before final bibliography
  cleanup.

Do not run new simulation and do not create `risk_adapter_v22`.
