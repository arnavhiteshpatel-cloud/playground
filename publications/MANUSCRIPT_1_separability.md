# When can residual graft be distinguished from new bone in preclinical micro-CT? A known-truth simulation benchmark of intensity, context and longitudinal strategies

**Status: DRAFT (2026-11-27). Computational results complete; physical-phantom validation (Aim/Section 2.9) NOT yet performed.
All quantitative results below are from synthetic phantoms except Section 3.6 (public real trabecular data).
Citations marked [REF-CHECK] must be verified against the original before submission. Authorship, affiliations and
funding to be decided with collaborators and UIUC OTM.**

## Abstract
**Background.** Preclinical evaluation of bone-graft substitutes requires separating newly formed bone, residual graft
and host bone in micro-CT, yet laboratories rely on thresholds whose validity depends on graft–bone attenuation contrast.
**Methods.** We built a procedural phantom generator with exact voxel ground truth (three defect models; 15 materials
with attenuation from NIST elemental coefficients), and benchmarked (i) intensity-only thresholding (global, Otsu,
multi-Otsu, GMM, k-means), (ii) a multi-scale feature random forest (RF), (iii) a 3D U-Net, and (iv) registration of a
day-0 scan, under controlled graft–bone density overlap, noise, resolution and artefacts. A *Dice-optimal
intensity-only oracle* (best union of intensity bins given the true class-conditional histograms) upper-bounds what
any voxel-wise intensity rule can achieve.
**Results.** On 16 held-out phantoms (4 ceramic materials), the U-Net reached graft Dice 0.918 (95% CI 0.886–0.950)
and new-bone Dice 0.861 (0.837–0.884), versus 0.771/0.674 for a CTAn-style two-threshold workflow. When graft density
fell inside the new-bone range (800–1000 mgHA/cm³), the intensity-only oracle fell to graft Dice 0.52–0.77 (noise
dependent), whereas an RF with shape/texture features retained 0.85–0.92 — but only when granules were morphologically
compact; with strut-like granules the oracle was 0.36 and the RF 0.66–0.70. A registered day-0 graft footprint gave graft Dice 0.915 (compact) and 0.816 (strut-like) with sub-voxel
registration error. An explicit ROI-context channel did not improve the U-Net (0.919 vs 0.918).
**Conclusions.** In simulation, intensity is sufficient only when graft and new bone differ in density by more than the
noise; spatial context compensates only when graft morphology is distinctive; a day-0 baseline scan is the most robust
strategy. Physical phantoms of commercial materials are required to determine where real materials fall.

## 1. Introduction
* FDA special controls for resorbable calcium-salt bone void fillers (21 CFR 888.3045/888.3046) require animal data on
  resorption and replacement by new bone [V: eCFR 888.3046]. Micro-CT reporting follows Bouxsein et al. 2010
  (JBMR 25:1468) [R1].
* Graft materials span HA (≈2.8× bone attenuation), microporous β-TCP and BCP (bone-like after resorption), bioactive
  glass and calcium sulfate (energy-dependent bone equivalence), and allograft/xenograft (bone-like by composition)
  [docs/science/SEPARABILITY_ANALYSIS.md; REF-CHECK].
* Prior work: automated callus segmentation (PMC10947128), synchrotron callus tissue classification with 0.69–0.81
  per-class accuracy (Bone Reports 2024), CNN segmentation of bioactive-glass scaffold/bone/pores (Dice 90.1), nnU-Net on
  Mg implants (mIoU 91–94%), and the BONe deep-learning bone tools that "often fail to generalize" [REF-CHECK all;
  docs/research/COMPETITOR_INTELLIGENCE.md].
* Gap: no study separates *what information* (intensity, morphology, spatial context, time) makes graft and new bone
  separable, using ground truth that is exact rather than annotator opinion.

