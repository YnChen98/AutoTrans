# Stage 4-AQ LaTeX Compile / Check Result

## Executive Summary

Stage 4-AQ is the first LaTeX compile/check pass for the Stage 4 manuscript
scaffold under `paper/stage4_governor/`.

The scaffold was inspected, but the local LaTeX toolchain is not available in
this environment. Both the preferred `latexmk` command and the fallback
`pdflatex` command failed before manuscript compilation began because the
commands are not installed. No PDF was produced, no auxiliary LaTeX files were
generated, and no manuscript-formatting fixes were required in this pass.

This is the first compile/check pass, not final manuscript formatting.

## Commands Run

Scaffold inspection:

```bash
find paper/stage4_governor -maxdepth 3 -type f | sort
sed -n '1,220p' paper/stage4_governor/main.tex
sed -n '1,160p' paper/stage4_governor/tables/table1_protocol_balanced_robustness.tex
```

Tool availability check:

```bash
command -v latexmk || true
command -v pdflatex || true
command -v bibtex || true
```

Preferred compile command:

```bash
cd paper/stage4_governor
latexmk -pdf -interaction=nonstopmode main.tex
```

Result:

```text
/bin/bash: latexmk: command not found
```

Fallback compile command:

```bash
cd paper/stage4_governor
pdflatex -interaction=nonstopmode main.tex
```

Result:

```text
/bin/bash: pdflatex: command not found
```

Fallback bibliography command:

```bash
cd paper/stage4_governor
bibtex main || true
```

Result:

```text
/bin/bash: bibtex: command not found
```

## Compile Status

- Compile succeeded: no.
- Reason: local LaTeX tools are unavailable.
- Preferred tool unavailable: `latexmk`.
- Fallback tools unavailable: `pdflatex`, `bibtex`.
- Output PDF path: none created.

## Major Warnings / Errors

The only blocking errors observed were missing executable errors:

- `latexmk: command not found`
- `pdflatex: command not found`
- `bibtex: command not found`

No LaTeX syntax errors, missing package errors, figure path errors,
bibliography style errors, or overfull layout warnings could be evaluated
because compilation did not start.

## Fixes Made

No manuscript source fixes were made in Stage 4-AQ because the compile pass was
blocked by missing local tools rather than by manuscript syntax or formatting
errors.

Files inspected:

- `paper/stage4_governor/main.tex`
- `paper/stage4_governor/tables/table1_protocol_balanced_robustness.tex`
- `paper/stage4_governor/refs.bib`
- `paper/stage4_governor/sections/*.tex`
- copied figure assets under `paper/stage4_governor/figures/`

## Unresolved TODOs

- Install or make available a LaTeX toolchain with `latexmk`, `pdflatex`, and
  `bibtex`, then rerun the compile/check pass.
- Confirm whether the final target is IROS / ICRA or RA-L before final
  template cleanup.
- Verify conditional citations before final bibliography insertion:
  - `Barikbin2019WindPayloadTracking`
  - `Wabersich2021PredictiveSafetyFilter`
  - `Jin2025NeuralPredictorPayload`
  - `Monteleone2023BalanceResilienceBenchmark`
  - `Dogga2023AutoARTS`
- After compilation is available, check Figure 6 sizing and table width in the
  generated PDF.
- Do not introduce `risk_adapter_v22`.

## Next Recommended Step

Recommended next step:

- Stage 4-AQ2 or Stage 4-AR: rerun compile/check in an environment with LaTeX
  installed, then fix only manuscript-formatting issues found by the compiler.

Alternative next step:

- Stage 4-AM5: verify remaining conditional citation metadata before final
  bibliography cleanup.
