# SOP-006 — Backup and Restore

| Field | Value |
|---|---|
| SOP ID / version | SOP-006 / 0.1 (DRAFT) |
| Effective date | Not effective (draft) |
| Owner | Engineering / IT |
| Related requirements | URS-120, URS-121, URS-124; FS-120-1, FS-121-1, FS-102-2; RSK-30, RSK-33 |
| Benchmarks | 21 CFR 11.10(c); OECD GLP No. 17 ¶73–75, ¶119–122 |

> **Status: DRAFT — not validated; not a claim of Part 11 compliance or GLP validation.**

## 1. Purpose
Protect OsteoQuant records against loss and ensure they can be restored completely and verifiably.

## 2. Backup scope
SQLite database (online backup API snapshot), file store (originals and derived data), model registry and artifacts, configuration, audit-chain head export, application release package for each version in use.

## 3. Schedule and retention (proposed defaults)
| Backup | Frequency | Retention |
|---|---|---|
| Incremental file store + DB snapshot | Daily | 35 days |
| Full | Weekly | 13 weeks |
| Monthly full | Monthly | 7 years or per DATA_RETENTION_POLICY, whichever is longer |
At least one copy off-site / different failure domain; backups encrypted; access limited to backup service account and named IT staff (not study personnel).

## 4. Procedure — backup monitoring
1. Automated job writes a backup manifest (file list with SHA-256, DB snapshot hash, chain head).
2. Job result is audited; failure triggers alert to IT.
3. IT reviews job status at least weekly and records it.

## 5. Procedure — restore test (quarterly, and after major changes)
1. Raise a CR (standard change) for the test.
2. Restore the latest full + incrementals to an isolated test instance.
3. Run restore verification tool: all file hashes match manifest; `PRAGMA integrity_check` = ok; audit-chain verification VALID and chain head matches anchored value.
4. Regenerate one sample report per tenant (or synthetic tenant) and compare to archived report hash/values.
5. Record duration (vs. recovery time objective) and outcome; destroy test instance per procedure.

## 6. Procedure — production restore
Only under an approved (Emergency allowed) CR. Record point-in-time restored to; identify any data created after that point (may be lost) and inform affected study leads; perform §5 verification steps on production before re-opening to users; audit entry documents the restore event.

## 7. Records
Backup manifests, job logs, restore test reports, CRs.

## 8. Revision history
| Version | Date | Change | Author |
|---|---|---|---|
| 0.1 | 2026-11-27 | Initial draft | QA/RA |
