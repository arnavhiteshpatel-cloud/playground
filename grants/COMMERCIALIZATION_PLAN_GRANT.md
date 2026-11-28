# Commercialization Plan: Grant-Oriented DRAFT

**Prepared:** 2026-11-27.
**Status:**
- No customers, no revenue, no physical validation, not incorporated.
- Every market statement below is **[HYP]** until supported by interviews or cited sources.
- The structure follows the NIH Phase II commercialization-plan headings (12-page limit for R42/R44 [V page-limits table]; the plan is not required at Phase I [V]). It also feeds the NSF pitch "Market Opportunity" and the NSF commercialization sections [INF].

---

## 1. Value of the SBIR/STTR project, expected outcomes and impact
- **Product:** OsteoQuant, a three-class micro-CT quantification tool (new bone / residual graft / host bone) that abstains when graft and new bone cannot be separated, aims to report calibrated uncertainty, and writes reports with a tamper-evident audit trail (research prototype; not validated).
- **Phase I aims:** physical ground-truth benchmark, a model with measured accuracy against that benchmark, and an expert-agreement study [PENDING RESULT for each].
- **Impact hypotheses [HYP]:**
  - Shorter analysis time per specimen.
  - Lower inter-operator variability.
  - Fewer re-analyses and disputes between sponsors and CROs.
  - Possibly smaller animal cohorts if measurement variance falls (requires a power-analysis demonstration; do not claim without data).

## 2. Company
- **Current:** pre-incorporation project led by a UIUC undergraduate founder.
- **Planned entity:** [PLACEHOLDER: Delaware or Illinois C-corp vs. LLC]. Note the DCEO match requirement that the grantee be an IRS "regarded entity" [V], and that SAFEs (Cozad prizes) presume a corporation [INF]. Obtain legal advice.
- **Location:** Illinois (Research Park / EnterpriseWorks if accepted). This is required for the DCEO match and Innovation Vouchers [V].
- **Ownership:** ≥51% US citizens or permanent residents (SBIR) [V]. iVenture requires UI students to hold majority ownership [V].
- **IP:** OTM determination and any license (see §5).

## 3. Market, customers and competition

### 3.1 Segments (to rank via discovery)

| Segment | Buyer / user | Pain hypothesis | Willingness-to-pay hypothesis |
|---|---|---|---|
| Preclinical CROs (orthopedic / dental bone-defect models) | Study director / imaging lead | Throughput, consistency, sponsor audits | Per-study or annual license [HYP] |
| Orthobiologic & bone-graft-substitute companies | Preclinical R&D lead | Trustworthy graft-resorption vs. new-bone numbers across CRO studies | Annual license; validation services [HYP] |
| Academic MSK labs & imaging cores | PI / core manager | Analyst time; reviewer scrutiny | Low-cost academic license; core-facility license [HYP] |
| Scanner / software vendors | BD / partnerships | Add-on analytics | OEM/licensing (Phase II+) [HYP] |

