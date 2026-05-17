#!/usr/bin/env python3
"""Generate Stage 4 protocol-split failure-mode paper assets."""

import argparse
import csv
import math
import sys
from collections import defaultdict
from pathlib import Path
from types import SimpleNamespace

import inspect_stage4_log_divergence as divergence_inspector


REPO_ROOT = Path(__file__).resolve().parents[2]

TRIALS = ["trial4", "trial5", "trial6"]
REPEATS = range(1, 11)

PROTOCOL_SINGLE = "single_goal_mission"
PROTOCOL_STRESS = "goal_reissue_stress"
PROTOCOL_ORDER = [PROTOCOL_SINGLE, PROTOCOL_STRESS]

SINGLE_GOAL_METHODS = [
    "original",
    "fixed_s085",
    "windlevel_s085",
    "fixed_s080",
    "risk_adapter_v1",
    "risk_adapter_v2",
    "risk_adapter_v21",
]
STRESS_METHODS = [
    "original",
    "fixed_s085",
    "windlevel_s085",
    "risk_adapter_v1",
    "fixed_s080",
    "risk_adapter_v21",
]
METHOD_ORDER = [
    "original",
    "fixed_s085",
    "windlevel_s085",
    "risk_adapter_v1",
    "fixed_s080",
    "risk_adapter_v2",
    "risk_adapter_v21",
]
FAILURE_GROUP_ORDER = [
    "valid_or_warning",
    "command_control_upstream",
    "planner_reference_upstream",
    "state_task_upstream",
    "unknown",
]
INVALID_FAILURE_GROUP_ORDER = [
    "command_control_upstream",
    "planner_reference_upstream",
    "state_task_upstream",
    "unknown",
]

EXPECTED_STRICT_VALID = {
    (PROTOCOL_SINGLE, "original"): 21,
    (PROTOCOL_SINGLE, "fixed_s085"): 22,
    (PROTOCOL_SINGLE, "windlevel_s085"): 26,
    (PROTOCOL_SINGLE, "fixed_s080"): 21,
    (PROTOCOL_SINGLE, "risk_adapter_v1"): 25,
    (PROTOCOL_SINGLE, "risk_adapter_v2"): 21,
    (PROTOCOL_SINGLE, "risk_adapter_v21"): 25,
    (PROTOCOL_STRESS, "original"): 18,
    (PROTOCOL_STRESS, "fixed_s085"): 18,
    (PROTOCOL_STRESS, "windlevel_s085"): 16,
    (PROTOCOL_STRESS, "risk_adapter_v1"): 23,
    (PROTOCOL_STRESS, "fixed_s080"): 24,
    (PROTOCOL_STRESS, "risk_adapter_v21"): 20,
}

RUN_FIELDS = [
    "protocol",
    "method",
    "trial",
    "repeat",
    "metrics_summary_path",
    "csv_path",
    "strict_valid",
    "raw_valid_suggested",
    "has_nan_state",
    "first_nan_time",
    "final_uav_xy_error",
    "max_swing_angle_deg",
    "max_uav_speed",
    "max_payload_speed",
    "arrival_detected",
    "first_arrival_time",
    "post_arrival_goal_received_count",
    "first_failure_after_arrival_flag",
    "mean_command_speed_scale",
    "min_command_speed_scale",
    "max_command_speed_scale",
    "failure_mode_guess",
    "failure_group",
    "first_command_nan_time",
    "first_state_divergence_time",
    "first_reference_jump_time",
    "reference_jump_after_divergence",
]

COUNT_FIELDS = [
    "protocol",
    "method",
    "failure_mode_guess",
    "count",
    "invalid_count",
    "strict_valid_count",
]

