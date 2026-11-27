# Scientific methods: an analyst's explainer

> **Status.** Research product: not validated on real graft materials; not a medical device; no GLP/Part 11
> compliance claimed. Every result below is labelled **[SYNTHETIC]** (computational phantoms with exact ground
> truth), **[REAL]** (public datasets) or **[ASSUMPTION]**. Synthetic results show mechanism, not product accuracy.

This page explains what OsteoQuant computes and why, at the level an imaging analyst or study director needs to
interpret a report. Authoritative definitions live in `docs/science/`:
[ENDPOINT_DEFINITIONS](../science/ENDPOINT_DEFINITIONS.md), [MEASUREMENT_SUPPORT](../science/MEASUREMENT_SUPPORT.md),
[PREREGISTRATION](../science/PREREGISTRATION.md), [HISTOLOGY_SCOPE](../science/HISTOLOGY_SCOPE.md). Every number
quoted here comes from a result file in `experiments/results/`; the index is
[EXPERIMENT_REGISTRY.md](../../EXPERIMENT_REGISTRY.md).

Contents: [1 Pipeline](#1-pipeline) · [2 Endpoints](#2-endpoints) · [3 Measurement support](#3-measurement-support-advisor-121) ·
[4 Uncertainty](#4-uncertainty) · [5 Longitudinal day-0 method](#5-longitudinal-day-0-method-and-its-limits) ·
[6 Morphometry conventions](#6-morphometry-conventions) · [7 Statistics](#7-statistics) · [8 Histology](#8-histology) ·
[9 Reproducibility](#9-reproducibility) · [10 Summary of limits](#10-summary-of-limits)

---

## 1. Pipeline

One analysis is a pure function of (volume, configuration). The configuration snapshot, its hash and the hashes of
inputs, labels and models are stored with the result so that each number can be traced and reproduced.

```
QC -> defect ROI -> segmentation -> uncertainty -> plausibility checks -> morphometry -> measurement support -> reported metrics
```

| Stage | What happens | Notes |
|---|---|---|
| **QC** | Deterministic checks (spacing, isotropy, missing slices, ingest errors, non-finite or saturated voxels, metadata completeness) and heuristic checks (bone/soft-tissue CNR, ring and cupping indices, slice-to-slice jumps, truncated anatomy, long-axis alignment) | Heuristic thresholds are developer choices, not standards. Verdict: suitable / review / unsuitable |
| **ROI** | Automatic cylindrical defect detection for plate-like defects (condyle, calvarial), helped by the nominal diameter; a segmental-gap detector; or a manual cylinder | [SYNTHETIC] Plate defects: ROI Dice 0.971/0.976 with the nominal diameter, 0.881/0.904 fully automatic. The segmental detector raises an explicit exception rather than guess when healing bridges the gap. [REAL] Ovine day-18 scan: regenerate found with confidence 0.56 and flagged for review; day-161 scan returned as an exception |
| **Segmentation** | Labels inside the ROI: 1 new bone, 2 residual graft, 3 host bone, 0 non-mineral, 255 uncertain | Methods: `multiotsu` (default in the desktop), `ctan_style` (two fixed thresholds), `advisor_threshold` (the threshold implied by the advisor), random forest, locked U-Net (PyTorch or ONNX Runtime). Out-of-field padding and metal are excluded before thresholds are computed ([REAL] without this, new-bone fraction read 1.00 on an ovine scan; with it 0.21) |
| **Uncertainty** | For probabilistic methods: test-time augmentation, predictive entropy and voxel abstention at max-softmax τ = 0.6 | Classical methods produce no probabilities and therefore no *uncertain* voxels |
| **Plausibility** | Sanity checks on the label map; failures flag every endpoint | |
| **Morphometry** | Endpoints of §2 | |
| **Measurement support** | The advisor (§3) assigns each endpoint a status; unsupported endpoints are replaced by "not measured" in the *reported* metrics | Raw values are kept in the audit record only |

The `no_graft` setting (empty-defect controls, distraction osteogenesis) relabels all mineral in the ROI as new bone.

---

## 2. Endpoints

Full definitions: [ENDPOINT_DEFINITIONS.md](../science/ENDPOINT_DEFINITIONS.md). The points analysts most often ask
about:

* **Volumes are voxel counts × voxel volume** inside the ROI, in mm³. There is no sub-voxel partial-volume
  correction.
* **Total mineral volume** (new bone + residual graft) is the robust primary endpoint: it does not require graft and
  new bone to be told apart.
* **Two denominators.** `new_bone_fraction` = V(NB)/TV treats uncertain voxels as not new bone (conservative);
  `new_bone_fraction_of_certain` = V(NB)/TV<sub>certain</sub> removes the material-dependent abstention bias. Reports
  give both. The same applies to residual graft.
* **Graft resorption** = 1 − V(RG, t)/V(RG, day 0) needs a registered day-0 scan that passes registration QC.
* **Bridging**: the fraction of ROI cross-sections, along the defect axis, that contain a connected mineral path from
  host to host. All-mineral bridging is always reported; new-bone bridging only if new bone is supported.
* **Radial ingrowth**: new-bone fraction in concentric shells from the ROI boundary; shell width max(200 µm,
  4 voxels).
* **Density** (TMD, mgHA/cm³) only when an HA-phantom calibration is recorded. Otherwise grey values are reported and
  labelled uncalibrated.

**Accuracy thresholds, one meaning each.** ±10% volume ratio and Dice ≥0.85: the advisor's *a-priori*
identifiability requirement (not a measured error). >20% graft-volume error or graft Dice <0.8: a *failed
measurement* in simulation experiments. |bias| ≤5% and 95% LoA within ±15%: what *supported* must achieve against
physical truth in validation stage B.

---

## 3. Measurement-support advisor (1.2.1)

Implementation: `osteoquant/advisor/separability.py` (`ADVISOR_VERSION = "1.2.1"`) and `integration.py`. Every
assessment records the advisor version. Policy: [MEASUREMENT_SUPPORT.md](../science/MEASUREMENT_SUPPORT.md).

### 3.1 The question

A segmentation method always outputs a residual-graft volume. For many materials that number is not identifiable:
graft and new bone share the same attenuation range (§3.5). The advisor decides **before reporting** whether each
endpoint can be measured, by which mechanism, and under which conditions.

### 3.2 Inputs

| Input | Default source | Preferred source |
|---|---|---|
| Graft material | Your selection in the analysis dialog | — |
| Graft intensity distribution | Material profile from the knowledge base (NIST attenuation physics × assumed porosity) | Measured: a day-0 scan or a scan of the material alone, same scanner and protocol |
| New-bone intensity | Assumed maturity range 0.60–1.00 of host bone (0.60–0.93 for early healing) | Measured from empty-defect controls at the same timepoint |
| Noise | Median absolute deviation of soft tissue outside the defect (conservative: includes tissue texture) | — |
| Grey-scale anchor | Soft-tissue and host-bone levels outside the defect | HA calibration phantom |
| Day-0 information | Registration result, QC, granule tracking | — |

**Relative mineral units.** Grey values are converted to r = (x − soft)/(host − soft), so soft tissue ≈ 0 and mature
host bone ≈ 1 without HA calibration. Noise is expressed the same way (`noise_rel`).

### 3.3 How a decision is computed

1. **Class models.** The graft is modelled as a normal distribution from its profile (or as measured samples), new bone
   as a uniform maturity range. Both get the scan's noise and partial-volume mixing: a share of voxels, derived from
   granule size and voxel size, is mixed towards neighbouring phases (soft tissue, the other class, host bone).
2. **Oracle.** For two histograms, every voxel-wise intensity rule is a union of bins; the Dice-maximising union is the
   *intensity-only oracle*, an upper bound for any threshold workflow. If the oracle fails, every threshold fails.
3. **The rule actually applied.** Because real methods use a single threshold, the decision uses the best
   *single-threshold* rule (the oracle is reported as the upper bound). Among near-optimal thresholds, the one with the
   smallest volume error is chosen.
4. **Robustness to graft share.** Volume error grows as residual graft becomes scarce, so the rule must pass at the
   graft share estimated from the scan **and** at half of it.
5. **Mineral rule (from 1.2.0).** New bone versus soft tissue is checked with partial-volume halos of dense phases. If
   that boundary is not reliable, mineral and new-bone endpoints are withdrawn too.

### 3.4 Decision rules

| # | Rule | Outcome |
|---|---|---|
| 1 | Noise ≥0.35 of the bone–soft-tissue contrast, or the mineral rule fails | Mineral endpoints (total mineral volume, mineralised fraction) and new-bone endpoints **not supported** |
| 2 | Radiolucent graft (mean <0.15 of host: collagen sponge, PLGA, PCL) | Graft endpoints **not supported** (invisible); new-bone endpoints **supported with conditions** ("graft has no mineral phase") |
| 2a | DBM (radiolucent but bone-derived), from 1.2.1 | Graft **and** new-bone endpoints **not supported**: mineralised DBM particles are indistinguishable from new bone |
| 3 | Intensity mechanism: single-threshold graft Dice ≥0.85 **and** graft-volume ratio within ±10%, at the estimated graft share and at half of it | Graft and new-bone endpoints **supported** |
| 3a | Graft share below 5% of mineral | Graft-volume endpoints **not supported** ("trace residual graft") |
| 4 | Bone-derived graft (autograft, allograft, DBBM xenograft) | Never supported by intensity, even with measured samples |
| 5 | Intensity fails, but a registered day-0 scan passes registration QC, with granule motion ≤200 µm (or tracked) and ≤20% untracked graft volume; all four day-0 fields computed by the software | **Supported with conditions**. For resorbable materials the conditions state that bone formed inside the original footprint is counted as graft |
| 6 | Texture/morphology model | Only with material-specific validation evidence in the model card (none exists) |
| 7 | Material not in the knowledge base, or measured reference samples with <500 voxels | **Not supported** until characterised |
| 7a | Metals (magnesium, titanium) | Never supported (streak and beam-hardening artefacts are not modelled) |
| 8 | Density endpoints | Only with HA calibration |
| — | New-bone thickness endpoints | Need structures ≥3 voxels (about 150 µm woven trabeculae) and supported new bone |

Each endpoint's result carries a status, the mechanism (intensity, day-0 registration, radiolucent graft, no-graft
design, calibration) and a reason. Conditions are listed with *supported with conditions*.

**Additional flags in the desktop.** Independently of the material, the desktop marks every endpoint *flagged* when
uncertain voxels exceed 10% of the ROI and *not supported* above 25%; flags Tb.Th below 2.5 voxels as
partial-volume dominated; and flags results whose QC verdict is unsuitable, whose plausibility checks failed or whose
automatic ROI requires review.

### 3.5 What the advisor does **not** do

* It does not check the segmentation method you used. The decision says whether the endpoint is identifiable from
  intensities; a poor method can still mis-measure a supported endpoint ([SYNTHETIC] S1: multi-Otsu errors on
  supported HA specimens). The `advisor_threshold` method applies the advisor's own threshold; the desktop default is
  multi-Otsu.
* It does not validate its own material profiles. Porosities and granule sizes are assumptions; the advisor and the
  phantom simulator share the same attenuation model, so their agreement in simulation is partly self-consistent.
* Its thresholds (0.85, ±10%, 0.35, 200 µm, 20%) are policy choices, frozen for the first real-data evaluation.

### 3.6 Evidence for the advisor

All [SYNTHETIC]. Failure is defined as graft-volume error >20%.

| Experiment | Advisor version | Result |
|---|---|---|
| S1, density × noise sweep (96 conditions, multi-Otsu) | 1.1.0 | 54 of 54 failures refused; 12 conditions supported, none failed (Clopper–Pearson upper 95% bound on P(fail \| supported) 0.26) |
| S1, 56 dataset specimens (4 trained + 2 held-out materials) | 1.1.0 | All failures refused (32/32 multi-Otsu, 6/6 synthetic U-Net), but only 3 of 56 specimens supported; 47 accurate U-Net measurements were refused, because the advisor reasons only from intensity |
| S1b, advisor's own threshold | 1.1.0 | Sweep: 52 of 52 failures refused; median graft-volume error of supported conditions 2.4%. On supported dataset specimens new-bone volume was over-estimated (median error 60%), the finding that led to the 1.2.0 mineral rule |
| S1c, measured new-bone reference from a different simulated control animal | 1.1.0 | 24 of 96 conditions supported, 18 of them failed (P(fail \| supported) 0.75); 77% of failures refused. A control-animal reference made the advisor over-confident |
| L3, day-0 rule (see §5) | 1.2.0 | Naive footprint: 29 of 29 failures refused. Tracked footprint: supported with conditions in 29 of 30 runs, all 29 failed |

S1–S1c predate advisor 1.2.0 and 1.2.1 and have not been re-run with the current version. Results produced before
1.1.0 are kept only as exploratory (pre-registration deviation log). Result files: `exp_S1_advisor.json`,
`exp_S1b_advisor_threshold.json`, `exp_S1c_control_reference.json`, `exp_L3_displacement.json`.

**Why separability fails** [SYNTHETIC, Experiments C and C2]: when graft density lies in the new-bone range
(800–1000 mgHA/cm³), the intensity-only oracle reaches graft Dice 0.52–0.77 depending on noise. A random forest with
shape and spatial features reaches 0.85–0.92 only when granules are compact; with strut-like (bone-like) granules the
oracle drops to 0.36 and the random forest to 0.65–0.70.

---

## 4. Uncertainty

* **Voxel abstention.** With probabilistic models, voxels whose maximum class probability is below τ = 0.6 are
  labelled *uncertain* (255) and excluded from class volumes; `*_of_certain` endpoints use the certain volume as
  denominator.
* **Evidence** [SYNTHETIC, Experiment K]: deferring the 10% least-confident voxels raised retained accuracy from
  0.940 to 0.973. A scan-level failure flag (graft Dice <0.8) had sensitivity 4/4 and specificity 0.75.
  Out-of-distribution detection is weak: ID-vs-OOD AUROC 0.66. Temperature scaling did not improve calibration.
* **Not yet available.** Deep ensembles, failure-detection AUROC on the current models and conformal volume intervals
  (Experiment U1) have not completed. Reports therefore carry no interval around volumes; the design intent is to
  abstain rather than claim coverage under distribution shift.
* **Domain shift** [REAL, Experiments H/I]: a U-Net trained only on synthetic phantoms reached Dice 0.379 zero-shot on
  real dog-forelimb scans (bone vs background); one labelled real scan lifted it to 0.787 (10-scan real model: 0.826).
  Do not use synthetic-only models on real scans.

---

## 5. Longitudinal day-0 method and its limits

**Idea.** If a scan is taken on the day of implantation, the graft footprint is known before any new bone forms.
Later scans are registered to day 0; mineral inside the propagated footprint is labelled residual graft, mineral
outside it new bone. This turns an unidentifiable intensity problem into change detection, and is most promising for
slowly resorbing, bone-like materials (DBBM, HA).

**Implementation** (`osteoquant/longitudinal/`, library only; there is **no desktop workflow yet**):

1. **Registration.** Rigid (also affine/B-spline available) with SimpleITK, masked to exclude the defect so that
   healing does not drive the alignment.
2. **Registration QC.** Block-wise residual displacement measured by masked normalised cross-correlation in a shell
   around the defect; pass if ≤2 voxels. This replaced a host-mineral Dice criterion that rejected 56% of harmless
   misalignments (Experiment L4). [SYNTHETIC] L4: all 6 harmful misalignments flagged; 85% of harmless ones passed.
3. **Footprint.** Mineral inside the ROI on day 0.
4. **Granule tracking** (optional). Per-granule search for displacement; reports the share of graft volume that could
   not be tracked and the 90th-percentile shift.
5. **Advisor rule 5** (§3.4) decides whether graft endpoints are *supported with conditions*.

**Best-case evidence** [SYNTHETIC, Experiments L and L2]: when the simulated graft only shrinks in place, the day-0
footprint gives graft Dice 0.915 in the overlap regime, and 0.816 with strut-like granules where a single-scan random
forest gives 0.663 and the intensity oracle 0.323.

**Limits shown by Experiment L3** [SYNTHETIC, generator v2, 3 seeds per cell, advisor 1.2.0]:

| Granule displacement | Naive footprint graft Dice (no fragmentation) | Tracked footprint |
|---|---|---|
| 0 µm | 0.80 | 0.41 |
| 50 µm | 0.535 | 0.35 |
| 100 µm | 0.35 | 0.34 |
| 200 µm | 0.24 | 0.32 |
| 400 µm | 0.17 | 0.30 |

* Graft Dice of the naive footprint falls from **0.80 to 0.535 with only 50 µm of granule motion**, well inside the
  advisor's 200 µm tolerance. With 30% fragmentation it is lower still (0.61 at 0 µm, 0.41 at 50 µm).
* Granule tracking, as implemented, does not recover accuracy, and reported median shifts of about 500 µm even when
  the granules had not moved.
* The advisor refused all failing naive-footprint measurements, but **supported the tracked footprint in 29 of 30
  runs, all of which failed**. The day-0 decision rule is therefore not validated, even in simulation.
* Deliberately skipped registrations were always flagged by registration QC.
* **Creeping substitution.** Bone formed inside the original footprint of a resorbing graft (β-TCP, calcium sulfate,
  bioactive glass) is counted as graft, so residual graft is over-estimated and new bone under-estimated. The
  generator models resorption as shrinkage and translation, not replacement, so simulation cannot reveal this bias.
* **Study design.** The method needs an in vivo post-operative scan with the same protocol, which not every study
  has.

Use the day-0 result, if at all, as a research read-out with the conditions printed beside it.

---

## 6. Morphometry conventions

Frozen in [PREREGISTRATION.md](../science/PREREGISTRATION.md) §1 before Generation-2 held-out data were analysed.

| Item | Convention |
|---|---|
| Local thickness (Tb.Th) | Hildebrand–Rüegsegger sphere fitting on the Euclidean distance-transform ridge; thickness = 2 × radius; border convention `edge` (primary), `background` also reported |
| Separation (Tb.Sp) | Same algorithm on the complement within the analysis region |
| Trabecular number | Tb.N = 1 / (Tb.Th + Tb.Sp), a model-independent plate approximation |
| Connectivity | 26-connectivity for foreground, 6 for background; Conn.D = (1 − χ)/TV |
| Surface | Marching cubes at 0.5 on the binary mask, voxel spacing applied |
| Reference segmentations | Used as provided (no re-thresholding) |
| Architecture endpoints | Computed on new bone inside the ROI; reported only when structures span ≥3 voxels |

**Accuracy.** [Analytic] Plates are exact for even voxel counts and +1 voxel for odd counts; digitised rods read about
one voxel thin; BV/TV is exact. [REAL] Against Scanco IPL on 8 public trabecular cubes: Tb.Th ICC(2,1) 0.983
(95% CI 0.912–0.997, mean −2.4%) and Tb.Sp ICC(2,1) 0.948 (mean −4.1%) with the `edge` convention; the `background`
convention under-reads (ICC 0.61/0.55). The `edge` convention was chosen after seeing these cubes, so this agreement is
not independent; held-out confirmation is pending (acceptance: point ICC ≥0.95 and lower bound ≥0.80 when n <20).

Nomenclature follows Bouxsein et al. 2010 (J Bone Miner Res 25:1468) where an equivalent exists. Graft endpoints have
no standard definition; OsteoQuant's definitions are in ENDPOINT_DEFINITIONS.

---

## 7. Statistics

* The **specimen (animal)** is the experimental unit. Repeated scans of one animal at one timepoint are averaged
  before group statistics. Voxels are never treated as replicates.
* Group comparisons use specimen-level values; longitudinal comparisons use mixed models with animal as a random
  effect.
* Agreement: ICC forms per Koo & Li (the implementation reproduces Shrout & Fleiss reference values), Bland–Altman bias
  and 95% limits of agreement, specimen-level bootstrap confidence intervals.

---

## 8. Histology

Histology is a complementary module and is not part of the desktop application. Kept: 2-D section to micro-CT slice
registration as an overlay ([SYNTHETIC] Dice 0.31–0.40 → 0.85–0.87) and graft-void area as an exploratory measure
(ICC 0.84, synthetic). Removed from reports: H&E bone-area fraction (ICC 0.35). Not offered: classical nuclei
detection ([REAL] NuInsSeg object F1 0.34). Histology remains the reference method for the cases the advisor refuses.
See [HISTOLOGY_SCOPE.md](../science/HISTOLOGY_SCOPE.md).

---

## 9. Reproducibility

[SYNTHETIC, Experiment P] Pipeline labels and metrics, network probabilities, fixed-seed training weights, random
forests and NIfTI/NRRD/Zarr/TIFF/DICOM round-trips were bit-identical across runs.

---

## 10. Summary of limits

* No real three-class (new bone / residual graft / host bone) ground truth exists yet; separation on real graft
  material is unknown.
* Material profiles are physics plus assumed porosity and granule size.
* Advisor evidence (S1–S1c) was produced with version 1.1.0; L3 with 1.2.0; the current version is 1.2.1.
* The day-0 method degrades with tens of micrometres of granule motion and counts creeping substitution as graft.
* Out-of-distribution detection is weak; no volume intervals yet.
* Real-data n is small (8 IPL cubes, 5 dog test scans, 2 ovine scans).
* Analyst time saving has not been measured; the "≈78%" figure from Experiment M is a model of assumed effort
  constants and is not a result.
