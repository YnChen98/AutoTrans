#!/usr/bin/env python3
"""Stage 4-H risk-conditioned command adapter v0.

This node publishes planner command scale topics only. It never commands
thrust/bodyrate and does not replace planner, controller, or simulator logic.
"""

import json
import math
import os

import rospy
from geometry_msgs.msg import PoseStamped, Vector3Stamped
from nav_msgs.msg import Odometry
from std_msgs.msg import Float64


class LogRegJsonModel:
    """Minimal JSON-only LogisticRegression inference helper."""

    MODEL_TYPE = "LogisticRegression"

    def __init__(self, path, label):
        self.path = path
        self.label = label
        self.feature_names = []
        self.feature_specs = []
        self.imputation_values = {}
        self.mean_values = {}
        self.standard_deviations = {}
        self.coefficients = []
        self.intercept = 0.0
        self.enabled = False
        self.warning = ""
        self._load()

    def infer_probability(self, feature_row):
        if not self.enabled:
            return None

        logit = self.intercept
        for index, spec in enumerate(self.feature_specs):
            feature_name = self.feature_names[index]
            value = self._feature_value(spec, feature_row)
            if not math.isfinite(value):
                return None

            mean_value = self.mean_values[feature_name]
            std_value = self.standard_deviations[feature_name]
            scaled = (value - mean_value) / std_value if std_value else value - mean_value
            logit += self.coefficients[index] * scaled

        probability = self._sigmoid(logit)
        if not math.isfinite(probability):
            return None
        return probability

    def _load(self):
        if not self.path:
            self.warning = "%s model path is empty" % self.label
            return

        resolved_path = os.path.expanduser(self.path)
        if not os.path.isabs(resolved_path):
            resolved_path = os.path.abspath(resolved_path)

        try:
            with open(resolved_path, "r", encoding="utf-8") as model_file:
                model = json.load(model_file)
            self._validate_and_assign(model)
        except (IOError, OSError, ValueError, KeyError, TypeError) as exc:
            self.warning = "%s model invalid at %s: %s" % (self.label, resolved_path, exc)
            self.enabled = False
            return

        self.path = resolved_path
        self.enabled = True

    def _validate_and_assign(self, model):
        model_block = model.get("model", {})
        if model_block.get("type") != self.MODEL_TYPE:
            raise ValueError("model.type is not %s" % self.MODEL_TYPE)

        feature_names = model.get("feature_names")
        preprocessing = model.get("preprocessing")
        if not isinstance(feature_names, list) or not feature_names:
            raise ValueError("missing non-empty feature_names")
        if not isinstance(preprocessing, dict):
            raise ValueError("missing preprocessing object")

        feature_specs = preprocessing.get("feature_specs")
        imputation_values = preprocessing.get("imputation_values")
        mean_values = preprocessing.get("mean_values")
        standard_deviations = preprocessing.get("standard_deviations")
        if not isinstance(feature_specs, list) or len(feature_specs) != len(feature_names):
            raise ValueError("feature_specs length does not match feature_names")
        for value_name, values in (
            ("imputation_values", imputation_values),
            ("mean_values", mean_values),
            ("standard_deviations", standard_deviations),
        ):
            if not isinstance(values, dict):
                raise ValueError("missing preprocessing.%s" % value_name)
            missing = [name for name in feature_names if name not in values]
            if missing:
                raise ValueError("preprocessing.%s missing %s" % (value_name, ", ".join(missing)))

        coefficients = model_block.get("coefficients")
        intercept = model_block.get("intercept")
        if not isinstance(coefficients, list) or not coefficients or not isinstance(coefficients[0], list):
            raise ValueError("missing model.coefficients[0]")
        if len(coefficients[0]) != len(feature_names):
            raise ValueError("coefficient count does not match feature_names")
        if not isinstance(intercept, list) or not intercept:
            raise ValueError("missing model.intercept[0]")

        parsed_coefficients = [self._parse_finite(value, "coefficient") for value in coefficients[0]]
        parsed_intercept = self._parse_finite(intercept[0], "intercept")
        parsed_imputation = {}
        parsed_means = {}
        parsed_stds = {}
        for feature_name in feature_names:
            parsed_imputation[feature_name] = self._parse_finite(
                imputation_values[feature_name], "imputation value for %s" % feature_name
            )
            parsed_means[feature_name] = self._parse_finite(
                mean_values[feature_name], "mean value for %s" % feature_name
            )
            parsed_stds[feature_name] = self._parse_finite(
                standard_deviations[feature_name], "standard deviation for %s" % feature_name
            )

        self.feature_names = list(feature_names)
        self.feature_specs = list(feature_specs)
        self.imputation_values = parsed_imputation
        self.mean_values = parsed_means
        self.standard_deviations = parsed_stds
        self.coefficients = parsed_coefficients
        self.intercept = parsed_intercept

    @staticmethod
    def _feature_value(spec, feature_row):
        feature_name = str(spec.get("name", ""))
        source_column = str(spec.get("source_column", ""))
        kind = str(spec.get("kind", ""))

        if kind == "categorical_onehot":
            source_value = feature_row.get(source_column, feature_row.get(feature_name, None))
            if source_value is None:
                return math.nan
            return 1.0 if str(source_value).strip() == str(spec.get("category", "")) else 0.0

        if source_column in feature_row:
            return LogRegJsonModel._parse_float(feature_row.get(source_column))
        if feature_name in feature_row:
            return LogRegJsonModel._parse_float(feature_row.get(feature_name))
        return math.nan

    @staticmethod
    def _parse_float(value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return math.nan

    @staticmethod
    def _parse_finite(value, label):
        number = LogRegJsonModel._parse_float(value)
        if not math.isfinite(number):
            raise ValueError("%s is non-finite" % label)
        return number

    @staticmethod
    def _sigmoid(logit):
        if logit >= 0.0:
            exp_negative = math.exp(-logit)
            return 1.0 / (1.0 + exp_negative)
        exp_positive = math.exp(logit)
        return exp_positive / (1.0 + exp_positive)


class RiskConditionedCommandAdapter:
    POLICY_MODE_WIND_LEVEL = "wind_level"
    POLICY_MODE_RISK_CONDITIONED = "risk_conditioned"
    VALID_POLICY_MODES = (POLICY_MODE_WIND_LEVEL, POLICY_MODE_RISK_CONDITIONED)

    def __init__(self):
        self.enable_risk_conditioning = bool(rospy.get_param("~enable_risk_conditioning", False))
        self.policy_mode = str(rospy.get_param("~policy_mode", self.POLICY_MODE_WIND_LEVEL))
        if self.policy_mode not in self.VALID_POLICY_MODES:
            rospy.logwarn(
                "unknown policy_mode=%s; falling back to %s",
                self.policy_mode,
                self.POLICY_MODE_WIND_LEVEL,
            )
            self.policy_mode = self.POLICY_MODE_WIND_LEVEL

        self.target_z = float(rospy.get_param("~target_z", 1.468415))
        self.payload_target_z = float(rospy.get_param("~payload_target_z", 0.799970))

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

        self.risk_threshold_3s = float(rospy.get_param("~risk_threshold_3s", 0.5))
        self.risk_threshold_5s = float(rospy.get_param("~risk_threshold_5s", 0.5))
        self.hard_threshold_5s = float(rospy.get_param("~hard_threshold_5s", 0.7))
        self.soft_scale_3s = float(rospy.get_param("~soft_scale_3s", 0.85))
        self.soft_scale_5s = float(rospy.get_param("~soft_scale_5s", 0.75))
        self.hard_scale_5s = float(rospy.get_param("~hard_scale_5s", 0.65))
        self.scale_rate_limit_per_sec = float(rospy.get_param("~scale_rate_limit_per_sec", 0.5))
        self.publish_same_acceleration_scale = bool(rospy.get_param("~publish_same_acceleration_scale", True))
        self.same_goal_position_tolerance = max(
            0.0,
            float(rospy.get_param("~same_goal_position_tolerance", 0.05)),
        )
        self.reset_on_new_distinct_goal = bool(rospy.get_param("~reset_on_new_distinct_goal", True))
        self.reset_on_first_trajectory_after_goal = bool(
            rospy.get_param("~reset_on_first_trajectory_after_goal", False)
        )

        self.model_3s = LogRegJsonModel(str(rospy.get_param("~model_json_3s", "")), "3s")
        self.model_5s = LogRegJsonModel(str(rospy.get_param("~model_json_5s", "")), "5s")
        model_json_15s = str(rospy.get_param("~model_json_15s", ""))
        self.model_15s = LogRegJsonModel(model_json_15s, "15s") if model_json_15s else None
        self.models_ready = self.model_3s.enabled and self.model_5s.enabled
        self._warn_model_state()

        self.uav_odom = None
        self.payload_odom = None
        self.wind_force = None
        self.goal_received = False
        self.last_goal_received_time = None
        self.has_trajectory = False
        self.trajectory_seen_for_goal = False
        self.episode_start_time = None
        self.current_goal_position = None
        self.target_x = math.nan
        self.target_y = math.nan
        self.samples = []
        self.latest_risk_score_3s = -1.0
        self.latest_risk_score_5s = -1.0
        self.previous_speed_scale = None
        self.previous_acceleration_scale = None
        self.last_publish_time = None

        self.speed_scale_pub = rospy.Publisher("/command_adaptation/speed_scale", Float64, queue_size=10)
        self.acceleration_scale_pub = rospy.Publisher(
            "/command_adaptation/acceleration_scale", Float64, queue_size=10
        )
        self.risk_score_3s_pub = rospy.Publisher("/command_adaptation/risk_score_3s", Float64, queue_size=10)
        self.risk_score_5s_pub = rospy.Publisher("/command_adaptation/risk_score_5s", Float64, queue_size=10)
        self.risk_scale_selected_pub = rospy.Publisher(
            "/command_adaptation/risk_scale_selected", Float64, queue_size=10
        )
        self.risk_target_scale_raw_pub = rospy.Publisher(
            "/command_adaptation/risk_target_scale_raw", Float64, queue_size=10
        )

        rospy.Subscriber("/visual_slam/odom", Odometry, self._uav_odom_callback, queue_size=20)
        rospy.Subscriber("/payload_odom", Odometry, self._payload_odom_callback, queue_size=20)
        rospy.Subscriber("/wind_force", Vector3Stamped, self._wind_force_callback, queue_size=20)
        rospy.Subscriber("/move_base_simple/goal", PoseStamped, self._goal_callback, queue_size=10)
        rospy.Subscriber("/planning/trajectory", rospy.AnyMsg, self._trajectory_callback, queue_size=10)

        timer_period = 1.0 / max(self.publish_rate, 1e-3)
        self.timer = rospy.Timer(rospy.Duration(timer_period), self._timer_callback)

        rospy.loginfo(
            (
                "risk_conditioned_command_adapter publishing command adaptation scales at %.3f Hz "
                "policy_mode=%s enable_risk_conditioning=%s models_ready=%s "
                "same_goal_position_tolerance=%.3f reset_on_new_distinct_goal=%s "
                "reset_on_first_trajectory_after_goal=%s"
            ),
            self.publish_rate,
            self.policy_mode,
            str(self.enable_risk_conditioning).lower(),
            str(self.models_ready).lower(),
            self.same_goal_position_tolerance,
            str(self.reset_on_new_distinct_goal).lower(),
            str(self.reset_on_first_trajectory_after_goal).lower(),
        )

    def _warn_model_state(self):
        for model in (self.model_3s, self.model_5s, self.model_15s):
            if model is None:
                continue
            if model.enabled:
                rospy.loginfo(
                    "loaded %s LogisticRegression model from %s with %d features",
                    model.label,
                    model.path,
                    len(model.feature_names),
                )
            else:
                rospy.logwarn(
                    "%s; risk-conditioned inference will fall back to wind_level when needed",
                    model.warning,
                )
        if self.enable_risk_conditioning and not self.models_ready:
            rospy.logwarn("risk conditioning enabled but required 3s/5s models are unavailable; using wind_level")

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

    def _goal_callback(self, msg):
        position = msg.pose.position
        if not self._all_finite(position.x, position.y, position.z):
            rospy.logwarn_throttle(1.0, "ignoring non-finite /move_base_simple/goal")
            return

        now = rospy.Time.now().to_sec()
        goal_position = (position.x, position.y, position.z)
        distance_from_current = self._goal_distance_from_current(goal_position)
        is_same_goal = (
            distance_from_current is not None
            and distance_from_current < self.same_goal_position_tolerance
        )

        if is_same_goal:
            self.goal_received = True
            self.last_goal_received_time = now
            rospy.loginfo_throttle(
                1.0,
                (
                    "risk_conditioned_command_adapter ignored repeated goal "
                    "distance=%.3f tolerance=%.3f episode_age=%.3f"
                ),
                distance_from_current,
                self.same_goal_position_tolerance,
                self._episode_age(now),
            )
            return

        active_episode = self._has_active_episode()
        self.goal_received = True
        self.last_goal_received_time = now
        self.current_goal_position = goal_position
        self.target_x = position.x
        self.target_y = position.y
        self.has_trajectory = False
        self.trajectory_seen_for_goal = False

        if not active_episode:
            self._reset_episode(now, "first_distinct_goal")
            return

        if self.reset_on_new_distinct_goal:
            self._reset_episode(now, "new_distinct_goal")
            return

        rospy.loginfo_throttle(
            1.0,
            (
                "risk_conditioned_command_adapter accepted distinct goal without reset "
                "distance=%.3f episode_age=%.3f target_x=%.3f target_y=%.3f"
            ),
            distance_from_current if distance_from_current is not None else -1.0,
            self._episode_age(now),
            self.target_x,
            self.target_y,
        )

    def _trajectory_callback(self, _msg):
        if not self.goal_received:
            return

        now = rospy.Time.now().to_sec()
        if not self.trajectory_seen_for_goal:
            self.has_trajectory = True
            self.trajectory_seen_for_goal = True
            if not self._has_active_episode():
                self._reset_episode(now, "first_trajectory_without_active_episode")
            elif self.reset_on_first_trajectory_after_goal:
                self._reset_episode(now, "first_trajectory_after_goal")
                self.has_trajectory = True
                self.trajectory_seen_for_goal = True
            rospy.logdebug(
                "risk_conditioned_command_adapter first trajectory for goal episode_age=%.3f",
                self._episode_age(now),
            )
            return

        self.has_trajectory = True

    def _timer_callback(self, _event):
        now = rospy.Time.now().to_sec()
        self._append_episode_sample(now)

        wind_force_norm = self._wind_force_norm()
        base_scale = self._base_wind_scale(wind_force_norm)
        target_scale = self._compute_target_scale(now, base_scale)
        target_acceleration_scale = target_scale if self.publish_same_acceleration_scale else target_scale

        speed_scale = self._apply_rate_limit(target_scale, self.previous_speed_scale, now)
        acceleration_scale = self._apply_rate_limit(target_acceleration_scale, self.previous_acceleration_scale, now)

        speed_scale = self._clamp_scale(speed_scale)
        acceleration_scale = self._clamp_scale(acceleration_scale)
        self.previous_speed_scale = speed_scale
        self.previous_acceleration_scale = acceleration_scale
        self.last_publish_time = now

        self.speed_scale_pub.publish(Float64(data=speed_scale))
        self.acceleration_scale_pub.publish(Float64(data=acceleration_scale))
        self.risk_score_3s_pub.publish(Float64(data=self._safe_score(self.latest_risk_score_3s)))
        self.risk_score_5s_pub.publish(Float64(data=self._safe_score(self.latest_risk_score_5s)))
        self.risk_scale_selected_pub.publish(Float64(data=speed_scale))
        self.risk_target_scale_raw_pub.publish(Float64(data=target_scale))

        rospy.loginfo_throttle(
            1.0,
            (
                "risk_conditioned_command_adapter base_scale=%.3f target_scale=%.3f speed_scale=%.3f "
                "risk_3s=%.3f risk_5s=%.3f goal=%s has_trajectory=%s samples=%d episode_age=%.3f"
            ),
            base_scale,
            target_scale,
            speed_scale,
            self._safe_score(self.latest_risk_score_3s),
            self._safe_score(self.latest_risk_score_5s),
            str(self.goal_received).lower(),
            str(self.has_trajectory).lower(),
            len(self.samples),
            self._episode_age(now),
        )

    def _reset_episode(self, now, reason):
        self.episode_start_time = now
        self.samples = []
        self.latest_risk_score_3s = -1.0
        self.latest_risk_score_5s = -1.0
        rospy.loginfo_throttle(
            1.0,
            (
                "risk_conditioned_command_adapter reset episode reason=%s "
                "target_x=%.3f target_y=%.3f episode_age=%.3f"
            ),
            reason,
            self.target_x,
            self.target_y,
            self._episode_age(now),
        )

    def _has_active_episode(self):
        return self.goal_received and self.episode_start_time is not None

    def _goal_distance_from_current(self, goal_position):
        if self.current_goal_position is None:
            return None
        if not self._all_finite(*(self.current_goal_position + goal_position)):
            return None
        dx = goal_position[0] - self.current_goal_position[0]
        dy = goal_position[1] - self.current_goal_position[1]
        dz = goal_position[2] - self.current_goal_position[2]
        distance = math.sqrt(dx * dx + dy * dy + dz * dz)
        return distance if math.isfinite(distance) else None

    def _episode_age(self, now):
        if self.episode_start_time is None:
            return -1.0
        age = now - self.episode_start_time
        return age if math.isfinite(age) else -1.0

    def _compute_target_scale(self, now, base_scale):
        base_scale = self._clamp_scale(base_scale)
        if not self.enable_risk_conditioning:
            self._set_unavailable_scores_if_needed(now)
            return base_scale

        if not self.models_ready:
            self._set_unavailable_scores_if_needed(now)
            return base_scale

        if not self.goal_received or self.episode_start_time is None:
            self.latest_risk_score_3s = -1.0
            self.latest_risk_score_5s = -1.0
            return base_scale

        elapsed = now - self.episode_start_time
        if not math.isfinite(elapsed) or elapsed < 3.0:
            self.latest_risk_score_3s = -1.0
            self.latest_risk_score_5s = -1.0
            return base_scale

        selected_scale = base_scale
        risk_3s = self._infer_window_risk(self.model_3s, 3.0)
        if risk_3s is None:
            return self._previous_or_base(base_scale)
        self.latest_risk_score_3s = risk_3s
        if risk_3s >= self.risk_threshold_3s:
            selected_scale = min(selected_scale, self.soft_scale_3s)

        if elapsed < 5.0:
            self.latest_risk_score_5s = -1.0
            return self._clamp_scale(selected_scale)

        risk_5s = self._infer_window_risk(self.model_5s, 5.0)
        if risk_5s is None:
            return self._previous_or_base(base_scale)
        self.latest_risk_score_5s = risk_5s
        if risk_5s >= self.risk_threshold_5s:
            selected_scale = min(selected_scale, self.soft_scale_5s)
        if risk_5s >= self.hard_threshold_5s:
            selected_scale = min(selected_scale, self.hard_scale_5s)

        return self._clamp_scale(selected_scale)

    def _set_unavailable_scores_if_needed(self, now):
        if not self.goal_received or self.episode_start_time is None:
            self.latest_risk_score_3s = -1.0
            self.latest_risk_score_5s = -1.0
            return
        elapsed = now - self.episode_start_time
        if not math.isfinite(elapsed) or elapsed < 3.0:
            self.latest_risk_score_3s = -1.0
            self.latest_risk_score_5s = -1.0
        elif elapsed < 5.0:
            self.latest_risk_score_5s = -1.0

    def _infer_window_risk(self, model, window_sec):
        feature_row = self._build_feature_row(window_sec)
        if feature_row is None:
            rospy.logwarn_throttle(
                1.0,
                "cannot compute required %.0fs online features; falling back safely",
                window_sec,
            )
            return None
        probability = model.infer_probability(feature_row)
        if probability is None or not math.isfinite(probability):
            rospy.logwarn_throttle(
                1.0,
                "%.0fs risk model produced non-finite output; keeping previous safe scale",
                window_sec,
            )
            return None
        return probability

    def _build_feature_row(self, max_window_sec):
        if not self.goal_received or self.episode_start_time is None:
            return None
        if not self._all_finite(self.target_x, self.target_y, self.target_z, self.payload_target_z):
            return None

        wind_force_norm = self._wind_force_norm()
        feature_row = {
            "wind_force_norm": wind_force_norm if math.isfinite(wind_force_norm) else 0.0,
            "target_x": self.target_x,
            "target_y": self.target_y,
            "target_z": self.target_z,
            "payload_target_z": self.payload_target_z,
        }

        for window_sec in self._required_windows(max_window_sec):
            window_features = self._compute_window_features(window_sec)
            if window_features is None:
                return None
            feature_row.update(window_features)

        return feature_row

    @staticmethod
    def _required_windows(max_window_sec):
        windows = []
        for window in (3.0, 5.0, 10.0, 15.0):
            if window <= max_window_sec + 1e-9:
                windows.append(window)
        return windows

    def _compute_window_features(self, window_sec):
        window_label = self._window_label(window_sec)
        prefix = "early_%ss_" % window_label
        end_time = self.episode_start_time + window_sec
        samples = [
            sample
            for sample in self.samples
            if self.episode_start_time <= sample["time"] <= end_time + 1e-9
        ]
        if not samples:
            return None

        uav_speeds = [sample["uav_speed"] for sample in samples]
        payload_speeds = [sample["payload_speed"] for sample in samples]
        swing_angles = [sample["swing_angle_deg"] for sample in samples]
        wind_norms = [sample["wind_force_norm"] for sample in samples]

        start_position = self._first_position(samples)
        end_position = self._last_position(samples)
        start_distance = self._target_distance(start_position)
        end_distance = self._target_distance(end_position)
        target_progress = (
            start_distance - end_distance
            if math.isfinite(start_distance) and math.isfinite(end_distance)
            else math.nan
        )

        values = {
            prefix + "max_uav_speed": self._max_or_nan(uav_speeds),
            prefix + "max_payload_speed": self._max_or_nan(payload_speeds),
            prefix + "mean_uav_speed": self._mean_or_nan(uav_speeds),
            prefix + "mean_payload_speed": self._mean_or_nan(payload_speeds),
            prefix + "max_swing_angle_deg": self._max_or_nan(swing_angles),
            prefix + "p95_swing_angle_deg": self._percentile(swing_angles, 95.0),
            prefix + "mean_swing_angle_deg": self._mean_or_nan(swing_angles),
            prefix + "max_wind_force_norm": self._max_or_nan(wind_norms),
            prefix + "mean_wind_force_norm": self._mean_or_nan(wind_norms),
            prefix + "target_distance_end": end_distance,
            prefix + "target_progress": target_progress,
        }

        if not all(math.isfinite(value) for value in values.values()):
            return None
        return values

    def _append_episode_sample(self, now):
        if not self.goal_received or self.episode_start_time is None:
            return
        if now < self.episode_start_time:
            return
        if self.uav_odom is None or self.payload_odom is None:
            return

        uav_speed = self._odom_speed(self.uav_odom)
        payload_speed = self._odom_speed(self.payload_odom)
        swing_angle_deg = self._compute_swing_angle_deg()
        wind_force_norm = self._wind_force_norm()
        if not self._all_finite(uav_speed, payload_speed, swing_angle_deg, wind_force_norm):
            return

        uav_pos = self.uav_odom.pose.pose.position
        self.samples.append(
            {
                "time": now,
                "uav_speed": uav_speed,
                "payload_speed": payload_speed,
                "swing_angle_deg": swing_angle_deg,
                "wind_force_norm": wind_force_norm,
                "uav_position": (uav_pos.x, uav_pos.y, uav_pos.z),
            }
        )

        max_keep_time = self.episode_start_time + 15.0
        if now > max_keep_time + 5.0 and len(self.samples) > 1:
            self.samples = [sample for sample in self.samples if sample["time"] <= max_keep_time + 1e-9]

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

    def _apply_rate_limit(self, target_scale, previous_scale, now):
        target_scale = self._clamp_scale(target_scale)
        if previous_scale is None or not math.isfinite(previous_scale):
            return target_scale

        if self.last_publish_time is None or not math.isfinite(self.last_publish_time):
            dt = 1.0 / max(self.publish_rate, 1e-3)
        else:
            dt = now - self.last_publish_time
            if not math.isfinite(dt) or dt <= 0.0:
                dt = 1.0 / max(self.publish_rate, 1e-3)

        max_step = max(0.0, self.scale_rate_limit_per_sec) * dt
        delta = target_scale - previous_scale
        if delta > max_step:
            return previous_scale + max_step
        if delta < -max_step:
            return previous_scale - max_step
        return target_scale

    def _previous_or_base(self, base_scale):
        if self.previous_speed_scale is not None and math.isfinite(self.previous_speed_scale):
            return self._clamp_scale(self.previous_speed_scale)
        return self._clamp_scale(base_scale)

    def _clamp_scale(self, value):
        if not math.isfinite(value):
            value = self.previous_speed_scale if self.previous_speed_scale is not None else 1.0
        lower = min(self.min_scale, self.max_scale)
        upper = max(self.min_scale, self.max_scale)
        return max(lower, min(upper, value))

    def _safe_score(self, value):
        if math.isfinite(value):
            return max(-1.0, min(1.0, value))
        return -1.0

    def _wind_force_norm(self):
        if self.wind_force is None:
            return 0.0
        wind = self.wind_force.vector
        norm = self._vector_norm(wind.x, wind.y, wind.z)
        return norm if math.isfinite(norm) else 0.0

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

    def _target_distance(self, position):
        if position is None or not self._all_finite(self.target_x, self.target_y):
            return math.nan
        xy_distance = math.sqrt((position[0] - self.target_x) ** 2 + (position[1] - self.target_y) ** 2)
        if not math.isfinite(self.target_z):
            return xy_distance
        return math.sqrt(xy_distance * xy_distance + (position[2] - self.target_z) ** 2)

    @staticmethod
    def _first_position(samples):
        for sample in samples:
            position = sample.get("uav_position")
            if position is not None and all(math.isfinite(value) for value in position):
                return position
        return None

    @staticmethod
    def _last_position(samples):
        for sample in reversed(samples):
            position = sample.get("uav_position")
            if position is not None and all(math.isfinite(value) for value in position):
                return position
        return None

    @staticmethod
    def _mean_or_nan(values):
        finite = [value for value in values if math.isfinite(value)]
        if not finite:
            return math.nan
        return sum(finite) / len(finite)

    @staticmethod
    def _max_or_nan(values):
        finite = [value for value in values if math.isfinite(value)]
        if not finite:
            return math.nan
        return max(finite)

    @staticmethod
    def _percentile(values, percent):
        finite = sorted(value for value in values if math.isfinite(value))
        if not finite:
            return math.nan
        if len(finite) == 1:
            return finite[0]
        rank = (len(finite) - 1) * percent / 100.0
        low_index = int(math.floor(rank))
        high_index = int(math.ceil(rank))
        if low_index == high_index:
            return finite[low_index]
        weight = rank - low_index
        return finite[low_index] * (1.0 - weight) + finite[high_index] * weight

    @staticmethod
    def _window_label(window_sec):
        if abs(window_sec - round(window_sec)) < 1e-9:
            return str(int(round(window_sec)))
        return ("%g" % window_sec).replace(".", "p")

    @staticmethod
    def _odom_is_finite(odom):
        position = odom.pose.pose.position
        velocity = odom.twist.twist.linear
        return RiskConditionedCommandAdapter._all_finite(
            position.x,
            position.y,
            position.z,
            velocity.x,
            velocity.y,
            velocity.z,
        )

    @staticmethod
    def _vector_norm(x_value, y_value, z_value):
        if not RiskConditionedCommandAdapter._all_finite(x_value, y_value, z_value):
            return math.nan
        return math.sqrt(x_value * x_value + y_value * y_value + z_value * z_value)

    @staticmethod
    def _all_finite(*values):
        return all(math.isfinite(value) for value in values)


def main():
    rospy.init_node("risk_conditioned_command_adapter")
    RiskConditionedCommandAdapter()
    rospy.spin()


if __name__ == "__main__":
    main()
