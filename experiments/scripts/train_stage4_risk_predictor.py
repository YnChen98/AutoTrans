#!/usr/bin/env python3
"""Train and evaluate Stage 4-B failure-risk prediction baselines."""

import argparse
import csv
import json
import math
import sys
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]

SUPPORTED_LABELS = [
    "label_invalid",
    "label_nan",
    "label_target_fail",
    "label_speed_fail",
    "label_swing_fail",
]

METADATA_CATEGORICAL_FEATURES = [
    "method",
    "adaptation_mode",
    "policy_mode",
]

METADATA_NUMERIC_FEATURES = [
    "command_scale_expected",
    "wind_force_norm",
    "target_x",
    "target_y",
    "target_z",
    "payload_target_z",
]

NON_FEATURE_COLUMNS = set(
    [
        "run_id",
        "csv_path",
        "trial_name",
        "notes",
        "valid_run_suggested",
        "has_nan_state",
        "final_row_has_nan",
        "first_nan_time",
    ]
)

LEAKAGE_COLUMNS = set(
    [
        "nan_count_total",
        "final_uav_xy_error",
        "final_payload_xy_error",
        "final_uav_position_error_3d",
        "final_payload_position_error_3d",
        "mean_swing_angle_deg",
        "max_swing_angle_deg",
        "p95_swing_angle_deg",
        "max_uav_speed",
        "max_payload_speed",
        "mean_uav_speed",
        "mean_payload_speed",
        "uav_path_length",
        "payload_path_length",
        "mean_wind_force_norm",
        "max_wind_force_norm",
        "mean_command_speed_scale",
        "min_command_speed_scale",
        "max_command_speed_scale",
        "final_command_speed_scale",
        "sample_count",
        "duration_sec",
        "effective_log_rate_hz",
    ]
)

COMMAND_SCALE_FEATURE_TOKENS = [
    "command_speed_scale",
    "command_acceleration_scale",
    "command_scale",
    "command_scale_expected",
]

METHOD_FEATURE_PREFIXES = [
    "method__",
    "adaptation_mode__",
    "policy_mode__",
]

METHOD_FEATURE_NAMES = set(
    [
        "method",
        "adaptation_mode",
        "policy_mode",
        "command_scale_expected",
    ]
)


try:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    SKLEARN_AVAILABLE = True
    SKLEARN_IMPORT_ERROR = ""
except ImportError as exc:
    SKLEARN_AVAILABLE = False
    SKLEARN_IMPORT_ERROR = str(exc)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Train and evaluate Stage 4-B failure-risk prediction baselines."
    )
    parser.add_argument("--dataset", required=True, help="Path to a Stage 4 risk dataset CSV.")
    parser.add_argument(
        "--label",
        default="label_invalid",
        choices=SUPPORTED_LABELS,
        help="Binary target column to predict.",
    )
    parser.add_argument(
        "--output-dir",
        default="experiments/results/stage4_risk_predictor",
        help="Output directory for metrics_summary.json, predictions.csv, and feature_summary.csv.",
    )
    parser.add_argument(
        "--feature-set",
        default="all",
        choices=["basic", "early", "all"],
        help="Feature set to evaluate.",
    )
    parser.add_argument(
        "--cv",
        default="loo",
        choices=[
            "loo",
            "leave-one-target-out",
            "leave-one-method-out",
            "leave-one-trial-out",
        ],
        help="Cross-validation mode.",
    )
    parser.add_argument(
        "--drop-command-scale-features",
        action="store_true",
        help="Drop features whose names contain command scale tokens.",
    )
    parser.add_argument(
        "--drop-method-features",
        action="store_true",
        help="Drop method/adaptation/policy identity features.",
    )
    parser.add_argument("--print-summary", action="store_true", help="Print selected features and model details.")
    parser.add_argument("--dry-run", action="store_true", help="Run evaluation without writing output files.")
    return parser.parse_args()


def resolve_path(path_text):
    path = Path(path_text).expanduser()
    if path.is_absolute():
        return path
    cwd_path = (Path.cwd() / path).resolve()
    if cwd_path.exists():
        return cwd_path
    return (REPO_ROOT / path).resolve()


