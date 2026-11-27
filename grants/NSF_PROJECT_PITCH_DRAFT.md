# NSF SBIR/STTR Project Pitch: DRAFT (OsteoQuant)

**Prepared:** 2026-11-27 · **Status:** draft for founder rewrite; not submitted.

**Section requirements [V]** (https://seedfund.nsf.gov/apply/project-pitch-information/):
- Technology Innovation: up to 3,500 characters
- Technical Objectives and Challenges: up to 3,500 characters
- Market Opportunity: up to 1,750 characters
- Company and Team: up to 1,750 characters

**Process [V]:**
- Response "Typically … about 1-2 months".
- An invitation is valid for the next two deadlines.
- Limits are ≤2 pitches per company per 12 months and ≤3 for the same technology.
- No registrations or incorporation are needed to pitch.
- Next full-proposal deadlines: Mar 4, 2027; Jul 7, 2027; Nov 3, 2027 [V].

**Topic choice [INF]:** Primary is **Biomedical Technologies → Medical Imaging**; alternative is **Super Intelligence Applications** (NSF's current name for its applied-AI topic [V topic list]). Avoid framing OsteoQuant as a "medical device": the Biomedical topic excludes "the development pre-clinical or clinical-stage … medical devices" [V]. Frame it as quantitative-imaging research software.

**Rules applied:**
- No results are claimed.
- Bracketed items are placeholders the founder must fill or delete. NSF counts characters, so re-check counts after editing (the counts below include spaces).
- NSF encourages (does not require) disclosure of generative-AI use, and proposers are responsible for accuracy [CC, NSF notice Dec 2023]. Rewrite this text in the founder's own voice.

**Pending results this pitch deliberately does NOT claim:**
- [PENDING RESULT: synthetic-phantom separability benchmark]
- [PENDING RESULT: model vs. threshold baseline on synthetic data]
- [PENDING RESULT: physical phantom scans]
- [PENDING RESULT: expert comparison]

If any of these are available before submission, add one sentence each to Section 1 or 2, with the actual number and test conditions.

---

## 1. The Technology Innovation  (2,346 / 3,500 characters)

```text
Preclinical studies of bone-graft substitutes and orthobiologics depend on micro-CT to answer one question: how much new bone formed, and how much graft is left? Many graft materials (calcium phosphates, bioactive glasses, allograft/xenograft) attenuate X-rays like mineralized bone. Today, analysts separate them with global thresholds and hand-drawn contours. Results shift with operator, scanner, voxel size and material, take hours per specimen, and leave no audit trail. Investigators, CROs and sponsors cannot tell whether a reported "new bone" volume is real tissue or misclassified graft.

OsteoQuant is software that performs three-class segmentation (new bone / residual graft / host bone), computes standard morphometry, and issues audited reports in which every number is traceable to data, parameters and model version. The high-risk innovation is not the user interface. It is three linked technical ideas that have not been combined or validated:

1. Physical ground truth for separability. We will build phantoms with known amounts and layouts of graft materials and bone-mimicking mineral, scan them across voxel sizes on a Zeiss Xradia 630 Versa, and measure where graft and new bone become separable and where they do not. Prior work validates bone morphometry, but we are not aware of a public, physically grounded benchmark for graft vs. new-bone separability (to be confirmed by literature review).

2. Material-aware segmentation with calibrated uncertainty. A model conditioned on the graft material and acquisition physics, trained largely on simulated data from our forward model, that outputs voxel-wise uncertainty and propagates it to confidence intervals on morphometric endpoints. Users see when the answer is unreliable instead of receiving a single confident number.

3. Low-label adaptation. New materials and scanners appear constantly. We will test whether a handful of annotated slices can adapt the model without a full retraining study.

Compared with thresholding plus manual correction, the intended advantages are reproducibility across sites, explicit error bars, faster analysis, and an audit trail suitable for sponsor review. None of these advantages has yet been demonstrated. Proving them is the purpose of Phase I. A synthetic-phantom benchmark is in progress; physical validation has not started.
```

---

## 2. The Technical Objectives and Challenges  (2,447 / 3,500 characters)

```text
Objective 1: Physical-phantom benchmark. Challenge: no phantom reproduces living new bone. We will use mineral-density-matched surrogates and calibration inserts, design layouts with known class volumes, and verify fabricated geometry independently (gravimetry, high-resolution reference scans). Milestone: separability map (class volume error vs. material x voxel size x noise) for [N] materials at [3] voxel sizes. Risk: surrogate realism. Mitigation: include ex vivo bone fragments with graft granules as a second phantom tier; report surrogate limits explicitly.

Objective 2: Material-aware 3-class segmentation with uncertainty. Challenge: overlapping attenuation makes some voxels intrinsically ambiguous; a model must express that rather than guess. We will train on forward-model simulations calibrated to Objective 1 scans, use texture, morphology and spatial-context priors (e.g., granule shape, defect geometry), and calibrate uncertainty (expected calibration error; coverage of 95% intervals on volume fractions). Milestone: beats threshold-plus-cleanup on phantom truth by a pre-specified margin. Risk: simulation-to-real gap. Mitigation: domain randomization, physics-based noise/beam-hardening models, and fine-tuning on phantom scans.

Objective 3: Low-label adaptation. Challenge: each new material or scanner shifts the data distribution. We will test semi-supervised and few-shot adaptation with k annotated slices (k from 1 to 20) and measure the accuracy-vs-annotation curve. Milestone: identify the minimum k that reaches target accuracy for a held-out material.

Objective 4: Retrospective validation against experts. Challenge: access to de-identified preclinical scans and blinded expert analysts. We will compare OsteoQuant with 2-3 experts on [N] specimens: time per specimen, ICC with 95% CI, Bland-Altman bias and limits of agreement for new-bone and residual-graft volume; inter-expert variability is the reference ceiling. Milestone: pre-specified ICC and time-saving targets. Risk: data access delays. Mitigation: letters of intent from multiple labs before award; synthetic and phantom results stand alone if access slips.

Cross-cutting: audited reporting (parameter, data and model provenance in every report) and a locked analysis plan defined before validation data are unblinded. Success means Phase II can focus on multi-site validation and production software rather than on whether the core method works.
```

---

## 3. The Market Opportunity  (1,259 / 1,750 characters)

```text
Customers: R&D teams at orthobiologic and bone-graft companies, preclinical CROs that run bone-defect studies for them, and academic musculoskeletal labs and imaging cores. These teams typically scan many specimens per study and spend analyst hours on segmentation that is hard for sponsors and reviewers to audit (to be quantified in customer interviews). Value: faster turnaround, fewer re-analyses, defensible numbers with error bars, and consistency across studies and sites. Beneficiaries extend to patients, through better-characterized graft products, and to animal welfare, if tighter measurement error reduces group sizes.

Business model (hypothesis to test in customer discovery): per-study or annual software licenses for CROs and companies, plus validated analysis services early on. Market size is not yet sized from primary data; we will quantify it from interviews and public data on preclinical bone-graft studies.

Competition: general micro-CT software from scanner vendors and analysis packages, and open-source tools, all built around thresholding and manual ROI work; in-house scripts; manual analysis. Our intended differentiation is graft-vs-new-bone separation that is checked for identifiability before reporting (abstaining otherwise), with validation against physical ground truth as the proposed work, plus calibrated uncertainty and audit trails.
```

---

## 4. The Company and Team  (1,039 / 1,750 characters)

```text
OsteoQuant is a pre-incorporation project founded by a University of Illinois Urbana-Champaign undergraduate in [MAJOR], who designed and built the current prototype: the 3-class segmentation pipeline, morphometry, audited reporting and synthetic-phantom benchmark. [FOUNDER: add 1-2 concrete, verifiable accomplishments.] The company will be incorporated before any full proposal.

Gaps and plans: (1) Principal Investigator: NSF requires the PI to be more than 50% employed by the company at award. The founder will meet this by [graduation / reduced enrollment / leave - choose and confirm], or the company will recruit a qualified full-time PI. (2) Bone biology and preclinical study design: recruiting a faculty advisor in musculoskeletal research [NAME TBD]. (3) Micro-CT physics and phantom fabrication: collaboration with Beckman Institute imaging staff [TBD]. (4) Expert validation: 2-3 experienced micro-CT analysts at partner labs [TBD]. (5) Business: customer discovery via Illinois I-Corps and the Cozad New Venture Challenge.
```

---

## Annotations for the founder (not part of the pitch)

- **Section 1:** "we are not aware of a public, physically grounded benchmark" is an [INF] claim. Run and document a literature search (PubMed and Google Scholar: micro-CT, bone graft, phantom, segmentation, residual graft) before submitting.
- **Section 2:** Fill [N] materials and voxel sizes from the actual phantom plan. Confirm Beckman access and rates (rates [UNR]: itg-ms@beckman.illinois.edu, a public facility address).
- **Section 3:** NSF reviewers weigh customer evidence heavily [INF]. Add "We have interviewed N potential customers…" **only after** the interviews happen. Market numbers must be sourced.
- **Section 4:** Choose a PI-employment path from NSF_vs_NIH_ELIGIBILITY.md §3 and state it honestly. NSF counts outside employment above 19.6 h/week as a conflict, and the archived FAQ says university policy that prevents >50% employment disqualifies the PI [V/V-old].
- **Do not** describe the company as incorporated until it is.
