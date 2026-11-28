# WS04-014 — Managed IT + HIPAA compliance for independent dental and vet practices (absorbs WS04-021) · Stage D deep dive

> **Verdict: FINALIST** (conditional on validation) · evidence level **D** · revised raw score 5.73, evidence-adjusted 5.51.
>
> **The decisive fact.** This is the only concept in this batch where the base case is cheap to start and cheap to test:
> - **Capital at risk:** about **$22k** with no owner draw, or **$35k** with a $4k/month draw.
> - **Billing:** monthly in advance.
> - **Cheapest test:** a paid stand-alone HIPAA Security Rule risk analysis, which the founder can try to sell within weeks.
>
> **What limits it:** the ceiling is modest. Remote dental MSPs publish **$399–749 per practice per month** [B, C6-S006, C6-S007], so the price is anchored low.
>
> **Model results:**
>
> | Case | Year-3 operating profit | Year-5 operating profit |
> |---|---|---|
> | Base | **$71k** (32 practices at $700/month) | about **$133k** |
> | Conservative | $14k | — |
> | Optimistic | $282k | — |
>
> All of this is before the founder's pay, and the founder is also the first technician.

## 1. Specific initial niche

**The offer.** Flat-fee managed IT plus a HIPAA Security Rule compliance layer for independent dental and companion-animal veterinary practices with 5–15 workstations.

**Where.** Chicago's North Side, roughly a 5-mile radius around Lakeview, North Center, Lincoln Square, Ravenswood, Lincoln Park, Logan Square and Wicker Park.

**What's included:**
- Monitoring, patching, endpoint protection and backup.
- Support for the practice-management server and the imaging/radiography workstations.
- Same-day on-site response.
- An annual risk analysis with policies and staff training.

**Why this area:**
- **Dental density:** NPPES lists **429 dental organisation NPIs in 14 North Side ZIP codes** [A, DD-S012].
- **Vet density:** the City of Chicago lists **about 79 veterinary/animal-hospital names with current Animal Care Licenses** [A, DD-S013].
- **Travel:** in a dense radius a technician drives minutes, not 45 minutes. That is what makes an on-site SLA cheap enough to compete with remote flat-rate providers.

**Why independents.** The base is mostly independent and consolidating slowly:
- Illinois DSO affiliation was 13.9% in 2025, up only 1.2 points since 2022 [C, C6-S001, C6-S002].
- Corporates own about 25% of primary-care vet practices [C, C6-S005].

**Fallback geography:** central DuPage, where there are 458 dental organisation NPIs in 20 cities, about 362 sites [A, DD-S012].

## 2. Named operators

| Operator | What is known | Level |
|---|---|---|
| Siotek | $399/month flat per practice (about 10 workstations): unlimited remote support, backup, up to 4 on-site visits a year. 12-month term, then month-to-month. HIPAA assessment only in a custom tier | B, C6-S007 |
| Darkhorse Tech | $422 (Silver) / $749 (Gold) a month for 15 workstations, i.e. $28–50 per workstation | B, C6-S006 |
| Henry Schein One (Dentrix) | 35,000+ practices on Dentrix. Sells managed dental IT, cybersecurity, backup and hardware-as-a-service | B, DD-S015 |
| Patterson (Eaglesoft) | Distributor with technology services. Dental segment operating margin about 8.4% | B, WS04-S026 |
| Dental Technology Services Inc. (Wauconda), Tech Direct 2 U (Chicago), NorthShore PC Service (Skokie), adNET Technology Management (Elgin), The Isidore Group (Chicago) | Local providers listed in a Chicago dental-IT directory. Directory states a market range of $500–2,000/month; no provider prices | D, DD-S019 |
| CMIT Solutions Chicago | Franchise MSP advertising dental-office support. Prices MISSING | D (search result) |
| FlossByte | $59–99 per device per month; legitimacy unverified | D, C6-S008 |

**Incumbent vs. new-entrant economics:**
- **Incumbents:** distributors earn distribution margins of about 7–8% [B, WS04-S013, WS04-S026]. Small-MSP P&Ls are MISSING.
- **New entrant:** pays list price for tools and carries the founder's labor at no cost until about 14 practices.

## 3. Suppliers and partners

The full list is in `09_databases/suppliers/WS04-014_suppliers.csv`.

