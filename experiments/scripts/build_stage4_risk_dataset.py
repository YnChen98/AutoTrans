#!/usr/bin/env python3
"""Build a Stage 4 failure-risk dataset from AutoTrans CSV logs."""

import argparse
import csv
import json
import math
import sys
from collections import defaultdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]

REQUIRED_RUN_FIELDS = [
    "run_id",
    "csv_path",
    "method",
    "policy_mode",
    "adaptation_mode",
    "command_scale_expected",
    "wind_level",
    "wind_force_norm",
    "target_x",
    "target_y",
    "target_z",
    "payload_target_z",
    "trial_name",
    "repeat_id",
]

METADATA_FIELDS = REQUIRED_RUN_FIELDS + ["notes", "target_xy_tolerance"]

RUN_FEATURE_FIELDS = [
    "sample_count",
    "duration_sec",
    "effective_log_rate_hz",
    "has_nan_state",
    "first_nan_time",
    "final_row_has_nan",
    "valid_run_suggested",
    "nan_count_total",
    "final_uav_xy_error",
    "final_payload_xy_error",
    "final_uav_position_error_3d",
    "final_payload_position_error_3d",
    "mean_swing_angle_deg",
    "max_swing_angle_deg",
    "p95_swing_angle_deg",
    "max_uav_speed",
    "max_payload_speed",
    "mean_uav_speed",
    "mean_payload_speed",
    "uav_path_length",
    "payload_path_length",
    "mean_wind_force_norm",
    "max_wind_force_norm",
    "mean_command_speed_scale",
    "min_command_speed_scale",
    "max_command_speed_scale",
    "final_command_speed_scale",
]

LABEL_FIELDS = [
    "label_invalid",
    "label_nan",
    "label_target_fail",
    "label_speed_fail",
    "label_swing_fail",
]

EARLY_FEATURE_SUFFIXES = [
    "max_uav_speed",
    "max_payload_speed",
    "mean_uav_speed",
    "mean_payload_speed",
    "max_swing_angle_deg",
    "p95_swing_angle_deg",
    "mean_swing_angle_deg",
    "max_wind_force_norm",
    "mean_wind_force_norm",
    "min_command_speed_scale",
    "mean_command_speed_scale",
    "target_distance_end",
    "target_progress",
]

KEY_STATE_FIELDS = [
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
    "so3_thrust",
    "so3_bodyrate_x",
    "so3_bodyrate_y",
    "so3_bodyrate_z",
    "swing_angle_deg",
]

MAX_REASONABLE_SPEED_MPS = 10.0
MAX_REASONABLE_SWING_DEG = 90.0
MIN_REASONABLE_UAV_Z = 0.2
MIN_REASONABLE_PAYLOAD_Z = -0.2
LABEL_SPEED_FAIL_MPS = 4.0
LABEL_SWING_FAIL_DEG = 60.0


def parse_args():
    parser = argparse.ArgumentParser(
        description="Build the Stage 4 early failure-risk dataset from AutoTrans logs."
    )
    parser.add_argument("--manifest", required=True, help="Path to a Stage 4 risk manifest JSON file.")
    parser.add_argument("--output", required=True, help="Output CSV dataset path.")
    parser.add_argument("--dry-run", action="store_true", help="Summarize planned rows without writing CSV output.")
    parser.add_argument(
        "--target-xy-tolerance",
        type=float,
        default=0.5,
        help="Final UAV XY tolerance used for target-failure labels.",
    )
    parser.add_argument(
        "--early-windows",
        default="3,5,10,15",
        help="Comma-separated early windows in seconds, for example 3,5,10,15.",
    )
    parser.add_argument("--print-summary", action="store_true", help="Print aggregate counts after building rows.")
    return parser.parse_args()


def parse_float(value):
    if value is None:
        return math.nan
    text = str(value).strip()
    if text == "":
        return math.nan
    try:
        return float(text)
    except ValueError:
        return math.nan


def parse_windows(text):
    windows = []
    for part in text.split(","):
        part = part.strip()
        if not part:
            continue
        value = parse_float(part)
        if not math.isfinite(value) or value <= 0.0:
            raise ValueError("early window must be a positive number: %s" % part)
        windows.append(value)
    if not windows:
        raise ValueError("at least one early window is required")
    return windows


