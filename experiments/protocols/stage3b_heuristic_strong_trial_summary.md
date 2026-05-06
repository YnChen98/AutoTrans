# Stage 3-B Heuristic Command Adapter Strong-Wind Trial Summary

## Executive Summary

Stage 3-B heuristic command adaptation has been implemented and initially validated under the strong drag-wind benchmark. The implementation uses an independent `heuristic_command_adapter` node that publishes runtime command scale topics consumed by the planner.

Current strong-wind evidence is promising but not fully stable:

- Trial 1 and Trial 2 are valid.
- Trial 3 had one invalid first run and one valid diagnostic repeat.
- The diagnostic repeat shows command scale logging works and captures risk-driven scale changes.
- More repeated trials and policy tuning are required before claiming this as the final proposed method.

## Method Snapshot

- Adapter node: `heuristic_command_adapter`
- Published topics:
  - `/command_adaptation/speed_scale`
  - `/command_adaptation/acceleration_scale`
- Planner mode:
  - `manager/enable_command_adaptation=true`
  - `manager/adaptation_mode=topic`
  - `manager/require_adaptation_topic_ready=true`
- Readiness gate: planner waits for scale topics before accepting `/move_base_simple/goal`.
- Simulator and controller remain unchanged.
- Logger records `command_speed_scale` and `command_acceleration_scale` for diagnosis.

Wind setting:

- wind level: strong
- `wind_velocity_x: 0.5`
- `wind_drag_linear: 0.015`
- `wind_max_force: 0.0075`
- `/wind_force` annotation norm: `0.007500`

## Trial Result Table

| Trial | Target | Valid | max_swing_angle_deg | p95_swing_angle_deg | max_uav_speed | max_payload_speed | final_uav_position | min_command_speed_scale | final_command_speed_scale | Interpretation |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- | ---: | ---: | --- |
| Trial 1 heuristic strong | `(0.0, -1.2)` | yes | 25.634289 | 11.646383 | 2.500851 | 2.617090 | `(0.000000, -1.200000, 1.468415)` | n/a | n/a | Valid strong-wind run with bounded swing and speed. |
| Trial 2 heuristic strong | `(-7.5, 1.5)` | yes | 25.501973 | 2.752511 | 2.522940 | 2.992567 | `(-7.499571, 1.501333, 1.468414)` | n/a | n/a | Valid strong-wind run; supports Trial 2 robustness in topic mode. |
| Trial 3 heuristic strong first run | `(8.0, 1.5)` | no | 173.617270 | 72.372001 | 14.654524 | 14.224621 | `(8.340385, -2.603849, -8.522439)` | observed `0.500000` | n/a | Invalid run; severe swing/speed growth and altitude failure. Scale was observed to drop to critical override. |
| Trial 3 heuristic strong diagnostic repeat | `(8.0, 1.5)` | yes | 25.862195 | 8.309135 | 2.550599 | 3.256075 | `(8.000000, 1.500000, 1.468415)` | 0.650000 | 0.850000 | Valid repeat; scale logging shows temporary warning-level override and recovery to strong-wind base scale. |

## Scale Behavior Interpretation

The strong-wind base scale is `0.85`. In nominal strong-wind behavior, both `command_speed_scale` and `command_acceleration_scale` should remain near `0.85` unless the heuristic risk overrides activate.

The Trial 3 diagnostic repeat reached a minimum `command_speed_scale` of `0.65` and recovered to a final scale of `0.85`. This is consistent with a warning-level override from either `speed_warn` or `swing_warn_deg`.

The first Trial 3 run was observed to reach `0.5`, which is consistent with a critical override from either `speed_critical` or `swing_critical_deg`. This drop is expected heuristic policy behavior and is not evidence of a topic-mode planner bug.

However, the invalid first Trial 3 run suggests that the policy can still react too late, react too aggressively, or interact poorly with an already unstable trajectory. The current heuristic should therefore be treated as a first risk-aware adapter, not as a frozen final method.

## Current Conclusion

- The heuristic adapter interface works.
- Planner runtime topic mode and readiness gate work with the independent adapter.
- Command scale logging and analysis work.
- Strong wind now has valid evidence on Trial 1, Trial 2, and Trial 3 diagnostic repeat.
- Trial 3 inconsistency means Stage 3-B should not yet be frozen as the final proposed method.

## Next Recommended Experiments

1. Repeat heuristic strong Trial 1, Trial 2, and Trial 3 at least once more.
2. Compare heuristic results against:
   - original strong-wind baseline without command adaptation
   - fixed `speed_scale=0.85` and `acceleration_scale=0.85`
   - topic-mode fixed publisher `0.85`
3. Inspect `command_speed_scale.png` and `command_acceleration_scale.png` whenever a run is invalid.
4. Correlate scale drops with `swing_angle_deg`, UAV speed, and payload speed.
5. Consider policy tuning only after repeated evidence confirms the failure pattern.

## What Not To Claim Yet

- Do not claim the heuristic adapter is strictly better than baseline.
- Do not claim strong wind is fully solved.
- Do not claim any RL result.
- Do not tune boundary wind before strong-wind repeats are stable.
