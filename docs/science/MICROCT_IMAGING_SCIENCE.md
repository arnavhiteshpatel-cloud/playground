# Micro-CT Imaging Science and the Calibration and Data-Quality Framework

Status: v1, 2026-11-27. Evidence tags are as in `BONE_BIOLOGY_AND_GRAFTS.md`: [RF], [RF-derived], [PK], [UNR], [ASSUMPTION]. References are in `REFERENCES.md`.

---

## 1. Image formation in one page

### 1.1 Attenuation

- A monoenergetic beam follows Beer–Lambert: I = I0·exp(−∫μ(x,E)dx).
- The linear attenuation coefficient is μ = ρ·(μ/ρ). (μ/ρ) is the mass attenuation coefficient, the weight-fraction sum over the elements present [PK; tabulated in NIST SRD 126, R59].
- At micro-CT energies (≈ 20–80 keV effective) two processes dominate:
  - **Photoelectric absorption** scales roughly as Z³–Z⁴/E³ [PK]. It dominates for Ca (Z = 20) and P (Z = 15) at low energy.
  - **Compton scatter** is roughly proportional to electron density and nearly energy-independent [PK].
- **Consequence:** contrast between materials with different effective Z changes with energy. Examples are bioactive glass (Na, Si) vs bone (Ca, P), CaSO4 (S), and Mg alloys. This is the physical root of "grey values aren't interchangeable" (§3).

### 1.2 Polychromatic sources

- Desktop μCT tubes emit a bremsstrahlung spectrum, typically 40–100 kVp with Al or Cu filtration [PK].
- Low energies are preferentially absorbed, so the beam "hardens" with path length. Thick or dense objects then appear less attenuating in the centre (cupping) and streaks appear between dense objects (§4.2).
- Kazakia 2008 compared desktop μCT (Scanco µCT 40, 70 kV, 8 µm) with synchrotron μCT (monochromatic 26 keV) and ash [RF, R23]:
  - Desktop μCT TMD was **12.9–15.0% lower** than SRμCT.
  - Ash density was 8.6–10.9% higher than SRμCT.
  - Values remained well correlated within a volume-fraction group.

### 1.3 Reconstruction

- Cone-beam systems usually reconstruct with the Feldkamp–Davis–Kress (FDK) filtered back-projection algorithm [R28; algorithm described as "practical cone-beam algorithm"].
- FDK is exact only in the central plane. Off-plane cone-beam artifacts grow with cone angle [PK].
- **Parameters that change grey values and texture [PK]:**
  - reconstruction filter/kernel (ramp, Shepp–Logan, Hann)
  - smoothing
  - beam-hardening correction (software polynomial or wedge-based; Scanco uses HA-wedge corrections, e.g. 200 vs 1200 mg HA/cm³ [RF, R21, R23])
  - ring-artifact correction
  - misalignment/centre-of-rotation correction
  - output scaling and dynamic range: e.g. Bruker NRecon maps an attenuation-coefficient window to 8- or 16-bit grey values [PK]; Scanco stores linear attenuation scaled to integers and reports per-mille of a maximum [RF: Kim 2021 per-mille thresholds, R7]
- **Effect sizes:**
  - Changing the Scanco beam-hardening correction from 200 to 1200 mg HA/cm³ changed callus TMD by **9.7%** and its SD by 16.1% [RF: Morgan 2009, R21].
  - In human trabecular cores it raised TMD by 4.7% in high-volume-fraction specimens [RF: R23].

### 1.4 Voxel size vs true spatial resolution

- The **nominal voxel size is not the resolution.** True resolution is set by focal-spot size, detector pixel and scintillator blur, geometric magnification, motion, and reconstruction filter. It is characterized by the modulation transfer function (MTF), e.g. the 10% MTF point [PK].
- **Example [RF: Stalder 2014, R30]:** synchrotron μCT at 2.17 µm pixel (binned ×2) gave a spatial resolution of 4.37 µm, derived from the 10% MTF value. That is about 2× the pixel size even on a synchrotron.
- Verdelis 2011 [RF, R26]: "the effective resolution may not be changing as much as the voxel size" when moving from 12 to 8 µm voxels on desktop systems.
- **Rule of thumb for morphometry:** at least 3–4 voxels across the smallest structure. Mouse trabeculae are about 40 µm, so a 6–10 µm voxel is recommended, 15–20 µm is acceptable, and anything coarser is not recommended [RF: Kim 2021, R7].
- Christiansen 2016 [RF, R11] found that a 6–30 µm voxel range strongly affected Conn.D, Tb.Th, and TMD. Segmentation methods agreed at small voxels but diverged at large voxels.

