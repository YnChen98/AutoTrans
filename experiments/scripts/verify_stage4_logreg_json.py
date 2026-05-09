#!/usr/bin/env python3
"""Verify Stage 4 LogisticRegression JSON inference without sklearn."""

import argparse
import csv
import json
import math
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Verify exported Stage 4 LogisticRegression JSON inference on a "
            "dataset CSV without requiring sklearn."
        )
    )
    parser.add_argument("--dataset", required=True, help="Path to a Stage 4 risk dataset CSV.")
    parser.add_argument("--model-json", required=True, help="Path to an exported LogisticRegression JSON model.")
    parser.add_argument(
        "--max-abs-diff-tol",
        type=float,
        default=1e-8,
        help="Maximum allowed absolute difference when JSON contains reference probabilities.",
    )
    parser.add_argument("--print-summary", action="store_true", help="Print feature and comparison details.")
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


def parse_binary(value, field, row_index, run_id):
    text = str(value).strip().lower()
    if text in ("1", "true", "yes"):
        return 1
    if text in ("0", "false", "no"):
        return 0
    number = parse_float(value)
    if math.isfinite(number) and number in (0.0, 1.0):
        return int(number)
    raise ValueError(
        "row %d run_id=%s has non-binary %s=%r"
        % (row_index + 1, run_id, field, value)
    )


def clean_category(value):
    text = str(value).strip()
    if text == "":
        return "__missing__"
    return text


def format_number(value):
    if value is None:
        return "n/a"
    if isinstance(value, float) and math.isnan(value):
        return "n/a"
    if isinstance(value, float):
        return "%.12g" % value
    return str(value)


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


def load_model_json(path):
    if not path.exists():
        raise FileNotFoundError("model JSON does not exist: %s" % path)
    with path.open("r", encoding="utf-8") as model_file:
        model = json.load(model_file)
    validate_model_json(model)
    return model


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate_model_json(model):
    require(model.get("model", {}).get("type") == "LogisticRegression", "model JSON is not LogisticRegression")
    require(isinstance(model.get("feature_names"), list), "model JSON is missing feature_names list")
    preprocessing = model.get("preprocessing")
    require(isinstance(preprocessing, dict), "model JSON is missing preprocessing object")
    feature_specs = preprocessing.get("feature_specs")
    require(isinstance(feature_specs, list), "model JSON is missing preprocessing.feature_specs list")
    feature_names = model["feature_names"]
    require(len(feature_specs) == len(feature_names), "feature_specs length does not match feature_names length")

    for key in ("imputation_values", "mean_values", "standard_deviations"):
        values = preprocessing.get(key)
        require(isinstance(values, dict), "model JSON is missing preprocessing.%s object" % key)
        missing = [name for name in feature_names if name not in values]
        require(not missing, "preprocessing.%s is missing feature(s): %s" % (key, ", ".join(missing)))
        non_finite = [
            name
            for name in feature_names
            if not math.isfinite(parse_float(values.get(name)))
        ]
        require(
            not non_finite,
            "preprocessing.%s has non-finite value(s): %s" % (key, ", ".join(non_finite)),
        )

    coefficients = model.get("model", {}).get("coefficients")
    intercept = model.get("model", {}).get("intercept")
    require(isinstance(coefficients, list) and coefficients, "model JSON is missing model.coefficients")
    require(isinstance(coefficients[0], list), "model.coefficients[0] must be a list")
    require(len(coefficients[0]) == len(feature_names), "coefficient count does not match feature_count")
    non_finite_coefficients = [
        index
        for index, value in enumerate(coefficients[0])
        if not math.isfinite(parse_float(value))
    ]
    require(
        not non_finite_coefficients,
        "model.coefficients[0] has non-finite value(s) at index: %s"
        % ", ".join(str(index) for index in non_finite_coefficients),
    )
    require(isinstance(intercept, list) and intercept, "model JSON is missing model.intercept")
    require(
        math.isfinite(parse_float(intercept[0])),
        "model.intercept[0] is non-finite",
    )


def feature_value_from_row(spec, row):
    feature_name = spec.get("name", "")
    source_column = spec.get("source_column", "")
    kind = spec.get("kind", "")

    if kind == "categorical_onehot":
        if source_column in row:
            return 1.0 if clean_category(row.get(source_column)) == spec.get("category", "") else 0.0
        if feature_name in row:
            return parse_float(row.get(feature_name))
        return math.nan

    if source_column in row:
        return parse_float(row.get(source_column))
    if feature_name in row:
        return parse_float(row.get(feature_name))
    return math.nan


