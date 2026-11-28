# Pricing Validation Plan (v1, 2026-11-27)

**Purpose:** turn the five founder pricing hypotheses into tested, defensible prices, or replace them. This plan sits on top of `PRICING_EXPERIMENT.md`: it keeps that file's three phases (interview pricing → real proposals → pilot-to-paid conversion) and adds the new offerings, the question scripts, the sample sizes, the logging fields and the decision thresholds.

**Status:** no interview has been run. Every price below is a hypothesis [HYP].

| Code | Offering | Hypothesis range | Model Base | Primary segment |
|---|---|---|---|---|
| H1 | Paid pilot (10–20 retrospective scans) | $2,500–5,000 | $3,500 | Manufacturers, CROs |
| H2 | Non-GLP study analysis (≤40 scans, ≤2 time points) | $8,000–15,000 per study | $11,000 | SME orthobiologic and dental manufacturers |
| H3 | Material characterisation | $5,000–15,000 | $9,000 | Manufacturers, CROs |
| H4 | Academic desktop licence | $4,000–10,000 per year | $6,000 | Academic labs, micro-CT cores |
| H5 | Enterprise desktop licence | $30,000–75,000 per year | $45,000 | CROs, high-volume manufacturers |

---

## 1. Principles
1. **Behaviour beats stated intent.** Interview answers are directional only. A hypothesis is validated only when someone pays, or signs a real offer (§7).
2. **Price questions come last** in a discovery interview, after the questions about pain, volume and current cost (`INTERVIEW_GUIDE.md` §11). Never quote a price first.
3. **Ask only about offerings the person could buy.** Manufacturers answer H1–H3. CROs answer H1, H3 and H5. Labs and cores answer H4, and H1 only if they run industry-funded work.
4. **One unit per question, defined on a card.** Respondents price different things if the unit is vague. Read the card aloud (§3).
5. **Anchors are only published, cited prices** (§5), and are shown only *after* the respondent has given their own numbers.
6. **Honesty.** Price-ladder questions are introduced as hypothetical ("if a service like this cost…"). Never imply that OsteoQuant is validated, GLP-compliant or already has customers. Never discuss prices with competitors.

## 2. Sample sizes and timing
| Segment (code from `INTERVIEW_CODING_SCHEME.md`) | Minimum interviews with pricing answers | Target | When |
|---|---|---|---|
| Manufacturers (MFR-SME, MFR-ENT, OEM, TISSUE) | 8 | 15 | Discovery waves 1–2 |
| CROs (CRO-DEV, CRO-ACAD, CRO-HISTO) | 3 | 6 | Waves 1–2 |
| Academic labs and cores (LAB, CORE) | 6 | 10 | Waves 1–3 |

Below about 30 responses per segment, Van Westendorp curves are **directional only**. Report medians, ranges and raw counts. Do not claim statistical significance.

## 3. Unit cards (read aloud; also shown on screen)
- **Card P (H1), paid pilot:** "We analyse 10–20 scans from a study you have already finished, blind to your results, and compare against your own analysis: agreement statistics, the time each step took, and a debrief. Research use only."
- **Card S (H2), non-GLP study analysis:** "One complete non-GLP study: up to 40 reconstructed scans, up to 2 time points, one defect model. You get a reviewed segmentation, morphometry using ASBMR nomenclature, an audit trail and a report. Residual-graft, new-bone and total-mineral volumes are reported only where the scan supports them; in simulation many are refused, and new-bone volume was never supported in the held-out tests. Not for GLP use."
- **Card M (H3), material characterisation:** "Before a study: we assess whether your graft material can be told apart from new bone at your scanner settings and recommend scan settings. The answer may be 'not separable by micro-CT alone'. We do not design or analyse day-0 baseline scans."
- **Card A (H4), academic licence:** "The desktop application for one lab or core, installed locally (no data leaves your computers), with updates and email support, for one year."
- **Card E (H5), enterprise licence:** "The desktop application for your whole organisation: multiple seats, onboarding, and a document pack describing what has been tested. It is not a GLP validation. One year."

## 4. Question scripts (embedded in `INTERVIEW_GUIDE.md` §11)

### 4a. Current cost first (behavioural anchor)
Ask before any price question:
1. "For your last study, roughly how many analyst hours went into the micro-CT analysis, from reconstructed scans to final numbers?" → `analyst_hours_per_study`
2. "If you outsourced it, what range was that line item?" → `outsource_cost_range_usd`
3. "Is that money budgeted per study, per year, or from a grant or core recharge?" → `budget_source`
4. "Above what amount does a purchase need procurement or committee approval?" → `approval_threshold_usd`

Derived figure: `current_cost_per_study_usd` = hours × the respondent's loaded rate, if they shared one, or the outsourced amount. **Do not** fill this in with OsteoQuant's own assumptions.

