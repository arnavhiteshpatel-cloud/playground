# SYN-004 Playbook: Energy cost management for large Illinois C&I users (licence-exempt >1,500 kW segment)

Stage E · 2026-11-28 · Read-only research: nobody was contacted, no form was submitted, no account was created. Evidence tags are [level, source_id]. E-SYN004 sources are in `06_playbooks/sources_E_SYN-004.jsonl`; DI-, C7- and WS11- sources come from earlier stages. Model: `08_financial_models/SYN-004_model.xlsx` and `_results.json` (rebuilt today).

> **Verdict: conditional finalist, downgraded. Run the $0 supplier test before spending anything.** Revised composite: raw 5.08, evidence-adjusted **5.06** (evidence D). Stage D was 5.56.
>
> **The licence-free path is confirmed in the current rule text.** It is narrower than Stage D implied:
> - Part 454 does not apply to anyone who solicits, prepares offers for, or runs a procurement for a customer whose affiliated Illinois accounts sum to more than 1,500 kW of billed demand [A, E-SYN004-S001, S002].
> - The test is applied customer by customer. Soliciting supply business from a smaller customer is a licensable act.
>
> **Revenue per account is higher, and the number of accounts lower, than Stage D assumed.**
> - An exempt customer uses roughly 7–12 GWh a year (my estimate, E), not the 2.75 GWh Stage D used to set revenue per account.
> - Such customers get lower fees: 0.75–1.5 mils [D, DI-S026, E-SYN004-S011].
> - There are fewer of them, and they are heavily courted.
>
> **Base case (rebuilt model, $4k/month owner draw from month 13):**
> - Year-3 operating profit **$98,323**; year 5 **$120,332**.
> - Peak funding **$62,155** ($32,371 without the draw).
> - Never reaches $25k a month of operating profit within 60 months.
>
> **Conservative case:** year 3 **−$10,282**, year 5 **$4,011**. Peak funding **$265,578**, which is almost entirely the owner draw; without it, $75,724.
>
> **What has to happen first:** two or more suppliers must agree in writing to pay an unlicensed broker that serves only exempt customers, and exempt-size prospects must sign mandates.
>
> **Why it stays on the list:**
> - capacity prices are collared at $175–$338/MW-day through May 2030 [A, E-SYN004-S008, S009];
> - the business is asset-light;
> - validation costs under $500.

## What changed since Stage D (explicit corrections)

1. **Correction: the capacity collar runs a year longer.**
   - FERC approved the collar for the 2029/30 auction too (closing Dec 15, 2026) [A, E-SYN004-S008].
   - Cap $337.83 and floor $181.91/MW-day UCAP [A, E-SYN004-S009].
   - COMED cannot import enough capacity (CETL/CETO <1), and COMED's import limit (CETL) fell 68% [A, E-SYN004-S009].
   - So capacity value is bounded through **May 2030**, not May 2029.
2. **Correction: exempt accounts are larger, and revenue per account was mis-specified.**
   - 1,500 kW of aggregate billed demand at a ~0.55–0.65 load factor implies ≥7 GWh/yr (E).
   - Stage D's average revenue per account (ARPC) used 2.75 GWh, a small-account volume.
   - The rebuilt model uses 9 GWh × 1.0 mil in the base case, with fewer leads (10 a month, not 22) and slower reps (0.6 accounts a month, not 1.5).
3. **Correction: Stage D's cold-storage transaction (T2) double-counted.**
   - A site's nominated DR value is its PLC minus its firm service level [D, E-SYN004-S014].
   - Stage D's T2 charged a PLC fee and a DR share on the same kilowatts.
4. **Correction: the DR accreditation factor was too low.**
   - PJM's 2028/29 auction converted 7,713.7 MW ICAP of DR into 7,017.4 MW UCAP, a factor of ~0.91 [A, E-SYN004-S010].
   - Stage D used 0.75.
5. **Correction: three Stage D prospects are probably not exempt.**
   - Saint Anthony (7.0 GWh), Thorek (4.9 GWh) and the 3.4 GWh Loop data centre are likely below 1,500 kW [A volumes, E-SYN004-S015; E inference].
   - The prospect CSV is updated, and Sinai Chicago and St. Bernard Hospital are added.
6. **Correction: the conservative case's "$494k loss" was a modelling artefact.**
   - It came from calendar-fixed hires: a rep at month 18 and a compliance partner at month 10.
   - All hires are now gated on revenue or account count.
   - The conservative case is now a founder-only business that never takes off, which is the honest kill case.
7. **Correction: Stage D's "$30k base peak funding" excluded the owner draw.** With the standard $4k/month draw it is $62,155.
8. **Clarification: the fee-disclosure code of conduct (454.90) binds only "any person or entity required to be licensed"** [A, C7-S005].
   - Exempt deals are not bound by it.
   - ENGIE's broker agreement imposes disclosure contractually anyway [B, E-SYN004-S007].

---

## 1. Business explanation

**What it is.** Large commercial and industrial (C&I) electricity users in northern Illinois buy "supply" (energy plus capacity) from competitive suppliers (ARES), and pay ComEd separately for delivery.

- Above 1 MW, 93% of ComEd usage is already on competitive supply [A, E-SYN004-S016].
- Only ComEd customers under 100 kW can still buy fixed-price supply from the utility [A, E-SYN004-S016].

So every target customer must, every 12–36 months, choose a supplier and a product: fixed price, index, or blocks with capacity passed through.

**What the business sells.** One analyst-led relationship that cuts the customer's energy cost in four ways:

| Service | What the founder does | How it is paid | Share of base revenue |
|---|---|---|---|
| Supply procurement | RFP to 4–6 ARES, contract structuring, renewal timing | Supplier remits a disclosed fee per kWh (a "mil" = $0.001/kWh) monthly as the customer pays [B, E-SYN004-S007] | ~88% |
| Capacity-tag (PLC) management | Forecast PJM summer peak hours, alert the site, verify the next year's tag | 12–20% of verified savings or a seasonal fee (E) | ~7% |
| Demand-response (DR) origination | Assess curtailable load, run a CSP bid, support tests and events | Share of the CSP's margin, or a customer-paid advisory fee (E, MISSING) | ~5% |
| Bill audit | Tariff, rate-class and demand-ratchet errors | 30–35% contingency on refunds (E) | One-time |

