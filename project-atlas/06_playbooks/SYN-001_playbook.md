# SYN-001 Playbook: Insurance-led compliance hub for small Chicago trucking companies

*Stage E finalist playbook, written 2026-11-28. Evidence tags: [level, source_id]. Sources are in
`09_databases/sources.jsonl` (earlier stages) and `06_playbooks/sources_E_SYN-001.jsonl` (IDs E-SYN001-S###). Model:
`08_financial_models/SYN-001_assumptions.json`, rebuilt into `SYN-001_results.json` and `SYN-001_model.xlsx`.
This research contacted no one, opened no accounts and requested no quotes. Everything in the materials file is a
DRAFT.*

> **Verdict: FINALIST (conditional). Validate it; do not invest in it yet.** Evidence on the economics is still
> **D**. The market structure is now **A**, because we re-analysed FMCSA's public insurance filings.
>
> **What this business is.** A local, done-for-you DOT-compliance office for established Chicago trucking companies
> with 3–20 trucks. It earns trucking-insurance commission when those clients renew their insurance. Compliance gets
> the business in the door. The insurance commission is where the profit comes from.
>
> **The make-or-break finding.** The question was whether a start-up can get access to the insurers that write
> these trucking risks. We checked the public liability filings of the 2,750 target carriers that have one
> [A, E-SYN001-S002]:
> - **About 63%** are insured by standard carriers that sell only through appointed agencies: Progressive, Great
>   West, Northland/Travelers, Sentry, Acuity and Berkley.
> - **About 10%** are with direct writers (mainly GEICO).
> - **About 27%** are on specialty, fronting, surplus-lines or risk-retention-group "paper" (the insurer actually
>   carrying the risk), which agents normally reach through wholesalers and MGAs.
>
> A newly licensed Illinois agency working through wholesalers alone could compete for only about 39% of the
> business that changes hands each year [A, E-SYN001-S003]. Even through an association, Progressive demands 2–3
> years of agency experience (a Texas association's published terms) [B, E-SYN001-S005]. The workable route is for the founder to be licensed as a
> **sub-producer** inside an established trucking agency that already holds those appointments. The founder gives
> up about half the commission. Whether such an agency exists and will sign written terms is the single cheapest
> decisive test (§4).
>
> **Base-case model:**
>
> | Metric | Value |
> |---|---|
> | Year-3 operating profit | **$48,348** (55 clients) |
> | Year-5 operating profit | **$177,513** (119 clients) |
> | Peak funding with the standard $4k/month owner draw | **$69,328** |
> | Peak funding without the draw | $36,634 |
> | Breakeven | month 14 |
> | Payback | month 54 |
>
> The **conservative case never breaks even**: year-5 operating profit is −$13,064 and peak funding is $357,303. It
> describes what happens if the validation gates are ignored.
>
> **Two answers to the brief's questions:**
> - **Carrier mortality is not what limits the business.** Established carriers exit at only 2.4–5.8% a year
>   [A, E-SYN001-S004]. The 41.9% survival figure applies to new ventures [A, C4-S001], which this plan excludes.
>   What does limit it is **insurer switching**: 30–37% of established carriers change insurer every year
>   [A, E-SYN001-S003].
> - **Realistic insurance attach is 10–25% of compliance clients after three years** (E, built on the A-level base
>   rates). Stage D assumed 25% from day one.

---

## 1. Business explanation

**What it does.** Every interstate trucking company must do two things:
- keep a long list of federal safety records current:
  - a driver-qualification (DQ) file for every driver (49 CFR 391.51) [A, WS17-S004];
  - an annual Drug & Alcohol Clearinghouse query per driver (382.701) [A, WS17-S005];
  - membership in a random drug and alcohol testing pool at 50% drugs and 10% alcohol [A, WS17-S006];
  - vehicle inspection files and the MCS-150 update cycle;
- file proof of liability insurance with FMCSA through its insurer.

Owners of 3–20-truck firms usually do the paperwork themselves, at night, badly. We take it over for a fixed monthly
fee. We keep the files audit-ready, chase expiring medical cards and licences, run the queries, and administer the
testing pool through a consortium. Then, at each client's insurance renewal, we offer to shop their trucking
insurance.

**What it sells.**
1. A done-for-you compliance subscription: **$199–$449 a month by driver count**, with the consortium included.
2. A one-time file rebuild.
3. Insurance placement, paid by insurers as commission (a percentage of premium) every year the policy renews.

**Who buys.** Owner-operators of established for-hire carriers. The defined niche is the 3,166 Chicago-area for-hire
carriers with 3–20 power units (PU) that registered before 2021 and filed an MCS-150 in 2024 or later. By county:
Cook 1,564, DuPage 602, Will 414, Lake 206, Kane 166, McHenry 127, Kendall 53, Grundy 34 [A, E-SYN001-S001]. The
median carrier runs 6 trucks; the mean is 7.9 trucks and 7.8 drivers [A, DC-S001].

**Why they pay.** Each kind of spending has a different reason behind it:
- **Compliance is a legal mandate.** Failing a safety audit or compliance review brings fines, out-of-service orders
  and higher premiums.
- **Insurance is mandatory and expensive.** ATRI puts average truck premiums at 10.6¢ per mile in 2025, and small
  fleets pay nearly double the per-mile rate of large fleets [C, WS02-S017]. For a 6-truck firm that is roughly
  $70k a year (E).
- **They shop insurance constantly.** 37.0% of the niche changed insurer in 2025 [A, E-SYN001-S003].

**How it earns.**
- **Compliance alone barely pays.** A $250 plan leaves about $119 a month after software, MVRs and coordinator time
  (transaction T1, §3).
- **Insurance is the profit pool.** One 6-truck insured account is worth about $3,800–$5,900 a year in
  contribution (T2/T3). Illinois commercial-auto "selling expense" (commissions and acquisition costs) is 15.9% of
  premium [C, C4-S015]. A 6-truck client's ~$72k premium therefore carries roughly $11k of distribution money each
  year, shared between insurer, wholesaler and retail agent.

**Why it is attractive.**
- It is asset-light: the setup capital is about $4,500 [model].
- Licensing is cheap and quick: about $650 in state and exam fees and 6–10 weeks [A, DC-S005–S007].
- Demand is mandated and recurring.
- The buyers are fully identifiable from public data, including their current insurer and approximate renewal month
  [A, E-SYN001-S002].
- An insurance renewal book is a sellable asset.

**Why it is not easy.**
- The bundle is the incumbent model, not an opening. OOIDA and Simplex already sell compliance plus insurance
  [B, C4-S004–S005; D, C4-S013].
- Compliance prices are anchored by $5-per-driver software and a $149 consortium [B, C4-S008; C, C4-S006].
- Insurance profit depends on access to markets that a start-up does not have.

---

## 2. Commercial entry

### 2.1 Niche, customer, geography
**Who we target:** established (registered 2020 or earlier) for-hire carriers with 3–20 PU in Cook, DuPage and Will
counties first; 2,580 of the 3,166 are there [A, E-SYN001-S001].

**Where we start:** the O'Hare freight cluster of Bensenville, Elk Grove Village, Itasca, Addison and Northlake. The
top-15 list includes four carriers there: Partner Carriers, OVN, Lion Logistics and Champion/ICAT. The full list adds
Area Wide, Nationwide Logistics, M&M Direct Express and Swift Global Intermodal. A founder can walk between these yards
in a day.

**Why established carriers:**
- **They survive.** Among carriers registered before 2021 that are now inactive, authority revocations ran
  2.4–5.8% a year in 2019–2025 [A, E-SYN001-S004]. That is a lower bound, since some exits leave no revocation
  record. For comparison, only 41.9% of the 2023 for-hire cohort and 29.5% of the 2021 cohort are still active
  [A, C4-S001].
- **They can be insured** by programs that require two years under the current DOT number [B, E-SYN001-S006].
- **Telemarketing agencies largely ignore them**; those agencies chase new authorities.

### 2.2 Market access: every documented path and its terms (the make-or-break)
Which insurers win the business that moves matters as much as which insurers hold it today. Of 2,366 insurer
switches in the niche in 2024–25 [A, E-SYN001-S003]:
- about 50% went to standard appointment carriers (Progressive alone 21.4%, Great West 8.5%, Northland 8.4%,
  Berkley 4.1%, Sentry 3.6%);
- about 39% went to specialty or fronting paper (IAT/Occidental/TransGuard, Crum & Forster, Trisura, Canal,
  SiriusPoint, Everspan, RRGs, Accredited, MS Transverse, AIG and others);
- about 11% went to direct writers, mainly GEICO at 10.8%.

The channel classification is our judgement (E, ±3 pts).

| Path | Documented terms | Evidence | What a start-up can quote |
|---|---|---|---|
| **A. Direct carrier appointment** (Progressive, Great West, Northland, Sentry, Acuity, Berkley) | Progressive access through a (Texas) association aggregator still needs a Progressive-approved subcode, 2–3 years of agency ownership and P&C experience, $1M E&O, a storefront and monthly minimum production. Commission schedules are unpublished. Other carriers' criteria are MISSING | B, E-SYN001-S005; D, E-SYN001-S016 | ~0% in year 1 |
| **B. Aggregator / network** (SIAA, Smart Choice) | SIAA promises "carriers from day one" and start-up E&O, but fees and splits are unpublished [B, DC-S008]. Smart Choice claims no fees and 24-hour Express appointments [B, DC-S009]. Its example shows it taking 4% on Level I carriers against 20% for a generic network [D, E-SYN001-S008]. Which trucking carriers are open to an Illinois start-up is MISSING. Anecdotes mention joining, monthly and departure fees (one 25%) [D, WS02-S015] | B/D | Unknown: the decisive question |
| **C. Wholesaler / general agent (GA)** (Amwins, XPT, Canal GAs, Union General-type) | A trucking GA's agreement requires $1M E&O and a trucking questionnaire (years in business, trucking premium volume, existing GAs). Commission is "as approved" by the GA. The producer must pay premiums within 30 days of billing **whether or not collected**, and premiums are held in trust; the producer owns its expirations [B, E-SYN001-S007]. Amwins' 1–25-unit ANTU program is sold "through a select group of retail brokers" and needs 2 years on the current DOT [B, E-SYN001-S006]. Canal sells only through GAs [B, DC-S011]. XPT has an appointment form [B, DC-S012] | B | Specialty paper, ≈39% of switch flow |
| **D. MGA online appointment** (Cover Whale) | Appointment in about 2 days. Auto liability for 1–25 PU in 41 states, with dashcam or ELD required. Commission is called "competitive" but not published. Illinois is not confirmed [B, E-SYN001-S009, DC-S010] | B | Part of the specialty share, if Illinois is open |
| **E. Sub-producer inside an established trucking agency** | 1099, commission-only trucking producer roles are advertised in Illinois [D, E-SYN001-S014]. Producer splits run 30–90%, typically 50/50 or 50% new / 40% renewal; renewal ownership is often unclear [D, E-SYN001-S010]. Non-specialist agencies refer trucking to specialists with direct contracts [D, E-SYN001-S017]. The UIIA directory lists 9 Illinois agencies familiar with motor-carrier requirements [B, E-SYN001-S018] | D/B | Up to ≈89% of switch flow, if the host holds the standard appointments |
| **F. Branch / agency-in-a-box** (TWFG) | Passes ~60% of commission to branches. Branches pay their own E&O and are exclusive for certain business. The book is ~80% personal lines; Illinois presence is unconfirmed [A, WS02-S012] | A | Unknown for trucking |
| **G. Buy a book** | Excluded as an initial entry by the mandate (G6) | – | – |

**Conclusion.**
- **Base plan:** path E, with B and C added later. The founder gets licensed and signs a written sub-producer
  agreement with a Chicago trucking agency that holds at least three of the seven dominant carriers. The founder
  also runs his own LLC for compliance, which needs no insurance licence.
- **Later:** move to the founder's own appointments once the book and tenure qualify, around year 3 (E).
- **Why the routes cost about the same:** keeping 50% of 12% (path E) or 85–100% of 10% (paths B/C) produces
  similar revenue per client. Path B/C reaches roughly half as many risks. Path E carries fewer fixed costs and no
  premium-trust liability, but the host may own the expirations.
- **Correction (Stage D §9 step 8):** an SIAA or Smart Choice contract plus Cover Whale and a wholesaler is not
  proven sufficient. Most of the niche's in-force business sits with carriers those routes may not open to a new
  agency.

### 2.3 Named suppliers and partners
- **Compliance stack:**
  - DOTDriverFiles: $5 per driver per month; MVR $12.95; PSP $19.99 [B, C4-S008];
  - DOTConsortium.com: $149 a year per company, $60 per test [C, C4-S006]. It is a consortium partner or competitor
    (wholesale terms MISSING);
  - FMCSA Clearinghouse: register as a service agent [A, C4-S037];
  - AgencyZoom CRM: $99 a month [B, DC-S015].
- **Licensing:**
  - Illinois Department of Insurance (IDOI): producer licence $215 per 2 years; entity licence $150 or $250 (two
    tables disagree); broker bond $2,500+ when placing without an agent contract [A, DC-S005, DC-S006];
  - Pearson VUE: about $184 for both P&C exam pairs [A, DC-S007].
- **Insurance markets:** host-agency candidates are listed in §10 [B, E-SYN001-S018]. Others are SIAA, Smart Choice,
  Amwins ANTU, XPT Specialty, Canal (through a GA), Cover Whale and Union General-type trucking GAs.

### 2.4 Named prospects (top 15; all 33 in `09_databases/prospects/SYN-001_prospects.csv`, all "not contacted")
How to read the table:
- Fleet size and registration year come from the census [A, DC-S001].
- The current liability insurer, the month of its filing and the number of insurer changes since 2021 come from
  FMCSA filings [A, E-SYN001-S002/S003].
- The filing month approximates the policy anniversary (E).

| # | Carrier (city) | PU / drivers, registered | Current insurer (filing) | Switches since 2021 | Why now |
|---|---|---|---|---|---|
| 1 | LogTrans Corp (Frankfort) | 5/5, 2015 | Great West (04/2024) | 3 | Habitual shopper; April renewal is inside the T−120 window |
| 2 | GTG Logistics (Inverness) | 4/4, 2014 | Northland (04/2024) | 3 | April renewal; shops often |
| 3 | Bella Intermodal (Oak Lawn) | 6/7, 2020 | Acuity (03/2025) | 3 | March renewal; young but established |
| 4 | Champion Transportation / ICAT (Northlake) | 5/5, 1991 | CNA Continental (03/2025) | 1 | March renewal; intrastate; O'Hare area |
| 5 | Tempo Freight Systems (Lyons) | 14/14, 2017 | Hoxbridge (05/2026) | 3 | On specialty paper, quotable through wholesale; 14 drivers to manage |
| 6 | Shiplex Logistics (Chicago) | 16/16, 2020 | Trisura (10/2025) | 6 | Heaviest shopper; specialty paper; compliance first |
| 7 | W A Braxton & Sons (Chicago) | 10/10, 2020, hazmat | Trisura (10/2025) | 4 | Specialty paper; hazmat makes compliance pain high |
| 8 | Iron Fleet Transport (Willowbrook) | 16/7, 2018 | AIG National Union (06/2025) | 5 | Frequent switcher; June renewal |
| 9 | First Way Inc (Algonquin) | 20/20, 2014 | AIG National Union (06/2025) | 4 | Top of the size band; 20 DQ files |
| 10 | BTR Freight (Skokie) | 7/8, 2020 | Sentry (09/2025) | 6 | Frequent switcher |
| 11 | Partner Carriers (Bensenville) | 8/8, 2020 | Sentry (12/2025) | 4 | O'Hare walking cluster |
| 12 | OVN LLC (Elk Grove Village) | 10/10, 2016 | Progressive (10/2025) | 2 | O'Hare cluster |
| 13 | Lion Logistics (Bensenville) | 12/24, 2003 | Northland (10/2024) | 1 | 24 drivers, so compliance-heavy; O'Hare cluster |
| 14 | Coach Xpress (Lemont) | 15/15, 2012 | Berkley (10/2025) | 2 | 15 drivers |
| 15 | Gordon Driveaway (Lynwood) | 16/16, 1985, hazmat | Canal (11/2025) | 2 | Canal is reached through GAs; long-tenured |

**What the 33 named prospects show.** Of the 32 with a filing, 7 are on specialty paper, 24 are with standard
appointment carriers and 1 is with a captive writer (Country). That confirms §2.2 at the prospect level.

### 2.5 Named competitors
| Competitor | Profile | Evidence |
|---|---|---|
| OOIDA | DQ-file "Compliance Connection", consortium at $145–170, permits, and bundle pricing tied to placing primary liability | B, C4-S003–S005 |
| Simplex Group | National back office plus insurance; claims 10,000+ trucking clients | D, C4-S013 |
| J.J. Keller | 600+ managed-services staff | C, C4-S010 |
| Foley | Consortium $50–150 per driver | D, C4-S007 |
| DOT Compliance Group | Partners with insurance brokers | D, C4-S014 |
| O Trucking | $150–400 a month | D, C4-S012 |
| HUB International, Downers Grove | Transportation practice | D, DC-S041 |
| Fleet Response | Fleet management and DQ files | D, DC-S016 |
| Agencies giving monitoring away free | e.g., free DOT monitoring for insureds | D, C4-S038 |
| GEICO | Direct writer: 8.4% of in-force and 10.8% of switches | A, E-SYN001-S002/S003 |
| The nine UIIA-listed Illinois agencies | Both potential hosts and competitors | B, E-SYN001-S018 |

### 2.6 Positioning, pricing, sales and acquisition
**Positioning.** "Your safety department, down the street." We offer an audit-ready file guarantee, multilingual
service where the founder can hire for it, and a free pre-renewal insurance review using the carrier's own public
filing history. We never mimic FMCSA mailers.

**Pricing** (market range $149–$400 [D, C4-S011, C4-S012]):

| Drivers | Monthly price |
|---|---|
| 3–5 | $199 |
| 6–10 | $249–$299 |
| 11–20 | $349–$449 |

- Consortium is included.
- Setup is $99–$150.
- Clients who place their auto liability through us get 20% off, mirroring OOIDA's tie [B, C4-S005].
- Commission is never discounted.
- Broker fees only where Illinois law allows and the fee is disclosed (rule MISSING, §12).

**Sales:**
1. Lead with a free 45-minute DQ and Clearinghouse audit.
2. Convert the gaps it finds into a monthly plan.
3. Ask for written permission to quote at T−90 days before renewal.

**Acquisition:**
- renewal-timed letters to the 3,166 carriers;
- yard visits;
- calls to business landlines only (TCPA restricts autodialed calls and texts to mobiles);
- referral partners: factoring firms, dispatch services, truck dealers and CPAs;
- a licensed producer hire once 60 clients are active [model].

---

## 3. Transaction economics
| # | Transaction | Revenue | Direct costs | Contribution | Cash timing |
|---|---|---|---|---|---|
| T1 | Compliance plan, 6 PU / 8 drivers [D, C4-S011] | $262.50/mo ($250 + $12.50 consortium share) | DQ software $40.00 [B]; MVRs $8.63 [B]; consortium cost $6.00 [E]; coordinator 2.7 h × $32.90 = $88.83 [C/E, C4-S016] | **$119.04/mo (45%)** | ACH in advance on the 1st; MVR fees paid when pulled |
| T2 | Insurance renewal as **sub-producer**: 6 PU × $12k = $72,000 premium [C/E, WS02-S017] | Host commission 12% = $8,640 [E, within the 15.9% pool, C4-S015]; our 50% = **$4,320/yr** [D, E-SYN001-S010] | Founder renewal prep 10 h × $32.90 = $329; chargeback reserve 3% = $130; E&O share $100 | **$3,761/yr** | Host pays monthly in arrears after the carrier pays the host; unearned commission is refunded on cancellation [B, E-SYN001-S007] |
| T3 | Insurance through **own agency + wholesaler**: same risk | 10% retail commission = **$7,200/yr** [D, DC-S014] | CSR 25 h × $34 = $850; reserve 4% = $288; E&O $150 | **$5,912/yr** | Agency-bill: we owe the GA within 30 days whether or not the client paid [B, E-SYN001-S007] |
| T4 | Onboarding / DQ file rebuild | $150 | MVRs 8 × $12.95 = $103.60; coordinator 4 h = $131.60 | **−$85.20** (loss leader) | At signing |
| T5 | Consortium membership | $150/yr [C, C4-S006] | Wholesale C/TPA cost $75 (MISSING, E) | $75/yr | Annual prepay |

**Contribution per client.**
- One insured client is worth about 2.6–4.1 years of compliance contribution in one year.
- At the base case's year-3 attach of about 21%, insurance adds roughly $76 a month to an average client
  (0.21 × $360).
- Blended year-3 revenue per client (ARPC) is ~$362 in the model ($305 × 1.09²).

**Cash timing.**
- Compliance is prepaid.
- Sub-producer commission arrives 30–45 days after the insurer is paid.
- The own-agency route can make us the debtor for premium. That is a working-capital and credit risk Stage D
  understated.
- **Correction (Stage D §8):** "avoid agency-bill" is not a free choice on the wholesale route. Trucking GAs' standard
  agreements put the premium obligation on the producer [B, E-SYN001-S007].

**Failure risks per transaction.**
- **T1:** the client stops uploading documents; a missed expiry leads to a fine (E&O); the client cancels on 30 days'
  notice.
- **T2:** the host's carriers decline or overprice the risk; the host keeps the expirations; the host's CSR gives
  poor service and loses the account.
- **T3:** a mid-term cancellation for non-payment leaves an unearned-commission refund and possibly unpaid premium.

**Repeat potential.**
- Compliance is monthly. Base churn is 1.5% a month, or 16.6% a year, consistent with average agency retention of 84%
  [C, E-SYN001-S012].
- Insurance renews annually. However, a third of the niche changes insurer each year [A, E-SYN001-S003], so the
  insured book must be re-won constantly.

---

## 4. Validation

**Minimum viable offering:**
- a one-page audit report;
- a $199–$299 monthly plan run on DOTDriverFiles plus a shared drive;
- a consortium enrolment;
- once licensed under a host, a renewal review.

**Experiments, ordered by information per dollar:**

| # | Test | Cost | Success | Kill / pivot |
|---|---|---|---|---|
| V1 | **Market-access term-sheet test** (cheapest decisive). The founder talks to ≥12 parties:<br>• the 9 UIIA-listed Illinois agencies [B, E-SYN001-S018];<br>• 2–3 other Chicago trucking agencies;<br>• SIAA's Illinois master agency and Smart Choice's Illinois state director;<br>• Amwins ANTU, XPT and Cover Whale.<br>Ask the questions in the materials file | $0–$100 (time, mileage) | ≥1 **written** offer that gives quotes from ≥3 of the 7 dominant carriers plus ≥2 trucking wholesalers, at ≥40% of commission on new and renewal business, with vested or founder-owned expirations | Only specialty access, or agency-bill-only terms, after 12 conversations. Then drop insurance: compliance-only economics are weak (§7) |
| V2 | Paid compliance pilot (O'Hare cluster plus first letter wave) | ~$300 (letters, sample MVRs) | ≥5 paying clients from ≤60 conversations in 60 days | <3 paid |
| V3 | Licensing (only if V1 has ≥2 positive conversations) | ~$700–$950 (course E $200–500, exams $184, licence $215) | Licensed in 6–10 weeks | – |
| V4 | Attach test: clients with renewals in the window | $0 | ≥30% sign authority to quote; ≥1 bind in the first 5 | <10% after 6 renewals |
| V5 | Competitiveness: submit 5–10 real renewals through the host | $0 | ≥50% of quotes within 10% of the incumbent premium | <25% |
| V6 | Price test: $199 vs $279 for 6–10 drivers, alternated across letter waves | $0 | Conversion falls <30% at $279 | – |
| V7 | Renewal-date data. **Already done:** 2,750 of 3,166 (87%) have a current liability filing month, and 1,889 of those filings are dated 2024–26 | $0 | Pass (60–87% usable) [A, E-SYN001-S003] | – |

**Budget:** about $1,500 in total before any hire or office.

**Testable assumptions:**
- win rate 25%;
- 20 qualified conversations a month;
- $250 average plan;
- a 50% split;
- attach ~21% by year 3;
- coordinator capacity of 60 clients;
- churn ≤1.5% a month.

**Conditions to invest beyond $2k:**
- V1 passes;
- V2 passes;
- at least one bound policy.

**Conditions to abandon or pivot:**
- **V1 fails.** Without insurance the model makes year-5 operating profit of $59,362 and needs $139,292 of peak
  funding (engine run with insurance removed, §7). That is not worth the founder's time. Pivot to compliance as a
  referral feeder for an established agency, or drop the concept.
- **V2 fails.** The local wedge does not exist. Stop.

---

## 5. Operations

### 5.1 Lead-to-cash workflow and how each step is done
| Step | Function | Classification |
|---|---|---|
| 1 | Pull the census and L&I filings, then rank prospects by renewal month and switch history | Automatable (public API, a scheduled script) |
| 2 | Write a letter or web message tailored to the carrier's filing facts | AI-assisted (founder approves) |
| 3 | Yard visit, phone call, the 45-minute audit | Human (founder) |
| 4 | Audit report from uploaded documents | AI-assisted, human-checked |
| 5 | Proposal, e-signature, ACH mandate, power of attorney (POA) for filings | Automatable |
| 6 | Onboarding: OCR of medical cards, CDLs, MVR consents; expiry calendar | AI-assisted, coordinator-verified |
| 7 | Monthly cycle: alerts, document chasing, Clearinghouse queries, random selections logged in the consortium | Automatable alerts; human chasing |
| 8 | Quarterly file attestation | Automatable report; human sign-off |
| 9 | Renewal at T−120/−90: loss runs, IFTA mileage, driver list, application pre-fill | AI-assisted |
| 10 | Marketing the risk to underwriters, negotiating, binding | **Professional-dependent (licensed producer)**; human |
| 11 | Certificates (COIs), filings (BMC-91X, MCS-90 by the insurer), endorsements | Host CSR (base); later our own licensed CSR |
| 12 | Claims advocacy, audits, disputes | Human; not automatable |
| 13 | Invoicing, commission reconciliation against host statements | Automatable plus monthly human review |

**Suppliers and fulfilment.**
- DQ software, the MVR vendor, the consortium/C-TPA and the lab/MRO network sit behind the consortium.
- The host agency holds the carrier appointments.

**Quality assurance.**
- A second check of every expiry date entered.
- A monthly exceptions report.
- 10% of files sampled quarterly against the 391.51 checklist.

**Exceptions:**
- a positive test (the consortium and MRO handle it under Part 40, with limits on intermediating [A, C4-S036]);
- a crash, which triggers post-accident testing within 8 or 32 hours (E: confirm in Part 382);
- an audit letter;
- an insurer non-renewal.

### 5.2 Software stack and prices
| Item | Price | Evidence |
|---|---|---|
| DOTDriverFiles | $5 per driver per month | B, C4-S008 |
| AgencyZoom | $99/month | B, DC-S015 |
| Quoting/rater/AMS | Host's in the base case; own ~$300/month later | MISSING; E |
| Compliance document portal | $200/month | E |
| LLM API / OCR | ~$150/month | E |
| E-sign, QuickBooks, phone | ~$150/month | E |
| Clearinghouse query | $1.25 + vendor | B, C4-S003 |
| MVR | $12.95 | B, C4-S008 |

**After December 2026.** The AI cost is ordinary API pricing of about $150 a month. If AI costs triple, year-3
operating profit falls to $31,798 (stress test, §7). The fallback is manual OCR and templates, at roughly 0.5
coordinator-hours more per client.

### 5.3 Legal and administrative requirements
| Requirement | Detail | Evidence |
|---|---|---|
| Illinois LLC | Fee MISSING (E ~$150) | MISSING |
| Illinois P&C producer licence | 40 h pre-licensing; exams within 90 days; NIPR application | A, DC-S005, DC-S007 |
| Business-entity licence | Only if we bill insurance ourselves; needs a designated responsible producer | A, DC-S006 |
| Broker bond | $2,500 or 5% of brokered premium (max $50k) when placing without an agent contract | A, DC-S005 |
| E&O | Platform median for agents is $781/yr at $1M/$1M; we budget $250/month to add compliance-services cover | C, E-SYN001-S013 |
| Clearinghouse service-agent registration | Required for the C/TPA role | A, C4-S037 |
| 49 CFR Part 40 | Testing-procedure limits | A, C4-S036 |
| Carrier POA | For IFTA, IRP and UCR filings | – |
| TCPA | No autodialed calls or texts to mobile phones | – |
| No legal advice | Avoid unauthorized practice of law | – |
| Driver PII | Data security (Illinois PIPA applicability not verified, E) | E |
| **Open questions** | Illinois rules on commission sharing, referral fees to unlicensed persons and producer fees: MISSING (ilga.gov TLS failure again). Secretary of State remitter licence for plates and titles: MISSING, so IRP plates are deferred | MISSING |

**Financial administration:**
- a separate operating account;
- a premium trust account only if the own-agency route is used;
- monthly reconciliation of host commission statements against bound policies;
- a chargeback reserve of 3% of commission.

---

## 6. Growth
**First 10 clients (months 3–12).**
- Walk the O'Hare cluster.
- Send renewal-timed letters to Cook and DuPage carriers whose filing month falls 3–5 months out.
- Run audits; waive setup for the first five.
- The model reaches 10.9 clients by month 12 [model].

**First 100 clients (about months 13–54).**
- Referral agreements with 3–5 factoring and dispatch firms.
- One language-community channel.
- A licensed producer hired at 60 active clients (month 40 in the base run).
- Base: 55 clients at year 3, 82.5 at year 4, 118.6 at year 5 [model].

**Hiring sequence (base model months):**

| Hire | Trigger | Month | Cost (loaded) | Productivity |
|---|---|---|---|---|
| Compliance coordinator #1 | 35 clients | 26 | $5,350/mo | ~60 clients each |
| Licensed producer | 60 clients | 40 | $6,000/mo | +1.5 clients/month after 4 months |
| Compliance coordinator #2 | 95 clients | 54 | $5,350/mo | ~60 clients |
| Licensed CSR | 150 clients (or own appointments) | – | $5,600/mo | – |
| Office manager / bookkeeper | $60k/month revenue | – | $5,000/mo | – |

Coordinator cost uses BLS Chicago clerk wages [C, C4-S016].

**Capacity limits:**
- Until month 26 the founder sells and services up to 35 clients, about 95 hours a month of servicing plus 90 hours
  of selling.
- Each coordinator handles about 60 clients (E).
- Hiring 30% earlier than planned drops year-3 profit to $264 (stress test). Coordinator productivity is a
  first-order driver.

**Geographic expansion.**
- **Compliance** can be delivered remotely to nearby markets such as NW Indiana and southern Wisconsin.
- **Insurance** needs non-resident licences. The Illinois non-resident fee of $380 shows the order of magnitude, but
  each state differs [A, DC-S006].
- **The local wedge does not travel.** Expand only once the Chicago churn and attach figures are proven.

**Adjacent services:**
- IFTA and IRP filings under POA;
- UCR, MCS-150 and BOC-3 filings;
- new-hire packets;
- premium-finance referral;
- occupational accident cover;
- fleet-safety coaching that lowers CSA scores, which can be marketed to underwriters;
- bookkeeping per mile, deferred (WS02-028 found it weak).

**Vertical integration: own appointments.**
- At 30 insured accounts × $72k, the book is $2.16M of premium.
- Moving from a 6% to a 10% net commission adds about $86k a year.
- That roughly equals a CSR at ~$67k plus AMS and extra E&O (~$9k), so it is marginal.
- At 60 insured accounts ($4.3M premium) the gain is about $173k against about $80k of cost: a high-return slot.
- Prerequisites: 2–3 years of tenure for Progressive [B, E-SYN001-S005], and carriers' production minimums (MISSING).

**When a manager can run it.** At about two coordinators, a producer and an office manager (base month 54+, ~$540k
revenue), the founder can hand day-to-day service to an operations lead. The designated responsible licensed
producer can be an employee [A, DC-S006].

**Reinvestment slots:**
1. more coordinators;
2. a second producer;
3. own agency appointments;
4. a second metro.

---

## 7. Financial analysis (model outputs quoted exactly from `SYN-001_results.json`)

### 7.1 How the model changed (corrections versus Stage D)
**Revenue per client (ARPC).**
- Stage D used a flat $405 a month, assuming 25% attach from day one at 10% commission net of a 20% split.
- **Correction:** attach can only accrue at renewal, and market access now sets the split.
- The base ARPC is now $305 in year 1, rising 9% a year: 3% from price and the rest from attach maturing at about
  5/14/21/25/28% across years 1–5.
- That reaches about $430 by year 5.

**Hiring triggers.**
- Stage D forced a producer hire at month 24 regardless of book size. That alone drove its conservative case to
  $603,950 of peak funding.
- **Correction:** the producer is hired at 60 clients.
- The CSR moves to 150 clients because the host agency services policies.
- Coordinator capacity is set at 60 clients, consistent with 2.7 hours per client-month. Stage D's 70 contradicted
  its own 3-hour line.

**Optimistic case.** It is cut from Stage D's $1.8M year-5 operating profit (ARPC $640) to $824,549. It is still an
upper tail.

**Standardization.**
- Owner draw of $4,000 a month from month 13 in all scenarios.
- Tax at 30%.
- Start capital of **$70,000**, the smallest round amount that keeps base cash ≥ 0. Base minimum cash is $672, in
  month 31.
- Long-term drivers are evidenced in the assumptions file.

### 7.2 Launch capital and working capital
**Setup capex** (licensing, LLC, computer, website, templates): $4,500 base, $6,000 conservative, $3,500 optimistic.

**Net working capital.**
- It is small because compliance is prepaid. Base DSO is 15 days.
- Year-1 change in working capital is $1,438.52; year 5 is $7,773.00.
- If customers pay 30 days later, peak funding rises to $87,134.

### 7.3 First 24 months, base case (engine monthly sheet, aggregated by quarter)
| Quarter | New clients | Active (end) | Revenue | Operating profit | Draw | Cash (end) |
|---|---|---|---|---|---|---|
| Q1 (m1–3) | 0.0 | 0.0 | $0 | −$7,890 | $0 | $57,610 |
| Q2 (m4–6) | 1.0 | 1.0 | $557 | −$8,574 | $0 | $48,893 |
| Q3 (m7–9) | 4.1 | 5.0 | $3,744 | −$8,515 | $0 | $39,847 |
| Q4 (m10–12) | 6.2 | 10.9 | $9,078 | −$4,716 | $0 | $34,367 |
| Q5 (m13–15) | 6.4 | 16.7 | $15,746 | $278 | $12,000 | $21,703 |
| Q6 (m16–18) | 6.6 | 22.4 | $21,509 | $4,876 | $12,000 | $13,779 |
| Q7 (m19–21) | 6.7 | 28.0 | $27,186 | $9,405 | $12,000 | $10,396 |
| Q8 (m22–24) | 6.9 | 33.6 | $32,779 | $13,867 | $12,000 | $11,487 |

**What the quarters show.**
- Month 24 revenue is $11,542 and operating profit $5,114, with 33.6 clients.
- Cash dips again after the first coordinator is hired in month 26, to its low point in month 31.
- In the conservative case cash goes negative in Q5 and is −$72,926 by month 24.

### 7.4 Five-year annual view
**Base case**

| Year | Revenue | Op. profit | Tax | FCF | Draw | Retained | Active clients |
|---|---|---|---|---|---|---|---|
| 1 | $13,378.92 | −$29,694.40 | $0 | −$35,632.92 | $0 | −$35,632.92 | 10.86 |
| 2 | $97,219.59 | $28,426.43 | $0 | $25,119.45 | $48,000 | −$22,880.55 | 33.58 |
| 3 | $202,072.25 | $48,347.97 | $0 | $42,659.57 | $48,000 | −$5,340.43 | 54.97 |
| 4 | $329,209.79 | $79,897.57 | $0 | $72,513.96 | $48,000 | $24,513.96 | 82.54 |
| 5 | $539,633.78 | $177,512.96 | $33,747.16 | $133,992.80 | $48,000 | $85,992.80 | 118.58 |

**Conservative and optimistic cases**

| Scenario | Y1 op | Y3 op | Y5 op | Y5 clients | Peak funding (draw) | Peak (no draw) | Breakeven | Payback |
|---|---|---|---|---|---|---|---|---|
| Conservative | −$44,432.54 | −$32,296.87 | −$13,063.64 | 18.40 | $357,302.53 | $165,303 | never | never |
| Base | −$29,694.40 | $48,347.97 | $177,512.96 | 118.58 | $69,327.91 | $36,634 | month 14 | month 54 |
| Optimistic | $428.47 | $245,704.21 | $824,549.15 | 281.98 | $16,863.00 | $16,863 | month 8 | month 15 |

"No draw" peaks come from the same engine with the draw set to 0; they are also reported by the comparison tool.

**What drives each case.**
- **Base:** 20 qualified conversations a month × 40% to proposal × 25% won ≈ 2 new clients a month at full pace,
  with 1.5% monthly churn and attach maturing to ~28%.
- **Conservative:** 12 conversations, 30% to proposal, 15% won, $236 ARPC, 2.2% churn and wholesale-only insurance. It
  never covers fixed costs of about $4.2k a month (overhead plus fixed marketing) plus the draw. It is a stop case.
- **Optimistic:** 25 conversations, 45% to proposal, 30% won, $375 ARPC rising 10% a year, 1.1% churn. It needs 282
  clients by year 5, which is 8.9% of the niche. Do not plan on it.

**Milestones (base):**

| Milestone | When |
|---|---|
| First profitable month | month 14 |
| ≥$1k/month operating profit | month 16 |
| ≥$5k/month | month 24 |
| ≥$10k/month | month 49 |
| ≥$25k/month | not reached within 60 months |
| $100k/year | year 5 ($177,513) |
| $250k/year | not reached in 10 years (year 10: $236,715) |

In the optimistic case, $25k a month arrives in month 34, and $500k a year in year 5.

**Founder pay.** Year-2 operating profit of $28,426 over about 2,200 founder hours is about $13 an hour; year 3 is
about $21 an hour. The early years are a low-paid job (see §11).

### 7.5 Sensitivity and stress (base)
**Tornado, year-3 operating profit at ±25%:**

| Driver | Low | High |
|---|---|---|
| Gross margin | $7,006 | $89,690 |
| ARPC | $8,729 | $87,967 |
| Labour cost | $63,956 | $32,739 |
| Overhead | $55,352 | $41,344 |
| Monthly churn | $55,416 | $47,351 |
| Founder leads / win rate | $49,210 | $62,444 |

The founder-leads row looks odd: fewer leads *raise* year-3 profit slightly. That happens because fewer clients delay
the coordinator hire. It is a step-function artifact, so judge capacity on year 5.

**Stress tests:**

| Test | Y3 op | Y5 op | Peak funding |
|---|---|---|---|
| CAC doubles | $35,565 | $161,027 | $100,694 |
| Win rate −40% / founder capacity −40% | $48,593 | $91,929 | $98,298 |
| Gross margin −10 pts | $28,141 | $123,550 | $104,645 |
| Key supplier refuses (3-month delay, −5 pts) | $37,699 | $133,383 | $101,307 |
| Labour +20% | $35,861 | $138,424 | $82,481 |
| AI/software ×3 | $31,798 | $159,955 | $113,289 |
| Hires needed 30% sooner | $264 | $38,039 | $163,249 |
| Recession (new −30%, churn ×1.5) | $51,806 | $76,449 | $92,893 |
| Competitor response | $17,300 | $29,583 | $165,578 |
| Growth takes twice as long | $20,227 | $60,314 | $137,787 |

**Extra downside runs** (same engine with overrides, not stored in the results file):
- **Insurance never attaches** (compliance only): year-3 $18,143, year-5 $59,362, peak funding $139,292.
- **Churn of 2.5% a month:** year-5 $103,280.

**The top drivers** are the price and margin per client (ARPC × gross margin) and coordinator productivity. Insurance
attach sits inside ARPC.

### 7.6 Capital accumulation to year 10 (base)
**Deployable cash** (after the draw, tax, maintenance capex, growth reinvestment and a 2-month reserve):
- **Years 1–3:** negative (−$42,812, −$27,167, −$19,496), funded by the injection.
- **Years 4–10:** year 4 $8,583, year 5 $67,191, year 6 $74,811, year 7 $84,068, year 8 $92,538, year 9 $100,166,
  year 10 $106,932.

**Ten-year totals:**
- **Cumulative positive deployable:** $534,288.72. It does not net off the ~$69k of early funding.
- **Year-10 operating profit:** $236,715.03.
- **Year-10 enterprise value** at 3.5× operating profit: $828,502.61. The multiple sits below the 6.8× average for
  independent agencies under $500k revenue [C, E-SYN001-S011], because of trucking churn and possible host ownership
  of expirations.
- **Owner draw over 10 years:** $454,483.67.

**Other scenarios.**
- **Optimistic:** ten-year deployable $4,031,768.89.
- **Conservative:** $0.

**Owner distributions.** Only the $4k-a-month draw before year 4. From year 5, about $67–107k a year is available to
fund other ventures in the base case.

---

## 8. Capital deployment ladder
| Tranche | What it buys | Evidence gate before spending | What could lose it |
|---|---|---|---|
| **$0–500** | FMCSA data ranking (done); materials; 12 market-access conversations (mileage); domain and email; letter templates | None | Founder time only |
| **$500–2k** | Pre-licensing course, exams, producer licence (~$700); LLC (~$150, E); first 300 letters (~$240); sample MVRs | ≥2 host or aggregator parties willing to put terms in writing; ≥10 carriers accept a free audit | Licensing fees, if no host signs |
| **$2–5k** | Setup kit ($4,500 base: computer and scanner, website, attorney review of service agreement, POA and BAA-style data terms); compliance-services E&O | Written host term sheet meeting V1; ≥3 paid pilots | E&O and legal fees, if pilots stall |
| **$5–10k** | Months 1–6 of fixed costs (~$2.6–3.5k/month) | ≥5 paying clients; ≥1 renewal submitted through the host | Burn, if conversion is <15% of audits |
| **$10–25k** | Run-rate losses through month 12 (base year-1 operating profit −$29,694) | ≥10 clients by month 9; quote permission ≥30%; ≥2 binds | Slow ramp; host underquotes |
| **$25–50k** | Founder draw from month 13 until operating profit covers it | ≥20 clients and break-even operating profit by month 15 | Cash crunch, if attach stays <10% |
| **$50–100k** | First coordinator (35 clients), producer (60 clients), working capital; base peak $69,328 | ≥35 retained clients; churn ≤1.5%/month for 6 months; attach ≥15%; SOPs written | Freight-recession churn; E&O claim; host terminates the agreement and keeps the book |

**Never** buy leads, sign aggregator joining fees or open an office before V1 and V2 pass.

---

## 9. Strategic wealth creation
**How it becomes a durable cash asset.**
- Three things compound: the renewal book, the held compliance records and the referral relationships.
- **Base case:** year-5 operating profit of $177,513, rising to $236,715 by year 10, with ~$70–107k a year
  deployable after the owner draw.
- **Total capital generated:** about $0.53M of deployable cash over 10 years plus a business worth about $0.83M at
  3.5×. Total owner wealth in the model is $1,817,275, including the draw.

**When management could take over.** Around year 5, once two coordinators, a producer and an office manager are in
place. The founder can then step back to principal-producer, ~15 hours a week (E).

**Can it fund other ventures?** Modestly, from year 5. It will not fund a large venture before 2031 in the base case.

**Is it a strong first company for a diversified holding company?**
- **For:** low capital ($37–69k at risk); mandated recurring demand; A-level buyer data; standard delegable roles; a
  sellable book.
- **Against:**
  - the profit engine depends on a third party (the host agency) until about year 3;
  - book ownership may not be ours;
  - the base case falls well short of the mandate's $500k-a-year FCF benchmark;
  - incumbents (OOIDA, Simplex, GEICO direct) cap pricing.
- **Verdict:** a solid, defensible small cash business ($150–250k a year) if V1 passes. It is not a compounding
  platform unless own appointments and a second metro follow. Rank it behind finalists with a stronger base case and
  no third-party dependency.

---

## 10. Execution plan

### First 7 days (spend $0)
**Founder:**
1. Read the materials file.
2. Shortlist 12 market-access targets:
   - Abis Insurance Services (Chicago);
   - Argo Insurance (Arlington Heights);
   - Cardinal Insurance Partners (Woodridge);
   - Elgin South Insurance (Hampshire);
   - ENSURE (Barrington);
   - Midwest Insurance Agency (Elk Grove Village);
   - Pro Guard Insurance Agency (Inverness);
   - Stassen Insurance Agency (Woodstock);
   - United-American Insurance Center (Arlington Heights) [B, E-SYN001-S018];
   - SIAA (Illinois master agency) and Smart Choice (Illinois state director);
   - Amwins ANTU, XPT and Cover Whale.
3. Book the first 4 conversations.

**Claude prepares** the host-agency inquiry, a one-page "what I bring" sheet (the FMCSA-ranked list of 3,166 carriers
with renewal months), the audit checklist, and a prospect board for the top 15.

**Questions to ask each party:**
1. Which of Progressive, Great West, Northland, Sentry, Acuity, Berkley and Auto-Owners/Secura can quote 3–20-PU
   for-hire Illinois risks under your codes?
2. What split do you pay on new and renewal business?
3. Who owns the expirations, and how do they vest?
4. Who services the policies (COIs, filings)?
5. Which E&O and appointment steps do you need from me?
6. What are your minimums and fees?
7. What are the termination and non-solicit terms?

**Evidence required:** a written term sheet or contract draft.

### First 30 days (spend ≤$600)
**Founder:**
- holds 12 market-access conversations;
- starts the pre-licensing course if ≥2 are positive;
- forms the LLC;
- walks the O'Hare cluster (Partner Carriers, Nationwide Logistics, Lion Logistics, Area Wide, OVN; not contacted
  yet);
- offers 10 free audits;
- sends the first 100 renewal-timed letters to Cook and DuPage carriers with March–May filing months.

**Claude prepares** audit reports from uploaded documents, proposal templates and the KPI sheet.

**Accept a first order when:**
- the client signs the service agreement and ACH;
- we can serve 8 or fewer drivers on DOTDriverFiles;
- no unresolved audit letter carries an imminent deadline that we cannot meet.

**Abandon when** no host offers terms after 12 conversations and fewer than 2 of 10 audits convert.

### First 90 days
**Milestones:**
- licensed (V3);
- host agreement signed (V1);
- ≥5 paying compliance clients (V2);
- the first 3 renewals (March–April filing months) submitted through the host (V5);
- a price test running (V6).

**Spend:** ≤$1,500 cumulative. **Decision:** at day 90, invest the $2–5k tranche only if V1 and V2 have passed.

### First year
| Point | Base milestones | Slow-growth branch | Failure branch |
|---|---|---|---|
| Month 6 | 1–2 clients in the model (aim for ≥5); ≥2 binds | <5 clients: cut office, keep home-based | – |
| Month 12 | 11 clients (model), ≥3 insured accounts, churn ≤1.5%/month | 5–10 clients: freeze spend, stay in letters plus referrals and delay the draw. Peak funding grows: growth taking twice as long means $137,787 | Attach <10% after 6 renewals, or the host terminates: stop the insurance thesis; sell or transfer compliance clients; total loss ≈ $10–25k |

---

## 11. Pre-mortem
| Scenario | How it happens | Early warning | Cheap prevention |
|---|---|---|---|
| **Lost $5k** | Licensed, but no host with standard carriers; only specialty quotes that run 20%+ above incumbent premiums | V1 fails after 12 conversations; <25% of 5 test submissions competitive | Run V1 before paying for licensing |
| **Lost $25k** | Compliance clients sign, but stay with their incumbent agent; attach <10% | <3 of the first 10 clients with renewals give quote authority | Tie the 20% compliance discount to placement; time audits for T−120 |
| **Lost $50k** | Coordinator hired at 35 clients, then freight recession churn (2.5%/month), plus an E&O claim from a missed expiry | Churn >2%/month for 3 months; any client fine traced to us | Dual-control expiry calendar; E&O that covers compliance services; hire only at 35 *retained* clients |
| **Revenue but no profit** | Selling compliance at $199 to 3–5-driver firms that never insure through us. Compliance-only year-5 is $59,362 | ARPC flat near $290 after month 18 | Minimum plan price; prefer 6+ driver firms |
| **Exhausting low-paid job** | Founder services 35 clients plus selling for ~$13–21/hour in years 2–3 | Founder >55 hours/week for 8 weeks | Raise prices, hire the coordinator earlier only if attach supports it |
| **Cash crunch** | Draw starts at month 13 while operating profit is ~$0; agency-bill premium owed to a GA | Cash < 3 months of fixed costs | Sub-producer route (no premium trust); keep the $70k backing undrawn until the gates pass |
| **Can't run without the founder** | Founder is the only licensed producer and the host relationship is personal | No producer by 70 clients | Hire the producer at 60; written host agreement assignable to the entity |
| **No deployable surplus** | Base deployable turns positive only in year 4; competitor response cuts year 5 to $29,583 | Year-3 operating profit < $30k | Stop at year 3 if the book is not compounding; sell clients to the host |
| **Regulatory shock** | The non-domiciled CDL rule (~194k drivers nationally, eligibility limited to H-2A, H-2B and E-2 [C, E-SYN001-S015]) shrinks client fleets | Clients losing drivers at onboarding MVR | Track driver eligibility in onboarding; do not over-concentrate in one community |

---

## 12. Required confirmations (the founder must confirm directly; none was confirmed by us)
**Supplier and market access:**
1. A host agency's written terms: carriers quotable for Illinois 3–20-PU for-hire risks, split, expiration ownership
   and vesting, servicing, non-solicit.
2. SIAA and Smart Choice Illinois: trucking carriers available to a start-up, fees, revenue share, departure terms.
3. Progressive commercial truck subcode criteria in Illinois.
4. Cover Whale: Illinois auto-liability availability and commission.
5. Amwins ANTU and XPT: retail-broker eligibility for a new agency.
6. Wholesale consortium/C-TPA pricing.
7. DOTDriverFiles multi-client dashboard.

**Regulatory:**
1. IDOI: whether a sub-producer must hold an appointment with each carrier or works under the host's code.
2. Whether the broker bond applies.
3. Entity licence fee ($150 vs $250).
4. Illinois rules on producer fees, commission sharing and referral payments to unlicensed persons (215 ILCS 5/500
   series, not readable this session).
5. The Illinois Secretary of State remitter licence for plates and titles.
6. Illinois LLC fee.
7. Data-privacy obligations for driver PII.

**Customer:**
1. Willingness to pay $249–$299 for 6–10 drivers.
2. Willingness to give quote authority at renewal.
3. Whether L&I filing months match actual policy anniversaries; ask during audits.

**Insurance (our own cover):**
1. E&O cost and wording covering compliance administration, not only insurance placement.
2. Cyber cover for driver PII.
3. Workers' comp from the first hire.

---

### Corrections made in this stage (summary)
1. **Attach.** It accrues only at renewal; base ~5% in year 1 rising to ~28% by year 5, not 25% from day one.
   Realistic year-3 range: 10–25%.
2. **Market access.** The aggregator-plus-MGA route is unproven for the niche's dominant carriers. Progressive
   subcodes need 2–3 years of experience. The base plan is a sub-producer arrangement.
3. **Agency-bill.** On the wholesale route it is a producer obligation, not an avoidable choice.
4. **Hiring.** The producer hire is milestone-gated, not calendar-based; coordinator capacity is aligned to 2.7
   hours per client; the CSR moves to 150 clients.
5. **Optimistic case.** Cut from $1.8M to $824,549 in year 5.
6. **Renewal-date test.** Stage D's validation 5 is answered from public data: 87% have a filing month.
7. **Churn.** Refined with revocation data at 2.4–5.8% a year among established carriers. Book churn is driven by
   30–37% annual insurer switching, not by carrier death.
8. **E&O budget.** Lowered to $250 a month on the Insureon median [C, E-SYN001-S013].
