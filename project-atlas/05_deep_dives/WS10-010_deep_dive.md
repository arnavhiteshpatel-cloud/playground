# WS10-010 — Chicago masonry restoration & tuckpointing (Stage D deep dive, batch DB)

Access date 2026-11-28.

| Deliverable | Location |
|---|---|
| Model | `08_financial_models/WS10-010_assumptions.json` / `_model.xlsx` / `_results.json` |
| Prospects (31) | `09_databases/prospects/WS10-010_prospects.csv` |
| Suppliers (9) | `09_databases/suppliers/WS10-010_suppliers.csv` |
| Sources | `05_deep_dives/sources_DB.jsonl`, plus C8/WS10 sources |

> **Verdict: DROP from the finalist set (keep as a documented demand pocket).**
>
> **Demand is the best-evidenced of this batch [A, DB-S001/S002]:**
> - About 1,900 express masonry permits a year, stable from 2024 to 2026.
> - Median job about $15–16k.
> - Condo-association jobs have a median of $48,550.
> - 3,722 addresses carry open exterior-wall, parapet or chimney violations, and only 250 of them pulled a masonry permit in 2024–26.
>
> **The founder still cannot do or supervise the work.** The City licence requires a hired supervising mason and W-2 crews [A, DB-S003].
>
> **The economics are fragile:**
> - **Base case:** year-3 operating profit about $65k, year-5 about $162k.
> - **Peak funding:** about $108k including the owner draw ($83k without it).
> - **Stress tests:** year 3 turns negative on a 20% labour-cost rise (−$14k), a 10-point fall in gross margin (−$7k), or growth taking twice as long (−$34k). A 40% lower win rate or a recession keeps year 3 positive ($53k and $70k; crew staffing is lumpy) but raises peak funding to $322k–$339k.

## 1. Specific initial niche
**Initial niche:** facade repair (tuckpointing, lintels, parapets, chimneys) for 2–6 flats and small condo associations of 6–30 units on Chicago's North and Northwest Sides.

**Sold through:**
- property-management firms that already buy masonry repeatedly;
- owners and associations with open City masonry violations.

**Out of scope:** high-rise facade programmes (swing stages, critical-examination work), which need more capital and insurance.

## 2. Named operators
| Operator (2025 express masonry permits as "mason contractor") | Permits | Capped reported cost | Level |
|---|---|---|---|
| Batiste Masonry | 86 | $1.19M | A |
| Continental Style Tuckpointing | 47 | $1.13M | A |
| Star Tuckpointing, Inc. | 39 | $0.67M | A |
| Holton Brother's Inc. | 37 | $1.16M | A |
| Mark C. Construction Corp | 34 | $1.31M | A |
| Jagra Corporation | 34 | $0.85M | A |
| AAA-1 Masonry & Tuckpointing | 28 | $1.16M | A |
| Bulley & Andrews Masonry Restoration (larger restorations) | 24 | $4.26M | A |
| Titan Masonry Enterprises | 23 | $0.87M | A |

All rows are from DB-S001.

**Market structure:**
- **Chicago:** 350 distinct mason contractors appear on 2025 permits, and the top firm holds about 4.5% [A, DB-S001].
- **Illinois (NAICS 238140):** 876 firms with $1.21B in receipts. Firms with 5–9 employees average $1.53M, which is about $232k in receipts and $71k in payroll per employee [C, DB-S036].
- **Margins:** the Census masonry proxy operating margin is 20%, an incumbent average before owner draw [C, WS10-S022].

## 3. Named suppliers and partners
- **Licensing:** City of Chicago DOB mason contractor licence, processed via Continental Testing Services (La Grange) [A, DB-S003; DB-S032]. Fees and conditions are in §9.
- **Materials:**
  - Brickworks Supply, formerly Illinois Brick Company, with yards in Bridgeview, Des Plaines, Naperville and New Lenox [B, DB-S030];
  - Prairie Materials [C, DB-S031].
  - Trade-credit terms are MISSING for both.
- **Access equipment:** scaffold and mast-climber rental (e.g., BrandSafway). Rates are MISSING, and Chicago permits record "Scaffolding" as a work type [A, DB-S001].
- **Labour benchmarks:**
  - IDOL Cook County prevailing wage: brick mason $54.81 plus $41.84 in fringes, about $96.65/h total; laborer about $92.11/h [A, DB-S004].
  - BLS brickmason mean wage for the Chicago MSA: $84,010 [C, DB-S005].
- **Insurance:**
  - Workers' comp class 5022: the Illinois rate is MISSING. The Missouri advisory loss cost of $4.143 per $100 of payroll is used as a proxy [C, DB-S006].
  - Insureon tiny-firm medians (GL $88/mo, WC $213/mo, auto $268/mo) do not fit a three-person height crew [D, DB-S007].
- **Channel:** CAI-Illinois, the community-association industry body [C, DB-S033].

