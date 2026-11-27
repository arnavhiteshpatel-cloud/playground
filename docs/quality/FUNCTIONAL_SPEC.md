# OsteoQuant — Functional Specification (FS)

| Field | Value |
|---|---|
| Document ID | OQ-QMS-FS-001 |
| Version | 0.1 (DRAFT) |
| Date | 2026-11-27 |
| Traces to | OQ-QMS-URS-001 |
| Owner | Engineering Lead (TBD) |

> **Status: DRAFT — not validated; not a claim of Part 11 compliance or GLP validation.**

## 1. Conventions
- FS IDs use the form **FS-<URS number>-<n>** (e.g., FS-020-1 implements URS-020). Some FS items satisfy additional URS items, listed in "Also".
- "Shall" statements are testable. Proposed test names appear in traceability_matrix.csv.
- Architecture context: Python/FastAPI backend, SQLite database, local/object file store, browser viewer. Module names refer to `osteoquant/` packages (api, audit, io, qc, roi, segment, morphometry, stats, study, report, ml, uncertainty).

## 2. Functional specifications

### 2.1 General
| FS ID | Specification | Also |
|---|---|---|
| FS-001-1 | UI footer and login page display: "Research use only. Not for diagnostic or clinical use. Not validated." Text is configuration-controlled. | |
| FS-001-2 | Every PDF report page footer and CSV header comment block contains the RUO statement. | URS-080 |
| FS-002-1 | `osteoquant.__version__` follows SemVer; build embeds git commit SHA and build timestamp; exposed via `GET /api/version` and embedded in all outputs. | URS-080 |

### 2.2 Access control
| FS ID | Specification | Also |
|---|---|---|
| FS-010-1 | Users table has immutable `user_id` (UUID), unique `username`, `full_name`, `tenant_id`, `status` (active/locked/deactivated). Unique constraint on username globally. | URS-014 |
| FS-010-2 | No built-in shared accounts; installer forces creation of a named initial admin and disables any bootstrap credential. | |
| FS-011-1 | Permission matrix (code constant + documentation): **admin** — user/role/tenant config, retention, backup; no analysis edits. **analyst** — ingest, QC override (with reason), ROI, segmentation correction, run analyses, draft reports. **reviewer** — review, approve/reject, sign; cannot edit data. **viewer** — read-only. | URS-015 |
| FS-011-2 | Every API endpoint declares required permission; a test enumerates all routes and fails if any route lacks a declaration. | |
| FS-012-1 | All data queries are scoped by `tenant_id` from the authenticated session via a single repository layer; direct un-scoped queries are prohibited (lint/test enforced). File-store paths are namespaced by tenant. | |
| FS-012-2 | Cross-tenant object access returns HTTP 404 (not 403) to avoid existence disclosure, and is logged as a security event. | URS-132 |
| FS-013-1 | Password policy: min length 12, checked against a common-password list; hashed with Argon2id (or bcrypt) with per-user salt. | |
| FS-013-2 | Account locks after 5 consecutive failed logins (configurable); unlock by admin is audited. | URS-016 |
| FS-013-3 | Session inactivity timeout 30 min (configurable); session tokens are random, server-side revocable, HttpOnly/Secure cookies. | |
| FS-014-1 | No DELETE endpoint for users; deactivation sets status and timestamp; `user_id` never reused. | |
| FS-015-1 | Assigning admin plus analyst/reviewer to the same user in one tenant requires a justification text and is audited and flagged in the access review report. | |
| FS-015-2 | The reviewer signing an "approved" signature on a report must differ from the report author and from any user who edited ROI/segmentation in that report's scope. | URS-090 |
| FS-016-1 | User/role/tenant changes emit audit events `user.create`, `user.role_change`, `user.deactivate`, `user.unlock`. | URS-100 |

