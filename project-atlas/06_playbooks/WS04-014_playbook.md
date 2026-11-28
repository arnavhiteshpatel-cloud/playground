# WS04-014 — Managed IT + HIPAA security compliance for independent dental and veterinary practices (Chicago North Side) · Stage E playbook

> **Verdict: FINALIST. Validate now (under $400); do not launch until the paid-wedge test passes.** Evidence level **D**. Revised raw score 5.68, evidence-adjusted 5.48.
>
> **What it is.** This is the cheapest finalist to test and to start. Revenue is recurring and billed in advance, and the technical work fits the founder. The founder can sell the first paid product, a HIPAA risk analysis for dental practices, within weeks.
>
> **What limits it.**
> - **Price ceiling.** Remote dental specialists publish list prices that put a 10-workstation office at roughly **$281–$499 per month** before add-ons.
> - **Founder as technician.** The founder does all the technical work until about 14 practices, which is month 20 in the base case.
> - **Organic ceiling.** One dense radius supports roughly **$150–250k a year** of operating profit before owner pay. Going beyond that needs a second radius or tuck-in acquisitions.
>
> **Model (rebuilt 2026-11-28).** All figures are operating profit before owner pay.
>
> | Case | Year 3 | Year 5 | Peak funding with $4k/mo draw | Peak funding with no draw |
> |---|---|---|---|---|
> | Base | **$64,047** | **$128,878** | **$42,408** | $21,831 |
> | Conservative | **$12,175** | **−$38,018** | **$307,555** | — |
> | Optimistic | $268,828 | $553,295 | — | — |
>
> - **The base case is a modest, durable, cash-generating local company.** It is not by itself a $500k-FCF engine.
> - **The conservative case is a failure** that the validation gates are designed to catch for a few hundred dollars.

---

## Corrections to earlier stages (explicit)

1. **Correction: veterinary practices are not HIPAA covered entities.**
   - **What changed.** Stages A–D framed HIPAA risk analysis as a vet product. Stage D's representative transaction #2 was a "HIPAA risk analysis for a 6-workstation vet clinic".
   - **Why.** HIPAA "health care" relates to the health of an *individual*, the person who is the subject of the information. A covered entity is a health plan, a clearinghouse, or a provider of health care that transmits standard transactions [A, E-WS04014-S003]. Animal care falls outside this.
   - **Consequence.** The HIPAA layer is a **dental** (and human-medical) product. For vets the equivalent is a cyber-insurance-readiness / payment-card / client-data documentation layer, which carries a weaker compulsion.
   - **Model change.** The transaction was rewritten as a dental practice. Blended ARPC was cut from $700 to $690.
2. **Correction: the remote price anchor is lower than "$399–749 per practice" implies.**
   - Darkhorse publishes *per-workstation* rates of $28.13 (Silver) and $49.93 (Gold). The $422/$749 figures are for 15 workstations, so a 10-workstation office would pay **$281/$499** [B, E-WS04014-S005].
   - Siotek's $399 *excludes* Huntress EDR and Proofpoint email security, which are add-ons. It also waives onboarding fees [B, E-WS04014-S004].
   - **Consequence.** The $700 dental price is a roughly 40% premium over the fully-secured remote alternative, not 0–75%. The on-site SLA has to earn that premium.
   - **Model change.** Onboarding revenue was cut from $1,500 to $1,000.
3. **Correction: HIPAA Security Rule status.** Stage D said the January 2025 NPRM was "still proposed". That is true [A, E-WS04014-S001] but incomplete.
   - The latest Unified Agenda moved the rule from **"Final Rule Stage" (target 05/2026)** to **"Long-Term Actions" (target 07/2027)** [A, E-WS04014-S002].
   - The NPRM proposes a final rule effective 60 days after publication, plus the standard 180-day compliance period [A, E-WS04014-S018].
   - Even if the July 2027 target holds, compliance would not be due before roughly **March 2028**. It is a talking point, not a demand driver for this plan.
4. **Correction: backup BAA.** Stage D assumed Backblaze would sign a BAA. Backblaze offers a BAA to customers who are **covered entities** [B, E-WS04014-S013]. A subcontractor BAA with an MSP is not stated.
   - **Fix:** either the practice holds its own B2 account (the practice signs the BAA and the MSP administers it), or the founder uses an MSP backup vendor that signs a subcontractor BAA. This must be confirmed.
5. **Correction: cabling.** This was MISSING and is now **A**. Chicago requires a licensed electrical contractor for communications and power-limited circuits. A "low voltage" licence ($150 a year) requires employing a licensed supervising electrician [A, E-WS04014-S016]. All structured cabling must be subcontracted.
6. **New: Chicago cloud tax.** The Personal Property Lease Transaction Tax on non-possessory computer leases (cloud software) rose from 11% to **15%** on 2026-01-01 [C, E-WS04014-S011].
   - **Modelled:** applied to the founder's own RMM/PSA.
   - **Not modelled:** whether a bundled managed-service fee charged to Chicago clients is taxable. This is **unconfirmed** and needs tax counsel.
7. **Insurance re-based.** The Stage C/D estimate of $7–12k/yr was E. Insureon's June 2026 medians for IT consultants are tech E&O $75, cyber $128 and GL $31 per month [D, E-WS04014-S010].
   - **Model change:** base $550/month, which allows for healthcare admin-access risk. Conservative $900, optimistic $400.
8. **Security stack re-priced.** Managed EDR runs $7–12 per endpoint and email security $5–10 per mailbox at retail [D, E-WS04014-S006].
   - **Model change:** base recurring gross margin 0.79 (was 0.80).

**Score change.** Only feasibility moves, from 9 to 8. Two things drive it:
- the company's own business-associate Security Rule programme;
- the PPLTT and sales-tax administration.

All other scores are unchanged: fcf 4, roic 7, access 5, scale 5, resilience 7, entry 4, delegation 7, cash 8, ai 5. Raw 5.68 → evidence-adjusted 5.48 (D).

**Net effect** (base case, Stage D → Stage E):

| Measure | Stage D | Stage E |
|---|---|---|
| Year-3 operating profit | $71,188 | $64,047 |
| Year-5 operating profit | $132,608 | $128,878 |
| Peak funding, with draw | $35,442 | $42,408 |
| Conservative year-3 operating profit | $14,155 | $12,175 |

---

## 1. Business explanation

**What it does.** A small local IT company that keeps independent dental (and companion-animal vet) offices running and secure for a flat monthly fee. Every computer and the server get:
- 24/7 monitoring;
- patching;
- endpoint detection and response (EDR);
- email and DNS security;
- local plus cloud backup that is tested.

The company also:
- supports the practice-management server (Dentrix, Eaglesoft, Open Dental; for vets, Cornerstone or AVImark) and the imaging chain (sensors, pan/CBCT, imaging bridges);
- manages the firewall and Wi-Fi;
- coordinates the practice's software vendors;
- turns up **on-site the same day** inside a ~5-mile radius.

For dental clients it adds a documented annual **HIPAA Security Rule risk analysis**, a policy set, staff training records and a BAA register.

