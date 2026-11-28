# WS16-006 — Stage E Playbook: Branded workwear, safety-recognition and promotional merchandise for Chicago trade contractors

> **Verdict: CONDITIONAL — validate for under $1,600; do not invest beyond that until a margin test passes.**
> - Evidence level: **C**. Incumbent prices and costs are A–B; new-entrant volume, win rate and reorder spend are E.
> - Model (rebuilt 2026-11-28, $4,000/month owner draw from month 13 in every scenario), operating profit before owner pay:
>   - **Base:** year 3 **$78,108**, year 5 **$141,481**.
>   - **Conservative:** year 3 **$18,914**, year 5 **$40,771**.
>   - **Optimistic:** year 3 $313,332, year 5 $800,927.
> - **Peak funding:** base **$39,105** with the draw ($17,718 without). Conservative is $161,983 with the draw ($35,722 without), and still rising in month 60, because the business cannot pay a $4,000 draw in that case.
> - **The decisive fact:** desk pricing (§3) shows a newcomer buying blanks at public prices and matching 4imprint's published prices earns **5–25% gross margin** on decorated apparel, and loses money on ANSI hi-vis tees. Reaching ≥30% needs one of two things:
>   - contractors already pay ~10–35% more than 4imprint and will keep doing so for better service; or
>   - distributor net costs come in well below public blank prices.
> - **Cheapest decisive test:** the "incumbent-invoice margin test" (§4, V1+V2) settles this for $0–$600 in about three weeks.

## 0. What changed since Stage D (corrections)
- **Correction — 4imprint price ceilings were mis-read.**
  - The ANSI Class 2 hi-vis tee (CornerStone, back embroidery) is $22.50 at 48 and $20.95 at 72 [B, E-WS16006-S001], not "$19.25–$32.75".
  - The 18-oz laser-engraved tumbler is $12.29 at 144 plus a $45 setup [B, E-WS16006-S003], not "$12.85–$21.35". Stage D's ranges came from the search-results layout.
  - As a result, Stage D's T1 (ANSI tee at $18 with a 67% cost ratio) and T2 (tumbler at $14, "at or below 4imprint") were not supported. They are rebuilt in §3.
- **Correction — conservative-case staffing.** Stage D hired an outside rep unconditionally in month 25. The conservative case then lost money for three years (peak funding $329k), which contradicts Stage D's own rule: hire a rep only after the founder sustains the pipeline. The rep is now hired only once monthly revenue reaches $60k.
  - Applying the old unconditional month-25 hire to today's drivers gives conservative peak funding of $417,290 and base year 3 of $35,491. This stays as a pre-mortem case.
- **Correction — gross margin lowered.**
  - Base recurring gross margin goes from 31% to 30%; first orders from 30% to 28%.
  - Conservative goes from 27%/26% to 25%/23%.
  - Reason: the item-level cost evidence in §3. Industry averages (34–37%) are kept as incumbent economics.
- **Correction — missing source.** "DH-S033" was cited in Stage D, but no such source record exists. The prospect method is the per-row Chicago permit API query in the prospect CSV [A, DH-S031].
- **Standardization.**
  - Draw raised from $3,000 to $4,000/month.
  - Tax 30%.
  - Start capital = **$39,200**, the smallest injection (rounded up to $100) that keeps base cash ≥ 0.
  - Coordinator cap raised from 3 to 6 so optimistic staffing scales.
  - Long-term drivers now evidenced (§7).

---

## 1. Business explanation

**What it is.** A promotional-products distributor that specialises in one buyer: commercial trade contractors in the Chicago area. These are electrical, plumbing, HVAC/sheet-metal and mid-size general contractors. It sells:
- branded crew apparel: safety-colour tees, embroidered hoodies, jackets and caps;
- ANSI-certified hi-vis where it can be sourced at a margin;
- new-hire "crew kits";
- Construction Safety Week and stand-down recognition items;
- superintendent and client gifts;
- later, online company stores and gear-allowance programs that turn one-off orders into scheduled reorders.

**How it works, for someone new to the industry.**
- The distributor owns no factory and holds almost no stock.
- Product comes from three places:
  - blank-apparel wholesalers (SanMar, S&S Activewear);
  - promotional suppliers that make and decorate hard goods such as tumblers;
  - contract decorators that screen-print or embroider for distributors only (e.g., Hightech Grafix: trade-only, 5–7 business days [B, DH-S030]).
- The distributor's job is everything around production:
  1. learn the crew's sizes, colours, logo and deadline;
  2. make a mockup;
  3. quote;
  4. take a deposit;
  5. place purchase orders with the supplier and decorator;
  6. manage the proof;
  7. check quality;
  8. deliver to the yard or jobsite;
  9. invoice;
  10. remind the customer to reorder.
- The industry sells $27.1B a year through U.S. distributors (PPAI, 2025, +1.3%) [C, E-WS16006-S008]; ASI puts North America at $27.7B (+4.2%) [C, C9-S012]. Both figures are kept.

**Why contractors pay.**
- Field crews turn over fast. Construction's hires rate averaged about 4.2% *per month* in Jan–Sep 2026, roughly half the workforce a year [A, E-WS16006-S015]. Every hire needs shirts, a hoodie and a cap.
- Safety culture runs on visible recognition. Safety Week 2027 is May 3–7, with 3,094+ participating companies [C, E-WS16006-S019].
- Branded crews advertise the firm on every jobsite.

**There are two budgets, with very different price sensitivity:**
- **Required PPE.** OSHA requires employers to pay for PPE used to comply with construction standards [A, E-WS16006-S016]. This is a safety-director line item: it must be compliant, and it is price-compared.
- **Discretionary items.** "Everyday clothing" and weather wear (jackets, hats) are *not* required employer purchases [A, E-WS16006-S016]. Branded hoodies, jackets and caps are therefore a culture, recruiting and marketing choice, where service and look matter more than unit price.

**How it earns.** Gross margin on each order: the sell price minus blank, decoration, freight and setup. Plus pass-through setup, rush and kitting fees. Plus, later, program fees.

**Why it is attractive:**
- It needs no licence.
- Validation costs hundreds of dollars.
- Revenue can start within 4–8 weeks.
- 4imprint, the largest direct marketer, keeps about 81% of its orders coming from existing customers [B, DH-S026], so repeat behaviour is a real feature of the category.

**Why it is hard:**
- Margins are thin and price-transparent. 4imprint publishes its prices, and its own gross margin fell to 31.5% in H1-2026 on tariff costs [B, C9-S015].
- Small distributors (under $1M) were flat in Q2-2026 [C, C9-S013].
- Profit grows only as fast as the founder can win and keep accounts.

## 2. Commercial entry

