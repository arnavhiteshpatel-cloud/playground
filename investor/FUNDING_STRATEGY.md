# OsteoQuant Funding Strategy (2026-11-27)

**Status:** research prototype; pre-revenue; unincorporated; no customers, interviews, pilots or letters of intent. Nothing in this document has been applied for, submitted or signed, and no investor or programme has been contacted.

**Labels:**
- [V] checked on the sponsor's own page (URL and access date given)
- [V-repo] checked in an earlier pass on 2026-11-27 and recorded in `grants/FUNDING_OPPORTUNITIES.md` or `grants/NSF_vs_NIH_ELIGIBILITY.md` (re-check before acting)
- [INF] inference
- [HYP] hypothesis
- [UNR] unresolved

> **Founder decisions that require counsel.** Incorporation (whether, when, entity type, state, tax election), university IP disclosure and ownership determination (UIUC Office of Technology Management), and every agreement (SAFE, convertible note, equity, grant sub-awards, NDAs, DPAs, advisor and founder agreements, facility-use agreements) are **the founder's decisions**. Each needs advice from a qualified attorney and, for IP, a written answer from OTM. Nothing here is legal, tax or investment advice. Question lists for OTM and the Landuyt IP Clinic are in `outreach/IP_AND_OTM_QUESTIONS.md`.

---

## 1. Bottom line [INF from `business/REVENUE_MODEL.md`]
1. **Cash without grants is the lead case.** Grants are not operating cash: none has been applied for, eligibility is unresolved, and an award is restricted to its project (an NIH STTR also needs a ≥30% research-institution subaward). In the Bootstrapped Base scenario (hypothetical), with no revenue before incorporation and a first signed pilot, revenue reaches $259K by 2031; **without grants the largest cumulative deficit is about $96K** and cumulative cash is still about −$35K in 2031. **If** the assumed awards ($325K) were won, only their fee share and the planned costs the funded project legitimately pays reach operating cash, and the deficit would fall to about $45K. Bootstrapping with customer revenue is the base path; grants are an upside that funds specific project work.
2. **Venture capital is not justified on today's evidence.** The Venture Base scenario (hypothetical) needs about **$4.2M of equity without grants** (about $3.7M if the assumed awards were won) to reach $0.63M revenue in 2031. That revenue equals about a third of the mid serviceable pool, and reaching it needs hypothetical expansion modules. No plausible study price closes the gap: the no-grant break-even study price in that structure is about $140K.
3. **Pre-seed equity becomes rational only after specific evidence exists** (§3): a separable path on real graft materials, paid pilots converting, and evidence of a larger market (non-US sponsors, adjacent modules, CRO licences). Raising before then would sell equity at the point of maximum uncertainty [INF].
4. **Valuation:** this document gives **no valuation figures**. No source the founder could cite and defend was verified for comparable pre-revenue research-software companies. SAFE terms (valuation cap, discount) for programmes such as Cozad are not stated on the pages checked (§6). Compare real term sheets with counsel when they exist.

## 2. Options compared

### 2a. Bootstrapping (customer revenue)
| Item | Detail |
|---|---|
| What | Paid pilots ($2.5–5K), non-GLP study analysis ($8–15K), material characterisation ($5–15K), academic and enterprise desktop licences. All prices [HYP] |
| Dilution | None |
| Preconditions | A legal entity to contract and invoice (founder decision with counsel); a reviewed pilot template; OTM clarity on who owns the software |
| Strength | Revenue is also the best validation evidence for every later funder [INF] |
| Limit | Founder bandwidth as a full-time student. Base-case delivery is ~0.4 FTE in 2031 (costed as paid analyst time), and sales and validation compete for the same hours. No revenue is possible before M0 (entity, IP clearance, insurance, counsel-reviewed contracts) and a first signed pilot (M3) |

