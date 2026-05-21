#!/usr/bin/env python3
"""Generate Stage 4-BJ paper-facing Figure 1 and Figure 2 schematics.

The figures are deterministic matplotlib vector schematics for the active
RA-L manuscript. They do not use ROS, simulation, seaborn, training code, or
generated experiment-output directories.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Iterable, Sequence

os.environ.setdefault("SOURCE_DATE_EPOCH", "0")

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.lines import Line2D


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_DIR = REPO_ROOT / "paper" / "stage4_governor_ral" / "figures"

PALETTE = {
    "ink": "#272727",
    "muted": "#686868",
    "grid": "#D9DEE7",
    "stack_fill": "#EFF4FA",
    "stack_edge": "#4E78A0",
    "governor_fill": "#F2F7F4",
    "governor_edge": "#4D8C6A",
    "support_fill": "#F4F2EE",
    "support_edge": "#7A756C",
    "accent_fill": "#F7F1DC",
    "accent_edge": "#A7832F",
    "panel_fill": "#FBFBFA",
    "timeline": "#3F5F83",
}


def configure_matplotlib() -> None:
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": [
                "Arial",
                "Helvetica",
                "DejaVu Sans",
                "Liberation Sans",
                "sans-serif",
            ],
            "svg.fonttype": "none",
            "svg.hashsalt": "stage4-bj-nature-schematics",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "font.size": 6.2,
            "axes.linewidth": 0.8,
            "axes.spines.right": False,
            "axes.spines.top": False,
            "legend.frameon": False,
        }
    )


def strip_trailing_whitespace(path: Path) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text("\n".join(line.rstrip() for line in lines) + "\n", encoding="utf-8")


def add_box(
    ax: plt.Axes,
    center: tuple[float, float],
    size: tuple[float, float],
    label: str,
    *,
    facecolor: str,
    edgecolor: str,
    fontsize: float = 5.8,
    linewidth: float = 0.9,
    zorder: int = 3,
) -> tuple[float, float, float, float]:
    width, height = size
    left = center[0] - width / 2.0
    bottom = center[1] - height / 2.0
    rect = patches.Rectangle(
        (left, bottom),
        width,
        height,
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=linewidth,
        zorder=zorder,
    )
    ax.add_patch(rect)
    ax.text(
        center[0],
        center[1],
        label,
        ha="center",
        va="center",
        fontsize=fontsize,
        color=PALETTE["ink"],
        linespacing=1.05,
        zorder=zorder + 1,
    )
    return (left, bottom, width, height)


def add_group(
    ax: plt.Axes,
    xy: tuple[float, float],
    size: tuple[float, float],
    label: str,
    *,
    facecolor: str,
    edgecolor: str,
) -> None:
    rect = patches.Rectangle(
        xy,
        size[0],
        size[1],
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=0.8,
        alpha=0.72,
        zorder=0,
    )
    ax.add_patch(rect)
    ax.text(
        xy[0] + 0.015,
        xy[1] + size[1] - 0.025,
        label,
        ha="left",
        va="top",
        fontsize=5.4,
        color=edgecolor,
        weight="bold",
        zorder=1,
    )


def add_arrow(
    ax: plt.Axes,
    start: tuple[float, float],
    end: tuple[float, float],
    *,
    color: str = PALETTE["ink"],
    linewidth: float = 1.0,
    linestyle: str = "-",
    mutation_scale: float = 7.5,
    zorder: int = 2,
) -> None:
    arrow = patches.FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=mutation_scale,
        linewidth=linewidth,
        linestyle=linestyle,
        color=color,
        shrinkA=0,
        shrinkB=0,
        zorder=zorder,
    )
    ax.add_patch(arrow)


def add_poly_arrow(
    ax: plt.Axes,
    points: Sequence[tuple[float, float]],
    *,
    color: str = PALETTE["ink"],
    linewidth: float = 1.0,
    linestyle: str = "-",
    mutation_scale: float = 7.5,
    zorder: int = 2,
) -> None:
    if len(points) < 2:
        raise ValueError("A connector needs at least two points.")
    for start, end in zip(points[:-2], points[1:-1]):
        ax.add_line(
            Line2D(
                [start[0], end[0]],
                [start[1], end[1]],
                color=color,
                linewidth=linewidth,
                linestyle=linestyle,
                zorder=zorder,
            )
        )
    add_arrow(
        ax,
        points[-2],
        points[-1],
        color=color,
        linewidth=linewidth,
        linestyle=linestyle,
        mutation_scale=mutation_scale,
        zorder=zorder,
    )


def save_figure(fig: plt.Figure, output_base: Path) -> list[Path]:
    output_base.parent.mkdir(parents=True, exist_ok=True)
    svg_metadata = {
        "Creator": "AutoTrans Stage 4-BJ deterministic matplotlib schematic generator",
        "Date": "1970-01-01T00:00:00",
    }
    pdf_metadata = {
        "Creator": "AutoTrans Stage 4-BJ deterministic matplotlib schematic generator",
    }
    outputs = [
        output_base.with_suffix(".svg"),
        output_base.with_suffix(".pdf"),
        output_base.with_suffix(".png"),
    ]
    fig.savefig(outputs[0], metadata=svg_metadata)
    strip_trailing_whitespace(outputs[0])
    fig.savefig(outputs[1], metadata=pdf_metadata)
    fig.savefig(outputs[2], dpi=600)
    plt.close(fig)
    return outputs


def build_architecture_figure(output_dir: Path) -> list[Path]:
    fig = plt.figure(figsize=(3.55, 2.45), facecolor="white")
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    add_group(
        ax,
        (0.045, 0.625),
        (0.91, 0.27),
        "Unchanged inner stack",
        facecolor=PALETTE["stack_fill"],
        edgecolor=PALETTE["stack_edge"],
    )
    add_group(
        ax,
        (0.045, 0.295),
        (0.68, 0.265),
        "External empirical governor",
        facecolor=PALETTE["governor_fill"],
        edgecolor=PALETTE["governor_edge"],
    )

    top_y = 0.755
    lower_y = 0.425
    box_size = (0.165, 0.13)
    centers = {
        "planner": (0.14, top_y),
        "mpc": (0.37, top_y),
        "so3": (0.60, top_y),
        "plant": (0.83, top_y),
        "risk": (0.14, lower_y),
        "governor": (0.37, lower_y),
        "interface": (0.60, lower_y),
        "logs": (0.83, lower_y),
    }

    add_box(
        ax,
        centers["planner"],
        box_size,
        "Planner /\nreference\ngenerator",
        facecolor="white",
        edgecolor=PALETTE["stack_edge"],
    )
    add_box(
        ax,
        centers["mpc"],
        box_size,
        "Payload\nMPC",
        facecolor="white",
        edgecolor=PALETTE["stack_edge"],
    )
    add_box(
        ax,
        centers["so3"],
        box_size,
        "SO(3)\ncontroller",
        facecolor="white",
        edgecolor=PALETTE["stack_edge"],
    )
    add_box(
        ax,
        centers["plant"],
        box_size,
        "UAV +\nsuspended\npayload",
        facecolor="white",
        edgecolor=PALETTE["stack_edge"],
        fontsize=5.5,
    )

    add_box(
        ax,
        centers["risk"],
        box_size,
        "Risk input /\nwarning scores",
        facecolor="white",
        edgecolor=PALETTE["governor_edge"],
    )
    add_box(
        ax,
        centers["governor"],
        box_size,
        "Risk-conditioned\nexecution\ngovernor",
        facecolor="white",
        edgecolor=PALETTE["governor_edge"],
        fontsize=5.4,
    )
    add_box(
        ax,
        centers["interface"],
        box_size,
        "Command-\nadaptation\ninterface",
        facecolor="white",
        edgecolor=PALETTE["governor_edge"],
        fontsize=5.4,
    )
    add_box(
        ax,
        centers["logs"],
        box_size,
        "Diagnostics /\nlogs",
        facecolor=PALETTE["support_fill"],
        edgecolor=PALETTE["support_edge"],
    )

    half_w = box_size[0] / 2.0
    half_h = box_size[1] / 2.0
    for left_key, right_key in [("planner", "mpc"), ("mpc", "so3"), ("so3", "plant")]:
        add_arrow(
            ax,
            (centers[left_key][0] + half_w, top_y),
            (centers[right_key][0] - half_w, top_y),
            color=PALETTE["ink"],
            linewidth=1.0,
            mutation_scale=7.5,
        )

    for left_key, right_key in [("risk", "governor"), ("governor", "interface")]:
        add_arrow(
            ax,
            (centers[left_key][0] + half_w, lower_y),
            (centers[right_key][0] - half_w, lower_y),
            color=PALETTE["governor_edge"],
            linewidth=1.0,
            mutation_scale=7.5,
        )

    add_arrow(
        ax,
        (centers["interface"][0], lower_y + half_h),
        (centers["so3"][0], top_y - half_h),
        color=PALETTE["governor_edge"],
        linewidth=1.0,
        mutation_scale=7.5,
    )
    ax.text(
        centers["interface"][0] + 0.026,
        0.59,
        "speed scale /\nacceleration scale",
        ha="left",
        va="center",
        fontsize=5.1,
        color=PALETTE["governor_edge"],
        linespacing=1.05,
    )

    add_arrow(
        ax,
        (centers["plant"][0], top_y - half_h),
        (centers["logs"][0], lower_y + half_h),
        color=PALETTE["support_edge"],
        linewidth=0.95,
        mutation_scale=7.0,
    )
    add_poly_arrow(
        ax,
        [
            (centers["logs"][0], lower_y - half_h),
            (centers["logs"][0], 0.18),
            (centers["risk"][0], 0.18),
            (centers["risk"][0], lower_y - half_h),
        ],
        color=PALETTE["support_edge"],
        linewidth=0.9,
        linestyle=(0, (3, 2)),
        mutation_scale=7.0,
    )
    ax.text(
        0.485,
        0.145,
        "feedback support",
        ha="center",
        va="top",
        fontsize=5.0,
        color=PALETTE["support_edge"],
    )

    ax.text(
        0.02,
        0.965,
        "a",
        ha="left",
        va="top",
        fontsize=7.5,
        weight="bold",
        color=PALETTE["ink"],
    )
    return save_figure(fig, output_dir / "fig1_architecture_nature")


def panel_box(
    ax: plt.Axes,
    xy: tuple[float, float],
    width: float,
    height: float,
) -> None:
    ax.add_patch(
        patches.Rectangle(
            xy,
            width,
            height,
            facecolor=PALETTE["panel_fill"],
            edgecolor=PALETTE["grid"],
            linewidth=0.9,
            zorder=0,
        )
    )


def add_timeline_arrow(
    ax: plt.Axes,
    start: tuple[float, float],
    end: tuple[float, float],
) -> None:
    add_arrow(
        ax,
        start,
        end,
        color=PALETTE["timeline"],
        linewidth=1.15,
        mutation_scale=7.5,
        zorder=2,
    )


def add_publish_marker(ax: plt.Axes, x: float, y: float, *, filled: bool = True) -> None:
    ax.add_line(
        Line2D([x, x], [y - 0.05, y + 0.05], color=PALETTE["timeline"], linewidth=0.8)
    )
    circle = patches.Circle(
        (x, y),
        radius=0.010,
        facecolor=PALETTE["timeline"] if filled else "white",
        edgecolor=PALETTE["timeline"],
        linewidth=0.8,
        zorder=3,
    )
    ax.add_patch(circle)


def add_arrival_marker(ax: plt.Axes, x: float, y: float, *, color: str) -> None:
    ax.add_line(Line2D([x, x], [y - 0.065, y + 0.065], color=color, linewidth=1.0))
    ax.add_patch(
        patches.RegularPolygon(
            (x, y),
            numVertices=4,
            radius=0.014,
            orientation=0.785,
            facecolor="white",
            edgecolor=color,
            linewidth=0.9,
            zorder=3,
        )
    )


def build_protocol_figure(output_dir: Path) -> list[Path]:
    fig = plt.figure(figsize=(3.55, 2.05), facecolor="white")
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    left = (0.055, 0.205, 0.405, 0.70)
    right = (0.540, 0.205, 0.405, 0.70)
    panel_box(ax, (left[0], left[1]), left[2], left[3])
    panel_box(ax, (right[0], right[1]), right[2], right[3])

    ax.text(
        left[0] + left[2] / 2.0,
        0.845,
        "Single-goal mission",
        ha="center",
        va="center",
        fontsize=6.4,
        weight="bold",
        color=PALETTE["ink"],
    )
    ax.text(
        left[0] + left[2] / 2.0,
        0.775,
        "Goal repeat = 1",
        ha="center",
        va="center",
        fontsize=5.6,
        color=PALETTE["muted"],
    )

    ax.text(
        right[0] + right[2] / 2.0,
        0.845,
        "Goal-reissue stress",
        ha="center",
        va="center",
        fontsize=6.4,
        weight="bold",
        color=PALETTE["ink"],
    )
    ax.text(
        right[0] + right[2] / 2.0,
        0.775,
        "Goal repeat = 10",
        ha="center",
        va="center",
        fontsize=5.6,
        color=PALETTE["muted"],
    )

    y = 0.485
    left_start = left[0] + 0.085
    left_end = left[0] + left[2] - 0.065
    add_timeline_arrow(ax, (left_start, y), (left_end, y))
    add_publish_marker(ax, left_start, y, filled=True)
    ax.text(
        left_start,
        0.635,
        "goal\npublish",
        ha="center",
        va="center",
        fontsize=5.1,
        color=PALETTE["timeline"],
        linespacing=1.0,
    )
    ax.text(
        (left_start + left_end) / 2.0,
        0.57,
        "transport interval",
        ha="center",
        va="center",
        fontsize=5.2,
        color=PALETTE["ink"],
    )
    ax.add_patch(
        patches.Rectangle(
            (left_end - 0.004, y - 0.036),
            0.035,
            0.072,
            facecolor=PALETTE["accent_fill"],
            edgecolor="none",
            zorder=1,
        )
    )
    add_arrival_marker(ax, left_end, y, color=PALETTE["accent_edge"])
    ax.text(
        left_end,
        0.330,
        "arrival /\nhold",
        ha="center",
        va="center",
        fontsize=5.1,
        color=PALETTE["accent_edge"],
        linespacing=1.0,
    )

    right_start = right[0] + 0.065
    right_end = right[0] + right[2] - 0.065
    add_timeline_arrow(ax, (right_start, y), (right_end, y))
    publish_xs = [
        right_start + i * ((right_end - right_start - 0.075) / 9.0) for i in range(10)
    ]
    for idx, x in enumerate(publish_xs):
        add_publish_marker(ax, x, y, filled=(idx == 0))
    ax.text(
        (publish_xs[0] + publish_xs[-1]) / 2.0,
        0.635,
        "repeated goal\npublishes",
        ha="center",
        va="center",
        fontsize=5.1,
        color=PALETTE["timeline"],
        linespacing=1.0,
    )
    ax.text(
        (right_start + right_end) / 2.0,
        0.57,
        "transport interval",
        ha="center",
        va="center",
        fontsize=5.2,
        color=PALETTE["ink"],
    )
    ax.add_patch(
        patches.Rectangle(
            (right_end - 0.020, y - 0.041),
            0.050,
            0.082,
            facecolor=PALETTE["accent_fill"],
            edgecolor=PALETTE["accent_edge"],
            linewidth=0.6,
            linestyle=(0, (2, 2)),
            zorder=1,
        )
    )
    add_arrival_marker(ax, right_end, y, color=PALETTE["accent_edge"])
    ax.text(
        right_end,
        0.315,
        "arrival /\nreissue\ninteraction",
        ha="center",
        va="center",
        fontsize=4.9,
        color=PALETTE["accent_edge"],
        linespacing=0.95,
    )

    ax.text(
        0.5,
        0.100,
        "Protocols reported separately",
        ha="center",
        va="center",
        fontsize=5.7,
        color=PALETTE["muted"],
    )
    ax.text(
        0.02,
        0.965,
        "b",
        ha="left",
        va="top",
        fontsize=7.5,
        weight="bold",
        color=PALETTE["ink"],
    )
    return save_figure(fig, output_dir / "fig2_protocol_split_nature")


def format_outputs(outputs: Iterable[Path]) -> str:
    return "\n".join(f"- {path}" for path in outputs)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate Stage 4-BJ nature-style schematic figures."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for Figure 1 and Figure 2 SVG/PDF/PNG outputs.",
    )
    parser.add_argument(
        "--print-summary",
        action="store_true",
        help="Print the generated output paths.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    configure_matplotlib()
    outputs = []
    outputs.extend(build_architecture_figure(args.output_dir))
    outputs.extend(build_protocol_figure(args.output_dir))
    if args.print_summary:
        print(format_outputs(outputs))
    else:
        print(f"Generated {len(outputs)} schematic files in {args.output_dir}")


if __name__ == "__main__":
    main()
