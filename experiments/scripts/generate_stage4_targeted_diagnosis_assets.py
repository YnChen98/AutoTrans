#!/usr/bin/env python3
"""Generate Stage 4-AA targeted diagnosis assets."""

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

RUN_FIELDS = [
    "protocol",
    "method",
    "trial",
    "repeat",
    "strict_valid",
    "failure_group",
    "failure_mode_guess",
    "metrics_summary_path",
    "csv_path",
    "first_nan_time",
    "first_command_nan_time",
    "first_state_divergence_time",
    "first_reference_jump_time",
    "arrival_detected",
    "first_arrival_time",
    "goal_received_count_final",
    "post_arrival_goal_received_count",
    "first_failure_after_arrival_flag",
    "final_uav_xy_error",
    "max_swing_angle_deg",
    "max_uav_speed",
    "max_payload_speed",
    "mean_command_speed_scale",
    "min_command_speed_scale",
    "max_command_speed_scale",
]

TRIAL6_SUMMARY_FIELDS = [
    "protocol",
    "method",
    "strict_valid_count",
    "repeat_count",
    "invalid_count",
    "command_control_upstream_count",
    "planner_reference_upstream_count",
    "state_task_upstream_count",
    "target_error_only_count",
    "post_arrival_failure_count",
    "arrival_detected_count",
    "mean_arrival_time",
    "mean_command_speed_scale",
    "mean_max_swing_angle_deg",
    "mean_final_uav_xy_error",
]

TRIAL4_STRESS_V21_PATTERN = (
    "stage4x_risk_adapter_v21_goalreissue_strong_trial4_goalrepeat10_"
    "repeat%d_metrics_summary.txt"
)

TRIAL6_SPECS = [
    (
        PROTOCOL_SINGLE,
        "original",
        "stage4x_singlegoal_original_strong_trial6_goalrepeat1_repeat%d_metrics_summary.txt",
    ),
    (
        PROTOCOL_SINGLE,
        "fixed_s085",
        "stage4x_singlegoal_fixed_s085_strong_trial6_goalrepeat1_repeat%d_metrics_summary.txt",
    ),
    (
        PROTOCOL_SINGLE,
        "windlevel_s085",
        "stage4x_singlegoal_windlevel_s085_strong_trial6_goalrepeat1_repeat%d_metrics_summary.txt",
    ),
    (
        PROTOCOL_SINGLE,
        "fixed_s080",
        "stage4u_fixed_s080_strong_trial6_goalrepeat1_repeat%d_metrics_summary.txt",
    ),
    (
        PROTOCOL_SINGLE,
        "risk_adapter_v1",
        "stage4x_singlegoal_risk_adapter_v1_strong_trial6_goalrepeat1_repeat%d_metrics_summary.txt",
    ),
    (
        PROTOCOL_SINGLE,
        "risk_adapter_v2",
        "stage4u_risk_adapter_v2_strong_trial6_goalrepeat1_repeat%d_metrics_summary.txt",
    ),
    (
        PROTOCOL_SINGLE,
        "risk_adapter_v21",
        "stage4v_risk_adapter_v21_strong_trial6_goalrepeat1_screening_repeat%d_metrics_summary.txt",
    ),
    (
        PROTOCOL_STRESS,
        "original",
        "stage4_original_strong_trial6_repeat%d_metrics_summary.txt",
    ),
    (
        PROTOCOL_STRESS,
        "fixed_s085",
        "stage4_fixed_s085_strong_trial6_repeat%d_metrics_summary.txt",
    ),
    (
        PROTOCOL_STRESS,
        "windlevel_s085",
        "stage4_windlevel_s085_strong_trial6_repeat%d_metrics_summary.txt",
    ),
    (
        PROTOCOL_STRESS,
        "risk_adapter_v1",
        "stage4_risk_adapter_v1_strong_trial6_repeat%d_metrics_summary.txt",
    ),
    (
        PROTOCOL_STRESS,
        "fixed_s080",
        "stage4_fixed_s080_strong_trial6_frontier_repeat%d_metrics_summary.txt",
    ),
    (
        PROTOCOL_STRESS,
        "risk_adapter_v21",
        "stage4x_risk_adapter_v21_goalreissue_strong_trial6_goalrepeat10_repeat%d_metrics_summary.txt",
    ),
]

