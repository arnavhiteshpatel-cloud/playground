# SOP-009 — Blinding

| Field | Value |
|---|---|
| SOP ID / version | SOP-009 / 0.1 (DRAFT) |
| Effective date | Not effective (draft) |
| Owner | Scientific Lead |
| Related requirements | URS-070, URS-075, URS-076; FS-070-2, FS-075-1, FS-075-2, FS-076-1; RSK-12, RSK-16 |
| Benchmarks | ARRIVE 2.0 (blinding) [PK] |

> **Status: DRAFT — not validated; not a claim of Part 11 compliance or GLP validation.**

## 1. Purpose
Prevent knowledge of treatment allocation from influencing ROI placement, segmentation correction, exclusions or analysis choices.

## 2. Roles
- **Allocation custodian:** person not performing image analysis; holds the allocation key; enters it in OsteoQuant's restricted allocation table (or keeps it offline until unblinding).
- **Analysts/reviewers performing image work:** blinded.
- **Unblinding authoriser:** study lead or delegate with `study:unblind` permission.

## 3. Procedure
1. **Coding:** custodian assigns random specimen codes; specimen manifest given to analysts contains codes only. File names, folder names and scanner metadata fields must not contain group/treatment information (check at intake, SOP-001).
2. **Allocation entry:** custodian enters allocation into the restricted table; analysts have no `allocation:read` permission.
3. **Analysis phase:** analysts complete ROI, segmentation review (SOP-003), exclusions per pre-specified criteria, and lock the SAP (SOP-002).
4. **Unblinding:** only after all datasets are "segmentation reviewed" and the SAP is locked. Authoriser performs unblinding in the system (password re-entry + reason). The event and time are recorded and printed in the report.
5. **After unblinding:** edits to ROI/segmentation/exclusions are strongly discouraged; any such edit is automatically flagged and must be justified in the report and reviewed under SOP-005.
6. **Accidental unblinding:** report immediately to the study lead; record who, what, when; assess impact; document in the study file and report.
7. **Situations where blinding is impossible** (e.g., graft visibly distinguishes groups): document the limitation in the protocol and report; consider blinding to time point or using independent analysts.

## 4. Records
Allocation key and custody log, unblinding event (automatic), accidental-unblinding reports.

## 5. Revision history
| Version | Date | Change | Author |
|---|---|---|---|
| 0.1 | 2026-11-27 | Initial draft | QA/RA |