### 1.5 Partial-volume effect (PVE)

A voxel straddling two materials takes an intermediate value. Our 1-D simulation [RF-derived/ASSUMPTION model: a 1100 mg HA/cm³ plate, Gaussian PSF, 50% threshold, run in the scratchpad] shows three things.

**1. Thin structures lose peak density.**

| True thickness (voxels) | Peak value at PSF FWHM = 1 voxel | Peak value at FWHM = 2 voxels | Peak value at FWHM = 3 voxels |
|---|---|---|---|
| 1 | 730 | 464 (below threshold → structure lost) | 328 (lost) |
| 2 | 1045 | 808 | 611 |
| 3 | 1097 | 996 | 824 |
| 4 | 1100 | 1072 | 962 |
| 6 | 1100 | 1099 | 1076 |

**2. The mean TMD of segmented voxels is biased low** even for thick structures, because the surface voxels are included. At FWHM = 2 voxels it is 808–1013 for 2–10-voxel plates whose true density is 1100.

- So TMD depends on structure thickness and on voxel size. This explains why early, thin woven-bone trabeculae read "less mineralized" partly for purely physical reasons.
- Mitigation: erode 1–2 surface voxels before computing TMD. Leong & Morgan removed 2 voxels from all surfaces [RF: Leong & Morgan 2009, R22]. Alternatively, report TMD only for structures thicker than 4× the PSF FWHM [ASSUMPTION].

**3. Edge halo at graft–tissue interfaces.**

- A 3000 mg HA/cm³ granule next to 700 mg HA/cm³ woven bone, at FWHM = 2 voxels, produces boundary voxels of about 1850 and 1000. These are values typical of *mature bone* or bioactive glass.
- Purely intensity-based classification therefore places a thin "bone" shell on every graft surface.
- This is exactly the artifact reported for xenografts: μCT "interprets the borders of the granules as newly formed bone tissue", inflating bone–material contact [RF: Kapogianni 2019, R14].
- **The phantom generator must reproduce this halo.** Apply the PSF to the true label image before noise, never after labeling.

### 1.6 Noise

- Quantum (Poisson) noise is set by photon count: tube current × exposure time × number of projections × frame averaging, and filtration [PK].
- Noise in reconstructed voxels scales roughly as 1/√(dose), and increases sharply as voxel size shrinks at fixed dose [PK].
- **In vivo imaging:** radiation dose limits the noise floor, and repeated scans can themselves affect bone [PK]. In vivo scans therefore have larger voxels and more noise than ex vivo scans.
- **Noise texture:** FBP gives correlated, not white, noise. The phantom generator should add noise in projection space and reconstruct, or approximate it with a filtered-Gaussian noise model [ASSUMPTION].

### 1.7 Orientation and positioning

- Long bones should be scanned with the long axis parallel to the rotation axis, and calvaria with the defect plane perpendicular to it (or consistently oriented) [PK].
- Beam-hardening and cone-beam artifacts are orientation-dependent. VOIs defined relative to anatomical landmarks require re-orientation (registration to a template) before analysis [PK].
- Bouxsein 2010 requires reporting of VOI size and location and of how regions were delineated [RF: R1 abstract].

---

## 2. Scanning medium and specimen preparation

- **Report the medium** (Bouxsein requirement [RF: R1]): PBS, saline, 70% ethanol, formalin, air, or PMMA embedding.
- The medium changes the calibration relationship. Nazarian 2008 found that **tube voltage, object-to-source distance, detector array size, and imaging medium** all significantly affected the μ → density conversion, whereas current, integration time, and projection number did not [RF: R25]. Scanco solid phantoms "cannot be scanned with a specimen or submerged in a different imaging media" [RF: R25].
- **PMMA embedding** (common for undecalcified histology): PMMA, soft tissue, and low-mineralized bone share a common histogram peak [RF: Stalder 2014 citing Bernhardt et al., R30].
- **Decalcified specimens are useless for mineral-based μCT.** Specimens must be scanned before decalcification.

---

## 3. Material attenuation and HA-equivalent density: the core table