GROUP_FIELDS = [
    "protocol",
    "method",
    "failure_group",
    "count",
    "invalid_count",
    "strict_valid_count",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate Stage 4 protocol-split failure-mode paper assets."
    )
    parser.add_argument(
        "--metrics-dir",
        default="experiments/figures",
        help="Directory containing *_metrics_summary.txt files.",
    )
    parser.add_argument(
        "--output-dir",
        default="experiments/results/stage4_failure_mode_paper_assets",
        help="Output directory for generated CSV/Markdown/PNG assets.",
    )
    parser.add_argument(
        "--print-summary",
        action="store_true",
        help="Print concise generation summary.",
    )
    return parser.parse_args()


def repo_path(path_text):
    path = Path(path_text).expanduser()
    if path.is_absolute():
        return path
    return (REPO_ROOT / path).resolve()


def protocol_methods(protocol):
    if protocol == PROTOCOL_SINGLE:
        return SINGLE_GOAL_METHODS
    if protocol == PROTOCOL_STRESS:
        return STRESS_METHODS
    raise ValueError("unknown protocol: %s" % protocol)


def method_sort_key(method):
    if method in METHOD_ORDER:
        return (METHOD_ORDER.index(method), method)
    return (len(METHOD_ORDER), method)


def protocol_sort_key(protocol):
    if protocol in PROTOCOL_ORDER:
        return (PROTOCOL_ORDER.index(protocol), protocol)
    return (len(PROTOCOL_ORDER), protocol)


def trial_sort_key(trial):
    if trial in TRIALS:
        return (TRIALS.index(trial), trial)
    return (len(TRIALS), trial)


def failure_group_sort_key(group):
    if group in FAILURE_GROUP_ORDER:
        return (FAILURE_GROUP_ORDER.index(group), group)
    return (len(FAILURE_GROUP_ORDER), group)


def invalid_failure_group_sort_key(group):
    if group in INVALID_FAILURE_GROUP_ORDER:
        return (INVALID_FAILURE_GROUP_ORDER.index(group), group)
    return (len(INVALID_FAILURE_GROUP_ORDER), group)


def single_goal_candidates(method, trial, repeat):
    if method in ("original", "fixed_s085", "windlevel_s085", "risk_adapter_v1"):
        return [
            "stage4x_singlegoal_%s_strong_%s_goalrepeat1_repeat%d_metrics_summary.txt"
            % (method, trial, repeat)
        ]
    if method == "fixed_s080":
        names = []
        if trial == "trial4" and repeat <= 3:
            names.append(
                "stage4t2_fixed_s080_strong_trial4_goalrepeat1_repeat%d_metrics_summary.txt"
                % repeat
            )
        names.append(
            "stage4u_fixed_s080_strong_%s_goalrepeat1_repeat%d_metrics_summary.txt"
            % (trial, repeat)
        )
        return names
    if method == "risk_adapter_v2":
        names = []
        if trial == "trial4" and repeat <= 3:
            names.append(
                "stage4t2_risk_adapter_v2_strong_trial4_goalrepeat1_repeat%d_metrics_summary.txt"
                % repeat
            )
        names.append(
            "stage4u_risk_adapter_v2_strong_%s_goalrepeat1_repeat%d_metrics_summary.txt"
            % (trial, repeat)
        )
        return names
    if method == "risk_adapter_v21":
        return [
            "stage4v_risk_adapter_v21_strong_%s_goalrepeat1_screening_repeat%d_metrics_summary.txt"
            % (trial, repeat)
        ]
    raise ValueError("unknown single-goal method: %s" % method)


def stress_candidates(method, trial, repeat):
    if method == "fixed_s080":
        return [
            "stage4_fixed_s080_strong_%s_frontier_repeat%d_metrics_summary.txt"
            % (trial, repeat)
        ]
    if method == "risk_adapter_v21":
        return [
            "stage4x_risk_adapter_v21_goalreissue_strong_%s_goalrepeat10_repeat%d_metrics_summary.txt"
            % (trial, repeat)
        ]
    return [
        "stage4_%s_strong_%s_repeat%d_metrics_summary.txt" % (method, trial, repeat)
    ]


def metrics_candidates(protocol, method, trial, repeat):
    if protocol == PROTOCOL_SINGLE:
        return single_goal_candidates(method, trial, repeat)
    if protocol == PROTOCOL_STRESS:
        return stress_candidates(method, trial, repeat)
    raise ValueError("unknown protocol: %s" % protocol)


