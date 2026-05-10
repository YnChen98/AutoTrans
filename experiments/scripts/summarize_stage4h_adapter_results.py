#!/usr/bin/env python3
"""Summarize Stage 4-H limited-repeat adapter evaluation results."""

import argparse
import csv
import json
import math
import sys
from collections import defaultdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]

REQUIRED_FIELDS = [
    "trial_id",
    "target_x",
    "target_y",
    "method",
    "repeat_count",
    "valid_count",
    "invalid_count",
    "success_rate",
    "notes",
    "source_protocol_doc",
]

CSV_FIELDS = [
    "trial_id",
    "method",
    "valid_count",
    "repeat_count",
    "invalid_count",
    "success_rate",
    "notes",
]

METHOD_ORDER = [
    "original",
    "fixed_s085",
    "windlevel_s085",
    "risk_adapter_v0",
    "risk_adapter_v1",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate Stage 4-H adapter limited-evaluation summary tables."
    )
    parser.add_argument(
        "--manifest",
        default="experiments/protocols/stage4h_adapter_limited_eval_manifest.json",
        help="Input Stage 4-H adapter limited-evaluation manifest JSON.",
    )
    parser.add_argument(
        "--output-md",
        default="experiments/results/stage4h_adapter_limited_eval_summary.md",
        help="Output Markdown summary path.",
    )
    parser.add_argument(
        "--output-csv",
        default="experiments/results/stage4h_adapter_limited_eval_summary.csv",
        help="Output CSV summary path.",
    )
    parser.add_argument("--print-summary", action="store_true", help="Print a concise text summary.")
    return parser.parse_args()


def resolve_path(path_text):
    path = Path(path_text).expanduser()
    if path.is_absolute():
        return path
    return (REPO_ROOT / path).resolve()


def method_sort_key(method):
    if method in METHOD_ORDER:
        return (METHOD_ORDER.index(method), method)
    return (len(METHOD_ORDER), method)


def trial_sort_key(trial_id):
    text = str(trial_id)
    if text.startswith("trial"):
        suffix = text[len("trial") :]
        if suffix.isdigit():
            return (int(suffix), text)
    return (math.inf, text)


def format_rate(value):
    return "%.3f" % value


def format_count_rate(valid_count, repeat_count):
    if repeat_count == 0:
        return "n/a"
    return "%d/%d (%.1f%%)" % (valid_count, repeat_count, 100.0 * valid_count / repeat_count)


def load_manifest(path):
    if not path.exists():
        raise FileNotFoundError("manifest does not exist: %s" % path)
    with path.open("r", encoding="utf-8") as manifest_file:
        manifest = json.load(manifest_file)
    if not isinstance(manifest, dict):
        raise ValueError("manifest must be a JSON object")
    rows = manifest.get("results")
    if not isinstance(rows, list):
        raise ValueError('manifest must contain a "results" list')

    normalized_rows = []
    seen = set()
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise ValueError("results[%d] must be a JSON object" % index)
        missing = [field for field in REQUIRED_FIELDS if field not in row]
        if missing:
            raise ValueError("results[%d] missing required fields: %s" % (index, ", ".join(missing)))
        normalized = normalize_row(row, index)
        key = (normalized["trial_id"], normalized["method"])
        if key in seen:
            raise ValueError("duplicate trial/method entry: %s/%s" % key)
        seen.add(key)
        normalized_rows.append(normalized)
    if not normalized_rows:
        raise ValueError("manifest has no result rows")
    return normalized_rows


