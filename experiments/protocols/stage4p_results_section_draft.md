# Stage 4-P Results Section Draft

## Balanced strong-wind simulation benchmark

We evaluated command-adaptation strategies in the balanced strong-wind simulation benchmark using 30 repeated runs per method across Trials 4–6, with strict-valid rate as the primary paper-facing metric. The original AutoTrans system and the fixed 0.85 command-scaling baseline (fixed_s085) each achieved 18/30 strict-valid runs (60.0%), while the wind-level heuristic adapter (windlevel_s085) achieved 16/30 (53.3%). The learned risk-conditioned adapter (risk_adapter_v1) improved the strict-valid rate to 23/30 (76.7%), outperforming the original system and the two pre-specified non-learned baselines under the same repeated-run protocol.

However, the tuned fixed-scale frontier (fixed_s080) achieved 24/30 strict-valid runs (80.0%), slightly exceeding risk_adapter_v1 by one successful run. Thus, risk_adapter_v1 should not be interpreted as the overall best method once the tuned static frontier is included. Instead, fixed_s080 defines a strong static operating point for this benchmark and provides a concrete reference target for a calibrated risk-conditioned governor, risk_adapter_v2. These results support a bounded repeated-run comparison under the tested strong-wind simulation setting; they do not establish statistical significance, provide a safety guarantee, or imply that all NaN/divergence failures are caused by command adaptation.

Stage 4-T2 indicates that this Results draft should later distinguish the
single-goal mission protocol (`goal_repeat=1`) from the repeated-goal stress
protocol (`goal_repeat=10`). The current 30-repeat Stage 4-J/4-R numbers should
be described as repeated-goal strong-wind protocol results until a separate
single-goal mission comparison is completed.

Stage 4-U adds the first single-goal mission screening result:
`risk_adapter_v2` achieved `9/9` strict-valid under `goal_repeat=1`, while
`fixed_s080` achieved `6/9`. This result is promising but diagnostic-only. A
future Results section should present single-goal mission and repeated-goal
stress protocols as separate benchmarks.

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

## Claims to avoid

- Do not claim risk_adapter_v1 is overall best after including fixed_s080.
- Do not claim statistical significance from the reported counts alone.
- Do not claim a safety guarantee.
- Do not claim final online robustness.
- Do not claim all NaN/divergence failures are caused by command adaptation.
- Do not claim risk_adapter_v1 beats every baseline on every target.
- Do not claim single-goal mission performance from goal_repeat=10 results.
- Do not claim final risk_adapter_v2 superiority from the Stage 4-U 9-run screening alone.
- Do not claim the results generalise to all wind levels, all trajectories, or real-world UAV deployment without further evidence.

## Notes

- This draft supersedes earlier wording that described risk_adapter_v1 as the aggregate best method before fixed_s080 was included.
- This is a Results draft for manuscript development, not a final manuscript section.
