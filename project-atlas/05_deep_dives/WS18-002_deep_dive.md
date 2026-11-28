# WS18-002 — Private-pay non-medical home care agency (absorbs WS04-001) · Stage D deep dive

> **Verdict: RESERVE** (not a finalist) · evidence level **C** · revised raw score 5.05, evidence-adjusted 5.04.
>
> **The decisive fact.** The cheapest credible independent entry still puts too much capital at risk for too little early profit:
> - **Capital at risk (base case):** about **$139k** with no owner draw, or **$209k** with a $4k/month draw from month 13.
> - **Operating profit (base case):** about **−$73k** in year 1 and **−$53k** in year 2, **+$27k** in year 3, and **+$119k** by year 5.
> - **Conservative case:** it never breaks even.
>
> Gross margin is thin because the business sells labor at a fixed mark-up. The Illinois 2025 median for in-home care is **$36/hr** [C, DD-S006], against a loaded caregiver cost of about $22–23/hr (E). The 37% that remains must carry the office, recruiting and the 24/7 on-call schedule.
>
> **What is still strong:**
> - Demand and delegation remain the best-documented in the portfolio.
> - Licensing is cheap: a $1,500 fee with no manager credential required [A, C6-S018, C6-S019].
>
> It stays on reserve as a capital-heavy second business, or as an option if a cheap demand test (§13) shows unusually strong inquiry flow.

## 1. Specific initial niche

**Offer.** Private-pay, non-medical in-home care for adults 75+ in central DuPage County: Wheaton, Glen Ellyn, Lombard, Downers Grove, Winfield, Carol Stream and Lisle (about a 10-mile radius). Two specialties:
- **Hospital-to-home transitions:** a start of care guaranteed within 24–48 hours.
- **Dementia companion care:** for families of residents in local memory-care communities.

**Rules for the launch:**
- No Medicaid/CCP. CCP pays $30.80/hr [A, WS18-S020], which leaves roughly a 26–28% gross margin (Stage C).
- No live-in day rates at launch, because of Illinois overtime exposure [A, DD-S008].
- Long-term-care-insurance clients are accepted only with family-guaranteed weekly payment.

**Why this area.** Central DuPage has dense referral sources:
- 7 licensed hospitals, including a rehabilitation hospital (Marianjoy) [A, DD-S002].
- About 30 licensed assisted-living or memory-care communities [A, DD-S003].

It also has fewer agency offices than the busiest suburbs. Wheaton has 4 licensed home services agency offices, Glen Ellyn 7 and Lombard 10, against 36 in Naperville and 33 in Skokie [A, DD-S001].

**Limitation:** an agency's office address is not its service area, and the Census ACS API needed a key, so seniors-per-agency could not be computed (MISSING).

## 2. Named operators

| Operator | What is known | Level |
|---|---|---|
| Home Instead (franchise) | 603 U.S. units. Average 2024 gross sales $2.61M, median $2.26M, about $33 per client-hour. Only 19 units are 1–4 years old; 4 of 5 units at 1–2 years are under $500k | B, WS18-S005, C6-S023 |
| A Place At Home (franchise, 34 outlets) | 2025 cohort medians: $329k at 12–24 months, $671k at 25–36 months, $1.50M at 37–48 months. Gross profit after direct labor is about 51%. **Illinois 24** (opened Aug 2022): $1.88M sales, 42.1% GP. **Illinois 19** (opened Aug 2021): $1.64M, 52.3%. Weak tail: outlets at $5k–$229k | B, C6-S022 |
| Addus HomeCare (public) | Illinois is its largest personal-care market, mostly Medicaid. Q4-25 gross margin 32.8%; Illinois incremental margin "low 20%"; Illinois DSO 54.7 days | B, WS04-S004 |
| ComForCare (Wheaton), Synergy HomeCare of DuPage County (Glen Ellyn), Always Best Care (Lombard), Assisting Hands and Home Helpers (Downers Grove), Best at Home Care (Glen Ellyn) | Franchise brands holding IDPH home services licences within the radius | A, DD-S001 |
| Independents within the radius: 1776 Senior Care, Trusted Hearts, Snug and Comfort, Kindly Home Care (Winfield), Suburban Home Care, Platinum Care Group and about 20 others | 35 licensed agency offices in 8 central DuPage cities. No revenue data | A, DD-S001 |
| Lifespace Personal Services (Beacon Hill, Lombard); Maxim Healthcare (Lombard) | Captive retirement-community agency; national staffing company | A, DD-S001 |

