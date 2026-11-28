# SYN-006 — Construction subcontractor back office (Stage D deep dive, batch DB)

Absorbs WS02-028 (construction bookkeeping), WS15-023 (certified payroll) and WS02-026 (payroll, as a platform add-on only). Access date 2026-11-28. Model: `08_financial_models/SYN-006_assumptions.json` / `_model.xlsx` / `_results.json`. Prospects: `09_databases/prospects/SYN-006_prospects.csv` (31). Suppliers/partners: `09_databases/suppliers/SYN-006_suppliers.csv` (16). Sources: `05_deep_dives/sources_DB.jsonl` (DB-S0xx), plus earlier C5/WS02 sources.

> **Verdict: FINALIST (conditional).** This is a low-capital, customer-funded, delegable recurring service with a legal path confirmed at A level. Bookkeeping is "not restricted to licensed or registered CPAs" [A, DB-S014]. The model base case reaches **year-3 operating profit of about $101k** (revenue $445k, 39 clients) and **year-5 about $188k**, with **peak funding under $10k**. The weak links are evidence and skill, not capital:
> - Prices are D-level.
> - Conversion rates are E.
> - The founder must become a competent construction accountant before the first hire.
>
> It stays a finalist only if the validation plan (§13) produces paid WIP/clean-up engagements within about 60 days.

## 1. Specific initial niche
**Initial niche:**
- **Product:** a fixed-fee "surety-ready close" (accrual books, a job-cost report, and a quarterly WIP schedule with over/under-billings and retainage).
- **Add-on:** IDOL certified-payroll filing for each month with prevailing-wage work.
- **Customers:** Illinois specialty subcontractors with $1–20M revenue that are newly or repeatedly winning public work in Cook, DuPage, Will and Kane.
- **Entry segments:** City of Chicago lead-service-line replacement (LSLR), Small Business Initiative (SBI) and job-order-contract (JOC) holders, plus federal-work subs who need WH-347 support.

**Why these segments:**
- The mandate is monthly, per project, and carries filer liability [A, C5-S014; A, DB-S013; C, C5-S019].
- Bonds are required on Illinois public works over $150,000, and on IDOT/Tollway work over $500,000 [A, DB-S017]. The bond requirement is what pulls the WIP schedule into existence.

**Out of scope at launch:**
- payroll-of-record (the client keeps QuickBooks Payroll, ADP or Gusto);
- lien filing (unauthorized-practice-of-law risk [A, C5-S030]);
- surety sales (needs a producer licence);
- anything using "CPA" or "public accountant" [A, DB-S015];
- assurance reports [A, DB-S016].

## 2. Named operators
| Operator | Type / geography | What is known | Level |
|---|---|---|---|
| Remote Books Online | National remote vertical bookkeeper | Specialty sub $500–1,000/mo; GC with WIP/retainage $900–1,800; multi-entity $1,600–2,800+ [C5-S009]. Its Chicago ZIP pages say $150–300/mo, which is inconsistent and kept as a discrepancy [DB-S029] | D |
| Bench (Employer.com) | National online bookkeeping | $199–$999+/mo; accrual tiers $699–$999 [C5-S003]. Shut down Dec-2024 after automation-driven service failures [C5-S006] | B/C |
| Pilot / Digits | National AI-first | $99/mo and $65–$250/mo, cash-basis or limited, no WIP [C5-S004/S005] | B |
| 24 Hour Bookkeeper | Remote construction specialist | Markets job costing, WIP and "AI-powered tools"; pricing not published [DB-S024] | D |
| Wishup | Offshore managed | "Construction-trained" virtual bookkeeper from $999/mo [C5-S035] | D |
| Porte Brown LLC | Illinois CPA firm (Elk Grove Village) | Construction practice; member of CFMA, IRTBA, FWC and ASA [DB-S023]. A competitor at the top end and a likely referral partner | B |
| Wipfli LLP | Regional CPA/advisory firm | Dedicated construction practice [DB-S026] | C |
| Legacy Professionals LLP | IL/IN/MN accounting firm | Serves many trade unions and benefit funds [DB-S025]. Relevant to fringe reconciliation, not a direct competitor | B |
| ADP + Points North; LCPtracker; PaidReady | Certified-payroll software | $175/mo + $7.50/report [C5-S013]; $12/report or $145/mo for 5 projects [DB-S020]; $49–99/mo [DB-S021] | B |

**Structure:** Illinois has 1,673 "other accounting services" firms; the 1,286 with under 5 employees average about $189k receipts [C, C5-S001]. Payroll per employee in those firms is about $45k and receipts per employee about $130k [C, DB-S036]. The field is fragmented, with no scale economy below enterprise size.

## 3. Named suppliers and partners
See the CSV for full terms.

