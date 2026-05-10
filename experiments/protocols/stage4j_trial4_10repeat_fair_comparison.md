# Stage 4-J Trial 4 10-Repeat Fair Comparison

## Executive Summary

Trial 4 10-repeat fair comparison is complete for `original`, `fixed_s085`,
`windlevel_s085`, and `risk_adapter_v1`.

`fixed_s085` is strongest on Trial 4 with `9/10` valid runs. `original`
achieved `8/10`, `risk_adapter_v1` achieved `7/10`, and `windlevel_s085`
achieved `4/10`.

`risk_adapter_v1` is not the best method on Trial 4. Trial 4 remains a weak
target for `risk_adapter_v1`.

Manual visual observation suggests that some invalid runs may involve obstacle
collision or path-feasibility failure, not only command-adaptation or
risk-prediction failure.

## Trial 4 Method Comparison Table

| Method | Valid runs | Invalid runs | Success rate | Invalid repeat summary |
| --- | ---: | ---: | ---: | --- |
| `original` | `8/10` | `2/10` | `0.800` | repeat4 and repeat6 were target-error failures without NaN. |
| `fixed_s085` | `9/10` | `1/10` | `0.900` | repeat9 was a NaN failure. |
| `windlevel_s085` | `4/10` | `6/10` | `0.400` | repeat1, repeat3, repeat4, repeat5, and repeat6 were NaN failures; repeat9 was a target-error/high-swing case. |
| `risk_adapter_v1` | `7/10` | `3/10` | `0.700` | repeat5 and repeat9 were late-risk NaN/safety failures; repeat7 was a target-error failure. |

## Failure Mode Analysis

`original` failures are target-error failures. repeat4 ended with
`final_uav_xy_error=1.288450` and no NaN. repeat6 ended with
`final_uav_xy_error=1.041486` and no NaN.

`fixed_s085` had one NaN failure. repeat9 had
`first_nan_time=14.800033`, `max_payload_speed=31.732132`, and
`final_uav_xy_error=12.589311`.

`windlevel_s085` had many NaN failures. repeat1 failed at
`first_nan_time=5.599925`, repeat3 at `41.749953`, repeat4 at `9.494192`,
repeat5 at `25.676854`, and repeat6 at `15.099965`. repeat9 had no NaN, but
ended as a target-error/high-swing case with `final_uav_xy_error=6.831146` and
`max_swing_angle_deg=37.770761`.

`risk_adapter_v1` had two late-risk NaN/safety failures and one target-error
failure. repeat5 failed at `first_nan_time=24.900021`, with risk trigger too
late. repeat9 failed at `first_nan_time=14.649950`, also with risk trigger too
late. repeat7 had no NaN or safety violation, but ended with
`final_uav_xy_error=0.711352`.

### Manual Obstacle-Collision Observations

During several invalid runs, the UAV visually appeared to collide with an
obstacle and then suddenly teleport or fly upward at very large speed. In at
least one case, the planned path appeared to pass directly through an obstacle;
the UAV then contacted the obstacle along the path and stopped or destabilized.

These observations mean that some Trial 4 invalid cases may be
obstacle-collision or path-feasibility failures, not purely
command-adaptation or risk-prediction failures. This distinction is important:
if the planner produces a path that intersects an obstacle, high-level command
adaptation alone should not be expected to solve the underlying path
feasibility problem.

## Interpretation Caveat

Trial 4 invalids mix several mechanisms:

- command adaptation / risk-detection limitations
- target-error failures
- NaN or simulator divergence
- visually observed obstacle-collision-related failures
- possible path-infeasibility failures

Therefore Trial 4 should not be used alone to claim `risk_adapter_v1`
superiority or failure.

## Comparison With Existing Trial 4 Baselines

| Method | Trial 4 10-repeat result | Notes |
| --- | ---: | --- |
| `original` | `8/10` | Fair 10-repeat expansion. |
| `fixed_s085` | `9/10` | Fair 10-repeat expansion; best Trial 4 method. |
| `windlevel_s085` | `4/10` | Fair 10-repeat expansion. |
| `risk_adapter_v1` | `7/10` | Fair 10-repeat expansion; weaker than `fixed_s085` and `original` on Trial 4. |

This 10-repeat comparison is more fair than the previous 5-repeat comparison.
It also changes the Trial 4 interpretation: `risk_adapter_v1` remains better
than `windlevel_s085`, but it does not beat `fixed_s085` or `original` on this
target.

## Updated Aggregate Interpretation

With current available repeats, using Trial 4 as 10 repeats and Trial 5/6 as 5
repeats, the weighted aggregate is:

| Method | Current weighted aggregate |
| --- | ---: |
| `original` | `13/20` |
| `fixed_s085` | `13/20` |
| `windlevel_s085` | `9/20` |
| `risk_adapter_v1` | `16/20` |

`risk_adapter_v1` remains strongest in the current weighted aggregate at
`16/20`. This aggregate is not final because Trial 4 now has 10 repeats while
Trial 5 and Trial 6 still have 5 repeats.

## Research Decision

Do not claim `risk_adapter_v1` is stable on Trial 4.

Do not proceed directly to `risk_adapter_v2` based only on Trial 4. Trial 4
contains a mixture of command-adaptation limitations, target-error failures,
NaN/divergence, and visually observed obstacle-collision/path-feasibility
issues.

The next recommended step is to expand Trial 5 and Trial 6 to 10 repeats for
the same methods, or add collision/path-feasibility annotations before using
Trial 4 for strong claims.

Future analysis should consider a manual collision/path-feasibility label.

## What Not To Claim

- Do not claim statistical significance.
- Do not claim a safety guarantee.
- Do not claim `risk_adapter_v1` beats `fixed_s085` on Trial 4.
- Do not hide `risk_adapter_v1` repeat5, repeat7, or repeat9 failures.
- Do not treat obstacle-collision/path-infeasibility cases as purely
  risk-adapter failures.
