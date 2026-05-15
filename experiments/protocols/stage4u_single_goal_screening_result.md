# Stage 4-U Single-Goal Mission Screening Result

## Executive Summary

Stage 4-U single-goal mission screening is complete for strong-wind Trial
4/5/6 with `goal_repeat=1`.

`risk_adapter_v2` achieved `9/9` strict-valid runs. `fixed_s080` achieved
`6/9` strict-valid runs. This reverses the earlier `goal_repeat=10`
interpretation from the Stage 4-S4 screening and supports evaluating
`risk_adapter_v2` under the single-goal mission protocol before further
threshold tuning.

This is still a diagnostic screening, not a final benchmark. It is strong
evidence that `risk_adapter_v2` should be expanded under `goal_repeat=1`, but
it does not establish statistical significance, a safety guarantee, or final
overall superiority.

## Protocol

- protocol: single-goal mission protocol
- `goal_repeat=1`
- wind: `strong`
- trials: Trial 4, Trial 5, Trial 6
- repeats: repeat1, repeat2, repeat3
- methods: `fixed_s080`, `risk_adapter_v2`
- main metric: strict-valid / `label_strict_invalid`
- purpose: diagnostic screening, not final benchmark

## Result Table

| Method | Trial 4 | Trial 5 | Trial 6 | Aggregate |
| --- | ---: | ---: | ---: | ---: |
| `fixed_s080` | `1/3` | `3/3` | `2/3` | `6/9` |
| `risk_adapter_v2` | `3/3` | `3/3` | `3/3` | `9/9` |

## Repeat-Level Details

### `fixed_s080`

Trial 4:

- repeat1: invalid, `state_divergence_before_command_nan`,
  `arrival=false`, `first_nan=20.803475`.
- repeat2: invalid, `command_saturation_before_nan`, `arrival=false`,
  `first_nan=5.400723`.
- repeat3: valid, `command_saturation_without_divergence`, `arrival=true`.

Trial 5:

- repeat1: valid, `command_saturation_without_divergence`.
- repeat2: valid, `command_saturation_without_divergence`.
- repeat3: valid, `no_divergence_detected`.

Trial 6:

- repeat1: valid.
- repeat2: valid.
- repeat3: invalid, `state_divergence_before_command_nan`, `arrival=true`,
  `first_nan=42.950013`.

### `risk_adapter_v2`

Trial 4:

- repeats1-3: all valid.
- labels: `command_saturation_without_divergence` for all repeats.
- mean scale: around `0.844`.

Trial 5:

- repeats1-3: all valid.
- labels: `command_saturation_without_divergence` for all repeats.
- mean scale: around `0.755` to `0.800`.

Trial 6:

- repeats1-3: all valid.
- labels: `command_saturation_without_divergence`,
  `command_saturation_without_divergence`, and `no_divergence_detected`.
- mean scale: around `0.666`.

## Interpretation

`risk_adapter_v2` performs strongly under the single-goal mission protocol in
this screening. `fixed_s080` remains a strong tuned static reference, but it
was less reliable than `risk_adapter_v2` in these nine single-goal runs.

The `risk_adapter_v2` behavior is adaptive rather than a `fixed_s080` clone:
it used a mean scale near `0.85` on Trial 4, around `0.75` to `0.80` on Trial
5, and around `0.65` on Trial 6. This supports the interpretation that the
policy is changing execution aggressiveness by target/run context.

The Trial 6 efficiency cost must be checked before any stronger claim because
`risk_adapter_v2` used a low mean scale there. A method can be strict-valid
while still being too conservative for the final paper-facing efficiency
tradeoff.

## Relationship To Stage 4-T2

Stage 4-T2 showed that `goal_repeat=10` can introduce post-arrival
repeated-goal / replan stress. Stage 4-U should therefore be interpreted as
single-goal mission screening.

Previous `goal_repeat=10` results remain useful as repeated-goal stress-test
evidence. They should not be discarded, but they should not be used as clean
single-goal mission evidence.

## Research Decision

- Do not tune `risk_adapter_v2` yet.
- Expand `risk_adapter_v2` and `fixed_s080` under `goal_repeat=1` to 10
  repeats across Trial 4/5/6.
- If `risk_adapter_v2` remains stronger, promote the single-goal mission
  protocol as the primary benchmark.
- Keep `goal_repeat=10` as the repeated-goal stress benchmark.
- Continue to label every Stage 4 result table with the goal protocol.

## What Not To Claim

- Do not claim final `risk_adapter_v2` superiority from these nine runs.
- Do not claim statistical significance.
- Do not claim a safety guarantee.
- Do not discard repeated-goal stress results.
- Do not claim `fixed_s080` is weak; it remains the tuned static frontier
  under `goal_repeat=10`.
