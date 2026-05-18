# AutoTrans Codex Instructions

请用中文回答，但保留所有文件路径、函数名、变量名、包名、topic 名称、launch 文件名和命令为英文原样。

## Project Context

This project is HKUST-Aerial-Robotics/AutoTrans, deployed as a ROS1 catkin workspace.

Environment:
- OS: Ubuntu 20.04 WSL
- ROS: Noetic
- Workspace root: ~/projects/autotrans_ws
- Repository root: ~/projects/autotrans_ws/src/AutoTrans
- Current active branch: high-level-command-adaptation
- Main demo launch command:
  cd ~/projects/autotrans_ws
  source /opt/ros/noetic/setup.bash
  source devel/setup.bash
  roslaunch payload_planner simple_run.launch

Current project status:
- ROS Noetic is installed successfully.
- catkin_make -DCMAKE_BUILD_TYPE=Release succeeds.
- RViz opens successfully.
- roslaunch payload_planner simple_run.launch starts successfully.
- 2D Nav Goal in RViz triggers planning and simulation response.
- Stage 2-B drag-wind benchmark has been implemented.
- Stage 3 planner-side command adaptation has been added.
- Current focus is Stage 3-C strong-wind repeated validation.
- Current comparison goal: original AutoTrans vs fixed scale 0.85 vs `policy_mode=wind_level` scale 0.85 using repeated Trial 2 success rate.
- Original AutoTrans strong-wind Trial 2 showed mixed repeated evidence: 1/3 valid, 2/3 invalid.
- Future Stage 3 evaluation should use repeated success-rate comparisons, not single-run conclusions.

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

Do not commit generated experiment outputs:
- CSV files
- PNG files
- TXT log/output files

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

## Standard Experiment Commands

Run baseline trial scripts from the repository root:

cd ~/projects/autotrans_ws/src/AutoTrans

Set drag-wind configuration:

python3 experiments/scripts/set_drag_wind_config.py --level none
python3 experiments/scripts/set_drag_wind_config.py --level strong

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
5. Do not modify controller, simulator, planner source, or generated directories unless explicitly requested.
6. Do not change core algorithm logic unless explicitly requested.
7. Prefer small, reversible changes.
8. Do not run simulation or RViz unless explicitly requested.
9. Do not commit or push unless explicitly instructed.
10. Do not commit generated CSV/PNG/TXT files.
11. Keep explanations beginner-friendly.
12. Preserve all file paths, function names, variable names, package names, topic names, launch file names, and commands in English.
13. Do not run long simulations unless explicitly requested.

After editing, report:
   - exact changed files
   - why each file was changed
   - verification command
   - whether commit was created
   - whether push was performed

## Codex Approval and Sandbox Policy

- Prefer static checks over heavy commands.
- Do not run `catkin_make`, `roslaunch`, RViz, simulation, or long-running trial commands unless explicitly requested.
- For most edit tasks, Codex should provide the build/run commands for the user to execute manually.
- Lightweight commands allowed by default:
  - `sed` / `grep` / `rg` file inspection
  - `git diff --check`
  - `git diff --stat`
  - `git status --short`
  - `python3 -m py_compile` for edited Python scripts
- If a command triggers sandbox retry or approval, do not repeatedly retry it. Stop and report the exact command for the user to run manually.
- Do not commit or push unless explicitly instructed.

## Local Codex Sandbox Note

- The local Codex sandbox may fail with `bwrap: Unknown option --perms`.
- For documentation-only and small static-edit tasks, it is acceptable to use:

  codex -C ~/projects/autotrans_ws/src/AutoTrans -s danger-full-access -a never

- When using `danger-full-access`, Codex must obey strict project constraints:
  - only edit allowed files
  - do not run `catkin_make`
  - do not run `roslaunch`
  - do not run simulation
  - do not launch RViz
  - do not modify `build/`, `devel/`, `install/`
  - do not stage generated CSV/PNG/TXT files
  - do not push unless explicitly requested
- Lightweight commands are allowed:
  - `git status --short`
  - `git diff --check`
  - `git diff --stat`
  - `sed`/`grep`/`rg` inspection
  - `python3 -m py_compile` for edited Python scripts
- If a command would require ROS runtime, long-running simulation, or workspace-level build, Codex should print the exact command and ask the user to run it manually.
- `pre_codex_checkpoint.sh` should remain a pre-edit check, not a post-edit check.
- For auto-commit tasks, Codex should commit only allowed files and report the latest SHA from `git rev-parse HEAD`.

## Auto-Commit Policy For Low-Risk Tasks

