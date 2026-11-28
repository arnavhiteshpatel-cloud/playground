# WS11-017: Commercial cooling-tower and boiler water-treatment route (Stage D, batch DI)

Investigated 2026-11-28. Read-only research: nobody was contacted, no quotes were requested and no accounts were created. Evidence levels A–E follow `EVIDENCE_STANDARDS.md`. Sources prefixed DI- are in `05_deep_dives/sources_DI.jsonl`; C1- sources come from the Stage C memo.

> **Verdict: DROP as a from-scratch entry. Keep the idea as a possible later bolt-on acquisition for the holding company.**
>
> **Revised composite:** raw 4.42, evidence-adjusted 4.59 (evidence level D). Stage C was 5.32.
>
> **Decisive facts:**
> 1. The founder cannot hold the industry credential before about 2029. The Certified Water Technologist (CWT) designation needs **5 years of documented water-treatment experience**; a technical degree credits only 2 of them [B, DI-S008]. Credibility and technical sign-off therefore have to be bought from day one.
> 2. Buyers who publish prices run price wars. A boiler and cooling-tower programme at VA Illiana drew **12 offers** and was awarded at **$32,512/yr** [A, DI-S005].
> 3. With evidence-derived drivers, the base model reaches only **~$24k year-3 operating profit** and ~$38k in year 5, with ~$117k peak funding.
>
> **What is good:**
> - Demand is mandated and recurring. CMS requires water-management programmes at certified healthcare facilities [A, DI-S011].
> - Prospects are trivially identifiable from public permit data: 211 Chicago addresses had cooling-tower permits from 2006 to 2026 [A, DI-S002].

---

## 1. Specific initial niche

**Monthly water-treatment programmes for Chicago condo and co-op high-rises, hotels and independent hospitals in Cook County** (Gold Coast, Streeterville, Near North, Lakeview/Edgewater lakefront, South Loop, Hyde Park). Each programme covers:
- cooling towers, fluid coolers or closed-circuit coolers;
- closed hydronic loops;
- heating boilers.

The fee includes chemistry, monthly testing and reports, controller management, and drafting of ASHRAE 188 / CMS QSO-17-30 water-management plans.

**Why this niche:**
- **Lakefront high-rises are numerous.** The 2023 Chicago benchmarking data show 363 multifamily buildings over 250k sq ft, plus 156 office buildings, 36 hotels and 13 hospitals [A, DI-S003]. Many have evaporative heat rejection (E).
- **The buyers are reachable.** They are condo boards and property managers, who are more price-sensitive and easier to reach than university or data-centre engineering departments, where national vendors are entrenched (E).
- **The work has a trigger date.** Recent tower replacements are public permits, and a newly installed tower needs a start-up passivation and a programme from day one.

## 2. Named operators

| Operator | Type | What is known |
|---|---|---|
| H-O-H Water Technology (Chicagoland, IL) | Illinois independent | City of Chicago awards of $11.36M (2007–12), $3.88M (2016–21) and $4.32M (2022–27, modification end-date 2030) [A, DI-S001]. Cook County chemical contract of ~$65k/yr in 2016–18 [A, DI-S004]. Family-owned for 50+ years per a trade-directory listing (D). |
| Global Water Technology Inc | Regional independent | Cook County Facilities Management water treatment and testing, **$349,541 for 2024-07 to 2027-06** (~$116.5k/yr). Prior contract $228,864 plus amendments [A, DI-S004]. A $6,400 Peoria Air National Guard boiler order appeared in a search summary (D). |
| AquaLab Water Treatment Inc (Prospect Heights, IL) | Chicago-area independent | VA Hines awards: $118,800 emergency softener/carbon filter and $14,450 boiler-plant repairs [A, DI-S006]. |
| Liberty Technical Services LLC (MD) | Out-of-state small vendor | Won the VA Illiana boiler programme at $32,512/yr against 11 other offers [A, DI-S005]. |
| Eldon Water Inc (Novi, MI) | Regional independent | VA Danville boiler and cooling-tower programme, $60,677 over 2016–20 (2 offers) [A, DI-S006]. |
| Fehr Solutions LLC | Specialist consultant | Chicago airports water-treatment services and consulting ($252k 2012–17; $1.5M ceiling) [A, DI-S001]. |
| Ecolab / Nalco Water; ChemTreat; Chem-Aqua (NCH); Garratt-Callahan | Nationals | Market "led by a few large companies" [A, C1-S010]. Garratt-Callahan bid $66,570 and Chem-Aqua $78,000 against an independent's $29,400 [A, C1-S006]. Solenis's site hosts Chem-Aqua material ("Solenis + NCH"), which implies common ownership (D). |
| Phigenics (Naperville, IL) | Water-management / Legionella specialist | Site blocked at access; could be a partner or a competitor (E). |

