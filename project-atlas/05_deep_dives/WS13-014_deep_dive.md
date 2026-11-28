# WS13-014 — Private utility locating & concrete GPR scanning (absorbs WS10-005, WS11-023): Stage D commercial deep dive (batch DF)

> **Verdict: RESERVE.** This is the strongest founder fit of the three DF concepts, and it is promoted to finalist only if validation passes. Revised evidence level **D**: prices and equipment are B, but account behaviour is E. Researched 2026-11-28.
>
> Stage D confirmed four facts:
> - **Price anchors.**
>   - Federal ceiling rates for a "Subsurface Utility Field Technician" are **$124.69/h** (about $1,000 per 8-hour day) [B, DF-S029].
>   - GPRS's federal awards since FY22 have a **median of $5,800**, including a $5,800 sewer-mapping job at the VA in Danville, IL [A, DF-S027].
> - **Equipment prices from a dealer list** [B, DF-S026]:
>   - EM locator kits cost $5.5–9.6k.
>   - Ground GPR carts cost $18–36k.
>   - A rented RD8200 kit costs $599/month.
> - **Demand in Chicago.** The city issued **5,042 permits worth ≥$250k** between January 2025 and November 2026, of which 3,325 were renovations [A, DF-S030]. The most frequent contractors on them are named (36 prospects).
> - **Competition.** Besides GPRS, local firms include Hard Rock Technologies (5 CSDA-certified GPR technicians), Butler Scanning (Gurnee) and Cobra Concrete Cutting, which has an in-house GPR team [D, DF-S031].
>
> The driver model gives **base year-3 operating profit of ~$112k**, rising to ~$200k in year 5. The cost is **~$230k peak funding** including owner draws (~$161k without them), because each technician needs a ~$45k kit and vehicle and contractors pay in about 45 days. The conservative case (lower price per visit, higher account churn) loses money once technicians are hired.

## 1. Specific initial niche
**Concrete slab and wall scanning (GPR) before core drilling and saw-cutting, plus EM/GPR private-utility locates, for Chicago renovation subcontractors and GCs.**
- **Buyers:** electrical, plumbing/mechanical and interior GCs working in Loop, River North, West Loop and near-north concrete high-rises (post-tension slabs), plus Cook/DuPage industrial and campus sites.
- **Offer:** next-business-day booking, half-day and full-day flat rates, PDF mark-up reports, and simple CAD/GIS exports of utility locates.
- **Excluded:** legal boundary or topographic surveys, which need a licensed land surveyor.

## 2. Named operators
| Operator | What is known |
|---|---|
| **GPRS (Ground Penetrating Radar Systems, LLC)** | National leader, founded 2001; 400+ project managers in 54+ metros [D, WS13-S032]. Markets same-day Chicagoland utility locating, plus concrete scanning, video pipe, leak detection and 3D scanning [D, DF-S032]. Federal awards FY22–26: 10 awards, median $5,800, range $925–18,609 [A, DF-S027]. 13 acquisitions 2018–25 and still buying [D, WS13-S033]. |
| **Hard Rock Technologies** (Chicago) | Described as a leading Chicago/Midwest GPR scanning firm with 5 CSDA-certified GPR technicians; also infrared and utility locating [D, DF-S031]. |
| **Butler Scanning** (Gurnee, IL) | Scanning plus core drilling and sawing; serves Chicago, Wisconsin, Indiana, Minnesota, Iowa and Michigan [D, DF-S031]. |
| **Cobra Concrete Cutting** (Chicago) | Coring/cutting firm with its own GPR team (Trump Tower, Wrigley Field) [D, DF-S031]. Coring firms can scan in-house, which caps demand. |
| **LaBella Associates** (federal SUE contractor) | GSA ceiling rates $124.69/h field technician, $134.66/h senior [B, DF-S029]. |
| **Equipment-owning subs** | Contractors can rent locators ($499–599/month [B, DF-S026]) or GPR ($450/day for a Mini XT [D, DF-S038]). The share that scan in-house is MISSING. |