### 3.1 Method [RF-derived]

1. Elemental mass attenuation coefficients for H, C, N, O, Na, Mg, Si, P, S, Cl, K, Ca, Ti were taken from NIST SRD 126 (Hubbell & Seltzer) [R59].
2. ICRU-44 compositions and densities for cortical bone (1.92 g/cm³), soft tissue (1.06), and adipose (0.95) were taken from NIST Table 2 [R59].
3. μ(E) was computed by log-log interpolation.
4. Densities used: HA 3.16 (R32: 3.155), β-TCP 3.07 (R32: 3.067), CaSO4 anhydrite 2.96 (NIST), CaSO4·2H2O 2.32 [PK], bioactive glass 2.70 [PK], Mg 1.74 [PK], Ti 4.51 [PK].
5. **HA-equivalent density** was defined as the reading of an ideal scanner calibrated with HA dispersed in a water-equivalent matrix: ρ_HAeq = (μ_m − μ_w)/((μ/ρ)_HA − μ_w/ρ_HA).

### 3.2 Linear attenuation μ (cm⁻¹)

| Material (density g/cm³) | 20 keV | 25 keV | 30 keV | 40 keV | 50 keV | 60 keV | 80 keV |
|---|---|---|---|---|---|---|---|
| HA, dense (3.16) | 20.73 | 11.06 | 6.63 | 3.12 | 1.85 | 1.29 | 0.82 |
| β-TCP, dense (3.07) | 19.92 | 10.63 | 6.38 | 3.00 | 1.78 | 1.24 | 0.79 |
| CaSO4 anhydrite (2.96) | 17.26 | 9.24 | 5.55 | 2.64 | 1.59 | 1.12 | 0.73 |
| CaSO4·2H2O (2.32) | 11.09 | 5.98 | 3.63 | 1.77 | 1.10 | 0.80 | 0.54 |
| Bioglass 45S5 (2.70) | 11.05 | 5.98 | 3.63 | 1.80 | 1.14 | 0.84 | 0.59 |
| Bioglass S53P4 (2.70) | 10.21 | 5.55 | 3.38 | 1.69 | 1.08 | 0.81 | 0.58 |
| Cortical bone ICRU-44 (1.92) | 7.68 | 4.18 | 2.56 | 1.28 | 0.81 | 0.60 | 0.43 |
| Mg metal (1.74) | 4.81 | 2.64 | 1.62 | 0.85 | 0.57 | 0.45 | 0.34 |
| Soft tissue ICRU-44 (1.06) | 0.87 | 0.57 | 0.40 | 0.29 | 0.24 | 0.22 | 0.19 |
| Water (1.00) | 0.81 | 0.53 | 0.38 | 0.27 | 0.23 | 0.21 | 0.18 |
| Adipose ICRU-44 (0.95) | 0.54 | 0.38 | 0.29 | 0.23 | 0.20 | 0.19 | 0.17 |
| Ti (4.51) | 71.5 | 37.8 | 22.4 | 9.99 | 5.47 | 3.46 | 1.83 |

**Cross-check against measurement:** at 25 keV the computed cortical-bone μ is 4.18 cm⁻¹. Stalder 2014 measured new bone at about 3.8 cm⁻¹ and BCP granules at about 7.5 cm⁻¹ by SRμCT at 25 keV [RF, R30]. That is consistent with less-mineralized new bone and BCP granules at roughly 68% of dense-HA attenuation.

### 3.3 HA-equivalent density (mg HA/cm³)

| Material | 20 keV | 25 keV | 30 keV | 40 keV | 50 keV | 60 keV | 80 keV |
|---|---|---|---|---|---|---|---|
| HA dense | 3160 | 3160 | 3160 | 3160 | 3160 | 3160 | 3160 |
| β-TCP dense | 3032 | 3031 | 3030 | 3028 | 3026 | 3024 | 3020 |
| CaSO4 anhydrite | 2610 | 2613 | 2615 | 2630 | 2653 | 2680 | 2732 |
| CaSO4·2H2O | 1631 | 1636 | 1641 | 1661 | 1691 | 1724 | 1789 |
| 45S5 | 1624 | 1636 | 1645 | 1696 | 1769 | 1852 | 2014 |
| S53P4 | 1491 | 1505 | 1515 | 1575 | 1661 | 1758 | 1947 |
| Cortical bone ICRU-44 | 1090 | 1095 | 1101 | 1118 | 1141 | 1167 | 1217 |
| Mg | 634 | 634 | 628 | 644 | 672 | 707 | 776 |
| Soft tissue | 10 | 11 | 13 | 18 | 25 | 33 | 48 |
| Adipose | −43 | −44 | −43 | −45 | −49 | −54 | −63 |

