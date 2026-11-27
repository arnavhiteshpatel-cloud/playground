# OsteoQuant: Functional Specification (FS)

| Field | Value |
|---|---|
| Document ID | OQ-QMS-FS-001 |
| Version | 0.2 (DRAFT), Generation-2 desktop re-baseline |
| Date | 2026-11-27 |
| Traces to | OQ-QMS-URS-001 v0.2 |
| Owner | Engineering Lead (TBD) |

> **Status: DRAFT. Not approved, not validated. No claim of 21 CFR Part 11 compliance, GLP compliance, computerised-system validation or regulatory acceptance.**

## 1. Conventions
- FS IDs use the form **FS-<URS number>-<n>** (FS-020-1 implements URS-020). IDs from v0.1 keep their meaning where the function still applies; new items take the next free number.
- **Impl** states the implementation status found in the code on 2026-11-27: **Y** implemented, **P** partly implemented, **N** not implemented. It is not a verification status; verification status is in `traceability_matrix.csv` (VERIFIED / PARTIAL / GAP).
- Architecture context: offline PySide6/VTK desktop (`osteoquant/desktop/`) over the in-process library (`io`, `qc`, `roi`, `segment`, `morphometry`, `advisor`, `longitudinal`, `ml`, `stats`, `study`, `audit`, `report`, `licensing`). The study store is SQLite in WAL mode inside the project folder; scans are chunked Zarr stores. See `docs/desktop/ARCHITECTURE.md`.
- "Store" means `osteoquant.study.db.Store`; "services" means `osteoquant/desktop/services.py`.

## 2. Functional specifications

### 2.1 General
| FS ID | Specification | Impl | Also |
|---|---|---|---|
| FS-001-1 | The About dialog and start page state: research software, not a medical device, not validated for GLP or clinical use. | Y | |
| FS-001-2 | Every PDF report carries the RUO / not-validated banner; the CSV carries the data class and review status. | Y | URS-080 |
| FS-002-1 | `osteoquant.__version__` is shown in About and the status bar, stored with each measurement (`measurements.software_version`) and printed in the PDF. | Y | URS-080 |

### 2.2 Access control
| FS ID | Specification | Impl | Also |
|---|---|---|---|
| FS-010-1 | `users` table: integer `id` (never reused, no delete path), globally unique `username`, `full_name`, role, `active`, failed-login counter, `locked_until`. | Y | URS-014 |
| FS-010-2 | *File > New project* creates the project with one named administrator chosen by the user; there is no default or shared account; the password policy applies. | Y | |
| FS-010-3 | Administrators can create named users, assign roles and deactivate users from within the desktop application (audited). | N | URS-014, URS-016 |
| FS-011-1 | Permission matrix (`study.db.ROLES`): **admin** read, write, run, review, manage_users, unblind, delete, export; **analyst** read, write, run, export; **reviewer** read, review, export; **viewer** read. Every Store function calls `require()`; denials are audited `authz.denied`. | Y | URS-132 |
| FS-011-2 | Desktop menus, toolbars and tabs reflect the signed-in role (e.g. Audit trail tab only for review/manage_users; editing and analysis only with write/run). | P | |
| FS-013-1 | Password policy: at least 10 characters, an upper-case letter and a digit; scrypt (N = 2^14, r = 8, p = 1) with a per-user salt; constant-cost check for unknown users. | Y | |
| FS-013-2 | Five consecutive failed sign-ins lock the account for 15 minutes; failures and locks are audited. | Y | URS-132 |
| FS-013-3 | After a configurable idle period the desktop locks the session and requires the user's password to continue. | N | |
| FS-014-1 | Users are deactivated (`set_user_active`), never deleted; deactivation ends sessions immediately; inactive users cannot sign in or re-authenticate. | Y | |
| FS-015-1 | The system-administration role is separable from study roles (an admin who also analyses or signs needs a recorded justification, flagged in access review). | N | |
| FS-015-2 | A reviewer cannot approve a segmentation or report they created (`review.self_approval_denied` audited). | Y | URS-090 |
| FS-016-1 | User creation, activation and deactivation emit `user.create`, `user.activate`, `user.deactivate`; role changes emit `user.role_change`. | P | URS-100 |
| FS-017-1 | The installation guide and IQ define the OS permissions for project folders (read/write only for named study users; no shared OS accounts) and recommend disk encryption. | N | |

