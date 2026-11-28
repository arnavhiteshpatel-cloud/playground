# WS18-035 — Stage F Adversarial Review (batch F6)

**Concept reviewed:** an independent garage door repair and installation company in NW Cook / central DuPage. It serves residential customers first, with a B2B referral layer of community-association managers (CAMs), home inspectors and brokerages, and adds light-commercial maintenance from year 2.

**Material reviewed:**
- Stage C memo, Stage D deep dive (verdict there: RESERVE), Stage E playbook and materials;
- `08_financial_models/WS18-035_assumptions.json` and `_results.json`;
- `09_databases/prospects/WS18-035_prospects.csv` (32 rows) and `09_databases/suppliers/WS18-035_suppliers.csv` (9 rows);
- `06_playbooks/sources_E_WS18-035.jsonl` and the cited DF, C8 and WS18 records.

**Reviewer:** independent; I did not write any of this. **Access date:** 2026-11-28.

**Re-runs:** made with `tools/fin_engine.py`, with overrides only. No model file was changed (md5 checked before and after). The scripts are `/tmp/claude-0/atlas_scratch/F6/ws18035_review_variants.py` and `07_review/cross_model_audit.py`. New sources are F6-S001…S004.

---

## 1. Verdict: **FAILS (as a first company for the holding-company mandate)**

**Retain only as a $0 desk test (V0 + V1).** It is a legitimate self-employment option, not a cash engine.

The Stage E author's work is unusually honest. Most of its self-corrections check out against the sources (§2). The playbook already calls the idea "conditional, low priority". I go one step further, for three reasons.

**1. The volume calibration is wrong, and fixing it removes the business's scale.** The base plateau of ~133 paid jobs a month was back-solved from franchise *revenue*:
- Access's year-3 cohort average, from a 7-unit system with an average unit age of 1.9 years;
- Precision's smallest-band median of $858k.

But that Precision median was earned at **$1,213 per job**, which is about 59 jobs a month. Converting the franchise medians to *jobs* gives **~59 jobs a month**. That is one founder-technician's capacity.

**2. At that volume the model's profit is the founder's own technician wage.**
- At the filed drivers, harmonized volume gives year-3 operating profit of $91k and year-5 of $114k, with no hires at all.
- Charging the $6,800/month a technician would cost leaves **~$22k** in year 5.
- At the model's own volume (133 jobs), the same charge gives **−$25k** in year 5.

**3. The three economic drivers that remain are each optimistic against independent evidence:**
- **Ticket.** Local published repair bands: most repairs cost $150–500 and an installed opener $250–600 [D, F6-S001].
- **Booking rate.** The model books 65% of leads; the ServiceTitan small-shop median is 30% [D, F6-S003].
- **Margin.** It depends on a dealer account nobody has confirmed.

**Corrected view (reviewer drivers):**
- plateau 58.9 jobs/month;
- ticket $545;
- 55% of leads booked and 85% of visits paid;
- acquisition cost $137 per paid job;
- margin after parts 58%.

| Case | Y3 op. profit | Y5 op. profit | Y5 after founder-technician charge | Peak funding (with $4k draw) | Peak funding (no draw) | 10-yr deployable |
|---|---|---|---|---|---|---|
| Filed base | $65.8k | $67.0k | −$25k | $93k | $43k | $9k |
| **Reviewer base** | **$51k** | **$70k** | **−$22k** | **$110k** | **$64k** | **$46k** |
| Reviewer conservative (45 jobs, $475, CAC $178, GM 52%) | −$33k | −$22k | −$114k | $392k | $200k | $0 |
| Reviewer optimistic (120 jobs, $650, CAC $85, GM 62%) | $181k | $236k | $144k | $42k | $42k | $771k |
| Reviewer base with a B2B share (CAC $90, ticket $575) | $93k | $116k | $24k | $76k | $54k | $256k |

**Bottom line of the table:**
- In every base-like case, year-5 "operating profit" is roughly a skilled technician's pay of $65–115k.
- Adding volume *lowers* profit, because a hired technician contributes about $0.9k a month at full utilisation in the reviewer base. Each hire is break-even at best.
- That is the definition of G7 (founder-capped). It is not a holding-company seed.

---

## 2. Factual errors found

