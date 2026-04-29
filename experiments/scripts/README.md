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