### 2.3 Ingestion
| FS ID | Specification | Also |
|---|---|---|
| FS-020-1 | Ingestion streams each file, computes SHA-256, stores hash, size, original filename, upload user and UTC time in `files` table before any parsing. | URS-024 |
| FS-020-2 | Files are stored content-addressed (`<tenant>/<sha256[0:2]>/<sha256>`); write-once; file-store permissions read-only after write. | URS-024 |
| FS-021-1 | Before each analysis run the job re-hashes all input files; mismatch aborts the run, sets dataset status `INTEGRITY_FAILED`, and emits audit + security events. | URS-132 |
| FS-021-2 | `POST /api/datasets/{id}/verify` performs on-demand verification; result is audited. | |
| FS-022-1 | Metadata extractor reads header fields per supported format into a typed `AcquisitionMetadata` record (voxel_size_xyz, unit, kvp, ua, filter, integration_ms, recon_params, scanner, calibration_id). Missing fields are explicitly `null`, never defaulted silently. | |
| FS-023-1 | Voxel spacing rules: all three spacings present and >0; units normalised to µm internally; plausibility range 0.5–200 µm (configurable); anisotropy >1% flagged; conflicting header sources (e.g., log file vs image header) → block. | URS-030 |
| FS-023-2 | Physical-unit computations require `spacing_status = VERIFIED`; otherwise morphometry endpoints return an error and reports omit physical units. | URS-060 |
| FS-024-1 | No API/UI path writes to original files; derived data (resampled volumes, masks) are new objects referencing source hashes. | |
| FS-025-1 | Datasets link to `study_id`, `specimen_id`, `timepoint`, `site/side`. Unique constraint on (study, specimen, timepoint, site); duplicate content hash within a study triggers a blocking warning requiring analyst confirmation with reason. | |
| FS-026-1 | Supported formats list is versioned in code and docs; parser failures produce `INGEST_REJECTED` with reason code; rejected files remain hashed and logged. | |

### 2.4 QC
| FS ID | Specification | Also |
|---|---|---|
| FS-030-1 | QC checks implemented as registered plug-ins with ID, version, threshold config: QC-INT (saturation % voxels at min/max), QC-SLC (missing/duplicate slices), QC-ORI (orientation metadata present & consistent), QC-FOV (ROI fully within volume), QC-CAL (calibration present when density requested), QC-SPC (voxel spacing status). | |
| FS-031-1 | QC results stored per dataset: check ID, version, threshold, measured value, PASS/WARN/FAIL. | |
| FS-032-1 | Analysis endpoints refuse datasets with any FAIL unless an `qc_override` exists (analyst role, reason ≥ 10 characters, audited). Override is printed in the report QC section. | URS-080 |

### 2.5 ROI
| FS ID | Specification | Also |
|---|---|---|
| FS-040-1 | ROI object: `roi_id`, `version`, `dataset_id`, method (e.g., cylinder centred on defect axis), parameters in physical units, landmark coordinates, binary mask hash. Versions are immutable; edits create a new version. | |
| FS-041-1 | ROI create/edit emits `roi.create`/`roi.update` with old/new parameters and required reason for updates. | URS-101 |
| FS-042-1 | Viewer renders ROI overlay in axial/coronal/sagittal planes; analysis requires an explicit "ROI verified" action by the analyst (audited). | URS-090 |

### 2.6 Segmentation
| FS ID | Specification | Also |
|---|---|---|
| FS-050-1 | Canonical label map: 0 = background, 1 = new bone, 2 = residual graft, 3 = host bone. Stored as JSON in model manifest and in every segmentation result. | |
| FS-051-1 | Segmentation record stores model_id, model_version, model_sha256, preprocessing config hash, inference device type and library versions. | URS-110 |
| FS-052-1 | Automated prediction saved as version 0 (immutable). Corrections saved as new versions with parent pointer; UI can toggle/compare versions. | |
| FS-053-1 | Correction save requires reason; stores per-class voxel deltas, editing tool used, user, UTC time; emits `seg.correct`. | URS-101 |
| FS-054-1 | At model load: manifest label map must equal canonical map (exact key/value match) or the load fails. At mask import: unique values ⊆ {0,1,2,3} and dtype integer, else reject. | |
| FS-054-2 | Report legend colors/names are generated from the stored label map (never hard-coded separately). | URS-080 |
| FS-055-1 | Per-dataset uncertainty score (e.g., mean voxel entropy within ROI) stored; results above threshold flagged `REVIEW_REQUIRED`. | |

