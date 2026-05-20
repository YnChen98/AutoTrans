# AutoTrans Baseline Trial Runner

`experiments/scripts/run_baseline_trial.sh` 是一个轻量的 terminal-based baseline runner，用于在已经验证过手动 RViz demo 后，重复执行标准 baseline trial。

它不会修改 planner、controller 或 simulator 核心逻辑。它只是：

1. 启动 `roslaunch payload_planner simple_run.launch`。
2. 等待关键 ROS topics 出现。
3. 启动 `roslaunch autotrans_logger state_logger.launch`。
4. 用 `rostopic pub -1 /move_base_simple/goal` 发布一个 `geometry_msgs/PoseStamped` goal。
5. 等待指定时长。
6. 停止 logger 和 demo。
7. 运行 `experiments/autotrans_logger/scripts/analyze_log.py`。

## 为什么它能替代手动 RViz 2D Nav Goal

手动流程中，RViz 的 `2D Nav Goal` 会向 `/move_base_simple/goal` 发布 `geometry_msgs/PoseStamped`。

这个脚本做同一件事，只是通过 terminal 执行：

```bash
rostopic pub -1 /move_base_simple/goal geometry_msgs/PoseStamped ...
```

因此它适合重复 baseline trials，减少人工点击误差。

脚本现在尽量贴近 RViz `2D Nav Goal` 行为：

- 使用 `frame_id: world`，对应 `planner/plan_manage/launch/sim_vis.rviz` 中的 RViz Fixed Frame。
- 默认 `--z 0.0`，对应 RViz 2D 平面 goal 的行为。
- 使用 `stamp: now`，而不是固定的 zero timestamp。
- 在发布 goal 前等待 `/visual_slam/odom`、`/payload_odom`、`/pcl_render_node/cloud`、`/so3cmd` 和 `/move_base_simple/goal` subscriber。
- 默认重复发布 goal `3` 次，每次间隔 `1.0 s`，降低一次性命令丢失或早发的风险。

注意：`payload_planner_node` 的 `ReplanFSM::waypointCallback` 只使用 goal 的 `x/y`，目标高度会被内部设置为 `fsm/waypoint0_z`。但是为了和 RViz 2D Nav Goal 保持一致，脚本仍默认发布 `z=0.0`。

## 为什么旧的 --z 1.0 trial 是 invalid

旧命令使用了 `--z 1.0`，且脚本在关键状态刚出现后立即发布 goal。虽然 planner 最终会覆盖目标高度，但这条自动消息与 RViz 2D Nav Goal 不完全一致，并且缺少保守的 odometry/map/controller readiness wait。

invalid run 的表现是 UAV/payload 状态严重发散，说明这次自动 trial 不能作为 baseline。修正后的脚本把 goal message 和发布时机改得更接近手动 RViz 流程。

## Trial 1 示例命令

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
bash experiments/scripts/run_baseline_trial.sh --name trial1 --x 0.0 --y -1.2 --z 0.0 --duration 75
```

## Trial 3 示例命令

如果目标点是 `(8.0, 1.5)`，必须显式写成 `--x 8.0 --y 1.5`，不要留下单独的 positional argument：

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
bash experiments/scripts/run_baseline_trial.sh --name trial3 --x 8.0 --y 1.5 --z 0.0 --duration 75
```

脚本会拒绝未知 option 或 positional argument。例如下面的命令会在启动 ROS 前失败：

```bash
bash experiments/scripts/run_baseline_trial.sh 8.0
```

可用参数见：

```bash
bash experiments/scripts/run_baseline_trial.sh --help
```

默认参数：

- `--name baseline_trial`
- `--x 0.0`
- `--y -1.2`
- `--z 0.0`
- `--duration 75`
- `--frame_id world`
- `--startup_wait 20`
- `--goal_repeat 3`
- `--goal_interval 1.0`

## Stage 2-B drag-wind 配置 helper

`experiments/scripts/set_drag_wind_config.py` 用于切换 Stage 2-B frozen drag-wind benchmark levels。它只修改：

```bash
uav_simulator/uav_simulator/config/so3_quadrotor.yaml
```

完整实验流程、validity criteria 和 repeat policy 见 `experiments/protocols/stage2b_drag_wind_experiment_protocol.md`。当前 frozen conclusion 和 evidence summary 见 `experiments/protocols/stage2b_drag_wind_results_summary.md`。

查看当前 wind config：

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/set_drag_wind_config.py --show
```

先预览 `strong` level，不写入文件：

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/set_drag_wind_config.py --level strong --dry-run
```

设置 no wind：

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/set_drag_wind_config.py --level none
```

设置 weak / moderate / strong wind：

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/set_drag_wind_config.py --level weak
python3 experiments/scripts/set_drag_wind_config.py --level moderate
python3 experiments/scripts/set_drag_wind_config.py --level strong
```

`boundary` 是 stress level，只在明确需要边界压力测试时使用：

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/set_drag_wind_config.py --level boundary
```

Stage 2-B frozen levels:

| Level | enable_wind | wind_velocity_x | wind_drag_linear | wind_max_force |
| --- | --- | ---: | ---: | ---: |
| none | false | 0.0 | 0.0 | 0.0 |
| weak | true | 0.5 | 0.004 | 0.002 |
| moderate | true | 0.5 | 0.010 | 0.005 |
| strong | true | 0.5 | 0.015 | 0.0075 |
| boundary | true | 0.5 | 0.020 | 0.010 |

运行 `wind_signal_publisher` 时，把 annotation `/wind_force` 的 cap 设置成同一个 level 的 `wind_max_force`。例如 weak / moderate / strong：

```bash
roslaunch autotrans_logger wind_signal_publisher.launch enable_wind:=true wind_mode:=constant wind_force_x:=0.002 wind_max_force:=0.002
roslaunch autotrans_logger wind_signal_publisher.launch enable_wind:=true wind_mode:=constant wind_force_x:=0.005 wind_max_force:=0.005
roslaunch autotrans_logger wind_signal_publisher.launch enable_wind:=true wind_mode:=constant wind_force_x:=0.0075 wind_max_force:=0.0075
```

运行 baseline trial：

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
bash experiments/scripts/run_baseline_trial.sh --name stage2b_weak_trial1 --x 0.0 --y -1.2 --z 0.0 --duration 75
```

每次 wind run 结束后恢复 no wind，避免下一次实验继承旧配置：

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/set_drag_wind_config.py --level none
```

## Stage 3-B heuristic command adapter

`experiments/command_adaptation` 提供第一个 heuristic runtime command adapter。它发布：

- `/command_adaptation/speed_scale`
- `/command_adaptation/acceleration_scale`

构建后启动：

```bash
roslaunch command_adaptation heuristic_command_adapter.launch
```

使用它时，planner 应设置为 topic mode，并启用 topic readiness gate：

- `manager/enable_command_adaptation=true`
- `manager/adaptation_mode=topic`
- `manager/require_adaptation_topic_ready=true`

详细流程见 `experiments/command_adaptation/README.md` 和 `experiments/protocols/stage3b_heuristic_command_adapter_protocol.md`。

## Stage 4-A risk dataset builder

`experiments/scripts/build_stage4_risk_dataset.py` 从 manifest 中列出的 AutoTrans CSV logs 构建 failure-risk prediction dataset。初始 manifest 是：

```bash
experiments/protocols/stage4_risk_manifest.json
```

先 dry-run 检查 planned rows 和 aggregate labels：

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/build_stage4_risk_dataset.py --manifest experiments/protocols/stage4_risk_manifest.json --output experiments/datasets/stage4_risk_dataset.csv --dry-run --print-summary
```

builder 会同时输出 legacy `label_invalid` 和推荐用于后续 risk prediction 的 `label_strict_invalid`。`label_strict_invalid` 会合并 target/speed/swing failure 和 manifest 中的 `manual_invalid=true`，因此碰撞观察但 `valid_run_suggested=true` 的 run 应在 manifest 中手工标为 `manual_invalid=true`。中断短日志应不加入 manifest，或用 `exclude_from_training=true` 标注；默认生成 dataset 时这些 excluded rows 不会写入 CSV，只有加 `--include-excluded` 才会写入。

完整 schema、labels 和 early-window features 见 `experiments/protocols/stage4_risk_dataset_protocol.md`。生成的 `experiments/datasets/*.csv` 不应提交到 git。

## Stage 4-B risk predictor baseline

`experiments/scripts/train_stage4_risk_predictor.py` 用于在 Stage 4-A dataset 上训练和评估 failure-risk prediction baseline。当前 dataset 很小，这一步只建立 learning/evaluation pipeline，不应声明最终性能。

默认 `--label label_invalid` 保持 legacy analyzer validity 行为，便于和早期结果兼容。安全阈值相关的 risk prediction 推荐显式使用 `--label label_strict_invalid`；它由 dataset builder 合并 target、speed、swing、NaN/log-health 和 `manual_invalid=true` 条件，适合 Trial 5 这类 `valid_run_suggested=true` 但安全阈值或人工观察判定失败的 run。

先用 dry-run 检查 `basic` feature set：

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/train_stage4_risk_predictor.py --dataset experiments/datasets/stage4_risk_dataset.csv --feature-set basic --dry-run --print-summary
```

检查 `early` feature set：

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/train_stage4_risk_predictor.py --dataset experiments/datasets/stage4_risk_dataset.csv --feature-set early --dry-run --print-summary
```

显式运行 LOO CV 的 `early` feature set：

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/train_stage4_risk_predictor.py --dataset experiments/datasets/stage4_risk_dataset.csv --feature-set early --cv loo --dry-run --print-summary
```

按 target group 做 `leave-one-target-out`：

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/train_stage4_risk_predictor.py --dataset experiments/datasets/stage4_risk_dataset.csv --feature-set early --cv leave-one-target-out --dry-run --print-summary
```

用推荐的 strict-invalid label 做 safety-aware dry-run：

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/train_stage4_risk_predictor.py --dataset experiments/datasets/stage4_risk_dataset.csv --label label_strict_invalid --feature-set early --cv leave-one-target-out --drop-command-scale-features --drop-method-features --dry-run --print-summary
```

做 prediction-horizon ablation，检查在线 risk-conditioned command adaptation 需要的早期窗口：

3s-only `leave-one-target-out`：

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/train_stage4_risk_predictor.py --dataset experiments/datasets/stage4_risk_dataset.csv --label label_strict_invalid --feature-set early --cv leave-one-target-out --drop-command-scale-features --drop-method-features --max-early-window 3 --dry-run --print-summary
```

5s-window `leave-one-target-out`：

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/train_stage4_risk_predictor.py --dataset experiments/datasets/stage4_risk_dataset.csv --label label_strict_invalid --feature-set early --cv leave-one-target-out --drop-command-scale-features --drop-method-features --max-early-window 5 --dry-run --print-summary
```

all-window `leave-one-target-out`：

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/train_stage4_risk_predictor.py --dataset experiments/datasets/stage4_risk_dataset.csv --label label_strict_invalid --feature-set early --cv leave-one-target-out --drop-command-scale-features --drop-method-features --max-early-window 15 --dry-run --print-summary
```

