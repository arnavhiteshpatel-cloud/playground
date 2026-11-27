# SOP-009: Blinding (OsteoQuant Desktop)

| Field | Value |
|---|---|
| SOP ID / version | SOP-009 / 0.2 (DRAFT) |
| Effective date | Not effective (draft) |
| Owner | Scientific Lead |
| Related requirements | URS-070, URS-075, URS-076; FS-070-2, FS-075-1…FS-075-4, FS-076-1; RSK-12, RSK-16 |
| Benchmarks | ARRIVE 2.0 (blinding) [PK] |

> **Status: DRAFT. Not approved or effective. No claim of 21 CFR Part 11 compliance, GLP compliance or validation.**

## 1. Purpose
Prevent knowledge of treatment allocation from influencing ROI placement, segmentation correction, exclusions or analysis choices.

## 2. Software support and its limits
- Studies created as **blinded** (*Study > New study*) show group codes instead of names to users without the `unblind` permission (analyst, reviewer, viewer). Administrators always see names.
- **Blinded review mode** hides group names, animal IDs and file names for every role, including administrators.
- Reports generated with allocation visible cannot be exported by users without `unblind`.
- **Not in the desktop:** an unblinding action (FS-075-2), a SAP lock (FS-070-1) and flagging of post-unblinding edits (FS-076-1). These steps are procedural below.

## 3. Roles
- **Allocation custodian:** does not perform image analysis; holds the allocation key.
- **Analysts and reviewers performing image work:** blinded; never hold the admin role in the study project.
- **Unblinding authoriser:** study lead or delegate.

## 4. Procedure
1. **Coding:** the custodian assigns random specimen codes; the manifest given to analysts contains codes only. File names, folder names and scanner metadata must not contain group or treatment information (checked at intake, SOP-001).
2. **Project set-up:** create the study as *blinded*. Either keep group allocation **out of the project** until unblinding (preferred; the key stays with the custodian), or have the custodian enter groups under *Study > Add group* with an admin account that no analyst uses.
3. **Analysis phase:** analysts and reviewers work with *Blinded review mode* switched on; complete ROI checks, segmentation review (SOP-003), exclusions per pre-specified criteria; the SAP is signed (SOP-002 step 2).
4. **Unblinding:** only after all scans are "segmentation reviewed" and the SAP is signed. The authoriser records the date, time, reason and their signature in the study file; the custodian then enters or reveals the allocation. Record the unblinding time in the report.
5. **After unblinding:** edits to ROI, segmentation or exclusions are strongly discouraged; any such edit is listed in the report with its justification (manual list) and reviewed under SOP-005 by comparing audit timestamps with the recorded unblinding time.
6. **Accidental unblinding:** report immediately to the study lead; record who, what and when; assess impact; document in the study file and report.
7. **When blinding is impossible** (e.g. the graft visibly distinguishes groups): document the limitation in the protocol and report; consider blinding to time point or independent analysts.

## 5. Records
Allocation key and custody log, unblinding record, manual post-unblinding edit list, accidental-unblinding reports; `ui.blinded_mode` and other audit entries (automatic).

## 6. Revision history
| Version | Date | Change | Author |
|---|---|---|---|
| 0.1 | 2026-11-27 | Initial draft | QA/RA |
| 0.2 | 2026-11-27 | Desktop blinded studies and blinded review mode; procedural unblinding and post-unblinding list until implemented | QA/RA |
