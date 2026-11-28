# OsteoQuant: IP Strategy (public code base: patent vs publish)

**Prepared:** 2026-11-27.
**Inputs:**
- `docs/ip/INVENTION_REGISTER.md`
- `docs/ip/PATENT_LANDSCAPE.md` and `docs/ip/patents.csv`
- `docs/research/COMPETITOR_MATRIX.md`
- `docs/security/IP_PROVENANCE.md`
- `outreach/IP_AND_OTM_QUESTIONS.md`

> **PRELIMINARY: NOT LEGAL ADVICE.** Everything here is a decision-support draft for the founder to take to UIUC OTM and a registered patent attorney (or the Landuyt IP Clinic, which `IP_AND_OTM_QUESTIONS.md` records as Spring-semester only). Statements of general patent law are marked INF and must be confirmed by counsel.

> **Cycle-2 rewrite (2026-11-27).** The repository is **public**, and the founder decided to keep it public and push
> all work (Addendum). Sections 1, 2, 4 and 5 are rewritten for a public code base: the gating rules, thresholds,
> advisor code, phantom-generator parameters, experiment results and manuscripts are **public**, so none of them can be
> a trade secret. Only material that has never been pushed (future measured reference data, customer data, physical
> phantom calibration, any future weights kept off the repository) can still be kept confidential.

## 1. Bottom line (preliminary)

1. **The US bar dates: 2027-11-27 and 2027-11-28 (so far).** The Generation-1 and Generation-2 material present on
   2026-11-27 (separability oracle, material/timepoint endpoint gating in the advisor, day-0 footprint, granule
   tracking, ROI propagation, characterisation) was publicly disclosed on 2026-11-27. The advisor 1.4.0–1.4.3
   mechanisms (scan-measured blur, blur-scaled ambiguous rim, new-bone error propagation, method binding, read-time
   support evaluation, unspecified-material rim proxy, worst-case mineral rim gate), external audit-chain anchors and
   fail-closed registration QC were publicly disclosed on 2026-11-28 (per-invention table:
   `docs/ip/INVENTION_REGISTER.md` §0a). Under 35 U.S.C. 102(b)(1)(A) the founder's own disclosure becomes US prior
   art one year later (INF; counsel to confirm). Outside the US the position is mixed and must be confirmed by counsel
   (§3): absolute-novelty jurisdictions are probably closed, but some jurisdictions have grace periods with
   conditions. Each further push of **new** inventive work starts its own one-year clock. The file-or-forgo decisions
   are listed with their deadlines in `FOUNDER_DECISIONS.md` #1 and #19 (practical decision date 2027-09; spring 2027
   IP Clinic intake).
2. **Settle ownership and inventorship first.**
   - The code was written with an AI coding tool on the founder's directive (`IP_PROVENANCE.md` §1).
   - The USPTO's revised guidance (2025-11-26) states that only natural persons can be inventors, AI tools are tools,
     and the touchstone is **conception** [V: uspto.gov notice, accessed 2026-11-27].
   - How much protectable copyright authorship AI-assisted code carries is an open question for counsel.
   - Ownership: the founder is a UIUC undergraduate and OTM has not made a determination. Do not assume ownership
     either way.
3. **The moat is data, validation and service, not algorithms or code.** The algorithms are public and the closest
   ideas have dense prior art (baseline registration, uncertainty gating, hash-chained audit). What competitors cannot
   copy from the repository: measured material reference data and physical-phantom results (once they exist and if
   they are kept off the public repository), validation evidence, customer relationships, study-design know-how and
   the analysis service.
