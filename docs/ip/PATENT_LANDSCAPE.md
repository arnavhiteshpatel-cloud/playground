# OsteoQuant: Preliminary Patent Landscape

**Prepared:** 2026-11-27. **Data file:** `docs/ip/patents.csv` (43 documents).

> **PRELIMINARY: NOT LEGAL ADVICE.** This is a technical screening by a non-attorney. It is not a freedom-to-operate (FTO) opinion, a validity opinion or a patentability opinion.
>
> - Claim summaries paraphrase **claim 1 as displayed on Google Patents** this session. Dependent claims, prosecution history, claim construction and later amendments were **not** reviewed.
> - "Status" and "expiry" are copied from Google Patents' displayed fields. Those fields are estimates and can be wrong (e.g. after term adjustments or fee lapses). They were not checked against USPTO Patent Center, EPO Register or national registers.
> - Every "FTO concern" level below is a **preliminary triage label for review by a registered patent attorney**. None of them is a conclusion that any OsteoQuant feature does or does not infringe.

## 1. Search method and access

| Database | Attempt | Result |
|---|---|---|
| Google Patents query endpoint (`/xhr/query`) | curl query | **Blocked** ("automated queries" page) |
| Google Patents individual documents (`/patent/<number>/en`) | curl + HTML parse (title, assignee, dates, status, claim 1), with back-off on rate limiting | **Worked** for 45 documents; one family member (US10178982B2) not retrieved |
| Google Patents via web search engine (`site:patents.google.com`) | ~25 thematic queries (below) | Used for discovery |
| USPTO PPUBS | web app loads; JSON search endpoints returned 404 | **Not usable programmatically**. Image PDFs (image-ppubs) downloaded for 5 patents but are scanned images with no text layer; Google Patents used for their text instead |
| Espacenet | HTTP 403 to automated client | **Not accessible** |
| Lens.org | Page is JavaScript-rendered; no results in HTML | **Not accessible** without a browser or API key |
| PatentsView API | Host unreachable through proxy | **Not accessible** |

**Consequences:**
- The search was **not exhaustive**. Discovery relied on a general web-search index over Google Patents, which favours English-language, older and highly-linked documents.
- Chinese, Korean and Japanese filings are under-sampled. One Chinese-language query was run.
- Recently published applications (2025–2026) may be missing.
- **Recommendation:** before any filing or product launch, a professional search with classification codes should be run in a commercial database. Suggested CPC classes (INF): G06T 7/11, G06T 7/136, G06T 7/30/33, G06T 2207/30008 (bone), G06T 2207/10081 (CT), A61B 6/505, G16H 30/40, G06F 21/64. The search should cover assignees Comet/ORS, Bruker, Scanco, Thermo Fisher/FEI, Revvity/PerkinElmer, ZEISS, Siemens, GE, Materialise, Synopsys, Hexagon and Nobel Biocare/Straumann/Dentsply.

**Query themes run (search-engine discovery):**
1. graft / new-bone / residual-graft segmentation in CT and micro-CT (EN; CN-language; KR-oriented)
2. deep-learning bone segmentation in micro-CT (incl. assignee-oriented: ORS, PerkinElmer, Scanco/Bruker)
3. longitudinal registration and bone healing / callus / follow-up quantification; time-lapse formation/resorption
4. uncertainty, abstention, deferral to human review, OOD gating, confidence-guided correction
5. bone-substitute resorption quantification; graft volume change on CBCT
6. automated bone-defect ROI detection; cortical shell / segmental gap
7. tamper-evident / hash-chained audit trail; signature bound to record hash; Part 11 imaging software
8. predicting segmentation feasibility/quality before or without ground truth
9. multi-material / dual-energy separability; material-specific segmentation parameters
10. synthetic phantom training data; histology-to-micro-CT registration; osseointegration / BIC quantification

## 2. Headline findings

1. **No document was found that claims three-class (new bone / residual graft / host bone) segmentation of micro-CT, or propagation of a day-0 graft footprint to classify later mineral.** Graft-vs-new-bone quantification appears in patents only as **experimental description inside composition or therapeutic patents**: WO2023135601A1, US12649019B2, US11524997B2, US20150150681A1 (seen in search snippets). These are prior art, not FTO risks for software.
2. **The closest active claim to OsteoQuant's longitudinal module is US9036899B2** (Nobel Biocare Services AG; KU Leuven inventor; priority 2010-06-11; expiry shown 2032-02-06) and its EP counterpart **EP2579778B1**. Claim 1 covers:
   - registering a first and second CT volume to one coordinate system;
   - selecting an ROI **by anatomical landmarks that define clipping planes**;
   - segmenting air/soft tissue in the ROI as "outside";
   - computing local bone volume in each scan and **subtracting** the volumes.

   **Preliminary concern: Medium.** OsteoQuant's ROI is an automatically detected cylinder, not landmark clipping planes. Its day-0 method labels later mineral per class by footprint overlap rather than subtracting total local-bone volumes. Its `class_volume_change` does compute per-timepoint volumes and a remaining-graft fraction. An attorney should map these elements before release of the longitudinal module, especially if a landmark/box ROI option is added.
