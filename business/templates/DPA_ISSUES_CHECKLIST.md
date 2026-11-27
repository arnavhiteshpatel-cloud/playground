# Data Processing / Data Handling Agreement: Issues Checklist

> Issue list for counsel. This is not legal advice. Preclinical animal micro-CT data are usually **not personal data** [INF]. File metadata, though, can contain personal data (operator names, emails in DICOM headers), and customers will still expect contractual confidentiality and security terms. Decide early whether a full DPA is needed or whether a data-handling/confidentiality schedule is enough.

## 1. Is personal data involved?
- [ ] Do DICOM/ISQ headers or filenames contain operator names, user IDs, emails or institution staff identifiers?
- [ ] Will any human or cadaver specimens be analysed? (This would raise HIPAA, consent and IRB questions. Exclude from scope unless separately reviewed.)
- [ ] Will business contact data (names/emails of customer staff) be processed in the portal? This is personal data under GDPR/UK GDPR and some US state laws.
- [ ] EU/UK customers: identify the controller/processor roles and the GDPR Art. 28 terms. Choose an international-transfer mechanism (SCCs / UK IDTA / EU-US Data Privacy Framework status) [UNR: check current status at signing].

## 2. Confidentiality and trade secrets
- [ ] Definition of Confidential Information covers images, study design, graft composition and results
- [ ] Use restriction: data used only to perform the services
- [ ] **No training on customer data** by default. Any opt-in must be written and specific (scope, de-identification, model ownership)
- [ ] Aggregated or anonymized statistics: what may be used, if anything (benchmarking, publications)
- [ ] Sponsor/third-party data: CRO customers must confirm they have the sponsor's permission to share

## 3. Security
- [ ] Encryption in transit (TLS 1.2+) and at rest
- [ ] Access control (least privilege, MFA), with access logs kept
- [ ] Hosting location and sub-processors (cloud provider, region) listed and change-notification process defined
- [ ] Vulnerability management and backup policy, described to a level that matches a pre-revenue startup (no overclaiming)
- [ ] Customer security questionnaire: prepare honest standard answers (no SOC 2 / ISO 27001 certification exists today)

## 4. Incident handling
- [ ] Breach notification timeline (e.g. ≤72 h after awareness) and contact route
- [ ] Cooperation duties and cost allocation

## 5. Retention, return and deletion
- [ ] Default retention period after delivery (e.g. 90 days)
- [ ] GLP archiving exception: who archives raw data and the audit trail, where, and for how long (see the Quality Agreement)
- [ ] Deletion certificate on request
- [ ] Backups: deletion timing for backup copies

## 6. Audit and cooperation
- [ ] Customer audit rights (remote questionnaire vs on-site), with frequency and notice
- [ ] Regulator access (relevant for GLP)

## 7. Liability
- [ ] Liability cap for data incidents (often carved out of the general cap; counsel to advise)
- [ ] Insurance (cyber / professional E&O) once the entity exists

## 8. University context [UNR]
- [ ] Confirm that no University of Illinois systems, accounts or student-data rules are implicated if university computing resources are used. If they are, institutional data policies may apply.
