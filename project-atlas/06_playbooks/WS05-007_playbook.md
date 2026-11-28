# WS05-007 Playbook: Chicago food-facility pest control (south-west side), with a residential plan line

**Stage E · finalist playbook · 2026-11-28.** Evidence tags are [level, source_id]. Sources with an `E-WS05007-` prefix are new in this stage (`06_playbooks/sources_E_WS05-007.jsonl`); the rest are in `09_databases/sources.jsonl`. Model figures come from the rebuilt `08_financial_models/WS05-007_results.json` and are rounded to the dollar. All outreach texts are drafts in `06_playbooks/WS05-007_materials.md`. Nothing has been sent, filed or bought.

> **Verdict: CONDITIONAL GO, for validation only.** This is not yet a launch decision. Spend about $100 now on a price-and-switching interview sprint. Spend about $2k more only if it passes. Commit only after a paid field test produces at least 6 accounts from 60 conversations.
>
> **The business case:**
> - **Demand is official, refreshed daily and local [A].** In 12 months, 942 Chicago food licences had pest activity recorded by inspectors, 165 of them in the target south-west cluster.
> - **The licence is obtainable by the founder:** a $75 exam, a $250 business licence and statutory minimum insurance [A].
> - **Capital at risk is small.** The base case needs **$23,559** with no owner draw, or **$47,268** with the standard $4,000/month draw from month 13.
>
> **The economics are modest** (operating profit before owner pay):
>
> | Case | Year 3 | Year 5 |
> |---|---|---|
> | Base | **$61,514** | **$101,452** |
> | Conservative | **−$9,916** | **$11,882** |
> | Optimistic | **$187,902** | **$398,541** |
>
> In the base case this is a well-paid owner-operator job through year 5, with one technician and no office staff. It becomes a self-running cash asset only if the founder's close rate comes in at the optimistic end.
>
> **What this stage changed:**
> 1. The urgent "fix it before the re-inspection" pitch is mostly too late. The city re-inspects about 7 days after a failed pest inspection, and 80% of those re-inspections pass [A].
> 2. The legal minimum service is **twice a year** with a logbook [A], so buyers who only want compliance are cheap.
> 3. The win rate was cut and the licensing timeline re-dated. Base year-5 profit falls from $142,989 to $101,452.

---

## 0. Corrections to earlier stages (explicit)

| # | Earlier claim | Correction (Stage E) | Evidence |
|---|---|---|---|
| 1 | Stage D: 1,416 food licences with live pests citywide, 256 in the south-west cluster | **942 citywide, 165 in the cluster (12 months).** Stage D counted any comment with "rodent", e.g. "make door rodent proof", which is a gap, not pests. The pool is about one-third smaller | [A, E-WS05007-S001] |
| 2 | Stage D: "the re-inspection deadline is the urgency" | Next inspection comes a **median 7 days** after a failed pest inspection (93% within 14); **79.5% pass**, only 8.5% still show pests. Records post 2–5 days late, so a newcomer usually arrives after the incumbent fixed it. **Base win rate cut 0.30 → 0.25** | [A, E-WS05007-S001] |
| 3 | Stage C/D: a pest logbook is required, so most sites have a vendor | Refined: inspectors cite a rule requiring a licensed exterminator "at least twice a year" and a 12-month logbook carrying the company's **IDPH licence number**. Monthly service is a choice, not a legal minimum | [A, E-WS05007-S001] |
| 4 | Stage D: about 2 months to first sale | Exam applications must be **received** 15 days ahead, by mail [A, E-WS05007-S013]. The last 2026 sitting is **12/16/2026** (deadline **12/1/2026**); no 2027 dates are posted [A, E-WS05007-S002]. Base delay is now 3 months; first sales in month 5 | [A] |
| 5 | Technician wage ($46,740) cited as DA-S011 | DA-S011 is the **janitor** table; the correct source is C2-S021. The value was right | [C, C2-S021] |
| 6 | 23 prospect licences "with live pest evidence" | Four had **no pest-activity inspections** in the window: MingHin Cuisine, 88 Marketplace, La Catedral Cafe, Park to Shop (Canal St). CSV annotated; 12 repeat offenders added (42 rows) | [A, E-WS05007-S001] |
| 7 | Business licence "renew by Dec 1" | Renewal is **due** 1 December; the licence **expires** 31 December, even if issued in spring | [A, E-WS05007-S003] |
| 8 | Base year-3 $52k, year-5 $143k, 10-year deployable $375k | Now **$61,514 / $101,452 / $177,267**. Year 3 rose only because the first technician hire slips to month 34, so unpaid founder labour flatters it (Section 7) | Model |

---

## 1. Business explanation (plain language)

**What it does.** The company is a licensed exterminator for Chicago food businesses: restaurants, bakeries, independent grocers, small food plants and institutional kitchens. Each month a technician visits the site and does five things:
- checks and re-baits rodent stations;
- reads glue-board monitors;
- treats roach and fly activity with gels and dusts;
- seals the gaps pests use to get in (door sweeps, sealant);
- writes a service report into the site's **pest-control logbook**.

The same licence, technician and van also serve a smaller line: quarterly mouse-and-insect plans for homeowners and 2–6-flat landlords in the same neighbourhoods.

**Who buys and why they pay.** Chicago health inspectors check every food licence. They cite a food business for pests, missing door sweeps or a missing logbook. The rule they enforce requires a contract with a licensed exterminator and a 12-month logbook containing the exterminator's IDPH licence number [A, E-WS05007-S001]. A citation means a failed inspection, a re-inspection within about a week, and a public record. The owner or manager therefore pays for three things:
1. **Staying off that list**, through prevention.
2. **Paperwork that satisfies the inspector**, and the auditor for wholesale plants.
3. **Fast response** when something goes wrong.

**How it earns.**
- **Recurring fees.** A monthly fee per site of about $100–150 for a restaurant [D, C2-S020], more for grocers and plants.
- **One-time work.** A first cleanout and exclusion job ($150–300), plus add-on jobs.
- **Annual escalators** on contracts, which are common [C, DA-S019].

Costs are mostly the technician's time and the van. Bait, monitors and sealant are about 10–12% of revenue (E). Profit comes from route density, meaning many stops close together, and from retention.

**Why it is attractive:**
- **Demand is legally anchored and recurring.**
- **The licence is reachable.** One certified technician (CT) is needed per location. The founder can become that person with a $75 exam that has no experience requirement [A, WS05-S013, E-WS05007-S013]. Uncertified technicians may work under supervision [A, C2-S002].
- **Small books sell.** Consolidators buy recurring books continuously. Rollins did 26 deals in 2025 [A, C2-S008]. Rentokil paid about $37m for businesses with about $26m of prior-year revenue in H1 2026 [B, E-WS05007-S006].

**Why it is hard:** almost every buyer already has a vendor; incumbents fix most crises within a week; the legal minimum is twice a year; and the idea is fully copyable (Rollins calls the market fragmented with "low barriers to entry" [A, C2-S008]). The business is won or lost on the founder's **displacement close rate** and technician quality.

---

## 2. Commercial entry

### 2.1 Niche and geography
**Niche:** monthly integrated pest management (IPM) for independent food establishments, with "inspector-ready" digital logbooks.

**Area:** five contiguous south-west ZIP codes: 60608 (Pilsen/Lower West Side), 60609 (Back of the Yards/Bridgeport south), 60616 (Chinatown/Near South), 60623 (Little Village/North Lawndale) and 60632 (Brighton Park/Archer Heights).

**Stage E re-test of the cluster choice** (12 months to 2026-11-25, stricter pest-activity classification [A, E-WS05007-S001]):

