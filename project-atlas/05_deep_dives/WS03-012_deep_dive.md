# WS03-012 — Overhead crane & hoist inspection, maintenance and repair (Stage D deep dive, batch DC)

> **Verdict: DROP**, though it can return as an add-on line if a crane-technician partner appears. Evidence stays at
> **C**:
> - prices B;
> - wages C;
> - repair pull-through E.
>
> **Base case (model):** never reaches sustained profit within five years.
>
> | Metric | Value |
> |---|---|
> | Year-3 operating profit | **−$38k** on $380k revenue (61 plants) |
> | Year-5 operating profit | −$42k on $714k revenue |
> | Peak funding | $733k ($541k without owner draw) |
> | Spend before first revenue | ~$94k |
>
> Only the optimistic case works: $193k in year 3, which needs 125 plants and $750/month per plant.
>
> **The decisive fact: inspection is cheap.**
> - Mazzella's list price is **$108–253 per crane** for a periodic inspection [B, C3-S001].
> - A federal hoist-inspection contract at the 183rd Wing **re-bid from ~$15.2k a year to $9,600** [A, DC-S025].
> - OSHA lets plants self-inspect [A, C3-S003, C3-S005].
>
> **What that does to the economics:**
> - A typical 8-crane plant yields ~$1.6k a year in inspections. Even assuming repairs at 2.5× inspection revenue, it
>   yields only ~$5.6k a year in total.
> - A $106k-loaded experienced crane technician generates about $21k a month of revenue capacity, so each technician
>   needs ~45 plants. A founder who cannot inspect cannot reach that number fast enough.
> - The incumbents' ~22% service margins rest on agreement bases and parts scale that a newcomer lacks
>   [B, C3-S007].

## 1. Specific initial niche
**What we sell:** fixed-price OSHA 1910.179 periodic (annual or quarterly) inspections with photo reports and a
compliance calendar, then repair of the deficiencies found:
- hooks, chain and rope;
- brakes;
- pendants and radio controls;
- VFD retrofits.

**Who we sell to:** mid-size steel service centres, fabricators, machine shops and forges with 3–20 cranes in the south
and west suburban metals corridor (Harvey, Lansing, Chicago Heights, Cicero, Alsip, University Park), then
DuPage/Kane.

**Size of the market:**
- **Illinois establishments** [C, C3-S014; WS03-S006]: 2,779 fabricated-metal, 1,266 machinery, 473 metal service
  centres, 77 foundries and 111 structural fabricators.
- **Census screen** [A, DC-S004]: 788 active private carriers hauling metal in 12 northern Illinois counties.
- **Crane share:** the share of these plants that run overhead cranes is MISSING. A crawl of 112 metals-company
  websites (home pages plus up to 25 linked pages each) found the word "crane" on 14. Only 6 of those described
  in-plant crane use.

## 2. Named operators
| Operator | Known facts | Level |
|---|---|---|
| Konecranes (Chicago-area branches) | Industrial Service Q3-26 sales €398M at 23.7% comparable EBITA; agreement base €351.7M. Chicago technician posting pays $22–48/hr | B, C3-S007; D, DC-S027 |
| Crane 1 Services (L Squared) | ~500 employees, 30 locations, 10 add-ons; Chicago service technician postings | C, WS03-S016 |
| Mazzella Companies | Published price list: $72–253 per crane; $150–160/hr; master distributor for Harrington and CMCO | B, C3-S001–S002 |
| Hoosier Crane; Hoist & Crane Service Group | Chicago locations | D, C3-S009 |
| Uesco (Alsip), U.S. Crane (Batavia), Simmers Crane | Family and regional builders and servicers; 24/7 service; 65+ years (Simmers) | D, C3-S008–S009, DC-S037 |
| Walter Payton Power Equipment LLC | USACE Illinois Waterway crane inspection & certification: $1.52M (2023–26), $0.96M (2018–24); Calumet Harbor crane repairs $18,964 | A, DC-S024, DC-S026 |
| MAS Rigging; Semper Supra LLC | 183rd Wing hoist inspections: $30,328 for 2024–26, then $9,600 for FY26 | A, DC-S025 |
| Sievert Electric Service & Sales; Kussmann Crane; Industrial Tool Products | Army awards in Illinois for bridge cranes, VFD retrofits ($336k, 2026) and crane systems | A, DC-S043 |