def window_label(value):
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    return ("%.6f" % value).rstrip("0").rstrip(".").replace(".", "p")


def resolve_input_path(path_text):
    path = Path(path_text).expanduser()
    if path.is_absolute():
        return path
    return (Path.cwd() / path).resolve()


def resolve_csv_path(path_text):
    path = Path(path_text).expanduser()
    if path.is_absolute():
        return path
    return (REPO_ROOT / path).resolve()


def load_manifest(path):
    if not path.exists():
        raise FileNotFoundError("manifest does not exist: %s" % path)
    with path.open("r", encoding="utf-8") as manifest_file:
        manifest = json.load(manifest_file)
    if not isinstance(manifest, dict):
        raise ValueError("manifest must be a JSON object")
    runs = manifest.get("runs")
    if not isinstance(runs, list):
        raise ValueError('manifest must contain a "runs" list')
    seen_run_ids = set()
    for index, run in enumerate(runs):
        if not isinstance(run, dict):
            raise ValueError("runs[%d] must be a JSON object" % index)
        missing = [field for field in REQUIRED_RUN_FIELDS if field not in run]
        if missing:
            raise ValueError("runs[%d] missing required fields: %s" % (index, ", ".join(missing)))
        run_id = str(run["run_id"])
        if run_id in seen_run_ids:
            raise ValueError("duplicate run_id in manifest: %s" % run_id)
        seen_run_ids.add(run_id)
    return runs


def read_csv_rows(path):
    if not path.exists():
        raise FileNotFoundError("CSV file does not exist: %s" % path)
    if path.stat().st_size == 0:
        raise ValueError("CSV file is empty: %s" % path)
    with path.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        if not reader.fieldnames:
            raise ValueError("CSV file has no header: %s" % path)
        rows = list(reader)
    if not rows:
        raise ValueError("CSV file has no data rows: %s" % path)
    return rows, list(reader.fieldnames)


def column(rows, name):
    return [parse_float(row.get(name)) for row in rows]


def values_at(values, indices):
    return [values[index] for index in indices if index < len(values)]


def valid_values(values):
    return [value for value in values if math.isfinite(value)]


def mean_or_nan(values):
    finite = valid_values(values)
    if not finite:
        return math.nan
    return sum(finite) / len(finite)


def max_or_nan(values):
    finite = valid_values(values)
    if not finite:
        return math.nan
    return max(finite)


def min_or_nan(values):
    finite = valid_values(values)
    if not finite:
        return math.nan
    return min(finite)


def final_or_nan(values):
    for value in reversed(values):
        if math.isfinite(value):
            return value
    return math.nan


def percentile(values, percent):
    finite = sorted(valid_values(values))
    if not finite:
        return math.nan
    if len(finite) == 1:
        return finite[0]
    rank = (len(finite) - 1) * percent / 100.0
    low_index = int(math.floor(rank))
    high_index = int(math.ceil(rank))
    if low_index == high_index:
        return finite[low_index]
    weight = rank - low_index
    return finite[low_index] * (1.0 - weight) + finite[high_index] * weight


def vector_norm_triplets(xs, ys, zs):
    norms = []
    for x_value, y_value, z_value in zip(xs, ys, zs):
        if all(math.isfinite(value) for value in (x_value, y_value, z_value)):
            norms.append(math.sqrt(x_value * x_value + y_value * y_value + z_value * z_value))
        else:
            norms.append(math.nan)
    return norms


def path_length(xs, ys, zs):
    total = 0.0
    previous = None
    for point in zip(xs, ys, zs):
        if not all(math.isfinite(value) for value in point):
            continue
        if previous is not None:
            total += math.sqrt(sum((point[index] - previous[index]) ** 2 for index in range(3)))
        previous = point
    return total if previous is not None else math.nan


def final_position(xs, ys, zs):
    for point in reversed(list(zip(xs, ys, zs))):
        if all(math.isfinite(value) for value in point):
            return point
    return None


