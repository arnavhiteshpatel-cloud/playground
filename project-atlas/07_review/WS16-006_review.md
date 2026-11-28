# WS16-006 — Stage F Adversarial Review (batch F1)

**Concept reviewed:** branded workwear, safety-recognition and promotional merchandise distributor for Chicago trade contractors.

**Material reviewed:**
- Stage C memo, Stage D deep dive (verdict there: RESERVE), Stage E playbook and materials;
- `08_financial_models/WS16-006_assumptions.json` and `_results.json`;
- the prospect CSV (30 rows) and the supplier CSV;
- `sources_E_WS16-006.jsonl` and the cited C9, DH and WS16 records.

**Reviewer:** independent; I did not write any of this. **Access date:** 2026-11-28.

**Re-runs:** made with `tools/fin_engine.py` (scripts in `/tmp/claude-0/atlas_scratch/F1/`). The finalist's files were not modified. New sources are F1-S007…S009.

---

## 1. Verdict: **FAILS (as a finalist / first-company candidate)**

**Retain only as a $0–600 desk-and-interview test (V0/V1).**

The Stage E author did careful, honest work, and it shows. The playbook's own item-level desk test finds that a newcomer earns **5–25% gross margin at 4imprint price parity** on decorated apparel, and loses money on ANSI hi-vis. Yet the model's base case still uses **30% recurring / 28% first-order GM**. That figure is an incumbent-industry average, carried into a newcomer model that the same document's evidence contradicts.

**The corrected base uses:**
- GM 27% recurring / 25% first-order: the newcomer reaches roughly +5–10% over parity on a mixed basket, after real distributor net prices;
- churn 3%/month;
- ARPC $600/month;
- DSO 45.

**Corrected results:**

| Case | Year-3 op. profit | Year-5 op. profit | Peak funding (with $4k draw) | Peak funding (no draw) |
|---|---|---|---|---|
| Corrected base | ~$47k | ~$86k | ~$98k | ~$22k |
| Corrected base + 1% bad debt | ~$44k | ~$81k | ~$106k | — |
| Corrected conservative | ~$13k | ~$30k | ~$191k | — |

- In corrected base, retained cash after the draw is negative in each of years 1–4.
- The structural facts are unfavourable:
  - price-transparent products against a $1.35B public competitor that publishes its prices;
  - an AGC-endorsed Cintas program;
  - most buyers already purchasing through e-commerce.
- This is a **good-job business with personal-guaranty and receivables exposure**, not a holding-company seed.
- It deserves revival only if V1 shows Chicago trade contractors already pay ≥1.15× 4imprint for comparable items, which would restore 30% GM. That test costs $0.

---

## 2. Factual errors found

| # | Claim | What the source says | Correction |
|---|---|---|---|
| F1 | Model base GM 30% "C" evidence, "anchored" on 4imprint 31.5% and PPAI 34–36% | 4imprint's H1-2026 GM of 31.5% (32.8% prior) is verified [B, C9-S015]. But it is earned at $666M of half-year revenue with scale purchasing. The playbook's own §3.1 newcomer cost build gives 25% (tee), 5–10% (hoodie), 17% (cap) and −12% (ANSI tee) at parity. | The incumbent figure must not be the newcomer base. **Newcomer GM is E**, with B-level evidence pointing *below* 30% until V1/V2 prove otherwise. Base 27/25, conservative 23/21. |
| F2 | "4imprint keeps about 81% of its orders coming from existing customers … so repeat behaviour is a real feature" | The H1 release (verified) gives total orders of 1,040k and new-customer orders of 202k (−7%). Existing-customer orders are *derived* (838k), not disclosed. | The arithmetic is fine. But order mix ≠ account retention, and it is a scale incumbent with heavy brand marketing. It does not support 2.5%/month churn for a newcomer's accounts (E). |
| F3 | "Construction's hires rate … roughly half the workforce a year [A]. Every hire needs shirts, a hoodie and a cap." | JOLTS 4.2%/month is industry-wide, including residential and seasonal re-hires. | It is A as a statistic but D as a demand driver. Commercial union trades in Chicago draw returning members from halls; re-hires do not need new kits. Per-account kit demand is E. |
| F4 | PPAI "Standard Base $595/yr for firms up to $500K" | Verified price. PPAI's page says size bands are *recommendations*; reported sales no longer determine tier. | Minor. Does not change cost. |
| F5 | Hightech Grafix as the national trade decorator anchor | Prices verified [B, DH-S030]. **The page states no location** (only a "3pm Central" cutoff). | Freight and transit time to Chicago are MISSING (the playbook notes this). Decoration-at-distance adds about 2–5 days and freight on every order; local trade pricing is unverified. |
| F6 | Hoodie comparison (§3.1) uses Gildan 18500 blanks against 4imprint's "Gildan … hoodie left-chest embroidery $22.50 at 48" | E-WS16006-S002's record describes the 4imprint item as a "Gildan 5050 hoodie". I could not confirm the exact style. | Possible apples-to-oranges. If the 4imprint garment is a lighter blank, the hoodie margin gap is overstated. Flagged as unresolved, not as an error against the author. |

