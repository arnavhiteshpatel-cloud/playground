# OsteoQuant — Installation Qualification (IQ) Protocol

> **Revision pending (2026-11-27, cycle-1 review QA-REG-02).** This draft describes the Generation-1 architecture (FastAPI server + browser workbench). The Generation-2 product is an offline desktop application (PySide6/VTK, in-process analysis library; the API is an optional integration interface). Requirements and protocols must be re-baselined to the desktop product before any qualification activity. Draft only; no compliance is claimed.


| Field | Value |
|---|---|
| Document ID | OQ-QMS-IQ-001 |
| Version | 0.1 (DRAFT) |
| Date | 2026-11-27 |
| Applies to | One named OsteoQuant installation (server/instance) per execution |
| Related | URS-001…141, FS, OQ_PROTOCOL.md, SOP-006, SOP-007, SOP-008 |

> **Status: DRAFT — not validated; not a claim of Part 11 compliance or GLP validation.**
> This protocol is a template. Executing it documents that an instance was installed as specified; it does not by itself validate the system for any regulated use.

## 1. Objective
Provide documented evidence that the OsteoQuant software, its dependencies, model artifacts, configuration and supporting infrastructure are installed as specified and are traceable to an approved release.

## 2. Scope
Server-side components (FastAPI application, worker, SQLite database, file store, model registry), reverse proxy/TLS, time synchronization, backup target. Client browsers are out of scope except the supported-browser check (IQ-12).

## 3. Responsibilities
| Role | Responsibility |
|---|---|
| Installer (IT/engineering) | Executes steps, records results |
| Engineering Lead | Approves protocol, reviews deviations |
| Quality (independent of installer) | Reviews executed protocol and approves summary |

## 4. Prerequisites
- Approved release package with `RELEASE_MANIFEST.json` (software artifact hash, dependency lock hash, model artifact hashes, default config hash, DB schema version).
- Approved change record (CHANGE_CONTROL.md) authorizing the installation.
- Installer has a named account on the host; no shared OS accounts.

## 5. Test execution rules (Good Documentation Practice)
Record actual results contemporaneously; attach evidence (screenshots, command output with hashes); no blank fields (use "N/A" with justification); corrections by single line-through with initials, date and reason (paper) or audited edit (electronic); deviations recorded in §8.

## 6. Environment record
| Item | Expected | Actual | Evidence ref |
|---|---|---|---|
| Host name / instance ID | | | |
| OS and version | Supported list in release notes | | |
| CPU / RAM / disk free | ≥ minimums in release notes | | |
| GPU model / driver / CUDA (if used) | Supported list | | |
| Python version | As pinned in release | | |
| Filesystem for data store; volume encryption enabled (Y/N) | Y (recommended) | | |
| Network: TLS certificate subject / expiry | Valid, not expiring < 30 days | | |

## 7. Test steps
| Step | Description | Acceptance criterion | Trace | Result (P/F) | Evidence |
|---|---|---|---|---|---|
| IQ-01 | Compute SHA-256 of installed application package/wheel and compare with release manifest | Exact match | URS-002, URS-111 | | |
| IQ-02 | Install dependencies with hash-checking mode from lock file; record `pip freeze`; run vulnerability audit | Install succeeds only with hash match; no unresolved critical CVEs, or documented risk acceptance | URS-131, FS-131-1 | | |
| IQ-03 | Verify each model artifact SHA-256 against model registry manifest; verify label map equals canonical map | All match; label map {0:background,1:new_bone,2:residual_graft,3:host_bone} | URS-111, URS-054 | | |
| IQ-04 | Export effective default configuration; compare hash to release manifest; record site-specific overrides via change record | Hash match or overrides documented | URS-110 | | |
| IQ-05 | Initialise DB; verify schema version; `PRAGMA integrity_check` = ok; WAL mode enabled; audit_log UPDATE/DELETE triggers present | All true | FS-100-1, RSK-32 | | |
| IQ-06 | Verify NTP synchronization; system timezone; application reports UTC | Offset < 1 s; app timestamps UTC | URS-106 | | |
| IQ-07 | Verify HTTPS only: HTTP redirects; HSTS header present; TLS ≥ 1.2 | All true | URS-130 | | |
| IQ-08 | Verify OS permissions: data store and DB writable only by service account; study-role users have no OS access | Permissions match spec | URS-024, URS-103, RSK-20 | | |
| IQ-09 | Verify backup target reachable and writable by backup service only; first backup job completes with manifest | Success, manifest hashes present | URS-120 | | |
| IQ-10 | Verify audit trail genesis entry exists per tenant and chain verification returns VALID | VALID | URS-102 | | |
| IQ-11 | Create initial named admin; confirm bootstrap credential disabled; attempt login with bootstrap credential | Login fails; admin creation audited | URS-010, FS-010-2 | | |
| IQ-12 | Open UI in each supported browser; RUO/not-validated banner visible; `/api/version` matches manifest | Matches | URS-001, URS-002 | | |
| IQ-13 | Confirm documentation set installed/available (user manual, SOPs, release notes) at stated versions | Available, versions match | URS-140, URS-141 | | |

## 8. Deviations
| Dev ID | Step | Description | Impact assessment | Resolution / CAPA | Approved by / date |
|---|---|---|---|---|---|

## 9. Acceptance
IQ passes when all steps pass, or every failure has an approved deviation with documented no-impact rationale. OQ may not start until IQ is approved.

## 10. Approval of executed IQ
| Role | Name | Signature | Date |
|---|---|---|---|
| Executed by | | | |
| Reviewed by (Engineering) | | | |
| Approved by (Quality) | | | |
