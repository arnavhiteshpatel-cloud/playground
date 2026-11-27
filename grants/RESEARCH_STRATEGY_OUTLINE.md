# Research Strategy Outline (NIH R41/R43-style; reusable for the NSF Phase I Project Description)

**Prepared:** 2026-11-27. NIH Research Strategy for R41/R43 is limited to **6 pages** [V]. NSF Phase I project description limits are [UNR] (check NSF 26-510 §V when drafting).
**Rule:** no results are claimed. Every **[PENDING RESULT: …]** must be filled with real data or removed. Drafts must be rewritten by the team (NIH NOT-OD-25-132 [V]).

---

## 0. Executive summary (≈150 words, reusable across applications)

OsteoQuant is software for quantifying bone regeneration in preclinical micro-CT. It separates **new bone**, **residual graft** and **host bone**, computes standard morphometry, and produces audited, reproducible reports.

The unmet need is that many graft materials have X-ray attenuation overlapping bone. Today's threshold-and-contour workflows are therefore slow, operator-dependent and difficult to audit [INF; cite literature].

OsteoQuant's approach combines three elements:
1. A physical-phantom ground-truth benchmark that maps where graft and new bone are separable across materials and voxel sizes.
2. Material-aware segmentation that reports calibrated uncertainty.
3. Low-label adaptation to new materials and scanners.

The project is a pre-incorporation research prototype from a UIUC undergraduate founder. A synthetic-phantom benchmark is in progress [PENDING RESULT]. Physical phantom scans are planned on the Beckman Institute Zeiss Xradia 630 Versa. There are no customers or physical validation yet. Phase I will establish ground truth and an expert-comparison validation. Phase II will pursue multi-site validation and a production product for CROs and orthobiologic developers.

## 0b. Technical innovation (≈250 words)

1. **Separability as a measured quantity, not an assumption.** Existing workflows assume a threshold can separate graft from bone. We will instead *measure* separability: class-volume error as a function of material, voxel size, noise and beam-hardening, using phantoms with independently verified composition. This produces a reusable public benchmark [HYP: novelty to be confirmed by literature review].
2. **Material-conditioned 3-class segmentation.** The model is conditioned on graft material and acquisition parameters. It is trained substantially on physics-based simulation (forward model calibrated to phantom scans) and uses texture, granule morphology and defect-geometry priors as well as intensity.
3. **Calibrated uncertainty propagated to endpoints.** Voxel-wise predictive uncertainty is calibrated (temperature scaling, deep ensembles or MC-dropout, to be selected) and propagated to morphometric endpoints as confidence intervals. Ambiguous regions are flagged rather than silently assigned.
4. **Low-label adaptation.** A few annotated slices (k ≈ 1–20) adapt the model to a new material or scanner via semi-supervised or few-shot methods. This aligns with NIBIB's stated interest in "unsupervised and semi-supervised techniques" [CC].
5. **Audited reporting.** Every report embeds data hashes, parameters, model version and QC flags, giving GLP-style traceability for sponsor review [HYP: confirm requirements with CRO quality staff; OsteoQuant is not claimed to be GLP-compliant].

---

## 1. Significance (≈1 page)

- **Problem scale:** Orthobiologic and bone-graft substitute development relies on preclinical defect models (rodent calvarial and femoral defects, rabbit, sheep, etc.) with micro-CT as a primary endpoint [CC; **CITATIONS NEEDED**].
- **Technical gap:** attenuation overlap between graft and new mineralized tissue; the sensitivity of BV/TV to threshold choice; variable reporting despite micro-CT reporting guidelines [**CITE** Bouxsein et al., JBMR 2010 guidelines; threshold-sensitivity papers].
- **Consequences:** irreproducibility across labs, inflated or deflated efficacy, extra animals and studies, and difficulty for sponsors auditing CRO analyses [INF; support with citations and interview evidence].
- **Why now:** high-resolution lab micro-CT is accessible (the Beckman Versa 630 installation [V]); modern uncertainty-aware deep learning; growing emphasis on rigor and reproducibility (NIH rigor policies [CC]).
- **Alignment:**
  - NIBIB Image Processing: "Image segmentation … morphometry measurement", "Quantitative imaging and image-based biomarkers", "Early-stage validation of tools" [V].
  - NIAMS bone biology and imaging, and musculoskeletal regenerative medicine [CC].
