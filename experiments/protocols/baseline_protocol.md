# AutoTrans Baseline Experiment Protocol

## 1. 实验目的

baseline experiment 的目标是在不加入 wind disturbance、不修改 planner、controller、simulator 核心逻辑的前提下，记录 `roslaunch payload_planner simple_run.launch` demo 的标准运行表现。

这些数据用于后续对比：

- 原始 payload swing 水平。
- 原始 UAV/payload 速度与路径长度。
- 原始 `payload_mpc_controller` 跟踪行为。
- 后续加入 wind disturbance、residual disturbance observer、learned prior 或 planner cost 修改后的变化。

在完成稳定 baseline 前，不建议修改算法逻辑。

## 2. 环境假设

- OS: Ubuntu 20.04 WSL
- ROS: Noetic
- Workspace root: `~/projects/autotrans_ws`
- Repository root: `~/projects/autotrans_ws/src/AutoTrans`
- Branch: `autotrans-deploy`
- `catkin_make -DCMAKE_BUILD_TYPE=Release` 已成功。
- `roslaunch payload_planner simple_run.launch` 可正常启动 RViz。
- RViz 中 `2D Nav Goal` 可触发规划和仿真响应。
- 已安装并可运行 `autotrans_logger`。

每次实验前建议记录：

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
git branch --show-current
git rev-parse HEAD
git status --short
```

只有 `git status --short` 没有未提交代码改动时，才建议作为正式 baseline 数据。

## 3. 构建命令

如果刚拉取代码或新增了 `autotrans_logger` package，先构建：

```bash
cd ~/projects/autotrans_ws
source /opt/ros/noetic/setup.bash
source devel/setup.bash 2>/dev/null || true
catkin_make -DCMAKE_BUILD_TYPE=Release
```

## 4. 启动 simple_run.launch

Terminal 1:

```bash
cd ~/projects/autotrans_ws
source /opt/ros/noetic/setup.bash
source devel/setup.bash
roslaunch payload_planner simple_run.launch
```

等待 RViz 打开，并确认：

- RViz Fixed Frame 为 `world`。
- 地图点云 `/map_generator/global_cloud` 可见。
- 仿真状态 `/vis` 可见。
- 终端没有持续刷屏的 fatal/error。

## 5. 启动 autotrans_logger

Terminal 2:

```bash
cd ~/projects/autotrans_ws
source /opt/ros/noetic/setup.bash
source devel/setup.bash
roslaunch autotrans_logger state_logger.launch
```

logger 会自动创建 CSV：

```text
~/projects/autotrans_ws/src/AutoTrans/experiments/logs/autotrans_log_YYYYMMDD_HHMMSS.csv
```

建议在每次 trial 开始前启动 logger，trial 结束后停止 logger。这样每个 CSV 对应一次清晰实验。

## 6. 使用 RViz 2D Nav Goal

在 RViz 中：

1. 点击顶部工具栏的 `2D Nav Goal`。
2. 在地图平面上点击目标位置。
3. 拖动鼠标设置 yaw 方向后松开。
4. 观察 planner 是否生成轨迹、UAV/payload 是否开始运动。

当前 demo 中，`2D Nav Goal` 发布到：

```text
/move_base_simple/goal
```

`payload_planner_node` 会消费该 topic，并把目标高度设置为 launch 中的第一个 waypoint 高度。

## 7. 推荐 baseline trials

建议至少做 3 次 baseline trial。每次启动新的 logger，生成独立 CSV。

| trial | 推荐 target point | 目的 |
|---|---:|---|
| Trial 1 | `(0.0, -1.2)` | 短距离、低风险，用于确认 logging 和分析链路正常 |
| Trial 2 | `(5.0, -1.5)` | 中距离横向移动，观察基本 payload swing |
| Trial 3 | `(-7.0, 1.5)` | 长距离穿越场景，观察较大速度变化和 swing 峰值 |

如果地图随机障碍导致某个点不可达，可以选择附近无障碍点，但必须在结果模板中记录实际 target point。

## 8. 推荐运行时长

每个 trial 建议记录：

- 最短：`60 s`
- 推荐：`90–180 s`
- 如果 UAV/payload 还未稳定到目标附近，可以延长到 `240 s`

记录时间应覆盖：

1. logger 启动后的静止阶段。
2. RViz `2D Nav Goal` 触发后的规划阶段。
3. UAV/payload 执行轨迹阶段。
4. 到达目标后短暂停留阶段。

## 9. 安全停止 logger

在 Terminal 2 中按：

```text
Ctrl-C
```

`state_logger.py` 会 flush 并关闭 CSV 文件。停止后检查 CSV 是否生成：

```bash
ls -lh ~/projects/autotrans_ws/src/AutoTrans/experiments/logs
```

不要手动编辑 CSV。不要把生成的 CSV 提交到 git。

## 10. 运行 analyze_log.py

默认分析最新 CSV：

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/autotrans_logger/scripts/analyze_log.py
```

