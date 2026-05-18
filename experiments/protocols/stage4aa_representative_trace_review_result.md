# Stage 4-AA3 Representative Trace Review Result

## Executive Summary

Stage 4-AA3 records the human review of the Stage 4-AA2 representative trace
plots. The review supports the Stage 4-AB paper reframing: keep
`risk_adapter_v1` as the tentative balanced learned / risk-conditioned
protagonist, treat `risk_adapter_v21` as a strong nominal variant / ablation,
and frame `windlevel_s085` and `fixed_s080` as protocol-specialist baselines.

The reviewed traces do not justify an immediate `risk_adapter_v22`. The
observed mechanisms are mixed: Trial 4 stress `risk_adapter_v21` failures
include early pre-arrival command/state failures, while Trial 6 single-goal
`risk_adapter_v21` includes a delayed post-arrival divergence with
`goal_repeat=1`. Lower scale is not automatically safer, and a simple
threshold-tuning variant would not address the observed failure diversity.

Next recommended stage: Stage 4-AC balanced robustness / protocol regret
assets.

Stage 4-AA3 motivates Stage 4-AC balanced robustness assets rather than an
immediate `risk_adapter_v22`: the reviewed traces show mixed mechanisms and do
not support simple threshold tuning as the next algorithmic step.

## Reviewed Trace Set

Single-goal mission protocol (`goal_repeat=1`), Trial 6:

- `single_goal_mission` `windlevel_s085` `trial6` `repeat2`
- `single_goal_mission` `fixed_s080` `trial6` `repeat2`
- `single_goal_mission` `risk_adapter_v1` `trial6` `repeat2`
- `single_goal_mission` `risk_adapter_v1` `trial6` `repeat3`
- `single_goal_mission` `risk_adapter_v21` `trial6` `repeat5`
- `single_goal_mission` `risk_adapter_v21` `trial6` `repeat6`
- `single_goal_mission` `original` `trial6` `repeat1`

Goal-reissue stress protocol (`goal_repeat=10`), Trial 4:

- `goal_reissue_stress` `risk_adapter_v21` `trial4` `repeat2`
- `goal_reissue_stress` `risk_adapter_v21` `trial4` `repeat5`
- `goal_reissue_stress` `risk_adapter_v21` `trial4` `repeat6`
- `goal_reissue_stress` `risk_adapter_v21` `trial4` `repeat8`
- `goal_reissue_stress` `fixed_s080` `trial4` `repeat7`
- `goal_reissue_stress` `risk_adapter_v1` `trial4` `repeat10`

## Single-Goal Trial 6 Observations

`windlevel_s085` success:

- Constant scale `0.85`.
- Fast arrival around `14 s`.
- Speed and swing decay after arrival.
- Target error goes to zero.
- No risk samples because this is heuristic/fixed-style behavior.
- Supports `windlevel_s085` as a strong single-goal specialist.

`fixed_s080` success:

- Clean arrival around `13 s`.
- Moderate speed and swing.
- Stable post-arrival hold.
- Supports `fixed_s080` as a strong conservative baseline.

`risk_adapter_v1`:

- `repeat3` valid: risk rises above threshold, scale drops toward `0.65`, and
  arrival succeeds.
- `repeat2` invalid: similar low-scale behavior, but target error remains near
  the strict-valid threshold and does not reach strict-valid; no NaN occurs.
- Interpretation: conservative risk-conditioned scaling can succeed, but can
  also produce target/no-arrival style failure.

`risk_adapter_v21`:

- `repeat5` valid: scale drops to about `0.70`, and arrival succeeds.
- `repeat6` invalid: arrival occurs first, then delayed divergence / NaN
  appears around `40 s`; `goal_count=1`, so this is not a goal-reissue
  artifact. Risk remains high and scale remains low before failure.
- Interpretation: this is post-arrival delayed divergence or
  hold/reference/state drift, not a failure solved by simply lowering scale.

`original` failure:

- No command scale or risk samples.
- Target error decreases, then state diverges.
- Swing and speed grow sharply near failure.
- Interpretation: the original stack can fail dynamically under strong wind,
  but learned governors do not uniformly eliminate this failure mode.

## Goal-Reissue Stress Trial 4 Observations

`risk_adapter_v21`:

- `repeat2` valid: arrives and remains stable despite `goal_count` increasing
  to `10`.
- `repeat5` invalid: early pre-arrival failure around `9 s`; risk scores are
  largely unavailable (`-1`), and scale remains around `0.80`.
- `repeat6` invalid: early pre-arrival divergence around `9-10 s`;
  `risk_score_3s` spikes, but `risk_score_5s` is not consistently useful;
  scale is mostly `0.80` with brief `0.75` dips.
- `repeat8` invalid: no arrival, failure around `27 s`; `goal_count` rises
  during the run; speed, position error, and swing grow before or near failure.
- Interpretation: Trial 4 stress weakness is not purely post-arrival. It
  includes early pre-arrival command/state failures and possible
  risk-availability / timing issues.

`fixed_s080` and `risk_adapter_v1` successes:

- `fixed_s080` `repeat7`: stable speed, swing, and position behavior with no
  dynamic risk scaling.
- `risk_adapter_v1` `repeat10`: stable trace, mostly simple `0.85` behavior in
  this success case.
- Interpretation: `risk_adapter_v1` and `fixed_s080` avoid some early
  `risk_adapter_v21` failure patterns and support the balanced /
  protocol-specialist framing.

## Mechanism Hypotheses

- Trial 4 stress `risk_adapter_v21` failures include early pre-arrival
  vulnerability.
- `risk_adapter_v21` risk signal availability / timing may be unreliable in
  some stress failures.
- Trial 6 `risk_adapter_v21` invalid behavior includes a post-arrival delayed
  divergence under `goal_repeat=1`, so it is not a goal-reissue artifact.
- Lower scale is not automatically safer.
- Future method changes should not be simple threshold tuning.

## v22 Decision

Do not create `risk_adapter_v22` yet.

If a future method is attempted, it should be generic rather than
trial-specific. Plausible directions are:

- risk-health-aware adaptation
- phase-aware adaptation
- reference / trajectory-health-aware adaptation
- command / state-health-aware adaptation

The next recommended work is Stage 4-AC balanced robustness / protocol regret
assets.

Do not create `risk_adapter_v22` before reviewing the Stage 4-AC balanced
robustness / protocol regret outputs.

## Paper-Framing Implications

- Continue centering `risk_adapter_v1` as the balanced learned /
  risk-conditioned protagonist.
- Treat `risk_adapter_v21` as a strong nominal variant / ablation, not a
  cross-protocol final method.
- Present `windlevel_s085` as the single-goal specialist.
- Present `fixed_s080` as the goal-reissue stress specialist.
- Use representative traces as qualitative mechanism support, not as a
  replacement for protocol-split repeated success-rate comparison.

## What Not To Claim

- Do not claim `risk_adapter_v21` is the overall best method.
- Do not claim learned governors dominate heuristic/static baselines.
- Do not claim lower scale is automatically safer.
- Do not claim Trial 4 stress failures are purely post-arrival.
- Do not claim Trial 6 `risk_adapter_v21` delayed divergence is a
  goal-reissue artifact.
- Do not claim exact physical root cause from representative traces.
- Do not claim statistical significance.
- Do not claim a safety guarantee.
- Do not create a Trial-4-specific `risk_adapter_v22` patch.
