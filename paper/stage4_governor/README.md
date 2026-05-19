# Stage 4 Governor Manuscript Scaffold

## Purpose

This directory is the Stage 4-AP manuscript source scaffold for the reframed
Stage 4 paper. It converts the assembled Stage 4 draft into an IROS / ICRA-like
LaTeX draft skeleton while keeping RA-L extension possible.

This scaffold is a draft source package, not a submission-ready manuscript. No
LaTeX compilation has been run.

Stage 4-AS now sets Paper 1's first target to RA-L, with `risk_adapter_v1` as
the protagonist. Stage 4-AT tracks RA-L conversion and submission readiness in
`experiments/protocols/stage4at_ral_conversion_submission_audit.md`. This
directory remains pre-RA-L-conversion until Stage 4-AV or a later explicit
template-conversion task.

Stage 4-AU documents the Paper 1 risk-score interface, `risk_adapter_v1`
governor logic, strict-valid metric, and diagnostic failure-label boundary in
`experiments/protocols/stage4au_risk_score_metric_documentation.md`.

## Target Style

- Current drafting style: IROS / ICRA-like conference skeleton.
- Paper 1 target: RA-L.
- TODO before submission: replace the draft `ieeeconf` setup with the official
  RA-L / IEEE template.
- Do not rewrite the manuscript template in Stage 4-AT; that stage is an
  audit / readiness plan only.

## Figure And Table Sources

Main figure assets were copied from:

`experiments/results/stage4_paper_figure_package/main/`

into:

`paper/stage4_governor/figures/`

The main table source is:

`paper/stage4_governor/tables/table1_protocol_balanced_robustness.tex`

## Citation Source

`refs.bib` uses only ready-to-use BibTeX draft blocks from:

`experiments/protocols/stage4am4_bibtex_draft.md`

Conditional citations are not active BibTeX entries in this scaffold.

## Conditional Citation TODOs

Verify before final bibliography insertion:

- `Barikbin2019WindPayloadTracking`
- `Wabersich2021PredictiveSafetyFilter`
- `Jin2025NeuralPredictorPayload`
- `Monteleone2023BalanceResilienceBenchmark`
- `Dogga2023AutoARTS`

## Claim Boundaries

- No `risk_adapter_v21` overall-best claim.
- No mixed-protocol aggregate as the main result.
- No statistical significance claim.
- No safety guarantee.
- No broad real-world deployment claim.
- Failure groups are diagnostic only.
- Risk scores are not claimed to be calibrated unless final deployed model
  calibration is documented.
- No `risk_adapter_v22`.

## Local Draft Structure

- `main.tex`: draft top-level manuscript file.
- `refs.bib`: provisional ready-to-use bibliography entries.
- `sections/`: modular manuscript sections.
- `figures/`: copied paper-ready figure assets.
- `tables/`: LaTeX table scaffold.
- `supplementary/`: placeholder for future supplementary material.
