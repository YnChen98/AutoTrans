# Stage 4-BK RA-L Prose Polishing Result

## Executive Summary

Stage 4-BK applies a controlled RA-L prose-polishing / de-AI pass to the active
Paper 1 manuscript under `paper/stage4_governor_ral/`. The pass improves
reader-facing clarity, reduces code-like wording, and removes formulaic
phrasing while preserving scientific claims, numerical results, citations,
limitations, method rankings, figure/table references, and the Paper 1
no-`risk_adapter_v22` boundary.

No experiments, simulations, ROS processes, training scripts, figure-generation
scripts, or algorithm changes were run.

## nature-polishing Guidance Source Inspected

The external skills repository was cloned to `/tmp/nature-skills` and inspected
before manuscript edits. The relevant `nature-polishing` guidance was found and
read at:

- `/tmp/nature-skills/skills/nature-polishing/SKILL.md`
- `/tmp/nature-skills/skills/nature-polishing/references/writing-strategy.md`
- `/tmp/nature-skills/skills/nature-polishing/references/section-moves.md`
- `/tmp/nature-skills/skills/nature-polishing/references/phrasebank-playbook.md`
- `/tmp/nature-skills/skills/nature-polishing/references/style-guardrails.md`

The local Codex skill file
`/home/cccyn2004/.codex/skills/nature-polishing/SKILL.md` was also inspected.
The guidance was used only for clarity, concision, precise hedging, and
paper-facing terminology. The manuscript was not converted into a Nature house
style rewrite, and IEEE / RA-L technical style was preserved.

## Polishing Scope

Edited active manuscript files:

- `paper/stage4_governor_ral/main.tex`
- `paper/stage4_governor_ral/sections/01_intro.tex`
- `paper/stage4_governor_ral/sections/02_related_work.tex`
- `paper/stage4_governor_ral/sections/03_method.tex`
- `paper/stage4_governor_ral/sections/04_experiments.tex`
- `paper/stage4_governor_ral/sections/05_results.tex`
- `paper/stage4_governor_ral/sections/06_discussion.tex`
- `paper/stage4_governor_ral/sections/07_conclusion.tex`

Updated status / planning files:

- `paper/stage4_governor_ral/README.md`
- `experiments/protocols/stage4bi_nature_skills_presentation_polish_plan.md`
- `experiments/protocols/stage4at2_ral_submission_readiness_checklist.md`
- `experiments/scripts/README.md`
- `AGENTS.md`

## Sections Edited

- Abstract: reduced repetition and code-like phrasing while preserving all
  quantitative results and caveats.
- Introduction: made the motivation more direct and tightened the contribution
  bullets without changing claims.
- Related Work: smoothed transitions and softened broad insufficiency framing
  without adding or removing citations.
- Method: replaced implementation-facing phrases with paper-facing terms such
  as 3 s and 5 s warning scores, serialized logistic-regression classifiers,
  speed scale, acceleration scale, and strict-invalid label.
- Experimental Setup: replaced raw protocol wording with single-goal mission
  and goal-reissue stress terminology while preserving strict-valid criteria.
- Results: tightened protocol-split, balanced-regret, failure-group, and trace
  interpretation prose without changing counts or rankings.
- Discussion and Conclusion: reduced repetitive caveat phrasing while keeping
  simulation-only, empirical-governor, no-significance, no-safety-guarantee,
  and no-hardware-transfer limitations.

## Examples of Wording Categories Improved

Code-like wording:

- Replaced raw implementation-style terms with paper-facing descriptions where
  exact code names were not needed.
- Kept mathematical notation only where it clarifies the governor interface.

Formulaic AI-like phrasing:

- Reworked generic contribution and transition language into more direct
  claims tied to the tested protocols and evidence.
- Avoided promotional phrasing and broad novelty claims.

Over-defensive caveat repetition:

- Consolidated repeated no-claim caveats into bounded, readable statements.
- Preserved the substantive caveats rather than deleting them.

