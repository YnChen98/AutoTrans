#!/usr/bin/env python3
"""Build the Stage 4-Q1 formal main-run audit table."""

import argparse
import csv
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path
from types import SimpleNamespace


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from inspect_stage4_log_divergence import inspect_csv, parse_metrics_summary, resolve_path  # noqa: E402


METHOD_ORDER = ["original", "fixed_s085", "windlevel_s085", "risk_adapter_v1"]
TRIAL_ORDER = ["trial4", "trial5", "trial6"]
REPEAT_ORDER = list(range(1, 11))

MANUAL_FIELDS = [
    "manual_collision_observed",
    "manual_path_infeasible",
    "manual_obstacle_stop_observed",
    "manual_teleport_after_collision",
    "path_through_obstacle_observed",
    "path_feasibility_unknown",
    "annotation_confidence",
    "manual_failure_note",
]

AUDIT_FIELDS = [
    "trial",
    "method",
    "repeat",
    "run_name",
    "metrics_summary_path",
    "csv_path",
    "raw_valid_suggested",
    "strict_valid",
    "has_nan_state",
    "first_nan_time",
    "max_swing_angle_deg",
    "max_uav_speed",
    "max_payload_speed",
    "final_uav_xy_error",
    "command_invalid_count",
    "first_command_invalid_time",
    "command_saturation_count",
    "first_command_saturation_time",
    "sustained_command_saturation_count",
    "guarded_command_applied_count",
    "has_reference_ratio",
    "first_ref_nonfinite_time",
    "first_ref_pos_jump_gt1m_time",
    "first_ref_vel_jump_gt2mps_time",
    "trajectory_publish_count_final",
    "trajectory_update_count_final",
    "trajectory_updates_before_first_nan",
    "trajectory_updates_before_first_swing_ge_30",
    "failure_mode_guess",
    "first_command_nan_time",
    "first_state_divergence_time",
    "first_reference_jump_time",
    "reference_jump_after_divergence",
    "earliest_failure_group",
] + MANUAL_FIELDS


def parse_args():
    parser = argparse.ArgumentParser(
        description="Build the Stage 4-Q1 formal main-run audit CSV and Markdown summary."
    )
    parser.add_argument(
        "--metrics-dir",
        default="experiments/figures",
        help="Directory containing Stage 4 *_metrics_summary.txt files.",
    )
    parser.add_argument(
        "--manual-annotations",
        default="experiments/protocols/stage4o_manual_failure_annotations.json",
        help="Stage 4-O manual path/collision annotation JSON.",
    )
    parser.add_argument(
        "--output-csv",
        default="experiments/results/stage4_main_run_audit/stage4_main_run_audit.csv",
        help="Output audit CSV path.",
    )
    parser.add_argument(
        "--output-md",
        default="experiments/results/stage4_main_run_audit/stage4_main_run_audit_summary.md",
        help="Output Markdown summary path.",
    )
    parser.add_argument("--print-summary", action="store_true", help="Print concise audit summary.")
    return parser.parse_args()


def repo_path(path_text):
    path = Path(path_text).expanduser()
    if path.is_absolute():
        return path
    return (REPO_ROOT / path).resolve()


def repo_relative(path):
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def metrics_name(method, trial, repeat):
    return "stage4_%s_strong_%s_repeat%d_metrics_summary.txt" % (method, trial, repeat)


def run_name(method, trial, repeat):
    return "stage4_%s_strong_%s_repeat%d" % (method, trial, repeat)


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


def parse_bool(value):
    return str(value).strip().lower() in ("true", "1", "yes")


def bool_text(value):
    return "true" if value else "false"


def format_rate(numerator, denominator):
    if denominator == 0:
        return ""
    return "%.3f" % (float(numerator) / float(denominator))


def metric(metrics, key):
    return str(metrics.get(key, "")).strip()


def normalized_csv_key(path_text, base=None):
    if not path_text:
        return ""
    path = resolve_path(path_text, base=base)
    if not path:
        return str(path_text).strip()
    return str(path.resolve())


