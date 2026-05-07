# Stage 4 Risk Predictor 30-Row Baseline Result

## Executive Summary

The Stage 4-B risk prediction pipeline works on the expanded 30-row Stage 4 risk dataset.

Early-time dynamics improve precision, AUPRC, F1, and Brier score compared with metadata-only `basic` features. The `early` and `all` feature sets produce the same result on this 30-row dataset.

AUROC remains low, and the dataset is still too limited for final claims about model quality, calibration, or method superiority.

## Dataset Snapshot

- Rows: 30
- Class 0 valid: 22
- Class 1 invalid: 8
- Wind level: `strong`
- Targets: Trial 1 and Trial 2
- Methods:
  - `original`: 10 rows
  - `fixed_s085`: 10 rows
  - `windlevel_s085`: 10 rows
- Modeling backend: standard-library fallback models, because `sklearn` is not available.

## Result Table

| Model | Accuracy | Precision | Recall | F1 | AUROC | AUPRC | Brier | TN | FP | FN | TP |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Majority baseline | 0.733333 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.266667 | 0.209275 | 22 | 0 | 8 | 0 |
| `basic`, `single_feature_threshold` | 0.700000 | 0.466667 | 0.875000 | 0.608696 | 0.556818 | 0.441667 | 0.178571 | 14 | 8 | 1 | 7 |
| `early`, `single_feature_threshold` | 0.833333 | 0.714286 | 0.625000 | 0.666667 | 0.568182 | 0.539881 | 0.156715 | 20 | 2 | 3 | 5 |
| `all`, `single_feature_threshold` | 0.833333 | 0.714286 | 0.625000 | 0.666667 | 0.568182 | 0.539881 | 0.156715 | 20 | 2 | 3 | 5 |

## Interpretation

The `basic` feature set reaches high recall at 0.875000, but it produces many false positives, with `fp=8`. This means it catches most invalid runs but marks too many valid runs as risky.

The `early` feature set reduces false positives to `fp=2` and improves balanced performance. Compared with `basic`, it improves precision, AUPRC, F1, and Brier score, while recall decreases from 0.875000 to 0.625000.

The `all` feature set does not improve over `early` in this 30-row dataset. For now, the additional full-run features do not add useful signal beyond the early-time dynamics used by `early`.

Early dynamics appear useful, but they are not sufficient for a final Stage 4 claim. The low AUROC indicates weak ranking quality, and the dataset is still too small and narrow for stable model conclusions.

## Limitations

- Only 30 rows are available.
- The dataset covers only strong wind.
- The dataset covers only Trial 1 and Trial 2.
- `sklearn` is not available, so this run used standard-library fallback models.
- There is no calibration claim yet.

## Next Step

Expand the manifest and dataset with Trial 3 runs to reach 45 rows. Then rerun the Stage 4 risk predictor and compare whether the `early` feature advantage remains stable.

After the dataset grows further, rerun the predictor with `sklearn` models to evaluate stronger baselines and calibration behavior.
