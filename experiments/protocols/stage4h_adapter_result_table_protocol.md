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

The current aggregate result is:

| Method | Trial 4+5+6 valid runs |
| --- | ---: |
| `original` | `9/15` |
| `fixed_s085` | `9/15` |
| `windlevel_s085` | `6/15` |
| `risk_adapter_v1` | `13/15` |

`risk_adapter_v1` is the current strongest aggregate candidate, but
`fixed_s085` remains best on Trial 4 with `5/5` valid runs.
