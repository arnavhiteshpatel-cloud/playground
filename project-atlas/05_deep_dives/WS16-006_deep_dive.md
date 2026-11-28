# WS16-006 — Promotional products distributor: Stage D commercial deep dive

> **Verdict: RESERVE** (fallback concept; not a finalist)
> - **Revised evidence level:** C. Incumbent margins, published prices, membership and software costs are A–B. Account volume, win rates and churn are E.
> - **Model base case, year 3:** revenue $720k, operating profit **$44k** (before founder pay).
>   - The figure includes an outside rep hired in month 25. Without the rep, year 3 is $91k.
>   - Year 5 is $165k ($200k without the rep).
>   - Conservative case: −$38k. Optimistic case: $309k.
> - **Decisive fact:** gross margin is the swing factor. At the margin 4imprint actually earns (31.5% in H1 2026 [B, C9-S015]), a founder plus a coordinator can clear about $90k by year 3. A 5-point margin loss from tariffs or price matching against 4imprint's published prices cuts base year 3 to about **$8k**.
> - **Bottom line:** this is a safe, fast, cheap-to-test business with a modest ceiling. It is not a holding-company engine.

## 1. Specific initial niche
**The offer:** branded workwear and safety-recognition merchandise for commercial trade contractors. Target firms are electrical, plumbing, HVAC/sheet-metal and mid-size general contractors with roughly 20–250 field employees, based in Cook, DuPage, Kane, Lake and McHenry counties.

**What they buy:**
- ANSI hi-vis tees and vests;
- embroidered hoodies, jackets and caps;
- new-hire "crew kits";
- Construction Safety Week and OSHA stand-down recognition items;
- superintendent and client gifts;
- an online company store for reorders, added later.

**Why this niche:**
- **The buyers are named in public data.** 1,266 contractors appear on five or more City of Chicago permits of at least $100k issued between 2025-01-01 and 2026-11-25 [A, DH-S031].
- **Demand is recurring.** It is driven by hiring, crew turnover, seasonal gear, annual safety events and jobsite PPE.
- **The sector is growing for promo.** Construction gained a point of promo-industry share in 2025 [C, C9-S012].
- **The large direct marketer leaves gaps.** 4imprint does not do jobsite delivery, size-run management, or union-label sourcing.
- **Corporate procurement is lighter** than in healthcare systems.

**Rejected alternatives:**
- **Healthcare employers.** This is the fastest-growing segment (+2 points [C, C9-S012]), but it is gated by GPOs and procurement.
- **Schools and teams.** Price-driven and seasonal.
- **Corporate onboarding kits.** Contested by BAMKO/HALO-type networks and Swag.com-type platforms.

## 2. Named operators

| Operator | What is known | Basis |
|---|---|---|
| **4imprint Group** (Oshkosh WI; national direct marketer) | FY2025 revenue $1,346.8M, operating margin 10.8%, 2.06M orders (~$654 AOV, our calc) [A, C9-S014]. H1-2026 gross margin 31.5% (32.8%) on tariff costs [B, C9-S015]. ~81% of H1 orders from existing customers (838k of 1,040k, our calc) [B, DH-S026]. ~$810k revenue per North American employee [B, DH-S027]. Publishes end-buyer prices, e.g. hi-vis short-sleeve tee $19.25–$32.75 [B, DH-S025]. | A–B |
| **Whitestone (ASI testimonial)** | ~$1M sales in 3 years, ~$16M after 11 years from ~$10k start | D, WS16-S026 |
| **HALO, Staples Promotional Products, Custom Ink, Proforma** | Lead the Counselor Top 40 | C, Stage C search extract |
| **Local contract decorators**, e.g. Chicago Printing and Embroidery / 4Logoz (Addison) | Founded 1997; contract decoration for ad-specialty distributors since ~2001 | D, DH-S032 |
| **Hightech Grafix** (trade-only decorator, national) | Publishes distributor pricing (below) | B, DH-S030 |
| **Small distributors (<$1M)** | Flat in Q2 2026 while >$1M firms grew ~4% [C, C9-S013]. Census counts 395 Illinois employer establishments in NAICS 541890; most distributors are non-employers [C, C9-S007] | C |