**Reading across the table:**
- Chicago-area independents (H-O-H, Global Water Technology, AquaLab) win public work at multi-hundred-thousand-dollar scale. The independent model is proven locally.
- Every documented independent has decades of references. None is a recent from-scratch entrant. Small-start evidence remains MISSING.

## 3. Named suppliers and partners (full detail in `09_databases/suppliers/WS11-017_suppliers.csv`)

| Supplier | Role | Status |
|---|---|---|
| **Dober** (Woodridge, IL) | Cooling-tower chemicals, water treatment, chemical delivery equipment; contract-manufacturing language; 12 plants [D, DI-S012] | *Assumed.* Private-label terms, minimum orders and credit for a new LLC require direct confirmation. |
| **QualiChem** | Private-label formulating manufacturer of boiler and cooling chemicals, listed in AWT's buyer's guide [D, DI-S014] | *Assumed.* Site blocked. |
| **Chem-Met Company** | Custom blending of private-label water-treatment chemicals [D, DI-S014] | *Assumed.* |
| **Hydrite Chemical** | Oxidising and non-oxidising biocides; scale and corrosion inhibitors [D, DI-S013] | *Assumed.* Reseller terms not stated. |
| **Association of Water Technologies (AWT)** | Training, buyer's guide, CWT credential [B, DI-S008, DI-S009, DI-S030] | *Documented* fees: exam $410 member / $510 non-member; processing $260 / $515. Dues MISSING. |
| Walchem, Taylor Technologies, LaMotte | Controllers, test kits, photometers | *Assumed* (prices not read). Public bids show controllers at $3,958–5,816 each [A, C1-S007]. |
| Contracted CWT (individual, to be found via the AWT member search) | Programme design and sign-off | *Assumed:* modelled retainer $1.5k–3k/month (E). Former employees of nationals may carry non-competes. |

- **Chemical price benchmark.** A state-contract price list (Maine, 2021) is the only published price data found [A, DI-S007]. It is end-customer pricing, so blender cost is lower but unknown.

  | Product | Price per gallon |
  |---|---|
  | Cooling inhibitor | $23.97–30.48 |
  | Oxidising biocide | $10.60 |
  | Non-oxidising biocide | $30.40 |
  | Closed-loop nitrite | $13.73 |
  | Boiler blend | $7.31–25.43 |

- **Missing terms.** No toll blender publishes reseller terms. The model's 62% gross margin assumes blender cost is 40–55% of those end-prices (E).

## 4. Named prospective customers

`09_databases/prospects/WS11-017_prospects.csv` lists **33 real Illinois organizations**, all marked "prospect — not contacted":
- **Building owners with recent cooling-tower permits [A, DI-S002]:**
  - condo associations: One East Scott, 1440 N Lake Shore, Folio Square, 3600, Ontario Place, Mayfair, City View;
  - other owners: VOP Lake Shore Drive LLC and Newcastle Limited.
- **Hotels:** Embassy Suites Chicago Downtown and Westin River North.
- **Institutions:** DePaul, Loyola, Anti-Cruelty Society, Chicago Child Care Society, Queen of Apostles Parish, United Center JV, Rush.
- **Owners and managers:** Peak Properties, Onni Group, Brookfield Properties.
- **Specialised sites:** CoreSite CH2 (data centre) and Scout Cold Logistics (evaporative condensers).
- **Long-term care:** The Alden Group, which falls under CMS.
- **Seven independent CMS-listed hospitals [A, DI-S016]:** Saint Anthony, Thorek, Humboldt Park Health, Jackson Park, Roseland, Loretto, St Bernard.
- **A public rebid:** Cook County Facilities Management; the current contract ends 2027-06-30 [A, DI-S004].
- **A channel:** FirstService Residential.

