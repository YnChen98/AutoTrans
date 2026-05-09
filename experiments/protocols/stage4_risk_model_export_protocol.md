# Stage 4-H1 LogisticRegression JSON Export Protocol

## Purpose

Stage 4-H1 exports the offline Stage 4 risk predictor into an inspectable JSON
format before any online ROS adapter integration.

The export target is the current `LogisticRegression` baseline trained from:

- dataset: `experiments/datasets/stage4_risk_dataset.csv`
- label: `label_strict_invalid`
- feature_set: `early`
- drop_command_scale_features: `true`
- drop_method_features: `true`

This step should verify that the model representation, feature order,
preprocessing, and probability calculation are reproducible outside sklearn.
It is not an online policy result.

## Why JSON First

JSON is preferred over pickle for the first implementation because it is
human-readable, language-neutral, and easier to audit before connecting the
model to a ROS node.

Pickle, `.joblib`, and similar binary formats are convenient for Python-only
experiments, but they are less transparent and can depend on exact Python and
sklearn versions. For the first adapter-facing model format, the exported JSON
must show:

- feature order
- categorical one-hot handling
- missing-value handling
- imputation values
- `StandardScaler` means and standard deviations
- `LogisticRegression` coefficients and intercept
- training metadata and class counts
- `reference_predictions` with full-dataset sklearn reference probabilities

Generated model files are ignored by default and should not be committed unless
explicitly approved.

## Export Requirements

Use the dedicated Stage 4 sklearn venv:

```bash
source ~/venvs/autotrans-stage4/bin/activate
```

The export command must include `--export-train-on-all`. Without it,
`experiments/scripts/train_stage4_risk_predictor.py` exits with a clear error,
because the JSON file must represent a deliberate full-dataset training run
after normal evaluation.

Do not implement the online adapter until strict JSON-vs-sklearn reference
probability consistency is checked on representative dataset rows.

## Recommended Export Commands

3s early soft-warning candidate:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
source ~/venvs/autotrans-stage4/bin/activate
python3 experiments/scripts/train_stage4_risk_predictor.py --dataset experiments/datasets/stage4_risk_dataset.csv --label label_strict_invalid --feature-set early --max-early-window 3 --drop-command-scale-features --drop-method-features --export-logreg-json experiments/models/stage4_risk_logreg_3s.json --export-train-on-all --print-summary
```

5s early soft-warning candidate:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
source ~/venvs/autotrans-stage4/bin/activate
python3 experiments/scripts/train_stage4_risk_predictor.py --dataset experiments/datasets/stage4_risk_dataset.csv --label label_strict_invalid --feature-set early --max-early-window 5 --drop-command-scale-features --drop-method-features --export-logreg-json experiments/models/stage4_risk_logreg_5s.json --export-train-on-all --print-summary
```

15s offline/high-confidence monitoring candidate:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
source ~/venvs/autotrans-stage4/bin/activate
python3 experiments/scripts/train_stage4_risk_predictor.py --dataset experiments/datasets/stage4_risk_dataset.csv --label label_strict_invalid --feature-set early --max-early-window 15 --drop-command-scale-features --drop-method-features --export-logreg-json experiments/models/stage4_risk_logreg_15s.json --export-train-on-all --print-summary
```

## Generated Files

Generated model files should live under:

```bash
experiments/models/
```

The default ignored model patterns are:

```bash
experiments/models/*.json
experiments/models/*.pkl
experiments/models/*.joblib
```

Protocol files under `experiments/protocols/` are not ignored.

## Consistency Check Before ROS Integration

Before implementing an online adapter, compare JSON inference against sklearn
`predict_proba` on the same rows used for export.

New `--export-logreg-json --export-train-on-all` outputs include a
`reference_predictions` section. It contains one object per dataset row:

- `row_index`: zero-based row position in the CSV data rows
- `run_id`: copied from the dataset when available
- `label`: selected label value when available
- `sklearn_probability_positive`: `P(class=1)` from the exact fitted
  `LogisticRegression` pipeline that was exported

The check should verify:

- exact selected `feature_names` order
- identical categorical one-hot expansion
- identical missing-value imputation
- identical `StandardScaler` transform
- close probability agreement between JSON inference and sklearn reference
  probabilities

Only after this strict check passes should Stage 4-H move from offline export to
adapter implementation under `experiments/command_adaptation`. Online adapter
implementation is blocked until strict JSON-vs-sklearn reference probability
verification passes for the intended exported model files.

Stage 4-H2 adds a JSON-only checker for this gate:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/verify_stage4_logreg_json.py --dataset experiments/datasets/stage4_risk_dataset.csv --model-json experiments/models/stage4_risk_logreg_3s.json --print-summary
python3 experiments/scripts/verify_stage4_logreg_json.py --dataset experiments/datasets/stage4_risk_dataset.csv --model-json experiments/models/stage4_risk_logreg_5s.json --print-summary
python3 experiments/scripts/verify_stage4_logreg_json.py --dataset experiments/datasets/stage4_risk_dataset.csv --model-json experiments/models/stage4_risk_logreg_15s.json --print-summary
```

The checker reconstructs the feature vector from `feature_names` and
`preprocessing.feature_specs`, applies the exported median imputation and
`StandardScaler` statistics, and computes the `LogisticRegression` probability
directly from the JSON coefficients and intercept. It does not require
`sklearn`.

When `reference_predictions` exists, the checker matches rows by `row_index`,
reports `reference_probability_check: passed`, `max_abs_diff`,
`mean_abs_diff`, and `rows_compared`, and fails if `max_abs_diff` exceeds
`--max-abs-diff-tol` (`1e-8` by default). If an old JSON file does not contain
`reference_predictions`, the checker remains backward-compatible and reports
`reference_probability_check: not_available` plus
`json_inference_check: passed_without_sklearn_reference`. Missing required
dataset feature columns or reference probability mismatches must be fixed
before the model is considered adapter-ready.
