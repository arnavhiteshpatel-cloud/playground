# SYN-004: Commercial energy cost management (Stage D, batch DI)

Supply brokerage + capacity-tag (PLC) management + demand-response origination + bill audit. Absorbs WS11-007, WS11-010 and WS11-008.

Investigated 2026-11-28. Read-only: nobody was contacted, and no supplier, CSP or ICC forms were submitted. Evidence levels A–E follow `EVIDENCE_STANDARDS.md`. DI- sources are in `05_deep_dives/sources_DI.jsonl`; C7- and WS11- sources come from earlier stages.

> **Verdict: FINALIST (conditional).** Revised composite: raw 5.80, evidence-adjusted **5.56** (evidence D). Stage C was 5.32.
>
> **Decisive facts:**
> 1. **There is a legal day-one path without a licence.** Part 454 does not apply to anyone who procures or sells retail electricity for a customer whose **aggregate Illinois billing demand exceeds 1,500 kW** [A, C7-S003]. Demand-response referral, PLC management and bill audits need no ICC licence. The founder can therefore start by serving multi-site grocers, cold-storage warehouses and food plants while a qualifying person is recruited for an ABC licence.
> 2. **Capacity stays a CFO problem to May 2029.** PJM's 2028/29 auction cleared at the **$325/MW-day cap in COMED**, and a no-cap simulation cleared COMED at **$776.69** [A, DI-S022].
> 3. **The money is now visible from public records.** An Illinois board packet shows the customer keeps **70–75% of DR revenue** and the CSP 25–30% [A, DI-S023].
>
> **Base model:** year-3 operating profit ~$98k on ~$30k peak funding.
>
> **Condition for final selection:** written supplier commission schedules and a CSP partner share. Both are still MISSING.

---

## 1. Specific initial niche

**Energy cost management for ComEd-zone cold-storage warehouses, food and beverage plants, and independent multi-site grocers in Cook, DuPage, Will and Kane counties, each with more than 1,500 kW aggregate Illinois billing demand.** The sequence of work:
1. a free capacity-tag and bill audit;
2. a supply RFP among ARES suppliers, paid as supplier mils;
3. PLC peak management;
4. DR enrollment of refrigeration or process load with a PJM CSP.

**Why this niche:**
- **Commission value.** Independent grocery stores use **2.5–3.3 GWh/yr each**: Pete's Fresh Market's Cermak, Pulaski, Madison, 118th and Kedzie stores, and Shop & Save Archer [A, DI-S003]. A multi-store grocer is a six-figure-kWh commission base.
- **Curtailable load.** Refrigeration has thermal inertia that makes it curtailable (E).
- **Legality.** These customers sit inside the 1,500 kW exemption. "Aggregate billing demand" sums the highest monthly billed demand of each affiliated account [A, 83 IAC 454.20, DI-S019].
- **Why not public bodies:**
  - City Colleges of Chicago enrolled DR with CPower directly through State of Illinois contract CMS5882960 and City of Chicago specification 1257550 [A, DI-S024, DI-S025].
  - The broker's own conflicts are under scrutiny: a 2021 BOMA presentation told buyers to "call any CSP directly" and warned of hidden referral kickbacks [D, DI-S026].

## 2. Named operators