### 2.1 Niche, customer, geography
- **Customer:** commercial trade contractors with about 20–250 field employees, based in Cook, DuPage, Kane, Lake and McHenry counties.
- **Buyer roles:**
  - safety director (PPE, Safety Week, recognition);
  - operations or HR/office manager (new-hire kits, reorders);
  - owner (at firms under ~50 people).
- **Universe:** 1,266 contractors appear on ≥5 City of Chicago permits of ≥$100k reported cost issued 2025-01-01 to 2026-11-25 [A, DH-S031]. By role: GC 341, electrical 309, plumbing 293, refrigeration 193, ventilation 109.
- **Not targeted first:**
  - healthcare (procurement-gated);
  - schools and teams (price-driven);
  - corporate onboarding kits (BAMKO/HALO-type networks and swag platforms).

### 2.2 Named suppliers and partners
Full list in `09_databases/suppliers/WS16-006_suppliers.csv`; Stage E rows were appended.

| Role | Organisation | What is documented | Evidence |
|---|---|---|---|
| Industry ID + product search | PPAI (incl. SAGE Workplace) | $595/yr up to $500K sales, 1 SAGE licence | B, DH-S020 |
| Industry ID (alternative) | ASI / ESP+ | Price not published; suppliers often ask for an ASI number | D, DH-S022; C, DH-S023 |
| Blank apparel | SanMar | Net 30 *or* card; credit app with personal guaranty, 1.5%/month late fee | B, DH-S024 |
| Blank apparel | S&S Activewear | Alphabroder's old decoration-price URL now redirects to ssactivewear.com (observed 2026-11-28; consolidation not otherwise verified) | D |
| Public blank-price benchmark | ShirtSpace | G500 tee from $2.71 (colours); G18500 hoodie $12.30–$13.83; Richardson 112 $9.75; CornerStone CS401 ANSI tee $17.54 | B (as e-tailer price), D (as proxy) — E-WS16006-S004/S005 |
| Contract decoration (national) | Hightech Grafix | Screen print $3.33/pc at 12 → $0.27 at 10k, $20/screen; embroidery $13.85 at 1 → $2.43 at 1,000 | B, DH-S030 |
| Supplier-decorator (list prices) | All-Secure Graphics | 2026 embroidery list: $9.58–$10.08 at 48 (≤8k stitches); embroidered G18500 hoodie $33.54 at 48 "(R)" | B, E-WS16006-S006 |
| Local contract decoration | Chicago Printing & Embroidery / 4Logoz (Addison) | Contract decoration for ad-specialty distributors since ~2001; no price list | D, DH-S032 |
| Local decoration + union label | Minuteman Press Chicago | Says it is a licensed union printer offering apparel | D, E-WS16006-S023 |
| Headwear | Cap America | ~$3.30 contract cap decoration at 48–71 pcs (2025 catalog extract) | D |
| CRM / stores | commonsku | $129/user/month (minimum 2); shop fee 2.5% → 1% | B, DH-S021 |
| Company/redemption stores | OrderMyGear / BrightStores | Company store hosting ~$119/month (Standard); redemption $0.99/order | D, E-WS16006-S017 |

**Decorator access in Chicago:**
- The suburban field is dense. BBB lists about 190 custom-logo-apparel and 70 uniform-embroidery businesses around Elk Grove Village/Addison [D, E-WS16006-S027].
- Most sell to end users, and a newcomer needs *trade* pricing. Only Chicago Printing & Embroidery/4Logoz is documented as serving distributors [D, DH-S032].
- Hightech Grafix is documented trade-only, but its location is not stated, so freight time to Chicago is MISSING.
- Union-label decoration requires a shop licensed for the Allied Printing Trades Council label, a registered certification mark [C, E-WS16006-S024]. Minuteman Press Chicago claims that licence [D, E-WS16006-S023]; whether it applies the label to garments is unconfirmed.
- **Supplier qualification is therefore a validation step (§4), not an assumption.**

**Tariff exposure on imported blanks and hard goods (status 2026-11-28):**
- **Base duties.** Most blanks are imported. Base (MFN) duty is:
  - 16.5% on cotton knit tees;
  - **32%** on man-made-fibre knit tees, which covers most polyester hi-vis tees;
  - 32% on man-made-fibre sweatshirts;
  - CAFTA-DR-origin goods enter free [A, E-WS16006-S014].
- **IEEPA and Section 122.** IEEPA tariffs were struck down on 2026-02-20 [A, WS16-S022]. A Section 122 global duty followed from 2026-02-24 to 2026-07-24, excluding CAFTA-DR duty-free textiles [C, E-WS16006-S013]. One firm reports it at 15%; RILA reports 10% [C, E-WS16006-S021]. Both are kept.
- **Section 301 since July 2026.** Additional tariffs of **10% or 12.5%** apply to the top 60 trading partners (99.4% of imports) [A, E-WS16006-S012]. The per-country rates and CAFTA-DR treatment are MISSING; check Federal Register notice 2026-15181.
- **Effect on pricing.** Nearly 90% of distributors raised prices in 2025, by about 11% on average [C, E-WS16006-S011]. SanMar says its basics line made in Tennessee is not tariffed [D, E-WS16006-S022].
- **Practical rules:**
  - Quote with a 15-day validity.
  - Re-price stores quarterly.
  - Prefer CAFTA-DR- or US-made blanks where the customer accepts them.
  - Treat ±5 gross-margin points as live tariff risk (stress test, §7).

### 2.3 Top 15 named prospects
Full list of 30 in `09_databases/prospects/WS16-006_prospects.csv`. All are "prospect — not contacted". Permit counts are Chicago-only and are proxies for crew size [A, DH-S031].

| # | Prospect | Trade / location | Why it is a target |
|---|---|---|---|
| 1 | Sherman Mechanical | HVAC/plumbing, Cary | 121 permits, so constant crews; suburban HQ suits yard delivery |
| 2 | CT Mechanical | HVAC, Addison | 62 permits; near Addison decorators |
| 3 | Chi-Town Plumbers | Plumbing, North Riverside | 51 permits; mid-size |
| 4 | REX Electric & Technologies | Electrical, Chicago | 88 permits; city HQ |
| 5 | CSL Climate Control | HVAC, Wheeling | 58 permits |
| 6 | Toro Construction | GC, Orland Park | 59 permits; a GC can pull in its subs |
| 7 | Redmond Construction | GC, Chicago | 59 permits |
| 8 | Battaglia Industries | Electrical/mechanical, Elgin | 40 permits |
| 9 | Air Comfort Corp. | Commercial HVAC service, Broadview | Service techs make a natural uniform-allowance program |
| 10 | Chicago Area Plumbing | Plumbing/mechanical, Elk Grove Village | 37 permits; $339M of reported project value |
| 11 | R. Carrozza Plumbing | Plumbing, Franklin Park | 34 permits |
| 12 | Mirex Electric & Construction | Electrical, Bensenville | 33 permits |
| 13 | All-Bry Construction | GC, Burr Ridge | 48 permits |
| 14 | Mechanical Contractors Association of Chicago | Association | Buyer for events and awards; channel to members |
| 15 | Chicagoland AGC | Association | Safety programs; channel to GCs |

