# SOP-008 — User Access Management

| Field | Value |
|---|---|
| SOP ID / version | SOP-008 / 0.1 (DRAFT) |
| Effective date | Not effective (draft) |
| Owner | Tenant admin (per organisation) with Quality |
| Related requirements | URS-010…016, URS-132; FS-010-1…FS-016-1; RSK-23…25 |
| Benchmarks | 21 CFR 11.10(d),(g),(i),(j), 11.300; OECD GLP No. 17 ¶90, ¶92, ¶97–98 |

> **Status: DRAFT — not validated; not a claim of Part 11 compliance or GLP validation.**

## 1. Purpose
Grant, change and remove access so that every action is attributable to a trained, authorised individual with the minimum necessary privileges.

## 2. Roles
| Role | Typical holder | Key restrictions |
|---|---|---|
| admin | IT / system owner | No analysis or review actions; should have no interest in study data (OECD 17 ¶98) |
| analyst | Scientists performing analysis | Cannot approve own reports |
| reviewer | Senior scientist / study lead | Cannot edit data |
| viewer | Collaborators, management | Read-only |

## 3. Procedure
1. **Request:** written/electronic access request naming the person, tenant, role, studies (if restricted), and justification; approved by the person's supervisor/study lead.
2. **Training prerequisite:** the requester has completed training on relevant SOPs (records kept) and signed the account-use and e-signature acknowledgement (no credential sharing; signature equivalence).
3. **Provisioning:** admin creates account (unique username, never reused), assigns role, sends activation via secure channel; first login forces password set.
4. **Role changes:** same as request; combinations admin+analyst/reviewer prohibited unless justified and approved by Quality (system requires justification).
5. **Deactivation:** within 1 working day of leaving or role end; immediate on suspected compromise. Never delete accounts.
6. **Lockouts:** unlock only after identity confirmation; audited.
7. **Periodic access review:** at least annually and on organisational change (OECD 17 ¶90): admin exports user/role list; study lead/Quality confirm each account; discrepancies corrected and recorded.
8. **Lost/compromised credentials:** report immediately; admin locks account, forces reset; Quality assesses records created during exposure window (SOP-005).

## 4. Records
Access requests/approvals, training records, acknowledgements, access review records, system audit trail.

## 5. Revision history
| Version | Date | Change | Author |
|---|---|---|---|
| 0.1 | 2026-11-27 | Initial draft | QA/RA |
