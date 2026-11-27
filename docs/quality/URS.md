# OsteoQuant — User Requirements Specification (URS)

> **Revision pending (2026-11-27, cycle-1 review QA-REG-02).** This draft describes the Generation-1 architecture (FastAPI server + browser workbench). The Generation-2 product is an offline desktop application (PySide6/VTK, in-process analysis library; the API is an optional integration interface). Requirements and protocols must be re-baselined to the desktop product before any qualification activity. Draft only; no compliance is claimed.


| Field | Value |
|---|---|
| Document ID | OQ-QMS-URS-001 |
| Version | 0.1 (DRAFT) |
| Date | 2026-11-27 |
| Owner | Product / Scientific Lead (TBD) |
| Approvals | Scientific Lead ___ · Engineering Lead ___ · Quality ___ |

> **Status: DRAFT — not validated; not a claim of Part 11 compliance or GLP validation.**

## 1. Purpose and intended use
OsteoQuant analyses **preclinical (animal) bone-defect micro-CT** data for **research use only (RUO)**: ingestion with file hashing, QC, defect ROI definition, 3-class segmentation (new bone / residual graft / host bone) with human correction, morphometry, statistics, and PDF/CSV reporting.

**Not intended** for diagnosis, treatment or monitoring of disease in humans or individual animals, nor (in its current unvalidated state) for generating records for GLP studies or regulatory submissions.

## 2. Conventions
- **Priority:** M = must, S = should, C = could.
- **Criticality (data-integrity / scientific impact):** H / M / L — drives verification depth (see VERIFICATION_PLAN.md).
- **Source:** regulatory/benchmark driver (references are benchmarks; see REGULATORY_RESEARCH.md). P11 = 21 CFR Part 11; GLP = 21 CFR Part 58; O17 = OECD GLP No. 17 (¶); O22 = OECD GLP No. 22; BX = Bouxsein 2010; SCI = scientific need.
- Each URS item is traced to FS items in FUNCTIONAL_SPEC.md and to tests in traceability_matrix.csv.

## 3. Requirements

### 3.1 General / intended use
| ID | Requirement | Pri | Crit | Source |
|---|---|---|---|---|
| URS-001 | The system shall display its intended use and RUO status in the UI and in every generated report. | M | M | §201(h) positioning |
| URS-002 | Every output (report, CSV, export) shall identify the software version (semantic version + build/commit identifier). | M | H | P11 11.10(k); O17 ¶86 |

### 3.2 Access control and identity
| ID | Requirement | Pri | Crit | Source |
|---|---|---|---|---|
| URS-010 | Each person shall use a unique, individual user account; shared/generic accounts shall not be possible for data-modifying actions. | M | H | P11 11.10(d), 11.100(a); O17 ¶95 |
| URS-011 | The system shall enforce role-based access with at least the roles admin, analyst, reviewer, viewer, each with a documented permission matrix. | M | H | P11 11.10(g); O17 ¶97 |
| URS-012 | Data of one organization (tenant) shall be inaccessible to users of another organization through any UI, API or export path. | M | H | P11 11.10(d) |
| URS-013 | Authentication shall enforce password strength, lockout after repeated failures, and session inactivity timeout. | M | H | P11 11.300 |
| URS-014 | User accounts shall be deactivated, never deleted, so that historical records remain attributable; user IDs shall never be reused. | M | H | P11 11.100(a); O17 ¶92 |
| URS-015 | The system shall support segregation of duties: the system administrator role shall not be combinable with analyst/reviewer roles within the same tenant without recorded justification; a report author shall not approve their own report. | M | H | O17 ¶27, ¶98 |
| URS-016 | Creation, change and deactivation of user accounts and role assignments shall be recorded in the audit trail. | M | H | O17 ¶92 |

### 3.3 Data ingestion and integrity
| ID | Requirement | Pri | Crit | Source |
|---|---|---|---|---|
| URS-020 | On ingestion the system shall compute and store a SHA-256 hash of every original file. | M | H | P11 11.10(a); O22 |
| URS-021 | The system shall re-verify file hashes before each analysis run and on demand, and block processing of files whose hash does not match. | M | H | P11 11.10(a) |
| URS-022 | The system shall capture acquisition/reconstruction metadata (at minimum voxel size per axis and units, scanner model, energy kVp/µA, filter, integration time, reconstruction parameters, calibration/phantom reference if any). | M | H | BX; SCI |
| URS-023 | The system shall validate voxel spacing (presence, positivity, units, plausibility range, consistency across axes and header sources) and refuse to compute physical-unit outputs when spacing is missing or ambiguous. | M | H | SCI |
| URS-024 | Original ingested data shall be immutable; no function shall overwrite or modify an original file. | M | H | P11 11.10(e); GLP 58.130(e); O17 ¶83 |
| URS-025 | Each dataset shall be linked to study, animal/specimen ID, time point and side/site; the system shall detect duplicate files (by hash) and duplicate specimen/time-point assignments. | M | H | SCI |
| URS-026 | Supported input formats and their parsing rules shall be documented; unsupported or malformed files shall be rejected with a recorded reason. | M | M | O17 ¶70 |