def strict_valid_from_metrics(metrics):
    raw_valid = parse_bool(metrics.get("valid_run_suggested", ""))
    has_nan = parse_bool(metrics.get("has_nan_state", ""))
    max_swing = parse_float(metrics.get("max_swing_angle_deg"))
    max_uav_speed = parse_float(metrics.get("max_uav_speed"))
    max_payload_speed = parse_float(metrics.get("max_payload_speed"))
    final_xy = parse_float(metrics.get("final_uav_xy_error"))
    tolerance = parse_float(metrics.get("target_xy_tolerance"))
    if not math.isfinite(tolerance):
        tolerance = 0.5
    return (
        raw_valid
        and not has_nan
        and math.isfinite(max_swing)
        and max_swing < 60.0
        and math.isfinite(max_uav_speed)
        and max_uav_speed < 4.0
        and math.isfinite(max_payload_speed)
        and max_payload_speed < 4.0
        and math.isfinite(final_xy)
        and final_xy <= tolerance
    )


def load_manual_annotations(path):
    if not path.exists():
        return {}, {}
    with path.open("r", encoding="utf-8") as annotation_file:
        payload = json.load(annotation_file)
    annotations = payload.get("annotations", [])
    if not isinstance(annotations, list):
        raise ValueError('manual annotations JSON must contain an "annotations" list')

    by_run_name = {}
    by_csv_path = {}
    for item in annotations:
        if not isinstance(item, dict):
            continue
        name = str(item.get("run_name", "")).strip()
        if name:
            by_run_name[name] = item
        csv_key = normalized_csv_key(item.get("csv_path", ""))
        if csv_key:
            by_csv_path[csv_key] = item
    return by_run_name, by_csv_path


def manual_value(annotation, field):
    if not annotation or field not in annotation:
        return ""
    value = annotation.get(field)
    if isinstance(value, bool):
        return bool_text(value)
    if value is None:
        return ""
    return str(value)


def manual_true(annotation, field):
    return parse_bool(manual_value(annotation, field))


def inspect_metrics(metrics, metrics_path):
    csv_path = resolve_path(metrics.get("csv_path"), base=metrics_path.parent)
    if not csv_path or not csv_path.exists():
        valid_text = str(metrics.get("valid_run_suggested", "")).strip().lower()
        has_nan_text = str(metrics.get("has_nan_state", "")).strip().lower()
        failure_mode = (
            "unknown_invalid"
            if valid_text in ("false", "0", "no") or has_nan_text in ("true", "1", "yes")
            else "no_divergence_detected"
        )
        return {
            "failure_mode_guess": failure_mode,
            "first_command_nan_time": "",
            "first_state_divergence_time": "",
            "first_reference_jump_time": "",
            "reference_jump_after_divergence": "",
        }

    inspector_args = SimpleNamespace(
        so3_thrust_saturation=59.9,
        bodyrate_xy_saturation=2.99,
        bodyrate_z_saturation=1.19,
    )
    row, _, _, _, _ = inspect_csv(csv_path, inspector_args, metrics=metrics)
    return row


def earliest_failure_group(strict_valid, failure_mode_guess, annotation):
    if strict_valid:
        return "valid_or_warning"
    if "reference_jump_before_command_nan" in failure_mode_guess or manual_true(
        annotation, "manual_path_infeasible"
    ) or manual_true(annotation, "manual_collision_observed"):
        return "planner_reference_upstream"
    if failure_mode_guess in ("command_saturation_before_nan", "command_nan_before_state_divergence"):
        return "command_control_upstream"
    if failure_mode_guess in (
        "state_divergence_before_command_nan",
        "strict_safety_no_nan",
        "target_error_only",
    ):
        return "state_task_upstream"
    return "unknown"


