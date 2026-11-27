# OsteoQuant — Operational Qualification (OQ) Protocol

> **Revision pending (2026-11-27, cycle-1 review QA-REG-02).** This draft describes the Generation-1 architecture (FastAPI server + browser workbench). The Generation-2 product is an offline desktop application (PySide6/VTK, in-process analysis library; the API is an optional integration interface). Requirements and protocols must be re-baselined to the desktop product before any qualification activity. Draft only; no compliance is claimed.


| Field | Value |
|---|---|
| Document ID | OQ-QMS-OQ-001 |
| Version | 0.1 (DRAFT) |
| Date | 2026-11-27 |
| Prerequisite | Approved, executed IQ (OQ-QMS-IQ-001) on the same instance |
| Related | URS, FS, RISK_ASSESSMENT.md, traceability_matrix.csv |

> **Status: DRAFT — not validated; not a claim of Part 11 compliance or GLP validation.**

## 1. Objective
Demonstrate that each specified function operates as intended across its operating range, including negative/challenge conditions, on a qualified installation.

## 2. Approach
- Risk-based depth (CSA/GAMP benchmark): functions with risk S ≥ 4 are tested with **scripted** tests with predefined expected results; lower-risk functions may use **unscripted/exploratory** testing with a recorded summary.
- Automated tests (pytest) may be executed as OQ evidence when: the test code is version-controlled, reviewed, traceable via traceability_matrix.csv, run on the qualified instance (or an identical, IQ'd instance), and the raw run log with software version and timestamp is retained.
- Test data: controlled OQ dataset set `OQ-DATA-vX` (synthetic phantoms, tampered files, malformed headers, multi-tenant fixtures), stored with SHA-256 manifest.
- Test accounts: named test users per role in two tenants (T-A, T-B).

## 3. Test cases
Each test: ID · Objective · Key steps · Expected result · Trace (FS / Risk). Record actual result, P/F, evidence reference, tester, date.

### 3.1 General
| ID | Objective / steps | Expected result | Trace |
|---|---|---|---|
| OQ-GEN-01 | Inspect UI, PDF and CSV for RUO/not-validated statement | Present on all | FS-001-1/2; RSK-34 |
| OQ-GEN-02 | Compare `/api/version` with report/CSV/JSON provenance | Identical version+commit | FS-002-1 |

### 3.2 Access control
| ID | Objective / steps | Expected result | Trace |
|---|---|---|---|
| OQ-ACC-01 | Create two users with same username; attempt shared-account indicators | Rejected; IDs unique | FS-010-1 |
| OQ-ACC-02 | For each role, attempt each permission in matrix (positive + negative) | Matches documented matrix exactly | FS-011-1; RSK-24 |
| OQ-ACC-03 | Run route-permission enumeration test | All routes declare permission | FS-011-2 |
| OQ-ACC-04 | As T-A user, request T-B objects by ID via API, UI deep link, export, search | 404; security event logged; no data returned | FS-012-1/2; RSK-25 |
| OQ-ACC-05 | Weak password; 5 failed logins; idle 31 min | Rejected; account locked & audited; session expired | FS-013-1/2/3 |
| OQ-ACC-06 | Attempt user deletion; deactivate user; check historical records | No delete; deactivation audited; old records still show user | FS-014-1, FS-016-1 |
| OQ-ACC-07 | Assign admin+analyst in same tenant without / with justification | Rejected without; accepted with, audited & flagged | FS-015-1 |
| OQ-ACC-08 | Trigger login fail, permission change, export, integrity failure | All appear in security log | FS-132-1 |

### 3.3 Ingestion
| ID | Objective / steps | Expected result | Trace |
|---|---|---|---|
| OQ-ING-01 | Ingest dataset; compute SHA-256 independently; inspect store | Hashes equal; stored read-only; no write path to original | FS-020-1/2, FS-024-1 |
| OQ-ING-02 | Flip one byte in stored file (OS level, test instance); start run; call verify | Run aborted; INTEGRITY_FAILED; audit + security events | FS-021-1/2; RSK-04 |
| OQ-ING-03 | Ingest files with missing voxel size / kVp | Fields null, not defaulted; flagged | FS-022-1; RSK-01 |
| OQ-ING-04 | Ingest spacing variants: mm-labelled, µm-labelled, 0, negative, 500 µm, anisotropic 2%, header conflict | Normalised correctly or blocked per rules; morphometry refused when unverified | FS-023-1/2; RSK-01/02 |
| OQ-ING-05 | Ingest same file twice in study; assign two datasets to same specimen/timepoint/site | Blocking warning / constraint error; confirmation with reason audited | FS-025-1; RSK-03 |
| OQ-ING-06 | Ingest malformed and unsupported files | INGEST_REJECTED with reason; file hash logged | FS-026-1 |

### 3.4 QC
| ID | Objective / steps | Expected result | Trace |
|---|---|---|---|
| OQ-QC-01 | Run QC on phantoms engineered to fail each check (saturation, missing slice, ROI outside FOV) | Correct PASS/WARN/FAIL; version & threshold stored | FS-030-1, FS-031-1 |
| OQ-QC-02 | Start analysis on QC-FAIL dataset; then override without reason; with reason | Blocked; blocked; allowed and printed in report | FS-032-1; RSK-05 |
| OQ-QC-03 | Ingest volume with flipped orientation metadata | QC-ORI flags; ROI view shows orientation markers | FS-030-1; RSK-36 |

### 3.5 ROI
| ID | Objective / steps | Expected result | Trace |
|---|---|---|---|
| OQ-ROI-01 | Create ROI with physical parameters; compute mask volume vs analytic | Within tolerance; version immutable | FS-040-1 |
| OQ-ROI-02 | Edit ROI without reason; with reason | Rejected; new version, old retained, audited with old/new | FS-041-1 |
| OQ-ROI-03 | Attempt analysis without "ROI verified" | Blocked | FS-042-1 |

### 3.6 Segmentation and models
| ID | Objective / steps | Expected result | Trace |
|---|---|---|---|
| OQ-SEG-01 | Run segmentation; inspect result record | Label map, model hash, preproc config stored | FS-050-1, FS-051-1 |
| OQ-SEG-02 | Load model with swapped label map (1↔2); import mask with value 5; inspect report legend | Load rejected; import rejected; legend from stored map | FS-054-1/2; RSK-08 |
| OQ-SEG-03 | Correct segmentation; inspect versions | v0 unchanged; v1 with reason, voxel deltas, user, time | FS-052-1, FS-053-1; RSK-13 |
| OQ-SEG-04 | Run on known high-uncertainty case | REVIEW_REQUIRED flag | FS-055-1; RSK-09 |
| OQ-SEG-05 | Run on dataset with acquisition parameters outside model's validated domain | Out-of-domain warning recorded and printed | RSK-11 |
| OQ-MOD-01 | Replace model file with altered copy | Load refused; integrity event | FS-111-1; RSK-10 |
| OQ-MOD-02 | Attempt production run with EXPERIMENTAL model | Refused; sandbox run watermarked | FS-112-1 |

### 3.7 Morphometry
| ID | Objective / steps | Expected result | Trace |
|---|---|---|---|
| OQ-MOR-01 | Inspect metric registry and result rows | Each metric: symbol, unit, definition, versions, voxel size | FS-060-1, FS-061-1 |
| OQ-MOR-02 | Run phantom suite (volumes, plate thickness, sphere diameters) at 3 voxel sizes incl. anisotropic | Within tolerances in VERIFICATION_PLAN §5 | FS-062-1; RSK-14 |
| OQ-MOR-03 | Request density without calibration | Value empty, reason NO_CALIBRATION | FS-063-1; RSK-15 |

### 3.8 Statistics and blinding
| ID | Objective / steps | Expected result | Trace |
|---|---|---|---|
| OQ-STA-01 | Edit locked SAP; unblind with unlocked SAP | Rejected; rejected | FS-070-1/2; RSK-16 |
| OQ-STA-02 | Exclude specimen without reason; with reason | Rejected; listed in report | FS-072-1 |
| OQ-STA-03 | Compare stats output to reference implementation (e.g., R or hand-calculated) on fixed dataset | Agreement to stated precision | FS-071-1 |
| OQ-STA-04 | Re-run stats; inspect provenance | Same results; seed and versions recorded | FS-071-1; RSK-17 |
| OQ-BLD-01 | As analyst pre-unblinding: inspect UI, API, CSV, PDF, filenames for group info | No allocation information leaked | FS-075-1; RSK-12 |
| OQ-BLD-02 | Unblind without permission / without password / without reason | Rejected; valid unblind audited | FS-075-2 |
| OQ-BLD-03 | Edit ROI after unblinding; generate report | Edit flagged post_unblinding in report | FS-076-1 |

### 3.9 Reporting, signatures
| ID | Objective / steps | Expected result | Trace |
|---|---|---|---|
| OQ-REP-01 | Generate report; check provenance fields against DB | Complete and consistent | FS-080-1; RSK-18 |
| OQ-REP-02 | Export PDF/CSV/JSON/NIfTI/audit; open in independent tools | Readable; content matches | FS-081-1 |
| OQ-REP-03 | Regenerate report | Numerics identical/within tolerance; mismatch raises error (challenge by altering config) | FS-082-1 |
| OQ-REP-04 | Export CSV under de_DE locale; re-import | Dot decimal, full precision, units in header | FS-083-1; RSK-19 |
| OQ-SIG-01 | Attempt DRAFT→APPROVED directly | 409, not applied | FS-090-1 |
| OQ-SIG-02 | Sign with/without password | Requires password; manifestation shows name, UTC time, meaning in UI and PDF | FS-091-1, FS-092-1 |
| OQ-SIG-03 | Change underlying segmentation after approval | Signature INVALIDATED; report returns to DRAFT | FS-093-1; RSK-26 |
| OQ-SIG-04 | Author attempts to approve own report | Rejected | FS-015-2 |

### 3.10 Audit trail
| ID | Objective / steps | Expected result | Trace |
|---|---|---|---|
| OQ-AUD-01 | Attempt UPDATE/DELETE on audit_log via SQL (test instance) | Trigger aborts | FS-100-1 |
| OQ-AUD-02 | Perform representative actions; inspect entries | All fields populated incl. old/new and reason | FS-101-1 |
| OQ-AUD-03 | With triggers dropped (simulated attacker), modify, insert, delete, reorder entries; run verification | Each tamper detected, first broken link reported | FS-102-1; RSK-20 |
| OQ-AUD-04 | Search API and config for any means to disable audit in production mode | None found; attempt via env var ignored in production mode | FS-103-1 |
| OQ-AUD-05 | Recompute an entirely new consistent chain; verify against external anchor | Mismatch detected | FS-102-2; RSK-21 |
| OQ-AUD-06 | Change client clock; perform actions | Server UTC timestamps; monotonic seq | FS-106-1; RSK-22 |
| OQ-AUD-07 | Filter and export audit trail to CSV/PDF | Human-readable, includes verification status | FS-104-1 |

### 3.11 Configuration, reproducibility, data management
| ID | Objective / steps | Expected result | Trace |
|---|---|---|---|
| OQ-CFG-01 | Change a parameter; run; inspect snapshot | Snapshot reflects resolved values; distinct hash | FS-110-1; RSK-27 |
| OQ-CFG-02 | Re-run identical analysis 3× (CPU deterministic mode; GPU if used) | Bitwise identical (CPU) / within tolerance (GPU) | FS-113-1; RSK-28 |
| OQ-BKP-01 | Run backup; inspect manifest | DB, files, models, chain head included with hashes | FS-120-1; RSK-30 |
| OQ-BKP-02 | Restore to clean instance; run verification | All hashes match; chain VALID; report regenerates identically | FS-121-1 |
| OQ-RET-01 | Delete record within retention | 423 blocked, audited attempt | FS-122-1; RSK-31 |
| OQ-RET-02 | Post-expiry delete: single user; dual approval; under legal hold | Rejected; succeeds and audited; blocked | FS-123-1 |
| OQ-RET-03 | After purge, verify audit entries retained | Retained per policy | FS-105-1 |
| OQ-ARC-01 | Export study archive; verify MANIFEST.sha256 independently | All files verify; open formats | FS-124-1; RSK-33 |
| OQ-DB-01 | Concurrent write load test; integrity check | No corruption; integrity_check ok | RSK-32 |
| OQ-DOC-01 | Review user manual vs functions/metric registry | Complete | FS-140-1 |
| OQ-DOC-02 | Review release notes | Changes, verification ref, limitations present | FS-141-1 |

## 4. Deviations and failures
Each failure → deviation record (ID, test, description, root cause, impact, fix via CHANGE_CONTROL, retest reference). Retests use the same test ID with suffix `-R1`, `-R2`.

## 5. Acceptance criteria
All tests for S ≥ 4 risks pass. Any other failure has an approved deviation with justification. Traceability matrix updated with test_id, test_file and status for every row.

## 6. OQ summary report
Lists executed tests, pass/fail counts, deviations, open items, conclusion, approvals (Engineering, Quality — Quality independent of test execution).
