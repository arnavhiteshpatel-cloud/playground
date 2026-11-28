# Cross-Finalist Model Consistency Audit (Stage F, batch F6)

**Scope:** the 11 finalists' Stage E models:
SYN-006, SYN-004, SYN-001, WS05-007, WS04-014, WS18-003, WS18-035, WS13-014, WS16-006, WS12-012, WS12-014.

**Material read:**
- each `08_financial_models/<ID>_assumptions.json` and `_results.json`;
- `MODEL_COMPARISON.md`;
- `tools/fin_engine.py`.

**Reviewer:** independent; I wrote none of these models. **Date:** 2026-11-28.

**Reproducibility:**
- Code: `07_review/cross_model_audit.py`, a copy of `/tmp/claude-0/atlas_scratch/F6/cross_model_audit.py`.
- Run with `python3 07_review/cross_model_audit.py /home/user/playground/project-atlas <out_dir>`.
- It calls `fin_engine.run(a, "base", overrides)` only. **No model file was written.** md5 sums of all 26 assumption files are identical before and after.
- Outputs: `cross_model_audit_results.json`, `_table.md` and `_sensitivity.md/.json`, in `/tmp/claude-0/atlas_scratch/F6/`.

**Limits of the audit:**
- It harmonizes the **base** scenario only.
- It does **not** fold in the model-specific corrections of the other F-batch reviewers (for example, F1's SYN-006 re-run at ARPC $950 gives Y3 $50k / Y5 $83k, and F1 rates WS16-006 "fails"). Those corrections are additional to the harmonization.
- Every harmonization rule is itself mostly E/D-level. Rankings are inputs to judgment, not the decision.

---

## 1. Were the standardization rules followed? (a)

| Rule | Result |
|---|---|
| Owner draw $4,000/month from month 13, all scenarios | **Followed in all 11.** |
| Tax 30% | **Followed in all 11.** |
| Start capital injection = base peak funding (smallest injection keeping base cash ≥ 0) | **Followed in all 11.** Each injection is within $1k of the base peak with draw: SYN-006 $10.0k, SYN-004 $63k, SYN-001 $70k, WS05-007 $47.3k, WS04-014 $42.5k, WS18-003 $142.3k, WS18-035 $93.5k, WS13-014 $52k, WS16-006 $39.2k, WS12-012 $24k, WS12-014 $12.9k. |
| Long-term drivers carry evidence/source fields | **Mostly followed.** Growth, decay, incremental ROIC, maintenance capex, reserve and EV multiple carry `__evidence`/`__source` in all 11. `owner_comp_growth_pct` is unsourced in 9 of 11 (it falls back to the 3% engine default; immaterial). |
| Long-term drivers "evidenced" | **Formally yes, substantively weak.** Of the 66 long-term fields (growth, decay, ROIC, maintenance capex, reserve, EV × 11), 54 are E, D or D/E, 9 are mixed with an E component, and only 3 are clean C/B. The few C/B anchors are incumbents' organic growth (Rollins, staffing, promo, 1-800-GOT-JUNK). Those are then used *above* their own anchor (see §2). |

---

## 2. Are comparable drivers calibrated consistently? (b)

| Driver | What the models do | Inconsistency |
|---|---|---|
| **Founder qualified conversations / month** (recurring models) | SYN-004 10, SYN-006 12, WS04-014 12, WS12-012 12, WS12-014 9, SYN-001 20, WS13-014 22, WS16-006 30, WS05-007 45. All **E**. | No common anchor. A full-time SDR's 2025 median quota is **10 meetings held per month** [D, F6-S004], and these founders also deliver the service. Four models exceed 1.5× that. |
| **Conversation → customer conversion** | 7 of 9 recurring models sit at 0.0875–0.105. Four (SYN-001, WS05-007, WS16-006, WS12-012) use exactly **0.40 × 0.25 = 0.10, the engine's TEMPLATE DEFAULTS** (`fin_engine.DRIVERS`). WS13-014 uses 0.175; WS12-014 uses 0.06. | The modal value is a template default labelled E, not evidence. WS13-014's is 1.75× the template. |
| **Founder ramp** | 6 months in 7 of 9; WS05-007 4; WS12-014 12. | WS05-007 is the outlier. |
| **Monthly churn** (recurring) | 1.0% (WS04-014), 1.2% (SYN-004), 1.5–1.8% (SYN-006, SYN-001, WS05-007), 2.5–5% (WS16-006, WS12-012, WS13-014, WS12-014). | Two newcomers are modelled as out-retaining incumbents: Paychex 82–83%/yr [A, WS02-S022]; Rentokil NA 80.7%/yr [B, C2-S009]; independent agencies 84% [C, E-SYN001-S012]. |
| **Referral/inbound per 100 active per month** | 0.5–1.0 in six recurring models; SYN-006 1.5; WS12-014 2.0. All E. | WS12-014's referral stream supplies ~28% of its year-5 new clients (4.1 of 14.8) on E evidence. |
| **Revenue-per-customer growth** | 3% in 7 models; SYN-004 0%; **SYN-001 9%** ("attach maturation", E); **WS12-012 8%** ("seat expansion", E). | WS12-012's seat expansion adds seats without adding the supervision staff that are triggered by account count, which is internally inconsistent. |
| **Job-model volume calibration** | WS18-003 calibrates plateau revenue to ~1.25× Junk King's median. WS18-035 calibrates to Access's year-3 *average* (a 7-unit system, average age 1.9 years) and to Precision's median earned at **2.1× the model's ticket**. | WS18-035's 133 jobs/month is ~2.3× what franchise medians imply in jobs (~59/month). See `WS18-035_review.md` §2. |
| **Founder unpaid delivery labour** | In **10 of 11** models, operating profit includes the founder personally doing a priced delivery role ($4.8–6.9k/month at the models' own staff costs). Only **WS18-003** puts a manager on payroll who replaces it. | The largest hidden inconsistency. Capacity-triggered models show *higher* profit when demand is *lower*, because hires are deferred: WS18-035 +70% Y5, WS04-014 +11%, SYN-004 +15% under the skeptic set. That is founder wage, not business economics. |
| **CAC per new customer** | $65–105 per job (job models; B/D); $120–500 per account (recurring; all E). None includes founder selling time. | Consistent treatment (founder time is excluded everywhere). Not harmonized. |
| **Staff loaded costs** | Loads of ×1.15 (WS18-003 manager), ×1.2 (SYN-006, CSRs), ×1.25 (most technicians), ×1.3 (WS04-014). Wage bases are mostly cited BLS/O\*NET medians [C]. | Small. Spreads are <8% of staff cost, so not harmonized. Vehicle costs sit sometimes in staff and sometimes in overhead; the totals look consistent. |
| **Insurance / overhead** | Professional E&O+cyber $175–550/month; vehicle trades $320 (WS05-007, GL+auto+pollution) to $2,500 (WS18-003). | WS05-007's $320 for GL + commercial auto + pollution, and WS16-006's $90 GL + product liability (E, no quote), look light. Neither changes a ranking: the "+50% overhead" stresses in MODEL_COMPARISON already show the effect. |
| **EV multiple** (base, on SDE-basis operating profit) | 2.0 (WS18-003, WS12-014), 2.5 (SYN-006, SYN-004, WS18-035, WS16-006), 3.0 (WS05-007, WS13-014, WS12-012), 3.5 (SYN-001, WS04-014). | The **same** BizBuySell sold-comps median of 2.38× SDE [D, E-WS05007-S007] underpins 2.0× (WS12-014), 3.0× (WS05-007, WS12-012) and nothing else. The DF-S004 *asking* 3.2× underpins 2.5× and 3.0×. EBITDA multiples (insurance agencies, MSPs) are applied to profit *before* owner pay in SYN-001 and WS04-014. |
| **Long-term growth / incremental ROIC** | Year-6 growth 8–10% in 6 models (SYN-006, SYN-001, WS05-007, WS04-014, WS13-014, WS16-006); 4–6% in 5. Incremental pre-tax ROIC 100% in 4 models; 30–80% in the rest. | Year-6 growth of 8% exceeds the cited incumbent anchors (Rollins residential 5.0% [A]; staffing +2.4% [C]; promo +1.3–4.2% [C]) for founder-led single-metro firms. |

---

## 3. Harmonized "skeptic" driver set — exact rules (c)

These are applied as `overrides` to each model's **base** scenario. A rule changes a driver only when the model is *more favourable* than the rule; nothing is made more optimistic.

| Rule | Applies to | Exact override | Anchor (level) |
|---|---|---|---|
| **H1** | recurring models | `founder_leads_per_month = min(model, 15)` | 1.5× the Bridge Group 2025 median full-time SDR quota of 10 meetings held/month [D, F6-S004]; the founder also delivers (E) |
| **H2** | recurring models | if `lead_to_proposal × proposal_to_win > 0.08`, set `proposal_to_win = 0.08 / lead_to_proposal` | The template default 0.10 is unevidenced; an unknown entrant in a displacement sale gets less (E) |
| **H3** | recurring models | `founder_ramp_months = max(model, 6)` | Modal value across models |
| **H4** | recurring models | `monthly_churn_pct = max(model, 0.015)` | Incumbent retention ~82–84%/yr [A/B/C as above]; a newcomer should not out-retain incumbents |
| **H5** | recurring models | `referral_new_per_100_active = min(model, 1.0)` | Modal value; all E |
| **H6** | recurring models | `rep_new_customers_per_month = min(model, harmonized founder new customers/month)` | A hire works the same funnel without founder credibility (E). *Non-binding in the harmonized runs, because no rep is hired before year 5.* |
| **H7** | job models (churn = 100%) | Set `founder_leads_per_month` so that plateau jobs/month = **franchise all-unit median volume**: leads = J × (1 − referral/100) ÷ (lead_to_proposal × proposal_to_win). **WS18-035:** J = 58.9, the median of {Access median $389,856 ÷ $575; ProLift middle-50% $424,136 ÷ $575; Precision smallest-band median $857,807 ÷ $1,213} [B, DF-S001, DF-S002, C8-S019]. **WS18-003:** J = $436k ÷ $389 ÷ 12 = 93.4 (Junk King median) [B, WS18-S001], with zone-2 output (`rep_new_customers_per_month`) scaled by the same ratio. | An unbranded independent with no call centre should not exceed the median franchise unit. Disagreeing figure kept: Precision CY2024 → ~166 jobs/month [B, C8-S020]. |
| **H8** | all | `lt_growth_y6_pct = min(model, 0.05)`; `lt_growth_decay = min(model, 0.85)`; `incremental_roic_pct = min(model, 0.60)`; `maint_capex_pct_op = max(model, 0.03)`; `ev_multiple = min(model, 3.0)` (sensitivity at 2.38) | Growth: incumbents' organic growth [A/C]. EV: operating profit is SDE-basis; BizBuySell sold service median 2.38× SDE [D, E-WS05007-S007]. ROIC: E. |
| **H9** | all | `arpc_annual_growth_pct = min(model, 0.03)` | Inflation pass-through. The excess in SYN-001/WS12-012 is E. |

**Metric added (not a driver): Founder-Delivery Charge (FDC).**
- FDC = 12 × the base monthly loaded cost of the delivery role the founder personally performs in that model (read from the model's own staff notes) × 1.03^(year−1).
- It is charged in a year unless the model has a manager on payroll who takes over that role. This applies only to WS18-003's operations manager, who is hired by year 3.
- The roles and costs charged: SYN-006 bookkeeper $5,800; SYN-004 analyst $6,000; SYN-001 coordinator $5,350; WS05-007 technician $5,700; WS04-014 technician $6,500; WS18-003 founder-on-truck $6,500; WS18-035 technician $6,800; WS13-014 technician $6,800; WS16-006 coordinator $4,800; WS12-012 account manager $6,000; WS12-014 recruiter $6,900.
- "Y5 op after FDC" approximates what the business earns if the founder only owns, sells and manages. That is the mandate's "not capped by the founder's hours" test.

**Composite ordering rule:**
- Mean of four ranks: Y5 op after FDC (higher is better), Y3 op after FDC (higher), 10-yr cumulative deployable (higher), and peak funding without draw (lower).
- Ties are broken by Y5 op after FDC.

---

## 4. Harmonized comparison (d)

All figures are base scenario. "Peak funding no draw" uses `founder_draw_per_month = 0`. 10-yr deployable is computed with the standard draw (engine `lt_y10_cum_deployable`).

| ID | Y3 op orig → harm | Y5 op orig → harm | Peak funding, no draw, orig → harm | 10-yr deployable orig → harm | Y5 op after FDC orig → harm | **Composite rank orig → harm** |
|---|---|---|---|---|---|---|
| **WS12-014** recruiting desk | $170k → $163k | $259k → $178k | $13k → $13k | $1.02M → $665k | $166k → $84k | **1 → 1** |
| **WS12-012** PH accounting staff | $54k → $83k | $373k → $168k | $24k → $25k | $1.26M → $380k | $292k → $87k | **3 → 2** |
| **SYN-006** construction back office | $95k → $151k* | $181k → $105k | $10k → $11k | $578k → $251k | $103k → $26k | **2 → 3** |
| **SYN-004** energy cost mgmt | $98k → $81k | $120k → $138k* | $32k → $33k | $315k → $387k | $39k → $57k | **8 → 4** |
| **WS04-014** dental/vet MSP | $64k → $39k | $129k → $143k* | $22k → $23k | $387k → $406k | $41k → $55k | **7 → 5** |
| **WS16-006** workwear | $78k → $46k | $141k → $56k | $18k → $16k | $248k → $5k | $77k → −$8k | **5 → 6** |
| **WS18-035** garage door | $66k → $91k* | $67k → $114k* | $43k → $54k | $9k → $249k* | −$25k → $22k | **11 → 7** |
| **SYN-001** carrier compliance hub | $48k → $38k | $178k → $48k | $37k → $46k | $534k → $0 | $105k → −$24k | **4 → 8** |
| **WS13-014** utility locating/GPR | $106k → $73k | $175k → $60k | $49k → $55k | $418k → $18k | $83k → −$32k | **6 → 9** |
| **WS18-003** junk removal | $49k → $42k | $83k → $34k | $90k → $88k | $31k → $0 | $83k → $34k | **10 → 10** |
| **WS05-007** commercial pest | $62k → −$2k | $101k → $23k | $24k → $47k | $177k → $0 | $24k → −$54k | **9 → 11** |

\* *Rises under the skeptic set because lower demand defers capacity-triggered hires, so the founder does more of the work unpaid.* Read these rows in the "after FDC" column.

**Peak funding *with* the $4k draw, harmonized.** It exceeds the $100k conditional backing for:
- SYN-001: $139k;
- WS18-003: $204k;
- WS05-007: $206k;
- WS18-035: $77k (harmonized); $110k under the reviewer's model-specific drivers.

**Y10 EV harmonized** (at 2.38× in brackets):
- WS12-012 $606k ($480k); WS04-014 $515k ($408k); WS12-014 $426k ($426k); SYN-004 $413k ($393k); WS18-035 $342k ($326k);
- SYN-006 $314k; WS13-014 $215k; SYN-001 $174k; WS16-006 $169k; WS05-007 $84k; WS18-003 $79k.

### How much each model is optimistic relative to the common norms (base Y5 op and 10-yr deployable, original → harmonized)

| Model | Y5 op change | 10-yr deployable change | Rules that bite (single-rule Y5 op, from $ base) |
|---|---|---|---|
| SYN-001 | **−73%** | −100% | H1 → $95k, H2 → $99k, H9 → $91k (from $178k); jointly $48k. A steep J-curve that depends on the volume, conversion and ARPC-growth assumptions together |
| WS05-007 | **−77%** | −100% | H1 (45 → 15 conversations) → $38k alone. H3 is minor. |
| WS13-014 | **−66%** | −96% | H1 → $115k, H2 (0.175 → 0.08) → $162k; jointly $60k. Its conversion is the highest of any recurring model. |
| WS16-006 | **−60%** | −98% | H1 (30 → 15) → $51k alone |
| WS18-003 | −59% | −100% | H7: 106 → 93 jobs/month, plus zone 2 scaled |
| WS12-012 | **−55%** | −70% | H2 → $290k, H9 (8% → 3%) → $274k; jointly $168k |
| SYN-006 | −42% | −57% | H2 → $127k, H5 → $155k |
| WS12-014 | −31% | −35% | H5 (2.0 → 1.0 referrals) → $178k; nothing else binds |
| SYN-004 | +15% (Y3 −17%) | +23% | Fewer customers defer the analyst hire (FDC-adjusted +$18k) |
| WS04-014 | +11% (Y3 −39%) | +5% | Churn floor and conversion lower Y3; the deferred senior-engineer hire lifts Y5 |
| WS18-035 | +70% raw / +$47k after FDC | n/m | H7 removes unprofitable technician hires; the business becomes founder-only |

---

## 5. Which rankings are robust?

**Rule-dropping sensitivity.** Each harmonization rule was relaxed one at a time and the composite rank recomputed (from `cross_model_audit_sensitivity.md`):

| Variant | SYN-006 | SYN-004 | SYN-001 | WS05-007 | WS04-014 | WS18-003 | WS18-035 | WS13-014 | WS16-006 | WS12-012 | WS12-014 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Harmonized (all rules) | 3 | 4 | 8 | 11 | 5 | 10 | 7 | 9 | 6 | 2 | 1 |
| Drop H1 (no conversation cap) | 3 | 4 | 11 | 9 | 6 | 10 | 8 | **5** | 7 | 2 | 1 |
| Drop H2 (template 10% kept) | 2 | 4 | 9 | 11 | 5 | 10 | 7 | 6 | 8 | 3 | 1 |
| Drop H5 (referrals uncapped) | 2 | 4 | 8 | 11 | 5 | 10 | 7 | 9 | 6 | 3 | 1 |
| Drop H7 (job volumes kept) | 3 | 4 | 10 | 11 | 5 | 7 | 8 | 9 | 6 | 2 | 1 |
| Original (no rules) | 2 | 8 | 4 | 9 | 7 | 10 | 11 | 6 | 5 | 3 | 1 |

**Robust:**
- **WS12-014 is #1 in every variant**, including the original. It is the least affected by harmonization, because its Stage E drivers were already benchmark-capped: conversion 6%, churn 5%, EV 2.0×.
  - Caveat: in Y5 op after FDC it ties WS12-012 ($84k vs $87k).
  - Its Y5 gain depends on H5. Uncapped referrals would double the after-FDC figure.
- **WS12-012 and SYN-006 are #2–3 in every harmonized variant.**
  - WS12-012's lead is much smaller than filed (Y5 $373k → $168k). It has the **worst conservative case of all 11**: Y5 −$50k and peak $456k in MODEL_COMPARISON, with GM −5 pts → Y3 $3k. Its rank is therefore base-case-only.
  - SYN-006's #3 rests partly on a Y3 hiring-step artifact ($151k) and the lowest peak funding. Its Y5 after FDC is only $26k, and the F1 reviewer's corrections lower it further.
- **SYN-004 #4 and WS04-014 #5–6 in every harmonized variant.** Both *rise* versus the original ranking. Their drivers already sit near the norms; only the churn floor and conversion cap bite.
- **WS05-007 is bottom (9–11) in every variant**, and **WS18-003 is 7–10.**
  - WS18-003 is the only model that already pays a manager to replace the founder. Its after-FDC Y5 ($34k) is therefore not inflated, but its capital need (peak $88k without draw, $204k with) is the highest.
- **SYN-001 falls from #4 to #8–11 in every harmonized variant.** It is the model most dependent on stacked optimistic E-drivers.

**Not robust:**
- **WS13-014 moves from #5 to #9 depending only on H1** (22 vs 15 conversations/month). Its ranking is a bet on founder prospecting volume, which nothing in the evidence pins down.
- **WS16-006 (6–8) and WS18-035 (7–8)** sit mid-to-low. Their order relative to each other is not meaningful.
  - WS18-035's harmonized improvement is founder labour (after FDC: $22k).
  - WS16-006's after-FDC Y5 is negative.

**What no ordering shows.** After the founder-delivery charge, **no finalist reaches $100k/yr of harmonized Y5 operating profit.** The best are WS12-012 at $87k, WS12-014 at $84k, SYN-004 at $57k and WS04-014 at $55k. The strongest robust claim is that *two staffing-type models (WS12-014, WS12-012) and two recurring B2B services (SYN-004, WS04-014) are the least sensitive to cross-model optimism*. Calling any of them proven would go beyond the evidence.

---

## 6. The three largest inconsistencies

1. **Founder pipeline and conversion are uncalibrated and unequal.**
   - Volumes range from 9 to 45 qualified conversations/month with no common anchor (a full-time SDR's median quota is 10 meetings held [D, F6-S004]).
   - Conversion clusters at the engine template default (0.40 × 0.25 = 10%; four models use it exactly), labelled E.
   - Capping volume at 15 and conversion at 8% cuts Y5 operating profit by 55–77% for SYN-001, WS05-007, WS13-014, WS16-006 and WS12-012.
2. **Unpaid founder delivery labour is embedded unequally.**
   - In 10 of 11 models, operating profit includes the founder doing a $4.8–6.9k/month delivery job. Capacity-triggered hiring then makes *lower* demand look *more* profitable (WS18-035, SYN-004, WS04-014, SYN-006 Y3).
   - Raw operating-profit rankings therefore reward founder labour. After the charge, WS18-035's filed base Y5 is −$25k, and no finalist clears $100k harmonized.
3. **Growth and valuation drivers sit above their own anchors.**
   - Year-6 growth of 8–10% (6 models) and incremental ROIC of 100% (4 models) exceed the cited incumbent organic growth.
   - Revenue-per-customer growth of 8–9% is E (WS12-012, SYN-001).
   - The same 2.38× sold-comps source supports EV multiples from 2.0× to 3.0×, and EBITDA multiples are applied to pre-owner-pay profit (3.5× in SYN-001, WS04-014).
   - Harmonizing these alone takes 10-yr deployable to ~zero for SYN-001, WS05-007, WS13-014, WS16-006 and WS18-003.

Job-model volume calibration (WS18-035 at ~2.3× the franchise-median job count) is a close fourth. It is documented in `WS18-035_review.md`.

---

## 7. Recommendations to the synthesis stage

- Report **Y5 op after the founder-delivery charge** alongside raw operating profit for every finalist.
- Replace template-default funnel drivers with a stated common prior before ranking.
- Rank finalists by the harmonized composite as **one** input, and treat WS13-014's and WS16-006's positions as unresolved until founder-volume tests (V-tests in their playbooks) run.
- Do not use any model's 10-year deployable or Y10 EV in prose without the harmonized figure beside it.