def build_audit_rows(metrics_dir, manual_by_run_name, manual_by_csv_path):
    rows = []
    for trial in TRIAL_ORDER:
        for method in METHOD_ORDER:
            for repeat in REPEAT_ORDER:
                name = metrics_name(method, trial, repeat)
                metrics_path = metrics_dir / name
                if not metrics_path.exists():
                    raise FileNotFoundError("missing formal metrics summary: %s" % metrics_path)

                metrics = parse_metrics_summary(metrics_path)
                run = run_name(method, trial, repeat)
                csv_key = normalized_csv_key(metrics.get("csv_path", ""), base=metrics_path.parent)
                annotation = manual_by_run_name.get(run) or manual_by_csv_path.get(csv_key) or {}
                inspector = inspect_metrics(metrics, metrics_path)
                strict_valid = strict_valid_from_metrics(metrics)
                failure_mode = str(inspector.get("failure_mode_guess", "")).strip()

                row = {
                    "trial": trial,
                    "method": method,
                    "repeat": str(repeat),
                    "run_name": run,
                    "metrics_summary_path": repo_relative(metrics_path),
                    "csv_path": metric(metrics, "csv_path"),
                    "raw_valid_suggested": metric(metrics, "valid_run_suggested"),
                    "strict_valid": bool_text(strict_valid),
                    "has_nan_state": metric(metrics, "has_nan_state"),
                    "first_nan_time": metric(metrics, "first_nan_time"),
                    "max_swing_angle_deg": metric(metrics, "max_swing_angle_deg"),
                    "max_uav_speed": metric(metrics, "max_uav_speed"),
                    "max_payload_speed": metric(metrics, "max_payload_speed"),
                    "final_uav_xy_error": metric(metrics, "final_uav_xy_error"),
                    "command_invalid_count": metric(metrics, "command_invalid_count"),
                    "first_command_invalid_time": metric(metrics, "first_command_invalid_time"),
                    "command_saturation_count": metric(metrics, "command_saturation_count"),
                    "first_command_saturation_time": metric(metrics, "first_command_saturation_time"),
                    "sustained_command_saturation_count": metric(
                        metrics, "sustained_command_saturation_count"
                    ),
                    "guarded_command_applied_count": metric(metrics, "guarded_command_applied_count"),
                    "has_reference_ratio": metric(metrics, "has_reference_ratio"),
                    "first_ref_nonfinite_time": metric(metrics, "first_ref_nonfinite_time"),
                    "first_ref_pos_jump_gt1m_time": metric(metrics, "first_ref_pos_jump_gt1m_time"),
                    "first_ref_vel_jump_gt2mps_time": metric(metrics, "first_ref_vel_jump_gt2mps_time"),
                    "trajectory_publish_count_final": metric(metrics, "trajectory_publish_count_final"),
                    "trajectory_update_count_final": metric(metrics, "trajectory_update_count_final"),
                    "trajectory_updates_before_first_nan": metric(
                        metrics, "trajectory_updates_before_first_nan"
                    ),
                    "trajectory_updates_before_first_swing_ge_30": metric(
                        metrics, "trajectory_updates_before_first_swing_ge_30"
                    ),
                    "failure_mode_guess": failure_mode,
                    "first_command_nan_time": str(inspector.get("first_command_nan_time", "")).strip(),
                    "first_state_divergence_time": str(
                        inspector.get("first_state_divergence_time", "")
                    ).strip(),
                    "first_reference_jump_time": str(
                        inspector.get("first_reference_jump_time", "")
                    ).strip(),
                    "reference_jump_after_divergence": str(
                        inspector.get("reference_jump_after_divergence", "")
                    ).strip(),
                }
                row["earliest_failure_group"] = earliest_failure_group(strict_valid, failure_mode, annotation)
                for field in MANUAL_FIELDS:
                    row[field] = manual_value(annotation, field)
                rows.append(row)
    return rows


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=AUDIT_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in AUDIT_FIELDS})


def markdown_table(fields, rows):
    lines = []
    lines.append("| " + " | ".join(fields) + " |")
    lines.append("| " + " | ".join(["---"] * len(fields)) + " |")
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def strict_by_method_trial(rows):
    table_rows = []
    for trial in TRIAL_ORDER:
        for method in METHOD_ORDER:
            selected = [row for row in rows if row["trial"] == trial and row["method"] == method]
            strict_count = sum(1 for row in selected if row["strict_valid"] == "true")
            total = len(selected)
            table_rows.append(
                {
                    "trial": trial,
                    "method": method,
                    "strict_valid": str(strict_count),
                    "total": str(total),
                    "strict_invalid": str(total - strict_count),
                    "strict_valid_rate": format_rate(strict_count, total),
                }
            )
    return table_rows


def aggregate_by_method(rows):
    table_rows = []
    for method in METHOD_ORDER:
        selected = [row for row in rows if row["method"] == method]
        strict_count = sum(1 for row in selected if row["strict_valid"] == "true")
        total = len(selected)
        table_rows.append(
            {
                "method": method,
                "strict_valid": str(strict_count),
                "total": str(total),
                "strict_invalid": str(total - strict_count),
                "strict_valid_rate": format_rate(strict_count, total),
            }
        )
    return table_rows


