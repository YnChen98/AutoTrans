#!/usr/bin/env python3
"""Generate paper-facing Stage 4 invalid-only failure-group Figure 5 assets."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


PROTOCOLS = [
    ("single_goal_mission", "Single-goal mission"),
    ("goal_reissue_stress", "Goal-reissue stress"),
]

METHOD_ORDER = [
    "original",
    "fixed_s085",
    "windlevel_s085",
    "fixed_s080",
    "risk_adapter_v1",
    "risk_adapter_v21",
]

DISPLAY_NAMES = {
    "original": "Original",
    "fixed_s085": "Fixed Scale 0.85",
    "windlevel_s085": "Wind-Level 0.85",
    "fixed_s080": "Fixed Scale 0.80",
    "risk_adapter_v1": "Risk Adapter v1",
    "risk_adapter_v21": "Risk Adapter v2.1",
}

GROUP_ORDER = [
    "command_control_upstream",
    "planner_reference_upstream",
    "state_task_upstream",
]

GROUP_LABELS = {
    "command_control_upstream": "Command/control",
    "planner_reference_upstream": "Planner/reference",
    "state_task_upstream": "State/task",
}

GROUP_COLORS = {
    "command_control_upstream": "#8f5d5d",
    "planner_reference_upstream": "#6a8f6a",
    "state_task_upstream": "#5b6c8f",
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def parse_args() -> argparse.Namespace:
    root = repo_root()
    parser = argparse.ArgumentParser(
        description="Generate paper-facing invalid-only failure-group PNG/SVG assets."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=(
            root
            / "experiments"
            / "results"
            / "stage4_failure_mode_paper_assets"
            / "stage4_failure_group_invalid_only_table.csv"
        ),
        help="Stage 4 invalid-only failure-group CSV table.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=root / "paper" / "stage4_governor_ral" / "figures",
        help="Directory for fig5_invalid_failure_groups PNG/SVG outputs.",
    )
    return parser.parse_args()


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"required failure-group table not found: {path}")
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def configure_matplotlib() -> None:
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "font.size": 6.6,
            "axes.labelsize": 6.8,
            "axes.linewidth": 0.65,
            "xtick.labelsize": 5.8,
            "ytick.labelsize": 6.0,
            "legend.fontsize": 5.8,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )


def strip_trailing_whitespace(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    path.write_text(
        "\n".join(line.rstrip() for line in text.splitlines()) + "\n",
        encoding="utf-8",
    )


def draw(rows: list[dict[str, str]], output_dir: Path) -> tuple[Path, Path]:
    configure_matplotlib()
    lookup: dict[tuple[str, str], dict[str, int]] = defaultdict(dict)
    for row in rows:
        protocol = row["protocol"]
        method = row["method"]
        group = row["failure_group"]
        if method not in METHOD_ORDER or group not in GROUP_ORDER:
            continue
        lookup[(protocol, method)][group] = int(row["count"])

    totals = [
        sum(lookup[(protocol, method)].values())
        for protocol, _ in PROTOCOLS
        for method in METHOD_ORDER
    ]
    y_max = max(totals) if totals else 1

    fig, axes = plt.subplots(2, 1, figsize=(3.45, 4.10), sharex=True)
    for ax, (protocol, label) in zip(axes, PROTOCOLS):
        y_positions = list(range(len(METHOD_ORDER)))
        lefts = [0] * len(METHOD_ORDER)
        for group in GROUP_ORDER:
            widths = [
                lookup[(protocol, method)].get(group, 0)
                for method in METHOD_ORDER
            ]
            ax.barh(
                y_positions,
                widths,
                height=0.62,
                left=lefts,
                color=GROUP_COLORS[group],
                label=GROUP_LABELS[group],
            )
            lefts = [left + width for left, width in zip(lefts, widths)]
        ax.set_title(label, fontsize=7.0, pad=3.0)
        ax.set_yticks(y_positions)
        ax.set_yticklabels([DISPLAY_NAMES[method] for method in METHOD_ORDER])
        ax.invert_yaxis()
        ax.set_xlim(0, max(10, y_max + 2))
        ax.grid(axis="x", color="#d8dee6", linewidth=0.5, alpha=0.72)
        ax.set_axisbelow(True)
    axes[1].set_xlabel("Invalid-run count")

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.02),
        ncol=3,
        frameon=False,
        columnspacing=0.8,
        handlelength=1.3,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.94), pad=0.35)

    output_dir.mkdir(parents=True, exist_ok=True)
    png_path = output_dir / "fig5_invalid_failure_groups.png"
    svg_path = output_dir / "fig5_invalid_failure_groups.svg"
    metadata = {"Creator": "generate_stage4_paper_ready_failure_groups.py", "Date": "2026-05-21"}
    fig.savefig(png_path, dpi=600, bbox_inches="tight", pad_inches=0.02, metadata=metadata)
    fig.savefig(svg_path, bbox_inches="tight", pad_inches=0.02, metadata=metadata)
    plt.close(fig)
    strip_trailing_whitespace(svg_path)
    return png_path, svg_path


def main() -> int:
    args = parse_args()
    rows = read_rows(args.input)
    png_path, svg_path = draw(rows, args.output_dir)
    print(f"read {args.input}")
    print(f"wrote {png_path}")
    print(f"wrote {svg_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
