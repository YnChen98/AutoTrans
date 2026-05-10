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

The manifest includes `original`, `fixed_s085`, `windlevel_s085`,
`risk_adapter_v0` where available, and `risk_adapter_v1`.

Manifest entries may temporarily have unequal per-target repeat counts. The
current manifest uses 10 repeats for Trial 4 while Trial 5 and Trial 6 remain
at 5 repeats. The generated aggregate table is therefore a weighted aggregate
over currently available repeats, not a final balanced comparison.

Final fair comparison should equalize repeats across Trial 4, Trial 5, and
Trial 6 before making broader claims.

Future result manifests should support manual annotations such as
`collision_observed` and `path_infeasible` when visual inspection identifies
obstacle contact, abnormal post-contact motion, or planned path-through-
obstacle behavior.

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

When per-target repeat counts are unequal, the aggregate table is a weighted
available-repeat aggregate. It should be read as "what the current manifest
contains", not as a final balanced comparison. Final paper comparison should
equalize repeat counts across Trial 4, Trial 5, and Trial 6 before making
broader claims.

The current aggregate result is:

| Method | Current available valid runs |
| --- | ---: |
| `original` | `13/20` |
| `fixed_s085` | `13/20` |
| `windlevel_s085` | `9/20` |
| `risk_adapter_v1` | `16/20` |

`risk_adapter_v1` is the current strongest weighted aggregate candidate, but
`fixed_s085` remains best on Trial 4 with `9/10` valid runs. This aggregate is
not final because Trial 4 has 10 repeats while Trial 5 and Trial 6 still have
5 repeats.
