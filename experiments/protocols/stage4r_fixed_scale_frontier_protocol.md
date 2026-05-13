# Stage 4-R Fixed-Scale Frontier Protocol

## Purpose

Stage 4-R screens fixed command-adaptation scales before adding new learned or
risk-conditioned variants. The goal is to answer a reviewer-facing baseline
question: whether a better fixed scale, such as `0.70` or `0.75`, can match or
exceed `risk_adapter_v1`.

This is a screening protocol, not a final paper comparison. It should be run
before tuning `risk_adapter_v2`.

## Background

The Stage 4-J balanced 30-repeat strong-wind result is:

| method | strict_valid | total |
| --- | --- | --- |
| `original` | 18 | 30 |
| `fixed_s085` | 18 | 30 |
| `windlevel_s085` | 16 | 30 |
| `risk_adapter_v1` | 23 | 30 |

`fixed_s085` already covers fixed scale `0.85`, so Stage 4-R reuses that
existing evidence instead of rerunning it during screening.

## Scale List

Screen these new fixed scales:

- `0.60`
- `0.65`
- `0.70`
- `0.75`
- `0.80`
- `0.90`

Together with the existing `fixed_s085` result, this forms a first fixed-scale
frontier around the current `risk_adapter_v1` policy.

## Screening Design

For each new scale:

- trials: `trial4`, `trial5`, `trial6`
- repeats: `repeat1`, `repeat2`, `repeat3`
- runs per trial: 3
- total runs per scale: 9
- total new runs for 6 scales: 54

This is intentionally smaller than the formal 10-repeat main comparison. It is
used to find competitive fixed-scale candidates before spending more simulation
time.

## Planner Configuration

Each run uses fixed planner-side command adaptation:

```text
manager/enable_command_adaptation=true
manager/adaptation_mode=fixed
manager/speed_scale=<scale>
manager/acceleration_scale=<scale>
manager/require_adaptation_topic_ready=false
```

After screening, restore the planner to no-op adaptation:

```text
manager/enable_command_adaptation=false
manager/adaptation_mode=none
manager/speed_scale=1.0
manager/acceleration_scale=1.0
manager/require_adaptation_topic_ready=false
```

Also restore wind with:

```bash
python3 experiments/scripts/set_drag_wind_config.py --level none
```

## Trial Targets

`trial4`:

```text
x=-3.5
y=-1.2
z=0.0
target_x=-3.5
target_y=-1.2
target_z=1.468415
payload_target_z=0.799970
```

`trial5`:

```text
x=3.5
y=0.8
z=0.0
target_x=3.5
target_y=0.8
target_z=1.468415
payload_target_z=0.799970
```

`trial6`:

```text
x=0.0
y=1.5
z=0.0
target_x=0.0
target_y=1.5
target_z=1.468415
payload_target_z=0.799970
```

## Naming Convention

Use:

```text
stage4_fixed_s<scale_no_dot>_strong_trial<trial>_frontier_repeat<repeat>
```

Examples:

```text
stage4_fixed_s075_strong_trial4_frontier_repeat1
stage4_fixed_s060_strong_trial6_frontier_repeat3
```

Metrics summaries should be copied to:

```text
experiments/figures/stage4_fixed_s<scale_no_dot>_strong_trial<trial>_frontier_repeat<repeat>_metrics_summary.txt
```

Generated CSV, PNG, TXT, and Markdown outputs should not be committed.

## Strict-Valid Metric

Screening should use the same paper-facing strict-valid convention as Stage
4-J and Stage 4-Q1:

- `valid_run_suggested=true`
- `has_nan_state=false`
- `max_swing_angle_deg < 60`
- `max_uav_speed < 4`
- `max_payload_speed < 4`
- `final_uav_xy_error <= target_xy_tolerance`

Use target-error args when running `experiments/autotrans_logger/scripts/analyze_log.py`:

```text
--target_x
--target_y
--target_z
--payload_target_z
--target_xy_tolerance 0.5
```

## Helper Runner

`experiments/scripts/run_stage4_fixed_scale_frontier.py` generates shell
commands for one scale at a time. Default behavior is print-only / dry-run
safe. It does not modify planner XML or run ROS unless `--execute` is provided.

Example dry run:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/run_stage4_fixed_scale_frontier.py \
  --scale 0.75 \
  --trials 4 5 6 \
  --repeats 1 2 3 \
  --duration 75 \
  --startup-wait 25 \
  --goal-repeat 10 \
  --goal-interval 1.0 \
  --dry-run \
  --print-commands
```

`--execute` is explicit because it will modify
`planner/plan_manage/launch/planning_node_params.xml`, run ROS simulation
through `experiments/scripts/run_baseline_trial.sh`, run offline analysis, copy
metrics summaries, and then print/attempt restore commands.

## Interpretation

Stage 4-R screening results are not final paper claims. With only 3 repeats per
trial, they are used for candidate selection and failure-mode review.

Decision rule:

1. Rank fixed scales by strict-valid count across the 9 screening runs.
2. Compare failure-mode profile against Stage 4-Q1 audit labels.
3. Select the top 1-2 fixed scales if they are competitive with
   `risk_adapter_v1` or clearly improve over `fixed_s085`.
4. Expand selected scales to 10 repeats per Trial 4/5/6 before making a
   paper-facing claim.

Do not claim statistical significance, safety guarantee, or final superiority
from the 3-repeat screening alone.