## 3. Suppliers and partners (`09_databases/suppliers/WS13-014_suppliers.csv`)
| Supplier | Published terms | Status |
|---|---|---|
| **UCG Underground Supplies** | Radiodetection RD8200+TX10 $9,592; RD7200+TX5 $5,657; Vivax vLoc3-Pro+Loc3-5Tx $5,530; vLoc3 RTK-Pro set $10,605; LMX100 GPR $20,508; LMX200 $36,476; ImpulseRadar PinPointR $18,444; RD8200 rental $599 (1 month) or $499/month (2+ months); financing and trade-ins [B, DF-S026] | Documented |
| **Radiodetection / Vivax-Metrotech** (OEMs) | Sold through dealers at the prices above | Documented via dealer |
| **GSSI** (StructureScan Mini XT, UtilityScan) | Purchase price not published. Concrete GPR class costs $11–17k [D, C3-S024]. Rental $450/day, $1,050/week, $3,000/month [D, DF-S038] | Assumed |
| **ImpulseRadar USA; Leica (via AEG Group)** | Federal buys: $16,710 (Army 2024), $31,417 (NASA 2026) [A, DF-S028] | Documented |
| **Pine Environmental** | Rents and sells the Mini XT; price placeholder only | Assumed |
| **Insurance (Insureon marketplace)** | E&O averages $88/month and GL $45/month for small businesses generally. GC-required limits are MISSING [D, DF-S034] | Assumed |

**Launch kit (base):**
- concrete GPR about $16k plus an RD7200 kit $5.7k = **$21.7k** in month 1;
- an LMX100 ground GPR **$20.5k** in month 4;
- the founder's own vehicle.

## 4. Named prospective customers (`09_databases/prospects/WS13-014_prospects.csv`, 36 organizations)
All 35 contractors come from City of Chicago permit data (contractor of record on ≥$250k permits, Jan 2025–Nov 2026) [A, DF-S030].
- **GCs (18):**
  - Skender (80 permits), Power (68), Bulley & Andrews (66), Clune (55), Pepper (46), Leopardo (46)
  - Berglund, Redmond, Executive Construction (80), F.H. Paschen, ARCO/Murray, Turner, McHugh, Valenti
  - K.R. Miller, Interior Construction Group, JC Anderson (81), Centre Construction
- **Electrical contractors (10):** Kelso-Burnett (96), Maron (92), REX (67), Blade (62), Titan (66), Molloy (74), CECO (71), Continental Electrical Construction, G & M Electrical, ABCO Electrical.
- **Plumbing/mechanical (7):** Great Lakes Plumbing & Heating (141), F.E. Moran, Hill Mechanical, Ewing-Doherty, Johns Plumbing, Admiral Heating & Ventilating, Sherman Mechanical.
- **Coring partner/competitor (1):** Cobra Concrete Cutting.

Large GCs often run master service agreements with national vendors (assumed). The more reachable buyers are the electrical and plumbing foremen who order cores weekly.

## 5. Representative transactions
| Job | Revenue | Direct costs | Contribution | Terms |
|---|---|---|---|---|
| Half-day slab scan before coring (electrical sub, high-rise) | $600 (E; guide range $300–600 [D, C3-S028]) | tech 5 h $200; vehicle/parking $45; kit depreciation $15; supplies/report $10 | **$330 (55%)** | Net-30/45 |
| Full-day private-utility locate + GPR sweep (GC, campus/industrial) | $1,100 (consistent with $124.69/h × 8–9 h [B, DF-S029]) | tech 9 h $360; vehicle $55; kit $30; paint/map $20 | **$635 (58%)** | Net-30/45 |
| Federal facility sewer/utility mapping | **$5,800** (actual GPRS award, VA Danville IL [A, DF-S027]) | tech 4 days $1,300; equipment incl. sewer-camera rental $600; travel $450; CAD/GIS $300 | **$3,150 (54%)** | Government net-30 |

Overhead, insurance and acquisition come out of these contributions.

**Key unknowns:** visit frequency per account, and whether Chicago subs pay $600 for a half day when GPRS and coring firms bundle scanning.

## 6. Customer acquisition
**Customer #1** comes from one of three routes:
- a coring/cutting firm that needs overflow (Cobra-type partner);
- an electrical foreman met on a permitted job site, with the job found in permit data;
- Google search for "concrete scanning Chicago" (organic plus Google Business Profile).

Offer the first half-day at a discount and deliver the PDF report the same day.

**Customers #2–10:**
- lunch-and-learns at electrical and plumbing contractors' offices ("why scan before coring, and how to read our report");
- follow-up on every permit that names the contractor.

**Customers #11–100:**
- referrals as superintendents move between firms;
- GC safety-department approved-vendor lists, which require COI, a safety program and possibly ISNetworld/Avetta-type prequalification (assumed);
- a part-time business-development hire from month 24.

