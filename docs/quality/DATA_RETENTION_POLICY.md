# OsteoQuant — Data Retention Policy (Draft)

| Field | Value |
|---|---|
| Document ID | OQ-QMS-DRP-001 |
| Version | 0.1 (DRAFT) |
| Date | 2026-11-27 |
| Owner | Quality with Legal/Privacy |
| Related | URS-105, URS-120…124; FS-105-1, FS-122-1, FS-123-1, FS-124-1; SOP-006 |

> **Status: DRAFT — not validated; not a claim of Part 11 compliance or GLP validation.**
> Retention periods below are proposed defaults for a research tool. Customers remain responsible for the retention obligations applicable to them (institutional policy, funder terms, publication requirements, and — if used in regulated studies — 21 CFR 58.195 / OECD GLP). Legal review required.

## 1. Principles
1. **No automatic deletion** of study records by default. Deletion is an explicit, approved act after retention expiry.
2. **Retain together:** original data, derived data, configuration snapshots, model artifacts/manifests, software version identifiers, audit trail and reports are retained as one information package so a study can be reconstructed (OECD GLP No. 17 ¶114, ¶117).
3. **Audit trail retention ≥ retention of the records it describes** (21 CFR 11.10(e) benchmark).
4. **Legal hold overrides** all expiry.
5. **Tenant ownership:** customer data belong to the customer organisation; OsteoQuant (as processor/host) retains per contract and returns/deletes on termination as agreed.

## 2. Record categories and proposed defaults
| Category | Examples | Proposed default retention | Rationale / reference |
|---|---|---|---|
| A. Study primary data | Original micro-CT files and hashes; acquisition metadata | Customer-configured; **minimum 10 years after study closure** proposed default for hosted service; or until customer export & instructed deletion | Typical institutional research-data policies; GLP 58.195 periods are shorter for some cases but customer obligations vary [INF] |
| B. Derived data | ROIs, segmentations (v0 + corrections), metrics, stats outputs | Same as A | Needed for reconstruction |
| C. Reports & signatures | PDF/CSV reports, signature records | Same as A | — |
| D. Audit trail | All entries for tenant | ≥ longest retention of A–C in the tenant; never purged while any related record exists | 21 CFR 11.10(e) benchmark |
| E. System records | Software releases, model artifacts & manifests, configuration defaults, validation/verification records, CRs | As long as any retained study result depends on them, plus 2 years | OECD 17 ¶117 |
| F. Security logs | Login, access, export events | 3 years (proposed) | Security investigation needs |
| G. Backups | Daily/weekly/monthly | Per SOP-006 (35 days / 13 weeks / 7 years for monthly) | Recovery; not a substitute for archive |
| H. Account data | User profiles (deactivated) | Retained as long as D (to keep attributability); personal data minimised | Attributability vs privacy — legal review |

Regulated-use reference (if a customer uses data in GLP studies): 21 CFR 58.195(b) — shortest of ≥2 years after FDA approval of the application; ≥5 years after submission of results; otherwise ≥2 years after study completion/termination [V; see REGULATORY_RESEARCH.md]. Customers in OECD-MAD jurisdictions must apply national GLP retention rules [PK].

## 3. Configuration (system)
- Retention policy objects per tenant and optionally per study: period, trigger event (study closure date, report approval date), legal hold flag.
- Records within retention cannot be deleted (HTTP 423, audited attempt).
- Changes to retention settings are audited and require admin + Quality (or tenant owner) approval.

## 4. Deletion after expiry
1. System lists records eligible for deletion; tenant owner reviews.
2. Deletion request (admin) + approval by a second authorised person (tenant owner/Quality); legal-hold check.
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
