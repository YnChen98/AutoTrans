#!/usr/bin/env python3
"""Inspect Stage 4 logs for command/state divergence timing."""

import argparse
import csv
import glob
import math
import sys
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]

TIME_COLUMNS = ["ros_time", "wall_time"]
UAV_POS_COLUMNS = ["uav_pos_x", "uav_pos_y", "uav_pos_z"]
UAV_VEL_COLUMNS = ["uav_vel_x", "uav_vel_y", "uav_vel_z"]
PAYLOAD_POS_COLUMNS = ["payload_pos_x", "payload_pos_y", "payload_pos_z"]
PAYLOAD_VEL_COLUMNS = ["payload_vel_x", "payload_vel_y", "payload_vel_z"]
SO3_BODYRATE_COLUMNS = ["so3_bodyrate_x", "so3_bodyrate_y", "so3_bodyrate_z"]
STATE_COLUMNS = UAV_POS_COLUMNS + UAV_VEL_COLUMNS + PAYLOAD_POS_COLUMNS + PAYLOAD_VEL_COLUMNS + ["swing_angle_deg"]
COMMAND_COLUMNS = ["so3_thrust"] + SO3_BODYRATE_COLUMNS

OUTPUT_FIELDS = [
    "csv_path",
    "metrics_path",
    "row_count",
    "valid_run_suggested",
    "has_nan_state",
    "metrics_first_nan_time",
    "metrics_max_uav_speed",
    "metrics_max_payload_speed",
    "metrics_max_swing_angle_deg",
    "metrics_final_uav_xy_error",
    "has_any_nonfinite",
    "has_state_nonfinite",
    "has_command_nonfinite",
    "has_command_saturation",
    "has_high_speed",
    "has_position_jump",
    "has_swing_threshold_crossing",
    "first_nonfinite_time",
    "first_nonfinite_column",
    "first_so3_thrust_nan_time",
    "first_so3_bodyrate_nan_time",
    "first_so3_thrust_saturation_time",
    "first_so3_bodyrate_saturation_time",
    "first_uav_speed_gt4_time",
    "first_uav_speed_gt10_time",
    "first_payload_speed_gt4_time",
    "first_payload_speed_gt10_time",
    "first_swing_ge30_time",
    "first_swing_ge60_time",
    "first_uav_position_jump_gt1m_time",
    "first_payload_position_jump_gt1m_time",
    "first_has_trajectory_time",
    "last_finite_uav_position_before_nan",
    "last_finite_payload_position_before_nan",
    "failure_mode_guess",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Inspect Stage 4 CSV logs for command saturation, NaN, high-speed, and jump timing."
    )
    parser.add_argument("--csv", help="Single AutoTrans CSV log to inspect.")
    parser.add_argument("--metrics-glob", help="Glob for *_metrics_summary.txt files to batch inspect.")
    parser.add_argument("--output-csv", help="Output CSV report path for single or batch inspection.")
    parser.add_argument("--print-summary", action="store_true", help="Print compact inspection summary.")
    parser.add_argument("--window-start", type=float, help="Relative-time window start for single-CSV row print.")
    parser.add_argument("--window-end", type=float, help="Relative-time window end for single-CSV row print.")
    parser.add_argument(
        "--so3-thrust-saturation",
        type=float,
        default=59.9,
        help="Absolute SO3 thrust saturation threshold.",
    )
    parser.add_argument(
        "--bodyrate-xy-saturation",
        type=float,
        default=2.99,
        help="Absolute SO3 bodyrate x/y saturation threshold.",
    )
    parser.add_argument(
        "--bodyrate-z-saturation",
        type=float,
        default=1.19,
        help="Absolute SO3 bodyrate z saturation threshold.",
    )
    return parser.parse_args()


def resolve_path(path_text, base=None):
    if not path_text:
        return None
    path = Path(path_text).expanduser()
    if path.is_absolute():
        return path
    if base is not None:
        candidate = (base / path).resolve()
        if candidate.exists():
            return candidate
    return (REPO_ROOT / path).resolve()