- For documentation-only tasks and small static-code tasks, Codex may commit automatically only if the user explicitly says auto-commit is allowed.
- Auto-commit is allowed only when all of these are true:
  - `git diff --check` passes
  - `git status --short` contains only allowed files
  - no generated CSV/PNG/TXT files are staged
  - no `build/`, `devel/`, or `install/` files are staged
  - no planner/controller/simulator files are modified unless explicitly allowed
  - no simulation/RViz was run
- Standard pre-edit commands:
  - `tools/pre_codex_checkpoint.sh`
  - `git branch --show-current`
  - `git rev-parse HEAD`
  - `git status --short`
- Standard post-edit commands:
  - `git diff --check`
  - `git status --short`
  - `git add <allowed files only>`
  - `git commit -m "<task-specific message>"`
  - `git rev-parse HEAD`
  - `git status`
- Codex should output:
  - changed files
  - verification results
  - commit SHA from `git rev-parse HEAD`
  - whether push was performed
- Do not push unless the user explicitly requests push.
- If any command triggers sandbox retry or approval, do not repeatedly retry. Stop and report the exact command for the user to run manually.

## Frozen Safety Constraints

- Do not modify `controller/**`, `uav_simulator/**`, `planner/**`, or generated directories unless explicitly requested.
- Do not modify `build/**`, `devel/**`, or `install/**`.
- Do not commit generated CSV/PNG/TXT files.
- Do not run simulation or RViz unless explicitly asked.
- For edit tasks, inspect files first and propose a minimal edit plan before modifying.
- Do not commit or push unless explicitly instructed.

## Stage 2-B Wind Benchmark Notes

- Stage 2-B drag-wind benchmark is implemented.
- Strong wind uses `wind_max_force: 0.0075`.
- Strong wind logging annotation uses `wind_force_norm: 0.007500`.
- `wind_signal_publisher` publishes `/wind_force` as an annotation/logging signal.
- Actual drag wind is configured through `uav_simulator/uav_simulator/config/so3_quadrotor.yaml`.
- Use `experiments/scripts/set_drag_wind_config.py` to switch wind levels.
- Always restore wind config to `none` after wind experiments.

## Stage 3 Command-Adaptation Notes

Planner runtime adaptation topics are absolute topic names:

- `/command_adaptation/speed_scale`
- `/command_adaptation/acceleration_scale`

Planner topic mode should use:

- `manager/enable_command_adaptation=true`
- `manager/adaptation_mode=topic`
- `manager/require_adaptation_topic_ready=true`

Restore planner params to no-op after experiments:

- `enable_command_adaptation=false`
- `adaptation_mode=none`
- `speed_scale=1.0`
- `acceleration_scale=1.0`
- `require_adaptation_topic_ready=false`

## Heuristic Adapter Notes

- The independent `command_adaptation` package lives under `experiments/command_adaptation`.
- `heuristic_command_adapter` supports `policy_mode=wind_level`.
- `heuristic_command_adapter` also supports `policy_mode=risk_reactive`.
- `policy_mode=wind_level` is the current recommended/default candidate.
- `policy_mode=risk_reactive` is experimental, not default, because it can react too late and produced mixed/invalid runs.
- `wind_level` strong scale is currently `0.85` unless a task explicitly changes it.
- Do not claim `wind_level` is final; it is a candidate requiring repeated validation.

## Analyzer and Validity Notes

Formal Stage 3 analysis should use target-error args:

--target_x
--target_y
--target_z
--payload_target_z
--target_xy_tolerance 0.5

- Interpret `valid_run_suggested` together with target-error metrics.
- `command_speed_scale` and `command_acceleration_scale` are logged and analyzed.

## Current Experiment Direction

Next major task: Stage 3-C success-rate comparison.

Compare:

- A. original AutoTrans
- B. fixed XML scale `0.85`
- C. `policy_mode=wind_level` scale `0.85`

Use repeated Trial 2 runs, not single-run metrics. Record invalid runs; do not hide them.

## Stage 4 Risk Learning Workflow

Stage 4-A dataset builder:

- Use `experiments/scripts/build_stage4_risk_dataset.py` to build the supervised risk dataset.
- The manifest is `experiments/protocols/stage4_risk_manifest.json`.
- Generated datasets under `experiments/datasets/` are ignored and should not be committed.

Stage 4-B risk predictor baseline:

- Use `experiments/scripts/train_stage4_risk_predictor.py` to train/evaluate the baseline risk predictor.
- Generated results under `experiments/results/` are ignored and should not be committed.

Stage 4 sklearn experiments:

- Use the dedicated Python venv:
  ~/venvs/autotrans-stage4
- Activate with:
  source ~/venvs/autotrans-stage4/bin/activate
