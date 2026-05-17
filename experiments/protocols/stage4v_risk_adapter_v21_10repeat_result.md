# Stage 4-V4 Risk Adapter V2.1 10-Repeat Result

## Executive Summary

Stage 4-V4 expanded `risk_adapter_v21` under the single-goal mission protocol.

`risk_adapter_v21` achieved `25/30` strict-valid runs across strong-wind Trial
4, Trial 5, and Trial 6 repeat1-10. At Stage 4-V4 it was the strongest method
among the then-evaluated single-goal methods, exceeding both `fixed_s080` and
`risk_adapter_v2`, which each achieved `21/30` in Stage 4-U2.

This is a meaningful improvement in the current 30-run single-goal benchmark,
but it should not be presented as statistical significance or as a safety
guarantee. Trial 6 remains the bottleneck: `risk_adapter_v21` achieved `6/10`
there, while `fixed_s080` achieved `8/10`.

Stage 4-X1 later evaluated `risk_adapter_v21` under the goal-reissue stress
protocol and recorded a corrected `20/30` result. That is below `fixed_s080`
(`24/30`) and `risk_adapter_v1` (`23/30`) under stress, so this single-goal
result should not be read as a cross-protocol final win.

Stage 4-X2 later completed the missing single-goal baselines. In the completed
single-goal comparison, `windlevel_s085` achieved `26/30`, while
`risk_adapter_v1` and `risk_adapter_v21` each achieved `25/30`. Therefore this
Stage 4-V4 result remains competitive but should no longer be described as the
best completed single-goal aggregate.

## Protocol

- protocol: single-goal mission protocol
- `goal_repeat=1`
- wind: `strong`
- trials: Trial 4, Trial 5, Trial 6
- repeats: repeat1 through repeat10
- method: `risk_adapter_v21`
- main metric: strict-valid / `label_strict_invalid`

## Method Comparison Table

Stage 4-V4 single-goal mission protocol comparison at the time:

| Method | Strict-valid count | Repeat count |
| --- | ---: | ---: |
| `fixed_s080` | `21` | `30` |
| `risk_adapter_v2` | `21` | `30` |
| `risk_adapter_v21` | `25` | `30` |

`risk_adapter_v21` exceeds `fixed_s080` by 4 strict-valid runs and exceeds
`risk_adapter_v2` by 4 strict-valid runs in this 30-run single-goal benchmark.
This comparison does not yet include `original`, `fixed_s085`,
`windlevel_s085`, or `risk_adapter_v1` under `goal_repeat=1`.

Stage 4-X2 completed those missing baselines and supersedes the "current"
comparison scope:

| Method | Strict-valid count | Repeat count |
| --- | ---: | ---: |
| `original` | `21` | `30` |
| `fixed_s085` | `22` | `30` |
| `windlevel_s085` | `26` | `30` |
| `fixed_s080` | `21` | `30` |
| `risk_adapter_v1` | `25` | `30` |
| `risk_adapter_v2` | `21` | `30` |
| `risk_adapter_v21` | `25` | `30` |

After Stage 4-X2, `risk_adapter_v21` is tied with `risk_adapter_v1` and is one
strict-valid run below `windlevel_s085` in the completed single-goal aggregate.

## Per-Trial Table

| Method | Trial 4 | Trial 5 | Trial 6 | Aggregate |
| --- | ---: | ---: | ---: | ---: |
| `risk_adapter_v21` | `10/10` | `9/10` | `6/10` | `25/30` |

Trial 4:

- strict-valid: `10/10`
- all runs valid
- diagnostic labels: `command_saturation_without_divergence` (`10`)
- mean scale around `0.843`
- interpretation: `risk_adapter_v21` preserves strong Trial 4 behavior and
  uses near-fast scale in the `0.80` to `0.85` range.

Trial 5:

- strict-valid: `9/10`
- repeat6 was invalid with `has_nan_state=false`, `final_xy=0.728490`, and
  `mode=command_saturation_without_divergence`
- interpretation for repeat6: likely target-error / no-arrival failure rather
  than NaN/divergence
- diagnostic labels: `command_saturation_without_divergence` (`8`),
  `no_divergence_detected` (`2`)
- mean scale around `0.720`
- interpretation: `risk_adapter_v21` is strong on Trial 5, but one
  target-error / no-arrival run remains.

Trial 6:

- strict-valid: `6/10`
- repeat6: `state_divergence_before_command_nan`, `first_nan=39.851856`,
  `failure_after_arrival=true`
- repeat7: `no_divergence_detected` but strict-invalid with
  `final_xy=14.911115` and `arrival=false`; interpret as target-error /
  no-arrival rather than true no-failure success
- repeat8: `command_nan_before_state_divergence`, `first_nan=8.801941`
- repeat9: `state_divergence_before_command_nan`, `first_nan=73.451881`,
  `failure_after_arrival=true`
- diagnostic labels: `command_saturation_without_divergence` (`5`),
  `no_divergence_detected` (`1`),
  `state_divergence_before_command_nan` (`2`),
  `command_nan_before_state_divergence` (`1`),
  `swing_warning_no_nan` (`1`)
