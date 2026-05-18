#!/usr/bin/env python3
"""Plot Stage 4-AA2 representative traces for mechanism diagnosis."""

import argparse
import csv
import math
import sys
from collections import defaultdict
from pathlib import Path

import generate_stage4_failure_mode_paper_assets as stage4z


REPO_ROOT = Path(__file__).resolve().parents[2]

PROTOCOL_SINGLE = "single_goal_mission"
PROTOCOL_STRESS = "goal_reissue_stress"
TRIAL4 = "trial4"
TRIAL6 = "trial6"
REPEATS = range(1, 11)

INDEX_FIELDS = [
    "selected_reason",
    "protocol",
    "method",
    "trial",
    "repeat",
    "metrics_summary_path",
    "csv_path",
    "strict_valid",
    "failure_mode_guess",
    "failure_group",
    "first_nan_time",
    "first_arrival_time",
    "arrival_detected",
    "final_uav_xy_error",
    "max_swing_angle_deg",
    "max_uav_speed",
    "max_payload_speed",
    "mean_command_speed_scale",
    "min_command_speed_scale",
    "max_command_speed_scale",
    "plot_path",
    "missing_columns",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate Stage 4-AA2 representative failure/success trace plots."
    )
    parser.add_argument(
        "--metrics-dir",
        default="experiments/figures",
        help="Directory containing *_metrics_summary.txt files.",
    )
    parser.add_argument(
        "--output-dir",
        default="experiments/results/stage4_representative_traces",
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


def strict_valid_text(strict_valid):
    return "true" if strict_valid else "false"


def run_row(protocol, method, trial, repeat, metrics_path):
    metrics = stage4z.parse_metrics_summary(metrics_path)
    strict_valid = stage4z.strict_valid_from_metrics(metrics)
    inspector_row = stage4z.inspect_metrics(metrics, metrics_path)
    failure_group = stage4z.failure_group(
        protocol, strict_valid, metrics, inspector_row
    )
    return {
        "selected_reason": "",
        "protocol": protocol,
        "method": method,
        "trial": trial,
        "repeat": str(repeat),
        "metrics_summary_path": str(metrics_path),
        "csv_path": stage4z.passthrough_text(metrics.get("csv_path")),
        "strict_valid": strict_valid_text(strict_valid),
        "failure_mode_guess": inspector_row.get("failure_mode_guess", ""),
        "failure_group": failure_group,
        "first_nan_time": stage4z.finite_text(metrics.get("first_nan_time")),
        "first_arrival_time": stage4z.finite_text(metrics.get("first_arrival_time")),
        "arrival_detected": stage4z.passthrough_text(metrics.get("arrival_detected")),
        "final_uav_xy_error": stage4z.finite_text(metrics.get("final_uav_xy_error")),
        "max_swing_angle_deg": stage4z.finite_text(
            metrics.get("max_swing_angle_deg")
        ),
        "max_uav_speed": stage4z.finite_text(metrics.get("max_uav_speed")),
        "max_payload_speed": stage4z.finite_text(metrics.get("max_payload_speed")),
        "mean_command_speed_scale": stage4z.finite_text(
            metrics.get("mean_command_speed_scale")
        ),
        "min_command_speed_scale": stage4z.finite_text(
            metrics.get("min_command_speed_scale")
        ),
        "max_command_speed_scale": stage4z.finite_text(
            metrics.get("max_command_speed_scale")
        ),
        "plot_path": "",
        "missing_columns": "",
    }


def build_rows_for(protocol, method, trial, metrics_dir):
    rows = []
    for repeat in REPEATS:
        metrics_path = stage4z.resolve_metrics_path(
            metrics_dir, stage4z.metrics_candidates(protocol, method, trial, repeat)
        )
        rows.append(run_row(protocol, method, trial, repeat, metrics_path))
    return rows


def parse_float(value):
    text = str(value or "").strip()
    if not text:
        return math.nan
    try:
        return float(text)
    except ValueError:
        return math.nan


def is_true(value):
    return str(value).strip().lower() == "true"


def quality_key(row):
    return (
        0 if row.get("failure_mode_guess") == "no_divergence_detected" else 1,
        parse_float(row.get("max_swing_angle_deg"))
        if math.isfinite(parse_float(row.get("max_swing_angle_deg")))
        else math.inf,
        parse_float(row.get("final_uav_xy_error"))
        if math.isfinite(parse_float(row.get("final_uav_xy_error")))
        else math.inf,
        parse_float(row.get("max_uav_speed"))
        if math.isfinite(parse_float(row.get("max_uav_speed")))
        else math.inf,
        parse_float(row.get("max_payload_speed"))
        if math.isfinite(parse_float(row.get("max_payload_speed")))
        else math.inf,
        int(row["repeat"]),
    )


def choose_valid_or_best(rows):
    valid_rows = [row for row in rows if is_true(row["strict_valid"])]
    if valid_rows:
        return sorted(valid_rows, key=quality_key)[0]
    return sorted(rows, key=quality_key)[0] if rows else None


def choose_invalid(rows, failure_group=None, failure_mode=None):
    candidates = [row for row in rows if not is_true(row["strict_valid"])]
    if failure_group:
        candidates = [
            row for row in candidates if row.get("failure_group") == failure_group
        ]
    if failure_mode:
        candidates = [
            row for row in candidates if row.get("failure_mode_guess") == failure_mode
        ]
    return sorted(candidates, key=lambda row: int(row["repeat"]))[0] if candidates else None


def add_selection(selected, row, reason):
    if row is None:
        return
    key = row["metrics_summary_path"]
    if key not in selected:
        selected[key] = dict(row)
        selected[key]["selected_reason"] = reason
        return
    existing = selected[key]["selected_reason"]
    if reason not in existing.split("; "):
        selected[key]["selected_reason"] = existing + "; " + reason


def select_representative_rows(metrics_dir):
    selected = {}

    v21_trial4 = build_rows_for(PROTOCOL_STRESS, "risk_adapter_v21", TRIAL4, metrics_dir)
    fixed_trial4 = build_rows_for(PROTOCOL_STRESS, "fixed_s080", TRIAL4, metrics_dir)
    v1_trial4 = build_rows_for(PROTOCOL_STRESS, "risk_adapter_v1", TRIAL4, metrics_dir)

    add_selection(
        selected,
        choose_valid_or_best(v21_trial4),
        "A: Trial 4 stress v21 strict-valid run",
    )
    add_selection(
        selected,
        choose_invalid(v21_trial4, failure_group="command_control_upstream"),
        "A: Trial 4 stress v21 command_control_upstream invalid run",
    )
    add_selection(
        selected,
        choose_invalid(v21_trial4, failure_group="state_task_upstream"),
        "A: Trial 4 stress v21 state_task_upstream invalid run",
    )
    add_selection(
        selected,
        choose_invalid(
            v21_trial4,
            failure_mode="command_nan_coincident_with_state_divergence",
        ),
        "A: Trial 4 stress v21 command_nan_coincident_with_state_divergence run",
    )

    add_selection(
        selected,
        choose_valid_or_best(fixed_trial4),
        "B: Trial 4 stress comparison fixed_s080 valid/near-best run",
    )
    add_selection(
        selected,
        choose_valid_or_best(v1_trial4),
        "B: Trial 4 stress comparison risk_adapter_v1 valid/near-best run",
    )
    add_selection(
        selected,
        choose_invalid(
            v21_trial4,
            failure_mode="command_nan_coincident_with_state_divergence",
        )
        or choose_invalid(v21_trial4),
        "B: Trial 4 stress comparison risk_adapter_v21 failed run",
    )

    trial6_by_method = {
        "original": build_rows_for(PROTOCOL_SINGLE, "original", TRIAL6, metrics_dir),
        "windlevel_s085": build_rows_for(
            PROTOCOL_SINGLE, "windlevel_s085", TRIAL6, metrics_dir
        ),
        "fixed_s080": build_rows_for(
            PROTOCOL_SINGLE, "fixed_s080", TRIAL6, metrics_dir
        ),
        "risk_adapter_v1": build_rows_for(
            PROTOCOL_SINGLE, "risk_adapter_v1", TRIAL6, metrics_dir
        ),
        "risk_adapter_v21": build_rows_for(
            PROTOCOL_SINGLE, "risk_adapter_v21", TRIAL6, metrics_dir
        ),
    }

    add_selection(
        selected,
        choose_valid_or_best(trial6_by_method["windlevel_s085"]),
        "C: Trial 6 single-goal windlevel_s085 valid run",
    )
    add_selection(
        selected,
        choose_valid_or_best(trial6_by_method["fixed_s080"]),
        "C: Trial 6 single-goal fixed_s080 valid run",
    )
    add_selection(
        selected,
        choose_valid_or_best(trial6_by_method["risk_adapter_v1"]),
        "C: Trial 6 single-goal risk_adapter_v1 valid run",
    )
    add_selection(
        selected,
        choose_invalid(trial6_by_method["risk_adapter_v1"]),
        "C: Trial 6 single-goal risk_adapter_v1 invalid run",
    )
    add_selection(
        selected,
        choose_valid_or_best(trial6_by_method["risk_adapter_v21"]),
        "C: Trial 6 single-goal risk_adapter_v21 valid run",
    )
    add_selection(
        selected,
        choose_invalid(trial6_by_method["risk_adapter_v21"]),
        "C: Trial 6 single-goal risk_adapter_v21 invalid run",
    )
    add_selection(
        selected,
        choose_invalid(trial6_by_method["original"]),
        "C: Trial 6 single-goal original invalid run",
    )

    add_selection(
        selected,
        choose_valid_or_best(trial6_by_method["risk_adapter_v1"]),
        "D: balanced-protagonist risk_adapter_v1 single-goal success",
    )
    add_selection(
        selected,
        choose_valid_or_best(v1_trial4),
        "D: balanced-protagonist risk_adapter_v1 goal-reissue stress success",
    )

    return sorted(
        selected.values(),
        key=lambda row: (
            row["selected_reason"][0],
            row["protocol"],
            row["method"],
            row["trial"],
            int(row["repeat"]),
        ),
    )


def read_csv_rows(csv_path):
    with csv_path.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)
        fieldnames = list(reader.fieldnames or [])
    return rows, fieldnames


