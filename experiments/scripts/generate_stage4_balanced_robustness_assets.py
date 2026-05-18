#!/usr/bin/env python3
"""Generate Stage 4-AC balanced robustness / protocol regret assets."""

import argparse
import csv
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]

SINGLE_TOTAL = 30
STRESS_TOTAL = 30
SINGLE_ORACLE_METHOD = "windlevel_s085"
STRESS_ORACLE_METHOD = "fixed_s080"
SINGLE_ORACLE_VALID = 26
STRESS_ORACLE_VALID = 24
ORACLE_TOTAL_VALID = SINGLE_ORACLE_VALID + STRESS_ORACLE_VALID

METHOD_ORDER = [
    "original",
    "fixed_s085",
    "windlevel_s085",
    "fixed_s080",
    "risk_adapter_v1",
    "risk_adapter_v21",
]

METHOD_ROLES = {
    "original": "unadapted baseline",
    "fixed_s085": "fixed static baseline",
    "windlevel_s085": "single-goal specialist heuristic",
    "fixed_s080": "stress specialist static frontier",
    "risk_adapter_v1": "balanced learned/risk-conditioned governor",
    "risk_adapter_v21": "strong nominal learned/risk-conditioned variant",
}

COUNTS = {
    "original": {"single": 21, "stress": 18},
    "fixed_s085": {"single": 22, "stress": 18},
    "windlevel_s085": {"single": 26, "stress": 16},
    "fixed_s080": {"single": 21, "stress": 24},
    "risk_adapter_v1": {"single": 25, "stress": 23},
    "risk_adapter_v21": {"single": 25, "stress": 20},
}

SINGLE_PROTOCOL_ONLY = [
    {
        "method": "risk_adapter_v2",
        "single_goal_valid": "21",
        "single_goal_total": str(SINGLE_TOTAL),
        "single_goal_success_rate": "0.700",
        "stress_valid": "",
        "stress_total": "",
        "stress_success_rate": "",
        "reason_excluded_from_balanced_ranking": (
            "goal-reissue stress protocol result is missing"
        ),
        "note": (
            "include as single-protocol evidence only; do not assign "
            "cross-protocol balance or regret metrics"
        ),
    }
]

BALANCED_FIELDS = [
    "method",
    "single_goal_valid",
    "single_goal_total",
    "single_goal_success_rate",
    "stress_valid",
    "stress_total",
    "stress_success_rate",
    "mean_valid_count",
    "mean_success_rate",
    "worst_protocol_valid",
    "worst_protocol_success_rate",
    "protocol_gap_valid_count",
    "protocol_gap_rate",
    "single_goal_regret",
    "stress_regret",
    "total_regret",
    "normalized_total_regret",
    "pareto_frontier",
    "method_role",
]

REGRET_FIELDS = [
    "method",
    "single_goal_regret",
    "stress_regret",
    "total_regret",
    "normalized_total_regret",
    "method_role",
]

PARETO_FIELDS = [
    "method",
    "single_goal_valid",
    "stress_valid",
    "pareto_frontier",
    "dominated_by",
    "method_role",
]