3. **Uncertainty-driven review is crowded.**
   - Active claims: GE **US11972593B2** (expiry 2042-07-19), Sandia **US11379991B2** (expiry 2041-01-06), Novocure **US12322112B2**, Siemens **US12198337B2**, EchoNous **US20210350529A1** (family shown "Granted").
   - Expired prior art: Siemens US8682074B2, Oxipita US9317927B2, Canon US8160357B2.
   - GE's claim is the closest conceptually. It uses test-time augmentation, pixel-wise label variation and a threshold that prompts the user to confirm or edit. It is limited to an **automatically placed caliper** and the uncertainty of the caliper position. **Preliminary concern: Medium** if OsteoQuant adds auto-placed measurements with uncertainty prompts. **Low-Medium** for its current voxel abstention.
   - Sandia's claim relabels high-uncertainty voxels with the next-highest class after MC-dropout. OsteoQuant marks them "uncertain" instead. **Low-Medium.**
4. **Hash-chained audit logs are old, expired art.** IBM US8230228B2 and Oracle US7000118B1 are expired; Capitec WO2020104935A1 has ceased. Schneier & Kelsey, "Secure audit logs to support computer forensics", ACM TISSEC 1999 (doi:10.1145/317087.317089, verified via Crossref) is non-patent prior art. Binding a signature to the signed record is a **regulatory requirement** (21 CFR 11.70, signature/record linking: INF from the regulation's title; the eCFR page could not be fetched). **FTO concern: Low; patentability of OsteoQuant's audit design: low.**
5. **Predicting segmentation quality** has active art: SUNY **US11748877B2** (expiry 2038-09-29) uses a classifier on patch-level intensity/texture features to predict segmentation quality. It is relevant prior art to the "separability oracle as feasibility advisor" idea. **Preliminary concern: Low-Medium.** OsteoQuant's oracle is an analytic upper bound from class-conditional histograms, not a trained quality classifier.
6. **Preclinical micro-CT bone segmentation by a scanner vendor:** PerkinElmer/Revvity **US9999400B2** (expiry 2035-12-04) covers second-derivative splitting filters + region growing to separate individual bones. OsteoQuant does not do this. **Low.**

## 3. Risk-ranked table (preliminary; for attorney review)

| Rank | Document | Assignee | Status / expiry (Google Patents) | Why it matters | Preliminary FTO concern |
|---|---|---|---|---|---|
| 1 | **US9036899B2** / **EP2579778B1** | Nobel Biocare Services AG | Active / 2032-02-06 (US) | Registered pre/post CT, landmark ROI, bone-volume change | **Medium** |
| 2 | **US11972593B2** | GE Precision Healthcare | Active / 2042-07-19 | TTA uncertainty → threshold → prompt user to confirm/edit (caliper) | **Medium** (future auto-measurement features) |
| 3 | **US11379991B2** | NTESS (Sandia) | Active / 2041-01-06 | MC-dropout uncertainty → relabel above threshold | Low-Medium |
| 4 | **US11748877B2** | Research Foundation SUNY | Active / 2038-09-29 | Predicting segmentation quality from intensity/texture features | Low-Medium |
| 5 | US20210350529A1 | EchoNous | Application; family "Granted" | Gating predictions by ensemble uncertainty (ultrasound device in claim) | Low |
| 6 | US12322112B2 | Novocure | Active / 2043-07-22 | Ensemble divergence uncertainty visualisation (tumour) | Low |
| 7 | US12198337B2 | Siemens Healthineers | Active / 2043-01-21 | OOD detection gating (prostate MR) | Low |
| 8 | US9999400B2 | PerkinElmer / Revvity | Active / 2035-12-04 | Micro-CT individual bone splitting | Low |
| 9 | EP4645228A1 | Siemens Healthineers / Duke | Shown "Granted" | Learned realism enhancement of digital-phantom images with ground-truth preservation | Low now; **Medium if OsteoQuant adds learned sim-to-real translation** |
| 10 | US9025815B2, US20100135453A1 | GE | Active / granted family | Multi-material / dual-energy decomposition | Low now; review if dual-energy added |
| — | US11449993B2, US9646229B2, US10783639B2, US11645746B2, US20180116620A1, US20140161334A1, WO2022108912A1, WO2021174078A1, US20190251397A1 | various | Active, ceased or application | Bone/medical DL segmentation, QC/OOD, µCT-guided pathology | Low |
| — | US8634626B2, US8682074B2, US9317927B2, US8160357B2, US9495752B2, US7593762B2, US6021213A, US7356367B2, US8230228B2, US7000118B1, US7158692B2 | various | Expired | Useful **prior art** for invalidity and for limiting others' claims | None |
| — | WO2023135601A1, US12649019B2, US11524997B2, US20150293026A1, US20050251011A1, WO2020104935A1, WO2018229490A1, WO2020109630A1 | various | Ceased, abandoned or compositional | Prior art only | None for software |

## 4. Theme-by-theme notes

**4.1 Graft / new-bone segmentation in CT.**
- No software claim was found. Composition patents describe µCT quantification of new bone and residual graft in their examples. WO2023135601A1 (Ramot) reports, per the search summary of its figures, new bone vs residual graft particles in inner/middle/outer zones.
- Academic prior art is stronger than patent prior art:
  - Beitlitum 2024 (doi:10.1038/s41598-024-54313-4): thresholds + manual refinement, coaxial regions.
  - Ganeshaaraj 2022 (doi:10.1109/EMBC48229.2022.9870828): CNN for scaffold/bone/pores.
  - Aboutaleb 2026 (doi:10.1007/s11517-026-03686-x): U-Net for scaffold ingrowth with the ΔBGF metric.

  All three were verified via Europe PMC/Crossref this session.

**4.2 DL bone segmentation in micro-CT.**
- Patents found are clinical (Siemens, Persimio, Univ. Iowa) or vendor rule-based (PerkinElmer US9999400B2).
- No ORS/Comet, Scanco or Bruker patent was surfaced. This is **absence in a limited search**, not evidence.

**4.3 Longitudinal registration / bone healing.**
- Active: Nobel Biocare US9036899B2/EP2579778B1.
- Expired: CUHK US8634626B2 (baseline/follow-up bone surface registration), SUNY US7356367B2.
- No callus-specific or time-lapse-formation/resorption patent was found. The method is in the academic literature (Schulte 2011, doi:10.1016/j.bone.2010.10.007; Wehrle 2019, doi:10.1038/s41598-019-53822-x; both verified).

**4.4 Uncertainty / abstention.** See finding 3. The pattern "estimate uncertainty → threshold → route to human" is claimed in several **narrow, application-specific** forms (caliper, ultrasound, tumour, prostate) and is widely published (Geifman & El-Yaniv, arXiv:1705.08500; Valindria et al., arXiv:1702.03407; both verified). Broad claims on it are unlikely to be available to anyone, OsteoQuant included (INF).

**4.5 Bone-substitute resorption quantification.**
- Clinical CBCT/CT studies quantify graft resorption by registration and segmentation. Francis-Pester 2022 (doi:10.3390/jcm11195514, verified) models a "timepoint-0" graft virtually and compares it to follow-up.
- The only active method claim found is the Nobel Biocare family.

**4.6 Automated bone-defect ROI detection.**
- No defect-ROI patent was found. Expired Eli Lilly US6021213A (cortical region must surround marrow) and Siemens rib/cortex patents are prior art for cortical-shell logic.

**4.7 Audit trail for image analysis.** See finding 4. Siemens US7158692B2 (expired) and US20050251011A1 (abandoned) discuss Part 11 audit trails for quantitative imaging, which is direct prior art.

## 5. Recommended next steps (founder + attorney decisions)

1. **Attorney review (before release of the longitudinal module)** of US9036899B2/EP2579778B1 claim set and prosecution history; obtain a written FTO view.
2. **Design notes, not legal conclusions:** record why OsteoQuant's design choices differ from the closest claims (cylinder ROI vs landmark clipping planes; per-class footprint labelling; abstention vs relabelling; no auto-caliper). This helps the attorney; it does not establish non-infringement.
3. **Professional search** in a commercial database (Derwent, PatBase, Orbit or Lens with API access) using the CPC classes in §1, for CN/KR/JP coverage and 2025–2026 publications.
4. **Watch list (quarterly):** new publications by Comet/ORS, Bruker, Scanco, Thermo Fisher, Revvity, ZEISS, GE, Siemens Healthineers with terms "graft", "bone substitute", "residual", "baseline scan", "uncertainty", "abstain".