**Notes:**
- Only 26 home services *placement* (registry) agencies are licensed statewide, against 1,244 employer agencies [A, DD-S007]. The registry model is rare, so it is not proposed here.
- Incumbent economics: franchise gross profit excludes the office, marketing and royalties. No independent-agency P&L was found (MISSING).

## 3. Suppliers and partners

The full list is in `09_databases/suppliers/WS18-002_suppliers.csv`.

- **IDPH licensing (documented, A).**
  - $1,500 a year, non-refundable.
  - Provisional licence valid 240 days, with a survey before it expires.
  - Liability-insurance evidence is required.
  - No manager credential is required [C6-S018–C6-S021, WS04-S027].
- **Health Care Worker Background Check, fingerprinting (requirement documented, A).** Vendor fees are MISSING.
- **Illinois Department of Labor (documented, A).** $15.00 minimum wage; overtime after 40 hours a week [DD-S008].
- **Scheduling, EVV and billing software (assumed).** AxisCare starts at about $200–325/month per third-party listings (D, DD-S010). CareSmartz360 and WellSky Personal Care pricing is MISSING.
- **Workers' compensation (assumed).** Class 8835 runs about $1.23–3.49 per $100 of payroll (D, DD-S009).
- **Liability package (assumed).** General/professional liability, abuse and molestation, hired and non-owned auto, EPLI and a crime bond. Premiums are MISSING; the model uses $700–1,300/month (E).
- **Franchise alternatives (Item 19 documented; Items 5–7 MISSING).** A Place At Home and Home Instead.

## 4. Named prospective referral partners

Families are the buyers, and they are private individuals, so they are not recorded. The CSV lists **28 referral-partner organizations**, all "prospect — not contacted":

| Type | Organizations |
|---|---|
| Hospitals (7) | NM Central DuPage, NM Marianjoy Rehabilitation, Advocate Good Samaritan, Elmhurst Memorial, Edward, UChicago Medicine AdventHealth GlenOaks and Hinsdale |
| Assisted living / memory care (15) | Brighton Gardens of Wheaton, Travanse Living at Wheaton, Westbridge (Wyndemere campus), Atria Park of Glen Ellyn, Maple Glen Memory Care, Lexington Square Lombard, Lombard Place, Sunrise of Fountain Square, and others |
| Home health agencies (2) | Anodyne (Glen Ellyn), Loyola Medicine Home Care |
| Hospices (3) | VITAS (Lombard), St. Croix Hospice Lombard, Advocate Hospice |
| Area Agency on Aging (1) | AgeGuide Northeastern Illinois, Lombard [C, DD-S011] |

**Caveat:** the IDPH assisted-living dataset shows licence dates from 2019–20, so community names and status must be re-verified [DD-S003].

**Elder-law attorneys** were not listed. No lawful directory was retrieved (NAELA not accessed), so that partner type is MISSING.

## 5. Representative transactions

Rates are C/E; wages are C/E. These lines are also in the model JSON.

