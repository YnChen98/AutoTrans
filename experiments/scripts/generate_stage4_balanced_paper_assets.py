#!/usr/bin/env python3
"""Generate Stage 4 balanced paper-ready tables and figures."""

import argparse
import csv
import json
import math
import sys
from collections import defaultdict
from pathlib import Path
from types import SimpleNamespace


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from inspect_stage4_log_divergence import inspect_csv, parse_metrics_summary, resolve_path  # noqa: E402


METHOD_ORDER = ["original", "fixed_s085", "windlevel_s085", "risk_adapter_v1"]
TRIAL_ORDER = ["trial4", "trial5", "trial6"]
EXCLUDED_NAME_PREFIXES = (
    "stage4n3_",
    "stage4n4_",
    "stage4o3_",
    "stage4_rootcause_",
    "stage4_risk_adapter_v0_",
    "resetcheck",
    "smoke",
)

SUCCESS_FIELDS = [
    "trial",
    "method",
    "valid_count",
    "repeat_count",
    "invalid_count",
    "success_rate",
    "success_percent",
]
AGGREGATE_FIELDS = [
    "method",
    "total_valid",
    "total_repeats",
    "total_invalid",
    "aggregate_success_rate",
    "aggregate_success_percent",
    "rank",
]
FAILURE_FIELDS = [
    "trial",
    "method",
    "repeat",
    "strict_valid",
    "raw_valid_suggested",
    "has_nan_state",
    "failure_mode_guess",
    "first_nan_time",
    "max_swing_angle_deg",
    "max_uav_speed",
    "max_payload_speed",
    "final_uav_xy_error",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate paper-ready Stage 4 balanced comparison assets."
    )
    parser.add_argument(
        "--manifest",
        default="experiments/protocols/stage4h_adapter_limited_eval_manifest.json",
        help="Balanced Stage 4 adapter manifest JSON.",
    )
    parser.add_argument(
        "--metrics-dir",
        default="experiments/figures",
        help="Directory containing *_metrics_summary.txt files.",
    )
    parser.add_argument(
        "--output-dir",
        default="experiments/results/stage4_balanced_paper_assets",
        help="Output directory for generated CSV/Markdown/PNG assets.",
    )
    parser.add_argument("--print-summary", action="store_true", help="Print concise generation summary.")
    return parser.parse_args()


def repo_path(path_text):
    path = Path(path_text).expanduser()
    if path.is_absolute():
        return path
    return (REPO_ROOT / path).resolve()


def method_sort_key(method):
    if method in METHOD_ORDER:
        return (METHOD_ORDER.index(method), method)
    return (len(METHOD_ORDER), method)


def trial_sort_key(trial):
    if trial in TRIAL_ORDER:
        return (TRIAL_ORDER.index(trial), trial)
    return (len(TRIAL_ORDER), trial)


def format_rate(value):
    return "%.3f" % value


def format_percent(value):
    return "%.1f" % (100.0 * value)


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


def is_missing_or_nan(value):
    text = str(value or "").strip().lower()
    return text in ("", "nan", "+nan", "-nan")


def load_manifest(path):
    with path.open("r", encoding="utf-8") as manifest_file:
        manifest = json.load(manifest_file)
    rows = manifest.get("results")
    if not isinstance(rows, list):
        raise ValueError('manifest must contain a "results" list')
    selected = []
    for row in rows:
        trial = str(row.get("trial_id", ""))
        method = str(row.get("method", ""))
        if trial in TRIAL_ORDER and method in METHOD_ORDER:
            selected.append(row)
    expected = {(trial, method) for trial in TRIAL_ORDER for method in METHOD_ORDER}
    seen = {(str(row["trial_id"]), str(row["method"])) for row in selected}
    missing = sorted(expected - seen)
    if missing:
        raise ValueError("manifest missing balanced entries: %s" % missing)
    return sorted(selected, key=lambda row: (trial_sort_key(str(row["trial_id"])), method_sort_key(str(row["method"]))))


