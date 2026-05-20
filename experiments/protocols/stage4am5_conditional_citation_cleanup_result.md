# Stage 4-AM5 Conditional Citation Cleanup Result

## Executive Summary

Stage 4-AM5 audits the active citation usage and BibTeX state of the RA-L
Paper 1 scaffold under `paper/stage4_governor_ral/`.

The active manuscript citations use only the 20 ready-to-use keys already
recorded in Stage 4-AM4. `paper/stage4_governor_ral/refs.bib` contains the
same 20 active BibTeX entries. No missing BibTeX keys and no unused active
BibTeX entries were found.

The conditional keys from Stage 4-AM3 / Stage 4-AM4 are excluded from active
Paper 1 citations and active BibTeX entries. They remain only as comments /
TODOs until metadata is verified. No fabricated citations were added.

No LaTeX compile was run in Stage 4-AM5 because Stage 4-AV2 already compiled
the scaffold with no undefined citations or bibliography warnings, and AM5 did
not change active citation syntax or `refs.bib`.

## Commands / Inspections Run

Inspect active citation usage:

```bash
grep -R "\\cite" -n paper/stage4_governor_ral/main.tex \
  paper/stage4_governor_ral/sections \
  paper/stage4_governor_ral/refs.bib
```

Inspect active BibTeX entries:

```bash
grep -n "@.*{" paper/stage4_governor_ral/refs.bib
```

Extract unique cited keys:

```bash
perl -0777 -ne 'while(/\\cite\w*\s*\{([^}]*)\}/g){ for $k (split /\s*,\s*/, $1){ $k =~ s/^\s+|\s+$//g; print "$k\n" if $k ne ""; }}' \
  paper/stage4_governor_ral/main.tex \
  paper/stage4_governor_ral/sections/*.tex | sort -u
```

Extract unique BibTeX keys:

```bash
grep -n "@.*{" paper/stage4_governor_ral/refs.bib \
  | sed -E 's/.*\{([^,]+),.*/\1/' | sort -u
```

Compare cited keys against BibTeX keys:

```bash
comm -23 <cited_keys> <bib_keys>
comm -13 <cited_keys> <bib_keys>
```

Check conditional key status:

```bash
for k in Barikbin2019WindPayloadTracking \
  Wabersich2021PredictiveSafetyFilter \
  Jin2025NeuralPredictorPayload \
  Monteleone2023BalanceResilienceBenchmark \
  Dogga2023AutoARTS; do
  rg -n "$k" paper/stage4_governor_ral/main.tex \
    paper/stage4_governor_ral/sections \
    paper/stage4_governor_ral/refs.bib || true
done
```

## Active Cited Keys

Active cited key count: 20.

- `Andersson2017RiskAwareActiveLearning`
- `Bauersfeld2021NeuroBEM`
- `Cameron2024DomesticRobotFailureOutcomes`
- `Garone2016ExplicitReferenceGovernor`
- `Garone2017ReferenceCommandGovernorsSurvey`
- `GuerreroSanchez2017SwingAttenuation`
- `Hsu2024SafetyFilterUnifiedView`
- `Koren2018AdaptiveStressTesting`
- `Lee2010GeometricTrackingSE3`
- `Lee2024HybridDisturbancePrediction`
- `Li2021ActionGovernor`
- `Li2023AutoTrans`
- `Muller2019MeasureTargetConfusion`
- `Nalic2020StressTestingScenarioBasedADS`
- `Nicotra2016UAVRobustERG`
- `Saviolo2022PITCN`
- `Son2020ObstacleAvoidanceSuspendedLoad`
- `Sreenath2013DifferentiallyFlatHybrid`
- `Torrente2021DataDrivenMPC`
- `UrbinaBrito2021PredictivePayloadTransport`

## BibTeX Entries

Active BibTeX entry count: 20.

The active `refs.bib` keys exactly match the active cited keys.

Missing BibTeX keys:

- none

Unused active BibTeX keys:

- none

## Conditional Citation Status

| conditional key | active citation status | active BibTeX status | AM5 decision |
| --- | --- | --- | --- |
| `Barikbin2019WindPayloadTracking` | absent from active `\cite{...}` | absent as active BibTeX entry | Keep only as TODO until venue/year metadata is verified. |
| `Wabersich2021PredictiveSafetyFilter` | absent from active `\cite{...}` | absent as active BibTeX entry | Keep only as TODO until DOI / Automatica metadata is verified. |
| `Jin2025NeuralPredictorPayload` | absent from active `\cite{...}` | absent as active BibTeX entry | Keep only as TODO until final metadata is verified. |
| `Monteleone2023BalanceResilienceBenchmark` | absent from active `\cite{...}` | absent as active BibTeX entry | Keep only as TODO until complete author-list metadata is verified. |
| `Dogga2023AutoARTS` | absent from active `\cite{...}` | absent as active BibTeX entry | Keep only as TODO until official USENIX URL metadata is verified. |

The conditional keys currently appear only in comments / TODOs in
`paper/stage4_governor_ral/refs.bib` and
`paper/stage4_governor_ral/sections/02_related_work.tex`.

## Changes Made

- Added this AM5 audit result document.
- Updated RA-L scaffold documentation to state that active citations were
  checked and conditional citations remain excluded from the active Paper 1
  bibliography unless later verified.
- Updated Stage 4-AM3 / AM4 / AT2 / scripts / AGENTS documentation to record
  the AM5 citation decision.

No active citation command was changed. No active BibTeX entry was added,
removed, or fabricated. `paper/stage4_governor_ral/refs.bib` was left
unchanged because it already contains only ready-to-use active entries.

## Remaining Citation TODOs

- Verify conditional citation metadata before any future activation:
  - `Barikbin2019WindPayloadTracking`
  - `Wabersich2021PredictiveSafetyFilter`
  - `Jin2025NeuralPredictorPayload`
  - `Monteleone2023BalanceResilienceBenchmark`
  - `Dogga2023AutoARTS`
- Perform final citation style polish for venue-specific formatting if needed.
- Re-run the final LaTeX compile after any future citation or BibTeX edits.

## Boundaries

- No fabricated citations.
- No web metadata was used.
- No conditional citations were added as active BibTeX entries.
- No simulation, RViz, `roslaunch`, `catkin_make`, training scripts, figure
  generation scripts, or new experimental runs were performed.
- No LaTeX compile was run in AM5.
- No `risk_adapter_v22` was created.