**Documented (published pages retrieved):**
- **Syncro (RMM + PSA):** $129 (Core) / $179 (Team) per technician per month on annual billing. Unlimited endpoints. Microsoft 365 backup $1.90/user/month. AI features are free until January 2027, then usage-based [B, DD-S017].
- **Backblaze B2 (off-site backup):** $6.95/TB-month, no minimums [B, DD-S018]. Whether Backblaze signs a BAA is not verified.
- **Open Dental (practice software; partner for server work):** $199/location/month for the first 12 months, then $149; +$20 per provider beyond 3 [B, DD-S014].
- **IDEXX:** Cornerstone is server-based, used by "thousands of practices"; ezyVet and Neo are cloud products [B, DD-S016]. Cloud migration both creates project work and removes server work.

**Assumed — requires direct confirmation:**
- Microsoft 365 Business Premium through a CSP distributor such as Pax8. The price page returned 503, so licences are treated as pass-through.
- The HHS/ONC Security Risk Assessment tool (free, not re-verified).
- Covetrus AVImark and Patterson Eaglesoft server requirements.
- Cyber liability + technology E&O insurers (premiums MISSING; the model uses $550–1,000/month, E).
- A licensed low-voltage cabling subcontractor. Chicago's licensing rule is MISSING.

**Not priced:** endpoint detection and response (EDR), email security and DNS filtering. No per-endpoint price was retrieved; the model uses about $6 per endpoint (E).

## 4. Named prospective customers

The CSV lists **35 prospects**, all "prospect — not contacted".

**21 dental practices** (brand-named, single-site NPPES organisations in the core ZIPs, not known DSO brands), for example:
- Cusp Dental Studio, Pristine Family Dentistry, Irving Park Dentistry, Montrose Dental Group
- Oz Park Family Dental, Park West Family Dentistry, Lincoln Park Dental Care, Riverpoint Dental
- West End Dental, Brushin' on Belmont, Skyline Smiles of Roscoe Village, Floss Dental Studio
- Wicker Park Dental, Lincoln Square Dental Associates, Andersonville Dental, Ravenswood Dental Group
- Lake View Dental Associates, The Wrigleyville Dental Group, Bristle Dental Studio

**14 veterinary hospitals** (City of Chicago Animal Care Licenses), for example:
- Delta, Belmont, Ravenswood, Duke, Lincoln Square, Portage Park, Roscoe Village
- North Center, Mid North and Logan Square Animal Hospitals
- Wrigleyville Veterinary, Ukrainian Village Veterinary Center

**Data caveats:**
- **Phone numbers:** dental phones are the practice-location phones filed in NPPES. Vet contact pages are MISSING.
- **Independence and current operation:** not verified. Many NPPES records were last updated in 2008–2020.
- **No IDFPR source:** the IDFPR licensee lookup was not used because it is interactive and lists individuals.

## 5. Representative transactions

| Transaction | Revenue | Direct costs | Contribution | Timing |
|---|---|---|---|---|
| 10-workstation dental practice, one month | $700 | Security stack, 11 endpoints × ~$6 = $66 (E); backup 2 TB × $6.95 = $14 (B); compliance portal and training $15 (E); technician 6 hrs × $37.40 = $224 (C) | **$381 (54%)** | Billed the 1st of the month, autopay |
| Stand-alone HIPAA risk analysis + policies, 6-workstation vet clinic | $1,500 | Analyst 10 hrs × $37.40 = $374; report production $25 | **$1,101 (73%)** | 50% upfront |
| Server replacement / new-office network project | $6,200 | Hardware $3,800 (resold at $4,300); technician 16 hrs = $598; cabling subcontractor $400 | **$1,402 (23%)** | 50% deposit at order |

**Notes:**
- The technician rate comes from the Illinois user-support median of $59,860, loaded ×1.3 and divided by 2,080 hours [C, C6-S026].
- Contribution is before RMM/PSA ($358/month for 2 seats), vehicle and insurance overhead.

## 6. Customer acquisition

**Customer #1 (weeks 1–8).** Walk into the 35 prospects with a one-page offer: a free 45-minute network and backup check, plus a fixed-price HIPAA risk analysis.

Two triggers matter most:
- Practices that cannot show a current risk analysis. It is a Security Rule obligation [A, WS04-S018].
- Practices running end-of-life servers.

