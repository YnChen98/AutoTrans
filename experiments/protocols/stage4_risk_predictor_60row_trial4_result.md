# Stage 4 Risk Predictor 60-Row Trial 4 Result

## Executive Summary

Trial 4 expands the Stage 4 strong-wind risk dataset from 45 rows to 60 rows and increases target diversity across Trial 1, Trial 2, Trial 3, and Trial 4.

Trial 4 reveals a strong target-method interaction. `fixed_s085` succeeds on all Trial 4 repeats, while `windlevel_s085` succeeds on only one Trial 4 repeat.

Early dynamics remain predictive under leave-one-out and leave-one-method-out validation. Leave-one-target-out remains weak, so the current bottleneck is target generalization.

Command-scale features are not the main leakage source. Dropping command-scale features produces nearly identical `LogisticRegression` performance and only modest `RandomForest` changes.

## Dataset Snapshot

Dataset scope:

- Rows: 60
- Class 0 valid: 37
- Class 1 invalid: 23
- Targets: Trial 1, Trial 2, Trial 3, Trial 4
- Methods: `original`, `fixed_s085`, `windlevel_s085`
- Wind level: `strong`
- Target label: `label_invalid`
- Feature set: `early`

Method counts:

| Method | Rows | Valid | Invalid |
| --- | ---: | ---: | ---: |
| `original` | 20 | 13 | 7 |
| `fixed_s085` | 20 | 12 | 8 |
| `windlevel_s085` | 20 | 12 | 8 |

Overall method success rates:

| Method | Valid Runs | Invalid Runs | Success Rate |
| --- | ---: | ---: | ---: |
| `original` | 13/20 | 7/20 | 0.650000 |
| `fixed_s085` | 12/20 | 8/20 | 0.600000 |
| `windlevel_s085` | 12/20 | 8/20 | 0.600000 |

## Trial 4 Method Result

Trial 4 is a strong target-method interaction case.

| Method | Trial | Valid Runs | Invalid Runs | Success Rate |
| --- | --- | ---: | ---: | ---: |
| `original` | Trial 4 | 4/5 | 1/5 | 0.800000 |
| `fixed_s085` | Trial 4 | 5/5 | 0/5 | 1.000000 |
| `windlevel_s085` | Trial 4 | 1/5 | 4/5 | 0.200000 |

Trial 4 changes the method ranking relative to earlier targets. `windlevel_s085` remains an important candidate, but Trial 4 shows it can fail badly on some targets and should not be treated as a final method.

## Predictor Result Table

| Setting | CV | Ablation | Model | Accuracy | Precision | Recall | F1 | AUROC | AUPRC | Brier |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | `loo` | none | `LogisticRegression` | 0.800000 | 0.761905 | 0.695652 | 0.727273 | 0.726204 | 0.763603 | 0.170830 |
| 1 | `loo` | none | `RandomForest` | 0.766667 | 0.736842 | 0.608696 | 0.666667 | 0.794947 | 0.794919 | 0.161433 |
| 2 | `leave-one-target-out` | none | `LogisticRegression` | 0.650000 | 0.555556 | 0.434783 | 0.487805 | 0.532315 | 0.623435 | 0.282035 |
| 2 | `leave-one-target-out` | none | `RandomForest` | 0.683333 | 0.642857 | 0.391304 | 0.486486 | 0.572268 | 0.625080 | 0.228878 |
| 3 | `leave-one-method-out` | none | `LogisticRegression` | 0.750000 | 0.722222 | 0.565217 | 0.634146 | 0.766157 | 0.777767 | 0.179079 |
| 3 | `leave-one-method-out` | none | `RandomForest` | 0.733333 | 0.684211 | 0.565217 | 0.619048 | 0.747944 | 0.750075 | 0.181990 |
| 4 | `loo` | `--drop-command-scale-features` | `LogisticRegression` | 0.800000 | 0.761905 | 0.695652 | 0.727273 | 0.728555 | 0.765665 | 0.170768 |
| 4 | `loo` | `--drop-command-scale-features` | `RandomForest` | 0.766667 | 0.736842 | 0.608696 | 0.666667 | 0.771445 | 0.768309 | 0.168444 |
| 5 | `leave-one-target-out` | `--drop-command-scale-features` | `LogisticRegression` | 0.650000 | 0.555556 | 0.434783 | 0.487805 | 0.532315 | 0.623435 | 0.282031 |
| 5 | `leave-one-target-out` | `--drop-command-scale-features` | `RandomForest` | 0.683333 | 0.666667 | 0.347826 | 0.457143 | 0.553467 | 0.605376 | 0.233525 |
| 6 | `leave-one-method-out` | `--drop-command-scale-features` | `LogisticRegression` | 0.750000 | 0.722222 | 0.565217 | 0.634146 | 0.766157 | 0.777767 | 0.179253 |
| 6 | `leave-one-method-out` | `--drop-command-scale-features` | `RandomForest` | 0.716667 | 0.650000 | 0.565217 | 0.604651 | 0.757344 | 0.743773 | 0.181575 |
| 7 | `loo` | `--drop-command-scale-features --drop-method-features` | `LogisticRegression` | 0.822222 | 0.750000 | 0.833333 | 0.789474 | 0.814815 | 0.808337 | 0.147624 |
| 8 | `leave-one-target-out` | `--drop-command-scale-features --drop-method-features` | `LogisticRegression` | 0.733333 | 1.000000 | 0.333333 | 0.500000 | 0.561728 | 0.653674 | 0.239227 |
| 9 | `leave-one-method-out` | `--drop-command-scale-features --drop-method-features` | `LogisticRegression` | 0.822222 | 0.750000 | 0.833333 | 0.789474 | 0.827160 | 0.817302 | 0.153065 |

## Interpretation

LOO remains useful but optimistic. It confirms that early dynamics contain predictive signal, but it still mixes nearly identical target and method conditions between train and test folds.

Leave-one-method-out is acceptable for this stage. The no-ablation `LogisticRegression` result reaches F1 `0.634146`, and the no-ablation `RandomForest` result reaches F1 `0.619048`. These are weaker than LOO but still indicate that the early features are not only memorizing method identity.

Leave-one-target-out is still the bottleneck. No-ablation `LogisticRegression` drops to F1 `0.487805`, and no-ablation `RandomForest` reaches only F1 `0.486486`. This means the predictor is not yet target-general.

Command-scale features are not the main leakage source. Dropping command-scale features leaves `LogisticRegression` nearly unchanged across LOO, leave-one-target-out, and leave-one-method-out. This supports the interpretation that early dynamics are carrying the main signal.

Trial 4 makes method rankings target-dependent. The Trial 4 result favors `fixed_s085`, while earlier 45-row summaries favored `windlevel_s085` overall. This means method ranking should be reported per target and across repeated runs, not as a single final ordering.

## Research Decision

Do not move to a risk-conditioned online policy yet.

The next priority is target diversity expansion with Trial 5 and Trial 6. After adding those targets, rebuild the Stage 4 risk dataset and rerun LOO, leave-one-target-out, leave-one-method-out, and the command-scale/method-feature ablations.

The current predictor is useful for pipeline validation and offline diagnostics. It is not ready to drive online command adaptation.

## What Not To Claim

- Do not claim target-general prediction.
- Do not claim final model performance.
- Do not claim a final method ranking from Trial 4 or from the 60-row aggregate.
- Do not hide the Trial 4 `windlevel_s085` failures.
- Do not treat LOO alone as evidence of robust generalization.
- Do not move to risk-conditioned policy logic from this result alone.