**Why practices pay:**
1. **Downtime stops production.** A dental chair that cannot pull X-rays or charts stops billing. Practices are small, have no IT staff, and the office manager absorbs the pain.
2. **The law already requires a risk analysis.** The Security Rule in force today requires covered entities, and their business associates, to "conduct an accurate and thorough assessment" of risks to ePHI. It also requires a data backup plan, a disaster recovery plan and an emergency-mode operation plan [A, E-WS04014-S020]. OCR enforces this:
   - Its **Risk Analysis Initiative** reached its 14th enforcement action by June 2026 [C, E-WS04014-S008].
   - That includes a **$103,000** settlement with a small **Illinois** provider after a phishing breach of 1,980 patients [C, E-WS04014-S009].
3. **Cyber insurance now demands specific controls and an attestation.** Travelers' MFA supplement asks about:
   - MFA on web email, on all remote access (including for third-party service providers) and on all admin access to directory, backups, firewalls and servers;
   - whether the signer was assisted by "the person in charge of IT security" [B, E-WS04014-S007].
   In an Illinois federal case, Travelers sought to rescind a $1M policy after a ransomware claim, alleging false MFA answers [C, E-WS04014-S019]. A small practice has no "person in charge of IT security". The MSP becomes that person.

**How it earns:**
- **Recurring fee per practice:** base blended **$690/month**. A dental office pays 10 workstations × $60 plus a $100 compliance layer = $700. A vet pays about $660.
- **One-time onboarding/remediation:** base $1,000.
- **Projects:** server replacement, new-office build-outs, hardware at cost +10–15%.
- **Stand-alone risk analyses:** $1,500 list.

The gross margin on the recurring fee after per-practice tools is about 79% (E/D). The real cost is technician hours: roughly 6 per practice per month (E).

**Why it is attractive for this founder:**
- Prepaid, recurring, sticky revenue: a 12-month initial term is market practice [B, E-WS04014-S004].
- No licence for IT work.
- Capital needs in the tens of thousands, not hundreds.
- Work the founder's technical background can do on day one.
- Established, hireable roles (help desk, field technician, systems engineer).
- A fragmented, slowly consolidating buyer base:
  - 71% of Illinois dentists work in single-location practices.
  - Illinois DSO affiliation rose from 12.7% to 13.9% over 2022–25, against 17.0% nationally [C, C6-S001, C6-S002].

**Why it is not more attractive:**
- Price is anchored by remote specialists.
- Distributor technology arms bundle IT with equipment and software (Henry Schein One markets managed IT, cybersecurity and backup to 35,000+ Dentrix practices) [B, DD-S015].
- Cloud practice-management software slowly removes server work.
- The ceiling of a single-radius local MSP is modest.

---

## 2. Commercial entry

**Initial niche.** Independent general and pediatric **dental** practices with 5–15 workstations, a local practice-management server and digital radiography.
- **Secondary:** independent companion-animal vet hospitals inside the same streets, sold on IT plus insurance readiness, not HIPAA.
- **Exclude for now:** DSO-affiliated offices (their IT is centralised) and practices fully on cloud PM with no imaging server (low on-site need).

**Geography.** Chicago North Side, roughly a 5-mile radius around Lakeview, North Center, Lincoln Square, Ravenswood, Lincoln Park, Logan Square and Wicker Park.
- **Dental:** NPPES lists 429 dental organisation NPIs in 14 North Side ZIPs [A, DD-S012].
- **Vet:** the City lists about 79 vet/animal-hospital names with current Animal Care Licenses [A, DD-S013].
- **Fallback / second radius:** central DuPage, with about 362 dental sites [A, DD-S012]. DuPage also avoids the Chicago lease-transaction-tax question [C, E-WS04014-S011].

**Named suppliers (full list in `09_databases/suppliers/WS04-014_suppliers.csv`):**

| Supplier | Terms | Evidence |
|---|---|---|
| Syncro RMM/PSA | $129/$179 per technician per month (annual), unlimited endpoints; AI features free until January 2027, then usage-based | [B, DD-S017] |
| Backblaze B2 | $6.95/TB-month; BAA for covered entities only | [B, DD-S018; B, E-WS04014-S013] |
| HHS SRA Tool v3.7 | Free | [B, E-WS04014-S017] |
| EDR/MDR (Huntress is the add-on Siotek resells) | Price MISSING; modelled at $7 per endpoint | |
| Email security (e.g., Proofpoint) | Price MISSING; modelled at $3 per mailbox | |
| Microsoft 365 Business Premium | About $22/user/month retail; pass-through [D, E-WS04014-S006]. Distributor route (e.g., Pax8) MISSING | |
| Insurance | Tech E&O + cyber + GL through a broker; Insureon medians as above | [D, E-WS04014-S010] |
| Cabling | A Chicago-licensed low-voltage electrical contractor (to be identified) | [A, E-WS04014-S016] |
| Optional compliance platform / benchmark competitor | Medcurity Small Practice SRA, $499/yr | [D, E-WS04014-S012] |

**Named prospects: top 15 to visit first.** All are "prospect — not contacted". None has been checked for DSO ownership or for an existing IT contract. Selection favours:
- group/associate names (more workstations);
- specialty or pediatric taxonomies (more imaging);
- recently updated NPPES records (likely active);
- physical clustering, so one walking route covers several.

| # | Practice | Address | Why it is on the list |
|---|---|---|---|
| 1 | Lincoln Square Dental Associates, Ltd. | 4770 N Lincoln Ave | "Associates" implies multiple dentists; record updated 2020; next to #15 |
| 2 | Lake View Dental Associates, PC | 1014 W Belmont Ave | Multi-dentist name; Belmont corridor cluster with Belmont Animal Hospital |
| 3 | Montrose Dental Group P.C. | 1744 W Montrose Ave | "Group"; Ravenswood cluster |
| 4 | Ravenswood Dental Group | 5015 N Paulina St | "Group"; 2008 record suggests a long-established practice, possibly a legacy server |
| 5 | The Wrigleyville Dental Group | 1353 W Cornelia Ave | "Group"; Lakeview cluster |
| 6 | Webster Dental Care of Lakeview, Ltd | 2829 N Lincoln Ave | GP + endodontics taxonomies, so likely CBCT/imaging complexity |
| 7 | Brushin' On Belmont | 2007 W Belmont Ave | Pediatric + general taxonomies; Roscoe Village cluster |
| 8 | Bristle Dental Studio | 1700 N Western Ave | NPPES updated 2024, so active; clinic/center taxonomy; Logan Square/Bucktown |
| 9 | Wicker Park Dental, Ltd | 1738 W North Ave | Clinic/center taxonomy; Wicker Park cluster |
| 10 | Lincoln Park Dental Care Ltd | 424 W Fullerton Pkwy | Long-established (2008); Lincoln Park cluster |
| 11 | Andersonville Dental | 1700 W Foster Ave | Updated 2020; pairs with #4 on a north route |
| 12 | Cusp Dental Studio PC | 3917 N Ashland Ave | Same block as #13; tests the dental + vet combined stop |
| 13 | Duke Animal Hospital | 3941 N Ashland Ave | Vet; licence valid to 2028-05 |
| 14 | North Center Animal Hospital | 1808 W Addison St | Vet; North Center cluster |
| 15 | Lincoln Square Animal Hospital | 4501 N Lincoln Ave | Vet; next to #1 |

