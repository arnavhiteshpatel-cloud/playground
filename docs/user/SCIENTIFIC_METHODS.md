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
| **Segmentation** | Labels inside the ROI: 1 new bone, 2 residual graft, 3 host bone, 0 non-mineral, 255 uncertain | Methods: `advisor_threshold` (default; the threshold implied by the advisor, the only method carrying measurement support), `multiotsu`, `ctan_style` (two fixed thresholds), random forest, locked U-Net (PyTorch or ONNX Runtime). Out-of-field padding and metal are excluded before thresholds are computed ([REAL] without this, new-bone fraction read 1.00 on an ovine scan; with it 0.21) |
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
  `new_bone_fraction_of_certain` = V(NB)/TV<sub>certain</sub> removes the material-dependent abstention bias. The same applies
  to residual graft. The PDF and CSV report print the TV-denominator fractions; the `*_of_certain` fractions and the
  architecture endpoints (BV/TV, Tb.Th, Tb.Sp, Tb.N, Conn.D) are kept in the analysis record and the library output
  but are **not yet printed in the report**.
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
physical truth in validation stage B. NBV relative bias within ±10%: the criterion *proposed* for PQ-01 in the draft
PQ plan (`docs/quality/PQ_PLAN.md`); it has to be aligned with the stage-B criterion before the PQ is executed.

**Group statistics in reports.** Group means are reported with SD and a t-based 95% confidence interval. The interval
is clipped to the physical range of the endpoint (volumes ≥0, fractions 0–1) and a clipped limit is marked "†"; for
n <3 per group no interval is printed. Specimens without a group are listed but excluded from group statistics.

---

## 3. Measurement-support advisor (1.4.3)

Implementation: `osteoquant/advisor/separability.py` (`ADVISOR_VERSION = "1.4.3"`) and `integration.py`. Every
assessment records the advisor version, and the PDF report prints it. Policy:
[MEASUREMENT_SUPPORT.md](../science/MEASUREMENT_SUPPORT.md). Evidence: §3.6.

### 3.1 The question

A segmentation method always outputs a residual-graft volume. For many materials that number is not identifiable:
graft and new bone share the same attenuation range (§3.5). The advisor decides **before reporting** whether each
endpoint can be measured, by which mechanism, and under which conditions.

### 3.2 Inputs

| Input | Default source | Preferred source |
|---|---|---|
| Graft material | Your selection in the analysis dialog | — |
| Graft intensity distribution | Material profile from the knowledge base, cross-checked against NIST attenuation physics × assumed porosity | Measured: a day-0 scan or a scan of the material alone, same scanner and protocol |
| New-bone intensity | Assumed maturity range 0.60–1.00 of host bone (a narrower early-healing range, 0.60–0.93, is defined in the code but not yet applied, even when the timepoint is known) | Measured from empty-defect controls at the same timepoint |
| Noise | Median absolute deviation of soft tissue outside the defect (conservative: includes tissue texture) | — |
| Blur | Edge-spread fit at host-bone/soft-tissue edges outside the defect, inflated conservatively above 0.6 voxel | — |
| Graft granule thickness and graft level | Measured in the scan (local thickness of graft-like voxels; their level one voxel inside the granules) | — |
| Grey-scale anchor | Soft-tissue and host-bone levels outside the defect | HA calibration phantom |
| Time since implantation | The scan's timepoint in the desktop (days, or a label such as "Week 4"); unknown if neither is usable | Entered explicitly in the analysis dialog when timepoint labels are not times |
| Day-0 information | Registration result, QC, granule tracking | — |

**Relative mineral units.** Grey values are converted to r = (x − soft)/(host − soft), so soft tissue ≈ 0 and mature
host bone ≈ 1 without HA calibration. Noise is expressed the same way (`noise_rel`).

### 3.3 How a decision is computed

1. **Class models.** The graft is modelled as a normal distribution from its profile (or as measured samples), new bone
   as a uniform maturity range. Both get the scan's noise and partial-volume mixing: a share of voxels is mixed towards
   neighbouring phases (soft tissue, the other class, host bone). For the graft that share comes from the measured
   blur and granule thickness (a two-sided edge model, Φ(δ/σ) + Φ((T−δ)/σ) − 1 of each granule's voxels keep their own
   value); for new bone and halos it comes from voxel and structure size. Measured reference samples get the analysis
   scan's noise added.
