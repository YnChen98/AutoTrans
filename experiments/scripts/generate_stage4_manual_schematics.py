#!/usr/bin/env python3
"""Generate Stage 4 paper-ready manual schematics for Figure 1 and Figure 2."""

import argparse
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib import patches


REPO_ROOT = Path(__file__).resolve().parents[2]


COLORS = {
    "stack": "#E8EEF7",
    "stack_edge": "#365A8C",
    "governor": "#F8E3C1",
    "governor_edge": "#9A6A1E",
    "data": "#E4F2E4",
    "data_edge": "#3F7D4A",
    "environment": "#E8F2F7",
    "environment_edge": "#4F7790",
    "warning": "#F5E6E6",
    "warning_edge": "#8C4E4E",
    "neutral": "#F2F2F2",
    "neutral_edge": "#555555",
    "line": "#222222",
}


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Generate deterministic Stage 4 Figure 1 and Figure 2 schematics "
            "with matplotlib only."
        )
    )
    parser.add_argument(
        "--output-dir",
        default="experiments/results/stage4_paper_figure_package/main",
        help="Output directory for fig1/fig2 PNG, SVG, and summary files.",
    )
    parser.add_argument(
        "--print-summary",
        action="store_true",
        help="Print a concise summary after writing outputs.",
    )
    return parser.parse_args()


def resolve_output_dir(path_text):
    path = Path(path_text).expanduser()
    if path.is_absolute():
        return path
    return (REPO_ROOT / path).resolve()


def set_rcparams():
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["DejaVu Sans", "sans-serif"],
            "svg.fonttype": "none",
            "font.size": 8,
            "axes.linewidth": 0.8,
            "figure.facecolor": "white",
            "savefig.facecolor": "white",
        }
    )


def wrap_label(text, width=18):
    wrapped = []
    for part in text.split("\n"):
        if not part:
            wrapped.append("")
        else:
            wrapped.extend(textwrap.wrap(part, width=width))
    return "\n".join(wrapped)


def draw_box(
    ax,
    x,
    y,
    width,
    height,
    label,
    facecolor,
    edgecolor,
    fontsize=8,
    wrap_width=20,
    linestyle="-",
    linewidth=1.0,
    hatch=None,
):
    box = patches.FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.035,rounding_size=0.045",
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=linewidth,
        linestyle=linestyle,
        hatch=hatch,
    )
    ax.add_patch(box)
    ax.text(
        x + width / 2,
        y + height / 2,
        wrap_label(label, wrap_width),
        ha="center",
        va="center",
        fontsize=fontsize,
        color="#111111",
    )
    return {
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "left": (x, y + height / 2),
        "right": (x + width, y + height / 2),
        "top": (x + width / 2, y + height),
        "bottom": (x + width / 2, y),
        "center": (x + width / 2, y + height / 2),
    }


def draw_arrow(
    ax,
    start,
    end,
    label=None,
    label_offset=(0.0, 0.0),
    color=None,
    linestyle="-",
    connectionstyle="arc3,rad=0.0",
    fontsize=7,
):
    line_color = color or COLORS["line"]
    ax.annotate(
        "",
        xy=end,
        xytext=start,
        arrowprops={
            "arrowstyle": "-|>",
            "color": line_color,
            "linewidth": 1.0,
            "linestyle": linestyle,
            "shrinkA": 4,
            "shrinkB": 4,
            "mutation_scale": 10,
            "connectionstyle": connectionstyle,
        },
    )
    if label:
        ax.text(
            (start[0] + end[0]) / 2 + label_offset[0],
            (start[1] + end[1]) / 2 + label_offset[1],
            wrap_label(label, 24),
            ha="center",
            va="center",
            fontsize=fontsize,
            color=line_color,
            bbox={
                "boxstyle": "round,pad=0.15",
                "facecolor": "white",
                "edgecolor": "none",
                "alpha": 0.9,
            },
        )


def save_figure(fig, output_dir, stem):
    png_path = output_dir / ("%s.png" % stem)
    svg_path = output_dir / ("%s.svg" % stem)
    fig.savefig(png_path, dpi=600, bbox_inches="tight")
    fig.savefig(svg_path, bbox_inches="tight")
    plt.close(fig)
    return [png_path, svg_path]


