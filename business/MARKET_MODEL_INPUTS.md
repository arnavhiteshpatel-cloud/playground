# Bottom-Up Market Model Inputs: DefectFill Report

Prepared 2026-11-27. Counts from APIs are [V], with the source file named. Per-customer volumes, shares and prices are assumptions [AE] or hypotheses [HYP]. None of them has been validated in an interview yet. The **first 10–15 interviews should replace the [AE] rows**.

## 1. Regulatory-activity counts (openFDA, data last updated 2026-11-16) [V]
Source: `raw/510k/*.json` (paginated pulls, decision_date 2016-01-01..2026-11-27), `raw/counts/*_by_date.json` (all-time counts by date), and the summary `raw/510k_summary_by_group.json`.

### 1a. 510(k) clearances per year by code group [V]
| Year | Ortho BVF (MQV, MBP, QRR, PJN) | Dental graft (LYC, NPM) | Dental barrier (NPK, NPL) | Spine fusion (MAX, ODP, PHM, OVD, OVE) |
|---|---|---|---|---|
| 2016 | 8 | 3 | 4 | 110 |
| 2017 | 17 | 5 | 4 | 130 |
| 2018 | 23 | 2 | 1 | 111 |
| 2019 | 14 | 0 | 1 | 101 |
| 2020 | 15 | 6 | 2 | 97 |
| 2021 | 9 | 2 | 3 | 88 |
| 2022 | 10 | 2 | 4 | 77 |
| 2023 | 21 | 2 | 5 | 92 |
| 2024 | 30 | 3 | 3 | 66 |
| 2025 | 14 | 6 | 5 | 60 |
| 2026 (to 27 Nov; data to 16 Nov) | 6 | 6 | 3 | 61 |
| **Total 2016–2026** | **167** | **37** | **35** | **993** |
| Mean/yr 2016–2025 | 16.1 | 3.1 | 3.2 | 93.2 |

MQV alone: 494 clearances all-time, 162 since 2016. LYC: 231 all-time, but only 13 since 2016. Most synthetic dental graft clearances predate 2016 [V].

### 1b. Unique applicants (normalized names; overstates true companies by roughly 5–10% because of name variants [AE]) [V]
| Group | Unique applicants 2016–2026 | Active 2023–2026 |
|---|---|---|
| Ortho BVF | 68 | **41** |
| Dental graft | 23 | 12 |
| Dental barrier | 21 | 12 |
| All graft/dental | 101 | **60** |
| Spine fusion | 248 | **117** |

### 1c. PMA biologic bone grafts [V] (`raw/pma/`)
Active sponsors with supplements in 2026: **Medtronic** (INFUSE; MPW/NEK/NPZ, latest 2026-08-26), **Cerapedics** (i-FACTOR/PearlMatrix; NOX, latest 2026-09-16), **Lynch Biologics** (GEM 21S; NPZ, latest 2026-08-03). Historic: BioMimetic Therapeutics (AUGMENT, latest 2022), Ceramed (PepGen P-15, 2010).

### 1d. Caveats
One primary product code per 510(k) means combination products are undercounted. Human-tissue DBM and allograft (HCT/P) do not appear. Companies selling only outside the US (EU MDR, Asia) are not captured. A clearance signals that preclinical work happened. It does not prove that micro-CT defect analysis was done [INF].

## 2. Organization counts
| Input | Value | Label / source |
|---|---|---|
| Orthobiologic + dental graft companies with US clearance activity 2023–2026 | ~55–60 (60 normalized applicants) | [V] openFDA; [AE] dedup adjustment |
| A/B-fit manufacturers, tissue banks, SBIR and dental firms in `prospects.csv` | 45 | [INF] fit rubric |
| Tissue banks with allograft/DBM R&D (no 510(k)) | 3 listed (MTF, AlloSource, LifeNet); likely 5–10 US total | [V] websites; [AE] total |
| Preclinical CROs with evidence of bone/orthopedic services | 9 identified; 6 with bone/orthopedic or bone-histology scope confirmed on a fetched page (AccelLAB, CSU PSRL, CBSET, Pharmatest, Inotiv/HistoTox, Altasciences) | [V] fetched pages; NAMSA, Charles River, T3 Labs [UNR] |
| Total CROs in NA+EU offering bone-healing models | 10–25 | [AE] |
| Academic micro-CT cores serving musculoskeletal research (identified) | 5 (Penn PCMD, WashU MRC Core B, Rochester CMSR, IU ICMH, MGH S10) | [V] core pages / NIH S10 |

