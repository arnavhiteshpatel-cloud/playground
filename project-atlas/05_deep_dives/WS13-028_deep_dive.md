# WS13-028: Pet cremation & aftercare for veterinary clinics (absorbs WS04-032)
Stage D · batch DE · 2026-11-28 · model `08_financial_models/WS13-028_assumptions.json` (results in `WS13-028_results.json`)

> **Verdict: DROP. Keep the Stage C regulatory finding on file.**
>
> **Scores:** revised adjusted score **4.60** (raw 4.43, evidence D), down from 5.48 at Stage C.
>
> **The decisive fact.** The Chicago market already belongs to a national consolidator that sells the same wedge Atlas planned to sell.
> - Gateway Services' **Trusted Journey** brand runs **6 Illinois sites**, including Hinsdale Animal Cemetery (Willowbrook), Paw Print Gardens (West Chicago) and Pets At Peace Crematory (Hampshire) [B, DE-S003].
> - It markets "Paws e-Track", which tracks each pet through **20+ barcode-scanned steps** from clinic pickup to return [C, DE-S004]. That chain-of-custody feature was our planned differentiator.
> - Meanwhile **43% of licensed veterinary-hospital locations in Chicago** belong to national or regional groups that buy centrally [A, DE-S001].
>
> **The economics.**
> - An owned retort needs an IEPA permit: no Illinois exemption covers incinerators, and the small-source registration route (ROSS) excludes incinerator systems [A, DE-S005, DE-S006]. It also usually needs a local special use, which can be refused (Mokena 2021) [C, DE-S008].
> - On evidence-derived drivers the base case reaches about **$0 operating profit in year 3 and ~$93k in year 5**.
> - It needs about **$344k of cumulative funding** before draws ($434k with a $4k/month owner draw). That is well beyond the $100k conditional capital.
> - The asset-light route, using a trade crematory, needs ~$124k but earns only **~$15k a year** (variant run, §5).

## 1. Specific initial niche
The niche is weekly freezer pickup, communal and private cremation, and return of remains for **independent small-animal general practices in the City of Chicago and inner Cook County**. A single van covers this route.

Chicago licence records list **115 veterinary-hospital locations** with active Animal Care licences [A, DE-S001]:
- **35** are held by national or venture groups identifiable by licence-holder name: VCA 7, Pathway 5, Bond Vet 4, NVA 4, Banfield 3, Sploot 3, Suveto 2, Southern Veterinary Partners 2, and MedVet, VEG, Ethos, AAH Acquisition and BRM IL with one each.
- **14** belong to regional multi-site groups: GoodVets 6 and Midwest Veterinary Hospitals PLLC 8.
- After removing shelters, rehab clinics and specialty sites, roughly **55–60 independent general practices** remain in the city.

Statewide, firms with 500+ employees run 22% of Illinois veterinary establishments and earn 41% of receipts [C, DE-S002].

## 2. Named operators
| Operator | What is known |
|---|---|
| **Gateway Services / Trusted Journey** | 150+ care centers, 49+ states and provinces, 2,000+ staff, 20 regional brands. Illinois sites: Champaign, East Dundee, Hampshire (Pets At Peace), Plainfield, West Chicago (Paw Print Gardens) and Willowbrook (Hinsdale Animal Cemetery). The legacy Hinsdale domain redirects to Trusted Journey. Paws e-Track barcode tracking; clinic login [B/C, DE-S003, DE-S004]. PAWS Chicago refers grieving owners to Hinsdale [C, DE-S040]. |
| **Animal Cremation Society of Chicagoland** (5201 N Pulaski) | Calls itself "Chicago's only local pet crematorium". Private cremation from $130 (cat) and $160 (small dog), priced by the pound. Takes nothing over 70 lb; drop-off only [B, DE-S015]. |
| **St Francis Pet Crematorium** (Wood Dale) | 4.9 rating on 41 Google reviews. The directory's price ranges look generic [D, DE-S047]. |
| **Forever Remembered** (Woodstock) | Communal from ~$100 [D, C8-S015]. |
| **Cherished Pets Remembered** (Justice); **Elm Lawn Pet Cemetery** | CodaPet lists both as local crematories [B, DE-S014]. |
| **DeFiore Furever Friends** (Huntley) | Funeral home building a 4,622 sq ft pet crematory. Special use approved January 2025 [C, DE-S007]. |
| **Pet Passages** (franchisor, Ontario NY) | No Illinois location listed [C, DE-S016]. |
| **Regency Pet** | Midwest roll-up [C, C8-S016]. Illinois footprint not found. |
| **Channels:** CodaPet and Lap of Love | Home-euthanasia networks. CodaPet Chicago charges from $415 for in-home euthanasia, with cremation $150–$505 [B, DE-S014; C, DE-S042]. |

