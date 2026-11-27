# Protocol P1: First Physical Micro-CT Phantom for Bone vs Graft Separation and Morphometry Accuracy

| Field | Value |
|---|---|
| Protocol ID | OQ-P1 |
| Version | v0.1 DRAFT, 2026-11-27 |
| Status | **Not approved. Not started.** Requires sign-off by a qualified imaging scientist or lab supervisor on every item in `DECISIONS_FOR_IMAGING_SCIENTIST.md`, and written answers from OTM and the facility (see `../outreach/IP_AND_OTM_QUESTIONS.md`). |
| Instrument (planned) | ZEISS Xradia Versa 630, Beckman Institute Microscopy Suite, UIUC (see `BECKMAN_ACCESS.md`) |
| Related | Synthetic-phantom Experiments B/C (OsteoQuant). This is the first **physical** test. |

**Evidence labels:** [V] verified today on an official page or PubMed/Crossref; [CC] cross-checked; [RF] single secondary source or standard textbook value; [INF] inference; [HYP] hypothesis; [UNR] unresolved.

---

## 0. Plain-language summary

The plan is to drill small holes ("defects") in butcher-sourced bovine bone cores and scan each core empty. The holes are then filled with **weighed** amounts of commercial bone-graft granules (HA, β-TCP, BCP, 45S5 bioactive glass, calcium sulfate) or with bone chips, and each core is scanned again at 10, 20 and 40 µm. Because we know exactly what went where and how much, we can check whether OsteoQuant (a) tells graft apart from bone and (b) measures volumes and BV/TV correctly. Repeat scans measure precision, and an HA phantom calibrates gray values.

**What this experiment cannot show:** biological *new* bone does not exist in an ex vivo phantom. Bone chips, and optionally partially demineralized chips, are only **surrogates**. Success here is necessary but **not sufficient** for claims about real preclinical graft studies. Any use of the results must say so.

---

## 1. Aims and hypotheses

### Aims
- **A1. Separability.** Quantify how well graft material, host bone and void/soft content are distinguished, per material and per voxel size.
- **A2. Accuracy.** Quantify bias and limits of agreement of OsteoQuant's graft volume, bone-chip volume and peri-defect host BV/TV against truth by construction.
- **A3. Precision.** Quantify scan–rescan repeatability after physical repositioning.
- **A4. Calibration.** Establish the gray value → mg HA/cm³ mapping and its session-to-session drift on this instrument and protocol.
- **A5. Failure modes.** Identify which materials, granule sizes and voxel sizes make OsteoQuant output "indeterminate" or wrong. The pipeline should *flag* rather than mislabel.

### Hypotheses (all [HYP]; thresholds to be fixed by the imaging scientist before unblinding, decision D10)

- **H1. Dense ceramics are separable at 10–20 µm.** Dense sintered calcium-phosphate granules (HA, β-TCP, BCP) and calcium sulfate are separable from host bone tissue at 10–20 µm voxels, because their attenuation exceeds that of bone tissue. Separability degrades at 40 µm through partial-volume averaging at granule and trabecular edges.
  - Rationale [RF]: theoretical skeletal densities are about 3.16 g/cm³ (HA), 3.07 (β-TCP), 2.32 (CaSO4·2H2O) and 2.7 (45S5 glass). Bone tissue is a lower-density mineral–collagen composite.
  - Rationale [INF]: microporous granules will have lower apparent attenuation, and that may close the gap.
- **H2. 45S5 glass overlaps more.** 45S5 glass has lower effective atomic number and density than CaP ceramics, so its intensity overlaps more with bone. Lower separability than HA/β-TCP is expected.
- **H3. Bone chips are not intensity-separable.** Bone chips (autograft surrogate) are not separable from host bone by intensity. Only spatial context (the defect ROI) separates them. The correct behaviour is to label them "bone-in-defect", not host bone, and never graft.
- **H4. Accuracy.** At 20 µm, defect graft volume agrees with the reference-calibrated truth within a pre-specified bias and LoA. Peri-defect host BV/TV after filling equals pre-fill BV/TV within a pre-specified tolerance, i.e. no "graft bleed" into host.
- **H5. Precision.** Scan–rescan ICC(2,1) (absolute agreement) is at or above a pre-specified value (e.g. 0.90) for defect graft volume and peri-defect BV/TV.

