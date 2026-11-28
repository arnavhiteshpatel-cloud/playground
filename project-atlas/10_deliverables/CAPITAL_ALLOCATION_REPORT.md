# Capital Allocation Report

*Project Atlas final deliverable, 2026-11-28. Read-only desk analysis: nobody was contacted and no money was spent. Citations follow EVIDENCE_STANDARDS.md as [evidence level, source ID]. Model outputs are E-level by definition and are cited by model ID, e.g. [E, WS12-014-REV]. The figures come from the post-review models `08_financial_models/<ID>-REV_*`: Stage E assumptions with the Stage F reviewer's corrected drivers applied. Those models are built with `tools/build_fin_model.py` and pass `tools/verify_fin_model.py` with 0 mismatches. The comparison is in `08_financial_models/MODEL_COMPARISON_REV.md`. "Draw" means the standardized $4,000/month owner draw from month 13.*

---

## 1. Bottom line

1. **The $100k is insurance, not a budget.** On the post-review base cases, the primary needs **$15.2k** of business capital, or **$29.3k** if the business also funds the founder's $4k/month draw from month 13 [E, WS12-014-REV]. The plan commits at most about **$35k** to the primary across the first two years, and only gate by gate. **At least $65k should stay uncommitted** throughout the cash-engine phase.
2. **The first $1,350 buys information, not a business.** An eight-week validation sprint (§8) runs the primary's decisive fee-agreement test and the cheapest tests of both alternatives. Only $600 of it is unconditional.
3. **The largest real "capital" is not in any model:** the founder's living costs for months 1–12, before the draw starts and before the first fee arrives (months 6–12) [review, 07_review/WS12-014_review.md §4]. Its size is MISSING because the founder's cost of living is unknown. The founder should hold 4–6 months of personal runway *before* month 1, separate from the backing.
4. **Capital does not buy growth in any of the four on present evidence.** In the primary, a hired recruiter at the modelled productivity *lowers* five-year operating profit (§5). In Alternative 1, launching with hired staff instead of founder labour needs $88.6k of funding and earns $5.8k in year 5 (§5). Money spent ahead of measured productivity is the main way to lose the backing.
5. **Alternative 2 (SYN-004) is the only option whose post-review base with the draw exceeds the backing:** peak funding **$122.0k** [E, SYN-004-REV]. It is fundable only if the founder takes no draw until five accounts are paying.

---

## 2. What the post-review models say

All figures are operating profit before owner pay. "Stage E base" is the pre-review figure, shown for contrast.

| Model | Case | Y1 | Y3 | Y5 | Peak funding with draw | Peak funding, no draw | First month op > 0 | Payback month |
|---|---|---|---|---|---|---|---|---|
| **WS12-014-REV** (primary) | Conservative | −$14.0k | $41.5k | $55.9k | $68.2k | $21.6k | 14 | never |
| | **Base** | −$7.7k | **$80.7k** | **$114.5k** | **$29.3k** | $15.2k | 10 | 37 |
| | Optimistic (= Stage E base) | $7.6k | $170.0k | $259.0k | $12.8k | $12.8k | 7 | 18 |
| **SYN-006-REV** (Alt 1) | Conservative | −$31.5k | $23.5k | $32.4k | $181.8k | $42.1k | 16 | never |
| | **Base** | $14.9k | **$49.7k** | **$82.6k** | **$11.5k** | $11.5k | 7 | 11 |
| | Optimistic (not reviewer-endorsed) | $70.5k | $318.4k | $724.1k | $6.1k | $6.1k | 4 | 7 |
| **SYN-004-REV** (Alt 2) | Conservative | −$25.8k | −$17.9k | −$4.6k | $291.8k | $99.8k | never | never |
| | **Base** | −$24.0k | **$33.5k** | **$105.7k** | **$122.0k** | $46.9k | 22 | never |
| | Optimistic (= reviewer upside) | −$23.9k | $68.3k | $144.2k | $87.8k | $40.8k | 18 | 51 |
| **WS04-014-REV** (reserve) | Conservative | −$34.3k | $11.6k | −$52.2k | $333.7k | $141.7k | 25 | never |
| | **Base** | −$19.4k | **$37.5k** | **$94.9k** | **$69.7k** | $23.4k | 11 | 50 |
| | Optimistic (not reviewer-endorsed) | $22.8k | $248.8k | $507.7k | $11.3k | $11.3k | 6 | 9 |

