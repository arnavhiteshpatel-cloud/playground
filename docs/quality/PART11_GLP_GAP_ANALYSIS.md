# OsteoQuant — 21 CFR Part 11 / OECD GLP No. 17 Gap Analysis

| Field | Value |
|---|---|
| Document ID | OQ-QMS-GAP-001 |
| Version | 0.1 (DRAFT) |
| Date | 2026-11-27 |
| Basis | 21 CFR Part 11 (CFR 2024 ed.) [V]; OECD GLP No. 17 (ENV/JM/MONO(2016)13, 2022 reissue) [V]; OECD GLP No. 22 [V, translation] — see REGULATORY_RESEARCH.md |

> **Status: DRAFT — not validated; not a claim of Part 11 compliance or GLP validation.**
> Part 11 and Part 58 do not currently apply to OsteoQuant's research use. This analysis benchmarks the prototype against them to plan readiness for customers who may use it in regulated contexts. "Planned" technical controls are **not yet implemented or verified**.

## 1. Legend
- **Tech** = planned technical control in OsteoQuant (FS reference).
- **Proc/Org** = procedural or organisational control required (by OsteoQuant as supplier and/or by the user organisation as the regulated entity).
- **Status:** GAP = nothing in place · PARTIAL = partially addressed (planned/draft only) · DESIGNED = addressed by planned design (still requires implementation and verification).
- **Owner:** V = OsteoQuant (vendor/supplier); U = user organisation (test facility).

## 2. 21 CFR Part 11

| Provision | Requirement (summary) | Planned technical control | Procedural / organisational control still missing | Status | Owner |
|---|---|---|---|---|---|
| 11.10(a) | Validation; ability to discern invalid/altered records | Hashing (FS-020/021), hash-chained audit (FS-102), config snapshots, phantom tests | No executed verification, IQ/OQ/PQ; no validation plan/report; no validated context of use; QA independence not established | PARTIAL | V (verification evidence) + U (validation for intended use) |
| 11.10(b) | Accurate, complete copies, human-readable & electronic | PDF/CSV/JSON/NIfTI exports, archive package (FS-081, FS-124) | Procedure for providing copies to inspectors; verification that exports are complete (incl. audit trail, metadata) | PARTIAL | V/U |
| 11.10(c) | Protection/retrieval through retention period | Backup/restore (FS-120/121), retention locks (FS-122/123), open formats | Approved retention schedule; restore tests executed; archive procedure and archivist role; long-term readability plan | PARTIAL | U (V supports) |
| 11.10(d) | Limit access to authorised individuals | Unique accounts, RBAC, tenant isolation (FS-010…016) | SOP-008 approval & training; OS/server physical & logical access control; hosting security policy | PARTIAL | V/U |
| 11.10(e) | Secure, computer-generated, time-stamped audit trail; does not obscure prior info; retained | Append-only, hash-chained, UTC, old/new values, reasons (FS-100…106) | Audit-trail review SOP approval and execution (SOP-005); external anchoring operation; retention alignment | DESIGNED (unverified) | V/U |
| 11.10(f) | Operational system checks (sequencing) | QC gating, ROI-verified gate, SAP lock before unblinding, review state machine (FS-032, 042, 070, 090) | — (verify) | DESIGNED (unverified) | V |
| 11.10(g) | Authority checks | Permission per route (FS-011-2); signing re-auth | Documented authorisation matrix approved by user org | PARTIAL | V/U |
| 11.10(h) | Device checks (valid input source) | Hashing; metadata/format checks; scanner/source recorded | Procedure defining permitted data sources/transfer paths (SOP-001 draft) | PARTIAL | U |
| 11.10(i) | Training/qualification of developers, maintainers, users | — | **No training programme or records** for developers or users | GAP | V/U |
| 11.10(j) | Written policy: accountability for e-signatures | Signature meaning, re-auth | **No e-signature policy**; no signed user acknowledgements | GAP | U |
| 11.10(k) | Control over systems documentation; change control with audit trail | Git history; release manifests | **No document control system**; CHANGE_CONTROL draft not effective; no controlled distribution | GAP | V |
| 11.30 | Open systems: additional measures (encryption, digital signatures) | TLS; encryption at rest optional | Determine whether hosted multi-tenant SaaS is "open" or "closed" (vendor controls access, customer owns content) — **counsel question** | GAP (unassessed) | V/U |
| 11.50 | Signature manifestation: printed name, date/time, meaning | FS-091-1 | — (verify) | DESIGNED (unverified) | V |
| 11.70 | Signature/record linking | Signature bound to record hash (FS-093-1) | — (verify; also for exported PDF) | DESIGNED (unverified) | V |
| 11.100(a) | Unique to one individual, not reused/reassigned | Unique IDs, no reuse (FS-014-1) | — | DESIGNED (unverified) | V |
| 11.100(b) | Verify identity before assigning e-signature | — | **Identity verification procedure** in SOP-008 | GAP | U |
| 11.100(c) | Certification to FDA that e-signatures are legally binding equivalent | — | **Letter of certification** by user organisation (if FDA-regulated use) | GAP | U |
| 11.200 | Two distinct identification components; continuous session rules | Username+password at login; password at signing | Confirm behaviour for multiple signings in one continuous session meets §11.200(a)(1) | PARTIAL | V |
| 11.300 | ID/password controls (uniqueness, periodic check/revision, loss management, transaction safeguards, device testing) | Password policy, lockout, audited security events | Periodic password/credential review policy; loss-management procedure; unauthorised-use reporting to management | PARTIAL | U |

