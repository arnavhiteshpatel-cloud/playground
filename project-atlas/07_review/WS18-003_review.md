# WS18-003 — Stage F adversarial review (batch F3)

**Subject:** Junk removal and cleanouts, independent, B2B-referral-led (Chicago north/west side and near-west suburbs).
**Reviewer:** independent Stage F reviewer, batch F3, 2026-11-28. I did not write any of the material reviewed.
**Read:** playbook, materials, Stage D deep dive, Stage C memo, assumptions/results JSON, prospect and supplier CSVs, and the cited sources.
**Method:**
- Re-opened 12 cited sources, including the three Item 19 PDFs, which I read line by line.
- Re-queried the Chicago licence register.
- Re-ran `tools/fin_engine.py` with alternative drivers (`/tmp/claude-0/atlas_scratch/F3/scripts/rerun.py`, `rerun2.py`). The finalist's model files were not modified.
- New sources are F3-S007 to F3-S012 in `07_review/sources_F3.jsonl`.

---

## 1. Verdict

**Fails as a primary first-company candidate.** Stage E's "reserve/conditional" label is fair only as a fallback that is cheap to test, and I would demote it to that.

**What is genuinely good:**
- Stage E already did the hard honest work. It caught the College Hunks junk-and-moving contamination, the U-Haul prohibition and the lead-cost understatement.
- The validation plan costs under $3k and can stop the project before a truck is bought.
- Cash collection at completion is real.

**Where it overstates the business:**
- The zone-1 plateau of about 106 jobs/month and $545k/yr is reached by an *unbranded* independent within about 30 months. That sits *above* the Junk King system median for all branded units ($436k) [B].
- The $430 average ticket is national and branded, set against Chicago aggregator averages of about $246 [D].
- The multi-zone, ops-manager structure does not survive modest corrections.

**Corrected evidence-adjusted view.** At reviewer drivers, as a single-zone owner-operator business (operating profit before owner pay):

| | Reviewer base | Stage E base |
|---|---|---|
| Year 3 | **≈ $35k** | $49k |
| Year 5 | **≈ $49k** | $83k |
| Revenue at year 5 | ≈ $420k | $927k |
| Peak funding, no draw | **≈ $136k** | $90k |
| Peak funding, standard draw | ≈ $202k | $142k |

- With Stage E's multi-zone structure kept, the reviewer base turns year 5 negative (−$11k).
- **Upside:** Stage E's own *single-zone* variant at Stage E drivers, about $105k in year 3 and $103k in year 5.
- **Conservative:** negative throughout.

**On delegation:** the business *can* become delegable and multi-crew operationally. At base economics, though, the manager layer consumes the owner's cash. Franchise evidence agrees: College Hunks stores of 60+ months earn a median 8.8% EBITDA, and its GM-run corporate stores earn about 4% [B].

## 2. Factual errors found