def parse_float(value):
    if value is None:
        return math.nan
    text = str(value).strip()
    if text == "":
        return math.nan
    try:
        return float(text)
    except ValueError:
        lowered = text.lower()
        if lowered in ("nan", "+nan", "-nan"):
            return math.nan
        if lowered in ("inf", "+inf", "infinity", "+infinity"):
            return math.inf
        if lowered in ("-inf", "-infinity"):
            return -math.inf
        return math.nan


def parse_bool_text(value):
    if value is None:
        return ""
    text = str(value).strip().lower()
    if text in ("true", "1", "yes"):
        return "true"
    if text in ("false", "0", "no"):
        return "false"
    return str(value).strip()


def format_float(value):
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if not math.isfinite(value):
        return "nan"
    return "%.6f" % value


def format_position(values):
    if not values or any(not math.isfinite(value) for value in values):
        return ""
    return "(%.6f, %.6f, %.6f)" % tuple(values)


def finite_time_base(rows, fieldnames):
    time_column = next((column for column in TIME_COLUMNS if column in fieldnames), None)
    if not time_column:
        raise ValueError("CSV must contain ros_time or wall_time")
    for row in rows:
        value = parse_float(row.get(time_column))
        if math.isfinite(value):
            return time_column, value
    raise ValueError("CSV has no finite timestamps in %s" % time_column)


def relative_time(row, time_column, first_time):
    value = parse_float(row.get(time_column))
    if not math.isfinite(value):
        return math.nan
    return value - first_time


def vector_values(row, columns):
    return [parse_float(row.get(column)) for column in columns]


def vector_norm(values):
    if any(not math.isfinite(value) for value in values):
        return math.nan
    return math.sqrt(sum(value * value for value in values))


def distance(values_a, values_b):
    if not values_a or not values_b:
        return math.nan
    if any(not math.isfinite(value) for value in values_a + values_b):
        return math.nan
    return math.sqrt(sum((a - b) * (a - b) for a, b in zip(values_a, values_b)))


def set_first(result, key, value):
    if result.get(key) == "":
        result[key] = format_float(value)