def count_rows(rows, field):
    return [
        {field: key, "count": str(count)}
        for key, count in sorted(Counter(row.get(field, "") or "blank" for row in rows).items())
    ]


def manual_count_rows(rows):
    fields = [
        "manual_collision_observed",
        "manual_path_infeasible",
        "manual_obstacle_stop_observed",
        "manual_teleport_after_collision",
        "path_through_obstacle_observed",
        "path_feasibility_unknown",
    ]
    table_rows = [{"manual_metric": "rows_with_any_annotation", "count": str(sum(any(row.get(field, "") for field in MANUAL_FIELDS) for row in rows))}]
    for field in fields:
        table_rows.append(
            {
                "manual_metric": "%s_true" % field,
                "count": str(sum(1 for row in rows if parse_bool(row.get(field, "")))),
            }
        )
    confidence_counts = Counter(row.get("annotation_confidence", "") or "blank" for row in rows)
    for confidence, count in sorted(confidence_counts.items()):
        table_rows.append({"manual_metric": "annotation_confidence_%s" % confidence, "count": str(count)})
    return table_rows


def build_markdown_summary(rows):
    strict_fields = ["trial", "method", "strict_valid", "total", "strict_invalid", "strict_valid_rate"]
    aggregate_fields = ["method", "strict_valid", "total", "strict_invalid", "strict_valid_rate"]
    count_fields = ["failure_mode_guess", "count"]
    group_fields = ["earliest_failure_group", "count"]
    manual_fields = ["manual_metric", "count"]
    return "\n".join(
        [
            "# Stage 4-Q1 Main Run Audit Summary",
            "",
            "## Scope",
            "",
            "This summary covers only the 120 formal Stage 4-J main repeats: `original`, `fixed_s085`, `windlevel_s085`, and `risk_adapter_v1` on strong-wind `trial4`, `trial5`, and `trial6`, with repeats `1` through `10`.",
            "",
            "Total rows: `%d`" % len(rows),
            "",
            "## Strict-Valid By Method And Trial",
            "",
            markdown_table(strict_fields, strict_by_method_trial(rows)),
            "",
            "## Aggregate Strict-Valid By Method",
            "",
            markdown_table(aggregate_fields, aggregate_by_method(rows)),
            "",
            "## `failure_mode_guess` Counts",
            "",
            markdown_table(count_fields, count_rows(rows, "failure_mode_guess")),
            "",
            "## `earliest_failure_group` Counts",
            "",
            markdown_table(group_fields, count_rows(rows, "earliest_failure_group")),
            "",
            "## Manual Annotation Counts",
            "",
            markdown_table(manual_fields, manual_count_rows(rows)),
            "",
            "## Caveat",
            "",
            "Manual annotations are incomplete and are used only when visual evidence exists. Empty manual fields mean no matched manual annotation was available; they do not prove that a path was feasible or collision-free.",
            "",
        ]
    )


def write_markdown(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(build_markdown_summary(rows), encoding="utf-8")


def print_summary(rows, output_csv, output_md):
    aggregate = aggregate_by_method(rows)
    print("Stage 4-Q1 main run audit")
    print("rows: %d" % len(rows))
    for row in aggregate:
        print(
            "%s: %s/%s strict-valid"
            % (row["method"], row["strict_valid"], row["total"])
        )
    for row in count_rows(rows, "earliest_failure_group"):
        print("%s: %s" % (row["earliest_failure_group"], row["count"]))
    print("output_csv: %s" % output_csv)
    print("output_md: %s" % output_md)


def main():
    args = parse_args()
    metrics_dir = repo_path(args.metrics_dir)
    manual_path = repo_path(args.manual_annotations)
    output_csv = repo_path(args.output_csv)
    output_md = repo_path(args.output_md)

    manual_by_run_name, manual_by_csv_path = load_manual_annotations(manual_path)
    rows = build_audit_rows(metrics_dir, manual_by_run_name, manual_by_csv_path)
    write_csv(output_csv, rows)
    write_markdown(output_md, rows)

    if args.print_summary:
        print_summary(rows, output_csv, output_md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
