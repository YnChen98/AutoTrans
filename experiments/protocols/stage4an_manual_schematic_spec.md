# Stage 4-AN Manual Schematic Specification

## Executive Summary

Stage 4-AN specifies the manual schematic requirements for Figure 1 and Figure
2 in the reframed Stage 4 paper. Figure 1 explains the stack-compatible
risk-conditioned execution-governor interface. Figure 2 explains the
protocol-split evaluation design.

No image files are created in this task. This document is a drawing
specification for a later schematic pass in PowerPoint, draw.io, Figma, TikZ,
or another chosen tool.

The schematics must preserve the current paper framing:

- `risk_adapter_v1` is the balanced learned / risk-conditioned protagonist.
- `windlevel_s085` is the single-goal specialist.
- `fixed_s080` is the goal-reissue stress specialist.
- `risk_adapter_v21` is a strong nominal / single-goal variant or ablation,
  not the final method.
- No `risk_adapter_v22` is part of the current paper figure plan.

## Figure 1: System Architecture Schematic

### Purpose

Figure 1 should show the stack-compatible execution governor. The schematic
must make clear that the governor does not replace the planner, payload MPC, or
SO3 controller. It should highlight the command-adaptation interface through
`speed_scale` and `acceleration_scale`.

### Required Visual Blocks

Use simple rectangular blocks or grouped boxes:

- Environment / strong wind / suspended-payload transport task.
- AutoTrans-like planner.
- Payload MPC.
- SO3 controller.
- UAV + suspended payload plant / simulator.
- Logger / diagnostics.
- Risk-conditioned execution governor.
- Risk input / risk score block.
- Command-adaptation interface.
- Output labels:
  - `speed_scale`
  - `acceleration_scale`

Recommended grouping:

- Put planner, payload MPC, SO3 controller, and plant in the main horizontal
  stack.
- Put the risk input / risk score block and execution governor above or below
  the main stack as an external layer.
- Put logger / diagnostics near the plant output.
- Put the command-adaptation interface between the governor and the command
  path.

### Required Arrows

Include these information/control-flow arrows:

- AutoTrans-like planner -> Payload MPC -> SO3 controller -> UAV + suspended
  payload plant / simulator.
- UAV + suspended payload plant / simulator -> Risk input / risk score block.
- Logger / diagnostics or plant logs -> Risk input / risk score block.
- Risk input / risk score block -> Risk-conditioned execution governor.
- Risk-conditioned execution governor -> Command-adaptation interface.
- Command-adaptation interface -> planner/MPC command path, labeled as
  modifying execution through `speed_scale` and `acceleration_scale`.
- UAV + suspended payload plant / simulator -> Logger / diagnostics.
- Logger / diagnostics -> failure-mode-aware analysis.

Do not draw the governor as replacing the planner, payload MPC, or SO3
controller. The visual relationship should be an external modulation layer,
not an inner-loop controller substitution.

### Caption Draft

Figure 1. Stack-compatible risk-conditioned execution-governor architecture.
The AutoTrans-like planner, payload MPC, and SO3 controller remain unchanged,
while an external governor uses risk-related inputs to publish `speed_scale`
and `acceleration_scale` through the command-adaptation interface. The logger
and diagnostics support failure-mode-aware analysis. The governor is empirical
and is not a formal safety filter or certified runtime assurance layer.

### Claim / Caveat

Supported claim:

- The proposed method is a stack-compatible execution governor that adapts
  execution aggressiveness through `speed_scale` and `acceleration_scale`.

Caveat:

- The figure does not claim a safety guarantee, certified runtime assurance, or
  replacement of the planner, payload MPC, or SO3 controller.

## Figure 2: Protocol Split Schematic

### Purpose

Figure 2 should explain why `goal_repeat=1` and `goal_repeat=10` are separate
protocols. The schematic must prevent the reader from interpreting the results
as one mixed-protocol aggregate.