def inspect_csv(path, args, metrics=None):
    if not path.exists():
        raise FileNotFoundError("CSV file does not exist: %s" % path)
    with path.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)
        fieldnames = list(reader.fieldnames or [])
    if not fieldnames:
        raise ValueError("CSV has no header: %s" % path)
    time_column, first_time = finite_time_base(rows, fieldnames)

    result = {
        "csv_path": str(path),
        "metrics_path": "",
        "row_count": str(len(rows)),
        "valid_run_suggested": "",
        "has_nan_state": "",
        "metrics_first_nan_time": "",
        "metrics_max_uav_speed": "",
        "metrics_max_payload_speed": "",
        "metrics_max_swing_angle_deg": "",
        "metrics_final_uav_xy_error": "",
        "has_any_nonfinite": "",
        "has_state_nonfinite": "",
        "has_command_nonfinite": "",
        "has_command_saturation": "",
        "has_high_speed": "",
        "has_position_jump": "",
        "has_swing_threshold_crossing": "",
        "first_nonfinite_time": "",
        "first_nonfinite_column": "",
        "first_so3_thrust_nan_time": "",
        "first_so3_bodyrate_nan_time": "",
        "first_so3_thrust_saturation_time": "",
        "first_so3_bodyrate_saturation_time": "",
        "first_uav_speed_gt4_time": "",
        "first_uav_speed_gt10_time": "",
        "first_payload_speed_gt4_time": "",
        "first_payload_speed_gt10_time": "",
        "first_swing_ge30_time": "",
        "first_swing_ge60_time": "",
        "first_uav_position_jump_gt1m_time": "",
        "first_payload_position_jump_gt1m_time": "",
        "first_has_trajectory_time": "",
        "last_finite_uav_position_before_nan": "",
        "last_finite_payload_position_before_nan": "",
        "failure_mode_guess": "",
    }
    if metrics:
        result.update(
            {
                "metrics_path": metrics.get("metrics_path", ""),
                "valid_run_suggested": metrics.get("valid_run_suggested", ""),
                "has_nan_state": metrics.get("has_nan_state", ""),
                "metrics_first_nan_time": metrics.get("first_nan_time", ""),
                "metrics_max_uav_speed": metrics.get("max_uav_speed", ""),
                "metrics_max_payload_speed": metrics.get("max_payload_speed", ""),
                "metrics_max_swing_angle_deg": metrics.get("max_swing_angle_deg", ""),
                "metrics_final_uav_xy_error": metrics.get("final_uav_xy_error", ""),
            }
        )

    last_uav_pos = None
    last_payload_pos = None
    last_finite_uav_before_nonfinite = None
    last_finite_payload_before_nonfinite = None
    first_nonfinite_seen = False
    has_state_nonfinite = False
    has_command_nonfinite = False
    numeric_columns = [column for column in fieldnames if column not in ("")]

    for row in rows:
        rel_time = relative_time(row, time_column, first_time)
        if not math.isfinite(rel_time):
            continue

        if not first_nonfinite_seen:
            for column in numeric_columns:
                text = str(row.get(column, "")).strip()
                if text == "":
                    continue
                value = parse_float(text)
                if not math.isfinite(value):
                    result["first_nonfinite_time"] = format_float(rel_time)
                    result["first_nonfinite_column"] = column
                    result["last_finite_uav_position_before_nan"] = format_position(last_finite_uav_before_nonfinite)
                    result["last_finite_payload_position_before_nan"] = format_position(last_finite_payload_before_nonfinite)
                    first_nonfinite_seen = True
                    break

        for column in STATE_COLUMNS:
            text = str(row.get(column, "")).strip()
            if text and not math.isfinite(parse_float(text)):
                has_state_nonfinite = True

        for column in COMMAND_COLUMNS:
            text = str(row.get(column, "")).strip()
            if text and not math.isfinite(parse_float(text)):
                has_command_nonfinite = True

        so3_thrust = parse_float(row.get("so3_thrust"))
        if not math.isfinite(so3_thrust):
            set_first(result, "first_so3_thrust_nan_time", rel_time)
        elif abs(so3_thrust) >= args.so3_thrust_saturation:
            set_first(result, "first_so3_thrust_saturation_time", rel_time)

        bodyrates = vector_values(row, SO3_BODYRATE_COLUMNS)
        if any(not math.isfinite(value) for value in bodyrates):
            set_first(result, "first_so3_bodyrate_nan_time", rel_time)
        elif (
            abs(bodyrates[0]) >= args.bodyrate_xy_saturation
            or abs(bodyrates[1]) >= args.bodyrate_xy_saturation
            or abs(bodyrates[2]) >= args.bodyrate_z_saturation
        ):
            set_first(result, "first_so3_bodyrate_saturation_time", rel_time)

        uav_speed = vector_norm(vector_values(row, UAV_VEL_COLUMNS))
        payload_speed = vector_norm(vector_values(row, PAYLOAD_VEL_COLUMNS))
        if math.isfinite(uav_speed):
            if uav_speed > 4.0:
                set_first(result, "first_uav_speed_gt4_time", rel_time)
            if uav_speed > 10.0:
                set_first(result, "first_uav_speed_gt10_time", rel_time)
        if math.isfinite(payload_speed):
            if payload_speed > 4.0:
                set_first(result, "first_payload_speed_gt4_time", rel_time)
            if payload_speed > 10.0:
                set_first(result, "first_payload_speed_gt10_time", rel_time)

        swing = parse_float(row.get("swing_angle_deg"))
        if math.isfinite(swing):
            if swing >= 30.0:
                set_first(result, "first_swing_ge30_time", rel_time)
            if swing >= 60.0:
                set_first(result, "first_swing_ge60_time", rel_time)

        has_trajectory = parse_float(row.get("has_trajectory"))
        if math.isfinite(has_trajectory) and has_trajectory > 0.5:
            set_first(result, "first_has_trajectory_time", rel_time)

        uav_pos = vector_values(row, UAV_POS_COLUMNS)
        payload_pos = vector_values(row, PAYLOAD_POS_COLUMNS)
        if all(math.isfinite(value) for value in uav_pos):
            if distance(last_uav_pos, uav_pos) > 1.0:
                set_first(result, "first_uav_position_jump_gt1m_time", rel_time)
            last_uav_pos = uav_pos
            if not first_nonfinite_seen:
                last_finite_uav_before_nonfinite = uav_pos
        if all(math.isfinite(value) for value in payload_pos):
            if distance(last_payload_pos, payload_pos) > 1.0:
                set_first(result, "first_payload_position_jump_gt1m_time", rel_time)
            last_payload_pos = payload_pos
            if not first_nonfinite_seen:
                last_finite_payload_before_nonfinite = payload_pos

    if result["last_finite_uav_position_before_nan"] == "" and last_finite_uav_before_nonfinite:
        result["last_finite_uav_position_before_nan"] = format_position(last_finite_uav_before_nonfinite)
    if result["last_finite_payload_position_before_nan"] == "" and last_finite_payload_before_nonfinite:
        result["last_finite_payload_position_before_nan"] = format_position(last_finite_payload_before_nonfinite)

    result["has_state_nonfinite"] = bool_text(has_state_nonfinite)
    result["has_command_nonfinite"] = bool_text(has_command_nonfinite)
    result["has_any_nonfinite"] = bool_text(has_state_nonfinite or has_command_nonfinite)
    result["has_command_saturation"] = bool_text(
        is_time_set(result, "first_so3_thrust_saturation_time")
        or is_time_set(result, "first_so3_bodyrate_saturation_time")
    )
    result["has_high_speed"] = bool_text(
        is_time_set(result, "first_uav_speed_gt4_time")
        or is_time_set(result, "first_payload_speed_gt4_time")
    )
    result["has_position_jump"] = bool_text(
        is_time_set(result, "first_uav_position_jump_gt1m_time")
        or is_time_set(result, "first_payload_position_jump_gt1m_time")
    )
    result["has_swing_threshold_crossing"] = bool_text(is_time_set(result, "first_swing_ge30_time"))
    result["failure_mode_guess"] = guess_failure_mode(result)
    return result, rows, fieldnames, time_column, first_time


