# SYN-001 — Insurance-led small-carrier compliance hub (Stage D deep dive, batch DC)

> **Verdict: FINALIST (conditional).** Evidence on the economics stays at **D**: the prices and the buyer census are
> well documented, but the attach rate and the market access are assumptions.
>
> **Base case (model):**
>
> | Metric | Value |
> |---|---|
> | Year-3 operating profit | **$20k** on $269k revenue |
> | Year-5 operating profit | **$172k** on $688k revenue, 140 accounts |
> | Peak funding | $92k with a $4k/month owner draw; $36k without |
>
> **The decisive fact:** compliance alone barely pays for itself. A $250/month done-for-you plan leaves about $109 a
> month after software and coordinator time. The profit sits in trucking commissions. Whether a start-up Illinois agency
> can actually quote 3–20-PU for-hire risks through an aggregator or MGA is documented only in marketing ("carriers from
> day one", "48-hour onboarding"). It has to be proven before money is spent on licensing staff.
>
> **Why it still leads the batch.** It is asset-light and the buyers are A-level identifiable. Licensing is cheap and
> quick: about $650 in state and exam fees and 6–10 weeks. The renewal book is sellable, and the work cannot be done
> without the founder's selling and tooling.

## 1. Specific initial niche
**What we sell:**
- done-for-you DOT compliance: DQ files, annual MVR and Clearinghouse queries, medical-card and expiry calendar,
  MCS-150/UCR reminders, new-hire packets;
- a drug & alcohol consortium;
- then commercial trucking insurance, quoted at the client's next renewal.

**Who we sell to:** established for-hire motor carriers, registered in 2020 or earlier, with 3–20 power units, in Cook,
DuPage and Will counties first and the rest of the 8-county Chicago area later.

**Size of the niche [A, DC-S001]:**
- 3,166 such carriers have an active MCS-150 updated in 2024 or later: Cook 1,564, DuPage 602, Will 414, Lake 206,
  Kane 166, McHenry 127.
- Fleet size: median 6 PU, mean 7.9 PU and 7.8 drivers. 95% run interstate.
- The wider band of 2–50 PU carriers totals 9,112.

**Why established carriers:**
- Survival flattens after about five years. 26–33% of the 2015–2019 cohorts are still active, versus 40% of 2023's.
- That implies an exit rate of about 6–7% a year among 5–10-year-old carriers [A data, E arithmetic, DC-S002].
- New ventures churn violently: the 2021 boom cohort is 29.2% alive.
- New ventures are also the segment every telemarketing agency chases.

## 2. Named operators (competitors and models)
| Operator | What is known | Level |
|---|---|---|
| OOIDA (association) | $45 dues. Consortium $145–170 per year plus $145 per extra driver. Compliance Connection DQ service. Bundle pricing tied to placing primary liability | B, C4-S003–S005 |
| Simplex Group | National back office: insurance, compliance, permits, IFTA, factoring. Claims 10,000+ trucking clients and has a Chicago page | D, C4-S013 |
| J.J. Keller | 600+ managed-services staff; DOT authority monitoring about $45/month | C/D, C4-S009–S010 |
| DOT Compliance Group (TX) | Compliance firm that partners with insurance brokers and does not sell insurance itself | D, C4-S014 |
| DOTConsortium.com | $149/yr per company (unlimited drivers); $60 per test | C, C4-S006 |
| Foley | Consortium $50–150 per driver per year, plus DQ/MVR services | D, C4-S007 |
| Done-for-you plans (unnamed provider; O Trucking) | $149/mo (1–2 drivers) to $249/mo (6–10), $99 setup; O Trucking $150–400/mo | D, C4-S011–S012 |
| HUB International, Downers Grove | National broker with a local transportation practice aimed at new carriers | D, DC-S041 |
| Fleet Response | Fleet management company selling DQ-file management, MVR monitoring and claims | D, DC-S016 |
| Agencies giving compliance away | e.g., free DOT monitoring for insureds | D, C4-S038 |

**What this means:**
- The bundle is the incumbent model, not an opening.
- The local gap is a hands-on, nearby, multilingual office for 3–20-PU firms. OOIDA serves owner-operators; Simplex and
  J.J. Keller sell remotely.
- That gap is a service wedge, and anyone can copy it.

## 3. Named suppliers / partners (see `09_databases/suppliers/SYN-001_suppliers.csv`)
| Partner | Role | What is published | Status |
|---|---|---|---|
| Illinois Dept. of Insurance | Licensing | 20 h per line; producer $215/2 yr; entity $250/2 yr (another table on the same page says $150); broker bond | **documented** [A, DC-S005–S006] |
| Pearson VUE | Exams | $92 per General+State pair ordered together (~$184 for P&C) | **documented** [A, DC-S007] |
| SIAA | Start-up aggregator | "Carriers from day one", start-up E&O; split and fees not published | assumed [B, DC-S008] |
| Smart Choice | No-fee network | Appointments within 24 h; split until a cap; cap not published | assumed [B, DC-S009] |
| Cover Whale | Trucking MGA | Online appointment, "48-Hour Onboarding"; commission not published | **documented** program; terms assumed [B, DC-S010] |
| Canal Insurance | Trucking carrier | Sells only through General Agents on a fixed-% commission | assumed: needs a GA [B, DC-S011] |
| XPT Specialty | Wholesaler, transportation practice | Appointment form | assumed [B, DC-S012] |
| Progressive Commercial | #1 truck insurer via independent agents | Appointment criteria not published | assumed [D, DC-S013] |
| DOTDriverFiles | DQ software | $5/driver/month; MVR $12.95 | **documented** [B, C4-S008] |
| AgencyZoom | Sales CRM | $99/month single location | **documented** [B, DC-S015] |

**Commission:** about 10% via MGAs and wholesalers. That figure comes from a 2010 forum post [D, DC-S014]. It sits
inside an Illinois commercial-auto selling-expense pool of 15.9% of premium [C, C4-S015]. The aggregator split (20%) is
**E**.

## 4. Named prospective customers
33 real carriers are recorded in `09_databases/prospects/SYN-001_prospects.csv`.
- **How they were chosen:** all are 3–20 PU, registered in 2020 or earlier, and have a live business website.
  Websites were found through the census business email *domain*; no emails were stored.
- **Examples:** K&L Logistics (St. Charles, 7 PU), Tempo Freight Systems (Lyons, 14), Schnidt Cartage (Hanover Park,
  15), Kirschhoffer Truck Service (Zion, 20), Chermak Cartage (Cary, 18), PDS Express (Batavia, 12), Load Monster
  (Rolling Meadows, 17), Iron Fleet Transport (Willowbrook, 16).
- **A first walking cluster near O'Hare:** Partner Carriers, Nationwide Logistics and Lion Logistics (Bensenville),
  plus OVN and Swift Global Intermodal (Elk Grove Village).
- **Status:** all are "prospect — not contacted".

## 5. Representative transactions
| # | Transaction | Revenue | Direct costs | Contribution | Payment timing |
|---|---|---|---|---|---|
| 1 | Monthly compliance plan, 6 PU / 8 drivers ($250 + $12.50 consortium) [D, C4-S011, C4-S006] | $262.50/mo | DQ software $40 [B]; MVRs $8.63 [B]; consortium cost $6 [E]; coordinator 3 h × $32.90 loaded [C, C4-S016] | **$109/mo** | ACH monthly in advance |
| 2 | Annual insurance placement, 6 PU × $12k premium × 10% [C/D, WS02-S017, DC-S014] | $7,200/yr | Aggregator split 20% $1,440 [E]; CSR 25 h $850; chargeback reserve $216; E&O share $150 | **$4,544/yr** | Commission monthly as premium is collected; clawed back on cancellation |
| 3 | Onboarding / DQ file rebuild | $150 | MVR pulls $104; coordinator 4 h $132 | **−$85** (loss leader) | At signing |
| 4 | Consortium membership | $150/yr [C, C4-S006] | Wholesale C/TPA cost $75 (MISSING, E) | $75/yr | Annual prepay |

**What the table shows:** one insured account is worth about 3.5 years of a compliance-only account. At a 25% attach
rate, insurance adds $120 a month to blended ARPC.

**Blended ARPC:** $405/month in the base case. The range is $275 (conservative) to $640 (optimistic).

## 6. Customer acquisition
**Customer #1.** Walk the O'Hare cluster. Offer a free 45-minute DQ-file and Clearinghouse audit. Write up the
findings in a one-page report (built with AI) and price the fix: $199–249/month, setup waived for the first five
clients.

**Customers #2–10:**
- direct letters to the 1,564 Cook and 602 DuPage carriers in the niche;
- follow-up calls to *business* landlines only: TCPA bars autodialed calls and texts to cell phones;
- yard visits;
- a "pre-renewal review" offer timed to policy dates. The FMCSA L&I insurance history is public; its usability is to
  be verified.

**Customers #11–100:**
- referral arrangements with factoring companies, dispatch services and truck dealers;
- one language-community channel (Polish/Ukrainian or Spanish media, community associations);
- a licensed producer (sales rep) from month 24;
- referrals, modelled at 1.0 new customer per 100 accounts a month [E].

**Funnel at full pace (all E):** 20 qualified conversations → 8 proposals (40%) → 2 wins (25%) a month, plus referrals.

**Effort:** about 20–25 founder hours a week of selling, made up of roughly 5 yard visits, 30 calls, 2 audits and 2
proposals.

**Unit economics (base):**

| Measure | Value |
|---|---|
| CAC | ~$430 per account ($150 variable + $700/month fixed, at ~2.5 new/month) |
| Contribution per account | ~$250/month after GM, variable cost and a coordinator share |
| CAC payback | ~2 months |
| 5-year LTV at 1.5%/month churn | ~$9.9k |

The constraint is founder conversation capacity, not CAC. Founder leads and win rate are among the top tornado drivers:
year-3 operating profit runs from $2k to $61k across a ±25% swing.

## 7. Pricing strategy
- **Market evidence:** done-for-you plans sell for $149–249/month plus a $99 setup [D, C4-S011] and up to $400/month
  [D, C4-S012]. OOIDA prices its bundle by whether it places the liability [B, C4-S005]. Software is $5/driver
  [B, C4-S008]. Consortium membership is $149/company [C, C4-S006].
- **Tiers:**

  | Drivers | Price |
  |---|---|
  | 3–5 | $199/month |
  | 6–10 | $249–299/month |
  | 11–20 | $349–449/month |

  Consortium is included. Setup is $99–150.
- **Insured-client discount:** 20% off compliance when we place auto liability. This mirrors OOIDA's tie and makes the
  compliance fee the retention tool.
- **Insurance commission:** never discounted. Fees on top of commission only where lawful and disclosed.
- **Do not compete** on $5/driver software. Sell the done-for-you guarantee: an audit-ready file every quarter.

## 8. Working capital and cash conversion
Compliance is prepaid by ACH. Commission arrives monthly, after premium collection by the insurer (direct bill).

| Customers | Revenue/mo | AR (DSO 15) | AP (DPO 15 on ~16% COGS) | Net WC | Comment |
|---|---|---|---|---|---|
| 10 | $4,050 | $2.0k | $0.3k | ~$1.7k | Founder only |
| 50 | $20,250 | $10.1k | $1.6k | ~$8.5k | One coordinator |
| 200 | $81,000 | $40.5k | $6.5k | ~$34k | Plus a chargeback reserve of ~3% of annual commission (~$4–6k) |

The cash conversion cycle is roughly +10 to +15 days. Avoid agency-bill premium handling in years 1–3: it creates
trust-account obligations and credit exposure.

## 9. Regulatory path (exact steps)
1. **Entity.** Illinois LLC and EIN. The SOS filing fee was not verified: ilsos.gov was not accessed, so it is MISSING.
2. **Pre-licensing.** 20 h Property + 20 h Casualty (7.5 h classroom each) with an IDOI-certified provider
   [A, DC-S005]. Course price is MISSING (E $200–500).
3. **Exams.** Pearson VUE GEN/STATE-Prop03 and GEN/STATE-Cas04 at $92 per pair, ~$184; both exams of a line must be
   passed within 90 days [A, DC-S007].
4. **Producer licence.** Wait 5 days after passing, then apply via NIPR: $215 per 2 years plus the NIPR fee (MISSING)
   [A, DC-S006]. Age 18+.
5. **Business-entity licence.** $250 per 2 years (the statute table says $150; both are recorded), with a designated
   responsible licensed producer [A, DC-S006].
6. **Broker bond.** Required when placing with insurers where we hold no agent contract: $2,500 or 5% of the prior
   year's brokered premium, maximum $50,000 [A, DC-S005]. The premium cost is MISSING (E $100–250/yr). Whether
   aggregator sub-codes avoid the bond needs confirmation.
7. **E&O.** Not statutory, but required by networks and MGAs. Budget $3–6k/yr (E). Get a policy that also covers the
   compliance services, not only the insurance.
8. **Market access.** An SIAA or Smart Choice contract, plus Cover Whale online appointment and a wholesaler/GA
   (XPT; a Canal GA).
9. **C/TPA duties.** Register in the FMCSA Clearinghouse as the service agent [A, C4-S037]. Follow Part 40: no routing
   of lab results to the MRO, no waivers [A, C4-S036].
10. **Compliance services.** No licence was identified (absence not verified). Avoid legal advice. File IFTA/IRP under
    a carrier power of attorney. Defer IRP plate and title processing until the Illinois SOS remitter question is
    answered (MISSING).
11. **Surplus lines.** Place E&S only through licensed wholesalers. A direct surplus-lines licence is not needed
    [A/C, WS02-S004].
12. **Other cover:** GL, cyber (driver PII), and workers' comp from the first hire.

**Timeline:** 6–10 weeks to a licensed agency. State and exam fees come to about $650. Compliance can be sold from
week 1.

## 10. Operations workflow (lead → cash)
1. **Census list → CRM.** Automated.
2. **Letter or visit → audit.** Human visit. AI drafts the audit report from uploaded documents.
3. **Proposal → e-sign + ACH mandate.** Automated.
4. **Onboarding.** The client uploads licences, medical cards and MVR consent. AI does OCR and checks expiry dates;
   the coordinator verifies.
5. **Monthly cycle.** Software sends expiry alerts. The coordinator chases documents and runs Clearinghouse queries,
   and logs random selections in the consortium portal.
6. **Quarterly file attestation** to the client. Automated report, human sign-off.
7. **Renewal at T−90 days.** Loss runs are requested. AI pre-fills applications from census and telematics data.
   Submissions go to 2–4 markets through aggregator and MGA portals. Binding, COIs and the insurer's MCS-90/BMC-91X
   filings follow, with a human producer.
8. **Claims advocacy and mid-term changes.** Done by a human CSR.

**Software stack and cost:**

| Tool | Cost |
|---|---|
| DOTDriverFiles | $5/driver |
| AgencyZoom | $99/mo |
| AMS + comparative rater | MISSING (budgeted $300–500/mo) |
| E-sign, QuickBooks, phone | ~$150/mo |
| LLM API for document intake | ~$150/mo |

All are ordinary-priced after December 2026.

## 11. Competitive position and defensibility
**What builds up over time:**
1. **The renewal book.** Commission recurs annually and the book is a sellable asset.
2. **Held DQ and Clearinghouse records.** Moving them is a chore, so switching costs are moderate.
3. **Referral relationships** with factoring companies and dealers.
4. **Density** inside one or two language communities.

**What does not build up:**
- Price. The $5 software and $149 consortium set a ceiling on compliance fees.
- Any exclusive market access.

Incumbents (OOIDA, Simplex, HUB) can match the offer. The defensibility therefore comes from service levels and from
the cost of moving a held book.

## 12. Key risks and pre-mortem
| Loss level | How it fails | Early warning |
|---|---|---|
| **$5k** | Licensed, but the aggregator or MGA declines most 3–20-PU for-hire risks, or quotes are uncompetitive | <50% of the first 10 submissions get a quote; no Cover Whale/Progressive access through a sub-code |
| **$25k** | Compliance clients sign, but insurance attach stays below 10% because they keep their incumbent agent | <3 broker-of-record letters from the first 15 clients within their renewal windows |
| **$50k** | A coordinator is hired, churn runs above 2.5%/month (freight recession), plus an E&O claim from a missed expiry | Churn >2%/month for 3 months; any client fine traced to our miss; chargebacks >5% of commission |

**Model stress results (base year-3 operating profit $20k):**

| Stress | Year-3 operating profit |
|---|---|
| Win rate −40% | −$17k |
| Recession | −$11k |
| Founder capacity −40% | −$14k |
| Growth takes twice as long | −$25k, with peak funding $235k |

**The conservative case** (12 leads, 15% win, $275 ARPC, 2.2% churn) never breaks even. It is a stop case, not a plan.
Kill criteria are in §13.

## 13. Validation plan (cheapest real evidence first)
| # | Experiment | Cost | Success | Kill |
|---|---|---|---|---|
| 1 | **Market-access test.** Once licensed (or through a licensed partner), submit 10 real 3–20-PU risks through one aggregator plus Cover Whale | ~$650 fees + E&O binder (~$500) | ≥6 bindable quotes; ≥2 within 10% of incumbent premium | <4 quotes |
| 2 | **Paid compliance pilot** before licensing finishes: sell the $199–249 plan to the O'Hare cluster and the first mail wave | ~$300 (mail, MVRs) | ≥5 paying clients from ≤60 conversations in 60 days | <3 paid |
| 3 | **Attach test.** Of the paying clients, how many sign a broker-of-record letter or allow a renewal quote | $0 | ≥30% within their renewal window | <10% after 6 renewals |
| 4 | **Price test.** $199 vs $279 for 6–10 drivers, alternated across mail waves | $0 | Conversion drops by <30% at the higher price | — |
| 5 | **Renewal-date data test.** Check that public FMCSA L&I insurance history yields policy dates for ≥70% of the 3,166 | $0 | Usable for timing outreach | Unusable: rely on asking |

**Budget:** total validation under $2k before any hire. The founder must run these experiments. This analysis contacted
no one.

## 14. Revised scores and verdict
| Key | Stage C | Stage D | Reason |
|---|---|---|---|
| fcf | 5 | **4** | Base year-3 $20k, year-5 $172k; the $260k Stage C high case needs ~190 accounts |
| roic | 7 | **6** | ~$36k at risk without owner draw; $92k with it |
| access | 6 | 5 | A-level list, but saturated outreach and low trust |
| scale | 6 | 6 | Remote compliance plus multi-state non-resident licences |
| resilience | 6 | 6 | Mandated, but freight-cycle mortality |
| entry | 4 | 4 | The bundle is the incumbent model |
| delegation | 6 | 6 | Coordinators and CSRs are standard roles |
| cash | 7 | 7 | Prepaid plus monthly commission |
| feasibility | 7 | 7 | ~$650 and 6–10 weeks to licence; market access unproven |
| ai | 6 | 6 | Document intake, applications, renewal prep |

Raw ≈ 5.4; evidence-adjusted (D) ≈ **5.3**.

**Model base case:** year-3 operating profit **$20,149**, year-5 $172k, breakeven month 13, payback month 53. Ten-year
cumulative deployable cash is $0.44M.

**Verdict:** FINALIST (conditional). It is the lowest-capital, most delegable and most founder-compatible concept in
batch DC. It is promoted only if validations 1–3 pass within about 90 days. Otherwise demote it to reserve.

*Limitations:*
- ilsos.gov and ilga.gov were not used (LLC fee and remitter rules are MISSING);
- aggregator, MGA and E&O terms are unpublished;
- the commission figure rests on a dated forum post plus the NAIC selling-expense pool;
- the attach rate and conversion rates are E.