def first_time_base(rows, fieldnames):
    time_column = "ros_time" if "ros_time" in fieldnames else ""
    if not time_column and "wall_time" in fieldnames:
        time_column = "wall_time"
    if not time_column:
        return "", math.nan
    times = [parse_float(row.get(time_column)) for row in rows]
    finite_times = [value for value in times if math.isfinite(value)]
    return time_column, min(finite_times) if finite_times else math.nan


def relative_time_series(rows, time_column, first_time):
    values = []
    for row in rows:
        time_value = parse_float(row.get(time_column))
        values.append(time_value - first_time if math.isfinite(time_value) else math.nan)
    return values


def available(fieldnames, columns):
    return all(column in fieldnames for column in columns)


def record_missing(missing, signal_name, fieldnames, columns):
    missing_columns = [column for column in columns if column not in fieldnames]
    if missing_columns:
        missing.append("%s missing %s" % (signal_name, ",".join(missing_columns)))


def vector_norm_series(rows, columns):
    values = []
    for row in rows:
        components = [parse_float(row.get(column)) for column in columns]
        if any(not math.isfinite(value) for value in components):
            values.append(math.nan)
        else:
            values.append(math.sqrt(sum(value * value for value in components)))
    return values


def column_series(rows, column):
    return [parse_float(row.get(column)) for row in rows]


