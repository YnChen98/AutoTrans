#!/usr/bin/env python3
"""Generate the Stage 4-BD paper-ready representative trace summary figure."""

from __future__ import annotations

import argparse
import csv
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


@dataclass(frozen=True)
class CaseSpec:
    panel: str
    protocol: str
    method: str
    trial: str
    repeat: str
    protocol_label: str
    display_name: str
    outcome_label: str


@dataclass(frozen=True)
class TraceCase:
    spec: CaseSpec
    index_row: dict[str, str]
    rows: list[dict[str, str]]
    time_s: list[float]
    x_end_s: float


SELECTED_CASES = (
    CaseSpec(
        panel="(a)",
        protocol="goal_reissue_stress",
        method="risk_adapter_v21",
        trial="trial4",
        repeat="8",
        protocol_label="T4 goal-reissue",
        display_name="Risk Adapter v2.1",
        outcome_label="failure",
    ),
    CaseSpec(
        panel="(b)",
        protocol="goal_reissue_stress",
        method="risk_adapter_v1",
        trial="trial4",
        repeat="10",
        protocol_label="T4 goal-reissue",
        display_name="Risk Adapter v1",
        outcome_label="success",
    ),
    CaseSpec(
        panel="(c)",
        protocol="single_goal_mission",
        method="windlevel_s085",
        trial="trial6",
        repeat="2",
        protocol_label="T6 single-goal",
        display_name="Wind-Level 0.85",
        outcome_label="success",
    ),
    CaseSpec(
        panel="(d)",
        protocol="single_goal_mission",
        method="risk_adapter_v21",
        trial="trial6",
        repeat="6",
        protocol_label="T6 single-goal",
        display_name="Risk Adapter v2.1",
        outcome_label="failure",
    ),
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def parse_args() -> argparse.Namespace:
    root = repo_root()
    parser = argparse.ArgumentParser(
        description=(
            "Generate compact paper-facing Stage 4 representative trace "
            "summary PNG/SVG assets for the RA-L scaffold."
        )
    )
    parser.add_argument(
        "--index",
        type=Path,
        default=(
            root
            / "experiments"
            / "results"
            / "stage4_representative_traces"
            / "stage4aa_representative_trace_index.csv"
        ),
        help="Representative trace index CSV from Stage 4-AA2.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=root / "paper" / "stage4_governor_ral" / "figures",
        help="Directory for fig6_trace_summary.png and fig6_trace_summary.svg.",
    )
    return parser.parse_args()


def parse_float(value: str | None) -> float:
    if value is None or value == "":
        return math.nan
    try:
        parsed = float(value)
    except ValueError:
        return math.nan
    if not math.isfinite(parsed):
        return math.nan
    return parsed


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"required CSV not found: {path}")
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def select_index_row(index_rows: Iterable[dict[str, str]], spec: CaseSpec) -> dict[str, str]:
    matches = [
        row
        for row in index_rows
        if row.get("protocol") == spec.protocol
        and row.get("method") == spec.method
        and row.get("trial") == spec.trial
        and row.get("repeat") == spec.repeat
    ]
    if len(matches) != 1:
        raise RuntimeError(
            "expected exactly one trace-index row for "
            f"{spec.protocol}/{spec.method}/{spec.trial}/repeat{spec.repeat}; "
            f"found {len(matches)}"
        )
    return matches[0]


def relative_time(rows: list[dict[str, str]]) -> list[float]:
    raw_times = [parse_float(row.get("ros_time")) for row in rows]
    if not any(math.isfinite(value) for value in raw_times):
        raw_times = [parse_float(row.get("wall_time")) for row in rows]
    finite_times = [value for value in raw_times if math.isfinite(value)]
    if not finite_times:
        raise RuntimeError("trace CSV has no finite ros_time or wall_time values")
    first_time = finite_times[0]
    return [value - first_time if math.isfinite(value) else math.nan for value in raw_times]


