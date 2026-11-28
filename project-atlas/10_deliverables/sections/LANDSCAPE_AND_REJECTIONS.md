# Landscape and Rejections

*Stage A discovery and Stage B screening, as of 2026-11-28. Citations follow EVIDENCE_STANDARDS.md as [evidence level, source ID]. Record IDs (WSxx-nnn) refer to `09_databases/opportunities.jsonl`; dispositions and scores come from `03_screening/screening_dispositions.csv`. Composites run 1–10, where 5 means a typical small business. "Adj" is the evidence-adjusted composite; current scores average the author score and the blind re-score. Stage C–F results (investigations, deep dives, playbooks, adversarial review) are summarized in `MASTER_RESEARCH_REPORT.md` and `INDEPENDENT_REVIEW_REPORT.md`; this chapter reflects the Stage A–B view.*

## 1. The opportunity landscape

### 1.1 What 630 ideas showed

The 18 workstreams produced 630 records backed by 630 sources. Deduplication linked 37 as duplicates (593 distinct ideas), and 7 cross-stream bundles (SYN-001…007) were added. Dispositions: 74 Stage C (67 records plus 7 bundles), 59 Stage B only, 444 deprioritized, 23 gate failures, 37 merged.

Three facts frame the rest of this chapter.

1. **The field is flat.** Adjusted composites range from 1.28 to 6.33 (mean 4.75). Only 3 records reach 6.0: WS05-007 commercial pest control (6.33), WS02-028 vertical bookkeeping (6.05) and WS13-004 first-aid route (6.02). Thirty reach 5.5. The Stage C core cut fell near 5.40 and the best deprioritized record scored 5.17. Gaps of 0.1–0.2 points are noise, which is why Stage C also includes nine judgment picks covering value-capture families the cut would have dropped (DECISION_LOG).
2. **No idea has an evidenced cold-start path to large owner cash.** Blind scorers gave only 53 of 630 records (8%) an fcf score of 5 or more (roughly $100–150k owner FCF a year in years 3–5) and none a 7 (about $250–400k). Authors themselves capped 204 records (32%) at $10k/month or less. No WS07 (logistics), WS08 (government), WS09 (information) or WS15 (regulation-driven) record reached fcf 5 under blind scoring. Our reading: the realistic prize is a $100–250k/yr business that grows through route density, adjacent service lines and, later, acquisitions.
3. **The strongest evidence mostly argues against ideas.** Statutes, agency data and public filings (A/B) are plentiful; private prices and new-entrant margins are not. 87% of records rest on D- or E-level economics (Section 5). The rankings are a validation queue, not conclusions.

### 1.2 Structurally attractive for this founder

Five families account for most of Stage C. Mechanism averages come from COMMERCIAL_MECHANISMS.md.

**(a) Mandated, recurring inspection and compliance routes where the credential is cheap or hireable.** The mechanisms recurring_service_contract (177 records, 43 in Stage C), compliance_workflow (114; 25), inspection_testing (63; 14) and geographic_density (51; 12) average 4.98–5.08 adj, near the top of the mechanism table. Examples:
- **Commercial pest control (WS05-007).** The IDPH business licence costs $250 and needs one certified technician; the technician exam is $75 with no stated experience prerequisite [A, WS05-S012, WS05-S013]. Chicago cited 2,147 food licences for insect or rodent violations in 13 months, a self-refreshing prospect list [A, WS05-S034].
- **Extinguisher and exit-lighting route (WS05-001).** OSFM Class A distributor licence $900 for three years [A, WS05-S001]; only 184 distributor licences are active statewide [A, WS05-S014].
- **Crane and hoist inspection (WS03-012).** OSHA requires periodic inspections at 1–12 month intervals with certification records [A, WS03-S015].
- **Construction stormwater (WS11-021).** ILR10 requires inspection every 7 days and within 24 hours of 0.5" of rain; a free USEPA course qualifies the inspector [A, WS11-S040].
- **UST compliance (WS15-020).** 17,822 active Illinois tanks; walkthrough compliance 83%, technical compliance 76% [A, WS15-S029].

They fit because rules, not discretion, set demand; buyers appear in public data; density lifts margin; technician and scheduler roles are standard and delegable; and consolidators buy such firms (2.2). The caution: WS05 found no primary price for any service, and the inspection-to-repair pull-through that carries much of the margin is unmeasured.

**(b) Consumable and equipment-as-a-service routes to fragmented workplaces.** First-aid restocking (WS13-004), dishmachine chemicals (WS13-001), restroom hygiene (WS05-025), kitchen wear parts (WS13-009). Incumbent margins are A-level and high: Cintas First Aid & Safety 57.7% gross and 25.4% operating [A, WS13-S003]; Ecolab Institutional 22.8% operating [A, WS13-S005]. Capital per account is small and accounts switch. An entrant will not earn incumbent margins, and its wedge, service quality, is easy to copy.

