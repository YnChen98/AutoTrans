# Stage 4-AM Citation Collection Plan

## Executive Summary

Stage 4-AM defines the citation collection workflow for the assembled Stage 4
paper draft. It follows the citation slot map in
`experiments/protocols/stage4ak_citation_references_plan.md`.
Stage 4-AL now tracks the parallel final figure/table generation plan:
`experiments/protocols/stage4al_final_figure_generation_plan.md`.
Stage 4-AM2 now records the user-provided verified citation collection result:
`experiments/protocols/stage4am2_verified_citation_collection_result.md`.

This document does not finalize the bibliography, does not generate BibTeX,
and does not insert unverified references. It defines what sources must be
collected, verified, and mapped to the paper before final manuscript assembly.

All exact paper metadata should remain `TODO` until verified from a primary
source, official project page, publisher page, arXiv page, DOI page, or
manually confirmed BibTeX entry. Do not fabricate paper titles, authors,
venues, years, DOIs, URLs, or BibTeX keys.

## Priority Citation Tiers

### Tier 1: Must-Have Before Submission

- AutoTrans / original suspended-payload stack paper or project.
- Suspended-payload UAV planning/control foundations.
- Payload MPC / NMPC for suspended loads.
- SO3 / geometric quadrotor control.
- Reference governor / runtime governor conceptual precedent.
- Robotics benchmarking / stress testing.
- Failure taxonomy / failure log analysis.

These citations support the paper's core problem framing, stack description,
method positioning, evaluation legitimacy, and diagnostic interpretation.

### Tier 2: Should-Have For Stronger Paper

- Learning-enhanced UAV robustness.
- Learned risk prediction / disturbance prediction.
- Safety filters for learned control.
- Aerial transport under wind.
- Sim-to-real / real-world suspended-payload transport systems.

These citations strengthen the learning and robustness positioning but should
not be used to overclaim that the current method is a formal safety filter,
real-world deployment result, or learned method that dominates all baselines.

### Tier 3: Optional Extension

- Broader runtime assurance literature.
- Robust/adaptive control under wind.
- Benchmark suite design.
- Field robotics failure case studies.

These references can improve Discussion and Future Work, but the paper should
not depend on them for the main claim.

## Citation Collection Table