**Funnel (base):**
- 22 qualified conversations a month;
- 50% receive a priced first job;
- 35% of first jobs become repeat accounts, so about 3.9 new accounts a month;
- 5% of accounts lapse each month;
- about 79 active accounts by month 36.

All rates are E.

**Economics:**
- CAC of $250 per account (discounted trial, travel, lunch-and-learn).
- ARPC of $750/month (about one visit per account per month), so CAC is repaid in the first month.
- LTV of about $750 × 90% × 20 months ≈ $13.5k gross before technician time.

**Weekly sales work:** 10–15 hours of founder field sales throughout years 1–2.

## 7. Pricing strategy
- **Published flat rates:**
  - half-day (≤4 h on site) at $550–650;
  - full day at $1,000–1,200;
  - an after-hours/weekend surcharge;
  - mobilisation for sites more than 40 miles out.
- **Mapping deliverables** (CAD/GIS) are priced per acre or per project.
- **Anchors:**
  - GSA ceiling $124.69/h [B, DF-S029];
  - consumer guides $300–600 half day and $800–1,500 full day [D, C3-S028];
  - GPRS federal median $5,800 per project [A, DF-S027].
- **Positioning:** do not undercut GPRS. Compete on booking lead time in the suburbs and on report turnaround. Chicago commercial rate cards remain MISSING, and the first validation task is to collect three or more competitor quotes from customers (§13).

## 8. Working capital and cash conversion
| Active accounts | Revenue/mo (ARPC $750) | Receivables (DSO 45) | Payables (15 days, small COGS) | Net working capital |
|---|---|---|---|---|
| 10 | $7.5k | $11.3k | $0.4k | **~$10.9k** |
| 50 | $37.5k | $56.3k | $1.9k | **~$54k** |
| 200 | $150k | $225k | $7.5k | **~$218k** |

- **Cash conversion cycle:** about 43 days.
- **Capex per technician:** about $45k (kit plus vehicle).
- **Funding:** both together push base peak funding to about $230k with draws, or about $161k without. Equipment financing through the dealer (offered, terms MISSING) or factoring would reduce the founder's capital.
- **Gate check:** capital at risk before first revenue is about $45–65k, so it passes G1.

## 9. Regulatory path
1. **Licensing:** no Illinois licence was identified for private locating or GPR scanning (ilga.gov was unreachable, so this is unverified; E).
   - Keep deliverables as "locate/scan reports", not surveys. Legal boundary or topographic surveys require an Illinois Professional Land Surveyor.
2. **JULIE (Illinois one-call):** member utilities do not locate private lines, and the owner bears the cost [B, WS11-S031]. This is the structural demand driver.
   - Excavators must still call JULIE. The private locate supplements it and does not replace it.
3. **City of Chicago:** no permit is needed for non-invasive scanning (E). Downtown sites need COIs and site safety orientation.
4. **OSHA:** excavation rules require that underground installations be located before digging. This is general knowledge and was not re-verified this session.
5. **Insurance:** GL ($1M/$2M; GCs often demand umbrella and additional-insured status), professional/E&O for mis-locates, commercial auto and WC.
   - Indicative averages of GL $45/month and E&O $88/month are floors [D, DF-S034]. They are modelled at $750/month combined (E).
6. **Credentials:** manufacturer GPR training plus NDT Level I-type courses at about $1,000 per level [D, C3-S024]. CSDA GPR certification is used by competitors [D, DF-S031].

## 10. Operations workflow
**From request to cash:**
1. Request (phone, web, foreman text) → schedule within 24–48 h.
2. Site arrival with JULIE ticket check and safety orientation.
3. Scan or locate, then field-mark the slab or ground.
4. Same-day PDF report with photos and depth estimates; CAD/GIS export for utility work.
5. Invoice via QuickBooks or field-service software; net-30/45 collections.

**Who does what:**
- **Human:** all fieldwork, radargram interpretation (liability), site safety, foreman relationships.
- **AI-assisted:** report drafting from field notes and photos, permit-data prospect lists, proposal writing, CRM follow-ups, bookkeeping.
- **Automatable:** scheduling confirmations, invoice reminders.

The AI edge is back-office only and stays cheap after December 2026 (modelled at $300/month). Interpretation must remain a certified human's call.

## 11. Competitive position and defensibility
**What could accumulate:**
- account relationships with foremen who core weekly;
- a reputation for zero strikes;
- suburban response-time coverage;
- certifications and GC approved-vendor status;
- a library of building scans for repeat clients (owners re-scan the same buildings);
- possible eventual sale to GPRS or a peer, an active acquirer [D, WS13-S033].