- **Rigor of prior research:** Summarize the strengths and weaknesses of existing approaches. Describe the synthetic-phantom benchmark only as [PENDING RESULT].

## 2. Innovation (≈½ page)

Use §0b condensed into 3–5 bullets, each contrasted with the status quo.

## 3. Approach (≈4 pages)

### 3.0 Preliminary data
- [PENDING RESULT: synthetic-phantom benchmark: separability vs. contrast-to-noise, voxel size; baseline threshold method vs. prototype]
- [PENDING RESULT: prototype pipeline run-time and reproducibility on synthetic data]
- **If no results exist at submission:** NIH Phase I does not strictly require preliminary data [CC], but reviewers expect feasibility evidence. Present the software prototype as a feasibility demonstration (screenshots, a description of the audited report) and the phantom design.

### 3.1 Aim 1: Physical-phantom ground-truth benchmark
- **Design:**
  - **Tier A (synthetic-material phantoms):** graft materials ([PLACEHOLDER: e.g., HA granules, β-TCP, BCP, bioactive glass, a deproteinized bovine bone mineral; final list per collaborator input]) embedded in a matrix with bone-mimicking mineral surrogates at known densities.
  - **Tier B (ex vivo):** graft granules in ex vivo bone fragments or defect cores, with reference composition established by [PLACEHOLDER: gravimetry, high-resolution reference scan, or post-scan histology/SEM].
- **Ground truth:** designed geometry plus independent verification. Report the uncertainty of the ground truth itself.
- **Acquisition:** Zeiss Xradia 630 Versa at [PLACEHOLDER: 3 voxel sizes spanning typical rodent study settings], [PLACEHOLDER: kV, filter, exposure, number of projections]. Include repeat scans for test–retest.
- **Outputs:** class-volume error, Dice, boundary error and test–retest CV, mapped across material × voxel size × noise level.
- **Statistics:** mixed-effects model of error with material and voxel size as fixed effects and phantom as random effect. Pre-register the analysis plan (OSF) [HYP].
- **Pitfalls and alternatives:**
  - Surrogate realism: Tier B mitigates this.
  - Scanner time constraints: prioritize voxel sizes.
  - Facility access and rates: [UNR; confirm with the Beckman ITG Microscopy Suite].
- **Milestone M1:** benchmark v1 released (data and code) with a separability map.

### 3.2 Aim 2: Material-aware 3-class segmentation with uncertainty and low-label adaptation
- **Data:** simulated volumes from a forward model calibrated to Aim 1 scans (noise, blur/PSF, beam hardening, partial volume), plus phantom scans for validation.
- **Model:** 3D U-Net-family or transformer baseline (to be selected) with material and acquisition conditioning. Uncertainty via [ensembles / MC-dropout / evidential, to be compared]. Calibration via ECE and reliability diagrams.
- **Endpoint uncertainty:** propagate voxel probabilities to the distributions of BV/TV(new bone), residual-graft fraction and Tb.Th/Tb.Sp, reported as 95% intervals. Check coverage against phantom truth.
- **Low-label adaptation:** hold out one material. Adapt with k ∈ {1, 2, 5, 10, 20} annotated slices and plot an accuracy-vs-k curve.
- **Baselines:** global threshold (Otsu and fixed), threshold plus morphological cleanup, and an unconditioned network.
- **Success targets (pre-specified, not results):** [PLACEHOLDER: e.g., ≥X% reduction in class-volume error vs. best threshold baseline; 95% interval coverage within ±5 points of nominal].
- **Pitfalls:** sim-to-real gap (domain randomization, fine-tuning); truly inseparable regimes (report as a finding, since this is itself valuable to the field).
- **Milestone M2:** model v1 meets the targets on held-out phantoms.

