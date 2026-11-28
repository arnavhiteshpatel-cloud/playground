# WS04-010 — Specialty billing/RCM for independent pediatric therapy clinics (Illinois Medicaid MCOs + commercial) · Stage D deep dive

> **Verdict: DROP** (keep the findings for any later healthcare-services bundle) · evidence level **D** (up from E) · revised raw score 5.00, evidence-adjusted 5.00.
>
> **The decisive fact.** The unit economics are bound by labor, and price is capped by platforms that bundle billing into their software:
> - **Revenue per client:** a 5-clinician pediatric clinic collecting about $420k a year pays about **$2,400 a month**, at roughly 6.8% blended.
> - **Labor per client:** one experienced biller (about $68k loaded [C, C6-S027]) can serve about 4 such clinics. That leaves about **$780–815 a month of contribution per client** before coordination, QA and overhead.
> - **Base-case result:** operating profit is about **$24k in year 3** and stays flat to year 5 ($25k) as headcount grows step by step. In the stress test, *losing* win rate *raises* profit, which shows that each extra client adds almost nothing.
> - **The price ceiling:** EHR vendors publish managed billing at **3.9% + per-provider fees** (Carepatron [B, DD-S022]) and **4–6%** (SPRY pediatric [D, DD-S024]). CentralReach bundles billing for ABA [C6-S037].
> - **The one real upside:** if AI-assisted workflows let one biller serve about 6 clinics, base year 3 rises to about **$109k**. That is an unproven productivity claim, not evidence.

## 1. Specific initial niche

**The customer.** Independent pediatric outpatient therapy clinics:
- Speech-language pathology, occupational therapy and physical therapy, often combined with developmental therapy or ABA.
- 3–10 clinicians each.
- Located in Cook, DuPage and Lake counties.
- Billing both commercial plans (BCBSIL and others) and the five HealthChoice Illinois Medicaid MCOs: Aetna Better Health, Blue Cross Community Health Plans, Molina, Meridian/YouthCare, and CountyCare (Cook only) [A, DD-S026].

**Why this niche looks underserved:**
- **Payer complexity:** five MCO rule sets, plus HFS fee-for-service, plus commercial plans.
- **Pediatric denial drivers:** authorisation lapses when several disciplines treat the same child, Medicaid payer-of-last-resort sequencing, and EPSDT rules [D, DD-S024].
- **The opening trigger is dated.** CPT 92507, the core speech-treatment code, is **deleted on 1 January 2027**. Ten time-based codes replace it (base 30 minutes plus 15-minute add-ons). Medicare finalised values, but Medicaid and commercial implementation is unaddressed and may vary [C, DD-S028]. Every SLP clinic faces a recoding and denial spike in Q1 2027.
- **Software gap:** ABA billing is bundled in CentralReach. Adult PT is served by WebPT and SPRY. Mixed pediatric clinics run on Fusion (Ensora), TheraPlatform, SimplePractice and similar systems, whose billing is mostly self-serve [B, DD-S025; D, DD-S024].

**Base size:** NPPES shows **205 organisation NPIs in Chicagoland with both speech and occupational-therapy taxonomies** [A, DD-S030]. Illinois PT/OT/speech establishments rose 26% from 2019 to 2023, to 2,545 [C, C6-S003].

## 2. Named operators

| Operator | What is known | Level |
|---|---|---|
| TheraThink | Mental-health billing at 6.5–8% of allowed amount. No setup fee; $35/month clearinghouse pass-through; credentialing $120–260 per application; month-to-month | B, DD-S021 |
| Carepatron | EHR with managed billing at 3.9% of collections + $79–99/provider/month + $0.25/claim. Credentialing for up to 5 payers included | B, DD-S022 |
| SPRY | PT/OT/SLP EHR (from $79/month) plus managed RCM at 4–6% of collections. Vendor estimate for an in-house biller: $55–73k/year | D, DD-S023, DD-S024 |
| CentralReach (BillMax) | ABA platform with about 4,000 practices; sells managed billing inside the software | C/B, C6-S036, C6-S037 |
| SimplePractice | Self-serve claim tools; paid "Claim Assistant" upgrade; no managed billing service described | B, DD-S025 |
| R1 RCM | $2.25B revenue, about 27% adjusted EBITDA. Hospital-enterprise incumbent | B, WS04-S011 |
| Illinois micro-billing firms | 1,759 Illinois establishments under NAICS 541219, 77% with fewer than 5 employees. No named Illinois pediatric-therapy specialist with published prices was found | C, C6-S003; MISSING |

