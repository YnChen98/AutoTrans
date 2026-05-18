# Stage 4-AA2 Representative Trace Protocol

## Purpose

Stage 4-AA2 generates offline representative trace plots from existing CSV
logs. It is a mechanism-diagnosis step before any `risk_adapter_v22` decision.

The goal is to inspect whether the next policy step should be phase-aware,
failure-aware, reference-jump-aware, or unnecessary. This step does not run
ROS, simulation, RViz, or `catkin_make`.

## Why Representative Traces Are Needed

Stage 4-AB reframed the paper away from a `risk_adapter_v21` universal-winner
story and toward:

- learned risk-conditioned execution governor
- protocol-split robustness evaluation
- balanced robustness / regret analysis
- failure-mode-aware diagnosis

The current aggregate tables show protocol specialization, but they do not
explain the mechanism. Representative traces are needed before deciding
whether a new `risk_adapter_v22` variant is justified.

Current interpretation:

- `windlevel_s085` is the single-goal mission specialist at `26/30`.
- `fixed_s080` is the goal-reissue stress specialist at `24/30`.
- `risk_adapter_v1` is the tentative balanced learned / risk-conditioned
  protagonist.
- `risk_adapter_v21` is a strong nominal variant / ablation, not the final
  cross-protocol method.

## Selected Slices

The generator selects representative runs automatically from existing
`*_metrics_summary.txt` files under `experiments/figures`.

Selection group A: Trial 4 goal-reissue stress, `risk_adapter_v21`

- one strict-valid run
- one `command_control_upstream` invalid run
- one `state_task_upstream` invalid run
- one `command_nan_coincident_with_state_divergence` run if available

Selection group B: Trial 4 goal-reissue stress comparison

- `fixed_s080` valid or near-best run
- `risk_adapter_v1` valid or near-best run
- `risk_adapter_v21` failed run

Selection group C: Trial 6 single-goal bottleneck

- `windlevel_s085` valid run
- `fixed_s080` valid run
- `risk_adapter_v1` valid and/or invalid run
- `risk_adapter_v21` valid and/or invalid run
- `original` invalid run if available

Selection group D: optional balanced-protagonist examples

- one `risk_adapter_v1` single-goal success
- one `risk_adapter_v1` goal-reissue stress success

## Plotted Signals

For each selected run, the generator reads the linked `csv_path` and plots the
signals that are available:

- UAV / payload speed over time
- `swing_angle_deg` over time
- target XY error or UAV-reference position error over time
- `command_speed_scale` and `command_acceleration_scale` over time
- `command_risk_score_3s` and `command_risk_score_5s` over time
- `goal_received_count` over time
- `trajectory_update_count` or `trajectory_time_since_last_update` over time
- vertical markers for `first_arrival_time` and `first_nan_time` when
  available

Missing columns are recorded in the generated summary. Missing signals are
skipped instead of causing the script to fail.

## Outputs

Generated outputs go under:

```bash
experiments/results/stage4_representative_traces
```

The generator writes:

- `stage4aa_representative_trace_index.csv`
- `stage4aa_representative_trace_index.md`
- `stage4aa_representative_trace_summary.md`
- PNG plots under `experiments/results/stage4_representative_traces/plots/`

Generated CSV, Markdown, and PNG outputs under `experiments/results/` are
ignored and should not be committed.

## How To Run

From the repository root:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/plot_stage4_representative_failure_traces.py \
  --metrics-dir experiments/figures \
  --output-dir experiments/results/stage4_representative_traces \
  --print-summary
```

## How To Use In The Paper

Use Stage 4-AA2 traces as qualitative support for failure-mode-aware diagnosis,
not as the main success-rate result. The main result should remain the
protocol-split strict-valid table and balanced robustness / regret analysis.

Paper-safe uses:

- illustrate why Trial 4 goal-reissue stress remains difficult for
  `risk_adapter_v21`
- compare `fixed_s080`, `risk_adapter_v1`, and `risk_adapter_v21` under the
  same stress slice
- inspect why learned variants trail `windlevel_s085` and `fixed_s080` on
  single-goal Trial 6
- motivate a generic mechanism only if the traces support it

Do not use Stage 4-AA2 to claim:

- exact physical root cause
- statistical significance
- a safety guarantee
- that `risk_adapter_v22` is required before human plot review
- that a Trial-4-specific patch is justified

## Limitations

- Representative traces are selected examples, not a replacement for repeated
  success-rate comparison.
- `failure_group` and `failure_mode_guess` are diagnostic labels, not perfect
  root-cause proof.
- Missing CSV columns can limit which signals appear in a plot.
- Very large invalid-run values may require symmetric log y-axis scaling for
  readability.

## v22 Decision Rule

Do not create `risk_adapter_v22` before reviewing Stage 4-AA2 trace outputs.

Create `risk_adapter_v22` only if the representative traces reveal a generic
phase-aware or failure-aware mechanism that can plausibly improve
dual-protocol balance. Do not create a Trial-4-specific or target-specific
patch.

If no generic mechanism appears, proceed with the Stage 4-AB
`risk_adapter_v1`-centered paper narrative and treat `risk_adapter_v21` as a
strong nominal variant / ablation.
