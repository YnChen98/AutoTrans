#!/usr/bin/env python3
"""Assemble the Stage 4 paper figure package from existing generated assets."""

import argparse
import csv
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]

MANIFEST_FIELDS = [
    "paper_item",
    "target_filename",
    "source_path",
    "status",
    "paper_section",
    "supported_claim",
    "caveat",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Create a Stage 4 paper figure package by copying/checking "
            "existing generated assets."
        )
    )
    parser.add_argument(
        "--source-root",
        default=".",
        help="Repository/source root containing experiments/results assets.",
    )
    parser.add_argument(
        "--output-dir",
        default="experiments/results/stage4_paper_figure_package",
        help="Output directory for the paper figure package.",
    )
    parser.add_argument(
        "--print-summary",
        action="store_true",
        help="Print a concise package summary.",
    )
    parser.add_argument(
        "--regenerate",
        action="store_true",
        help=(
            "Explicitly regenerate offline source assets before packaging. "
            "Default behavior is copy/check only."
        ),
    )
    return parser.parse_args()


def resolve_from(base, path_text):
    path = Path(path_text).expanduser()
    if path.is_absolute():
        return path
    return (base / path).resolve()


def relpath(path, base):
    try:
        return str(path.resolve().relative_to(base.resolve()))
    except ValueError:
        return str(path)


def run_offline_regenerators(source_root):
    commands = [
        [
            sys.executable,
            "experiments/scripts/generate_stage4_protocol_split_paper_assets.py",
            "--metrics-dir",
            "experiments/figures",
            "--output-dir",
            "experiments/results/stage4_protocol_split_paper_assets",
        ],
        [
            sys.executable,
            "experiments/scripts/generate_stage4_balanced_robustness_assets.py",
            "--output-dir",
            "experiments/results/stage4_balanced_robustness_assets",
        ],
        [
            sys.executable,
            "experiments/scripts/generate_stage4_failure_mode_paper_assets.py",
            "--metrics-dir",
            "experiments/figures",
            "--output-dir",
            "experiments/results/stage4_failure_mode_paper_assets",
        ],
        [
            sys.executable,
            "experiments/scripts/plot_stage4_representative_failure_traces.py",
            "--metrics-dir",
            "experiments/figures",
            "--output-dir",
            "experiments/results/stage4_representative_traces",
        ],
    ]
    for command in commands:
        subprocess.run(command, cwd=str(source_root), check=True)