def parse_float(value):
    if value is None:
        return math.nan
    text = str(value).strip()
    if text == "":
        return math.nan
    try:
        return float(text)
    except ValueError:
        return math.nan


def parse_binary(value, field, run_id):
    text = str(value).strip().lower()
    if text in ("1", "true", "yes"):
        return 1
    if text in ("0", "false", "no"):
        return 0
    number = parse_float(value)
    if math.isfinite(number) and number in (0.0, 1.0):
        return int(number)
    raise ValueError("run_id=%s has non-binary %s=%r" % (run_id, field, value))


def format_number(value):
    if value is None:
        return "n/a"
    if isinstance(value, float) and math.isnan(value):
        return "n/a"
    if isinstance(value, float):
        return "%.6g" % value
    return str(value)


def clean_category(value):
    text = str(value).strip()
    if text == "":
        return "__missing__"
    return text


def sanitize_token(text):
    cleaned = []
    for char in str(text):
        if char.isalnum():
            cleaned.append(char)
        else:
            cleaned.append("_")
    token = "".join(cleaned).strip("_")
    return token or "missing"


def read_dataset(path):
    if not path.exists():
        raise FileNotFoundError("dataset does not exist: %s" % path)
    if path.stat().st_size == 0:
        raise ValueError("dataset is empty: %s" % path)
    with path.open("r", newline="", encoding="utf-8") as dataset_file:
        reader = csv.DictReader(dataset_file)
        if not reader.fieldnames:
            raise ValueError("dataset has no CSV header: %s" % path)
        rows = list(reader)
    if not rows:
        raise ValueError("dataset has no data rows: %s" % path)
    return rows, list(reader.fieldnames)


def selected_feature_specs(rows, fieldnames, feature_set):
    field_set = set(fieldnames)
    specs = []

    for column in METADATA_CATEGORICAL_FEATURES:
        if column not in field_set:
            continue
        categories = sorted({clean_category(row.get(column)) for row in rows})
        for category in categories:
            specs.append(
                {
                    "name": "%s__%s" % (column, sanitize_token(category)),
                    "kind": "categorical_onehot",
                    "source_column": column,
                    "category": category,
                }
            )

    for column in METADATA_NUMERIC_FEATURES:
        if column in field_set:
            specs.append(
                {
                    "name": column,
                    "kind": "numeric",
                    "source_column": column,
                    "category": "",
                }
            )

    if feature_set in ("early", "all"):
        early_columns = sorted(column for column in fieldnames if column.startswith("early_"))
        for column in early_columns:
            specs.append(
                {
                    "name": column,
                    "kind": "numeric",
                    "source_column": column,
                    "category": "",
                }
            )

    if not specs:
        raise ValueError("feature-set %s produced no usable feature columns" % feature_set)
    return specs


def is_command_scale_feature(spec):
    return any(token in spec["name"] for token in COMMAND_SCALE_FEATURE_TOKENS)


def is_method_feature(spec):
    name = spec["name"]
    source_column = spec["source_column"]
    return (
        any(name.startswith(prefix) for prefix in METHOD_FEATURE_PREFIXES)
        or name in METHOD_FEATURE_NAMES
        or source_column in METHOD_FEATURE_NAMES
    )


def apply_feature_ablations(specs, args):
    filtered = []
    dropped = []
    for spec in specs:
        reasons = []
        if args.drop_command_scale_features and is_command_scale_feature(spec):
            reasons.append("command_scale")
        if args.drop_method_features and is_method_feature(spec):
            reasons.append("method_identity")
        if reasons:
            dropped.append(
                {
                    "feature": spec["name"],
                    "source_column": spec["source_column"],
                    "reasons": reasons,
                }
            )
        else:
            filtered.append(spec)

    if not filtered:
        raise ValueError("feature ablation removed all usable feature columns")
    return filtered, dropped


def build_feature_matrix(rows, specs):
    matrix = []
    for row in rows:
        values = []
        for spec in specs:
            if spec["kind"] == "categorical_onehot":
                value = 1.0 if clean_category(row.get(spec["source_column"])) == spec["category"] else 0.0
            else:
                value = parse_float(row.get(spec["source_column"]))
            if not math.isfinite(value):
                values.append(math.nan)
            else:
                values.append(float(value))
        matrix.append(values)
    return matrix


