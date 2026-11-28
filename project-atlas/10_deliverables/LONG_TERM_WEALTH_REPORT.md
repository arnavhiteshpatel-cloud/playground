# Long-Term Wealth Report

*Project Atlas final deliverable, 2026-11-28. Read-only desk analysis; nobody was contacted. Citations follow EVIDENCE_STANDARDS.md as [evidence level, source ID]. Model outputs are E-level and are cited by model ID, e.g. [E, WS12-014-REV]. The post-review ("-REV") models are the Stage E models with the Stage F reviewers' corrected drivers applied (`08_financial_models/<ID>-REV_*`). They are built by `tools/build_fin_model.py`, verified in LibreOffice with 0 mismatches, and compared in `MODEL_COMPARISON_REV.md`. The harmonized view applies the cross-model audit's rules H1–H9 to the -REV base. The founder-delivery charge (FDC) subtracts the market cost of the delivery job the founder does unpaid (`07_review/CROSS_MODEL_AUDIT.md` §3). Helper scripts are in `/tmp/claude-0/atlas_scratch/WEALTH/`.*

---

## 1. Bottom line

1. **None of the four is, on its own, the foundation of a holding company.** In the post-review base case each one is a founder's well-paid job:
   - year-5 operating profit before owner pay of $83–114k;
   - year-5 owner cash (draw plus distributable) of $67–97k a year.
   - After pricing the founder's own delivery labour, year-5 profit is between **−$6k and +$25k** [E, all -REV].
2. **The primary (WS12-014) is the best *engine* and the weakest *asset*.**
   - *Engine:* the highest post-review year-3 and year-5 profit, the smallest capital at risk, and the most stress-robust year 3.
   - *Asset:* the lowest delegation and resilience scores (3 and 3) [review, 07_review/WS12-014_review.md §11], and the lowest exit value ($206k at year 10; about $44k after FDC).
   - **Its job in the plan is to produce deployable cash and a track record, not to be compounded.**
3. **Reinvesting inside the engine does not pay at modelled productivity.**
   - A second recruiter at 0.35 new clients/month *reduces* year-3 to year-5 profit (−$14.6k, −$32.0k, −$1.7k). It pays only at about 2× that productivity [E, WS12-014-REV].
   - So the default is to **harvest and redeploy**.
4. **The durable asset is most likely bought, not built, in years 4–6 of the base case.**
   - In the post-review base, the primary has paid back the backing and accumulated **$69k of net deployable capital by year 5**. The optimistic case reaches $98k by year 3.
   - Building Alternative 1 (SYN-006) with hired staff loses money unless realized price is at least about $1,100 a month [E, SYN-006-REV staffed variant].
5. **No from-scratch option shows evidence of $500k–$1M a year of owner cash within 5 years.**
   - Only the not-reviewer-endorsed optimistic cases of SYN-006 and WS04-014 reach it.
   - The realistic route to $500k+ is several managed businesses by years 8–12 (§9).

---

## 2. The four as holding-company foundations

**Measures in the table:**
- Base = REV base.
- Harmonized = audit rules H1–H9 applied to REV base.
- "Owner cash" = after-tax free cash flow before the owner draw. It equals the draw plus distributable surplus, net of any capital consumed.

