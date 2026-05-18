# Stage 4-AL2 Paper Figure Package Protocol

## Purpose

Stage 4-AL2 creates a clean paper figure package from existing Stage 4 paper
assets. The goal is to collect the current main-paper tables, generated plots,
representative traces, supplementary summaries, and manual schematic TODOs in
one package directory before manuscript formatting.

This stage does not run simulation, does not create new experimental evidence,
and does not introduce `risk_adapter_v22`.

## Inputs

The package generator reads existing generated assets from:

- `experiments/results/stage4_balanced_robustness_assets/`
- `experiments/results/stage4_failure_mode_paper_assets/`
- `experiments/results/stage4_representative_traces/`
- `experiments/results/stage4_protocol_split_paper_assets/`

Main expected source assets include:

- `experiments/results/stage4_balanced_robustness_assets/stage4_balanced_robustness_table.md`
- `experiments/results/stage4_balanced_robustness_assets/stage4_protocol_regret_table.md`
- `experiments/results/stage4_balanced_robustness_assets/stage4_balanced_robustness_pareto.png`
- `experiments/results/stage4_balanced_robustness_assets/stage4_protocol_regret_bar.png`
- `experiments/results/stage4_failure_mode_paper_assets/stage4_failure_group_invalid_only_stacked_bar.png`
- `experiments/results/stage4_representative_traces/plots/*.png`

## Outputs

Default output directory:

`experiments/results/stage4_paper_figure_package`

Package layout:

- `main/`
  - `table1_protocol_balanced_robustness.md`
  - `table1_protocol_regret.md`
  - `fig3_pareto.png`
  - `fig4_protocol_regret.png`
  - `fig5_invalid_failure_groups.png`
  - selected Figure 6 representative trace PNG files
- `supplementary/`
  - copied summary files when available
- `TODO/`
  - `fig1_architecture_TODO.md`
  - `fig2_protocol_split_TODO.md`
- `stage4_paper_figure_manifest.csv`
- `stage4_paper_figure_manifest.md`
- `stage4_paper_figure_package_summary.md`

Generated outputs under `experiments/results/` must not be committed.

## Default Copy-Only Behavior

By default, `create_stage4_paper_figure_package.py` does not regenerate source
assets. It only:

- checks whether each expected source asset exists,
- copies available main-paper and supplementary assets,
- writes TODO files for the manual schematics,
- records missing assets in the manifest,
- writes a package summary.

Missing manual schematic assets are expected and are not fatal.

## Optional Regeneration Behavior

The `--regenerate` flag explicitly allows offline source asset regeneration
before packaging. This flag may call existing offline generators:

- `experiments/scripts/generate_stage4_protocol_split_paper_assets.py`
- `experiments/scripts/generate_stage4_balanced_robustness_assets.py`
- `experiments/scripts/generate_stage4_failure_mode_paper_assets.py`
- `experiments/scripts/plot_stage4_representative_failure_traces.py`

Do not use `--regenerate` unless the intent is to refresh generated assets.
Even with `--regenerate`, this stage must not run simulation, `roslaunch`,
RViz, or `catkin_make`.

## Manual Schematic TODOs

Figure 1 and Figure 2 remain manual / future generated schematics:

- Figure 1 should show the AutoTrans-like planner, payload MPC, SO3 controller,
  external risk-conditioned execution governor, risk input, and
  `speed_scale` / `acceleration_scale` interface.
- Figure 2 should show the single-goal mission protocol (`goal_repeat=1`) and
  goal-reissue stress protocol (`goal_repeat=10`) as separate evaluation
  regimes.

The TODO files in the package record the required content and caveats.

## Claim / Caveat Alignment

The manifest keeps every packaged item aligned to:

- paper section,
- supported claim,
- source asset,
- caveat.

The package should preserve the Stage 4-AL claim boundaries:

- no mixed-protocol aggregate,
- no `risk_adapter_v21` overall-best claim,
- no statistical significance claim,
- no safety guarantee,
- no failure-group root-cause proof,
- no `risk_adapter_v22`.

## How To Run

Copy/check only:

```bash
python3 experiments/scripts/create_stage4_paper_figure_package.py \
  --output-dir experiments/results/stage4_paper_figure_package \
  --print-summary
```

Explicit offline regeneration before packaging:

```bash
python3 experiments/scripts/create_stage4_paper_figure_package.py \
  --output-dir experiments/results/stage4_paper_figure_package \
  --regenerate \
  --print-summary
```

The default command is the recommended safe path for manuscript packaging.