### 2.7 Morphometry
| FS ID | Specification | Also |
|---|---|---|
| FS-060-1 | Metric registry with ID, name, symbol (Bouxsein nomenclature where applicable), unit, operational definition, algorithm version. Initial set: TV, NBV (new bone volume), RGV (residual graft volume), HBV (host bone volume), NBV/TV, RGV/TV, fill fraction (NBV+RGV)/TV, and Tb.Th/Tb.Sp (distance-transform method) for new bone where applicable. | |
| FS-061-1 | Each result row stores value, unit, voxel_size, roi_version, seg_version, metric algorithm version, config snapshot ID. | URS-110 |
| FS-062-1 | Phantom suite: synthetic spheres, cylinders, plates and slabs of known volume/thickness at several voxel sizes; verification tolerances defined in VERIFICATION_PLAN.md. | |
| FS-063-1 | Density metrics computed only if `calibration_id` linked and QC-CAL PASS; otherwise column present but value empty with reason code `NO_CALIBRATION`. | |

### 2.8 Statistics and blinding
| FS ID | Specification | Also |
|---|---|---|
| FS-070-1 | Statistical analysis plan (SAP) object: outcomes, groups, tests, alpha, multiplicity method, exclusion criteria. Lock action (reviewer/analyst lead) is audited; locked SAP is immutable; amendments create new version with reason. | |
| FS-070-2 | Unblinding (FS-075-2) requires a locked SAP. | |
| FS-071-1 | Stats output stores SAP version, analysis table hash, library versions (e.g., SciPy/statsmodels), random seed. | |
| FS-072-1 | Analysis table includes all specimens; exclusions are flags with reason and user; report lists excluded specimens and reasons. | |
| FS-075-1 | Group allocation stored in separate table accessible only via `allocation:read` permission; before unblinding, UI/API/exports show coded IDs only. | |
| FS-075-2 | Unblind action: role with `study:unblind` permission, password re-entry, reason; audited `study.unblind`. | URS-092 |
| FS-076-1 | ROI/segmentation edits made after unblinding are tagged `post_unblinding=true` and listed in the report. | |

### 2.9 Reporting and export
| FS ID | Specification | Also |
|---|---|---|
| FS-080-1 | Report provenance section: input hashes, software version + commit, model sha256, config snapshot hash, ROI/seg versions, QC status & overrides, users and UTC timestamps, SAP version, unblinding time. | |
| FS-081-1 | Export endpoints: PDF (report), CSV (metrics), JSON (full provenance), NIfTI or TIFF (label maps), CSV/JSON (audit trail). | URS-124 |
| FS-082-1 | `report.regenerate` re-runs from stored inputs/config and compares CSV numeric content to the original; differences beyond tolerance raise an error. | URS-113 |
| FS-083-1 | CSV writer: UTF-8, `.` decimal, `,` separator, header `name [unit]`, `repr`-round-trip float precision, ISO 8601 UTC timestamps. | |

### 2.10 Review and signatures
| FS ID | Specification | Also |
|---|---|---|
| FS-090-1 | State machine: DRAFT → IN_REVIEW → APPROVED or REJECTED → (REJECTED → DRAFT). Invalid transitions return 409 and are not applied. | |
| FS-091-1 | Signature record: user_id, printed full name, meaning (AUTHORED/REVIEWED/APPROVED), UTC timestamp, record hash. Rendered in UI and PDF. | |
| FS-092-1 | Signing endpoint requires current password in the request; failure count contributes to lockout. | URS-013 |
| FS-093-1 | Record hash = SHA-256 over canonical JSON of report content + provenance. Any change to underlying data recomputes the hash; signatures with non-matching hash shown as INVALIDATED and report returns to DRAFT. | |