def choose_x_end(index_row: dict[str, str], time_s: list[float]) -> float:
    finite_time = [value for value in time_s if math.isfinite(value)]
    if not finite_time:
        return 45.0
    max_time = max(finite_time)
    first_nan = parse_float(index_row.get("first_nan_time"))
    first_arrival = parse_float(index_row.get("first_arrival_time"))

    candidates: list[float] = []
    if math.isfinite(first_arrival):
        candidates.append(first_arrival + 18.0)
    if math.isfinite(first_nan):
        candidates.append(first_nan + 4.0)
    else:
        candidates.append(45.0)
    return max(12.0, min(max_time, max(candidates)))


def signal_x_end(case: TraceCase) -> float:
    first_nan = parse_float(case.index_row.get("first_nan_time"))
    if math.isfinite(first_nan):
        return min(case.x_end_s, first_nan)
    return case.x_end_s


def load_cases(index_path: Path) -> list[TraceCase]:
    index_rows = read_csv_rows(index_path)
    cases: list[TraceCase] = []
    for spec in SELECTED_CASES:
        index_row = select_index_row(index_rows, spec)
        csv_path_text = index_row.get("csv_path", "")
        if not csv_path_text:
            raise RuntimeError(
                f"trace-index row for {spec.protocol}/{spec.method}/{spec.trial} "
                f"repeat{spec.repeat} has no csv_path"
            )
        csv_path = Path(csv_path_text)
        rows = read_csv_rows(csv_path)
        time_s = relative_time(rows)
        cases.append(
            TraceCase(
                spec=spec,
                index_row=index_row,
                rows=rows,
                time_s=time_s,
                x_end_s=choose_x_end(index_row, time_s),
            )
        )
    return cases


def column_series(rows: list[dict[str, str]], column: str) -> list[float] | None:
    if not rows or column not in rows[0]:
        return None
    values = [parse_float(row.get(column)) for row in rows]
    if not any(math.isfinite(value) for value in values):
        return None
    return values


def vector_norm_series(
    rows: list[dict[str, str]], columns: tuple[str, str, str]
) -> list[float] | None:
    if not rows or not all(column in rows[0] for column in columns):
        return None
    values: list[float] = []
    any_finite = False
    for row in rows:
        components = [parse_float(row.get(column)) for column in columns]
        if all(math.isfinite(component) for component in components):
            values.append(math.sqrt(sum(component * component for component in components)))
            any_finite = True
        else:
            values.append(math.nan)
    return values if any_finite else None


def xy_error_series(
    rows: list[dict[str, str]],
    point_columns: tuple[str, str],
    target_columns: tuple[str, str],
) -> list[float] | None:
    needed = point_columns + target_columns
    if not rows or not all(column in rows[0] for column in needed):
        return None
    values: list[float] = []
    any_finite = False
    for row in rows:
        px = parse_float(row.get(point_columns[0]))
        py = parse_float(row.get(point_columns[1]))
        tx = parse_float(row.get(target_columns[0]))
        ty = parse_float(row.get(target_columns[1]))
        if all(math.isfinite(value) for value in (px, py, tx, ty)):
            values.append(math.hypot(px - tx, py - ty))
            any_finite = True
        else:
            values.append(math.nan)
    return values if any_finite else None


def xy_displacement_series(
    rows: list[dict[str, str]], point_columns: tuple[str, str]
) -> list[float] | None:
    if not rows or not all(column in rows[0] for column in point_columns):
        return None

    origin: tuple[float, float] | None = None
    values: list[float] = []
    any_finite = False
    for row in rows:
        px = parse_float(row.get(point_columns[0]))
        py = parse_float(row.get(point_columns[1]))
        if not all(math.isfinite(value) for value in (px, py)):
            values.append(math.nan)
            continue
        if origin is None:
            origin = (px, py)
        values.append(math.hypot(px - origin[0], py - origin[1]))
        any_finite = True
    return values if any_finite else None


def finite_pairs(time_s: list[float], values: list[float], x_end_s: float) -> tuple[list[float], list[float]]:
    x_values: list[float] = []
    y_values: list[float] = []
    last_time = -math.inf
    for time_value, value in zip(time_s, values):
        if (
            math.isfinite(time_value)
            and math.isfinite(value)
            and 0.0 <= time_value <= x_end_s
            and abs(value) < 1.0e6
        ):
            if time_value < last_time:
                x_values.append(math.nan)
                y_values.append(math.nan)
            x_values.append(time_value)
            y_values.append(value)
            last_time = time_value
    return x_values, y_values


