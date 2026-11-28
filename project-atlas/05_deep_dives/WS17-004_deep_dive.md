# WS17-004 — Mobile preventive maintenance for light/medium-duty service fleets (Stage D deep dive, batch DC)

> **Verdict: RESERVE.** Evidence on the economics stays at **D**. The PM price anchors are A-level municipal purchase
> orders, but capacity and conversion are E.
>
> **Base case (model):**
>
> | Metric | Value |
> |---|---|
> | Year-3 operating profit | **$71k** on $842k revenue (60 fleets, 4 technicians) |
> | Year-5 operating profit | $104k on $1.6M |
> | Free cash flow | Negative through year 3, because each technician needs a ~$55k equipped van |
> | Peak funding | $550k ($433k without owner draw) if the vans are bought outright |
>
> **The decisive fact.** After parts (≈31% of revenue), supplies and van running costs, about 61% of revenue is left
> to pay a ~$7k/month loaded technician. A technician generates about $21k/month at full utilisation. Each van
> therefore contributes only ~20–25% of its revenue before overhead.
>
> **What drives the profit:** technician cost and gross margin dominate the tornado (year-3 operating profit runs from
> −$65k to +$208k across ±25% on gross margin). That makes this a labor-arbitrage route business that the founder
> cannot staff personally.
>
> **Why it stays in reserve rather than being dropped:**
> - the Dickinson-to-Cox precedent (C);
> - an A-level list of 528 private fleets with 10–100 power units;
> - it would become attractive if a partner lead technician with his own van (or van leasing) and a higher-margin
>   repair mix were secured.

## 1. Specific initial niche
**What we sell:** overnight and weekend yard PM, plus same-week DVIR-defect repair. PM covers oil and filters,
multipoint and photo DVI, tires, brakes, batteries and wipers.

**Who we sell to:** trade-service and route fleets with **10–100 trucks and vans parked at one yard** in Cook, DuPage,
Lake and Will counties.

**Entry clusters:**
1. Landscape and tree-care fleets in Wheeling, Lake Zurich, Grayslake and Lockport. Their winter downtime is the
   natural PM and repair season.
2. Electrical, HVAC and linen fleets in Franklin Park, Elk Grove Village and Mount Prospect.

**Size of the niche [A, DC-S003]:** the census shows 528 private-property fleets with 10–100 USDOT power units (mean 28)
and 1,009 with 5–100. 106 carry trade-service names. Light vans under 10,001 lb are not registered, so true fleet
counts are higher.

## 2. Named operators
| Operator | Known facts | Level |
|---|---|---|
| Cox Fleet (ex-Dickinson) | Chicago page offers onsite mobile PM and repairs, plus a 65,000+ roadside network. Dickinson started in 1997 in Indianapolis; ~800 techs at sale (2021); 1,500+ techs now | C, DC-S017, C4-S021 |
| Coltrain Onsite Fleet Care | Founded Aug 2025 by Dickinson heirs; ~70 techs in 15 states within a year; prices "on par with a quality shop" | C, C4-S021 |
| Tasca Commercial Trucks of Chicago (Arlington Heights) | Ford Pro Elite heavy-duty service centre plus mobile service units for light-, medium- and heavy-duty trucks | D, DC-S042 |
| Ryder (Torque / SelectCare) | SelectCare & other $680M; FMS earnings before tax 8.6% | A, WS17-S022 |
| Rush Truck Centers | Aftermarket $2.52B; service gross margin 66–68%, parts 28–30%; mobile units for heavy trucks | A, WS17-S021 |
| LubeZone Mobile | On-site oil changes and PM for multiple units per visit; photo reports; refers repairs to partners | D, DC-S018 |
| Wrench | Venture-backed mobile-mechanic platform with a fleet oil-change product | D, DC-S023 |
| Fleet Response; Enterprise/Merchants FMCs | Route maintenance through vendor networks: 55,325 shops (Enterprise), 40,000+ (Merchants) | D/B, DC-S016, C4-S019–S020 |

**Where the competition sits:**
- **Nationals** (Cox, Coltrain, Ryder) chase multi-state accounts.
- **Dealers** (Tasca) push their own brands.
- **Quick lubes and independents** require the drivers to bring the vehicles in.