| Criterion | WS12-014 recruiting desk | SYN-006 construction back office | SYN-004 C&I energy | WS04-014 dental MSP (reserve) |
|---|---|---|---|---|
| Owner cash in year 5 (per year): base / harmonized | $93.0k / $78.7k | $66.6k / $24.5k | $97.1k / $89.8k | $88.2k / $102.8k |
| Y5 op after FDC: base / harmonized | $21.3k / $0.0k | −$1.2k / −$63.3k | $24.7k / $16.5k | −$6.4k / $1.3k |
| Return on capital: Y5 op after FDC ÷ peak funding with no draw | 1.4× | negative | 0.53× | negative |
| Incremental return on growth capital | Negative at the modelled recruiter productivity (0.35/month). Positive only at ≥0.7/month (§5) | Negative for a staffed launch at $950. Positive at ≥$1,050–1,150 (§5) | A rep below 0.4 accounts/month costs ~$78k a year for <$41k of fees [playbook §8] | Positive if hiring follows density: a technician at 18 practices gives Y5 $111.7k vs $94.9k at 14 |
| 10-yr cumulative deployable: base / harmonized | **$316k** / $208k | $104k / $24k | $239k / $189k | $217k / **$230k** |
| Delegation (Stage F score) | 3. Founder-bound; non-competes void below $75k ($80k from 2027) [A, E-WS12014-S006] | 5. Founder keeps ~12 clients to year 5 | 5. Consent-bound relationships [B, F2-S005] | **6.** Standard technician roles |
| Resilience (Stage F score) | **3.** Perm recruiting fell 57% in 2009 and 21.7% in 2023 [A, E-WS12014-S011, S009] | 6. Statutory demand, construction-cyclical | 6. Essential spend; capacity prices collared to May 2030 [A, E-SYN004-S008] | 6. Recurring, prepaid |
| Revenue recurrence | Low: non-exclusive job orders; 5.5%/month client churn (E) | Monthly retainer; incumbent retention 82–83%/yr [A, WS02-S022] | Residuals; terminable per account [B, F2-S005] | 12-month prepaid contracts (E) |
| Year-10 EV: base multiple / harmonized | $206k (1.5×) / $168k | $275k (2.5×) / $61k | $317k (2.5×) / $292k | **$475k** (3.5×) / **$369k** |
| Year-10 EV after FDC (base multiple) | ≈$44k | ≈$33k | ≈$82k | ≈$63k |
| Capital at risk: peak with draw / no draw | $29.3k / $15.2k | **$11.5k** / **$11.5k** | $122.0k / $46.9k | $69.7k / $23.4k |

**Reading:**
- On every measure of *durability* (recurrence, delegation, resilience, exit value), the primary ranks last or tied-last. On *cash speed and capital efficiency* it ranks first or second.
- WS04-014, only the reserve, is the strongest *asset* on paper: the best delegation and exit value, and the best harmonized 10-year accumulation. But its post-review year 3 is only $37.5k, and its conservative case loses $333.7k with the draw.
- SYN-006 collapses under harmonization. The audit's conversion cap (H2) and the cuts to its long-term drivers take its 10-year deployable to $24k.
- **This is the main evidence against treating the primary as the long-term core.** The orchestrator's framing already reflects it: a 2–3-year cash engine with a month-24 decision.

---

## 3. Scenario tables: 3, 5 and 10 years

**Column definitions:**
- **Op** = operating profit in that year, before owner pay.
- **After FDC** = Op minus 12 × the delivery role's REV monthly cost × 1.03^(year−1). The REV role costs are recruiter $6,900, bookkeeper $6,200, analyst $6,000 and technician $7,500.
- **Owner cash** = cumulative after-tax FCF before draw over years 1–N. It can be negative: that is capital consumed.
- **Deployable** = the engine's cumulative positive surplus after draw, tax, reinvestment and reserves.
- **EV** = Op × the model's multiple.

Years 6–10 use each model's long-term drivers. These are mostly E-level, and harmonization caps them [review, CROSS_MODEL_AUDIT §1]. All figures are in $k.

### 3.1 Year 3

| Model | Case | Op | After FDC | Owner cash, Y1–3 | Deployable | EV |
|---|---|---|---|---|---|---|
| WS12-014 | Conservative | 41.5 | −46.4 | 28.3 | 0 | 41.5 |
| | **Base** | **80.7** | −7.1 | 93.9 | 22.2 | 121.0 |
| | Optimistic | 170.0 | 82.2 | 207.9 | 109.6 | 340.0 |
| | Harmonized | 71.1 | −16.7 | 86.6 | 17.5 | 106.7 |
| SYN-006 | Conservative | 23.5 | −55.5 | −15.8 | 0 | 35.2 |
| | **Base** | **49.7** | −29.3 | 129.2 | 21.6 | 124.2 |
| | Optimistic | 318.4 | 239.5 | 430.8 | 227.7 | 1,114.5 |
| | Harmonized | 108.6* | 29.7 | 144.3 | 24.0 | 271.6 |
| SYN-004 | Conservative | −17.9 | −94.2 | −80.9 | 0 | ≈0 |
| | **Base** | **33.5** | −42.9 | −22.8 | 0 | 83.7 |
| | Optimistic | 68.3 | −8.1 | 19.5 | 0 | 170.7 |
| | Harmonized | 32.1 | −44.2 | −23.8 | 0 | 80.4 |
| WS04-014 | Conservative | 11.6 | −83.9 | −42.2 | 0 | 28.9 |
| | **Base** | **37.5** | −58.0 | 33.5 | 0 | 131.1 |
| | Optimistic | 248.8 | 153.3 | 346.9 | 187.3 | 1,119.5 |
| | Harmonized | 14.0 | −81.5 | 12.7 | 0 | 41.9 |

