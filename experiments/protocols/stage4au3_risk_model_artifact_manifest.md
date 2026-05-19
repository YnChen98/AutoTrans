# Stage 4-AU3 Risk Model Artifact Manifest

## Executive Summary

Stage 4-AU3 records checksums and reproducibility metadata for the generated
local risk model and dataset artifacts used by the current RA-L Paper 1 draft.
No models or datasets are committed by this task. No model training, new
experiments, ROS launch, simulation, LaTeX compile, or figure generation was
run.

This manifest supports RA-L reproducibility by freezing the exact local
artifact identities through paths, file sizes, and SHA256 checksums. It does
not imply calibration, safety, confidence, OOD, real-hardware, or inference
latency guarantees. `risk_adapter_v22` is not created.

## Artifact Manifest Table

| artifact | path | exists | file_size | sha256 | ignored_generated_status | paper_use | status |
| --- | --- | --- | ---: | --- | --- | --- | --- |
| 3s risk model JSON | `experiments/models/stage4_risk_logreg_3s.json` | yes | 23533 bytes | `bd3b15f30bc2d45577051d1adf727dfc82239786e1495dad97755da7cdcfe813` | ignored by `.gitignore` pattern `experiments/models/*.json`; generated artifact | Main Paper 1 early warning score used by `risk_adapter_v1` as `risk_score_3s`. | Exact local artifact identified by checksum; not tracked by git. |
| 5s risk model JSON | `experiments/models/stage4_risk_logreg_5s.json` | yes | 28417 bytes | `0a582e378c35d7a2a06999a8015ffa4c69ffd1d3dcc9b4e04251925122d4ad21` | ignored by `.gitignore` pattern `experiments/models/*.json`; generated artifact | Main Paper 1 early warning score used by `risk_adapter_v1` as `risk_score_5s`. | Exact local artifact identified by checksum; not tracked by git. |
| 15s risk model JSON | `experiments/models/stage4_risk_logreg_15s.json` | yes | 38399 bytes | `d1b4a666f0ea7a1d9dbf9ab8c18758abbb3bcc8636a2440abfdc996e77924635` | ignored by `.gitignore` pattern `experiments/models/*.json`; generated artifact | Exists as a generated support / monitoring artifact; not the main Paper 1 online protagonist channel. | Exact local artifact identified by checksum; not tracked by git. |
| Stage 4 risk dataset CSV | `experiments/datasets/stage4_risk_dataset.csv` | yes | 85669 bytes | `fd7f4d6437a2691e9ba55457f9e2536e038ed4ecefa0bc95504ce49d8ac0f153` | ignored by `.gitignore` pattern `experiments/datasets/*.csv`; generated artifact | Source dataset embedded in the JSON metadata for all three audited risk models. | Exact local artifact identified by checksum; not tracked by git. |

Commands used for this audit:

```bash
ls -lh experiments/models/stage4_risk_logreg_3s.json experiments/models/stage4_risk_logreg_5s.json experiments/models/stage4_risk_logreg_15s.json experiments/datasets/stage4_risk_dataset.csv
sha256sum experiments/models/stage4_risk_logreg_3s.json experiments/models/stage4_risk_logreg_5s.json experiments/models/stage4_risk_logreg_15s.json experiments/datasets/stage4_risk_dataset.csv
wc -l experiments/datasets/stage4_risk_dataset.csv
```

## Dataset Check

`wc -l experiments/datasets/stage4_risk_dataset.csv` reports:

```text
91 experiments/datasets/stage4_risk_dataset.csv
```

Interpretation:

- 1 header line.
- 90 data rows.
- The JSON metadata for the 3s, 5s, and 15s models reports
  `training_data.row_count=90`.
- The JSON metadata reports class counts `0=51` and `1=39`.
- The JSON metadata uses `label=label_strict_invalid`.

The dataset itself is ignored/generated and is not tracked by git. Before final
RA-L submission, it should either be archived in a controlled supplementary
package or regenerated reproducibly from a committed manifest and documented
commands.

## Model Metadata Summary

Shared metadata across the audited JSON model artifacts:

- `schema_version=stage4_logreg_json_v1`
- `created_by=train_stage4_risk_predictor.py`
- `model.type=LogisticRegression`
- `model.solver=liblinear`
- `model.class_weight=balanced`
- `model.max_iter=1000`
- `model.random_state=0`
- `model.sklearn_version=1.3.2`
- `label=label_strict_invalid`
- `feature_set=early`
- `drop_command_scale_features=true`
- `drop_method_features=true`
- `training_data.row_count=90`
- `training_data.class_counts`: class `0` has 51 rows, class `1` has 39 rows
- `reference_predictions`: 90 rows in each JSON artifact
- No calibration transform metadata found
- No confidence or OOD metadata found
- No inference latency metadata found
- No embedded export timestamp found

Horizon-specific metadata:

| artifact | horizon metadata | feature_count | paper interpretation |
| --- | ---: | ---: | --- |
| `stage4_risk_logreg_3s.json` | `max_early_window=3` | 16 | Main 3s empirical strict-invalid warning score for Paper 1. |
| `stage4_risk_logreg_5s.json` | `max_early_window=5` | 27 | Main 5s empirical strict-invalid warning score for Paper 1. |
| `stage4_risk_logreg_15s.json` | `max_early_window=15` | 49 | Generated support / monitoring artifact, not the main Paper 1 online protagonist channel. |

## Paper 1 Reproducibility Status

The exact local generated artifacts are now identified by SHA256 checksum.
This makes the current Paper 1 draft reproducible relative to the local files
inspected in Stage 4-AU2 and Stage 4-AU3.

The current git commit still does not track the generated JSON or CSV artifacts.
For final submission, use one of these controlled options:

- archive the generated model JSONs and dataset CSV in supplementary material;
- copy the artifacts into a controlled, explicitly allowed supplementary
  package;
- provide a regeneration script / command manifest that recreates artifacts
  with matching checksums.

Do not treat this checksum manifest as evidence of calibration, OOD detection,
formal safety, or real-world deployment robustness.

## Manuscript / Supplementary Wording

Safe manuscript wording:

> The risk models used in Paper 1 are generated artifacts identified in the
> supplementary reproducibility manifest by SHA256 checksums.

Safe method wording:

> The 3s and 5s models are used as empirical strict-invalid warning scores for
> execution governance.

Safe claim-boundary wording:

> No deployed calibration transform, confidence / OOD rejection mechanism, or
> inference-latency measurement is claimed for these artifacts.

## Remaining TODOs

- Decide whether to archive generated JSON / CSV artifacts in supplementary
  material.
- Decide whether to provide a regeneration script or command manifest that can
  reproduce the exact checksums.
- Verify whether the 15s model should be mentioned only as implementation
  support, not as a Paper 1 main method component.
- Avoid probability / calibration language unless a calibration method is
  added and documented.
- Avoid latency claims unless inference latency is measured.