---

## 2. Design overview

### 2.1 Factors

| Factor | Levels (Tier B full) | Tier A minimal |
|---|---|---|
| Fill condition | HA, β-TCP, BCP, 45S5, CaSO4, Bone chips (BC), EMPTY. Optional: partially demineralized BC (pdBC, a woven-bone surrogate [HYP]) | Same 7 conditions, fewer replicates |
| Defect geometry | Ø6 mm × 8 mm deep (≈226 mm³); Ø4 mm × 8 mm deep (≈100 mm³) | Same |
| Voxel size | 40, 20, 10 µm (10 µm on a subset) | Same, smaller 10 µm subset |
| Host | Bovine distal-femoral trabecular cores (primary). Sawbones laminated PU foam (registration/geometry control only). | Same |
| Repeats | 6 cores repositioned and rescanned at 20 µm. 1 core scanned on 3 separate days. | 4 cores repositioned |

### 2.2 Specimens

**Core geometry.** Each **host core** is about Ø25 mm × 15 mm, cut from a distal femoral condyle slab. It carries **4 blind defects** at 90° spacing on a 6.5 mm radius:
- D1 and D3: Ø6 mm, opposite each other
- D2 and D4: Ø4 mm, opposite each other
- Depth: 8 mm

[INF] The minimum bone bridge is about 4.2 mm between Ø6 and Ø4 defects, and the wall is about 3 mm.

**Main cores (Tier B):** 12 cores = 48 defects, assigned as follows:
- 6 filled conditions × 7 defects = 42
- EMPTY × 6
- The assignment is **balanced by geometry** and randomized within bone-of-origin blocks (§6).

**Layered cores:** 2 cores (8 defects). Each defect contains:
- bottom 4 mm: graft X (HA, β-TCP, BCP or 45S5)
- a PTFE film or filter-paper spacer disc
- top 4 mm: bone chips

The spacer gives a **known spatial boundary** between graft and bone-in-defect.

**Pure-material references:** 6 tubes (one each of HA, β-TCP, BCP, 45S5, CaSO4 and bone chips). Each is a weighed mass in a 15 mL tube, packed to a known height. These provide per-material intensity distributions and the "segmented volume per gram" calibration.

**Calibration:** HA phantom (decision D4), scanned at each voxel size and kV setting, plus a short QC scan in each session.

**Foam controls:** 2 Sawbones 1522-440 blocks (20 PCF with a 50 PCF laminate as a "cortical shell"), each with 4 defects. These test registration and geometry only. [INF] Polyurethane foam is **not** a bone radiodensity surrogate.

**Tier A:**
- 8 main cores = 32 defects (6 conditions × 5 = 30, plus 2 EMPTY)
- 1 layered core
- 6 references
- 1 foam block

### 2.3 Scan schedule and time estimate

Times are estimates [INF]; Phase 0 measures the real ones. Per-scan times include mounting and warm-up.

| Scan set | Objects (Tier B) | Voxel | Est. h/scan | Tier B h | Tier A h |
|---|---|---|---|---|---|
| Phase 0 pilot (settings, phantom, 1 practice core at all voxel sizes) | 1 core + phantom | 40/20/10 | n/a | 6–8 | 4–8 |
| Pre-fill (empty defects) | 14 cores + 2 foam | 20 µm | 1.25 | 20 | 10 |
| Post-fill | same | 20 µm | 1.25 | 20 | 10 |
| Post-fill | same | 40 µm | 0.5 | 8 | 4 |
| Post-fill ROI (one Ø6 defect per core) | 6 cores | 10 µm | 3 | 18 | 6–9 |
| Repositioned repeat | 6 cores | 20 µm | 1.25 | 7.5 | 5 |
| Pure-material references | 6 tubes (+2 at 10 µm) | 20 (+10) | 1 (3) | 12 | 6 |
| Calibration phantom (full + per-session QC) | n/a | all | n/a | 5 | 4 |
| **Total** | n/a | n/a | n/a | **≈97** | **≈50** |

---

## 3. Ground truth: independent of OsteoQuant

Truth is established by **four independent routes**. Discordance between them is itself a finding.