\* A hiring-step artefact: lower demand defers hires, so the founder works unpaid [review, CROSS_MODEL_AUDIT §4].

### 3.2 Year 5

| Model | Case | Op | After FDC | Owner cash, Y1–5 | Deployable | EV |
|---|---|---|---|---|---|---|
| WS12-014 | Conservative | 55.9 | −37.2 | 132.7 | 7.5 | 55.9 |
| | **Base** | **114.5** | **21.3** | 269.3 | 100.3 | 171.7 |
| | Optimistic | 259.0 | 165.8 | 529.4 | 300.8 | 518.0 |
| | Harmonized | 93.2 | 0.0 | 237.2 | 71.3 | 139.8 |
| SYN-006 | Conservative | 32.4 | −51.4 | 10.2 | 0 | 48.6 |
| | **Base** | **82.6** | −1.2 | 244.0 | 21.6 | 206.4 |
| | Optimistic | 724.1 | 640.3 | 1,277.6 | 857.6 | 2,534.3 |
| | Harmonized | 20.4 | −63.3 | 198.1 | 24.0 | 51.0 |
| SYN-004 | Conservative | −4.6 | −85.6 | −99.8 | 0 | ≈0 |
| | **Base** | **105.7** | **24.7** | 127.9 | 47.3 | 264.3 |
| | Optimistic | 144.2 | 63.2 | 227.0 | 92.7 | 360.5 |
| | Harmonized | 97.5 | 16.5 | 116.2 | 39.6 | 243.8 |
| WS04-014 | Conservative | −52.2 | −153.5 | −141.7 | 0 | n/m |
| | **Base** | **94.9** | −6.4 | 228.3 | 69.0 | 332.0 |
| | Optimistic | 507.7 | 406.4 | 999.9 | 664.7 | 2,284.7 |
| | Harmonized | 102.6 | 1.3 | 198.4 | 74.2 | 307.8 |

### 3.3 Year 10

| Model | Case | Op | After FDC | Owner cash, Y1–10 | Deployable | EV |
|---|---|---|---|---|---|---|
| WS12-014 | Conservative | 57.5 | −50.5 | 398.2 | 11.1 | 57.5 |
| | **Base** | **137.3** | 29.3 | 749.5 | **316.4** | 206.0 |
| | Optimistic | 310.7 | 202.6 | 1,516.6 | 1,015.8 | 621.3 |
| | Harmonized | 111.8 | 3.7 | 637.5 | 207.6 | 167.7 |
| SYN-006 | Conservative | 35.2 | −61.9 | 168.0 | 0 | 52.7 |
| | **Base** | **110.1** | 13.0 | 630.8 | 104.3 | 275.2 |
| | Optimistic | 1,156.5 | 1,059.5 | 4,416.4 | 3,597.8 | 4,047.9 |
| | Harmonized | 24.5 | −72.6 | 303.0 | 24.0 | 61.2 |
| SYN-004 | Conservative | −4.6 | −98.5 | −122.8 | 0 | ≈0 |
| | **Base** | **126.8** | 32.9 | 585.6 | 239.4 | 317.1 |
| | Optimistic | 173.0 | 79.0 | 822.6 | 419.5 | 432.5 |
| | Harmonized | 117.0 | 23.0 | 531.5 | 189.4 | 292.4 |
| WS04-014 | Conservative | −56.7 | −174.1 | −419.1 | 0 | n/m |
| | **Base** | **135.6** | 18.1 | 664.6 | 216.5 | 474.5 |
| | Optimistic | 905.6 | 788.2 | 3,305.7 | 2,595.7 | 4,075.3 |
| | Harmonized | 123.1 | 5.6 | 625.4 | 229.6 | 369.2 |

**How the optimistic cases were set:**
- *WS12-014:* the Stage E base. The reviewer said "the Stage E base becomes the optimistic case".
- *SYN-004:* the reviewer's upside case.
- *SYN-006 and WS04-014:* the Stage E optimistic cases with only cost corrections applied. **No reviewer endorses them.** The SYN-006 reviewer puts its ceiling at about $150k a year [review, SYN-006 §1].

### 3.4 The audit's Stage E harmonized view, for reference

