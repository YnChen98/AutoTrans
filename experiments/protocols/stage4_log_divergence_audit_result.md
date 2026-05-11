# Stage 4 Log Divergence Audit Result

## Executive Summary

The Stage 4 divergence audit now separates transient command saturation from
invalid divergence. With the corrected classifier, the dominant diagnostic
label is `command_saturation_without_divergence`, while
`command_saturation_before_nan` remains the dominant detected invalid
divergence precursor.

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
logs. Therefore `rows_inspected=177` should not be treated as the final
balanced evaluation sample.

Generated output under `experiments/results/` should remain uncommitted.

## Result Table

| Failure-mode guess | Count |
| --- | ---: |
| rows inspected | `177` |
| `command_saturation_before_nan` | `57` |
| `command_saturation_without_divergence` | `90` |
| `no_divergence_detected` | `7` |
| `strict_safety_no_nan` | `17` |
| `target_error_only` | `6` |

This table uses the corrected classifier. Earlier diagnostic wording did not
separate transient command saturation from saturation followed by
NaN/divergence.

## Correction Note

The previous audit over-counted `command_saturation_before_nan` because the
classifier did not distinguish transient command saturation without later
NaN/nonfinite state, high-speed divergence, position jump, or swing threshold
crossing. The corrected audit shows that command saturation can occur without
failure and should be treated as a diagnostic signal, not automatically as an
invalid divergence.

The inspector has also been updated to scan only numeric state, SO3 command,
and reference fields for nonfinite detection. String diagnostic columns such
as `command_invalid_reason` and `command_saturation_reason` are excluded from
`first_nonfinite_column`.

For logs with reference columns, the inspector now distinguishes late
reference jumps from root-cause reference jumps. A reference jump observed
after command NaN or after state divergence is marked with
`reference_jump_after_divergence=true` and should not be interpreted as
`reference_jump_before_command_nan`.

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

Stage 4 reference logging is the next diagnostic step after this audit. New
logs should record the detected controller reference topic as `ref_*` columns
so reference position jumps, velocity jumps, or acceleration spikes can be
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
before NaN/nonfinite state or later high-speed/position-jump divergence.

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

Two root-cause diagnostic smoke checks were run after reference logging was
added:

| Smoke check | Validity | Reference discontinuity | Corrected classification |
| --- | --- | --- | --- |
| `goal_repeat=1` | `valid_run_suggested=true`, `has_nan_state=false` | none detected | `command_saturation_without_divergence` |
| `goal_repeat=10` | `valid_run_suggested=true`, `has_nan_state=false` | none detected | `no_divergence_detected` |

These smoke checks did not reproduce sudden fly-away. Therefore repeated goal
publishing or replanning discontinuity remains a possible factor, but it is
not proven by these two runs.

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

Add desired/reference trajectory logging before root-cause tests. This logging
should capture controller reference fields in the CSV and let the analyzer
report reference jumps, reference acceleration spikes when available, and
UAV-reference tracking error. Then run small root-cause isolation tests:

- repeated goal disabled / `goal_repeat=1`
- open map / no obstacle if supported
- same target with desired/reference logging
- command NaN guard diagnostic later if needed

Future root-cause tests should use reference logging and multiple repeats
before assigning a mechanism to repeated goal publishing, replanning
discontinuity, collision/contact interaction, or controller/simulator
instability.

## What Not To Claim

- Do not claim statistical significance from this 177-row diagnostic scan.
- Do not use this scan as the main evaluation table.
- Do not hide mixed failure mechanisms.
- Do not claim root cause is proven without desired/reference trajectory
  logging.
- Do not treat transient command saturation alone as proof of invalid
  divergence.