Citations that checked out exactly:
- 4imprint ANSI Class 2 tee: $28.75 (12) … $20.95 (72) … $16.25 (576), with a $35 setup and a $35 tape charge under 72 (CornerStone, Type R Class 2).
- 4imprint Gildan tee: $7.25 (72) / $6.25 (144), no setup.
- ShirtSpace CS401: $17.54 (list $21.92).
- Hightech Grafix price points.
- SanMar credit application: Net 30 or card; ASI #; a **"continuing and irrevocable" personal guaranty**; Washington law.
- ASI's 37% claim (marketing; it also says "many distributors launch for just a few thousand dollars").

---

## 3. Unsupported or over-stated claims

| Claim | Warranted level |
|---|---|
| ARPC $650/month (≈$7.8k/yr) per active contractor account | **E, probably high.** Bottom-up for a 40-person sub: kits for about 10–20 genuinely new hires a year (~$1–1.6k), a Safety Week order (~$3k, annual), a seasonal refresh (~$2k). That is about $5–7k *at 100% share of wallet*. Realized share is lower when Cintas or a local shop holds part of the wallet. Base $600, conservative $450. |
| "The wedge is service: size-run management, yard delivery, reorder records" | E. Stage E itself corrected Stage D's claim that 4imprint lacks these. Local embroidery shops (about 190 suburban BBB listings, D) already deliver locally. |
| Recognition-program design (OSHA memo; IRS $400/$1,600 achievement awards) as a differentiator | The sources are A. Commercial value to buyers is E, and the playbook says the client's adviser must confirm. Useful content, not a moat. |
| "Revenue can start within 4–8 weeks" | Plausible (C/E), but only on card-prepaid supplier terms. That pushes supplier cost onto the founder's personal card limits (see §6). |

---

## 4. Financial model audit

**Recomputation.** The base re-runs exactly: year 3 $78,108, year 5 $141,481, peak $39,105 ($17,718 with no draw). The 24-month table reproduces. The engine applies DSO 40 to *all* revenue, partly offsetting the 50% deposit on first orders, which is fair.

**Driver challenges and re-runs (base):**

| Change | Y3 op. profit | Y5 op. profit | Peak (draw) | Evidence |
|---|---|---|---|---|
| Playbook base | $78,108 | $141,481 | $39,105 | — |
| GM 26/24 | $52,056 | $89,243 | $90,087 | §3.1 desk test [B prices / E interpolation] |
| GM 26/24 + churn 3% + DSO 45 + ARPC $550 | $32,757 | $47,032 | $117,679 | E |
| **Corrected base: GM 27/25, churn 3%, DSO 45, ARPC $600** | **$47,301** | **$86,175** | **$98,336** ($22,274 no draw) | E anchored on B |
| … + bad debt 1% | $44,399 | $80,802 | $106,491 | No bad-debt line in the model; contractors are unsecured trade credit |
| … with win rate 20% | $37,048 | $45,541 | $95,957 | E |
| … if V1 proves GM 30/28 | $64,714 | $118,413 | $55,946 | Upside case |
| Corrected conservative: GM 23/21, churn 4%, DSO 55, ARPC $450 | $13,118 | $29,689 | $191,133 | — |
| GM 22/20 on base volume | $11,093 | $9,180 | $222,277 | Parity-pricing case |

**Blended margin after decoration, freight and tariffs.** Using the playbook's own landed-cost table:
- **Basic tees** clear about 25% at parity and about 30% at +7%.
- **Embroidered items** need +18% to +36% over 4imprint to reach 30%.
- **ANSI hi-vis** needs +60%.
- **Card fees, reprints and unrecovered freight** (3.5% of revenue in the model) come off *after* GM. A 27% GM newcomer therefore keeps about 23.5% contribution before labour.

**Tariffs** are additive and live:
- MFN duty of 32% on man-made-fibre knit tees (most hi-vis) [A, E-WS16006-S014];
- Section 301 at 10–12.5% on 60 economies from July 2026 [A, E-WS16006-S012].

