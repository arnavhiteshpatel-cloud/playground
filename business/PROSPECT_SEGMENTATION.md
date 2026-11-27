# Prospect Segmentation and Discovery Priorities (2026-11-27)

Built by `segment_prospects.py` from `prospects.csv` (103 organisations). Output: `prospect_segments.csv`.
**No organisation has been contacted.** A priority score estimates who is most likely to have the problem and to answer. It is not evidence of demand. Every input comes from fields already in `prospects.csv`, whose sources are listed per row. The only addition is the HSS micro-CT core, whose fee page was fetched on 2026-11-27 (https://www.hss.edu/research/core-facilities/micro-computed-tomography-core).

## 1. Segments
| Segment | IDs | n | Fit A / B / C | Pricing hypotheses it tests | Why it matters [INF] |
|---|---|---|---|---|---|
| **ORTHO**: orthobiologic, spine-graft and tissue companies | P001–P051 | 51 | 11 / 26 / 14 | H1 pilot, H2 study, H3 characterisation | 41 bone-void-filler applicants active 2023–26 [V openFDA]. Residual graft versus new bone is central to their 510(k) and PMA evidence |
| **DENTAL**: dental graft and membrane companies | P052–P069 | 18 | 3 / 5 / 10 | H1, H2, H3 | 12 dental-graft and 12 barrier applicants active [V]. Xenograft particles persist, so the three-class problem is acute |
| **CRO**: preclinical CROs | P070–P081 | 12 | 3 / 6 / 3 | H5 enterprise, H1, H3 | One CRO serves many sponsors. Six have bone/orthopaedic scope confirmed on a fetched page [V] |
| **CORE**: academic micro-CT cores | P087–P091, P094, P101 | 7 | 0 / 7 / 0 | H4 academic (core-wide) | Cores multiply reach across user labs. HSS publishes analysis fees [V] |
| **LAB**: academic and VA research labs | P092, P093, P095–P100, P102, P103 | 10 | 0 / 6 / 4 | H4 academic | 45–49 organisations with NIH micro-CT bone-repair projects [V]. Free substitutes exist |
| **CHANNEL**: imaging and software vendors | P082–P086 | 5 | 0 / 1 / 4 | none (partner or competitor) | Not buyers. No sales approach before validation; IP clearance first |

## 2. Priority score (transparent rubric)
| Component | Points | Source field |
|---|---|---|
| Fit A / B / C (rubric in `PROSPECTS.md`) | +3 / +2 / 0 | `fit` |
| Manufacturers only: 510(k) or PMA activity in 2025–26 / 2023–24 | +2 / +1 | `latest_510k`, `relevant_activity` |
| Company-level contact route verified on the organisation's own site | +1 | `public_contact_route`, `evidence` |
| Enterprise procurement (large company, or "enterprise" in the fit rationale) | −1 | `type`, `fit_rationale` |
| CROs: bone, orthopaedic or GLP scope on a fetched page [V] | +1 | `relevant_activity`, `evidence` |
| Cores and labs: an NIH micro-CT bone project on record [V] | +1 | `evidence` |
| Channel/competitor | set to 0, excluded from buyer waves | |

**Waves.**
- **Wave 1** is the first 10 conversations, filled by a segment quota: 4 ORTHO, 2 DENTAL, 2 CRO, 1 CORE, 1 LAB. The quota makes every pricing hypothesis meet its own buyer early. Within a segment, candidates are ranked by score, then by the existing top-15 rank in `PROSPECTS.md`, then by ID.
- **Wave 2:** score ≥4.
- **Wave 3:** the remaining A/B organisations.
- **Hold:** fit C, or channel.

| Segment | Wave 1 | Wave 2 | Wave 3 | Hold |
|---|---|---|---|---|
| ORTHO | 4 | 23 | 10 | 14 |
| DENTAL | 2 | 4 | 2 | 10 |
| CRO | 2 | 3 | 4 | 3 |
| CORE | 1 | 2 | 4 | 0 |
| LAB | 1 | 1 | 4 | 4 |
| CHANNEL | 0 | 0 | 0 | 5 |

## 3. Wave 1: first 10 discovery conversations
Roles come from the `decision_maker_role` column. **No individual is named.** Reach them only through the public, company-level route recorded in `prospects.csv`, and re-check that route on the day of contact.

| # | Segment | Organisation (ID) | Role to reach | Why first (facts from `prospects.csv`) | Primary card |
|---|---|---|---|---|---|
| 1 | ORTHO | Kuros Biosciences (P001) | Director of R&D or preclinical/translational research manager | 13 graft-code clearances 2017–25, latest K243474 (2025-05-23) [V]; verified contact page | S, then M |
| 2 | ORTHO | Biocomposites (P026) | Director of R&D or preclinical manager | CaSO4/HA portfolio, latest K250521 (2025-04-07) [V]; resorbing material [INF] | S, then M |
| 3 | ORTHO | Cerapedics (P023) | Preclinical/translational research manager | PMA supplements to 2026-09-16 [V]; peptide-enhanced graft needs bone-formation endpoints [INF] | S |
| 4 | ORTHO | SurGenTec (P006) | Director of R&D | 5 clearances, latest K251720 (2025-07-02) [V]; SME; verified contact page | S, then P |
| 5 | DENTAL | Geistlich Pharma (P052) | Head of clinical and scientific affairs / R&D biomaterials | 16 records, latest K260364 (2026-06-02) [V]; persistent xenograft particles [INF] | S, then M |
| 6 | DENTAL | Regenity (P054) | R&D biomaterials lead (OEM) | 10 records, latest K233203 (2024-05-01) [V]; OEM for several brands, so one relationship reaches many studies [INF] | M, then S |
| 7 | CRO | Colorado State Univ. PSRL / TMI / ORC (P072) | Director of preclinical surgical research, or study director | GLP and non-GLP orthopaedic device studies on a fetched page [V]; academic CRO open to collaboration | E, then S |
| 8 | CRO | AccelLAB (P071) | Head of orthopaedic preclinical services, or head of imaging/pathology | Orthopaedic categories and a GLP environment on a fetched homepage [V] | E, then P |
| 9 | CORE | Penn Center for Musculoskeletal Disorders MicroCT Core (P087) | Core manager or core director | Penn: 2 (FY25) and 4 (FY26) NIH bone-repair micro-CT projects [V]; general core email on its site | A (core-wide) |
| 10 | LAB | University of Oregon Knight Campus bone-regeneration labs (P093) | PI or lab manager running a micro-CT bone-defect project | 2 FY2025 micro-CT bone projects [V]; verified institutional route | A |

**Alternates if a Wave 1 organisation is unreachable:**
- ORTHO: Ventris Medical (P008), Lynch Biologics (P024), Prosidyan (P003; contact route unverified)
- DENTAL: Straumann/botiss (P053; enterprise caveat)
- CRO: CBSET (P076), Inotiv (P074)
- CORE: Rochester (P089), Indiana (P090)
- LAB: UConn Health (P095)

**Not in early waves (rationale from `PROSPECTS.md`):**
- **Large strategics** (Medtronic, Stryker, Globus, J&J, Baxter, Dentsply Sirona, Envista): wait for a validation report and a reference customer.
- **Vendors** (Scanco, Bruker, Comet/Dragonfly, Rigaku, BIOQUANT) and the imaging CRO Perceptive: partner or competitor, not buyer. Wait for IP clearance first.
- **Beckman ITG (P091):** approach as a validation and scanning partner (`outreach/OUTREACH_EMAILS.md`), not as a buyer.

## 4. Segment rationale for sequencing [INF]
1. **Manufacturers first (6 of 10).** They are the buyers of the per-study service (H2) and characterisation (H3), and the market model's largest pool (`REVENUE_MODEL.md` §5d). The biggest unknown is whether they outsource analysis or keep it in-house; these interviews answer that.
2. **CROs second (2 of 10).** One enterprise licence (H5) at the Base price ($45K) carries as much revenue as about 4 studies at $11K. The open questions are whether CROs already have satisfactory in-house pipelines (`SCIENTIFIC_EVIDENCE.md` §7) and whether they would license or subcontract.
3. **Cores and labs (2 of 10).** Academic licences make up 32% of Base 2031 revenue, and their price is the second-largest sensitivity. Free tools are the main threat, so test H4 early with one core and one lab.

## 5. Limits
- Scores reuse desk-research labels. Several contact routes and ownership statuses are [UNR] (see `PROSPECTS.md` "Known limitations").
- A recent clearance proves regulatory activity, not that micro-CT defect analysis was done or outsourced [INF].
- Re-run `segment_prospects.py` after editing `prospects.csv`. The wave quota is in `WAVE1_QUOTA`.
