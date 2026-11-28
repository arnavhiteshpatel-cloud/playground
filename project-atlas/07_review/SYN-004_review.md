# SYN-004 Stage F review (batch F2): Energy cost management for large Illinois C&I users

Independent adversarial review, 2026-11-28. I did not write any of the material reviewed. This was read-only desk work: nobody was contacted, and no form, account or enquiry was created. New sources are `07_review/sources_F2.jsonl` (F2-S###). Helper scripts and outputs are in `/tmp/claude-0/atlas_scratch/F2/` (`syn004_alt.py`, `syn004_alt_results.json`). The finalist's model files were not modified.

## 1. Verdict

**Survives with major revisions. It stays a $500 validation candidate. It does not justify a full-time commitment, and on the corrected base case it would rank below a business with a $100k+ year-3 base.**

The legal core holds up better than the playbook could show:
- I read the statute text of 220 ILCS 5/16-115C(b) from an unofficial mirror. It excludes from the licensed class "any person or entity that is attempting to procure on behalf of or sell retail electric service to a third party that has aggregate billing demand of all of its affiliated electric service accounts in Illinois of greater than 1,500 kW" [A via mirror, F2-S001].
- 83 Ill. Adm. Code 454.30(b)(5) repeats the carve-out, and its last amendment is still 35 Ill. Reg. 17602, effective 2011-11-01 [A, F2-S003].
- So the licence-free path is statutory, not just regulatory.

The commercial core is weaker than the model says, for three reasons:
1. **The model ignores the contract-expiry wait.** The supplier fee starts only when the new supply contract flows. That happens at the customer's current expiry, typically 0–18 months after a mandate under the playbook's own qualification gate.
2. **The funnel assumes an unknown newcomer converts heavily courted, already-brokered large accounts** at 10 qualified conversations and 0.88 wins a month.
3. **The demand-response (DR) "partner share" is probably close to zero.** Curtailment service providers (CSPs) now advertise 100% pass-through to the customer.

**Corrected base view** (reviewer base: sales cycle 10 months, 7 qualified leads a month, 20% proposal-to-win, ARPC $800):

| Measure | Value |
|---|---|
| Year-3 operating profit | **≈ $33k** (filed: $98k) |
| Year-4 operating profit | ≈ $63k |
| Year-5 operating profit | ≈ $106k (filed: $120k) |
| Active accounts, end of year 5 | 23 |
| Peak funding including the $4k/month draw | **≈ $122k**, above the $100k conditional backing |
| Peak funding without the draw | ≈ $47k |

The shape of the plateau ($100–150k a year with founder plus one hire) does not change much. What changes is that it arrives about 12–18 months later, and the founder lives on backing money for about two years.

## 2. Factual errors found

| # | Claim (where) | What the source actually says | Correction |
|---|---|---|---|
| F1 | "The statute itself (220 ILCS 5/16-115C) could not be read"; the 1,500 kW carve-out in 16-115C(b) is "not verified verbatim" (playbook §2.1, §12 item 1) | The statute text is readable on a mirror. Subsection (b) contains the exclusion verbatim, along with exclusions for single-ARES exclusive agents and municipal power agencies [A via mirror, F2-S001]. Its history line reads P.A. 95-679 and 96-1385 | Upgrade the exemption to **statutory, A-level (text via unofficial mirror)**. Remaining gap: an ilga search result shows 16-115C was also amended by **P.A. 102-958 (HB 4973, eff. 2023-01-01)**. The content of that amendment could not be read (ilga.gov returned 503) [D, F2-S002]. The playbook asks only about "2025–26 amendments" and misses this 2023 amendment. Counsel must read the current official text |
| F2 | "The fee-disclosure code of conduct binds only 'any person or entity required to be licensed'", so exempt deals carry no statutory conduct duty (playbook "What changed" item 8) | True for 16-115C(e). However, **16-115C(a-5)** says "All third-party sales representatives engaged in the marketing of retail electricity supply must, prior to the customer signing a contract, disclose that they are not employed by the electric utility" [F2-S001]. That text is not limited to licensees | Add a utility non-affiliation disclosure to every exempt-deal agency agreement and pitch. Small cost, but the playbook says the opposite |
| F3 | ENGIE's request form asks for "state licence copies" (playbook §2.3) | The documents page asks for "Copies of broker/agent licenses **and/or state approval documents** for every state in which you intend to do business" [B, F2-S004]. The remittance agreement also requires the broker to warrant that it holds "all governmental authorizations, permits and licenses necessary" [B, F2-S005] | Broadly right, but the operative problem is sharper than the playbook says. An exempt-only Illinois broker has **no state document to show**, so the supplier's compliance team must accept a legal argument instead of a licence. This should raise the prior that suppliers refuse (V1). The credit-score and experience items come from the request-form PDF, which I did not re-open |
| F4 | ComEd cleared 1,105.6 MW of DR in 2028/29 (Stage D, DI-S022) | The same PJM report's Table 9 shows COMED offered and cleared **1,200.3 MW**; the 1,105.6 figure is in its narrative text [A, F2-S006] | Internal inconsistency in PJM's report. Immaterial to economics; cite the table |
| F5 | The model's `sales_cycle_months` = 4 (base) is treated as lead to revenue | The model's own notes say the fee starts only "when the new supply contract flows", and ENGIE pays nothing until a Customer Agreement is executed and the customer pays [B, F2-S005]. The qualification gate admits expiries up to 18 months out (playbook §2.7) | Effective mandate-to-first-fee time is about 3 months of selling plus an average expiry wait of about 9 months, so **8–12 months**. This is the biggest error in the model. See §4 |

**Checked and correct:**
- The capacity collar for 2029/30: cap $337.83, floor $181.91/MW-day UCAP; COMED import limit (CETL) down 68%; COMED CETL/CETO below 1 [A, F2-S007].
- 2028/29 cleared at the $325 cap RTO-wide (cap = $256.75/MW-ICAP) [A, F2-S006].
- The DR UCAP/ICAP ratio of about 0.91 [A, F2-S006].
- Above 1 MW, 93% of ComEd usage is on ARES [A, F2-S008].
- ENGIE remittance mechanics: paid on the 25th, withheld if the customer does not pay, true-ups, no fee after termination, no assignment without consent, ENGIE may contact the customer directly, and the customer designates between competing brokers [B, F2-S005].
- The 20–40% CSP-share checklist [C, F2-S009].
- The 454.30 exemption text [A, F2-S003].

## 3. Unsupported or over-stated claims

| Claim | Evidence level actually warranted |
|---|---|
| Suppliers will pay an unlicensed exempt-only broker | **MISSING.** No source shows any ARES remitting fees to an unlicensed Illinois consultant. ENGIE's process presumes per-state licence or approval documents [B, F2-S004]. Treat as E with a negative prior |
| 0.75–1.5 mils on 7–12 GWh accounts | D. The BOMA "offers" ($0.001–0.005) are an illustrative slide from a flat-fee competitor arguing against commissions, not a transaction record [D, F2-S011]. The 0.75-mil Urbana fee is a municipal search summary. Plausible, but D |
| 6% DR partner share (base ARPC) | E, and probably high. GridBeyond advertised **100% revenue share plus a $73k/MW-year 10-year floor** to PJM C&I customers (window Nov 2025–Apr 2026, now closed) [D, F2-S010]. When customers can get 100% directly, a channel fee has to be customer-paid and justified separately. Model DR at about 0 in the base case |
| "Capacity analytics" is the wedge | E. The Stage C memo itself says PLC alerts are "a retention tool... competitors give away free". This is not a defensible paid wedge |
| 10 qualified exempt-size conversations a month, each yielding 12 months of bills | E. Pool size MISSING: the ORMD report gives no count of customers above 1 MW [A, F2-S008]. After excluding chains, REITs, health systems and public bodies (as the playbook does), the private independent exempt pool is probably in the hundreds-to-low-thousands in ComEd (E). Most of it already has a supplier and probably a broker |
| 22% proposal-to-win against incumbent brokers | E. ENGIE's clause makes the **customer designate** between competing brokers [B, F2-S005], so every win requires displacing an incumbent adviser |
| Optimistic case of $1.22M year-5 operating profit | Not a plan, as the playbook says. It should not appear in milestone tables |

## 4. Financial model audit

**Reproduced.** Re-running `fin_engine.run` on the filed assumptions reproduces every headline:
- base year 3 $98,323, year 5 $120,332, peak funding $62,155;
- conservative year 3 −$10,282, peak $265,578.

**The arithmetic is internally consistent.** ARPC of $850 = $750 supply + $43 DR + $56 PLC, which checks.

**Top-5 driver challenge** (base, other drivers as filed):

| Driver | Filed | Challenge (evidence) | Reviewer base | Year-3 operating profit alone |
|---|---|---|---|---|
| Lead-to-revenue time (`sales_cycle_months`) | 4 | The fee flows only at the new contract start, after the current expiry [B, F2-S005]. The playbook's gate allows ≤18-month expiries, so the average wait is ~9 months (E) | **10** | $62,267 (year 5 $131k; peak with draw $99k) |
| Founder qualified leads/month | 10 | Courted, already-brokered pool; must screen kW before any supply pitch; no track record (E) | **7** | $57,043 |
| Proposal → win | 22% | Incumbent broker displacement; customer designates [B] (E) | **20%** | — |
| ARPC | $850 | DR share ≈ 0 [D, F2-S010]; true-ups [B] | **$800** | $90,022 |
| Churn | 1.2%/month | Reasonable: ~20–30% lost per 2–3-year renewal (E). Kept | 1.2% | — |

**Combined runs** (engine, base scenario with overrides):

| Case | Year 1 | Year 2 | Year 3 | Year 4 | Year 5 | Accounts at year 5 | Peak (draw) | Peak (no draw) | Breakeven |
|---|---|---|---|---|---|---|---|---|---|
| Filed base | −20.3k | 32.5k | 98.3k | 151.5k | 120.3k | 45.6 | 62.2k | 32.4k | month 13 |
| **Reviewer base** (cycle 10, leads 7, win 20%, ARPC 800) | −24.0k | −9.6k | **33.5k** | 62.8k | **105.7k** | 22.9 | **122.0k** | 46.9k | month 22 |
| Reviewer conservative (cycle 12, leads 5, win 15%, ARPC 650, churn 1.8%) | −24.0k | −20.6k | −2.7k | 14.9k | 30.4k | 10.4 | 212.6k | 59.6k | month 33 |
| Reviewer upside (cycle 8, leads 9, win 22%, ARPC 900) | −23.9k | 10.3k | 68.3k | 138.7k | 144.2k | 35.5 | 87.8k | 40.8k | month 18 |

**Working capital.** DSO of 60 days is right for remittance after the customer pays, with annual DR. Net working capital is not the problem; time to revenue is.

**Founder draw.** The standard $4k/month from month 13 is the main use of capital. In the reviewer base, operating profit does not cover the draw until about month 30. Peak funding with the draw ($122k) **exceeds the $100k conditional backing**. G1 still passes (pre-revenue capital is under $25k), but the realistic plan is part-time or unpaid until mandates are signed. The playbook's "slow-growth branch: do not draw" is the right instinct and should be the base plan.

**Year-5 dips are artefacts.** Several filed and reviewer runs show year-5 profit below year 4. That comes from the revenue-gated $6.5k/month rep hire, not economics.

**Ten-year view.** The 2.5× multiple on a supplier-terminable, consent-bound book [B, F2-S005] is reasonable to generous. Keep the 2.5× for the base case.

## 5. Customer acquisition challenge

**How incumbents sell:**
- Large private C&I buyers above 1.5 MW in ComEd buy through national consultancies, licensed brokers (392 ABCs), supplier direct teams, or in-house energy managers. Ninety-three percent of their usage is already on ARES [A, F2-S008].
- ENGIE's agreement says it "may also from time to time make contact with Customer outside the presence of Broker" [B, F2-S005].
- CSPs sell direct, and some now advertise 100% pass-through plus a revenue floor [D, F2-S010].

**What a newcomer has:** no references, no track record, no licence (which some CFOs will read as a red flag even if it is legal), and no supplier agreements until V1 passes.

**What the first 10 customers really require:**
1. Two or more supplier agreements signed despite having no state document.
2. Twenty to forty site-level conversations to yield about 10 bill sets.
3. A free capacity-tag review that finds a real, dollar-quantified error the incumbent broker missed. That is the only credible displacement trigger.
4. Expiry timing. At an average 9-month wait, the 10th fee-paying account arrives around month 24–30, not months 8–20 as in the playbook.

**A cheaper first-customer route the playbook underweights:** customer-paid flat-fee advisory. E-Quantum's model shows this exists in Illinois (DI-S026). It is equally licence-free above 1,500 kW (the statute exempts both "procure on behalf of" and "sell"). It sidesteps supplier acceptance entirely, though at lower and slower revenue. V1 should test supplier-paid fees and customer-paid fees in parallel.

## 6. Supplier and partner accessibility challenge

**Most likely to refuse:**
1. **ENGIE and other national ARES compliance teams.** Their onboarding asks for per-state licences or approvals [B, F2-S004], and the broker must warrant it holds all necessary licences [B, F2-S005]. An exempt-only firm is an unusual case. Expect "get licensed first" from some suppliers.
2. **CSPs paying a channel share.** Margins are being competed down to 100% pass-through [D, F2-S010]. Partner-share economics are MISSING for every CSP.
3. **A licensed ABC partner at a 50% split, or a licence-qualifying "compliance partner" at $1.5k/month.** No evidence either exists at those terms (E).

**Least likely to refuse:** customers paying a flat advisory fee directly, if the review finds real money.

## 7. Legal and regulatory challenge

- **Exemption.** Now statutory (F1). Still needed: the current official text after P.A. 102-958; the ICC's reading of "affiliated" (undefined); and whether mixed-size marketing lists are a solicitation of non-exempt customers.
- **Missed duty.** The 16-115C(a-5) utility non-affiliation disclosure applies to "all third-party sales representatives" (F2).
- **Deceptive-practice exposure** remains for exempt deals (Consumer Fraud Act). Never use "independent" while holding supplier agreements. The playbook handles this correctly.
- **Agency agreements are under Texas law**, with a class-action waiver [B, F2-S005]. Counsel should review venue and limitation clauses.
- **Professional advice.** One hour with Illinois utility counsel before the first mandate is cheap and necessary. The playbook's $2.5k counsel line is right; spend it after V1 and V3 pass.

## 8. Competitive response

- Incumbent brokers defend accounts by matching the capacity-tag review, which they already give away (Stage C). They can also invoke the customer-designation clause.
- Suppliers can quote the customer direct at the same price without the broker fee. ENGIE reserves the right to contact customers [B].
- CSPs undercut any DR channel fee with 100% pass-through.
- The advantage incumbents hold, which the playbook underestimates, is **supplier credit lines and volume relationships**. Better pricing access, not analytics, wins RFPs above 5 GWh.

## 9. Founder execution and delegation realism

- The founder's analytical strengths fit the work.
- The binding constraint is trust-selling to CFOs, plus surviving an 18–30-month fee lag.
- Delegation:
  - an analyst is a standard hire;
  - large-account rep productivity of 0.6 accounts a month is E, and the playbook's own sensitivity shows a weak rep loses money;
  - the book is consent-bound [B], which limits management handover and exit.
- AI dependence is negligible: bill parsing costs under $10 a month at ordinary API prices. That is correct, and it is not a moat.

## 10. Pre-mortem

| # | Failure | Early indicator | Cheapest preventive test |
|---|---|---|---|
| 1 | Suppliers will not onboard an exempt-only unlicensed broker, or onboard but quote worse than incumbents' brokers | No written yes from 2 of 3 ARES within 45 days; any "licence required" reply | V1, run in parallel with a customer-paid fee offer ($0) |
| 2 | Prospects engage but expiries are 12–30 months out; fees start in 2028–29; the draw drains backing | <30% of reviewed bills show expiry ≤12 months | V3 expiry statistic before forming the LLC; **no draw until 5 fee-paying accounts** |
| 3 | Win rate against incumbent brokers is under 15%; the founder becomes an unpaid capacity-tag auditor | 10 reviews delivered, <2 mandates | Ask in V3 for a signed letter of agency conditional on the review finding at least X dollars |

## 11. Corrected scores

| Criterion | Stage E | Stage F (F2) | Reason |
|---|---|---|---|
| fcf | 4 | **3** | Reviewer base: year 3 ~$33k, year 5 ~$106k; plateau $100–150k only after year 4 |
| roic | 6 | **5** | ~$100k steady operating profit on $47k (no draw) to $122k (with draw) at risk |
| access | 4 | **3** | Courted, already-brokered pool; customer designates broker; supplier onboarding presumes licences |
| scale | 5 | **4** | Illinois-only exempt pool; other states need licences; weak rep economics |
| resilience | 6 | 6 | Essential spend; capacity collared to May 2030 [A] |
| entry | 4 | **3** | Wedge (PLC alerts) is given away free by incumbents |
| delegation | 6 | **5** | Consent-bound, relationship-held book |
| cash | 5 | 5 | Monthly after the customer pays; annual DR |
| feasibility | 7 | 7 | Statutory exemption confirmed; P.A. 102-958 content and "affiliated" unresolved |
| ai | 6 | **5** | Back-office savings only |

**Composite:** raw **4.28**, evidence-adjusted **4.50** (evidence D). Stage E was raw 5.08 / adjusted 5.06.

**Gates:** G2 PASS (statutory). G4 WARN: $100k a year arrives only around year 5 in the reviewer base. G7 WARN: founder-held relationships until year 5+.

**Bottom line.** The licence-free route is real and now rests on statute, not just rule text. That is the one thing the playbook undersold. Everything else was oversold:
- the model starts fees four months after a lead, when they actually start at the customer's contract expiry;
- it assumes an unknown newcomer wins about ten large, already-brokered accounts a year;
- it banks a DR channel share that the market is competing to zero.

With those corrected, year 3 is about $33k and peak funding with the standard draw is about $122k. That is a slow, founder-dependent route to a $100–150k plateau. Run V1 (suppliers, plus a customer-paid fee variant) and V3 (expiry statistics) for under $500. Proceed only if both pass clearly, and do not draw until five accounts are paying.

I disagree with Stage E's year-3 base of $98k and its roic 6 and access 4 scores. I agree with its "not a strong first holding-company asset in base case" conclusion.
