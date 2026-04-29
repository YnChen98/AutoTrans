# Baseline Trial 1 Valid Result

## Basic Information

- Date: 2026-04-29
- Branch: autotrans-deploy
- Commit SHA: de6ff79811a91cef41064ae0dfbd3efc5cfd1496
- Trial name: trial1
- Run type: non-interactive terminal runner
- Valid run: yes

## Commands

Launch command:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
bash experiments/scripts/run_baseline_trial.sh --name trial1 --x 0.0 --y -1.2 --z 0.0 --duration 75 --startup_wait 15 --goal_repeat 3 --goal_interval 1.0
```

Analyzer command:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/autotrans_logger/scripts/analyze_log.py
```

## CSV File

- CSV filename: experiments/logs/autotrans_log_20260429_204208.csv

## Target Point

- target_x: 0.0
- target_y: -1.2
- target_z: 0.0
- duration_sec requested: 75

## Metrics

- sample_count: 1875
- duration_sec: 93.699989
- effective_log_rate_hz: 20.000002
- has_trajectory_ratio: 0.958933
- mean_swing_angle_deg: 0.766033
- max_swing_angle_deg: 17.945416
- p95_swing_angle_deg: 6.901148
- max_uav_speed: 2.556923
- mean_uav_speed: 0.170931
- max_payload_speed: 2.590570
- mean_payload_speed: 0.177423
- uav_path_length: 15.821692
- payload_path_length: 16.432259
- final_uav_position: (0.000000, -1.200000, 1.468415)
- final_payload_position: (-0.000000, -1.200000, 0.799970)

## Qualitative Notes

This trial was generated using the corrected non-interactive baseline runner.

The run is physically reasonable. The UAV converged to the target region near (0.0, -1.2), the final altitude remained stable, and the payload settled below the UAV with near-zero final swing angle. The maximum swing angle occurred during transient motion and did not indicate divergence.

Compared with the previous invalid automated trial, this run confirms that the corrected runner can reproduce the expected RViz 2D Nav Goal workflow.

## Validity Decision

- Valid run: yes
- Reason:
  - final UAV position is close to the target
  - final UAV altitude is physically reasonable
  - final payload position is physically reasonable
  - max UAV and payload speeds are reasonable
  - mean and p95 swing angles are moderate
  - trajectory was received for most of the run

## Next Action

Use this corrected runner for additional baseline trials before adding wind disturbance.

Recommended next trials:
1. Trial 2: target (-7.5, 1.5), duration 75 s
2. Trial 3: target (8.0, 1.5), duration 75 s

Do not proceed to wind disturbance until at least three valid baseline trials are recorded.