def main_asset_specs():
    return [
        {
            "paper_item": "Table 1a protocol-split balanced robustness table",
            "target_filename": "main/table1_protocol_balanced_robustness.md",
            "source_path": (
                "experiments/results/stage4_balanced_robustness_assets/"
                "stage4_balanced_robustness_table.md"
            ),
            "paper_section": "Results",
            "supported_claim": (
                "risk_adapter_v1 is the most balanced learned / "
                "risk-conditioned method in the current two-protocol evaluation"
            ),
            "caveat": (
                "Descriptive counts only; no statistical significance or "
                "safety guarantee."
            ),
        },
        {
            "paper_item": "Table 1b protocol regret table",
            "target_filename": "main/table1_protocol_regret.md",
            "source_path": (
                "experiments/results/stage4_balanced_robustness_assets/"
                "stage4_protocol_regret_table.md"
            ),
            "paper_section": "Results",
            "supported_claim": (
                "risk_adapter_v1 has the lowest total regret relative to "
                "observed protocol oracles"
            ),
            "caveat": "Observed protocol oracle is not a theoretical optimum.",
        },
        {
            "paper_item": "Figure 3 balanced robustness Pareto frontier",
            "target_filename": "main/fig3_pareto.png",
            "source_path": (
                "experiments/results/stage4_balanced_robustness_assets/"
                "stage4_balanced_robustness_pareto.png"
            ),
            "paper_section": "Results",
            "supported_claim": (
                "windlevel_s085, fixed_s080, and risk_adapter_v1 form the "
                "observed Pareto frontier"
            ),
            "caveat": "Frontier is limited to evaluated methods and protocols.",
        },
        {
            "paper_item": "Figure 4 protocol regret bar chart",
            "target_filename": "main/fig4_protocol_regret.png",
            "source_path": (
                "experiments/results/stage4_balanced_robustness_assets/"
                "stage4_protocol_regret_bar.png"
            ),
            "paper_section": "Results",
            "supported_claim": "risk_adapter_v1 has the lowest total regret",
            "caveat": "Regret is relative to observed protocol oracles.",
        },
        {
            "paper_item": "Figure 5 invalid-only failure group stacked bar",
            "target_filename": "main/fig5_invalid_failure_groups.png",
            "source_path": (
                "experiments/results/stage4_failure_mode_paper_assets/"
                "stage4_failure_group_invalid_only_stacked_bar.png"
            ),
            "paper_section": "Failure Analysis",
            "supported_claim": (
                "invalid-only failure groups show heterogeneous invalid-run "
                "patterns"
            ),
            "caveat": (
                "Failure groups are diagnostic labels, not physical root-cause "
                "proof."
            ),
        },
        {
            "paper_item": "Figure 6a Trial 4 stress v21 failure trace",
            "target_filename": "main/fig6a_trial4_stress_v21_failure.png",
            "source_path": (
                "experiments/results/stage4_representative_traces/plots/"
                "goal_reissue_stress_risk_adapter_v21_trial4_repeat8.png"
            ),
            "paper_section": "Failure Analysis",
            "supported_claim": (
                "Trial 4 stress risk_adapter_v21 failure illustrates early "
                "pre-arrival vulnerability"
            ),
            "caveat": "Representative trace only; not population-level proof.",
        },
        {
            "paper_item": "Figure 6b Trial 4 stress fixed_s080 success trace",
            "target_filename": (
                "main/fig6b_trial4_stress_comparison_fixed_s080.png"
            ),
            "source_path": (
                "experiments/results/stage4_representative_traces/plots/"
                "goal_reissue_stress_fixed_s080_trial4_repeat7.png"
            ),
            "paper_section": "Failure Analysis",
            "supported_claim": (
                "fixed_s080 avoids some Trial 4 stress failure patterns"
            ),
            "caveat": "Representative trace only; not population-level proof.",
        },
        {
            "paper_item": "Figure 6c Trial 4 stress risk_adapter_v1 success trace",
            "target_filename": (
                "main/fig6c_trial4_stress_comparison_risk_adapter_v1.png"
            ),
            "source_path": (
                "experiments/results/stage4_representative_traces/plots/"
                "goal_reissue_stress_risk_adapter_v1_trial4_repeat10.png"
            ),
            "paper_section": "Failure Analysis",
            "supported_claim": (
                "risk_adapter_v1 avoids some Trial 4 stress v21 failure patterns"
            ),
            "caveat": "Representative trace only; not population-level proof.",
        },
        {
            "paper_item": "Figure 6d Trial 6 single-goal windlevel_s085 success trace",
            "target_filename": "main/fig6d_trial6_single_goal_windlevel_s085.png",
            "source_path": (
                "experiments/results/stage4_representative_traces/plots/"
                "single_goal_mission_windlevel_s085_trial6_repeat2.png"
            ),
            "paper_section": "Failure Analysis",
            "supported_claim": (
                "windlevel_s085 is a strong single-goal specialist in the "
                "Trial 6 bottleneck"
            ),
            "caveat": "Representative trace only; not population-level proof.",
        },
        {
            "paper_item": "Figure 6e Trial 6 single-goal v21 failure trace",
            "target_filename": (
                "main/fig6e_trial6_single_goal_risk_adapter_v21_failure.png"
            ),
            "source_path": (
                "experiments/results/stage4_representative_traces/plots/"
                "single_goal_mission_risk_adapter_v21_trial6_repeat6.png"
            ),
            "paper_section": "Failure Analysis",
            "supported_claim": (
                "lower scale is not automatically safer in the Trial 6 "
                "single-goal bottleneck"
            ),
            "caveat": "Representative trace only; not population-level proof.",
        },
    ]