def set_panel_limits(ax: plt.Axes, y_values: list[float], *, minimum_zero: bool = True) -> None:
    finite_values = [value for value in y_values if math.isfinite(value)]
    if not finite_values:
        return
    y_min = min(finite_values)
    y_max = max(finite_values)
    if minimum_zero:
        y_min = min(0.0, y_min)
    if math.isclose(y_min, y_max):
        pad = max(0.1, abs(y_max) * 0.08)
    else:
        pad = max(0.08, (y_max - y_min) * 0.12)
    ax.set_ylim(y_min - pad, y_max + pad)


def add_time_markers(ax: plt.Axes, index_row: dict[str, str]) -> None:
    first_arrival = parse_float(index_row.get("first_arrival_time"))
    first_nan = parse_float(index_row.get("first_nan_time"))
    if math.isfinite(first_arrival):
        ax.axvline(first_arrival, color="#2f7d5b", linewidth=0.75, linestyle="--", alpha=0.8)
    if math.isfinite(first_nan):
        ax.axvline(first_nan, color="#a83a32", linewidth=0.8, linestyle=":", alpha=0.95)


def style_axis(ax: plt.Axes, case: TraceCase, row_index: int) -> None:
    ax.set_xlim(0.0, case.x_end_s)
    ax.grid(True, color="#d7dde4", linewidth=0.45, alpha=0.62)
    ax.tick_params(axis="both", labelsize=5.7, width=0.55, length=2.0, pad=1.5)
    add_time_markers(ax, case.index_row)
    if row_index < 3:
        ax.tick_params(labelbottom=False)


def plot_speed(ax: plt.Axes, case: TraceCase) -> list[float]:
    uav_speed = vector_norm_series(case.rows, ("uav_vel_x", "uav_vel_y", "uav_vel_z"))
    payload_speed = vector_norm_series(
        case.rows, ("payload_vel_x", "payload_vel_y", "payload_vel_z")
    )
    plotted: list[float] = []
    data_x_end = signal_x_end(case)
    if uav_speed is not None:
        x_values, y_values = finite_pairs(case.time_s, uav_speed, data_x_end)
        ax.plot(x_values, y_values, color="#2b5c8a", linewidth=0.95)
        plotted.extend(y_values)
    if payload_speed is not None:
        x_values, y_values = finite_pairs(case.time_s, payload_speed, data_x_end)
        ax.plot(x_values, y_values, color="#2b5c8a", linewidth=0.95, linestyle="--")
        plotted.extend(y_values)
    set_panel_limits(ax, plotted)
    return plotted


def plot_swing(ax: plt.Axes, case: TraceCase) -> list[float]:
    swing = column_series(case.rows, "swing_angle_deg")
    if swing is None:
        ax.text(0.5, 0.5, "swing not logged", ha="center", va="center", transform=ax.transAxes)
        return []
    x_values, y_values = finite_pairs(case.time_s, swing, signal_x_end(case))
    ax.plot(x_values, y_values, color="#6f4b8b", linewidth=0.95)
    set_panel_limits(ax, y_values)
    return y_values


def plot_xy_travel(ax: plt.Axes, case: TraceCase) -> list[float]:
    travel = xy_displacement_series(case.rows, ("uav_pos_x", "uav_pos_y"))
    if travel is None:
        raise RuntimeError(
            "selected trace lacks finite UAV XY position columns needed for "
            f"{case.spec.protocol}/{case.spec.method}/{case.spec.trial}/"
            f"repeat{case.spec.repeat}"
        )
    x_values, y_values = finite_pairs(case.time_s, travel, signal_x_end(case))
    ax.plot(x_values, y_values, color="#b36b2c", linewidth=0.95)
    set_panel_limits(ax, y_values)
    return y_values


