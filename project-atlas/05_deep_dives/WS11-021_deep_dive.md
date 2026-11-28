# WS11-021 — Construction stormwater (ILR10/SWPPP) inspections and BMP maintenance (Stage D deep dive, batch DB)

Absorbs WS15-021. Access date 2026-11-28.
- Model: `08_financial_models/WS11-021_assumptions.json` / `_model.xlsx` / `_results.json`.
- Prospects: `09_databases/prospects/WS11-021_prospects.csv` (32).
- Suppliers: `09_databases/suppliers/WS11-021_suppliers.csv` (12).
- Sources: `05_deep_dives/sources_DB.jsonl` plus C7 and WS11 sources.

> **Verdict: RESERVE.** Demand and access are now A-level and better than Stage C knew:
> - ECHO names the permittee on every coverage.
> - Coverage grew from 1,306 new coverages (2024) to 1,503 (2025) and 1,525 (2026 YTD) [A, DB-S008].
> - 346 repeat permittees hold 55% of 2025–26 sites.
>
> But the economics are thin. The model base gives **year-3 operating profit of about $54k** on 31 active sites. It plateaus at around $50–80k because sites churn out at about 7% a month and a founder-led pipeline only replaces them. Pricing is still D: no private Illinois price was found, and the only Illinois figure is the Kane-DuPage SWCD public fee of $690/yr for oversight inspections on small sites [A, DB-S009]. Use it as an add-on to a site-services or compliance business, not as the founder's main vehicle.

## 1. Specific initial niche
**Initial niche:** per-site monthly ILR10 inspection contracts for mid-size site/civil contractors, design-builders and municipal owners running 3–25 Chicagoland sites a year in Will, DuPage, Kane and south/west Cook.

**The service:**
- weekly and post-0.5-inch-storm inspections;
- signed reports within 24 hours;
- corrective-action tickets;
- an optional BMP repair crew (inlet filters, silt fence, construction entrances).

**Why these buyers:** they are repeat permittees (e.g., Austin Tyler 9 sites, D Construction 10, Wight 10, Nicholas & Associates 12 in 2025–26 [A, DB-S008]). They are large enough to need help but too small to keep an environmental department.

**Deferred:**
- homebuilders (national divisions likely contract centrally);
- rural community-solar sites. These total 455 statewide, but drives of about 90 miles erase margin (transaction D).

## 2. Named operators
| Operator | Type | What is known | Level |
|---|---|---|---|
| Kane-DuPage Soil & Water Conservation District (St. Charles) | Public agency | Oversight inspections at least monthly and after significant rain under municipal MOUs (Batavia, Aurora, North Aurora, Elburn, St. Charles). Developer pays $690/yr (0–9 acres) to $8,730/yr (400–499 acres); non-compliance $95/h [DB-S009] | A |
| Engineering Enterprises, Inc. | Illinois civil engineer | Has handled North Aurora's erosion-control reviews, inspections and close-outs "for over twenty years" [DB-S034]; fees not seen | D |
| Fehr Graham | Illinois engineering firm | Appears in Illinois municipal stormwater work [C7-S035] | A |
| Silver Leaf SWPPP | National specialist (Utah) | Pays inspectors about $25–28 per inspection [C7-S016] | D |
| ARCXIS | National builder-focused | Fixed-monthly SWPPP inspection packages for residential builders; price undisclosed [C7-S036] | D |
| Pro SWPPP (Texas) | National plan/inspection vendor | Illinois guide page; no prices [DB-S043] | D |
| Manhard Consulting, V3 Companies | Chicago-area civil engineers | Websites list stormwater/land-development services [DB-S044, DB-S045]; inspection pricing MISSING | D |
| GC self-inspection | DIY | ILR10 lets any "knowledgeable person" inspect [A, C7-S011] | A |

**Pricing proxies from other states:**
- $95 per inspection (New Mexico vendor proposal) [D, C7-S014];
- $240 per monthly municipal inspection (Fort Wayne) [B proxy, C7-S013].

**Market structure:** Illinois environmental consulting (NAICS 541620) has 239 firms. The 139 with under 5 employees average $362k receipts [C, DB-S036].