## 3. Suppliers and partners (documented vs assumed)
Full detail is in `09_databases/suppliers/WS16-006_suppliers.csv`.

- **PPAI membership, which includes SAGE Workplace — documented [B, DH-S020].**
  - Standard Base costs **$595/yr** for firms up to $500K and includes one SAGE licence. Standard Plus costs $785/yr (up to $1M).
  - Distributor status is defined by business model; "additional qualifications may apply" (documents MISSING).
  - This is the cheapest route to supplier search and an industry ID.
- **ASI / ESP+ — assumed.**
  - The price is not published. Stale third-party figures are $29.99/month plus a $150 application fee; an ASI page shows ESP+ promo pricing of $99.99–$149.99/month [D, DH-S022].
  - Suppliers often ask for an ASI number [C, DH-S023]. Whether a PPAI/SAGE number suffices is to be confirmed.
- **SanMar (blank apparel and workwear) — documented [B, DH-S024].**
  - The credit application offers **Net 30 or credit card** and asks for ASI number, resale number, D&B, trade references and bank details.
  - It includes a credit report, a **personal guaranty** and a 1.5% monthly late charge.
  - The founder's personal credit is unknown, so this is flagged.
- **Hightech Grafix (contract decoration) — documented [B, DH-S030].**
  - Screen print: $3.33/piece at 12 pieces, falling to $0.27 at 10k+; $20 per screen.
  - Embroidery: $13.85 for 1 piece, falling to $2.43 at 1,000.
  - Turnaround 5–7 business days; trade-only.
- **commonsku (CRM, presentations, stores) — documented [B, DH-S021].**
  - $129/user/month with a 2-user minimum.
  - Store fees fall from 2.5% to 1% as lifetime store sales rise.
- **Cap America (headwear decoration) — assumed [D, search extract].** About $3.30 at 48–71 pieces.
- **Supplier credit in general [C, DH-S023]:** granted case by case after a credit application. New accounts should be modelled as card-prepaid (DPO 15 days base).

## 4. Named prospective customers
**30 Illinois organizations** are listed in `09_databases/prospects/WS16-006_prospects.csv`. All are "prospect — not contacted". Each was matched to Chicago permit records and its own website on 2026-11-28 [A, DH-S031; D, DH-S033 method].

- **Electrical:**
  - REX Electric & Technologies (88 permits);
  - Battaglia Industries (Elgin);
  - Carlyn Electrical (Elk Grove Village);
  - Edge Electrical Systems;
  - Connor Electric;
  - Mirex Electric (Bensenville).
- **Plumbing:**
  - Chi-Town Plumbers (North Riverside);
  - R. Carrozza Plumbing;
  - Katco Development;
  - Chicago Area Plumbing.
- **HVAC / mechanical:**
  - Sherman Mechanical (Cary, 121 permits);
  - CT Mechanical (Addison);
  - Admiral Heating & Ventilating (151 permits);
  - CSL Climate Control;
  - Air Comfort Corp.;
  - Atomatic Mechanical;
  - F.E. Moran and The Hill Group (larger; stretch prospects).
- **General contractors:**
  - Toro Construction;
  - Redmond Construction;
  - All-Bry Construction;
  - Reed Construction;
  - K.R. Miller;
  - Valenti Builders;
  - Lo Destro;
  - 41 North Contractors;
  - TBI Contractors.
- **Associations (buyers and channels):**
  - Mechanical Contractors Association of Chicago;
  - ECA of the City of Chicago;
  - Chicagoland AGC.

Permit counts measure Chicago activity only. "Reported cost" is project value, not firm revenue.

## 5. Representative transactions