### 3.4 Quality control
| ID | Requirement | Pri | Crit | Source |
|---|---|---|---|---|
| URS-030 | The system shall run documented automated QC checks (e.g., intensity range/saturation, missing slices, orientation, field-of-view coverage of defect, calibration availability) on each dataset. | M | H | SCI |
| URS-031 | QC results, thresholds and QC-module version shall be recorded with each dataset. | M | M | O17 ¶86 |
| URS-032 | A failed QC check shall block downstream analysis unless an authorized user records an override with a reason; overrides shall be visible in reports. | M | H | P11 11.10(f) |

### 3.5 Region of interest
| ID | Requirement | Pri | Crit | Source |
|---|---|---|---|---|
| URS-040 | The defect ROI shall be defined by a documented method (shape, dimensions in physical units, anchor landmarks) and stored as a versioned object linked to the dataset. | M | H | BX; SCI |
| URS-041 | Any ROI creation or modification shall be audit-trailed with user, time, old/new geometry and reason. | M | H | P11 11.10(e) |
| URS-042 | The user shall be able to visually verify the ROI overlay on the image in all three orthogonal planes before analysis. | M | M | SCI |

### 3.6 Segmentation
| ID | Requirement | Pri | Crit | Source |
|---|---|---|---|---|
| URS-050 | The system shall segment the ROI into the classes background, new bone, residual graft and host bone using a fixed, declared label map stored with each model and each result. | M | H | SCI |
| URS-051 | Each segmentation result shall record the model identifier, version and SHA-256 hash of the model artifact, and the preprocessing configuration. | M | H | O17 ¶86 |
| URS-052 | Users shall be able to correct segmentations; the original automated prediction shall be retained unchanged alongside each corrected version. | M | H | GLP 58.130(e); O17 ¶83 |
| URS-053 | Each correction session shall record user, time, affected classes, voxel counts changed per class, and a reason. | M | H | P11 11.10(e) |
| URS-054 | The system shall verify at model load and at result import that the label map matches the expected schema and reject mismatches. | M | H | SCI |
| URS-055 | The system should provide a per-dataset segmentation confidence/uncertainty indicator and flag low-confidence results for review. | S | M | SCI |

### 3.7 Morphometry
| ID | Requirement | Pri | Crit | Source |
|---|---|---|---|---|
| URS-060 | The system shall compute documented morphometric outcomes using standard nomenclature and units (e.g., TV, BV, BV/TV; Tb.Th, Tb.N, Tb.Sp where applicable) and defect-specific outcomes (new-bone volume, residual-graft volume, host-bone volume, fraction of defect volume filled), each with an operational definition. | M | H | BX |
| URS-061 | Each morphometric value shall be stored with its units and the voxel size, ROI version, segmentation version and algorithm version used. | M | H | O17 ¶86 |
| URS-062 | Morphometric algorithms shall be verified against analytic/synthetic phantoms with documented tolerances. | M | H | P11 11.10(a); O17 ¶52 |
| URS-063 | Mineral density outputs (if offered) shall only be reported when a valid calibration is linked; otherwise they shall be suppressed. | M | H | SCI |

### 3.8 Statistics and blinding
| ID | Requirement | Pri | Crit | Source |
|---|---|---|---|---|
| URS-070 | The statistical analysis plan (outcomes, tests, groups, exclusion rules) shall be recorded and locked before unblinding. | M | H | GLP 58.120; ARRIVE |
| URS-071 | Statistical results shall record method, software library versions, inputs (hash of analysis table) and random seeds. | M | H | O17 ¶86 |
| URS-072 | All specimens shall appear in analysis outputs; any exclusion shall require a recorded reason and be listed in the report. | M | H | 2016 GLP NPRM 58.180(c) (proposed); ARRIVE |
| URS-075 | Group/treatment allocation shall be hidden from analysts and reviewers performing ROI/segmentation work until an authorized unblinding event. | M | H | SCI; ARRIVE |
| URS-076 | Unblinding shall be an explicit, authorized, audit-trailed event per study; post-unblinding edits to ROI/segmentation shall be flagged in reports. | M | H | SCI |

### 3.9 Reporting
| ID | Requirement | Pri | Crit | Source |
|---|---|---|---|---|
| URS-080 | Reports (PDF and CSV) shall include provenance: input file hashes, software version, model hash, configuration snapshot ID, ROI/segmentation versions, users, UTC timestamps, QC status and overrides. | M | H | P11 11.10(b); GLP 58.185 |
| URS-081 | All records shall be exportable in human-readable and machine-readable form (PDF, CSV, JSON; label maps in an open image format). | M | H | P11 11.10(b); O17 ¶79, ¶113 |
| URS-082 | Reports shall be regenerable from stored inputs and configuration with identical numeric results (or within documented tolerance). | M | H | O17 ¶86 |
| URS-083 | CSV exports shall be locale-independent (dot decimal, UTF-8), state units in headers and preserve full numeric precision. | M | M | SCI |

