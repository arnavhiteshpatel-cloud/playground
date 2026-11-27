# SOP-005: Audit Trail Review (OsteoQuant Desktop)

| Field | Value |
|---|---|
| SOP ID / version | SOP-005 / 0.2 (DRAFT) |
| Effective date | Not effective (draft) |
| Owner | Quality |
| Related requirements | URS-100…106, URS-132, URS-017; FS-100-1…FS-106-2, FS-132-1; RSK-20…23, RSK-48 |
| Benchmarks | 21 CFR 11.10(e); OECD GLP No. 17 ¶82; OECD GLP No. 22 (audit trail review) |

> **Status: DRAFT. Not approved or effective. No claim of 21 CFR Part 11 compliance, GLP compliance or validation.**

## 1. Purpose
Detect unauthorised, undocumented or suspicious changes to project records and verify the technical integrity of the project's audit trail.

## 2. Responsibilities
- **Reviewer (Quality or designee independent of the study team, with a reviewer account in the project):** performs reviews.
- **Project administrator:** provides access; must not review their own administrative actions alone.
- **Study lead:** responds to findings.

## 3. Frequency (risk-based, proposed)
| Review type | When |
|---|---|
| Study-level review | Before report approval (SOP-004) for each study |
| Technical chain verification + anchor comparison | Weekly while a project is active, and before every backup |
| Periodic project review | Quarterly: sign-in failures and lockouts, permission denials, user changes, exports, rejected imports |
| Event-driven | After any incident, integrity failure, unexpected file change, or suspected misconduct |

## 4. Anchors (until the desktop can export them, FS-102-2)
After each verification, record the latest sequence number and row hash shown in the *Audit trail* tab (newest entry) in the anchor log, which is kept **outside the project folder** (controlled document or paper). Compare the current chain with the last recorded anchor: the entry with that sequence number must still carry that hash. A missing or changed anchor entry indicates truncation or rewrite.

## 5. Procedure: study-level review
1. Open the project with a reviewer account; *Audit trail* tab; **Verify chain**. Record the result (intact / first altered event) and perform the anchor comparison (section 4).
2. Filter by the study's objects and by action; review:
   - rejected imports and their reasons; spacing confirmations;
   - QC verdicts of analysed scans against the intake log overrides (SOP-001 §6);
   - ROI saves and segmentation revisions: reasons specific? clusters by one user? large voxel changes?
   - edits after the unblinding date (from the study file);
   - re-runs and cancelled/failed jobs;
   - reviews: signer independence, failed re-authentications (`review.reauth_failed`), self-approval attempts;
   - report generation and exports, including `report.blinded_download_denied`;
   - blinded-mode and workflow-timing setting changes;
   - activity at unusual times or by unexpected users or roles.
3. Because study tables are not covered by the hash chain (RSK-48), compare for ≥ 3 specimens the values in the Results tab with the `segmentation.save` / `report.generate` hashes and with the exported report.
4. Record findings in the review log: none / observation / finding requiring action. The desktop has no audit export (FS-104-2): record entry sequence numbers and attach screenshots of relevant entries.
5. Findings: study lead response; potential data-integrity issues: incident report and CHANGE_CONTROL / CAPA as needed.

## 6. Procedure: periodic project review
Review user accounts and roles against access records (SOP-008), lockouts, failed sign-ins and re-authentications, permission denials, rejected imports, exports, and the backup log (SOP-006). Confirm that the project folder's OS permissions are unchanged (IQ-06).

## 7. Escalation
Altered chain, anchor mismatch or unexplained file change = critical incident: close the project on all workstations, make a read-only copy of the whole project folder and of the latest backups, notify Quality and management within 24 h, investigate.

## 8. Records
Verification results, anchor log, review log, screenshots, incident reports.

## 9. Revision history
| Version | Date | Change | Author |
|---|---|---|---|
| 0.1 | 2026-11-27 | Initial draft (server, tenants, daily job) | QA/RA |
| 0.2 | 2026-11-27 | Desktop Audit trail tab; manual anchor log; checks for data tables outside the chain | QA/RA |