| # | Transaction | Revenue | Direct costs | Contribution | Payment timing |
|---|---|---|---|---|---|
| T1 | New-account crew kit for a ~40-person electrical sub: 60 hi-vis tees @ $18, 30 embroidered hoodies @ $38, 60 caps @ $16, $60 screens, $45 freight | $3,285 | Blanks + decoration ~$2,200 (67%); freight $60; card 3% $99 | **$926 (28%)** | 50% deposit, balance net-30; supplier paid by card at PO |
| T2 | Construction Safety Week order: 150 laser-engraved 18-oz tumblers @ $14, 150 safety tees @ $12 | $3,900 | Product + decoration $2,535; freight $90; processing $60 | **$1,215 (31%)** | Net-30 invoice vs card at order → ~45-day float gap |
| T3 | Monthly company-store replenishment, 120-employee mechanical contractor | $2,000/mo | Product $1,380; store fee 2.5% $50; kitting/shipping $70 | **$500/mo (25%)** | Store paid by card or monthly invoice |

**How the prices were set:**
- All sell prices sit at or below 4imprint's published ranges [B, DH-S025]:
  - tumblers: $12.85–$21.35;
  - embroidered caps: $6.75–$39.75.
- The cost ratios assume the newcomer earns slightly below 4imprint's 31.5% gross margin. This is E, anchored on B.

**Per-account economics (E):** a typical active account is modelled at ~$650/month in reorders (about $7.8k/yr) plus a $2,500 first order.

## 6. Customer acquisition

**Customer #1:**
- Join PPAI ($595) and build a $300 jobsite sample kit (hi-vis tee, hoodie, cap, tumbler).
- Call 40 contractors from the permit list where the founder can reach the office or safety lead.
- Offer free mockups and size-run management. Win one first order of $1.5–3k.

**Customers #2–10:**
- Time outreach to calendar triggers: spring hiring, Construction Safety Week (May), winter gear (Sept–Oct) and the holidays.
- Ask every first customer for an introduction to its GC or sub partners.
- Attend MCA Chicago, ECA and Chicagoland AGC events. Associate-membership cost is MISSING.

**Customers #11–100:**
- Open company stores for the 5–10 largest accounts.
- Systematize a referral ask.
- Hire one outside rep only after the founder sustains ≥3 new accounts a month and ≥31% gross margin.
- Expand targeting to suburban permit data. Not yet pulled; DuPage, Lake and others have their own portals.

**Funnel (all E):**

| Stage | Monthly volume |
|---|---|
| Outbound touches | ~150 |
| Qualified conversations | 30 |
| Quote/mockup (40%) | 12 |
| Win (25%) | ~3 new accounts |

**Unit economics:**
- **CAC:** about $150 variable plus ~$117 of fixed marketing per win, plus ~20 founder hours.
- **LTV:** gross profit ≈ $650 × 31% × 40-month expected life (2.5% monthly churn) + $750 first-order gross profit ≈ **$8.8k**.
- **Payback:** 2–5 months on cash cost. It is dominated by founder time.

**Weekly human sales work:** 15–20 hours prospecting and meetings, plus 10–15 hours on quotes and orders until a coordinator is hired (modelled at about $35k/month of sales).

**Why acquisition assumptions are kept modest:**
- Industry evidence argues for caution: 4imprint's new-customer orders fell 12% in 2025 [A, C9-S014] and 7% in H1 2026 [B, DH-S026].
- Small distributors were flat [C, C9-S013].

## 7. Pricing strategy
- **Price ceiling:** 4imprint's published price for the comparable item and quantity [B, DH-S025].
- **Target gross margin:**
  - 30–38% on decorated apparel and hard goods (4imprint 31.5% [B]; ASI claims 37% [C, WS16-S026]);
  - 25% floor on large company-store programs.
- **Always pass through:** setup and screen charges ($20/screen benchmark [B, DH-S030]), rush fees and freight.
- **Deposits:** require a 50% deposit on first orders and on any order over $2,500.
- **Card surcharge:** apply one where lawful (requires confirmation).
- **Premium items:** charge extra for union-label printing, ANSI-certified hi-vis, embroidery on brand-name workwear and jobsite delivery or kitting.
- **Do not compete on commodity tees** below 4imprint's price.

