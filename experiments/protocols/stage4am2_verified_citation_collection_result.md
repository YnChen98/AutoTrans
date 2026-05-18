# Stage 4-AM2 Verified Citation Collection Result

## Executive Summary

Stage 4-AM2 records the user-provided verified citation collection for the
reframed Stage 4 paper. The collection is organized by citation slots from
Stage 4-AK and Stage 4-AM.

This document does not finalize the bibliography, does not generate BibTeX,
and does not insert final citation keys into manuscript prose. It records only
the metadata provided in the verified citation list. Incomplete metadata is
marked as `TODO` / needs verification before final bibliography insertion.
Stage 4-AM3 now drafts section-level citation insertion guidance based on these
keys:
`experiments/protocols/stage4am3_citation_insertion_draft.md`.

The current paper framing remains:

- risk-conditioned execution governance for suspended-payload UAV transport
  under strong wind,
- protocol-split robustness evaluation,
- balanced robustness / protocol regret analysis,
- failure-mode-aware diagnosis.

`risk_adapter_v1` remains the tentative balanced learned / risk-conditioned
protagonist. `risk_adapter_v21` remains an ablation / strong nominal variant,
not the final method. Do not create `risk_adapter_v22`.

## Citation Groups

### Suspended-Payload UAV Transport And Control

This group supports the AutoTrans-like suspended-payload transport stack,
payload-aware planning / control background, geometric quadrotor control
backbone, wind / swing sensitivity, and the claim that the proposed governor
does not replace the planner, payload MPC, or SO3 controller.

Included citations:

- `Li2023AutoTrans`
- `Sreenath2013DifferentiallyFlatHybrid`
- `Son2020ObstacleAvoidanceSuspendedLoad`
- `UrbinaBrito2021PredictivePayloadTransport`
- `Lee2010GeometricTrackingSE3`
- `GuerreroSanchez2017SwingAttenuation`
- `Barikbin2019WindPayloadTracking`

### Runtime Governors / Reference Governors / Safety Filters

This group supports the conceptual boundary around reference / command
governors, action governors, runtime safety filters, and the distinction
between certified safety filters and the empirical execution governor used in
this paper.

Included citations:

- `Garone2017ReferenceCommandGovernorsSurvey`
- `Garone2016ExplicitReferenceGovernor`
- `Nicotra2016UAVRobustERG`
- `Li2021ActionGovernor`
- `Wabersich2021PredictiveSafetyFilter`
- `Hsu2024SafetyFilterUnifiedView`

### Learning-Enhanced Aerial Robustness

This group supports learning-enhanced aerial robustness, risk-aware learning,
hybrid aerodynamic modeling, data-driven MPC, physics-inspired temporal
learning, disturbance prediction, and payload-specific learned predictors.
These references should motivate risk-conditioned adaptation, not learned
uniform domination.

Included citations:

- `Andersson2017RiskAwareActiveLearning`
- `Bauersfeld2021NeuroBEM`
- `Torrente2021DataDrivenMPC`
- `Saviolo2022PITCN`
- `Lee2024HybridDisturbancePrediction`
- `Jin2025NeuralPredictorPayload`

### Benchmarking / Stress Testing / Failure Analysis

This group supports protocol-conditioned benchmarking, stress testing, repeated
perturbation protocols, and failure taxonomy / diagnostic-label framing.

Included citations:

- `Muller2019MeasureTargetConfusion`
- `Monteleone2023BalanceResilienceBenchmark`
- `Koren2018AdaptiveStressTesting`
- `Nalic2020StressTestingScenarioBasedADS`
- `Cameron2024DomesticRobotFailureOutcomes`
- `Dogga2023AutoARTS`

## Must-Cite Shortlist

- `Li2023AutoTrans`
- `Sreenath2013DifferentiallyFlatHybrid`
- `Son2020ObstacleAvoidanceSuspendedLoad`
- `Lee2010GeometricTrackingSE3`
- `Garone2017ReferenceCommandGovernorsSurvey`
- `Garone2016ExplicitReferenceGovernor`
- `Nicotra2016UAVRobustERG`
- `Andersson2017RiskAwareActiveLearning`
- `Torrente2021DataDrivenMPC`
- `Lee2024HybridDisturbancePrediction`
- `Muller2019MeasureTargetConfusion`
- `Koren2018AdaptiveStressTesting`

