# Stage 4-AN2 Manual Schematic Generation Protocol

## Purpose

Stage 4-AN2 adds a deterministic offline generator for the paper's manual
schematics:

- Figure 1: stack-compatible execution-governor architecture.
- Figure 2: protocol-split evaluation.

The generator converts the Stage 4-AN manual schematic specification into
paper-ready PNG and SVG files. It does not run ROS, does not run simulation,
does not create new experimental evidence, and does not introduce
`risk_adapter_v22`.

## Inputs

Primary specification:

- `experiments/protocols/stage4an_manual_schematic_spec.md`

Source script:

- `experiments/scripts/generate_stage4_manual_schematics.py`

No external online assets, proprietary fonts, ROS runtime, or simulation logs
are required.

## Outputs

Default output directory:

- `experiments/results/stage4_paper_figure_package/main/`

Generated files:

- `fig1_architecture.png`
- `fig1_architecture.svg`
- `fig2_protocol_split.png`
- `fig2_protocol_split.svg`
- `fig1_fig2_schematic_summary.md`

Generated outputs under `experiments/results/` are ignored outputs and must not
be committed.

## How To Run

```bash
python3 experiments/scripts/generate_stage4_manual_schematics.py \
  --output-dir experiments/results/stage4_paper_figure_package/main \
  --print-summary
```

The script uses `matplotlib` only. It does not use `seaborn`, external image
assets, online resources, ROS, `catkin_make`, `roslaunch`, simulation, or RViz.

## Figure Content

### Figure 1

Figure 1 includes:

- strong wind / suspended-payload task block,
- AutoTrans-like planner,
- Payload MPC,
- SO3 controller,
- UAV + suspended payload plant / simulator,
- risk input / risk score block,
- risk-conditioned execution governor,
- command-adaptation interface,
- logger / diagnostics block,
- exact `speed_scale` and `acceleration_scale` labels.

The figure shows the planner -> payload MPC -> SO3 controller -> plant command
path, risk/log feedback into the governor, and the command-adaptation interface
modulating execution aggressiveness.

### Figure 2

Figure 2 uses two side-by-side panels:

- single-goal mission protocol, `goal_repeat=1`,
- goal-reissue stress protocol, `goal_repeat=10`.

The panels include time axes, goal publish markers, trajectory/reference update
markers, arrival markers, and a visible reminder that the protocols should be
reported separately rather than collapsed into a mixed-protocol aggregate.

## Style Constraints

- Use `matplotlib` only.
- Use deterministic block positions and marker positions.
- Use simple colors and shapes, but do not rely on color alone.
- Use editable SVG text by keeping `svg.fonttype=none`.
- Use non-proprietary `DejaVu Sans` as the font family.
- Keep labels short enough for IROS/ICRA/RA-L two-column formatting.
- Use exact labels `speed_scale` and `acceleration_scale`.
- Use the protocol name goal-reissue stress.

## Claim Boundaries

Figure 1 supports:

- the method is a stack-compatible execution governor,
- the governor adapts `speed_scale` and `acceleration_scale`,
- the planner, payload MPC, and SO3 controller remain unchanged.

Figure 1 does not support:

- a safety guarantee,
- certified runtime assurance,
- replacement of the planner, payload MPC, or SO3 controller.

Figure 2 supports:

- the two protocols test different behavior,
- protocol-split reporting is necessary,
- mixed-protocol aggregates should be avoided.

Figure 2 does not support:

- any method ranking by itself,
- statistical significance,
- a safety guarantee.

## Current Paper State

The generated schematics should preserve the current Stage 4 paper framing:

- `risk_adapter_v1` is the balanced learned / risk-conditioned protagonist.
- `windlevel_s085` is the single-goal specialist.
- `fixed_s080` is the goal-reissue stress specialist.
- `risk_adapter_v21` is a strong nominal / single-goal variant or ablation.
- `risk_adapter_v22` is not part of the current paper.

## Next Step

After Stage 4-AN2 outputs are generated and reviewed, the next paper-asset step
is Stage 4-AL3: refresh the paper figure package so Figure 1 and Figure 2 TODOs
can be replaced or supplemented by the generated schematic files. Stage 4-AM2
verified citation collection can proceed in parallel.

Stage 4-AL3 consumes these generated schematics by detecting the PNG/SVG files
in `experiments/results/stage4_paper_figure_package/main/` and adding them to
the package manifest as real main-paper assets. The AL3 package refresh does
not call this generator automatically and does not overwrite the generated
schematic files.