| Operator | Type | What is known |
|---|---|---|
| CPower (Enerwise Global Technologies; NRG-owned) | PJM CSP | Selected provider for City of Chicago Emergency Capacity DR (spec 1257550); City Colleges agreement 2025/26–2026/27 plus three 1-year options [A, DI-S025]; earlier via State contract CMS5882960, with funds escrowed for HVAC upgrades [A, DI-S024]. |
| NRG Curtailment Solutions / Direct Energy Business | CSP + supplier | Customer keeps 70% (NRG) or 75% (Direct); company keeps 25–30%; 5-year contract; paid at end of the DR season [A, DI-S023, 2020]. |
| Enel X North America | CSP | Active in Illinois per the PJM CSP list [A, DI-S021]. Named CSP for ComEd's Mandatory Load Reduction Program per a search summary (D). |
| Voltus | CSP | 2 MW at Illinois Valley Community College (press release, D). Partner models are revenue share, fixed price or upfront, with no percentages published [D, WS11-S021]. |
| Constellation NewEnergy | ARES + channel programme | Supplies City Colleges [A, DI-S024]; channel-partner portal tracks commissions [B, DI-S028]. |
| E-Quantum Consulting LLC (Illinois) | Independent flat-fee consultant | Presented to BOMA. Shows supplier commission offers of $0.001–0.005/kWh and positions itself as one of three independent consultants in Illinois [D, DI-S026]. |
| MC Squared Energy Services | ARES | Holds most ComEd-territory municipal aggregation deals (CUB, via search summary; D). |
| 392 licensed ABCs | Brokers | 19 new and 10 withdrawn in the year to May 2026 [A, C7-S007]. The official list still returned HTTP 500 [DI-S031], so named Illinois broker sizes are MISSING. |
| Schooley Mitchell | Contingency franchise | "No savings, no charge" cost-reduction network [D, WS11-S047]. |

**Competitive reading:**
- CSPs sell direct to large and public sites.
- The broker field is crowded and largely telemarketing-driven (Stage C, E).
- The opening is mid-size private food and cold-storage accounts, where one analyst can combine supply, PLC and DR. Copyable, but rarely done by phone-room brokers.

## 3. Named suppliers and partners (`09_databases/suppliers/SYN-004_suppliers.csv`)

| Partner | Programme | Status |
|---|---|---|
| **ENGIE Resources** | Online inquiry, reply in 15 business days, then nine application documents; "easy and accurate commissioning" [B, DI-S027] | *Documented process.* Rates and acceptance of exempt-only brokers MISSING. |
| **Constellation** | Channel-partner portal for commission earnings and receivables [B, DI-S028] | *Documented existence.* Terms assumed. |
| **MC Squared, Calpine Energy Solutions** | ARES (Calpine is also a CSP) [A, DI-S021] | *Assumed* broker channels. |
| **CPower, Enel X, Voltus, NRG Curtailment, Enersponse, GridBeyond** | PJM CSPs active in Illinois [A, DI-S021] | *Documented* as CSPs. Channel-partner share is **MISSING** for all of them. |
| **Illinois Commerce Commission** | ABC licence once below-1,500 kW customers are served | *Documented:* no fee, $5,000 bond, 1 year management plus 1 year electric-industry experience of named persons, 90–180 days, annual report by March 31 [A, WS11-S023, C7-S001, C7-S004, DI-S020]. |

**Commission evidence:**
- **Supplier mils (D):** offers of $0.005, $0.003, $0.002 and $0.001/kWh, the last two paired with $12k–18k upfront [DI-S026]. Trade sites say mils shrink with account size [C7-S008, C7-S009].
- **Model assumption (E):** 1.25–1.75 mils on 2–5 GWh accounts.
- **CSP economics (A):** the CSP keeps 25–30% of capacity revenue [DI-S023]. A channel partner's share must come out of that.
- **Partner share (E, MISSING):** modelled at 8% of gross.

## 4. Named prospective customers

`09_databases/prospects/SYN-004_prospects.csv` lists **28 Illinois organizations**, all marked "prospect — not contacted":
- **Grocers:** Pete's Fresh Market and Shop & Save Market [A, DI-S003].
- **Cold storage:** Scout Cold Storage Chicago, Ashland Cold Storage, Frozen Assets Cold Storage, Produce Terminal Cold Storage, Interstate Warehousing (Joliet), ODW Logistics (Romeoville) [A, DI-S017].
- **Food plants:** Gonnella Baking, Turano Baking, Highland Baking, Carl Buddig, Ed Miniat, Land O'Frost, Stampede, Peer Foods, Vienna Beef, World's Finest Chocolate, Newly Weds Foods, Kronos Foods, Oberweis Dairy, Bridgford (Chicago plants), Vegetable Juices Inc, Lawrence Foods [A, DI-S018].
- **Hospitals with generators:** Saint Anthony (7.0 GWh), Humboldt Park Health (10.2 GWh), Thorek (4.9 GWh) [A, DI-S003].
- **Data centre:** one small Loop facility.