### 2b. Non-dilutive
| Programme | Amount | Eligibility fact relevant to a student founder | Source | Fit |
|---|---|---|---|---|
| **NSF I-Corps Teams** (NSF 25-549) | ≤ $50,000 over 12 months | The institution submits. The Technical Lead "may be a faculty member, senior research scientist, or postdoctoral scholar". The Entrepreneurial Lead "may be a postdoctoral scholar, graduate, or other student". Lineage: a prior relevant NSF award, or participation in a Regional I-Corps programme with a recommendation letter. Teams are expected to do ≥100 customer/partner interviews | https://www.nsf.gov/funding/opportunities/nsf-national-innovation-corps-teams-nsf-national-i-corps-tm/nsf25-549/solicitation [V, accessed 2026-11-27] | Good **after** regional I-Corps and with a faculty Technical Lead. Pays for discovery travel. Does not build product |
| **Illinois I-Corps** (Workshop Series; I-Corps Boost; National I-Corps; SBIR/STTR technical assistance) | Boost is "a free program". No stipend is listed | The programmes page states no student eligibility rules. Boost requires ≥20 prior interviews and a Hub-partner nomination [V-repo] | https://icorps.illinois.edu/programs [V, accessed 2026-11-27]; Boost details in `grants/FUNDING_OPPORTUNITIES.md` §3.3 | **Start here.** Training, and the lineage route to NSF I-Corps Teams |
| **NSF SBIR/STTR Phase I** (NSF 26-510) | Up to $305,000 [V-repo] | The PI "must be more than 50% employed by the small business for the duration of the SBIR/STTR project"; "Primary employment is not required at the time of full proposal submission"; ≥51% owned by US citizens or permanent residents. SAM, Research.gov and SBA registrations are not needed to submit a Project Pitch | https://seedfund.nsf.gov/solicitation-eligibility/ [V, accessed 2026-11-27] | Project Pitch possible now. An award needs an entity **and** a >50%-employed PI, which conflicts with full-time study [INF] |
| **NIH SBIR / STTR Phase I** (PA-27-100 / PA-27-102) | SBA guideline: up to $335,937 [V-repo] | SBIR: PD/PI primarily employed by the company. **STTR: PD/PI may be primarily employed by the partner research institution** (≥10% effort) [V-repo] | `SCIENTIFIC_EVIDENCE.md` §4; `grants/NSF_vs_NIH_ELIGIBILITY.md` | NIH STTR with a UIUC faculty PD/PI is the only federal route that avoids the founder-employment problem now [V-repo/INF] |
| SBIR/STTR programme status | Lapsed 30 Sep 2025; reauthorised 13 Apr 2026 through 30 Sep 2031 (P.L. 119-83) | n/a | `SCIENTIFIC_EVIDENCE.md` §4 [V] | Programmes are open |
| NIH policy on AI-written applications | Applications "substantially developed by AI" are not considered the applicants' original ideas | n/a | `SCIENTIFIC_EVIDENCE.md` §4 [V]; NOT-OD-25-132 | **The founder and team must write every application themselves.** The drafts in `grants/` are scaffolds only |
| Illinois DCEO SBIR/STTR Match | Phase I ≤ $75,000; Phase II ≤ $250,000 | Only after a federal Phase I award; Illinois-based for-profit; IRS "regarded entity" (a disregarded single-member LLC is ineligible [INF]) | `grants/FUNDING_OPPORTUNITIES.md` §3.8 [V-repo] | Conditional follow-on |
| Illinois Innovation Award; NIBIB DEBUT; UIUC undergraduate research grant | $20K; $10–20K prizes; [UNR] | Faculty nomination (IIA); team of 3–8 undergraduates (DEBUT) | `grants/FUNDING_OPPORTUNITIES.md` §§3.4, 3.11 [V-repo] | Small amounts, but they can fund the phantom study ($10–20K, `validation/BILL_OF_MATERIALS.csv`) |

