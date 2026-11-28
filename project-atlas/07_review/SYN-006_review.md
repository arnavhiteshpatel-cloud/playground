# SYN-006 — Stage F Adversarial Review (batch F1)

**Concept reviewed:** surety-ready job-cost/WIP bookkeeping plus Illinois certified payroll (CP) for Chicagoland public-works subcontractors.

**Material reviewed:**
- Stage C memo, Stage D deep dive, Stage E playbook and materials;
- `08_financial_models/SYN-006_assumptions.json` and `_results.json`;
- the prospect CSV (36 rows) and the supplier CSV;
- `sources_E_SYN-006.jsonl` and the cited C5, DB and WS02 records.

**Reviewer:** independent; I did not write any of this. **Access date:** 2026-11-28.

**Re-runs:** made with `tools/fin_engine.py` (scripts in `/tmp/claude-0/atlas_scratch/F1/rerun*.py`). The finalist's model files were not modified. New sources are F1-S001…S006 in `07_review/sources_F1.jsonl`.

---

## 1. Verdict: **SURVIVES WITH MAJOR REVISIONS**

**What holds up:**
- The legal path for bookkeeping is clean (verified).
- Capital at risk is genuinely tiny: about $10–12k peak funding in base, even after my corrections.
- Certified payroll is a real, monthly, penalty-backed mandate.

**Why the evidence-adjusted case is much weaker than the playbook says:**
- The base case stacks four favourable labour and price assumptions, and the model is extremely sensitive to each:
  - $1,000 blended ARPC;
  - 15 clients per bookkeeper;
  - a $5,800/month loaded bookkeeper;
  - a $600/month external construction reviewer.
- Each correction alone costs $5–18k of year-3 profit. All four together cut base year-3 operating profit from **$94,734 to about $49,700**, and year 5 from **$181,482 to about $82,600**.
- The surety-producer referral channel, which the playbook ranks first, has no supporting evidence.
- The niche where non-CPA statements plus a WIP satisfy a surety is narrower than the target segment.

**Corrected view:**

| | Year-3 operating profit | Year-5 operating profit |
|---|---|---|
| Corrected base | ~$50k (plausible range $25–85k) | ~$80k |
| Corrected conservative | ~$23k | ~$32k (peak funding $182k with the $4k draw, $42k without) |

**Plausible ceiling:** about $150k/yr for a founder-led Illinois firm, not $250k, unless labour productivity is proven well above my base.

It remains a reasonable *low-capital* validation bet. It is not a strong holding-company engine on present evidence.

---

## 2. Factual errors found

| # | Claim (where) | What the source actually says | Correction |
|---|---|---|---|
| F1 | "No licence is needed for bookkeeping **or for preparing certified payroll** [A, DB-S014; A, E-SYN006-S024]" (playbook verdict) | 225 ILCS 450/8.05 (verified on FindLaw) covers accounting services only: bookkeeping, compilations and tax under (a)(3), not restricted to CPAs. It says nothing about certified payroll or the Prevailing Wage Act. | That no licence exists for CP preparation is plausible but **unverified (E)**. The Accounting Act cannot carry an A-level claim about prevailing-wage filing. Keep "counsel: is CP preparation regulated?" as an open item (the playbook lists it in §12.4, contradicting its own verdict line). |
| F2 | "A filer entering payrolls for two companies needs a separate log-in per company, i.e., third-party filing is contemplated [A, DB-S013]" (model evidence note) | IDOL FAQ 17 (verified) answers only "Yes" to whether separate log-ins are needed for two companies. FAQ 10 concerns GCs filing for subs; IDOL "recommends that every contractor file their own certified payroll". The FAQ is silent on outside preparers. | The *inference* is D/E, not A. Stage E's own note concedes this ("IDOL FAQ silent on third-party filers"), but the A-level wording survives in the model's `evidence_notes`. |
| F3 | Western National "No C.P.A. Requirement" program cited as current surety practice [B, E-SYN006-S005] | Verified. The chart says "Effective for New Business: October 1, 2016". Xpress Xtra is capped at **$1.5M single and $1.5M bonded aggregate**. | The playbook notes the date only in §12. The cap matters more: the targeted sub ($2–15M revenue, $1–5M bonded backlog, §2.1) is mostly **above** the one documented no-CPA program. Those firms will need CPA-compiled or reviewed year-ends. A practitioner rule of thumb puts compiled statements at about a $3M program [D, F1-S003]. Our product is therefore the *interim* WIP and clean books feeding the CPA, not the surety's primary document. |
| F4 | TMHCC packet "requires … a Work-on-Hand schedule" [B, E-SYN006-S004] | Verified, and stronger than cited. The packet asks "Is statement prepared on an (A) audited or (B) unaudited basis?" and, "IF NOT FULL CPA AUDITS", asks for schedules of all balance-sheet items plus work-on-hand. | It confirms WIP demand, but also that underwriters expect CPA year-ends as the norm and treat non-audited statements as needing extra support. |
| F5 | Stage C/D: SB1344 brings "civil penalties, 4-year debarment" | Amundsen Davis (verified, C5-S019) says SB1344 adds civil penalties of $1,000 / $2,000 per missed month on the employer and on "any officer, employee, or agent … whose duty … is to file". Debarment comes from the pre-existing two-violations-in-5-years rule (820 ILCS 130/11a), not from SB1344. | A minor conflation. The *agent* liability, which matters most, is correctly reported. |
| F6 | Remote Books Online bands $500–1,800 described as "vertical construction bookkeeping list ranges" (as if an industry survey) | Verified. These are the **vendor's own** pricing bands in a marketing blog post (published 2025-08-25, updated July 2026). | D-level and self-interested. Fine as an anchor, not as market evidence. |