**Customers #2–10:**
- Referrals from equipment-dealer reps and practice brokers, who handle new-office build-outs and practice sales.
- Study clubs.
- Converting stand-alone risk-analysis clients to monthly service.

**Customers #11–100:**
- Peer referrals.
- Content on ransomware recovery for dental imaging.
- Local dental-society sponsorships.
- A second radius (central DuPage) once the first technician is hired.

**Funnel (E):** 12 qualified conversations a month → 35% reach a proposal → 25% win, about 1.05 new practices a month. Referrals add about 1 per 100 active practices per month.

**Weekly founder time:** about 8–10 hours of in-person selling, about 25 hours of technical delivery until the first technician is hired at about 14 practices.

**CAC and payback:**
- About $150 variable plus $400/month fixed, roughly **$450–500 per customer** plus founder time.
- Contribution is about $320/month after technician time, so payback is under 2 months.
- At 1% monthly churn the expected life is long. Capped at 60 months, lifetime contribution is about $19k.

## 7. Pricing strategy

| Item | Price |
|---|---|
| Per workstation | $60/month |
| Minimum per office | $450/month |
| HIPAA compliance layer | +$100/month: annual risk analysis, policy set, staff training log, BAA register |
| Base 10-workstation office | **$700/month** |
| Onboarding / remediation | $1,500 one-time |
| Stand-alone risk analysis | $1,500 |
| Projects | Hardware at cost +10–15%; labor $120/hour (E) |

**Where this sits in the market:**
- **Above** remote flat-rate rivals: $28–50 per workstation (Darkhorse) and $399 flat (Siotek).
- **Inside** the local $500–2,000 retainer range [D, DD-S019].

**The justification for the premium:**
- Same-day on-site response.
- Imaging and practice-management server competence.
- Compliance work that rivals sell only in custom tiers [C6-S007].

**Contract terms:** 12-month initial term, then month-to-month, matching market practice [C6-S007].

**Sensitivity:** if price must fall to $550, year-3 operating profit falls to about **$26k** (tornado, −25%).

## 8. Working capital and cash conversion

The business runs on prepaid recurring revenue.

| Practices | Monthly recurring revenue | Prepaid float (0.33–0.5 month) | Project hardware exposure |
|---|---|---|---|
| 10 | $7k | +$2–3.5k cash | ~$4k (2 projects/month at 50% deposit) |
| 50 | $35k | +$12–17k | ~$8k |
| 200 | $140k | +$47–70k | ~$20k |

- Distributor credit terms are MISSING; net-30 is assumed.
- Year-3 base free cash flow ($76k) slightly exceeds operating profit ($71k) because of the prepayment.

## 9. Regulatory path

- **No Illinois licence** has been identified for IT management.
- **HIPAA:**
  - Sign a BAA with each practice [A, WS04-S018].
  - Hold the Security Rule safeguards for the founder's own systems.
  - Flow breach-notification duties down to subcontractors such as Backblaze and the RMM vendor.
- **Pending federal rule.** The January 2025 Security Rule proposal would require asset inventories, MFA, encryption and annual compliance audits. It is **still proposed**: the Federal Register showed no final rule on 2026-11-28 [A, DD-S020]. It is a sales talking point, not a mandate.
- **Cabling:** subcontract to a licensed firm; Chicago's low-voltage rules are MISSING.
- **Insurance:** cyber liability + technology E&O + general liability, about $7–12k a year (E). Many practices will ask for evidence.
- **Biometric timeclocks:** avoid recommending them, because of Illinois BIPA exposure (statute not re-verified here).
- **Timeline:** about 1 month (entity, insurance, tool accounts, BAA template).

## 10. Operations workflow

**Lead to cash:**
1. Lead.
2. Free assessment, with an RMM agent deployed under a temporary agreement.
3. Proposal.
4. Signed MSA + BAA.
5. Onboarding: documentation, credential vault, backup to B2 plus a local NAS, security stack, firewall review.
6. Monthly autopay.
7. Tickets through the PSA.
8. A quarterly review, plus the annual risk analysis report.

**Who does what:**
- **Human:** on-site imaging and sensor issues, server replacement, client relationships.
- **AI-assisted (affordable after December 2026 at ordinary API prices):** ticket triage and summaries (Syncro AI), drafting policies and risk-analysis narratives from scan data, client reports.
- **Automatable:** patching, monitoring and backup verification.