### 2c. University venture programmes (existence and eligibility checked on their pages)
| Programme | Form | Eligibility fact | Source (accessed 2026-11-27) | Fit |
|---|---|---|---|---|
| **Cozad New Venture Challenge** (Landuyt Center) | Competition. "All of the top cash prizes in Cozad are awarded in the form of SAFE funding" | "All teams must include at least one full-time, degree-seeking student". The FAQ does not make incorporation a condition of entry. "Registration for 2027 will open in Fall 2026". SAFE cap and discount are **not stated** on the FAQ | https://landuyt.illinois.edu/programs/cozad/faq [V] | **High.** Mentoring and visibility. But a SAFE is equity-linked and needs an entity to receive it: read the SAFE document with counsel before accepting |
| **iVenture Accelerator** (Gies) | "Up to $20,000": "$10,000 in capacity funding" plus "$2,500 stipends for 4 full-time team members". "No equity is taken." | "A majority of your team must be University of Illinois students who hold majority ownership"; the team must work full-time for 10 summer weeks; preference for founders "NOT graduating in the summer". 2027 deadlines are not yet posted (the 2026 final wave closed 7 Mar 2026) | https://iventure.illinois.edu/ ; https://iventure.illinois.edu/apply [V] | **High.** Non-dilutive, and it funds the summer when the pilots would run |
| **Illinois Ventures Pre-Seed Fund** | Equity: "investments ranging from $100,000 to $300,000" | "early-stage companies with connections to the University of Illinois System"; "pre-seed and early-stage opportunities" | https://illinoisventures.com/pre-seed-fund/ [V] | Later: after the milestones in §3. Needs an entity |
| **Illinois Ventures angel network** | Equity: "between $100,000 and $300,000" | "a connection to the University of Illinois System"; "early-stage companies" | https://illinoisventures.com/angels/ [V] | Later, as above |
| Illinois Deep Technology Strategic Venture Fund | Equity; Seed and Series A | Founders tied to the UI System [V-repo] | `grants/FUNDING_OPPORTUNITIES.md` §3.6 | Not before seed-stage traction |
| EnterpriseWorks Student Startup Initiative | Space and shared lab access | Founder enrolled at UI; for-profit; technology-based [V-repo] | `grants/FUNDING_OPPORTUNITIES.md` §3.5 | Useful once incorporated |
| Landuyt IP Clinic | In-kind patent and trademark drafting; spring semester only; the student pays USPTO fees [V-repo] | | `outreach/IP_AND_OTM_QUESTIONS.md` | Use **before** public pitches disclose the method |

### 2d. Pre-seed equity (angels, pre-seed funds)
- **When it makes sense:** after milestone M4 in §3, if the evidence points to a market larger than US graft-defect analysis. Equity cannot fix a small-market problem [INF].
- **Investor types to consider** (none contacted; no individuals named):
  1. University-affiliated pre-seed funds and angel networks (Illinois Ventures, §2c).
  2. Life-science-tools and research-software seed investors.
  3. Medtech and orthopaedic angels who have operated graft or device companies.
  4. Strategic investors: imaging vendors and CROs. They carry **conflict risk**, because they are also channels or competitors (`docs/research/COMPETITOR_INTELLIGENCE.md`). Avoid exclusivity.
- **What to look for:** experience with research-tool businesses and service-heavy revenue; tolerance for a modest market; no demand for exclusivity that blocks CRO or vendor channels.

