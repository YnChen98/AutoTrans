# Stage 3-C Strong-Wind Trial 2 Existing-Log Audit

## Executive Summary

Stage 3-C should compare repeated Trial 2 success rate under strong wind rather than relying on single-run metrics. The target case is:

- Target: `(-7.5, 1.5)`
- `target_xy_tolerance: 0.5`
- Strong wind annotation: `wind_force_norm: 0.007500`

Existing evidence already shows mixed stability. Original AutoTrans has 1 valid run out of 3 known repeats. `policy_mode=wind_level` with scale `0.85` also has mixed evidence, with at least 3 valid runs out of 5 candidate logs. Fixed XML scale `0.85` is currently incomplete because the exact Trial 2 log set still needs confirmation.

The immediate Stage 3-C task is therefore log consolidation and equal-repeat success-rate comparison across the three methods.

## Existing Result Inventory

### A. Original AutoTrans

Configuration:

- `enable_command_adaptation=false`
- `adaptation_mode=none`
- no `heuristic_command_adapter`
- strong drag wind enabled

| log file | valid_run_suggested | has_nan_state | first_nan_time | max_uav_speed | max_payload_speed | final_uav_xy_error | note |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| `autotrans_log_20260507_104355.csv` | false | true | 34.899964 | 32.334157 | 32.349150 | 14.120674 | Invalid repeat with late NaN and large final target error. |
| `autotrans_log_20260507_104811.csv` | false | true | 9.900357 | 377.059532 | 375.944487 | 219.374642 | Invalid repeat with early NaN and severe speed growth. |
| `autotrans_log_20260507_105138.csv` | true | false | n/a | 2.438925 | 2.484804 | 0.000000 | Valid repeat with exact final XY target convergence. |

Known count: 1 valid / 3 total.

### B. `policy_mode=wind_level` Scale `0.85`

Configuration:

- `policy_mode=wind_level`
- command scale `0.85` throughout known valid runs
- planner topic mode with readiness gate enabled
- strong drag wind enabled

| log file | valid_run_suggested | has_nan_state | first_nan_time | final_uav_xy_error | command scale | note |
| --- | --- | --- | ---: | ---: | --- | --- |
| `autotrans_log_20260506_213036.csv` | true in earlier analysis | not listed | n/a | not listed | `0.85` throughout | Candidate valid log; should be re-analyzed with target args if needed. |
| `autotrans_log_20260506_215700.csv` | false | true | 9.899776 | 196.263063 | `0.85` throughout | Invalid run with early NaN and severe target divergence. |
| `autotrans_log_20260506_220634.csv` | true | false | n/a | 0.423067 | `0.85` throughout | Valid repeat, within `target_xy_tolerance: 0.5` but close to threshold. |
| `autotrans_log_20260506_221504.csv` | true | false | n/a | 0.010671 | `0.85` throughout | Valid repeat with very small final XY target error. |
| `autotrans_log_20260507_101853.csv` | false | true | 9.849928 | not listed | `0.85` throughout | Invalid candidate log with early NaN. |

Current count: at least 3 valid / 5 total, pending reanalysis of `autotrans_log_20260506_213036.csv` with target-error args.

### C. Fixed XML Scale `0.85`

Configuration:

- Fixed planner XML scale `0.85`
- strong drag wind enabled
- no runtime `wind_level` policy

| log file | valid_run_suggested | has_nan_state | final_uav_xy_error | note |
| --- | --- | --- | ---: | --- |
| exact log file not yet identified | likely one earlier valid Trial 2 result exists | unknown | unknown | Incomplete until the exact CSV/log association is confirmed from protocol docs or git history. |

Current count: incomplete.

## Current Count

| method | current known valid count | current total count | status |
| --- | ---: | ---: | --- |
| Original AutoTrans | 1 | 3 | Mixed baseline stability; needs 2 more repeats to reach 5. |
| `policy_mode=wind_level` scale `0.85` | at least 3 | 5 | Candidate log set exists; `autotrans_log_20260506_213036.csv` should be re-analyzed with target args if needed. |
| Fixed XML scale `0.85` | incomplete | incomplete | Needs exact log identification or new repeats. |

## Missing Data

- Original AutoTrans needs 2 more Trial 2 repeats to reach 5 total runs.
- Fixed XML scale `0.85` needs enough confirmed Trial 2 repeats to reach 5 total runs.
- `policy_mode=wind_level` scale `0.85` may already have 5 candidate logs, but `autotrans_log_20260506_213036.csv` should be re-analyzed with target args before final aggregation.

## Next Recommended Experiment Plan

1. Do not run more `policy_mode=wind_level` scale `0.85` until existing logs are consolidated.
2. Run original AutoTrans Trial 2 two more times under the same strong-wind setting.
3. Run fixed XML scale `0.85` Trial 2 until 5 total confirmed runs are available.
4. Produce an aggregate comparison table with equal-repeat success rate, NaN count, final target error, swing statistics, and speed statistics.

## What Not To Do

- Do not hide invalid runs.
- Do not compare one method's best run against another method's worst run.
- Do not tune `strong_scale` again until baseline, fixed XML scale `0.85`, and `policy_mode=wind_level` scale `0.85` success rates are tabulated.
