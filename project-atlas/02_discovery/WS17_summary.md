# WS17 — Automotive, fleet & equipment aftermarket: discovery summary

35 records (WS17-001…035), 22 sources. Access date 2026-11-28.

## Method and limitations
The shared web-search budget ran out after about 10 searches. Everything after that came from
**primary sources fetched directly**:
- the FMCSA Company Census API;
- the CFR via Cornell LII (eCFR and fmcsa.dot.gov blocked automated access);
- 92 Ill. Adm. Code 451;
- SEC EDGAR 10-Ks and XBRL data for LKQ, Copart, RB Global, GPC, Rush and Ryder.

ilga.gov returned 503 errors, so Illinois statute details rest on search excerpts and a D-level surety-broker guide.
The BLS wage data and Census County Business Patterns could not be reached: BLS blocked download and its API hit its
daily quota; the Census API now needs a key.

**As a result, the economics of nearly every record (prices, wages, margins) are E-level.** Market size and mandates are
A-level. Read the rankings as a prioritized validation list, not as conclusions.

## Landscape
**The Chicago fleet base is large and can be identified record by record** [A, WS17-S001]. Across the 8 counties (Cook,
DuPage, Will, Lake, Kane, McHenry, Kendall, Grundy) there are 36,851 active carriers, of which 25,049 updated their
MCS-150 in 2024 or later. Among those recent filers:
- **17,611 carriers** run 1–5 power units.
- **5,288 carriers** run 6–100 power units (about 120,800 units). Of these, 4,442 are for-hire and 842 are private-only.
- The 6–100 PU group reports **52,879 owned and 42,998 term-leased trailers**.
- **3,325 carriers** flag construction cargo, 824 utility, 1,261 hazmat.

Mid-size carriers cluster in Chicago (535), Schaumburg (177), Naperville (169), Plainfield (160), Aurora (138) and Elk
Grove Village (134). Every record carries the public name, address and fleet size, so buyers can be found cheaply. The
caveat is that the counts are self-reported and power-unit totals include outliers.

**Incumbent benchmarks** [A]:

| Company | Key figures |
|---|---|
| Rush (S021) | Aftermarket revenue $2.52B at about 36.9% gross margin. Parts gross margin 28–30% vs service/collision 66–68%. Absorption 130.7%. New Class 8 gross margin fell to 8.6% in the freight recession. |
| Ryder (S022) | Fleet Management Solutions EBT margin 8.6%. "SelectCare and other" (maintenance) $680M. Runs on-demand mobile maintenance (Torque). |
| LKQ (S017) | Gross margin 38.6%, operating margin 7.3%. |
| Copart (S018) | Operating margin about 36%. |
| RB Global (S019) | Operating margin 15.5%. |

The lesson: **labor-led service earns the margin; parts, vehicles and fuel are thin.** Network-effect auction margins
(Copart, RB Global) are out of reach for a new entrant.

## Strongest candidates (all need price validation)
1. **WS17-001 DOT compliance management** for 2–100 PU carriers. The demand is mandated: DQ files under 391.51,
   Clearinghouse queries under 382.701, and inspections. It needs little capital, the buyer list is public and
   quantified, the roles are admin jobs that can be delegated, and AI tooling is genuinely useful. Weaknesses: crowded,
   carrier churn in recessions, and distrust created by scam "compliance" mailers.
2. **WS17-009 Outsourced fleet maintenance management** for 15–300-vehicle service fleets. Ryder's SelectCare validates
   demand at the top end. Capital stays low if vendors bill clients directly. The open risk is proving savings to SMB
   fleets.
3. **WS17-006 Mobile trailer repair/PM**, with liftgate repair (WS17-024) as a service line. The verified local
   trailer base is very large, and trailer techs are easier to train than diesel engine techs. Caveat: Illinois's own
   test regime limits a mobile "annual inspection" product.
4. **WS17-004 Mobile PM for light/medium-duty service and delivery fleets.** Demand is non-discretionary and incumbents
   validate it. Hiring technicians is the key risk.
