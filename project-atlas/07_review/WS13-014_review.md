# WS13-014 — Stage F Adversarial Review (batch F4)

**Concept reviewed:** private utility locating plus concrete GPR scanning for Chicago-area subcontractors, GCs and facilities.

**Material reviewed:**
- Stage C memo and Stage D deep dive;
- Stage E playbook and materials;
- `08_financial_models/WS13-014_assumptions.json` and `_results.json`;
- the prospect CSV (39 rows) and the supplier CSV (8 rows);
- `sources_E_WS13-014.jsonl` and the cited DF/C3/WS10/WS11/WS13 records.

**Reviewer:** independent; I did not write any of this. **Access date:** 2026-11-28.

**Re-runs:** all made with `tools/fin_engine.py`. Scripts are in `/tmp/claude-0/atlas_scratch/F4/` (`base.py`, `ws13.py`, `ws13b.py`). The finalist's files were not modified. New sources are F4-S007…S010 and F4-S012…S014 in `07_review/sources_F4.jsonl`.

---

## 1. Verdict: **SURVIVES WITH MAJOR REVISIONS**

It survives as a validation-only candidate, planned as an owner-operator business. It is not a technician-scaling business until measured.

The Stage E author did good work:
- **Capital restructuring.** The rent-first, lease and mileage plan cut peak funding from about $230k to $51k.
- **Corrections.** The 811 Chicago and PE/QL corrections are right.
- **Survival variable.** The playbook names hiring discipline as the variable that decides survival.

The review question was whether the founder-only conservative variant (~$45–68k) is the honest base. **My answer is: nearly. The honest base is about $50–90k a year, whether or not technicians are hired.** The reasons:

1. **Thin technician unit.** By the playbook's own numbers, the hired technician is a thin-margin unit. Break-even ARPC is $488 at $8,300/month, against an unverified $750 base. No Chicago price, visit-frequency or rebooking data exists (all E).
2. **The corrected base.** With modest corrections (ARPC $700, first-job-to-account 30%, technician $8,700, insurance $1,000/month), the hired-technician plan earns:

| Measure | Stage E base | Corrected base |
|---|---|---|
| Year-3 operating profit | $106k | **$49.9k** |
| Year-5 operating profit | $175k | **$86.1k** |
| Peak funding with draw | $51k | **$110k** |
| Peak funding with draw at DSO 60 | — | $146k |
| 10-year deployable | $418k | $59k |

   A founder-only firm at a steady 15–20 accounts and $675 ARPC earns about **$55–90k** (analyst arithmetic, §4) with about $52k at peak risk. In other words, hiring adds risk but little expected profit until the price is proven above roughly $750.
3. **Competence and liability.** The founder plans 2 days of hands-on GPR training plus 20 practice scans, then scanning post-tensioned slabs in occupied high-rises. GPRS, the incumbent, requires 4 weeks of field mentoring, 80 classroom hours and another 4 weeks of mentoring before working under a senior PM [D, E-WS13014-S004, verified].
4. **Competition.** Chicago has at least four coring or cutting firms that advertise in-house GPR, besides GPRS [D, F4-S013].

**Bottom line.** It remains worth a $0–200 interview sprint because the buyers are named and the test is decisive. As a first holding-company asset it is weak:
- corrected base ≈ **$50k year 3 / $86k year 5**;
- **G4 WARN** (below $100k in year 5 on the corrected base);
- a strike-liability tail.

---

## 2. Factual errors found