**Interpretation:**

1. **CaP ceramics (HA, β-TCP)** are chemically bone-like, so their HA-equivalent value is energy-independent. When dense they are about 2.8× bone tissue. All their contrast with bone comes from *density/packing*, which erodes as micro-porosity rises or resorption proceeds.
2. **Bioactive glass, CaSO4, and Mg** have energy-dependent HA equivalents. The same specimen will read differently at 50 vs 90 kVp, or with different filtration, even on a perfectly HA-calibrated scanner. The glass/bone ratio is about 1.4 at 30 keV and about 1.65 at 80 keV.
3. **Bone itself** is not exactly HA in collagen/water: ICRU cortical bone drifts from about 1090 to 1220 across energy. So "mg HA/cm³" is an *equivalent* unit, not a true mineral concentration [PK, consistent with R23's ash offset].

---

## 4. Artifacts

| Artifact | Cause | Effect on graft/bone analysis | Mitigation | Evidence |
|---|---|---|---|---|
| Beam hardening (cupping, streaks) | Polychromatic beam | TMD biased by position and specimen size; dense grafts or metal cause streaks into neighbouring bone. Artifacts **up to 32.6%** in mineralized-tissue-sized samples. The number of bones in the beam path and the scan set-up changed murine cortical and trabecular densitometry | Al/Cu filtration; wedge-phantom correction matched to the object (200 vs 1200 mg HA/cm³ changes TMD 4.7–9.7%); consistent specimen size and holder | [RF: Meganck 2009, R24; Kazakia 2008, R23; Morgan 2009, R21] |
| Geometric non-uniformity of TMD | Cone-beam + beam hardening | Spatial TMD gradients in desktop μCT, reduced but not eliminated by the 1200 mg HA/cm³ correction; absent in SRμCT | Position the ROI near the central plane; correct radially | [RF: R23] |
| Scatter | Compton scatter to the detector | Reduced contrast, cupping, streaks between dense objects | Collimation, anti-scatter processing | [PK] |
| Ring artifacts | Defective or miscalibrated detector pixels | Concentric rings, often through the defect centre in centred calvarial scans; mimic thin bone/graft arcs | Flat-field calibration, detector shifting/"random movement", sinogram ring filters | [RF: Boin & Haibel 2006, R29 (synchrotron)] + [PK] |
| Motion | Animal breathing (in vivo), drying/shrinkage (ex vivo) | Blur, double edges | Immobilization, respiratory gating, hydrated scanning | [PK] |
| Metal artifacts (Ti plates, screws, Mg alloy) | Photon starvation, beam hardening | Streaks obliterate peri-implant bone | Higher kVp, Cu filter, MAR algorithms, ROI exclusion bands | [PK] |
| Reconstruction artifacts at individual slices | Misalignment, centre-of-rotation errors | Local histogram distortion. Stalder 2014 saw correlation drops at slices with reconstruction artifacts | Per-slice QC on histogram consistency | [RF: R30] |
| Partial volume | Finite PSF and voxel | Thin trabeculae lost or under-dense; graft-edge halo classified as bone | High resolution; PSF-aware or model-based segmentation; surface erosion for TMD | [RF-derived §1.5; RF R14, R22] |

---

## 5. Cross-scanner and cross-protocol variation

### 5.1 Evidence

- **Verdelis 2011 [RF, R26]:** the same mouse distal femora on GE eXplore Locus SP, Scanco µCT35, and SkyScan 1172, at 12 and 8 µm voxels.
  - BV/TV and Tb.Sp were similar across systems.
  - Tb.Th differed by up to **236%** and Tb.N by up to **218%**.
  - Tb.Th ranges were 21–29 µm (GE), 37–45 µm (Scanco), and 50–63 µm (SkyScan).
  - The systems used different density calibration paradigms: pre-reconstruction phantom (GE), automatic built-in (Scanco), and post-reconstruction phantom (SkyScan). No single threshold could be shared.
  - Conclusion: "trabecular morphometry measurements should not be directly compared across microCT systems."
- **Nazarian 2008 [RF, R25]:** the μ-to-density calibration depends on kVp, source–object distance, detector array size, and imaging medium.

### 5.2 Vendor landscape

All entries are [PK] unless noted. Vendor specification sheets were not fetched in this review, so no performance figures are quoted.

| System family | Typical use | Native output | Notes for OsteoQuant |
|---|---|---|---|
| Bruker SkyScan (1172, 1272, 1275, 1276) | Ex vivo and in vivo (1176, 1276) | Reconstructed attenuation mapped to 8/16-bit grey by a user-set window in NRecon; BMD by post-hoc phantom calibration in CTAn (e.g. 0.25 and 0.75 g/cm³ HA rods) | Grey-to-μ mapping varies per dataset with the "contrast limits". **Must capture the NRecon log file** (window, smoothing, beam-hardening %, ring-artifact level) |
| Scanco Medical (µCT 35/40/45/50/100, vivaCT, XtremeCT) | Ex vivo, in vivo, HR-pQCT | Linear attenuation stored as scaled integers; density via factory HA calibration (QC1 phantom weekly [RF: R7]); per-mille thresholds; BH correction wedge (e.g. 200 or 1200 mg HA/cm³ [RF: R21, R23]) | Calibration slope/intercept in the ISQ/AIM header; analysis in IPL |
| Zeiss Xradia Versa / Context | X-ray microscopy (two-stage magnification, sub-µm voxels) | Grey values not natively density-calibrated; source filters and "beam hardening constant" per scan | Excellent resolution; density units require a co-scanned phantom under identical filter/kV |
| PerkinElmer / Rigaku Quantum (GX, GX2, FX) | Fast in vivo, larger FOV | HU-like scaling | Larger voxels (tens of µm) → PVE dominates; suited to defect fill and bridging, not Tb.Th |
| GE eXplore Locus SP (legacy) | Ex vivo | Pre-reconstruction phantom calibration [RF: R26] | Legacy datasets |
| Clinical CT / dental CBCT | Large-animal and clinical | HU (CT). CBCT grey values show "great variability" (limited field size, high scatter, reconstruction limitations); "quantitative use of GVs in CBCT should be generally avoided" [RF: Pauwels 2015, R60] | Do not treat CBCT grey values as HU. Structural analysis is preferred [RF: R60] |

### 5.3 Why grey values aren't interchangeable

1. **Different physical quantity per vendor:** μ, scaled μ, HU, or windowed 8-bit [RF partially: R26 calibration paradigms].
2. **Spectrum-dependent μ:** kVp, filtration, and specimen size via beam hardening [RF: R24, R25].
3. **Calibration-dependent HA equivalence:** the medium and geometry matter [RF: R25]. Non-HA materials have energy-dependent HA equivalents [RF-derived §3.3].
4. **Reconstruction filters and corrections** alter means and texture [RF: R21, R23].
5. **Different effective resolutions** at the same nominal voxel size, so different PVE [RF: R26, R11].
6. **Post-processing:** Gaussian sigma/support, thresholds in per-mille vs mg HA vs grey [RF: R7, R22].

---

## 6. OsteoQuant calibration and data-quality framework

### 6.1 Tiered data-quality levels

| Tier | Requirements | Allowed outputs |
|---|---|---|
| **Q0: Uncalibrated grey** | Image + voxel size only | Binary morphometry *within-dataset only* (BV/TV, Tb.Th, etc.) with a "not comparable across scanners" flag. No density units. Graft/bone classes only by morphology priors |
| **Q1: Protocol-documented** | All required metadata (§6.2) present; same scanner and protocol across groups | Morphometry comparable within the study. Relative density (Δ grey or %-of-host-cortex) allowed |
| **Q2: Density-calibrated** | Q1 + HA phantom scanned with the **same kVp, filter, medium, holder, and reconstruction** (ideally same session); linear fit with R² ≥ 0.99 [ASSUMPTION]; ≥ 2 phantom rods within the bone range (e.g. 250 and 750, or 0–800 mg HA/cm³) | TMD, vBMD, BMC in mg HA/cm³; density-based class thresholds |
| **Q3: Cross-site harmonized** | Q2 + a travelling/reference phantom (density rods + resolution target such as wire/edge for MTF) scanned on each system; MTF and noise (NPS) measured | Cross-scanner pooling with harmonization; resolution-matched morphometry (resample to the worst common MTF) |
| **Q4: Validated** | Q3 + co-registered histology or SRμCT ground truth for a subset | Graft vs new bone volumes with stated accuracy and uncertainty |

**Rule:** density units (mg HA/cm³) may only be reported at Q2 or higher. For non-HA materials (bioactive glass, CaSO4, Mg), mg HA/cm³ must be labeled "HA-equivalent at <kVp/filter>". Values must not be compared across energy settings [RF-derived §3.3].

### 6.2 Required metadata (ingest schema)

**Acquisition (from Bouxsein 2010 [RF R1] plus imaging physics):**

- Scanner make/model/serial, software version
- kVp, µA, filter (material, thickness), focal spot mode, exposure/integration time, frame averaging
- Number of projections, rotation step and angle (180° + fan vs 360°)
- Source–object and source–detector distances (magnification), detector binning
- Nominal voxel size (isotropic?), FOV, in vivo/ex vivo
- Scanning medium, specimen holder, specimen orientation
- Date/time; phantom scan ID (same session?)

**Reconstruction:**

- Algorithm (FDK or other), filter/kernel, smoothing
- Beam-hardening correction (type, %, wedge density), ring-artifact correction level, misalignment/centre-of-rotation compensation
- Output data type, scaling (grey ↔ μ mapping, window limits), HU or μ units

**Calibration:**

- Phantom type (solid HA-resin vs K2HPO4 liquid), rod densities, fit coefficients, R², date
- Wedge/BH calibration
- QC log (e.g. Scanco QC1 weekly density and QC2 geometry [RF: R7])

**Analysis:**

- VOI definition (shape, size, anchor landmark; defect VOI from trephine size or day-0 scan)
- Filter (Gaussian sigma/support), segmentation (global/local/adaptive/ML, thresholds with units), surface erosion for TMD
- Software and version (CTAn, IPL, BoneJ [R9], OsteoQuant)

**Study context:**

- Species, strain, sex, age, defect model and size, graft material (product, lot, granule size, composition), timepoint, and fixation status (formalin/ethanol)

### 6.3 Automated QC checks (implementation targets)

| Check | Method | Fail action |
|---|---|---|
| Calibration validity | Phantom fit residuals; rods within ±2% [ASSUMPTION]; phantom scanned at the same kVp/filter/medium | Downgrade to Q1 |
| Histogram sanity | Air/medium and soft-tissue peaks at expected μ; bone peak present | Flag |
| Beam-hardening / cupping | Radial profile of a uniform region (medium or phantom rod); > 5% centre–edge deviation [ASSUMPTION] | Flag; recommend filtration |
| Ring artifacts | Polar transform + azimuthal-uniformity detector | Flag; ring map overlay |
| Motion | Projection consistency, or edge-sharpness drop between halves of the scan | Flag |
| Resolution adequacy | Voxel (and, if available, MTF10) vs expected Tb.Th; require ≥ 3–4 voxels per structure [RF: R7] | Disable thickness/connectivity outputs; keep volume outputs with a warning |
| Metal present | Values > 3× the cortical TMD region + streak detector | Apply an exclusion band; flag |
| Slice-wise consistency | Slice histogram correlation with the volume histogram (cf. Stalder's 94–98% correlation [RF: R30]) | Flag outlier slices |

### 6.4 Phantom generator requirements derived from this physics

1. Generate the **true label + density map first**. Then:
   - forward project with a polychromatic spectrum (or at least apply a beam-hardening model)
   - add Poisson noise in projection space
   - reconstruct (FDK)
   - or apply a PSF blur + correlated noise as a cheap surrogate [ASSUMPTION].
2. Express material densities in **mg HA/cm³ equivalent at a declared spectrum**. Store the energy dependence for non-CaP materials (§3.3 table) so the generator can produce kVp-dependent contrast.
3. Model **sub-voxel micro-porosity** as a solid-fraction multiplier on dense-material density, and **macro-porosity** as resolved geometry.
4. Model **PSF FWHM of 1.5–3 voxels** for desktop systems. The SR reference was about 2 pixels at 10% MTF [RF: R30]; the desktop value is an [ASSUMPTION].
5. Include **scanner "personalities"**: grey-value scaling, BH correction strength, ring artifacts, and smoothing, to train harmonization (motivated by R26).