运行 Stage 4-F calibration、threshold sweep 和 group diagnostics：

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/train_stage4_risk_predictor.py --dataset experiments/datasets/stage4_risk_dataset.csv --label label_strict_invalid --feature-set early --cv leave-one-target-out --drop-command-scale-features --drop-method-features --threshold-sweep --group-metrics --dry-run --print-summary
```

新增 diagnostics：

- `--max-early-window 3|5|10|15` 控制 `early_*` feature 的最大 prediction horizon。默认 `15` 保持旧命令行为；`3` 和 `5` 更适合检查在线 adapter 是否能足够早地得到 risk signal，`10` 和 `15` 可能对快速失败模式太晚。
- `--calibration-bins 10` 控制 ECE/calibration bins 的 equal-width bin 数量，默认是 `10`。
- `--threshold-sweep` 会检查 thresholds `0.1` 到 `0.9`，输出 precision、recall、F1、false positives 和 false negatives。
- `--group-metrics` 会按当前 `--cv` 的 held-out group 输出 per-target 或 per-method metrics。
- `--positive-label-name failure` 用于给 positive class 一个 human-readable 名称，默认是 `failure`。

非 `--dry-run` 时，脚本继续写入 `metrics_summary.json`、`predictions.csv` 和
`feature_summary.csv`，并额外写入 `calibration_bins.csv`。启用对应 diagnostics
时，还会写入 `threshold_sweep.csv` 和 `group_metrics.csv`。这些文件位于
`experiments/results/` 下，不应提交到 git。

测试去掉 command-scale 相关特征后的 `early` feature set：

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/train_stage4_risk_predictor.py --dataset experiments/datasets/stage4_risk_dataset.csv --feature-set early --drop-command-scale-features --dry-run --print-summary
```

测试去掉 method/adaptation/policy identity 特征后的 `early` feature set：

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/train_stage4_risk_predictor.py --dataset experiments/datasets/stage4_risk_dataset.csv --feature-set early --drop-method-features --dry-run --print-summary
```

完整 protocol 见 `experiments/protocols/stage4_risk_prediction_protocol.md`。生成的 `experiments/results/` 不应提交到 git。

## Stage 4-H1 LogisticRegression JSON export

Stage 4-H1 只做离线 `LogisticRegression` model export，不实现在线 ROS adapter。推荐先在
`~/venvs/autotrans-stage4` 中运行，并使用 `label_strict_invalid`、`feature-set early`、
`--drop-command-scale-features` 和 `--drop-method-features`。

3s early soft-warning candidate:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
source ~/venvs/autotrans-stage4/bin/activate
python3 experiments/scripts/train_stage4_risk_predictor.py --dataset experiments/datasets/stage4_risk_dataset.csv --label label_strict_invalid --feature-set early --max-early-window 3 --drop-command-scale-features --drop-method-features --export-logreg-json experiments/models/stage4_risk_logreg_3s.json --export-train-on-all --print-summary
```

5s early soft-warning candidate:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
source ~/venvs/autotrans-stage4/bin/activate
python3 experiments/scripts/train_stage4_risk_predictor.py --dataset experiments/datasets/stage4_risk_dataset.csv --label label_strict_invalid --feature-set early --max-early-window 5 --drop-command-scale-features --drop-method-features --export-logreg-json experiments/models/stage4_risk_logreg_5s.json --export-train-on-all --print-summary
```

15s offline/high-confidence monitoring candidate:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
source ~/venvs/autotrans-stage4/bin/activate
python3 experiments/scripts/train_stage4_risk_predictor.py --dataset experiments/datasets/stage4_risk_dataset.csv --label label_strict_invalid --feature-set early --max-early-window 15 --drop-command-scale-features --drop-method-features --export-logreg-json experiments/models/stage4_risk_logreg_15s.json --export-train-on-all --print-summary
```

`--export-logreg-json` 必须和 `--export-train-on-all` 一起使用，避免无意中把 cross-validation fold model 当成 deployable model。生成的 `experiments/models/*.json`、`experiments/models/*.pkl` 和 `experiments/models/*.joblib` 默认不应提交。完整 export protocol 见 `experiments/protocols/stage4_risk_model_export_protocol.md`。

## Stage 4-H2 LogisticRegression strict JSON-vs-sklearn verification

`experiments/scripts/verify_stage4_logreg_json.py` 用于在不依赖 `sklearn` 的情况下，检查导出的
`LogisticRegression` JSON 能否在 dataset rows 上完成一致的 feature reconstruction、median
imputation、`StandardScaler` transform 和 probability inference。新的
`--export-logreg-json --export-train-on-all` export 会写入 `reference_predictions`，
其中每一行包含 `row_index`、可用时的 `run_id`、`label` 和
`sklearn_probability_positive`，这些概率来自同一个被导出的 sklearn
`LogisticRegression` model。

3s JSON checker:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/verify_stage4_logreg_json.py --dataset experiments/datasets/stage4_risk_dataset.csv --model-json experiments/models/stage4_risk_logreg_3s.json --print-summary
```

5s JSON checker:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/verify_stage4_logreg_json.py --dataset experiments/datasets/stage4_risk_dataset.csv --model-json experiments/models/stage4_risk_logreg_5s.json --print-summary
```

15s JSON checker:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/verify_stage4_logreg_json.py --dataset experiments/datasets/stage4_risk_dataset.csv --model-json experiments/models/stage4_risk_logreg_15s.json --print-summary
```

如果 JSON 包含 `reference_predictions`，checker 会按 `row_index` 匹配 dataset rows，
用默认 `--max-abs-diff-tol 1e-8` 比较 JSON-only probabilities 和
`sklearn_probability_positive`，并输出 `reference_probability_check: passed`、
`max_abs_diff`、`mean_abs_diff` 和 `rows_compared`。旧 JSON 没有
`reference_predictions` 时仍可兼容检查，但会明确输出
`reference_probability_check: not_available` 和
`json_inference_check: passed_without_sklearn_reference`。在线 ROS adapter
implementation 必须等 strict JSON-vs-sklearn reference probability verification 通过后再开始。

## Stage 4-I adapter result table generator

`experiments/scripts/summarize_stage4h_adapter_results.py` 从 committed manifest 生成 Stage 4-H
`risk_adapter_v1` limited evaluation 的 Markdown/CSV summary table。Interpretation 会从
manifest 动态计算 per-trial best、aggregate best 和 repeat-count caveat，避免旧结果硬编码。
它只做离线表格整理，不运行 ROS、simulation、RViz 或 `catkin_make`。

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/summarize_stage4h_adapter_results.py \
  --manifest experiments/protocols/stage4h_adapter_limited_eval_manifest.json \
  --output-md experiments/results/stage4h_adapter_limited_eval_summary.md \
  --output-csv experiments/results/stage4h_adapter_limited_eval_summary.csv \
  --print-summary
```

生成的 `experiments/results/stage4h_adapter_limited_eval_summary.md` 和
`experiments/results/stage4h_adapter_limited_eval_summary.csv` 不应提交。完整 protocol 见
`experiments/protocols/stage4h_adapter_result_table_protocol.md`。

Stage 4-J Trial 6 10-repeat fair comparison is complete and documented in
`experiments/protocols/stage4j_trial6_10repeat_fair_comparison.md`. Using
strict-valid / `label_strict_invalid`, Trial 6 results are `original=3/10`,
`fixed_s085=4/10`, `windlevel_s085=6/10`, and `risk_adapter_v1=7/10`. With
Trial 4/5/6 all at 10 repeats for the main four methods, the balanced
aggregate is `original=18/30`, `fixed_s085=18/30`, `windlevel_s085=16/30`,
and `risk_adapter_v1=23/30`. Do not mix diagnostic smoke runs into this main
repeat comparison.

The Stage 4-J balanced 30-repeat aggregate result is documented in
`experiments/protocols/stage4j_balanced_30repeat_aggregate_result.md`.
`risk_adapter_v1` is the best aggregate method among the original four methods
at `23/30`; `original` and `fixed_s085` are tied at `18/30`, and
`windlevel_s085` is `16/30`. Stage 4-R now supplements this with the tuned
`fixed_s080` static frontier at `24/30`, so paper-facing assets must include
`fixed_s080` or avoid claiming `risk_adapter_v1` is best overall. This remains
simulation-only limited-repeat evidence and does not support
statistical-significance or safety-guarantee claims.

## Stage 4-P balanced paper assets

`experiments/scripts/generate_stage4_balanced_paper_assets.py` generates
paper-ready CSV/Markdown tables and an aggregate success-rate PNG for the
Stage 4-J balanced Trial 4/5/6 comparison. It uses strict-valid /
`label_strict_invalid`, excludes diagnostic smoke runs, writes generated
outputs under ignored `experiments/results/stage4_balanced_paper_assets/`, and
describes divergence-inspector outputs as run-level diagnostic labels because
some labels correspond to valid or warning-only runs.

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/generate_stage4_balanced_paper_assets.py \
  --manifest experiments/protocols/stage4h_adapter_limited_eval_manifest.json \
  --metrics-dir experiments/figures \
  --output-dir experiments/results/stage4_balanced_paper_assets \
  --print-summary
```

Generated CSV/Markdown/PNG outputs should not be committed. Full protocol:
`experiments/protocols/stage4p_balanced_paper_assets_protocol.md`.

## Stage 4-Q1 main-run audit table

`experiments/scripts/build_stage4_main_run_audit.py` builds one formal
run-level audit table for the Stage 4-J balanced Trial 4/5/6 main repeats. It
uses exact formal repeat filenames, excludes diagnostic smoke/root-cause files,
joins divergence-inspector labels, preserves command/reference/trajectory
diagnostic fields when available, and joins Stage 4-O manual path/collision
annotations when a row matches by `run_name` or `csv_path`.

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/build_stage4_main_run_audit.py \
  --metrics-dir experiments/figures \
  --manual-annotations experiments/protocols/stage4o_manual_failure_annotations.json \
  --output-csv experiments/results/stage4_main_run_audit/stage4_main_run_audit.csv \
  --output-md experiments/results/stage4_main_run_audit/stage4_main_run_audit_summary.md \
  --print-summary
```

Generated CSV/Markdown outputs under
`experiments/results/stage4_main_run_audit/` should not be committed. Full
protocol: `experiments/protocols/stage4q_main_run_audit_protocol.md`.

## Stage 4-R fixed-scale frontier runner

`experiments/scripts/run_stage4_fixed_scale_frontier.py` generates a safe
print-only command plan for fixed-scale frontier screening. The purpose is to
test scales such as `0.70` or `0.75` before adding more learned adapter tuning.
Default behavior does not modify planner XML or run simulation; `--execute`
must be provided explicitly to run the generated commands.

Example dry run for scale `0.75`:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/run_stage4_fixed_scale_frontier.py \
  --scale 0.75 \
  --trials 4 5 6 \
  --repeats 1 2 3 \
  --duration 75 \
  --startup-wait 25 \
  --goal-repeat 10 \
  --goal-interval 1.0 \
  --dry-run \
  --print-commands
