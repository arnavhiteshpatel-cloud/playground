# OsteoQuant Desktop: Engineering Verification Dossier

| Field | Value |
|---|---|
| Document ID | OQ-QMS-EVD-001 |
| Version | 0.1 (DRAFT) |
| Date | 2026-11-27 |
| Software baseline | `osteoquant` 0.1.0 (Generation-2 desktop), measurement-support advisor 1.3.3, working tree of 2026-11-27 (not a tagged release) |
| Owner | Quality / Engineering (TBD) |
| Related | URS.md v0.2, FUNCTIONAL_SPEC.md v0.2, RISK_ASSESSMENT.md v0.2, traceability_matrix.csv, IQ/OQ/PQ v0.2, PART11_GLP_GAP_ANALYSIS.md v0.2 |

> **What this document is:** an index of the engineering verification evidence that exists for OsteoQuant Desktop, where to find it, and how far it goes.
>
> **What it is not:** it is **not a computerised-system validation**, not an executed IQ/OQ/PQ, not a validation report for any intended use, and **not a claim of compliance** with 21 CFR Part 11, 21 CFR Part 58, OECD GLP or any other regulation. No regulator, customer QA unit or independent human expert has reviewed this evidence. Nothing here may be quoted as "validated" or "compliant" (see the review findings QA-REG-03, QA-REG-04 and QA-REG-07).

## 1. Summary
| Item | Value | Source |
|---|---|---|
| Active requirements (URS) | 88 (64 retained or revised from v0.1, 24 new); 2 retired | URS.md §5 |
| Functional specification items | 129 (3 retired) | FUNCTIONAL_SPEC.md |
| Traceability (FS rows) | **VERIFIED 54 · PARTIAL 42 · GAP 33** (was 12 · 24 · 45 of 81 rows for the Generation-1 baseline) | traceability_matrix.csv |
| Requirements fully verified (all FS rows VERIFIED) | 22 of 88; 55 mixed; 11 entirely GAP | `scripts/build_traceability.py` output |
| Automated tests collected | 439–457 test items during 2026-11-27 (the suite grew while this dossier was written); 55 items in `tests/desktop/` | `pytest --collect-only -q` |
| Distinct tests cited as evidence | 172 | traceability_matrix.csv |
| Library line+branch coverage | 62 % (desktop GUI excluded) | docs/qa/coverage_baseline.txt |
| QA defects | 25 found, 21 fixed with regression tests, 4 assigned (open) | docs/qa/DEFECTS_FOUND.md |
| Security findings (Gen 2) | 20: 12 fixed (including the critical-conditional G2-01), 3 assigned to the lead, 3 open (low), 2 info | docs/security/SECURITY_REVIEW_GEN2.md |
| IQ / OQ / PQ executed | **None** | IQ_PROTOCOL.md, OQ_PROTOCOL.md, PQ_PLAN.md |

Counting rule for the matrix: VERIFIED = an automated test asserts the specified behaviour; PARTIAL = a test exists but does not assert all of it, or the only evidence is a recorded script or manual run; GAP = nothing. Protocol steps written during the re-baseline do not count as evidence. Most of the improvement from the Generation-1 counts comes from mapping tests that already existed (desktop, advisor, audit-property, security and QA tests written after the v0.1 matrix), not from new tests; the requirement set also changed (section 3).

## 2. How to reproduce
```bash
# traceability: checks every cited test exists, URS/FS/protocol consistency, then writes the CSV
python scripts/build_traceability.py            # or --check (CI), --no-collect (fast, weaker)

# full test suite (desktop tests need PySide6, VTK, pytest-qt; they run off-screen)
QT_QPA_PLATFORM=offscreen python -m pytest -q

# headless end-to-end self-test of the desktop
python -m osteoquant.desktop --selftest

# coverage (library; desktop omitted by pyproject configuration)
python -m pytest --cov=osteoquant --cov-branch -q
```

