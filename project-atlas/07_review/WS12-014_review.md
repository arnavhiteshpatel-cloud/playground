# WS12-014 — Stage F Adversarial Review (batch F5)

**Concept reviewed:** an employer-paid contingency direct-hire desk placing controls, automation and I&C engineers with Illinois integrators, plants and engineering firms.

**Material reviewed:**
- Stage C memo; Stage D deep dive; Stage E playbook and materials;
- `08_financial_models/WS12-014_assumptions.json` and `_results.json`;
- the prospect CSV (27 employers) and the supplier CSV;
- `sources_E_WS12-014.jsonl` plus the cited C9, DG and WS12 records.

**Reviewer:** independent; I did not write any of this. **Access date:** 2026-11-28.

**Re-runs:** made with `tools/fin_engine.py` (script `/tmp/claude-0/atlas_scratch/F5/rerun.py`). The finalist's files were not modified. New sources are F5-S006 and F5-S007.

---

## 1. Verdict: **SURVIVES WITH MAJOR REVISIONS**

**Recast it as a low-capital personal cash engine, not as the holding-company core. The Stage E base becomes the optimistic case.**

What Stage E gets right, and verified:
- the legal entry (225 ILCS 515/1.1 exclusion, with its "never charged … résumé … other personal service" proviso);
- the incumbent cyclicality data (RH perm −13.6% placements and SG&A 96.9% of perm revenue in 2025);
- the PageGroup productivity benchmark;
- the fee level.

Where it goes wrong is the **funnel**. The base has a first-time recruiter with no candidate network and no track record:
- reaching full pace in 12 months;
- converting 30% of hiring-manager conversations into signed fee agreements;
- filling 20% of those.

That produces ~8.5 placements in year 2 and ~12 in year 3, with ~$227k of year-3 revenue. That is about the output of a **mature PageGroup fee earner** (£148.9k GP ≈ $195k), who has a brand, a database and existing clients [B, verified]. It is also at or above the **modal 9–12 placements a year of established split-network recruiters** [D, F5-S006]. In 2025 it would have ranked about #3–#4 by network cash-in among Top Echelon's top-10 recruiters, though that ranking covers network deals only [D, E-WS12014-S019, verified].

The playbook's own decisive validation gate (≥5 signed agreements from 30 conversations, i.e. 17%) is **passed at a conversion rate barely half the base's 30%**. A founder who just clears the gate is in a case well below base.

**Corrected base:** conversion 22%, fill 15%, ramp 15 months, sales cycle 5 months, repeat revenue $520/month (0.35 repeat placements/yr), churn 5.5%.

| Case | Year-3 op. profit | Year-5 op. profit | Peak funding (with $4k draw) | Peak funding (no draw) | Placements y2 / y3 / y5 |
|---|---|---|---|---|---|
| Stage E base (= F5 optimistic) | $170,012 | $259,002 | $12,836 | $12,836 | ~8.5 / ~12 / ~23 |
| **F5 corrected base** | **$80,698** | **$114,468** | **$29,277** | $15,180 | ~3.7 / ~5.8 / ~7.4 |
| Corrected base + 2023-type year (new ×0.75, churn ×1.3) | $50,009 | $64,229 | $42,239 | — | — |
| Corrected base + 2009-type (new ×0.45, churn ×2) | $19,110 | $22,345 | $140,717 | — | — |
| Conservative (unchanged) | $41,471 | $55,944 | $68,241 | $21,559 | — |

- In the corrected base the desk **never hires**: trailing revenue never exceeds $20k/month. Year-5 operating profit of ~$114k is in substance the founder's own full-time recruiting wage.
- It is still the cheapest validated route to six-figure personal income in Atlas, with ≈$600 to validate and ≤$30k at risk. That is why it survives.
- It is weak on scale, delegation and resilience. That is why it should not anchor the holding company.

---

## 2. Factual errors found

