# Stage 4-T2 Goal-Repeat Artifact Diagnostic Result

## Executive Summary

Stage 4-T2 confirms that `goal_repeat=10` introduces a repeated-goal /
post-arrival stress condition. This condition is different from a normal
single-goal transport mission because the same `/move_base_simple/goal` can be
received after the UAV/payload has already reached or nearly reached the
target.

On strong-wind Trial 4, `risk_adapter_v2` was `3/3` strict-valid under
`goal_repeat=1`, but `0/3` strict-valid under `goal_repeat=10`. All
`risk_adapter_v2` `goal_repeat=10` failures occurred after arrival and after
post-arrival goal publishes. `fixed_s080` also had one `goal_repeat=10`
failure after arrival, but `fixed_s080` `goal_repeat=1` also failed before
arrival in two repeats. Therefore the repeated-goal artifact affects results,
but it does not explain all failures.

This diagnostic should not be treated as a final benchmark. It is a protocol
diagnostic that separates single-goal mission behavior from repeated-goal /
post-arrival replan stress behavior.

Stage 4-U later expanded the single-goal screening across Trial 4/5/6
repeat1-3. Under `goal_repeat=1`, `risk_adapter_v2` achieved `9/9`
strict-valid while `fixed_s080` achieved `6/9`. This supports the Stage 4-T2
protocol split: `goal_repeat=1` should be analyzed as single-goal mission
screening, while `goal_repeat=10` remains repeated-goal stress evidence.

Stage 4-U2 then expanded the single-goal mission protocol to repeat1-10 across
Trial 4/5/6. Under `goal_repeat=1`, `fixed_s080` and `risk_adapter_v2` both
achieved `21/30` strict-valid. This reinforces the protocol split: U2 is
single-goal mission evidence, while the Stage 4-R `fixed_s080` `24/30` and
Stage 4-J `risk_adapter_v1` `23/30` remain repeated-goal stress protocol
evidence.

## Test Setup

- wind: `strong`
- target: Trial 4
- methods: `fixed_s080`, `risk_adapter_v2`
- goal protocols: `goal_repeat=1` and `goal_repeat=10`
- repeats: repeat1, repeat2, repeat3
- purpose: diagnostic-only, not final benchmark evidence

Relevant prior code-path finding:

- `experiments/scripts/run_baseline_trial.sh` publishes
  `/move_base_simple/goal` according to `goal_repeat` and `goal_interval`.
- `goal_repeat=10` repeatedly publishes the same goal for roughly 9 seconds.
- `planner/plan_manage/src/replan_fsm.cpp` handles the goal in
  `ReplanFSM::waypointCallback`.
- `ReplanFSM::waypointCallback` does not ignore duplicate same-goal messages.
- Repeated same-goal messages may trigger new target handling, replan, and
  `/planning/trajectory` updates.

## Result Table

| Method | `goal_repeat` | Strict-valid count | Repeat count | Post-arrival failure count | Post-arrival goal observation |
| --- | ---: | ---: | ---: | ---: | --- |
| `fixed_s080` | 1 | 1 | 3 | 0 | no post-arrival goals in valid repeat; two failures occurred before arrival |
| `fixed_s080` | 10 | 2 | 3 | 1 | all repeats had arrival; all had `post_arrival_goals=8`; one failure after arrival |
| `risk_adapter_v2` | 1 | 3 | 3 | 0 | all repeats arrived; all had `post_arrival_goals=0`; all were strict-valid |
| `risk_adapter_v2` | 10 | 0 | 3 | 3 | all repeats arrived; all had `post_arrival_goals=8`; all failed after arrival |

## Repeat-Level Details

### `fixed_s080`, `goal_repeat=1`

| Repeat | Strict-valid | Raw valid | NaN | Mode | First NaN | Arrival | Goals | Post-arrival goals | Traj updates after arrival | Failure after arrival | Final XY | Max swing |
| --- | --- | --- | --- | --- | ---: | --- | ---: | ---: | ---: | --- | ---: | ---: |
| repeat1 | false | false | true | `state_divergence_before_command_nan` | 20.803475 | false | 1 | 0 | 0 | false | 73.736509 | 177.797893 |
| repeat2 | false | false | true | `command_saturation_before_nan` | 5.400723 | false | 1 | 0 | 0 | false | 181.624558 | 128.394528 |
| repeat3 | true | true | false | `command_saturation_without_divergence` | nan | true | 1 | 0 | 0 | false | 0.000393 | 14.749132 |

Summary: `1/3` strict-valid.

### `fixed_s080`, `goal_repeat=10`

| Repeat | Strict-valid | Raw valid | NaN | Mode | First NaN | Arrival | First arrival | Goals | Post-arrival goals | Time to next post-arrival goal | Traj updates after arrival | Failure after arrival | Final XY | Max swing |
| --- | --- | --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| repeat1 | false | false | true | `state_divergence_before_command_nan` | 30.900793 | true | 12.299937 | 10 | 8 | 2.218471 | 2 | true | 132.935322 | 79.197791 |
| repeat2 | true | true | false | `command_saturation_without_divergence` | nan | true | 13.449866 | 10 | 8 | 1.132243 | 6 | false | 0.013007 | 15.244624 |
| repeat3 | true | true | false | `command_saturation_without_divergence` | nan | true | 13.549931 | 10 | 8 | 1.124555 | 2 | false | 0.084549 | 17.750393 |

