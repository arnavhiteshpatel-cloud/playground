# SOP-002 — Analysis Run (ROI, Segmentation, Morphometry, Statistics)

| Field | Value |
|---|---|
| SOP ID / version | SOP-002 / 0.1 (DRAFT) |
| Effective date | Not effective (draft) |
| Owner | Scientific Lead |
| Related requirements | URS-040…042, URS-050…051, URS-060…063, URS-070…072, URS-110…113; RSK-06, RSK-10, RSK-14, RSK-16, RSK-27 |

> **Status: DRAFT — not validated; not a claim of Part 11 compliance or GLP validation.**

## 1. Purpose
Define a consistent, reproducible procedure for running analyses so that each result is traceable to inputs, ROI, model, configuration and software version.

## 2. Prerequisites
- Datasets ingested and QC-reviewed per SOP-001; voxel spacing VERIFIED.
- Study analysis protocol defines: ROI method and parameters, released model version, metric set, and Statistical Analysis Plan (SAP).
- Analyst is blinded (SOP-009).

## 3. Procedure
1. **Confirm versions:** record (or confirm on the run screen) software version and the RELEASED model version specified in the study protocol. Do not use EXPERIMENTAL models for study results.
2. **SAP:** before any group-level output is viewed, enter the SAP (outcomes, groups, tests, alpha, multiplicity, exclusion criteria) and **lock** it. Amendments after lock require a reason and Scientific Lead approval, and are reported.
3. **ROI:** define the ROI per protocol in physical units; check the overlay in all three planes; confirm orientation markers and side; click "ROI verified". Edits require a reason.
4. **Segmentation:** run with the protocol model. Review per SOP-003 before morphometry is accepted.
5. **Morphometry:** run the protocol metric set. Density metrics only with linked calibration.
6. **Exclusions:** apply only pre-specified exclusion criteria, each with a reason; never delete specimens.
7. **Statistics:** run only after all datasets have status "segmentation reviewed" and the SAP is locked; unblinding per SOP-009.
8. **Re-runs:** if a run must be repeated (e.g., after a correction), do not discard prior runs; the system retains them. Record the reason.
9. **Report draft:** generate a draft report; check provenance section completeness; submit for review (SOP-004).

## 4. Consistency rules
One software version and one model version per study unless a justified change is approved (CHANGE_CONTROL §4). Configuration overrides must be recorded with reason and are captured in the run snapshot.

## 5. Records
Run records and configuration snapshots (automatic); SAP and amendments; analysis notes for any deviation.

## 6. Revision history
| Version | Date | Change | Author |
|---|---|---|---|
| 0.1 | 2026-11-27 | Initial draft | QA/RA |
