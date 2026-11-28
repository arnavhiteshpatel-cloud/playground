# WS18-035 — Garage door repair & installation: Stage D commercial deep dive (batch DF)

> **Verdict: RESERVE.** Revised evidence level **D**: revenue and cost structure are B, owner profit is D. Researched 2026-11-28.
>
> - **Owner economics now exist.** A one-employee garage door firm in the NW Chicago suburbs lists $472k revenue and $171k SDE (36%). A seven-employee St. Louis firm lists $2.27M revenue and $317k cash flow (14%) [D, DF-S004, DF-S005].
> - **Franchise data set the ramp and the cost of goods.** Access Garage Doors franchisees average $226k in year 1, $731k in year 2 and $1.02M in year 3, with product COGS of 46–47% [B, DF-S001].
> - **A new entrant's problem is buying demand.** Our driver model (founder plus capacity-hired technicians, every job paying for a lead) gives a **base year-3 operating profit of ~$95k on ~$951k revenue (10%)**, rising to ~$129k in year 5.
> - **The conservative case loses money.** At a $450 ticket and $150 per job acquisition cost it runs about −$64k in year 3.
> - **Where the profit is decided:** ticket size and lead cost, not technician productivity.
> - **No structural opening.** Precision (Neighborly) covers every Chicagoland county [DF-S003], and Clopay lists 18+ authorized dealers around Chicago [B, DF-S010].
> - **Supply is not open from day one.** Raynor requires $100k/yr of purchases [B, DF-S009] and SSC sells to approved dealers only [B, DF-S011].

## 1. Specific initial niche
Flat-rate garage door **repair** (springs, cables, rollers, openers, off-track doors) and replacement doors for:
- owner-occupied single-family homes and townhomes in **NW Cook and north/central DuPage** (Arlington Heights–Palatine–Schaumburg–Elk Grove–Itasca–Bloomingdale–Lombard);
- a **B2B referral layer** of community association management (CAM) firms (townhome and condo associations, parking-garage doors), licensed home-inspection firms and residential brokerages.

Commercial dock and rolling-steel work, gates and Chicago-city electrical work are excluded at launch.

## 2. Named operators
| Operator | What is known |
|---|---|
| **Precision Garage Door Service (Neighborly)** | 147 U.S. franchised units. 2025 avg ticket $1,213 (2024: $706). Smallest-territory avg sales $1.38M, median $858k [B, C8-S019/C8-S020]. Chicago pages cover Cook, DuPage, Lake, McHenry, Kendall, Kankakee, Aurora and Naperville [D, DF-S003]. |
| **Access Garage Doors** (franchise, Chattanooga HQ) | 13 franchisees. 2024 avg $718k, median $390k. COGS 46.3%. Affiliate territory $6.29M. Year-of-operation averages $226k → $731k → $1.02M → $1.20M [B, DF-S001]. No Chicago unit verified. |
| **ProLift Garage Doors** (franchise) | 70 locations. FY2024 avg $511k. Top quartile $1.03M; bottom quartile $162k. Royalty 6% + marketing 2% + contact centre 2% + $295/wk fees [B, DF-S002]. |
| **A1 Garage Door Service** | National premium brand. Advertises $350–750 per single spring and a $199 emergency trip fee [D, DF-S037]. Chicago presence not verified. |
| **Raynor Door Company** (Chicago-area Raynor dealer) | Publishes Chicago cost guides: spring pair $250–400, cables $150–250 [D, DF-S036]. |
| **Clopay authorized dealers** | Andy Ryba Garage Doors (Algonquin), Consolidated Garage Doors (Batavia), A-All Style (Bolingbrook), Innovative Door (Downers Grove), Builders Chicago (Elk Grove Village), Sears Garage Doors (Glenview), Anagnos Door (Justice), Aero (Libertyville), Allied and Buckeridge Door (Lombard), Illinois Garage Door (Northbrook), Four Seasons (Roselle), CF Garage Door Wholesale (Volo) [B, DF-S010]. |
| **NW-suburb independent** (anonymous listing) | Est. 1983, 1 employee. $472k revenue, $171k SDE, 3-year average SDE $193k. Asking $550k [D, DF-S004]. |
| **Chicago licensees** | 14 unexpired Chicago licences carry "garage door" in the business name (13 entities, mostly home-based "Home Repair Services"). 4–11 new issuances a year [A, DF-S014]. |

Two readings:
- The trade has many small owner-operators and a handful of multi-truck dealers and franchises.
- The "honest flat-rate" wedge is already the marketing line of Precision ("upfront pricing") and of most dealers.