**Why customers pay.** Capacity is now a CFO-visible line.
- PJM capacity cleared at the cap in COMED for 2026/27 through 2028/29, and is collared at up to $337.83/MW-day for 2029/30 [A, WS11-S020, DI-S022, E-SYN004-S009]. That is about $119–123 per kW-year of peak-load obligation.
- A 2 MW capacity tag therefore costs about $240k a year before utility scaling factors (E arithmetic).
- Supply prices in recent Illinois public approvals were roughly 5–8¢/kWh [D, E-SYN004-S021]. A 9 GWh customer therefore spends roughly $450–720k a year on supply.
- A 1-mil broker fee is $9k a year, about 1.3–2% of that spend. It is easy to justify if the RFP or capacity-tag work saves several times that.

**How it earns.** Each signed account produces a monthly residual for the contract term, plus occasional DR and PLC fees. The value is the book of residuals that renew.

**Why it is attractive (and why not).**
- **For:** almost no capital, recurring fees, analytical work that suits the founder, and a legal day-one path.
- **Against:** a saturated field (392 licensed brokers [A, C7-S007]), suppliers who can go around the broker [B, E-SYN004-S007], CSPs compressing their own margins [D, E-SYN004-S013, S014], and revenue that starts only when a customer's current contract expires.

## 2. Commercial entry

### 2.1 Licensing re-verification (critical)

**Sources read today:**
- the current rule text, 83 Ill. Adm. Code 454.20 and 454.30 (LII reproduction) [A, E-SYN004-S001, S002];
- an independent mirror showing 454.30 unchanged since 35 Ill. Reg. 17602, effective 2011-11-01 [C, E-SYN004-S003];
- the ICC ABC page and FAQ (rev. 2025-06-17) [A, E-SYN004-S005].

**The statute itself (220 ILCS 5/16-115C) could not be read.** ilga.gov returned HTTP 503 or TLS errors, and the mirrors are behind Cloudflare challenges [E-SYN004-S020]. Search snippets indicate that P.A. 96-1385 placed the same 1,500 kW carve-out in the statutory definition in 16-115C(b) [D, E-SYN004-S004]. This was **not verified verbatim**, and neither were any 2025–26 amendments.

**Rule summary:**
- **Who must hold a licence.** Part 454 covers each ABC that "sells or attempts to sell ... on behalf of a RES" or "procures or attempts to procure ... on behalf of a retail customer" [A, E-SYN004-S001].
- **What "attempts to sell" covers:** soliciting customers, making offers or preparing contracts.
- **What "attempts to procure" covers:** preparing solicitations, notifying bidders, or determining the results.
- **What is excluded:** both definitions exclude professional services "incidental" to the transaction, such as legal, accounting or engineering services [A, E-SYN004-S002].
- **The exemption (454.30(b)(5)).** The Part does not apply to anyone dealing with "a third party that has an aggregate billing demand of all of its affiliated electric service accounts in Illinois of greater than 1,500 kW".
- **How aggregate billing demand is measured:** "the total of the highest monthly billed demand of each of the retail customer's affiliated electric accounts during the past calendar year" [A, E-SYN004-S002]. "Affiliated" is not defined (MISSING).

**Exactly what is and is not allowed without a licence:**