## 3. Requirement baseline and traceability
| Evidence | Location | Notes |
|---|---|---|
| URS v0.2 | docs/quality/URS.md | Desktop baseline; retired URS-012 (multi-tenant isolation) and URS-130 (TLS); new sections for measurement support, validation records, material characterisation, longitudinal QC, licence verification, workflow timing (opt-in) and offline operation |
| FS v0.2 | docs/quality/FUNCTIONAL_SPEC.md | Each item has an implementation status (Y/P/N) separate from verification status |
| Risk assessment v0.2 | docs/quality/RISK_ASSESSMENT.md | RSK-25 retired; RSK-37…48 added; status column from the matrix |
| Traceability matrix | docs/quality/traceability_matrix.csv | Generated; columns: URS, FS, area, status, tests, other_evidence, level, risks, protocol step, notes, proposed test |
| Mapping and checker | scripts/build_traceability.py | Holds the mapping table; fails on missing tests, ID mismatches or unknown protocol steps |

Verification status by area (FS rows):

| Area | VERIFIED | PARTIAL | GAP |
|---|---|---|---|
| General, offline | 0 | 4 | 1 |
| Access control | 5 | 2 | 6 |
| Import, QC | 6 | 4 | 5 |
| ROI, segmentation, editing | 6 | 5 | 2 |
| Morphometry, statistics, blinding | 6 | 4 | 5 |
| Reporting, signatures | 3 | 5 | 3 |
| Audit trail | 5 | 4 | 2 |
| Configuration, models, jobs, data management, security, documentation | 5 | 10 | 4 |
| Measurement support, validation records, material characterisation, longitudinal QC | 12 | 2 | 5 |
| Licence, workflow timing | 6 | 2 | 0 |

(Grouped from the per-area counts that the script prints; totals 54 / 42 / 33.)

## 4. Automated test evidence
| Test module | What it verifies (main FS links) |
|---|---|
| tests/desktop/test_editing.py | Brush/eraser protection, physical-unit brush, region grow, fill holes, interpolation, exact undo/redo (FS-054-1, FS-056-1/2) |
| tests/desktop/test_import.py | Format probing, explicit spacing, assignment, visible rejections, duplicates, QC flagging, slab-import hash equality (FS-020-1, FS-023, FS-025-1, FS-026-1, FS-030-1) |
| tests/desktop/test_jobs.py | Background jobs: completion, cancellation, error capture, UI responsiveness, no partial records (FS-114-1/2) |
| tests/desktop/test_licensing.py | Ed25519 licence verification, tampering, expiry, machine binding, test-key gating, no production key shipped (FS-190…192) |
| tests/desktop/test_main_window.py | Off-screen main window: open/sign-in, views, edit and save revision, blinded mode, chain verification, 3D/oblique, About, `--selftest` (FS-042-1, FS-075-3, FS-102-1, FS-210-1) |
| tests/desktop/test_services.py | Project creation/sign-in, label-revision audit, re-authenticated sign-off and separation of duties, watermarked report and preview, measurement-support statuses, results rows, manual ROI, workflow timing (FS-010-2, FS-053-1, FS-092-1, FS-151, FS-191-1, FS-200…202) |
| tests/test_advisor.py | Measurement-support policy, material rules, suppression, material characterisation, validation records (FS-150…171, FS-181-1) |
| tests/test_audit_properties.py | Hash-chain tamper detection (modify, delete, reorder, truncate with anchor), triggers, atomicity, concurrency (FS-100-1, FS-102) |
| tests/test_longitudinal_v2.py | Registration QC, granule tracking, ROI propagation (FS-180-1, FS-181-2, FS-182-1) |
| tests/test_morphometry_analytic.py, tests/test_properties_science.py, tests/test_core.py | Analytic phantoms, invariances, I/O round-trips, ROI, statistics basics (FS-062-1, FS-040-1, FS-023-1) |
| tests/test_stats_reference.py | Statistics against published/reference values (FS-071-2) |
| tests/test_io_destructive.py, tests/test_io_metadata.py, tests/test_io_properties.py, tests/test_safe_archive.py | Malformed and malicious inputs, metadata extraction, round-trips, archive safety (FS-026-2, FS-133-1, FS-022-1) |
| tests/test_security_fixes.py, tests/test_security_gen2.py | Regression tests for security findings S-xx and G2-xx; store integrity, re-authentication lockout (FS-125-1, FS-092-2 store path) |
| tests/test_api.py, tests/test_store_api_workflows.py | Store RBAC, blinding, backup, deletion, reviews, jobs; optional API interface (FS-011-1, FS-075-1, FS-105-1, FS-123-1) |
| tests/test_controls.py | Controls added to close Generation-1 matrix gaps (density without calibration, model hash, self-approval, UTC timestamps) |
| Other (analysis modules, segmentation metrics, ML/phantom, transforms) | Segmentation semantics, uncertainty, model identity and safe loading, ROI geometry |