| citation_slot | target_claim | section | priority | source_type_needed | candidate_source_if_known | metadata_status | action_required | insertion_location |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `[TODO: AutoTrans]` | The evaluated stack is AutoTrans-like and comes from an existing suspended-payload transport system. | Related Work 2.1, Method, Experimental Setup | Tier 1 | primary paper or official project / repository | HKUST-Aerial-Robotics/AutoTrans project; exact paper metadata TODO | TODO | Find official paper/project citation and verify metadata. | Related Work 2.1; Method stack paragraph; Experimental Setup |
| `[TODO: suspended-payload UAV planning]` | Suspended-payload UAV transport requires payload-aware planning because of coupled load dynamics. | Abstract / Introduction, Related Work 2.1 | Tier 1 | primary robotics planning papers | TODO | TODO | Collect foundational and recent suspended-payload planning references. | Introduction paragraph 1; Related Work 2.1 |
| `[TODO: payload-aware MPC]` | Payload MPC / NMPC is a relevant control approach for suspended loads. | Introduction, Related Work 2.1, Method | Tier 1 | primary MPC / NMPC papers for suspended loads | TODO | TODO | Collect payload MPC/NMPC references and verify exact terminology. | Related Work 2.1; Method stack description |
| `[TODO: SO3 / geometric quadrotor control]` | SO3 / geometric control is a relevant low-level quadrotor control foundation. | Related Work 2.1, Method | Tier 1 | primary SO3 / geometric control papers | TODO | TODO | Collect canonical SO3 / geometric control references. | Related Work 2.1; Method stack description |
| `[TODO: wind-disturbance suspended-payload UAV transport]` | Wind disturbance can affect tracking, swing, and transport robustness. | Introduction, Related Work 2.1, Experimental Setup | Tier 2 | wind-disturbance or robust suspended-payload transport papers | TODO | TODO | Collect wind / disturbance references or narrow wording to tested setup. | Introduction paragraph 1; Experimental Setup |
| `[TODO: reference governor]` | Reference governors provide conceptual precedent for runtime reference modification. | Related Work 2.2, Method, Discussion | Tier 1 | reference governor survey or primary papers | TODO | TODO | Collect canonical reference governor references. | Related Work 2.2; Method claim boundary |
| `[TODO: explicit reference governor]` | Explicit reference governors are a related runtime governance method. | Related Work 2.2 | Tier 1 | primary explicit reference governor papers | TODO | TODO | Collect exact explicit reference governor citation if used. | Related Work 2.2 |
| `[TODO: action governor]` | Action governors / command shaping are related to modifying execution commands online. | Related Work 2.2 | Tier 1 | action governor or command-governor papers | TODO | TODO | Collect action governor references or remove slot if not used. | Related Work 2.2 |
| `[TODO: command filtering for robotics]` | Command filters provide conceptual precedent for adapting commands without replacing the controller. | Related Work 2.2, Method | Tier 1 | robotics command filtering papers | TODO | TODO | Collect command filtering references or keep discussion generic. | Related Work 2.2; Method interface paragraph |
| `[TODO: runtime safety filter]` | Runtime safety filters are related but stronger because they aim at certified safety. | Related Work 2.2, Method, Discussion | Tier 1 | safety filter / runtime assurance papers | TODO | TODO | Collect runtime safety filter references and use to state distinction. | Related Work 2.2; Claim boundary |
| `[TODO: safety filters for learned control]` | Learned-control safety filters provide contrast for the empirical governor. | Related Work 2.2, Discussion / Limitations | Tier 2 | safety filters for learned control papers | TODO | TODO | Collect references only if the manuscript discusses learned-control safety. | Related Work 2.2; Limitations |
| `[TODO: learning-enhanced UAV control]` | Learning can support adaptive aerial control / robustness. | Related Work 2.3 | Tier 2 | learning-enhanced UAV control papers | TODO | TODO | Collect representative learning-enhanced UAV control references. | Related Work 2.3 |
| `[TODO: learned risk prediction]` | Learned risk prediction can support adaptive execution decisions. | Related Work 2.3, Method | Tier 2 | learned risk prediction papers | TODO | TODO | Collect risk prediction references; avoid claiming exact task match unless found. | Related Work 2.3; Method risk paragraph |
| `[TODO: learned disturbance or risk prediction]` | Disturbance/risk prediction is relevant to the risk-conditioned governor idea. | Related Work 2.3 | Tier 2 | learned disturbance or risk prediction papers | TODO | TODO | Collect representative references and keep wording broad. | Related Work 2.3 |
| `[TODO: disturbance-aware learning for UAVs]` | Disturbance-aware learning can improve aerial robustness. | Related Work 2.3, Future Work | Tier 2 | disturbance-aware learning papers | TODO | TODO | Collect if using disturbance-aware learning language. | Related Work 2.3; Discussion |
| `[TODO: hybrid learning + model-based control]` | Hybrid learning + model-based control is a relevant positioning category. | Related Work 2.3 | Tier 2 | hybrid learning/model-based control papers | TODO | TODO | Collect if manuscript keeps hybrid-control framing. | Related Work 2.3 |
| `[TODO: data-driven robustness in aerial robotics]` | Data-driven methods can support robustness analysis/adaptation. | Related Work 2.3 | Tier 2 | data-driven aerial robotics robustness papers | TODO | TODO | Collect representative references or keep as optional. | Related Work 2.3 |
| `[TODO: robotics benchmarking]` | Robotics robustness claims require careful benchmarking. | Related Work 2.4, Experimental Setup, Discussion | Tier 1 | robotics benchmarking papers/surveys | TODO | TODO | Collect benchmarking references supporting repeated protocol design. | Related Work 2.4; Experimental Setup |
| `[TODO: stress testing for autonomous systems]` | Stress protocols help expose failures hidden by nominal tests. | Introduction, Related Work 2.4, Experimental Setup | Tier 1 | autonomous-system stress-testing papers | TODO | TODO | Collect stress-testing references or phrase as this paper's design choice. | Introduction protocol paragraph; Related Work 2.4 |
| `[TODO: repeated-run robotics evaluation]` | Repeated runs improve robustness interpretation. | Related Work 2.4, Experimental Setup | Tier 1 | repeated-run evaluation / benchmarking papers | TODO | TODO | Collect references or keep claim internal to this evaluation. | Experimental Setup repeated-run paragraph |
| `[TODO: failure analysis / taxonomy]` | Failure taxonomy can support system diagnosis. | Related Work 2.4, Results, Discussion | Tier 1 | failure taxonomy / diagnostic analysis papers | TODO | TODO | Collect references and keep failure labels diagnostic. | Related Work 2.4; Results failure analysis |
| `[TODO: failure log analysis]` | Failure-log analysis can help interpret invalid runs. | Related Work 2.4, Results, Discussion | Tier 1 | failure log analysis papers | TODO | TODO | Collect references if using log-analysis framing. | Related Work 2.4; Discussion |