TRIAL6_SPEC_ORDER = {
    (protocol, method): index for index, (protocol, method, _) in enumerate(TRIAL6_SPECS)
}

EXPECTED_STRICT_VALID = {
    (PROTOCOL_STRESS, "risk_adapter_v21", TRIAL4): 4,
    (PROTOCOL_SINGLE, "original", TRIAL6): 7,
    (PROTOCOL_SINGLE, "fixed_s085", TRIAL6): 8,
    (PROTOCOL_SINGLE, "windlevel_s085", TRIAL6): 9,
    (PROTOCOL_SINGLE, "fixed_s080", TRIAL6): 8,
    (PROTOCOL_SINGLE, "risk_adapter_v1", TRIAL6): 7,
    (PROTOCOL_SINGLE, "risk_adapter_v2", TRIAL6): 6,
    (PROTOCOL_SINGLE, "risk_adapter_v21", TRIAL6): 6,
    (PROTOCOL_STRESS, "original", TRIAL6): 3,
    (PROTOCOL_STRESS, "fixed_s085", TRIAL6): 4,
    (PROTOCOL_STRESS, "windlevel_s085", TRIAL6): 6,
    (PROTOCOL_STRESS, "risk_adapter_v1", TRIAL6): 7,
    (PROTOCOL_STRESS, "fixed_s080", TRIAL6): 7,
    (PROTOCOL_STRESS, "risk_adapter_v21", TRIAL6): 7,
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate Stage 4-AA targeted diagnosis assets."
    )
    parser.add_argument(
        "--metrics-dir",
        default="experiments/figures",
        help="Directory containing *_metrics_summary.txt files.",
    )
    parser.add_argument(
        "--output-dir",
        default="experiments/results/stage4_targeted_diagnosis",
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
        "protocol": protocol,
        "method": method,
        "trial": trial,
        "repeat": str(repeat),
        "strict_valid": strict_valid_text(strict_valid),
        "failure_group": failure_group,
        "failure_mode_guess": inspector_row.get("failure_mode_guess", ""),
        "metrics_summary_path": str(metrics_path),
        "csv_path": stage4z.passthrough_text(metrics.get("csv_path")),
        "first_nan_time": stage4z.finite_text(metrics.get("first_nan_time")),
        "first_command_nan_time": stage4z.finite_text(
            inspector_row.get("first_command_nan_time")
        ),
        "first_state_divergence_time": stage4z.finite_text(
            inspector_row.get("first_state_divergence_time")
        ),
        "first_reference_jump_time": stage4z.finite_text(
            inspector_row.get("first_reference_jump_time")
        ),
        "arrival_detected": stage4z.passthrough_text(metrics.get("arrival_detected")),
        "first_arrival_time": stage4z.finite_text(metrics.get("first_arrival_time")),
        "goal_received_count_final": stage4z.passthrough_text(
            metrics.get("goal_received_count_final")
        ),
        "post_arrival_goal_received_count": stage4z.passthrough_text(
            metrics.get("post_arrival_goal_received_count")
        ),
        "first_failure_after_arrival_flag": stage4z.passthrough_text(
            metrics.get("first_failure_after_arrival_flag")
        ),
        "final_uav_xy_error": stage4z.finite_text(
            metrics.get("final_uav_xy_error")
        ),
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
    }


def build_trial4_stress_v21_rows(metrics_dir):
    rows = []
    for repeat in REPEATS:
        metrics_path = stage4z.resolve_metrics_path(
            metrics_dir, [TRIAL4_STRESS_V21_PATTERN % repeat]
        )
        rows.append(
            run_row(
                PROTOCOL_STRESS,
                "risk_adapter_v21",
                TRIAL4,
                repeat,
                metrics_path,
            )
        )
    return rows


