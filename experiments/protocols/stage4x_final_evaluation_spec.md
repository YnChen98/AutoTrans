# Stage 4-X0 Final Evaluation Specification

## Purpose

Stage 4-X0 freezes the final evaluation plan for the protocol-split paper
before any additional Stage 4 experiments or policy variants are run.

The missing method-by-protocol cells are now complete through Stage 4-X2. The
next step is to update the protocol-split paper assets, then decide whether the
paper should emphasize learned-governor analysis with a strong heuristic
frontier or motivate a new phase-aware final method after failure analysis.

## Protocol Names

Use these paper-facing protocol names:

- single-goal mission protocol: `goal_repeat=1`
- goal-reissue stress protocol: `goal_repeat=10`

Older notes may call `goal_repeat=10` the repeated-goal or post-arrival replan
stress protocol. For the final paper assets, use goal-reissue stress protocol
and keep `goal_repeat=10` explicit.

## Strict-Valid Metric

Paper-facing success is strict-valid. A run is strict-valid only when all of
the following are true:

- `valid_run_suggested=true`
- `has_nan_state=false`
- `max_swing_angle_deg < 60`
- `max_uav_speed < 4`
- `max_payload_speed < 4`
- `final_uav_xy_error <= 0.5`

Do not use raw `valid_run_suggested` alone as the paper-facing success metric.

## Current Included Methods

Single-goal mission protocol, `goal_repeat=1`:

| Method | Strict-valid count |
| --- | ---: |
| `windlevel_s085` | `26/30` |
| `risk_adapter_v1` | `25/30` |
| `risk_adapter_v21` | `25/30` |
| `fixed_s085` | `22/30` |
| `original` | `21/30` |
| `fixed_s080` | `21/30` |
| `risk_adapter_v2` | `21/30` |

Goal-reissue stress protocol, `goal_repeat=10`:

| Method | Strict-valid count |
| --- | ---: |
| `fixed_s080` | `24/30` |
| `risk_adapter_v1` | `23/30` |
| `risk_adapter_v21` | `20/30` |
| `original` | `18/30` |
| `fixed_s085` | `18/30` |
| `windlevel_s085` | `16/30` |

The `risk_adapter_v21` goal-reissue stress result was corrected in Stage 4-X1
after a duplicate CSV issue was found in Trial 4 repeat2-5. Trial 4 repeat3-5
were rerun, and the corrected result was recorded only after confirming `No
duplicate csv_path detected`.

The Stage 4-X2 missing single-goal baseline completion is recorded in
`experiments/protocols/stage4x_single_goal_baseline_completion_result.md`.
It completes `original`, `fixed_s085`, `windlevel_s085`, and
`risk_adapter_v1` under `goal_repeat=1`. `windlevel_s085` is now the highest
completed single-goal aggregate at `26/30`; `risk_adapter_v1` and
`risk_adapter_v21` are tied at `25/30`.

## Missing Methods

No protocol-split cells in the Stage 4-X0 completion matrix remain missing.
Stage 4-X1 completed `risk_adapter_v21` under goal-reissue stress, and Stage
4-X2 completed `original`, `fixed_s085`, `windlevel_s085`, and
`risk_adapter_v1` under the single-goal mission protocol.

## Completion Matrix Status

These cells complete the Stage 4-X0 matrix.

| Protocol | `goal_repeat` | Method | Corrected strict-valid count |
| --- | --- | --- | ---: |
| goal-reissue stress protocol | `10` | `risk_adapter_v21` | `20/30` |
| single-goal mission protocol | `1` | `original` | `21/30` |
| single-goal mission protocol | `1` | `fixed_s085` | `22/30` |
| single-goal mission protocol | `1` | `windlevel_s085` | `26/30` |
| single-goal mission protocol | `1` | `risk_adapter_v1` | `25/30` |

Use strong-wind Trial 4, Trial 5, and Trial 6 with repeat1 through repeat10 for
each method so the final tables stay aligned with the current 30-run
per-method protocol split.

## Final-Method Decision Rule

- If `risk_adapter_v21` is strongest or near strongest in both protocols,
  freeze `risk_adapter_v21` as the final method.
- If `risk_adapter_v21` is strong in the single-goal mission protocol but weak
  in the goal-reissue stress protocol, perform failure analysis before
  designing a new variant.
- Do not create `risk_adapter_v21.1`, `risk_adapter_v22`, or any other new
  variant before protocol-split paper assets and failure analysis are updated.

Stage 4-X2 changes the single-goal branch: `risk_adapter_v21` is competitive
but no longer the highest completed single-goal method because
`windlevel_s085` achieved `26/30`. Stage 4-X1 also shows `risk_adapter_v21` is
weaker under goal-reissue stress than `fixed_s080` (`24/30`) and
`risk_adapter_v1` (`23/30`). Do not freeze `risk_adapter_v21` as a
cross-protocol final method.

Near strongest means close enough to the top method that the result supports a
paper-facing adaptive-method choice without claiming statistical significance.
Use the final tables and failure analysis to justify that judgment.

## Claim Limits

Allowed claims after the completed protocol-split comparison:

- Under the completed single-goal mission protocol, `windlevel_s085` achieved
  the highest aggregate at `26/30` strict-valid.
- Under the completed single-goal mission protocol, `risk_adapter_v1` and
  `risk_adapter_v21` each achieved `25/30` strict-valid.
- Among the currently evaluated goal-reissue stress methods, `fixed_s080`
  achieved `24/30` strict-valid.
- Under the corrected Stage 4-X1 goal-reissue stress evaluation,
  `risk_adapter_v21` achieved `20/30` strict-valid.
- The two protocols test different system properties.
- `risk_adapter_v21` remains competitive and improves over `original`,
  `fixed_s080`, `fixed_s085`, and `risk_adapter_v2` in the completed
  single-goal aggregate.

Avoid:

- statistical significance
- safety guarantee
- mixed-protocol aggregate claims
- claiming `risk_adapter_v21` is the best single-goal method
- claiming `risk_adapter_v21` beats all single-goal baselines
- claiming a learned governor uniformly dominates simple heuristic baselines
- claiming `fixed_s080`, `windlevel_s085`, or `risk_adapter_v21` is the overall
  best method across protocols
- creating or reporting a new policy variant before the protocol-split paper
  assets and failure analysis are updated
- claiming `risk_adapter_v21` is best under goal-reissue stress
- claiming all goal-reissue stress failures are post-arrival failures

## Next Experiment Order

The Stage 4-X0 completion order is now:

1. Completed in Stage 4-X1: evaluate `risk_adapter_v21` under the
   goal-reissue stress protocol (`goal_repeat=10`).
2. Completed in Stage 4-X2: evaluate the missing single-goal baselines:
   `original`, `fixed_s085`,
   `windlevel_s085`, and `risk_adapter_v1` under `goal_repeat=1`.
3. Next: update the protocol-split paper assets with the completed
   single-goal table and corrected goal-reissue stress table.
4. Decide the final method using the final-method decision rule.

Do not tune thresholds or add new variants before the protocol-split paper
assets and failure analysis are updated.
