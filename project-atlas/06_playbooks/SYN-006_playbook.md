# SYN-006 — Construction Subcontractor Back Office: Stage E Playbook

**Concept:** surety-ready job-cost/WIP bookkeeping plus Illinois certified payroll for Chicagoland public-works subcontractors.
**Stage E date:** 2026-11-28 · **Status:** finalist · **Evidence on economics:** D (prices are vendor list prices; conversion is assumption)

**Files**
- Model: `08_financial_models/SYN-006_assumptions.json`, `_model.xlsx`, `_results.json` (rebuilt today under the Stage E standardization rules).
- Prospects: `09_databases/prospects/SYN-006_prospects.csv` (36 rows; 5 added today).
- Partners and suppliers: `09_databases/suppliers/SYN-006_suppliers.csv`.
- New sources: `06_playbooks/sources_E_SYN-006.jsonl` (E-SYN006-S001…S024).
- Draft materials: `06_playbooks/SYN-006_materials.md`.

---

## Verdict

**GO to validation only.** Spend no more than about $1,000 and about 60–90 days. Make no hire and no capital commitment before the gates in §4.

**Why it stays a finalist:**
- **The legal path is clean.** No licence is needed for bookkeeping or for preparing certified payroll [A, DB-S014; A, E-SYN006-S024].
- **Demand is mandated and recurring.** Certified payroll is due monthly by the 15th on every Illinois public works job [A, C5-S014].
- **Surety demand for WIP schedules is now documented at B, not D.** One carrier will bond contractors up to $1.5M with "No C.P.A. Requirement", underwriting on business statements plus a WIP schedule [B, E-SYN006-S005].
- **Leads are public.** City and federal award records name the buyers [A, E-SYN006-S019; A, DB-S019].
- **Capital needs are tiny.** Base-case peak funding is **$9,979**, so the start capital is **$10,000**.

**Why it is not a clear winner:**
- **Price evidence is still D.** We have no realized Chicago fee.
- **The founder has no construction-accounting track record**, yet the whole product is trust in accuracy.
- **Profit is very sensitive to labour productivity.** Labour +20% cuts base year-3 operating profit from **$94,734 to $41,901**. Hiring 30% sooner turns it to **−$22,178**.
- **The ceiling is about $250k/yr** of operating profit for a founder-led Illinois firm.

---

## 1. Business explanation (for someone new to construction)

**Who the buyer is.** A specialty subcontractor (plumber, electrician, roofer, concrete or sewer contractor) with $1–20M of revenue.
- It wins work from general contractors (GCs) and public bodies.
- On public jobs it must post a performance and payment bond. Illinois requires bonds on state and local public works over $150,000 (over $50,000 from 2029), and on IDOT and Tollway work over $500,000 [A, DB-S017].
- The bond is issued by a surety company through a surety broker. Before issuing, the surety underwrites the contractor's finances.

**What the surety asks for.** A typical carrier packet [B, E-SYN006-S004] asks for:
- the last two fiscal year-end statements;
- a current interim statement, required if the year-end statement is more than six months old;
- a **Work-on-Hand (WIP) schedule**. For each open job it lists the contract price, estimated total cost, cost to date, billed to date and the revised estimate.

**Why the WIP schedule matters.** From those columns the underwriter calculates:
- percent complete (cost to date ÷ estimated total cost);
- earned revenue;
- **over-billings and under-billings** (billed vs earned).

Over-billing means the contractor has collected cash ahead of the work. That cash should still be in the bank. Under-billing often means a job is losing money.

**Why small subs cannot produce it.** Most of these firms keep cash-basis QuickBooks with no job costing, so they cannot produce a credible WIP schedule. The pain shows up as:
- smaller bond lines;
- slow bond approvals;
- expensive CPA clean-up bills.

**Certified payroll, the second mandate.** Every contractor and subcontractor on an Illinois public works project must file a certified payroll with the Illinois Department of Labor (IDOL):
- monthly, by the 15th for the prior month, and only for months with work;
- filed per project, through IDOL's portal, using a fixed-column Excel template [A, C5-S014; A, E-SYN006-S002];
- the employer keeps the liability ("liability falls with the individual contractor") [A, E-SYN006-S002].

**Penalties.**
- Since SB1344 (Public Act 104-0023, signed 2025-06-30), a missed filing carries a civil penalty of up to $1,000, or $2,000 for a repeat within 5 years [C, E-SYN006-S001; C, C5-S019].
- A conviction for willful failure or false filing means automatic 4-year debarment from public work [A, C5-S016].

**Extra reporting on some owners' jobs.**
- On Public Building Commission (PBC) of Chicago jobs, subs also report payroll monthly in the PBC's LCPtracker system and M/WBE payments in B2GNow [B, E-SYN006-S018].
- On state-funded public works of $500k or more, contractors must certify Illinois Works apprenticeship hours: a goal of 10% of labour hours per classification [A, E-SYN006-S017].

**What the business sells.** One fixed monthly fee covers:
- **Monthly accrual close by about day 10:** reconciliations, accruals and retainage, with books kept on the client's own QuickBooks file.
- **A job-cost report.**
- **A quarterly WIP schedule** in surety format.
- **Certified payroll:** prepared for each month and project with prevailing-wage work.
- **A year-end package** handed to the client's CPA.

**What it does not do:**
- It is not the payroll processor; the client keeps QuickBooks Payroll, ADP or Gusto.
- It does not issue CPA reports or opinions, and never uses the "CPA" title.
- It does not file liens or give legal advice.
- It does not sell bonds or insurance.

**Why customers pay.**
- A usable WIP keeps or expands their bond line. That decides whether they can bid a $1M job.
- A missed certified payroll can freeze GC payments, trigger penalties and, if repeated or willful, cost them public work entirely.
- The owner or office manager does not have the skill or time.
- Generic bookkeepers and AI tools do not do WIP. Pilot ($99/month) is cash-basis [B, C5-S004]; Digits ($65–$250/month) includes no human [B, C5-S005].

**How it earns.**
- Recurring revenue: about $1,000 per client per month blended (model base, D).
- One-time revenue: about $1,500 per new client for onboarding clean-up.
- Customers pay monthly in advance by ACH.
- Direct costs are small software tools. The real cost is staff labour.

**Why it is attractive for this founder.**
- **Low capital:** no inventory, no licence, cash collected at or before service.
- **Durable:** demand rests on statutes and on surety practice, not on fashion.
- **Delegable:** standard bookkeeping and payroll-clerk roles.
- **Sticky:** WIP history and monthly filing cadence are painful to move mid-project.
- **Easy to find buyers:** public award lists name them.

---

## 2. Commercial entry

### 2.1 Initial niche (refined in Stage E)
**Target:** Chicagoland (Cook, DuPage, Will and Kane counties) specialty subcontractors and small primes with $2–15M revenue who are **graduating past express bonding**.

**Why the line sits at about $500k:**
- Bonds for small contracts barely need financial reporting. SBA's Quick Bond covers contracts up to $500,000 [A, E-SYN006-S006] with "minimal paperwork" and approval in about a day [A, E-SYN006-S007]. Western National's ContractXpress, also up to $500,000, underwrites on a one-page application and personal credit [B, E-SYN006-S005].
- Above that, the same carrier's Xpress Xtra (up to $1.5M) needs business statements plus a WIP schedule. Larger standard programs also expect CPA-prepared statements [B, E-SYN006-S004/S005].
- So the buyer with acute WIP pain is the sub bidding single jobs above about $500k, or carrying about $1–5M of bonded backlog.