**Data caveats:**
- **Dental phones:** the dental phone numbers in the CSV are NPPES practice-location numbers.
- **Vet contact pages:** MISSING.
- **Record age:** many NPPES records are 2008–2020 vintage [A, DD-S012]. Confirm each practice is operating and independent on the first walk.

**Named competitors:**

| Competitor | What is known | Evidence |
|---|---|---|
| Siotek | $399 flat, about 10 workstations, 4 on-site visits a year, EDR/email security as add-ons | [B, E-WS04014-S004] |
| Darkhorse Tech | $28.13/$49.93 per workstation; service areas listed do not include Chicago | [B, E-WS04014-S005] |
| FlossByte | $59–99 per device per month | [D, C6-S008] |
| Henry Schein One / Patterson technology services | Distributor and software bundlers | [B, DD-S015; B, WS04-S026] |
| CMIT Solutions Chicago | Franchise MSP | [D] |
| Local providers in a Chicago dental-IT directory | Dental Technology Services Inc. (Wauconda), Tech Direct 2 U (Chicago), NorthShore PC Service (Skokie), adNET (Elgin), The Isidore Group (Chicago) | [D, DD-S019] |
| Compliance-only software | e.g., Medcurity at $499/yr | [D, E-WS04014-S012] |
| The free HHS SRA Tool (DIY) | | [B, E-WS04014-S017] |

**Positioning.** "Your IT person who shows up, and who will sit with you when you sign the insurance and HIPAA paperwork." The contrast with remote specialists is the same-day on-site SLA inside the radius, plus the compliance documentation done *with* the practice, not left in a portal.

**Pricing (draft list; testable):**
- **Dental:** $60 per workstation per month, minimum $450, plus a $100/month HIPAA layer (annual risk analysis, policies, training log, BAA register, insurance-attestation support).
- **Vet:** $55 per workstation plus a $60 insurance-readiness layer.
- **One-time:** onboarding/remediation $1,000 (scoped in writing); stand-alone risk analysis $1,500 (introductory $750 for the first five).
- **Projects:** labour $120/hour (E); hardware at cost +10–15%.
- **Terms:** 12-month initial term, then month-to-month with 30 days' notice (market practice [B, E-WS04014-S004]).

**The realistic ceiling on price.**
- **The remote all-in comparator** for a 10-workstation office is about $500–600 per month: Siotek $399 plus EDR and email add-ons, or Darkhorse Gold at $499.
- **Siotek's own buyer guide** says a "well-staffed" provider costs $80–150 per workstation. Its example "reasonable" 8-workstation invoice is $1,401 including M365 [D, E-WS04014-S006]. That is marketing.
- **The defensible range** for a local on-site provider is therefore about **$600–900** for a 10-workstation office before M365 pass-through.
- **The model's floor:** at $441 the base year-3 operating profit falls to zero (ad hoc run of the same engine).

**Sales strategy:** founder-led, in person, inside the radius:
- Walk in with a one-page offer.
- Ask for 15 minutes with the office manager.
- Lead with a concrete, paid, low-commitment deliverable:
  - the dental risk analysis;
  - for any practice, an "insurance MFA attestation readiness check".
- Convert to monthly service after the report shows the gaps.

**Acquisition channels, in expected order of yield (E):**
1. Walk-ins on the route.
2. Equipment-dealer service technicians and independent dental equipment repairers. They see failing servers but do not want IT work.
3. Practice-transition brokers and dental CPAs, who see practice purchases (a classic IT trigger).
4. Insurance producers writing practice cyber policies, who need someone to make MFA answers true.
5. Study clubs and the Chicago Dental Society calendar (Midwinter Meeting each February; confirm 2027 dates and exhibitor costs).
6. Peer referrals from clients.

---

## 3. Transaction economics (line by line)

| # | Transaction | Revenue | Direct costs | Contribution | Cash timing | Failure risks | Repeat |
|---|---|---|---|---|---|---|---|
| T1 | 10-workstation dental practice, one month of managed IT + HIPAA layer | **$700** | Managed EDR/MDR 11 × $7 = $77 (retail $7–12, D); email security 8 × $3 = $24 (E); DNS filtering 11 × $1.50 = $16.50 (E); B2 backup 2 TB × $6.95 = $13.90 (B); compliance portal/training $15 (E); technician 6 h × $37.40 = $224.40 (C6-S026) | **$329.20 (47.0%)** | ACH autopay on the 1st, in advance; tool vendors bill monthly in arrears | Hours creep past 6/month (imaging bridges, printers); a ransomware event before backups are verified | Monthly; 12-month term; about 1%/month churn (E) |
| T2 | Stand-alone HIPAA risk analysis + policy set, 6-workstation dental practice | **$1,500** | Analyst time 10 h × $37.40 = $374; SRA Tool (free) / templates and report production $25 | **$1,101 (73.4%)** | 50% at signature, 50% at report | Price anchored by a $0 DIY tool and $499/yr software [D, E-WS04014-S012]; the founder must not overstate what the report certifies | Annual refresh; the best conversion path into T1 |
| T3 | Server replacement / new-office network | **$6,200** | Hardware at cost $3,800 (resold at $4,300); technician 16 h = $598.40; licensed low-voltage cabling subcontractor $400 (allowance, E) | **$1,401.60 (22.6%)** | 50% deposit; distributor terms assumed net-30 (MISSING; a new account may need card/prepay) | Hardware price swings; cabling scope larger than the allowance; a permit is needed for Chicago cabling [A, E-WS04014-S016] | Every 4–5 years per practice; new offices; practice purchases |
| T4 | 12-workstation vet hospital, one month of managed IT + insurance-readiness layer (no HIPAA) | **$720** | EDR 13 × $7 = $91; email 10 × $3 = $30; DNS 13 × $1.50 = $19.50; backup 3 TB × $6.95 = $20.85 (radiology images); technician 7 h × $37.40 = $261.80 | **$296.85 (41.2%)** | As T1 | Weaker compliance pull; corporate acquisition of the hospital | As T1 |

**Overhead and contribution per practice.**
- Overhead runs about $2,470/month in year 2 of the base case (insurance, RMM/PSA, vault, AI tools, vehicle, accounting, misc).
- At 32 practices, allocated overhead is about $77 per practice. T1 then contributes about **$250/month after overhead**.
- **Founder time is not costed until the first technician is hired.** That is why the base case breaks even at only 4.7 practices (month 10).

**CAC and payback.**
- Variable acquisition cost is about $150 per win, plus $400/month fixed (E).
- A T1 win pays back its acquisition cost in about one month of contribution.
- A T2 that converts to T1 is acquisition that pays for itself.

---

## 4. Validation

**Minimum viable commercial offering.** Two paid offers and one proposal, all deliverable by the founder alone:

| Offer | Price | What it includes |
|---|---|---|
| (a) Dental "Security Rule risk analysis + policy set" | $1,500 ($750 for the first five) | 2-week delivery: interview, configuration and backup review, SRA Tool-based assessment, written risk register and remediation plan, policy templates adapted to the practice. The BAA is signed first. |
| (b) "Cyber-insurance MFA attestation readiness check" (any practice, including vets) | $350 (E) | A one-visit check of each control a carrier asks about [B, E-WS04014-S007], with a written yes/no/fix list |
| (c) Monthly managed-service proposal | At list | Produced from (a) or (b) |

**Experiments, ordered by information value per dollar:**