def build_labels(rows, label_column):
    labels = []
    for index, row in enumerate(rows):
        run_id = row.get("run_id", "row_%d" % index)
        if label_column not in row:
            raise ValueError("dataset is missing label column: %s" % label_column)
        labels.append(parse_binary(row.get(label_column), label_column, run_id))
    return labels


def finite_values(values):
    return [value for value in values if math.isfinite(value)]


def mean(values):
    finite = finite_values(values)
    if not finite:
        return math.nan
    return sum(finite) / len(finite)


def stddev(values):
    finite = finite_values(values)
    if len(finite) < 2:
        return 0.0 if finite else math.nan
    average = sum(finite) / len(finite)
    return math.sqrt(sum((value - average) ** 2 for value in finite) / len(finite))


def median(values):
    finite = sorted(finite_values(values))
    if not finite:
        return 0.0
    midpoint = len(finite) // 2
    if len(finite) % 2 == 1:
        return finite[midpoint]
    return 0.5 * (finite[midpoint - 1] + finite[midpoint])


def summarize_features(specs, matrix):
    summaries = []
    for column_index, spec in enumerate(specs):
        values = [row[column_index] for row in matrix]
        finite = finite_values(values)
        summaries.append(
            {
                "feature": spec["name"],
                "kind": spec["kind"],
                "source_column": spec["source_column"],
                "category": spec["category"],
                "missing_count": len(values) - len(finite),
                "finite_count": len(finite),
                "mean": mean(values),
                "std": stddev(values),
                "min": min(finite) if finite else math.nan,
                "max": max(finite) if finite else math.nan,
            }
        )
    return summaries


def impute_train_test(matrix, train_indices, test_index):
    medians = []
    for column_index in range(len(matrix[0])):
        medians.append(median([matrix[row_index][column_index] for row_index in train_indices]))

    def impute_row(row):
        values = []
        for column_index, value in enumerate(row):
            if math.isfinite(value):
                values.append(value)
            else:
                values.append(medians[column_index])
        return values

    train_matrix = [impute_row(matrix[row_index]) for row_index in train_indices]
    test_vector = impute_row(matrix[test_index])
    return train_matrix, test_vector


def class_counts(labels):
    counts = Counter(labels)
    return {"0": counts.get(0, 0), "1": counts.get(1, 0)}


def nonempty_text(value):
    return str(value).strip() if value is not None else ""


def require_column(fieldnames, column, cv_mode):
    if column not in fieldnames:
        raise ValueError("cv %s requires dataset column: %s" % (cv_mode, column))


def trial_name_is_available(rows, fieldnames):
    return "trial_name" in fieldnames and all(nonempty_text(row.get("trial_name")) for row in rows)


def group_by_trial_name(rows, fieldnames, cv_mode):
    require_column(fieldnames, "trial_name", cv_mode)
    groups = []
    for index, row in enumerate(rows):
        group = nonempty_text(row.get("trial_name"))
        if not group:
            raise ValueError("cv %s found empty trial_name at row %d" % (cv_mode, index + 1))
        groups.append(group)
    return groups, "trial_name"


def group_by_method(rows, fieldnames, cv_mode):
    require_column(fieldnames, "method", cv_mode)
    groups = []
    for index, row in enumerate(rows):
        group = nonempty_text(row.get("method"))
        if not group:
            raise ValueError("cv %s found empty method at row %d" % (cv_mode, index + 1))
        groups.append(group)
    return groups, "method"


def group_by_target_xy(rows, fieldnames, cv_mode):
    require_column(fieldnames, "target_x", cv_mode)
    require_column(fieldnames, "target_y", cv_mode)
    groups = []
    for row in rows:
        groups.append("target_x=%s,target_y=%s" % (row.get("target_x", ""), row.get("target_y", "")))
    return groups, "target_x,target_y"


