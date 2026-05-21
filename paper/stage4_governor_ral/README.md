# Stage 4 Governor RA-L-Oriented Manuscript Scaffold

## Purpose

This directory is the Stage 4-AV RA-L-oriented Paper 1 manuscript scaffold. It
is copied and lightly adapted from the existing source scaffold:

```text
paper/stage4_governor/
```

The official user-provided template source directory is:

```text
paper/templates/ral/
```

No LaTeX compile was run in Stage 4-AV. Stage 4-AV2 later records the first
RA-L scaffold compile/check pass in
`experiments/protocols/stage4av2_ral_scaffold_compile_check_result.md`.

## Template Inspection

Template files detected:

- `paper/templates/ral/ieeeconf.cls`
- `paper/templates/ral/root.pdf`
- `paper/templates/ral/root.tex`

Likely main template file:

- `paper/templates/ral/root.tex`

Detected document class in `paper/templates/ral/root.tex`:

```tex
\documentclass[letterpaper, 10 pt, conference]{ieeeconf}
```

Required class/style/bibliography files detected in `paper/templates/ral/`:

- `ieeeconf.cls`

No `IEEEtran.cls`, `.sty`, or `.bst` files were found in the template
directory. The template appears to be `ieeeconf`-based, not `IEEEtran`-based.

`paper/stage4_governor/ieeeconf.cls` was already present in the previous
scaffold, but Stage 4-AV copied `paper/templates/ral/ieeeconf.cls` into this
RA-L-oriented scaffold so this directory uses the user-provided template class
file.

## Scaffold Status

- Scaffold basis: `paper/stage4_governor/`.
- Template source: `paper/templates/ral/`.
- Current scaffold type: `ieeeconf`-based RA-L-oriented conversion scaffold.
- Final RA-L / IEEE template requirements and page budget still need
  confirmation before submission.
- Scientific claims, numerical results, method rankings, citations, figures,
  and tables were not changed by Stage 4-AV.
- Stage 4-AV2 compile/check succeeded with `latexmk_exit=0`; the generated
  `main.pdf` was 8 pages during the check. Generated PDF / aux / log files
  should remain out of git.
- Stage 4-AM5 checked active RA-L scaffold citation usage. Active citations
  and active `refs.bib` entries match, and conditional citation keys are
  excluded from the active Paper 1 bibliography unless later verified.
- Stage 4-AW polished figure / table captions for the active RA-L scaffold,
  preserved claim boundaries, and recompiled successfully to an 8-page PDF
  during the check.
- Stage 4-AX performed the final claim audit for the active manuscript,
  tightened overclaiming-risk wording, and removed active manuscript
  `risk_adapter_v22` wording.
- Stage 4-AY ran the final compile / submission checklist. The scaffold
  compiled to an 8-page PDF during the check, and a temporary inspection copy
  was written to `/tmp/stage4_governor_ral_final_check.pdf`.
- Stage 4-AZ recorded human visual inspection findings after the clean compile.
  Compile success does not yet mean visual-submission readiness: raw method
  tokens, Figure 1 / Figure 2 schematic quality, Figure 3 compactness, and
  Figure 6 overcrowding remain presentation blockers.
- Stage 4-BA cleaned manuscript-visible method names in active prose,
  captions, panel labels, and Table 1. Figure-internal labels embedded in
  existing image files remain for the figure-specific polish stages.
- Stage 4-BB replaced the active Figure 1 / Figure 2 generated schematic
  images with LaTeX placeholder boxes and documented the external redraw
  workflow. Final paper-quality schematics are still required before
  submission.
- Stage 4-BC regenerated Figure 3 as a compact paper-facing Pareto frontier
  plot with display names, reduced whitespace, no raw underscore labels, and no
  redundant in-plot title. Figure 3 now has both PNG and SVG assets.
- Stage 4-BD regenerated Figure 6 as one simplified paper-facing trace summary
  with display names, fewer key signals, larger labels, and no visible raw
  underscore method labels. The scaffold compiled to 7 pages during the BD
  check.
- Stage 4-BE replaced the active Figure 1 / Figure 2 placeholder boxes with
  TikZ vector schematics. The old generated schematic PNG/SVG assets remain
  unchanged and inactive.
