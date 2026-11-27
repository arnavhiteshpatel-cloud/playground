# SOP-008: User Access Management (OsteoQuant Desktop)

| Field | Value |
|---|---|
| SOP ID / version | SOP-008 / 0.2 (DRAFT) |
| Effective date | Not effective (draft) |
| Owner | Project administrator (per project) with Quality |
| Related requirements | URS-010…017, URS-092, URS-132; FS-010-1…FS-017-1, FS-092-2; RSK-23, RSK-24, RSK-48 |
| Benchmarks | 21 CFR 11.10(d),(g),(i),(j), 11.300; OECD GLP No. 17 ¶90, ¶92, ¶97–98 |

> **Status: DRAFT. Not approved or effective. No claim of 21 CFR Part 11 compliance, GLP compliance or validation.**

## 1. Purpose
Grant, change and remove access so that every action in a project is attributable to a trained, authorised individual with the minimum necessary privileges, on the application **and** on the workstation.

## 2. Two layers of access
| Layer | Controls | Owner |
|---|---|---|
| Workstation / OS | Named OS accounts; read/write on the project folder only for named study users and the backup account; screen lock; disk encryption (IQ-06) | User organisation IT |
| Project (application) | Named project accounts and roles; lockout; re-authentication at signing | Project administrator |

Accounts are **per project**: a person working in two projects has an account in each.

## 3. Roles
| Role | Typical holder | Key restrictions |
|---|---|---|
| admin | Project owner / system owner | Holds every permission in the current software. Should not analyse or sign study work; where unavoidable (small labs), record the justification in the access log (FS-015-1 not implemented) |
| analyst | Scientists performing analysis | Cannot sign; cannot approve own work |
| reviewer | Senior scientist / study lead | Cannot import, analyse or edit |
| viewer | Collaborators, management | Read-only |

## 4. Procedure
1. **Request:** written or electronic request naming the person, project, role and justification; approved by the supervisor or study lead.
2. **Training prerequisite:** relevant SOPs completed (records kept) and the account-use / e-signature acknowledgement signed (no credential sharing; signature equivalence).
3. **Provisioning:** the desktop has **no user-administration screen** (FS-010-3) and no password-change function. Until they exist, additional project accounts can only be created through the library (`Store.create_user` with the administrator as actor, recorded as `user.create`). An administration script for this must be issued under CHANGE_CONTROL before use; none has been issued yet. The new user types their own initial password (≥ 10 characters, an upper-case letter and a digit) with the administrator present but not watching. **Never** let several people work under the administrator account; if named accounts cannot be provisioned, the project is not used for work that requires attributability.
4. **Workstation access:** IT grants OS access to the project folder (layer 1) only after step 3.
5. **Role changes:** as a new request; the software has no role-change function, so a new account is created and the old one deactivated.
6. **Deactivation:** within 1 working day of leaving or role end; immediately on suspected compromise; deactivate (never delete) the project account (`user.deactivate`) and remove OS access.
7. **Lockouts:** five wrong passwords at sign-in lock the account for 15 minutes. Known defect: wrong passwords at signing in the desktop do not count (FS-092-2). Users report repeated failed signing attempts to the administrator, who checks `review.reauth_failed` entries.
8. **Unattended workstations:** lock the OS session when leaving (the desktop has no idle lock, FS-013-3).
9. **Periodic access review:** at least yearly and on organisational change: list project accounts and roles, and OS permissions on the project folder; study lead/Quality confirm each; discrepancies corrected and recorded.
10. **Lost/compromised credentials:** report immediately; administrator deactivates the account; Quality assesses records created during the exposure window (SOP-005).

## 5. Records
Access requests and approvals, training records, acknowledgements, access log (justifications, provisioning), access reviews, project audit trail.

## 6. Revision history
| Version | Date | Change | Author |
|---|---|---|---|
| 0.1 | 2026-11-27 | Initial draft (tenant administration) | QA/RA |
| 0.2 | 2026-11-27 | Per-project accounts; OS layer; interim provisioning without a user-administration screen; known lockout defect | QA/RA |