## 4. Named prospective customers (31; see CSV)
**22 property managers and owners with repeat 2024–26 masonry permits [A, DB-S001]:**
- Prairie Shores Management (16)
- Broad Shoulders Management (17)
- Peak Properties (17)
- Planned Property Management (15)
- Pro Invest Management (15)
- Cagan Management Group (13)
- FirstService Residential Illinois (11)
- Seminary Properties (10)
- Eastlake Management (10)
- Group Fox (9)
- ICM Properties (8)
- Premier Management Services (8, mostly condo associations)
- The Habitat Company (7)
- Sudler (6)
- First Community Management (6)
- Kass, Bass, Third City, Bertsch, Laramar, Associa Chicagoland and Mercy Housing Lakefront

**9 condominium associations with OPEN masonry violations and recent masonry permits [A, DB-S001/S002]:**
- 1750 N Wells
- 2930 Sheridan Tower
- 501 W Belmont
- Dorchester Green
- Hale Avenue
- Leland Manor
- Towers (1221 N Dearborn)
- 6929 Crandon
- Whipple Estates

Individuals are not recorded. Websites were recorded only where the page was fetched and matched; seven managers and all nine associations are listed as "MISSING".

## 5. Representative transactions
| Job | Revenue | Direct costs | Contribution | Evidence |
|---|---|---|---|---|
| A. 3-flat: 450 sq ft repoint, 2 lintels, coping (express permit) | $17,500 | crew 162 h $6,640; materials $1,350; scaffold $900; permit $375; dumpster $450; silica consumables $250 = **$9,965** | **$7,535 (43%)** | Price near the 2025–26 median [A]; costs E |
| B. 12-unit condo: 1,800 sq ft repoint + parapet rebuild | $48,000 | crew 432 h $17,710; materials $3,800; mast climber $4,500; permits/right-of-way $900; debris/protection $1,400 = **$28,310** | **$19,690 (41%)** | Condo median $48,550 [A]; costs E |
| C. Violation-driven chimney rebuild (2-flat) | $6,500 | **$3,710** | **$2,790 (43%)** | 1,468 chimney violations 2025–26 [A]; price E |

**Payment timing:**
- Residential jobs: about 1/3 deposit, balance at completion (Home Repair Act paperwork for jobs over $1,000 [A, WS18-S011]).
- Condo boards: progress draws plus 10% retainage (E).

**Permit cost per square foot:** the median is $54/sq ft for 100–499 sq ft jobs and $27.50 for 500–1,499 sq ft jobs [A, DB-S001]. The figure includes lintel and rebuild work, and the cost is applicant-reported.

## 6. Customer acquisition
**Customer #1 (before hiring a crew):**
- Market to violation addresses and property-management firms.
- Refer the first 3–5 signed jobs to an established licensed mason contractor for a disclosed referral fee. This proves lead-to-job conversion without payroll. The founder may not perform or contract mason work unlicensed [A, DB-S003].

**Customers #2–20:**
- Hire the supervising mason and crew unit 1.
- Work property-management portfolios: one manager buys 5–17 jobs over three years.
- Run condo-board proposals with photo or drone condition reports and a 5-year repair schedule.

**Customers #21–100:**
- An estimator role.
- Google LSA/search.
- A CAI-Illinois partner membership.
- A second crew unit.

**Funnel (base, E):**
- 20 estimate requests a month, of which 50% get a site visit and proposal, and 25% of proposals are won: about 2.5 jobs a month.
- Referrals add 1.5 per 100 past customers per month.

**Unit economics:**
- CAC: about $450 per job plus $800/mo fixed marketing.
- Contribution: about $7.5k per median job.
- **Founder time:** 20+ hours a week on sales and estimates in season, plus permits and payroll.

## 7. Pricing strategy
- **Price on measured quantities, not hours:** about $30–45/sq ft for small repoint jobs (inside the A-level permit range), $350–600 per lintel, and parapet rebuild per linear foot (E).
- **Condo work:** priced as a multi-year programme.
- **Never chase the permit-data median:** reported costs understate contract values, and 25% of permits are under $7,500 [A].
- **Deposit:** one-third, with weekly progress billing on jobs over $25k.
- **Model ticket:** $17,500 average (A-anchored, E-mix).

## 8. Working capital and cash conversion cycle
| Jobs per year | Average revenue/month | AR (DSO ~12) | AP (DPO 25) | NWC + winter carry |
|---|---|---|---|---|
| 10 | ~$15k | ~$6k | ~$3k | ~$3k plus crew idle cost (a 2-person crew is ~$15.5k/mo) |
| 50 | ~$73k (peaks ~$100k) | ~$29–40k | ~$14k | ~$20–30k, plus ~$30k winter payroll if crews are kept |
| 200 | ~$290k | ~$115k | ~$55k | ~$60k, plus retainage ~$35k and winter carry |

**Capex:** about $38k at start (truck, scaffold, silica-controlled tools), plus about $6k per added crew unit.

**Model peak funding:**

| Scenario | With owner draw | Without owner draw |
|---|---|---|
| Base | ~$108k | ~$83k |
| Optimistic | ~$44k | — |
| Conservative | ~$808k (a business that would be shut) | — |