| # | Claim | What the source says | Correction |
|---|---|---|---|
| F1 | Base per-producer revenue "≈$195k at year 3 … at to ~15% above PageGroup's average fee earner" is described as merely "optimistic for a newcomer" | PageGroup's £148.9k GP per fee earner is a **blended** figure across a 72%-perm/28%-temp mix, earned inside a firm with brand, database, management and existing clients. The release names interview-to-offer conversion as its "most significant area of challenge" [B, verified]. | A first-time solo recruiter equalling the *average* PageGroup fee earner by year 3 is not a base case. It is the optimistic case. Corrected year-3 revenue is ~$110k (≈55% of the benchmark). |
| F2 | Base funnel 30% conversation → signed agreement is consistent with the validation plan | The plan's success threshold is ≥5 signed from 30 conversations = **16.7%**, and the kill threshold is <2 (6.7%). | The base sits nearly 2× above the gate. Set base conversion at ~20–22%, so that passing the gate is consistent with the base case. |
| F3 | "Top-10 Top Echelon split-network recruiters produced $99k–$524k" used to say a $130k junior is "below the mature-firm average" | Verified: the #10 had 7 placements / $99,312 and #1 had 61 / $523,600. These are the **top 10** of a national network (network deals only). | This list shows the *top* of the distribution, not the average. It supports a lower newcomer base, not the filed one. |
| F4 | Stage D: "LinkedIn Recruiter Lite price MISSING"; Stage E: $170 [D] | Third-party pages only. | No error; still D. Confirm at checkout. |

**Verified as stated:**
- 225 ILCS 515/1.1 exclusion text, including the 18+/HS-diploma, no-fee, résumé and "other personal service" provisos and the theatrical/domestic carve-out [A];
- IDOL FAQ 1, 7 (criminal sanctions, $1,000 fine) and 14 [A];
- RH 2025 10-K: perm $440M (−9.8%), placements −13.6%, average fee +3.8%, perm SG&A 96.9% of revenue [A];
- PageGroup: GP per fee earner £148.9k, conversion 2.7% group / 3.2% Americas, 4,968 fee earners, North America GP +8% with the US +9% and Manufacturing strong [B];
- JOLTS manufacturing openings: 376k (Apr 2025), 426k (Dec 2025), 584k (Sep 2026, preliminary) [C, BLS API];
- Top Echelon 2018: engineering 23% / $24,521 / $105,831; overall 21.6% / $20,283 [D];
- secondtalent/SIA 2021: 20% most common (42% of firms), direct-hire-only firms 20–25%, RH 35% standard vs 25% contract [D]. Note that the source treats 20% as a *floor*, so the fee assumption is, if anything, cautious;
- Recruiterflow: "no universally agreed industry number" for ramp, and a first placement or near-miss by days 61–90 *inside a firm* [D];
- LinkedIn Hiring Assistant GA in English by end-September 2025, with 4+ hours, −62% profiles and +69% InMail acceptance [B; vendor claims];
- Formic: 72 open roles; Chicago/Bolingbrook Controls & Automation Engineer $120–145k, updated 2026-11-05 [D, live Greenhouse API].

**Spot-checks:** 11 citations opened. All substantively verified; the errors are in interpretation.

---

## 3. Unsupported or over-stated claims