2. **Oracle.** For two histograms, every voxel-wise intensity rule is a union of bins; the Dice-maximising union is the
   *intensity-only oracle*, an upper bound for any threshold workflow. If the oracle fails, every threshold fails.
3. **The rule actually applied.** Because real methods use a single threshold, the decision uses the best
   *single-threshold* rule (the oracle is reported as the upper bound). Among near-optimal thresholds, the one with the
   smallest volume error is chosen.
4. **Robustness to graft share.** Volume error grows as residual graft becomes scarce, so the rule must pass at the
   graft share estimated from the scan **and** at half of it.
5. **Mineral rule.** New bone versus soft tissue is checked with partial-volume halos of dense phases. If that boundary
   is not reliable, mineral and new-bone endpoints are withdrawn too.
6. **Profile checks.** The intensity mechanism is also refused when the material profile is uncertain (knowledge base
   and physics model disagree by >25%), when the scan's graft-like intensities disagree with the profile by >15%, or
   when a resorbable material is scanned at an unknown timepoint or later than 4 weeks (rules 4a–4c below). A
   measured material reference lifts the first two refusals; nothing lifts the third except a known early timepoint.
7. **New bone is mineral minus graft.** Its relative error is its own error plus the graft error scaled by p/(1−p),
   where p is the scan's graft share of mineral; new-bone endpoints need the propagated error ≤10%.
8. **Ambiguous rim.** Mineral that is not graft-like but lies within max(1, ⌈2σ⌉) voxels of graft-like voxels may be
   new-bone coating or graft halo. New-bone endpoints are refused if this rim exceeds 10% of the would-be new bone;
   total mineral is refused if the worst-case error, rim / (mineral − rim), could exceed 20%. With no material model
   (unspecified material), voxels brighter than host bone stand in for the graft in this check (since 1.4.3).

### 3.4 Decision rules

| # | Rule | Outcome |
|---|---|---|
| 1 | Noise ≥0.35 of the bone–soft-tissue contrast, or the mineral rule fails | Mineral endpoints (total mineral volume, mineralised fraction) and new-bone endpoints **not supported** |
| 2 | Radiolucent graft (mean <0.15 of host: collagen sponge, PLGA, PCL) | Graft endpoints **not supported** (invisible); new-bone endpoints **supported with conditions** ("graft has no mineral phase") |
| 2a | DBM (radiolucent but bone-derived) | Graft **and** new-bone endpoints **not supported**: mineralised DBM particles are indistinguishable from new bone |
| 3 | Intensity mechanism: single-threshold graft Dice ≥0.85 **and** graft-volume ratio within ±10%, at the estimated graft share and at half of it | Graft and new-bone endpoints **supported** |
| 3a | Graft share below 5% of mineral | Graft-volume endpoints **not supported** ("trace residual graft") |
| 4 | Bone-derived graft (autograft, allograft, DBBM xenograft, DBM) | Never supported by intensity, even with measured samples. The remodelling grafts (autograft, allograft, DBM) are **never supported by the day-0 mechanism** either: their footprint becomes bone. Slowly resorbing DBBM may use the day-0 mechanism (since 1.4.2) |
| 4a | Knowledge-base profile and NIST physics model disagree by >25% (currently β-TCP and bioactive glass 45S5) and no measured material reference | Intensity mechanism refused ("material appearance is uncertain") |
| 4b | Scan-versus-profile consistency: the median of the defect's graft-like intensities (brighter than mature bone) differs >15% from the profile's graft level, and no measured reference | Intensity mechanism refused (profile does not describe this scanner/protocol) |
| 4c | Resorbable material (β-TCP, BCP, calcium sulfate, bioactive glasses 45S5 and S53P4, polymer–ceramic composites) at an unknown timepoint or later than 4 weeks | Intensity mechanism refused; the reason states the timepoint used ("timepoint: unknown" or the weeks) |
| 5 | Intensity fails, but a registered day-0 scan passes registration QC, with granule motion ≤200 µm (or tracked) and ≤20% untracked graft volume; all four day-0 fields computed by the software; graft not bone-derived | **Supported with conditions**. For resorbable materials the conditions state that bone formed inside the original footprint is counted as graft. There is no desktop day-0 workflow |
| 6 | Texture/morphology model | Only with material-specific validation evidence in the model card (none exists) |
| 7 | Material not in the knowledge base, or measured reference samples with <500 voxels | **Not supported** until characterised |
| 7b | Measured new-bone reference (empty-defect controls) | Used, with graft-adjacent partial-volume mixing and the analysis scan's noise added, because control new bone lacks the blur of new bone next to dense graft |
| 7a | Metals (magnesium, titanium) | Never supported, including total mineral (streak and beam-hardening artefacts are not modelled) |
| 9 | Propagated new-bone error >10% (step 7) | New-bone endpoints **not supported** |
| 10 | Ambiguous rim >10% of new bone, or worst-case mineral error rim/(mineral − rim) >20% (step 8) | New-bone, or total-mineral, endpoints **not supported** |
| 12 | Resorbable material with a day-0 scan, time since implantation unknown or >12 weeks (policy constant) | Day-0 mechanism **not supported**: the footprint is replaced by bone |
| 13 | Knowledge-base profile without a physics cross-check (S53P4, polymer–ceramic composite) | Treated as uncertain: intensity support needs a measured reference |
| 14 | Stored result analysed by another advisor version or support-rule set, or before method binding | Shown as **not assessed** ("re-analyse"); a manually corrected segmentation keeps at most *supported with conditions* |
| 11 | Segmentation method other than the advisor's own threshold (`advisor_threshold`) | Tissue endpoints **not supported**; graft endpoints of a learned model only with a qualifying signed validation record (none exists). Tissue mineral density is unaffected |
| 8 | Density endpoints | Only with HA calibration |
| — | New-bone thickness endpoints | Need structures ≥3 voxels (about 150 µm woven trabeculae) and supported new bone |

