# Stage 2-B Drag-Wind Results Summary

## Executive Summary

Stage 2-B uses velocity-relative linear drag as the simulator plant wind disturbance. This replaces direct constant `fq` force injection, which was abandoned for benchmark use because it caused instability and `NaN` failures.

The current formal strong benchmark is the `0.0075 N` cap setting:

- `wind_velocity_x=0.5`
- `wind_drag_linear=0.015`
- `wind_max_force=0.0075`

The `0.01 N` cap setting is boundary/stress only. It can produce valid runs, but Trial 2 produced repeated invalid runs, so it is not frozen as a stable benchmark.

The current Stage 2-B stop condition is to stop increasing wind magnitude and use the frozen matrix below for reproducible benchmark comparison.

## Implementation Snapshot

- Wind model: velocity-relative linear drag.
- `wind_apply_to=quadrotor`.
- No payload/both wind.
- No quadratic drag: `wind_drag_quad=0.0`.
- No step/sine wind in the simulator benchmark.
- Independent `/wind_force` is used as a logging annotation signal through `wind_signal_publisher`; it is not the simulator-computed drag force.
- Wind configuration should be changed with `experiments/scripts/set_drag_wind_config.py`, not by manual YAML editing.

## Benchmark Level Table

| Level | wind_velocity_x | wind_drag_linear | wind_max_force | Intended use | Current status |
| --- | ---: | ---: | ---: | --- | --- |
| none | 0.0 | 0.0 | 0.0 | no-wind baseline | valid baseline condition |
| weak | 0.5 | 0.004 | 0.002 | weak wind benchmark | valid |
| moderate | 0.5 | 0.010 | 0.005 | moderate wind benchmark | mostly valid; one invalid run occurred |
| strong | 0.5 | 0.015 | 0.0075 | formal stable strong benchmark | selected and frozen as current strong setting |
| boundary | 0.5 | 0.020 | 0.010 | boundary/stress test only | not stable enough for formal benchmark |

## Evidence Summary

- No-wind regression passed. The corrected baseline runner has valid Trial 1, Trial 2, and Trial 3 evidence in the baseline result markdown files.
- Zero-drag enabled regression passed. Enabling the drag-wind path with zero effective disturbance did not break the no-wind behavior.
- `0.002 N` cap is valid as weak wind. The recorded weak run has `valid_run_suggested: true`, no `NaN` state, bounded speeds, and physically reasonable final state.
- `0.005 N` cap is mostly valid. One invalid run occurred, but multiple later repeats were valid, so this level remains useful as the moderate benchmark with repeat checks.
- `0.0075 N` cap is valid across Trial 1, Trial 2, Trial 3, and additional Trial 2/Trial 3 repeats. It is the current formal strong stable benchmark.
- `0.01 N` cap is valid in some runs but invalid repeatedly on Trial 2. It is retained only as boundary/stress evidence and should not be used as the formal stable benchmark.

## Recommended Official Matrix

Use this matrix for the next formal experiment round:

| Condition | Trial 1 `(0.0, -1.2)` | Trial 2 `(-7.5, 1.5)` | Trial 3 `(8.0, 1.5)` | Role |
| --- | --- | --- | --- | --- |
| no wind baseline | run | run | run | baseline comparison |
| weak wind | run | run | run | weak disturbance benchmark |
| moderate wind | run | run | run | moderate disturbance benchmark |
| strong wind | run | run | run | formal strong benchmark |
| boundary wind | optional | optional | optional | stress test only, not stable benchmark |

## Validity Criteria

A normal benchmark run is valid only if all of the following are true:

- `valid_run_suggested: true`
- `has_nan_state: false`
- `final_row_has_nan: false`
- `max_uav_speed < 4.0`
- `max_payload_speed < 4.0`
- `max_swing_angle_deg < 60`
- final UAV/payload state is physically reasonable and near the intended target region

For `boundary` stress tests, still record these fields. Any violation should be treated as boundary evidence, not ignored.

## Invalid Run Policy

Do not delete invalid runs. Record invalid runs in result markdown with the wind level, target, `CSV` filename, and failed metrics.

Invalid runs are useful for identifying boundary conditions. Repeated invalid runs disqualify a wind level from being frozen as stable, even if some runs at that level are valid.

## Reproduction Commands

Run all commands from the repository root:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
```

Set no wind:

```bash
python3 experiments/scripts/set_drag_wind_config.py --level none
```

Set weak wind:

```bash
python3 experiments/scripts/set_drag_wind_config.py --level weak
```

Set moderate wind:

```bash
python3 experiments/scripts/set_drag_wind_config.py --level moderate
```

Set strong wind:

```bash
python3 experiments/scripts/set_drag_wind_config.py --level strong
```

Set boundary wind:

```bash
python3 experiments/scripts/set_drag_wind_config.py --level boundary
```

Match `/wind_force` annotation to the selected force cap when logging wind runs.

Weak:

```bash
roslaunch autotrans_logger wind_signal_publisher.launch enable_wind:=true wind_mode:=constant wind_force_x:=0.002 wind_max_force:=0.002
```

Moderate:

```bash
roslaunch autotrans_logger wind_signal_publisher.launch enable_wind:=true wind_mode:=constant wind_force_x:=0.005 wind_max_force:=0.005
```

Strong:

```bash
roslaunch autotrans_logger wind_signal_publisher.launch enable_wind:=true wind_mode:=constant wind_force_x:=0.0075 wind_max_force:=0.0075
```

Boundary:

```bash
roslaunch autotrans_logger wind_signal_publisher.launch enable_wind:=true wind_mode:=constant wind_force_x:=0.01 wind_max_force:=0.01
```

Trial 1:

```bash
bash experiments/scripts/run_baseline_trial.sh --name stage2b_LEVEL_trial1 --x 0.0 --y -1.2 --z 0.0 --duration 75
```

Trial 2:

```bash
bash experiments/scripts/run_baseline_trial.sh --name stage2b_LEVEL_trial2 --x -7.5 --y 1.5 --z 0.0 --duration 75
```

Trial 3:

```bash
bash experiments/scripts/run_baseline_trial.sh --name stage2b_LEVEL_trial3 --x 8.0 --y 1.5 --z 0.0 --duration 75
```

Analyze the latest log:

```bash
python3 experiments/autotrans_logger/scripts/analyze_log.py
cat experiments/figures/metrics_summary.txt
```

Always restore no wind after each wind run:

```bash
python3 experiments/scripts/set_drag_wind_config.py --level none
```

Before committing, verify that the simulator YAML is not accidentally modified:

```bash
git status --short
```

## Current Stop Condition

- Do not increase beyond `0.01 N` in this stage.
- Do not enable payload/both wind.
- Do not enable quadratic drag.
- Do not add step/sine wind yet.
- The next task should be formal data aggregation or plotting, not new wind physics.

## Next Recommended Tasks

- Build a CSV/Markdown result table from selected valid runs.
- Generate comparison plots for no wind vs weak/moderate/strong.
- Only after result aggregation, consider controller-side robustness improvements.
