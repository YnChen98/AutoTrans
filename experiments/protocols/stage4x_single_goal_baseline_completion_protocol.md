# Stage 4-X2 Single-Goal Baseline Completion Protocol

## Purpose

Stage 4-X2 completes the missing single-goal mission baselines required by the
protocol-split Stage 4 paper evaluation.

The current single-goal mission protocol (`goal_repeat=1`) includes:

| Method | Strict-valid count |
| --- | ---: |
| `fixed_s080` | `21/30` |
| `risk_adapter_v2` | `21/30` |
| `risk_adapter_v21` | `25/30` |

It does not yet include `original`, `fixed_s085`, `windlevel_s085`, or
`risk_adapter_v1`. Therefore `risk_adapter_v21` must not be claimed to beat
all single-goal baselines until these four missing methods are evaluated under
the same single-goal protocol.

## Required Methods

Complete these missing methods:

- `original`
- `fixed_s085`
- `windlevel_s085`
- `risk_adapter_v1`

## Protocol Definition

For every method:

- protocol: single-goal mission protocol
- `goal_repeat=1`
- wind: `strong`
- trials: Trial 4, Trial 5, Trial 6
- repeats: repeat1 through repeat10
- paper-facing metric: strict-valid / `label_strict_invalid`
- run duration: `75`
- startup wait: `25`
- goal interval: `1.0`

Trial targets:

| Trial | `x` | `y` | `z` | `target_x` | `target_y` | `target_z` | `payload_target_z` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Trial 4 | `-3.5` | `-1.2` | `0.0` | `-3.5` | `-1.2` | `1.468415` | `0.799970` |
| Trial 5 | `3.5` | `0.8` | `0.0` | `3.5` | `0.8` | `1.468415` | `0.799970` |
| Trial 6 | `0.0` | `1.5` | `0.0` | `0.0` | `1.5` | `1.468415` | `0.799970` |

## Naming Convention

Run names and metrics summaries use:

```text
stage4x_singlegoal_<method>_strong_trial<trial>_goalrepeat1_repeat<repeat>
stage4x_singlegoal_<method>_strong_trial<trial>_goalrepeat1_repeat<repeat>_metrics_summary.txt
```

Examples:

- `stage4x_singlegoal_original_strong_trial4_goalrepeat1_repeat1`
- `stage4x_singlegoal_fixed_s085_strong_trial5_goalrepeat1_repeat7`
- `stage4x_singlegoal_windlevel_s085_strong_trial6_goalrepeat1_repeat10`
- `stage4x_singlegoal_risk_adapter_v1_strong_trial4_goalrepeat1_repeat3`

## Helper Script

Use:

```bash
python3 experiments/scripts/run_stage4_single_goal_baseline_completion.py \
  --method original \
  --trials 4 5 6 \
  --repeats 1 2 3 4 5 6 7 8 9 10 \
  --dry-run \
  --print-commands
```

Default behavior is dry-run / print-only. The helper must not execute ROS
simulation unless `--execute` is explicitly provided.

When `--execute` is used, the helper attempts to detect the distinct new CSV
after each run and calls `experiments/autotrans_logger/scripts/analyze_log.py`
with explicit `--csv`. After the batch, still run a duplicate `csv_path` check
before treating the outputs as paper-facing records.

## Adapter Prerequisites

For every method, start `wind_signal_publisher` as the wind annotation signal:

```bash
roslaunch autotrans_logger wind_signal_publisher.launch enable_wind:=true wind_mode:=constant wind_force_x:=0.0075 wind_max_force:=0.0075
```

`original`:

- no command-adaptation adapter process required
- planner command adaptation disabled

`fixed_s085`:

- no command-adaptation adapter process required
- planner fixed mode with `manager/speed_scale=0.85` and
  `manager/acceleration_scale=0.85`

`windlevel_s085`:

- planner topic mode with `manager/require_adaptation_topic_ready=true`
- start:

```bash
roslaunch command_adaptation heuristic_command_adapter.launch policy_mode:=wind_level
```

`risk_adapter_v1`:

- planner topic mode with `manager/require_adaptation_topic_ready=true`
- start:

```bash
roslaunch command_adaptation risk_conditioned_command_adapter.launch \
  enable_risk_conditioning:=true \
  policy_mode:=risk_conditioned \
  risk_threshold_3s:=0.5 \
  risk_threshold_5s:=0.5 \
  hard_threshold_5s:=0.7 \
  soft_scale_3s:=0.75 \
  soft_scale_5s:=0.65 \
  hard_scale_5s:=0.60 \
  scale_rate_limit_per_sec:=0.5
```

## Strict-Valid Metric

A run is strict-valid only when all of these are true:

- `valid_run_suggested=true`
- `has_nan_state=false`
- `max_swing_angle_deg < 60`
- `max_uav_speed < 4`
- `max_payload_speed < 4`
- `final_uav_xy_error <= 0.5`

Do not use raw `valid_run_suggested` alone as the paper-facing metric.

## Restore Commands

After each batch, restore wind and planner adaptation:

```bash
python3 experiments/scripts/set_drag_wind_config.py --level none
```

Restore planner no-op adaptation:

```text
manager/enable_command_adaptation=false
manager/adaptation_mode=none
manager/speed_scale=1.0
manager/acceleration_scale=1.0
manager/require_adaptation_topic_ready=false
```

## Claim Limits

- Do not claim statistical significance.
- Do not claim a safety guarantee.
- Do not mix `goal_repeat=1` and `goal_repeat=10` aggregates.
- Do not claim `risk_adapter_v21` beats all single-goal baselines until
  `original`, `fixed_s085`, `windlevel_s085`, and `risk_adapter_v1` are
  complete under `goal_repeat=1`.
- Do not create a new `risk_adapter_v22` or other new method variant before
  Stage 4-X2 is complete.

## Next Decision Rule

After all four missing methods are complete:

1. Regenerate the protocol-split paper assets.
2. Decide whether `risk_adapter_v21` remains strongest in the completed
   single-goal mission protocol.
3. Combine that single-goal decision with the corrected goal-reissue stress
   result, where `fixed_s080` remains strongest and `risk_adapter_v21` achieved
   `20/30`.
4. Decide whether the paper should position `risk_adapter_v21` as a
   nominal-goal method with a stress limitation, or whether a new phase-aware
   final method is needed.