**Customer complaints** about local providers: not collected, so MISSING.

## 3. Named suppliers / partners (see `09_databases/suppliers/WS17-004_suppliers.csv`)
| Partner | Role | Status |
|---|---|---|
| NAPA (GPC); O'Reilly First Call | Commercial parts accounts with delivery | Terms unpublished, **assumed** |
| Enterprise / Merchants / Fleet Response | Overflow work channels; impose labor-rate caps | **Documented** networks [B/D]; vendor terms assumed |
| Shopmonkey (or similar) | Shop/DVI software; pricing page exists | Plan price not captured [D] |
| Knapheide-type upfitter | Service-van body and fluid dispensing | Capex **assumed** $45–65k per equipped van |
| Safety-Kleen | Used-oil and filter recycling | **Assumed** |

**Parts margin:** taken from Rush's 28–30% [A]. A small operator's actual parts discount is MISSING.

## 4. Named prospective customers
33 organisations are recorded in `09_databases/prospects/WS17-004_prospects.csv`:
- **31 private fleets from the FMCSA census, each with a live website.** Examples, with census power units:
  - landscape and tree care: Bertog Landscape (Wheeling, 58), Homer Tree Service (Lockport, 81), Apex Landscaping
    (Lake Zurich, 95), Western DuPage Landscaping (Naperville, 39);
  - linen and refrigeration service: Mickey's Linen (Chicago, 72), Empire Cooler Service (Arlington Heights, 35);
  - electrical, HVAC and plumbing: Lyons & Pinner Electric (La Grange, 62), Temperature Service Company (Elk Grove
    Village, 62), Calumet City Plumbing (10);
  - roofing: Olsson Roofing (Aurora, 51).
- **Two public fleets with documented outsourced maintenance:** the Village of Buffalo Grove and the City of Rockford.

Status: "prospect — not contacted".

## 5. Representative transactions
| # | Transaction | Revenue | Direct costs | Contribution | Payment |
|---|---|---|---|---|---|
| 1 | Overnight yard PM, 6 vans at a trade contractor: 6 × $130 PM [E, anchored on A] + $520 minor repairs | $1,300 | Oil/filters $228; repair parts $190; technician 9 h × $40.90 loaded [C, C4-S016] $368; fuel/disposal $60 | **$454 (35%)** | Net-30 invoice |
| 2 | DVIR brake job on a Transit van: 2.4 h × $125 labor [E] + $350 parts | $650 | Parts $245; technician 3 h incl. travel $123; consumables $20 | **$262** | Net-30 |
| 3 | Annual 49 CFR 396 inspection, interstate box truck | $150 [E] | Technician 1.25 h $51; forms $5 | **$94** | Net-30 |
| Ref. | City of Rockford POs: oil change + rotation $66; PM on two vehicles $380.50; full service + 6 repairs $1,218 | — | — | — | Municipal PO [A, DC-S019–S021] |

**What the Rockford POs show:** the shop prices a municipality pays (~$66–190 per PM) are the price ceiling for basic
PM. Repairs found during PM (the $1,218 order) are the margin opportunity.

## 6. Customer acquisition
**Customer #1.** Run a winter campaign to 20 landscape and tree fleets in Wheeling, Lake Zurich and Lockport. Offer one
paid trial night: 3 trucks at a discounted $99 PM, with a photo DVI report on every unit. The lead technician joins the
yard walk-through.

**Customers #2–10:**
- Franklin Park / Elk Grove Village electrical, HVAC and linen fleets;
- referrals from parts-store counters and equipment dealers;
- one public quote (Buffalo Grove-type outsourcing).

**Customers #11–100:**
- referrals, at 0.8 per 100 accounts a month [E];
- overflow and vendor work from FMC networks at capped rates;
- route density selling: "we are already in your industrial park on Tuesdays".

**Funnel at full pace (all E):** 15 conversations → 7.5 trial proposals (50%) → 2.25 recurring accounts (30%) a month.

**Effort:** about 15 founder hours a week (yard visits at 6–8 a.m., when fleet managers are present), plus a
technician walk-around for each proposal.

**Unit economics (base):**

