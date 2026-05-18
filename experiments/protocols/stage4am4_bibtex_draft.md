# Stage 4-AM4 BibTeX Draft And Citation Key Package

## Executive Summary

Stage 4-AM4 is a BibTeX draft / citation key package for the reframed Stage 4
paper. It converts only the ready-to-use citation metadata recorded in Stage
4-AM2 and organized by Stage 4-AM3 into draft BibTeX blocks.

This document is not final bibliography insertion and does not create or edit
any manuscript `.tex` or `.bib` file. The blocks below are a manuscript
preparation aid that should be checked against the final venue template before
use.

Only entries that Stage 4-AM3 marked ready-to-use are converted into draft
BibTeX blocks. Conditional entries remain TODO items and require metadata
verification before final BibTeX is written.

The paper framing remains risk-conditioned execution governance for
suspended-payload UAV transport under strong wind, protocol-split robustness
evaluation, balanced robustness / protocol regret analysis, and
failure-mode-aware diagnosis. `risk_adapter_v1` remains the tentative balanced
learned / risk-conditioned protagonist. Do not create `risk_adapter_v22`.

## Ready-To-Use BibTeX Draft Blocks

The following draft blocks use only metadata recorded in
`experiments/protocols/stage4am2_verified_citation_collection_result.md`.
Missing fields are omitted rather than filled from memory.

```bibtex
@article{Li2023AutoTrans,
  title = {{AutoTrans}: A Complete Planning and Control Framework for Autonomous {UAV} Payload Transportation},
  author = {Li, Haojia and Wang, Haokun and Feng, Chen and Gao, Fei and Zhou, Boyu and Shen, Shaojie},
  journal = {IEEE Robotics and Automation Letters},
  volume = {8},
  number = {10},
  pages = {6859--6866},
  year = {2023},
  doi = {10.1109/LRA.2023.3313010}
}
```

```bibtex
@inproceedings{Sreenath2013DifferentiallyFlatHybrid,
  title = {Trajectory Generation and Control of a Quadrotor With a Cable-Suspended Load---A Differentially-Flat Hybrid System},
  author = {Sreenath, Koushil and Michael, Nathan and Kumar, Vijay},
  booktitle = {ICRA 2013},
  pages = {4888--4895},
  year = {2013},
  doi = {10.1109/ICRA.2013.6631275}
}
```

```bibtex
@article{Son2020ObstacleAvoidanceSuspendedLoad,
  title = {Real-Time Optimal Trajectory Generation and Control of a Multi-Rotor With a Suspended Load for Obstacle Avoidance},
  author = {Son, Clark Youngdong and Seo, Hoseong and Jang, Dohyun and Kim, H. Jin},
  journal = {IEEE Robotics and Automation Letters},
  volume = {5},
  number = {2},
  pages = {1915--1922},
  year = {2020},
  doi = {10.1109/LRA.2020.2967279}
}
```

```bibtex
@article{UrbinaBrito2021PredictivePayloadTransport,
  title = {A Predictive Control Strategy for Aerial Payload Transportation with an Unmanned Aerial Vehicle},
  author = {Urbina-Brito, Norberto and Guerrero-Sánchez, María-Eusebia and Valencia-Palomo, Guillermo and Hernández-González, Omar and López-Estrada, Francisco-Ronay and Hoyo-Montaño, José Antonio},
  journal = {Mathematics},
  volume = {9},
  number = {15},
  pages = {1822},
  year = {2021},
  doi = {10.3390/math9151822}
}
```

```bibtex
@inproceedings{Lee2010GeometricTrackingSE3,
  title = {Geometric Tracking Control of a Quadrotor {UAV} on {SE(3)}},
  author = {Lee, Taeyoung and Leok, Melvin and McClamroch, N. Harris},
  booktitle = {49th IEEE Conference on Decision and Control},
  pages = {5420--5425},
  year = {2010},
  doi = {10.1109/CDC.2010.5717652}
}
```

```bibtex
@article{GuerreroSanchez2017SwingAttenuation,
  title = {Swing-attenuation for a quadrotor transporting a cable-suspended payload},
  author = {Guerrero-Sánchez, María-Eusebia and Mercado-Ravell, Diego Alberto and Lozano, Rogelio and García-Beltrán, C. Daniel},
  journal = {ISA Transactions},
  volume = {68},
  pages = {433--449},
  year = {2017},
  doi = {10.1016/j.isatra.2017.01.027}
}
```

```bibtex
@article{Garone2017ReferenceCommandGovernorsSurvey,
  title = {Reference and command governors for systems with constraints: A survey on theory and applications},
  author = {Garone, Emanuele and Di Cairano, Stefano and Kolmanovsky, Ilya},
  journal = {Automatica},
  volume = {75},
  pages = {306--328},
  year = {2017},
  doi = {10.1016/j.automatica.2016.08.013}
}
```

```bibtex
@article{Garone2016ExplicitReferenceGovernor,
  title = {Explicit Reference Governor for Constrained Nonlinear Systems},
  author = {Garone, Emanuele and Nicotra, Marco M.},
  journal = {IEEE Transactions on Automatic Control},
  volume = {61},
  number = {5},
  pages = {1379--1384},
  year = {2016},
  doi = {10.1109/TAC.2015.2476195}
}
```

