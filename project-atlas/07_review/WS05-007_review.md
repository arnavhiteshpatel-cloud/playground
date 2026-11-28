# WS05-007 — Stage F adversarial review (batch F3)

**Subject:** Commercial pest control for Chicago food facilities (south-west cluster) with a residential plan line.
**Reviewer:** independent Stage F reviewer, batch F3, 2026-11-28. I did not write any of the material reviewed.
**Read:** playbook, materials, Stage D deep dive, Stage C memo, assumptions/results JSON, prospect and supplier CSVs, and the cited sources.
**Method:**
- Recomputed the CDPH inspection counts from the live Socrata API with my own classifier.
- Re-fetched 11 cited sources (listed in §12).
- Re-ran `tools/fin_engine.py` with alternative drivers. Scripts are in `/tmp/claude-0/atlas_scratch/F3/scripts/` (`pest.py`, `reinsp.py`, `rerun2.py`, `rerun3.py`). The finalist's model files were not modified.
- New sources are F3-S001 to F3-S007 in `07_review/sources_F3.jsonl`.

---

## 1. Verdict

**Survives with major revisions.** It should be kept only as a validation candidate, not as a launch candidate.

**What Stage E gets right:**
- Demand is official and refreshed daily.
- The licence is genuinely reachable for this founder.
- The cheap validation ladder (E1 interview sprint, then E4 paid field test) is well designed.
- Stage E is already candid that the base case is "a well-paid owner-operator job".

**Where I disagree:** Stage E still prices the book too high and assumes a founder-to-delegate path that the base case never pays for.

The most consequential problem is the **price**. The model's top driver, the $125/month restaurant price ($105 blended), rests on a 2021 national HomeAdvisor consumer guide. The source record itself calls it a "paraphrase of search-result summary". I could not retrieve it: Wayback connection failed and the live page returned 403. It is the only basis for a price charged to independent taquerias, bakeries and Chinatown restaurants on Chicago's south-west side, where the competition is small local exterminators.

**Corrected evidence-adjusted view (reviewer base).** Operating profit before owner pay:

| | Reviewer base | Stage E base |
|---|---|---|
| Year 3 | **≈ $43k** | $61.5k |
| Year 5 | **≈ $80k** | $101k |
| Peak funding with the standard draw | **≈ $79k** | $47k |
| Peak funding with no draw | ≈ $29k | — |

- The reviewer conservative case never reliably pays the owner: year 5 ≈ $43k, peak funding ≈ $153k with the draw.
- The reviewer upside is year 3 ≈ $100k and year 5 ≈ $144k.
- Expect a well-paid technician-owner job of about $45–80k a year by years 3–5, not a holding-company cash engine.

## 2. Factual errors found

