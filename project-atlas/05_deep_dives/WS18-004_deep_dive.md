# WS18-004: Lawn fertilization & weed-control subscription route
Stage D · batch DE · 2026-11-28 · model `08_financial_models/WS18-004_assumptions.json` (results in `WS18-004_results.json`)

> **Verdict: RESERVE.** The unit economics are well documented, but entry is crowded and the business depends on CAC.
>
> **Scores:** revised adjusted score **5.16** (raw 5.19, evidence C), against 5.29 at Stage C.
>
> **The decisive fact: incumbents have published their cost structure, and it shows margin is not the problem.**
> - Spring-Green is headquartered in Plainfield, IL. Its 2026 FDD Item 19 shows **gross profit of 68.4%** after materials (12.9%) and direct labor (18.8%).
> - It also shows **$585 average revenue per customer**, **81.2% annual retention**, and **$209k of sales per production truck**.
> - Franchisees spend **7.4% of revenue on local marketing** and get back **$2.62 of new-service revenue per $1** [B, DE-S027, DE-S028].
>
> **Customer acquisition is the problem.**
> - Illinois has 4,949 landscaping firms [C, DE-S002] and had **1,132 IDOA-permitted lawn-care facilities** as of 2011 [A, DE-S033].
> - TruGreen, Spring-Green, Weed Man and Lawn Doctor all sell in the same subdivisions.
> - If CAC doubles from $210 to $420, base year-3 profit falls from **$48k to −$6k**.
>
> **The model.** Base year 3 is **$48k** (429 customers) and year 5 **$98k** (704 customers). Peak funding is **$74k before draws** ($141k with a $4k/month draw).
>
> **The Stage C containment finding still holds, but it is cheap to satisfy.**
> - A turf-pesticide loading or rinse area needs an IDOA permit before first use, at **$250 per 5-year permit**.
> - Rigs of 100 gallons or less qualify for a **General Class A portable pad** [A, DE-S030, DE-S031, DE-S032].

## 1. Specific initial niche
The niche is auto-renewing **5–6 application fertilization and weed-control programs** for single-family homes in dense 1990s–2010s subdivisions of **DuPage and Will counties**: Naperville, Bolingbrook, Plainfield, Romeoville, Shorewood and New Lenox.

- **Sales channels:** instant aerial-measured quotes, direct mail and door hangers by subdivision.
- **B2B partners:** maintenance landscapers (mow-only crews) and HOA management companies.
- **Equipment:** the founder holds the IDOA commercial applicator licence with the Turf category and runs one truck with a ≤100-gal skid sprayer.

## 2. Named operators
| Operator | What is known |
|---|---|
| **Spring-Green** (HQ Plainfield, IL; franchisor) | 2026 FDD, Item 19 (CY2025): 72 franchised businesses averaged $1.12M in gross sales, median $929k, range $123k–$5.36M; single-territory average $774k. Revenue per customer $585 (range $401–$967); GP 68.4%; retention 81.2%; 385 trucks [B, DE-S027]. CY2024 GP was 68.1% [B, DE-S028]. |
| **Weed Man** (franchise) | 149 US units averaged $2.04M; bottom quartile $347k; low $96k (CY2025) [B, WS18-S007]. |
| **Lawn Doctor** (franchise) | 675 locations. Units open 2+ years averaged $1.17M in net revenue, median $616k, low $15k. Royalty 10%, marketing fund at least 5%, technology fee $150–$250/month; initial investment $135.8k–$163.9k [C, DE-S029]. A local unit, *Lawn Doctor of Antioch, Gurnee & Lake Villa*, is a Landscape Illinois member [C, DE-S034]. |
| **TruGreen** | National #1, private; economics MISSING. |
| **Chicago-area independents** (Landscape Illinois directory) | Emerald Lawn Care, LawnWorks Lawncare, Greenwise Organic Lawn Care, Flora Lawn Care & Landscaping, McGinty Bros. Lawn & Tree Care (also holds ILG87 aquatic coverage [A, DE-S025]), SavATree & SavaLawn, Turf Care Enterprises [C, DE-S034]. Sizes MISSING. |

The two FDDs show the spread inside branded systems: Lawn Doctor's lowest unit was $15k and Spring-Green's lowest $123k. Small units are common even with a brand behind them.

## 3. Suppliers and partners
See `09_databases/suppliers/WS18-004_suppliers.csv`.

| Supplier | What we found | Status |
|---|---|---|
| **SiteOne Landscape Supply** (incl. LESCO) | Site blocked from this environment | Assumed; Illinois branches and Partners Program not verified |
| **Helena Agri-Enterprises** | Account portal exists | Assumed |
| **Harrell's** | Store locator needs a ZIP code | Illinois presence unverified |
| **Target Specialty Products** | Free delivery over $500 [B, DE-S044] | Documented |
| **LebanonTurf** | Sells through distributors | Assumed |
| **BWI Companies** | Footprint is Mid-South and Southeast | Likely does not serve Illinois |
| **Jobber** | Core $49/month, Connect $139/month [B, DE-S035] | Documented |
| **RealGreen** | Price not published | Assumed |
| **IDOA containment permit** | $250 [A] | Documented |
| **Spring-Green franchise** | Alternative entry route; Items 5–7 not retrieved | Documented existence |