def position_from_row(row, prefix):
    point = (
        parse_float(row.get("%s_pos_x" % prefix)),
        parse_float(row.get("%s_pos_y" % prefix)),
        parse_float(row.get("%s_pos_z" % prefix)),
    )
    if all(math.isfinite(value) for value in point):
        return point
    return None


def xy_error(position, target_x, target_y):
    if position is None or not (math.isfinite(target_x) and math.isfinite(target_y)):
        return math.nan
    return math.sqrt((position[0] - target_x) ** 2 + (position[1] - target_y) ** 2)


def position_error_3d(position, target_x, target_y, target_z):
    if position is None:
        return math.nan
    if not all(math.isfinite(value) for value in (target_x, target_y, target_z)):
        return math.nan
    return math.sqrt(
        (position[0] - target_x) ** 2
        + (position[1] - target_y) ** 2
        + (position[2] - target_z) ** 2
    )


def target_distance(position, target_x, target_y, target_z):
    if position is None or not (math.isfinite(target_x) and math.isfinite(target_y)):
        return math.nan
    xy_distance = math.sqrt((position[0] - target_x) ** 2 + (position[1] - target_y) ** 2)
    if not math.isfinite(target_z):
        return xy_distance
    return math.sqrt(xy_distance * xy_distance + (position[2] - target_z) ** 2)


def invalid_value_counts(rows, fieldnames, fields):
    counts = {}
    first_invalid_index = None
    for field in fields:
        if field not in fieldnames:
            counts[field] = 0
            continue
        count = 0
        seen_finite_value = False
        for index, row in enumerate(rows):
            value = parse_float(row.get(field))
            if math.isfinite(value):
                seen_finite_value = True
            elif seen_finite_value:
                count += 1
                if first_invalid_index is None or index < first_invalid_index:
                    first_invalid_index = index
        counts[field] = count
    return counts, first_invalid_index


def row_has_invalid_key_state(row, fieldnames):
    for field in KEY_STATE_FIELDS:
        if field in fieldnames and not math.isfinite(parse_float(row.get(field))):
            return True
    return False


def row_has_finite_key_state(row, fieldnames):
    for field in KEY_STATE_FIELDS:
        if field in fieldnames and math.isfinite(parse_float(row.get(field))):
            return True
    return False


def select_time_values(rows, fieldnames):
    ros_time = column(rows, "ros_time") if "ros_time" in fieldnames else [math.nan for _ in rows]
    if len(valid_values(ros_time)) >= 2:
        return ros_time, "ros_time"
    wall_time = column(rows, "wall_time") if "wall_time" in fieldnames else [math.nan for _ in rows]
    return wall_time, "wall_time"


def compute_duration_and_rate(rows, time_values):
    finite = valid_values(time_values)
    if len(finite) < 2:
        return math.nan, math.nan
    duration = finite[-1] - finite[0]
    if duration <= 0.0:
        return math.nan, math.nan
    return duration, (len(rows) - 1) / duration


def choose_anchor_index(rows, fieldnames, time_values):
    if "has_trajectory" in fieldnames:
        for index, row in enumerate(rows):
            if (
                index < len(time_values)
                and math.isfinite(time_values[index])
                and parse_float(row.get("has_trajectory")) > 0.5
                and row_has_finite_key_state(row, fieldnames)
            ):
                return index
    for index, row in enumerate(rows):
        if (
            index < len(time_values)
            and math.isfinite(time_values[index])
            and row_has_finite_key_state(row, fieldnames)
        ):
            return index
    for index, time_value in enumerate(time_values):
        if math.isfinite(time_value):
            return index
    return None


def finite_position_at_or_after(rows, indices, prefix):
    for index in indices:
        position = position_from_row(rows[index], prefix)
        if position is not None:
            return position
    return None


def finite_position_at_or_before(rows, indices, prefix):
    for index in reversed(indices):
        position = position_from_row(rows[index], prefix)
        if position is not None:
            return position
    return None


def wind_force_norms(rows, fieldnames):
    if "wind_force_norm" in fieldnames:
        return column(rows, "wind_force_norm")
    if all(field in fieldnames for field in ("wind_force_x", "wind_force_y", "wind_force_z")):
        return vector_norm_triplets(
            column(rows, "wind_force_x"),
            column(rows, "wind_force_y"),
            column(rows, "wind_force_z"),
        )
    return [math.nan for _ in rows]


