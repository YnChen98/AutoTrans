#!/usr/bin/env python3
"""Generate the Stage 4-BC paper-ready Pareto frontier figure."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt


@dataclass(frozen=True)
class MethodPoint:
    label: str
    single_goal: int
    stress: int
    frontier: bool
    dx: float
    dy: float
    ha: str = "left"
    va: str = "center"


POINTS = (
    MethodPoint("Original", 21, 18, False, 0.10, -0.38),
    MethodPoint("Fixed 0.85", 22, 18, False, 0.10, 0.35),
    MethodPoint("Wind-Level 0.85", 26, 16, True, -0.10, 0.55, ha="right"),
    MethodPoint("Fixed 0.80", 21, 24, True, 0.10, 0.30),
    MethodPoint("Risk Adapter v1", 25, 23, True, -0.12, 0.42, ha="right"),
    MethodPoint("Risk Adapter v2.1", 25, 20, False, -0.12, -0.42, ha="right"),
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate compact paper-facing Stage 4 Pareto frontier PNG/SVG "
            "assets for the RA-L scaffold."
        )
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=repo_root() / "paper" / "stage4_governor_ral" / "figures",
        help="Directory for fig3_pareto.png and fig3_pareto.svg.",
    )
    return parser.parse_args()


def configure_matplotlib() -> None:
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "font.size": 7,
            "axes.labelsize": 7.4,
            "axes.linewidth": 0.7,
            "xtick.labelsize": 6.7,
            "ytick.labelsize": 6.7,
            "legend.fontsize": 5.9,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )


def draw_pareto(output_dir: Path) -> tuple[Path, Path]:
    configure_matplotlib()

    frontier = [p for p in POINTS if p.frontier]
    non_frontier = [p for p in POINTS if not p.frontier]
    frontier_line = sorted(frontier, key=lambda p: p.single_goal)

    fig, ax = plt.subplots(figsize=(3.35, 2.35))

    ax.plot(
        [p.single_goal for p in frontier_line],
        [p.stress for p in frontier_line],
        color="#2b5c8a",
        linewidth=1.15,
        alpha=0.9,
        zorder=1,
        label="Observed frontier",
    )
    ax.scatter(
        [p.single_goal for p in non_frontier],
        [p.stress for p in non_frontier],
        marker="o",
        s=32,
        facecolor="white",
        edgecolor="#6f7378",
        linewidth=1.0,
        zorder=3,
        label="Other evaluated",
    )
    ax.scatter(
        [p.single_goal for p in frontier],
        [p.stress for p in frontier],
        marker="D",
        s=42,
        facecolor="#2b5c8a",
        edgecolor="#1f2f43",
        linewidth=0.7,
        zorder=4,
        label="Frontier method",
    )

    text_effect = [pe.withStroke(linewidth=2.0, foreground="white")]
    for point in POINTS:
        ax.text(
            point.single_goal + point.dx,
            point.stress + point.dy,
            point.label,
            ha=point.ha,
            va=point.va,
            fontsize=6.2,
            color="#20242a",
            path_effects=text_effect,
            zorder=5,
        )

    ax.set_xlim(20.5, 26.5)
    ax.set_ylim(15.5, 24.5)
    ax.set_xticks([21, 22, 23, 24, 25, 26])
    ax.set_yticks([16, 18, 20, 22, 24])
    ax.set_xlabel("Single-goal strict-valid count / 30")
    ax.set_ylabel("Goal-reissue stress strict-valid count / 30")
    ax.grid(True, color="#d8dde3", linewidth=0.55, alpha=0.65)
    ax.tick_params(length=3.0, width=0.65, color="#44484d")
    ax.legend(
        loc="lower center",
        bbox_to_anchor=(0.5, 1.01),
        ncol=3,
        frameon=False,
        borderaxespad=0.0,
        handlelength=1.3,
        handletextpad=0.45,
        columnspacing=0.9,
    )

    fig.subplots_adjust(left=0.16, right=0.98, bottom=0.20, top=0.89)

    output_dir.mkdir(parents=True, exist_ok=True)
    png_path = output_dir / "fig3_pareto.png"
    svg_path = output_dir / "fig3_pareto.svg"
    fig.savefig(png_path, dpi=600, bbox_inches="tight", pad_inches=0.02)
    fig.savefig(svg_path, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    strip_trailing_whitespace(svg_path)
    return png_path, svg_path


def strip_trailing_whitespace(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    path.write_text(
        "\n".join(line.rstrip() for line in text.splitlines()) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    args = parse_args()
    png_path, svg_path = draw_pareto(args.output_dir)
    print(f"wrote {png_path}")
    print(f"wrote {svg_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
