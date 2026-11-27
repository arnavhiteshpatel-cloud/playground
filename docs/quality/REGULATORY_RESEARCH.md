# OsteoQuant — Regulatory & Quality Research Summary

| Field | Value |
|---|---|
| Document ID | OQ-QMS-RES-001 |
| Version | 0.1 (DRAFT) |
| Date | 2026-11-27 |
| Author | Quality-systems / regulatory specialist (drafted with AI assistance; requires human expert review) |

> **Status: DRAFT — not validated; not a claim of Part 11 compliance or GLP validation.**
> OsteoQuant is a non-clinical, non-GLP research prototype. Nothing in this document is legal advice.

## Evidence labels

| Label | Meaning |
|---|---|
| **[V]** | Verified on 2026-11-27 by fetching a primary (or official-government/standards-body) source; URL given. Quotes are short excerpts. |
| **[PK]** | Prior knowledge of the author; not re-fetched today. Should be checked before reliance. |
| **[UNR]** | Unresolved / could not be verified today (source blocked, paywalled, or only secondary sources found). |
| **[INF]** | Inference / interpretation by the author; not a statement found in a source. |

Access notes: `ecfr.gov` and `federalregister.gov` HTML pages redirected to a bot-block page. CFR text was therefore taken from the **GovInfo annual CFR edition (21 CFR revised as of April 1, 2024)**. Part 11 and Part 58 have not been substantively amended since that edition to the author's knowledge **[PK]**, and the Federal Register API returned **zero documents published on/after 2025-01-01 that affect 21 CFR 58** **[V]** (https://www.federalregister.gov/api/v1/documents.json?conditions[cfr][title]=21&conditions[cfr][part]=58&conditions[publication_date][gte]=2025-01-01). OECD's own site returned HTTP 403; OECD texts were read from copies hosted by the German GLP authority (BfR).

---

## 1. 21 CFR Part 11 — Electronic Records; Electronic Signatures

Source text: https://www.govinfo.gov/content/pkg/CFR-2024-title21-vol1/xml/CFR-2024-title21-vol1-part11.xml **[V]**

### 1.1 Scope
- §11.1(b): Part 11 "applies to records in electronic form that are created, modified, maintained, archived, retrieved, or transmitted, under any records requirements set forth in agency regulations." **[V]** for the opening words fetched; remainder of the quoted clause **[PK]** (excerpt; the paragraph also covers electronic records submitted under the FD&C Act and PHS Act, and excludes paper records merely transmitted electronically).
- §11.3(b)(4) "Closed system means an environment in which system access is controlled by persons who are responsible for the content of electronic records that are on the system." **[V]** (final words "that are on the system" **[PK]**) A multi-tenant hosted deployment operated by OsteoQuant (not by the customer who owns the records) may need to be evaluated against §11.30 (open systems) **[INF]**.

### 1.2 Key controls (§11.10, closed systems) **[V]**
| Para | Short excerpt |
|---|---|
| (a) | "Validation of systems to ensure accuracy, reliability, consistent intended performance, and the ability to discern invalid or altered records." |
| (b) | "The ability to generate accurate and complete copies of records in both human readable and electronic form…" |
| (c) | "Protection of records to enable their accurate and ready retrieval throughout the records retention period." |
| (d) | "Limiting system access to authorized individuals." |
| (e) | "Use of secure, computer-generated, time-stamped audit trails to independently record the date and time of operator entries and actions…"; changes "shall not obscure previously recorded information"; audit trail retained at least as long as the subject records. |
| (f) | Operational system checks to enforce permitted sequencing of steps and events. |
| (g) | Authority checks (only authorized individuals can use the system, sign, alter records, perform operations). |
| (h) | Device checks (validity of source of data input). |
| (i) | Persons have education, training, experience. |
| (j) | Written policies holding individuals accountable for actions under their e-signatures. |
| (k) | Controls over systems documentation (distribution, revision and change control with audit trail). |

Note: the fetch tool returned the opening words of each paragraph verbatim and summarised the rest; where a quote above runs beyond those opening words, the continuation reflects the author's knowledge of the (unchanged since 1997) text **[PK]** and should be checked against eCFR before external use.

