# OsteoQuant Desktop: Installation Qualification (IQ) Protocol

| Field | Value |
|---|---|
| Document ID | OQ-QMS-IQ-001 |
| Version | 0.2 (DRAFT), Generation-2 desktop re-baseline |
| Date | 2026-11-27 |
| Applies to | One named workstation installation of OsteoQuant Desktop per execution |
| Related | URS / FS v0.2, OQ_PROTOCOL.md, SOP-006, SOP-007, SOP-008, `docs/desktop/PACKAGING.md` |

> **Status: DRAFT template. Never executed. No claim of 21 CFR Part 11 compliance, GLP compliance, computerised-system validation or regulatory acceptance.**
> Executing this protocol would document that one workstation was installed as specified. It would not by itself validate the system for any regulated use; that remains the user organisation's responsibility for its intended use.

## 1. Objective
Provide documented evidence that OsteoQuant Desktop, its bundled dependencies, any model artifacts, its licence state and the workstation controls it relies on are installed as specified and traceable to an identified release.

## 2. Scope
The installed application bundle (PyInstaller build or Python environment), bundled third-party components, model artifacts (if any), the licence file (if any), the workstation clock, the location and OS permissions of project folders, and the backup arrangement for project folders. There is no server, database service, reverse proxy or network component.

## 3. Responsibilities
| Role | Responsibility |
|---|---|
| Installer (IT or engineering) | Executes the steps, records results and evidence |
| Engineering Lead | Approves the protocol, reviews deviations |
| Quality (independent of the installer) | Reviews the executed protocol and approves the summary |
| User organisation | Owns workstation OS controls (accounts, permissions, clock, disk encryption, backup) |

## 4. Prerequisites
- Identified release: installer/bundle SHA-256, version, bundled-component list (SBOM), model artifact hashes, release notes (URS-141; none exist yet).
- Approved change record (CHANGE_CONTROL.md) authorising the installation.
- Named OS accounts for every person who will use the workstation; no shared OS accounts.

## 5. Execution rules (good documentation practice)
Record actual results contemporaneously; attach evidence (screenshots, command output with hashes, the self-test JSON log); no blank fields (N/A with justification); corrections by single line-through with initials, date and reason (paper) or as a new dated entry (electronic); deviations in section 8.

## 6. Environment record
| Item | Expected | Actual | Evidence ref |
|---|---|---|---|
| Workstation name / asset ID | | | |
| OS and version | Supported list in release notes | | |
| CPU / RAM / free disk | ≥ minimums in release notes (analysis is in-memory; see ARCHITECTURE.md *Performance and memory*) | | |
| Display / GPU driver (OpenGL for VTK) | Supported list | | |
| Disk encryption for project storage (Y/N) | Y recommended | | |
| Network connectivity during use | Not required | | |

## 7. Test steps
| Step | Description | Acceptance criterion | Trace | Result (P/F) | Evidence |
|---|---|---|---|---|---|
| IQ-01 | Compute SHA-256 of the installer / application bundle and compare with the release record. | Exact match | URS-002 | | |
| IQ-02 | Compare bundled components with the SBOM; record the `pip-audit` result for the release; open *Help > About* and check the third-party component and licence list. | Components match; no unresolved critical vulnerability, or documented risk acceptance; licence list present | URS-131, FS-131-1 | | |
| IQ-03 | If model artifacts are installed: compute SHA-256 of each and compare with the model registry; record the label map. | All match; label map {0 background, 1 new bone, 2 residual graft, 3 host bone} | URS-111, URS-054 | | |
| IQ-04 | Start the application; *Help > About*: record version, licence state and the RUO / not-validated statement. | Version matches release; RUO statement visible; licence state as intended (evaluation, valid, or test with watermark) | URS-001, URS-002, URS-191 | | |
| IQ-05 | Check workstation time synchronisation (OS time service) and time zone; create a test project and confirm audit timestamps are UTC. | Offset < 1 s from the reference; timestamps end in "Z" | URS-106, FS-106-2 | | |
| IQ-06 | Record the project-folder location; verify OS permissions (read/write only for named study users and the backup account; no "Everyone"/world write); verify the folder is on a local or supported drive and that disk encryption status matches the environment record. | Permissions as specified by the user organisation | URS-017, FS-017-1, RSK-20, RSK-48 | | |
| IQ-07 | Disconnect the network (or block it with the OS firewall) and run `osteoquant-desktop --selftest` (or `python -m osteoquant.desktop --selftest`); keep the JSON log. | Every step `"ok": true`; final line `"selftest": "PASS"` | URS-210, FS-210-1 | | |
| IQ-08 | Confirm `OSTEOQUANT_ACCEPT_TEST_LICENCES` is not set in the user environment. If a licence is to be installed: *Help > Licence*, install the `.oqlic` file, record state, edition, licensee, expiry and whether reports carry a watermark. | Test licences not accepted; installed licence state *valid* (or documented evaluation use) | URS-190, URS-192 | | |
| IQ-09 | Create the study project (*File > New project*) with a named administrator; open *Audit trail* and *Verify chain*; record the chain head (seq, hash) in the IQ record as the first external anchor. | Chain intact; administrator is a named person; anchor recorded outside the project folder | URS-010, URS-102 | | |
| IQ-10 | Configure backup of the project folder per SOP-006; run the first backup; restore it to a scratch location and open it; *Verify chain*. | Backup completes; restored project opens; chain intact | URS-120, URS-121 | | |
| IQ-11 | Confirm the documentation set is available at the stated versions (user guide, SOPs, release notes). | Available, versions match | URS-140, URS-141 | | |

## 8. Deviations
| Dev ID | Step | Description | Impact assessment | Resolution / CAPA | Approved by / date |
|---|---|---|---|---|---|

## 9. Acceptance
IQ passes when all steps pass, or every failure has an approved deviation with a documented no-impact rationale. OQ may not start until IQ is approved.

## 10. Approval of executed IQ
| Role | Name | Signature | Date |
|---|---|---|---|
| Executed by | | | |
| Reviewed by (Engineering) | | | |
| Approved by (Quality) | | | |

## Change history
| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-11-27 | Generation-1 server installation (FastAPI, TLS, NTP, server database) |
| 0.2 | 2026-11-27 | Re-baselined to the offline desktop workstation; server, TLS and tenant steps removed |
