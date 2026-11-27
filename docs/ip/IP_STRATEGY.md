# OsteoQuant: IP Strategy (trade secret vs patent vs publish)

**Prepared:** 2026-11-27.
**Inputs:**
- `docs/ip/INVENTION_REGISTER.md`
- `docs/ip/PATENT_LANDSCAPE.md` and `docs/ip/patents.csv`
- `docs/research/COMPETITOR_MATRIX.md`
- `docs/security/IP_PROVENANCE.md`
- `outreach/IP_AND_OTM_QUESTIONS.md`

> **PRELIMINARY: NOT LEGAL ADVICE.** Everything here is a decision-support draft for the founder to take to UIUC OTM and a registered patent attorney (or the Landuyt IP Clinic, which `IP_AND_OTM_QUESTIONS.md` records as Spring-semester only). Statements of general patent law are marked INF and must be confirmed by counsel.

## 1. Bottom line (preliminary)

1. **Settle ownership and inventorship before spending on patents.**
   - The code was written with an AI coding tool on the founder's directive (`IP_PROVENANCE.md` §1).
   - The USPTO's revised guidance (2025-11-26) states that only natural persons can be inventors, AI tools are tools, and the touchstone is **conception** [V: uspto.gov notice, accessed 2026-11-27].
   - The founder must document which ideas they conceived (dated directive or playbook, notes).
   - Ownership: the founder is a UIUC undergraduate and OTM has not made a determination. Do not assume ownership either way.
2. **The moat is data, validation and process, not algorithms.** The landscape shows that the closest algorithmic ideas have dense prior art: baseline registration, uncertainty gating, hash-chained audit. Most value sits in material-specific reference data, physical-phantom calibration, trained weights, a validation dossier and know-how. Those are **trade secrets** and need active protection.
3. **At most one provisional is worth considering now**, and only if publication is imminent. Candidate scope: the **material/timepoint-aware endpoint gating** (INV-03) combined with the **separability-oracle feasibility advisor** (INV-02) and the **day-0 footprint protocol** (INV-01) as embodiments.
   - These are mostly Concept today. A provisional must enable what it describes (INF), so a filing **after** the physical-phantom data exist will be stronger.
   - If the founder intends to submit Manuscript 1 or a preprint first, a provisional filed beforehand preserves options (INF).
4. **Publish deliberately** (defensive publications and credibility): the audit design (INV-05), the border-convention note (INV-07) and the benchmark protocol/metrics (INV-06 protocol only). Hold back the gating rules, material thresholds, phantom calibration data and trained weights.
5. **Clear FTO on one active family before shipping the longitudinal module:** Nobel Biocare **US9036899B2 / EP2579778B1** (expiry shown 2032-02-06). Also brief the attorney on GE **US11972593B2** before adding auto-placed measurements with uncertainty prompts. Both are preliminary **Medium** flags.

## 2. Asset-by-asset recommendation

| Asset | Protection route (preliminary) | Why | Actions |
|---|---|---|---|
| Material/timepoint endpoint-gating rules + separability thresholds (INV-02/03) | **Keep confidential.** Provisional candidate (decision D-IP-3) | Most distinctive. Not yet reduced to practice in product. §101 and obviousness risk | Implement in code with dated commits; attorney consult before any publication |
| Per-material reference library, physical-phantom calibration, scanner personalities | **Trade secret** | Not visible in output. Hard to reverse-engineer. Grows over time | Keep out of any public repo. Access control. NDAs with collaborators. Mark "Confidential" |
| Trained model weights | **Trade secret** + licence terms | Licence-aware provenance already enforced (D-006). CC-BY attribution obligations for SPROUT-derived models (`IP_PROVENANCE.md` §2) | Encrypt or obfuscate distribution. EULA bans reverse engineering (counsel to draft) |
| Day-0 protocol parameters and failure-mode know-how (INV-01) | **Trade secret / know-how.** Possibly publish the general method later | Weak novelty vs Schulte 2011, Wehrle 2019, US9036899B2 | FTO review first |
| ROI detectors (INV-04) | **Trade secret / know-how** | Low patentability; invisible in output | None beyond confidentiality |
| Audit trail + review binding (INV-05) | **Publish**; copyright on code | Old prior art; publishing builds QA trust | Write a short design note for customers |
| Border-convention cross-walk (INV-07) | **Publish** | Credibility; low patent value | Fix post-hoc caveat (Q-10) before submission |
| Benchmark protocol & metrics (INV-06 protocol) | **Publish** (after D-IP-3 decision) | Establishes scientific standing. Sets the evaluation standard competitors must meet | Publish protocol, not calibration data |
| Source code | **Copyright** (automatic); keep proprietary | Permissive dependencies only; GPL tools not linked (`IP_PROVENANCE.md` §2) | Add licence headers/EULA later. Keep SBOM current |
| Name "OsteoQuant" | **Trademark** knockout search before wider outreach | Already used on landing page and decks | Clearance search (USPTO search system) via counsel or clinic |

