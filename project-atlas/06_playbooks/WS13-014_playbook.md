# WS13-014 — Private utility locating & concrete GPR scanning for Chicago-area contractors and facilities — Stage E Playbook

*Absorbs WS10-005 and WS11-023. Researched 2026-11-28. This is a standalone playbook. Evidence tags are [level, source_id], with levels A–E as defined in `00_governance/EVIDENCE_STANDARDS.md`. Sources with E-WS13014-S### IDs are listed in `06_playbooks/sources_E_WS13-014.jsonl`; all other IDs are in `09_databases/sources.jsonl`. Model outputs are quoted from `08_financial_models/WS13-014_results.json`, rebuilt today. Nothing has been sent, bought or registered.*

> ## Verdict: CONDITIONAL GO, for validation only
> **Do not buy equipment or hire anyone until the gates below pass.**
>
> **Why it is worth validating.** The founder can learn the trade, deliver the work, sell it and later delegate it. No licence was identified for it. The buyers are named repeat B2B accounts: the electrical, plumbing and interior contractors on Chicago's large permits [A, DF-S030]. The price anchors are solid:
> - federal ceiling rates of $124.69–135.26 per hour for utility field technicians [B, DF-S029; B, E-WS13014-S014];
> - a GPRS federal award median of $5,800 per project [A, DF-S027].
>
> **The capital structure is fixed.**
> - Stage D: buy $42k of equipment before any proof, plus a $45k kit and vehicle for every technician. That gave about $230k peak funding.
> - Stage E: rent first, buy the founder's kit only after proof, lease technician kits and pay technicians mileage for their own cars. Base-case peak funding is now **$51,180 with the standard owner draw and $48,622 without it**.
> - About $48.6k of that is at risk before the first technician is hired.
>
> **The model (rebuilt today):**
>
> | Scenario | Year-3 operating profit | Year-5 operating profit |
> |---|---|---|
> | Base | $106,226 | $174,985 |
> | Conservative | $34,834 | –$55,758 |
>
> - In the conservative case a hired technician loses money at $550 a month per account. The honest conservative business is a founder-only job earning roughly $45–68k a year (analyst variant, §7).
> - Evidence stays at **D**: prices and equipment are B/A, but account behaviour is E.
>
> **What it is and is not.** It is a good first cash asset with an acquirer exit. On its own it is not a holding-company engine: base operating profit reaches $233k in year 10 and never $250k in Chicago alone.
>
> **The single cheapest decisive test** is a two-week "last invoice and wait time" interview sprint with 12 or more electrical and plumbing project managers or foremen from the permit list, plus three coring firms. It costs about $0–200. Ask what they last paid for a half-day scan, how long they waited, and whether they would book a dated half-day at $550.
> - **Pass:** median last-paid ≥ $550, ≥ 30% report waits over 48 hours or dissatisfaction, and ≥ 3 dated conditional bookings.
> - **Kill:** median < $400, or "our coring sub scans for free".

---

## 1. Business explanation (for someone new to the industry)

**The problem.** Before an electrician cores a 4-inch hole through a concrete floor for a conduit riser, someone has to know what is inside the slab. Downtown slabs can hold:
- live conduits;
- reinforcing steel;
- in post-tensioned buildings, steel tendons under tens of thousands of pounds of tension.

A drill bit that hits a tendon or an energized conduit can injure workers, shut down a building and trigger a claim. GPRS, the largest scanning firm, says a missed post-tension cable or conduit costs an average of $56,000 per incident [D, E-WS13014-S004]. That figure is incumbent marketing, but it shows the order of magnitude.

The same logic applies outdoors. In Illinois, the one-call system's member utilities mark only their own lines. They do not locate customer-owned lines such as sewer laterals, site lighting, sprinkler and fire mains, secondary electric or septic lines, and the owner bears the cost of protecting them [B, WS11-S031]. Inside the City of Chicago, the one-call service is 811 Chicago (DIGGER). Outside the city it is JULIE [A, E-WS13014-S012].

**What the business sells.** A trained technician arrives with two instruments:
- a **ground-penetrating radar (GPR)** unit, which sends radio pulses into concrete or soil and reads the reflections;
- an **electromagnetic (EM) locator**, which traces metal pipes and cables, either by putting a signal on them or by picking up existing current.

The technician scans the area, marks the slab or ground with paint or tape ("no-cut zones", line paths, approximate depths), and leaves a same-day PDF report with photographs. For campus and industrial work the deliverable can be a simple CAD or KMZ map.

**Who buys and why.**
- **Main buyers:** subcontractor project managers and foremen at electrical, plumbing and HVAC firms, and general contractors' superintendents. They buy because their own contracts, their GC or the building owner require scanning before coring, and because a strike is far more expensive than a $600 half-day.
- **Facility managers** at campuses, hospitals and plants buy locating before excavation, fence, EV-charger or landscaping work.

**How it earns.** Pricing is half-day or full-day flat rates, plus extras for after-hours work and mapping. Equipment is bought once and lasts years. The variable cost is technician time. The whole business is **technician utilization × price per visit**.

**Why it is attractive for this founder.**
- It is technical, suits a research background and needs no licence (§5).
- Customers rebook for every new penetration.
- GPRS grew from one founder renting a scanner in 2001 to 400+ project managers in 54+ metros [D, WS13-S032; C, C3-S025], and it buys small firms [D, WS13-S033].

**Why it is hard.**
- GPRS already runs Chicago crews and markets exactly the "one call to report" service a newcomer would pitch [D, DF-S032].
- Local specialists and coring firms scan in-house [D, DF-S031].
- Chicago permit counts fell 34% from 2019 to 2025 [A, WS10-S010].

---

## 2. Commercial entry

### 2.1 Niche, customer, geography
**Initial niche.**
- **Core:** GPR slab and wall scanning before coring and saw-cutting, for renovation subcontractors in occupied Chicago concrete buildings (Loop, River North, West Loop, Near North, Fulton Market).
- **Secondary:** EM + GPR private-utility locates on Cook and DuPage industrial, campus and commercial sites.

**The wedge:**
- next-business-day booking in the suburbs and on downtown overflow;
- published flat half-day pricing;
- the report in the foreman's inbox before the crew leaves the floor.

**Excluded at entry:**
- anything labelled a survey;
- ASCE 38 "quality level" deliverables (§5.6);
- sewer CCTV (an adjacency, §6);
- residential one-offs, except as fill-in.

**Demand base:** the City of Chicago issued 5,042 permits with a reported cost of at least $250k between January 2025 and November 2026, of which 3,325 were renovations or alterations. The most frequent contractors are named in those permits [A, DF-S030].

### 2.2 Named suppliers and partners