### 2.3 Import
| FS ID | Specification | Impl | Also |
|---|---|---|---|
| FS-020-1 | Import computes SHA-256 of each source file (manifest for folders) and the content hash of the voxel data plus spacing; slab-by-slab import yields the same content hash as a whole-volume read; hashes are stored on the scan record. | Y | URS-024 |
| FS-020-2 | The imported image array is written once into the scan's Zarr store; analysis and editing write separate label/ROI arrays and never rewrite the image. | Y | URS-024 |
| FS-021-1 | Every full read of a stored scan (QC, analysis) recomputes the content hash and raises `CorruptInput` on mismatch or missing chunks. | P | |
| FS-021-2 | *Tools > Verify project integrity* re-hashes every scan store, label revision and report file and records the result in the audit trail. | N | |
| FS-022-1 | `probe_source` reports format, shape, metadata found, metadata assumed and the spacing source (*file*, *assumed*, *missing*); format readers extract acquisition fields where present (TXM, DICOM, OME-TIFF, Bruker log). Missing fields stay empty, never silently defaulted. | P | |
| FS-023-1 | `validate_spacing`: three finite values > 0 within the plausibility range; otherwise the value is rejected with a message. | Y | |
| FS-023-2 | The import wizard cannot proceed while any scan has assumed or missing spacing; the user enters values and ticks *Confirmed*; the spacing source and any override are stored. | Y | |
| FS-024-1 | Import reads sources read-only and copies them into the project store; no code path writes to the source location. | Y | |
| FS-025-1 | Each scan is assigned to study, animal and time point in the wizard; a scan whose content duplicates an existing scan is rejected ("Duplicate"). | Y | |
| FS-025-2 | A second scan for the same animal and time point requires explicit confirmation with a reason. | N | |
| FS-026-1 | Unreadable, unsupported, duplicate and user-excluded sources are recorded in `desktop_import_log` with a reason, shown under *Rejected imports* and audited `scan.import_rejected`. | Y | URS-100 |
| FS-026-2 | Malformed files never crash a reader: parser errors map to `CorruptInput` / `VolumeTooLarge` / `UnsafeArchive`. | Y | URS-133 |

### 2.4 QC
| FS ID | Specification | Impl | Also |
|---|---|---|---|
| FS-030-1 | `qc.run_qc` runs after import; checks carry `basis` deterministic (e.g. missing slices, saturation, non-finite voxels, metadata completeness) or heuristic (rings, cupping, CNR, partial-volume risk); verdict suitable / review / unsuitable; QC at full resolution up to 2 GiB, otherwise on a decimated copy. | Y | |
| FS-031-1 | The QC record (qc_version, per-check value, threshold, status, basis, decimation note) is stored on the scan and the verdict is audited `scan.qc`. | Y | |
| FS-032-1 | Analysis of an "unsuitable" scan is refused unless a user with write permission records an override with a reason (audited, printed in the report). | N | URS-080 |

### 2.5 ROI
| FS ID | Specification | Impl | Also |
|---|---|---|---|
| FS-040-1 | ROI objects (cylinder, box, sphere, landmark, mask) are defined in µm, carry a definition SHA-256 and are stored as numbered versions (`rois`, UNIQUE(scan, version)); a change creates a new version. | Y | |
| FS-041-1 | ROI saves are audited `roi.save` with version, definition hash, method and reason; the manual ROI dialog requires a reason. | P | URS-101 |
| FS-042-1 | Axial, coronal and sagittal views with linked crosshair, an oblique reslice and a 3D panel display the image with label and ROI overlays. | Y | |
| FS-042-2 | Results of a scan are marked accepted only after an explicit, audited "ROI verified" action. | N | URS-090 |