Engineering run record (not OQ execution; developer container, Linux, Python 3.13, run as root, 2026-11-27):

| Run | Scope | Result |
|---|---|---|
| R1 | tests/desktop, test_controls, test_audit_properties, test_advisor, test_longitudinal_v2, test_security_gen2, test_security_fixes, test_store_api_workflows, test_api | 157 passed, 1 failed, 1 skipped (109 s). The failure was `test_advisor.py::test_resorbable_material_needs_early_known_timepoint`, a test being added concurrently with an advisor change; it is not cited in the matrix. The skip is `test_read_only_data_directory` (POSIX permissions are not enforced for root). |
| R2 | test_controls, test_advisor (after the concurrent change was completed) | 35 passed |

A complete suite run on a clean, release-tagged build, with the log retained, is still required before any of this is used as OQ evidence. One test is a strict expected failure documenting an open defect (`test_update_registry_works_without_fcntl`, QA-022, Windows only).

## 5. Coverage
`docs/qa/coverage_baseline.txt` (library, line + branch, desktop GUI excluded by configuration): **62 % overall**. High: `qc/engine.py` 94 %, `morphometry/core.py` 87 %, `audit/log.py` 85 %, `study/db.py` 79 %. Low: `io/readers.py` 55 %, `stats/core.py` 56 %, `roi/engine.py` 54 %, `segment/classical.py` 24 %, `uncertainty/core.py` 23 %, `cli.py`, `histology`, `phantom/ctsim.py` 0 %. The baseline predates the advisor, licensing and longitudinal tests and does not list `advisor/` or `licensing/`; `longitudinal/core.py` shows 0 % although tests now exist. Re-measure on the release build; add `licensing`, `advisor` and the non-GUI desktop modules (`project`, `services`, `support`, `editing`, `timing`, `import_wizard` model) to the measured set.

## 6. QA reports
| Evidence | Location | Content |
|---|---|---|
| Gen-2 QA test campaign | docs/qa/DEFECTS_FOUND.md | 25 defects (QA-001…025): 21 fixed, each with named regression tests; QA-022 (Windows registry lock), QA-023 (ONNX load TOCTOU), QA-024 (dependency floors), QA-025 (unused imports) open and assigned; 6 documented observations of ambiguous expected behaviour (OBS-01…06) |
| Coverage baseline | docs/qa/coverage_baseline.txt | See section 5 |
| Mutation helper | tests/tools/mutate.py | Mutation fuzzing of readers (used for QA-004) |