| Transaction | Revenue | Direct costs | Contribution | Payment timing |
|---|---|---|---|---|
| Standard client week: 18 hrs at $36 | $648 | Wages 18 × $19 = $342; payroll load ~18% = $62; non-billable time 3% = $10; processing 1% = $6 | **$228 (35%)** | Weekly, card or ACH. Caregiver paid weekly or biweekly in arrears |
| Hospital-to-home: 3 × 4-hr visits at $38 | $456 | Wages $228; load $41; mileage $12; processing $5 | **$170 (37%)** | Weekly |
| 24/7 hourly case: 168 hrs at $34, three 8-hr shifts, no overtime | $5,712 | Wages $3,276 (at $19.50); load $590; backfill premium $164; processing $57 | **$1,625 (28%)** | Weekly in advance (recommended) |

**Evidence behind these lines:**
- **Rates:** CareScout Illinois median $36 [C, DD-S006]; Home Instead national ≈$33 (2024) [B, WS18-S005]. The $2 short-visit premium and the $34 rate for 24/7 cases are assumptions (E).
- **Wages:** the Illinois personal-care-aide median is $18.30 (Chicago $18.36; 90th percentile $20.43) [C, C6-S024]. Paying $19–19.50 is a recruiting assumption (E).
- **The 24/7 case:** it has the lowest margin and the highest scheduling risk. Treat it as a capacity-filler, not a target.

## 6. Customer acquisition

**Client #1** (months 5–7, after the provisional licence):
- Ask the 28 partners to add the agency to their private-duty resource lists.
- Run a Google Business Profile.
- Use the founder's personal network.

Hospital case managers usually give families a list of several agencies, so the first client is likely from search or a memory-care community, not a hospital (E).

**Clients #2–10:** 10–15 in-person partner visits a week (E). Lead with:
- the 24–48-hour start guarantee;
- a named caregiver bench (Polish- and Spanish-speaking caregivers where recruitable);
- in-services on dementia care for community staff.

**Clients #11–100:**
- A community liaison from month 18.
- Reciprocal referrals with hospice and home health.
- Reviews and local search.

**Funnel at full pace (all E):** about 4.5 qualified inquiries a month from the founder's network → 50% become an in-home assessment → 55% start care. On top of that come about 1 referral per 100 active clients a month and 0.8 starts a month per liaison.

The base case was calibrated so that year-3 revenue (**$798k**) sits near the **$671k A Place At Home 25–36-month median** [B, C6-S022]. Without that check, the first draft driver set produced $1.76M, which is implausible for an unbranded entrant.

**Unit economics (base, E):**
- **Contribution per client** ≈ $2,806 × (37% − 3.5%) ≈ $940 a month.
- **Tenure:** 1 / 6% ≈ 17 months.
- **Lifetime contribution** ≈ $15.7k.
- **Blended CAC in year 3:** including the liaison and fixed marketing, about $3,000–3,500 per start. Payback is about 3.5 months of contribution.

## 7. Pricing strategy

| Element | Price |
|---|---|
| Standard rate | $36/hr (state median) |
| Visits under 4 hours | $38–40/hr |
| Weekends and holidays | 1.5× on named holidays |
| Shift minimum | 4 hours |
| 24/7 hourly cases | $34/hr |
| Annual escalator | 3% |

**Price references:**
- **CCP:** $30.80 [A, WS18-S020] is the floor families compare against only if Medicaid-eligible.
- **Home Instead:** ≈$33 nationally in 2024 [B].
- **CareScout Illinois median:** $36 [C].

**No Chicago-metro or DuPage private-pay median was retrieved (MISSING).** Validating the local rate is experiment #2 in §13.

## 8. Working capital and cash conversion

Payroll for 50 clients is about $87k a month: 18 hrs × 4.33 × $19 × 1.18. The table compares two billing approaches.

| Active clients | Weekly billing in arrears, all private pay | Same, with 20% LTC insurance at 45 days |
|---|---|---|
| 10 | about **$2.5k** (one week of revenue minus one week of payroll) | **≈ $10.8k** |
| 50 | **≈ $12k** | **≈ $54k** |
| 200 | **≈ $49k** | **≈ $216k** |