def normalize_row(row, index):
    normalized = dict(row)
    normalized["trial_id"] = str(row["trial_id"])
    normalized["method"] = str(row["method"])
    normalized["notes"] = str(row["notes"])
    normalized["source_protocol_doc"] = str(row["source_protocol_doc"])
    try:
        normalized["target_x"] = float(row["target_x"])
        normalized["target_y"] = float(row["target_y"])
        normalized["repeat_count"] = int(row["repeat_count"])
        normalized["valid_count"] = int(row["valid_count"])
        normalized["invalid_count"] = int(row["invalid_count"])
        normalized["success_rate"] = float(row["success_rate"])
    except (TypeError, ValueError) as exc:
        raise ValueError("results[%d] has invalid numeric fields: %s" % (index, exc))

    repeat_count = normalized["repeat_count"]
    valid_count = normalized["valid_count"]
    invalid_count = normalized["invalid_count"]
    success_rate = normalized["success_rate"]
    if repeat_count <= 0:
        raise ValueError("results[%d] repeat_count must be positive" % index)
    if valid_count < 0 or invalid_count < 0:
        raise ValueError("results[%d] valid_count/invalid_count must be non-negative" % index)
    if valid_count + invalid_count != repeat_count:
        raise ValueError("results[%d] valid_count + invalid_count must equal repeat_count" % index)
    expected_rate = valid_count / repeat_count
    if abs(success_rate - expected_rate) > 1e-9:
        raise ValueError(
            "results[%d] success_rate %.12g does not match valid_count/repeat_count %.12g"
            % (index, success_rate, expected_rate)
        )
    return normalized


def group_by_trial(rows):
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["trial_id"]].append(row)
    return {
        trial_id: sorted(trial_rows, key=lambda row: method_sort_key(row["method"]))
        for trial_id, trial_rows in grouped.items()
    }


def aggregate_by_method(rows):
    grouped = defaultdict(lambda: {"valid_count": 0, "repeat_count": 0, "invalid_count": 0, "trials": set()})
    for row in rows:
        item = grouped[row["method"]]
        item["valid_count"] += row["valid_count"]
        item["repeat_count"] += row["repeat_count"]
        item["invalid_count"] += row["invalid_count"]
        item["trials"].add(row["trial_id"])

    aggregate_rows = []
    for method, item in grouped.items():
        repeat_count = item["repeat_count"]
        aggregate_rows.append(
            {
                "method": method,
                "valid_count": item["valid_count"],
                "repeat_count": repeat_count,
                "invalid_count": item["invalid_count"],
                "success_rate": item["valid_count"] / repeat_count if repeat_count else math.nan,
                "trial_count": len(item["trials"]),
                "trials": sorted(item["trials"], key=trial_sort_key),
            }
        )
    return sorted(aggregate_rows, key=lambda row: method_sort_key(row["method"]))


def best_methods(rows):
    if not rows:
        return []
    best_rate = max(row["success_rate"] for row in rows)
    return [row for row in rows if abs(row["success_rate"] - best_rate) < 1e-12]


def markdown_table(headers, rows):
    lines = []
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for row in rows:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(lines)