| Need | Supplier | Published terms | Evidence |
|---|---|---|---|
| EM locator (rental) | UCG Underground Supplies | RD8200 + TX10 kit at $599 for one month, or $499 a month for two or more | [B, DF-S026] |
| EM locator (buy, used or new) | UCG | Used RD7000 DL + TX5 kit $2,300; used Vermeer Verifier G3+ $2,949; new RD7200 + TX5 $5,657; new RD8200 + TX10 $9,592 | [B, E-WS13014-S007; B, DF-S026] |
| Concrete GPR (rental) | CSDS (Sensors & Software Conquest 100) | $125 per day, 3-day minimum; California dealer, shipping cost MISSING | [B, E-WS13014-S001] |
| Concrete GPR (rental) | Field Environmental (GSSI StructureScan Mini XT 3D) | $450 per day, $1,050 per week, $3,000 per month | [D, DF-S038] |
| Utility GPR (rental) | CSDS (LMX200 bundle) | $155 per day, 3-day minimum | [B, E-WS13014-S001] |
| Concrete GPR (buy) | GSSI, Proceq, Hilti, Leica via dealers | Complete system $12–19k [D, E-WS13014-S004]; handheld $11–17k [D, C3-S024]; used StructureScan Mini LT around $10.8k asking (D, search result) | D |
| Utility GPR cart (buy or lease) | UCG | LMX100 $20,508; LMX200 $36,476; ImpulseRadar PinPointR $18,444 | [B, DF-S026] |
| Equipment lease | KWIPPED marketplace (Leica C-Thrue) | $825.30 a month for 36 months; first and last month upfront; the schedule implies about 7% APR | [B, E-WS13014-S006] (APR is analyst arithmetic) |
| Training: EM | CSDS NULCA-certified course | $500 per person, 1 day in person plus 1–2 h online | [B, E-WS13014-S002] |
| Training: GPR | Radiodetection online, NULCA-accredited | $200, about 2 h | [B, E-WS13014-S003] |
| Training: hands-on concrete GPR | Manufacturer or rental house | About $500 per person per day | [D, E-WS13014-S004] |
| Insurance | Broker or Insureon-type marketplace | Excavation-class medians: GL $120, E&O $67, umbrella $93, inland marine $101, WC $190, auto $370 per month | [D, E-WS13014-S009] |

### 2.3 Top 15 prospects (full list of 39 in `09_databases/prospects/WS13-014_prospects.csv`)
- **Who is first:** subcontractors before GCs. Electrical and plumbing foremen order cores weekly and choose their own scanning vendor. Large GCs often hold national-vendor master service agreements (assumed, E).
- **Permit counts** are City of Chicago permits ≥ $250k from January 2025 to November 2026 [A, DF-S030].
- **Status:** none of these organizations has been contacted.

| # | Organization (HQ) | Type | Permits | Why this one |
|---|---|---|---|---|
| 1 | Great Lakes Plumbing & Heating (Westmont) | Plumbing | 141 | Highest plumbing count; drain and riser coring in slabs |
| 2 | Johns Plumbing (Chicago) | Plumbing | 114 | High count, city-based, smaller jobs, so more frequent half-days |
| 3 | DW Mechanical Group (Hoffman Estates) | Plumbing | 101 | Added at Stage E; suburban HQ |
| 4 | Admiral Heating & Ventilating (Hillside) | HVAC | 100 | Duct and pipe penetrations |
| 5 | Kelso-Burnett (Rolling Meadows) | Electrical | 96 | Highest electrical count; also campus and industrial feeders |
| 6 | Texa Engineering (Cary) | Electrical | 93 | Added at Stage E; outer-collar HQ fits the suburban-response pitch |
| 7 | Maron Electric (Skokie) | Electrical | 92 | High count and large projects |
| 8 | Current Communications (Broadview) | Low-voltage / electrical | 87 | Added at Stage E; many small penetrations |
| 9 | Ewing-Doherty Mechanical (Bensenville) | Plumbing | 87 | High count |
| 10 | Molloy Electrical (Chicago) | Electrical | 74 | City-based, mid-size, so a likely foreman-level buyer |
| 11 | CECO Inc. (Chicago) | Electrical | 71 | City-based, mid-size |
| 12 | REX Electric & Technologies (Chicago) | Electrical | 67 | City-based |
| 13 | JC Anderson (Elmhurst) | Interiors GC | 81 | Interior build-outs mean many small cores |
| 14 | Executive Construction (Hillside) | Interiors GC | 80 | Same |
| 15 | Cobra Concrete Cutting (Chicago) | Coring firm (partner or competitor) | n/a | Has an in-house GPR team [D, DF-S031]. Test whether it buys overflow or utility-locate help |

**Secondary segment** (A-level data, used for targeting only). 811 Chicago publishes about 1,200 utility-hit tickets a year: 1,205 in 2025 and 1,165 in 2026 to 26 November. The most-hit facilities are gas services (655 in 2025–26) and water services (462) [A, E-WS13014-S013].
- The frequent excavators in that data (water, sewer and gas contractors) are a later segment for private-side locates.
- The City states that a hit ticket does not establish fault.
- **Never reference hit data in outreach.**

### 2.4 Competitors and positioning
- **GPRS:**
  - national, with a Chicago office;
  - markets Chicagoland utility locating, concrete scanning, video pipe, leak detection and 3D scanning [D, DF-S032];
  - 400+ project managers and a 400-hour training standard [D, C3-S024];
  - revenue estimates range from $29M to $244M [D, C3-S027].
- **Hard Rock Technologies:** Chicago, 5 CSDA-certified GPR technicians [D, DF-S031].
- **Butler Scanning:** Gurnee; scanning plus coring and sawing; serves 6 states [D, DF-S031].
- **Cobra Concrete Cutting:** in-house GPR [D, DF-S031].
- **Self-performers:** subcontractors who rent a Mini XT at $450 a day [D, DF-S038].

**Positioning:**
- Do not undercut GPRS.
- Sell three things it cannot always guarantee in the outer collar:
  - booking within 24–48 hours;
  - the same technician every time, who knows the foreman's buildings;
  - a flat published price.
- Whether GPRS has capacity gaps there is **unverified** and is the first thing the sprint must measure.

### 2.5 Pricing (draft rate card; E within B/D anchors)

| Service | Price | Basis |
|---|---|---|
| Concrete scan, half-day (≤ 4 h on site) | $595; first-visit trial floor $550, never lower (the promotion gate) | Guides $300–600 [D, C3-S028] |
| Concrete scan, full day (≤ 8 h) | $1,095 | Consistent with GSA ceiling $124.69–135.26/h × 8 h [B, DF-S029; E-WS13014-S014] |
| Additional hour | $150 | |
| Private-utility locate (EM + GPR sweep) | $650 half-day / $1,195 full day | Covers the per-job GPR cart rental of $465 per 3-day block [B, E-WS13014-S001] |
| CAD/KMZ export of a locate | $150 | |
| After-hours or weekend | +30% | |
| Outer zone (> 40 mi) | $95 mobilization | |
| Late cancellation (< 24 h) | 50% | |
| Payment | Net-30 for approved accounts; card on site for first jobs | |

The model's ARPC of $750 a month means about one visit per account per month at this mix.