SINGLE_ONLY_FIELDS = [
    "method",
    "single_goal_valid",
    "single_goal_total",
    "single_goal_success_rate",
    "stress_valid",
    "stress_total",
    "stress_success_rate",
    "reason_excluded_from_balanced_ranking",
    "note",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate Stage 4-AC balanced robustness / protocol regret assets."
    )
    parser.add_argument(
        "--output-dir",
        default="experiments/results/stage4_balanced_robustness_assets",
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


def dominates(candidate, target):
    return (
        candidate["single"] >= target["single"]
        and candidate["stress"] >= target["stress"]
        and (
            candidate["single"] > target["single"]
            or candidate["stress"] > target["stress"]
        )
    )


def dominated_by(method):
    target = COUNTS[method]
    dominators = [
        other
        for other in METHOD_ORDER
        if other != method and dominates(COUNTS[other], target)
    ]
    return ", ".join(dominators)


def is_pareto(method):
    return dominated_by(method) == ""


def build_balanced_rows():
    rows = []
    for method in METHOD_ORDER:
        single = COUNTS[method]["single"]
        stress = COUNTS[method]["stress"]
        single_rate = float(single) / SINGLE_TOTAL
        stress_rate = float(stress) / STRESS_TOTAL
        mean_count = (single + stress) / 2.0
        mean_rate = (single_rate + stress_rate) / 2.0
        worst_count = min(single, stress)
        worst_rate = min(single_rate, stress_rate)
        gap_count = abs(single - stress)
        gap_rate = abs(single_rate - stress_rate)
        single_regret = SINGLE_ORACLE_VALID - single
        stress_regret = STRESS_ORACLE_VALID - stress
        total_regret = single_regret + stress_regret
        normalized_total_regret = float(total_regret) / ORACLE_TOTAL_VALID
        rows.append(
            {
                "method": method,
                "single_goal_valid": str(single),
                "single_goal_total": str(SINGLE_TOTAL),
                "single_goal_success_rate": "%.3f" % single_rate,
                "stress_valid": str(stress),
                "stress_total": str(STRESS_TOTAL),
                "stress_success_rate": "%.3f" % stress_rate,
                "mean_valid_count": "%.1f" % mean_count,
                "mean_success_rate": "%.3f" % mean_rate,
                "worst_protocol_valid": str(worst_count),
                "worst_protocol_success_rate": "%.3f" % worst_rate,
                "protocol_gap_valid_count": str(gap_count),
                "protocol_gap_rate": "%.3f" % gap_rate,
                "single_goal_regret": str(single_regret),
                "stress_regret": str(stress_regret),
                "total_regret": str(total_regret),
                "normalized_total_regret": "%.3f" % normalized_total_regret,
                "pareto_frontier": "true" if is_pareto(method) else "false",
                "method_role": METHOD_ROLES[method],
            }
        )
    return rows


def build_regret_rows(balanced_rows):
    rows = []
    for row in sorted(
        balanced_rows,
        key=lambda item: (
            int(item["total_regret"]),
            int(item["stress_regret"]),
            METHOD_ORDER.index(item["method"]),
        ),
    ):
        rows.append({field: row.get(field, "") for field in REGRET_FIELDS})
    return rows


def build_pareto_rows():
    rows = []
    for method in METHOD_ORDER:
        rows.append(
            {
                "method": method,
                "single_goal_valid": str(COUNTS[method]["single"]),
                "stress_valid": str(COUNTS[method]["stress"]),
                "pareto_frontier": "true" if is_pareto(method) else "false",
                "dominated_by": dominated_by(method),
                "method_role": METHOD_ROLES[method],
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


def method_row(rows, method):
    for row in rows:
        if row["method"] == method:
            return row
    raise KeyError(method)


def pareto_methods(pareto_rows):
    return [row["method"] for row in pareto_rows if row["pareto_frontier"] == "true"]


def build_summary(balanced_rows, regret_rows, pareto_rows, single_only_rows, plots):
    v1 = method_row(balanced_rows, "risk_adapter_v1")
    wind = method_row(balanced_rows, "windlevel_s085")
    fixed80 = method_row(balanced_rows, "fixed_s080")
    v21 = method_row(balanced_rows, "risk_adapter_v21")
    return "\n".join(
        [
            "# Stage 4-AC Balanced Robustness Summary",
            "",
            "## Executive Summary",
            "",
            "Stage 4-AC converts the completed protocol-split Stage 4 results into balanced robustness, protocol regret, and Pareto-frontier paper assets.",
            "",
            "`risk_adapter_v1` has the best mean valid count (`%s/30`), the best worst-protocol valid count (`%s/30`), and the lowest total regret (`%s`) relative to the protocol oracle. It is therefore the current balanced learned / risk-conditioned protagonist." % (
                v1["mean_valid_count"],
                v1["worst_protocol_valid"],
                v1["total_regret"],
            ),
            "",
            "`windlevel_s085` remains the single-goal specialist, while `fixed_s080` remains the goal-reissue stress specialist. `risk_adapter_v21` ties `risk_adapter_v1` in single-goal count but is dominated by `risk_adapter_v1` under stress.",
            "",
            "## Protocol Oracles",
            "",
            "- single-goal mission protocol (`goal_repeat=1`): `%s` with `%d/%d` strict-valid" % (
                SINGLE_ORACLE_METHOD,
                SINGLE_ORACLE_VALID,
                SINGLE_TOTAL,
            ),
            "- goal-reissue stress protocol (`goal_repeat=10`): `%s` with `%d/%d` strict-valid" % (
                STRESS_ORACLE_METHOD,
                STRESS_ORACLE_VALID,
                STRESS_TOTAL,
            ),
            "",
            "## Balanced Robustness Ranking",
            "",
            markdown_table(BALANCED_FIELDS, balanced_rows),
            "",
            "Ranking by mean and worst-protocol performance favors `risk_adapter_v1`: it reaches `%s/30` mean valid count and `%s/30` worst-protocol valid count." % (
                v1["mean_valid_count"],
                v1["worst_protocol_valid"],
            ),
            "",
            "`windlevel_s085` is best in single-goal (`%s/30`) but has a large protocol gap of `%s` valid runs. `fixed_s080` is best in stress (`%s/30`) but weaker in single-goal (`%s/30`)." % (
                wind["single_goal_valid"],
                wind["protocol_gap_valid_count"],
                fixed80["stress_valid"],
                fixed80["single_goal_valid"],
            ),
            "",
            "## Protocol Regret Analysis",
            "",
            markdown_table(REGRET_FIELDS, regret_rows),
            "",
            "`risk_adapter_v1` has the lowest total regret (`%s`), with `single_goal_regret=%s` and `stress_regret=%s`. This supports the balanced-governor framing rather than a single-protocol winner story." % (
                v1["total_regret"],
                v1["single_goal_regret"],
                v1["stress_regret"],
            ),
            "",
            "## Pareto Frontier",
            "",
            markdown_table(PARETO_FIELDS, pareto_rows),
            "",
            "Pareto-frontier methods: `%s`." % "`, `".join(pareto_methods(pareto_rows)),
            "",
            "`risk_adapter_v21` is not on the Pareto frontier because `risk_adapter_v1` has the same single-goal count (`%s/30`) and higher stress count (`%s/30` versus `%s/30`)." % (
                v21["single_goal_valid"],
                v1["stress_valid"],
                v21["stress_valid"],
            ),
            "",
            "## Single-Protocol-Only Note For risk_adapter_v2",
            "",
            markdown_table(SINGLE_ONLY_FIELDS, single_only_rows),
            "",
            "`risk_adapter_v2` has a completed single-goal result (`21/30`) but no completed goal-reissue stress result in the current protocol-split table, so it is excluded from complete cross-protocol balanced ranking.",
            "",
            "## Paper-Facing Interpretation",
            "",
            "- `risk_adapter_v1` is the current balanced learned / risk-conditioned protagonist.",
            "- `windlevel_s085` is the single-goal specialist.",
            "- `fixed_s080` is the goal-reissue stress specialist.",
            "- `risk_adapter_v21` remains a strong nominal / single-goal variant, but it is weaker under stress and is dominated by `risk_adapter_v1` in the two-protocol plane.",
            "- No current learned variant wins both protocols in the absolute per-protocol winner sense.",
            "",
            "## What Not To Claim",
            "",
            "- Do not claim statistical significance.",
            "- Do not claim a safety guarantee.",
            "- Do not claim a single mixed-protocol aggregate as the main result.",
            "- Do not claim learned methods dominate heuristic/static baselines.",
            "- Do not claim `risk_adapter_v21` is overall best.",
            "- Do not create `risk_adapter_v22` before reviewing Stage 4-AC outputs.",
            "",
            "## Next Recommended Work",
            "",
            "- Review the Stage 4-AC tables and plots for paper placement.",
            "- Use the Pareto and regret assets to support the Stage 4-AB paper narrative.",
            "- Keep `risk_adapter_v1` as the tentative protagonist unless future evidence changes the balance/regret picture.",
            "- Do not create `risk_adapter_v22` until the balanced robustness evidence has been reviewed.",
            "",
            "## Generated Plot Status",
            "",
            "- `stage4_balanced_robustness_pareto.png`: `%s`" % plots.get("pareto", "skipped"),
            "- `stage4_protocol_regret_bar.png`: `%s`" % plots.get("regret", "skipped"),
            "",
        ]
    )


def write_pareto_plot(path, balanced_rows):
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as exc:
        print("warning: matplotlib unavailable; skipping Pareto plot: %s" % exc, file=sys.stderr)
        return False

    fig, ax = plt.subplots(figsize=(8.2, 6.0))
    frontier_rows = [row for row in balanced_rows if row["pareto_frontier"] == "true"]
    non_frontier_rows = [row for row in balanced_rows if row["pareto_frontier"] != "true"]

    ax.scatter(
        [int(row["single_goal_valid"]) for row in non_frontier_rows],
        [int(row["stress_valid"]) for row in non_frontier_rows],
        s=80,
        color="#8a8f98",
        label="non-frontier",
    )
    ax.scatter(
        [int(row["single_goal_valid"]) for row in frontier_rows],
        [int(row["stress_valid"]) for row in frontier_rows],
        s=120,
        color="#1f6f8b",
        label="Pareto frontier",
    )
    for row in balanced_rows:
        ax.annotate(
            row["method"],
            (int(row["single_goal_valid"]), int(row["stress_valid"])),
            xytext=(5, 5),
            textcoords="offset points",
            fontsize=8,
        )
    ordered_frontier = sorted(frontier_rows, key=lambda row: int(row["single_goal_valid"]))
    ax.plot(
        [int(row["single_goal_valid"]) for row in ordered_frontier],
        [int(row["stress_valid"]) for row in ordered_frontier],
        color="#1f6f8b",
        linewidth=1.0,
        alpha=0.75,
    )
    ax.set_xlabel("single-goal strict-valid count / 30")
    ax.set_ylabel("goal-reissue stress strict-valid count / 30")
    ax.set_title("Stage 4-AC protocol-split Pareto frontier")
    ax.set_xlim(15, 27)
    ax.set_ylim(15, 25)
    ax.grid(alpha=0.25)
    ax.legend(frameon=False, loc="lower left")
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(str(path), dpi=200)
    plt.close(fig)
    return True


def write_regret_plot(path, regret_rows):
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as exc:
        print("warning: matplotlib unavailable; skipping regret plot: %s" % exc, file=sys.stderr)
        return False

    methods = [row["method"] for row in regret_rows]
    single_regrets = [int(row["single_goal_regret"]) for row in regret_rows]
    stress_regrets = [int(row["stress_regret"]) for row in regret_rows]
    x_values = list(range(len(methods)))

    fig, ax = plt.subplots(figsize=(9.2, 5.2))
    ax.bar(x_values, single_regrets, color="#6d8db3", label="single-goal regret")
    ax.bar(
        x_values,
        stress_regrets,
        bottom=single_regrets,
        color="#c77d57",
        label="stress regret",
    )
    ax.set_xticks(x_values)
    ax.set_xticklabels(methods, rotation=35, ha="right")
    ax.set_ylabel("regret relative to protocol oracle")
    ax.set_title("Stage 4-AC protocol regret")
    ax.grid(axis="y", alpha=0.25)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(str(path), dpi=200)
    plt.close(fig)
    return True


def main():
    args = parse_args()
    output_dir = repo_path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    balanced_rows = build_balanced_rows()
    regret_rows = build_regret_rows(balanced_rows)
    pareto_rows = build_pareto_rows()

    write_csv(
        output_dir / "stage4_balanced_robustness_table.csv",
        BALANCED_FIELDS,
        balanced_rows,
    )
    write_markdown_table(
        output_dir / "stage4_balanced_robustness_table.md",
        "Stage 4-AC Balanced Robustness Table",
        BALANCED_FIELDS,
        balanced_rows,
    )
    write_csv(
        output_dir / "stage4_protocol_regret_table.csv",
        REGRET_FIELDS,
        regret_rows,
    )
    write_markdown_table(
        output_dir / "stage4_protocol_regret_table.md",
        "Stage 4-AC Protocol Regret Table",
        REGRET_FIELDS,
        regret_rows,
    )
    write_csv(
        output_dir / "stage4_pareto_frontier_table.csv",
        PARETO_FIELDS,
        pareto_rows,
    )
    write_markdown_table(
        output_dir / "stage4_pareto_frontier_table.md",
        "Stage 4-AC Pareto Frontier Table",
        PARETO_FIELDS,
        pareto_rows,
    )
    write_csv(
        output_dir / "stage4_single_protocol_only_table.csv",
        SINGLE_ONLY_FIELDS,
        SINGLE_PROTOCOL_ONLY,
    )
    write_markdown_table(
        output_dir / "stage4_single_protocol_only_table.md",
        "Stage 4-AC Single-Protocol-Only Table",
        SINGLE_ONLY_FIELDS,
        SINGLE_PROTOCOL_ONLY,
    )

    plots = {}
    plots["pareto"] = (
        "written"
        if write_pareto_plot(output_dir / "stage4_balanced_robustness_pareto.png", balanced_rows)
        else "skipped"
    )
    plots["regret"] = (
        "written"
        if write_regret_plot(output_dir / "stage4_protocol_regret_bar.png", regret_rows)
        else "skipped"
    )

    (output_dir / "stage4_balanced_robustness_summary.md").write_text(
        build_summary(
            balanced_rows,
            regret_rows,
            pareto_rows,
            SINGLE_PROTOCOL_ONLY,
            plots,
        ),
        encoding="utf-8",
    )

    if args.print_summary:
        v1 = method_row(balanced_rows, "risk_adapter_v1")
        print("output_dir: %s" % output_dir)
        print("complete_cross_protocol_methods: %d" % len(balanced_rows))
        print("pareto_frontier: %s" % ", ".join(pareto_methods(pareto_rows)))
        print(
            "best_balanced_method: risk_adapter_v1 mean=%s worst=%s total_regret=%s"
            % (
                v1["mean_valid_count"],
                v1["worst_protocol_valid"],
                v1["total_regret"],
            )
        )
        print("pareto_plot: %s" % plots["pareto"])
        print("regret_plot: %s" % plots["regret"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
