# Stage 4-H3 Risk Adapter v1 Aggregate Result

## Executive Summary

This earlier limited aggregate has been superseded by the balanced 30-repeat
Stage 4-J aggregate in
`experiments/protocols/stage4j_balanced_30repeat_aggregate_result.md`.

The superseding balanced result is: `risk_adapter_v1` `23/30`, `original`
`18/30`, `fixed_s085` `18/30`, and `windlevel_s085` `16/30`, using
strict-valid / `label_strict_invalid` as the paper-facing metric.

`risk_adapter_v1` is the strongest current candidate in the limited-repeat
strong-wind Trial 4, Trial 5, and Trial 6 evaluation.

Across Trial 4, Trial 5, and Trial 6, `risk_adapter_v1` achieved `13/15` valid
runs. The comparable aggregate results are `9/15` for `original`, `9/15` for
`fixed_s085`, and `6/15` for `windlevel_s085`.

This is a promising limited-repeat result, not a final robustness proof. The
Trial 4 repeat5 and Trial 6 repeat1 failures remain important negative
evidence.

The `risk_adapter_v1` policy used:

- `soft_scale_3s=0.75`
- `soft_scale_5s=0.65`
- `hard_scale_5s=0.60`
- `risk_threshold_3s=0.5`
- `risk_threshold_5s=0.5`
- `hard_threshold_5s=0.7`
- `scale_rate_limit_per_sec=0.5`

## Method Comparison Table

| Method | Trial 4 | Trial 5 | Trial 6 | Trial 4+5+6 | Notes |
| --- | ---: | ---: | ---: | ---: | --- |
| `original` | `4/5` valid | `3/5` strict-valid | `2/5` valid | `9/15` valid | Historical baseline. |
| `fixed_s085` | `5/5` valid | `2/5` valid | `2/5` valid | `9/15` valid | Strongest Trial 4 result, but weaker on Trial 5 and Trial 6. |
| `windlevel_s085` | `1/5` valid | `3/5` valid | `2/5` valid | `6/15` valid | Weakest aggregate result across these targets. |
| `risk_adapter_v0` | `n/a` | `2/5` valid | `4/5` valid | `6/10` valid where tested | Prior risk-conditioned adapter; not evaluated on Trial 4 in this comparison. |
| `risk_adapter_v1` | `4/5` valid | `5/5` valid | `4/5` valid | `13/15` valid | Current strongest limited-repeat candidate. |

## Per-Target Analysis

### Trial 4

`risk_adapter_v1` achieved `4/5` valid runs on Trial 4. This matches
`original`, underperforms `fixed_s085`, and is much better than
`windlevel_s085`.

The result is mixed because Trial 4 repeat5 failed with a NaN at
`first_nan_time=24.900021`. The failure timing suggests that the risk trigger
came too late: `first_swing_angle_ge_30_time=25.150046`,
`first_command_risk_score_3s_ge_0p5_time=27.599985`, and
`first_command_risk_score_5s_ge_0p5_time=29.599997`.

### Trial 5

`risk_adapter_v1` achieved `5/5` valid runs on Trial 5 and is the best method
in this limited-repeat comparison.

The Trial 5 result suggests that stronger early intervention addressed the
`risk_adapter_v0` failures on this target. The comparison is especially useful
because `risk_adapter_v0` achieved only `2/5` valid runs on Trial 5, while
`risk_adapter_v1` achieved `5/5`.

### Trial 6

`risk_adapter_v1` achieved `4/5` valid runs on Trial 6. This matches
`risk_adapter_v0` and beats the historical Trial 6 baselines, where
`original`, `fixed_s085`, and `windlevel_s085` each achieved `2/5` valid runs.

The result is still not a robustness claim. Trial 6 repeat1 failed with a NaN
at `first_nan_time=25.099965`, despite early risk activation before safety
violation.

## Failure Analysis

Trial 4 repeat5 is primarily a risk timing and detection failure. The NaN
appeared at `24.900021`, the swing threshold crossed at `25.150046`, and the
first `3s` risk threshold crossing did not appear until `27.599985`. The
adapter therefore reacted after the critical failure window had already
started.

Trial 6 repeat1 is a different failure mode. Early risk activation occurred
before the safety-threshold violations, but the intervention was still
insufficient or the hard threshold arrived too late. The `3s` threshold crossed
at `7.699993`, the `5s` `0.5` threshold crossed at `9.700228`, the swing
threshold crossed at `11.049988`, and the payload-speed threshold crossed at
`11.699972`. The hard `5s >= 0.7` threshold crossed only at `29.900020`, after
the NaN at `25.099965`.

These failures motivate a later `risk_adapter_v2` design, but not before
documenting the `risk_adapter_v1` aggregate result. The two failures should be
kept visible because they separate model timing limitations from scale-policy
limitations.

## Research Decision

`risk_adapter_v1` should become the current main candidate for Stage 4-H
risk-conditioned command adaptation.

Reasonable next steps are:

- Run a slightly larger repeat set for Trial 4, Trial 5, and Trial 6.
- Add a formal aggregate table or figure generation script.
- Design `risk_adapter_v2` based on the Trial 4 and Trial 6 failure timing.

Do not tune further before recording this aggregate result.

## What Not To Claim

- Do not claim statistical significance.
- Do not claim a safety guarantee.
- Do not claim final online robustness.
- Do not hide the Trial 4 repeat5 and Trial 6 repeat1 failures.
- Do not claim superiority over `fixed_s085` on every target, because
  `fixed_s085` is `5/5` on Trial 4 while `risk_adapter_v1` is `4/5`.

## Paper-Framing Note

This result supports the paper direction: early learned risk estimates can
condition high-level command adaptation and improve limited-repeat transport
robustness in strong-wind suspended-payload simulation.

Claims must remain simulation-only and limited-repeat.