**What this shows:** the market is crowded and already served at both ends: by OEM and PE-backed nationals, and by
century-old local family firms.

## 3. Named suppliers / partners (see `09_databases/suppliers/WS03-012_suppliers.csv`)
| Partner | Role | Status |
|---|---|---|
| Mazzella | Parts source and competitor; its inspection and labor prices are **documented** [B] | Parts terms to a rival are assumed doubtful |
| R&M Materials Handling, Harrington, Gorbel | Hoist and crane OEMs selling through distributor/dealer networks | Terms unpublished, **assumed**; existing distributors may hold the territories [D] |
| CICB | Inspector training; recommends ~2,000 h of experience before the NCCCO inspector exams | **Documented** [D, C3-S006] |
| NCCCO | Voluntary certification | Fees MISSING (Cloudflare) |
| Grainger | MRO parts | Assumed |
| Aerial-lift rental | Runway access | Rates MISSING |

## 4. Named prospective customers
32 organisations are recorded in `09_databases/prospects/WS03-012_prospects.csv`.

**Crane or hoist use documented on their own sites:**

| Organisation | Evidence | Source |
|---|---|---|
| LB Steel (Harvey) | Overhead cranes in job requirements | DC-S029 |
| Mah Machine (Cicero) | Cranes 1–15 t | DC-S030 |
| Technox Machine (Chicago) | 15-t crane-handled parts | DC-S031 |
| Synergy Steel Structures (Lansing) | Recruits crane operators | DC-S032 |
| Pittco Architectural Metals (Elk Grove Village) | Overhead crane in job description | DC-S033 |
| 425 Manufacturing (Rockford) | 3-t crane | DC-S034 |
| Kloeckner Metals (University Park) | Crane capacity for 60,000-lb coils | DC-S028 |

**Public buyers:**

| Buyer | What they buy | Source |
|---|---|---|
| Illinois Tollway | IFB for overhead crane inspections and repairs | D, DC-S036 |
| 183rd Wing | Hoist inspections | A, DC-S025 |
| USACE Rock Island District | Crane inspection & certification | A, DC-S024 |
| MWRD | Hoist procurement | A, DC-S035 |

**Industry-typical, crane use not yet verified:** Lapham-Hickey Steel, Chicago Tube & Iron, Napco Steel, Clingan
Steel, Chicago Heights Steel, Calumet Brass Foundry and others.

Status: "prospect — not contacted".

## 5. Representative transactions
| # | Transaction | Revenue | Direct costs | Contribution | Payment |
|---|---|---|---|---|---|
| 1 | Annual periodic inspection of 8 cranes (5–30 t mix) at Mazzella list ~$170 each | $1,360 [B] | Technician 9.5 h (on site, travel, report) × $51 loaded [C/E] $485; truck $40 | **$835** | Net-45/60 PO |
| 2 | Hoist repair found at inspection: load chain, hook/latch, brake; 6 h × $150 + $1,400 parts | $2,300 [B rate; E scope] | Parts at 67% $938; technician 7 h $357; consumables $30 | **$975** | Net-45/60 |
| 3 | Federal small-purchase hoist inspection, 183rd Wing FY26 | $9,600 [A] | Technician ~40 h incl. travel to Springfield $2,040; lodging $900; truck $300 [E] | **~$6,360** | Net-30 federal; SAM registration required |

**What the table shows:**
- Each inspection technician-day is worth roughly $1.1–1.4k of revenue.
- Repairs carry the margin, but only if the plant buys them from us rather than from the OEM distributor that sells
  them their hoists.

