# SOP-004: Report Review and Sign-off (OsteoQuant Desktop)

| Field | Value |
|---|---|
| SOP ID / version | SOP-004 / 0.2 (DRAFT) |
| Effective date | Not effective (draft) |
| Owner | Quality / Scientific Lead |
| Related requirements | URS-080…083, URS-090…093, URS-015, URS-152, URS-191; FS-090-1…FS-093-2, FS-015-2, FS-152-2; RSK-18, RSK-26, RSK-38 |

> **Status: DRAFT. Not approved or effective. No claim of 21 CFR Part 11 compliance, GLP compliance or validation.**

## 1. Purpose
Ensure reports are complete, consistent with the underlying project data, carry their measurement-support statements, and are approved by an independent reviewer with an attributable electronic sign-off.

## 2. Electronic sign-off policy (summary; full policy TBD)
- Signing in OsteoQuant means the signer takes responsibility for the stated meaning, which is typed at each signature.
- Each signer has signed a written acknowledgement that the electronic signature is the equivalent of their handwritten signature within the organisation and that they will not share credentials. (For FDA-regulated use, 21 CFR 11.100(c) requires a certification to FDA by the organisation; **not in place**, see the gap analysis.)
- Signing requires password re-entry. Known defect: in the desktop, wrong passwords at signing do not count towards account lockout (FS-092-2). Report repeated failures to the project administrator.

## 3. Responsibilities
- **Author (analyst):** generates the report and submits it for review.
- **Reviewer (reviewer role):** independent of the author and of anyone who edited ROI/segmentation for the report; signs segmentation versions and the report, or rejects with a reason. The software refuses approval by the creator of the object.

## 4. Review checklist
1. Licence state: no evaluation or test watermark on a report used for study decisions.
2. RUO / not-validated statement present.
3. Provenance: scan hashes, voxel spacing, software version, model hash (if used), ROI and segmentation versions, corrections, advisor version. Acquisition parameters are not yet printed (FS-080-1); attach them from the acquisition log.
4. QC overrides (SOP-001 §6) listed and justified.
5. Measurement-support section: every *not measured* endpoint has a reason; conditional values are marked "(c)" and their conditions are stated in the conclusions; no conclusion relies on an endpoint that is not supported.
6. All specimens accounted for; exclusions listed with reasons and pre-specified criteria (from the analysis log).
7. Post-unblinding edits (if any) listed and justified (manual list, SOP-003 step 10).
8. Spot-check ≥ 3 specimens: open the scan, compare the Results tab values with the PDF/CSV.
9. Statistical methods match the signed SAP; deviations explained.
10. Audit trail review for this study completed per SOP-005.
11. Conclusions do not exceed the validated context of use (currently none: research software).

## 5. Procedure
1. Author: *Reports* tab, **Generate DefectFill report**; preview; inform the reviewer.
2. Reviewer: approve each reviewed segmentation version in the **Review** panel (state the meaning, re-enter password).
3. Reviewer: complete the checklist and record comments in the review log.
4. Reviewer: in the *Reports* tab, **Approve...** (meaning + password), or record rejection with a reason. The PDF sign-off table does not yet show in-system signatures (CRO-13); the signature record in the project and audit trail is the record of approval.
5. If any segmentation is revised or the report is regenerated after approval, the earlier signature covers only the earlier object (the stored SHA-256 differs); repeat the review and signature. The software does not yet display this supersession (FS-093-2): check the signed hash against the current one in the Review panel.
6. **Export...** the approved PDF and CSV; record the PDF SHA-256 (from the `report.generate` audit entry); archive per DATA_RETENTION_POLICY.

## 6. Records
Signatures and report hashes (automatic); checklist and review log; exported final report with its hash.

## 7. Revision history
| Version | Date | Change | Author |
|---|---|---|---|
| 0.1 | 2026-11-27 | Initial draft | QA/RA |
| 0.2 | 2026-11-27 | Desktop Review panel and Reports tab; measurement-support and watermark checks; known signature limitations | QA/RA |
