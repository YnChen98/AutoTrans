# Stage 4-BA Display Name Cleanup Result

## Executive Summary

Stage 4-BA cleaned manuscript-visible method names in the RA-L Paper 1
scaffold under `paper/stage4_governor_ral/`. Raw underscore-style internal
method tokens were replaced in active prose, captions, panel labels, and
Table 1 visible method names with paper-facing display names.

The cleanup is presentation-only. It does not change numerical results,
rankings, figures, citations, algorithms, experiment outputs, or claim
boundaries. Figure-internal labels embedded inside existing image files were
not changed because no figures were regenerated in BA.

No simulation, training, ROS action, RViz, `catkin_make`, or figure generation
was run. No `risk_adapter_v22` was created.

## Display-Name Mapping Applied

| Internal token | Paper-facing display name |
| --- | --- |
| `original` | Original |
| `fixed_s085` | Fixed Scale 0.85 |
| `fixed_s080` | Fixed Scale 0.80 |
| `windlevel_s085` | Wind-Level 0.85 |
| `risk_adapter_v1` | Risk Adapter v1 |
| `risk_adapter_v2` | Risk Adapter v2 |
| `risk_adapter_v21` | Risk Adapter v2.1 |

## Files Inspected

- `paper/stage4_governor_ral/main.tex`
- `paper/stage4_governor_ral/sections/01_intro.tex`
- `paper/stage4_governor_ral/sections/02_related_work.tex`
- `paper/stage4_governor_ral/sections/03_method.tex`
- `paper/stage4_governor_ral/sections/04_experiments.tex`
- `paper/stage4_governor_ral/sections/05_results.tex`
- `paper/stage4_governor_ral/sections/06_discussion.tex`
- `paper/stage4_governor_ral/sections/07_conclusion.tex`
- `paper/stage4_governor_ral/tables/table1_protocol_balanced_robustness.tex`

## Files Changed

- `paper/stage4_governor_ral/main.tex`
- `paper/stage4_governor_ral/sections/01_intro.tex`
- `paper/stage4_governor_ral/sections/03_method.tex`
- `paper/stage4_governor_ral/sections/04_experiments.tex`
- `paper/stage4_governor_ral/sections/05_results.tex`
- `paper/stage4_governor_ral/sections/06_discussion.tex`
- `paper/stage4_governor_ral/sections/07_conclusion.tex`
- `paper/stage4_governor_ral/tables/table1_protocol_balanced_robustness.tex`

## Raw-Token Search Results After Cleanup

The post-cleanup search over active manuscript text and Table 1 was:

```bash
rg -n "risk_adapter_v1|risk_adapter_v2|risk_adapter_v21|risk\\_adapter\\_v1|risk\\_adapter\\_v2|risk\\_adapter\\_v21|windlevel_s085|windlevel\\_s085|fixed_s080|fixed\\_s080|fixed_s085|fixed\\_s085|\\boriginal\\b|\\texttt\\{original\\}" paper/stage4_governor_ral/main.tex paper/stage4_governor_ral/sections paper/stage4_governor_ral/tables/table1_protocol_balanced_robustness.tex
```

Remaining raw method-token matches are only file paths used by Figure 6
`\includegraphics` commands:

- `figures/fig6b_trial4_stress_comparison_fixed_s080.png`
- `figures/fig6c_trial4_stress_comparison_risk_adapter_v1.png`
- `figures/fig6d_trial6_single_goal_windlevel_s085.png`
- `figures/fig6e_trial6_single_goal_risk_adapter_v21_failure.png`

These are intentionally left raw because they are committed asset filenames
and this task does not rename files or regenerate figures.

## Cases Intentionally Left Raw

- Figure image filenames and `\includegraphics` paths.
- Code-facing parameter and field names such as `speed_scale`,
  `acceleration_scale`, `goal_repeat`, `risk_score_3s`, `risk_score_5s`,
  `risk_threshold_3s`, `risk_threshold_5s`, `hard_threshold_5s`,
  `soft_scale_3s`, `soft_scale_5s`, `hard_scale_5s`,
  `scale_rate_limit_per_sec`, `label_strict_invalid`,
  `command_risk_score_3s`, and `command_risk_score_5s`.
- Diagnostic field labels such as `failure_mode_guess`,
  `command_control_upstream`, `planner_reference_upstream`, and
  `state_task_upstream`.
- Internal implementation references in documentation or supplementary
  planning notes where raw IDs are useful for traceability.

## Compile Command and Result

Command run from `paper/stage4_governor_ral/`:

```bash
latexmk -pdf -interaction=nonstopmode -file-line-error main.tex
```

Result:

- `latexmk` exited successfully with status 0.
- `main.pdf` was generated during the check.
- Final log output: `Output written on main.pdf (8 pages, 2297201 bytes).`
- PDF size on disk: approximately 2.2 MB.

## Warning / Error Summary

Final `main.log` inspection found:

- LaTeX errors: none.
- Undefined citations: none in the final log.
- Undefined references: none in the final log.
- Overfull hboxes: 0.
- Missing figures: none.
- Bibliography warnings: none in the final log.
- Float warnings: none.
- Underfull hboxes: 25.
- Underfull vboxes: 3.

The remaining underfull boxes are non-blocking layout reminders.

## Remaining TODOs

- Figure 3 internal labels still need the Stage 4-BC compact polish / label
  cleanup.
- Figure 6 internal labels still need the Stage 4-BD simplified paper-facing
  replot plan.
- Figure 1 / Figure 2 still need the Stage 4-BB placeholder or redraw
  workflow.
- Final visual PDF inspection should be repeated after the figure-specific
  polish stages.

Continue: no `risk_adapter_v22` before Paper 1 RA-L submission.
