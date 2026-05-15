# Stage 4-R Fixed S080 Frontier Result

## Executive Summary

The Stage 4-R tuned fixed-scale frontier screening for `fixed_s080` is
complete on the balanced strong-wind Trial 4/5/6 benchmark.

Using strict-valid / `label_strict_invalid` as the paper-facing metric,
`fixed_s080` achieved `24/30` strict-valid runs (`80.0%`). This slightly
exceeds the current `risk_adapter_v1` balanced result of `23/30` (`76.7%`).

Protocol caveat: this `fixed_s080` result was obtained under the current
`goal_repeat=10` repeated-goal protocol, where the same
`/move_base_simple/goal` may be received repeatedly after the UAV/payload has
already reached or nearly reached the target. The result remains the current
tuned fixed-scale frontier for that protocol, but a single-goal mission
comparison is reported separately in Stage 4-U2.

Stage 4-T2 later confirmed that `goal_repeat=10` should be interpreted as a
repeated-goal / post-arrival replan stress protocol. The `fixed_s080` `24/30`
frontier remains valid for that protocol, but it should not be reported as
single-goal mission performance.

Stage 4-U single-goal screening later found `fixed_s080` at `6/9` under
`goal_repeat=1`, while `risk_adapter_v2` reached `9/9`. Therefore
`fixed_s080` remains the tuned static frontier for the repeated-goal protocol,
but its single-goal mission performance should be evaluated and reported
separately.

Stage 4-U2 completed that single-goal 10-repeat expansion. Under
`goal_repeat=1`, `fixed_s080` achieved `21/30`, while `risk_adapter_v2` also
achieved `21/30`. Therefore `fixed_s080` should be described as `24/30` under
the repeated-goal stress protocol and `21/30` under the single-goal mission
protocol.

This changes the Stage 4 interpretation. `risk_adapter_v1` improves over the
initial baselines `original`, `fixed_s085`, and `windlevel_s085`, but it should
no longer be described as the best overall method once the tuned `fixed_s080`
static frontier is included.

This is not a failure of the learned adapter direction. It reveals a strong
static operating point and motivates `risk_adapter_v2`: a calibrated,
failure-mode-aware learned execution governor that can match or exceed
`fixed_s080` while preserving adaptivity.

## Method Comparison Table

| Method | Strict-valid aggregate |
| --- | ---: |
| `original` | `18/30` (`60.0%`) |
| `fixed_s085` | `18/30` (`60.0%`) |
| `windlevel_s085` | `16/30` (`53.3%`) |
| `risk_adapter_v1` | `23/30` (`76.7%`) |
| `fixed_s080` | `24/30` (`80.0%`) |

## Per-Trial Fixed S080 Table

| Trial | Strict-valid count |
| --- | ---: |
| Trial 4 | `8/10` |
| Trial 5 | `9/10` |
| Trial 6 | `7/10` |
| Aggregate | `24/30` (`80.0%`) |

## Repeat-Level Notes

Invalid `fixed_s080` repeats:

- Trial 4 repeat5: invalid, NaN, `first_nan=16.449967`,
  `command_saturation_before_nan`.
- Trial 4 repeat10: invalid, NaN, `first_nan=22.949909`,
  `state_divergence_before_command_nan`.
- Trial 5 repeat10: invalid target/final-position failure, no NaN,
  `final_xy=0.780889`.
- Trial 6 repeat3: invalid, NaN, `first_nan=19.600075`,
  `command_saturation_before_nan`.
- Trial 6 repeat6: invalid, NaN, `first_nan=98.952192`,
  `command_saturation_before_nan`.
- Trial 6 repeat7: invalid, NaN, `first_nan=8.300523`,
  `command_saturation_before_nan`.

Per-trial summaries:

- Trial 4: repeats 1, 2, 3, 4, 6, 7, 8, and 9 were strict-valid; repeats 5
  and 10 were invalid.
- Trial 5: repeats 1 through 9 were strict-valid; repeat 10 was invalid.
- Trial 6: repeats 1, 2, 4, 5, 8, 9, and 10 were strict-valid; repeats 3, 6,
  and 7 were invalid.

## Failure-Mode Interpretation

Aggregate diagnostic-label counts for `fixed_s080`:

| Diagnostic label | Count |
| --- | ---: |
| `command_saturation_before_nan` | `4` |
| `command_saturation_without_divergence` | `23` |
| `no_divergence_detected` | `2` |
| `state_divergence_before_command_nan` | `1` |

Most `fixed_s080` runs are either `command_saturation_without_divergence` or
valid/no-divergence cases. Transient command saturation remains not a failure
by itself.

However, `fixed_s080` still has `command_saturation_before_nan` failures and
one `state_divergence_before_command_nan` failure. It is a strong tuned static
baseline, not a safety-guaranteed controller or planner setting.

## Impact On Paper Claim

The previous claim that "`risk_adapter_v1` is aggregate best" should be
revised after including Stage 4-R.

New cautious claim:

`risk_adapter_v1` improves over `original`, `fixed_s085`, and
`windlevel_s085`, but a tuned `fixed_s080` static frontier slightly exceeds it
in this benchmark.

This motivates a calibrated risk-conditioned governor `risk_adapter_v2`.

The `fixed_s080` `24/30` result should be reported as a repeated-goal protocol
result after the Stage 4-T1/T2 goal reception, arrival, and post-arrival
trajectory-update diagnostics. It should not be used alone to claim
single-goal mission robustness.

Stage 4-T2 found that `fixed_s080` Trial 4 was `1/3` under `goal_repeat=1` and
`2/3` under `goal_repeat=10`. This diagnostic does not weaken `fixed_s080` as
the tuned repeated-goal frontier, but it shows that single-goal mission
evaluation must be run and reported separately.

Stage 4-U extended that single-goal check to Trial 4/5/6 repeat1-3:
`fixed_s080` was `6/9` and `risk_adapter_v2` was `9/9`. This is screening
evidence only; it should be expanded before any final ranking claim.

Stage 4-U2 completed the 10-repeat single-goal expansion: `fixed_s080` was
`21/30` and `risk_adapter_v2` was also `21/30` under `goal_repeat=1`. This
means `fixed_s080` remains a strong tuned static frontier, but its repeated-goal
`24/30` result and single-goal `21/30` result must be reported under separate
protocol labels.

## Research Decision

Freeze `fixed_s080` as the current tuned fixed-scale frontier.

Do not run more fixed scales until `fixed_s080` is recorded and paper assets
are updated.

The next algorithmic step should be `risk_adapter_v2`, using `fixed_s080` as a
static frontier reference.

The next reporting step should update Stage 4-P paper assets to include
`fixed_s080`.

The Stage 4-S `risk_adapter_v2` design protocol is documented in
`experiments/protocols/stage4s_risk_adapter_v2_design.md`.

## What Not To Claim

- Do not claim `risk_adapter_v1` is best overall after including `fixed_s080`.
- Do not claim `fixed_s080` has a safety guarantee.
- Do not claim statistical significance.
- Do not hide that `fixed_s080` exceeds `risk_adapter_v1` by `1/30`.
- Do not treat diagnostic smokes as main results.
