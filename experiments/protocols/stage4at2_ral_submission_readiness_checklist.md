# Stage 4-AT2 RA-L Submission Readiness Checklist

## Executive Summary

Stage 4-AT2 is the RA-L submission readiness checklist after the clean Stage
4-AR manuscript compile / layout pass.

The manuscript currently compiles to 8 pages under the current tracked
template. The Stage 4-AR compile recorded `latexmk_exit=0`, generated
`main.pdf`, and found no LaTeX errors, undefined citations, undefined
references, overfull hboxes, missing figures, bibliography warnings, or float
warnings in the final log.

This is not final submission yet. AT2 records what is ready, what remains
mandatory before submission, what is optional if time allows, and what should
stay outside Paper 1.

No `risk_adapter_v22` is allowed before Paper 1 RA-L submission unless the
submission strategy is explicitly changed.

Stage 4-AV is the first template-conversion scaffold step after this
submission checklist. It creates a separate RA-L-oriented scaffold under
`paper/stage4_governor_ral/` while preserving the existing
`paper/stage4_governor/` scaffold unchanged.

Stage 4-AV2 is the RA-L scaffold compile check for
`paper/stage4_governor_ral/`. It records whether the new scaffold compiles,
the generated PDF page count, and remaining warnings / submission TODOs.

Stage 4-AM5 addresses the conditional citation decision / BibTeX cleanup item
for the active RA-L scaffold by confirming that active citations and active
`refs.bib` entries match and that unresolved conditional citation keys remain
excluded from active Paper 1 citations / BibTeX entries.

Stage 4-AW addresses the final figure / caption polish item for the active
RA-L scaffold. It updates Table 1 and Figures 2-4 / 6 caption text, preserves
claim boundaries, and recompiles the scaffold to 8 pages. Final visual PDF
inspection remains a submission TODO.

Stage 4-AX addresses the final claim audit item for the active RA-L scaffold.
It checks manuscript text for overclaiming risk, removes active
`risk_adapter_v22` wording from the manuscript, and preserves the bounded
balanced-protagonist claim for `risk_adapter_v1`.

Stage 4-AY performs the final compile / submission package check. It confirms
that the RA-L scaffold compiles to an 8-page PDF after AX, records a temporary
inspection copy under `/tmp/stage4_governor_ral_final_check.pdf`, and tracks
the remaining human-only submission tasks.

Stage 4-AZ records human visual inspection findings after the clean AY compile.
It confirms that compile success does not yet mean visual-submission readiness:
raw underscore-style method names, Figure 1 / Figure 2 schematic quality,
Figure 3 compactness, and Figure 6 overcrowding remain presentation blockers.

Stage 4-BA addresses the manuscript-visible raw-token naming blocker by
replacing active prose, captions, panel labels, and Table 1 method labels with
paper-facing display names. Figure-internal raw labels remain for the
figure-specific Stage 4-BC / Stage 4-BD polish steps.

## Current Ready Items

- Manuscript scaffold created under `paper/stage4_governor/`.
- Official class file is present in the scaffold.
- Clean compile achieved in Stage 4-AR.
- Current manuscript compiles to 8 pages under the current template.
- Main figures and tables are present.
- Table 1 and Figures 1-6 are ready at scaffold level.
- Citations have been drafted.
- Risk score / metric documentation has been created.
- Risk model artifact checksums have been recorded.
- Paper strategy is fixed: RA-L first.
- Paper 1 protagonist is `risk_adapter_v1`.
- `windlevel_s085` is the single-goal specialist.
- `fixed_s080` is the goal-reissue stress specialist.
- `risk_adapter_v21` remains an ablation / strong nominal variant, not the
  final Paper 1 method.

## Remaining Must-Fix Before Submission

- Confirm the final RA-L / IEEE template requirement and page budget.
- Perform visual PDF inspection: first pass recorded by Stage 4-AZ, with
  presentation blockers still open.
- Fill final author names and affiliations.
- Perform final title check.
- Complete final citation style polish if venue-specific formatting requires
  it.
- Conditional citation decision / BibTeX cleanup: addressed by Stage 4-AM5 for
  the active RA-L scaffold; unresolved conditional keys remain excluded unless
  later verified.
- Final figure / caption polish for Table 1 and Figures 1-6: addressed by
  Stage 4-AW.
- Check final Figure 6 visual readability in the compiled PDF during final
  visual inspection: Stage 4-AZ found Figure 6 overcrowded and recommended a
  simplified paper-facing replot plan.
- Final claim audit: addressed by Stage 4-AX:
  - no statistical significance claim;
  - no formal safety guarantee;
  - no broad real-world deployment claim;
  - no learned-method uniform domination claim;
  - no `risk_adapter_v21` overall-best claim;
  - no mixed-protocol aggregate as the main result;
  - no calibrated-probability claim for risk scores unless calibration is
    documented;
  - no active manuscript `risk_adapter_v22` wording.
