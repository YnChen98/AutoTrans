# Stage 4-F 90-Row Calibration, Threshold, And Group Diagnostics

## Executive Summary

The 90-row strict-label Stage 4 risk prediction setup is now usable for offline
calibration and threshold diagnostics. The target label is
`label_strict_invalid`, with 51 valid rows and 39 strict-invalid rows.

Leave-one-target-out improves substantially compared with earlier smaller
datasets. This is the most important Stage 4-F signal, because it tests whether
the predictor can transfer across target points instead of only fitting repeated
runs from familiar targets.

`LogisticRegression` is the current balanced baseline. It has the strongest
leave-one-target-out AUROC, AUPRC, and Brier score among the recorded models,
and its ECE is close to `RandomForest`.

For leave-one-target-out `LogisticRegression`, threshold `0.4` is suitable for a
high-recall warning mode. Threshold `0.5` and threshold `0.7` are better treated
as high-precision guards, with threshold `0.7` reaching perfect precision in
the recorded sweep.

Do not deploy an online policy yet. The current `early` feature set includes
10s and 15s windows, so it is not yet clear whether the predictor can warn early
enough for online adaptation.

## Dataset Snapshot

| Field | Value |
| --- | --- |
| Rows | 90 |
| Label | `label_strict_invalid` |
| Class 0 | 51 valid rows |
| Class 1 | 39 strict-invalid rows |
| Targets | Trial 1, Trial 2, Trial 3, Trial 4, Trial 5, Trial 6 |
| Methods | `original`, `fixed_s085`, `windlevel_s085` |
| Feature set | `early` |
| `drop_command_scale_features` | `true` |
| `drop_method_features` | `true` |
| sklearn environment | `~/venvs/autotrans-stage4` |

## Overall Metrics Table

| Validation | Model | Accuracy | Precision | Recall | F1 | AUROC | AUPRC | Brier | ECE |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Leave-one-target-out | `LogisticRegression` | 0.766667 | 0.875000 | 0.538462 | 0.666667 | 0.831071 | 0.847736 | 0.166523 | 0.112538 |
| Leave-one-target-out | `RandomForest` | 0.766667 | 0.875000 | 0.538462 | 0.666667 | 0.748869 | 0.792929 | 0.179753 | 0.104944 |
| LOO | `LogisticRegression` | 0.777778 | 0.787879 | 0.666667 | 0.722222 | 0.800905 | 0.828661 | 0.161343 | 0.108740 |
| LOO | `RandomForest` | 0.755556 | 0.793103 | 0.589744 | 0.676471 | 0.765460 | 0.802512 | 0.174859 | 0.101222 |
| Leave-one-method-out | `LogisticRegression` | 0.711111 | 0.685714 | 0.615385 | 0.648649 | 0.769734 | 0.788423 | 0.185327 | 0.124164 |
| Leave-one-method-out | `RandomForest` | 0.722222 | 0.705882 | 0.615385 | 0.657534 | 0.750126 | 0.777804 | 0.182028 | 0.152722 |

`LogisticRegression` is preferred as the current balanced baseline because it
has the best leave-one-target-out ranking metrics and Brier score, while keeping
similar classification metrics to `RandomForest`.

## Threshold Sweep Interpretation

Leave-one-target-out `LogisticRegression` threshold sweep:

| Threshold | Precision | Recall | F1 | Interpretation |
| ---: | ---: | ---: | ---: | --- |
| 0.4 | 0.611111 | 0.846154 | 0.709677 | High-recall warning threshold |
| 0.5 | 0.875000 | 0.538462 | 0.666667 | Default high-precision guard |
| 0.7 | 1.000000 | 0.461538 | 0.631579 | Strict high-precision guard |

Threshold `0.4` catches most strict-invalid rows and is the better candidate if
the predictor is used as an offline warning signal. It also accepts more false
positives, so it should not directly force a conservative online action yet.

Threshold `0.5` keeps precision high and is a reasonable default guard for
offline diagnostics. Threshold `0.7` is stricter: it avoids false positives in
the recorded sweep, but misses more strict-invalid rows.

## Group Diagnostics Summary

Leave-one-target-out is the key group diagnostic for Stage 4-F. The 90-row
dataset improves cross-target behavior enough that `LogisticRegression` reaches
`AUROC=0.831071` and `AUPRC=0.847736`, which is a substantial improvement over
the earlier target-generalization bottleneck.

LOO remains the strongest overall classification setting for
`LogisticRegression`, with `F1=0.722222` and `recall=0.666667`. This is useful
as a pipeline check, but it is less strict than grouped validation.

Leave-one-method-out remains lower than LOO and leave-one-target-out. This means
the model is not only reading method identity, especially because
`drop_method_features=true`, but method-level transfer is still a visible
diagnostic gap.

Across the recorded diagnostics, `RandomForest` is competitive on accuracy and
precision, but `LogisticRegression` gives a cleaner balance of ranking,
calibration, and interpretability for the current small dataset.

## Current Limitation

The main limitation is prediction horizon. The current `early` feature set
includes 10s and 15s windows, so the result does not yet prove that the model can
warn early enough for online risk-conditioned adaptation.

The next validation needs prediction-horizon ablation:

- 3s-only
- 5s-only
- 3+5s
- all windows

Until that ablation is complete, treat these results as offline calibration and
threshold diagnostics, not as an online policy result.

## Next Step

Add early-window feature selection to `train_stage4_risk_predictor.py`, then
rerun the 90-row strict-label diagnostics with 3s-only, 5s-only, 3+5s, and all
windows.
