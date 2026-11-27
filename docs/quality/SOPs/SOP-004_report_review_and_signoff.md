# SOP-004 — Report Review and Sign-off

| Field | Value |
|---|---|
| SOP ID / version | SOP-004 / 0.1 (DRAFT) |
| Effective date | Not effective (draft) |
| Owner | Quality / Scientific Lead |
| Related requirements | URS-080…083, URS-090…093, URS-015; FS-090-1…FS-093-1, FS-015-2; RSK-18, RSK-26 |

> **Status: DRAFT — not validated; not a claim of Part 11 compliance or GLP validation.**

## 1. Purpose
Ensure reports are complete, consistent with underlying data, and approved by an independent reviewer using an attributable electronic sign-off.

## 2. Electronic sign-off policy (summary; full policy TBD)
- Signing in OsteoQuant means the signer takes responsibility for the stated meaning (AUTHORED / REVIEWED / APPROVED).
- Each signer must have signed a written acknowledgement that their electronic signature is the equivalent of their handwritten signature within the organisation and that they will not share credentials. (Note: for FDA-regulated use, 21 CFR 11.100(c) requires a certification to FDA by the organisation — **not in place**; see gap analysis.)
- Signing requires password re-entry.

## 3. Responsibilities
- **Author (analyst):** prepares and signs AUTHORED.
- **Reviewer:** independent of the author and of anyone who edited ROI/segmentation for the report; signs REVIEWED/APPROVED or REJECTS with reason.

## 4. Review checklist
1. RUO/not-validated statement present.
2. Provenance: input hashes, software version/commit, model hash, config snapshot ID, ROI/segmentation versions, SAP version, unblinding time.
3. All specimens accounted for; exclusions listed with reasons and pre-specified criteria.
4. QC overrides listed and justified.
5. Post-unblinding edits (if any) listed and justified.
6. Units and voxel sizes shown; density metrics only with calibration.
7. Spot-check: ≥ 3 specimens — open segmentation and compare displayed metric values to the report/CSV.
8. Statistical methods match the locked SAP; deviations explained.
9. Audit trail review for this study completed per SOP-005 (or scheduled before approval).
10. Report conclusions do not exceed the validated context of use (currently: none — research prototype).

## 5. Procedure
1. Author submits (DRAFT → IN_REVIEW).
2. Reviewer completes checklist; records comments in system.
3. Approve (sign with password) or Reject (reason mandatory) → returns to DRAFT.
4. If any underlying record changes after approval, the system invalidates the signature; repeat review.
5. Export final PDF/CSV and archive per DATA_RETENTION_POLICY.

## 6. Records
Signatures (automatic), checklist record, review comments, exported final report with its hash.

## 7. Revision history
| Version | Date | Change | Author |
|---|---|---|---|
| 0.1 | 2026-11-27 | Initial draft | QA/RA |