Other sections: §11.30 open systems; §11.50 signature manifestations (printed name, date/time, meaning — e.g., review, approval, responsibility, authorship); §11.70 signature/record linking ("shall be linked to their respective electronic records" **[V]**, "…to ensure that the signatures cannot be excised, copied, or otherwise transferred…" **[PK]**); §11.100 general e-signature requirements (uniqueness; identity verification; certification to FDA **[PK]** for §11.100(c)); §11.200 e-signature components (two distinct identification components such as ID + password) **[PK]**; §11.300 "Controls for identification codes/passwords." **[V heading]**.

### 1.3 FDA Guidance "Part 11, Electronic Records; Electronic Signatures — Scope and Application" (2003; FDA page lists September 2003)
URL: https://www.fda.gov/regulatory-information/search-fda-guidance-documents/part-11-electronic-records-electronic-signatures-scope-and-application **[V]** (final, nonbinding; docket FDA-2003-D-0143)
- FDA "intends to interpret the scope of part 11 narrowly." **[V]**
- Enforcement discretion for specific Part 11 requirements on **validation, audit trails, record retention, record copying**, and for **legacy systems** (operational before Aug 20, 1997). **[V]**
- "We will enforce all predicate rule requirements, including predicate rule record and recordkeeping requirements." **[V]**
- Records required by predicate rules and kept electronically **in place of** paper are Part 11 records; records kept electronically but not required by a predicate rule are not; records kept in both paper and electronic form are Part 11 records if they are **relied on** to perform regulated activities. **[V]**
- The guidance recommends a justified, documented risk assessment as the basis for validation and audit trail decisions **[PK]**.

### 1.4 FDA Guidance "Electronic Systems, Electronic Records, and Electronic Signatures in Clinical Investigations: Questions and Answers" (final, October 2024)
URLs: https://www.fda.gov/regulatory-information/search-fda-guidance-documents/electronic-systems-electronic-records-and-electronic-signatures-clinical-investigations-questions ; Federal Register notice 89 FR (2 Oct 2024), https://www.govinfo.gov/content/pkg/FR-2024-10-02/html/2024-22562.htm **[V]**
- Final; docket FDA-2017-D-1105; finalizes the March 2023 draft; **supersedes** the May 2007 guidance "Computerized Systems Used in Clinical Investigations" **[V]**. It does not state that it supersedes the 2003 Scope and Application guidance; it "expand[s] upon" it **[V]**.
- Purpose includes expanding "recommendations on the risk-based approach to validation of electronic systems" **[V]**.
- Scope: clinical investigations of foods, medical products, tobacco products and new animal drugs **[V]**. It does **not** address nonclinical/GLP studies **[V — scope statement]**. Its risk-based thinking (e.g., IT service providers, cloud, validation proportional to risk) is a useful benchmark for OsteoQuant's design, but it is not directly applicable to preclinical animal imaging **[INF]**.

### 1.5 Does Part 11 apply to nonclinical GLP data?
- §11.1(b) applies Part 11 to electronic records kept "under any records requirements set forth in agency regulations" **[V]**; 21 CFR Part 58 is such a regulation (a predicate rule) **[INF]**.
- In FDA's 2016 GLP proposed rule, FDA stated: comments noted "that part 11 … is applicable to part 58 and therefore parts 11 and 58 should be consistent. We agree, and do not intend to duplicate in part 58 the requirements in part 11." **[V]** (https://www.govinfo.gov/content/pkg/FR-2016-08-24/html/2016-19875.htm)
- **Conclusion [INF]:** When OsteoQuant is used by a testing facility to create/maintain records required by Part 58 (raw data, derived data, reports) for a GLP study, those electronic records are Part 11 records, and validation for intended use is the **testing facility's** obligation (with supplier support). For OsteoQuant's current non-GLP research use, Part 11 does not legally apply, but it is the right design benchmark.

---

## 2. 21 CFR Part 58 — Good Laboratory Practice for Nonclinical Laboratory Studies

Source: https://www.govinfo.gov/content/pkg/CFR-2024-title21-vol1/xml/CFR-2024-title21-vol1-part58.xml and §58.3: https://www.govinfo.gov/content/pkg/CFR-2024-title21-vol1/xml/CFR-2024-title21-vol1-sec58-3.xml **[V]**

