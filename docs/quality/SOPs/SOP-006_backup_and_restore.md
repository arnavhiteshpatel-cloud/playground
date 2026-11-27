# SOP-006: Backup and Restore of Project Folders (OsteoQuant Desktop)

| Field | Value |
|---|---|
| SOP ID / version | SOP-006 / 0.2 (DRAFT) |
| Effective date | Not effective (draft) |
| Owner | User organisation IT, with Engineering |
| Related requirements | URS-120, URS-121, URS-124, URS-125; FS-120-1, FS-121-1, FS-125-1; RSK-30, RSK-32, RSK-33 |
| Benchmarks | 21 CFR 11.10(c); OECD GLP No. 17 ¶73–75, ¶119–122 |

> **Status: DRAFT. Not approved or effective. No claim of 21 CFR Part 11 compliance, GLP compliance or validation.**

## 1. Purpose
Protect OsteoQuant Desktop projects against loss and ensure they can be restored completely and verifiably. The desktop has no built-in backup function (FS-120-1); backup is by copying the whole project folder.

## 2. Backup scope
The entire project folder: `osteoquant-project.json`, `osteoquant.db` (with any `osteoquant.db-wal` / `-shm` files), and the `data/` directory (scan Zarr stores, label revisions, ROI masks, reports). Also: the installer of each OsteoQuant version used for the project, model artifacts used, `models/validation_records.json`, the licence file, and the anchor log (SOP-005).

## 3. Schedule and retention (proposed defaults)
| Backup | Frequency | Retention |
|---|---|---|
| Project folder copy | Daily while the project is active | 35 days |
| Full copy | Weekly | 13 weeks |
| Monthly full copy | Monthly | 7 years or per DATA_RETENTION_POLICY, whichever is longer |
At least one copy off the workstation and in a different failure domain; copies encrypted; access limited to the backup account and named IT staff.

## 4. Procedure: backup
1. **Close the project in every OsteoQuant instance** (*File > Close project*) so that the SQLite write-ahead log is checkpointed. Copying an open project can produce an inconsistent copy.
2. Run *Verify chain* (SOP-005) and record the anchor.
3. Copy the whole folder with a tool that preserves file contents; generate a SHA-256 manifest of all files in the copy and store it with the copy.
4. Record date, project, manifest hash, anchor and operator in the backup log. Failures are reported to IT the same day.

## 5. Procedure: restore test (quarterly and after major changes)
1. Raise a CR (standard change).
2. Restore the latest copy to an isolated location on a qualified workstation.
3. Verify all files against the manifest.
4. Open the restored project; *Verify chain*; confirm the anchor from the backup log is present.
5. Regenerate one report and compare the numeric values with the archived report.
6. Record duration (vs recovery time objective) and outcome; delete the test copy per procedure.

## 6. Procedure: production restore
Only under an approved (emergency allowed) CR. Record the point in time restored; identify work done after it (may be lost) and inform the study leads; perform §5 steps 3–4 before users resume; record the restore in the study file. (The restore itself is not an event in the restored audit trail.)

## 7. Records
Backup log, manifests, restore-test reports, CRs.

## 8. Revision history
| Version | Date | Change | Author |
|---|---|---|---|
| 0.1 | 2026-11-27 | Initial draft (server database, file store, backup job) | QA/RA |
| 0.2 | 2026-11-27 | Desktop project-folder backup; close-before-copy rule; manual manifest and anchor | QA/RA |