| Cluster (5 ZIPs) | Licences inspected | Violation-38 licences | With pest activity | Share | ≥2 pest inspections | Licence-type inspections |
|---|---|---|---|---|---|---|
| **South-west** 60608/09/16/23/32 | 1,492 | 428 | **165** | 11.1% | 22 | 270 |
| North-west 60647/39/18/41/22 | 1,319 | 260 | 119 | 9.0% | 26 | 332 |
| Far north 60625/40/59/45/26 | 765 | 127 | 89 | 11.6% | 12 | 153 |
| Near north 60611/10/54/14/57 | 1,470 | 195 | 99 | 6.7% | 19 | 293 |
| Far south 60628/17/19/20/43 | 924 | 223 | 80 | 8.7% | 6 | 187 |

**The south-west cluster stays first.** It has the largest pest pool and the most violation-38 citations. It also contains the Stockyards wholesale corridor (214 wholesale food licences [A, DA-S029]) and two pest-supply points: Veseris on Kedzie [B, DA-S014] and Pest Management Supply, Inc. on Wabash [A, E-WS05007-S005].
- **Within the cluster**, 60632 (43 licences with pest activity), 60623 (41) and 60616 (39) are the densest. 60608 (27) and 60609 (15) are thinner than Stage D implied.
- **Second-route candidates:** north-west (by volume) or far north (by rate).
- **Residential pressure is visible.** The cluster's ZIPs logged 4,377 City "rodent baiting/rat complaint" 311 requests in 12 months, and adjacent 60629/60638 another 2,741 [A, E-WS05007-S014].

**Founder-fit flag.** The cluster is predominantly Spanish-speaking (Little Village, Pilsen, Back of the Yards) and Chinese-speaking (Chinatown). If the founder speaks neither language, expect lower close rates. That is a reason to test the north-west cluster in parallel during the interview sprint (Section 4).

### 2.2 Target customer and trigger flow
**Decision-makers:**
- Owners and general managers of independent restaurants and bakeries (decide in days).
- Store managers or owners of independent grocers.
- QA or plant managers of wholesale food plants (1–3 months, audit-driven).
- Administrators of supportive-living kitchens.

**Monthly flow of trigger sites in the south-west cluster** [A, E-WS05007-S001, S004]:

| Trigger | Sites per month | Notes |
|---|---|---|
| Licences cited with pest activity | ~14 | About 13% become repeat offenders within the year |
| Other violation-38 citations (gaps, door sweeps, missing logbook) | ~22 | An exclusion-job opener |
| Newly issued retail food licences | ~10 | 116 a year; includes ownership changes |
| **Total** | **~46** | |

The model's 45 qualified conversations a month (E) assume about 60% of the ~46 trigger sites reach a decision-maker (~28). The rest come from about 10 residential inbound enquiries and about 7 cold walk-ins or referrals.

**Seasonality.** The pest-activity share of inspections bottoms in December (4.8%) and peaks in September (8.8%) [A, E-WS05007-S001]. A spring 2027 start catches the seasonal rise.

### 2.3 Named suppliers and partners (full detail in `09_databases/suppliers/WS05-007_suppliers.csv`)

| Organisation | Role | What is known | Level |
|---|---|---|---|
| **Veseris**, 3642 S Kedzie Ave, 60632 | Pest products and equipment distributor | Account form requires a pesticide applicator licence number and attestation; online credit application; prices and terms behind login | B, DA-S014 |
| **Pest Management Supply, Inc.**, 2027–29 S Wabash Ave, 60616 | Wholesale pest supplies | Holds a City Limited Business License for wholesale sales; terms MISSING | A, E-WS05007-S005 |
| Target Specialty Products (Chicago / Des Plaines) | Second distributor | Chicago-area presence per search summary only | D, E-WS05007-S017 |
| Bell Laboratories (stations, baits) | Manufacturer, sold through distributors | MISSING | E |
| GorillaDesk | Routing, invoicing, service reports | Basic $49/mo, Pro $99/mo, plus $50 per added route | B, DA-S016 |
| Insureon marketplace, or an independent agent | GL, auto, pollution, workers' comp | Pest-firm averages: GL $112/mo, auto $114, workers' comp $90, professional $58 | C, DA-S010 |
| IDPH Structural Pest Control Program (regulator) | CT exam, business licence | $75 exam; $250/location/yr; certificate of insurance form | A, WS05-S012/S013 |
| Brooks Equipment (Elk Grove Village), **phase 2 only** | Extinguisher wholesale | Net 30 if credit-approved | B, DA-S017 |

### 2.4 Top 15 named prospects (all "prospect — not contacted"; 42 rows in `09_databases/prospects/WS05-007_prospects.csv`)
Counts are inspections with pest activity in the 12 months to 2026-11-25 [A, E-WS05007-S001] unless noted.

| # | Prospect (licensed premises) | Why it ranks |
|---|---|---|
| 1 | Tacos y Tamales El Pollo, 4014 W 26th St | 4 of 9 inspections with pests; 7 violation-38 citations; anchors a 26th St route |
| 2 | Taquizas Don Rafa 2, 3857 W 26th St | 4 pest inspections, latest 2026-10-14; same corridor |
| 3 | New Grand Chinese Kitchen, 5401 S Wentworth Ave | 4 pest inspections of 9 |
| 4 | Del Refugio Bakery, 5005 S Ashland Ave | 4 pest inspections; **Amazcakes** across the street (2) makes a two-account block |
| 5 | La Torta Chilanga #2, 5407 S Kedzie Ave | 3 pest inspections, latest 2026-10-06 |
| 6 | Pete's Fresh Market (4343 S Pulaski; 2526 W Cermak) | 2 each; one chain decision covers several stores |
| 7 | Park to Shop Supermarket, 2425 S Wallace St | 2 of 4; two-store owner |
| 8 | Dongpo Impression, 228 W Cermak Rd | 2; Chinatown density with Yummy Yummy Noodles and Mayflower Seafood (2 each) |
| 9 | M K Poultry, Inc., 2600 W 51st St | 2, latest 2026-11-12 (most recent repeat) |
| 10 | La Casa del Pueblo, 1834 S Blue Island Ave | 2, latest 2026-10-21 |
| 11 | Birrieria La Tapatia, 2861 W Cermak Rd | 2, latest 2026-09-08 |
| 12 | Shiki Buffet, 4717 S Kedzie Ave | 4 violation-38 citations, 1 with pests (2026-11-04); high-volume, twice-monthly service |
| 13 | The Montclare Supportive Living, 4339 W 18th Pl | Institutional kitchen plus resident units; facility-wide ticket |
| 14 | Winfar Foods, Inc., 3800 W 45th St | Wholesale site with a pest citation; $300–600/mo audit programme |
| 15 | El Milagro (2919 S Western; 3120 W 36th; 1927 S Blue Island) | Multi-plant tortilla maker; long displacement cycle, high ticket (no citation found) |

Excluded: national chains, Chicago Public Schools sites (bought centrally), and anything procured through public bids. City IPM work flows through incumbent joint-purchasing contracts. One example: City Colleges' $1.2M award (2026–29) to ABC Humane/Landmark Pest Management under City contract #280182 [A, E-WS05007-S008].

### 2.5 Named competitors

| Competitor | Profile | Evidence |
|---|---|---|
| Orkin (Rollins) | Commercial revenue $1.245B, gross margin 52.8% | A, C2-S008 |
| Rentokil-Terminix | North America retention 80.7%; Commercial and National Accounts retention "needs more focus"; opening small local branches | B, C2-S009; E-WS05007-S006 |
| Ecolab Pest Elimination | Food-segment specialist | A, C2-S011 |
| Rose Pest Solutions; Smithereen (Niles) | Regional players. Smithereen bid $2,715/mo against a $780/mo winner for Springfield schools | D, E-WS05007-S015 |
| ABC Humane / Landmark Pest Management | City airports $4.374M; City Colleges $1.2M; WBE-certified | A, C2-S016; E-WS05007-S008 |
| R.B. Pest Solutions | Cook County facilities | A, DA-S024 |
| Small firms with a Chicago business licence | Samuel Pest Control (4100 S Ashland, *inside the cluster*); Verminator Pest Eliminator (3143 W 71st, adjacent); A-1 Pest Master (1943 W 63rd); D'Raco's (400 W 76th); Logan Square Pest Control; Superior Pest Solutions; US Exterminators; Safe Place; Effective Pest Solutions (home-based) | A, E-WS05007-S005 |
| Firms bidding public work | D-Bug Enders, Next Step, Chicago Pests LLC | A, C2-S018 |