- Decide the supplementary package boundary for the risk model JSON artifacts
  and dataset checksum manifest.
- Decide whether the generated PDF belongs in the submission package only, not
  in git.
- Final compile / submission package check: addressed by Stage 4-AY.
- Confirm generated experiment outputs are not accidentally committed.
- Resolve Stage 4-AZ presentation blockers before final submission:
  - manuscript-visible display-name cleanup: addressed by Stage 4-BA;
  - Figure 1 / Figure 2 placeholder swap and redraw plan;
  - Figure 3 compactness polish;
  - Figure 6 simplified paper-facing replot plan.

## Remaining Should-Fix If Time Allows

These items are useful but not required unless the team chooses to strengthen
RA-L before submission.

- Paired / blocked analysis over the repeated-run design.
- Fixed-scale frontier summary beyond the current `fixed_s080` reference.
- Channel ablation:
  - speed-only;
  - acceleration-only;
  - combined `speed_scale` / `acceleration_scale`.
- Risk calibration / lead-time plan.
- Efficiency metrics:
  - arrival time;
  - mission time;
  - peak swing;
  - peak speed;
  - time under low scale.
- `goal_repeat` curve for `1/3/5/10`.

If these cannot be completed cleanly before RA-L timing, keep them as
limitations, supplementary notes, or Paper 2 extension directions rather than
creating `risk_adapter_v22`.

## RA-L Risk Register

| risk | submission concern | required handling |
| --- | --- | --- |
| Simulation-only evidence | Reviewers may ask whether the result transfers to hardware. | Keep claims bounded to tested simulation protocols and avoid deployment wording. |
| No statistical significance | Repeated-run counts are descriptive. | Avoid significance wording unless a valid paired / blocked analysis is added. |
| No formal safety guarantee | The governor is empirical, not a certified safety filter. | Do not claim safety guarantees or formal invariance. |
| Risk scores not calibrated probabilities | Current scores are empirical strict-invalid warning scores. | Avoid probability wording unless calibration evidence is added. |
| Strong simple baselines | `windlevel_s085` and `fixed_s080` are strong specialists. | Frame Paper 1 around balanced robustness / protocol regret with `risk_adapter_v1`. |
| 8-page budget pressure | Final template or author/caption changes may force cuts. | Inspect final PDF and move details to supplementary material if needed. |
| Failure groups diagnostic only | Failure labels are useful but not perfect root-cause proof. | Present them as diagnostic support, not as definitive causality. |
| Paper 2 overlap risk | A later extension could look incremental. | Keep Paper 2 mechanism-driven and substantially new; cite Paper 1 if appropriate. |

## Submission Package Checklist

- Final PDF.
- Source files.
- Figures.
- `refs.bib`.
- Supplementary material if used.
- Optional video / trace package.
- Code / data availability statement if needed.
- Final check that generated experiment outputs are not accidentally committed:
  - no CSV files;
  - no PNG files from generated experiment outputs;
  - no TXT log / output files;
  - no generated PDF / aux / log files;
  - no files under `experiments/results/`, `experiments/models/`, or
    `experiments/datasets/`;
  - no files under `build/`, `devel/`, or `install/`.

## Paper 2 Boundary

Do not add `risk_adapter_v22` to Paper 1.

Paper 2 may later introduce a mechanism-driven final governor, broader
protocol family, calibration / ablation / generalization evidence, and optional
HIL or minimal hardware evidence if it supports the mechanism story.

Paper 2 must be substantially new and should cite Paper 1 if Paper 1 is
submitted or published.

## Recommended Next Stage

Recommended submission-readiness path:

1. Stage 4-AV RA-L template conversion scaffold.
2. Stage 4-AV2 RA-L scaffold compile/check pass.
3. Stage 4-AM5 conditional citation verification and BibTeX cleanup.
4. Stage 4-AW final figure / caption polish.
5. Stage 4-AX final claim audit.
6. Stage 4-AY final compile / submission package check.
7. Stage 4-AZ human visual PDF inspection finding record.
8. Stage 4-BA through Stage 4-BD presentation-polish follow-ups.

Suggested order:

```text
AV -> AV2 -> AM5 -> AW -> AX -> AY -> AZ -> BA -> BB -> BC -> BD
```

Continue: no `risk_adapter_v22` before Paper 1 RA-L submission.

After Stage 4-AZ, continue with Stage 4-BA display-name cleanup, Stage 4-BB
schematic placeholder / redraw preparation, Stage 4-BC Figure 3 compact polish,
and Stage 4-BD Figure 6 simplified replot planning before final submission
package assembly.
