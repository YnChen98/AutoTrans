#!/usr/bin/env python3
"""Set frozen Stage 2-B drag-wind levels in so3_quadrotor.yaml."""

import argparse
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = REPO_ROOT / "uav_simulator/uav_simulator/config/so3_quadrotor.yaml"

WIND_KEYS = (
    "enable_wind",
    "wind_model",
    "wind_velocity_x",
    "wind_velocity_y",
    "wind_velocity_z",
    "wind_drag_linear",
    "wind_drag_quad",
    "wind_max_force",
    "wind_apply_to",
)

LEVELS = {
    "none": {
        "enable_wind": "false",
        "wind_model": '"drag"',
        "wind_velocity_x": "0.0",
        "wind_velocity_y": "0.0",
        "wind_velocity_z": "0.0",
        "wind_drag_linear": "0.0",
        "wind_drag_quad": "0.0",
        "wind_max_force": "0.0",
        "wind_apply_to": '"quadrotor"',
    },
    "weak": {
        "enable_wind": "true",
        "wind_model": '"drag"',
        "wind_velocity_x": "0.5",
        "wind_velocity_y": "0.0",
        "wind_velocity_z": "0.0",
        "wind_drag_linear": "0.004",
        "wind_drag_quad": "0.0",
        "wind_max_force": "0.002",
        "wind_apply_to": '"quadrotor"',
    },
    "moderate": {
        "enable_wind": "true",
        "wind_model": '"drag"',
        "wind_velocity_x": "0.5",
        "wind_velocity_y": "0.0",
        "wind_velocity_z": "0.0",
        "wind_drag_linear": "0.010",
        "wind_drag_quad": "0.0",
        "wind_max_force": "0.005",
        "wind_apply_to": '"quadrotor"',
    },
    "strong": {
        "enable_wind": "true",
        "wind_model": '"drag"',
        "wind_velocity_x": "0.5",
        "wind_velocity_y": "0.0",
        "wind_velocity_z": "0.0",
        "wind_drag_linear": "0.015",
        "wind_drag_quad": "0.0",
        "wind_max_force": "0.0075",
        "wind_apply_to": '"quadrotor"',
    },
    "boundary": {
        "enable_wind": "true",
        "wind_model": '"drag"',
        "wind_velocity_x": "0.5",
        "wind_velocity_y": "0.0",
        "wind_velocity_z": "0.0",
        "wind_drag_linear": "0.020",
        "wind_drag_quad": "0.0",
        "wind_max_force": "0.010",
        "wind_apply_to": '"quadrotor"',
    },
}

YAML_LINE_RE = re.compile(
    r"^(?P<indent>\s*)(?P<key>[A-Za-z_][A-Za-z0-9_]*)\s*:\s*"
    r"(?P<value>.*?)(?P<newline>\r?\n)?$"
)


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Set or inspect frozen Stage 2-B drag-wind parameters in "
            "uav_simulator/uav_simulator/config/so3_quadrotor.yaml."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python3 experiments/scripts/set_drag_wind_config.py --show
  python3 experiments/scripts/set_drag_wind_config.py --level none
  python3 experiments/scripts/set_drag_wind_config.py --level weak
  python3 experiments/scripts/set_drag_wind_config.py --level strong --dry-run
""",
    )
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--level", choices=sorted(LEVELS), help="wind level to write")
    action.add_argument("--show", action="store_true", help="print current wind config")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print proposed changes without writing the YAML file",
    )
    return parser.parse_args()


def read_config():
    if not CONFIG_PATH.exists():
        raise RuntimeError(f"Config file not found: {CONFIG_PATH}")
    return CONFIG_PATH.read_text().splitlines(keepends=True)


def find_wind_entries(lines):
    entries = {}
    duplicates = []

    for index, line in enumerate(lines):
        match = YAML_LINE_RE.match(line)
        if not match:
            continue

        key = match.group("key")
        if key not in WIND_KEYS:
            continue

        if key in entries:
            duplicates.append(key)
            continue

        entries[key] = {
            "index": index,
            "indent": match.group("indent"),
            "value": match.group("value").strip(),
            "newline": match.group("newline") or "",
        }

    missing = [key for key in WIND_KEYS if key not in entries]
    if missing:
        raise RuntimeError(
            "Missing required wind config key(s) in "
            f"{CONFIG_PATH}: {', '.join(missing)}"
        )
    if duplicates:
        raise RuntimeError(
            "Duplicate wind config key(s) in "
            f"{CONFIG_PATH}: {', '.join(sorted(set(duplicates)))}"
        )

    return entries


def show_config(entries):
    print(CONFIG_PATH)
    for key in WIND_KEYS:
        print(f"{key}: {entries[key]['value']}")


def apply_level(lines, entries, level, dry_run):
    values = LEVELS[level]
    new_lines = list(lines)

    print(f"Config: {CONFIG_PATH}")
    print(f"Level: {level}")
    if dry_run:
        print("DRY RUN: no file written.")

    for key in WIND_KEYS:
        entry = entries[key]
        old_value = entry["value"]
        new_value = values[key]
        marker = "unchanged" if old_value == new_value else f"{old_value} -> {new_value}"
        print(f"{key}: {marker}")

        new_lines[entry["index"]] = (
            f"{entry['indent']}{key}: {new_value}{entry['newline']}"
        )

    if not dry_run:
        CONFIG_PATH.write_text("".join(new_lines))


def main():
    args = parse_args()

    try:
        lines = read_config()
        entries = find_wind_entries(lines)

        if args.show:
            if args.dry_run:
                raise RuntimeError("--dry-run can only be used with --level")
            show_config(entries)
            return 0

        apply_level(lines, entries, args.level, args.dry_run)
        return 0
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
