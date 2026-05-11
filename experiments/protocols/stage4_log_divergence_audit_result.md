# Stage 4 Log Divergence Audit Result

## Executive Summary

The Stage 4 divergence audit now separates transient command saturation,
command NaN timing, state divergence timing, and late reference jumps. With the
latest corrected classifier, the dominant diagnostic label is
`command_saturation_without_divergence`, while
`command_saturation_before_nan` remains a major real divergence class.

The audit also now finds a significant `state_divergence_before_command_nan`
category. This means an active command NaN guard remains useful for diagnosis,
but it cannot explain or fix every invalid failure mode.

Invalid runs should be separated by failure mode before strong claims are
made. This audit is diagnostic evidence for failure classification and
debugging, not the main paper success-rate table.

## Audit Command and Scope

The audit was run with:

```bash
python3 experiments/scripts/inspect_stage4_log_divergence.py \
  --metrics-glob "experiments/figures/*_metrics_summary.txt" \
  --output-csv experiments/results/stage4_log_divergence_report.csv \
  --print-summary
```

The glob includes historical, smoke, debug, resetcheck, and old experiment
logs. Therefore `rows_inspected=184` should not be treated as the final
balanced evaluation sample.

Generated output under `experiments/results/` should remain uncommitted.

## Result Table

| Failure-mode guess | Count |
| --- | ---: |
| rows inspected | `184` |
| `command_nan_before_state_divergence` | `1` |
| `command_saturation_before_nan` | `35` |
| `command_saturation_without_divergence` | `94` |
| `no_divergence_detected` | `7` |
| `state_divergence_before_command_nan` | `20` |
| `strict_safety_no_nan` | `21` |
| `target_error_only` | `6` |

This table uses the latest timing-aware classifier. Earlier diagnostic wording
did not separate transient command saturation from saturation followed by
NaN/divergence, and it did not separate state divergence before command NaN
from command NaN before state divergence.

## Correction Note

Earlier audits overemphasized `command_saturation_before_nan` because the
classifier did not fully separate transient command saturation without later
NaN/nonfinite state, high-speed divergence, position jump, or swing threshold
crossing. It also did not yet distinguish cases where state divergence appears
before command NaN. The latest audit shows that command saturation is common
and should be treated as a diagnostic signal, not automatically as an invalid
divergence.

The inspector has also been updated to scan only numeric state, SO3 command,
and reference fields for nonfinite detection. String diagnostic columns such
as `command_invalid_reason` and `command_saturation_reason` are excluded from
`first_nonfinite_column`.

For logs with reference columns, the inspector now distinguishes late
reference jumps from root-cause reference jumps. A reference jump observed
after command NaN or after state divergence is marked with
`reference_jump_after_divergence=true` and should not be interpreted as
`reference_jump_before_command_nan`.

The `state_divergence_before_command_nan` category is now significant in the
batch scan. This limits the expected scope of a future active command NaN
guard: the guard can test whether command NaN propagation pollutes simulator
state, but it should not be presented as a complete fix for all Stage 4
invalids.

## Motivating Example: original Trial 6 repeat10

The motivating log is:

```bash
experiments/logs/autotrans_log_20260510_190453.csv
```

Detailed inspection showed this timing sequence:

| Event | Relative time |
| --- | ---: |
| Saturated SO3 commands: `so3_thrust=60.0`, `so3_bodyrate_x=-3.0`, `so3_bodyrate_y=3.0`, `so3_bodyrate_z=1.2` | `14.900053` |
| `so3_thrust` / bodyrate NaN | `14.950161` |
| UAV speed `> 4` and swing `> 30 deg` | `15.250058` |
| swing `> 60 deg` | `15.299990` |
| payload speed `> 4` | `15.350023` |
| UAV position jump `> 1 m` | `15.849978` |

In this run, command NaN appears before state divergence. The CSV currently
lacks reference, desired-state, or full trajectory columns beyond
`has_trajectory`, so planner reference discontinuity cannot be proven from
this log alone.

The corrected `failure_mode_guess` for this run remains
`command_saturation_before_nan`, so original Trial 6 repeat10 remains a true
divergence example.

## Timing-Fix Example: late reference jump after divergence

The Stage 4-N3 smoke log below exercised the latest timing fix:

```bash
experiments/logs/autotrans_log_20260511_131044.csv
```

The corrected inspector reports:

| Field | Value |
| --- | ---: |
| `failure_mode_guess` | `command_saturation_before_nan` |
| `first_command_nan_time` | `6.004893` |
| `first_state_divergence_time` | `6.004893` |
| `first_reference_jump_time` | `8.004397` |
| `reference_jump_after_divergence` | `true` |

