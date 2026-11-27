# Quality Agreement Issues Checklist (GLP-supporting analysis)

> Issue list to agree with the customer's QA and to review with a GLP/QA consultant and counsel. **OsteoQuant software is not currently validated, and OsteoQuant has no quality system.** Do not offer GLP-supporting work until the items marked ★ are in place. The regulatory references are named for orientation. Confirm their current versions before relying on them [UNR].

## 1. Regulatory frame
- [ ] Which regime applies: US FDA GLP (21 CFR Part 58), OECD GLP Principles, or both? Is the study GLP or non-GLP?
- [ ] Is OsteoQuant a **contributing scientist/test site**, a **service supplier**, or a **computerized-system vendor** to the test facility? Each role carries different responsibilities. Define the role explicitly.
- [ ] Electronic records and signatures: does 21 CFR Part 11 apply to the reports/audit trail delivered? What controls are expected?
- [ ] Guidance to consider: OECD GLP Advisory Document No. 17 (computerised systems); GAMP 5 risk-based approach; data-integrity (ALCOA+) expectations [UNR: confirm current editions]

## 2. Computerized-system validation ★
- [ ] Software classification and risk assessment
- [ ] Requirements specification (URS/FS) for ROI, segmentation, morphometry and reporting
- [ ] Verification and validation: test datasets, acceptance criteria, traceability matrix, validation report
- [ ] Version control and release management. The software version is locked per study
- [ ] Change control: how changes are assessed, validated and notified during a study
- [ ] Who supplies the validation evidence, and who performs the customer's own validation or acceptance

## 3. Data integrity and audit trail ★
- [ ] Definition of **raw data** for image analysis: original scans, ROI definitions, masks, reviewer edits, parameter outputs
- [ ] Audit trail: who, what, when and why for every human correction, and its immutability
- [ ] Time synchronization, user accounts (no shared logins), e-signature meaning
- [ ] Data transfer verification (checksums)

## 4. Personnel ★
- [ ] Training records for analysts and reviewers; CVs/job descriptions available for the study file
- [ ] Independence of the reviewer from the analyst

## 5. Study conduct
- [ ] Study-specific analysis plan approved by the Study Director before analysis
- [ ] Deviation handling and reporting timelines
- [ ] Communication lines: Study Director ↔ OsteoQuant lead; QA ↔ QA
- [ ] Contributions to the final study report (signed contributor report / statement)

## 6. QA and audits
- [ ] Customer QA audit rights (supplier audit, study-specific inspection), with notice and frequency
- [ ] Regulatory inspection support (FDA/monitoring authority access)
- [ ] OsteoQuant internal QA: if there is no independent QA function, the customer's QA must cover it; document how

## 7. Archiving
- [ ] Who archives raw data, the audit trail, the software version (or environment snapshot) and validation documents
- [ ] Retention period required by the regime and the sponsor
- [ ] Format longevity and retrieval on request; responsibilities if OsteoQuant ceases operations (escrow / transfer to the customer)

## 8. Subcontractors
- [ ] Cloud/hosting provider qualification; no further subcontracting without approval

## 9. Non-GLP studies
- [ ] A lighter "quality terms" schedule: version locking, audit trail, protocol approval and deviation log, without claiming GLP compliance