def compute_early_features(
    rows,
    windows,
    time_values,
    uav_speed,
    payload_speed,
    swing_angle,
    wind_force_norm,
    command_speed_scale,
    target_x,
    target_y,
    target_z,
):
    features = {}
    anchor_index = choose_anchor_index(rows, set(rows[0].keys()), time_values)
    anchor_time = time_values[anchor_index] if anchor_index is not None else math.nan
    for window in windows:
        label = window_label(window)
        prefix = "early_%ss_" % label
        if not math.isfinite(anchor_time):
            indices = []
        else:
            window_end = anchor_time + window
            indices = [
                index
                for index, time_value in enumerate(time_values)
                if math.isfinite(time_value) and anchor_time <= time_value <= window_end
            ]
        start_position = finite_position_at_or_after(rows, indices, "uav")
        end_position = finite_position_at_or_before(rows, indices, "uav")
        start_distance = target_distance(start_position, target_x, target_y, target_z)
        end_distance = target_distance(end_position, target_x, target_y, target_z)

        features[prefix + "max_uav_speed"] = max_or_nan(values_at(uav_speed, indices))
        features[prefix + "max_payload_speed"] = max_or_nan(values_at(payload_speed, indices))
        features[prefix + "mean_uav_speed"] = mean_or_nan(values_at(uav_speed, indices))
        features[prefix + "mean_payload_speed"] = mean_or_nan(values_at(payload_speed, indices))
        features[prefix + "max_swing_angle_deg"] = max_or_nan(values_at(swing_angle, indices))
        features[prefix + "p95_swing_angle_deg"] = percentile(values_at(swing_angle, indices), 95.0)
        features[prefix + "mean_swing_angle_deg"] = mean_or_nan(values_at(swing_angle, indices))
        features[prefix + "max_wind_force_norm"] = max_or_nan(values_at(wind_force_norm, indices))
        features[prefix + "mean_wind_force_norm"] = mean_or_nan(values_at(wind_force_norm, indices))
        features[prefix + "min_command_speed_scale"] = min_or_nan(values_at(command_speed_scale, indices))
        features[prefix + "mean_command_speed_scale"] = mean_or_nan(values_at(command_speed_scale, indices))
        features[prefix + "target_distance_end"] = end_distance
        features[prefix + "target_progress"] = (
            start_distance - end_distance
            if math.isfinite(start_distance) and math.isfinite(end_distance)
            else math.nan
        )
    return features