Each endpoint's result carries a status, the mechanism (intensity, day-0 registration, radiolucent graft, no-graft
design, calibration) and a reason. Conditions are listed with *supported with conditions*.

**Additional flags in the desktop.** Independently of the material, the desktop marks every endpoint *flagged* when
uncertain voxels exceed 10% of the ROI and *not supported* above 25%; flags Tb.Th below 2.5 voxels as
partial-volume dominated; and flags results whose QC verdict is unsuitable, whose plausibility checks failed or whose
automatic ROI requires review.

### 3.5 What the advisor does **not** do

* It does not evaluate the quality of a segmentation. Support is bound to the method it was validated with
  (`advisor_threshold`, the desktop and pipeline default, which applies the advisor's own threshold); other methods
  are refused by name (rule 11). Within that method, a supported endpoint can still be mis-measured when the scan
  differs from anything validated in simulation.
* It does not validate its own material profiles. Porosities and granule sizes are assumptions; the advisor and the
  phantom simulator share the same attenuation model, so their agreement in simulation is partly self-consistent.
* Its thresholds (0.85, ±10%, 0.35, 25%, 15%, 10%, 20%, 4 weeks, 200 µm) are policy choices, to be revisited with
  real data.

### 3.6 Evidence for the advisor

[SYNTHETIC, pre-registered held-out tests] In the pre-registered held-out simulation S1H4 (advisor 1.4.3; 720 synthetic specimens from 36 phantom structures, knowledge-base and Unspecified material paths; a failure is a volume error above 20%): residual graft volume supported in 10% of specimens (HA only), every failing measurement refused and none of the supported ones failed (95% upper bound on the supported-failure rate 0.14 counting phantom structures as the unit; 0.052 if the 69 supported measurements were independent); supported graft volumes: median error 2.2%, maximum 11.4%; total mineral volume supported in 2% of specimens (β-TCP at PSF 40 µm only); supported mineral volumes: maximum error 16.9%; new-bone volume never supported; no volume endpoint supported for 89% of specimens. An earlier held-out test of advisor 1.4.1 (S1H3, 9 phantom structures) is recorded in the experiment registry.

This test used the shipped advisor 1.4.3, frozen before the run. The simulator and the advisor share attenuation physics, so this is evidence of internal safety, not of accuracy on real scans; no physical validation has been run. Two earlier held-out tests found supported measurements that failed: S1H (advisor 1.3.3: supported new-bone
volumes over-estimated by 20–50% and some supported graft volumes under-estimated by 21–28%, under wider blur) and S1H2 (advisor 1.4.0: supported total mineral over-estimated
under heavy blur). Each failure led to a rule (scan-measured blur, new-bone error propagation, the blur-scaled
ambiguous rim) that was then tested on new held-out data, not on the data that revealed it. The in-sample development
experiments (S1, S1b, S1c) are in [EXPERIMENT_REGISTRY.md](../../EXPERIMENT_REGISTRY.md) and are not evidence of
generalisation. The day-0 rule is discussed with Experiment L3 in §5.

**Why separability fails** [SYNTHETIC, Experiments C and C2]: when graft density lies in the overlap regime
simulated in Experiment C (800–1000 mgHA/cm³, inside the assumed 650–1000 mgHA/cm³ woven-bone range), the
intensity-only oracle reaches graft Dice 0.52–0.77 depending on noise. A random forest with
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
2. **Registration QC.** Residual displacement measured by masked normalised cross-correlation in eight blocks of a
   shell around the defect; each block's shift is projected onto the directions its structure constrains; pass if every
   block is within 2 voxels **and** every direction is constrained by at least one block. Along the axis of a featureless
   diaphyseal tube a shift cannot be measured: the QC then fails closed and names the unverifiable direction
   (cycle-3 review; Experiment L5: 0/18 misregistrations passed, aligned specimens reported as not verifiable). This replaced a host-mineral Dice criterion that rejected 56% of harmless misalignments
   (Experiment L4). [SYNTHETIC] L4: all 6 harmful misalignments flagged; 78% of harmless ones passed (the others were
   4–8° rotations beyond the tolerance that had not yet lowered graft Dice by 0.10).
3. **Footprint.** Mineral inside the ROI on day 0.
4. **Granule tracking** (optional). Per-granule search for displacement; reports the share of graft volume that could
   not be tracked and the 90th-percentile shift.
5. **Advisor rule 5** (§3.4) decides whether graft endpoints are *supported with conditions*.

**Best-case evidence** [SYNTHETIC, Experiments L and L2]: when the simulated graft only shrinks in place, the day-0
footprint gives graft Dice 0.915 in the overlap regime, and 0.816 with strut-like granules where a single-scan random
forest gives 0.663 and the intensity oracle 0.323.

**Limits shown by Experiment L3** [SYNTHETIC, generator v2, strut-like granules in the overlap regime, 3 seeds per
cell; result file `exp_L3_displacement.json`]:

* **The day-0 method is fragile under granule motion.** Naive day-0 footprint graft Dice — no motion: 0.80;
  50 µm motion: 0.535; 100 µm motion: 0.35. The loss happens well inside the advisor's 200 µm tolerance, and
  fragmentation lowers it further.
* Conservative granule tracking does not rescue this regime: small strut-like granules in heavy noise cannot be
  localised, so a large share of the graft volume stays ambiguous.
* **The advisor refuses these cases**, because the computed untracked fraction exceeds its limit. An earlier tracking
  version produced spurious matches that an earlier advisor accepted; that defect is fixed, and the re-run is
  recorded in the registry.
* Deliberately skipped registrations were always flagged by registration QC.
* Day-0 therefore works in simulation **only without granule motion**. It is not a general solution, and it is not
  offered in the desktop application.
* **Bone ingrowth within a resorbing footprint.** Bone formed inside the original footprint of a resorbing ceramic or
  glass (β-TCP, calcium sulfate, bioactive glass) is counted as graft, so residual graft is over-estimated and new
  bone under-estimated. The generator models resorption as shrinkage and translation, not replacement, so simulation
  cannot reveal this bias.
* **Remodelling bone-derived grafts** (autograft, allograft, DBM) are never supported by the day-0 mechanism: the
  footprint is remodelled into bone. Slowly resorbing DBBM may be (since advisor 1.4.2).
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
* The advisor has been tested only in simulation (held-out tests S1H3 and S1H4), where it refused every failing
  measurement; in S1H4 (shipped advisor, the application's material paths) it supported residual graft only for HA,
  total mineral rarely and new bone never, and nothing with the material set to Unspecified.
* The day-0 method degrades with tens of micrometres of granule motion, counts bone formed inside a resorbing
  footprint as graft, and has no desktop workflow.
* **Biological limits.** In segmental and long-bone models the bone-diameter cylinder ROI excludes periosteal and
  external callus (bridging and new bone are under-estimated; external callus is labelled host bone). Calcified
  cartilage in endochondral healing (roughly 1–4 weeks) reads as mineral or new bone. Ectopic bone (e.g. from rhBMP-2
  collagen carriers), mineralised debris and haematoma inside the ROI are counted as new bone.
* Out-of-distribution detection is weak; no volume intervals yet.
* Real-data n is small (8 IPL cubes, 5 dog test scans, 2 ovine scans).
* Analyst time saving has not been measured; the "≈78%" figure from Experiment M is a model of assumed effort
  constants and is not a result.