## 8. Working capital and cash conversion cycle
Base case: DSO 40 days, inventory 3 days, DPO 15 days, so the cycle is **~28 days**.

| Accounts | Monthly sales | AR (40 d) | AP | Inventory | Net working capital |
|---|---|---|---|---|---|
| 10 | ~$9k | ~$12k | ~$3k (15 d) | ~$0.6k | **~$9–10k** |
| 50 | ~$35k | ~$47k | ~$12k (15 d) | ~$2k | **~$37k** |
| 200 | ~$140k | ~$187k | ~$80k (25 d, once credit exists) | ~$7k | **~$110k** |

- **Model results:** peak funding need is **$45k** including a $3k/month owner draw from month 13, or **$17k** without the draw. Year-3 ending net working capital is $78k.
- **Main stress:** "Customers pay 30 days later" raises peak funding to $124k. ASI's 2023 survey says big-client terms now reach "sometimes 120 days" [C, DH-S028].
- **Mitigations:** deposits, card-on-file for small accounts, and avoiding net-60 or net-90 GCs until supplier credit lines exist.
- **Personal credit:** supplier credit needs a personal guaranty [B, DH-S024].

## 9. Regulatory path
| Step | Detail | Fee / time |
|---|---|---|
| Illinois LLC | Articles of Organization with the Secretary of State | Fee not re-verified (MISSING); ~1 week (E) |
| Tax registration | IDOR registration (REG-1, MyTax Illinois) so the firm can buy tax-free for resale (CRT-61) and collect Retailers' Occupation Tax [A, WS16-S036] | No fee found; 1–2 weeks (E) |
| Local taxes | Chicago and home-rule sales-tax layers on Illinois-delivered goods | Rates MISSING; requires confirmation |
| Product rules | ANSI/ISEA 107 hi-vis compliance (buy certified garments; check that logo placement does not breach the background or retroreflective-area rules — requires confirmation). CPSIA only for youth items; Prop 65 only for California shipments | — |
| Licences | No professional licence | — |
| Insurance | General plus product liability; indicative ~$70–125/month (E, no quote) | — |

## 10. Operations workflow (lead to cash)

| Step | Who / what does it | Mode |
|---|---|---|
| 1. Lead | From permit list or referral | Human |
| 2. Discovery | Crew size, sizes, colours, union label, deadline | Human |
| 3. Mockups | Logo vectorizing and mockups | AI-assisted; vectorizing uses supplier or decorator services |
| 4. Quote | In SAGE Workplace, included in PPAI, [B] | AI-assisted |
| 5. Deposit invoice | QuickBooks | Automated |
| 6. Purchase order | To supplier or contract decorator | — |
| 7. Proof approval | Customer approves | Human |
| 8. Production | 5–7 business days [B, DH-S030] | Supplier |
| 9. Delivery | Drop-ship, or founder delivers and kits for jobsites | Human / supplier |
| 10. Balance invoice | Net-30 reminders | Automated |
| 11. Reorder prompts | From order history (sizes, logo files) | Automated |

**Software stack and monthly cost:**

| Tool | Cost | Source |
|---|---|---|
| PPAI incl. SAGE | $50/mo | B |
| commonsku, from month 13 when a coordinator joins | $258/mo | B |
| AI assistants | ~$60/mo | E |
| Accounting, e-sign, phone, website | ~$120/mo | E |

**Total AI/software is about $490/month.** A ×3 AI-cost stress cuts base year 3 to $32k, so the model does not rely on cheap AI.

**What stays human:** relationship selling, problem-solving on deadlines and quality control.

## 11. Competitive position and defensibility over time
**What accumulates:**
1. Account records: size runs, logo files and reorder calendars. These lower switching for HR and safety managers.
2. Company stores embedded in onboarding.
3. Approved-vendor status at GCs, which pulls in their subs.
4. Association presence.
5. A local decorator bench that can do union-label and rush work.

