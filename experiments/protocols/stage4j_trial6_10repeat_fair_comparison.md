# Stage 4-J Trial 6 10-Repeat Fair Comparison

## Executive Summary

Trial 6 fair 10-repeat comparison is complete for `original`, `fixed_s085`,
`windlevel_s085`, and `risk_adapter_v1`.

Using strict-valid / `label_strict_invalid` interpretation,
`risk_adapter_v1` is strongest on Trial 6 with `7/10` strict-valid runs.
`windlevel_s085` is second with `6/10`, `fixed_s085` is `4/10`, and
`original` is `3/10`.

Trial 6 remains difficult for all methods. The margin between
`risk_adapter_v1` and `windlevel_s085` is modest, and these results should not
be presented as statistical significance, a safety guarantee, or final online
robustness.

## Trial 6 Method Comparison Table

| Method | Strict-valid count | Repeat count | Success rate | Raw `valid_run_suggested` count | Dominant failure-mode notes |
| --- | ---: | ---: | ---: | ---: | --- |
| `original` | `3` | `10` | `0.300` | `3/10` | Mostly `state_divergence_before_command_nan`; also `command_saturation_before_nan`, valid saturation-only diagnostics, and one `swing_warning_no_nan`. |
| `fixed_s085` | `4` | `10` | `0.400` | `4/10` | Mostly `command_saturation_before_nan`; one no-NaN strict safety/target failure. |
| `windlevel_s085` | `6` | `10` | `0.600` | `6/10` | Mix of `command_saturation_before_nan`, many valid `command_saturation_without_divergence` runs, and one `state_divergence_before_command_nan`. |
| `risk_adapter_v1` | `7` | `10` | `0.700` | `7/10` | Mostly valid or saturation-without-divergence cases; failures include `state_divergence_before_command_nan` and `reference_jump_before_command_nan`. |

## Repeat-Level Result Table

| Method | Repeat | `strict_valid` | NaN status | `first_nan_time` | Compact failure note |
| --- | ---: | --- | --- | ---: | --- |
| `original` | 1 | `true` | no NaN |  | strict-valid |
| `original` | 2 | `false` | NaN | `11.994827` | NaN strict-invalid |
| `original` | 3 | `false` | NaN | `8.073223` | NaN strict-invalid |
| `original` | 4 | `false` | NaN | `15.000126` | NaN strict-invalid |
| `original` | 5 | `true` | no NaN |  | strict-valid |
| `original` | 6 | `true` | no NaN |  | strict-valid |
| `original` | 7 | `false` | NaN | `20.000981` | NaN strict-invalid |
| `original` | 8 | `false` | NaN | `8.344965` | NaN strict-invalid |
| `original` | 9 | `false` | NaN | `43.686064` | NaN strict-invalid |
| `original` | 10 | `false` | NaN | `14.950161` | NaN strict-invalid |
| `fixed_s085` | 1 | `false` | NaN | `20.282728` | NaN strict-invalid |
| `fixed_s085` | 2 | `false` | NaN | `19.850080` | NaN strict-invalid |
| `fixed_s085` | 3 | `false` | NaN | `14.900028` | NaN strict-invalid |
| `fixed_s085` | 4 | `true` | no NaN |  | strict-valid |
| `fixed_s085` | 5 | `true` | no NaN |  | strict-valid |
| `fixed_s085` | 6 | `false` | NaN | `50.800010` | NaN strict-invalid |
| `fixed_s085` | 7 | `false` | NaN | `35.149583` | NaN strict-invalid |
| `fixed_s085` | 8 | `true` | no NaN |  | strict-valid |
| `fixed_s085` | 9 | `true` | no NaN |  | strict-valid |
| `fixed_s085` | 10 | `false` | no NaN |  | payload speed `4.107203`, final XY error `2.347776` |
| `windlevel_s085` | 1 | `false` | NaN | `16.349862` | NaN strict-invalid |
| `windlevel_s085` | 2 | `false` | NaN | `14.637101` | NaN strict-invalid |
| `windlevel_s085` | 3 | `true` | no NaN |  | strict-valid |
| `windlevel_s085` | 4 | `false` | NaN | `24.945165` | NaN strict-invalid |
| `windlevel_s085` | 5 | `true` | no NaN |  | strict-valid |
| `windlevel_s085` | 6 | `true` | no NaN |  | strict-valid |
| `windlevel_s085` | 7 | `false` | NaN | `14.799990` | NaN strict-invalid |
| `windlevel_s085` | 8 | `true` | no NaN |  | strict-valid |
| `windlevel_s085` | 9 | `true` | no NaN |  | strict-valid |
| `windlevel_s085` | 10 | `true` | no NaN |  | strict-valid |
| `risk_adapter_v1` | 1 | `false` | NaN | `25.099965` | NaN strict-invalid |
| `risk_adapter_v1` | 2 | `true` | no NaN |  | strict-valid |
| `risk_adapter_v1` | 3 | `true` | no NaN |  | strict-valid |
| `risk_adapter_v1` | 4 | `true` | no NaN |  | strict-valid |
| `risk_adapter_v1` | 5 | `true` | no NaN |  | strict-valid |
| `risk_adapter_v1` | 6 | `true` | no NaN |  | strict-valid |
| `risk_adapter_v1` | 7 | `true` | no NaN |  | strict-valid |
| `risk_adapter_v1` | 8 | `true` | no NaN |  | strict-valid |
| `risk_adapter_v1` | 9 | `false` | NaN | `14.899877` | NaN strict-invalid |
| `risk_adapter_v1` | 10 | `false` | NaN | `14.799948` | NaN strict-invalid |

