# WS12-012 — Dedicated Philippine tax & accounting staff for Chicago-area CPA firms: Stage E playbook

> **Verdict: conditional finalist, downgraded.** Validate for about $600 before spending on any legal entity. Evidence level **C**: statutes and rules are A, competitor prices B/D, churn and conversion E. Researched 2026-11-28. Model rebuilt with `tools/build_fin_model.py`. Every figure below is quoted from `08_financial_models/WS12-012_results.json` unless marked otherwise.
>
> | Rebuilt model | Conservative | Base | Optimistic (ceiling) |
> |---|---|---|---|
> | Year-3 operating profit | **−$44,675** | **$54,249** | $1,336,053 |
> | Year-5 operating profit | **−$50,048** | **$373,388** | $3,753,362 |
> | Peak funding (draw of $4k/month from month 13) | **$455,972** | **$23,540** | $7,500 |
> | Breakeven month | never | 11 | 4 |
>
> - **Base start capital:** $24,000, the smallest round amount that keeps base cash ≥ 0 (minimum cash $460).
> - **Conservative peak funding without the owner draw:** $263,972. This is a separate engine run with the draw set to 0, not a field in results.json.
>
> **What changed since Stage D, and why the base fell from $231k to $54k in year 3.** Primary-source work found three things:
>
> 1. **Structure.** Stage D's base used Philippine *contractors*. That structure is legally weak:
>    - Under the Philippine four-fold test, the employer's control over how the work is done is decisive [A, E-WS12012-S014]. A full-time seat directed by a CPA firm looks like employment.
>    - The US–Philippines treaty creates a permanent establishment (PE) once services are furnished in the Philippines "through employees or other personnel" for more than 183 days [A, E-WS12012-S011].
>    - So the base now employs workers through the founder's own Philippine export company from about month 9. It carries the statutory costs and an entity-compliance overhead.
> 2. **Price.** Compliant competitors publish $1,963–2,500 per seat, including a SOC 2 Type II provider serving 500+ CPA firms at $2,500 [B/D, E-WS12012-S020–S022]. The base price falls from $2,400 to $2,300, and the account size from 1.4 to 1.25 seats.
> 3. **AI.** Agentic 1040 preparation now ships inside CCH Axcess [C, E-WS12012-S025] and Thomson Reuters [D, E-WS12012-S027]. Black Ore markets its tool as an alternative to offshoring [C, E-WS12012-S026]. Churn rises from 2.5% to 2.8% a month.
>
> **Bridge in the model (base year-3 operating profit):**
>
> | Step | Effect | Running total |
> |---|---|---|
> | Stage D base | | $231k |
> | Price and seat mix | −$71k | $160k |
> | Gross margin 38%→31% | −$73k | $87k |
> | Churn | −$7k | $79k |
> | Entity, SOC 2, insurance and PH coordinator | −$25k | **$54k** |
>
> This bridge was computed in scratch with the same engine.
>
> **Still attractive:** prepaid monthly billing, an A-level prospect register, about $24k of peak funding in base, and highly delegable roles.
>
> **Not attractive:**
> - The conservative case never breaks even.
> - Year-3 base profit is thin because the step hires (US account manager, account executive, SOC 2) all land in year 3.
> - The core 1040 data-entry seat is exactly what AI vendors are automating.

## Corrections to earlier stages (explicit)
- **Correction (structure):** Stage D modelled contractor engagement as the base structure and an own Philippine entity "at ~20+ seats". The PE clock is 183 days [A, E-WS12012-S011], and the control test points to employment [A, E-WS12012-S014]. Contractors are acceptable only for a short pilot after a Philippine counsel opinion. The entity is needed by about month 9, not at 20 seats.
- **Correction (statutory cost):** Stage D used "~20%" ($230) for 13th-month pay plus statutory contributions. The correct figure is **~16%** of a $1,100 salary:

  | Item | Monthly cost | Source |
  |---|---|---|
  | 13th-month pay (1/12 of salary) | $92 | [A, E-WS12012-S012] |
  | SSS employer 10%, capped at a PHP 35,000 monthly salary credit | ≈$56 | [B, E-WS12012-S015] |
  | PhilHealth 5% of basic salary, split equally | ≈$28 | [A, E-WS12012-S016] |
  | Pag-IBIG employer, PHP 200 cap | ≈$3 | [A, E-WS12012-S033] |

  All are converted at PHP 62.658/USD [A, E-WS12012-S019]. Stage D missed two items:
  - the 10% night-shift differential for hours worked between 10pm and 6am [A, E-WS12012-S013], which covers Chicago business hours;
  - double pay for work on Philippine holidays [A, E-WS12012-S013].
- **Correction (EOR contribution):** Stage D said an employer-of-record (EOR) seat leaves ~9% ($221). At $2,300 with night and holiday premia, it leaves **~5% ($122)**.
- **Correction (data privacy):** Stage D said the Philippine Data Privacy Act "likely applies" to client data. Section 4(g) excludes personal information collected from residents of foreign jurisdictions under their own laws and processed in the Philippines [A, E-WS12012-S018]. US obligations (§7216, the FTC Safeguards Rule) govern the client data instead. The Act still covers the Philippine entity's own employee records.
- **Correction (7216 wedge):** Stage D presented the §7216 consent kit as a wedge. The rule requires consent before *any* disclosure to someone located outside the US, *even the firm's own employee* [A, E-WS12012-S001]. Every offshore model therefore carries the same friction. The kit is table stakes, not a moat.
- **Correction (competitor fee):** Stage D recorded Accountant Offshore's management fee as undisclosed. The homepage still does not state it [B, E-WS12012-S023]. A competitor-authored roundup reports ~$600, or about $2,000 all-in for a US accountant [D, E-WS12012-S020]. That is below Stage D's $2,400 rate.

---

## 1. Business explanation
**What it is.** A US company, owned and run by the founder in Illinois, places full-time accounting staff who live in the Philippines inside Chicago-area CPA firms. Each person is dedicated to one firm. They work in that firm's tax and accounting software and are supervised day to day by the firm's CPAs. The company:
- recruits, tests, employs, equips and secures these people;
- replaces them if they leave;
- bills the CPA firm a flat monthly fee per person, in advance.

The roles are staff accountant (bookkeeping, reconciliations, CAS/client accounting), tax preparer (data entry and first-draft preparation of 1040/1065/1120 returns for a CPA to review) and audit associate (work-paper support).

**Who buys and why.**
- **The buyer:** a managing partner or firm administrator at a 5–60-person CPA firm.
- **The pain: capacity.** New Illinois CPA licences fell from ~1,800–1,900 a year (2016–2019) to ~1,300–1,600 a year (2020–2024) [A, DG-S001]. Busy season (January–April) and the September/October extension deadlines need more hands than the firm can hire locally.
- **The saving:** a Chicago staff accountant costs several thousand dollars a month. A dedicated Philippine staff accountant is sold at about $2,000–2,700 a month all-in by established providers [B/D, E-WS12012-S020–S022].
- **Adoption is mainstream but not universal.** In the 2023 AICPA MAP survey, about 25% of firms offshored and 12% planned to start [C, E-WS12012-S029]. Coverage of the 2025 survey puts the share at 29% [D, E-WS12012-S030].

