# Stage 4-BG Presentation Polish Cleanup Result

## Executive Summary

Stage 4-BG performs a paper-facing presentation polish cleanup for the active
RA-L Paper 1 scaffold after Stage 4-BF / BE. It cleans the remaining
manuscript-visible code-token style wording, redraws Figure 1 and Figure 2
TikZ schematics in cleaner aligned layouts, regenerates Figure 4 and Figure 5
with paper-facing display names, and polishes the Figure 6 trace-summary
layout.

No scientific claims, numerical results, rankings, citations, algorithms, or
experiment outputs were changed.

Stage 4-BI follow-up note: manual inspection after BG still found that Figure 1
and Figure 2 are not final and that some manuscript prose still reads as
code-like or AI-like. Stage 4-BI therefore plans a deeper
nature-skills-assisted presentation / prose polish pass using `nature-figure`
for Figure 1 / Figure 2 redesign guidance and `nature-polishing` for a bounded
RA-L prose polish workflow.

## Issues Addressed

- Remaining paper-facing raw-token / monospace / source-code-like wording in
  the active manuscript.
- Figure 1 TikZ architecture layout still looked visually busy after BE / BF.
- Figure 2 TikZ protocol schematic still had cramped text / timeline spacing.
- Figure 4 and Figure 5 still needed paper-facing generated SVG / PNG assets
  with display names and no stage-style raw method labels.
- Figure 6 needed one closer global legend, reduced top whitespace, and
  subcaptions below the four column panels.

## Wording Cleanup Summary

Active manuscript wording was cleaned in:

- `paper/stage4_governor_ral/main.tex`
- `paper/stage4_governor_ral/sections/01_intro.tex`
- `paper/stage4_governor_ral/sections/02_related_work.tex`
- `paper/stage4_governor_ral/sections/03_method.tex`
- `paper/stage4_governor_ral/sections/04_experiments.tex`
- `paper/stage4_governor_ral/sections/05_results.tex`
- `paper/stage4_governor_ral/sections/07_conclusion.tex`

The cleanup removed the prior narrow `\texttt{...}` rendering workaround from
`main.tex`, changed active interface mentions to paper-facing prose such as
`speed scale` and `acceleration scale`, changed the model export description to
`JSON-serialized logistic regression models`, and standardized the controller
name as `SO(3)` in active prose.

Raw-token searches over the active manuscript source found no remaining
problem strings for the targeted method / protocol / interface tokens.

## Figure 1 Redesign Summary

`paper/stage4_governor_ral/figures/fig1_architecture_tikz.tex` was redrawn as
a cleaner aligned flowchart. The top row now shows the unchanged inner stack:

```text
Planner / reference generator -> Payload MPC -> SO(3) controller -> UAV + suspended payload
```

The lower row separates risk input / warning scores, the empirical
risk-conditioned execution governor, the command-adaptation interface, and
diagnostics / logs. Feedback arrows are routed outside the main boxes, and the
main command path is visually separated from auxiliary feedback.

## Figure 2 Redesign Summary

`paper/stage4_governor_ral/figures/fig2_protocol_split_tikz.tex` was redrawn
as a cleaner two-panel timeline schematic. The left panel defines the
single-goal mission with `goal repeat = 1`; the right panel defines
goal-reissue stress with `goal repeat = 10`. Labels were reduced and spaced so
the figure defines the protocols without looking like a result plot.

## Figure 4 / Figure 5 Cleanup Summary

Added deterministic matplotlib-only generators:

- `experiments/scripts/generate_stage4_paper_ready_protocol_regret.py`
- `experiments/scripts/generate_stage4_paper_ready_failure_groups.py`

Regenerated assets:

- `paper/stage4_governor_ral/figures/fig4_protocol_regret.png`
- `paper/stage4_governor_ral/figures/fig4_protocol_regret.svg`
- `paper/stage4_governor_ral/figures/fig5_invalid_failure_groups.png`
- `paper/stage4_governor_ral/figures/fig5_invalid_failure_groups.svg`

Figure 4 now uses display names, removes the stage-style in-plot title, and
keeps protocol regret values unchanged. Figure 5 now uses a one-column
horizontal stacked-bar layout with readable paper-facing method labels and
legend labels. The underlying invalid-only failure counts are unchanged.

## Figure 6 Layout Polish Summary