## Citation Table

| bibtex_key | priority | title | authors | venue_year | DOI_or_arXiv_or_URL | supported_claim | insertion_location | metadata_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `Li2023AutoTrans` | must-cite | AutoTrans: A Complete Planning and Control Framework for Autonomous UAV Payload Transportation | Haojia Li, Haokun Wang, Chen Feng, Fei Gao, Boyu Zhou, Shaojie Shen | IEEE Robotics and Automation Letters, 8(10), 2023, pp. 6859-6866 | DOI: 10.1109/LRA.2023.3313010 | AutoTrans-like suspended-payload stack; planner/control baseline context; contrast that our governor does not replace planner/MPC/controller. | Introduction; Related Work 2.1; Method; Experimental Setup | verified from user-provided list |
| `Sreenath2013DifferentiallyFlatHybrid` | must-cite | Trajectory Generation and Control of a Quadrotor With a Cable-Suspended Load—A Differentially-Flat Hybrid System | Koushil Sreenath, Nathan Michael, Vijay Kumar | ICRA 2013, pp. 4888-4895 | DOI: 10.1109/ICRA.2013.6631275 | Suspended-load trajectory generation and hybrid/differential-flatness foundation. | Introduction; Related Work 2.1 | verified from user-provided list |
| `Son2020ObstacleAvoidanceSuspendedLoad` | must-cite | Real-Time Optimal Trajectory Generation and Control of a Multi-Rotor With a Suspended Load for Obstacle Avoidance | Clark Youngdong Son, Hoseong Seo, Dohyun Jang, H. Jin Kim | IEEE Robotics and Automation Letters, 5(2), 2020, pp. 1915-1922 | DOI: 10.1109/LRA.2020.2967279 | Online optimal trajectory generation, obstacle avoidance, suspended-load-aware planning/control. | Introduction; Related Work 2.1 | verified from user-provided list |
| `UrbinaBrito2021PredictivePayloadTransport` | should-cite | A Predictive Control Strategy for Aerial Payload Transportation with an Unmanned Aerial Vehicle | Norberto Urbina-Brito, María-Eusebia Guerrero-Sánchez, Guillermo Valencia-Palomo, Omar Hernández-González, Francisco-Ronay López-Estrada, José Antonio Hoyo-Montaño | Mathematics, 9(15), 2021, Article 1822 | DOI: 10.3390/math9151822 | Payload MPC / predictive control for aerial payload transport; swing-angle constraints. | Related Work 2.1; Method | verified from user-provided list |
| `Lee2010GeometricTrackingSE3` | must-cite | Geometric Tracking Control of a Quadrotor UAV on SE(3) | Taeyoung Lee, Melvin Leok, N. Harris McClamroch | 49th IEEE Conference on Decision and Control, 2010, pp. 5420-5425 | DOI: 10.1109/CDC.2010.5717652 | SO(3) / SE(3) geometric quadrotor control backbone. | Related Work 2.1; Method | verified from user-provided list |
| `GuerreroSanchez2017SwingAttenuation` | should-cite | Swing-attenuation for a quadrotor transporting a cable-suspended payload | María-Eusebia Guerrero-Sánchez, Diego Alberto Mercado-Ravell, Rogelio Lozano, C. Daniel García-Beltrán | ISA Transactions, 68, 2017, pp. 433-449 | DOI: 10.1016/j.isatra.2017.01.027 | Swing attenuation and suspended-payload transport performance/risk. | Introduction; Related Work 2.1; Discussion | verified from user-provided list |
| `Barikbin2019WindPayloadTracking` | optional | Trajectory tracking for quadrotor UAV transporting cable-suspended payload in wind presence | Baharnaz Barikbin, Ahmad Fakharian | TODO verify venue/year details from provided DOI source | DOI: 10.1177/0142331218774606 | Wind presence in cable-suspended payload transport. | Introduction; Related Work 2.1; Experimental Setup | needs venue/year verification before manuscript insertion |
| `Garone2017ReferenceCommandGovernorsSurvey` | must-cite | Reference and command governors for systems with constraints: A survey on theory and applications | Emanuele Garone, Stefano Di Cairano, Ilya Kolmanovsky | Automatica, 75, 2017, pp. 306-328 | DOI: 10.1016/j.automatica.2016.08.013 | Reference/command governor concept as add-on scheme for constrained/pre-stabilized systems. | Related Work 2.2; Method; Discussion | verified from user-provided list |
| `Garone2016ExplicitReferenceGovernor` | must-cite | Explicit Reference Governor for Constrained Nonlinear Systems | Emanuele Garone, Marco M. Nicotra | IEEE Transactions on Automatic Control, 61(5), 2016, pp. 1379-1384 | DOI: 10.1109/TAC.2015.2476195 | Explicit reference governor concept and dynamic reference modulation. | Related Work 2.2; Method | verified from user-provided list |
| `Nicotra2016UAVRobustERG` | must-cite | A robust explicit reference governor for constrained control of Unmanned Aerial Vehicles | Marco M. Nicotra, Roberto Naldi, Emanuele Garone | American Control Conference, 2016 | DOI: 10.1109/ACC.2016.7526657 | Reference governor concept in UAV setting. | Related Work 2.2; Method; Discussion | verified from user-provided list |
| `Li2021ActionGovernor` | should-cite | Action Governor for Discrete-Time Linear Systems With Non-Convex Constraints | Nan Li, Kyoungseok Han, Anouck Girard, H. Eric Tseng, Dimitar Filev, Ilya Kolmanovsky | IEEE Control Systems Letters, 5(1), 2021, pp. 121-126 | DOI: 10.1109/LCSYS.2020.3000198 | Action governor / supervisory modification of nominal control signal. | Related Work 2.2 | verified from user-provided list |
| `Wabersich2021PredictiveSafetyFilter` | should-cite | A predictive safety filter for learning-based control of constrained nonlinear dynamical systems | Kim P. Wabersich, Melanie N. Zeilinger | Automatica, 2021 | arXiv: 1812.05506 | Safety-filter boundary; cite to distinguish our empirical governor from certified predictive safety filters. | Related Work 2.2; Method claim boundary; Discussion / Limitations | DOI missing; verify before final bibliography |
| `Hsu2024SafetyFilterUnifiedView` | should-cite | The Safety Filter: A Unified View of Safety-Critical Control in Autonomous Systems | Kai-Chieh Hsu, Haimin Hu, Jaime F. Fisac | Annual Review of Control, Robotics, and Autonomous Systems, 7, 2024, pp. 47-72 | DOI: 10.1146/annurev-control-071723-102940 | Safety filter / runtime intervention boundary; clarify our method is not certified. | Related Work 2.2; Discussion / Limitations | verified from user-provided list |
| `Andersson2017RiskAwareActiveLearning` | must-cite | Deep Learning Quadcopter Control via Risk-Aware Active Learning | Olov Andersson, Mariusz Wzorek, Patrick Doherty | Proceedings of the AAAI Conference on Artificial Intelligence, 31(1), 2017, pp. 3812-3818 | DOI: 10.1609/aaai.v31i1.11041 | Risk-aware learning in quadcopter control. | Related Work 2.3; Method motivation | verified from user-provided list |
| `Bauersfeld2021NeuroBEM` | should-cite | NeuroBEM: Hybrid Aerodynamic Quadrotor Model | Leonard Bauersfeld, Elia Kaufmann, Philipp Foehn, Sihao Sun, Davide Scaramuzza | Robotics: Science and Systems, 2021 | DOI: 10.15607/RSS.2021.XVII.042 | Hybrid aerodynamic modeling / learning-enhanced aerial robustness. | Related Work 2.3; Discussion / Future Work | verified from user-provided list |
| `Torrente2021DataDrivenMPC` | must-cite | Data-Driven MPC for Quadrotors | Guillem Torrente, Elia Kaufmann, Philipp Föhn, Davide Scaramuzza | IEEE Robotics and Automation Letters, 6(2), 2021, pp. 3769-3776 | DOI: 10.1109/LRA.2021.3061307 | Data-driven model enhancement integrated with MPC. | Related Work 2.3; Method motivation | verified from user-provided list |
| `Saviolo2022PITCN` | should-cite | Physics-Inspired Temporal Learning of Quadrotor Dynamics for Accurate Model Predictive Trajectory Tracking | Alessandro Saviolo, Guanrui Li, Giuseppe Loianno | IEEE Robotics and Automation Letters, 7(4), 2022, pp. 10256-10263 | DOI: 10.1109/LRA.2022.3192609 | Physics-inspired temporal learning plus MPC. | Related Work 2.3; Discussion / Future Work | verified from user-provided list |
| `Lee2024HybridDisturbancePrediction` | must-cite | Hybrid model-based and data-driven disturbance prediction for precise quadrotor trajectory tracking | Changhyeon Lee, Junwoo Jason Son, Seongwon Yoon, Soo Jeon, Soohee Han | Engineering Applications of Artificial Intelligence, 136(Part A), 2024, Article 108895 | DOI: 10.1016/j.engappai.2024.108895 | Hybrid model-based and data-driven disturbance prediction. | Related Work 2.3; Discussion / Future Work | verified from user-provided list |
| `Jin2025NeuralPredictorPayload` | should-cite | Neural Predictor for Flight Control With Payload | Ao Jin, Chenhao Li, Qinyi Wang, Ya Liu, Panfeng Huang, Fan Zhang | IEEE Robotics and Automation Letters, 10(7), 2025, pp. 7055-7062 | DOI: 10.1109/LRA.2025.3573624 | Payload-specific learned predictor integrated into MPC. | Related Work 2.3; Discussion / Future Work | verify final metadata before final bibliography because it is recent |
| `Muller2019MeasureTargetConfusion` | must-cite | Measuring Progress in Robotics: Benchmarking and the 'Measure-Target Confusion' | Vincent C. Müller | Book chapter in Metrics of Sensory Motor Coordination and Integration in Robots and Animals, 2019 | DOI: 10.1007/978-3-030-14126-4_9 | Benchmark/protocol scores are context-dependent; avoid measure-target confusion. | Introduction; Related Work 2.4; Discussion | verified from user-provided list |
| `Monteleone2023BalanceResilienceBenchmark` | should-cite | A method to benchmark the balance resilience of robots | Simone Monteleone, Francesco Negrello, Manuel G. Catalano, Antonio Bicchi, Manuel Garabini, plus full Frontiers author list to verify | Frontiers in Robotics and AI, 2023 | DOI: 10.3389/frobt.2022.817870 | Repeatable perturbation protocol for robustness evaluation. | Related Work 2.4; Experimental Setup; Discussion | verify complete author list before final bibliography |
| `Koren2018AdaptiveStressTesting` | must-cite | Adaptive Stress Testing for Autonomous Vehicles | Mark Charles Koren, Saud Alsaif, Ritchie Lee, Mykel J. Kochenderfer | 2018 IEEE Intelligent Vehicles Symposium | DOI: 10.1109/IVS.2018.8500400 | Stress testing as method to expose failure modes. | Introduction; Related Work 2.4; Experimental Setup | verified from user-provided list |
| `Nalic2020StressTestingScenarioBasedADS` | should-cite | Stress Testing Method for Scenario Based Testing of Automated Driving Systems | Demin Nalic, Hexuan Li, Arno Eichberger, Christoph Wellershaus, Aleksa Pandurevic, Branko Rogic | arXiv preprint, 2020 | arXiv: 2011.06553 | Scenario-based stress testing methodology. | Related Work 2.4; Experimental Setup; Discussion | verified from user-provided list |
| `Cameron2024DomesticRobotFailureOutcomes` | should-cite | A taxonomy of domestic robot failure outcomes: understanding the impact of failure on trustworthiness of domestic robots | Harriet R. Cameron, Simon Castle-Green, Muhammad Chughtai, Liz Dowthwaite, Ayse Kucukyilmaz, Horia A. Maior, Victor Ngo, Eike Schneiders, Bernd C. Stahl | Proceedings of the 2nd International Symposium on Trustworthy Autonomous Systems, 2024, pp. 1-14 | DOI: 10.1145/3686038.3686050 | Failure outcome taxonomy; caveat diagnostic labels vs physical cause. | Related Work 2.4; Results; Discussion / Limitations | verified from user-provided list |
| `Dogga2023AutoARTS` | optional | AutoARTS: Taxonomy, Insights and Tools for Root Cause Labelling of Incidents in Microsoft Azure | Pradeep Dogga, Chetan Bansal, Richie Costleigh, Gopinath Jayagopal, Suman Nath, Xuchao Zhang | USENIX Annual Technical Conference, 2023 | URL: TODO official USENIX URL | Root-cause labeling boundary and incident analysis. | Related Work 2.4; Discussion / Limitations | verify URL before final bibliography |