**T1. Gravimetric.** Weigh the graft mass *m* placed in each defect (by difference: boat before and after transfer).
- Solid-graft truth volume: V_skel = m / ρ_skel.
- Take ρ_skel from the supplier CoA or from helium pycnometry (decision D7). Fall back on textbook values only if neither is available, and flag that [RF].
- Also record the envelope volume where the bulk/tap density is measured.
- [INF] Precision with a 1 mg balance: a Ø6 defect holds roughly 0.2–0.3 g of HA granules at ~55% packing, so ±1 mg is ≲0.5%. A 0.1 mg balance is better but not essential.

**T2. Reference-calibrated volume.** From the pure-material reference scans, compute k_mat,voxel = (segmented volume)/(mass) at each voxel size.
- Truth for a filled defect is V_ref = k × m.
- This absorbs sub-voxel microporosity, which T1 cannot. Report results against **both** T1 and T2.

**T3. Registration (pre-fill vs post-fill).**
- Rigidly register the post-fill scan to the pre-fill scan using host bone *outside* the defect ROI (mutual-information metric; the implementation is the imaging scientist's choice, e.g. elastix or SimpleITK).
- Host-bone truth is the pre-fill bone mask. Defect ROI truth is the pre-fill void cylinder.
- "Added material" is the mineral present post-fill inside the defect ROI and absent pre-fill.
- Report the target registration error (TRE) using 3 notches cut in the core side wall. **No metal fiducials**, to avoid streak artifacts.

**T4. Segregated placement.**
- Single-material defects: everything added is that material.
- Layered defects: the spacer plane gives the boundary between graft and bone chips.
- Reference tubes: pure material.

**"New bone" surrogates.** Bone chips are milled from the same donor bone, sieved to 0.5–2 mm, and weighed. **Optional pdBC:** chips partially demineralized under a controlled, documented protocol (decision D11) to emulate lower-mineral woven bone [HYP]. pdBC truth mineral content comes from paired ash or mass-loss measurement on sister chips (decision D11).

**Displacement check.** After filling, cap the defect (§5.6) and do a quick 40 µm scan. Compare it with the final post-fill scan. Granule movement greater than 2 voxels at 40 µm is recorded and the defect is excluded from accuracy analysis (pre-specified).

---

## 4. Calibration

1. **HA phantom.** Scan the HA rods (e.g. Bruker 0.3 and 1.25 g/cm³ CaHA, or the facility's own; decision D4):
   - at every voxel size, kV and filter combination used, and
   - for a short QC scan in each session.
   Fit linear gray-value → mg HA/cm³ per setting. Record the fit coefficients, R², and residuals.
2. **Do not change** kV, filter or exposure **within** a scan set. Calibration is specific to each setting.
3. **Beam hardening.** Use the facility's standard beam-hardening correction. Record the constant, and keep it identical across all scans of a set. Measure cupping on the phantom (radial profile).
4. **Drift QC.** Session-to-session drift in the phantom mean must be ≤ a pre-set % (decision D10). If it is exceeded, rescan or apply a recorded correction.
5. **Report TMD and BMD in mg HA/cm³** only for bone. For graft, report calibrated gray values but **not** "HA-equivalent density" as if it were a true density. [INF] The material composition differs, so HA-equivalence is an approximation for non-HA materials.
6. If a DIY K2HPO4 solution phantom is used instead, treat it as **drift QC only**, not absolute HA calibration, unless it has been cross-calibrated (decision D4).

---

## 5. Specimen preparation (record everything in `worksheets/SPECIMEN_PREP_LOG.md`)

### 5.1 Sourcing and receipt
- Buy 2–3 bovine distal femurs or condyle slabs (food-grade) from a butcher or meat locker. Record source, date, animal age if known, and price.
- **Do not use** bovine vertebral column or skull tissue. Use femur only. [RF] USDA FSIS classifies certain tissues from cattle ≥30 months as specified risk materials.
- Transport in a cooler at 2–8 °C. Log receipt on the chain-of-custody form.
- Freeze at −20 °C in double bags if not processed within 24 h. Log freeze/thaw cycles; the maximum is 2.

### 5.2 Cutting cores
- Have the butcher band-saw ~30 mm slabs through the condyles. This reduces home or shop saw work.
- Core with a Ø~25 mm diamond hole saw in a drill press, with the slab clamped in a vise. Irrigate with water or saline. Never hand-hold the work.
- Trim to 15 mm height. The defect face is the cut face, perpendicular to the core axis.
- Record diameter and height (calipers, 3 readings each) and wet mass.

### 5.3 Defects
- Mark positions with a printed template or a 3D-printed jig. Drill D1–D4 at 8 mm depth with depth-stop collars:
  - Ø6 at positions 1 and 3
  - Ø4 at positions 2 and 4
- Flush debris with water and blow out gently with an air bulb.
- Cut **3 side-wall notches** at unequal angles as registration fiducials and orientation keys.
- Record measured diameter and depth per defect.

### 5.4 Storage and conditioning (decision D6)
- **Default proposal:** store cores in 70% ethanol at 4 °C until the pre-fill scan.
- Before scanning, drain and blot. Then seal the core in a 50 mL tube with ethanol-moistened gauze in the cap (humid, not immersed).
- Use **identical conditioning** for pre-fill and post-fill scans.
- Note [INF]: 45S5 glass and CaSO4 react with or dissolve in water, and 70% ethanol is 30% water. After filling, therefore:
  - keep filled specimens **humid-sealed, not immersed**;
  - scan within 48 h;
  - record elapsed time between filling and scan.

### 5.5 Graft preparation
- **Commercial granules:** record lot number and CoA. Sieve to the target size class and record the fraction retained. Dry at room temperature in a desiccator (or as the supplier directs). Record the drying protocol.
- **CaSO4 granules (DIY):** cast hemihydrate with water at a recorded ratio, cure ≥24 h, dry, crush and sieve to 0.5–2 mm. Record phase as dihydrate (assumed [INF]; confirm with XRD only if available, decision D7).
- **Bone chips:** rongeur or mill cancellous bone from the same donor. Sieve 0.5–2 mm. Blot to a standard dampness and weigh immediately. Record mass and time.

### 5.6 Filling (blinded fill map, §6)
1. Tare the boat, weigh the graft, and transfer it with a funnel. Tamp with the matched PTFE rod: 3 standardized taps, or a fixed weight (decision D8).
2. Re-weigh the boat. **m_placed = m_before − m_after.** Fill to flush with the core face; record any over- or under-fill.
3. Cap all defects with a thin PTFE disc plus Kapton tape so that granules cannot move.
4. Layered defects: graft to 4 mm, spacer disc, then bone chips to flush. Weigh each component separately.
5. Record the time, the fill operator, and environmental humidity if available.

### 5.7 Mounting
- Use a 50 mL polypropylene tube with low-density PE foam for immobilization. Keep the core axis vertical and the defect face up.
- Mark a reference line on the tube and core for repositioning.
- Wrap the tube cap in Parafilm. Use a secondary container for transport.

---

## 6. Randomization and blinding

1. A **custodian** generates the fill map with a seeded randomization script and keeps it sealed. The custodian is not the analyst; this could be an advisor, a lab supervisor or a trusted second person (decision D12).
   - Conditions are balanced by geometry and blocked by donor bone.
   - The custodian records the SHA-256 hash of the fill-map file in the chain-of-custody log *before* any scan.
2. Specimen labels carry only blinded IDs (`worksheets/specimen_labels.csv`).
3. The filler necessarily sees the materials. If possible, the filler should not be the analyst. If the founder must do both (a likely reality), declare that limitation. Mitigate it by **freezing the pipeline version** (commit hash) and all parameters before unblinding.
4. **Pre-registration.** Before unblinding, timestamp the analysis plan, acceptance criteria and frozen pipeline commit (e.g. OSF registration, or an emailed hash to the advisor).
5. **Unblinding** happens only after all OsteoQuant outputs are written and hashed.
6. Note [INF]: materials are partly recognizable by eye (granule shape, brightness). Blinding mainly prevents parameter tuning toward the truth, not recognition.

---

## 7. Scan settings to record for every scan

Record in `worksheets/SCAN_ACQUISITION_LOG.md` and `worksheets/scan_log.csv`:

- **Specimen and session:** scan ID; specimen ID; date and start/end time; operator; session number; condition (pre-fill, post-fill, repeat, reference, phantom).
- **System:** instrument and software versions. ZEISS acquisition and reconstruction software names and versions as displayed [INF: names vary by release, e.g. Scout-and-Scan, Reconstructor].
- **Source:** voltage (kV), power (W), current (µA), filter ID (from the filter wheel).
- **Optics:** objective (flat panel, 0.4X, 4X…), camera binning, pixel size.
- **Geometry:** source–sample and detector–sample distances, geometric magnification. Voxel size (µm), field of view (mm), and number of vertical stitches.
- **Acquisition:** exposure time per projection, number of projections, angular range. Reference (flat-field) acquisition settings, dynamic ring removal on or off, warm-up time.
- **Reconstruction:** algorithm (FDK or iterative), **any AI or deep-learning reconstruction (must be OFF for truth scans unless decision D3 says otherwise)**, beam-hardening constant, center shift, smoothing or kernel, output bit depth and format (.txrm/.txm, TIFF).
- **Environment and sample:** sample conditioning (humid or immersed, time since fill), room temperature if displayed.
- **Data:** file names, file sizes, SHA-256 checksums, storage locations (CTData path and founder drive).
- **Notes:** QC notes (motion, rings, streaks, cupping).

---

## 8. Data collection and management

- **File naming:** `OQ-P1_<SpecimenID>_<SCANTYPE>_<VOXEL>um_R<rep>_<YYYYMMDD>`
  - Example: `OQ-P1_C07_POST_020um_R1_20270115`
- **Raw data:** copy the vendor files (.txrm projections and .txm reconstructions) plus TIFF exports **the same day** to founder-owned drive #1. Verify SHA-256, then copy to drive #2.
  - Leave nothing only on CTData, beyond the facility's retention policy and subject to OTM's answer.
- **Data entry:** every measurement goes into the CSV templates in `worksheets/`. Paper worksheets are the primary record; CSV is transcribed within 24 h and double-checked.
- **Data dictionary:** column definitions are in each CSV header row. Units go in the column names.
- **Versioning:** record the pipeline commit hash with every analysis output, in the audit module record.

---

## 9. Analysis plan (link to the OsteoQuant pipeline)

All parameters are frozen before unblinding. Module names refer to directories under `osteoquant/`.

1. **Ingest** (`osteoquant/io`): read .txm/.txrm or TIFF stacks and capture scan metadata into the audit record (`osteoquant/audit`).
2. **Scan QC** (`osteoquant/qc`): automated checks (§10). Failing scans are flagged, not silently used.
3. **Calibration:** apply the per-setting HA fit (§4) and store the coefficients in the audit record.
4. **ROI** (`osteoquant/roi`): from the pre-fill scan, detect each defect cylinder and build:
   - the defect ROI
   - a **peri-defect host ring** (e.g. 0.5–1.5 mm from the defect wall; decision D10)
   - a remote host region
5. **Registration (truth builder, separate code path from the method under test):** post→pre rigid registration, TRE from notches, truth label maps (T3/T4). Truth code must not share segmentation code with the method under test.
6. **Segmentation under test** (`osteoquant/segment`): OsteoQuant labels host bone / graft (by material if supported) / bone-in-defect / void / indeterminate. Also run baselines:
   - (a) global Otsu threshold
   - (b) a fixed literature-style dual threshold
   - (c) optionally BONe (Lee et al., Front Bioinform 2026, doi:10.3389/fbinf.2025.1677527; license check first)
7. **Morphometry** (`osteoquant/morphometry`): graft volume (mm³) and graft volume fraction in the defect ROI; bone-in-defect volume; host BV/TV, Tb.Th, Tb.Sp and Tb.N in the peri-defect ring; TMD in host bone. Nomenclature follows Bouxsein et al. 2010 (doi:10.1002/jbmr.141) [V].
8. **Uncertainty** (`osteoquant/uncertainty`): per-defect uncertainty intervals as implemented. Assess coverage: the fraction of truths inside the intervals.
9. **Stats** (`osteoquant/stats`): §11.
10. **Report** (`osteoquant/report`): the audited report per specimen, plus the experiment summary. Each report states that this is ex vivo phantom data and not in vivo validation.

---

## 10. QC checks (pass/fail logged in `worksheets/qc_checks.csv`)

| # | Check | Pass criterion (proposal; decision D10 finalizes) |
|---|---|---|
| Q1 | Instrument warm-up and reference images acquired | Per facility SOP |
| Q2 | Motion artifact (projection 0 vs 360° comparison or visual double edges) | None visible; else rescan |
| Q3 | Ring artifacts in the ROI | None affecting the defect ROI |
| Q4 | Beam-hardening cupping on phantom (center vs edge) | ≤ X % |
| Q5 | HA phantom calibration linearity | R² ≥ 0.99 |
| Q6 | Session drift in phantom mean | ≤ Y % vs session 1 |
| Q7 | Noise (SD in a uniform phantom region) | Recorded; ≤ Z |
| Q8 | Registration TRE (notches) | ≤ 2 voxels at 20 µm |
| Q9 | Granule displacement (quick vs final post-fill) | ≤ 2 voxels at 40 µm |
| Q10 | Defect ROI fully inside FOV | Yes |
| Q11 | Specimen mass before vs after scan (drying) | Change ≤ 1 % |
| Q12 | File checksum verified on both drives | Yes |
| Q13 | Metadata completeness (§7 fields) | 100 % |
| Q14 | Mass balance: Σ placed masses vs inventory decrease | Within balance tolerance |

---

## 11. Statistics

**Units and structure.** The analysis unit is the defect. Defects are nested in cores, and cores are nested in donor bones. Use linear mixed models with random intercepts for core (and bone where there are ≥3 donors). Otherwise treat donor as a fixed block.

### Primary endpoints, at 20 µm, filled defects
1. **Graft volume agreement** vs T2 (also reported vs T1):
   - Bland–Altman: bias, 95% limits of agreement, and approximate 95% CIs (Bland & Altman 1986, doi:10.1016/S0140-6736(86)90837-8 [V]).
   - Check proportional bias by regressing the difference on the mean. If differences scale with size, use percentage or log-ratio differences.
2. **Voxel-wise separability** vs T3/T4 truth labels: per-class Dice, balanced accuracy, and a confusion matrix of graft ↔ host bone ↔ bone-in-defect ↔ void, reported per material.

### Secondary endpoints
- Peri-defect host BV/TV change (post − pre), expected to be 0. Test equivalence (TOST) within the pre-specified margin.
- Voxel-size effect: mixed model error ~ voxel × material + geometry + (1 | core).
- Fraction labelled "indeterminate" by material and voxel size.
- Uncertainty-interval coverage.
- Baseline comparison: OsteoQuant vs Otsu, dual threshold and BONe, using paired differences in absolute error. Use a Wilcoxon signed-rank test, or the mixed model.
- Multiplicity: report primary endpoints as pre-specified; apply Holm correction to secondary tests.

### Precision
- Repositioned scan–rescan **ICC(2,1)**: two-way random effects, absolute agreement, single measurement (Shrout & Fleiss 1979, doi:10.1037/0033-2909.86.2.420; reporting per Koo & Li 2016, doi:10.1016/j.jcm.2016.02.012 [V]). Report the ICC form explicitly.
- Also report the repeatability coefficient (RC = 2.77 × within-subject SD) and RMS-CV%.

### Sample-size reasoning
This is a feasibility study; per-material claims are exploratory.

- **ICC precision** (Bonett 2002, doi:10.1002/sim.1108 [V]), with k = 2 repeats [computed]. The 95% CI width is the total width.

  | Expected ICC | Target CI width | n units needed |
  |---|---|---|
  | 0.90 | 0.20 | 15 |
  | 0.90 | 0.15 | 26 |
  | 0.95 | 0.10 | 16 |

  - Tier B repeats 6 cores × 4 defects = 24 defect units, which is close to n = 26. Clustering within cores reduces the effective n, so the CIs will be wider than nominal [INF].
- **Bland–Altman LoA precision.** The approximate half-width of the 95% CI of each LoA is ≈ 1.96·√(3/n)·SD [computed]:

  | n | Half-width |
  |---|---|
  | 42 (all filled defects, Tier B) | ±0.52 SD |
  | 24 | ±0.69 SD |
  | 7 (per material) | ±1.28 SD |

  Pooled agreement is therefore estimable. **Per-material LoA are imprecise, and per-material claims must be labelled exploratory.**
- **Exclusions** (pre-specified): Q2/Q8/Q9 failures; specimens damaged in handling; mass-balance failures. Report all exclusions with reasons. Report no imputation.

---

## 12. Safety

- **Radiation:** the Versa 630 is an enclosed, interlocked system operated in a facility. Follow facility training and University x-ray safety training. DRS requires annual online X-Ray Safety training for users of radiation-producing machines [RF]; confirm the requirement with the Suite. Never defeat interlocks.
- **Biological tissue:**
  - Treat butcher bone as potentially contaminated with enteric bacteria. Wear nitrile gloves, lab coat and eye protection.
  - Clean surfaces with 10% bleach (fresh) or 70% ethanol. Keep tissue out of food areas. Wash hands.
  - Transport in leak-proof double containment.
  - Ask the Suite whether animal-tissue specimens must be handled in the BL-2 room (B420) [V that the room exists; rule UNR].
- **Sharp tools and drilling:** clamp the work in a vise. Use the drill press guard, safety glasses, tied-back hair and no loose sleeves. **Do not wear cut-resistant or loose gloves near rotating bits** (entanglement risk). Use cut-resistant gloves only for knife or saw work. Wet-cut to limit bone dust. Unplug the drill before changing bits.
- **Powders:** CaP and bioactive-glass fines are respiratory irritants [INF]. Weigh with a draft shield, avoid dry sweeping, and use an N95 if dust is visible.
- **Chemicals:**
  - 70% ethanol is flammable; keep it away from ignition sources.
  - If formalin is chosen (decision D6), formaldehyde is a regulated carcinogen and sensitizer (OSHA 29 CFR 1910.1048 [RF]). It requires a fume hood, training and hazardous-waste handling. **The default is ethanol, to avoid this.**
- **Ergonomics and fatigue:** no drilling while tired. Use a buddy where possible.

## 13. Waste handling

| Waste | Route |
|---|---|
| Bone tissue and bone chips (unfixed or ethanol-stored) | If handled on campus, follow DRS / facility guidance for animal tissue [UNR exact route]. If handled at a non-University location, double-bag, freeze and dispose per local municipal rules for meat waste [INF]. |
| Formalin (if used) | Hazardous chemical waste. On campus, use DRS chemical-waste pickup. Never pour down the drain. |
| Ethanol 70% | Collect. Small quantities per local rules; on campus, use DRS chemical waste. |
| Graft granules (unused, clean) | Retain for future scans (labelled, desiccated). |
| Graft granules (used, tissue-contaminated) | Dispose as tissue waste. |
| Sharps (blades, broken bits) | Sharps container. |
| PU foam and dust | Normal solid waste; vacuum, don't sweep. |

## 14. Institutional approvals and checks

| Item | Proposed status | Evidence / action |
|---|---|---|
| IACUC | **Likely not required.** No live animals; tissue bought post-slaughter from the food chain. | [INF]. Many institutions exempt food-source tissue [RF, e.g. USF IACUC guidance surfaced in search]. **Confirm in writing with the UIUC IACUC/OPA office.** |
| IBC / DRS biosafety registration | **Unresolved.** Non-infectious food-source tissue may not need registration. | [UNR]. Ask DRS (drs@illinois.edu [RF]) and the Suite. |
| Facility registration and training | Required | [V] (`BECKMAN_ACCESS.md` §4) |
| X-ray safety training | Required | [RF] DRS |
| OTM ownership determination / IP | **Required before using University equipment, accounts or storage** | See `../outreach/IP_AND_OTM_QUESTIONS.md` |
| Billing pathway | Required | Faculty CFOP (internal) vs contract (external). Decision D1. |
| Human subjects (IRB) | Not applicable | No human data |

## 15. Decisions an imaging scientist or lab supervisor must make

See `DECISIONS_FOR_IMAGING_SCIENTIST.md` (D1–D14). **The protocol may not start until those are signed.**

## 16. Costs

Itemized in `BILL_OF_MATERIALS.csv`. Prices are from public listings where available; the rest are labelled estimates. Instrument rates are the posted 2021 rates [V].

| Scenario | Materials, tools, consumables | Instrument + training | Total (before 10% contingency) |
|---|---|---|---|
| Phase 0 pilot only (8 scan h + 4 training h) | ~$1,700–2,900 | $441 (internal) – $893 (ext. with F&A) | **≈ $2,100–3,800** |
| **Tier A minimal** (~50 scan h) | $2,703–5,595 | $2,121 (internal) – $4,212 (ext. with F&A) | **≈ $4,800–9,800** |
| **Tier B full** (~97 scan h) | $6,633–11,470 | $4,122 – $8,186 | **≈ $10,800–19,700** |

**Cost drivers:**
1. **Instrument hours.** Measured scan durations from Phase 0 will tighten this.
2. **Billing category.** The difference between internal and external-with-F&A is about 2×.
3. **Bruker HA phantom ($2,296.16 [V]).** It may be unnecessary if the facility has one.
4. **Balance purchase.** $150 for a 1 mg balance (adequate per §3) vs up to $2,500 for a 0.1 mg balance.
5. **β-TCP and BCP granule quotes [UNR].**

Phase 0 tools carry over into Tier A/B; the scenarios are alternatives, not additive.

## 17. Timeline (indicative; the winter break may limit facility and staff availability [INF])

| Week (from go-ahead) | Activity |
|---|---|
| 0–2 | OTM/Landuyt questions; Suite inquiry; advisor identified; decisions D1–D14 drafted |
| 2–4 | Quotes and orders (granule lead times may be weeks [RF]); Suite orientation; DRS x-ray training; Versa training |
| 4 | Tool setup; drilling practice on Sawbones; CaSO4 casting; bone sourcing |
| 5 | **Phase 0 pilot**: 1 core, references, phantom; measure scan times; check settings |
| 6 | Pilot analysis; finalize settings; **pre-register**; custodian generates the fill map |
| 7–9 | Main preparation and scanning in batches of about 4 cores per week (≤8 h blocks per facility policy [V]) |
| 10–11 | Analysis with frozen pipeline; hash outputs; unblind; statistics |
| 12 | Report (with limitations); advisor review; decide on Protocol P2 (in vivo samples or partner data) |

## 18. Known limitations (state these in any report)

1. No biological new bone; surrogates only.
2. Ex vivo bone lacks in vivo soft-tissue and marrow conditions; scanning humid and drained differs from typical in vivo or fixed preclinical samples.
3. Commercial research granules may differ from the clinical products used in preclinical studies.
4. Single instrument; results may not transfer to other scanners or settings without recalibration.
5. The founder may be both filler and analyst, which gives partial blinding (§6).
6. Per-material conclusions are exploratory given n ≈ 5–7 defects per material.

## 19. References (DOIs verified via PubMed/Crossref on 2026-11-27)

- Bouxsein ML, Boyd SK, Christiansen BA, Guldberg RE, Jepsen KJ, Müller R. Guidelines for assessment of bone microstructure in rodents using micro-computed tomography. J Bone Miner Res 2010. doi:10.1002/jbmr.141
- Polak SJ, Candido S, Levengood SK, Johnson AJ. Automated segmentation of micro-CT images of bone formation in calcium phosphate scaffolds. Comput Med Imaging Graph 2012. doi:10.1016/j.compmedimag.2011.07.004
- Kang Y, …, Harley BAC, Xu S, Lee JC. Evaluating Mineral Deposition in Bone-Regenerative Collagen-Based Scaffolds Using High-Resolution microCT and 3D Computational Segmentation. Curr Protoc 2026. doi:10.1002/cpz1.70306
- Lima JR, …, Oliveira GJPL. Effect of different thresholds on the accuracy of linear and volumetric analysis of native- and grafted-bone. Braz Dent J 2022. doi:10.1590/0103-6440202204823
- Lee AH, …, Al-Nakkash L. Deep learning software and revised 2D model to segment bone in micro-CT scans. Front Bioinform 2026. doi:10.3389/fbinf.2025.1677527
- Bland JM, Altman DG. Statistical methods for assessing agreement between two methods of clinical measurement. Lancet 1986. doi:10.1016/S0140-6736(86)90837-8
- Shrout PE, Fleiss JL. Intraclass correlations: uses in assessing rater reliability. Psychol Bull 1979. doi:10.1037/0033-2909.86.2.420
- Koo TK, Li MY. A Guideline of Selecting and Reporting Intraclass Correlation Coefficients for Reliability Research. J Chiropr Med 2016. doi:10.1016/j.jcm.2016.02.012
- Bonett DG. Sample size requirements for estimating intraclass correlations with desired precision. Stat Med 2002. doi:10.1002/sim.1108