| Section | Relevance to OsteoQuant | Excerpt / summary |
|---|---|---|
| §58.1(a) Scope | Studies supporting FDA applications/permits (incl. devices) | "This part prescribes good laboratory practices for conducting nonclinical laboratory studies…" **[V]** |
| §58.3(d) Nonclinical laboratory study | Defines when GLP applies | Experiments "under laboratory conditions to determine their safety"; does **not** include "basic exploratory studies carried out to determine whether a test article has any potential utility…" **[V]** |
| §58.3(k) Raw data | Micro-CT projections/reconstructions, segmentation edits may be raw data | "…result of original observations and activities of a nonclinical laboratory study and are necessary for the reconstruction and evaluation of the report…"; may include "computer printouts, magnetic media" **[V]** |
| §58.35(b)(3) QAU | QA inspection of computerized processes | Inspect each study at intervals adequate to assure integrity **[V]** |
| §58.61 / §58.63 Equipment | Computerized systems are treated as equipment **[INF]**; must be "adequately tested, calibrated and/or standardized" | **[V]** |
| §58.81 SOPs | SOPs required; deviations authorized by study director | **[V]** |
| §58.120 Protocol | Statistical methods pre-specified | **[V]** |
| §58.130(e) Data entry | Changes "shall be made so as not to obscure the original entry, shall indicate the reason for such change," dated and identified | **[V]** |
| §58.185 Final report | Storage location of raw data/report; statistical methods | **[V]** |
| §58.190 Storage/retrieval | Archives "for orderly storage and expedient retrieval of all raw data"; "Only authorized personnel shall enter the archives." | **[V]** |
| §58.195(b) Retention | Shortest of: ≥2 yrs after FDA approval of the application; ≥5 yrs after submission of results in support of a research/marketing permit; otherwise ≥2 yrs after study completion/termination | **[V]** (paraphrase of (b)(1)–(3)) |