## Related Work Organization

### Suspended-Payload Transport Stack And Control Backbone

Use `Li2023AutoTrans`, `Sreenath2013DifferentiallyFlatHybrid`,
`Son2020ObstacleAvoidanceSuspendedLoad`, `UrbinaBrito2021PredictivePayloadTransport`,
`Lee2010GeometricTrackingSE3`, `GuerreroSanchez2017SwingAttenuation`, and
optionally `Barikbin2019WindPayloadTracking` after venue/year verification.

This subsection should emphasize coupled load dynamics, payload-aware
trajectory generation, MPC / predictive control, SO(3) / SE(3) control, and
wind / swing sensitivity. It should also make clear that the Stage 4 paper is
not replacing the planner, payload MPC, or SO3 controller.

### External Execution Governance And Safety-Filter Boundary

Use `Garone2017ReferenceCommandGovernorsSurvey`,
`Garone2016ExplicitReferenceGovernor`, `Nicotra2016UAVRobustERG`,
`Li2021ActionGovernor`, `Wabersich2021PredictiveSafetyFilter`, and
`Hsu2024SafetyFilterUnifiedView`.

This subsection should position the proposed interface as empirical execution
governance related to runtime command/reference modulation. It should avoid
claiming certified safety, formal invariance, or a predictive safety filter.

