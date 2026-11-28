# Project Atlas: Handoff for Independent Verification by ChatGPT Deep Research

**Prepared:** 28 November 2026, by Claude (Anthropic), the system that ran the Project Atlas research.
**Reader:** an independent research system that cannot see Atlas files. Everything you need is in this document. Evidence is given as URLs.
**Purpose:** verify, challenge and improve Claude's conclusions **without repeating the broad discovery campaign**. The highest-value work is in §14. The response format we want is in §15.

## How to read this document

- **Evidence levels** (used throughout, in brackets):
  - **A**: direct commercial or official evidence (statutes, agency data, SEC filings, procurement awards);
  - **B**: strong documentation (official price lists, partner agreements, FDD Item 19);
  - **C**: supporting industry evidence (trade surveys, government statistics);
  - **D**: indirect proxies (vendor blogs, job postings, third-party pricing pages, asking prices);
  - **E**: our assumptions or estimates.
- **"Op"** means operating profit before any owner pay (EBITDA basis). It is not owner cash.
- **"Peak funding"** is the maximum cumulative cash deficit. Unless marked "no draw", it includes a standardized owner draw of $4,000/month from month 13, 30% tax, and no external financing.
- **Stage E** figures come from the finalist playbook models. **Post-review** (or "REV") figures are Stage E models with the independent Stage F reviewer's corrected drivers.
- **FDC (founder-delivery charge):** the market cost of the delivery job the founder does unpaid (recruiter $6,900/month, bookkeeper $6,200, energy analyst $6,000, IT technician $7,500 in the REV models). "Y5 after FDC" subtracts it.
- **IDs** such as WS12-014 (opportunity) or F5-S006 (source) are Atlas internal identifiers. They are included only so your findings can be mapped back. They are not evidence; the URLs are.
- **Nothing has been tested in the market.** No customer, supplier, regulator or person was contacted. No money was spent and no account was created. All customer interest and supplier accessibility is documented from public pages or assumed, never confirmed.
- **Statutes:** ilga.gov returned HTTP 503 throughout the research window. Illinois statute text was therefore read from unofficial mirrors (FindLaw, Onecle, Cornell LII). Treat it as "A-text with C-currency": the wording is official but may not be current.

---

## 1. The founder: objectives, resources, constraints

**The question Atlas answers.** What is the strongest business this founder can start **from scratch today** that becomes a substantial, profitable, cash-generating operating company, and the first asset of a future diversified holding company?

**Objective function.**
- Success means sustainable free cash flow and owner wealth. Revenue, valuation and technical novelty do not count.
- In the founder's terms, a conventional business producing $500k/yr of sustainable FCF beats a speculative startup.

**Long-term wealth objective.**
- Build a diversified holding company over time.
- The first business should produce deployable cash and eventually not be capped by the founder's personal hours.
- Acquisitions are allowed **later** as a capital-allocation tool, but **not** as the initial entry.
- Milestones to assess: first profitable transaction, then $1k, $5k, $10k and $25k per month of operating profit, then $100k, $250k, $500k and $1M+ per year. Judge only which are *plausible* for a capable new entrant. Never manufacture a path to $1M.

**What counts.** Operating profit, FCF, distributable cash, ROIC, incremental return on growth capital, cash conversion, working capital, resilience, delegation, customer and supplier diversification, business value, risk-adjusted return and the opportunity cost of founder time. Revenue, profit and cash are kept separate, as are accounting profit and distributable cash.

**Resources.**
- Up to about **$100,000 of conditional personal backing**. This is **not a spending target**. The strong preference is to validate for hundreds of dollars, launch for low thousands, and deploy more only after demand is proven.
- Location: **Illinois**. Chicago-area access is assumed plausible; the exact city is unknown. The broader U.S. market is reachable.
- Background: technology, research and entrepreneurship.
- Heavy AI (Claude) access only until **5 December 2026**. After that, AI use must be ordinary and affordable. The business must not depend on unlimited AI.

**Constraints.**
- **Industry agnostic.** Examples in the founder's brief (loan brokerage, procurement, middlemen, distribution) are illustrations, not preferences.
- **No acquisition as entry.** Franchises are allowed, judged on owner economics after fees.
- **Not venture-style.** Software gets no bonus.
- **Not passive initially.** The founder will sell, negotiate, serve customers, work long hours, travel and hire. But the business must eventually not be capped by founder hours.
- **No professional licences held:** not a CPA, attorney, physician, PE, licensed contractor, insurance producer, MLO or real-estate broker.
- **Unknown founder facts:** age, credit history, veteran/minority/women-owned status, exact location, weekly hours available, existing network, and the terms of the conditional $100k.
- Separate from the founder's existing technology ventures, which are not reused.

---

## 2. Research methodology and funnel

**Design principles.**
- Breadth before depth.
- Founder-specific scoring: each idea judged as *this* founder would execute it.
- Owner cash as the objective function.
- **Shrinkage of weakly evidenced scores** toward the mean.
- Independent blind re-scoring.
- Adversarial reviewers who wrote none of what they reviewed.
- Every number tagged with an evidence level and a source.

**Scoring framework** (integer 1–10 per criterion; 5 = a typical small business):

| Criterion | Weight | Criterion | Weight |
|---|---|---|---|
| Sustainable FCF and owner wealth (`fcf`) | 18% | Competitive entry and defensibility (`entry`) | 10% |
| ROIC and capital efficiency (`roic`) | 15% | Delegation (`delegation`) | 8% |
| Customer accessibility for an unknown entrant (`access`) | 12% | Cash conversion and working capital (`cash`) | 5% |
| Scalability and reinvestment runway (`scale`) | 12% | Regulatory and practical feasibility (`feasibility`) | 5% |
| Resilience (`resilience`) | 10% | Durable, affordable AI leverage (`ai`) | 5% |

- **FCF anchors:** 5 ≈ $100–150k realistic year-3 to year-5 owner FCF; 7 ≈ $250–400k; 9 ≈ $750k+.
- **Evidence-adjusted composite** = 5 + (raw − 5) × k, where k = 1.00 (A), 0.95 (B), 0.85 (C), 0.70 (D), 0.55 (E).
- **Gates:**
  - G1 FAIL if more than $100k is at risk before first revenue;
  - G2 FAIL if it needs a licence the founder cannot get within ~12 months or work around;
  - G3 FAIL if predatory or high enforcement risk;
  - G4 WARN if there is no credible path to $100k/yr;
  - G5 WARN if it is venture-dependent;
  - G6 FAIL if acquisition is the only entry;
  - G7 WARN if capped at founder hours.

**Funnel with numbers:**

| Stage | What happened | Count |
|---|---|---|
| A: broad discovery | 18 parallel workstreams with web research | **630 records**, each with sources (630 Stage A source records; **1,618** source records in the final database across all stages) |
| Dedupe and bundling | 37 near-duplicates merged; 7 cross-stream bundles (SYN-001…007) synthesized | 593 distinct ideas + 7 bundles |
| B: structured screening | Gates, composite, **blind re-score of all 630** by 12 independent scorers in 13 packets | Dispositions: **74 to Stage C** (67 records + 7 bundles), 59 Stage-B-only, 444 deprioritized, 23 gate failures, 37 merged |
| C: industry investigations | Mechanism, competition, operator economics and failure research; ~280 new sources | 74 memos; median evidence-adjusted score fell ≈0.3 once real prices were found |
| D: commercial deep dives | Named Illinois prospects, suppliers, transaction examples, regulation, driver-based model | **25 concepts** in 9 themed batches |
| E: finalist playbooks | Standalone playbooks, draft (unsent) materials, standardized 24-month/5-year/10-year models | **11 finalists** |
| F: adversarial review | 6 independent review batches plus a cross-model audit; 72 new sources; ~120 citations re-opened; ~54 substantive corrections | All 11 weakened; 3 failed outright, 1 failed as primary |
| G/H: recommendation | Post-review ("REV") models for the top 4; capital-allocation and long-term-wealth analysis | 1 primary, 2 alternatives, 1 reserve |

**Calibration finding.**
- Authors scored their own ideas higher than blind scorers on **every** criterion. Mean raw composite: 4.81 (author) against 4.41 (blind). Blind scores were lower on 554 records (88%).
- Inflation by workstream ran from +0.17 (human capital) to +0.70 (insurance/payments).
- The most over-claimed criteria were AI leverage (4.15 → 3.41) and FCF (3.58 → 2.90).
- Stage B scores average the author and blind scores.
- The 7 bundles were **not** blind-scored.

**Modelling standard.**
- Driver-based: conversations × conversion → customers → revenue.
- Monthly for 24 months, annual to year 5, capital accumulation to year 10.
- Conservative, base and optimistic cases, with 17 standard stress tests.
- Every model is a live Excel workbook. All 40 workbooks (25 Stage D, 11 Stage E, 4 REV) were verified against an independent Python implementation with **0 mismatches**.
- Arithmetic is therefore not the main risk. **The inputs are.**

**Cross-model audit ("skeptic" rules H1–H9).** Applied only where a model was more favourable:
- H1: ≤15 founder sales conversations/month;
- H2: conversion ≤8%;
- H3: ramp ≥6 months;
- H4: churn ≥1.5%/month;
- H5: ≤1.0 referral per 100 active clients per month;
- H6: hired rep output ≤ founder output;
- H7: franchise-median job volumes;
- H8: year-6 growth ≤5%, incremental ROIC ≤60%, EV multiple ≤3.0× (2.38× sensitivity);
- H9: price growth ≤3%/yr.

The FDC was added on top.

---

## 3. Industries investigated and the landscape (630 → 74 → 25 → 11)

### 3.1 The 18 discovery workstreams

| WS | Domain | Records | To Stage C |
|---|---|---|---|
| WS01 | Credit intermediation and lending | 33 | 1 |
| WS02 | Insurance, payments, financial administration | 34 | 7 |
| WS03 | Industrial and manufacturing | 35 | 5 |
| WS04 | Healthcare, dental, veterinary, life-sciences operations | 36 | 6 |
| WS05 | Commercial and building services (mandated, recurring) | 36 | 5 |
| WS06 | Consumer products, brands, retail, food | 35 | 0 |
| WS07 | Logistics, transport, trade, liquidation | 36 | 3 |
| WS08 | Government and institutional procurement | 33 | 2 |
| WS09 | Publishing, education, information, media | 35 | 0 |
| WS10 | Construction, building materials, real-estate operations | 35 | 2 |
| WS11 | Agriculture, energy, utilities, environmental, waste | 35 | 5 |
| WS12 | Human capital and professional services | 34 | 2 |
| WS13 | Under-explored "quiet money" niches | 40 | 8 |
| WS14 | Mechanism-first (contingency recovery, consignment, aggregation) | 35 | 4 |
| WS15 | Regulation-driven and Illinois-specific demand | 34 | 2 |
| WS16 | Specialty B2B distribution and manufacturer representation | 34 | 2 |
| WS17 | Automotive, fleet, equipment aftermarket | 35 | 4 |
| WS18 | Local and consumer services | 35 | 9 |
| SYN | Cross-stream bundles | 7 | 7 |

Stage C also includes nine "judgment picks", so that each value-capture family (freight, customs, contingency audit, government, group purchasing, recruiting, sourcing brokerage, code-driven trades) had its best representative tested.

### 3.2 What the landscape showed

1. **The field is flat.**
   - Adjusted composites ran from 1.28 to 6.33 (mean 4.75). Only three records reached 6.0: commercial pest control (6.33), vertical bookkeeping (6.05) and a first-aid restocking route (6.02).
   - Gaps of 0.1–0.2 points are noise.
2. **No idea has an evidenced cold-start path to large owner cash.**
   - Blind scorers gave only 53 of 630 records an FCF score of ≥5 (≈$100–150k/yr) and **none a 7** (≈$250–400k).
   - No logistics, government, information or regulation-driven record reached FCF 5 under blind scoring.
