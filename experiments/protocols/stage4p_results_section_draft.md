# Stage 4-P Results Section Draft

## Balanced strong-wind simulation benchmark

We evaluated command-adaptation strategies in the balanced strong-wind simulation benchmark using 30 repeated runs per method across Trials 4–6, with strict-valid rate as the primary paper-facing metric. The original AutoTrans system and the fixed 0.85 command-scaling baseline (fixed_s085) each achieved 18/30 strict-valid runs (60.0%), while the wind-level heuristic adapter (windlevel_s085) achieved 16/30 (53.3%). The learned risk-conditioned adapter (risk_adapter_v1) improved the strict-valid rate to 23/30 (76.7%), outperforming the original system and the two pre-specified non-learned baselines under the same repeated-run protocol.

However, the tuned fixed-scale frontier (fixed_s080) achieved 24/30 strict-valid runs (80.0%), slightly exceeding risk_adapter_v1 by one successful run. Thus, risk_adapter_v1 should not be interpreted as the overall best method once the tuned static frontier is included. Instead, fixed_s080 defines a strong static operating point for this benchmark and provides a concrete reference target for a calibrated risk-conditioned governor, risk_adapter_v2. These results support a bounded repeated-run comparison under the tested strong-wind simulation setting; they do not establish statistical significance, provide a safety guarantee, or imply that all NaN/divergence failures are caused by command adaptation.

Stage 4-T2 indicates that this Results draft should later distinguish the
single-goal mission protocol (`goal_repeat=1`) from the repeated-goal stress
protocol (`goal_repeat=10`). The current 30-repeat Stage 4-J/4-R numbers should
be described as repeated-goal strong-wind protocol results and kept separate
from the Stage 4-U2 single-goal mission comparison.

Stage 4-U adds the first single-goal mission screening result:
`risk_adapter_v2` achieved `9/9` strict-valid under `goal_repeat=1`, while
`fixed_s080` achieved `6/9`. This result is promising but diagnostic-only. A
future Results section should present single-goal mission and repeated-goal
stress protocols as separate benchmarks.

Stage 4-U2 supersedes that 9-run screen with a 10-repeat single-goal mission
comparison: `fixed_s080` achieved `21/30` and `risk_adapter_v2` achieved
`21/30` under `goal_repeat=1`. Future Results should distinguish this
single-goal mission result from repeated-goal stress results such as
`fixed_s080` `24/30` and `risk_adapter_v1` `23/30` under `goal_repeat=10`.

Stage 4-V4 provides protocol-labeled `risk_adapter_v21` evidence under the
single-goal mission protocol. Stage 4-X1 adds the corrected
`risk_adapter_v21` goal-reissue stress result after fixing the duplicate CSV
issue in Trial 4 repeat2-5. Future Results should report:

| Protocol | Method | Strict-valid count |
| --- | --- | ---: |
| single-goal mission, `goal_repeat=1` | `fixed_s080` | `21/30` |
| single-goal mission, `goal_repeat=1` | `risk_adapter_v2` | `21/30` |
| single-goal mission, `goal_repeat=1` | `risk_adapter_v21` | `25/30` |
| goal-reissue stress, `goal_repeat=10` | `fixed_s080` | `24/30` |
| goal-reissue stress, `goal_repeat=10` | `risk_adapter_v1` | `23/30` |
| goal-reissue stress, `goal_repeat=10` | `risk_adapter_v21` | `20/30` |
| goal-reissue stress, `goal_repeat=10` | `original` | `18/30` |
| goal-reissue stress, `goal_repeat=10` | `fixed_s085` | `18/30` |
| goal-reissue stress, `goal_repeat=10` | `windlevel_s085` | `16/30` |

Older wording that treated `risk_adapter_v2.1` as unevaluated is superseded.
The Results narrative should describe `risk_adapter_v21` as the current
strongest method among the currently evaluated single-goal methods, while
stating that `fixed_s080` remains the strongest evaluated goal-reissue stress
method. `risk_adapter_v21` should not be described as a cross-protocol final
winner.

## Chinese logic explanation