def bool_text(value):
    return "true" if value else "false"


def is_time_set(result, key):
    return math.isfinite(time_value(result, key))


def time_value(result, key):
    value = parse_float(result.get(key))
    return value if math.isfinite(value) else math.nan


def bool_metric(result, key):
    return str(result.get(key, "")).strip().lower() == "true"


def max_metric(result, key):
    value = parse_float(result.get(key))
    return value if math.isfinite(value) else math.nan


def guess_failure_mode(result):
    first_nonfinite = time_value(result, "first_nonfinite_time")
    first_state_or_command_nonfinite = first_nonfinite if bool_metric(result, "has_any_nonfinite") else math.nan
    command_nan_times = [
        time_value(result, "first_so3_thrust_nan_time"),
        time_value(result, "first_so3_bodyrate_nan_time"),
    ]
    command_nan_times = [value for value in command_nan_times if math.isfinite(value)]
    first_command_nan = min(command_nan_times) if command_nan_times else math.nan
    saturation_times = [
        time_value(result, "first_so3_thrust_saturation_time"),
        time_value(result, "first_so3_bodyrate_saturation_time"),
    ]
    saturation_times = [value for value in saturation_times if math.isfinite(value)]
    first_saturation = min(saturation_times) if saturation_times else math.nan
    state_divergence_times = [
        time_value(result, "first_uav_speed_gt4_time"),
        time_value(result, "first_payload_speed_gt4_time"),
        time_value(result, "first_uav_position_jump_gt1m_time"),
        time_value(result, "first_payload_position_jump_gt1m_time"),
    ]
    state_divergence_times = [value for value in state_divergence_times if math.isfinite(value)]
    first_state_divergence = min(state_divergence_times) if state_divergence_times else math.nan

    has_any_nonfinite = bool_metric(result, "has_any_nonfinite")
    has_command_nonfinite = bool_metric(result, "has_command_nonfinite")
    has_command_saturation = bool_metric(result, "has_command_saturation")
    has_high_speed = bool_metric(result, "has_high_speed")
    has_position_jump = bool_metric(result, "has_position_jump")
    has_swing_threshold_crossing = bool_metric(result, "has_swing_threshold_crossing")
    has_nan = bool_metric(result, "has_nan_state") or has_any_nonfinite
    max_uav_speed = max_metric(result, "metrics_max_uav_speed")
    max_payload_speed = max_metric(result, "metrics_max_payload_speed")
    max_swing = max_metric(result, "metrics_max_swing_angle_deg")
    final_xy_error = max_metric(result, "metrics_final_uav_xy_error")
    valid_run_text = str(result.get("valid_run_suggested", "")).strip().lower()
    metrics_says_invalid = valid_run_text in ("false", "0", "no") or bool_metric(result, "has_nan_state")
    safety_no_nan = (
        not has_nan
        and (
            has_high_speed
            or has_swing_threshold_crossing
            or (math.isfinite(max_uav_speed) and max_uav_speed > 4.0)
            or (math.isfinite(max_payload_speed) and max_payload_speed > 4.0)
            or (math.isfinite(max_swing) and max_swing >= 60.0)
        )
    )
    target_error_only = (
        not has_nan
        and math.isfinite(final_xy_error)
        and final_xy_error > 0.5
        and not safety_no_nan
    )

    no_invalid_evidence = not (
        has_any_nonfinite
        or has_high_speed
        or has_position_jump
        or has_swing_threshold_crossing
        or target_error_only
        or safety_no_nan
    )
    if no_invalid_evidence:
        if metrics_says_invalid:
            return "unknown_invalid"
        if has_command_saturation:
            return "command_saturation_without_divergence"
        return "no_divergence_detected"

    if math.isfinite(first_saturation) and (
        (math.isfinite(first_state_or_command_nonfinite) and first_saturation <= first_state_or_command_nonfinite)
        or (
            not math.isfinite(first_state_or_command_nonfinite)
            and math.isfinite(first_state_divergence)
            and first_saturation <= first_state_divergence
        )
    ):
        return "command_saturation_before_nan"

    if math.isfinite(first_command_nan) and math.isfinite(first_state_divergence) and (
        first_command_nan <= first_state_divergence
    ):
        return "command_nan_before_state_divergence"

    if has_position_jump:
        return "teleport_like_position_jump"
    if has_nan and math.isfinite(first_command_nan) and math.isfinite(first_nonfinite) and first_nonfinite < first_command_nan:
        return "state_nan_before_command_nan"
    if has_nan and (
        math.isfinite(max_uav_speed)
        and max_uav_speed > 10.0
        or math.isfinite(max_payload_speed)
        and max_payload_speed > 10.0
    ):
        return "high_speed_nan_divergence"
    if safety_no_nan:
        return "strict_safety_no_nan"
    if target_error_only:
        return "target_error_only"
    if has_nan:
        return "manual_collision_or_path_infeasible_needed"
    if has_command_saturation:
        return "command_saturation_without_divergence"
    if has_command_nonfinite:
        return "manual_collision_or_path_infeasible_needed"
    if metrics_says_invalid:
        return "unknown_invalid"
    return "no_divergence_detected"


