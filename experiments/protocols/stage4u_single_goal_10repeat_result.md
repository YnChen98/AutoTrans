# Stage 4-U2 Single-Goal 10-Repeat Result

## Executive Summary

Stage 4-U2 expanded the single-goal mission protocol to 10 repeats for
`fixed_s080` and `risk_adapter_v2` under strong wind.

Both methods achieved `21/30` strict-valid runs. `risk_adapter_v2` was
stronger on Trial 4, equal on Trial 5, and weaker on Trial 6. This differs
from the `goal_repeat=10` repeated-goal stress results and should be reported
as a separate single-goal mission protocol result.

The result supports `risk_adapter_v2` as a promising learned governor, but it
does not show that `risk_adapter_v2` is overall better than `fixed_s080` yet.
It also shows target-dependent trade-offs that should guide a `risk_adapter_v2.1`
design before further expansion.

Stage 4-V3 later screened `risk_adapter_v21` and achieved `9/9` strict-valid
under the same single-goal protocol across Trial 4/5/6 repeat1-3. That result
is promising, but it should be expanded to 10 repeats before revising the main
single-goal comparison recorded here.

## Protocol

- protocol: single-goal mission protocol
- `goal_repeat=1`
- wind: `strong`
- trials: Trial 4, Trial 5, Trial 6
- repeats: repeat1 through repeat10
- methods: `fixed_s080`, `risk_adapter_v2`
- main metric: strict-valid / `label_strict_invalid`
- diagnostic labels: from `experiments/scripts/inspect_stage4_log_divergence.py`
  after the corrected position/reference jump warning taxonomy

## Method-By-Trial Table

| Method | Trial 4 | Trial 5 | Trial 6 | Aggregate |
| --- | ---: | ---: | ---: | ---: |
| `fixed_s080` | `7/10` | `6/10` | `8/10` | `21/30` |
| `risk_adapter_v2` | `9/10` | `6/10` | `6/10` | `21/30` |

## Failure-Mode / Diagnostic Label Summary

Aggregate diagnostic-label counts for `fixed_s080`:

| Diagnostic label | Count |
| --- | ---: |
| `command_saturation_before_nan` | `3` |
| `command_saturation_without_divergence` | `17` |
| `no_divergence_detected` | `3` |
| `position_or_reference_jump_warning_no_nan` | `1` |
| `reference_jump_before_command_nan` | `1` |
| `state_divergence_before_command_nan` | `5` |

Aggregate diagnostic-label counts for `risk_adapter_v2`:

| Diagnostic label | Count |
| --- | ---: |
| `command_nan_before_state_divergence` | `1` |
| `command_saturation_before_nan` | `2` |
| `command_saturation_without_divergence` | `20` |
| `no_divergence_detected` | `2` |
| `reference_jump_before_command_nan` | `2` |
| `state_divergence_before_command_nan` | `1` |
| `swing_warning_no_nan` | `2` |

`command_saturation_without_divergence` is not a failure by itself. It means
the command reached a diagnostic saturation threshold without NaN/divergence or
strict-invalid evidence in the inspector taxonomy.

`position_or_reference_jump_warning_no_nan` is warning-only after the corrected
taxonomy. It should not override paper-facing strict-valid status when the run
is otherwise strict-valid by analyzer metrics.

Diagnostic labels remain heuristic timing labels, not perfect physical
root-cause proof.

## Scale Behavior Analysis

`risk_adapter_v2` used different mean command scales across targets:

- Trial 4: around `0.844`
- Trial 5: around `0.755` to `0.800`
- Trial 6: often around `0.666`

This confirms that `risk_adapter_v2` is not merely a `fixed_s080` clone. It
adapts scale by target/run context.

The Trial 6 result also suggests that long-duration use of `0.65` may be too
conservative. `fixed_s080` achieved `8/10` on Trial 6, while
`risk_adapter_v2` achieved `6/10`. A `risk_adapter_v2.1` design should reduce
long-duration `0.65` use and consider `0.70` or `0.75` for high-risk states
unless severe risk persists.

Stage 4-V records this follow-up design direction in
`experiments/protocols/stage4v_risk_adapter_v21_design.md`. The main
motivation is Trial 6 underperformance: `risk_adapter_v2` matched
`fixed_s080` in aggregate, but lost `6/10` vs `8/10` on Trial 6, where mean
scale often stayed near `0.666`.

## Relationship To Stage 4-T

Stage 4-T2 showed that `goal_repeat=10` can introduce repeated-goal /
post-arrival replan stress. Therefore:

- `goal_repeat=1` should be treated as the single-goal mission protocol.
- `goal_repeat=10` should be treated as the repeated-goal stress protocol.
- The prior `risk_adapter_v2` `5/9` screening under `goal_repeat=10` should
  not be used as single-goal mission evidence.

Previous repeated-goal results remain useful stress-test evidence, but they
must be reported separately from Stage 4-U2 single-goal results.

## Research Decision

- Do not claim `risk_adapter_v2` beats `fixed_s080` overall yet.
- Design `risk_adapter_v2.1` before further expansion.
- `risk_adapter_v2.1` should reduce long-duration use of `0.65`.
- `risk_adapter_v2.1` should use `0.70` or `0.75` for high-risk states unless
  severe risk persists.
- Keep `risk_adapter_v2` results recorded as the baseline for the Stage 4-V
  design comparison.
- Treat the Stage 4-V3 `risk_adapter_v21` `9/9` screening as a motivation for
  10-repeat expansion, not as a replacement for this Stage 4-U2 result.
- Future paper results must separate single-goal mission and repeated-goal
  stress protocols.

## What Not To Claim

- Do not claim statistical significance.
- Do not claim a safety guarantee.
- Do not claim `risk_adapter_v2` dominates `fixed_s080`.
- Do not mix `goal_repeat=1` and `goal_repeat=10` results into one table
  without protocol labels.
- Do not treat diagnostic labels as perfect root-cause proof.