### 2.1 Status of FDA's proposed GLP amendments
- **2010** ANPRM; **24 Aug 2016** proposed rule "Good Laboratory Practice for Nonclinical Laboratory Studies" (81 FR 58342; docket FDA-2010-N-0548) proposing a "GLP Quality System", multisite-study provisions, explicit computerized-system language (e.g., proposed §58.61 "Equipment, including computerized systems…"), and an ALCOA data standard ("accurate, legible, contemporaneous, original, and attributable"). Comment period extended 31 Oct 2016. **[V]** (FR API docket listing: https://www.federalregister.gov/api/v1/documents.json?conditions[docket_id]=FDA-2010-N-0548 ; rule text: https://www.govinfo.gov/content/pkg/FR-2016-08-24/html/2016-19875.htm)
- **Unified Agenda, RIN 0910-AJ01**: Spring 2025 edition lists it as **Long-Term Action**; abstract says FDA is proposing to require "a modern quality system", add a hearing before disqualification (Part 16), and "simultaneously withdraw the 2016 proposed rule"; timetable "NPRM 08/00/2026". **[V]** https://www.reginfo.gov/public/do/eAgendaViewRule?pubId=202504&RIN=0910-AJ01
- The subsequent agenda edition (labelled "2026") lists **Proposed Rule Stage**, NPRM 08/00/2026. **[V]** https://www.reginfo.gov/public/do/eAgendaViewRule?pubId=202510&RIN=0910-AJ01
- As of 2026-11-27 the Federal Register API returns **no documents** for RIN 0910-AJ01 and none affecting 21 CFR 58 since 2025-01-01 **[V]** → **no new NPRM or final rule has been published; current Part 58 (1987/1989 text) remains in force** **[INF from V]**. A 2026 PRA information-collection notice for Part 58 (FR Doc 2026-08371, 30 Apr 2026) exists **[V — title/abstract via FR API]**.

---

## 3. OECD GLP

### 3.1 OECD Principles of GLP (1998; ENV/MC/CHEM(98)17) **[PK]**
Basis of the OECD Mutual Acceptance of Data (MAD) system; require test facility management, QA programme, SOPs, study plans, raw-data recording, archiving. Not fetched today. **[PK]**

### 3.2 OECD Series on GLP No. 17 — "Application of GLP Principles to Computerised Systems" (ENV/JM/MONO(2016)13)
Source: BfR-hosted copy dated 9 Nov 2022, "Cancels & replaces the same document of 22 April 2016": https://www.bfr.bund.de/cm/349/No17_Application-of-GLP-Principles-to-Computerised-Systems_2022.pdf **[V]**

Key points (paragraph numbers from the document) **[V]**:
- ¶1: "introduces a life cycle approach to the validation and operation of computerised systems. It emphasises risk assessment as the central element…"
- ¶5–6: validation of new systems should be prospective; retrospective validation not permitted (except changed scope / not-validated existing system).
- ¶13: "Decisions on the extent of validation and data integrity controls should be based on a documented rationale and documented risk assessment."
- ¶27: segregation — "analytical personnel should not be in control of the audit trail settings of the system they are" using (excerpt).
- ¶33: up-to-date inventory of GLP-relevant computerised systems.
- ¶34–39: written agreements and risk-based assessment of suppliers (incl. hosted/cloud services).
- ¶44–45: written change control across validation, operation, archiving, retirement; can use ISPE GAMP software categorisation.
- ¶51: validation deliverables may be limited to URS, validation plan, user acceptance testing and validation report if justified by risk assessment.
- ¶56–57: URS "of paramount importance"; should be traceable to further specifications and testing.
- ¶60: customised systems — development process quality must be assessed; source code access (e.g., escrow).
- ¶66–69: data migration and format conversion must preserve content, meaning, audit trail and e-signature links.
- ¶72: data entry accuracy checks; "uncontrolled use of spreadsheets" should be excluded.
- ¶73–78: backup, restorability verification, readability across software versions; software retained if needed to read data.
- ¶80: "Any change to electronic records must not obscure the original entry and be time and date stamped and traceable to the person who made the change."
- ¶81: personnel involved in a study "should not be authorised to change audit trail settings."
- ¶82: risk-based **audit trail review**, with QA involvement.
- ¶86: "Any GLP study result should be traceable to the relevant and validated system configuration…" (supports configuration snapshots).
- ¶89–90: periodic review; user access review "at least yearly".
- ¶98: "Administrator rights should not be given to persons with a potential interest in the data."
- ¶99–100: incident management linked to change control and affected studies.
- ¶102: e-signatures linked to record, time/date, signatory identity and meaning; ¶105: "Password re-entry should be considered as a minimum requirement for an electronic signature."; ¶106: a change to a signed record invalidates the signature.
- ¶108: electronic data approval functionality must be validated.
- ¶113: electronic archiving is an independent validated procedure; consider open, non-proprietary formats.
- ¶117: source code, validation, operation records held at least as long as study records.
- ¶118: no electronic data destroyed without management (and sponsor) authorisation.
- ¶119–122: business continuity and disaster recovery.
- ¶123: retirement phase planned and risk based.

### 3.3 OECD Series on GLP No. 22 — "GLP Data Integrity" (ENV/CBC/MONO(2021)26)
- Read from the BfR German working translation, which states the English text of **20 September 2021** is authoritative: https://www.bfr.bund.de/assets/02_Service/03_Downloads/OECD_GLP_Nr._22_final.pdf **[V]** (English original at one.oecd.org returned 403 → English wording **[UNR]**).
- Defines data integrity as the extent to which data are complete, consistent, accurate and trustworthy throughout the data life cycle; uses **ALCOA** (Attributable, Legible, Contemporaneous, Original, Accurate) and **ALCOA+** adding **Complete, Consistent, Enduring, Available** **[V — English attribute names appear in the translation]**.
- Calls for a risk-based approach to data governance considering data risk, criticality and life cycle; computerised systems should retain full audit trails showing all changes without obscuring originals, with reasons for changes recorded; contains a section on audit-trail review (§7.2) **[V — translated]**.
- The UK MHRA states the OECD document takes precedence over MHRA GXP DI guidance for UK GLP facilities **[UNR — secondary blog]**.

### 3.4 Other OECD documents
- No. 15 "Establishment and Control of Archives…" (referenced in No. 17 ¶109) **[V reference]**; No. 23 on QA and GLP exists **[UNR]**.

---

## 4. Data-integrity principles (ALCOA+)
| Attribute | OsteoQuant design implication **[INF]** |
|---|---|
| Attributable | Unique accounts; every action and output stamped with user ID |
| Legible | Human-readable exports of data, audit trail, reports |
| Contemporaneous | Server-generated UTC timestamps at time of action |
| Original | Immutable original files with SHA-256; corrections stored as new versions |
| Accurate | Verified algorithms, phantom tests, QC gating |
| Complete | No silent exclusions; all runs/reruns retained |
| Consistent | Hash-chained, sequenced audit trail; consistent units |
| Enduring | Backup, open formats, retention controls |
| Available | Retrieval and export throughout retention |

Sources: OECD No. 22 **[V]**; FDA 2016 GLP proposed rule (ALCOA) **[V]**; FDA "Data Integrity and Compliance With Drug CGMP: Q&A" (final, Dec 2018, docket FDA-2018-D-3984) https://www.fda.gov/regulatory-information/search-fda-guidance-documents/data-integrity-and-compliance-drug-cgmp-questions-and-answers **[V existence/status]**; its ALCOA wording ("attributable, legible, contemporaneously recorded, original or a true copy, and accurate") **[PK/UNR — not on the landing page fetched]**. The CGMP guidance does not apply to OsteoQuant; cited as a benchmark only **[INF]**.

---

## 5. GAMP 5 (Second Edition) and risk-based CSV
- ISPE GAMP 5 Guide, 2nd ed., "A Risk-Based Approach to Compliant GxP Computerized Systems", **July 2022** **[PK; publication confirmed via ISPE search results — UNR for full text (paywalled)]**.
- ISPE Pharmaceutical Engineering (Jan/Feb 2026) describes 2nd-ed. categories as infrastructure software, tools and IT services, standard system components, configured components, custom applications and components; categorisation applied to **components**, "the categories should be viewed as a continuum"; scale life-cycle activities by GxP impact, complexity and novelty. **[V]** https://ispe.org/pharmaceutical-engineering/january-february-2026/when-category-not-category
- Conventional numbering: Category 1 infrastructure; Category 3 standard (non-configured) products; Category 4 configured products; Category 5 custom applications; Category 2 (firmware) retired in GAMP 5 (2008) **[PK]**. 2nd ed. emphasises critical thinking, agile/iterative development, and has an appendix on AI/ML **[PK]**.
- **OsteoQuant classification [INF]:** custom application (Category 5) built on Category 1/3 components (OS, Python, NumPy/SciPy, PyTorch, SQLite, FastAPI). The ML segmentation model is a custom, high-novelty component requiring data-set governance and performance verification.

## 6. FDA Computer Software Assurance (CSA) guidance — status verified
- "Computer Software Assurance for Production and Quality **System** Software" — final guidance issued **24 Sept 2025** (docket FDA-2022-D-0795) after the Sept 2022 draft **[V via FR doc 2025-18468 listing in search; UNR for text]**.
- **Superseded** by "Computer Software Assurance for Production and Quality **Management** System Software", **final, February 2026** (content current as of 02/03/2026), docket FDA-2022-D-0795; "describes a risk-based approach to establish confidence in the automation used for production or quality management systems." **[V]** https://www.fda.gov/regulatory-information/search-fda-guidance-documents/computer-software-assurance-production-and-quality-management-system-software
- Scope is software used in device **production or the QMS**, not device software functions **[PK; consistent with the page]**. The renaming aligns with the QMSR **[INF]**.
- Relevance **[INF]:** not legally applicable to OsteoQuant itself; relevant if a device-manufacturer customer uses OsteoQuant to generate design-verification/validation evidence (that could make OsteoQuant "QMS software" from the customer's perspective — question for counsel). CSA's emphasis on unscripted/exploratory testing for lower-risk functions and scripted testing for high-risk functions is adopted in the Verification Plan.

## 7. QMSR / ISO 13485
- FDA's Quality Management System Regulation (21 CFR 820 amended; incorporates ISO 13485:2016 by reference) **effective 2 Feb 2026** **[UNR — from FDA pages surfaced in search; not fetched]**.
- ISO 13485:2016 is a QMS standard for medical-device organisations **[PK]**. **Relevance [INF]:** not required for a non-device research tool; a lightweight ISO 13485-aligned QMS (document control, CAPA, design controls, supplier control) would ease a later move into device-adjacent markets or supplier qualification by device customers.
- **ISO 10993** (biocompatibility) — **not relevant** to software **[PK]**.

## 8. Reporting standards (scientific)
- **Bouxsein ML, Boyd SK, Christiansen BA, Guldberg RE, Jepsen KJ, Müller R.** "Guidelines for assessment of bone microstructure in rodents using micro-computed tomography." *J Bone Miner Res* 2010;25(7):1468–1486; PMID 20533309; EQUATOR category "Animal pre-clinical research". **[V]** https://www.equator-network.org/reporting-guidelines/guidelines-for-assessment-of-bone-microstructure-in-rodents-using-micro-computed-tomography/ ; DOI 10.1002/jbmr.141 **[UNR — from secondary search]**.
  - Recommends standardized terminology/units, methods reporting (scanner, voxel size, energy, filtering, segmentation method, VOI definition), and minimal outcome sets (trabecular: BV/TV, Tb.N, Tb.Th, Tb.Sp; cortical: Tt.Ar, Ct.Ar, Ct.Ar/Tt.Ar, Ct.Th) **[UNR — from abstract via secondary sources; consistent with PK]**.
  - Bouxsein is commonly described as an ASBMR-endorsed guideline **[PK]**. It addresses rodent trabecular/cortical bone, **not** defect-specific 3-class (new bone / graft / host) quantification; OsteoQuant must define and document defect-specific metrics **[INF]**.
- ARRIVE 2.0 guidelines (animal research reporting, 2020) **[PK]** — relevant to blinding, randomisation, exclusions.

## 9. ASTM standards for later modules (titles only; texts paywalled)
| Designation | Title | Evidence |
|---|---|---|
| ASTM F2884-21 | Standard Guide for Pre-clinical in vivo Evaluation of Spinal Fusion | **[V]** https://store.astm.org/f2884-21.html — active; species rat→NHP; outcome measures include "radiographic, histologic, and CT imaging"; §4.4 recommends safety testing per 21 CFR 58 |
| ASTM F3207-17 | Standard Guide for in vivo Evaluation of Rabbit Lumbar Intertransverse Process Spinal Fusion Model | **[V listing]** |
| ASTM F2721-09(2023) | Standard Guide for Preclinical in vivo Evaluation in Critical-Size Segmental Bone Defects | **[V listing]** — highly relevant to defect module |
| ASTM F2529-13(2021) | Standard Guide for in vivo Evaluation of Osteoinductive Potential for Materials Containing Demineralized Bone (DBM) | **[V listing]** |
| ASTM F3259-17 | Standard Guide for Micro-computed Tomography of Tissue Engineered Scaffolds | **[V listing]** — scaffold (ex vivo/in vitro) characterization; current status (active/withdrawn) **[UNR]** |

Listing source: ASTM Volume 13.02 index, Sept 2025 (hosted by JSA): https://webdesk.jsa.or.jp/link/annualbook/astm25_1302.pdf **[V]**. No ASTM standard specifically for micro-CT analysis software for bone defects was found **[UNR]**. FDA device-specific guidance for bone void fillers: "Class II Special Controls Guidance Document: Resorbable Calcium Salt Bone Void Filler Device" (June 2, 2003), 21 CFR 888.3045 **[UNR — search only]**.

## 10. Is OsteoQuant a medical device?
- FD&C Act §201(h) device definition includes articles intended "for use in the diagnosis of disease or other conditions, or in the cure, mitigation, treatment, or prevention of disease, in man or other animals" and "does not include software functions excluded pursuant to section 520(o)." **[V]** https://www.fda.gov/medical-devices/classify-your-medical-device/how-determine-if-your-product-medical-device
- Animal devices: "The FDA does not require submission of a 510(k), PMA, or any pre-market approval for devices intended for animal use"; FDA retains authority over adulterated/misbranded animal devices. **[V]** https://www.fda.gov/animal-veterinary/animal-health-literacy/how-fda-regulates-animal-devices
- EU MDR 2017/745 device definition is limited to use "for human beings" **[PK]**.
- **Reasoning [INF]:** OsteoQuant's intended use is quantification of experimental endpoints in animal research specimens (often ex vivo), to evaluate test articles — not diagnosis/treatment of disease in a particular animal or human. It therefore does not meet the "intended use" element of §201(h) as currently labelled. Even if it were characterised as an animal device, no premarket submission is required. **Caveats:** (1) intended use is determined by labelling, promotional claims and circumstances of distribution — claims such as "assess fracture healing in patients", use on clinical CT, or veterinary clinical use would change the analysis; (2) data generated by OsteoQuant may support customers' device/drug submissions, which brings GLP and Part 11 obligations on the customer and validation expectations on the tool, but not device status; (3) a future clinical module would need a full SaMD analysis (FDA, EU MDR, IMDRF). Formal confirmation should come from regulatory counsel (see memo).

## 11. FDA guidance on device animal studies
- "General Considerations for Animal Studies Intended to Evaluate Medical Devices" — final, March 2023, docket FDA-2015-D-3419; covers facility selection, housing, records and reports **[V]** https://www.fda.gov/regulatory-information/search-fda-guidance-documents/general-considerations-animal-studies-intended-evaluate-medical-devices . Its statement that animal studies supporting device **safety** must comply with GLP, and that GLP applicability depends on facts and circumstances (Q-Sub recommended) **[UNR — from secondary summary, not on landing page]**.

## 12. Key take-aways for OsteoQuant [INF]
1. Today: research prototype; neither Part 11 nor Part 58 legally applies, and no device premarket pathway applies.
2. If customers use OsteoQuant in GLP safety studies or to generate data submitted to FDA, Part 58 + Part 11 apply to **their** records; they must validate for intended use (OECD No. 17 ¶51: URS, validation plan, UAT, report at minimum).
3. Technical controls planned (audit trail, RBAC, hashing, version locks) map well to §11.10(a)–(h) and OECD No. 17 §3; **procedural/organisational controls (SOP approval, training, e-signature policy and FDA certification, periodic review, QA independence, supplier agreements, archivist role) are missing**.
4. The FDA GLP quality-system rulemaking (RIN 0910-AJ01) is pending; monitor for an NPRM.
5. Adopt Bouxsein nomenclature and define defect-specific metrics with explicit operational definitions.

## Sources consulted (fetched 2026-11-27)
- 21 CFR Part 11 (CFR 2024 ed.): https://www.govinfo.gov/content/pkg/CFR-2024-title21-vol1/xml/CFR-2024-title21-vol1-part11.xml
- 21 CFR Part 58 (CFR 2024 ed.): https://www.govinfo.gov/content/pkg/CFR-2024-title21-vol1/xml/CFR-2024-title21-vol1-part58.xml
- 21 CFR 58.3: https://www.govinfo.gov/content/pkg/CFR-2024-title21-vol1/xml/CFR-2024-title21-vol1-sec58-3.xml
- 21 CFR 58.195 (eCFR renderer API): https://www.ecfr.gov/api/renderer/v1/content/enhanced/current/title-21?part=58&section=58.195
- FDA Part 11 Scope & Application: https://www.fda.gov/regulatory-information/search-fda-guidance-documents/part-11-electronic-records-electronic-signatures-scope-and-application
- FDA 2024 Clinical Investigations Q&A: https://www.fda.gov/regulatory-information/search-fda-guidance-documents/electronic-systems-electronic-records-and-electronic-signatures-clinical-investigations-questions ; https://www.govinfo.gov/content/pkg/FR-2024-10-02/html/2024-22562.htm
- 2016 GLP proposed rule: https://www.govinfo.gov/content/pkg/FR-2016-08-24/html/2016-19875.htm
- Unified Agenda RIN 0910-AJ01: https://www.reginfo.gov/public/do/eAgendaViewRule?pubId=202504&RIN=0910-AJ01 ; https://www.reginfo.gov/public/do/eAgendaViewRule?pubId=202510&RIN=0910-AJ01
- OECD No. 17: https://www.bfr.bund.de/cm/349/No17_Application-of-GLP-Principles-to-Computerised-Systems_2022.pdf
- OECD No. 22 (German working translation): https://www.bfr.bund.de/assets/02_Service/03_Downloads/OECD_GLP_Nr._22_final.pdf
- FDA CSA (Feb 2026): https://www.fda.gov/regulatory-information/search-fda-guidance-documents/computer-software-assurance-production-and-quality-management-system-software
- ISPE article on GAMP categories: https://ispe.org/pharmaceutical-engineering/january-february-2026/when-category-not-category
- FDA device definition: https://www.fda.gov/medical-devices/classify-your-medical-device/how-determine-if-your-product-medical-device
- FDA animal devices: https://www.fda.gov/animal-veterinary/animal-health-literacy/how-fda-regulates-animal-devices
- FDA Data Integrity Q&A: https://www.fda.gov/regulatory-information/search-fda-guidance-documents/data-integrity-and-compliance-drug-cgmp-questions-and-answers
- FDA device animal studies guidance: https://www.fda.gov/regulatory-information/search-fda-guidance-documents/general-considerations-animal-studies-intended-evaluate-medical-devices
- Bouxsein 2010 (EQUATOR): https://www.equator-network.org/reporting-guidelines/guidelines-for-assessment-of-bone-microstructure-in-rodents-using-micro-computed-tomography/
- ASTM F2884-21: https://store.astm.org/f2884-21.html ; ASTM Vol. 13.02 index: https://webdesk.jsa.or.jp/link/annualbook/astm25_1302.pdf