def parse_metrics_summary(path):
    metrics = {"metrics_path": str(path)}
    with path.open("r", encoding="utf-8") as metrics_file:
        for line in metrics_file:
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            metrics[key.strip()] = value.strip()
    return metrics


def inspect_metrics_glob(pattern, args):
    paths = sorted(Path(path) for path in glob.glob(pattern))
    results = []
    for metrics_path in paths:
        metrics = parse_metrics_summary(metrics_path)
        csv_path = resolve_path(metrics.get("csv_path"), base=metrics_path.parent)
        if not csv_path or not csv_path.exists():
            valid_text = parse_bool_text(metrics.get("valid_run_suggested", ""))
            has_nan_text = parse_bool_text(metrics.get("has_nan_state", ""))
            failure_mode_guess = (
                "unknown_invalid"
                if valid_text == "false" or has_nan_text == "true"
                else "no_divergence_detected"
            )
            row = {field: "" for field in OUTPUT_FIELDS}
            row.update(
                {
                    "csv_path": str(csv_path) if csv_path else metrics.get("csv_path", ""),
                    "metrics_path": str(metrics_path),
                    "valid_run_suggested": metrics.get("valid_run_suggested", ""),
                    "has_nan_state": metrics.get("has_nan_state", ""),
                    "metrics_first_nan_time": metrics.get("first_nan_time", ""),
                    "metrics_max_uav_speed": metrics.get("max_uav_speed", ""),
                    "metrics_max_payload_speed": metrics.get("max_payload_speed", ""),
                    "metrics_max_swing_angle_deg": metrics.get("max_swing_angle_deg", ""),
                    "metrics_final_uav_xy_error": metrics.get("final_uav_xy_error", ""),
                    "failure_mode_guess": failure_mode_guess,
                }
            )
            results.append(row)
            continue
        row, _, _, _, _ = inspect_csv(csv_path, args, metrics=metrics)
        results.append(row)
    return results


