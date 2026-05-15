# Stage 4-V Risk Adapter V2.1 Design

## Executive Summary

Stage 4-V proposes `risk_adapter_v2.1`, the next calibrated
risk-conditioned execution-governor design after Stage 4-U2.

`risk_adapter_v2.1` should improve over `risk_adapter_v2` by reducing
long-duration over-conservative scaling. The main target is to exceed
`fixed_s080` under the single-goal mission protocol while preserving the strong
Trial 4 behavior observed with `risk_adapter_v2`.

This is a design protocol only. It does not claim `risk_adapter_v2.1`
superiority before experiments, and it does not require planner, controller, or
simulator changes.

Stage 4-V2 implements the first minimal `risk_adapter_v2.1` policy as
`policy_mode=risk_adapter_v21` in
`experiments/command_adaptation/scripts/risk_conditioned_command_adapter.py`.
This implementation is risk-only plus hysteresis/dwell and remains disabled by
default.

## Motivation

Stage 4-U2 expanded the single-goal mission protocol:

- wind: `strong`
- `goal_repeat=1`
- Trial 4, Trial 5, Trial 6
- repeat1 through repeat10
- paper-facing metric: strict-valid / `label_strict_invalid`

The Stage 4-U2 result was:

| Method | Trial 4 | Trial 5 | Trial 6 | Aggregate |
| --- | ---: | ---: | ---: | ---: |
| `fixed_s080` | `7/10` | `6/10` | `8/10` | `21/30` |
| `risk_adapter_v2` | `9/10` | `6/10` | `6/10` | `21/30` |

`risk_adapter_v2` matched `fixed_s080` in aggregate. It was stronger on Trial
4, equal on Trial 5, and weaker on Trial 6.

The main suspected issue is that `risk_adapter_v2` stays near `0.65` for
difficult Trial 6 cases. The observed mean scale pattern was:

- Trial 4: around `0.844`
- Trial 5: around `0.755` to `0.800`
- Trial 6: often around `0.666`

More conservative scaling is not automatically safer. It can increase exposure
time, prolong operation near difficult states, or fail to address failure modes
that are not command-magnitude dominated.

## V2.1 Policy Direction

Proposed default parameter direction:

- `base_scale_v21=0.80`
- `low_risk_fast_scale_v21=0.85`
- `medium_scale_v21=0.80`
- `high_short_horizon_scale_v21=0.75`
- `high_long_horizon_scale_v21=0.70` or `0.75`
- `severe_scale_v21=0.65`
- `0.60` disabled by default

The core change is to reserve `0.65` for sustained or severe risk. Ordinary
high-risk states should use `0.70` or `0.75` rather than long-duration `0.65`.

The aim is not simply to slow down more. The aim is to preserve the useful
Trial 4 adaptation while reducing possible Trial 6 over-conservatism.

## Suggested V2.1 Candidate Policies

### Candidate A: `conservative-high`

- low risk: `0.85`
- medium risk: `0.80`
- high 3s risk: `0.75`
- high 5s risk: `0.70`
- severe sustained risk: `0.65`

Candidate A is the recommended first implementation. It is a middle-ground
revision: less conservative than the current long-duration `0.65` behavior,
but still below the `fixed_s080` frontier when long-horizon risk is high.

### Candidate B: `static-frontier-biased`

- low risk: `0.85`
- medium risk: `0.80`
- high 3s risk: `0.80` or `0.75`
- high 5s risk: `0.75`
- severe sustained risk: `0.65`

Candidate B is more aggressive and closer to the static frontier. It may be
useful if Candidate A remains too conservative on Trial 6, but it should not be
the first default unless screening shows Candidate A still loses too much
Trial 6 performance.

## Hysteresis / Dwell Revision

`risk_adapter_v2.1` should keep upscale dwell, but revise downscale behavior:

- Keep upscale dwell before returning to faster scales.
- Add downscale dwell for ordinary high risk.
- Allow immediate downscale only for severe risk.
- Add minimum dwell time before entering `severe_scale_v21`.
- Add maximum continuous time at `severe_scale_v21` if feasible.

This separates sustained severe-risk handling from transient high-risk
predictions. It should reduce oscillation and avoid spending long periods at
`0.65` unless severe risk persists.

## Failure-Mode-Aware Interpretation

Failure modes should guide how aggressively scale is reduced:

- `command_saturation_before_nan` may benefit from downscaling.
- `state_divergence_before_command_nan` may not always be solved by slower
  scaling.
- `reference_jump_before_command_nan` suggests planner/reference issues, not
  only adapter issues.
- `command_saturation_without_divergence` should not force excessive
  downscale.

Diagnostic labels are heuristic. They should inform policy design, not replace
strict-valid / `label_strict_invalid` as the paper-facing metric.

## Evaluation Plan

First screening:

- `goal_repeat=1` only
- wind: `strong`
- Trial 4, Trial 5, Trial 6
- repeat1, repeat2, repeat3
- compare:
  - `fixed_s080`
  - `risk_adapter_v2`
  - `risk_adapter_v2.1`
- main metric: strict-valid / `label_strict_invalid`
- also inspect diagnostic labels and mean scale behavior

Expansion rule:

- If `risk_adapter_v2.1 >= 8/9`, expand to 10 repeats.
- If `risk_adapter_v2.1 = 7/9`, inspect failure modes before expanding.
- If `risk_adapter_v2.1 <= 6/9`, revise policy before expansion.

Keep `goal_repeat=10` as a separate repeated-goal stress protocol. Do not mix
single-goal mission and repeated-goal stress results into one unlabeled table.

## Success Criteria

`risk_adapter_v2.1` should satisfy these criteria before any stronger claim:

- Preserve Trial 4 near `9/10` behavior.
- Improve Trial 6 relative to `risk_adapter_v2`'s `6/10`.
- Exceed `21/30` in the full single-goal benchmark.
- Ideally match or beat `fixed_s080` Trial 6 `8/10`.
- Do not increase NaN/divergence frequency.

## What Not To Claim

- Do not claim `risk_adapter_v2.1` superiority before experiments.
- Do not claim `fixed_s080` is weak.
- Do not claim a safety guarantee.
- Do not claim lower scale is always safer.
- Do not mix `goal_repeat=1` and `goal_repeat=10` results.

## Implementation Status And Next Evaluation

Stage 4-V2 minimal implementation status:

- `policy_mode=risk_adapter_v21` is implemented.
- Keep `risk_adapter_v2` unchanged.
- Params are added for `high_long_horizon_scale_v21`, severe dwell, ordinary
  downscale dwell, and upscale dwell.
- The first implementation is risk-only plus hysteresis/dwell.
- Execution diagnostics remain deferred with `use_execution_diagnostics_v21=false`.
- `risk_adapter_v21` remains disabled by default.
- Do not modify planner, controller, or simulator code.
- Compare `risk_adapter_v21` against `fixed_s080` and `risk_adapter_v2` under
  the single-goal protocol before any 10-repeat expansion.
