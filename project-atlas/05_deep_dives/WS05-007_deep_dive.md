# WS05-007 — Commercial pest control for Chicago food facilities, with a residential/landlord plan line (absorbs WS18-007)

**Stage D deep dive · batch DA (Chicago commercial building services) · 2026-11-28**

> **Verdict: FINALIST (conditional on a paid 90-day field test).** Revised evidence level: **C**.
> - **Demand is well evidenced (A).** CDPH inspections recorded live pests at 1,416 Chicago food licences in 13 months, 256 of them in the chosen south-west cluster.
> - **Licensing is founder-obtainable (A):** a $75 exam held monthly, a $250 licence, and legal supervision of uncertified technicians.
> - **Capital is small:** about $24k at risk excluding owner draws, $36k including them.
> - **Economics are thinner than Stage C assumed.** The driver model gives base year-3 operating profit of **about $52k** (before owner pay), not $135k. Year 5 rises to about $143k. The conservative case is roughly break-even and the optimistic case about $200k.
> - **The decisive unknown is the founder's close rate** on displacement sales to sites that already have a vendor. It can be measured for under $2k.

---

## 1. Specific initial niche

**Customer × service × geography:**
- **Customers:** independent restaurants, bakeries, independent grocers and wholesale food plants.
- **Service:** monthly integrated pest management (IPM) with inspector-ready digital logbooks.
- **Area:** Chicago's south-west cluster, ZIPs 60608, 60609, 60616, 60623 and 60632 (Pilsen, Chinatown/Bridgeport, Back of the Yards, Little Village, Brighton Park/Gage Park).
- **Second line:** quarterly mouse-and-insect plans for 2–6-flat landlords and homeowners in the same ZIPs. This line shares the licence, technician and van.

**Why this cluster** (analyst queries of CDPH food inspections, 2025-11-03 to 2026-11-25 [A, DA-S001]; licence register [A, DA-S029]):

| Measure | Citywide | SW cluster |
|---|---|---|
| Food licences inspected | 10,606 | 1,572 |
| Cited under violation 38 (insects, rodents, animals) | 2,147 | — |
| Live-pest evidence in inspector comments | 1,416 | 256 (16%) |
| Live-pest evidence in ≥2 inspections | 264 | 46 |
| Active Retail Food licences | 11,223 [C2-S015] | 1,403 |
| Active Wholesale Food licences | 396 | 214 |

Top ZIPs by live-pest licences:
- 60616: 86 of 322 inspected (27%)
- 60647: 61 of 359
- 60611: 55 of 350
- 60608: 54 of 366
- 60628: 53 of 180 (29%)
- 60639: 52 of 323
- 60623: 45 of 251
- 60632: 44 of 348
- 60609: 27 of 285

The five cluster ZIPs are contiguous. They contain the Stockyards/Back of the Yards wholesale food corridor: 214 wholesale licences, mostly meat processors, tortillerias and bakeries, each with an audit-driven pest-documentation need. They also contain a pest-supply branch (Veseris, 3642 S Kedzie Ave) [B, DA-S014].

**What the inspection comments say:**
- Of 3,182 violation-38 comments, 1,267 cite door gaps or openings. That is an exclusion upsell.
- 878 tell the operator to contact or increase pest-control service.
- 181 licences were cited for a missing or incomplete pest logbook [A, DA-S001].

**Residential line (WS18-007).** It is modelled as about 25% of accounts. Its pricing is D-level: Chicago monthly visits run about $40–70 [D, DA-S021]. It uses paid search leads rather than inspection data, so its acquisition cost is higher.

## 2. Named operators