- Verified versions:
  numpy==1.24.4
  scipy==1.10.1
  scikit-learn==1.3.2
- Do not use system Python for sklearn experiments because system Python has incompatible numpy/scipy/sklearn packages.
- Generated outputs under `experiments/results/` and `experiments/datasets/*.csv` should not be committed.
- The venv is only for offline learning scripts; do not run ROS/catkin/roslaunch from this venv.

Current dataset status:

- The first dataset has 15 Stage 3-C strong Trial 2 runs.
- `original`: 3/5 valid.
- `fixed_s085`: 2/5 valid.
- `windlevel_s085`: 3/5 valid.
- The dataset is too small for final claims.

Current learning conclusion:

- Early dynamic features show more promise than metadata-only features.
- The current predictor is pipeline validation, not a final algorithm result.

Stage 4-H risk-conditioned adapter status:

- `risk_adapter_v1` is the strongest learned adapter candidate so far.
- `risk_adapter_v1` policy:
  - `soft_scale_3s=0.75`
  - `soft_scale_5s=0.65`
  - `hard_scale_5s=0.60`
  - `risk_threshold_3s=0.5`
  - `risk_threshold_5s=0.5`
  - `hard_threshold_5s=0.7`
  - `scale_rate_limit_per_sec=0.5`

Stage 4-J balanced 30-repeat result:

- Stage 4-J balanced Trial 4/5/6 comparison is complete.
- Paper-facing metric is strict-valid / `label_strict_invalid`, not raw
  `valid_run_suggested` alone.
- `risk_adapter_v1`: 23/30.
- `original`: 18/30.
- `fixed_s085`: 18/30.
- `windlevel_s085`: 16/30.
- `risk_adapter_v1` is the strongest aggregate candidate among these four
  methods.
- `risk_adapter_v1` is strongest on Trial 5 and Trial 6.
- `fixed_s085` remains strongest on Trial 4.
- Do not claim statistical significance, safety guarantee, final online
  robustness, or that `risk_adapter_v1` beats every baseline on every target.

Stage 4-R tuned fixed-scale frontier result:

- `fixed_s080` achieved 24/30 strict-valid in balanced Trial 4/5/6.
- `fixed_s080` per-trial counts: Trial 4 8/10, Trial 5 9/10, Trial 6 7/10.
- `risk_adapter_v1` achieved 23/30 on the same balanced Trial 4/5/6 set.
- `fixed_s080` slightly exceeds `risk_adapter_v1` by 1/30 after tuned
  fixed-scale frontier screening.
- Do not claim `risk_adapter_v1` is overall best after including `fixed_s080`.
- `risk_adapter_v1` still outperforms `original`, `fixed_s085`, and
  `windlevel_s085`.
- `fixed_s080` is a strong static operating point, not a safety guarantee.
- The next method target is `risk_adapter_v2` / a calibrated risk governor that
  can match or exceed the tuned fixed frontier while preserving adaptivity.

Stage 4-S risk_adapter_v2 design:

- Stage 4-S is the next algorithmic direction.
- `risk_adapter_v2` should be a calibrated risk-conditioned execution governor,
  not simple threshold tuning.
- `risk_adapter_v2` should use `fixed_s080` as the static frontier reference.
- Do not claim `risk_adapter_v1` is overall best after Stage 4-R.
- Do not run more fixed-scale frontier before the Stage 4-S design is
  documented.
- The design protocol is
  `experiments/protocols/stage4s_risk_adapter_v2_design.md`.

Stage 4-T goal-repeat artifact diagnostics:

- Future Stage 4 evaluations must label the goal protocol explicitly:
  `goal_repeat=1` is the single-goal mission protocol, and `goal_repeat=10` is
  the repeated-goal / post-arrival replan stress protocol.
- Do not interpret `goal_repeat=10` results as generic single-goal mission
  results.
- Stage 4-T2 strong-wind Trial 4 diagnostic showed `risk_adapter_v2` was `3/3`
  strict-valid under `goal_repeat=1` but `0/3` under `goal_repeat=10`; all
  `risk_adapter_v2` `goal_repeat=10` failures occurred after arrival and after
  post-arrival goal publishes.
- `fixed_s080` remains the tuned frontier for the repeated-goal protocol, but
  single-goal mission performance must be evaluated separately.
- Do not claim all prior invalid runs are caused by the goal-repeat artifact;
  `fixed_s080` still had Trial 4 pre-arrival failures under `goal_repeat=1`.
- Stage 4-U2 now provides the current `goal_repeat=1` single-goal evidence;
  use it before any `risk_adapter_v2` threshold change.
- Do not modify planner same-goal handling yet; keep it as a future
  system-level intervention after diagnostics.