**Stage E base, for contrast (Y3 / Y5 / peak with draw):**
- WS12-014: $170.0k / $259.0k / $12.8k
- SYN-006: $94.7k / $181.5k / $10.0k
- SYN-004: $98.3k / $120.3k / $62.2k
- WS04-014: $64.0k / $128.9k / $42.4k

**What the review changed, in one line each:**
- **WS12-014:** the funnel. Conversion 30%→22%, fill 20%→15%, ramp 12→15 months, repeat revenue $670→$520 a month, churn 5%→5.5%. The reviewer's logic: the playbook's own pass mark for the decisive gate (5 of 30, i.e. 16.7%) implies a below-base funnel [review, WS12-014 §2 F2].
- **SYN-006:** price and labour. ARPC $950, 13 clients per bookkeeper, bookkeeper at $6,200 a month, outside reviewer at $1,000 a month [review, SYN-006 §4; C, F1-S001].
- **SYN-004:** a 10-month lag from mandate to first fee, because the fee starts only when the customer's current contract expires [B, F2-S005]. Also 7 leads a month, a 20% win rate and ARPC $800.
- **WS04-014:** technician cost $7,500, re-based on Chicago network-support wages [C, F4-S004]. ARPC $650 and onboarding $500, against Siotek's $399 price with free onboarding [B, F4-S003].