def build_success_rows(manifest_rows):
    rows = []
    for row in manifest_rows:
        repeat_count = int(row["repeat_count"])
        valid_count = int(row["valid_count"])
        invalid_count = int(row["invalid_count"])
        if repeat_count != 10:
            raise ValueError("%s/%s repeat_count must be 10" % (row["trial_id"], row["method"]))
        if valid_count + invalid_count != repeat_count:
            raise ValueError("%s/%s valid+invalid mismatch" % (row["trial_id"], row["method"]))
        rate = valid_count / repeat_count
        rows.append(
            {
                "trial": str(row["trial_id"]),
                "method": str(row["method"]),
                "valid_count": str(valid_count),
                "repeat_count": str(repeat_count),
                "invalid_count": str(invalid_count),
                "success_rate": format_rate(rate),
                "success_percent": format_percent(rate),
            }
        )
    return rows


def build_aggregate_rows(success_rows):
    grouped = defaultdict(lambda: {"valid": 0, "repeats": 0, "invalid": 0})
    for row in success_rows:
        item = grouped[row["method"]]
        item["valid"] += int(row["valid_count"])
        item["repeats"] += int(row["repeat_count"])
        item["invalid"] += int(row["invalid_count"])

    raw_rows = []
    for method in METHOD_ORDER:
        item = grouped[method]
        rate = item["valid"] / item["repeats"]
        raw_rows.append((method, item["valid"], item["repeats"], item["invalid"], rate))

    sorted_rows = sorted(raw_rows, key=lambda item: (-item[4], method_sort_key(item[0])))
    rows = []
    previous_rate = None
    rank = 0
    for index, (method, valid, repeats, invalid, rate) in enumerate(sorted_rows, start=1):
        if previous_rate is None or abs(rate - previous_rate) > 1.0e-12:
            rank = index
            previous_rate = rate
        rows.append(
            {
                "method": method,
                "total_valid": str(valid),
                "total_repeats": str(repeats),
                "total_invalid": str(invalid),
                "aggregate_success_rate": format_rate(rate),
                "aggregate_success_percent": format_percent(rate),
                "rank": str(rank),
            }
        )
    return rows


def metrics_name(method, trial, repeat):
    return "stage4_%s_strong_%s_repeat%d_metrics_summary.txt" % (method, trial, repeat)


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


def inspect_failure_mode(metrics, metrics_path):
    csv_path = resolve_path(metrics.get("csv_path"), base=metrics_path.parent)
    if not csv_path or not csv_path.exists():
        return "unknown_invalid" if parse_bool(metrics.get("has_nan_state", "")) else "no_divergence_detected"
    inspector_args = SimpleNamespace(
        so3_thrust_saturation=59.9,
        bodyrate_xy_saturation=2.99,
        bodyrate_z_saturation=1.19,
    )
    row, _, _, _, _ = inspect_csv(csv_path, inspector_args, metrics=metrics)
    return row.get("failure_mode_guess", "")


def build_failure_rows(metrics_dir):
    rows = []
    for trial in TRIAL_ORDER:
        for method in METHOD_ORDER:
            for repeat in range(1, 11):
                name = metrics_name(method, trial, repeat)
                if name.startswith(EXCLUDED_NAME_PREFIXES):
                    continue
                metrics_path = metrics_dir / name
                if not metrics_path.exists():
                    raise FileNotFoundError("missing metrics summary: %s" % metrics_path)
                metrics = parse_metrics_summary(metrics_path)
                strict_valid = strict_valid_from_metrics(metrics)
                rows.append(
                    {
                        "trial": trial,
                        "method": method,
                        "repeat": str(repeat),
                        "strict_valid": "true" if strict_valid else "false",
                        "raw_valid_suggested": str(metrics.get("valid_run_suggested", "")).strip(),
                        "has_nan_state": str(metrics.get("has_nan_state", "")).strip(),
                        "failure_mode_guess": inspect_failure_mode(metrics, metrics_path),
                        "first_nan_time": "" if is_missing_or_nan(metrics.get("first_nan_time")) else metrics.get("first_nan_time", ""),
                        "max_swing_angle_deg": metrics.get("max_swing_angle_deg", ""),
                        "max_uav_speed": metrics.get("max_uav_speed", ""),
                        "max_payload_speed": metrics.get("max_payload_speed", ""),
                        "final_uav_xy_error": metrics.get("final_uav_xy_error", ""),
                    }
                )
    return rows