def build_trial6_rows(metrics_dir):
    rows = []
    for protocol, method, pattern in TRIAL6_SPECS:
        for repeat in REPEATS:
            metrics_path = stage4z.resolve_metrics_path(metrics_dir, [pattern % repeat])
            rows.append(run_row(protocol, method, TRIAL6, repeat, metrics_path))
    return rows


def finite_values(rows, field):
    values = []
    for row in rows:
        value = stage4z.parse_float(row.get(field))
        if math.isfinite(value):
            values.append(value)
    return values


def mean_text(values):
    if not values:
        return ""
    return "%.6f" % (sum(values) / len(values))


def bool_count(rows, field):
    return sum(1 for row in rows if stage4z.parse_bool(row.get(field)))


def build_trial6_summary_rows(trial6_rows):
    grouped = defaultdict(list)
    for row in trial6_rows:
        grouped[(row["protocol"], row["method"])].append(row)

    rows = []
    for key, run_rows in grouped.items():
        protocol, method = key
        valid_count = sum(1 for row in run_rows if row["strict_valid"] == "true")
        invalid_rows = [row for row in run_rows if row["strict_valid"] == "false"]
        arrival_rows = [
            row for row in run_rows if stage4z.parse_bool(row.get("arrival_detected"))
        ]
        rows.append(
            {
                "protocol": protocol,
                "method": method,
                "strict_valid_count": str(valid_count),
                "repeat_count": str(len(run_rows)),
                "invalid_count": str(len(invalid_rows)),
                "command_control_upstream_count": str(
                    sum(
                        1
                        for row in invalid_rows
                        if row["failure_group"] == "command_control_upstream"
                    )
                ),
                "planner_reference_upstream_count": str(
                    sum(
                        1
                        for row in invalid_rows
                        if row["failure_group"] == "planner_reference_upstream"
                    )
                ),
                "state_task_upstream_count": str(
                    sum(
                        1
                        for row in invalid_rows
                        if row["failure_group"] == "state_task_upstream"
                    )
                ),
                "target_error_only_count": str(
                    sum(
                        1
                        for row in invalid_rows
                        if row["failure_mode_guess"] == "target_error_only"
                    )
                ),
                "post_arrival_failure_count": str(
                    bool_count(invalid_rows, "first_failure_after_arrival_flag")
                ),
                "arrival_detected_count": str(len(arrival_rows)),
                "mean_arrival_time": mean_text(
                    finite_values(arrival_rows, "first_arrival_time")
                ),
                "mean_command_speed_scale": mean_text(
                    finite_values(run_rows, "mean_command_speed_scale")
                ),
                "mean_max_swing_angle_deg": mean_text(
                    finite_values(run_rows, "max_swing_angle_deg")
                ),
                "mean_final_uav_xy_error": mean_text(
                    finite_values(run_rows, "final_uav_xy_error")
                ),
            }
        )
    rows.sort(key=lambda row: TRIAL6_SPEC_ORDER[(row["protocol"], row["method"])])
    return rows


def validate_expected_counts(trial4_rows, trial6_summary_rows):
    observed = {
        (PROTOCOL_STRESS, "risk_adapter_v21", TRIAL4): sum(
            1 for row in trial4_rows if row["strict_valid"] == "true"
        )
    }
    for row in trial6_summary_rows:
        observed[(row["protocol"], row["method"], TRIAL6)] = int(
            row["strict_valid_count"]
        )

    for key, expected in EXPECTED_STRICT_VALID.items():
        actual = observed.get(key)
        if actual != expected:
            raise ValueError(
                "%s/%s/%s strict-valid mismatch: expected %d observed %s"
                % (key[0], key[1], key[2], expected, actual)
            )


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


