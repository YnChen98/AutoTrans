# Stage 4-W Protocol-Split Paper Assets Protocol

## Purpose

Stage 4-W generates paper-ready tables, a summary Markdown file, and one
success-rate figure that separate Stage 4 results by goal protocol.

The generator is offline only. It does not run ROS, simulation, RViz, or
`catkin_make`.

The protocol split is now required because `goal_repeat=1` and `goal_repeat=10`
test different system properties:

- `goal_repeat=1`: single-goal mission protocol
- `goal_repeat=10`: goal-reissue stress protocol

These results must not be mixed into one aggregate table without protocol
labels.

Stage 4-X0 freezes the final evaluation completion plan in
`experiments/protocols/stage4x_final_evaluation_spec.md`. Stage 4-X2 completes
the missing single-goal baselines in
`experiments/protocols/stage4x_single_goal_baseline_completion_result.md`.

## Inputs

Default metrics directory:

```bash
experiments/figures
```

The script reads `*_metrics_summary.txt` files and recomputes strict-valid
counts from run-level metrics.

Single-goal mission protocol inputs:

- `goal_repeat=1`
- wind: `strong`
- trials: Trial 4, Trial 5, Trial 6
- repeats: repeat1 through repeat10
- methods: `original`, `fixed_s085`, `windlevel_s085`, `fixed_s080`,
  `risk_adapter_v1`, `risk_adapter_v2`, `risk_adapter_v21`

Goal-reissue stress protocol inputs:

- `goal_repeat=10`
- wind: `strong`
- trials: Trial 4, Trial 5, Trial 6
- repeats: repeat1 through repeat10
- methods: `original`, `fixed_s085`, `windlevel_s085`,
  `risk_adapter_v1`, `fixed_s080`, `risk_adapter_v21`

## Claim Scope Warning

The completed single-goal comparison set includes all seven current methods:
`original`, `fixed_s085`, `windlevel_s085`, `fixed_s080`,
`risk_adapter_v1`, `risk_adapter_v2`, and `risk_adapter_v21`.
`windlevel_s085` is the completed single-goal aggregate leader at `26/30`;
`risk_adapter_v1` and `risk_adapter_v21` are tied at `25/30`.

The current goal-reissue stress comparison set includes `original`,
`fixed_s085`, `windlevel_s085`, `risk_adapter_v1`, `fixed_s080`, and
`risk_adapter_v21`. Stage 4-X1 records the corrected `risk_adapter_v21`
stress result as `20/30`.

Paper-facing wording must still keep protocol labels explicit. The
single-goal mission and goal-reissue stress results should not be combined into
one mixed-protocol aggregate because the protocols test different system
properties.

The Stage 4-X0 matrix is complete. The next paper-facing task is to regenerate
the protocol-split assets with all seven single-goal methods and the corrected
six-method goal-reissue stress table.

## Outputs

Default output directory:

```bash
experiments/results/stage4_protocol_split_paper_assets
```

Generated outputs:

- `stage4_single_goal_success_table.csv`
- `stage4_single_goal_success_table.md`
- `stage4_repeated_goal_stress_success_table.csv`
- `stage4_repeated_goal_stress_success_table.md`
- `stage4_protocol_split_aggregate_table.csv`
- `stage4_protocol_split_aggregate_table.md`
- `stage4_protocol_split_summary.md`
- `stage4_protocol_split_success_rates.png`

Generated outputs under `experiments/results/` should not be committed.

If `matplotlib` is unavailable, the script prints a warning and skips only the
PNG figure. CSV and Markdown outputs are still generated.

## Strict-Valid Metric

Paper-facing success uses strict-valid / `label_strict_invalid`, not raw
`valid_run_suggested` alone.

The script computes strict-valid as:

- `valid_run_suggested=true`
- `has_nan_state=false`
- `max_swing_angle_deg < 60`
- `max_uav_speed < 4`
- `max_payload_speed < 4`
- `final_uav_xy_error <= 0.5`

Diagnostic labels can inform interpretation, but strict-valid remains the
paper-facing success metric.

