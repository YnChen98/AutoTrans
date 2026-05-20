# Stage 4-AW Final Figure / Caption Polish Result

## Executive Summary

Stage 4-AW polished final figure and table captions for the RA-L Paper 1
scaffold under `paper/stage4_governor_ral/`. The pass focused on readability,
caption accuracy, and submission claim boundaries.

The manuscript still compiles successfully with `latexmk_exit=0`. The generated
`main.pdf` is 8 pages. No scientific claims, numerical results, method
rankings, citation keys, figure files, experiment outputs, planner files,
controller files, simulator files, or template files were changed.

No simulation, RViz, `roslaunch`, `catkin_make`, training scripts, figure
generation scripts, or new experimental runs were performed. `risk_adapter_v22`
was not created.

Stage 4-AX later audited the manuscript claim boundaries after this caption
polish pass. AX preserved the Figure/Table caption intent while tightening
overclaiming-risk wording in the active manuscript.

## Files Inspected

- `paper/stage4_governor_ral/sections/03_method.tex`
- `paper/stage4_governor_ral/sections/04_experiments.tex`
- `paper/stage4_governor_ral/sections/05_results.tex`
- `paper/stage4_governor_ral/tables/table1_protocol_balanced_robustness.tex`

## Figure / Table Captions Updated

- Figure 1: inspected and left unchanged. The existing caption already states
  stack-compatible governance, unchanged planner / payload MPC / SO3
  controller, the `speed_scale` / `acceleration_scale` interface, and the
  empirical-not-certified-safety-filter caveat.
- Figure 2: clarified that the figure is a protocol-split evaluation schematic,
  defines the single-goal mission and goal-reissue stress protocols, and is not
  a result plot.
- Table 1: clarified that the table reports protocol-split strict-valid counts
  and balanced robustness metrics, that total regret is relative to observed
  protocol oracles, and that the counts are descriptive rather than a
  statistical-significance claim.
- Figure 3: added explicit x-axis / y-axis interpretation, named the observed
  Pareto frontier methods, and bounded the frontier to evaluated methods and
  protocols.
- Figure 4: clarified that protocol regret is relative to observed protocol
  oracles and that the oracle is an observed best method, not a theoretical
  optimum.
- Figure 5: inspected and left unchanged. The existing caption already marks
  invalid-only failure groups as diagnostic rather than exact physical
  root-cause proof.
- Figure 6: shortened panel labels, kept the 3+2 `figure*` layout, and clarified
  that the traces compare Trial 4 goal-reissue stress behavior and the Trial 6
  single-goal bottleneck as qualitative mechanism evidence only.

## Consistency Checks

- `goal-reissue stress` wording remains the main protocol wording.
- No `risk_adapter_v21` overall-best wording was added.
- No mixed-protocol aggregate claim was added.
- No statistical significance claim was added.
- No safety guarantee was added.
- No real-world deployment claim was added.
- Failure groups remain diagnostic only.
- `risk_adapter_v1` remains the balanced learned / risk-conditioned
  protagonist.

## Compile Command and Result

Generated LaTeX outputs were removed before the compile:

```bash
cd paper/stage4_governor_ral
rm -f main.aux main.bbl main.blg main.fdb_latexmk main.fls main.log \
  main.out main.pdf main.synctex.gz bibtex.log
```

Compile command:

```bash
cd paper/stage4_governor_ral
latexmk -pdf -interaction=nonstopmode -file-line-error main.tex
```

Compile result:

- Compile succeeded: yes.
- `latexmk_exit=0`.
- Generated PDF during the check:
  `paper/stage4_governor_ral/main.pdf`.
- Final log page count:
  `Output written on main.pdf (8 pages, 2310811 bytes).`
- Final PDF size observed by `ls -lh`: approximately 2.3 MB.
- `pdfinfo` was not available in `PATH`, so page count was taken from
  `main.log`.

## Warnings / Errors

Final log status after Stage 4-AW:

- LaTeX errors: none found by `grep -n "!" main.log`.
- LaTeX warnings: none found in the final log.
- Undefined citations: none found in the final log.
- Undefined references: none found in the final log.
- Overfull hboxes: none found.
- Missing figures: none found.
- Bibliography warnings: none found.
- Float warnings: none found.
- Residual underfull boxes: 40 `Underfull \hbox` messages and 3
  `Underfull \vbox` messages. These remain non-blocking layout reminders.

The `ieeeconf` camera-ready reminder about last-page column equalization remains
a template-level reminder, not a compile failure.

## Unresolved Layout TODOs

- Perform final visual PDF inspection, with specific attention to Figure 6
  readability after the caption / panel-label polish.
- Confirm final RA-L / IEEE page-budget and template requirements.
- Stage 4-AX final claim audit is complete.
- Run one final compile after all submission edits.

## Generated Outputs Excluded From Commit

Generated LaTeX outputs created during the compile/check pass are excluded from
the commit:

- `paper/stage4_governor_ral/main.pdf`
- `paper/stage4_governor_ral/main.aux`
- `paper/stage4_governor_ral/main.bbl`
- `paper/stage4_governor_ral/main.blg`
- `paper/stage4_governor_ral/main.fdb_latexmk`
- `paper/stage4_governor_ral/main.fls`
- `paper/stage4_governor_ral/main.log`
- `paper/stage4_governor_ral/main.out`
- `paper/stage4_governor_ral/main.synctex.gz`
- `paper/stage4_governor_ral/bibtex.log`

Continue: no `risk_adapter_v22` before Paper 1 RA-L submission.
