# WS14-008 — UNFI/KeHE + Walmart deduction recovery for Midwest emerging food & beverage brands: Stage D deep dive (batch DG)

> **Verdict: DROP.** Evidence level **D**. Researched 2026-11-28.
>
> **The pain is real.** Vendor and trade sources put deductions at:
> - **1–5% of revenue** [D, DG-S053; C9-S009];
> - **3–8% of gross sales**, with **65–80% of shortage claims invalid** (RVCF data cited by a recovery firm) [D, DG-S052].
>
> **Why it is dropped: the done-for-you service is already being given away or bundled for exactly this segment.**
> - **Clairelist** advertises UNFI deduction recovery for small food and beverage brands at **$0, "no fees, no contract"**. It claims 68% of disputes won and 41 days to repayment [D, DG-S050].
> - **SPS Commerce**, the EDI network most suppliers already use, leads with a free audit and sells either a flat fee per retailer or a take rate [D, C9-S010, DG-S054].
> - **Glimpse** runs a "first 3 months free" guarantee aimed at **$1–30M** brands on Walmart/KeHE/UNFI [D, DG-S056].
> - **Contingency firms** Upstream Chargeback Solutions and Threecolts publish **no fee percentage** [D, DG-S051/S055]. Neither does anyone else.
>
> **Small-brand economics are thin.** A $3M UNFI-only brand yields ~$115/month of contribution at a 20% fee (E arithmetic).
>
> **Model results:**
>
> | Case | Year-3 operating profit | What it requires |
> |---|---|---|
> | Base | **$149k** | Winning ~1 brand/month at a 20% fee against free alternatives (E) |
> | Conservative | **$4k** | |
> | Optimistic | $1.1M | A ceiling with no evidence behind it |

## 1. Specific initial niche (as tested)
**Contingency recovery of invalid UNFI and KeHE deductions (shortages, duplicate deductions, promo/MCB, pricing, spoilage), plus Walmart compliance/OTIF and shortage claims.**

- **Customers:** $3–30M food and beverage brands headquartered in Illinois and the Midwest.
- **Fee:** 20% of cash or credit actually received, plus a one-time retroactive "backlog sweep."
- **No portal passwords:** brands export remittance and deduction files themselves, as Clairelist does [D, DG-S050]. That avoids portal terms-of-service risk.

## 2. Named operators
| Operator | What is known |
|---|---|
| **SPS Commerce Revenue Recovery** | Covers Walmart, Amazon, Kroger, Target, UNFI, KeHE and others; free audit; "$2B+" recovered [D, C9-S010]. Calculator: deduction fees 1–5%, recovery "up to 99%"; pricing is a flat fee per retailer or a take rate [D, DG-S054]. Lookbacks: pricing/inventory shortages up to 5 years, chargebacks 1–2 years [D, DG-S053]. |
| **Clairelist** (Lacamas Studio LLC, Spokane WA) | UNFI only; $0; $1.2M recovered; 68% of disputes won; 41 days to repayment; works the 12-month UNFI window [D, DG-S050]. Funding model undisclosed; client names unverifiable. |
| **Glimpse** | Software plus recovery for CPG; guarantee for $1–30M brands; pricing unpublished [D, DG-S056]. A case study cites a 1.1-point gross-margin gain at a bakery brand. |
| **Upstream Chargeback Solutions (UCS)** | Founded 2023; contingency-only; no licence fee, retainer or minimum; Walmart OTIF, Target, Kroger MCB, Amazon Vendor Central [D, DG-S051]. Publishes thought leadership via RVCF [D, DG-S052]. |
| **Threecolts Margin Pro** | Walmart vendor recovery; free audit; performance fee (% unpublished); 150+ Walmart codes; first recovery within 4 weeks; "$360M+" recovered [D, DG-S055]. |
| **Carbon6 (ChargeGuard)** | Amazon 1P chargebacks and shortages; fee on recovered amounts [D, DG-S058]. |
| **Confido** | AI deduction management; claims 30–60% of deductions are invalid and 50–70% win rates on documented shortages [D, C9-S009]. |
| **Getida** (adjacent: Amazon FBA) | The only published fee found: performance pricing "starting at 20%" [B, DG-S057]. |
| **PRGX** (retailer side) | Generates post-audit claims against suppliers [D, WS14-S026]. These arrive 18–24 months after the transaction [D, DG-S052]. |

