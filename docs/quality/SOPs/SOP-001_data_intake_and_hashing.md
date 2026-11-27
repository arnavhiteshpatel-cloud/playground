# SOP-001 — Data Intake and Hashing

| Field | Value |
|---|---|
| SOP ID / version | SOP-001 / 0.1 (DRAFT) |
| Effective date | Not effective (draft) |
| Owner | Scientific Lead |
| Related requirements | URS-020…026, URS-030…032; FS-020-1…FS-026-1; RSK-01, RSK-03, RSK-04 |

> **Status: DRAFT — not validated; not a claim of Part 11 compliance or GLP validation.**

## 1. Purpose
Ensure micro-CT datasets enter OsteoQuant complete, correctly identified, with verified acquisition metadata (especially voxel spacing) and a fixed SHA-256 fingerprint of the original files.

## 2. Scope
All datasets ingested into OsteoQuant for any study.

## 3. Responsibilities
- **Analyst:** performs intake, verifies metadata, resolves warnings.
- **Second person (analyst or reviewer):** verifies specimen identity mapping (step 5.4).
- **Study lead:** maintains the specimen manifest and approves exceptions.

## 4. Materials
Study specimen manifest (specimen ID, animal ID, time point, site/side, coded group label — **no treatment information**, see SOP-009); scanner acquisition logs; original reconstructed files as exported from the scanner workstation.

## 5. Procedure
1. **Before transfer:** on the scanner workstation, record file list and (if tooling available) SHA-256 of each exported file in the transfer log.
2. **Upload:** log in with your own account; select the study; upload original files (do not rename, convert, crop or rescale beforehand; if conversion is unavoidable, upload the unconverted original as well and record the conversion tool/version).
3. **Hash check:** confirm the system-computed SHA-256 for each file matches the transfer log value (where available). Mismatch → stop; re-transfer; record a deviation.
4. **Identity mapping:** assign specimen ID, time point and site/side from the manifest. A second person verifies the mapping against the manifest and confirms in the system (or signs the transfer log).
5. **Metadata verification:** review the extracted metadata: voxel size (each axis and unit), kVp, µA, filter, integration time, reconstruction settings, calibration reference. Compare voxel size against the scanner log. If spacing status ≠ VERIFIED, do **not** override from memory — obtain the value from the acquisition log and record its source as a reason; otherwise leave unverified (physical-unit outputs will be blocked).
6. **Duplicates:** resolve any duplicate-hash or duplicate specimen/time-point warning; never confirm a duplicate without a written reason.
7. **QC:** run automated QC. Review each WARN/FAIL. Overrides only per §6.
8. **Rejections:** note any INGEST_REJECTED file, its reason code, and corrective action in the intake log.

## 6. QC override rules
Override only when the failure is understood and does not affect the planned measurements (e.g., saturation outside the ROI). Enter a specific reason (not "OK"). Overrides appear in reports and are reviewed under SOP-004 and SOP-005.

## 7. Records
System audit trail (automatic); transfer log; intake log (exceptions/deviations); specimen manifest version used.

## 8. Do not
Edit files on disk; share accounts; upload data containing group/treatment names in filenames or metadata.

## 9. Revision history
| Version | Date | Change | Author |
|---|---|---|---|
| 0.1 | 2026-11-27 | Initial draft | QA/RA |