### Learning-Enhanced Robustness Without Claiming Learning Dominates

Use `Andersson2017RiskAwareActiveLearning`, `Bauersfeld2021NeuroBEM`,
`Torrente2021DataDrivenMPC`, `Saviolo2022PITCN`,
`Lee2024HybridDisturbancePrediction`, and `Jin2025NeuralPredictorPayload`
after final metadata verification for the recent paper.

This subsection should motivate risk-conditioned adaptation and
learning-enhanced aerial robustness while preserving the Stage 4 result
boundary: learned methods do not uniformly dominate the strong heuristic /
static baselines.

### Protocol-Conditioned Benchmarking And Failure Analysis

Use `Muller2019MeasureTargetConfusion`,
`Monteleone2023BalanceResilienceBenchmark`,
`Koren2018AdaptiveStressTesting`, `Nalic2020StressTestingScenarioBasedADS`,
`Cameron2024DomesticRobotFailureOutcomes`, and optionally `Dogga2023AutoARTS`
after URL verification.

This subsection should support protocol-split evaluation, repeated robustness
assessment, stress testing, and diagnostic failure labels. It should not claim
that the Stage 4 failure groups prove exact physical root cause.

## Citation Gaps Remaining

- Verify `Barikbin2019WindPayloadTracking` venue/year from the provided DOI
  source before manuscript insertion.
