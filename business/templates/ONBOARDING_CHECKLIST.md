# Customer Onboarding Checklist (TEMPLATE)

Use this for every pilot or paid study. Tick each item, add the date, and file the checklist with the study record.

## A. Commercial and legal (before any data moves)
- [ ] OsteoQuant legal entity exists and can sign (currently **not** incorporated)
- [ ] Mutual NDA signed
- [ ] MSA/Terms + SOW or Pilot Proposal signed by authorized signatories
- [ ] DPA signed, or written confirmation that no personal data will be shared (see `DPA_ISSUES_CHECKLIST.md`)
- [ ] Confirm the work is non-GLP (GLP-related work is not offered; see `QUALITY_AGREEMENT_ISSUES.md`)
- [ ] PO received / payment terms confirmed (paid work)
- [ ] Customer vendor-qualification forms completed (security questionnaire, W-9/tax forms, insurance certificates if required)
- [ ] Publication/anonymization consent recorded (pilots)

## B. Contacts and roles
- [ ] Customer technical contact (role)
- [ ] Customer approver for the analysis protocol (study director / R&D lead)
- [ ] Customer QA contact (GLP)
- [ ] OsteoQuant analyst + a second person as scientific reviewer assigned (authors cannot approve their own work)

## C. Data intake
- [ ] Secure transfer method agreed (encrypted upload, SFTP or customer-hosted share). No email attachments.
- [ ] File inventory received: scan IDs, groups (or blinded codes), time points
- [ ] Format confirmed (DICOM / ISQ / TIFF / other), voxel size, scanner model, kVp/µA/filter, reconstruction parameters, calibration phantom (HA) data
- [ ] Checksums verified on receipt and logged
- [ ] Data scanned for personal data (file headers, filenames). Remove or escalate if any found.
- [ ] Data stored in the access-controlled study folder. Access list recorded.

## D. Protocol set-up
- [ ] Defect model and defect dimensions documented
- [ ] Graft material(s) and expected radiodensity documented; contrast feasibility check done on 2–3 scans
- [ ] ROI definition agreed (geometry, anchoring landmarks)
- [ ] Class definitions agreed (new bone / residual graft / host bone), including edge cases
- [ ] Parameter list agreed (ASBMR nomenclature)
- [ ] Blinding arrangement agreed
- [ ] Analysis protocol (SOW Annex A) approved in writing by the customer

## E. Production
- [ ] Software version locked and recorded; validation status recorded
- [ ] Each scan: automated run → human review → corrections logged → reviewer sign-off
- [ ] Second-reader QC on [10–20%] of scans
- [ ] Deviations logged and reported

## F. Delivery and close-out
- [ ] Draft report delivered; comments received
- [ ] Final report, CSV, masks and audit log delivered via the secure route
- [ ] Customer acceptance recorded
- [ ] Invoice issued (paid work)
- [ ] Data retention/deletion executed per agreement; deletion certificate sent
- [ ] Debrief / feedback interview completed and coded (`INTERVIEW_CODING_SCHEME.md`)