**How it earns.**
- **Spread:** the monthly fee minus the worker's all-in cost (salary, 13th month, Philippine social contributions, night/holiday premia, HMO, equipment). Base is $2,300 − ~$1,579 ≈ **$721 per seat-month (31%)**.
- **Fixed costs:** recruiting, supervision, security/SOC 2, insurance and Philippine entity compliance, all paid from that spread.
- **Working capital:** customers pay at the start of the month and workers are paid semi-monthly in arrears, so the cash cycle is negative.

**Why it is (moderately) attractive.**
- Little capital: base peak funding is $23,540.
- Recurring prepaid revenue.
- A prospect register from the state licensing database: 680 licensed CPA firms in the six-county Chicago area [A, DG-S001].
- Roles that can be delegated: a Philippine team lead and a US account manager.

**Why it is not a sure thing.**
- Many competitors already exist, some with SOC 2 and hundreds of CPA clients.
- The spread per seat is only ~$700.
- The 1040 data-entry work these seats do is the first target of new AI tax-prep agents.

---

## 2. Commercial entry

### 2.1 Initial niche, customer, geography
- **Niche:** dedicated **staff accountant / bookkeeping (CAS) and tax-preparer seats** for **5–60-person licensed CPA firms** in Cook, DuPage, Lake, Will, Kane and McHenry counties. There are 680 such firm licences [A, DG-S001].
- **Pair seasons.** Sell seats as **year-round roles**: CAS and bookkeeping all year, tax January–April and September–October. Do not sell busy-season-only seats.
- **Open with CAS/bookkeeping, not 1040 data entry.** CAS work is less seasonal, and it is less directly targeted by the new agentic 1040 tools [C, E-WS12012-S025].
- **Exclude national and PE-backed firms.** They run captive offshore centres. ORBA, for example, now redirects to Citrin Cooperman [D, DG-S015].
- **Geography:** sell in person in Chicagoland first. National selling comes after 15 accounts, because the product is remote.

### 2.2 Named suppliers and partners (full list: `09_databases/suppliers/WS12-012_suppliers.csv`)

| Supplier / partner | Role | Published terms | Evidence |
|---|---|---|---|
| OnlineJobs.ph | Recruiting channel | Pro $69/month, Premium $99/month; no salary markups | [B, DG-S008] |
| Deel | Contractor management (pilots); EOR bridge | $49/contractor-month; EOR from $599; Contractor of Record $325 | [B, DG-S004] |
| Remote / Oyster | Alternative contractor management / EOR | Contractors $29; EOR $599 (annual) and $699 (monthly) | [B, DG-S005/S006] |
| Penbrothers | Interim co-employer (PEO) option or competitor | Example: $1,463 pay + $500 management fee = $1,963; $300 setup; one-month deposit | [D, E-WS12012-S020] |
| Sourcefit | Staff-leasing option or competitor | Accounting $1,260 / $2,010 / $2,760; $0 setup; ISO 27001 | [D, E-WS12012-S020] |
| Philippine labour/tax counsel | Opinion on structure; entity setup | MISSING; budget $1,500–3,000 | E |
| ICPAS | Events/sponsorship channel | MISSING | E |

### 2.3 Named prospects — top 15 (all have an active IDFPR Public Accountant Firm Licence [A, DG-S001]; none contacted; headcounts MISSING)

| # | Firm (city) | Why prioritised |
|---|---|---|
| 1 | Cray, Kaiser Ltd (Oakbrook Terrace) | Five open roles on its careers page, including Staff Accountant and Senior Tax Accountant [D, DG-S016]. Pain is current. |
| 2 | CJBS LLC (Deerfield) | Open Senior Tax and Senior Audit Associate roles [D, DG-S016]. |
| 3 | Callero and Callero LLP (Des Plaines) | Advertises Senior Tax Associates [D, DG-S016]. Tax-heavy, so a tax-preparer seat fits. |
| 4 | Prado & Renteria CPAs (Chicago) | Recruiting a Senior Auditor and Senior Accountants [D, DG-S016]. Audit support plus a CAS seat. |
| 5 | Miller Cooper & Co (Deerfield) | Careers page, and the site mentions outsourcing services (CSV). Capacity for a CAS line. |
| 6 | Mowery & Schoenfeld (Lincolnshire) | Mid-size; the site references outsourcing services (CSV). |
| 7 | FGMK LLC (Bannockburn) | Multi-office; markets outsourced accounting (CSV). Bookkeeping seats sell year-round. |
| 8 | DHJJ (Naperville) | Two offices; outsourced accounting offered; careers page (CSV). |
| 9 | CDH CPA (Itasca) | Markets outsourced accounting, tax and advisory (CSV). CAS-led demand. |
| 10 | Lauterbach & Amen (Naperville) | Governmental audit specialist (CSV). Its audit season runs counter to tax season, which suits year-round seat pairing. |
| 11 | Legacy Professionals (Westchester) | Benefit-plan and union audits (CSV). Form 5500 season is counter-cyclical to 1040. |
| 12 | Weiss & Company (Glenview) | Experienced-professional careers page (CSV). |
| 13 | Pasquesi Sheppard (Lake Forest) | Careers page (CSV). High-net-worth tax work, so sell a review-support seat, not data entry. |
| 14 | Porte Brown (Elk Grove Village) | Mid-size suburban firm (CSV). Likely multi-seat. |
| 15 | Gray Hunter Stenn (Oak Brook) | DuPage firm (CSV). Easy in-person meetings. |

The remaining 12 firms and full contact pages are in `09_databases/prospects/WS12-012_prospects.csv`. Beyond the 27, the IDFPR dataset gives the full 680-firm universe [A, DG-S001].

### 2.4 Competitors and published prices

| Competitor | Model | Published price (per full-time seat-month) | Evidence |
|---|---|---|---|
| QX Accounting Services (India, Mexico) | Dedicated staff; 500+ CPA firms; SOC 2 Type II, ISO 27001 | Staff accountant / tax preparer / bookkeeper **$2,500**; senior $4,000 | [B, E-WS12012-S021] |
| Cloud Accountant Staffing (PH/LatAm/ZA) | Dedicated staff, employed by the provider | Accountants $2,700, tax $2,900, auditors $3,100, VA $2,200; **$2,250 kickoff fee** | [B, E-WS12012-S022] |
| Accountant Offshore (Pasig City) | Dedicated staff; own office | Talent from $1,400 / $2,300 / $2,400 plus fee [B, E-WS12012-S023]; ~$2,000 all-in for a US accountant [D, E-WS12012-S020] | B/D |
| Penbrothers (PH) | PEO co-employment | $1,963 example | [D, E-WS12012-S020] |
| Sourcefit (PH) | Staff leasing / EOR | $1,260–2,760 accounting | [D, E-WS12012-S020] |
| MYCPE ONE (India/PH) | Dedicated staff; SOC 2 Type II | From $11/hour (~$1,760 at 160 h) | [D, E-WS12012-S020] |
| Finsmart (India) | Seats | Bookkeeping $2,400; senior $3,200; reviewer $3,600; three-month notice | [D, E-WS12012-S020] |
| Generalist VA firms | Managed VAs | $1,500–3,500 | [B, C9-S016/S018/S019] |
| Marketplaces (VirtualStaff.ph, OnlineJobs.ph) | Self-managed | $99/seat + salary; $69–99/month job board | [B, DG-S007/S008] |
| Nearshore LatAm (e.g., Vintti) | Staffing | Staff accountant ~$1,650 | [D, E-WS12012-S020] |
| **AI substitutes** | Software | CCH Axcess agentic 1040 prep (Oct 2026) [C, E-WS12012-S025]; TR Ready to Review (Dec 2025) [D, E-WS12012-S027]; Black Ore Tax Autopilot, claims >98% autonomy and up to 80% lower cost per return [C/D, E-WS12012-S026]; QuickBooks Accounting Agent [D, E-WS12012-S028] | C/D |