Stretch accounts, likely centralised procurement: Admiral Heating & Ventilating (151 permits), F.E. Moran, The Hill Group.

### 2.4 Named competitors
- **4imprint.** National online player and the price ceiling. FY2025 revenue $1,346.8M; operating margin 10.8% [A, C9-S014]. It publishes item-level prices (§3).
- **Custom Ink, HALO, Staples Promotional Products, Proforma.** Lead the Counselor Top 40 [C, Stage C].
- **Local decorators and shops.** About 190 listings in the suburbs [D, E-WS16006-S027], e.g., DLS Printing & Custom Embroidery (Elk Grove Village) and Chicago Printing & Embroidery (Addison).
- **Uniform rental.** UniFirst sells managed rental to Chicago trades, with hi-vis, logo embroidery and weekly service [C, E-WS16006-S020]. Alsco and Cintas are similar, but their terms were not researched.
- **The contractor's current habit:** the owner's cousin's shop, Amazon, or the GC's giveaway. No data; V1 measures it.

### 2.5 Positioning
"The crew-gear desk for Chicago trade contractors":
- sized, branded and delivered to the yard;
- new-hire kits restocked automatically;
- Safety Week handled end to end;
- one email to reorder.

**The wedge is service, not price:**
- size-run management;
- jobsite and yard delivery;
- reorder records;
- union-label sourcing where it is wanted;
- compliance-aware recognition programs (§3.4).

Stage D claimed that 4imprint lacks jobsite delivery and size-run management. That claim is unverified (E).

### 2.6 Pricing
- **Price index target: 1.05–1.20 × 4imprint's published price** for the same item and quantity [B, E-WS16006-S001/S002/S003]. This stays below supplier list pricing; for example, an embroidered hoodie is $33.54 at list [B, E-WS16006-S006] against $22.50 at 4imprint.
- **Gross-margin floors:**
  - 30% blended;
  - 25% on company stores;
  - never below 20% on any line without the founder's sign-off.
- **ANSI-certified hi-vis:** quote only after the real net cost is known. At public blank prices it loses money at 4imprint parity (§3).
- **Always pass through:**
  - setup and screen charges ($20/screen benchmark [B, DH-S030]);
  - tape/digitizing (4imprint charges $35 under 24–72 pieces [B, E-WS16006-S001/S002]);
  - rush fees;
  - freight to multiple drop points.
- **Deposits:** 50% on first orders and on any order over $2,500. Card on file for small accounts.

### 2.7 Sales and acquisition strategy
- **List:** permit-active firms (§2.3), extended to suburban permit portals once validation passes.
- **Entry offers, in order:**
  1. **Safety Week 2027** (May 3–7). Pre-sell February–March; this creates urgency and is a natural first order.
  2. **New-hire crew kit.** Pre-packed by size and delivered to the yard.
  3. **Winter/seasonal refresh** (September–October).
- **Channels:**
  - phone and email to the main line, asking for the safety or office manager;
  - a jobsite sample kit (one of each item);
  - association events (MCA Chicago, ECA Chicago, Chicagoland AGC; associate-membership costs MISSING);
  - GC-to-sub referrals.
- **Model funnel (E):** 30 qualified conversations/month → 40% ask for a quote → 25% win, which is ~3 new accounts/month at full pace, after a 6-month ramp.

## 3. Transaction economics

### 3.1 The margin problem, item by item
**Landed newcomer cost** = public blank price + contract decoration + setup per piece + freight. Decoration between Hightech Grafix's published points is interpolated (E). The table compares this cost against 4imprint's published price.

| Item, quantity | 4imprint price | Landed cost | GM at parity | GM at +10% | Price needed for 30% |
|---|---|---|---|---|---|
| Gildan G500 safety-colour tee, 1-colour, 144 | $6.25 | $4.69 | 25.0% | 31.8% | $6.70 (+7%) |
| Gildan G500 safety-colour tee, 72 | $7.25 | $5.38 | 25.8% | 32.6% | $7.68 (+6%) |
| Gildan 18500 hoodie, left-chest embroidery, 24 | $25.75 | $23.16 | 10.1% | 18.2% | $33.08 (+28%) |
| Gildan 18500 hoodie, embroidery, 48 | $22.50 | $21.43 | 4.8% | 13.4% | $30.61 (+36%) |
| Richardson 112 cap, embroidery, 24 | $18.95 | $15.65 | 17.4% | 24.9% | $22.36 (+18%) |
| CornerStone CS401 ANSI Class 2 tee, back embroidery, 72 | $20.95 | $23.43 | −11.8% | −1.7% | $33.47 (+60%) |

Sources: prices [B, E-WS16006-S001/S002]; blanks [B/D, E-WS16006-S004/S005]; decoration [B, DH-S030; E interpolation].

**What this means:**
- **Public blank prices are probably an upper bound.** 4imprint sells the decorated ANSI tee at $16.25 at 576 pieces, below ShirtSpace's $17.54 *blank* price. Large-buyer net prices must therefore be far lower. The newcomer's real SanMar/S&S net price is MISSING. Finding it is validation step V2.
- **Distributors normally quote off supplier list, not 4imprint.** All-Secure's list for an embroidered hoodie at 48 is $33.54. At the conventional "R" code (40% off list; an industry convention, not verified here) the distributor pays $20.12, so selling at list earns 40%, and selling at 4imprint's $22.50 earns 10.6% [B, E-WS16006-S006].
- **The industry's reported margins depend on buyers paying above 4imprint.** PPAI reports 34–36% gross margin for 2025 across size bands, and 34% for firms under $3M in 2024 [C, E-WS16006-S009]. Counselor reports a 37.1% average [C, E-WS16006-S010]. Those margins can exist only if many end buyers pay well above 4imprint, through habit, relationship or service.
- **The business works only if Chicago contractors are among those buyers.** That is exactly what V1 measures.
- **Merchandising rule that follows:**
  - Lead with safety-colour tees, hard goods with setup fees, and service bundles.
  - Price embroidery and brand items from list downward, not from 4imprint upward.
  - Quote certified hi-vis only after the net cost is known.

### 3.2 Representative transactions (rebuilt; in model `UnitEconomics`)

**T1 — New-account crew kit for a ~40-person electrical sub**

| Line | Amount |
|---|---|
| Revenue: 96 safety tees @ $8.25 + 40 embroidered hoodies @ $26.50 + 40 embroidered caps @ $18.50 | **$2,592.00** |
| Tees: blank $2.95 avg + print ~$1.60 + $20 screen + freight $0.35 | −$490.56 |
| Hoodies: blank $14.60 avg + embroidery ~$5.50 + $35 digitizing + freight $0.60 | −$863.00 |
| Caps: blank $9.75 + embroidery ~$4.75 + freight $0.40 | −$596.00 |
| Card fee on the 50% deposit (3%) | −$38.88 |
| **Contribution** | **≈$604 (23.3%); gross margin 24.8%** |