| Claim | Evidence level actually warranted |
|---|---|
| Founder full pace in 12 months, then 9 × 30% × 20% = 0.54 new paying clients/month | **E**, and above the available D benchmarks for experienced recruiters. The in-firm ramp source assumes the *firm's existing job orders* [D, S023]. A solo newcomer must build candidates and clients at once. |
| "A founder with a tech/research background can learn to run a credible technical screen" (the wedge); Day-1 plan of a "2-hour self-study of PLC/SCADA basics" | **E.** Screening ladder logic, commissioning and DCS experience is a trade skill. A research background is adjacent, not equivalent. Until a placed engineer or hiring manager validates the screen (gate §4.5), the wedge is hypothetical. Entry 4 → 3. |
| Repeat engine: 0.45 repeat placements per active client per year, at zero modelled labour | **E**. Unsourced, as the playbook concedes. Repeats consume the same desk time as first placements, so the engine overstates capacity. Corrected to 0.35. |
| Referrals 2 per 100 active clients a month | E; immaterial at <10 clients. |
| "First cash between months 5 and 10" | E; plausible for a capable founder. The model's smoothing reaches one full fee of revenue by month 11, which is consistent. |
| Fallout/discount reserve 15% | E with an A mechanism (Kforce net-of-fallout). Reasonable. |
| Valuation 2.0× | D/E; arguably generous for a single-producer desk where relationships leave with the producer. 1.0–1.5× is more defensible. |

---

## 4. Financial model audit

**Recomputation.** The engine mirror reproduces the filed results exactly: base y3 $170,012, y5 $259,002, peak $12,836; conservative $41,471 / $55,944 / $68,241. The transaction math is correct: $105k × 20% = $21,000 − 15% reserve − $420 = $17,430.

**Top-5 drivers challenged:**

| Driver | Stage E base | Independent evidence | F5 corrected base | Level |
|---|---|---|---|---|
| Conversation → signed agreement | 30% | Own gate success = 16.7%. Large employers gated ("please do not contact our hiring managers" [D, verified in Stage E]) | **22%** | E |
| Agreement → placement (fill) | 20% | Non-exclusive contingency orders competing with in-house TA (LinkedIn Hiring Assistant [B]) and Actalent/Aerotek. PageGroup flags offer-acceptance conversion as its top problem [B] | **15%** | E |
| Founder ramp | 12 months | No agreed number; in-firm ramp assumes existing job orders [D] | **15 months**; sales cycle 4 → **5** | E |
| Repeat revenue / churn | $670/month (0.45/yr), 5% | Unsourced | **$520 (0.35/yr), 5.5%** | E |
| Realised first fee | $17,850 | 20% is the most common fee and is treated as a floor [D]; RH average fee rose through downturns [A] | **Kept**; stress at 18% × 80% gives y3 $69,234 / y5 $100,494 | D |

- **Single-driver effects** (y3): conversion 22% alone gives $131,237; fill 15% alone $134,576; ramp 15 alone $178,794 (year 3 rises from a later hire).
- **Benchmark check of the corrected base:** ~3.7 placements in year 2 (first full year), ~5.8 in year 3, ~7.4 in year 5. That is below the modal 9–12 of established network recruiters [D, F5-S006], which is appropriate for a first-time solo desk. Recruiterflow's data shows output is extremely skewed: top quartile 5.21 placements per recruiter vs 1.38 for the rest, period unstated [D, F5-S007]. A capable newcomer reaching ~6/yr by year 3 is a fair base. Matching the filed base requires top-quartile performance.

**Working capital and draw.**
- Receivables only: DSO 40 days. That is correct and benign.
- **In the corrected base the $4k/month draw is not covered until about month 20, so peak funding is $29k with the draw versus $15k without.**
- The model excludes the founder's living costs for months 1–12. With the first fee arriving around months 6–10, the real "capital" is 6–12 months of personal runway. That is acceptable only if the founder can self-fund it.
- A 2009-type year during ramp pushes peak funding to ~$141k with the draw. In practice that means stopping, not borrowing.

---

## 5. Customer acquisition challenge