None of this is proprietary; any of the "tens of thousands" of distributors [C, C9-S012] can copy it. Over 3–5 years the moat is relationship density in one trade cluster, which supports the model's ~26% annual account loss rather than lower.

**Delegation:** rep-based selling is standard in the industry. But a rep costs ~$75k median [C, DH-S028] or about 40–50% of gross profit [D, DH-S029]. In the model, a rep hired in month 25 *reduces* year-3 profit by ~$47k and only pays back from year 4.

## 12. Key risks and pre-mortem
**How it fails, by amount lost:**
- **$5k lost.** PPAI, samples and 3 months of outreach produce fewer than 3 orders. The likely cause is that contractors already have a local shop or buy from 4imprint, so the wedge failed.
- **$25k lost.** A contractor customer defaults on two large invoices, or a misprinted 300-piece order must be re-run at the distributor's cost. With 31% margin, one $8k reprint wipes out about 3 months of profit.
- **$50k lost.** The founder hires a rep and coordinator ahead of demand. Tariffs and price matching then cut gross margin by 5 points; the model shows base year 3 at $8k and a ×1.5 recession stress near zero. The founder keeps paying staff for a year.

**Early-warning indicators:**
- quote-to-win rate below 15% after 40 quotes;
- average first order below $1,200;
- blended gross margin below 28% for two months;
- DSO above 55 days;
- under 40% of first-order accounts reordering within 6 months.

**Other risks:**
- construction cyclicality (a recession stress takes year 3 to ~$0);
- supplier tariff shocks [A, WS16-S022];
- founder burnout, since the business is founder-capped (G7 WARN).

## 13. Validation plan

| # | Experiment | Cost | Success | Kill |
|---|---|---|---|---|
| V1 | Join PPAI (SAGE) and open SanMar plus one hard-goods supplier on card terms; price 20 real contractor baskets against 4imprint | $595 + $0 | ≥30% achievable gross margin at or below 4imprint price on ≥70% of baskets | <25% gross margin on most baskets |
| V2 | 45-day outbound sprint to 120 permit-listed contractors with a $300 sample kit | ~$400 + time | ≥5 **paid** orders, average ≥$1,500 | ≤1 paid order |
| V3 | Company-store pilot with the 2 largest V2 customers (commonsku trial or SAGE store) | ~$300 | ≥$1,500/month combined after 90 days | <$500/month |
| V4 | Union-label probe: quote union-printed vs standard to 10 union subs | $0 | ≥3 pay a ≥10% premium | 0 care |
| V5 | 90-day reorder check on V2 accounts | $0 | ≥50% reorder | <25% |

Total cash before go/no-go is about **$1.3–1.6k**.

## 14. Revised scores and verdict

| Criterion | Stage C | Stage D | Reason |
|---|---|---|---|
| fcf | 4 | 4 | Base year 3–5 is $44–165k ($91–200k without a rep) |
| roic | 8 | 7 | Receivable float raises capital at risk to $17–45k |
| access | 6 | 6 | Buyers named via permits; short cycle; incumbents entrenched |
| scale | 5 | 5 | Reps and stores scale, but rep economics are thin |
| resilience | 4 | 4 | Discretionary spend in a cyclical customer base |
| entry | 3 | 4 | A trade-vertical wedge plus stores is credible but copyable |
| delegation | 5 | 5 | — |
| cash | 7 | 6 | DSO 40 days vs supplier prepay; terms creep |
| feasibility | 10 | 9 | No licence; supplier credit needs a personal guaranty |
| ai | 4 | 4 | — |

- **Raw score:** about 5.24 (Stage C was 5.39). Evidence-adjusted (C): about **5.2**.
- **Verdict:** **RESERVE.**
  - **For:** the best "start this week" fallback in the batch. It needs no licence, validation costs under $2k, and gross margin is verified.
  - **Against:**
    - base economics are a good job, not a holding-company engine;
    - tornado and stress tests show profit is hostage to gross margin and win rate;
    - small distributors are the industry's weak tier.
- **What would promote it:** V2 and V5 both passing — five or more paid orders and at least 50% of those accounts reordering.
