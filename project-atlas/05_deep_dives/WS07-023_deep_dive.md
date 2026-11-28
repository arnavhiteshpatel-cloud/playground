# WS07-023 — Online consignment auctions for business liquidations: Stage D commercial deep dive

> **Verdict: DROP.** Keep only as a possible later add-on for an operating business that already sees distressed assets.
>
> - **Revised evidence level:** D. Supply counts, licensing rules and platform fees are A–B. Average hammer and win rates are E.
> - **Model base case, year 3:** revenue $220k; operating profit **$6k** before founder pay.
>   - Founder alone, with no second licensee, year 3 is $60k.
>   - Year 5 is $47k.
>   - Conservative case −$87k; optimistic $290k (needs a $30k average hammer and twice the deal flow).
> - **Decisive fact:** small closings are too small to pay for staff.
>   - Even a 25% combined take (15% buyer's premium plus 10% seller commission), above incumbents' 9.8–18.6% of GMV [A, C9-S033], earns only ~$2.9k of contribution on an $18k sale.
>   - Meanwhile, Illinois's new online-auction licensing is pulling in entrants: **137 new individual auctioneer licences in 2026 vs 23–49 a year in 2019–2024** [A, DH-S003].
>   - A national specialist already serves Chicago restaurant closings at a 15% buyer's premium [B, DH-S010].

## 1. Specific initial niche
- **Service:** timed online consignment auctions (on HiBid) for closing or relocating restaurants, bakeries, small light-industrial shops and office move-outs.
- **Size and geography:** $5k–$50k hammer sales in Chicago and inner Cook and DuPage suburbs.
- **Sources:**
  - Chapter 7 panel trustees;
  - commercial landlords and property managers;
  - SBA/commercial lenders' special-assets groups;
  - used-equipment dealers' overflow.
- **Execution:** catalogued on site, 7–10-day timed sale, supervised buyer pickup, settlement from a special (escrow) account.

**Supply evidence:**
- **Chicago restaurant closures:** inspectors recorded **883** restaurants as "Out of Business" in 2025, 665 of them Risk 1 (full kitchens) [A, DH-S001]. The 2026 count is 562 through November 25.
- **N.D. Illinois business bankruptcies:** **789** filings in the 12 months to 2026-06-30, up 3.5%, including **558 Chapter 7** (up from 504) [A, DH-S006].
- **Panel trustees:** 25 Chapter 7 panel trustees serve the district [A, DH-S004].
- **Not measured:** how many closings own equipment worth auctioning (versus leased, landlord-liened or dealer-bought assets).

## 2. Named operators

| Operator | What is known | Basis |
|---|---|---|
| **Liquidity Services** (GovDeals, AllSurplus, Capital Assets Group) | FY2026 GMV $1.645B. Take rate: GovDeals 9.8%, CAG 18.6% of GMV. Consignment segments keep 85–95% of revenue as direct profit; consignment was 86% of Q4 GMV | A, C9-S033 / WS07-S036 |
| **TAGeX Brands – RestaurantEquipment.Bid** (national) | Runs Chicago closings (Over/Under Sports Bar, Lincoln Park, Feb 2026; Lawry's, 2021). **15% buyer's premium** on every transaction; card/PayPal only; $1 starts; no shipping | B, DH-S010 |
| **Heath Industrial Auction Services** (Hoffman Estates) | Licensed IL auction firm since 2011; "Asset Conversion Specialists Since 1985"; industrial auctions and appraisals for businesses, banks, estates | A, DH-S003; D, DH-S012 |
| **Hyper Group (formerly HyperAMS)** (Rolling Meadows) | Licensed firm; valuation and monetization for lenders and restructuring professionals; 16 years | A, DH-S003; D, DH-S013 |
| **Machine Tool Bids** (Chicago); **Perfection Global** (Elk Grove Village); **Premier Asset Recovery Group** (Prospect Heights) | Active licensed auction firms in machinery and asset recovery | A, DH-S003 |
| **Taylor Auction & Realty** (Chicago, on HiBid) | Bi-weekly tool and surplus liquidation sales | B, DH-S011 |
| **Surplus Depot** (Aurora), **Ironcrest Asset Group** (Chicago) | **Newly licensed in 2026** (2026-07-09, 2026-02-24). Evidence of entry under the new regime | A, DH-S003 |
| **Illinois market overall** | 1,064 active individual auctioneers and 231 firms (38 firms in Cook). Typical HiBid buyer's premiums 10–23% | A, DH-S003; B, DH-S011 |

**Substitutes:**
- used-equipment dealers buying outright, e.g. Gator Chef (Lisle) and City Food Equipment [D, DH-S014];
- Facebook Marketplace;
- landlords simply clearing premises.

## 3. Suppliers and partners
Full detail is in `09_databases/suppliers/WS07-023_suppliers.csv`.

- **HiBid via AuctionFlex 360 — documented [B, DH-S007]:**
  - 2% auction fee; the base of the 2% is not stated.
  - $0.25 per unique bid, capped at $150 per auction. HiBid's help centre says a $75 cap; the discrepancy is kept.
  - AuctionFlex 360 software: Solo $95/month, Team $145/month.
  - HiBid "reserves the right" to add fees for select auctioneers.
- **LiveAuctioneers (ATG) — documented [B, DH-S008]:**
  - Timed sales: $25–275 per event plus 5% commission.
  - Card processing 3.99% + $0.25.
  - Poor category fit for restaurant and industrial lots.
- **BidSpotter (ATG) — assumed.** The fee page errored. ATG's group take rate is 4.8% [C, DH-S009].
- **Proxibid — assumed.** The site is blocked. Only LiveAuctioneers' cross-listing fees are known [B, DH-S008].
- **Auction Mobility — assumed.** The site is blocked; pricing is believed to be quote-based (E).
- **IDFPR licensing — documented [A, C9-S030; DH-S015].**
- **U.S. Trustee Region 11 auctioneer bonding questionnaire — documented [A, DH-S005].** The premium is MISSING.

## 4. Named prospects and referral partners
**28 Illinois organizations** are listed in `09_databases/prospects/WS07-023_prospects.csv`. All are "prospect — not contacted".

- **Law and advisory firms hosting the N.D. Ill. Chapter 7 panel trustees (14)** [A, DH-S004]:
  - Crane Simon Clar & Goodman;
  - Cohen & Krol;
  - Gutnicki;
  - Moglia Advisors;
  - Smith Gambrell & Russell;
  - Taft;
  - Nixon Peabody;
  - Seyfarth Shaw;
  - Jenner & Block;
  - Fox Swibel;
  - Springer Brown;
  - Kokoszka & Janczur;
  - Chill Chill & Radtke;
  - Barrick Switzer.

  Individual trustees' contact details are deliberately not recorded.
- **Associations:** TMA Chicago/Midwest; Illinois Restaurant Association.
- **Landlords and property managers:** Inland Real Estate Group; Sterling Bay; Bradford Allen.
- **Lenders:** Byline Bank; Wintrust.
- **Equipment dealers (buyers and overflow sources):**
  - Gator Chef;
  - City Food Equipment;
  - Rong City Restaurant Equipment Supply;
  - Alliance Paper & Foodservice Equipment;
  - Midwest Restaurant Equipment Supply (Foremost).

  The last three come from Chicago licence records [A, DH-S002].
- **Larger licensed firms as possible overflow partners:** Hyper Group; Heath Industrial.

## 5. Representative transactions

| # | Sale | Hammer | Revenue | Direct costs | Contribution | Cash timing |
|---|---|---|---|---|---|---|
| T1 | Closing 60-seat Chicago restaurant, ~180 lots, lease ending | $18,000 | $4,500 (15% BP $2,700 + 10% commission $1,800) | HiBid ~$510; card fees absorbed ~$310; load-out crew $500; ads/van $270 | **$2,910 (65%)** | Buyers pay in 2–3 days; seller paid from special account in ~10–14 days |
| T2 | Trustee-retained Chapter 7 small machine shop | $40,000 | $6,000 (15% BP; no seller commission) | HiBid ~$950; processing $300; rigging/forklift $1,200; bond + ads $350 | **$3,200 (53%)** | Court approval of retention and fees; slower |
| T3 | Office move-out (furniture, IT), Schaumburg | $6,000 | $1,500 | HiBid $200; card $105; crew $400; ads/van $150 | **$645 (43%)** | As T1 |

- **Where the fees come from:** HiBid fees [B, DH-S007] and the 15% buyer's premium [B, DH-S010] are documented. The seller commission, hammer values and crew costs are E.
- **What T3 shows:** without a **minimum fee** (proposed $750), sales under about $8k do not cover the founder's 2–3 days on site.

## 6. Customer acquisition
**Customer #1:**
- Do not pitch first-time closers cold.
- Approach landlords and property managers with abandoned FF&E (furniture, fixtures and equipment) clean-outs, and equipment dealers with closings they decline to buy.
- Offer a free written valuation and a 21-day "keys back" guarantee.
- Alternatively, work one sale as hired help for a licensed auctioneer before licensing (see V3).

**Customers #2–10:**
- Introduce the firm, with its bond, to the 25 panel trustees through TMA and bankruptcy-bar events.
- Trustees retain auctioneers repeatedly, but each needs court approval and most have incumbents.
- Restaurant-broker and landlord referrals.

**Customers #11–100:**
- Build a HiBid follower and buyer list; higher bidder density raises hammer prices, which attracts sellers.
- Search capture for "restaurant liquidation Chicago".
- Lender special-assets groups (Byline Bank, Wintrust).

**Funnel (E):**

| Stage | Monthly volume |
|---|---|
| Qualified consignment inquiries | 9 |
| Site visit and proposal (60%) | ~5.4 |
| Signed (40%) | ~2.2 sales |

- **Referral and repeat:** 2.5 new sales per 100 relationship records per month.
- **Model output:** 7 sales in year 1, 31 in year 2, 47 in year 3.
- **CAC:** ~$250 cash per sale plus ~6 founder hours of selling.
- **LTV:** a typical closing seller is a one-time customer (~$2.9k contribution). Value sits in **referral partners**: a trustee or landlord sending 3–4 sales a year is worth ~$10k a year of contribution.

**Weekly human work:** at 2–3 sales a month, about 20 hours on site plus 10 hours selling and settlement.

## 7. Pricing strategy
- **Buyer's premium:** 15%, matching TAGeX [B] and within the Illinois HiBid range of 10–23% [B, DH-S011].
- **Card fee to buyers:** 3–3.5% where lawful. HiBid sellers commonly add one [B, DH-S011]; requires confirmation.
- **Seller commission:**
  - 0–5% on trustee or lender sales over $25k, which must be competitive and court-approved;
  - 10% on standard closings;
  - 20–25% plus a $750 minimum on sales under $8k.
- **Pass-through charges:** rigging, forklift and dumpster costs pass through at cost.
- **Benchmarks:** incumbents' all-in take is 9.8–18.6% of GMV [A, C9-S033], so a 25% combined take is at the top of the market. The base model may be generous.

## 8. Working capital and cash conversion cycle
- **How cash moves:**
  - Buyers pay before pickup [B, DH-S010].
  - Premium and commission are deducted from the proceeds held in the **special account**, which IDFPR may audit [A, C9-S030].
  - Remitting to sellers is a trust obligation; the float is *not* operating cash.
- **Cycle:** DSO ≈ 5 days and DPO ≈ 15 days, so the cash conversion cycle is ≈ −10 days and net working capital is about zero at any scale.
- **Model results:** peak funding is **$32k** including a $3k/month owner draw, or **$16k** without it.

| Annual sales | Cash need |
|---|---|
| 10 | ~$1–2k of crew wages and van rental fronted per concurrent sale |
| 50 | ~$5k fronted; storage bay ~$350/month |
| 200 | ~$15–20k fronted; a staff payroll float becomes the binding need |

## 9. Regulatory path
1. **Individual auctioneer licence (IDFPR)** [A, C9-S030]:
   - PSI exam (fee MISSING);
   - **$200** application;
   - high school diploma or GED;
   - personal history disclosures;
   - 45-day permit sponsor card (self-sponsorship allowed);
   - consent to audit special accounts.
2. **Auction firm registration:** **$100** plus a named licensed managing auctioneer [A]. A licensed employee or partner can fill this role.
3. **Continuing education:** a 2026 CE fact sheet exists (hours MISSING) [A, DH-S015].
4. **P.A. 104-0145 (effective 2026-01-01)** makes online auctions licensed activity. The conditional exemptions could not be read: ilga.gov returned 503/TLS errors, and FindLaw's text is current only to 2025-01-01 [C, C9-S032; DH-S015].
5. **Sunset:** the Act is scheduled for repeal on 2030-01-01, so rules may change [C, C9-S032].
6. **Bankruptcy work:** court-approved employment (11 U.S.C. §327, general knowledge) and bonding per the USTP Region 11 questionnaire [A, DH-S005].
7. **Sales tax:** Illinois Retailers' Occupation Tax treatment of auction sales and of the auctioneer as agent is MISSING; requires confirmation with IDOR.
8. **Title and liens:** run an Illinois Secretary of State UCC lien search before each sale (fee MISSING).
9. **Insurance (E, no quotes):**
   - general liability;
   - bailee/inland marine;
   - auto;
   - workers' compensation once crew are on payroll.

   Indicative total: ~$200–400/month.

**Time to first sale:** 3–5 months (E).

## 10. Operations workflow
1. Inquiry and referral.
2. Site visit with lot count, lien/UCC check, and removal deadline from the lease.
3. Consignment contract covering commission, minimum fee, no-reserve policy and pickup date.
4. Cataloguing: photographs, then AI-drafted titles and descriptions and comps from past HiBid results.
5. HiBid listing for 7–10 days, plus an email blast to the buyer list.
6. Close; AuctionFlex invoices and collects.
7. Pickup days: ID checks and supervised load-out, with forklift where needed.
8. Unpaid lots re-offered.
9. Settlement statement and remittance from the special account.
10. Clean-out upsell.

**Human vs automated:**
- **Human:** site work, photography, pickups, seller hand-holding.
- **AI-assisted:** listings, valuations and buyer outreach.
- **Automated:** invoicing and notices.

**Software:** AuctionFlex 360 at $95–145/month [B]; AI tools about $80/month; website, phone and books about $120/month. An AI-cost ×3 stress is survivable.

## 11. Competitive position and defensibility
**What accumulates:**
- buyer-list density (bidders per lot, which drives hammer);
- trustee and landlord relationships;
- a track record of net proceeds;
- licensed and bonded status.

**Why this is weak:**
- **Licensing is a low barrier,** and the new rule is *adding* licensees: 137 new individuals and 34 new firms in 2026 alone [A, DH-S003].
- **National specialists** such as TAGeX and established local firms (Heath since 1985, Hyper Group) already hold the referral channels for larger assets.
- **Dealers** absorb restaurant equipment by buying outright.
- **Sellers have no switching cost,** and closers are one-time customers.

**Delegation:**
- Firm registration requires a licensed managing auctioneer.
- A second licensee costing about $66k a year does not pay for itself in the base case. At 1.5 sales a month × $2.9k contribution = $4.4k/month, against a $5.5k/month cost.

## 12. Key risks and pre-mortem
**How the money is lost:**
- **$5k lost.** Licence, kit, trailer and website are done, but only 3–4 small sales happen in 6 months (average hammer under $8k). Dealers and TAGeX took the restaurant closings.
- **$25k lost.** The founder hires a cataloguer and leases storage on the strength of a few good months. Flow is lumpy, and the "hires needed 30% sooner" stress shows year 3 at −$25k. A load-out injury or damaged-premises claim adds to the loss.
- **$50k lost.** A second licensee, storage and a rented van run through a recession-year supply glut, with lower recovery rates — an effect Liquidity Services flagged in Q4 [A, WS07-S036]. Misdescription disputes and chargebacks follow, then a licensing complaint.

**Early-warning indicators:**
- fewer than 2 signed consignments a month by month 9;
- average hammer below $10k;
- zero trustee retentions after 6 months of outreach;
- fewer than 15 bidders per sale;
- unpaid-lot rate above 8%.

**Model stress results (base year 3):**

| Stress | Year-3 operating profit |
|---|---|
| Win rate −40% | −$21k |
| Founder capacity −40% | −$33k |
| Recession | −$19k |

## 13. Validation plan

| # | Experiment | Cost | Success | Kill |
|---|---|---|---|---|
| V1 | Desk audit: track every Chicago-area business-liquidation sale on HiBid and RestaurantEquipment.Bid for 60 days (lots, premiums, closing prices where visible) | $0 | ≥8 sales/month in the niche, with a median hammer ≥$12k visible | <4/month or median <$8k |
| V2 | Referral-source interviews: 10 landlords/property managers, 5 dealers, 3 trustees' offices — *after* the founder decides to proceed | ~$150 | ≥3 say they would refer within 90 days, at named sale sizes | No referrals at any size |
| V3 | Work two sales as paid hired help for a licensed Illinois auctioneer to observe real hammer, labour hours and premiums (legality of unlicensed assistance to be confirmed) | ~$300 travel | Observed contribution ≥$3k/sale at ≤40 labour hours | <$1.5k/sale |
| V4 | Only then: licence ($200 + exam) and firm ($100); first 3 own sales with a $750 minimum fee | ~$1.5k incl. kit | ≥3 paid sales in 90 days, average revenue ≥$3k | <2 sales |

## 14. Revised scores and verdict

| Criterion | Stage C | Stage D | Reason |
|---|---|---|---|
| fcf | 4 | **3** | Base year 3 $6k with staff, ~$60k founder-only; year 5 $47k |
| roic | 7 | **6** | Low capital ($16–32k), but conservative losses are large |
| access | 5 | **4** | Referral sources are named, but trustees have incumbents, closers are one-time, and dealers buy outright |
| scale | 5 | **3** | Δ−2: unit contribution (~$2.9k/sale) cannot fund catalogue staff plus a second licensee; local pickup radius |
| resilience | 6 | 6 | Counter-cyclical supply; recovery rates fall in gluts |
| entry | 4 | **3** | 137 new licensees in 2026; national 15%-premium specialist present |
| delegation | 6 | **4** | Δ−2: needs a licensed managing auctioneer; second licensee uneconomic in base; on-site work |
| cash | 8 | 8 | Buyer-prepaid; escrow is not float |
| feasibility | 6 | 6 | Licence obtainable; exemption text MISSING; sunset 2030 |
| ai | 5 | 5 | Listing and comps automation is real but small relative to on-site labour |

- **Raw score:** about 4.45 (Stage C was 5.40). Evidence-adjusted (D, k=0.70): about **4.6**.
- **Verdict:** **DROP.** The licence wave plus national competition and thin per-sale contribution leave a founder-sized job (~$5k/month) rather than a scalable company.
- **What would reopen it:** V1 showing a niche median hammer of at least $12k, plus V2 producing three or more committed referral sources.
