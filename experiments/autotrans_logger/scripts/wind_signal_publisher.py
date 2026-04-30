#!/usr/bin/env python3

import math

import rospy
from geometry_msgs.msg import Vector3Stamped


class WindSignalPublisher:
    VALID_MODES = ("none", "constant", "step", "sine")

    def __init__(self):
        self.enable_wind = rospy.get_param("~enable_wind", False)
        self.wind_mode = str(rospy.get_param("~wind_mode", "none")).lower()
        self.wind_frame = str(rospy.get_param("~wind_frame", "world"))
        self.wind_force_x = float(rospy.get_param("~wind_force_x", 0.0))
        self.wind_force_y = float(rospy.get_param("~wind_force_y", 0.0))
        self.wind_force_z = float(rospy.get_param("~wind_force_z", 0.0))
        self.wind_start_time = float(rospy.get_param("~wind_start_time", 0.0))
        self.wind_sine_amp_x = float(rospy.get_param("~wind_sine_amp_x", 0.0))
        self.wind_sine_amp_y = float(rospy.get_param("~wind_sine_amp_y", 0.0))
        self.wind_sine_amp_z = float(rospy.get_param("~wind_sine_amp_z", 0.0))
        self.wind_sine_freq = float(rospy.get_param("~wind_sine_freq", 0.1))
        self.wind_max_force = float(rospy.get_param("~wind_max_force", 0.0))
        publish_rate = float(rospy.get_param("~publish_rate", 20.0))

        self.start_time = rospy.Time.now()
        self.publisher = rospy.Publisher("/wind_force", Vector3Stamped, queue_size=10)
        self.timer = rospy.Timer(
            rospy.Duration(1.0 / max(publish_rate, 1e-3)), self._timer_callback
        )

        rospy.loginfo(
            "wind_signal_publisher publishing /wind_force mode=%s enable_wind=%s",
            self.wind_mode,
            self.enable_wind,
        )

    def _timer_callback(self, _event):
        now = rospy.Time.now()
        elapsed = max(0.0, (now - self.start_time).to_sec())
        wind = self._compute_wind(elapsed)

        msg = Vector3Stamped()
        msg.header.stamp = now
        msg.header.frame_id = "world"
        msg.vector.x = wind[0]
        msg.vector.y = wind[1]
        msg.vector.z = wind[2]
        self.publisher.publish(msg)

    def _compute_wind(self, elapsed):
        if self.wind_frame != "world":
            rospy.logwarn_throttle(
                5.0,
                "wind_signal_publisher only supports wind_frame=world; got %s. Publishing zero wind.",
                self.wind_frame,
            )
            return (0.0, 0.0, 0.0)

        if not self.enable_wind or self.wind_mode == "none":
            return (0.0, 0.0, 0.0)

        if self.wind_mode == "constant":
            wind = (self.wind_force_x, self.wind_force_y, self.wind_force_z)
        elif self.wind_mode == "step":
            if elapsed < self.wind_start_time:
                wind = (0.0, 0.0, 0.0)
            else:
                wind = (self.wind_force_x, self.wind_force_y, self.wind_force_z)
        elif self.wind_mode == "sine":
            phase = 2.0 * math.pi * self.wind_sine_freq * elapsed
            sine_value = math.sin(phase)
            wind = (
                self.wind_sine_amp_x * sine_value,
                self.wind_sine_amp_y * sine_value,
                self.wind_sine_amp_z * sine_value,
            )
        else:
            rospy.logwarn_throttle(
                5.0,
                "Invalid wind_mode=%s. Expected one of %s. Publishing zero wind.",
                self.wind_mode,
                ", ".join(self.VALID_MODES),
            )
            return (0.0, 0.0, 0.0)

        return self._clip_norm(wind)

    def _clip_norm(self, wind):
        if self.wind_max_force <= 0.0:
            return wind

        norm = math.sqrt(wind[0] * wind[0] + wind[1] * wind[1] + wind[2] * wind[2])
        if norm <= self.wind_max_force or norm < 1e-9:
            return wind

        scale = self.wind_max_force / norm
        return (wind[0] * scale, wind[1] * scale, wind[2] * scale)


def main():
    rospy.init_node("wind_signal_publisher")
    WindSignalPublisher()
    rospy.spin()


if __name__ == "__main__":
    main()
