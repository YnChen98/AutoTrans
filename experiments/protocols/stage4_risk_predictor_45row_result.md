# Stage 4 Risk Predictor 45-Row Baseline Result

## Executive Summary

The Stage 4 risk dataset now has 45 rows across Trial 1, Trial 2, and Trial 3 strong-wind runs.

In this 45-run set, `windlevel_s085` has the highest success rate among the three compared methods.

Early-time dynamics strongly improve failure-risk prediction over metadata-only prediction. The `early` feature set improves F1, AUROC, AUPRC, and Brier score compared with the `basic` feature set.

This result is still preliminary. The dataset is not large or diverse enough for final claims about predictor quality, calibration, or method superiority.

## Dataset Snapshot

Dataset scope:

- Rows: 45
- Class 0 valid: 27
- Class 1 invalid: 18
- Wind level: `strong`
- Targets: Trial 1, Trial 2, and Trial 3
- Modeling backend: standard-library fallback models, because `sklearn` is not available.

Method counts:

| Method | Rows | Valid | Invalid |
| --- | ---: | ---: | ---: |
| `original` | 15 | 9 | 6 |
| `fixed_s085` | 15 | 7 | 8 |
| `windlevel_s085` | 15 | 11 | 4 |

## Method Success-Rate Table

| Method | Valid Runs | Invalid Runs | Success Rate |
| --- | ---: | ---: | ---: |
| `original` | 9/15 | 6/15 | 0.600000 |
| `fixed_s085` | 7/15 | 8/15 | 0.466667 |
| `windlevel_s085` | 11/15 | 4/15 | 0.733333 |

## Predictor Result Table

| Feature Set | Model | Accuracy | Precision | Recall | F1 | AUROC | AUPRC | Brier | TN | FP | FN | TP |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Majority baseline | `majority` | 0.600000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.400000 | 0.251033 | 27 | 0 | 18 | 0 |
| `basic` | `single_feature_threshold` | 0.533333 | 0.434783 | 0.555556 | 0.487805 | 0.452675 | 0.548148 | 0.272113 | 14 | 13 | 8 | 10 |
| `early` | `single_feature_threshold` | 0.800000 | 0.736842 | 0.777778 | 0.756757 | 0.633745 | 0.659607 | 0.171799 | 22 | 5 | 4 | 14 |
| `all` | `single_feature_threshold` | 0.800000 | 0.736842 | 0.777778 | 0.756757 | 0.633745 | 0.659607 | 0.171799 | 22 | 5 | 4 | 14 |

## Interpretation

The `basic` feature set is metadata-only and remains unreliable on this 45-row dataset. It performs worse than the majority baseline on accuracy, produces many false positives with `fp=13`, and has weak ranking quality with AUROC below 0.5.

The `early` feature set adds early-time dynamics and improves the main risk-detection metrics. Compared with `basic`, it improves F1 from 0.487805 to 0.756757, AUROC from 0.452675 to 0.633745, AUPRC from 0.548148 to 0.659607, and Brier score from 0.272113 to 0.171799.

The `all` feature set does not improve beyond `early` in this 45-row dataset. In this run, the additional features do not add useful signal beyond the early-time dynamics.

This supports continuing the early failure-risk prediction route. It does not yet justify final claims about a deployable risk predictor or a final command-adaptation policy.

## Limitations

- Only 45 rows are available.
- The dataset covers only `strong` wind.
- The dataset covers only 3 targets.
- `sklearn` is not available in the current environment.
- The predictor uses only the fallback `single_feature_threshold` model beyond the majority baseline.
- There is no leave-one-target-out analysis yet.
- There is no calibration curve yet.

## Next Step

- Install or use `sklearn` after confirming the environment.
- Add `logistic_regression` and `random_forest` baselines.
- Add a leave-one-target-out split.
- Expand beyond `strong` wind to `moderate` and boundary wind cases.
- Eventually build risk-conditioned command adaptation.
