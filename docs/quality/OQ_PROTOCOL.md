# OsteoQuant Desktop: Operational Qualification (OQ) Protocol

| Field | Value |
|---|---|
| Document ID | OQ-QMS-OQ-001 |
| Version | 0.2 (DRAFT), Generation-2 desktop re-baseline |
| Date | 2026-11-27 |
| Prerequisite | Approved, executed IQ (OQ-QMS-IQ-001) on the same workstation |
| Related | URS / FS v0.2, RISK_ASSESSMENT.md, traceability_matrix.csv, ENGINEERING_VALIDATION_DOSSIER.md |

> **Status: DRAFT template. Never executed. No claim of 21 CFR Part 11 compliance, GLP compliance, computerised-system validation or regulatory acceptance.**
> Steps marked "not implemented" in the Trace column test functions the current build does not have; they are kept so that the protocol shows what the requirements demand. They will fail until the function exists.

## 1. Objective
Demonstrate that each specified function of OsteoQuant Desktop operates as intended across its operating range, including negative and challenge conditions, on a qualified workstation.

## 2. Approach
- Risk-based depth (CSA/GAMP benchmark): functions with risk S ≥ 4 are tested with scripted tests with predefined expected results; lower-risk functions may use unscripted testing with a recorded summary.
- **Automated tests as OQ evidence.** The pytest suite (`tests/`, `tests/desktop/` with `QT_QPA_PLATFORM=offscreen`) may be executed as OQ evidence when the test code is version-controlled and reviewed, traced in `traceability_matrix.csv`, run on the qualified workstation (or an identical IQ'd one), and the raw log with software version and timestamp is retained. The Trace column names the FS items; the matrix names the tests. Engineering test runs recorded in ENGINEERING_VALIDATION_DOSSIER.md are **not** OQ execution.
- **Test data:** controlled set `OQ-DATA-vX` (synthetic phantoms from `osteoquant.desktop.demo`, malformed and tampered files, a saturated volume, TIFF stacks without spacing, licence files signed with an OQ test key) stored with a SHA-256 manifest.
- **Test accounts:** in one OQ project, named users for each role (admin, analyst, reviewer, viewer).

## 3. Test cases
Each test: ID · objective and key steps · expected result · trace (FS / risk). Record actual result, P/F, evidence reference, tester, date.

### 3.1 General and offline operation
| ID | Objective / steps | Expected result | Trace |
|---|---|---|---|
| OQ-GEN-01 | Inspect About, start page, PDF and CSV for the RUO / not-validated statement | Present on all | FS-001-1/2; RSK-34 |
| OQ-GEN-02 | Compare the version in About, status bar, PDF and stored measurement | Identical | FS-002-1 |
| OQ-OFF-01 | With the network disconnected: create project, import, QC, analyse, edit, sign, report, verify licence, run `--selftest` | All succeed | FS-210-1; RSK-44 |
| OQ-OFF-02 | Run the self-test and a full workflow under an OS-level connection monitor (or with socket creation blocked) | No outbound connection attempts | FS-211-1, FS-201-1; RSK-44 |

### 3.2 Access control
| ID | Objective / steps | Expected result | Trace |
|---|---|---|---|
| OQ-ACC-01 | Create a project with a weak password, then a strong one; attempt a second user with the same user name | Weak refused; named admin created; duplicate name refused | FS-010-1/2 |
| OQ-ACC-02 | As admin, create users for each role in the desktop; deactivate one | Possible in the application and audited (not implemented) | FS-010-3; RSK-23 |
| OQ-ACC-03 | For each role, attempt each action (import, analyse, edit, save revision, sign, open audit tab, export, unblind, delete) | Allowed/denied exactly as the permission matrix | FS-011-1/2; RSK-24 |
| OQ-ACC-04 | Sign in with a wrong password 5×, then the right one; wait 15 min | Locked, then unlocked; failures audited | FS-013-1/2 |
| OQ-ACC-05 | Leave a signed-in session idle beyond the configured period | Session locks; password needed (not implemented) | FS-013-3 |
| OQ-ACC-06 | Deactivate a user; try to sign in as that user; check that records still show the user | Sign-in refused; history attributable; `user.deactivate` audited | FS-014-1, FS-016-1 |
| OQ-ACC-07 | Admin who created a segmentation tries to approve it; admin analyses and signs work of others | Self-approval refused; admin/study-role separation needs justification (not implemented) | FS-015-1/2 |
| OQ-ACC-08 | Trigger failed sign-in, failed re-authentication, permission denial, user change, export; inspect the audit trail | All recorded | FS-132-1 |

### 3.3 Import
| ID | Objective / steps | Expected result | Trace |
|---|---|---|---|
| OQ-ING-01 | Import a NIfTI and a TIFF folder; compute SHA-256 of sources independently; re-hash sources after import; analyse and edit; check the stored image array | Hashes recorded; sources byte-identical; stored image unchanged | FS-020-1/2, FS-024-1; RSK-04 |
| OQ-ING-02 | Delete or alter one chunk of a stored scan (OS level, test project); run QC/analysis; run the project integrity check | Read refused with an integrity error; integrity check reports and audits (not implemented) | FS-021-1/2; RSK-04 |
| OQ-ING-03 | Import files with and without spacing and acquisition fields | Found vs assumed metadata shown; nothing silently defaulted | FS-022-1; RSK-01 |
| OQ-ING-04 | Enter spacing 0, negative, NaN, 99999, two values; leave spacing unconfirmed | Rejected; wizard cannot proceed until explicit confirmed values | FS-023-1/2; RSK-01/02 |
| OQ-ING-05 | Import the same file twice; import a second scan for an existing animal/time point | Duplicate rejected with reason; second scan flagged for confirmation (not implemented) | FS-025-1/2; RSK-03 |
| OQ-ING-06 | Import corrupt, truncated, unsupported files; untick one scan | Rejected with reasons, listed under *Rejected imports*, audited; no crash | FS-026-1/2 |

### 3.4 QC
| ID | Objective / steps | Expected result | Trace |
|---|---|---|---|
| OQ-QC-01 | Import phantoms engineered to fail deterministic checks (saturation, missing slice, non-finite) and heuristic checks | Correct statuses; deterministic/heuristic split; QC version and thresholds stored | FS-030-1, FS-031-1 |
| OQ-QC-02 | Analyse an "unsuitable" scan without and with an override reason | Blocked; allowed with reason and printed in report (not implemented) | FS-032-1; RSK-05 |
| OQ-QC-03 | Import a volume with flipped orientation metadata | Orientation check flags it | FS-030-1; RSK-36 |

### 3.5 ROI
| ID | Objective / steps | Expected result | Trace |
|---|---|---|---|
| OQ-ROI-01 | Define a cylindrical ROI at the crosshair; compare mask volume with the analytic value; redefine | Within tolerance; new version; old retained | FS-040-1 |
| OQ-ROI-02 | Define a manual ROI without and with a reason; inspect the audit trail | Reason required; `roi.save` with version, hash, reason | FS-041-1 |
| OQ-ROI-03 | Inspect ROI overlay in three planes and oblique; try to accept results without "ROI verified" | Overlay visible; acceptance blocked (not implemented) | FS-042-1/2 |

### 3.6 Segmentation and editing
| ID | Objective / steps | Expected result | Trace |
|---|---|---|---|
| OQ-SEG-01 | Analyse with the classical method and with a locked model; inspect the segmentation record | Method, model SHA-256, label map and preprocessing recorded | FS-050-1, FS-051-1 |
| OQ-SEG-02 | Paint/save label value 9; load a model with a permuted label map | Both refused (model check not implemented) | FS-054-1/2; RSK-08 |
| OQ-SEG-03 | Correct a segmentation; save without and with a reason; re-open the base version | Reason required; new version with parent, voxel deltas, user, tools; base unchanged | FS-052-1, FS-053-1; RSK-13 |
| OQ-SEG-04 | Analyse a scan with high uncertainty | Abstained voxels; endpoints not supported in results | FS-055-1; RSK-09 |
| OQ-EDT-01 | Brush, eraser, region grow, fill holes, interpolation with protection on/off; anisotropic voxels | Only targeted voxels change; brush round in µm | FS-056-1; RSK-47 |
| OQ-EDT-02 | 40 random edits, undo all, redo all | Original and final states restored exactly | FS-056-2; RSK-47 |

### 3.7 Morphometry
| ID | Objective / steps | Expected result | Trace |
|---|---|---|---|
| OQ-MOR-01 | Compare result columns and stored measurement with ENDPOINT_DEFINITIONS.md | Every endpoint defined, with unit; measurement linked to segmentation, ROI, configuration, version | FS-060-1, FS-061-1 |
| OQ-MOR-02 | Run the analytic phantom suite at three voxel sizes including anisotropic | Within VERIFICATION_PLAN §5 tolerances | FS-062-1; RSK-14 |
| OQ-MOR-03 | Request density without calibration | Not reported / labelled uncalibrated | FS-063-1; RSK-15 |

### 3.8 Statistics and blinding
| ID | Objective / steps | Expected result | Trace |
|---|---|---|---|
| OQ-STA-01 | Edit a locked SAP; unblind with an unlocked SAP | Both refused (not implemented) | FS-070-1/2; RSK-16 |
| OQ-STA-02 | Check that every scan appears in results; exclude a specimen without and with a reason | All scans listed; exclusion needs reason and is reported (exclusion not implemented) | FS-072-1/2 |
| OQ-STA-03 | Run the statistics reference suite | Agreement with published/reference values | FS-071-2 |
| OQ-STA-04 | Re-run statistics; inspect provenance | Same results; versions, seed and table hash recorded (not implemented) | FS-071-1; RSK-17 |
| OQ-BLD-01 | As analyst in a blinded study: inspect groups, specimens, results, exports | Only group codes | FS-075-1; RSK-12 |
| OQ-BLD-02 | Toggle *Blinded review mode* as admin | Group names, animal IDs, file names hidden; toggle audited | FS-075-3 |
| OQ-BLD-03 | Generate a report with unblinded allocation; export it as a user without `unblind` | Export denied and audited | FS-075-4 |
| OQ-BLD-04 | Unblind without permission, without password, without reason; edit an ROI afterwards and report | Refused; valid unblind audited; post-unblinding edit flagged (desktop unblind and flag not implemented) | FS-075-2, FS-076-1 |

### 3.9 Reporting and signatures
| ID | Objective / steps | Expected result | Trace |
|---|---|---|---|
| OQ-REP-01 | Generate a report; check each provenance item against the project | Complete and consistent | FS-080-1; RSK-18 |
| OQ-REP-02 | Export PDF, CSV, JSON provenance, label maps; open in independent tools | Readable; content matches (JSON/labels not implemented in desktop) | FS-081-1 |
| OQ-REP-03 | Regenerate a report; alter a configuration value and regenerate | Identical numerics; altered run detected (not implemented) | FS-082-1 |
| OQ-REP-04 | Export CSV under a comma-decimal OS locale; include a group named "=HYPERLINK(...)" | Dot decimal, full precision, units in header; formula neutralised | FS-083-1/2; RSK-19 |
| OQ-SIG-01 | Attempt invalid review decisions and reviews of non-existent objects | Refused | FS-090-1 |
| OQ-SIG-02 | Sign with wrong and right password; inspect Review panel, audit trail and PDF | Password required; name, UTC time, meaning shown (PDF sign-off table incomplete, CRO-13) | FS-091-1, FS-092-1 |
| OQ-SIG-03 | Enter a wrong password at signing 5× in the desktop; then sign in | Account locked (defect: desktop re-authentication bypasses lockout) | FS-092-2; RSK-23 |
| OQ-SIG-04 | Author tries to approve own segmentation and report | Refused and audited | FS-015-2 |
| OQ-SIG-05 | Approve a segmentation; save a new revision; regenerate the report | Signature bound to the old hash; UI shows it does not cover the new version (not implemented) | FS-093-1/2; RSK-26 |

### 3.10 Audit trail
| ID | Objective / steps | Expected result | Trace |
|---|---|---|---|
| OQ-AUD-01 | Attempt UPDATE/DELETE on `audit_log` with a SQLite tool (test project) | Trigger aborts | FS-100-1 |
| OQ-AUD-02 | Perform each desktop action of FS-100-2; inspect entries | Each recorded with user, time, object and details (old/new values where specified) | FS-100-2, FS-101-1 |
| OQ-AUD-03 | With triggers dropped (simulated attacker): modify, delete, reorder entries; *Verify chain* | Each detected; first bad entry reported | FS-102-1; RSK-20 |
| OQ-AUD-04 | Review settings, menus and environment variables for any way to disable or edit auditing | None | FS-103-1 |
| OQ-AUD-05 | Export an anchor; truncate the tail / rebuild a consistent chain; verify against the anchor | Mismatch detected (desktop anchor export not implemented) | FS-102-2; RSK-21 |
| OQ-AUD-06 | Change the OS time zone; perform actions | UTC timestamps; monotonic sequence | FS-106-1; RSK-22 |
| OQ-AUD-07 | Filter the Audit trail tab; open as analyst; export | Filters work; analyst denied; export available (export not implemented) | FS-104-1/2 |

### 3.11 Configuration, models, jobs
| ID | Objective / steps | Expected result | Trace |
|---|---|---|---|
| OQ-CFG-01 | Change a parameter; analyse; inspect the stored configuration | Snapshot of resolved values with distinct hash, linked to the measurement | FS-110-1; RSK-27 |
| OQ-CFG-02 | Analyse the same scan 3× | Bit-identical labels and metrics (CPU) | FS-113-1; RSK-28 |
| OQ-MOD-01 | Replace a model file with an altered copy; select an `rf:` model in the desktop | Load refused; rf refused | FS-111-1/2; RSK-10 |
| OQ-MOD-02 | Attempt a study analysis with an unreleased model | Refused or labelled experimental (not implemented) | FS-112-1 |
| OQ-JOB-01 | Run, cancel (queued and running), and fail jobs; interact with the UI during a job | Correct terminal states; errors shown; UI responsive | FS-114-1; RSK-46 |
| OQ-JOB-02 | Cancel an analysis before it writes; inspect jobs table, audit and segmentations | Terminal state recorded; no partial segmentation | FS-114-2; RSK-46 |

### 3.12 Data management
| ID | Objective / steps | Expected result | Trace |
|---|---|---|---|
| OQ-BKP-01 | Back up a project (SOP-006 and, when available, the application function) | Database, scans, revisions, reports, audit included with hash manifest | FS-120-1; RSK-30 |
| OQ-BKP-02 | Restore to a clean location; verify | Hashes match; chain intact; report regenerates identically | FS-121-1 |
| OQ-RET-01 | Delete study data within the retention period | Refused and audited (not implemented) | FS-122-1; RSK-31 |
| OQ-RET-02 | Delete study data as analyst; as admin with reason; check audit retention | Analyst refused; admin deletion audited; audit entries retained (second approval and legal hold not implemented) | FS-123-1, FS-105-1 |
| OQ-ARC-01 | Export a study archive; verify the manifest independently | All files verify; open formats (not implemented in desktop) | FS-124-1; RSK-33 |
| OQ-DB-01 | Open a corrupted and a truncated project database; reopen a valid one | Clear error; valid project reopens with chain intact | FS-125-1; RSK-32 |
| OQ-DB-02 | Open the same project in two application instances | Second instance warned or read-only (not implemented) | FS-125-2; RSK-32 |

### 3.13 Security
| ID | Objective / steps | Expected result | Trace |
|---|---|---|---|
| OQ-SEC-01 | Import the controlled malicious set (pickle-codec Zarr, huge-header NIfTI/Zarr, OME external reference, symlinked folder, zip traversal/bomb) | Each rejected without code execution or memory exhaustion | FS-133-1, FS-026-2; RSK-45 |

### 3.14 Measurement support, validation records, characterisation, longitudinal QC
| ID | Objective / steps | Expected result | Trace |
|---|---|---|---|
| OQ-SUP-01 | Analyse phantoms of a separable material at increasing noise | Support decisions as the policy; supported set shrinks with noise; advisor version recorded | FS-150-1; RSK-37 |
| OQ-SUP-02 | Analyse with material = metal, DBM, bone-derived, radiolucent, no graft, scarce graft | Statuses per FS-150-2 | FS-150-2 |
| OQ-SUP-03 | Check results, CSV and stored record for a not-supported endpoint; correct the segmentation | Value withheld with reason; raw value only in the record; decision carried over | FS-151-1/2; RSK-37 |
| OQ-SUP-04 | Inspect Results tab, results CSV, PDF and report CSV for a scan with conditional and not-supported endpoints | Status, conditions and advisor version present in all | FS-152-1/2; RSK-38 |
| OQ-SUP-05 | Analyse with material "unspecified"; then with sufficient and with too few measured reference samples | Not supported; supported; small samples ignored | FS-153-1 |
| OQ-VAL-01 | Evaluate validation records: synthetic, n < 8, voxel outside range, p95 > 15 %, other model SHA-256, other material | None qualifies; a compliant record qualifies | FS-160-1; RSK-39 |
| OQ-VAL-02 | Analyse with a learned model and a declared material, with and without a qualifying record | Outcome and reason stored with the segmentation | FS-160-2 |
| OQ-VAL-03 | Edit `models/validation_records.json` outside the application | Change detected (not implemented) | FS-161-1; RSK-39 |
| OQ-MAT-01 | Characterise a material-only phantom and a too-small mask | Profile with hash, voxel size, acquisition, version; small mask refused | FS-170-1/2; RSK-40 |
| OQ-MAT-02 | Reuse the characterisation at +30 % voxel size and different kVp | Refused with reason | FS-171-1 |
| OQ-MAT-03 | Run a characterisation from the desktop and attach it to a study | Stored and audited (not implemented) | FS-171-2 |
| OQ-LON-01 | Register aligned and deliberately shifted time-point pairs (0–400 µm) | QC passes aligned; flags shifts beyond 2 voxels | FS-180-1; RSK-41 |
| OQ-LON-02 | Day-0 assessment with complete, incomplete and out-of-tolerance inputs; granule tracking with disappearing graft | Supported only when complete and within tolerance; untracked fraction reported | FS-181-1/2 |
| OQ-LON-03 | Propagate an ROI to a later time point after known motion | ROI overlap within tolerance; QC reported | FS-182-1; RSK-07 |
| OQ-LON-04 | Pair time points of an animal in the desktop and run registration QC | Available and audited (not implemented) | FS-180-2 |

### 3.15 Licence and workflow timing
| ID | Objective / steps | Expected result | Trace |
|---|---|---|---|
| OQ-LIC-01 | Install licences: valid; payload edited; signature altered; unknown key; malformed | Valid accepted; all others invalid with reason and not installed | FS-190-1; RSK-42 |
| OQ-LIC-02 | Licences: expired yesterday; expiring today; perpetual; bound to another machine | Expired invalid; today valid; perpetual valid; other machine invalid | FS-190-2 |
| OQ-LIC-03 | Generate reports with no licence, a valid licence, a test licence | Evaluation watermark; none; test watermark | FS-191-1 |
| OQ-LIC-04 | Install a test-key licence without and with `OSTEOQUANT_ACCEPT_TEST_LICENCES` | Refused; accepted and labelled TEST | FS-192-1 |
| OQ-TIM-01 | New project: work on a scan; enable timing; work; disable; export | Nothing recorded while off; enable/disable/export audited | FS-200-1/2; RSK-43 |
| OQ-TIM-02 | Inspect where timing data are stored; monitor network during timing | Only in the project database; no transmission | FS-201-1 |
| OQ-TIM-03 | Scripted session with a > 60 s pause; export | Active time excludes the pause; per-class voxel changes and sign-offs correct | FS-202-1 |

### 3.16 Documentation
| ID | Objective / steps | Expected result | Trace |
|---|---|---|---|
| OQ-DOC-01 | Review the user guide against the desktop functions and ENDPOINT_DEFINITIONS.md | Complete | FS-140-1 |
| OQ-DOC-02 | Review the release notes | Changes, verification reference and limitations present (no release notes exist) | FS-141-1 |

## 4. Deviations and failures
Each failure creates a deviation record (ID, test, description, root cause, impact, fix via CHANGE_CONTROL, retest reference). Retests use the same test ID with suffix `-R1`, `-R2`.

## 5. Acceptance criteria
All tests for S ≥ 4 risks pass. Any other failure has an approved deviation with justification. The traceability matrix is regenerated (`scripts/build_traceability.py`) for the executed build. With the current build, every step marked "not implemented" fails; OQ cannot pass until those functions exist or the requirements are formally changed.

## 6. OQ summary report
Lists executed tests, pass/fail counts, deviations, open items, conclusion and approvals (Engineering; Quality independent of test execution).

## Change history
| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-11-27 | Generation-1 server/API test cases (tenants, TLS, endpoints) |
| 0.2 | 2026-11-27 | Re-baselined to the desktop; new sections for offline operation, editing, jobs, measurement support, validation records, material characterisation, longitudinal QC, licence and workflow timing; tenant/TLS cases removed |