## 3. OECD GLP Advisory Document No. 17

| ¶ / Section | Expectation (summary) | Planned technical control | Procedural / organisational gap | Status |
|---|---|---|---|---|
| ¶12–15 Risk management | Documented risk assessment drives validation | RISK_ASSESSMENT.md (draft) | Approval; periodic re-assessment | PARTIAL |
| ¶16–21, App. 1 Roles & personnel | Defined roles, training, test facility management responsibilities | Roles in system | **No org chart, role descriptions, training records**; no QA function independent of development | GAP |
| ¶22–30 Management/QA/Study director | Management responsibilities; QA knowledge of systems | — | **No QA unit / QA programme** | GAP |
| ¶33 Inventory | Inventory of computerised systems | — | User org must inventory OsteoQuant; vendor provides system description | GAP (U) |
| ¶34–39 Suppliers / hosted services | Written agreements; supplier assessment; hosted-service agreements | — | **No quality agreement / SLA template**; no supplier-audit readiness pack; no subprocessor (cloud host) assessment | GAP |
| ¶42, ¶56–58 URS | URS for all GLP-relevant functions, traceable | URS.md, FS.md, RTM | Approval; customer-specific URS for intended use | PARTIAL |
| ¶44–45, ¶53–55, ¶84–88 Change & configuration mgmt | Written change control through life cycle | Release manifests, config snapshots, model hash locks | CHANGE_CONTROL.md not effective; no CR records yet; OS patch management under change control | PARTIAL |
| ¶46–50 Documentation | System documentation available for retention period | Drafts | Document control, versioning, retention | GAP |
| ¶51–52, ¶59–65 Validation & testing | Prospective validation; evidence of testing; UAT | Verification plan, IQ/OQ/PQ drafts | **No executed tests**; customised system → development-process assessment (¶60) and source-code access/escrow arrangement for customers | GAP |
| ¶66–69 Data migration | Validated migration preserving audit trail & signatures | Archive export with manifest | Migration procedure for schema upgrades; verification protocol | GAP |
| ¶70 Data exchange | Controlled interfaces | Hash verification at ingest | Interface specification for scanner exports | PARTIAL |
| ¶72 Accuracy checks for manual entry | Second-person checks where risk warrants | Duplicate checks; constraints | SOP-001 second-person verification (draft) | PARTIAL |
| ¶73–78 Data storage, backup | Defined backup; verified restorability; storage policy | FS-120/121 | Executed restore tests; storage policy (DATA_RETENTION_POLICY draft) | PARTIAL |
| ¶79 Printouts | Complete printouts or verifiable on-screen | PDF + JSON provenance | Define which record is the "regulated record" (electronic vs PDF) | PARTIAL |
| ¶80–83 Audit trail | Enabled, not changeable by study personnel, risk-based review | FS-100…106 | SOP-005 approval and execution; QA involvement | PARTIAL |
| ¶89–90 Periodic review | Periodic system review; yearly user review | — | **No periodic review procedure** (access review in SOP-008 draft) | GAP |
| ¶91–98 Security | Physical/logical security; admin without data interest; authorisation policy | RBAC, tenant isolation, segregation rule FS-015-1 | Hosting physical security evidence; security policy; vulnerability management process | PARTIAL |
| ¶99–100 Incident management | Incident records, CAPA, linkage to studies | Security event log | **No incident/CAPA procedure** | GAP |
| ¶101–107 E-signatures | Linked, timed, identity & meaning; password re-entry; policy | FS-091…093 | E-signature policy; signer list | PARTIAL |
| ¶108 Data approval | Validated approval workflow | Review state machine | Verification | DESIGNED (unverified) |
| ¶109–118 Archiving | Validated electronic archiving; archivist control; no destruction without authorisation; retain software/validation records as long as data | Archive export; retention lock; dual-approval deletion | **No archivist role or archive procedure**; long-term format/readability plan; retention of software versions | GAP |
| ¶119–122 Business continuity | Documented and tested contingency | Backup/restore | **No BC/DR plan**; RTO/RPO undefined | GAP |
| ¶123 Retirement | Planned retirement and data handling | Archive export | Retirement procedure | GAP |