**Heartland / VCA:** no Chicago licence holder named "Heartland" appears in the city data [A, DE-S001]. VCA's seven city hospitals are corporate and presumably follow a national aftercare contract; the vendor is MISSING.

## 3. Suppliers and partners
See `09_databases/suppliers/WS13-028_suppliers.csv`.

| Supplier | What we found | Status |
|---|---|---|
| **B&L Cremation Systems** | 8 single-chamber and 12 multi-chamber pet models, 100–2,000 lb capacity, 50–300 lb/hr; third-party financing [B, DE-S009, DE-S010] | Documented; prices MISSING |
| **Matthews Environmental Solutions** | Only hard price found: a **federal purchase of a Power Pak I cremator system plus accessories for $95,047 (2018)** [A, DE-S011] | Documented |
| **Shenandoah** | Website did not respond; existence not verified | MISSING |
| **Used equipment** | Seller claims new pet systems run $35k–$100k+ and used ones $2k–$35k [D, DE-S012] | Seller figures only |
| **Trade cremation** (Animal Cremation Society of Chicagoland, St Francis, Forever Remembered) | All are competitors; willingness and fee MISSING | Assumed — requires direct confirmation |
| **CANA CPCO course** | $595 member / $695 non-member [C, WS13-S018] | Documented |
| **Jobber** | $49–$399/month [B, DE-S035] | Documented |

## 4. Named prospective customers
`09_databases/prospects/WS13-028_prospects.csv` lists **35 organizations**: 34 independent Chicago clinics from city licence records plus PAWS Chicago.
- Websites were verified by name and street number for 18 of them.
- Examples: Precious Bond Animal Hospital, Near North Animal Hospital, Animal House of Chicago, Fullerton Animal Clinic, Animal Medical Center of Chicago, Mayfair Animal Clinic, Pulaski Animal Hospital, Kragness Animal Hospital, West Wrigley Animal Hospital, Marquette Animal Hospital, Oz Animal Hospital and Chicago Cat Clinic.
- Ownership is inferred only from licence-holder names. All are "prospect — not contacted".

## 5. Representative transactions
These are clinic accounts billed monthly on net-30 (E).

| Transaction | Revenue | Direct costs | Contribution | Evidence |
|---|---|---|---|---|
| Private cremation, cat, own retort | $110 wholesale | Gas/maintenance $12; urn/tag/certificate $10; route $20; operator $10 | **$58** | E (retail $130–$300 [B]) |
| Communal cremation, 40-lb dog, own retort | $40 | $6 + $2 + $12 + $4 | **$16** | E (retail group $75 [B, C8-S014]) |
| Private cremation via trade crematory (months 1–11) | $110 | Trade fee $65 (MISSING); urn $10; route plus extra leg $28 | **$7** | E |
| Direct-family private with residence pickup (prepaid) | $280 | $12 + $18 + $45 + $8 | **$197** | D |

**Model results (base case):**