def resolve_metrics_path(metrics_dir, names):
    tried = []
    for name in names:
        path = metrics_dir / name
        tried.append(str(path))
        if path.exists():
            return path
    raise FileNotFoundError("missing metrics summary; tried: %s" % ", ".join(tried))


def parse_metrics_summary(path):
    metrics = {"metrics_path": str(path)}
    with path.open("r", encoding="utf-8") as metrics_file:
        for line in metrics_file:
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            metrics[key.strip()] = value.strip()
    return metrics


def parse_bool(value):
    return str(value).strip().lower() in ("true", "1", "yes")


def parse_float(value):
    text = str(value or "").strip()
    if not text:
        return math.nan
    try:
        return float(text)
    except ValueError:
        return math.nan


def finite_text(value):
    parsed = parse_float(value)
    if not math.isfinite(parsed):
        return ""
    return "%.6f" % parsed


def passthrough_text(value):
    text = str(value or "").strip()
    if text.lower() == "nan":
        return ""
    return text


def strict_valid_from_metrics(metrics):
    raw_valid = parse_bool(metrics.get("valid_run_suggested"))
    has_nan = parse_bool(metrics.get("has_nan_state"))
    max_swing = parse_float(metrics.get("max_swing_angle_deg"))
    max_uav_speed = parse_float(metrics.get("max_uav_speed"))
    max_payload_speed = parse_float(metrics.get("max_payload_speed"))
    final_xy = parse_float(metrics.get("final_uav_xy_error"))
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
        and final_xy <= 0.5
    )


def inspector_args():
    return SimpleNamespace(
        so3_thrust_saturation=59.9,
        bodyrate_xy_saturation=2.99,
        bodyrate_z_saturation=1.19,
    )


def inspect_metrics(metrics, metrics_path):
    csv_path = divergence_inspector.resolve_path(
        metrics.get("csv_path"), base=metrics_path.parent
    )
    if not csv_path or not csv_path.exists():
        row = {field: "" for field in divergence_inspector.OUTPUT_FIELDS}
        row.update(
            {
                "csv_path": str(csv_path) if csv_path else metrics.get("csv_path", ""),
                "metrics_path": str(metrics_path),
                "valid_run_suggested": metrics.get("valid_run_suggested", ""),
                "has_nan_state": metrics.get("has_nan_state", ""),
                "metrics_first_nan_time": metrics.get("first_nan_time", ""),
                "metrics_max_uav_speed": metrics.get("max_uav_speed", ""),
                "metrics_max_payload_speed": metrics.get("max_payload_speed", ""),
                "metrics_max_swing_angle_deg": metrics.get("max_swing_angle_deg", ""),
                "metrics_final_uav_xy_error": metrics.get("final_uav_xy_error", ""),
                "failure_mode_guess": (
                    "unknown_invalid"
                    if not strict_valid_from_metrics(metrics)
                    else "no_divergence_detected"
                ),
            }
        )
        return row
    row, _, _, _, _ = divergence_inspector.inspect_csv(
        csv_path, inspector_args(), metrics=metrics
    )
    return row


def target_or_no_arrival_failure(metrics, strict_valid):
    final_xy = parse_float(metrics.get("final_uav_xy_error"))
    arrival_detected = parse_bool(metrics.get("arrival_detected"))
    return (
        not strict_valid
        and not parse_bool(metrics.get("has_nan_state"))
        and (
            (math.isfinite(final_xy) and final_xy > 0.5)
            or not arrival_detected
        )
    )