### 2.6 Segmentation and editing
| FS ID | Specification | Impl | Also |
|---|---|---|---|
| FS-050-1 | Canonical label map: 0 background, 1 new bone, 2 residual graft, 3 host bone, 255 uncertain (abstained). The pipeline refuses tissue models that are not 4-class; the map is stored with each segmentation. | P | |
| FS-051-1 | The segmentation record stores method, model name, model SHA-256 (and ONNX SHA-256 for the ONNX runtime), ROI id and the preprocessing configuration. | P | URS-110 |
| FS-052-1 | The automated prediction is version 1 (`kind=automatic`); each saved correction is a new version (`kind=corrected`, `parent_id`) under a new labels key; earlier arrays are never overwritten. | Y | |
| FS-053-1 | *Save as new revision* requires a non-empty reason and records user, base version, per-class voxel changes and per-tool operation counts in the segmentation record and in the audit trail (`segmentation.save`, `segmentation.edit`). | Y | URS-101 |
| FS-054-1 | The label editor and `save_label_revision` reject label values outside {0, 1, 2, 3, 255}. | Y | |
| FS-054-2 | At model load the manifest label map must equal the canonical map, else the load fails; report legends are generated from the stored map. | N | URS-080 |
| FS-055-1 | Models that return probabilities produce a voxel entropy map; voxels above the abstention threshold become 255; the per-scan uncertain fraction is stored; in the desktop results a high uncertain fraction makes endpoints not supported. | Y | URS-151 |
| FS-056-1 | Tools: brush and eraser (radius in µm, round in physical space; 2D disk or 3D sphere), region grow (2D/3D), fill holes, interpolation between key slices. With *Protect other classes* painting changes only background voxels and the eraser only the active class. One mouse stroke is one operation. | Y | |
| FS-056-2 | Every operation returns a compressed sparse diff (indices, old and new values, bounding box, per-class delta); undo/redo through `QUndoStack` restores states bit-exactly; the last 500 operations are kept. | Y | |

### 2.7 Morphometry
| FS ID | Specification | Impl | Also |
|---|---|---|---|
| FS-060-1 | `defect_report_metrics` computes the endpoints of ENDPOINT_DEFINITIONS.md (TV, class volumes and fractions, mineral volume, bridging, radial ingrowth, new-bone architecture Tb.Th/Tb.Sp/Tb.N, density when calibrated) with units in the key names. | P | |
| FS-061-1 | Each measurement row stores metrics JSON, segmentation id, ROI id, configuration id and software version. | P | URS-110 |
| FS-062-1 | Analytic phantom suite (plates, rods, spheres, hollow cylinders, cubes) at several and anisotropic voxel sizes, with tolerances in VERIFICATION_PLAN.md; property tests for invariance and scaling. | Y | |
| FS-063-1 | Density statistics are labelled "uncalibrated grey value" unless a calibration is linked; the advisor marks tissue mineral density not supported without calibration. | Y | URS-150 |