Citations that checked out as stated:
- BLS OOH: bookkeeping-clerk median $50,670 (May 2025); construction-industry median $54,890; −6% outlook for 2025–35.
- Insureon bookkeeper medians: E&O $37/month, cyber $47/month, $1M/$1M limits.
- LCPcertified prices, with CA/WA/MD-only exports.
- SB1344 agent clause.

---

## 3. Unsupported or over-stated claims

| Claim | Warranted level | Comment |
|---|---|---|
| "Surety demand for WIP schedules is now documented at B" | B for *demand that a WIP exist*; **E for demand for an outside non-CPA preparer** | Both carrier documents show what underwriters ask for, not who contractors pay to produce it. Construction CPAs routinely include the WIP in year-end statements [D, F1-S004 / search extracts]. |
| Surety producers as the #1 acquisition channel ("surety producers > award letters > CPA referrals", §6.1) | **E, with contrary priors** | No source shows producers referring clients to bookkeepers. Producers' public guidance points contractors to construction CPAs. A producer who sends a client to an unknown non-CPA whose WIP later misleads an underwriter carries reputational risk. Expect referrals only after 12–24 months of visible, clean WIPs. **Rank award-triggered CP outreach first.** |
| "Leads are public. City and federal award records name the buyers [A]" | A for **primes**; buyers below primes MISSING | The playbook concedes City data names primes only: 49 distinct vendors in about 13 months. Several listed prospects are large (Millennium about $28M of POs; Courtesy Electric with a $6.7M O'Hare job) and probably have in-house controllers. The true target, small non-union subs, is not in any public list reviewed. |
| "Delegable: standard bookkeeping and payroll-clerk roles" | Over-stated | The model's hiring trigger (first bookkeeper at 12 clients, then one per 15) leaves the **founder producing books for about 8–12 clients through year 5**. Construction accrual/WIP staff are not "standard clerks" (see §4). |
| Bench $699 accrual tier as a live price anchor [B] | B for the page, but weak as a comparator | Bench collapsed in Dec-2024 (C5-S006) and was bought by Employer.com. Its pricing now reflects a distressed relaunch. |
| Year-2 operating profit $124,997 > year-3 $94,734 | Model artefact | Acknowledged in §6.3. Year 2 contains about $45–90k of unpriced founder production. |

---

## 4. Financial model audit

**Recomputation.** I re-ran the base with the engine and got $94,734 (year 3) / $181,482 (year 5) and peak funding of $9,979, matching `_results.json`. The 24-month table and the tornado reproduce. Working-capital logic is sound: DSO 8 with ACH in advance means NWC is immaterial. The draw logic follows the standardization rule: the draw starts at month 13, the base trough is in month 5, so the draw does not change base peak funding.

**Top-5 drivers challenged:**

| Driver | Playbook base | Independent evidence | Proposed base / conservative |
|---|---|---|---|
| ARPC | $1,000 (D) | Vendor bands $500–1,800 (own pricing, D) [C5-S009 verified]. Vendor-marketing search extracts put "full-service with job costing" at $1,000–2,500 and "full stack with WIP/retainage" at $800–1,300+ (D). **Wishup offers a "dedicated construction-trained virtual bookkeeper" from $999/month, and the page lists WIP report preparation** [D, C5-S035 re-verified]. AI tiers ($65–250) do not do WIP. | **$950 / $800.** A newcomer with no track record sells against an offshore *dedicated* resource at the same price. The 40% CP attach rate is E. |
| Clients per bookkeeper | 15 (E) | Census: Illinois 541219 firms average about $130k receipts per employee (C, DB-S036). The model's year-5 revenue per head *including* the founder is $97k, so overall staffing is **not** unrealistically lean. That is a point in the playbook's favour, and I record it. But transaction A implies 9 h a month for an accrual close, retainage, committed costs, job-cost report and quarterly WIP for a 25-employee, $4M sub. That is the low end (E). | **13 / 11** (E). Disagreement preserved: the author's 15 is defensible if the IDOL mapper and close SOPs work. |
| Bookkeeper loaded cost | $5,800/month | Chicago metro mean for bookkeeping/accounting clerks: $25.75/h, $53,560 (May 2024) [C, F1-S001]. Chicago business and financial operations mean: $46.54/h (May 2025) [C, F1-S002]. A full-charge construction bookkeeper who can do percent-complete WIP sits between clerk and staff accountant. | **$6,200 / $7,000** loaded |
| External construction reviewer | $600/month for 5–8 h (implies $75–120/h) | No rate found (MISSING). An experienced construction controller or CPA reviewing a WIP is unlikely to bill under $150/h (E). | **$1,000 / $1,500** |
| Win rate and lead volume | 12 conversations × 35% × 30% | No benchmark (E). Trust barrier: an unknown, non-CPA founder with no construction track record is selling *accuracy*. | Keep 30% as base, but report year 5 at 25%. Lower demand flatters year 3 by delaying hires. |

**Re-run results (base unless noted):**

| Case | Y3 operating profit | Y5 operating profit | Peak funding (with draw) |
|---|---|---|---|
| Playbook base | $94,734 | $181,482 | $9,979 |
| ARPC $950 only | $76,822 | $150,093 | — |
| 13 clients per bookkeeper only | $82,427 | $142,314 | — |
| Bookkeeper $6,200 only | $85,822 | $161,223 | — |
| Reviewer $1,000 only | $89,641 | $176,079 | — |
| **All four (corrected base)** | **$49,662** | **$82,563** | **$11,540** |
| Corrected base, ARPC $900 | $31,750 | $51,174 | $11,701 |
| Corrected base, ARPC $1,000 | $67,575 | $113,951 | $11,379 |
| Corrected base, win 25% | $84,201 | $71,104 | $12,346 |
| Corrected conservative | $23,478 | $32,372 | $181,795 ($42,087 with no draw) |

*Corrected base:* 13 clients per bookkeeper at $6.2k, reviewer $1k, ARPC $950. *Corrected base, win 25%:* the hire delay flatters year 3.

**Reading:**
- Each $50 of ARPC is worth about $18k of year-3 profit.
- The business is a labour-arbitrage service with about a 10–15% operating margin once staffed. Year-5 operating profit runs at about 10–13% of revenue in my corrected base, versus 21% in the playbook.
- FCF anchor for scoring: the year-3 to year-5 base of about $50–83k sits at the **3–4** band, not 5.

**Founder-draw logic.** The base covers the $4k draw from month 13. In the corrected conservative case, the draw makes peak funding $182k: the business cannot pay its founder. This is honest and consistent with the playbook's "conservative is a kill case".

**Missing line.** There is no allowance for unbilled clean-up overruns or write-offs on troubled first clients (E, about 1–2% of revenue). The clean-up price is unbenchmarked, and §11 itself flags scope creep.

---

## 5. Customer acquisition challenge
**Incumbent sales motions:**
- Construction CPAs win through year-end/tax relationships, CFMA and ASA networks, and surety and bank referrals (Porte Brown lists CFMA, IRTBA, FWC and ASA; DB-S023).
- National remote vertical bookkeepers win by search and content marketing (Remote Books Online's programmatic ZIP pages).
- Offshore firms win on price per dedicated hour.
- Construction payroll services now publish Illinois-specific prevailing-wage guides and position themselves as complete certified-payroll compliance services, e.g. Payroll4Construction [D, F1-S005] and Miter [D, F1-S006]. **Neither is named in the playbook.**

**What the first 10 customers will really require:**
1. A **credibility artefact before the first sale**: two WIPs reviewed by a named construction controller or CPA. The playbook's skill gate does this. Make it a hard prerequisite, not a parallel test.
2. An **entry product with low trust risk**. Certified payroll on a fresh award (first month free) is the realistic door. Owners hand over a filing chore far more readily than their books and surety relationship.
3. **Subs, not primes.** The award list gives primes. Each prime must be asked for its subs, and that ask yields names only once the founder has delivered for that prime.
4. **Time.** At 12 qualified owner conversations a month (E), with no producer referrals in year 1, expect 5–8 clients at month 12, not 9.4. Base year-1 clients fall to about 7–8 at a 25% win rate.

The $450 health check is a good instrument. But a "≥3 paid within 60 days from 40 letters" success bar is permissive for a decision of this size. **Require ≥2 of the paid checks to come from non-referral cold outreach**, to test the scalable channel.

---

## 6. Supplier/partner accessibility challenge
- **Surety producers (Horton, Gallagher):** the most likely to decline engagement.
  - Gallagher Surety is national and large-account focused (the CSV itself says "large-account focus likely").
  - Producers have no incentive to endorse an unproven non-CPA.
  - *Test as written (8 interviews), but treat "≥3 will introduce a named client" as unlikely before a track record exists.*
- **Construction CPA firms:** these are competitors for monthly work as well as referral sources. Porte Brown-type firms offer outsourced accounting themselves. White-label WIP preparation (pivot B) is plausible, but at subcontract rates (about $40–60/h, E), not $1,000/client.
- **IDOL:** accessible (a free portal). Unresolved: whether an outside preparer may operate under the client's log-in (F2).
- **E&O carriers:** accessible. The real risk is an **exclusion** for fines, penalties and debarment-related losses (MISSING; a quote is needed).
- **LCPtracker / PaidReady:** client-side only. The firm-licence correction in Stage E is right.

---

## 7. Legal/regulatory challenge
1. **SB1344 agent exposure (confirmed).** Penalties reach "any officer, employee, or agent … whose duty … is to file" [C, C5-S019 verified]. An engagement letter that makes the firm responsible for preparation *and* timely submission makes it the agent "whose duty … is to file".
   - The playbook's mitigation (client certifies and clicks submit) is correct, but it shifts the client's deadline risk back to the client. That weakens the value proposition ("we keep you filed on time").
   - Counsel must draft the duty allocation. E&O probably excludes the fines themselves.
2. **False-certification exposure.** Willful false filing is a Class A misdemeanor (820 ILCS 130/5, C5-S014). The preparer maps hours to classifications. If a client instructs a misclassification to underpay, the preparer is a witness or participant.
   - **Needed:** a written policy to refuse and resign, plus a classification-approval log signed by the client.
3. **Payroll-service creep.** Fringe reconciliation and "payroll admin on the client's platform" (year-2 adjacency) edge toward payroll-service-provider status (IRS Form 8655 / reporting-agent rules). Keep the client's platform as payer of record; counsel should confirm.
4. **Title use.** Section 9 / 225 ILCS 450 risk is correctly handled ("no 'accountant' in the name pending legal review").
5. **Not addressed:** state data-breach duties (Illinois PIPA, 815 ILCS 530) for SSNs and wage data in certified payrolls. CP files contain worker SSNs or IDs and addresses. A written security plan is listed; PIPA should be named and reviewed by counsel (not verified here).

---

## 8. Competitive response
- **Construction CPAs** can bundle monthly close and WIP into the year-end relationship at will. The wedge ("they don't want sub-$5M bookkeeping") is E.
- **Offshore/remote vertical firms** (Wishup $999 dedicated; Remote Books Online) already advertise WIP. They would not even need to respond.
- **Software is eroding the labour content of certified payroll.** Construction payroll platforms (Miter, Payroll4Construction, ADP + Points North/Dapt) generate CP reports from payroll. As clients adopt them, the $300/month CP add-on shrinks toward a review fee. The IDOL-template tooling advantage is real but copyable.
- **Intuit** is pushing done-for-you AI bookkeeping (C5-S008), which compresses generic close prices. WIP and estimates-to-complete remain human judgment, which is the moat. It is thin.
- **Underestimated incumbent advantage:** the CPA's year-end report is what the surety actually relies on. The bookkeeper's work is an input whose quality the CPA can disparage.

---

## 9. Founder execution and delegation realism
- **Skill gap is the critical path.** Surety-grade WIP needs:
  - percent-complete revenue recognition (cost-to-cost);
  - estimated-cost-at-completion discipline with PMs;
  - retainage receivable and payable;
  - committed costs;
  - contract-asset and contract-liability tie-out to the balance sheet;
  - fade analysis.
- The arithmetic is learnable in weeks. The judgment (challenging a PM's estimate to complete, spotting a loss job) takes most practitioners years. With a paid reviewer on every early WIP, a capable founder can produce acceptable *interim* WIPs within about 3–6 months (E).
- **They cannot be the client's credibility with a surety.** Recommendation: hire or contract the senior construction accountant from client 1 (part-time), not at 30 clients.
- **Founder hours.** The model keeps the founder producing for about 12 clients indefinitely, plus selling and review: about 200 h/month in months 10–24 (§6.4). This is the "exhausting low-paid job" scenario by design.
- **Real delegation needs two hires:**
  - a controller-level operations lead (about $100k+ loaded, not modelled; §6.8);
  - a second bookkeeper to absorb the founder's book.
- In corrected base, both together cost about the entire year-5 operating profit.

---

## 10. Pre-mortem
| # | Most plausible failure | Early indicator | Cheapest preventive test |
|---|---|---|---|
| 1 | **Price ceiling.** Owners anchor on their current $300–600 bookkeeper, offshore $999 dedicated offers, or the CPA. Realized ARPC lands at $750–850, and the firm is profitable only while the founder does the work for free. | Median signed fee below $900; requests to drop WIP from scope | Before any hire, require ≥5 signed monthly clients at a median ≥$950 |
| 2 | **Labour productivity.** Hours per client run 12–16 on construction accrual plus WIP. Bookkeeper #1 covers 10–11 clients, and year-3 profit goes to roughly zero (model: labour +20% → $41,901; corrected base −$50 ARPC → $31,750). | Time-tracked hours per client above 10 after month 3 | Time-track every client from day 1. The hire gate stays at ≥11 clients **and** ≤10 h per client. |
| 3 | **Liability event in year 1–2.** A misclassification or late filing triggers back-wages, a 20% IDOL penalty and an SB1344 penalty. The client blames the preparer, and E&O excludes the fines. | Any IDOL notice; any client pushing back on classification approvals | Get counsel to draft the duty allocation, and an E&O quote with penalty language, **before** the first CP engagement (about $500–1,500, E) |

---

## 11. Corrected scores
| Criterion | Stage E | **F1** | Reason |
|---|---|---|---|
| fcf | 5 | **4** | Corrected base about $50k (year 3) to about $83k (year 5) |
| roic | 8 | **8** | Peak funding about $12k; year-3 operating profit/capital still above 300% |
| access | 5 | **4** | Primes are public, subs are not; trust wall for a non-CPA newcomer; surety channel unproven |
| scale | 5 | **4** | Labour-linear; Illinois-specific CP rules; corrected ceiling about $150k/yr |
| resilience | 6 | **6** | Statutory demand, but construction-cyclical |
| entry | 5 | **4** | CPAs, offshore WIP-capable firms at $999, and CP software platforms |
| delegation | 6 | **5** | Founder keeps about 12 clients through year 5; a scarce senior skill is needed |
| cash | 8 | **8** | ACH in advance; immaterial NWC (verified) |
| feasibility | 8 | **7** | Licence-free bookkeeping verified; CP agent liability and the CP-licence question need counsel |
| ai | 5 | **5** | Real back-office savings; also compresses generic prices |

- **Raw composite:** 5.28. Evidence **D** (k = 0.70) gives an **evidence-adjusted score of 5.20** (Stage E: 5.65).
- **Gates:** none fail.
  - G4: WARN-borderline. Corrected base reaches $100k/yr only around year 6.
  - G7: WARN. Founder-produced client book.

**Bottom line.** SYN-006 is the kind of business the mandate says it values:
- licence-free;
- customer-funded;
- recurring;
- anchored in statute.

Its downside is capped at about $10–40k if the validation gates are obeyed. But the Stage E base case is built on the favourable end of every labour and price assumption. Corrected for a realistic newcomer price ($950), Chicago construction-bookkeeper cost, an honestly priced construction reviewer, and slightly lower productivity, it becomes about a $50k year-3 / $80k year-5 business. That is a good job with a modest firm attached, until labour productivity and a ≥$950 realized price are *measured*.

The surety-referral channel and the "surety-grade WIP" claim are the weakest links. The realistic product is interim WIPs and clean books feeding the client's CPA, entered through certified payroll.

**It survives only with these changes:**
- reorder the channels (CP first, sureties later);
- make the external reviewer, counsel and E&O-penalty check prerequisites;
- raise the go gate to median realized ARPC ≥$950 with time-tracked hours ≤10 per client.

I disagree with the author's "fcf 5 / plausible ceiling $250k" and record it.