- Verify `Wabersich2021PredictiveSafetyFilter` DOI / Automatica metadata
  before final bibliography.
- Verify `Jin2025NeuralPredictorPayload` final metadata because it is recent.
- Verify the complete Frontiers author list for
  `Monteleone2023BalanceResilienceBenchmark`.
- Verify the official USENIX URL for `Dogga2023AutoARTS`.
- Generate final BibTeX keys and BibTeX entries later; no BibTeX is generated
  in Stage 4-AM2.

## Insertion Plan

### Introduction

Use:

- `Li2023AutoTrans`
- `Sreenath2013DifferentiallyFlatHybrid`
- `Son2020ObstacleAvoidanceSuspendedLoad`
- `GuerreroSanchez2017SwingAttenuation`
- `Koren2018AdaptiveStressTesting`
- `Muller2019MeasureTargetConfusion`

Purpose: motivate suspended-payload UAV transport, coupled load dynamics,
strong wind / swing sensitivity, and the need to avoid over-relying on one
nominal protocol score.

### Related Work 2.1

Use:

- `Li2023AutoTrans`
- `Sreenath2013DifferentiallyFlatHybrid`
- `Son2020ObstacleAvoidanceSuspendedLoad`
- `UrbinaBrito2021PredictivePayloadTransport`
- `Lee2010GeometricTrackingSE3`
- `GuerreroSanchez2017SwingAttenuation`
- `Barikbin2019WindPayloadTracking` after metadata verification.

