# Stage 4-V3 Risk Adapter V2.1 Screening Result

## Executive Summary

Stage 4-V3 screened `risk_adapter_v21` under the single-goal mission protocol.

`risk_adapter_v21` achieved `9/9` strict-valid runs across strong-wind Trial 4,
Trial 5, and Trial 6 repeat1-3. This passes the Stage 4-V expansion threshold
and motivates a 10-repeat expansion under `goal_repeat=1`.

The screening preserved the strong Trial 4 behavior of `risk_adapter_v2` and
avoided the long-duration `0.65` behavior that motivated Stage 4-V. This is
not final proof of superiority. It is a 9-run screening result.

Stage 4-V4 supersedes this 9-run screening with a 10-repeat single-goal
expansion: `risk_adapter_v21` achieved `25/30` strict-valid under
`goal_repeat=1`, with Trial 4 `10/10`, Trial 5 `9/10`, and Trial 6 `6/10`.
Use `experiments/protocols/stage4v_risk_adapter_v21_10repeat_result.md` as the
current `risk_adapter_v21` single-goal result.

## Protocol

- protocol: single-goal mission protocol
- `goal_repeat=1`
- wind: `strong`
- trials: Trial 4, Trial 5, Trial 6
- repeats: repeat1 through repeat3
- method: `risk_adapter_v21`
- main metric: strict-valid / `label_strict_invalid`

## Result Table

| Method | Trial 4 | Trial 5 | Trial 6 | Aggregate |
| --- | ---: | ---: | ---: | ---: |
| `risk_adapter_v21` | `3/3` | `3/3` | `3/3` | `9/9` |

## Diagnostic Label Summary

Aggregate diagnostic-label counts:

| Diagnostic label | Count |
| --- | ---: |
| `command_saturation_without_divergence` | `6` |
| `no_divergence_detected` | `2` |
| `swing_warning_no_nan` | `1` |

`command_saturation_without_divergence` is not a failure by itself. It means
the command reached a diagnostic saturation threshold without NaN/divergence or
strict-invalid evidence in the inspector taxonomy.

Trial 6 repeat1 had `swing_warning_no_nan` with `max_swing=40.090619`, but the
run remained strict-valid. This should be tracked during expansion, not treated
as a Stage 4-V3 failure.

## Scale Behavior Analysis

Observed `risk_adapter_v21` scale behavior:

- Trial 4: mean scale around `0.843`, minimum `0.80`, maximum `0.85`
- Trial 5: mean scale around `0.711`, minimum `0.70`, maximum `0.80`
- Trial 6: mean scale around `0.711`, minimum `0.70`, maximum `0.80`

This is consistent with the Stage 4-V design goal. `risk_adapter_v21` keeps
Trial 4 behavior close to the faster `0.80` to `0.85` range while using `0.70`
for ordinary long-horizon high risk in Trial 5 and Trial 6.

The screening did not show long-duration `0.65` behavior. That directly
addresses the Stage 4-U2 concern that `risk_adapter_v2` often stayed near
`0.666` on Trial 6 and may have been over-conservative.

## Research Decision

- Expand `risk_adapter_v21` to 10 repeats under `goal_repeat=1`.
- Compare the 10-repeat result against the Stage 4-U2 single-goal results for
  `fixed_s080` and `risk_adapter_v2`.
- Do not tune `risk_adapter_v21` before the 10-repeat expansion unless the
  expansion reveals a clear failure mechanism.
- Continue reporting `goal_repeat=1` single-goal mission and `goal_repeat=10`
  repeated-goal stress results separately.
- Do not claim final superiority before the 10-repeat expansion.
- Superseded by Stage 4-V4: use the `25/30` 10-repeat result for current
  `risk_adapter_v21` single-goal comparison.

## What Not To Claim

- Do not claim statistical significance from this 9-run screening.
- Do not claim a safety guarantee.
- Do not claim final `risk_adapter_v21` dominance from this screening.
- Do not claim `fixed_s080` is weak.
- Do not mix `goal_repeat=1` and `goal_repeat=10` evidence without protocol
  labels.
