# SOP-002: Analysis Run (ROI, Segmentation, Morphometry, Measurement Support, Statistics)

| Field | Value |
|---|---|
| SOP ID / version | SOP-002 / 0.2 (DRAFT) |
| Effective date | Not effective (draft) |
| Owner | Scientific Lead |
| Related requirements | URS-040…042, URS-050…051, URS-060…063, URS-070…072, URS-110…114, URS-150…153, URS-160; RSK-06, RSK-10, RSK-14, RSK-16, RSK-27, RSK-37 |

> **Status: DRAFT. Not approved or effective. No claim of 21 CFR Part 11 compliance, GLP compliance or validation.**

## 1. Purpose
Run analyses consistently so that each result is traceable to inputs, ROI, segmentation method or model, configuration, measurement-support decision and software version.

## 2. Prerequisites
- Scans imported and QC-reviewed per SOP-001 with explicit, confirmed spacing.
- The study analysis protocol defines: defect model and nominal diameter, ROI method, segmentation method or locked model (with its SHA-256), graft material(s) as named in the advisor, endpoint set, and the Statistical Analysis Plan (SAP).
- The analyst works blinded (SOP-009).

## 3. Procedure
1. **Confirm versions:** *Help > About*: record the software version and licence state. Reports from evaluation or test licences carry a watermark and must not be used for study decisions.
2. **SAP:** before any group-level output is viewed, the SAP (outcomes, groups, tests, alpha, multiplicity, exclusion criteria) is signed and dated **on paper or in the controlled document system**. The software has no SAP lock (FS-070-1 not implemented). Amendments after signature need a reason and Scientific Lead approval and are reported.
3. **Analyse:** select scans in the Project panel, **Analyse...** Enter the defect model and nominal diameter from the protocol, the segmentation method/model from the protocol, and the **graft material** exactly as the protocol states (*Unspecified* if not known; *No graft* only for empty-defect controls). The material drives the measurement-support decision; never choose a material to obtain a "supported" result.
4. **ROI:** if a scan is marked *needs ROI*, place the crosshair at the defect centre, *Study > Define cylindrical ROI at crosshair*, enter radius and extent from the protocol and a specific reason, then analyse again with *Use the latest saved ROI*. For every scan, check the ROI in all three planes and the 3D view, including side and orientation. Record "ROI checked" with date and initials in the analysis log (the software has no "ROI verified" action, FS-042-2).
5. **Jobs:** monitor the Jobs panel. A failed or cancelled job leaves no new segmentation; re-run after fixing the cause and record it.
6. **Segmentation review:** per SOP-003 before results are accepted.
7. **Measurement support:** in the Results tab read the Support column. Endpoints shown as *not measured* are not reported by any other means (no manual threshold work-arounds). Conditional (orange) endpoints are reported only with their conditions. Record the advisor version shown in the report.
8. **Exclusions:** apply only pre-specified exclusion criteria, each with a reason in the analysis log (the software has no exclusion workflow, FS-072-2). Never delete scans or specimens.
9. **Statistics:** only after all scans are reviewed and the SAP is signed; unblinding per SOP-009.
10. **Re-runs:** earlier segmentation versions and measurements are retained automatically. Record the reason for every re-run in the analysis log.
11. **Report draft:** *Reports* tab, **Generate DefectFill report**; check the provenance and measurement-support sections; submit for review (SOP-004).

## 4. Consistency rules
One software version, one segmentation method/model version and one advisor version per study unless a justified change is approved (CHANGE_CONTROL §4). Configuration choices that differ from the protocol are recorded with a reason (the software does not yet link a configuration snapshot to each measurement, FS-110-1).

## 5. Records
Segmentation versions, measurements, jobs and audit trail (automatic); signed SAP and amendments; analysis log (ROI checks, exclusions, re-runs, deviations).

## 6. Revision history
| Version | Date | Change | Author |
|---|---|---|---|
| 0.1 | 2026-11-27 | Initial draft (web workbench) | QA/RA |
| 0.2 | 2026-11-27 | Desktop analysis, jobs, measurement support; procedural SAP, ROI check and exclusions until implemented | QA/RA |