**Material cost** is anchored to Spring-Green's 12.9% of revenue [B]. Product price lists are MISSING because distributors gate them behind accounts.

## 4. Named B2B partners and prospects
Households are not listed. `09_databases/prospects/WS18-004_prospects.csv` holds **29 organizations**:
- **FirstService Residential (Illinois)** and **Associa Chicagoland**: HOA management, controlling townhome-association turf contracts and resident vendor lists [C, DE-S036, DE-S037].
- **CAI Illinois**: channel to community-association managers.
- **Campton Crossings Unit 1 HOA**: a self-managing HOA with its own ILG87 coverage [A, DE-S025].
- **25 maintenance-focused Landscape Illinois members** that could subcontract or refer fertilization, for example A-1 Landscaping & Maintenance, Kuhn's Lawn & Snow Service, Lawnscape Maintenance Co., PTL Landscaping & Maintenance, Three Brothers Landscaping & Maintenance and Sitarz Landscape & Maintenance [C, DE-S034]. Their licences and need are unverified.

All are "prospect — not contacted".

## 5. Representative transactions
| Transaction | Revenue | Direct costs | Contribution |
|---|---|---|---|
| 6-application program, ~7,000 sq ft lot | $450/yr (E; below Spring-Green's $585 [B]) | Product 13% $59; labor 6 × 0.4 h × $28 = $67; fuel $20; card fees $13 | **$291 (65%)** |
| Core aeration add-on | $150 | Labor $28; aerator $12; fuel $5 | **$105** |
| Grub-control add-on | $90 | Product $18; labor $8 | **$64** |
| Benchmark: mature Spring-Green franchisee | $1.12M | Materials $144k; direct labor $211k; local marketing $83k [B] | Royalties, overhead and owner pay not shown |

**Payment timing:** card on file, billed per application or prepaid with a discount (DSO about 5 days, E).

**Model results (base case):**

| Item | Value |
|---|---|
| Revenue in year 3 / year 5 | $193k / $365k |
| Operating profit by year | −$35k / $13k / **$48k** / $74k / **$98k** (years 1–5) |
| Breakeven month | 16 |
| Conservative case | Year 3 −$17k (137 customers) |
| Optimistic case | Year 3 $159k (927 customers) |

**Tornado ranking:** gross margin, then revenue per customer, then CAC.

**Stress tests:**
- CAC doubles → year 3 −$6k;
- hires needed 30% sooner → year 3 $14k;
- recession (new customers −30%, churn ×1.5) → $30k.

## 6. Customer acquisition
| Stage | Approach |
|---|---|
| **#1** | Founder door-to-door in one 400-home subdivision in March, with instant quotes and a first-application guarantee. |
| **#2–10** | Neighbours of #1 (yard signs), Nextdoor/Google, one mow-only landscaper referral partner. |
| **#11–100** | 5–10k-piece direct-mail waves to 3–4 subdivisions; an HOA resident-vendor listing through FirstService/Associa managers. |
| **#100–700** | Repeat mail, referrals (1.5 per 100 active customers per month, E), add-ons. |

- **Funnel (E):** 60 quote requests a month (annual average; the season peaks Feb–May) → 85% quoted → 28% won, about **14 new customers a month**.
- **Unit economics:** CAC $210 (Spring-Green's ratios imply ~$223 [B]). Lifetime value ≈ $42 × 86% / 2% ≈ $1,800 of gross profit. Payback on gross profit is about 6 months, roughly one season.
- **Founder time:** 20–30 hours a week selling in spring, then applying from April onward.

## 7. Pricing strategy
- **Revenue per customer:** set the base at $504 a year, below Spring-Green's $585 average and inside its $401–$967 range [B]. Raise it with aeration, grub and overseeding add-ons.
- **Per-application prices** in Chicago are MISSING; competitors do not publish them. Use lot-size tiers from aerial measurement.
- **Billing terms:** prepay discount of about 5% and auto-renewal with clear cancellation, to avoid the auto-renewal complaints alleged against large players.

## 8. Working capital and cash conversion
Customers prepay or autopay, so receivables are negligible. The cash need is **seasonal**: product is bought in Feb–Mar (about 13% of annual revenue) and marketing is spent Jan–May, before most applications are billed.

| Customers | Annual revenue | Spring outlay before revenue | Winter fixed costs to cover |
|---|---|---|---|
| 10 | $5k | ~$2k (mostly marketing) | — |
| 50 | $25k | ~$15k | — |
| 200 | $100k | ~$13k product + ~$35k marketing + $9k shop/insurance | — |
| 700 | — | — | ~$40k+ |

## 9. Regulatory path
| Step | Requirement | Cost and timing |
|---|---|---|
| **1. IDOA licences** | Commercial applicator licence: General Standards exam (100 questions, 70+) and Turf exam (50 questions, 35+), online-proctored. Operators $240. Certificate of insurance or surety bond (415 ILCS 60/10) [A, C2-S026, WS18-S019]. | $300 for 3 years; exams Dec–Feb |
| **2. Lawn-care containment permit (8 IAC 256)** | Needed for each area used to load turf pesticides or capture spills and rinse water, **before use**. Fertilizer-only handling is exempt [A, DE-S030]. Rig choices: **General Class A** portable pad for ≤100-gal liquid or ≤100-lb dry devices; Class B fixed small-device pad; Class C for larger rigs (120% of the largest tank) [A, DE-S031]. Submittal includes site map, plot plan, water-supply and backflow schematic, and PE plans where required [A, DE-S032]. | $250 per application or renewal, 5-year term; processing time MISSING |
| **3. Lawn Care Products Application and Notice Act** | Posting and notification duties. Text not retrievable (ilga.gov unreachable); MISSING. | — |
| **4. Home Repair and Remodeling Act** | Does not apply; landscaping is excluded [A, WS18-S010]. | — |
| **5. Insurance** | General liability with pesticide drift coverage, plus commercial auto. No quotes obtained. | ~$450/month (E) |

## 10. Operations workflow
1. Lead via mail, door or web.
2. Aerial measurement and instant quote; card on file.
3. Route schedule by subdivision.
4. Load at the permitted pad.
5. Apply, post markers and leave a service note.
6. Autopay.
7. Renewal in November–February.

**Human work:** application, door-to-door selling, complaint calls.

**Automatable or AI-assisted:** quoting from imagery, routing, reminders, reviews, mail targeting.

AI here matches incumbents rather than beating them; aerial quoting is industry standard.

## 11. Competitive position and defensibility
**What accumulates:** subdivision density (more stops per hour, referral flywheel) and the renewal base. Retention runs 65–93% even inside Spring-Green [B].

**Weaknesses:** no brand or national advertising, against franchises that pay 15%+ of revenue for theirs. Easy switching every spring.

**Possible edge:** bundling with pond and aquatic work (WS13-016) uses the same licence, trucks and HOA buyers. Mosquito work (separate category) and holiday lighting can fill the shoulder seasons.

## 12. Risks and pre-mortem
| Loss level | How it happens |
|---|---|
| **$5k lost** | Spring mail produces fewer than 1 lead per 200 pieces, so the first season ends with under 50 customers. |
| **$25k lost** | Truck, rig and pad bought; CAC above $350; churn above 30% after a drought year or a drift or turf-burn complaint. |
| **$50k lost** | Second truck and applicator hired on 350 customers whose retention falls; winter fixed costs drain cash. |

**Early warnings:**
- quote-to-win below 20%;
- CAC above $300;
- first-renewal rate below 75%;
- revenue per customer below $430.

## 13. Validation plan
| Test | Cost | Success | Kill |
|---|---|---|---|
| Pass IDOA General Standards and Turf exams | ~$300 + proctoring | Licence before March | — |
| Door hangers plus 3,000 mailers to 2 subdivisions (after authorization) with an instant-quote page | ~$1,800 | ≥25 paid prepay sign-ups (CAC ≤$75 in mail spend) | <10 sign-ups |
| Referral or subcontract offer to 10 mow-only landscapers | $0 | ≥2 send paying customers | 0 |
| Season-1 retention check (Nov–Feb renewals) | $0 | ≥75% renew | <65% |
| Compare with the Spring-Green franchise: obtain Items 5–7 and 19 and check territory availability | $0 | Franchise owner economics beat the independent case after fees | — |

## 14. Revised scores and verdict
| Key | Stage C | Stage D | Why |
|---|---|---|---|
| fcf | 4 | 4 | Base year 3 $48k, year 5 $98k |
| roic | 5 | 5 | $48k on $74k |
| access | 6 | 6 | Homeowners reachable, CAC ~$210 |
| scale | 6 | 6 | Repeatable trucks; Spring-Green units reach $1M+ over long tenure |
| resilience | 6 | 6 | Discretionary but recurring |
| entry | 4 | **3** | National franchises plus ~1,100 permitted facilities; CAC-doubling stress wipes out profit |
| delegation | 6 | 6 | |
| cash | 8 | **7** | Prepay, but spring outlays and a winter gap |
| feasibility | 7 | 7 | Containment permit $250 with portable pad |
| ai | 4 | 4 | |

**Composite:** raw 5.19, evidence-adjusted 5.16 (C).

**Year-3 operating profit:** low −$17k, **base $48k**, high $159k.

**Ceiling:** $250k a year (about 2,000 customers and 5 trucks).

**Verdict:** **RESERVE.** Strongest as the core of a combined turf-plus-aquatic applicator business, not on its own.
