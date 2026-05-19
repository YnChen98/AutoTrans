# Stage 4-AU Risk Score And Strict-Valid Metric Documentation

## Executive Summary

Stage 4-AU documents risk score usage and the strict-valid metric for the RA-L
Paper 1 track. It is a documentation and manuscript-readiness step, not a new
experiment, not a new algorithm implementation, and not a template conversion.

Paper 1 remains centered on `risk_adapter_v1` as the balanced learned /
risk-conditioned execution governor. This document does not claim formal
safety, statistical significance, or real-world deployment robustness. It also
does not introduce `risk_adapter_v22`.

## Inspected Sources

Implementation and documentation inspected for this audit:

- `experiments/command_adaptation/scripts/risk_conditioned_command_adapter.py`
- `experiments/command_adaptation/launch/risk_conditioned_command_adapter.launch`
- `experiments/command_adaptation/README.md`
- `experiments/autotrans_logger/scripts/state_logger.py`
- `experiments/autotrans_logger/scripts/analyze_log.py`
- `experiments/scripts/inspect_stage4_log_divergence.py`
- `experiments/scripts/generate_stage4_protocol_split_paper_assets.py`
- `experiments/scripts/generate_stage4_failure_mode_paper_assets.py`
- `experiments/scripts/build_stage4_risk_dataset.py`
- `experiments/protocols/stage4_risk_model_export_protocol.md`
- Stage 4-Z / AA / AC / AH / AI documentation as needed for metric and
  failure-label boundaries.

## Risk Score Source / Interface

The online adapter implementation publishes risk scores as ROS diagnostics:

- `/command_adaptation/risk_score_3s`
- `/command_adaptation/risk_score_5s`

`state_logger.py` records these topics into CSV columns:

- `command_risk_score_3s`
- `command_risk_score_5s`

The adapter also publishes and logs related scale diagnostics:

- `/command_adaptation/risk_scale_selected`
- `/command_adaptation/risk_target_scale_raw`
- `command_risk_scale_selected`
- `command_risk_target_scale_raw`

The `risk_conditioned_command_adapter.py` node loads JSON
`LogisticRegression` models through:

- `model_json_3s`
- `model_json_5s`
- optional `model_json_15s`

The launch defaults point to generated model files:

- `experiments/models/stage4_risk_logreg_3s.json`
- `experiments/models/stage4_risk_logreg_5s.json`
- `experiments/models/stage4_risk_logreg_15s.json`

Generated model files under `experiments/models/` are ignored and were not
inspected as committed artifacts in this task. The documented export protocol
uses `experiments/scripts/train_stage4_risk_predictor.py` with
`label_strict_invalid`, `feature-set early`, `--drop-command-scale-features`,
`--drop-method-features`, and `--export-train-on-all`.

The online node subscribes to:

- `/visual_slam/odom`
- `/payload_odom`
- `/wind_force`
- `/move_base_simple/goal`
- `/planning/trajectory`

The verified `risk_adapter_v1` risk feature row uses the active goal, wind
force norm, and early episode windows of UAV speed, payload speed, swing angle,
wind norm, target-distance endpoint, and target progress. For a 3 s model, the
row uses the 3 s early window. For a 5 s model, it uses the 3 s and 5 s early
windows. The code also supports 10 s and 15 s early windows for other exported
models.

Unavailable risk is represented by `-1.0` in the adapter state and published
diagnostics. `analyze_log.py` treats finite non-negative risk scores as valid
for summary statistics, so `-1.0` is excluded from risk-score mean, max, final,
and first-finite calculations.

The adapter `publish_rate` defaults to `5.0 Hz`. The code publishes risk and
scale diagnostics from the same timer. Inference latency is not measured in the
inspected implementation.

Metrics summaries may include:

- `mean_command_risk_score_3s`
- `max_command_risk_score_3s`
- `final_command_risk_score_3s`
- `first_finite_command_risk_score_3s_time`
- `first_command_risk_score_3s_ge_0p5_time`
- `mean_command_risk_score_5s`
- `max_command_risk_score_5s`
- `final_command_risk_score_5s`
- `first_finite_command_risk_score_5s_time`
- `first_command_risk_score_5s_ge_0p5_time`
- `first_command_risk_score_5s_ge_0p7_time`

