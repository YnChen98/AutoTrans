# Stage 4-BC Figure 3 Compact Polish Result

## Executive Summary

Stage 4-BC regenerates Figure 3 for the RA-L Paper 1 scaffold as a compact
paper-facing Pareto frontier plot. The new plot uses display names, reduced
whitespace, no raw underscore labels, no redundant in-plot title, and marker
styles that do not rely on color alone.

This is a figure-presentation pass only. It does not change scientific claims,
numerical results, rankings, citations, Table 1 data, algorithms, or
experiment outputs. No new experiments were run.

No simulation, training, ROS action, RViz, or `catkin_make` was run. No
`risk_adapter_v22` was created.

## Old Issue From AZ

Stage 4-AZ found that Figure 3 content was acceptable but visually too sparse:

- redundant in-plot title;
- raw token labels;
- canvas too large for the small number of points;
- labels and markers not paper-facing enough.

Stage 4-BC addresses these Figure 3-specific presentation issues.

## Script Added

Added:

```text
experiments/scripts/generate_stage4_paper_ready_pareto.py
```

The script:

- uses Python / matplotlib only;
- does not use seaborn;
- does not require ROS;
- does not read or write `experiments/results/`;
- hard-codes the final Table 1 counts used by the active manuscript;
- writes directly to the RA-L scaffold figure directory.

Commands run:

```bash
python3 -m py_compile experiments/scripts/generate_stage4_paper_ready_pareto.py
python3 experiments/scripts/generate_stage4_paper_ready_pareto.py
```

Both commands succeeded.

## Generated Files

- `paper/stage4_governor_ral/figures/fig3_pareto.png`
- `paper/stage4_governor_ral/figures/fig3_pareto.svg`

The regenerated PNG is `1890 x 1344` pixels. The SVG was generated with
editable text (`svg.fonttype=none`).

## Data Values Used

| Method | Single-goal | Goal-reissue stress | Frontier |
| --- | ---: | ---: | --- |
| Original | 21 | 18 | no |
| Fixed 0.85 | 22 | 18 | no |
| Wind-Level 0.85 | 26 | 16 | yes |
| Fixed 0.80 | 21 | 24 | yes |
| Risk Adapter v1 | 25 | 23 | yes |
| Risk Adapter v2.1 | 25 | 20 | no |

These values match the active Table 1 counts. Risk Adapter v2.1 remains
non-frontier because it ties Risk Adapter v1 in the single-goal protocol but
has lower goal-reissue stress count.

## Display-Name Mapping

The generated image uses only paper-facing labels:

- Original
- Fixed 0.85
- Wind-Level 0.85
- Fixed 0.80
- Risk Adapter v1
- Risk Adapter v2.1

No raw underscore method tokens appear in the SVG text.

## Plot-Style Changes

- Removed the redundant in-plot title.
- Tightened the visible x-axis range to `20.5` through `26.5`.
- Tightened the visible y-axis range to `15.5` through `24.5`.
- Used direct labels for every method.
- Used diamond markers for frontier methods and hollow circle markers for
  other evaluated methods.
- Added a concise legend above the plot.
- Used a light grid and compact single-column-oriented dimensions.
- Avoided statistical-significance or theoretical-optimum implications.

## Caption Changes

Updated the Figure 3 caption in
`paper/stage4_governor_ral/sections/05_results.tex` to state that:

- Figure 3 is the balanced robustness / Pareto frontier across the two tested
  protocols;
- the x-axis is single-goal strict-valid count / 30;
- the y-axis is goal-reissue stress strict-valid count / 30;
- the observed frontier contains Wind-Level 0.85, Fixed Scale 0.80, and Risk
  Adapter v1;
- the frontier is limited to evaluated methods and protocols.

## Compile Command and Result

Command run from `paper/stage4_governor_ral/`:

```bash
latexmk -pdf -interaction=nonstopmode -file-line-error main.tex
```

Result:

- Compile succeeded with exit status 0.
- `main.pdf` was generated during the check.
- Final log output: `Output written on main.pdf (8 pages, 1463685 bytes).`
- LaTeX errors: none.
- Undefined citations / references: none in the final log.
- Overfull hboxes: 0.
- Missing figures: none.
- Bibliography warnings: none in the final log.
- Float warnings: none.
- Underfull hboxes: 25.
- Underfull vboxes: 1.

Generated LaTeX PDF / aux / log files were excluded from git.

## Remaining TODOs

- Stage 4-BD Figure 6 simplified paper-facing replot.
- Later Stage 4-BE Figure 1 / Figure 2 external schematic replacement after
  the placeholder workflow.

Continue: no `risk_adapter_v22` before Paper 1 RA-L submission.