def validate_failure_counts(success_rows, failure_rows):
    expected = {(row["trial"], row["method"]): int(row["valid_count"]) for row in success_rows}
    observed = defaultdict(int)
    for row in failure_rows:
        if row["strict_valid"] == "true":
            observed[(row["trial"], row["method"])] += 1
    mismatches = []
    for key, expected_count in sorted(expected.items()):
        if observed[key] != expected_count:
            mismatches.append("%s/%s expected %d observed %d" % (key[0], key[1], expected_count, observed[key]))
    if mismatches:
        raise ValueError("strict-valid counts do not match manifest: %s" % "; ".join(mismatches))


def write_csv(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def markdown_table(fields, rows):
    lines = []
    lines.append("| " + " | ".join(fields) + " |")
    lines.append("| " + " | ".join(["---"] * len(fields)) + " |")
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def write_markdown_table(path, title, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# %s" % title, "", markdown_table(fields, rows), ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def build_paper_summary(success_rows, aggregate_rows, failure_rows):
    failure_counts = defaultdict(int)
    for row in failure_rows:
        failure_counts[row["failure_mode_guess"]] += 1
    failure_count_rows = [
        {"failure_mode_guess": mode, "count": str(count)}
        for mode, count in sorted(failure_counts.items())
    ]
    return "\n".join(
        [
            "# Stage 4 Balanced Paper Summary",
            "",
            "## Executive Summary",
            "",
            "Stage 4 balanced Trial 4/5/6 comparison is complete for `original`, `fixed_s085`, `windlevel_s085`, and `risk_adapter_v1`.",
            "",
            "`risk_adapter_v1` achieved the best aggregate strict-valid rate: `23/30` (`76.7%`). `original` and `fixed_s085` are tied at `18/30` (`60.0%`), and `windlevel_s085` is `16/30` (`53.3%`).",
            "",
            "## Method-by-Trial Success Table",
            "",
            markdown_table(SUCCESS_FIELDS, success_rows),
            "",
            "## Aggregate Ranking",
            "",
            markdown_table(AGGREGATE_FIELDS, aggregate_rows),
            "",
            "## Run-Level Diagnostic Label Caveat",
            "",
            "The table below reports divergence-inspector labels over the 120 formal main-repeat runs. These labels are run-level diagnostic labels, not all failure modes.",
            "",
            "Some labels indicate valid or warning-only behavior rather than failures. `command_saturation_without_divergence` is not a failure by itself, `no_divergence_detected` is not a failure, and `swing_warning_no_nan` is warning-only. Paper-facing strict-valid / `label_strict_invalid` remains the primary success metric.",
            "",
            markdown_table(["failure_mode_guess", "count"], failure_count_rows),
            "",
            "## Paper-Facing Claim",
            "",
            "The learned risk-conditioned command adaptation achieved the best aggregate strict-valid rate in the balanced strong-wind Trial 4/5/6 simulation benchmark.",
            "",
            "Compared with the best non-risk baseline aggregate rate of `18/30` (`60.0%`), `risk_adapter_v1` achieved `23/30` (`76.7%`) under the same 30-repeat balanced strong-wind benchmark, while not outperforming every baseline on every target.",
            "",
            "Claims remain simulation-only and limited to this benchmark.",
            "",
            "## What Not To Claim",
            "",
            "- Do not claim statistical significance.",
            "- Do not claim safety guarantee.",
            "- Do not claim `risk_adapter_v1` is best on every target.",
            "- Do not claim all NaN/divergence failures are command-adaptation failures.",
            "- Do not use diagnostic smoke runs as main evaluation data.",
            "",
        ]
    )


def write_plot(path, aggregate_rows):
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as exc:
        print("warning: matplotlib unavailable; skipping plot: %s" % exc, file=sys.stderr)
        return False

    ordered = sorted(aggregate_rows, key=lambda row: method_sort_key(row["method"]))
    methods = [row["method"] for row in ordered]
    percents = [float(row["aggregate_success_percent"]) for row in ordered]
    colors = ["#5b6c8f", "#8a8d91", "#6f9f7a", "#b45f4d"]
    fig, ax = plt.subplots(figsize=(8.0, 4.8))
    bars = ax.bar(methods, percents, color=colors)
    ax.set_ylabel("Strict-valid success rate (%)")
    ax.set_ylim(0, 100)
    ax.set_title("Stage 4 balanced strong-wind success rate")
    ax.grid(axis="y", alpha=0.25)
    ax.set_axisbelow(True)
    for bar, percent in zip(bars, percents):
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            bar.get_height() + 2.0,
            "%.1f%%" % percent,
            ha="center",
            va="bottom",
            fontsize=9,
        )
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(str(path), dpi=200)
    plt.close(fig)
    return True


def main():
    args = parse_args()
    manifest_path = repo_path(args.manifest)
    metrics_dir = repo_path(args.metrics_dir)
    output_dir = repo_path(args.output_dir)

    manifest_rows = load_manifest(manifest_path)
    success_rows = build_success_rows(manifest_rows)
    aggregate_rows = build_aggregate_rows(success_rows)
    failure_rows = build_failure_rows(metrics_dir)
    validate_failure_counts(success_rows, failure_rows)

    write_csv(output_dir / "stage4_balanced_success_table.csv", SUCCESS_FIELDS, success_rows)
    write_markdown_table(
        output_dir / "stage4_balanced_success_table.md",
        "Stage 4 Balanced Success Table",
        SUCCESS_FIELDS,
        success_rows,
    )
    write_csv(output_dir / "stage4_balanced_aggregate_table.csv", AGGREGATE_FIELDS, aggregate_rows)
    write_markdown_table(
        output_dir / "stage4_balanced_aggregate_table.md",
        "Stage 4 Balanced Aggregate Table",
        AGGREGATE_FIELDS,
        aggregate_rows,
    )
    write_csv(output_dir / "stage4_balanced_failure_mode_table.csv", FAILURE_FIELDS, failure_rows)
    write_markdown_table(
        output_dir / "stage4_balanced_failure_mode_table.md",
        "Stage 4 Balanced Failure Mode Table",
        FAILURE_FIELDS,
        failure_rows,
    )
    (output_dir / "stage4_balanced_paper_summary.md").write_text(
        build_paper_summary(success_rows, aggregate_rows, failure_rows),
        encoding="utf-8",
    )
    plot_written = write_plot(output_dir / "stage4_balanced_success_rates.png", aggregate_rows)

    if args.print_summary:
        best = min(aggregate_rows, key=lambda row: int(row["rank"]))
        print("Stage 4 balanced paper assets")
        print("success_rows: %d" % len(success_rows))
        print("failure_rows: %d" % len(failure_rows))
        print(
            "aggregate_best: %s %s/%s (%s%%)"
            % (
                best["method"],
                best["total_valid"],
                best["total_repeats"],
                best["aggregate_success_percent"],
            )
        )
        print("plot_written: %s" % ("true" if plot_written else "false"))
        print("output_dir: %s" % output_dir)

    return 0


if __name__ == "__main__":
    sys.exit(main())