### 2.6 Sales and acquisition strategy
1. **Permit-triggered prospecting.** Every week, pull new Chicago permits ≥ $250k and list the electrical, plumbing and HVAC contractor of record [A, DF-S030].
2. **Foreman-level contact.** Visit active job sites with a one-page offer sheet and a sample report. Ask for the next core date, never for "a meeting".
3. **First visit at the floor price ($550).** Deliver the report before the crew leaves. Ask for the next booking on site.
4. **Lunch-and-learns** at subcontractor offices: "reading a scan report; what GPR cannot see".
5. **Coring firms.** Offer overflow and utility-locate capacity to 3 firms (test E3).
6. **Google Business Profile and a simple site** for "concrete scanning [suburb]" (in the $400 a month fixed marketing line).
7. **Prequalification.** Prepare COIs to GC forms [B, E-WS13014-S008] and register on GC vendor portals only when asked.

**Model funnel (base, all E):** 22 qualified conversations a month → 50% get a priced first job → 35% become repeat accounts → about 3.9 new accounts a month at full pace. Churn is 5% a month, CAC $250.

---

## 3. Transaction economics (line by line; costs E unless tagged)

| # | Transaction | Revenue | Direct costs | Contribution | Cash timing |
|---|---|---|---|---|---|
| T0 | **Pilot half-day on a RENTED kit**, at the gate price | $550 | GPR rental share $350 (a $1,050 week over 3 jobs [D, DF-S038]); EM rental share $100 [B, DF-S026]; vehicle/parking $55 [A, E-WS13014-S016]; supplies $10; founder time 5 h at a $40/h shadow wage $200 | **$35** after the shadow wage ($235 before) | Card on site, or net-30 |
| T1 | **Half-day slab scan on an owned kit** (electrical sub, high-rise) | $600 | Technician 5 h at $40/h loaded $200; vehicle/parking $45; kit depreciation $15; supplies/report $10 | **$330 (55%)** | Net-30/45 |
| T2 | **Full-day private-utility locate + GPR sweep** (GC, campus or industrial) | $1,100 | Technician 9 h $360; vehicle $55; kit depreciation $30; paint/map $20 | **$635 (58%)** | Net-30/45 |
| T3 | **Federal facility sewer/utility mapping** (a real comparable) | $5,800 [A, DF-S027] | Technician 4 days $1,300; equipment incl. CCTV rental $600; travel $450; CAD/GIS $300 | **$3,150 (54%)** | Government net-30 |

**What the transactions show.**
1. **Rented-kit jobs are a test, not a business.** T0 nearly breaks even once founder time is counted. The pilot is judged on price and repeat bookings, not margin.
2. **The real unit is a technician-month.**

| Technician-month | Accounts × ARPC | Revenue | After gross margin and 5% variable cost | Technician cost | Contribution |
|---|---|---|---|---|---|
| Base | 20 × $750 | $15,000 | $12,750 | $8,300 | **+$4,450 a month** |
| Conservative | 20 × $550 | $11,000 | $9,130 | $9,200 | **–$70 a month** |
| Optimistic | 20 × $1,000 | $20,000 | $17,400 | $7,700 | **+$9,700 a month** |

At the base cost the break-even ARPC per technician is about **$488**, and **$554** in the conservative case. **This is why the hire gate requires realized ARPC of at least $650.**

3. **Cash timing.** At 45 days DSO, every $10k of monthly revenue ties up about $15k of receivables (model working-capital logic).

**Failure risks per transaction:**
- a missed tendon or conduit (liability);
- a slab too thick or congested for GPR, where the honest answer is "X-ray or no-cut";
- no-show or cancellation;
- slow-paying GCs.

**Repeat potential** is high per subcontractor, because every project has many penetrations. It is low per one-off owner.

---

## 4. Validation plan (ordered by information value per dollar)

### 4.1 Minimum viable commercial offering
- One founder-technician, insured to GC-form limits.
- NULCA-accredited EM training and hands-on concrete GPR training.
- A rented kit: EM locator monthly, concrete GPR by the week, utility GPR by the 3-day block.
- A published half-day and full-day rate card, and same-day PDF reports.
- Service area: Chicago plus near Cook and DuPage.

### 4.2 Experiments

| # | Experiment | Cost | What it tells you | Pass | Kill / pivot |
|---|---|---|---|---|---|
| E0 | Desk prep (Claude, before 5 Dec): refresh the permit target list; build the interview, insurance and rental question sets (materials file) | $0 | Readiness | Done | n/a |
| **E1** | **Price and wait-time sprint:** ≥ 12 project managers/foremen from the top-15 list plus walk-ups at permitted sites; ask about past behaviour only (last job, last price, wait, who scanned) | **$0–200** (gas, parking, coffee) | Price, pain and incumbency: the decisive unknowns | Median last-paid half-day ≥ $550; ≥ 30% report waits > 48 h or dissatisfaction; ≥ 3 dated conditional bookings at ≥ $550 | Median < $400; or most say "the coring sub does it free"; or GPRS same-day everywhere with no complaints |
| E2 | Insurance indications from 2–3 brokers to the W.E. O'Neil-type form (GL $1M/$2M incl. XCU/underground, auto $1M, EL $1M, umbrella $2M, PL $1M) [B, E-WS13014-S008] | $0 (no binding) | Feasibility and fixed cost | Written indication ≤ $10k a year with XCU and AI endorsements | > $20k a year, or "no market for a new locator" → pivot to subcontracting under an insured firm, or stop |
| E3 | Coring-firm partner test: offer overflow and utility-locate capacity to Cobra plus 2 others | $0 | Channel and competitor behaviour | ≥ 1 firm says it would send overflow at ≥ $500 a half-day | All scan in-house and refuse → wedge weaker; lean on the subcontractor channel |
| E4 | Training: GPR online $200 [B]; NULCA EM $500 [B] (Illinois provider MISSING); 2 days hands-on concrete GPR ~$1,000 [D] | $1,700 (+ ≤ $700 travel) | Competence and credentials | Certificates, plus 20 practice scans on known slabs | Founder dislikes fieldwork → stop |
| **E5** | **Rented-kit pilot, 60 days.** Rent the EM kit monthly; rent concrete GPR only for weeks with ≥ 2 booked jobs | Rentals $1,098 (EM, 2 months) + ~$2,100–3,150 (GPR, 2–3 weeks) + $930 (2 utility blocks) | Real price, delivery quality, rebooking | **≥ 10 paid visits; realized median half-day ≥ $550; ≥ 3 repeat accounts within 60 days of first job; zero strikes** | < 5 paid visits, or median < $500 → stop; repeat 1–2 → extend 30 days once |
| E6 | Month-6 gate (owned kit) | Operating | Trajectory | ≥ 6 active accounts, ARPC ≥ $600, DSO ≤ 45 | < 4 accounts → stay part-time or pivot (§4.4) |
| E7 | Hire gate (base month ~12) | Operating | Delegation economics | ≥ 20 active accounts; founder ≥ 22 billable visits a month for 2 months; realized ARPC ≥ $650; backlog > 5 business days; churn < 5% a month | Fails → no hire; stay owner-operator |