def failure_group(protocol, strict_valid, metrics, inspector_row):
    mode = str(inspector_row.get("failure_mode_guess") or "").strip()
    command_modes = {
        "command_saturation_before_nan",
        "command_nan_before_state_divergence",
        "command_nan_coincident_with_state_divergence",
    }
    planner_modes = {
        "reference_jump_before_command_nan",
    }
    state_modes = {
        "state_divergence_before_command_nan",
        "strict_safety_no_nan",
        "target_error_only",
    }

    if strict_valid:
        return "valid_or_warning"
    if (
        protocol == PROTOCOL_STRESS
        and parse_bool(metrics.get("first_failure_after_arrival_flag"))
    ):
        return "planner_reference_upstream"
    if mode in command_modes:
        return "command_control_upstream"
    if mode in planner_modes:
        return "planner_reference_upstream"
    if mode in state_modes or target_or_no_arrival_failure(metrics, strict_valid):
        return "state_task_upstream"
    return "unknown"


def build_run_rows(metrics_dir):
    rows = []
    strict_counts = defaultdict(int)
    for protocol in PROTOCOL_ORDER:
        for method in protocol_methods(protocol):
            for trial in TRIALS:
                for repeat in REPEATS:
                    metrics_path = resolve_metrics_path(
                        metrics_dir,
                        metrics_candidates(protocol, method, trial, repeat),
                    )
                    metrics = parse_metrics_summary(metrics_path)
                    strict_valid = strict_valid_from_metrics(metrics)
                    if strict_valid:
                        strict_counts[(protocol, method)] += 1
                    inspector_row = inspect_metrics(metrics, metrics_path)
                    group = failure_group(protocol, strict_valid, metrics, inspector_row)
                    rows.append(
                        {
                            "protocol": protocol,
                            "method": method,
                            "trial": trial,
                            "repeat": str(repeat),
                            "metrics_summary_path": str(metrics_path),
                            "csv_path": passthrough_text(metrics.get("csv_path")),
                            "strict_valid": "true" if strict_valid else "false",
                            "raw_valid_suggested": passthrough_text(
                                metrics.get("valid_run_suggested")
                            ),
                            "has_nan_state": passthrough_text(metrics.get("has_nan_state")),
                            "first_nan_time": finite_text(metrics.get("first_nan_time")),
                            "final_uav_xy_error": finite_text(
                                metrics.get("final_uav_xy_error")
                            ),
                            "max_swing_angle_deg": finite_text(
                                metrics.get("max_swing_angle_deg")
                            ),
                            "max_uav_speed": finite_text(metrics.get("max_uav_speed")),
                            "max_payload_speed": finite_text(
                                metrics.get("max_payload_speed")
                            ),
                            "arrival_detected": passthrough_text(
                                metrics.get("arrival_detected")
                            ),
                            "first_arrival_time": finite_text(
                                metrics.get("first_arrival_time")
                            ),
                            "post_arrival_goal_received_count": passthrough_text(
                                metrics.get("post_arrival_goal_received_count")
                            ),
                            "first_failure_after_arrival_flag": passthrough_text(
                                metrics.get("first_failure_after_arrival_flag")
                            ),
                            "mean_command_speed_scale": finite_text(
                                metrics.get("mean_command_speed_scale")
                            ),
                            "min_command_speed_scale": finite_text(
                                metrics.get("min_command_speed_scale")
                            ),
                            "max_command_speed_scale": finite_text(
                                metrics.get("max_command_speed_scale")
                            ),
                            "failure_mode_guess": inspector_row.get(
                                "failure_mode_guess", ""
                            ),
                            "failure_group": group,
                            "first_command_nan_time": finite_text(
                                inspector_row.get("first_command_nan_time")
                            ),
                            "first_state_divergence_time": finite_text(
                                inspector_row.get("first_state_divergence_time")
                            ),
                            "first_reference_jump_time": finite_text(
                                inspector_row.get("first_reference_jump_time")
                            ),
                            "reference_jump_after_divergence": passthrough_text(
                                inspector_row.get("reference_jump_after_divergence")
                            ),
                        }
                    )
    for key, expected in EXPECTED_STRICT_VALID.items():
        observed = strict_counts[key]
        if observed != expected:
            raise ValueError(
                "%s/%s strict-valid mismatch: expected %d observed %d"
                % (key[0], key[1], expected, observed)
            )
    return rows