def validate_required_features(fieldnames, feature_specs):
    field_set = set(fieldnames)
    missing = []
    for spec in feature_specs:
        feature_name = spec.get("name", "")
        source_column = spec.get("source_column", "")
        kind = spec.get("kind", "")
        if kind == "categorical_onehot":
            if source_column not in field_set and feature_name not in field_set:
                missing.append("%s (source_column=%s)" % (feature_name, source_column))
        else:
            if source_column not in field_set and feature_name not in field_set:
                missing.append("%s (source_column=%s)" % (feature_name, source_column))
    if missing:
        raise ValueError(
            "dataset is missing required feature column(s): %s"
            % "; ".join(missing)
        )


def sigmoid(logit):
    if logit >= 0.0:
        exp_negative = math.exp(-logit)
        return 1.0 / (1.0 + exp_negative)
    exp_positive = math.exp(logit)
    return exp_positive / (1.0 + exp_positive)


def infer_row_probability(model, row):
    feature_names = model["feature_names"]
    preprocessing = model["preprocessing"]
    feature_specs = preprocessing["feature_specs"]
    imputation = preprocessing["imputation_values"]
    means = preprocessing["mean_values"]
    standard_deviations = preprocessing["standard_deviations"]
    coefficients = model["model"]["coefficients"][0]
    logit = float(model["model"]["intercept"][0])
    imputed_count = 0

    for index, spec in enumerate(feature_specs):
        feature_name = feature_names[index]
        value = feature_value_from_row(spec, row)
        if not math.isfinite(value):
            value = float(imputation[feature_name])
            imputed_count += 1
        mean_value = float(means[feature_name])
        std_value = float(standard_deviations[feature_name])
        scaled = (value - mean_value) / std_value if std_value else value - mean_value
        logit += float(coefficients[index]) * scaled

    return sigmoid(logit), imputed_count


def infer_probabilities(model, rows):
    probabilities = []
    imputed_counts = []
    for row in rows:
        probability, imputed_count = infer_row_probability(model, row)
        probabilities.append(probability)
        imputed_counts.append(imputed_count)
    return probabilities, imputed_counts


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


def metrics_at_threshold(labels, probabilities, threshold):
    predictions = [1 if probability >= threshold else 0 for probability in probabilities]
    matrix = confusion_matrix(labels, predictions)
    tp = matrix["tp"]
    fp = matrix["fp"]
    fn = matrix["fn"]
    tn = matrix["tn"]
    total = len(labels)
    precision = tp / float(tp + fp) if (tp + fp) else 0.0
    recall = tp / float(tp + fn) if (tp + fn) else 0.0
    f1_value = 2.0 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    return {
        "accuracy": (tp + tn) / float(total) if total else 0.0,
        "precision": precision,
        "recall": recall,
        "f1": f1_value,
        "confusion_matrix": matrix,
    }


def maybe_build_labels(model, rows, fieldnames):
    label_name = model.get("label", "")
    if not label_name or label_name not in fieldnames:
        return label_name, None
    labels = []
    for index, row in enumerate(rows):
        labels.append(parse_binary(row.get(label_name), label_name, index, row.get("run_id", "")))
    return label_name, labels


def parse_reference_row_index(value):
    if isinstance(value, bool):
        raise ValueError("reference_predictions row_index must be an integer")
    if isinstance(value, int):
        return value
    text = str(value).strip()
    if text == "":
        raise ValueError("reference_predictions row_index is empty")
    try:
        number = int(text)
    except ValueError:
        raise ValueError("reference_predictions row_index must be an integer: %r" % value)
    if str(number) != text and not (text.startswith("+") and str(number) == text[1:]):
        raise ValueError("reference_predictions row_index must be an integer: %r" % value)
    return number


def parse_reference_predictions(candidate, row_count):
    if not isinstance(candidate, list):
        raise ValueError("reference_predictions must be a list")

    probabilities = [math.nan] * row_count
    seen = set()
    for position, item in enumerate(candidate):
        if not isinstance(item, dict):
            raise ValueError("reference_predictions item %d must be an object" % position)
        if "row_index" not in item:
            raise ValueError("reference_predictions item %d is missing row_index" % position)
        if "sklearn_probability_positive" not in item:
            raise ValueError(
                "reference_predictions item %d is missing sklearn_probability_positive"
                % position
            )
        row_index = parse_reference_row_index(item.get("row_index"))
        if row_index < 0 or row_index >= row_count:
            raise ValueError(
                "reference_predictions row_index %d is outside dataset row range 0..%d"
                % (row_index, row_count - 1)
            )
        if row_index in seen:
            raise ValueError("reference_predictions has duplicate row_index %d" % row_index)
        probability = parse_float(item.get("sklearn_probability_positive"))
        if not math.isfinite(probability):
            raise ValueError(
                "reference_predictions row_index %d has non-finite sklearn_probability_positive"
                % row_index
            )
        probabilities[row_index] = probability
        seen.add(row_index)

    if len(seen) != row_count:
        missing = [str(index) for index in range(row_count) if index not in seen]
        raise ValueError(
            "reference_predictions is missing row_index value(s): %s"
            % ", ".join(missing)
        )
    return probabilities


