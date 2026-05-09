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

Do not implement the online adapter until JSON-vs-sklearn consistency is checked
on representative dataset rows.

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

The check should verify:

- exact selected `feature_names` order
- identical categorical one-hot expansion
- identical missing-value imputation
- identical `StandardScaler` transform
- close probability agreement between JSON inference and sklearn

Only after this consistency check should Stage 4-H move from offline export to
adapter implementation under `experiments/command_adaptation`.

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

If a future export includes stored sklearn reference probabilities, the checker
compares JSON-only probabilities against them using `--max-abs-diff-tol`
(`1e-8` by default). If no reference probabilities are present, it reports that
only JSON inference was checked. Missing required dataset feature columns must
be fixed before the model is considered adapter-ready.