```bibtex
@inproceedings{Nicotra2016UAVRobustERG,
  title = {A robust explicit reference governor for constrained control of Unmanned Aerial Vehicles},
  author = {Nicotra, Marco M. and Naldi, Roberto and Garone, Emanuele},
  booktitle = {American Control Conference},
  year = {2016},
  doi = {10.1109/ACC.2016.7526657}
}
```

```bibtex
@article{Li2021ActionGovernor,
  title = {Action Governor for Discrete-Time Linear Systems With Non-Convex Constraints},
  author = {Li, Nan and Han, Kyoungseok and Girard, Anouck and Tseng, H. Eric and Filev, Dimitar and Kolmanovsky, Ilya},
  journal = {IEEE Control Systems Letters},
  volume = {5},
  number = {1},
  pages = {121--126},
  year = {2021},
  doi = {10.1109/LCSYS.2020.3000198}
}
```

```bibtex
@article{Hsu2024SafetyFilterUnifiedView,
  title = {The Safety Filter: A Unified View of Safety-Critical Control in Autonomous Systems},
  author = {Hsu, Kai-Chieh and Hu, Haimin and Fisac, Jaime F.},
  journal = {Annual Review of Control, Robotics, and Autonomous Systems},
  volume = {7},
  pages = {47--72},
  year = {2024},
  doi = {10.1146/annurev-control-071723-102940}
}
```

```bibtex
@inproceedings{Andersson2017RiskAwareActiveLearning,
  title = {Deep Learning Quadcopter Control via Risk-Aware Active Learning},
  author = {Andersson, Olov and Wzorek, Mariusz and Doherty, Patrick},
  booktitle = {Proceedings of the AAAI Conference on Artificial Intelligence},
  volume = {31},
  number = {1},
  pages = {3812--3818},
  year = {2017},
  doi = {10.1609/aaai.v31i1.11041}
}
```

```bibtex
@inproceedings{Bauersfeld2021NeuroBEM,
  title = {{NeuroBEM}: Hybrid Aerodynamic Quadrotor Model},
  author = {Bauersfeld, Leonard and Kaufmann, Elia and Foehn, Philipp and Sun, Sihao and Scaramuzza, Davide},
  booktitle = {Robotics: Science and Systems},
  year = {2021},
  doi = {10.15607/RSS.2021.XVII.042}
}
```

```bibtex
@article{Torrente2021DataDrivenMPC,
  title = {Data-Driven {MPC} for Quadrotors},
  author = {Torrente, Guillem and Kaufmann, Elia and Föhn, Philipp and Scaramuzza, Davide},
  journal = {IEEE Robotics and Automation Letters},
  volume = {6},
  number = {2},
  pages = {3769--3776},
  year = {2021},
  doi = {10.1109/LRA.2021.3061307}
}
```

```bibtex
@article{Saviolo2022PITCN,
  title = {Physics-Inspired Temporal Learning of Quadrotor Dynamics for Accurate Model Predictive Trajectory Tracking},
  author = {Saviolo, Alessandro and Li, Guanrui and Loianno, Giuseppe},
  journal = {IEEE Robotics and Automation Letters},
  volume = {7},
  number = {4},
  pages = {10256--10263},
  year = {2022},
  doi = {10.1109/LRA.2022.3192609}
}
```

```bibtex
@article{Lee2024HybridDisturbancePrediction,
  title = {Hybrid model-based and data-driven disturbance prediction for precise quadrotor trajectory tracking},
  author = {Lee, Changhyeon and Son, Junwoo Jason and Yoon, Seongwon and Jeon, Soo and Han, Soohee},
  journal = {Engineering Applications of Artificial Intelligence},
  volume = {136},
  number = {Part A},
  pages = {108895},
  year = {2024},
  doi = {10.1016/j.engappai.2024.108895}
}
```

```bibtex
@incollection{Muller2019MeasureTargetConfusion,
  title = {Measuring Progress in Robotics: Benchmarking and the 'Measure-Target Confusion'},
  author = {Müller, Vincent C.},
  booktitle = {Metrics of Sensory Motor Coordination and Integration in Robots and Animals},
  year = {2019},
  doi = {10.1007/978-3-030-14126-4_9}
}
```

```bibtex
@inproceedings{Koren2018AdaptiveStressTesting,
  title = {Adaptive Stress Testing for Autonomous Vehicles},
  author = {Koren, Mark Charles and Alsaif, Saud and Lee, Ritchie and Kochenderfer, Mykel J.},
  booktitle = {2018 IEEE Intelligent Vehicles Symposium},
  year = {2018},
  doi = {10.1109/IVS.2018.8500400}
}
```

```bibtex
@misc{Nalic2020StressTestingScenarioBasedADS,
  title = {Stress Testing Method for Scenario Based Testing of Automated Driving Systems},
  author = {Nalic, Demin and Li, Hexuan and Eichberger, Arno and Wellershaus, Christoph and Pandurevic, Aleksa and Rogic, Branko},
  year = {2020},
  eprint = {2011.06553},
  archivePrefix = {arXiv}
}
```

