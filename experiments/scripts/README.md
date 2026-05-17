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

The generated summary uses "among evaluated methods" wording because the
method set differs between the two protocols.

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