## Failure-Mode Analysis

Trial 6 `original` failures are mostly `state_divergence_before_command_nan`.
Its failure-mode counts are:

- `command_saturation_before_nan`: `2`
- `command_saturation_without_divergence`: `2`
- `state_divergence_before_command_nan`: `5`
- `swing_warning_no_nan`: `1`

`fixed_s085` failures are mostly `command_saturation_before_nan`, with one
no-NaN strict safety / target failure:

- `command_saturation_before_nan`: `5`
- `command_saturation_without_divergence`: `4`
- `strict_safety_no_nan`: `1`

`windlevel_s085` has both `command_saturation_before_nan` failures and valid
`command_saturation_without_divergence` cases:

- `command_saturation_before_nan`: `3`
- `command_saturation_without_divergence`: `6`
- `state_divergence_before_command_nan`: `1`

`risk_adapter_v1` has mostly valid / saturation-without-divergence cases, but
its failures include `state_divergence_before_command_nan` and
`reference_jump_before_command_nan`:

- `command_saturation_without_divergence`: `6`
- `no_divergence_detected`: `1`
- `reference_jump_before_command_nan`: `1`
- `state_divergence_before_command_nan`: `2`

Transient `command_saturation_without_divergence` should not be treated as a
failure by itself. `swing_warning_no_nan` is warning-only, not a strict failure
by itself.

## Balanced Aggregate Interpretation

With Trial 4, Trial 5, and Trial 6 all at 10 repeats for the main four methods,
the balanced aggregate is:

| Method | Trial 4 | Trial 5 | Trial 6 | Balanced aggregate |
| --- | ---: | ---: | ---: | ---: |
| `original` | `8/10` | `7/10` | `3/10` | `18/30` |
| `fixed_s085` | `9/10` | `5/10` | `4/10` | `18/30` |
| `windlevel_s085` | `4/10` | `6/10` | `6/10` | `16/30` |
| `risk_adapter_v1` | `7/10` | `9/10` | `7/10` | `23/30` |

`risk_adapter_v1` is strongest in aggregate at `23/30`. `original` and
`fixed_s085` are tied at `18/30`, and `windlevel_s085` is `16/30`.

`risk_adapter_v1` is not best on every target: `fixed_s085` remains best on
Trial 4 with `9/10`. Trial 6 supports `risk_adapter_v1` as the strongest
candidate, but the margin over `windlevel_s085` is modest.

## Research Decision

Stage 4 30-repeat balanced comparison is now complete for Trial 4, Trial 5,
and Trial 6 across `original`, `fixed_s085`, `windlevel_s085`, and
`risk_adapter_v1`.

Next step should be to update the aggregate manifest and regenerate the
Stage 4-H adapter result summary. Do not tune `risk_adapter_v2` before
recording these balanced results. Do not mix diagnostic smoke runs with these
main repeat results.

## What Not To Claim

- Do not claim statistical significance.
- Do not claim a safety guarantee.
- Do not claim `risk_adapter_v1` beats every baseline on every target.
- Do not treat all NaN/divergence as command-adaptation failures.
- Do not treat transient command saturation as failure.
