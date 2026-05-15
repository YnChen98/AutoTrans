# Stage 4-S Risk Adapter V2 Design

## Executive Summary

Stage 4-S proposes `risk_adapter_v2`, the next risk-conditioned command
adaptation direction after the Stage 4-R `fixed_s080` frontier result.

`risk_adapter_v2` should be designed to match or beat `fixed_s080` while
retaining adaptive behavior. It should not be framed as simple threshold
tuning. The intended method is a calibrated risk-conditioned execution
governor that selects command scale from calibrated risk, failure-mode
diagnostics, and runtime execution signals.

Stage 4-S3 implements the first minimal `risk_adapter_v2` policy mode in
`experiments/command_adaptation/scripts/risk_conditioned_command_adapter.py`.
This first pass is risk-only plus hysteresis. It reuses the existing command
adaptation output topics and is disabled by default.

Stage 4-S4 screening should be interpreted cautiously because the current
screening protocol used repeated `/move_base_simple/goal` publication through
`goal_repeat=10`. This may introduce a repeated-goal / post-arrival replan
stress artifact that is distinct from normal single-goal transport success or
failure. Stage 4-T1 goal reception, arrival, and post-arrival trajectory-update
diagnostics must be added and inspected before further `risk_adapter_v2`
tuning.

## Motivation

The current balanced Trial 4/5/6 results are:

| Method | Strict-valid aggregate |
| --- | ---: |
| `original` | `18/30` |
| `fixed_s085` | `18/30` |
| `windlevel_s085` | `16/30` |
| `risk_adapter_v1` | `23/30` |
| `fixed_s080` | `24/30` |

`risk_adapter_v1` improves over `original`, `fixed_s085`, and
`windlevel_s085`, but the tuned static `fixed_s080` frontier slightly exceeds
it. Therefore `risk_adapter_v2` must use `fixed_s080` as the static frontier
reference.

The goal is not merely to slow down more. The goal is to adapt command scale
based on risk, likely failure mode, and runtime execution signals, while using
the strong `fixed_s080` operating point as the default reference.

## V1 Limitation

`risk_adapter_v1` uses fixed thresholds and fixed scale outputs:

- `soft_scale_3s=0.75`
- `soft_scale_5s=0.65`
- `hard_scale_5s=0.60`
- `risk_threshold_3s=0.5`
- `risk_threshold_5s=0.5`
- `hard_threshold_5s=0.7`
- `scale_rate_limit_per_sec=0.5`

This makes `risk_adapter_v1` useful as a first learned governor, but it has
several limitations:

- It may be too conservative in some cases and not conservative enough in
  others.
- It does not explicitly use `fixed_s080` as the baseline operating point.
- It does not yet use failure-mode-aware features strongly enough.
- It does not yet use calibrated risk bins as the main decision input.
- It lacks strong hysteresis and dwell-time logic around threshold crossings.

## Proposed V2 Policy

First candidate policy:

```text
base_scale = 0.80
```

Low risk:

- Allow `0.85` when both 3s and 5s calibrated risks are low.
- Only allow `0.85` if no recent saturation, reference jump, or replan upset
  is observed.

Medium risk:

- Use `0.80`.

High short-horizon risk:

- Use `0.75`.

High 5s risk or sustained risk:

- Use `0.65`.

Severe diagnostic trigger:

- Optionally use `0.60` or a hold-like conservative mode.
- This should be diagnostic / safety-ablation only, not the default behavior.

This policy uses `fixed_s080` as the center operating point, not as a fallback
after risk detection fails.

Stage 4-S3 parameter names:

- `base_scale_v2=0.80`
- `low_risk_fast_scale_v2=0.85`
- `medium_scale_v2=0.80`
- `high_short_horizon_scale_v2=0.75`
- `high_long_horizon_scale_v2=0.65`
- `severe_scale_v2=0.60`
- `enable_severe_scale_v2=false`
- `low_risk_threshold_3s_v2=0.30`
- `low_risk_threshold_5s_v2=0.30`
- `high_risk_threshold_3s_v2=0.50`
- `high_risk_threshold_5s_v2=0.50`
- `severe_risk_threshold_5s_v2=0.70`
- `enable_hysteresis_v2=true`
- `upscale_dwell_time_sec_v2=2.0`
- `downscale_dwell_time_sec_v2=0.0`
- `use_execution_diagnostics_v2=false`

## Hysteresis And Rate Limit

`risk_adapter_v2` should keep `scale_rate_limit_per_sec` and add explicit
hysteresis so scale does not oscillate near risk thresholds.

Required behavior:

- Keep rate limiting for scale changes.
- Add separate enter and exit thresholds for low/medium/high risk bins.
- Add a minimum dwell time before returning to a faster scale.
- Downscale faster than upscale if needed.
- Do not immediately return to `0.85` after one low-risk prediction if recent
  diagnostic events are still active.