**Correction (Stage E):** Stage D framed the niche as "subs newly winning public work". Many first-time public-works subs on small jobs need certified payroll but **not** a WIP. Pitch WIP only to firms bidding above roughly $500k. Offer certified payroll as the entry service to the rest.

**Entry segments, in priority order:**
1. **City of Chicago lead-service-line replacement (LSLR) primes and subs.**
   - Chicago has 400,000+ lead service lines and replaced about 15,000 in 2021–2025 [C, E-SYN006-S012], so the work runs for decades.
   - September 2026 brought a new tranche of IEPA SRF block-level awards to United Enterprise (3), Advanced Water Solutions (2) and Millennium Contracting (2) [A, E-SYN006-S019].
2. **Job-order-contract (JOC) holders.** Many short work orders mean many per-project filings, e.g., 2026 Department of Water Management (DWM) and Chicago Department of Transportation (CDOT) JOCs [A, E-SYN006-S019].
3. **Small Business Initiative (SBI) awardees.**
4. **Illinois-based federal specialty subs** who need WH-347 weekly payroll support. Davis-Bacon-only contracts do not file with IDOL [A, E-SYN006-S002; A, DB-S019].

### 2.2 Named suppliers, tools and partners
| Organization | Role | Known terms | Level |
|---|---|---|---|
| IDOL Certified Transcript of Payroll portal | Mandatory filing channel | Free; one log-in per company; per-project Excel template | A, E-SYN006-S002 |
| Intuit QuickBooks Online / ProAdvisor | Client ledger; firm access | ProAdvisor "sign up for free"; firm gets QBO Advanced free [B, E-SYN006-S021]; QBO itself is client-paid | B |
| QuickBooks Payroll / ADP RUN / Gusto | Client payroll of record (not us) | QB Payroll from $50 + $7 per employee [B, C5-S010] | B |
| PaidReady | WH-347 software if the client needs it | $49/month for 5 projects; $99/month for 25 [B, DB-S021] | B |
| LCPtracker (LCPcertified) | Client-side certified payroll; owner systems (e.g., PBC) | $12/report or $145/month for 5 projects; licensed **per organization**; no IDOL export listed [B, E-SYN006-S010] | B |
| Knowify / WIP tools | Optional client job-costing tools | Knowify Advanced $329–399/month [B, DB-S035]; WIP tools $20–70/month [D, C5-S036] | B/D |
| Anthropic Claude Team | AI review layer | $25/seat/month (monthly billing) [B, DB-S022] | B |
| Insureon / NEXT Insurance | E&O, cyber, GL/BOP quotes | Bookkeeper medians: E&O $37/month, cyber $47/month [D, E-SYN006-S008] | D |
| CFMA Chicago | Channel to construction controllers, CPAs, sureties | Associate dues $500/yr; 290+ members from 200+ firms [B, E-SYN006-S011] | B |
| ASA Chicago; Federation of Women Contractors | Channels to sub owners | Dues MISSING | C |
| The Horton Group (Orland Park); Arthur J. Gallagher Surety (Rolling Meadows) | Surety brokers; referral sources | NASBP member [B, DB-S027]; referral behaviour MISSING | B/D |
| SBA Surety Bond Guarantee | Client enabler | Contracts up to $9M non-federal / $14M federal; fee 0.729% [A, E-SYN006-S003] | A |
| Porte Brown LLC; Wipfli LLP | Construction CPAs: referral partners and top-end competitors | Prices not published [B, DB-S023; C, DB-S026] | B/C |

**Correction (Stage E): firm-level certified-payroll software.** Stage D modelled a firm-level LCPcertified licence covering many clients at $210/month. LCPtracker describes the product as reporting "for an individual organization" [B, E-SYN006-S010].
- The firm will instead build IDOL-template tooling in-house, on IDOL's free fixed-column template [A, C5-S017], at about $75/month modelled.
- Clients needing software (WH-347, or owner-mandated LCPtracker) keep it in their own name.

### 2.3 Top 15 named prospects (all "prospect — not contacted"; full list of 36 in CSV)
| # | Organization | Why now | Source |
|---|---|---|---|
| 1 | United Enterprise LLC (Brookfield) | Three SRF block-level LSLR awards on 2026-09-01 ($1.26M, $3.78M, $4.12M) plus earlier drain and LSLR POs. High per-project filing volume | A, E-SYN006-S019 |
| 2 | Advanced Water Solutions LLC (Chicago) | LSLR award Dec 2025 ($529k), then two SRF awards Sept 2026 ($2.35M, $3.13M). Growing fast; bonded | A, E-SYN006-S019 |
| 3 | Millennium Contracting Corp. (Chicago) | Two SRF LSLR awards Sept 2026 (~$2.7M each), adding to a ~$28M history | A, E-SYN006-S019 |
| 4 | Ryans Plumbing 1 Inc (Dolton) | Two SBI II block LSLR POs Dec 2025 (~$564k total). A small firm entering bonded City work | A, DB-S018 |
| 5 | SWR Joint Venture (Chicago) | SBI II LSLR $577,550 (Nov 2025). JV reporting adds complexity | A, E-SYN006-S019 |
| 6 | Plumbing Professionals Co (Morris) | Daycare LSLR term agreement (~$32.5M ceiling): many small sites, years of filings | A, DB-S018 |
| 7 | Courtesy Electric Inc (Chicago) | Midway SBI lighting $3.26M (Jul 2026) plus O'Hare Ring Tunnel electrical $6.74M (Feb 2026). Bond capacity growing | A, E-SYN006-S019 |
| 8 | Tiles in Style LLC dba Taza Supplies (Naperville) | Two DWM JOC secondary awards Sept 2026 ($15M ceilings). New JOC holder: many work orders | A, E-SYN006-S019 |
| 9 | Ashlaur Construction Co. (Chicago/Lombard) | CDOT 2026 flatwork JOC rebid (Nov 2026; $30M ceiling) | A, E-SYN006-S019 |
| 10 | City Lights, Ltd. (Chicago Ridge) | City JOC for underground trenching: many short prevailing-wage jobs | A, DB-S018 |
| 11 | CSI 3000 Inc (Cicero) | MBE site contractor on the CDOT structures JOC: equipment-heavy job costing | A, DB-S018 |
| 12 | GMA Construction Group (Chicago) | Assets, Information and Services (AIS) department JOC (Sept 2024): per-work-order filings | A, DB-S018 |
| 13 | Industria Inc (Des Plaines) | Navy roof $8.26M (WH-347 weekly), DBE; also on IDOT/City work | A, DB-S019 |
| 14 | Troop Contracting Inc (Willowbrook) | VA Hines demolition $1.59M, service-disabled-veteran-owned (SDVOSB): WH-347 plus WIP | A, DB-S019 |
| 15 | CCS–Nu Veterans JV LLC (Chicago) | Combustion-control maintenance award $3.40M (Aug 2026). JV job costing | A, E-SYN006-S019 |

**How to use the list.** City data names **primes only**; subcontractors are not listed [A, E-SYN006-S019].
- Each prime is both a prospect and a channel. A prime cannot close out pay applications until its subs' certified payrolls are in.
- So ask every prime: "Which of your subs struggle with certified payroll or bonding paperwork?"
- Only 49 distinct vendors won City construction, JOC or work-service awards in about 13 months [A, E-SYN006-S019]. City primes alone are too few to build 40 clients; the sub tier and referrals must do most of the work.