## BibTeX / Metadata Verification Checklist

For each collected source, verify and record:

- title
- authors
- venue
- year
- DOI or arXiv / official URL if available
- BibTeX key
- reason for citation
- exact claim supported
- whether it is a primary source

Minimum source-quality rules:

- Prefer primary papers, official project pages, publisher pages, arXiv pages,
  or official repository documentation.
- Do not cite secondary summaries unless the manuscript explicitly needs a
  survey.
- Do not infer metadata from memory.
- Do not insert a citation key into the manuscript until the metadata is
  verified.
- If a source is only partially verified, keep the citation slot as TODO.

## Paper Insertion Plan

### Introduction

Insert citation slots for:

- `[TODO: suspended-payload UAV planning]`
- `[TODO: payload-aware MPC]`
- `[TODO: SO3 / geometric quadrotor control]`
- `[TODO: wind-disturbance suspended-payload UAV transport]`
- `[TODO: stress testing for autonomous systems]`

Use these to support broad problem framing and evaluation motivation. Keep the
paper's specific numerical results supported by internal tables and figures.

### Related Work 2.1

Insert citation slots for:

- `[TODO: AutoTrans]`
- `[TODO: suspended-payload UAV planning]`
- `[TODO: payload-aware MPC]`
- `[TODO: SO3 / geometric quadrotor control]`
- `[TODO: wind-disturbance suspended-payload UAV transport]`

This subsection should establish the suspended-payload transport and control
background.

### Related Work 2.2

Insert citation slots for:

- `[TODO: reference governor]`
- `[TODO: explicit reference governor]`
- `[TODO: action governor]`
- `[TODO: command filtering for robotics]`
- `[TODO: runtime safety filter]`
- `[TODO: safety filters for learned control]`

This subsection should position the governor concept while explicitly stating
that the present method is empirical and not certified.

### Related Work 2.3

Insert citation slots for:

- `[TODO: learning-enhanced UAV control]`
- `[TODO: learned risk prediction]`
- `[TODO: learned disturbance or risk prediction]`
- `[TODO: disturbance-aware learning for UAVs]`
- `[TODO: hybrid learning + model-based control]`
- `[TODO: data-driven robustness in aerial robotics]`

This subsection should explain the learning-enhanced robustness context without
claiming learned-method uniform domination.

### Related Work 2.4

Insert citation slots for:

- `[TODO: robotics benchmarking]`
- `[TODO: stress testing for autonomous systems]`
- `[TODO: repeated-run robotics evaluation]`
- `[TODO: failure analysis / taxonomy]`
- `[TODO: failure log analysis]`

