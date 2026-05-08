# Stage 4 Risk Predictor 90-Row Strict-Label Result

## Executive Summary

Stage 4-E Trial 6 expands the Stage 4 strict-label risk dataset to 90 rows
across six strong-wind targets. The main safety-risk label remains
`label_strict_invalid`, because it keeps strict-invalid failure cases visible as
the positive risk class.

Leave-one-target-out performance improves substantially after the Trial 6
expansion. This supports the working hypothesis that broader target diversity is
helping cross-target risk prediction.

Early dynamics remain predictive even after dropping method identity and command
scale features. This means the current result is not only memorizing `method`,
`speed_scale`, or `acceleration_scale`.

## Dataset Snapshot

| Field | Value |
| --- | --- |
| Rows | 90 |
| Label | `label_strict_invalid` |
| Class 0 | 51 valid rows |
| Class 1 | 39 invalid rows |
| Targets | Trial 1, Trial 2, Trial 3, Trial 4, Trial 5, Trial 6 |
| Methods | `original`, `fixed_s085`, `windlevel_s085` |
| Wind level | `strong` |
| Feature set | `early` |
| `drop_command_scale_features` | `true` |
| `drop_method_features` | `true` |
| sklearn environment | `~/venvs/autotrans-stage4` |

## Result Table

| Split | Model | Accuracy | Precision | Recall | F1 | AUROC | AUPRC | Brier |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| LOO | LogisticRegression | 0.777778 | 0.787879 | 0.666667 | 0.722222 | 0.800905 | 0.828661 | 0.161343 |
| LOO | RandomForest | 0.755556 | 0.793103 | 0.589744 | 0.676471 | 0.765460 | 0.802512 | 0.174859 |
| Leave-one-target-out | LogisticRegression | 0.766667 | 0.875000 | 0.538462 | 0.666667 | 0.831071 | 0.847736 | 0.166523 |
| Leave-one-target-out | RandomForest | 0.766667 | 0.875000 | 0.538462 | 0.666667 | 0.748869 | 0.792929 | 0.179753 |
| Leave-one-method-out | LogisticRegression | 0.711111 | 0.685714 | 0.615385 | 0.648649 | 0.769734 | 0.788423 | 0.185327 |
| Leave-one-method-out | RandomForest | 0.722222 | 0.705882 | 0.615385 | 0.657534 | 0.750126 | 0.777804 | 0.182028 |

## Interpretation

`LogisticRegression` is the main balanced baseline for the 90-row strict-label
dataset. It gives the strongest leave-one-target AUROC, AUPRC, and Brier score
among the recorded models, while keeping a reasonable precision and recall
balance across LOO and leave-one-method-out.

`RandomForest` has the same leave-one-target precision as `LogisticRegression`
(`precision=0.875000`), but its calibration and recall tradeoff is weaker in the
recorded results. Its leave-one-target Brier score is higher, and its LOO recall
is lower.

The Trial 6 expansion improves target diversity and appears to improve
cross-target generalization. This is an important step for Stage 4, because a
risk predictor should not only work on targets already represented in the
training fold.

The predictor is promising, but it is not yet an online policy. These results
support continued diagnostics before using predictions to drive online
risk-conditioned command adaptation.

## Comparison With 75-Row Result

Compared with the 75-row strict-label result, leave-one-target-out
`LogisticRegression` improves from `AUROC=0.708148` and `AUPRC=0.700699` to
`AUROC=0.831071` and `AUPRC=0.847736`.

This improvement is consistent with the current Stage 4 direction: add more
target diversity first, then evaluate whether the learned risk signal is stable
enough for calibration and threshold design.

## Limitations

- The dataset is strong wind only.
- The dataset still has only 90 rows.
- No calibration curve has been checked yet.
- No threshold selection has been performed yet.
- No online risk-conditioned command adaptation has been implemented yet.

## Next Step

- Run Stage 4-F calibration and threshold diagnostics.
- Add per-target and per-method fold diagnostics.
- Then design risk-conditioned command adaptation.

## What Not To Claim

- Do not claim final generalization yet.
- Do not claim the online policy is ready.
- Do not hide strict-invalid safety failures.