4. **The code licence is undecided and matters for revenue.** There is no `LICENSE` file and no licence field in
   `pyproject.toml`. Public code without a licence is "all rights reserved" by default (INF), but GitHub's terms of
   service let other users view and fork a public repository (counsel to confirm the scope). Four separate points
   bear on licence revenue (56% of the Base 2031 model), and they should not be conflated:
   - *copyright* in the code may still be enforceable once ownership is settled (INF; extent for AI-assisted code
     unclear);
   - there is no EULA and no entity to grant or enforce a licence;
   - the OTM ownership determination is open;
   - *practically*, a fully functional evaluation mode and a licence check are in the public source, and the check can
     be removed by anyone who builds from source.

   Options (proprietary, source-available such as PolyForm Noncommercial or BSL, or open source) are a founder
   decision with counsel (`FOUNDER_DECISIONS.md` #2).
5. **Clear FTO on one active family before offering the longitudinal module:** Nobel Biocare **US9036899B2 /
   EP2579778B1** (expiry shown 2032-02-06). Also brief the attorney on GE **US11972593B2** before adding auto-placed
   measurements with uncertainty prompts. Both are preliminary **Medium** flags.

## 2. Asset-by-asset recommendation (public code base)

| Asset | Status | Protection route (preliminary) | Actions |
|---|---|---|---|
| Material/timepoint endpoint-gating rules, separability thresholds, advisor code (INV-02/03) | **Public** since 2026-11-27; the advisor 1.4.0–1.4.3 mechanisms (INV-08a–e) since 2026-11-28 | Patent only (US, before 2027-11-27, or 2027-11-28 for the 28 Nov mechanisms; possibly grace-period jurisdictions, see §3) or nothing; no trade secret possible | Founder decision on a provisional with counsel (D-IP-3); founder decisions #1 and #19 |
| Day-0 protocol and footprint method, granule tracking (INV-01) | **Public** | As above; weak novelty vs Schulte 2011, Wehrle 2019, US9036899B2 | FTO review (D-IP-4) before offering it |
| ROI detectors and ROI propagation (INV-04) | **Public** | Low patentability; copyright in the code only | None |
| Phantom-generator parameters (`docs/science/phantom_parameters.json`), knowledge-base material profiles, experiment results, manuscripts | **Public** | Copyright only; publication value (credibility) | Publish deliberately; cite the repository |
| Trained model weights in `models/` | Registry and any weights pushed are **public**; the desktop bundle ships none | Licence terms (once a licence exists) + CC-BY attribution for models derived from CC-BY data (`ATTRIBUTION.md`) | Decide whether future weights stay off the public repository |
| Future measured material references, physical-phantom calibration, scanner-specific parameters | **Not yet created** | Can be kept confidential **only if never pushed** | Store in a private location with access logging from day one; NDAs with collaborators |
| Customer data and customer-specific adapted weights | Not yet existing | Confidentiality under the DPA; never public | Already required by `business/templates/DPA_ISSUES_CHECKLIST.md` |
| Audit trail + review binding (INV-05; external audit-chain anchors since 2026-11-28), border-convention cross-walk (INV-07), benchmark protocol (INV-06) | Public | Publish (credibility) | Write short design notes |
| Source code | **Public, no licence chosen** | Copyright (automatic; extent for AI-assisted code unclear); licence choice pending | The product **links LGPL-3.0 Qt/PySide6 dynamically** and ships GPL-2 font files with their licence and source; whichever licence is chosen must be compatible with those and keep the LGPL relinking carve-out. Keep the SBOM current (`docs/security/SBOM.csv`, regenerated by `packaging/bundle_inventory.py`) |
| Name "OsteoQuant" (and "DefectFill") | Used on the site, reports and app | **Trademark** knockout before publishing the website or wider outreach | Clearance search via counsel or the IP Clinic (D-IP-5) |

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
- **Foreign rights (INF; corrected 2026-11-28, cycle-3 review C3-BIZ-08; counsel must confirm every point):**
  - The U.S. has a one-year grace period for the inventor's own disclosures (35 U.S.C. 102(b)(1)).
  - The EPO and China generally require absolute novelty, so the disclosed material is probably not patentable there.
  - Some jurisdictions have grace periods for the applicant's own disclosure, with conditions (for example, formal
    steps about the disclosure when filing). Japan and Korea are examples; the cycle-3 review also names Canada and
    Australia. Whether any of them applies to these disclosures, which conditions apply, and by which date a PCT or
    national filing would have to be made, is for a registered patent attorney to confirm.
    "Foreign rights are already lost" overstates the position; "may be lost unless counsel confirms a grace-period
    route" is the accurate statement.
  - **Any public disclosure before filing (paper, preprint, poster, public GitHub, pitch with no NDA) may forfeit
    rights in absolute-novelty jurisdictions.**