```

Screening scales are `0.60`, `0.65`, `0.70`, `0.75`, `0.80`, and `0.90`;
existing `fixed_s085` covers scale `0.85`. Generated CSV/PNG/TXT/Markdown
outputs should not be committed. Full protocol:
`experiments/protocols/stage4r_fixed_scale_frontier_protocol.md`.

Stage 4-R tuned fixed-scale frontier result:

- `fixed_s080` achieved `24/30` strict-valid runs (`80.0%`) across Trial 4/5/6.
- Per-trial counts were Trial 4 `8/10`, Trial 5 `9/10`, and Trial 6 `7/10`.
- `fixed_s080` slightly exceeds `risk_adapter_v1` (`23/30`) and should be used
  as the current tuned static frontier reference for `risk_adapter_v2`.
- Result document:
  `experiments/protocols/stage4r_fixed_s080_frontier_result.md`.

## Stage 4-S risk_adapter_v2 design

Stage 4-S defines the `risk_adapter_v2` calibrated risk-conditioned execution
governor design. The design uses `fixed_s080` as the static frontier reference
and aims to match or exceed the protocol-matched `fixed_s080` result while
preserving adaptive behavior.

Stage 4-S3 implements the first disabled-by-default `risk_adapter_v2` policy
mode in
`experiments/command_adaptation/scripts/risk_conditioned_command_adapter.py`
while keeping `risk_adapter_v1` unchanged. This first pass is risk-only plus
hysteresis; command/reference/trajectory diagnostics are deferred to later v2
extensions.

Example launch snippet for a future manual screening run:

```bash
roslaunch command_adaptation risk_conditioned_command_adapter.launch \
  policy_mode:=risk_adapter_v2 \
  enable_risk_conditioning:=true
```

Stage 4-U2 later found `risk_adapter_v2` and `fixed_s080` tied at `21/30`
under the single-goal mission protocol. The next step is `risk_adapter_v2.1`
design before further tuning or paper-facing dominance claims.

Design protocol:
`experiments/protocols/stage4s_risk_adapter_v2_design.md`.

Current v2.1 design protocol:
`experiments/protocols/stage4v_risk_adapter_v21_design.md`.

## Stage 4 log divergence inspector

`experiments/scripts/inspect_stage4_log_divergence.py` 用于离线检查 Stage 4 CSV log 中的
SO3 command saturation、command NaN、speed threshold、swing warning/strict threshold 和 position jump
timing，帮助区分 sudden fly-away / teleport-like divergence。它不运行 ROS、simulation、RViz
或 `catkin_make`。`failure_mode_guess` 是 heuristic label；clean valid runs 应显示
`no_divergence_detected`，transient saturation without NaN/divergence 会显示
`command_saturation_without_divergence`，不应当作 invalid divergence。
`swing_angle_deg >= 30` 只是 warning threshold，会报告为
`swing_warning_no_nan`；`strict_safety_no_nan` 只保留给 no-NaN 条件下的
paper-facing strict safety violation，例如 `swing_angle_deg >= 60`、
UAV/payload speed `>= 4 m/s`、target-error failure evidence，或伴随 high
speed / large final error / NaN / other instability evidence 的 clear
teleport-like position jump。raw UAV/payload position jump 或 reference jump
alone 现在是 warning-only taxonomy，会报告为
`position_or_reference_jump_warning_no_nan` 或通过
`position_jump_warning_only` / `reference_jump_warning_only` 字段暴露；它不应覆盖
strict-valid / `label_strict_invalid`。

The inspector sorts rows by timestamp before timing analysis, ignores string
diagnostic reason fields during nonfinite scans, and reports aggregate timing
fields such as `first_command_nan_time`, `first_state_divergence_time`,
`first_reference_jump_time`, and `reference_jump_after_divergence`. Late
reference jumps after command NaN/state divergence should not be treated as
initial planner reference root cause.

The latest batch audit categories include `command_nan_before_state_divergence`,
`command_saturation_before_nan`, `command_saturation_without_divergence`,
`no_divergence_detected`, `state_divergence_before_command_nan`,
`position_or_reference_jump_warning_no_nan`, `strict_safety_no_nan`,
`swing_warning_no_nan`, and `target_error_only`. These are heuristic
classification labels, not final physical root-cause proof; paper-facing
success-rate tables should still use strict-valid / `label_strict_invalid`.

检查单个 CSV，并打印一个相对时间窗口内的关键列：

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/inspect_stage4_log_divergence.py \
  --csv experiments/logs/autotrans_log_20260510_190453.csv \
  --window-start 13.5 \
  --window-end 16.5 \
  --print-summary
```

扫描所有 metrics summaries，并把报告写到 ignored `experiments/results/`：

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/inspect_stage4_log_divergence.py \
  --metrics-glob "experiments/figures/*_metrics_summary.txt" \
  --output-csv experiments/results/stage4_log_divergence_report.csv \
  --print-summary
```

生成的 `experiments/results/stage4_log_divergence_report.csv` 不应提交。完整 protocol 见
`experiments/protocols/stage4_log_divergence_inspection_protocol.md`。

## Stage 4-L reference logging

`experiments/autotrans_logger/scripts/state_logger.py` can now log the controller
reference stream when `enable_reference_logging=true`。默认 source 是当前
`simple_run.launch` 中的 `/mpc_controller_node/mpc/all_ref_data`
(`nav_msgs/Path`)；如果某个 launch flow 发布 `/position_cmd`
(`quadrotor_msgs/PositionCommand`)，可以设置
`reference_message_type=position_command` 和 `reference_topic=/position_cmd`。
新增 CSV columns 包括 `ref_pos_*`、`ref_vel_*`、`ref_acc_*`、`ref_yaw`、
`ref_yaw_dot`、`ref_msg_ros_time` 和 `ref_available`。

`experiments/autotrans_logger/scripts/analyze_log.py` 会在这些 columns 存在时输出
`first_ref_pos_jump_gt1m_time`、`first_ref_acc_gt5_time`、`max_uav_ref_position_error`
等 reference diagnostics，并尝试生成 `ref_xyz.png`、`ref_speed.png` 和
`uav_ref_error.png`。旧 CSV 没有 `ref_*` columns 时仍可正常分析。

## Stage 4-N3 SO3 command validity diagnostics

`experiments/autotrans_logger/scripts/state_logger.py` now derives SO3 command
validity diagnostics from `/so3cmd` without changing the command path. New CSV
columns include `command_invalid_event`, `command_invalid_reason`,
`command_saturation_event`, `command_saturation_reason`,
`sustained_command_saturation_event`, and `guarded_command_applied`.

The default diagnostic thresholds are `thrust_saturation_threshold=59.9`,
`bodyrate_xy_saturation_threshold=2.99`,
`bodyrate_z_saturation_threshold=1.19`, and
`sustained_saturation_duration_sec=0.2`. Since Stage 4-N3 is logging-only,
`guarded_command_applied` should remain `0` until a future active C++ guard is
implemented.

`experiments/autotrans_logger/scripts/analyze_log.py` reports command-invalid,
command-saturation, sustained-saturation, and guarded-command counts/timing
when these columns exist. Old CSV logs without the Stage 4-N3 columns still
analyze normally.

## Stage 4-N4 active SO3 command NaN guard

Stage 4-N4 adds an optional active diagnostic guard in
`uav_simulator/so3_quadrotor/src/so3_quadrotor_nodelet.cpp::cmd_callback()`.
It is disabled by default with `enable_command_nan_guard: false` in
`uav_simulator/uav_simulator/config/so3_quadrotor.yaml`.

When enabled, the guard blocks NaN/Inf `so3_thrust` or `so3_bodyrate_*` values
from being copied into simulator command state, optionally holds the last
finite command, and publishes `/so3_command_guard/guarded_command_applied` as
`std_msgs/Bool`. `guarded_command_applied=1` marks a diagnostic-invalid safety
event; guarded runs should not be mixed with unguarded baseline claims, and
the guard does not address `state_divergence_before_command_nan` cases.

## Stage 4-O path-feasibility annotations

`experiments/protocols/stage4o_path_feasibility_annotation_protocol.md`
defines manual annotations for path-through-obstacle, obstacle contact,
obstacle stop, and teleport-like divergence after obstacle interaction.
Initial annotations are stored in
`experiments/protocols/stage4o_manual_failure_annotations.json`. These fields
explain failure causes alongside strict-valid / `label_strict_invalid`
metrics; they do not change planner, controller, simulator, or logger
behavior.

Stage 4-O3 adds lightweight trajectory publish diagnostics to
`experiments/autotrans_logger/scripts/state_logger.py` and
`experiments/autotrans_logger/scripts/analyze_log.py`. New CSV metrics include
`trajectory_publish_count`, `trajectory_update_count`,
`trajectory_last_update_time`, `trajectory_time_since_last_update`, and
`first_trajectory_time`. These values are a replan proxy only; they do not
prove path infeasibility or collision without manual annotation or later
path/ESDF checking.

The first Stage 4-O3 diagnostic smoke result is documented in
`experiments/protocols/stage4o_trajectory_publish_diagnostic_smoke_result.md`.
All three `original` / strong-wind / Trial 6 / `goal_repeat=10` smokes were
valid and did not reproduce NaN or teleport-like divergence. The smoke2 run is
classified as `swing_warning_no_nan`, not `strict_safety_no_nan`, because
`swing_angle_deg >= 30` is warning-only and the run stayed below strict safety
thresholds. These smokes are diagnostic-only and should not be used as final
balanced comparison evidence.

## Stage 4-T1 goal/arrival diagnostics

Stage 4-T1 adds goal reception and post-arrival diagnostics to separate normal
single-goal transport from repeated-goal / post-arrival replan stress under
`goal_repeat=10`.

`experiments/autotrans_logger/scripts/state_logger.py` now subscribes to
`/move_base_simple/goal` by default and records `goal_received_count`,
`goal_last_received_time`, `goal_time_since_last_received`,
`first_goal_time`, `goal_pos_x`, `goal_pos_y`, `goal_pos_z`, and
`goal_available`. The logger params are:

- `enable_goal_logging`, default `true`
- `goal_topic`, default `/move_base_simple/goal`

`experiments/autotrans_logger/scripts/analyze_log.py` uses target args to
estimate `first_arrival_time` with a `0.5 s` sustained window. The first-pass
criterion is UAV XY error within `target_xy_tolerance`, payload XY error within
the same tolerance when payload position is available, and UAV/payload speed
below `0.5 m/s` when velocity fields are available. It then reports
post-arrival goal reception and trajectory-update counts. Old CSV files without
goal columns remain analyzable; goal metrics are emitted only when the new goal
columns are available, and arrival metrics require target args.

Stage 4-S `risk_adapter_v2` results should be interpreted with these
diagnostics before further tuning. Results collected with `goal_repeat=10`
should be labeled as repeated-goal protocol evidence. Stage 4-U2 now provides
the current 10-repeat `goal_repeat=1` single-goal comparison.

## Stage 4-T2 goal-repeat artifact diagnostic

`experiments/protocols/stage4t_goal_repeat_artifact_diagnostic_result.md`
records the minimal strong-wind Trial 4 diagnostic comparing `fixed_s080` and
`risk_adapter_v2` under `goal_repeat=1` and `goal_repeat=10`.

Main result:

- `risk_adapter_v2`, `goal_repeat=1`: `3/3` strict-valid.
- `risk_adapter_v2`, `goal_repeat=10`: `0/3` strict-valid.
- All `risk_adapter_v2` `goal_repeat=10` failures occurred after arrival and
  after post-arrival goal publishes.
- `fixed_s080`, `goal_repeat=10`: `2/3` strict-valid with one post-arrival
  failure.
- `fixed_s080`, `goal_repeat=1`: `1/3` strict-valid with two pre-arrival
  failures.

Interpretation: `goal_repeat=10` is a useful repeated-goal / post-arrival
replan stress protocol, not a generic single-goal mission protocol. Future
Stage 4 tables should label the goal protocol explicitly. `risk_adapter_v2`
should be screened under `goal_repeat=1` across Trial 4/5/6 before further
threshold tuning.

## Stage 4-U single-goal mission screening

`experiments/protocols/stage4u_single_goal_screening_result.md` records the
first strong-wind single-goal mission screening under `goal_repeat=1` across
Trial 4, Trial 5, and Trial 6 repeat1-3.

Main result:

| Method | Trial 4 | Trial 5 | Trial 6 | Aggregate |
| --- | ---: | ---: | ---: | ---: |
| `fixed_s080` | `1/3` | `3/3` | `2/3` | `6/9` |
| `risk_adapter_v2` | `3/3` | `3/3` | `3/3` | `9/9` |

Interpretation: this was diagnostic screening and is superseded by Stage 4-U2.
Use `experiments/protocols/stage4u_single_goal_10repeat_result.md` for the
current single-goal comparison. Keep `goal_repeat=10` as the repeated-goal
stress benchmark.

## Stage 4-U2 single-goal 10-repeat expansion

`experiments/protocols/stage4u_single_goal_10repeat_result.md` records the
10-repeat strong-wind single-goal mission expansion under `goal_repeat=1`
across Trial 4, Trial 5, and Trial 6.

Main result:

| Method | Trial 4 | Trial 5 | Trial 6 | Aggregate |
| --- | ---: | ---: | ---: | ---: |
| `fixed_s080` | `7/10` | `6/10` | `8/10` | `21/30` |
| `risk_adapter_v2` | `9/10` | `6/10` | `6/10` | `21/30` |

Interpretation: `risk_adapter_v2` matches `fixed_s080` in aggregate under the
single-goal mission protocol, improves Trial 4, matches Trial 5, and
underperforms on Trial 6. Do not claim `risk_adapter_v2` dominates
`fixed_s080`. Design `risk_adapter_v2.1` before further expansion, with
attention to reducing long-duration `0.65` use on Trial 6. Keep
`goal_repeat=10` as the separate repeated-goal stress benchmark.

## Stage 4-V risk_adapter_v2.1 design

`experiments/protocols/stage4v_risk_adapter_v21_design.md` records the next
algorithmic design step after the Stage 4-U2 tie.

Design direction:

- Keep the strong `risk_adapter_v2` Trial 4 behavior.
- Reduce long-duration `0.65` use that may hurt Trial 6.
- Use `0.70` or `0.75` for ordinary high-risk states.
- Reserve `0.65` for sustained or severe risk.
- Keep `risk_adapter_v2` unchanged; Stage 4-V2 implements the separate
  `policy_mode=risk_adapter_v21`.
- Do not modify planner, controller, or simulator code for this policy.

## Stage 4-V2 risk_adapter_v21 implementation

Stage 4-V2 adds the first disabled-by-default `risk_adapter_v21` policy mode in
`experiments/command_adaptation/scripts/risk_conditioned_command_adapter.py`.
It keeps `risk_adapter_v2` unchanged and uses the existing command-adaptation
topics.

Manual screening launch snippet:

```bash
roslaunch command_adaptation risk_conditioned_command_adapter.launch \
  policy_mode:=risk_adapter_v21 \
  enable_risk_conditioning:=true