### 4b. Van Westendorp: four questions, one card at a time
Ask in this order and record numbers only:
1. "At what price would [card] be **so expensive** that you would not consider it?" → `vw_too_expensive_usd`
2. "At what price would it be **expensive, but you would still consider** it?" → `vw_expensive_usd`
3. "At what price would it be **a bargain**, a great buy for the money?" → `vw_bargain_usd`
4. "At what price would it be **so cheap** that you would doubt its quality?" → `vw_too_cheap_usd`

Record which card was used in `vw_offering` (P/S/M/A/E). Use one card per interview: the primary card for that segment. Use a second card only if more than 10 minutes remain.

**Analysis.** Per segment, plot cumulative curves: "too cheap" and "bargain" reversed, "expensive" and "too expensive" forward. Then read off:
- **PMC** (point of marginal cheapness): "too cheap" crosses "not a bargain".
- **PME** (point of marginal expensiveness): "too expensive" crosses "not expensive".
- **OPP**: "too cheap" crosses "too expensive".
- **IPP**: "bargain" crosses "expensive".
- **Acceptable range** = PMC to PME.

Below n = 8, report the median of each answer instead of curve intersections.

### 4c. Gabor–Granger ladder: one ladder per card, randomised start
"If [card] cost **$X**, how likely would you be to buy it for your next [study / year]? 1 = definitely not … 5 = definitely." A score of 4–5 counts as **yes**. Step up after a yes and down after a no. Stop after the first change of answer, or at the end of the ladder.

| Card | Ladder (USD) | Start A / Start B (coin flip) |
|---|---|---|
| P | 1,500 → 2,500 → 3,500 → 5,000 → 7,500 | 2,500 / 5,000 |
| S | 5,000 → 8,000 → 11,000 → 15,000 → 20,000 | 8,000 / 15,000 |
| M | 3,000 → 5,000 → 9,000 → 15,000 → 20,000 | 5,000 / 15,000 |
| A | 2,000 → 4,000 → 6,000 → 10,000 → 15,000 per year | 4,000 / 10,000 |
| E | 20,000 → 30,000 → 45,000 → 75,000 → 100,000 per year | 30,000 / 75,000 |

Each ladder deliberately extends **beyond the hypothesis range on both sides**, so a range that is wrong can be detected. Log `ladder_start_anchor_usd` and `ladder_max_yes_usd` (existing columns) and the card in `gg_offering`.

**Analysis.** Build a demand curve per segment: the share of respondents saying yes at each price. Revenue index = price × share. A price whose revenue index falls within 10% of the maximum is "revenue-equivalent". Compare start-A and start-B groups. A difference of more than one ladder step between them signals anchoring, so weight behavioural evidence (§7) more heavily.

### 4d. Pricing unit and model preference (unchanged card sort)
Use the M1–M8 card sort from `PRICING_EXPERIMENT.md` §2 and record `model_rank_1` and `model_rank_last`. Add one question: "Would you rather buy the analysis as a **service**, or the **software** and run it yourselves?" → `price_unit_preferred` (service / software / both / neither).

### 4e. Reference-price reaction (only after 4b–4d, only with published figures)
"For context, one academic micro-CT core publishes **$200 per hour** for analysis it performs for corporate clients ([HSS fee page](https://www.hss.edu/research/core-facilities/micro-computed-tomography-core), accessed 2026-11-27). How does that compare with what analysis costs you?" Record the reaction verbatim in `reference_price_reaction` and set `anchor_shown` = `HSS_200h`. Do **not** revise the answers already given in 4b–4c.

## 5. Allowed anchors (verified, published) and disallowed ones
| Allowed | Figure | Source (accessed 2026-11-27) |
|---|---|---|
| HSS micro-CT core: analysis performed by the core | $200/h corporate; $100/h academic non-NIH; $75/h NIH-funded; $25/h self-analysis | https://www.hss.edu/research/core-facilities/micro-computed-tomography-core [V] (no effective date on the page) |
| Beckman Versa 630 instrument time (scanner time only) | $40.00–79.02/h | https://microscopy.beckman.illinois.edu/equipment/fees [V], effective 2021-08-01 |
| Dragonfly academic licence | Free; excludes fee-for-service and industry collaboration | `docs/research/COMPETITOR_INTELLIGENCE.md` [V] |

**Not allowed:** any figure from Scanco, Bruker, Dragonfly commercial, Charles River, Inotiv or any other vendor or CRO that has not been published and fetched with a URL and date. Do not quote "industry averages" or remembered numbers. If a respondent volunteers a competitor's price, record it coded (`[RF]`, no company name in shared files) and never repeat it to another respondent.

## 6. Logging (new columns appended to `interview_log_template.csv`)
`vw_offering`, `gg_offering`, `current_cost_per_study_usd`, `price_unit_preferred`, `anchor_shown`, `reference_price_reaction`, `gg_secondary_offering`, `gg_secondary_max_yes_usd`, `offer_sent_usd`, `offer_outcome` (accepted / negotiated / declined / no response at 14 days), `offer_signed_date`.