### 3.10 Review and electronic sign-off
| ID | Requirement | Pri | Crit | Source |
|---|---|---|---|---|
| URS-090 | The system shall implement a review workflow (draft → in review → approved / rejected) enforcing permitted state transitions. | M | H | P11 11.10(f) |
| URS-091 | Sign-off shall display the signer's printed name, date/time (UTC) and meaning (e.g., authored, reviewed, approved) on screen and in the report. | M | H | P11 11.50; O17 ¶102 |
| URS-092 | Signing shall require re-entry of the user's password (or equivalent re-authentication) at the time of signing. | M | H | P11 11.200; O17 ¶105 |
| URS-093 | The signature shall be cryptographically linked to the hash of the signed record; any later change shall invalidate the signature and require re-review. | M | H | P11 11.70; O17 ¶106 |

### 3.11 Audit trail
| ID | Requirement | Pri | Crit | Source |
|---|---|---|---|---|
| URS-100 | The system shall maintain a secure, computer-generated, time-stamped, append-only audit trail of creation, modification, deletion and signing of all data-relevant records, and of security events. | M | H | P11 11.10(e); O17 ¶80 |
| URS-101 | Audit entries shall capture user, UTC timestamp, action, object, old and new values (or hashes), and reason for change where applicable. | M | H | GLP 58.130(e); O17 ¶80 |
| URS-102 | Audit entries shall be hash-chained; the system shall provide a verification function that detects insertion, deletion, reordering or modification of entries. | M | H | P11 11.10(a)/(e) |
| URS-103 | No user role, including admin, shall be able to disable, edit or delete audit trail entries through the application. | M | H | O17 ¶81 |
| URS-104 | The audit trail shall be reviewable and exportable in human-readable form, filterable by study, user, object and date. | M | H | P11 11.10(e); O17 ¶82 |
| URS-105 | Audit trail records shall be retained at least as long as the records they describe. | M | H | P11 11.10(e) |
| URS-106 | Timestamps shall come from a synchronized server time source, stored in UTC. | M | H | P11 11.10(e) |

### 3.12 Configuration and version control
| ID | Requirement | Pri | Crit | Source |
|---|---|---|---|---|
| URS-110 | Each analysis run shall store an immutable configuration snapshot (all parameters affecting results) with a content hash. | M | H | O17 ¶86 |
| URS-111 | Model artifacts shall be version-locked and identified by SHA-256; the system shall refuse to run a model whose hash does not match the release manifest. | M | H | O17 ¶95 |
| URS-112 | Only released (approved) model versions shall be selectable for production analyses; experimental models shall be clearly segregated and labelled. | M | H | O17 ¶95 |
| URS-113 | Re-running an analysis with identical inputs, configuration, software and model versions shall reproduce results (bitwise or within a documented tolerance). | M | H | SCI |

### 3.13 Data management
| ID | Requirement | Pri | Crit | Source |
|---|---|---|---|---|
| URS-120 | The system shall support scheduled backups of database, original files, derived data, models and audit trail. | M | H | O17 ¶73 |
| URS-121 | Restore shall be verifiable: restored data shall be checked against stored hashes and the audit-chain verification. | M | H | O17 ¶74 |
| URS-122 | Retention periods shall be configurable per tenant/study; records shall not be deletable before expiry. | M | H | P11 11.10(c); GLP 58.195 |
| URS-123 | Deletion after retention expiry shall require authorized approval, shall be audit-trailed, and shall be blocked under legal hold. | M | H | O17 ¶118 |
| URS-124 | A complete study archive package (originals, derived data, configuration, audit trail, reports, manifest with hashes) shall be exportable in open formats. | M | H | O17 ¶113–114 |

### 3.14 Security and operations
| ID | Requirement | Pri | Crit | Source |
|---|---|---|---|---|
| URS-130 | Data in transit shall be encrypted (TLS); data at rest should be encrypted where the deployment supports it. | M | H | O17 ¶91 |
| URS-131 | Third-party dependencies shall be pinned and monitored for known vulnerabilities. | M | M | O17 ¶95 |
| URS-132 | Security-relevant events (logins, failed logins, permission changes, exports) shall be logged. | M | M | O17 ¶93 |

### 3.15 Documentation
| ID | Requirement | Pri | Crit | Source |
|---|---|---|---|---|
| URS-140 | User documentation shall describe each function, its limitations and the meaning of each output. | M | M | P11 11.10(k) |
| URS-141 | Each release shall have release notes listing changes, known issues and the verification evidence reference. | M | M | O17 ¶84 |

## 4. Open questions
1. Supported scanner/vendor formats (DICOM, vendor TIFF stacks, NIfTI) — Scientific Lead.
2. Numeric tolerance definitions for URS-113 on GPU inference — Engineering.
3. Defect-specific metric definitions and minimum reporting set — Scientific Lead (to align with BX and ASTM F2721).
