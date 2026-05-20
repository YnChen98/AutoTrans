#!/usr/bin/env python3
"""Generate paper-facing Stage 4 protocol-regret Figure 4 assets."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


DISPLAY_NAMES = {
    "original": "Original",
    "fixed_s085": "Fixed Scale 0.85",
    "windlevel_s085": "Wind-Level 0.85",
    "fixed_s080": "Fixed Scale 0.80",
    "risk_adapter_v1": "Risk Adapter v1",
    "risk_adapter_v21": "Risk Adapter v2.1",
}

METHOD_ORDER = [
    "risk_adapter_v1",
    "fixed_s080",
    "risk_adapter_v21",
    "windlevel_s085",
    "fixed_s085",
    "original",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def parse_args() -> argparse.Namespace:
    root = repo_root()
    parser = argparse.ArgumentParser(
        description="Generate paper-facing protocol regret PNG/SVG assets."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=(
            root
            / "experiments"
            / "results"
            / "stage4_balanced_robustness_assets"
            / "stage4_protocol_regret_table.csv"
        ),
        help="Stage 4 protocol-regret CSV table.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=root / "paper" / "stage4_governor_ral" / "figures",
        help="Directory for fig4_protocol_regret PNG/SVG outputs.",
    )
    return parser.parse_args()


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"required protocol-regret table not found: {path}")
    with path.open("r", newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    lookup = {row["method"]: row for row in rows}
    missing = [method for method in METHOD_ORDER if method not in lookup]
    if missing:
        raise RuntimeError(f"missing expected methods in protocol-regret table: {missing}")
    return [lookup[method] for method in METHOD_ORDER]


def configure_matplotlib() -> None:
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "font.size": 7.0,
            "axes.labelsize": 7.2,
            "axes.linewidth": 0.65,
            "xtick.labelsize": 6.1,
            "ytick.labelsize": 6.2,
            "legend.fontsize": 6.2,
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
    methods = [row["method"] for row in rows]
    x_positions = list(range(len(methods)))
    single_regret = [int(row["single_goal_regret"]) for row in rows]
    stress_regret = [int(row["stress_regret"]) for row in rows]
    totals = [int(row["total_regret"]) for row in rows]

    fig, ax = plt.subplots(figsize=(3.45, 2.45))
    ax.bar(
        x_positions,
        single_regret,
        width=0.62,
        color="#5b8cc0",
        label="Single-goal regret",
    )
    ax.bar(
        x_positions,
        stress_regret,
        width=0.62,
        bottom=single_regret,
        color="#b8895a",
        label="Goal-reissue regret",
    )
    for x_value, total in zip(x_positions, totals):
        ax.text(x_value, total + 0.18, str(total), ha="center", va="bottom", fontsize=6.0)

    ax.set_ylabel("Protocol regret (runs)")
    ax.set_xticks(x_positions)
    ax.set_xticklabels([DISPLAY_NAMES[method] for method in methods], rotation=35, ha="right")
    ax.set_ylim(0, max(totals) + 1.8)
    ax.grid(axis="y", color="#d8dee6", linewidth=0.5, alpha=0.72)
    ax.set_axisbelow(True)
    ax.legend(loc="upper left", frameon=False, ncol=1, handlelength=1.3)
    fig.tight_layout(pad=0.35)

    output_dir.mkdir(parents=True, exist_ok=True)
    png_path = output_dir / "fig4_protocol_regret.png"
    svg_path = output_dir / "fig4_protocol_regret.svg"
    metadata = {"Creator": "generate_stage4_paper_ready_protocol_regret.py", "Date": "2026-05-21"}
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