**Market fee ranges (vendor-stated, D):**
- 4–9% of collections [DD-S023].
- 4–10%, most 5–7% [DD-S022].
- $1–10 per claim.

**Incumbent vs. new-entrant economics:** incumbents spread offshore labor and software across thousands of clinics. A new entrant pays U.S. biller wages and has no track record.

## 3. Suppliers and partners

The full list is in `09_databases/suppliers/WS04-010_suppliers.csv`.

**Documented:**
- **Claim.MD clearinghouse:** Unlimited plan $120/month per tax ID; Small Volume $60; Basic $30 + per-transaction fees; no setup fee listed [B, DD-S029].
- **HFS practitioner fee schedule, effective 10/1/2026** [A, DD-S027]:
  - 92507: $50.81
  - 92523 (evaluation): $151.80
  - 97530: $23.99 per unit
  - 97110: $19.41 per unit
  - A separate column applies a 2.7% reduction to non-excluded provider types.
- **HealthChoice Illinois MCO list** [A, DD-S026].
- **Federal fee rules:** 42 CFR 424.73 for Medicare [A, WS04-S012] and 42 CFR 447.10 for Medicaid [A, C6-S035]. Both prohibit percentage fees when the billing agent receives the payment.

**Assumed — requires direct confirmation:**
- Office Ally, Availity and the MCO portals.
- AAPC Certified Professional Biller course (cost MISSING).
- HFS rules on billing-agent registration (MISSING).

## 4. Named prospective customers

The CSV lists **31 clinics**, all "prospect — not contacted":

| County | Clinics |
|---|---|
| Cook (Chicago) | Chicago Kids Therapy, Chicago Pediatric Therapy & Wellness Center, Pediatric Therapy Network, PediaSource Therapy Specialists, Kids On The Grow, Playworks Therapy, Sensable Kids, Blossom Therapy, Lumiere Children's Therapy |
| Cook (north and west suburbs) | Achieve Pediatric Therapy (Lincolnwood), Timber Ridge Pediatric Therapy (Skokie), Milestones Pediatric Therapy (Northbrook), North Shore Pediatric Therapy and Little Steps Pediatric PT (Glenview), KidsConnect, M Street and Kids Unlimited (Oak Park), Momentum Pediatric Therapy (Bartlett) |
| Lake | Kids Therapy Ltd. and Building Block Pediatric Therapies (Libertyville), TheraPediatrics (Vernon Hills), Pathways Pediatric Therapy (Buffalo Grove) |
| DuPage | Kids Count and Tiny Steps (Elmhurst), PediaProgress and Therapeutic Strategies (Downers Grove), Right Start and Spot On Therapies (Naperville), Apex Pediatric Therapy (Lisle), Hummingbird (Westmont), Color Along (Hinsdale) |

**Data caveats:**
- **Missing details:** clinician counts, payer participation and current billing arrangements are all MISSING.
- **Early Intervention:** several clinics are also EI provider agencies, and that work is billed through the state's central billing office, which shrinks the addressable volume (E).

## 5. Representative transactions

| Transaction | Revenue | Direct costs | Contribution | Timing |
|---|---|---|---|---|
| 5-clinician clinic, one month (about $35k collections) | $2,400 | Biller 0.25 FTE = $1,425; clearinghouse $120; statements $40 | **$815 (34%)** | Invoiced early the next month, net 15 or auto-debit |
| Medicaid MCO claim batch: 250 claims at a $5 flat fee | $1,250 | Biller 250 × 6 min × $32.50/hour = $813 | **$438 (35%)** | Monthly |
| Onboarding: credentialing 4 payers + aged A/R recovery | $1,500 | Coordinator 14 hours = $388; biller 8 hours = $260 | **$852 (57%)** | 50% upfront |