def group_counts_text(rows):
    counts = defaultdict(int)
    for row in rows:
        if row["strict_valid"] == "false":
            counts[row["failure_group"]] += 1
    ordered = [
        "command_control_upstream",
        "planner_reference_upstream",
        "state_task_upstream",
        "unknown",
    ]
    parts = ["%s=%d" % (group, counts[group]) for group in ordered if counts[group]]
    return ", ".join(parts) if parts else "none"


def summary_row(summary_rows, protocol, method):
    for row in summary_rows:
        if row["protocol"] == protocol and row["method"] == method:
            return row
    raise KeyError("%s/%s missing from summary rows" % (protocol, method))


def build_summary(trial4_rows, trial6_summary_rows, trial4_plot, trial6_plot):
    trial4_valid = sum(1 for row in trial4_rows if row["strict_valid"] == "true")
    trial4_invalid = len(trial4_rows) - trial4_valid
    trial4_post_arrival = bool_count(
        [row for row in trial4_rows if row["strict_valid"] == "false"],
        "first_failure_after_arrival_flag",
    )
    v21_single = summary_row(trial6_summary_rows, PROTOCOL_SINGLE, "risk_adapter_v21")
    v1_single = summary_row(trial6_summary_rows, PROTOCOL_SINGLE, "risk_adapter_v1")
    fixed_single = summary_row(trial6_summary_rows, PROTOCOL_SINGLE, "fixed_s080")
    wind_single = summary_row(trial6_summary_rows, PROTOCOL_SINGLE, "windlevel_s085")
    v21_stress = summary_row(trial6_summary_rows, PROTOCOL_STRESS, "risk_adapter_v21")
    v1_stress = summary_row(trial6_summary_rows, PROTOCOL_STRESS, "risk_adapter_v1")
    fixed_stress = summary_row(trial6_summary_rows, PROTOCOL_STRESS, "fixed_s080")

    return "\n".join(
        [
            "# Stage 4-AA Targeted Diagnosis Summary",
            "",
            "## Executive Summary",
            "",
            "Stage 4-AA targets two follow-up questions from Stage 4-Z2: why `risk_adapter_v21` is weak on Trial 4 under goal-reissue stress, and why Trial 6 remains a bottleneck for learned/risk-conditioned variants.",
            "",
            "The generated tables preserve strict-valid as the paper-facing metric and use Stage 4-Z2 `failure_group` labels only as diagnostic evidence. These labels are not exact physical root-cause proof.",
            "",
            "## Trial 4 Stress `risk_adapter_v21` Diagnosis",
            "",
            "`risk_adapter_v21` achieved `%d/10` strict-valid on Trial 4 under the goal-reissue stress protocol, leaving `%d` strict-invalid runs." % (trial4_valid, trial4_invalid),
            "",
            "Invalid-only failure groups for this slice: `%s`." % group_counts_text(trial4_rows),
            "",
            "`%d` strict-invalid Trial 4 stress runs were flagged as first failure after arrival. The remaining invalid runs are not explained by that post-arrival flag alone, so the result should not be reduced to a pure post-arrival artifact." % trial4_post_arrival,
            "",
            "## Trial 6 Bottleneck Diagnosis",
            "",
            "Single-goal Trial 6 shows a gap between simple baselines and learned/risk-conditioned variants: `windlevel_s085` is `%s/10`, `fixed_s080` is `%s/10`, `risk_adapter_v1` is `%s/10`, and `risk_adapter_v21` is `%s/10`." % (
                wind_single["strict_valid_count"],
                fixed_single["strict_valid_count"],
                v1_single["strict_valid_count"],
                v21_single["strict_valid_count"],
            ),
            "",
            "Goal-reissue stress Trial 6 is flatter among the leading methods: `fixed_s080`, `risk_adapter_v1`, and `risk_adapter_v21` are each `%s/10`, `%s/10`, and `%s/10`, respectively." % (
                fixed_stress["strict_valid_count"],
                v1_stress["strict_valid_count"],
                v21_stress["strict_valid_count"],
            ),
            "",
            "## Trial 6 Method Summary",
            "",
            markdown_table(TRIAL6_SUMMARY_FIELDS, trial6_summary_rows),
            "",
            "## Key Evidence",
            "",
            "- Trial 4 stress `risk_adapter_v21` failures include command/control and state/task diagnostic signals; they are not all flagged as post-arrival failures.",
            "- Single-goal Trial 6 is where `risk_adapter_v21` trails `windlevel_s085` and `fixed_s080` most clearly.",
            "- Goal-reissue stress Trial 6 does not show the same `risk_adapter_v21` deficit relative to `fixed_s080` and `risk_adapter_v1`; all three are `7/10` there.",
            "- Scale behavior and timing fields are retained in the run-level tables so representative failed CSVs can be inspected next if needed.",
            "",
            "## What The Data Suggests",
            "",
            "The Trial 4 stress weakness appears mixed rather than single-cause: command/control symptoms and state/task symptoms are both present, while no strict-invalid run in this slice is flagged as first failure after arrival.",
            "",
            "The Trial 6 bottleneck appears protocol-dependent. The single-goal gap favors `windlevel_s085` and `fixed_s080`, while the stress Trial 6 comparison is more even among `fixed_s080`, `risk_adapter_v1`, and `risk_adapter_v21`.",
            "",
            "## What It Does Not Prove",
            "",
            "- It does not prove exact physical root cause.",
            "- It does not show that all goal-reissue stress failures are post-arrival artifacts.",
            "- It does not show that `risk_adapter_v21` is globally flawed.",
            "- It does not show that `risk_adapter_v22` is required before inspecting representative failures.",
            "",
            "## Recommendation",
            "",
            "- Do not create `risk_adapter_v22` yet.",
            "- Inspect representative failed CSVs or plots for Trial 4 stress `risk_adapter_v21` and Trial 6 bottleneck cases if more diagnosis is needed.",
            "- If a future method is justified, it should be phase-aware or failure-aware, not narrowly tuned to Trial 4.",
            "",
            "## Generated Plot Status",
            "",
            "- `stage4aa_trial4_stress_v21_failure_timing.png`: `%s`" % ("written" if trial4_plot else "skipped"),
            "- `stage4aa_trial6_success_by_method.png`: `%s`" % ("written" if trial6_plot else "skipped"),
            "",
        ]
    )