**The promotion criteria from Stage D are built into E1 and E5:** half-day price of at least $550 and at least 3 repeat accounts within 60 days.
- The E5 bar sits above the base model's ramp, which has only about 1.9 accounts by month 4.
- So passing it is evidence for at least the base case, not merely consistent with it.

### 4.3 Validation budget (gross, worst case)

| Item | Cost |
|---|---|
| Training | $1,700 (+ $700 travel if out of state) |
| Rentals | $4,128–5,178 |
| Insurance for the first quarter | ~$2,250 (E; quote MISSING) |
| PPE and marking | $400 |
| LLC and admin | ~$300 (E; Illinois filing fee to confirm) |
| Marketing basics | $150 |
| Sales travel | $300 |
| **Total** | **≈ $9.2–10.3k** |

- Ten paid visits at about $575 bring in about $5.75k (≈ 70% collected by day 90). **Net at-risk if the pilot passes: ≈ $4–5k.**
- Because spending is staged, a failed E1 sprint stops spending at **≤ $200**.
- A failed E2 stops it at **≤ $900**, the cost of the online course plus the NULCA course if booked.

**Correction.** Stage D budgeted the rent-before-buy pilot at $1,500–3,000. That omitted training and insurance. The realistic gross cost is about $9–10k, of which roughly half returns as pilot revenue.

### 4.4 Conditions to invest more, abandon or pivot
- **Invest (buy the founder kit: $21,657 base, $13,100 used):** E5 passes, E2 is bound at ≤ $10k a year, and E3 shows no "free scanning" ceiling.
- **Abandon:**
  - E1 median below $400;
  - insurance unavailable;
  - E5 fewer than 5 paid visits;
  - any strike caused by an interpretation error during the pilot;
  - the founder finds the field-and-sales load unsustainable.
- **Pivots, in order of preference:**
  1. Private-utility locating only, for fence, irrigation, EV-charger and solar installers in the collar counties. The JULIE gap is structural [B, WS11-S031].
  2. Overflow subcontractor to coring firms, lower price with zero acquisition cost.
  3. Facility utility mapping for campuses.
  4. Stop, and sell the kit on the used market (UCG lists used locators at $2.3–4.5k [B, E-WS13014-S007]).

---

## 5. Operations

