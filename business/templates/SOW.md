# Statement of Work: DefectFill Report (TEMPLATE)

> **Template only. Needs legal review before use (see `LEGAL_REVIEW_TERMS.md`).** OsteoQuant is not yet incorporated, and a legal entity must exist before this SOW can be signed. All prices are hypotheses [HYP]. Remove this box before sending.

**SOW No.:** [OQ-SOW-YYYY-NNN]  **Under Master Services Agreement / Terms dated:** [date]
**Customer:** [Legal name, address]  **Provider:** [OsteoQuant legal entity — TBD]
**Customer study identifier:** [code — no sponsor-confidential names required]
**Effective date:** [ ]  **Target completion:** [ ] business days after Data Acceptance

## 1. Background
Customer has run a preclinical bone-defect study and holds reconstructed micro-CT image data. Customer engages Provider to perform image analysis and deliver a DefectFill Report.

## 2. Scope of services
| Item | Included |
|---|---|
| Data intake & integrity check (file checksums, voxel size, orientation, completeness) | Yes |
| Defect ROI definition per Customer-approved protocol (geometry, size, location) | Yes |
| Three-class segmentation: new bone / residual graft / host bone | Yes |
| Human expert review of every segmentation, with corrections logged | Yes |
| Morphometry per ASBMR nomenclature (Bouxsein et al., JBMR 2010): e.g., TV, BV, BV/TV within defect ROI, residual graft volume fraction, Tb.Th/Tb.Sp/Tb.N where applicable | Yes (parameter list in Annex A) |
| Audit-trailed PDF report + CSV data tables + segmentation masks | Yes |
| Statistical comparison between groups | [Optional — Annex B] |
| GLP-related work | **Not offered** (no validation report exists; no GLP or Part 11 claim can be made) |

**Out of scope unless added by change order:** scanning or reconstruction; histology or histomorphometry; additional ROIs, time points or parameters beyond Annex A; re-analysis after Customer protocol changes; regulatory submission writing; any clinical or diagnostic use.

## 3. Customer responsibilities
- Provide reconstructed scans in an agreed format (DICOM / ISQ / TIFF stack / other), with voxel size, scanner model, energy/filter and reconstruction settings.
- Provide the study protocol excerpt: defect model, defect dimensions, graft material and its radiodensity if known, group allocation (it may be blinded), and time points.
- Name a technical contact. Approve the analysis protocol (Annex A) before production analysis starts.
- Confirm Customer has the right to share the data with Provider. Data must contain no human-subject identifiers.

## 4. Deliverables and acceptance
| # | Deliverable | Format | Acceptance |
|---|---|---|---|
| D1 | Analysis protocol (Annex A) | PDF | Customer approval in writing |
| D2 | Draft DefectFill Report | PDF + CSV + masks | Customer review within [10] business days |
| D3 | Final report (one round of comments included) | PDF + CSV + masks + audit log | Deemed accepted [10] business days after delivery unless a written non-conformance is raised |

## 5. Timeline
Data Acceptance (T0) → D1 at T0 + [5] bd → D2 at T0 + [turnaround: founder decision #14; same figure as the quote and the pilot proposal] bd depending on scan count → D3 within [5] bd of comments.

## 6. Fees [HYP — placeholders]
| Item | Basis | Amount |
|---|---|---|
| Non-GLP study report (≤[40] scans, ≤[2] time points) | Fixed | $[8,000–15,000] [HYP] |
| Material characterisation (optional) | Fixed | $[5,000–15,000] [HYP] |
| Additional scans beyond allowance | Per scan | $[___] [HYP] |
| GLP-related work | Not offered | Not offered: no validation report, quality system or Quality Agreement exists |
| Statistical analysis (optional) | Fixed | $[___] [HYP] |
| Change orders | Hourly | $[___]/h [HYP] |

Payment terms: [50% on SOW signature, 50% on D3] / [Net 30]. Prices exclude taxes.

## 7. Assumptions
Scans are reconstructed, artifact-free and consistent within the study. **Pre-contract feasibility gate:** before this SOW is signed, Provider runs the measurement-support advisor on representative scans or the scan protocol supplied by the Customer (material, timepoints, scanner protocol, noise, availability of empty-defect controls) and states in Annex A which endpoints are expected to be supported, conditional or not supported. Whether graft and new bone can be separated is confirmed per scan during D1 (material, scanner protocol, noise, availability of day-0 scans or empty-defect controls). **If an endpoint is assessed as not supported** — in D1 or, exceptionally, after analysis (e.g. unexpected artefacts, metal hardware) — Provider reports it as "not measured" with the reason and reports total mineral volume instead; Customer may (a) accept the reduced endpoint set at a [__]% fee reduction for the affected endpoints, (b) commission a material characterisation or histology-referenced extension by change order, or (c) terminate the affected part of the study with fees limited to work performed. Provider will not deliver a numeric value for an endpoint it has assessed as not supported.

## 8. Data handling
Covered by [DPA/Confidentiality terms]. Retention: [founder decision #14 in `FOUNDER_DECISIONS.md`: either deletion [90] days after D3 with a certificate, or return of a full archive package (scans, masks, report, audit-trail export) and deletion; must match `docs/quality/DATA_RETENTION_POLICY.md`]. GLP archiving is not offered.

## 9. Limitations
Results are for preclinical research use. Provider does not guarantee any regulatory outcome. Software version [x.y.z] and its validation status will be stated in the report.

**Signatures:** Customer ____________ Provider ____________

### Annex A: Analysis protocol (to be completed jointly)
Model, ROI geometry, thresholds/segmentation method, class definitions, parameter list, QC criteria, blinding.

### Annex B: Optional statistics
