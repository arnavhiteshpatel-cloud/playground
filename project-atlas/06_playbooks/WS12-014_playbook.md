# WS12-014 — Contingency Direct-Hire Desk for Controls & Automation Engineers (Illinois): Stage E Playbook

**Concept:** an employer-paid contingency recruiting desk. It places controls, automation and instrumentation & controls (I&C) engineers (PLC/HMI, SCADA/DCS, robotics, motion control) at Illinois control-system integrators, process plants and engineering firms.

- **Stage E date:** 2026-11-28
- **Status:** finalist, conditional (G7 founder-dependence WARN)
- **Evidence on economics: D.** Fee rate and salary are D, conversion is E. Correction: Stage C/D rated this C. That overstated it, because the fee level and the salaries are public-posting and secondary-survey evidence, not transactions.

**Files**
- **Model:** `08_financial_models/WS12-014_assumptions.json`, `_model.xlsx`, `_results.json`. Rebuilt today under the Stage E standardization rules; `verify_fin_model.py` not run, per protocol.
- **Prospects:** `09_databases/prospects/WS12-014_prospects.csv` (27 employers, all "prospect — not contacted").
- **Tools and partners:** `09_databases/suppliers/WS12-014_suppliers.csv`.
- **New sources:** `06_playbooks/sources_E_WS12-014.jsonl` (E-WS12014-S001…S031).
- **Draft materials:** `06_playbooks/WS12-014_materials.md`. Every item is a DRAFT; nothing has been sent.

---

## Verdict

**GO to validation only.** Spend at most about $600 and 60 days to answer one question: will Illinois controls hiring managers sign a 20% fee agreement with a newcomer who brings a specific, vetted engineer? Do not hire, sign leases or buy data contracts until the gates in §4 are met.

**Why it stays a finalist:**
- **Legal entry is clean and fast.** The Private Employment Agency Act's definition of "employment agency" excludes a recruiting business "compensated solely by any employer" [A, E-WS12014-S001; A, E-WS12014-S002]. The condition is that the candidate is never charged for anything, including résumé help. So there is no IDOL licence, no bond and no state-approved forms.
- **The unit sale is large and almost pure margin.**
  - Illinois controls/I&C postings carry pay bands of $72k–$157k. Engineer-level midpoints cluster around $95k–$140k (median ≈ $107k across 11 postings) [D, E-WS12014-S025, S027, S028; DG-S034].
  - At 20%, one placement is a ≈$21k fee [D, C9-S025].
  - Incumbent perm gross margin is 99.8% [A, E-WS12014-S009].
- **Capital at risk is small.** Base-case peak funding is **$12,836**, so start capital is **$12,900**. It is well under the founder's limit even in the conservative case (**$68,241** with the standardized draw; **$21,559** without it).
- **Demand is visible today.** Employers' own career systems show live roles, several open for months. Examples: Ingredion's Bedford Park Controls Systems Engineer, posted 2026-06-08; Abbott's warehouse controls role, posted 2026-07-20 [D, E-WS12014-S025]. Manufacturing job openings are recovering from a 2025 trough [C, E-WS12014-S014].

**Why it is not the holding-company core:**
- **It is the founder's labour.** In the base case the desk is still founder plus one recruiter at year 5. The second recruiter is never triggered, so the G7 warning stands.
- **It is the most cyclical line in staffing:**
  - Robert Half's permanent-placement revenue fell **57% in 2009** [A, E-WS12014-S011].
  - It fell **21.7% in 2023**, on 24.1% fewer placements [A, E-WS12014-S009].
  - Manufacturing job openings fell from 1,025k to 376k between April 2022 and April 2025 [C, E-WS12014-S014].
- **AI is lowering the value of plain sourcing.** LinkedIn's agentic Hiring Assistant went global in English in September 2025 [B, E-WS12014-S021]. The defensible service is persuasion and technical vetting of scarce, experienced engineers, not finding names.
- **Transfer value is low.** Valuation in the model is 2.0× operating profit (base), against a 2.38× median for sold service businesses [D, E-WS05007-S007].

**Model headline (rebuilt; quoted from `_results.json`):**

| | Base | Conservative | Optimistic |
|---|---|---|---|
| Year-3 operating profit | **$170,012** | **$41,471** | $385,952 |
| Year-5 operating profit | **$259,002** | **$55,944** | $923,616 |
| Peak funding need | **$12,836** | **$68,241** | $10,617 |

Operating profit is before owner pay. Peak funding is after the standardized $4,000/month draw from month 13. The optimistic case is a ceiling, not a plan (§7).

---

## 1. Business explanation (for someone new to recruiting)

**What it is.** A company has a hard-to-fill engineering job: for example, a controls engineer who programs and commissions PLC-based machines at a food plant. Its own HR team posts the job, and nobody suitable applies for months. The best candidates already have jobs and are not looking.

A contingency recruiter does the rest:
1. Finds those people.
2. Persuades a few to consider the move.
3. Checks that they can really do the work.
4. Presents two or three to the hiring manager.
5. Manages interviews, the offer and the counter-offer from the current employer.

The employer pays **only if someone is hired**. The fee is a percentage of the new hire's first-year base salary. Robert Half describes perm fees as paid only by the employer and "generally a percentage of the new employee's annual compensation" [A, WS12-S008].

**Who pays and why:**
- **Who:** the hiring company.
- **Why:**
  - An empty controls seat delays projects and plant upgrades.
  - Job boards and in-house recruiters have failed.
  - Speed matters.
- **Who does not pay:** the candidate. Charging the candidate anything would void the Illinois licensing exclusion [A, E-WS12014-S001].

**How it earns.** The fee, typically 20% [D, C9-S025], is invoiced when the engineer starts. It is paid about 30–45 days later. Kforce recognises direct-hire revenue once the candidate has accepted, resigned and is due to start [A, E-WS12014-S012]. If the hire leaves within the guarantee period (usually 30–90 days [D, E-WS12014-S024]; Kforce: "typically 90 days or less" [A, E-WS12014-S012]), the recruiter must find a replacement or refund part of the fee.

**Cost structure.**
- There is almost no cost of goods: Robert Half's perm gross margin is 99.8% [A, E-WS12014-S009].
- The real cost is recruiter time. At Robert Half the perm segment's SG&A was 96.9% of revenue in 2025 [A, E-WS12014-S010]. At PageGroup, operating profit was only 2.7% of gross profit in 2025 [B, E-WS12014-S013].
- **For an owner-producer, the margin is the owner's own labour.** That is why it is lucrative for the individual and hard to scale profitably.

**Why it is attractive for this founder:**
1. Near-zero capital.
2. A licence exclusion.
3. A large ticket, often $17–31k per placement.
4. A wedge a technical founder can use. Most recruiters cannot tell a strong Rockwell/Siemens commissioning engineer from a résumé full of keywords. A founder with a tech/research background can learn to run a credible technical screen.

**Why it is dangerous:**
1. Income is lumpy and contingent. Weeks of work can earn $0 when a client freezes hiring or fills internally.
2. It is strongly cyclical.
3. It is personal. Clients and candidates follow the recruiter, not the firm.

---

## 2. Commercial entry