**Existing tools:**
- Syncro Team, $179/tech.
- Backblaze B2.
- A password/documentation vault (about $120/month, E).
- The HHS SRA tool.

**Staffing (base case):**
- Founder is the only technician until about 14 practices.
- One technician per about 28 practices (about 300 endpoints, E).
- A coordinator at about $40k monthly recurring revenue.
- A senior engineer at about 70 practices.

## 11. Competitive position and defensibility

**What accumulates:**
1. **Route density:** more practices per square mile lowers the cost of the on-site SLA.
2. **Documentation lock-in:** credential vaults, network diagrams and the risk-analysis history make switching tedious.
3. **Referral relationships** with dealer reps and brokers.
4. **Practice-software and imaging know-how.**

**Threats:**
- Henry Schein One and Patterson bundle IT with the software and equipment they already sell [B, DD-S015].
- Cloud practice-management software (Dentrix Ascend, ezyVet) shrinks server work.
- DSO and corporate-vet acquisitions remove clients. Illinois DSO affiliation is rising about 0.4 points a year [C].

Defensibility is "credible wedge, slowly accumulating moat". Entry score: 4.

## 12. Key risks and pre-mortem

| Loss level | What happened | Early warning sign |
|---|---|---|
| **$5k** | Insurance and tools bought; 30 walk-ins produce <3 paid risk analyses; the founder stops | Office managers say "our IT guy handles it" |
| **$25k** | 8–10 practices won, but on-site time runs 10+ hours/practice/month; the first technician hire makes it loss-making | Tickets per endpoint above about 1.5 a month; unbilled project time |
| **$50k** | A ransomware incident at a client during onboarding, before backups are verified; liability claim and lost referrals | Any client without a tested restore in 30 days |

**Other risks:**
- A practice is sold to a DSO (expect churn of about 1–1.5% a month).
- Founder burnout from doing both sales and the technical work.
- Remote rivals undercut price.

**Stress tests** (year-3 operating profit stays positive in every test):

| Test | Year-3 operating profit |
|---|---|
| Win rate −40% | $22k |
| Recession | $22k |
| Labor +20% | $55k |
| Growth twice as slow | $43k |

## 13. Validation plan

These experiments are ordered so paid evidence comes before verbal evidence.

| # | Experiment | Cost | Success | Kill |
|---|---|---|---|---|
| 1 | Paid HIPAA risk-analysis offer at $750–1,500, walked into 30 of the 35 prospects over 4 weeks | ~$150 (print, mileage) | ≥3 paid engagements (≥10% of visits) | 0–1 paid |
| 2 | Free 45-minute network/backup check offered alongside, to count "no tested restore" findings | Time only | ≥50% of checked practices lack a tested restore or run an unsupported OS | <20% |
| 3 | Price test: present $60/workstation + $100 compliance and record objections against Siotek's $399 | $0 | ≥2 signed letters of intent for monthly service at ≥$550 | All prospects anchor below $450 |
| 4 | Referral-partner test: 5 conversations with equipment-dealer reps or practice brokers | ~$50 | ≥2 named introductions | None |

**Total cost:** under about **$300**. Insurance should be bound only once the first paid engagement is agreed (E).

## 14. Revised scores and verdict

| Criterion | Stage C | Stage D | Note |
|---|---|---|---|
| fcf | 4 | **4** | Base year-3 $71k, years 4–5 $133–150k |
| roic | 7 | **7** | Year-3 operating profit ÷ $22–35k peak ≈ 200–320% |
| access | 5 | 5 | |
| scale | 5 | 5 | |
| resilience | 7 | 7 | |
| entry | 4 | 4 | |
| delegation | 7 | 7 | |
| cash | 8 | 8 | |
| feasibility | 9 | 9 | |
| ai | 5 | 5 | |

- **Composite:** raw 5.73; evidence-adjusted 5.51 (D).
- **Model detail (base):** breakeven in month 10; first month with ≥$10k operating profit is month 37; 10-year deployable cash $346k.
- **Model range (year-3 operating profit):** conservative $14k, optimistic $282k.
- **Verdict: FINALIST**, conditional on experiment #1.

**Limitations:**
- Atera, Microsoft and Henry Schein TechCentral pages could not be retrieved.
- Chicago MSP prices come from a directory (D).
- Technician capacity and conversion rates are E.