These are prospects, not leads: no interest has been expressed.

## 5. Representative transactions (annual unless stated)

| # | Transaction | Revenue | Direct costs | Contribution | Evidence / timing |
|---|---|---|---|---|---|
| T1 | Condo high-rise: one ~400-ton tower or fluid cooler + closed loop + 2 boilers, monthly programme | $7,800 ($650/mo) | Chemicals at blender cost $2,200; quarterly Legionella lab tests and reagents $500; technician 12 visits × 3 h × $45 = $1,620; vehicle $300 | **$3,180 (41%)** | Revenue E; chemicals E from DI-S007 prices; labour C (BLS, DI-S015). Monthly billing, net-30. |
| T2 | Public multi-facility contract (Cook County scale) | $116,514 | Chemicals $38,000; ~0.6 FTE technician $54,000; lab $6,000; vehicle $4,000 | **$14,514 (12%)** | Revenue A [DI-S004]; costs E. Public work is thin-margin, and a newcomer cannot win this without references. |
| T3 | New-tower start-up passivation + conductivity controller | $5,500 one-time | Controller at dealer cost $2,800; passivation chemistry $250; labour $270 | **$2,180** | Controller price range A [C1-S007]; costs E. Paid on completion. |
| T4 | ASHRAE 188 water-management plan for a small long-term-care building | $3,500 one-time | CWT review 10 h × $100 = $1,000; baseline sampling $400 | **$2,100** | Price MISSING; E. |

- **Unit economics.** T1 is the core unit. With 45 buildings per technician, one technician (~$90k loaded) is covered by roughly 28 T1 accounts before overhead.
- **Thin margin per building.** This is why scale comes slowly.

## 6. Customer acquisition

- **Customer #1:** a condo association or non-profit whose tower was just replaced. Permits are issued weeks before commissioning [A, DI-S002]. The offer:
  - a paid **"water-system health check" ($350–750)**: water analysis, a Legionella risk walk-through and a written report;
  - the fee credited against a 12-month programme.

  The approach goes through the property manager and the chief engineer.
- **Customers #2–10:**
  - referrals from the first property manager (a single FirstService-type firm manages many buildings);
  - mechanical contractors who replace towers (permit data names them);
  - small public bids (park and school districts) for price discovery.
- **Customers #11–100:**
  - technician-led upsell (controllers, WMPs);
  - hospital and long-term-care WMP audits under CMS;
  - Cook County's 2027 rebid once references exist.

  A dedicated $10k/month technical sales hire **does not pay back** within 3 years at ~$650 per building, so growth stays founder- and referral-led. This was tested in the model.

**Funnel (all E):**

| Stage | Base | Conservative–optimistic |
|---|---|---|
| Qualified site conversations per month | 12 | 8–16 |
| → proposal | 35% | |
| → win | 22% | 15–30% |
| New buildings per month at full pace | ~0.9 | |
| Referral buildings | +1 per 100 active per month | |

**Unit metrics (E):**
- **Cash CAC ≈ $730:** lab fees and travel of $400, plus allocated marketing.
- **Contribution after technician labour ≈ $2.5k per building per year.**
- **LTV** about $20k at 1% monthly churn.
- **Payback** on CAC is about 3 months of contribution.

**Founder time:** about 10–15 hours of selling a week, plus 25–35 hours of route work once there are 20–30 accounts. That is a hard ceiling until the first technician is hired (modelled at 30 accounts).

## 7. Pricing strategy and market prices

**Market evidence:**
- **Public price evidence (A):**
  - VA Illiana $32,512/yr for a 16-boiler plus cooling-tower programme, 12 offers [DI-S005];
  - Cook County ~$116.5k/yr across county facilities [DI-S004];
  - Columbus, GA: same multi-building scope bid at $29,400 by an independent vs $66,570 and $78,000 by nationals [C1-S006];
  - Nebraska service labour about $25/h [C1-S007].