**Where the evidence cuts against the decision.** On post-review numbers the primary leads on year-3 profit, capital efficiency and stress survival. That much supports the orchestrator's choice. But after charging the founder's own delivery labour (the cross-model audit's founder-delivery charge, FDC: the market cost of the delivery job the founder does unpaid), its base year-5 profit is only **$21.3k**, and **$0** under the audit's harmonized rules [E, WS12-014-REV; review, CROSS_MODEL_AUDIT §3]. It is a well-paid job that needs very little capital, not a capital-absorbing asset. That is exactly why capital allocation here is mostly about *not* spending.

---

## 3. How the $100k should and should not be used

### 3.1 Principles

1. **Capital buys evidence first, then working capital, then capacity.** Each tier is unlocked by a measured result, not by elapsed time.
2. **Fund the business, not the lifestyle.** Peak funding *with* the draw exists mainly because the backing pays the founder's living costs while the business ramps. For SYN-004, $75k of the $122k peak is draw [E, SYN-004-REV]. Where the draw cannot be covered, slow the draw rather than draw down the backing.
3. **Stop rather than borrow in a downturn.** A 2009-type year during the ramp pushes the primary's peak funding to $140.7k [E, WS12-014-REV; review, WS12-014 §4]. Its perm benchmark fell 57% in 2009 [A, E-WS12014-S011].
4. **No hire before productivity is measured on the founder's own book**, in any of the four.
5. **One launch at a time.** Every option is founder-hours-bound. Running two launches spends capital and time on two half-businesses.

### 3.2 Should not be used for

- paid leads, bulk contact-data licences, big job-board contracts, or office space before a second producer (the playbook's own exclusions);
- **any hire in the primary while trailing-6-month revenue is under $20k/month.** The REV base reaches only $7.1k at month 24 and $12.6k at month 60, so that hire never comes in base [E, WS12-014-REV];
- launching SYN-006 with a hired bookkeeper from client 1, or before measuring price (median ≥$950) and productivity (≤10 hours per client) (§5);
- funding SYN-004's owner draw before five fee-paying accounts [review, SYN-004 §10];
- annual software or tool commitments before monthly LOIs exist (WS04-014);
- acquisitions in years 1–2. The mandate excludes them as an entry route, and none is funded from cash flow before year 4 in base (see LONG_TERM_WEALTH_REPORT).

### 3.3 Allocation by purpose (primary path, base case)

| Purpose | Amount | When | Source of figure |
|---|---|---|---|
| Validation | ≤$500 for the primary, ≤$1,350 including the alternatives' tests | Weeks 1–8 | Playbook §4.2; §8 below |
| Launch (LLC, attorney fee-agreement review, CRM, laptop and website) | ≈$4.2k | Only after test 3 passes | ≈$1,500 legal (E), $2,500 equipment, ~$150 LLC (confirm) [playbook §8] |
| Operating losses to breakeven, months 1–10 (tools ≈$940/month) | ≈$11k | Months 1–10 | Covered by the $15.2k no-draw peak [E, WS12-014-REV] |
| Working capital (receivables, DSO 40) | ≈$13k of receivables at year 3; funded from fees, not backing | Year 2 onward | [E, WS12-014-REV] |
| Draw bridge (months 13–20, until profit covers $4k/month) | ≈$14k | Months 13–20 | Peak with draw $29.3k minus $15.2k without |
| Cash reserve: 3 months of business cash costs | ≈$7–8k | Held from first fee | Model reserve rule (3 months base) |
| Growth capital (recruiter #1 ramp, ≈6 × $6,900) | $0 planned; ≈$41k only if the boutique gate passes | Not before month 24 | §4.1 tier $25–50k |
| **Uncommitted** | **≥$65k** | Always | Insurance against a cycle; the month-24 decision; seed for the holding company |

---

## 4. Evidence gates by tier

Each tier's money is released only when the gate is met. The gates incorporate the Stage F reviewers' tightening.

### 4.1 Primary: WS12-014 (controls/automation contingency desk)

| Tier | Buys | Evidence gate (post-review) | How it is lost |
|---|---|---|---|
| **$0–500** | Role-map refresh; Recruiter Lite for 2 months ($170/month [D, E-WS12014-S022]); mileage | None. Tests 1–3 (§8) | A subscription with no replies |
| **$500–2k** | LLC; attorney review of the fee agreement and the candidate-ownership and guarantee clauses (≈$1,500, E); CRM month | **Test 3 passes:** ≥5 signed agreements at ≥18% from 30 conversations. Plus ≥5 movable candidates at ≥$100k. Note that a bare pass implies the REV base (≈$81k in year 3), not the Stage E base | Paperwork for a desk that never places |
| **$2–5k** | Laptop, headset, website ($2,500); first months of the full tool stack | ≥2 candidates in active interview processes. A senior controls engineer or hiring manager confirms the founder's technical screen is credible (consult cost MISSING) [review §3] | No final rounds after 8 submittals |
| **$5–10k** | Tools and insurance runway to month 10; E&O/GL (premium MISSING) | ≥1 candidate in a final round by month 4. The founder holds 4–6 months of personal runway | A fallout or cancelled search wipes out the first fee |
| **$10–25k** | Receivables float; 3-month reserve; the draw bridge (the REV peak of $29.3k falls here) | **≥1 fee ≥$15k collected by month 10, otherwise stop.** Then ≥3 collected fees and DSO ≤60 | A fee dispute; slow payers. Budget for one collections action in 24 months [review §7] |
| **$25–50k** | Recruiter #1 (an experienced controls recruiter, not a junior) | Trailing-6-month revenue ≥$20k/month; ≥8 open searches; reserve held; Tier A/B postings not falling two quarters running. **And** the hire has a verifiable record equivalent to ≥0.7 new clients/month (§5) | A wash-out hire (assume 50% odds, E); a cycle turn mid-ramp |
| **$50–100k** | Not for this business as modelled. Contract engineering staffing needs its own payroll-float model (MISSING) | Only after a separate model, and recruiter #1 producing ≥$60k of collected fees in 9 months | Two salaries on payroll into a downturn |

### 4.2 Alternative 1: SYN-006 (construction back office: WIP/job-cost books plus certified payroll)

| Tier | Buys | Evidence gate (post-review) | How it is lost |
|---|---|---|---|
| **$0–500** | Award-list pulls; WIP workbook and IDOL template mapper, built before 5 Dec; postage | None. Test 1 (8 surety producers) and test 2 (20 owners) | Time only |
| **$500–2k** | **Paid review of the founder's two sample WIPs plus one certified payroll (≈$500, E)**, as a hard prerequisite [review §5]. LLC $150 and assumed name $120 [A, E-SYN006-S014] | Test 2: ≥6 of 20 owners had a surety or bank WIP request in the last 12 months, and ≥5 spend ≥$700/month. The skill gate is passed by the second attempt | Skill gate fails twice: stop |
| **$2–5k** | Counsel on how the duty to file certified payroll is allocated (SB1344 agent liability [C, C5-S019]); E&O/cyber with the penalty-exclusion language read ($500–1,500 counsel, E); CFMA ($500) | ≥3 paid $450 checks within 60 days, **≥2 of them from cold outreach** [review §5]. Counsel and E&O in place **before** the first certified-payroll engagement | An E&O exclusion for fines; a classification dispute |
| **$5–10k** | Cash buffer for the month-1–6 trough | ≥2 monthly clients at **≥$950** (raised from $900) | Slow conversion |
| **$10–25k** | Bookkeeper #1, hired 1–3 months early | ≥5 signed monthly clients at median ARPC ≥$950. Time-tracked ≤10 hours per client after month 3. ≥11 clients | Labour +20% turns REV year 3 to −$8.6k [E, SYN-006-REV] |
| **$25–50k** | Compliance specialist and senior reviewer | ≥25 clients; ≥13 clients per bookkeeper *measured*; ≥90% on-time filings | Hiring 30% sooner: REV year 3 −$86.8k |
| **$50–100k** | Not justified on post-review evidence. The reviewer's ceiling is about $150k a year [review §1] | — | — |

### 4.3 Alternative 2: SYN-004 (large-C&I energy cost management, licence-exempt above 1,500 kW)

| Tier | Buys | Evidence gate (post-review) | How it is lost |
|---|---|---|---|
| **$0–500** | V1 supplier enquiries, plus a customer-paid flat-fee variant [review §5]; V2 demand-response provider (CSP) terms; screened list | None | Time only |
| **$500–2k** | LLC, CRM, domain | V1: ≥2 written supplier yeses despite no state licence document [B, F2-S004]. V3: ≥4 LOAs or bill sets, and **≥30% of reviewed bills expiring within 12 months** [review §10] | Suppliers decline at onboarding |
| **$2–5k** | Counsel to read the current 16-115C text (P.A. 102-958 is unread [D, F2-S002]) and the meaning of "affiliated"; E&O; kW data logger | ≥2 supplier agreements; ≥1 RFP mandate | Counsel finds the exemption narrower than assumed |
| **$5–10k** | Tools and travel to the first remittance | A supplier confirmation letter showing the fee in mils | The contract starts late; fees are withheld [B, F2-S005] |
| **$10–25k** | Runway with **no draw** | ≥3 signed accounts | Win rate below 15% |
| **$25–50k** | Draw bridge. The REV no-draw peak of $46.9k sits here | **≥5 fee-paying accounts** before any draw [review §10]. Starting the draw at month 25 instead of 13 cuts peak funding from $122.0k to $74.0k [E, SYN-004-REV] | The draw outlasts growth (the conservative case: $291.8k) |
| **$50–100k** | ABC licence, compliance partner, first rep | ≥$25k/month revenue, which the REV base does not reach within 5 years | A weak rep loses money [review §9] |

**Reserve, WS04-014 (dental managed IT).** Tier $0–500 holds the referral-partner test as the first kill gate (≈$50) and the paid-wedge test (≤$400) [review §11]. No insurance until a deposit is paid. No technician until 18 practices: the reviewer's rule, which cuts REV peak funding from $69.7k to $38.8k [E, WS04-014-REV variant]. Insurer and attorney sign-off on BAA liability comes before the first monthly contract.

---

## 5. Potential return on deployed capital

| Model (REV base) | Y3 op ÷ peak with draw | Y3 op ÷ peak, no draw | Y5 op after FDC ÷ peak, no draw | 5-yr cumulative owner cash (FCF before draw) | Return mostly from |
|---|---|---|---|---|---|
| WS12-014 | 2.8× | 5.3× | 1.4× ($21.3k ÷ $15.2k) | $269k | Founder's own billing |
| SYN-006 | 4.3× | 4.3× | negative (−$1.2k) | $244k | Founder's bookkeeping labour |
| SYN-004 | 0.27× | 0.71× | 0.53× ($24.7k ÷ $46.9k) | $128k | Founder's analysis and selling |
| WS04-014 | 0.54× | 1.6× | negative (−$6.4k) | $228k | Founder as technician |

[E, <ID>-REV; FDC per CROSS_MODEL_AUDIT §3, using the REV role costs: recruiter $6,900, bookkeeper $6,200, analyst $6,000, technician $7,500]

**How to read this table:**
- The headline ratios are very high because the capital is tiny. They are not evidence of a capital-compounding business. Once the founder's labour is priced, every option's year-5 return on capital is modest or negative.
- **Incremental returns on *growth* capital are worse than average returns.** Each finding below is an engine run on the REV models:
  - **WS12-014.** In the optimistic case, hiring recruiter #1 (month 35) at the modelled 0.35 new clients/month changes operating profit by −$14.6k (Y3), −$32.0k (Y4) and −$1.7k (Y5). The hire adds value only at ≥0.7 new clients/month, giving +$122.8k in Y5. That is about the modal established network recruiter's 9–12 placements a year [D, F5-S006].
  - **SYN-006.** Replacing founder delivery with a bookkeeper from client 1 gives Y3 −$22.7k and Y5 $5.8k, with peak funding of $88.6k even without the draw.
  - **WS04-014.** Hiring the first technician at 18 practices instead of 14 *raises* Y5 to $111.7k.

  In every case capital creates value by being withheld until density exists, not by being deployed early.

---

## 6. Downside exposure

### 6.1 Stress tests (REV base; the engine's 17 standard stresses)

| | WS12-014 | SYN-006 | SYN-004 | WS04-014 |
|---|---|---|---|---|
| Base Y3 op | $80.7k | $49.7k | $33.5k | $37.5k |
| Win rate −40% | $42.2k | $104.8k* | $11.8k | $1.9k |
| Recession (new −30%, churn ×1.5) | $43.6k | $105.2k* | $15.4k | −$0.1k |
| Labour +20% | $80.7k | **−$8.6k** | $32.8k | $18.4k |
| Hires 30% sooner | $80.7k | **−$86.8k** | $23.9k | $21.5k |
| Growth twice as slow | **$17.1k** | $68.2k | −$1.1k | $34.7k |
| Worst peak funding (test) | $132.6k (growth twice as slow) | $653.7k (hires sooner) | $198.7k (growth twice as slow) | $278.5k (hires sooner) |
| Stresses with peak > $100k | 1 of 17 | 3 of 17 | **all 17** | 4 of 17 |

\* Lower demand defers hires, so the founder works unpaid. This is founder wage, not resilience [review, CROSS_MODEL_AUDIT §2].

**Supplementary downturn runs for the primary** [E, WS12-014-REV; review §1]:

| Scenario | Y3 | Y5 | Peak funding |
|---|---|---|---|
| 2023-type downturn | $50.0k | $64.2k | $42.2k |
| 2009-type collapse | $19.1k | $22.3k | $140.7k |
| Fee 18% × 80% realization | $69.2k | $100.5k | $34.2k |

### 6.2 Maximum plausible loss

| | Gate-disciplined loss (stops at the first failed gate) | If gates are ignored (conservative peak with draw) | Worst single stress (peak) |
|---|---|---|---|
| WS12-014 | **≈$600–1,500** at day 60. **≈$15–22k** if no fee by month 10 (the no-draw peak range in base and conservative) | $68.2k | $140.7k (2009-type) |
| SYN-006 | **≈$600** (skill gate or tests 1–2 fail). ≈$12–15k after launch | $181.8k | $653.7k |
| SYN-004 | **≈$0–500** (V1 fails) | $291.8k | $198.7k (base); the conservative case is worse |
| WS04-014 | **≈$400** | $333.7k | $278.5k |

**The maximum plausible loss of the recommended plan is about $35k:** the primary's tiers up to $10–25k plus validation. That exposure is reached only if the desk places, then stalls. It requires breaching the "first fee by month 10" stop to go higher. Loss above $35k comes only from funding the draw through a downturn, or from hiring ahead of evidence. Both are prohibited above.

---

## 7. Financing alternatives

| Option | Fit | Evidence |
|---|---|---|
| **No external financing (recommended for the primary)** | The base no-draw peak of $15.2k fits inside the backing with large headroom | [E, WS12-014-REV] |
| **Customer prepayment** | **Strong** for SYN-006: ACH in advance, DSO 8 days, negligible working capital [D, model; review §4 "verified"]. **Strong** for WS04-014: monthly service billed in advance, DSO −10 days (E); hardware projects at 50% deposit. **None** for SYN-004: the supplier remits on the 25th only after the customer pays [B, F2-S005]. **Primary:** contingency fees are paid only on start. Retained or engaged search (part paid upfront) needs a reputation, so it is a year-2+ option (playbook §6.6) | as cited |
| **Factoring of recruiting receivables** | **Not needed.** REV base receivables are about $13k at year 3. Perm invoices are single, lumpy and subject to guarantee fallout and disputes, which makes them weak collateral (E). Factoring terms and availability for perm fees are MISSING from Atlas evidence. Factoring becomes relevant only if the month-24 decision adds contract engineering staffing, where payroll is paid weekly before clients pay. That needs its own model | MISSING |
| **Seller financing or earn-out (later acquisitions only)** | Insurance-book deals run 20–50% down, with a retention-based earn-out over about 3 years [C, C5-S021] | as cited |
| **Personal credit, HELOC, cards** | **Do not use** to fund draws or a downturn. The review's rule: "stopping, not borrowing" [review, WS12-014 §4] | — |
| **SBA or bank acquisition loans** | Not researched in Atlas: MISSING. Research before any year 3–5 acquisition | MISSING |

---

## 8. Combined validation sprint, weeks 1–8 (30 Nov 2026 – 24 Jan 2027)

**Purpose:**
- run the primary's decisive gate, its test 3;
- run the cheapest disconfirming test of each alternative;
- keep the reserve's first kill gate ready.

The founder executes everything; this research contacted no one.

| Week | Primary: WS12-014 (≈70% of hours) | Alt 1: SYN-006 (≈15%) | Alt 2: SYN-004 (≈10%) | Reserve: WS04-014 |
|---|---|---|---|---|
| 1 (to 6 Dec; heavy AI ends 5 Dec) | Build the ATS role-map scripts, outreach templates and technical-screen scenario bank with AI. Refresh the role map (test 1, $0) | Build the WIP workbook and IDOL certified-payroll mapper with AI | Build the bill-parsing template; draft the V1/V2 enquiries | — |
| 2–3 | Test 2: 60 candidate approaches (Recruiter Lite month 1, $170) | Test 1: 8 surety-producer interviews ($0) | Send V1 (3 suppliers, plus the customer-paid variant) and V2 (CSPs) ($0) | — |
| 3–8 | **Test 3: 30 hiring-manager conversations about specific anonymized candidates** (Recruiter Lite month 2, $170; mileage $100) | Weeks 4–6: test 2, 20 owner discovery calls (≤$100) | Weeks 5–6: V1 replies due (ENGIE replies within 15 business days [B, DI-S027]) | If test 3 trends to fail by week 5: experiment 1, 5 referral-partner chats (≈$50) |
| 6–8 | Submittals to signed agreements; log conversion | **Only if tests 1–2 pass:** paid skill-gate review of 2 WIPs and 1 certified payroll (≈$500) | **Only if V1 brings ≥1 yes:** V3 partial, collecting bill sets and expiry statistics (≈$200) | — |
| 8 | **Decision meeting** (below) | | | |

**Budget:**

| Item | Unconditional | Conditional |
|---|---|---|
| WS12-014: Recruiter Lite 2 × $170 [D, E-WS12014-S022]; mileage and coffee $100 (E); ISA meeting allowance $60 (cost MISSING) | $500 | — |
| SYN-006: discovery postage and travel (E) | $100 | — |
| SYN-006: paid construction-controller review (E; rate MISSING) | — | $500 |
| SYN-004: enquiries $0; V3 travel and data (E) | — | $200 |
| WS04-014: partner chats (E) | — | $50 |
| **Total** | **$600** | **$750** → **ceiling $1,350** |

Not in the sprint: LLCs, E&O, attorney review (≈$1,500), paid $450 checks. All of these come after a pass.

**Decision rules at week 8:**
1. **WS12-014 test 3 passes** (≥5 signed at ≥18%): launch the primary (tier $500–2k). Record the alternatives' evidence and park them until the month-24 decision. Do not run a second launch.
2. **Test 3 fails, SYN-006 passes tests 1–2 and the skill gate:** switch to SYN-006, starting with certified payroll.
3. **Test 3 fails, SYN-004 V1 brings ≥2 written yeses and the V3 expiry share is ≥30% within 12 months:** SYN-004 only as a no-draw build. Alternatively, keep recruiting income while SYN-004's fee lag runs.
4. **All fail:** run WS04-014's experiments 1–3 (≤$400), then the validation candidates WS05-007, SYN-001 and WS13-014.

**Sprint maximum loss:** $1,350. The expected loss if everything fails early is about $600.

---

## 9. Summary: what is committed and what stays free

| Phase | Primary path committed (cumulative) | Uncommitted |
|---|---|---|
| Weeks 1–8 | ≤$1,350 | ≥$98.6k |
| Months 3–10 (launch to first fee) | ≈$15–17k (the no-draw peak) | ≈$83k |
| Months 13–20 (draw bridge, REV base) | ≈$29–35k including the reserve | **≈$65k** |
| Month 24 decision | Business is self-funding in REV base. Cumulative retained turns positive in month 37 | ≥$65k, available for a durable asset (see LONG_TERM_WEALTH_REPORT) |

**Most of the $100k should never be committed to the cash engine.** Its job is to absorb a cycle the primary cannot survive alone ($140.7k peak in a 2009-type year), and to give the founder the option, at month 24 or later, to buy into a durable recurring-revenue business with evidence in hand.