def compute_run_row(run, args, windows):
    csv_path = resolve_csv_path(run["csv_path"])
    rows, fieldnames = read_csv_rows(csv_path)
    fieldnames = set(fieldnames)

    target_x = parse_float(run.get("target_x"))
    target_y = parse_float(run.get("target_y"))
    target_z = parse_float(run.get("target_z"))
    payload_target_z = parse_float(run.get("payload_target_z"))

    uav_pos_x = column(rows, "uav_pos_x")
    uav_pos_y = column(rows, "uav_pos_y")
    uav_pos_z = column(rows, "uav_pos_z")
    uav_speed = vector_norm_triplets(column(rows, "uav_vel_x"), column(rows, "uav_vel_y"), column(rows, "uav_vel_z"))

    payload_pos_x = column(rows, "payload_pos_x")
    payload_pos_y = column(rows, "payload_pos_y")
    payload_pos_z = column(rows, "payload_pos_z")
    payload_speed = vector_norm_triplets(
        column(rows, "payload_vel_x"),
        column(rows, "payload_vel_y"),
        column(rows, "payload_vel_z"),
    )

    swing_angle = column(rows, "swing_angle_deg")
    wind_force_norm = wind_force_norms(rows, fieldnames)
    command_speed_scale = (
        column(rows, "command_speed_scale")
        if "command_speed_scale" in fieldnames
        else [math.nan for _ in rows]
    )
    time_values, _time_source = select_time_values(rows, fieldnames)

    duration_sec, effective_log_rate_hz = compute_duration_and_rate(rows, time_values)
    final_uav_position = final_position(uav_pos_x, uav_pos_y, uav_pos_z)
    final_payload_position = final_position(payload_pos_x, payload_pos_y, payload_pos_z)

    nan_counts, first_nan_index = invalid_value_counts(rows, fieldnames, KEY_STATE_FIELDS)
    nan_count_total = sum(nan_counts.values())
    has_nan_state = nan_count_total > 0
    final_row_has_nan = row_has_invalid_key_state(rows[-1], fieldnames)

    first_nan_time = ""
    if first_nan_index is not None and first_nan_index < len(time_values):
        first_nan_time_value = time_values[first_nan_index]
        valid_times = valid_values(time_values)
        if math.isfinite(first_nan_time_value) and valid_times:
            first_nan_time = first_nan_time_value - valid_times[0]

    max_uav_speed = max_or_nan(uav_speed)
    max_payload_speed = max_or_nan(payload_speed)
    max_swing_angle_deg = max_or_nan(swing_angle)
    final_uav_xy_error = xy_error(final_uav_position, target_x, target_y)
    final_payload_xy_error = xy_error(final_payload_position, target_x, target_y)
    final_uav_position_error_3d = position_error_3d(final_uav_position, target_x, target_y, target_z)
    final_payload_position_error_3d = position_error_3d(
        final_payload_position,
        target_x,
        target_y,
        payload_target_z,
    )

    target_xy_failure = (
        math.isfinite(final_uav_xy_error)
        and final_uav_xy_error > args.target_xy_tolerance
    )
    unreasonable_final_altitude = (
        final_uav_position is not None
        and final_payload_position is not None
        and (
            final_uav_position[2] < MIN_REASONABLE_UAV_Z
            or final_payload_position[2] < MIN_REASONABLE_PAYLOAD_Z
        )
    )
    valid_run_suggested = not (
        has_nan_state
        or final_row_has_nan
        or final_uav_position is None
        or final_payload_position is None
        or (math.isfinite(max_uav_speed) and max_uav_speed > MAX_REASONABLE_SPEED_MPS)
        or (math.isfinite(max_payload_speed) and max_payload_speed > MAX_REASONABLE_SPEED_MPS)
        or (math.isfinite(max_swing_angle_deg) and max_swing_angle_deg > MAX_REASONABLE_SWING_DEG)
        or unreasonable_final_altitude
        or target_xy_failure
    )

    row = {}
    for field in REQUIRED_RUN_FIELDS:
        row[field] = run.get(field)
    row["notes"] = run.get("notes", "")
    row["target_xy_tolerance"] = args.target_xy_tolerance
    row.update(
        {
            "sample_count": len(rows),
            "duration_sec": duration_sec,
            "effective_log_rate_hz": effective_log_rate_hz,
            "has_nan_state": has_nan_state,
            "first_nan_time": first_nan_time,
            "final_row_has_nan": final_row_has_nan,
            "valid_run_suggested": valid_run_suggested,
            "nan_count_total": nan_count_total,
            "final_uav_xy_error": final_uav_xy_error,
            "final_payload_xy_error": final_payload_xy_error,
            "final_uav_position_error_3d": final_uav_position_error_3d,
            "final_payload_position_error_3d": final_payload_position_error_3d,
            "mean_swing_angle_deg": mean_or_nan(swing_angle),
            "max_swing_angle_deg": max_swing_angle_deg,
            "p95_swing_angle_deg": percentile(swing_angle, 95.0),
            "max_uav_speed": max_uav_speed,
            "max_payload_speed": max_payload_speed,
            "mean_uav_speed": mean_or_nan(uav_speed),
            "mean_payload_speed": mean_or_nan(payload_speed),
            "uav_path_length": path_length(uav_pos_x, uav_pos_y, uav_pos_z),
            "payload_path_length": path_length(payload_pos_x, payload_pos_y, payload_pos_z),
            "mean_wind_force_norm": mean_or_nan(wind_force_norm),
            "max_wind_force_norm": max_or_nan(wind_force_norm),
            "mean_command_speed_scale": mean_or_nan(command_speed_scale),
            "min_command_speed_scale": min_or_nan(command_speed_scale),
            "max_command_speed_scale": max_or_nan(command_speed_scale),
            "final_command_speed_scale": final_or_nan(command_speed_scale),
            "label_invalid": 0 if valid_run_suggested else 1,
            "label_nan": 1 if has_nan_state else 0,
            "label_target_fail": 1 if target_xy_failure else 0,
            "label_speed_fail": 1
            if (
                (math.isfinite(max_uav_speed) and max_uav_speed > LABEL_SPEED_FAIL_MPS)
                or (math.isfinite(max_payload_speed) and max_payload_speed > LABEL_SPEED_FAIL_MPS)
            )
            else 0,
            "label_swing_fail": 1
            if math.isfinite(max_swing_angle_deg) and max_swing_angle_deg > LABEL_SWING_FAIL_DEG
            else 0,
        }
    )
    row.update(
        compute_early_features(
            rows,
            windows,
            time_values,
            uav_speed,
            payload_speed,
            swing_angle,
            wind_force_norm,
            command_speed_scale,
            target_x,
            target_y,
            target_z,
        )
    )
    return row