def build_count_rows(run_rows):
    grouped = defaultdict(lambda: {"count": 0, "invalid": 0, "valid": 0})
    for row in run_rows:
        key = (row["protocol"], row["method"], row["failure_mode_guess"])
        grouped[key]["count"] += 1
        if row["strict_valid"] == "true":
            grouped[key]["valid"] += 1
        else:
            grouped[key]["invalid"] += 1
    rows = []
    for (protocol, method, mode), counts in grouped.items():
        rows.append(
            {
                "protocol": protocol,
                "method": method,
                "failure_mode_guess": mode,
                "count": str(counts["count"]),
                "invalid_count": str(counts["invalid"]),
                "strict_valid_count": str(counts["valid"]),
            }
        )
    rows.sort(
        key=lambda row: (
            protocol_sort_key(row["protocol"]),
            method_sort_key(row["method"]),
            row["failure_mode_guess"],
        )
    )
    return rows


def build_group_rows(run_rows, invalid_only=False):
    grouped = defaultdict(lambda: {"count": 0, "invalid": 0, "valid": 0})
    for row in run_rows:
        if invalid_only and row["strict_valid"] == "true":
            continue
        key = (row["protocol"], row["method"], row["failure_group"])
        grouped[key]["count"] += 1
        if row["strict_valid"] == "true":
            grouped[key]["valid"] += 1
        else:
            grouped[key]["invalid"] += 1
    rows = []
    for (protocol, method, group), counts in grouped.items():
        rows.append(
            {
                "protocol": protocol,
                "method": method,
                "failure_group": group,
                "count": str(counts["count"]),
                "invalid_count": str(counts["invalid"]),
                "strict_valid_count": str(counts["valid"]),
            }
        )
    rows.sort(
        key=lambda row: (
            protocol_sort_key(row["protocol"]),
            method_sort_key(row["method"]),
            invalid_failure_group_sort_key(row["failure_group"])
            if invalid_only
            else failure_group_sort_key(row["failure_group"]),
        )
    )
    return rows