Inspectors rarely name the provider. "Orkin" appears in 15 violation-38 comments over 24 months, so incumbent share cannot be measured from the data.

### 2.6 Positioning
**"Keep you off the inspection list, with the paperwork to prove it."**

Three commitments:
1. A logbook kept to the CDPH standard, holding every service report with the IDPH licence number (physical binder plus digital copy).
2. Service within 24 hours of a sighting or any citation.
3. Exclusion included in the first-month cleanout.

The documented proof point is the client's own public inspection record. The quality loop in Section 5 tracks it.

**Do not lead on price.** Public bids show 3.5× to 12× spreads [A, C2-S018; D, E-WS05007-S015], and incumbents can go lower. Never imply any connection with the City or CDPH.

### 2.7 Pricing (proposed list; validation tests it)

| Offer | Price | Basis |
|---|---|---|
| Restaurant monthly IPM | **$125/mo** (12-month agreement, 30-day cancellation, 3% annual escalator) | D, C2-S020 / C2-S019; escalator C, DA-S019 |
| High-volume kitchen (buffet, banquet), twice monthly | $200–250/mo | E |
| Grocer or bakery | $175–250/mo | E |
| Wholesale plant, audit programme (twice monthly plus trend reports) | $400–600/mo | E; nearest public anchor is the Waubonsee low bid of about $535/mo [A, C2-S018] |
| Initial cleanout plus exclusion | $150–300 | E |
| "Compliance-minimum" semi-annual plan | **$95 per visit minimum**; steer buyers to monthly | E; see transaction 4 |
| Landlord or homeowner quarterly plan | $150 initial plus $150 per quarter | D, DA-S021 |

The model blends this to **$105/month per account**: 75% commercial at about $125 and 25% residential at about $45/month equivalent. Nationally, published commercial plans span $35 to $2,000+ a month, and a trade-press average acquisition cost of $63 per customer (2023) sits below the model's blended $120 [D, E-WS05007-S011].

A sensitivity run shows the residential line dilutes results. A commercial-only book (blended price $125, acquisition cost $40) gives base year-3 profit of $88,104 and year-5 of $148,000, if the same number of accounts could be won commercially (E). **Keep residential only if experiment 6 shows a cost per won plan of $150 or less, and only as winter-season filler.**

### 2.8 Sales and acquisition strategy
1. **Daily triage from the public feed.** A free Python query against the Socrata API (specification in the materials, Section J) ranks new records:
   - repeat offenders (2 or more pest inspections);
   - failed re-inspections (13% of re-inspections fail);
   - new or changed licences;
   - other violation-38 records.
2. **Walk in 7–21 days after the citation**, after the re-inspection, with a factual opener: the public record shows a pest citation; offer a free inspection, a written IPM plan and a logbook audit. Repeat offenders hear "your current programme isn't preventing citations"; others, "be ready before the next canvass".
3. **Density first:** after each signed account, canvass the same block or corridor (26th St, Cermak, Archer, Wentworth, Ashland, Kedzie).
4. **Referrals:** two names from every signed owner; Chinatown and Little Village owner networks are dense.
5. **Wholesale plants:** letter and visit to QA managers from the licence register, with food-safety consultants as referrers; 1–3-month cycles.
6. **Residential.** Google Business Profile plus a capped Local Services Ads test. Pest LSA leads cost $22–65 (median $38) across 600 accounts [D, E-WS05007-S010]. Booked-job costs run higher, and agency estimates for Midwest leads across all channels are $140–220 [D, E-WS05007-S010].
7. **No paid commercial lead buying.** No telemarketing lists or automated calling (TCPA risk). All contact is in person, by mail, or by email to a published business address.

---

## 3. Transaction economics (year 1, line by line)

Labour is costed at $28/h loaded: the Chicago median of $46,740 [C, C2-S021] × about 1.25 load (E). The same figures sit in the model's UnitEconomics sheet.

| # | Transaction | Revenue | Direct costs | Contribution | Cash timing |
|---|---|---|---|---|---|
| 1 | Independent restaurant after a pest citation: $200 cleanout/exclusion + 12 × $125 | $1,700 | Materials/devices $210; technician (12 × 0.75 h + 2 callbacks × 1 h) $310; vehicle $110; card fees and bad debt 3% $51 | **$1,019 (60%)** | Paid at service by card on file, or net-15. Positive from month 1 because the cleanout covers device costs |
| 2 | Wholesale tortilla/meat plant, twice-monthly audit programme at $500/mo | $6,000 | Materials and insect-light-trap bulbs $700; technician 24 × 1.5 h $1,010; audit reporting $300; vehicle $190 | **$3,800 (63%)** | Net-30. About $1,000 of materials and labour before the first payment |
| 3 | 2-flat landlord quarterly plan: $150 initial + 3 × $150 | $600 | Materials $60; technician 5 × 0.75 h $105; vehicle $40; paid lead $150 | **$245 (41%) in year 1**, about $450 in year 2 | Autopay. The lead cost is paid before revenue |
| 4 | **New:** compliance-minimum corner grocery, 2 visits × $95 | $190 | Materials $30; technician 2 × 1 h $56; vehicle $16; fees $6 | **$82 (43%)** | At service |
| 5 | **Phase 2 (OSFM licence needed):** extinguisher and exit-light service added to an existing restaurant client | $289 | Technician 1.2 h $41; tags $6; replacement unit $45; batteries $30; vehicle $12 | **$155 (54%)** | At visit; annual |

**Evidence for prices:**
- Transaction 1 is D (C2-S019/S020).
- Transaction 2 is E (nearest anchor A, C2-S018).
- Transaction 3 is D (DA-S021).
- Transaction 4 is E. The rule floor behind it is A (E-WS05007-S001).
- Transaction 5 is E, taken from the WS05-001 deep dive. Its unit prices sit between Illinois public bids of $3–7 per extinguisher [A, DA-S005] and small-account practice [D, DA-S007].

**Failure risks per transaction:**
- **Restaurants (1):** closures (979 of 10,140 inspected licences were recorded "Out of Business" in 12 months [A, E-WS05007-S001]); callbacks that wipe out the margin; slow payment.
- **Plants (2):** audit non-conformances blamed on the vendor; long sales cycle; insurance certificates demanded at higher limits than the IDPH minimum.
- **Residential (3):** paid-lead inflation and about 40% annual churn, which an agency cites as the industry average [D, E-WS05007-S010].
- **Compliance-minimum (4):** worth almost nothing, and fills route time.

**Repeat potential.**
- Transactions 1–3 renew monthly or quarterly. At 1.8% monthly churn the expected life is about 56 months [B, C2-S009].
- Commercial retention benchmarks are higher: a target above 94% a year, with independents at about 85–88% [D, E-WS05007-S009]. That would add life, but a new entrant's closure-heavy restaurant book is unlikely to match it in year 1.
- Upsells: exclusion jobs (most violation-38 comments are gaps and door sweeps), fly units, bed-bug work for supportive-living sites, and phase-2 extinguisher service.

---

## 4. Validation (ordered by information value per dollar)

**Minimum viable commercial offering:**
- One certified founder-technician with an IDPH business licence and a bound insurance certificate.
- A starter kit in a compliant vehicle.
- A one-page offer, a 12-month agreement, and a digital and paper logbook with service reports carrying the IDPH licence number.

**No sales or advertising before the business licence is issued.** The statute (225 ILCS 235) could not be retrieved, so the rules on pre-licence advertising are unverified. Interviews before licensing are research only: no prices offered and no sign-ups.