def generate_figure1(output_dir):
    fig, ax = plt.subplots(figsize=(9.8, 5.7))
    ax.set_xlim(0, 12.3)
    ax.set_ylim(0, 7)
    ax.axis("off")

    ax.text(
        0.1,
        6.82,
        "Figure 1. Stack-compatible execution-governor architecture.",
        ha="left",
        va="top",
        fontsize=11,
        fontweight="bold",
    )

    ax.text(
        3.35,
        6.47,
        "External execution-governor layer",
        ha="left",
        va="center",
        fontsize=8,
        color=COLORS["governor_edge"],
        fontweight="bold",
    )

    task = draw_box(
        ax,
        0.35,
        5.55,
        2.15,
        0.78,
        "Strong wind\nsuspended-payload task",
        COLORS["environment"],
        COLORS["environment_edge"],
        wrap_width=20,
    )
    planner = draw_box(
        ax,
        0.65,
        3.25,
        1.85,
        0.88,
        "AutoTrans-like\nplanner",
        COLORS["stack"],
        COLORS["stack_edge"],
    )
    mpc = draw_box(
        ax,
        2.95,
        3.25,
        1.85,
        0.88,
        "Payload MPC",
        COLORS["stack"],
        COLORS["stack_edge"],
    )
    controller = draw_box(
        ax,
        5.25,
        3.25,
        1.85,
        0.88,
        "SO3 controller",
        COLORS["stack"],
        COLORS["stack_edge"],
    )
    plant = draw_box(
        ax,
        7.55,
        3.15,
        2.25,
        1.08,
        "UAV + suspended\npayload plant /\nsimulator",
        COLORS["stack"],
        COLORS["stack_edge"],
        wrap_width=18,
    )
    risk = draw_box(
        ax,
        6.7,
        5.35,
        2.05,
        0.88,
        "Risk input /\nrisk score",
        COLORS["data"],
        COLORS["data_edge"],
    )
    governor = draw_box(
        ax,
        3.8,
        5.35,
        2.25,
        0.88,
        "Risk-conditioned\nexecution governor",
        COLORS["governor"],
        COLORS["governor_edge"],
        wrap_width=22,
    )
    adapter = draw_box(
        ax,
        3.55,
        1.28,
        2.55,
        0.9,
        "Command-adaptation\ninterface",
        COLORS["governor"],
        COLORS["governor_edge"],
        wrap_width=22,
    )
    logger = draw_box(
        ax,
        8.0,
        1.2,
        1.75,
        0.85,
        "Logger /\ndiagnostics",
        COLORS["data"],
        COLORS["data_edge"],
    )
    failure = draw_box(
        ax,
        10.15,
        1.2,
        1.85,
        0.85,
        "Failure-mode-aware\nanalysis",
        COLORS["neutral"],
        COLORS["neutral_edge"],
        wrap_width=16,
    )
    caveat = draw_box(
        ax,
        0.45,
        0.45,
        2.35,
        0.75,
        "Empirical governor;\nnot a certified\nsafety filter",
        COLORS["warning"],
        COLORS["warning_edge"],
        fontsize=7.5,
        wrap_width=18,
    )

    draw_arrow(ax, planner["right"], mpc["left"], "reference")
    draw_arrow(ax, mpc["right"], controller["left"], "command")
    draw_arrow(ax, controller["right"], plant["left"], "actuation")
    draw_arrow(ax, task["bottom"], plant["top"], "wind / task", label_offset=(0.8, 0.0))

    draw_arrow(
        ax,
        plant["top"],
        risk["right"],
        "plant logs",
        label_offset=(0.2, 0.25),
        connectionstyle="arc3,rad=0.25",
    )
    draw_arrow(ax, logger["top"], risk["bottom"])
    draw_arrow(ax, risk["left"], governor["right"], "risk scores")
    draw_arrow(ax, governor["bottom"], adapter["top"], "scale policy")
    draw_arrow(
        ax,
        adapter["top"],
        (2.78, 3.22),
        "speed_scale\nacceleration_scale",
        label_offset=(-0.55, 0.0),
        connectionstyle="arc3,rad=-0.12",
    )
    draw_arrow(ax, plant["bottom"], logger["top"], "logs")
    draw_arrow(ax, logger["right"], failure["left"], "invalid-run labels", label_offset=(0.0, 0.32))
    draw_arrow(ax, caveat["right"], adapter["left"], "claim boundary", linestyle="--")

    ax.text(
        7.45,
        0.42,
        "Inner stack unchanged; governor modulates execution aggressiveness only.",
        ha="center",
        va="center",
        fontsize=7.4,
        color="#333333",
    )

    return save_figure(fig, output_dir, "fig1_architecture")


