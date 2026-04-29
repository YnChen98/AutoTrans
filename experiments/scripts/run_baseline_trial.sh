#!/usr/bin/env bash
set -euo pipefail

TRIAL_NAME="baseline_trial"
GOAL_X="0.0"
GOAL_Y="-1.2"
GOAL_Z="0.0"
DURATION_SEC="75"
FRAME_ID="world"
STARTUP_WAIT_SEC="20"
GOAL_REPEAT="3"
GOAL_INTERVAL_SEC="1.0"

WORKSPACE_ROOT="${HOME}/projects/autotrans_ws"
REPO_ROOT="${WORKSPACE_ROOT}/src/AutoTrans"
LOG_DIR="${REPO_ROOT}/experiments/logs"
FIGURE_DIR="${REPO_ROOT}/experiments/figures"

DEMO_PID=""
LOGGER_PID=""
MARKER_FILE=""
RUN_LOG_DIR=""

usage() {
  cat <<'EOF'
Usage:
  bash experiments/scripts/run_baseline_trial.sh [options]

Options:
  --name <trial_name>      Trial name used in temporary process logs.
  --x <goal_x>             Goal x position. Default: 0.0
  --y <goal_y>             Goal y position. Default: -1.2
  --z <goal_z>             Goal z position. Default: 0.0, matching RViz 2D Nav Goal.
  --duration <seconds>     Logging duration after goal publish. Default: 75
  --frame_id <frame_id>    Goal frame_id. Default: world
  --startup_wait <seconds> Conservative wait after topics/messages are ready. Default: 20
  --goal_repeat <count>    Number of one-shot goal publications. Default: 3
  --goal_interval <sec>    Delay between repeated goal publications. Default: 1.0
  -h, --help               Show this help.
EOF
}

parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --name)
        if [[ $# -lt 2 ]]; then
          echo "ERROR: --name requires a value" >&2
          exit 2
        fi
        TRIAL_NAME="$2"
        shift 2
        ;;
      --x)
        if [[ $# -lt 2 ]]; then
          echo "ERROR: --x requires a value" >&2
          exit 2
        fi
        GOAL_X="$2"
        shift 2
        ;;
      --y)
        if [[ $# -lt 2 ]]; then
          echo "ERROR: --y requires a value" >&2
          exit 2
        fi
        GOAL_Y="$2"
        shift 2
        ;;
      --z)
        if [[ $# -lt 2 ]]; then
          echo "ERROR: --z requires a value" >&2
          exit 2
        fi
        GOAL_Z="$2"
        shift 2
        ;;
      --duration)
        if [[ $# -lt 2 ]]; then
          echo "ERROR: --duration requires a value" >&2
          exit 2
        fi
        DURATION_SEC="$2"
        shift 2
        ;;
      --frame_id)
        if [[ $# -lt 2 ]]; then
          echo "ERROR: --frame_id requires a value" >&2
          exit 2
        fi
        FRAME_ID="$2"
        shift 2
        ;;
      --startup_wait)
        if [[ $# -lt 2 ]]; then
          echo "ERROR: --startup_wait requires a value" >&2
          exit 2
        fi
        STARTUP_WAIT_SEC="$2"
        shift 2
        ;;
      --goal_repeat)
        if [[ $# -lt 2 ]]; then
          echo "ERROR: --goal_repeat requires a value" >&2
          exit 2
        fi
        GOAL_REPEAT="$2"
        shift 2
        ;;
      --goal_interval)
        if [[ $# -lt 2 ]]; then
          echo "ERROR: --goal_interval requires a value" >&2
          exit 2
        fi
        GOAL_INTERVAL_SEC="$2"
        shift 2
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        echo "ERROR: unknown argument: $1" >&2
        usage >&2
        exit 2
        ;;
    esac
  done
}

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "ERROR: required command not found: $1" >&2
    exit 1
  fi
}

stop_process() {
  local pid="$1"
  local label="$2"

  if [[ -z "${pid}" ]]; then
    return
  fi

  if kill -0 "${pid}" >/dev/null 2>&1; then
    echo "Stopping ${label} process ${pid}..."
    kill -INT "${pid}" >/dev/null 2>&1 || true
    for _ in {1..15}; do
      if ! kill -0 "${pid}" >/dev/null 2>&1; then
        wait "${pid}" 2>/dev/null || true
        return
      fi
      sleep 1
    done
    echo "Process ${pid} did not exit after SIGINT; sending SIGTERM."
    kill -TERM "${pid}" >/dev/null 2>&1 || true
    wait "${pid}" 2>/dev/null || true
  fi
}

cleanup() {
  local exit_code=$?
  trap - EXIT INT TERM

  stop_process "${LOGGER_PID}" "autotrans_logger"
  stop_process "${DEMO_PID}" "simple_run.launch"

  if [[ -n "${MARKER_FILE}" && -f "${MARKER_FILE}" ]]; then
    rm -f "${MARKER_FILE}"
  fi

  exit "${exit_code}"
}

wait_for_topic() {
  local topic="$1"
  local timeout_sec="$2"
  local start_time
  local current_time
  start_time="$(date +%s)"

  echo "Waiting for topic ${topic}..."
  while true; do
    if rostopic list 2>/dev/null | grep -qx "${topic}"; then
      echo "Found topic ${topic}."
      return
    fi

    current_time="$(date +%s)"
    if (( current_time - start_time >= timeout_sec )); then
      echo "ERROR: timed out waiting for topic ${topic}" >&2
      exit 1
    fi

    sleep 1
  done
}

wait_for_message() {
  local topic="$1"
  local timeout_sec="$2"

  echo "Waiting for one message on ${topic}..."
  if ! timeout "${timeout_sec}" rostopic echo -n 1 "${topic}" >/dev/null 2>&1; then
    echo "ERROR: timed out waiting for message on ${topic}" >&2
    exit 1
  fi
}

subscriber_count() {
  local topic="$1"

  rostopic info "${topic}" 2>/dev/null \
    | awk '
      /^Subscribers:/ {in_subscribers=1; next}
      /^Publishers:/ {in_subscribers=0}
      /^$/ {in_subscribers=0}
      in_subscribers && /^[[:space:]]*\*/ {count++}
      END {print count + 0}
    '
}

wait_for_subscribers() {
  local topic="$1"
  local min_count="$2"
  local timeout_sec="$3"
  local start_time
  local current_time
  local count
  start_time="$(date +%s)"

  echo "Waiting for at least ${min_count} subscriber(s) on ${topic}..."
  while true; do
    count="$(subscriber_count "${topic}")"
    if (( count >= min_count )); then
      echo "Topic ${topic} has ${count} subscriber(s)."
      return
    fi

    current_time="$(date +%s)"
    if (( current_time - start_time >= timeout_sec )); then
      echo "ERROR: timed out waiting for subscribers on ${topic}; current subscriber count=${count}" >&2
      exit 1
    fi

    sleep 1
  done
}

latest_new_csv() {
  find "${LOG_DIR}" -maxdepth 1 -name 'autotrans_log_*.csv' -newer "${MARKER_FILE}" -printf '%T@ %p\n' 2>/dev/null \
    | sort -nr \
    | awk 'NR == 1 {print $2}'
}

publish_goal() {
  local goal_msg
  goal_msg="header:
  stamp: now
  frame_id: '${FRAME_ID}'
pose:
  position:
    x: ${GOAL_X}
    y: ${GOAL_Y}
    z: ${GOAL_Z}
  orientation:
    x: 0.0
    y: 0.0
    z: 0.0
    w: 1.0"

  echo "Publishing PoseStamped goal to /move_base_simple/goal:"
  printf '%s\n' "${goal_msg}"

  for ((i = 1; i <= GOAL_REPEAT; i++)); do
    echo "Goal publish ${i}/${GOAL_REPEAT}"
    rostopic pub -1 /move_base_simple/goal geometry_msgs/PoseStamped "${goal_msg}"
    if (( i < GOAL_REPEAT )); then
      sleep "${GOAL_INTERVAL_SEC}"
    fi
  done
}

main() {
  parse_args "$@"
  trap cleanup EXIT INT TERM

  require_command roslaunch
  require_command rostopic
  require_command timeout
  require_command python3

  if [[ ! -d "${WORKSPACE_ROOT}" ]]; then
    echo "ERROR: workspace root does not exist: ${WORKSPACE_ROOT}" >&2
    exit 1
  fi

  if [[ ! -f "/opt/ros/noetic/setup.bash" ]]; then
    echo "ERROR: missing ROS setup file: /opt/ros/noetic/setup.bash" >&2
    exit 1
  fi

  if [[ ! -f "${WORKSPACE_ROOT}/devel/setup.bash" ]]; then
    echo "ERROR: missing workspace setup file: ${WORKSPACE_ROOT}/devel/setup.bash" >&2
    exit 1
  fi

  mkdir -p "${LOG_DIR}" "${FIGURE_DIR}"
  MARKER_FILE="$(mktemp)"
  touch "${MARKER_FILE}"
  RUN_LOG_DIR="$(mktemp -d "/tmp/autotrans_${TRIAL_NAME}_XXXXXX")"

  cd "${WORKSPACE_ROOT}"
  # shellcheck disable=SC1091
  source /opt/ros/noetic/setup.bash
  # shellcheck disable=SC1091
  source devel/setup.bash

  echo "Starting payload_planner simple_run.launch..."
  roslaunch payload_planner simple_run.launch >"${RUN_LOG_DIR}/simple_run.log" 2>&1 &
  DEMO_PID=$!
  echo "simple_run.launch PID: ${DEMO_PID}"
  echo "simple_run.launch log: ${RUN_LOG_DIR}/simple_run.log"

  wait_for_topic "/move_base_simple/goal" 90
  wait_for_topic "/visual_slam/odom" 90
  wait_for_topic "/payload_odom" 90
  wait_for_topic "/cable_info" 90
  wait_for_topic "/so3cmd" 90
  wait_for_topic "/pcl_render_node/cloud" 90
  wait_for_subscribers "/move_base_simple/goal" 1 90
  wait_for_message "/visual_slam/odom" 30
  wait_for_message "/payload_odom" 30
  wait_for_message "/pcl_render_node/cloud" 60
  wait_for_message "/so3cmd" 30

  echo "Conservative startup wait: ${STARTUP_WAIT_SEC} seconds..."
  sleep "${STARTUP_WAIT_SEC}"

  echo "Starting autotrans_logger..."
  roslaunch autotrans_logger state_logger.launch >"${RUN_LOG_DIR}/state_logger.log" 2>&1 &
  LOGGER_PID=$!
  echo "autotrans_logger PID: ${LOGGER_PID}"
  echo "autotrans_logger log: ${RUN_LOG_DIR}/state_logger.log"
  sleep 5

  publish_goal

  echo "Sleeping for ${DURATION_SEC} seconds..."
  sleep "${DURATION_SEC}"

  stop_process "${LOGGER_PID}" "autotrans_logger"
  LOGGER_PID=""
  stop_process "${DEMO_PID}" "simple_run.launch"
  DEMO_PID=""

  local latest_csv
  latest_csv="$(latest_new_csv || true)"

  cd "${REPO_ROOT}"
  echo "Running offline analysis..."
  python3 experiments/autotrans_logger/scripts/analyze_log.py

  if [[ -n "${latest_csv}" ]]; then
    echo "Latest CSV from this run: ${latest_csv}"
  else
    echo "WARNING: no new CSV was detected after this run." >&2
  fi

  local summary_path="${FIGURE_DIR}/metrics_summary.txt"
  if [[ -f "${summary_path}" ]]; then
    echo "Metrics summary:"
    cat "${summary_path}"
  else
    echo "WARNING: metrics summary not found: ${summary_path}" >&2
  fi
}

main "$@"