Paper-facing terminology:

- Used single-goal mission protocol and goal-reissue stress protocol.
- Used empirical strict-invalid warning scores rather than calibrated
  probability language.
- Used learned / risk-conditioned execution governor and balanced method
  framing for Risk Adapter v1.

## Claims Preserved

- Risk Adapter v1 remains the most balanced learned / risk-conditioned method
  under the tested two-protocol evaluation by mean valid count,
  worst-protocol valid count, and total regret.
- Wind-Level 0.85 remains the highest observed single-goal strict-valid method
  in the evaluated set.
- Fixed Scale 0.80 remains the highest observed goal-reissue stress strict-valid
  method in the evaluated set.
- Protocol-split reporting remains the central reason that trade-offs are not
  collapsed into a single mixed aggregate.
- Failure groups remain diagnostic labels, not exact physical root-cause proof.
- Representative traces remain qualitative mechanism evidence, not
  population-level causality proof.
- Risk scores remain empirical strict-invalid warning scores, not calibrated
  physical probabilities.
- No formal safety guarantee, statistical significance claim, or broad
  real-world deployment / hardware-transfer claim was introduced.

## Quantitative Values Preserved

The prose pass preserved the paper-facing values and rankings, including:

- Wind-Level 0.85: `26/30` single-goal strict-valid runs.
- Fixed Scale 0.80: `24/30` goal-reissue stress strict-valid runs.
- Risk Adapter v1: `24.0/30` mean valid count.
- Risk Adapter v1: `23/30` worst-protocol valid count.
- Risk Adapter v1: total regret `2`.
- Risk Adapter v2.1: strong nominal / single-goal variant framing, not a
  cross-protocol final winner.

## Citation Status

No citations were added, removed, or replaced. The active citation keys remain
unchanged, and `paper/stage4_governor_ral/refs.bib` was not modified.

## Raw / Code-Like Wording Check Result

The requested active-manuscript search was run for:

```bash
\texttt
_
JSON LogisticRegression
LogisticRegression
goal_repeat
speed_scale
acceleration_scale
risk_score
label_strict_invalid
command_control_upstream
planner_reference_upstream
state_task_upstream
risk_adapter
fixed_s080
fixed_s085
windlevel
```

Remaining matches are LaTeX structural commands / labels and mathematical
notation, such as `\input`, `\includegraphics`, `\label`, `$r_3$`, `$r_5$`,
`$u_{\mathrm{ref}}$`, `$s_v$`, `$s_a$`, and `$u_{\mathrm{exec}}$`. No active
prose matches remain for the raw method / field tokens listed above.

## Compile Result

The RA-L scaffold was compiled with:

```bash
cd paper/stage4_governor_ral
rm -f main.aux main.bbl main.blg main.fdb_latexmk main.fls main.log \
  main.out main.pdf main.synctex.gz bibtex.log
latexmk -pdf -interaction=nonstopmode -file-line-error main.tex
```

Result: `latexmk` exited successfully with `exit code 0` and generated a
7-page `main.pdf` during the check.

## Warning / Error Summary

Final log inspection found:

- LaTeX errors: none.
- Undefined citations: none.
- Undefined references: none.
- Overfull hboxes: none.
- Missing figures: none.
- Bibliography warnings: none.
- Float warnings: none.
- Residual non-blocking messages: five `Underfull \hbox` messages.

Generated LaTeX output files were cleaned before commit.

## Remaining TODOs

- Final visual inspection after the prose polish.
- Final visual / claim check after BJ/BK.
- Fill final author metadata.
- Source / PDF package assembly.

## Scope Boundaries

- No scientific claim changed.
- No numerical result changed.
- No citation changed.
- No experiment run.
- No simulation / ROS / training.
- No figure-generation script run.
- No algorithm, planner, controller, or simulator change.
- No `risk_adapter_v22`.