Purpose: cover suspended-payload transport stack, trajectory generation,
payload-aware MPC / predictive control, geometric control, and wind / swing
transport context.

### Related Work 2.2

Use:

- `Garone2017ReferenceCommandGovernorsSurvey`
- `Garone2016ExplicitReferenceGovernor`
- `Nicotra2016UAVRobustERG`
- `Li2021ActionGovernor`
- `Wabersich2021PredictiveSafetyFilter` after DOI / metadata verification.
- `Hsu2024SafetyFilterUnifiedView`

Purpose: position external execution governance and clearly bound the method
against certified reference governors and safety filters.

### Related Work 2.3

Use:

- `Andersson2017RiskAwareActiveLearning`
- `Bauersfeld2021NeuroBEM`
- `Torrente2021DataDrivenMPC`
- `Saviolo2022PITCN`
- `Lee2024HybridDisturbancePrediction`
- `Jin2025NeuralPredictorPayload` after final metadata verification.

Purpose: motivate learning-enhanced aerial robustness, risk-aware learning,
data-driven model enhancement, and disturbance / payload prediction.

### Related Work 2.4

Use:

- `Muller2019MeasureTargetConfusion`
- `Monteleone2023BalanceResilienceBenchmark` after author-list verification.
- `Koren2018AdaptiveStressTesting`
- `Nalic2020StressTestingScenarioBasedADS`
- `Cameron2024DomesticRobotFailureOutcomes`
- `Dogga2023AutoARTS` after official URL verification.

Purpose: justify protocol-conditioned benchmarking, stress testing, repeated
perturbation evaluation, and failure taxonomy / diagnostic-label framing.

### Method

Use:

- `Li2023AutoTrans`
- `UrbinaBrito2021PredictivePayloadTransport`
- `Lee2010GeometricTrackingSE3`
- `Garone2017ReferenceCommandGovernorsSurvey`
- `Garone2016ExplicitReferenceGovernor`
- `Nicotra2016UAVRobustERG`
- `Andersson2017RiskAwareActiveLearning`

Purpose: cite the underlying stack / controller context and the conceptual
precedent for external command/reference governance while preserving the
empirical-governor claim boundary.

### Discussion / Limitations

Use:

- `Garone2017ReferenceCommandGovernorsSurvey`
- `Wabersich2021PredictiveSafetyFilter`
- `Hsu2024SafetyFilterUnifiedView`
- `Muller2019MeasureTargetConfusion`
- `Koren2018AdaptiveStressTesting`
- `Cameron2024DomesticRobotFailureOutcomes`
- `Dogga2023AutoARTS` after URL verification.

Purpose: state that the method is not certified, no safety guarantee is
claimed, protocol scores are context-dependent, and failure groups are
diagnostic rather than exact root-cause proof.

## Claim Boundary

- Use governor and safety-filter literature to position and bound the method.
- Do not claim certified safety.
- Do not claim formal invariance, stability, or runtime assurance.
- Use learning literature to motivate risk-conditioned adaptation, not learned
  domination.
- Use benchmarking and failure literature to justify protocol split and
  diagnostic labels, not root-cause certainty.
- Keep `risk_adapter_v1` as the current balanced learned / risk-conditioned
  protagonist under the tested protocols only.
- Keep `risk_adapter_v21` as a strong nominal / single-goal variant or
  ablation, not a final cross-protocol winner.
- Do not create or introduce `risk_adapter_v22`.