### Required Visual Layout

Use two side-by-side panels with parallel time axes.

Left panel:

- Title: Single-goal mission protocol.
- Label: `goal_repeat=1`.
- Show one goal publish event.
- Show normal transport to target.
- Show arrival / hold.
- Primary test label: nominal single-goal execution.

Right panel:

- Title: Goal-reissue stress protocol.
- Label: `goal_repeat=10`.
- Show repeated same-goal publish events.
- Show transport plus repeated goal / replan / reference-update pressure.
- Show arrival and post-arrival / reissue interactions.
- Primary test label: goal-reissue stress and protocol robustness.

### Required Visual Elements

Each panel should include:

- A time axis.
- Goal publish markers.
- Arrival marker.
- Trajectory / reference update markers.
- A shaded stress interval or repeated-goal interval in the right panel.
- A visible note that the protocols are reported separately and are not
  combined into one aggregate.

Recommended layout:

- Use identical horizontal scales for the two panels if possible.
- Use one marker style for goal publishes, one for arrival, and one for
  reference updates.
- Keep labels short enough for a two-column IROS/ICRA/RA-L figure.

### Caption Draft

Figure 2. Protocol-split evaluation design. The single-goal mission protocol
uses `goal_repeat=1` and tests one commanded transport mission, whereas the
goal-reissue stress protocol uses `goal_repeat=10` and repeatedly republishes
the same goal to stress replan, reference-update, arrival, and post-arrival
behavior. Results are reported separately because the two protocols expose
different method rankings and should not be collapsed into a mixed-protocol
aggregate.

### Claim / Caveat

Supported claim:

- The protocol split exposes different method rankings and motivates separate
  reporting.

Caveat:

- The schematic is explanatory. It is not a result plot and does not by itself
  establish method performance.

## Style Guidelines

- Use consistent colors and shapes later, but do not rely on color alone.
- Use readable labels for a two-column IROS/ICRA/RA-L paper format.
- Keep the schematics simple enough for the main paper.
- Avoid excessive ROS topic names in the main figures; put full implementation
  details in the appendix.
- Use `speed_scale` and `acceleration_scale` labels exactly.
- Use `goal-reissue stress` for the protocol name in the final drawing.
- Avoid labels such as "safe", "certified", "guaranteed", or "safety filter"
  unless explicitly negated in the caveat.
- Make the visual hierarchy clear: Figure 1 is a method/interface schematic;
  Figure 2 is an evaluation-protocol schematic.

## Asset Naming Plan

Figure 1 final target:

- `experiments/results/stage4_paper_figure_package/main/fig1_architecture.png`
- `experiments/results/stage4_paper_figure_package/main/fig1_architecture.pdf`
- `experiments/results/stage4_paper_figure_package/main/fig1_architecture.svg`

Figure 2 final target:

- `experiments/results/stage4_paper_figure_package/main/fig2_protocol_split.png`
- `experiments/results/stage4_paper_figure_package/main/fig2_protocol_split.pdf`
- `experiments/results/stage4_paper_figure_package/main/fig2_protocol_split.svg`

Keep these TODO markdown files until final images exist:

- `experiments/results/stage4_paper_figure_package/TODO/fig1_architecture_TODO.md`
- `experiments/results/stage4_paper_figure_package/TODO/fig2_protocol_split_TODO.md`

## Checklist Before Drawing

- Verify final terminology: use goal-reissue stress, not repeated-goal stress
  unless referring to a legacy file name.
- Verify protagonist: `risk_adapter_v1`.
- Verify no `risk_adapter_v22`.
- Verify no mixed-protocol aggregate.
- Verify no safety guarantee language.
- Verify Figure 1 does not imply planner, payload MPC, or SO3 controller
  replacement.
- Verify Figure 2 uses separate panels for `goal_repeat=1` and
  `goal_repeat=10`.
- Verify captions include claim boundaries and caveats.