The ECHO registry contains historic records, so current operation, load size and existing contract dates must be verified. These are prospects, not leads.

## 5. Representative transactions

| # | Transaction | Annual revenue | Direct costs | Contribution | Evidence / payment timing |
|---|---|---|---|---|---|
| T1 | Independent grocer, 3 stores × 2.9 GWh, 24-month fixed supply (exempt: aggregate >1,500 kW) | $13,050 (8.7 GWh × $0.0015) | Data/CRM $300 | **$12,750** | Volumes A [DI-S003]; mils D/E. Residuals monthly in arrears for the term. |
| T2 | Cold storage, 0.8 MW peak, 5 GWh: supply + DR (0.5 MW) + PLC management | $13,700 (supply $6,250; DR partner share 0.5 MW × $325 × 365 × 0.75 accreditation × 8% = $3,560; PLC fee 15% of ~$26k tag savings = $3,890) | Assessment, DR test support, travel $900 | **$12,800** | Price A [DI-S022]; customer split A [DI-S023]; partner share, accreditation factor and PLC fee E. DR cash arrives after the delivery season. The site is below 1,500 kW, so supply needs a licence or a licensed partner. |
| T3 | Manufacturer, 1.2 GWh (~250 kW), via a licensed partner ABC | $3,000 (2.5 mils) | 50% split $1,500; data $100 | **$1,400** | D/E. |
| T4 | One-time contingency bill audit (rate-class/ratchet error) | $2,800 (35% of $8,000 refund) | Filing/data $150 | **$2,650** | E. Hit rates MISSING; paid 3–9 months later. |

**PLC value check:** E-Quantum's example of a 315 kW tag cut worth $26,941/yr at 2020–23 prices [D, DI-S026] scales to roughly $45k at $325/MW-day (E). The capacity tag is often the largest controllable line on a C&I bill.

## 6. Customer acquisition

**Customer #1:**
- **Who:** a multi-store grocer or cold-storage operator above 1,500 kW (exempt).
- **Offer:** a free capacity-tag analysis that shows dollars at the $325/MW-day cap and a post-2029 scenario at COMED's uncapped $776.69 [A, DI-S022].
- **Steps:** a letter of authorisation for utility data, a bill and interval audit, then an RFP to 4–6 ARES suppliers.
- **Timing:** the pitch is time-sensitive. DR enrollment works best in Sept–Dec [D, DI-S026], and the 2027/28 delivery year starts June 2027.

**Customers #2–10:**
- referrals from refrigeration contractors and CPAs;
- food-industry associations: the Midwest Food Products Association member directory [D, DI-S032];
- renewal-timed outreach using contract-expiry dates gathered in audits.

**Customers #11–100:**
- one commissioned rep from month 18;
- a licensed ABC (own licence once a qualifying person is named) to open the 100–1,500 kW segment.

**Funnel (all E):**

| Stage | Base | Conservative–optimistic |
|---|---|---|
| Qualified conversations per month with data access | 22 | 15–30 |
| → proposal | 40% | |
| → win | 25% | 18–32% |
| New accounts per month from the founder | ~2.2 | |
| Referral accounts | +0.8 per 100 active per month | |
| Rep, once productive | +1.5 per month | |

**Unit metrics (E):**
- **Cash CAC ≈ $280.**
- **Gross margin per account** about $3.9k/yr at $410/month ARPC.
- **LTV** about $25k at 1.3% monthly churn.
- **Payback** under 1 month of margin, but cash lags about 60 days.

**Founder time:** 30–35 hours of selling and analysis a week in year 1; by year 2, renewals and DR events add about 8 hours.

## 7. Pricing strategy and market evidence

**Market evidence:**
- **Supplier-paid adders** are standard. Examples run $0.001–$0.005/kWh, sometimes with $12k–18k upfront [D, DI-S026; C7-S008].
- **Disclosure rule.** Licensed ABCs must give signed written disclosure of total price including their fee [A, C7-S005].
- **Customer DR share:** 70–75% [A, DI-S023].

