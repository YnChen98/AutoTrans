# AutoTrans Codex Instructions

请用中文回答，但保留所有文件路径、函数名、变量名、包名、topic 名称、launch 文件名和命令为英文原样。

Project context:
- This is HKUST-Aerial-Robotics/AutoTrans.
- It is a ROS1 catkin workspace project.
- OS: Ubuntu 20.04 WSL
- ROS: Noetic
- Workspace root: ~/projects/autotrans_ws
- Repository root: ~/projects/autotrans_ws/src/AutoTrans
- Main demo command:
  cd ~/projects/autotrans_ws
  source devel/setup.bash
  roslaunch payload_planner simple_run.launch

Deployment status:
- The project has already built successfully with catkin_make.
- RViz opens successfully.
- 2D Nav Goal triggers planning/simulation response.

Rules:
1. Always read this AGENTS.md first.
2. Do not edit files unless explicitly asked.
3. For read-only tasks, inspect code and explain structure without modifications.
4. For edit tasks, first inspect relevant files and propose a minimal edit plan.
5. Do not modify generated files under ~/projects/autotrans_ws/build or ~/projects/autotrans_ws/devel.
6. Do not rewrite algorithm logic unless explicitly requested.
7. Prefer small, reversible changes.
8. After any edit, report the exact changed files and give the next terminal command to verify.
9. Keep explanations beginner-friendly.

Important packages:
- payload_planner is located at planner/plan_manage.
- payload_mpc_controller is located at controller/payload_mpc_controller.
- so3_quadrotor is located at uav_simulator/so3_quadrotor.
- local_sensing_node is located at uav_simulator/local_sensing.
- rviz_plugins is located at Utils/rviz_plugins.

Build command:
cd ~/projects/autotrans_ws
source /opt/ros/noetic/setup.bash
source devel/setup.bash 2>/dev/null || true
catkin_make -DCMAKE_BUILD_TYPE=Release

Run command:
cd ~/projects/autotrans_ws
source devel/setup.bash
roslaunch payload_planner simple_run.launch