These figures are from the audit, before the reviewers' corrections [review, CROSS_MODEL_AUDIT §4].

| Model | Y3 op, harmonized | Y5 op, harmonized | Y5 after FDC | 10-yr deployable | Y10 EV |
|---|---|---|---|---|---|
| WS12-014 | $163k | $178k | $84k | $665k | $426k |
| SYN-006 | $151k* | $105k | $26k | $251k | $314k |
| SYN-004 | $81k | $138k* | $57k | $387k | $413k |
| WS04-014 | $39k | $143k* | $55k | $406k | $515k |

**The two corrections compound.** The audit harmonizes optimism *across* models; the reviewers correct each model's drivers *within* it. Stacking both, the -REV harmonized year-5 after-FDC figures are $0, −$63k, $17k and $1k. The audit's own conclusion survives and hardens: "no finalist reaches $100k/yr of harmonized Y5 operating profit" after FDC.

---

## 4. Capital accumulation: what the engine actually produces

**Net deployable capital** is cumulative surplus after the draw, tax, reinvestment and reserves. Here the early deficits are netted, i.e. it is shown after repaying the backing. Figures for the primary, $k [E, WS12-014-REV]:

| End of year | 1 | 2 | 3 | 4 | 5 | 7 | 10 |
|---|---|---|---|---|---|---|---|
| Conservative | −26.7 | −67.0 | −77.0 | −76.2 | −69.5 | −66.6 | −66.7 |
| **Base** | −18.9 | −31.6 | **−9.3** | 24.4 | **68.8** | 146.6 | 284.9 |
| Optimistic | −12.0 | 23.7 | **97.6** | 161.2 | 288.8 | 550.8 | 1,003.8 |

**On top of this:**
- The founder receives the $48k/year draw from month 13.
- The business holds its reserve (3 months of cash costs: about $8.5k in base at year 5).

**What this means for timing:**
- **Base:** the engine finishes repaying its own funding in year 4 (cumulative retained turns positive in month 37). It has about $69k to deploy by the end of year 5.
- **Optimistic:** $98k by year 3.
- **Conservative:** never self-funds. The month-10 "first fee" and month-24 gates exist to stop this case before it consumes $68k.

**Month-24 check:**
- The boutique trigger is trailing-6-month revenue of at least $20k/month.
- In base, trailing-6-month revenue is $7.1k at month 24, $9.6k at month 36 and $12.6k at month 60, so the trigger is never met.
- In the optimistic case it is $15.1k at month 24 and $19.9k at month 36.
- **The base-case month-24 decision is therefore "keep the solo desk running and harvest", not "build a boutique".**

---

## 5. Incremental returns: reinvest inside, or redeploy outside?

**WS12-014: recruiter hire.** Optimistic case; hire at month 35 at the model's $6,900/month all-in.

| Recruiter productivity (new clients/month) | ΔY3 | ΔY4 | ΔY5 | Y5 op (desk) | Hired recruiters at month 60 |
|---|---|---|---|---|---|
| 0.35 (model) | −$14.6k | −$32.0k | −$1.7k | $259.0k | 1 |
| 0.5 | −$14.6k | −$18.3k | +$10.1k | $270.7k | 2 |
| 0.7 | −$14.6k | −$16.1k | **+$122.8k** | $383.5k | 3 |
| 1.0 | −$14.6k | +$21.5k | +$443.4k | $704.0k | 3 |

- 0.7 new clients a month is about 8 first placements a year, plus repeats. That sits in the modal 9–12-placements band of *established* network recruiters [D, F5-S006].
- Top-quartile recruiters average 5.21 placements against 1.38 for the rest (period unstated) [D, F5-S007].
- **A hire is worth making only if the candidate has a verifiable record at that level.** Such recruiters will cost more than $6,900 a month, which the table does not price.
- Non-competes are void below $75k/$80k [A, E-WS12014-S006], so the producer can leave with clients.

**SYN-006: launch with hired staff instead of founder delivery.** REV drivers, first bookkeeper at the first client, no owner draw.

| Realized ARPC | Y5 op | Peak funding |
|---|---|---|
| $950 (REV base) | $5.8k | $88.6k |
| $1,050 | $73.3k | $45.4k |
| $1,150 | $145.5k | $43.1k |
| Stage E drivers ($1,000; 15 clients per bookkeeper at $5,800) | $122.7k | $40.1k |

