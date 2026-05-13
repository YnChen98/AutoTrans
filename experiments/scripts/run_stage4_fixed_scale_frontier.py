#!/usr/bin/env python3
"""Generate or execute Stage 4-R fixed-scale frontier screening commands."""

import argparse
import shlex
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]

TRIAL_TARGETS = {
    4: {
        "x": "-3.5",
        "y": "-1.2",
        "z": "0.0",
        "target_x": "-3.5",
        "target_y": "-1.2",
        "target_z": "1.468415",
        "payload_target_z": "0.799970",
    },
    5: {
        "x": "3.5",
        "y": "0.8",
        "z": "0.0",
        "target_x": "3.5",
        "target_y": "0.8",
        "target_z": "1.468415",
        "payload_target_z": "0.799970",
    },
    6: {
        "x": "0.0",
        "y": "1.5",
        "z": "0.0",
        "target_x": "0.0",
        "target_y": "1.5",
        "target_z": "1.468415",
        "payload_target_z": "0.799970",
    },
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate Stage 4-R fixed-scale frontier screening commands."
    )
    parser.add_argument("--scale", type=float, required=True, help="Fixed speed/acceleration scale.")
    parser.add_argument(
        "--trials",
        type=int,
        nargs="+",
        default=[4, 5, 6],
        help="Trial numbers to run. Supported: 4 5 6.",
    )
    parser.add_argument(
        "--repeats",
        type=int,
        nargs="+",
        default=[1, 2, 3],
        help="Repeat IDs to run for each trial.",
    )
    parser.add_argument("--duration", type=float, default=75.0, help="Run duration passed to run_baseline_trial.sh.")
    parser.add_argument(
        "--startup-wait",
        type=float,
        default=25.0,
        help="Startup wait passed to run_baseline_trial.sh.",
    )
    parser.add_argument("--goal-repeat", type=int, default=10, help="Goal publish repeat count.")
    parser.add_argument("--goal-interval", type=float, default=1.0, help="Goal publish interval in seconds.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print commands without executing them. This is also the default unless --execute is used.",
    )
    parser.add_argument(
        "--print-commands",
        action="store_true",
        help="Print the generated command plan.",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute generated commands. This runs ROS simulation and modifies planner XML params.",
    )
    return parser.parse_args()


def shell_join(parts):
    return " ".join(shlex.quote(str(part)) for part in parts)


def format_number(value):
    if isinstance(value, str):
        return value
    if isinstance(value, int):
        return str(value)
    if abs(float(value) - round(float(value))) < 1.0e-9:
        return str(int(round(float(value))))
    return ("%.6f" % float(value)).rstrip("0").rstrip(".")


def scale_tag(scale):
    return "s%03d" % int(round(scale * 100.0))


def validate_args(args):
    if not (0.0 < args.scale <= 1.0):
        raise ValueError("--scale must be in (0, 1]: %s" % args.scale)
    unsupported = [trial for trial in args.trials if trial not in TRIAL_TARGETS]
    if unsupported:
        raise ValueError("--trials supports only 4, 5, 6; got: %s" % unsupported)
    if any(repeat <= 0 for repeat in args.repeats):
        raise ValueError("--repeats must be positive integers: %s" % args.repeats)
    if args.duration <= 0:
        raise ValueError("--duration must be positive")
    if args.startup_wait < 0:
        raise ValueError("--startup-wait must be non-negative")
    if args.goal_repeat <= 0:
        raise ValueError("--goal-repeat must be positive")
    if args.goal_interval <= 0:
        raise ValueError("--goal-interval must be positive")


def planner_patch_command(scale):
    scale_text = format_number(scale)
    return f"""python3 - <<'PY'
from pathlib import Path
import re

path = Path("planner/plan_manage/launch/planning_node_params.xml")
text = path.read_text(encoding="utf-8")

def replace_param(source, name, value):
    pattern = r'(<param\\s+name="%s"\\s+value=")[^"]*(")' % re.escape(name)
    updated, count = re.subn(pattern, r'\\g<1>%s\\2' % value, source)
    if count != 1:
        raise RuntimeError("expected exactly one param for %s, found %d" % (name, count))
    return updated

for key, value in [
    ("manager/enable_command_adaptation", "true"),
    ("manager/adaptation_mode", "fixed"),
    ("manager/require_adaptation_topic_ready", "false"),
    ("manager/speed_scale", "{scale_text}"),
    ("manager/acceleration_scale", "{scale_text}"),
]:
    text = replace_param(text, key, value)

path.write_text(text, encoding="utf-8")
print("configured planner fixed command adaptation scale={scale_text}")
PY"""