## 2. Methods
2.1 **Phantom generator** (osteoquant/phantom, v1.0.0). Condyle (cancellous block, cortical surface, drilled
cylinder), calvarial (plate with diploe; dural osteogenesis) and segmental (tube with gap) models; 2× supersampled
tissue map integrated to the output grid (exact partial-volume class fractions). Host trabeculae from the zero level-set
of a band-limited Gaussian random field; graft granules by continuous-space random sequential addition with angular
roughness; healing stage s∈[0,1] controls resorption (per-granule, faster near host bone), osteoconductive coating,
creeping substitution and a noisy ingrowth front. Material attenuation by the mixture rule from NIST XCOM elemental
coefficients; bone tissue as HA in a soft-tissue matrix. **All biological rates are assumptions** (SCIENTIFIC_EVIDENCE §5).
2.2 **Imaging.** Mode A: grey = µ(40 keV)·gain + offset, Gaussian PSF, block-mean resolution loss, rings, cupping,
Gaussian/Poisson noise, scanner gain/offset shift. Mode B (implemented, not used for the results here): polychromatic
parallel-beam projection with Poisson counting and FBP.
2.3 **Datasets.** 48 training, 8 validation, 16 test specimens (β-TCP, BCP, HA, CaSO4; three defect models; stage
0.15–0.9; randomised blur 15–35 µm, noise σ 30–110, gain 0.85–1.15, offset ±80); 40 held-out-material specimens
(45S5 glass, deproteinised bovine bone mineral). Splits by specimen; distinct seed ranges per split.
2.4 **Methods compared.** Global SOP threshold (fixed from training data), Otsu + within-ROI Otsu ("CTAn-style"),
adaptive, multi-Otsu, GMM-3, k-means-3, intensity+morphology (solidity filter), RF (60 trees; Gaussian, gradient, LoG,
local SD at 0–160 µm, Hessian eigenvalues, distance to ROI boundary; 15k voxels/class from 6 specimens), 3D U-Net
(0.79 M parameters, 4 levels, instance norm, Dice + boundary-weighted CE, 1,500 iterations of 48³ patches, CPU),
day-0 propagation (Section 2.6). All single-timepoint methods received the true ROI so ROI error does not confound.
2.5 **Separability benchmark.** Graft modelled as mineral of HA-equivalent density X ∈ {2200…650} mgHA/cm³ (new
bone 650–1000 by maturity; host 1000–1150) × noise σ ∈ {30, 80, 150, 250}; 4 specimens (RF trained on 1, tested on 3).
Intensity-only oracle: with the test volumes' true class-conditional histograms (256 bins), the Dice-maximising union
of bins (a superlevel set of the graft likelihood ratio) — an upper bound for any voxel-wise intensity method at this
binning. (An earlier draft reported the accuracy-optimal rule's Dice, which is not a Dice bound; corrected after
independent review.) Ablation (C2): RF feature sets and granule
morphology (compact 300–600 µm, roughness 0.15 vs strut-like 120–250 µm, roughness 0.6).
2.6 **Longitudinal.** For each specimen, day-0 (s=0) and later (s=0.6) phantoms share host anatomy and initial packing;
the later scan undergoes random rigid motion (≤5°, ≤200 µm) and is registered (rigid, normalised correlation, metric
mask = host anatomy outside the dilated defect, 2-level pyramid with voxel-unit smoothing). Residual graft := later
mineral ∩ day-0 graft footprint. Target registration error (TRE) at ROI points from the known motion.
2.7 **Metrics.** Dice, HD95 (µm), ECE (15 bins); specimen-level means with t-based 95% CI (voxels are not replicates).
2.8 **Morphometry verification.** Analytic objects and 8 public trabecular cubes with Scanco IPL thickness maps
(Zenodo 10.5281/zenodo.11061947, CC-BY-4.0); ICC(2,1) and Bland–Altman.
2.9 **Physical validation — PENDING.** Protocol in validation/PHANTOM_EXPERIMENT_PROTOCOL.md (3–5 commercial grafts in
ex vivo bone defects, Zeiss Xradia 630 Versa, 10/20/40 µm, HA calibration, repeat scans). [PENDING RESULT]

