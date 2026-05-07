# Stage 3-C Strong-Wind Trial 2 Aggregate Comparison

## Executive Summary

Stage 3-C aggregate comparison is now available for strong-wind Trial 2. The formal setting is:

- Trial 2 target: `(-7.5, 1.5)`
- Strong wind annotation: `wind_force_norm = 0.007500`
- `target_xy_tolerance = 0.5`
- Formal validity uses target-error analyzer metrics.
- Invalid runs are kept and must not be hidden.

Original AutoTrans and `policy_mode=wind_level` scale `0.85` both achieved 3/5 valid runs. Fixed XML scale `0.85` achieved 2/5 valid runs.

There is no current evidence that `policy_mode=wind_level` scale `0.85` improves success rate over original AutoTrans. Fixed XML scale `0.85` should not be claimed as an improvement. The main achieved contribution at this stage is a repeated-trial evaluation framework and command-adaptation infrastructure.

## Method Groups

### A. Original AutoTrans

- Command adaptation disabled.
- No `heuristic_command_adapter`.
- Strong drag wind enabled.
- This is the baseline behavior for strong-wind Trial 2.

### B. Fixed XML Scale `0.85`

- Planner fixed speed/acceleration scale is set to `0.85`.
- No runtime `wind_level` policy.
- This tests whether simple fixed scaling improves strong-wind Trial 2 robustness.

### C. `policy_mode=wind_level` Scale `0.85`

- Independent `heuristic_command_adapter` is active.
- `policy_mode=wind_level` selects command scale from `wind_force_norm`.
- Strong wind maps to command scale `0.85`.
- `command_speed_scale` was `0.85` throughout the `wind_level` runs.

## Aggregate Table

| method | valid / total | invalid count | success rate | valid-only mean final_uav_xy_error | valid-only max final_uav_xy_error | notes |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| Original AutoTrans | 3 / 5 | 2 | 60% | 0.000000 | 0.000000 | Baseline is mixed: two invalid NaN runs and three exact valid target convergences. |
| Fixed XML scale `0.85` | 2 / 5 | 3 | 40% | 0.079465 | 0.158929 | Fixed scaling did not improve success rate in this 5-run set. |
| `policy_mode=wind_level` scale `0.85` | 3 / 5 | 2 | 60% | 0.144579 | 0.423067 | Matches original success rate, with command scale fixed at `0.85` throughout. |

## Per-Run Table

| method | repeat / log | valid | first_nan_time | final_uav_xy_error | note |
| --- | --- | --- | ---: | ---: | --- |
| Original AutoTrans | repeat1 | no | 34.899964 | 14.120674 | Invalid NaN run. |
| Original AutoTrans | repeat2 | no | 9.900357 | 219.374642 | Invalid early NaN run. |
| Original AutoTrans | repeat3 | yes | n/a | 0.000000 | Valid run. |
| Original AutoTrans | repeat4 | yes | n/a | 0.000000 | Valid run. |
| Original AutoTrans | repeat5 | yes | n/a | 0.000000 | Valid run. |
| Fixed XML scale `0.85` | repeat1 | no | 9.899995 | 140.293221 | Invalid early NaN run. |
| Fixed XML scale `0.85` | repeat2 | no | 36.099987 | 550.502019 | Invalid NaN run with very large final XY error. |
| Fixed XML scale `0.85` | repeat3 | yes | n/a | 0.158929 | Valid run. |
| Fixed XML scale `0.85` | repeat4 | no | 9.899806 | 238.164724 | Invalid early NaN run. |
| Fixed XML scale `0.85` | repeat5 | yes | n/a | 0.000000 | Valid run. |
| `policy_mode=wind_level` scale `0.85` | `autotrans_log_20260506_213036.csv` | yes | n/a | 0.000000 | Valid run. |
| `policy_mode=wind_level` scale `0.85` | `autotrans_log_20260506_215700.csv` | no | 9.899776 | 196.263063 | Invalid early NaN run. |
| `policy_mode=wind_level` scale `0.85` | `autotrans_log_20260506_220634.csv` | yes | n/a | 0.423067 | Valid run within `target_xy_tolerance`. |
| `policy_mode=wind_level` scale `0.85` | `autotrans_log_20260506_221504.csv` | yes | n/a | 0.010671 | Valid run with small final XY error. |
| `policy_mode=wind_level` scale `0.85` | `autotrans_log_20260507_101853.csv` | no | 9.849928 | n/a | Invalid early NaN run. |

## Interpretation

Trial 2 is a stochastic or initialization-sensitive stress case under strong wind. Single-run results are misleading because each method has both valid and invalid outcomes.

Invalid runs exist in original AutoTrans, fixed XML scale `0.85`, and `policy_mode=wind_level` scale `0.85`. In this 5-run set, `policy_mode=wind_level` scale `0.85` is not worse than original AutoTrans in success rate, but it is not better either. Fixed XML scale `0.85` has a lower success rate than original in this comparison.

Further algorithmic improvement is required before making strong method claims.

## Current Research Decision

Keep `policy_mode=wind_level` as an infrastructure/candidate baseline. Do not freeze it as the final proposed method, and do not continue tuning scale blindly.

The next algorithm step should consider one of the following:

- stronger planner-side robustness modification
- trajectory feasibility/safety checking
- adaptive replanning guard
- learned/RL high-level policy after the repeated-evaluation framework is stable

## What Not To Claim

- Do not claim `policy_mode=wind_level` improves success rate.
- Do not claim fixed `0.85` improves robustness.
- Do not hide invalid runs.
- Do not use best-run cherry-picking.