### 2.8 Statistics and blinding
| FS ID | Specification | Impl | Also |
|---|---|---|---|
| FS-070-1 | Statistical analysis plan object (outcomes, groups, tests, alpha, multiplicity, exclusion criteria) with an audited lock; locked plans are immutable; amendments are new versions with a reason. | N | |
| FS-070-2 | Unblinding (FS-075-2) requires a locked plan. | N | |
| FS-071-1 | Statistics outputs store plan version, analysis-table hash, library versions and random seed. | N | |
| FS-071-2 | `osteoquant.stats` (ICC, Bland–Altman, Hedges' g, p-value adjustment, bootstrap CI, group comparisons, mixed model) reproduces published or reference-implementation values; bootstrap uses a fixed seed. | Y | |
| FS-072-1 | The results table lists every scan of the study, including *not analysed* and *not supported*. | Y | |
| FS-072-2 | Specimens can be excluded only with a reason and user; reports list exclusions. | N | |
| FS-075-1 | For blinded studies, users without `unblind` see group codes ("G-xxxx", "(blinded)") in group and specimen listings and in study exports. | Y | |
| FS-075-2 | Unblinding requires the `unblind` permission, password re-entry and a reason, and is audited `study.unblind`. Available from the desktop. | P | URS-076, URS-092 |
| FS-075-3 | Desktop *Blinded review mode* hides group names, animal IDs and file names in the project tree, results and viewer for every role; toggling is audited `ui.blinded_mode`. | Y | |
| FS-075-4 | Reports generated with unblinded allocation are marked; their export is denied to users without `unblind` (`report.blinded_download_denied`). | Y | |
| FS-076-1 | ROI/segmentation edits after unblinding are tagged `post_unblinding` and listed in the report. | N | |

### 2.9 Reporting and export
| FS ID | Specification | Impl | Also |
|---|---|---|---|
| FS-080-1 | The DefectFill PDF contains: banner, study and data class, software version, specimen table with reported (support-filtered) values, corrections table, measurement-support section, reproducibility block (config hash, version), sign-off table. Acquisition parameters are not yet printed (CRO-06). | P | URS-152 |
| FS-081-1 | The Reports tab exports PDF and CSV to a folder (audited `report.export`); JSON provenance and label maps (NIfTI/TIFF) are exportable. | P | URS-124 |
| FS-082-1 | Report regeneration recomputes from stored inputs and compares numeric content with the original; differences beyond tolerance raise an error. | N | URS-113 |
| FS-083-1 | CSV writer: UTF-8, `.` decimal, `,` separator, units in headers, round-trip float precision, ISO 8601 UTC timestamps, independent of the OS locale. | P | |
| FS-083-2 | Cells beginning with `=`, `+`, `-`, `@` are prefixed so spreadsheets do not execute them. | Y | URS-133 |

### 2.10 Review and signatures
| FS ID | Specification | Impl | Also |
|---|---|---|---|
| FS-090-1 | Review decisions are `approved`, `needs_changes`, `rejected`; reviews of unknown objects are refused. A draft → in review → approved/rejected state machine is not implemented. | P | |
| FS-091-1 | A review record stores reviewer, UTC time, decision, meaning (≥ 5 characters) and comment; the Review panel shows the history; the PDF sign-off table shows in-system signatures. | P | |
| FS-092-1 | `services.sign_review` requires the `review` permission and the signer's password; failures raise and are audited `review.reauth_failed`. | Y | URS-132 |
| FS-092-2 | Failed re-authentication counts towards the 5-failure lockout and is refused for inactive or locked accounts, in every front end (`Store.reauthenticate`). | P | URS-013 |
| FS-093-1 | Each review stores `object_sha256`: labels SHA-256 for segmentations, PDF SHA-256 for reports. | Y | |
| FS-093-2 | When the signed object is superseded (new revision, regenerated report) the UI and report show that the signature covers the earlier version only. | N | |

### 2.11 Audit trail
| FS ID | Specification | Impl | Also |
|---|---|---|---|
| FS-100-1 | `audit_log` is insert-only in code; SQLite triggers abort UPDATE and DELETE. | Y | URS-103 |
| FS-100-2 | Desktop actions emit audit events: sign-in/out, import and rejection, QC, jobs, analysis, ROI, label edits, reviews, reports and exports, screenshots, blinded mode, workflow-timing settings and export, scan views. | Y | |
| FS-101-1 | Entry fields: seq, UTC timestamp (µs), user_id, org_id, action, object type/id, details (canonical JSON: reason, hashes, deltas), prev_hash, row_hash. Old/new values only where the action records them. | P | |
| FS-102-1 | row_hash = SHA-256(prev_hash ‖ canonical fields); `verify_chain` reports the first altered, removed or reordered row; writes serialised with `BEGIN IMMEDIATE`. | Y | |
| FS-102-2 | `anchor()` exports (seq, head hash); `verify_chain(anchor)` detects truncation or rewrite; the desktop offers anchor export and verification against a saved anchor. | P | URS-120 |
| FS-103-1 | No desktop function or setting disables, edits or deletes audit entries. | Y | |
| FS-104-1 | *Audit trail* tab (review or manage_users permission): events with time, user, action, object; text and object-type filters; details pane; *Verify chain*. | Y | |
| FS-104-2 | The audit trail (filtered or whole) is exportable to CSV/PDF with the verification result. | N | |
| FS-105-1 | Study data deletion keeps all audit entries (append-only). | Y | URS-123 |
| FS-106-1 | Timestamps are UTC with microseconds from a single clock read; sequence numbers are monotonic. | Y | |
| FS-106-2 | IQ verifies workstation time synchronisation; the application warns when the system clock moves backwards relative to the last audit entry. | N | |

### 2.12 Configuration, models and jobs
| FS ID | Specification | Impl | Also |
|---|---|---|---|
| FS-110-1 | The resolved analysis configuration (defaults + user values) is serialised canonically, hashed (`config_hash`) and stored in `analysis_configs`, linked to the measurement. | P | |
| FS-111-1 | Model registry entries carry SHA-256; `load_model` verifies the hash before deserialising and uses `torch.load(weights_only=True)`; the ONNX runtime verifies the file hash. | Y | |
| FS-111-2 | Pickled random-forest models (`rf:`) are refused by the desktop (command line only, with a trusted-local flag). | Y | URS-133 |
| FS-112-1 | Models carry a release status; only RELEASED models are offered for study analyses; others are labelled experimental and watermarked. | N | |
| FS-113-1 | CPU pipeline runs are deterministic (fixed seeds, deterministic algorithms); tolerance for ONNX/GPU defined per metric. | P | |
| FS-114-1 | `JobManager` runs jobs on a `QThreadPool` with progress, cooperative cancellation at stage boundaries, error and traceback capture; the GUI thread stays responsive. | Y | |
| FS-114-2 | A job's terminal state is written to the `jobs` table and the audit trail before it is reported finished; a cancelled analysis stores no segmentation or measurement. | Y | |

### 2.13 Data management
| FS ID | Specification | Impl | Also |
|---|---|---|---|
| FS-120-1 | `Store.backup` writes a consistent SQLite copy (online backup API) and returns its SHA-256. A desktop *Back up project* function copying database, scan stores, revisions and reports with a hash manifest is not implemented; SOP-006 covers folder-level backup. | P | |
| FS-121-1 | A restored database opens, keeps its schema version and passes `verify_chain`; a restore-verification tool for whole projects re-hashes all files against the manifest. | P | |
| FS-122-1 | Retention period per organisation (`orgs.retention_days`) and per study is enforced: deletion within retention is refused and audited. | N | |
| FS-123-1 | `delete_study_data` requires `delete` permission and a reason, removes scan stores and reports, keeps the audit trail and marks the study deleted; second approval and legal hold are not implemented. | P | |
| FS-124-1 | Study archive export: data, configuration, audit trail, reports and `MANIFEST.sha256` in open formats. Currently `export_study` returns JSON records and audit only (API). | P | |
| FS-125-1 | The store opens in WAL mode with schema versioning; a corrupted or truncated database raises `DatabaseError`; reopening keeps the chain verifiable against an anchor; a read-only database refuses writes. | Y | |
| FS-125-2 | Opening a project already open in another application instance is detected and the second instance is warned or opened read-only. | N | |

### 2.14 Security
| FS ID | Specification | Impl | Also |
|---|---|---|---|
| FS-131-1 | Dependencies pinned with hashes; vulnerability audit (`pip-audit`) per release; SBOM; About lists bundled third-party components and licences. | P | |
| FS-132-1 | Security events audited: `auth.login`, `auth.login_failed`, `auth.reauth_failed`, `review.reauth_failed`, `authz.denied`, `review.self_approval_denied`, `user.*`, `report.export`, `report.blinded_download_denied`. | Y | |
| FS-133-1 | Safe-input checks: Zarr codec/dtype allow-list (no pickle), header-declared size checked before allocation, archive traversal/bomb/symlink/encrypted-member rejection, OME external references refused, symlinks refused, models loaded only with weights-only deserialisation. | Y | |

### 2.15 Documentation
| FS ID | Specification | Impl | Also |
|---|---|---|---|
| FS-140-1 | `docs/desktop/USER_GUIDE.md` sections map to the desktop functions and to ENDPOINT_DEFINITIONS.md. | P | |
| FS-141-1 | Release notes template: change IDs (CHANGE_CONTROL.md), verification-evidence reference (ENGINEERING_VALIDATION_DOSSIER.md), known limitations. | N | |

### 2.16 Measurement support and abstention
| FS ID | Specification | Impl | Also |
|---|---|---|---|
| FS-150-1 | `advisor.assess_support` evaluates intensity separability (Dice-optimal intensity oracle as upper bound), day-0 and validated-model mechanisms for the material, scan noise (relative units), voxel size and design, and returns per-endpoint status with reason and `advisor_version`. | Y | |
| FS-150-2 | Material-class rules: metals never supported; bone-derived grafts and DBM never intensity-supported for new bone; radiolucent grafts conditional; scarce graft refuses graft volume only; support must be robust to low graft share; no-graft design supports new-bone endpoints. | Y | |
| FS-151-1 | `apply_support` replaces every not-supported metric by `None` in `reported_metrics` and lists it with its reason in `suppressed_metrics`; raw metrics stay in the stored record. Desktop `reported_value` returns no value plus reason. | Y | |
| FS-151-2 | After a label revision, endpoints are recomputed with the base version's ROI and the advisor decision is carried over (`measurement_support` in the new measurement). | Y | |
| FS-152-1 | The Results tab shows a Support column (supported / flagged / not supported / not analysed), shows unsupported values as *not measured* with the reason on hover, and the results CSV includes per-endpoint support. | Y | |
| FS-152-2 | The PDF marks conditional values "(c)" and not-measured values "n/m", prints a per-specimen measurement-support section (status, reason/conditions, advisor version); the report CSV has `<endpoint>__support` columns. | Y | |
| FS-153-1 | Material "unspecified"/unknown makes graft/new-bone-split endpoints not supported unless measured reference samples above the minimum size are supplied; small samples are ignored and cannot bypass the bone-derived rule. | Y | |

### 2.17 Validation records
| FS ID | Specification | Impl | Also |
|---|---|---|---|
| FS-160-1 | `ValidationRecord.qualifies`: data class in {physical_phantom, ex_vivo, in_vivo} (synthetic never), n ≥ 8 specimens, voxel size within the validated range, graft-volume p95 absolute relative error ≤ 15 %; `validated_for` matches the exact model SHA-256 and material. | Y | |
| FS-160-2 | For learned models with a declared material, the pipeline calls `validated_for` and stores the outcome (`segmentation.validation_record`). | Y | |
| FS-161-1 | `models/validation_records.json` is protected: content hash recorded in the model registry, additions audited and approved under change control (SOP-007). | N | |

### 2.18 Material characterisation
| FS ID | Specification | Impl | Also |
|---|---|---|---|
| FS-170-1 | `characterise_material` (material-only scan) and `characterise_from_day0` produce a `MaterialCharacterisation` (relative-unit distribution, thickness median and p10–p90, voxel count, scan hash, voxel size, acquisition, version) usable as advisor reference samples. | Y | |
| FS-170-2 | Characterisations from masks below the minimum sample size are refused; small reference samples are ignored by the advisor. | Y | |
| FS-171-1 | `compatible_with` refuses reuse when voxel size differs by > 25 % or kVp, filter or scanner model differ. | Y | |
| FS-171-2 | The desktop runs a characterisation, stores it in the project, attaches it to a study/material and audits it. | N | |

### 2.19 Longitudinal QC
| FS ID | Specification | Impl | Also |
|---|---|---|---|
| FS-180-1 | `registration_qc`: block-wise residual displacement (masked NCC) ≤ 2 voxels is the pass criterion; Dice/NCC secondary; passes aligned pairs and flags shifted pairs. | Y | |
| FS-180-2 | The desktop pairs time points of an animal, runs registration with QC, shows the QC result and stores it with an audit record. | N | |
| FS-181-1 | Day-0 support requires computed `registered`, `qc_pass`, `untracked_fraction` and `max_displacement_um` within tolerance; any missing input gives "not supported". | Y | |
| FS-181-2 | `track_granules` reports per-granule displacement and the untracked volume fraction; `day0_propagation` and `change_map` give class-volume change. | Y | |
| FS-182-1 | `propagate_roi` maps a reference ROI to a later scan through rigid registration and reports registration QC. | Y | |

### 2.20 Licence verification
| FS ID | Specification | Impl | Also |
|---|---|---|---|
| FS-190-1 | `.oqlic` envelope: format, key_id, canonical payload string, detached Ed25519 signature over the exact payload bytes; unknown key, bad signature, altered payload, malformed JSON or invalid fields → state *invalid* with reason. | Y | |
| FS-190-2 | Expiry is inclusive of the last day; null expiry is perpetual; an optional machine fingerprint must match. | Y | |
| FS-191-1 | Without a valid licence: state *evaluation*, all features usable, reports watermarked "EVALUATION COPY - NOT FOR STUDY DECISIONS"; valid test licences watermark "TEST LICENCE - NOT A VALID PRODUCT LICENCE". | Y | URS-001 |
| FS-192-1 | The published test key is trusted only when `OSTEOQUANT_ACCEPT_TEST_LICENCES` is set; `PRODUCTION_KEYS` holds public keys only (currently none); `install_licence` copies a file only if it verifies. | Y | |

### 2.21 Workflow timing
| FS ID | Specification | Impl | Also |
|---|---|---|---|
| FS-200-1 | Timing is off by default (`desktop_settings.workflow_timing`); *Tools > Record workflow timing* enables it per project; nothing is recorded while off. | Y | |
| FS-200-2 | Enabling/disabling is audited `settings.workflow_timing`; export is audited `timing.export`. | Y | URS-100 |
| FS-201-1 | Events are stored only in `desktop_timing_events` of the project database; the application contains no transmission path. | Y | URS-211 |
| FS-202-1 | Events: scan_open, scan_close, first_edit, edit (tool, voxels changed per class), review_signoff, active_time (inputs ≤ 60 s apart); per-scan/user summary and raw-event CSV export. | Y | |

### 2.22 Offline operation
| FS ID | Specification | Impl | Also |
|---|---|---|---|
| FS-210-1 | All desktop functions, including licence verification and the `--selftest` end-to-end check, run without network access. | Y | |
| FS-211-1 | The desktop and library open no sockets and contain no telemetry; About states this. | Y | |

## 3. Retired FS items (not applicable to the desktop; IDs not reused)
| FS ID | Former specification (v0.1) | Reason |
|---|---|---|
| FS-012-1 | All queries scoped by tenant; file store namespaced by tenant. | Multi-tenant hosting (URS-012 retired). Organisation scoping remains in the Store for the optional API. |
| FS-012-2 | Cross-tenant access returns 404 and is logged. | Web API behaviour (URS-012 retired). |
| FS-130-1 | TLS required, HTTP redirect, HSTS. | No network transport (URS-130 retired). |

FS items revised with the same ID (meaning kept, mechanism changed for the desktop): FS-010-2 (project creation instead of installer), FS-011-2 (desktop actions instead of API routes), FS-013-1 (actual policy and scrypt; v0.1 named Argon2id and 12 characters), FS-013-3 (idle lock instead of web session cookies), FS-021-2 (menu function instead of endpoint), FS-042-1/042-2 (split), FS-054-1/054-2 (split by import vs model), FS-072-1/072-2 (split), FS-075-2 (now desktop), FS-093-1/093-2 (split), FS-106-1/106-2 (workstation clock), FS-120-1 (project backup).
