# Stage 4-BB Schematic Placeholder and Redraw Plan

## Executive Summary

Stage 4-BB replaces the active Figure 1 and Figure 2 schematic images in the
RA-L Paper 1 scaffold with clean LaTeX placeholder boxes. The existing image
files remain in `paper/stage4_governor_ral/figures/`, but they are no longer
used by the active manuscript figures.

This is a presentation-readiness step only. It does not change scientific
claims, numerical results, citations, algorithms, method rankings, figure data,
or experiment outputs. No final schematic redraw was performed in BB.

No simulation, training, ROS action, RViz, `catkin_make`, or figure generation
script was run. No `risk_adapter_v22` was created.

## Why Figure 1 / Figure 2 Are Temporarily Replaced

Stage 4-AZ human visual inspection found that the current Figure 1 and Figure
2 schematic images are useful development placeholders but are not final-paper
quality. Leaving them as if they were final submission visuals would make the
manuscript visually misleading.

BB therefore makes the active manuscript visually honest: Figure 1 and Figure
2 now compile as compact placeholder boxes until externally redrawn schematics
are available.

## Figure 1 Redraw Specification

Figure 1 should communicate the stack-compatible risk-conditioned execution
governor.

Required blocks:

- nominal planner / reference generator;
- payload MPC;
- SO3 controller;
- UAV / suspended-payload plant;
- risk-conditioned execution governor;
- command-adaptation interface carrying `speed_scale` and
  `acceleration_scale`;
- optional diagnostic / risk-score input block if space allows.

Required arrows:

- planner output to payload MPC;
- payload MPC output to SO3 controller;
- SO3 controller output to the UAV / suspended-payload plant;
- governor output to the command-adaptation interface;
- command-adaptation effect on execution aggressiveness;
- risk / diagnostic input into the governor.

Intended message:

- The governor is a drop-in execution layer.
- The planner, payload MPC, and SO3 controller remain unchanged.
- The only main interface exposed in the paper is `speed_scale` /
  `acceleration_scale`.

Caption boundary:

- Describe empirical risk-conditioned execution governance.
- Do not imply a certified safety filter.
- Do not imply a formal safety guarantee.
- Do not imply a new planner, controller, or MPC design.

## Figure 2 Redraw Specification

Figure 2 should define the protocol split without looking like a result plot.

Required layout:

- two side-by-side panels;
- left panel: single-goal mission protocol;
- right panel: goal-reissue stress protocol;
- horizontal time axis in each panel;
- goal publish markers;
- arrival marker or arrival window;
- repeated goal publish markers in the stress protocol;
- clear visual separation between protocol definition and reported results.

Intended message:

- The single-goal mission protocol publishes one goal.
- The goal-reissue stress protocol republishes the same goal repeatedly.
- Results are reported separately by protocol.
- The figure defines evaluation protocols and does not encode method ranking.

## Accepted Tools

Accepted redraw tools include:

- PowerPoint;
- draw.io;
- Figma;
- Illustrator;
- TikZ;
- manually curated vector graphic.

## Required Style

- Readable in a two-column layout.
- No raw underscore method tokens.
- No clutter or dense implementation metadata.
- No certified-safety implication.
- No result-ranking implication.
- Clear labels, large enough text, and simple arrows.
- Prefer vector output when possible.

## Placeholder Status

The active manuscript now uses placeholder boxes with these messages:

- `Figure 1 placeholder: architecture schematic to be redrawn.`
- `Figure 2 placeholder: protocol split schematic to be redrawn.`

The old generated schematic files remain available as historical/generated
assets, but they should not be treated as final submission visuals.

Stage 4-BE follow-up:

- Stage 4-BE replaced the Figure 1 / Figure 2 placeholder boxes with active
  TikZ vector schematics.
- The replacement files are
  `paper/stage4_governor_ral/figures/fig1_architecture_tikz.tex` and
  `paper/stage4_governor_ral/figures/fig2_protocol_split_tikz.tex`.
- The old generated schematic PNG/SVG assets remain unchanged and inactive.

## Compile Check

Command run from `paper/stage4_governor_ral/`:

```bash
latexmk -pdf -interaction=nonstopmode -file-line-error main.tex
```

Result:

- Compile succeeded with exit status 0.
- `main.pdf` was generated during the check.
- Final log output: `Output written on main.pdf (8 pages, 1401762 bytes).`
- LaTeX errors: none.
- Undefined citations / references: none in the final log.
- Overfull hboxes: 0.
- Missing figures: none.
- Bibliography warnings: none in the final log.
- Float warnings: none.
- Underfull hboxes: 25.
- Underfull vboxes: 1.

Generated PDF / aux / log files were excluded from git.

## Remaining TODO

- Final visual PDF inspection after the Stage 4-BE TikZ replacement.
- Optional manual external artist polish if the team wants a more bespoke
  schematic style before submission.

Continue: no `risk_adapter_v22` before Paper 1 RA-L submission.