### 2.4 Named competitors
| Competitor | Offer | Our position |
|---|---|---|
| Construction CPA firms (Porte Brown, Wipfli, local practitioners) | Full service including review/audit; WIP | They are often too expensive for sub-$5M monthly bookkeeping. We feed them clean books, so treat them as referral partners. |
| Remote Books Online (national) | Lists specialty sub $500–1,000/month and GC with WIP $900–1,800 [D, C5-S009]; its Chicago pages say $150–300 [D, DB-S029] | Local, public-works-specific, with certified payroll included |
| Bench / Pilot / Digits / Intuit QuickBooks Live | $65–$999/month; AI-led; no WIP [B, C5-S003/S004/S005]; Intuit is building AI agents for done-for-you work [A, C5-S008] | Do not compete on price. Compete on WIP, retainage and prevailing wage. |
| 24 Hour Bookkeeper; Wishup | Remote construction bookkeeping; Wishup "construction-trained" bookkeeper from $999/month [D, DB-S024; D, C5-S035] | Illinois prevailing-wage depth; surety relationships |
| ADP + Points North; Dapt; LCPcertified; PaidReady | Certified-payroll **software**: $145/month (LCP), $175–375/month + $7.50/report (Points North), $8,000/yr for 1–5 jobs (Dapt on ADP Workforce Now) [B, E-SYN006-S010/S013; B, C5-S013; D, E-SYN006-S023] | We do the labour. The software price shows what buyers already spend: $1,750–$8,000 a year for tools alone. |
| In-house office manager; GC filing for the sub | Free or sunk cost | Our entry point is when that person quits, or when a GC holds payment. |

### 2.5 Positioning
> "The back office that keeps a public-works sub bondable and paid: books closed by the 10th, a WIP your surety accepts, and certified payroll filed on time on every job."

Proof points to build:
- WIP samples reviewed by an experienced construction controller;
- zero late filings;
- a two-page "surety package" format agreed with two named surety producers.

### 2.6 Pricing (E/D; validate)
| Tier | Scope | Price |
|---|---|---|
| WIP & Surety-Readiness Check (validation offer) | Read-only review of the client's QBO file and job list. Delivers a rebuilt current WIP, a list of gaps versus a surety packet, and a 30-minute call | **$450 one-time** |
| Core | Monthly accrual close by day 10 plus a job-cost report | $750/month |
| Surety-ready | Core plus a quarterly WIP (over/under-billings, retainage) and a surety interim package | $1,100/month |
| Public-works | Surety-ready plus certified payroll for up to 2 IDOL projects, a fringe reconciliation and an audit binder | $1,400/month; +$125 per extra active project |
| Certified payroll (entry) | Preparation for 1 project, client submits | $300/month while the job is active |
| Clean-up / bond-graduation | Rebuild 6–12 months, cost codes, opening WIP, interim statement | $1,500–3,000 one-time, 50% upfront |

**Anchors:**
- Bench's accrual tier is $699/month [B, C5-S003].
- Vertical construction bookkeepers list $500–1,800 [D, C5-S009].
- Certified-payroll software alone costs $145–667/month [B, E-SYN006-S010/S013].

**Rules:**
- No hourly billing.
- Annual prepay at 10% off.
- The model blends to $1,000 ARPC: about 40% of clients carry certified payroll for about 9.5 months a year.

### 2.7 Sales and acquisition strategy
1. **Surety producers first.** They see every failed WIP. Ask eight of them "which clients struggle to give you a current WIP?" This tests the gap and opens the best referral channel.
   - Start with Horton and Gallagher [B, DB-S027]. Then find others through NASBP and SBA's directory of authorized surety agencies [A, E-SYN006-S003].
2. **Award-triggered letters.** Within 2 weeks of each new City, PBC or federal award, send a letter and make a call that cites the award. Offer the $450 check, or a free first month of certified payroll on the new job.
3. **Construction CPAs.** Five firms. Offer "we produce monthly books and WIPs your review team can rely on". Ask for sub-$5M clients they do not want to keep books for.
4. **Associations.**
   - CFMA Chicago as an associate ($500/yr) [B, E-SYN006-S011], but only after a paid-check gate.
   - ASA Chicago and FWC events.
5. **Referrals.** Ask every client after its first WIP or first clean filing month.

**Funnel (model base, E):** 12 qualified owner conversations a month → 35% reach a proposal → 30% win. That is about 1.26 new clients a month at full pace, plus 1.5 referrals per 100 active clients a month.

---

## 3. Transaction economics
All monthly unless stated. Labour is at loaded rates:
- bookkeeper $34/h ($5,800/month);
- senior reviewer $55/h;
- compliance specialist $33/h.

Source: the model's `transactions` [E prices within D bands].

**A. Public-works specialty sub** ($4M revenue, 25 employees, 2 active IDOL projects): Public-works tier.
| Line | $ |
|---|---|
| Revenue: close + job cost + quarterly WIP + certified payroll for 2 projects | 1,250 |
| Bookkeeper, 9 h | −306 |
| Senior review, 1.5 h | −83 |
| Compliance specialist, 3 h (2 projects × 4–5 weekly payrolls mapped to class and county rate) | −99 |
| Certified-payroll tooling share (2 projects) | −58 |
| WIP tool + document capture | −45 |
| **Contribution** | **659 (52.7%)** |

- **Cash timing:** billed on the 1st by ACH, in advance. Labour is paid biweekly, so there is no working-capital drag.
- **Failure risks:**
  - a mis-mapped classification causes back wages (20% penalty to IDOL on underpayments [A, C5-S015]);
  - a late filing exposes the filer if we are the "agent";
  - the project ends and the certified-payroll revenue drops.
- **Repeat:** monthly; plus each new public award.

**B. Small sub without public work** ($1.2M revenue, 8 employees): Core with a semiannual WIP.
| Line | $ |
|---|---|
| Revenue | 750 |
| Bookkeeper, 6 h | −204 |
| Senior review, 0.75 h | −41 |
| Tools | −35 |
| **Contribution** | **470 (62.7%)** |

- **Risks:** price comparison with Bench's $699 tier; churn if the owner sees no bonding benefit.
- **Repeat:** monthly. Upsell to Surety-ready when the first job above $500k is bid.

**C. Onboarding / bond-graduation project** (one-time).
| Line | $ |
|---|---|
| Revenue: rebuild 6 months, cost codes, opening WIP, interim statement | 2,000 |
| Bookkeeper, 20 h | −680 |
| Senior review, 4 h | −220 |
| Setup and migration | −60 |
| **Contribution** | **1,040 (52%)** |

- **Cash timing:** 50% upfront, 50% on delivery.
- **Risks:** scope creep, and books worse than quoted. Mitigate with a paid diagnostic first.
- **Trigger:** a surety asking for a current interim and WIP. For a December year-end contractor, the year-end statement passes six months old around July [B, E-SYN006-S004].

**D. Certified-payroll-only client** (1 project, about 9 months a year).
| Line | $ |
|---|---|
| Revenue | 300 |
| Specialist, 2.5 h | −83 |
| Tooling | −54 |
| **Contribution** | **163 (54%)** |

Low ticket and seasonal. It is an entry wedge, not a business (Stage C finding stands).