**(c) Vertical back-office managed services.** Vertical bookkeeping (WS02-028, which absorbed WS12-022), niche payroll (WS02-026), prevailing-wage certified payroll (WS15-023), specialty billing (WS04-010), dental/vet managed IT (WS04-014), insurance-agency back office (WS02-018). managed_service is the highest-scoring mechanism (5.12; 11 of 33 in Stage C), and these are the most stable ideas under re-weighting: across 1,000 random weight perturbations WS02-028 stayed top-10 every time and WS02-026 95% of the time (rankings.md). Paychex keeps 82–83% of payroll clients and gets over half from CPA, broker and bank referrals [A, WS02-S022] (incumbent). Weakness: D/E economics, and AI is both their cost lever and their substitution threat (2.6).

**(d) Renewal-commission insurance agencies in one vertical.** Trucking (WS02-001), contractors (WS02-002), small landlords (WS02-004). A producer licence takes 20 hours per line and $215 [A, WS02-S001, WS02-S003]. A published regional schedule pays 15–20% on most commercial lines, the same on renewal [B, WS02-S016]. The book is sellable: 695 agency deals in 2025 [C, WS02-S006], about 11.4x EBITDA for agencies above $1M EBITDA [C, WS02-S007]. The binding barrier is carrier and aggregator access, whose terms are unverified.

**(e) Labour-led household services with franchise-disclosed revenue.** Home care (WS18-002): Home Instead units average $2.61M at about $33 per client-hour [B, WS18-S005]; A Place At Home outlets keep 42–64% gross profit after caregiver labour [B, WS18-S006]; Illinois CCP pays $30.80/hour [A, WS18-S020]. Lawn fertilization (WS18-004): Weed Man units average $2.04M [B, WS18-S007]. Junk removal (WS18-003): 56.3% gross profit after fees [B, WS18-S001]. WS18-002, WS18-003 and the GPO WS14-019 are the only Stage C records with B-level economics. Disclosed revenue is still not owner profit (see the handyman row in Section 3).

By workstream, Stage C draws most from WS18 (9), WS13 (8), WS02 (7), WS04 (6) and WS03, WS05, WS11 (5 each). WS06 and WS09 placed none.

### 1.3 Structurally unattractive for this founder

- **Consumer brands and marketplace selling (WS06).** High gross, near-zero or negative operating margins: BARK about 62% gross and −7% to −12% operating every year [C, WS06-S023], with Zevia and Honest similar [C, WS06-S021, WS06-S024]; Pattern, a $3.3B exclusive marketplace reseller, made 1.0% operating margin in 2025 [C, WS06-S010]. Amazon referral fees of 8–17% plus a 2026 FBA increase [B, WS06-S001, WS06-S002], the end of de minimis [A, WS06-S032] and stacked Section 301 duties [A, WS06-S006] compound it. private_label (4.21) and marketplace_seller (4.48) sit near the bottom of the mechanism table.
- **Owning production or a fleet.** U.S. machine shops keep about 10% of shipments after materials, payroll, depreciation and rent, and hold about $1.32M of machinery each [C, WS03-S007]. Herc's 38.5% dollar utilization [B, WS10-S027] means each fleet dollar earns about $0.39 a year before depreciation. Republic Services spends 11.4% of revenue on capex [A, WS11-S009]. financing_own_capital is the lowest mechanism (4.13): a six-person public hard-money lender earns about 12% on equity [B, WS01-S032], implying $10–15k a year on a $100k book before losses (E).
- **Commodity distribution and resale.** Independent merchant wholesalers average 20.1% gross and about 6.9% implied operating margin [C, WS16-S018, WS16-S019]; Patterson Animal Health about 3.4% operating [B, WS04-S026]; CDW 7.4% [A, WS08-S037]. A newcomer without rebates starts 4–8 points below incumbent gross margin (E).
- **Transactional brokerage without recurrence.** Agents and brokers realize about 4.5% average commission [C, WS16-S020]; about 33k freight brokers compete for freight on which the largest keeps about 13.5% [A, WS07-S001, WS07-S008]. Blind scorers cut brokerage mechanisms the most (Section 4).
- **Labour-arbitrage staffing.** TrueBlue earned 0.7% adjusted EBITDA on 22.8% gross margin [B, WS12-S010]; Robert Half's contract segment ran −0.8% operating margin on 39.0% gross [B, WS12-S007].
- **Pure information products.** Chegg's revenue fell 39% in 2025 as search changed [B, WS09-S012]; unmandated exam prep, directories and content licensing are in AI's direct path.
- **Government procurement as the primary channel.** Demand is A-level (DLA obligations $58.3B in FY2025 [A, WS08-S017]; E-Rate Category 2 $1.52B [A, WS08-S041]), but there is almost no A/B evidence of what small resellers keep, and policy is consolidating buying into GSA [A, WS08-S032]. government_contracting averages 4.54.