The 4imprint margin fell 1.3 points in one half-year on tariff costs. **I would treat 27% as a *ceiling* until real SanMar/S&S net prices are seen.**

**Working capital, guaranty and credit.**
- In corrected base, year-3 AR is about **$82k** owed by construction firms, against roughly $40k a month of supplier cost paid at PO by card or Net 30. Peak funding with draw is about $98k, close to the full conditional $100k.
- SanMar's Net-30 account requires a **continuing, irrevocable personal guaranty** [B, DH-S024 verified]. Business cards will likely need personal guaranties too (unverified).
- Promotional goods carry **no mechanics'-lien protection**, unlike construction services. If a sub fails, the distributor is an unsecured creditor.
- The founder's credit history is unknown (brief), so **feasibility depends on an unknown personal fact**.

**Draw logic.** FCF first covers the draw in year 3 in the playbook base. In corrected base, retained cash is negative in years 1–4 (−$22k, −$23k, −$19k, −$27k). The $4k draw is partly funded by the founder's own capital for four years.

---

## 5. Customer acquisition challenge
- **Where buyers already buy:**
  - ASI's 2024 end-buyer survey (manufacturing, the nearest published sector) found **65% of end-buyers purchase promo through an e-commerce company** [C, F1-S007]. "Save money" (66%) ranks almost level with "save time" (68%) as what they want from a distributor.
  - AGC's national member benefit gives AGC members exclusive Cintas discounts on uniform rental *and direct sale*, with hi-vis and FR options [C, F1-S008].
  - UniFirst sells managed rental to Chicago trades with logo embroidery [C, E-WS16006-S020].
- **The realistic incumbent set** for a Chicago electrical or mechanical sub:
  - a rental program for core uniforms (Cintas/UniFirst);
  - a safety-supply distributor for PPE;
  - a local embroidery shop or 4imprint/Amazon for tees and hoodies;
  - union-local or GC giveaways.
- **The newcomer must displace the local shop or e-commerce** on discretionary items, where the buyer compares unit prices in seconds.
- **The first 10 customers will require:**
  - 150 touches a month to produce 30 qualified conversations, which is aggressive for main-line calls to safety managers (E);
  - free mockups;
  - a sample kit;
  - matching or beating the shop the owner already knows.
- Expect 1.5–2 wins a month in year 1, not about 3 at full pace. That is why the win-rate stress matters.
- **The Safety Week entry offer is the best idea in the plan:** dated, recurring, and bought by a single safety lead. But it is a once-a-year spike.

---

## 6. Supplier/partner accessibility challenge
| Partner | Risk |
|---|---|
| **SanMar / S&S** | Accessible on card terms. Net terms require a personal guaranty and trade references a newcomer does not have. *Distributor net pricing below public e-tailer prices is the single most important unverified number in the plan.* |
| **ASI vs PPAI** | Suppliers "often ask for an ASI number" [C, DH-S023]. If PPAI/SAGE is not accepted, ASI's unpublished fee applies. |
| **Trade decorators** | Hightech Grafix is accessible (trade-only, online), but its location and freight are unknown. Chicago-area trade pricing is documented for only one firm (4Logoz, D). Most local shops sell retail and may decline to price a competitor-distributor at trade rates. |
| **Union-label shop** | Only Minuteman Press Chicago claims a union-printer licence, and garment labelling is unconfirmed (D). For union-shop customers this could be a gating requirement, not a premium feature. |

---

## 7. Legal/regulatory challenge
- **No licence is required (correct).** IDOR REG-1 and resale certificates are correctly identified.
- **Missed or under-weighted:**
  1. **Personal-guaranty and personal-credit dependence** is a G-type feasibility flag, given the founder's unknown credit.
  2. **ANSI/ISEA 107 decoration.** Decorating certified hi-vis can void compliance if logos cover background or retroreflective material. Mis-decorated PPE sold for OSHA-required use is product-liability exposure. Product-liability cover is assumed at $70–125/month with no quote, and needs confirming.
  3. **Sales-tax sourcing** across Chicago and home-rule jurisdictions for delivered goods (flagged MISSING; it needs an accountant).
  4. **Card surcharging** (flagged).
- Nothing in the plan is structurally unlawful.

---