## Calibration

`risk_adapter_v2` should use the calibration diagnostics already available
from the Stage 4 risk predictor workflow:

- calibration bins
- ECE
- Brier score
- threshold sweep
- group metrics

The policy should convert raw risk score into a calibrated risk bin before
selecting scale. Calibration should improve interpretability of low/medium/high
risk thresholds, but it does not provide a formal statistical or safety
guarantee by itself.

Optional later extension:

- conformal or confidence-aware decision logic
- abstain / conservative fallback when model confidence is poor
- per-target or per-failure-mode calibration if enough data exists

## Failure-Mode-Aware Features

Candidate online features for `risk_adapter_v2`:

- `command_saturation_count`
- `sustained_command_saturation_event`
- `trajectory_publish_count`
- `trajectory_update_count`
- `trajectory_time_since_last_update`
- reference jump indicators
- short-window tracking error
- swing angle growth rate
- payload speed trend
- UAV speed trend
- prior risk score persistence
- `wind_force_norm`

These features should be optional and used only when available. Missing
diagnostic streams should not break the adapter; the policy should fall back to
calibrated risk and base-scale behavior.

Stage 4-S3 defers command, reference, and trajectory diagnostic subscriptions.
The minimal implementation uses only the existing online risk scores and local
hysteresis state. Later v2 extensions may add these diagnostics without changing
planner, controller, or simulator code.

## Failure-Mode-Aware Decision Logic

Command/control-upstream risk should trigger conservative scaling earlier,
especially when saturation is sustained or paired with rising short-horizon
risk.

Planner/reference-upstream risk should avoid accelerating back to `0.85`,
because faster execution can amplify reference discontinuities or replan upset.

State/task-upstream risk should prefer sustained conservative scale, especially
when tracking error, swing growth, or speed trend indicates the vehicle is
already near a strict-invalid condition.

Transient `command_saturation_without_divergence` should not automatically
force failure classification or excessive slowdown. It should be treated as a
warning signal whose effect depends on persistence, co-occurring risk, and
whether NaN/divergence or strict safety evidence follows.

## Evaluation Plan

Stage 4-T1 diagnostic prerequisite:

- Log `/move_base_simple/goal` reception count and timing.
- Estimate first arrival time from target-error and low-speed criteria.
- Report post-arrival goal reception and trajectory-update counts.
- Separate single-goal mission evidence from repeated-goal stress evidence.
- Do not tune `risk_adapter_v2` further until the current Stage 4-S4 failures
  are checked against these diagnostics.

Initial `risk_adapter_v2` screening:

- Trials: Trial 4, Trial 5, Trial 6.
- Repeats: 3 repeats per trial.
- Compare against `fixed_s080` and `risk_adapter_v1`.
- Use strict-valid / `label_strict_invalid` as the main metric.
- Also report diagnostic labels and efficiency metrics.

Full `risk_adapter_v2` evaluation:

- Expand to 10 repeats only if screening is competitive.
- Compare:
  - `original`
  - `fixed_s085`
  - `fixed_s080`
  - `windlevel_s085`
  - `risk_adapter_v1`
  - `risk_adapter_v2`

Do not mix diagnostic smoke runs into the main evaluation.

## Success Criteria

`risk_adapter_v2` should satisfy these criteria before any overall-best claim:

- It must reach at least `24/30` to match `fixed_s080`.
- It should exceed `24/30` to justify an overall-best claim.
- It should not degrade Trial 4 far below `fixed_s080`.
- It should maintain or improve Trial 5 and Trial 6 performance.
- It should reduce `command_saturation_before_nan` and
  `state_divergence_before_command_nan` counts if possible.

## What Not To Claim

- Do not claim `risk_adapter_v2` has a safety guarantee.
- Do not claim `fixed_s080` is weak.
- Do not claim `risk_adapter_v1` is overall best after Stage 4-R.
- Do not claim calibration gives a formal guarantee unless separately proven.
- Do not claim diagnostic labels are perfect root-cause proof.

## Next Coding Task

Stage 4-S3 implementation status:

- `risk_adapter_v2` policy mode is implemented and disabled by default.
- The first pass is risk-only plus hysteresis.
- `risk_adapter_v1` behavior remains available as `policy_mode=risk_conditioned`.
- Command, reference, and trajectory diagnostics are deferred to later v2
  extensions.

Recommended follow-up:

- Run static checks first.
- Screen `risk_adapter_v2` against `fixed_s080` and `risk_adapter_v1`.
- Do not run the full 10-repeat evaluation until the screening result is
  competitive.
- Do not claim `risk_adapter_v2` is better than `fixed_s080` before experiments.
