# SYN-001 Stage F review (batch F2): Insurance-led small-carrier compliance hub

Independent adversarial review, 2026-11-28. I did not write any of the material reviewed. This was read-only desk work: nobody was contacted, and no form, account or enquiry was created. New sources are in `07_review/sources_F2.jsonl` (F2-S###). Helper scripts are in `/tmp/claude-0/atlas_scratch/F2/` (`syn001_cohort.py`, `syn001_cohort_results.json`). The finalist's model files were not modified.

## 1. Verdict

**Survives with major revisions.** The data work is excellent. I re-ran it from the FMCSA APIs and reproduced it exactly:
- the niche is 3,166 carriers, with the same county split [A, F2-S012];
- 2,750 of them have a current BIPD primary filing;
- the insurer shares match: Progressive/Artisan 14.0%, Great West 13.1%, Northland 12.1%, GEICO 8.4%, Sentry 5.5%, Acuity 5.3%, Berkley 4.0% [A, F2-S013].

The market-access diagnosis is also right. The path through a host agency (sub-producer) is the honest base case.

**Two errors materially overstate the economics.**

1. **The model's attach error.** The model raises one blended ARPC for every client by 9% a year. The intent is that insurance attach "matures" to 5/14/21/25/28%. But that path is attach by *client tenure*. The model applies it to the *whole book*, including clients who joined last month and have not yet reached a renewal.
   - In a book that is growing fast, most clients are young.
   - Corrected by cohort, the book-average attach is **about 11% in year 3 and about 13% in year 5**, not 21% and 28%.
2. **A legal problem the playbook missed.** The playbook and the customer-facing draft offer "20% off when we also place your liability". Illinois' anti-rebating statute, 215 ILCS 5/151, bars an agent from giving "any paid employment or contract for services of any kind or any other valuable consideration or inducement to or for insurance... not specified in the policy" [A via mirror, F2-S019]. Bills to allow value-added services do not appear to have been enacted (SB 3466 in 2022; HB 2766 re-referred to Rules in 2025) [D, F2-S020]. Even those bills would have required that the benefit *not* be conditioned on buying insurance.
   - The tie-in discount has to go unless Illinois counsel clears it.
   - The broader tactic of below-cost compliance as an insurance lure also needs a legal read.

**Corrected base view.** Filed funnel, cohort-correct attach, and a 40% blended sub-producer split instead of 50%:
- year-3 operating profit about **$33k** (filed: $48k);
- year-5 operating profit about **$102k** (filed: $178k);
- peak funding about **$95k** with the $4k/month draw, about $37k without.

With a modest funnel haircut (15 leads a month, 22% win rate, 1.8% monthly churn), year 5 is only about $52k. That is close to the compliance-only case.

## 2. Factual errors found

| # | Claim (where) | What the source or arithmetic actually shows | Correction |
|---|---|---|---|
| F1 | "Blended year-3 ARPC ~$362 ($305 × 1.09²)", with attach maturing "5/14/21/25/28% across years 1–5" applied to all active clients (playbook §3, §7.1; assumptions `arpc_annual_growth_pct`) | The assumptions' own derivation describes attach "after 3 yrs" of tenure. The engine multiplies every active client's ARPC by `price_index`, so a client who joins in month 40 is credited with the year-4 attach immediately. A cohort recalculation using the engine's own new-client and churn series gives book-average attach of 5% in year 1, ~11% in year 3 and ~13% in year 5 | Year-3 operating profit falls from $48.3k to $37.1k and year 5 from $177.5k to $113.9k. Peak funding with the draw rises from $69k to ~$85k. This is the **most important error** |
| F2 | "Clients who place their auto liability through us get 20% off, mirroring OOIDA's tie" (playbook §2.6; materials lines 179, 200, 229, 255) | 215 ILCS 5/151(1) prohibits inducements to insurance not specified in the policy, including "contract for services of any kind" [A via mirror, F2-S019]. The value-added-services reforms are apparently unenacted [D, F2-S020] | Remove the discount from all drafts. Get an Illinois insurance-counsel opinion on the whole bundle, including the free audit timed to renewal, before launch. That an incumbent does something is not a legal opinion |
| F3 | "Business-entity licence: only if we bill insurance ourselves" (playbook §5.3) | 215 ILCS 5/500-80(a)–(b) bars paying or accepting commission for selling, soliciting or negotiating insurance without the required licence. Subsection (d) lets commission go to "an insurance agency" or to persons who do not sell, unless that would violate §151 [A via mirror, F2-S021]. The founder's LLC does sell through the founder | If the host pays the split to the founder's LLC, the LLC almost certainly needs an IDOI business-entity licence with a designated producer. Otherwise pay the founder personally. Confirm with IDOI or counsel |
| F4 | Progressive's "2–3 years of agency experience" comes from a Texas association's personal-lines page (playbook §2.2) | The IIAT page is filed under personal lines but is headed "Personal and Commercial Auto Insurance". It requires 2–3 years of agency ownership and P&C experience, $1M E&O, a storefront and monthly minimums [B, F2-S014] | The citation is correct and in fact stronger than described: it covers commercial auto. It is still Texas-specific |
| F5 | The 84% agency-retention figure supports 1.5% monthly churn (assumptions) | The IA Magazine figure comes from a survey of ~1,200 independent agencies of all lines. It is not trucking-specific and not commercial-specific [C, F2-S024] | It is a weak anchor for a compliance subscription sold to small carriers. Use 1.5–1.8% monthly churn, and label the figure C-general |
| F6 | The month-12 milestone of "≥3 insured accounts" and "≥2 binds by month 6" (playbook §10) | The base model has 10.9 clients × 5% attach, which is about 0.5 insured accounts at month 12 | The validation gate is 6× the model's own expectation. Either the gate is unrealistic or the model is too pessimistic in year 1. Reconcile them: I would keep the gate as a kill test and accept that most founders will fail it |

**Checked and correct:**
- The Amwins 1–25-unit programme: Lancer paper, 2 years on the current DOT, "distributed through a select group of retail brokers" [B, F2-S015].
- The Union General trucking GA agreement, which says:
  - commission is "as approved" by the GA;
  - the producer pays premium due "whether or not Producer has collected such premium";
  - premiums are held in trust;
  - the producer retains its expiration list on termination [B, F2-S016].
- Smart Choice's 30–90% producer splits, with examples of 50/40 and 60/40 [D, F2-S017].
- Cover Whale writes auto liability in 41 states for 1–25 power units, needs a dashcam or ELD, and does not publish commission. Illinois is not named [B, F2-S022].
- DOTDriverFiles costs $5 per driver per month; MVR from $12.95; PSP $19.99 [B, F2-S023].

## 3. Unsupported or over-stated claims

| Claim | Evidence level actually warranted |
|---|---|
| A host agency will pay 50% on new **and** renewal business, with vested or founder-owned expirations | E. Published splits are 30–90%, often lower on renewals [D, F2-S017]. A sample agreement found in search keeps 60% for the agency (D). Courts usually uphold non-solicits for 2–3 years [C, F2-S018]. A host lending its appointments and CSRs to a first-year producer has every reason to keep the expirations. **Base should assume a 40% blended split, a host-owned book and a 2-year non-solicit** |
| Host gross commission of 12% | E. The only trucking figure is "generally 10%" through MGAs/wholesalers (D, 2010 forum, DC-S014). The 15.9% Illinois selling expense includes acquisition costs beyond commission [C]. Use 10–12% |
| 25% proposal-to-win and 20 qualified conversations a month | E. There is no benchmark. Competitors give compliance away free to insureds (C4-S038). The 3–5-driver tier at $199 competes against $149–249 done-for-you plans (D) and $5-per-driver software [B, F2-S023]. Managed DQ pricing from J.J. Keller is unpublished; the site says to "speak with a Compliance Specialist" [B, F2-S025] |
| "One 6-truck insured account is worth $3,800–5,900 a year" | Arithmetic is fine. The $12k/truck premium rests on ATRI's 10.6¢/mile with small fleets paying nearly double (C, WS02-S017). The CCJ page returned 403 on re-check, so it is not re-verified |
| Year-10 owner wealth $1.82M; enterprise value at 3.5× | E. In the base case the host may own the expirations, so the saleable asset is a compliance book worth roughly 1–2× SDE plus whatever expiration rights are negotiated |
| Optimistic case: $825k year-5 operating profit, 282 clients | Upper tail only. Drop it from milestone tables |

## 4. Financial model audit

**Reproduced.** The engine reproduces every headline:
- base year 3 $48,348, year 5 $177,513, peak funding $69,328;
- conservative never breaks even, peak $357,303.

**The true first-year cash profile (base, filed):**

| Item | Value |
|---|---|
| Revenue, year 1 | $13.4k |
| Operating profit, year 1 | −$29.7k |
| Setup capex | $4.5k |
| Cash out, year 1 | ~$35.6k (founder unpaid) |
| Insurance commission, year 1 | Essentially nil: 0.5 insured accounts at month 12, worth roughly $1–2k |
| Cash after the draw starts (month 13) | Keeps falling, to $672 at month 31, as the first coordinator is hired at 35 clients |

The real first-year business is an **unpaid compliance office**. Insurance does not contribute meaningfully until year 2 at the earliest.

**Driver challenges** (top 5 by impact):
1. **Attach by tenure, not calendar.** See F1. Cohort-correct attach takes year-3 operating profit to $37.1k and year 5 to $113.9k.
2. **Sub-producer split: 50% → 40% blended** (new and renewal mix, host-owned book; D/E). Insurance per insured client falls from $360 to $288 a month. With the cohort fix: year 3 **$33.5k**, year 5 **$102.1k**, peak about $95k with the draw and $37k without.
3. **Attach path at two-thirds of filed** (3/9/14/17/19% by tenure). This applies if "lets us quote" is 50% rather than 70% and the win rate is 40% rather than 50% (E). Year 3 $28.2k, year 5 $85.6k, peak about $116k with the draw.
4. **Funnel.** At 15 leads a month, 22% win rate and 1.8% monthly churn, together with fixes 2 and 3: year 3 $41.5k, year 5 $51.8k, 58 clients.
   - Year 3 *rises* because the coordinator hire at 35 clients is delayed. That is a step-function artefact.
   - Year 5 is the honest figure: close to the compliance-only case ($59k).
5. **Reviewer conservative** (12 leads, 18% win, 2.2% churn, low attach): year 3 $7.9k, year 5 $51.7k, peak about $168k. Profit is still positive only because the founder performs all servicing unpaid for 34 clients.

| Case | Year 3 op. | Year 5 op. | Book-average attach, year 5 | Peak (draw) | Peak (no draw) |
|---|---|---|---|---|---|
| Filed base | $48.3k | $177.5k | 28% (as filed) | $69.3k | $36.6k |
| Cohort attach | $37.1k | $113.9k | 13% | ~$85k | ~$37k |
| **Reviewer base** (cohort attach + 40% split) | **$33.5k** | **$102.1k** | 13% | **~$95k** | ~$37k |
| + attach path at two-thirds | $28.2k | $85.6k | 9% | ~$116k | — |
| + funnel haircut | $41.5k | $51.8k | 10% | ~$136k | — |

Peaks for the cohort runs are approximate: they are computed from the engine's retained-cash series plus the operating-profit delta, before second-order tax effects.

**Working capital.** Compliance is prepaid, so working capital is not an issue on the sub-producer route. On the own-agency or GA route it is a real liability: premium is owed within 30 days whether collected or not [B, F2-S016]. The playbook handles this correctly.

**Founder draw.** Cash stays positive only because the founder services up to 35 clients unpaid for about 26 months, then draws $4k. The playbook's own figure of $13–21 an hour in years 2–3 is right.

## 5. Customer acquisition challenge

- **Reach is the business's best feature.** It rests on A-level data: renewal month and switch history for every target [A, F2-S013].
- **Winning compliance clients is unproven.** Owners of 3–20-truck firms are flooded with "FMCSA" mailers, so trust is the barrier.
- **Incumbent sales motions:**
  - OOIDA sells to members;
  - Simplex and DOT Compliance Group run national phone teams;
  - insurance agencies give DOT monitoring away free to insureds.
- **The local, in-person wedge is real but copyable.** The first 10 clients need roughly 60–80 yard visits and audits, plus a written host agreement *before* any insurance conversation.
- **Insurance attach is gated twice.** First the client's renewal date arrives. Then the host's markets must beat the incumbent agent, who usually also gives compliance help free.
- **Realistic year-3 attach** is 7–15% of the book, not 21%.

## 6. Supplier and partner accessibility challenge

**Most likely to refuse or offer poor terms:**
1. **Chicago trucking agencies as hosts.** A host gains a producer with leads but no book. Expect:
   - a 30–50% split on new business and lower on renewals;
   - expirations owned by the host;
   - a non-solicit of 2–3 years [C, F2-S018];
   - possibly a demand to see the compliance client list.

   Some will see the founder as a future competitor and decline.
2. **Progressive direct.** It needs 2–3 years of experience plus minimums [B, F2-S014].
3. **Amwins' "select group" programme** [B, F2-S015].

**Accessible:**
- Cover Whale, if Illinois auto liability is open; not confirmed [B, F2-S022];
- trucking GAs on agency-bill terms [B, F2-S016];
- DOTDriverFiles and consortium vendors.

## 7. Legal and regulatory challenge

1. **Anti-rebating and inducement (§151).** This is a new finding (F2). It affects the 20% discount and possibly the free-audit lure. It needs an Illinois insurance-counsel opinion before any materials are used.
2. **Commission recipient licensing (§500-80).** The LLC needs a business-entity licence if it receives commission (F3).
3. **Referral fees to factoring, dispatch and dealer partners.** Paying unlicensed referrers per placed policy is restricted by §500-80. Pay flat, non-contingent marketing fees only, after counsel review.
4. **The host agreement itself.** Have counsel review expiration ownership, the non-solicit, the assignment to the founder's entity, and the treatment of the compliance client relationship. That client relationship must be carved out explicitly, or the host's non-solicit could reach the founder's own compliance clients.
5. **Part 40 C/TPA limits and Clearinghouse service-agent registration.** These are correctly identified. E&O must cover compliance administration (correctly flagged).
6. **ilga.gov was unreachable.** Statute text came from an unofficial mirror whose source lines predate recent sessions. Treat it as A-text with C-currency until checked on the official site.

## 8. Competitive response

- Incumbent agents respond to a quote request at renewal by matching it, or by adding free compliance. Section 151 constrains them too, but large agencies have counsel-approved programmes.
- OOIDA and Simplex already bundle.
- GEICO writes direct (8.4% of in-force).
- The underestimated advantage is the incumbent agent's **control of the policy and the filings**. Moving a trucking policy mid-term is rare, so the founder gets one shot a year per client.

## 9. Founder execution and delegation realism

- The founder needs three things: a P&C licence (achievable in 6–10 weeks), trucking underwriting fluency (a 1–2-year learning curve, under-weighted in the playbook), and yard-level selling.
- The early workload is a dual job: about 95 hours a month servicing compliance plus about 90 hours selling.
- Delegation is plausible for the compliance side: coordinators are a standard role.
- The insurance side stays founder-dependent until a second licensed producer exists. A host-owned book limits what is ever delegable or saleable.
- AI use (OCR and letters) is cheap and durable but not differentiating.

## 10. Pre-mortem

| # | Failure | Early indicator | Cheapest preventive test |
|---|---|---|---|
| 1 | No host offers better than a 35% split with host-owned expirations and a broad non-solicit; insurance economics never justify the effort | Fewer than 2 written term sheets from 12 conversations | V1, and include an explicit carve-out request for the compliance client list ($0) |
| 2 | Compliance clients sign but stay with their incumbent agent: book-average attach under 8% at month 24; the founder runs a $59k-a-year compliance office | Fewer than 3 of the first 10 renewals give quote authority | V4 attach test on the first 6 renewals before any hire |
| 3 | A regulatory complaint from a competing agent over the insurance-tied discount or free services (§151) | Any materials using the discount | Counsel opinion before printing materials (~$500–1,500) |

## 11. Corrected scores

| Criterion | Stage E | Stage F (F2) | Reason |
|---|---|---|---|
| fcf | 4 | 4 | Reviewer base: year 3 ~$33k, year 5 ~$102k; downside $52k |
| roic | 6 | **5** | ~$100k year-5 operating profit on ~$95k at risk with the draw (~$37k without) |
| access | 5 | 5 | A-level targeting; trust barrier; double-gated insurance |
| scale | 6 | **5** | ~3k-carrier local niche; host-owned book; non-resident licences per state |
| resilience | 6 | 6 | Mandated demand; freight-cycle churn |
| entry | 4 | **3** | Bundle is the incumbent model; §151 limits the tie that was supposed to be the wedge |
| delegation | 6 | **5** | Insurance side tied to the founder's licence and host relationship |
| cash | 7 | 7 | Prepaid compliance; host pays monthly |
| feasibility | 6 | **5** | Host dependency; §151 and §500-80 issues need counsel |
| ai | 6 | **5** | Back-office only |

**Composite:** raw **4.82**, evidence-adjusted **4.87** (evidence D). Stage E was raw 5.37 / adjusted 5.26.

**Gates:**
- G3: **WARN**, pending counsel on §151; not FAIL, because the discount is removable.
- G4: passes in the reviewer base at year 5 only.
- G7: WARN.

**Bottom line.** The data work is the best I have seen in the project, and I reproduced it exactly. The diagnosis that trucking insurance market access requires a host agency is correct and honest.

The model then overstates the profit engine:
- It credits every new client with matured insurance attach. Fixing this alone cuts year-5 operating profit by about 36%.
- It assumes a generous 50/50 split on a book the founder probably will not own.
- The playbook's main retention tool, the insured-client discount, is very likely an illegal inducement under 215 ILCS 5/151.

Corrected, this is a ~$100k-a-year business by year 5 if a decent host is found. Otherwise it is a ~$50–60k compliance office. It is worth the $0–1,500 V1/V2 validation. It is not worth a full-time commitment until a written host term sheet and at least 3 quote authorities from the first 10 renewals exist.

I disagree with Stage E's year-5 base of $178k and its feasibility and entry scores. I agree with its ranking caution: "rank it behind finalists with a stronger base case and no third-party dependency".