```

`risk_adapter_v21` uses `0.70` for ordinary long-horizon high risk and reserves
`0.65` for sustained/severe risk after dwell. It must be screened under
`goal_repeat=1` against `fixed_s080` and `risk_adapter_v2` before any
10-repeat expansion. Do not claim improvement before those experiments.

## Stage 4-V3 risk_adapter_v21 screening result

`experiments/protocols/stage4v_risk_adapter_v21_screening_result.md` records
the first `risk_adapter_v21` single-goal screening under strong wind:

- protocol: `goal_repeat=1`
- trials: Trial 4, Trial 5, Trial 6
- repeats: repeat1 through repeat3
- result: `risk_adapter_v21` achieved `9/9` strict-valid
- diagnostic labels: `command_saturation_without_divergence` (`6`),
  `no_divergence_detected` (`2`), `swing_warning_no_nan` (`1`)

Scale behavior: Trial 4 stayed around mean scale `0.843`; Trial 5 and Trial 6
stayed around mean scale `0.711` with minimum `0.70`, avoiding the long-duration
`0.65` behavior that motivated Stage 4-V.

This screening is superseded by Stage 4-V4 below. It motivated the
`goal_repeat=1` 10-repeat expansion and should not be used as the current
`risk_adapter_v21` result.

## Stage 4-V4 risk_adapter_v21 10-repeat result

`experiments/protocols/stage4v_risk_adapter_v21_10repeat_result.md` records
the 10-repeat `risk_adapter_v21` single-goal expansion under strong wind:

- protocol: `goal_repeat=1`
- trials: Trial 4, Trial 5, Trial 6
- repeats: repeat1 through repeat10
- result: `risk_adapter_v21` achieved `25/30` strict-valid
- per-trial counts: Trial 4 `10/10`, Trial 5 `9/10`, Trial 6 `6/10`

Stage 4-V4 comparison at the time:

| Method | Strict-valid count |
| --- | ---: |
| `fixed_s080` | `21/30` |
| `risk_adapter_v2` | `21/30` |
| `risk_adapter_v21` | `25/30` |

Stage 4-X2 later completed the missing single-goal baselines. In the completed
single-goal comparison, `windlevel_s085` achieved `26/30`, while
`risk_adapter_v1` and `risk_adapter_v21` each achieved `25/30`.
Interpretation: `risk_adapter_v21` remains competitive and preserves strong
Trial 4 behavior, but it is not the completed single-goal aggregate winner and
Trial 6 remains the bottleneck. Do not claim statistical significance, a safety
guarantee, or that `risk_adapter_v21` beats all baselines.

## Stage 4-W protocol-split paper assets

`experiments/scripts/generate_stage4_protocol_split_paper_assets.py` generates
current paper-facing Stage 4 tables and a grouped success-rate plot with
explicit protocol labels.

It separates:

- single-goal mission protocol: `goal_repeat=1`
- goal-reissue stress protocol: `goal_repeat=10`

Stage 4-W3 updates this generator after Stage 4-X2 and corrected Stage 4-X1 so
the generated summary reports the completed single-goal method set and the
corrected `risk_adapter_v21` goal-reissue stress result.

Example:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/generate_stage4_protocol_split_paper_assets.py \
  --metrics-dir experiments/figures \
  --output-dir experiments/results/stage4_protocol_split_paper_assets \
  --print-summary
```

Generated outputs under `experiments/results/` are ignored and should not be
committed.

Current paper-facing protocol split:

| Protocol | Best method in evaluated set | Strict-valid count |
| --- | --- | ---: |
| single-goal mission, `goal_repeat=1` | `windlevel_s085` | `26/30` |
| goal-reissue stress, `goal_repeat=10` | `fixed_s080` | `24/30` |

The single-goal mission table must include all seven methods: `original`,
`fixed_s085`, `windlevel_s085`, `fixed_s080`, `risk_adapter_v1`,
`risk_adapter_v2`, and `risk_adapter_v21`.

The goal-reissue stress table must include all six methods: `original`,
`fixed_s085`, `windlevel_s085`, `risk_adapter_v1`, `fixed_s080`, and
`risk_adapter_v21`.

Stage 4-W3 generated-summary claim scope:

- Under completed single-goal protocol, `windlevel_s085` achieved `26/30`.
- `risk_adapter_v1` and `risk_adapter_v21` each achieved `25/30` in
  single-goal and tie as the strongest learned/risk-conditioned variants.
- Under goal-reissue stress, `fixed_s080` achieved `24/30`.
- No current learned variant dominates both protocols.
- Do not claim `risk_adapter_v21` beats all baselines, is overall best, or
  that learned methods uniformly dominate heuristics.

## Stage 4-Y results narrative draft

`experiments/protocols/stage4y_results_narrative_draft.md` is the current
paper-facing Results narrative draft after Stage 4-W3.

It frames Stage 4 as:

- learned risk-conditioned execution governor
- dual-protocol evaluation
- strong heuristic/static frontier comparison
- failure-mode-aware analysis

Current paper-facing interpretation:

- Single-goal mission protocol (`goal_repeat=1`): `windlevel_s085` is highest
  at `26/30`; `risk_adapter_v1` and `risk_adapter_v21` tie at `25/30`.
- Goal-reissue stress protocol (`goal_repeat=10`): `fixed_s080` is highest at
  `24/30`; `risk_adapter_v1` is second at `23/30`;
  `risk_adapter_v21` is `20/30`.
- No current learned variant dominates both protocols.

Do not claim `risk_adapter_v21` is the overall best method, do not create a
mixed-protocol aggregate, and do not claim statistical significance or a safety
guarantee.

## Stage 4-Z failure-mode paper assets

`experiments/scripts/generate_stage4_failure_mode_paper_assets.py` generates
paper-ready failure-mode tables and a stacked-bar figure for the completed
protocol-split Stage 4 results.

It uses strict-valid as the paper-facing success metric and calls
`experiments/scripts/inspect_stage4_log_divergence.py` for diagnostic
`failure_mode_guess` fields. The derived `failure_group` is diagnostic, not
perfect root-cause proof.

Stage 4-Z2 refines the output for paper use:

- all-run failure groups use `valid_or_warning` for strict-valid runs,
  including warning-style diagnostic labels
- invalid-only failure-group CSV/Markdown tables are generated
- `stage4_failure_group_invalid_only_stacked_bar.png` is the preferred
  failure-analysis figure

Stage 4-Z3 records the Stage 4-Z2 result in
`experiments/protocols/stage4z_failure_mode_paper_assets_result.md`: the
generated assets cover `390` run rows and `110` strict-invalid runs. The
invalid-only figure should support failure-aware analysis, while strict-valid
remains the main paper-facing metric.

Example:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/generate_stage4_failure_mode_paper_assets.py \
  --metrics-dir experiments/figures \
  --output-dir experiments/results/stage4_failure_mode_paper_assets \
  --print-summary
```

Generated outputs under `experiments/results/` are ignored and should not be
committed. The protocol is
`experiments/protocols/stage4z_failure_mode_paper_assets_protocol.md`.

Use Stage 4-Z outputs to inspect Trial 4 goal-reissue stress weakness and
Trial 6 bottlenecks before any `risk_adapter_v22` design.

## Stage 4-AA targeted diagnosis assets

`experiments/scripts/generate_stage4_targeted_diagnosis_assets.py` generates
targeted diagnosis tables and optional plots for Trial 4 goal-reissue stress
`risk_adapter_v21` failures and the Trial 6 bottleneck.

It reuses the Stage 4-Z2 strict-valid and `failure_group` mapping, then writes
run-level tables, a Trial 6 method summary, and a cautious diagnosis summary.
Generated outputs under `experiments/results/` are ignored and should not be
committed.

Example:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/generate_stage4_targeted_diagnosis_assets.py \
  --metrics-dir experiments/figures \
  --output-dir experiments/results/stage4_targeted_diagnosis \
  --print-summary
```

The protocol is
`experiments/protocols/stage4aa_targeted_diagnosis_protocol.md`. Review the
Stage 4-AA outputs before designing `risk_adapter_v22`; any future method
should be phase-aware / failure-aware rather than Trial-4-specific.

## Stage 4-AA2 representative trace plots

`experiments/scripts/plot_stage4_representative_failure_traces.py` generates
offline representative trace plots from existing CSV logs. It supports the
Stage 4-AB decision gate before any `risk_adapter_v22` design.

