# AutoTrans Codex Instructions

请用中文回答，但保留所有文件路径、函数名、变量名、包名、topic 名称、launch 文件名和命令为英文原样。

## Project Context

This project is HKUST-Aerial-Robotics/AutoTrans, deployed as a ROS1 catkin workspace.

Environment:
- OS: Ubuntu 20.04 WSL
- ROS: Noetic
- Workspace root: ~/projects/autotrans_ws
- Repository root: ~/projects/autotrans_ws/src/AutoTrans
- Current working branch: autotrans-deploy
- Main demo launch command:
  cd ~/projects/autotrans_ws
  source /opt/ros/noetic/setup.bash
  source devel/setup.bash
  roslaunch payload_planner simple_run.launch

Deployment status:
- ROS Noetic is installed successfully.
- catkin_make -DCMAKE_BUILD_TYPE=Release succeeds.
- RViz opens successfully.
- roslaunch payload_planner simple_run.launch starts successfully.
- 2D Nav Goal in RViz triggers planning and simulation response.
- The current GitHub remote branch autotrans-deploy exists.

## Important Paths

Workspace:
- ~/projects/autotrans_ws

Repository:
- ~/projects/autotrans_ws/src/AutoTrans

Build output:
- ~/projects/autotrans_ws/build

Devel environment:
- ~/projects/autotrans_ws/devel

Do not modify generated files under:
- ~/projects/autotrans_ws/build
- ~/projects/autotrans_ws/devel
- ~/projects/autotrans_ws/install

## Important Packages

payload_planner:
- ROS package path: ~/projects/autotrans_ws/src/AutoTrans/planner/plan_manage
- Main role: payload-aware planning / runtime planner management

payload_mpc_controller:
- ROS package path: ~/projects/autotrans_ws/src/AutoTrans/controller/payload_mpc_controller
- Main role: payload-aware MPC control

so3_quadrotor:
- ROS package path: ~/projects/autotrans_ws/src/AutoTrans/uav_simulator/so3_quadrotor
- Main role: quadrotor simulation / dynamics interface

local_sensing_node:
- ROS package path: ~/projects/autotrans_ws/src/AutoTrans/uav_simulator/local_sensing
- Main role: local sensing / environment perception simulation

rviz_plugins:
- ROS package path: ~/projects/autotrans_ws/src/AutoTrans/Utils/rviz_plugins
- Main role: RViz visualization plugins

## Build Command

Use this command to build the full workspace:

cd ~/projects/autotrans_ws
source /opt/ros/noetic/setup.bash
source devel/setup.bash 2>/dev/null || true
catkin_make -DCMAKE_BUILD_TYPE=Release

If saving logs:

cd ~/projects/autotrans_ws
source /opt/ros/noetic/setup.bash
source devel/setup.bash 2>/dev/null || true
catkin_make -DCMAKE_BUILD_TYPE=Release 2>&1 | tee build_autotrans.log

## Run Command

Use this command to run the main demo:

cd ~/projects/autotrans_ws
source /opt/ros/noetic/setup.bash
source devel/setup.bash
roslaunch payload_planner simple_run.launch

## Rules for Codex

1. Always read this AGENTS.md first.
2. For read-only tasks, do not modify files.
3. For edit tasks, first inspect relevant files and propose a minimal edit plan.
4. Do not modify generated files under build/, devel/, or install/.
5. Do not change core algorithm logic unless explicitly requested.
6. Prefer small, reversible changes.
7. After editing, report:
   - exact changed files
   - why each file was changed
   - verification command
8. Keep explanations beginner-friendly.
9. Preserve all file paths, function names, variable names, package names, topic names, and commands in English.
10. Do not run long simulations unless explicitly requested.

## Research Direction

The intended research use of this project is not merely reproducing the demo. The goal is to turn AutoTrans into a benchmark and research platform for:

- cable-suspended payload UAV planning
- payload-aware MPC
- disturbance-aware planning and control
- wind disturbance simulation
- payload swing logging and metrics
- residual disturbance observer
- learned disturbance or swing-risk prior

Future modification candidates:
- Add wind disturbance into simulator or controller interface.
- Add logging for UAV state, payload state, control input, reference trajectory, odometry, and swing angle.
- Add metrics for tracking error, maximum swing angle, average swing angle, success rate, collision rate, control effort, and computation time.
- Modify payload_mpc_controller for residual disturbance compensation.
- Modify planner cost function for payload swing risk or disturbance-aware trajectory generation.
- Add learned prior only after baseline logging and metrics are stable.

## Pre-Codex Checkpoint

Before any edit task, run:

cd ~/projects/autotrans_ws/src/AutoTrans
tools/pre_codex_checkpoint.sh
git branch --show-current
git rev-parse HEAD

Only proceed with edit tasks if the working tree is clean.
