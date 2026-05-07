# Stage 4 Risk Predictor Group-CV And Ablation Result

## Executive Summary

Stage 4-D evaluates whether the 45-row Stage 4 risk predictor result survives stricter validation. The main result is that early dynamics remain predictive under leave-one-out and leave-one-method-out validation, but target generalization remains weak.

Dropping command-scale features and method/adaptation/policy identity features only mildly affects `LogisticRegression`. This suggests that command-scale leakage and method identity are not the main source of the observed performance.

Leave-one-target-out performance is much weaker than LOO and leave-one-method-out. The current bottleneck is target generalization, not model choice or command-scale metadata.

## Dataset And Model Setup

Dataset:

```bash
experiments/datasets/stage4_risk_dataset.csv
```

Dataset snapshot:

- Rows: 45
- Class 0 valid: 27
- Class 1 invalid: 18
- Targets: Trial 1, Trial 2, Trial 3
- Methods: `original`, `fixed_s085`, `windlevel_s085`
- Wind level: `strong`
- Target label: `label_invalid`
- Feature set: `early`

Model environment:

```bash
~/venvs/autotrans-stage4
```

Models:

- `LogisticRegression`
- `RandomForest`

Validation modes:

- `--cv loo`
- `--cv leave-one-target-out`
- `--cv leave-one-method-out`

Feature ablations:

- No ablation
- `--drop-command-scale-features`
- `--drop-method-features`
- `--drop-command-scale-features --drop-method-features`

## Result Table

| Setting | CV | Ablation | Model | Accuracy | Precision | Recall | F1 | AUROC | AUPRC | Brier |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | `loo` | none | `LogisticRegression` | 0.844444 | 0.823529 | 0.777778 | 0.800000 | 0.837449 | 0.860471 | 0.145346 |
| 1 | `loo` | none | `RandomForest` | 0.800000 | 0.800000 | 0.666667 | 0.727273 | 0.777778 | 0.811451 | 0.168795 |
| 2 | `leave-one-target-out` | none | `LogisticRegression` | 0.622222 | 0.545455 | 0.333333 | 0.413793 | 0.588477 | 0.602070 | 0.273460 |
| 2 | `leave-one-target-out` | none | `RandomForest` | 0.555556 | 0.250000 | 0.055556 | 0.090909 | 0.467078 | 0.434273 | 0.290366 |
| 3 | `leave-one-method-out` | none | `LogisticRegression` | 0.822222 | 0.750000 | 0.833333 | 0.789474 | 0.827160 | 0.823720 | 0.156238 |
| 3 | `leave-one-method-out` | none | `RandomForest` | 0.755556 | 0.705882 | 0.666667 | 0.685714 | 0.752058 | 0.753476 | 0.185973 |
| 4 | `loo` | `--drop-command-scale-features` | `LogisticRegression` | 0.844444 | 0.823529 | 0.777778 | 0.800000 | 0.839506 | 0.861429 | 0.145164 |
| 4 | `loo` | `--drop-command-scale-features` | `RandomForest` | 0.755556 | 0.705882 | 0.666667 | 0.685714 | 0.774691 | 0.801124 | 0.172034 |
| 5 | `loo` | `--drop-method-features` | `LogisticRegression` | 0.822222 | 0.750000 | 0.833333 | 0.789474 | 0.814815 | 0.808337 | 0.147624 |
| 5 | `loo` | `--drop-method-features` | `RandomForest` | 0.777778 | 0.750000 | 0.666667 | 0.705882 | 0.781893 | 0.807417 | 0.169722 |
| 6 | `loo` | both ablations | `LogisticRegression` | 0.822222 | 0.750000 | 0.833333 | 0.789474 | 0.814815 | 0.808337 | 0.147624 |
| 6 | `loo` | both ablations | `RandomForest` | 0.800000 | 0.800000 | 0.666667 | 0.727273 | 0.770576 | 0.796963 | 0.174212 |
| 7 | `leave-one-target-out` | both ablations | `LogisticRegression` | 0.733333 | 1.000000 | 0.333333 | 0.500000 | 0.561728 | 0.653674 | 0.239227 |
| 7 | `leave-one-target-out` | both ablations | `RandomForest` | 0.577778 | 0.333333 | 0.055556 | 0.095238 | 0.489712 | 0.433672 | 0.282536 |
| 8 | `leave-one-method-out` | both ablations | `LogisticRegression` | 0.822222 | 0.750000 | 0.833333 | 0.789474 | 0.827160 | 0.817302 | 0.153065 |
| 8 | `leave-one-method-out` | both ablations | `RandomForest` | 0.755556 | 0.705882 | 0.666667 | 0.685714 | 0.748971 | 0.740644 | 0.183655 |

## Interpretation

Command-scale leakage is not the main source of performance. Under LOO, `LogisticRegression` with `--drop-command-scale-features` keeps the same accuracy and F1 as the no-ablation run, with nearly identical AUROC, AUPRC, and Brier score.

Method identity is not the main source of performance. Under LOO, `LogisticRegression` with `--drop-method-features` still reaches accuracy `0.822222` and F1 `0.789474`, close to the no-ablation result.

`LogisticRegression` is more stable than `RandomForest` on this small dataset. It is stronger in the main LOO run, the leave-one-target-out run, and the leave-one-method-out run, and it changes less under ablation.

Target generalization is weak. Leave-one-target-out causes the largest degradation: no-ablation `LogisticRegression` drops from LOO F1 `0.800000` to leave-one-target-out F1 `0.413793`. Even with both ablations, leave-one-target-out recall remains `0.333333`, so the model is still not reliably detecting invalid runs on unseen targets.

Leave-one-method-out remains comparatively strong. With both ablations, `LogisticRegression` still reaches accuracy `0.822222`, recall `0.833333`, F1 `0.789474`, and AUROC `0.827160`. This suggests the early features are not only memorizing method labels.

## Current Research Decision

Do not move to a risk-conditioned online policy yet.

The next research priority is target diversity. The current predictor can support pipeline validation and offline diagnostics, but it is not ready to drive online adaptation because leave-one-target-out validation is still weak.

## Next Step

Stage 4-E should expand target diversity before adding risk-conditioned policy logic.

Recommended next actions:

- Add at least 3 new target points beyond Trial 1, Trial 2, and Trial 3.
- Keep repeated runs for `original`, `fixed_s085`, and `windlevel_s085`.
- Rebuild the Stage 4 risk dataset after expansion.
- Re-evaluate `--cv leave-one-target-out` after expansion.
- Re-run command-scale and method-feature ablations on the expanded dataset.

## What Not To Claim

- Do not claim target-general risk prediction yet.
- Do not claim the model is ready for online policy.
- Do not ignore the leave-one-target-out degradation.
- Do not treat the LOO result alone as evidence of robust generalization.
- Do not claim `policy_mode=wind_level` is final from these predictor results.