### 5.1 Lead-to-cash workflow
1. **Request** by phone, text, web form or email. Intake captures:
   - site address and floor;
   - slab type if known (PT, rebar or unknown);
   - number and size of penetrations;
   - for outdoor work, the 811 Chicago or JULIE ticket number (the excavator's duty);
   - access and escort needs and site-safety orientation;
   - who signs the report.
2. **Quote and schedule** within 2 business hours. Book in the CRM/FSM; confirm the day before.
3. **Pre-visit.**
   - COI sent with the GC's additional-insured wording.
   - Kit check: batteries, calibration log, marking supplies.
   - For rented units, rental pickup or delivery.
4. **On site.**
   - Safety orientation.
   - Calibrate on known features.
   - Scan in grid passes.
   - EM sweep for energized conduits.
   - Mark targets and no-cut zones.
   - Photograph every mark with a scale.
   - Walk the foreman through limitations.
5. **Report the same day:** PDF with photos, target list, depth estimates with a stated uncertainty, a limitations statement, and the technician's credentials. CAD/KMZ for locates.
6. **Invoice the same day.** Card on site for first jobs; net-30 accounts.
7. **Follow-up.** Ask for the next core date. Log the account's project pipeline.
8. **Collections.** Reminders at day 25, 35 and 45. Escalate to the PM at day 50.

### 5.2 Function classification

| Function | Human | AI-assisted | Automatable | Professional-dependent | Not automatable |
|---|---|---|---|---|---|
| Prospecting from permits | | ✓ (Socrata queries plus scoring) | ✓ weekly pull | | |
| Foreman relationship and site visits | ✓ | | | | ✓ |
| Quoting and scheduling | ✓ | ✓ drafts | ✓ confirmations | | |
| Scanning and EM locating | ✓ | | | | ✓ |
| Radargram interpretation (liability) | ✓ certified technician | Second-look aids only | | | ✓ (final call stays human) |
| Report drafting | | ✓ from field notes and photos | Template fill | | |
| ASCE 38 quality-level or SUE deliverables | | | | ✓ PE in responsible charge [C, E-WS13014-S011] (partner only) | |
| Survey-grade mapping | | | | ✓ Illinois PLS (E) | |
| Invoicing and reminders | | ✓ | ✓ | | |
| Bookkeeping and tax | | ✓ | | ✓ CPA at year-end | |
| Insurance placement | | | | ✓ broker | |
| Hiring and training technicians | ✓ | ✓ SOPs and quizzes | | | ✓ field mentoring |

### 5.3 Fulfilment, support, QA, exceptions
- **QA.** Every interpretation is checked against the walk-through and, on PT slabs, a second pass at a different orientation. Every report carries a limitations section: GPR cannot reliably see below congested top mats, through some metal decks, or plastic conduits without water.
  - From technician #1: monthly peer review of 5 random reports, plus a "strike drill" checklist.
- **Exceptions:**
  - **Strike or suspected strike:** stop work, make safe, notify the GC and 811 Chicago if it involves a utility facility (Chicago code requires immediate notification [A, E-WS13014-S013]), photograph, notify the insurer the same day.
  - **Unscannable slab:** recommend X-ray (refer to a partner) or a no-cut decision; charge the half-day.
  - **Rental unit failure:** keep a backup reservation; never scan PT with an unverified unit.
- **Support:** a reachable mobile line; reports kept 7 years for claims (E).

### 5.4 Software stack (prices E unless tagged)

| Tool | Cost |
|---|---|
| Field service and CRM: Housecall Pro Basic, or Essentials for dispatch | $59/mo billed annually, or $149/mo [B, DF-S035] |
| Accounting (QuickBooks-class) | ~$35–100/mo (E) |
| Scanner software | Bundled with the unit (E) |
| QGIS for KMZ/SHP exports | Free (E) |
| Google Workspace | ~$7–14 per user (E) |
| AI drafting (API or subscription) | ~$20–100/mo (E) |

The model carries $300 a month for software and AI. The "AI cost ×3" stress cuts year-3 profit only from $106,226 to $98,587.

**After December 2026,** the AI uses are low-volume: report text from field notes, proposals, follow-ups and permit scoring. The fallback is fixed templates plus a scripted permit pull, which needs no AI. **Nothing in delivery depends on AI.**

### 5.5 Legal and administrative requirements
- **Entity:** Illinois LLC. Filing fee to confirm with the Secretary of State (E).
- **Licence:** no Illinois licence for private locating or GPR scanning was identified. This is unverified: ilga.gov returned HTTP 503 again today, so 220 ILCS 50 was not re-read (E).
  - City of Chicago business-licence applicability: MISSING.
- **One-call rules:**
  - Inside Chicago, the excavator obtains an 811 Chicago ticket with 2 business days' minimum notice [A, E-WS13014-S012].
  - Outside Chicago it is JULIE, with at least 2 days' notice excluding the day of notice [B, WS11-S031].
  - The private locate supplements the ticket; it never replaces it.
  - **Correction:** the Stage D workflow said "JULIE ticket check" for Chicago sites. Inside city limits it is 811 Chicago (DIGGER), and digs on a boundary street need both.
- **FCC:** GPR is an ultra-wideband imaging device. Operator coordination or registration duties under FCC Part 15 UWB rules must be confirmed with the manufacturer (E, not verified).
- **OSHA:** excavation rules require utility locations to be estimated before digging. This is the excavator's duty and general knowledge, not re-verified (E).
- **Employment:**
  - Use W-2 technicians.
  - Illinois' construction-industry employee-classification rules make 1099 field technicians risky (E; statute not re-read).
  - Workers' compensation is required once there are employees.
  - Public-works jobs may trigger Illinois prevailing wage (E; confirm the classification).
- **Insurance:** see E2 and §12.

### 5.6 Survey and SUE boundary
**Correction and refinement.** Stage D excluded only "legal surveys". The FHWA's description of Subsurface Utility Engineering defines:
- **Quality Level B** as surface-geophysical designating;
- **Quality Level A** as exposure and measurement.

It says those in responsible charge and certifying deliverables should be registered engineers, geologists or land surveyors [A, E-WS13014-S010]. Under ASCE 38-22, a quality level "requires a PE seal in order to exist" [C, E-WS13014-S011].

**So:** sell "private utility locating and marking" and "concrete scanning reports". Never sell "QL-B" or "SUE". Offer QL work only as a subcontractor to a PE-led firm.

### 5.7 Financial administration
- Weekly invoicing review, DSO tracking and a 13-week cash forecast.
- Separate tax savings at 30% of profit after draw (model tax rate).
- Equipment lease payments on autopay.
- A rental-damage waiver (+10% of the daily rate at CSDS [B, E-WS13014-S001]) during the pilot.

---

## 6. Growth

### 6.1 First 10 and first 100 customers
**First 10:**
- From the E1 sprint conversations: the electrical and plumbing subcontractors in the top 15, starting with city-based mid-size firms (Molloy, CECO, REX, Johns Plumbing), where a foreman can say yes.
- Plus one coring-firm overflow relationship.

**Accounts 11–100:**
- referrals as foremen and superintendents move between firms;
- lunch-and-learns;
- GC approved-vendor lists once the COI and a safety program exist;
- the business-development hire at 45 active accounts (base month 21);
- referral and inbound at 1 per 100 active accounts per month (E).

**Base model:** 25 active accounts at the end of year 1, 54 at the end of year 2, 82 at the end of year 3, and 110 at the end of year 5.

### 6.2 Hiring sequence (gated; model triggers in brackets)

| Hire | Trigger milestone | Cost | Productivity |
|---|---|---|---|
| **Technician #1** | E7 hire gate (≥ 20 accounts, ARPC ≥ $650, backlog) [model: active ≥ 20, base month 12] | $8,300/mo loaded incl. leased kit and mileage; $3,000 capex | ~20 accounts, ~$180k/yr revenue; contribution ~$4,450/mo at base ARPC |
| Technician #2+ | Every +20 accounts and E7 conditions again [base month 19] | Same | Same |
| BD rep (part-time, commission-heavy) | ≥ 45 active accounts [base month 21] | $3,500/mo | 1.2 new accounts/mo after a 3-month ramp (E) |
| Scheduler / report admin | Revenue ≥ $45k/mo [base year 3] | $4,900/mo loaded (dispatcher median $58,900 [C, DF-S033]) | Frees ~10 founder hours a week |
| Operations manager / lead technician | ~5–6 technicians (year 4–5) | Promote the best technician (E) | QA, scheduling, training |

**Capacity limits:**
- the founder carries about 20 accounts (≈ 22–25 half-day visits a month) while also selling 10–15 hours a week;
- each technician carries about 20.

### 6.3 Geographic expansion and adjacencies
**Geography:**
- Phase 1: Chicago plus near Cook and DuPage.
- Phase 2: Lake, Will and Kane, with the technician based in that county.
- Phase 3, only with an operations manager: Milwaukee or NW Indiana. Each is a replicated technician unit.

**Adjacencies, by incremental return:**
1. **Sewer CCTV and lateral tracing:** a RIDGID SeeSnake Mini 200 ft costs $9,347 [B, E-WS13014-S007]. It reuses the EM locator (sonde tracing) and sells to plumbers and facility managers. The comparable T3 federal job paid $5,800 [A, DF-S027].
2. **Campus utility mapping** (CAD/KMZ) for facility managers: recurring annual updates. Small private locators win recurring federal facility contracts of $9.8k–27.2k a year [A, E-WS13014-S015].
3. **SUE subcontracting** to PE-led firms (designating only).
4. 3D laser scanning and leak detection follow GPRS's adjacency path [D, DF-S032]. These are higher capex, so year 4+.

**Vertical integration** into coring or sawing is not recommended: it is a heavier-capital trade and competes with channel partners.

### 6.4 Delegation and reinvestment
- **When a manager can run day-to-day:** at about 5–6 technicians, with a lead technician doing QA and a scheduler. **The founder keeps sales and key accounts until a BD rep has held accounts for a year.**
- **Reinvestment slots:**
  - technician units (~$45k growth capital each: $3k capex, ~$25k receivables, ramp losses);
  - the CCTV adjacency (~$10–15k);
  - county expansion.
- The model's incremental pre-tax return on growth reinvestment is set at **0.6 base**.

---

## 7. Financial analysis (quoted from the rebuilt `WS13-014_results.json`)

### 7.1 What changed in the model, and why (Stage D → Stage E)
1. **Rent, don't buy, in months 1–3.**
   - Rentals are $1,900/mo base, expensed.
   - The founder's kit is bought in **month 4** only after the gate: **$21,657 base**, $26,600 conservative, $13,100 optimistic (used).
2. **Utility GPR cart** is rented per job (one $465 block a month) until month 13, then **leased**: $633/mo base; a $1,266 deposit as capex.
   - **Correction:** Stage D bought a $20,508 cart in month 4, before any proof.
3. **Technicians.** The kit is leased at about 7% APR over 36 months [B, E-WS13014-S006], and mileage on the technician's own car is paid at IRS 72.5–76¢ a mile [A, E-WS13014-S016].
   - Loaded cost is $8,300/mo base; capex is $3,000 per hire.
   - **Correction:** Stage D charged $45,000 of capex per hire (kit plus a $20k used vehicle). Its insurance line was flat regardless of headcount; per-technician workers' comp and auto cost now sit inside technician cost.
4. **Hire on backlog.** The first technician comes when the founder carries 20 accounts, not 15. Technician capacity is unchanged at 20 accounts.
5. **The business-development hire** comes at 45 active accounts, not automatically in month 24.
6. **Standardization:**
   - owner draw $4,000/mo from month 13;
   - tax 30%;
   - `start_capital_injection` = **$52,000**, the smallest $1k amount that keeps base cash ≥ 0 (minimum cash balance $820.15);
   - long-term drivers evidenced (EV 2.0/3.0/3.5×, incremental ROIC 0.3/0.6/0.9).

**Attribution (base case, engine re-runs):**
- Moves 1–3 cut peak funding from $230,074 to $80,618, but lowered year-3 profit from $112,443 to $76,951, because leasing and mileage cost more per month than owning.
- Move 4 (hiring on backlog) brings year-3 profit to $112,173 and peak funding to $48,622.
- Move 5 (an earlier, demand-triggered BD hire) gives the final **$106,226 / $51,180**.
- So the operating economics are about the same as Stage D. **The difference is capital, not optimism.**

### 7.2 Five-year annual view

| | Y1 | Y2 | Y3 | Y4 | Y5 |
|---|---|---|---|---|---|
| **Base revenue** | $87,588 | $383,087 | $670,544 | $904,038 | $1,065,820 |
| **Base operating profit** (before owner pay; includes founder fieldwork) | $13,417 | $100,120 | $106,226 | $158,360 | $174,985 |
| Base FCF | –$42,683 | $47,234 | $48,629 | $102,021 | $117,485 |
| Base owner draw | $0 | $48,000 | $48,000 | $48,000 | $48,000 |
| Base retained after draw | –$42,683 | –$766 | $629 | $54,021 | $69,485 |
| Base active accounts / headcount at year-end | 25 / 1 | 54 / 3 | 82 / 6 | 99 / 6 | 110 / 7 |
| **Conservative operating profit** | –$37,287 | $13,946 | $34,834 | –$60,606 | –$55,758 |
| Conservative active / headcount | 9 / 0 | 17 / 0 | 20 / 1 | 22 / 1 | 23 / 1 |
| **Optimistic operating profit** | $90,281 | $406,595 | $822,314 | $1,135,652 | $1,435,043 |

**Interpreting the scenarios:**
- **Base:** operating margin 15.8% in year 3 and 16.4% in year 5. That is plausible for a labour-intensive field service; US NAICS 541370 firms with $1–2.5M receipts pay 45.9% of receipts as payroll [C, C3-S015].
- **Optimistic:** a 43.6% margin. **Treat it as an upper bound, not a forecast.**
- **Conservative:** goes negative in year 4 because the engine hires technician #1 in month 36 at a $550 ARPC, where a technician loses about $70 a month.
  - The analyst variant with the same engine and no hires is the real conservative business: a one-person firm making **$44,594 in year 3 and $68,498 in year 5**, with peak funding of $127,107 including draws ($80,179 without).
  - That variant is not in `results.json`.

### 7.3 Launch capital, working capital, funding

| Item | Base |
|---|---|
| Founder kit (month 4) | $21,657 |
| Cart lease deposit (month 13) | $1,266 |
| Technician hire capex | $3,000 each |
| Total capex, Y1 / Y2 / Y3 | $24,657 / $4,266 / $6,000 |
| Working-capital build, Y1 / Y2 / Y3 | $27,418 / $32,984 / $34,129 |
| **Peak funding with standard draw** | **$51,179.85** (month 30) |
| Peak funding without draw | $48,622 (month 8; engine re-run) |
| Breakeven (first month with positive operating profit) | Month 7 |
| Payback (cumulative retained ≥ 0) | Month 47 |
| Year-3 operating profit ÷ peak funding | 2.08 |
| Conservative peak funding | $356,043.76 (cash never recovers while $48k a year is drawn) |
| Optimistic peak funding | $31,518.35 |

### 7.4 Twenty-four-month base view (engine monthly rows = `M_Base` sheet)

| Month | Active accounts | Revenue | Operating profit | Staff cost | Capex | Cumulative retained | Cash (with $52k injection) |
|---|---|---|---|---|---|---|---|
| 1 | 0.0 | $0 | –$4,850 | 0 | 0 | –$4,850 | $47,150 |
| 2 | 0.0 | $0 | –$4,850 | 0 | 0 | –$9,700 | $42,300 |
| 3 | 0.6 | $481 | –$4,601 | 0 | 0 | –$14,999 | $37,001 |
| 4 | 1.9 | $1,424 | –$2,527 | 0 | $21,657 | –$40,550 | $11,450 |
| 5 | 3.7 | $2,811 | –$1,511 | 0 | 0 | –$44,073 | $7,927 |
| 6 | 6.2 | $4,624 | –$136 | 0 | 0 | –$46,837 | $5,163 |
| 7 | 9.1 | $6,845 | $1,586 | 0 | 0 | –$48,472 | $3,528 |
| 8 | 12.6 | $9,459 | $3,640 | 0 | 0 | –$48,622 | $3,378 |
| 9 | 16.0 | $11,968 | $5,764 | 0 | 0 | –$46,496 | $5,504 |
| 10 | 19.2 | $14,377 | $7,803 | 0 | 0 | –$42,281 | $9,719 |
| 11 | 22.3 | $16,689 | $9,760 | 0 | 0 | –$38,802 | $13,198 |
| 12 | 25.2 | $18,909 | $3,340 | $8,300 | $3,000 | –$42,683 | $9,317 |
| 13 | 28.1 | $21,671 | $5,164 | $8,549 | $1,266 | –$47,140 | $4,860 |
| 14 | 30.8 | $23,779 | $6,948 | $8,549 | 0 | –$48,132 | $3,868 |
| 15 | 33.4 | $25,802 | $8,661 | $8,549 | 0 | –$47,802 | $4,198 |
| 16 | 35.9 | $27,744 | $10,305 | $8,549 | 0 | –$46,205 | $5,795 |
| 17 | 38.3 | $29,608 | $11,884 | $8,549 | 0 | –$43,389 | $8,611 |
| 18 | 40.6 | $31,398 | $13,399 | $8,549 | 0 | –$39,405 | $12,595 |
| 19 | 42.9 | $33,116 | $6,305 | $17,098 | $3,000 | –$43,284 | $8,716 |
| 20 | 45.0 | $34,766 | $7,701 | $17,098 | 0 | –$43,084 | $8,916 |
| 21 | 47.1 | $36,349 | $5,437 | $20,703 | 0 | –$44,375 | $7,625 |
| 22 | 49.0 | $37,869 | $6,724 | $20,703 | 0 | –$44,672 | $7,328 |
| 23 | 50.9 | $39,329 | $7,959 | $20,703 | 0 | –$44,017 | $7,983 |
| 24 | 53.9 | $41,657 | $9,633 | $20,703 | 0 | –$43,449 | $8,551 |

**Note.** Months 1–3 carry the full overhead (insurance, the founder's car at the mileage rate, software, accounting, marketing, rental) and no pilot revenue, because account revenue starts in month 3. So the model's –$14,999 at month 3 is more cautious than the ≈ $9–10k cash pilot budget in §4.3.

### 7.5 Sensitivity (±25%, base)
- **ARPC:** $562.50 gives year-3 profit of **$5,322**; $937.50 gives **$243,518**. Peak funding ranges from $396,957 to $47,514.
- **Labour cost:** ×0.75 gives $206,507; ×1.25 gives $5,944.
- **Win rate or leads:** $103,251 to $157,298.
- **Churn** (3.75%–6.25%): $125,314 to $85,809.
- **DSO:** no effect on year-3 profit; peak funding ranges from $45,905 to $72,391.
- The gross-margin row (–$44,647 to $257,098) includes an impossible 112.5% margin and should be read only as "margin matters".

**Decisive ratio:** technician cost relative to price per visit.

### 7.6 Stress tests (base)

| Stress | Y3 operating profit | Y5 operating profit | Peak funding |
|---|---|---|---|
| Base | $106,226 | $174,985 | $51,180 |
| CAC doubles | $84,239 | $151,904 | $83,121 |
| Win rate 40% below plan | $127,790 | $106,222 | $55,051 |
| Gross margin –10 pts | $39,171 | $68,403 | $137,747 |
| Customers pay 30 days later | $106,226 | $174,985 | $114,064 |
| **Labour cost +20%** | **$26,000** | $42,062 | $169,961 |
| **Hires needed 30% sooner** | **–$50,590** | –$45,294 | $551,110 |
| Recession (new –30%, churn ×1.5) | $108,325 | $161,715 | $51,868 |
| **Competitor response** (no price growth, –3 pts margin, churn ×1.3) | $56,081 | **–$4,584** | $128,641 |
| Growth takes twice as long | $66,438 | $158,431 | $71,062 |

The "win rate" and "recession" rows look benign in year 3 only because fewer accounts trigger fewer hires. Year-5 profit and 10-year deployable cash ($183,883 for win rate) show the real damage. **Hiring discipline is the survival variable.**

### 7.7 Profit milestones (base)

| Milestone | When | Optimistic | Conservative |
|---|---|---|---|
| First profitable owned-kit job (T1 contribution $330) | Month 4–5 | | |
| $1k/mo operating profit | Month 7 | | Month 18 |
| $5k/mo | Month 9 | | Never |
| $10k/mo | Month 16 | Month 8 | Never |
| $25k/mo | Never within 60 months | Month 12 | Never |
| $100k/yr | Year 2 ($100,120) | | |
| $250k/yr | Not reached within 10 years (year 10 = $233,343.50) | Year 2 | |
| $500k/yr | | Year 3 | |
| $1M/yr | | Year 4 | |

### 7.8 Capital accumulation to year 10 and owner distributions (base)
| Measure | Base | Conservative | Optimistic |
|---|---|---|---|
| Owner draw | $48k a year from year 2, rising 3% a year from year 6 ($454,484 over 10 years) | | |
| Deployable cash after reinvestment and reserves | Negative in years 1–3; $23,795 in year 4, $45,292 in year 5, rising to $86,862 in year 10 | | |
| 10-year cumulative deployable | **$418,024** | $0 | $6,938,790 |
| Operating profit, year 10 | $233,343.50 | | |
| EV at 3.0× | $524,954 in year 5; $700,030.50 in year 10 | | |
| Model "owner wealth" in year 10 (deployable + draws + EV) | $1,572,538 | | |

**Downside:** in the conservative case, 10-year deployable cash is $0 and year-10 EV is –$123,214.

---

## 8. Capital deployment ladder

| Band | What it buys | Evidence gate before spending | How it could be lost |
|---|---|---|---|
| **$0–500** | Permit list refresh; E1 sprint (gas, parking); GPR online course $200 [B]; broker indications (free) | None (founder decision only) | Time only |
| **$500–2k** | NULCA EM course $500 [B]; hands-on GPR training ~$1,000 [D]; LLC; PPE and marking ~$400 | E1 pass (median ≥ $550, ≥ 3 dated bookings) and E2 indication ≤ $10k a year | Training sunk if demand later fails |
| **$2–5k** | Insurance binding deposit (~$1.5–2.5k, E); first rental month (EM $599 + one GPR week $1,050 + one utility block $465) | ≥ 3 booked jobs on the calendar; COI accepted by the first customer's GC form | Rental and premium sunk if bookings cancel |
| **$5–10k** | The rest of the 60-day pilot (rentals to ~$4.1–5.2k total; insurance for the quarter) | First 3 paid jobs delivered cleanly; ≥ 1 rebooking by day 30 | Low price or no rebooking means ≈ $4–5k net loss |
| **$10–25k** | Buy the founder kit: $21,657 new, or $13,100 used | **Promotion gate:** ≥ 10 paid visits, median ≥ $550, ≥ 3 repeat accounts in 60 days, zero strikes, first invoices paid ≤ 45 days | Accounts stall. Kit resale is partial (used EM kits $2.3–4.5k [B, E-WS13014-S007]; used GPR ~$10.8k asking [D]) |
| **$25–50k** | Months 4–12 operating losses and receivables (model trough –$48,622 at month 8) plus technician #1 ($3,000 capex and lease) | Month-6 gate (≥ 6 accounts, ARPC ≥ $600) then hire gate E7 | Hiring before backlog; a strike claim; DSO > 60 |
| **$50–100k** | Technicians #2–3, cart lease, CCTV adjacency ($9,347 [B]); receivables growth | Technician #1 contribution ≥ $3k/mo for 3 months, DSO ≤ 45, clean insurance renewal; **cumulative owner capital capped at ~$60k (base peak $51,180)** | Price war with GPRS or coring firms; a recession; over-hiring (the "hires 30% sooner" stress drives peak funding to $551k) |

**Rule:** owner capital above about $60k is never needed in the base case. If the business needs more, the gates have failed and it should shrink to owner-operator.

---

## 9. Strategic wealth creation
- **How it becomes a durable cash asset:**
  - a book of 80–110 subcontractor accounts;
  - 4–6 technicians on SOPs;
  - a zero-strike record;
  - approved-vendor status at several GCs;
  - a library of scans of repeat buildings.
- **Cash it could generate (base):** about $100–175k a year of operating profit in years 2–5 (including founder fieldwork), and about $418k of deployable cash over 10 years after a $48k-a-year draw.
- **Management takeover:** day-to-day operations in years 4–5 with a lead technician and a scheduler. Sales delegation is later.
- **Exit:**
  - GPRS buys locating and scanning firms [D, WS13-S033], so a sale at about 2–3.5× operating profit (E/D, DF-S004) is a realistic liquidity path;
  - 3.0× base gives an EV of $524,954 in year 5.
- **Can it fund other ventures?** Modestly. Deployable cash starts in year 4 at $23,795 and reaches $86,862 by year 10. That is enough to seed one small adjacent business, not a holding company.
- **As a first company in a diversified portfolio:**
  - **For:**
    - lowest capital after restructuring (peak $51,180);
    - B2B repeat accounts;
    - compounding technical skill;
    - founder fit;
    - an acquirer exit.
  - **Against:**
    - construction-cyclical (permits –34% [A, WS10-S010]);
    - labour-intensive (payroll 45.9% of receipts [C, C3-S015]);
    - strike-liability tail;
    - entrenched incumbent;
    - base year-10 operating profit only about $233k.
  - **Verdict:** a solid first asset *if* E1 and E5 pass, but not a route to $500k a year without multi-metro replication.

---

## 10. Execution plan

### 10.1 First 7 days (30 Nov – 6 Dec 2026; heavy AI access ends 5 Dec)
**Founder:**
- Answer F1–F7: age, credit (lease approval), location and vehicle, hours, network.
- Decide "validate yes or no".
- Review the drafts in the materials file.
- Start E1 with 4–5 site walk-ups at permitted downtown jobs.
- Call 2 commercial insurance brokers for indications only (E2).

**Claude prepares by 5 Dec:** a fresh 90-day permit pull for all 39 prospects with job addresses, the interview tracker and scoring sheet, an insurance submission narrative (no PII sent), a rental reservation checklist, the KPI sheet, report and quote templates, and a QGIS export template.

**Spend:** $0–200.

### 10.2 First 30 days
**Founder:**
- Complete ≥ 12 E1 interviews. Questions are in the materials file and are past-behaviour only: last scan date, vendor, price, wait, who chose the vendor, what went wrong.
- Run E3 with Cobra plus 2 coring firms.
- Take the GPR online course ($200).
- Book the NULCA EM course and hands-on GPR training, and identify an Illinois provider (MISSING).
- Get 2–3 written insurance indications.
- Form the LLC after E1 passes.

**Organizations to approach:** the top-15 list, plus rental houses (UCG; Pine Environmental and Field Environmental for the Mini XT; CSDS for the Conquest 100) for availability and shipping.

**Evidence required:** E1 pass and E2 ≤ $10k a year.

**Spend:** ≤ $2k.

**Accept a first order only if:**
- insurance is bound with additional-insured wording;
- training is complete;
- the rented kit is verified on a known slab;
- the scope and limitations are in writing;
- the excavator holds an 811 Chicago or JULIE ticket where digging.

**Abandon if:** E1 median is below $400, or insurance is unavailable.

### 10.3 First 90 days
- Run E5: 60 days, ≥ 10 paid visits.
- Track every quote, price, rebooking and payment day.
- Decide at days 75–90:
  - **Buy the kit** (promotion gate), or
  - **extend once** for 30 days (1–2 repeat accounts), or
  - **stop** (< 5 paid visits or median < $500).

**Spend:** ~$9–10k gross, ≈ $4–5k net.

### 10.4 First year
| Period | Milestone |
|---|---|
| Months 4–6 | Owned kit; month-6 gate ≥ 6 accounts (model 6.2) |
| Month 9 | ≥ 14 accounts (model 16.0); utility-locate demand measured |
| Month 12 | Hire gate (model 25.2 accounts); technician #1 with leased kit |

- **Slow-growth branch** (8–15 accounts at month 12): stay owner-operator, add the private-locate pivot for collar-county installers and coring overflow, and do not hire.
- **Failure branch** (< 6 accounts at month 9, or a strike claim): wind down and sell the kit. Expected loss ≈ $25–35k (model base cumulative –$46,496 at month 9, less kit resale).

---

## 11. Pre-mortem

| Failure | Story | Early warning | Cheap preventive test |
|---|---|---|---|
| **Lost $5k** | Pilot rentals and insurance spent; foremen stayed with GPRS or coring firms | < 3 rebookings by day 45; quotes lost on price | E1 before renting; rent GPR only for booked weeks |
| **Lost $25k** | Kit bought; average visit $450; < 8 accounts at month 9 | ARPC < $600 at month 6; DSO > 60 | Hold the kit purchase until the E5 gate; buy used ($13.1k) |
| **Lost $50k** | Technician hired at 15 accounts or at $550 ARPC (–$70/mo per technician); or a PT-tendon claim | Technician utilization < 70%; any mis-mark; E&O premium > $12k a year | Hire gate E7; QA second pass; claims-made E&O with a retro date |
| **Revenue but no profit** | Accounts grow but price slides to compete with GPRS ("competitor response": year-5 profit –$4,584) | Discount requests; rising half-day share | Publish the rate card; sell response time, not price |
| **Exhausting low-paid job** | The founder does every scan plus sales for ~$45–68k a year (conservative owner-only variant) | > 55 h/week for 3 months with < 15 accounts | Month-6 and month-9 gates; pivot to the private-locate niche |
| **Cash crunch** | GCs pay at 75 days ("customers pay 30 days later" peak: $114,064) | DSO > 50 | Card-on-file for first jobs; deal with subcontractors, not GCs; early-pay terms |
| **Can't run without the founder** | Foremen buy from the founder personally; technicians lack interpretation judgment | Customers ask for the founder by name > 50% of the time | Pair-scan for 3 months; report QA; introduce technicians on every account |
| **No deployable surplus** | Draw plus growth capital absorb all cash (base deployable is negative in years 1–3) | Retained < 0 in year 3 | Slow hiring; stop growth capex if retained stays negative for 2 quarters |

---

## 12. Required confirmations (must be confirmed directly)
- **Supplier:**
  - Chicago-area availability and weekly rates for a concrete GPR (Mini XT, Conquest 100, GP8000, PS1000).
  - Whether CSDS ships rentals to Illinois, and at what cost.
  - UCG RD8200 rental availability.
  - Lease approval for a new LLC (depends on founder credit, F2).
  - An Illinois NULCA-accredited course date and the hands-on GPR course price.
- **Customer:**
  - Actual last-paid half-day prices.
  - Booking lead times with GPRS and local firms in the collar counties.
  - Share of subcontractors that rent or own scanners, or rely on coring subcontractors.
  - Who chooses the vendor (foreman, PM or GC).
  - Required prequalification platforms (ISNetworld, Avetta, others).
- **Regulatory:**
  - 220 ILCS 50 text on private locating (ilga.gov unavailable).
  - Whether a City of Chicago business licence applies.
  - FCC UWB operator coordination for GPR.
  - Illinois employee-classification rules for field technicians.
  - Prevailing-wage classification on public jobs.
  - The boundary of the Illinois Professional Land Surveyor Act for maps.
- **Insurance:**
  - Whether a start-up locator can get cover at all.
  - XCU/underground coverage, and whether mis-locates fall under GL or E&O.
  - A $2M umbrella.
  - Workers' comp for an owner-only LLC (GC forms require it [B, E-WS13014-S008]).
  - Inland marine for owned or rented kit.
  - Total premium (modelled at $750 a month base).

## Appendix — Corrections log (Stage D → Stage E)
1. **Peak funding** fell from about $230k / $161k (with / without draw) to **$51,180 / $48,622** after the switch to rent-first, lease and mileage (§7.1).
2. **Pilot budget** of $1.5–3k is now about $9–10k gross (§4.3).
3. **One-call service:** "JULIE" on Chicago sites is wrong; inside the city it is 811 Chicago (§5.5).
4. **Deliverables:** no ASCE 38 quality-level or SUE labels (§5.6).
5. **Insurance** now scales with headcount (§7.1).
6. **BD hire** is triggered by demand (45 accounts), not the calendar (§7.1).
7. **Tornado:** the gross-margin bar is an artifact (§7.5).
8. **Ceiling** is cut from $500k a year to about $250k a year for Chicago alone (§9).
