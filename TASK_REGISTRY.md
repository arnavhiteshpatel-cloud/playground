# Task Registry

Status: `todo` · `doing` · `done` · `blocked` (see BLOCKERS.md). Workstreams run in parallel with file ownership
recorded in ARCHITECTURE_DECISIONS.md (ADR-G2-01). Audit finding IDs (FA-NN) refer to FORENSIC_AUDIT.md.

## Generation 0 — audit and baseline
| ID | Task | Owner | Status | Output |
|---|---|---|---|---|
| T0.1 | Environment, Qt/VTK offscreen verification, tooling install | lead | done | EGL offscreen OK; PySide6 6.12, VTK 9.7.2 |
| T0.2 | Reproduce baseline tests and key experiments (G, P, C, H/I) | lead | done | G exact, P bit-identical, C ±0.004, H/I 29/29 rows (EXECUTION_STATE.md) |
| T0.3 | Forensic audit + remediation register | lead | done | FORENSIC_AUDIT.md |
| T0.4 | Create mandate §55 ledgers | lead | done | this file and siblings |
| T0.5 | Fix specimen-count inconsistency in Manuscript 1 (FA-10) | lead | done | publications/MANUSCRIPT_1_separability.md |

## Generation 1–2 — science and data
| ID | Task | Owner | Status | Audit |
|---|---|---|---|---|
| T1.1 | Dataset discovery round 2, licence-aware manifests, leakage-free split plan | research stream | done | FA-08 |
| T1.2 | Science knowledge base with verified references; machine-readable materials knowledge | research stream | done | FA-16 |
| T1.3 | Phantom v2: correlated noise/blur from real scans, irregular/fragmenting granules, displacement, non-uniform resorption | lead | done (generator v2: displacement, fragmentation, resorption variability) | FA-21 |
| T1.4 | Sim→real: domain randomisation, normalisation, self-supervised pretraining, few-shot curves (multi-seed, CIs) on real dog data | lead | doing (S2 a and b done: zoom recovers part of the gap, domain randomisation was worse on every test scan; S2 c running; S3 queued) | FA-02 |
| T1.5 | Ensembles, multi-seed variance, failure-detection AUROC, conformal volume intervals | lead | doing (U1 queued behind S2 c and S3) | FA-03, FA-17 |
| T1.6 | Longitudinal v2: displacement/fragmentation, registration-failure detection | lead | done (L3, L4, L5 fail-closed axis verification, F2; no desktop day-0 workflow) | FA-04 |
| T1.7 | Separability advisor + measurement support/abstention in pipeline | lead | done (advisor 1.4.3; held-out S1H–S1H5; read-time support; method binding) | FA-16 |
| T1.8 | Measurement-based model selection and benchmark scorecard | lead | doing (scorecard current; U1 selection queued) | FA-15 |
| T1.9 | Endpoint definitions document | lead | done | FA-25 |
| T1.10 | Licence enforcement in training | lead | done (enforcement + parent inheritance + safe defaults) | FA-26 |
| T1.11 | Segmental ROI after bridging via day-0 propagation | lead | done (propagate_roi; F2) | FA-05 |
| T1.12 | TIGRE/ASTRA investigation | lead | done (ADR-G2-08) | FA-22 |
| T1.13 | Runtime evaluation: ONNX Runtime, int8 quantisation, tiling | lead | doing (ONNX path done and shipped; O2 benchmark queued) | FA-23 |
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
| T4.1 | Coverage, property, fuzz, destructive, mutation tests; CI | QA stream | done (611 passed, 1 skipped; 93.4% / 99% critical; CI green on 3 OS × 2 Python with desktop tests and claims checker blocking) | FA-18 |
| T4.2 | Security review Gen 2 | QA stream | done (docs/security/SECURITY_REVIEW_GEN2.md; cycle-3 product review fixes) | FA-19 |
| T4.3 | Claims checker for documents vs result files | lead | done (scripts/check_claims.py) | FA-10, FA-27 |
| T4.4 | Traceability matrix regeneration | lead | done (58 verified / 47 partial / 24 gap FS rows, 28 Nov) | FA-20 |
| T4.5 | Independent reviews: 12 perspectives × ≥3 cycles | lead + reviewers | done (3 cycles; automated reviewer agents, not human experts; human review is founder decision #24) | — |

## Commercial
| ID | Task | Owner | Status | Audit |
|---|---|---|---|---|
| T5.1 | Competitor capability matrix, patent landscape, invention register | competitive stream | done | FA-11 |
| T5.2 | Revenue model with mandated pricing hypotheses, financial model rebuild, funding strategy | commercial stream | done | FA-12 |
| T5.3 | Time-saving claim relabelled; measurement protocol | lead | done (relabelled; desktop timing instrumentation) | FA-06 |

## Final deliverables
| ID | Task | Status |
|---|---|---|
| T6.1 | PDF report (Gen 2) | doing (built; final rebuild after the ML queue) |
| T6.2 | Master spreadsheet (Gen 2) | doing (built; final rebuild after the ML queue) |
| T6.3 | Engineering validation dossier | done (v0.2, 28 Nov) |
| T6.4 | Founder executive summary | doing (current to S1H5 and S2 b; final update after the ML queue) |
| T6.5 | Comparison against Gen-0 baseline | done (BASELINE_COMPARISON.md) |
| T6.6 | Linux desktop bundle rebuilt from a clean tree with provenance | done (1f568f4; rebuild again after the last code change) |
| T6.7 | Cycle-3 review responses (science, product, business/regulatory) | done (docs/reviews/cycle3/RESPONSE_*.md) |
| T6.8 | Pre-registered held-out tests of the shipped advisor (S1H4 product paths; S1H5 HA precision) | done |