Remaining TODOs before RA-L submission:

- TODO: record the exact final risk model source artifact used for Paper 1.
- TODO: record exact final training dataset version, row count, and class
  counts from the exported JSON metadata.
- TODO: record the exact exported `feature_names` schema for the Paper 1 3 s
  and 5 s models.
- TODO: define the horizon semantics in manuscript language, including whether
  the model score is a warning score for strict-invalid risk rather than a
  calibrated physical probability.
- TODO: document the calibration method or explicitly state that no deployed
  calibration transform is used.
- TODO: document confidence / OOD behavior; no confidence or OOD rejection
  mechanism was found in the inspected adapter.
- TODO: measure or bound inference latency if the RA-L paper makes any timing
  claim beyond the configured `5.0 Hz` publish rate.

## `risk_adapter_v1` Policy Logic

`risk_adapter_v1` is implemented as the `risk_conditioned` policy mode. It
uses the following Paper 1 settings from the current Stage 4 documentation:

- `risk_threshold_3s=0.5`
- `risk_threshold_5s=0.5`
- `hard_threshold_5s=0.7`
- `soft_scale_3s=0.75`
- `soft_scale_5s=0.65`
- `hard_scale_5s=0.60`
- `scale_rate_limit_per_sec=0.5`

The launch file defaults for the soft scales are not the complete Paper 1 run
configuration, so the final manuscript should cite the experiment settings
used for the Paper 1 results rather than only the launch defaults.

Verified policy behavior:

- If risk conditioning is disabled, the model is unavailable, no active goal
  exists, or the episode has insufficient history, the adapter publishes
  unavailable risk scores and falls back to the wind-level/base scale.
- Before 3 s of episode history, both risk scores are unavailable.
- At 3 s and later, a finite `risk_score_3s` can reduce the selected scale to
  `soft_scale_3s` when it is at least `risk_threshold_3s`.
- Before 5 s of episode history, `risk_score_5s` remains unavailable.
- At 5 s and later, a finite `risk_score_5s` can reduce the selected scale to
  `soft_scale_5s` when it is at least `risk_threshold_5s`.
- If `risk_score_5s` is at least `hard_threshold_5s`, the selected scale can be
  reduced further to `hard_scale_5s`.
- The same selected scale is published to `speed_scale` and
  `acceleration_scale`.
- Rate limiting bounds the change in scale using
  `scale_rate_limit_per_sec`.

In low-risk or unavailable-risk conditions, `risk_adapter_v1` behaves close to
the base wind-level scale. In medium/high-risk conditions, it reduces execution
aggressiveness using the risk thresholds above. This differs from
`fixed_s080` / `fixed_s085`, which apply static scales, and from
`windlevel_s085`, which selects scales from wind magnitude rather than learned
short-horizon risk scores.

Claim boundary: `risk_adapter_v1` is an empirical execution governor. It is not
a certified safety filter and does not provide formal safety, stability, or
real-world deployment guarantees.

## Strict-Valid Metric Definition

The raw analyzer field `valid_run_suggested` is not the final paper-facing
success metric. It is a broad analyzer heuristic from
`experiments/autotrans_logger/scripts/analyze_log.py`. It rejects runs with
NaN state, final-row NaN state, missing final UAV/payload position,
unreasonable final altitude, broad speed or swing excursions, or target XY
failure when target arguments are provided.

The paper-facing strict-valid metric is implementation-derived from the Stage 4
paper-asset generators, including
`experiments/scripts/generate_stage4_protocol_split_paper_assets.py` and
`experiments/scripts/generate_stage4_failure_mode_paper_assets.py`.

A run is strict-valid only when all of the following hold:

- `valid_run_suggested=true`
- `has_nan_state=false`
- `max_swing_angle_deg` is finite and `< 60.0`
- `max_uav_speed` is finite and `< 4.0`
- `max_payload_speed` is finite and `< 4.0`
- `final_uav_xy_error` is finite and `<= 0.5`

Implementation-derived details:

- `valid_run_suggested` uses broader analyzer thresholds:
  `MAX_REASONABLE_SPEED_MPS=10.0` and `MAX_REASONABLE_SWING_DEG=90.0`.