## 7. Security reviews
| Evidence | Location | Status |
|---|---|---|
| Generation-1 security review | docs/security/SECURITY_REVIEW.md, REVIEW_RESPONSE.md | S-01…S-21; responses recorded |
| Generation-2 security review | docs/security/SECURITY_REVIEW_GEN2.md | G2-01…G2-20; open: G2-13 (ONNX TOCTOU), G2-14 (dependency floors), G2-15 (Windows lock), G2-16 (audit metadata via API), G2-17 (synchronous upload parsing, API), G2-18 (scrypt cost) |
| Dependency audit and SBOM | docs/security/pip_audit_output.txt, SBOM.csv, sbom.cdx.json | Manual runs; no hash-pinned lock file |
| IP / provenance | docs/security/IP_PROVENANCE.md | Third-party and data provenance |
| Bundled-licence check | packaging/check_bundle_licences.py; About dialog (`test_about_lists_third_party_licences`) | Packaging-time check |

Not yet reviewed for security: the desktop-specific code paths (`osteoquant/desktop/`), in particular re-authentication (defect D-1 below), the choice of safe vs unsafe read mode for locally imported files, and licence handling.

## 8. Scientific experiment results
All experiment results are scripted runs with recorded JSON in `experiments/results/`. They are engineering and research evidence, not PQ. Most use **synthetic** phantoms whose generator shares assumptions with the advisor (accepted limitation STAT-04).

| Experiment | Relevance | Data | Location |
|---|---|---|---|
| G | Morphometry vs analytic and vs Scanco IPL maps (URS-062) | Analytic + 8 real cubes | experiments/results/exp_G_morphometry.json |
| P | Bit-identical reruns, format round-trips (URS-113) | Synthetic | experiments/results/exp_P_reproducibility.json |
| S1, S1b, S1c | Advisor refuses failing measurements (URS-150/151) | Synthetic | experiments/results/exp_S1*.json; EXPERIMENT_REGISTRY.md |
| F, F2 | ROI detection; ROI propagation (URS-040, URS-182) | Synthetic + 2 real ovine | experiments/results/exp_F*.json |
| L, L2, L3, L4 | Day-0 propagation, displacement, registration QC (URS-180/181) | Synthetic | experiments/exp_L*.py, results |
| H, I | Real-data bone segmentation; synthetic-to-real transfer (zero-shot fails) | Public dog forelimb CT (not defects) | experiments/results/exp_H_I_real.json |
| O, O2 | Speed and memory; ONNX runtime | Real large volumes; synthetic | experiments/results/exp_O*.json |
| Blocked | Physical separability (E2), real adaptation (U3), analyst time/ICC (A7/E6), micro-CT vs histology (E8) | Need physical or partner data | EXPERIMENT_REGISTRY.md |

No experiment uses real grafted-defect specimens with ground truth. The graft/new-bone separation and the advisor's decisions are therefore unverified on physical data (RSK-09, RSK-37; PQ-05).

## 9. Review registry
| Evidence | Location | Notes |
|---|---|---|
| Review registry | REVIEW_REGISTRY.md | 12 perspectives × 3 cycles planned. Per the registry's own disclosure, the reviews were performed by **automated reviewer agents, not qualified human experts**, and must not be presented as expert review. |
| Cycle-1 science/architecture reviews | docs/reviews/cycle1/REVIEW_IMAGING_STATS.md, REVIEW_ML_ARCH.md, RESPONSE.md, RESPONSE_PART2.md | 60 findings; critical and high findings fixed or accepted with documented limitation (STAT-04); medium/low open for cycle 2 |
| Cycle-1 biology/CRO/quality review | docs/reviews/cycle1/REVIEW_BIO_CRO_QUALITY.md | QA-REG-01 (report omitted support status) now implemented in `report/defectfill.py` but untested (FS-152-2 GAP); QA-REG-02 (quality documents described the web architecture) addressed by this re-baseline; QA-REG-04 (no executed verification) remains open; BIO and CRO findings partly open |
| Forensic audit | FORENSIC_AUDIT.md | FA-20 (traceability 45 of 81 GAP) addressed by regenerating the matrix; remaining GAP rows listed in the matrix |
| Human expert review | — | **None.** Imaging scientist, bone biologist, biostatistician, quality/regulatory professional and counsel reviews are open founder actions |