**What limits it:**
- GPRS already sells a "one contact, call to report" model with Chicago crews;
- at least two local specialists and coring firms scan in-house;
- the city's permit count fell 34% from 2019 to 2025 [A, WS10-S010].

**Entry score stays at 4.**

## 12. Key risks and pre-mortem
| Loss level | How it happens | Early warning signs |
|---|---|---|
| **$5k** | Rented locator and GPR for two months, but foremen stay with GPRS or the coring firm's in-house scanner | Fewer than 3 paid jobs from 20 conversations |
| **$25k** | Concrete GPR bought; average visit $450 rather than $600; under 8 repeat accounts at month 9 | ARPC under $500/month; DSO over 60 days |
| **$50k** | First technician plus kit hired at 15 accounts while price and frequency are low (conservative case −$87k in year 3); or a post-tension tendon or conduit strike claim | Account churn over 7% a month; any mis-locate; E&O premium over $12k/year |

**Stress tests (base year-3 operating profit $112k):**

| Stress | Year-3 operating profit |
|---|---|
| Labour +20% | $39k |
| Hiring 30% sooner | −$50k |
| Gross margin −10 pts | $49k |
| Recession (new −30%, churn ×1.5) | $50k |
| Growth takes twice as long | $43k |

Technician cost relative to price per visit is the decisive ratio.

## 13. Validation plan
1. **Price discovery ($0, 2 weeks).** Ask 10 foremen and PMs from the prospect list what they paid for their last scan and how far ahead they booked *(only once the founder authorizes outreach)*. Search public bid tabulations: CPS, Chicago Park District, Cook County, U of I, and other municipal "private utility locating".
   - **Success:** median of at least $550 per half day, and at least 30% of buyers report waits over 48 hours.
   - **Kill:** median under $400, or "the coring company does it free".
2. **Rent-before-buy pilot ($1,500–3,000).** Rent an RD8200 kit ($599/month [B]) and a GPR ($3,000/month or $450/day [D]) for one month after training. Sell 10 paid half-days.
   - **Success:** 10 paid visits and 3 repeat bookings within 60 days.
   - **Kill:** under 5 paid visits.
3. **Insurance and prequalification quote ($0).** Get written GL/E&O indications with GC-standard endorsements.
   - **Success:** under $10k a year.
   - **Kill:** over $20k a year, or unavailable without a track record.
4. **Partner test ($0).** Offer overflow capacity to 3 coring/cutting firms.
   - **Success:** one subcontract job a month.
   - **Kill:** all decline because they scan in-house.

Buy equipment and hire technician #1 only after experiments 1–3 pass and at least 12 repeat accounts are active.

## 14. Revised scores and verdict
| Key | Stage C | Stage D | Why |
|---|---|---|---|
| fcf | 4 | **5** | Base: $112k in year 3 and $200k in year 5, including founder fieldwork. Conservative is negative. |
| roic | 6 | **5** | ~$230k peak funding (with draws) for $112k year-3 operating profit; per-technician capex of $45k |
| access | 6 | 6 | Buyers identifiable from permit data [A]; incumbency of GPRS and coring firms |
| scale | 6 | 6 | Repeatable technician-kit units; multi-metro shown by GPRS |
| resilience | 4 | 4 | Construction-cyclical; permits down 34% |
| entry | 4 | 4 | GPRS, Hard Rock, Butler and coring firms with in-house scanning |
| delegation | 6 | 6 | Trainable, but interpretation liability needs strong QA |
| cash | 6 | **5** | Net-45 receivables plus equipment per technician |
| feasibility | 9 | 9 | No licence identified; avoid survey practice |
| ai | 4 | 4 | Reporting and prospecting only |

**Composite:** raw **5.27**, evidence-adjusted **5.19** (D), versus 5.29 / 5.20 at Stage C.

**Model:**
- base year-3 operating profit **~$112k**, range −$87k to $743k across scenarios;
- plausible milestone ceiling **$500k/yr**, multi-technician and multi-county, five or more years out.

**Verdict: RESERVE (lead reserve of batch DF).**
- **For:** best fit with the founder's technical profile, B2B repeat accounts, A/B-level price anchors and an acquirer exit.
- **Against:** account economics are unproven, the incumbent is strong, and growth needs about $160k or more of funding or equipment finance.
- **Promotion:** to finalist if experiments 1–2 show a half-day price of at least $550 and at least 3 repeat accounts within 60 days of a rented-kit pilot.