def xy_error_series(rows):
    values = []
    for row in rows:
        ux = parse_float(row.get("uav_pos_x"))
        uy = parse_float(row.get("uav_pos_y"))
        gx = parse_float(row.get("goal_pos_x"))
        gy = parse_float(row.get("goal_pos_y"))
        if all(math.isfinite(value) for value in (ux, uy, gx, gy)):
            values.append(math.hypot(ux - gx, uy - gy))
        else:
            values.append(math.nan)
    return values


def ref_error_series(rows):
    values = []
    for row in rows:
        ux = parse_float(row.get("uav_pos_x"))
        uy = parse_float(row.get("uav_pos_y"))
        uz = parse_float(row.get("uav_pos_z"))
        rx = parse_float(row.get("ref_pos_x"))
        ry = parse_float(row.get("ref_pos_y"))
        rz = parse_float(row.get("ref_pos_z"))
        if all(math.isfinite(value) for value in (ux, uy, uz, rx, ry, rz)):
            values.append(math.sqrt((ux - rx) ** 2 + (uy - ry) ** 2 + (uz - rz) ** 2))
        else:
            values.append(math.nan)
    return values


def finite_pairs(times, values):
    pairs = [
        (time_value, value)
        for time_value, value in zip(times, values)
        if math.isfinite(time_value) and math.isfinite(value)
    ]
    if not pairs:
        return [], []
    x_values, y_values = zip(*pairs)
    return list(x_values), list(y_values)


