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
- Visually inspect Figure 6 layout in the compiled PDF.
- Verify conditional citations before adding any missing metadata or active
  BibTeX entries.
- Polish final captions.
- Run final claim audit before submission.
- Keep generated PDF / aux / log files out of git.