- Each $100 of monthly price is worth about $70k of staffed year-5 profit.
- **Launching Alternative 1 with hired staff only makes sense once a founder-run pilot has *measured* median ARPC ≥$1,100 and ≥13 clients per bookkeeper.** The Stage F gate of ≥$950 is not enough for the staffed version [E, SYN-006-REV variants].
- The ARPC evidence today is D-level, and an offshore competitor sells dedicated construction bookkeepers from $999 [D, C5-S035].

**WS04-014.** Hiring to density (18 practices rather than 14) raises base year 5 from $94.9k to $111.7k and 10-year deployable from $216k to $298k [E, WS04-014-REV]. This is the only one of the four where internal reinvestment at the modelled rates clearly beats waiting, and only when hires follow density.

**SYN-004.** The book is consent-bound, and rep productivity is E. A rep is justified only above $25k/month of revenue, which the REV base does not reach within five years.

---

## 6. Sequencing strategy

### 6.1 The plan

**Phase 1: cash engine (months 0–36).**
- Validate the primary (8-week sprint), then run the solo desk.
- No hires unless the boutique gate is met with an experienced producer.
- Every dollar above the reserve goes to a separate holding account once the engine has repaid its funding (year 3–4 in base).

**Phase 2: accumulate and prepare (years 2–5).** While recruiting, the founder builds the next asset's evidence cheaply:
- *Keeps* the SYN-006 option alive through the CFMA and surety relationships, which recruiting does not provide. The realistic option is to buy rather than build.
- *Screens* acquisition targets: small bookkeeping and payroll practices, or an insurance book.
- *Learns* the target's unit economics.

No capital is committed in this phase.

**Phase 3: redeploy (years 4–6 in base, 3–4 in optimistic).** Buy one durable recurring-revenue business **with a manager in place**, or install one at purchase, so the acquired business does not need the founder's hours. The engine keeps paying the founder. Alternatively, launch SYN-006 with hired staff, but only if a founder-run pilot measured the price and productivity in §5.

**Phase 4: decide the engine's future (year 5+).** Options:
- keep it as a founder-run income line;
- hand it to an experienced recruiter on a profit share;
- wind it down if the founder's time is worth more as capital allocator and manager of the acquired business.

### 6.2 Illustrative acquisition economics

Every input below is E or D; the arithmetic is shown so the founder can redo it with real listings.

| | (a) Bookkeeping/payroll practice | (b) Small insurance book |
|---|---|---|
| Earnings bought | SDE $150k (E) | Commission revenue $300k (E); profit at 25% = $75k (typical 15–30% [C, C5-S021]) |
| Price | 2.38× SDE = $357k. This is the general sold-service median [D, E-WS05007-S007]; **bookkeeping-practice multiples are MISSING** | 5–7× profit = $375–525k, **or** "two-times commission usually a minimum" = $600k [C, C5-S021]. The source's two rules conflict at this margin, so both are kept. Agencies under $500k revenue average 6.8× EBITDA [C, E-SYN001-S011] |
| Manager to replace the seller's labour | −$75k loaded (E) | Included in "profit" only if the book is already serviced by staff (MISSING) |
| Manager-adjusted earnings; unlevered pre-tax yield | $75k; **21%** | $75k; **12.5–20%** |
| Financing | 30% down ($107k); 70% seller note over 5 years at 8% (E) = $62.6k/yr | 20–50% down plus a ~3-year retention earn-out [C, C5-S021] |
| Pre-tax cash to the holding company while the note runs | ≈$12k/yr | Depends on the earn-out |
| Retention risk | Payroll incumbents keep 82–83%/yr [A, WS02-S022]. Without new sales the book shrinks ~17%/yr, so the manager must also sell | Agencies average ~84% retention [C, E-SYN001-S012] |
| Licence | None for bookkeeping [A, DB-S014] | **An Illinois producer licence is needed** for the founder or a hired producer (cost and time MISSING) |

**Timing and verdict:**
- In base, the engine's $69k at year 5 plus the ≥$65k of uncommitted backing would cover option (a)'s $107k down payment and still leave a reserve. In the optimistic case it is affordable in year 3–4.
- Option (a) beats internal reinvestment in the primary at modelled recruiter productivity, which is negative (§5).
- **Two cautions:**
  - Its 21% unlevered yield is a hypothesis built on D/E inputs.
  - The acquired book decays without selling effort.

### 6.3 Ten-year comparison of sequencing paths