| Operator | What is known | Evidence |
|---|---|---|
| Rollins (Orkin; Vernon Hills IL branch) | 2025 revenue $3.76B; commercial $1.245B (+7.6% organic); gross margin 52.8%, operating margin 19.3%; 26 acquisitions for $309.5M in 2025 | A, C2-S008 |
| Rentokil-Terminix | NA Pest Control 19.7% adjusted margin (H1 2026); customer retention 80.7%; opened 70 small local branches in H1 2026 | B, C2-S009 |
| Ecolab Pest Elimination | Separate segment aimed at restaurants, food plants and grocers; margins not retrieved | A, C2-S011 |
| ABC Humane Wildlife Control & Prevention (Arlington Heights/Schaumburg) | ~40-year firm; City of Chicago O'Hare/Midway integrated pest control contract $4.374M (2024–29) | A, C2-S016 |
| R.B. Pest Solutions | Cook County Facilities pest control $595,500 (Oct 2021–Sep 2024), renewed at $218,800 (2025–26) | A, DA-S024 |
| Quality & Excellence Pest Control | Cook County Sheriff pest control $488,816 (2017–19) | A, DA-S024 |
| D-Bug Enders, Next Step, Chicago Pests LLC (+1) | Bid the same 3-year Waubonsee College job at $19,260–$236,400 (a 12× spread) | A, C2-S018 |
| Rose Pest Solutions, Smithereen | Chicago-area incumbents with restaurant programmes (Rose's page was 403 this session) | C2-S016; D |

**Reading of the field:**
- Nationals hold chains and big public contracts. Local firms win county and college work at widely dispersed prices.
- Small books get bought: Rollins does about 26 deals a year. Acquisition multiples are MISSING.
- **Incumbent economics** (Rollins 52.8% gross margin including technician labour) are not entrant economics. The model below builds entrant costs bottom-up.

## 3. Named suppliers and partners

| Supplier | Role | Terms found | Status |
|---|---|---|---|
| **Veseris**, 3642 S Kedzie Ave, Chicago | Pesticides, rodent stations, traps, equipment | The account form requires a Pesticide Applicator's Licence number, expiry and an attestation; an online credit application exists. Prices and terms are behind login (MISSING) | documented [B, DA-S014] |
| Target Specialty Products | Alternative distributor | Online account creation; Illinois branch unverified | assumed |
| Bell Laboratories | Rodent stations and bait (bought through distributors) | MISSING | assumed |
| GorillaDesk | Routing, invoicing, service reports | Basic $49/mo; Pro $99/mo plus $50 per extra route; Growth $149/mo | documented [B, DA-S016] |
| Insureon (broker marketplace) | GL, auto, WC, professional | Pest-firm averages: GL $112/mo ($1M/$2M), WC $90, professional $58, auto $114 | documented [C, DA-S010] |
| IDPH Structural Pest Control (regulator) | Exam, licence | $75 exam fee (2017 form), $250 per location per year | documented [A, WS05-S012/S013] |

Full detail and follow-up questions are in `09_databases/suppliers/WS05-007_suppliers.csv`. **Requires direct confirmation:** Veseris credit terms for a new licensee, and whether GorillaDesk's reports satisfy CDPH logbook expectations.

## 4. Named prospective customers

`09_databases/prospects/WS05-007_prospects.csv` lists **30 real Chicago organizations**. All are prospects, none contacted.

**23 licences that CDPH recorded with live pest evidence** (each row links its inspection records):
- **Multi-site grocers:** Pete's Fresh Market (3 stores), Fairplay Foods (2), Park to Shop (2), Cermak Fresh Market and 88 Marketplace.
- **Restaurants:**
  - Tacos y Tamales El Pollo, cited 7 times (the most-cited licence in the cluster)
  - La Torta Chilanga #2, cited 5 times
  - MingHin Cuisine (a 6-location group), Shiki Buffet, Tio Luis Tacos, Dongpo Impression, La Catedral Cafe, Fiesta Tapatia and others
- **Bakeries:** Del Refugio and Fat Peach.
- **Institutional kitchens:** two supportive-living facilities (The Montclare, New City).
- **Wholesale:** one wholesale food site (Winfar Foods).

**7 wholesale food plants** from the active licence register: Chicago Meat Authority, Lincoln Provision, Schulze & Burch Biscuit, Amity Packing, Tortilleria Atotonilco, Old Fashioned Meat Co./El Superior, and El Milagro.

Websites were recorded only where the organization's own site was fetched and matched. Others are "MISSING", with the licensed premises given as the walk-in contact point. No individuals are named.

## 5. Representative transactions

| # | Transaction | Revenue | Direct costs | Contribution | Payment |
|---|---|---|---|---|---|
| 1 | Independent restaurant after a live-rodent citation, first year: $200 cleanout/exclusion + 12 × $125 | $1,700 | Materials and devices $210; technician 12 × 0.75 h plus 2 callbacks at ~$28/h loaded = $310; vehicle $110; card fees and bad debt $51 | **$1,019 (60%)** | At service or net-15 |
| 2 | Wholesale food plant, twice-monthly audit-ready programme at $500/mo | $6,000 | Materials and insect light traps $700; technician 24 × 1.5 h = $1,010; audit reporting admin $300; vehicle $190 | **$3,800 (63%)** | Net-30 |
| 3 | 2-flat landlord, quarterly plan ($150 initial + 3 × $150) | $600 | Materials $60; technician $105; vehicle $40; paid lead $150 | **$245 (41%) in year 1**, about $450 in year 2 | Autopay |

**Evidence for the transaction inputs:**
- **Prices.** Transaction 1 is D: restaurants pay $100–150 a month [C2-S020], and one published range is $50–422 [C2-S019]. Transaction 2 is E, anchored on the Waubonsee low bid of about $535 a month for a multi-campus job [A, C2-S018]. Transaction 3 is D [DA-S021].
- **Wage.** Technician labour uses the Chicago median of $46,740 [C, C2-S021].

## 6. Customer acquisition

- **Customer #1:**
  - Pull the inspection feed daily (it is public and needs no API key).
  - Within 72 hours, walk into each cited licence in the cluster, starting with the 46 repeat offenders.
  - Offer a free inspection, a cleanout price and a digital logbook the inspector can see on re-inspection.
  - The re-inspection deadline is the urgency.
- **Customers #2–10:**
  - Same channel, plus bakeries and grocers.
  - Ask every signed owner for two referrals; Chinatown and Little Village operators are dense networks.
- **Customers #11–100:**
  - Add newly licensed establishments (about 124 a month citywide [A, C2-S014]).
  - Add wholesale plant quality-assurance managers, with food-safety consultants and auditors as referrers.
  - Add the landlord line through Google Local Services and Business Profile.
  - Hire a commission-heavy rep only after 300 accounts. Hiring a salaried rep at month 20 cut base year-3 profit to about $4k.
- **Customers #100+:** run route density inside the five ZIPs. Expand to the 60628/60617 and 60639/60647 clusters as a second route.

| Funnel step (base) | Value | Evidence |
|---|---|---|
| Qualified conversations / month at full pace | 45 (conservative 32; optimistic 60) | E |
| Conversation → inspection and proposal | 40% | E |
| Proposal → paying account | 30% | E, a displacement sale; L.E.K. finds about 37% of facility managers switched a provider in the past year [C, DA-S019] |
| New accounts / month (founder) | about 5.4, plus about 1 per 100 active from referrals | E |
| Blended cash acquisition cost | $120 per account (commercial near $0; residential paid leads) | E |
| Contribution per account per month, before labour | about $86; about $65 after technician time | E |
| Expected life at 1.8% monthly churn | about 56 months, so contribution value about $3,600 after labour | B churn [C2-S009] |
| Founder sales time | about 12–15 h a week (8 conversations per win; about 5 h per won account) | E |

## 7. Pricing strategy

**Market price evidence:**
- **Public bids (A):** per-building monthly bids of $30–180 [C2-S017]; Waubonsee bids from $19,260 to $236,400 [C2-S018]; Cook County facilities about $198k a year across many buildings [DA-S024].
- **Restaurant guides (D):** $100–150 a month [C2-S020].
- **Chicago residential (D):** monthly visits about $40–70 [DA-S021].
- No Chicago commercial rate card exists publicly (MISSING).

**Proposed price list:**

| Customer | Price |
|---|---|
| Restaurants | $125/mo |
| Grocers and bakeries | $175–250/mo |
| Wholesale plants (twice monthly with trend reports) | $400–600/mo |
| Initial cleanout/exclusion | $150–300 |
| Landlord plans | $150 per quarterly visit |

**Contract terms:** 12-month agreements, 30-day cancellation, 3% annual escalator. More than 95% of facility managers have escalators in some contracts [C, DA-S019].

**Positioning:** do not lead on price. Public bids show incumbents will go very low. The wedge is speed after a citation, plus documentation. The model's blended recurring revenue per account is $105 (75% commercial, 25% residential).

## 8. Working capital and cash conversion

Base drivers: days sales outstanding 20 (Rollins about 20 [A, C2-S008]); inventory 20 days of cost of goods; supplier credit 25 days, which is unverified. The conservative case assumes 0 days, i.e. cash on delivery.

| Active accounts | Monthly revenue | Receivables | Inventory | Payables | Net working capital |
|---|---|---|---|---|---|
| 10 | $1,050 | $700 | $84 | $105 | **$679** |
| 50 | $5,250 | $3,500 | $420 | $525 | **$3,395** |
| 200 | $21,000 | $14,000 | $1,680 | $2,100 | **$13,580** |

The cash conversion cycle is short, about 15–20 days of revenue. Working capital is not a constraint.

**Capital at risk:**
- Peak base funding need is **$24k excluding owner draws**, or **$36k with a $4k/month draw from month 13**. That covers launch equipment ($5.5k), insurance, storage and early losses.
- The conservative case needs about $71k before draws. The kill criteria below are meant to stop well before that.

## 9. Regulatory path (exact steps)

1. **Certified Technician (CT).** File the General Standards application, plus any category exams, at least 15 days before an exam date. The fee is $75 per the 2017 form [A, WS05-S013]. Exams run roughly monthly at Westchester, with 10 seats per session [A, C2-S005], and the pass mark is 70%. No experience prerequisite is listed. Allow 1–2 months.
2. **Entity.** Form an LLC, obtain an EIN and open a bank account. A Chicago business licence for an office-less service firm is unverified, because chicago.gov returned 403.
3. **Insurance.** Minimums are $100k/$300k bodily injury and $50k property damage, or a $350k combined single limit, filed on the IDPH certificate form [A, C2-S004]. Indicative broker averages are GL $112/mo, auto $114, WC $90 and professional $58 [C, DA-S010]. The model carries $320/mo, rising 6% a year, because Rollins reports a hardening market [A, C2-S008].
4. **IDPH Commercial Structural Pest Control Business Licence.** $250 per location per year, renewed by 1 December. The application lists the employed CT, the certificate of insurance and the pesticide-storage well-distance disclosure [A, WS05-S012]. Processing time is MISSING; the model assumes 2 months to the first sale.
5. **Staff supervision.** Uncertified technicians may apply pesticides after 2 supervised applications per pesticide type per site type. After that the CT must be reachable and able to be on site within 1 hour [A, C2-S002].
6. **Location limit.** A CT cannot be the sole CT for more than one location [A, C2-S003], so a second branch needs a second CT.
7. **Renewals and penalties.** CT renewal every 3 years with 9 classroom hours [A, C2-S007]. Operating unlicensed draws a $1,000 initial fine [A, C2-S006].
8. **Home Repair Act.** It may apply to residential exclusion jobs over $500. Use written contracts [A, WS18-S010].
9. **Risk limits.** No termite warranties early. Rentokil carries $392M of termite provisions [B, C2-S009].

**Unverified:** the statute text (225 ILCS 235, because ilga.gov returned 503) and whether soliciting before licensure is permitted. Recommendation: license first.

## 10. Operations workflow (lead to cash)

1. **Daily data pull** (automatable): a Python/Socrata script ranks new violation-38 records in the cluster by live evidence, repeat status and facility type.
2. **Walk list and pitch** (human, AI-assisted): an AI drafts bilingual (Spanish/Chinese) leave-behinds and cites the public inspection date.
3. **Free inspection and proposal on a tablet** (human). E-signature and card-on-file or autopay.
4. **Initial service** (human): cleanout, stations, door sweeps. The digital logbook is created and a printed binder left on site.
5. **Monthly route** (human, with routing software): GorillaDesk Pro at $99 plus $50 per route [B]. Service reports are emailed automatically. Callbacks within 24 hours.
6. **Billing:** autopay or net-15, with weekly receivables review.
7. **Quality loop:** re-check the CDPH feed for clients' re-inspections. Any repeat citation triggers a free extra service. This is the retention metric.

**Software stack (base about $190/mo):**
- Field-service app $150
- AI assistant $40
- Bookkeeping, phone and web $300 (E)

**What AI does:** prospect ranking, translations, proposals and reports. The treatment itself stays human. After December 2026 the AI line is an ordinary $20–40 subscription; at 3× AI cost, year-3 profit falls only about $1k.

## 11. Competitive position and defensibility over time

**What accumulates:**
1. **Route density** inside five ZIPs, which cuts minutes per stop.
2. **A record of re-inspection passes** for clients, which can be shown with public data.
3. **Wholesale-plant audit files.** These are hard to switch away from mid-audit-cycle.
4. **Saleability.** A recurring book is sellable to active consolidators; Rollins did 26 deals in 2025.

**What does not accumulate:**
- The licence, which anyone can obtain.
- The inspection-data idea, which is public and copyable.
- Rentokil is opening local branches specifically to compete on proximity [B, C2-S009].

The entry score stays at 4.

## 12. Key risks and pre-mortem

| Loss level | How it fails | Early warning |
|---|---|---|
| **$5k** | The CT exam is failed twice, or 60 cited sites yield fewer than 3 paid accounts in 4 weeks, because owners stay with their incumbent | Close rate below 15% in the first 40 conversations |
| **$25k** | Accounts are won but lost to callbacks and restaurant closures (about 10% of inspected licences were "Out of Business" within 13 months [A, DA-S001]); churn above 3% a month | Callbacks over 20% of visits; any client re-cited twice |
| **$50k** | A salaried technician and rep are hired before 300 accounts; the technician quits; a misapplication claim lands. The "hires 30% sooner" stress drives year-5 operating profit negative (−$15k) | Staff cost above 45% of revenue; second-year churn above 25% |

**Stress results (base y3 operating profit $52k):**

| Stress | Year-3 operating profit |
|---|---|
| CAC doubles | $38k |
| Gross margin −10 points | $33k |
| Labour +20% | $41k |
| Insurance and overhead +50% | $39k |
| Growth takes twice as long | $30k |

**Largest sensitivities:** gross margin and revenue per account. A ±25% swing moves year 3 between about $15k and $89k.

## 13. Validation plan (cheapest real commercial evidence)

| # | Experiment | Cost | Success | Kill |
|---|---|---|---|---|
| 1 | Pass the IDPH General Standards exam | about $125 (fee plus manual) | Pass on the first or second sitting | Two failures |
| 2 | Obtain the licence and insurance, then canvass 60 cited licences in the cluster over 4 weeks | about $1,200–1,800 (licence $250, first insurance month, materials) | **≥6 signed paid accounts at ≥$100/mo**, and at least one at ≥$175 | Fewer than 3 paid accounts |
| 3 | Wholesale-plant test: 10 quality-assurance conversations using the licence register | about $100 | ≥1 paid programme at ≥$300/mo | 0 proposals requested |
| 4 | Residential line: $300 of Local Services/Business Profile spend over 4 weeks | $300 | Cost per won plan ≤$150 | Above $300 per plan; drop the residential line |
| 5 | Retention and re-inspection check at month 4 | $0 (public data) | ≤1 of the first 10 cancels; no client re-cited for live pests | ≥3 cancellations |

Total is about $2k. Revenue from experiment 2 is real paid evidence.

## 14. Revised scores and verdict

| Criterion | Stage C | Stage D | Reason |
|---|---|---|---|
| fcf | 5 | **4** | Base year-3 about $52k, year-5 about $143k (driver model); optimistic about $200k / $480k |
| roic | 7 | **6** | Year-3 operating profit ÷ $36k peak funding ≈ 144%; ≈ 400% by year 5 |
| access | 6 | 6 | A-level public prospect list, but displacement sales |
| scale | 6 | 6 | Branch replication needs a CT per location |
| resilience | 7 | 7 | Code-driven, low cyclicality; restaurant closures |
| entry | 4 | 4 | Copyable wedge; nationals localising |
| delegation | 7 | 7 | Supervision rule verified |
| cash | 7 | 7 | DSO about 20; small inventory |
| feasibility | 8 | 8 | Licence path A-level |
| ai | 4 | 4 | Prospecting, reports, translation |

**Composite:** raw score about **5.67**; evidence-adjusted (C, k = 0.85) about **5.57**, against 5.85 at Stage C.

**Model milestones (base):**
- First profitable month: month 11
- $5k/month operating profit: month 22
- $10k/month: month 49
- $25k/month: not reached in 5 years (optimistic: month 43)

**Plausible ceiling:** $250–500k/yr with 3–4 routes in years 6–10. A capable entrant reaching that would be a top-quartile outcome, given that 66% of US pest firms have under $500k in receipts [C, C2-S012].

**Why finalist despite a modest base case:**
- It has the cheapest, fastest *paid* validation of the batch.
- Its demand list is official and refreshed daily.
- Capital at risk is small.
- It has a real exit market.

The founder should treat the 90-day field test as a go/no-go.

**Limitations:**
- Chicago commercial prices, the CT exam fee after 2017 and licence processing time are MISSING.
- Veseris terms are behind login.
- Win rates, lead volume and residential CAC are E.
- The live-pest classification is a keyword count of inspector free text.