| Measure | Value |
|---|---|
| CAC | ~$485 ($300 trial discount and visits + $500/month fixed, ÷ ~2.7 new/month) |
| Contribution per account after parts, van costs and the technician share | ~$345/month |
| CAC payback | ~1.5 months |
| 5-year LTV at 1.5%/month churn | ~$13.7k |

Acquisition is not the problem. The problem is the contribution left after technician pay.

## 7. Pricing strategy
- **Basic PM:** $110–160 per light-duty van, base $130. That covers oil up to ~7 qt, filter, rotation, fluids and a
  40-point photo DVI. Waive the trip charge for 4+ vehicles in one visit.
- **Repairs:** $125/hour, parts at list or cost + 35–40%, with approval by text before work starts.
- **Optional fleet plan:** $35–45 per vehicle per month, covering scheduled PM plus inspection records. It smooths
  revenue for budgeting.

**Price evidence:**
- municipal shop PM at $66–190 per vehicle [A, DC-S019–S020];
- Coltrain prices at quality-shop parity [C, C4-S021].

**Limits:**
- Do not undercut quick lubes. Sell the driver-hours saved: one shop visit costs a driver 1–3 paid hours plus a lost
  service call.
- A local labor-rate benchmark for Chicago is MISSING. Rate caps imposed by FMC networks are unknown.

## 8. Working capital and cash conversion
Model assumptions: ARPC $1,250/month, DSO 40 days, inventory 10 days of COGS, DPO 25 days on COGS (COGS ≈31% of
revenue).

| Accounts | Revenue/mo | AR | Van stock | AP | Net WC | Vans (owned) |
|---|---|---|---|---|---|---|
| 10 | $12.5k | $16.7k | $1.3k | $3.2k | ~$15k | 1 ($55k) |
| 50 | $62.5k | $83k | $6.5k | $16k | ~$74k | 3–4 ($165–220k) |
| 200 | $250k | $333k | $26k | $65k | ~$294k | 12 (~$660k) |

**Cash cycle:** the conversion cycle is about +45 days. Combined with vehicle capex, growth consumes cash. **Van leasing
or financing is essential:** it is assumed available but needs confirming. It would cut spend before first revenue from
~$100k (borderline for gate G1) to ~$45–50k.

## 9. Regulatory path
1. **Entity and tax.** Illinois LLC, EIN, and Illinois Department of Revenue registration for parts sales
   [A, WS16-S036].
2. **Licensing.**
   - No Illinois general mechanic licence was identified. 625 ILCS 5/5-301 licensing targets rebuilders, and its
     applicability to general repair is E (ilga.gov not accessible).
   - A Chicago repair-business licence for mobile work at customer sites is MISSING (chicago.gov not accessed).
3. **Used oil and filters.** Illinois EPA used-oil management rules apply (specifics MISSING). Contract a recycler and
   carry spill kits.
4. **Air conditioning.** EPA Section 609 technician certification is needed for A/C service. Skip A/C in year 1.
5. **Inspections.** Federal annual inspection (49 CFR 396.17) is allowed for interstate units. **Illinois intrastate
   units must be inspected at IDOT Official Testing Stations**, which limits a mobile inspection product line (WS17
   summary).
6. **Insurance.** Garage liability, garagekeepers (customer vehicles in our care), commercial auto for each van, GL and
   workers' comp. Premiums are MISSING; the model budgets $1,200/month (E).
7. **Night yard access.** A written site-access and keys agreement with each customer.

**Timing:** 1–3 months, paced mainly by hiring the technician and upfitting the van.

## 10. Operations workflow (lead → cash)
| Step | Who / what |
|---|---|
| Yard survey: vehicle list, VINs, mileage, PM intervals | Human; AI builds the PM calendar from the VIN list |
| Paid trial night | Technician |
| Recurring route schedule | Software; dispatcher once revenue passes ~$60k/month |
| Night PM with photo DVI | Technician on a tablet |
| Repair quote and text approval | Template, AI-drafted |
| Parts on account, delivered by morning | Counter account |
| Repair visit | Technician |
| Invoice in shop software, net-30 | Automated AR reminders |
| Monthly fleet health report | Generated automatically |

**Stack:** shop/DVI software ~$250/month, QuickBooks, telematics for the vans, small AI tools ~$100/month. AI only
saves admin time. It cannot replace wrenching, so the `ai` score stays low.