**Reading.** The compliant market price for a Philippine staff accountant is **~$2,000–2,500**. A new entrant without SOC 2 cannot sit above QX's $2,500. Undercutting Penbrothers' $1,963 compliant price leaves almost no spread. The only defensible position is **local, partner-level service at a mid-market price ($2,200–2,400)**, plus seat pairing and replacement guarantees.

### 2.5 AI threat assessment (critical issue 3)
- **Evidence that seats will shrink:**
  - BLS projects bookkeeping, accounting and auditing clerks to fall 6% (−85,600 jobs) over 2025–35, because "software innovations have automated many of the tasks" [C, E-WS12012-S024].
  - IBPAP's Philippine 2028 downside of 1.85M FTE sits below 2025's 1.9M, with AI cited [C, C9-S021].
  - Wolters Kluwer's agents classify source documents, extract and map data, calculate the return and generate work papers before review [C, E-WS12012-S025]. That is the job description of an offshore 1040 preparer.
  - Black Ore explicitly pitches itself to firms that would otherwise offshore [C, E-WS12012-S026].
- **Evidence that seats survive (for now):**
  - Every vendor keeps a human reviewer in the loop: "Professionals review, decide and approve" [C, E-WS12012-S025].
  - Vendor autonomy claims are unverified (D).
  - Adoption of offshoring is still rising (25% → 29%) [C/D, E-WS12012-S029/S030].
- **Seat churn data:** none published for any provider (MISSING). Providers publish only *worker* retention: Connext 22% attrition [D, DG-S012]; KMC 86% retention [D, DG-S013].
- **Implications:**
  1. Sell CAS/bookkeeping and review-support seats, where AI lifts output per seat, ahead of pure 1040 input seats.
  2. Train workers to operate the firm's AI tools (exception handling, document chasing, diagnostics clean-up).
  3. Measure each seat's task mix in the pilot (§4).
  4. Treat 2.8%/month base churn as a hypothesis with a kill threshold.

### 2.6 Positioning, pricing, sales and acquisition strategy
- **Positioning:** "Your dedicated, Chicago-managed Philippine accountant: tested on your software, employed compliantly, replaced in 10 business days, and delivered with a §7216 consent pack and Safeguards vendor file your clients and insurer can read."
- **Rate card** (model base $2,300 per seat):

  | Role | Price per month |
  |---|---|
  | Bookkeeper | $1,950 |
  | Staff accountant | $2,300 |
  | Tax preparer | $2,600 |
  | Senior / reviewer | $3,100 |

- **Fees and terms:**
  - Setup $600, waived on a 12-month term. For comparison, Cloud Accountant Staffing charges $2,250 and Sourcefit $0 [B/D].
  - Prepaid monthly; a 90-day initial term, then 60 days' notice.
  - Annual prepay buys 5% off. Never discount for month-to-month.
- **Sales motion:**
  1. Founder outbound to partners and firm administrators: LinkedIn, email and a phone follow-up.
  2. In-person meeting.
  3. Free role profile and a shortlist of 3 tested candidates.
  4. Paid trial week, credited to month 1.
  5. 90-day pilot.
- **Acquisition:**
  - The 27 named firms, then the 680-firm IDFPR list.
  - ICPAS chapter events (cost MISSING).
  - Referrals between partners.
  - Content: a plain-English §7216 offshore consent guide built on the A-level rules.

---

## 3. Transaction economics (all monthly; prepaid at month start, payroll semi-monthly in arrears)

**T1 — Staff-accountant seat employed by the founder's Philippine entity (base structure from ~month 9)**

| Line | $ | Evidence |
|---|---|---|
| Revenue (fee) | 2,300 | C (price band B/D) |
| Gross salary (PHP ~68,900) | −1,100 | D (PH CPA-qualified $1,500–1,900 [D, DG-S003]; local staff accountant ~PHP 240k/yr [D, E-WS12012-S032]) |
| 13th-month accrual (1/12) | −92 | A, E-WS12012-S012 |
| SSS + EC + PhilHealth + Pag-IBIG (employer) | −87 | A/B, E-WS12012-S015/S016/S033 |
| Night differential / holiday premia (half of seats on US hours) | −70 | A, E-WS12012-S013 (rate); share E |
| HMO | −50 | E |
| Laptop/internet/MDM | −80 | E |
| Recruiting/backfill reserve | −100 | E |
| **Contribution** | **721 (31%)** | |

Entity compliance costs ~$1,500/month, which is ~$190 per seat at 8 seats and ~$40 at 40 seats (E).

**T2 — Pilot seat as direct contractor (first ≤6 months only)**
- **Lines:** $2,300 − fee $1,100 − retention bonus $92 − HMO stipend $50 − equipment $80 − Deel $49 [B, DG-S004] − reserve $100 = **$829 (36%)**.
- **Why only for pilots:** the extra ~$108/seat looks attractive, but a full-time seat directed by the client meets the control test [A, E-WS12012-S014], and beyond 183 days it creates a PE [A, E-WS12012-S011].
- **US side:** pay for services performed abroad is not US wages and is not withheld [A, DG-S011]. Collect a W-8BEN [A, E-WS12012-S009]. No 1099-NEC is issued; that form covers US payees, with a $2,000 threshold [A, E-WS12012-S008].

**T3 — Same seat through an EOR (bridge only)**
- **Lines:** $2,300 − salary 1,100 − 13th month and statutory 179 − premia 70 − HMO 50 − equipment 80 − EOR fee 599 [B, DG-S004/S005] − reserve 100 = **$122 (5%)**.
- **Implication:** an EOR is viable only at prices of about $2,900 or more. At that price, firms switch to Cloud Accountant Staffing or QX.

**T4 — Tax-preparer seat (1040/1065), own entity**
- **Lines:** $2,700 − salary 1,350 − 13th month 113 − statutory 93 − premia 80 − HMO 50 − equipment 80 − reserve 100 − PTIN (annual fee $18.75 [A, E-WS12012-S007], ≈$2/month) = **$832 (31%)**.
- **Anchors:** Cloud Accountant Staffing tax $2,900 [B]; QX $2,500 [B].

