# Stage 4-I Adapter Result Table Protocol

## Purpose

Stage 4-I adds a small static result-table generator for the completed
Stage 4-H `risk_adapter_v1` limited evaluation. It turns the committed
summary manifest into reproducible Markdown and CSV tables for Trial 4,
Trial 5, and Trial 6.

This script does not run ROS, simulation, RViz, `catkin_make`, or any trial
command. It only reads a JSON manifest and writes summary files under
`experiments/results/`.

## Manifest Structure

The manifest is:

```bash
experiments/protocols/stage4h_adapter_limited_eval_manifest.json
```

Each entry in `results` contains:

- `trial_id`
- `target_x`
- `target_y`
- `method`
- `repeat_count`
- `valid_count`
- `invalid_count`
- `success_rate`
- `notes`
- `source_protocol_doc`

The current balanced manifest includes `original`, `fixed_s085`,
`windlevel_s085`, and `risk_adapter_v1`.

The current manifest supports a balanced 30-repeat comparison for the main
Trial 4, Trial 5, and Trial 6 methods: `original`, `fixed_s085`,
`windlevel_s085`, and `risk_adapter_v1` each have 10 repeats per target.
Historical `risk_adapter_v0` repeat results remain in their source protocol
documents, but they are not included in this balanced manifest.

For the main four methods, Trial 4/5/6 repeat counts are now equalized. This
supports a fair 30-repeat aggregate, while still remaining limited-repeat
simulation evidence rather than a statistical proof.

Paper-facing safety comparison should use strict-valid /
`label_strict_invalid` interpretation as the primary success metric.
`valid_run_suggested` can overestimate safety success when swing or payload
speed exceeds strict thresholds, as seen in Trial 5 runs that passed
target/NaN checks but violated safety limits.

Trial 6 10-repeat expansion is recorded in
`experiments/protocols/stage4j_trial6_10repeat_fair_comparison.md`.

Invalid runs should also include failure-mode labels so success rate is not
interpreted without failure context.

For paper-facing tables, strict-valid / `label_strict_invalid` remains the
success metric, while failure-mode labels explain why invalid runs failed.
Transient labels such as `command_saturation_without_divergence` should not be
counted as invalid by themselves unless strict-valid / `label_strict_invalid`
also marks the run invalid.

Failure-mode labels and manual annotations explain mechanisms, but they do not
replace strict-valid / `label_strict_invalid` success accounting.

Future result manifests should support manual annotations such as
`collision_observed` and `path_infeasible` when visual inspection identifies
obstacle contact, abnormal post-contact motion, or planned path-through-
obstacle behavior.

Final result summaries should optionally join strict-valid metrics with
Stage 4-O manual failure annotations from
`experiments/protocols/stage4o_manual_failure_annotations.json`. These
annotations should explain invalid-run failure causes, not replace
strict-valid / `label_strict_invalid` success accounting.

Invalid runs should be classified beyond valid/invalid whenever possible.
Future manifests should support:

- `manual_collision_observed`
- `manual_path_infeasible`
- `manual_teleport_like_divergence`
- `divergence_failure_mode`
- `manual_failure_note`

Use `experiments/scripts/inspect_stage4_log_divergence.py` to produce
repeatable timing evidence for command saturation, command NaN, speed
threshold crossings, swing thresholds, and teleport-like position jumps.
Final fair comparison should report both success rate and failure-mode
distribution.

## How To Run

From the repository root:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/summarize_stage4h_adapter_results.py \
  --manifest experiments/protocols/stage4h_adapter_limited_eval_manifest.json \
  --output-md experiments/results/stage4h_adapter_limited_eval_summary.md \
  --output-csv experiments/results/stage4h_adapter_limited_eval_summary.csv \
  --print-summary
```

## Outputs

The script writes:

- `experiments/results/stage4h_adapter_limited_eval_summary.md`
- `experiments/results/stage4h_adapter_limited_eval_summary.csv`

The Markdown output includes:

- Executive Summary
- Per-Trial Comparison
- Aggregate Comparison
- Interpretation
- What Not To Claim

The Interpretation section is derived from the manifest. It computes
per-trial best method(s), aggregate best method(s), and per-method aggregate
valid counts from the current `results` entries instead of relying on
hard-coded Stage 4-H numbers.

The CSV output contains one row per manifest result entry with:

- `trial_id`
- `method`
- `valid_count`
- `repeat_count`
- `invalid_count`
- `success_rate`
- `notes`

Generated files under `experiments/results/` should not be committed.

## Limitations

The result table is based on manually recorded limited-repeat evaluation
summaries. It is not a statistical test and does not prove final online
robustness or safety.

For the main four methods, the current aggregate table is now a balanced
Trial 4/5/6 30-repeat comparison.

The current aggregate result is:

| Method | Current available valid runs |
| --- | ---: |
| `original` | `18/30` |
| `fixed_s085` | `18/30` |
| `windlevel_s085` | `16/30` |
| `risk_adapter_v1` | `23/30` |

`risk_adapter_v1` is the strongest balanced aggregate candidate, but
`fixed_s085` remains best on Trial 4 with `9/10` valid runs. Do not claim
`risk_adapter_v1` beats every baseline on every target.
