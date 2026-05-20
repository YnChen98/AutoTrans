# Stage 4-BD Figure 6 Simplified Replot Result

## Executive Summary

Stage 4-BD replaces the crowded five-panel Figure 6 representative-trace
layout in the RA-L Paper 1 scaffold with one simplified paper-facing composite
trace figure. The new active Figure 6 uses display names, fewer signals, larger
labels, and no raw underscore method labels.

The manuscript scientific content, numerical results, rankings, citations,
Table 1, algorithms, and claim boundaries were not changed. The traces remain
qualitative mechanism evidence only, not proof of general causality.

## Old Issue From AZ

Stage 4-AZ found the previous Figure 6 visually overcrowded:

- too many stacked signal rows per panel;
- small labels and legends;
- raw underscore method labels inside figure text;
- too much trace detail for the main paper;
- likely need to shift full trace detail to supplementary / archived assets.

## Cases Selected And Why

The simplified main-paper figure uses four representative cases:

| panel | protocol | method display name | outcome | rationale |
| --- | --- | --- | --- | --- |
| (a) | Trial 4 goal-reissue stress | Risk Adapter v2.1 | failure | shows the Trial 4 stress weakness of the strong nominal variant |
| (b) | Trial 4 goal-reissue stress | Risk Adapter v1 | success | shows the balanced protagonist avoiding the same stress case class |
| (c) | Trial 6 single-goal | Wind-Level 0.85 | success | shows the single-goal specialist behavior |
| (d) | Trial 6 single-goal | Risk Adapter v2.1 | failure | shows that lower scale is not automatically safer and delayed divergence can occur |

Fixed Scale 0.80 remains covered by Table 1, Figure 3, and Figure 4. Its full
trace remains appropriate for supplementary / archived trace material rather
than the simplified main-paper Figure 6.

## Script Added

Added:

```text
experiments/scripts/generate_stage4_paper_ready_trace_summary.py
```

The script uses matplotlib only, does not import ROS, does not run simulation,
does not use seaborn, and does not write `experiments/results/**`.

## Source Index / CSV Use

The script reads:

```text
experiments/results/stage4_representative_traces/stage4aa_representative_trace_index.csv
```

It then reads the selected underlying logs through the `csv_path` field:

- `experiments/logs/autotrans_log_20260516_133400.csv`
- `experiments/logs/autotrans_log_20260510_132031.csv`
- `experiments/logs/autotrans_log_20260517_132241.csv`
- `experiments/logs/autotrans_log_20260516_002809.csv`

If the index or any selected CSV is missing, the script raises a clear error
instead of fabricating data.

## Generated Files

Generated and staged as paper assets:

```text
paper/stage4_governor_ral/figures/fig6_trace_summary.png
paper/stage4_governor_ral/figures/fig6_trace_summary.svg
```

The previous five Figure 6 panel images were not modified.

## Signals Plotted

The composite uses a 4-column by 4-row small-multiple layout:

- UAV speed and payload speed;
- swing angle;
- target XY error or UAV-reference XY error when available;
- command `speed_scale` and `acceleration_scale`.

For the Trial 4 Risk Adapter v1 success case, position error fields are not
logged in the selected CSV, so that panel explicitly says `position error not
logged` rather than fabricating an error trace. Failure / NaN traces are drawn
only up to the first failure / NaN marker, with the axis retaining a small
post-marker margin for readability.

## Display-Name Cleanup

Visible figure text uses paper-facing display names:

- Risk Adapter v2.1;
- Risk Adapter v1;
- Wind-Level 0.85;
- T4 goal-reissue;
- T6 single-goal.

SVG raw-token check:

```bash
rg -n "risk_adapter|fixed_s080|fixed_s085|windlevel_s085|goal_reissue_stress|single_goal_mission" paper/stage4_governor_ral/figures/fig6_trace_summary.svg || true
```

Result: no matches.

## Caption / Manuscript Changes

`paper/stage4_governor_ral/sections/05_results.tex` now includes one figure:

```tex
\includegraphics[width=\textwidth]{figures/fig6_trace_summary.png}
```

The caption states that the columns compare Trial 4 goal-reissue stress and
Trial 6 single-goal bottleneck behavior, that only key speed, swing, error, and
governor-scale signals are retained for readability, and that the traces are
qualitative mechanism evidence rather than proof of general causality.

## Compile Command / Result

Command:

```bash
cd paper/stage4_governor_ral
latexmk -pdf -interaction=nonstopmode -file-line-error main.tex
```

Result:

- `latexmk_exit=0`
- `main.pdf` generated
- final log output: `Output written on main.pdf (7 pages, 893935 bytes).`
- PDF size by `ls -lh`: `873K`

## Warning / Error Summary

Final `main.log` inspection:

- LaTeX errors: none
- undefined citations: none in final log
- undefined references: none in final log
- overfull hboxes: 0
- missing figures: none
- bibliography warnings: none in final log
- float warnings: none in final log
- residual underfull boxes: 25 Underfull hbox messages and 1 Underfull vbox
  message

The first LaTeX pass reported undefined citations before BibTeX ran; latexmk
resolved them by the final pass.

## Remaining TODOs

- Full trace details may move to supplementary / archived trace assets.
- Figure 1 / Figure 2 still require external paper-quality redraw.
- Final visual PDF inspection remains required after BD because the PDF page
  count changed from 8 pages to 7 pages under the simplified Figure 6 layout.

## Scope

- No simulation was run.
- No ROS / RViz / `catkin_make` action was run.
- No training script was run.
- No new experiments were run.
- No `experiments/results/**` files were modified.
- No `risk_adapter_v22` was created.