The script automatically selects representative runs for Trial 4
goal-reissue stress `risk_adapter_v21`, Trial 4 stress comparison against
`fixed_s080` and `risk_adapter_v1`, and the Trial 6 single-goal bottleneck.
It skips missing CSV columns and records caveats in the generated summary.

Example:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/plot_stage4_representative_failure_traces.py \
  --metrics-dir experiments/figures \
  --output-dir experiments/results/stage4_representative_traces \
  --print-summary
```

Generated outputs under `experiments/results/` are ignored and should not be
committed. The protocol is
`experiments/protocols/stage4aa_representative_trace_protocol.md`. Do not
create `risk_adapter_v22` until these representative trace plots are reviewed.

## Stage 4-AA3 representative trace review

`experiments/protocols/stage4aa_representative_trace_review_result.md` records
the human review of the Stage 4-AA2 representative trace plots.

The review supports the Stage 4-AB balanced-governor framing: keep
`risk_adapter_v1` as the tentative balanced learned / risk-conditioned
protagonist, treat `risk_adapter_v21` as a strong nominal variant / ablation,
and present `windlevel_s085` and `fixed_s080` as protocol-specialist
baselines.

The AA3 decision is to not create `risk_adapter_v22` yet. If a future variant
is attempted, it should use a generic risk-health-aware, phase-aware,
reference / trajectory-health-aware, or command / state-health-aware mechanism
rather than simple threshold tuning. The next recommended step is Stage 4-AC
balanced robustness / protocol regret assets.

## Stage 4-AC balanced robustness assets

`experiments/scripts/generate_stage4_balanced_robustness_assets.py` generates
paper-facing balanced robustness, protocol regret, and Pareto-frontier assets
from the completed protocol-split Stage 4 counts.

It writes complete cross-protocol tables for `original`, `fixed_s085`,
`windlevel_s085`, `fixed_s080`, `risk_adapter_v1`, and `risk_adapter_v21`.
`risk_adapter_v2` is included only in the single-protocol-only table because
its goal-reissue stress result is missing in the current protocol-split
matrix.

Example:

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/scripts/generate_stage4_balanced_robustness_assets.py \
  --output-dir experiments/results/stage4_balanced_robustness_assets \
  --print-summary
```

Generated outputs under `experiments/results/` are ignored and should not be
committed. The protocol is
`experiments/protocols/stage4ac_balanced_robustness_assets_protocol.md`.
The completed result interpretation is recorded in
`experiments/protocols/stage4ac_balanced_robustness_assets_result.md`.

## Stage 4-AC2 balanced robustness result

`experiments/protocols/stage4ac_balanced_robustness_assets_result.md` records
the completed Stage 4-AC balanced robustness / protocol regret result.

The result confirms `risk_adapter_v1` as the tentative balanced learned /
risk-conditioned protagonist: it has the best mean valid count (`24.0/30`),
the best worst-protocol valid count (`23/30`), and the lowest total regret
(`2`). `windlevel_s085` remains the single-goal specialist, `fixed_s080`
remains the goal-reissue stress specialist, and `risk_adapter_v21` should not
be framed as the final protagonist.

Do not create `risk_adapter_v22` yet. Stage 4-AD now freezes the
figure/table plan for Results writing using the Stage 4-AC assets.

## Stage 4-AD paper figure/table plan

`experiments/protocols/stage4ad_paper_figure_table_plan.md` freezes the main
paper figure/table plan for the reframed Stage 4 paper.

The plan uses protocol-split success, balanced robustness / protocol regret,
invalid-only failure groups, and representative trace case studies. It centers
`risk_adapter_v1` as the balanced learned / risk-conditioned governor,
presents `windlevel_s085` and `fixed_s080` as protocol specialists, and keeps
`risk_adapter_v21` as a strong nominal / single-goal variant rather than the
final method.

Stage 4-AE records the paper outline / section skeleton, Stage 4-AF records
the paper Abstract and Introduction draft, Stage 4-AG records the Method
section draft, Stage 4-AH records the Results section draft, Stage 4-AI
records the Discussion and Limitations draft, Stage 4-AJ records the current
full paper assembly draft, Stage 4-AK records the citation / references plan,
Stage 4-AM records the citation collection workflow, Stage 4-AL records the
final figure generation plan, Stage 4-AL2 records the paper figure package
generator, and Stage 4-AN records the manual schematic specification. The next
writing step is Stage 4-AM2 verified citation collection or Stage 4-AN2 manual
schematic creation. Do not create `risk_adapter_v22` yet.

## Stage 4-AE paper outline section skeleton

`experiments/protocols/stage4ae_paper_outline_section_skeleton.md` records the
paper-level outline for the reframed IROS/ICRA/RA-L style paper.

It defines candidate titles, the core thesis, a draft abstract skeleton,
Introduction and Related Work structure, Method and Experimental Setup
sections, Results paragraphs aligned to the Stage 4-AD figure plan, Discussion
and Limitations sections, an Appendix plan, and a claim audit table.

Stage 4-AF records the paper Abstract and Introduction draft, Stage 4-AG
records the Method section draft, Stage 4-AH records the Results section
draft, Stage 4-AI records the Discussion and Limitations draft, Stage 4-AJ
records the full paper assembly draft, Stage 4-AK records the citation /
references plan, Stage 4-AM records the citation collection workflow, Stage
4-AL records the final figure generation plan, Stage 4-AL2 records the paper
figure package generator, and Stage 4-AN records the manual schematic
specification. The next writing step is Stage 4-AM2 verified citation
collection or Stage 4-AN2 manual schematic creation. Do not create
`risk_adapter_v22` yet.

## Stage 4-AF abstract introduction draft

`experiments/protocols/stage4af_abstract_introduction_draft.md` records the
current paper Abstract and Introduction draft based on the Stage 4-AE skeleton.

The draft presents `risk_adapter_v1` as the tentative balanced learned /
risk-conditioned protagonist, keeps `risk_adapter_v21` as a nominal /
single-goal variant or ablation, and uses bounded wording around
balanced/protocol-level robustness under the tested protocols.

Stage 4-AG now records the Method section draft, Stage 4-AH records the
Results section draft, and Stage 4-AI records the Discussion and Limitations
draft. Stage 4-AJ now records the full paper assembly draft, Stage 4-AK
records the citation / references plan, Stage 4-AM records the citation
collection workflow, Stage 4-AL records the final figure generation plan,
Stage 4-AL2 records the paper figure package generator, and Stage 4-AN records
the manual schematic specification. The next writing step is Stage 4-AM2
verified citation collection or Stage 4-AN2 manual schematic creation. Do not
create `risk_adapter_v22` yet.

## Stage 4-AG method section draft

`experiments/protocols/stage4ag_method_section_draft.md` records the current
paper Method section draft.

The draft presents a stack-compatible execution governor that publishes
`speed_scale` and `acceleration_scale` through the command-adaptation
interface while keeping the planner, payload MPC, and SO3 controller
unchanged. It centers `risk_adapter_v1` as the balanced learned /
risk-conditioned protagonist and treats `risk_adapter_v21` as a strong
nominal / single-goal variant or ablation.

## Stage 4-AH results section draft

`experiments/protocols/stage4ah_results_section_draft.md` records the current
paper Results section draft.

The draft organizes the Results around protocol-split success, balanced
robustness / protocol regret, invalid-only failure groups, and representative
trace analysis. It centers `risk_adapter_v1` as the balanced learned /
risk-conditioned protagonist, presents `windlevel_s085` and `fixed_s080` as
protocol specialists, and keeps `risk_adapter_v21` as a strong nominal /
single-goal variant rather than the final method.

## Stage 4-AI discussion limitations draft

`experiments/protocols/stage4ai_discussion_limitations_draft.md` records the
current paper Discussion and Limitations draft.

The draft argues for balanced robustness rather than universal learned-method
dominance, explains why strong simple baselines matter, bounds the
failure-mode interpretation, and states that `risk_adapter_v22` is not
justified without a reusable phase-aware, reference-aware, risk-health-aware,
or failure-aware mechanism.

Stage 4-AJ now records the full paper assembly draft, Stage 4-AK records the
citation / references plan, Stage 4-AM records the citation collection
workflow, Stage 4-AL records the final figure generation plan, Stage 4-AL2
records the paper figure package generator, and Stage 4-AN records the manual
schematic specification. The next writing step is Stage 4-AM2 verified
citation collection or Stage 4-AN2 manual schematic creation. Do not create
`risk_adapter_v22` yet.

## Stage 4-AM citation collection plan

`experiments/protocols/stage4am_citation_collection_plan.md` records the
practical citation collection and bibliography insertion workflow.

The plan converts the Stage 4-AK citation slots into priority tiers, a
collection table, a BibTeX / metadata verification checklist, paper insertion
locations, citation-risk wording fallbacks, and an internal-vs-external
evidence boundary. It does not finalize the bibliography and does not insert
unverified citations.

Stage 4-AL now records the final figure generation plan, Stage 4-AL2 records
the paper figure package generator, Stage 4-AN records the manual schematic
specification, Stage 4-AN2 records schematic generation, Stage 4-AL3 refreshes
the figure package, and Stage 4-AM2 records verified citations. The next step
after AM2 is Stage 4-AM3 BibTeX drafting / citation insertion plan or Stage
4-AO manuscript formatting plan. Do not create `risk_adapter_v22` yet.

## Stage 4-AM2 verified citation collection result

`experiments/protocols/stage4am2_verified_citation_collection_result.md`
records the user-provided verified citation collection for the assembled Stage
4 paper.

It maps verified citation metadata to the Stage 4-AK / Stage 4-AM citation
slots for suspended-payload UAV transport and control, runtime governors /
reference governors / safety filters, learning-enhanced aerial robustness, and
benchmarking / stress testing / failure analysis. It does not finalize the
bibliography, does not generate BibTeX, and does not insert citation keys into
manuscript prose.

Remaining metadata gaps are explicitly marked as TODO / needs verification.
The next citation step is Stage 4-AM3 BibTeX drafting / citation insertion
plan, or Stage 4-AO manuscript formatting plan in parallel. Do not create
`risk_adapter_v22` yet.

## Stage 4-AM3 citation insertion draft

`experiments/protocols/stage4am3_citation_insertion_draft.md` maps Stage
4-AM2 citation keys into the current full paper assembly draft.

The draft separates ready-to-use keys, conditional keys that require metadata
verification, and internal-result references such as Table 1 and Figures 1-6.
It provides citation insertion guidance for the Abstract, Introduction,
Related Work, Method, Experimental Setup, and Discussion / Limitations
sections.

This stage does not generate BibTeX and does not insert final citations into
the manuscript body. Conditional keys should remain marked "use after
verification" until their AM2 metadata gaps are closed. The next step is Stage
4-AM4 BibTeX drafting after metadata verification, or Stage 4-AO manuscript
formatting plan. Do not create `risk_adapter_v22` yet.

## Stage 4-AM4 BibTeX draft

`experiments/protocols/stage4am4_bibtex_draft.md` records the draft BibTeX
blocks for ready-to-use citation metadata from Stage 4-AM2 / AM3.

This stage does not create or edit manuscript `.tex` or `.bib` files. It keeps
conditional references as TODO entries until their missing metadata is
verified. The next step is Stage 4-AO manuscript formatting plan or Stage
4-AP manuscript source scaffold. Do not create `risk_adapter_v22` yet.

