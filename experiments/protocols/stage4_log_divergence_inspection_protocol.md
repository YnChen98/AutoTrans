# Stage 4 Log Divergence Inspection Protocol

## Purpose

Stage 4 invalid runs include several sudden fly-away or teleport-like failures
after apparently stable flight. These failures need separate classification
because a simple valid/invalid label does not explain whether the run failed
from target error, strict safety violation, command saturation, command NaN,
state divergence, obstacle contact, or path feasibility.

`experiments/scripts/inspect_stage4_log_divergence.py` is an offline CSV
inspection helper. It does not run ROS, simulation, RViz, or `catkin_make`.

## Motivating Example

A detailed inspection of original Trial 6 repeat10 showed:

- first nonfinite value: `so3_thrust` at `t=14.950161`
- at `t=14.900`, SO3 commands were saturated:
  - `so3_thrust=60.0`
  - `so3_bodyrate_x=-3.0`
  - `so3_bodyrate_y=3.0`
  - `so3_bodyrate_z=1.2`
- `first_uav_speed_gt4` occurred later at `t=15.250058`
- `first_payload_speed_gt4` occurred later at `t=15.350023`
- `first_uav_position_jump_gt1m` occurred later at `t=15.849978`

This ordering suggests that command saturation or command NaN can precede
state divergence. The inspection tool is intended to make that timing
repeatable instead of relying on ad hoc manual checks.

## What The Tool Computes

For each CSV log, the tool reports timing for:

- first nonfinite value and its column
- first SO3 thrust/bodyrate NaN
- first SO3 thrust/bodyrate saturation
- first UAV/payload speed thresholds at `4 m/s` and `10 m/s`
- first swing thresholds at `30 deg` and `60 deg`
- first UAV/payload position jump above `1 m`
- first `has_trajectory` time
- last finite UAV/payload position before the first nonfinite value when
  available

For batch mode, it reads `*_metrics_summary.txt` files, extracts the referenced
`csv_path`, and combines analyzer summary fields with the same CSV divergence
inspection.

## Usage

Inspect one CSV around a suspected divergence window:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/inspect_stage4_log_divergence.py \
  --csv experiments/logs/autotrans_log_20260510_190453.csv \
  --window-start 13.5 \
  --window-end 16.5 \
  --print-summary
```

Scan all metrics summaries and write an ignored report:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/inspect_stage4_log_divergence.py \
  --metrics-glob "experiments/figures/*_metrics_summary.txt" \
  --output-csv experiments/results/stage4_log_divergence_report.csv \
  --print-summary
```

Generated reports under `experiments/results/` should not be committed.

## Failure Mode Caveats

The `failure_mode_guess` field is best-effort. It is intended for triage and
manifest annotation, not as a definitive physical diagnosis.

Command NaN before state divergence is possible. In those cases, the first
visible fly-away may be downstream of an earlier command failure.

Obstacle collision and path infeasibility remain manual annotations unless
they are explicitly logged. Visual inspection is still required for cases
where the UAV appears to contact an obstacle or where the planned path appears
to pass through an obstacle.

Current logs do not include the full reference trajectory. Therefore planner
trajectory discontinuity or planned path-through-obstacle behavior cannot be
proven from the CSV alone.