def style_protocol_panel(ax, title, goal_repeat):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")
    ax.text(0.2, 4.72, title, ha="left", va="top", fontsize=10, fontweight="bold")
    ax.text(
        0.2,
        4.28,
        "goal_repeat=%s" % goal_repeat,
        ha="left",
        va="top",
        fontsize=8.5,
        bbox={"boxstyle": "round,pad=0.2", "facecolor": "#F7F7F7", "edgecolor": "#777777"},
    )
    ax.annotate(
        "",
        xy=(9.35, 1.05),
        xytext=(0.75, 1.05),
        arrowprops={
            "arrowstyle": "-|>",
            "linewidth": 1.0,
            "color": COLORS["line"],
            "mutation_scale": 10,
        },
    )
    ax.text(9.52, 1.05, "time", ha="left", va="center", fontsize=7.5)


def draw_goal_marker(ax, x, y, label=None):
    ax.plot([x, x], [y - 0.18, y + 1.15], color="#365A8C", linewidth=0.8)
    ax.plot(
        x,
        y + 1.15,
        marker="o",
        markersize=5.5,
        markerfacecolor="white",
        markeredgecolor="#365A8C",
        markeredgewidth=1.0,
    )
    if label:
        ax.text(x, y + 1.42, label, ha="center", va="bottom", fontsize=7)


def draw_reference_marker(ax, x, y, label=None):
    ax.plot(
        x,
        y + 0.52,
        marker="^",
        markersize=5,
        markerfacecolor="#F8E3C1",
        markeredgecolor="#9A6A1E",
        markeredgewidth=0.8,
    )
    ax.plot([x, x], [y + 0.18, y + 0.52], color="#9A6A1E", linewidth=0.7)
    if label:
        ax.text(x, y + 0.72, label, ha="center", va="bottom", fontsize=6.6)


def draw_arrival_marker(ax, x, y, label="arrival"):
    ax.plot([x, x], [y - 0.18, y + 1.55], color="#3F7D4A", linewidth=1.0)
    ax.plot(
        x,
        y + 1.55,
        marker="*",
        markersize=8,
        markerfacecolor="#E4F2E4",
        markeredgecolor="#3F7D4A",
        markeredgewidth=0.9,
    )
    ax.text(x, y + 1.82, label, ha="center", va="bottom", fontsize=7)


def generate_figure2(output_dir):
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.35), gridspec_kw={"wspace": 0.18})
    fig.suptitle(
        "Figure 2. Protocol-split evaluation.",
        x=0.02,
        y=0.98,
        ha="left",
        fontsize=11,
        fontweight="bold",
    )

    left, right = axes
    style_protocol_panel(left, "Single-goal mission protocol", "1")
    style_protocol_panel(right, "Goal-reissue stress protocol", "10")

    left.plot([1.1, 7.35], [1.05, 1.05], color="#365A8C", linewidth=3, solid_capstyle="round")
    left.plot([7.35, 9.0], [1.05, 1.05], color="#3F7D4A", linewidth=3, solid_capstyle="round")
    draw_goal_marker(left, 1.35, 1.05, "goal")
    for idx, x in enumerate([3.0, 5.0]):
        draw_reference_marker(left, x, 1.05, "ref update" if idx == 0 else None)
    draw_arrival_marker(left, 7.35, 1.05)
    left.text(4.2, 0.55, "transport to target", ha="center", va="center", fontsize=8)
    left.text(8.2, 1.72, "arrival / hold", ha="center", va="center", fontsize=8)
    left.text(
        5.0,
        3.25,
        "Tests nominal single-goal execution",
        ha="center",
        va="center",
        fontsize=8.5,
        bbox={"boxstyle": "round,pad=0.25", "facecolor": "#F7F7F7", "edgecolor": "#777777"},
    )

    stress = patches.Rectangle(
        (1.05, 0.62),
        7.75,
        2.48,
        facecolor="#F5E6E6",
        edgecolor="#8C4E4E",
        linewidth=0.8,
        hatch="///",
        alpha=0.55,
    )
    right.add_patch(stress)
    right.text(5.0, 3.18, "repeated-goal / reference-update pressure", ha="center", fontsize=7.4)
    right.plot([1.1, 8.85], [1.05, 1.05], color="#365A8C", linewidth=3, solid_capstyle="round")
    right.plot([6.45, 8.85], [1.05, 1.05], color="#3F7D4A", linewidth=3, solid_capstyle="round")
    goal_xs = [1.25, 1.95, 2.65, 3.35, 4.05, 4.75, 5.45, 6.15, 6.85, 7.55]
    for idx, x in enumerate(goal_xs):
        draw_goal_marker(right, x, 1.05, "goals" if idx == 1 else None)
    for idx, x in enumerate([2.2, 3.6, 5.0, 6.4, 7.8]):
        draw_reference_marker(right, x, 1.05, "ref updates" if idx == 1 else None)
    draw_arrival_marker(right, 6.45, 1.05)
    right.text(4.0, 0.55, "transport + reissue pressure", ha="center", va="center", fontsize=8)
    right.text(7.6, 1.78, "post-arrival /\nreissue interactions", ha="center", va="center", fontsize=7.6)
    right.text(
        5.0,
        3.78,
        "Tests goal-reissue stress and protocol robustness",
        ha="center",
        va="center",
        fontsize=8.4,
        bbox={"boxstyle": "round,pad=0.25", "facecolor": "#F7F7F7", "edgecolor": "#777777"},
    )

    fig.text(
        0.5,
        0.04,
        "Report protocols separately; do not collapse them into a mixed-protocol aggregate.",
        ha="center",
        va="center",
        fontsize=8.5,
        fontweight="bold",
    )

    legend_items = [
        ("open circle", "goal publish"),
        ("triangle", "trajectory/reference update"),
        ("star", "arrival"),
        ("hatched band", "stress interval"),
    ]
    fig.text(
        0.5,
        0.0,
        "Markers: " + "; ".join("%s = %s" % item for item in legend_items),
        ha="center",
        va="bottom",
        fontsize=7.2,
        color="#333333",
    )

    return save_figure(fig, output_dir, "fig2_protocol_split")