- **Subject-matter eligibility (INF):** image-analysis software claims face U.S. §101 (Alice) scrutiny. Claims tied to specific imaging acquisition (day-0 scan protocol), specific data transformations and changes to the analysis output are generally more defensible than abstract decision rules. The attorney must assess.
- **Cost reality (INF):** a provisional drafted by counsel typically costs far more than the filing fee. The Landuyt IP Clinic (Spring only; students pay USPTO fees, per `IP_AND_OTM_QUESTIONS.md`, not re-verified this session) is the low-cost route if timing fits.

## 4. Publication and disclosure from now on

Everything already pushed is public; withholding it achieves nothing. What still matters:
1. **New inventive work** (e.g. a new advisor mechanism, a tracking method that works under motion, phantom-derived
   calibration): decide **before pushing** whether it goes to a private store first (founder decisions #2 and #17 in
   `FOUNDER_DECISIONS.md`). Each push of new inventive work opens its own one-year US clock and ends any
   confidentiality. On 2026-11-28 new advisor mechanisms were pushed under the 27 Nov instruction to push all work
   (Addendum); see Addendum 2.
2. **Manuscripts and preprints** of material already public do not change the bar date for that material, but they
   can disclose new detail; check against the provisional decision (D-IP-3) first.
3. **Physical-phantom and measured material data:** keep off the public repository until a decision on their use is
   made; they are the only technical assets that can still be confidential.
4. **Third-party material in the repository** (non-privileged FTO triage `PATENT_LANDSCAPE.md` / `patents.csv`,
   prospect lists, a named faculty member without recorded consent, runtime logs): whether to remove them, and whether
   to rewrite history, is a founder decision with counsel (`FOUNDER_DECISIONS.md`); history rewriting does not cure
   copies already taken.

## 5. Hygiene (actions; INF)

1. **Private store** for anything that should stay confidential (future calibration data, measured references,
   customer data), with access logging. Keep only placeholders in the public repository.
2. **NDAs** before technical discussions about unpublished work; **invention-assignment** and confidentiality
   agreements with any contributor or advisor (counsel or the clinic for templates).
3. **Dated invention log**: who conceived what and when, and which parts were tool-generated. Given the AI-assisted
   development, this is central to inventorship (D-IP-2).
4. Record the push date of every new inventive change, so each one-year clock is known. The table is
   `docs/ip/INVENTION_REGISTER.md` §0a (first entries for the 2026-11-28 pushes added on 2026-11-28).

## 6. Decisions required (founder + OTM + attorney)

