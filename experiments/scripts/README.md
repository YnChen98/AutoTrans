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