## 2. Cross-cutting findings

**2.1 Permanent state and local compliance cycles last; federal deadline surges do not.** Recurring obligations appear in WS03, WS05, WS11, WS15 and WS17: OSHA crane inspections [A, WS03-S015], ILR10 stormwater [A, WS11-S040], AHERA three-year school asbestos reinspections [A, WS15-S020], UST walkthroughs [A, WS15-S029], and Illinois's own truck safety tests at about 260 Official Testing Stations [A, WS17-S007]. Federal deadline demand kept collapsing in 2025–26:

| Federal driver | What happened | Source |
|---|---|---|
| Corporate Transparency Act filing | U.S. companies exempted; ~28k filers left of 32.6M | [C, WS15-S004] |
| FinCEN residential real-estate rule | Vacated 2026-03-19 | [A, WS15-S031] |
| WOTC hiring credit | Lapsed for hires after 2025-12-31 | [A, WS12-S025] |
| ADA Title II web rule | Deadlines moved to 2027/2028 | [A, WS15-S001] |
| PFAS drinking-water rule | Narrowed (proposals of 2026-05-18) | [A, WS15-S006] |
| 25C/25D; 30C; 179D | Ended 2025-12-31; 2026-06-30; construction after 2026-06-30 | [A, WS11-S017, WS11-S018, WS11-S019] |

A mandate also fails when the state supplies the service free (IDHR harassment training [A, WS09-S003]) or attracts a glut (18,384 active ELDT driver-training providers [A, WS09-S023]). Mandates protect margin only where delivery is in person, licensed or supply-limited; only 8 providers may sell OSHA outreach training online [A, WS09-S018].

**2.2 Private-equity roll-ups cluster where the attractive ideas are — evidence of exit demand, not entrant profitability.** APi Group: inspection-first, 140 acquisitions since 2005 [A, WS05-S019]. Rollins: 44 acquisitions in 2024 and 26 in 2025 [A, WS05-S018]. Cintas Fire Protection: $729M to $929M revenue in two years [A, WS05-S024]. Pye-Barker about 246 locations [C, WS05-S020]; Service Logic states no revenue floor [C, WS05-S030]; Crane 1 at 30 locations [C, WS03-S016]; about 196 industrial-services add-ons in 2025 [D, WS03-S017]; GPRS 13 locating acquisitions [D, WS13-S033]; Bunzl 220–230+ acquisitions since 2004 [B, WS16-S031]; 695 insurance-agency deals [C, WS02-S006]; the Cintas–UniFirst merger agreement [A, WS13-S004]; C.H. Robinson acquiring RXO for $5.8B [A, WS07-S010]. Two cautions: consolidators are also the price competitors a newcomer faces, and in some verticals consolidation removes customers (dental-group and corporate-vet roll-ups shrink the independent base, WS04; Accel paid about $0.84M per Illinois gaming location [A, WS13-S013]).

**2.3 In Illinois, who may legally do the work decides entry more than demand does.**
- *Obtainable by the founder in weeks to months:* insurance producer [A, WS02-S001]; OSFM extinguisher employee licence ($300 per class) backed by an open-book NAFED/ICC exam [A, WS05-S002; B, WS05-S025]; IDPH pest technician [A, WS05-S013]; IDOA applicator, $300 for three years [A, WS18-S019]; IEMA radon via course plus NRPP/NRSB exam [A, WS18-S016]; IDPH asbestos [A, WS11-S042]; scale service agency, $100/yr [A, WS03-S028]; Chicago Class E general-contractor licence with no exam [A, WS10-S004].
- *Verified workarounds:* success-fee-only business-loan brokers are exempt from Loan Brokers Act registration [A, WS01-S002]; commercial-only mortgage lending falls outside RMLA [A, WS01-S004]; Form IL-2848 accepts a non-credentialed "other" representative for sales-tax refunds [A, WS14-S008].
- *Must be hired:* sprinkler inspectors (699 licensed statewide [A, WS05-S015]), plumbing-qualified backflow testers, a licensed funeral director for direct cremation, a managing broker for property management.
- *Closed or uneconomic:* Cook County Board of Review practice is attorney-only [A, WS14-S001, WS15-S015]; unclaimed-property finders face a 10% fee cap, Treasurer licence and fidelity bond [A, WS14-S004, WS14-S005]; process serving as a business effectively needs private-detective licensure [A, WS12-S018]; a wholesaling pattern counts as brokerage [C, WS10-S017]; customs brokerage needs the CBLE, with recent pass rates of 12–30% [A, WS07-S025; C/D, WS07-S026, WS07-S027].