## Stage 4-AO manuscript formatting plan

`experiments/protocols/stage4ao_manuscript_formatting_plan.md` defines how to
convert the assembled Stage 4 paper draft into a future manuscript source
scaffold.

This stage does not create `paper/`, `manuscript/`, `.tex`, or `.bib` files.
It maps the assembled draft, figure package, and AM4 citation key package into
a proposed manuscript layout. The next step is Stage 4-AP manuscript source
scaffold or Stage 4-AM5 conditional citation verification. Do not create
`risk_adapter_v22` yet.

## Stage 4-AP manuscript source scaffold

`paper/stage4_governor/` now contains the draft manuscript source scaffold for
the reframed Stage 4 paper.

`experiments/protocols/stage4ap_manuscript_scaffold_protocol.md` records the
created files, source inputs, copied figure assets, citation boundaries, and
claim boundaries. No LaTeX compile was run. The next step is Stage 4-AQ
LaTeX compile/check pass or Stage 4-AM5 conditional citation verification. Do
not create `risk_adapter_v22` yet.

## Stage 4-AQ LaTeX compile/check pass

`experiments/protocols/stage4aq_latex_compile_check_result.md` records the
first compile/check attempt for `paper/stage4_governor/`.

The scaffold inspection completed, but compilation could not start because
`latexmk`, `pdflatex`, and `bibtex` were not available in the local
environment. No PDF or auxiliary LaTeX files were produced, and no manuscript
formatting fixes were made. The next step is Stage 4-AR manuscript polish /
layout pass after a LaTeX toolchain is available, or Stage 4-AM5 conditional
citation verification. Do not create `risk_adapter_v22` yet.

## Stage 4-AQ2 LaTeX compile retry

`experiments/protocols/stage4aq2_latex_compile_retry_result.md` records the
compile retry after `latexmk`, `pdflatex`, and `bibtex` became available.

The retry still did not produce a PDF because `ieeeconf.cls` is missing from
the local TeX installation. The manuscript `\documentclass` was not changed;
the next compile step should add the official target venue class/template or
run in a matching LaTeX environment. Do not create `risk_adapter_v22` yet.

## Stage 4-AQ3 official template compile success

`experiments/protocols/stage4aq3_official_template_compile_result.md` records
the successful manual compile/check pass after adding
`paper/stage4_governor/ieeeconf.cls` as a tracked template class dependency.

The user ran:

```bash
cd paper/stage4_governor
latexmk -pdf -interaction=nonstopmode -file-line-error main.tex
```

The recorded result is `latexmk_exit=0`; `main.pdf` was generated successfully
during the manual check at approximately 2.3 MB, and `main.log` existed during
the check. Generated PDF, auxiliary, and log files were cleaned before commit
and are not tracked. No manuscript source content, figures, tables, references,
simulation, RViz, `roslaunch`, `catkin_make`, or figure generation changed.
Next step: Stage 4-AR manuscript polish / layout pass or Stage 4-AV RA-L
conversion continuation. Do not create `risk_adapter_v22` before Paper 1 RA-L
submission.

## Stage 4-AR manuscript polish / layout pass

`experiments/protocols/stage4ar_manuscript_polish_layout_result.md` records
the Stage 4-AR compile and presentation-only layout polish after AQ3.

Stage 4-AR cleaned prior LaTeX generated outputs, ran:

```bash
cd paper/stage4_governor
latexmk -pdf -interaction=nonstopmode -file-line-error main.tex
```

The compile succeeded with `latexmk_exit=0`; `main.pdf` was generated during
the check as an 8-page PDF of approximately 2.3 MB. The final log had no LaTeX
errors, undefined citations, undefined references, overfull hboxes, missing
figures, bibliography warnings, or float warnings. Remaining underfull boxes
are recorded as non-blocking layout reminders. The source-only fixes were a
two-row Figure 6 layout and removal of a resolved Table 1 layout TODO. Generated
PDF, auxiliary, and log files are not tracked. Next step: Stage 4-AT2 RA-L
submission checklist or Stage 4-AM5 conditional citation verification,
depending on final submission-readiness priorities. Do not create
`risk_adapter_v22` before Paper 1 RA-L submission.

## Stage 4-AS submission strategy plan

`experiments/protocols/stage4as_submission_strategy_plan.md` records the
post-research venue strategy. Paper 1 should target RA-L first with
`risk_adapter_v1` as the protagonist, while `risk_adapter_v21` remains a
strong nominal / single-goal variant or ablation.

Paper 2 should be a later mechanism-driven extension track, not a lightly
enlarged version of Paper 1. Possible extension targets include T-RO, IROS
2027, the next ICRA cycle, TCST, or T-ASE depending on the final mechanism and
evaluation direction. Do not create `risk_adapter_v22` before Paper 1 RA-L
submission unless explicitly overridden. The next step is Stage 4-AT RA-L
format conversion / venue-specific manuscript preparation.

## Stage 4-AT RA-L conversion submission audit

`experiments/protocols/stage4at_ral_conversion_submission_audit.md` records the
RA-L conversion and submission readiness audit for Paper 1. It inventories the
current `paper/stage4_governor/` scaffold, confirms that the scaffold is still
IROS / ICRA-like rather than RA-L-template-specific, lists RA-L conversion
needs, and separates Paper 1 must-fix items from optional should-fix evidence.

Stage 4-AT does not rewrite `paper/stage4_governor/main.tex`, section files,
`refs.bib`, figures, or tables. It also does not run LaTeX compilation,
simulation, RViz, ROS launch files, or figure generation. Stage 4-AU now
addresses the risk score / strict-valid metric documentation item, and Stage
4-AT2 now records the post-AR RA-L submission readiness checklist. The current
submission-readiness order is Stage 4-AM5 conditional citation verification,
Stage 4-AW final figure / caption polish, Stage 4-AX final claim audit, then
final compile. Do not create `risk_adapter_v22` before Paper 1 RA-L
submission.

## Stage 4-AT2 RA-L submission readiness checklist

`experiments/protocols/stage4at2_ral_submission_readiness_checklist.md`
records the RA-L submission readiness checklist after the clean Stage 4-AR
manuscript compile / layout pass.

Stage 4-AT2 confirms that the manuscript scaffold, official class file, clean
compile, main figures/tables, Table 1, Figures 1-6, drafted citations,
risk-score / metric documentation, artifact checksums, and RA-L-first paper
strategy are ready at scaffold level. It also tracks remaining must-fix items:
final RA-L / IEEE template and page-budget confirmation, visual PDF inspection,
author / affiliation completion, final title and citation checks, conditional
citation decisions, Figure 6 readability, caption polish, final claim audit,
supplementary package decisions, generated-PDF submission packaging, and final
compile after all edits.

The recommended next order after AT2 was Stage 4-AV template conversion,
Stage 4-AV2 compile/check, then Stage 4-AM5 conditional citation verification
and BibTeX cleanup, Stage 4-AW final figure / caption polish, Stage 4-AX final
claim audit, and final compile. Do not create `risk_adapter_v22` before Paper 1
RA-L submission.

## Stage 4-AV RA-L template conversion scaffold

`experiments/protocols/stage4av_ral_template_conversion_protocol.md` records
the RA-L-oriented template conversion scaffold for Paper 1.

Stage 4-AV uses the existing source scaffold under `paper/stage4_governor/`
and the user-provided template files under `paper/templates/ral/` to create a
separate scaffold under `paper/stage4_governor_ral/`. The detected template
uses:

```tex
\documentclass[letterpaper, 10 pt, conference]{ieeeconf}
```

The source scaffold remains unchanged. No LaTeX compile, simulation, RViz,
`roslaunch`, `catkin_make`, training script, or figure generation script is
run in Stage 4-AV. The next recommended stage is Stage 4-AV2 RA-L scaffold
compile/check pass. Do not create `risk_adapter_v22` before Paper 1 RA-L
submission.

## Stage 4-AV2 RA-L scaffold compile/check pass

`experiments/protocols/stage4av2_ral_scaffold_compile_check_result.md`
records the first compile/check pass for `paper/stage4_governor_ral/`.

Stage 4-AV2 cleans stale LaTeX generated outputs under
`paper/stage4_governor_ral/`, runs:

```bash
cd paper/stage4_governor_ral
latexmk -pdf -interaction=nonstopmode -file-line-error main.tex
```

The recorded compile succeeds with `latexmk_exit=0`; `main.pdf` is generated
as an 8-page PDF of approximately 2.3 MB during the check. The final log has
no LaTeX errors, undefined citations, undefined references, overfull hboxes,
missing figures, bibliography warnings, or float warnings. Residual underfull
boxes are recorded as non-blocking layout reminders. Generated PDF, auxiliary,
and log files are not committed. Next recommended work is Stage 4-AM5
conditional citation verification, Stage 4-AW final figure / caption polish,
or Stage 4-AX final claim audit depending on submission-readiness priority. Do
not create `risk_adapter_v22` before Paper 1 RA-L submission.

## Stage 4-AM5 conditional citation cleanup

`experiments/protocols/stage4am5_conditional_citation_cleanup_result.md`
records the active citation / BibTeX cleanup audit for the RA-L Paper 1
scaffold under `paper/stage4_governor_ral/`.

Stage 4-AM5 checks active `\cite{...}` usage against
`paper/stage4_governor_ral/refs.bib`, confirms 20 active cited keys and 20
matching active BibTeX entries, and finds no missing or unused active keys.
The unresolved conditional keys from Stage 4-AM3 / AM4 remain only as comments
/ TODOs and are excluded from active Paper 1 citations and active BibTeX
entries unless later verified. No fabricated citations are added, no web
metadata is used, and no LaTeX compile is run in AM5. Next recommended work is
Stage 4-AW final figure / caption polish, Stage 4-AX final claim audit, and
final compile. Do not create `risk_adapter_v22` before Paper 1 RA-L
submission.

## Stage 4-AW final figure / caption polish

`experiments/protocols/stage4aw_final_figure_caption_polish_result.md`
records the final figure / table caption polish pass for the RA-L Paper 1
scaffold under `paper/stage4_governor_ral/`.

Stage 4-AW updates caption text for the protocol schematic, balanced
robustness table, Pareto plot, protocol-regret plot, and representative trace
figure, while preserving numerical results, rankings, citation keys, and claim
boundaries. The pass keeps `risk_adapter_v1` as the balanced protagonist,
keeps `windlevel_s085` and `fixed_s080` as protocol specialists, and keeps
`risk_adapter_v21` as a strong nominal variant / ablation. The RA-L scaffold
recompiled successfully to 8 pages after the caption polish. No simulation,
RViz, `roslaunch`, `catkin_make`, training scripts, or figure generation
scripts were run. Do not create `risk_adapter_v22` before Paper 1 RA-L
submission.

## Stage 4-AX final claim audit

`experiments/protocols/stage4ax_final_claim_audit_result.md` records the final
claim audit for the RA-L Paper 1 scaffold under
`paper/stage4_governor_ral/`.

Stage 4-AX inspects active manuscript text for overclaiming-risk wording,
tightens broad `best`, proof, causality, deployment, and future-variant
language, and preserves the bounded core claim that `risk_adapter_v1` is the
balanced learned / risk-conditioned protagonist under the tested protocol
split. AX does not change numerical results, rankings, citation keys, Table 1
data, figures, algorithms, or experiment outputs. Next recommended work is
final compile / submission package checks, or an optional Stage 4-AM5 follow-up
if citation metadata changes. Do not create `risk_adapter_v22` before Paper 1
RA-L submission.

