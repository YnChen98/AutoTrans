# Stage 4-AV RA-L Template Conversion Protocol

## Purpose

Stage 4-AV creates a separate RA-L-oriented Paper 1 manuscript scaffold from
the existing Stage 4 manuscript scaffold and the user-provided official
RA-L / IEEE template files.

This stage does not run LaTeX compile, simulation, RViz, `roslaunch`,
`catkin_make`, training scripts, or figure generation scripts. It does not
change scientific claims, numerical results, method rankings, citation
choices, figures, or tables. It does not create `risk_adapter_v22`.

Stage 4-AV2 now compiles/checks the RA-L-oriented scaffold created here:
`experiments/protocols/stage4av2_ral_scaffold_compile_check_result.md`.

## Input Scaffold

Source scaffold:

```text
paper/stage4_governor/
```

Key source files copied:

- `paper/stage4_governor/main.tex`
- `paper/stage4_governor/refs.bib`
- `paper/stage4_governor/sections/*.tex`
- `paper/stage4_governor/figures/*`
- `paper/stage4_governor/tables/table1_protocol_balanced_robustness.tex`
- `paper/stage4_governor/supplementary/README.md`

The source scaffold remains unchanged.

## Template Source

Template directory:

```text
paper/templates/ral/
```

Template files found:

- `paper/templates/ral/ieeeconf.cls`
- `paper/templates/ral/root.pdf`
- `paper/templates/ral/root.tex`

Likely main template file:

- `paper/templates/ral/root.tex`

Detected document class in `paper/templates/ral/root.tex`:

```tex
\documentclass[letterpaper, 10 pt, conference]{ieeeconf}
```

Required class/style/bibliography files present in the template directory:

- `ieeeconf.cls`

No `IEEEtran.cls`, `.sty`, or `.bst` files were found in the template
directory. The provided template appears to be `ieeeconf`-based rather than
`IEEEtran`-based.

The previous scaffold also had `paper/stage4_governor/ieeeconf.cls`, but the
RA-L scaffold uses the user-provided `paper/templates/ral/ieeeconf.cls`.

## Files Created

New scaffold root:

```text
paper/stage4_governor_ral/
```

Created files:

- `paper/stage4_governor_ral/README.md`
- `paper/stage4_governor_ral/main.tex`
- `paper/stage4_governor_ral/refs.bib`
- `paper/stage4_governor_ral/ieeeconf.cls`
- `paper/stage4_governor_ral/sections/01_intro.tex`
- `paper/stage4_governor_ral/sections/02_related_work.tex`
- `paper/stage4_governor_ral/sections/03_method.tex`
- `paper/stage4_governor_ral/sections/04_experiments.tex`
- `paper/stage4_governor_ral/sections/05_results.tex`
- `paper/stage4_governor_ral/sections/06_discussion.tex`
- `paper/stage4_governor_ral/sections/07_conclusion.tex`
- `paper/stage4_governor_ral/supplementary/README.md`
- `paper/stage4_governor_ral/tables/table1_protocol_balanced_robustness.tex`

## Main Template Adaptation

`paper/stage4_governor_ral/main.tex` preserves the source scaffold structure
and uses the detected template document class:

```tex
\documentclass[letterpaper, 10 pt, conference]{ieeeconf}
```

The scaffold keeps:

- title:
  "Risk-Conditioned Execution Governance for Balanced Robustness in Windy
  Suspended-Payload UAV Transport"
- author placeholder
- current cautious abstract
- section inputs:
  - `sections/01_intro`
  - `sections/02_related_work`
  - `sections/03_method`
  - `sections/04_experiments`
  - `sections/05_results`
  - `sections/06_discussion`
  - `sections/07_conclusion`
- bibliography using `refs.bib`

Only top-level template provenance comments were added to `main.tex`. No
scientific content was changed.

## Figures And Tables Copied

Figures copied into `paper/stage4_governor_ral/figures/`:

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

Table copied into `paper/stage4_governor_ral/tables/`:

- `table1_protocol_balanced_robustness.tex`

## Citation Boundary

`paper/stage4_governor_ral/refs.bib` was copied from the source scaffold.
Conditional citations without verified metadata were not added. Any future
conditional citation insertion should happen only after metadata verification.

## Claim Boundary

Stage 4-AV preserves the Paper 1 claim boundaries:

- no `risk_adapter_v21` overall-best claim;
- no mixed-protocol aggregate as the main result;
- no statistical significance claim;
- no formal safety guarantee;
- no broad real-world deployment claim;
- failure groups are diagnostic only;
- risk scores are empirical strict-invalid warning scores unless calibration
  is documented;
- no `risk_adapter_v22`.

## Remaining TODOs

- Confirm final RA-L / IEEE template requirements and page budget.
- Fill author names and affiliations.
- Use the Stage 4-AV2 compile/check result as the current RA-L scaffold
  compile baseline.
- Inspect the compiled PDF visually.
- Check Figure 6 readability under the RA-L-oriented scaffold.
- Verify conditional citation metadata and clean up BibTeX.
- Polish captions.
- Run final claim audit.
- Keep generated PDF / aux / log files out of git.

## Next Stage Recommendation

Original next recommended stage:

- Stage 4-AV2 RA-L scaffold compile/check pass.

After Stage 4-AV2, next recommended work is Stage 4-AM5 conditional citation
verification, Stage 4-AW final figure / caption polish, or Stage 4-AX final
claim audit depending on submission-readiness priority.

Do not create `risk_adapter_v22` before Paper 1 RA-L submission.