## 8. Competitive response
- **4imprint:** no response needed. It already publishes the price ceiling and runs frequent promotions.
- **Local shops:** will match on price for a known customer. They own equipment and do not pay a contract-decoration margin.
- **Cintas/UniFirst reps:** already in the yard weekly and can add logo items to the route.
- **Underestimated advantages of incumbents:**
  - decorators with their own machines capture the decoration margin the newcomer pays away;
  - rental programs are contracted and route-serviced.
- The playbook's own stress test, "competitor response: −3 pts GM, churn ×1.3", gives year 3 of $48k *from the playbook base*. From my corrected base it would be around $25k (not separately run).

---

## 9. Founder execution and delegation realism
- **Hours.** Until a coordinator joins (at ≥$35k/month revenue, base month 21), the founder does:
  - 15–20 h a week of prospecting;
  - 10–15 h a week of quotes and orders;
  - kitting and yard delivery.
- **Corrected base never reaches $10k/month operating profit within 60 months.**
- **Rep economics are thin.** A rep takes 40–50% of gross profit [D/C, DH-S028/S029]. At a 27% GM, a rep paid 45% of gross profit must sell about $41k a month of their own book just to earn $5k. The firm keeps only about 15% of that rep's sales to cover coordinators, overhead and bad debt. Delegation of selling is therefore weak.
- **Delegation verdict:** order operations are delegable (coordinators); selling stays with the founder (G7 WARN stands).

---

## 10. Pre-mortem
| # | Most plausible failure | Early indicator | Cheapest preventive test |
|---|---|---|---|
| 1 | **Margin.** Contractors' incumbent prices sit at or below 4imprint parity. Realized GM settles at 20–25% and the business works only as a founder job. | V1 median price paid ≤1.05× 4imprint; first-order GM <27% on supplier invoices | **V1 incumbent-invoice benchmark (15 interviews, $0) plus V2 real SanMar/S&S net quotes. Run both before PPAI or samples.** |
| 2 | **Account depth.** Accounts buy once (a Safety Week or kit) and then revert to the local shop or Cintas. ARPC proves $300–450/month and churn 4%+. | <40% reorder within 6 months; second-order value < half the first | V5 reorder check (180 days) **before** any coordinator hire |
| 3 | **Credit and guaranty event.** One or two subs pay late or fail. The founder carries $30–80k of AR against personally guaranteed supplier balances, or a 300-piece misdecorated hi-vis order is reprinted at our cost. | DSO >50; any account >60 days; card balance >2× deposits | 50% deposits on all orders over $1,000; trade-credit checks; written decorator reprint policy (V2) |

---

## 11. Corrected scores
| Criterion | Stage E | **F1** | Reason |
|---|---|---|---|
| fcf | 4 | **3** | Corrected base about $47k (year 3) / $86k (year 5) |
| roic | 7 | **5** | About $22k no-draw peak, but about $98k with draw plus personally guaranteed payables |
| access | 6 | **5** | Buyers are nameable, but entrenched in e-commerce, rental and local-shop habits |
| scale | 5 | **4** | Sales-capped; thin rep economics |
| resilience | 4 | **4** | Discretionary spend in a cyclical customer base |
| entry | 4 | **3** | Price-transparent commodity; the desk test shows no margin at parity |
| delegation | 5 | **5** | Coordinators are delegable; selling is not |
| cash | 6 | **5** | DSO 45 vs card-paid COGS; unsecured contractor AR |
| feasibility | 9 | **8** | Personal guaranty; unknown founder credit |
| ai | 4 | **4** | — |

- **Raw composite:** 4.32. Evidence **C** (k = 0.85) gives an **evidence-adjusted score of 4.42** (Stage E: about 5.2).
- **Gates:**
  - G4: WARN. Corrected base reaches about $86k in year 5; $100k is not reached within 5 years.
  - G7: WARN.

**Bottom line.** The Stage E playbook is unusually honest: it found its own margin problem and said so. The model, however, did not absorb that finding.

At the newcomer margins the playbook's own evidence supports, this is about a **$45–50k year-3 / $80–90k year-5 business**. It needs about $100k of founder-funded draw and receivables at peak, and carries a personal guaranty on supplier credit. It competes against published 4imprint prices, an AGC-endorsed Cintas program and an e-commerce-first buyer base. That fails the mandate's test for a first holding-company asset.

I preserve one disagreement with my own verdict: if V1 finds Chicago trade contractors routinely paying 15–35% above 4imprint, as PPAI/ASI's 34–37% industry margins imply *some* buyers do, the playbook's base (~$65–78k year 3) is restored. The $0 interview test is worth running before discarding it. It should not consume founder months ahead of a stronger finalist.