def maybe_symlog(ax, series_list):
    values = [
        abs(value)
        for values in series_list
        for value in values
        if math.isfinite(value) and abs(value) > 0.0
    ]
    if values and max(values) > 1000.0:
        ax.set_yscale("symlog", linthresh=1.0)


def add_markers(ax, first_arrival_time, first_nan_time):
    if math.isfinite(first_arrival_time):
        ax.axvline(first_arrival_time, color="#2f7d32", linestyle="--", linewidth=1.0)
    if math.isfinite(first_nan_time):
        ax.axvline(first_nan_time, color="#b3261e", linestyle="--", linewidth=1.0)


def signal_panels(rows, fieldnames):
    missing = []
    panels = []

    if available(fieldnames, ["uav_vel_x", "uav_vel_y", "uav_vel_z"]):
        series = [("uav speed", vector_norm_series(rows, ["uav_vel_x", "uav_vel_y", "uav_vel_z"]))]
        if available(fieldnames, ["payload_vel_x", "payload_vel_y", "payload_vel_z"]):
            series.append(
                (
                    "payload speed",
                    vector_norm_series(
                        rows, ["payload_vel_x", "payload_vel_y", "payload_vel_z"]
                    ),
                )
            )
        else:
            record_missing(
                missing,
                "payload speed",
                fieldnames,
                ["payload_vel_x", "payload_vel_y", "payload_vel_z"],
            )
        panels.append(("UAV / payload speed", "speed (m/s)", series))
    else:
        record_missing(
            missing, "UAV speed", fieldnames, ["uav_vel_x", "uav_vel_y", "uav_vel_z"]
        )

    if "swing_angle_deg" in fieldnames:
        panels.append(
            (
                "Swing angle",
                "angle (deg)",
                [("swing_angle_deg", column_series(rows, "swing_angle_deg"))],
            )
        )
    else:
        record_missing(missing, "swing angle", fieldnames, ["swing_angle_deg"])

    position_series = []
    if available(fieldnames, ["uav_pos_x", "uav_pos_y", "goal_pos_x", "goal_pos_y"]):
        position_series.append(("target XY error", xy_error_series(rows)))
    else:
        record_missing(
            missing,
            "target XY error",
            fieldnames,
            ["uav_pos_x", "uav_pos_y", "goal_pos_x", "goal_pos_y"],
        )
    if available(
        fieldnames,
        ["uav_pos_x", "uav_pos_y", "uav_pos_z", "ref_pos_x", "ref_pos_y", "ref_pos_z"],
    ):
        position_series.append(("UAV-reference position error", ref_error_series(rows)))
    else:
        record_missing(
            missing,
            "UAV-reference position error",
            fieldnames,
            ["uav_pos_x", "uav_pos_y", "uav_pos_z", "ref_pos_x", "ref_pos_y", "ref_pos_z"],
        )
    if position_series:
        panels.append(("Position error", "error (m)", position_series))

    scale_series = []
    if "command_speed_scale" in fieldnames:
        scale_series.append(("speed_scale", column_series(rows, "command_speed_scale")))
    else:
        record_missing(missing, "command speed scale", fieldnames, ["command_speed_scale"])
    if "command_acceleration_scale" in fieldnames:
        scale_series.append(
            ("acceleration_scale", column_series(rows, "command_acceleration_scale"))
        )
    else:
        record_missing(
            missing,
            "command acceleration scale",
            fieldnames,
            ["command_acceleration_scale"],
        )
    if scale_series:
        panels.append(("Command scales", "scale", scale_series))

    risk_series = []
    if "command_risk_score_3s" in fieldnames:
        risk_series.append(("risk_score_3s", column_series(rows, "command_risk_score_3s")))
    else:
        record_missing(missing, "risk_score_3s", fieldnames, ["command_risk_score_3s"])
    if "command_risk_score_5s" in fieldnames:
        risk_series.append(("risk_score_5s", column_series(rows, "command_risk_score_5s")))
    else:
        record_missing(missing, "risk_score_5s", fieldnames, ["command_risk_score_5s"])
    if risk_series:
        panels.append(("Risk scores", "score", risk_series))

    if "goal_received_count" in fieldnames:
        panels.append(
            (
                "Goal received count",
                "count",
                [("goal_received_count", column_series(rows, "goal_received_count"))],
            )
        )
    else:
        record_missing(missing, "goal received count", fieldnames, ["goal_received_count"])

    trajectory_series = []
    if "trajectory_update_count" in fieldnames:
        trajectory_series.append(
            ("trajectory_update_count", column_series(rows, "trajectory_update_count"))
        )
    else:
        record_missing(
            missing, "trajectory update count", fieldnames, ["trajectory_update_count"]
        )
    if "trajectory_time_since_last_update" in fieldnames:
        trajectory_series.append(
            (
                "trajectory_time_since_last_update",
                column_series(rows, "trajectory_time_since_last_update"),
            )
        )
    else:
        record_missing(
            missing,
            "trajectory time since last update",
            fieldnames,
            ["trajectory_time_since_last_update"],
        )
    if trajectory_series:
        panels.append(("Trajectory updates", "count / seconds", trajectory_series))

    return panels, missing