def write_trial4_timing_plot(path, rows):
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as exc:
        print("warning: matplotlib unavailable; skipping Trial 4 timing plot: %s" % exc, file=sys.stderr)
        return False

    fields = [
        ("first_arrival_time", "arrival", "o"),
        ("first_command_nan_time", "command NaN", "x"),
        ("first_state_divergence_time", "state divergence", "^"),
        ("first_reference_jump_time", "reference jump", "s"),
        ("first_nan_time", "metrics first NaN", "d"),
    ]
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    for field, label, marker in fields:
        x_values = []
        y_values = []
        for row in rows:
            value = stage4z.parse_float(row.get(field))
            if math.isfinite(value):
                x_values.append(int(row["repeat"]))
                y_values.append(value)
        if x_values:
            ax.scatter(x_values, y_values, label=label, marker=marker, s=56)
    invalid_repeats = [
        int(row["repeat"]) for row in rows if row["strict_valid"] == "false"
    ]
    for repeat in invalid_repeats:
        ax.axvline(repeat, color="#dddddd", linewidth=0.8, zorder=0)
    ax.set_title("Trial 4 goal-reissue stress v21 timing diagnostics")
    ax.set_xlabel("repeat")
    ax.set_ylabel("time since log start (s)")
    ax.set_xticks(list(REPEATS))
    ax.grid(axis="y", alpha=0.25)
    ax.legend(frameon=False, loc="best")
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(str(path), dpi=200)
    plt.close(fig)
    return True