Stage 4-U single-goal mission screening:

- Stage 4-U screened `fixed_s080` and `risk_adapter_v2` under strong wind with
  `goal_repeat=1`, Trial 4/5/6, repeat1-3.
- `risk_adapter_v2`: 9/9 strict-valid.
- `fixed_s080`: 6/9 strict-valid.
- This is diagnostic screening, not final statistical evidence.
- Check Trial 6 efficiency because `risk_adapter_v2` used a low mean scale
  around `0.666`.

Stage 4-U2 single-goal 10-repeat expansion:

- Stage 4-U2 expanded `fixed_s080` and `risk_adapter_v2` under strong wind with
  `goal_repeat=1`, Trial 4/5/6, repeat1-10.
- Single-goal protocol (`goal_repeat=1`) now includes the completed Stage
  4-X2 matrix: `windlevel_s085` 26/30, `risk_adapter_v1` 25/30,
  `risk_adapter_v21` 25/30, `fixed_s085` 22/30, and `original`,
  `fixed_s080`, and `risk_adapter_v2` 21/30 strict-valid.
- Per-trial counts: `fixed_s080` Trial 4 7/10, Trial 5 6/10, Trial 6 8/10;
  `risk_adapter_v2` Trial 4 9/10, Trial 5 6/10, Trial 6 6/10.
- Repeated-goal protocol (`goal_repeat=10`): `fixed_s080` 24/30 and
  `risk_adapter_v1` 23/30 remain the key Stage 4-R/4-J references.
- Do not claim `risk_adapter_v2` beats `fixed_s080` overall yet.
- `risk_adapter_v2.1` should reduce long-duration `0.65` use and consider
  `0.70` or `0.75` for high-risk states unless severe risk persists.
- Future Stage 4 result tables must separate single-goal mission and
  repeated-goal stress protocols.

Stage 4-V risk_adapter_v2.1 design:

- Stage 4-V is the current algorithmic step after Stage 4-U2.
- The design protocol is
  `experiments/protocols/stage4v_risk_adapter_v21_design.md`.
- Do not claim `risk_adapter_v2` beats `fixed_s080` overall; they tied at
  `21/30` under the single-goal protocol.
- Stage 4-V2 implemented `policy_mode=risk_adapter_v21` as a separate mode
  while keeping `risk_adapter_v2` unchanged.
- Stage 4-V3 screened `risk_adapter_v21` under strong wind with
  `goal_repeat=1`, Trial 4/5/6, repeat1-3.
- `risk_adapter_v21`: 9/9 strict-valid in the Stage 4-V3 screening.
- The screening avoided long-duration `0.65` behavior; Trial 5 and Trial 6
  used mean scale around `0.711` with minimum `0.70`.
- Stage 4-V4 expanded `risk_adapter_v21` to 10 repeats under `goal_repeat=1`.
- `risk_adapter_v21`: 25/30 strict-valid under the single-goal protocol.
- Per-trial counts: Trial 4 10/10, Trial 5 9/10, Trial 6 6/10.
- After Stage 4-X2, `risk_adapter_v21` is no longer the highest completed
  single-goal aggregate method; `windlevel_s085` achieved 26/30, while
  `risk_adapter_v1` and `risk_adapter_v21` tied at 25/30.
- Trial 6 remains a bottleneck for `risk_adapter_v21` because it achieved
  6/10 there while `fixed_s080` achieved 8/10.
- Goal-reissue stress protocol (`goal_repeat=10`) remains separate:
  `fixed_s080` 24/30, `risk_adapter_v1` 23/30, and corrected
  `risk_adapter_v21` 20/30.
- `risk_adapter_v21` is not the strongest goal-reissue stress method and
  should not be described as a cross-protocol final winner.
- Stage 4-W3 updated protocol-split paper assets, and Stage 4-Y is the current
  paper narrative state before further tuning.
- Do not claim statistical significance or a safety guarantee.
- No planner/controller/simulator changes are needed for the next policy step.

Stage 4-X0 final evaluation specification:

- The protocol is
  `experiments/protocols/stage4x_final_evaluation_spec.md`.
- Use paper-facing protocol names:
  - single-goal mission protocol: `goal_repeat=1`
  - goal-reissue stress protocol: `goal_repeat=10`
- Current single-goal included methods are complete: `windlevel_s085` 26/30,
  `risk_adapter_v1` 25/30, `risk_adapter_v21` 25/30, `fixed_s085` 22/30,
  and `original`, `fixed_s080`, and `risk_adapter_v2` 21/30 strict-valid.
