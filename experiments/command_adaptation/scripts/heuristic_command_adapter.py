#!/usr/bin/env python3

import math
from collections import deque

import rospy
from geometry_msgs.msg import Vector3Stamped
from nav_msgs.msg import Odometry
from quadrotor_msgs.msg import PolynomialTraj
from std_msgs.msg import Float64


class HeuristicCommandAdapter:
    def __init__(self):
        self.publish_rate = float(rospy.get_param("~publish_rate", 5.0))
        self.min_scale = float(rospy.get_param("~min_scale", 0.4))
        self.max_scale = float(rospy.get_param("~max_scale", 1.0))

        self.weak_wind_norm = float(rospy.get_param("~weak_wind_norm", 0.002))
        self.moderate_wind_norm = float(rospy.get_param("~moderate_wind_norm", 0.005))
        self.strong_wind_norm = float(rospy.get_param("~strong_wind_norm", 0.0075))
        self.boundary_wind_norm = float(rospy.get_param("~boundary_wind_norm", 0.010))

        self.no_wind_scale = float(rospy.get_param("~no_wind_scale", 1.0))
        self.weak_scale = float(rospy.get_param("~weak_scale", 0.95))
        self.moderate_scale = float(rospy.get_param("~moderate_scale", 0.90))
        self.strong_scale = float(rospy.get_param("~strong_scale", 0.85))
        self.boundary_scale = float(rospy.get_param("~boundary_scale", 0.70))

        self.swing_warn_deg = float(rospy.get_param("~swing_warn_deg", 20.0))
        self.swing_critical_deg = float(rospy.get_param("~swing_critical_deg", 35.0))
        self.swing_warn_scale = float(rospy.get_param("~swing_warn_scale", 0.65))
        self.swing_critical_scale = float(rospy.get_param("~swing_critical_scale", 0.50))

        self.speed_warn = float(rospy.get_param("~speed_warn", 3.2))
        self.speed_critical = float(rospy.get_param("~speed_critical", 4.0))
        self.speed_warn_scale = float(rospy.get_param("~speed_warn_scale", 0.65))
        self.speed_critical_scale = float(rospy.get_param("~speed_critical_scale", 0.50))

        self.recent_speed_window_sec = float(rospy.get_param("~recent_speed_window_sec", 3.0))
        self.scale_rate_limit_per_sec = float(rospy.get_param("~scale_rate_limit_per_sec", 0.5))
        self.publish_same_acceleration_scale = bool(rospy.get_param("~publish_same_acceleration_scale", True))

        self.uav_odom = None
        self.payload_odom = None
        self.wind_force = None
        self.has_trajectory = False
        self.previous_speed_scale = None
        self.previous_acceleration_scale = None
        self.recent_speeds = deque()

        self.speed_scale_pub = rospy.Publisher("/command_adaptation/speed_scale", Float64, queue_size=10)
        self.acceleration_scale_pub = rospy.Publisher("/command_adaptation/acceleration_scale", Float64, queue_size=10)

        rospy.Subscriber("/visual_slam/odom", Odometry, self._uav_odom_callback, queue_size=20)
        rospy.Subscriber("/payload_odom", Odometry, self._payload_odom_callback, queue_size=20)
        rospy.Subscriber("/wind_force", Vector3Stamped, self._wind_force_callback, queue_size=20)
        rospy.Subscriber("/planning/trajectory", PolynomialTraj, self._trajectory_callback, queue_size=10)

        timer_period = 1.0 / max(self.publish_rate, 1e-3)
        self.timer = rospy.Timer(rospy.Duration(timer_period), self._timer_callback)

        rospy.loginfo(
            "heuristic_command_adapter publishing command adaptation scales at %.3f Hz",
            self.publish_rate,
        )

    def _uav_odom_callback(self, msg):
        if self._odom_is_finite(msg):
            self.uav_odom = msg
        else:
            rospy.logwarn_throttle(1.0, "ignoring non-finite /visual_slam/odom")

    def _payload_odom_callback(self, msg):
        if self._odom_is_finite(msg):
            self.payload_odom = msg
        else:
            rospy.logwarn_throttle(1.0, "ignoring non-finite /payload_odom")

    def _wind_force_callback(self, msg):
        wind = msg.vector
        if self._all_finite(wind.x, wind.y, wind.z):
            self.wind_force = msg
        else:
            rospy.logwarn_throttle(1.0, "ignoring non-finite /wind_force")

    def _trajectory_callback(self, _msg):
        self.has_trajectory = True

    def _timer_callback(self, _event):
        now = rospy.Time.now().to_sec()
        uav_speed = self._odom_speed(self.uav_odom)
        payload_speed = self._odom_speed(self.payload_odom)

        if math.isfinite(uav_speed) or math.isfinite(payload_speed):
            current_speed = max(
                uav_speed if math.isfinite(uav_speed) else 0.0,
                payload_speed if math.isfinite(payload_speed) else 0.0,
            )
            self.recent_speeds.append((now, current_speed))

        self._trim_recent_speeds(now)

        wind_force_norm = self._wind_force_norm()
        swing_angle_deg = self._compute_swing_angle_deg()
        recent_max_speed = self._recent_max_speed()

        target_speed_scale = self._compute_policy_scale(wind_force_norm, swing_angle_deg, recent_max_speed)
        target_acceleration_scale = target_speed_scale if self.publish_same_acceleration_scale else target_speed_scale

        speed_scale = self._apply_rate_limit(target_speed_scale, self.previous_speed_scale)
        acceleration_scale = self._apply_rate_limit(target_acceleration_scale, self.previous_acceleration_scale)

        speed_scale = self._clamp_scale(speed_scale)
        acceleration_scale = self._clamp_scale(acceleration_scale)
        self.previous_speed_scale = speed_scale
        self.previous_acceleration_scale = acceleration_scale

        self.speed_scale_pub.publish(Float64(data=speed_scale))
        self.acceleration_scale_pub.publish(Float64(data=acceleration_scale))

        rospy.loginfo_throttle(
            1.0,
            (
                "heuristic_command_adapter wind_force_norm=%.6f swing_angle_deg=%.3f "
                "recent_max_speed=%.3f speed_scale=%.3f acceleration_scale=%.3f has_trajectory=%s"
            ),
            wind_force_norm,
            swing_angle_deg,
            recent_max_speed,
            speed_scale,
            acceleration_scale,
            str(self.has_trajectory).lower(),
        )

    def _compute_policy_scale(self, wind_force_norm, swing_angle_deg, recent_max_speed):
        if self.uav_odom is None and self.payload_odom is None:
            return self._clamp_scale(1.0)

        scale = self._base_wind_scale(wind_force_norm)

        if math.isfinite(swing_angle_deg):
            if swing_angle_deg > self.swing_critical_deg:
                scale = min(scale, self.swing_critical_scale)
            elif swing_angle_deg > self.swing_warn_deg:
                scale = min(scale, self.swing_warn_scale)

        if math.isfinite(recent_max_speed):
            if recent_max_speed > self.speed_critical:
                scale = min(scale, self.speed_critical_scale)
            elif recent_max_speed > self.speed_warn:
                scale = min(scale, self.speed_warn_scale)

        return self._clamp_scale(scale)

    def _base_wind_scale(self, wind_force_norm):
        if not math.isfinite(wind_force_norm):
            return self.no_wind_scale
        if wind_force_norm >= self.boundary_wind_norm:
            return self.boundary_scale
        if wind_force_norm >= self.strong_wind_norm:
            return self.strong_scale
        if wind_force_norm >= self.moderate_wind_norm:
            return self.moderate_scale
        if wind_force_norm >= self.weak_wind_norm:
            return self.weak_scale
        return self.no_wind_scale

    def _apply_rate_limit(self, target_scale, previous_scale):
        target_scale = self._clamp_scale(target_scale)
        if previous_scale is None or not math.isfinite(previous_scale):
            return target_scale

        max_step = max(0.0, self.scale_rate_limit_per_sec) / max(self.publish_rate, 1e-3)
        delta = target_scale - previous_scale
        if delta > max_step:
            return previous_scale + max_step
        if delta < -max_step:
            return previous_scale - max_step
        return target_scale

    def _wind_force_norm(self):
        if self.wind_force is None:
            return 0.0
        wind = self.wind_force.vector
        return self._vector_norm(wind.x, wind.y, wind.z)

    def _compute_swing_angle_deg(self):
        if self.uav_odom is None or self.payload_odom is None:
            return math.nan

        uav_pos = self.uav_odom.pose.pose.position
        payload_pos = self.payload_odom.pose.pose.position
        cable_x = payload_pos.x - uav_pos.x
        cable_y = payload_pos.y - uav_pos.y
        cable_z = payload_pos.z - uav_pos.z
        cable_norm = self._vector_norm(cable_x, cable_y, cable_z)
        if not math.isfinite(cable_norm) or cable_norm < 1e-9:
            return math.nan

        dot_with_down = -cable_z / cable_norm
        dot_with_down = max(-1.0, min(1.0, dot_with_down))
        return math.degrees(math.acos(dot_with_down))

    def _odom_speed(self, odom):
        if odom is None:
            return math.nan
        velocity = odom.twist.twist.linear
        return self._vector_norm(velocity.x, velocity.y, velocity.z)

    def _trim_recent_speeds(self, now):
        window = max(0.0, self.recent_speed_window_sec)
        while self.recent_speeds and now - self.recent_speeds[0][0] > window:
            self.recent_speeds.popleft()

    def _recent_max_speed(self):
        values = [speed for _, speed in self.recent_speeds if math.isfinite(speed)]
        if not values:
            return 0.0
        return max(values)

    def _clamp_scale(self, value):
        if not math.isfinite(value):
            if self.previous_speed_scale is not None and math.isfinite(self.previous_speed_scale):
                value = self.previous_speed_scale
            else:
                value = 1.0
        lower = min(self.min_scale, self.max_scale)
        upper = max(self.min_scale, self.max_scale)
        return max(lower, min(upper, value))

    @staticmethod
    def _odom_is_finite(odom):
        position = odom.pose.pose.position
        velocity = odom.twist.twist.linear
        return HeuristicCommandAdapter._all_finite(
            position.x,
            position.y,
            position.z,
            velocity.x,
            velocity.y,
            velocity.z,
        )

    @staticmethod
    def _vector_norm(x_value, y_value, z_value):
        if not HeuristicCommandAdapter._all_finite(x_value, y_value, z_value):
            return math.nan
        return math.sqrt(x_value * x_value + y_value * y_value + z_value * z_value)

    @staticmethod
    def _all_finite(*values):
        return all(math.isfinite(value) for value in values)


def main():
    rospy.init_node("heuristic_command_adapter")
    HeuristicCommandAdapter()
    rospy.spin()


if __name__ == "__main__":
    main()
