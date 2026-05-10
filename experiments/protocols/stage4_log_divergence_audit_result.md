# Stage 4 Log Divergence Audit Result

## Executive Summary

The Stage 4 divergence audit found `command_saturation_before_nan` as the
dominant detected failure-mode guess. Teleport-like position jumps are also
frequent.

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
logs. Therefore `rows_inspected=175` should not be treated as the final
balanced evaluation sample.

Generated output under `experiments/results/` should remain uncommitted.

## Result Table

| Failure-mode guess | Count |
| --- | ---: |
| rows inspected | `175` |
| `command_nan_before_state_divergence` | `1` |
| `command_saturation_before_nan` | `114` |
| `teleport_like_position_jump` | `54` |
| `unknown_invalid` | `6` |

## Motivating Example: original Trial 6 repeat10

The motivating log is:

```bash
experiments/logs/autotrans_log_20260510_190453.csv
```

Detailed inspection showed this timing sequence:

| Event | Relative time |
| --- | ---: |
| Saturated SO3 commands: `so3_thrust=60.0`, `so3_bodyrate_x=-3.0`, `so3_bodyrate_y=3.0`, `so3_bodyrate_z=1.2` | `14.900` |
| `so3_thrust` / bodyrate NaN | `14.950` |
| UAV speed `> 4` | `15.250` |
| payload speed `> 4` | `15.350` |
| UAV position jump `> 1 m` | `15.849` |

In this run, command NaN appears before state divergence. The CSV currently
lacks reference, desired-state, or full trajectory columns beyond
`has_trajectory`, so planner reference discontinuity cannot be proven from
this log alone.

## Interpretation

`command_saturation_before_nan` means SO3 thrust or bodyrate saturation often
appears before NaN or state divergence.

`teleport_like_position_jump` means the logged state has an abrupt position
jump after apparently stable flight.

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

## Failure-Mode Label Taxonomy

Use the following proposed labels when annotating invalid runs:

- `target_error_only`
- `strict_safety_no_nan`
- `command_saturation_before_nan`
- `command_nan_before_state_divergence`
- `teleport_like_position_jump`
- `manual_collision_observed`
- `manual_path_infeasible`
- `unknown_invalid`

## Paper-Facing Caveat

Main success-rate results must be paired with failure-mode classification.
NaN/divergence failures should be counted as invalid, but root-cause wording
must remain cautious.

Do not claim all NaN failures are control-policy failures. Do not claim all
`risk_adapter_v1` failures are model false negatives.

## Next Step

Add manual annotations for `collision_observed`, `path_infeasible`, and
`teleport_like_divergence` to final comparison manifests.

Add desired/reference trajectory logging before root-cause tests. Then run
small root-cause isolation tests:

- repeated goal disabled / `goal_repeat=1`
- open map / no obstacle if supported
- same target with desired/reference logging
- command NaN guard diagnostic later if needed

## What Not To Claim

- Do not claim statistical significance from this 175-row diagnostic scan.
- Do not use this scan as the main evaluation table.
- Do not hide mixed failure mechanisms.
- Do not claim root cause is proven without desired/reference trajectory
  logging.
