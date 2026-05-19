# Stage 4-AS Submission Strategy Plan

## Executive Summary

Stage 4-AS records the submission strategy after deep-research venue planning.
The immediate Paper 1 target should be RA-L. Paper 2 should be a later
mechanism-driven extension track targeting T-RO, IROS 2027, the next ICRA
cycle, or TCST depending on the final extension direction.

Do not downgrade the venue target for Paper 1. The current work is already
best framed as a focused RA-L submission centered on a stack-compatible
risk-conditioned execution governor, protocol-split evaluation, balanced
robustness, and failure diagnosis.

Prefer algorithm, evaluation, and theory-style strengthening over complex real
hardware as a requirement. Hardware-in-the-loop or minimal hardware can support
a later extension, but Paper 1 should not be blocked on full real-hardware
validation.

## Paper 1 RA-L Track

Paper 1 immediate target:

- Venue: RA-L.
- Protagonist: `risk_adapter_v1`.
- Role of `risk_adapter_v21`: strong nominal / single-goal variant or
  ablation, not the final method.
- New variant boundary: do not create `risk_adapter_v22` before Paper 1 RA-L
  submission unless explicitly overridden.

Core contribution package:

- Drop-in governor: stack-compatible execution governance through
  `speed_scale` and `acceleration_scale`, without replacing the planner,
  payload MPC, or SO3 controller.
- Protocol split: separate single-goal mission protocol (`goal_repeat=1`) from
  goal-reissue stress protocol (`goal_repeat=10`).
- Balanced robustness: use mean valid count, worst-protocol valid count, and
  protocol regret to explain why `risk_adapter_v1` is the balanced learned /
  risk-conditioned protagonist.
- Failure diagnosis: use invalid-only failure groups and representative trace
  cases to explain heterogeneous failure behavior without claiming exact root
  cause or certified safety.

Must-fix items before RA-L submission:

- Convert the manuscript to the official RA-L / IEEE template and formatting.
- Finalize citations and unresolved metadata.
- Fix Figure 6 layout and make the representative trace story readable within
  the paper page budget.
- Document the risk score source, training data, feature windows, inference
  assumptions, and calibration caveats.
- Define the strict-valid metric clearly, including `label_strict_invalid`,
  target-error conditions, speed/swing/log-health checks, and manual-invalid
  boundaries.
- Run a final claim audit for no statistical significance claim, no formal
  safety guarantee, no real-world deployment claim, and no learned uniform
  domination claim.

Optional small evidence package:

- Paired or block analysis over the repeated-run design.
- Fixed-scale frontier summary, with `fixed_s080` treated as a strong static
  operating point rather than a safety guarantee.
- Channel ablation, such as speed-only, acceleration-only, or combined
  `speed_scale` / `acceleration_scale`, if it can be added without delaying or
  destabilizing the RA-L submission.

## Paper 2 Extension Track

Paper 2 must be substantially new. It should not be a lightly enlarged version
of the RA-L paper with extra runs added to the same central method.

Candidate Paper 2 protagonist:

- A mechanism-driven final governor that extends beyond `risk_adapter_v1`.
- `risk_adapter_v1` can become a baseline, predecessor, or reference method in
  Paper 2.

Possible mechanisms:

- Phase-aware governance.
- Failure-aware governance.
- Risk-health-aware governance.
- Reference / trajectory-age-aware governance.
- Command / state-health-aware governance.

Expanded evidence package:

- `goal_repeat` curve, not only `goal_repeat=1` and `goal_repeat=10`.
- Fixed and dynamic heuristic frontier.
- Calibration and lead-time analysis.
- Speed-only, acceleration-only, no-risk, delayed-risk, and shuffled-risk
  ablations.
- Wind, payload, cable, and mission generalization.
- Optional HIL or minimal hardware evidence if it supports the mechanism
  story without becoming the central requirement.

## Venue Mapping

- RA-L: immediate first target for Paper 1.
- IROS 2027 / ICRA next cycle: 1-2 month algorithm and evaluation upgrade
  target if the work is pushed toward a stronger conference version.
- T-RO: 3-6 month major extension target requiring a mechanism-driven final
  governor and broader evaluation.
- TCST: control / supervisory-governor extension target, especially if the
  mechanism is framed through runtime governance, calibration, stability
  boundaries, or supervisory control structure.
- T-ASE: automation / reliability reframing target, especially if the paper
  emphasizes protocol reliability, failure diagnosis, and operational
  robustness under repeated missions.
- CoRL, RSS, T-Cyber, T-IV, and Autonomous Robots are not the current priority.

## Publication Ethics / Overlap Boundary

Paper 2 must cite Paper 1 if Paper 1 is submitted or published.

Paper 2 must have a new central method and substantially expanded evaluation.
It should not reuse Paper 1 as a lightly extended duplicate.

Acceptable Paper 2 overlap:

- Reuse Paper 1 as the baseline context.
- Treat `risk_adapter_v1` as the predecessor or baseline governor.
- Reuse protocol definitions if the new work expands them clearly.

Required Paper 2 novelty:

- A mechanism-driven final governor or equivalent new central method.
- Broader protocol family and generalization evidence.
- Calibration, ablation, and lead-time analysis that were not merely cosmetic
  additions to Paper 1.

## Current Next Step

Stage 4-AT now audits RA-L conversion and submission readiness:
`experiments/protocols/stage4at_ral_conversion_submission_audit.md`.

Stage 4-AT does not perform template conversion. It records the current
`paper/stage4_governor/` scaffold inventory, RA-L conversion needs, Paper 1
must-fix / should-fix items, Paper 2 overlap boundary, risk register, and the
recommended next order: Stage 4-AU risk score / strict-valid metric
documentation, then Stage 4-AV RA-L template acquisition and conversion unless
the template is already ready.

No `risk_adapter_v22` should be created before Paper 1 RA-L submission unless
explicitly overridden.

Future planning should distinguish Paper 1 evidence polishing from Paper 2
extension work. Paper 1 should prioritize RA-L readiness, claim audit, citation
finalization, template conversion, Figure 6 readability, risk-score
documentation, and strict-valid metric definition. Paper 2 should wait for a
new mechanism-driven governor and broader evidence package.