**T5 — New-account setup**
- **Lines:** $600 − OnlineJobs Premium $99 [B] − screening $150 − consent/security onboarding $50 = **$301**.
- **Note:** this fee is often waived.

**Cash timing:**
- The customer prepays around day −10. Payroll falls on the 15th and the end of the month.
- **Exposures:**
  - a 30-day replacement guarantee;
  - the 13th-month accrual, paid by 24 December [A, E-WS12012-S012];
  - separation pay of at least one month per year of service if a seat is cut for redundancy or labour-saving devices, with one month's written notice to the worker and DOLE [A, E-WS12012-S013]. This applies when a client cancels or AI replaces a seat.

**Failure risks per transaction:**
- The worker quits (backfill cost and up to two weeks of lost billing).
- The client cancels after April.
- A §7216 consent gap creates penalties: $250 per disclosure under §6713 (max $10,000/yr), and §7216 is a misdemeanour [A, E-WS12012-S003].
- A data incident.

**Repeat potential:** high if the seat survives April. Expansion comes from a second seat after the first season. That is modelled as `arpc_annual_growth_pct` = 8% (E).

---

## 4. Validation (ordered by information value per dollar)

**Minimum viable commercial offering:** one dedicated staff-accountant or tax seat.
- **Price:** $2,200–2,300, prepaid, with a 90-day initial term.
- **Pre-hire:** three pre-tested candidates presented before the client commits.
- **Compliance pack:** §7216 consent template plus a Safeguards vendor packet.
- **Pilot structure:** run on a counsel-reviewed contractor agreement for the pilot, with a written plan to move to the founder's own Philippine entity (or a co-employer) before day 150.

| # | Test (order) | Cost | Time | Success | Kill / pivot |
|---|---|---|---|---|---|
| 1 | **20 partner/administrator discovery interviews** from the 27 named firms plus the IDFPR list (questionnaire in materials) | $0 | 3 weeks | ≥8 already use or used offshore staff, and ≥5 state a past or current price ≥$2,100/seat | <3 above $2,000, or most cite the AI tools as their plan |
| 2 | **Pre-sell ask** in the same meetings: a 90-day prepaid pilot at ≥$2,100 | $0–300 (travel) | 6 weeks | ≥2 signed letters of intent or deposits | 0 after 25 qualified conversations |
| 3 | **Supply test:** two OnlineJobs.ph postings ("US tax preparer – Lacerte/UltraTax/CCH" and "staff accountant – QuickBooks/CAS") with a 30-minute skills test | $99 [B, DG-S008] | 2 weeks | ≥10 applicants pass at asks ≤$1,200/month | Qualified asks >$1,400 (spread falls below ~$550) |
| 4 | **Philippine counsel limited-scope opinion** (questions in materials) | $1,500–3,000 (E) | 2–3 weeks | Written route: pilot contractors ≤150 days, then a 100% foreign-owned export corporation (BOI-registered [A, E-WS12012-S017]), or a named PEO at ≤$500 | Counsel says the entity needs >$25k capital or >6 months |
| 5 | **Paid pilot delivery** (2 seats) | Payroll covered by prepayment; ~$1,000 tools | Feb–Apr 2027 | Weekly QA scores ≥4/5; no consent gaps | Client escalations in weeks 1–4 on both seats |
| 6 | **AI task log:** classify every assigned task for 8 weeks into judgment, software operation or data entry | $0 | 8 weeks | <40% pure data entry | >60% data entry (seat replaceable by CCH/TR agents) |
| 7 | **Retention through 30 April 2027** | $0 | — | ≥50% of pilot seats renew at full price into May | All cancel (it is a seasonal labour product) |

**Testable assumptions:**

| Assumption | Base value | Evidence | Tests |
|---|---|---|---|
| Price | ≥$2,100 | E | 1–2 |
| Salary ask | ≤$1,200 | D | 3 |
| Funnel conversion | 40% to proposal, 25% to win | E | 2 |
| Churn | ≤2.8%/month | E | 7 |
| Data-entry share of tasks | <40% | E | 6 |
| Entity setup | ≤$10k | E | 4 |

**Budget to a decision:** $600 for tests 1–3 (allowing for travel and data), then $1,500–3,000 for test 4 only once test 2 has succeeded.

**Conditions to invest more:**
- Tests 1–3 pass;
- 2 prepaid seats live;
- a counsel route is confirmed.

**Abandon or pivot if:**
- the kill thresholds above are hit by 15 February 2027; or
- by June 2027 fewer than 50% of seats renew.

The pivot is a staff-leasing referral or partner model with a Philippine PEO (lower margin, no entity), or exit.

---

## 5. Operations

### 5.1 Lead-to-cash workflow and function classification

| Step | Function | Class |
|---|---|---|
| 1 | Prospect list from IDFPR data; enrichment of open roles and partners | Automatable / AI-assisted |
| 2 | Outreach sequences; call booking | AI-assisted (drafting), human (calls) |
| 3 | Discovery meeting with a partner | **Human (founder)** |
| 4 | Role profile, skills test design, job post | AI-assisted |
| 5 | Sourcing and screening (OnlineJobs.ph, referrals); skills test grading | Human (PH team lead), with AI-assisted grading |
| 6 | Final interview by the client; selection | Human (client) |
| 7 | MSA, DPA, §7216 consent pack, Safeguards vendor file | AI-assisted drafting; **professional-dependent** (US attorney sign-off once) |
| 8 | Employment contract, SSS/PhilHealth/Pag-IBIG enrolment, payroll | **Professional-dependent** (PH payroll provider/accountant); automatable runs |
| 9 | Laptop provisioning, MDM, MFA, encrypted access to client VDI | Human (IT setup) plus automatable policies |
| 10 | Monthly prepaid invoice; collections | Automatable |
| 11 | Weekly QA check-in; work-paper sampling | Human (PH team lead / US account manager), AI-assisted sampling |
| 12 | Quarterly business review, seat expansion | Human (founder / account manager) |
| 13 | Backfill within 10 business days | Human |
| 14 | 13th-month, separation pay, statutory filings | Professional-dependent |
| 15 | Partner relationship, escalations, incident response | **Not automatable** |

### 5.2 Fulfilment, support, QA, exceptions
- **Fulfilment:** workers log into the client's own environment (UltraTax, Lacerte, CCH Axcess, QuickBooks Online) through the client's VDI or VPN, from a company-managed laptop with MDM.
  - MFA is required for anyone accessing customer information [A, E-WS12012-S005].
  - Customer information must be encrypted in transit and at rest [A, E-WS12012-S005].
  - No local downloads.
- **QA:**
  - a weekly 15-minute client check-in;
  - monthly sampling of 5 work items against the firm's review notes;
  - an error log;
  - quarterly scorecards.
- **Exceptions:**
  - worker absence: same-day notice and a cover worker from the bench (bench of 1–2 at 10+ seats);
  - a resignation: 10-day backfill;
  - suspected data incident: the incident plan is run, and the client is told so it can meet its FTC duty to notify within 30 days if ≥500 consumers are involved [A, E-WS12012-S005];
  - consent gap: the worker stops work on that client until consent is on file.