- Stage 4-BF fixed remaining presentation blockers after BE: manuscript-visible
  interface / protocol tokens render as paper-facing names, Figure 1 / Figure 2
  TikZ spacing was polished, and Figure 6 was regenerated without unavailable
  position-error placeholder text. The scaffold compiled to 7 pages during the
  BF check.
- Stage 4-BG performed a further paper-facing presentation cleanup: remaining
  active manuscript code-token rendering was removed, Figure 1 / Figure 2 TikZ
  schematics were redrawn with cleaner spacing, Figure 4 / Figure 5 were
  regenerated with paper-facing display names and SVG outputs, and Figure 6 was
  layout-polished with one global legend and subcaptions below the columns. The
  scaffold compiled to 7 pages during the BG check.
- Stage 4-BI records a documentation-only plan for a deeper
  nature-skills-assisted presentation / prose polish pass after manual
  inspection found that Figure 1 / Figure 2 and some code-like / AI-like prose
  remain active blockers before final submission readiness.
- Stage 4-BJ replaces the active Figure 1 / Figure 2 TikZ schematic inputs
  with deterministic nature-style matplotlib SVG / PDF / PNG assets. The old
  TikZ files remain as historical scaffold assets, and final human visual
  inspection remains pending.
- No fabricated citations were added.
- No `risk_adapter_v22` was created.

## Claim Boundaries

- No `risk_adapter_v21` overall-best claim.
- No mixed-protocol aggregate as the main result.
- No statistical significance claim.
- No safety guarantee.
- No broad real-world deployment claim.
- Failure groups are diagnostic only.
- Risk scores are empirical strict-invalid warning scores, not calibrated
  physical probabilities unless final calibration evidence is added.
- No `risk_adapter_v22`.

## Local Structure

- `main.tex`: RA-L-oriented top-level manuscript scaffold.
- `refs.bib`: copied ready-to-use bibliography entries from the source
  scaffold.
- `sections/`: copied manuscript sections.
- `figures/`: copied paper figure assets.
- `tables/`: copied Table 1 source.
- `supplementary/`: supplementary planning placeholder.
- `ieeeconf.cls`: copied from `paper/templates/ral/`.

## Remaining TODOs

- Fill final author names and affiliations.
- Confirm official RA-L / IEEE template requirements if the final submission
  target differs from the provided `ieeeconf` template.
- Use Stage 4-AV2 as the current compile/check baseline.
- Check final page limit.
- Visually inspect the simplified Figure 6 layout in the compiled PDF after
  Stage 4-BD.
- Verify conditional citations before adding any missing metadata or active
  BibTeX entries.
- Use Stage 4-AX as the current final claim-audit baseline.
- Use Stage 4-AY as the current final compile / submission package checklist
  baseline.
- Use Stage 4-AZ as the current human visual inspection baseline.
- Use Stage 4-BA as the current manuscript-visible display-name cleanup
  baseline.
- Use Stage 4-BB as the current Figure 1 / Figure 2 placeholder and redraw
  workflow baseline.
- Use Stage 4-BC as the current Figure 3 compact polish baseline.
- Use Stage 4-BD as the current Figure 6 simplified replot baseline.
- Use Stage 4-BE as the current Figure 1 / Figure 2 vector schematic
  replacement baseline.
- Use Stage 4-BF as the current presentation blocker fix baseline.
- Use Stage 4-BG as the current paper-facing presentation polish baseline.
- Use Stage 4-BI as the current nature-skills-assisted Figure 1 / Figure 2 and
  prose polish planning baseline.
- Use Stage 4-BJ as the current active Figure 1 / Figure 2 nature-style
  schematic baseline, pending final visual inspection.
- Next presentation-polish sequence:
  - Stage 4-BK RA-L prose polishing / de-AI pass using a
    `nature-polishing`-inspired workflow;
  - Stage 4-BL compile and visual inspection after BJ / BK.
- Perform final submission package assembly only after the AZ blockers are
  resolved or explicitly accepted.
- Keep generated PDF / aux / log files out of git.
