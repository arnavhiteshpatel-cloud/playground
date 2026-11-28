# Cozad New Venture Challenge 2027: Application Package (DRAFT)

**Prepared:** 2026-11-27. Labels follow FUNDING_OPPORTUNITIES.md.

> **What is and isn't known about the 2027 form.**
> - The 2027 registration form and rule book are **not public yet** [UNR]. Registration opens Dec 1, 2026 [V calendar].
> - Registration runs on a rolling weekly basis through **Feb 2, 2027** [CC].
> - This package is built from:
>   - the current FAQ, rules and prizes pages [V];
>   - the **2018–19 Official Rules, Guidelines and Judging Criteria** [V-old] (https://ws.engr.illinois.edu/blogs/getfile/60/31061). That document lists the registration "executive summary" fields, the pitch formats and the judging criteria.
> - Re-map these drafts to the 2027 form when it is released.

---

## A. Eligibility and logistics checklist

| Item | Requirement | Source | Status |
|---|---|---|---|
| Student status | "Students must be enrolled full-time at the University of Illinois Urbana-Champaign" | [V] FAQ | [FOUNDER: confirm full-time, spring 2027] |
| Team | "All teams must include at least one full-time, degree-seeking student"; solo entry allowed | [V] FAQ | OK |
| Health prizes | Sports Medicine and Healthcare Innovation: "teams must have at least one CI MED student" | [V] rules page (2024–25 framework) | **Recruit a Carle Illinois MD student** [action] |
| Venture limits (historical) | Excluded if revenue >$50k or outside equity >$50k | [V-old] 2018–19 | OK (none) |
| Prize receipt | Top cash prizes are SAFEs [V]. In 2019, prizes >$500 required forming a company and becoming a university vendor [V-old] | FAQ / 2018–19 | Plan the entity type (C-corp is typical for SAFEs [INF]) |
| IP | "The University and the Landuyt Center do not receive the right to own your IP if you participate" | [V] FAQ | Separate University ownership question under General Rules: see §G |
| Confidentiality | 2018–19: all events "accessible to the general public"; no confidentiality | [V-old] | **Do not disclose unfiled patentable details** |
| Registration window | Dec 1, 2026 → Feb 2, 2027 (rolling weekly) | [CC] | Register in the **first week of December** |
| Contacts | landuyt@illinois.edu (program address) | [V] | Do not contact until the founder decides |

---

## B. Registration "executive summary" (11 fields, per the 2018–19 form [V-old])

1. **Title of business / concept:** OsteoQuant
2. **Team leader name:** [FOUNDER NAME]
3. **One-line pitch (≤~200 characters; describe it, do not sell it):**
   > OsteoQuant is software that measures how much new bone versus leftover graft forms in preclinical micro-CT, with error bars and an audit trail, for orthobiologic R&D teams and CROs.

   (181 characters)
4. **Team (names, roles, capabilities, objectives):**
   - [FOUNDER]: technical lead, built the prototype (segmentation, morphometry, reports, synthetic benchmark). Objective: physical validation and customer discovery.
   - [OPEN ROLE: Carle Illinois MD student]: clinical and preclinical context; enables health-prize eligibility.
   - [OPEN ROLE: business/Gies student]: customer discovery, pricing, financial model.
   - [ADVISOR: faculty, musculoskeletal or imaging]: scientific guidance.
5. **Problem:** Graft-based bone-regeneration studies hinge on separating new bone from residual graft in micro-CT. The two can look alike. Today's threshold-and-hand-contour workflow is slow, operator-dependent and hard to audit. As a result, sponsors and reviewers cannot fully trust reported "new bone" numbers [INF: validate in interviews].
6. **Solution:** Three-class segmentation (new bone / residual graft / host bone) that uses material-aware models and reports uncertainty. It produces standard morphometry and an audited, reproducible report. It is designed to be validated against physical phantoms with known ground truth; that validation has **not** yet been performed, and until it is, the software abstains from graft/new-bone measurements it cannot support.
7. **Customer segment(s):** B2B. The segments are orthobiologic and bone-graft-substitute companies (R&D and preclinical), preclinical CROs running bone-defect models, and academic musculoskeletal labs and imaging cores [HYP: rank after ≥30 interviews].
8. **Value proposition:** Hours per specimen become minutes [PENDING RESULT: time study]. The aim is numbers whose measurement support is stated per endpoint (and not reported where graft and new bone cannot be separated), with group confidence intervals, consistent results across operators and sites, and an audit trail a sponsor can inspect [HYP].
9. **Target market:** [PLACEHOLDER: bottom-up estimate = # organizations × studies/yr × specimens/study × price. Every input must come from interviews or a cited source. Do not invent a TAM.]
10. **Competitors (how the problem is solved today):** Scanner-vendor analysis software and commercial micro-CT packages, open-source image tools, in-house scripts and manual analysis [CC: general knowledge; build a feature-comparison table from public product documentation].
11. **Competitive advantage:** Graft/new-bone separation to be benchmarked on physical ground truth (planned; not started). Aims to calibrate uncertainty per endpoint (not achieved yet). Audited, versioned reports. A low-label path to new graft materials [HYP until validated].

---

## C. 90-second elevator pitch (one static 16:9 slide; only an Illinois student presents) [V-old format]

> **[0:00–0:15] Problem.** Every new bone-graft product is tested in animals, and the key readout is a micro-CT scan. The hard question is how much of that white stuff is new bone and how much is graft that hasn't dissolved yet. Today an analyst draws thresholds and contours by hand. It takes hours, and two analysts can disagree.
> **[0:15–0:40] Solution.** OsteoQuant separates new bone, residual graft and host bone automatically. It tells you how confident it is, and every report is fully traceable.
> **[0:40–0:60] Proof so far (honest).** We have a working prototype and a synthetic benchmark. [PENDING RESULT: one headline number from the synthetic benchmark, or omit.] Next we validate on physical phantoms scanned on Beckman's Zeiss Versa micro-CT.
> **[0:60–0:75] Market.** Our customers are orthobiologic companies, the CROs that run their animal studies, and academic labs. [PENDING: "We've interviewed N of them; X said…" — only after interviews.]
> **[0:75–0:90] Ask.** We're looking for a musculoskeletal faculty mentor, a Carle Illinois teammate, and introductions to preclinical CROs.

**Single slide content:** logo + one-line pitch, a 3-panel image (raw scan → 3-class overlay → report with CI), and three bullets: *Separates graft vs. new bone · Reports uncertainty · Audited reports*.

---

## D. Final pitch: 5 minutes + 3 minutes Q&A (PowerPoint 16:9) [V-old format]

| # | Slide | Content | Evidence status |
|---|---|---|---|
| 1 | Title | OsteoQuant: auditable bone-regeneration quantification | — |
| 2 | Problem | Overlapping attenuation; manual thresholds; variability; no audit trail | [INF] + interview quotes [PENDING] |
| 3 | Who feels it | Personas: CRO study director, orthobiologic R&D scientist, academic PI | [PENDING: interviews] |
| 4 | Solution / demo | Before/after 3-class overlay; report screenshot with CI | Prototype exists; use synthetic or phantom images, **labeled as such** |
| 5 | Validation plan & results | Synthetic benchmark → physical phantoms → expert comparison (ICC, Bland–Altman, time) | [PENDING RESULT: …] for each |
| 6 | Why now / why us | Accessible high-resolution micro-CT (Beckman Versa); ML uncertainty methods; founder-built prototype | [V] Beckman scanner exists |
| 7 | Market | Bottom-up sizing from interviews | [PENDING] |
| 8 | Business model | Per-study license + validation services → annual CRO license | [HYP] |
| 9 | Competition | Matrix: vendor software / open source / manual vs. OsteoQuant (separation, uncertainty, audit) | [CC] |
| 10 | Go-to-market | Academic design partners → CRO pilots → orthobiologic companies | [HYP] |
| 11 | Milestones & funding | Cozad → iVenture → NSF SBIR Phase I (Jul 2027) / NIH STTR | See the milestones in COMMERCIALIZATION_PLAN_GRANT.md |
| 12 | Team & ask | Roles, advisor gaps, specific asks | — |

**Likely Q&A to rehearse:**
- "Is this a medical device / FDA?" Answer: no. It is a preclinical research tool, though GLP-style auditability matters [INF].
- "What if graft and bone are truly inseparable?" Answer: Aim 1 measures exactly where they are separable, and uncertainty flags the ambiguous cases.
- "Why won't the scanner vendor do this?"
- "Who pays, and how much?"
- "Who owns the IP?" (see §G)
- "How do you get scans?"

---

## E. Five-page business summary outline (due before the Demo Showcase) [V-old requirement]

1. **Executive summary** (½ page)
2. **Problem and customer evidence** (¾ page): interview count, quotes and segments [PENDING]
3. **Solution and technology** (¾ page): 3-class segmentation, uncertainty, audit trail, phantom benchmark, with honest status
4. **Market and business model** (¾ page): bottom-up sizing [PENDING]; pricing hypotheses; design-partner pilots
5. **Competition and advantage** (½ page)
6. **Go-to-market and milestones** (½ page)
7. **Team and advisors** (½ page)
8. **Financials and funding plan** (½ page): non-dilutive first (iVenture, NSF/NIH), Cozad SAFE, then Illinois Ventures pre-seed after validation
9. **Risks and mitigations** (¼ page): see RISK in COMMERCIALIZATION_PLAN_GRANT.md

---

## F. Business Model Canvas (draft; all [HYP])

| Block | Draft |
|---|---|
| Customer segments | CROs (bone-defect models); orthobiologic / graft companies; academic MSK labs and imaging cores |
| Value propositions | Graft vs. new-bone separation where identifiable (and explicit abstention where not); CIs on endpoints; hypothesised analyst time savings (unmeasured — to be tested in a timed study); audit trail |
| Channels | Direct sales to CRO study directors; ORS/TERMIS conferences; academic design partners; imaging-core referrals |
| Customer relationships | Design-partner pilots; validation reports per material; support SLAs |
| Revenue streams | Per-study fee; annual site license; validation-as-a-service for new materials |
| Key resources | Phantom benchmark data; trained models; audit/reporting engine; scanner access |
| Key activities | Validation; material library expansion; QA/QMS documentation |
| Key partners | Beckman Imaging Technology Group; faculty advisor; CROs; graft manufacturers |
| Cost structure | Engineering; compute; scan time; phantom materials; validation studies; QMS |

---

## G. IP and disclosure guardrails before any public Cozad event

1. **Ownership check.** The UI System guidance [CC] is that the University owns IP developed "by anyone, including students, using University facilities, equipment or funds". Scans on the Beckman Versa and any RA work could trigger this. Request an IP determination from the Office of Technology Management **before** forming the company or pitching publicly [INF].
2. **Patentability.** If any method is patentable (for example, a phantom design or the uncertainty-propagation method), discuss filing (provisional) through the **Landuyt IP Clinic** (spring only [V]) or OTM **before** the elevator pitch. Cozad events have no confidentiality [V-old].
3. **Data.** Use only data you have rights to show. Label synthetic and phantom images clearly.

## H. Prize targeting (2026 prize list as the guide [V]; the 2027 list is [UNR])

| Prize (2026) | Fit | Requirement / note |
|---|---|---|
| Top placements ($100k / $50k / $25k SAFEs) | Medium–high | Requires customer evidence and a crisp story |
| Microsoft Azure credits ($25k, AI software startups) | High | Compute for model training |
| Carle Illinois Health Innovation Prizes ($25k total) | Medium | Needs a CI MED teammate [V rules] |
| Sports Medicine Prize ($20k) | Low–medium | Needs a CI MED teammate; bone healing is adjacent |
| Landuyt Business & Engineering Partnership ($5k ×4) | Medium | Recruit a Gies co-founder |
| Grainger Innovation Fund Technology Advancement ($5k ×4) | Medium | Technology progress |
| Heinz MedTech Prize | Not eligible | Requires a Class II+ device [V] |
| EnterpriseWorks / Research Park awards | Medium | Student startup tenancy [CC] |

## I. Timeline (founder to fill)

| Date | Task |
|---|---|
| Week of Dec 1, 2026 | Register; read the 2027 rule book; calendar all mandatory workshops |
| Dec 2026 – Jan 2027 | 20+ customer interviews (Illinois I-Corps workshop methods); recruit a CI MED teammate and a Gies teammate |
| Jan 2027 | OTM IP determination; IP Clinic application; first phantom scans (if access is approved) |
| Feb 2, 2027 | Registration deadline (latest) |
| Feb–Mar 2027 | Workshops; elevator pitch; [PENDING RESULT: first phantom results] |
| Apr 2027 | Demo Showcase and Finals (date [UNR]; 2026 Demo Day was Apr 16 [CC]) |