- **The cold-start loop is the real barrier.** Candidate-led marketing needs movable, vetted candidates. Candidates engage when the recruiter has live, credible job orders. The founder starts with neither. Every experienced recruiter who goes solo brings a book of candidates and two or three clients; this founder brings none. That is the core reason the base should sit near 0.3 new paying clients/month, not 0.54.
- **The best buyers are fenced off.** Large employers use agency portals (Abbott) and explicit no-contact notices (Chamberlain). Volume competitors (Actalent/Aerotek, an Allegis company) already work Illinois controls roles. In-house TA now has agentic sourcing (LinkedIn Hiring Assistant [B]). The accessible segment is integrators and mid-size plants, which is a smaller and lumpier pool.
- **Incumbent sales motion:** a specialist recruiter typically makes daily calls to hiring managers about a specific candidate, and gets repeat orders from the same few integrators. The playbook's motion is right; the volume and conversion assumed are not.
- **What the first 10 clients really require:**
  1. ~3–6 months to build a pipeline of 30–50 qualified controls engineers.
  2. A technical screen hiring managers trust: a short paid consult with a senior controls engineer to calibrate the scenario bank, or a placed-engineer reference.
  3. Acceptance that early fees may need 18% or a two-role exclusive.
  4. Roughly 150–250 hiring-manager touches to get ~30 conversations (E).
  5. 12–24 months for 10 distinct paying clients, against Stage E's ~17–18 months.

---

## 6. Supplier/partner accessibility challenge

Low risk. Tools are self-serve with published prices (Recruit CRM, Loxo, Crelate [B]) or are third-party-priced (Recruiter Lite [D]).

The two partners most likely to disappoint are:
- **Top Echelon/split networks.** Split terms are unpublished, and controls job orders in the network are unverified; Q2 2025's largest fees list contained no controls roles [D, verified in Stage E].
- **Vendor portals at large employers.** These typically require insurance certificates and MSAs, and give preference to established vendors. Treating them as year-2 targets is right.

LinkedIn's terms on scraping are respected in the plan.

---

## 7. Legal/regulatory challenge

Stage E's legal section is accurate and better than most. Verified: the licence exclusion, salary-history ban, pay-scale third-party liability, criminal-history timing, AI Video Interview Act, the IHRA AI amendment (C) and the non-compete thresholds.