def fieldnames_for(windows):
    fields = list(METADATA_FIELDS) + list(RUN_FEATURE_FIELDS) + list(LABEL_FIELDS)
    for window in windows:
        label = window_label(window)
        for suffix in EARLY_FEATURE_SUFFIXES:
            fields.append("early_%ss_%s" % (label, suffix))
    return fields


def format_value(value):
    if value == "":
        return ""
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if math.isnan(value):
            return "nan"
        if math.isinf(value):
            return "inf" if value > 0.0 else "-inf"
        return "%.9g" % value
    return str(value)


def write_dataset(path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: format_value(row.get(field)) for field in fieldnames})


def print_summary(rows, skipped_count, output_path, dry_run):
    total = len(rows)
    label_totals = {field: sum(int(row.get(field, 0)) for row in rows) for field in LABEL_FIELDS}
    method_counts = defaultdict(lambda: {"rows": 0, "valid": 0, "invalid": 0})
    for row in rows:
        method = str(row.get("method", "unknown"))
        method_counts[method]["rows"] += 1
        if int(row.get("label_invalid", 0)) == 1:
            method_counts[method]["invalid"] += 1
        else:
            method_counts[method]["valid"] += 1

    action = "would write" if dry_run else "wrote"
    print("%s %d dataset rows to %s" % (action, total, output_path))
    print("skipped_runs: %d" % skipped_count)
    for field in LABEL_FIELDS:
        print("%s_count: %d" % (field, label_totals[field]))
    print("method_counts:")
    for method in sorted(method_counts):
        counts = method_counts[method]
        print(
            "  %s: rows=%d valid=%d invalid=%d"
            % (method, counts["rows"], counts["valid"], counts["invalid"])
        )


def build_rows(runs, args, windows):
    rows = []
    errors = []
    for run in runs:
        run_id = str(run.get("run_id", "<unknown>"))
        try:
            rows.append(compute_run_row(run, args, windows))
        except Exception as exc:
            message = "ERROR: %s: %s" % (run_id, exc)
            print(message, file=sys.stderr)
            errors.append(message)
    return rows, errors


def main():
    args = parse_args()
    try:
        windows = parse_windows(args.early_windows)
        manifest_path = resolve_input_path(args.manifest)
        output_path = resolve_input_path(args.output)
        runs = load_manifest(manifest_path)
        rows, errors = build_rows(runs, args, windows)
    except Exception as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        return 1

    if args.dry_run:
        for row in rows:
            print(
                "planned_row run_id=%s method=%s valid_run_suggested=%s label_invalid=%s"
                % (
                    row.get("run_id"),
                    row.get("method"),
                    format_value(row.get("valid_run_suggested")),
                    row.get("label_invalid"),
                )
            )
        print_summary(rows, len(errors), output_path, dry_run=True)
        return 1 if errors else 0

    if errors:
        print("ERROR: refusing to write partial dataset because %d run(s) failed." % len(errors), file=sys.stderr)
        return 1

    fieldnames = fieldnames_for(windows)
    write_dataset(output_path, rows, fieldnames)
    if args.print_summary:
        print_summary(rows, 0, output_path, dry_run=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