| # | Claim | What the source actually says | Correction |
|---|---|---|---|
| F1 | Base plateau "~133 × $575 = ~$0.92M (Access yr-3 avg $1.02M; Precision smallest-band median $858k)" [B] | **Precision 2026 FDD, Table B** (verified): CY2025 average gross sales per job **$1,213**; smallest band (n=19) median **$857,807** [B, C8-S019]. That is ~707 jobs/yr, **~59 jobs/month**. **Access 2025 FDD** (verified): year-3 average $1,016,560. But the system reported only **7 franchised units** in 2024, with average age **1.88 years** (median 1.33) and an all-unit median of **$389,856** [B, DF-S001]. | Calibrate in *jobs*, not revenue at half the ticket. Median-based estimates are 57–61 jobs/month: Access median ÷ $575 = 57; ProLift middle-50% $424k ÷ $575 = 61; Precision 59. Keep the disagreeing figure: Precision's CY2024 smallest band, $1.41M ÷ $706, gives ~166 jobs/month [B, C8-S020]. Base volume is **D/E at best, not B**. |
| F2 | The 8 launch suburbs hold ~109k one-unit homes, "the size of Precision's smallest territory band (91k–230k single-family homes)" | Precision bands count **single-family one-unit *detached*** homes (FDD Table A note 1). ACS 2024 5-yr B25024 for the 8 suburbs: **89,152 detached** plus 20,125 attached = 109,277 [C, F6-S002]. | On Precision's own definition, the launch area is *below* the smallest band. Its volume comparable is the bottom of the smallest band, not its median. |
| F3 | "Searchlight LSA average $49 … The same data put non-branded search at $173/lead and the blended figure at $145" | The page attributes $145 blended to Searchlight (11 contractors, Jan–Apr 2026). It attributes **$173 non-branded and $66 branded to Elevarus**, with no sample stated [D, E-WS18035-S006, re-fetched]. | Minor misattribution. The $173 has no disclosed sample. The correction that the "38% book rate / $198 per customer" is not on the page is **confirmed**. |
| F4 | Opener installed at "≥ $870" on the menu; ticket mix of 13% openers at ~$800 | **Raynor Door Co., "How Much Does Garage Door Repair Cost in Chicago?" (18 May 2026):** opener replacement installed **$250–600**; most repairs **$150–500**; cable $150–250; rollers $100–200; off-track $125–250 [D, F6-S001]. | The local published band sits *below* the playbook's opener price. At DDM's public head cost ($592) the opener line cannot be priced competitively at all. Base ticket corrected to ~$545: 78% repairs at ~$350, 13% openers at ~$650, 9% doors at ~$2,100 (E). |
| F5 | DF-S004 listing is "one NW-suburb firm … $171k SDE on $472k revenue" | The listing's location field reads "Not Disclosed, IL **McHenry County**". Est. 1983, 1 employee, revenue $472,431, cash flow $170,716, asking $550,000 [D, verified]. | Exurban, mature (43 years), seller-claimed. Fine as a D-level ceiling for a decades-old owner-operator. It says nothing about a newcomer. |

**Citations that checked out exactly** (opened 2026-11-28):
- **Google Ads Advanced Verification** "typically … 6-8 weeks" for US garage-door services [B, E-WS18035-S002].
- **Chicago Home Repair licence** [A, E-WS18035-S004]: $1,000 fee; 2-year term; $300,000-per-occurrence GL; signed written estimate before work; no charge above the estimate without approval.
- **Raynor spring guide** (15 June 2026) [D, E-WS18035-S009]: single $200–300; pair $250–400 (parts $100–180); extension pair $150–300.
- **SSC register page** [B, E-WS18035-S008]: "ONLY sell to professional garage door dealers"; "<1 Year" option; 5–7 business days.
- **C.H.I. 2-100 course** [B, E-WS18035-S010]: $550, 4 days, "Recommended for: New Installers". Billing wording ("invoiced upon registration", "COD Customers") implies a customer account. Eligibility for a non-dealer remains unconfirmed, as the playbook says.
- **O\*NET 49-9011 Chicago MSA** [C, DF-S006]: median $65,090; 25th percentile $51,300.
- **Precision 2026 FDD** [B, C8-S019]: 147 units, 116 reporting; smallest band average $1,382,488 / median $857,807; average per job $1,213.
- **Access COGS** [B, DF-S001]: 46.26% (2024) and 47% (2023).

That is 11 consequential citations opened.

---

## 3. Unsupported or over-stated claims

