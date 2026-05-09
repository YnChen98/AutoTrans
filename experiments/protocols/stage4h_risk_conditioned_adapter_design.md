# Stage 4-H Risk-Conditioned Command Adapter Design

## Executive Summary

Stage 4-H designs a risk-conditioned command adapter for AutoTrans strong-wind
experiments. The adapter should use early failure-risk prediction to adapt the
planner command scale before an unstable run develops further.

The first implementation must be soft and conservative. It should reduce command
scale gradually, never issue a hard stop, and never replace the planner or
controller.

The adapter must be no-op by default. Unless explicitly enabled, it should not
change AutoTrans behavior, planner settings, controller behavior, or simulator
behavior.

## Motivation

Stage 4-G shows that early failure-risk signal exists in the 90-row strict-label
dataset. The target label is `label_strict_invalid`.

The `3s` and `5s` feature windows are early enough for online use. They have
high recall, which is useful for an early warning signal, but only moderate
precision.

The `10s` and `15s` windows improve precision, AUROC, and AUPRC. They are useful
for monitoring and offline diagnostics, but they may be too late for fast
failures.

Direct hard intervention is not justified yet. The first online policy should
therefore treat risk prediction as a conservative soft command-scaling signal,
not as a safety certificate or hard guard.

## Proposed Runtime Architecture

Stage 4-H should extend the existing adapter approach or add a new adapter node
under:

```bash
experiments/command_adaptation
```

The node should subscribe to:

- `/visual_slam/odom`
- `/payload_odom`
- `/wind_force`
- `/planning/trajectory` if needed

The node should publish:

- `/command_adaptation/speed_scale`
- `/command_adaptation/acceleration_scale`

Keep the `PlannerManager` topic readiness gate unchanged. The planner-side
runtime adaptation interface should still use:

- `manager/enable_command_adaptation=true`
- `manager/adaptation_mode=topic`
- `manager/require_adaptation_topic_ready=true`

The adapter remains an external experimental node. It must not replace
planner-side trajectory generation or `payload_mpc_controller`.

## Feature Computation

The adapter should maintain rolling buffers for UAV odometry and payload
odometry. These buffers should be timestamped and should support online feature
windows without using future samples.

For the first online intervention, compute `3s` and `5s` features online:

- `max_uav_speed`
- `max_payload_speed`
- `mean_uav_speed`
- `mean_payload_speed`
- `max_swing_angle_deg`
- `p95_swing_angle_deg`
- `mean_swing_angle_deg`
- `target_distance_end`
- `target_progress`
- `wind_force_norm`

Do not use `10s` or `15s` features for the first online intervention. They can
be logged later for monitoring, but they should not drive the v0 command scale.

If history is insufficient, output default scale `1.0` or the wind-level scale,
depending on the selected `policy_mode`.

## Risk Model Input

Use the same feature names and units as
`experiments/scripts/build_stage4_risk_dataset.py`. This keeps offline training,
JSON export, and online inference aligned.

Avoid final-outcome leakage. The online model must not use final validity,
full-run summary metrics, future target error, final NaN state, or any feature
that cannot be known at the prediction time.

Do not use method identity or command-scale features for the first model. The
first deployed model should not learn shortcuts from `method`, `policy_mode`,
`adaptation_mode`, `command_scale_expected`, `command_speed_scale`, or
`command_acceleration_scale`.

Use `label_strict_invalid` as the learning target.

## Risk-To-Scale Policy v0

The first policy should start from the existing wind-level candidate and then
apply only conservative risk-conditioned reductions.

Base scale from `policy_mode=wind_level`:

- strong wind -> `0.85`

Risk-conditioned rules:

- If `3s` `risk_score >= 0.5`, keep or set scale to `0.85`.
- If `5s` `risk_score >= 0.5`, reduce scale to `0.75`.
- If `risk_score >= 0.7` after `5s`, reduce scale to `0.65`.
- Clamp scale to `[0.4, 1.0]`.
- Apply a rate limit to scale changes.
- Publish the same value for `speed_scale` and `acceleration_scale` in v0.

This policy is intentionally mild. It is a candidate for repeated validation,
not a final online robustness result.

## Safety Rules

- No-op by default.
- Do not issue a hard stop.
- Do not command thrust or bodyrate.
- Do not modify controller or simulator behavior.
- If the model file is missing or invalid, fall back to `policy_mode=wind_level`.
- If input odometry has NaN or Inf, ignore that input and keep the previous safe
  scale.
- If risk model output is NaN or Inf, ignore it and keep the previous safe
  scale.
- Always clamp published scale to `[0.4, 1.0]`.
- Keep publishing both scale topics while enabled so the planner topic readiness
  gate can be satisfied.

## Model Export Plan

First train `LogisticRegression` offline with the Stage 4 risk predictor
pipeline. Export a simple JSON representation containing:

- model coefficients
- intercept
- feature means
- feature standard deviations
- feature order
- metadata such as label name, horizon, and training command

Avoid pickle for the first implementation if possible. A JSON file is easier to
inspect, version, and reproduce.

Proposed model path:

```bash
experiments/models/stage4_risk_logreg_model.json
```

Generated model files should not be committed unless explicitly approved.

## Implementation Plan

Phase 1:

- Add model export support to `experiments/scripts/train_stage4_risk_predictor.py`.
- Export JSON for `LogisticRegression`.
- Add a protocol note for the model export format and required fields.

Phase 2:

- Add an offline model inference test script.
- Verify that the JSON model reproduces sklearn predictions on the same input
  rows.
- Check missing, NaN, and Inf handling before any ROS integration.

Phase 3:

- Add the risk-conditioned adapter node under `experiments/command_adaptation`.
- Run no-op regression first.
- Run a limited strong-wind Trial 2/3/4/5/6 comparison.

## Evaluation Plan

Baselines:

- `original`
- `fixed_s085`
- `windlevel_s085`
- `risk_conditioned_v0`

Metrics:

- strict valid rate
- NaN rate
- target error
- max swing
- max speed
- command scale trace
- risk score trace

Initial comparison:

- strong wind
- Trial 2/3/4/5/6
- 5 repeats each

Record invalid runs directly. Do not remove, hide, or relabel invalid runs just
because the policy changed command scale.

## What Not To Claim Yet

- Do not claim online robustness improvement before closed-loop evaluation.
- Do not claim RL.
- Do not claim real-world robustness.
- Do not claim a hard safety guarantee.
- Do not hide invalid runs.
- Do not claim `risk_conditioned_v0` is better than `windlevel_s085` until
  repeated comparisons support that conclusion.

## Immediate Next Coding Task

The smallest next coding task is:

- add `LogisticRegression` JSON export to
  `experiments/scripts/train_stage4_risk_predictor.py`
- add a protocol for the model export format
- do not implement the online adapter yet

This keeps Stage 4-H focused on reproducible offline model export before adding
new ROS runtime behavior.