| # | Experiment (when) | Cost | Success | Kill / pivot |
|---|---|---|---|---|
| E1 | **Price-and-switching interview sprint.** 30 in-person, research-only interviews at south-west food sites (mix of cited and uncited; 5 in the north-west cluster as a language and fit check). Days 1–21 | ≤$150 (printing, transit) | Median current restaurant price ≥$90/mo; ≥25% switched or seriously considered switching in the past 12 months; ≥10 owners agree to a free post-licence inspection | Median price <$70/mo, **or** <10% ever switched, **or** most are on prepaid multi-year contracts → stop before spending on licence and insurance; re-check the north-west cluster or drop the idea |
| E2 | CT General Standards exam (January 2027 Westchester sitting, if posted) | ~$100 ($75 fee + photo + travel); free IDPH manual and practice exam | Pass first or second sitting | Two failures |
| E3 | Supplier and insurance qualification by founder calls; quotes are free (days 7–45) | $0 | Insurer will file the IDPH certificate, all-in premium ≤$450/mo; a distributor opens an account on the new licence | Premium >$800/mo or no carrier → re-price the model; no distributor → Target Specialty / Pest Management Supply |
| E4 | **Paid field test.** Licence ($250) + insurance first instalment + starter kit; canvass 60+ qualified conversations at cited and new licences over 4–6 weeks (about months 4–5) | ~$1,600–2,000 | **≥6 signed paid accounts at ≥$100/mo, at least 1 at ≥$175** (≥10% conversion = base model) | **<3 accounts** (<5%) → abandon; 3–5 → one more 4-week cycle, then decide |
| E5 | Wholesale-plant test: 10 QA conversations from the licence register | ~$100 | ≥1 paid programme at ≥$300/mo, or ≥2 proposal requests | 0 proposal requests → drop the plant segment |
| E6 | Residential: $300 of Google Business Profile / LSA spend over 4 weeks | $300 | Cost per won plan ≤$150 | >$300 per plan → drop the residential line |
| E7 | Retention and re-inspection check at month 4 of selling (public data) | $0 | ≤1 of the first 10 cancels; no client re-cited for pests | ≥3 cancellations or ≥2 re-citations → technical quality problem; stop growth |

**Budget:**
- E1 + E2 + E3: about $250.
- E4: about $1.6–2.0k.
- E5 + E6: $400.
- **Total about $2.3–2.7k.** E4 revenue offsets part of it.

**Testable assumptions and their model drivers:**
- Conversation-to-win 10%: `lead_to_proposal_pct` 0.40 × `proposal_to_win_pct` 0.25.
- 45 conversations per month.
- Blended price $105, commercial about $125.
- One-time revenue $200 per new account.
- Materials at 12% of recurring revenue (gross margin 0.88).
- Monthly churn 1.8%.
- Blended acquisition cost $120.
- Insurance $320/mo.

E4 measures the first three directly.

**Conditions to invest more**, moving to the $5–25k rungs:
- E4 passes.
- 90 days after E4, at least 15 paying accounts with average recurring revenue of at least $110/mo.
- Callbacks below 20% of visits.
- E7 passes.

**Conditions to abandon or pivot:**
- E1 or E4 kill criteria are hit.
- Insurance cost cannot be covered.
- Two exam failures.
- Pivot options, in order:
  1. Commercial-only in the north-west or far-north cluster, if E1 showed better fit there.
  2. A narrow wholesale-plant specialist, if E5 produced business and restaurants did not.
  3. Stop. The extinguisher route alone is weaker: base year-3 profit $34,321 in the WS05-001 model.

---

## 5. Operations

### 5.1 Lead-to-cash workflow and labour classification

| Step | What happens | Classification |
|---|---|---|
| 1. Data pull | Daily SoQL query on the inspections dataset (`4ijn-s7e5`) and the licence datasets; rank by pest activity, repeat status, ZIP, facility type | **Automatable** (script; no AI needed) |
| 2. Walk list and leave-behinds | Route-ordered list; bilingual one-pager referencing the public record | **AI-assisted** drafting; founder reviews |
| 3. Walk-in and free inspection | Talk to the owner, inspect, photograph, write a proposal on a tablet | **Human** (founder) |
| 4. Agreement and payment set-up | E-signature; card on file or autopay; certificate of insurance on request | **Automatable** (software) |
| 5. Initial service | Cleanout, stations, door sweeps, sealant; logbook created | **Human**, by the licensed CT or a supervised technician |
| 6. Monthly route | Routed visits; service report with EPA registration numbers and amounts; logbook updated | **Human** service; **automatable** routing and report e-mail |
| 7. Records | Keep 2 years of pesticide application records; CT reviews uncertified technicians' records [A, E-WS05007-S012] | **Professional-dependent** (CT sign-off) |
| 8. Billing and collections | Autopay or net-15; weekly receivables review | **Automatable** plus **human** follow-up |
| 9. Quality loop | Weekly re-check of the public feed for clients' inspections; any citation triggers a free extra service within 24 h | **Automatable** detection; **human** response |
| 10. Exceptions | Pesticide incident, customer complaint, failed audit, misapplication | **Not automatable**; CT and insurer |

### 5.2 Fulfilment, support, quality assurance and exceptions
- **Service standard:** agreed monthly visit window; 24-hour response to sightings; a written report every visit.
- **Callbacks:** free revisit within 48 h; target under 10% of visits, alarm at 20%.
- **Quality assurance:** monthly self-audit of three logbooks against CDPH expectations; photographed station maps; weekly check of client inspections (step 9).
- **Exceptions:** pesticide exposures go to the poison centre and insurer (830.870, not read); label instructions prevail; no termite work or warranties at first (Rentokil carries $392M of termite provisions [B, C2-S009]).

### 5.3 Equipment, storage and vehicle (legal minimums)
- **Storage [A, E-WS05007-S012].** A dedicated, locked, signed, ventilated-to-outside, lit area. It needs a fire extinguisher, nearby washing facilities, absorbent, emergency information and a label file.
  - Whether a Chicago home or garage qualifies is unverified. Home occupations face emission limits [D, E-WS05007-S016].
  - One Chicago competitor holds a "Storage or Use of Hazardous Materials" regulated licence [A, E-WS05007-S005].
  - The model carries $300/mo for a small storage space from month 3 (E).
- **Vehicle [A, E-WS05007-S012].** Locked when unattended, with container restraints, absorbent, PPE, a first-aid kit with poison information, labels for every product carried, and a full change of clothing. A used cargo van or an SUV with a lockable cargo box (E) meets this; the model uses $850/mo from month 4.

### 5.4 Software stack (prices)

| Item | Price | Evidence |
|---|---|---|
| GorillaDesk | Basic $49/mo for the first route; Pro $99/mo plus $50 per added route | B, DA-S016 |
| Model line for software | $150/mo, growing 5% a year | E |
| Bookkeeping, phone, website | $300/mo | E |
| AI assistant | $40/mo | E |
| Socrata API | Free; no key needed | A |
| E-signature and card processing | Assumed inside the field app or processor fees (3% in variable costs) | E |

**Requires confirmation:** that GorillaDesk's reports can carry the IDPH licence number and serve as the logbook copy.

### 5.5 Legal requirements (founder checklist)

| Requirement | Detail | Evidence |
|---|---|---|
| IDPH Certified Technician | General Standards exam, 70% to pass; renew every 3 years with 9 classroom hours | A, WS05-S011; C2-S007 |
| IDPH Commercial Structural Pest Control Business License | $250 per location per year; employ ≥1 CT; certificate of insurance filed by the insurer; due 1 December, expires 31 December | A, WS05-S012; E-WS05007-S003 |
| Insurance minimums | $100k/$300k bodily injury and $50k property damage, or $350k combined single limit. Commercial clients will ask for $1M/$2M (E) | A, C2-S004 |
| One location per CT | A CT cannot be the sole CT for more than one location | A, C2-S003 |
| Supervision of uncertified technicians | Supervised on-the-job training, then remote supervision within 1 hour | A, C2-S002 |
| Records, storage, vehicles, display | See Section 5.3 | A, E-WS05007-S012 |
| Penalty | $1,000 initial fine for operating unlicensed | A, C2-S006 |
| City of Chicago licence | Unverified. The City says activities not covered by a state licence need a City licence; a home-occupation licence is $250 for 2 years | D, E-WS05007-S016 |
| Home Repair and Remodeling Act | Written contracts for residential exclusion jobs over $1,000 (as enacted) | A, WS18-S010 |
| Employer rules (from first hire) | Chicago minimum wage $17.05 (July 2026); workers' comp; Chicago Paid Leave | B, DA-S013 |