| Claim | Evidence level actually warranted |
|---|---|
| Lead → booked visit 65% and visit → paid 85% (55% lead → paid job) | **E, optimistic.** ServiceTitan, all trades, May 2025–Jul 2026 [D, F6-S003]: regional median call booking 28–38% (Midwest 38%); shops with 1–10 technicians 30%; top quartile 76–82%. Emergency garage-door calls plausibly book above the trades median. But a new, unreviewed listing booking 65% assumes near-top-quartile call handling from day one. Reviewer base: 55%/85%; conservative: 45%/80%. At 38%/85%, acquisition cost per paid job is ~$198. |
| Acquisition cost $105 per paid job [D] | D for cost per lead; **E for cost per job**. It inherits the booking-rate assumption. $64 blended cost per lead ÷ 0.4675 = **$137** (reviewer base); ÷ 0.36 = **$178** (conservative). |
| "Revenue density … single-territory revenue near $1M within three years" [B] | B as a statement about **Access's** few year-3 units. **Not B** as a statement about an independent. Median units of all three franchisors are $0.39–0.86M. |
| Founder can do ~60 jobs/month *and* sell, dispatch, answer CAM requests and manage LSA | **E.** 60 jobs/month is 3 jobs per day for 20 days, plus parts runs. Lowering the founder's field capacity to 45 jobs (technician hired at 45) makes the reviewer base **−$41k in year 3**. |
| Technician productivity of 60 jobs/month, with install weeks halving capacity | E. It is not reflected in the model (no install-day capacity penalty). |
| Margin after parts 60% "C" | **E for a newcomer.** It requires a dealer account (SSC/Clopay) that nobody has confirmed. The component prices are B; the mix and the discount are E. |
| B2B (CAM/inspector) share ≥30% of jobs | **E.** In townhome associations, unit garage doors are usually the owner's responsibility (unverified; the playbook rightly lists it as a confirmation). Parking-garage doors are often commercial rolling or sectional doors needing the year-2+ commercial skill set. |
| Year-10 EV $201k at 2.5× | D/E. On the reviewer base the "EV" is a multiple on the founder's own labour. A buyer would pay little for a business whose profit disappears when the owner leaves the van. |

---

## 4. Financial model audit

**Recomputation.** The engine reproduces the filed results exactly:
- base Y3 $65,781 and Y5 $67,046;
- peak funding $93,434 with draw and $43,278 without;
- 10-yr deployable $8,701.

The standardization rules are followed: $4k/month draw from month 13; 30% tax; start capital injection set to peak funding ($93.5k).

The 24-month table in playbook §7 also matches the engine. For example, month 20 operating profit is $102, after a technician plus a CSR.

**Top-5 drivers challenged:**

| Driver | Filed base | Independent evidence | Reviewer base / conservative | Effect alone on Y3 op (filed $65.8k) |
|---|---|---|---|---|
| Plateau jobs/month (via leads) | 133 | Franchise medians ≈ 57–61 jobs/month [B, DF-S001, DF-S002, C8-S019]; the area is below Precision's smallest band [C, F6-S002] | 58.9 / 45 | **+$25k** (fewer unprofitable hires) |
| Average ticket | $575 | Raynor Chicago bands [D, F6-S001, E-WS18035-S009]; Precision $706–1,213 is a premium-upsell brand [B] | $545 / $475 | −$26k |
| Acquisition cost per paid job | $105 | ServiceTitan booking medians [D, F6-S003]; LSA $45–59/lead [D] | $137 / $178 | −$36k |
| Margin after parts | 60% | DDM public prices [B]; dealer pricing MISSING | 58% / 52% | −$19k |
| Founder field capacity / technician trigger | 60 | E | 60 / 45 | −$92k at 45, with reviewer drivers |

**Working capital** is genuinely small, and the model's ~2-week cycle is right. The real capital is vans: $32k for the founder plus $30k per technician.

**Founder-draw logic:**
- Under the reviewer base, cumulative retained cash after the draw stays negative for years. Peak funding with the draw is **$110k**, above the $100k conditional backing (but not a G1 fail, because that money is not at risk before first revenue).
- The draw is paid from the founder's own technician labour. In economic terms the owner is lending the business his wage and taking it back.

**Structural finding:** hired-technician contribution.
- Per technician: 60 jobs × ($545 × (0.58 − 0.06) − $137) ≈ **$8.8k a month**, against **$7.9k** for pay plus van running. That leaves ≈ +$0.9k a month at 100% utilisation, before the CSR and any callbacks.
- This is why every volume increase above founder capacity *reduces* profit. It is why "delegation" fails, and why "Recession" and "Competitor response" *raise* filed profit.
- The playbook correctly identifies this as an artifact of free founder labour.

---

