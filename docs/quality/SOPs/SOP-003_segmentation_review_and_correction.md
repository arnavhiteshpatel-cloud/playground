# SOP-003: Segmentation Review and Correction (OsteoQuant Desktop)

| Field | Value |
|---|---|
| SOP ID / version | SOP-003 / 0.2 (DRAFT) |
| Effective date | Not effective (draft) |
| Owner | Scientific Lead |
| Related requirements | URS-052…056, URS-075/076, URS-151; FS-052-1, FS-053-1, FS-055-1, FS-056-1/2, FS-075-3; RSK-08, RSK-09, RSK-12, RSK-13, RSK-35, RSK-47 |

> **Status: DRAFT. Not approved or effective. No claim of 21 CFR Part 11 compliance, GLP compliance or validation.**

## 1. Purpose
Review and correct automated 3-class segmentations (new bone / residual graft / host bone) consistently, blinded, and with full traceability, while preserving every earlier version.

## 2. Responsibilities
- **Analyst (blinded):** reviews and corrects.
- **Second reviewer (blinded):** reviews a sample and all flagged cases.
- **Scientific Lead:** maintains the visual class-definition guide (reference images per graft material) and resolves disagreements.

## 3. Class definitions
Use the approved visual guide (document ref TBD) for the graft material and species of the study, including typical attenuation and morphology and known confounders (graft particles with ingrowth, defect margins, periosteal callus outside the ROI). If the advisor reports the graft/new-bone split as *not supported*, corrections cannot make those endpoints reportable; correct only what the reported endpoints depend on and notify the Scientific Lead.

## 4. Procedure
1. Switch on **Blinded review mode** (Review panel or *View* menu) before opening scans.
2. Open the scan (double-click in the Project panel). In the Display panel, confirm the legend shows the canonical classes (new bone, residual graft, host bone; uncertain voxels shown separately). Any mismatch: stop and report as an incident.
3. Review every scan in all three planes through the full ROI, and in the 3D panel; pay attention to graft/new-bone interfaces, defect margins and uncertain voxels.
4. **Mandatory review:** 100 % of scans whose Support status is *flagged* or *not supported*, or whose uncertain fraction is high; plus a second-reviewer sample of ≥ 20 % (minimum 3) of the remaining scans per study, selected by a documented random procedure.
5. **Correction:** use the Segmentation panel tools with **Protect other classes** on. Brush radius is in µm. Correct only clear misclassifications according to the guide; never adjust towards expected values. Use Undo/Redo freely: nothing is stored until the revision is saved.
6. **Save:** *Save as new revision...* (Ctrl+S) with a specific reason (e.g. "graft granules at proximal margin labelled as new bone"). A new *corrected* version is stored; the earlier version stays unchanged; user, reason, per-class voxel changes and tools are written to the audit trail; endpoints are recomputed with the same ROI and the same measurement-support decision.
7. **Disagreements** between analyst and second reviewer: Scientific Lead adjudicates; record the decision in the review log.
8. **Large corrections:** if a class volume changes by > 20 % (proposed threshold, shown as the per-class change before saving), add a note and notify the Scientific Lead (possible model domain shift; input to SOP-007 monitoring).
9. Record the scan as "segmentation reviewed" in the review log; the reviewer then signs the version under SOP-004.
10. **After unblinding:** corrections are discouraged. The software does not yet flag post-unblinding edits (FS-076-1); any such correction is listed manually in the report with its justification.

## 5. Records
All segmentation versions, reasons and voxel deltas (automatic); review log (sample selection, second review, adjudication, "segmentation reviewed", post-unblinding edits).

## 6. Revision history
| Version | Date | Change | Author |
|---|---|---|---|
| 0.1 | 2026-11-27 | Initial draft | QA/RA |
| 0.2 | 2026-11-27 | Desktop tools, blinded review mode, measurement support; manual post-unblinding list until implemented | QA/RA |
