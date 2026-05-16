# Stage 4-X1 Risk Adapter V2.1 Goal-Reissue Stress Result

## Executive Summary

Stage 4-X1 completed the corrected `risk_adapter_v21` evaluation under the
goal-reissue / post-arrival replan stress protocol.

A duplicate CSV issue was found in Trial 4 repeat2-5. Trial 4 repeat3-5 were
rerun, and the corrected set was recorded only after confirming `No duplicate
csv_path detected`.

Under strong wind with `goal_repeat=10`, `risk_adapter_v21` achieved `20/30`
strict-valid runs:

- Trial 4: `4/10`
- Trial 5: `9/10`
- Trial 6: `7/10`
- Aggregate: `20/30`

This is below `fixed_s080` (`24/30`) and `risk_adapter_v1` (`23/30`) under the
same goal-reissue stress protocol. Therefore, `risk_adapter_v21` should not be
treated as a cross-protocol final winner.

## Protocol

- protocol: goal-reissue / post-arrival replan stress protocol
- `goal_repeat=10`
- wind: `strong`
- trials: Trial 4, Trial 5, Trial 6
- repeats: repeat1 through repeat10
- method: `risk_adapter_v21`
- paper-facing metric: strict-valid / `label_strict_invalid`

Strict-valid requires:

- `valid_run_suggested=true`
- `has_nan_state=false`
- `max_swing_angle_deg < 60`
- `max_uav_speed < 4`
- `max_payload_speed < 4`
- `final_uav_xy_error <= 0.5`

## Method Comparison

Goal-reissue stress protocol aggregate comparison:

| Method | Strict-valid count | Repeat count |
| --- | ---: | ---: |
| `fixed_s080` | `24` | `30` |
| `risk_adapter_v1` | `23` | `30` |
| `risk_adapter_v21` | `20` | `30` |
| `original` | `18` | `30` |
| `fixed_s085` | `18` | `30` |
| `windlevel_s085` | `16` | `30` |

`fixed_s080` remains the strongest evaluated method under the goal-reissue
stress protocol. `risk_adapter_v1` also remains stronger than
`risk_adapter_v21` under this protocol.

## Per-Trial Result

| Trial | Strict-valid count | Repeat count |
| --- | ---: | ---: |
| Trial 4 | `4` | `10` |
| Trial 5 | `9` | `10` |
| Trial 6 | `7` | `10` |
| Aggregate | `20` | `30` |

Trial 4 is the main stress weakness for `risk_adapter_v21`.

## Per-Trial Diagnostic Labels

Trial 4:

| Diagnostic label | Count |
| --- | ---: |
| `command_nan_before_state_divergence` | `2` |
| `command_nan_coincident_with_state_divergence` | `2` |
| `command_saturation_without_divergence` | `2` |
| `no_divergence_detected` | `1` |
| `state_divergence_before_command_nan` | `2` |
| `swing_warning_no_nan` | `1` |

Trial 5:

| Diagnostic label | Count |
| --- | ---: |
| `command_saturation_before_nan` | `1` |
| `command_saturation_without_divergence` | `6` |
| `no_divergence_detected` | `2` |
| `swing_warning_no_nan` | `1` |

Trial 6:

| Diagnostic label | Count |
| --- | ---: |
| `command_saturation_before_nan` | `2` |
| `command_saturation_without_divergence` | `5` |
| `no_divergence_detected` | `1` |
| `reference_jump_before_command_nan` | `1` |
| `swing_warning_no_nan` | `1` |

## Aggregate Diagnostic Label Summary

| Diagnostic label | Count |
| --- | ---: |
| `command_nan_before_state_divergence` | `2` |
| `command_nan_coincident_with_state_divergence` | `2` |
| `command_saturation_before_nan` | `3` |
| `command_saturation_without_divergence` | `13` |
| `no_divergence_detected` | `4` |
| `reference_jump_before_command_nan` | `1` |
| `state_divergence_before_command_nan` | `2` |
| `swing_warning_no_nan` | `3` |

Additional metrics:

- `aggregate_mean_of_mean_scale=0.796423`
- `aggregate_min_mean_scale=0.783255`
- `aggregate_max_mean_scale=0.834459`
- `post_arrival_failure_count=2`
- `post_arrival_goal_received_count_total=158`

## Interpretation

`risk_adapter_v21` remains strong under the single-goal mission protocol, where
it achieved `25/30` among the currently evaluated methods. Under goal-reissue
stress, however, it achieved `20/30`, below `fixed_s080` and
`risk_adapter_v1`.

Trial 4 is the main stress weakness. The stress failures are not exclusively
post-arrival failures; many Trial 4 stress failures occur before arrival.
Goal-reissue stress therefore remains a distinct unresolved robustness regime.

## Research Decision

- Do not freeze `risk_adapter_v21` as a cross-protocol final method.
- Do not create `risk_adapter_v22` yet.
- Next, complete the missing single-goal baselines so the single-goal mission
  protocol has full baseline coverage.
- After the full single-goal table is complete, decide whether the paper should
  position `risk_adapter_v21` as a nominal-goal method with a stress limitation,
  or whether a new phase-aware final method is needed.

## What Not To Claim

- Do not claim `risk_adapter_v21` is best under goal-reissue stress.
- Do not claim `risk_adapter_v21` is a cross-protocol winner.
- Do not claim all stress failures are post-arrival.
- Do not claim statistical significance.
- Do not claim a safety guarantee.
- Do not mix `goal_repeat=1` and `goal_repeat=10` aggregates.