| Item | Value |
|---|---|
| Clinics in year 3 / year 5 | 38 / 67 |
| Revenue in year 3 / year 5 | $339k / $693k |
| Operating profit by year | −$30k / −$54k / **$0** / $87k / **$93k** (years 1–5) |
| Breakeven month | 31 |
| Conservative case | Never breaks even |
| Optimistic case (2–3 retorts) | Year 3 $259k |

**Sensitivity:** the largest swings come from gross margin and per-clinic revenue, each moving year 3 by about ±$55k.

**Asset-light variant** (gross margin 38%, no retort; run on the same engine): year 3 $15k, year 5 $15k, peak funding $124k.

The model **excludes the direct-family channel**. Adding 300–400 family cases a year would add about $60–80k of contribution, but how much of that volume is obtainable is E.

## 6. Customer acquisition
| Stage | Approach |
|---|---|
| **#1** | Walk in to one independent clinic within 3 miles of the cold room. Offer to take its next 5 cases free of pickup charges, with photo-documented returns inside 7 days. |
| **#2–10** | Lunch-and-learns for practice managers; referrals from home-euthanasia vets; a compliant 815 ILCS 318 written explanation the clinic can hand owners. |
| **#11–100** | Route density across Chicago and inner-ring suburbs, plus a shelter account. Requires winning against Gateway and corporate contracts. |

- **Funnel (E):** 18 qualified conversations a month → 40% agree to a priced trial → 20% convert, about **1.4 new clinics a month**.
- **Unit economics:** CAC about $300 a clinic. Base lifetime value is about $850 × 66% / 1.5% churn ≈ $37k of gross profit per clinic, which looks attractive. The binding constraint is win rate against an incumbent with equal tracking, not CAC.
- **Founder time:** 12–15 hours a week of in-person selling in year 1, plus driving the route until 20 clinics.

## 7. Pricing strategy
Retail prices set the ceiling:
- Chicago private cremation $130–$160 and up [B, DE-S015].
- CodaPet Chicago cremation $150–$505 [B, DE-S014].
- Downstate Deiters: individual $200–$300, group $50–$180, vet transfer $95 [B, C8-S014, DE-S041].
- The UK CMA found clinics mark up crematory wholesale fees, with communal two to five times cheaper than individual [C, DE-S013].

Proposed wholesale: about $110 private and $40 communal, with free scheduled pickup, plus memorial upsells. **Wholesale price sheets are MISSING.** Until a clinic shows its current invoice, every margin above is E.

## 8. Working capital and cash conversion
DSO is 30 days, inventory 10 days of COGS and DPO 15 days, for a cash conversion cycle of about **25 days**.

| Clinics | Net working capital | Notes |
|---|---|---|
| 10 (~$8.5k/month revenue) | ≈ $8k | |
| 50 (~$42k/month) | ≈ $40k | |
| 200 (~$170k/month) | ≈ $160k | Needs 3 retorts |

Capital intensity dominates working capital:
- van $35k, freezer $12k;
- fit-out, permits and engineering $30k;
- retort $110k (E, anchored to $95k [A]);
- $30k per extra van.

## 9. Regulatory path
1. **No state licence.** 815 ILCS 318 requires a written explanation of services (no misleading "private" claims), copies to referring vets and the Attorney General, and a certification with returned remains. Fines run $1,001–$2,500 [A, C8-S006]. Not a waste facility under 415 ILCS 5/22.49 [A, C8-S007].
2. **Own retort: IEPA air permit.** 35 IAC 201.146 has no crematory exemption and keeps incinerators inside permit requirements. ROSS (201.175) excludes "incinerator systems" [A, DE-S005, DE-S006]. Plan for a construction permit, then an operating permit; fees and timing are MISSING. Next step: an IEPA Bureau of Air pre-application (read-only research cannot do this).
3. **Zoning.** Expect a special use. Huntley approved one in about 7 months after neighbour concerns [C, DE-S007]; Mokena denied a crematorium special use 7–0 [C, DE-S008]. Target industrial parcels where crematories are permitted by right (MISSING).
4. **Insurance:** general liability with care-custody-control, commercial auto and property. About $800/month (E, no quotes). The CANA CPCO credential is optional.

