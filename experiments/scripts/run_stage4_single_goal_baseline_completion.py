#!/usr/bin/env python3
"""Generate or execute Stage 4-X2 single-goal baseline completion commands."""

import argparse
import shutil
import shlex
import subprocess
import sys
import time
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
LOG_DIR = REPO_ROOT / "experiments" / "logs"
FIGURE_DIR = REPO_ROOT / "experiments" / "figures"

METHODS = ["original", "fixed_s085", "windlevel_s085", "risk_adapter_v1"]

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

PLANNER_CONFIGS = {
    "original": {
        "manager/enable_command_adaptation": "false",
        "manager/adaptation_mode": "none",
        "manager/speed_scale": "1.0",
        "manager/acceleration_scale": "1.0",
        "manager/require_adaptation_topic_ready": "false",
    },
    "fixed_s085": {
        "manager/enable_command_adaptation": "true",
        "manager/adaptation_mode": "fixed",
        "manager/speed_scale": "0.85",
        "manager/acceleration_scale": "0.85",
        "manager/require_adaptation_topic_ready": "false",
    },
    "windlevel_s085": {
        "manager/enable_command_adaptation": "true",
        "manager/adaptation_mode": "topic",
        "manager/speed_scale": "1.0",
        "manager/acceleration_scale": "1.0",
        "manager/require_adaptation_topic_ready": "true",
    },
    "risk_adapter_v1": {
        "manager/enable_command_adaptation": "true",
        "manager/adaptation_mode": "topic",
        "manager/speed_scale": "1.0",
        "manager/acceleration_scale": "1.0",
        "manager/require_adaptation_topic_ready": "true",
    },
}

PLANNER_RESTORE_CONFIG = {
    "manager/enable_command_adaptation": "false",
    "manager/adaptation_mode": "none",
    "manager/speed_scale": "1.0",
    "manager/acceleration_scale": "1.0",
    "manager/require_adaptation_topic_ready": "false",
}

WIND_SIGNAL_COMMAND = (
    "roslaunch autotrans_logger wind_signal_publisher.launch "
    "enable_wind:=true wind_mode:=constant wind_force_x:=0.0075 "
    "wind_max_force:=0.0075"
)