def write_csv(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def markdown_table(fields, rows):
    lines = ["| " + " | ".join(fields) + " |"]
    lines.append("| " + " | ".join(["---"] * len(fields)) + " |")
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def write_markdown_table(path, title, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# %s" % title, "", markdown_table(fields, rows), ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def compact_count_rows(count_rows):
    return [row for row in count_rows if int(row["count"]) > 0]


def build_summary(run_rows, count_rows, group_rows, invalid_group_rows):
    mode_summary = compact_count_rows(count_rows)
    total_runs = len(run_rows)
    invalid_runs = sum(1 for row in run_rows if row["strict_valid"] == "false")
    return "\n".join(
        [
            "# Stage 4-Z Failure-Mode Paper Summary",
            "",
            "## Executive Summary",
            "",
            "Stage 4-Z summarizes diagnostic failure groups for the completed protocol-split Stage 4 results. Strict-valid remains the paper-facing success metric; `failure_group` is a diagnostic grouping, not proof of physical root cause.",
            "",
            "The run table covers `%d` runs, including `%d` strict-invalid runs." % (total_runs, invalid_runs),
            "",
            "Single-goal mission results still show `windlevel_s085` as the strongest aggregate method, with `risk_adapter_v1` and `risk_adapter_v21` remaining competitive learned/risk-conditioned variants.",
            "",
            "Goal-reissue stress results still show `fixed_s080` as the strongest aggregate method, with `risk_adapter_v1` second and `risk_adapter_v21` below both `fixed_s080` and `risk_adapter_v1`.",
            "",
            "## Protocols And Methods Included",
            "",
            "- single-goal mission protocol: `goal_repeat=1`; methods `original`, `fixed_s085`, `windlevel_s085`, `fixed_s080`, `risk_adapter_v1`, `risk_adapter_v2`, `risk_adapter_v21`",
            "- goal-reissue stress protocol: `goal_repeat=10`; methods `original`, `fixed_s085`, `windlevel_s085`, `risk_adapter_v1`, `fixed_s080`, `risk_adapter_v21`",
            "",
            "## All-Run Failure Groups",
            "",
            "The full all-run table contains `valid_or_warning` rows for strict-valid runs. This is useful for accounting, but paper failure-analysis figures should use the invalid-only view below.",
            "",
            markdown_table(GROUP_FIELDS, group_rows),
            "",
            "## Invalid-Only Failure Groups",
            "",
            "Strict-valid runs are excluded from this table. Use `stage4_failure_group_invalid_only_stacked_bar.png` as the preferred paper-facing failure-analysis figure because it does not mix successful runs with diagnostic failure categories.",
            "",
            markdown_table(GROUP_FIELDS, invalid_group_rows),
            "",
            "## Failure-Mode Count Table By Protocol And Method",
            "",
            markdown_table(COUNT_FIELDS, mode_summary),
            "",
            "## Key Observations",
            "",
            "- In the single-goal mission protocol, `windlevel_s085` remains strongest overall; the learned variants `risk_adapter_v1` and `risk_adapter_v21` remain competitive but do not dominate.",
            "- In the goal-reissue stress protocol, `fixed_s080` remains strongest; `risk_adapter_v1` is second; `risk_adapter_v21` underperforms both `fixed_s080` and `risk_adapter_v1`.",
            "- `risk_adapter_v21` Trial 4 stress weakness and Trial 6 bottleneck require diagnosis before any new policy variant is justified.",
            "",
            "## Paper-Facing Caveats",
            "",
            "- Strict-valid remains the paper-facing metric.",
            "- `failure_group` is diagnostic and not perfect root-cause proof.",
            "- `command_saturation_without_divergence` is not a failure by itself.",
            "- `no_divergence_detected` can still coincide with target/no-arrival strict-invalid runs, so strict-valid overrides label interpretation.",
            "",
            "## What Not To Claim",
            "",
            "- Do not claim `risk_adapter_v21` is a cross-protocol winner.",
            "- Do not claim learned governors uniformly dominate heuristic/static baselines.",
            "- Do not make mixed-protocol aggregate claims.",
            "- Do not claim statistical significance.",
            "- Do not claim a safety guarantee.",
            "- Do not treat diagnostic labels as perfect root-cause proof.",
            "",
            "## Next Recommended Work",
            "",
            "- Inspect Trial 4 stress failures and Trial 6 bottlenecks using the run-level table.",
            "- Use the invalid-only failure-group figure to decide whether a phase-aware or failure-aware ablation is justified.",
            "- Do not create `risk_adapter_v22` until the failure-mode outputs are reviewed.",
            "",
        ]
    )


def write_group_plot(path, group_rows, group_order, title, y_limit=None):
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as exc:
        print("warning: matplotlib unavailable; skipping plot: %s" % exc, file=sys.stderr)
        return False

    colors = {
        "valid_or_warning": "#8a8d91",
        "command_control_upstream": "#b45f4d",
        "planner_reference_upstream": "#7f5fa8",
        "state_task_upstream": "#5b6c8f",
        "unknown": "#555555",
    }
    lookup = defaultdict(dict)
    for row in group_rows:
        lookup[(row["protocol"], row["method"])][row["failure_group"]] = int(row["count"])

    fig, axes = plt.subplots(1, 2, figsize=(13.5, 5.2), sharey=True)
    for ax, protocol, panel_title in [
        (axes[0], PROTOCOL_SINGLE, "single-goal mission"),
        (axes[1], PROTOCOL_STRESS, "goal-reissue stress"),
    ]:
        methods = protocol_methods(protocol)
        x_positions = list(range(len(methods)))
        bottoms = [0] * len(methods)
        for group in group_order:
            heights = [
                lookup[(protocol, method)].get(group, 0)
                for method in methods
            ]
            ax.bar(
                x_positions,
                heights,
                bottom=bottoms,
                label=group,
                color=colors.get(group, "#777777"),
            )
            bottoms = [bottom + height for bottom, height in zip(bottoms, heights)]
        ax.set_title(panel_title)
        ax.set_xticks(x_positions)
        ax.set_xticklabels(methods, rotation=45, ha="right")
        if y_limit is not None:
            ax.set_ylim(0, y_limit)
        ax.grid(axis="y", alpha=0.25)
        ax.set_axisbelow(True)
    axes[0].set_ylabel("Run count")
    handles, labels = axes[1].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.5, 0.02), ncol=3, frameon=False)
    fig.suptitle(title)
    fig.tight_layout(rect=(0, 0.08, 1, 0.95))
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(str(path), dpi=200)
    plt.close(fig)
    return True