This confirms that the reference jump was late relative to the command NaN and
state divergence timing. It should not be treated as the initial planner
reference root cause. The better interpretation is command saturation followed
by command NaN and near-simultaneous state divergence.

Stage 4 reference logging remains required for root-cause tests. New logs
should record the detected controller reference topic as `ref_*` columns so
reference position jumps, velocity jumps, or acceleration spikes can be
compared against SO3 command saturation and NaN timing. In the current
`simple_run.launch` flow, the default source is
`/mpc_controller_node/mpc/all_ref_data`; `/position_cmd` remains supported for
launch flows that publish `quadrotor_msgs/PositionCommand`.

## Interpretation

`command_saturation_without_divergence` means SO3 thrust or bodyrate saturation
appeared, but the CSV did not show NaN/nonfinite state, high-speed divergence,
position jump, or swing threshold crossing. It is a diagnostic signal, not an
invalid divergence label by itself.

`command_saturation_before_nan` means SO3 thrust or bodyrate saturation appears
before command NaN and before or near state divergence. It remains a major
real divergence class.

`state_divergence_before_command_nan` means speed, swing, or position-jump
divergence appears before any logged SO3 command NaN. These cases need
separate investigation because an active command NaN guard may not prevent
them.

These are invalid safety failures, but they should not automatically be
assigned to `risk_adapter_v1` or any single command-adaptation method.
Possible root causes include reference discontinuity, path infeasibility,
obstacle/contact interaction, simulator numerical instability, controller
saturation, and missing NaN guards.

Several invalid runs were also observed manually as sudden high-speed fly-away
or teleport-like divergence after apparently stable flight. Some invalid runs
appeared associated with obstacle contact or a planned path passing through an
obstacle. These observations reinforce that Stage 4 invalids can mix simulator
or contact instability, path feasibility, and command adaptation effects.

## Root-Cause Smoke Checks

Root-cause smoke checks after reference logging showed that both
`goal_repeat=1` and `goal_repeat=10` can produce
`command_saturation_without_divergence`, and both settings have reproduced
`command_saturation_before_nan` in limited repeats. Therefore repeated goal
publishing or replanning remains possible, but it is no longer the primary
supported explanation.

The failed reference-logging smoke runs did not show `ref_pos` or `ref_vel`
nonfinite values or jumps before failure. However, `ref_acc` remains
unavailable or NaN in the `nav_msgs/Path` reference source, so acceleration
reference discontinuity is not fully ruled out.

## Failure-Mode Label Taxonomy

Use the following proposed labels when annotating invalid runs:

- `target_error_only`
- `strict_safety_no_nan`
- `command_saturation_before_nan`
- `command_saturation_without_divergence`
- `command_nan_before_state_divergence`
- `command_nan_coincident_with_state_divergence`
- `state_divergence_before_command_nan`
- `reference_jump_before_command_nan`
- `reference_jump_after_divergence`
- `no_divergence_detected`
- `unknown_invalid`

## Paper-Facing Caveat

Main success-rate results must be paired with failure-mode classification.
NaN/divergence failures should be counted as invalid, but root-cause wording
must remain cautious.

Do not claim all NaN failures are control-policy failures. Do not claim all
`risk_adapter_v1` failures are model false negatives.

Main paper results should use strict-valid / `label_strict_invalid` and should
also report failure-mode labels or distributions for invalid runs.

## Next Step

Add manual annotations for `collision_observed`, `path_infeasible`, and
`teleport_like_divergence` to final comparison manifests.

Use desired/reference trajectory logging for root-cause tests. This logging
should capture controller reference fields in the CSV and let the analyzer
report reference jumps, reference acceleration spikes when available, and
UAV-reference tracking error. Then run small root-cause isolation tests:

- repeated goal disabled / `goal_repeat=1`
- open map / no obstacle if supported
- same target with desired/reference logging
- command NaN guard diagnostic for command-NaN propagation cases

Future root-cause tests should use reference logging and multiple repeats
before assigning a mechanism to repeated goal publishing, replanning
discontinuity, collision/contact interaction, or controller/simulator
instability.

## What Not To Claim

- Do not claim statistical significance from this 184-row diagnostic scan.
- Do not use this scan as the main evaluation table.
- Do not hide mixed failure mechanisms.
- Do not claim root cause is proven without desired/reference trajectory
  logging.
- Do not treat transient command saturation alone as proof of invalid
  divergence.
- Do not claim an active command NaN guard can solve
  `state_divergence_before_command_nan` failures.