- **Billing weekly in advance by card on file** turns net working capital slightly negative, so clients fund payroll. The base model uses DSO 4 days and DPO 7 days.
- **Long-term-care insurance** reimburses in arrears (Stage A, E). Addus's Illinois Medicaid DSO of 54.7 days [B, WS04-S004] shows why government payers were excluded.
- **Real cash need:** working capital is not the problem. The ramp losses are. The peak cumulative deficit is about $139k (no draw) and occurs around month 28.

## 9. Regulatory path

**Steps to licence (A, unless marked otherwise):**
1. Form the LLC (E: $150 state fee, not verified).
2. Bind general/professional liability insurance. Evidence is required with the application [C6-S019].
3. Write policies covering service agreements, supervision, complaints and training.
4. Designate the founder as the supervisor of services. No credential is required [C6-S017, C6-S019].
5. Hire or contract a trainer or supervisor with 2 years of relevant experience [C6-S015].
6. File the IDPH Home Services application with the $1,500 cheque [C6-S021].
7. Wait for the provisional licence. IDPH aims for about 90 days; the licence is valid 240 days, with an on-site survey before it expires [WS04-S027].

**Before each caregiver's first assignment:**
- A fingerprint background check under the Health Care Worker Background Check Act [WS18-S013].
- 5 hours of training plus a competency check.
- 5 more hours within 30 days, then 10 hours a year [C6-S015].
- Dementia training under 77 IAC 973 [WS04-S027].

**Ongoing supervision:** on-site supervision every 90 days, and it cannot be billed [C6-S016].

**Labor law:**
- $15 minimum wage and overtime after 40 hours a week [A, DD-S008].
- Illinois paid-leave rules apply (details not re-verified).
- The federal FLSA third-party companionship status was not re-verified (MISSING). Illinois overtime applies regardless.

**Insurance:**
- Workers' compensation, class 8835, $1.23–3.49 per $100 of payroll [D].
- Liability package: E at $8–16k a year.

**Timeline:** 4 months in the base case (3–6) from filing to first billable hour.

## 10. Operations workflow

1. **Inquiry → assessment.** The founder handles intake and does a same- or next-day in-home assessment. Care plan and service agreement are signed; card or ACH is set up.
2. **Matching.** The coordinator matches a caregiver using software-based matching.
3. **Start of care.** Caregivers clock visits through EVV.
4. **Billing and payroll.** Weekly billing is automated; payroll runs weekly or biweekly through a payroll service.
5. **Supervision.** A supervisor visits every 90 days [C6-S016].

**What stays human:** all care, matching judgment, family conflict resolution and on-call cover.

**Where AI helps (affordable after December 2026):**
- Screening caregiver applicants.
- Shift-fill messaging.
- Summarizing care notes and writing family updates.
- Drafting the documentation trail for IDPH surveys.

**Software stack:**

| Tool | Monthly cost |
|---|---|
| Scheduling/EVV (AxisCare-type) | $200–450 |
| Payroll service | about $250 |
| AI tools | about $150 |
| Google Workspace and phones | about $100 (E) |

**Staffing in the model:**
- Part-time trainer/supervisor from month 4.
- Coordinator/scheduler at 10 clients.
- Full-time care manager at 30 clients.
- Community liaison at month 18.
- General manager at about $1.8M annual revenue.

## 11. Competitive position and defensibility

The wedge is speed to start, dementia competence and caregiver language match. All of it is copyable. What accumulates over time:
1. **A caregiver bench with low turnover.** Turnover runs about 75% industry-wide [C, C6-S028]. Paying at the 75th–90th percentile and guaranteeing hours is the lever.
2. **Referral-source trust:** hospital resource lists and memory-care directors.
3. **Local density,** which reduces drive time and missed shifts.
4. **Reviews.**

None of this is contractual. Families and caregivers can both switch at will.

## 12. Key risks and pre-mortem

