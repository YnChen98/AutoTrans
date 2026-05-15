#!/usr/bin/env python3
"""Generate Stage 4 protocol-split paper tables and figures."""

import argparse
import csv
import math
import sys
from collections import defaultdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]

TRIALS = ["trial4", "trial5", "trial6"]
REPEATS = range(1, 11)

PROTOCOL_SINGLE = "single_goal_mission"
PROTOCOL_REPEATED = "repeated_goal_stress"
PROTOCOL_ORDER = [PROTOCOL_SINGLE, PROTOCOL_REPEATED]

SINGLE_GOAL_METHODS = ["fixed_s080", "risk_adapter_v2", "risk_adapter_v21"]
REPEATED_GOAL_METHODS = [
    "original",
    "fixed_s085",
    "windlevel_s085",
    "risk_adapter_v1",
    "fixed_s080",
]
PLOT_METHOD_ORDER = [
    "original",
    "fixed_s085",
    "windlevel_s085",
    "risk_adapter_v1",
    "fixed_s080",
    "risk_adapter_v2",
    "risk_adapter_v21",
]

EXPECTED_TRIAL_COUNTS = {
    (PROTOCOL_SINGLE, "fixed_s080", "trial4"): 7,
    (PROTOCOL_SINGLE, "fixed_s080", "trial5"): 6,
    (PROTOCOL_SINGLE, "fixed_s080", "trial6"): 8,
    (PROTOCOL_SINGLE, "risk_adapter_v2", "trial4"): 9,
    (PROTOCOL_SINGLE, "risk_adapter_v2", "trial5"): 6,
    (PROTOCOL_SINGLE, "risk_adapter_v2", "trial6"): 6,
    (PROTOCOL_SINGLE, "risk_adapter_v21", "trial4"): 10,
    (PROTOCOL_SINGLE, "risk_adapter_v21", "trial5"): 9,
    (PROTOCOL_SINGLE, "risk_adapter_v21", "trial6"): 6,
    (PROTOCOL_REPEATED, "original", "trial4"): 8,
    (PROTOCOL_REPEATED, "original", "trial5"): 7,
    (PROTOCOL_REPEATED, "original", "trial6"): 3,
    (PROTOCOL_REPEATED, "fixed_s085", "trial4"): 9,
    (PROTOCOL_REPEATED, "fixed_s085", "trial5"): 5,
    (PROTOCOL_REPEATED, "fixed_s085", "trial6"): 4,
    (PROTOCOL_REPEATED, "windlevel_s085", "trial4"): 4,
    (PROTOCOL_REPEATED, "windlevel_s085", "trial5"): 6,
    (PROTOCOL_REPEATED, "windlevel_s085", "trial6"): 6,
    (PROTOCOL_REPEATED, "risk_adapter_v1", "trial4"): 7,
    (PROTOCOL_REPEATED, "risk_adapter_v1", "trial5"): 9,
    (PROTOCOL_REPEATED, "risk_adapter_v1", "trial6"): 7,
    (PROTOCOL_REPEATED, "fixed_s080", "trial4"): 8,
    (PROTOCOL_REPEATED, "fixed_s080", "trial5"): 9,
    (PROTOCOL_REPEATED, "fixed_s080", "trial6"): 7,
}

SUCCESS_FIELDS = [
    "protocol",
    "trial",
    "method",
    "valid_count",
    "repeat_count",
    "invalid_count",
    "success_rate",
    "success_percent",
]