Remaining items:
1. **Staying inside the exclusion is an operating discipline, not a one-time fact.** "Indirectly" charging a fee, or "any other personal service" (résumé polishing, interview coaching sold to candidates, or a candidate-paid "career" product later), voids it [A]. Put it in the operating agreement.
2. **Counsel questions are correctly flagged:**
   - out-of-state placements of Illinois residents and vice versa (other states' agency laws may apply);
   - FCRA if the desk runs reference checks;
   - fee-agreement enforceability.
3. **Chicago business licence** if operating within city limits [D]. Confirm with BACP.
4. **Fee disputes and collections** are the most likely legal cost. The materials' candidate-ownership and time-stamped-submittal clauses are the right mitigations. Budget for at least one collections action in the first 24 months (E).

No gate concern; feasibility 9 stands.

---

## 8. Competitive response

- Incumbents will not notice a single new desk. The response comes from:
  - **in-house TA** with AI sourcing [B], which shrinks the set of roles that need an agency to the genuinely scarce and senior ones;
  - **volume firms** offering contract-to-hire;
  - **marketplaces** (Paraform 80% split [D]) that pool job orders and compress fees on commoditised roles.
- **Underestimated incumbent advantage:** proprietary candidate databases. Recruiterflow reports top firms place 54.4% of hires from candidates already in their CRM [D, verified]. The newcomer starts at 0%.
- **Fee rate is not the vulnerability.** RH's average fee rose through 2023 and 2025 while placements fell [A]. Volume is.

---

## 9. Founder execution & delegation realism

- **Founder-bound by construction.** In the corrected base no recruiter is ever hired. In the Stage E base, recruiter #1 arrives in month 35 and #2 never does.
- **Delegation path:**
  - a 6-month trailing revenue trigger of ≥$20k/month;
  - a recruiter ramp of 6–9 months, with ~50% wash-out (E);
  - non-competes void below $75k/$80k [A];
  - so a hired producer can walk with clients.

  Realistic delegation needs an experienced controls recruiter as a team lead (~$130–150k all-in, E). The playbook correctly notes that this halves deployable cash.
- **Founder fit.** The founder must enjoy daily cold calling and candidate persuasion. The playbook's kill rule ("dislikes cold calling after 60 days → abandon") is exactly right.
- **AI after 5 December 2026:** negligible dependence (~$60/month). Correct.

---

## 10. Pre-mortem

**The three most plausible ways it fails:**

1. **Cold start never closes.** Candidates reply, but managers either do not sign, or sign and then fill internally or through Actalent. Twenty submittals in six months produce no final-round interview.
   - **Early indicator:** <5 agreements from 30 conversations by day 60; zero final rounds by month 4.
   - **Cheapest test:** test 3 as written ($0–270).
2. **A slow ramp meets a cycle turn.** The first 2–3 placements land in months 8–14, then manufacturing openings reverse (they fell 63% from April 2022 to April 2025 [C]). Year-2 revenue stalls at ~$40–60k while the draw runs.
   - **Early indicator:** Tier A/B postings down >40% quarter on quarter; JOLTS manufacturing openings falling for two consecutive prints.
   - **Cheapest test:** keep the weekly ATS scan running, and hold a 4–6-month personal runway before month 1.
3. **Fee leakage.** Disputes ("we already had that résumé"), guarantee fallouts and 18% intro fees push realisation to ~80% at 18%, and one bad-debt client wipes out a quarter.
   - **Early indicator:** DSO >60; any dispute in the first five placements.
   - **Cheapest test:** attorney-reviewed agreement before the first submittal; time-stamped consent log.

---

## 11. Corrected scores and bottom line

| Criterion | Stage E | F5 | Reason |
|---|---|---|---|
| fcf | 5 | **4** | Corrected base y3 $81k, y5 $114k, i.e. the founder's own production |
| roic | 8 | **7** | $81–114k on ~$15–29k at risk (≈300–750%), excluding founder runway; downturn peak much higher |
| access | 5 | **4** | No candidate network or track record; large employers gated; in-house AI sourcing |
| scale | 4 | **3** | Corrected base never hires; ceiling ≈ one founder desk without a team lead |
| resilience | 3 | **3** | Perm is the most cyclical line (RH −57% 2009, −21.7% 2023) [A] |
| entry | 4 | **3** | The technical-screen wedge is unproven for this founder; copyable |
| delegation | 4 | **3** | Founder-bound; non-competes void for juniors; G7 WARN |
| cash | 7 | **7** | No float; net-30 receivables |
| feasibility | 9 | **9** | Licence exclusion verified [A] |
| ai | 5 | **5** | Real productivity help, equally available to clients' in-house teams |

- **Raw score:** 4.50. **Evidence-adjusted (D):** 4.65. Stage E was 5.25 / 5.17.
- **Profit range (year 3):** $41,471 (conservative) / $80,698 (corrected base) / $170,012 (Stage E base as optimistic).
- **Year 5:** $114,468 corrected base; $55,944 conservative.
- **Plausible milestone ceiling:** ~$100–150k/yr as a founder desk. $250k+ only with an experienced team lead and 2–3 producers, which is the optimistic path.

**Bottom line.** This is a legally clean, capital-light business that can be tested for ~$600 in 60 days. The Stage E author was candid about its founder-dependence and cyclicality. But the base case gives a first-time recruiter, with no candidates and no clients, the output of an established specialist by year 2–3. Its own validation gate implies a much lower funnel.

Evidence-adjusted, it is a good *job*:
- ~$80k year 3 and ~$115k year 5 before owner pay;
- ~6–7 placements a year;
- no hires;
- highly exposed to a manufacturing downturn.

It can fund the founder's living costs and some seed capital. It will not become a self-running, cash-compounding first asset unless the founder proves top-quartile production and then recruits an experienced team lead. If the founder runs it, set a month-24 boutique-or-harvest decision from the start.