### 5.6 Financial administration
Separate LLC bank account; monthly close (profit by account and route, receivables ageing); quarterly estimated taxes (model: 30%); IDPH renewal calendar (1 December); a card on file for every restaurant.

### 5.7 After December 2026 (end of heavy AI access)
**Nothing in the operation depends on AI.** The prospect pull is a plain script, reports and routing live in the field app, and translations and proposals need an ordinary $20–40/month subscription. At 3× AI and software cost, base year-3 profit is $60,495 against $61,514. Claude should finish the Section 10.1 tasks before 5 December.

---

## 6. Growth

### 6.1 First 10 customers
- Come from the repeat-offender and recent-citation walk lists in the 26th St, Cermak/Archer and Wentworth corridors (Section 2.4), plus two referral asks per signed account.
- The model expects 10 accounts by about month 7–8, roughly 2.5 months after selling starts.
- The field test (E4) asks for 6 within 4–6 weeks.

### 6.2 First 100 customers
- **Base model:** 50 accounts at month 18 and 100 at month 30. **Optimistic:** months 11 and 16.
- Sources: in-cluster triggers (~46 sites a month), block canvassing around clients, plant QA conversations, landlord referrals, and a residential trickle.
- Watch three numbers: conversion per conversation (≥10%), average recurring revenue (≥$110), and monthly churn (≤1.8%).

### 6.3 Hiring sequence (from the model's staff triggers)

| Hire | Trigger | Cost | Productivity | Base timing | Optimistic timing |
|---|---|---|---|---|---|
| Pest technician (uncertified, supervised; includes van) | 110 active accounts | $5,700/mo | ~190 blended accounts | **Month 34** | Month 18 |
| Office / dispatch coordinator | Monthly revenue ≥$30k | $4,200/mo | Up to 2 people | Never within 5 years | Month 29 |
| Commercial sales rep, commission-heavy | 300 accounts | $5,500/mo | 4 new accounts/mo after 3 months | Never within 5 years | Month 40 |
| Service manager / second CT | 650 accounts, or a second location | $6,800/mo | — | Never | Not within 5 years |

**Why the sequence matters.** In the base case **the founder is CT, salesperson and office for five years.** A rep hired before 300 accounts destroys profit. In Stage D, a salaried rep hired at month 20 cut base year-3 profit to about $4k. The "hires 30% sooner" stress takes base year-3 profit to $7,090.

### 6.4 Capacity limits
Founder: about 110 serviced accounts while selling 12–15 h a week (about 50 h a week, E). Technician: about 190 blended accounts, or 8–12 commercial stops a day (E). One licensed location per CT [A, C2-S003], but one location can serve all of Chicago (the licence is per location, not territory). Drive time is the hidden limit, hence five ZIPs until about 150 accounts.

### 6.5 Geographic expansion
1. Fill the south-west cluster (60632, 60623 and 60616 first).
2. Extend residential to adjacent 60629/60638, which have high rodent-complaint volume [A, E-WS05007-S014].
3. Open a second route in the north-west cluster (119 pest-activity licences; 26 repeat offenders) or the far north (89 at 11.6%) from the same licensed location.
4. A second licensed location needs a second CT and is justified only above about 600 accounts.

### 6.6 Adjacent services

| Adjacency | Economics | When |
|---|---|---|
| Exclusion and door-sweep jobs | Gap comments dominate violation-38 citations [A, E-WS05007-S001] | From day 1, as add-on revenue |
| Fly-control units and insect-light-trap programmes for kitchens and plants | E | Year 1–2 |
| Bed-bug programmes for supportive-living facilities | Heat-treatment bids $800–1,250 per application in Rockford [A, C2-S017] | Year 2+ |
| **OSFM Class A fire-extinguisher licence** (second service) | Licence about $1,520: NAFED exam $320, distributor licence $900 for 3 years, employee licence $300 [A, WS05-S001/S002; B, WS05-S025]. Needs **$1M liability insurance** [A, DA-S003] | **Trigger: about 150 commercial accounts** (base month 45; optimistic month 22) |
| Kitchen-hood suppression inspections (OSFM Class B) | Public Illinois prices $185–240 per inspection (Fox Valley) and $250–500 (JCI), semi-annual [A, DA-S005]. Class B is $1,500 [A, WS05-S001] plus manufacturer training, which is gated: Amerex wants "proven experience" [B, DA-S018] | Year 3+, only if a manufacturer will train |

**How the extinguisher line works.** Tag, inspect and replace units; subcontract recharges and hydrotests at first, so no shop is needed [WS05-001 deep dive]. At about $155 a year of contribution per shared account and 40% uptake across 150 commercial accounts, it adds about **$9k a year** (E), before $1–3k a year of extra insurance and licence cost. It is a retention add-on, not a growth engine (standalone WS05-001 base year 3: $34,321). The OSFM Act's 1 January 2028 repeal date is unresolved; the 2022 review recommended continuation [A, DA-S002] and no 2026 extension bill was found. Decide at 150 accounts.

