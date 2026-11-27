# OsteoQuant: Prospect Database for the DefectFill Report

Prepared 2026-11-27. Status: desk research only. OsteoQuant has no customers, has done no interviews and has not validated anything on real graft data. Every fit score below is a hypothesis about who is most likely to have the problem. None of it shows that anyone will buy.

Data file: `prospects.csv`, 103 organizations, columns as specified. The raw API pulls are in `raw/`.

## Evidence labels (used in every business file)

| Label | Meaning |
|---|---|
| [V] | Verified this session from a primary source: an openFDA or NIH RePORTER API record, or a page fetched or resolved on 2026-11-27 |
| [CC] | Cross-checked: two or more independent secondary sources agree |
| [RF] | Reported fact from one secondary source (news, press release, search summary), not independently confirmed |
| [AE] | Analyst assumption or estimate |
| [INF] | Inference drawn from the evidence |
| [HYP] | Hypothesis to be tested, e.g. prices, willingness to pay, pain points |
| [UNR] | Unverified or unresolved, including prior knowledge not re-checked this session |

## Method

1. **Product-code discovery [V].** I searched the openFDA classification endpoint by device name ("bone void", "bone grafting", "intervertebral", "osteoinduction", "calcium", "barrier intraoral") and saved each code's classification record in `raw/classification/`. The codes used:

   | Code | Device name (openFDA) | Class | Reg. | Group |
   |---|---|---|---|---|
   | MQV | Filler, Bone Void, Calcium Compound | 2 | 888.3045 | Ortho bone void filler |
   | MBP | Filler, Bone Void, Osteoinduction (w/o human growth factor) (DBM-type) | 2 | 888.3045 | Ortho BVF |
   | QRR | Filler, Bone Void, Calcium Compound containing single approved aminoglycoside | 2 | 888.3046 | Ortho BVF |
   | PJN | Filler, Bone Void, Non-Alterable Compound for Cranioplasty | 2 | 882.5330 | Ortho/CMF |
   | OIS, QCG | Calcium-salt drillable BVF; BVF for bone marrow lesions | 2 / N | | No 510(k)s since 2016 |
   | LYC / NPM / NUN | Dental bone grafting material: synthetic / animal / human source | 2 | 872.3930 | Dental graft (NUN: none since 2016) |
   | NPZ | Dental bone grafting material with biologic component (PMA) | 3 | | Dental biologic |
   | NPK / NPL | Intraoral barrier: synthetic / animal source | 2 | 872.3930 | Dental GBR membranes |
   | MAX / ODP / PHM / OVD / OVE | Intervertebral fusion device with bone graft (lumbar/cervical/thoracic) and with integrated fixation | 2 | 888.3080 | Spine fusion |
   | NOX, MPW, NEK (PMA) | Synthetic peptide / rhBMP-2 fillers | 3 | | Biologic PMAs |
   | MBS | Filler, Bone Void, Non-Osteoinduction (PMA, historic) | 3 | | Historic only (latest 2005) |

   Calcium sulfate products have no code of their own. They are cleared under MQV (e.g. Synthecure, K250141) [V]. Human-tissue DBM and allograft are mostly regulated as HCT/Ps, not 510(k)s [INF], so MTF, AlloSource and LifeNet were added by hand.