| Partner | Role | Terms | Status |
|---|---|---|---|
| IDOL certified-payroll portal | Mandatory filing channel | Free; Illinois Public ID; separate log-in per company when one person files for two companies [A, DB-S013] | documented |
| LCPtracker (LCPcertified) | Firm-level software | $2,500/yr for 25 active projects. Lists CA/WA/MD exports only; **IDOL support unverified** | documented |
| QuickBooks Online / Payroll | Client ledger and payroll of record | Payroll $50 + $7/employee [B, C5-S010]; ProAdvisor terms MISSING | documented / assumed |
| Knowify; WIPkeep | Job-cost and WIP tooling | Knowify Advanced $329–399/mo (10 users) [DB-S035]; WIP tools listed at $20–70/mo [D, C5-S036] | documented |
| Claude Team | AI review layer | $25/seat/mo monthly [B, DB-S022] | documented |
| The Horton Group (Orland Park) | Surety broker, referral partner | NASBP member, affiliated with AGC/ASA [B, DB-S027]. Referral behaviour MISSING. No referral fees should be accepted | assumed |
| Arthur J. Gallagher Surety (Rolling Meadows) | Surety broker, referral partner | Page exists; content not extracted | assumed |
| SBA Surety Bond Guarantee | Client enabler | Up to $9M non-federal; fee 0.729% [A, DB-S028] | documented |
| CFMA Illinois / ASA Chicago / FWC | Channels | Dues MISSING [DB-S041, DB-S023] | assumed |

## 4. Named prospective customers (31; CSV)
All prospects are drawn from public award records, are "prospect — not contacted", and carry the award URL. Two sources were used:

**City of Chicago awards since 2022 (Illinois Prevailing Wage Act applies)** [A, DB-S018]:
- Ryans Plumbing 1 (Dolton, LSLR SBI II, $563,583);
- Advanced Water Solutions (SRF LSLR, about $6.0M);
- Millennium Contracting (about $28.2M across 6 POs);
- United Enterprise (Brookfield, 9 POs);
- Plumbing Professionals (Morris, daycare LSLR term agreement);
- Courtesy Electric (SBI lighting at Midway);
- Autumn Construction Services (Lombard);
- City Lights Ltd;
- JOC holders: GMA Construction Group, Robe Inc, Pacific Construction Services, CSI 3000, Cordos Development, Old Veterans Construction;
- NCI primes: Seven D, G&V.

**Federal specialty-trade awards to Illinois-based firms (WH-347 duties)** [A, DB-S019]:
- Industria (Des Plaines, Navy roof $8.26M);
- Cora Jane and KDA (Itasca);
- 2BG Venture, Troop Contracting and Azimuth Contracting (Hines VA);
- Helm Builds;
- K.C. Electrical;
- J & B Builders (GSA masonry restoration);
- Lawdensky;
- Marval Group;
- Celtic Commercial Painting;
- Shine On Group;
- Bi-State Masonry and Goetz Concrete (Quad Cities).

Websites were recorded only where the page was fetched and matched the name. Seventeen are "MISSING".

## 5. Representative transactions (monthly unless stated)
| Transaction | Revenue | Direct cost (labour at loaded rates + software) | Contribution | Evidence |
|---|---|---|---|---|
| A. $4M sub, 25 employees, 2 IDOL projects: close + job cost + quarterly WIP + certified payroll | $1,250 | bookkeeper 9 h $306; senior review 1.5 h $83; compliance 3 h $99; CP software $58; WIP/capture $45 = **$591** | **$659 (53%)** | Price within the D band [C5-S009]; software [B, DB-S020] |
| B. $1.2M sub, no public work: close + job cost, semiannual WIP | $750 | $204 + $41 + $35 = **$280** | **$470 (63%)** | D/E |
| C. One-time onboarding/clean-up (6 months rebuild, cost codes, opening WIP) | $2,000 | 20 h + 4 h review + setup = **$960** | **$1,040 (52%)** | E |
| D. Certified-payroll-only (1 project, about 9 months/yr) | $300 | $83 + $54 = **$137** | **$163** | B/E |

**Payment timing:**
- Monthly fees are billed in advance by ACH or card (model DSO 8 days; E).
- Clean-up is billed 50% upfront.
- Transaction D shows why certified payroll alone is not a business. Its main value is the award-list lead source and the switching cost it adds to A.

## 6. Customer acquisition
**Customer #1:**
- **Who to target first:** subs with fresh City or federal awards (the CSV list) and the two or three most construction-active CPA firms. These firms do not want sub-$5M bookkeeping, and Porte Brown's association list shows where they meet clients [DB-S023].
- **Offer:** a $450 fixed-fee "WIP and job-cost health check" (see §13).