def write_plot(path, group_rows):
    return write_group_plot(
        path,
        group_rows,
        FAILURE_GROUP_ORDER,
        "Stage 4 all-run failure-group distribution by protocol and method",
        y_limit=32,
    )


def write_invalid_only_plot(path, group_rows):
    max_total = 0
    totals = defaultdict(int)
    for row in group_rows:
        totals[(row["protocol"], row["method"])] += int(row["count"])
    if totals:
        max_total = max(totals.values())
    y_limit = max(10, max_total + 2)
    return write_group_plot(
        path,
        group_rows,
        INVALID_FAILURE_GROUP_ORDER,
        "Stage 4 invalid-only failure-group distribution by protocol and method",
        y_limit=y_limit,
    )


def main():
    args = parse_args()
    metrics_dir = repo_path(args.metrics_dir)
    output_dir = repo_path(args.output_dir)

    run_rows = build_run_rows(metrics_dir)
    count_rows = build_count_rows(run_rows)
    group_rows = build_group_rows(run_rows)
    invalid_group_rows = build_group_rows(run_rows, invalid_only=True)

    write_csv(output_dir / "stage4_failure_mode_run_table.csv", RUN_FIELDS, run_rows)
    write_markdown_table(
        output_dir / "stage4_failure_mode_run_table.md",
        "Stage 4 Failure-Mode Run Table",
        RUN_FIELDS,
        run_rows,
    )
    write_csv(output_dir / "stage4_failure_mode_count_table.csv", COUNT_FIELDS, count_rows)
    write_markdown_table(
        output_dir / "stage4_failure_mode_count_table.md",
        "Stage 4 Failure-Mode Count Table",
        COUNT_FIELDS,
        count_rows,
    )
    write_csv(output_dir / "stage4_failure_group_table.csv", GROUP_FIELDS, group_rows)
    write_markdown_table(
        output_dir / "stage4_failure_group_table.md",
        "Stage 4 Failure Group Table",
        GROUP_FIELDS,
        group_rows,
    )
    write_csv(
        output_dir / "stage4_failure_group_invalid_only_table.csv",
        GROUP_FIELDS,
        invalid_group_rows,
    )
    write_markdown_table(
        output_dir / "stage4_failure_group_invalid_only_table.md",
        "Stage 4 Invalid-Only Failure Group Table",
        GROUP_FIELDS,
        invalid_group_rows,
    )
    (output_dir / "stage4_failure_mode_summary.md").write_text(
        build_summary(run_rows, count_rows, group_rows, invalid_group_rows),
        encoding="utf-8",
    )
    plot_written = write_plot(
        output_dir / "stage4_failure_group_stacked_bar.png",
        group_rows,
    )
    invalid_plot_written = write_invalid_only_plot(
        output_dir / "stage4_failure_group_invalid_only_stacked_bar.png",
        invalid_group_rows,
    )

    if args.print_summary:
        print("Stage 4 failure-mode paper assets")
        print("run_rows: %d" % len(run_rows))
        print("failure_mode_rows: %d" % len(count_rows))
        print("failure_group_rows: %d" % len(group_rows))
        print("invalid_failure_group_rows: %d" % len(invalid_group_rows))
        print("plot_written: %s" % ("true" if plot_written else "false"))
        print(
            "invalid_plot_written: %s"
            % ("true" if invalid_plot_written else "false")
        )
        print("output_dir: %s" % output_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