2. **510(k) pull [V].** I queried `device/510k.json?search=product_code:X+AND+decision_date:[20160101+TO+20261127]` with pagination. That returned 1,232 records, saved as `raw/510k/*.json`, flattened in `raw/510k_flat_since2016.json`, and aggregated by normalized applicant in `raw/applicants_aggregated.csv`, which has 333 normalized applicants: 101 in graft/dental codes and 244–248 in spine codes. openFDA `last_updated` was 2026-11-16. Name normalization is imperfect. Variants such as "Kuros Biosciences B.V" / "Kuros Biosciences" were merged by hand in `prospects.csv`, and the raw unique-applicant counts overstate true companies by roughly 5–10% [AE].
3. **PMA pull [V].** Pulled for NOX, MPW, NEK, NPZ, MBS, OYR, OKD and OJZ into `raw/pma/`. Active applicants: Medtronic (INFUSE), Cerapedics (i-FACTOR/PearlMatrix), Lynch Biologics (GEM 21S).
4. **Status verification.** WebSearch confirmed ownership changes for ZimVie→ArchiMed, ZB Spine→Highridge/H.I.G., Collagen Matrix→Linden, NovaBone→Isto, Xtant/Surgalign/RTI, Anika divestitures and Cerapedics PearlMatrix. The search budget for this session (shared across agents) then ran out. Remaining statuses were checked by fetching each company's own homepage directly (HTTP status, title and redirect) and pulling contact-page and LinkedIn links from that page's HTML. Those redirects exposed several renames or acquisitions [V]: Collagen Matrix→Regenity, RTI Surgical→Evergen, Artoss→Biocomposites, Sirakoss→OssDsign, Datum Dental→Dentsply Sirona Regenerative, Sinclair Research→Altasciences, HistoTox Labs→Inotiv, Invicro→Perceptive, Dimension Inx→Dimension Bio. Facts I did not re-check are labelled [UNR] in the CSV, e.g. the Globus–NuVasive and Orthofix–SeaSpine mergers.
5. **Added by hand.** CROs, dental firms, tissue banks, imaging vendors and academic sites. Academic sites came from NIH RePORTER: FY2025/2026 projects whose abstracts mention micro-CT together with bone-defect, fracture, dental or spine terms (`raw/nih/microct_subset_FY*.csv`).
6. **Contacts.** Only company-level routes appear: a contact page, a general mailbox found on the organization's own site (e.g. info@), or a LinkedIn company page linked from that site. I recorded no personal names or personal emails. Where no route could be verified, the CSV says "Not verified".
7. **Excluded or not listed.** Medpace (clinical CRO, no bone preclinical evidence); American Preclinical Services, Alizée Pathology and Numira (their websites did not resolve, so status is unknown); about 230 spine-cage-only applicants (low fit for a graft-defect product, but kept in `raw/applicants_aggregated.csv` for a later spine-fusion module); most single-clearance overseas dental graft makers beyond the few listed as C.

## Fit rubric

- **A:** At least one of: a graft/dental/biologic clearance or PMA supplement since 2023, or a verified orthopedic GLP/non-GLP preclinical service. The organization must also be one where defect-fill, residual graft and new bone are central claims, and it must be small or mid-size enough that an R&D or study director could plausibly approve a pilot [INF].
- **B:** Relevant, but one of the following holds: enterprise procurement (long cycle), lower clearance cadence, ownership in transition, academic budget, an adjacent use case (fusion, mineralization), or the organization is a channel/partner rather than a buyer.
- **C:** Weak fit: no graft clearance since about 2021, soft-tissue-only products, mainly a distributor, overseas with no visible US channel, a competing tool vendor, or unknown status.

Result: **A = 17, B = 51, C = 35** (103 total).

| Segment | A | B | C | Total |
|---|---|---|---|---|
| Orthobiologic / spine / tissue / SBIR (P001–P051) | 11 | 26 | 14 | 51 |
| Dental regenerative (P052–P069) | 3 | 5 | 10 | 18 |
| Preclinical / imaging CROs (P070–P081) | 3 | 6 | 3 | 12 |
| Imaging and software vendors (P082–P086) | 0 | 1 | 4 | 5 |
| Academic cores / labs / VA (P087–P103) | 0 | 13 | 4 | 17 |

## Top 15, ranked

Ranking factors: (a) how clearly the business depends on separating new bone from residual graft; (b) recent regulatory activity, as a proxy for studies running now; (c) whether one person can say yes to a pilot; (d) channel multiplier effect; (e) how solid the evidence is.