Illustrative figures for the base case, $k, pre-tax where marked.

| Path | Years 1–5 | Years 6–10 | Year-10 position |
|---|---|---|---|
| **A. Harvest only.** Primary solo desk, cash to the holding account | Owner cash $269k; net deployable $69k | +$216k deployable | Net deployable $285k; desk EV $206k (≈$44k after FDC); still founder-bound |
| **B. Engine + acquisition (a) at end of year 5** | As A | +$62k pre-tax during the note; deployable −$107k for the down payment | Net deployable ≈$240k; a debt-free practice earning ≈$75k (manager-adjusted, *if* retention is held), worth ≈$357k at 2.38× SDE; desk as in A |
| **C. Engine + SYN-006 launched with staff in year 3 at the REV price ($950)** | Staffed unit needs $88.6k; Y5 op $5.8k | ≈breakeven | Capital tied up for a sub-scale firm. **Rejected** unless the §5 price test passes |
| **D. Boutique at month 24** (optimistic only) | Requires trailing revenue ≥$20k/month, which base never reaches | Y5 desk op $384k with ≥0.7/month producers | Larger cyclical, non-transferable desk; lower resilience than B |

**Path B is the base-case recommendation.** Path D is justified only if the optimistic case materializes *and* experienced producers can be hired.

---

## 7. Holding-company progression

| Stage | Timing (REV base) | Milestone to enter the next stage | Reserves | Governance |
|---|---|---|---|---|
| **1. Founder-operated** | Weeks 1–8 validation; months 3–24 solo desk | Test 3 passed. First fee by month 10. $5k/month operating profit (month 21). Draw covered (~month 20) | 4–6 months of personal runway; 3 months of business cash costs; ≥$65k of backing uncommitted | LLC and separate bank account. Operating agreement clause: candidates are never charged (225 ILCS 515/1.1 [A, E-WS12014-S001]). Monthly P&L. Written collections policy |
| **2. Early profitable** | Months 24–48 | Month-24 decision recorded. Cumulative retained ≥0 (month 37). Net deployable positive (year 4) | Add 12 months of draw ($48k) as a cycle buffer while one cyclical business carries the founder | External accountant. Holding entity and distribution policy (counsel; E). Annual written capital-allocation memo |
| **3. Small staffed** | Years 4–6 | First durable asset acquired with a manager (path B), or SYN-006 staffed after its price test, or a boutique (optimistic only) | 6 months of fixed costs plus debt service for each business | Manager KPIs (retention, hours per client, DSO). Monthly close. E&O and contract review |
| **4. Professionally managed** | Years 5–7 | FDC ≈ 0 in each business: a paid manager does the delivery role. Founder ≤20 hours/week per business | As above, plus a holding-level reserve ≥3 months of combined fixed costs | Monthly operating reviews. Two or three outside operator-advisers (E). Owner-independent bank relationship |
| **5. Multi-business** | Years 6–10 | Two or three businesses with weakly correlated cycles: perm recruiting is cyclical, recurring compliance services are not. No business >50% of cash flow | Combined reserve sized to the worst business's downturn: for the desk, a −57% year [A, E-WS12014-S011] | Each business on its own P&L and bank. Inter-company loans documented |
| **6. Holding company** | Year 8+ | Founder is a full-time capital allocator. Repeatable acquisition process (sourcing, diligence, manager placement) | Policy-set | Written hurdle rates, reviewed annually. Independent review of accounts. Succession plan for each manager |

---

## 8. Decision rules: when investing elsewhere beats reinvesting

These are E-level rules derived from the -REV models and the reviews.

1. **Measured, not modelled.** An internal reinvestment qualifies only if the productivity driver it relies on has at least six months of measured data. Examples:
   - recruiter: placements per producer;
   - bookkeeper: hours per client;
   - technician: practices per technician.
2. **Internal hurdle.** Reinvest when the outlay's modelled incremental pre-tax return is at least **30%** with payback within **24 months** on the measured driver (hurdle E). Otherwise distribute to the holding account. On today's evidence, no outlay in the primary passes; WS04-014's density hiring does.
3. **External hurdle.** Buy a business only if all of these hold:
   - manager-adjusted unlevered pre-tax yield ≥**20%**;
   - ≥3 years of retention data at ≥80%;
   - ≥20% of the price in a retention-linked earn-out [C, C5-S021];
   - no client above 10% of revenue;
   - equity ≤50% of the holding company's liquid capital.