3. **The strongest evidence mostly argues against ideas.**
   - Economics evidence: E 430 (68.3%), D 119 (18.9%), C 63 (10.0%), B 10 (1.6%), A 8 (1.3%).
   - Rules can be verified from a desk; private prices and new-entrant margins cannot.
   - 392 records (62%) list a price, fee or margin among their unanswered questions.

**Structurally attractive families** (most of Stage C):
- (a) **Mandated recurring inspection and compliance routes** with a cheap or hireable credential: pest control, extinguisher routes, crane inspection, construction stormwater, UST compliance.
- (b) **Consumable and equipment-as-a-service routes** to fragmented workplaces: first aid, dishmachine chemicals, restroom hygiene. Incumbent margins are high (Cintas First Aid & Safety 57.7% gross / 25.4% operating [A]), but an entrant will not earn them.
- (c) **Vertical back-office managed services:** vertical bookkeeping, niche payroll, prevailing-wage certified payroll, specialty billing, dental managed IT. These were the most stable under re-weighting: vertical bookkeeping stayed top-10 in all 1,000 random weight perturbations.
- (d) **Renewal-commission insurance agencies in one vertical.** A producer licence takes 20 hours per line and $215 [A]. Carrier and aggregator access is the binding barrier.
- (e) **Labour-led household services with franchise-disclosed revenue:** home care, lawn fertilization, junk removal.

**Structurally unattractive families:**
- consumer brands and marketplace selling (high gross, near-zero operating margins; Amazon fees; the end of de minimis; tariffs);
- owning production or a fleet;
- commodity distribution;
- transactional brokerage without recurrence (about 33k freight brokers);
- labour-arbitrage temp staffing (TrueBlue 0.7% adjusted EBITDA);
- pure information products (Chegg revenue −39% in 2025);
- government procurement as the primary channel.