**Customers #2–10:**
- Convert health checks into monthly engagements.
- Ask each surety broker (Horton, Gallagher, smaller NASBP producers [DB-S042]) one question: "who struggles to give you a WIP?"
- Attend ASA Chicago and FWC events.

**Customers #11–100:**
- Referrals (CPAs, sureties, GCs that hold sub pay applications).
- A monthly award-list mailer.
- An associate membership in CFMA.

**Funnel (model base, all E):**
- 12 qualified conversations a month → 35% reach proposal → 30% win, which is about 1.3 new clients a month at full pace.
- Referrals add 1.5 new clients per 100 active clients per month.
- Churn is 1.6% a month, slightly worse than Paychex's 82–83% retention [A, WS02-S022, incumbent].

**Unit economics:**
- CAC about $250 variable plus $400/mo fixed.
- Contribution about $550–650 per client-month after direct labour.
- Payback is under one month of contribution.
- LTV at 1.6% churn: about 62 months × ~$600 ≈ **$37k contribution**.

**Founder sales time:** about 12–15 hours a week in year 1, falling to about 8 once referrals start.

## 7. Pricing strategy
| Tier | Scope | Price | Anchor |
|---|---|---|---|
| Core | Monthly accrual close by day 10, job-cost report | $750/mo | Bench Complexity 2 $699 [B]; vertical specialty sub $500–1,000 [D] |
| Surety-ready | Core + quarterly WIP with over/under-billings + retainage schedule + surety package | $1,100/mo | Vertical GC-with-WIP $900–1,800 [D] |
| Public-works | Surety-ready + IDOL certified payroll (up to 2 projects) + fringe reconciliation | $1,400/mo, +$125 per extra active project | Software alone $145–190/mo [B] |
| Clean-up | One-time | $1,500–3,000 | E |

**Rules:**
- Never price against the $65–99 AI tiers [B, C5-S004/S005]. They do not do WIP.
- Annual prepay at 10% off.
- No hourly billing.
- Model ARPC is a $1,000 blended average (D).

## 8. Working capital and cash conversion cycle
| Clients | Monthly revenue | AR (DSO 8) | AP (DPO 15 on ~12% COGS) | Net working capital |
|---|---|---|---|---|
| 10 | ~$10k | ~$2.7k | ~$0.6k | ~$2k |
| 50 | ~$50k | ~$13k | ~$3k | ~$10k |
| 200 | ~$200k | ~$53k | ~$12k | ~$41k (≈6 days of revenue) |

If billing moves fully to the 1st of the month in advance, DSO turns negative and working capital is a source of cash.

**The real cash risk is payroll ahead of clients:** each bookkeeper costs about $5,800/mo before their 15 clients exist.

**Model peak funding:**
- about $8k base;
- about $37k conservative (including the $3k/mo owner draw from month 13);
- about $23k conservative excluding the draw.

## 9. Regulatory path
1. Form an Illinois LLC and assumed name. The Secretary of State fee is not verified this session (E).
2. **No licence is required for bookkeeping** [A, DB-S014]. Never use "CPA", "public accountant" or similar terms (civil penalty up to $10,000 per offense) [A, DB-S015]. Issue no assurance or opinion reports [A, DB-S016].
3. **Certified payroll:**
   - the client creates its Illinois Public ID;
   - the firm files under a separate log-in for each client company [A, DB-S013];
   - engagement letter: client approves worker classifications, the firm prepares and the client certifies;
   - SB1344 penalties of $1,000/$2,000 per missed month reach the "agent" responsible for filing [C, C5-S019]. Confirm E&O covers this; fines are often excluded (MISSING).
4. **Federal work:** Davis-Bacon contracts do not file with IDOL [A, DB-S013]; WH-347 is prepared for the client.
5. **Payroll processing:** stay off it at launch. Paid tax preparation would need a PTIN (not verified); refer tax work to CPA partners.
6. **Insurance:** E&O plus cyber (premium MISSING; modelled at $275/mo, E). No WC beyond office employees (MO clerical loss cost $0.085/$100 as a proxy [C, DB-S006]).
7. **Data security:** written information-security plan; whether the FTC Safeguards Rule applies to bookkeepers is not verified (MISSING).

**Timing:** 2–4 weeks.

## 10. Operations workflow (lead to cash)
1. **Lead:** an award-list record or referral, logged in the CRM. *Human.*
2. **Discovery call and read-only QBO review.** *Human, with AI summarizing chart of accounts and job setup.*
3. **Proposal and engagement letter (scope, classifications responsibility).** *AI drafts, human sends.*
4. **Onboarding clean-up:** cost codes, opening WIP. *Human; AI helps reconcile.*
5. **Monthly close:**
   - bank feeds and AI categorization;
   - accruals, retainage, committed costs;
   - human review by the senior accountant.