def group_values_for_cv(rows, fieldnames, cv_mode):
    if cv_mode == "leave-one-trial-out":
        return group_by_trial_name(rows, fieldnames, cv_mode)
    if cv_mode == "leave-one-method-out":
        return group_by_method(rows, fieldnames, cv_mode)
    if cv_mode == "leave-one-target-out":
        if trial_name_is_available(rows, fieldnames):
            return group_by_trial_name(rows, fieldnames, cv_mode)
        return group_by_target_xy(rows, fieldnames, cv_mode)
    raise ValueError("unsupported group cv mode: %s" % cv_mode)


def build_cv_folds(rows, fieldnames, cv_mode):
    if cv_mode == "loo":
        folds = []
        for test_index in range(len(rows)):
            folds.append(
                {
                    "fold": test_index + 1,
                    "held_out_group": "",
                    "train_indices": [index for index in range(len(rows)) if index != test_index],
                    "test_indices": [test_index],
                }
            )
        return folds, {"group_by": "", "held_out_groups": []}

    group_values, group_by = group_values_for_cv(rows, fieldnames, cv_mode)
    group_order = []
    grouped_indices = {}
    for index, group in enumerate(group_values):
        if group not in grouped_indices:
            grouped_indices[group] = []
            group_order.append(group)
        grouped_indices[group].append(index)
    if len(group_order) < 2:
        raise ValueError("cv %s requires at least two held-out groups" % cv_mode)

    folds = []
    all_indices = list(range(len(rows)))
    for fold_number, group in enumerate(group_order, start=1):
        test_indices = grouped_indices[group]
        test_set = set(test_indices)
        folds.append(
            {
                "fold": fold_number,
                "held_out_group": group,
                "train_indices": [index for index in all_indices if index not in test_set],
                "test_indices": test_indices,
            }
        )

    return folds, {"group_by": group_by, "held_out_groups": group_order}


def filter_usable_folds(folds, labels):
    used = []
    skipped = []
    for fold in folds:
        train_labels = [labels[index] for index in fold["train_indices"]]
        counts = class_counts(train_labels)
        if not train_labels:
            reason = "training fold is empty"
        elif counts["0"] == 0 or counts["1"] == 0:
            reason = "training fold has one class: class_0=%d class_1=%d" % (
                counts["0"],
                counts["1"],
            )
        else:
            reason = ""

        if reason:
            skipped.append(
                {
                    "fold": fold["fold"],
                    "held_out_group": fold["held_out_group"],
                    "reason": reason,
                }
            )
        else:
            used.append(fold)

    return used, skipped


def majority_probability(labels):
    if not labels:
        return 0.0
    return sum(labels) / float(len(labels))


def safe_probability(value):
    if value is None or not math.isfinite(value):
        return 0.0
    if value < 0.0:
        return 0.0
    if value > 1.0:
        return 1.0
    return float(value)


def sklearn_logistic_probability(x_train, y_train, x_test):
    if len(set(y_train)) < 2:
        return float(y_train[0]), "train fold has one class; used constant probability"
    model = make_pipeline(
        StandardScaler(),
        LogisticRegression(
            solver="liblinear",
            max_iter=1000,
            class_weight="balanced",
            random_state=0,
        ),
    )
    model.fit(x_train, y_train)
    probabilities = model.predict_proba([x_test])[0]
    classes = list(model.classes_)
    if 1 not in classes:
        return 0.0, "trained logistic model has no positive class"
    return safe_probability(float(probabilities[classes.index(1)])), ""


def sklearn_random_forest_probability(x_train, y_train, x_test):
    if len(set(y_train)) < 2:
        return float(y_train[0]), "train fold has one class; used constant probability"
    model = RandomForestClassifier(
        n_estimators=200,
        random_state=0,
        class_weight="balanced",
        min_samples_leaf=1,
    )
    model.fit(x_train, y_train)
    probabilities = model.predict_proba([x_test])[0]
    classes = list(model.classes_)
    if 1 not in classes:
        return 0.0, "trained random forest model has no positive class"
    return safe_probability(float(probabilities[classes.index(1)])), ""


def threshold_candidates(values):
    unique_values = sorted(set(finite_values(values)))
    if len(unique_values) < 2:
        return []
    return [
        0.5 * (unique_values[index - 1] + unique_values[index])
        for index in range(1, len(unique_values))
    ]


