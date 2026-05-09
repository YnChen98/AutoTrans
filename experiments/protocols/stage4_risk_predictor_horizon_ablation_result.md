# Stage 4-G Prediction-Horizon Ablation Result

## Executive Summary

Stage 4-G evaluates whether the Stage 4 risk predictor can detect strict-invalid
risk early enough to support online command adaptation. The target label is
`label_strict_invalid`, with 51 strict-valid rows and 39 strict-invalid rows
from the 90-row strong-wind dataset.

The 3s and 5s feature windows already contain a useful risk signal. In
leave-one-target-out validation, `LogisticRegression` reaches high recall at
both horizons, which is the most important property for an early warning signal.

The 3s and 5s windows are high-recall but lower-precision settings. This means
they are better suited for soft warning or mild command adaptation, not for a
hard intervention policy.

The 10s and 15s windows improve AUROC, AUPRC, and precision, but they may be too
late for fast failures. The first online policy should therefore use 3s/5s risk
only as a conservative soft warning, while treating 10s/15s risk as higher
confidence monitoring evidence.

## Dataset And Evaluation Setup

| Field | Value |
| --- | --- |
| Rows | 90 |
| Label | `label_strict_invalid` |
| Class 0 | 51 strict-valid rows |
| Class 1 | 39 strict-invalid rows |
| Targets | Trial 1, Trial 2, Trial 3, Trial 4, Trial 5, Trial 6 |
| Methods | `original`, `fixed_s085`, `windlevel_s085` |
| Wind level | `strong` |
| Feature set | `early` |
| CV | `leave-one-target-out` |
| `drop_command_scale_features` | `true` |
| `drop_method_features` | `true` |
| Model | `LogisticRegression` |
| sklearn environment | `~/venvs/autotrans-stage4` |

## Horizon Result Table

| Horizon | `max_early_window` | Accuracy | Precision | Recall | F1 | AUROC | AUPRC | Brier | ECE |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 3s only | 3 | 0.655556 | 0.566667 | 0.871795 | 0.686869 | 0.718451 | 0.696647 | 0.219672 | 0.138340 |
| 5s window | 5 | 0.644444 | 0.559322 | 0.846154 | 0.673469 | 0.730518 | 0.694884 | 0.206345 | 0.120873 |
| 10s window | 10 | 0.644444 | 0.577778 | 0.666667 | 0.619048 | 0.770739 | 0.781897 | 0.192087 | 0.146416 |
| 15s / all windows | 15 | 0.766667 | 0.875000 | 0.538462 | 0.666667 | 0.831071 | 0.847736 | 0.166523 | 0.112538 |

## Threshold Interpretation

| Horizon | Threshold | Precision | Recall | F1 | Interpretation |
| --- | ---: | ---: | ---: | ---: | --- |
| 3s only | 0.4 | 0.557377 | 0.871795 | 0.680000 | High-recall early warning |
| 3s only | 0.5 | 0.566667 | 0.871795 | 0.686869 | Default early warning |
| 5s window | 0.5 | 0.559322 | 0.846154 | 0.673469 | Default early warning |
| 10s window | 0.5 | 0.577778 | 0.666667 | 0.619048 | Later, more balanced warning |
| 15s / all windows | 0.4 | 0.611111 | 0.846154 | 0.709677 | High-recall late warning |
| 15s / all windows | 0.5 | 0.875000 | 0.538462 | 0.666667 | High-precision late guard |
| 15s / all windows | 0.7 | 1.000000 | 0.461538 | 0.631579 | Strict high-precision late guard |

The 3s and 5s thresholds preserve strong recall, which is useful when missing an
invalid run is more costly than producing a false warning. Their precision is
still modest, so the prediction should not directly force a large intervention.

The 15s thresholds show the expected precision-recall tradeoff. Threshold `0.4`
recovers high recall, while thresholds `0.5` and `0.7` move toward high
precision and lower recall. This is useful for offline diagnostics and
high-confidence monitoring, but it does not solve the online timing problem.

## Online Policy Implication

The 3s and 5s risk scores can trigger mild command adaptation, such as a small
temporary speed or acceleration reduction. They are the best current candidates
for a first online warning channel because they appear early enough to matter.

The 10s and 15s risk scores can support high-confidence monitoring and offline
diagnostics, but they may be too late to prevent fast failures. They should not
be treated as the primary trigger for the first online policy.

Do not directly deploy a hard guard based only on 15s features. The 15s result
has stronger ranking metrics and precision, but using it alone would bias the
policy toward late detection.

## Limitations

- The dataset is strong wind only.
- No actual online closed-loop risk policy has been tested yet.
- The 3s and 5s precision is still modest.
- Risk score calibration still needs caution.
- The dataset has only 90 rows, so the result is still a research diagnostic,
  not a final safety guarantee.

## Next Step

Design Stage 4-H risk-conditioned command adaptation v0.

The first implementation should start with conservative soft intervention:

- Use 3s/5s risk as the early warning source.
- Apply only mild command adaptation at first.
- Keep 10s/15s risk for monitoring and post-run diagnostics.
- Evaluate the policy with repeated strong-wind runs before making any final
  claim.