| Activity | Without an ABC licence? | Basis |
|---|---|---|
| Solicit, quote, run an RFP, prepare and negotiate supply contracts for a customer whose affiliated Illinois accounts' peak billed demands sum to >1,500 kW (prior calendar year) | **Allowed** | 454.30(b)(5) [A, E-SYN004-S001] |
| Receive supplier-remitted fees on those exempt deals | Allowed (Part 454 does not regulate them; the supplier's contract does) | [A, E-SYN004-S001; B, E-SYN004-S007] |
| Sell for one supplier only, any customer size, with exclusivity disclosed | Allowed (but this gives up the multi-supplier RFP pitch) | 454.30(b)(3) [A] |
| Bill audit, PLC forecasting and alerts, DR assessment and CSP referral, energy-efficiency engineering, for any customer size | Allowed (not procurement or sale of retail electric supply) | 454.20 definitions [A, E-SYN004-S002]; DR registration is the CSP's [A, DI-S021] |
| Natural-gas brokerage | ABC licence does not cover gas [A, E-SYN004-S005]; no state gas-broker licence per a compliance vendor [D, DI-S029] | Confirm |
| Soliciting supply business from, quoting, or running an RFP for a customer at or below 1,500 kW aggregate | **Not allowed** (needs an ABC licence, a licensed partner who does the soliciting, or single-RES exclusivity) | 454.20 "attempts to sell" includes "soliciting customers" [A] |
| Mass "we'll cut your electricity rate" outreach to an unscreened list | **Risky:** each sub-1,500 kW recipient is arguably a solicitation | Same; interpretation (E) |
| A 1099 sub-agent soliciting non-exempt customers under the founder's firm | Not allowed without a licence (assume each "third-party individual" needs one) | 454.20 [A]; interpretation (E) |
| Calling the firm "independent" while holding supplier agreements | Barred for licensees [A, C7-S005]; for exempt deals, deceptive-practice law and supplier contracts still apply | Use "fee disclosed in writing" instead |

**What the founder must do in practice:**
- Screen every supply prospect for aggregate billed demand before any supply pitch.
- Keep a per-customer exemption file: 12 bills per account, the affiliate list, and the computed sum.
- Lead all general marketing with capacity-tag, DR and audit services, which are licence-free for any size.

**The licence itself, when needed:**
- no fee, a $5,000 bond, and a 90–180-day review [A, E-SYN004-S005, C7-S004];
- one year of managerial experience, and one year of electric-industry experience held by the persons named [A, C7-S001, C7-S002];
- an annual report due March 31, and a designated-agent report by January 31 [A, E-SYN004-S005].

### 2.2 Niche, customer, geography

**The niche:** privately owned refrigerated and food businesses in the ComEd zone (Cook, DuPage, Will and Kane counties) with >1,500 kW aggregate billed demand:
- independent multi-store grocers;
- multi-plant bakeries and meat processors;
- independent cold stores;
- independent hospitals with generators, as a secondary group.

**Why these customers:**
- Refrigeration load is large and somewhat shiftable, which supports PLC and DR (E).
- Owners or CFOs decide locally.
- Chains (Jewel-Osco, Mariano's, Costco, Walmart), REIT office towers and big hospital systems are excluded, because they buy centrally through large consultancies [A presence in E-SYN004-S015; E inference].

**Public bodies are excluded.** They buy DR and supply through state and city contracts [A, DI-S024, DI-S025].

### 2.3 Named suppliers and partners

Full list: `09_databases/suppliers/SYN-004_suppliers.csv`.

**Retail suppliers (ARES):**
- **ENGIE Resources** (application documented):
  - inquiry, a reply within 15 business days, then nine documents;
  - the request form asks for years of energy experience, the number of customers represented, **state licence copies**, a credit score and legal review of marketing [B, E-SYN004-S006].
  - Its remittance agreement pays monthly on the 25th, after the customer pays, with consumption true-ups. Fees stop if the customer agreement terminates [B, E-SYN004-S007].
- **Constellation:** a channel-partner portal [B, DI-S028].
- **NRG/Direct Energy Business**, **Calpine Energy Solutions** and **MC Squared:** ARES, some of which also act as CSPs [A, DI-S021]. Broker terms MISSING.

**Curtailment service providers (CSPs) for demand response:**
- **Listed by PJM as active in Illinois:** CPower (NRG), Voltus, Enel X, Enersponse, GridBeyond, Calpine [A, DI-S021].
- **Channel-partner shares:** MISSING for all of them.
- **Margins are shrinking:** the CSP's share of revenue is "usually 20–40%, negotiable" [C, E-SYN004-S012], and some providers now offer 100% revenue share with a fixed fee or a floor [D, E-SYN004-S013, S014].

**A licensed Illinois ABC as a partner** (for sub-1,500 kW deals at a ~50% split): split level MISSING (E).

### 2.4 Top 15 named prospects

Full list of 30: `09_databases/prospects/SYN-004_prospects.csv`. All are "prospect — not contacted". Exemption status must be verified from bills.

| # | Prospect | Why | Evidence |
|---|---|---|---|
| 1 | Pete's Fresh Market | Five Chicago stores at 2.53–3.25 GWh each (~14.6 GWh), plus suburban stores; clearly >1,500 kW aggregate | [A, E-SYN004-S015] |
| 2 | Shop & Save Market | Archer store 2.55 GWh; multi-store; likely exempt (store count to verify) | [A, E-SYN004-S015] |
| 3 | Humboldt Park Health | 10.18 GWh independent hospital; likely >1.5 MW; generator DR candidate | [A, E-SYN004-S015] |
| 4 | Sinai Chicago (Mount Sinai 16.81 + Holy Cross 8.69 GWh) | Clearly exempt; a system buyer, so incumbent risk is high | [A, E-SYN004-S015] |
| 5 | Gonnella Baking | Chicago, Aurora and Schaumburg (frozen) plants; aggregate likely exempt | [A, DI-S018] |
| 6 | Carl Buddig & Co. | Two IL plants, refrigeration-heavy | [A, DI-S018] |
| 7 | Land O'Frost (Lansing) | Large processor; may use a national consultant | [A, DI-S018] |
| 8 | Oberweis Dairy | Plant plus store network; aggregation pushes it over 1,500 kW (E) | [A, DI-S018] |
| 9 | Kronos Foods (Glendale Heights) | Refrigerated manufacturing and distribution | [A, DI-S018] |
| 10 | Scout Cold Storage Chicago | Cold store; recent refrigeration permit | [A, DI-S017] |
| 11 | Interstate Warehousing (Joliet) | Large cold store; parent may buy centrally | [A, DI-S017] |
| 12 | Stampede Culinary Partners (Bridgeview) | Refrigeration-heavy processor | [A, DI-S018] |
| 13 | Turano Baking (Berwyn) | Large bakery | [A, DI-S018] |
| 14 | Newly Weds Foods (Chicago) | Process load; multi-plant parent | [A, DI-S018] |
| 15 | St. Bernard Hospital | 7.02 GWh, borderline; DR/PLC first, supply only if bills prove >1,500 kW | [A, E-SYN004-S015] |

### 2.5 Competitors

**Direct sales and CSPs:**
- Supplier direct sales teams: ENGIE may contact the broker's customer directly [B, E-SYN004-S007].
- CSP direct teams: CPower, Enel X, Voltus, GridBeyond.
- Flat-fee DR models such as KilowattLogic [D, E-SYN004-S014].

**Brokers and consultants:**
- 392 licensed ABCs [A, C7-S007].
- Illinois institutional brokers named in board materials: Vanguard Energy Services and Nania Energy Advisors [D, E-SYN004-S021].
- Flat-fee consultant E-Quantum Consulting, which tells buyers to avoid commissions and call CSPs directly [D, DI-S026].
- Contingency networks such as Schooley Mitchell [D, WS11-S047].
- Large national consultancies (not researched, E).

### 2.6 Positioning and pricing

**Positioning:** "The capacity-cost specialist for refrigerated food businesses: one written, disclosed fee; every supplier bid shown; DR bid among CSPs; summer peak alerts included."

ENGIE's agreement already obliges brokers to disclose the fee and share all bids [B, E-SYN004-S007]. Disclosure is therefore a hygiene factor, not a moat. The wedge is **capacity analytics plus food-plant operational playbooks**, delivered by someone who shows up on site.

**Pricing (E unless noted):**

| Service | Price | Note |
|---|---|---|
| Supply | 0.75–1.25 mils on exempt accounts, disclosed in a signed agency agreement | Evidence for the band: offers of $0.001–0.005 [D, DI-S026]; an Illinois district's ~3-mil broker estimate [D, E-SYN004-S011]; a 0.75-mil municipal consultant fee [D, E-SYN004-S017] |
| PLC | 15% of verified tag savings, or $350/month for June–September | |
| DR | Either a disclosed CSP-paid partner share, or a customer-paid 10–20% of the *uplift* the founder negotiates above the customer's best direct CSP offer | Never take a fee out of the customer's share without disclosing it [D, DI-S026; D, E-SYN004-S018] |
| Audit | 30–35% of refunds | |

### 2.7 Sales and acquisition strategy

**The hook** (January–May 2027):
- The 2029/30 auction result (closes Dec 15, 2026) sets capacity for June 2029–May 2030 [A, E-SYN004-S008].
- Summer peaks set next year's capacity tags. Summer 2027 most likely sets the tag priced at the 2028/29 cap of $325 (E; confirm the ComEd PLC timing).

**The offer:** a free two-page "capacity-tag and contract-expiry review" from 12 months of bills plus an interval-data letter of authorisation (LOA).

**Channels:**
- direct outreach to owners and CFOs on the screened list;
- refrigeration contractors and CPAs;
- the Midwest Food Products Association directory [D, DI-S032];
- site visits.

**Qualification gates** before any supply discussion:
1. aggregate billed demand >1,500 kW;
2. a current contract expiring within 18 months, or capacity passed through on the bill;
3. a decision maker present.

## 3. Transaction economics

These match the model's UnitEconomics sheet. Amounts are per year.

**T1. Independent grocer: 5 stores, 14.6 GWh, exempt, 24-month fixed contract.**

| Line | Amount |
|---|---|
| Revenue (14.6 GWh × $0.0010) | **$14,600** |
| Partner split | $0 |
| Data/CRM | −$300 |
| True-up/withholding allowance (3%) | −$438 |
| **Contribution** | **$13,862** (95%) |

- **Cash timing:** first fee about 45–60 days after the first contract month, because the customer pays the supplier and the supplier remits on the 25th [B, E-SYN004-S007]. It then arrives monthly. If the contract was signed early, nothing flows until the old contract expires.
- **Failure risks:** ENGIE-type agreements pay nothing after a terminated agreement or on unpaid bills [B]. The supplier may approach the customer directly. A competing broker may claim the customer, and the supplier picks [B, E-SYN004-S007].
- **Repeat potential:** a renewal at month 18–22 if the relationship holds.

**T2. Cold store: 1.8 MW billed demand, 9 GWh, supply plus DR on 0.4 MW.**

| Line | Amount |
|---|---|
| Supply fee (9 GWh × 1.0 mil) | $9,000 |
| DR partner share (0.4 MW × 0.91 × $325 × 365 × 6%) | $2,590 |
| **Revenue** | **$11,590** |
| Assessment, test support, travel | −$900 |
| True-up allowance | −$270 |
| **Contribution** | **$10,420** |

- **Inputs:** price [A, E-SYN004-S008]; factor [A, E-SYN004-S010]; partner share [E, MISSING].
- **No PLC fee here.** The same kW cannot be sold twice [D, E-SYN004-S014].
- **DR cash** arrives once a year, typically mid-July after the delivery year [C, E-SYN004-S012].
- **Failure risks:** non-performance penalties under all-hours availability [A, WS11-S020], and the CSP changing partner terms.
- **Repeat:** each delivery year.

**T3. Manufacturer: 1.2 GWh, ~250 kW, not exempt, via a licensed partner ABC.**

| Line | Amount |
|---|---|
| Revenue (2.5 mils) | **$3,000** |
| 50% split | −$1,500 |
| Data | −$100 |
| **Contribution** | **$1,400** |

- **Legal constraint:** the founder may only refer this customer; the licensed partner must do the soliciting and quoting [A, E-SYN004-S002].
- Evidence D/E.

**T4. One-time contingency audit.**

| Line | Amount |
|---|---|
| Revenue (35% × $8,000 refund) | **$2,800** |
| Data and filing | −$150 |
| **Contribution** | **$2,650** |

- **Not shown:** about 20 hours of founder time.
- **Cash:** 3–9 months later.
- **Hit rate:** MISSING [E, WS11-010].

**T5 (licence-free, any size). DR-only for a 600 kW cold store curtailing 250 kW.**
- Gross capacity revenue: 0.25 × 0.91 × $325 × 365 = **$26,987**.
- At a 6% partner share, the founder earns about **$1,620 a year**.
- Alternatively, if the founder lifts the customer's share from 70% to 85% through a CSP bid, the uplift is about $4,050, and 25% of it is about **$1,010** (E).
- **Lesson:** DR alone is a door-opener, not a business.

**Unit view (base model):**
- ARPC $850/month; cash acquisition cost $350 plus $400/month fixed marketing.
- Monthly churn 1.2%, so expected life is about 83 months.
- Lifetime gross margin about $56k per account at 80% gross margin (E).
- **The binding constraint is not unit economics.** It is the rate of winning exempt mandates: 0.88 a month from the founder in the base case.

## 4. Validation

Experiments are ordered by information value per dollar. The founder executes all of them; nothing was sent by this research.

| # | Test | Cost | Success | Failure / pivot |
|---|---|---|---|---|
| V1 | **Supplier acceptance and terms.** Three ARES: ENGIE broker inquiry, Constellation channel team, plus NRG/Direct or Calpine. Ask whether they will contract with an Illinois broker that serves only 454.30(b)(5)-exempt customers and holds no ABC licence. Also ask the mils range on 5–15 GWh fixed deals, payment timing, true-up and termination terms, and whether a new firm with no customers is accepted | $0; 3–4 weeks (ENGIE replies within 15 business days [B, DI-S027]) | ≥2 written yes; ≥0.75 mil on exempt accounts; paid on usage | No supplier accepts: pivot to sub-agent under a licensed ABC (get the split in writing) or single-RES exclusivity, or drop the supply leg |
| V2 | **CSP terms.** CPower, Voltus, Enersponse, GridBeyond, Enel X: channel-partner share or per-MW fee; minimum kW; penalty pass-through; whether they accept a customer-paid advisor | $0 | Written partner share ≥5% of gross, or ≥$5k/MW-year | All under 3%, or none pays partners: run DR as a customer-paid bid service, or as a free retention feature |
| V3 | **Demand: 25 exempt-size conversations from the screened list** | ~$200 travel/data | ≥8 LOAs or 12-month bill sets; ≥40% with expiry ≤18 months; ≥3 RFP mandates in 60 days | <4 LOAs after 25, or <20% with near expiries: stop or defer to the 2028 renewal wave |
| V4 | **Regulatory confirmation.** Written question to ICC ORMD (contact on the ICC ABC page) on (a) the meaning of "affiliated", (b) marketing to mixed-size lists, (c) whether a year of exempt brokerage or DR counts as electric-industry experience under 454.70. Then one hour with Illinois utility-regulatory counsel to read 16-115C verbatim | $0 + $500–2,500 (counsel only after V1 and V3 pass) | Written answers consistent with this playbook | The exemption is narrower than the rule text, or the statute differs: stop the supply leg until licensed |
| V5 | **First paid event:** one signed agency agreement plus a supplier confirmation letter showing the fee, or one audit refund | ~$300 | A confirmation letter with the fee in mils | None within 120 days of V1 success: abandon |

**Minimum viable offering:** the free capacity-tag and contract-expiry review, plus one RFP run in a spreadsheet with emailed supplier quotes. No software build.

**Interview plan:** 25 conversations, using the questionnaire in `SYN-004_materials.md`, focused on past behaviour:
- who bought the last contract, how, and through whom;
- the fee paid, if known;
- the expiry date;
- whether the site has ever done DR;
- what it was paid.

**Validation budget:** ≤$500 cash before counsel.

**Testable assumptions** (model base values):
- mils ≥1.0 on 9 GWh;
- 10 qualified conversations a month;
- 40% proposals, 22% wins;
- partner share 6%;
- churn 1.2% a month.

**Invest more** (move to the $2–5k step) only when V1 and V3 pass and at least one mandate is signed.

**Abandon or pivot** when V1 fails and no licensed partner offers ≥50%, or when V3 shows <20% near-term expiries. The pivot options are licence-free PLC/DR/audit, or another Atlas finalist.

## 5. Operations

### 5.1 Lead-to-cash workflow

| Step | Function | Class |
|---|---|---|
| 1 | Build the target list: benchmarking, EPA ECHO, association directories; estimate aggregate kW | AI-assisted / automatable |
| 2 | Exemption pre-screen (estimate, then verify from bills before any supply pitch) | Human decision, AI-assisted |
| 3 | Outreach (letter, call, visit) leading with the capacity-tag review | Human |
| 4 | LOA and data pull (bills, ComEd interval data) | Human plus automatable |
| 5 | Bill parsing, PLC and peak analysis, contract-expiry calendar | AI-assisted (LLM extraction, Python) |
| 6 | Proposal and agency agreement with disclosed fee | Human; template reviewed by a lawyer (professional-dependent) |
| 7 | RFP package to 4–6 ARES; compare bids on identical usage | Templated / automatable |
| 8 | Negotiation and contract signature | Human |
| 9 | Supplier enrollment, confirmation letter (fee), CRM record | Automatable |
| 10 | Monthly remittance reconciliation against expected kWh × mils; chase withheld fees | Automatable plus human exceptions |
| 11 | Summer PLC alerts (June–Sept) and post-season verification | Automatable plus human calls |
| 12 | DR: CSP bid, registration, tests and events, July settlement check | Human plus CSP tools |
| 13 | Renewal campaign 9–12 months before expiry | CRM-driven |
| 14 | Insurance, tax, licence filings (if licensed) | Professional-dependent |
| — | Relationship, trust, on-site walkthrough of refrigeration operations | Not automatable |

### 5.2 Support, QA and exceptions

**QA rules:**
- Every bid comparison uses one usage estimate, which is the rule for licensees [A, C7-S005] and adopted here voluntarily.
- A second person checks the exemption computation and each fee confirmation.
- Remittances are reconciled monthly against expected volume.

**Exceptions:**
- **Supplier withholds a fee because the customer has not paid** [B, E-SYN004-S007]: chase and document.
- **Competing broker claim:** produce the dated agency agreement.
- **DR non-performance:** a post-event review with the site.
- **A customer drops below 1,500 kW**, for example after a store closure: stop supply solicitation until licensed.

### 5.3 Software stack (list prices, E; verify)

| Item | Cost |
|---|---|
| Google Workspace | ~$8/user/mo |
| CRM (HubSpot Starter or Pipedrive) | ~$15–30/seat/mo |
| E-signature | ~$15–25/mo |
| QuickBooks Online | ~$35–65/mo |
| Supplier portals (ENGIE OneHub, Constellation) | Free [B, E-SYN004-S006; DI-S028] |
| PJM and ComEd public data, NOAA weather | Free |
| Peak-alert SMS | Cents per message |

The model carries $150/month for CRM and portals, $200 for analytics and LLM, $200 for market data (placeholder, MISSING), $500 for travel, $300 for accounting and admin, and $250 for insurance. Total overhead is $1,600/month in base.

### 5.4 Legal and administrative requirements

**Entity and insurance:**
- Illinois LLC, EIN and bank account.
- E&O/professional liability, general liability and cyber cover. Quotes MISSING; the model carries $250–400/month.

**Exemption file per customer:** 12 bills per account, the affiliate list, and the computed aggregate demand.

**Contracts:**
- written agency agreement with the customer, with the fee disclosed;
- ComEd interval-data LOA;
- supplier broker agreements, which are under Texas law in ENGIE's case [B, E-SYN004-S007];
- CSP partner agreement;
- mutual NDA.

**Records:** keep authorisations and marketing materials for three years. This mirrors the duty on licensees under 454.90 and 454.100 [A, C7-S005].

**Later licence:** a $5,000 bond and the annual and designated-agent filings [A, E-SYN004-S005].

**Accounts:** a CPA for pass-through tax. The model uses a simplified 30% rate.

### 5.5 Post-December-2026 AI cost and fallback

**Cost.** Bill extraction is the only recurring LLM use. 300 bills a month at ~10k input and ~1k output tokens each comes to about 3M input and 0.3M output tokens:
- Claude Haiku 5.5 ($0.10/$0.50 per million tokens): **under $1/month**;
- Claude Sonnet 5.5 ($2/$10): **about $9/month**.

The model's $200/month AI line is generous, and the "AI cost ×3" stress test moves year-3 profit only from $98,323 to $93,230.

**Fallback:** rule-based PDF parsers and supplier or utility data downloads. AI saves analyst hours; it is not a dependency.

## 6. Growth

**First 10 customers** (months 8–20 in the base case):
- **Who:** exempt independents from §2.4. Grocers and multi-plant food firms first, because their aggregation makes exemption easy to prove.
- **How:** the free review and site walkthroughs.
- **Expect:** 0.9 wins a month from the founder alone (model base).

**First 100 customers.** Not reached within 5 years in the base case (45.6 active accounts at the end of year 5). Reaching 100 needs three things:
1. an ABC licence, to open the 400 kW–1.5 MW segment, which is 87% switched and more numerous [A, C7-S007];
2. two productive reps;
3. referral density in food and cold-chain circles.

**Hiring sequence** (each hire is triggered in the model by a milestone, not by the calendar):

| Hire | Milestone | Cost | Productivity / role |
|---|---|---|---|
| Licence-qualifying compliance partner (part-time) | Revenue ≥$8k/month (model: month 21) | $1,500/month base | Named under 454.70; opens sub-1,500 kW deals |
| Commissioned rep | Revenue ≥$25k/month (month 45) | $6,500/month base | 0.6 large accounts/month after a 6-month ramp. Pays back in ~2 years, which causes the year-5 profit dip |
| Energy analyst | 35 active accounts (month 54) | $6,000/month base | Covers ~50 accounts |
| Second rep | Revenue ≥$75k/month | Same as first | Not reached in base |

**Capacity limits:**
- the founder can carry about 35 large accounts while still selling;
- a rep adds about 7 accounts a year;
- DR/PLC summer workload peaks in June–September.

**Geographic expansion:**
- **Ameren territory:** MISO, different DR mechanics, same ABC rules.
- **Other PJM retail-choice states (PA, OH, MD, NJ):** each has its own broker licensing (not researched, E). This is a new-licence project per state, not a quick win.

**Adjacent services:**
- natural-gas brokerage [D, DI-S029];
- ComEd Voluntary Load Reduction, paying ≥$0.25/kWh per event [D, E-SYN004-S019];
- solar and storage referrals, including Illinois Shines [B, WS11-S045];
- battery dispatch.

**Vertical integration: becoming one's own CSP.**
- **Gain:** at 5 MW enrolled, gross capacity revenue is about $540k a year. Holding the CSP's 25% margin instead of a 6% partner share adds about $100k a year gross (E).
- **Cost:** PJM membership, credit, settlement and training (MISSING).
- **When:** only above ~10 MW, and only if prices hold after May 2030.

Becoming an ARES (a licensed supplier) is not recommended: it carries credit and collateral risk.

**Delegation.** A manager can run day-to-day work once the analyst and rep are in place (year 5+).
- The book is not freely transferable: ENGIE's agreement bars the broker from assigning it without consent [B, E-SYN004-S007].
- That limits exit value and is why the base valuation multiple is 2.5×.

**Reinvestment slots:**
- the rep ramp, about $39k;
- receivables, about 2 months of revenue;
- the licence;
- later, the own-CSP option.

## 7. Financial analysis (rebuilt model)

All figures are quoted from `08_financial_models/SYN-004_results.json`. Operating profit is EBITDA-basis, before owner pay. A standard $4,000/month draw runs from month 13; tax 30%; start capital $63,000, the smallest injection that keeps base cash ≥0 (minimum base cash balance $845). Verification against the workbook is done centrally.

### 7.1 Launch and working capital

- **Pre-revenue cash need** (base, months 1–7): about $14k of operating loss plus $5.5k of one-time capex (laptop, data logger, counsel review).
- **First revenue:** month 8.
- **Working capital:** receivables at 60 days of sales outstanding (DSO) on remittances and annual DR. Net working capital grows $16,488 in year 2 and $23,288 in year 5.
- **Peak funding** (maximum cumulative cash deficit including the draw): conservative **$265,578**, base **$62,155**, optimistic **$20,781**.
- **Without the draw:** $75,724 / $32,371 / $20,781.

### 7.2 Five-year annual view

| Scenario | Year | Revenue | Op. profit | FCF | Active accounts (end) |
|---|---|---|---|---|---|
| Conservative | 1 | $155 | −$25,783 | −$33,042 | 0.2 |
| | 3 | $30,621 | −$10,282 | −$13,453 | 7.2 |
| | 5 | $56,114 | $4,011 | $2,146 | 12.3 |
| **Base** | 1 | $5,680 | −$20,281 | −$30,103 | 2.2 |
| | 2 | $85,980 | $32,549 | $16,061 | 12.4 |
| | 3 | $188,209 | **$98,323** | $78,390 | 22.2 |
| | 4 | $285,637 | $151,456 | $105,594 | 31.5 |
| | 5 | $404,540 | **$120,332** | $75,344 | 45.6 |
| Optimistic | 3 | $654,765 | $411,459 | $246,968 | 47.9 |
| | 5 | $1,917,813 | $1,221,322 | $770,831 | 123.5 |

The optimistic case stacks top-decile funnel rates, 1.25 mils and 0.8% churn. It is not a plan.

### 7.3 Twenty-four-month base view

Monthly, from the model's M_Base sheet.

| Months | New accounts/mo | Active (end) | Revenue (end month) | Op. profit (end month) | Cash (end) |
|---|---|---|---|---|---|
| 1–7 | 0 | 0 | $0 | −$2,000/mo | $43,500 |
| 8 | 0.15 | 0.1 | $213 | −$1,881 | $41,219 |
| 12 | 0.75 | 2.2 | $2,307 | −$439 | $32,897 |
| 13 (draw starts) | 0.90 | 3.1 | $3,139 | $108 | $27,450 |
| 18 | 0.93 | 7.4 | $6,818 | $2,952 | $9,706 |
| 21 (compliance partner) | 0.95 | 9.9 | $8,991 | $3,095 | $4,341 |
| 24 | 0.97 | 12.4 | $11,137 | $4,763 | $958 |

**Milestones:**
- operating breakeven at month 13;
- ≥$1k/month at month 15, ≥$5k at month 25, ≥$10k at month 34;
- ≥$25k/month never within 60 months;
- payback (cumulative cash after draws recovers) at month 43.

**Conservative:** breakeven month 46, never ≥$1k/month, no payback. **Optimistic:** breakeven month 8, ≥$10k at month 15, ≥$25k at month 27.

### 7.4 Sensitivity (±25% on each driver, base year-3 operating profit)

| Driver | Year-3 op. profit range |
|---|---|
| Gross margin | $62,143 – $134,502 |
| Founder leads (and identically, win rate) | $62,597 – $134,048 |
| ARPC | $63,047 – $133,598 |
| Overhead | $93,788 – $102,857 |
| Labour | $93,548 – $103,097 |
| Churn | $94,077 – $102,744 |

The business is a function of **mandate win rate × fee per account × the share kept after splits**.

### 7.5 Stress tests (base)

| Stress | Year-3 op. profit | Peak funding |
|---|---|---|
| Win rate −40% | $47,526 | $84,771 |
| Founder capacity −40% | $47,526 | $84,771 |
| Sales cycle doubles | $72,269 | $86,835 |
| Key supplier refuses (3-month delay, −5 pts margin) | $70,666 | $85,608 |
| Recession (new accounts −30%, churn ×1.5) | $50,558 | $79,265 |
| Growth takes twice as long | $33,959 | $116,945 (no payback in 60 months) |
| Gross margin −10 pts | $79,502 | $72,767 |
| Overhead +50% | $89,253 | $80,360 |
| Customers pay 30 days later | $98,323 | $74,267 |

Some stresses raise year-5 profit (win rate −40% gives $127,309 in year 5), because hires are triggered later. That is an artefact of milestone-gated hiring, not a benefit.

### 7.6 Capital accumulation to year 10 (base)

**Year 10:**
- operating profit $144,338;
- cumulative deployable surplus $314,966 (after taxes, reinvestment, reserves and the draw);
- cumulative owner pay $454,484;
- enterprise value $360,846 at 2.5× [C/D anchors: C5-S021, DF-S004];
- owner-wealth proxy $1,130,296.

**Conservative:** deployable $0, enterprise value $6,016. **Optimistic:** deployable $5,857,281.

**Long-term drivers:**
- **Growth after year 5:** 5% in year 6, decaying 0.85 a year (0% in conservative). The Illinois ARES non-residential market is flat to −1.5% [A, E-SYN004-S016], so growth has to come from share gains.
- **Return on reinvested capital:** 1.0×.
- **Reserve:** 2 months (3 in conservative), because fees can stop on termination [B, E-SYN004-S007].

### 7.7 Downside cases

- **Conservative (the realistic failure):** 6 conversations a month, 15% wins, 0.75 mil on 7 GWh, 2% churn. The business earns nothing meaningful for 4 years, and the draw consumes $48,000 a year.
- **Supplier refusal or capacity-price collapse after May 2030.** The capacity price affects DR/PLC (12% of base ARPC) and the urgency of the pitch more than supply fees.
- **Fee compression to 0.5 mil on renewals** (E): roughly halves the base case.

## 8. Capital deployment ladder

| Step | What it buys | Evidence gate before spending | How it could be lost |
|---|---|---|---|
| $0–500 | V1/V2/V4 enquiries; screened list; review template; 25 conversations (fuel, parking) | None | Time only |
| $500–2k | LLC, domain/website, CRM, first association event or dues | V1: ≥1 written supplier yes; V3: ≥4 LOAs | Suppliers later decline onboarding (credit score, no track record [B, E-SYN004-S006]) |
| $2–5k | E&O/GL binder, counsel review of exemption and agency agreement ($2.5k in model), kW data logger | ≥2 supplier agreements in hand; ≥1 RFP mandate | Mandate lost to the incumbent broker; counsel finds a narrower exemption |
| $5–10k | 4–6 months of tools, insurance and travel until the first remittance | First supplier confirmation letter showing the fee | Contract starts late; customer defaults and the fee is withheld [B] |
| $10–25k | Runway to month 12 (base cash falls from $63,000 to $32,897 by month 12) | ≥3 signed accounts; ≥8 qualified conversations/month sustained | Win rate stays below 15% |
| $25–50k | Owner-draw bridge, months 13–24 (base cash reaches $958 at month 24) | Monthly revenue ≥$5k by month 16; on track to model | Draw outlasts growth (the conservative path) |
| $50–100k | ABC licence plus compliance partner; first rep, only at ≥$25k/month revenue | Revenue gate met; rep plan commission-heavy | A rep below 0.4 accounts/month costs ~$78k a year and adds under ~$41k of annual fees |

**Do not deploy above ~$63k without the base-case milestones being hit.** The conservative case shows that money spent here mostly funds the owner's living costs.

## 9. Strategic wealth creation

**Durable asset if it works:** a book of large-account residuals, interval-data histories, contract-expiry calendars and DR baselines. The supply market will exist (essential spend), but the asset is:
- terminable account by account;
- dependent on suppliers, and assignable only with consent [B, E-SYN004-S007];
- sensitive to capacity-market rules after May 2030.

**Capital it could generate:**
- **Base:** about $315k of deployable surplus over 10 years, on top of $454k of owner pay, with operating profit plateauing around $120–150k a year.
- **Higher outcomes:** need a licence, reps and density. The optimistic case shows the shape, but not with evidence.

**Management takeover:** plausible in year 5+ with an analyst, a rep and a manager. The founder keeps the supplier and CSP relationships.

**Can it fund other ventures?** Modestly, in base: about $40–55k a year deployable in years 6–10.

**Is it a strong first company for a holding company? Not in base case.**
- **For:** cheap to test, legal from day one, and suited to the founder's analytical strengths.
- **Against:** the base outcome is a ~$120–150k-a-year book, reached through a crowded, broker-hostile, supplier-controlled channel.

It deserves its $500 validation. It should win the founder's full-time commitment only if V1 and V3 come back clearly positive.

## 10. Execution plan

### First 7 days
- **Founder:**
  - Submit the ENGIE broker inquiry form.
  - Contact Constellation's channel team and NRG/Direct Energy Business. Ask the V1 questions (`SYN-004_materials.md` §1).
  - Email CPower, Voltus and Enersponse partner teams with the V2 questions.
  - Send the ICC ORMD question (V4).
  - Shortlist 40 exempt-likely prospects.
- **Claude prepares (before Dec 5):**
  - the screened list with estimated kW;
  - review and RFP spreadsheet templates;
  - a bill-parsing script;
  - the drafted messages.
- **Spend:** $0.
- **Evidence required:** acknowledgements; ENGIE's 15-day clock running.

### First 30 days
- **Founder:**
  - Hold 10–15 discovery conversations (questionnaire, materials §2).
  - Collect ≥4 LOAs or bill sets; build each prospect's aggregate-kW file.
- **Organisations to approach:**
  - Pete's Fresh Market, Gonnella, Carl Buddig, Oberweis, Kronos, Scout Cold Storage, Humboldt Park Health;
  - refrigeration contractors and CPAs serving them;
  - Midwest Food Products Association.
- **Questions:** who bought the last contract and how; expiry; fee paid; DR history; capacity line on the bill.
- **Spend:** ≤$300.
- **Accept a first order only when:** the customer's exemption is documented, a supplier agreement is signed, and the fee is in a signed agency agreement.
- **Abandon when:** no supplier will onboard an exempt-only broker and no licensed ABC partner offers a ≥50% split, or fewer than 2 of 15 conversations yield data.

### First 90 days
- 25 conversations; ≥3 RFP mandates; ≥2 supplier agreements; one CSP agreement.
- Form the LLC; bind E&O; hold the counsel review after the gates pass.
- First RFP run. The first contract may start later, at the customer's expiry.
- Summer-2027 PLC alert pilot offered free to 3 sites.
- **Milestone:** first supplier confirmation letter showing the fee.

### First year
- Base model: about 2.2 active accounts by month 12, roughly $2.3k/month revenue, and operating breakeven at month 13.
- Run the first PLC season (June–September 2027) and the first DR enrolment.
- **Slow-growth branch:** fewer than 3 accounts by month 12, but mandates pending into 2028 expiries. Keep it part-time and do not draw.
- **Failure branch:** fewer than 1 win per 8 proposals, or suppliers withhold or claw back fees. Stop.

## 11. Pre-mortem

| Failure | How it happens | Early warning | Cheap preventive test |
|---|---|---|---|
| Lost $5k | Suppliers refuse an unlicensed exempt-only broker (ENGIE asks for licence copies and a track record [B, E-SYN004-S006]) | No written yes within 45 days | V1 before forming anything |
| Lost $25k | Prospects engage but are locked into 2028–29 expiries; revenue starts a year late; draw burns cash | <20% of reviews show expiry ≤18 months | V3 expiry statistic |
| Lost $50k | Rep hired ahead of revenue; a supplier exits; post-2030 capacity drops toward the floor | Rep <0.4 accounts/month after 6 months; 2029/30 results; ComEd active ARES count (−14% y/y [A, C7-S007]) | Commission-heavy rep plan; revenue-gated hiring (model) |
| Revenue but no profit | Fees too thin (0.5 mil) or splits with a licensed partner eat 50% | Average confirmed mils <0.75 | Price floor in the agency agreement; walk away from sub-0.75 deals |
| Exhausting low-paid job | Founder runs RFPs, alerts and DR events for 15 accounts at $4k/month | Hours >55/week with revenue <$8k/month at month 18 | Kill criterion at month 18 |
| Cash crunch | Fee withheld on customer non-payment; DR paid once a year | Remittance gaps >30 days | Monthly reconciliation; 2-month reserve |
| Can't run without the founder | Relationships and analysis sit only in the founder's head | No analyst by 35 accounts | Documented playbooks; CRM discipline |
| No deployable surplus | Plateau at ~$120–150k op while paying the owner | Year-4 op <$100k | Decide licence-plus-reps expansion or harvest |
| Regulatory | Soliciting a sub-1,500 kW customer; statute narrower than the rule | Any supply pitch without an exemption file | Pre-screen rule; V4 counsel read of 16-115C |

## 12. Required confirmations

**Regulatory:**
1. Verbatim 220 ILCS 5/16-115C(b), and any 2025–26 amendment.
2. That 454.30(b)(5) is current in the official JCAR text.
3. ICC ORMD's reading of "affiliated", of mixed-list marketing, and of whether exempt-only experience counts under 454.70.
4. Whether 1099 sub-agents need their own licence.
5. That Illinois has no gas-broker licence (220 ILCS 5/19).
6. The ComEd PLC (capacity tag) methodology and timing for 2028/29 and 2029/30, and the over-billing refund limit (9-252).

**Suppliers:**
7. Written acceptance of an exempt-only unlicensed broker by ≥2 ARES.
8. Mils on 5–15 GWh deals.
9. Payment timing, true-up, termination and clawback terms.
10. Credit-score requirements.

**CSPs:**
11. Partner share or per-MW fee.
12. Penalty pass-through and enrolment cut-offs for the 2027/28 and 2028/29 delivery years.
13. The PLC-minus-FSL rule in PJM Manual 18.

**Customers:**
14. Aggregate billed demand from 12 months of bills per account.
15. Contract expiry dates and whether capacity is passed through.
16. Decision authority.

**Insurance:**
17. E&O/professional-liability quote covering procurement advice and DR performance advice.
18. Cyber cover for customer data.

## Scores (Stage E revision)

| Criterion | Stage D | Stage E | Reason |
|---|---|---|---|
| fcf | 5 | **4** | Base year-5 op $120,332; plateau ~$150k |
| roic | 8 | **6** | $98,323 year-3 op on $62,155 peak funding (1.58×) |
| access | 5 | **4** | Exempt pool courted; supplier onboarding wants licences and track record [B]; expiry timing |
| scale | 6 | **5** | Rep productivity weak; state-by-state licences |
| resilience | 6 | 6 | Essential spend; collar to May 2030 [A] |
| entry | 4 | 4 | Wedge copyable |
| delegation | 6 | 6 | Standard roles; consent-bound book |
| cash | 5 | 5 | Monthly remittance after the customer pays; annual DR |
| feasibility | 7 | 7 | Exempt path in the rule [A]; statute verbatim unverified |
| ai | 6 | 6 | Cheap, durable bill and PLC analytics |

**Composite:** raw 5.08; evidence-adjusted 5.06 (evidence D).

**Gates:**
- G2_LICENSE: PASS, conditional on V4.
- G4_CEILING: WARN. The base case passes $100k/yr (year 3+), but plateaus there.
