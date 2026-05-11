#!/usr/bin/env python3

import csv
import math
import os
import time
from datetime import datetime

import rospy
import rospkg
from geometry_msgs.msg import Vector3Stamped
from mavros_msgs.msg import AttitudeTarget
from nav_msgs.msg import Odometry
from nav_msgs.msg import Path as NavPath
from quadrotor_msgs.msg import PolynomialTraj
from sensor_msgs.msg import Imu
from std_msgs.msg import Float64

try:
    from quadrotor_msgs.msg import PositionCommand
except ImportError:
    PositionCommand = None


class StateLogger:
    CSV_FIELDS = [
        "ros_time",
        "wall_time",
        "uav_pos_x",
        "uav_pos_y",
        "uav_pos_z",
        "uav_vel_x",
        "uav_vel_y",
        "uav_vel_z",
        "payload_pos_x",
        "payload_pos_y",
        "payload_pos_z",
        "payload_vel_x",
        "payload_vel_y",
        "payload_vel_z",
        "cable_orientation_x",
        "cable_orientation_y",
        "cable_orientation_z",
        "cable_orientation_w",
        "so3_thrust",
        "so3_bodyrate_x",
        "so3_bodyrate_y",
        "so3_bodyrate_z",
        "command_invalid_event",
        "command_invalid_reason",
        "command_saturation_event",
        "command_saturation_reason",
        "sustained_command_saturation_event",
        "guarded_command_applied",
        "swing_angle_deg",
        "has_trajectory",
        "ref_pos_x",
        "ref_pos_y",
        "ref_pos_z",
        "ref_vel_x",
        "ref_vel_y",
        "ref_vel_z",
        "ref_acc_x",
        "ref_acc_y",
        "ref_acc_z",
        "ref_yaw",
        "ref_yaw_dot",
        "ref_msg_ros_time",
        "ref_available",
        "wind_force_x",
        "wind_force_y",
        "wind_force_z",
        "wind_force_norm",
        "command_speed_scale",
        "command_acceleration_scale",
        "command_risk_score_3s",
        "command_risk_score_5s",
        "command_risk_scale_selected",
        "command_risk_target_scale_raw",
    ]

    def __init__(self):
        self.uav_odom = None
        self.payload_odom = None
        self.cable_info = None
        self.so3cmd = None
        self.wind_force = None
        self.command_speed_scale = None
        self.command_acceleration_scale = None
        self.command_risk_score_3s = None
        self.command_risk_score_5s = None
        self.command_risk_scale_selected = None
        self.command_risk_target_scale_raw = None
        self.has_trajectory = False
        self.reference_cmd = None

        self.enable_reference_logging = bool(rospy.get_param("~enable_reference_logging", True))
        self.reference_topic = rospy.get_param("~reference_topic", "/mpc_controller_node/mpc/all_ref_data")
        self.reference_message_type = rospy.get_param("~reference_message_type", "mpc_all_ref_data")
        self.reference_required = bool(rospy.get_param("~reference_required", False))
        self.thrust_saturation_threshold = float(rospy.get_param("~thrust_saturation_threshold", 59.9))
        self.bodyrate_xy_saturation_threshold = float(rospy.get_param("~bodyrate_xy_saturation_threshold", 2.99))
        self.bodyrate_z_saturation_threshold = float(rospy.get_param("~bodyrate_z_saturation_threshold", 1.19))
        self.sustained_saturation_duration_sec = float(
            rospy.get_param("~sustained_saturation_duration_sec", 0.2)
        )
        self.saturation_start_time = None

        self.log_path = self._make_log_path()
        self.csv_file = open(self.log_path, "w", newline="")
        self.writer = csv.DictWriter(self.csv_file, fieldnames=self.CSV_FIELDS)
        self.writer.writeheader()
        self.csv_file.flush()

        rospy.Subscriber("/visual_slam/odom", Odometry, self._uav_odom_callback, queue_size=50)
        rospy.Subscriber("/payload_odom", Odometry, self._payload_odom_callback, queue_size=50)
        rospy.Subscriber("/cable_info", Imu, self._cable_info_callback, queue_size=50)
        rospy.Subscriber("/so3cmd", AttitudeTarget, self._so3cmd_callback, queue_size=50)
        rospy.Subscriber("/planning/trajectory", PolynomialTraj, self._trajectory_callback, queue_size=10)
        self._subscribe_reference_command()
        rospy.Subscriber("/wind_force", Vector3Stamped, self._wind_force_callback, queue_size=50)
        rospy.Subscriber("/command_adaptation/speed_scale", Float64, self._command_speed_scale_callback, queue_size=50)
        rospy.Subscriber("/command_adaptation/acceleration_scale", Float64, self._command_acceleration_scale_callback, queue_size=50)
        rospy.Subscriber("/command_adaptation/risk_score_3s", Float64, self._command_risk_score_3s_callback, queue_size=50)
        rospy.Subscriber("/command_adaptation/risk_score_5s", Float64, self._command_risk_score_5s_callback, queue_size=50)
        rospy.Subscriber(
            "/command_adaptation/risk_scale_selected",
            Float64,
            self._command_risk_scale_selected_callback,
            queue_size=50,
        )
        rospy.Subscriber(
            "/command_adaptation/risk_target_scale_raw",
            Float64,
            self._command_risk_target_scale_raw_callback,
            queue_size=50,
        )

        log_rate = rospy.get_param("~log_rate", 20.0)
        self.timer = rospy.Timer(rospy.Duration(1.0 / max(log_rate, 1e-3)), self._timer_callback)
        rospy.on_shutdown(self.close)

        rospy.loginfo("autotrans_logger writing CSV to: %s", self.log_path)

    def _subscribe_reference_command(self):
        if not self.enable_reference_logging:
            rospy.loginfo("reference command logging disabled")
            return
        if self.reference_message_type == "mpc_all_ref_data":
            rospy.Subscriber(
                self.reference_topic,
                NavPath,
                self._reference_path_callback,
                queue_size=50,
            )
            rospy.loginfo("reference path logging enabled on topic: %s", self.reference_topic)
            return
        if self.reference_message_type != "position_command":
            message = "unsupported reference_message_type=%s; reference logging disabled" % (
                self.reference_message_type
            )
            if self.reference_required:
                rospy.logerr(message)
            else:
                rospy.logwarn(message)
            return
        if PositionCommand is None:
            message = "quadrotor_msgs/PositionCommand import failed; reference logging disabled"
            if self.reference_required:
                rospy.logerr(message)
            else:
                rospy.logwarn(message)
            return
        rospy.Subscriber(
            self.reference_topic,
            PositionCommand,
            self._reference_cmd_callback,
            queue_size=50,
        )
        rospy.loginfo("reference PositionCommand logging enabled on topic: %s", self.reference_topic)

    def _make_log_path(self):
        package_path = rospkg.RosPack().get_path("autotrans_logger")
        log_dir = os.path.abspath(os.path.join(package_path, "..", "logs"))
        os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(log_dir, "autotrans_log_%s.csv" % timestamp)

    def _uav_odom_callback(self, msg):
        self.uav_odom = msg

    def _payload_odom_callback(self, msg):
        self.payload_odom = msg

    def _cable_info_callback(self, msg):
        self.cable_info = msg

    def _so3cmd_callback(self, msg):
        self.so3cmd = msg

    def _trajectory_callback(self, _msg):
        self.has_trajectory = True

    def _reference_cmd_callback(self, msg):
        self.reference_cmd = msg

    def _reference_path_callback(self, msg):
        if len(msg.poses) < 2:
            return
        self.reference_cmd = {
            "header": msg.header,
            "position": msg.poses[0].pose.position,
            "orientation": msg.poses[0].pose.orientation,
            "velocity": msg.poses[1].pose.position,
        }

    def _wind_force_callback(self, msg):
        self.wind_force = msg

    def _command_speed_scale_callback(self, msg):
        self.command_speed_scale = msg

    def _command_acceleration_scale_callback(self, msg):
        self.command_acceleration_scale = msg

    def _command_risk_score_3s_callback(self, msg):
        self.command_risk_score_3s = msg

    def _command_risk_score_5s_callback(self, msg):
        self.command_risk_score_5s = msg

    def _command_risk_scale_selected_callback(self, msg):
        self.command_risk_scale_selected = msg

    def _command_risk_target_scale_raw_callback(self, msg):
        self.command_risk_target_scale_raw = msg

    def _timer_callback(self, _event):
        self.writer.writerow(self._make_row())
        self.csv_file.flush()

    def _make_row(self):
        row = {field: "" for field in self.CSV_FIELDS}
        now_ros_time = rospy.Time.now().to_sec()
        row["ros_time"] = "%.9f" % now_ros_time
        row["wall_time"] = "%.9f" % time.time()
        row["has_trajectory"] = int(self.has_trajectory)
        row["ref_available"] = 1 if self.reference_cmd is not None else 0
        row["command_invalid_event"] = 0
        row["command_saturation_event"] = 0
        row["sustained_command_saturation_event"] = 0
        row["guarded_command_applied"] = 0

        if self.uav_odom is not None:
            self._fill_odom(row, "uav", self.uav_odom)

        if self.payload_odom is not None:
            self._fill_odom(row, "payload", self.payload_odom)

        if self.cable_info is not None:
            row["cable_orientation_x"] = self._fmt(self.cable_info.orientation.x)
            row["cable_orientation_y"] = self._fmt(self.cable_info.orientation.y)
            row["cable_orientation_z"] = self._fmt(self.cable_info.orientation.z)
            row["cable_orientation_w"] = self._fmt(self.cable_info.orientation.w)

        if self.so3cmd is not None:
            row["so3_thrust"] = self._fmt(self.so3cmd.thrust)
            row["so3_bodyrate_x"] = self._fmt(self.so3cmd.body_rate.x)
            row["so3_bodyrate_y"] = self._fmt(self.so3cmd.body_rate.y)
            row["so3_bodyrate_z"] = self._fmt(self.so3cmd.body_rate.z)
            self._fill_command_diagnostics(row, self.so3cmd, now_ros_time)
        else:
            self.saturation_start_time = None

        if self.reference_cmd is not None:
            self._fill_reference_command(row, self.reference_cmd)

        swing_angle = self._compute_swing_angle_deg()
        if swing_angle is not None:
            row["swing_angle_deg"] = self._fmt(swing_angle)

        if self.wind_force is not None:
            wind = self.wind_force.vector
            row["wind_force_x"] = self._fmt(wind.x)
            row["wind_force_y"] = self._fmt(wind.y)
            row["wind_force_z"] = self._fmt(wind.z)
            row["wind_force_norm"] = self._fmt(
                math.sqrt(wind.x * wind.x + wind.y * wind.y + wind.z * wind.z)
            )

        if self.command_speed_scale is not None:
            row["command_speed_scale"] = self._fmt(self.command_speed_scale.data)

        if self.command_acceleration_scale is not None:
            row["command_acceleration_scale"] = self._fmt(self.command_acceleration_scale.data)

        if self.command_risk_score_3s is not None:
            row["command_risk_score_3s"] = self._fmt(self.command_risk_score_3s.data)

        if self.command_risk_score_5s is not None:
            row["command_risk_score_5s"] = self._fmt(self.command_risk_score_5s.data)

        if self.command_risk_scale_selected is not None:
            row["command_risk_scale_selected"] = self._fmt(self.command_risk_scale_selected.data)

        if self.command_risk_target_scale_raw is not None:
            row["command_risk_target_scale_raw"] = self._fmt(self.command_risk_target_scale_raw.data)

        return row

    def _fill_odom(self, row, prefix, odom):
        row["%s_pos_x" % prefix] = self._fmt(odom.pose.pose.position.x)
        row["%s_pos_y" % prefix] = self._fmt(odom.pose.pose.position.y)
        row["%s_pos_z" % prefix] = self._fmt(odom.pose.pose.position.z)
        row["%s_vel_x" % prefix] = self._fmt(odom.twist.twist.linear.x)
        row["%s_vel_y" % prefix] = self._fmt(odom.twist.twist.linear.y)
        row["%s_vel_z" % prefix] = self._fmt(odom.twist.twist.linear.z)

    def _fill_command_diagnostics(self, row, so3cmd, now_ros_time):
        command_values = {
            "so3_thrust": so3cmd.thrust,
            "so3_bodyrate_x": so3cmd.body_rate.x,
            "so3_bodyrate_y": so3cmd.body_rate.y,
            "so3_bodyrate_z": so3cmd.body_rate.z,
        }
        invalid_fields = [
            name for name, value in command_values.items() if not math.isfinite(value)
        ]
        if invalid_fields:
            row["command_invalid_event"] = 1
            row["command_invalid_reason"] = ",".join(invalid_fields)

        saturated_fields = []
        thrust = command_values["so3_thrust"]
        bodyrate_x = command_values["so3_bodyrate_x"]
        bodyrate_y = command_values["so3_bodyrate_y"]
        bodyrate_z = command_values["so3_bodyrate_z"]
        if math.isfinite(thrust) and thrust >= self.thrust_saturation_threshold:
            saturated_fields.append("so3_thrust")
        if math.isfinite(bodyrate_x) and abs(bodyrate_x) >= self.bodyrate_xy_saturation_threshold:
            saturated_fields.append("so3_bodyrate_x")
        if math.isfinite(bodyrate_y) and abs(bodyrate_y) >= self.bodyrate_xy_saturation_threshold:
            saturated_fields.append("so3_bodyrate_y")
        if math.isfinite(bodyrate_z) and abs(bodyrate_z) >= self.bodyrate_z_saturation_threshold:
            saturated_fields.append("so3_bodyrate_z")

        if saturated_fields:
            row["command_saturation_event"] = 1
            row["command_saturation_reason"] = ",".join(saturated_fields)
            if self.saturation_start_time is None:
                self.saturation_start_time = now_ros_time
            elif now_ros_time - self.saturation_start_time >= self.sustained_saturation_duration_sec:
                row["sustained_command_saturation_event"] = 1
        else:
            self.saturation_start_time = None

    def _fill_reference_command(self, row, msg):
        if isinstance(msg, dict):
            position = msg["position"]
            velocity = msg["velocity"]
            row["ref_pos_x"] = self._fmt(position.x)
            row["ref_pos_y"] = self._fmt(position.y)
            row["ref_pos_z"] = self._fmt(position.z)
            row["ref_vel_x"] = self._fmt(velocity.x)
            row["ref_vel_y"] = self._fmt(velocity.y)
            row["ref_vel_z"] = self._fmt(velocity.z)
            row["ref_yaw"] = self._fmt(self._yaw_from_quaternion(msg["orientation"]))
            row["ref_msg_ros_time"] = self._fmt(msg["header"].stamp.to_sec())
            return

        row["ref_pos_x"] = self._fmt(msg.position.x)
        row["ref_pos_y"] = self._fmt(msg.position.y)
        row["ref_pos_z"] = self._fmt(msg.position.z)
        row["ref_vel_x"] = self._fmt(msg.velocity.x)
        row["ref_vel_y"] = self._fmt(msg.velocity.y)
        row["ref_vel_z"] = self._fmt(msg.velocity.z)
        row["ref_acc_x"] = self._fmt(msg.acceleration.x)
        row["ref_acc_y"] = self._fmt(msg.acceleration.y)
        row["ref_acc_z"] = self._fmt(msg.acceleration.z)
        row["ref_yaw"] = self._fmt(msg.yaw)
        row["ref_yaw_dot"] = self._fmt(msg.yaw_dot)
        row["ref_msg_ros_time"] = self._fmt(msg.header.stamp.to_sec())

    @staticmethod
    def _yaw_from_quaternion(quat):
        siny_cosp = 2.0 * (quat.w * quat.z + quat.x * quat.y)
        cosy_cosp = 1.0 - 2.0 * (quat.y * quat.y + quat.z * quat.z)
        return math.atan2(siny_cosp, cosy_cosp)

    def _compute_swing_angle_deg(self):
        if self.uav_odom is None or self.payload_odom is None:
            return None

        uav_pos = self.uav_odom.pose.pose.position
        payload_pos = self.payload_odom.pose.pose.position
        cable_x = payload_pos.x - uav_pos.x
        cable_y = payload_pos.y - uav_pos.y
        cable_z = payload_pos.z - uav_pos.z
        cable_norm = math.sqrt(cable_x * cable_x + cable_y * cable_y + cable_z * cable_z)
        if cable_norm < 1e-9:
            return None

        dot_with_down = -cable_z / cable_norm
        dot_with_down = max(-1.0, min(1.0, dot_with_down))
        return math.degrees(math.acos(dot_with_down))

    @staticmethod
    def _fmt(value):
        return "%.9f" % value

    def close(self):
        if not self.csv_file.closed:
            self.csv_file.flush()
            self.csv_file.close()


def main():
    rospy.init_node("state_logger")
    StateLogger()
    rospy.spin()


if __name__ == "__main__":
    main()