## 3. Results
3.1 **Classical baselines (Table 1; Experiment A).** Mineral Dice 0.91–0.93 for Otsu-type methods; within the ROI,
graft Dice 0.72–0.77 and new-bone Dice 0.57–0.72 for intensity methods; RF 0.882 (0.842–0.922) / 0.744 (0.688–0.799).
3.2 **3D U-Net (Experiment B).** Graft 0.918 (0.886–0.950), new bone 0.861 (0.837–0.884), host 0.960; HD95 graft
47 µm; ECE 0.008; inference 0.7 s per ~0.4 Mvoxel volume on 4 CPU cores. By material: HA 0.968, BCP 0.950, CaSO4
0.889, β-TCP 0.886. Context ablation: without ROI channel 0.919 / 0.866 / 0.966 — no benefit from explicit context.
3.3 **Separability (Figure 1; Experiment C).** At noise σ=80: graft density 1600 → intensity oracle 0.955, multi-Otsu
0.951, RF 0.962; 1000 → 0.771 / 0.749 / 0.917; 900 → 0.686 / 0.683 / 0.899. At σ=250 and 900 mgHA/cm³: oracle 0.551,
multi-Otsu 0.508, RF 0.877. Resolution (D): RF graft Dice 0.947→0.880 from 40→120 µm voxels at 1300 mgHA/cm³.
Artefacts (E): rings and 20% cupping cost ≤0.01 Dice; a 60 µm PSF cut multi-Otsu to 0.846 (RF 0.925); an unnormalised
gain/offset shift cut RF to 0.810, restored to 0.962 by percentile normalisation.
3.4 **What carries the information (C2).** Overlap regime (900 mgHA/cm³, σ=150), compact granules: intensity oracle
0.610, RF raw intensity 0.486, multi-scale intensity 0.720, + shape/texture 0.857, + spatial prior (true-ROI distance)
0.881. Strut-like granules: oracle 0.357; 0.246 / 0.534 / 0.646 / 0.704. Multi-scale smoothing alone exceeds the
voxel-wise oracle because it pools neighbouring voxels (denoising), which a voxel-wise rule cannot.
3.5 **Day-0 propagation (L, L2).** Rigid TRE 0.3–4 µm (sub-voxel). Compact granules, 900 mgHA/cm³: day-0 0.915 vs RF
0.887, multi-Otsu 0.558, bound 0.394. Strut-like: day-0 **0.816** vs RF 0.663, multi-Otsu 0.318, intensity oracle 0.323. At 1600 mgHA/cm³
(easy regime) day-0 (0.893) is slightly *worse* than single-timepoint RF (0.955) because new bone formed inside the
original footprint is counted as graft (creeping substitution).
3.6 **Morphometry vs Scanco IPL (real data).** Tb.Th ICC(2,1) 0.983, mean difference −2.4%; Tb.Sp ICC 0.948, −4.1%;
with a background-border convention the agreement fell to ICC 0.61/0.55 (−18%/−34%). Analytic plates: exact for even
voxel thicknesses (+1 voxel for odd); digitised rods ≈1 voxel thin.
3.7 **Low-label adaptation and uncertainty** — see Manuscript 3 (Experiments J, K).

## 4. Discussion
* Intensity separability is governed by (graft − new-bone density)/noise; with typical desktop noise, ceramics whose
  effective density approaches the new-bone range lose intensity separability before they become physically similar.
* Context-based methods succeed in simulation partly because the simulator encodes distinct morphologies; this is the
  key uncertainty for real materials and the reason a physical phantom programme is necessary.
* A day-0 scan converts an underdetermined classification into a registration problem; it requires in vivo imaging at
  implantation, which terminal ex vivo study designs often lack — a study-design recommendation for sponsors.
* Explicit ROI context added nothing for the U-Net — the network learns spatial priors from the image.
* Border conventions alone change thickness by ~18% against a reference implementation; methods sections should state them.

## 5. Limitations
**Independent-review caveats (2026-11-27):** (i) RF "spatial" features and the U-Net context channel use the *true*
ROI, whose geometry partly determines labels in the generator — the no-context U-Net and no-spatial RF are the fair
comparisons; (ii) the day-0 experiment is best-case: graft only shrinks in place between timepoints (no migration,
fragmentation or swelling); (iii) the thickness edge convention was chosen after seeing the IPL comparison set;
(iv) RF baselines in an earlier run were trained on fewer materials than the U-Net (rerun with balanced training).
Synthetic morphology and biology are simplified assumptions; single generator family for training and test (optimistic);
attenuation model ignores carbonate substitution and real granule microstructure; Mode A imaging is not projection
physics; rigid registration only (no biological deformation); n of specimens per condition is small (3–16); one
external morphometry dataset (n=8); no physical scans yet.

## 6. Data and code availability
Code: private repository (OTM review pending). Synthetic data regenerable from seeds. Public datasets cited by DOI.

## Tables/figures available
Fig 1 `experiments/results/figures/exp_C_separability.png`; Fig 2 phantom overview `phantom_models_overview.png`;
Fig 3 `exp_G_morphometry.png`; tables from `experiments/results/*.json`.

## Target venues [UNR — verify scope/deadlines]
Journal of Orthopaedic Research; Bone; JBMR Plus; Tissue Engineering Part C: Methods; Scientific Reports;
conferences ORS Annual Meeting, TERMIS-AM, SPIE Medical Imaging.
