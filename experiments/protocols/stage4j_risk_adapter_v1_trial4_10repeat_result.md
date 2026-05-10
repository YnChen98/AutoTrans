# Stage 4-J Risk Adapter v1 Trial 4 10-Repeat Result

## Executive Summary

`risk_adapter_v1` Trial 4 was expanded from 5 repeats to 10 repeats.

The expanded result is `7/10` valid. This is below the intended `>=8/10`
continuation gate.

`risk_adapter_v1` remains better than `windlevel_s085` on Trial 4, but Trial 4
is still a weak target for the current policy. The invalid repeats were
repeat5, repeat7, and repeat9.

Do not continue Trial 5 or Trial 6 expansion before documenting and
interpreting this Trial 4 result.

## Result Table

| Repeat | `valid_run_suggested` | `has_nan_state` | `first_nan_time` | `max_swing_angle_deg` | `max_payload_speed` | `final_uav_xy_error` | Risk trigger summary | `min_command_speed_scale` | Interpretation |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- | ---: | --- |
| repeat1 | `true` | `false` | `nan` | `17.998654` | `2.499334` | `0.000000` | no risk trigger | `0.850000` | valid low-risk run |
| repeat2 | `true` | `false` | `nan` | `13.779706` | `2.610758` | `0.029931` | no risk trigger | `0.850000` | valid low-risk run |
| repeat3 | `true` | `false` | `nan` | `16.645079` | `2.771085` | `0.071210` | no risk trigger | `0.850000` | valid low-risk run |
| repeat4 | `true` | `false` | `nan` | `18.741379` | `2.513542` | `0.000000` | no risk trigger | `0.850000` | valid low-risk run |
| repeat5 | `false` | `true` | `24.900021` | `134.956542` | `32.810948` | `157.854930` | `3s>=0.5` at `27.599985`; `5s>=0.5` at `29.599997` | `n/a` | late risk detection failure |
| repeat6 | `true` | `false` | `nan` | `21.259881` | `2.471526` | `0.233796` | no risk trigger | `0.850000` | valid low-risk run |
| repeat7 | `false` | `false` | `nan` | `17.555989` | `2.650889` | `0.711352` | no risk trigger | `0.850000` | target-error failure without safety violation |
| repeat8 | `true` | `false` | `nan` | `12.898343` | `2.512373` | `0.000000` | no risk trigger | `0.850000` | valid low-risk run |
| repeat9 | `false` | `true` | `14.649950` | `61.709278` | `31.964786` | `105.941102` | `3s>=0.5` at `22.399925` | `n/a` | late risk detection failure |
| repeat10 | `true` | `false` | `nan` | `11.898677` | `2.492978` | `0.078049` | no risk trigger | `0.850000` | valid low-risk run |

Additional failure timing details:

| Repeat | `first_swing_angle_ge_30_time` | `first_payload_speed_ge_4_time` | `first_command_risk_score_3s_ge_0p5_time` | `first_command_risk_score_5s_ge_0p5_time` |
| --- | ---: | ---: | ---: | ---: |
| repeat5 | `25.150046` | `25.200054` | `27.599985` | `29.599997` |
| repeat9 | `14.949983` | `14.900088` | `22.399925` | `nan` |

## Failure Analysis

repeat5 and repeat9 are late risk detection failures. In repeat5, the NaN
appeared at `first_nan_time=24.900021`, before the `3s` risk threshold at
`27.599985` and the `5s` risk threshold at `29.599997`. In repeat9, the NaN
appeared at `first_nan_time=14.649950`, while the first `3s` risk threshold
crossing did not occur until `22.399925`.

repeat7 is a target-error failure without a safety violation. It had
`has_nan_state=false`, `max_swing_angle_deg=17.555989`,
`max_payload_speed=2.650889`, and `final_uav_xy_error=0.711352`. No risk
trigger occurred, which is consistent with the absence of swing or speed
safety violation.

The valid repeats show that `risk_adapter_v1` does not falsely intervene on
low-risk valid runs. repeats 1, 2, 3, 4, 6, 8, and 10 had no risk trigger and
kept `min_command_speed_scale=0.850000`.

## Comparison With Existing Trial 4 Baselines

| Method | Trial 4 result | Notes |
| --- | ---: | --- |
| `original` | `4/5` valid | Historical 5-repeat baseline. |
| `fixed_s085` | `5/5` valid | Historical 5-repeat baseline and best existing Trial 4 result. |
| `windlevel_s085` | `1/5` valid | Historical 5-repeat baseline. |
| `risk_adapter_v1` | `7/10` valid | Expanded 10-repeat result; invalid repeats were repeat5, repeat7, and repeat9. |

The 10-repeat `risk_adapter_v1` result is not directly statistically
comparable to the 5-repeat baselines. It does show that Trial 4 remains a weak
target for the current policy and that the earlier `4/5` result was not enough
evidence to proceed as if Trial 4 were stable.

## Research Decision

Do not claim `risk_adapter_v1` is stable on Trial 4.

Do not proceed directly to broad expansion. The `7/10` result missed the
intended `>=8/10` continuation gate and includes two late risk detection
failures plus one target-error failure.

The next step should be either fair 10-repeat baseline expansion on Trial 4 or
`risk_adapter_v2` design targeting false-negative risk detection.

## What Not To Claim

- Do not claim statistical significance.
- Do not claim a safety guarantee.
- Do not claim `risk_adapter_v1` beats `fixed_s085` on Trial 4.
- Do not hide the repeat5, repeat7, or repeat9 failures.