### 5.3 Software stack and prices
Prices are E unless marked; none were verified at source this session except Deel and OnlineJobs.ph.

| Need | Tool | Monthly cost |
|---|---|---|
| Email, docs | Google Workspace or Microsoft 365 | ~$15–25/user |
| CRM | HubSpot free tier or a spreadsheet | $0 |
| Passwords | 1Password or Bitwarden business | ~$4–8/user |
| MDM/endpoint | Intune (M365 Business Premium) or similar | ~$22/user |
| Contractor payouts (pilot) | Deel | $49/contractor [B, DG-S004] |
| PH payroll (entity) | Local payroll provider | Inside the $1,500/month entity line |
| Recruiting | OnlineJobs.ph Premium | $99 [B, DG-S008] |
| Accounting | QuickBooks Online | ~$40–100 |
| AI drafting/QA | Claude or another LLM at ordinary paid tiers | ~$20–100 |

The model's software/AI line is $250/month, and security tooling is a separate $400/month.

### 5.4 Legal requirements — US and Illinois
1. **Formation and records.** Form an Illinois LLC and obtain an EIN. The Secretary of State fee was not fetched (MISSING; verify).
2. **No employment-agency licence, as long as only employers pay.** The Illinois Private Employment Agency Act excludes recruiters compensated solely by employers [A, C9-S022]. Never charge workers a fee. The licence otherwise needs a $5,000 bond [A, WS12-S015].
3. **Do not hold out as a CPA firm.** The company provides staff under CPA supervision. It does not issue attest reports or sign returns. The Illinois Public Accounting Act title restrictions were not retrievable (ILGA unreachable); confirm the name and marketing wording with counsel (E).
4. **Payments to foreign contractors.**
   - Services performed abroad by nonresident aliens are not US wages and are not withheld [A, DG-S011].
   - Collect a W-8BEN [A, E-WS12012-S009].
   - No 1099-NEC [A, E-WS12012-S008].
5. **Once a Philippine subsidiary exists.**
   - File Form 5471 [A, E-WS12012-S031].
   - Expect CFC income-inclusion rules and FBAR filing if foreign accounts are held (E; needs an international tax CPA).
   - Set a cost-plus service agreement between the US company and the Philippine entity, with transfer-pricing documentation (E).
6. **Insurance.** Professional liability/E&O, cyber and general liability. Quotes are MISSING; the model uses $450/month (E).

### 5.5 CPA-firm-specific requirements (critical issue 2) — what the product must do for the client

| Requirement | What the rule says | What the product does |
|---|---|---|
| **IRC §7216 consent** | Consent is required before disclosing tax return information to anyone located outside the US, including the firm's own employee [A, E-WS12012-S001]. Separate documents for "use" and "disclosure"; one-year default duration; copy to the taxpayer [A, E-WS12012-S002]. | A ready-to-send consent template set (individual and business), a tracking sheet, and a rule that **no return is assigned without a logged consent**. |
| **SSNs offshore (1040 series)** | Allowed only if both the US firm and the offshore preparer maintain an "adequate data protection safeguard" conforming to a recognised framework, with a prescribed statement in the consent [A, E-WS12012-S002/S004]. | **Default to masked SSNs.** Where unmasked SSNs are needed, document the security program against a named framework; ISO 27001 or SOC 2 as "equivalent" needs counsel confirmation. |
| **Penalties** | §7216 misdemeanour; §6713 $250 per disclosure, up to $10,000/yr. The staffing company and each worker are "tax return preparers" [A, E-WS12012-S003]. | Workers sign confidentiality undertakings, and training is logged. |
| **FTC Safeguards Rule** | Accountants and tax preparers are "financial institutions". They need a WISP, MFA, encryption and service-provider oversight by contract and periodic assessment [A, E-WS12012-S005]. IRS Pub 4557 restates the WISP duty [A, E-WS12012-S006]. Small firms (<5,000 consumers) are *not* exempt from vendor oversight [A, E-WS12012-S005]. | A "vendor file": our WISP summary, MFA/encryption attestations, contract safeguard clauses, an annual assessment questionnaire, and SOC 2 from year 2. |
| **PTIN** | Anyone who prepares or assists in preparing returns for compensation needs a PTIN ($18.75 for 2027) [A, E-WS12012-S007]. | Tax-preparer seats obtain PTINs. The foreign-applicant process was not fetched (verify). |
| **AICPA Code** | Inform the client, preferably in writing, before disclosing confidential information to a third-party service provider [A, E-WS12012-S010 (1.150.040)]. Ensure qualifications and adequately plan and supervise [1.300.040]. Have a confidentiality contract or obtain specific consent [1.700.040]. | A client-notice letter template, an MSA confidentiality clause, and a qualifications dossier per worker. |

### 5.6 Philippine (and LatAm) structure (critical issue 1)

| Option | What the law says | Seat contribution | Use |
|---|---|---|---|
| Direct contractors | Four-fold test with control decisive [A, E-WS12012-S014]. Work "usually necessary or desirable" to the business is regular employment [A, E-WS12012-S013]. A treaty service PE arises after >183 days [A, E-WS12012-S011]. | ~$829 (36%) | **Pilot only (≤150 days)**, with a counsel opinion. |
| EOR (Deel/Remote/Oyster) | The EOR is the legal employer, at $599–699 [B, DG-S004–S006]. | ~$122 (5%) | Emergency bridge only. |
| PEO / staff leasing (Penbrothers/Sourcefit-type) | Co-employer; ~$500 fee in the one documented example [D, E-WS12012-S020]. | ~$220 (10%) | Bridge for 1–8 seats if the entity is delayed. |
| **Own Philippine export-services corporation** | RA 11647 allows 100% foreign ownership of export enterprises; non-Philippine-national export enterprises register with BOI and keep ≥60% exports. The US$200k minimum applies to domestic-market enterprises [A, E-WS12012-S017]. The entity owes 13th month, SSS/PhilHealth/Pag-IBIG, night differential, holiday pay, 5-day SIL and separation pay [A/B]. | ~$721 (31%) before ~$1,500/month compliance | **Base from ~month 9.** |
| PEZA/BOI incentive registration | Not needed at this scale (E). | — | Revisit at 50+ seats. |
| LatAm (Colombia/Mexico) | Labour law not researched (MISSING). Nearshore staff accountant ~$1,650 [D, E-WS12012-S020]. | Unknown | Later option, EOR only. |

**PE logic.** The US company furnishing services through Philippine personnel for more than 183 days risks a Philippine PE, and Philippine tax on the profits attributable to it. Under Art. 5(8), a subsidiary that bills the US company at cost-plus does not by itself make the parent a PE [A, E-WS12012-S011]. This is the standard structure, and its tax and transfer-pricing details need counsel (E).