## Stage 4-AY final compile / submission package check

`experiments/protocols/stage4ay_final_compile_submission_check.md` records the
final compile check and submission package readiness checklist for the RA-L
Paper 1 scaffold under `paper/stage4_governor_ral/`.

Stage 4-AY cleans LaTeX generated outputs, runs:

```bash
cd paper/stage4_governor_ral
latexmk -pdf -interaction=nonstopmode -file-line-error main.tex
```

The final compile succeeds with `latexmk_exit=0` and produces an 8-page PDF
during the check. A temporary human-inspection copy is written to
`/tmp/stage4_governor_ral_final_check.pdf`. Generated PDF / aux / log files are
excluded from git. Next recommended work is Stage 4-AZ human visual PDF
inspection and final submission package assembly. Do not create
`risk_adapter_v22` before Paper 1 RA-L submission.

## Stage 4-AZ human visual inspection finding record

`experiments/protocols/stage4az_human_visual_submission_package_result.md`
records the manual PDF inspection findings after the Stage 4-AY clean compile.

Stage 4-AZ is documentation-only. It does not compile LaTeX, regenerate
figures, run simulation, run ROS, run training, or create new experiment
outputs. The human review finds presentation blockers: raw underscore-style
method names remain visible, Figure 1 / Figure 2 need placeholder handling and
external redraw, Figure 3 needs compactness polish, and Figure 6 needs a
simplified paper-facing replot plan with possible supplementary trace detail.
Next recommended stages are Stage 4-BA display-name cleanup, Stage 4-BB
schematic placeholder / redraw prep, Stage 4-BC Figure 3 compact polish, and
Stage 4-BD Figure 6 simplified replot. Do not create `risk_adapter_v22` before
Paper 1 RA-L submission.

## Stage 4-BA manuscript-visible display-name cleanup

`experiments/protocols/stage4ba_display_name_cleanup_result.md` records the
display-name cleanup pass for the RA-L Paper 1 scaffold under
`paper/stage4_governor_ral/`.

Stage 4-BA replaces manuscript-visible raw method tokens in active prose,
captions, panel labels, and Table 1 with paper-facing display names such as
Risk Adapter v1, Risk Adapter v2.1, Wind-Level 0.85, and Fixed Scale 0.80. It
preserves code-facing parameter names, file paths, artifact identifiers, and
diagnostic field names. The RA-L scaffold compiles successfully to 8 pages
after the cleanup. Figure-internal labels embedded inside existing images are
not regenerated in BA and remain for Stage 4-BC / Stage 4-BD. Do not create
`risk_adapter_v22` before Paper 1 RA-L submission.

## Stage 4-BB Figure 1 / Figure 2 placeholders and redraw workflow

`experiments/protocols/stage4bb_schematic_placeholder_redraw_plan.md` records
the placeholder swap and external redraw workflow for Figure 1 and Figure 2 in
the RA-L Paper 1 scaffold.

Stage 4-BB stops using the current generated Figure 1 / Figure 2 schematic
images in the active manuscript and replaces them with compact LaTeX
placeholder boxes. The existing image files remain in
`paper/stage4_governor_ral/figures/`, but they are not treated as final
submission visuals. The redraw plan allows PowerPoint, draw.io, Figma,
Illustrator, TikZ, or a manually curated vector graphic. Next recommended work
is Stage 4-BC Figure 3 compact polish, Stage 4-BD Figure 6 simplified replot,
and later Stage 4-BE external schematic replacement. Do not create
`risk_adapter_v22` before Paper 1 RA-L submission.

## Stage 4-AU risk score and strict-valid metric documentation

`experiments/protocols/stage4au_risk_score_metric_documentation.md` records the
Paper 1 RA-L documentation pass for `risk_score_3s`, `risk_score_5s`,
`risk_adapter_v1`, and the strict-valid metric. It is documentation-only: it
does not run experiments, regenerate figures, compile LaTeX, or create
`risk_adapter_v22`.

Stage 4-AU documents the adapter topics and logged fields, unavailable risk
score handling, `risk_adapter_v1` thresholds and scale logic, the exact
paper-facing strict-valid predicate, and the boundary between strict-valid
success and diagnostic `failure_group` / `failure_mode_guess` labels. Remaining
RA-L risk-score TODOs are final exported model metadata, exact feature schema,
calibration method or caveat, confidence / OOD behavior, and inference latency
if those are claimed.

## Stage 4-AU2 risk model metadata audit

`experiments/protocols/stage4au2_risk_model_metadata_audit.md` records the
Paper 1 RA-L metadata audit for the local generated risk model JSON artifacts.
It is documentation-only: it does not train models, modify
`experiments/models/`, modify `experiments/datasets/`, run ROS, compile
LaTeX, or create `risk_adapter_v22`.

Stage 4-AU2 confirms that the local ignored JSON files exist for the 3s, 5s,
and 15s models. The audited 3s and 5s Paper 1 risk-score artifacts are
`LogisticRegression` JSON exports trained on `label_strict_invalid` with 90
rows, class counts `0=51` and `1=39`, and feature counts 16 and 27. The audit
also records that no deployed calibration transform, confidence / OOD
mechanism, inference-latency measurement, embedded export timestamp, or
artifact checksum was found. Stage 4-AU3 now records local checksums for these
generated artifacts.

## Stage 4-AU3 risk model artifact manifest

`experiments/protocols/stage4au3_risk_model_artifact_manifest.md` records the
Paper 1 RA-L reproducibility manifest for generated local risk model and
dataset artifacts. It records file sizes and SHA256 checksums for
`experiments/models/stage4_risk_logreg_3s.json`,
`experiments/models/stage4_risk_logreg_5s.json`,
`experiments/models/stage4_risk_logreg_15s.json`, and
`experiments/datasets/stage4_risk_dataset.csv`.

Stage 4-AU3 is documentation-only: it does not train models, modify
`experiments/models/`, modify `experiments/datasets/`, run ROS, compile
LaTeX, or create `risk_adapter_v22`. The generated artifacts remain ignored
and untracked; final RA-L submission should archive them or provide a
regeneration path. The next recommended stage is Stage 4-AV RA-L template
acquisition / conversion.

## Stage 4-AL final figure generation plan

`experiments/protocols/stage4al_final_figure_generation_plan.md` records the
final paper figure/table generation plan for the assembled Stage 4 paper.

The plan maps Table 1 and Figures 1-6 to their source assets, source
generators, paper claims, caveats, formatting requirements, and missing
asset risks. It does not generate figures, run figure scripts, or create
paper-ready output files.

Stage 4-AL2 now records the paper figure package generator, Stage 4-AN records
the manual schematic specification, Stage 4-AN2 records the schematic
generator, and Stage 4-AL3 refreshes the figure package after schematic
generation. Stage 4-AM2 now records the verified citation collection result.
The next writing step after AM2 is Stage 4-AM3 BibTeX drafting / citation
insertion plan or Stage 4-AO manuscript formatting plan. Do not create
`risk_adapter_v22` yet.

## Stage 4-AL2 paper figure package generator

`experiments/scripts/create_stage4_paper_figure_package.py` assembles existing
Stage 4 generated assets into a clean paper figure package directory.

Default behavior is copy/check only: it does not regenerate source assets,
does not run simulation, and does not create new experimental evidence. It
copies available main-paper assets, copies available supplementary summaries,
detects generated Figure 1 and Figure 2 schematic files when present, writes
TODO files only when those schematics are missing, and writes manifest
CSV/Markdown plus a package summary.

Example command:

```bash
python3 experiments/scripts/create_stage4_paper_figure_package.py \
  --output-dir experiments/results/stage4_paper_figure_package \
  --print-summary
```

Generated outputs under `experiments/results/stage4_paper_figure_package/`
must not be committed. Stage 4-AN2 now records the schematic generator and
Stage 4-AL3 refreshes the package manifest after schematic generation. The next
writing step after AM2 is Stage 4-AM3 BibTeX drafting / citation insertion
plan or Stage 4-AO manuscript formatting plan. Do not create
`risk_adapter_v22` yet.

## Stage 4-AN manual schematic specification

`experiments/protocols/stage4an_manual_schematic_spec.md` specifies the manual
drawing requirements for Figure 1 and Figure 2.

Figure 1 should show the stack-compatible risk-conditioned execution governor,
the unchanged AutoTrans-like planner / payload MPC / SO3 controller stack, and
the `speed_scale` / `acceleration_scale` command-adaptation interface. Figure
2 should show the protocol split between the single-goal mission protocol
(`goal_repeat=1`) and the goal-reissue stress protocol (`goal_repeat=10`).

No schematic image files are created by Stage 4-AN. Stage 4-AN2 now implements
the deterministic schematic generator, Stage 4-AL3 refreshes the figure
package, and Stage 4-AM2 records verified citations. The next writing step is
Stage 4-AM3 BibTeX drafting / citation insertion plan or Stage 4-AO manuscript
formatting plan. Do not create `risk_adapter_v22` yet.

## Stage 4-AN2 manual schematic generator

`experiments/scripts/generate_stage4_manual_schematics.py` generates
paper-ready Figure 1 and Figure 2 schematic PNG/SVG files from the Stage 4-AN
manual schematic specification.

The script is deterministic and offline. It uses `matplotlib` only, does not
use ROS, does not run simulation, and does not create new experimental
evidence. Figure 1 shows the stack-compatible execution-governor architecture
with `speed_scale` and `acceleration_scale`; Figure 2 shows the protocol split
between `goal_repeat=1` and `goal_repeat=10`.

Example command:

```bash
python3 experiments/scripts/generate_stage4_manual_schematics.py \
  --output-dir experiments/results/stage4_paper_figure_package/main \
  --print-summary
```

Generated PNG/SVG/Markdown outputs under
`experiments/results/stage4_paper_figure_package/main/` must not be committed.
Stage 4-AL3 refreshes the paper figure package after schematic generation, and
Stage 4-AM2 records verified citations. The next writing step is Stage 4-AM3
BibTeX drafting / citation insertion plan or Stage 4-AO manuscript formatting
plan. Do not create `risk_adapter_v22` yet.

## Stage 4-AL3 paper figure package refresh

`experiments/scripts/create_stage4_paper_figure_package.py` now refreshes the
paper figure package after Stage 4-AN2 schematic generation.

When these files already exist, the package manifest records them as real
main-paper assets:

- `experiments/results/stage4_paper_figure_package/main/fig1_architecture.png`
- `experiments/results/stage4_paper_figure_package/main/fig1_architecture.svg`
- `experiments/results/stage4_paper_figure_package/main/fig2_protocol_split.png`
- `experiments/results/stage4_paper_figure_package/main/fig2_protocol_split.svg`

If the schematic files are missing, the generator keeps the Figure 1 / Figure
2 TODO fallback behavior. The default path remains copy/check only; it does not
call `experiments/scripts/generate_stage4_manual_schematics.py` automatically.

Example command:

```bash
python3 experiments/scripts/create_stage4_paper_figure_package.py \
  --output-dir experiments/results/stage4_paper_figure_package \
  --print-summary
```

Generated manifest and summary outputs under
`experiments/results/stage4_paper_figure_package/` must not be committed. The
next step after AM2 is Stage 4-AM3 BibTeX drafting / citation insertion plan
or Stage 4-AO manuscript formatting plan. Do not create `risk_adapter_v22`
yet.