One conflict is live: SBA SOP 50 10 8.1 bars contingency fees charged to 7(a) applicants [A, WS01-S013], which probably pushes applicant-paid packagers outside the Illinois contingency exemption (WS01's reading; needs counsel). ilga.gov returned 503 throughout, so much statute text came from mirrors.

**2.4 Tariffs and de minimis: volatile, net hostile to import-dependent models.** The Supreme Court held on 2026-02-20 that IEEPA does not authorize tariffs [A, WS16-S022]. A 10% Section 122 surcharge ran 2026-02-24 to 07-24 (sources conflict on a rise to 15%) [C, WS03-S010, WS06-S007], replaced by Section 301 duties of 10–12.5% on 60 economies [A, WS06-S006]; Section 232 duties of 50% on steel, aluminium and copper remain [C, WS03-S011]. The $800 de minimis exemption was suspended indefinitely for non-postal shipments on 2026-06-24 [A, WS06-S032]; statutory repeal is reported for July 2027 (press date, WS07-S032). About $166B of IEEPA refunds is flowing through CBP's CAPE system [C, WS14-S011]; Fastenal's refunds were limited because it is not the importer of record [A, WS16-S021]. Effects: consumer private label and children's products weaken (WS06); refund advisory is a crowded one-time window (WS14-012, WS07-016); customs brokerage and duty drawback gain (WS07-015, WS14-013); domestic sourcing is a selling point for contract-manufacturing brokerage (WS03-001) but not a foundation (WS03-002 on hold).

**2.5 Illinois labour law and labour supply constrain every people-heavy model.** The amended Day and Temporary Labor Services Act (DTLSA) requires equal pay after 720 hours at one client [C, WS12-S003]; a federal court denied an injunction against its equal-benefits clause on 2025-05-22, so it is enforceable [A, WS12-S001]; registration is $3,000 plus $750 per branch and a bond [A, WS12-S004]. Its Section 67 "interested party" suit provision was held unconstitutional at trial level in March 2026, on appeal [C, WS12-S005]. Nurse-agency enforcement expanded in 2025 [A, WS04-S010]. Medicaid home care faces the unresolved 80/20 rule [C, WS04-S009], and Addus reports only "low 20%" margins on added Illinois hours [B, WS04-S004]. Net effect: avoid light-industrial and per-diem staffing; prefer direct hire (IDOL licence $250–500 and $5k bond [A, WS12-S015]), clerical or professional niches that may be exempt from registration, and W-2 route models. Separately, skilled-labour scarcity (sprinkler inspectors, crane technicians, biomedical technicians, caregivers) is the most common operating constraint, and wage evidence is E everywhere because BLS data was inaccessible.

**2.6 AI commoditizes information and clerical work; it helps only where something else anchors the deliverable.** Chegg revenue −39% [B, WS09-S012]; BLS projects 0% court-reporter growth, citing AI transcription [C, WS12-S022]; Robert Half lists client automation as a risk factor [A, WS12-S008]; Kforce Finance & Accounting revenue −12.3% [A, WS12-S009]; C.H. Robinson cut North American Surface Transportation headcount 11.4% while volume rose 3.5% [A, WS07-S008] (the AI attribution of the last two is the authors', not the filers'). Records rejected mainly for AI substitution: transcription, translation, answering services, outbound SDR, hourly screening, grant writing, exam prep, directories (WS12-027, -028, -033, -031, -017, -030; WS09-014, -032). AI is a durable cost edge only where the deliverable is anchored by a licence, a seat-time mandate (Illinois still requires 7.5 classroom hours per insurance line [A, WS09-S002]), a physical service or filing liability. Blind scorers cut the ai criterion more than any other (Section 4), consistent with the mandate: AI cannot rescue weak economics, and heavy AI access ends 2026-12-05.

**2.7 Freight is in a supply-driven squeeze, not a recovery.**

| Indicator | Evidence |
|---|---|
| Costs outrunning prices | C.H. Robinson cost per mile +33.5% vs price +31.5% [A, WS07-S008] |
| Spot below contract (Oct.) | Van $3.05 vs $3.28; flatbed $3.61 vs $4.05; volumes −2% to −9% [C, WS07-S013] |
| Broker margin | RXO brokerage gross margin down to 12.6% [A, WS07-S010] |
| Fraud and claims | Cargo theft ~$725M, +60% [C, WS07-S016]; Landstar insurance and claims $33.0M→$55.3M [A, WS07-S011] |
| New-authority friction | Motus identity proofing [A, WS07-S002]; BMC-85 trusts limited to cash, letters of credit or Treasuries [A, WS07-S001] |
| Equipment | Rush new Class 8 gross margin 8.6% [A, WS17-S021] |

Spillovers: trucking insurance (WS02-001) and DOT compliance (WS17-001) face carrier churn; used-truck dealing (WS17-010) was rejected. The eight Chicago-area counties hold 36,851 active carriers as a prospect base [A, WS17-S001].

**2.8 Other recurring patterns.**
- *Gross margin is not owner profit:* Robert Half permanent placement 99.8% gross but 2.9% operating [B, WS12-S007]; Ace Handyman owners keep 2–11% of revenue [B, WS18-S009]. None of the five franchise-mechanism records advanced; Goosehead's 50% renewal royalty and ownership of the policies [A, WS02-S011] defeat the equity goal.
- *Rates and housing:* 30-year mortgages 7.21% [C, WS10-S019]; single-family permits −12.9% y/y [C, WS10-S020]; Chicago permits 48,540 (2019) → 32,032 (2025) [A, WS10-S010]; Builders FirstSource operating margin 12.7% → 5.2% [A, WS10-S028]; retainage up to 10% [A, WS10-S029]. This favours rental operations (unit turns, WS10-016) and code-driven repair over new construction.
- *Public data is a lead engine, not a product:* Chicago food inspections, building violations, permits, energy benchmarking (542 non-submitting buildings [A, WS15-S010]), the FMCSA census, OSFM rosters, USAC and USASpending gave A-level prospect lists in at least seven workstreams; as standalone products the idea was weak (WS10-006; WS09-015 merged).
- *Energy:* PJM capacity cleared at the cap, $329.17 and $333.44/MW-day [A, WS11-S020], a tailwind for advisory models, but competitive suppliers already serve 83–87% of Illinois non-residential load [A, WS15-S026].
- *Public payers:* Medicare home health −1.3% for 2026 and DMEPOS bidding back by 2028 [A, WS04-S008]; Medicaid work requirements by January 2027 [C, WS04-S007]; Illinois general-funds payables of $1.45B across 17,398 vouchers [A, WS08-S028]. Private-pay variants were preferred throughout.

## 3. Notable rejections and why

All 23 gate failures come first. Outcome shows the current adjusted composite and economics evidence level; "Depr." means below the Stage B cut (ranked below 130th).

**3.1 Capital gate (G1: more than $100k at risk before first revenue)**

| ID | Idea | Outcome | Decisive reason |
|---|---|---|---|
| WS18-021 | Express car wash with memberships | G1 fail (C) | $3–8M per new site; Mister Car Wash's 32.8% adjusted EBITDA is scale economics [A, WS18-S022] |
| WS18-022 | Self-storage development | G1 fail (E) | $2–10M plus years of lease-up; buying a site is outside the mandate |
| WS18-023 | New-build laundromat | G1 fail (E) | $300k–1M with personally guaranteed equipment |
| WS18-016 | Licensed child care centre | G1 fail (E) | $0.4–3M facility plus pre-opening payroll; heavy IDEC rules [A, WS18-S015] |
| WS18-015 | Dog daycare and boarding | G1 fail (E) | $150–800k build-out and lease deposits |
| WS06-024 | Winmark resale franchise | G1 fail (B) | Best-evidenced WS06 record (store gross profit $625–846k [B, WS06-S013]) but $339–486k to open |
| WS03-022 | Hydroblasting and vacuum trucks | G1 fail (D) | $150–600k of trucks; plants vet vendors on safety records a newcomer lacks |
| WS05-018 | Independent elevator contractor | G1 fail, blind (E) | OSFM-licensed mechanics [A, WS05-S022], union labour and manufacturer oligopoly; $100–300k payroll before contracts |
| WS04-005 | Medicare home health or hospice | G1 fail, blind (E) | $150–500k before certification; 2026 Medicare HH −1.3% [A, WS04-S008] |
| WS04-006 | Adult day centre | G1 fail, blind (E) | $100–350k and ~12 months to revenue; year-3 high case only $100k |
| WS02-016 | Niche MGA | G1 fail, blind (E) | Carriers want an underwriting record; $100–500k |
| WS02-022 | Premium finance company | G1 fail, blind (E) | Funds premiums up front: $100k–1M equity plus a bank line; licence needs $50k net worth [A, WS02-S025] |
| WS07-029 | Public warehousing | G1 fail, blind (E) | $100–500k plus a lease liability; record cites no sources |
| WS11-006 | Crop-input retail | G1 fail, blind (E) | 5–15% margins plus 6–12 months of grower credit, against co-ops |
| WS08-032 | DoD Fresh produce distribution | G1 fail (D) | Needs cold-chain fleet, warehouse and audits; $150–500k |
| WS16-026 | Stocking branch (pool, irrigation, waterworks) | G1 fail (A) | Inventory-heavy, slow-turn incumbents [A, WS16-S005, WS16-S007, WS16-S008] |
| WS12-013 | On-demand shift-staffing app | G1 fail (D) | Marketplace burn; PeopleReady earned $6.5M on $884M [B, WS12-S010] |
| WS13-026 | Illinois video gaming terminal operator | G1 fail (C) | $150–500k, ~18 months of licensing, locations already contracted [A, WS13-S013, WS13-S014] |
| WS10-028 | Prefab wall panels and trusses | G1 fail (C) | $250k–1.5M plant at a housing trough [A, WS10-S028] |

**3.2 Legal/ethics gate (G3) and licence gate (G2)**

| ID | Idea | Outcome | Decisive reason |
|---|---|---|---|
| WS01-006 | Merchant cash advance (MCA) brokerage | G3 fail (D) | Relies on renewals and stacking to distressed merchants; TX, NY, CA broker rules tightening [A, WS01-S014, WS01-S015, WS01-S018] |
| WS06-028 | Hemp THC/CBD products | G3 fail (A) | Federal redefinition bans >0.4 mg THC per container from ~2026-11-12 [A, WS06-S015] |
| WS06-029 | Vape shop | G3 fail (E) | A competitive range relies on unauthorized e-cigarettes |
| WS14-005 | Cook County property-tax appeals | G2 fail (A) | Attorney-only Board of Review; fee-splitting barred [A, WS14-S001]; HB4931 pending [A, WS14-S003] |

**3.3 Legal or regulatory walls short of a gate failure**

| ID | Idea | Outcome | Decisive reason |
|---|---|---|---|
| WS15-027 | Property-tax analytics for appeal attorneys | Depr. 4.65 (E) | Attorney-only rule removes the contingency fee; small data niche left [A, WS15-S015] |
| WS14-006 | Unclaimed-property finder | Depr. 3.73 (A) | 10% fee cap, Treasurer licence, bond up to $100k [A, WS14-S004, WS14-S005] |
| WS10-033 | Real-estate wholesaling | Depr. 3.96 (E) | Counts as brokerage [C, WS10-S017]; aggressive distressed-seller marketing |
| WS01-021 | Residential note buying | Depr. 3.79 (E) | RMLA licence plus $150k net worth [A, WS01-S004, WS01-S006] |
| WS01-029 | Small-dollar consumer lending | Depr. 3.65 (E) | 36% APR cap leaves no room for losses at small scale [A, WS01-S020] |
| WS05-005 | Backflow testing route | Depr. 4.98 (E) | Tester needs plumbing qualification (4-year apprenticeship); $75–200 commodity tickets |
| WS12-025 | Process serving and skip tracing | Depr. 4.05 (D) | Effectively needs private-detective licensure [A, WS12-S018, WS12-S020] |
| WS02-012 | Final-expense life telesales | Depr. 4.54 (E) | Bought leads, chargebacks, TCPA exposure |
| WS07-016 | Unlicensed tariff-refund advisory | Depr. 3.82 (D) | Temporary; filings need a licensed broker or attorney |

**3.4 Mandate removed or incentive ended**

| ID | Idea | Outcome | Decisive reason |
|---|---|---|---|
| WS15-034 | FinCEN real-estate reporting | Depr. 1.81 (A) | Rule vacated 2026-03-19 [A, WS15-S031] |
| WS15-033 | CTA beneficial-ownership filing | Depr. 2.60 (C) | U.S. companies permanently exempt [C, WS15-S004, WS15-S005] |
| WS12-019 | WOTC screening | Depr. 2.94 (A) | Credit lapsed [A, WS12-S025]; duplicate WS14-015 merged |
| WS14-012 | IEEPA refund filing support | Depr. 3.22 (C) | One-time window, already crowded [C, WS14-S011] |
| WS11-016 | Residential solar after 25D | Depr. 3.58 (D) | Credit ended [A, WS11-S017]; 974 approved vendors [B, WS11-S045] |
| WS09-005 | Paid harassment-prevention training | Depr. 3.60 (A) | State provides it free [A, WS09-S003, WS09-S024] |

**3.5 Platform dependence and customer-acquisition cost**

| ID | Idea | Outcome | Decisive reason |
|---|---|---|---|
| WS06-001 | Amazon FBA private label | Depr. 4.14 (D) | One platform; 8–17% referral plus FBA fees [B, WS06-S001, WS06-S002]; copycats; tariffs |
| WS06-006 | TikTok Shop brand | Depr. 3.80 (D) | 6–8% referral plus 10–20% creator commission [D, WS06-S014]; fad risk |
| WS14-009 | Amazon reimbursement recovery | Depr. 4.64 (E) | Wholly dependent on Amazon policy, which Amazon is automating |
| WS07-026 | Amazon delivery partner (DSP) | Depr. 4.34 (E) | One customer sets price and volume and can terminate |
| WS10-030 | Chicago short-term-rental co-hosting | Depr. 4.33 (D) | Only 3,712 registered units [A, WS10-S013]; primary-residence rules |
| WS06-007 | Retail and online arbitrage | Depr. 3.95 (E) | Capped by founder hours; suspension risk |

**3.6 Incumbent economics, thin margins and working capital**

| ID | Idea | Outcome | Decisive reason |
|---|---|---|---|
| WS07-001 | Freight brokerage with own authority | Depr. 4.85 (C) | ~33k brokers; incumbent keeps 13.5% [A, WS07-S008]; $75k security [A, WS07-S001]; shippers pay in 30–60 days, carriers want quick pay |
| WS07-002 | Freight agent under a host broker | Depr. 4.86 (C) | Income is founder sales labour; Landstar's 7.8% is mature-agent data [A, WS07-S011] |
| WS12-001 | Light-industrial temp staffing | Depr. 4.03 (C) | 0.7% incumbent EBITDA [B, WS12-S010]; DTLSA equal pay and benefits [A, WS12-S001]; payroll float |
| WS10-022 | Construction equipment rental | Depr. 3.69 (C) | 38.5% dollar utilization [B, WS10-S027]; United Rentals $4.2B annual rental capex [B, WS10-S026] |
| WS07-019 | Liquidation pallets and bin stores | Depr. 3.97 (C) | Incumbent makes ~19% gross on goods it buys and is shifting to consignment [A, WS07-S036] |
| WS03-026 | Owned CNC job shop | Depr. 4.23 (C) | ~10% residual and $1.32M machinery per shop [C, WS03-S007] |
| WS04-022 | Dental and vet consumables | Depr. 3.74 (B) | Incumbent operating margins 3.4–8.4% [B, WS04-S026] |
| WS05-029 | Facilities-maintenance aggregator | Depr. 4.67 (E) | 10–25% gross on pass-through spend, negative float; Lessen has 34K vendors [C, WS05-S031] |
| WS01-002 | Generalist small-business loan brokerage | Depr. 4.68 (C) | Commoditized; a large lender's broker programme is "at full capacity" [D, WS01-S026] |

**3.7 Ownership structure defeats the wealth goal**

| ID | Idea | Outcome | Decisive reason |
|---|---|---|---|
| WS02-015 | Goosehead-type insurance franchise | Depr. 4.13 (B) | 20% new / 50% renewal royalties; franchisor owns the policies [A, WS02-S011] |
| WS02-014 | Captive carrier agency | Depr. 4.68 (E) | Carrier controls the book |

**3.8 AI substitution**

| ID | Idea | Outcome | Decisive reason |
|---|---|---|---|
| WS12-027 | Transcription services | Depr. 3.54 (D) | Near-total speech-to-text substitution [C, WS12-S022] |
| WS12-033 | Answering service | Depr. 4.45 (E) | AI voice agents undercut it |
| WS09-014 | Trade-licence exam prep | Depr. 4.58 (E) | Unmandated content in AI's direct path |

**3.9 Low ceiling, declining demand or founder-capped**

| ID | Idea | Outcome | Decisive reason |
|---|---|---|---|
| WS18-008 | Handyman company | Depr. 4.99 (B) | Owners keep 2–11% of revenue [B, WS18-S009] |
| WS13-025 | Ignition-interlock service centre | Depr. 4.16 (B) | ~$20 per calibration; ceiling near $10k/month |
| WS13-033 | Apostille expediting | Depr. 4.87 (E) | Convention accessions shrink demand [A, WS13-S035] |
| WS03-029 | 3D-printing service bureau | Depr. 3.77 (C) | Protolabs 3D printing −4.1% while CNC +17.6% [C, WS03-S003] |
| WS02-033 | Chicago currency exchange | Depr. 4.17 (E) | Secular decline; cash float and security costs |

**3.10 Access walls**

| ID | Idea | Outcome | Decisive reason |
|---|---|---|---|
| WS02-013 | Crop insurance agency | Depr. 4.57 (E) | Multi-generational farm relationships; ~36-month ramp |
| WS11-003 | Independent seed dealership | Depr. 4.19 (E) | Grower base locked into existing relationships |

## 4. Calibration

Twelve independent scorers re-scored all 630 records in 13 packets without seeing authors' scores, rationales, gates, verdicts or evidence ratings.

- **Direction and size.** Mean raw composite fell from 4.81 (author) to 4.41 (blind), −0.40. Blind was lower on 554 records (88%), higher on 69, equal on 7. The drift was consistent but modest: gaps above 2 points on one criterion occurred on 1% of records or fewer, and only 28 records differed by more than 1.0 composite point. Because current scores average the two, they still carry about half the measured optimism (~0.2 raw points above the blind view).
- **By workstream.** Inflation was highest in WS02 insurance/payments (+0.70), WS08 government (+0.68) and WS01 credit (+0.61), whose economics hinge on unpublished commission, split and margin assumptions; lowest in WS12 (+0.17), WS09 (+0.19) and WS11 (+0.24), whose authors had already scored harshly.
- **Criteria most over-claimed.** ai: 4.15 → 3.41 (−0.74; lowered on 399 records, raised on 22). fcf: 3.58 → 2.90 (−0.67; lowered on 365, raised on 9); at 18% weight it explains about 30% of the composite gap. Authors gave 148 records fcf ≥5; blind scorers gave 53. Then roic −0.44, scale −0.39, entry −0.36, resilience −0.34, feasibility −0.32, cash −0.23, access −0.18, delegation −0.12.
- **By mechanism.** Largest cuts: manufacturer_rep (−0.78), financing_own_capital (−0.66), brokerage_commission (−0.61), contract_manufacturing_broker (−0.60), referral_fee (−0.58), government_contracting (−0.57). Smallest: consignment and staffing_placement (−0.18), training_certification (−0.22), inspection_testing and geographic_density (−0.27). The mandated-route cluster survived calibration largely intact; the brokerage and procurement clusters did not.
- **Largest single disagreements** were mostly structures scored as if they were businesses: a cooperative purchasing contract (WS08-021, +1.72), a HUBZone overlay (WS08-012, +1.58), AP-automation resale (WS02-025, +1.47). Others were capital-heavy ideas where authors scored the upside (self-storage WS18-022, car wash WS18-021).
- **Gates and verdicts.** Blind scorers added a capital-gate failure to seven records (WS02-016, WS02-022, WS04-005, WS04-006, WS05-018, WS07-029, WS11-006). Of 115 author "advance" verdicts, 56 reached Stage C, 26 stopped at Stage B, 11 merged and 22 were deprioritized, clustered in freight brokerage (WS07-001, -002, -004, -005) and distribution (WS16-001, -003, -011, -024). No author "reject" advanced.
- **Evidence ratings.** Blind and author ratings matched on 494 records; blind was lower on 72 and higher on 64. Blind scorers rated 6 records A/B against 18 by authors, mainly because an A-level legal fact does not prove economics (WS14-005, WS14-006, WS09-005 fell from A to D).

## 5. Evidence quality and limitations of Stage A

**Economics evidence.** E 430 (68.3%), D 119 (18.9%), C 63 (10.0%), B 10 (1.6%), A 8 (1.3%): D and E together cover 87%. The E share ranges from 38% (WS16) and 46% (WS03) to 91% (WS15), 92% (WS05) and 100% (WS17). Stage C is better but still weak (of 67 records: 3 B, 10 C, 26 D, 28 E), partly by design because evidence-adjusted scoring favours better-evidenced ideas.

**Strong evidence mostly kills ideas.** Only 3 of the 18 A/B records reached Stage C (WS14-019, WS18-002, WS18-003); the rest include the hemp, property-tax, unclaimed-property, WOTC and FinCEN rejections. Rules can be verified from a desk; prices cannot.

**Sources.** The 630 sources are 60% A, 13% B, 18% C and 10% D, but A-level sources document statutes, rosters, award data and incumbent filings, not entrant earnings. 74 flag their figures as incumbent, not entrant, economics, and 251 carry no publication date (keyword counts).

**Missing prices.** 392 records (62%) list a price, fee, rate or margin among their unanswered questions (keyword count); 106 records (17%) cite no source. WS05 found no primary price for any service, and WS15 labelled every price E.

**Inaccessible sources.** The shared web-search budget ran out in every workstream (WS15 after 2 searches, WS13 before starting), so most evidence came from direct fetches of known pages.

| Source | Problem | Consequence |
|---|---|---|
| ilga.gov | 503 throughout | Illinois statutes read via FindLaw/Cornell mirrors or snippets |
| chicago.gov, Cook County Assessor | 403 | Chicago municipal code unverified |
| BLS wage data | Blocked | All wage assumptions E |
| Census API | Key required | Bulk files used instead |
| BizBuySell | 403 | No D-level owner-earnings proxies |
| eCFR, fmcsa.dot.gov, dla.mil | Bot blocks / 403 | Mirrors or search extracts used |

Paywalled research and member-only rep-commission tables were not bypassed; bulk SEC EDGAR access was not used, to avoid sending personal details. 134 sources (21%) state that content came from search snippets or that the primary page was blocked (keyword count). FDD Item 19 figures came from a third-party archive and need checking against state copies.

**Conflicts recorded, not resolved.** Examples: the Section 122 rate (10% vs 15%) [C, WS06-S007]; a contrary press report on Section 232 coverage [C, WS03-S011]; the contested ~200k driver-exit estimate [C, WS07-S014, WS07-S015].

**Unknowns.** Founder age, credit and veteran or set-aside status affect broker security, surety bonding, VA set-asides, gaming and customs licensing; all were treated as conditional. With no external contact, supplier access, carrier appointments and customer interest are documented or assumed, never confirmed. Tariffs and federal rules are stated as of 2026-11-28, and several are in litigation.

**Bottom line.** Stage A is a well-sourced map of what is legal, mandated or contested, and a poorly sourced map of what pays. For almost every finalist, the most valuable missing fact is a local price and a new-entrant margin.