**Strategy:**
- **Mils:** 1.0–2.0 mils on exempt accounts. Disclose the fee in writing on every deal, even where the rule does not apply, to neutralise the "hidden commission" objection [DI-S026].
- **PLC management:** 15–25% of verified tag savings, or a flat monthly fee.
- **DR:** the customer keeps 70–75%. The founder negotiates the partner share from the CSP's 25–30%, never from the customer's share.
- **Audits:** a 30–40% contingency on refunds. This is a door-opener, not a profit centre.
- **No price growth is modelled.** Mils are fixed per contract, and capacity value after May 2029 could fall to the $175 floor or rise.

## 8. Working capital and cash conversion

Drivers: DSO 60 days (residuals paid monthly in arrears after the customer pays; DR settled annually), DPO 20 days, no inventory.

| Accounts | Monthly revenue | Net working capital | Cash conversion |
|---|---|---|---|
| 10 | ~$4.1k | ≈ $8k | ~55–60 days |
| 50 | ~$20.5k | ≈ $39k | ~55–60 days |
| 200 | ~$82k | ≈ $155k | ~55–60 days, longer for the DR share (season-end) |

- **Base peak funding is ~$30k**, mostly the ramp and receivables.
- **Clawback reserve.** Hold back about 5% of residuals against supplier clawbacks on customer default (terms MISSING).

## 9. Regulatory path

| Phase | Step |
|---|---|
| **Phase 0 (month 0–2)** | Form an Illinois LLC. A Secretary of State registration is required before any ABC application [A, WS11-S023]. Bind E&O/GL insurance ($2–5k/yr, E). Sign CSP partner and ARES broker agreements. |
| **Exempt operation (from month 1)** | Serve only customers with >1,500 kW aggregate Illinois billing demand (454.30(b)(5)), and keep the 12-month billed-demand evidence on file. Optionally act as the **exclusive agent of a single RES** with disclosed exclusivity (454.30(b)(3)) [A, C7-S003]. DR referral, PLC services and audits: no ICC licence identified. |
| **Own ABC licence (target month 10–16)** | Application via e-docket with: <ul><li>no fee;</li><li>a $5,000 bond from a Treasury-listed surety [A, C7-S004];</li><li>1 year of management experience;</li><li>1 year of electric-industry experience of the persons used to satisfy the rule [A, C7-S001].</li></ul> Decision in 90 days, extendable to 180, and it cannot be expedited [A, WS11-S023]. Then annual recertification by March 31, listing each RES relationship and its type [A, DI-S020]. Avoid residential and small-commercial customers, which trigger Parts 412/453. |
| **Interpretation risk (requires ICC staff confirmation)** | (a) whether a year of exempt brokerage and DR work counts as "electric-industry experience"; (b) whether 1099 sub-agents need their own licence. "Attempts to sell" covers anyone "soliciting customers" [A, DI-S019], so assume yes. |
| **Gas** | No state gas-broker licence according to a compliance vendor [D, DI-S029]; confirm before selling gas. |

## 10. Operations workflow

1. **Lead list (automatable).** ECHO, benchmarking and association data.
2. **Outreach (human).**
3. **Letter of authorisation and data pull (semi-automated).**
4. **LLM-assisted bill parsing and PLC analysis (AI).** About $200/month modelled; durable at ordinary API prices.
5. **RFP package to ARES suppliers (templated).**
6. **Negotiation and contract (human).**
7. **Enrollment and supplier portal tracking (automatable).**
8. **PLC peak alerts in summer (automatable).**
9. **DR registration, test and event support with the CSP (human plus CSP tools).**
10. **Residual reconciliation monthly (automatable).**
11. **Renewal campaign 6–12 months before expiry (CRM-driven).**

**Stack:** CRM, e-signature, supplier portals, market-data tools and analytics; about $850/month total modelled (E).

## 11. Competitive position and defensibility

**What accumulates:**
- a residual book that renews;
- contract-expiry calendars;
- each site's interval-data history and DR performance baselines;
- vertical density: refrigeration contractors and food-plant managers refer within their industry.

**Why the moat stays moderate:**
- 392 licensees compete [A, C7-S007];
- switching at renewal is easy;
- CSPs sell direct;
- the capacity premium could fade after the collar.

