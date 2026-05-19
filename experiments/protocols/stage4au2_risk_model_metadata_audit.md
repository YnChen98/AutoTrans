# Stage 4-AU2 Risk Model Metadata Audit

## Executive Summary

Stage 4-AU2 audits the final risk model metadata available for the RA-L Paper
1 track. No model training, simulation, ROS launch, LaTeX compile, or figure
generation was run. The audit is based only on existing generated model JSONs,
existing scripts, and existing protocol documents.

All three expected JSON model files are present locally under
`experiments/models/`, but they are ignored/generated artifacts. Their metadata
is sufficient to describe the current local model family, dataset row count,
class counts, feature schema, and exported `LogisticRegression` configuration.
Calibration transforms, confidence / OOD handling, inference latency, embedded
export timestamp, and a committed/frozen model artifact remain TODOs before
final RA-L submission claims.

No `risk_adapter_v22` is introduced.

## Model Artifact Inventory

| path | exists | ignored/generated | inspected | metadata summary |
| --- | --- | --- | --- | --- |
| `experiments/models/stage4_risk_logreg_3s.json` | yes | yes, ignored by `.gitignore` pattern `experiments/models/*.json` | yes | `schema_version=stage4_logreg_json_v1`; `LogisticRegression`; `max_early_window=3`; 16 features; 90 rows; class counts `0=51`, `1=39`. |
| `experiments/models/stage4_risk_logreg_5s.json` | yes | yes, ignored by `.gitignore` pattern `experiments/models/*.json` | yes | `schema_version=stage4_logreg_json_v1`; `LogisticRegression`; `max_early_window=5`; 27 features; 90 rows; class counts `0=51`, `1=39`. |
| `experiments/models/stage4_risk_logreg_15s.json` | yes | yes, ignored by `.gitignore` pattern `experiments/models/*.json` | yes | `schema_version=stage4_logreg_json_v1`; `LogisticRegression`; `max_early_window=15`; 49 features; 90 rows; class counts `0=51`, `1=39`. |

The source dataset path embedded in all three JSON files is:

```text
/home/cccyn2004/projects/autotrans_ws/src/AutoTrans/experiments/datasets/stage4_risk_dataset.csv
```

The dataset file exists locally and is also ignored/generated. `wc -l` reports
91 lines, meaning 90 data rows plus the CSV header. This matches the JSON
`training_data.row_count=90`.

## Extracted Metadata Table

| artifact | horizon | model_type | feature_count | feature_names_summary | training_rows | positive_count | negative_count | calibration_metadata | confidence_or_ood_metadata | metadata_status |
| --- | ---: | --- | ---: | --- | ---: | ---: | ---: | --- | --- | --- |
| `stage4_risk_logreg_3s.json` | 3 | `LogisticRegression`, `solver=liblinear`, `class_weight=balanced`, `max_iter=1000`, `random_state=0`, `sklearn_version=1.3.2` | 16 | base target/wind fields plus `early_3s_*` features | 90 | 39 | 51 | no calibration transform or calibration metadata in JSON | no confidence or OOD metadata in JSON | model/training/features present; calibration/confidence/OOD/latency/timestamp/export command absent |
| `stage4_risk_logreg_5s.json` | 5 | `LogisticRegression`, `solver=liblinear`, `class_weight=balanced`, `max_iter=1000`, `random_state=0`, `sklearn_version=1.3.2` | 27 | base target/wind fields plus `early_3s_*` and `early_5s_*` features | 90 | 39 | 51 | no calibration transform or calibration metadata in JSON | no confidence or OOD metadata in JSON | model/training/features present; calibration/confidence/OOD/latency/timestamp/export command absent |
| `stage4_risk_logreg_15s.json` | 15 | `LogisticRegression`, `solver=liblinear`, `class_weight=balanced`, `max_iter=1000`, `random_state=0`, `sklearn_version=1.3.2` | 49 | base target/wind fields plus `early_3s_*`, `early_5s_*`, `early_10s_*`, and `early_15s_*` features | 90 | 39 | 51 | no calibration transform or calibration metadata in JSON | no confidence or OOD metadata in JSON | model/training/features present; calibration/confidence/OOD/latency/timestamp/export command absent |

Additional fields found in each JSON:

- `created_by=train_stage4_risk_predictor.py`
- `label=label_strict_invalid`
- `feature_set=early`
- `drop_command_scale_features=true`
- `drop_method_features=true`
- `class_mapping`: negative class `0`, positive class `1`, positive
  probability class `1`, sklearn classes `[0, 1]`
- `preprocessing`: median imputation for missing / NaN / Inf numeric values,
  `StandardScaler` statistics, and feature specs
- `reference_predictions`: 90 full-dataset sklearn reference probabilities
- `model.coefficients` and `model.intercept`: present; not dumped here because
  the exact values are long and already stored in the JSON artifacts

No embedded export timestamp, train/validation/test split, calibration model,
confidence threshold, OOD detector, or inference latency measurement was found
inside the JSON metadata.

## Feature Schema

### `stage4_risk_logreg_3s.json`

Exact feature names:

- `wind_force_norm`
- `target_x`
- `target_y`
- `target_z`
- `payload_target_z`
- `early_3s_max_payload_speed`
- `early_3s_max_swing_angle_deg`
- `early_3s_max_uav_speed`
- `early_3s_max_wind_force_norm`
- `early_3s_mean_payload_speed`
- `early_3s_mean_swing_angle_deg`
- `early_3s_mean_uav_speed`
- `early_3s_mean_wind_force_norm`
- `early_3s_p95_swing_angle_deg`
- `early_3s_target_distance_end`
- `early_3s_target_progress`

### `stage4_risk_logreg_5s.json`

Exact feature names:

- `wind_force_norm`
- `target_x`
- `target_y`
- `target_z`
- `payload_target_z`
- `early_3s_max_payload_speed`
- `early_3s_max_swing_angle_deg`
- `early_3s_max_uav_speed`
- `early_3s_max_wind_force_norm`
- `early_3s_mean_payload_speed`
- `early_3s_mean_swing_angle_deg`
- `early_3s_mean_uav_speed`
- `early_3s_mean_wind_force_norm`
- `early_3s_p95_swing_angle_deg`
- `early_3s_target_distance_end`
- `early_3s_target_progress`
- `early_5s_max_payload_speed`
- `early_5s_max_swing_angle_deg`
- `early_5s_max_uav_speed`
- `early_5s_max_wind_force_norm`
- `early_5s_mean_payload_speed`
- `early_5s_mean_swing_angle_deg`
- `early_5s_mean_uav_speed`
- `early_5s_mean_wind_force_norm`
- `early_5s_p95_swing_angle_deg`
- `early_5s_target_distance_end`
- `early_5s_target_progress`

### `stage4_risk_logreg_15s.json`

The 15 s artifact is present but is not the Paper 1 online protagonist risk
channel. Exact feature names:

- `wind_force_norm`
- `target_x`
- `target_y`
- `target_z`
- `payload_target_z`
- `early_10s_max_payload_speed`
- `early_10s_max_swing_angle_deg`
- `early_10s_max_uav_speed`
- `early_10s_max_wind_force_norm`
- `early_10s_mean_payload_speed`
- `early_10s_mean_swing_angle_deg`
- `early_10s_mean_uav_speed`
- `early_10s_mean_wind_force_norm`
- `early_10s_p95_swing_angle_deg`
- `early_10s_target_distance_end`
- `early_10s_target_progress`
- `early_15s_max_payload_speed`
- `early_15s_max_swing_angle_deg`
- `early_15s_max_uav_speed`
- `early_15s_max_wind_force_norm`
- `early_15s_mean_payload_speed`
- `early_15s_mean_swing_angle_deg`
- `early_15s_mean_uav_speed`
- `early_15s_mean_wind_force_norm`
- `early_15s_p95_swing_angle_deg`
- `early_15s_target_distance_end`
- `early_15s_target_progress`
- `early_3s_max_payload_speed`
- `early_3s_max_swing_angle_deg`
- `early_3s_max_uav_speed`
- `early_3s_max_wind_force_norm`
- `early_3s_mean_payload_speed`
- `early_3s_mean_swing_angle_deg`
- `early_3s_mean_uav_speed`
- `early_3s_mean_wind_force_norm`
- `early_3s_p95_swing_angle_deg`
- `early_3s_target_distance_end`
- `early_3s_target_progress`
- `early_5s_max_payload_speed`
- `early_5s_max_swing_angle_deg`
- `early_5s_max_uav_speed`
- `early_5s_max_wind_force_norm`
- `early_5s_mean_payload_speed`
- `early_5s_mean_swing_angle_deg`
- `early_5s_mean_uav_speed`
- `early_5s_mean_wind_force_norm`
- `early_5s_p95_swing_angle_deg`
- `early_5s_target_distance_end`
- `early_5s_target_progress`