## 10. Desktop self-test and documentation evidence
| Evidence | Location |
|---|---|
| Headless end-to-end self-test (import → QC → analysis → views → edit/undo/save → watermarked report → PDF → chain verification) | osteoquant/desktop/selftest.py; `test_selftest_entry_point` |
| User guide | docs/desktop/USER_GUIDE.md (completeness review OQ-DOC-01 not done) |
| Architecture | docs/desktop/ARCHITECTURE.md |
| Packaging | docs/desktop/PACKAGING.md, packaging/ |
| Screenshots of the workflow | docs/screenshots/desktop/ (start page, viewer, editing, revision dialog, import, QC, results, report preview, audit trail, blinded review) |
| Release notes | **None** (URS-141 GAP) |

## 11. Defects and gaps found during the re-baseline
These were found while mapping requirements to code and tests. They are listed here because this document owns no code; proposed changes are for the engineering backlog.

| ID | Severity | Finding | Evidence | Proposed change |
|---|---|---|---|---|
| D-1 | medium (security / attributability) | Desktop e-signature re-authentication bypasses the lockout. `desktop/project.py::Project.reauthenticate` calls `check_password` directly, so wrong passwords at signing never lock the account and inactive or locked accounts are not refused. The Store/API path (`Store.reauthenticate`, fix for G2-03/QA-011) does all three. | FS-092-2 | Make `Project.reauthenticate` delegate to `Store.reauthenticate` (keep the `review.reauth_failed` event or rely on `auth.reauth_failed`); add `test_desktop_reauth_failures_lock_account`. |
| D-2 | high (attributability) | No user administration in the desktop: a project has one admin and further named accounts need library calls. No password change. | FS-010-3, FS-016-1 | Add *Project > Users* (create, role, deactivate, reset password) for `manage_users`. |
| D-3 | high (integrity) | Study tables (scans, segmentations, measurements, reviews) are outside the audit hash chain; direct SQLite edits leave no trace except where hashes appear in audit details. | RSK-48 | Record a per-row content hash in the audit details for every insert/update of data tables, or chain the tables; add an on-demand integrity check (FS-021-2). |
| D-4 | medium | No anchor export/import, audit export, backup, archive or JSON/label export in the desktop. | FS-102-2, FS-104-2, FS-120-1, FS-124-1, FS-081-1 | Tools menu functions; tests for each. |
| D-5 | medium | QC "unsuitable" verdict does not block analysis; manual ROI reason defaults to a fixed text. | FS-032-1, FS-041-1 | Gate with audited override; require a reason. |
| D-6 | medium | `models/validation_records.json` is an unprotected file that can turn learned-model support on. | FS-161-1, RSK-39 | Record its hash in the model registry; verify at load; audit changes. |
| D-7 | medium | Unblinding, SAP lock and post-unblinding flags are not available in the desktop; admin role holds all permissions. | FS-075-2, FS-070-1, FS-076-1, FS-015-1 | Desktop unblind with re-authentication; SAP object; role separation option. |
| D-8 | low | No idle lock; no second-instance detection. | FS-013-3, FS-125-2 | Idle lock timer; project lock file. |
| D-9 | low (test gap) | Report PDF/CSV support content, RUO text and provenance are not asserted by any test; offline operation is not tested with the network blocked. | FS-152-2, FS-001-1/2, FS-080-1, FS-211-1 | Text-extraction tests on the generated PDF (pypdfium2 is already used); a self-test run with socket creation blocked. |

## 12. Statement of limitations
- All evidence is engineering verification produced by the developers on a development container; nothing has been executed under an approved protocol on a qualified installation.
- Every review so far was automated; no independent human expert has assessed code, science or quality documents.
- All quality documents are drafts without approvals; there is no document control, training, CAPA or independent QA.
- Scientific performance on real grafted-defect specimens is unknown.
- Therefore OsteoQuant Desktop is research software. It is **not validated** and **not compliant** with 21 CFR Part 11, GLP or any other regulation, and this dossier must not be presented as evidence that it is.