## 3. Milestones and the capital each unlocks
| # | Milestone (evidence, not claims) | Unlocks | Approx. timing [INF] |
|---|---|---|---|
| M0 | **One definition (used everywhere, including `business/REVENUE_MODEL.md` §4):** an entity exists (founder decision with counsel); the OTM ownership determination is received (IP clearance); insurance is in place; the NDA, SOW and DPA templates are counsel-reviewed | Everything below. Required before any SAFE, grant award, paid contract or evaluation on customer data | Requests start Dec 2026 – Feb 2027 (ask OTM; decide the entity type); completion date not set |
| M1 | ≥20 discovery interviews logged and coded (`business/INTERVIEW_GUIDE.md`) | I-Corps Boost eligibility (≥20 interviews [V-repo]); stronger Cozad, NSF Pitch and iVenture applications | By Feb 2027 |
| M2 | Physical phantom study: a separable path for ≥1 commercial material class, single-scan (or day-0, which is unproven under granule motion) (`validation/PHANTOM_EXPERIMENT_PROTOCOL.md`) | Credible SBIR/STTR technical aims; the first real-data claim in any pitch | Spring 2027 |
| M3 | First **paid** pilot ($2.5–5K [HYP]) under a reviewed template. **Prerequisites:** M0 and Gate 2 in `RELEASE_READINESS.md` (Gate 1; real-data validation for at least one task; closed human expert review; counsel-reviewed SOW/DPA), none met today | Behavioural price evidence (`business/PRICING_VALIDATION_PLAN.md` §7); a commercial letter of support for an SBIR/STTR | Mid 2027 at the earliest |
| M4 | ≥3 paid pilots or studies **and** ≥1 licence; measured analyst hours per study | Illinois Ventures pre-seed or angel conversations; NSF/NIH Phase I commercialisation plan | Late 2027 – 2028 |
| M5 | Phase I award, or ≥$100K trailing revenue, plus a published validation (e.g. an ORS abstract or manuscript) | Phase II (NSF up to $1.25M [V-repo]); DCEO match; a seed round **only if** expansion or non-US demand is evidenced | 2028+ |

## 4. Recommended sequence (next 12 months) [INF]
1. **Dec 2026 – Feb 2027:**
   - Ask OTM for an ownership determination (counsel-guided).
   - Register for Cozad (registration opens 1 Dec 2026; deadline 2 Feb 2027; finals April 2027, date not confirmed; `grants/COZAD_APPLICATION_PACKAGE.md`).
   - Join an Illinois I-Corps workshop.
   - Run Wave 1 interviews (`business/PROSPECT_SEGMENTATION.md`).
   - Optionally submit an NSF Project Pitch, which needs no registrations [V].
2. **Feb–Apr 2027:**
   - Run the phantom study (M2).
   - Ask a faculty member to nominate the founder for the IIA.
   - Apply to iVenture if a 2027 wave opens.
   - Decide on an NIH STTR with a UIUC faculty PD/PI.
3. **Summer 2027:** iVenture (if accepted); first paid pilots only once M0 and Gate 2 are met (M3).
4. **Late 2027:** NSF I-Corps Teams (with a faculty Technical Lead) or a Phase I submission. Talk to pre-seed investors only if M4 is met.

**Do not:** accept a SAFE or other investment, sign a grant sub-award, or make a public pitch that discloses the method before M0. Do not apply to programmes whose eligibility the founder does not meet. Do not let any application text be substantially machine-written (NIH policy above).

## 5. Use of funds (first $60–100K; ranges from existing files)
| Item | Range | Source |
|---|---|---|
| Phantom validation study (materials, scanner time, calibration) | $10–20K | `validation/BILL_OF_MATERIALS.csv` |
| Validation and QA spend, years 1–2 | $15–35K per year | `business/FINANCIAL_MODEL.xlsx` Inputs, Bootstrapped Base [AE] |
| Legal (formation, IP, pilot/SOW/DPA review) | within other opex of $15–22K per year | Same [AE] |
| Founder stipend | $12–40K per year | Same [AE] |
| Discovery travel and conferences | $150 per conversation [AE] | Same |