def extract_reference_probabilities(model, rows):
    row_count = len(rows)
    if "reference_predictions" in model:
        return (
            "reference_predictions",
            parse_reference_predictions(model["reference_predictions"], row_count),
            row_count,
        )
    return "", None, 0


def compare_reference_probabilities(probabilities, reference_probabilities):
    differences = [
        abs(probability - reference_probability)
        for probability, reference_probability in zip(probabilities, reference_probabilities)
    ]
    max_diff = max(differences) if differences else 0.0
    mean_diff = sum(differences) / float(len(differences)) if differences else 0.0
    return max_diff, mean_diff, len(differences)


def print_report(args, dataset_path, model_path, model, probabilities, imputed_counts, label_name, labels, reference_result):
    row_count = len(probabilities)
    feature_count = len(model["feature_names"])
    print("Stage 4-H2 LogisticRegression JSON verifier")
    print("dataset: %s" % dataset_path)
    print("model_json: %s" % model_path)
    print("row_count: %d" % row_count)
    print("feature_count: %d" % feature_count)
    print("min_probability: %s" % format_number(min(probabilities)))
    print("max_probability: %s" % format_number(max(probabilities)))
    print("mean_probability: %s" % format_number(sum(probabilities) / float(row_count)))

    if labels is None:
        print("label: not_available%s" % ((" (%s)" % label_name) if label_name else ""))
    else:
        positive_count = sum(labels)
        metrics = metrics_at_threshold(labels, probabilities, 0.5)
        matrix = metrics["confusion_matrix"]
        print("label: %s" % label_name)
        print("label_positive_count: %d" % positive_count)
        print("label_negative_count: %d" % (len(labels) - positive_count))
        print("threshold: 0.5")
        print("accuracy: %s" % format_number(metrics["accuracy"]))
        print("precision: %s" % format_number(metrics["precision"]))
        print("recall: %s" % format_number(metrics["recall"]))
        print("f1: %s" % format_number(metrics["f1"]))
        print(
            "confusion_matrix: tn=%d fp=%d fn=%d tp=%d"
            % (matrix["tn"], matrix["fp"], matrix["fn"], matrix["tp"])
        )

    reference_name, reference_probabilities, max_diff, mean_diff, rows_compared = reference_result
    if reference_probabilities is None:
        print("reference_probability_check: not_available")
        print("json_inference_check: passed_without_sklearn_reference")
    else:
        print("reference_probability_check: passed")
        print("reference_probability_source: %s" % reference_name)
        print("max_abs_diff: %s" % format_number(max_diff))
        print("mean_abs_diff: %s" % format_number(mean_diff))
        print("rows_compared: %d" % rows_compared)
        print("max_abs_diff_tol: %s" % format_number(args.max_abs_diff_tol))

    if args.print_summary:
        imputed_rows = sum(1 for count in imputed_counts if count > 0)
        imputed_values = sum(imputed_counts)
        print("imputed_rows: %d" % imputed_rows)
        print("imputed_values: %d" % imputed_values)
        print("schema_version: %s" % model.get("schema_version", ""))
        print("feature_names:")
        for feature_name in model["feature_names"]:
            print("  %s" % feature_name)


def main():
    args = parse_args()
    try:
        if args.max_abs_diff_tol < 0.0 or not math.isfinite(args.max_abs_diff_tol):
            raise ValueError("--max-abs-diff-tol must be a finite non-negative number")

        dataset_path = resolve_path(args.dataset)
        model_path = resolve_path(args.model_json)
        rows, fieldnames = read_dataset(dataset_path)
        model = load_model_json(model_path)
        validate_required_features(fieldnames, model["preprocessing"]["feature_specs"])
        probabilities, imputed_counts = infer_probabilities(model, rows)
        label_name, labels = maybe_build_labels(model, rows, fieldnames)

        reference_name, reference_probabilities, rows_compared = extract_reference_probabilities(model, rows)
        max_diff = mean_diff = None
        if reference_probabilities is not None:
            max_diff, mean_diff, rows_compared = compare_reference_probabilities(
                probabilities,
                reference_probabilities,
            )
            if max_diff > args.max_abs_diff_tol:
                raise ValueError(
                    "JSON probability differs from reference probabilities: max_abs_diff=%s tol=%s"
                    % (format_number(max_diff), format_number(args.max_abs_diff_tol))
                )

        print_report(
            args,
            dataset_path,
            model_path,
            model,
            probabilities,
            imputed_counts,
            label_name,
            labels,
            (reference_name, reference_probabilities, max_diff, mean_diff, rows_compared),
        )
    except Exception as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
