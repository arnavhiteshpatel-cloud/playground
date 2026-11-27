# SOP-005 — Audit Trail Review

| Field | Value |
|---|---|
| SOP ID / version | SOP-005 / 0.1 (DRAFT) |
| Effective date | Not effective (draft) |
| Owner | Quality |
| Related requirements | URS-100…106, URS-132; FS-100-1…FS-106-1, FS-132-1; RSK-20…23 |
| Benchmarks | 21 CFR 11.10(e); OECD GLP No. 17 ¶82; OECD GLP No. 22 (audit trail review) |

> **Status: DRAFT — not validated; not a claim of Part 11 compliance or GLP validation.**

## 1. Purpose
Detect unauthorised, undocumented or suspicious changes to data-relevant records and verify the technical integrity of the audit trail.

## 2. Responsibilities
- **Reviewer (Quality or designee independent of the study team):** performs reviews.
- **Admin:** provides exports; must not review their own administrative actions alone.
- **Study lead:** responds to findings.

## 3. Frequency (risk-based, proposed)
| Review type | When |
|---|---|
| Study-level review | Before report approval (SOP-004) for each study |
| Technical chain verification | Daily automated job; result reviewed weekly |
| Periodic system review | Quarterly: security events, admin actions, role changes, failed integrity checks |
| Event-driven | After any incident, integrity failure, or suspected misconduct |

## 4. Procedure — study-level review
1. Run audit-chain verification for the tenant; record result (VALID / first broken link). Compare chain head with the external anchor (FS-102-2).
2. Filter the audit trail by study; review:
   - QC overrides — reasons adequate?
   - ROI and segmentation corrections — reasons specific? Clusters by one user? Large corrections?
   - Post-unblinding edits — justified?
   - SAP amendments and exclusions — before or after unblinding?
   - Re-runs — reasons; were earlier results superseded selectively?
   - Signatures — signer independence; invalidations.
   - Activity at unusual times or by unexpected users/roles.
3. Record findings in the review log: none / observation / finding requiring action.
4. Findings → study lead response; potential data-integrity issues → incident report and CHANGE_CONTROL/CAPA as needed.

## 5. Procedure — periodic system review
Review user/role changes against access requests (SOP-008), lockouts, cross-tenant attempts, export volume anomalies, integrity failures, backup job results.

## 6. Escalation
Broken chain or anchor mismatch = critical incident: freeze affected tenant writes (admin), notify Quality and management within 24 h, preserve evidence (copy DB and backups), investigate.

## 7. Records
Verification outputs, review log, incident reports. Audit trail exports used in review are retained with the review record.

## 8. Revision history
| Version | Date | Change | Author |
|---|---|---|---|
| 0.1 | 2026-11-27 | Initial draft | QA/RA |