| Loss level | What happened | Early warning signs |
|---|---|---|
| **$5k** | Licence application and insurance bound; the demand test shows fewer than 3 qualified inquiries a month after 90 days of partner visits; the founder stops | Partners say "we already have 6 agencies on our list" |
| **$25k** | Licensed; 3–5 clients; two caregivers quit and shifts are missed, so referral sources stop sending families | Unfilled-shift rate above 3%; caregiver 90-day attrition above 40% |
| **$50k+** | Office staff hired ahead of census (the model's year-1 −$73k); the conservative path (13 clients at month 36) burns about $150k a year | Census below 8 at month 12, or below 15 at month 18 |

**Other risks:**
- Abuse or injury allegations.
- Overtime from back-to-back cases.
- A recession cutting private-pay hours. The stress test (−30% new clients, churn ×1.5) gives a year-3 operating loss of **−$79k**.
- Wage inflation. Labor +20% gives **−$5k**.

**Most sensitive drivers (±25%):** gross margin (year-3 range −$47k to +$101k) and hours per client (−$40k to +$94k).

## 13. Validation plan

Paid evidence is impossible before licensure, because providing care unlicensed is illegal. So the tests measure demand cheaply, then commit only after that.

| # | Experiment | Cost | Success | Kill |
|---|---|---|---|---|
| 1 | Twenty in-person referral-partner interviews from the CSV, asking how many private-pay referrals a month go unfilled and which agencies fail | $100 (mileage) | ≥5 partners say they will add a new agency and describe unmet hospital-to-home or dementia demand | <3 partners interested |
| 2 | Rate check: collect published or quoted rates from 15 DuPage agencies' public pages, plus mystery-shopper calls *by the founder* | $0–50 | Local median ≥$35/hr with 4-hr minimums | Median ≤$32/hr |
| 3 | A $500 Google Ads + landing-page test for "home care Wheaton / Glen Ellyn" (no service sold; capture inquiries and refer them on) | $500 | Cost per qualified inquiry ≤$60 and ≥8 inquiries in 30 days | ≤3 inquiries |
| 4 | Caregiver supply test: free job posting at $19–20/hr | $0–200 | ≥25 qualified applicants in 2 weeks | <8 |

**Gate:** proceed to the $1,500 licence only if #1, #3 and #4 pass. Total validation cost is about **$800**.

## 14. Revised scores and verdict

| Criterion | Stage C | Stage D | Reason |
|---|---|---|---|
| fcf | 5 | **4** | Base years 3–5 operating profit is $27k → $119k |
| roic | 6 | **3** | Year-3 op ÷ peak capital ≈ 13–19%; year 5 ≈ 57–85% |
| access | 5 | 5 | |
| scale | 6 | 6 | |
| resilience | 7 | 7 | |
| entry | 4 | 4 | |
| delegation | 7 | 7 | |
| cash | 6 | **7** | Weekly private-pay billing roughly matches weekly payroll |
| feasibility | 7 | 7 | |
| ai | 4 | 4 | |

- **Composite:** raw 5.05; evidence-adjusted 5.04 (C).
- **Model results:**

| Case | Year-3 operating profit | Peak funding |
|---|---|---|
| Conservative | −$147k | unbounded |
| Base | **+$27k** | $209k with draw / $139k without |
| Optimistic | +$301k | $44k |

- **Base milestones:** first month at ≥$10k operating profit is month 41; 10-year deployable cash is $158k.
- **Verdict: RESERVE.** The demand, delegation and ceiling are real. But the base case breaches the founder's $100k conditional backing, and the profit arrives in years 4–5.

**Limitations of this analysis:**
- The Census API required a key.
- cookcountyil.gov returned 404 and chicago.gov is blocked.
- The AxisCare and HHS pages returned 403.
- No local private-pay rate survey or independent-agency P&L exists.
- Client tenure and hours per client are E.
