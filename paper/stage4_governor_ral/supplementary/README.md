# RA-L Supplementary Material Placeholder

This directory is the supplementary-material placeholder for the Stage 4-AV
RA-L-oriented scaffold.

Supplementary candidates:

- full run tables
- full protocol-split summaries
- invalid-only failure tables
- representative trace packages
- launch / protocol settings
- strict-valid metric details
- `risk_adapter_v1` parameter table
- risk model feature-schema summary
- risk model artifact checksum manifest from
  `experiments/protocols/stage4au3_risk_model_artifact_manifest.md`
- duplicate CSV audit notes if needed
- optional video / trace package if the submission uses one

Generated experiment outputs are not copied automatically into this scaffold.
Only intentionally packaged, submission-facing supplementary files should be
added later.

Stage 4-AY confirms that final supplementary package decisions remain before
actual submission. In particular, decide whether to include risk model JSON
artifacts, checksum manifests, full CSV summaries, representative traces, or
video / trace packages in the RA-L submission package. Generated experiment
outputs should not be copied into this scaffold or committed unless they are
intentionally packaged as submission-facing supplementary material.

Stage 4-AZ human visual inspection found that Figure 6 is too crowded for its
current main-paper role. A later Figure 6 simplification may keep only key
signals in the main paper and shift full trace detail to supplementary material.
If this split is used, supplementary trace content should remain clearly tied
to the diagnostic-only claim boundary.

Claim boundaries remain the same as the main paper: no statistical
significance claim, no safety guarantee, no learned uniform domination, no
mixed-protocol aggregate as the main result, diagnostic-only failure groups,
and no `risk_adapter_v22`.