## Stage 4-AJ full paper assembly draft

`experiments/protocols/stage4aj_full_paper_assembly_draft.md` records the
current full paper assembly draft for the reframed IROS/ICRA/RA-L style paper.

The draft assembles the current Abstract / Introduction, Related Work
skeleton, Method, Experimental Setup, Results, Discussion / Limitations,
Conclusion, main figure/table checklist, appendix plan, master claim audit,
and paper readiness checklist. It keeps `risk_adapter_v1` as the balanced
learned / risk-conditioned protagonist, presents `windlevel_s085` and
`fixed_s080` as protocol specialists, and keeps `risk_adapter_v21` as a strong
nominal / single-goal variant or ablation.

## Stage 4-AK citation references plan

`experiments/protocols/stage4ak_citation_references_plan.md` records the
citation / reference planning document for the assembled Stage 4 paper.

The plan maps paper sections, Related Work topics, claims, and non-citation
technical gaps to explicit TODO citation slots. It does not finalize the
bibliography, does not generate BibTeX, and should not be used to replace TODO
placeholders with unverified references.

Stage 4-AM now records the citation collection workflow, Stage 4-AL now
records the final figure generation plan, Stage 4-AL2 now records the paper
figure package generator, and Stage 4-AN now records the manual schematic
specification. The next writing step after AN is Stage 4-AM2 verified citation
collection or Stage 4-AN2 manual schematic creation. Do not create
`risk_adapter_v22` yet.

## Stage 4-AB paper reframing decision

`experiments/protocols/stage4ab_paper_reframing_decision.md` records the paper
reframing after the completed protocol-split comparison and failure-mode
analysis.

Stage 4-AB moves the paper away from a `risk_adapter_v21`-as-winner narrative.
The tentative protagonist is `risk_adapter_v1` as the most balanced learned /
risk-conditioned execution governor. `risk_adapter_v21` should be treated as a
strong nominal variant / ablation, while `windlevel_s085` and `fixed_s080`
should be presented as strong protocol-specialist baselines.

The Stage 4-AB table tracks single-goal count, stress count, mean count,
worst-protocol count, and total regret relative to the protocol oracle. The
Stage 4-AA3 representative trace review did not justify immediate
`risk_adapter_v22`; Stage 4-AC2 now records the balanced robustness / protocol
regret result. Stage 4-AD now freezes the figure/table plan, Stage 4-AG
records the Method draft, and Stage 4-AH records the Results section draft.
Stage 4-AI records the Discussion and Limitations draft, Stage 4-AJ records the
full paper assembly draft, Stage 4-AK records the citation / references plan,
Stage 4-AM records the citation collection workflow, Stage 4-AL records the
final figure generation plan, Stage 4-AL2 records the paper figure package
generator, and Stage 4-AN records the manual schematic specification. The next
writing step is Stage 4-AM2 verified citation collection or Stage 4-AN2 manual
schematic creation.

## Stage 4-X0 final evaluation specification

`experiments/protocols/stage4x_final_evaluation_spec.md` freezes the final
protocol-split evaluation plan before more experiments or variants.

Current status:

- Stage 4-X1 completed the goal-reissue stress protocol cell for
  `risk_adapter_v21`.
- Stage 4-X2 completed the missing single-goal mission baselines:
  `original`, `fixed_s085`, `windlevel_s085`, and `risk_adapter_v1`.
- The next step is to update the protocol-split paper assets.

Next order:

1. Completed in Stage 4-X1: run `risk_adapter_v21` under the goal-reissue
   stress protocol (`goal_repeat=10`).
2. Completed in Stage 4-X2: run the missing single-goal baselines under
   `goal_repeat=1`.
3. Next: update the protocol-split paper assets.
4. Decide the final method.

Do not create `risk_adapter_v21.1`, `risk_adapter_v22`, or another new variant
before the protocol-split paper assets and failure analysis are updated.

## Stage 4-X1 corrected risk_adapter_v21 goal-reissue result

`experiments/protocols/stage4x_risk_adapter_v21_goalreissue_result.md`
records the corrected `risk_adapter_v21` goal-reissue stress result.

A duplicate CSV issue was found in Trial 4 repeat2-5. Trial 4 repeat3-5 were
rerun, and the corrected set was recorded after confirming `No duplicate
csv_path detected`.

Corrected goal-reissue stress result:

| Method | Strict-valid count |
| --- | ---: |
| `fixed_s080` | `24/30` |
| `risk_adapter_v1` | `23/30` |
| `risk_adapter_v21` | `20/30` |
| `original` | `18/30` |
| `fixed_s085` | `18/30` |
| `windlevel_s085` | `16/30` |

`risk_adapter_v21` per-trial counts are Trial 4 `4/10`, Trial 5 `9/10`, and
Trial 6 `7/10`. Stage 4-X2 later showed `risk_adapter_v21` is not the
completed single-goal aggregate winner; it tied `risk_adapter_v1` at `25/30`
and was below `windlevel_s085` at `26/30`. It is not the strongest
goal-reissue stress method and should not be described as a cross-protocol
final winner.

## Stage 4-X2 single-goal baseline completion result

`experiments/scripts/run_stage4_single_goal_baseline_completion.py` generates
the command plan for completing the missing single-goal mission baselines:

- `original`
- `fixed_s085`
- `windlevel_s085`
- `risk_adapter_v1`

Protocol:

- strong wind
- `goal_repeat=1`
- Trial 4, Trial 5, Trial 6
- repeat1 through repeat10
- strict-valid / `label_strict_invalid` as the paper-facing metric

Default behavior is dry-run / print-only. The script does not execute ROS
simulation unless `--execute` is explicitly provided.

Dry-run examples:

```bash
python3 experiments/scripts/run_stage4_single_goal_baseline_completion.py \
  --method original \
  --trials 4 5 6 \
  --repeats 1 2 3 \
  --dry-run \
  --print-commands

python3 experiments/scripts/run_stage4_single_goal_baseline_completion.py \
  --method risk_adapter_v1 \
  --trials 4 \
  --repeats 1 \
  --dry-run \
  --print-commands
```

For `windlevel_s085`, start:

```bash
roslaunch command_adaptation heuristic_command_adapter.launch policy_mode:=wind_level
```

For `risk_adapter_v1`, start:

```bash
roslaunch command_adaptation risk_conditioned_command_adapter.launch \
  enable_risk_conditioning:=true \
  policy_mode:=risk_conditioned \
  risk_threshold_3s:=0.5 \
  risk_threshold_5s:=0.5 \
  hard_threshold_5s:=0.7 \
  soft_scale_3s:=0.75 \
  soft_scale_5s:=0.65 \
  hard_scale_5s:=0.60 \
  scale_rate_limit_per_sec:=0.5
```

The protocol is
`experiments/protocols/stage4x_single_goal_baseline_completion_protocol.md`.
The completed result is recorded in
`experiments/protocols/stage4x_single_goal_baseline_completion_result.md`.

Completed single-goal mission results:

| Method | Trial 4 | Trial 5 | Trial 6 | Aggregate |
| --- | ---: | ---: | ---: | ---: |
| `original` | `6/10` | `8/10` | `7/10` | `21/30` |
| `fixed_s085` | `5/10` | `9/10` | `8/10` | `22/30` |
| `windlevel_s085` | `8/10` | `9/10` | `9/10` | `26/30` |
| `fixed_s080` | `7/10` | `6/10` | `8/10` | `21/30` |
| `risk_adapter_v1` | `9/10` | `9/10` | `7/10` | `25/30` |
| `risk_adapter_v2` | `9/10` | `6/10` | `6/10` | `21/30` |
| `risk_adapter_v21` | `10/10` | `9/10` | `6/10` | `25/30` |

`windlevel_s085` is now the strongest completed single-goal aggregate at
`26/30`. `risk_adapter_v1` and `risk_adapter_v21` tie at `25/30`.
`risk_adapter_v21` should not be claimed as the best single-goal method or as
beating all baselines. Do not create a new method variant before updating the
protocol-split paper assets and doing failure analysis.

## Stage 4-C risk dataset expansion

Stage 4-C 的下一步是把当前 15-row strong Trial 2 dataset 扩展到至少 45 rows，优先增加 Trial 1 和 Trial 3 的 `original`、`fixed_s085`、`windlevel_s085` repeats。执行前先看计划文档：`experiments/protocols/stage4_risk_dataset_expansion_plan.md`。

## Stage 4-E target diversity expansion

Stage 4-D group-CV 和 feature-ablation 结果显示 `leave-one-target-out` generalization 仍然偏弱。进入 risk-conditioned policy learning 前，先按 `experiments/protocols/stage4e_target_diversity_expansion_protocol.md` 将 dataset 从 45 rows 扩展到 90 rows，并增加 Trial 4、Trial 5、Trial 6 的 target diversity。

## 查看生成结果

CSV logs:

```bash
ls -lh ~/projects/autotrans_ws/src/AutoTrans/experiments/logs
latest=$(ls -t ~/projects/autotrans_ws/src/AutoTrans/experiments/logs/autotrans_log_*.csv | head -1)
head -5 "$latest"
```

Analysis figures and metrics:

```bash
ls -lh ~/projects/autotrans_ws/src/AutoTrans/experiments/figures
cat ~/projects/autotrans_ws/src/AutoTrans/experiments/figures/metrics_summary.txt
```

生成的 CSV、PNG、TXT 已由 `.gitignore` 忽略，不应提交到 git。

## 如果 /move_base_simple/goal 不工作

按以下顺序排查：

1. 先手动运行 `roslaunch payload_planner simple_run.launch`，确认 RViz 中 `2D Nav Goal` 可以触发规划。
2. 检查 topic 是否存在：

```bash
rostopic list | grep /move_base_simple/goal
```

3. 检查 planner 是否仍在等待 odometry 或 target。
4. 检查 goal 的 `frame_id` 是否为 `world`。
5. 如果手动 RViz goal 有效但脚本无效，先单独测试：

```bash
rostopic pub -1 /move_base_simple/goal geometry_msgs/PoseStamped "header:
  stamp: now
  frame_id: 'world'
pose:
  position:
    x: 0.0
    y: -1.2
    z: 0.0
  orientation:
    x: 0.0
    y: 0.0
    z: 0.0
    w: 1.0"
```

如果 automated run 仍明显偏离手动 RViz run，重点检查：

- `/move_base_simple/goal` 是否至少有 `payload_planner_node` subscriber。
- `/pcl_render_node/cloud` 是否稳定发布，说明 map/local sensing 已准备好。
- `/visual_slam/odom` 和 `/payload_odom` 是否已经稳定，且位置没有异常跳变。
- `/so3cmd` 是否已经有控制命令输出。
- 手动 RViz `2D Nav Goal` 在同一 target point 是否仍然有效。
- 是否选择了过远、穿越密集障碍或超出地图边界的 target point。

## 使用前提

只在以下条件满足后使用本脚本：

- `catkin_make -DCMAKE_BUILD_TYPE=Release` 已成功。
- 手动 `roslaunch payload_planner simple_run.launch` 已验证。
- RViz 手动 `2D Nav Goal` 已验证可以触发规划和仿真响应。
- `autotrans_logger` 和 `analyze_log.py` 已验证可用。

不要用它替代首次部署验证。首次部署仍应按手动 RViz demo 流程确认系统状态。
