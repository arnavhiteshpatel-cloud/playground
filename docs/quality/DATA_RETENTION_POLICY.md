# OsteoQuant: Data Retention Policy (Draft)

| Field | Value |
|---|---|
| Document ID | OQ-QMS-DRP-001 |
| Version | 0.2 (DRAFT), Generation-2 desktop re-baseline |
| Date | 2026-11-27 |
| Owner | Quality with Legal/Privacy |
| Related | URS-105, URS-120…124; FS-105-1, FS-122-1, FS-123-1, FS-124-1; SOP-006 |

> **Status: DRAFT. Not approved. No claim of 21 CFR Part 11 compliance, GLP compliance or validation.**
> Desktop context: records live in project folders on the customer's own workstations and storage. The customer, not OsteoQuant, holds and retains them. The software does not yet enforce retention periods, legal hold or dual-approval deletion (FS-122-1, FS-123-1); until it does, sections 3–4 are procedural controls of the customer.
> Retention periods below are proposed defaults for a research tool. Customers remain responsible for the retention obligations applicable to them (institutional policy, funder terms, publication requirements, and — if used in regulated studies — 21 CFR 58.195 / OECD GLP). Legal review required.

## 1. Principles
1. **No automatic deletion** of study records by default. Deletion is an explicit, approved act after retention expiry.
2. **Retain together:** original data, derived data, configuration snapshots, model artifacts/manifests, software version identifiers, audit trail and reports are retained as one information package so a study can be reconstructed (OECD GLP No. 17 ¶114, ¶117).
3. **Audit trail retention ≥ retention of the records it describes** (21 CFR 11.10(e) benchmark).
4. **Legal hold overrides** all expiry.
5. **Customer ownership:** project folders belong to and are stored by the customer organisation. OsteoQuant (as software supplier) holds no customer study data; for analysis services, retention and return/deletion follow the service contract (which must not conflict with this policy, review CRO-10).

## 2. Record categories and proposed defaults
| Category | Examples | Proposed default retention | Rationale / reference |
|---|---|---|---|
| A. Study primary data | Original micro-CT files and hashes; acquisition metadata | Customer-configured; **minimum 10 years after study closure** proposed default | Typical institutional research-data policies; GLP 58.195 periods are shorter for some cases but customer obligations vary [INF] |
| B. Derived data | ROIs, segmentations (v0 + corrections), metrics, stats outputs | Same as A | Needed for reconstruction |
| C. Reports & signatures | PDF/CSV reports, signature records | Same as A | — |
| D. Audit trail | All entries in the project | ≥ longest retention of A–C in the project; never purged while any related record exists (the software never deletes audit entries) | 21 CFR 11.10(e) benchmark |
| E. System records | Software releases, model artifacts & manifests, configuration defaults, validation/verification records, CRs | As long as any retained study result depends on them, plus 2 years | OECD 17 ¶117 |
| F. Security events | Sign-in, failed sign-in/re-authentication, permission denials, export events (in the project audit trail) | As D (they are audit entries) | Security investigation needs |
| G. Backups | Daily/weekly/monthly | Per SOP-006 (35 days / 13 weeks / 7 years for monthly) | Recovery; not a substitute for archive |
| H. Account data | User profiles (deactivated) | Retained as long as D (to keep attributability); personal data minimised | Attributability vs privacy — legal review |

Regulated-use reference (if a customer uses data in GLP studies): 21 CFR 58.195(b) — shortest of ≥2 years after FDA approval of the application; ≥5 years after submission of results; otherwise ≥2 years after study completion/termination [V; see REGULATORY_RESEARCH.md]. Customers in OECD-MAD jurisdictions must apply national GLP retention rules [PK].

## 3. Configuration (system)
- Target (FS-122-1, not implemented): retention period per project and optionally per study (period, trigger event such as study closure or report approval, legal-hold flag); deletion within retention refused and the attempt audited; changes to retention settings audited and approved by admin + Quality.
- Current software: `delete_study_data` requires the `delete` permission (admin) and a reason, keeps the audit trail and records the deletion; there is no retention check, legal hold or second approval, and the desktop offers no delete function. Customers control deletion of project folders through OS permissions and this policy.

## 4. Deletion after expiry
1. The study lead lists records eligible for deletion; the data owner reviews.
2. Deletion request (project admin) + written approval by a second authorised person (data owner/Quality); legal-hold check.
3. Optional pre-deletion archive export (FS-124-1) delivered to customer, with manifest verification.
4. Deletion executed; audit entry retains object IDs, hashes, approvers and timestamps (not content).
5. Backups containing deleted data expire naturally per backup schedule; documented in the deletion record.

## 5. Archiving and readability
- Archive packages use open formats (CSV, JSON, PDF, NIfTI/TIFF) with SHA-256 manifest.
- Long-term readability: retain the software release (or container image) for each version that produced retained results; test readability of archived packages at least every 2 years (proposed) and after major format/storage changes.

## 6. Personal data
Image data are animal data; user account data are personal data. Minimise personal data; document lawful basis and retention for user data; apply applicable privacy law (legal review required).

## 7. Review
Annually, or on regulatory/contractual change.