| # | Experiment | Cost | What it proves | Success | Failure / kill |
|---|---|---|---|---|---|
| 1 | 5 referral-partner conversations: an independent dental equipment technician, a dealer service rep, a practice-transition broker, a dental CPA, an insurance producer who writes practice cyber | ~$50 (coffee, parking) | Who currently does IT for independents and what triggers a switch | ≥2 offer to introduce a practice; ≥3 name the incumbent IT model ("one-person IT guy", distributor, remote MSP) | Everyone says practices are locked into distributor IT |
| 2 | 15 discovery interviews: 12 dental office managers/owners, 3 vet managers. Past-behaviour questions only (see materials) | ~$100 (printing, parking) | Current spend, last outage, last risk analysis, who signed the cyber application | ≥8 of 12 dental practices cannot produce a risk analysis dated within 24 months; median current IT spend ≥$400/month or ≥$4k/yr of break-fix | ≥7 of 12 have a current risk analysis *and* a satisfied managed provider |
| 3 | **Paid pre-sale** of offer (a) or (b): walk into 30 practices over 3–4 weeks | ~$150 (print, mileage) | Willingness to pay a newcomer; reach to the owner dentist | **≥3 paid engagements with deposit received** (≥10% of visits) | **0–1 paid after 30 visits** |
| 4 | Price test of (c) during experiment 3: present $60/workstation + $100 next to the remote anchors | $0 | Whether the on-site premium survives | ≥2 signed LOIs for monthly service at ≥$550 | All prospects anchor below $450 |
| 5 | Free 45-minute backup/restore check for 5 practices that bought (a) or (b) | Time | Severity of pain; remediation project pipeline | ≥3 of 5 lack a tested restore or run an unsupported OS | <1 of 5 |
| 6 | Supplier qualification (founder-run, no purchases): Backblaze BAA route; EDR vendor MSP programme terms (minimums, monthly vs annual); Syncro trial length and post-January-2027 AI pricing; two broker quotes for E&O + cyber at $1M/$2M | $0 | Unit costs and insurability | EDR ≤$8 per endpoint at <20 endpoints with no minimum; E&O + cyber ≤$600/month | EDR minimums of ≥50 endpoints with no month-to-month; insurance >$1,200/month |

**Budget.**
- Stage 1, experiments 1–5: **≤ $400**.
- Insurance (≈$234–550/month, D/E) is bound **only after** the first paid engagement is agreed and before any system access.
- Attorney review of the MSA/BAA (E: $500–1,500) only after ≥2 paid engagements.

**Testable assumptions (and the measured value that would change the model):**

| Assumption | Model value (base) | Measure it by | Re-run model if |
|---|---|---|---|
| Qualified conversations per month | 12 | Visits → conversations with the decision-maker, logged weekly | <8 |
| Lead → proposal | 35% | Proposals ÷ conversations | <20% |
| Proposal → win | 25% | Signed ÷ proposals | <15% |
| ARPC | $690 | LOI prices | <$600 |
| Technician hours per practice per month | 6 | Time log on the first 3 clients for 60 days | >8 |
| Tools cost per practice | ~$146 | Vendor quotes | >$190 |
| Insurance | $550/month | Broker quotes | >$900 |
| Churn | 1%/month | Lost clients | Any loss in the first 12 months not caused by a practice sale |

**Conditions to invest more (unlock $2–10k):**
1. ≥3 paid engagements and ≥2 monthly LOIs at ≥$550.
2. Insurance quoted at ≤$900/month.
3. A workable backup BAA route.
4. One referral partner has made a real introduction.

**Conditions to abandon or pivot:**

| Outcome | Decision |
|---|---|
| 0–1 paid engagements after 30 visits *and* <2 LOIs | Abandon |
| Paid risk analyses sell but monthly LOIs anchor below $450 | Pivot to a compliance-plus-projects consultancy. It needs no hires and has a lower ceiling: WS04-021 logic, "$10k/mo" ceiling |
| Dental access is blocked but vets respond | Re-test with small human-medical practices (optometry, podiatry, physical therapy, chiropractic). They are HIPAA covered and fall outside the dental distributor channel |

---

## 5. Operations

**Lead-to-cash workflow and function classification:**