- mean scale around `0.736`
- interpretation: Trial 6 remains the main bottleneck. Failures include
  post-arrival divergence, early NaN/divergence, and target-error / no-arrival
  cases. Future work should focus on these Trial 6 failure families, not on
  global downscaling.

## Diagnostic Label Summary

Aggregate diagnostic-label counts for `risk_adapter_v21`:

| Diagnostic label | Count |
| --- | ---: |
| `command_nan_before_state_divergence` | `1` |
| `command_saturation_without_divergence` | `23` |
| `no_divergence_detected` | `3` |
| `state_divergence_before_command_nan` | `2` |
| `swing_warning_no_nan` | `1` |

`command_saturation_without_divergence` is not a failure by itself. It means
the command reached a diagnostic saturation threshold without NaN/divergence or
strict-invalid evidence in the inspector taxonomy.

`no_divergence_detected` can still coincide with target-error or no-arrival in
strict-valid analysis. Therefore strict-valid / `label_strict_invalid` remains
the primary paper-facing metric.

Diagnostic labels remain heuristic timing labels, not perfect root-cause proof.

## Scale Behavior Analysis

Observed scale summary:

- `aggregate_mean_of_mean_scale=0.766376`
- `aggregate_min_mean_scale=0.710587`
- `aggregate_max_mean_scale=0.843137`
- `mean_first_arrival_time=14.737031`
- `min_first_arrival_time=11.499970`
- `max_first_arrival_time=25.999959`

Per-trial interpretation:

- Trial 4 used near-fast scale around `0.843`.
- Trial 5 and Trial 6 used lower scales around `0.71` to `0.74`.
- `risk_adapter_v21` avoided the long-duration `0.65` behavior observed as a
  concern in `risk_adapter_v2`.
- `risk_adapter_v21` is adaptive and should not be described as a
  `fixed_s080` clone.

The result supports the Stage 4-V design premise: avoiding ordinary
long-duration `0.65` behavior can improve aggregate single-goal performance
without losing Trial 4 behavior.

## Trial 6 Bottleneck Analysis

Trial 6 remains weak at `6/10`. This matters because `fixed_s080` achieved
`8/10` on Trial 6 in Stage 4-U2.

The invalid Trial 6 runs are not one uniform failure type:

- Some failures occurred after arrival.
- One run was target-error / no-arrival without inspector divergence.
- Some failures were NaN/divergence cases.

After Stage 4-X0 completion, any future `risk_adapter_v21.1` or
`risk_adapter_v22` work should focus on Trial 6 failure families. The next
policy change should not simply lower scale globally, because
`risk_adapter_v21` already improves the aggregate result and because lower
scale is not automatically safer.

## Relationship To Stage 4-T / U

Stage 4-T established that the goal protocol must be labeled explicitly:

- `goal_repeat=1` is the single-goal mission protocol.
- `goal_repeat=10` is the goal-reissue stress protocol.

Do not mix these protocols into one aggregate table without protocol labels.

Stage 4-U2 recorded the prior single-goal comparison:

- `fixed_s080`: `21/30`
- `risk_adapter_v2`: `21/30`

Stage 4-V4 adds:

- `risk_adapter_v21`: `25/30`

Goal-reissue stress results remain separate. Stage 4-X1 records the corrected
stress comparison: `fixed_s080` `24/30`, `risk_adapter_v1` `23/30`, and
`risk_adapter_v21` `20/30` under `goal_repeat=10`.

Stage 4-X0 in
`experiments/protocols/stage4x_final_evaluation_spec.md` defines the final
completion matrix before any new `risk_adapter_v21.1` or `risk_adapter_v22`
variant is created. Stage 4-X1 completed the goal-reissue stress cell, and
Stage 4-X2 completed the missing single-goal baselines.

## Research Decision

- Treat `risk_adapter_v21` as a competitive single-goal method tied with
  `risk_adapter_v1`, not as the completed single-goal winner.
- Treat `windlevel_s085` as the strongest completed single-goal aggregate
  method at `26/30`.
- Treat Stage 4-X1 as evidence that `risk_adapter_v21` is not the strongest
  goal-reissue stress method.
- Before further tuning, update the protocol-split paper assets and perform
  failure analysis.
- Keep the goal-reissue stress protocol as a separate benchmark.

## What Not To Claim

- Do not claim statistical significance from the current counts.
- Do not claim a safety guarantee.
- Do not claim `risk_adapter_v21` solves Trial 6.
- Do not claim `risk_adapter_v21` is the best single-goal method.
- Do not claim `risk_adapter_v21` beats all baselines under the single-goal
  protocol.
- Do not claim `risk_adapter_v21` is best under goal-reissue stress.
- Do not claim `risk_adapter_v21` is a cross-protocol final winner.
- Do not claim learned methods uniformly dominate heuristic or fixed baselines.
- Do not mix `goal_repeat=1` and `goal_repeat=10` results without protocol
  labels.
- Do not claim diagnostic labels are perfect root-cause proof.
- Do not create a new `risk_adapter_v21.1` or `risk_adapter_v22` variant before
  updating paper assets and completing failure analysis.
