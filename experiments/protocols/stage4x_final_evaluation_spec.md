# Stage 4-X0 Final Evaluation Specification

## Purpose

Stage 4-X0 freezes the final evaluation plan for the protocol-split paper
before any additional Stage 4 experiments or policy variants are run.

The goal is to complete the missing method-by-protocol cells, update the
protocol-split paper assets, and then decide whether `risk_adapter_v21` should
be positioned as a nominal-goal method with a stress limitation or replaced by
a new phase-aware final method.

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
| `fixed_s080` | `21/30` |
| `risk_adapter_v2` | `21/30` |
| `risk_adapter_v21` | `25/30` |

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

## Missing Methods

Single-goal mission protocol currently lacks:

- `original`
- `fixed_s085`
- `windlevel_s085`
- `risk_adapter_v1`

Goal-reissue stress protocol no longer lacks `risk_adapter_v21`; Stage 4-X1
completed that cell with a corrected `20/30` result.

## Must-Run Completion Matrix

Complete these remaining cells before making a final method claim.

| Protocol | `goal_repeat` | Methods to add |
| --- | --- | --- |
| single-goal mission protocol | `1` | `original`, `fixed_s085`, `windlevel_s085`, `risk_adapter_v1` |

Use strong-wind Trial 4, Trial 5, and Trial 6 with repeat1 through repeat10 for
each missing method so the final tables stay aligned with the current 30-run
per-method protocol split.

Completed matrix cells:

| Protocol | `goal_repeat` | Method | Corrected strict-valid count |
| --- | --- | --- | ---: |
| goal-reissue stress protocol | `10` | `risk_adapter_v21` | `20/30` |

## Final-Method Decision Rule

- If `risk_adapter_v21` is strongest or near strongest in both protocols,
  freeze `risk_adapter_v21` as the final method.
- If `risk_adapter_v21` is strong in the single-goal mission protocol but weak
  in the goal-reissue stress protocol, perform failure analysis before
  designing a new variant.
- Do not create `risk_adapter_v21.1`, `risk_adapter_v22`, or any other new
  variant until the completion matrix is done.

Stage 4-X1 now matches the second branch: `risk_adapter_v21` is strong in the
currently evaluated single-goal comparison but weaker under goal-reissue stress
than `fixed_s080` (`24/30`) and `risk_adapter_v1` (`23/30`). Do not freeze
`risk_adapter_v21` as a cross-protocol final method.

Near strongest means close enough to the top method that the result supports a
paper-facing adaptive-method choice without claiming statistical significance.
Use the final tables and failure analysis to justify that judgment.

## Claim Limits

Allowed claims after the current incomplete comparison:

- Among the currently evaluated single-goal methods, `risk_adapter_v21`
  achieved `25/30` strict-valid.
- Among the currently evaluated goal-reissue stress methods, `fixed_s080`
  achieved `24/30` strict-valid.
- Under the corrected Stage 4-X1 goal-reissue stress evaluation,
  `risk_adapter_v21` achieved `20/30` strict-valid.
- The two protocols test different system properties.

Avoid:

- statistical significance
- safety guarantee
- mixed-protocol aggregate claims
- claiming `risk_adapter_v21` beats all baselines under the single-goal mission
  protocol until the missing single-goal baselines are evaluated
- claiming `fixed_s080` or `risk_adapter_v21` is the overall best method across
  protocols before the completion matrix is done
- creating or reporting a new policy variant before the completion matrix is
  done
- claiming `risk_adapter_v21` is best under goal-reissue stress
- claiming all goal-reissue stress failures are post-arrival failures

## Next Experiment Order

Run the final evaluation completion in this order:

1. Completed in Stage 4-X1: evaluate `risk_adapter_v21` under the
   goal-reissue stress protocol (`goal_repeat=10`).
2. Next: evaluate the missing single-goal baselines: `original`, `fixed_s085`,
   `windlevel_s085`, and `risk_adapter_v1` under `goal_repeat=1`.
3. Update the protocol-split paper assets.
4. Decide the final method using the final-method decision rule.

Do not tune thresholds or add new variants before the missing single-goal
baselines are complete.