4. **Choosing between them.** When both pass, prefer the one that lowers the share of the holding company's cash coming from the cyclical desk, even at a somewhat lower return. Diversification is worth paying for while one perm desk funds the founder.
5. **Cycle freeze.** Make no new commitment when manufacturing job openings fall in two consecutive JOLTS prints [C, E-WS12014-S014], or when the desk's trailing-6-month revenue falls 30%. Downturns are when the reserve is used, not when capital is deployed [review, WS12-014 §10].
6. **Stop compounding a business** when its last two growth outlays returned less than the external hurdle. From then on, treat it as a cash source.
7. **Never fund a draw with acquisition capital,** and never let a single deal take the reserve below Stage 3 levels.

---

## 9. The $500k–$1M question

**Stated plainly: no from-scratch option in Atlas shows evidence of $500k–$1M a year of owner cash within five years.**

**Post-review base case.** Year-5 owner cash runs $66.6–97.1k a year, and year-5 operating profit $82.6–114.5k.

**Optimistic cases.** Year-5 owner cash per year:
- SYN-006: $512.7k;
- WS04-014: $388.2k;
- WS12-014: $187.4k;
- SYN-004: $98.0k.

The two that approach the band, SYN-006 and WS04-014, are optimistic cases **that no reviewer endorses.**

**Landscape.** This matches the wider search. No record of the 630 earned an fcf score of 7 (about $250–400k) under blind scoring (`10_deliverables/sections/LANDSCAPE_AND_REJECTIONS.md` §1.1).

**What would have to be true:**

| Model | Conditions needed | Status of the evidence |
|---|---|---|
| **WS12-014** | The founder performs at the Stage E base funnel (≈12 placements in year 3: top-quartile, mature-PageGroup-fee-earner output [B, E-WS12014-S013]). Three hired experienced producers each bring ≥1.0 new clients a month. No downturn hits in years 2–5. That gives ≈$704k of year-5 operating profit before a ≈$130–150k team lead (E) | Contradicted for a newcomer by the reviewer's benchmarks [D, F5-S006, F5-S007]. Perm placements fell 24.1% in 2023 [A, E-WS12014-S009] |
| **SYN-006** | Realized price ≈$1,200 a month. ≥15 clients per bookkeeper at ≤$5,800. 16 conversations a month at a 35% win rate. 1.2% monthly churn | Each is above the reviewer's evidence. An offshore competitor charges $999 [D, C5-S035]. Chicago bookkeeping wages run higher [C, F1-S001] |
| **WS04-014** | $860 a month per practice. 32% win rate. 0.7% churn. About 125 practices by year 5 | A local competitor charges $399 with free onboarding [B, F4-S003] |
| **SYN-004** | Not reachable from the exempt segment alone. It would need the ABC licence to serve accounts below 1,500 kW, productive reps, and supplier acceptance | Supplier acceptance is MISSING [review, SYN-004 §3] |

**The plausible route to $500k+.** Add businesses rather than stretch one. For example:
- the desk at ≈$90–110k of owner cash;
- plus three acquired recurring businesses at ≈$75k each, manager-adjusted, once their notes are paid off.

That reaches roughly $300–350k a year by years 8–12 (E). Reaching $500k needs larger or more acquisitions, financed by seller notes or bank debt. Bank and SBA terms are MISSING from Atlas evidence.

---

## 10. Where the evidence cuts against the decision

1. **Post-review, the primary's advantage is speed, not size.**
   - SYN-004's year-5 after-FDC profit ($24.7k) is slightly above the primary's ($21.3k).
   - WS04-014 has the highest base exit value ($475k) and the best harmonized 10-year accumulation ($230k vs $208k).
2. **The primary's 10-year accumulation lead ($316k) assumes the founder recruits full-time for ten years.** Its conservative case accumulates $11k, and a 2009-type year needs $140.7k of funding [E, WS12-014-REV].
3. **The primary is the one finalist whose value leaves with its producer** [review, WS12-014 §9]. A holding company built on it must buy or build its durability elsewhere. This report's sequencing assumes exactly that, and the assumption rests on D/E-level acquisition evidence.
4. **The alternatives' validation remains worthwhile.** If SYN-006's founder-run pilot measures a price of at least $1,100 with ≤10 hours per client, it becomes the better holding-company core: recurring, statutory demand, resilience 6. The primary then becomes its funding source rather than the core.