## 3. NIH RePORTER (academic demand) [V]
Source: `raw/nih/bone_repair_phrases_FY2025.json`, `..._FY2026.json`, `raw/nih/SUMMARY.json`, `raw/nih/microct_subset_FY*.csv`, `raw/nih/broad_word_counts.json`.

**Query:** advanced text search over title/terms/abstract for any of the phrases "bone defect(s)", "critical-size", "critical size defect", "calvarial defect(s)", "segmental defect", "fracture healing", "fracture repair", "nonunion", "non-union", "bone regeneration", "bone graft(s)", "spinal fusion", "alveolar ridge", "alveolar bone", "osseointegration", "bone substitute", "bone repair". The micro-CT subset was found by a local regex on the abstract (micro-CT / µCT / micro-computed tomography).

| Metric | FY2025 | FY2026 |
|---|---|---|
| Project-year records matching phrases | 376 | 343 |
| Unique core projects | 359 | 336 |
| Total award $ (matching records) | $166.3M | $146.6M |
| Unique organizations | 148 | 146 |
| **Core projects mentioning micro-CT in abstract** | **54** | **67** |
| …of which defect/graft-related | 18 | 21 |
| …fracture-healing-related | 19 | 19 |
| …dental/periodontal/osseointegration | 19 | 26 |
| …spine fusion | 4 | 6 |
| Organizations with micro-CT bone-repair projects | 45 | 49 |
| SBIR/STTR core projects (all / micro-CT) | 12 / 2 | 14 / 2 |

**Sensitivity (broad word-match, over-inclusive) [V]:** records containing all of the words "micro-computed tomography bone" = 334 (FY2025) and 334 (FY2026). "bone defect" (all words) = 1,465 / 1,244. "bone regeneration" = 627 / 564.

**Interpretation [INF]:** Abstracts often leave out methods, so the 54–67 phrase-plus-micro-CT projects are a **lower bound** on NIH-funded labs doing micro-CT bone-repair work. The ~334 broad matches are an **upper bound**. NIH covers US federally funded labs only. DoD (CDMRP), VA (partly included), NSF, foundation, industry-funded and non-US labs are excluded.

## 4. Per-customer volume assumptions [AE], to be replaced by interview data
| Segment | Studies per customer per year (low / mid / high) | Scans per study | GLP share | Basis |
|---|---|---|---|---|
| Ortho BVF manufacturer | 0.5 / 1.5 / 3 | 20–60 | 10–30% | [AE] ~1 clearance per active firm every 1–2 years (§1), each supported by 1–3 animal studies |
| Dental graft/membrane manufacturer | 0.5 / 1 / 2 | 16–40 | 10–20% | [AE] |
| Spine fusion company (graft-related studies) | 10% / 20% / 30% of firms × 1 study | 12–30 | 20–40% | [AE] most cage 510(k)s rely on mechanical testing, not animal fusion studies |
| PMA biologic sponsor | 1 / 2 / 4 | 30–100 | 50%+ | [AE] |
| CRO (bone-healing) | 5 / 15 / 40 qualifying studies | 20–60 | 30–60% | [AE] |
| Academic lab (NIH micro-CT bone-repair) | 1 / 2 / 3 | 10–40 | ~0% | [AE] |

## 5. Illustrative serviceable pool at hypothesis prices [HYP]
Price inputs (founder playbook, unvalidated): non-GLP study $12K, GLP study $25K, academic licence $4K/yr, CRO licence $40K/yr. Blended industry study price at a 20% GLP share = 0.8×12K + 0.2×25K = **$14.6K** [HYP].