def write_output_csv(rows, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in OUTPUT_FIELDS})


def print_result_summary(rows):
    counts = Counter(row.get("failure_mode_guess", "unknown_invalid") for row in rows)
    print("rows_inspected: %d" % len(rows))
    for mode, count in sorted(counts.items()):
        print("%s: %d" % (mode, count))
    if len(rows) == 1:
        row = rows[0]
        for field in OUTPUT_FIELDS:
            if field in ("metrics_path",):
                continue
            value = row.get(field, "")
            if value != "":
                print("%s: %s" % (field, value))


def window_print(rows, fieldnames, time_column, first_time, start, end):
    if start is None or end is None:
        return
    key_columns = [
        "uav_pos_x",
        "uav_pos_y",
        "uav_pos_z",
        "uav_vel_x",
        "uav_vel_y",
        "uav_vel_z",
        "payload_pos_x",
        "payload_pos_y",
        "payload_pos_z",
        "payload_vel_x",
        "payload_vel_y",
        "payload_vel_z",
        "swing_angle_deg",
        "has_trajectory",
        "so3_thrust",
        "so3_bodyrate_x",
        "so3_bodyrate_y",
        "so3_bodyrate_z",
    ]
    available = [column for column in key_columns if column in fieldnames]
    print("window_rows:")
    print(",".join(["rel_time"] + available))
    for row in rows:
        rel_time = relative_time(row, time_column, first_time)
        if not math.isfinite(rel_time) or rel_time < start or rel_time > end:
            continue
        values = [format_float(rel_time)]
        values.extend(str(row.get(column, "")) for column in available)
        print(",".join(values))


def main():
    args = parse_args()
    if not args.csv and not args.metrics_glob:
        print("error: provide --csv or --metrics-glob", file=sys.stderr)
        return 2
    if args.csv and args.metrics_glob:
        print("error: use only one of --csv or --metrics-glob", file=sys.stderr)
        return 2
    if (args.window_start is None) != (args.window_end is None):
        print("error: --window-start and --window-end must be provided together", file=sys.stderr)
        return 2
    try:
        if args.csv:
            csv_path = resolve_path(args.csv)
            row, rows, fieldnames, time_column, first_time = inspect_csv(csv_path, args)
            results = [row]
            window_print(rows, fieldnames, time_column, first_time, args.window_start, args.window_end)
        else:
            results = inspect_metrics_glob(args.metrics_glob, args)
        if args.output_csv:
            write_output_csv(results, resolve_path(args.output_csv))
        if args.print_summary:
            print_result_summary(results)
    except Exception as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
