cmake_minimum_required(VERSION 3.0.2)
project(command_adaptation)

find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  nav_msgs
  rospy
  std_msgs
)

catkin_package()

catkin_install_python(PROGRAMS
  scripts/heuristic_command_adapter.py
  scripts/risk_conditioned_command_adapter.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY launch
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
