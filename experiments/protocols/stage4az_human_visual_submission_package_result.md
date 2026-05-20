# Stage 4-AZ Human Visual Submission Package Result

## Executive Summary

Stage 4-AZ records the human visual inspection findings after manual review of
the RA-L-oriented Paper 1 PDF generated in Stage 4-AY.

The compile/package check in Stage 4-AY succeeded, but the manual PDF review
identified presentation blockers that must be addressed before submission.
These blockers do not change the scientific result, method ranking, claim
boundary, citation state, or evaluation evidence. They are manuscript
presentation and figure-quality issues.

No manuscript scientific claims were changed in AZ. No LaTeX compile was run,
no figures were regenerated, no simulations / training / ROS actions were run,
and `risk_adapter_v22` was not created.

## Inspected PDF Context

The inspected PDF was the Stage 4-AY temporary inspection copy:

```text
/tmp/stage4_governor_ral_final_check.pdf
```

Stage 4-AY recorded that the RA-L scaffold compiled successfully with
`latexmk_exit=0`, generated an 8-page PDF, and had no LaTeX errors, undefined
citations, undefined references, overfull hboxes, missing figures,
bibliography warnings, or float warnings. Stage 4-AZ starts from that clean
compile state and records human visual readiness findings.

## Ranked Human-Review Issues

1. Manuscript-wide raw token / underscore naming problem.
2. Figure 1 / Figure 2 are not ready as final paper schematics.
3. Figure 3 content is acceptable, but the current plot is too spacious.
4. Figure 6 is visually overcrowded and needs a simplified paper-facing
   treatment.

## Issue 1: Manuscript-Wide Raw Token / Underscore Naming Problem

Raw internal method tokens are still visible throughout the manuscript and
figures. Examples include:

- `risk_adapter_v21`
- `fixed_s080`
- `windlevel_s085`

This appears in the abstract, body text, captions, and figure labels / legends.
The current naming style is useful internally, but it reads as implementation
metadata rather than polished paper terminology.

Recommended next action:

- Stage 4-BA should define paper-facing display names for all methods.
- The cleanup should preserve exact internal IDs in a mapping table or first-use
  parenthetical, while replacing repeated raw tokens in visible prose,
  captions, legends, and labels where feasible.
- The cleanup should not change numerical results, rankings, claim boundaries,
  or citation keys.

## Issue 2: Figure 1 / Figure 2 Not Ready

Figure 1 and Figure 2 are not acceptable as final paper schematics in their
current form. They should be redrawn later using an external illustration tool.

The current schematic visuals are useful placeholders for scaffold development,
but they do not yet have final-paper visual quality. Before the external redraw
is available, the manuscript should use explicit placeholders rather than keep
low-quality current schematics as if they are final assets.

Recommended next action:

- Stage 4-BB should replace Figure 1 / Figure 2 with manuscript placeholders
  and write the redraw specification.
- The redraw should be external-tool driven.
- The placeholder swap should make the submission-readiness status clear
  without changing scientific content.

## Issue 3: Figure 3 Too Spacious

Figure 3 content is acceptable, but the current plot is visually sparse.

Main visual issues:

- redundant in-plot title;
- raw token labels;
- canvas too large for the small number of points;
- plot should be visually compacted in a later figure-polish stage.

Recommended next action:

- Stage 4-BC should compact Figure 3.
- Remove redundant in-plot title if the caption already carries the meaning.
- Replace raw labels with paper-facing display names once Stage 4-BA defines
  them.
- Keep the same data points, protocol axes, and Pareto / frontier meaning.

## Issue 4: Figure 6 Overcrowded

Figure 6 is too visually crowded for the main paper in its current style.

Main visual issues:

- too many stacked signal rows per panel;
- very small text / legends;
- raw underscore labels in panel titles and legends;
- trace content needs a simplified paper-facing style;
- likely only key signals should remain in the main paper;
- some full trace content may need to move to supplementary material.

Recommended next action:

- Stage 4-BD should create a Figure 6 paper-facing replot plan.
- The plan should identify the key signals needed in the main paper.
- Full trace detail should be considered for supplementary material.
- Replotting must preserve the case-study interpretation and claim caveats:
  representative traces are qualitative mechanism evidence only, not
  population-level causal evidence.

## Why These Are Presentation Blockers

These findings are presentation blockers rather than scientific-result
blockers because:

- the Stage 4-AY compile succeeded;
- the evidence tables, method rankings, and claim boundaries remain unchanged;
- the active citation cleanup remains valid;
- the claim audit remains valid;
- no issue changes the strict-valid counts, protocol regret values, or method
  roles;
- the problems affect readability, polish, and submission-facing visual quality.

The manuscript should not proceed to final RA-L submission until these
presentation blockers are resolved or explicitly accepted by the team.

## Recommended Next-Stage Sequence

Recommended order:

1. Stage 4-BA: manuscript-visible display-name cleanup.
2. Stage 4-BB: Figure 1 / Figure 2 placeholder swap and redraw plan.
3. Stage 4-BC: Figure 3 compactness polish.
4. Stage 4-BD: Figure 6 paper-facing replot plan.

These stages should remain presentation-focused. They should not introduce new
experiments, new methods, new claims, new citations, or `risk_adapter_v22`.

## Explicit Scope Statement

- No manuscript scientific claims changed.
- No LaTeX compile was run.
- No figures were regenerated.
- No simulations / training / ROS actions were run.
- No `roslaunch`, RViz, `catkin_make`, or figure generation scripts were run.
- No `risk_adapter_v22` was created.

Continue: no `risk_adapter_v22` before Paper 1 RA-L submission.