- **Unit chemical prices:** the Maine state contract [A, DI-S007].
- **Private-building prices are MISSING.** No price list or budget line was found, including a targeted search of condo budgets.

**Strategy:**
- **Price structure:** a transparent fixed monthly fee per system: about $350 for a tower or fluid cooler, $150 for a closed loop, $150 per heating boiler (E). Chemistry is included up to a usage band. The pitch is "60–75% of your national-vendor quote", supported by the 2.3–2.65× bid gap [A, C1-S006].
- **Separately priced work:** start-ups, controllers and WMP drafting.
- **Avoid early public bids** except for price discovery. With 12 offers, the winner prices at labour cost.

## 8. Working capital and cash conversion

Drivers: DSO 45 days, drum inventory 30 days of COGS, payables 30 days (blender terms MISSING).

| Active buildings | Monthly revenue | Net working capital | Cash conversion |
|---|---|---|---|
| 10 | ~$6.5k | ≈ $10k | ~45 days |
| 50 | ~$33k | ≈ $49k | ~45 days |
| 200 | ~$130k | ≈ $195k | ~45 days, plus a warehouse inventory step-up |

The model's peak funding of **$117k (base)** is mostly operating losses during the 26-month climb to breakeven, not working capital:
- the CWT retainer, insurance and the vehicle run before density;
- the first technician hire temporarily resets profit to near zero.

## 9. Regulatory path

| Item | Status |
|---|---|
| Illinois water-treatment licence | None identified (Stage C; E — ilga.gov unavailable). |
| Pesticide licensing for biocides | Illinois has **12 pesticide categories and none covers cooling towers**. Category 5 (Aquatic) covers pesticides "purposefully applied to standing or running water"; Category 7 sits with IDPH under the Structural Pest Control Act [A, DI-S010]. Whether for-hire biocide dosing needs a commercial applicator licence **requires written confirmation from IDOA and IDPH**. If yes: General Standards exam plus a category exam (search summary, D); timing likely 1–3 months (E). |
| Healthcare demand driver | CMS S&C/QSO-17-30 requires a programme, not a vendor [A, C1-S008, DI-S011]. IDPH describes no state cooling-tower registry [A, DI-S011]. |
| Transport | The DOT materials-of-trade exception (49 CFR 173.6) limits quantities; 55-gal drums of corrosives likely exceed it. Plan blender drop-ship to sites (E; verify). |
| CWT | Voluntary. Exam $410/$510; 5 years' experience; recertify every 5 years [B, DI-S008, DI-S009]. |
| Entity | Illinois LLC; Chicago business licence only if based in the city (E). |
| Insurance | GL, contractor's pollution, professional/E&O and commercial auto. Indicative $8–15k/yr (E — no quotes requested). |

## 10. Operations workflow (lead to cash)

1. **Lead (automatable).** A weekly pull of Chicago permits (cooling tower, fluid cooler, chiller) and benchmarking data.
2. **Qualification (human).** A call with the property manager or chief engineer.
3. **Site survey and water sampling (human, with lab support).**
4. **Proposal (AI-assisted).** Drafted from survey data with a contracted-CWT review.
5. **Start-up (human).** Passivation, controller set-up, WMP drafting.
6. **Monthly visit (human).** Conductivity, inhibitor residual, halogen/ORP, dip slides; quarterly Legionella lab samples.
7. **Report (AI-drafted, human-signed).**
8. **Invoice and collection (automatable).**

**Stack:** CRM, a route/forms app, accounting, controller cloud dashboards and an LLM for reports; about $250/month modelled (E, AI items flagged). AI saves report-writing time but **does not reduce the binding constraint**, which is skilled on-site hours and trust.

## 11. Competitive position and defensibility

**What accumulates:**
- route density (shorter drive time per visit);
- controller installs and programme histories, which raise switching friction;
- a reference list of condo boards and hospitals;
- an eventual in-house CWT.

**Why the position stays weak:**
- **AWT counts 500+ member firms** [C, C1-S009], and nationals discount when challenged.
- **Public buyers attract 12 offers.**
- **Technicians are poachable.** The scarce asset is the experienced technologist, who can leave with the accounts. This is the industry's typical origin story (E).

