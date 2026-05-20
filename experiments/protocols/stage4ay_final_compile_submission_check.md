# Stage 4-AY Final Compile / Submission Package Check

## Executive Summary

Stage 4-AY ran the final compile check for the RA-L Paper 1 scaffold under
`paper/stage4_governor_ral/` and records the submission package readiness
checklist.

Stage 4-AZ later records the human visual inspection of the compiled PDF. That
manual review found presentation blockers after compile success, including raw
underscore-style method tokens, Figure 1 / Figure 2 schematic quality,
Figure 3 compactness, and Figure 6 overcrowding. These are presentation issues,
not scientific-result blockers.

The final compile succeeded with `latexmk_exit=0`. The generated `main.pdf`
was 8 pages and approximately 2.3 MB during the check. The final `main.log`
had no LaTeX errors, undefined citations, undefined references, overfull
hboxes, missing figures, bibliography warnings, or float warnings. Residual
underfull boxes remain non-blocking layout reminders.

No scientific content, manuscript claims, citations, figures, tables,
algorithms, or experiment outputs were changed. No simulation, RViz,
`roslaunch`, `catkin_make`, training scripts, figure generation scripts, or new
experimental runs were performed. `risk_adapter_v22` was not created.

## Compile Command

Generated LaTeX outputs were removed before the final compile:

```bash
cd paper/stage4_governor_ral
rm -f main.aux main.bbl main.blg main.fdb_latexmk main.fls main.log \
  main.out main.pdf main.synctex.gz bibtex.log
```

Final compile command:

```bash
cd paper/stage4_governor_ral
latexmk -pdf -interaction=nonstopmode -file-line-error main.tex
```

## Compile Result

- Compile succeeded: yes.
- `latexmk_exit=0`.
- Generated PDF during the check:
  `paper/stage4_governor_ral/main.pdf`.
- Final log page count:
  `Output written on main.pdf (8 pages, 2310478 bytes).`
- PDF size observed by `ls -lh`: approximately 2.3 MB.
- `pdfinfo` was not available in `PATH`, so the page count was taken from
  `main.log`.

## Temporary PDF Inspection Copy

Temporary inspection copy created outside git:

```text
/tmp/stage4_governor_ral_final_check.pdf
```

This copy is for human visual inspection only and is not committed.

## Warning / Error Summary

Final log status:

- LaTeX errors: none found by `grep -n "!" main.log`.
- LaTeX warnings: none found in the final log.
- Undefined citations: none found in the final log.
- Undefined references: none found in the final log.
- Overfull hboxes: none found.
- Missing figures: none found.
- Bibliography warnings: none found.
- Float warnings: none found.
- Residual underfull boxes: 41 `Underfull \hbox` messages and 3
  `Underfull \vbox` messages. These remain non-blocking layout reminders.

The `ieeeconf` camera-ready reminder about last-page column equalization remains
a template-level reminder, not a compile failure.

## Submission Package Readiness Checklist

- Final PDF generated during the check: yes.
- Source tree available under `paper/stage4_governor_ral/`: yes.
- Figures available under `paper/stage4_governor_ral/figures/`: yes.
- `refs.bib` available: yes.
- Supplementary README available:
  `paper/stage4_governor_ral/supplementary/README.md`.
- Risk model checksum manifest exists:
  `experiments/protocols/stage4au3_risk_model_artifact_manifest.md`.
- Active citations clean: yes, per Stage 4-AM5.
- Claim audit complete: yes, per Stage 4-AX.
- No generated experiment outputs staged: yes during AY verification.
- Generated LaTeX PDF / aux / log outputs are excluded from git.

Remaining before actual submission:

- Fill final author names and affiliations.
- Perform final visual PDF inspection, including Figure 6 readability and
  last-page / column balance.
- Confirm final RA-L / IEEE official requirements and page budget.
- Decide whether to include supplementary risk model JSON artifacts, dataset
  checksum manifests, full CSV summaries, trace packages, or video.
- Decide final code / data availability statement.
- Assemble the submission package from the final PDF, source files, figures,
  `refs.bib`, and optional supplementary material.

## Remaining Human-Only Tasks

- Confirm author metadata and institutional affiliations.
- Confirm final venue template / upload rules.
- Inspect `/tmp/stage4_governor_ral_final_check.pdf` visually. Stage 4-AZ
  records the first human visual inspection findings and identifies follow-up
  presentation-polish stages.
- Decide what supplementary artifacts are acceptable to upload.
- Submit through the RA-L / IEEE system.

## Generated Outputs Excluded From Git

Generated LaTeX outputs created during the final compile/check pass are
excluded from the commit:

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