- Current goal-reissue stress included methods are `original` 18/30,
  `fixed_s085` 18/30, `windlevel_s085` 16/30, `risk_adapter_v1` 23/30, and
  `fixed_s080` 24/30 strict-valid; Stage 4-X1 adds corrected
  `risk_adapter_v21` 20/30 strict-valid.
- Remaining completion matrix before final claims:
  - none; Stage 4-X2 completed the missing single-goal baselines.
- Next experiment order:
  1. completed in Stage 4-X1: run `risk_adapter_v21` under goal-reissue
     stress (`goal_repeat=10`)
  2. completed in Stage 4-X2: run missing single-goal baselines
     (`goal_repeat=1`)
  3. update protocol-split paper assets
  4. decide final method
- Final-method decision rule:
  - if `risk_adapter_v21` is strongest or near strongest in both protocols,
    freeze `risk_adapter_v21` as the final method
  - if `risk_adapter_v21` is strong in single-goal but weak in stress, do
    failure analysis before a new variant
- Do not create `risk_adapter_v21.1`, `risk_adapter_v22`, or another new
  variant before protocol-split paper assets and failure analysis are updated.
- Do not claim `risk_adapter_v21` beats all single-goal baselines; Stage 4-X2
  shows `windlevel_s085` is higher in the completed single-goal aggregate.
- Do not claim statistical significance, safety guarantee, or mixed-protocol
  aggregate results.

Stage 4-X1 corrected risk_adapter_v21 goal-reissue stress result:

- The result document is
  `experiments/protocols/stage4x_risk_adapter_v21_goalreissue_result.md`.
- Duplicate CSV issue was found in Trial 4 repeat2-5; Trial 4 repeat3-5 were
  rerun and the corrected set was recorded after confirming `No duplicate
  csv_path detected`.
- Protocol: strong wind, `goal_repeat=10`, goal-reissue / post-arrival replan
  stress protocol, Trial 4/5/6, repeat1-10.
- Corrected `risk_adapter_v21` result: Trial 4 4/10, Trial 5 9/10, Trial 6
  7/10, aggregate 20/30 strict-valid.
- Goal-reissue stress aggregate order is now `fixed_s080` 24/30,
  `risk_adapter_v1` 23/30, `risk_adapter_v21` 20/30, `original` 18/30,
  `fixed_s085` 18/30, and `windlevel_s085` 16/30.
- Trial 4 is the main stress weakness for `risk_adapter_v21`.
- Stress failures are not exclusively post-arrival; many Trial 4 stress
  failures occur before arrival.
- Do not freeze `risk_adapter_v21` as a cross-protocol final method.
- Do not create `risk_adapter_v22` yet.
- Stage 4-X2 completed the missing single-goal baselines, Stage 4-W3 updated
  protocol-split paper assets, and Stage 4-Y is the current paper narrative
  state.

Stage 4-X2 missing single-goal baseline completion:

- The helper script is
  `experiments/scripts/run_stage4_single_goal_baseline_completion.py`.
- The protocol is
  `experiments/protocols/stage4x_single_goal_baseline_completion_protocol.md`.
- Stage 4-X2 completed the previously missing single-goal methods:
  `original`, `fixed_s085`, `windlevel_s085`, and `risk_adapter_v1`.
- Protocol: strong wind, `goal_repeat=1`, single-goal mission protocol,
  Trial 4/5/6, repeat1-10.
- Naming convention:
  `stage4x_singlegoal_<method>_strong_trial<trial>_goalrepeat1_repeat<repeat>`.
- The completed result document is
  `experiments/protocols/stage4x_single_goal_baseline_completion_result.md`.
- Default helper behavior is dry-run / print-only. Do not run simulation from
  Codex unless explicitly requested.
- `wind_signal_publisher` must be running for Stage 4-X2 runs.
- `windlevel_s085` requires
  `roslaunch command_adaptation heuristic_command_adapter.launch policy_mode:=wind_level`.
- `risk_adapter_v1` requires
  `roslaunch command_adaptation risk_conditioned_command_adapter.launch`
  with `enable_risk_conditioning:=true`, `policy_mode:=risk_conditioned`,
  `risk_threshold_3s:=0.5`, `risk_threshold_5s:=0.5`,
  `hard_threshold_5s:=0.7`, `soft_scale_3s:=0.75`,
  `soft_scale_5s:=0.65`, `hard_scale_5s:=0.60`, and
  `scale_rate_limit_per_sec:=0.5`.
- Completed single-goal results:
  - `windlevel_s085`: 26/30 strict-valid.
  - `risk_adapter_v1`: 25/30 strict-valid.
  - `risk_adapter_v21`: 25/30 strict-valid.
  - `fixed_s085`: 22/30 strict-valid.
  - `original`: 21/30 strict-valid.
  - `fixed_s080`: 21/30 strict-valid.
  - `risk_adapter_v2`: 21/30 strict-valid.