def build_markdown(rows):
    grouped = group_by_trial(rows)
    aggregates = aggregate_by_method(rows)
    complete_trial_count = len(grouped)

    risk_v1 = next((row for row in aggregates if row["method"] == "risk_adapter_v1"), None)
    original = next((row for row in aggregates if row["method"] == "original"), None)
    fixed = next((row for row in aggregates if row["method"] == "fixed_s085"), None)
    windlevel = next((row for row in aggregates if row["method"] == "windlevel_s085"), None)

    lines = [
        "# Stage 4-H Adapter Limited Evaluation Summary",
        "",
        "## Executive Summary",
        "",
        "`risk_adapter_v1` is the best aggregate method in this limited-repeat strong-wind evaluation.",
    ]
    if risk_v1 and original and fixed and windlevel:
        lines.extend(
            [
                "",
                "Across Trial 4, Trial 5, and Trial 6, `risk_adapter_v1` achieved `%s`, compared with `%s` for `original`, `%s` for `fixed_s085`, and `%s` for `windlevel_s085`."
                % (
                    format_count_rate(risk_v1["valid_count"], risk_v1["repeat_count"]),
                    format_count_rate(original["valid_count"], original["repeat_count"]),
                    format_count_rate(fixed["valid_count"], fixed["repeat_count"]),
                    format_count_rate(windlevel["valid_count"], windlevel["repeat_count"]),
                ),
            ]
        )
    lines.extend(
        [
            "",
            "These results are limited-repeat and simulation-only. They should be used as evaluation evidence, not as a statistical or safety guarantee.",
            "",
            "## Per-Trial Comparison",
            "",
        ]
    )

    per_trial_rows = []
    for trial_id in sorted(grouped, key=trial_sort_key):
        for row in grouped[trial_id]:
            per_trial_rows.append(
                [
                    trial_id,
                    "%.1f" % row["target_x"],
                    "%.1f" % row["target_y"],
                    "`%s`" % row["method"],
                    "%d/%d" % (row["valid_count"], row["repeat_count"]),
                    format_rate(row["success_rate"]),
                    row["notes"],
                ]
            )
    lines.append(
        markdown_table(
            ["Trial", "`target_x`", "`target_y`", "Method", "Valid", "Success rate", "Notes"],
            per_trial_rows,
        )
    )

    best_lines = []
    for trial_id in sorted(grouped, key=trial_sort_key):
        winners = best_methods(grouped[trial_id])
        winner_text = ", ".join("`%s`" % row["method"] for row in winners)
        rate_text = format_rate(winners[0]["success_rate"]) if winners else "n/a"
        best_lines.append([trial_id, winner_text, rate_text])
    lines.extend(
        [
            "",
            "### Best Method Per Trial",
            "",
            markdown_table(["Trial", "Best method", "Success rate"], best_lines),
            "",
            "## Aggregate Comparison",
            "",
        ]
    )

    aggregate_table_rows = []
    for row in aggregates:
        coverage = "%d/%d trials" % (row["trial_count"], complete_trial_count)
        aggregate_table_rows.append(
            [
                "`%s`" % row["method"],
                "%d/%d" % (row["valid_count"], row["repeat_count"]),
                row["invalid_count"],
                format_rate(row["success_rate"]),
                coverage,
            ]
        )
    lines.append(
        markdown_table(
            ["Method", "Valid", "Invalid", "Success rate", "Coverage"],
            aggregate_table_rows,
        )
    )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "`risk_adapter_v1` is the best aggregate method over Trial 4, Trial 5, and Trial 6, with `13/15` valid runs.",
            "",
            "`fixed_s085` remains the best method on Trial 4 with `5/5` valid runs, while `risk_adapter_v1` achieved `4/5` on Trial 4.",
            "",
            "`risk_adapter_v1` is best on Trial 5 with `5/5` valid runs. On Trial 6, `risk_adapter_v1` matches `risk_adapter_v0` at `4/5` and beats the historical baselines.",
            "",
            "The Trial 4 repeat5 and Trial 6 repeat1 failures remain important. Trial 4 repeat5 suggests late risk detection; Trial 6 repeat1 suggests that early soft intervention or late hard-threshold detection can still be insufficient.",
            "",
            "## What Not To Claim",
            "",
            "- Do not claim statistical significance.",
            "- Do not claim a safety guarantee.",
            "- Do not claim final online robustness.",
            "- Do not hide the Trial 4 repeat5 and Trial 6 repeat1 failures.",
            "- Do not claim superiority over `fixed_s085` on every target, because `fixed_s085` remains best on Trial 4.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_csv(rows, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    sorted_rows = sorted(rows, key=lambda row: (trial_sort_key(row["trial_id"]), method_sort_key(row["method"])))
    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for row in sorted_rows:
            writer.writerow({field: row[field] for field in CSV_FIELDS})


def write_markdown(rows, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(build_markdown(rows), encoding="utf-8")


def print_summary(rows):
    grouped = group_by_trial(rows)
    aggregates = aggregate_by_method(rows)
    print("Stage 4-H adapter limited evaluation")
    for trial_id in sorted(grouped, key=trial_sort_key):
        winners = best_methods(grouped[trial_id])
        winner_text = ", ".join(row["method"] for row in winners)
        print("%s best: %s (%s)" % (trial_id, winner_text, format_rate(winners[0]["success_rate"])))
    for row in aggregates:
        if row["method"] == "risk_adapter_v1":
            print("risk_adapter_v1 aggregate: %s" % format_count_rate(row["valid_count"], row["repeat_count"]))
            break
    print("Notes: limited-repeat, simulation-only; fixed_s085 remains best on Trial 4.")


def main():
    args = parse_args()
    try:
        manifest_path = resolve_path(args.manifest)
        output_md_path = resolve_path(args.output_md)
        output_csv_path = resolve_path(args.output_csv)
        rows = load_manifest(manifest_path)
        write_markdown(rows, output_md_path)
        write_csv(rows, output_csv_path)
        if args.print_summary:
            print_summary(rows)
    except Exception as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