## 4. OECD No. 22 / ALCOA+ quick check
| Attribute | Status |
|---|---|
| Attributable | DESIGNED (unique accounts, audit) — training/procedures missing |
| Legible | DESIGNED (human-readable exports) |
| Contemporaneous | DESIGNED (server UTC) — NTP control in IQ |
| Original | DESIGNED (immutable originals, v0 prediction) |
| Accurate | PARTIAL — verification and PQ not executed; graft vs new-bone discrimination unproven |
| Complete | DESIGNED (no silent exclusions, all runs retained) |
| Consistent | DESIGNED (hash chain, sequencing) |
| Enduring | PARTIAL — backup/archive procedures not tested |
| Available | PARTIAL — retrieval procedure for inspection not defined |
| Data governance (management responsibility, culture, risk-based review) | GAP |

## 5. Top gaps (prioritised)
1. **No executed verification/validation evidence** (IQ/OQ/PQ, verification report) — every technical control is "planned/unverified"; graft vs new-bone accuracy unproven.
2. **No quality management system basics:** document control, training records, independent QA function, incident/CAPA, periodic review.
3. **E-signature governance:** policy, identity verification, user acknowledgements; (for FDA-regulated customers) §11.100(c) certification is the customer's.
4. **Supplier/hosting framework:** quality agreement and SLA template, hosted-service security evidence, open-vs-closed system determination, source-code access/escrow for customers.
5. **Archiving and business continuity:** archivist role, validated archive procedure, executed restore tests, BC/DR plan with RTO/RPO, long-term readability (software retention).

## 6. Recommended next steps
1. Approve URS/FS/RA (v1.0) and implement high-risk controls first (RSK-01, -08, -12, -20).
2. Stand up a lightweight QMS (document control, training, CAPA, change control) — ISO 13485-aligned structure optional.
3. Execute verification and IQ/OQ on a reference instance; publish a "validation support package" for customers.
4. Draft customer quality agreement template; resolve counsel questions (REGULATORY_POSITIONING_MEMO.md).
