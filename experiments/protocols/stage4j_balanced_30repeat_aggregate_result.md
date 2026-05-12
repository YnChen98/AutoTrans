# Stage 4-J Balanced 30-Repeat Aggregate Result

## Executive Summary

Stage 4 balanced 30-repeat comparison is complete for `original`,
`fixed_s085`, `windlevel_s085`, and `risk_adapter_v1` on strong-wind Trial 4,
Trial 5, and Trial 6.

Using strict-valid / `label_strict_invalid` as the paper-facing metric,
`risk_adapter_v1` achieved `23/30` strict-valid runs and is the best aggregate
method. `original` and `fixed_s085` tied at `18/30`, and `windlevel_s085`
achieved `16/30`.

This is simulation-only benchmark evidence. Do not claim statistical
significance, a safety guarantee, or final online robustness from this
30-repeat comparison.

## Method-by-Trial Table

| Method | Trial 4 | Trial 5 | Trial 6 | Aggregate |
| --- | ---: | ---: | ---: | ---: |
| `original` | `8/10` | `7/10` | `3/10` | `18/30` (`60.0%`) |
| `fixed_s085` | `9/10` | `5/10` | `4/10` | `18/30` (`60.0%`) |
| `windlevel_s085` | `4/10` | `6/10` | `6/10` | `16/30` (`53.3%`) |
| `risk_adapter_v1` | `7/10` | `9/10` | `7/10` | `23/30` (`76.7%`) |

## Aggregate Ranking

| Rank | Method | Strict-valid aggregate |
| ---: | --- | ---: |
| 1 | `risk_adapter_v1` | `23/30` (`76.7%`) |
| 2 | `original` | `18/30` (`60.0%`) |
| 2 | `fixed_s085` | `18/30` (`60.0%`) |
| 4 | `windlevel_s085` | `16/30` (`53.3%`) |

## Per-Target Interpretation

Trial 4 remains the target where `fixed_s085` is strongest: `fixed_s085`
achieved `9/10`, while `risk_adapter_v1` achieved `7/10`. Therefore
`risk_adapter_v1` does not dominate every individual target.

Trial 5 is strongest for `risk_adapter_v1`, which achieved `9/10`.

Trial 6 is also strongest for `risk_adapter_v1`, which achieved `7/10`.
However, `windlevel_s085` is close at `6/10`, and Trial 6 remains difficult
for all methods.

## Failure-Mode Caveat

Failure modes are mixed. Some failures are `command_saturation_before_nan`,
some are `state_divergence_before_command_nan`, and some are
`strict_safety_no_nan` or `target_error_only`.

Manual path/collision annotations should be used when visual evidence exists.
NaN/divergence failures should be counted as invalid, but they should not be
automatically attributed to `risk_adapter_v1`, command adaptation, or any
single method without supporting evidence.

Transient `command_saturation_without_divergence` is not a failure by itself.
`swing_angle_deg >= 30` is warning-only; `strict_safety_no_nan` is reserved for
stronger conditions such as `swing_angle_deg >= 60`, speed `>= 4 m/s`, position
jump, NaN/nonfinite state or command evidence, or target failure.

Supporting documents:

- `experiments/protocols/stage4j_trial4_10repeat_fair_comparison.md`
- `experiments/protocols/stage4j_trial5_10repeat_fair_comparison.md`
- `experiments/protocols/stage4j_trial6_10repeat_fair_comparison.md`
- `experiments/protocols/stage4_log_divergence_audit_result.md`
- `experiments/protocols/stage4o_path_feasibility_annotation_protocol.md`
- `experiments/protocols/stage4n_command_nan_guard_smoke_result.md`

## Paper-Facing Claim

A cautious paper-facing claim is:

The learned risk-conditioned command adaptation improves aggregate
strict-valid rate in the balanced strong-wind Trial 4/5/6 evaluation. The
result supports `risk_adapter_v1` as the current strongest candidate.

Claims remain simulation-only and limited to this benchmark.

## What Not To Claim

- Do not claim statistical significance.
- Do not claim a safety guarantee.
- Do not claim final online robustness.
- Do not claim `risk_adapter_v1` beats every baseline on every target.
- Do not claim all NaN failures are command-adaptation failures.
- Do not use diagnostic smokes as main evaluation results.

## Next Recommended Work

Freeze the current Stage 4-J balanced comparison.

Generate a paper-ready table or figure from
`experiments/protocols/stage4h_adapter_limited_eval_manifest.json`.

Consider a failure-mode distribution table that joins strict-valid metrics,
divergence `failure_mode_guess`, and manual path/collision annotations.

Only after this documentation and table/figure generation should
`risk_adapter_v2` design or deeper path-feasibility diagnostics be considered.