### 3.2 Market sizing method (no numbers until sourced)
Bottom-up: (# target organizations) × (bone-graft studies per year) × (specimens per study) × (price per specimen or study).

| Input | Value | Source |
|---|---|---|
| # target organizations | [PENDING] | Interviews, CRO directories |
| Studies per year | [PENDING] | Interviews; literature counts |
| Specimens per study | [PENDING] | Literature counts |
| Price | [PENDING] | Pricing interviews |

Optionally cross-check top-down with cited reports on the bone-graft-substitute and preclinical imaging markets [UNR: cite only from accessible sources].

### 3.3 Competition (build from public documentation; [CC] general knowledge)
- Scanner-vendor analysis software and commercial micro-CT analysis packages (threshold/ROI-based morphometry).
- General image-analysis and open-source tools, plus in-house scripts.
- Manual analysis by trained staff (often the status quo).
- **Differentiators [HYP until validated]:** physically benchmarked graft/new-bone separation (aim); calibrated uncertainty (aim; not achieved yet: temperature scaling did not improve calibration in simulation); audit trail; low-label adaptation to new materials.

### 3.4 Customer-discovery plan (Dec 2026 – Mar 2027)
- **Target:** ≥30 interviews by Feb 2027 and ≥60 by Jun 2027. Mix: ≥10 CRO, ≥10 industry, ≥10 academic.
- **Questions:**
  - Current workflow and time per specimen
  - Graft materials used
  - How graft and new bone are separated today
  - Disputes and re-analyses
  - Who signs off
  - Budget owner
  - Data-sharing constraints
- **Exit criteria:**
  - A clear #1 segment.
  - ≥3 design partners willing to share de-identified scans (supports Aim 3).
  - ≥1 letter of intent to pilot.
- **Vehicles:** Illinois I-Corps workshops [V], Cozad mentoring [V], ORS/TERMIS conferences [INF].

## 4. Go-to-market and revenue model [HYP]
1. **Design-partner phase (2027):** free or low-cost pilots with 2–3 academic labs plus 1 CRO, in exchange for data and feedback.
2. **Analysis service with a documented verification status (2027–28, after incorporation and a first signed pilot):** OsteoQuant-run non-GLP analyses with reports carrying a tamper-evident audit trail (cash flow before a full software product).
3. **Software licenses (2028+):** per-study and annual CRO/company licenses; academic tier.
4. **Partnerships (Phase II+):** scanner vendors and imaging cores.

## 5. Intellectual property protection
- **Ownership:** University policy [CC] may claim IP created with University facilities, equipment or funds. Get an OTM determination; negotiate a license if needed [INF].
- **Patents:** evaluate phantom design, uncertainty-to-endpoint propagation and the material-conditioning method. Use a provisional before public disclosure (Cozad is non-confidential [V-old]). Use the IP Clinic (spring) [V].
- **Copyright and trade secrets:** source code, trained weights, benchmark curation pipeline.
- **Open vs. closed:** consider releasing the **benchmark** openly to build credibility and adoption, while keeping models and reporting proprietary [HYP].
- **Trademark:** "OsteoQuant" clearance search before branding spend (IP Clinic trademark track [V]).

## 6. Finance plan (sequenced; amounts checked against sources where marked)

| Stage | Source | Amount | Status |
|---|---|---|---|
| Now–Apr 2027 | Cozad 2027 prizes (SAFE) | 2026 scale: up to $100k grand prize [V] | Apply |
| Jun–Aug 2027 | iVenture | Up to $20k, no equity [V] | Apply (~Mar 2027 [INF]) |
| 2027 | Illinois Innovation Award (nominated) | $20k [V] | Needs a nomination |
| 2027 | UIUC OUR grant / Innovation Voucher | [UNR] / ≤$75k at 75% [V] | Fund phantom scans |
| Late 2027 – 2028 | NSF SBIR Phase I **or** NIH STTR Phase I | $305k [V] / $335,937 guideline [V] | Pitch now |
| After federal award | DCEO Phase I match | ≤$75k [V] | Conditional |
| After validation and pilots | Illinois Ventures Pre-Seed / Illini Angels | $100k–$300k [V] | Later |
| Phase II | NSF $1.25M / NIH SBA guideline $2.24M [V] | — | 2029+ [INF] |

## 7. Milestones (go/no-go)

| ID | Milestone | Target date | Go / no-go criterion |
|---|---|---|---|
| M0 | Synthetic-phantom benchmark complete | [FOUNDER: date] | [PENDING RESULT] documented and reproducible |
| M1 | 30 customer interviews; segment ranked | Feb 2027 | ≥1 segment with a strong pain signal (≥50% of interviewees rate it 4–5 of 5) [HYP threshold] |
| M2 | OTM IP determination; entity formed | Feb–Mar 2027 | Clear rights to the software |
| M3 | NSF Project Pitch invited | Feb–Mar 2027 | Invitation received |
| M4 | First physical phantom scans | Mar–Apr 2027 | Scans acquired; ground truth verified |
| M5 | Faculty partner + 2 data LOIs | Apr 2027 | Signed LOIs |
| M6 | NSF Phase I full proposal submitted | Jul 7, 2027 [V] | PI eligibility plan confirmed |
| M7 | Phase I complete: benchmark + validation | 2028 [INF] | Pre-specified Aim 1–3 targets met |
| M8 | 1 paid pilot | 2028 [HYP] | Signed pilot agreement |

## 8. Business risk mitigation

| Risk | Mitigation |
|---|---|
| No customer pull | Discovery before building more features; pivot to service or academic-core licensing if needed |
| Founder bandwidth (full-time student) | Recruit co-founders; time-box; use summer (iVenture) for intensive work |
| PI eligibility | Plan per NSF_vs_NIH_ELIGIBILITY.md §3 |
| IP ownership | Early OTM engagement |
| Data access for validation | Multiple design partners; data-use agreements; phantom-first evidence |
| Regulatory / quality expectations of CROs | Audit-trail design; document validation; investigate 21 CFR Part 58 (GLP) expectations for analysis software with CRO QA staff [UNR] |
| Competitive response from vendors | Benchmark leadership; integrate with, rather than replace, vendor tools |
