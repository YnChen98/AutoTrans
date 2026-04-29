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

## Trial 1 示例命令

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
bash experiments/scripts/run_baseline_trial.sh --name trial1 --x 0.0 --y -1.2 --z 1.0 --duration 75
```

默认参数：

- `--name baseline_trial`
- `--x 0.0`
- `--y -1.2`
- `--z 1.0`
- `--duration 75`
- `--frame_id world`

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
  stamp:
    secs: 0
    nsecs: 0
  frame_id: 'world'
pose:
  position:
    x: 0.0
    y: -1.2
    z: 1.0
  orientation:
    x: 0.0
    y: 0.0
    z: 0.0
    w: 1.0"
```

## 使用前提

只在以下条件满足后使用本脚本：

- `catkin_make -DCMAKE_BUILD_TYPE=Release` 已成功。
- 手动 `roslaunch payload_planner simple_run.launch` 已验证。
- RViz 手动 `2D Nav Goal` 已验证可以触发规划和仿真响应。
- `autotrans_logger` 和 `analyze_log.py` 已验证可用。

不要用它替代首次部署验证。首次部署仍应按手动 RViz demo 流程确认系统状态。