## 6. Risks
| Risk | Why it matters | Mitigation |
|---|---|---|
| **PI eligibility** | NSF SBIR/STTR and NIH SBIR need a PI >50% employed by the company at award [V]. The founder is a full-time student | NIH STTR with a faculty PD/PI; graduation timing; a hired PI. Get program-officer answers in writing |
| **IP ownership** | Use of university resources may bring the software within university ownership rules [RF/INF] | OTM determination before any investment, award or paid pilot (M0) |
| **Market ceiling** | Serviceable pool ≈ $0.8–3.9M per year at Base prices [V counts × AE volumes × HYP prices] | Treat venture scale as conditional on adjacent modules and non-US demand. Test before raising |
| **Separability** | Graft and new bone may be inseparable for some materials (`SCIENTIFIC_EVIDENCE.md` §1 #5, R3) | Material characterisation states "not separable" honestly. Total mineral is not a safe fallback: in the held-out simulation S1H3 (SYNTHETIC), total mineral volume supported in 10% of held-out specimens (sharp imaging only), new-bone volume was never supported, and no volume endpoint supported for 58% of held-out specimens; the model carries no feasibility or refused-endpoint term (`business/REVENUE_MODEL.md` §2a-bis; founder decision #20). **Day-0 is unproven under granule motion** (simulation, naive day-0 footprint graft Dice — no motion: 0.80; 50 µm motion: 0.535; 100 µm motion: 0.35; the advisor refuses those cases); **histology is the fallback** |
| **Free substitutes** | The Dragonfly academic licence is free; general platforms add deep learning [V] | Graft-specific value, abstention and audit trail. Test academic willingness to pay early (H4) |
| **Grant dependence** | Grants are conditional and restricted; the model's lead case counts none | The no-grant path (max deficit ~$96K, Bootstrapped Base) is the default plan; treat any award as project funding |
| **No licence on a public code base** | Licences are 56% of Bootstrapped Base 2031 revenue. In practice they are hard to collect: the full source is public with no LICENSE file, evaluation mode is fully functional, and the licence check can be removed from the public source. Legally, copyright may still be enforceable once ownership is settled, but no EULA, entity or production signing key exists and the OTM determination is open (counsel to confirm) | Founder decision on the code licence (`FOUNDER_DECISIONS.md`); without licence revenue Base 2031 revenue is $114K |
| **Third-party licence compliance of the desktop bundle** | The bundle ships LGPL Qt, LGPL-2.1 system libraries and many other components; notices were incomplete until cycle 2 and the archive packed before that must not be distributed | `packaging/bundle_inventory.py` now fails the build on any unmapped library; counsel to confirm the LGPL source arrangement and draft the EULA |
| **US patent bar dates 2027-11-27 and 2027-11-28** | The Generation-1 and most Generation-2 inventions became public on 2026-11-27; the advisor 1.4.0–1.4.3 mechanisms, external audit-chain anchors and fail-closed registration QC on 2026-11-28 (`docs/ip/INVENTION_REGISTER.md` §0a). The founder's own disclosure becomes US prior art after one year. Absolute-novelty jurisdictions (e.g. the EPO, China) are probably closed; some others (e.g. Japan, Korea) have grace periods with conditions — counsel must confirm | Decide on a provisional application, and on any filings in grace-period jurisdictions, well before the bar dates (practical decision date 2027-09; spring 2027 IP Clinic intake) — `FOUNDER_DECISIONS.md` #1, #19 |
| **Copyright and inventorship of AI-assisted code** | How much protectable authorship and inventorship AI-assisted work carries is an open question (cycle-1 IP-08) | Inventorship analysis with counsel before any filing; keep records of human contributions |
| **Early dilution / SAFE stacking** | Several small SAFEs (competitions, accelerators) compound before a priced round [INF] | Track every instrument in a cap table with counsel. Read SAFE terms before accepting prizes |
| **Founder bandwidth** | Student workload versus sales, delivery and validation | Wave-based discovery (10 conversations at a time); summer accelerator |
| **Compliance claims** | Any GLP, Part 11 or regulatory-acceptance claim would be false today | Language rules in `business/outreach_drafts/README.md`; validation-status line in every report |

## 7. What this document does not contain
- No named investors or individuals.
- No valuation figures (no citable source verified).
- No claim that any application has been made or any conversation has happened.