| # | Claim (where) | What the source / data actually shows | Correction |
|---|---|---|---|
| 1 | "College Hunks pays a median $32 per lead and closes 40%, about $80 per paid-lead job" (playbook header; CAC source) | In the 2025 Item 19 performance table, $32 and 40% are the **all-franchised** medians. The **junk-only** column shows median CPL **$42** and lead-to-close **51%**, which also gives about $82 per job [B, F3-S008] | The net cost per job is about the same, but the junk-only line is the right citation. Also: junk-only stores average 3 territories and complete a median 2,345 jobs a year, about **65 jobs per territory per month** for a branded operator |
| 2 | Base plateau "~106 jobs × $430 ≈ $545k/yr, between Junk King median $436k and 1-800-GOT-JUNK 12–24-month average $512k" (`founder_leads_per_month` source) | Junk King's $436k median is for **all** 166 continually operated branded units, many of them mature. The quartiles are bottom $194k, third $355k, second $556k and top $1.115M [B, F3-S009 re-read]. 1-800-GOT-JUNK's 12–24-month figure is for multi-subterritory franchisees with a national call centre. College Hunks' call centre books **48%** of junk sales [B, re-read] | An unbranded independent's base plateau should sit near the Junk King **third quartile** ($355k), not the system median. Reviewer base plateau is about 80 jobs at $390 (≈ $375k/yr) |
| 3 | Base ticket $430 [B] | The Item 19 tickets are branded national averages (Junk King $399, CH junk-only $443). The playbook's own Chicago anchors are HomeGuide half-truck ≈ $200–300 / full ≈ $400–450 and Angi Chicago average ≈ $246 [D, E-WS18003-S021]. The playbook notes it is "genuinely contested" but puts the high number in base | **$390** base. The B2B full-load mix justifies more than $246, not more than the branded national average |
| 4 | SWANCC Glenview has "short hours" | Re-read: Mon–Fri **6:00–10:00 AM and 2:00–3:30 PM, closed 10 AM–2 PM**; Saturday 6–12; self-unload; credit card only; vehicles ≥24 ft may be refused [B, F3-S007] | Material operationally. A crew doing 9 AM–2 PM jobs can tip only in a 90-minute afternoon window or the next morning. Glenview is also 30–45 minutes from the west side. Private stations (LRS Packers Ave, Groot, WM) remain the real outlet, and their **gate rates are still MISSING**. The 2.5 jobs/truck/day capacity (55/month) is unproven |
| 5 | Commercial auto "~$600–900/mo per box truck"; Insureon debris-removal auto **$268/mo** cited as the floor | Insureon's **box-truck** medians (June 2025): commercial auto **$909/mo**, workers' comp **$673/mo**, GL $52 [D, F3-S010]. The $268 debris-removal median covers mixed, mostly smaller vehicles | Base truck auto should be about $900+/month in Cook County. Add about $150–300 per truck per month, i.e. +10% overhead in the reviewer base |
| 6 | "1-800-GOT-JUNK … is the only junk-removal brand that holds [scavenger licences]" | Confirmed: KLGR LLC holds 10 Private Scavenger Vehicle licences plus an office licence; there are 29 Junk Peddler licences. **No active licence appears under any DBA containing "JUNK" for Junk King or College Hunks** [A, F3-S012] | The licence regime appears weakly enforced: most active haulers hold neither licence. That lowers the barrier for the founder **and** for every competitor. Treat the licence as a compliance item (licence anyway), not a moat |
| 7 | Junk Peddler "$150 per 2 years" [D] | The BACP fact sheet and the amlegal code page both returned 403 this session | Still unverified. The private-scavenger fee is still MISSING. Experiment 1 (call BACP) remains necessary |
| 8 | Lead cost $65 blended / $80 paid | Independent vendor estimates (Q2 2026): junk LSA CPL $30–65 with 60–70% booking for fast responders, about **$45–110 per booked job**; one example of a $55 lead at 65% gives about $85/job [D, F3-S011] | The $80 paid-lead figure is **reasonable**. The $25 "account-servicing" CAC on 30% of jobs is unevidenced (see §3). Reviewer blended CAC is **$80** |

## 3. Unsupported or over-stated claims

| Claim | Stated level | Warranted level and comment |
|---|---|---|
| "Repeat B2B accounts can supply ~30% of jobs at near-zero CAC" (it drives CAC $65 and the optimistic path) | E | **E, and internally inconsistent.** The model's repeat driver (`referral_new_per_100_active` = 6) generates only about 6 repeat jobs per 100. The 30% B2B share exists only in the CAC blend, not in job generation. There is no evidence on cleanouts per manager per month (the "1–4" is E) |
| Self-storage defaulted units as a recurring channel (Extra Space 47 licences, CubeSmart) | A (licence count) | The licence count is A. **Demand is E.** Illinois lien sales transfer contents to winning bidders, who clear the unit; only unsold or abandoned units need a hauler (volume MISSING). Extra Space and CubeSmart are REITs that typically run district or national vendor programmes with insurance and vendor-onboarding requirements a new LLC may not meet (E) |
| Property and association managers (Habitat, FirstService, Associa, Sudler) as top prospects | A (licence) | For condos, most junk belongs to residents, who hire their own hauler. Rental turnover crews and building engineers often use dumpsters or the building's waste hauler. Large PMs onboard vendors through compliance platforms with COI and additional-insured requirements (E). **Mid-size rental PMs and independent restoration firms are the realistic first accounts.** The big names are for later |
| "Every operating role is a commodity labour-market job" (delegation 7) | C | True operationally [C]. Economically, the delegation layer costs more than base margins cover (§4, §9) |
| "Downside capped by truck resale (60–70%)" | E | Plausible but unevidenced. Penske asking prices are B for asking, not realised resale |
| "Single-zone founder-run y5 $103,410" as the honest fallback | Model | Only at Stage E drivers. At reviewer drivers the same structure gives year 5 ≈ $49k |
| Evidence level B for economics | B | The Item 19s are B **for branded units**. Ticket and plateau for an unbranded Chicago independent are D/E. **Warranted overall: C.** This disagreement is preserved |

## 4. Financial model audit