- At strict 4imprint parity the order earns 21.5% gross margin.
- At local-shop-like prices (hoodie $29, cap $21) it earns **30.2%**.
- **Cash:** 50% deposit at order. Suppliers are paid by card at PO. The balance is due net-30 after delivery, roughly 5 weeks out.

**T2 — Construction Safety Week order (May 3–7, 2027)**

| Line | Amount |
|---|---|
| Revenue: 150 laser-engraved 18-oz tumblers @ $13.50 + $45 setup passed through; 150 "Safety Week" tees @ $7.25 | **$3,157.50** |
| Tumblers: supplier net incl. engraving *assumed* $9.25 + $36 setup + $75 freight | −$1,498.50 |
| Tees | −$702.50 |
| Processing | −$47.00 |
| **Contribution** | **≈$910 (28.8%)** |

- Tumbler supplier net is MISSING (E).
- The sell price sits 10% above 4imprint's $12.29 at 144 [B, E-WS16006-S003].
- **Cash:** net-30 invoice, with suppliers card-paid, gives a ~45-day float.

**T3 — Monthly company-store replenishment, 120-employee mechanical contractor**
- $2,000/month revenue.
- Costs: product $1,400; commonsku shop fee 2.5% ($50) [B, DH-S021]; kitting/shipping $70.
- **Contribution $480/month (24%).**

**T4 — Annual gear-allowance redemption store, 150 field/service employees × $150/year**
- $22,500/year revenue.
- Costs: product $16,200; store fee $563; individual pick/pack/ship $1,200.
- **Contribution ≈$4,537/year (20%).**
- Low percentage, but contracted, predictable and sticky.
- The allowance size is E. The OMG redemption fee of $0.99/order [D, E-WS16006-S017] is an alternative to the 2.5% commonsku fee.

**Failure risks per transaction:**
- **Reprints.** Decorators disclaim errors on customer-supplied files and defective garments [B, E-WS16006-S006], so the distributor eats the risk. One misprinted 150-piece order wipes out about three orders' profit.
- **Size-run errors.**
- **Late delivery** missing Safety Week.
- **Tariff price moves** between quote and PO.
- **Slow general contractors** (ASI reports terms "sometimes 120 days" [C, DH-S028]).

### 3.3 Repeat potential: recurring programs
| Program | Recurrence driver | Evidence | Design |
|---|---|---|---|
| New-hire crew kits | ~4.2%/month hires rate in construction | A, E-WS16006-S015 | Pre-packed size-run boxes held at the yard; auto-replenish at a reorder point |
| Seasonal refresh | Winter gear Sept–Oct; summer tees Apr–May | E | Calendar reminders from order history |
| Safety Week / stand-downs | Annual, fixed date (May 3–7, 2027) | C, E-WS16006-S019 | Book in February; invoice in April |
| Company store | Employees and managers reorder continuously | B, DH-S021 (fees) | Set up once logo files and size data exist (~month 6+) |
| Gear-allowance / redemption store | Annual employer budget per worker | D, E-WS16006-S017 | Budgets and points in the platform; the employer pays once a year or monthly |
| Safety-recognition awards | Quarterly or annual awards | A, E-WS16006-S018/S025/S026 | See §3.4 |

### 3.4 Safety-recognition programs: a compliance-aware design worth selling
- **OSHA:**
  - Programs that reward hazard or near-miss reporting and participation are "always permissible".
  - Prizes for injury-free periods are permissible only if they do not discourage reporting [A, E-WS16006-S018].
  - Employers may not discriminate against workers who report injuries [A, E-WS16006-S025].
- **IRS:** safety achievement awards of **tangible property** can be excluded from employee income up to $400 (non-qualified plan) or $1,600 (qualified plan). Gift cards and cash do not qualify [A, E-WS16006-S026].
- **The offer that follows:**
  - a recognition program built on leading indicators (reporting, training, toolbox talks);
  - tangible branded awards rather than gift cards;
  - fulfilled through a redemption store.
- **The pitch:** a better program with no tax surprise. The client's own tax adviser and counsel must confirm eligibility; we do not give tax or legal advice.

## 4. Validation
**Minimum viable offering:**
- a jobsite sample kit;
- a one-page offer sheet;
- a quote-in-24-hours promise;
- three products (safety tee, embroidered hoodie, cap) plus Safety Week items;
- 50% deposit;
- yard delivery.

**Experiments, ordered by information value per dollar:**

| # | Experiment | Cost | Success | Kill / pivot |
|---|---|---|---|---|
| **V0** | Desk basket test (started in §3.1): 20 baskets × 3 prices (4imprint, supplier list, landed public cost) | $0 | Identify the item classes that clear 30% at ≤1.15 × 4imprint | — (informs V1) |
| **V1** | **Incumbent-invoice benchmark:** 15 discovery interviews with safety or office managers from the §2.3 list, collecting the last two branded orders (vendor, items, quantity, unit price, problems) | $0 + ~20 h | ≥10 usable price points; median price paid ≥1.15 × 4imprint parity for the same items; ≥5 report a concrete pain (late, sizes wrong, reorder hassle) | Median ≤1.05 × 4imprint, or most buy from 4imprint/Amazon → stop |
| **V2** | **Real net-cost check:** register (LLC + IDOR REG-1), open SanMar and S&S accounts on card terms, request trade price lists from 2 Chicago decorators and Hightech Grafix; re-cost the V1 baskets | $0–$595 (PPAI only if suppliers require an industry number) + registration fees | ≥70% of V1 baskets beatable by ≥5% while keeping ≥30% landed GM | <40% of baskets → stop or narrow to hard goods/programs |
| V3 | 45-day outbound sprint to 120 permit-listed firms with a $300–400 sample kit; Safety Week pre-sell | ~$400 | ≥5 **paid** orders, average ≥$1,500, **realized** blended GM ≥30% on supplier invoices | ≤1 paid order, or realized GM <25% |
| V4 | Program pilot: new-hire kit program or company store with the 2 best V3 customers | $0–$300 | ≥$1,500/month combined after 90 days | <$500/month |
| V5 | Reorder check on V3 accounts at day 90–180 | $0 | ≥50% reorder | <25% |
| V6 | Union-label probe: quote union-label vs standard to 10 union subs | $0 | ≥3 accept a ≥10% premium | None care → drop the feature |

**Budget to the go/no-go:** about **$1,200–$1,600**: PPAI $595, samples ~$400, registration fees (LLC fee unverified), first-month insurance (quote MISSING). V1 and V0 cost nothing.