| Rank | ID | Organization | Fit | Why it ranks here |
|---|---|---|---|---|
| 1 | P001 | Kuros Biosciences | A | Highest graft-code cadence of any SME: 13 MagnetOs clearances 2017–2025, latest K243474 (2025-05-23) [V]. The product thesis rests on new bone forming on a residual CaP surface, which is exactly the DefectFill three-class problem [INF]. Contact page verified [V]. |
| 2 | P052 | Geistlich Pharma | A | 16 dental/ortho clearances, latest K260364 (2026-06-02) [V]. Bio-Oss xenograft particles persist, so separating residual xenograft from new bone is the core question in its ridge and sinus studies [INF]. |
| 3 | P005 | Bone Solutions, Inc. | A | 6 Mg-based graft clearances, latest K262230 (2026-09-11) [V], so a programme is active now. Small company. Its contact route is unverified (domain error) [UNR]. |
| 4 | P003 | Prosidyan | A | FIBERGRAFT multi-product clearance K253147 (2025-10-22) [V]. Bioactive glass fibres are hard to threshold away from new bone [INF]. DePuy Synthes promotion deal (2018) [RF]. |
| 5 | P072 | Colorado State Univ. PSRL / TMI / ORC | A | GLP and non-GLP orthopedic device studies, confirmed on a fetched page [V]. Collaboration-friendly academic CRO that can supply a validation dataset and act as a route to sponsors [INF]. |
| 6 | P071 | AccelLAB | A | Fetched homepage lists dental, spine and long-bone orthopedics plus a GLP environment [V]. Mid-size device CRO, so a white-label or licence pilot is plausible [INF]. |
| 7 | P026 | Biocomposites (incl. ARTOSS NanoBone) | A | CaSO4/HA portfolio, latest K250521 (2025-04-07) [V]. New Novo Holdings/TA capital (2025) [RF] may fund evidence generation [INF]. |
| 8 | P023 | Cerapedics | A | PMA-class peptide graft. PearlMatrix approved June 2025 with a label expansion in 2026 [RF], and PMA records run to 2026-09-16 [V]. Needs rigorous bone-formation endpoints [INF]. |
| 9 | P054 | Regenity (ex-Collagen Matrix) | A | OEM for many dental and ortho brands: 10 clearances, latest 2024 [V]. One relationship could serve several brand owners' studies [INF]. |
| 10 | P006 | SurGenTec | A | 5 clearances, latest K251720 (2025-07-02) [V]. SME with a verified contact page. |
| 11 | P008 | Ventris Medical | A | 4 clearances in 2024–2025 [V], so development is active. Verified contact page. |
| 12 | P024 | Lynch Biologics | A | GEM 21S (rhPDGF-BB + β-TCP) PMA with supplements to 2026-08-03 [V]. Small, focused company whose clinical claim is defect fill [INF]. |
| 13 | P053 | Straumann Group / botiss | A | botiss Jason membrane K260132 (2026-11-08) [V]. Category leader, but enterprise buying slows a pilot [INF]. |
| 14 | P070 | NAMSA | A | Device CRO and a likely gateway to many SME graft makers [INF]. Scope not verified because the site blocked automated fetch [UNR]. Confirm in the interview before investing effort. |
| 15 | P007 | Biogennix | A | Synthetic CaP line with 5 clearances, latest 2024 [V]. Verified contact page. |

Also A, but outside the top 15: P002 BONESUPPORT (contact route unverified) and P025 OssDsign.

### What to do with this list (recommendation [INF])
- The first 10–12 discovery interviews should be split roughly 5 SME orthobiologic, 2 dental, 3 CRO and 2 academic core. This tests the two biggest unknowns: do manufacturers outsource the analysis or run it in-house, and do CROs see three-class segmentation as a bottleneck at all?
- Use the academic and local route (P091 UIUC Beckman, P087 Penn, P088 WashU) to get validation scans before making paid offers. The pilot template assumes access to retrospective scans with expert ground truth.
- Do not pitch large strategics (Medtronic, Stryker, Globus, Orthofix) until there is a validation report and at least one reference customer.

## Known limitations
- The web-search budget ran out partway through. Several ownership statuses come from prior knowledge or a homepage redirect only, and are marked [UNR] or [INF].
- openFDA counts cover one primary product code per 510(k). Combination products cleared under other codes, De Novos and HCT/P allografts are undercounted.
- A 510(k) clearance proves regulatory activity. It does not prove that micro-CT defect analysis was done or outsourced. That link is [INF] and has to be tested in interviews.
- Contact routes are company-level only. Several prospects (Bone Solutions, Orthocon, Etex, Elute, Purgo) had sites that did not resolve and need a manual check before any outreach.
- No one has been contacted.