## 9. Regulatory path
1. Form an Illinois LLC.
2. **Recruit and employ a supervising mason** who holds a City exam pass (21+), or who sits the exam: $150 exam plus $150 licence, renewed yearly. The licence lapses if the mason leaves [A, DB-S003]. All mason work must be done by W-2 employees.
3. **No separate Chicago GC licence is needed** for work within mason scope [A, WS10-S004].
4. **Permits:** an express permit for each job. The median fee is $375 [A, DB-S001].
5. **Home Repair and Remodeling Act:** written contract and consumer-rights pamphlet for residences of 6 units or fewer [A, WS18-S010/S011].
6. **Insurance:** WC is mandatory [A, C5-S020]; add GL and umbrella. **Premiums are MISSING**; GL is modelled at $1,500/mo and WC as about 7–10% of payroll (E, against the Missouri loss cost proxy).
7. **Safety and suburbs:** OSHA silica and fall-protection compliance is not re-verified this session. Suburban registration is MISSING.

**Timing:** 2–5 months, driven by the hire.

## 10. Operations workflow
1. **Lead:** a violation list or manager request. *AI drafts the letter; a human sends it.*
2. **Site visit and measurement:** photos and drone. *Human; AI produces the condition report.*
3. **Proposal:** AI drafts the scope and board memo; the estimator prices it. *Human.*
4. **Contract and deposit.**
5. **Permit:** the express permit is filed by the office. *Human.*
6. **Material order and scaffold.**
7. **Crew executes:** supervising mason, plus daily photo logs.
8. **Inspection, final invoice, warranty letter.**

**Software:** CRM/estimating plus Claude, about $180/mo (E).

**AI's role:** it touches perhaps 5% of cost. Labour, materials and insurance dominate.

## 11. Competitive position and defensibility
**What accumulates:**
- property-manager relationships (repeat portfolios);
- a reputation for permit-clean, mortar-matched work;
- a database of building condition histories.

**What does not:**
- the licence (anyone can hire a supervising mason);
- data (violation and permit data are public to all 350 competitors).

Switching costs between jobs are near zero.

## 12. Key risks and pre-mortem
| Loss | How it fails | Early warning |
|---|---|---|
| ~$5k | Referral-phase leads do not convert; no qualified supervising mason applies | <2 signed jobs from 30 estimates; <3 qualified mason applicants |
| ~$25k | Crew hired, then wet spring and slow boards leave it idle; WC quote far above plan | Crew utilisation <60% in May–June; WC above 12% of payroll |
| ~$50k+ | Injury claim or fall on a parapet job → experience-mod spike; key mason quits → licence inactive mid-season | Any OSHA recordable; supervising mason turnover |

**Model stresses:**
- Labour +20% → year 3 about −$14k.
- Gross margin −10 pts → about −$7k.
- Win rate −40% → $53k, with peak funding $322k.

## 13. Validation plan
| # | Experiment | Cost | Success | Kill |
|---|---|---|---|---|
| 1 | Job ad for a City-licensed supervising mason/foreman at $85–95k | ~$400 | ≥3 qualified applicants in 3 weeks | <2 |
| 2 | Broker quote for WC/GL on a ~$200k masonry payroll with height work (founder action) | $0 | WC + GL ≤ 15% of payroll | >20%, or no carrier |
| 3 | Mail 200 open-violation owners and associations a free photo condition report offer | ~$600 | ≥15 estimate requests; ≥3 jobs referred for a fee | <5 requests |
| 4 | Pitch 10 repeat-buyer property managers from the CSV for one trial job each | ~$100 | ≥2 put the firm on a bid list | 0 |
| 5 | Margin check: compare 10 won bids against permit-reported costs | $0 | Win price ≥ permit median | Wins only below median |

Total validation cost is about **$1,100**.

## 14. Revised scores and verdict
| | fcf | roic | access | scale | resilience | entry | delegation | cash | feasibility | ai |
|---|---|---|---|---|---|---|---|---|---|---|
| Stage C | 5 | 6 | 6 | 5 | 7 | 4 | 5 | 6 | 4 | 3 |
| Stage D (revised) | **4** | **4** | 6 | 5 | 7 | 4 | 5 | 6 | 4 | 3 |

**Why fcf and roic fell:**
- **fcf 5→4:** base year-3 operating profit is about $65k.
- **roic 6→4:** about $83–108k at risk for about $65k of year-3 operating profit.

**Composite:** raw 4.79; evidence C (k = 0.85) gives an adjusted score of **4.82**.

**Gates:** G2_LICENSE:WARN. The work-around is the licensed supervising-mason employee, and the business is exposed to that one person.

**Model year-3 operating profit:**

| Scenario | Year-3 operating profit |
|---|---|
| Conservative | −$119k |
| Base | $65k |
| Optimistic | $347k |

**Verdict: DROP.** Revisit only if the founder secures a committed supervising-mason partner with an existing book of business.