## 3. Named suppliers and partners
- **USEPA CGP inspector course:** free; passing it qualifies the inspector [A, DB-S010].
- **EnviroCert CESSWI:** $370 application + $345 exam, $160/yr renewal [B, DB-S011].
- **Illinois EPA ILR10 / NeT:** NOI fee $250/$750 is paid by the permittee [A, WS15-S028].
- **ECHO API:** free prospecting data [A, DB-S008].
- **Field apps:**
  - Fulcrum $43–55/user/mo [B, DB-S037];
  - GoCanvas $29–49/user/mo with a 3-user minimum [B, DB-S038].
- **Claude Pro/Team:** $20–25/mo [B, DB-S022].
- **BMP materials:**
  - Dandy Products (inlet protection manufacturer; distributors MISSING) [C, DB-S039];
  - SiteOne Landscape Supply (Illinois branches/terms MISSING) [D, DB-S040].
- **Price benchmark for BMP work:** IDOT 2022 awards [A, DB-S012]:
  - inlet filters $61.60–$176 each;
  - perimeter erosion barrier $1.93–$8.80/ft;
  - ditch checks $8.80–$25/ft;
  - stabilized construction entrance $70/sq yd.
- **Insurance:** Insureon small-firm medians (GL $88/mo, professional $67/mo, auto $268/mo) [D, DB-S007]. A real stormwater-inspector quote is MISSING.

## 4. Named prospective customers (32; CSV)
All are drawn from ECHO 2025–26 coverages, with an ECHO facility link and site counts.

- **Site/civil and GCs:**
  - Austin Tyler Construction (Elwood);
  - A Lamp Concrete Contractors;
  - Copenhaver Construction;
  - D Construction (Coal City);
  - Otto Baum (Morton);
  - AKRA Builders;
  - Henry Bros. (Hickory Hills);
  - Dunnet Bay;
  - Power Construction;
  - Wight & Company (Darien);
  - Pepper Construction;
  - ARCO/Murray;
  - Nicholas & Associates (Mount Prospect);
  - Leopardo (Hoffman Estates);
  - K-Five;
  - 41 North Contractors;
  - Lamp Incorporated;
  - Iroquois Paving;
  - Campanella & Sons.
- **Homebuilders:**
  - M/I Homes of Chicago;
  - Pulte;
  - CalAtlantic (Lennar Chicago);
  - NVR Ryan Homes Illinois;
  - D.R. Horton Midwest.
- **Public owners:**
  - Villages of Glendale Heights, Shorewood, Bensenville, Orland Park;
  - City of Crest Hill;
  - Bloomingdale School District 13;
  - Kane County DOT.
- **Out-of-state solar:** Nexamp (58 Illinois coverages; flagged as out-of-state headquarters).

## 5. Representative transactions
| Transaction | Revenue | Direct costs | Contribution | Evidence |
|---|---|---|---|---|
| A. 12-acre subdivision (Kane), peak month: 5 inspections including 1 storm, at $130 | $650 | inspector 6.25 h incl. drive $225; mileage $88; app $10 = **$323** | **$327 (50%)** | Price E within the $95–240 proxies |
| B. Same site, frozen-shutdown month: 1 inspection (ILR10 allows monthly [A, C7-S011]) | $130 | $63 | $67 | A/E |
| C. BMP ticket: replace 8 inlet filters and repair 150 ft of silt fence | $1,450 | materials $480; labour 8 h $256; truck/disposal $80 = **$816** | **$634 (44%)** | Priced below IDOT 2022 awards [A, DB-S012]; costs E |
| D. Rural 10-acre community-solar site, 4.5 inspections | $700 | inspector 10 h $365; mileage $284 = **$649** | **$51 (7%)** | E. Unviable unless clustered |

**Payment:** invoiced monthly; GCs pay net 30–60 (model DSO 45; E).

**Annualized per site:**
- about 45 inspections a year;
- revenue about $5,800–6,700 including some BMP work;
- direct contribution about $2,800–3,300 before overhead.