## 10. Operations workflow
1. Clinic calls or uses a portal.
2. Scheduled pickup: barcode tag, photograph and weigh.
3. Cold room.
4. Cremation (trade, then own retort), with scans at each step.
5. Return to the clinic with the certificate.
6. Monthly invoice.

**Human work:** driving, intake, retort operation, grief-sensitive calls.

**Automatable or AI-assisted:** scheduling, notifications, invoicing, memorial-product ordering. Jobber at $49–$139/month plus a barcode app (E).

AI does not lower cremation cost.

## 11. Competitive position and defensibility
**What accumulates:** clinic routines, a permitted retort site (scarce because of zoning and IEPA friction), and owner reviews.

**The problem:** the incumbent already holds these assets in Illinois, including cemeteries, multiple retorts and a tracking system. A newcomer's wedge (speed, service, a local face) is copyable. Corporate consolidation keeps shrinking the open share of the market [A/C, DE-S001, DE-S002].

## 12. Risks and pre-mortem
| Loss level | How it happens |
|---|---|
| **$5k lost** | Months of clinic visits produce verbal interest but no trial, because practices are satisfied with Gateway or bound by group contracts. |
| **$25k lost** | Van, freezer and insurance bought; 5–8 clinics signed; the trade crematory raises its fee or refuses (it is a competitor). |
| **$50k+ lost** | Lease signed and retort ordered before 25 clinics; special use or IEPA delay; or a mix-up of remains, which is a statutory offense [A, C8-S006] and a reputational catastrophe. |

**Early warnings:**
- win rate below 15% after 20 proposals;
- trade fee above $55 for a private cremation;
- below 8 pets per clinic per month;
- loss of any clinic to a corporate acquisition.

**Stress tests:**
- win rate −40% → year 3 −$36k;
- "growth takes twice as long" → year 3 −$58k, funding $713k.

## 13. Validation plan
Only worth running if the founder disagrees with the drop verdict.

| Test | Cost | Success | Kill |
|---|---|---|---|
| Ask 10 independent clinics (in person) for their current aftercare invoice and volume | $100 fuel | ≥3 share invoices showing wholesale ≥$100 private and ≥10 pets/month | Wholesale below $80 or volume below 8 |
| Request written trade-cremation terms from 2 crematories | $0 | Private trade fee ≤$50 | Refusal or fee ≥$65 |
| IEPA Bureau of Air pre-application call plus one industrial-zoning check | $0 | Permit path ≤6 months, by-right site exists | Special use required everywhere |
| Paid pilot: 3 clinics on 5 cases each via trade crematory | ~$1,500 | ≥2 clinics convert to standing weekly pickup | 0–1 convert |

## 14. Revised scores and verdict
| Key | Stage C | Stage D | Why |
|---|---|---|---|
| fcf | 5 | **3** | Base case: year 3 ~$0, year 5 ~$93k |
| roic | 5 | **3** | ~$93k on $344k of funding |
| access | 5 | **4** | 43% of Chicago locations in groups; Gateway entrenched |
| scale | 6 | 5 | Each retort is a capacity step (~8k pets a year) |
| resilience | 8 | 8 | Non-discretionary |
| entry | 5 | **3** | The tracking wedge is the incumbent's standard |
| delegation | 7 | 7 | |
| cash | 7 | **6** | Net-30 plus heavy capex |
| feasibility | 7 | **5** | IEPA permit plus special-use siting |
| ai | 3 | 3 | |

**Composite:** raw 4.43, evidence-adjusted 4.60 (D).

**Year-3 operating profit:** low −$138k, **base ~$0**, high $259k.

**Plausible ceiling:** ~$250k a year, and only with 2–3 retorts.

**Verdict:** **DROP.**