`experiments/scripts/generate_stage4_paper_ready_trace_summary.py` was updated
to keep a single global legend close to the panel grid, reduce top whitespace,
and place `(a)`-`(d)` subcaptions below the four selected trace columns.

Regenerated assets:

- `paper/stage4_governor_ral/figures/fig6_trace_summary.png`
- `paper/stage4_governor_ral/figures/fig6_trace_summary.svg`

The current Figure 6 preserves the selected signals: UAV speed, payload speed,
swing, UAV XY displacement, speed scale, acceleration scale, arrival marker,
and failure / NaN marker. It does not reintroduce `position error not logged`.

## Verification

Python checks:

```bash
python3 -m py_compile experiments/scripts/generate_stage4_paper_ready_trace_summary.py experiments/scripts/generate_stage4_paper_ready_protocol_regret.py experiments/scripts/generate_stage4_paper_ready_failure_groups.py
python3 experiments/scripts/generate_stage4_paper_ready_protocol_regret.py
python3 experiments/scripts/generate_stage4_paper_ready_failure_groups.py
python3 experiments/scripts/generate_stage4_paper_ready_trace_summary.py
```

Result: all commands succeeded.

Raw-token checks:

```bash
rg -n "goal_repeat|speed_scale|acceleration_scale|risk_threshold|hard_threshold|soft_scale|hard_scale|scale_rate|command_control_upstream|planner_reference_upstream|state_task_upstream|LogisticRegression|texttt|risk_adapter|fixed_s080|fixed_s085|windlevel_s085|goal_reissue_stress|single_goal_mission|position error not logged" paper/stage4_governor_ral/main.tex paper/stage4_governor_ral/sections paper/stage4_governor_ral/tables/table1_protocol_balanced_robustness.tex
rg -n "risk_adapter|fixed_s080|fixed_s085|windlevel_s085|goal_repeat|goal_reissue_stress|single_goal_mission|command_control_upstream|planner_reference_upstream|state_task_upstream|position error not logged|Stage 4" paper/stage4_governor_ral/figures/fig4_protocol_regret.svg paper/stage4_governor_ral/figures/fig5_invalid_failure_groups.svg paper/stage4_governor_ral/figures/fig6_trace_summary.svg paper/stage4_governor_ral/figures/fig1_architecture_tikz.tex paper/stage4_governor_ral/figures/fig2_protocol_split_tikz.tex
```

Result: no matches.

LaTeX command:

```bash
cd paper/stage4_governor_ral
rm -f main.aux main.bbl main.blg main.fdb_latexmk main.fls main.log main.out main.pdf main.synctex.gz bibtex.log
latexmk -pdf -interaction=nonstopmode -file-line-error main.tex
```

Result:

- `latexmk_exit=0`
- final output: `Output written on main.pdf (7 pages, 983223 bytes).`
- PDF size by `ls -lh`: `961K`
- page count remains 7 pages after BG.

Final log inspection:

- LaTeX errors: none
- undefined citations: none in final log
- undefined references: none in final log
- overfull hboxes: 0
- missing figures: none
- bibliography warnings: none in final log
- float warnings: none in final log
- residual underfull boxes: 5 Underfull hbox messages, 0 Underfull vbox
  messages

A temporary Ghostscript render under `/tmp` was used for visual sanity checks;
those files were not committed.

## Residual Non-Blocking Reminders

- Stage 4-BI should plan the deeper nature-skills-assisted Figure 1 / Figure 2
  and prose polish pass because BG did not fully resolve those issues.
- Stage 4-BJ should redesign Figure 1 / Figure 2 after BI.
- Stage 4-BK should perform the bounded RA-L prose polishing / de-AI pass after
  BI.
- Stage 4-BL should compile and visually inspect the paper after BJ / BK.
- Author names and affiliations remain placeholders.
- Final RA-L official requirements and page-budget confirmation remain
  human/submission tasks.
- Optional external artist polish for Figure 1 / Figure 2 remains possible if
  the team wants a more bespoke schematic style.

## Scope

- No scientific claims changed.
- No numerical results changed.
- No citations changed.
- No experiments were run.
- No simulation was run.
- No RViz / `roslaunch` / `catkin_make` action was run.
- No training script was run.
- No `risk_adapter_v22` was created.
- Generated LaTeX PDF / aux / log files were excluded from git.
