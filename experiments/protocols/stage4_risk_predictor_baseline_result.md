# Stage 4-B Risk Predictor Baseline Result

## Executive Summary

The Stage 4-B failure-risk prediction pipeline is working end to end on the local Stage 4-A dataset. The script can read `experiments/datasets/stage4_risk_dataset.csv`, select leakage-controlled feature sets, run leave-one-out evaluation, and report metrics without requiring additional package installation.

The first baseline result suggests that early dynamic features are more predictive than metadata-only features on this dataset. With `--feature-set early`, the `single_feature_threshold` fallback reaches higher recall and f1 than the `basic` feature set.

This dataset is still too small for final claims. The result should be treated as a pipeline validation and an early diagnostic, not as final Stage 4 performance evidence.

## Dataset Snapshot

Dataset:

```bash
experiments/datasets/stage4_risk_dataset.csv
```

Rows and labels:

- total rows: 15
- class_0 valid: 8
- class_1 invalid: 7

Method counts:

| Method | Rows | Valid | Invalid |
| --- | ---: | ---: | ---: |
| `original` | 5 | 3 | 2 |
| `fixed_s085` | 5 | 2 | 3 |
| `windlevel_s085` | 5 | 3 | 2 |

The dataset covers repeated strong-wind Trial 2 runs only. It does not yet cover enough targets, wind levels, or methods to support broad generalization claims.

## Model / Environment

Script:

```bash
experiments/scripts/train_stage4_risk_predictor.py
```

Environment note:

- `sklearn` was not available.
- The script used the standard-library fallback path.

Evaluated fallback models:

- `majority`
- `single_feature_threshold`

Evaluation mode:

- leave-one-out cross-validation with `--cv loo`
- default target label `label_invalid`

## Result Table

| Feature Set | Model | Accuracy | Precision | Recall | F1 | AUROC | AUPRC | Brier |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `basic` | `majority` | 0.533333 | 0 | 0 | 0 | 0 | 0.466667 | 0.285714 |
| `basic` | `single_feature_threshold` | 0.2 | 0.272727 | 0.428571 | 0.333333 | 0 | 0.38355 | 0.366975 |
| `early` | `majority` | 0.533333 | 0 | 0 | 0 | 0 | 0.466667 | 0.285714 |
| `early` | `single_feature_threshold` | 0.666667 | 0.625 | 0.714286 | 0.666667 | 0.714286 | 0.847619 | 0.291667 |
| `all` | `majority` | 0.533333 | 0 | 0 | 0 | 0 | 0.466667 | 0.285714 |
| `all` | `single_feature_threshold` | 0.666667 | 0.625 | 0.714286 | 0.666667 | 0.714286 | 0.847619 | 0.291667 |

In this dataset, `--feature-set all` is the same as `--feature-set early` because `all` currently includes metadata plus `early_*` features while excluding final-outcome leakage features.

## Interpretation

The `basic` feature set uses metadata-like features such as `method`, `adaptation_mode`, `policy_mode`, `command_scale_expected`, `wind_force_norm`, and target coordinates. On the current 15 rows, metadata alone is not enough for a useful invalid-run detector.

The `early` feature set adds early-window dynamics such as `early_*_max_uav_speed`, `early_*_max_payload_speed`, `early_*_max_swing_angle_deg`, `early_*_target_distance_end`, and `early_*_target_progress`. The fallback `single_feature_threshold` performs better with these features, which is consistent with the goal of early failure-risk prediction.

The `majority` model predicts the dominant training-fold class. It is useful as a sanity baseline, but it has zero recall for invalid runs in this evaluation, so it is not useful as a risk detector.

The `single_feature_threshold` result should be interpreted carefully. It shows that early dynamics contain signal, but a 15-row dataset can be highly sensitive to one or two runs.

## What Not To Claim

Do not claim final Stage 4 predictor performance from this result.

Do not claim that `single_feature_threshold` is the preferred final model.

Do not claim that `policy_mode=wind_level` is final or generally superior based on this dataset.

Do not compare methods using single-run evidence. Stage 4 and later Stage 3 conclusions should continue to use repeated success-rate comparisons.

Do not treat `--feature-set all` as a broad full-feature model yet. In this baseline, it intentionally remains leakage-controlled and matches `early`.

## Next Steps

Expand the dataset beyond the current 15 rows.

Add more targets, wind levels, and methods so the predictor is not only fitting strong-wind Trial 2 repeats.

Run the same script again once `sklearn` is available to evaluate `logistic_regression` and `random_forest`.

Add calibration-oriented checks as the dataset grows, including Brier score trends, reliability curves, and probability calibration.

Keep result summaries explicit about repeated-run counts, invalid runs, and the difference between pipeline validation and final performance claims.