Every real offer (§7) is logged with the exact price sent and its outcome. That gives the behavioural record the interview answers alone cannot.

## 7. Decision thresholds
A hypothesis needs **both** the interview signal **and** a behavioural signal to be marked validated. The "cost floor" is 2× the delivery cost measured in the first pilot (model Base estimate: $3.6K per study in 2027 → floor about $7.3K). That rule is inherited from `PRICING_EXPERIMENT.md` §5.

| Hyp. | Interview signal: VALIDATE if… | Behavioural signal: VALIDATE if… | REVISE DOWN / RESTRUCTURE if… | REVISE UP if… | REJECT if… |
|---|---|---|---|---|---|
| H1 Pilot | Median `vw_expensive_usd` (card P) ≥ $2,500 among ≥5 manufacturers and CROs | ≥3 of the first 10 written pilot offers signed at ≥$2,500 | 0 of the first 5 offers signed: consider a free pilot that converts to a paid study, with a credit, only if founder decision #18 allows evaluation on customer data and M0, a DPA and Gate 1 are in place | ≥50% say yes at $5,000 on the ladder | No one shares scans at any price (B-CONF/B-SPONSOR blockers dominate): build a data-free demo |
| H2 Study | Acceptable range (PMC–PME, or medians) overlaps $8–15K for ≥8 manufacturers; ≥40% of decision-makers (DM-YES) say yes at ≥$8K | ≥1 paid study at ≥$8K within 6 months of the first pilot; this is the single gate definition; the earlier one-pager gate "≥3 of 15 buyers at ≥$10K" is retired (`investor/ONE_PAGE_OVERVIEW.md` now cites this row) | Median PME < $8K but > cost floor: price at the revenue-maximising ladder point | Median `vw_bargain_usd` ≥ $12K and ≥40% say yes at $15K | Median PME < cost floor, or ≥50% code P-NONE or C-COMP |
| H3 Characterisation | ≥2 manufacturers code P-GRAFT at severity ≥4 and say yes at ≥$5K | ≥1 paid characterisation | Ladder yes only at $3–5K: limit scope to customer-supplied scans (cost below $2.5K) | ≥40% say yes at $15K | <20% of manufacturers see density overlap as a problem |
| H4 Academic | ≥6 labs/cores; median `vw_expensive_usd` ≥ $4K; ≥3 name a budget line (BUD-GRANT / BUD-RECHARGE) | ≥1 paid licence after an evaluation; ≥2 evaluations started | Median < $4K: core-wide licence with per-scan recharge | Cores say yes at $10K for a core-wide licence | ≥50% say free tools are enough (C-COMP naming Dragonfly academic / BoneJ) |
| H5 Enterprise | ≥2 CROs confirm ≥10 qualifying studies per year **and** say yes at ≥$30K | ≥1 signed enterprise evaluation or licence | Yes only below $30K: sell per-study subcontracting instead | ≥1 says yes at $75K | CROs code C-COMP (in-house deep-learning pipeline), or C-PULL in fewer than 1 of 3 CROs |

**Two gates (changed 2026-11-28, cycle-3 review C3-BIZ-09).** The earlier single "combined gate around 25 Feb 2027" could not be evaluated on that date: the phantom study (M2) is planned for spring 2027 at the earliest, and its protocol is not approved (it still needs the 14 imaging-scientist decisions, the OTM determination and a Beckman agreement).
- **Price gate (around 25 Feb 2027):** does H2 meet its interview signal? If H2 fails but H4 or H5 passes, plan to lead with licences.
- **Separability gate (after the phantom study read-out; spring 2027 at the earliest, date not set):** does the phantom study show a separable path for at least one commercial material (single scan; day-0 is unproven under granule motion and not offered)?

Proceed with the services-plus-licence plan only if both gates pass. If everything fails, stop selling and keep the project as research and publication.

## 8. After every five interviews
1. Update the per-segment medians and ladder curves in a scratch analysis. Do not edit the model yet.
2. After 15 interviews, replace the Base inputs in `build_financial_model.py` with the measured medians (prices, funnel rates, studies per customer), rerun the script, and record the change and its source interview IDs in the `REVENUE_MODEL.md` changelog.
3. Promote a hypothesis from [HYP] to [V] in `REVENUE_MODEL.md` §7 only when the behavioural signal exists, backed by a signed document.

## 9. Ethics and compliance
- Every written offer is genuine, has a validity date, and states its limits ("research use; no GLP or Part 11 claim").
- No written offer, quote or proposal is sent before M0 (an entity exists to make and honour it; `investor/FUNDING_STRATEGY.md` §3).
- No fabricated scarcity, discounts, testimonials or logos.
- Respondents' price answers are confidential. Store them coded, with no company names in shared files.
- No price discussions with competitors, ever.
- A paid offer can only be signed once a legal entity exists. Incorporation is a founder decision that needs counsel (see the note at the top of `investor/FUNDING_STRATEGY.md`).
