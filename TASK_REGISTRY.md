# Task Registry

Status: `todo` · `doing` · `done` · `blocked` (see BLOCKERS.md). Workstreams run in parallel with file ownership
recorded in ARCHITECTURE_DECISIONS.md (ADR-G2-01). Audit finding IDs (FA-NN) refer to FORENSIC_AUDIT.md.

## Generation 0 — audit and baseline
| ID | Task | Owner | Status | Output |
|---|---|---|---|---|
| T0.1 | Environment, Qt/VTK offscreen verification, tooling install | lead | done | EGL offscreen OK; PySide6 6.12, VTK 9.7.2 |
| T0.2 | Reproduce baseline tests and key experiments (G, P, C, H/I) | lead | doing | experiments/results_gen0_repro/ |
| T0.3 | Forensic audit + remediation register | lead | done | FORENSIC_AUDIT.md |
| T0.4 | Create mandate §55 ledgers | lead | done | this file and siblings |
| T0.5 | Fix specimen-count inconsistency in Manuscript 1 (FA-10) | lead | done | publications/MANUSCRIPT_1_separability.md |

## Generation 1–2 — science and data
| ID | Task | Owner | Status | Audit |
|---|---|---|---|---|
| T1.1 | Dataset discovery round 2, licence-aware manifests, leakage-free split plan | research stream | done | FA-08 |
| T1.2 | Science knowledge base with verified references; machine-readable materials knowledge | research stream | done | FA-16 |
| T1.3 | Phantom v2: correlated noise/blur from real scans, irregular/fragmenting granules, displacement, non-uniform resorption | lead | done (generator v2: displacement, fragmentation, resorption variability) | FA-21 |
| T1.4 | Sim→real: domain randomisation, normalisation, self-supervised pretraining, few-shot curves (multi-seed, CIs) on real dog data | lead | doing (S2v2/S3 running) | FA-02 |
| T1.5 | Ensembles, multi-seed variance, failure-detection AUROC, conformal volume intervals | lead | doing (U1 queued) | FA-03, FA-17 |
| T1.6 | Longitudinal v2: displacement/fragmentation, registration-failure detection | lead | doing (L3 v1 done; conservative tracking re-run queued) | FA-04 |
| T1.7 | Separability advisor + measurement support/abstention in pipeline | lead | done (advisor 1.3.0; S1 re-runs queued) | FA-16 |
| T1.8 | Measurement-based model selection and benchmark scorecard | lead | doing (endpoint errors in S1; U1 selection queued) | FA-15 |
| T1.9 | Endpoint definitions document | lead | done | FA-25 |
| T1.10 | Licence enforcement in training | lead | done (enforcement + parent inheritance + safe defaults) | FA-26 |
| T1.11 | Segmental ROI after bridging via day-0 propagation | lead | done (propagate_roi; F2) | FA-05 |
| T1.12 | TIGRE/ASTRA investigation | lead | done (ADR-G2-08) | FA-22 |
| T1.13 | Runtime evaluation: ONNX Runtime, int8 quantisation, tiling | lead | doing (ONNX done; O2 benchmark queued) | FA-23 |
| T1.14 | Pre-registered morphometry convention + held-out validation | lead | done (pre-registered; no held-out data found yet) | FA-07 |

## Generation 3 — desktop product
| ID | Task | Owner | Status | Audit |
|---|---|---|---|---|
| T3.1 | PySide6+VTK workstation: projects, import wizard, viewers, 3D, editing, jobs, review, reports | desktop stream | done | FA-13, FA-14 |
| T3.2 | Offline signed licensing (test keys only) | desktop stream | done | — |
| T3.3 | PyInstaller packaging (Linux built here), CI matrix for Windows/macOS/Linux | desktop stream | done | FA-13 |
| T3.4 | Website and documentation set | lead (later) | done (website/, docs/user/) | — |

## Generation 4–5 — verification
| ID | Task | Owner | Status | Audit |
|---|---|---|---|---|
| T4.1 | Coverage, property, fuzz, destructive, mutation tests; CI | QA stream | doing | FA-18 |
| T4.2 | Security review Gen 2 | QA stream | doing | FA-19 |
| T4.3 | Claims checker for documents vs result files | lead | done (scripts/check_claims.py) | FA-10, FA-27 |
| T4.4 | Traceability matrix regeneration | lead | doing (quality stream) | FA-20 |
| T4.5 | Independent reviews: 12 perspectives × ≥3 cycles | lead + reviewers | doing (cycle 1: 9/12 perspectives) | — |

## Commercial
| ID | Task | Owner | Status | Audit |
|---|---|---|---|---|
| T5.1 | Competitor capability matrix, patent landscape, invention register | competitive stream | done | FA-11 |
| T5.2 | Revenue model with mandated pricing hypotheses, financial model rebuild, funding strategy | commercial stream | done | FA-12 |
| T5.3 | Time-saving claim relabelled; measurement protocol | lead | done (relabelled; desktop timing instrumentation) | FA-06 |

## Final deliverables
| ID | Task | Status |
|---|---|---|
| T6.1 | PDF report (Gen 2) | todo |
| T6.2 | Master spreadsheet (Gen 2) | todo |
| T6.3 | Engineering validation dossier | doing (quality stream) |
| T6.4 | Founder executive summary | todo |
| T6.5 | Comparison against Gen-0 baseline | todo |