## 12. Key risks and pre-mortem

| Loss level | How it fails | Early warning |
|---|---|---|
| **$5k** | No blender will sell private-label at ≤55% of contract end-prices, or no CWT will contract at ≤$100/h without equity. Stops at validation. | Fewer than 2 of 4 blenders respond with price lists; no CWT is available within 60 days. |
| **$25k** | 6–10 buildings are won, but the founder's route hours cap selling; the 12-month learning curve produces a scaling or corrosion complaint; churn follows. | Win rate below 10% after 25 proposals; any account lost in year 1; gross margin below 50% on real invoices. |
| **$50k** | A Legionella finding or equipment-damage claim at a client building, or plateauing at ~25 buildings after hiring a technician, with losses continuing. | Positive Legionella lab results not resolved within 30 days; technician utilisation below 60%; month-24 operating profit still negative. |

**Structural risks:**
- non-competes on hired staff;
- national price response;
- possible biocide licensing;
- insurance cost escalation.

## 13. Validation plan (cheapest experiments that produce commercial evidence)

| # | Experiment | Cost | Success | Kill |
|---|---|---|---|---|
| V1 | Written confirmation from IDOA/IDPH on whether for-hire cooling-tower biocide application needs a licence | $0 | Answer in hand; licence obtainable in ≤3 months | Licence needs more than 12 months or prior experience |
| V2 | Price lists and minimum orders from Dober, QualiChem, Hydrite and Chem-Met (founder action after 2026-12-05) | $0 | ≥2 suppliers sell to a new LLC at ≤55% of Maine end-prices, net-30 | No supplier will open an account without volume history |
| V3 | Recruit a contract CWT (AWT member search; LinkedIn) | ≤$300 | Signed letter of intent at ≤$2.5k/month retainer, no non-compete conflict | None found in 60 days |
| V4 | Sell 3 paid "water-system health checks" to permit-identified buildings | ~$600 lab costs | 3 paid checks and ≥1 programme proposal accepted within 90 days | 0 paid after 30 qualified pitches |
| V5 | Price discovery: obtain two private national-vendor programme prices via prospects' own invoices (with permission) | $0 | Private prices of ≥$700/month per tower building confirmed | Below $450/month, which leaves no margin |

Total cash for validation is about $1,500.

## 14. Revised scores and verdict

| Criterion | Stage C | Stage D | Reason |
|---|---|---|---|
| fcf | 4 | **3** | Base year-3 ~$24k, year-5 ~$38k; optimistic $157k / $356k |
| roic | 6 | **3** | Base year-3 operating profit ÷ peak funding ≈ 21% |
| access | 4 | 4 | Buyers easy to identify (permits, CMS lists) but credibility-gated |
| scale | 6 | **5** | ~$650/building; technician-limited |
| resilience | 8 | 8 | Consumable; CMS programme mandate |
| entry | 5 | **4** | 500+ independents; 12-offer public bids; copyable wedge |
| delegation | 6 | **5** | Skilled technologists scarce; CWT needs 5 years |
| cash | 6 | 6 | Net-30/45; modest inventory |
| feasibility | 7 | **5** | Paid CWT from month 1; biocide licensing unconfirmed; hazmat logistics |
| ai | 4 | 4 | Reports and anomaly flags only |

**Composite and gates:**
- **Composite:** raw 4.42, evidence-adjusted **4.59** (evidence D).
- **Gates:** G4_CEILING WARN (base never reaches $100k/yr within 5 years) and G7_FOUNDER_DEPENDENT WARN.
- **Model** (`08_financial_models/WS11-017_model.xlsx`):

  | | Conservative | Base | Optimistic |
  |---|---|---|---|
  | Year-3 operating profit | −$66k | **$24k** | $157k |
  | Peak funding | $349k (the model keeps running; a founder would stop at the kill criteria) | $117k | $63k |
  | Base breakeven | | month 26 | |

**Verdict: DROP.** The industry is attractive, but the founder lacks the one asset that wins it: a decade of technical relationships. Acquiring an independent route later is the better route, and acquisitions are outside Stage-1 rules.