- The strict-valid speed threshold is `< 4.0 m/s` for both UAV and payload.
- The strict-valid swing threshold is `< 60.0 deg`.
- The strict-valid final target threshold is `final_uav_xy_error <= 0.5 m`.
- `target_xy_tolerance` defaults to `0.5` in `analyze_log.py` and is passed by
  Stage 4 run helpers for paper-facing metrics.
- Arrival diagnostics use UAV/payload XY tolerance, speed below `0.5 m/s`, and
  sustained arrival for `0.5 s`; arrival timing is diagnostic unless a
  paper-asset script explicitly maps no-arrival evidence into a failure group.

Warning and diagnostic boundaries:

- Command saturation diagnostics are not strict-invalid by themselves.
- `command_saturation_without_divergence` is warning-style diagnostic behavior,
  not an automatic paper failure.
- `swing_angle_deg >= 30` is a warning threshold, not the strict-invalid
  threshold.
- Position jump and reference jump diagnostics are warning or failure-mode
  evidence, not direct replacements for strict-valid.
- `label_strict_invalid` in dataset-building documentation combines
  analyzer-invalid, target, speed, swing, and manual-invalid labels for risk
  learning. The paper-facing strict-valid generators use the metric-summary
  conditions above for completed Paper 1 result tables.

## Failure Group Boundary

Strict-valid count is the paper-facing success metric.

`failure_mode_guess` and `failure_group` are diagnostic labels. They are useful
for failure-aware analysis, invalid-only stacked bars, and representative trace
selection, but they are not exact physical root-cause proof.

Stage 4-Z2 distinguishes all-run accounting from invalid-only failure
analysis. Strict-valid runs may appear as `valid_or_warning` in all-run
diagnostic tables. The preferred paper failure-analysis view excludes
strict-valid runs and groups only strict-invalid runs.

## Paper Insertion Text

Method section draft:

> The risk-conditioned governor receives online odometry, payload odometry,
> wind annotation, goal, and trajectory-context streams and publishes
> `speed_scale` and `acceleration_scale` together with diagnostic
> `risk_score_3s` and `risk_score_5s` signals. In the current Paper 1 policy,
> the scores are produced by exported JSON `LogisticRegression` models over
> early episode features. Unavailable scores are represented as `-1` and do not
> trigger risk reductions. `risk_adapter_v1` reduces execution scale when the
> 3 s or 5 s score crosses configured thresholds and rate-limits scale changes.
> This is an empirical execution governor, not a certified safety filter.

Experimental setup draft:

> The main success metric is strict-valid count over repeated runs. A run is
> strict-valid only if the analyzer marks it as valid, no NaN state is observed,
> the maximum swing remains below `60 deg`, both UAV and payload speeds remain
> below `4 m/s`, and the final UAV XY error is at most `0.5 m`. Diagnostic
> failure labels, command-saturation events, swing warnings, and
> reference/position jump warnings are used for interpretation but do not
> replace the strict-valid definition.

Supplementary draft:

> Supplementary material should list the exact strict-valid predicate, the raw
> `valid_run_suggested` predicate, the risk-score topics and logged fields, the
> final exported model metadata, and the launch parameters used for
> `risk_adapter_v1`. Missing risk scores are logged as `-1` and are excluded
> from non-negative risk-score summary statistics.

## RA-L Readiness Impact

Stage 4-AU closes the RA-L must-fix item for documenting:

- `risk_score_3s` / `risk_score_5s` adapter interface and logged fields;
- unavailable risk behavior;
- `risk_adapter_v1` threshold and scale logic;
- the strict-valid metric used for Paper 1 result tables;
- the boundary between paper-facing success and diagnostic failure labels.

Remaining before RA-L submission:

- official RA-L / IEEE template acquisition and compile;
- final citation verification and BibTeX cleanup;
- Figure 6 multi-panel layout polish;
- final claim audit;
- final exported model metadata, feature schema, calibration caveat, and
  inference-latency documentation if the manuscript makes those claims.

## What Not To Claim

Do not claim:

- the risk scores are calibrated unless calibration is documented for the
  deployed model;
- learned risk guarantees safety;
- strict-valid proves real-world safety;
- failure groups prove exact physical root cause;
- `risk_adapter_v22` is needed before Paper 1 RA-L submission;
- statistical significance unless a separate statistical analysis is completed;
- broad real-world deployment robustness from the current simulation-only
  evidence.