分析指定 CSV：

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
python3 experiments/autotrans_logger/scripts/analyze_log.py \
  --csv experiments/logs/autotrans_log_YYYYMMDD_HHMMSS.csv \
  --output_dir experiments/figures
```

输出包括：

- `experiments/figures/metrics_summary.txt`
- `experiments/figures/swing_angle.png`
- `experiments/figures/xy_trajectory.png`
- `experiments/figures/altitude.png`
- `experiments/figures/speed.png`
- `experiments/figures/thrust_bodyrate.png`

不要把生成的 PNG/TXT 提交到 git。

## 11. 必须记录的 metrics

每次 trial 至少记录以下指标到 `experiments/protocols/baseline_result_template.md` 的副本中：

- `csv_path`
- `sample_count`
- `duration_sec`
- `effective_log_rate_hz`
- `has_trajectory_ratio`
- `mean_swing_angle_deg`
- `max_swing_angle_deg`
- `p95_swing_angle_deg`
- `max_uav_speed`
- `mean_uav_speed`
- `max_payload_speed`
- `mean_payload_speed`
- `uav_path_length`
- `payload_path_length`
- `final_uav_position`
- `final_payload_position`

同时记录 RViz 观察：

- 是否成功规划。
- 是否有明显绕障。
- payload 是否出现大幅摆动。
- 是否有异常停顿、跳变、碰撞或 RViz 卡死。

## 12. swing_angle_deg 解释

`swing_angle_deg` 表示 cable vector 与竖直向下方向之间的夹角：

```text
cable vector = payload position - UAV position
vertical downward direction = (0, 0, -1)
```

解释建议：

- 接近 `0 deg`：payload 基本在 UAV 正下方，摆动很小。
- `5–10 deg`：有可见轻中等摆动，baseline 中可接受但要记录。
- `10–20 deg`：摆动明显，后续 disturbance 或 controller 修改时应重点关注。
- 大于 `20 deg`：摆动较大，需要检查是否目标过激、速度过高、轨迹绕障剧烈或仿真状态异常。

注意：`swing_angle_deg` 是几何角度，不直接等于控制误差。它适合作为 payload swing risk 的 baseline 指标。

## 13. 有效 run 判定

一次 run 建议满足以下条件才标记为 valid：

- `sample_count > 1000`。
- `duration_sec >= 60`。
- `effective_log_rate_hz` 接近 logger 设置值，默认约 `20 Hz`，建议不低于 `15 Hz`。
- `has_trajectory_ratio > 0.1`，说明至少有一段时间接收到 planner trajectory。
- `mean_swing_angle_deg`、`max_swing_angle_deg`、速度和路径长度不是 `nan`。
- RViz 中 UAV/payload 有实际运动响应。
- 没有明显 simulator crash、ROS node crash、RViz 完全卡死或严重 topic 中断。

如果 run invalid，仍可保留本地 CSV 作调试，但不要纳入正式 baseline 对比。

## 14. 推荐命名和记录方式

建议每个 trial 复制一份模板：

```bash
cd ~/projects/autotrans_ws/src/AutoTrans
cp experiments/protocols/baseline_result_template.md \
  experiments/protocols/baseline_result_YYYYMMDD_trial1.md
```

然后填写实际结果。正式对比时，优先比较同一 branch、同一 commit、同一 target point 的 runs。