The exempt segment is the most courted, so the wedge has to be the analytics plus DR depth that phone-room brokers lack.

## 12. Key risks and pre-mortem

| Loss level | How it fails | Early warning |
|---|---|---|
| **$5k** | ARES suppliers will not contract with an unlicensed, exempt-only broker, or CSPs offer under 5% of gross. Stops at validation. | Fewer than 2 supplier agreements in 60 days; no written CSP partner share. |
| **$25k** | Audits find savings, but most targets are locked into contracts expiring in 2028–29, so the residual book builds too slowly. Wins come in under 1 per month. | Under 20% of audited prospects have contracts expiring within 12 months; win rate under 15% after 20 proposals. |
| **$50k** | A rep is hired before the book supports one; a large supplier exits or claws back; capacity prices normalise after May 2029 and DR/PLC value halves. | Rep under 1 account per month after 4 months; active ComEd ARES count falls further (it was −14% year over year [A, C7-S007]); the 2029/30 auction results. |

**Conservative scenario:** the model loses money every year and needs ~$494k cumulatively if run unchecked. That is a mechanical artefact of not stopping, which is why the kill criteria below matter.

## 13. Validation plan

| # | Experiment | Cost | Success | Kill |
|---|---|---|---|---|
| V1 | Written broker terms from ENGIE, Constellation and one more ARES for exempt (>1,500 kW) customers (founder action) | $0 | ≥2 agreements available; ≥1.0 mil on 2–10 GWh accounts, paid on usage | No supplier contracts without an ABC licence |
| V2 | CSP partner terms from CPower, Voltus and Enersponse | $0 | Written partner share ≥8% of gross, or ≥$8k per MW-year | All under 5%, or partner-share disclosure forbidden |
| V3 | Free capacity-tag and bill audits for 10 exempt-size prospects from the CSV | ~$200 (travel, data) | ≥5 letters of authorisation; ≥3 RFP mandates in 60 days | Under 3 letters of authorisation after 30 pitches |
| V4 | ICC ORMD written answer on the experience interpretation and sub-agent licensing | $0 | Clear path to own licence in ≤12 months | Licence path needs a full-time hire costing over $60k/yr |
| V5 | First paid event: one signed supply contract generating residuals, or one audit refund | ~$300 | Supplier commission confirmation received | None after 120 days |

Total cash for validation is about $500.

## 14. Revised scores and verdict

| Criterion | Stage C | Stage D | Reason |
|---|---|---|---|
| fcf | 4 | **5** | Base year-3 ~$98k, year-5 ~$344k (conservative negative) |
| roic | 8 | 8 | ~$30k peak funding |
| access | 5 | 5 | Identifiable buyers and a free-audit door, but heavily solicited |
| scale | 5 | **6** | Residual book plus DR; other PJM and choice states later |
| resilience | 6 | 6 | Essential spend; capacity collar ends May 2029 |
| entry | 4 | 4 | Crowded; analytics/DR wedge copyable |
| delegation | 6 | 6 | Analysts and reps are standard roles |
| cash | 5 | 5 | 60-day residual lag; DR paid annually |
| feasibility | 6 | **7** | Exempt and exclusive-agent paths legal from day one [A] |
| ai | 6 | 6 | Bill parsing and PLC analytics cheap and durable |

**Composite and gates:**
- **Composite:** raw 5.80, evidence-adjusted **5.56** (evidence D).
- **Gates:** G2_LICENSE now PASS.
- **Model** (`08_financial_models/SYN-004_model.xlsx`):

  | | Conservative | Base | Optimistic |
  |---|---|---|---|
  | Year-3 operating profit | −$98k | **$98k** | $608k |
  | Peak funding | $494k (the model keeps running; a founder would stop at the kill criteria) | $30k | $13k |

  The optimistic case compounds top-decile funnel rates and is not a forecast.
- **Base milestones:** breakeven month 9; $10k operating profit per month by month 30.

**Verdict: FINALIST (conditional on V1–V2).** It is cheap, legal on day one and recurring, and the founder's analytical strengths fit it. The risks are real: a crowded field, capacity-price dependence and unknown partner shares.