## 3. Suppliers and partners (`09_databases/suppliers/WS18-035_suppliers.csv`)
| Supplier | Terms found | Status |
|---|---|---|
| **Raynor** (Dixon IL) | Dealer must plan ≥$100k/yr Raynor purchases. Approved credit terms. No credit cards [B, DF-S009]. | Documented. Not reachable in year 1. |
| **Clopay** | 3,000+ dealers. "Become a dealer" application. Criteria not published [B, DF-S010]. | Assumed. Confirm minimums. |
| **Service Spring Corp (SSC), Chicago service center** | Dealer-only application. Orders staged in ~2 h. Delivery Direct needs 3 doors or a $3,000 minimum [B, DF-S011]. | Documented. Approval criteria MISSING. |
| **DDM Garage Doors** (West Chicago) | Public online prices. 112 residential torsion springs at $35–88 each (median $52). LiftMaster heads $456–880. Wholesale dealer list suspended [B, DF-S012]. | Documented. **Day-one supplier.** |
| **CF Garage Door Wholesale** (Volo) | Clopay advanced dealer that stocks parts for installers [D, DF-S013]. | Assumed. |
| **LiftMaster / Chamberlain** (Oak Brook) | Dealer page not found. | Assumed. |
| **Housecall Pro** | $59–329/mo [B, DF-S035]. | Documented. |
| **Google LSA; Insureon** | LSA garage-door leads reported at $15–49 [D, DF-S008]. Insurance averages are floors [D, DF-S034]. | Assumed. |

**Implication:** springs and parts are buyable on day one at public prices. Openers and doors at dealer cost require an approved account. At DDM's public price an installed opener at $750 *loses* money (see §5), so getting an SSC/Clopay account by month 3–6 is a gating task.

## 4. Named prospective customers (`09_databases/prospects/WS18-035_prospects.csv`, 32 organizations)
All are prospects, not leads; none has been contacted.
- **CAM firms (17)**, all with active IDFPR licences [A, DF-S023]:
  - FirstService Residential Illinois, Associa Chicagoland (Vanguard Community Management), Sudler, The Habitat Company, Foster/Premier
  - Red Brick Community Management, Association Partners, Condominium Management Services, MGD Property Specialists, Vista Property Management
  - McGill Management, Clearview Management, Advantage Management, W. L. Seymour, Premier Community Management, Property Specialists Inc., Community Management Solutions
- **Licensed home-inspector entities (8)** [A, DF-S024]: White Glove Building Inspections, HBI Inspection Services/The BrickKicker HQ, Spyglass Property Inspections, Inspect All Home Consultants, Pinnacle Property Inspection Services, Chicagoland Home Inspectors, Insight Property Services, Carroll Inspections.
- **Brokerages (5)** [A, DF-S025]: @properties, Baird & Warner, Compass Illinois, Berkshire Hathaway HomeServices Chicago, Coldwell Banker.
- **Light-commercial tests (2)**, both with Chicago self-storage licences [A, DF-S021]: CubeSmart, U-Haul.

## 5. Representative transactions (paid at completion unless noted)
| Job | Revenue | Direct costs | Contribution |
|---|---|---|---|
| Torsion-spring pair, 16×7 door | $395 | springs $104 (DDM public [B]), hardware $25, tech 1.5 h $60, fuel/card $24, lead $110 | **$72 (18%)** |
| Opener replacement, LiftMaster 6580L | $750 | head unit $592 (DDM public [B]), rail/accessories $40, tech $80, fuel/card $45, lead $110 | **−$117** at public price. Needs dealer cost (MISSING) or a ≥$900 price. |
| New insulated steel door 16×7, installed | $2,200 | door $1,100 (assumed ≈ Access 46–47% COGS [B]), two-person install $320, disposal $25, fuel/card $130, lead $110 | **$515 (23%)**. 50% deposit; Home Repair Act contract. |

**Reading:**
- Repair jobs only become attractive when the lead is free (repeat, referral or B2B), which would lift the spring job to ~$180.
- Prices are D-level (Chicago dealer guides, competitor pages). The founder must benchmark prices before launch (§13).

## 6. Customer acquisition
- **Customer #1.** A home-inspector or CAM referral, or a Google Business Profile listing with posted flat prices, after 2–3 months of training (ride-along/apprentice or manufacturer courses; MISSING) and insurance.
- **Customers #2–10.** Google LSA (pay per lead) plus neighbours of the first jobs.
- **Customers #11–100.**
  - CAM firms: vendor applications, COI on file, a written maintenance-visit offer for association parking-garage doors.
  - Brokerage office presentations.
  - Review accumulation to climb LSA rankings.
