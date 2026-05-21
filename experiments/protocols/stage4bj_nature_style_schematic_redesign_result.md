# Stage 4-BJ Nature-Style Schematic Redesign Result

## Executive Summary

Stage 4-BJ redraws Figure 1 and Figure 2 for the active RA-L scaffold using a
deterministic, paper-facing vector schematic workflow inspired by
`nature-figure` guidance.

The active manuscript now uses the new PDF schematics:

- `paper/stage4_governor_ral/figures/fig1_architecture_nature.pdf`
- `paper/stage4_governor_ral/figures/fig2_protocol_split_nature.pdf`

The old TikZ files remain in the repository as historical scaffold assets, but
they are no longer the active Figure 1 / Figure 2 inputs.

## `nature-figure` Guidance Source Inspected

The external skill repository was cloned outside the repository:

```bash
rm -rf /tmp/nature-skills
git clone https://github.com/Yuan1z0825/nature-skills.git /tmp/nature-skills
```

The inspected guidance included:

- `/tmp/nature-skills/skills/nature-figure/SKILL.md`
- `/tmp/nature-skills/skills/nature-figure/README.md`
- `/tmp/nature-skills/skills/nature-figure/references/figure-contract.md`
- `/tmp/nature-skills/skills/nature-figure/references/design-theory.md`
- `/tmp/nature-skills/skills/nature-figure/references/qa-contract.md`

The local `nature-figure` skill guidance was also used for the figure contract:
schematic-led figure archetype, Python-only backend, editable SVG/PDF export,
restrained palette, direct labels, and review-risk checks.

## Why Figure 1 / Figure 2 Were Redrawn

Manual inspection after Stage 4-BG found that the active TikZ schematics still
had paper-facing layout blockers:

- arrows or lines could visually interfere with text boxes;
- labels risked leaving boxes or colliding with connectors;
- alignment was uneven;
- diagnostic and feedback paths competed with the main explanatory structure.

Stage 4-BJ addresses those presentation blockers without changing the
scientific content.

## Script Added

The deterministic generator is:

```text
experiments/scripts/generate_stage4_nature_style_schematics.py
```

The script:

- uses `matplotlib` only;
- does not use seaborn;
- does not require ROS;
- does not write under `experiments/results/`;
- generates SVG, PDF, and PNG outputs;
- keeps labels paper-facing and avoids raw code-style tokens.

## Figure 1 Design Summary

Figure 1 is redrawn as a clean architecture schematic.

Design choices:

- top row shows the unchanged inner stack:
  Planner / reference generator, Payload MPC, SO(3) controller, and UAV +
  suspended payload;
- lower row shows the external empirical governor path:
  Risk input / warning scores, Risk-conditioned execution governor, and
  Command-adaptation interface;
- Diagnostics / logs are separated as a support block;
- main execution arrows, governor arrows, and feedback arrows use different
  grouping and line styles so the figure does not rely on color alone;
- connectors are orthogonal or straight, routed outside text boxes, and avoid
  crossing through labels;
- the figure does not imply certified safety, controller replacement, or result
  ranking.

## Figure 2 Design Summary

Figure 2 is redrawn as a two-panel protocol schematic.

Design choices:

- left panel defines the single-goal mission protocol with one goal publish,
  a transport interval, and an arrival / hold marker;
- right panel defines the goal-reissue stress protocol with repeated goal
  publish markers, a transport interval, and an arrival / reissue interaction
  marker;
- the global note states that protocols are reported separately;
- the figure contains no method names, result values, or ranking encodings;
- the schematic is not a result plot.

## Generated Files

- `paper/stage4_governor_ral/figures/fig1_architecture_nature.svg`
- `paper/stage4_governor_ral/figures/fig1_architecture_nature.pdf`
- `paper/stage4_governor_ral/figures/fig1_architecture_nature.png`
- `paper/stage4_governor_ral/figures/fig2_protocol_split_nature.svg`
- `paper/stage4_governor_ral/figures/fig2_protocol_split_nature.pdf`
- `paper/stage4_governor_ral/figures/fig2_protocol_split_nature.png`

## Raw-Token Check Result

Command:

```bash
rg -n "risk_adapter|fixed_s080|fixed_s085|windlevel_s085|goal_repeat|goal_reissue_stress|single_goal_mission|position error not logged" \
  paper/stage4_governor_ral/figures/fig1_architecture_nature.svg \
  paper/stage4_governor_ral/figures/fig2_protocol_split_nature.svg || true
```

Result: no matches.

## Compile Result

Commands:

```bash
python3 -m py_compile experiments/scripts/generate_stage4_nature_style_schematics.py
python3 experiments/scripts/generate_stage4_nature_style_schematics.py

cd paper/stage4_governor_ral
rm -f main.aux main.bbl main.blg main.fdb_latexmk main.fls main.log \
  main.out main.pdf main.synctex.gz bibtex.log
latexmk -pdf -interaction=nonstopmode -file-line-error main.tex
```

Result:

- Python compile succeeded.
- Figure generation succeeded.
- LaTeX compile succeeded with `latexmk_exit=0`.
- `main.pdf` was generated during the check as a 7-page PDF.
- Generated LaTeX PDF / auxiliary / log files were cleaned before commit.

## Warning / Error Summary

Final `main.log` inspection found:

- no LaTeX errors;
- no undefined citations or references;
- no overfull hboxes;
- no missing figures;
- no bibliography warnings in `main.blg`;
- no float warnings.

Residual non-blocking layout notes:

- 5 `Underfull \hbox` messages remain in the final log.

## Remaining TODOs

- Perform human visual inspection of the compiled PDF after BJ and the planned
  Stage 4-BK prose polish.
- Continue to treat the old TikZ files as historical scaffold assets unless a
  future submission package explicitly needs provenance material.

## Scope Boundaries

- No scientific claim changed.
- No numerical result changed.
- No citation changed.
- No Table 1 change.
- No algorithm change.
- No experiment run.
- No simulation, ROS, RViz, `roslaunch`, `catkin_make`, or training script was
  run.
- No `risk_adapter_v22` was created.