**Derivation of the base revenue (A/B/E):**
- Volume: 5 clinicians × 1,200 billed visits a year (E).
- Blended collection per visit, about $70:
  - Medicaid 92507 pays $49.44 after the 2.7% cut [A].
  - Commercial is assumed at $85–100 (E; BCBSIL rates MISSING).
- That gives about $420k in collections. The fee is 6.5% of commercial collections (inside TheraThink's 6.5–8% [B]) plus $5 per Medicaid claim. Flat per-claim pricing on Medicaid follows 42 CFR 447.10.

## 6. Customer acquisition

**Client #1:** a free "2027 code-change readiness and denial audit" for the 31 prospects (A/R aging, denial reasons, authorisation tracking), delivered by Q1 2027. Convert at the first painful denial cycle.

**Clients #2–10:**
- Referrals between therapist-owners.
- ISHA and IOTA chapters.
- Practice consultants.
- EHR partner listings.

**Clients #11–100:** content on MCO-specific denial fixes, and owner-to-owner referrals.

**Funnel (E):** 10 qualified conversations a month → 30% audit → 20% win, about **0.6 clients a month**. Referrals add about 1.5 per 100 active clients.

**Weekly founder time:** about 10 hours of selling, plus heavy QA of billing until a lead biller is proven.

**CAC and lifetime value:**
- CAC is about $250 variable plus $300/month fixed, roughly **$750 per client** plus founder time.
- At 1.2% monthly churn, lifetime contribution looks large (about $65k at $780/month). But coordination and QA staff absorb most of it, so the realised contribution is about $300/month at scale.

## 7. Pricing strategy

| Element | Price |
|---|---|
| Commercial collections | 6.5% |
| Medicaid and MCO claims | $5 per claim (flat) |
| Monthly minimum | $750 |
| Credentialing | $150 per application |
| A/R recovery | Fixed project fee |

**Market evidence:**
- TheraThink: 6.5–8% [B].
- Carepatron: 3.9% + $79–99/provider + $0.25/claim [B].
- SPRY pediatric: 4–6% [D].
- Vendor ranges: 4–10% and $1–10 per claim [D].

A rate below 4% "often signals a basic, automated, or offshore service" [D, DD-S022]. In other words, a newcomer must justify 6.5% against cheaper bundled options. Year-3 operating profit falls to **−$77k** if the price is 25% lower (tornado).

## 8. Working capital and cash conversion

Fees are invoiced monthly in arrears on the prior month's collections. Base DSO is 25 days. Billers are paid biweekly.

| Clients | Monthly revenue | Receivables (DSO 25) | Accrued payroll offset (about ½ month) | Net working capital |
|---|---|---|---|---|
| 10 | $24k | about $20k | about −$9k | about $11k |
| 50 | $120k | about $100k | about −$45k | about $55k |
| 200 | $480k | about $400k | about −$180k | about $220k |

- **Cash cycle:** about 20–25 days positive (receivables before payment) (E).
- **Peak funding in the base case:** **$30k** without an owner draw, but **$192k** with a $4k/month draw. The business does not earn enough to pay the founder.
- **Auto-debit** cuts DSO to about 10 days.

## 9. Regulatory path

- **Licence:** no Illinois licence for billing services was identified. Stage C did not re-verify this, because ilga.gov was unavailable (MISSING).
- **HIPAA:** a BAA with each clinic [A, WS04-S018], plus Security Rule safeguards for the founder's own systems.
- **Fee rules:**
  - Medicare 42 CFR 424.73 and Medicaid 42 CFR 447.10 restrict percentage fees when the agent receives the payment.
  - Use provider-account deposits, and flat per-claim fees on Medicaid.
  - The HFS interpretation for MCO claims is MISSING.
- **Liability:**
  - False Claims Act exposure from coding errors, especially during the 2027 code change.
  - E&O + cyber insurance, about $5–10k a year (E).
- **Clinic-side requirements:** each clinic must be enrolled in HFS IMPACT and credentialed with each MCO [A, DD-S026].
- **Optional:** CPB certification (cost and duration MISSING).
- **Timeline:** 1–3 months.

## 10. Operations workflow

**Lead to cash:**
1. Lead and audit.
2. Signed agreement + BAA.
3. Credentialing check and EHR access.
4. Eligibility and authorisation tracking.
5. Claim scrub and submit through Claim.MD.
6. ERA posting.
7. Denial work and appeals.
8. Patient statements.
9. Monthly report and invoice.

**Who does what:**
- **Human:** payer phone calls, appeal judgment, client communication.
- **AI-assisted:** claim scrubbing rules, denial categorisation, appeal-letter drafting, authorisation-expiry alerts.
- **Automatable:** eligibility batches and ERA posting.

**Stack and staffing:**
- Clearinghouse $120/month per tax ID [B].
- Scrubbing and AI tools about $300/month (E).
- One biller per about 4 clinics; a coordinator from 10 clients; an operations lead from 16.

## 11. Competitive position and defensibility

**What could accumulate:**
- A payer-specific playbook for the five Illinois MCOs.
- 2027 code-crosswalk know-how.
- Referral trust among therapist-owners.

**What prevents a moat:** EHR vendors own the data and workflow, and can bundle billing at 3.9–6% [DD-S022, DD-S024]. Owners see an outsourced biller as risk to their cash flow, and switching costs protect incumbents more than entrants.

Entry score: 3.

## 12. Key risks and pre-mortem

| Loss level | What happened | Early warning sign |
|---|---|---|
| **$5k** | Audits delivered free to 10 clinics, but only 0–1 sign because owners prefer their EHR's billing add-on | Prospects ask "is this cheaper than Carepatron?" |
| **$25k** | Biller hired at client #1; 3 clients by month 9; the biller is under-used, and clients churn after a denial spike from 2027 code errors | Denial rate above 10%; days in A/R rising |
| **$50k** | An over-coding or modifier error triggers MCO recoupment or an audit; clients leave; possible E&O claim | Any recoupment letter; payer audit request |

**Stress tests (year-3 operating profit):**

| Test | Result |
|---|---|
| Labor +20% | −$48k |
| Hires 30% sooner | −$149k |
| Gross margin −10 points | −$22k |

## 13. Validation plan

The plan applies only if the founder wants to retest the drop decision. Total cost is under about $300.

| # | Experiment | Cost | Success | Kill |
|---|---|---|---|---|
| 1 | Paid 2027 code-change readiness audit at $500, offered to 20 of the 31 prospects | ~$100 | ≥3 paid audits | <2 |
| 2 | Pull 3 months of A/R and denial data (with permission) from paying audit clients to measure claims per clinician and denial rate | Time | Data supports ≥6 clinics per biller with tooling | <4 clinics per biller |
| 3 | Price test: 6.5% + $5 per Medicaid claim against the client's quoted EHR-bundled option | $0 | ≥2 signed letters of intent at ≥6% | All prospects choose a ≤4% bundle |
| 4 | Ask 3 clinics which billing their EHR already offers | $0 | ≥2 of 3 have no managed option | Most have one |

## 14. Revised scores and verdict

| Criterion | Stage C | Stage D | Note |
|---|---|---|---|
| fcf | 4 | **3** | Base operating profit $24–25k in years 3–5 |
| roic | 8 | **5** | Operating profit ÷ $30k no-draw peak ≈ 80% |
| access | 5 | 5 | |
| scale | 6 | **5** | |
| resilience | 6 | 6 | |
| entry | 3 | 3 | |
| delegation | 7 | 7 | |
| cash | 7 | 7 | |
| feasibility | 8 | 8 | |
| ai | 6 | 6 | |

- **Composite:** raw 5.00; evidence-adjusted 5.00 (D).
- **Model results:**

| Case | Year-3 operating profit | Peak funding (with $4k/month draw) |
|---|---|---|
| Conservative | −$33k | $466k |
| Base | **+$24k** | $192k |
| Optimistic | +$295k | $7k |

- **Verdict: DROP.** Revisit only if experiment #2 shows a capacity of 6 or more clinics per biller.

**Limitations:**
- ASHA pages returned 403; MedBridge was used instead.
- MCO and BCBSIL rates, clinic payer mix and biller productivity are MISSING or E.
