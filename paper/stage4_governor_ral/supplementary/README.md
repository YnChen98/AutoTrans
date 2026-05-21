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

Stage 4-BA cleans paper-facing method names in the active manuscript and
Table 1. Internal tokens may still appear in supplementary implementation
references, artifact filenames, manifests, parameter documentation, and trace
packages where exact reproducibility requires the raw identifiers.

Stage 4-BB stops using the old generated Figure 1 / Figure 2 schematic images
as active main-paper visuals. Those generated schematics may remain as
historical/generated assets, but they should not be used as final RA-L
submission visuals after the placeholder workflow unless they are externally
redrawn or manually curated to final paper quality.

Stage 4-BE replaces the Figure 1 / Figure 2 placeholder boxes with TikZ vector
schematics. The old generated schematic PNG/SVG files are no longer active main
visuals; keep them only as historical/generated assets unless the team
intentionally packages them for provenance or comparison.

Stage 4-BJ replaces the active Figure 1 / Figure 2 TikZ schematic inputs with
deterministic nature-style matplotlib SVG / PDF / PNG assets. The old TikZ
files and old generated schematic assets are not active final visuals; keep
them only as historical scaffold / provenance material unless explicitly
packaged outside the main-paper visual set.

Stage 4-BD replaces the active five-panel Figure 6 trace block with a
simplified main-paper trace summary. Full trace detail, including the omitted
Fixed Scale 0.80 representative trace and risk-score traces, should remain in
supplementary material or archived trace assets if the final submission package
uses them. Keep these materials tied to the qualitative / diagnostic claim
boundary.

Stage 4-BF regenerates the active Figure 6 summary without unavailable
position-error placeholder text by using UAV XY displacement as the common
main-paper position signal. Full target-error, reference-error, risk-score, and
other trace details should remain supplementary / archived trace material if
used.

Stage 4-BG further polishes the main-paper presentation assets. Figure 4 and
Figure 5 now use paper-facing labels in the active main-paper PNG/SVG assets,
and Figure 6 keeps only the simplified main-paper signals with one global
legend. Full trace details and richer diagnostic tables should remain
supplementary / archived materials if the final submission package uses them.

Claim boundaries remain the same as the main paper: no statistical
significance claim, no safety guarantee, no learned uniform domination, no
mixed-protocol aggregate as the main result, diagnostic-only failure groups,
and no `risk_adapter_v22`.
