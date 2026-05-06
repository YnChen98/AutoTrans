
#pragma once

#include <stdlib.h>
#include <string>

#include <optimizer/poly_traj_optimizer.h>
#include <traj_utils/DataDisp.h>
#include <plan_env/grid_map.h>
#include <optimizer/plan_container.hpp>
#include <ros/ros.h>
#include <plan_manage/planning_visualization.h>
#include <optimizer/poly_traj_utils.hpp>
#include <std_msgs/Float64.h>
#include <sstream>

namespace payload_planner
{

  // Planner Manager
  // Key algorithms of mapping and planning are called in this class

  class PlannerManager
  {
  public:
  
    PlannerManager();
    ~PlannerManager();

    EIGEN_MAKE_ALIGNED_OPERATOR_NEW
    
    /* main planning interface */
    bool reboundReplan(
        const Eigen::Vector3d &start_pt, const Eigen::Vector3d &start_vel, const Eigen::Vector3d &start_acc, const Eigen::Vector3d &start_jerk ,
        const double trajectory_start_time, const Eigen::Vector3d &end_pt, const Eigen::Vector3d &end_vel ,const Eigen::Vector3d &end_acc, 
        const bool flag_polyInit, const bool have_local_traj);
    bool computeInitReferenceState(
        const Eigen::Vector3d &start_pt, const Eigen::Vector3d &start_vel, 
        const Eigen::Vector3d &start_acc, const Eigen::Vector3d &start_jerk , const Eigen::Vector3d &local_target_pt,
        const Eigen::Vector3d &local_target_vel,const Eigen::Vector3d &local_target_acc, const double &ts, poly_traj::MinSnapOpt &initMJO,
        const bool flag_polyInit);
    bool planGlobalTrajWaypoints(
        const Eigen::Vector3d &start_pos, const Eigen::Vector3d &start_vel, 
        const Eigen::Vector3d &start_acc, const std::vector<Eigen::Vector3d> &waypoints, 
        const Eigen::Vector3d &end_vel, const Eigen::Vector3d &end_acc);
    void getLocalTarget(
        const double planning_horizen,
        const Eigen::Vector3d &start_pt, const Eigen::Vector3d &global_end_pt,
        Eigen::Vector3d &local_target_pos, Eigen::Vector3d &local_target_vel,Eigen::Vector3d &local_target_acc);
    void initPlanModules(ros::NodeHandle &nh, PlanningVisualization::Ptr vis = NULL);
    bool EmergencyStop(Eigen::Vector3d stop_pos);
    double effectiveMaxVel() const;
    double effectiveMaxAcc() const;
    bool commandAdaptationReady() const;
    std::string commandAdaptationStatusString() const;

    PlanParameters pp_;
    GridMap::Ptr grid_map_;
    TrajContainer traj_;
    
    // ros::Publisher obj_pub_; //zx-todo

    PolyTrajOptimizer::Ptr ploy_traj_opt_;

    bool start_flag_, reach_flag_;
    ros::Time global_start_time_;
    double start_time_, reach_time_, average_plan_time_;

  private:
    /* main planning algorithms & modules */
    PlanningVisualization::Ptr visualization_;

    int continous_failures_count_{0};
    bool enable_command_adaptation_{false};
    bool require_adaptation_topic_ready_{false};
    std::string adaptation_mode_{"none"};
    double speed_scale_{1.0};
    double acceleration_scale_{1.0};
    bool speed_scale_topic_received_{false};
    bool acceleration_scale_topic_received_{false};
    ros::Subscriber speed_scale_sub_;
    ros::Subscriber acceleration_scale_sub_;

    double clampAdaptationScale(double value) const;
    bool isCommandAdaptationActive() const;
    void speedScaleCallback(const std_msgs::Float64::ConstPtr &msg);
    void accelerationScaleCallback(const std_msgs::Float64::ConstPtr &msg);

  public:
    typedef unique_ptr<PlannerManager> Ptr;

    // !SECTION
  };
} // namespace payload_planner
