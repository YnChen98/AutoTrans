# Stage 2-B Drag-Wind Experiment Protocol

## Purpose

Stage 2-B uses velocity-relative linear drag as the real plant wind disturbance in the simulator. The wind disturbance is configured through `uav_simulator/uav_simulator/config/so3_quadrotor.yaml`, and the reproducible entry point is:

```bash
python3 experiments/scripts/set_drag_wind_config.py --level LEVEL
```

This replaces direct constant `fq` force injection for benchmark runs. Direct constant force injection caused instability and `NaN` failures, so it is not used as the formal Stage 2-B benchmark disturbance.

The goal of Stage 2-B is reproducible benchmark experiments, not maximal wind magnitude. The frozen levels below are intentionally conservative enough to support repeated trials and fair comparison between future planning/control changes.

## Benchmark Levels

All non-`none` levels use:

- `enable_wind=true`
- `wind_model=drag`
- `wind_velocity_y=0.0`
- `wind_velocity_z=0.0`
- `wind_drag_quad=0.0`
- `wind_apply_to=quadrotor`

| Level | enable_wind | wind_model | wind_velocity_x | wind_drag_linear | wind_drag_quad | wind_max_force | Intended use |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| none | false | drag | 0.0 | 0.0 | 0.0 | 0.0 | no wind baseline |
| weak | true | drag | 0.5 | 0.004 | 0.0 | 0.002 | weak wind benchmark |
| moderate | true | drag | 0.5 | 0.010 | 0.0 | 0.005 | moderate wind benchmark |
| strong | true | drag | 0.5 | 0.015 | 0.0 | 0.0075 | formal stable strong benchmark |
| boundary | true | drag | 0.5 | 0.020 | 0.0 | 0.010 | boundary/stress test only |

Current experimental conclusion:

- `0.002 N` cap: valid weak wind.
- `0.005 N` cap: mostly valid, but one invalid run occurred.
- `0.0075 N` cap: selected as the formal strong stable benchmark.
- `0.01 N` cap: boundary/unstable setting because Trial 2 had repeated invalid runs.

Do not use `boundary` as the formal stable benchmark unless additional repeated Trial 1, Trial 2, and Trial 3 evidence is valid.

## Set Wind Config

Run all commands from the repository root:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
```

Show the current wind config:

```bash
python3 experiments/scripts/set_drag_wind_config.py --show
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

Before writing a config, preview it with `--dry-run` when needed:

```bash
python3 experiments/scripts/set_drag_wind_config.py --level strong --dry-run
```

## Wind Signal Publisher

`wind_signal_publisher` publishes `/wind_force` as an annotation/logging signal. For Stage 2-B drag-wind runs, match this signal to the same force cap as the selected simulator level.

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

For no-wind baseline runs, either do not start `wind_signal_publisher`, or publish zero wind:

```bash
roslaunch autotrans_logger wind_signal_publisher.launch enable_wind:=false wind_mode:=none wind_force_x:=0.0 wind_max_force:=0.0
```

## Baseline Trial Commands

Run each trial with the selected wind level already set in `so3_quadrotor.yaml`.

Trial 1 target `(0.0, -1.2)`:

```bash
bash experiments/scripts/run_baseline_trial.sh --name stage2b_LEVEL_trial1 --x 0.0 --y -1.2 --z 0.0 --duration 75
```

Trial 2 target `(-7.5, 1.5)`:

```bash
bash experiments/scripts/run_baseline_trial.sh --name stage2b_LEVEL_trial2 --x -7.5 --y 1.5 --z 0.0 --duration 75
```

Trial 3 target `(8.0, 1.5)`:

```bash
bash experiments/scripts/run_baseline_trial.sh --name stage2b_LEVEL_trial3 --x 8.0 --y 1.5 --z 0.0 --duration 75
```

Replace `LEVEL` with `none`, `weak`, `moderate`, `strong`, or `boundary`.

## Analyzer Commands

After each trial, run:

```bash
python3 experiments/autotrans_logger/scripts/analyze_log.py
cat experiments/figures/metrics_summary.txt
```

Copy the relevant metrics into a result markdown file under `experiments/protocols/`. Do not commit generated CSV, PNG, or TXT files.

## Validity Criteria

A run is valid only if all of the following are true:

- `valid_run_suggested: true`
- `has_nan_state: false`
- `final_row_has_nan: false`
- `max_uav_speed < 4.0` for normal benchmark runs
- `max_payload_speed < 4.0` for normal benchmark runs
- `max_swing_angle_deg < 60` for normal benchmark runs
- final UAV/payload positions are physically reasonable and near the intended target region

For `boundary` stress tests, record any violation explicitly. A stress-test run can be useful evidence, but it should not be counted as a stable benchmark run unless it also satisfies the normal benchmark criteria.

## Invalid-Run Policy

Do not delete invalid runs. Record invalid runs in protocol/result markdown with the CSV filename, target, wind level, and failed metrics.

Invalid runs are useful for identifying boundary conditions. If a benchmark level has repeated invalid runs, do not freeze it as a stable setting.

## Repeat Policy

For a wind level to be considered stable, run:

- Trial 1: `(0.0, -1.2)`
- Trial 2: `(-7.5, 1.5)`
- Trial 3: `(8.0, 1.5)`

If any trial fails, repeat that target at least twice. A stable benchmark should have repeated valid evidence, not just one successful run.

## YAML Safety Rule

Always restore no wind after each wind experiment:

```bash
python3 experiments/scripts/set_drag_wind_config.py --level none
```

Before committing, run:

```bash
git status --short
```

Ensure `uav_simulator/uav_simulator/config/so3_quadrotor.yaml` is not modified. If it is modified only because of a wind experiment, restore no wind with the helper before committing.

## Current Recommended Matrix

| Matrix item | Trial 1 | Trial 2 | Trial 3 | Role |
| --- | --- | --- | --- | --- |
| no wind baseline | yes | yes | yes | baseline comparison |
| weak wind | yes | yes | yes | stable weak disturbance |
| moderate wind | yes | yes | yes | moderate disturbance with repeat checks |
| strong wind | yes | yes | yes | formal stable strong benchmark |
| boundary | optional | optional | optional | stress test only |

## What Not To Do

- Do not manually edit `uav_simulator/uav_simulator/config/so3_quadrotor.yaml` unless debugging.
- Do not commit generated CSV, PNG, or TXT files.
- Do not use `0.01 N` boundary as the formal stable benchmark.
- Do not increase wind beyond `0.01 N` in this stage.
- Do not enable payload/both wind.
- Do not enable quadratic drag.
- Do not add step/sine wind yet.