## 6. Customer acquisition
**Customer #1.** Walk the Harvey, Lansing and Chicago Heights corridor with the lead technician: LB Steel, Synergy,
Chicago Heights Steel, Calumet Brass, Mah Machine. Offer a fixed-price inspection 10% below the published list, a photo
report within 48 h, and a repair quote with parts prices shown.

**Customers #2–10:**
- insurer loss-control and broker referrals (E);
- machinery dealers without crane service;
- federal small purchases (SAM.gov: 183rd Wing-type hoist inspections);
- the Tollway re-bid.

**Customers #11–100:**
- referrals, at 0.8 per 100 plants a month [E];
- bundling with rack and scale inspections (WS03-013/017);
- a second technician, hired at ~$21k/month of revenue.

**Funnel at full pace (all E):** 15 plant conversations → 7.5 quotes (50%; fixed-price quoting is the norm
[B, C3-S002]) → 2.25 wins (30%) a month.

**Unit economics (base):**

| Measure | Value |
|---|---|
| CAC | ~$435 per plant |
| Contribution per plant after parts, variable costs and the technician share | only ~$117/month |
| Payback | ~4 months |
| 5-year LTV at 1.2%/month churn | ~$5k |

**Effort:** about 15 founder hours a week, plus about 4 hours a week of the technician's time on walk-throughs.

## 7. Pricing strategy
- **Inspections:** per crane, $100–200 periodic and $70–130 frequent, with a ~$450 minimum visit (E). Publish the list,
  as Mazzella does.
- **Repairs:** $140–150/hr standard and ~$195/hr emergency (E). Parts at cost + 35%.
- **Upsell:** modernisation (VFDs, radio controls). Federal VFD-retrofit awards show the demand [A, DC-S043].

**The price ceiling** is set by published lists, by self-inspection (OSHA allows it), and by aggressive re-bids. The
183rd Wing re-bid fell 37% per year-equivalent. No new entrant can raise these prices.

## 8. Working capital and cash conversion
Model assumptions: ARPC $470/month, DSO 50, inventory 15 days, DPO 30.

| Plants | Revenue/mo | AR | Parts stock | AP | Net WC | Trucks |
|---|---|---|---|---|---|---|
| 10 | $4.7k | $7.8k | $0.7k | $1.3k | ~$7k | 1 ($45k) |
| 50 | $23.5k | $39k | $3.3k | $6.6k | ~$36k | 2 |
| 200 | $94k | $157k | $13k | $26k | ~$144k | 5 |

**Cash cycle:** the conversion cycle is about +50–60 days, because manufacturers pay at net-45/60.

## 9. Regulatory path
1. **Entity and tax.** Illinois LLC, EIN, IDOR registration for parts sales [A, WS16-S036].
2. **OSHA 1910.179** [A, C3-S005]:
   - "designated" persons inspect and repair, and no licence or third-party inspector is required;
   - rerating needs a qualified engineer or the manufacturer;
   - monthly certification records are kept for hooks, chain and rope;
   - ASME B30.2 is paywalled and was not read. It binds through customer contracts and insurers.
3. **Illinois or Chicago licence** for in-plant crane inspection or repair: MISSING (ilga.gov unavailable).
   - Electrical work on crane controls inside Chicago may fall under city electrical-contractor licensing. Also
     MISSING; must be checked before VFD work.
4. **Voluntary credentials.** NCCCO inspector certification. The prep provider recommends ~2,000 documented hours
   [D, C3-S006], so the founder cannot be the inspector within about 2 years.
5. **Insurance.**
   - GL with completed operations; plants commonly require a $1M/$2M limit plus a $5M umbrella (E).
   - Workers' comp (a high-hazard class), commercial auto, inland marine for tools and test equipment.
   - Premiums are MISSING; the model budgets $1,500/month (E).
6. **Federal work.** SAM.gov registration. The buyer wants a "properly licensed and certified" company: buyer-specific
   wording, not a state licence [A, DC-S025].