def write_summary(output_dir, generated_files):
    summary_path = output_dir / "fig1_fig2_schematic_summary.md"
    lines = [
        "# Stage 4 Figure 1 / Figure 2 Schematic Summary",
        "",
        "## Executive Summary",
        "",
        "Stage 4-AN2 generated deterministic paper schematic files for Figure 1 and Figure 2 using `matplotlib` only.",
        "The schematics are explanatory manuscript assets, not result plots and not new experimental evidence.",
        "",
        "## Generated Files",
        "",
    ]
    for path in generated_files:
        lines.append("- `%s`" % path.name)
    lines.extend(
        [
            "",
            "## Source Script",
            "",
            "- `experiments/scripts/generate_stage4_manual_schematics.py`",
            "",
            "## Claim Supported By Each Figure",
            "",
            "| figure | supported claim | caveat |",
            "| --- | --- | --- |",
            "| Figure 1 | The method is a stack-compatible execution governor that adapts `speed_scale` and `acceleration_scale` outside the unchanged planner / payload MPC / SO3 controller stack. | Empirical governor only; not a certified safety filter and not a planner/controller replacement. |",
            "| Figure 2 | The single-goal mission protocol (`goal_repeat=1`) and goal-reissue stress protocol (`goal_repeat=10`) test different behaviors and should be reported separately. | Explanatory schematic only; not a method-ranking result plot and not a mixed-protocol aggregate. |",
            "",
            "## Reminders",
            "",
            "- `risk_adapter_v1` remains the balanced learned / risk-conditioned protagonist.",
            "- `risk_adapter_v21` remains a strong nominal / single-goal variant or ablation.",
            "- Do not claim statistical significance from these schematics.",
            "- Do not claim a safety guarantee.",
            "- Do not introduce `risk_adapter_v22`.",
            "",
        ]
    )
    summary_path.write_text("\n".join(lines), encoding="utf-8")
    return summary_path


def print_summary(output_dir, generated_files, summary_path):
    print("Stage 4 manual schematic generator")
    print("output_dir: %s" % output_dir)
    for path in generated_files:
        print("generated: %s" % path)
    print("summary: %s" % summary_path)


def main():
    args = parse_args()
    set_rcparams()
    output_dir = resolve_output_dir(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    generated_files = []
    generated_files.extend(generate_figure1(output_dir))
    generated_files.extend(generate_figure2(output_dir))
    summary_path = write_summary(output_dir, generated_files)

    if args.print_summary:
        print_summary(output_dir, generated_files, summary_path)


if __name__ == "__main__":
    main()