**Cross-cutting findings:**
- Permanent state and local compliance cycles last, while federal deadline surges collapsed in 2025–26: CTA exemption, the FinCEN real-estate rule vacated, WOTC lapsed, ADA Title II deadlines moved, 25C/25D ended.
- Private-equity roll-ups cluster in the attractive families (APi, Rollins, Pye-Barker, GPRS). That is evidence of exit demand, not of entrant profitability.
- **In Illinois, who may legally do the work decides entry more than demand does.**
- Tariffs and de minimis changes are net hostile to import-dependent models.
- Illinois labour law (the amended Day and Temporary Labor Services Act's equal pay after 720 hours) pushes toward direct hire rather than temp staffing.
- AI commoditizes information and clerical work. It is a durable cost edge only where a licence, a seat-time mandate, physical service or filing liability anchors the deliverable.
- Freight is in a supply-driven squeeze.
- PJM capacity prices cleared at the cap: a tailwind for energy-advisory models.

### 3.3 Notable rejections (examples, with the decisive reason)

| Idea | Why rejected |
|---|---|
| Express car wash, self-storage, laundromat, child-care centre, Winmark resale franchise | G1 capital ($300k–$10M) |
| Merchant-cash-advance brokerage | G3: relies on renewals and stacking to distressed merchants |
| Hemp THC/CBD products | G3: federal redefinition bans >0.4 mg THC per container from about 2026-11-12 |
| Cook County property-tax appeals | G2: attorney-only Board of Review practice; fee-splitting barred |
| Unclaimed-property finder | 10% fee cap, Treasurer licence, bond |
| Freight brokerage with own authority | ~33k brokers; incumbent keeps ~13.5%; $75k security; float |
| Light-industrial temp staffing | 0.7% incumbent EBITDA; Illinois DTLSA equal pay and benefits |
| Amazon FBA private label, TikTok Shop | Platform dependence, fees, copycats, tariffs |
| Goosehead-type insurance franchise | 20% new / 50% renewal royalties; franchisor owns the policies |
| Transcription, answering services, exam prep | AI substitution |
| Handyman company | Owners keep 2–11% of revenue [B] |
| FinCEN, CTA, WOTC services | The mandate was removed |

### 3.4 How 74 became 25, and 25 became 11

- **Stage D selection:** all Stage C "advance" verdicts, plus "hold" records with adjusted score ≥5.25 not absorbed elsewhere, plus masonry restoration for its C-level permit data. Overlapping survivors were merged:
  - vertical bookkeeping, certified payroll and niche payroll → **SYN-006**;
  - trucking insurance and DOT compliance → **SYN-001**;
  - residential pest → commercial pest.
- **Stage E rule:** every Stage D finalist, plus reserves with base-case year-3 op ≥ ~$40k **and** either peak funding (no draw) ≤$90k or B-level evidence.
  - GPR scanning was kept as an exception (peak $161k) for founder fit and A/B price anchors.
  - Excluded reserves: stormwater, clinic janitorial, extinguisher route, lawn fertilization, pond management, home care and mobile fleet maintenance, for low year 3, high funding or margin fragility.

---
## 4. The 25 Stage D concepts

The economics column shows each Stage D driver model's **base case**: year-3 op, with peak funding where it was decisive. These are pre-Stage-F figures. For the 11 finalists, the post-review numbers in §5 supersede them.

| # | Concept (ID) | Stage D verdict | Post-D economics (base) | Decisive fact |
|---|---|---|---|---|
| 1 | Commercial pest control for Chicago food facilities (WS05-007) | Finalist | Y3 ≈$52k (Y5 $143k); peak ≈$36k | Official CDPH data list 1,416 live-pest food licences (256 in the SW cluster); founder-obtainable IDPH licence |
| 2 | Medical/dental clinic janitorial (WS05-026) | Reserve, not advanced | Y3 ≈$30k; payroll float ≈$83k at 50 sites | $17.05 Chicago wage floor leaves ~36% GM; −5 pts margin or +20% labour turns it negative |
| 3 | Extinguisher + emergency-lighting route (WS05-001) | Reserve (second licence for a pest company) | Y3 ≈$34k, founder-only | Illinois public price $3–7 per extinguisher; small account ~$330/yr including pull-through |
| 4 | Construction subcontractor back office: WIP bookkeeping + certified payroll (SYN-006) | Finalist (conditional) | Y3 ≈$101k (39 clients), Y5 ≈$188k; peak <$10k | Bookkeeping not CPA-restricted [A]; labour +20% → Y3 $49k |
| 5 | Construction stormwater (ILR10) inspections (WS11-021) | Reserve (SYN-006 adjacency) | Y3 ≈$54k; plateau $50–80k | Only Illinois price found was a $690/yr district oversight fee; 4,861 of 5,341 coverages show no agency inspection |
| 6 | Chicago masonry restoration (WS10-010) | Drop | Y3 ≈$65k; peak ≈$83–108k | Founder cannot perform or supervise; needs a City-exam supervising mason and W-2 crews |
| 7 | Insurance-led small-carrier compliance hub (SYN-001) | Finalist (conditional) | Y3 $20k (68 accounts), Y5 $172k; peak $36k / $92k with draw | Compliance-only contribution ~$109/month; profit depends on insurance attach (E) |
| 8 | Mobile preventive maintenance for service fleets (WS17-004) | Reserve | Y3 $71k, Y5 $104k; ~$100k before first revenue with an owned van | ~$7k/month loaded technician vs ~$21k/month revenue capacity; labour +20% → Y3 −$4k |
| 9 | Overhead crane and hoist inspection (WS03-012) | Drop | Y3 −$38k, Y5 −$42k; peak $541k | Inspection is cheap ($108–253 per crane on list) and self-inspection is legal |
| 10 | Private-pay non-medical home care (WS18-002) | Reserve | Y3 ≈$27k; $139–209k at risk | ~37% GM ($36/h median price vs ~$22–23/h loaded wage) |
| 11 | Managed IT + HIPAA for dental/vet practices (WS04-014) | Finalist | Y3 ≈$71k (32 practices × $700), Y5 ≈$133k; peak $22–35k | Price anchored at $399–749 by remote rivals |
| 12 | Specialty billing/RCM for therapy practices (WS04-010) | Drop | Y3 ≈$24k, flat to Y5 | One biller per ~4 clinics → ~$780/month contribution per client; EHR-bundled RCM at 3.9–6% |
| 13 | Pet cremation for veterinary clinics (WS13-028) | Drop | Y3 ≈$0, Y5 ≈$93k on ≈$344k funding | Gateway's "Trusted Journey" already runs 6 Illinois sites; 43% of Chicago vet locations group-owned; retort needs an IEPA permit |
| 14 | Lake, pond and stormwater-basin management (WS13-016) | Reserve | Y3 $61k; peak $68k (no draw) | Public pond work is bid as public works (prevailing wage, bonds); ~15 licensed rivals |
| 15 | Lawn fertilization subscription route (WS18-004) | Reserve | Y3 $48k; peak $74k / $141k with draw | CAC-bound against TruGreen, Spring-Green, Weed Man, Lawn Doctor; CAC ×2 → −$6k |
| 16 | Garage door repair (WS18-035) | Reserve → Stage E | Y3 ≈$95k on ≈$951k revenue | Supply is dealer-gated (Raynor $100k/yr minimum; SSC dealer-only); Precision covers every Chicagoland county |
| 17 | Junk removal (WS18-003) | Reserve → Stage E (only B-level economics in its batch) | Y3 ≈$132k on ≈$669k | Weak moat; ~1.3× asking multiples |
| 18 | Private utility locating and concrete GPR scanning (WS13-014) | Lead reserve → Stage E | Y3 ≈$112k; peak ≈$230k with draw | GSA CALC ceiling $124.69/h [B]; GPRS federal-award median $5,800 [A]; GPRS entrenched |
| 19 | Offshore (Philippine) staff for small CPA firms (WS12-012) | Finalist (conditional) | Y3 $231k on $1.33M revenue; peak $13k | An employer-of-record at $599–699/worker-month cuts seat contribution from ~38% to ~9% |
| 20 | Contingency direct-hire recruiting desk, controls/automation engineers (WS12-014) | Finalist (conditional; G7 WARN) | Y3 $171k (~13 placements); peak $11k; conservative $44k | 27 Illinois employers with live postings; no IDOL licence when employer-paid [A] |
| 21 | Retail deduction recovery for emerging CPG brands (WS14-008) | Drop | Y3 $149k on an E-level fee | Clairelist offers UNFI deduction recovery to small brands at $0 (68% of disputes won); SPS and Glimpse offer free audits or trials |
| 22 | Branded workwear/promo for trade contractors (WS16-006) | Reserve → Stage E | Y3 $44k ($91k without a rep); peak $45k | −5 pts GM cuts Y3 to ~$8k; SanMar Net 30 needs a personal guaranty |
| 23 | Online consignment auctions for business liquidations (WS07-023) | Drop | Y3 $6k (~$60k founder-only) | ~$2.9k contribution per $18k sale; 137 new Illinois auctioneer licences in 2026 |
| 24 | Cooling-tower and boiler water treatment (WS11-017) | Drop | Y3 ≈$24k; peak ≈$117k | A certified technologist needs 5 years' experience, so one must be paid from month 1; public bids are price wars |
| 25 | Energy cost management for >1,500 kW Illinois C&I users (SYN-004) | Finalist (conditional) | Y3 ≈$98k on ≈$30k peak (no draw) | Part 454 does not apply to deals for customers above 1,500 kW; PJM capacity cleared at the cap |

---

## 5. The 11 finalists: post-review profiles

**Summary of Stage E against post-review figures** (operating profit before owner pay; peak funding includes the draw unless noted):

| ID | Concept | Final status | Stage E Y3 / Y5 / peak | Post-review Y3 / Y5 / peak |
|---|---|---|---|---|
| WS12-014 | Controls/automation recruiting desk | **PRIMARY** | $170,012 / $259,002 / $12,836 | **$80,698 / $114,468 / $29,277** (no draw $15,180) |
| SYN-006 | Construction back office | **ALTERNATIVE 1** | $94,734 / $181,482 / $9,979 | **$49,662 / $82,563 / $11,540** |
| SYN-004 | Large C&I energy cost management | **ALTERNATIVE 2** | $98,323 / $120,332 / $62,155 | **$33,486 / $105,728 / ≈$122.0k** (no draw ≈$46.9k) |
| WS04-014 | Dental managed IT + HIPAA | **RESERVE** | $64,047 / $128,878 / $42,408 | **$37,459 / $94,859 / $69,661** (technician at 18 practices: Y5 $111,741, peak $38,761) |
| WS05-007 | Commercial pest control | Validation-only | $61.5k / $101k / $47k | ≈$43k / ≈$80k / ≈$79k |
| SYN-001 | Trucking compliance hub → insurance sub-producer | Validation-only | $48.3k / $177.5k / $69k | ≈$33.5k / ≈$102.1k / ≈$95k |
| WS13-014 | GPR scanning and utility locating | Validation-only | $106k / $175k / $51k | $49,869 / $86,098 / $110,459 ($145,622 at DSO 60) |
| WS12-012 | Offshore CPA-firm staff | Failed review | $54,249 / $373,388 / $23,540 | $57,548 / $78,364 / $63,125 |
| WS16-006 | Branded workwear | Failed review | $78k / $141k / $39k | ≈$47k / ≈$86k / ≈$98k |
| WS18-035 | Garage doors | Failed review | $65.8k / $67.0k / $93k | ≈$51k / ≈$70k (−$22k after technician charge) / ≈$110k |
| WS18-003 | Junk removal | Failed as primary | $49k / $83k / $142k | ≈$35k / ≈$49k / ≈$136k with no draw (≈$202k with draw) |

**Cross-model audit, harmonized Y5 op after FDC** (Stage E base with H1–H9; before the reviewers' corrections):
- WS12-012 $87k, WS12-014 $84k, SYN-004 $57k, WS04-014 $55k, WS18-003 $34k, SYN-006 $26k, WS18-035 $22k;
- WS16-006 −$8k, SYN-001 −$24k, WS13-014 −$32k, WS05-007 −$54k.
- **No finalist reaches $100k/yr.**

### 5.1 WS12-014: Employer-paid contingency recruiting desk for controls, automation and I&C engineers (PRIMARY)

- **Model.**
  - Place PLC/HMI, SCADA/DCS, robotics and motion-control engineers ($90–160k base) at Illinois integrators, mid-size process plants and engineering firms.
  - Fee 20% (floor 18%), invoiced on start, 90-day replacement guarantee.
  - Corrected base: ~3.7 placements in year 2, ~5.8 in year 3, ~7.4 in year 5. **Never hires** (trailing revenue never exceeds $20k/month).
- **Key evidence:**
  - **Licence exclusion:** "employment agency" excludes recruiters compensated solely by an employer, provided candidates are never charged, including for résumé preparation or "any other personal service" [A via mirror]: https://codes.findlaw.com/il/chapter-225-professionsoccupations-and-business-operations/il-st-sect-225-515-1-1/ ; IDOL FAQ [A]: https://labor.illinois.gov/faqs/private-employment-agency-faq.html
  - **Incumbent cyclicality:**
    - Robert Half permanent placement −57% in 2009 [A]: https://www.sec.gov/Archives/edgar/data/315213/000119312510034421/d10k.htm
    - −21.7% in 2023 on 24.1% fewer placements, average fee +2.4% [A]: https://www.sec.gov/Archives/edgar/data/315213/000031521324000011/rhi-20231231.htm
    - −9.8% in 2025, perm SG&A 96.9% of revenue [A]: https://www.sec.gov/Archives/edgar/data/315213/000031521326000006/rhi-20251231.htm
  - **Productivity benchmarks:**
    - PageGroup GP per fee earner £148.9k in 2025 [B]: https://investors.michaelpage.com/~/media/Files/P/page-v2/ir/result-reports/2026/Prelims-2025-combined-Final-v3.pdf
    - Top Echelon 2015 poll, modal 9–12 placements a year [D]: https://topechelon.com/blog/how-many-perm-placements-recruiters-made-in-2015/
    - Recruiterflow: top quartile 5.21 placements vs 1.38 for the rest [D]: https://recruiterflow.com/blog/revenue-per-recruiter-benchmark/
  - **Fee level:**
    - 20% most common North American direct-hire fee (SIA 2021, via secondary) [D]: https://www.secondtalent.com/resources/direct-hire-placement-fees/
    - Top Echelon 2018 engineering placements averaged 23% / $24,521 on $105,831 [D]: https://pinnacle.topechelon.com/average-fees-percentages-discipline-2018/
  - **Live demand:**
    - Ingredion Controls Systems Engineer, posted 2026-06-08, $84,400–112,533 [D]: https://ingredion.wd1.myworkdayjobs.com/IngredionCareers/job/Bedford-Park-IL/Controls-Systems-Engineer_Req-38726
    - Formic $120–145k [D]: https://boards-api.greenhouse.io/v1/boards/formic/jobs
    - Sargent & Lundy, 20 I&C listings [D]: https://careers-sargentlundy.icims.com/jobs/search?ss=1&searchKeyword=instrumentation
  - **Access barriers:**
    - Chamberlain posting tells agencies not to contact hiring managers [D]: https://chamberlain.wd1.myworkdayjobs.com/Chamberlain_Group/job/Elmhurst-IL/Engineer-3--Test-Automation-C00253_JR31990
    - LinkedIn Hiring Assistant in in-house hands [B]: https://news.linkedin.com/2025/hiring-assistant-globally-available
- **Weakest assumptions:**
  - conversation → signed fee agreement 22% (E);
  - agreement → placement 15% (E);
  - candidate supply for a founder with no network (E);
  - a credible technical screen after self-study (E);
  - no 2009-type downturn in years 1–3;
  - founder tolerance for daily cold outreach.
- **Decisive test:** ≈$600 over 60 days. ≥5 of 30 hiring managers sign ≥18% fee agreements about a specific vetted candidate.

### 5.2 SYN-006: Construction subcontractor back office (ALTERNATIVE 1)

- **Model.**
  - Monthly accrual close, job-cost report, quarterly surety-format WIP schedule and Illinois certified payroll for Chicagoland public-works subcontractors with $2–15M revenue.
  - Entry products: a $450 "WIP & Surety-Readiness Check", and certified payroll at $300/month per project.
  - Tiers: $750, $1,100 and $1,400/month.
  - ACH in advance.
- **Key evidence:**
  - **Bookkeeping not CPA-restricted** [A via mirror]: https://codes.findlaw.com/il/chapter-225-professionsoccupations-and-business-operations/il-st-sect-225-450-8-05.html
  - **Certified payroll mandate:** due monthly by the 15th [A]: https://codes.findlaw.com/il/chapter-820-employment/il-st-sect-820-130-5/ ; IDOL FAQ [A]: https://labor.illinois.gov/faqs/certifiedpayrollfaq.html
  - **SB1344 penalties** reach the filing agent [C]: https://www.amundsendavislaw.com/labor-employment-law-update/illinois-prevailing-wage-update-failure-to-timely-file-a-certified-payroll-individual-liability-debarment-financial-penalties ; bill status: https://ilga.gov/ftp/legislation/104/BillStatus/HTML/10400SB1344.html
  - **Surety WIP demand:**
    - TMHCC contract-bond packet [B]: https://www.tmhcc.com/en-us/-/media/tmhcc/surety-group/contractbonds/contractbondpacket.pdf
    - Western National "No C.P.A." program, capped at $1.5M, effective 2016 [B]: https://wnins.com/r3m0teProXyL0G1n/surety/Central%20Region/Sales%20Brochures/Central%20Region%20Rate%20Chart%20Contract%20Surety.pdf
  - **Price anchors:**
    - Wishup construction-trained bookkeeper from $999 [D]: https://www.wishup.co/industry/professional-services/bookkeeping-for-construction-company
    - Remote Books Online vendor bands $500–1,800 [D]: https://www.remotebooksonline.com/blog/construction-bookkeeping-wip-job-costing-pricing
  - **Labour cost:** Chicago bookkeeping-clerk mean $53,560 [C]: https://www.bls.gov/regions/midwest/news-release/2025/occupationalemploymentandwages_chicago_20250424.htm
  - **Buyers:** City of Chicago award records [A]: https://data.cityofchicago.org/resource/rsxa-ify5.json
- **Weakest assumptions:**
  - realized ARPC $950 (D/E);
  - 13 clients per bookkeeper (E);
  - an outside construction reviewer at $1,000/month (rate MISSING);
  - win rate 30% (E);
  - surety producers as a referral channel (E, contrary priors);
  - the founder's WIP competence (skill gap).
- **Decisive test:** ≈$1,000.
  - 8 surety-producer interviews (≥4 name recent WIP failures);
  - 20 owner calls;
  - ≥3 paid $450 checks in 60 days, ≥2 of them from cold outreach;
  - a paid skill gate: two clean WIPs reviewed by a construction CPA.

### 5.3 SYN-004: Energy cost management for >1,500 kW Illinois C&I users (ALTERNATIVE 2)

- **Model.**
  - Supplier-paid broker fees of ~1.0 mil on ~9 GWh exempt accounts (≈$750/month).
  - Licence-free services for any size: capacity-tag (PLC) management, demand-response (DR) referral and contingency bill audit.
  - Niche: refrigerated food businesses, independent grocers and independent hospitals in the ComEd zone.
- **Key evidence:**
  - **Statutory exemption:**
    - 220 ILCS 5/16-115C(b) excludes anyone procuring for, or selling to, a customer whose affiliated Illinois accounts exceed 1,500 kW aggregate billing demand [A via mirror]: https://law.onecle.com/illinois/220ilcs5/16-115C.html
    - Rule 83 Ill. Adm. Code 454.30(b)(5) [A]: https://www.law.cornell.edu/regulations/illinois/Ill-Admin-Code-tit-83-SS-454.30 ; definition of aggregate billing demand in 454.20: https://www.law.cornell.edu/regulations/illinois/Ill-Admin-Code-tit-83-SS-454.20
  - **Supplier onboarding and payment:**
    - ENGIE documents page asks for "broker/agent licenses and/or state approval documents" [B]: https://resources.engie-na.com/brokers-and-consultants/documents/
    - ENGIE remittance agreement: fee paid only after the customer pays, true-ups, ENGIE may contact the customer, the customer designates between brokers [B]: https://resources.engie-na.com/wp-content/uploads/2025/11/Broker-Agreement-ENGIE-Monthly-Payment-Remittance-Agreement-V.-10.2025.docx
  - **Capacity prices:**
    - 2028/29 cleared at the $325 cap [A]: https://www.pjm.com/-/media/DotCom/markets-ops/rpm/rpm-auction-info/2028-2029/2028-2029-bra-results-report.pdf
    - 2029/30 collar $181.91–$337.83 [A]: https://www.pjm.com/-/media/DotCom/markets-ops/rpm/rpm-auction-info/2029-2030/2029-2030-planning-period-parameters-for-base-residual-auction-report.pdf
  - **Market structure:** 93% of ComEd >1 MW usage is already on competitive suppliers; 392 licensed brokers [A]: https://icc.illinois.gov/downloads/public/icc-reports/ORMD%20Section%2020-110%20Report%202026%20Revised.pdf
  - **DR pass-through:** GridBeyond offered 100% revenue share plus a $73k/MW-yr floor [D]: https://environmentenergyleader.com/stories/pjm-demand-response-gridbeyond-introduces-73kmw-year-guaranteed-revenue-program,103582
- **Weakest assumptions:**
  - suppliers will pay an unlicensed exempt-only broker (MISSING, negative prior);
  - fee level in mils (D);
  - contract-expiry wait (E: 10 months average);
  - win rate 20% against incumbent brokers (E);
  - 7 qualified exempt-size conversations a month (E);
  - the content of P.A. 102-958 (unread).
- **Decisive test:** $0, about 3 weeks. ≥2 of ENGIE, Constellation and NRG confirm **in writing** that they will pay an unlicensed consultant serving only >1,500 kW customers, with mils and payment timing. Counsel then confirms the exemption. Run a customer-paid flat-fee offer in parallel.

### 5.4 WS04-014: Managed IT + HIPAA security for independent dental practices (RESERVE)

- **Model.** Prepaid monthly managed IT plus a HIPAA risk-analysis wedge for North Side Chicago practices.
- **Key evidence:**
  - Siotek: $399/month for ~10 workstations, free onboarding including risk assessment [B]: https://siotek.net/pricing ; Chicago marketing page [D]: https://siotek.net/dental-it/chicago-il
  - Chicago network-support median $73,340 [C]: https://www.onetonline.org/link/localwages/15-1231.00?st=IL
  - Systemic MSP risk: one ransomware event hit ~400 dental practices [C]: https://krebsonsecurity.com/2019/08/ransomware-bites-dental-data-backup-firm/
  - HIPAA Security Rule NPRM still not final [A]: https://www.federalregister.gov/api/v1/documents.json?conditions[regulation_id_number]=0945-AA22
- **Weakest assumptions:**
  - ARPC $650 against a $399 competitor;
  - proposal → win (the most sensitive driver);
  - insurability of business-associate liability.
- **Decisive test:** ≈$150. ≥3 paid risk-analysis deposits plus 2 monthly LOIs ≥$550. Walk away below $600.

### 5.5 WS05-007: Commercial pest control for Chicago food facilities (validation-only)

- **Key evidence:**
  - CDPH food-inspection data [A]: https://data.cityofchicago.org/resource/4ijn-s7e5.json
  - IDPH business licence $250 [A]: https://dph.illinois.gov/content/dam/soi/en/web/idph/forms/topics-services/environmental-health-protection/structural-pest-control/Commercial-Business-Application-2022.pdf ; technician exam $75 [A]: https://dph.illinois.gov/content/dam/soi/en/web/idph/files/forms/structural-pest-control-technician-application-generaluse-11032017.pdf
  - Public bid tabs $30–180/month per building [A]: https://wincoil.gov/images/departments/purchasing/awarded-bids-proposals/2018/bid_tab_joint_purchasing_pest_control_by_rpd_030818.pdf
  - EPA proposal to make most professional rodent baits restricted-use (still proposed) [A]: https://www.epa.gov/rodenticides/rodent-control-pesticide-safety-review
- **Weakest assumptions:**
  - Price: the $125 restaurant / $105 blended rate rests on a 2021 HomeAdvisor consumer guide that could not be reopened [D-]: https://webcf.waybackmachine.org/web/20211213221203/https://www.homeadvisor.com/cost/environmental-safety/hire-an-insect-control-service
  - 45 founder conversations a month: capping at 15 alone takes Y5 to $38k.
  - Displacement sales to only 112 licences citywide.
- **Decisive test:** a ≈$100–150 interview sprint. Pass = median price paid ≥$90/month and ≥25% switched or considered switching; kill = median <$70/month or <10% ever switched (an earlier summary conflated the kill and pass thresholds; corrected).

### 5.6 SYN-001: Trucking compliance hub leading to an insurance sub-producer role (validation-only)

- **Key evidence:**
  - FMCSA census, 3,166 established 3–20 power-unit Chicago carriers [A]: https://data.transportation.gov/resource/az4n-8mr2.json
  - Insurer shares (Progressive/Artisan 14.0%, Great West 13.1%, Northland 12.1%, GEICO 8.4%) [A]: https://data.transportation.gov/resource/qh9u-swkp.json
  - Anti-inducement statute 215 ILCS 5/151 [A via mirror]: https://law.onecle.com/illinois/215ilcs5/151.html ; commission rule §500-80: https://law.onecle.com/illinois/215ilcs5/500-80.html
- **Weakest assumptions:**
  - cohort-correct insurance attach (≈11% in Y3, not 21%);
  - a 40% sub-producer split (published splits 30–90% [D]): https://www.smartchoiceagents.com/tips/insurance-agency-producer-commission-structure
  - quote authority at renewal.
- **Legal flag:** the drafted "20% off when we also place your liability" offer is a likely illegal inducement.
- **Decisive test:** $0–100. A written sub-producer offer quoting ≥3 of the 7 dominant carriers at ≥40% split.

### 5.7 WS13-014: Private utility locating and concrete GPR scanning (validation-only)

- **Key evidence:**
  - GSA CALC subsurface-utility technician ceiling $124.69/h [B]: https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?keyword=subsurface
  - Published guide of ~$1,000–3,000/day; no half-day figure at the cited page [D]: https://www.sphengineering.com/news/gpr-cost
  - GC umbrella requirement of $5M for concrete and electrical trades [B]: https://www.weoneil.com/wp-content/uploads/2022/07/W.E.-ONeil-Insurance-Requirements.pdf
  - Winter excavation-ticket trough about 30% below April–October [A]: https://data.cityofchicago.org/resource/nphj-5zur.json
- **Weakest assumptions:**
  - ARPC $700 (E);
  - monthly rebooking;
  - competence: 2 days' training against GPRS's 4 weeks + 80 h + 4 weeks;
  - insurability.
- **Decisive test:** $0–200. 12+ project-manager interviews, a median half-day price ≥$550 (the review uses ≥$600) and ≥3 dated bookings.

### 5.8 WS12-012: Offshore Philippine accounting staff for CPA firms (FAILED)

- **Key evidence:**
  - Philippine Revised Corporation Code requires a resident treasurer and a Filipino citizen-resident corporate secretary [A]: https://lawphil.net/statutes/repacts/ra2019/ra_11232_2019.html
  - Compliant market prices about $1,963–2,100 [D]: https://www.vintti.com/blog/best-offshore-staffing-companies-for-accounting-firms-in-2026-18-reviewed-by-hiring-model
  - AICPA MAP offshoring survey [C]: https://www.journalofaccountancy.com/issues/2024/nov/offshoring-for-cpa-firms-the-hows-and-whys/
- **Why it failed:**
  - GM 27% on $2,250 seats;
  - the worst conservative case of all 11 (Y5 −$50,048; peak $455,972);
  - DO 174 labour-only-contracting exposure;
  - the most AI-targeted task set.
- **Disagreement preserved:** if salary asks are ≤$1,100 and prepaid acceptance is ≥$2,300, the Stage E base returns.

### 5.9 WS16-006: Branded workwear and promotional products for trade contractors (FAILED)

- **Key evidence:**
  - 65% of manufacturing end-buyers buy promo through e-commerce [C]: https://members.asicentral.com/media/0k0kmxtq/manufacturing-end-buyer.pdf
  - AGC members get exclusive Cintas discounts [C]: https://www.agc.org/member-benefits/cintas-uniforms-facility-services
  - SanMar credit requires a "continuing and irrevocable" personal guaranty [B]: https://info.sanmar.com/medias/sys_master/root/hde/h75/16478323081246/Credit%20Application%20SanMar/Credit-Application-SanMar.pdf
- **Why it failed:** the playbook's own desk test found 5–25% GM at 4imprint price parity (−12% on an ANSI tee), against a model at 30%.
- **Revival test ($0):** do Chicago contractors already pay ≥1.15× 4imprint?

### 5.10 WS18-035: Garage door repair (FAILED)

- **Key evidence:**
  - Raynor Chicago price page: most repairs $150–500, opener installed $250–600 [D]: https://raynordoor.com/blog/garage-door-repair-cost-in-chicago/
  - Precision FDD smallest-band median earned at $1,213/job (≈59 jobs/month) [B]: https://pub-22da695f2b6542a48e234bc59bc67d23.r2.dev/item19/324ef784-0ba1-4d3b-bf97-9207e0738196.pdf
  - ServiceTitan small-shop booking median ~30% [D]: https://www.servicetitan.com/toolbox/state-of-the-trades/trends/quarterly-industry-trends
  - Chicago Home Repair licence [A]: https://www.chicago.gov/city/en/sites/chicago-business-licensing/home/homerepair.html
- **Why it failed:** volume was back-solved from franchise revenue at half the franchise ticket. Year-5 profit is the founder's technician wage (−$22k after the charge).

### 5.11 WS18-003: Junk removal (FAILED as primary)

- **Key evidence:**
  - Junk King FDD: 166 units, median $435,663, third quartile $355,222 [B]: https://pub-22da695f2b6542a48e234bc59bc67d23.r2.dev/item19/bb80c3d0-cdc0-4e43-a659-28bed689b425.pdf
  - Chicago aggregator ticket ≈$246 [D]: https://homeguide.com/il/chicago/waste-and-junk-removal/
  - Box-truck insurance medians: auto $909/month, workers' comp $673/month [D]: https://www.insureon.com/trucking-business-insurance/box-trucks/cost
  - 1-800-GOT-JUNK Chicagoland holds 10 licensed trucks [A]: https://data.cityofchicago.org/resource/uupf-x98q.json
- **Why it failed:**
  - an unbranded plateau above the branded median;
  - peak funding with no draw ≈$136k;
  - GM-run corporate stores at College Hunks earn about 4% [B].

---
## 6. The recommendation and its reasons

### 6.1 Primary: WS12-014, the controls/automation/I&C contingency recruiting desk

**Framing.** A **2–3-year cash engine**, not the permanent core of the holding company. A formal month-24 decision follows: build a boutique (recruiters, then contract engineering staffing) or harvest the cash into a more durable asset. **Commit no capital before a 60-day, ≈$600 validation.**

**Why it wins:**
- It is **#1 in every variant** of the cross-model audit, including the unharmonized ranking. Its Stage E drivers were already benchmark-capped.
- Validation is the cheapest and fastest of any finalist.
- It has a clean statutory licence exclusion (no licence, bond or state forms).
- It has the best post-review cash (≈$81k Y3 / ≈$114k Y5) on ≤$30k at risk. It wins the two heaviest criteria, FCF (18%) and ROIC (15%).
- It is a "try a newcomer" offer: the employer pays nothing unless it hires.
- The founder's technical background is plausibly useful for screening.

**What it does not do:**
- It is founder-bound: the base never hires.
- It is the most cyclical line in staffing.
- Transfer value is low (~1.5–2× op).
- Its Y5 after FDC is only $21.3k (post-review base) and $0 (harmonized).

**Abandon at day 60** if any of these hold: fewer than 2 signed agreements; managers buy only through portals or MSPs; the founder dislikes the work. Stop before any hire if no fee of ≥$15k is collected by month 10.

### 6.2 Alternative 1 (durable-asset choice): SYN-006, the construction subcontractor back office

**For:**
- the lowest capital in the study (peak ≈$10–12k);
- mandated monthly demand;
- licence-free bookkeeping;
- public award records name every prime;
- recurring revenue with hireable roles and a sellable book.

**Against:**
- post-review Y3 ≈$50k and Y5 ≈$83k;
- D-level price evidence (~$950/month, unverified in Chicago);
- no construction-accounting track record, when the product is trust in accuracy;
- certified-payroll licensing rests on a statute that does not mention it;
- SB1344 agent liability;
- **Y5 after FDC −$1.2k, and −$63.3k harmonized.**

**Switch to it if** the primary's fee-agreement test fails, or the founder prefers to build a staffed organization from year 1, **and** its own gates pass. A staffed launch makes sense only at a measured median ARPC of **≥$1,100** with ≥13 clients per bookkeeper. At $950 a staffed launch earns $5.8k in Y5 on $88.6k of funding.

### 6.3 Alternative 2 (high-upside choice): SYN-004, licence-exempt energy cost management

**For:**
- a statutory exemption read verbatim;
- licence-free PLC, DR and audit work for any customer size;
- PJM capacity at the cap makes energy a CFO problem;
- the highest long-term enterprise value among reviewed options (Y10 EV $317k base).

**Against:**
- post-review Y3 ≈$33k, because fees begin only at the customer's contract expiry (8–12+ months);
- DR revenue share is likely about zero;
- a major supplier's onboarding asks for state licence documents;
- peak funding with the draw (≈$122.0k) exceeds the backing; starting the draw at month 25 instead of 13 cuts it to $74.0k;
- P.A. 102-958 is unread;
- all 17 stresses push peak funding above $100k.

**Switch to it if** ≥2 of 3 suppliers say yes in writing **and** at least 30% of reviewed bills expire within 12 months **and** counsel confirms the exemption. Take no draw until five accounts are paying.

### 6.4 Reserve and the rest

- **Reserve: WS04-014.** Prepaid recurring revenue and the cheapest test (~$150). But a $399 Chicagoland competitor with free onboarding, plus uncovered breach liability, cut its base to ≈$37k in Y3. It is the best *asset* on paper: delegation score 6, base Y10 EV $475k.
- **Validation-only:** WS05-007, SYN-001, WS13-014.
- **Failed:** WS12-012, WS16-006, WS18-035, and WS18-003 as primary.

### 6.5 Why major alternatives were not chosen

| Candidate | Reason it did not become primary or an alternative |
|---|---|
| WS12-012 offshore CPA staff (#2 harmonized; Y5 after FDC $87k) | Worst conservative case of all 11 (peak $455,972); needs Philippine resident officers; DO 174 exposure; GM is thin (each point ≈$15k of Y5); reviewer verdict "fails" |
| WS05-007 pest control (#1 at Stages B and C) | Its top price driver is unverifiable; it falls to last on the harmonized model; peak ≈$79k; restricted-use bait rule risk |
| SYN-001 trucking hub (#2 by Stage F score) | #8 harmonized; stacked E-drivers; likely illegal tie-in; peak ≈$95k (harmonized $139k) |
| WS13-014 GPR | Rank not robust (#5 to #9 on one rule); competence and liability; peak ≈$110k |
| WS18-003 junk removal (only B-level economics) | B applies to branded units only; peak too high; manager layer consumes owner cash |
| Vertical bookkeeping (most weight-stable at Stage B) | Absorbed into SYN-006 (construction vertical), which is Alternative 1 |
| Home care (best documented demand and delegation) | $139–209k at risk for ≈$27k Y3 |

**The primary-versus-Alternative-1 choice is acknowledged as close.** The day-60 gates are meant to decide it.

---

## 7. Critical financial assumptions (Stage E against post-review)

All drivers are monthly unless noted. "→" marks a Stage F correction. Values without an arrow were unchanged. Standard rules in all three models: $4,000/month draw from month 13; 30% tax; start capital equal to base peak funding.

### 7.1 WS12-014: recruiting desk

| Driver | Stage E base | Post-review base (cons / opt) | Level | Basis / source |
|---|---|---|---|---|
| Hiring-manager conversations about a live role | 9 | 9 (7 / 9) | E | Universe from public postings (e.g. Formic and Sargent & Lundy URLs in §5.1) |
| Conversation → signed fee agreement | 30% | **22%** (25% / 30%) | E | Playbook gate 5/30 = 16.7% |
| Agreement → placement (fill) | 20% | **15%** (15% / 20%) | E | In-house TA with LinkedIn Hiring Assistant [B]; PageGroup offer-conversion problem [B] |
| Founder ramp to full pace | 12 months | **15** (18 / 12) | E | No agreed benchmark [D]: https://recruiterflow.com/blog/recruiter-onboarding/ |
| Lead → cash cycle | 4 months | **5** (5 / 4) | E | Paraform guide [D]: https://www.paraform.com/insights/contingency-recruiting-guide |
| Realized first fee | $17,850 ($105k × 20% × 85%) | $17,850 ($13,680 / $17,850) | D | Salaries [D] in §5.1; fee [D]; fallout reserve mechanism [A]: https://www.sec.gov/Archives/edgar/data/930420/000093042026000007/kfrc-20251231.htm |
| Repeat revenue per active client | $670 (0.45 repeats/yr) | **$520** (0.35/yr) ($570 / $670) | E | Unsourced |
| Client churn | 5.0% | **5.5%** (7% / 5%) | E | — |
| Referrals per 100 active | 2 | 2 (1 / 2) | E | H5 caps at 1.0 |
| Gross margin (repeat / first) | 95% / 93% | same | C | RH perm GM 99.8% [A]: https://www.sec.gov/Archives/edgar/data/315213/000031521326000049/rhiq32026ex991.htm |
| Bad debt / disputes | 4% of revenue | same | E | — |
| CAC per new client | $400 | same | E | — |
| DSO | 40 days | 40 (55 / 40) | D | Invoice on start, net 30 |
| Recruiter #1 (trigger: revenue ≥$20k/month) | $6,900, 0.35 new clients/month | same; **never triggered in base** | E | Pays only at ≥0.7/month |
| LinkedIn Recruiter Lite | $170 | same | D | https://100hires.com/linkedin-recruiter-cost.html (LinkedIn does not publish it) |
| CRM | $135 | same | B | https://recruitcrm.io/pricing/ |
| E&O + GL insurance | $175 | same | E | Quotes MISSING |
| EV multiple | 2.0× | **1.5×** (1.0× / 2.0×) | D/E | BizBuySell sold-service median 2.38× [D]: https://www.bizbuysell.com/learning-center/valuation-benchmarks/service-business/ |
| **Results** | Y3 $170,012; Y5 $259,002; peak $12,836 | **Y3 $80,698; Y5 $114,468; peak $29,277 (no draw $15,180)**; cons $41,471 / $55,944 / $68,241 | | 2023-type year: $50,009 / $64,229; 2009-type: $19,110 / $22,345, peak $140,717; fee 18% × 80%: $69,234 / $100,494 |

### 7.2 SYN-006: construction back office

| Driver | Stage E base | Post-review base (cons / opt) | Level | Basis / source |
|---|---|---|---|---|
| Blended ARPC | $1,000 | **$950** ($800 / $1,200) | D/E | Wishup $999 [D]; vendor bands [D] (URLs in §5.2) |
| Clients per bookkeeper | 15 | **13** (13 / 13) | E | Census: ~$130k receipts per employee in Illinois NAICS 541219 [C]: https://www2.census.gov/programs-surveys/susb/tables/2022/us_state_6digitnaics_2022.txt |
| Bookkeeper loaded cost | $5,800 | **$6,200** ($7,000 / $5,800) | C | BLS Chicago clerk mean $53,560 [C] (§5.2); business and financial operations $46.54/h [C]: https://www.bls.gov/regions/midwest/news-release/2026/occupationalemploymentandwages_chicago_20260723.htm |
| External construction reviewer (from month 3) | $600 | **$1,000** ($1,500 / $700) | E (rate MISSING) | Reviewer judgment: unlikely under $150/h |
| Founder conversations | 12 | 12 (8 / 16) | E | Award lists [A] |
| Conversation → proposal → win | 35% × 30% | same (win 20% / 35%) | E | No benchmark |
| Churn | 1.6% | same (2.5% / 1.2%) | C (incumbent proxy) | Paychex 82–83% retention [A]: https://www.sec.gov/Archives/edgar/data/723531/000119312526307785/payx-20260531.htm |
| One-time onboarding / clean-up | $1,500 | same ($750 / $2,500) | E | Unbenchmarked |
| Gross margin (tools only; labour in staff) | 88% | same | B | Certified-payroll software $12/report or $145/month [B]: https://lcptracker.com/lcpcertified/ |
| DSO | 8 days | same (30 / 3) | D | ACH in advance |
| CAC / fixed marketing | $250 / $400 | same | E | CFMA associate $500/yr [B]: https://cfmachicago.wildapricot.org/Membership |
| E&O + cyber | $275 | same | E | Insureon bookkeeper floor $37 + $47 [D]: https://www.insureon.com/finance-accounting-business-insurance/bookkeepers/cost |
| Senior accountant (≥30 clients) / compliance specialist (≥25) | $8,500 / $5,500 | same | E | — |
| EV multiple | 2.5× | same | D | Bookkeeping-practice multiples MISSING |
| **Results** | Y3 $94,734; Y5 $181,482; peak $9,979 | **Y3 $49,662; Y5 $82,563; peak $11,540**; cons $23,478 / $32,372 / $181,795 ($42,087 no draw) | | ARPC $900 → $31,750 / $51,174; labour +20% → Y3 −$8.6k; hires 30% sooner → Y3 −$86.8k |

### 7.3 SYN-004: energy cost management

| Driver | Stage E base | Post-review base (cons / opt) | Level | Basis / source |
|---|---|---|---|---|
| Lead → first fee (includes the contract-expiry wait) | 4 months | **10** (12 / 8) | E (mechanism B) | ENGIE pays only once the new contract flows [B] (§5.3) |
| Qualified exempt-size conversations | 10 | **7** (5 / 9) | E | Courted pool; 93% already on ARES [A] |
| Proposal → win | 22% | **20%** (15% / 22%) | E | Customer designates between brokers [B] |
| Lead → proposal | 40% | same | E | — |
| ARPC | $850 ($750 supply + $43 DR + $56 PLC) | **$800** ($460 / $900) | D/E | 9 GWh × 1.0 mil [D]: https://growthzonesitesprod.azureedge.net/wp-content/uploads/sites/2326/2021/05/boma-energy-procurement-slides-printer-friendly.pdf ; DR share ≈0 [D] (GridBeyond, §5.3) |
| Churn | 1.2% | same (2.0% / 1.2%) | E | 20–30% lost per renewal |
| One-time revenue (audit hits) | $600 | same ($250 / $600) | E | Hit rates MISSING |
| Gross margin | 80% | same (65% / 80%) | E | Partner split for sub-1,500 kW deals MISSING |
| DSO | 60 days | same (75 / 60) | B/C | Remittance on the 25th after the customer pays; DR paid annually [C]: https://www.sustainablejersey.com/fileadmin/media/Actions_and_Certification/Actions/Energy/Energy_Tracking_and_Management/PJM_Demand_Response_Guide.pdf |
| Supplier onboarding delay | 3 months | same | B/E | ENGIE replies within 15 business days [B]: https://www.engieresources.com/brokers-and-consultants |
| Price growth | 0% | same (−3% / 0%) | A/E | Capacity collared through May 2030 [A] |
| Analyst (≥35 accounts) / rep (≥$25k/month revenue) / licence partner (≥$8k/month) | $6,000 / $6,500 / $1,500 | same | E/C | Chicago wholesale sales rep mean $85,490 [C] |
| Counsel review (month 2) | $2,500 | same | E | — |
| EV multiple | 2.5× | same | C/D | Insurance-book multiples as a ceiling [C]: https://www.insurancejournal.com/magazines/mag-features/2025/07/21/832139.htm |
| **Results** | Y3 $98,323; Y5 $120,332; peak $62,155 ($32,371 no draw) | **Y3 $33,486; Y5 $105,728; peak ≈$122.0k ($46.9k no draw)**; breakeven month 22 | | Reviewer's conservative: −$2.7k / $30.4k, peak $212.6k; upside $68.3k / $144.2k, peak $87.8k |

---

## 8. Named operators, suppliers and prospects (top 3)

**Prospects are business names only.** All are marked "prospect — not contacted". None has expressed interest.

**WS12-014: recruiting desk.**
- **Competitors:**
  - Actalent / Aerotek (Allegis);
  - Robert Half (perm revenue $440M in 2025);
  - Kforce (direct hire $25.7M);
  - Paraform (recruiter marketplace);
  - 356 Illinois placement-agency and 329 executive-search establishments (2023 Census; controls specialists not enumerated);
  - **in-house talent acquisition using LinkedIn Hiring Assistant**, the largest competitor.
- **Suppliers and tools:** LinkedIn Recruiter Lite; Recruit CRM; Loxo; Crelate; Top Echelon (split network); Paraform; Apollo.io; Indeed / ZipRecruiter; an E&O insurer; Illinois Department of Labor (regulator).
- **Prospects (27):**
  - **Tier A/B (integrators, mid-size plants, engineering firms):** Wunderlich-Malec Engineering; Barry-Wehmiller Design Group; Concentric Integration; WESA Automation; Daifuku Intralogistics America (Wynright); Formic Technologies; Yaskawa America; Medline Industries; Ingredion; Primient; Rivian Automotive; Baxter & Woodman; CDM Smith; Woodward; Sargent & Lundy.
  - **Demoted as vendor-gated or no-contact:** Abbott; Chamberlain Group; AbbVie; Caterpillar; Mars Wrigley; Ameren Illinois.
  - **Demoted as technician tier or weak fit:** Novolex; Mondelez International; Baxter International; Littelfuse; Huntsman; Conagra Brands.

**SYN-006: construction back office.**
- **Competitors:**
  - construction CPA firms (Porte Brown, Wipfli, Legacy Professionals);
  - Remote Books Online; 24 Hour Bookkeeper; Wishup;
  - Bench / Pilot / Digits / Intuit QuickBooks Live;
  - certified-payroll software: LCPtracker, PaidReady, ADP + Points North, Dapt;
  - **construction payroll platforms Payroll4Construction and Miter**, not named in the playbook;
  - in-house office managers.
- **Suppliers and partners:** IDOL certified-payroll portal; Intuit QuickBooks Online / ProAdvisor; QuickBooks Payroll / ADP RUN / Gusto; Check; Knowify; WIPkeep; Anthropic Claude Team; The Horton Group (surety); Arthur J. Gallagher Surety; SBA Surety Bond Guarantee Program; CFMA Chicago; ASA Chicago; Federation of Women Contractors; NEXT Insurance / Insureon.
- **Prospects (36 public-award primes):** United Enterprise LLC; Advanced Water Solutions LLC; Millennium Contracting Corp.; Ryans Plumbing 1 Inc; SWR Joint Venture; Plumbing Professionals Co; Courtesy Electric Inc; Tiles in Style LLC (Taza Supplies); Ashlaur Construction Co.; City Lights, Ltd.; CSI 3000 Inc; GMA Construction Group; Industria Inc; Troop Contracting Inc; CCS–Nu Veterans JV LLC; Autumn Construction Services; Cordos Development & Associates; Old Veterans Construction; Pacific Construction Services; Robe Inc.; Seven D Construction; G & V Construction; Cora Jane Contractors; KDA Contractors; 2BG Venture; Helm Builds; K.C. Electrical Construction; Bi-State Masonry; J & B Builders; Lawdensky Construction; Azimuth Contracting; Marval Group; Celtic Commercial Painting; Shine On Group; Goetz Concrete Construction; Sumit Construction.
- **Caveat:** these are **primes**. The true target, small subcontractors, appears in no public list reviewed.

**SYN-004: energy cost management.**
- **Competitors:**
  - supplier direct sales teams;
  - CSP direct teams (CPower, Enel X, Voltus, GridBeyond);
  - KilowattLogic (flat-fee DR);
  - 392 licensed brokers, including Vanguard Energy Services and Nania Energy Advisors;
  - E-Quantum Consulting (flat fee);
  - Schooley Mitchell (contingency);
  - national consultancies (not researched).
- **Suppliers and partners:**
  - **Retail suppliers:** ENGIE Resources; Constellation (Channel Partners); MC Squared Energy Services; Calpine Energy Solutions; NRG / Direct Energy Business.
  - **CSPs:** CPower; Enel X North America; Voltus; Enersponse; GridBeyond.
  - **Regulator:** Illinois Commerce Commission.
- **Prospects (30):** Pete's Fresh Market; Shop & Save Market; Humboldt Park Health; Sinai Chicago; Gonnella Baking; Carl Buddig & Company; Land O'Frost; Oberweis Dairy; Kronos Foods; Scout Cold Storage; Interstate Warehousing; Stampede Culinary Partners; Turano Baking; Newly Weds Foods; St. Bernard Hospital; Ashland Cold Storage; Frozen Assets Cold Storage; Produce Terminal Cold Storage; ODW Logistics; Highland Baking; Ed Miniat; Peer Foods Group; Vienna Beef; World's Finest Chocolate; Bridgford Foods; Vegetable Juices Inc.; Lawrence Foods; Saint Anthony Hospital; Thorek Memorial Hospital; 1547 CSR-Chicago Wells.
- **Caveat:** exemption status is unverified for every prospect. Saint Anthony, Thorek and one data centre are probably below 1,500 kW.

---
## 9. Transaction evidence and the most important primary sources

**The founder has made no transactions.** Atlas holds **no realized price from a signed contract** in any of the three recommended businesses. The closest things to real transaction evidence are:

| Evidence | What it shows | Level | URL |
|---|---|---|---|
| Top Echelon network placements, 2018 | Average fees by discipline (engineering 23%, $24,521) | D | https://pinnacle.topechelon.com/average-fees-percentages-discipline-2018/ |
| Top Echelon top-10 recruiters, 2025 | #10 made 7 placements / $99,312; #1 61 / $523,600 | D | https://pinnacle.topechelon.com/the-top-10-te-network-recruiters-in-2025/ |
| Top Echelon largest Q2 2025 split fees | Mostly 25% fees on manufacturing leadership roles | D | https://pinnacle.topechelon.com/the-largest-te-network-placement-fees-in-q2/ |
| Robert Half and Kforce 10-Ks | Realized perm revenue, placements and average-fee changes | A | URLs in §5.1 and §7.1 |
| City of Chicago contract awards | Named awardees, dates and amounts (the primes SYN-006 targets) | A | https://data.cityofchicago.org/resource/rsxa-ify5.json |
| USASpending awards | 226 federal specialty-trade awards to Illinois recipients | A | https://api.usaspending.gov/api/v2/search/spending_by_award/ |
| Illinois school district DR board packet | Customer kept 70% (NRG) and 75% (Direct Energy) of DR revenue | A | https://nbcusd.schoolboard.net/sites/il.nbcusd.schoolboard.net/files/09.%20A-Demand%20Response-Board%20January%202020.pdf |
| City Colleges of Chicago board item | Supply via Constellation, DR via CPower under state contract | A | https://apps.ccc.edu/brpublic/2022/feb/34407.pdf |
| Morton CUSD 709 board summary | Outside broker estimated at ~3 mils (~$13k/yr) | D | https://citizenportal.ai/articles/6001099/Illinois/School-Boards/Morton-CUSD-709/Board-authorizes-administration-to-secure-electricity-contracts-up-to-five-years-if-rates-meet-thresholds |
| Urbana council resolution | 0.75-mil consultant fee on municipal aggregation | D | https://www.city.urbana.il.us/_Agendas_-_Packets_-_Minutes/Agendas_2016/01-04-2016_Special_Meeting/Resolutions_2016-01-001R-002R.pdf |
| PJM capacity auctions | Cleared prices (market transactions) | A | URLs in §5.3; 2027/28: https://www.pjm.com/-/media/DotCom/markets-ops/rpm/rpm-auction-info/2027-2028/2027-2028-bra-report.pdf |
| Public pest-control bid tabulation | $30–180/month per building | A | URL in §5.5 |

**Further consequential primary sources not listed above:**
- Illinois Equal Pay Act: salary-history ban and pay-scale disclosure, including for employment agencies [A via mirror]: https://codes.findlaw.com/il/chapter-820-employment/il-st-sect-820-112-10/
- Job Opportunities for Qualified Applicants Act (timing of criminal-history questions) [A]: https://codes.findlaw.com/il/chapter-820-employment/il-st-sect-820-75-15/
- AI Video Interview Act [A]: https://codes.findlaw.com/il/chapter-820-employment/il-st-sect-820-42-5/
- Freedom to Work Act: non-competes void below $75k ($80k from 2027) [A]: https://codes.findlaw.com/il/chapter-820-employment/il-st-sect-820-90-10/
- Illinois Human Rights Act, employment agencies [A]: https://codes.findlaw.com/il/chapter-775-human-rights/il-st-sect-775-5-2-102/ ; AI amendment, P.A. 103-0804 [C]: https://www.foley.com/insights/publications/2025/02/illinois-takes-aim-artificial-intelligence-employment/
- Private employment agency licence (required only if candidates are charged): $250–500 fee, $5,000 bond [A]: https://labor.illinois.gov/content/dam/soi/en/web/idol/2025-updated-chicago-address-forms/pea-license-instructions%2011-12-25.pdf
- U.S. manufacturing job openings (JOLTS) [C]: https://data.bls.gov/timeseries/JTS300000000000000JOL
- Accounting Act §9 (titles) [A]: https://codes.findlaw.com/il/chapter-225-professionsoccupations-and-business-operations/il-st-sect-225-450-9.html ; §8 (attest) [A]: https://codes.findlaw.com/il/chapter-225-professionsoccupations-and-business-operations/il-st-sect-225-450-8.html
- Prevailing Wage Act §11a (debarment) [A]: https://codes.findlaw.com/il/chapter-820-employment/il-st-sect-820-130-11a/
- Public works bond thresholds (30 ILCS 550/1) [A]: https://codes.findlaw.com/il/chapter-30-finance/il-st-sect-30-550-1.html
- SBA Quick Bond limit (13 CFR 115.30) [A]: https://www.law.cornell.edu/cfr/text/13/115.30 ; SBA surety program [A]: https://www.sba.gov/funding-programs/surety-bonds
- Surety practitioner guidance on when CPA-prepared statements are needed [C/D]: https://orsurety.com/blog/your-underwriter-says-you-need-a-cpa-prepared-statement.-what-now-part-i ; https://www.acppubs.com/CN/article/51F9DFA0-what-do-sureties-look-for-in-financial-statements
- Competing construction payroll platforms [D]: https://www.payroll4construction.com/il-prevailing-wage/ ; https://www.miter.com/resources/illinois-prevailing-wage-rates/
- ICC agents, brokers and consultants page [A]: https://icc.illinois.gov/authority/agents-brokers-and-consultants
- ABC experience rule 454.70 [A]: https://www.law.cornell.edu/regulations/illinois/Ill-Admin-Code-tit-83-SS-454.70 ; disclosure rule 454.90 [A]: https://www.law.cornell.edu/regulations/illinois/Ill-Admin-Code-tit-83-SS-454.90
- Official 16-115C page (unreachable during research; search snippets cite P.A. 102-958) [D]: https://lig.ilga.gov/legislation/ilcs/documents/022000050K16-115C.htm
- Constellation channel partners [B]: https://www.constellation.com/solutions/for-your-commercial-business/channel-partners.html
- PJM active CSP list [A]: https://www.pjm.com/markets-and-operations/demand-response/csps.aspx
- Chicago building energy benchmarking (prospect consumption) [A]: https://data.cityofchicago.org/resource/xq83-jr8c.json
- Intuit's 10-K on AI done-for-you bookkeeping [A]: https://www.sec.gov/Archives/edgar/data/896878/000089687826000037/intu-20260731.htm

---

## 10. Competitive, capital, regulatory and wealth analysis

### 10.1 Competition

- **WS12-014.**
  - The real competitor is in-house talent acquisition with AI sourcing. It shrinks the set of roles needing an agency to the genuinely scarce ones.
  - Volume firms (Actalent/Aerotek) already work Illinois controls roles.
  - Top firms place 54.4% of hires from their own candidate databases [D]; a newcomer starts at 0%.
  - **Fee rate is not the vulnerability** (RH's average fee rose through 2023 and 2025). Volume is.
- **SYN-006.**
  - Construction CPAs can bundle monthly close and WIP at will, and their year-end report is what the surety relies on.
  - Offshore firms already advertise WIP at $999.
  - Construction payroll software is eroding the labour content of certified payroll.
  - The moat is WIP judgment, which is thin.
- **SYN-004.**
  - Incumbent brokers give PLC alerts away free.
  - Suppliers may contact customers directly.
  - CSPs undercut DR channel fees with 100% pass-through.
  - Incumbents' supplier credit and volume relationships win large RFPs.

### 10.2 Capital requirements

- **Validation sprint (weeks 1–8):** $600 unconditional, $1,350 ceiling including both alternatives' tests.
- **Primary launch tiers:**
  - ≈$2–5k after the gate (LLC ~$150, attorney fee-agreement review ≈$1,500 (E), CRM, laptop and website $2,500);
  - ≈$5–10k runway to first fee;
  - ≈$10–25k working capital and reserve;
  - recruiter #1 ($25–50k) only at trailing-6-month revenue ≥$20k/month with ≥8 open searches.
- **Maximum plausible loss of the recommended plan ≈$35k.** At least $65k should stay uncommitted.
- **The largest real capital need is unmodelled:** the founder's personal living costs for months 1–12. Atlas advises holding 4–6 months of personal runway before month 1.
- Capital does not buy growth on present evidence. A hired recruiter at modelled productivity (0.35 new clients/month) *lowers* profit: −$14.6k, −$32.0k and −$1.7k in Y3–Y5. A hire pays only at ≥0.7/month.

### 10.3 Regulatory analysis (Illinois)

| Business | Statute or rule | Atlas reading | Needs counsel |
|---|---|---|---|
| WS12-014 | **225 ILCS 515/1.1** (Private Employment Agency Act) | Excludes recruiters "compensated solely by any employer"; void if any candidate is charged "directly or indirectly", including résumé preparation or "any other personal service"; theatrical/domestic carve-outs | Confirm current text; out-of-state placements; FCRA if the desk runs reference checks; fee-agreement enforceability; Chicago business licence (BACP) |
| WS12-014 | 820 ILCS 112/10; 820 ILCS 75/15; 820 ILCS 42/5; 820 ILCS 90/10; 775 ILCS 5/2-102; P.A. 103-0804 | Salary-history ban applies to agencies; third-party liability for pay-scale omissions; criminal-history timing; AI video-interview consent; non-compete thresholds; AI discrimination ban (IDHR rules withdrawn 2 June 2026) | Whether any AI note-taking or ranking use triggers P.A. 103-0804 notice |
| SYN-006 | **225 ILCS 450/8.05, /8, /9** (Accounting Act) | Bookkeeping, compilations and tax are not CPA-restricted; attest is; titles barred (up to $10,000 per offense) | Use of "accountant" in the name |
| SYN-006 | **820 ILCS 130/5, /11a** (Prevailing Wage Act); **SB1344 = P.A. 104-0023** (signed 2025-06-30) | Certified payroll monthly by the 15th; penalties up to $1,000 / $2,000 per missed month reach "any officer, employee, or agent… whose duty… is to file"; willful false filing is a Class A misdemeanour; debarment comes from §11a | **Is certified-payroll preparation itself regulated? (Unverified; the Accounting Act is silent.)** Duty-allocation wording; E&O coverage of fines; outside preparer using the client's IDOL log-in; payroll-service-provider creep; PIPA (815 ILCS 530) for worker SSNs; FTC Safeguards applicability |
| SYN-004 | **220 ILCS 5/16-115C(b)** and 83 Ill. Adm. Code 454.20 / 454.30(b)(5) | Exemption for customers with aggregate billing demand of affiliated Illinois accounts >1,500 kW (highest monthly billed demand per account in the prior calendar year); **16-115C(a-5) non-affiliation disclosure applies to "All third-party sales representatives"** | **Content of P.A. 102-958 (HB 4973, eff. 2023-01-01)**; meaning of "affiliated"; whether mixed-size marketing lists are solicitations; whether exempt-only experience counts under 454.70; Consumer Fraud Act; Texas-law agency agreements |
| SYN-001 | **215 ILCS 5/151; 215 ILCS 5/500-80** | A tie-in discount is a likely illegal inducement; the LLC likely needs an IDOI business-entity licence to receive the split | Full opinion before any materials |

### 10.4 Wealth creation

- **No from-scratch option shows evidence of $500k–$1M a year of owner cash within five years.** Post-review base Y5 owner cash is $66.6–97.1k a year across the top four.
- **Planned sequence:**
  1. cash engine (months 0–36);
  2. accumulate (the primary's base reaches ≈$69k net deployable by end of year 5; cumulative retained turns positive in month 37);
  3. redeploy in years 4–6 into a **durable recurring-revenue business bought with a manager in place**;
  4. multi-business by years 6–10.
- **Illustrative acquisition (all D/E):** a bookkeeping/payroll practice at SDE $150k × 2.38× = $357k; 30% down ($107k); about 21% manager-adjusted unlevered yield. Bookkeeping-practice multiples are MISSING.
- **10-year deployable (base / harmonized):** WS12-014 $316k / $208k; SYN-006 $104k / $24k; SYN-004 $239k / $189k; WS04-014 $217k / $230k.
- **Year-10 EV (base):** $206k / $275k / $317k / $475k for the same four.
- Plausible route to $300–350k/yr by years 8–12: the desk plus three acquired businesses at ≈$75k each (E).

---

## 11. Independent review findings, disputes and preserved disagreements

**How the review worked.**
- Six reviewers who wrote nothing they reviewed reproduced every model exactly.
- They challenged the top five drivers, re-opened about 120 citations and found errors in every playbook.
- At least 10 cited sources could not be opened.

**Findings that matter most:**
1. Founder unpaid delivery labour was embedded in profit in 10 of 11 models.
2. Funnel drivers came from template defaults: 0.40 × 0.25 in four models.
3. Optimism stacked across individually defensible drivers.
4. Real comparator prices cut price or margin in 10 of 11. **WS12-014 was the exception:** its fee held; its funnel fell.
5. Incumbent benchmarks were applied to newcomers.
6. Evidence labels drifted upward (A labels on sources that do not say the claim).
7. Validation gates contradicted the models.

**Disputed conclusions and preserved disagreements:**

| Topic | Author view | Reviewer view | What settles it |
|---|---|---|---|
| WS12-014 funnel | 30% / 20%, 12-month ramp | 22% / 15%, 15 months; the Stage E base is the *optimistic* case | Top-quartile output (5.21 vs 1.38 placements) would justify the filed base; test 3 |
| SYN-006 productivity | 15 clients/bookkeeper; fcf 5; ceiling $250k | 13; fcf 4; ceiling ~$150k | Time-tracked ≤10 h/client; median ARPC ≥$950 |
| SYN-004 economics | Y3 $98k; roic 6; access 4 | Y3 ~$33k; roic 5; access 3 | Supplier acceptance (V1) and expiry statistics (V3) |
| WS04-014 price | Local on-site premium justifies $690 | $650 until proven | ≥2 LOIs at $690+ |
| WS13-014 | Y3 $106k | Y3 ~$50k ("unevidenced, not wrong") | Measured ARPC ≥$750 and rebooking |
| WS12-012 | Base defensible | Fails | Salary asks ≤$1,100; prepaid ≥$2,300 |
| WS16-006 | GM 30% | Fails at 27% (the reviewer would reverse if contractors pay 15–35% above 4imprint) | $0 invoice test |
| Ranking method | Stage F scorecard: SYN-006 #1, SYN-001 #2, WS05-007 #3, WS12-014 #5 | Harmonized model: WS12-014 #1, WS12-012 #2, SYN-006 #3 | Neither is "the decision" |
| Primary vs Alternative 1 | — | "Close"; day-60 gates decide | Founder preference to build an organization vs earn fees |

**Data-integrity notes:**
- The screening database still carries WS18-035 at its Stage E score; the Stage F update was not merged.
- WS12-014's economics evidence was rated C at Stages C/D and corrected to D at Stage E.
- Validation thresholds: WS05-007's summary previously conflated kill and pass thresholds (now corrected). For WS13-014 the playbook's pilot gate is a ≥$550 half-day median; the reviewer raises it to ≥$600 and moves the pilot out of winter — Atlas adopts the reviewer's stricter gate.

---

## 12. Evidence gaps, limitations, and claims requiring verification

### 12.1 Research limitations

1. **No direct contact was authorized.** Supplier acceptance, prices, customer interest and partner terms are documented or assumed, never confirmed.
2. **Inaccessible sites:**
   - ilga.gov (503/TLS failure on all hosts);
   - Justia, FindLaw (intermittently), LegiScan and BillTrack50 (Cloudflare);
   - chicago.gov and the Cook County Assessor (403);
   - BLS API (blocked or limited; regional pages were used);
   - Census API (key required);
   - BizBuySell (403);
   - eCFR, fmcsa.dot.gov and dla.mil (bot blocks);
   - several cited pages (403s or redirects), including the HomeAdvisor pest-price source, a Junk Peddler licence fact sheet, HomeGuide Chicago, a chicago.gov low-voltage rule page and a trade-press (CCJ) article.
3. **Economics are mostly D/E.** Prices come from vendor pages, third-party pricing pages, job postings, FDDs and asking prices. 54 of 66 long-term driver fields across the 11 models are E, D or D/E.
4. **Paywalled research** (IBISWorld, RMA, LinkedIn's own pricing) was not bypassed. Bulk SEC EDGAR access was not used.
5. **Search budget.** The web-search budget was exhausted early; many facts came from search-result summaries. About 21% of Stage A sources say so.
6. **Founder facts are unknown** (§13).
7. **Desk research cannot measure sales skill**, which is the decisive variable for the primary.

### 12.2 Claims requiring independent verification

Each item gives the exact claim and the source we used.

1. Employer-paid recruiters need no Illinois licence; the exclusion is lost if a candidate is charged for anything. Source: 225 ILCS 515/1.1 via FindLaw (URL §5.1); IDOL FAQ.
2. The current official text of 225 ILCS 515/1.1 matches the mirror (no 2024–26 amendment). Source: mirror only.
3. 20% of first-year base is the most common direct-hire fee, and 18–25% is achievable for controls engineers in Illinois. Source: SIA 2021 via secondtalent.com [D] (URL §5.1); Top Echelon 2018 [D].
4. Illinois engineer-level controls/I&C salary midpoints are ≈$95–140k (median ≈$107k across 11 postings). Source: employer ATS postings [D].
5. A newcomer can convert ~22% of hiring-manager conversations into signed fee agreements, and ~15% of agreements fill. Source: none (E).
6. Established recruiters' modal output is 9–12 placements a year. Source: Top Echelon 2015 poll [D].
7. LinkedIn Recruiter Lite is ~$170/month with 30 InMails. Source: 100hires third-party page [D].
8. Robert Half perm revenue fell 57% (2009), 21.7% (2023) and 9.8% (2025). Source: RH 10-Ks [A].
9. Large Illinois employers route agencies through portals or forbid contact (Abbott, Chamberlain). Source: Workday postings [D].
10. Chicago construction-subcontractor bookkeeping with WIP sells at ~$950/month. Source: Wishup $999 and Remote Books Online bands [D].
11. Surety underwriters accept non-CPA interim WIPs below about $1.5M programs. Source: Western National chart (2016) [B]; TMHCC packet [B].
12. Surety producers will refer clients to a non-CPA bookkeeper. Source: none (E; contrary prior).
13. Preparing Illinois certified payroll for a client needs no licence. Source: none directly (the Accounting Act is silent).
14. An outside preparer may file under the client's IDOL log-in. Source: IDOL FAQ (silent) [A].
15. SB1344 penalties reach an outside filing agent. Source: Amundsen Davis [C]; SB1344 status page.
16. A Chicago full-charge construction bookkeeper costs ~$6,200/month loaded. Source: BLS Chicago clerk mean [C] plus burden (E).
17. 220 ILCS 5/16-115C(b) exempts >1,500 kW customers, and P.A. 102-958 did not narrow it. Source: Onecle mirror [A]; ilga snippet [D].
18. ENGIE, Constellation or NRG will onboard and pay an unlicensed exempt-only broker. Source: ENGIE documents page (asks for licences) [B].
19. Exempt-account broker fees are 0.75–1.5 mils. Source: BOMA slide [D]; Morton CUSD summary [D]; Urbana resolution [D].
20. Average contract-expiry wait for exempt prospects is ~9 months, and ≥30% expire within 12 months. Source: none (E).
21. CSP channel shares for DR are near zero. Source: GridBeyond 100% pass-through [D]; CSP share 20–40% [C].
22. Siotek charges $399/month with free onboarding and serves Chicago. Source: siotek.net [B/D].
23. Chicago restaurant pest-control contracts average ≈$92–125/month. Source: HomeAdvisor 2021 [D-]; GorillaDesk [D]; bid tabs [A].
24. EPA's proposed rodenticide restricted-use reclassification is still not final. Source: EPA page [A].
25. A sold service business median SDE multiple is 2.38×. Source: BizBuySell via search summary [D].
26. 215 ILCS 5/151 bars a "20% off with liability" tie-in, and the value-added-services bills were not enacted. Source: Onecle mirror [A]; bill-status summaries [D].
27. U.S. manufacturing job openings were 584k in September 2026 (preliminary). Source: BLS JOLTS [C].

### 12.3 Most important evidence gaps

- a realized fee and conversion rate for a newcomer recruiter in this niche;
- the share of Illinois controls hiring that runs through vendor portals or MSPs;
- Chicago construction-bookkeeping prices from signed contracts;
- surety producers' actual referral behaviour;
- whether any Illinois retail supplier pays exempt-only unlicensed consultants;
- the exempt-customer pool size and contract-expiry distribution;
- E&O quotes and penalty exclusions;
- bookkeeping-practice acquisition multiples;
- SBA/bank acquisition terms.

---

## 13. Questions that would materially improve the decision

1. **Founder:** weekly hours available in daytime business hours (the desk needs ~25–40 focused hours).
2. **Founder:** existing network in manufacturing, engineering, construction or accounting.
3. **Founder:** age and credit (contracts, insurance, supplier credit, surety); veteran/minority/women-owned status (set-asides).
4. **Founder:** the terms of the conditional $100k (loan or equity, who decides), and personal runway for months 1–12.
5. **Founder:** tolerance for daily cold outreach and rejection, the abandon trigger for the primary.
6. **Market:** do Illinois integrators accept 18–20% from a newcomer, or insist on 15%?
7. **Market:** what fraction of Chicagoland public-works subs already pay for outside bookkeeping, and at what price?
8. **Market:** will any ARES pay an exempt-only consultant, at what mils, and with what onboarding documents?
9. **Legal:** what P.A. 102-958 changed in 16-115C, and whether certified-payroll preparation is regulated.
10. **Strategy:** is there an adjacent role family (e.g., electrical, process or water/wastewater engineering) with better newcomer access than controls?

---
## 14. Highest-value tasks for ChatGPT Deep Research (in priority order)

Do not re-run broad discovery. Each task gives its objective, what to check, where to look, and **what result would change the recommendation**.

**T1. Newcomer recruiter conversion and fill rates (primary's decisive driver).**
- **Objective:** benchmark the post-review funnel (22% conversation → signed agreement; 15% agreement → placement; ~5.8 placements in year 3).
- **Check:** published first-year results for solo or new contingency recruiters; fill ratios on non-exclusive contingency orders; time to first placement; engineering-niche specifics.
- **Where:** Top Echelon, Recruiterflow, Bullhorn and Loxo benchmark reports; SIA; NAPS; recruiter-trainer publications; practitioner surveys.
- **Changes the recommendation if:** credible data show first-year solo fill rates ≤8%, or year-3 output ≤3 placements. The primary's base then falls toward the $41k conservative case, and SYN-006 should lead. Evidence of ≥20% fill would restore the Stage E base.

**T2. Portal/MSP gating of Illinois controls hiring.**
- **Objective:** estimate the share of target employers that buy recruiting only through vendor portals or MSP/VMS.
- **Check:** the 27 named employers' agency policies; MSP use by integrators against plants.
- **Where:** employer career sites, supplier portals, MSP case studies, integrator association (CSIA) material.
- **Changes the recommendation if:** most integrators and mid-size plants are gated. That triggers the primary's abandon rule.

**T3. Construction-bookkeeping pricing in Chicago.**
- **Objective:** replace D-level ARPC ($950 base; $1,100 needed for a staffed launch).
- **Check:** published prices of Chicago or Midwest construction bookkeepers and outsourced controllers offering WIP; CFMA compensation and fee surveys; prices of construction payroll services that include certified payroll.
- **Where:** firm websites, CFMA benchmarker summaries, Payroll4Construction, Miter, regional CPA outsourcing pages, Upwork/agency rate cards.
- **Changes the recommendation if:** the median is ≤$800 (Alternative 1 drops to reserve) or ≥$1,100 with WIP included (Alternative 1 may become the better holding-company core).

**T4. Retail-supplier broker fees for licence-exempt consultants.**
- **Objective:** test whether any Illinois ARES pays brokers who hold no ABC licence because they serve only >1,500 kW customers.
- **Check:** supplier broker-program terms; ICC guidance; mils paid on 5–15 GWh fixed deals.
- **Where:** ENGIE, Constellation, NRG/Direct, Calpine and MC Squared broker pages; ICC ORMD materials; ICC complaint and docket records; energy-broker trade groups (for example, ABCs' industry associations).
- **Changes the recommendation if:** suppliers uniformly require a licence. Alternative 2 becomes customer-paid flat-fee only, or is dropped.

**T5. Correct the regulatory analysis.**
- **Check:**
  - (a) current official 225 ILCS 515/1.1, and any amendment;
  - (b) 220 ILCS 5/16-115C as amended by **P.A. 102-958**, and the meaning of "affiliated";
  - (c) 215 ILCS 5/151 and value-added-services status;
  - (d) the Illinois Prevailing Wage Act (820 ILCS 130) as amended by **SB1344 / P.A. 104-0023**: who is the "agent", whether third-party certified-payroll preparers are regulated, and IDOL guidance on outside preparers.
- **Where:** ilga.gov public acts, JCAR, ICC dockets, IDOL notices, law-firm alerts.
- **Changes the recommendation if:** any exemption is narrower than stated, or certified-payroll preparation needs a licence or bond.

**T6. Overlooked competitors.**
- **Check:**
  - Illinois or Midwest controls/automation recruiting boutiques (count, fees, specialization);
  - Chicago construction back-office firms offering certified payroll plus WIP;
  - Illinois large-C&I energy consultants serving food and cold-storage firms.
- **Where:** LinkedIn company pages (public), Clutch, CSIA, CFMA and ASA directories, ICC ABC list.
- **Changes the recommendation if:** a dense specialist field exists in the primary's niche, or a cheap incumbent already serves SYN-006's exact niche.

**T7. Challenge customer-acquisition assumptions.**
- **Check:** realistic touches per conversation in each channel (cold calls, InMail reply rates, award-triggered letters); construction owners' willingness to outsource books to a non-CPA; CFO receptiveness to unlicensed energy advisers.
- **Where:** sales benchmark reports (Bridge Group, Gong), surety and CPA practitioner articles, energy-buyer surveys.
- **Changes the recommendation if:** volumes imply fewer than ~9 qualified conversations a month for the primary, or fewer than ~12 for SYN-006.

**T8. Supplier and partner accessibility.**
- **Check:** LinkedIn Recruiter Lite actual price and terms; Top Echelon split terms and network fees; E&O availability and price for a small perm desk and for a certified-payroll preparer (penalty exclusions); CSP channel-partner shares; whether the IDOL portal allows preparer accounts.
- **Changes the recommendation if:** E&O will not cover certified-payroll preparers (SYN-006 weakens), or recruiting-tool costs are materially above ~$940/month.

**T9. Verify the numbered claims in §12.2.** Prioritize items 1, 3, 5, 10, 13, 17, 18, 19 and 20. Mark each verified, contradicted or unverifiable, with a URL.

**T10. Independently re-estimate the three base cases.** Using your verified drivers, recompute year-3 and year-5 operating profit and peak funding with the §7 structure. Report Y5 after FDC. **Changes the recommendation if** SYN-006 or SYN-004 beats WS12-014 on Y5 after FDC by more than ~$20k on better evidence.

**T11. Discover stronger adjacent opportunities.** Look only near the evidence. Candidates:
- recruiting for adjacent scarce technical roles (electrical/power, process, water/wastewater, validation engineers);
- retained or engaged search for controls leaders;
- contract controls engineering staffing (payroll float);
- the vertical bookkeeping families (trucking/IFTA, restaurants);
- the extinguisher/first-aid route as a pest add-on;
- buying a small bookkeeping/payroll practice or insurance book in years 3–5 (multiples, SBA 7(a) terms).

**Changes the recommendation if:** an adjacency shows better newcomer access with equal or better economics at A/B/C evidence.

**T12. Refine entry strategies.** For the primary: the best first segment (integrators vs plants vs engineering firms), a split-network or marketplace bridge for early income, and whether to start with 18% two-role exclusives. For SYN-006: certified payroll first vs WIP first. For SYN-004: customer-paid flat fee vs supplier-paid mils.

**T13. Design stronger validation experiments.** Propose cheaper or more decisive tests than:
- the primary's "≥5 of 30 sign";
- SYN-006's "≥3 paid $450 checks, ≥2 cold";
- SYN-004's "≥2 of 3 written supplier yeses plus ≥30% expiries within 12 months".

Include sample sizes, false-positive risks and pass/fail thresholds consistent with the models.

**T14. Improve the recommendation itself.** State whether you would keep the ordering primary → Alternative 1 → Alternative 2 → reserve, given T1–T13. Give the single fact that most supports your view, and say what you would tell the founder to do in the next 14 days.

---

## 15. Suggested output format for your response

Please return one Markdown document with these sections:

1. **Executive verdict** (≤200 words): agree, modify or reverse the recommendation, and why.
2. **Claim verification table:** # (from §12.2) | claim | status (Verified / Contradicted / Partly / Unverifiable) | evidence level A–E | URL(s) | access date | note.
3. **Driver re-estimates:** for each of WS12-014, SYN-006 and SYN-004, a table of driver | Atlas post-review value | your value | evidence level | URL | effect on Y3/Y5 (if computed).
4. **Regulatory corrections:** statute or rule | exact current text (≤25-word quotes) | official URL | effect | counsel question.
5. **New competitors, suppliers and partners:** name | type | URL | relevance | evidence level.
6. **Customer-acquisition challenges** and **adjacent opportunities** (each with evidence and a "would it change the ranking?" line).
7. **Improved validation experiments:** test | cost | duration | sample | pass/fail | which driver it measures.
8. **Revised ranking** of the top four with reasons, and the single most decisive unknown.
9. **What you could not verify,** and why (paywall, block, no source).

Conventions:
- Label every number with an evidence level.
- Separate incumbent from new-entrant economics.
- Never present asking prices or vendor claims as transactions.
- Write MISSING rather than estimating silently.
- Give access dates.