| Segment | Count (source) | Volume assumption | Annual pool low / mid / high |
|---|---|---|---|
| Ortho BVF manufacturers | 41 active [V] | 0.5 / 1.5 / 3 studies | $0.30M / $0.90M / $1.80M |
| Dental graft + barrier | 24 active [V] | 0.5 / 1 / 2 | $0.18M / $0.35M / $0.70M |
| Spine fusion (graft-related) | 117 active [V] | 10 / 20 / 30% × 1 study | $0.17M / $0.34M / $0.51M |
| PMA biologic sponsors (at $25K) | 3 [V] | 1 / 2 / 4 | $0.08M / $0.15M / $0.30M |
| **Industry subtotal (per-study route)** | | | **$0.73M / $1.74M / $3.31M** |
| Academic licences | 49 / 100 / 250 labs [V lower bound; AE above] | 1 licence | $0.20M / $0.40M / $1.00M |
| **Total** | | | **≈ $0.9M / $2.1M / $4.3M per year** |
| *Alternative channel:* CRO enterprise licences | 10 / 15 / 25 CROs [AE] | 1 licence | $0.40M / $0.60M / $1.00M (largely the same studies as the industry rows; do not add) |

**Interpretation [INF]:**
- At the playbook prices, the US-visible serviceable pool for graft-defect reports alone is likely **low single-digit millions of dollars per year**.
- That supports a founder-scale services business or a wedge product. It does not support a venture-scale business on its own.
- Upside depends on: (a) higher study volumes than assumed; (b) adjacent modules (fracture callus, implant osseointegration, spine fusion mass, dental ridge); (c) non-US sponsors under EU MDR; (d) per-scan academic volume through cores; (e) a vendor or CRO licence that reaches the installed base.
- Interviews should check (a) first. If typical manufacturers run fewer than one qualifying study a year, the per-study model is unlikely to sustain the business.

## 5b. Pool recomputed at the 2026-11-27 price hypotheses [HYP]
At Base prices of $11K per non-GLP study (no GLP study priced) and $6K per academic licence, with the same counts and volumes as §5, the pool is:

| | Low | Mid | High |
|---|---|---|---|
| Industry per-study pool | $0.52M | $1.26M | $2.40M |
| Academic licences | $0.29M | $0.60M | $1.50M |
| **Total** | **$0.81M** | **$1.86M** | **$3.90M** per year |

Formulas are in the `Market check` sheet of `FINANCIAL_MODEL.xlsx`; the rationale is in `REVENUE_MODEL.md` §5d. Material characterisation and enterprise licences are excluded (characterisation is not sized; enterprise licences overlap the industry rows). The §5 conclusion is unchanged: low single-digit millions per year.

## 6. Inputs still missing (collect in interviews or pilots)
- [ ] Actual studies per year and scans per study by segment (§4)
- [ ] Share of studies where micro-CT analysis is outsourced vs in-house
- [ ] Current cost of analysis (internal hours × rate; outsourced line items)
- [ ] GLP share of studies
- [ ] Willingness-to-pay ranges (Van Westendorp) per segment
- [ ] Cost-to-serve per study, measured in the pilot (see `PRICING_EXPERIMENT.md` §4)
- [ ] Non-US sponsor count (EU MDR bone-graft manufacturers). The EUDAMED public data could be explored [UNR]

## 7. Raw data index (`raw/`)
| Path | Content |
|---|---|
| `classification/*.json` | openFDA classification records for 26 product codes |
| `510k/{CODE}_p{n}.json` | Paginated 510(k) pulls since 2016 for 17 codes |
| `510k_flat_since2016.json` | Flattened 1,232 records (code, K-number, applicant, date, device) |
| `applicants_aggregated.csv` | Applicant-level aggregation (counts, codes, latest decision, latest devices) |
| `510k_summary_by_group.json` | Per-group yearly counts and unique applicants |
| `counts/*_by_date.json` | openFDA `count=decision_date` results (all-time) per code |
| `pma/*.json` | PMA records for NOX, OYR, MPW, NEK, NPZ, OKD, OJZ, MBS |
| `nih/bone_repair_phrases_FY2025.json`, `…FY2026.json` | Full NIH RePORTER results incl. abstracts |
| `nih/microct_subset_FY*.csv` | Micro-CT-mentioning subset with category tags |
| `nih/SUMMARY.json`, `nih/broad_word_counts.json` | Summary metrics and sensitivity counts |
