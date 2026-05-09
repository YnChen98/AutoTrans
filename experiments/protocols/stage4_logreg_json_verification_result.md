# Stage 4-H2 LogisticRegression JSON Verification Result

## Executive Summary

All three exported `LogisticRegression` JSON models passed strict JSON-vs-sklearn
reference probability checks:

- `experiments/models/stage4_risk_logreg_3s.json`
- `experiments/models/stage4_risk_logreg_5s.json`
- `experiments/models/stage4_risk_logreg_15s.json`

The maximum absolute probability differences are around `1e-16`, which is far
below the default `1e-8` tolerance used by
`experiments/scripts/verify_stage4_logreg_json.py`.

JSON-only inference is now trusted for downstream adapter integration. This
means the exported feature order, preprocessing, imputation, scaling,
coefficients, intercept, and probability calculation are consistent with the
sklearn reference probabilities embedded in the exported model files.

## Model Summary Table

| Model | Rows | Features | reference_probability_check | max_abs_diff | mean_abs_diff | Rows Compared | Accuracy @ 0.5 | Precision @ 0.5 | Recall @ 0.5 | F1 @ 0.5 |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `3s` | 90 | 16 | passed | 1.38777878078e-16 | 1.97372982156e-17 | 90 | 0.655555555556 | 0.566666666667 | 0.871794871795 | 0.686868686869 |
| `5s` | 90 | 27 | passed | 2.22044604925e-16 | 2.89891567541e-17 | 90 | 0.666666666667 | 0.576271186441 | 0.871794871795 | 0.693877551020 |
| `15s` | 90 | 49 | passed | 2.22044604925e-16 | 3.8395212935e-17 | 90 | 0.800000000000 | 0.818181818182 | 0.692307692308 | 0.750000000000 |

## Verification Interpretation

`reference_probability_check` passed for all three models. The JSON-only
inference path reproduced the sklearn reference probabilities with numerical
differences at floating-point roundoff scale.

No missing features or imputation failures were needed during verification. The
dataset rows contained the required exported feature inputs, and the checker was
able to reconstruct the model input vector for every compared row.

The generated JSON model files remain ignored by git and should not be
committed:

- `experiments/models/stage4_risk_logreg_3s.json`
- `experiments/models/stage4_risk_logreg_5s.json`
- `experiments/models/stage4_risk_logreg_15s.json`

## Research Decision

Stage 4-H2 is complete.

The next step can be Stage 4-H3 risk-conditioned adapter v0.

The first online adapter should use the `3s` and `5s` models for soft
intervention only. These horizons are early enough to support conservative
online command scaling, but their current threshold `0.5` metrics should be
treated as warning signals rather than final safety decisions.

The `15s` model is useful for offline diagnostics and higher-confidence
monitoring, but it may be too late for the first online adapter response.

## What Not To Claim

Do not claim online performance yet.

Do not claim a safety guarantee.

Do not claim hardware robustness.
