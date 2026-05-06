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
from quadrotor_msgs.msg import PolynomialTraj
from sensor_msgs.msg import Imu
from std_msgs.msg import Float64


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
        "swing_angle_deg",
        "has_trajectory",
        "wind_force_x",
        "wind_force_y",
        "wind_force_z",
        "wind_force_norm",
        "command_speed_scale",
        "command_acceleration_scale",
    ]

    def __init__(self):
        self.uav_odom = None
        self.payload_odom = None
        self.cable_info = None
        self.so3cmd = None
        self.wind_force = None
        self.command_speed_scale = None
        self.command_acceleration_scale = None
        self.has_trajectory = False

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
        rospy.Subscriber("/wind_force", Vector3Stamped, self._wind_force_callback, queue_size=50)
        rospy.Subscriber("/command_adaptation/speed_scale", Float64, self._command_speed_scale_callback, queue_size=50)
        rospy.Subscriber("/command_adaptation/acceleration_scale", Float64, self._command_acceleration_scale_callback, queue_size=50)

        log_rate = rospy.get_param("~log_rate", 20.0)
        self.timer = rospy.Timer(rospy.Duration(1.0 / max(log_rate, 1e-3)), self._timer_callback)
        rospy.on_shutdown(self.close)

        rospy.loginfo("autotrans_logger writing CSV to: %s", self.log_path)

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

    def _wind_force_callback(self, msg):
        self.wind_force = msg

    def _command_speed_scale_callback(self, msg):
        self.command_speed_scale = msg

    def _command_acceleration_scale_callback(self, msg):
        self.command_acceleration_scale = msg

    def _timer_callback(self, _event):
        self.writer.writerow(self._make_row())
        self.csv_file.flush()

    def _make_row(self):
        row = {field: "" for field in self.CSV_FIELDS}
        row["ros_time"] = "%.9f" % rospy.Time.now().to_sec()
        row["wall_time"] = "%.9f" % time.time()
        row["has_trajectory"] = int(self.has_trajectory)

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

        return row

    def _fill_odom(self, row, prefix, odom):
        row["%s_pos_x" % prefix] = self._fmt(odom.pose.pose.position.x)
        row["%s_pos_y" % prefix] = self._fmt(odom.pose.pose.position.y)
        row["%s_pos_z" % prefix] = self._fmt(odom.pose.pose.position.z)
        row["%s_vel_x" % prefix] = self._fmt(odom.twist.twist.linear.x)
        row["%s_vel_y" % prefix] = self._fmt(odom.twist.twist.linear.y)
        row["%s_vel_z" % prefix] = self._fmt(odom.twist.twist.linear.z)

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
