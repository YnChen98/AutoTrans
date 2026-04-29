# Baseline Trial 3 Invalid Result

## Basic Information

- Date: 2026-04-29
- Branch: autotrans-deploy
- Commit SHA: c106bd38c2616220c163b28b8145cd1fbbeb8929
- Trial name: trial3
- Run type: non-interactive terminal runner
- Valid run: no

## Intended Target Point

- target_x: 8.0
- target_y: 1.5
- target_z: 0.0

## Metrics

- sample_count: 1867
- duration_sec: 89.041688
- effective_log_rate_hz: 20.956476
- has_trajectory_ratio: 0.960364
- mean_swing_angle_deg: 2.495034
- max_swing_angle_deg: 41.298981
- p95_swing_angle_deg: 13.869499
- max_uav_speed: 2.628435
- mean_uav_speed: 0.097020
- max_payload_speed: 2.537794
- mean_payload_speed: 0.175679
- uav_path_length: 8.993513
- payload_path_length: 16.189491
- final_uav_position: (-8.307044, -0.188211, 1.881615)
- final_payload_position: (-8.307114, -0.188158, 1.213170)

## Qualitative Notes

Trial 3 was intended to reach target (8.0, 1.5), but the final UAV and payload positions are far from the intended target.

The run did not catastrophically diverge, but it cannot be used as a valid baseline because the commanded goal was not reached. The maximum swing angle is also much larger than Trial 1 and Trial 2.

The shell command used for this trial may have included an accidental standalone argument line: 8.0 \ . Future runner versions should reject unknown positional arguments to avoid ambiguous experiments.

## Validity Decision

- Valid run: no
- Reason:
  - final UAV position is far from the intended target (8.0, 1.5)
  - final payload position is also far from the intended target
  - final altitude differs from the usual settled baseline altitude
  - max_swing_angle_deg is noticeably higher than Trial 1 and Trial 2
  - command input may have contained an accidental extra positional argument

## Next Action

Do not use this run as a valid baseline.

Next, improve run_baseline_trial.sh so it rejects unknown positional arguments, then rerun Trial 3 with a cleaner command or use a safer verified target point.