def planner_restore_command():
    return """python3 - <<'PY'
from pathlib import Path
import re

path = Path("planner/plan_manage/launch/planning_node_params.xml")
text = path.read_text(encoding="utf-8")

def replace_param(source, name, value):
    pattern = r'(<param\\s+name="%s"\\s+value=")[^"]*(")' % re.escape(name)
    updated, count = re.subn(pattern, r'\\g<1>%s\\2' % value, source)
    if count != 1:
        raise RuntimeError("expected exactly one param for %s, found %d" % (name, count))
    return updated

for key, value in [
    ("manager/enable_command_adaptation", "false"),
    ("manager/adaptation_mode", "none"),
    ("manager/require_adaptation_topic_ready", "false"),
    ("manager/speed_scale", "1.0"),
    ("manager/acceleration_scale", "1.0"),
]:
    text = replace_param(text, key, value)

path.write_text(text, encoding="utf-8")
print("restored planner command adaptation to no-op")
PY"""


def run_name(scale, trial, repeat):
    return "stage4_fixed_%s_strong_trial%d_frontier_repeat%d" % (
        scale_tag(scale),
        trial,
        repeat,
    )


def metrics_summary_name(scale, trial, repeat):
    return "%s_metrics_summary.txt" % run_name(scale, trial, repeat)


def build_run_commands(args):
    commands = [
        ("set strong wind", "python3 experiments/scripts/set_drag_wind_config.py --level strong"),
        ("set planner fixed scale", planner_patch_command(args.scale)),
    ]

    for trial in args.trials:
        target = TRIAL_TARGETS[trial]
        for repeat in args.repeats:
            name = run_name(args.scale, trial, repeat)
            commands.append(
                (
                    "run %s" % name,
                    shell_join(
                        [
                            "bash",
                            "experiments/scripts/run_baseline_trial.sh",
                            "--name",
                            name,
                            "--x",
                            format_number(target["x"]),
                            "--y",
                            format_number(target["y"]),
                            "--z",
                            format_number(target["z"]),
                            "--duration",
                            format_number(args.duration),
                            "--startup_wait",
                            format_number(args.startup_wait),
                            "--goal_repeat",
                            str(args.goal_repeat),
                            "--goal_interval",
                            format_number(args.goal_interval),
                        ]
                    ),
                )
            )
            commands.append(
                (
                    "analyze %s with target metrics" % name,
                    shell_join(
                        [
                            "python3",
                            "experiments/autotrans_logger/scripts/analyze_log.py",
                            "--target_x",
                            format_number(target["target_x"]),
                            "--target_y",
                            format_number(target["target_y"]),
                            "--target_z",
                            format_number(target["target_z"]),
                            "--payload_target_z",
                            format_number(target["payload_target_z"]),
                            "--target_xy_tolerance",
                            "0.5",
                        ]
                    ),
                )
            )
            commands.append(
                (
                    "copy metrics summary for %s" % name,
                    shell_join(
                        [
                            "cp",
                            "experiments/figures/metrics_summary.txt",
                            "experiments/figures/%s" % metrics_summary_name(args.scale, trial, repeat),
                        ]
                    ),
                )
            )

    return commands


def build_restore_commands():
    return [
        ("restore wind none", "python3 experiments/scripts/set_drag_wind_config.py --level none"),
        ("restore planner no-op adaptation", planner_restore_command()),
    ]


def print_commands(args, run_commands, restore_commands):
    mode = "execute" if args.execute else "dry-run"
    print("# Stage 4-R fixed-scale frontier command plan (%s)" % mode)
    print("# Repository root: %s" % REPO_ROOT)
    print("# scale: %s (%s)" % (format_number(args.scale), scale_tag(args.scale)))
    print("# trials: %s" % " ".join(str(trial) for trial in args.trials))
    print("# repeats: %s" % " ".join(str(repeat) for repeat in args.repeats))
    print("cd %s" % shlex.quote(str(REPO_ROOT)))
    for label, command in run_commands:
        print("")
        print("# %s" % label)
        print(command)
    print("")
    print("# restore instructions")
    for label, command in restore_commands:
        print("")
        print("# %s" % label)
        print(command)


def execute_commands(run_commands, restore_commands):
    try:
        for label, command in run_commands:
            print("== %s ==" % label)
            subprocess.run(command, cwd=str(REPO_ROOT), shell=True, check=True)
    finally:
        for label, command in restore_commands:
            print("== %s ==" % label)
            subprocess.run(command, cwd=str(REPO_ROOT), shell=True, check=False)


def main():
    args = parse_args()
    try:
        validate_args(args)
        run_commands = build_run_commands(args)
        restore_commands = build_restore_commands()
        if args.print_commands or args.dry_run or not args.execute:
            print_commands(args, run_commands, restore_commands)
        if args.execute:
            execute_commands(run_commands, restore_commands)
    except Exception as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