**Testable assumptions and where they sit in the model:**
- gross margin 30%/28% (V1, V2, V3);
- 30 conversations/month and a 25% quote win rate (V3);
- ARPC $650/month and 2.5% monthly churn (V4, V5);
- DSO 40 days (V3 invoices);
- DPO 15 days (V2 credit decisions).

**Supplier qualification steps:**
1. Request each decorator's distributor price list, minimums and turnaround.
2. Run a sample run of 12 pieces on our own logo.
3. Check rush policy, reprint policy and liability for its own errors.
4. Confirm union-label licence, if any.
5. Confirm ANSI garment handling (no logo over retroreflective tape).
6. Get freight time to Chicago.
7. Confirm the blank supplier will ship to that decorator.

**Customer interview plan:**
- 15 interviews: 5 electrical, 5 mechanical/plumbing, 3 GC, 2 association staff.
- 20 minutes each.
- Questions about *past* behaviour and spend only (materials, Q-section).
- Each interview should yield: vendor, unit prices, annual spend estimate, decision-maker, payment terms, union-label and ANSI needs.

**Conditions to invest more** (move to the $2–10k rungs):
- V1 + V2 pass;
- V3 delivers ≥5 paid orders at ≥30% realized GM.

**Conditions to abandon or pivot:**
- V1 median ≤1.05 × 4imprint;
- V2 <40% of baskets viable;
- V3 realized GM <25%.

**Pivot options:**
- programs only (Safety Week, recognition, allowance stores), where GM is less price-transparent;
- a different vertical where buyers do not benchmark against 4imprint.

## 5. Operations

### 5.1 Lead-to-cash workflow
| Step | What happens | Classification |
|---|---|---|
| 1 Prospect list | Permit API pull, de-duplicate, enrich with websites | Automatable (script) |
| 2 Outreach | Calls and emails to safety/office managers | Human (AI drafts) |
| 3 Discovery | Crew size, sizes, colours, logo, deadline, union/ANSI needs | Human |
| 4 Logo prep | Vectorise, digitise | AI-assisted plus decorator service (digitizing fee) |
| 5 Mockups | Supplier virtual samples and our own mockup tool | AI-assisted |
| 6 Quote | SAGE/commonsku quote using the pricing calculator (index vs 4imprint; GM floor) | AI-assisted |
| 7 Deposit invoice | Accounting system | Automatable |
| 8 Purchase orders | Blank PO to SanMar/S&S shipping to the decorator; decoration PO | Human (coordinator), templated |
| 9 Proof approval | Customer signs the proof (size run, placement, colours) | Human |
| 10 Production QA | Decorator; we inspect the first piece by photo | Supplier plus human |
| 11 Kitting and delivery | Sort by size and person; deliver to yard or jobsite | Human (founder, later part-time help) |
| 12 Balance invoice and collections | Net-30 reminders | Automatable |
| 13 Realized-margin check | Compare quote with actual supplier invoices per order | Automatable report; human review |
| 14 Reorder prompts | From size history and calendar (hires, seasons, Safety Week) | Automatable |
| 15 Tax filing, insurance, contracts | ROT returns, certificates | Professional-dependent (accountant) |
| Not automatable | Relationship selling, deadline rescue, quality judgement on garments | Human |

### 5.2 Fulfillment, support, QA and exceptions
- **Fulfillment:**
  - drop-ship to the customer for simple orders;
  - via the founder's garage or a small storage unit for kitting (cost not modelled; E);
  - company stores ship to individuals.