### 6.7 Vertical integration (incremental return logic)
- **Own storage and warehouse:** no. Storage is a compliance cost, not a margin source.
- **Direct manufacturer buying:** only at a scale where materials exceed about $50k a year. Materials are about 12% of revenue, so a 15% discount on about $33k (base year 5) saves about $5k: low return.
- **Training your own CTs** (sponsor a technician's exam, $75): very high return. It is the gate to a second location and to a manager.
- **Buying small books later** (a capital-allocation tool after organic proof, not the entry route):
  - Consolidators pay about 1.4× prior-year revenue [B, E-WS05007-S006].
  - A $60k book bought at 1.2× revenue ($72k) with 30% route contribution earns about $18k a year, about 25% pre-tax, plus density savings.
  - That beats organic growth only once the founder no longer sells (organic return about 50%, E; Section 7).

### 6.8 Management delegation
- A manager who is also a CT (about $6,800/mo, E) can run the business day to day.
- That makes sense only when operating profit before owner pay exceeds about $150k, so the business still pays the owner after the manager.
- **Base:** not reached within 10 years (year-10 profit $135,287).
- **Optimistic:** about year 3–4 (year-3 $187,902).
- In the base case the founder remains the operator. That is the core reason this is a "B-grade" holding-company first asset (Section 9).

### 6.9 Reinvestment slots, in priority order
1. Route density in-cluster: canvass time and leave-behinds.
2. A technician once 110 accounts are reached.
3. A sponsored second CT.
4. The second route cluster.
5. OSFM Class A at 150 commercial accounts.
6. Book acquisitions from retiring owners.

The model's long-term assumption is a 50% incremental pre-tax return in base, 30% conservative and 80% optimistic. That is derived from about $1,500 of rep-led acquisition cost per account against about $56/month of contribution after technician time over about 56 months (E).

---

## 7. Financial analysis (rebuilt model)

**Standardization.**
- Owner draw is $4,000/month from month 13, in all scenarios.
- Tax is 30%.
- The start capital injection is **$47,300** in all scenarios. That is the smallest amount, rounded up to $100, that keeps the base cash balance at or above zero; the minimum base cash balance is $32, in month 24.

Operating profit is on an EBITDA basis and **before owner pay**. In the base case it includes the value of the founder's own technician work until month 34.

### 7.1 Launch capital and working capital
- **Launch spend in base:**
  - $5,500 of equipment and starter stock in month 3, after the exam.
  - Pre-revenue overhead of $690/month in months 1–2, $1,340 in month 3 (insurance, storage and licence start) and $2,340 in month 4 (vehicle and software start).
- **Year 1 (base):** revenue $17,644; operating profit −$15,506; free cash flow −$23,493.
- **Working capital is small** (unchanged from Stage D: receivables 20 days, inventory 20 days, payables 25 days):
  - about $679 at 10 accounts;
  - about $3,395 at 50;
  - about $13,580 at 200.
- The stress "customers pay 30 days later" raises peak funding only to $61,360.

### 7.2 Base case, months 1–24

| Month | New accounts | Active accounts | Revenue | Operating profit | Owner draw | Cash balance |
|---|---|---|---|---|---|---|
| 1 | 0.0 | 0.0 | $0 | −$690 | $0 | $46,610 |
| 2 | 0.0 | 0.0 | $0 | −$690 | $0 | $45,920 |
| 3 | 0.0 | 0.0 | $0 | −$1,340 | $0 | $39,080 |
| 4 | 0.0 | 0.0 | $0 | −$2,340 | $0 | $36,740 |
| 5 | 1.1 | 1.1 | $343 | −$2,290 | $0 | $34,244 |
| 6 | 2.3 | 3.4 | $806 | −$2,145 | $0 | $31,816 |
| 7 | 3.4 | 6.7 | $1,387 | −$1,905 | $0 | $29,551 |
| 8 | 4.6 | 11.2 | $2,085 | −$1,571 | $0 | $27,545 |
| 9 | 4.6 | 15.6 | $2,557 | −$1,193 | $0 | $26,048 |
| 10 | 4.7 | 19.9 | $3,026 | −$818 | $0 | $24,928 |
| 11 | 4.7 | 24.3 | $3,490 | −$446 | $0 | $24,182 |
| 12 | 4.7 | 28.6 | $3,951 | −$77 | $0 | $23,807 |
| 13 | 4.8 | 32.9 | $4,540 | $312 | $4,000 | $19,741 |
| 14 | 4.8 | 37.1 | $5,007 | $686 | $4,000 | $16,126 |
| 15 | 4.9 | 41.3 | $5,470 | $1,057 | $4,000 | $12,884 |
| 16 | 4.9 | 45.5 | $5,930 | $1,426 | $4,000 | $10,013 |
| 17 | 5.0 | 49.6 | $6,386 | $1,791 | $4,000 | $7,510 |
| 18 | 5.0 | 53.7 | $6,838 | $2,153 | $4,000 | $5,371 |
| 19 | 5.0 | 57.8 | $7,287 | $2,512 | $4,000 | $3,594 |
| 20 | 5.1 | 61.8 | $7,732 | $2,869 | $4,000 | $2,175 |
| 21 | 5.1 | 65.8 | $8,173 | $3,222 | $4,000 | $1,113 |
| 22 | 5.2 | 69.8 | $8,611 | $3,573 | $4,000 | $403 |
| 23 | 5.2 | 73.7 | $9,046 | $3,921 | $4,000 | $44 |
| 24 | 5.2 | 77.7 | $9,477 | $4,266 | $4,000 | $32 |

New accounts per month include referrals (1 per 100 active). Founder wins at full pace are 4.5 a month in base, 2.02 conservative and 8.91 optimistic.

### 7.3 Five-year annual view (operating profit before owner pay; free cash flow before draw; retained cash after draw)

| Scenario | Year | Revenue | Operating profit | Free cash flow | Retained after $48k draw | Active accounts at year end | Staff |
|---|---|---|---|---|---|---|---|
| Conservative | 1 | $4,479 | −$30,927 | −$39,772 | −$39,772 | 11 | 0 |
| | 2 | $26,007 | −$23,981 | −$25,934 | −$73,934 | 30 | 0 |
| | 3 | $45,756 | **−$9,916** | −$11,580 | −$59,580 | 46 | 0 |
| | 4 | $62,649 | $1,900 | $471 | −$47,529 | 58 | 0 |
| | 5 | $77,228 | **$11,882** | $10,643 | −$37,357 | 68 | 0 |
| Base | 1 | $17,644 | −$15,506 | −$23,493 | −$23,493 | 29 | 0 |
| | 2 | $84,499 | $27,790 | $24,226 | −$23,774 | 78 | 0 |
| | 3 | $150,496 | **$61,514** | $55,568 | $7,568 | 122 | 1 |
| | 4 | $214,371 | $55,076 | $51,738 | $3,738 | 163 | 1 |
| | 5 | $276,325 | **$101,452** | $86,714 | $38,714 | 199 | 1 |
| Optimistic | 1 | $55,431 | $13,140 | $454 | $454 | 67 | 0 |
| | 2 | $228,520 | $103,570 | $77,698 | $29,698 | 174 | 1 |
| | 3 | $410,764 | **$187,902** | $138,833 | $90,833 | 281 | 2 |
| | 4 | $627,408 | $233,214 | $165,214 | $117,214 | 418 | 4 |
| | 5 | $934,994 | **$398,541** | $278,836 | $230,836 | 585 | 5 |

**Why year 4 dips below year 3 in base.** The first technician arrives in month 34 ($5,700/month including van) before the book fills the technician's capacity. This is the hiring valley.

### 7.4 Breakeven, payback and milestones

| Metric | Conservative | Base | Optimistic |
|---|---|---|---|
| First month with operating profit >0 | 41 | **13** | 7 |
| ≥$1k/month operating profit | 55 | 15 | 8 |
| ≥$5k/month | never (60 months) | 26 | 12 |
| ≥$10k/month | never | 60 | 17 |
| ≥$25k/month | never | never | 49 |
| Payback of cumulative deficit | never | month 60 | month 12 |
| **Peak funding** (with draw) | **$258,172** | **$47,268** | $10,574 |
| Peak funding (no draw) | $78,519 | **$23,559** | $10,574 |

In base, monthly cash after the draw first turns positive in month 25.

**Milestone plausibility for a capable entrant:**
- **$1k/month:** likely.
- **$5k/month** (month 26): plausible.
- **$10k/month:** only at the end of year 5 in base.
- **$25k/month:** requires the optimistic close rate, two-plus technicians, an office coordinator and a rep.
- **$1M/year:** not a plausible milestone. Only 2.5% of US pest firms exceed $5M in revenue [C, C2-S012].

### 7.5 Sensitivity (each driver ×0.75 and ×1.25, base)

| Driver | Year-3 profit at ×0.75 | Year-3 profit at ×1.25 | Peak funding at ×0.75 / ×1.25 | 5-year retained cash at ×0.75 / ×1.25 |
|---|---|---|---|---|
| Gross margin 0.88 | $31,477 | $91,551 | $135,500 / $33,814 | −$134,144 / $106,370 |
| Price per account $105 | $33,525 | $89,503 | $124,122 / $35,404 | −$121,022 / $89,682 |
| Overhead | $67,799 | $55,229 | $37,069 / $64,090 | $24,030 / −$18,524 |
| Labour cost | $66,049 | $56,978 | $47,268 / $59,872 | $32,480 / −$28,217 |
| Founder leads 45 / win rate 0.25 (identical effect) | $52,279 | $52,607 | $65,836 / $36,261 | −$50,092 / $62,150 |
| Churn 1.8% | $61,653 | $67,847 | $45,913 / $48,804 | $27,843 / −$14,992 |

Base 5-year retained cash is $2,753.

**How to read it:**
- The gross-margin upper bound of 1.10 is not physically possible. Use the −5 and −10 point stresses below instead.
- Leads and win rate barely move year 3 either way, because more accounts bring the technician hire forward. Peak funding and 5-year retained cash show their real effect.

**The top drivers are price per account, materials margin and close rate.**

### 7.6 Stress tests (base)

| Stress | Year-3 profit | Year-5 profit | Peak funding | 10-year deployable |
|---|---|---|---|---|
| Base | $61,514 | $101,452 | $47,268 | $177,267 |
| Acquisition cost doubles | $49,416 | $88,183 | $82,080 | $128,998 |
| Win rate 40% below plan | $35,853 | $62,279 | $85,066 | $34,034 |
| Sales cycle doubles | $65,470 | $94,327 | $59,961 | $159,843 |
| Gross margin −5 pts | $53,989 | $87,636 | $61,654 | $125,898 |
| Gross margin −10 pts | $46,464 | $73,820 | $82,390 | $65,917 |
| Supplier refuses (3-month delay, −5 pts) | $60,639 | $77,574 | $80,152 | $89,547 |
| 25% of base lost in month 18 | $67,405 | $90,726 | $54,899 | $150,163 |
| Customers pay 30 days later | $61,514 | $101,452 | $61,360 | $170,052 |
| Labour +20% | $57,885 | $86,055 | $56,048 | $118,492 |
| Insurance/overhead +50% | $48,943 | $87,940 | $85,278 | $127,957 |
| AI/software ×3 | $60,495 | $100,372 | $49,216 | $173,086 |
| Hires needed 30% sooner | **$7,090** | $54,181 | $98,290 | $1,330 |
| Recession (new −30%, churn ×1.5) | $36,731 | $81,663 | $80,772 | $121,630 |
| Competitor response | $56,779 | $49,654 | $80,753 | $373 |
| Founder capacity −40% | $35,853 | $62,279 | $85,066 | $34,034 |
| Growth takes twice as long | **$18,147** | $59,509 | $124,178 | $20,785 |

**Survivable:** cash and AI shocks; recession (code-driven demand keeps year-5 profit at $81,663). **Dangerous:** hiring early; slow growth (the only stress pushing peak funding above $100k, to $124,178); competitor price pressure (10-year deployable $373); a conservative-level win rate.

### 7.7 Capital accumulation to year 10 and owner distributions

| | Conservative | Base | Optimistic |
|---|---|---|---|
| Year-10 operating profit | $13,008 | $135,287 | $636,578 |
| Cumulative deployable surplus, year 5 | $0 | $38,307 | $386,222 |
| Cumulative deployable surplus, year 10 | $0 | **$177,267** | $1,640,322 |
| Owner pay, 10 years (standard draw) | $454,484 | $454,484 | $454,484 |
| Indicative enterprise value, year 10 | $31,220 | $405,862 | $2,546,314 |

**Assumptions behind the long-term years (6–10):**
- Growth in year 6 of 3% / 8% / 12%, decaying ×0.75 / 0.85 / 0.90 a year. Rollins' organic growth was 7.6% commercial and 5.0% residential [A, C2-S008].
- Incremental return of 30% / 50% / 80%.
- Maintenance capex of 8% / 5% / 4% of operating profit.
- Cash reserves of 3 / 2 / 2 months.
- An exit multiple of 2.4× / 3.0× / 4.0× pre-owner-pay profit. Sold service businesses fetch 1.75–3.13× owner earnings (interquartile) [D, E-WS05007-S007], and consolidators pay about 1.4× revenue [B, E-WS05007-S006].

**Owner distributions.** The base business funds the $48k/year draw from month 13 only by first consuming the injected $47,300. In the conservative case the draw is not affordable: the $258,172 peak funding is mostly draws financed by capital. **The honest conservative answer is no owner pay for five years.**

### 7.8 Downside cases in plain terms
- **Conservative close rate** (6.3% conversion, $85 price, 2.5% churn): 68 accounts after 5 years, never profitable enough to pay the owner.
- **Base close rate with a competitor price response:** year-5 profit $49,654, with nothing left to deploy.

Both are detectable within about 4 months of selling (E4 and E7). That is why the capital ladder stops at about $2.5k until they pass.

---

## 8. Capital deployment ladder

| Rung | What it buys | Evidence gate before spending | How it could be lost |
|---|---|---|---|
| **$0–500** | E1 interview sprint (≤$150); CT exam application ($75 + photo); free IDPH manual and practice exam; insurance and supplier questions by phone ($0) | None. This is the gate | Time only |
| **$500–2k** | LLC (filing fee about $150, confirm with the Secretary of State); IDPH licence $250; insurance first instalment (about $300–600, E); starter kit (stations, glue boards, gels, dusts, sealant, sweeps, PPE, hand sprayer; about $700–900, E); GorillaDesk Basic $49/mo | E1 passed; CT exam passed; insurer will file the IDPH certificate | Field test fails; insurance is annual or non-refundable |
| **$2–5k** | Remainder of E4/E5/E6 (residential $300); compliant vehicle fit-out (lockbox, restraints, spill kit, first aid); storage area set-up; printed logbooks | **E4 ≥6 paid accounts** from ≥60 conversations | Accounts churn at month 2–4; callbacks consume time |
| **$5–10k** | Full base equipment ($5,500: tablet, sprayers, ILTs, stock); storage lease; 2–3 months of overhead | ≥15 paid accounts, average ≥$110/mo, callbacks <20%, E7 clean | Price war; a pesticide incident (insured) |
| **$10–25k** | Months 5–24 operating losses and working capital; base no-draw peak $23,559 | Run-rate ≥5 new accounts a month and churn ≤2% a month for 2 consecutive quarters | Slow growth: twice as long gives peak funding $124,178 with draw |
| **$25–50k** | The owner draw from month 13 until the book covers it; base peak with draw $47,268 | ≥50 accounts by month 18 (base path) | Draw continues while the book stalls: the conservative path |
| **$50–100k** | Only for a technician hire at 110 accounts plus van ($2,500 capex + $5,700/mo); a sponsored second CT; or OSFM Class A licence plus kit at 150 commercial accounts. Book acquisitions above this, from profits | Technician-ready book (110+ accounts, churn ≤1.8%); 2 quarters of positive operating profit | Hiring early ("30% sooner" → year-3 $7,090) or a book acquisition that churns |

**Rule: never move up a rung on interest alone.** Only signed, paid and retained accounts count.

---

## 9. Strategic wealth creation

**How it becomes a durable cash asset.** The asset is a dense, contracted route of 200–600 food and residential accounts. It has a logbook-and-audit history, a CT bench, and pricing that rises with escalators.
- That asset survives recessions: in the stress, new accounts −30% and churn ×1.5 still leave year-5 profit at $81,663.
- It is saleable to active consolidators: Rollins' 26 deals [A, C2-S008]; Rentokil about 1.4× revenue [B, E-WS05007-S006].

**How much capital it could generate:**

| Case | Deployable after owner pay, 10 years | Indicative enterprise value, year 10 |
|---|---|---|
| Base | $177,267 | $405,862 |
| Optimistic | $1,640,322 | $2,546,314 |
| Conservative | $0 | $31,220 |

**When management could take over.** Only once profit before owner pay exceeds about $150k (Section 6.8): never in the 10-year base case, about year 3–4 in optimistic.

**Can it fund other ventures?** In base, only modestly and late: about $18–37k a year of deployable surplus in years 6–10. In optimistic, yes: $189k–313k a year in years 6–10.

**Is it a strong first company for a diversified portfolio?**

**For:** small, staged capital at risk; a fast, cheap, paid test; code-driven recurring demand; obtainable regulated entry; a real exit market; AI-independent operations; and route, hiring and density skills that transfer to other service roll-ups. **Against:** base economics look like a job for 5+ years; founder-dependent (CT and seller); copyable wedge; two-thirds of US pest firms stay under $500k revenue [C, C2-S012].

**It is a strong first company only if E4 lands at or above the optimistic conversion** (about 15% per conversation, about 9 wins a month at full pace). At base conversion, it is a respectable but slow first asset. Compare it against the other finalists' refreshed models before committing to a 12-month build.

---

## 10. Execution plan

### 10.1 First 7 days (Mon 30 Nov – Sun 6 Dec 2026)

**What the founder does:**
1. **Exam decision (by Mon 30 Nov).** The 12/16 sitting needs the mailed application, $75 check or money order and 2×2 photo **received in Springfield by 1 December** [A, E-WS05007-S013]. That is realistic only with overnight delivery on Monday.
   - Otherwise list 12/16 as first preference anyway; the form says the next available choice is used. Mail it this week for January.
   - IDPH has posted no 2027 dates, so ask IDPH by phone or e-mail for the January date (founder only).
2. Download the General Standards Manual and practice exam (free). Plan 15–20 h of study.
3. Answer the founder facts: age, credit, vehicle, weekly hours, languages, location (UNRESOLVED_QUESTIONS F1–F7).
4. Run **10 of the 30 E1 interviews** with the questionnaire. Research only: no offers.

**What Claude prepares before 5 December** (all drafts): the SoQL data-pull and ranking script specification (materials, Section J); walk lists for the 26th St, Cermak/Archer and Wentworth corridors; the interview questionnaire and tally sheet; Spanish and Chinese leave-behind drafts for native-speaker review; a 100-question practice quiz from the free IDPH manual; insurance and supplier question lists; the KPI sheet.

**Spend this week:** about $100 or less. **Evidence required:** 10 completed interview tallies.

### 10.2 First 30 days (to about 30 Dec 2026)

**What the founder does:**
- Finish E1 (30 interviews, including 5 in the north-west cluster).
- Mail the CT application.
- Collect 2–3 insurance quotes. These are the founder's own requests; Claude does not request quotes.
- Ask the suppliers the account questions.
- Decide on a storage location that meets 830.830.

**Named organisations the founder approaches:**

| Organisation | Questions |
|---|---|
| IDPH Structural Pest Control Program | 2027 exam dates; current exam fee; business-licence processing time; storage disclosure for a rented unit |
| Veseris (3642 S Kedzie Ave) | Account on a new licence; terms; minimums; station and bait prices |
| Pest Management Supply, Inc. (2027 S Wabash Ave) | Same as Veseris |
| Target Specialty Products | Chicago-area branch; terms |
| An independent insurance agent or Insureon | GL $1M/$2M, auto, pollution; IDPH certificate filing; premium; payment plan |
| City of Chicago BACP small business centre | Whether a state-licensed pest firm with a home office needs a City licence |
| Prospects | Interviews only (top-15 list and E1 sample) |

**Evidence required to continue:** E1 pass, meaning a median restaurant price of at least $90 and at least 25% who switched or considered switching.

**Proposed spend:** ≤$250.

**Conditions to abandon at day 30:** E1 kill criteria hit in both clusters.

### 10.3 First 90 days (to about end of February 2027)
1. Sit the January exam.
2. On passing: form the LLC, bind insurance (the insurer files the certificate), and mail the business licence application with $250.
3. Set up storage, fit the vehicle, open supplier accounts (licence number required), and pre-book free inspections with the E1 owners who agreed.

**Conditions to accept a first paid order:**
- The IDPH business licence is issued and the certificate of insurance is on file.
- A written agreement is signed.
- The service report template carries the IDPH licence number.
- The site is in the cluster.
- The price is at or above the floor ($100/mo, or $95 per visit).
- A card on file or net-15 terms are in place.

**Milestone by about day 90:** licensed, insured and equipped, with at least 10 pre-booked inspections.

**Slow branch:** if licence processing pushes past March, keep overhead off; the vehicle and storage start only with the licence.

### 10.4 First year (to about December 2027)

| Period | Model (base) | Gate |
|---|---|---|
| Months 4–6 (Mar–May 2027) | E4/E5/E6 run | **≥6 paid accounts from ≥60 conversations** |
| Month 8 | About 11 active accounts | E7 retention check: ≤1 of the first 10 cancels |
| Month 12 | About 29 active accounts; revenue $3,951/month; operating profit −$77 | ≥25 paying accounts; average ≥$110; churn ≤2%/month |

**Optimistic branch** (≥9 wins a month): plan the technician hire for about 110 accounts (around month 18 in optimistic). Start sponsoring a second CT.

**Slow-growth branch** (3–5 wins a month): stay founder-only and keep the $4k draw off. Add the north-west cluster route, and drop residential if E6 failed.

**Failure branch** (fewer than 15 accounts by month 8, or 3 or more early cancellations): stop at about $5k total spend. The remaining assets are sellable: route, stock, van lease.

---

## 11. Pre-mortem

| Failure | Most likely path | Early warning | Cheap preventive test |
|---|---|---|---|
| **Lost $5k** | Licensed and equipped, but owners stay with their incumbent. The crisis is already fixed by re-inspection, and $60–90 "compliance" pricing undercuts | Conversion <5% after 40 conversations; median quoted price objection <$90 | E1 before any licence spend; walk in after re-inspection with the prevention pitch |
| **Lost $25k** | Accounts are won but lost. Restaurant closures (9.7% a year recorded "Out of Business"), callbacks, re-citations; the draw starts at month 13 regardless | Churn >2.5%/month; callbacks >20%; any client re-cited twice | E7 weekly re-inspection monitoring; no draw until the run-rate covers it |
| **Lost $50k** | Technician or rep hired early ("30% sooner" → year-3 $7,090); the technician quits; a misapplication claim | Staff cost >45% of revenue; technician utilisation <70% | Hire only at 110 accounts; commission-heavy rep pay only at 300; written supervision and records under 830.270/830.820 |
| **Revenue but no profit** | Compliance-minimum buyers at $95 a visit, too many residential paid leads, scattered sites; materials creep above 15% | Contribution per account <$56/month; drive time >35% of the day | Price floor; five-ZIP rule; drop residential if cost per won plan >$150 |
| **Exhausting low-paid job** | Base years 2–4: the founder works about 50 h a week for a $48k draw while the business retains $3–8k a year | Founder hours >55/week for 3 months; profit per founder hour <$25 | Decide at month 18: optimistic conversion trend or exit/sell the book |
| **Cash crunch** | Base cash falls to $32 in month 24 because the draw (from month 13) exceeds profit until month 25 | Cash <$10k before month 20 | Fund the full $47,300 up front or delay the draw; card on file for all restaurants |
| **Can't run without the founder** | The founder is the only CT and the only seller through year 5 in base | No CT candidate by 150 accounts | Sponsor a technician's CT exam ($75) from year 2; write SOPs from month 1 |
| **No deployable surplus** | Base 5-year cumulative deployable $38,307; competitor-response stress gives 10-year $373 | Price escalators refused; churn up | Escalator clause in every agreement; quality loop as a retention proof point |

---

## 12. Required confirmations (must be confirmed directly before relying on them)

**Regulatory:**
1. Current CT exam fee (the form is dated 2017, $75), the 2027 exam dates and seat availability, and whether the 12/16/2026 seats are still open.
2. Business-licence processing time (MISSING).
3. Whether advertising or soliciting before licensure is prohibited (225 ILCS 235 text not retrieved).
4. The current Chicago Food Code / Municipal Code 7-38-020 text on the twice-a-year service rule and logbook contents (seen only in inspector comments).
5. Whether a City of Chicago business licence is needed for a state-licensed pest firm, and whether pesticide storage at a Chicago home or garage is allowed, or needs a hazardous-materials regulated licence.
6. Home Repair Act current thresholds for residential exclusion jobs.
7. The OSFM Act's 1 January 2028 sunset status (phase 2).

**Insurance:**
8. Carriers willing to write a new pest firm and file the IDPH certificate; premiums for GL $1M/$2M, auto, pollution and workers' comp. Model: $320/month in base, $450 conservative.
9. Whether one GL policy also covers OSFM's $1M requirement later.

**Suppliers:**
10. Veseris, Pest Management Supply and Target Specialty: account eligibility for a newly licensed firm, credit terms (base assumes 25 days of payables, conservative cash on delivery), minimums, and price lists for Bell stations, glue boards, gels and insect-light-trap bulbs.
11. GorillaDesk (or an alternative): whether reports can include the IDPH licence number and serve as the CDPH logbook copy.

**Customers:**
12. Real Chicago prices currently paid, contract terms and switching history (E1).
13. Conversion per conversation at cited and uncited sites (E4).
14. Wholesale-plant QA requirements: audit scheme, required service frequency and insurance limits (E5).
15. Residential cost per won plan in the cluster (E6).

**Founder:** age, high-school/GED (required on the CT form), vehicle, languages, weekly hours, location, and the terms of the conditional $100k (UNRESOLVED_QUESTIONS F1–F7).