## 6. Customer acquisition
**Customer #1:**
- Run a weekly ECHO pull of new coverages within 40 miles (about 69 a month in Chicagoland [A, DB-S008]).
- Visit site trailers with a one-page "storm guarantee": an inspection within 24 hours of 0.5 inches, a report the same day, and a corrective ticket.
- Target the 306 "TBD operator" coverages too. The owner filed before picking a GC, so the owner or engineer may choose the inspector.

**Customers #2–10:**
- Ask each new GC client for its next sites. Repeat buyers dominate.
- Ask SWPPP-writing civil engineers for overflow inspections.
- Ask public-works directors whether contractor inspection records are weak, and let them refer the contractor.

**Customers #11–100:**
- Account management of about 15–25 repeat GCs.
- A part-time business-development role. Not in the model base, which explains the plateau.

**Funnel (base, E):**
- 15 qualified site leads a month → 40% proposal → 25% win, about 1.5 sites a month.
- Repeat/referral sites add 4 per 100 active sites per month.
- Site churn is 7% a month (average coverage life about 14 months; E).

**Unit economics:**
- CAC about $150 per site.
- LTV is about 14 months × about $300 contribution ≈ **$4.2k** per site.

**Founder sales time:** about 10–15 hours a week, ongoing, because sites expire.

## 7. Pricing strategy
- **Per-site monthly retainer** instead of per-inspection, so storm surges do not create billing disputes:
  - $450/mo under 5 acres;
  - $575/mo 5–20 acres;
  - $750+/mo above 20 acres or with dewatering.
- **Winter (frozen shutdown):** $150/mo.
- **Set-up visit and SWPPP map markup:** $350.
- **BMP work:** unit prices at about 70–90% of IDOT awards, or T&M at $85/h per worker plus materials (E).

**Floors and ceilings:**
- The public KDSWCD fee of about $58/month for oversight on 0–9 acres [A] is a floor for buyers' price expectations, not a comparable service.
- The $240 Fort Wayne monthly inspection is the ceiling proxy.

Model ARPC is $560/site-month blended (D).

## 8. Working capital and cash conversion cycle
| Active sites | Monthly revenue | AR (DSO 45) | AP + inventory | Net working capital |
|---|---|---|---|---|
| 10 | ~$5.6k | ~$8.4k | ~$0.5k | ~$8k |
| 50 | ~$28k | ~$42k | ~$3k | ~$39k |
| 200 | ~$112k | ~$168k | ~$13k | ~$156k |

Inspectors are paid every two weeks; GCs pay in 45–60 days. Working capital is the binding constraint on growth beyond about 50 sites.

**Model peak funding (including the owner draw from month 13):**
- about $52k base;
- about $24k base without the draw;
- about $186k conservative, a kill scenario.

## 9. Regulatory path
1. Form an LLC.
2. **Qualification:** complete the free USEPA CGP inspector course and exam [A, DB-S010]. ILR10 accepts this route, as well as PE/CPESC/CESSWI/CSI or any "knowledgeable person" [A, C7-S011].
3. **Credibility:** CESSWI within 12 months ($715 plus 6 PDH/yr) [B, DB-S011].
4. **No state licence.**
5. **Local rules:** some local ordinances require the project PE to inspect, e.g., Hodgkins [D, C7-S015]. Prevalence is MISSING, so check each municipality.
6. **Insurance:** GL, professional/E&O and auto. Premiums MISSING; modelled at $550/mo, E.
7. **Public-work BMP labour:** if BMP labour is performed on public works, Illinois prevailing wage (Cook laborer $53.00 + $39.11 fringes [A, DB-S004]) and IDOL certified payroll apply.

**Timing:** 2–4 weeks.

## 10. Operations workflow
1. **ECHO pull and site list.** *Automated script.*
2. **Site visit, proposal and contract.** *Human.*
3. **Set-up:** SWPPP map, BMP inventory, photo points. *Human, with AI building the checklist from the SWPPP PDF.*
4. **Scheduling:** weekly routes plus storm triggers. *Weather-API alert at 0.5 inches → automatic re-route.*
5. **Inspection:** photos, GPS, checklist. *Human. AI drafts the report from photos and notes; the inspector signs.*
6. **Corrective-action ticket to the superintendent; BMP crew dispatch if bought.** *Semi-automated.*
7. **Monthly invoice; AR follow-up.** *Automated.*

