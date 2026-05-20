# Stage 4-BE Schematic Vector Replacement Result

## Executive Summary

Stage 4-BE replaces the active Figure 1 / Figure 2 placeholder boxes in the
RA-L Paper 1 scaffold with clean TikZ vector schematics. The old generated
Figure 1 / Figure 2 PNG/SVG assets remain unchanged but are no longer active
main-paper visuals.

This is a presentation-readiness step only. It does not change scientific
claims, numerical results, method rankings, citations, Table 1, algorithms, or
experiment outputs.

## Why Placeholders Were Replaced

Stage 4-BB made the manuscript visually honest by replacing low-quality
generated schematics with placeholder boxes. Stage 4-BE completes the next
presentation step by replacing those placeholders with editable vector
schematics built directly in LaTeX / TikZ.

## Files Added

Added TikZ source files:

```text
paper/stage4_governor_ral/figures/fig1_architecture_tikz.tex
paper/stage4_governor_ral/figures/fig2_protocol_split_tikz.tex
```

Updated active manuscript files:

```text
paper/stage4_governor_ral/main.tex
paper/stage4_governor_ral/sections/03_method.tex
paper/stage4_governor_ral/sections/04_experiments.tex
```

`main.tex` now loads TikZ with:

```tex
\usepackage{tikz}
\usetikzlibrary{arrows.meta,positioning,fit,calc}
```

## Figure 1 Design Summary

Figure 1 now shows:

- Planner / reference generator;
- Payload MPC;
- SO(3) controller;
- UAV + suspended payload;
- Risk input / warning scores;
- Risk-conditioned execution governor;
- Command-adaptation interface;
- Diagnostics / logs.

The main command path remains Planner / reference generator -> Payload MPC ->
SO(3) controller -> UAV + suspended payload. A dashed adaptation arrow shows
the command-adaptation interface acting on the execution command path through
speed scale and acceleration scale. Dotted feedback arrows show logs / plant
signals feeding warning scores and diagnostics.

The figure explicitly labels the unchanged inner stack and empirical governor,
without implying a certified safety filter or a formal safety guarantee.

## Figure 2 Design Summary

Figure 2 now uses two side-by-side timeline panels:

- Single-goal mission: one goal publish marker, transport interval, arrival /
  hold marker, and `goal repeat = 1`.
- Goal-reissue stress: repeated same-goal publish markers, transport interval,
  arrival / reissue interaction marker, and `goal repeat = 10`.

The figure includes a note that protocols are reported separately. It defines
the protocol split and does not encode method ranking or result values.

## Raw-Token Check Results

Command:

```bash
rg -n "risk_adapter|fixed_s080|fixed_s085|windlevel_s085|goal_repeat|goal_reissue_stress|single_goal_mission" paper/stage4_governor_ral/figures/fig1_architecture_tikz.tex paper/stage4_governor_ral/figures/fig2_protocol_split_tikz.tex || true
```

Result: no matches.

The new TikZ files use paper-facing terms such as `goal repeat = 1`, `goal
repeat = 10`, `Single-goal mission`, and `Goal-reissue stress`.

## Compile Command / Result

Command:

```bash
cd paper/stage4_governor_ral
latexmk -pdf -interaction=nonstopmode -file-line-error main.tex
```

Result:

- `latexmk_exit=0`
- `main.pdf` generated
- final log output: `Output written on main.pdf (7 pages, 912433 bytes).`
- PDF size by `ls -lh`: `892K`

## Warning / Error Summary

Final `main.log` inspection:

- LaTeX errors: none
- undefined citations: none in final log
- undefined references: none in final log
- overfull hboxes: 0
- missing figures: none
- bibliography warnings: none in final log
- float warnings: none in final log
- residual underfull boxes: 25 Underfull hbox messages and 0 Underfull vbox
  messages

The first LaTeX pass reported undefined citations before BibTeX ran; latexmk
resolved them by the final pass.

## Remaining TODOs

- Final visual PDF inspection after the Figure 1 / Figure 2 TikZ replacement
  and Figure 6 simplification.
- Optional manual external artist polish if the team wants a more bespoke
  schematic style before submission.

## Stage 4-BF Follow-Up

Stage 4-BF polished the Figure 1 / Figure 2 TikZ layouts after manual PDF
inspection found remaining overlap / spacing issues. The active schematics
remain TikZ vector figures, but arrows and event labels were repositioned for
cleaner paper-facing rendering. BF also recompiled the scaffold successfully to
7 pages with no LaTeX errors, undefined citations / references, overfull
hboxes, missing figures, bibliography warnings, or float warnings in the final
log.

## Stage 4-BG Follow-Up

Stage 4-BG further redrew the Figure 1 / Figure 2 TikZ schematics for a cleaner
paper-facing presentation. Figure 1 now uses a more disciplined aligned
flowchart with the unchanged inner stack on the top row and feedback /
diagnostic paths separated below. Figure 2 now uses a less crowded two-panel
timeline with fewer labels and clearer protocol definitions. The old generated
Figure 1 / Figure 2 PNG/SVG assets remain inactive.

## Scope

- No simulation was run.
- No ROS / RViz / `catkin_make` action was run.
- No training script was run.
- No figure generation script was run.
- No new experiments were run.
- No old Figure 1 / Figure 2 PNG/SVG assets were regenerated.
- No `experiments/results/**` files were modified.
- No `risk_adapter_v22` was created.
