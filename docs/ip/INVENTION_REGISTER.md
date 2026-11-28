# OsteoQuant: Invention Register (candidate inventions and prior art)

**Prepared:** 2026-11-27, from the repository as of that date: code, `EXPERIMENT_REGISTRY.md`, `docs/science/SEPARABILITY_ANALYSIS.md`, `DECISIONS.md` and the manuscript drafts in `publications/`. Prior-art citations are in `docs/ip/PATENT_LANDSCAPE.md` and `docs/ip/patents.csv`. DOIs were verified via Crossref/Europe PMC this session unless marked otherwise.

> **PRELIMINARY: NOT LEGAL ADVICE.** The novelty hypotheses and recommendations here are an engineer's triage, not opinions on patentability, inventorship or ownership. A registered patent attorney must review any filing decision. University ownership is **not** concluded here. Questions are listed for the UIUC Office of Technology Management (OTM).

## 0. Facts that apply to every entry

| Topic | Fact (evidence) | Implication |
|---|---|---|
| **Creation date** | Git history: first commit `deab961`, 2026-11-27; 15 commits, all dated 2026-11-27 [V: `git log`] | Dated record of reduction to practice (simulation level) |
| **How code was written** | `docs/security/IP_PROVENANCE.md` §1: all code and documents were generated **by an AI coding tool acting on the founder's written directive**, in a commercial cloud container, not on university computers [V: repo] | **Inventorship risk.** Under the USPTO's revised guidance (published 2025-11-26, rescinding the Feb 2024 guidance), "only natural persons can be properly named as inventors", AI systems "are tools used by human inventors", and "the touchstone of inventorship" is **conception** [V: https://www.uspto.gov/subscription-center/2025/revised-inventorship-guidance-ai-assisted-inventions, accessed 2026-11-27]. For each entry, the founder must be able to show they **personally conceived** the definite and permanent idea (e.g. in the directive or playbook), not just accepted a tool's output. **Attorney question.** |
| **Repository hosting** | `origin` on **github.com** under a personal account, repository `playground`. **Visibility: PUBLIC** (checked 2026-11-27, `docs/ip/IP_STRATEGY.md` Addendum); the founder decided to keep it public and push all work. Generation-1 and Generation-2 commits were pushed on 2026-11-27 [V] | **Every entry below is publicly disclosed** as of 2026-11-27: single US bar date **2027-11-27** (35 U.S.C. 102(b)(1)(A), INF); foreign rights likely lost; no entry can be a trade secret. New inventive work pushed later starts its own one-year clock. Decision and deadlines: `FOUNDER_DECISIONS.md` |
| **Outward-facing drafts in repo** | `web/landing/index.html` mentions a "day-0 baseline scan" benefit and a "Separability check". `investor/ONE_PAGE_OVERVIEW.md` (rewritten in cycle 2) states that day-0 works in simulation only without granule motion. `publications/MANUSCRIPT_1_separability.md` describes the Dice-optimal oracle and the day-0 footprint in detail [V: repo] | Not a disclosure until published or sent. Treat as **do-not-send** until filing decisions are made (see `IP_STRATEGY.md`) |
| **University context** | Founder is a UIUC undergraduate. `outreach/IP_AND_OTM_QUESTIONS.md` lists open OTM questions. `docs/security/IP_PROVENANCE.md` states no university data, equipment or funds were used [V: repo] | Ownership determination by OTM is pending (do not assume) |

**Status codes:**
- **RTP-sim**: reduced to practice in simulation/code.
- **RTP-code**: implemented and tested in code.
- **Concept**: documented but not implemented in the product.

---

## INV-01: Day-0 graft-footprint propagation for residual-graft quantification

**Description:**
- A post-implantation (day-0) micro-CT is acquired. The graft is segmented on it, using its known high contrast at day 0 or the material's known geometry.
- Each later scan is **rigidly registered** to day 0, with the metric masked to host anatomy (D-012).
- Later mineral inside the defect ROI is labelled:
  - **residual graft** if it lies within the (optionally eroded) day-0 graft footprint;
  - **new bone** if it lies inside the ROI and outside the footprint;
  - **host** if it lies outside the ROI or in a host mask.
- Per-timepoint class volumes and the remaining-graft fraction Gr.V/Gr.V0 follow.
- Code: `osteoquant/longitudinal/core.py` (`register`, `day0_propagation`, `class_volume_change`). Evidence: Experiments L and L2. With strut-like graft that mimics new bone, the method gave graft Dice 0.816, against 0.663 (RF), 0.318 (multi-Otsu) and 0.323 (intensity oracle).
- **Status: RTP-sim.**

**Novelty hypothesis:**
- The general idea of registering baseline and follow-up scans is old.
- The specific combination may be new:
  - (i) using the day-0 **graft** footprint as a class prior to split later mineral into residual graft vs new bone, **for bone-like grafts where intensity cannot separate them**;
  - (ii) erosion tolerance for bone apposed on graft surfaces;
  - (iii) reporting Gr.V/Gr.V0 with registration-error (TRE) qualification.

**Closest prior art found:**
- **US9036899B2 / EP2579778B1** (Nobel Biocare; active; expiry shown 2032-02-06): registers two CT volumes, selects a landmark/clipping-plane ROI, segments local bone and subtracts volumes. This is total bone change, not class assignment, but it is close.
- **Schulte et al., Bone 2011** (doi:10.1016/j.bone.2010.10.007): time-lapsed in vivo µCT formation/resorption from registered scans.
- **Wehrle et al., Sci Rep 2019** (doi:10.1038/s41598-019-53822-x): fracture-healing VOIs "created automatically from the post-operative measurement" with registration of consecutive scans.
- **Francis-Pester et al., J Clin Med 2022** (doi:10.3390/jcm11195514): models a "timepoint-0" graft and compares it with the follow-up graft volume (Latarjet).
- **US8634626B2** (CUHK; expired): baseline/follow-up bone registration.
- Clinical CBCT graft-resorption protocols registering post-op and 6-month scans (search results; e.g. PMC7817723, not fetched).

**Preliminary assessment:**
- Novelty over the combined art is **uncertain to weak**; obviousness risk is **high**. A person skilled in time-lapse µCT would likely consider labelling "present at day 0 = graft".
- The value is mostly **know-how**: when it works, erosion settings, failure modes such as creeping substitution where it under-performed RF in the easy regime (Exp L), and the study-design protocol.

**Recommendation (preliminary):**
- **Trade secret for the tuned protocol and parameters.**
- **Publish the general method** (defensive) once ownership is settled, unless the attorney identifies a narrow claim worth a provisional, e.g. combining it with INF-02/03 gating.
- **FTO review of Nobel Biocare is required** before commercial use (see landscape).

**Ownership questions (OTM):**
- Was the day-0 idea discussed with or derived from any UIUC lab work (prior research employment listed in `IP_AND_OTM_QUESTIONS.md` A3)?
- Will future day-0 scans use Beckman equipment?

**Disclosure risk:**
- Described in `publications/MANUSCRIPT_1_separability.md`, `investor/ONE_PAGE_OVERVIEW.md` and `web/landing/index.html`.
- Exposed if the GitHub repository is public.

---

## INV-02: Dice-optimal intensity-only separability oracle used as a feasibility advisor that triggers abstention

**Description:**
- Given class-conditional intensity histograms for graft and new bone, from phantoms, the material reference library or a labelled calibration subset, sort intensity bins by graft fraction.
- Scan superlevel sets of the likelihood ratio to find the **Dice-maximising union of bins**. This is an upper bound on graft Dice for *any* voxel-wise intensity rule at that binning.
- Code: `experiments/recompute_intensity_oracle.py::dice_oracle`. The independent review corrected an earlier accuracy-optimal bound (Q-01).
- Proposed product use (**Concept**, not implemented in `osteoquant/`):
  - before a study, or per scan, compute the oracle for the declared material, voxel size and noise;
  - if the bound is below a threshold, the advisor (a) recommends a day-0 scan, morphology features or histology, and (b) forces the report to **abstain** from intensity-based class volumes (see INV-03).
- **Status: RTP-sim for the oracle; Concept for the advisor/abstention trigger.**

**Novelty hypothesis:** Using an analytic, Dice-specific intensity-only upper bound, computed from known-truth class histograms, as a *gate* on whether an analysis may report class-specific endpoints, and as a *study-design recommender*.

**Closest prior art found:**
- **US11748877B2** (SUNY; active; expiry 2038-09-29): predicts segmentation quality with a classifier on patch intensity/texture features.
- **US8160357B2** (Canon; expired): predicts atlas segmentation overlap.
- **Valindria et al. 2017**, Reverse Classification Accuracy (arXiv:1702.03407; IEEE TMI): predicts segmentation performance without ground truth.
- **Geifman & El-Yaniv 2017** (arXiv:1705.08500): selective classification with a reject option.
- Bayes-error / class-overlap measures are textbook (INF; no specific citation verified).
- Stalder et al. 2014, Int J Mater Res 105(7):679 (from `docs/science/REFERENCES.md` R30; DOI not confirmed): a joint histology–µCT histogram shows overlapping BCP / new-bone classes.

**Preliminary assessment:**
- The oracle math (likelihood-ratio superlevel sets maximise a ratio metric) is likely **known or obvious**.
- The **application** (material- and voxel-size-specific pre-study feasibility gating that changes what a regulated-style report may state) may have **some novelty**. It is exposed to **§101 subject-matter risk** in the U.S. (abstract idea / mathematical concept; INF from general patent-law knowledge; attorney to assess).

**Recommendation (preliminary):** **Candidate for a provisional** *only if* combined with concrete technical steps: phantom-calibrated histograms per material, automated report-content gating, and the recommendation output. Otherwise **trade secret** for the per-material reference histograms and thresholds. **Do not publish the gating rules** before a decision (the oracle definition is already in the manuscript draft).

**Ownership questions:** none beyond §0.

**Disclosure risk:**
- Manuscript draft §Methods describes the oracle.
- The landing page advertises a "Separability check".

---

## INV-03: Material- and timepoint-aware measurement support (report what µCT can support; abstain otherwise)

**Description:**
- Each declared graft material × timepoint × voxel size is classified EASY / HARD / UNDERDETERMINED (`docs/science/SEPARABILITY_ANALYSIS.md` §1–§4).
- The report then:
  - always gives total mineralised volume in the defect;
  - gives class-specific volumes only with a separability label and an interval;
  - for UNDERDETERMINED cases (e.g. DBBM late, autograft, allograft), outputs "mineralised tissue volume" or a "model-based estimate" with an explicit prior, never "new bone volume".
- Current code implements only parts:
  - the `graft_brighter` material prior (`osteoquant/segment/classical.py`, `pipeline.py`);
  - voxel abstention and plausibility checks (`osteoquant/uncertainty/core.py`);
  - report exceptions (`osteoquant/report/defectfill.py`).
- The automated material lookup and report-gating are **Concept**.
- **Status: Concept + partial RTP-code.**

**Novelty hypothesis:** A rule- or benchmark-driven system that **changes the endpoint vocabulary** of a quantitative imaging report (measurement vs estimate vs refusal) based on material physics and timepoint, rather than only flagging uncertain voxels.

**Closest prior art found:**
- **US11972593B2** (GE; active): uncertainty above a threshold prompts user confirmation of a caliper measurement.
- **US20210350529A1** (EchoNous): gates predictions on ensemble uncertainty.
- **US12198337B2** (Siemens; active) and **WO2022108912A1** (Subtle Medical; ceased): OOD determination.
- **US11379991B2** (Sandia; active): relabels uncertain voxels.
- Selective classification (arXiv:1705.08500).
- Material-specific thresholding in **US11551420B2** (threshold by modality/bone type; seen in search summary, not fetched).
- No document found that gates *which endpoint names may be reported* by graft-material separability.

**Preliminary assessment:**
- Possibly the **most distinctive concept** in the register, but it is currently **not reduced to practice** in the product.
- It is close to "business rules on top of uncertainty", which carries §101 and obviousness risk.

**Recommendation (preliminary):**
- **Keep confidential.** Decide on a **provisional** after the physical-phantom data exist (they make the claims concrete and enabled), or earlier if the founder plans to publish Manuscript 1.
- Material thresholds and reference library: **trade secret**.

**Ownership questions:** Will the physical-phantom data be generated on university equipment? If so, ownership of the reference library may be affected (OTM A5–A8).

**Disclosure risk:**
- The separability doc and the grant drafts (`grants/SPECIFIC_AIMS_DRAFT.md`, `grants/NSF_PROJECT_PITCH_DRAFT.md`) describe "material-aware" segmentation at concept level.
- Grant submissions are confidential to agencies, but awarded abstracts are public (INF). **Review grant text before submission.**

---

## INV-04: Cortical-annulus segmental-gap ROI detection with metal suppression and explicit failure

**Description** (`osteoquant/roi/engine.py::detect_segmental_gap`):
- Find the cortical envelope from the max projection of dense bone along the long axis.
- Score each slice by dense-voxel occupancy **of the envelope's outer annulus only**, so dense graft inside the cavity does not masquerade as cortex.
- Suppress metal/hardware above a robust percentile.
- Pick the longest **interior** low-occupancy run bounded by bone on both sides.
- Build the cylinder from the cortical slices adjacent to it.
- Return a confidence and a `requires_review` flag. Raise an explicit error instead of returning a silent wrong ROI.
- Plate defects (`detect_plate_defect`) use a Kasa circle fit in a cortical band.
- Experiment F: plate Dice 0.971/0.976 with nominal diameter. Segmental: 50 % explicit failures when the gap is bridged (by design).
- **Status: RTP-code (synthetic + 2 real ovine scans).**

**Novelty hypothesis:** The annulus-only scoring, which is robust to dense intracavitary graft, combined with refusal semantics.

**Closest prior art found:**
- **US6021213A** (Eli Lilly; expired): the cortical region must surround the marrow.
- **US7593762B2** (Siemens; expired): cortical mask detection then dilation.
- Wehrle 2019: VOIs automatically created from the post-op scan.
- Hopkinson 2023 (doi:10.1002/jor.25507): automated CTAn callus segmentation subtracting cortex.
- Lagzouli 2025 (doi:10.1038/s41598-025-19698-w): DL VOI/landmark detection in the mouse tibia.

**Preliminary assessment:** Incremental image-processing heuristic. Patentability is **low**, and enforcement would be hard (detection is invisible in output).

**Recommendation (preliminary):** **Trade secret / unpublished know-how.** Inexpensive to keep. If a methods paper is wanted, publish it as defensive disclosure later.

**Disclosure risk:** Only in code (repository visibility).

---

## INV-05: Hash-chained audit trail with review binding to object hash

**Description:**
- `osteoquant/audit/log.py`:
  - append-only SQLite table;
  - each row hash = SHA-256(previous hash + canonical JSON of ts, user, org, action, object, details);
  - atomic append under `BEGIN IMMEDIATE`;
  - verification detects altered, inserted, removed or reordered rows;
  - exported **anchors** detect tail truncation or rewrite.
- `osteoquant/study/db.py::review`:
  - reviews require re-authentication;
  - each review is bound to the reviewed object's SHA-256;
  - self-approval is blocked and audited;
  - the latest decision governs (D-014).
- Reports embed model, ROI and labels hashes.
- **Status: RTP-code (tests in `tests/`).**

**Novelty hypothesis:** Weak. The combination is good engineering practice for 21 CFR Part 11-style controls.

**Closest prior art found:**
- **Schneier & Kelsey 1999**, "Secure audit logs to support computer forensics", ACM TISSEC (doi:10.1145/317087.317089).
- **US8230228B2** (IBM; expired).
- **US7000118B1** (Oracle; expired).
- **WO2020104935A1** (Capitec; ceased).
- **US7158692B2** (expired) and **US20050251011A1** (abandoned): Part 11 audit trails for quantitative medical imaging.
- Commercial: the ZEISS ZEN core GxP Toolkit advertises an audit trail and e-signatures; the HALO Link compliance add-on is described in `COMPETITOR_INTELLIGENCE.md`.

**Preliminary assessment:** Not patentable in any useful scope (INF).

**Recommendation (preliminary):**
- **Publish freely** (credibility with QA buyers).
- Protect the implementation by **copyright** only.
- The commercial moat is the validation package (IQ/OQ/PQ documentation), not the mechanism.

**Disclosure risk:** None material.

---

## INV-06: Physics-based phantom generator + known-truth per-material separability benchmark (material reference library)

**Description:**
- `osteoquant/phantom/` (materials from NIST XCOM, `ctsim.py`, structures, imaging artefacts) generates labelled defect phantoms for 15 materials with scanner "personalities".
- Experiments A–E and J quantify separability versus density, noise, voxel size and artefacts.
- Planned extension: physical phantoms of commercial grafts scanned to calibrate the library.
- **Status: RTP-sim.**

**Novelty hypothesis:**
- Simulation for training data is well known: **EP4645228A1** (Siemens/Duke, digital phantoms with ground-truth preservation); **US20190251397A1** (Nvidia); XCAT-style simulation (search results).
- The **calibrated per-material reference data** are the asset, not the generator concept.

**Preliminary assessment:** Data and parameters are best protected as **trade secret**. The generator code is protected by copyright.

**Recommendation (preliminary):**
- **Trade secret** for calibrated parameters, physical-phantom measurements and trained weights.
- **Publish** the benchmark *protocol and metrics* (credibility), as `IP_PROVENANCE.md` §4 already suggests.
- **Avoid** adding learned sim-to-real image translation without checking EP4645228A1.

**Ownership questions:** Physical-phantom scans on Beckman equipment, and storage on university servers (OTM A5–A8).

**Disclosure risk:**
- The `phantom_parameters.json` and the code are in the repository.

---

## INV-07: Thickness border-convention cross-walk to Scanco IPL (publish)

**Description:**
- The `edge` border convention for local thickness gives Tb.Th ICC 0.983 against Scanco IPL maps, against 0.61 for the `background` convention (Exp G; D-009).
- **Caveat:** the convention was chosen post hoc (review Q-10).
- **Status: RTP-code.**

**Prior art:**
- Hildebrand & Rüegsegger 1997 local thickness (cited in BoneJ docs).
- Mys et al. 2021 (doi:10.1016/j.bone.2020.115653): IPL vs CTAn differ.

**Recommendation (preliminary):** **Publish** (`publications/MANUSCRIPT_2_border_convention_technical_note.md`). It has low patent value and high credibility value.

---

## Summary table (all preliminary)

| ID | Short name | Status | Novelty (prelim.) | Closest art | Recommendation |
|---|---|---|---|---|---|
| INV-01 | Day-0 graft footprint propagation | RTP-sim | Weak–uncertain | US9036899B2; Schulte 2011; Wehrle 2019; Francis-Pester 2022 | Trade-secret protocol; FTO review; maybe publish later |
| INV-02 | Dice-optimal intensity oracle → feasibility advisor/abstention | Oracle RTP-sim; advisor Concept | Some (application) | US11748877B2; Valindria 2017; Geifman 2017 | Provisional candidate only with INV-03; else trade secret |
| INV-03 | Material/timepoint-aware endpoint gating | Concept + partial code | Most distinctive; §101 risk | US11972593B2; US20210350529A1; selective classification | Keep confidential; decide on provisional after phantom data or before Manuscript 1 |
| INV-04 | Cortical-annulus segmental ROI | RTP-code | Low | US6021213A; Hopkinson 2023; Wehrle 2019 | Trade secret / know-how |
| INV-05 | Hash-chained audit + hash-bound review | RTP-code | Very low | Schneier & Kelsey 1999; IBM/Oracle expired | Publish; copyright |
| INV-06 | Phantom generator + material reference library | RTP-sim | Concept low; data valuable | EP4645228A1; US20190251397A1 | Trade secret (data); publish protocol |
| INV-07 | Border-convention cross-walk | RTP-code | Low | Mys 2021 | Publish |