## 3. Provisional filing considerations (INF unless marked V)

- **Fees** [V: USPTO fee schedule, effective 2025-01-19, last revised 2026-11-01, accessed 2026-11-27]: provisional application filing fee **$325 large / $130 small / $65 micro entity**. Micro-entity eligibility (37 CFR 1.29) depends on income limits and prior filings, or on an institution-of-higher-education basis. Counsel to confirm.
- **What a provisional does (INF):**
  - It establishes a U.S. priority date for what it **adequately describes and enables**.
  - It is not examined and expires after **12 months**. The non-provisional and/or PCT application must be filed within that window to claim priority.
  - New matter added later does not get the earlier date.
- **Content for a useful provisional:**
  - detailed method steps;
  - multiple embodiments (materials, defect models, day-0 vs no day-0);
  - concrete thresholds/decision logic;
  - flow diagrams;
  - pseudo-code;
  - experimental results (Exp C, C2, L, L2, K);
  - and, ideally, physical-phantom data.

  A thin "cover-sheet + slides" provisional often fails to support later claims (INF; counsel to advise).
- **Trade-off:** filing discloses nothing until publication (18 months from priority, INF). However, claims-worthy detail placed in a patent will eventually be public, so **do not put trade-secret calibration data into a filing** unless needed for enablement.
- **Foreign rights (INF):**
  - The U.S. has a one-year grace period for the inventor's own disclosures (35 U.S.C. 102(b)(1)).
  - The EPO, China, Japan and Korea generally require absolute novelty.
  - **Any public disclosure before filing (paper, preprint, poster, public GitHub, pitch with no NDA) may forfeit foreign rights.**
- **Subject-matter eligibility (INF):** image-analysis software claims face U.S. §101 (Alice) scrutiny. Claims tied to specific imaging acquisition (day-0 scan protocol), specific data transformations and changes to the analysis output are generally more defensible than abstract decision rules. The attorney must assess.
- **Cost reality (INF):** a provisional drafted by counsel typically costs far more than the filing fee. The Landuyt IP Clinic (Spring only; students pay USPTO fees, per `IP_AND_OTM_QUESTIONS.md`, not re-verified this session) is the low-cost route if timing fits.

## 4. What NOT to publish or send yet

Until decisions D-IP-1 to D-IP-4 are made:
1. `publications/MANUSCRIPT_1_separability.md`: do not submit or preprint. It discloses the Dice-optimal oracle (INV-02) and the day-0 footprint results (INV-01).
2. Any description of **endpoint gating rules** by material and timepoint (INV-03), including the EASY/HARD/UNDERDETERMINED table thresholds in `docs/science/SEPARABILITY_ANALYSIS.md`, in posters, talks, grant abstracts that become public, or emails without an NDA.
3. Physical-phantom calibration data, per-material histograms, scanner-personality parameters (`docs/science/phantom_parameters.json`) and trained weights.
4. Specific algorithm details in outreach emails (already advised in `IP_AND_OTM_QUESTIONS.md` §C4).
5. Hosting `web/landing/index.html` publicly is lower risk (it names a "Separability check" and "day-0 baseline scan" benefit without method detail). Still, decide **after** D-IP-1.

