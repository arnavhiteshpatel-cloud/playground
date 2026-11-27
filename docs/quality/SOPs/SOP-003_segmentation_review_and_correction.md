# SOP-003 — Segmentation Review and Correction

| Field | Value |
|---|---|
| SOP ID / version | SOP-003 / 0.1 (DRAFT) |
| Effective date | Not effective (draft) |
| Owner | Scientific Lead |
| Related requirements | URS-052…055, URS-075/076; FS-052-1, FS-053-1, FS-055-1, FS-076-1; RSK-08, RSK-09, RSK-12, RSK-13, RSK-35 |

> **Status: DRAFT — not validated; not a claim of Part 11 compliance or GLP validation.**

## 1. Purpose
Ensure automated 3-class segmentations (new bone / residual graft / host bone) are reviewed and corrected consistently, blinded, and with full traceability, while preserving the original prediction.

## 2. Responsibilities
- **Analyst (blinded):** reviews and corrects.
- **Second reviewer (blinded):** reviews a sample and all flagged cases.
- **Scientific Lead:** maintains the visual class-definition guide (reference images per graft material) and resolves disagreements.

## 3. Class definitions
Use the approved visual guide (document ref TBD) defining new bone, residual graft and host bone for the graft material and species of the study, including typical attenuation and morphology and known confounders (e.g., graft particles with bone ingrowth, defect margins). If the study's graft material is not in the model's validated domain, notify the Scientific Lead before proceeding.

## 4. Procedure
1. Open each dataset's segmentation; confirm the legend shows the canonical label map (1 new bone, 2 residual graft, 3 host bone). Any mismatch → stop and report as an incident.
2. Review every dataset in all three planes, scrolling through the full ROI; pay specific attention to graft/new-bone interfaces and defect margins (host vs new bone).
3. **Mandatory review:** 100% of datasets flagged REVIEW_REQUIRED or out-of-domain; plus a second-reviewer sample of ≥ 20% (minimum 3) of remaining datasets per study, randomly selected by the system or a documented random procedure.
4. **Correction:** correct only clear misclassifications according to the guide. Do not adjust to reach expected values. Enter a specific reason (e.g., "graft particles at proximal margin labelled as new bone").
5. **Disagreements:** between analyst and second reviewer → Scientific Lead adjudicates; record decision.
6. **Large corrections:** if corrections change any class volume by > 20% (proposed threshold), add a note and notify the Scientific Lead (may indicate model domain shift — feed into periodic review/SOP-007).
7. Mark the dataset "segmentation reviewed".
8. **After unblinding:** corrections are discouraged; if essential, they are automatically flagged as post-unblinding and must be justified in the report.

## 5. Records
Original prediction (v0) and all versions (automatic); correction reasons and voxel deltas (automatic); second-review and adjudication records.

## 6. Revision history
| Version | Date | Change | Author |
|---|---|---|---|
| 0.1 | 2026-11-27 | Initial draft | QA/RA |
