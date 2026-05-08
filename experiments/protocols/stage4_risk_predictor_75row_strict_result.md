# Stage 4 Risk Predictor 75-Row Strict-Label Result

## Executive Summary

Trial 5 expands the Stage 4 strict-label risk dataset to 75 rows. The main
safety-risk label is now `label_strict_invalid`, because it keeps strict-invalid
failure cases visible instead of relying on a looser validity interpretation.

The leave-one-target-out setting improves compared with earlier smaller
datasets, indicating that adding target diversity is helping cross-target risk
prediction. Early dynamics remain useful even after dropping method identity and
command-scale features, so the result is not only memorizing `method` or
`speed_scale` / `acceleration_scale`.

## Dataset Snapshot

| Field | Value |
| --- | --- |
| Rows | 75 |
| Label | `label_strict_invalid` |
| Class 0 | 45 valid rows |
| Class 1 | 30 invalid rows |
| Targets | Trial 1, Trial 2, Trial 3, Trial 4, Trial 5 |
| Methods | `original`, `fixed_s085`, `windlevel_s085` |
| Wind level | `strong` |
| Feature set | `early` |
| `drop_command_scale_features` | `true` |
| `drop_method_features` | `true` |
| sklearn environment | `~/venvs/autotrans-stage4` |

## Predictor Result Table

| Split | Model | Accuracy | Precision | Recall | F1 | AUROC | AUPRC | Brier |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| LOO | LogisticRegression | 0.800000 | 0.777778 | 0.700000 | 0.736842 | 0.778519 | 0.795698 | 0.169411 |
| LOO | RandomForest | 0.733333 | 0.708333 | 0.566667 | 0.629630 | 0.757778 | 0.761008 | 0.182410 |
| Leave-one-target-out | LogisticRegression | 0.600000 | 0.500000 | 0.533333 | 0.516129 | 0.708148 | 0.700699 | 0.208627 |
| Leave-one-target-out | RandomForest | 0.773333 | 0.933333 | 0.466667 | 0.622222 | 0.736296 | 0.733438 | 0.185040 |
| Leave-one-method-out | LogisticRegression | 0.720000 | 0.666667 | 0.600000 | 0.631579 | 0.748889 | 0.738149 | 0.192940 |
| Leave-one-method-out | RandomForest | 0.693333 | 0.620690 | 0.600000 | 0.610169 | 0.734815 | 0.714111 | 0.197178 |

## Interpretation

`LogisticRegression` is the balanced baseline for the 75-row strict-label
dataset. It has the best LOO accuracy, recall, F1, AUROC, AUPRC, and Brier
score among the recorded LOO results, and it remains competitive in
leave-one-method-out.

`RandomForest` gives high precision in leave-one-target-out
(`precision=0.933333`), but its lower recall (`recall=0.466667`) means it misses
more strict-invalid cases. That behavior is useful as a conservative positive
prediction signal, but it is not enough by itself for safety-risk screening.

The stronger leave-one-target-out result after adding Trial 5 supports the
working hypothesis that target diversity improves cross-target risk prediction.
This is still early evidence: more targets are needed before using the predictor
inside an online command-adaptation policy.

Early dynamics remain useful even with `drop_command_scale_features=true` and
`drop_method_features=true`. This suggests the predictor is learning from early
run behavior rather than directly keying on method names or command-scale
settings.

## Research Decision

Continue Trial 6 expansion before attempting risk-conditioned command
adaptation. Keep `label_strict_invalid` as the main Stage 4 safety-risk label,
because it directly preserves strict-invalid failures as the positive risk
class.

## What Not To Claim

- Do not claim final generalization yet.
- Do not claim the online policy is ready.
- Do not hide strict-invalid safety failures.