**Stack:**
- field app about $43/user;
- Claude Pro;
- weather alerts (E);
- about $250/mo in total.

**Capacity:** one storm triggers every site within about one business day, so one inspector covers about 25 sites (Stage C reasoning; E).

## 11. Competitive position and defensibility
**What accumulates:**
- repeat-GC relationships;
- route density in one corridor (I-55/I-80 Will County, for example);
- a compliance record (zero missed storm windows) that a superintendent can show IEPA.

**Weaknesses:**
- The service is copyable, and engineers can bundle it as a loss-leader.
- Self-inspection is legal, and the agency inspection count is low: 4,861 of 5,341 coverages show zero recorded EPA/state inspections [A, DB-S008]. Enforcement pressure, and therefore willingness to pay, may be weak.

Entry stays at 4.

## 12. Key risks and pre-mortem
| Loss | How it fails | Early warning |
|---|---|---|
| ~$5k | Superintendents say "we do it ourselves" or "the engineer includes it" | <3 signed sites from 40 site visits in the first season |
| ~$25k | First inspector hired at 15 sites; winter drops ARPC; GCs pay at 60+ days | Winter ARPC below $200; AR above 60 days |
| ~$50k | Price war at about $95/inspection, or a recession cuts new coverages; the model "competitor response" stress gives about $10k year-3 profit | New coverages in ECHO falling year on year; proposals lost on price |

**Missed-storm liability** (a client's violation blamed on us) is the E&O risk.

## 13. Validation plan
| # | Experiment | Cost | Success | Kill |
|---|---|---|---|---|
| 1 | Complete the EPA CGP course; build an ECHO watch for 40-mile-radius new coverages | $0 | Running in 1 week | — |
| 2 | Visit 40 new-coverage sites over 6 weeks (season starts about March) with a $450–575/mo retainer offer | ~$300 fuel/print | ≥3 signed paying sites | ≤1 signed |
| 3 | Price discovery: ask 10 civil engineers and GCs what they pay now; collect any written proposals voluntarily shared | $0 | Median ≥$110/inspection or ≥$450/site-month | Median <$90 |
| 4 | Ask KDSWCD and 5 public-works directors how often permittee weekly records are missing | $0 | They identify ≥10 deficient permittees a season | "Rare" |
| 5 | Winter test: share of December–February sites still active (ECHO plus drive-bys) | ~$100 | ≥50% still billing | <30% |

Total validation cost is about **$400**.

## 14. Revised scores and verdict
| fcf | roic | access | scale | resilience | entry | delegation | cash | feasibility | ai |
|---|---|---|---|---|---|---|---|---|---|
| 4 | 7 | 6 | 4 | 5 | 4 | 7 | 5 | 9 | 5 |

**Changes from Stage C:**
- fcf 5→4: base year 3 about $54k, plateau about $50–80k.
- roic 8→7: working capital at DSO 45.
- scale 5→4: high site churn caps a founder-led pipeline.

**Composite:** raw 5.38; evidence D gives an adjusted score of **5.27**.

**Gates:** G4_CEILING:WARN. The base case never reaches $100k/yr; the optimistic case reaches $168k in year 3 and $362k in year 5.

**Model results:**

| Scenario | Year-3 operating profit |
|---|---|
| Conservative | $4k |
| Base | $54k |
| Optimistic | $168k |

**Verdict: RESERVE.** Best used as a module inside a broader construction-compliance or site-services business. One possibility is cross-selling to SYN-006's public-works subs, who also need IDOL payroll on BMP crews.

**Research limitations (this session):**
- No private Illinois inspection price list was found; municipal engineering packets (e.g., North Aurora) blocked automated fetch.
- BLS inspector wages were not retrievable (API limit).
- Active vs stale ILR10 coverages and the share of GCs that self-inspect remain MISSING.
