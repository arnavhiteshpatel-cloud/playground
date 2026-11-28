# Pricing Experiment Design: DefectFill Report

> **Update 2026-11-27:** the price hypotheses are now: paid pilot $2.5–5K, non-GLP study analysis $8–15K, material characterisation $5–15K, academic desktop licence $4–10K/yr, enterprise desktop licence $30–75K/yr. No GLP-study price is tested until a validation report exists. The question scripts, ladders, logging fields and decision thresholds in `PRICING_VALIDATION_PLAN.md` replace §3 Phase 1 and §5 below where they differ. The cost-to-serve floor in §4 is now estimated in `REVENUE_MODEL.md` §2 (compute ≈ $0 because the product runs locally). The playbook anchors below are kept for history.

**Every price in this document is a hypothesis [HYP].** None has been validated with a customer. The founder-playbook anchors (~$12K per non-GLP study, ~$25K per GLP study, ~$4K/yr academic licence, ~$40K/yr CRO licence) are starting points to test. They are not targets.

## 1. Questions to answer
1. Which **pricing unit** matches how each segment budgets: scan, study, year, or seat?
2. What is the **acceptable price range** per segment, and does it sit above the cost to serve?
3. Do buyers need GLP-related work at all (a need question only; GLP work is not offered and is not priced)?
4. Do CROs prefer to **resell or white-label** (enterprise licence) or to **subcontract** (per-study service)?
5. Does a **vendor partnership** or **algorithm licence** offer a faster route to revenue than direct sales?

## 2. Models to compare (card set for interviews)
| # | Model | Unit | Hypothesis anchor [HYP] | Likely fit [INF] | Main risk |
|---|---|---|---|---|---|
| M1 | Per-scan | Each analysed scan | $150–$600/scan | Academic labs, ad-hoc users | Hard to recover setup/QC cost on small jobs |
| M2 | Per-study report (non-GLP) | Study (≤40 scans, ≤2 time points) | ~$12K | SME manufacturers | Scope creep (extra ROIs, time points) |
| M3 | **Not offered:** GLP-related study work. Do not show as a priced card; ask only whether the buyer needs GLP work (a need question) | — | — | Manufacturers, CROs running GLP | No validation report, quality system or Quality Agreement exists; no GLP or Part 11 claim can be made |
| M4 | Annual subscription (self-serve software) | Org/year, seat-limited | Academic ~$4K/yr; Industry $15–30K/yr | Cores, labs, high-volume SMEs | Support load; customer validation burden |
| M5 | CRO enterprise licence | CRO/year, unlimited internal studies | ~$40K/yr | Device CROs | Long sales cycle; CRO captures the margin |
| M6 | Full analysis service (OsteoQuant analysts + human review) | Study, priced on time & materials or fixed | $8–20K/study | Sponsors without in-house expertise | Founder-time bound; doesn't scale |
| M7 | Vendor partnership | Revenue share per plug-in seat or bundled licence | 15–30% rev share | Micro-CT vendors' installed base | Dependence on partner; competitor conflict |
| M8 | Algorithm licensing | Up-front + royalty to a vendor/CRO | Up-front $25–100K + royalty | Vendors, large CROs | Needs validated, defensible IP; university IP ownership must be checked first |

## 3. Experiment phases

### Phase 1: interview pricing (n ≥ 15, target 25; weeks 1–8)
- Run the Van Westendorp four questions and a Gabor–Granger ladder inside discovery interviews (`INTERVIEW_GUIDE.md` §10).
- **Randomize the starting anchor** (low $6K vs high $18K) per interview by coin flip, logged in `ladder_start_anchor_usd`. This measures anchoring sensitivity.
- Card-sort M1–M8. Record the top and bottom choice with reasons.
- **Analysis:** Van Westendorp curves per segment (OPP and IPP points, range of acceptable prices). Read them as directional only below about 30 responses per segment. Use the Gabor–Granger demand curve to estimate a revenue-maximizing price.

### Phase 2: proposal-level test with real offers (weeks 6–16)
- Send real written proposals (`templates/QUOTE_TEMPLATE.md`) to prospects who asked for one, built on the same scope.
- **Two-arm framing test:** alternate prospects between framing A (per-study fixed price) and framing B (annual subscription with an included study allowance). Each prospect gets one coherent, genuine offer that OsteoQuant would honour, and can ask about the other model at any time.
- Record: response within 14 days, request to negotiate, requested price change, and conversion to a signed pilot or SOW.
- Because n will be small, decide on qualitative evidence plus raw counts. Do not claim statistical significance.

### Phase 3: pilot-to-paid conversion (weeks 12–26)
- After a free or discounted retrospective pilot (`templates/PILOT_PROPOSAL.md`), make a paid follow-on offer at the price indicated by Phases 1–2.
- **Primary metric:** pilot→paid conversion rate. **Secondary:** discount requested, procurement time, required contract changes.

## 4. Cost-to-serve floor (to fill in; currently [AE])
| Input | Placeholder [AE] | How to measure |
|---|---|---|
| Compute per scan | <$5 | Log cloud/GPU cost during the pilot |
| Human review minutes per scan | 10–30 min | Time-stamp review in the audit trail |
| Study setup and QC hours | 4–10 h | Track in pilot |
| Report assembly and QA sign-off | 2–6 h | Track in pilot |
| GLP overhead (validation upkeep, QA review, archiving) per study | 8–20 h | Estimate with a QA consultant |
| Loaded hourly rate | $75–150/h | Founder decision |

Price floor per study ≈ (setup + review × scans + report + GLP overhead) × rate × (1 + margin). This must be recomputed with pilot data before any price is published.

## 5. Decision rules [HYP]
- Choose **per-study** pricing for manufacturers if ≥60% of MFR interviews budget per study and the Van Westendorp range of acceptable prices includes a price ≥2× the cost-to-serve floor.
- Pursue the **CRO licence** only if ≥2 CROs code C-PULL **and** confirm ≥10 qualifying studies per year [AE threshold].
- Pursue a **vendor partnership or algorithm licence** if interviews show strong installed-base lock-in (≥50% using a single vendor's software) **and** a vendor expresses interest. Get UIUC IP clearance first.
- Drop any model that ≥70% of a segment ranks last.

## 6. Ethics and compliance
- No fake products, no fake scarcity, no fabricated testimonials or customer logos.
- Every quote is a genuine offer with a validity date and clearly stated limits ("research use; not validated for GLP until validation report X is issued").
- Price discussions are with individual prospects only. Never discuss or coordinate pricing with competitors.