## Horizon Semantics

The horizon semantics are implementation-derived from
`experiments/scripts/train_stage4_risk_predictor.py`,
`experiments/scripts/build_stage4_risk_dataset.py`,
`experiments/protocols/stage4_risk_prediction_protocol.md`, and
`experiments/command_adaptation/scripts/risk_conditioned_command_adapter.py`.

Verified statements:

- The 3 s model uses `max_early_window=3` and the `early_3s_*` feature family.
- The 5 s model uses `max_early_window=5` and keeps both `early_3s_*` and
  `early_5s_*` feature families.
- The 15 s model uses `max_early_window=15` and keeps `early_3s_*`,
  `early_5s_*`, `early_10s_*`, and `early_15s_*` feature families.
- All audited JSON artifacts use `label_strict_invalid` as the positive class
  label.
- Existing Stage 4-G documentation frames 3 s and 5 s scores as high-recall
  early warning signals with modest precision, suitable for soft warning or
  mild command adaptation rather than a hard intervention policy.

Safe manuscript wording should call the outputs risk scores or
strict-invalid warning scores, not calibrated physical probabilities.

## Calibration / Confidence / Latency

Calibration:

- No calibration transform was found in the JSON artifacts.
- `train_stage4_risk_predictor.py` can compute calibration diagnostics such as
  ECE and calibration bins during evaluation, and Stage 4-F / Stage 4-G record
  offline ECE diagnostics.
- Those diagnostics are not a deployed calibration transform in the audited
  JSONs.
- Do not claim calibrated probabilities for Paper 1 unless a calibration method
  is added and documented separately.

Confidence and OOD:

- No confidence output, OOD detector, OOD threshold, or abstention behavior was
  found in the audited JSONs or current adapter implementation.
- The adapter treats finite non-negative risk scores as available and uses
  threshold comparisons; it does not reject OOD states.

Latency and rate:

- No inference latency measurement was found.
- The adapter `publish_rate` default is `5.0 Hz` in
  `experiments/command_adaptation/launch/risk_conditioned_command_adapter.launch`
  and `risk_conditioned_command_adapter.py`.
- Safe wording: scores are published by the adapter timer at the configured
  default `5.0 Hz`; inference latency was not separately measured.

## RA-L Manuscript Wording

Safe Method wording:

> The governor uses exported JSON `LogisticRegression` models trained on the
> 90-row Stage 4 strict-valid dataset with `label_strict_invalid` as the
> positive class. The 3 s model uses 16 features from wind/target metadata and
> `early_3s_*` dynamics; the 5 s model uses 27 features from the same metadata
> plus `early_3s_*` and `early_5s_*` dynamics. The resulting values are used as
> empirical strict-invalid warning scores. They are not claimed to be calibrated
> physical probabilities, and the current implementation does not include
> confidence or OOD rejection.

Safe supplementary wording:

> Supplementary material lists the full feature schema and JSON metadata for
> `experiments/models/stage4_risk_logreg_3s.json` and
> `experiments/models/stage4_risk_logreg_5s.json`. The generated artifacts are
> ignored by git, so final submission should archive or checksum the exact
> model and dataset artifacts used for Paper 1.

Safe rate wording:

> Risk scores are published by the adapter timer at the configured default
> `5.0 Hz`; separate inference-latency measurements were not collected.

## Remaining TODOs

Before RA-L submission, still verify or complete:

- Freeze or archive the exact generated model artifacts used for Paper 1.
- Freeze or archive the exact generated dataset artifact, or record a checksum
  / manifest version for `experiments/datasets/stage4_risk_dataset.csv`.
- Decide whether the ignored local JSONs are the final Paper 1 artifacts or
  whether regenerated equivalents will be used.
- Record an export timestamp or model-artifact checksum; no embedded timestamp
  is present in the current JSONs.
- If the manuscript wants to use probability/calibration language, add a
  calibration method and document it; otherwise keep "warning score" wording.
- If the manuscript wants confidence / OOD claims, add and document a
  confidence / OOD mechanism; none exists in the audited files.
- If the manuscript wants timing claims beyond the configured `5.0 Hz` publish
  rate, measure inference latency; no latency measurement was found.