ADAPTER_PREREQUISITES = {
    "original": [],
    "fixed_s085": [],
    "windlevel_s085": [
        "roslaunch command_adaptation heuristic_command_adapter.launch "
        "policy_mode:=wind_level"
    ],
    "risk_adapter_v1": [
        "roslaunch command_adaptation risk_conditioned_command_adapter.launch "
        "enable_risk_conditioning:=true "
        "policy_mode:=risk_conditioned "
        "risk_threshold_3s:=0.5 "
        "risk_threshold_5s:=0.5 "
        "hard_threshold_5s:=0.7 "
        "soft_scale_3s:=0.75 "
        "soft_scale_5s:=0.65 "
        "hard_scale_5s:=0.60 "
        "scale_rate_limit_per_sec:=0.5"
    ],
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate Stage 4-X2 single-goal baseline completion commands."
    )
    parser.add_argument(
        "--method",
        choices=METHODS,
        required=True,
        help="Baseline method to run.",
    )
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
        default=list(range(1, 11)),
        help="Repeat IDs to run.",
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=75.0,
        help="Run duration passed to run_baseline_trial.sh.",
    )
    parser.add_argument(
        "--startup-wait",
        type=float,
        default=25.0,
        help="Startup wait passed to run_baseline_trial.sh.",
    )
    parser.add_argument(
        "--goal-repeat",
        type=int,
        default=1,
        help="Goal publish repeat count. Stage 4-X2 expects 1.",
    )
    parser.add_argument(
        "--goal-interval",
        type=float,
        default=1.0,
        help="Goal publish interval in seconds.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print commands without executing them. This is the default unless --execute is used.",
    )
    parser.add_argument(
        "--print-commands",
        action="store_true",
        help="Print the generated command plan.",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute generated commands. This runs ROS simulation and edits planner XML params.",
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


def validate_args(args):
    unsupported = [trial for trial in args.trials if trial not in TRIAL_TARGETS]
    if unsupported:
        raise ValueError("--trials supports only 4, 5, 6; got: %s" % unsupported)
    if any(repeat <= 0 for repeat in args.repeats):
        raise ValueError("--repeats must be positive integers: %s" % args.repeats)
    if args.duration <= 0:
        raise ValueError("--duration must be positive")
    if args.startup_wait < 0:
        raise ValueError("--startup-wait must be non-negative")
    if args.goal_repeat != 1:
        raise ValueError("Stage 4-X2 single-goal completion requires --goal-repeat 1")
    if args.goal_interval <= 0:
        raise ValueError("--goal-interval must be positive")
    if args.execute and args.dry_run:
        raise ValueError("--execute and --dry-run are mutually exclusive")


def planner_patch_command(config, label):
    entries = ",\n    ".join(
        "(%r, %r)" % (name, value) for name, value in config.items()
    )
    template = """python3 - <<'PY'
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
    {entries},
]:
    text = replace_param(text, key, value)

path.write_text(text, encoding="utf-8")
print("{label}")
PY"""
    return template.format(entries=entries, label=label)


def run_name(method, trial, repeat):
    return "stage4x_singlegoal_%s_strong_trial%d_goalrepeat1_repeat%d" % (
        method,
        trial,
        repeat,
    )


def metrics_summary_name(method, trial, repeat):
    return "%s_metrics_summary.txt" % run_name(method, trial, repeat)


def run_trial_command(args, trial, repeat):
    target = TRIAL_TARGETS[trial]
    return shell_join(
        [
            "bash",
            "experiments/scripts/run_baseline_trial.sh",
            "--name",
            run_name(args.method, trial, repeat),
            "--x",
            target["x"],
            "--y",
            target["y"],
            "--z",
            target["z"],
            "--duration",
            format_number(args.duration),
            "--startup_wait",
            format_number(args.startup_wait),
            "--goal_repeat",
            str(args.goal_repeat),
            "--goal_interval",
            format_number(args.goal_interval),
        ]
    )


def analyze_command_for_csv(csv_expr, trial):
    target = TRIAL_TARGETS[trial]
    command = shell_join(
        ["python3", "experiments/autotrans_logger/scripts/analyze_log.py", "--csv"]
    )
    if csv_expr.startswith("$"):
        command += ' "%s"' % csv_expr
    else:
        command += " %s" % shlex.quote(csv_expr)
    command += " " + shell_join(
        [
            "--target_x",
            target["target_x"],
            "--target_y",
            target["target_y"],
            "--target_z",
            target["target_z"],
            "--payload_target_z",
            target["payload_target_z"],
            "--target_xy_tolerance",
            "0.5",
        ]
    )
    return command


def printed_run_block(args, trial, repeat):
    name = run_name(args.method, trial, repeat)
    metrics_path = "experiments/figures/%s" % metrics_summary_name(
        args.method, trial, repeat
    )
    return """before_csv="$(ls -t experiments/logs/autotrans_log_*.csv 2>/dev/null | head -1 || true)"
%s
after_csv="$(ls -t experiments/logs/autotrans_log_*.csv 2>/dev/null | head -1 || true)"
if [ -z "${after_csv}" ] || [ "${after_csv}" = "${before_csv}" ]; then
  echo "WARNING: no distinct new CSV detected for %s; check duplicate CSV safety before recording." >&2
fi
%s
cp experiments/figures/metrics_summary.txt %s""" % (
        run_trial_command(args, trial, repeat),
        name,
        analyze_command_for_csv("${after_csv}", trial),
        shlex.quote(metrics_path),
    )


def build_run_commands(args):
    commands = [
        ("set strong wind", "python3 experiments/scripts/set_drag_wind_config.py --level strong"),
        (
            "set planner params for %s" % args.method,
            planner_patch_command(
                PLANNER_CONFIGS[args.method],
                "configured planner for Stage 4-X2 method=%s" % args.method,
            ),
        ),
    ]
    for trial in args.trials:
        for repeat in args.repeats:
            name = run_name(args.method, trial, repeat)
            commands.append(("run/analyze/copy %s" % name, printed_run_block(args, trial, repeat)))
    return commands


def build_restore_commands():
    return [
        ("restore wind none", "python3 experiments/scripts/set_drag_wind_config.py --level none"),
        (
            "restore planner no-op adaptation",
            planner_patch_command(
                PLANNER_RESTORE_CONFIG,
                "restored planner command adaptation to no-op",
            ),
        ),
    ]


def print_prerequisites(method):
    print("# prerequisites")
    print("# Run from a sourced ROS/catkin environment in another terminal when executing:")
    print("# %s" % WIND_SIGNAL_COMMAND)
    if ADAPTER_PREREQUISITES[method]:
        for command in ADAPTER_PREREQUISITES[method]:
            print("# %s" % command)
    else:
        print("# no command-adaptation adapter process is required for %s" % method)
    print("# after the batch, run a duplicate csv_path check before paper-facing recording")


def print_commands(args, run_commands, restore_commands):
    mode = "execute" if args.execute else "dry-run"
    print("# Stage 4-X2 single-goal baseline completion command plan (%s)" % mode)
    print("# Repository root: %s" % REPO_ROOT)
    print("# method: %s" % args.method)
    print("# trials: %s" % " ".join(str(trial) for trial in args.trials))
    print("# repeats: %s" % " ".join(str(repeat) for repeat in args.repeats))
    print("# goal_repeat: %d" % args.goal_repeat)
    print_prerequisites(args.method)
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


def latest_csv():
    candidates = list(LOG_DIR.glob("autotrans_log_*.csv"))
    if not candidates:
        return None
    return max(candidates, key=lambda path: path.stat().st_mtime)


def detect_new_csv(before_path, start_time):
    candidates = sorted(
        LOG_DIR.glob("autotrans_log_*.csv"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    for path in candidates:
        if path.stat().st_mtime >= start_time - 1.0 and path != before_path:
            return path
    latest = candidates[0] if candidates else None
    if latest and latest != before_path:
        return latest
    return None


def run_shell(label, command, check=True):
    print("== %s ==" % label)
    subprocess.run(command, cwd=str(REPO_ROOT), shell=True, check=check)


def run_list(label, command):
    print("== %s ==" % label)
    subprocess.run(command, cwd=str(REPO_ROOT), check=True)


def execute(args, restore_commands):
    print_prerequisites(args.method)
    try:
        run_shell(
            "set strong wind",
            "python3 experiments/scripts/set_drag_wind_config.py --level strong",
        )
        run_shell(
            "set planner params for %s" % args.method,
            planner_patch_command(
                PLANNER_CONFIGS[args.method],
                "configured planner for Stage 4-X2 method=%s" % args.method,
            ),
        )

        for trial in args.trials:
            for repeat in args.repeats:
                name = run_name(args.method, trial, repeat)
                before = latest_csv()
                start_time = time.time()
                run_list(
                    "run %s" % name,
                    [
                        "bash",
                        "experiments/scripts/run_baseline_trial.sh",
                        "--name",
                        name,
                        "--x",
                        TRIAL_TARGETS[trial]["x"],
                        "--y",
                        TRIAL_TARGETS[trial]["y"],
                        "--z",
                        TRIAL_TARGETS[trial]["z"],
                        "--duration",
                        format_number(args.duration),
                        "--startup_wait",
                        format_number(args.startup_wait),
                        "--goal_repeat",
                        str(args.goal_repeat),
                        "--goal_interval",
                        format_number(args.goal_interval),
                    ],
                )
                csv_path = detect_new_csv(before, start_time)
                if csv_path is None:
                    raise RuntimeError(
                        "could not detect a distinct new CSV for %s; run duplicate CSV checks before recording"
                        % name
                    )
                run_list(
                    "analyze %s with explicit CSV" % name,
                    [
                        "python3",
                        "experiments/autotrans_logger/scripts/analyze_log.py",
                        "--csv",
                        str(csv_path),
                        "--target_x",
                        TRIAL_TARGETS[trial]["target_x"],
                        "--target_y",
                        TRIAL_TARGETS[trial]["target_y"],
                        "--target_z",
                        TRIAL_TARGETS[trial]["target_z"],
                        "--payload_target_z",
                        TRIAL_TARGETS[trial]["payload_target_z"],
                        "--target_xy_tolerance",
                        "0.5",
                    ],
                )
                destination = FIGURE_DIR / metrics_summary_name(
                    args.method, trial, repeat
                )
                shutil.copyfile(FIGURE_DIR / "metrics_summary.txt", destination)
                print("copied metrics summary to %s" % destination)
    finally:
        for label, command in restore_commands:
            run_shell(label, command, check=False)


def main():
    args = parse_args()
    try:
        validate_args(args)
        run_commands = build_run_commands(args)
        restore_commands = build_restore_commands()
        if args.print_commands or args.dry_run or not args.execute:
            print_commands(args, run_commands, restore_commands)
        if args.execute:
            execute(args, restore_commands)
    except Exception as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