**Reproduction.** The engine reproduces base year-3 $49,282, year-5 $83,289 and peak funding $142,264 / $90,179 exactly.
- Crew labour at 25% of revenue charges both crew members, including the founder while on the truck. That is conservative and correct.
- Disposal at 11% after diversion is plausible at $100/ton, but private gate rates are MISSING.

**Top-5 drivers, challenged:**

| Driver | Stage E base | Independent evidence | Reviewer base |
|---|---|---|---|
| `onetime_revenue_per_new_customer` (ticket) | $430 | §2 #3: Chicago aggregator averages ≈ $246; branded national $399–443 | **$390** |
| `founder_leads_per_month` (zone-1 plateau) | 245 (~106 jobs) | §2 #1–2: about 65 jobs per *branded* territory per month; Junk King third quartile $355k | **185** (~80 jobs incl. repeat) |
| `cac_per_new_customer` | $65 | §2 #8: $45–110 per booked job; the B2B $25 share is unevidenced | **$80** |
| `onetime_gross_margin_pct` | 0.64 | Chicago laborer median $40,550 [C, re-verified]; box-truck WC median $673/mo [D]; SWANCC $100/ton plus item fees; private rates MISSING | **0.62** |
| Overhead (insurance, yard) | as built | §2 #5: auto about $900/mo per box truck | **×1.10** |

**Re-runs** (operating profit before owner pay; `rerun2.py`):

| Run | Year 1 | Year 2 | Year 3 | Year 4 | Year 5 | Year-5 revenue | Peak (draw) | Peak (no draw) | 10-yr deployable |
|---|---|---|---|---|---|---|---|---|---|
| Stage E base (reproduced) | −$22,511 | $58,292 | $49,282 | $83,880 | $83,289 | $926,502 | $142,264 | $90,179 | $30,895 |
| Reviewer drivers, Stage E structure (zone 2, dispatcher at $35k/mo, ops manager) | −$45,851 | $1,001 | $34,878 | $46,344 | **−$11,282** | $422,960 | $260,959 | — | $0 |
| **Reviewer base, single-zone owner-operator** (dispatcher at $45k/mo; no zone 2 or ops manager) | −$45,851 | $1,001 | **$34,878** | $46,344 | **$49,383** | $422,960 | **$201,563** | **$135,934** | $0 ($185,554 with no draw) |
| Reviewer conservative, single-zone (ticket $370, 150 leads, CAC $95, GM 0.58) | −$56,081 | −$32,809 | −$13,980 | −$15,546 | −$14,450 | $325,353 | $417,288 | — | $0 |
| Reviewer upside = Stage E single-zone variant at Stage E drivers | −$22,511 | $58,292 | $104,979 | $98,563 | $103,410 | $617,585 | $117,128 | $90,179 | $151,789 |

**Capital:**
- The reviewer base needs about **$136k at risk even with no owner draw**: truck #1 ($45k), truck #2 at 60 jobs ($42k), and about two years of ramp losses.
- That exceeds the founder's ~$100k conditional backing. Stage E's own base ($142k with draw) also exceeds it.
- G1 technically passes, because the truck is bought before revenue at only about $45–55k. But the **ROIC is poor**: year-3 operating profit ÷ peak no-draw funding ≈ **26%**, or ≈ 17% with the draw.
- Leasing trucks lowers peak funding but, per Stage E's variant, cuts year-3 profit to about $19k.

**Working capital.** Negligible, as stated. Receivables are small; disposal is paid at the scale.

**Founder-draw logic.**
- In the reviewer base, the $4k/month draw from month 13 is financed by capital for 3+ years.
- In the conservative case it is never covered.
- The honest framing is no owner pay until monthly operating profit clears about $5k. In the reviewer base that happens around year 3–4, not month 13.

## 5. Customer acquisition challenge