- **Funnel (base):**
  - At plateau (month ~30), inbound leads ≈ 240/month.
  - 65% book a visit (Searchlight LSA book rate 38% is a floor [D, DF-S008]).
  - 85% of visits buy, so ~133 paid jobs/month.
  - Ramp evidence: Access franchisees take ~3 years to pass $1M [B, DF-S001].
- **CAC:** $100 per job in base. Blended LSA ($15–49/lead) and search ($81–173/lead) at ~55% lead-to-job [D, DF-S007/S008].
- **Payback and LTV:** first job contribution covers CAC. LTV is low because springs and openers last years; referral/repeat is ~4 jobs per 100 (E).
- **Weekly sales work.** 10–15 h a week once the founder is off the van: CAM and inspector visits, review requests, LSA dispute management.

## 7. Pricing strategy
- **Published flat-rate menu** set near the Chicago dealer band: spring pair $350–425, cable/roller service $175–250, opener installed $650–900, door installs quoted.
- **Why not premium pricing:** Precision's $1,213 average ticket reflects an upsell-heavy premium brand [B, C8-S019]. A1's $350–750 *per spring* [D, DF-S037] shows how high national brands price.
- **Trip fee** of $79–99, credited to the repair.
- **B2B:** a CAM price sheet and annual safety inspection for association parking-garage doors (price E).
- **Model ticket assumptions:** $450 / $575 / $700 (conservative / base / optimistic).

## 8. Working capital and cash conversion
| Scale (paid jobs/month) | Revenue/mo | Receivables (DSO 4) | Parts inventory (20 days of COGS) | Payables (10 days) | Net working capital |
|---|---|---|---|---|---|
| 10 | ~$5.8k | $0.8k | $1.3k | $0.7k | **~$1.4k** |
| 50 | ~$28.8k | $3.8k | $6.7k | $3.4k | **~$7.2k** |
| 200 | ~$115k | $15.3k | $26.8k | $13.4k | **~$28.7k** |

- The cash conversion cycle is ~2 weeks.
- Door deposits (50%) offset door inventory.
- The real capital is vans: about $30k per technician plus $32k for the founder's van and tools.
- Base-case peak funding is ~$76k including a $4k/month owner draw from month 13; ~$48k excluding the draw.

## 9. Regulatory path
1. **Entity and tax.** LLC, EIN, Illinois Department of Revenue registration (sales tax on parts; confirm treatment).
2. **Illinois Home Repair and Remodeling Act.** Garages are covered.
   - Written contract above $1,000.
   - "Home Repair: Know Your Consumer Rights" brochure.
   - Insurance minimums of $100k/$300k bodily injury, $50k property damage and $10k improper repair (as enacted).
   - 3-business-day cancellation for home-solicited contracts (15 days for buyers over 65) [A, WS18-S010/S011].
3. **City of Chicago.** Garage-door firms hold a **Regulated Business License (Home Repair Services)** [A, DF-S014]; the fee is MISSING because chicago.gov fee pages were blocked.
   - The General Contractor licence (Class E $300) may apply to repair work [A, WS10-S004].
   - Opener wiring beyond plug-in replacement needs a licensed electrician in Chicago [A, WS10-S006].
   - The launch geography (suburbs) avoids most of this.
4. **Suburbs.** Contractor registration rules vary by village (MISSING). Check Arlington Heights, Schaumburg and Lombard before launch.
5. **Product safety.** Openers sold in the U.S. must meet UL 325 entrapment-protection requirements (industry standard; not re-verified this session). Technicians must test auto-reverse on every visit.
6. **Insurance.** GL meeting the Home Repair Act and CAM COI demands ($1M/$2M typical, E), commercial auto per van, and workers' compensation once anyone is hired. Insureon averages (GL $45/mo, auto $245/mo, WC $54/mo; construction WC $179/mo) are floors, not quotes [D, DF-S034].

## 10. Operations workflow
- **Lead to visit.** Lead (LSA call, web form, CAM email) → AI-assisted call answering and photo/video triage (human-reviewed) → booked arrival window → technician diagnosis with a flat-rate menu on tablet.
- **On site.** Written estimate (contract plus brochure for jobs over $1,000) → repair → auto-reverse/safety test photos → card payment on site.
- **After the job.** Review request → Housecall Pro job record → parts reorder (DDM/SSC).

