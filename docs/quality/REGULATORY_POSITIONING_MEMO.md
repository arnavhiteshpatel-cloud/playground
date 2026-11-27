# Memo — Regulatory Positioning of OsteoQuant

| Field | Value |
|---|---|
| Document ID | OQ-QMS-MEMO-001 |
| Version | 0.1 (DRAFT) |
| Date | 2026-11-27 |
| To | Founders; external device/regulatory counsel |
| From | Quality-systems / regulatory specialist |
| Re | Device status, Part 11 / GLP applicability, and questions for counsel |

> **Status: DRAFT — not validated; not a claim of Part 11 compliance or GLP validation.**
> This memo is not legal advice. Evidence labels: [V] verified primary source (see REGULATORY_RESEARCH.md for URLs), [PK] prior knowledge, [UNR] unresolved, [INF] inference.

## 1. Summary position (proposed)
1. **OsteoQuant is a research-use-only analysis tool for preclinical animal micro-CT; it is not intended to be, and as currently labelled likely is not, a medical device.** [INF]
2. **Part 11 and Part 58 do not apply to OsteoQuant's current research use**, but they **will apply to customers' records** if customers use OsteoQuant in GLP studies or to generate data submitted to FDA. In that case validation for intended use is the customer's (test facility's) obligation; OsteoQuant's role is a supplier providing a validation-support package. [INF, based on 21 CFR 11.1(b) [V] and FDA's 2016 statement that Part 11 "is applicable to part 58" [V]]
3. **OsteoQuant is not validated** and must not be marketed as "Part 11 compliant", "GLP compliant", or "validated". Acceptable phrasing (for counsel review): "designed with technical controls that support customers' Part 11 / GLP data-integrity programs; not validated."

## 2. Device analysis
- **Definition:** FD&C Act §201(h) covers articles intended "for use in the diagnosis of disease or other conditions, or in the cure, mitigation, treatment, or prevention of disease, in man or other animals", excluding software functions under §520(o). [V]
- **Intended use:** quantifying experimental endpoints (new bone, residual graft, host bone) in animal research specimens to evaluate test articles. No diagnosis or treatment decision for any patient or individual animal. [INF]
- **Animal devices:** even if characterised as an animal device, "The FDA does not require submission of a 510(k), PMA, or any pre-market approval for devices intended for animal use"; FDA retains authority over adulteration/misbranding. [V]
- **EU:** MDR 2017/745 device definition is limited to human use. [PK]
- **Caveats / triggers that could change the conclusion** [INF]:
  - Claims or features for human clinical CT/CBCT (e.g., assessing fusion or graft incorporation in patients) → potential SaMD (FDA, EU MDR, others); requires a full regulatory pathway analysis.
  - Veterinary clinical use (diagnosing individual animals) → animal-device considerations (no premarket, but adulteration/misbranding and labelling responsibilities).
  - Marketing materials suggesting clinical decision support; integrations into clinical PACS.
  - Customers using outputs in device submissions does not make the tool a device, but raises validation expectations.

## 3. GLP and Part 11 analysis
- GLP (21 CFR 58) covers nonclinical studies "to determine their safety"; excludes "basic exploratory studies" for potential utility. [V] Many bone-regeneration efficacy studies are non-GLP; safety studies supporting device/drug applications are GLP. FDA's 2023 device animal-study guidance reportedly states safety studies must comply with GLP and that applicability depends on facts and circumstances. [UNR]
- ASTM F2884-21 (spinal fusion) recommends safety testing per 21 CFR 58. [V]
- FDA's GLP quality-system rulemaking (RIN 0910-AJ01) plans to replace/withdraw the 2016 proposal; agenda timetable "NPRM 08/00/2026"; **no NPRM published as of 2026-11-27**. [V]
- OECD GLP No. 17 applies to computerised systems in OECD-GLP studies and allows reduced validation deliverables (URS, validation plan, UAT, report) if justified by risk assessment. [V]

## 4. Other frameworks
- **FDA CSA guidance** (final Feb 2026, superseding the Sept 2025 version) — applies to software used in device production/QMS; relevant if device-manufacturer customers treat OsteoQuant as QMS/design-control software. [V/INF]
- **QMSR / ISO 13485:2016** — not required for a non-device tool; an aligned lightweight QMS is recommended commercially. [UNR for QMSR date (2 Feb 2026); INF for recommendation]
- **ISO 10993** — not applicable to software. [PK]
- **Reporting standard:** Bouxsein et al. 2010 (JBMR) micro-CT guidelines [V]; ARRIVE 2.0 [PK]; ASTM F2721 (critical-size segmental defects), F2529 (DBM osteoinductivity), F3259-17 (micro-CT of scaffolds) for later modules [V listing; status UNR].

## 5. Recommended labelling and claims (for counsel review)
- "For research use only. Not for use in diagnostic procedures or clinical decision-making."
- "Not validated. Customers using OsteoQuant in GLP studies or regulatory submissions are responsible for validation for their intended use."
- Avoid: "FDA compliant", "Part 11 compliant", "GLP certified/validated", "clinically proven", "diagnoses".

## 6. Questions for device/regulatory counsel
1. Do our current and planned claims (incl. website, publications, pitch decks) keep OsteoQuant outside §201(h)? Which specific phrases create risk?
2. If we add a module for **clinical** CT (e.g., spinal fusion assessment in patients), what pathway applies (FDA SaMD classification, EU MDR rule 11), and can the research product be firewalled from it (separate product/labelling)?
3. Does **veterinary clinical** use by customers create any obligations for us (labelling, adulteration/misbranding), and should our terms prohibit it?
4. When a customer uses OsteoQuant in a **GLP study**, what is our legal/contractual role (supplier/service provider; "test site"?), and what must a **quality agreement** cover (OECD 17 ¶34–39; hosted services)?
5. Is a hosted, vendor-operated multi-tenant deployment an **open or closed system** under 21 CFR 11.3/11.30 from the customer's perspective? Which additional controls (e.g., encryption, digital signatures) are expected?
6. Can our electronic sign-off be used as a Part 11 e-signature by customers, and what do they need (11.100(c) certification, policies)? Should we disable "approval" semantics for unvalidated deployments?
7. If device-manufacturer customers use OsteoQuant outputs for **design verification/validation** evidence, does the FDA CSA guidance / QMSR make us a supplier subject to their purchasing controls (ISO 13485 §7.4), and what documentation should we provide?
8. Which marketing statements about data integrity are permissible without validation (e.g., "supports ALCOA+")?
9. For OECD-MAD customers (EU, UK, Japan), are there national GLP monitoring authority expectations for vendor-hosted systems or data stored outside the country?
10. What **record-retention and data-return** terms should our contracts include (customer obligations under 58.195 vs our hosting role)? Liability for data loss?
11. Should we pursue ISO 13485 or ISO 9001 / ISO 27001 certification for commercial credibility, and in what order?
12. Data-protection: user account data and any human data accidentally uploaded — required terms (GDPR/US state law), and how to block human data uploads?
13. Do ML-model training on customer data (federated or pooled) raise IP/confidentiality issues that affect GLP data ownership and archiving?
14. Export-control or animal-welfare (e.g., institutional/IACUC) considerations for hosted processing of animal-study data — any?
15. Status monitoring: should we comment on the forthcoming GLP NPRM (RIN 0910-AJ01) regarding computerised systems?

## 7. Decision requested
Approve the research-use-only positioning and labelling in §5, and engage counsel on questions 1, 2, 4, 5 and 7 before any customer pilot that could involve GLP or submission-supporting studies.