**E. Validation check** ($450 one-time, E).
| Line | $ |
|---|---|
| Revenue | 450 |
| Founder 4 h (shadow-priced at bookkeeper cost) | −144 |
| External reviewer 1 h (rate MISSING; assume ~$100) | −100 |
| **Contribution** | **~206** |

Its purpose is information, not profit.

**Unit economics at steady state (model base):**
- A client contributes about $880 a month after direct tools (88% gross margin).
- Fully loaded staff runs at about 63% of revenue in year 5.
- So operating margin before owner pay is about 21% (year-5 operating profit $181,482 on revenue $874,090).
- Labour productivity is the profit lever. A bookkeeper covering 12 instead of 15 clients is roughly the "hires 30% sooner" stress (year-3 operating profit **−$22,178**).

---

## 4. Validation

### 4.1 Minimum viable commercial offering
The **$450 WIP & Surety-Readiness Check**, delivered from read-only QBO access plus the client's job list and contracts.
- Output: a rebuilt WIP in the Work-on-Hand column format, a gap list versus a surety packet, and the next steps.
- Then offer the monthly Surety-ready or Public-works tier.
- In parallel, offer **certified-payroll preparation**: first month free on one new project, then $300/month.

### 4.2 Experiments, ordered by information value per dollar
| # | Test | Cost | Success | Kill / pivot |
|---|---|---|---|---|
| 1 | **Surety-producer interviews** (8: Horton, Gallagher and 6 more from NASBP/SBA directories). Ask past-behaviour questions: how many submissions last quarter lacked a usable WIP or interim, and who fixed them | $0 | ≥4 of 8 name recent cases. ≥3 agree to introduce a named client after seeing a sample | 0–1 see a gap → the WIP thesis is weak; pivot to certified payroll plus CPA outsourcing (test 6) |
| 2 | **Owner discovery calls** (20 from the CSV and producer intros), using the questionnaire in the materials | ≤$100 (mail, travel) | ≥6 of 20 had a surety or bank WIP/interim request in the last 12 months. ≥5 now spend ≥$700/month on bookkeeping, payroll admin or an in-house person | <3 recent requests and <3 spending ≥$700 |
| 3 | **Skill gate.** The founder builds 2 WIPs and 1 IDOL certified payroll from anonymized or sample data. An experienced construction controller or CPA reviews them for a fee | ~$500 | No material errors in the second attempt | Material errors twice → hire a senior reviewer before selling, or stop |
| 4 | **Paid $450 checks** offered to 40 prospects (letters plus calls) and producer intros | ~$300 | ≥3 paid within 60 days | ≤1 paid |
| 5 | **Monthly conversion** of completed checks | $0 | ≥2 signed at ≥$900/month by day 90 | 0 signed after ≥3 checks |
| 6 | **CPA-firm channel** (5 construction CPAs): would they refer, or subcontract monthly WIP prep? | $0 | ≥1 referral or one white-label trial | None interested (not a kill alone) |
| 7 | **Certified-payroll trial** on fresh LSLR, JOC and SBI awards | ~$100 | ≥4 paying by month 2 | <2 → keep it only as an add-on |

**Total validation budget:** about **$1,000**, plus founder time. The LLC ($150) and assumed name ($120 in 2026) [A, E-SYN006-S014] are needed only before the first paid check. E&O must be bound before any client data is touched.

### 4.3 Supplier and partner qualification steps
- **IDOL:** confirm in writing how an outside preparer may work. Options: the client grants its own account, the client submits after our preparation, or a firm user under the client's company log-in [A, E-SYN006-S002 is silent].
- **E&O/cyber:** get 2–3 quotes. Confirm cover for certified-payroll preparation and for SB1344 penalties (often excluded).
- **QBO ProAdvisor:** sign up; confirm firm access and client-billing options [B, E-SYN006-S021].
- **Surety producers:** obtain their preferred WIP and interim formats. Ask whether they accept company-prepared statements below their CPA thresholds.

### 4.4 Testable assumptions (model drivers)
- ARPC $1,000 (D).
- 12 conversations a month, 35% to proposal, 30% win (E).
- Churn 1.6% a month (C, incumbent proxy).
- 15 clients per bookkeeper, 45 per senior reviewer, 60 per compliance specialist (E).
- One-time revenue $1,500 (E).
- DSO 8 days (D).

### 4.5 Conditions to invest more
- Tests 1, 2, 4 and 5 pass.
- Hours per client stay at or under 10 a month after month 3.
- Then bind E&O, form the LLC and join CFMA.
- Hire the first bookkeeper only at **≥11 active clients** with founder hours above 55 a week.

### 4.6 Conditions to abandon or pivot
- **Abandon:** tests 1 and 2 both fail, or the skill gate fails twice.
- **Pivot A: certified-payroll compliance desk.** If owners want certified payroll but not books: sell to payroll bureaus and CPA firms as subcontract labour, priced per project. Accept the ~$50k ceiling of WS15-023 unless volume proves otherwise.
- **Pivot B: white-label WIP preparation for construction CPA firms.** If producers say CPAs already handle WIP.

---

## 5. Operations

### 5.1 Lead-to-cash workflow and function classification
| Step | Function | Class |
|---|---|---|
| 1 | Award monitoring (City Socrata API, USASpending, PBC) → CRM | **Automatable** (script) |
| 2 | Letter and call citing the award; producer and CPA relationship work | **Human** |
| 3 | Discovery call; read-only QBO review | **Human**, with AI summarizing the chart of accounts and job list |
| 4 | Proposal and engagement letter (scope; classifications approved by the client; client certifies and submits) | **AI-assisted** draft; **professional-dependent** template (attorney review once) |
| 5 | Onboarding: cost codes, retainage accounts, opening WIP | **Human** judgment, AI-assisted reconciliation |
| 6 | Monthly close: bank feeds, categorization, accruals, retainage, committed costs | **AI-assisted** categorization; **human** accruals and review |
| 7 | WIP: estimates to complete from the client's project manager | **Not automatable**. The estimate is the client's judgment; we challenge it and document it |
| 8 | Certified payroll: export payroll → map hours to project, classification and county rate → IDOL template → client approval → submission by the 15th | **Automatable** template fill; **AI-assisted** rate check against IDOL county rate PDFs [A, DB-S004]; **human** sign-off |
| 9 | Senior review / external QA | **Human** (skilled) |
| 10 | Invoice on the 1st by ACH; dunning | **Automatable** |
| 11 | Year-end package to the client's CPA; responses to surety questions | **Human**, AI-assisted |
| 12 | Exceptions: IDOL notices, GC holds, surety queries | **Human**, escalated to the client's attorney when legal |

### 5.2 Fulfillment, support, quality assurance and exceptions
- **Calendar:** close by day 10; certified payroll prepared by day 10 and submitted by the client by day 12. Keep a buffer: prior-month payrolls cannot be withdrawn after the 15th [A, E-SYN006-S002].
- **Quality assurance:**
  - maker-checker on every WIP;
  - a quarter-over-quarter WIP revision check (flag above 10%);
  - a 100% rate check on the first month of each new project.
- **Support:** one named bookkeeper per client, and a shared inbox.
- **Exception log** reviewed weekly.