def supplementary_specs():
    return [
        {
            "paper_item": "Supplementary full protocol split summary",
            "target_filename": "supplementary/full_protocol_split_summary.md",
            "source_path": (
                "experiments/results/stage4_protocol_split_paper_assets/"
                "stage4_protocol_split_summary.md"
            ),
            "paper_section": "Appendix",
            "supported_claim": "protocol-split success tables are auditable",
            "caveat": "Supplementary audit material; not main figure evidence.",
        },
        {
            "paper_item": "Supplementary balanced robustness summary",
            "target_filename": "supplementary/balanced_robustness_summary.md",
            "source_path": (
                "experiments/results/stage4_balanced_robustness_assets/"
                "stage4_balanced_robustness_summary.md"
            ),
            "paper_section": "Appendix",
            "supported_claim": "balanced robustness and regret calculations are auditable",
            "caveat": "Supplementary audit material; no statistical claim.",
        },
        {
            "paper_item": "Supplementary failure mode summary",
            "target_filename": "supplementary/failure_mode_summary.md",
            "source_path": (
                "experiments/results/stage4_failure_mode_paper_assets/"
                "stage4_failure_mode_summary.md"
            ),
            "paper_section": "Appendix",
            "supported_claim": "failure-mode accounting is auditable",
            "caveat": "Failure groups are diagnostic, not root-cause proof.",
        },
        {
            "paper_item": "Supplementary representative trace summary",
            "target_filename": "supplementary/representative_trace_summary.md",
            "source_path": (
                "experiments/results/stage4_representative_traces/"
                "stage4aa_representative_trace_summary.md"
            ),
            "paper_section": "Appendix",
            "supported_claim": "representative trace selection is auditable",
            "caveat": "Trace set is qualitative and selected.",
        },
    ]


def todo_specs():
    return [
        {
            "paper_item": "Figure 1 system architecture schematic TODO",
            "target_filename": "TODO/fig1_architecture_TODO.md",
            "source_path": "",
            "paper_section": "Method",
            "supported_claim": (
                "the execution governor is stack-compatible and uses "
                "speed_scale / acceleration_scale"
            ),
            "caveat": "Manual schematic still required; not a formal safety filter.",
            "todo_title": "Figure 1 Architecture Schematic TODO",
            "todo_body": [
                "Draw the AutoTrans-like planner, payload MPC, and SO3 controller stack.",
                "Show the external risk-conditioned execution governor.",
                "Show `speed_scale` and `acceleration_scale` entering through the command-adaptation interface.",
                "Show risk input and command adaptation output.",
                "Caption caveat: empirical governor, not a certified safety filter.",
            ],
        },
        {
            "paper_item": "Figure 2 protocol split schematic TODO",
            "target_filename": "TODO/fig2_protocol_split_TODO.md",
            "source_path": "",
            "paper_section": "Experimental Setup",
            "supported_claim": (
                "single-goal and goal-reissue stress protocols test different "
                "system behavior"
            ),
            "caveat": "Manual schematic still required; no mixed-protocol aggregate.",
            "todo_title": "Figure 2 Protocol Split Schematic TODO",
            "todo_body": [
                "Draw `goal_repeat=1` as the single-goal mission protocol.",
                "Draw `goal_repeat=10` as the goal-reissue stress protocol.",
                "Show that the two protocols test different behavior.",
                "Caption caveat: report protocols separately and avoid a mixed-protocol aggregate.",
            ],
        },
    ]


def copy_asset(spec, source_root, output_dir, missing_status):
    target_rel = Path(spec["target_filename"])
    target_path = output_dir / target_rel
    source_path = resolve_from(source_root, spec["source_path"])

    if source_path.exists():
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(source_path), str(target_path))
        status = "copied"
    else:
        status = missing_status

    return {
        "paper_item": spec["paper_item"],
        "target_filename": str(target_rel),
        "source_path": relpath(source_path, source_root),
        "status": status,
        "paper_section": spec["paper_section"],
        "supported_claim": spec["supported_claim"],
        "caveat": spec["caveat"],
    }


