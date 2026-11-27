# OsteoQuant — Change Control Procedure

| Field | Value |
|---|---|
| Document ID | OQ-QMS-CC-001 |
| Version | 0.1 (DRAFT) |
| Date | 2026-11-27 |
| Owner | Quality (TBD) |
| Benchmarks | 21 CFR 11.10(k)(2); OECD GLP No. 17 ¶44–45, ¶84–88 |

> **Status: DRAFT — not validated; not a claim of Part 11 compliance or GLP validation.**

## 1. Purpose and scope
Ensure that changes to OsteoQuant software, ML models, configuration defaults, infrastructure, dependencies, controlled documents (URS/FS/SOPs) and qualified installations are assessed, approved, verified and traceable, so that results remain reproducible and the (future) validated state is maintained.

## 2. Change classes
| Class | Definition | Examples | Approval |
|---|---|---|---|
| **Major** | May affect scientific results, data integrity, security, or regulatory-relevant controls | Segmentation model change; morphometry algorithm; voxel-spacing logic; audit trail; auth/RBAC; DB schema migration; numerics-affecting dependency upgrade | Engineering Lead + Scientific Lead + Quality |
| **Minor** | No impact on results or controls; verified by regression | UI text, layout, logging verbosity, non-numerical dependency patch | Engineering Lead + one reviewer; Quality notified |
| **Emergency** | Urgent fix (security, data loss) | CVE patch, crash fix | Engineering Lead (verbal/recorded) → retrospective full review within 5 working days |
| **Documentation** | Controlled document revision | SOP update | Document owner + Quality |

## 3. Procedure
1. **Request** — Change Request (CR) record: CR-YYYY-NNN, requester, description, reason, affected items (URS/FS/modules/models/SOPs), proposed class.
2. **Impact assessment** — Engineering + Scientific Lead complete:
   - Affected URS/FS and risks (RISK_ASSESSMENT.md); new risks?
   - Effect on results: will any metric change for existing data? (Run golden regression in a branch and attach diff.)
   - Data migration needed? (OECD 17 ¶66–69: preserve content, meaning, audit trail and signature links.)
   - Re-verification scope (tests), re-qualification (IQ/OQ/PQ) scope.
   - User communication / training / SOP updates.
   - Effect on in-progress studies (should ongoing studies stay on the prior version? — default **yes**, version-pinned).
3. **Approval** — per class, before implementation in the release branch. Approvers must not be the sole implementer for Major changes.
4. **Implementation** — on a branch referencing CR ID; code review mandatory; commits reference CR ID.
5. **Verification** — tests per VERIFICATION_PLAN; golden regression; for model changes, SOP-007.
6. **Release** — SemVer bump (MAJOR for result-affecting or incompatible changes; MINOR for features; PATCH for fixes), release manifest with hashes, release notes listing CRs.
7. **Deployment** — via approved CR to each installation; IQ steps re-executed as defined by impact assessment; OQ subset as defined.
8. **Closure** — Quality verifies evidence complete; CR closed; traceability matrix updated.

## 4. Special rules
- **ML models:** any retraining, fine-tuning, threshold change, or preprocessing change = new model version = Major (see SOP-007). Silent model replacement is prohibited; loader enforces hash (FS-111-1).
- **Configuration defaults:** changes to defaults affecting computation = Major; site-specific overrides recorded per installation via CR and captured in run snapshots.
- **Dependencies:** lock-file changes run golden regression; any metric change → Major.
- **Infrastructure:** OS patches and antivirus updates fall under change/configuration management (OECD 17 ¶88) — may be pre-approved as a "standard change" category with periodic review.
- **Rollback:** each Major release documents rollback steps and data compatibility; rollback itself is a CR (Emergency allowed).
- **Studies in progress:** a study's analyses should use one software/model version; mid-study changes require Scientific Lead justification recorded in the study file.

## 5. Records
CR record, impact assessment, approvals (signed/e-signed), test evidence, release manifest, deployment record, closure. Retained per DATA_RETENTION_POLICY.md (at least as long as any study analysed with the affected version — OECD 17 ¶117).

## 6. CR template
```
CR ID: CR-____-___        Class: Major / Minor / Emergency / Documentation
Requester / date:
Description and reason:
Affected: URS __ FS __ Modules __ Models __ SOPs __ Installations __
Risk impact (RSK IDs; new risks):
Result impact (golden regression diff attached? Y/N; summary):
Data migration: Y/N (plan ref)
Verification scope:            Re-qualification scope (IQ/OQ/PQ):
Training / SOP updates:
In-progress studies impact:
Approvals: Engineering ____ Scientific ____ Quality ____ (date)
Implementation refs (commits/PR):   Release version:
Closure (Quality) / date:
```