5. **WS17-008 Illinois Official Testing Station.** Testing is state-mandated: semiannual for intrastate vehicles,
   annual for interstate. There are about 260 stations statewide. A permit needs a $1,000 bond and a Certified Safety
   Tester, which gives a small moat. Customers pay at the time of service. Missing: test fees and the CST process.
6. **WS17-018 Mobile ADAS calibration.** Demand is rising, buyers are concentrated B2B shops, and LKQ (Elitek)
   validates the service.
7. **WS17-023 Forklift PM route** in a dense warehouse market, supported by OSHA's daily-examination regime.
8. **WS17-017 DPF cleaning.** A recurring diesel-maintenance niche, helped by a slower EV transition. Equipment capital
   and pricing still need checking.

**A stacked play looks strongest:** compliance subscription (001), then trailer/PM routes (006/004), then an OTS lane
and shop (008/034). The compliance relationship would feed paid service work, and the mandated test lane would anchor
customer retention.

## Surprises
- **Illinois runs its own periodic safety-test program** [A, S007/S008]. Testing happens inside permitted OTS
  buildings, with private stations reserved for firms testing 75+ of their own vehicles. The national "mobile DOT
  annual inspection" model (49 CFR 396.17 with 396.19 inspectors) is therefore weaker for Illinois-based units, and the
  OTS permit is the real Illinois-specific opening.
- **Rush's 10-K reports EPA moves to repeal its GHG endangerment finding**, while noting EVs would reduce parts and
  service demand. Diesel aftermarket demand (DPFs, trailers, diesel repair) looks more durable than EV narratives
  imply.
- **Mobile fleet washing is not a cheap, easy route business.** Federal MS4 rules require cities to prohibit
  non-stormwater discharges, and only *residential* car washing is listed as an allowed flow [A, S013]. Add Chicago
  winters and spending that fleets cut first in downturns.

## Looked good but fails
- **Used truck/trailer dealing** (010): needs a $50k bond, a dealer premises and inventory, and it is in a freight
  recession.
- **Salvage dismantling** (015): LKQ dominates, salvage costs are rising, zoning is hard, and EVs erode engine and
  transmission parts.
- **Mobile fueling** (032): capital, hazmat requirements and thin margins.
- **Commercial tires** (027): incumbents have scale.
- **Telematics installs** (026): self-install devices erode the work.
- **Consumer pre-purchase inspections** (020): low ticket.
- **Snow equipment** (033): seasonal and inventory-heavy.
- **Dealer porter driving** (035): thin margins and an insurance tail.

## EV/hybrid effects
Both LKQ and Rush flag EV drivetrains as a long-run threat to powertrain parts and service. GPC frames EV/hybrid as
an opportunity. Hybrid battery reconditioning (030; LKQ's Green Bean shows it is real) is a modest hedge. Records that
are mostly EV-neutral: 001, 006, 008, 009, 018, 023. ADAS work grows regardless of drivetrain.

## Biggest evidence gaps
- Local prices for everything: compliance subscriptions, washes, PM, OTS tests, DPF cleaning, ADAS.
- Technician wages in Chicago (BLS not retrievable).
- FDD Item 19 data, e.g. Fleet Clean USA (not retrieved).
- MWRD and municipal rules for mobile wash water.
- Fees and requirements for the IL Certified Safety Tester, remitter, auctioneer and recycler licenses.
- Counts of fleets under 10,001 lb, collision shops and forklifts in Chicago.
- Churn among small-carrier service clients.

## Cross-stream leads
- Trucking insurance agency for small carriers (WS02).
- Freight factoring brokerage for the 17.6k small carriers (WS01).
- CDL Entry-Level Driver Training and CDL staffing (WS09/WS12).
- Truck parking yards and equipment rental (WS10), recorded here as 029 but with real-estate/zoning economics.
- Forklift battery service (WS13).
- EV fleet charger install/O&M (WS11).
- Freight brokerage serving the dense Chicago carrier base (WS07).