- **QA checklist on every order:**
  - logo version and colour;
  - size breakdown matches the roster;
  - ANSI garments: logo placement leaves the retroreflective tape and minimum background area untouched (confirm with each garment's labelling);
  - a count on arrival.
- **Exceptions:**
  - *Misprint:* claim against the decorator if it was the decorator's error (written policy needed); otherwise reprint at our cost.
  - *Late blanks:* substitute an equivalent style only with written approval.
  - *Price change after quote:* honour quotes within validity; re-quote after.
- **Support:** one shared inbox and phone. A 4-business-hour response promise.

### 5.3 Software stack (monthly)
| Tool | Cost | Evidence |
|---|---|---|
| PPAI incl. SAGE Workplace | $595/yr ≈ $50 | B, DH-S020 |
| commonsku Essentials (2 users, from coordinator hire) | $258 | B, DH-S021 |
| Company/redemption store (if not commonsku) | ~$119/store hosting; $0.99/redemption order | D, E-WS16006-S017 |
| AI assistant + mockup tools (ordinary pricing) | ~$60 | E |
| Accounting, e-sign, phone, website | ~$120 | E (prices not researched) |
| Insurance (GL + product liability) | $70–125 | E (no quote) |

### 5.4 Legal requirements (Illinois)
- **Business setup:** Illinois LLC (fee not verified; ilsos.gov unreachable 2026-11-28).
- **Tax registration:** IDOR REG-1 registration so the firm can buy for resale (CRT-61) and collect Retailers' Occupation Tax [A, WS16-S036].
- **Sales tax:** contractors buying apparel for workers are end users, so tax is charged. Chicago and home-rule rates and sourcing rules must be confirmed with IDOR or an accountant (MISSING).
- **Logos and customer terms:** the customer warrants that it owns the logo. Quote terms carry deposit, reprint and cancellation clauses.
- **Card surcharge:** legality in Illinois requires confirmation.
- **Union label:** only through licensed shops [C, E-WS16006-S024].
- **California shipments:** Prop 65 only for those.

### 5.5 Financial administration
- **Per-order job costing** (quote vs actual) is the core control, because the business lives or dies on realized GM.
- **Weekly:** AR aging; deposits received; supplier card balance.
- **Monthly:** ROT return.
- **Quarterly:** price-index review against 4imprint.
- **Credit:** extend net terms only after a credit check; slow general contractors go on deposit.

### 5.6 After December 2026
- The model includes AI at $60/month. Tripling AI and software cost reduces base year 3 to $65,683 (model stress). Nothing depends on unlimited AI.
- **Claude's work now:** templates, pricing calculator, prospect scripts and KPI sheet (materials file).
- **Afterwards:** a $20–60/month assistant drafts quotes and emails.
- **Fallback:** supplier tools (SAGE, commonsku) do quoting and mockups without AI.

## 6. Growth
- **First 10 customers (model months 3–8; 10 active accounts in month 8):** permit-list outbound, Safety Week pre-sell, and one introduction requested from every first customer.
- **First 100 (model month 45; 109 active at the end of year 4):**
  - company stores for the top 10;
  - association events;
  - suburban permit portals;
  - one outside rep.
- **Hiring sequence (model):**

| Hire | Trigger | Base month | Cost | Productivity |
|---|---|---|---|---|
| Account coordinator #1 | Monthly revenue ≥$35k | 21 | $4,800/month loaded (E) | ~$70k/month of orders each (E) |
| Outside rep #1 | Monthly revenue ≥$60k *and* founder pipeline full | 36 | $5,000/month (E; ASI median $75k [C, DH-S028]) | 1.5 new accounts/month after a 4-month ramp (E) |
| Coordinator #2 | Next $70k/month | Year 5 | as above | as above |
| Part-time kitting help | >10 stores | not modelled | ~$20/h (E) | — |

- **Rep economics are thin.** Reps commonly take 40–50% of gross profit [D, DH-S029; C, DH-S028]. A rep pays back in about 18–24 months at 30% GM (E). This is why the hire is gated.
- **Capacity limits:**
  - The founder alone handles about $35k/month of orders.
  - Each coordinator adds about $70k/month.
  - Sales capacity, not production, is the binding limit.
- **Geographic expansion:** suburban permits first, then Milwaukee and NW Indiana with the same playbook. Only after the Chicago account base reaches about 100.
- **Adjacent products:**
  - jobsite mesh banners and signage (4imprint sells these, so it is a commodity);
  - hard hats with logo;
  - uniform purchase programs for service techs, competing with rental (UniFirst [C, E-WS16006-S020]);
  - recruiting/job-fair kits;
  - recognition programs (§3.4).
- **Vertical integration:**
  - An in-house embroidery machine or DTF printer pays only when monthly outsourced decoration spend × savings rate × 12 is at least 1.0 × the capex plus operator cost.
  - Machine prices were not researched (MISSING). Evaluate at the year-3 checkpoint using actual decorator invoices.
  - The real return is control of rush jobs, not cost.
- **Management delegation:**
  - A coordinator runs order operations from about month 21.
  - An operations/account manager could run day-to-day at about $1.5M revenue (year 5+ in base; E).
  - The founder stays the main seller until two reps are productive.
- **Reinvestment slots:**
  1. working capital for growth (receivables are about 8% of revenue in the model);
  2. reps;
  3. a store platform;
  4. a second metro.
  Each needs the evidence gates in §8.

## 7. Financial analysis
All figures are quoted from `08_financial_models/WS16-006_results.json` (rebuilt 2026-11-28). Operating profit is EBITDA-basis, before owner pay. Draw: $4,000/month from month 13. Tax: 30%.

### 7.1 Launch capital and working capital
- **Start capital in the model:** $39,200, the smallest injection that keeps base cash ≥ 0.
- **Capex:** $2,000 base in month 1 (laptop, sample display, registration).
- **Working capital:** DSO 40 days vs DPO 15 days and 3 inventory days. Net working capital is $65,361 at the end of year 3 and $125,743 at the end of year 5 (base, engine). This is the main use of growth cash.

### 7.2 First 24 months (base, monthly)
| Month | Revenue | Gross profit | Op. profit | Cum. retained | Cash |
|---|---|---|---|---|---|
| 1 | 0 | 0 | −1,270 | −3,270 | 35,930 |
| 2 | 0 | 0 | −1,270 | −4,540 | 34,660 |
| 3 | 1,575 | 448 | −953 | −7,142 | 32,058 |
| 4 | 3,483 | 995 | −548 | −9,689 | 29,511 |
| 5 | 5,718 | 1,640 | −58 | −12,091 | 27,109 |
| 6 | 8,276 | 2,381 | 517 | −14,258 | 24,942 |
| 7 | 11,152 | 3,218 | 1,175 | −16,101 | 23,099 |
| 8 | 14,341 | 4,149 | 1,916 | −17,534 | 21,666 |
| 9 | 16,263 | 4,724 | 2,419 | −17,718 | 21,482 |
| 10 | 18,157 | 5,290 | 2,915 | −17,671 | 21,529 |
| 11 | 20,022 | 5,849 | 3,404 | −17,253 | 21,947 |
| 12 | 21,859 | 6,398 | 3,885 | −16,468 | 22,732 |
| 13 (draw starts) | 24,379 | 7,148 | 4,248 | −18,946 | 20,254 |
| 14 | 26,215 | 7,697 | 4,729 | −20,369 | 18,831 |
| 15 | 28,023 | 8,239 | 5,203 | −21,431 | 17,769 |
| 16 | 29,804 | 8,772 | 5,669 | −22,139 | 17,061 |
| 17 | 31,559 | 9,297 | 6,129 | −22,496 | 16,704 |
| 18 | 33,287 | 9,814 | 6,582 | −22,508 | 16,692 |
| 19 | 34,989 | 10,323 | 7,028 | −22,181 | 17,019 |
| 20 | 36,666 | 10,825 | 7,468 | −21,519 | 17,681 |
| 21 (coordinator) | 38,318 | 11,319 | 2,957 | −23,989 | 15,211 |
| 22 | 39,945 | 11,806 | 3,383 | −26,134 | 13,066 |
| 23 | 41,547 | 12,286 | 3,803 | −27,959 | 11,241 |
| 24 | 43,126 | 12,758 | 4,216 | −29,470 | 9,730 |

- **Conservative:** cumulative retained is −$25,838 at month 12 and −$83,124 at month 24. Cash goes negative from month 15.

### 7.3 Five-year view
| | Y1 | Y2 | Y3 | Y4 | Y5 |
|---|---|---|---|---|---|
| **Base revenue** | 120,844 | 407,857 | 651,321 | 953,900 | 1,305,941 |
| Base gross profit | 35,091 | 120,284 | 193,087 | 282,877 | 387,906 |
| **Base op. profit** | 12,134 | 61,415 | 78,108 | 92,227 | 141,481 |
| Base FCF (before draw) | −16,468 | 34,998 | 49,068 | 46,854 | 85,160 |
| Base retained after draw | −16,468 | −13,002 | 1,068 | −1,146 | 37,160 |
| Base active accounts (year end) | 21.4 | 51.0 | 75.7 | 109.0 | 140.7 |
| **Conservative op. profit** | −11,282 | 3,700 | 18,914 | 31,017 | 40,771 |
| Conservative revenue | 29,535 | 131,020 | 209,104 | 271,744 | 322,743 |
| **Optimistic op. profit** | 45,056 | 161,632 | 313,332 | 563,881 | 800,927 |
| Optimistic revenue | 263,691 | 963,768 | 1,922,637 | 3,024,943 | 4,075,768 |

**Breakeven, funding and payback:**

| Measure | Base | Conservative | Optimistic |
|---|---|---|---|
| Operating breakeven month | 6 | 16 | 4 |
| Peak funding need, with draw | $39,105 (month 41) | $161,983 (month 60, still falling) | $6,982 |
| Peak funding need, no draw | $17,718 | $35,722 | — |
| Payback month | 58 | never within 60 months | — |

- **Base Y3 op / peak funding:** 1.997.
- **Conservative is a "good job" at best:** the business pays the founder less than $4,000/month for five years.
- **Optimistic is an upper bound, not a plan.** It needs 2 productive reps and 341 accounts by year 5.

### 7.4 Sensitivity (base, each driver ×0.75 / ×1.25)
| Driver | Year-3 op. profit range | Peak funding range |
|---|---|---|
| Gross margin | $37,917 – $118,300 | $141,603 – $16,649 |
| Labour cost | $94,712 – $61,505 | $27,614 – $68,668 |
| Leads or win rate | $52,657 – $84,466 | $39,808 – $46,792 |
| Recurring spend per account | $53,003 – $82,898 | $38,633 – $46,592 |
| DSO | year 3 unaffected | $16,921 – $65,810 |

Gross margin dominates.

### 7.5 Stress tests (base)
| Stress | Y3 op. profit | Y5 op. profit | Peak funding |
|---|---|---|---|
| Gross margin −5 pts | 45,542 | 76,184 | 110,393 |
| Gross margin −10 pts | 12,976 | 10,887 | 273,585 |
| Key supplier refuses (3-month delay, −5 pts) | 39,406 | 79,234 | 126,736 |
| Customers pay 30 days later | 78,108 | 141,481 | 126,770 |
| Recession (new −30%, churn ×1.5) | 72,833 | 56,883 | 37,088 |
| Competitor response (−3 pts, churn ×1.3, no price growth) | 48,125 | 60,041 | 69,015 |
| Hires needed 30% sooner | 35,491 | 71,778 | 175,708 |
| Win rate 40% below plan | 68,831 | 78,496 | 41,152 |
| Growth takes twice as long | 51,175 | 38,180 | 62,503 |
| AI/software ×3 | 65,683 | 128,299 | 64,847 |

- **The recession case keeps year 3 high only because hiring is delayed.** Year 5 is the honest damage.
- **Downside cases above $100k peak funding:**
  - GM −5 or −10 pts;
  - supplier refusal;
  - +30 days DSO;
  - early hiring.
- **Each has a cheap early warning (§11).**

### 7.6 Profit milestones and capital accumulation
**Profit milestones:**

| Milestone | Base | Optimistic |
|---|---|---|
| First month with op. profit ≥$1k | 7 | — |
| ≥$5k/month | 15 | — |
| ≥$10k/month | 47 | 14 |
| ≥$25k/month | never within 60 months | 30 |

- **Annual milestones (base):** about $100k/yr operating profit is reached in year 5 ($141,481). $250k/yr is not reached within 10 years in base (year 10 op $188,666).

**Capital accumulation to year 10 (base):**
- Cumulative deployable surplus after reserves and reinvestment: **$248,008**. It starts in year 6 ($33,377).
- Year-10 enterprise value at 2.5×: $471,665.
- Owner draws over 10 years: $454,484.
- **Conservative:** no deployable surplus; year-10 EV $66,405.
- **Optimistic:** $3,391,433 deployable.

**Long-term drivers:**

| Driver | Conservative | Base | Optimistic | Basis |
|---|---|---|---|---|
| Year-6 growth | 3% | 8% | 12% | Industry +1.3% to +4.2% [C, E-WS16006-S008; C9-S012] |
| Decay | 0.7 | 0.85 | 0.9 | — |
| Incremental ROIC | 0.35 | 0.6 | 0.9 | Mostly receivables |
| Maintenance capex (% of op. profit) | 5% | 3% | 2% | — |
| Reserve (months of cash costs) | 3 | 2 | 1.5 | — |
| EV multiple | 1.5× | 2.5× | 3.0× | E: no completed-sale multiple found; promo books are less sticky than insurance books at 5–7× [C, C5-S021] |

### 7.7 Owner distributions and downside
- In base, free cash flow first covers the $4,000/month draw in year 3 ($49,068 FCF vs $48,000 draw); in year 2 the draw exceeds FCF by $13,002. Retained cash then hovers around zero until year 5, because growth absorbs it.
- Real distributable surplus beyond the draw begins in year 6.
- **Downside:** in the conservative case the draw is not earned. In the GM −10 pt case, peak funding exceeds $270k. Both are prevented by the V1–V3 gates and by stopping early.

## 8. Capital deployment ladder
| Rung | What it buys | Evidence gate before spending | How it could be lost |
|---|---|---|---|
| $0–500 | V0 desk baskets; V1 interviews; target list; REG-1 filing (no fee found) | None | Founder time only |
| $500–2k | LLC; PPAI $595; sample kit ~$400; first insurance month | V1: median incumbent price ≥1.15 × 4imprint; ≥5 pains | Memberships wasted if suppliers or customers fail |
| $2–5k | Supplier card float for the first 3–5 orders; mockup tools; one association event | V2: ≥70% of baskets at ≥30% landed GM | A misprint or a customer default on the first orders |
| $5–10k | Receivable float for ~10 accounts (~$9–10k net working capital) | V3: ≥5 paid orders at ≥30% realized GM | Slow payers; GM leakage on first orders |
| $10–25k | Working capital for 25–50 accounts; commonsku; store pilots | V4/V5: ≥$1,500/month program revenue; ≥50% reorder | Programs that don't reorder; tariff price jumps inside stores |
| $25–50k | Coordinator at $35k/month revenue plus the draw bridge (base peak $39,105) | 6 months of revenue ≥$30k/month with realized GM ≥30% | Hiring ahead of revenue (stress: hires 30% sooner → $175,708 peak) |
| $50–100k | First rep, second coordinator, suburban expansion | Founder sustaining ≥3 new accounts/month; revenue ≥$60k/month; DSO ≤45 | Rep doesn't produce (the ungated Stage D case gives conservative peak $417,290) |

## 9. Strategic wealth creation
- **How it becomes a durable cash asset.** Through embedded programs (kits, stores, allowances, recognition) in a dense cluster of trade contractors. Size records, logo files and reorder calendars raise switching costs. GC approved-vendor status pulls in subcontractors.
- **None of this is proprietary.** "Tens of thousands" of distributors could copy it [C, C9-S012].
- **How much capital it could generate:**
  - Base: about $78–141k/yr operating profit in years 3–5 and $189k in year 10.
  - Cumulative deployable surplus of about $248k by year 10, after a $4,000/month owner draw.
  - Conservative: nothing deployable.
- **When management could take over:**
  - day-to-day operations around year 5 in base;
  - selling only once two reps are productive.
- **Can it fund other ventures?** Modestly, from year 6, at about $33–64k/yr deployable in base.
- **Is it a strong first company for a diversified portfolio?** **Not as the primary engine.**
  - **For:** it is the cheapest, fastest finalist to test, and it is legal and licence-free. It builds sales skill and a contractor network that adjacent Atlas ideas sell into (WS13-014 utility locating, SYN-006 construction back office).
  - **Against:** the ceiling is a $100–200k/yr distributorship; profit is hostage to price-transparent margins; and owner time is the constraint (G7 WARN).
- **Best use:** a validation-stage parallel bet, or a cash-flow bridge alongside a higher-ceiling finalist, unless V1–V3 come back strongly.

## 10. Execution plan

### First 7 days (Dec 1–7, 2026; heavy AI available only until Dec 5)
**Founder:**
- Answer F1–F7 (age, credit, location, hours, $100k terms, network). A personal guaranty for supplier credit depends on F2.
- Choose to run V0/V1.
- Block 6 hours for calls.

**Claude prepares (by Dec 5):**
- the item-level price benchmark table (§3.1) extended to 20 baskets;
- the pricing-calculator spec and the interview questionnaire (materials);
- a call list of the top 40 permit prospects with main-line numbers taken from their own sites;
- supplier inquiry drafts.

**Founder spend:** $0.

### First 30 days (December 2026)
**Founder:**
- Run 15 V1 interviews. Prospects: Sherman Mechanical, CT Mechanical, Chi-Town Plumbers, REX Electric, CSL Climate Control, Toro Construction, Redmond Construction, Battaglia, Air Comfort, Chicago Area Plumbing, R. Carrozza, Mirex, All-Bry; staff at MCA Chicago and Chicagoland AGC.
- File the LLC and IDOR REG-1.
- Open SanMar and S&S accounts on card terms.
- Send inquiry emails to Hightech Grafix, Chicago Printing & Embroidery/4Logoz, All-Secure Graphics and Minuteman Press Chicago.

**Questions:** who supplies you now; last two orders (items, quantity, unit price); what went wrong; who approves; payment terms; union-label or ANSI requirements on your sites; your Safety Week plans.

**Evidence required:** ≥10 incumbent price points; ≥3 decorator trade price lists; SanMar/S&S net prices for G500, G18500, Richardson 112 and CS401.

**Spend:** up to ~$800 (registration fees, optional PPAI).

**Accept a first order only if:**
- the deposit has been received;
- the proof is signed;
- supplier and decorator net prices are confirmed in writing;
- the order's GM is ≥28%;
- the deadline leaves ≥3 business days of buffer.

**Abandon if:** V1 median ≤1.05 × 4imprint, or V2 shows <40% of baskets viable.

### First 90 days (Dec 2026 – Feb 2027)
- **V3 sprint (January–February):** 120 firms, sample kit, Safety Week pre-sell.
- **Targets:**
  - ≥5 paid orders;
  - realized GM ≥30% on supplier invoices;
  - ≥3 Safety Week bookings by April 1, 2027.
- **Deliverables:** a job-costing sheet for every order; weekly KPI sheet (materials).
- **Slow branch:** 2–4 orders → extend 30 days and switch the offer to Safety Week/programs only.
- **Failure branch:** ≤1 order, or GM <25% → stop and keep the materials.

### First year (to Dec 2027)
**Milestones (base model):**
- 5 active accounts by month 7 and 10 by month 8 (model);
- about 21 active accounts and about $22k monthly revenue by month 12 (model: 21.4 accounts; $21,859);
- two company stores or kit programs live by month 9;
- coordinator only when revenue is ≥$35k/month (base month 21, i.e., year 2).

**Slow-growth branch:** fewer than 10 accounts at month 6 → run it as a side business with programs only, no hires; decide by month 9.

**Failure branch:** realized GM below 27% for two consecutive months, or DSO above 55 days → stop new acquisition and fix pricing and terms; exit if not fixed in 60 days.

## 11. Pre-mortem
| Failure | How it happens | Early warning | Cheap preventive test |
|---|---|---|---|
| **Lost $5k** | PPAI, samples and 3 months of outreach produce under 3 orders; contractors are happy with a local shop or 4imprint | <2 quotes per 10 conversations; V1 shows prices near 4imprint | V1 before any spend |
| **Lost $25k** | Two large invoices default, or a 300-piece misprint is re-run at our cost | Customers asking for net-60; vague proofs | Deposits, signed proofs, decorator reprint policy in writing (V2) |
| **Lost $50k** | Coordinator and rep hired ahead of demand while tariffs and price-matching cut 5 pts | GM <28% for 2 months; new accounts <2/month | Hiring gates (§8); quarterly price index |
| **Revenue but no profit** | Selling ANSI tees and embroidered brand items at 4imprint prices (−12% to +10% GM, §3.1) | Order-level realized GM report | Merchandising rule; no hi-vis quotes before net cost is known |
| **Exhausting low-paid job** | The founder does sales, proofs, kitting and delivery for <$4k/month (conservative case) | Founder hours >55/week at <$25k/month revenue | Decide at month 9; programs-only mode |
| **Cash crunch** | Card-prepaid suppliers vs net-30/60 general contractors (+30 days DSO → peak $126,770) | DSO >45; card balance >2× deposits | Deposits; card-on-file; no net-60 without supplier credit |
| **Can't run without founder** | All relationships and quoting judgement sit with the founder | Coordinator cannot quote unaided by month 30 | SOP library; pricing calculator with GM floors |
| **No deployable surplus** | Growth working capital and the draw absorb all FCF (base: none deployable until year 6) | Retained cash ≤0 in year 3 | Don't scale reps until DSO ≤40 and GM ≥30% |

## 12. Required confirmations (direct, by the founder)
**Suppliers:**
- SanMar and S&S distributor net prices and case breaks for G500, G18500, Richardson 112 and CS401/CS204 hi-vis;
- card vs Net-30 terms, and whether a personal guaranty is required [B, DH-S024];
- whether a PPAI/SAGE number is accepted in place of ASI;
- decorator trade price lists (24/48/72/144 pieces), minimums, rush and reprint liability, freight time to Chicago, Hightech Grafix's location;
- union-label licence for garments (Minuteman Press Chicago; the Allied directory);
- hard-goods net prices for an 18-oz engraved tumbler.

**Customers:**
- current vendors and unit prices;
- annual branded spend and budget owner (safety vs HR/marketing);
- payment terms and approved-vendor onboarding;
- site requirements for ANSI class and logo placement;
- interest in kits, stores and allowance programs;
- Safety Week plans for May 3–7, 2027.

**Regulatory:**
- Illinois LLC fee and annual report;
- IDOR REG-1 timing;
- Chicago/Cook/home-rule rates and sourcing for delivered goods;
- legality of card surcharges;
- ANSI/ISEA 107 decoration rules from garment makers;
- country rates and CAFTA-DR treatment in Federal Register notice 2026-15181.

**Insurance:**
- general and product-liability quote, including coverage for misdecorated PPE;
- whether customers require certificates or additional-insured status.

**Tax and legal for clients' programs:**
- the client's adviser confirms achievement-award treatment [A, E-WS16006-S026] and incentive design [A, E-WS16006-S018];
- we do not advise on either.