6. **WIP:** percent-complete from cost-to-date over estimated total cost; over/under-billings. Estimates to complete come from the PM and are always human-confirmed.
7. **Certified payroll:** export payroll → map hours to project, classification and county rate (rates from IDOL county PDFs [A, DB-S004]) → IDOL template → client signs → upload by the 15th. *Template filling is automatable; the rate check is AI-assisted.*
8. **Invoice by ACH on the 1st.** *Automated.*

**Stack and cost:**
- Claude Team $25/seat;
- LCPcertified $210/mo, or the IDOL Excel template if LCP cannot export;
- practice management about $50/user (E);
- client-paid QBO;
- total software about $510/mo modelled.

**After Dec-2026:** the ordinary paid AI tier is enough. Nothing depends on unlimited AI.

## 11. Competitive position and defensibility
**What accumulates:**
- client files and WIP history, which is sticky because rebuilding it is painful;
- monthly certified-payroll cadence, which is hard to drop mid-project;
- surety/CPA referral trust;
- a growing internal rate/classification library by county.

**What does not:** technology, or the right to the work. Any construction CPA can copy the offer.

**The opening:** the documented scarcity of WIP literacy in low-cost tiers, plus small subs' penalty exposure. A small extra wedge: the main certified-payroll software does not list Illinois export (to verify).

**AI cuts both ways:** it lowers our labour per client but also commoditizes generic bookkeeping [A, C5-S008].

## 12. Key risks and pre-mortem
| Loss level | How it fails | Early warning |
|---|---|---|
| ~$5k | Health checks do not sell; contractors say "my CPA does this" | <3 paid checks from 40 conversations by day 60 |
| ~$25k | The first bookkeeper is hired at 12 clients, then 4 churn when a big job ends or a sub fails. Labour productivity below 15 clients per bookkeeper destroys margin; the model shows labour +20% halves year-3 profit ($49k) and hiring 30% sooner turns it negative | Hours per client above 10/month after month 3; churn above 2%/month |
| ~$50k | An E&O event: a mis-mapped classification causes back-wages and an SB1344 penalty, and the client claims against the firm; or WIP errors mislead a surety | Any client receiving an IDOL notice; WIP revisions above 10% between quarters |

**Other risks:**
- Construction recession: new clients −30% and churn ×1.5 still give about $132k in the stress model, a lumpy-staffing artefact. Treat recession as at least −30% (E).
- Founder skill bottleneck.
- Intuit AI agents moving into job costing [A, C5-S008].

## 13. Validation plan
| # | Experiment | Cost | Success | Kill |
|---|---|---|---|---|
| 1 | Paid "WIP and job-cost health check" at $450, offered by letter and call to 40 CSV prospects | ~$300 (mail, travel) | ≥3 paid within 60 days | 0–1 paid |
| 2 | Convert health checks into monthly Surety-ready engagements at $1,100 | $0 | ≥2 signed monthly clients by day 90 | None signed after 3 completed checks |
| 3 | Surety-broker test: 8 producer conversations ("which clients fail to give you a WIP?") | $0 | ≥3 agree to introduce a named client | No broker sees a gap |
| 4 | Certified-payroll trial: first month at $0, then $250/mo, offered to 15 fresh LSLR/JOC/SBI subs | ~$100 | ≥4 paying by month 2 | <2 paying |
| 5 | Skill gate: founder rebuilds two sample WIPs; a construction CPA reviews them for a fee | ~$500 | Reviewer error rate ≤ minor | Material errors twice |

Total validation cost is about **$900**.

These experiments involve contact and are for the founder to run. None were performed in this research.

## 14. Revised scores and verdict
| fcf | roic | access | scale | resilience | entry | delegation | cash | feasibility | ai |
|---|---|---|---|---|---|---|---|---|---|
| 5 | 8 | 5 | 5 | 6 | 5 | 6 | 8 | 8 | 5 |

**Scores:**
- Unchanged from Stage C. The model confirms the base case at about $101k year 3 / $188k year 5 (fcf 5), with near-zero capital (roic 8).
- Feasibility stays 8 even though the no-licence path is now A: filer liability makes E&O essential.
- Raw composite 5.93; evidence D (k = 0.70) gives an adjusted score of **5.65**.

**Gates:** none.

**Model results:**

| Scenario | Year-3 operating profit | Year-5 operating profit |
|---|---|---|
| Conservative | $42k | $74k |
| Base | $101k | $188k |
| Optimistic | $369k | $847k |

**Milestones:**
- $10k/month operating profit in month 14 (base).
- $25k/month not reached within 60 months in base.
- Plausible ceiling $250k/yr. $500k needs multiple remote pods selling WIP-heavy work beyond Illinois.

**Verdict: FINALIST (conditional on §13 experiments 1–2).**