Summary: `2/3` strict-valid.

### `risk_adapter_v2`, `goal_repeat=1`

| Repeat | Strict-valid | Raw valid | NaN | Mode | Arrival | First arrival | Goals | Post-arrival goals | Traj updates after arrival | Failure after arrival | Final XY | Max swing |
| --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| repeat1 | true | true | false | `command_saturation_without_divergence` | true | 13.449841 | 1 | 0 | 0 | false | 0.000000 | 12.988650 |
| repeat2 | true | true | false | `command_saturation_without_divergence` | true | 12.949864 | 1 | 0 | 0 | false | 0.000000 | 14.068106 |
| repeat3 | true | true | false | `command_saturation_without_divergence` | true | 11.449895 | 1 | 0 | 0 | false | 0.000000 | 14.221634 |

Summary: `3/3` strict-valid.

### `risk_adapter_v2`, `goal_repeat=10`

| Repeat | Strict-valid | Raw valid | NaN | Mode | First NaN | Arrival | First arrival | Goals | Post-arrival goals | Time to next post-arrival goal | Traj updates after arrival | Failure after arrival | Final XY | Max swing |
| --- | --- | --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| repeat1 | false | false | true | `state_divergence_before_command_nan` | 21.801676 | true | 12.249902 | 10 | 8 | 2.432260 | 1 | true | 129.886369 | 155.655552 |
| repeat2 | false | false | false | `strict_safety_no_nan` | nan | true | 12.749986 | 10 | 8 | 1.886280 | 8 | true | 0.010770 | 129.421802 |
| repeat3 | false | false | true | `command_nan_before_state_divergence` | 14.799989 | true | 12.649954 | 10 | 8 | 1.985507 | 1 | true | 495.656769 | 158.486705 |

Summary: `0/3` strict-valid.

## Timing Interpretation

`risk_adapter_v2` with `goal_repeat=1` had no post-arrival goals and was `3/3`
strict-valid. `risk_adapter_v2` with `goal_repeat=10` had
`post_arrival_goals=8` in all three repeats and was `0/3` strict-valid; all
three failures occurred after arrival.

`fixed_s080` with `goal_repeat=10` also showed `post_arrival_goals=8` in all
three repeats and had one post-arrival failure. However, `fixed_s080` with
`goal_repeat=1` still had two pre-arrival failures. This means repeated-goal /
post-arrival stress is a real protocol factor, but it is not the only failure
mechanism in the benchmark.

## Protocol Interpretation

Future Stage 4 evaluation should be split into two protocols:

- single-goal mission protocol: `goal_repeat=1`
- repeated-goal / post-arrival replan stress protocol: `goal_repeat=10`

Existing Stage 4 repeated-goal results should be described as repeated-goal
strong-wind protocol results, not generic single-mission results. The
`goal_repeat=10` protocol should not be discarded; it is a meaningful stress
test. It should simply be labeled as such.

## Impact On `risk_adapter_v2`

Do not conclude that `risk_adapter_v2` is poor from the original `5/9`
screening alone. That screening used `goal_repeat=10` and was likely affected
by repeated-goal / post-arrival stress.

The follow-up `risk_adapter_v2` evaluation should use `goal_repeat=1` across
Trial 4/5/6 before threshold tuning. Stage 4-U2 has now completed that
single-goal expansion, so the next step is `risk_adapter_v2.1` design before
any further tuning or repeated-goal stress retest.

Stage 4-U completed the first such single-goal screening and found
`risk_adapter_v2` at `9/9` strict-valid versus `fixed_s080` at `6/9`.
Stage 4-U2 completed that 10-repeat expansion and found both methods at
`21/30` under `goal_repeat=1`. The next step is `risk_adapter_v2.1` design,
not direct threshold tuning from the earlier `goal_repeat=10` result.

This diagnostic also does not prove that `risk_adapter_v2` is better than
`fixed_s080` overall. It only shows that the previous `goal_repeat=10`
screening mixed method behavior with protocol stress.

## Impact On `fixed_s080`

`fixed_s080` remains a strong tuned static frontier under the existing
`goal_repeat=10` repeated-goal protocol. However, its single-goal mission
performance still needs separate evaluation.

In this Trial 4 diagnostic, `fixed_s080` under `goal_repeat=1` was only `1/3`
strict-valid. Therefore single-goal behavior is not automatically stronger
than repeated-goal behavior for every method and target.

## Research Decision

- Split future evaluation into single-goal mission protocol
  (`goal_repeat=1`) and repeated-goal stress protocol (`goal_repeat=10`).
- Use Stage 4-U2 as the current single-goal mission evidence before any
  `risk_adapter_v2` threshold change.
- Design `risk_adapter_v2.1` before further tuning or runs.
- Do not modify planner same-goal logic yet. Keep planner same-goal handling
  as a future system-level intervention after diagnostics.
- Label all future Stage 4 result tables with the goal protocol used.

## What Not To Claim

- Do not claim all previous invalid runs are due to the `goal_repeat` artifact.
- Do not claim `risk_adapter_v2` is better than `fixed_s080` overall from this
  three-run Trial 4 diagnostic.
- Do not claim `goal_repeat=10` is invalid as a stress test.
- Do not claim single-goal performance from `goal_repeat=10` results.
- Do not hide that previous Stage 4 results used the repeated-goal protocol.