- `windlevel_s085` is currently the strongest completed single-goal method.
- `risk_adapter_v1` and `risk_adapter_v21` tie as the strongest
  learned/adaptive risk-conditioned variants in the completed single-goal
  aggregate.
- `risk_adapter_v21` is no longer the highest single-goal aggregate method
  after adding `windlevel_s085`.
- `risk_adapter_v21` still improves over `original`, `fixed_s080`,
  `fixed_s085`, and `risk_adapter_v2`.
- `fixed_s085` and `windlevel_s085` both use 0.85-like scaling but through
  different execution paths; `windlevel_s085` is topic-based and must be
  treated separately.
- Trial 6 remains a bottleneck for `risk_adapter_v1` and
  `risk_adapter_v21`.
- Do not create `risk_adapter_v22` or another new method variant before
  updating protocol-split paper assets and failure analysis.
- Do not claim `risk_adapter_v21` beats all single-goal baselines.
- Stage 4-W3 regenerated protocol-split paper assets with completed
  single-goal and corrected goal-reissue stress tables.

Stage 4-Y paper results narrative:

- The current paper-facing narrative draft is
  `experiments/protocols/stage4y_results_narrative_draft.md`.
- Stage 4-W3 protocol-split paper assets are complete.
- Current framing should be learned risk-conditioned execution governor,
  dual-protocol evaluation, strong heuristic/static frontier comparison, and
  failure-mode-aware analysis.
- Single-goal mission protocol (`goal_repeat=1`): `windlevel_s085` is highest
  at 26/30; `risk_adapter_v1` and `risk_adapter_v21` tie at 25/30.
- Goal-reissue stress protocol (`goal_repeat=10`): `fixed_s080` is highest at
  24/30; `risk_adapter_v1` is second at 23/30; `risk_adapter_v21` is 20/30.
- No current learned variant dominates both protocols.
- Do not claim `risk_adapter_v21` is overall best.
- Do not create mixed-protocol aggregate claims.
- Do not claim statistical significance.
- Do not claim a safety guarantee.
- Next recommended work: build a failure-mode summary table/figure, inspect
  Trial 4 stress and Trial 6 bottlenecks, and do not create
  `risk_adapter_v22` immediately.

Stage 4-Z failure-mode paper assets:

- The generator is
  `experiments/scripts/generate_stage4_failure_mode_paper_assets.py`.
- The protocol is
  `experiments/protocols/stage4z_failure_mode_paper_assets_protocol.md`.
- Stage 4-Z outputs support the Stage 4-Y protocol-split Results narrative
  with failure-mode tables and a failure-group stacked-bar figure.
- Generated outputs go under
  `experiments/results/stage4_failure_mode_paper_assets/` and should not be
  committed.
- `failure_group` is diagnostic, not perfect root-cause proof; strict-valid
  remains the paper-facing metric.
- Stage 4-Z2 distinguishes all-run accounting from paper-facing failure
  analysis:
  - all-run failure groups use `valid_or_warning` for strict-valid runs,
    including warning-style diagnostic labels.
  - invalid-only failure-group tables and
    `stage4_failure_group_invalid_only_stacked_bar.png` exclude strict-valid
    runs and should be used for paper failure-analysis figures.
- The Stage 4-Z2 result is recorded in
  `experiments/protocols/stage4z_failure_mode_paper_assets_result.md`.
- Stage 4-Z2 generated `390` run rows and `110` strict-invalid runs.
- Invalid-only failure groups support failure-aware analysis but do not change
  the protocol-split success ranking.
- Next step: diagnose Trial 4 goal-reissue stress failures for
  `risk_adapter_v21` and the Trial 6 bottleneck across single-goal and stress.
- Do not create `risk_adapter_v22` or another new variant before this
  diagnosis is complete.

Stage 4-AA targeted diagnosis assets:

- The generator is
  `experiments/scripts/generate_stage4_targeted_diagnosis_assets.py`.
- The protocol is
  `experiments/protocols/stage4aa_targeted_diagnosis_protocol.md`.
- Stage 4-AA targets:
  - Trial 4 goal-reissue stress failures for `risk_adapter_v21`.
  - Trial 6 bottleneck behavior across single-goal and goal-reissue stress
    protocols.
- Generated outputs go under
  `experiments/results/stage4_targeted_diagnosis/` and should not be
  committed.
- Use Stage 4-AA outputs to inspect timing, arrival behavior, command-scale
  behavior, and diagnostic failure groups before any new variant design.