| # | Claim | What the source actually says | Correction |
|---|---|---|---|
| F1 | "Guides $300–600" half-day and "$800–1,500 full day (one guide)", cited to C3-S028 (sphengineering.com) | The cited page (verified) gives concrete scanning at **"~$1,000–$3,000 per day, or hourly with a 2-hour minimum"**, labelled "market estimate … planning ranges only". It is AI-translated, and the publisher is a drone/sensor vendor. **No half-day figure appears** [D, F4-S010]. | The $300–600 half-day anchor is not at the cited URL. The record itself says "paraphrase of search-result guides". Downgrade the half-day anchor to **unsourced/E**. The only verifiable private-market figure (D) is $1,000–3,000 per day. |
| F2 | Hard Rock Technologies (5 CSDA-certified technicians), Butler, Cobra: in-house GPR [D, DF-S031, concreteopenings.com] | The URL now **301-redirects to csda.org**; the article cannot be re-verified. | Independent search summaries confirm Chicago-area coring/cutting firms advertising GPR: Butler Coring/Scanning, Chicago Cut Concrete Cutting (20 operators), Cobra (GPR division; job posting lists company-supplied GPR and EM equipment), and Apple Concrete Coring (Lombard) [D, F4-S013]. The claim stands at D, and **competition is broader than four names**. |
| F3 | Utility GPR cart and E5 pilot rentals assume rental logistics from CSDS | CSDS rates are verified ($125 Conquest 100; $155 LMX200; 3-day minimum; +10% protection plan). The page says nothing on shipping to Illinois; freight rates changed August 2025 [B, E-WS13014-S001]. | Correctly flagged MISSING. Freight on every 3-day block to Chicago can add materially to the $465 block cost. |
| F4 | NULCA EM course $500 [B, E-WS13014-S002] | Verified. But sessions are only in Anaheim/Sacramento, and **attendees must bring their own locator**. | Sequencing: rent the locator before training. Add about $700 travel (the playbook allows for it). |
| F5 | W.E. O'Neil form: "umbrella $2M" | Verified PDF: umbrella **$5M** each occurrence for Concrete, Electrical, Plumbing, HVAC and other listed trades; $2M for "all other trades". WC/EL $1M/$1M/$1M is required with waiver of subrogation. Completed-operations cover must be kept **5 years**; per-project aggregate [B, F4-S009]. | A scanner subcontracted under an electrical or plumbing sub may be asked to match **$5M**. The premium estimate ($750/month base) and the E2 pass threshold ($10k/yr) are optimistic. Use $1,000/month base and $1,400/month conservative (E). |
| F6 | "Inside the City … utilities likewise mark only 'their facilities'" [A, E-WS13014-S012] | The 811 Chicago page (verified) says utilities mark "where their facilities exist". It does not expressly address private lines. | Minor over-reading. The private-line gap is properly supported by JULIE's FAQ (verified: operators "DO NOT locate private underground lines"; owner bears cost [B, WS11-S031]). |

