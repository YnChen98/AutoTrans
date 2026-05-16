# Stage 4-X0 Final Evaluation Specification

## Purpose

Stage 4-X0 freezes the final evaluation plan for the protocol-split paper
before any additional Stage 4 experiments or policy variants are run.

The goal is to complete the missing method-by-protocol cells, update the
protocol-split paper assets, and then decide whether `risk_adapter_v21` should
be frozen as the final method.

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
| `original` | `18/30` |
| `fixed_s085` | `18/30` |
| `windlevel_s085` | `16/30` |
| `risk_adapter_v1` | `23/30` |
| `fixed_s080` | `24/30` |

## Missing Methods

Single-goal mission protocol currently lacks:

- `original`
- `fixed_s085`
- `windlevel_s085`
- `risk_adapter_v1`

Goal-reissue stress protocol currently lacks:

- `risk_adapter_v21`

## Must-Run Completion Matrix

Complete these cells before making a final method claim.

| Protocol | `goal_repeat` | Methods to add |
| --- | --- | --- |
| single-goal mission protocol | `1` | `original`, `fixed_s085`, `windlevel_s085`, `risk_adapter_v1` |
| goal-reissue stress protocol | `10` | `risk_adapter_v21` |

Use strong-wind Trial 4, Trial 5, and Trial 6 with repeat1 through repeat10 for
each missing method so the final tables stay aligned with the current 30-run
per-method protocol split.

## Final-Method Decision Rule

- If `risk_adapter_v21` is strongest or near strongest in both protocols,
  freeze `risk_adapter_v21` as the final method.
- If `risk_adapter_v21` is strong in the single-goal mission protocol but weak
  in the goal-reissue stress protocol, perform failure analysis before
  designing a new variant.
- Do not create `risk_adapter_v21.1`, `risk_adapter_v22`, or any other new
  variant until the completion matrix is done.

Near strongest means close enough to the top method that the result supports a
paper-facing adaptive-method choice without claiming statistical significance.
Use the final tables and failure analysis to justify that judgment.

## Claim Limits

Allowed claims after the current incomplete comparison:

- Among the currently evaluated single-goal methods, `risk_adapter_v21`
  achieved `25/30` strict-valid.
- Among the currently evaluated goal-reissue stress methods, `fixed_s080`
  achieved `24/30` strict-valid.
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

## Next Experiment Order

Run the final evaluation completion in this order:

1. Evaluate `risk_adapter_v21` under the goal-reissue stress protocol
   (`goal_repeat=10`).
2. Evaluate the missing single-goal baselines: `original`, `fixed_s085`,
   `windlevel_s085`, and `risk_adapter_v1` under `goal_repeat=1`.
3. Update the protocol-split paper assets.
4. Decide the final method using the final-method decision rule.

Do not tune thresholds or add new variants between steps 1 and 2.