- Do not create `risk_adapter_v22` before reviewing Stage 4-AA outputs.

Stage 4-AA2 representative trace plots:

- The plotter is
  `experiments/scripts/plot_stage4_representative_failure_traces.py`.
- The protocol is
  `experiments/protocols/stage4aa_representative_trace_protocol.md`.
- Generated outputs go under
  `experiments/results/stage4_representative_traces/` and should not be
  committed.
- Stage 4-AA2 generated representative traces for the `risk_adapter_v22`
  decision gate; Stage 4-AA3 recorded the human review.
- The trace set should inspect Trial 4 goal-reissue stress
  `risk_adapter_v21` failures, Trial 4 stress comparison against
  `fixed_s080` / `risk_adapter_v1`, and the Trial 6 single-goal bottleneck.
- AA3 review is complete and did not justify immediate `risk_adapter_v22`.
- Do not create `risk_adapter_v22` yet; do not create a Trial-4-specific
  patch.

Stage 4-AA3 representative trace review:

- The review result is
  `experiments/protocols/stage4aa_representative_trace_review_result.md`.
- Human review inspected the AA2 representative plots for single-goal Trial 6
  and goal-reissue stress Trial 4.
- AA3 supports the Stage 4-AB balanced-governor framing:
  `risk_adapter_v1` remains the tentative balanced learned /
  risk-conditioned protagonist.
- `risk_adapter_v21` remains a strong nominal variant / ablation, not the
  cross-protocol final method.
- Do not create `risk_adapter_v22` yet.
- If a future variant is attempted, it should use a generic risk-health-aware,
  phase-aware, reference / trajectory-health-aware, or command /
  state-health-aware mechanism, not simple threshold tuning or a
  Trial-4-specific patch.
- Next recommended step: Stage 4-AC balanced robustness / protocol regret
  assets.

Stage 4-AC balanced robustness assets:

- The generator is
  `experiments/scripts/generate_stage4_balanced_robustness_assets.py`.
- The protocol is
  `experiments/protocols/stage4ac_balanced_robustness_assets_protocol.md`.
- The result document is
  `experiments/protocols/stage4ac_balanced_robustness_assets_result.md`.
- Generated outputs go under
  `experiments/results/stage4_balanced_robustness_assets/` and should not be
  committed.
- Stage 4-AC2 balanced robustness / protocol regret result is complete.
- Protocol oracles: `windlevel_s085` is the single-goal oracle at `26/30`;
  `fixed_s080` is the goal-reissue stress oracle at `24/30`.
- Complete cross-protocol balanced ranking excludes `risk_adapter_v2` because
  its goal-reissue stress result is missing.
- `risk_adapter_v1` has the best mean valid count (`24.0/30`), best
  worst-protocol valid count (`23/30`), and lowest total regret (`2`).
- Pareto-frontier methods: `windlevel_s085`, `fixed_s080`, and
  `risk_adapter_v1`.
- `risk_adapter_v21` should not be Pareto-frontier because `risk_adapter_v1`
  has the same single-goal count and higher stress count.
- `risk_adapter_v1` is the tentative balanced learned / risk-conditioned
  protagonist.
- Do not create `risk_adapter_v22` yet.
- Stage 4-AD freezes the paper figure/table plan using protocol-split
  success, balanced robustness / protocol regret, invalid-only failure groups,
  and representative trace case studies.
- Stage 4-AE paper outline / section skeleton is complete.
- Next step: Stage 4-AF paper Abstract and Introduction draft.

Stage 4-AD paper figure/table plan:

- The plan document is
  `experiments/protocols/stage4ad_paper_figure_table_plan.md`.
- Main paper evidence layers: protocol-split success, balanced robustness /
  protocol regret, invalid-only failure groups, and representative trace case
  studies.
- Main protagonist remains `risk_adapter_v1` as the balanced learned /
  risk-conditioned execution governor.
- `windlevel_s085` and `fixed_s080` should be framed as protocol specialists.
- `risk_adapter_v21` should remain a strong nominal / single-goal variant or
  ablation, not the final method.
- Main planned items: protocol-split balanced robustness table, architecture
  figure, protocol split diagram, Pareto plot, protocol regret bar chart,
  invalid-only failure group stacked bar, and representative trace case study.
- Do not create `risk_adapter_v22` yet.
- Stage 4-AE paper outline / section skeleton is complete.
- Next step: Stage 4-AF paper Abstract and Introduction draft.

Stage 4-AE paper outline / section skeleton:

- The outline document is
  `experiments/protocols/stage4ae_paper_outline_section_skeleton.md`.