def plot_run_trace(row, output_dir):
    csv_text = row.get("csv_path", "")
    if not csv_text:
        return "", "csv_path missing"
    csv_path = Path(csv_text)
    if not csv_path.exists():
        return "", "csv file missing"

    rows, fieldnames = read_csv_rows(csv_path)
    time_column, first_time = first_time_base(rows, fieldnames)
    if not time_column or not math.isfinite(first_time):
        return "", "time column missing"
    times = relative_time_series(rows, time_column, first_time)
    panels, missing = signal_panels(rows, fieldnames)
    if not panels:
        return "", "; ".join(missing) if missing else "no plottable signals"

    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as exc:
        return "", "matplotlib unavailable: %s" % exc

    first_arrival_time = parse_float(row.get("first_arrival_time"))
    first_nan_time = parse_float(row.get("first_nan_time"))
    panel_count = len(panels)
    fig_height = max(3.0, 2.15 * panel_count)
    fig, axes = plt.subplots(panel_count, 1, figsize=(11.0, fig_height), sharex=True)
    if panel_count == 1:
        axes = [axes]

    for ax, (title, ylabel, series_list) in zip(axes, panels):
        plotted_series = []
        plotted_count = 0
        for label, values in series_list:
            x_values, y_values = finite_pairs(times, values)
            if x_values:
                ax.plot(x_values, y_values, linewidth=1.2, label=label)
                plotted_series.append(y_values)
                plotted_count += 1
        if plotted_count == 0:
            ax.text(
                0.5,
                0.5,
                "No finite samples",
                transform=ax.transAxes,
                ha="center",
                va="center",
                fontsize=9,
            )
        add_markers(ax, first_arrival_time, first_nan_time)
        maybe_symlog(ax, plotted_series)
        ax.set_title(title)
        ax.set_ylabel(ylabel)
        ax.grid(alpha=0.25)
        if plotted_count > 1:
            ax.legend(frameon=False, loc="best")

    marker_legend = []
    if math.isfinite(first_arrival_time):
        marker_legend.append("green dashed = first_arrival_time")
    if math.isfinite(first_nan_time):
        marker_legend.append("red dashed = first_nan_time")
    title = "%s %s %s repeat%s" % (
        row["protocol"],
        row["method"],
        row["trial"],
        row["repeat"],
    )
    if marker_legend:
        title += " (%s)" % "; ".join(marker_legend)
    axes[0].text(
        0.0,
        1.12,
        title,
        transform=axes[0].transAxes,
        fontsize=10,
        va="bottom",
    )
    axes[-1].set_xlabel("time since log start (s)")
    fig.tight_layout(rect=(0, 0, 1, 0.98))

    plot_dir = output_dir / "plots"
    plot_dir.mkdir(parents=True, exist_ok=True)
    plot_name = "%s_%s_%s_repeat%s.png" % (
        row["protocol"],
        row["method"],
        row["trial"],
        row["repeat"],
    )
    plot_path = plot_dir / plot_name
    fig.savefig(str(plot_path), dpi=180)
    plt.close(fig)
    return str(plot_path), "; ".join(missing)


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