def score_predictions(labels, predictions):
    correct = sum(1 for label, prediction in zip(labels, predictions) if label == prediction)
    return correct / float(len(labels)) if labels else 0.0


def f1_from_labels(labels, predictions):
    tp = sum(1 for label, prediction in zip(labels, predictions) if label == 1 and prediction == 1)
    fp = sum(1 for label, prediction in zip(labels, predictions) if label == 0 and prediction == 1)
    fn = sum(1 for label, prediction in zip(labels, predictions) if label == 1 and prediction == 0)
    precision = tp / float(tp + fp) if (tp + fp) else 0.0
    recall = tp / float(tp + fn) if (tp + fn) else 0.0
    return 2.0 * precision * recall / (precision + recall) if (precision + recall) else 0.0


def threshold_probability(matrix, labels, feature_names, train_indices, test_index):
    y_train = [labels[row_index] for row_index in train_indices]
    prior = majority_probability(y_train)
    majority_label = 1 if prior >= 0.5 else 0
    best = None

    for column_index, feature_name in enumerate(feature_names):
        train_values = [matrix[row_index][column_index] for row_index in train_indices]
        candidates = threshold_candidates(train_values)
        if not candidates:
            continue
        for threshold in candidates:
            for direction in ("ge", "le"):
                predictions = []
                positive_group_labels = []
                negative_group_labels = []
                for value, label in zip(train_values, y_train):
                    if not math.isfinite(value):
                        prediction = majority_label
                    else:
                        is_positive_group = value >= threshold if direction == "ge" else value <= threshold
                        prediction = 1 if is_positive_group else 0
                        if is_positive_group:
                            positive_group_labels.append(label)
                        else:
                            negative_group_labels.append(label)
                    predictions.append(prediction)
                accuracy = score_predictions(y_train, predictions)
                f1_value = f1_from_labels(y_train, predictions)
                candidate = {
                    "accuracy": accuracy,
                    "f1": f1_value,
                    "feature_name": feature_name,
                    "column_index": column_index,
                    "threshold": threshold,
                    "direction": direction,
                    "positive_probability": majority_probability(positive_group_labels)
                    if positive_group_labels
                    else prior,
                    "negative_probability": majority_probability(negative_group_labels)
                    if negative_group_labels
                    else prior,
                }
                if best is None or (candidate["accuracy"], candidate["f1"]) > (best["accuracy"], best["f1"]):
                    best = candidate

    if best is None:
        return (
            safe_probability(prior),
            "no finite threshold candidate; used majority probability",
            majority_label,
        )

    value = matrix[test_index][best["column_index"]]
    if not math.isfinite(value):
        return safe_probability(prior), "test value missing; used majority probability", majority_label
    is_positive_group = value >= best["threshold"] if best["direction"] == "ge" else value <= best["threshold"]
    probability = best["positive_probability"] if is_positive_group else best["negative_probability"]
    predicted_label = 1 if is_positive_group else 0
    return safe_probability(probability), (
        "feature=%s direction=%s threshold=%.9g"
        % (best["feature_name"], best["direction"], best["threshold"])
    ), predicted_label


def evaluate_model(model_name, rows, matrix, labels, feature_names, folds, cv_mode):
    predictions = []
    warnings = []

    for fold in folds:
        train_indices = fold["train_indices"]
        y_train = [labels[index] for index in train_indices]
        for test_index in fold["test_indices"]:
            probability = majority_probability(y_train)
            forced_predicted_label = None
            detail = ""

            if model_name == "majority":
                detail = "train_positive_rate"
                forced_predicted_label = 1 if probability > 0.5 else 0
            elif model_name == "single_feature_threshold":
                probability, detail, forced_predicted_label = threshold_probability(
                    matrix,
                    labels,
                    feature_names,
                    train_indices,
                    test_index,
                )
            elif model_name in ("logistic_regression", "random_forest"):
                x_train, x_test = impute_train_test(matrix, train_indices, test_index)
                try:
                    if model_name == "logistic_regression":
                        probability, detail = sklearn_logistic_probability(x_train, y_train, x_test)
                    else:
                        probability, detail = sklearn_random_forest_probability(x_train, y_train, x_test)
                except Exception as exc:
                    probability = majority_probability(y_train)
                    detail = "model failed; used majority probability: %s" % exc
                    warnings.append("fold %d: %s" % (fold["fold"], detail))
            else:
                raise ValueError("unknown model: %s" % model_name)

            probability = safe_probability(probability)
            predicted_label = (
                forced_predicted_label
                if forced_predicted_label is not None
                else 1 if probability > 0.5 else 0
            )
            row = rows[test_index]
            predictions.append(
                {
                    "model": model_name,
                    "cv": cv_mode,
                    "fold": fold["fold"],
                    "held_out_group": fold["held_out_group"],
                    "run_id": row.get("run_id", "row_%d" % test_index),
                    "method": row.get("method", ""),
                    "label": labels[test_index],
                    "predicted_label": predicted_label,
                    "probability": probability,
                    "correct": 1 if predicted_label == labels[test_index] else 0,
                    "detail": detail,
                }
            )
    return predictions, warnings


