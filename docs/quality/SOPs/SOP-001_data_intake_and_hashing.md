# SOP-001: Data Intake and Hashing (OsteoQuant Desktop)

| Field | Value |
|---|---|
| SOP ID / version | SOP-001 / 0.2 (DRAFT) |
| Effective date | Not effective (draft) |
| Owner | Scientific Lead |
| Related requirements | URS-020…026, URS-030…032; FS-020-1…FS-026-2, FS-030-1, FS-031-1; RSK-01, RSK-03, RSK-04 |

> **Status: DRAFT. Not approved or effective. No claim of 21 CFR Part 11 compliance, GLP compliance or validation.**

## 1. Purpose
Ensure micro-CT scans enter an OsteoQuant Desktop project complete, correctly identified, with explicit voxel spacing and a fixed SHA-256 fingerprint.

## 2. Scope
All scans imported into an OsteoQuant Desktop project for any study.

## 3. Responsibilities
- **Analyst:** performs the import, verifies metadata, resolves warnings.
- **Second person (analyst or reviewer):** verifies the specimen identity mapping (step 5.5).
- **Study lead:** maintains the specimen manifest and approves exceptions.

## 4. Materials
Study specimen manifest (specimen ID, animal ID, time point, site/side, coded group label; **no treatment information**, see SOP-009); scanner acquisition logs; original reconstructed files as exported from the scanner workstation, on a local or removable drive readable by the analysis workstation.

## 5. Procedure
1. **Before transfer:** on the scanner workstation, record the file list and (if tooling is available) the SHA-256 of each exported file in the transfer log.
2. **Open the project:** start OsteoQuant Desktop, *File > Open project*, sign in **with your own account** (never another person's). Select the study in the Project panel.
3. **Import wizard, step 1 (Select scans):** *File > Import scans*. Add the original files or folders. Do not rename, convert, crop or rescale beforehand. If conversion is unavoidable, keep the unconverted original and record the conversion tool and version in the intake log.
4. **Step 2 (Metadata and voxel spacing):** for every scan check the spacing source shown (*file metadata*, *ASSUMED by reader*, *MISSING*). For assumed or missing spacing, take the value from the acquisition log (never from memory), type it in µm (z, y, x), tick *Confirmed*, and record the source of the value in the intake log. Compare file-derived spacing with the scanner log; if they differ, stop and resolve with the study lead.
5. **Step 3 (Assign):** enter animal ID, time point label and day from the manifest; untick *Import* for anything that must not be imported. A second person checks the assignments against the manifest **before** step 6 and initials the intake log. The software does not yet flag a second scan for the same animal and time point (FS-025-2), so the second person checks for this explicitly.
6. **Step 4 (Import and QC):** *Start import*. Record for each scan the outcome (*imported*, *flagged*, *rejected*). Compare the SHA-256 shown in the scan information with the transfer log where available; a mismatch means stop, re-transfer and record a deviation.
7. **Rejections:** every rejected or excluded source stays listed under *Rejected imports* with its reason. Record each in the intake log with the corrective action.
8. **QC review:** for *flagged* scans open the QC checks. Deterministic failures (e.g. missing slices, saturation, non-finite values) are facts about the file; heuristic warnings are developer-chosen scores. The software does **not** block analysis of an unsuitable scan (FS-032-1 not implemented); apply section 6 manually.

## 6. QC override rules (procedural until FS-032-1 exists)
A scan with an "unsuitable" verdict may be analysed only when the failure is understood and does not affect the planned measurements (e.g. saturation outside the ROI). The study lead approves in writing, the reason is recorded in the intake log, and the report reviewer is informed (SOP-004 checklist item 4).

## 7. Records
Project audit trail (automatic: `scan.import`, `scan.import_rejected`, `scan.qc`); import log in the project (*Rejected imports*); transfer log; intake log (spacing sources, second-person check, QC overrides, deviations); specimen manifest version used.

## 8. Do not
Edit or move files inside the project folder with other programs; share accounts; import data containing group/treatment names in file names, folder names or metadata.

## 9. Revision history
| Version | Date | Change | Author |
|---|---|---|---|
| 0.1 | 2026-11-27 | Initial draft (web upload) | QA/RA |
| 0.2 | 2026-11-27 | Desktop import wizard; explicit spacing confirmation; manual QC-override and second-scan checks until implemented | QA/RA |