## 3. Suppliers / partners (`09_databases/suppliers/WS14-008_suppliers.csv`)
| Party | Role | Status |
|---|---|---|
| UNFI supplier portal, KeHE portal | Data sources. Third-party access rules MISSING. | Assumed |
| Walmart Retail Link | Data source | Assumed |
| SPS Commerce | ASN/EDI proof data and the main competitor | Documented (D) |
| RVCF | Benchmarks and education; membership cost MISSING | Assumed |
| UCS, Glimpse, Clairelist, Threecolts, Carbon6 | Potential subcontract or referral counterparties. Nobody publishes partner terms. | Documented existence; terms assumed |

**Dispute windows conflict:**
- UNFI: **12 months** per Clairelist [D, DG-S050] vs **~30–60 days** per the Stage C source [D, C9-S011].
- KeHE: ~180 days, with an 8% MCB fee (min $65 per DC) [D, C9-S011].
- Big-box: 30–90 days [D, DG-S052].

## 4. Named prospective customers (`09_databases/prospects/WS14-008_prospects.csv`, 25 brands)
| Group | Brands |
|---|---|
| **Chicago (12)** | Lil' Gourmets (Walmart 1,300 stores, then ~300 Whole Foods) [D, DG-S059]; Amylu Foods (Target; PODs 87.5k → 130k projected) [D, DG-S063]; EM Delish (Meijer Chicago from Sep 2026) [D, DG-S062]; Every Body Eat [D, DG-S064]; Vosges Haut-Chocolat; Metropolis Coffee; Dark Matter Coffee; Eli's Cheesecake; Kitchfix; Upton's Naturals; Pretty Cool Ice Cream; Co-op Sauce |
| **Midwest (13)** | Lillie's Q (Leawood KS); Peace Coffee, Bare Honey, Flackers (Minneapolis); Purple Door (Milwaukee); Sassy Cow (Columbus WI); Wonderstate Coffee (Viroqua WI); Jeni's (Columbus OH); Graeter's (Cincinnati); Kalona SuperNatural (IA); Hungry Planet (St. Louis); Great Lakes Potato Chip Co. (MI); Bobak's (Chicago, established) |

- **HQ cities:** verified from Shopify storefront metadata or the brands' own pages [D, DG-S061].
- **Excluded after checking:** Lexington Bakes (Los Angeles), Laoban (DC), Chomps (Naples FL) and Mighty Spark (HQ not stated).
- **Distributor relationships (UNFI/KeHE) are MISSING for every brand.** Store locators are JavaScript-rendered. This is the biggest qualification gap; it is noted in each row.

## 5. Representative transactions
| Transaction | Revenue | Direct costs | Contribution | Cash timing |
|---|---|---|---|---|
| Ongoing month, $8M brand | $840 (= 20% × $4.2k/month recovered) [E; inputs D] | Analyst ~6 h $180; AI/OCR $30; processing $25 | **$605** | Paid after UNFI repays (~41 days [D]), then net-30 |
| Backlog sweep at onboarding | $5,000 [E] | Analyst ~40 h $1,200; 3PL POD retrieval $150; AI/OCR $50 | **$3,600** | 1.5–3 months |
| $3M UNFI-only brand, monthly | $260 | Analyst 4 h $120; AI/processing $25 | **$115** | Same — not serviceable by hand |
| Walmart OTIF fine reversed ($3k) | $600 | Analyst 3 h $90; carrier/ASN pull $30 | **$480** | Walmart claim cycle |