- Target style: IROS/ICRA/RA-L system-method paper.
- The skeleton defines candidate titles, core thesis, draft abstract,
  Introduction structure, contribution bullets, Related Work, Method,
  Experimental Setup, Results, Discussion, Limitations, Appendix plan, and a
  claim audit table.
- Paper protagonist remains `risk_adapter_v1` as the tentative balanced
  learned / risk-conditioned governor.
- `risk_adapter_v21` remains an ablation / strong nominal variant, not the
  final method.
- Do not create `risk_adapter_v22` yet.
- Next step after AE: Stage 4-AF paper Abstract and Introduction draft.

Stage 4-AB paper reframing decision:

- The decision document is
  `experiments/protocols/stage4ab_paper_reframing_decision.md`.
- Protocol-split comparison and failure-mode analysis are complete enough to
  reset the paper framing away from a `risk_adapter_v21`-as-winner story.
- Tentative paper protagonist: `risk_adapter_v1` as the most balanced learned
  / risk-conditioned execution governor.
- `risk_adapter_v21` should be treated as a strong nominal variant / ablation,
  not the final cross-protocol method.
- `windlevel_s085` is the single-goal mission specialist at `26/30`.
- `fixed_s080` is the goal-reissue stress specialist at `24/30`.
- `risk_adapter_v1` has the lowest current dual-protocol regret relative to
  the protocol oracle: `(26 - 25) + (24 - 23) = 2`.
- Stage 4-AD now freezes the paper figure/table plan that follows this
  balanced-governor framing.
- Stage 4-AE now formalizes the paper outline and section skeleton.
- Next step: Stage 4-AF paper Abstract and Introduction draft.
- Do not create `risk_adapter_v22` yet.
- Only consider `risk_adapter_v22` if later evidence shows a generic
  phase-aware, failure-aware, risk-health-aware, reference /
  trajectory-health-aware, or command / state-health-aware mechanism; do not
  make a Trial-4-specific patch.

Earlier Stage 4-H limited-repeat results:

Trial 4:

- `original`: 4/5 valid.
- `fixed_s085`: 5/5 valid.
- `windlevel_s085`: 1/5 valid.
- `risk_adapter_v1`: 4/5 valid.

Trial 5:

- `original`: 3/5 strict-valid.
- `fixed_s085`: 2/5 valid.
- `windlevel_s085`: 3/5 valid.
- `risk_adapter_v0`: 2/5 valid.
- `risk_adapter_v1`: 5/5 valid.

Trial 6:

- `original`: 2/5 valid.
- `fixed_s085`: 2/5 valid.
- `windlevel_s085`: 2/5 valid.
- `risk_adapter_v0`: 4/5 valid.
- `risk_adapter_v1`: 4/5 valid.

Aggregate Trial 4+5+6:

- `original`: 9/15.
- `fixed_s085`: 9/15.
- `windlevel_s085`: 6/15.
- `risk_adapter_v1`: 13/15.

Stage 4-I result table generator:

- Use `experiments/scripts/summarize_stage4h_adapter_results.py` to generate
  Stage 4-H limited evaluation Markdown/CSV tables.
- The committed manifest is
  `experiments/protocols/stage4h_adapter_limited_eval_manifest.json`.
- Generated outputs under `experiments/results/` are ignored and should not be
  committed.

Stage 4-H/4-I/4-J claim limits:

- Do not claim statistical significance.
- Do not claim a safety guarantee.
- Do not claim final online robustness.
- Do not claim `risk_adapter_v1` is overall best after including `fixed_s080`.
- Do not hide the Trial 4 repeat5 and Trial 6 repeat1 `risk_adapter_v1`
  failures.
- Do not claim `risk_adapter_v1` beats `fixed_s085` on every target, because
  `fixed_s085` is 9/10 on Trial 4 while `risk_adapter_v1` is 7/10.

Next recommended Stage 4-J/4-R/4-S work:

- Freeze the current Stage 4-J balanced comparison.
- Freeze `fixed_s080` as the current tuned fixed-scale frontier.
- Next reporting step should be paper-ready table/figure generation updated to
  include `fixed_s080`, not more simulation or fixed-scale screening.
- Next algorithmic step should be Stage 4-S `risk_adapter_v2` design before any
  implementation or additional fixed-scale frontier runs.
- Consider a failure-mode distribution table.
- Only after Stage 4-S documentation and paper table updates, consider
  `risk_adapter_v2` implementation or path-feasibility diagnostics.

Safety:

- Do not modify planner/controller/simulator for Stage 4 dataset/model tasks.
- Do not run simulation, RViz, or `catkin_make` in Codex for Stage 4 learning scripts.
- Use static checks only unless the user explicitly asks otherwise.

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