### 2.11 Audit trail
| FS ID | Specification | Also |
|---|---|---|
| FS-100-1 | `audit_log` table insert-only at application layer (no UPDATE/DELETE code paths); SQLite triggers abort UPDATE/DELETE on `audit_log`. | URS-103 |
| FS-101-1 | Entry fields: seq (monotonic), entry_id, tenant_id, user_id, timestamp_utc, action, object_type, object_id, old_value_hash/old_value, new_value_hash/new_value, reason, client info, prev_hash, entry_hash. | |
| FS-102-1 | entry_hash = SHA-256(canonical(entry fields) ‖ prev_hash); genesis entry per tenant. Verification walks the chain and reports first broken link, gaps in seq, and timestamp regressions. | |
| FS-102-2 | Chain head hash periodically (daily) exported/anchored outside the database (e.g., to backup target and a signed log file) to detect wholesale chain replacement. | URS-120 |
| FS-103-1 | No API endpoint modifies audit configuration; audit logging cannot be disabled by configuration in production mode. | |
| FS-104-1 | Audit viewer with filters (study, user, object, action, date range) and CSV/PDF export including verification status. | |
| FS-105-1 | Retention purge (FS-123-1) never purges audit entries of records still under retention; purged-record audit entries are retained per policy. | |
| FS-106-1 | Server timestamps from system clock in UTC; startup check warns if NTP sync unavailable; client-supplied timestamps never used for audit. | |

### 2.12 Configuration and models
| FS ID | Specification | Also |
|---|---|---|
| FS-110-1 | Run start serialises the effective configuration (all defaults resolved) to canonical JSON; stores it with SHA-256 `config_snapshot_id`. | |
| FS-111-1 | Model registry: release manifest (model_id, version, sha256, label map, training-data reference, performance summary, release status, approver). Loader verifies sha256 before use. | URS-050 |
| FS-112-1 | Production run endpoints accept only models with status RELEASED; EXPERIMENTAL models require "research sandbox" flag and outputs are watermarked "EXPERIMENTAL MODEL". | |
| FS-113-1 | Deterministic mode: fixed seeds, deterministic algorithms flag for inference, CPU reference path; tolerance for GPU defined per metric. | |

### 2.13 Data management, security, documentation
| FS ID | Specification | Also |
|---|---|---|
| FS-120-1 | Backup job: SQLite online backup API snapshot + file-store sync + model registry + chain-head export; backup manifest with hashes; job result audited. | |
| FS-121-1 | Restore tool: restores to a target, verifies all file hashes against manifest, runs audit-chain verification, outputs a restore verification report. | |
| FS-122-1 | Retention policy objects per tenant/study (period, trigger event). Delete endpoints check retention and legal hold; return 423 if blocked. | |
| FS-123-1 | Post-expiry deletion requires request (admin) + approval (second authorized user), legal-hold check; audit retains deletion event with record hashes. | |
| FS-124-1 | Study archive export: ZIP/TAR with originals, derived data, config snapshots, reports, audit-trail CSV/JSON, `MANIFEST.sha256`, and format README. | |
| FS-130-1 | Production deployment requires TLS; HTTP redirected; HSTS enabled. At-rest encryption delegated to volume encryption (documented in IQ). | |
| FS-131-1 | Dependencies pinned with hashes in lock file; CI runs vulnerability audit on each build. | |
| FS-132-1 | Security events (login success/failure, lockout, permission change, export, integrity failure, cross-tenant attempt) logged with user, IP and time. | |
| FS-140-1 | User manual sections map one-to-one to UI functions and metric registry definitions. | |
| FS-141-1 | Release notes template includes change IDs (CHANGE_CONTROL.md), verification report reference and known limitations. | |