**OK to share now:** audit-trail design (INV-05), general product description, morphometry border-convention note (after Q-10 fix), competitor/market analyses.

## 5. Trade-secret hygiene (actions; INF)

1. **Repository visibility:** confirm today whether the GitHub repository is private. If it is or was public, record when, and tell the attorney; trade-secret status of anything pushed may be lost.
2. Move calibration data, weights and phantom parameters to a **separate private store** with access logging. Keep only placeholders in the code repository.
3. Use **NDAs** before technical discussions with collaborators and CROs. Use **invention-assignment** and confidentiality agreements with any contributor or advisor (counsel or the clinic for templates).
4. Keep a **dated invention log**: who conceived what and when, and which parts were tool-generated. Given the AI-assisted development, this is central to inventorship.
5. Label confidential documents. Keep the trade-secret inventory (Section 2) current.

## 6. Decisions required (founder + OTM + attorney)

| ID | Decision | Who | Inputs | Suggested timing |
|---|---|---|---|---|
| **D-IP-0** | Confirm GitHub repository visibility and history of any public exposure | Founder | GitHub settings | Immediately |
| **D-IP-1** | Obtain OTM ownership determination (file software/invention disclosure as OTM advises) | Founder + OTM | `IP_AND_OTM_QUESTIONS.md` A1–A4, this register | Before any filing, publication or external collaboration |
| **D-IP-2** | Inventorship analysis for AI-assisted work: which conceptions are the founder's | Founder + attorney | Directive/playbook, invention log, USPTO 2025-11-26 guidance | Before D-IP-3 |
| **D-IP-3** | File or skip a provisional covering INV-03 (+ INV-02, INV-01 embodiments) | Founder + attorney/clinic | Register, landscape, physical-phantom timeline, publication plan | Before Manuscript 1 or any preprint; ideally after phantom data |
| **D-IP-4** | FTO opinion on US9036899B2 / EP2579778B1 for the longitudinal module; brief on US11972593B2 | Attorney | `patents.csv`, design notes | Before commercial use of the longitudinal module |
| **D-IP-5** | Trademark clearance for "OsteoQuant" | Founder + counsel/clinic | Knockout search | Before wider outreach or incorporation |
| **D-IP-6** | Incorporation and IP assignment from founder to company (after OTM) | Founder + counsel | OTM outcome | With entity formation |
| **D-IP-7** | Publication plan: what to publish (INV-05, INV-07, benchmark protocol) and when | Founder | Sections 2 and 4 | After D-IP-3 |

## Addendum (2026-11-27) — repository visibility verified: PUBLIC
The GitHub repository `arnavhiteshpatel-cloud/playground` was checked through the GitHub search API and is
**public** (`"visibility": "public"`). Commits pushed between 2026-11-27 06:58 UTC (`deab961`) and 09:30 UTC
(`ee09a70`) are therefore publicly accessible. This publicly discloses the Generation-1 material: the day-0 graft
footprint propagation method, the Dice-optimal intensity-only oracle as a separability bound, the cortical-annulus
segmental ROI detector, the hash-chained audit design, the manuscripts in `publications/` and all experiment results.

Consequences to raise with a registered patent attorney (not legal advice):
* In the United States an inventor's own public disclosure starts a one-year grace period (35 U.S.C. 102(b)(1)(A)),
  so a US application covering those items would need to be filed by 2027-11-27.
* Most other jurisdictions apply absolute novelty; foreign patent rights for the disclosed items may already be lost.
* Generation-2 work (material-aware endpoint gating / measurement-support advisor, granule tracking, ROI
  propagation, ONNX runtime) has been **committed locally but not pushed** pending the founder's decision to make the
  repository private or to accept publication.

Founder actions: (1) decide repository visibility now; (2) include the disclosure dates above in the OTM/attorney
conversation; (3) note that the repository also contains copies of public datasets' derived results but no raw data.

**Founder decision (2026-11-27):** keep the repository public and push all work, including Generation-2 material.
Generation-2 inventions are therefore publicly disclosed from their push date; the US one-year grace-period note above
applies to them from that date as well.
