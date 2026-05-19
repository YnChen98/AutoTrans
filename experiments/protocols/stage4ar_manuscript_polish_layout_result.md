# Stage 4-AR Manuscript Polish / Layout Result

## Executive Summary

Stage 4-AR performs the manuscript polish / layout pass after the Stage 4-AQ3
official `ieeeconf.cls` compile success. The pass is limited to LaTeX
formatting and manuscript-presentation issues under `paper/stage4_governor/`.

The manuscript compiles successfully with `latexmk_exit=0`. The generated
`main.pdf` is 8 pages and approximately 2.3 MB. No scientific claims,
numerical results, method rankings, citation choices, risk model artifacts, or
experiment outputs were changed. No simulation, RViz, `roslaunch`,
`catkin_make`, training scripts, or figure generation scripts were run.
`risk_adapter_v22` was not created.

## Commands Run

Clean previous LaTeX generated outputs:

```bash
rm -f paper/stage4_governor/main.aux \
  paper/stage4_governor/main.bbl \
  paper/stage4_governor/main.blg \
  paper/stage4_governor/main.fdb_latexmk \
  paper/stage4_governor/main.fls \
  paper/stage4_governor/main.log \
  paper/stage4_governor/main.out \
  paper/stage4_governor/main.pdf \
  paper/stage4_governor/main.synctex.gz \
  paper/stage4_governor/bibtex.log
```

Compile command:

```bash
cd paper/stage4_governor
latexmk -pdf -interaction=nonstopmode -file-line-error main.tex
```

Log inspection commands:

```bash
test -f main.pdf && ls -lh main.pdf
grep -n "Output written on main.pdf" main.log || true
grep -n "!" main.log | head -80 || true
grep -n "Warning\|Overfull\|Underfull\|Citation\|undefined\|Reference\|Float\|Missing\|Error" main.log | head -220 || true
grep -n "LaTeX Warning\|Package.*Warning\|Citation.*undefined\|Reference.*undefined\|undefined references\|undefined citations\|Rerun\|Float\|Overfull" main.log || true
```

`pdfinfo` was not available in `PATH`, so the page count was taken from
`main.log`.

## Compile Result

- Compile succeeded: yes.
- `latexmk_exit=0`.
- Generated PDF during the check:
  `paper/stage4_governor/main.pdf`.
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
  `Underfull \vbox` messages, mostly from two-column text, long
  `\texttt{...}` identifiers, and bibliography line breaking. These are
  recorded as non-blocking layout reminders for a later venue-specific polish.

The class reminder from `ieeeconf.cls` about final camera-ready column
equalization remains a template-level reminder, not a compile failure.

## Fixes Made

- Updated Figure 6 in `paper/stage4_governor/sections/05_results.tex` from a
  five-panel single row to a 3+2 two-row `figure*` layout, increasing panel
  width from `0.19\textwidth` to `0.32\textwidth` and using `\scriptsize`
  panel labels.
- Removed the resolved Table 1 layout TODO from
  `paper/stage4_governor/tables/table1_protocol_balanced_robustness.tex`; the
  table already uses `\resizebox{\linewidth}{!}{...}` and produced no overfull
  warning.

No source images were replaced. No table rows or columns were removed. The
Figure 6 caption still preserves the claim boundary that representative traces
are qualitative mechanism evidence, not proof of general causality.

## Unresolved TODOs

- Review residual underfull boxes during the final venue-specific layout pass,
  especially long `\texttt{...}` method names in the two-column format.
- Perform final visual PDF inspection before submission.
- Continue RA-L-specific template / page-budget work in Stage 4-AV or a
  follow-on Stage 4-AT2 checklist.
- Continue conditional citation verification if any unverified citations are
  considered later; do not add conditional citations as active BibTeX entries
  without metadata verification.

## Generated Files

Generated LaTeX outputs were excluded from commit and should remain untracked:

- `paper/stage4_governor/main.pdf`
- `paper/stage4_governor/main.aux`
- `paper/stage4_governor/main.bbl`
- `paper/stage4_governor/main.blg`
- `paper/stage4_governor/main.fdb_latexmk`
- `paper/stage4_governor/main.fls`
- `paper/stage4_governor/main.log`
- `paper/stage4_governor/main.out`
- `paper/stage4_governor/main.synctex.gz`
- `paper/stage4_governor/bibtex.log`