| Type | Steps |
|---|---|
| Human | Field work, spring winding, door installs, CAM relationships, pricing judgement |
| AI-assisted | Call answering, photo triage, review responses, CAM proposal drafting, bookkeeping categorisation |
| Automatable | Reminders, invoicing, reorder points |

- **Software stack:** Housecall Pro Essentials $149–189/mo [B], QuickBooks, Google Business Profile, LSA. Modelled at $350/mo including AI tools (E).

## 11. Competitive position and defensibility
Durable advantages that could accumulate:
- review density in a few ZIP codes;
- CAM vendor approvals (sticky once on file);
- inspector and realtor referral habits;
- dealer pricing.

None is structural. The national brands already claim upfront pricing and guarantees, and dealers have showrooms. Mature owner-operators earn high SDE (36% in DF-S004) only after decades of repeat and referral demand, which a newcomer must buy at ~17–19% of revenue. **Defensibility score stays 4.**

## 12. Key risks and pre-mortem
| Loss level | How it happens | Early warning signs |
|---|---|---|
| **$5k** | LSA leads arrive but convert under 40%, and three months pass without a dealer account | Cost per paid job above $150 after 60 leads; SSC/Clopay decline |
| **$25k** | Van bought, founder still slow and unsure at spring work; 25 jobs/month at $400; overhead uncovered | Under 30 paid jobs/month at month 6; callbacks above 5% |
| **$50k** | First technician hired before demand is proven (conservative case: −$64k/yr), or an injury/property-damage claim without adequate coverage | Technician utilisation under 60%; any spring injury |

**Stress tests (base y3 op $95k):**
- CAC doubles: −$68k
- Gross margin −10 pts: ~$0
- Labour +20%: $44k
- Hiring 30% sooner (founder field capacity lower): −$45k
- Recession (new demand −30%): $73k

Churn-based stress rows are not meaningful in a job-based model.

## 13. Validation plan (cheapest real commercial evidence first)
1. **Price benchmark, ~$0, 1 week.** Collect published flat-rate menus from 10 Chicagoland competitors; read 200 Google reviews for price mentions.
   - Success: a median spring-pair price of $300+ is confirmed.
   - Kill: under $250.
2. **Supplier gate, ~$0.** Request SSC dealer and Clopay dealer requirements in writing *(only after the founder authorizes contact)*.
   - Success: an account is achievable with insurance plus an entity.
   - Kill: minimums above $50k/yr or a 12-month track record required.
3. **Paid lead test, ~$600–900.** After training and insurance, run LSA in 6 ZIP codes for 30 days.
   - Success: cost per paid job ≤$100 and ≥15 paid jobs.
   - Kill: above $175 per job.
4. **B2B proof, ~$200.** Pitch 10 CAM firms from the prospect list for a parking-garage-door inspection pilot.
   - Success: 2 paid pilots in 60 days.
   - Kill: 0 after 10 meetings.
5. **Unit economics, ~$0.** Track 50 jobs. Gross margin after parts must be ≥60% and average ticket ≥$500, or stop before buying a second van.

## 14. Revised scores and verdict
| Key | Stage C | Stage D | Why |
|---|---|---|---|
| fcf | 5 | **4** | Base y3 $95k / y5 $129k includes founder field labour; conservative negative |
| roic | 7 | **6** | ~$76k peak funding (with draw) for $95k y3 op; per-van capex $30k |
| access | 6 | 6 | Urgent inbound demand; CAM/inspector channels identifiable [A] |
| scale | 5 | 5 | Single-territory plateau ~$1M revenue; multi-territory is the ceiling |
| resilience | 6 | 6 | Repairs non-discretionary |
| entry | 4 | 4 | Precision in every county; dense Clopay dealer network; dealer-only supply |
| delegation | 6 | 6 | Technician labour market exists (Chicago median $65k [C]) |
| cash | 8 | 8 | Paid on completion; ~2-week cycle |
| feasibility | 8 | 8 | Home Repair Act formalities; Chicago licensing edge cases |
| ai | 4 | 4 | Booking/triage only |

- **Composite:** raw **5.42**, evidence-adjusted **5.29** (D). Stage C was 5.75 / 5.53.
- **Model:** base year-3 operating profit **~$95k**, range −$64k to $634k across scenarios. Plausible milestone ceiling: **$250k/yr** for one territory; $500k only multi-territory.
- **Verdict: RESERVE.** It is a sound, cash-paid trade with documented owner earnings in mature firms. A newcomer has no wedge, supply needs dealer approval, and profit depends on buying leads at ≤$100 per job. Revisit only if experiments 1–3 pass.
