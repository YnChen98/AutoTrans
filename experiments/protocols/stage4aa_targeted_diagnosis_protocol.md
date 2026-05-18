# Stage 4-AA Targeted Diagnosis Protocol

## Purpose

Stage 4-AA generates targeted diagnosis assets for the two follow-up questions
raised by Stage 4-Z2:

- Why does `risk_adapter_v21` perform poorly on Trial 4 under the
  goal-reissue stress protocol?
- Why does Trial 6 remain a bottleneck for the learned/risk-conditioned
  variants?

This is an offline paper-support step. It does not run ROS, simulation, RViz,
or `catkin_make`.

Stage 4-AA2 should use representative trace inspection to support the
`risk_adapter_v22` decision. A new variant is justified only if the inspected
traces reveal a generic phase-aware or failure-aware mechanism; otherwise the
paper should proceed with the Stage 4-AB reframing around `risk_adapter_v1` as
the balanced learned / risk-conditioned governor.

The Stage 4-AA2 trace protocol is
`experiments/protocols/stage4aa_representative_trace_protocol.md`. Its plotter
is `experiments/scripts/plot_stage4_representative_failure_traces.py`.

## Why These Slices

Trial 4 goal-reissue stress is selected because corrected Stage 4-X1 results
showed `risk_adapter_v21` at `4/10` strict-valid there. Stage 4-Z2 also showed
that the broader `risk_adapter_v21` stress weakness includes multiple
diagnostic groups, so Trial 4 should be inspected before describing it as a
purely post-arrival artifact.

Trial 6 is selected because it remains a bottleneck in the completed
single-goal comparison:

- `fixed_s080`: `8/10`
- `windlevel_s085`: `9/10`
- `risk_adapter_v1`: `7/10`
- `risk_adapter_v21`: `6/10`

Under goal-reissue stress, Trial 6 is more even among the leading methods:

- `fixed_s080`: `7/10`
- `risk_adapter_v1`: `7/10`
- `risk_adapter_v21`: `7/10`

This makes Trial 6 useful for separating target-specific behavior from
protocol-specific behavior.

## Inputs

Default metrics directory:

```bash
experiments/figures
```

The generator reads `*_metrics_summary.txt` files and their linked CSV logs.
It reuses the Stage 4-Z2 strict-valid calculation, diagnostic inspector, and
`failure_group` mapping.

Trial 4 goal-reissue stress input:

- `stage4x_risk_adapter_v21_goalreissue_strong_trial4_goalrepeat10_repeat{repeat}_metrics_summary.txt`

Trial 6 single-goal inputs:

- `stage4x_singlegoal_original_strong_trial6_goalrepeat1_repeat{repeat}_metrics_summary.txt`
- `stage4x_singlegoal_fixed_s085_strong_trial6_goalrepeat1_repeat{repeat}_metrics_summary.txt`
- `stage4x_singlegoal_windlevel_s085_strong_trial6_goalrepeat1_repeat{repeat}_metrics_summary.txt`
- `stage4u_fixed_s080_strong_trial6_goalrepeat1_repeat{repeat}_metrics_summary.txt`
- `stage4x_singlegoal_risk_adapter_v1_strong_trial6_goalrepeat1_repeat{repeat}_metrics_summary.txt`
- `stage4u_risk_adapter_v2_strong_trial6_goalrepeat1_repeat{repeat}_metrics_summary.txt`
- `stage4v_risk_adapter_v21_strong_trial6_goalrepeat1_screening_repeat{repeat}_metrics_summary.txt`

Trial 6 goal-reissue stress inputs:

- `stage4_original_strong_trial6_repeat{repeat}_metrics_summary.txt`
- `stage4_fixed_s085_strong_trial6_repeat{repeat}_metrics_summary.txt`
- `stage4_windlevel_s085_strong_trial6_repeat{repeat}_metrics_summary.txt`
- `stage4_risk_adapter_v1_strong_trial6_repeat{repeat}_metrics_summary.txt`
- `stage4_fixed_s080_strong_trial6_frontier_repeat{repeat}_metrics_summary.txt`
- `stage4x_risk_adapter_v21_goalreissue_strong_trial6_goalrepeat10_repeat{repeat}_metrics_summary.txt`

## Outputs

Generated outputs go under:

```bash
experiments/results/stage4_targeted_diagnosis
```

The generator writes:

- `stage4aa_trial4_stress_v21_run_table.csv`
- `stage4aa_trial4_stress_v21_run_table.md`
- `stage4aa_trial6_bottleneck_run_table.csv`
- `stage4aa_trial6_bottleneck_run_table.md`
- `stage4aa_trial6_method_summary.csv`
- `stage4aa_trial6_method_summary.md`
- `stage4aa_targeted_diagnosis_summary.md`
- `stage4aa_trial4_stress_v21_failure_timing.png`
- `stage4aa_trial6_success_by_method.png`

Generated CSV, Markdown, and PNG outputs under `experiments/results/` are
ignored and should not be committed.

## Failure-Group Mapping

Stage 4-AA uses the same mapping as Stage 4-Z2:

| failure_group | Mapping logic |
| --- | --- |
| `valid_or_warning` | Any strict-valid run. |
| `command_control_upstream` | `command_saturation_before_nan`, `command_nan_before_state_divergence`, or `command_nan_coincident_with_state_divergence`. |
| `planner_reference_upstream` | `reference_jump_before_command_nan`, or goal-reissue stress failure after arrival with `first_failure_after_arrival_flag=true`. |
| `state_task_upstream` | `state_divergence_before_command_nan`, `strict_safety_no_nan`, `target_error_only`, no-arrival failure, or final XY failure without a stronger command/planner category. |
| `unknown` | Anything not mapped above. |

Strict-valid remains the paper-facing metric. The failure groups are
diagnostic, not proof of exact physical root cause.

## Limitations

- The labels do not prove exact physical root cause.
- A post-arrival flag does not explain every stress failure.
- The targeted slices do not prove that `risk_adapter_v21` is globally flawed.
- The targeted slices do not prove that `risk_adapter_v22` is required.
- Representative failed CSVs or plots may still need manual inspection before
  any new method design.

## How To Run

From the repository root:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/generate_stage4_targeted_diagnosis_assets.py \
  --metrics-dir experiments/figures \
  --output-dir experiments/results/stage4_targeted_diagnosis \
  --print-summary
```

## How To Use In The Paper

Use Stage 4-AA as supporting evidence for failure-mode-aware analysis, not as
the main success-rate result. The main result should remain the protocol-split
strict-valid success table from Stage 4-W3.

Paper-safe uses:

- explain why Trial 4 goal-reissue stress needs targeted diagnosis before
  tuning a new variant
- show that Trial 6 behavior differs between single-goal and stress protocols
- motivate phase-aware or failure-aware follow-up analysis if representative
  failures support it

Do not use Stage 4-AA to claim:

- exact physical root cause
- all stress failures are post-arrival
- `risk_adapter_v21` is globally flawed
- `risk_adapter_v22` is required before inspecting the targeted outputs
- a Trial-4-specific patch is a valid next method without a generic mechanism
- Stage 4-AA2 plots have been reviewed before running the AA2 plotter