### 3.3 Aim 3: Retrospective validation vs. expert manual analysis
- **Data:** [PLACEHOLDER: N] existing de-identified preclinical micro-CT scans from [PLACEHOLDER: partner labs or CRO]. A data-use agreement is required. **No new animals** are used in Phase I [INF]; confirm with NIH whether a Vertebrate Animals section is needed for existing data [UNR].
- **Readers:** [2–3] experienced analysts, blinded and working independently with their usual workflow. Time is logged per specimen.
- **Endpoints:** new-bone volume, residual-graft volume and BV/TV within a standardized defect ROI.
- **Statistics:**
  - Agreement: ICC(2,1), absolute agreement, with 95% CI. Analyze OsteoQuant vs. each expert and vs. the expert mean.
  - Bias: Bland–Altman bias and 95% limits of agreement (log-transform if heteroscedastic).
  - Time: paired comparison of time per specimen (Wilcoxon signed-rank).
  - Reference ceiling: inter-expert ICC.
- **Sample-size planning [INF, Walter–Eliasziw–Donner approximation, α=0.05 one-sided, power 0.80]:**
  - With 4 ratings per specimen (3 experts + OsteoQuant), ρ1 = 0.90 vs. ρ0 = 0.75 needs n ≈ 17; ρ1 = 0.85 vs. ρ0 = 0.70 needs n ≈ 26.
  - With 2 ratings, n ≈ 26–42.
  - **Plan for n ≈ 30–40 specimens** across ≥2 graft materials [PLACEHOLDER: confirm availability].
- **Success targets (pre-specified):** lower 95% CI of ICC ≥ [0.75]; time reduction ≥ [X]%; Bland–Altman limits within [±Y]% of the mean [PLACEHOLDER].
- **Pitfalls:**
  - Data-access delays: obtain LOIs from ≥2 labs.
  - Expert disagreement: report the inter-expert ceiling.
  - Heterogeneous scan settings: stratify and use the Aim 2 uncertainty.
- **Milestone M3:** validation report.

### 3.4 Rigor and reproducibility
- Pre-registered analysis plan; held-out test sets locked before model selection; blinded readers.
- Code and benchmark versioning; containerized pipeline; seeds fixed.
- Authentication of key resources: phantom materials (lot numbers, certificates), scanner calibration logs.
- SABV: not applicable to phantoms. For retrospective animal data, record and report sex where available [INF].

### 3.5 Timeline (Phase I; NIH normally 6 months [V]; NSF 6–18 months [V])

| Month | 1 | 2 | 3 | 4 | 5 | 6 | 7–12 (NSF option) |
|---|---|---|---|---|---|---|---|
| Aim 1 phantoms: fabricate / scan | ■ | ■ | ■ | | | | Tier B expansion |
| Aim 2 model + uncertainty | | ■ | ■ | ■ | ■ | | Low-label study |
| Aim 3 data agreements + reads | ■ | | | ■ | ■ | ■ | Expanded n |
| Reporting / audit module hardening | | | ■ | | ■ | ■ | |

### 3.6 Phase II preview
Multi-site, multi-scanner validation; expansion of the material library; production software with QMS-grade documentation; CRO pilot deployments; a pathway toward a qualified analysis method for sponsor studies [HYP].

---

## 4. Technical risk register

| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| Phantom surrogates don't mimic new bone | Med | High | Tier B ex vivo phantoms; report limits | Founder + Beckman staff |
| Some graft/bone pairs truly inseparable at practical voxel sizes | Med | Med | Report as a benchmark finding; uncertainty flags; recommend acquisition settings | Founder |
| Sim-to-real gap | Med | Med | Physics-calibrated simulation; fine-tuning; domain randomization | ML lead |
| No retrospective data access | Med | High | LOIs from ≥2 labs before submission; phantom-only fallback | Advisor |
| Scanner time / cost | Low–Med | Med | Prioritized scan matrix; OUR / Innovation Voucher co-funding | Founder |
| Expert reader availability | Med | Med | Paid readers, budgeted; staggered schedule | Founder |
| IP ownership dispute with the University | Med | High | OTM determination before incorporation; license if needed | Founder |
| PI eligibility not met at award | High (currently) | Fatal for SBIR | See NSF_vs_NIH_ELIGIBILITY.md §3 | Founder |