def confusion_matrix(labels, predictions):
    tn = fp = fn = tp = 0
    for label, prediction in zip(labels, predictions):
        if label == 0 and prediction == 0:
            tn += 1
        elif label == 0 and prediction == 1:
            fp += 1
        elif label == 1 and prediction == 0:
            fn += 1
        elif label == 1 and prediction == 1:
            tp += 1
    return {"tn": tn, "fp": fp, "fn": fn, "tp": tp}


def auroc(labels, probabilities):
    positive_scores = [score for label, score in zip(labels, probabilities) if label == 1]
    negative_scores = [score for label, score in zip(labels, probabilities) if label == 0]
    if not positive_scores or not negative_scores:
        return None
    wins = 0.0
    for positive_score in positive_scores:
        for negative_score in negative_scores:
            if positive_score > negative_score:
                wins += 1.0
            elif positive_score == negative_score:
                wins += 0.5
    return wins / float(len(positive_scores) * len(negative_scores))


def auprc(labels, probabilities):
    positive_count = sum(labels)
    if positive_count == 0:
        return None
    grouped = []
    for score in sorted(set(probabilities), reverse=True):
        group_labels = [label for label, probability in zip(labels, probabilities) if probability == score]
        grouped.append((score, group_labels))
    tp = 0
    fp = 0
    previous_recall = 0.0
    area = 0.0
    for _score, group_labels in grouped:
        tp += sum(group_labels)
        fp += len(group_labels) - sum(group_labels)
        recall = tp / float(positive_count)
        precision = tp / float(tp + fp) if (tp + fp) else 0.0
        area += (recall - previous_recall) * precision
        previous_recall = recall
    return area


def brier_score(labels, probabilities):
    if not labels:
        return None
    return sum((probability - label) ** 2 for label, probability in zip(labels, probabilities)) / float(len(labels))


def compute_metrics(labels, prediction_rows):
    predicted_labels = [int(row["predicted_label"]) for row in prediction_rows]
    probabilities = [float(row["probability"]) for row in prediction_rows]
    matrix = confusion_matrix(labels, predicted_labels)
    tn = matrix["tn"]
    fp = matrix["fp"]
    fn = matrix["fn"]
    tp = matrix["tp"]
    total = len(labels)
    precision = tp / float(tp + fp) if (tp + fp) else 0.0
    recall = tp / float(tp + fn) if (tp + fn) else 0.0
    f1_value = 2.0 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    return {
        "accuracy": (tp + tn) / float(total) if total else 0.0,
        "precision": precision,
        "recall": recall,
        "f1": f1_value,
        "auroc": auroc(labels, probabilities),
        "auprc": auprc(labels, probabilities),
        "brier": brier_score(labels, probabilities),
        "confusion_matrix": matrix,
    }


def model_names():
    if SKLEARN_AVAILABLE:
        return ["majority", "logistic_regression", "random_forest"]
    return ["majority", "single_feature_threshold"]