## 6. Customer acquisition (as it would have to work)
- **Customer #1:**
  - A free retro review of a Chicago brand's UNFI/KeHE export; convert to 20% contingency.
  - Problem: the brand can get the same review free from SPS or Clairelist.
- **Customers #2–10:** brokers, 3PLs and fractional CFOs serving Midwest brands; Chicago food-founder communities.
- **Customers #11–100:** an account executive once revenue passes $30k/month; national natural-channel brands.
- **Funnel (base, E):**
  - 12 conversations/month → 35% share data → 20% sign = **0.84 brands/month**.
  - 3% monthly churn; 21 active brands by year 3.
  - Conservative: 8 × 30% × 12%.
- **Unit economics:**
  - CAC ≈ $300 plus $500/month marketing.
  - LTV ≈ 33 months × $605 + $3.6k ≈ $23k.
  - Brands under $5M are not worth acquiring at a 20% fee.

## 7. Pricing strategy and market evidence
- **No contingency rate is published** by SPS, Threecolts, UCS, Glimpse or Carbon6 [D].
- **The only anchors:**
  - FBA reimbursement "starting at 20%" [B, DG-S057];
  - a $0 UNFI service [D, DG-S050];
  - flat-fee-per-retailer options at SPS [D, DG-S054].
- **Realistic structure if pursued:**
  - 15–25% of cash received; backlog at 25%; no retainer.
  - Or a $300–500/month flat fee for brands at $10–30M.
- **Pricing power:** low.

### 7b. Which retailer and distributor deduction regimes are hardest (evidence-ranked)
| Rank | Retailer / distributor | Why |
|---|---|---|
| 1 (hardest) | **Walmart** | "Fully automated enforcement"; OTIF, SQEP and Perfect Order programmes "actively enforced"; 30–90-day windows [D, DG-S052]. More than 150 deduction codes across six categories [D, DG-S055]. Specialist vendors (Threecolts, UCS, SPS) all lead with Walmart, a sign of both difficulty and competition. |
| 2 | **Amazon Vendor Central** | High-volume shortage and accrual claims. SPS says 98% of the cases it identified were "confirmed by Amazon as disputable" [D, DG-S053]. A separate tool category (Carbon6) exists for it [D, DG-S058]. |
| 3 | **UNFI** | Short or uncertain window (30–60 days in one source vs 12 months in another [D, C9-S011, DG-S050]) and idiosyncratic codes. The segment where a free service now operates. |
| 4 | **KeHE** | Longer ~180-day window, but MCB fees of 8% (min $65 per DC) [D, C9-S011]. |
| Cross-cutting | **Retailer post-audit claims** (PRGX-type) | Arrive 18–24 months later, when documentation is cold [D, DG-S052]. Arguably the most defensible niche for a human service, but it serves larger suppliers than the emerging-brand target. |

Difficulty does not translate into opportunity here. The hardest regimes (Walmart, Amazon) are where funded specialists and SPS concentrate. The easier natural-channel regimes (UNFI/KeHE) are where the dollar value per small brand is lowest and a $0 competitor exists.

## 8. Working capital and cash conversion
Revenue arrives only after retailers repay: work → dispute → repayment (~41 days [D]) → invoice → net-30. That is ~70 days from labour to cash, while analysts are paid semi-monthly.

| Brands | Receivables (fee AR) | Analyst float |
|---|---|---|
| 10 | ≈ $8–14k | ≈ $5–10k |
| 50 | ≈ $42k | ≈ $25k |
| 200 | ≈ $170k | ≈ $130k (13 analysts × 2 months) |

Base model peak funding is only $7.6k, because backlog fees arrive early. The conservative case reaches $194k with founder draws, because it never covers them.

