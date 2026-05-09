# Stage 4-H3 Risk-Conditioned Adapter Smoke Results

## Executive Summary

Stage 4-H3 smoke tests show that the risk-conditioned command adapter v0 is
ready for limited repeat evaluation, but not for robustness claims.

The adapter fallback paths passed. With `enable_risk_conditioning=false`, the
no-wind case kept `command_speed_scale=1.0`, and the strong-wind case kept the
expected wind-level fallback scale `command_speed_scale=0.85`.

Risk score logging works. The logged `command_risk_score_3s`,
`command_risk_score_5s`, `command_risk_scale_selected`, and
`command_risk_target_scale_raw` diagnostics are sufficient to inspect whether
the model produced risk early enough and whether the risk-to-scale rule acted.

The episode timing issue was fixed. In the Trial 6 smoke test, the first finite
`3s` and `5s` risk scores appeared at reasonable times after the episode start,
instead of appearing tens of seconds late.

The v0 soft intervention path can activate without breaking the task. Trial 6
triggered the intended `5s` soft scale of `0.75` and still remained valid.
However, performance improvement is not proven yet.

## Smoke Test Table

| Test | Configuration | Wind / target | Validity | Key diagnostics | Conclusion |
| --- | --- | --- | --- | --- | --- |
| no-risk / no-wind smoke | `enable_risk_conditioning=false` | `wind_force_norm=0.0` | `valid_run_suggested=true`, `has_nan_state=false` | `command_speed_scale` stayed `1.0` | no-wind fallback passed |
| no-risk / strong-wind smoke | `enable_risk_conditioning=false` | `wind_force_norm=0.0075` | `valid_run_suggested=true`, `has_nan_state=false` | `command_speed_scale` stayed `0.85` | strong-wind wind-level fallback passed |
| risk-conditioning / strong Trial 5 smoke | `enable_risk_conditioning=true` | trial5 target `(3.5, 0.8)` | `valid_run_suggested=false`, `has_nan_state=false`; final target error near zero | `max_swing_angle_deg=101.658897`, `max_payload_speed=5.189568`, `min_command_speed_scale` approximately `0.750006` | risk adapter was active, but policy did not prevent safety invalid |
| risk-conditioning / strong Trial 4 smoke | `enable_risk_conditioning=true` | trial4 target `(-3.5, -1.2)` | `valid_run_suggested=true`, `has_nan_state=false` | `max_swing_angle_deg=14.871981`, `max_payload_speed=2.496655`, `max_command_risk_score_3s=0.214530`, `max_command_risk_score_5s=0.120600`, `command_speed_scale` stayed `0.85` | low-risk valid run, no false intervention |
| risk-conditioning / strong Trial 6 smoke | `enable_risk_conditioning=true` | trial6 target `(0.0, 1.5)` | `valid_run_suggested=true`, `has_nan_state=false` | `max_swing_angle_deg=13.645845`, `max_payload_speed=2.511246`, `final_uav_xy_error=0.006180`, `first_finite_command_risk_score_3s_time=7.649958`, `first_finite_command_risk_score_5s_time=9.650004`, `first_command_risk_score_3s_ge_0p5_time=7.649958`, `first_command_risk_score_5s_ge_0p5_time=9.650004`, `first_command_scale_below_0p85_time=9.650004`, `min_command_speed_scale=0.750000`, `min_command_risk_target_scale_raw=0.750000` | episode timing fixed; `5s` risk triggered soft scale `0.75`; run stayed valid |

## Interpretation

The adapter is safe enough for limited repeat evaluation because both fallback
paths passed, risk diagnostics are logged, and the soft scale path can activate
without immediately breaking a valid task.

The Trial 5 invalid smoke is important negative evidence. It shows that v0 is
not yet a reliable safety solution: the adapter was active and reduced scale to
about `0.75`, but the run still became safety-invalid due to large swing and
payload speed.

The Trial 6 smoke shows the intended soft intervention path working. The `3s`
and `5s` risk scores appeared at reasonable times, the `5s` score triggered the
soft scale `0.75`, and the run stayed valid.

## Current Research Decision

Proceed to limited repeat evaluation.

Do not claim robustness improvement yet. The smoke tests only verify fallback
behavior, logging, timing, and a first online intervention path.

Compare `risk_adapter_v0` against `windlevel_s085` using the same targets and
the same repeat structure.

## Next Step

Run `risk_adapter_v0` on Trial 5 and Trial 6 with 5 repeats each.

Use `label_strict_invalid` for evaluation so safety-invalid runs remain visible
even when target error is small.

Compare the repeat results with `windlevel_s085` historical results.

## What Not To Claim

- Do not claim safety guarantee.
- Do not claim online robustness yet.
- Do not hide the failed Trial 5 smoke.