**Consumers.**
- LSA and Google Business Profile are accessible and cost per lead is reasonable (§2 #8).
- But LSA ranking rewards review count and responsiveness. In Chicago the leads are contested by 1-800-GOT-JUNK (10 licensed trucks), Junk King, College Hunks, $79-per-item marketplaces (Dropcurb, LoadUp) and dozens of unlicensed micro-haulers.
- A new profile with no reviews will not get 245 leads a month in year 2.

**B2B.**
- The incumbents' B2B motion is national accounts and franchise-brand trust. College Hunks and 1-800-GOT-JUNK have commercial programmes; local micro-haulers win on price.
- The realistic first 10 B2B customers are:
  - owners of independent restoration firms (Real Restoration, Redefined, Big Shoulders);
  - small and mid-size rental PMs and landlords;
  - estate-sale and senior-move managers.
- They will require a COI with $1M/$2M GL, auto and WC, additional-insured wording, a W-9, and one flawless trial job.
- **Experiment 2 is the right decisive test.** Its pass bar (≥3 trial orders, ≥3 accounts reporting ≥2 cleanouts/month) should be scored on **reorders within 60 days**, not self-reported frequency.

**Access score 7 → 6**: consumer access is high, but B2B access to the named large prospects is overstated.

## 6. Supplier / partner accessibility

| Partner | Risk |
|---|---|
| **Private transfer stations** (most likely to constrain) | SWANCC accepts contractors, but with a midday closure. Private stations' self-haul acceptance, account terms and rates for an unlicensed or newly licensed box truck are **MISSING**. If they require a Chicago Private Scavenger licence or a commercial account history, disposal becomes the bottleneck |
| **Commercial truck rental for the pilot** | U-Haul is excluded [B, re-verified: junk and moving companies are ineligible for business accounts]. Penske/Enterprise debris terms are MISSING. A subcontracted insured hauler is the realistic pilot route |
| **Insurers** | Box truck with hired drivers and lifting injuries. Expect $20k+/yr all-in for one truck and two employees once workers' comp is on payroll (Insureon box-truck auto plus WC medians ≈ $19k/yr [D]). This is near the playbook's $22k kill line, not its ≤$15k pass line |
| **Truck financing** | Founder credit unknown |

## 7. Legal / regulatory challenge

- **City licence category is unresolved** (Junk Peddler vs per-vehicle Private Scavenger), and the fees are unverified. Enforcement looks weak (§2 #6).
  - Licence anyway: B2B onboarding and LSA screening ask for registration and insurance [B].
  - Get a written answer from BACP.
- **Suburban hauler licences** (Evanston, Oak Park, Skokie, Park Ridge, Elmwood Park) are still MISSING. Several suburbs franchise residential refuse collection; confirm that cleanout hauling is not restricted.
- **ICC Household Goods authority** applies to "transporting household property for hire" [A, re-verified]. A clean disposal-only service is probably outside it, but donation delivery, "move-outs" or estate work moving items between homes may fall inside. Legal read needed before offering those.
- **Workers' compensation** is mandatory from the first hire. The class code (refuse collection vs trucking vs moving) drives cost and is not verified.
- **Special wastes.** EPA §608 refrigerant chain of custody [A] and the Illinois e-waste landfill ban [A] are correctly handled. Add a written asbestos/lead refusal and a needle/biohazard SOP for hoarding and eviction work.
- **Eviction cleanouts** carry legal risk. Never touch a unit without written authority showing the eviction order has been executed; the playbook says this correctly. Attorney review of the B2B terms is required.

## 8. Competitive response

- The 10-truck licensed 1-800-GOT-JUNK franchise and the other brands own branded search. They can absorb a newcomer by out-bidding on LSA and Google Ads in peak months.
- Marketplaces set a $79 single-item price floor, which makes single items a loss for an independent (playbook transaction C).
- Micro-haulers undercut on B2B.
- **Underestimated:** restoration franchises (SERVPRO, ServiceMaster) and PMs can self-perform with a dumpster. Dumpster rental (Bin There Dump That and others) is a direct substitute for full-load cleanouts, which are the very jobs that carry the business.
- Entry 3 is right. The wedge (a 1-hour photo quote and 48-hour slot) is copyable in a week.

## 9. Founder execution and delegation realism

- **Months 1–12:** physical labour on the truck (Stage E correctly costs it).
- **Years 2–3:** sales, dispatch and quality control.
- A crew lead and dispatcher are standard hires. A field ops manager ($6,500/month) is affordable only above about $600k of revenue, which the reviewer base never reaches. A GM (about $109k median [C]) is affordable only near $2M of revenue at optimistic margins.
- **Can it become a delegable multi-crew business with real owner cash?** Operationally, yes. Financially, not at base. Franchise data show margins *falling* with GM delegation (corporate stores about 4%, 60+ month franchisees 8.8% median EBITDA after fees [B]).
- Delegation 7 → **6**: roles are standard, but delegating them destroys the base margin.

## 10. Pre-mortem

| # | Most plausible failure | Early indicator | Cheapest preventive test |
|---|---|---|---|
| 1 | **Volume never reaches plateau.** No-review LSA profile, branded competition, B2B accounts that order once. Plateau stalls at 40–60 jobs/month on 2 trucks' fixed costs | Fewer than 25 jobs/month by month 6; B2B reorder rate <30% within 60 days | Experiment 2 scored on *reorders*; LSA test capped at $1,000 before any truck purchase |
| 2 | **Margin squeeze.** Disposal (private gate rates, midday SWANCC closure, mattress and appliance fees), Cook County box-truck auto and WC push gross margin below 60% and fixed costs above $4k/month for one truck | Disposal >13% of revenue; insurance indication >$18k/yr | Experiments 3 and 5 (insurance indications and disposal map) at $0, before the LLC is formed |
| 3 | **Capital overrun.** Truck #2 bought at 60 jobs; peak funding passes $100k (reviewer base $136k with no draw) while operating profit stays at $35–50k | Cash below 3 months of fixed costs at the truck #2 decision | Hard rule: a second truck only after 2 months above 60 jobs **and** monthly operating profit >$5k; otherwise subcontract overflow |

## 11. Corrected scores

| Key | Stage E | Stage F (reviewer) | Reason |
|---|---|---|---|
| fcf | 3 | **2** | Reviewer base years 3–5 ≈ $35–49k before owner pay |
| roic | 4 | **2** | Year-3 operating profit ÷ peak funding ≈ 26% (no draw) / 17% (draw) |
| access | 7 | **6** | Consumer search is open but branded; large B2B names are gated by onboarding; storage demand mostly absorbed by lien-sale buyers (E) |
| scale | 4 | **3** | Margins fall with delegation [B]; multi-zone turns negative at reviewer drivers |
| resilience | 5 | 5 | Mildly cyclical (moves, estates, renovations) |
| entry | 3 | 3 | Commodity; weak licence enforcement cuts both ways |
| delegation | 7 | **6** | Standard roles, but the delegation layer consumes base profit |
| cash | 9 | **8** | Paid at completion, but B2B net-30 and truck capex |
| feasibility | 7 | 7 | Light licensing (unresolved category); WC/auto cost and ICC edge cases |
| ai | 4 | 4 | Photo quotes and booking; incumbents already have both |

- **Composite:** raw **3.97**, evidence-adjusted (C, k = 0.85) **4.12**; at Stage E's B it would be 4.02. Stage E was 4.82 / 4.83.

**Bottom line.** Stage E already corrected most of Stage D's optimism. The remaining overstatement is that an unbranded newcomer reaches a branded unit's median volume at a branded national ticket within 30 months.

Corrected to Chicago evidence (Junk King third-quartile volume, a $390 ticket, $80 paid-lead cost, box-truck insurance and the SWANCC hours), the business earns about $35k in year 3 and $49k in year 5 before owner pay. It needs about $136k at risk even without a draw, which is above the founder's conditional $100k. It can become a delegable multi-crew company, but at base margins the managers take the owner's cash.

Keep it only as a **fallback** to be tested for under $3k (experiments 1, 2, 3 and 5) if a primary finalist fails. Upgrade it only if experiment 2 shows ≥3 B2B accounts **reordering** within 60 days and the insurance plus disposal map comes in at ≤$15k/yr and ≤$100/ton.

## 12. Citations spot-checked (opened this session)

| Source | Result |
|---|---|
| WS18-S001: Junk King Item 19 | Confirmed: average $553,959 / median $435,663; quartiles; $399 average ticket; labour 20.6%, dumping 7.2% |
| E-WS18003-S001/S002, C8-S017: College Hunks Item 19 | Confirmed, but the CPL/close citation should use the junk-only column ($42 / 51%) (§2 #1); 48% call-centre share confirmed |
| E-WS18003-S003: 1-800-GOT-JUNK Item 19 | $220,855 / $511,647 / $422,996 tenure averages present (redline-overlaid text) |
| E-WS18003-S004: 1-800-GOT-JUNK pricing blog | Confirmed: $107–396 / $396–600 / $600–1,099 |
| DF-S016: SWANCC Glenview | Rates confirmed; hours are more restrictive than "short" implies (§2 #4) |
| DF-S015 / E-WS18003-S013: Chicago licences | Confirmed (KLGR 10 Private Scavenger Vehicle; 29 Junk Peddler) via the current-licence dataset |
| E-WS18003-S006: U-Haul business FAQ | Confirmed: junk-removal firms ineligible |
| WS18-S014: ICC Household Goods | Page confirmed |
| DF-S018: Naperville cleanout listing | Confirmed: $814,489 revenue, $219,912 cash flow, $284,999 asking |
| DF-S020: O*NET hand laborers | Page fetched (Chicago median used, $40,550) |
| E-WS18003-S008: Insureon debris-removal costs | Page fetched. Its $268 auto median is not a box-truck figure (§2 #5) |
| E-WS18003-S018: Junk Peddler fact sheet | **403**, unverified |
| E-WS18003-S021: HomeGuide Chicago | **403** this session; values taken as recorded |