| Step | What happens | Classification |
|---|---|---|
| 1. Prospect list & route | NPPES/City licence pulls, map clusters, de-duplicate DSO brands | Automatable (scripts) / AI-assisted |
| 2. Walk-in & first conversation | Office manager, then owner dentist | **Human (founder)** |
| 3. Paid assessment / risk analysis | Interview, configuration review, SRA Tool, risk register | Human + AI-assisted (narrative drafting from structured findings) |
| 4. Proposal | Pricing calculator → proposal PDF | AI-assisted / automatable |
| 5. Contract | MSA + BAA + order form; e-signature; ACH mandate | Professional-dependent (attorney-reviewed templates), then automatable |
| 6. Onboarding (weeks 1–4) | Agent deployment, documentation, credential vault, MFA rollout, EDR, email/DNS security, backup to NAS + B2, **first verified restore**, firewall review | Human (technical) + automatable (agent push, scripts) |
| 7. Monitoring & patching | RMM alerts, patch windows | Automatable |
| 8. Tickets | PSA triage, remote fixes, on-site dispatch | AI-assisted triage; human resolution; on-site is **not automatable** |
| 9. Imaging/PM vendor coordination | Bridges, sensor drivers, PM upgrades | Human |
| 10. Monthly billing | Autopay invoice from PSA | Automatable |
| 11. Quarterly business review | Backup test evidence, patch compliance, open risks | AI-assisted report; human meeting |
| 12. Annual risk analysis + policy refresh + training | Dental: Security Rule; vet: insurance/payment-card readiness | Human + AI-assisted |
| 13. Projects | Quote, deposit, procurement, install, cabling subcontract | Human; cabling **professional-dependent** (licensed contractor [A, E-WS04014-S016]) |
| 14. Incident response | Isolate, restore, breach-assessment support | Human; legal/breach notification **professional-dependent** (practice's counsel/insurer panel) |

**Suppliers and fulfilment.**
- **Tools.** RMM/PSA (Syncro), EDR/MDR, email/DNS security and backup are self-serve subscriptions.
- **Hardware.** Bought through a distributor or retail at first. Distributor credit terms are MISSING, so assume card or prepay until an account history exists.
- **Cabling.** Subcontracted.
- **Backup.** Practice-owned B2 accounts or a BAA-signing MSP backup vendor (Correction 4).

**Support and SLA (draft):**
- **Hours:** remote help desk on business days 7am–6pm.
- **Response:** critical issues (practice cannot see patients) answered within 15 minutes; on-site within 2 hours inside the radius.
- **After-hours emergencies:** included.
- **Capacity:** one person cannot cover simultaneous on-site emergencies. Before about 10 clients, line up a vetted backup technician on hourly terms (E).

**QA:**
- A monthly restore test on every client.
- A patch-compliance report.
- An MFA coverage checklist mapped to carrier questions [B, E-WS04014-S007].
- A quarterly ticket review per endpoint, with an alert if tickets exceed 1.5 per endpoint per month.

**Exceptions:**
- **Practice sale to a DSO:** offboarding fee and clean handover, which is market practice [B, E-WS04014-S004].
- **Breach:** follow the incident runbook. The practice decides on notification with its counsel.
- **Non-payment:** suspend non-critical services after 15 days. Never hold data hostage.

**Software stack with prices** (monthly, base, at about 2 technicians):

| Tool | Cost | Evidence |
|---|---|---|
| Syncro Team | $179/technician (annual), plus 15% Chicago PPLTT if Chicago-based | [B, DD-S017; C, E-WS04014-S011] |
| Backblaze B2 | $6.95/TB | [B, DD-S018] |
| EDR/MDR | $7/endpoint (E; retail $7–12) | [D, E-WS04014-S006] |
| Email security | $3/mailbox (E) | |
| DNS filtering | $1.50/endpoint (E) | |
| Documentation/password vault | ~$120 (E) | |
| AI tools | ~$100 (E) | |
| HHS SRA Tool | Free | [B, E-WS04014-S017] |
| Accounting/e-signature/ACH | Inside the accounting and 2% variable lines (E) | |

**Legal requirements:**
- **Entity:** Illinois LLC. The filing fee was not verified.
- **BAAs:** a BAA with every covered-entity client [A, WS04-S018]. A confidentiality and data-processing agreement for vets.
- **Business-associate compliance:** the company's *own* Security Rule programme, because it is a business associate: its own risk analysis, policies, training and backup plan [A, E-WS04014-S020].
- **Subcontractor BAAs** with any vendor touching ePHI.
- **Tax:**
  - Illinois sales/use tax registration for hardware resale (not verified; confirm).
  - Chicago PPLTT exposure on cloud components [C, E-WS04014-S011].
- **Cabling:** licensed low-voltage subcontractor in Chicago [A, E-WS04014-S016].
- **BIPA:** do not deploy biometric timeclocks or fingerprint logins at clients without counsel (statute not re-verified).
- **Illinois data-breach law (PIPA):** applies to vets' and dentists' client data. Not re-verified; the ILGA site was unavailable on 2026-11-28.
- **Insurance referrals:** do not accept commissions from insurance producers without an Illinois producer licence. The founder has none; confirm the rule.

**Financial administration:**
- Monthly close.
- ACH autopay collection: DSO is −10 days in the model, i.e. prepaid.
- Hardware deposits held separately.
- 1099s for subcontractors.
- Quarterly estimated taxes. The model uses a 30% blended rate on profit after draw.
- Keep a 2–3-month cash reserve once profitable (model `reserve_months` 2 base, 3 conservative).

**Post-December-2026 AI cost and fallback:**
- **Where AI is used:** drafting risk-analysis narratives and policies from structured findings, ticket summaries, QBR reports and prospect research.
- **Costs:** Syncro's AI features become usage-based after January 2027 [B, DD-S017]. The model carries $100/month of AI tools inside the "is_ai" software lines.
- **Stress test:** multiplying all software/AI lines ×3 cuts base year-3 operating profit to **$47,955**.
- **Fallback:** a fixed template library (built this week while heavy AI access lasts) plus about 2 extra human hours per risk analysis. Nothing in delivery *requires* AI.

---

## 6. Growth

**First 10 customers (months 1–15 in base).** Base ends year 1 with 6.8 practices and reaches 10 in month 15.
- **Sources:** experiment-3 conversions, walk-ins on the 15-prospect route, then the next 20 NPPES/licence names, and 1–2 referral-partner introductions.
- **The rule:** no client outside the radius, so the on-site promise stays cheap.

**First 100.** Base reaches 57.2 practices at month 60; optimistic reaches 124.6. To get there:
- referrals (1 per 100 active per month, E);
- study clubs;
- one Chicago Dental Society presence per year;
- broker/CPA practice-purchase introductions;
- a **second radius** in central DuPage once about 40 practices fill the first.

At 100+ the business is two or three dense pods, not one sprawling territory.

**Hiring sequence (base model months):**

| Hire | Trigger | Month | Cost | Productivity | Why it is justified |
|---|---|---|---|---|---|
| Field/remote technician #1 | 14 practices | **20** | $6,500/month loaded (IL median $59,860 ×1.3 [C, C6-S026]) | ~28 practices (E) | Frees about 85 hours/month of founder time for selling. The model shows month-20 operating profit falling to −$884, and cash bottoms at $92 in month 27. |
| Technician #2 | 42 practices | **47** | $6,500/month | ~28 practices | Pod capacity |
| Service coordinator / dispatcher | Monthly revenue ≥ $40k | **54** | $4,200/month | Scheduling, billing, onboarding paperwork | Removes founder admin |
| Senior systems/network engineer | 70 practices | Not reached by month 60 in base (month 40 in optimistic) | $8,500/month | Projects, imaging servers, firewalls; can become service manager | Lets the founder stop L3 work |

**Capacity limits:**
- The founder as sole technician covers about 14 practices, plus 8–10 hours a week of selling.
- A technician covers about 28 practices (E; measure in validation).
- On-site radius is about 5 miles per pod.
- Emergency coverage requires ≥2 technicians before an SLA can be guaranteed (E).

**Geographic expansion:**
1. North Side pod.
2. Central DuPage pod (362 dental sites [A, DD-S012]).
3. Possibly North Shore or western suburbs.

Each pod needs one technician and a local referral base. Do not chase single remote practices.

**Adjacent products** (SYN-002 adjacency logic: keep only lines that share data, access and competence):
- **Keep:**
  - The compliance layer (absorbed).
  - VoIP/phone management (Siotek includes it in custom tiers [B, E-WS04014-S004]).
  - Practice-purchase IT due diligence for buyers and brokers (project revenue).
  - Optional insurance verification as a partner service (WS04-011: SYN-002 estimated about +$15k year-3 at 20% attach, E).
  - Expansion into small *human-medical* HIPAA practices.
- **Refer only:**
  - Medical-waste pickup (a self-performed route loses money below about 150 customers).
  - Spore testing (a commodity at $229.99 per 52 tests) [SYN-002; B, C6-S013].
  - Cyber insurance (no producer licence).

**Vertical integration (incremental return logic):**
- **Leasing:** hardware-as-a-service leasing ties up capital at finance-company returns. Skip.
- **Own backup appliance (BDR):** a standard local recovery appliance (Darkhorse sells one at +$99/month [B, E-WS04014-S005]) adds about $60–80 of margin per practice for about $1,000 of hardware per site. That is a 1–1.5-year payback. Do it after 20 practices.
- **Cabling crew:** bringing cabling in-house requires a Chicago low-voltage contractor licence and a supervising electrician [A]. Only worth it above roughly 30 projects a year (E).

**Management delegation.**
- **When a manager can run day-to-day:** at about 70 practices, a senior engineer or service manager can run delivery with two technicians and a coordinator.
- **What stays with the founder:** sales and key referral relationships until a second pod exists.
- **When it becomes realistic:** about years 5–7 in base.

**Reinvestment slots, ranked:**
1. Fill the first pod (highest return; founder time).
2. A BDR appliance programme.
3. A second-pod technician (~$40k ramp; incremental ROIC about 1.0x in base, E).
4. Tuck-in purchase of a 10–30-client local dental IT book from a retiring "one-person IT guy". Small MSPs trade at about 3.4x SDE (<50% recurring) to about 5.4x (≥70% recurring) [D, E-WS04014-S015]. This is allowed later as capital allocation, not as entry.

---

## 7. Financial analysis (rebuilt model: `08_financial_models/WS04-014_model.xlsx` / `_results.json`)

**Standardised settings:**
- Founder draw $4,000/month from month 13 in all scenarios.
- Tax 30%.
- **Start capital injection $42,500**: the base peak funding of $42,408, rounded up to $500. It leaves a minimum base cash balance of $92 in month 27.

**Launch capital and working capital:**
- **Capex:** $5,000 in month 1 (bench equipment, spare firewall/NAS, laptop, test imaging workstation; $7,000 conservative), plus $3,000 per technician hire.
- **Working capital is negative,** because practices pay in advance. The base change in NWC is −$3,004 in year 1 and −$5,243 in year 5, i.e. cash *released*.
- **Hardware deposits** cover project exposure if 50% is collected at order.

**24-month monthly view (base).** Same engine as the workbook; operating profit is before owner draw.

| Month | New | Active | Revenue | Op. profit | Draw | Retained | Cash |
|---|---|---|---|---|---|---|---|
| 1 | 0.00 | 0.0 | $0 | −$2,782 | $0 | −$7,782 | $34,718 |
| 2 | 0.00 | 0.0 | $0 | −$2,782 | $0 | −$2,782 | $31,936 |
| 3 | 0.00 | 0.0 | $0 | −$2,782 | $0 | −$2,782 | $29,154 |
| 4 | 0.17 | 0.2 | $296 | −$2,640 | $0 | −$2,460 | $26,694 |
| 5 | 0.35 | 0.5 | $714 | −$2,405 | $0 | −$2,167 | $24,527 |
| 6 | 0.53 | 1.0 | $1,255 | −$2,076 | $0 | −$1,779 | $22,748 |
| 7 | 0.71 | 1.7 | $1,918 | −$1,653 | $0 | −$1,298 | $21,449 |
| 8 | 0.89 | 2.6 | $2,704 | −$1,137 | $0 | −$724 | $20,725 |
| 9 | 1.08 | 3.7 | $3,612 | −$528 | $0 | −$57 | $20,669 |
| 10 | 1.09 | 4.7 | $4,347 | $33 | $0 | $383 | $21,051 |
| 11 | 1.10 | 5.8 | $5,082 | $593 | $0 | $944 | $21,995 |
| 12 | 1.11 | 6.8 | $5,817 | $1,154 | $0 | $1,505 | $23,500 |
| 13 | 1.12 | 7.9 | $6,749 | $1,767 | $4,000 | −$1,782 | $21,718 |
| 14 | 1.13 | 8.9 | $7,506 | $2,345 | $4,000 | −$1,294 | $20,423 |
| 15 | 1.14 | 10.0 | $8,263 | $2,922 | $4,000 | −$717 | $19,707 |
| 16 | 1.15 | 11.0 | $9,020 | $3,500 | $4,000 | −$139 | $19,567 |
| 17 | 1.16 | 12.1 | $9,777 | $4,078 | $4,000 | $439 | $20,006 |
| 18 | 1.17 | 13.1 | $10,534 | $4,655 | $4,000 | $1,016 | $21,022 |
| 19 | 1.18 | 14.2 | $11,291 | $5,233 | $4,000 | $1,594 | $22,616 |
| 20 | 1.19 | 15.2 | $12,048 | −$884 | $4,000 | −$7,523 | $15,093 |
| 21 | 1.20 | 16.3 | $12,805 | −$307 | $4,000 | −$3,946 | $11,147 |
| 22 | 1.21 | 17.3 | $13,562 | $271 | $4,000 | −$3,368 | $7,779 |
| 23 | 1.22 | 18.4 | $14,319 | $849 | $4,000 | −$2,790 | $4,989 |
| 24 | 1.23 | 19.4 | $15,076 | $1,427 | $4,000 | −$2,213 | $2,776 |

**5-year annual (from `_results.json`).**

*Base:*

| | Y1 | Y2 | Y3 | Y4 | Y5 |
|---|---|---|---|---|---|
| Revenue | $25,744 | $130,948 | $247,162 | $370,231 | $500,462 |
| Operating profit | −$17,005 | $25,857 | $64,047 | $140,020 | $128,878 |
| FCF (before draw) | −$19,000 | $27,276 | $68,729 | $121,301 | $109,857 |
| Draw | $0 | $48,000 | $48,000 | $48,000 | $48,000 |
| Retained | −$19,000 | −$20,724 | $20,729 | $73,301 | $61,857 |
| Practices (year-end) | 6.8 | 19.4 | 32.0 | 44.6 | 57.2 |
| Staff (year-end) | 0 | 1 | 1 | 2 | 3 |

- Year-5 operating profit dips below year 4 because technician #2 (month 47) and the coordinator (month 54) are added before they are filled.

*Conservative:*

| | Y1 | Y2 | Y3 | Y4 | Y5 |
|---|---|---|---|---|---|
| Revenue | $6,571 | $41,272 | $77,593 | $111,950 | $144,551 |
| Operating profit | −$34,013 | −$12,096 | $12,175 | −$33,841 | −$38,018 |
| Practices (year-end) | 2.7 | 8.1 | 12.9 | 17.2 | 21.0 |

- The first technician arrives in month 40 at 14 practices paying $540, so the business loses money from then on.
- **Peak funding: $307,555** with the draw, or $115,555 without it.

*Optimistic:*

| | Y1 | Y2 | Y3 | Y4 | Y5 |
|---|---|---|---|---|---|
| Operating profit | $22,759 | $149,707 | $268,828 | $372,349 | $553,295 |
| Practices (year-end) | 13.8 | 37.7 | 63.9 | 92.8 | 124.6 |

- Peak funding is $11,272.
- **Caution:** the optimistic case implies about a 40% operating margin on $1.37M of revenue with the founder still unpaid for management, and about 125 practices. Treat it as an upper bound, not a plan.

**Breakeven and milestones:**

| Milestone | Base | Conservative | Optimistic |
|---|---|---|---|
| First month of positive operating profit | 10 | 25 | 6 |
| ≥$1k/month | 12 | 31 | 7 |
| ≥$5k/month | 19 | Never | 10 |
| ≥$10k/month | 38 | Never | 13 |
| ≥$25k/month | Never within 60 months | Never | 34 |
| Cumulative-cash payback | 39 | Never | 9 |

- In base, ≥$5k/month first appears in month 19, is interrupted by the month-20 hire, and recurs from month 30.

**Sensitivity (±25%, effect on base year-3 operating profit):**

| Driver | Low (−25%) | High (+25%) |
|---|---|---|
| Win rate / founder leads (identical effect) | $18,463 | $109,631 |
| Gross margin | $18,506 | $109,588 |
| ARPC | $19,659 | $108,435 |
| Labour cost (−25% / +25%) | $84,734 | $43,359 |
| Overhead | $69,720 | $58,374 |
| Churn | $69,645 | $58,670 |

- **The business is a volume-and-price machine.** Selling capacity, win rate and price matter about four times more than churn.
- **Ad hoc runs** (same engine, not in `_results.json`):
  - ARPC $600 → year 3 $40,888, peak $64,893.
  - ARPC $550 → year 3 $28,022, peak $80,694.

**Stress tests (base, from `_results.json`):**

| Test | Year-3 operating profit | Year-5 operating profit | Peak funding |
|---|---|---|---|
| Win rate −40% | $18,696 | $99,588 | $86,913 |
| Recession (new customers −30%, churn ×1.5) | $18,325 | $92,393 | $77,672 |
| Growth twice as slow | $40,547 | $31,840 | $137,493 |
| Hires needed 30% sooner | $50,255 | −$12,937 | $139,617 |
| Gross margin −10 points | $39,331 | — | $65,276 |
| Labour +20% | $47,497 | $87,144 | — |
| Competitor response | $41,103 | — | $52,028 |
| Key supplier refuses | $31,670 | — | $73,327 |
| 25% of base lost in month 18 | $43,517 | — | — |
| AI/software ×3 | $47,955 | — | — |
| Insurance/overhead +50% | $52,700 | — | $67,512 |

- Year-3 operating profit stays positive in every base stress.
- **The two that break the business are over-hiring and slow growth.** Both are controllable by hiring to density, not to plan.

**Capital accumulation to year 10 (base):**

| Measure | Value |
|---|---|
| Cumulative deployable surplus by year 5 (after draw, tax, reinvestment and reserves) | $111,471 |
| Cumulative deployable surplus by year 10 | $386,875 |
| Year-10 operating profit | $184,195 |
| Year-10 EV at 3.5× (the multiple applies to profit before owner pay; small MSPs trade at about 3–4× EBITDA [C, E-WS04014-S014] and 3.4–5.4× SDE [D, E-WS04014-S015]) | $644,684 |
| Cumulative owner stipend over 10 years | $454,484 |
| Model "owner wealth" at year 10 | $1,486,042 |

- **Conservative:** zero deployable; year-10 operating profit −$41,281.
- **Optimistic:** $2,885,001 deployable; year-10 operating profit $986,926.

**Owner distributions.**
- In base, the owner takes $48k a year from year 2.
- Distributable surplus above that begins in year 3: $7,725 deployable, then $65,451 in year 4.

**Downside cases.** The honest downside is not bankruptcy but a job: a founder-technician earning a $4k/month stipend for two years while working 55–60 hours a week.

An ad hoc conservative run in which the founder never hires shows:
- Year-5 operating profit $56,525 with 21 practices.
- Peak funding $149,769 once the draw is counted.

That is a self-employed technician earning less than the founder's likely market salary.

---

## 8. Capital deployment ladder

| Tranche | What it buys | Evidence gate before spending | How it could be lost |
|---|---|---|---|
| **$0–500** | One-pager printing, mileage/parking, coffees for 5 partner chats, the free SRA Tool, Claude-built templates | None. Start next week | Time only; at worst ~$400 |
| **$500–2k** | Illinois LLC; tech E&O + cyber + GL first premiums (median ~$234/month IT-consultant baseline [D], likely higher); domain/email/M365 for the business; e-signature | **≥1 paid engagement with deposit** and a BAA ready to sign | Insurance prepaid with no further sales |
| **$2–5k** | Attorney review of MSA/BAA/SOW (E $500–1,500); Syncro (annual $179×12 = $2,148 or monthly); EDR/backup for the first clients | **≥3 paid engagements; ≥2 monthly LOIs ≥$550**; insurance quoted ≤$900/month | Annual tool commitments stranded if LOIs do not sign |
| **$5–10k** | Bench equipment, spare firewall/NAS, test imaging workstation (model capex $5,000); 3 months of overhead runway (~$7k) | **First 3 monthly clients live with verified restores**; ≥5 proposals outstanding | Gear idle; a client incident during onboarding (the $50k pre-mortem) |
| **$10–25k** | Carrying the founder's stipend from month 13 while profit < draw (base retained is negative months 13–16 and 20–27); CDS presence; BDR appliances (practice-paid) | **10 practices, MRR ≥$6.5k, zero non-sale churn, ≤1.5 tickets per endpoint per month** | Drawing a stipend the business cannot yet fund; sales stall |
| **$25–50k** | First technician ramp: $6,500/month × 4–6 under-utilised months, plus $3,000 capex; vehicle share. **The base peak of $42,408 sits here (cash low in month 27)** | **14 practices; pipeline ≥1 win/month for 3 consecutive months; founder >50 technical hours/week** | Hiring before density. "Hires 30% sooner" turns year-5 operating profit negative (−$12,937) |
| **$50–100k** | Second pod (DuPage) technician ramp, or a tuck-in purchase of a 10–30-client dental IT book at ~3–5× SDE [D, E-WS04014-S015] | **~40 practices, run-rate ≥$8k/month operating profit, documented SOPs, churn ≤1%/month, 12 months of restore-test evidence** | Overpaying for a book that churns; second pod without referral base |

**Do not put more than $50k at risk before the first pod is profitable after the technician hire.** The conservative case shows how a mechanical plan turns into $300k of losses.

---

## 9. Strategic wealth creation

**How it becomes a durable cash asset:**
- Contracts are recurring, prepaid and documented.
- Route density lowers the cost of service.
- Documentation lock-in (credential vaults, network diagrams, risk-analysis history) raises switching costs.
- Relationships with dealers and brokers keep supplying triggered buyers (outages, purchases, new offices).
- Cash conversion is better than profit: FCF before draw exceeds operating profit in year 3 ($68,729 vs $64,047) because clients prepay.

**How much capital it could generate.**
- **Base:** about $40–70k a year of deployable surplus in years 6–10, $386,875 cumulative by year 10, plus a saleable book worth about $645k at 3.5×.
- **Optimistic:** about $0.3–0.5M a year.
- **Conservative:** nothing.

**When management could take over.**
- At about 70 practices: a senior engineer as service manager, two technicians and a coordinator.
- In base that is beyond month 60 (years 6–7). In optimistic it is month 40.
- Sales stay founder-led until a second pod exists.

**Can it fund other ventures?** Modestly, and late. It is better at *not consuming* capital than at producing it.
- **Capital needed:** peak funding is $21,831 with no draw.
- **What it produces:** a steady cash floor and a credible operating track record, which help a later holding company borrow or acquire.

**Is it a strong first company for a diversified portfolio?**

*For:*
- Very low capital at risk.
- A paid test for a few hundred dollars.
- Prepaid recurring revenue.
- Standard delegable roles.
- Mandated documentation work (the risk analysis is required by the Security Rule in force [A, E-WS04014-S020]).
- Slow consolidation of Illinois dentistry.

*Against:*
- **Ceiling.** One pod supports roughly $150–250k a year of operating profit. Pods need about 28 practices per technician, so $250k needs about 115–120 practices; $500k needs about 185–225 practices plus a paid manager.
- **Price.** Price is capped by remote rivals at about $500–600 all-in for a 10-workstation office.
- **Founder time.** The first two years are founder-as-technician.
- **Platform threat.** Henry Schein One and cloud practice-management software are long-run threats.

*Verdict:* a strong **first** company for a founder who wants low-risk compounding and is comfortable being a technician-salesperson for two years. It is weak as the *only* engine of a holding company.

---

## 10. Execution plan

**First 7 days (Nov 29 – Dec 5, 2026, the last week of heavy AI access).**

*Claude prepares now:*
- The full template library: risk-analysis report skeleton, a 30-policy Security Rule policy set for a dental office, MSA/BAA/SOW drafts for attorney review, onboarding runbook, restore-test log, QBR template.
- A pricing calculator.
- A route map of the 35 prospects.
- The KPI sheet.
- The interview guide and scripts (see `WS04-014_materials.md`).

*The founder:*
1. Reads this playbook and the materials.
2. Walks the Lakeview–North Center–Lincoln Square route once without pitching, noting which practices are open, branded or DSO-signed.
3. Books 2–3 referral-partner coffees: an independent dental equipment repair technician, a practice-transition broker, a dental CPA.
4. Downloads the SRA Tool v3.7 and completes a mock assessment of a fictional practice.

*Spend:* ≤$100.

**Seasonality (E).** December is a heavy production month for dental offices (patients use annual insurance benefits before they reset). Use December for partner conversations and interviews by appointment, and do the bulk of walk-ins in January.

**First 30 days (by about Jan 4–15, 2027):**
- **Founder:**
  - 15 discovery interviews.
  - 5 referral-partner conversations.
  - Start experiment 3: 30 walk-ins with the paid offers.
- **Organisations to approach** (no contact made by Claude):
  - The 15 prospects above, then the remaining 20 in the CSV.
  - Chicago Dental Society (membership/exhibitor terms; Midwinter Meeting).
  - The Chicago Veterinary Medical Association.
  - Local branches of Henry Schein Dental, Patterson Dental and Benco Dental: their service technicians, as referral sources and to learn their IT offer.
  - Two insurance brokers writing practice cyber.
- **Questions to ask:**
  - Who does your IT and what did you pay last year?
  - When did your last outage happen, and what did it cost?
  - When was your last risk analysis, and who did it?
  - Who signed your cyber-insurance application, and how did you answer the MFA questions?
- **Evidence required:** a paid deposit, an LOI, or a written introduction. Opinions do not count.
- **Proposed spend:** ≤$400.
- **Accept a first order when:**
  - the scope is a risk analysis or readiness check;
  - a BAA is signed;
  - 50% is paid upfront;
  - insurance can be bound before any system access.
- **Abandon/pivot** per §4 if 0–1 paid engagements come from 30 visits.

**First 90 days (to about end of February 2027):**
- **Targets:**
  - 3–6 paid assessments delivered.
  - 2–4 monthly LOIs.
  - The first 1–3 monthly clients onboarded, each with a verified restore within 30 days.
- **Setup:** LLC formed, insurance bound, MSA/BAA reviewed by an attorney, Syncro and EDR live, two vetted backup technicians on call.
- **Measure:** hours per practice and tickets per endpoint from day 1.
- **Re-run the model** with measured conversion and hours.
- **If ARPC <$600 or hours >8/month, stop and re-price** before adding clients.

**First year (to December 2027):**
- **Base milestones:** about 7 practices and MRR about $4.7k by month 12; first month of positive operating profit at month 10; year-1 operating profit −$17,005.
- **Before month 13:** decide whether the business can carry the $4k/month stipend. It cannot fully until about month 17.
- **Slow-growth branch** (<4 practices by month 9):
  - Stay a solo compliance-plus-projects practice with no hires.
  - Add small human-medical HIPAA practices.
  - Or move the pod to central DuPage.
- **Failure branch:** <2 monthly clients by month 9, or a client security incident traced to an onboarding gap. Wind down: hand over documentation cleanly and stop insurance at renewal.

---

## 11. Pre-mortem

| Scenario | What happened | Early warning | Cheap preventive test |
|---|---|---|---|
| **Lost $5k** | Insurance bound, tools bought, LLC formed; 30 walk-ins gave 1 paid analysis; the founder quit | "Our IT guy handles it"; the owner is never available; LOIs below $450 | Do not bind insurance or buy tools before experiment 3 passes |
| **Lost $25k** | 8–10 practices won; on-site time ran to 10+ h/practice/month; the first technician made the business loss-making while the stipend ran | Tickets >1.5 per endpoint per month; unbilled project hours; imaging bridges failing weekly | Time-log the first 3 clients for 60 days; set onboarding remediation as paid scope |
| **Lost $50k** | A ransomware event at a client during onboarding, before backups were verified; claim, lost referrals, insurer dispute over MFA answers | Any client without a tested restore after 30 days; MFA exceptions "temporarily" allowed | No monthly contract starts until restore + MFA are done; insurance-attestation checklist signed by the client |
| **Revenue but no profit** | Price conceded to $450–550 to beat remote rivals; each technician covers only about 20 practices | LOI prices clustering near $500; discounts requested on 3 of 5 proposals | Walk away below $550; sell the on-site SLA explicitly |
| **Exhausting low-paid job** | The founder does sales + help desk + projects at 60 h/week for $48k/yr through year 3 (base) | Response-time slips; selling hours <5/week | Hire at density, not exhaustion; keep a backup technician on hourly call |
| **Cash crunch** | The technician hired at month 20 while the stipend runs; cash fell to $92 in month 27 (base) | Fewer than 1 win/month in the 3 months before hire | Hire only with 6 months of technician cost in reserve or 18+ practices |
| **Can't run without founder** | All client relationships and L3 knowledge sit with the founder | No SOPs; the technician escalates everything | Document every onboarding in the vault from client #1; senior engineer at about 70 practices |
| **No deployable surplus** | The business plateaus at about 20 practices (conservative path) | Net adds <0.6/month after month 12 | The month-9 and month-18 gates; pivot to compliance consultancy or DuPage |

---

## 12. Required confirmations (direct, before money is at risk)

**Supplier:**
1. Will Backblaze sign a BAA with an MSP as subcontractor, or only with the practice? If only the practice, confirm the practice-owned-account workflow [B, E-WS04014-S013].
2. EDR/MDR vendor (e.g., Huntress) MSP programme: per-endpoint price, monthly minimums, BAA.
3. Email-security vendor terms and BAA.
4. Syncro trial length, current price, and post-January-2027 AI usage pricing [B, DD-S017].
5. Distributor credit terms for hardware.
6. M365 CSP route and margin.

**Customer:**
7. Whether each top-15 practice is independent, operating, and under an IT contract (and when it expires).
8. Actual current IT spend.
9. Who signs the cyber application.
10. Whether owners will pay a premium for on-site over the remote all-in of about $500–600.

**Regulatory/tax:**
11. Chicago PPLTT treatment of a bundled managed-service fee and of resold cloud tools; registration duty [C, E-WS04014-S011].
12. Illinois sales/use tax on hardware resale.
13. Illinois PIPA duties for vet/dental client data (not re-verified).
14. Illinois veterinary record-confidentiality rules.
15. That the founder may not accept insurance referral fees without a producer licence.
16. Suburban (DuPage) low-voltage cabling rules.
17. HIPAA Security Rule rulemaking status at each quarterly review [A, E-WS04014-S001, S002].

**Insurance:**
18. Bound quotes for tech E&O + cyber + GL at $1M/$2M limits for an MSP with healthcare clients, and the underwriting control requirements on the MSP itself (MFA on all admin access, including the RMM).
19. The contractual liability limits practices will ask for in BAAs.

**Model inputs to replace with measurements:**
- Technician hours per practice.
- Conversion rates.
- Tools cost per practice.
- Insurance premium.