def plot_scale(ax: plt.Axes, case: TraceCase) -> list[float]:
    speed_scale = column_series(case.rows, "command_speed_scale")
    acceleration_scale = column_series(case.rows, "command_acceleration_scale")
    plotted: list[float] = []
    data_x_end = signal_x_end(case)
    if speed_scale is not None:
        x_values, y_values = finite_pairs(case.time_s, speed_scale, data_x_end)
        ax.plot(x_values, y_values, color="#356d3c", linewidth=0.95)
        plotted.extend(y_values)
    if acceleration_scale is not None:
        x_values, y_values = finite_pairs(case.time_s, acceleration_scale, data_x_end)
        ax.plot(x_values, y_values, color="#356d3c", linewidth=0.95, linestyle="--")
        plotted.extend(y_values)
    if plotted:
        ax.set_ylim(0.55, 1.02)
    else:
        ax.text(0.5, 0.5, "scale not logged", ha="center", va="center", transform=ax.transAxes)
        ax.set_ylim(0.0, 1.0)
    return plotted


def configure_matplotlib() -> None:
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "font.size": 6.4,
            "axes.labelsize": 6.6,
            "axes.linewidth": 0.6,
            "xtick.labelsize": 5.8,
            "ytick.labelsize": 5.8,
            "legend.fontsize": 5.8,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )


def draw_summary(cases: list[TraceCase], output_dir: Path) -> tuple[Path, Path]:
    configure_matplotlib()
    fig, axes = plt.subplots(4, 4, figsize=(7.25, 4.95), sharex="col")
    row_labels = ("Speed (m/s)", "Swing (deg)", "UAV XY disp. (m)", "Scale")

    for column_index, case in enumerate(cases):
        axes[0, column_index].set_title(
            f"{case.spec.panel} {case.spec.protocol_label}\n"
            f"{case.spec.display_name} {case.spec.outcome_label}",
            fontsize=6.6,
            pad=4.0,
        )
        plot_speed(axes[0, column_index], case)
        plot_swing(axes[1, column_index], case)
        plot_xy_travel(axes[2, column_index], case)
        plot_scale(axes[3, column_index], case)
        for row_index in range(4):
            style_axis(axes[row_index, column_index], case, row_index)
            if column_index == 0:
                axes[row_index, column_index].set_ylabel(row_labels[row_index])
            else:
                axes[row_index, column_index].tick_params(labelleft=False)
        axes[3, column_index].set_xlabel("time (s)")

    legend_handles = [
        Line2D([0], [0], color="#2b5c8a", linewidth=1.0, label="UAV speed"),
        Line2D(
            [0],
            [0],
            color="#2b5c8a",
            linewidth=1.0,
            linestyle="--",
            label="Payload speed",
        ),
        Line2D([0], [0], color="#356d3c", linewidth=1.0, label="speed scale"),
        Line2D(
            [0],
            [0],
            color="#356d3c",
            linewidth=1.0,
            linestyle="--",
            label="accel. scale",
        ),
        Line2D([0], [0], color="#2f7d5b", linewidth=0.9, linestyle="--", label="arrival"),
        Line2D(
            [0],
            [0],
            color="#a83a32",
            linewidth=0.9,
            linestyle=":",
            label="failure / NaN",
        ),
    ]
    legend_ax = fig.add_axes([0.095, 0.905, 0.86, 0.055])
    legend_ax.axis("off")
    legend_ax.legend(
        handles=legend_handles,
        loc="center",
        ncol=6,
        frameon=False,
        columnspacing=1.0,
        handlelength=1.8,
        handletextpad=0.4,
    )
    fig.subplots_adjust(left=0.075, right=0.995, bottom=0.085, top=0.785, hspace=0.16, wspace=0.08)

    output_dir.mkdir(parents=True, exist_ok=True)
    png_path = output_dir / "fig6_trace_summary.png"
    svg_path = output_dir / "fig6_trace_summary.svg"
    metadata = {"Creator": "generate_stage4_paper_ready_trace_summary.py", "Date": "2026-05-20"}
    fig.savefig(png_path, dpi=600, bbox_inches="tight", pad_inches=0.02, metadata=metadata)
    fig.savefig(svg_path, bbox_inches="tight", pad_inches=0.02, metadata=metadata)
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
    cases = load_cases(args.index)
    png_path, svg_path = draw_summary(cases, args.output_dir)
    print(f"read index {args.index}")
    for case in cases:
        print(
            "selected "
            f"{case.spec.protocol}/{case.spec.method}/{case.spec.trial}/"
            f"repeat{case.spec.repeat}: {case.index_row.get('csv_path')}"
        )
    print(f"wrote {png_path}")
    print(f"wrote {svg_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