### 2.1 Initial niche (confirmed in Stage E)
**Roles:** controls, automation and I&C engineers at base salaries of about $90k–$160k. The second tier is adjacent electrical and test engineers. Avoid technician roles ($72–99k bands, e.g. Baxter's Automation Technician [D, E-WS12014-S025]). Their fees are lower and in-house teams fill them more easily.

**Customers, in order of access:**

| Order | Customer type | Examples / rationale |
|---|---|---|
| 1 | Control-system integrators and automation OEMs | Controls labour is what they sell, they hire continuously, and owners or engineering managers are reachable |
| 2 | Mid-size process plants | Plant engineering managers |
| 3 | Engineering consultancies | Sargent & Lundy, Baxter & Woodman, CDM Smith |
| — | Large corporates | Route through agency portals (Abbott runs a separate Workday "Agency" site [D, DG-S026]). Some tell agencies outright not to contact hiring managers: Chamberlain's posting says "Staffing agencies, headhunters, recruiters… please do not contact our hiring managers directly" [D, E-WS12014-S026]. **Treat these as year-2 targets via vendor onboarding, not first clients.** |

**Geography:**
- **Primary:** Chicago metro (Cook, DuPage, Lake, Kane, McHenry, Will).
- **Secondary:** the Rockford, Peoria/Morton, Bloomington-Normal and Decatur corridor.
- **Later:** Wisconsin, Indiana and Iowa integrators. Remote work is possible, but plant visits build trust.

### 2.2 Named suppliers, tools and partners (see suppliers CSV)
- **Candidate access:**
  - LinkedIn Recruiter Lite: about $170/month with 30 InMails. LinkedIn does not publish the price; it comes from third-party pages [D, E-WS12014-S022].
  - Full LinkedIn Recruiter is priced by sales only [D, DG-S045].
- **CRM/ATS:**
  - Recruit CRM: $95/$135/$215 per user/month [B, DG-S040].
  - Loxo: from $149/user/month (annual) [B, DG-S041].
  - Crelate: $85–$299 [B, DG-S042].
- **Split network (optional):** Top Echelon at $150/month plus $350 startup (monthly), or $135/month (annual) [B, DG-S043]. Its split terms and per-placement network fee are not published (MISSING).
- **Marketplace (optional, for learning reps):** Paraform shows an 80% success-fee split to recruiters [D, DG-S044]. Its role mix skews to tech and startups.
- **Professional services:**
  - An Illinois employment attorney to review the fee agreement (≈$1,500 one-time, E; no quote).
  - An insurance broker for E&O/GL (premium MISSING; modeled at $175/month, E).
- **Regulator:** IDOL, licensing exclusion [A, E-WS12014-S002].

### 2.3 Top 15 named prospects (all "prospect — not contacted"; 27 in CSV)
Ranked by likely access and fee value. Evidence is employer career systems accessed 2026-11-28 [D].

| # | Employer (location) | Why |
|---|---|---|
| 1 | Wunderlich-Malec (Addison) | Integrator with 100+ engineering openings company-wide, including multiple Controls Engineer roles [D, DG-S035]. An Addison posting surfaced on Illinois JobLink [D, DG-S034], but no Illinois requisition was visible on its own board on 2026-11-28 [D, DG-S035] |
| 2 | Barry-Wehmiller Design Group (Oak Brook) | SCADA engineer posted 2026-11-02 at $100–130k [D, E-WS12014-S025]; 20+ controls roles across offices [D, DG-S022] |
| 3 | Concentric Integration (Crystal Lake HQ) | Growing water-SCADA integrator; acquired P.J. Kortens [D, DG-S039]. Municipal water is less cyclical |
| 4 | WESA Automation (Elgin) | Small integrator and panel shop recruiting PLC/HMI and field-service staff [D, DG-S036]; owner-level access |
| 5 | Daifuku Intralogistics / Wynright (Bolingbrook) | Controls Engineer III, travel-heavy commissioning work, hard to fill [D, DG-S034/S038] |
| 6 | Formic Technologies (Chicago/Bolingbrook) | Controls & Automation Engineer $120–145k; 72 open roles [D, E-WS12014-S027] |
| 7 | Yaskawa America (Waukegan) | Several concurrent motion-control roles [D, DG-S023] |
| 8 | Medline (Mundelein) | Controls Engineer $85–128k, posted 2026-10-23 [D, E-WS12014-S025] |
| 9 | Ingredion (Bedford Park) | Controls Systems Engineer $84.4–112.5k, posted 2026-06-08, open about 5.7 months [D, E-WS12014-S025] |
| 10 | Primient (Decatur) | Sr. Engineer, Electrical $123.5–154.4k, plus a second 30+-day role [D, E-WS12014-S025; DG-S029] |
| 11 | Rivian (Normal) | Staff/Senior Automation & Controls at $125.8–157.2k [D, DG-S034] |
| 12 | Baxter & Woodman (Crystal Lake) | Consulting engineers with SCADA/automation disciplines [D, DG-S037] |
| 13 | CDM Smith (Lisle) | PLC/HMI process-control role [D, DG-S034] |
| 14 | Woodward (Loves Park) | Test/electrical engineers $70–115k in the Rockford corridor [D, E-WS12014-S025] |
| 15 | Sargent & Lundy (Chicago) | 20 I&C/automation listings with bands of $74–129k [D, E-WS12014-S028]. The largest repeat need, but likely vendor-gated, so approach through discipline managers only after a first placement elsewhere |

**Demoted:**
- **Vendor-gated or explicit no-contact:** Abbott, Chamberlain, AbbVie, Caterpillar, Mars Wrigley, Ameren.
- **Technician tier:** Novolex, Mondelez, Baxter.
- **Weak fit or possibly filled:** Littelfuse, Huntsman.

### 2.4 Named competitors
| Competitor | Presence / evidence |
|---|---|
| Actalent / Aerotek (Allegis) | Post Illinois controls roles on the state job bank [D, DG-S034]; volume and contract-to-hire |
| Robert Half | Incumbent perm business, $440M revenue in 2025 [A, E-WS12014-S010] |
| Kforce | Direct Hire $25.7M [A, E-WS12014-S012] |
| Illinois boutiques | 356 placement-agency and 329 executive-search establishments (2023) [C, C9-S007]; controls specialists not enumerated (MISSING) |
| Marketplaces | Paraform [D, C9-S024] |
| In-house talent acquisition | Now armed with LinkedIn Hiring Assistant [B, E-WS12014-S021]. **This is the biggest competitor** |

### 2.5 Positioning
"Controls engineers, vetted by someone who can read your ladder logic."

The offer:
- Three or fewer candidates per role, each with a written technical-screen summary.
- Clear pay-band compliance.
- A 90-day replacement guarantee.

It does not offer volume, brand or lowest price.

### 2.6 Pricing
| Item | Terms | Evidence |
|---|---|---|
| Standard fee | 20% of first-year base | Most common North American fee [D, C9-S025]; Top Echelon engineering placements averaged 23% in 2018 [D, E-WS12014-S018] |
| Senior I&C / relocation searches | 22–25% | Top Echelon's largest 2025 manufacturing splits were 25% fees [D, E-WS12014-S020] |
| Introductory fee | 18% on the first role per client | — |
| Never offer | Below 18% | Trade exclusivity for price instead (a two-role exclusive at 18%) |
| Guarantee | 90-day replacement, no cash refund | — |
| Candidate ownership | 12 months | — |
| Invoicing | On start, net-30 | — |

### 2.7 Sales and acquisition strategy
"Candidate-led marketing":
1. First recruit a real, consenting, strong engineer.
2. Present an anonymised profile to hiring managers who have a matching open role, found from public postings.
3. The call is about a specific person, not a pitch for the agency.

Supporting channels:
- **ISA Chicago-section meetings** (cost MISSING).
- **Referrals** from placed engineers.
- **Repeat roles** at the first clients.

**No paid lead generation.** CAC is founder time: about 15–20 hours a week of business development within a 45–50-hour week.

---

## 3. Transaction economics

Rebuilt transactions from the assumptions file (fee and salary D, reserve E):

| Transaction | Revenue | Direct costs | Contribution | Cash timing / note |
|---|---|---|---|---|
| **A. Controls engineer, $105k × 20%** (e.g. a Medline-type $85–128k band) | $21,000 | Fallout/discount reserve 15% $3,150; job ads $300; client visit $120; reference checks by founder $0 | **$17,430** | Invoice on start; paid around day 40 after start; 90-day guarantee |
| **B. Senior I&C engineer, $140k × 22%** (e.g. Primient $123.5–154.4k, Formic $120–145k) | $30,800 | Reserve $4,620; ads + InMail $450 | **$25,730** | Same |
| **C. Controls technician, $72k × 18%, split 50/50 through a network** | $12,960 | Partner share $6,480; reserve $972; network allocation $150 | **$5,358** | Same, plus partner settlement. **A capacity trap** |
| **D. Fallout inside the 90-day guarantee** (replacement, no refund) | $0 | Re-advertising $300 | **−$300**, plus 4–6 weeks of desk time | — |
| **E. Search cancelled after 6 weeks** (freeze or internal hire) | $0 | Ads/InMail $300 | **−$300**, plus about 60 hours of time | PageGroup's biggest 2025 challenge was conversion of interviews to accepted offers [B, E-WS12014-S013] |

**Cash timing.** The earliest realistic sequence is:
1. Outreach.
2. Signed fee agreement: weeks 1–8.
3. Submittals and interviews: 4–10 weeks.
4. Offer, then resignation and notice: 2–4 weeks.
5. Start.
6. Cash about 40 days after start.

So **first cash lands between months 5 and 10 (E)**. The model smooths this: base cumulative revenue reaches one full fee in month 11. Reality is lumpier: $0 for months, then a $17–21k receipt.

**Failure risks per transaction:**
- **Counter-offer:** the candidate accepts, then stays.
- **Fee dispute:** "we already had that résumé".
- **Late start or no-start.**
- **Guarantee fallout.**
- **Bad debt** at small clients.

Mitigations:
- Written fee agreement before any submittal.
- Time-stamped submittals with candidate consent to each role.
- Candidate-ownership clause.
- Invoice on start.

**Repeat potential.** The base case assumes an active client yields 0.45 further placements a year, with 5% monthly churn, or about 20 months of active life (E). Integrators with continuous hiring can repeat far more often. Large plants hire controls engineers rarely.

---

## 4. Validation

### 4.1 Minimum viable commercial offering
The founder offers one contingency search on one live controls role, and has:
- one signed fee agreement (attorney-reviewed DRAFT in materials);
- one or two real candidates who consented to be presented;
- a one-page offer sheet;
- a technical-screen template.

**No LLC is needed to hold validation conversations.** Form the LLC (Illinois Articles of Organization fee ≈ $150; confirm with the Secretary of State, E) before signing the first fee agreement.

### 4.2 Experiments, ordered by information value per dollar
| # | Test | Cost | Duration | Success | Kill |
|---|---|---|---|---|---|
| 1 | **Role map refresh.** Rerun the public ATS queries weekly (scripts from Stage D) | $0 | 4 weeks | ≥40 engineer-level controls/I&C roles at ≥20 Illinois employers; ≥30% open 30+ days; ≥10 at Tier A/B (non-gated) employers | <15 roles, or most at gated large employers |
| 2 | **Candidate supply.** 60 personalised approaches to Illinois controls engineers (LinkedIn Recruiter Lite month 1; 30 InMails plus connection requests and referrals) | $0–$170 | 3 weeks | ≥20% reply; ≥5 open to a move at ≥$100k; ≥2 willing to be presented now | <8% reply, or nobody movable at ≥$95k |
| 3 | **Fee-agreement test (decisive).** 30 hiring-manager conversations at Tier A/B employers, each about a specific anonymised candidate whose fit to a posted role is evidenced | $0–$170 + mileage ≈$100 | 60 days | ≥5 signed agreements at ≥18% | <2 signed, or all demand ≤15% or "portal only" |
| 4 | **Interview conversion.** Submittals from test 3 | Founder time | Months 2–5 | ≥1 candidate in a final-round interview by month 4; ≥1 accepted offer by month 6 | No final rounds after 8 submittals |
| 5 | **First collected fee** | Tools ≈ $940/month + $300 ads | By month 10 | ≥1 fee ≥$15k collected | None by month 10: stop before any hire |
| 6 | **Split-network probe (optional).** Top Echelon | $350 + $150/month | 60 days | ≥3 relevant controls/engineering job orders available | <3 |

**Total validation budget:** about $600 through day 60. That covers Recruiter Lite for two months ($340), mileage and coffee ($100), and an ISA meeting (cost MISSING). The attorney review (≈$1,500) is the first spend after the gate, not before.

### 4.3 Supplier and partner qualification steps
- **LinkedIn:**
  - Confirm the Recruiter Lite price and InMail rules at checkout. These are third-party figures [D, E-WS12014-S022].
  - Read the user agreement. **No scraping**; use manual sourcing.
- **CRM:** trial Recruit CRM or Loxo and check Chrome-extension sourcing, sequencing and data credits [B, DG-S040/S041].
- **Insurance:** ask a broker for E&O/GL premiums for a $0–300k-revenue perm desk. Many larger clients require certificates (E).
- **Attorney:** review the fee agreement, candidate-ownership, guarantee and collection clauses, plus Illinois compliance (§5.4).
- **Top Echelon:** request the split terms and the network fee per placement (MISSING) before joining.

### 4.4 Testable assumptions (model drivers)
| Driver | Base | Test that measures it |
|---|---|---|
| Founder conversations about a live role per month (at full pace) | 9 | Test 3 activity log |
| Conversation → signed agreement | 30% | Test 3 |
| Agreement → placement (fill ratio) | 20% | Tests 4–5 |
| Realized first fee | $17,850 ($105k × 20% × 85%) | Signed fee %, offer salary, fallouts |
| Founder ramp to full pace | 12 months | Monthly trend in submittals and interviews |
| Repeat placements per active client | 0.45/yr | Second job order from first clients within 6 months |
| DSO | 40 days | First invoices |

### 4.5 Conditions to invest more (each step in §8)
Move past about $2k only when all of these are true:
- ≥5 signed fee agreements at ≥18%;
- ≥2 candidates in active interview processes;
- the founder can personally run a credible technical screen, judged by a placed engineer or hiring manager.

Hire recruiter #1 only when **trailing 6-month revenue is ≥$20k/month** and the founder has ≥8 open searches.

### 4.6 Conditions to abandon or pivot
| Trigger | Response |
|---|---|
| Test 3 fails | Abandon |
| Managers say they only buy through portals or MSPs | Pivot: apply as a vendor to 2–3 large employers and treat that as a 6–12-month credibility build. Or abandon |
| Candidates are plentiful but clients won't pay 18–20% | Pivot to marketplace recruiting (Paraform-type, 80% split [D, DG-S044]) for income only. **It is not a business asset** |
| Engineer-level demand collapses (Tier A/B postings down >40% quarter on quarter) | Pause; keep candidate relationships warm |
| Founder dislikes cold calling after 60 days | Abandon. It is the job |

---

## 5. Operations

### 5.1 Lead-to-cash workflow and function classification
| Step | Function | Classification |
|---|---|---|
| 1 | Role intelligence: weekly ATS scan of Illinois controls postings | **Automatable** (scripts; ≈$0) |
| 2 | Target list and hiring-manager identification | **AI-assisted** (drafts, org mapping); human verifies |
| 3 | Candidate sourcing: LinkedIn, referrals, ISA, alumni of integrators | **AI-assisted** search strings and outreach drafts; **human** relationships |
| 4 | Candidate first call: motivation, constraints, pay *expectations*, never salary history [A, E-WS12014-S003] | **Human** |
| 5 | Technical screen: PLC/SCADA scenario interview, project review | **Human, founder's wedge.** Not automatable |
| 6 | Hiring-manager call with an anonymised profile | **Human** |
| 7 | Fee agreement signature | **Human**; template is **professional-dependent** (attorney) |
| 8 | Intake: role scorecard, pay band, interview steps | **AI-assisted** notes; human |
| 9 | Submittal: consent-to-represent per role, redacted résumé, screen summary | **AI-assisted** formatting; human judgement |
| 10 | Interview coordination | **Automatable/AI-assisted** (scheduling); coordinator later |
| 11 | Offer, counter-offer, resignation coaching | **Human. Not automatable** |
| 12 | Start, invoice, 30/60/90-day check-ins | **Automatable** (invoicing) plus **human** check-ins |
| 13 | Collection and dispute | **Human**; **professional-dependent** if escalated |

### 5.2 Fulfilment, support, QA and exceptions
**Quality assurance:**
- Every submittal includes a one-page technical screen with scored scenarios.
- The founder never submits without a live conversation and written consent.

**Exceptions:**
- **Duplicate résumé:** submittal time-stamps and the consent log decide ownership.
- **Counter-offer:** pre-close questions on day 1.
- **Freeze:** cap time on any search without a hiring-manager interview at 3 weeks.
- **Fallout:** begin the replacement search the same week.

### 5.3 Software stack and monthly prices (model overhead, base)
| Item | $/month | Basis |
|---|---|---|
| Recruit CRM (Pro) | $135 | [B, DG-S040] |
| LinkedIn Recruiter Lite (founder) | $170 | [D, E-WS12014-S022] |
| Contact data / sequencing (Apollo-type) | $100 | E (pricing page unreadable) |
| AI assistant + transcription | $60 | E |
| E&O + GL insurance | $175 | E, MISSING quote |
| Legal + accounting | $200 | E |
| Phone, video, home office | $100 | E |
| Job ads (fixed marketing) | $300 | E (Indeed/ZipRecruiter pages blocked) |

**Total ≈ $1,240/month.** One-time costs are $2,500 for laptop, headset and website, plus $1,500 for the attorney and the LLC.

Each hired recruiter's tool seats (≈$400/month) are included in their $6,900/month all-in cost.

### 5.4 Legal requirements (Illinois/Chicago; verified where marked A)
1. **No private-employment-agency licence while paid solely by employers:**
   - The 225 ILCS 515/1.1 exclusion requires that the individual is never charged "directly or indirectly", including "for preparation of any resume" or any "other personal service" [A, E-WS12014-S001]. **Never sell résumé writing, coaching or career services to candidates in this entity.**
   - The exclusion does not cover theatrical or domestic-service placement.
   - If the business ever charges candidates, the full licence applies: annual, $250–500 fee, $5,000 bond, IDOL-approved forms [A, WS12-S015]. IDOL can impose criminal sanctions [A, E-WS12014-S002].
   - Statute text was read from a mirror because ilga.gov returned 503. **Have counsel confirm.**
2. **Salary-history ban.** It is unlawful for an employer *or employment agency* to screen on, or require, wage or salary history [A, E-WS12014-S003]. Scripts ask for *expectations* only. Correction: Stage D did not flag this.
3. **Pay-scale disclosure:**
   - Employers with 15+ employees must include pay scale and benefits in postings.
   - A third party posting for them "is liable for failure to include" them, unless the employer did not provide them.
   - An employment agency must disclose the pay scale to an applicant on request before an offer [A, E-WS12014-S003].
   - Correction: Stage D marked this "unverified (E)". It is now verified from statute text.
4. **Criminal-history timing.** No inquiry until the candidate is selected for interview, or after a conditional offer if there is no interview [A, E-WS12014-S004]. Leave background checks to the employer's own consumer-reporting agency. Whether desk-run reference checks trigger the federal FCRA is a counsel question (E).
5. **AI rules:**
   - Do not use AI-analysed video interviews. The AI Video Interview Act requires notice, an explanation and consent [A, E-WS12014-S005].
   - The Illinois Human Rights Act AI amendment (P.A. 103-0804, effective 2026-01-01) bars AI with discriminatory effect in recruitment and hiring, bars zip-code proxies, and requires notice [C, E-WS12014-S007]. IDHR's draft rules were proposed in May 2026 and withdrawn on 2 June 2026; their status since is unconfirmed [D, E-WS12014-S008].
   - **Use AI for drafting and notes, never for ranking or rejecting candidates**, and disclose the AI tools used to clients.
6. **Anti-discrimination.** The Illinois Human Rights Act covers employment agencies directly [A, E-WS12014-S031]. Federal Title VII and the ADEA also apply (E, standard).
7. **Hiring recruiters later:**
   - Non-competes are void below $75k of earnings ($80k from 2027-01-01).
   - Non-solicits are void below $45k ($47,500 from 2027-01-01) [A, E-WS12014-S006].
   - A $50k-base junior is therefore protected mainly by a non-solicit, confidentiality and CRM ownership.
   - Illinois paid-leave rules apply. They are built into the $6,900 cost (E).
8. **Chicago.** If the business operates within city limits, including from home, a City business license is required [D, E-WS12014-S029]. Confirm the type and fee with BACP.
9. **Outreach law.** Follow CAN-SPAM for cold email. Make manual calls only, with no autodialer or text blasts, given TCPA risk (E; confirm).

### 5.5 Financial administration
- Separate business bank account.
- Invoice in the CRM or accounting tool on the start date.
- A 30/60/90 collection cadence.
- A fallout reserve held in cash: 15% of each fee until the guarantee expires.
- Quarterly estimated taxes (the model uses a 30% blended rate).
- Recruiter commissions paid **on collection, after the guarantee period**. This protects cash and limits clawbacks.

### 5.6 After December 2026: AI cost and fallback
At ordinary prices the AI work (search strings, outreach drafts, interview notes, redaction, market maps) costs about $60/month in the model.

The ATS-scan scripts written during research run on plain Python, with no AI dependency.

Stress test: AI/software cost ×3 cuts base year-3 operating profit from $170,012 to **$158,172** [model]. **The business does not depend on heavy AI. It depends on the founder's phone time.**

---

## 6. Growth

### 6.1 First 10 customers
1. **Clients 1–3:** Tier A integrators and mid-size plants from §2.3, won through candidate-led calls.
2. **Clients 4–7:**
   - repeat roles at those clients (integrators often have several controls openings);
   - referrals from the first placed engineers' former colleagues;
   - Rockford and central-Illinois plants (Woodward, Primient, Rivian).
3. **Clients 8–10:** engineering consultancies, once a track record exists.

In the base model the desk has about 6 active clients at month 24 and about 10 at month 36.

### 6.2 First 100 customers
- **Not plausible for the founder's desk alone.** Base has 19.3 active clients at the end of year 5.
- Reaching 50–100 needs 3–5 producing recruiters plus Wisconsin, Indiana and Iowa integrators. That is the optimistic case's 51.6 active clients at the end of year 5.

### 6.3 Hiring sequence (model triggers)
| Hire | Trigger | All-in cost | Productivity assumption | Base hires in month | Optimistic month |
|---|---|---|---|---|---|
| Recruiter #1 (full desk) | Prior-month revenue >$20k | $6,900/month | 6-month ramp, then 0.35 new paying clients/month plus their repeats ≈ $130k/yr realized (E) | **35** | 14 |
| Part-time coordinator | Revenue >$35k | $2,600/month | Scheduling, CRM, invoicing | 50 | 20 |
| Recruiter #2 | Revenue >$40k | $6,900/month | As above | **never (≤60 mo)** | 23 |
| Recruiter #3 / team lead | Revenue >$60k | $7,500/month | Experienced hire who can run the desk | never | 30 |

**Desk economics of one hire (E):**
- **Year 1 of tenure:** about 6 months at $6,900 before meaningful production, then a ramp. Expect a net loss of $35–45k.
- **Year 2 of tenure:** ~$130k realized revenue against ~$83k cost leaves **~$45–50k contribution** before founder coaching time.
- **Wash-out:** assume 1 in 2 hires does not make it (E). The expected investment per *successful* recruiter is therefore $70–90k. That is why the long-term incremental ROIC is set at 60% (base) and 35% (conservative).
- **Benchmarks:**
  - PageGroup's average fee earner generated £148.9k of gross profit in 2025 (≈$195k at about $1.31/£, analyst conversion) [B, E-WS12014-S013].
  - Top-10 Top Echelon split-network recruiters produced $99k–$524k of network cash-in in 2025 [D, E-WS12014-S019].
  - A $130k boutique junior is below the mature-firm average, which is appropriate.

### 6.4 Capacity limits
One full-desk producer handles about 8–12 open searches and roughly 12–20 placements a year (E). Engine caveat: repeat placements consume no modeled labour, so per-producer revenue was checked against benchmarks:

| Scenario | Year 3 revenue per producer | Year 5 revenue per producer | Benchmark position |
|---|---|---|---|
| Base | ≈ $195k | ≈ $227k | At to ~15% above PageGroup's average fee earner. **Optimistic for a newcomer; see §11** |
| Optimistic | — | ≈ $356k | Near the top of public benchmarks. Correction: the Stage D optimistic case implied ≈$519k per producer, above any public benchmark, and was cut |

### 6.5 Geographic expansion
Order: Illinois first, then Wisconsin and Indiana integrators (the same OEM and integrator ecosystems), then Iowa and Missouri process plants. Remote searches are feasible, but in-person plant visits are the trust builder.

### 6.6 Adjacent products and services
| Adjacency | Economics | Notes |
|---|---|---|
| **Contract or contract-to-hire controls engineers** (WS12-005/006 logic) | Recurring revenue, but needs payroll float, workers' comp and MSP access. Kforce flags MSP fees of 1–4% of revenue and margin compression [A, E-WS12014-S012] | Year 3+ only |
| **Retained or engaged search** for senior I&C, nuclear and DCS roles | Part-paid upfront, better cash | Requires a reputation |
| **RPO-lite subscription** for integrators | Monthly fee for ongoing sourcing | Recurring, but service-heavy |
| Anything sold **to candidates** | — | **Prohibited** in this entity: it voids the licence exclusion [A, E-WS12014-S001] |

### 6.7 Vertical integration
None worth capital. Assessment centres, training or a controls-engineering bootcamp would be separate businesses with separate licensing questions (e.g., private schools). The return logic is weak.

### 6.8 Management delegation
A manager can run day-to-day only when two things hold:
- ≥3 producing recruiters exist, one of them an experienced team lead;
- the CRM, not the founder's memory, holds client and candidate relationships.

**In the base case that never happens within 5 years**, because recruiter #2 is never triggered. In the optimistic case it happens around month 30 (recruiter #3).

Even then the business is a "team of producers". PageGroup describes its model as team-based with profit share [B, E-WS12014-S013].

### 6.9 Reinvestment slots
1. Recruiter hires: the main slot, at about 60% incremental ROIC (E).
2. Vendor onboarding at gated large employers: insurance certificates, MSAs.
3. Contract-staffing working capital, later.

---

## 7. Financial analysis (rebuilt model; figures quoted from `_results.json`)

**Standardized settings:**
- $4,000/month owner draw from month 13 in all scenarios.
- 30% tax.
- Start capital $12,900: the smallest round amount keeping the base cash balance ≥0. Base minimum cash is **$64.38**.

**Changes from Stage D (corrections):**

| Driver | Stage D | Stage E | Reason |
|---|---|---|---|
| Founder ramp (cons/base/opt) | 12/9/6 | **18/12/8** | In-firm benchmarks assume existing job orders [D, E-WS12014-S023] |
| Optimistic leads per month | 10 | **9** | Benchmark cap |
| Optimistic repeat revenue | $950 | **$800** | Benchmark cap |
| Optimistic churn | 4% | **4.5%** | Benchmark cap |
| Optimistic referrals | 2.5 | **2** | Benchmark cap |
| Staffing | One junior | **Up to 3 full-desk recruiters at $6,900–7,500/month all-in, plus a coordinator** | — |
| Recruiter Lite | MISSING | **$170 (D)** | Third-party pages |
| Background-check line | Included | **Removed** | Employer runs checks |
| One-time legal/LLC | — | **$1,500 added** | — |
| Long-term drivers | Defaults | **Set with evidence** (below) | — |

**Long-term drivers set:**

| Driver | Cons | Base | Opt | Evidence |
|---|---|---|---|---|
| Year-6 growth | 1% | 5% | 8% | SIA +2.4% / +2.2% [C, E-WS12014-S030] |
| Growth decay | 0.70 | 0.85 | 0.90 | E |
| Incremental ROIC | 35% | 60% | 90% | E |
| Maintenance capex | 3% | 2% | 2% | E |
| Reserve months | 4 | 3 | 2 | RH perm −57% (2009) [A, E-WS12014-S011] |
| EV multiple | 1.0× | 2.0× | 2.75× | [D, E-WS05007-S007] |

### 7.1 Launch capital and working capital
| | Base | Conservative | Optimistic |
|---|---|---|---|
| Peak funding need (with draw) | **$12,836** | **$68,241** | $10,617 |
| Peak funding (no draw) | $12,836 | $21,559 | $10,617 |
| Breakeven month (first month op > 0) | 7 | 14 | 5 |
| Payback month (cumulative retained back to ≥0) | 18 | never within 60 months | 10 |

- **Working capital** is receivables only: DSO 40 days in the base case. Year-1 working-capital build is $8,758 and year 2 adds $12,241.
- **Not in the model: the founder's own living costs for months 1–12**, before the draw starts. This is the real "capital" of this business.

### 7.2 24-month monthly view (base; engine mirror identical to the XLSX formulas)
| Month | Revenue | Operating profit | Cash balance |
|---|---|---|---|
| 1–5 | $0 each | −$1,240 each | 7,660 → 2,700 |
| 6 | 833 | −516 | 1,102 |
| 7 | 1,712 | 249 | 210 |
| 8 | 2,635 | 1,053 | **64 (minimum)** |
| 9 | 3,600 | 1,896 | 706 |
| 10 | 4,607 | 2,775 | 2,173 |
| 11 | 5,653 | 3,690 | 3,618 |
| 12 | 6,739 | 4,641 | 5,455 |
| 13 (draw starts) | 8,098 | 5,803 | 4,950 |
| 14 | 9,293 | 6,851 | 5,392 |
| 15 | 10,525 | 7,932 | 6,542 |
| 16 | 11,792 | 9,044 | 8,425 |
| 17 | 13,093 | 10,187 | 11,063 |
| 18 | 13,569 | 10,613 | 15,071 |
| 19 | 14,031 | 11,027 | 19,387 |
| 20 | 14,479 | 11,428 | 24,002 |
| 21 | 14,914 | 11,817 | 28,907 |
| 22 | 15,336 | 12,195 | 34,093 |
| 23 | 15,745 | 12,561 | 39,552 |
| 24 | 16,141 | 12,916 | 45,275 |

The monthly revenue is an expected value of fractional placements. **Real months will be $0 or $17–31k.** The cash buffer must therefore cover 2–3 consecutive zero months even in year 2. That is the reason the reserve was raised to 3 months (base).

### 7.3 Five-year annual summary
| Year | Base revenue | Base op profit | Base FCF | Cons op profit | Opt op profit |
|---|---|---|---|---|---|
| 1 | $25,780 | $7,589 | −$7,445 | −$14,004 | $59,458 |
| 2 | $157,016 | $122,373 | $87,820 | $15,903 | $211,171 |
| 3 | $227,264 | **$170,012** | $127,501 | **$41,471** | $385,952 |
| 4 | $342,149 | $195,267 | $134,093 | $50,547 | $707,656 |
| 5 | $453,515 | **$259,002** | $187,421 | **$55,944** | $923,616 |

**Drivers:**
- **Base:**
  - The year-2 jump is the founder reaching full pace: 0.54 new paying clients/month plus repeats.
  - Year 3 is ≈12 placements.
  - The year-4 growth is muted by recruiter #1's ramp from month 35.
- **Conservative:** never hires and stays a part-time-income desk.
- **Optimistic:** a 4-producer boutique.

### 7.4 Sensitivity (tornado, base, ±25%, year-3 operating profit)
| Driver | −25% | +25% |
|---|---|---|
| Founder conversations per month | $134,576 | $187,624 |
| Fill ratio (agreement → placement) | $134,576 | $187,624 |
| Gross margin | $153,597 | $186,427 |
| First-fee size | $149,464 | $180,153 |

- **Founder activity and fill ratio dominate.**
- **A hiring-trigger artefact:** lower churn, more referrals or higher repeat revenue *lower* year-3 profit. Monthly churn −25% gives $159,395. The extra revenue triggers recruiter #1 earlier, and that ramp cost falls in year 3. This is realistic. Each hire depresses profit for about 6–9 months.

### 7.5 Stress tests (base; year-3 / year-5 operating profit; peak funding)
| Stress | Year 3 | Year 5 | Peak |
|---|---|---|---|
| Base | $170,012 | $259,002 | $12,836 |
| Win rate −40% | $104,530 | $149,818 | $14,852 |
| Founder capacity −40% | $104,530 | $149,818 | $14,852 |
| Recession (new −30%, churn ×1.5) | $104,462 | $127,405 | $13,159 |
| Growth twice as slow | **$62,319** | $94,228 | **$46,606** |
| Sales cycle doubles | $169,478 | $235,862 | $25,967 |
| Hires 30% sooner | $125,393 | $326,813 | $12,836 |
| Competitor response | $160,463 | $145,004 | $12,841 |
| Labour +20% | $167,084 | $233,926 | $12,836 |
| Customers pay 30 days later | $170,012 | $259,002 | $16,882 |

**Supplementary runs** (same engine, base drivers, **not in `_results.json`**). The built-in recession is milder than the record:

| Analogue | Overrides | Year 3 | Year 5 | Peak |
|---|---|---|---|---|
| 2023-type downturn | New ×0.75, churn ×1.3 | $118,580 | $150,556 | $13,105 |
| 2009-type collapse | New ×0.45, churn ×2, held for 5 years | **$53,513** | $61,058 | $25,098 |

Applied to the whole horizon, the 2009 analogue overstates its length, since that decline lasted roughly a year. Its depth is evidenced: RH perm revenue fell 57% in 2009 [A, E-WS12014-S011], and manufacturing openings fell 63% from peak to trough in 2022–25 [C, E-WS12014-S014].

**What a downturn does to fees.** At incumbents, downturns cut *volume*, not *rate*. RH's average fee per placement rose 2.4% in 2023 and 3.8% in 2025 while placements fell 24.1% and 13.6% [A, E-WS12014-S009, S010]. A newcomer faces more discount pressure and more cancelled searches (E). The current cycle position is favourable:
- US manufacturing openings: 584k in September 2026, preliminary, up from 376k in April 2025 [C, E-WS12014-S014].
- Illinois manufacturing employment: 573.9k in October 2026, up from 562.5k in December 2025 [C, E-WS12014-S016].
- PageGroup's US gross profit: +9% in 2025, with strong Manufacturing [B, E-WS12014-S013].
- SIA's 2026 staffing forecast: +2.4% [C, E-WS12014-S030].

**Cycles recur. Plan for one inside years 2–6.**

### 7.6 Profit milestones (base)
| Milestone | Month reached |
|---|---|
| First month with operating profit ≥ $1k | **8** |
| ≥ $5k | **13** |
| ≥ $10k | **17** |
| ≥ $25k | **never within 60 months** |
| $100k/yr | Year 2 ($122,373) |
| $250k/yr | Year 5 ($259,002) |

- **$500k/yr:** only in the optimistic case (year 4, $707,656).
- **Conservative:** reaches ≥$1k/month in month 18 and never reaches $5k/month.

### 7.7 Capital accumulation to year 10 and owner distributions
| | Base | Conservative | Optimistic |
|---|---|---|---|
| Cumulative deployable, years 1–5 | $300,755 | $7,506 | $1,237,462 |
| Cumulative deployable, years 1–10 | **$1,015,803** | **$11,104** | $4,501,243 |
| Year-10 operating profit | $310,674 | $57,512 | $1,268,271 |
| Year-10 EV | $621,349 | $57,512 | $3,487,746 |
| Owner compensation, 10 years | $454,484 | $454,484 | $454,484 |

**Caveat that changes the reading.** "Deployable" treats the founder as working full-time for a $48k/year draw while producing most of the revenue.

If the founder stepped back and a producer-manager were hired at about $130–150k all-in (E), base year-5 operating profit of $259,002 would fall to roughly $110–130k before tax. Deployable cash would roughly halve. The 10-year figure is the value of the founder's own selling labour, not of a self-running asset.

### 7.8 Downside cases
| Case | Year 3 | Year 5 | Peak funding | Note |
|---|---|---|---|---|
| Conservative | $41,471 | $55,944 | $68,241 | The draw is not covered until year 4 |
| Growth twice as slow | $62,319 | — | $46,606 | — |
| 2009-type | $53,513 | — | $25,098 | Supplementary run |
| Validation failure | — | — | ≈$600–1,500 | **The realistic most-likely downside**: no fee agreements, stop at day 60 |

---

## 8. Capital deployment ladder

| Tier | What it buys | Evidence gate before spending | How it could be lost |
|---|---|---|---|
| **$0–500** | Role-map refresh; Recruiter Lite for 1–2 months ($170/month [D]); mileage; an ISA meeting | None (validation) | Subscription with no replies |
| **$500–2k** | LLC (≈$150, confirm); attorney review of the fee agreement (≈$1,500, E); domain and email; first CRM month ($95–135 [B]) | ≥3 managers say they would sign for a presented candidate; ≥5 movable candidates (tests 2–3 trending to pass) | Paperwork for a desk that never places |
| **$2–5k** | Laptop/headset/website ($2,500); 3 months of the full tool stack ($940/month); job ads | **≥5 signed agreements at ≥18%** (test 3 pass) | No placements in months 3–6 |
| **$5–10k** | Runway for tools and insurance to month 10; E&O/GL premium (MISSING); plant visits; optional Top Echelon ($350 + $150/month [B]) | ≥1 candidate in final rounds, or ≥1 accepted offer | A fallout or cancelled search wipes out the first fee |
| **$10–25k** | Receivables float (≈$23k of AR at about $17k/month revenue); 3-month cash reserve | ≥3 collected fees; trailing 3-month revenue ≥$15k/month | Slow-paying clients; fee dispute legal costs |
| **$25–50k** | Recruiter #1 ramp (~6 months × $6,900) | Trailing **6-month** revenue ≥$20k/month; ≥8 open searches; ≥8 active clients; 3-month reserve held | Wash-out hire (assume 50% odds, E); a downturn during the ramp |
| **$50–100k** | Recruiter #2 + coordinator, or contract-staffing payroll float (separate model) | Recruiter #1 produced ≥$60k of collected fees within 9 months; postings stable or rising | Cycle turn with two salaries on payroll: the 2009 analogue (−57% [A]) |

**Never spend capital on:**
- paid leads;
- big-brand job-board contracts;
- contact-data bulk licences beyond one seat;
- office space before recruiter #2.

---

## 9. Strategic wealth creation

**How it becomes a durable cash asset.** Only partly. Durability comes from three things:
1. The proprietary map of Illinois controls engineers.
2. Repeat integrator clients.
3. Placed-engineer referrals.

None of these is contractually locked: job orders are non-exclusive and recruiters can leave. Non-competes are void for recruiters earning under $75k ($80k from 2027) [A, E-WS12014-S006].

**How much capital it could generate:**
- **Base:** about $74k (year 3) to $128k (year 5) of deployable cash a year after the $48k draw, tax and reserves, with $300,755 cumulative by year 5.
- **Conservative:** essentially nothing beyond the founder's draw.

**When management could take over.** Not in the base case within 5 years. In the optimistic case, around year 3, with a team lead plus two recruiters and a coordinator.

**Can it fund other ventures?** Yes, in the base case: it is the cheapest route in Atlas to $100k+/yr of cash (year 2) on a peak funding of $12,836. The catch is that the cash is generated by the founder's hours. Every hour spent building the next holding-company asset is an hour not recruiting.

**Why it is / is not a strong first company:**

| It is, if... | It is not, because... |
|---|---|
| The founder's goal is a fast, low-capital personal cash engine that funds living costs and seeds the next venture | It fails the "durable, delegable, resilient" core test |
| The 60-day test passes | It is cyclical (resilience 3) |
| — | It is founder-bound (delegation 4, G7) |
| — | It has low transfer value (EV 2.0× base, 1.0× conservative) |

**Recommended framing:** a 2–3-year cash engine with an explicit decision at month 24. Either hire into a boutique, if trailing revenue is ≥$20k/month and recruiter #1 is working, or harvest and redeploy the cash into a more durable business.

---

## 10. Execution plan

### 10.1 First 7 days (Mon 30 Nov – Sun 6 Dec 2026; heavy AI access ends 5 Dec)

**Founder:**
1. Read §5.4 and the materials.
2. Decide hours available (F4).
3. Build a LinkedIn profile positioned as "controls & automation engineering recruiter".
4. Make a list of personal contacts in engineering or manufacturing (F7).
5. Pick 10 Tier A/B target roles from the role map.
6. Do a 2-hour self-study of PLC/SCADA basics: Rockwell vs Siemens, commissioning, DCS vs PLC, ISA-88/95 vocabulary.
7. Shadow-read 20 controls-engineer LinkedIn profiles and score them with the screen template.

**Claude prepares, before 5 Dec:**
- A packaged weekly ATS-scan script with a README, covering Workday CXS, Greenhouse, iCIMS and UKG.
- A spreadsheet CRM template mirroring the KPI sheet.
- Technical-screen scenario bank: 10 scenarios across PLC logic, HMI alarm management, SCADA historian, motion and safety.
- Anonymised candidate-profile template.
- Fee agreement draft for the attorney.
- All outreach drafts (materials).

**Spend:** $0.

### 10.2 First 30 days
**Founder:**
- 60 candidate approaches (test 2).
- Start hiring-manager conversations once ≥2 candidates are presentable (test 3).
- Attend one ISA Chicago-section event (cost MISSING).
- Begin Recruiter Lite only when sending the first InMails.

**Organisations to approach first** (Tier A/B only): Wunderlich-Malec Addison, BW Design Group Oak Brook, Concentric, WESA, Wynright Bolingbrook, Formic, Yaskawa Waukegan, Medline Mundelein, Ingredion Bedford Park, Primient Decatur.

**Questions to ask hiring managers** (past behaviour, not hypotheticals):
1. "When did you last use an outside recruiter for a controls role, and what fee did you pay?"
2. "What happened with this posting so far?"
3. "Do you need vendor approval to engage a new firm?"
4. "What would make you interview someone this week?"

**Evidence required:**
- Logged reply rates.
- Count of signed agreements.
- Fee percentages quoted.
- Portal or MSP mentions.

**Proposed spend:** ≤$340.

**Accept a first "order"** (a signed fee agreement) only when all of these hold:
- the fee is ≥18%;
- the guarantee is ≤90 days, replacement-only;
- payment is net-30 from start;
- candidate ownership is ≥12 months;
- the attorney-reviewed template is used. Sign the LLC first.

**Abandon** if, at day 60, there are <2 agreements after 30 conversations.

### 10.3 First 90 days
- 5+ fee agreements and 8–12 submittals.
- First final-round interviews, and ideally one accepted offer.
- Form the LLC; have the attorney review the template; bind E&O/GL if a client requires it.
- Weekly KPI review: §4 and the materials.
- **Slow branch:** if agreements are signed but there are no interviews by day 90, the screen or candidate quality is the problem. Re-score candidates and narrow to integrators.

### 10.4 First year
| Milestone | Target | Failure / slow branch |
|---|---|---|
| Month 6 | ≥1 accepted offer; ≥5 active agreements | None: **stop before any spend >$2k** |
| Month 10 | ≥1 collected fee ≥$15k | None: stop. Total loss ≈ $10–13k plus time |
| Month 12 | ≥3 placements; run-rate toward the base case's $157k year-2 revenue | 1–2 placements: you are in the conservative case. Continue only if trend improves; no hires |
| Month 18 | Trailing revenue ≥$13k/month (base month 18 = $13,569) | Below $8k/month: harvest or exit |
| Month 24 | Boutique or harvest decision (§9) | — |

---

## 11. Pre-mortem

| Failure | How it happens | Early warning | Cheap preventive test |
|---|---|---|---|
| **Lost $5k** | Tools and insurance bought before demand is proven; candidates reply but managers say "portal only" or "we use Actalent" | <5 agreements after 60 conversations | Do test 3 before buying anything but Recruiter Lite |
| **Lost $25k** | One fee falls off; a client hires a presented candidate later and refuses to pay; legal costs; 10 months without a collected fee | "We already had that résumé" disputes; DSO >60 | Signed agreement before submittal; consent log; replacement-only guarantee |
| **Lost $50k** | Recruiter #1 hired on two lumpy good months, then a manufacturing downturn hits (2023-type −21.7% perm [A]) | Tier A/B postings down >40% quarter on quarter (JOLTS trend [C]) | Use the 6-month trailing trigger and a 3-month reserve before hiring |
| **Revenue but no profit** | Recruiters hired faster than they ramp. The model's "hires 30% sooner" cuts year-3 operating profit to $125,393. At scale PageGroup converts only 2.7% of gross profit to EBIT [B] | Recruiter cost >60% of their trailing billings after month 9 | Commission on collection; strict 9-month productivity gate |
| **Exhausting low-paid job** | The conservative case: the founder works full-time for a ~$41k year-3 operating profit and the draw is not covered until year 4 | Year-1 placements ≤2 | Month-12 checkpoint (§10.4) |
| **Cash crunch** | Zero-revenue months while the $4k draw runs; one slow payer | Cash <2 months of costs plus draw | Hold a 15% fallout reserve; invoice on start |
| **Can't run without founder** | The base case; clients follow the founder | >70% of revenue from the founder's desk at year 3 | Accept it consciously; CRM discipline; non-solicits [A, E-WS12014-S006] |
| **No deployable surplus** | Conservative: $11,104 over 10 years | Year-2 operating profit <$50k | Exit to employment or marketplace recruiting; redeploy time |

**Additional risks:**
- **AI substitution.** Clients' in-house teams source the same engineers with LinkedIn Hiring Assistant. Early adopters reported reviewing 62% fewer profiles, a vendor claim [D, E-WS12014-S021]. Robert Half lists AI substitution as a risk [A, E-WS12014-S010]. PageGroup expects AI to stay a supporting tool [B, E-WS12014-S013].
  - **Indicator:** rising "we found them ourselves" disputes and falling fee acceptance.
  - **Prevention:** stay in roles where persuasion and technical vetting decide the hire, such as experienced commissioning, nuclear I&C and DCS.
- **Compliance misstep.** Asking salary history or charging a candidate is a statutory breach [A, E-WS12014-S003, S001]. Script it out.

**The three weakest assumptions:**
1. **Founder conversion.** 9 conversations/month × 30% × 20% = 0.54 new paying clients/month at full pace by month 12 (E). This puts the founder at a mature-firm average fee earner (≈$195k/yr) by year 3.
2. **The repeat engine.** 0.45 repeat placements per active client per year, 5% monthly churn and 2 referrals per 100 active clients per month (E). There is no source for any of these.
3. **No downturn in years 1–5.** The model's built-in recession is milder than the record [A, E-WS12014-S011, S009].

---

## 12. Required confirmations (direct contact needed; none performed)
1. **Counsel:**
   - The 225 ILCS 515 exclusion applies to this contingency model as operated, including remote placements of Illinois residents with out-of-state employers.
   - The current statute text on ilga.gov (unavailable 2026-11-28).
   - Equal Pay Act duties as a third-party poster.
   - Whether desk-run reference checks trigger the FCRA.
   - Fee-agreement enforceability: candidate ownership, replacement guarantee, interest and attorney fees.
2. **IDHR:** status of AI-in-employment rules under P.A. 103-0804 [D, E-WS12014-S008].
3. **City of Chicago BACP:** licence type and fee if operating within city limits [D, E-WS12014-S029].
4. **Illinois SOS:** LLC filing and annual report fees (E).
5. **Insurance broker:** E&O/GL premiums and coverage for discrimination and fee-dispute claims (MISSING).
6. **LinkedIn:** Recruiter Lite price, InMail allowance and rollover, and permitted use [D, E-WS12014-S022].
7. **Top Echelon:** split percentages and per-placement network fee (MISSING); volume of controls job orders.
8. **Customers:**
   - fee percentages actually paid to agencies for controls roles;
   - guarantee norms;
   - vendor-approval requirements at Tier A/B employers;
   - whether long-open postings (e.g., Ingredion since 2026-06-08) are live, filled or evergreen.
9. **Candidates:** mobility and pay expectations of experienced Illinois controls engineers. Ask expectations only, never salary history [A, E-WS12014-S003].

### Scores (Stage E)
| Criterion | Stage D | Stage E | Reason |
|---|---|---|---|
| fcf | 5 | 5 | Base year-3 $170,012 / year-5 $259,002, but founder labour |
| roic | 8 | 8 | Peak funding $12,836 (base) |
| access | 5 | 5 | Integrators reachable; large employers gated [D, E-WS12014-S026] |
| scale | 4 | 4 | Base hires only 1 recruiter in 5 years |
| resilience | 4 | **3** | 2009 −57%, 2023 −21.7% perm [A]; AI sourcing pressure |
| entry | 4 | 4 | Technical-screen wedge, copyable |
| delegation | 4 | 4 | G7 WARN; non-competes void for juniors [A] |
| cash | 7 | 7 | No float; net-30 |
| feasibility | 10 | **9** | Licence exclusion verified [A], with conditions; plus agency-specific pay and AI rules |
| ai | 6 | **5** | Efficiency is real but equally available to clients' in-house recruiters [B, E-WS12014-S021] |

**Evidence confidence:** D (was C).