### 5.3 Software stack and prices
| Item | Price | Who pays |
|---|---|---|
| QuickBooks Online | Client subscription (price not re-verified) | Client |
| QBO Accountant / ProAdvisor | Free sign-up [B, E-SYN006-S021] | Firm |
| Claude Team | $25/seat/month [B, DB-S022] | Firm |
| IDOL portal and template | Free [A] | — |
| Certified-payroll tooling (in-house template automation, secure portal) | ~$75/month modelled (E) | Firm |
| Practice management, e-sign, document capture | ~$300/month modelled including AI seats (E) | Firm |
| PaidReady / LCPtracker | $49–145/month [B] | Client, where needed |

### 5.4 Legal requirements
1. **Entity:** Illinois LLC ($150), assumed name ($120 in 2026), annual report $75 [A, E-SYN006-S014].
2. **Accounting Act:**
   - bookkeeping, compilations and accounting services are not CPA-restricted [A, E-SYN006-S024];
   - assurance or opinion reports and other attest work are [A, DB-S016];
   - never use "CPA", "public accountant" or similar terms (civil penalty up to $10,000 per offense) [A, DB-S015];
   - avoid "accountant" in the firm name pending legal review.
3. **Policy:** issue company-prepared statements only, and no compilation reports at launch. Many sureties want CPA-prepared statements above their express tiers, so we are the CPA's input, not a substitute.
4. **Certified payroll:**
   - the client approves worker classifications;
   - the client certifies and preferably clicks submit, because SB1344 penalties reach the agent whose job is to file [C, E-SYN006-S001];
   - give no legal opinions on classification;
   - keep records 5 years [A, C5-S014].
5. **Federal work:** prepare WH-347s; do not file with IDOL [A, E-SYN006-S002].
6. **Payroll processing:** none at launch. The client's platform holds tax impounds (avoids WS02-026 fiduciary risk).
7. **Tax preparation:** none (refer it to CPAs).
8. **Insurance:**
   - E&O plus cyber modelled at $275/month. The Insureon bookkeeper floor is about $84/month [D, E-SYN006-S008]. The certified-payroll risk class needs real quotes.
   - GL/BOP about $29–45/month [D].
9. **Data security:** a written information-security plan; MFA everywhere; no client credentials in email. FTC Safeguards Rule applicability to a non-tax bookkeeper is MISSING; ask counsel.

### 5.5 Financial administration
- Separate operating and tax-reserve bank accounts.
- Our own books are kept by us and reviewed by an outside CPA at year end.
- Collect by ACH only, with prepay preferred.
- Monthly KPI pack (see the materials).

### 5.6 After Dec-2026: AI cost and fallback
- **What AI does:** categorization review, variance commentary, rate lookups, drafts.
- **Cost:** about $25/seat/month [B, DB-S022]. Even ×3, base year-3 operating profit only falls to **$85,186** (stress).
- **Fallback:** every workflow is a spreadsheet template plus human time. Nothing requires unlimited AI.
- **Before 5 Dec 2026:** build the durable assets (WIP workbook, IDOL mapper, SOPs, letter library) while heavy access lasts.

---

## 6. Growth

### 6.1 First 10 customers
- **Months 1–3:** 3–5 paid checks from producer intros and award letters. Convert 2.
- **Months 4–12:** about 1.3 new clients a month (model base). Year-1 end is **9.4 active clients** (base).
- **Source mix:** surety producers > award letters > CPA referrals.
- The founder does all production and uses the external reviewer for QA.