This subsection should motivate protocol-split evaluation and diagnostic
failure analysis.

### Method

Insert citation slots for:

- `[TODO: AutoTrans]`
- `[TODO: payload-aware MPC]`
- `[TODO: SO3 / geometric quadrotor control]`
- `[TODO: reference governor]`
- `[TODO: learned risk prediction]`

Use these slots to distinguish established stack components and conceptual
precedent from the paper's internal implementation.

### Experimental Setup

Insert citation slots for:

- `[TODO: AutoTrans]`
- `[TODO: wind-disturbance suspended-payload UAV transport]`
- `[TODO: robotics benchmarking]`
- `[TODO: stress testing for autonomous systems]`
- `[TODO: repeated-run robotics evaluation]`

Use internal protocol documents and generated assets for exact counts, strict
metrics, and method-specific results.

### Discussion

Insert citation slots for:

- `[TODO: runtime safety filter]`
- `[TODO: safety filters for learned control]`
- `[TODO: robotics benchmarking]`
- `[TODO: failure analysis / taxonomy]`
- `[TODO: failure log analysis]`
- `[TODO: learning-enhanced UAV control]`

Use these to support cautious comparison and future work, not to strengthen
claims beyond the current evidence.

## Citation Risk Audit

| high-risk claim if citation is missing | risk | safer wording if citation remains missing |
| --- | --- | --- |
| AutoTrans-like stack claim | The paper may appear to rely on an uncited prior stack. | "We evaluate on an AutoTrans-like stack implemented in this repository; exact external citation pending." |
| Reference governor conceptual grounding | The method may be over-positioned as a formal governor. | "The interface is conceptually related to runtime command adaptation; unlike certified governors, it is empirical." |
| Failure taxonomy contribution | Failure labels may sound like proven root causes. | "We use diagnostic failure groups to organize invalid runs; they do not establish exact physical root cause." |
| Benchmarking / stress protocol legitimacy | Protocol split may look ad hoc. | "In our evaluation, the two protocols expose different rankings; broader benchmarking precedent remains a citation TODO." |
| Learning-enhanced robustness positioning | Learning claim may sound too broad. | "`risk_adapter_v1` is the most balanced learned / risk-conditioned method among currently evaluated variants under the tested protocols." |

## Internal-vs-External Evidence Boundary

Internal experimental evidence supports the Stage 4 result counts, protocol
split rankings, balanced robustness table, protocol regret, Pareto-frontier
status, invalid-only failure groups, and representative trace observations.

The protocol split is internally supported by the fact that the single-goal and
goal-reissue stress protocols produce different method rankings. However, the
broader framing that protocol-split evaluation is a benchmarking or
stress-testing best practice needs external citations before submission.

Failure groups are internally generated diagnostics. They support
failure-aware interpretation of this experiment set, but the broader idea that
failure taxonomy or log analysis is a robust system-diagnosis method needs
external citations.

The method implementation is internal. The specific `speed_scale` /
`acceleration_scale` interface, `risk_adapter_v1` settings, and Stage 4
results are internal evidence. The broader governor concept and comparison to
reference governors, runtime safety filters, and learning-enhanced control
need external citations.

## Next Action After AM

- Stage 4-AM2: collect verified citations manually or via deep research. This
  is now recorded in
  `experiments/protocols/stage4am2_verified_citation_collection_result.md`
  using only the user-provided verified metadata.
- Stage 4-AM3: draft BibTeX entries and citation insertion only after the AM2
  remaining metadata gaps are verified.
- Stage 4-AL: final figure generation plan can proceed in parallel after the
  citation slots are stable.
- Stage 4-AL2: final figure package generation can proceed in parallel with
  citation collection, but figure captions and claims should be audited against
  verified citations before final manuscript assembly.
- Do not insert unverified BibTeX.
- Do not replace TODO placeholders with guessed references.
- Do not create `risk_adapter_v22` yet.