def rows_matching(rows, prefix):
    return [
        row
        for row in rows
        if any(part.startswith(prefix) for part in row["selected_reason"].split("; "))
    ]


def compact_fields():
    return [
        "selected_reason",
        "protocol",
        "method",
        "trial",
        "repeat",
        "strict_valid",
        "failure_group",
        "failure_mode_guess",
        "first_nan_time",
        "first_arrival_time",
        "plot_path",
    ]


def build_summary(rows):
    missing_by_reason = defaultdict(list)
    for row in rows:
        if row.get("missing_columns"):
            missing_by_reason[row["selected_reason"]].append(row["missing_columns"])

    lines = [
        "# Stage 4-AA2 Representative Trace Summary",
        "",
        "## Executive Summary",
        "",
        "Stage 4-AA2 generated offline representative trace plots from existing CSV logs. No ROS, simulation, RViz, or `catkin_make` is required.",
        "",
        "The selected traces target the current mechanism question before any `risk_adapter_v22` decision: whether the next method should be phase-aware, failure-aware, reference-jump-aware, or unnecessary.",
        "",
        "## Selected Runs Table",
        "",
        markdown_table(compact_fields(), rows),
        "",
        "## Trial 4 Stress v21 Trace Set",
        "",
        markdown_table(compact_fields(), rows_matching(rows, "A:")),
        "",
        "This set includes one strict-valid `risk_adapter_v21` run, command/control invalid examples, a state/task invalid example, and a `command_nan_coincident_with_state_divergence` example when available.",
        "",
        "## Trial 4 Stress Comparison Set",
        "",
        markdown_table(compact_fields(), rows_matching(rows, "B:")),
        "",
        "This set compares representative `fixed_s080`, `risk_adapter_v1`, and failed `risk_adapter_v21` traces under the same Trial 4 goal-reissue stress slice.",
        "",
        "## Trial 6 Single-Goal Bottleneck Set",
        "",
        markdown_table(compact_fields(), rows_matching(rows, "C:")),
        "",
        "This set compares strong single-goal Trial 6 examples from `windlevel_s085` and `fixed_s080` against valid and failed learned/risk-conditioned traces.",
        "",
        "## Optional Balanced-Protagonist Examples",
        "",
        markdown_table(compact_fields(), rows_matching(rows, "D:")),
        "",
        "These traces support the current `risk_adapter_v1`-centered balanced-governor narrative.",
        "",
        "## Missing Columns / Caveats",
        "",
    ]
    if missing_by_reason:
        for reason, missing_values in missing_by_reason.items():
            unique_missing = sorted(set(value for value in missing_values if value))
            lines.append("- `%s`: %s" % (reason, "; ".join(unique_missing)))
    else:
        lines.append("- No missing plottable signal groups were reported.")
    lines.extend(
        [
            "- Missing signals are skipped rather than treated as errors.",
            "- Very large invalid-run values may use a symmetric log y-axis for readability.",
            "- `failure_group` and `failure_mode_guess` are diagnostic labels, not exact physical root-cause proof.",
            "",
            "## Initial Diagnostic Questions For Human Inspection",
            "",
            "- Do Trial 4 stress `risk_adapter_v21` failures show a consistent pre-arrival phase pattern, or are command/control and state/task symptoms mixed?",
            "- Do `fixed_s080` and `risk_adapter_v1` avoid the same early command/control symptoms seen in selected `risk_adapter_v21` failures?",
            "- In Trial 6 single-goal runs, do learned governors trail because of scale timing, target approach behavior, swing growth, reference jumps, or late target error?",
            "- Are any reference or trajectory update signals aligned with the first divergence markers?",
            "",
            "## What The Plots Can Support",
            "",
            "- A mechanism hypothesis for phase-aware, failure-aware, or reference-jump-aware follow-up design.",
            "- A paper-side explanation for why protocol specialists and balanced learned governors behave differently.",
            "- Selection of representative traces for failure-mode-aware qualitative discussion.",
            "",
            "## What They Cannot Prove",
            "",
            "- They cannot prove exact physical root cause.",
            "- They cannot establish statistical significance.",
            "- They cannot prove a safety guarantee.",
            "- They cannot justify a Trial-4-specific patch without a reusable mechanism.",
            "",
            "## Recommendation",
            "",
            "Do not create `risk_adapter_v22` until these plots are reviewed. Create `risk_adapter_v22` only if the traces reveal a generic phase-aware or failure-aware mechanism that can improve dual-protocol balance.",
            "",
        ]
    )
    return "\n".join(lines)


def main():
    args = parse_args()
    metrics_dir = repo_path(args.metrics_dir)
    output_dir = repo_path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    selected_rows = select_representative_rows(metrics_dir)
    for row in selected_rows:
        plot_path, missing_columns = plot_run_trace(row, output_dir)
        row["plot_path"] = plot_path
        row["missing_columns"] = missing_columns

    write_csv(
        output_dir / "stage4aa_representative_trace_index.csv",
        INDEX_FIELDS,
        selected_rows,
    )
    write_markdown_table(
        output_dir / "stage4aa_representative_trace_index.md",
        "Stage 4-AA2 Representative Trace Index",
        INDEX_FIELDS,
        selected_rows,
    )
    (output_dir / "stage4aa_representative_trace_summary.md").write_text(
        build_summary(selected_rows), encoding="utf-8"
    )

    if args.print_summary:
        print("selected_runs: %d" % len(selected_rows))
        print("output_dir: %s" % output_dir)
        print(
            "plots_written: %d"
            % sum(1 for row in selected_rows if row.get("plot_path"))
        )
        missing_count = sum(1 for row in selected_rows if row.get("missing_columns"))
        print("rows_with_missing_columns: %d" % missing_count)
    return 0


if __name__ == "__main__":
    sys.exit(main())