### 6.2 First 100 customers
- The model base reaches **39.1 clients by year 3, 53.7 by year 4 and 68.1 by year 5**. It does not reach 100 within 60 months; the optimistic case reaches 101.5 in year 4.
- Getting to 100 needs:
  - a referral engine (sureties, CPAs and primes' sub lists);
  - federal WH-347 work beyond Chicagoland;
  - possibly a second sales person.

### 6.3 Hiring sequence (model triggers)
| Hire | Trigger | Loaded cost | Productivity |
|---|---|---|---|
| External construction-accounting reviewer (part-time) | Month 3 | $600/month base ($1,200 conservative), E | 5–8 h/month QA |
| Bookkeeper #1 | ≥12 active clients (month 16 in base) | $5,800/month (BLS construction median $54,890 [C, E-SYN006-S009] + burden) | 15 clients |
| Payroll/prevailing-wage specialist | ≥25 clients | $5,500/month | 60 clients |
| Senior construction accountant/reviewer | ≥30 clients | $8,500/month | 45 clients (max 2) |
| Office/admin coordinator | Monthly revenue ≥$60k | $4,200/month | Billing, onboarding |
| Further bookkeepers | Every +15 clients | $5,800/month | 15 clients |

**Staffing path:** headcount at year-end is 1, 2, 5, 7 and 8 in years 1–5 (base, counting the reviewer).

**Why year 3 dips:** base year-2 operating profit **$124,997** is higher than year 3's **$94,734**. In year 2 the founder is still doing unpaid production, review and compliance. Price that founder labour and year 2 would be roughly $45–90k lower: about $45k at the hourly rates in §3, about $90k at full-time-hire cost. Year 3 is the first honest "staffed" year.

### 6.4 Capacity limits
- The founder: about 200 h/month in months 10–24 (production for about 12 clients + sales + review).
- About 15 clients per bookkeeper.
- The certified-payroll deadline (the 15th) concentrates the workload into days 1–12 of each month.
- The real ceiling is senior-review capacity and founder selling hours.

### 6.5 Geographic expansion
- **First:** Illinois statewide (IDOL is statewide). Federal WH-347 work nationally, remotely.
- **Then:** another state's public-works regime only after Illinois exceeds 50 clients. Each state's rules need new research (not done).

### 6.6 Adjacent products and the two named adjacencies
| Adjacency | Incremental logic | Verdict |
|---|---|---|
| **Construction stormwater inspections (WS11-021)** | Different buyer (site/civil GCs, homebuilders and public owners in ECHO vs our specialty subs); field labour and storm-driven scheduling; DSO 45 vs 8. WS11-021's Stage D model: base year-3 op $53,554, year-5 $52,486, peak funding $52,267; conservative peak $185,596. That is about $1 of capital per $1 of annual profit, versus about $0.11 here | **Do not bundle.** Use a reciprocal referral with an inspector firm. Revisit only after year 3, if ≥5 site/civil clients ask for it |
| **Surety/insurance referral income: (a) unpaid reciprocal referrals** | Producers send WIP-deficient clients; we send clients needing bonds | **Do from day 1** |
| **(b) Paid referral fees from producers** | 215 ILCS 5/500-80(d) lets producers pay persons who do not sell, solicit or negotiate insurance, unless it violates §151 (not read) [A, E-SYN006-S015]. But it compromises the independence of books a surety relies on | **Decline in years 1–2.** If ever accepted: written client disclosure plus counsel sign-off |
| **(c) A licensed surety/insurance affiliate** | P&C producer licence (20 h per line, $215) [A, WS02-S001/S002]. Which line covers surety is MISSING (500-35 names none [A, E-SYN006-S016]). Premium example: a $1M Class B job at basic rates is about $20,000; at standard, about $13,500 [B, E-SYN006-S005]. **Producer commission % MISSING.** Carrier/MGA access for a new producer is unverified | **Option at the year-2 gate** (≥30 bonded clients), in a separate entity. Upside is E-level and not in the model |
| Illinois Works / M/WBE / PBC LCPtracker / residency reporting | Same data, more reports [A, E-SYN006-S017; B, E-SYN006-S018]; +$100–200 per project-month (E) | Add in year 1 as a line item |
| Payroll administration on the client's platform (WS02-026) | About +$250/client-month margin with no new CAC (Stage C, E). The platform holds the impound | Year 2, if ≥30% of clients ask |
| Lien-deadline calendar (WS10-004) | Deadline tracking only; notices and liens go through the client's attorney. UPL exposure documented even for Procore/Levelset [A, C5-S030] | Calendar feature only; no fees from attorneys |

### 6.7 Vertical integration
- **Internal IDOL-template generator and rate library.** Built in-house for about $0 cash before 5 Dec. It returns labour hours: −1 h per report on about 40% of clients is about 4% of bookkeeper capacity at 40 clients.
- **Productizing it as software:** not before year 3. It would compete with $145/month tools [B].

### 6.8 Management delegation
- At about 45–60 clients (year 4 base), the senior construction accountant becomes the operations lead. The founder moves to sales, partnerships and QA sampling.
- Full day-to-day delegation needs a controller-level manager at about 70+ clients (year 5+). That role is not in the model; budget roughly $100k+ loaded (E).

### 6.9 Reinvestment slots
- More bookkeeper pods (each about $70k/yr of cost against about $180k of revenue at 15 × $1,000).
- A sales hire.
- A federal WH-347 remote desk.
- The licensed surety affiliate.
- Acquiring small bookkeeping books in later years (acquisitions are allowed later, not as entry).

---

## 7. Financial analysis (rebuilt model; figures quoted from `_results.json`)

**Stage E standardization:** owner draw $4,000/month from month 13 in all scenarios; tax 30%; start capital $10,000 (the smallest base-case injection keeping cash ≥ 0; base minimum cash is $21 in month 5).

**Corrections vs Stage D:**
- owner draw raised from $3,000 to $4,000;
- a part-time external reviewer added ($600/month base);
- firm-level certified-payroll licence replaced with in-house tooling;
- E&O range widened ($175 / $275 / $450);
- conservative churn raised to 2.5%/month and conservative DSO to 30 days;
- conservative bookkeeper cost raised to $6,400;
- long-term drivers now scenario-specific and evidenced.

**Effect:** base year-3 operating profit moves from Stage D's **$101k to $94,734**; year 5 from **$188k to $181,482**.

### 7.1 Launch capital and working capital
- **Base:** peak funding **$9,979** (identical with no draw, because the trough is in month 5, before the draw starts).
- **Conservative:** peak funding **$145,953** with the $4k draw, **$37,825** without it.
- **Optimistic:** **$5,816**.
- **Working capital is negligible** at DSO 8: change in NWC is $2,292 in year 1 and $3,790 in year 5 (base). Even "customers pay 30 days later" raises base peak funding only to **$13,271**.
- The cash risk is **payroll ahead of clients**, not receivables.

### 7.2 24-month monthly view (base)
| Month | Active clients | Revenue | Op. profit | Cash (after draw) |
|---|---|---|---|---|
| 1 | 0.0 | $0 | −$1,525 | $5,475 |
| 2 | 0.0 | $0 | −$1,525 | $3,950 |
| 3 | 0.2 | $525 | −$1,746 | $2,108 |
| 4 | 0.6 | $1,265 | −$1,256 | $712 |
| 5 | 1.3 | $2,218 | −$507 | $21 |
| 6 | 2.1 | $3,386 | $428 | $221 |
| 7 | 3.1 | $4,768 | $1,548 | $1,497 |
| 8 | 4.4 | $6,363 | $2,853 | $4,033 |
| 9 | 5.7 | $7,647 | $3,963 | $7,062 |
| 10 | 6.9 | $8,930 | $5,071 | $10,348 |
| 11 | 8.2 | $10,211 | $6,179 | $14,410 |
| 12 | 9.4 | $11,491 | $7,286 | $19,246 |
| 13 | 10.7 | $13,153 | $8,660 | $22,169 |
| 14 | 11.9 | $14,469 | $9,798 | $25,956 |
| 15 | 13.2 | $15,783 | $10,935 | $30,540 |
| 16 | 14.4 | $17,097 | $6,096 (bookkeeper #1 hired) | $29,737 |
| 17 | 15.7 | $18,408 | $7,230 | $31,728 |
| 18 | 16.9 | $19,719 | $8,363 | $34,513 |
| 19 | 18.1 | $21,028 | $9,496 | $38,090 |
| 20 | 19.4 | $22,336 | $10,626 | $42,460 |
| 21 | 20.6 | $23,643 | $11,756 | $47,620 |
| 22 | 21.9 | $24,948 | $12,885 | $53,571 |
| 23 | 23.1 | $26,252 | $14,012 | $60,311 |
| 24 | 24.3 | $27,555 | $15,139 | $67,841 |

The ramp in months 1–15 rests on unpaid founder production. The model starts the draw at month 13; the founder is working about 45–50 h a week on production and sales.

### 7.3 Five-year annual summary
| | Y1 | Y2 | Y3 | Y4 | Y5 |
|---|---|---|---|---|---|
| **Base:** revenue | $56,805 | $244,391 | $444,747 | $654,533 | $874,090 |
| Base: operating profit | $20,769 | $124,997 | $94,734 | $134,607 | $181,482 |
| Base: FCF (before draw) | $9,246 | $96,594 | $71,254 | $103,003 | $135,647 |
| Base: active clients (year end) | 9.4 | 24.3 | 39.1 | 53.7 | 68.1 |
| **Conservative:** operating profit | −$28,519 | $13,226 | $29,843 | $12,091 | $44,527 |
| Conservative: active clients | 3.5 | 9.1 | 13.8 | 17.7 | 21.0 |
| **Optimistic:** operating profit | $73,804 | $236,464 | $365,733 | $553,248 | $843,382 |
| Optimistic: active clients | 15.1 | 41.2 | 69.9 | 101.5 | 136.3 |

**Breakeven month:**
- base month 6 (payback month 10);
- conservative month 16, never paid back within 60 months;
- optimistic month 4.

**The optimistic case is not a plan.** It needs 16 conversations a month at 35% win, ARPC $1,200 and churn 1.2%, all E. Treat it as the upside bound.

### 7.4 Sensitivity (tornado, base, ±25%; year-3 operating profit)
| Driver | ×0.75 | ×1.25 | Comment |
|---|---|---|---|
| ARPC ($1,000) | **$5,173** | **$184,294** | Price is the #1 unknown (D). At ×0.75, peak funding rises to $72,512 |
| Gross margin (88%) | $4,144 | $185,324 | ×1.25 exceeds 100% and is not meaningful. The downside shows tool-cost creep risk |
| Labour cost | $160,775 | **$28,693** | Productivity per staff member is the #2 lever |
| Founder leads / win rate | $146,996 | $95,516 | Inverted: fewer clients mean fewer hires in year 3. Not a real benefit (see year 5 below) |
| One-time revenue | $88,221 | $101,246 | Minor |
| Churn, referrals, CAC, overhead, DSO | $92–98k | $92–98k | Minor in year 3 |

### 7.5 Stress tests (base; year-3 / year-5 operating profit; peak funding)
| Stress | Y3 | Y5 | Peak funding |
|---|---|---|---|
| CAC doubles | $84,753 | $170,189 | $12,712 |
| Win rate 40% below plan | $125,776 | $75,111 | $11,892 |
| Sales cycle doubles | $109,064 | $170,588 | $14,379 |
| Gross margin −5 pts | $72,496 | $137,777 | $10,124 |
| Gross margin −10 pts | $50,259 | $94,073 | $10,349 |
| Key supplier refuses (3-month delay, −5 pts) | $96,373 | $121,539 | $16,724 |
| Largest customers leave (25% in month 18) | $114,232 | $160,709 | $9,979 |
| Customers pay 30 days later | $94,734 | $181,482 | $13,271 |
| **Labour cost +20%** | **$41,901** | **$71,947** | $10,339 |
| Insurance/overhead +50% | $89,414 | $175,762 | $12,254 |
| AI/software ×3 | $85,186 | $171,352 | $13,829 |
| **Hires needed 30% sooner** | **−$22,178** | **−$107,211** | **$320,025** |
| Recession (new clients −30%, churn ×1.5) | $126,072 | $37,845 | $11,303 |
| Competitor response | $71,605 | $88,155 | $10,027 |
| Founder capacity 40% lower | $125,776 | $75,111 | $11,892 |
| Growth takes twice as long | $83,587 | $165,350 | $24,525 |

**How to read this:**
- **Read year 5, not year 3, for the demand stresses.** Lower demand delays hires, which flatters year 3. Recession cuts year 5 to **$37,845**; a 40% lower win rate cuts it to **$75,111**.
- **The killer is labour productivity.** If each bookkeeper handles 10.5 instead of 15 clients, the business loses money at every scale. The validation KPI "hours per client ≤10" exists to catch this.

### 7.6 Profit milestones (base)
- $1k/month operating profit: month 7.
- $5k/month: month 10.
- $10k/month: month 15.
- $25k/month: not reached within 60 months.
- $100k/yr: year 4 ($134,607; year 3 is $94,734).
- $250k/yr: not within 10 years in base (year 10 is $242,007).
- Conservative never reaches $10k/month. Optimistic reaches $25k/month in month 17.

### 7.7 Capital accumulation to year 10 and owner distributions
| Scenario | Cumulative deployable, Y5 | Cumulative deployable, Y10 | Y10 op. profit | Y10 EV | Owner draws, 10 yrs |
|---|---|---|---|---|---|
| Base | $123,493 | $578,447 | $242,007 | $605,019 (2.5×) | $454,484 |
| Conservative | $0 | $0 | $48,349 | $72,524 (1.5×) | $454,484 (unfunded: the business cannot pay it) |
| Optimistic | $1,070,698 | $4,326,973 | $1,347,109 | $4,714,882 (3.5×) | $454,484 |

**Base deployable surplus** after the draw, taxes, reserves and reinvestment:
- about $27–59k a year in years 4–5;
- about $73–107k a year in years 6–10.

**Long-term drivers:**
- **Growth in year 6:** 8% base (3% conservative / 12% optimistic), decaying at 0.85 (0.7 / 0.9).
- **Incremental ROIC:** 1.0 (0.5 / 1.5).
- **Maintenance capex:** 3% of operating profit (5% / 2%).
- **Reserve:** 2 months (3 conservative / 2 optimistic).
- **EV multiple** of operating profit before owner pay: 2.5× (1.5× / 3.5×). Anchors:
  - one Chicago-suburb owner-operated service listing asked about 3.2× SDE [D, DF-S004];
  - small insurance books trade at 5–7× profit [C, C5-S021];
  - agencies under $1M EBITDA trade at about 4× [C, WS02-S007].
  - Bookkeeping-practice multiples are MISSING.

### 7.8 Downside cases
- **Conservative is a kill case.** Year-5 operating profit is $44,527 on 21 clients, and $146k of cumulative funding is needed if the founder draws $4k a month.
- The decision rule is not "survive the conservative case". It is: **do not proceed past validation unless the evidence points to base-or-better on price and productivity.**

---

## 8. Capital deployment ladder
| Tranche | What it buys | Evidence gate before spending | How it could be lost |
|---|---|---|---|
| **$0–500** | Free IDOL template and rate PDFs; City/USASpending award pulls; QBO ProAdvisor sign-up; WIP workbook and IDOL mapper built with Claude before 5 Dec; postage for 40 letters (~$100) | None. This is preparation | Time only |
| **$500–2k** | Paid review of the founder's sample WIPs (~$500, E); LLC $150 + assumed name $120 [A]; engagement-letter legal review (MISSING, E); first E&O/cyber premium installment | Test 1 (≥4 of 8 producers see a gap) **and** test 2 (≥6 of 20 owners with recent WIP requests) | Skill gate fails; owners will not pay |
| **$2–5k** | Annual E&O/cyber (quotes needed); CFMA associate $500 [B]; laptop/monitors (~$3k modelled); event fees | ≥3 paid $450 checks | E&O claim; event spend without leads |
| **$5–10k** | Cash buffer for the month-1–6 trough (model start capital $10,000) | ≥2 monthly clients at ≥$900 | Slow conversion: the cash runs out in about month 5 if no clients sign |
| **$10–25k** | Bookkeeper #1 hired 1–3 months ahead (~$17k of payroll before full load) | ≥11 active clients; hours per client ≤10; churn ≤2%/month; founder above 55 h/week | Clients churn after the hire (Stage D $25k pre-mortem) |
| **$25–50k** | Compliance specialist and senior reviewer ahead of revenue; a sales or marketing push | ≥25 clients; ≥90% on-time filings; two producers referring regularly | Productivity below 12 clients per bookkeeper turns operating profit negative |
| **$50–100k** | Second pod; a federal WH-347 remote desk; or the licensed surety affiliate (separate entity) | Year-3 run-rate ≥40 clients and ≥$100k operating profit; counsel opinion on the conflict; producer commission terms verified | Expansion outside Illinois rules; commission dependence |

---

## 9. Strategic wealth creation
- **Durability:**
  - recurring monthly revenue paid in advance;
  - switching friction (WIP history, filing cadence);
  - statutory demand (Prevailing Wage Act, Bond Act);
  - Chicago LSLR work lasting decades [C, E-SYN006-S012].
- **Cyclicality:** construction downturns raise churn and reduce new awards (recession stress: year 5 at $37,845).
- **Capital generated:** base about $578k cumulative deployable over 10 years, plus $454k of owner draws, at about $242k operating profit in year 10. That is a solid small business, not a large one.
- **Management handover:** an operations lead at about year 4; a full manager at 70+ clients.
- **Funding other ventures:** at base, about $73–107k a year of deployable cash in years 6–10. That is enough to seed one or two later low-capital businesses or small acquisitions.
- **As a first company for a diversified holding company:**
  - **For:** almost no capital at risk (about $10k); cash-at-service; licence-free; teaches the founder SME finance and the construction ecosystem; creates relationships with sureties and CPAs that later acquisitions can use.
  - **Against:** the founder's skill gap; D-level prices; labour-productivity fragility; an Illinois-construction concentration; a roughly $250k/yr ceiling without multi-pod expansion.
  - **Conclusion:** a strong *low-risk* first company if validation shows ≥$900/month prices and ≤10 h per client. A weak one if the founder cannot become a credible construction accountant within about 6 months.

---

## 10. Execution plan

### 10.1 First 7 days (Mon 30 Nov – Sun 6 Dec 2026; heavy AI access ends 5 Dec)
**Founder:**
- Read the IDOL FAQ and template.
- Study the Work-on-Hand column logic.
- Draft the list of 8 surety producers (Horton, Gallagher, SBA directory, NASBP).
- Pick 20 owner-call targets from the CSV.
- Decide the firm name. Avoid "CPA", "public accountant" and probably "accountant".

**Claude prepares (durable assets):**
- WIP workbook (percent complete, over/under-billings, retainage, gross-profit fade);
- IDOL template mapper (payroll export → template columns; county-rate lookup from IDOL PDFs);
- engagement-letter draft (for attorney review);
- SOPs for close, WIP and certified payroll;
- award-monitoring script (City API);
- letter library;
- KPI sheet.

**Spend:** $0–100.

### 10.2 First 30 days
**Approach:**
- the 8 surety producers;
- 5 construction CPA firms (Porte Brown, Wipfli and 3 local firms found through the CFMA directory);
- 20 owners: LSLR and JOC primes first (United Enterprise, Advanced Water Solutions, Millennium, Ryans Plumbing 1, SWR JV, Taza Supplies, Ashlaur, City Lights).

**Questions to ask:** see the materials (past surety requests, who prepares the WIP, current spend, certified-payroll workflow, GC holds).

**Founder work:**
- Run skill gate #3 with a paid reviewer.
- Form the LLC.
- Get E&O quotes. Bind E&O before handling any client data.
- Collect producer WIP formats.

**Evidence required by day 30:** ≥8 producer conversations, ≥15 owner conversations, and the skill-gate result.

**Proposed spend:** ≤$1,000.

**Conditions:**
- **Accept a first paid check** only with: a signed engagement letter, read-only access, E&O bound and a reviewer lined up.
- **Abandon** if tests 1 and 2 both fail.

### 10.3 First 90 days
- 40 award-triggered letters.
- ≥3 paid checks (test 4); ≥2 monthly clients (test 5); a certified-payroll trial with ≥4 projects (test 7).
- Keep the first 2–3 clients on the founder's own production, with external QA.
- Measure hours per client, days to close, and filing timeliness.
- **Day-90 decision:**
  - **Continue** (the gates in §4.5);
  - **Pivot** A or B (§4.6);
  - **Stop.**

### 10.4 First year
| Milestone | Target (base) | Slow-growth branch | Failure branch |
|---|---|---|---|
| Month 6 | 2 active clients; operating-profit breakeven | 1 client → add the CPA white-label channel | 0 clients → stop |
| Month 9 | 5–6 clients; a 2-producer referral flow | 3 clients → raise outreach to 60 letters a month | — |
| Month 12 | 9–10 clients; ~$11.5k monthly revenue; first annual prepay | 5 clients → stay solo; no hire | Churn above 3%/month or any IDOL penalty attributable to us → stop and review |
| Month 15–16 | First bookkeeper (≥12 clients) | Delay the hire; raise prices on new clients | — |

---

## 11. Pre-mortem
| Scenario | How it happens | Early warning | Cheap preventive test |
|---|---|---|---|
| **Lost $5k** | Checks do not sell: "my CPA does it" or "the surety never asks" | <3 recent WIP requests in 20 owner calls; producers see no gap | Tests 1–2 before any spend |
| **Lost $25k** | Bookkeeper hired at 12 clients; 4 churn when a large job ends or a sub fails; at 10–11 clients per bookkeeper, margin vanishes | Hours per client above 10 after month 3; churn above 2%/month; client concentration above 15% of revenue | Track time per client from day 1; hire only at ≥11 clients plus a waiting list |
| **Lost $50k** | E&O event: a mis-mapped classification leads to back wages and penalties, the client blames the preparer; or a WIP error misleads a surety | Any IDOL notice; WIP revisions above 10% quarter over quarter; the client's PM refuses to give estimates to complete | Client-approved classifications; the client certifies and submits; maker-checker; E&O coverage confirmed for payroll preparation |
| **Revenue but no profit** | Underpricing ($500–700 tiers), scope creep, unbilled clean-ups | ARPC below $850; more than 15% of hours unbilled | Fixed-scope tiers; paid diagnostic first; annual repricing |
| **Exhausting low-paid job** | The founder becomes the bookkeeper for 12–15 clients at about 50 h/week, deadline-driven every month | Founder hours above 55/week for 8 weeks; no referrals | Price for staffing (each client must carry about $400 of labour); hire at ≥11 clients |
| **Cash crunch** | Payroll ahead of clients; contractors paying by check at net 30 | DSO above 15; cash below 1 month of payroll | ACH-only, billing on the 1st; annual prepay discount; hire only with 2 months' payroll in reserve |
| **Can't run without the founder** | The founder is the only senior reviewer and the only relationship holder | No second reviewer by 30 clients | Senior hire at 30 clients; documented SOPs; producer relationships shared with the operations lead |
| **No deployable surplus** | Stuck at about 20 clients (conservative path: year-5 op $44,527) | Fewer than 1 net new client a month after month 9 | Decide at month 12: grow channels or stop. Do not drift |

---

## 12. Required confirmations (direct contact needed; none performed)
1. **IDOL:**
   - Can an outside preparer work under the client's company log-in, or must the client submit?
   - Are SB1344 penalties applied to outside preparers who do not submit?
   - Obtain the enrolled text of P.A. 104-0023 (ilga.gov was unreachable) [C, E-SYN006-S001].
2. **Surety producers and underwriters:** at what bond size do they require CPA-compiled, reviewed or audited statements versus company-prepared statements plus a WIP? How current must interims be? Western National's 2016 chart says no CPA up to $1.5M [B, E-SYN006-S005]; confirm current practice.
3. **E&O/cyber carriers:**
   - premiums at $1M/$2M limits for "bookkeeping plus certified-payroll preparation";
   - exclusions for fines, penalties and debarment losses;
   - whether a construction class surcharge applies.
4. **Counsel (Illinois):**
   - firm name and title wording (Section 9);
   - engagement-letter liability caps;
   - whether preparing certified payroll is a regulated activity;
   - FTC Safeguards Rule applicability;
   - the 215 ILCS 5/500-80(d)/§151 referral-fee question.
5. **IDOI:** which line of authority covers surety bonds, if the licensed affiliate is ever pursued [A, E-SYN006-S016 shows none named].
6. **Customers:**
   - realized willingness to pay ≥$900/month;
   - the share of clients with public work;
   - typical hours per client (time-tracked).
7. **PBC / City departments:** current LCPtracker and B2GNow requirements for subs. The 2019 brochure is the latest seen [B, E-SYN006-S018].
8. **QBO ProAdvisor:** firm-billing terms and client discounts (percentages not shown) [B, E-SYN006-S021].
9. **Wages:** Chicago construction-bookkeeper pay. BLS metro tables were blocked; the May 2023 Chicago mean of about $52,890 is D-level only [D, E-SYN006-S022].

---

### Scores (Stage E; unchanged from Stage D)
| fcf | roic | access | scale | resilience | entry | delegation | cash | feasibility | ai |
|---|---|---|---|---|---|---|---|---|---|
| 5 | 8 | 5 | 5 | 6 | 5 | 6 | 8 | 8 | 5 |

- **Evidence D** (k = 0.70); raw 5.93; adjusted **5.65**.
- **Gates:** none (G4 not triggered: base reaches $134,607 in year 4).
- **Why no change:**
  - The surety-WIP evidence upgrade (D→B) strengthens `access` and `entry` slightly.
  - That is offset by the per-organization software correction and the lower conservative case.
  - Prices remain D.