**Citations that checked out exactly:**
- CSDS rental rates;
- the NULCA course price;
- GPRS training hours and the $56k-per-incident marketing claim (an unsourced figure on GPRS's own page, correctly tagged D);
- Insureon excavation medians (GL $120, E&O $67, umbrella $93, inland marine $101, WC $190, auto $370);
- GSA CALC $124.69 / $134.66 / $135.26 per hour (these are federal *ceiling* rates, not market prices);
- City permits: 5,042 = 3,325 renovation + 1,717 new construction ≥ $250k since 2025-01-01 (re-queried; the 6,346 total also includes express, elevator and wrecking permits);
- 811 Chicago hit tickets: 1,205 in 2025 and 1,165 in 2026 (re-queried; note the dataset holds records back to 2015, not "since 2020" as its description says);
- JULIE private-line FAQ.

Field Environmental (Mini XT $450/day) returned 403 and could not be re-verified.

---

## 3. Unsupported or over-stated claims

| Claim | Warranted level |
|---|---|
| ARPC $750 ("about 1 visit per account per month") | **E.** No Chicago rate card, invoice or visit-frequency data. GSA ceilings are federal maximums, not commercial prices. GPRS publishes no prices; it "tailors every quote" [D, F4-S014]. |
| 22 qualified PM/foreman conversations a month, 50% priced first job, 35% repeat account (≈3.9 accounts/month) while the founder also performs about 25 field visits a month | **E**, optimistic. That is 100+ hours a month of field work plus 40–60 hours of selling. The repeat rate faces incumbents and bundled scan-and-core. |
| Technician carries 20 accounts at ~25 half-days a month | **E**, plausible only with dense scheduling. Utilisation is demand-limited, not capacity-limited, in a lumpy trade. |
| Base year-5 revenue about $1.07M (110 accounts) | **E.** At roughly $600 per visit that is about 1,700–1,800 visits a year. Chicago issues about 2,600 new and renovation permits ≥ $250k a year [A, re-queried], so the base implies about 0.65 visits per large city permit per year. Suburbs and smaller permits add demand, but that is a material share against GPRS plus at least four coring/scanning firms. |
| "No licence identified" | **E** (ilga.gov unavailable). Correctly flagged. The business-licence question for Chicago is still MISSING. |
| GPRS's "one founder renting a scanner" origin as small-start evidence | **D**, and survivorship. The founder had a captive customer, his father's coring firm [C, C3-S025]. The Stage C memo says this; the playbook's §1 omits the caveat. |

---

## 4. Financial model audit

**Reproduction.** The engine reproduces Stage E exactly:
- base $106,226 / $174,985 / $51,180 ($48,622 with no draw);
- conservative $34,834 / −$55,758 / $356,044;
- conservative owner-only $44,594 / $68,498.

**Unit check.**
- A technician-month at base is 20 × $750 × 0.85 − $8,300 = $4,450, which matches the playbook.
- At the corrected values (ARPC $700, technician $8,700) it is **$3,200**, before the BD hire and scheduler and with full utilisation.
- Break-even ARPC is about **$512**.
- Under-filled technicians, which are normal after each hire, push the unit to zero.

**Top drivers.** Each was challenged; all are re-runs on base with only that driver changed.

| Driver | Stage E | Evidence | Proposed base / conservative | Year-3 effect alone |
|---|---|---|---|---|
| ARPC | $750 | No Chicago data. The half-day anchor is uncited (F1). The trial floor is $550. | **$700** / $550 | $106k → $79k |
| Technician cost | $8,300 | Chicago surveying-technician 75th percentile $68,640 [C, DF-S033]. "Experienced" GPR technicians are being recruited by coring firms. | **$8,700** / $9,200 | $106k → $92k |
| First job → repeat account | 35% | GPRS and bundled coring incumbency (E) | **30%** / 25% | $106k → $86k |
| Insurance | $750/month | O'Neil form: $5M umbrella for core trades; WC even owner-only [B, F4-S009] | **$1,000** / $1,400 | $106k → $103k |
| DSO | 45 | Sub-tier vendors are paid after the sub is paid (E) | 45 base; **60 stress** | Peak $110k → $146k |

**Combined corrected base** (ARPC $700, win 30%, technician $8,700, insurance $1,000):

| | Year 1 | Year 2 | Year 3 | Year 4 | Year 5 |
|---|---|---|---|---|---|
| Operating profit | $4.9k | $67.2k | **$49.9k** | $57.5k | $86.1k |

- Headcount: 2 at month 24, 5 at month 36, 6 at month 60.
- Peak funding $110k with draw, $52k without.
- 10-year deployable $59k; year-10 operating profit $115k.
- With churn also at 6%: year 3 $63k, year 5 $73k. Fewer accounts trigger fewer hires.
- ARPC sensitivity: $650 gives $34k / $33k (year 3 / year 5); $750 gives $71k / $139k.

**Founder-only steady state** (analyst arithmetic: 0.90 GM, 5% variable cost, fixed overhead of about $46k/yr at corrected insurance, cart lease, 5% churn replacement at $250 CAC):

| Accounts | ARPC $550 | $600 | $675 | $750 |
|---|---|---|---|---|
| 15 | $36k | $44k | $55k | $67k |
| 20 | $63k | $73k | $89k | $104k |

The engine's "never hire" variant without a capacity cap is meaningless: it shows $292k because the founder "serves" 50+ accounts.

**Is the founder-only ~$45–68k the honest base?**
- **For the decision the founder faces now, yes, roughly.** It brackets the low half of the honest range.
- With proven price ($675–750) and 20 sustained accounts, a founder-only firm earns $90–105k. On the evidence today the expected value sits around **$55–90k**.
- Technician hiring should be treated as an *option* that opens only when measured ARPC is ≥ $750 and backlog is > 5 days. It should not be in the base.

**Working capital and draw.**
- DSO 45 on sub-tier construction work is optimistic. Card-on-site for first jobs helps.
- In the corrected base, cumulative retained cash stays negative through year 5 with the $48k draw: −$59k at month 24, −$105k at month 48 and −$93k at month 60. The founder in effect funds the stipend.

**Seasonality (missing from the model).** City data, 2022–25, re-queried [A]:

| Indicator | Winter level | Season comparison |
|---|---|---|
| 811 Chicago initial hit tickets (a proxy for excavation activity) | Dec–Feb average about 308/month | About 30% below the Apr–Oct average of about 438 [F4-S008] |
| Large-permit issuance | Dec–Feb average 661 | About 23% below Mar–Aug at 857 [F4-S007] |

- Interior slab scanning is less seasonal than outdoor locating.
- **Consequence:** the E5 pilot, if started in January–February 2027, runs in the trough. It could falsely fail on visit count, or pass on a mix that is unrepresentative. Either judge the pilot on price and rebooking rather than volume, or schedule E5 for March–April.

---

## 5. Customer acquisition challenge

**How incumbents sell:**
- **GPRS:** technician-PMs sell on site. It has a 400+ PM national network, a "99.8% accuracy" claim, and no published prices.
- **Coring and cutting firms:** many sell **scan-and-core as one purchase**. For an electrical sub that subcontracts coring, the scanner choice is often the coring firm's.

**Who the newcomer can win:** subs that self-core (often, E) and facility managers needing private locates.

**What the first 10 accounts really require:**
- (a) a COI matching GC forms, possibly with a $5M umbrella;
- (b) a demonstrable track record on post-tensioned slabs. No foreman will let an unknown first-month scanner mark tendons on a high-rise without one.
- (c) availability inside 24–48 hours;
- (d) a price at or below GPRS for the first job.

**Practical sequence (E):**
1. Start with **slab-on-grade, non-PT and private-utility locate work** in the collar counties, where the consequence of error and the credibility bar are lower.
2. Take overflow from a coring firm, which provides supervised volume.
3. Pursue downtown PT work only after 100+ documented scans.

The E1 sprint should explicitly ask whether a foreman would let a new firm scan PT slabs, and what proof they would need.

---

## 6. Supplier and partner accessibility challenge

1. **Insurers are the most likely refusal point.** There is no premium evidence specific to locating (search found none). Carriers may exclude professional interpretation errors from GL, or decline a zero-history locator. **Bind nothing until E2 returns written terms**, including XCU, a professional-services exclusion check, and a $2M/$5M umbrella.
2. **Rental houses.** CSDS is in California, with freight to Illinois MISSING. Local availability of a Mini XT or GP8000 is unconfirmed.
3. **Equipment lessors.** Lease approval for a new LLC depends on the founder's credit, which is unknown (F2).
4. **Coring firms as partners (E3).** They are more likely to view the founder as a competitor than as overflow capacity, since they already employ GPR technicians.

---

## 7. Legal and regulatory challenge

1. **Liability allocation.**
   - GC subcontract forms require indemnity, additional-insured status, waiver of subrogation and 5-year completed-operations cover [B, F4-S009].
   - A tendon or conduit strike after a mis-mark can produce claims far above a $600 invoice; GPRS markets $56k as the *average* [D].
   - **Required:** attorney-drafted terms that cap liability and state limitations ("GPR cannot reliably detect …"), plus an E&O policy that covers interpretation. Expect GCs to strike the cap.
2. **WC for an owner-only LLC.** GC forms require WC/EL. Illinois owner-officer exclusion rules need a broker's confirmation (MISSING).
3. **SUE/QL boundary.** Correctly handled (no QL-B labels) [A, E-WS13014-S010].
4. **Statutes not re-read:** 220 ILCS 50 (JULIE Act) on private locating, the Chicago business licence, and FCC UWB operator rules. All remain open.
5. **Classification and prevailing wage.** Correctly flagged.

---

## 8. Competitive response

- **GPRS** can match response time in any county by routing a PM. It is an acquirer, so it may also simply ignore a one-truck entrant until it is worth buying.
- **Coring firms** can bundle scanning at zero marginal price into a coring quote. The playbook's kill condition, "our coring sub scans for free", is the most likely incumbent response, not a remote one.
- **"Competitor response" stress** (no price growth, −3 points margin, churn ×1.3) gives year 5 of −$4.6k on the *Stage E* base. On the corrected base it would be worse.

---

## 9. Founder execution and delegation realism

**Equipment.** Rent-first is realistic and the dealer prices are verified.

**Training is the weakest link:**
- 2 days of hands-on training plus 20 practice scans is not competence on congested or post-tensioned slabs.
- A realistic ramp is 2–3 months of supervised scanning (E, from GPRS's 4-week + 80 h + 4-week programme).
- The best route: a paid ride-along or mentorship, or an overflow arrangement with an established scanner.

**Founder load.** About 25 visits a month plus 10–15 hours a week of selling plus reports and admin is sustainable for a hard-working founder in year 1, not indefinitely.

**Delegation.**
- Field technicians are hireable, but interpretation liability means each needs months of mentoring.
- QA stays with the founder until a lead technician exists (year 4–5).
- Delegation 6 → 5.

---

## 10. Pre-mortem

| # | Most plausible failure | Early indicator | Cheapest preventive test |
|---|---|---|---|
| 1 | **Price and frequency below plan.** Accounts book 0.5–0.7 visits a month at about $550–600. ARPC lands at $350–450 and the founder earns $35–55k. | E1 median last-paid < $550; E5 rebookings < 3 | E1 sprint ($0–200). Explicitly ask about visit frequency per project, not just price. |
| 2 | **A strike or mis-mark** in the first 12 months on a PT slab. The claim exceeds the deductible, renewal fails, and GCs drop the firm. | Any "unsure" interpretation signed off; scanning PT before 100 supervised scans | Restrict PT/elevated-slab work until the competence threshold; X-ray referral partner; E&O confirmed to cover interpretation |
| 3 | **Premature technician hire** on an unproven ARPC: the "hires 30% sooner" stress goes to −$50k in year 3 | Technician utilisation < 70% in month 2 after the hire | Hire only at measured ARPC ≥ $750, backlog > 5 days and 3 months of technician-equivalent overflow already booked |

---

## 11. Corrected scores

| Criterion | Stage E | **F4** | Reason |
|---|---|---|---|
| fcf | 5 | **3** | Corrected base year 3 about $50k, year 5 about $86k; founder-only $55–90k |
| roic | 6 | **5** | About $50–90k on $52k (no draw) to $110k (with draw) at risk |
| access | 6 | **5** | Buyers are named (A), but face a credibility bar on PT work, scan-and-core bundling and GC prequalification |
| scale | 6 | **5** | The technician unit is thin ($3.2k/month at full fill); replication is fragile |
| resilience | 4 | **4** | Construction-cyclical; winter trough of about 25–30% on outdoor work |
| entry | 4 | **3** | GPRS plus at least four Chicago coring firms with GPR; a response-time wedge that is copyable |
| delegation | 6 | **5** | Interpretation liability; long technician mentoring |
| cash | 5 | **5** | Net 45–60 sub-tier receivables |
| feasibility | 8 | **7** | Insurance availability and limits ($5M umbrella possible); WC owner-only; statutes unread |
| ai | 4 | **4** | — |

- **Raw composite:** 4.39. Evidence D (k = 0.70) gives an **evidence-adjusted score of 4.57** (Stage E: 5.26).
- **Gates:**
  - G4: WARN (corrected base year 5 $86k).
  - G7: WARN.
  - G1: passes (capital at risk before first revenue about $10k gross).

**Bottom line.** The capital restructuring was the right fix, and the buyer list is real (A). But the economics hinge on an ARPC with no Chicago evidence. The half-day anchor is not in its cited source, and hired technicians earn a thin margin that disappears at about $510 ARPC. Corrected, the realistic business is an owner-operator scanning firm earning roughly $50–90k a year, with a strike-liability tail and an incumbent and coring-firm ecosystem that already offers what the newcomer pitches.

It remains worth the $0–200 E1 sprint, which should also test PT-slab trust and visit frequency. It should not absorb the $9–10k pilot unless E1 shows median ≥ $600 and dated bookings.

**Preserved disagreement.** The Stage E author's base ($106k year 3) is reachable *if* measured ARPC is ≥ $750 and accounts truly rebook monthly. GPRS's scale shows demand exists at a price that supports technician PMs. I cannot show that it is wrong, only that it is unevidenced.
