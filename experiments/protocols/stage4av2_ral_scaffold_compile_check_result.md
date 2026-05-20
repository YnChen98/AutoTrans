# Stage 4-AV2 RA-L Scaffold Compile / Check Result

## Executive Summary

Stage 4-AV2 runs the first compile/check pass for the RA-L-oriented scaffold
under `paper/stage4_governor_ral/`.

The scaffold compiled successfully with `latexmk_exit=0`. The generated
`main.pdf` was 8 pages and approximately 2.3 MB during the check. The final
`main.log` had no LaTeX errors, undefined citations, undefined references,
overfull hboxes, missing figures, bibliography warnings, or float warnings.

Stage 4-AW later recompiled the RA-L scaffold after final figure / table
caption polish. That compile also succeeded with `latexmk_exit=0` and produced
an 8-page `main.pdf`; the final log again had no LaTeX errors, undefined
citations, undefined references, overfull hboxes, missing figures,
bibliography warnings, or float warnings.

No scientific claims, numerical results, method rankings, citation choices,
figures, tables, experiment outputs, planner/controller/simulator files, or
template source files were changed. No simulation, RViz, `roslaunch`,
`catkin_make`, training scripts, or figure generation scripts were run.
`risk_adapter_v22` was not created.

## Template / Scaffold Status

- Scaffold root: `paper/stage4_governor_ral/`.
- Template class: `ieeeconf`.
- Detected document class:
  `\documentclass[letterpaper, 10 pt, conference]{ieeeconf}`.
- Source scaffold remains separate: `paper/stage4_governor/`.
- The original scaffold under `paper/stage4_governor/` was not modified.
- Template source under `paper/templates/ral/` was not modified.

## Commands Run

Clean stale generated outputs:

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

Log / output inspection commands:

```bash
test -f main.pdf && ls -lh main.pdf
grep -n "Output written on main.pdf" main.log || true
grep -n "!" main.log | head -80 || true
grep -n "Warning\|Overfull\|Underfull\|Citation\|undefined\|Reference\|Float\|Missing\|Error" main.log | head -220 || true
grep -n "LaTeX Warning\|Package.*Warning\|Citation.*undefined\|Reference.*undefined\|undefined references\|undefined citations\|Rerun\|Float\|Overfull" main.log || true
```

`pdfinfo` was checked but was not available in `PATH`, so the page count was
taken from `main.log`.

## Compile Result

- Compile succeeded: yes.
- `latexmk_exit=0`.
- Generated PDF during the check:
  `paper/stage4_governor_ral/main.pdf`.
- Final log page count:
  `Output written on main.pdf (8 pages, 2310603 bytes).`
- Final PDF size observed by `ls -lh`: approximately 2.3 MB.

## Warnings / Errors Found

Final log status:

- LaTeX errors: none found by `grep -n "!" main.log`.
- Undefined citations: none found in the final log.
- Undefined references: none found in the final log.
- Overfull hboxes: none found.
- Missing figures: none found.
- Bibliography warnings: none found in the final log.
- Float warnings: none found.
- Residual underfull boxes: 40 `Underfull \hbox` messages and 2
  `Underfull \vbox` messages. These are non-blocking layout reminders,
  mostly from long `\texttt{...}` identifiers, narrow two-column paragraphs,
  and bibliography line breaking.

The `ieeeconf` class camera-ready reminder about final column equalization
remains a template-level reminder, not a compile failure.

## Fixes Made

No LaTeX / manuscript formatting fixes were needed after the compile. The AV2
task did not change manuscript source content under
`paper/stage4_governor_ral/`.

## Unresolved TODOs

- Perform visual PDF inspection before submission.
- Confirm final RA-L / IEEE template requirements and page budget.
- Fill final author names and affiliations.
- Complete Stage 4-AM5 conditional citation verification and BibTeX cleanup if
  any conditional citations are considered.
- Stage 4-AW final figure / caption polish is complete; perform final visual
  PDF inspection before submission.
- Continue Stage 4-AX final claim audit.
- Keep generated PDF / aux / log files out of git.

## Generated Files Excluded From Commit

Generated LaTeX outputs were created during the compile/check pass and should
remain untracked / unstaged:

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

Before commit, these generated outputs should be removed or left unstaged.

## Next Stage Recommendation

Recommended next stage depends on final submission priorities:

- Stage 4-AM5 conditional citation verification and BibTeX cleanup;
- Stage 4-AW final figure / caption polish;
- Stage 4-AX final claim audit.

Continue: no `risk_adapter_v22` before Paper 1 RA-L submission.