## 5. Customer acquisition challenge

**How incumbents sell.** In this market, incumbents sell through:
- Google LSA and the map pack, where ranking is driven by review count, responsiveness and verification;
- branded search;
- dealer showrooms (the Clopay dealers in the area);
- Precision's national brand and call handling.

**What a newcomer faces:**
- Advanced Verification of 6–8 weeks [B, E-WS18035-S002].
- Background checks for the owner and every technician [B, E-WS18035-S001].
- No reviews in a category that Google polices aggressively because of fake listings [C, E-WS18035-S005, E-WS18035-S017]. It is plausible, but unverified, that new garage-door Business Profiles face extra suspension and verification friction.

**What the first 10 customers really require:**
- the founder to be trained and insured;
- personal-network jobs at friendly prices;
- 1–2 inspector or CAM trial jobs;
- LSA live by about month 3.

The playbook's sequence is right. Its timing is optimistic only in that the C.H.I. course eligibility and dates are unconfirmed.

**What the first 100 require:** ~$64 per lead × ~210 leads at reviewer conversion ≈ $13k of ads, plus 4–6 months of field work.

**Cheapest decisive test:** V1, the $0 desk benchmark of posted prices and review-coded paid prices. If the median paid spring pair is below ~$325, or posted opener installs sit in Raynor's $250–600 band, the $545 reviewer ticket is itself too high. Stop there.

---

## 6. Supplier/partner accessibility challenge

**Most likely to refuse or delay:**
- **SSC.** "ONLY professional garage door dealers"; the form asks for a contractor licence, and Illinois has no state garage-door licence [B, E-WS18035-S008]. A brand-new LLC with no truck history may be asked for references.
- **Clopay.** Criteria are unpublished. Existing dealers in the area are not obviously a problem for Clopay, but door samples and showroom expectations are MISSING.
- **Raynor** requires $100k/yr of purchases [B, DF-S009].

**Day-one supply** is DDM at public prices. DDM's wholesale list is suspended [B, DF-S012], and I could not re-verify its prices: products.json returned 403 to a direct request. Without a dealer account, the reviewer conservative margin (52%) applies.

**Training:** DDM has discontinued training [B, verified via E-WS18035-S011]. C.H.I. course access for non-customers is unconfirmed (§2).

---

## 7. Legal/regulatory challenge

**Home Repair and Remodeling Act scope.** The enacted definition excludes "maintenance, service, or repairs under $500" [A, WS18-S010]. Most spring and cable jobs therefore fall *outside* the Act's definition, while door installs are inside it.
- The playbook applies the Act's insurance minimums and contract formalities broadly. That is prudent but not legally required for sub-$500 work.
- More importantly, it leaves the question of which consumer-fraud rules govern the bulk of the jobs to the general Consumer Fraud Act.
- Confirm the current text, which may be amended, with counsel.

**Workers' compensation.** The class code and rate for door installation are MISSING. Door installation is a high-hazard class, so the $7.9k/month technician load may be light. Obtain a broker quote before the first hire.

**Suburban contractor registration** remains MISSING for all 8 suburbs. Illinois villages commonly run their own contractor registration and bond rules, but I did not verify any of the 8 here. Expect small fees; check before the first job.

**Electrical work.** Opener replacement that requires new wiring needs an electrician in Chicago [A, WS10-S006]. The suburbs are unverified.

**Inspector channel.** Licensing rules for Illinois home inspectors may restrict repair work and referral arrangements (225 ILCS 441; not re-read this session), and referral fees invite conflict-of-interest problems. The playbook's "no referral fee, price menu only" rule is correct. Confirm 225 ILCS 441 details before approaching inspectors.

**Personal injury exposure.** Torsion-spring injuries are the trade's signature risk. Confirm GL coverage of spring incidents and damage to vehicles in the garage before the first job (the playbook lists this).

---

## 8. Competitive response

**How incumbents react.** They do not need to react to one new van: LSA auctions and review density already price out a newcomer.

**The honest-pricing wedge is not a wedge:**
- Chicago *law* requires the signed estimate [A, E-WS18035-S004].
- Precision markets upfront pricing [D, DF-S003].
- Raynor publishes Chicago price bands [D, F6-S001].

**What is underestimated is the lead-gen fronts.** They bid on the same LSA and search inventory, depress the trust of every new name, and set price anchors ($199 trip fees, $350–750 per spring) that a low-price honest firm cannot match on conversion economics. The playbook covers this well.

---

## 9. Founder execution & delegation realism