这段 Results 的核心逻辑是先固定评价协议和主指标：balanced strong-wind simulation benchmark、Trials 4–6、每个方法 30 次重复运行，以及 strict-valid rate。随后按 baseline 到 adapter 的顺序报告结果，说明 risk_adapter_v1 相比 original、fixed_s085 和 windlevel_s085 有更高的 strict-valid rate。最后加入 Stage 4-R 的更新解释：fixed_s080 作为 tuned fixed-scale frontier 达到 24/30，略高于 risk_adapter_v1 的 23/30，因此 risk_adapter_v1 不能再被写成 overall best。更稳妥的论文表述是：fixed_s080 提供了一个强静态参考点，并推动下一步 risk_adapter_v2 设计成为 calibrated risk-conditioned governor。

## Safe claims

- risk_adapter_v1 achieved 23/30 strict-valid runs (76.7%) in the balanced strong-wind simulation benchmark.
- fixed_s080 achieved 24/30 strict-valid runs (80.0%) on the same balanced Trials 4–6 setting.
- risk_adapter_v1 outperformed original, fixed_s085, and windlevel_s085 under the repeated-run protocol.
- fixed_s080 slightly exceeded risk_adapter_v1 by one strict-valid run.
- fixed_s080 can be described as a strong static operating point or tuned fixed-scale frontier for this benchmark.
- fixed_s080 provides a concrete reference target for risk_adapter_v2.
- The benchmark supports a bounded repeated-run comparison under the tested strong-wind simulation setting.
- Current Stage 4-J/4-R results are repeated-goal protocol results and should be labeled separately from future single-goal mission results.
- Stage 4-U provides diagnostic single-goal screening evidence: `risk_adapter_v2` `9/9` and `fixed_s080` `6/9` under `goal_repeat=1`.
- Stage 4-U2 provides the `fixed_s080` and `risk_adapter_v2` single-goal 10-repeat baseline comparison: `risk_adapter_v2` `21/30` and `fixed_s080` `21/30` under `goal_repeat=1`.
- Stage 4-V4 provides the current strongest evaluated single-goal result:
  `risk_adapter_v21` `25/30` under `goal_repeat=1`.
- Stage 4-X1 provides the corrected `risk_adapter_v21` goal-reissue stress
  result: `20/30` under `goal_repeat=10`.
- Future Results should separate single-goal mission results (`fixed_s080`
  `21/30`, `risk_adapter_v2` `21/30`, `risk_adapter_v21` `25/30`) from
  goal-reissue stress results (`fixed_s080` `24/30`, `risk_adapter_v1`
  `23/30`, `risk_adapter_v21` `20/30`, `original` `18/30`, `fixed_s085`
  `18/30`, `windlevel_s085` `16/30`).
- `risk_adapter_v21` can be described as the current strongest method among
  the evaluated single-goal methods.
- `fixed_s080` remains the strongest evaluated goal-reissue stress method.

## Claims to avoid

- Do not claim risk_adapter_v1 is overall best after including fixed_s080.
- Do not claim statistical significance from the reported counts alone.
- Do not claim a safety guarantee.
- Do not claim final online robustness.
- Do not claim all NaN/divergence failures are caused by command adaptation.
- Do not claim risk_adapter_v1 beats every baseline on every target.
- Do not claim single-goal mission performance from goal_repeat=10 results.
- Do not claim final risk_adapter_v2 superiority from the Stage 4-U 9-run screening alone.
- Do not claim risk_adapter_v2 dominates fixed_s080 after Stage 4-U2; they match in aggregate under the single-goal protocol.
- Do not claim statistical significance or a safety guarantee for `risk_adapter_v21`.
- Do not claim `risk_adapter_v21` solves Trial 6; it achieved `6/10` on Trial 6 while `fixed_s080` achieved `8/10`.
- Do not claim `risk_adapter_v21` is best under goal-reissue stress; it
  achieved `20/30`, below `fixed_s080` `24/30` and `risk_adapter_v1` `23/30`.
- Do not claim `risk_adapter_v21` is a cross-protocol final winner.
- Do not claim all goal-reissue stress failures are post-arrival failures.
- Do not mix single-goal mission and goal-reissue stress results into one table without protocol labels.
- Do not claim the results generalise to all wind levels, all trajectories, or real-world UAV deployment without further evidence.

## Notes

- This draft supersedes earlier wording that described risk_adapter_v1 as the aggregate best method before fixed_s080 was included.
- Stage 4-V4 supersedes older wording that treated `risk_adapter_v2.1` as a design-only method without evaluation.
- Stage 4-X1 supersedes any uncorrected `risk_adapter_v21` goal-reissue stress
  result affected by the duplicate CSV issue.
- This is a Results draft for manuscript development, not a final manuscript section.