### 5.7 Financial administration
- **US books:** monthly close in QuickBooks; revenue recognised by service month.
- **Philippine entity:** books kept by a PH accountant; 13th-month accrual; separation-pay reserve.
- **FX:** treasury sends USD to the PH entity monthly. The peso moved from 56.443 to 62.658 per USD in 15 months [A, E-WS12012-S019]. Keep 1 month of PHP payroll in reserve.
- **Model reserve:** 2 months of cash costs in base, 3 in conservative.

### 5.8 Post-December-2026 AI cost and fallback
- **Where AI is used:** drafting (job posts, SOPs, consent templates), QA sampling and prospect research. The model budgets $250/month.
- **Sensitivity:** if AI/software costs triple, base year-3 operating profit is $47,884 versus $54,249.
- **Fallback:** every AI-assisted step has a manual SOP. The business does not depend on unlimited AI. The *threat* side of AI (customers' tools) matters far more than the *cost* side.

---

## 6. Growth

**First 10 customers (months 1–12).**
- Founder-sold from the 27 named firms and IDFPR lists, at ~12 qualified conversations/month (E).
- **Base funnel:** 12 × 40% × 25% ≈ 1.2 accounts/month.
- **Base model:** 6.3 active accounts at the end of year 1 and 18.1 at the end of year 2.
- **Keys:** in-person meetings, pre-tested candidates and seat pairing.

**First 100 customers.**
- **Base model:** 32.9 accounts at the end of year 3 and 60.6 at the end of year 5. 100 accounts is not reached in base within 5 years.
- **Optimistic case:** 97.6 accounts by year 3. Treat this as a ceiling.
- **What it takes:** national selling through state CPA societies after 15 accounts; one account executive; referrals.

**Hiring sequence (model staff table):**

| Hire | Milestone that justifies it | Monthly cost (base) | Productivity |
|---|---|---|---|
| PH team lead/recruiter | 8 active accounts (model month ~15) | $1,600 | 15 accounts per lead |
| PH HR/payroll coordinator | 20 accounts | $900 | 40 accounts each |
| Account executive | $60k monthly revenue (year 3) | $6,500 loaded | 0.8 new accounts/month after a 4-month ramp (E) |
| US account manager | $70k monthly revenue | $6,000 | One per $150k MRR, max 3 |

**Capacity limits:**
- **Founder:** ~12 partner conversations a month while also vetting candidates.
- **Team lead:** ~15 accounts (~20 seats).
- **Recruiting pipeline:** OnlineJobs Premium gives 10 posts and 500 contacts a month [B, DG-S008].

**Geographic expansion:** Chicago first, then Milwaukee/Indianapolis/St. Louis through state CPA societies, then remote national selling. Delivery cost does not change with geography.

**Adjacent products:**
- audit and benefit-plan audit seats (counter-seasonal);
- CAS/bookkeeping pods for firms launching client accounting;
- "AI-exception" seats that run the CCH or TR agents and clear diagnostics.

**Vertical integration and incremental return:**
- **Own PH entity (included in base):** +~$600/seat-month versus EOR. At 8 seats that covers the ~$1,500/month compliance cost 3×.
- **Secure office pod:** later, only if clients demand office-based staff (E).
- **SOC 2:** $1,000/month from month 13 (E) unlocks firms with more than 20 staff.

**Delegation:** a US account manager plus a PH operations lead can run the day-to-day at about 30–40 accounts (model year 3–4). The founder keeps sales and partner relationships until the account executive is productive.

**Reinvestment slots:**
1. A second account executive.
2. A national CPA-society channel.
3. A LatAm nearshore line via EOR.
4. Acquisition of a small competitor's book later. This is not an entry route.

---

## 7. Financial analysis (quoted from the rebuilt results)

**Launch capital and working capital (base):**
- **Start capital:** $24,000. It funds $12,500 of one-time setup in year 1 ($3,500 setup, a $2,000 counsel opinion, $7,000 entity formation) plus the operating losses before breakeven: overhead is ~$1,550/month, rising to ~$3,050 from month 9.
- **Peak funding:** $23,540. Minimum cash is $460, in month 8, when the entity capex lands.
- **Working capital:** customer-funded (DSO −10 days, DPO 7 days).

**24-month view (base; monthly engine output, same logic as the workbook):**

| Month | 1–4 | 6 | 8 | 10 | 12 | 15 | 18 | 21 | 24 |
|---|---|---|---|---|---|---|---|---|---|
| Active accounts | 0 | 0.6 | 2.0 | 4.1 | 6.3 | 9.5 | 12.5 | 15.4 | 18.1 |
| Revenue ($) | 0 | 1,956 | 6,135 | 12,457 | 18,890 | 30,362 | 39,794 | 48,725 | 57,183 |
| Operating profit ($) | −2,150/mo | −1,673 | −575 | −378 | 1,419 | 1,860 | 4,496 | 6,992 | 9,356 |
| Cash ($) | 18,350→9,900 | 7,187 | 460 | 1,890 | 7,016 | 6,808 | 10,353 | 21,277 | 39,190 |

**5-year annual view:**

| | Year 1 | Year 2 | Year 3 | Year 4 | Year 5 |
|---|---|---|---|---|---|
| **Base revenue** | $68,640 | $491,855 | $1,032,150 | $1,825,854 | $2,613,084 |
| Base gross profit | $22,455 | $155,450 | $324,611 | $572,334 | $817,275 |
| **Base operating profit** | −$13,771 | $61,253 | $54,249 | $214,973 | $373,388 |
| Base FCF | −$16,984 | $80,174 | $79,622 | $196,764 | $306,593 |
| Base retained after $48k draw | −$16,984 | $32,174 | $31,622 | $148,764 | $258,593 |
| **Conservative operating profit** | −$41,621 | −$57,658 | −$44,675 | −$55,305 | −$50,048 |
| Conservative revenue | $9,848 | $110,919 | $203,354 | $263,802 | $304,315 |
| **Optimistic operating profit** | $84,777 | $504,046 | $1,336,053 | $2,417,540 | $3,753,362 |

**Breakeven and milestones (base):**

| Milestone | Month |
|---|---|
| Breakeven | 11 |
| First month with operating profit ≥ $1k | 12 |
| ≥ $5k | 19 |
| ≥ $10k | 25 |
| ≥ $25k | 49 |
| Payback | 22 |

The conservative case never reaches $1k a month. The optimistic case breaks even in month 4.

**Why year 3 dips in base ($61,253 → $54,249):** three step costs land together:
- SOC 2 at $1,000/month;
- the account executive, $6,500, triggered at $60k monthly revenue;
- the US account manager, $6,000, triggered at $70k monthly revenue.

The same artifact explains why some stresses *raise* year-3 profit while crushing year 5. Win rate −40% gives year 3 $79,570 but year 5 only $96,210, because slower growth postpones the hires. **Judge stresses on year 5.**

**Scenario drivers:**

| Driver | Conservative | Base | Optimistic |
|---|---|---|---|
| Revenue per account | $2,200 | $2,875 | $3,900 |
| Gross margin | 24% | 31% | 40% |
| Monthly churn | 4.5% | 2.8% | 1.8% |
| Founder wins per month | ~0.5 | ~1.2 | ~2.4 |

**Sensitivity (tornado, base year-3 operating profit at ±25%):**
- **Gross margin is dominant:** −$24,502 at 23.25%, $132,999 at 38.75%.
- **Labour cost multiplier:** $97,321 / $11,176.
- **ARPC:** $66,885 / $128,239. The low side looks better because of the step-hire artifact.
- **Overhead:** $66,428 / $42,070.
- **Churn:** $63,301 / $49,989.

**Stress tests (base; year-3 / year-5 operating profit / peak funding):**

| Stress | Year 3 | Year 5 | Peak funding |
|---|---|---|---|
| Gross margin −5 pts | $2,641 | $242,734 | $31,413 |
| **Gross margin −10 pts** | **−$48,966** | $112,079 | $108,118 |
| Competitor response | $47,240 | **$83,934** | $28,548 |
| Recession | $75,414 | **$48,198** | $44,287 |
| Growth twice as slow | $36,758 | **$38,497** | $88,943 |
| Founder capacity −40% | $79,570 | $147,151 | $49,126 |
| Labour +20% | $19,791 | $314,951 | — |
| 25% of accounts lost in month 18 | $58,033 | $363,995 | — |
| Customers pay 30 days later | — | — | $66,935 |

**Downside cases.** The conservative case loses about $45–58k a year in every year. Its peak funding is $455,972 with the owner draw and $263,972 without it (separate engine run with the draw set to 0). The validation gates in §4 exist so this path is stopped within about $5–10k.

**Capital accumulation to year 10 (base, long-term table):**

| Measure | Value |
|---|---|
| Cumulative deployable cash, year 5 | $197,058 |
| Cumulative deployable cash, year 10 | $1,256,368 |
| Year-10 operating profit | $464,095 |
| Enterprise value at 3.0×, year 5 | $1,120,164 |
| Enterprise value at 3.0×, year 10 | $1,392,286 |
| Cumulative owner compensation over 10 years | $454,484 |
| Owner wealth at year 10 | $3,103,138 |

- **Conservative:** deployable cash is $0.
- **Optimistic:** year-10 cumulative deployable is $19,129,201. This is not credible as a forecast; it is a ceiling.
- **Owner distributions:** the draw of $4,000/month from month 13 is funded from operations in base, with year-2 retained cash of $32,174.
- **Long-term drivers:**

  | Driver | Base | Conservative | Evidence |
  |---|---|---|---|
  | Year-6 growth | 6% | 2% | BLS −6% for clerks [C, E-WS12012-S024]; adoption 25→29% [C/D] |
  | Growth decay | 0.85 | 0.7 | E |
  | Incremental ROIC | 0.8 | 0.4 | E |
  | Maintenance capex | 3% | 5% | E |
  | Reserve | 2 months | 3 months | separation pay [A, E-WS12012-S013] |
  | Exit multiple | 3.0× | 2.0× | service businesses median 2.38× SDE [D, E-WS05007-S007]; recurring MSPs ~5.4× [D, E-WS04014-S015] |

**Structure variant.** This was computed in scratch with the engine and is not in results.json. It keeps contractors for the whole 5 years (GM 30% / 36% / 43%, with no entity costs). Base year-3 operating profit would be ~$133k, and conservative still ~−$7k. It is shown only to size what the legal structure is worth; it is **not** recommended.

---

## 8. Capital deployment ladder

| Tranche | What it buys | Evidence gate before spending | How it could be lost |
|---|---|---|---|
| $0–500 | Desk research on the 27 firms; 20 discovery interviews; OnlineJobs Premium supply test ($99); domain/Workspace | None | Time only |
| $500–2k | Illinois LLC + EIN; WISP and security baseline (password manager, MDM trial); MSA/DPA/consent templates reviewed by a US attorney (limited) | ≥5 interviewees state current or past offshore pricing ≥$2,100; supply test passes | Templates unused if no pilot |
| $2–5k | Philippine counsel opinion ($1.5–3k E); 2 loaner laptops; E&O/cyber binding | ≥2 signed letters of intent or deposits for prepaid pilots | Opinion shows the structure is unworkable (still worth knowing) |
| $5–10k | Run 2–4 pilot seats. Payroll is prepaid by the clients; the founder funds equipment, tools and the guarantee | Deposits received; consents in place | Refunds on failed pilots; worker turnover |
| $10–25k | Philippine entity formation (~$7k E) + compliance retainer ($1,500/month); PH team lead | ≥5 prepaid seats, ≥3 months live, counsel confirms the route, ≥1 seat renewed into May | Entity fixed costs with too few seats (the conservative path) |
| $25–50k | SOC 2 readiness and audit; US account manager | ≥15 accounts or ≥$40k MRR; churn ≤3%/month for 6 months | SOC 2 spend without upmarket wins |
| $50–100k | Account executive ramp; ICPAS/state-society sponsorships; national push | ≥25 accounts, ≥$60k MRR, CAC payback <3 months, task log shows <40% data entry | AI substitution (Black Ore/CCH/TR) collapses 1040 seat demand mid-ramp |

---

## 9. Strategic wealth creation
- **How it becomes a durable cash asset:**
  - a book of prepaid, multi-seat accounts;
  - a Philippine entity with a trained bench and SOPs;
  - security attestations;
  - referral density among Chicago partners.
- **Cash generation:** in base, ~$300k/yr of FCF by year 5 ($306,593) and $1,256,368 of cumulative deployable cash by year 10.
- **The base depends on three unproven drivers:** gross margin of ~31% (the single largest sensitivity), churn of 2.8% and ~1.2 founder wins a month.
- **Management takeover:** at ~30–40 accounts (year 3–4 in base), with a US account manager and a PH operations lead.
- **Funding other ventures:** this becomes possible only after year 4 in base, when deployable cash turns positive ($43,267 in year 4).
- **As a first company for a diversified portfolio, the weaknesses are four:**
  1. The moat is thin. Competitors already have SOC 2 and hundreds of CPA clients, and the §7216 kit is table stakes.
  2. It faces the most direct AI-substitution threat among the finalists' service lines. The vendors are explicitly selling against offshoring.
  3. The compliant structure drags in foreign-entity complexity: Philippine labour law, separation pay, Form 5471 and transfer pricing.
  4. The conservative case is a steady loss, not a small profit.
- **The strengths are three:** cheap validation, customer-funded working capital, and a path to delegation. It is best treated as a **cheap option to test**, not the anchor first company, unless the pilots beat the base drivers.

---

## 10. Execution plan

### First 7 days (1–7 December 2026; heavy Claude access ends 5 December)
**Claude prepares before 5 December** (all DRAFTS):
- interview guide and outreach variants (see materials);
- a §7216 consent template set: individual and business disclosure consents, including the mandatory offshore-SSN statement [A, E-WS12012-S004];
- a WISP outline mapped to 16 CFR 314.4;
- a client vendor-file packet;
- the Philippine counsel question list;
- a pricing calculator spec;
- an enriched sheet of the 27 firms with partner names from firm websites.

**Founder:**
1. Read the materials.
2. Pick 15 firms.
3. Personally make the first 20 outreach touches: LinkedIn connection notes and email to managing partners and firm administrators.
4. Book 3–5 meetings for 8–19 December, before busy season.

**Spend:** $0.

### First 30 days (to 31 December 2026)
- **Founder:**
  - hold ≥12 discovery interviews (Cray Kaiser, CJBS, Callero, Prado & Renteria, Miller Cooper, Mowery & Schoenfeld, FGMK and DHJJ first);
  - ask past-behaviour questions: who they used, what they paid, why they stopped, and how they handle §7216 consent;
  - at the end of each qualified meeting, ask for a prepaid 90-day pilot starting in January or February.
- **Supply test:** post the two OnlineJobs.ph roles ($99). This is the founder's own account; Claude never creates it. Run 30-minute skills tests.
- **Evidence required by 31 December:**
  - ≥12 interviews logged;
  - ≥5 price data points;
  - ≥10 applicants passing the test with asks ≤$1,200;
  - ≥1 written pilot commitment.
- **Proposed spend:** ≤$300.
- **Accept a first order only if all hold:**
  - prepaid;
  - ≥$2,100;
  - 90-day term;
  - the client agrees to obtain §7216 consents before assigning returns;
  - the client provides VDI or remote access with MFA.
- **Abandon if:** <3 firms quote ≥$2,000, or nobody will even pilot.

### First 90 days (to 28 February 2027)
- **If ≥2 pilot commitments:**
  - commission the Philippine counsel opinion ($1.5–3k);
  - bind E&O/cyber;
  - sign the MSA/DPA;
  - start 2 seats (contractor pilot via Deel, $49) with weekly QA and the AI task log.
- **Keep selling through busy season** to CAS-focused firms; tax partners will be unreachable February–April.
- **Gate at 28 February:**
  - 2–4 prepaid seats live;
  - no consent gaps;
  - QA ≥4/5.
- **Slow branch:** 1 seat live. Extend selling to May–June, which is the true buying window for next season.
- **Failure branch:** 0 seats. Stop. The loss is ≤$600.

### First year (to December 2027)

| When | Milestone |
|---|---|
| 30 April | Renewal test: ≥50% of seats renew. |
| By ~month 8 (July 2027) | Form the PH entity if ≥5 seats and counsel confirms the route. Otherwise use a PEO bridge. |
| By ~month 9 | Move pilots onto entity payroll, before the 183-day threshold. |
| May–October | Sell next season's seats. |
| Month 12 | ~6 accounts (base). Operating profit ≥$1k/month (base month 12). |

- **Slow-growth branch:** at <4 accounts by month 12, do not form the entity. Run a PEO referral model or stop.
- **Failure branch:** if >30% of seats cancel by June, or the task log shows >60% data entry, exit with the loss capped around $5–10k.

---

## 11. Pre-mortem

| Scenario | How it happens | Early warning | Cheap preventive test |
|---|---|---|---|
| **Lost $5k** | No firm pays ≥$2,100; founder spends on templates, laptops and a counsel opinion before demand | <2 commitments after 25 qualified conversations | Pre-sell before any spend (§4 test 2) |
| **Lost $25k** | Entity formed at 3–4 seats; post-April cancellations; separation pay and 13th-month accruals on idle staff [A, E-WS12012-S013] | Renewal <50% on 30 April; bench >1 idle worker for 30 days | Entity gate (≥5 seats, ≥1 renewal); PEO bridge first |
| **Lost $50k+** | Data incident (an unmasked SSN leak) or a §7216 consent gap leads to client loss, E&O deductible and counsel fees; or a worker misclassification and PE assessment on a long-running contractor model | Any consent gap; any client asking for SOC 2 before renewal; any worker dispute | Masked-SSN default; consent log check before assignment; 150-day contractor limit |
| **Revenue but no profit** | Price drifts to ~$2,000 against Penbrothers/Sourcefit; gross margin −10 pts → base year-3 −$48,966 | Realised price <$2,150; salary asks >$1,300 | Rate card held; quote role-by-role; supply test |
| **Exhausting low-paid job** | Founder becomes recruiter, IT help desk and payroll clerk for 10 seats at ~$700 spread | Founder >20 h/week on fulfilment by month 9 | Hire the PH team lead at 8 accounts (model) |
| **Cash crunch** | Client pays late or disputes a month; 13th-month pay due 24 December; peso moves | Any invoice >5 days late; Q4 payroll forecast | Strict prepay; 1 month PHP reserve; card-on-file |
| **Can't run without founder** | Partners buy the founder, not the company | Clients refuse account-manager meetings | Introduce the account manager at onboarding from account #10 |
| **No deployable surplus** | Base y1–3 FCF absorbed by reserves (deployable cash is negative through year 3 in base) | Year-3 operating profit <$50k | Do not add SOC 2 or an account executive until ≥$40k MRR |
| **AI wipes out 1040 seats** | CCH/TR/Black Ore agents prepare 1040s; firms cancel input seats [C/D, E-WS12012-S025–S027] | Task log >60% data entry; clients piloting agentic prep | Sell CAS/review seats; train workers on the firm's AI tools |

---

## 12. Required confirmations (must be confirmed directly; none confirmed by research)
1. **Philippine counsel:**
   - Would a full-time dedicated contractor be reclassified under the four-fold test?
   - Does contractor service beyond 183 days create a PE under Art. 5(2)(j)? What Philippine tax and penalty exposure follows?
   - What are the minimum capital, timeline, fees and BOI requirements for a 100%-foreign-owned export-services corporation (RA 11647)?
   - How do separation pay and notice rules apply when a client cancels?
   - Is a PEO bridge DOLE-compliant?
2. **US tax counsel/CPA:**
   - Whether ISO 27001 or SOC 2 counts as an "adequate data protection safeguard" under Rev. Proc. 2013-14 §5.07.
   - Consent mechanics for business returns.
   - PTIN requirement and process for foreign preparers.
   - Form 5471, CFC inclusions, FBAR and transfer pricing for the PH subsidiary.
   - Whether any US withholding or reporting applies to the US–PH service charge.
3. **Illinois:**
   - LLC filing fee.
   - Public Accounting Act limits on names and marketing ("accounting", "CPA").
   - The Personal Information Protection Act breach duties.
   - Confirmation that the employment-agency exclusion applies to the business model.
4. **Suppliers:**
   - Penbrothers/Sourcefit interim co-employer fees and terms.
   - Deel contractor terms for the Philippines.
   - PH payroll provider cost.
   - OnlineJobs.ph applicant volume for US-tax skills.
5. **Customers:**
   - Real prices paid for offshore seats.
   - Willingness to prepay.
   - Who obtains §7216 consents: the firm, under its engagement letter.
   - Whether VDI/MFA access is available.
   - Their AI-tool plans for 2027.
6. **Insurance:** E&O, cyber and GL quotes with offshore-staff and tax-data exposures disclosed.
7. **Market data:** any client-churn or seat-tenure data from providers (MISSING), and the ICPAS sponsorship/endorsement terms.