| # | Claim (where) | What the source / data actually shows | Correction |
|---|---|---|---|
| 1 | Restaurant monthly IPM "about $100–150" [D, C2-S020] anchors $125/mo (playbook §1, §2.7; `arpc_monthly`) | C2-S020 is a 2021 Wayback copy of a national consumer guide, recorded as a *search-summary paraphrase*. I could not re-open it (Wayback failed, live page 403). The GorillaDesk page the playbook itself cites (E-WS05007-S011) shows low-end commercial ranges of $30–160/mo in many markets (Louisiana $35–120, Utah $39–159, Las Vegas $30–40) [D, F3-S005]. Official Illinois public bids are $30–180 per building per month [A, C2-S017] | The $125 restaurant price is an unverified ceiling, not a midpoint. Use **≈ $105–110 commercial and ≈ $92 blended** in base until E1 measures it |
| 2 | "Rentokil NA retention 80.7%" used as the **B-level** churn basis for a restaurant book | Re-read the H1 2026 statement: 80.7% is *total* North America customer retention. Residential growth is called out, and Commercial and National Accounts retention "needs more focus" [B, C2-S009 re-fetched] | It is not a commercial-restaurant churn figure. For a book built from *cited* (distressed) independents, closures alone run 979 of 10,138 inspected licences a year (≈0.8%/mo) [A, F3-S001]. Base churn should be about 2.2%/mo, and the evidence level is E, not B |
| 3 | Stage E counts: 942 citywide / 165 SW licences with pest activity; 22 SW repeat offenders | My independent classifier (different regex, 12 months to 2026-11-25) gives **994 / 186** with pest activity. It gives **149 citywide / 26 SW** licences with pest evidence on ≥2 distinct inspection dates [A, F3-S001] | Scale confirmed within about 13%. **No correction needed.** Per-prospect counts depend on the regex (e.g. Tacos y Tamales El Pollo: 6 distinct pest dates by my count vs "4 of 9"), but the ranking holds |
| 4 | Re-inspection: median 7 days, 93% within 14, 79.5% pass | Recomputed: median gap **7 days**, **93.6%** within 14 days; the next result is Pass or Pass w/ Conditions in **83%** of cases [A, F3-S001] | Confirmed. Stage E's urgency correction is right, and if anything understated |
| 5 | Implicit: there are "unserved" buyers to sell to | Only **112 licences citywide, 20 in the SW cluster** drew comments in 12 months saying they had no licensed pest-control operator (e.g. "observed retail food establishment without a licensed pest control operator") [A, F3-S001] | Greenfield demand is about **2 sites a month** in the cluster. Nearly every account is a displacement sale. This strengthens Stage C's point and weakens access |
| 6 | "Only ~15 pest firms hold an active City of Chicago business licence", incl. Samuel Pest Control at 4100 S Ashland (E-WS05007-S005) | The current-active-licence query on exterminator/pest business activity returns **6** firms (Verminator, Superior, Safe Place, D'Raco's, US Exterminators, Wegsalper). Samuel Pest Control is not returned [A, F3-S006] | Minor. The more useful inference is that most state-licensed firms operating in Chicago hold no City licence, so the City licence is probably not a gate. Still confirm with BACP |
| 7 | Pete's Fresh Market listed as a top-6 prospect: "one chain decision covers several stores" | Pete's is a multi-store regional chain (store numbers up to at least #18 appear in the inspection data) [A, F3-S001]. A chain of that size almost certainly buys pest control centrally, on terms and with multi-site coverage a one-person firm cannot offer (E) | Move Pete's, 88 Marketplace and MingHin to "log for later". The prospect list's realistic core is single-site independents |

## 3. Unsupported or over-stated claims

| Claim | Stated level | Warranted level and comment |
|---|---|---|
| Restaurant $125/mo; blended $105 | D | **D-, unverifiable source.** This is the #1 driver (×0.75 → year 3 $33.5k) |
| Proposal → win 25%; conversation → win 10% | E | **E.** No newcomer displacement benchmark exists. The L.E.K. "37% switched some provider" figure covers scaled facility managers (C), not taqueria owners |
| One-time cleanout $200 on every new account | E | **E, likely high.** Incumbents and challengers routinely waive set-up fees to win a switch. Use $150 |
| "Founder can service ~110 accounts while selling 12–15 h/wk" | E | Plausible. 110 accounts ≈ 90 visits a month, about 4–5 stops a day, and revenue per person of about $139k/yr, in line with Illinois 5–9-employee pest firms at about $100k receipts per employee [C, C2-S013]. **Accepted.** |
| Technician capacity 190 blended accounts (≈ $240k revenue per technician) | E | High against the Census small-firm benchmark (about $100–122k per employee [C, C2-S012/S013]). It only matters in the optimistic case |
| "Licence obtainable by the founder: $75 exam … [A]" | A | **A, confirmed.** General-use certification needs only the General Standards exam [A, F3-S002] |
| "Rentokil paid ~1.4× revenue" as an exit anchor for a 150–200 account book | B | It is B for Rentokil's acquisitions in general (14 businesses, c.$26m revenue, $37m) [B, re-verified]. It does not show what a buyer pays for a $180–280k restaurant-heavy book with founder-dependent relationships. The 2.4–3.0× SDE base is more defensible |
| "Recession-resilient: code-driven demand keeps year 5 at $81.7k" | Model | The *service* is mandated. The *price* is not: the legal floor is twice a year [A], and restaurant closures rise in recessions. Resilience 7 is acceptable, not stronger |

## 4. Financial model audit

**Reproduction.** `E.run(assumptions,"base")` reproduces year-3 $61,514, year-5 $101,452 and peak funding $47,268 exactly. Transaction 1 reconciles: $1,700 − 210 − 310 − 110 − 51 = $1,019.

**Top-5 drivers, challenged:**

| Driver | Stage E base | Independent evidence | Reviewer base |
|---|---|---|---|
| `arpc_monthly` | $105 | §2 #1: national commercial lows of $30–160; public bids of $30–180/building [A]; residential $40–70 [D] | **$92** (commercial ≈ $108) |
| `proposal_to_win_pct` | 0.25 | 98% displacement (§2 #5); incumbents fix the crisis in 7 days, and 83% then pass (§2 #4); language barrier in the Little Village, Pilsen and Chinatown core | **0.21** |
| `monthly_churn_pct` | 1.8% | Closures ≈ 0.8%/mo alone [A]; Rentokil's 80.7% is a blended figure (§2 #2) | **2.2%** |
| `onetime_revenue_per_new_customer` | $200 | Waived set-ups are common (E) | **$150** |
| `sales_start_delay_months` | 3 | No 2027 exam dates posted as of 2026-11-28 [A, F3-S003]; business-licence processing time MISSING | **4** |
| `gross_margin_pct` (materials) | 0.88 | No contrary evidence found | **0.88** (kept) |

**Reviewer re-runs** (operating profit before owner pay; scratch script `rerun2.py`):

| Run | Year 1 | Year 3 | Year 4 | Year 5 | Peak funding (draw) | Peak funding (no draw) | 10-yr deployable |
|---|---|---|---|---|---|---|---|
| Stage E base (reproduced) | −$15,506 | $61,514 | $55,076 | $101,452 | $47,268 | $23,559 | $177,267 |
| Reviewer base, technician hired at 110 accounts (as built) | −$19,915 | $42,875 | $44,439 | **$28,895** | $106,820 | — | $0 |
| **Reviewer base, technician hired at 140 accounts** | −$19,915 | **$42,875** | $75,581 | **$80,218** | **$78,709** | **$29,484** | $119,268 |
| Reviewer conservative (ARPC $85, win 0.17, churn 2.5%, 35 leads/mo) | −$21,739 | $10,504 | $27,511 | $42,693 | $152,879 | — | $0 |
| Reviewer optimistic (ARPC $110, win 0.28, churn 1.7%) | −$13,983 | $100,336 | $92,623 | $143,743 | $38,682 | — | $383,267 |

**The hiring valley is structural, not cosmetic.** At reviewer drivers the book reaches only about 150 accounts by year 5. A $5,700/month technician hired at 110 accounts (capacity 190) sinks year-5 profit to $28.9k. The founder must carry about 140 accounts before hiring, i.e. stay on the route for 3–4 years.

**Non-technician-owner test** (`rerun3.py`). If the founder will not be the technician and instead employs a CT from month 4 at about $6,200/month loaded:
- At Stage E drivers: year 3 ≈ $0.7k; peak funding $240k with draw, $142k without.
- At reviewer drivers: year 3 −$36k; peak funding $375k.

This **fails G1** in substance. The idea works only if the founder personally becomes the CT and route technician.

**Working capital.** Small, as stated (receivables about 20 days). No issue.

**Founder-draw logic:**
- The $4k/month draw from month 13 is funded from injected capital until about month 25 in Stage E's base, and until year 3 at reviewer drivers.
- In the reviewer conservative case the draw is never covered: roughly $150k of the founder's own money is used to pay the founder.
- Honest framing: the founder needs about 24–30 months of outside income or savings. The "$48k draw" is mostly the founder's own capital recycled.

## 5. Customer acquisition challenge

**How incumbents sell:**
- **Nationals** (Orkin, Rentokil-Terminix, Ecolab) sell through commercial reps, national accounts and franchise/chain programmes. Rentokil is deliberately opening small local branches to compete on proximity [B].
- **Local independents** (Verminator at 71st/Kedzie, D'Raco's and the many unlicensed-in-City operators) sell by referral, in Spanish, often at low monthly prices with set-up fees waived (E).
- Inspection comments almost never name the vendor. Even with word-boundary matching, only Ecolab appears (10 inspections) [A, F3-S001]. Incumbent share is unknowable.

**What the first 10 customers actually require:**
- The IDPH licence plus a certificate of insurance.
- Spanish (or Cantonese/Mandarin) on the doorstep. Without it, the SW cluster is the wrong cluster. The north-west cluster check in E1 should be a full parallel test, not 5 interviews.
- Roughly 100–150 owner-present conversations (at 6–10% conversion) at a price near what the incumbent charges.
- A credible written cancellation path, because many owners have 12-month auto-renewing agreements.

**The 7–21-day "after re-inspection" opener is honest and compliant**, and the materials handle the "never imply the City sent you" risk well. But it is a *prevention* pitch to an owner who just passed. That is a weaker motive than the playbook's headline.

**Reachability is fine; motive is the weak link.** Access score 5 → **4**.

## 6. Supplier / partner accessibility

- **Low refusal risk overall.** Veseris and Target Specialty gate accounts on an applicator/CT number [B], which the founder will have after the exam.
- **Most likely to refuse or delay:**
  - **Insurers** writing pollution/pesticide-drift cover for a zero-history firm and filing the IDPH certificate. Insureon medians (GL $112, auto $114) are small-applicant medians, not quotes [C, re-verified]. Commercial clients will ask for $1M/$2M with additional-insured endorsements.
  - **Landlords or the City for pesticide storage.** 830.830 storage specifications [A] plus Chicago home-occupation limits [D] mean a home garage may not qualify. The $300/month storage assumption is E.
- **The real gating partner is IDPH itself:** exam seats (10 per Westchester session, no 2027 dates posted [A, F3-S003]) and business-licence processing time (MISSING).

## 7. Legal / regulatory challenge

1. **Missed: the pending EPA rodenticide reclassification.** EPA's November 2022 proposed interim decisions would make **all second-generation anticoagulant rodenticides, strychnine and zinc phosphide restricted-use pesticides**. They would do the same for first-generation anticoagulants, bromethalin and cholecalciferol in packages over 1 lb. EPA's page still shows this as proposed, not final [A, F3-S004].
   - In Illinois, using restricted-use pesticides requires the General Standards exam **plus** the relevant restricted-use subcategory exam(s) [A, F3-S002].
   - If finalised, a general-use-only CT could not use the professional rodent baits this business runs on.
   - **Budget for the restricted-use exam from the start** (the restricted-use application and fee were not verified; confirm with IDPH) and track the EPA docket.
2. **Supervision rule cuts both ways.** Uncertified technicians are legal after two supervised uses per pesticide type per site type. After that, the CT must have voice contact at all times and be able to reach the site **within one hour** [A, 830.270 re-verified]. A founder-CT therefore cannot be out of the metro area during service hours until a second CT is employed, and a consultant cannot be the only CT [A, 830.230 re-verified]. This caps delegation (§9).
3. **Pre-licence solicitation.** 225 ILCS 235 is still unread. The playbook's "research only, no prices" rule is the right precaution.
4. **Professional advice needed:**
   - zoning and fire code for pesticide storage inside Chicago;
   - the auto-renew and cancellation clause in the 12-month agreement;
   - whether Chicago Paid Leave and minimum wage push the technician load above ×1.25.

## 8. Competitive response

- **Incumbents' cheapest response:**
  - waive the set-up fee;
  - match the monthly price;
  - send a technician the same day the newcomer's card appears;
  - for nationals, invoke the multi-year national contract.
- **Underestimated advantage of local independents:** they speak the customers' languages, they are already in the neighbourhood, and they can price at $50–80 because their owner is also the technician.
- Stage E's "competitor response" stress already takes the 10-year deployable surplus to $373. At reviewer drivers the same stress leaves nothing.
- Entry score 4 is acceptable only because a clean public re-inspection record for clients is a demonstrable, slowly accumulating proof point.

## 9. Founder execution and delegation realism

- The founder is CT, route technician, seller, dispatcher and bookkeeper for at least 3–4 years in the reviewer base. A non-technician-owner version fails (§4).
- A CT-manager (about $6,800/month) is affordable only above about $150k of pre-owner-pay profit. That is reached only on the reviewer optimistic path, around year 5.
- The supervision rule ties the founder geographically until a second CT exists.
- Delegation 7 is too high. It is **5**: delegable after 2–3 years of systemisation, *if* a second CT can be hired or grown.
- Execution risk is real but normal: a 70% exam, physical route work, and a technical-quality failure (re-citations) that the public feed will expose.

## 10. Pre-mortem

| # | Most plausible failure | Early indicator | Cheapest preventive test |
|---|---|---|---|
| 1 | **Price and motive.** Owners pay $50–90 to a neighbourhood exterminator, just passed re-inspection, and will not switch for a stranger at $110–125 | E1 median price <$90; fewer than 25% have ever switched; "we already have someone" in more than 70% of interviews | E1 as designed (≤$150), plus a **parallel north-west cluster sample of ≥10 interviews** |
| 2 | **Founder capacity cap.** About 140 accounts × (route + selling + logbooks) fills a 55–60 h week. The technician hire then sinks profit (year 5 $28.9k when hired at 110), so the business stalls at a $45–80k job | Founder hours >55/week; won accounts <4.5/month after month 8 | Time-and-motion log during E4 (minutes per stop, drive, admin per account) before committing to the vehicle lease |
| 3 | **Technical, regulatory or quality shock.** A client re-cited for pests twice, a misapplication, or the RUP reclassification forcing extra exams and product changes | Any client re-cited within 90 days; EPA final interim decision published | E7 public-feed monitoring (free); sit the restricted-use subcategory exam in year 1 |

## 11. Corrected scores

| Key | Stage E | Stage F (reviewer) | Reason |
|---|---|---|---|
| fcf | 4 | **3** | Reviewer base years 3–5 ≈ $43–80k; anchor 3 = $50–75k |
| roic | 6 | **5** | Year-3 operating profit $42.9k ÷ $78.7k peak with draw ≈ 54% (≈ 145% without draw) |
| access | 5 | **4** | 98% displacement; incumbent fixes the crisis in a median 7 days; language fit |
| scale | 6 | **5** | One CT per location; 66% of US pest firms stay under $500k [C]; reviewer base about 150 accounts at year 5 |
| resilience | 7 | 7 | Mandated service (twice a year) [A]; restaurant closures |
| entry | 4 | 4 | Copyable; weak but real proof point from the public record |
| delegation | 7 | **5** | Founder must be the CT; 1-hour supervision rule; manager unaffordable in base |
| cash | 7 | 7 | Card on file, about 20 days of receivables |
| feasibility | 8 | **7** | Licence reachable [A], but pending RUP reclassification, storage siting and an exam calendar with no 2027 dates |
| ai | 4 | 4 | Prospecting scripts and translation; not a cost advantage |

- **Composite:** raw **4.77**, evidence-adjusted (D, k = 0.70) **4.84**; at C it would be 4.80. Stage E was 5.55 / 5.47.
- I rate the economics' evidence **D**: the ticket, which is the top driver, is D- and unverifiable. Stage E rated it C. This disagreement is preserved.

**Bottom line.** The demand data are real and the licence path is real. What is not supported is the price a newcomer can charge for displacing an incumbent who already fixed the problem, and a delegation path the base case never pays for. Corrected, this is a founder-as-technician business earning about $43k (year 3) to $80k (year 5) before owner pay. The founder funds about two years of their own draw, and roughly $30k is at risk without the draw. Keep it in the finalist set **only** as a cheap test:

1. Run E1 now (≤$150) with a full north-west parallel sample.
2. Proceed to the CT exam only if the median price is ≥$90 and ≥25% switch.
3. Kill it if E4 does not produce ≥6 accounts at ≥$100.

Do not rank it above finalists whose corrected base exceeds $100k without the founder doing the core labour.

## 12. Citations spot-checked (opened this session)

| Source | Result |
|---|---|
| E-WS05007-S001 / DA-S001 / C2-S014: CDPH inspections API (recomputed) | Counts confirmed within 13%. Re-inspection confirmed. The twice-a-year rule text appears in inspector comments |
| E-WS05007-S002 / C2-S005: IDPH exam calendar JSON | Confirmed; last date 12/16/2026, none in 2027 |
| WS05-S011: IDPH Structural Pest Control page | Confirmed (CT required; General Standards suffices for general-use) |
| E-WS05007-S003: IDPH FAQ | Confirmed; licences expire 31 December |
| C2-S002: 77 IAC 830.270 | Confirmed: 2 supervised uses; voice contact; on site within 1 hour |
| C2-S003: 830.230 | Confirmed: one CT cannot be the only CT for more than one location; a consultant cannot be the only CT |
| C2-S009 / E-WS05007-S006: Rentokil H1 2026 statement | Confirmed: 80.7% retention; "needs more focus"; 70 branches; 14 businesses c.$26m revenue for $37m |
| DA-S010: Insureon pest-control costs | Confirmed: GL $112, WC $90, professional $58, auto $114 (medians) |
| C2-S021: O*NET pest-control workers, Chicago MSA | Confirmed: median $46,740 |
| E-WS05007-S011: GorillaDesk commercial pricing | Confirmed, including the low-end ranges used against the price (§2 #1) and the $63 CAC figure |
| C2-S020: HomeAdvisor via Wayback | **Could not be opened** (Wayback failed; live page 403). Treat as unverified |
| E-WS05007-S005: Chicago licence register | Partly contradicted (6 firms, not about 15) |