def write_todo(spec, output_dir):
    target_rel = Path(spec["target_filename"])
    target_path = output_dir / target_rel
    target_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# %s" % spec["todo_title"],
        "",
        "## Purpose",
        "",
        spec["supported_claim"],
        "",
        "## Required Content",
        "",
    ]
    lines.extend("- %s" % item for item in spec["todo_body"])
    lines.extend(
        [
            "",
            "## Caveat",
            "",
            spec["caveat"],
            "",
        ]
    )
    target_path.write_text("\n".join(lines), encoding="utf-8")
    return {
        "paper_item": spec["paper_item"],
        "target_filename": str(target_rel),
        "source_path": "",
        "status": "todo_manual",
        "paper_section": spec["paper_section"],
        "supported_claim": spec["supported_claim"],
        "caveat": spec["caveat"],
    }


def write_manifest_csv(rows, output_dir):
    path = output_dir / "stage4_paper_figure_manifest.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=MANIFEST_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in MANIFEST_FIELDS})
    return path


def md_cell(value):
    text = str(value or "").replace("\n", " ")
    return text.replace("|", "\\|")


def write_manifest_md(rows, output_dir):
    path = output_dir / "stage4_paper_figure_manifest.md"
    lines = [
        "# Stage 4 Paper Figure Manifest",
        "",
        "| paper_item | target_filename | source_path | status | paper_section | supported_claim | caveat |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| %s | %s | %s | %s | %s | %s | %s |"
            % (
                md_cell(row["paper_item"]),
                md_cell(row["target_filename"]),
                md_cell(row["source_path"]),
                md_cell(row["status"]),
                md_cell(row["paper_section"]),
                md_cell(row["supported_claim"]),
                md_cell(row["caveat"]),
            )
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def rows_with_prefix(rows, prefix):
    return [row for row in rows if row["target_filename"].startswith(prefix)]


def write_summary(rows, output_dir, regenerated):
    path = output_dir / "stage4_paper_figure_package_summary.md"
    main_rows = rows_with_prefix(rows, "main/")
    supplementary_rows = rows_with_prefix(rows, "supplementary/")
    todo_rows = rows_with_prefix(rows, "TODO/")
    copied_main = [row for row in main_rows if row["status"] == "copied"]
    copied_supp = [row for row in supplementary_rows if row["status"] == "copied"]
    missing_rows = [row for row in rows if row["status"].startswith("missing")]

    lines = [
        "# Stage 4 Paper Figure Package Summary",
        "",
        "## Executive Summary",
        "",
        "Stage 4-AL2 assembled a paper figure package from existing generated Stage 4 assets.",
        "Default behavior is copy/check only; source assets were regenerated only if `--regenerate` was explicitly provided.",
        "This run used `--regenerate=%s`." % ("true" if regenerated else "false"),
        "",
        "`risk_adapter_v1` remains the balanced learned / risk-conditioned protagonist.",
        "`risk_adapter_v21` remains a strong nominal / single-goal variant or ablation, not the final method.",
        "",
        "## Main Paper Assets Copied",
        "",
        "| paper_item | target_filename | status | source_path |",
        "| --- | --- | --- | --- |",
    ]
    for row in main_rows:
        lines.append(
            "| %s | %s | %s | %s |"
            % (
                md_cell(row["paper_item"]),
                md_cell(row["target_filename"]),
                md_cell(row["status"]),
                md_cell(row["source_path"]),
            )
        )
    lines.extend(
        [
            "",
            "Copied main assets: `%d/%d`." % (len(copied_main), len(main_rows)),
            "",
            "## Supplementary Assets Copied",
            "",
            "| paper_item | target_filename | status | source_path |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in supplementary_rows:
        lines.append(
            "| %s | %s | %s | %s |"
            % (
                md_cell(row["paper_item"]),
                md_cell(row["target_filename"]),
                md_cell(row["status"]),
                md_cell(row["source_path"]),
            )
        )
    lines.extend(
        [
            "",
            "Copied supplementary assets: `%d/%d`." % (len(copied_supp), len(supplementary_rows)),
            "",
            "## Missing Manual Assets",
            "",
        ]
    )
    if todo_rows:
        for row in todo_rows:
            lines.append(
                "- `%s`: `%s` (%s)"
                % (row["target_filename"], row["paper_item"], row["status"])
            )
    else:
        lines.append("- None.")
    lines.extend(
        [
            "",
            "## Claim Alignment",
            "",
            "| paper_item | supported_claim | caveat |",
            "| --- | --- | --- |",
        ]
    )
    for row in main_rows + todo_rows:
        lines.append(
            "| %s | %s | %s |"
            % (
                md_cell(row["paper_item"]),
                md_cell(row["supported_claim"]),
                md_cell(row["caveat"]),
            )
        )
    lines.extend(
        [
            "",
            "## What Still Needs Manual Work",
            "",
            "- Create the Figure 1 architecture schematic.",
            "- Create the Figure 2 protocol split schematic.",
            "- Decide the final multi-panel layout and caption for Figure 6.",
            "- Polish final captions against the claim mapping table.",
            "- Resolve citation placeholders through Stage 4-AM2 before final manuscript assembly.",
            "- Move or export paper-ready files into the manuscript source tree only after final formatting is chosen.",
            "",
            "## Reminder",
            "",
            "- No mixed-protocol aggregate.",
            "- No `risk_adapter_v21` overall-best claim.",
            "- No statistical significance claim.",
            "- No safety guarantee.",
            "- No `risk_adapter_v22`.",
        ]
    )
    if missing_rows:
        lines.extend(["", "## Missing Source Assets", ""])
        for row in missing_rows:
            lines.append(
                "- `%s`: expected `%s` (%s)"
                % (
                    row["target_filename"],
                    row["source_path"],
                    row["status"],
                )
            )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def build_package(source_root, output_dir, regenerate):
    if regenerate:
        run_offline_regenerators(source_root)

    output_dir.mkdir(parents=True, exist_ok=True)
    for dirname in ("main", "supplementary", "TODO"):
        (output_dir / dirname).mkdir(parents=True, exist_ok=True)

    rows = []
    for spec in main_asset_specs():
        rows.append(copy_asset(spec, source_root, output_dir, "missing_required"))
    for spec in supplementary_specs():
        rows.append(copy_asset(spec, source_root, output_dir, "missing_optional"))
    for spec in todo_specs():
        rows.append(write_todo(spec, output_dir))

    csv_path = write_manifest_csv(rows, output_dir)
    md_path = write_manifest_md(rows, output_dir)
    summary_path = write_summary(rows, output_dir, regenerate)
    return rows, csv_path, md_path, summary_path


def print_summary(rows, output_dir, summary_path):
    main_rows = rows_with_prefix(rows, "main/")
    supplementary_rows = rows_with_prefix(rows, "supplementary/")
    copied_main = sum(1 for row in main_rows if row["status"] == "copied")
    copied_supp = sum(1 for row in supplementary_rows if row["status"] == "copied")
    missing = [row for row in rows if row["status"].startswith("missing")]
    todo = [row for row in rows if row["status"] == "todo_manual"]
    print("Stage 4 paper figure package")
    print("output_dir: %s" % output_dir)
    print("main copied: %d/%d" % (copied_main, len(main_rows)))
    print("supplementary copied: %d/%d" % (copied_supp, len(supplementary_rows)))
    print("missing source assets: %d" % len(missing))
    print("manual TODO assets: %d" % len(todo))
    print("summary: %s" % summary_path)


def main():
    args = parse_args()
    source_root = resolve_from(REPO_ROOT, args.source_root)
    output_dir = resolve_from(source_root, args.output_dir)
    rows, _csv_path, _md_path, summary_path = build_package(
        source_root, output_dir, args.regenerate
    )
    if args.print_summary:
        print_summary(rows, output_dir, summary_path)


if __name__ == "__main__":
    main()