## 10. Operations workflow (lead → cash)
| Step | Who / what |
|---|---|
| Site survey: crane list, capacities, last inspection | Technician plus founder |
| Fixed-price quote, then PO | Template |
| Schedule around shutdown windows | Dispatcher, or the founder early on |
| Inspection on a tablet checklist | Technician |
| AI-drafted report with deficiency photos and repair quote | Human sign-off by the technician; the liability point |
| Approval, parts order, repair and load test (test weights rented) | Technician |
| Invoice net-45/60, then calendar the next inspection | Automated |

**Stack:** inspection app plus CRM ~$200/month, AI drafting ~$100/month, QuickBooks. AI shortens report writing, but
the technician hours that make up ~42% of revenue stay human.

## 11. Competitive position and defensibility
**What builds up:**
- inspection histories;
- corridor density;
- the technician's reputation;
- possibly modernisation projects.

**What does not build up:**
- OEM parts access. Distributors such as Mazzella hold the territories.
- Inspection pricing power.

**Exit:** PE roll-ups such as Crane 1 buy independents, so a book of plants has exit value. That is evidence the niche
can be built by *acquisition*, which the mandate excludes at entry.

## 12. Key risks and pre-mortem
| Loss | Failure path | Early warning |
|---|---|---|
| **$5k** | No experienced crane technician will leave an incumbent for a start-up, even at $35–45/hr | <2 qualified applicants with 5+ years of experience after 4 weeks |
| **$25k** | Technician on payroll for 4–6 months with <10 plants; plants buy inspections but send repairs to their OEM distributor | Repair revenue below 1× inspection revenue on the first 10 plants |
| **$50k** | Liability incident after our sign-off (dropped load); insurer demands a $5M umbrella; plant or federal price war | Insurance quote >$30k/yr; lost re-bids at a 30%+ price cut |

**Model stresses:** every stress case keeps year-3 operating profit negative. Labor +20% gives −$83k; hires needed 30%
sooner give −$114k.

## 13. Validation plan (only if a technician partner emerges)
| # | Experiment | Cost | Success | Kill |
|---|---|---|---|---|
| 1 | **Technician-partner search:** recruit an experienced crane technician for profit share or equity | $500 ads | ≥2 qualified candidates | None |
| 2 | **Subcontract test:** pay an independent crane inspector (1099) to deliver 3 paid inspections; measure repair pull-through | ~$500 net | Repairs ≥2× inspection revenue within 90 days | <1× |
| 3 | **Insurance quote** for GL with completed operations plus umbrella (founder-run) | $0 | ≤$20k/yr | >$30k/yr |
| 4 | **Corridor demand test:** 15 plants asked for crane count, current vendor and inspection due date | $100 | ≥5 quote requests | <2 |
| 5 | **Bundle test** with rack and scale inspection in the same visits | $0 | Per-visit revenue ≥$2.5k | — |

## 14. Revised scores and verdict
| Key | Stage C | Stage D | Reason |
|---|---|---|---|
| fcf | 4 | **2** | Base negative through year 5; only the optimistic case exceeds $100k |
| roic | 5 | **2** | $0.5–0.7M cumulative funding in base |
| access | 5 | 5 | Identifiable plants; incumbent relationships |
| scale | 6 | **5** | Technician-limited; ARPC low |
| resilience | 6 | 6 | Mandated inspection, but self-inspection is allowed |
| entry | 4 | **3** | Published low prices, OEM distributors, PE roll-ups |
| delegation | 6 | 6 | Technician-run once hired |
| cash | 5 | 5 | Net-45/60 |
| feasibility | 7 | 7 | No licence identified; liability insurance cost unknown |
| ai | 4 | 4 | Report drafting |

Raw ≈ 4.0; evidence-adjusted (C) ≈ **4.2**.

**Model base case:** year-3 operating profit **−$37,998**; year-5 −$42k.

**Verdict: DROP** as a stand-alone business for this founder. Keep the prospect list for a possible plant-inspection
bundle.

*Limitations:*
- the share of plants with cranes is MISSING;
- the repair pull-through ratio is E, derived from Konecranes incumbent ratios (~3.5×);
- the Tollway bid page was blocked;
- the Illinois/Chicago licence question and insurance premiums are MISSING.