| ID | Decision | Who | Inputs | Suggested timing |
|---|---|---|---|---|
| **D-IP-0** | Confirm GitHub repository visibility and history of any public exposure | Founder | GitHub settings | **Done**: public; founder decided to keep it public (Addendum) |
| **D-IP-1** | Obtain OTM ownership determination (file software/invention disclosure as OTM advises) | Founder + OTM | `IP_AND_OTM_QUESTIONS.md` A1–A4, this register | Before any filing, publication or external collaboration |
| **D-IP-2** | Inventorship analysis for AI-assisted work: which conceptions are the founder's | Founder + attorney | Directive/playbook, invention log, USPTO 2025-11-26 guidance | Before D-IP-3 |
| **D-IP-3** | File or skip a US provisional covering the publicly disclosed inventions (INV-03 + INV-02, INV-01 and the Gen-2 advisor, tracking and ROI-propagation embodiments) | Founder + attorney/clinic | Register, landscape, physical-phantom timeline | **Hard deadlines: US bar dates 2027-11-27 (27 Nov material) and 2027-11-28 (28 Nov material)**; practical decision date 2027-09; apply for the spring 2027 IP Clinic intake; non-US filings: founder decision #19 |
| **D-IP-4** | FTO opinion on US9036899B2 / EP2579778B1 for the longitudinal module; brief on US11972593B2 | Attorney | `patents.csv`, design notes | Before commercial use of the longitudinal module |
| **D-IP-5** | Trademark clearance for "OsteoQuant" | Founder + counsel/clinic | Knockout search | Before wider outreach or incorporation |
| **D-IP-6** | Incorporation and IP assignment from founder to company (after OTM) | Founder + counsel | OTM outcome | With entity formation |
| **D-IP-7** | Publication plan: what to publish (INV-05, INV-07, benchmark protocol) and when | Founder | Sections 2 and 4 | After D-IP-3 |

## Addendum (2026-11-27) — repository visibility checked: PUBLIC
The GitHub repository `arnavhiteshpatel-cloud/playground` was checked through the GitHub search API and is
**public** (`"visibility": "public"`). Commits pushed between 2026-11-27 06:58 UTC (`deab961`) and 09:30 UTC
(`ee09a70`) are therefore publicly accessible. This publicly discloses the Generation-1 material: the day-0 graft
footprint propagation method, the Dice-optimal intensity-only oracle as a separability bound, the cortical-annulus
segmental ROI detector, the hash-chained audit design, the manuscripts in `publications/` and all experiment results.

Consequences to raise with a registered patent attorney (not legal advice):
* In the United States an inventor's own public disclosure starts a one-year grace period (35 U.S.C. 102(b)(1)(A)),
  so a US application covering those items would need to be filed by 2027-11-27.
* Many other jurisdictions apply absolute novelty; foreign patent rights for the disclosed items may already be lost
  there. Some (e.g. Japan, Korea) have grace periods with conditions (corrected 2026-11-28; see §3).
* Generation-2 work (material-aware endpoint gating / measurement-support advisor, granule tracking, ROI
  propagation, ONNX runtime) has been **committed locally but not pushed** pending the founder's decision to make the
  repository private or to accept publication.

Founder actions: (1) decide repository visibility now; (2) include the disclosure dates above in the OTM/attorney
conversation; (3) note that the repository also contains copies of public datasets' derived results but no raw data.

**Founder decision (2026-11-27):** keep the repository public and push all work, including Generation-2 material.
Generation-2 inventions are therefore publicly disclosed from their push date; the US one-year grace-period note above
applies to them from that date as well.

## Addendum 2 (2026-11-28) — further public disclosures (facts)
After `FOUNDER_DECISIONS.md` was created (2026-11-28, 00:05 UTC) with decision #2 marked "now, before the next push",
the following were committed and pushed to the public `origin` on 2026-11-28, under the founder's 27 Nov instruction
above (commit times UTC; details in `docs/ip/INVENTION_REGISTER.md` §0a):
* advisor 1.4.0 (`a22da5a`, 00:25): scan-measured blur; new-bone error propagation; measured ambiguous graft rim;
* advisor 1.4.1 (`7a3ae70`, 00:30): blur-scaled ambiguous rim;
* advisor 1.4.2 (`cfad464`, 00:34): method binding;
* `4b5e84c` (01:37): read-time support evaluation; advisor 1.4.3 (unspecified-material rim proxy, worst-case mineral
  rim gate); external audit-chain anchors; registration QC that fails closed.

Their US one-year date is 2027-11-28 (INF; counsel to confirm). No prior-art search has been done for them. Whether
the 27 Nov instruction continues to govern pushes is founder decision #17.