def write_trial6_success_plot(path, summary_rows):
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as exc:
        print("warning: matplotlib unavailable; skipping Trial 6 success plot: %s" % exc, file=sys.stderr)
        return False

    fig, axes = plt.subplots(1, 2, figsize=(12.8, 4.8), sharey=True)
    for ax, protocol, title in [
        (axes[0], PROTOCOL_SINGLE, "single-goal Trial 6"),
        (axes[1], PROTOCOL_STRESS, "goal-reissue stress Trial 6"),
    ]:
        rows = [row for row in summary_rows if row["protocol"] == protocol]
        methods = [row["method"] for row in rows]
        values = [int(row["strict_valid_count"]) for row in rows]
        ax.bar(range(len(rows)), values, color="#5b6c8f")
        ax.set_title(title)
        ax.set_xticks(range(len(rows)))
        ax.set_xticklabels(methods, rotation=45, ha="right")
        ax.set_ylim(0, 10)
        ax.grid(axis="y", alpha=0.25)
        ax.set_axisbelow(True)
    axes[0].set_ylabel("strict-valid count / 10")
    fig.suptitle("Stage 4-AA Trial 6 strict-valid count by method")
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(str(path), dpi=200)
    plt.close(fig)
    return True


def main():
    args = parse_args()
    metrics_dir = repo_path(args.metrics_dir)
    output_dir = repo_path(args.output_dir)

    trial4_rows = build_trial4_stress_v21_rows(metrics_dir)
    trial6_rows = build_trial6_rows(metrics_dir)
    trial6_summary_rows = build_trial6_summary_rows(trial6_rows)
    validate_expected_counts(trial4_rows, trial6_summary_rows)

    write_csv(
        output_dir / "stage4aa_trial4_stress_v21_run_table.csv",
        RUN_FIELDS,
        trial4_rows,
    )
    write_markdown_table(
        output_dir / "stage4aa_trial4_stress_v21_run_table.md",
        "Stage 4-AA Trial 4 Stress v21 Run Table",
        RUN_FIELDS,
        trial4_rows,
    )
    write_csv(
        output_dir / "stage4aa_trial6_bottleneck_run_table.csv",
        RUN_FIELDS,
        trial6_rows,
    )
    write_markdown_table(
        output_dir / "stage4aa_trial6_bottleneck_run_table.md",
        "Stage 4-AA Trial 6 Bottleneck Run Table",
        RUN_FIELDS,
        trial6_rows,
    )
    write_csv(
        output_dir / "stage4aa_trial6_method_summary.csv",
        TRIAL6_SUMMARY_FIELDS,
        trial6_summary_rows,
    )
    write_markdown_table(
        output_dir / "stage4aa_trial6_method_summary.md",
        "Stage 4-AA Trial 6 Method Summary",
        TRIAL6_SUMMARY_FIELDS,
        trial6_summary_rows,
    )

    trial4_plot = write_trial4_timing_plot(
        output_dir / "stage4aa_trial4_stress_v21_failure_timing.png",
        trial4_rows,
    )
    trial6_plot = write_trial6_success_plot(
        output_dir / "stage4aa_trial6_success_by_method.png",
        trial6_summary_rows,
    )
    (output_dir / "stage4aa_targeted_diagnosis_summary.md").write_text(
        build_summary(trial4_rows, trial6_summary_rows, trial4_plot, trial6_plot),
        encoding="utf-8",
    )

    if args.print_summary:
        print("Stage 4-AA targeted diagnosis assets")
        print("trial4_stress_v21_rows: %d" % len(trial4_rows))
        print("trial6_bottleneck_rows: %d" % len(trial6_rows))
        print("trial6_method_summary_rows: %d" % len(trial6_summary_rows))
        print("trial4_plot_written: %s" % ("true" if trial4_plot else "false"))
        print("trial6_plot_written: %s" % ("true" if trial6_plot else "false"))
        print("output_dir: %s" % output_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