## 9. Regulatory path
1. **Illinois LLC and EIN.** No licence found. This is not consumer debt collection: the brand is disputing its own receivables.
2. **Engagement letter:** define the fee base (cash versus credit memo), claim ownership and data use. Sign an NDA/DPA.
3. **Portal access:** use brand-run exports rather than shared credentials. UNFI/KeHE/Walmart third-party terms of service are MISSING.
4. **Insurance:** E&O and cyber ≈ $2–4k/yr. No quotes; E.

## 10. Operations workflow
1. The brand exports deduction and remittance files.
2. AI classification by code (shortage, promo/MCB, pricing, duplicate, spoilage).
3. Evidence matching: POD/BOL from the 3PL, ASN from EDI, promo agreements.
4. Dispute packets assembled.
5. The brand approves and files, or files via an authorised user.
6. Repayment matched to remittance.
7. Invoice.

**Human vs automatable:**
- **Human:** 3PL document chasing, escalations, root-cause advice.
- **AI and automation:** classification and packet drafting are highly automatable. That is exactly why software competitors can offer them free or bundled. AI is table stakes, not an edge.

## 11. Competitive position and defensibility
**What would accumulate:**
- code-level knowledge of UNFI/KeHE rules;
- broker/3PL referral relationships;
- a document-retrieval network.

**Against that:**
- SPS already holds the ASN/EDI proof data and the supplier relationship.
- Funded software firms compete in the segment.
- A free entrant shows the marginal price of the core task is near zero.

**No structural opening was found.**

## 12. Key risks and pre-mortem
| Loss level | How it happens | Early warning |
|---|---|---|
| **$5k** | Free reviews are done for 6 brands; none sign because SPS or Clairelist is free | >50% of reviewed brands cite a free alternative |
| **$25k** | Brands sign, but windows have expired (UNFI 30–60-day reading); backlog fees are tiny; an analyst is hired early | Recovered < $10k per brand in 90 days |
| **$50k** | Retailer terms of service bar third parties; brand failures and acquisitions churn the base | Portal access refused; churn >5%/month |

**Stress results (base year-3 operating profit $149k):**

| Stress | Year-3 operating profit |
|---|---|
| Win rate −40% | $84k |
| Recession | $90k |
| Growth twice as slow | $80k |
| Hires 30% sooner | $90k |

## 13. Validation plan (if ever revisited)
1. **Read the UNFI/KeHE/Walmart supplier terms (≈$0).**
   - **Kill:** third-party processing is prohibited.
2. **Three free retro reviews on brand-exported data.**
   - **Success:** ≥$15k recoverable per $5M+ brand, with ≥30% of deductions invalid.
   - **Kill:** <$5k.
3. **Paid conversion.**
   - **Success:** 2 of 3 brands sign 20% contingency despite free alternatives.
   - **Kill:** 0.
4. **Channel test.**
   - **Success:** ≥2 referrals from 5 brokers or fractional CFOs in 60 days.

## 14. Revised scores and verdict
| Criterion | Stage C | Stage D | Note |
|---|---|---|---|
| fcf | 4 | 3 | Base y3 $149k rests on E fee and win rate; conservative $4k |
| roic | 7 | 7 | Little capital |
| access | 5 | 4 | Distributor relationships unverifiable from public data; free alternatives |
| scale | 5 | 4 | Small brands uneconomic; large brands use SPS or in-house staff |
| resilience | 6 | 6 | Deductions persist through cycles |
| entry | 3 | 2 | Free, bundled and funded competitors in the exact segment |
| delegation | 6 | 6 | SOP-friendly analyst work |
| cash | 5 | 5 | ~70-day work-to-cash cycle |
| feasibility | 9 | 9 | No licence |
| ai | 6 | 5 | Automation benefits incumbents equally |

**Verdict: DROP.** It could be revisited only as an add-on service inside a broader CPG back-office business (bookkeeping, trade-spend accounting), where deduction recovery is bundled rather than sold alone.
