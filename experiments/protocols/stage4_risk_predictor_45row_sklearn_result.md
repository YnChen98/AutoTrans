# Stage 4 Risk Predictor 45-Row Sklearn Result

## Executive Summary

The 45-row `sklearn` run confirms that early-time dynamics substantially improve Stage 4 failure-risk prediction.

`LogisticRegression` with `early` and `all` features is currently the best baseline in this run. It reaches the highest accuracy, F1, AUROC, AUPRC, and the lowest Brier score among the tested models.

`RandomForest` underperforms `LogisticRegression` on this small dataset. This likely reflects limited data rather than a final model conclusion.

These results are promising, but they are not final. The dataset is still small and narrow, so this should be treated as stronger pipeline evidence, not as a deployable risk predictor claim.

## Dataset Snapshot

Dataset:

```bash
experiments/datasets/stage4_risk_dataset.csv
```

Rows and labels:

- Total rows: 45
- Class 0 valid: 27
- Class 1 invalid: 18
- Wind level: `strong` only
- Targets: Trial 1, Trial 2, and Trial 3

Method counts:

| Method | Rows | Valid | Invalid |
| --- | ---: | ---: | ---: |
| `original` | 15 | 9 | 6 |
| `fixed_s085` | 15 | 7 | 8 |
| `windlevel_s085` | 15 | 11 | 4 |

Model environment:

- Python venv: `~/venvs/autotrans-stage4`
- `numpy`: 1.24.4
- `scipy`: 1.10.1
- `scikit-learn`: 1.3.2
- Evaluation mode: leave-one-out cross-validation
- Target label: `label_invalid`

## Result Table

| Feature Set | Model | Accuracy | Precision | Recall | F1 | AUROC | AUPRC | Brier | TN | FP | FN | TP |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Majority baseline | `majority` | 0.600000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.400000 | 0.251033 | 27 | 0 | 18 | 0 |
| `basic` | `LogisticRegression` | 0.711111 | 0.600000 | 0.833333 | 0.697674 | 0.759259 | 0.725765 | 0.208351 | 17 | 10 | 3 | 15 |
| `basic` | `RandomForest` | 0.555556 | 0.458333 | 0.611111 | 0.523810 | 0.687243 | 0.650649 | 0.236184 | 14 | 13 | 7 | 11 |
| `early` | `LogisticRegression` | 0.844444 | 0.823529 | 0.777778 | 0.800000 | 0.837449 | 0.860471 | 0.145346 | 24 | 3 | 4 | 14 |
| `early` | `RandomForest` | 0.800000 | 0.800000 | 0.666667 | 0.727273 | 0.777778 | 0.811451 | 0.168795 | 24 | 3 | 6 | 12 |

The `all` feature set matched the `early` feature set in this run.

## Interpretation

The `basic` feature set is helpful but not sufficient. With `LogisticRegression`, it improves over the majority baseline and detects invalid runs with recall of 0.833333, but it also produces many false positives with `fp=10`.

Early dynamics improve the overall risk-prediction profile. Compared with `basic` plus `LogisticRegression`, `early` plus `LogisticRegression` improves accuracy from 0.711111 to 0.844444, precision from 0.600000 to 0.823529, F1 from 0.697674 to 0.800000, AUROC from 0.759259 to 0.837449, AUPRC from 0.725765 to 0.860471, and Brier score from 0.208351 to 0.145346.

`LogisticRegression` is currently the most stable baseline. It outperforms `RandomForest` on both `basic` and `early` feature sets in this 45-row evaluation.

`RandomForest` may need more data before it becomes competitive. On this small dataset, it has lower accuracy, F1, AUROC, AUPRC, and calibration quality than `LogisticRegression`.

## Caveats

- Only 45 rows are available.
- The dataset covers only `strong` wind.
- The dataset covers only 3 targets.
- The evaluation uses leave-one-out cross-validation only.
- There is no leave-one-target-out evaluation yet.
- Command-scale missingness may encode method information, so some predictive signal may come from method identity rather than only early dynamics.

## Next Steps

- Add group cross-validation and leave-one-target-out support.
- Add a no-command-scale ablation to test whether command-scale missingness is leaking method information.
- Expand the dataset beyond `strong` wind.
- Later develop risk-conditioned command adaptation after the risk predictor is validated on broader data.