def make_metrics_summary(
    args,
    dataset_path,
    output_dir,
    rows,
    labels,
    specs,
    feature_summaries,
    dropped_features,
    cv_summary,
    results,
):
    return {
        "dataset": str(dataset_path),
        "label": args.label,
        "feature_set": args.feature_set,
        "cv": args.cv,
        "folds_total": cv_summary["folds_total"],
        "folds_used": cv_summary["folds_used"],
        "folds_skipped": cv_summary["folds_skipped"],
        "group_by": cv_summary["group_by"],
        "held_out_groups": cv_summary["held_out_groups"],
        "skipped_folds": cv_summary["skipped_folds"],
        "row_count": len(rows),
        "class_counts": class_counts(labels),
        "feature_count": len(specs),
        "features": [spec["name"] for spec in specs],
        "drop_command_scale_features": args.drop_command_scale_features,
        "drop_method_features": args.drop_method_features,
        "dropped_features": dropped_features,
        "sklearn_available": SKLEARN_AVAILABLE,
        "sklearn_import_error": "" if SKLEARN_AVAILABLE else SKLEARN_IMPORT_ERROR,
        "leakage_avoidance": {
            "label_columns_excluded": SUPPORTED_LABELS,
            "non_feature_columns_excluded": sorted(NON_FEATURE_COLUMNS),
            "final_outcome_columns_excluded": sorted(LEAKAGE_COLUMNS),
        },
        "models": results,
        "feature_summary": feature_summaries,
        "dry_run": args.dry_run,
        "output_dir": str(output_dir),
    }


def json_ready(value):
    if isinstance(value, dict):
        return {key: json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_ready(item) for item in value]
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def write_metrics(path, summary):
    with path.open("w", encoding="utf-8") as output_file:
        json.dump(json_ready(summary), output_file, indent=2, sort_keys=True)
        output_file.write("\n")


def write_predictions(path, label_name, prediction_rows):
    fieldnames = [
        "model",
        "cv",
        "fold",
        "held_out_group",
        "run_id",
        "method",
        "label_name",
        "label",
        "predicted_label",
        "probability",
        "correct",
        "detail",
    ]
    with path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in prediction_rows:
            output_row = dict(row)
            output_row["label_name"] = label_name
            output_row["probability"] = "%.9g" % row["probability"]
            writer.writerow(output_row)


def write_feature_summary(path, feature_summaries):
    fieldnames = [
        "feature",
        "kind",
        "source_column",
        "category",
        "missing_count",
        "finite_count",
        "mean",
        "std",
        "min",
        "max",
    ]
    with path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        for summary in feature_summaries:
            writer.writerow(
                {
                    "feature": summary["feature"],
                    "kind": summary["kind"],
                    "source_column": summary["source_column"],
                    "category": summary["category"],
                    "missing_count": summary["missing_count"],
                    "finite_count": summary["finite_count"],
                    "mean": format_number(summary["mean"]),
                    "std": format_number(summary["std"]),
                    "min": format_number(summary["min"]),
                    "max": format_number(summary["max"]),
                }
            )


def print_terminal_summary(
    args,
    dataset_path,
    output_dir,
    labels,
    specs,
    dropped_features,
    cv_summary,
    results,
    feature_summaries,
):
    counts = class_counts(labels)
    print("Stage 4-B risk predictor baseline")
    print("dataset: %s" % dataset_path)
    print("label: %s" % args.label)
    print("rows: %d class_0=%d class_1=%d" % (len(labels), counts["0"], counts["1"]))
    print("feature_set: %s features=%d" % (args.feature_set, len(specs)))
    print(
        "ablations: drop_command_scale_features=%s drop_method_features=%s dropped_features=%d"
        % (
            "true" if args.drop_command_scale_features else "false",
            "true" if args.drop_method_features else "false",
            len(dropped_features),
        )
    )
    print("cv: %s" % args.cv)
    print("folds_used: %d" % cv_summary["folds_used"])
    print("folds_skipped: %d" % cv_summary["folds_skipped"])
    if args.cv != "loo":
        print("group_by: %s" % cv_summary["group_by"])
        print("held_out_groups: %s" % ", ".join(cv_summary["held_out_groups"]))
    print("sklearn_available: %s" % ("true" if SKLEARN_AVAILABLE else "false"))
    if not SKLEARN_AVAILABLE:
        print("sklearn_import_error: %s" % SKLEARN_IMPORT_ERROR)
    print("dry_run: %s" % ("true" if args.dry_run else "false"))
    if not args.dry_run:
        print("output_dir: %s" % output_dir)
    print("models:")
    for name in model_names():
        metrics = results[name]["metrics"]
        matrix = metrics["confusion_matrix"]
        print(
            "  %s: accuracy=%s precision=%s recall=%s f1=%s auroc=%s auprc=%s brier=%s cm[tn=%d fp=%d fn=%d tp=%d]"
            % (
                name,
                format_number(metrics["accuracy"]),
                format_number(metrics["precision"]),
                format_number(metrics["recall"]),
                format_number(metrics["f1"]),
                format_number(metrics["auroc"]),
                format_number(metrics["auprc"]),
                format_number(metrics["brier"]),
                matrix["tn"],
                matrix["fp"],
                matrix["fn"],
                matrix["tp"],
            )
        )
        if results[name]["warnings"]:
            print("    warnings: %d fold warning(s)" % len(results[name]["warnings"]))
    if args.print_summary:
        print("selected_features:")
        for summary in feature_summaries:
            print(
                "  %s kind=%s missing=%d"
                % (summary["feature"], summary["kind"], summary["missing_count"])
            )


