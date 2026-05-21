# Stage 4-BI Nature-Skills Presentation and Prose Polish Plan

## Executive Summary

Stage 4-BI defines a documentation-only integration plan for using
`nature-figure` and `nature-polishing` as guidance for the next RA-L Paper 1
presentation polish steps.

Manual inspection after Stage 4-BG found that the active RA-L scaffold still
has presentation blockers: Figure 1 is not final, Figure 2 is not final, and
some manuscript prose still reads as code-like or AI-like. Stage 4-BI does not
change the manuscript, figures, experiments, algorithms, citations, or data. It
only records how to use the nature-skills workflow in the next stages.

The next execution stages should be:

- Stage 4-BJ: Figure 1 / Figure 2 redesign using a `nature-figure`-inspired
  editable schematic style.
- Stage 4-BK: RA-L prose polishing / de-AI pass using a
  `nature-polishing`-inspired workflow.
- Stage 4-BL: compile and visual inspection after both presentation passes.

Continue: no `risk_adapter_v22` before Paper 1 RA-L submission.

Stage 4-BJ now executes the Figure 1 / Figure 2 redesign branch defined here:
it replaces the active TikZ schematics with deterministic, paper-facing
matplotlib SVG / PDF / PNG assets while preserving the scientific claims,
protocol definitions, and method rankings.

## Why Stage 4-BI Is Needed

Stage 4-BG improved the active paper-facing presentation by redrawing Figure 1
and Figure 2 TikZ schematics, regenerating Figure 4 and Figure 5 with
paper-facing display names, and polishing Figure 6. However, human inspection
after BG still found that compile success and static checks are not enough for
submission readiness.

The remaining issues are not scientific-content issues. They are visual
communication and prose-quality issues that can affect reviewer trust even when
the underlying results are unchanged. Stage 4-BI therefore creates a controlled
plan for a deeper presentation pass without expanding claims or creating new
method variants.

## Current Blockers

- Figure 1 is not final:
  - arrow / line / box layout still needs improvement;
  - the architecture path should be cleaner and easier to scan;
  - feedback and diagnostic paths should not compete with the main pipeline.
- Figure 2 is not final:
  - timeline labels and arrows still risk overlap;
  - visual clutter can obscure the protocol distinction;
  - the schematic should define protocols, not imply result ranking.
- Prose still has code-like / AI-like style:
  - some wording still feels closer to implementation notes than RA-L prose;
  - some phrasing risks an AI-template tone;
  - the manuscript needs a final reader-facing polish pass without changing
    claims, citations, values, or caveats.

## `nature-figure` Usage Plan

Use `nature-figure` as design guidance for high-impact, editable,
non-redundant figures. For Stage 4-BJ, the target is not a generated result
plot. The target is a clear paper-facing schematic pair that supports the
Method and Experimental Setup narrative.

Stage 4-BJ should use the `nature-figure` workflow in this limited way:

- define the figure contract before drawing:
  - one-sentence purpose for each figure;
  - evidence / explanation role of each visual element;
  - review risks, including safety-guarantee and result-ranking implications;
  - export and editability requirements.
- treat Figure 1 and Figure 2 as schematic-led explanatory figures, not
  quantitative plots.
- prefer an editable target format:
  - SVG;
  - PDF with editable text when possible;
  - PPT-editable source if PowerPoint is used as the manual authoring tool.
- avoid raw AI-generated raster images as final paper assets.
- avoid decorative complexity that does not carry a unique explanatory role.
- preserve scientific content exactly:
  - no new algorithm block;
  - no new experimental claim;
  - no changed result ranking;
  - no changed protocol definition.

If Stage 4-BJ renders figures using Python or R, the `nature-figure` backend
selection rule should be handled at that stage before drawing. Stage 4-BI does
not choose or run a plotting backend because it is documentation-only.

## Figure 1 Redesign Target

Figure 1 should become a pipeline-like architecture figure.

Required visual target:

- aligned rectangular blocks;
- orthogonal arrows;
- no line crossing through text boxes;
- clear main path and feedback path;
- main command path visually dominant;
- feedback / diagnostic path visually secondary;
- compact text suitable for the RA-L two-column page;
- editable vector or source format.

Recommended content structure:

- main path:
  - planner / reference generator;
  - payload MPC;
  - SO(3) controller;
  - UAV + suspended payload.
- adaptation / governance path:
  - empirical strict-invalid warning scores;
  - risk-conditioned execution governor;
  - command-adaptation interface;
  - speed scale / acceleration scale effect.