## 11. Competitive position and defensibility
**What builds up:**
- **Route density** in one or two industrial corridors: more stops per night raises utilisation, which is the profit
  lever.
- **Vehicle histories** held in our system.
- **Fleet-manager relationships.**
- **A stable technician team.** Coltrain's founders built their firm around technician culture [C, C4-S021].

**What does not build up:** contracts. The norm is no long-term contract.

**The threat:** the national players, already in Chicago, can match the offer, and dealers bundle warranty work. The
defensible slot is the 10–60-vehicle local fleet below national-account thresholds.

## 12. Key risks and pre-mortem
| Loss | Failure path | Early warning |
|---|---|---|
| **$5k** | Cannot hire a capable self-directed night technician at ≤$35/hr; trial nights do not convert | <5 qualified applicants in 3 weeks; <1 of 3 trials converts |
| **$25k** | Van leased and 3 months of technician pay spent with only 3–5 accounts; utilisation <50% | <60 billable hours a month per technician by month 4 |
| **$50k** | Van bought, contractors pay at 60+ days, one comeback or damage claim, technician quits | DSO >55; comebacks >3% of jobs; technician turnover |

**Model stresses (base year-3 operating profit $71k):**

| Stress | Year-3 operating profit |
|---|---|
| Labor cost +20% | −$4k |
| Gross margin −10 pts | −$13k |
| Hires needed 30% sooner | −$71k |
| Recession | $30k |

**The conservative case** (10 vehicles per account, 2.5% churn, 20% win rate) loses about $107k a year. Stop at the kill
criteria in §13.

**Long-run drift:** EV adoption reduces engine PM.

## 13. Validation plan
| # | Experiment | Cost | Success | Kill |
|---|---|---|---|---|
| 1 | **Lead-technician recruiting test:** post a "mobile fleet technician, nights, $30–36/hr" ad and screen applicants | $300–500 | ≥5 qualified applicants in 3 weeks; one willing to take profit share | <2 qualified |
| 2 | **Three paid trial nights,** using a 1099 mobile mechanic with his own van, at 3 landscape/trade fleets | $1–2k (subcontract cost minus revenue) | ≥2 of 3 convert to a recurring schedule at ≥$120/PM | 0 conversions |
| 3 | **Price test:** $110 vs $150 per PM across trial offers | $0 | Conversion holds at $150 | — |
| 4 | **Parts-account and van-lease quotes** (founder-run) | $0 | Parts discount ≥30% off list; van lease ≤$1,300/month | Margin below 60% |
| 5 | **Winter landscape campaign** to 20 fleets | ~$200 | ≥4 bookings | <2 |

## 14. Revised scores and verdict
| Key | Stage C | Stage D | Reason |
|---|---|---|---|
| fcf | 5 | **4** | Base year-3 $71k, year-5 $104k; FCF negative to year 3 |
| roic | 5 | **3** | $433–550k cumulative funding if vans are owned; ~$100k before first revenue |
| access | 6 | 6 | A-level fleet list; short trial-based cycle |
| scale | 6 | 6 | Repeatable van units (Dickinson precedent) |
| resilience | 7 | **6** | PM deferred in recessions; EV drift |
| entry | 5 | 5 | Cox, Tasca and Coltrain already mobile in Chicago |
| delegation | 5 | 5 | Scarce technicians; founder cannot wrench |
| cash | 6 | **5** | Net-30–60 plus parts; ~45-day cycle |
| feasibility | 7 | 7 | No licence identified |
| ai | 4 | **3** | Admin only |

Raw ≈ 4.9; evidence-adjusted (D) ≈ **4.9**.

**Model base case:** year-3 operating profit **$71,311**, year-5 $104k, breakeven month 13. Ten-year cumulative
deployable cash is only ~$56k.

**Verdict: RESERVE.** Revisit only if experiment 2 converts and vans can be leased.

*Limitations:*
- no Chicago fleet PM price list or labor-rate benchmark was found; the PM price is anchored on Rockford POs, which
  are municipal shop prices;
- insurance premiums, parts discounts and the Chicago licence are MISSING;
- capacity and conversion are E.