def main():
    args = parse_args()
    try:
        dataset_path = resolve_path(args.dataset)
        output_dir = resolve_path(args.output_dir)
        rows, fieldnames = read_dataset(dataset_path)
        labels = build_labels(rows, args.label)
        counts = class_counts(labels)
        if len(labels) < 2:
            raise ValueError("dataset must contain at least two rows for cross-validation")
        if counts["0"] == 0 or counts["1"] == 0:
            raise ValueError(
                "label %s has only one class: class_0=%d class_1=%d"
                % (args.label, counts["0"], counts["1"])
            )
        specs = selected_feature_specs(rows, fieldnames, args.feature_set)
        specs, dropped_features = apply_feature_ablations(specs, args)
        matrix = build_feature_matrix(rows, specs)
        feature_names = [spec["name"] for spec in specs]
        feature_summaries = summarize_features(specs, matrix)
        folds, group_summary = build_cv_folds(rows, fieldnames, args.cv)
        usable_folds, skipped_folds = filter_usable_folds(folds, labels)
        cv_summary = {
            "folds_total": len(folds),
            "folds_used": len(usable_folds),
            "folds_skipped": len(skipped_folds),
            "group_by": group_summary["group_by"],
            "held_out_groups": group_summary["held_out_groups"],
            "skipped_folds": skipped_folds,
        }
        for skipped in skipped_folds:
            group_text = (
                " held_out_group=%s" % skipped["held_out_group"]
                if skipped["held_out_group"]
                else ""
            )
            print(
                "WARNING: skipping fold %d%s: %s"
                % (skipped["fold"], group_text, skipped["reason"]),
                file=sys.stderr,
            )
        if not usable_folds:
            raise ValueError(
                "all folds were skipped for cv %s because no training fold had both classes"
                % args.cv
            )

        all_predictions = []
        results = {}
        for name in model_names():
            prediction_rows, warnings = evaluate_model(
                name,
                rows,
                matrix,
                labels,
                feature_names,
                usable_folds,
                args.cv,
            )
            all_predictions.extend(prediction_rows)
            results[name] = {
                "metrics": compute_metrics([int(row["label"]) for row in prediction_rows], prediction_rows),
                "warnings": warnings,
            }

        metrics_summary = make_metrics_summary(
            args,
            dataset_path,
            output_dir,
            rows,
            labels,
            specs,
            feature_summaries,
            dropped_features,
            cv_summary,
            results,
        )

        print_terminal_summary(
            args,
            dataset_path,
            output_dir,
            labels,
            specs,
            dropped_features,
            cv_summary,
            results,
            feature_summaries,
        )

        if not args.dry_run:
            output_dir.mkdir(parents=True, exist_ok=True)
            write_metrics(output_dir / "metrics_summary.json", metrics_summary)
            write_predictions(output_dir / "predictions.csv", args.label, all_predictions)
            write_feature_summary(output_dir / "feature_summary.csv", feature_summaries)

    except Exception as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