**The founder becomes the business's spring technician.** That is a hazardous, physically demanding trade learned in months from a 4-day course plus practice. It is feasible for a capable, willing person.

**But the evidence says it never stops being the founder's job.**
- Every model path that removes the founder from the van loses money, in both the filed base and the reviewer base.
- The playbook's own variant V1 (an experienced technician from month 1) gives −$35k in year 3.
- **Delegation is labour-feasible but economically unfeasible.**
- An opportunity cost also applies: the founder's 2027–2029 working hours go into ~$65–115k/yr of technician-equivalent earnings, instead of into a business that compounds.

---

## 10. Pre-mortem

| # | Failure story | Early indicator | Cheapest preventive test |
|---|---|---|---|
| 1 | **Founder-capped plateau.** The business settles at 45–60 jobs/month with the founder on the van. It earns ~$50–70k/yr of SDE, never hires profitably, and has no deployable surplus. | < 40 paid jobs/month at month 9; ticket < $525; any month with a hired technician under 50 jobs | V1 desk benchmark ($0) plus a month-6 rule: no technician hire unless 75+ jobs/month for 2 months *and* contribution per job ≥ $150 |
| 2 | **Lead economics worse than modelled.** LSA bookings run at 35–45%, not 65%. Cost per paid job is $150–200. Every paid-lead spring job is break-even after technician time. | The first 40 LSA leads book < 50%, or cost per paid job > $140 | V5 45-day LSA test ($1.5–3k), but only after V1 and V2 pass |
| 3 | **No dealer pricing plus the opener price ceiling.** Margin stays at ~52%; openers lose money at the local $250–600 band. The conservative case (−$22k in year 5) materialises. | SSC/Clopay decline or delay > 3 months; parts > 45% of revenue on the first 50 jobs | V3 supplier questions ($0) |

---

## 11. Corrected scores and bottom line

| Key | Stage E | **Stage F (F6)** | Reason |
|---|---|---|---|
| fcf | 3 | **3** | Reviewer base Y3–Y5 $51–70k, before founder pay and including his technician labour (anchor 3 = $50–75k). Conservative negative. |
| roic | 4 | **3** | Y3 op ÷ peak funding = 0.47 (reviewer base); negative once the founder's labour is charged |
| access | 6 | **5** | Buyers search actively, but paid-lead toll, Advanced Verification, review deficit, a fake-listing-polluted channel and booking-rate evidence keep a newcomer near franchise-median volume or below |
| scale | 4 | **3** | Hired-technician contribution ≈ break-even, so each van adds risk, not profit. Single-territory ceiling ~founder capacity. |
| resilience | 6 | 6 | Repairs are non-discretionary; installs cyclical (unchanged) |
| entry | 3 | 3 | Wedge legally required and already claimed (unchanged) |
| delegation | 5 | **3** | Labour market exists, but every delegated configuration loses money in the filed and reviewer models |
| cash | 8 | 8 | Paid on completion; deposits on doors (correct) |
| feasibility | 7 | **6** | Founder must learn a hazardous trade. Training access unconfirmed (DDM stopped, C.H.I. customer billing). Dealer-only supply. Suburban registrations MISSING. |
| ai | 4 | 4 | Unchanged |

**Composite:** raw **3.99**, evidence-adjusted **4.29** (D, k = 0.70). Stage E was 4.59 / 4.71.

**Gates:** G7_FOUNDER_DEPENDENT **WARN** (structural); G4_CEILING **WARN** (no evidenced path to ≥$100k/yr *after* founder labour). No FAIL gates.

**Bottom line.** This is a real, cash-paid, essential trade, and the playbook says so honestly. Converting franchise revenue benchmarks into jobs shows that a median franchise unit does about 59 jobs a month, which is one founder's van. At realistic ticket and booking rates, a hired technician barely covers his own cost.

The base case is therefore a well-paid trade job for the founder, at $50–115k/yr of SDE. It produces negligible surplus for a holding company and rests on the founder's own field labour. Only the optimistic or B2B-heavy cases change that:
- ≥ 120 jobs a month;
- a $650 ticket;
- acquisition cost ≤ $85–90 per job.

No evidence yet shows an independent newcomer reaching them.

I agree with the Stage E author on almost every fact. I disagree only on the classification: it should leave the finalist set rather than sit as "conditional". The one test worth running is V1, the $0 price and review benchmark. If it found paid spring-pair medians ≥ $375 and visible upsell complaints, I would reopen the B2B-heavy variant.