AGGREGATE_FIELDS = [
    "protocol",
    "method",
    "total_valid",
    "total_repeats",
    "total_invalid",
    "aggregate_success_rate",
    "aggregate_success_percent",
    "rank_within_protocol",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate Stage 4 protocol-split paper assets."
    )
    parser.add_argument(
        "--metrics-dir",
        default="experiments/figures",
        help="Directory containing *_metrics_summary.txt files.",
    )
    parser.add_argument(
        "--output-dir",
        default="experiments/results/stage4_protocol_split_paper_assets",
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


def format_rate(value):
    return "%.3f" % value


def format_percent(value):
    return "%.1f" % (100.0 * value)


def protocol_sort_key(protocol):
    if protocol in PROTOCOL_ORDER:
        return (PROTOCOL_ORDER.index(protocol), protocol)
    return (len(PROTOCOL_ORDER), protocol)


def trial_sort_key(trial):
    if trial in TRIALS:
        return (TRIALS.index(trial), trial)
    return (len(TRIALS), trial)


def method_sort_key(method):
    if method in PLOT_METHOD_ORDER:
        return (PLOT_METHOD_ORDER.index(method), method)
    return (len(PLOT_METHOD_ORDER), method)


def parse_metrics_summary(path):
    metrics = {}
    with path.open("r", encoding="utf-8") as metrics_file:
        for line in metrics_file:
            if ":" not in line:
                continue
            key, value = line.rstrip("\n").split(":", 1)
            metrics[key.strip()] = value.strip()
    return metrics


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


def single_goal_candidates(method, trial, repeat):
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


def repeated_goal_candidates(method, trial, repeat):
    if method == "fixed_s080":
        return [
            "stage4_fixed_s080_strong_%s_frontier_repeat%d_metrics_summary.txt"
            % (trial, repeat)
        ]
    return [
        "stage4_%s_strong_%s_repeat%d_metrics_summary.txt" % (method, trial, repeat)
    ]


def resolve_metrics_path(metrics_dir, names):
    tried = []
    for name in names:
        path = metrics_dir / name
        tried.append(str(path))
        if path.exists():
            return path
    raise FileNotFoundError("missing metrics summary; tried: %s" % ", ".join(tried))


def protocol_methods(protocol):
    if protocol == PROTOCOL_SINGLE:
        return SINGLE_GOAL_METHODS
    if protocol == PROTOCOL_REPEATED:
        return REPEATED_GOAL_METHODS
    raise ValueError("unknown protocol: %s" % protocol)


def metrics_candidates(protocol, method, trial, repeat):
    if protocol == PROTOCOL_SINGLE:
        return single_goal_candidates(method, trial, repeat)
    if protocol == PROTOCOL_REPEATED:
        return repeated_goal_candidates(method, trial, repeat)
    raise ValueError("unknown protocol: %s" % protocol)


def build_success_rows(metrics_dir, protocol):
    rows = []
    for trial in TRIALS:
        for method in protocol_methods(protocol):
            valid_count = 0
            for repeat in REPEATS:
                metrics_path = resolve_metrics_path(
                    metrics_dir,
                    metrics_candidates(protocol, method, trial, repeat),
                )
                metrics = parse_metrics_summary(metrics_path)
                if strict_valid_from_metrics(metrics):
                    valid_count += 1
            repeat_count = len(REPEATS)
            invalid_count = repeat_count - valid_count
            expected = EXPECTED_TRIAL_COUNTS[(protocol, method, trial)]
            if valid_count != expected:
                raise ValueError(
                    "%s/%s/%s strict-valid mismatch: expected %d observed %d"
                    % (protocol, trial, method, expected, valid_count)
                )
            rate = valid_count / repeat_count
            rows.append(
                {
                    "protocol": protocol,
                    "trial": trial,
                    "method": method,
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
        key = (row["protocol"], row["method"])
        grouped[key]["valid"] += int(row["valid_count"])
        grouped[key]["repeats"] += int(row["repeat_count"])
        grouped[key]["invalid"] += int(row["invalid_count"])

    rows = []
    for protocol in PROTOCOL_ORDER:
        raw_rows = []
        for method in protocol_methods(protocol):
            item = grouped[(protocol, method)]
            rate = item["valid"] / item["repeats"]
            raw_rows.append((method, item["valid"], item["repeats"], item["invalid"], rate))

        sorted_rows = sorted(raw_rows, key=lambda item: (-item[4], method_sort_key(item[0])))
        previous_rate = None
        rank = 0
        for index, (method, valid, repeats, invalid, rate) in enumerate(sorted_rows, start=1):
            if previous_rate is None or abs(rate - previous_rate) > 1.0e-12:
                rank = index
                previous_rate = rate
            rows.append(
                {
                    "protocol": protocol,
                    "method": method,
                    "total_valid": str(valid),
                    "total_repeats": str(repeats),
                    "total_invalid": str(invalid),
                    "aggregate_success_rate": format_rate(rate),
                    "aggregate_success_percent": format_percent(rate),
                    "rank_within_protocol": str(rank),
                }
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


def build_summary(single_rows, repeated_rows, aggregate_rows):
    single_aggregate = [
        row for row in aggregate_rows if row["protocol"] == PROTOCOL_SINGLE
    ]
    repeated_aggregate = [
        row for row in aggregate_rows if row["protocol"] == PROTOCOL_REPEATED
    ]
    return "\n".join(
        [
            "# Stage 4 Protocol-Split Paper Summary",
            "",
            "## Executive Summary",
            "",
            "Stage 4 results are split by goal protocol. `goal_repeat=1` is the single-goal mission protocol, and `goal_repeat=10` is the repeated-goal / post-arrival replan stress protocol.",
            "",
            "Under the single-goal mission protocol, `risk_adapter_v21` achieved the highest strict-valid rate: `25/30`.",
            "",
            "Under the repeated-goal stress protocol, `fixed_s080` achieved the highest strict-valid rate: `24/30`.",
            "",
            "## Single-Goal Mission Results",
            "",
            markdown_table(SUCCESS_FIELDS, single_rows),
            "",
            "Aggregate ranking:",
            "",
            markdown_table(AGGREGATE_FIELDS, single_aggregate),
            "",
            "## Repeated-Goal Stress Results",
            "",
            markdown_table(SUCCESS_FIELDS, repeated_rows),
            "",
            "Aggregate ranking:",
            "",
            markdown_table(AGGREGATE_FIELDS, repeated_aggregate),
            "",
            "## Protocol Split Interpretation",
            "",
            "The two protocols test different system properties. The single-goal mission protocol evaluates ordinary one-command transport behavior. The repeated-goal stress protocol keeps publishing the same goal and can exercise post-arrival replan behavior.",
            "",
            "`risk_adapter_v21` improves over `fixed_s080` and `risk_adapter_v2` in single-goal aggregate, but Trial 6 remains a bottleneck. `fixed_s080` remains the strongest repeated-goal stress method.",
            "",
            "## Paper-Facing Claims",
            "",
            "- Under the single-goal mission protocol, `risk_adapter_v21` achieved the highest strict-valid rate: `25/30`.",
            "- Under the repeated-goal stress protocol, `fixed_s080` achieved the highest strict-valid rate: `24/30`.",
            "- `risk_adapter_v21` improves over `fixed_s080` and `risk_adapter_v2` in single-goal aggregate, but Trial 6 remains a bottleneck.",
            "- The two protocols test different system properties.",
            "",
            "## What Not To Claim",
            "",
            "- Do not claim statistical significance.",
            "- Do not claim a safety guarantee.",
            "- Do not mix `goal_repeat=1` and `goal_repeat=10` into one aggregate without protocol labels.",
            "- Do not claim diagnostic labels prove exact root cause.",
            "- Do not claim `risk_adapter_v21` solves all failures.",
            "- Do not describe `risk_adapter_v1` as overall best after including `fixed_s080`.",
            "",
            "## Next Recommended Work",
            "",
            "- Update paper tables and figures to use this protocol split.",
            "- Keep repeated-goal stress results separate from single-goal mission results.",
            "- Inspect Trial 6 failure families before any `risk_adapter_v21.1` or `risk_adapter_v22` tuning.",
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

    protocols = PROTOCOL_ORDER
    methods = [method for method in PLOT_METHOD_ORDER if any(row["method"] == method for row in aggregate_rows)]
    rate_lookup = {
        (row["protocol"], row["method"]): float(row["aggregate_success_percent"])
        for row in aggregate_rows
    }
    colors = {
        "original": "#8a8d91",
        "fixed_s085": "#6b8fb3",
        "windlevel_s085": "#72a276",
        "risk_adapter_v1": "#b45f4d",
        "fixed_s080": "#5b6c8f",
        "risk_adapter_v2": "#c78f3a",
        "risk_adapter_v21": "#7f5fa8",
    }
    width = 0.11
    x_positions = list(range(len(protocols)))

    fig, ax = plt.subplots(figsize=(10.5, 5.2))
    for index, method in enumerate(methods):
        legend_drawn = False
        for x, protocol in zip(x_positions, protocols):
            if (protocol, method) not in rate_lookup:
                continue
            height = rate_lookup[(protocol, method)]
            offset = x + (index - (len(methods) - 1) / 2.0) * width
            bars = ax.bar(
                [offset],
                [height],
                width=width,
                label=method if not legend_drawn else None,
                color=colors.get(method, "#777777"),
            )
            legend_drawn = True
            bar = bars[0]
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height + 1.5,
                "%.1f%%" % height,
                ha="center",
                va="bottom",
                fontsize=8,
                rotation=90,
            )

    ax.set_xticks(x_positions)
    ax.set_xticklabels(["single-goal\nmission", "repeated-goal\nstress"])
    ax.set_ylabel("Strict-valid success rate (%)")
    ax.set_ylim(0, 110)
    ax.set_title("Stage 4 protocol-split success rates")
    ax.grid(axis="y", alpha=0.25)
    ax.set_axisbelow(True)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=4, frameon=False)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(str(path), dpi=200)
    plt.close(fig)
    return True


def main():
    args = parse_args()
    metrics_dir = repo_path(args.metrics_dir)
    output_dir = repo_path(args.output_dir)

    single_rows = build_success_rows(metrics_dir, PROTOCOL_SINGLE)
    repeated_rows = build_success_rows(metrics_dir, PROTOCOL_REPEATED)
    success_rows = single_rows + repeated_rows
    aggregate_rows = build_aggregate_rows(success_rows)

    write_csv(
        output_dir / "stage4_single_goal_success_table.csv",
        SUCCESS_FIELDS,
        single_rows,
    )
    write_markdown_table(
        output_dir / "stage4_single_goal_success_table.md",
        "Stage 4 Single-Goal Success Table",
        SUCCESS_FIELDS,
        single_rows,
    )
    write_csv(
        output_dir / "stage4_repeated_goal_stress_success_table.csv",
        SUCCESS_FIELDS,
        repeated_rows,
    )
    write_markdown_table(
        output_dir / "stage4_repeated_goal_stress_success_table.md",
        "Stage 4 Repeated-Goal Stress Success Table",
        SUCCESS_FIELDS,
        repeated_rows,
    )
    write_csv(
        output_dir / "stage4_protocol_split_aggregate_table.csv",
        AGGREGATE_FIELDS,
        aggregate_rows,
    )
    write_markdown_table(
        output_dir / "stage4_protocol_split_aggregate_table.md",
        "Stage 4 Protocol-Split Aggregate Table",
        AGGREGATE_FIELDS,
        aggregate_rows,
    )
    (output_dir / "stage4_protocol_split_summary.md").write_text(
        build_summary(single_rows, repeated_rows, aggregate_rows),
        encoding="utf-8",
    )
    plot_written = write_plot(
        output_dir / "stage4_protocol_split_success_rates.png",
        aggregate_rows,
    )

    if args.print_summary:
        print("Stage 4 protocol-split paper assets")
        print("single_goal_rows: %d" % len(single_rows))
        print("repeated_goal_rows: %d" % len(repeated_rows))
        for protocol in PROTOCOL_ORDER:
            best = min(
                [row for row in aggregate_rows if row["protocol"] == protocol],
                key=lambda row: int(row["rank_within_protocol"]),
            )
            print(
                "%s_best: %s %s/%s (%s%%)"
                % (
                    protocol,
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