## Filename Assumptions

Goal-reissue stress filenames:

```text
stage4_<method>_strong_trial<trial>_repeat<repeat>_metrics_summary.txt
stage4_fixed_s080_strong_trial<trial>_frontier_repeat<repeat>_metrics_summary.txt
```

Single-goal `fixed_s080` filenames:

```text
stage4t2_fixed_s080_strong_trial4_goalrepeat1_repeat<repeat>_metrics_summary.txt
stage4u_fixed_s080_strong_trial<trial>_goalrepeat1_repeat<repeat>_metrics_summary.txt
```

Single-goal `risk_adapter_v2` filenames:

```text
stage4t2_risk_adapter_v2_strong_trial4_goalrepeat1_repeat<repeat>_metrics_summary.txt
stage4u_risk_adapter_v2_strong_trial<trial>_goalrepeat1_repeat<repeat>_metrics_summary.txt
```

Single-goal `risk_adapter_v21` filenames:

```text
stage4v_risk_adapter_v21_strong_trial<trial>_goalrepeat1_screening_repeat<repeat>_metrics_summary.txt
```

The `risk_adapter_v21` filenames include `screening`, but repeat1 through
repeat10 are the Stage 4-V4 10-repeat expansion.

Stage 4-X2 single-goal baseline filenames:

```text
stage4x_singlegoal_<method>_strong_trial<trial>_goalrepeat1_repeat<repeat>_metrics_summary.txt
```

These cover `original`, `fixed_s085`, `windlevel_s085`, and
`risk_adapter_v1` under the completed single-goal mission protocol.

The generator validates computed strict-valid counts against the frozen Stage
4-U2 / Stage 4-V4 / Stage 4-X2 / Stage 4-J / Stage 4-R results before writing
outputs. Generated goal-reissue stress tables should include the corrected
Stage 4-X1 result: `risk_adapter_v21` `20/30`.

## Claim Limits

Safe paper-facing claims:

- Under the completed single-goal mission protocol, `windlevel_s085` achieved
  the highest aggregate at `26/30` strict-valid.
- Under the completed single-goal mission protocol, `risk_adapter_v1` and
  `risk_adapter_v21` each achieved `25/30` strict-valid.
- Among the currently evaluated goal-reissue stress methods, `fixed_s080`
  achieved `24/30` strict-valid.
- Under goal-reissue stress, `risk_adapter_v21` achieved `20/30`, below
  `fixed_s080` `24/30` and `risk_adapter_v1` `23/30`.
- In the completed single-goal comparison set, `risk_adapter_v21` improves
  over `original`, `fixed_s080`, `fixed_s085`, and `risk_adapter_v2` in
  aggregate, but Trial 6 remains a bottleneck.
- `windlevel_s085` is a strong non-learning heuristic baseline and should be
  treated separately from `fixed_s085` because it uses topic-based command
  adaptation.
- The two protocols test different system properties.

Avoid:

- statistical significance
- safety guarantee
- mixing `goal_repeat=1` and `goal_repeat=10` into one aggregate
- claiming `risk_adapter_v21` is the best single-goal method
- claiming `risk_adapter_v21` beats all single-goal baselines
- claiming a learned method uniformly dominates heuristic or fixed baselines
- describing `fixed_s080` as the overall best method across protocols
- describing `windlevel_s085` as the overall best method across protocols
- claiming `risk_adapter_v21` is the best goal-reissue stress method
- claiming `risk_adapter_v21` is a cross-protocol final winner
- mixed-protocol aggregate claims
- claiming diagnostic labels prove exact root cause
- claiming `risk_adapter_v21` solves all failures
- describing `risk_adapter_v1` as overall best after including `fixed_s080`

## How To Run

From the repository root:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/generate_stage4_protocol_split_paper_assets.py \
  --metrics-dir experiments/figures \
  --output-dir experiments/results/stage4_protocol_split_paper_assets \
  --print-summary
```

Generated outputs under `experiments/results/` should not be committed.