- feedback / logging path:
  - state / task logs;
  - diagnostic outputs;
  - warning-score input.

Claim boundaries:

- no result ranking;
- no safety guarantee implication;
- no certified-safety-filter implication;
- no implication that the planner, payload MPC, or SO(3) controller was
  replaced;
- `risk_adapter_v1` remains the Paper 1 protagonist only under the already
  documented balanced robustness / protocol regret framing.

## Figure 2 Redesign Target

Figure 2 should become a two-panel protocol schematic.

Required visual target:

- two panels:
  - single-goal mission protocol;
  - goal-reissue stress protocol.
- minimal text;
- no overlapping labels;
- no timeline label / arrow collisions;
- explicit `goal repeat = 1`;
- explicit `goal repeat = 10`;
- visually clear separation between protocol definition and result reporting;
- editable vector or source format.

Recommended content structure:

- left panel:
  - one initial goal publish;
  - transport interval;
  - arrival / hold region;
  - `goal repeat = 1`.
- right panel:
  - initial goal publish;
  - repeated same-goal publish markers;
  - transport interval;
  - arrival / reissue interaction region;
  - `goal repeat = 10`.

Claim boundaries:

- report protocols separately;
- do not combine protocols into a mixed aggregate;
- do not make Figure 2 a result plot;
- do not encode method ranking, success counts, or protocol-oracle ordering in
  the schematic.

## `nature-polishing` Usage Plan

Use `nature-polishing` for prose polish, not for claim expansion. The paper is
an RA-L / IEEE robotics manuscript, so the polishing workflow should improve
reader-facing argument and sentence quality while preserving IEEE-style
technical restraint.

Stage 4-BK should use the `nature-polishing` workflow in this limited way:

- identify the paper type as an algorithmic / systems-method robotics paper;
- polish section logic before sentence-level wording when a paragraph reads as
  implementation chronology;
- reduce code-like wording in reader-facing prose;
- reduce AI-template phrasing, including overly generic transitions or
  inflated contribution language;
- preserve RA-L / IEEE robotics style;
- do not blindly convert the manuscript to Nature house style;
- do not blindly convert to British English if that conflicts with IEEE style;
- preserve all citations, numerical values, method names, claims, and caveats;
- keep bounded wording for:
  - no statistical significance claim;
  - no formal safety guarantee;
  - no broad real-world deployment claim;
  - no learned-method uniform domination claim;
  - no mixed-protocol aggregate as the main result.

Polishing should leave code-facing names unchanged where they are required for
reproducibility, file paths, topic names, parameter names, and artifact
identifiers.

## Proposed Execution Stages

### Stage 4-BJ: Figure 1 / Figure 2 Redesign

Goal: replace or revise the active Figure 1 / Figure 2 schematics using a
`nature-figure`-inspired design contract.

Expected output:

- revised Figure 1 source / vector asset;
- revised Figure 2 source / vector asset;
- result document recording design choices, boundaries, and verification;
- no scientific-content change.

Do not run new experiments. Do not alter algorithm logic. Do not imply a safety
guarantee.

### Stage 4-BK: RA-L Prose Polishing / De-AI Pass

Goal: polish the active RA-L Paper 1 prose using a `nature-polishing`-inspired
workflow while preserving all claims and evidence.

Expected output:

- focused manuscript prose edits;
- before / after claim-boundary audit;
- no citation fabrication;
- no changed numbers, method rankings, or protocol conclusions.

Do not rewrite the manuscript into a Nature article. Preserve RA-L / IEEE
robotics style.

### Stage 4-BL: Compile and Visual Inspection

Goal: compile and inspect the RA-L scaffold after BJ and BK are both complete.

Expected output:

- clean compile result if a LaTeX run is explicitly allowed in that future
  stage;
- visual inspection notes for Figure 1, Figure 2, and polished prose;
- final blocker list before submission packaging.

Stage 4-BI itself does not compile LaTeX.

## Boundaries

- No new experiments.
- No algorithm change.
- No `risk_adapter_v22`.
- No claim strengthening.
- No fabricated citations.
- No unverified data.
- No changed numerical values.
- No changed method rankings.
- No changed protocol definitions.
- No raw AI-generated raster images as final paper assets.
- No manuscript text or figure edits in Stage 4-BI itself.

## Verification Scope for Stage 4-BI

Stage 4-BI is documentation-only. Verification should be limited to Markdown
inspection and git static checks:

```bash
git diff --check
git diff --cached --check
git status --short
```

No LaTeX compile, simulation, RViz, `roslaunch`, `catkin_make`, training
script, or figure generation script should be run in this stage.