```bibtex
@inproceedings{Cameron2024DomesticRobotFailureOutcomes,
  title = {A taxonomy of domestic robot failure outcomes: understanding the impact of failure on trustworthiness of domestic robots},
  author = {Cameron, Harriet R. and Castle-Green, Simon and Chughtai, Muhammad and Dowthwaite, Liz and Kucukyilmaz, Ayse and Maior, Horia A. and Ngo, Victor and Schneiders, Eike and Stahl, Bernd C.},
  booktitle = {Proceedings of the 2nd International Symposium on Trustworthy Autonomous Systems},
  pages = {1--14},
  year = {2024},
  doi = {10.1145/3686038.3686050}
}
```

## Conditional Citation TODO Blocks

Do not create final BibTeX for the following entries until the missing
metadata is verified.

| key | missing metadata | action required before final BibTeX |
| --- | --- | --- |
| `Barikbin2019WindPayloadTracking` | venue/year details | Verify venue and year from the DOI source, then decide whether the entry should be `@article` and add the complete journal metadata. |
| `Wabersich2021PredictiveSafetyFilter` | DOI / Automatica metadata | Verify DOI and complete Automatica metadata before writing final BibTeX. |
| `Jin2025NeuralPredictorPayload` | final metadata because the paper is recent | Verify final publication metadata before final bibliography insertion. |
| `Monteleone2023BalanceResilienceBenchmark` | complete author list | Verify the full Frontiers author list before final BibTeX. |
| `Dogga2023AutoARTS` | official USENIX URL | Verify the official USENIX URL before final BibTeX. |

## Citation Insertion Short Guide

- Introduction: cite `Li2023AutoTrans`,
  `Sreenath2013DifferentiallyFlatHybrid`,
  `Son2020ObstacleAvoidanceSuspendedLoad`,
  `GuerreroSanchez2017SwingAttenuation`,
  `Koren2018AdaptiveStressTesting`, and
  `Muller2019MeasureTargetConfusion`.
- Related Work 2.1: cite suspended-payload transport and control backbone
  entries, including `Li2023AutoTrans`,
  `Sreenath2013DifferentiallyFlatHybrid`,
  `Son2020ObstacleAvoidanceSuspendedLoad`,
  `UrbinaBrito2021PredictivePayloadTransport`,
  `Lee2010GeometricTrackingSE3`, and
  `GuerreroSanchez2017SwingAttenuation`.
- Related Work 2.2: cite governor and safety-boundary entries, including
  `Garone2017ReferenceCommandGovernorsSurvey`,
  `Garone2016ExplicitReferenceGovernor`, `Nicotra2016UAVRobustERG`,
  `Li2021ActionGovernor`, and `Hsu2024SafetyFilterUnifiedView`.
- Related Work 2.3: cite learning-enhanced aerial robustness entries,
  including `Andersson2017RiskAwareActiveLearning`, `Bauersfeld2021NeuroBEM`,
  `Torrente2021DataDrivenMPC`, `Saviolo2022PITCN`, and
  `Lee2024HybridDisturbancePrediction`.
- Related Work 2.4: cite benchmarking, stress-testing, and failure-analysis
  entries, including `Muller2019MeasureTargetConfusion`,
  `Koren2018AdaptiveStressTesting`, `Nalic2020StressTestingScenarioBasedADS`,
  and `Cameron2024DomesticRobotFailureOutcomes`.
- Method: use `Li2023AutoTrans`, `Lee2010GeometricTrackingSE3`,
  `Garone2017ReferenceCommandGovernorsSurvey`,
  `Garone2016ExplicitReferenceGovernor`, and `Li2021ActionGovernor` to frame
  the stack and governor interface.
- Discussion: use `Hsu2024SafetyFilterUnifiedView`,
  `Muller2019MeasureTargetConfusion`, `Koren2018AdaptiveStressTesting`, and
  `Cameron2024DomesticRobotFailureOutcomes` to bound safety, protocol, and
  diagnostic-label claims.

Conditional entries from the TODO table should be inserted only after their
metadata gaps are closed.

## Final Bibliography Checklist

- Check DOI formatting against the target venue's preferred style.
- Check venue names for official capitalization and abbreviation style.
- Check author accents, including names such as `Müller`, `Föhn`,
  `Guerrero-Sánchez`, `Hernández-González`, `López-Estrada`, and
  `Hoyo-Montaño`.
- Check conference / journal capitalization after importing into the final
  bibliography manager.
- Check duplicate citation keys before creating a manuscript `.bib` file.
- Verify conditional entries before final use.
- Compile with the target IROS / ICRA / RA-L template later.

## Claim Boundary Reminder

- Governor citations do not imply a formal safety guarantee.
- Learning citations do not imply learned domination over heuristic / static
  baselines.
- Stress-testing citations do not justify a mixed-protocol aggregate.
- Failure-taxonomy citations do not prove exact physical root cause.
- Stage 4 internal counts remain supported by Table 1 and Figures 1-6, not by
  external citations.
