# OsteoQuant Scientific and Statistical Review

Scope:
- Library: `osteoquant/` (io, phantom, segment, morphometry, stats, uncertainty, longitudinal, roi, qc, report).
- Experiment scripts: `experiments/`.
- Stored results: `experiments/results/*.json`.
- Claims ledger: `SCIENTIFIC_EVIDENCE.md`.

Review date 2026-11-27. Reproductions were benign local checks (script `/tmp/claude-0/-home-user/b184cf39-87b0-5bba-b79b-9f478d2dc224/scratchpad/review/poc_integrity.py` plus inline checks quoted below). No file was modified.

Severity scale (impact on validity of reported results): critical, high, medium, low, info.

---

## Findings

### Q-01 — The "intensity-only Bayes bound" is not a bound for Dice, and claim R3 rests on it (high)
- **Location:** `experiments/exp_C_separability.py:50-65` (`bayes_bound`), used in `exp_C2_ablation.py:37`, `exp_L_longitudinal.py:78`, `exp_L2_strutlike.py:130`; claim `SCIENTIFIC_EVIDENCE.md` R3.
- **Description:**
  - The function builds the MAP rule `h2 > h1` on 128 histogram bins, which maximises **accuracy** with the test volume's own class priors. It then reports that rule's graft and new-bone Dice as the "bound".
  - The accuracy-optimal rule is not Dice-optimal. Under class imbalance it predicts the majority class almost everywhere, so its graft Dice can be near zero while other intensity-only rules achieve much more.
  - Further problems:
    - The bound is resubstitution (fitted on the evaluated voxels).
    - The histogram range drops the 1% extreme voxels from the accuracy denominator (`np.histogram` discards out-of-range values, `:53-56`), while the Dice part uses all voxels via clipping (`:58-60`).
    - The bound solves a 2-class problem, while the compared methods are scored on 4-class predictions.
- **Evidence (`experiments/results/exp_C2_ablation.json`, strut-like):**
  - The "bound" has accuracy 0.850 but graft Dice 0.0016.
  - An RF using only the raw voxel intensity (`features: raw`) reaches graft Dice 0.246.
  - An intensity-only classifier therefore exceeds the "bound" by about 150×.
- **Impact:** the statement "intensity-only Bayes bound for graft Dice falls to 0.30–0.63; context RF ≈0.88–0.91" overstates what context adds.
- **Fix:**
  - Compare *accuracy* to the accuracy bound only.
  - For Dice, report the maximum over thresholds or likelihood-ratio cut-offs (the Dice-optimal intensity rule), estimated on held-out phantoms.
  - Include all voxels.

### Q-02 — RF "spatial" feature and U-Net context channel encode the simulator's ground-truth geometry (high)
- **Location:**
  - `osteoquant/segment/classical.py:232-236` (`dist_to_roi_boundary_um` from the **true** ROI);
  - `osteoquant/ml/train.py:67-72` (`roi_distance_channel`);
  - generator `osteoquant/phantom/generator.py` lines 141-142, 193, 217-232 (graft packed only in `inner_def`, new bone grows inward from host surfaces with BV/TV decaying with distance, resorption greater near host);
  - experiments A, B, C, C2, J, L.
- **Description:**
  - In the phantoms, the defect boundary *is* the ROI. Class membership is a deterministic function of distance to that boundary, plus noise: host only outside, new bone near the walls, graft deep inside.
  - Giving the true ROI's distance map to the RF (`feature_set="full"`) or U-Net (`unet_ctx`) hands the model the generator's spatial prior. On real defects, the boundary is estimated (Exp F) and in-growth patterns differ.
  - C2 shows this feature alone adds about 7.5 accuracy points (`full` 0.908 vs `no_spatial` 0.833, compact).
  - Experiment A gives the *true* ROI to all methods, so results are conditional on oracle ROI, not on the auto-ROI used in the product.
- **Fix:**
  - Report all synthetic headline numbers with the detected ROI (Exp F detector), plus the oracle-ROI numbers as an upper bound.
  - Report RF `no_spatial` as the primary RF.
  - Add phantoms whose healing pattern is not centripetal (e.g., periosteal or diffuse ossification) to test reliance on the prior.

### Q-03 — Classical-vs-learned comparison is unfair to the RF baseline (high)
- **Location:** `experiments/exp_A_baselines.py:28`; `experiments/exp_B_unet.py:55-61`; `experiments/exp_J_adaptation.py:156-158`; `experiments/exp_H_I_real.py:63` vs `:73`.
- **Description:**
  - Exp A trains the RF on `load_split("train")[:6]`. Because files sort by index and material is `(i//3)%4`, these six cases are **beta-TCP and BCP only**. HA and CaSO4 (6 of the 16 test cases) are therefore out-of-distribution for the RF.
  - The U-Net (Exp B) is trained on all 48 cases of all four materials.
  - Exp J compares a U-Net fine-tuned from 48-case pre-training with an RF "from scratch" on k cases.
  - Exp H trains the RF on 3 real specimens and the U-Net on 10.
  - Any "U-Net beats classical/RF" conclusion is confounded by training-set size and material coverage.
- **Fix:** train the RF on the same 48 cases (subsample voxels to fit CPU), or at least a material-stratified subset. In J, also give the RF the 48 synthetic cases plus k.

### Q-04 — `mean_dice_roi` mixes 2- and 3-class means with a structurally zero host class (medium)
- **Location:** `osteoquant/segment/metrics.py:87-88`; `experiments/exp_A_baselines.py:208-212`; `osteoquant/segment/classical.py:53-58`.
- **Description:**
  - Exp A evaluates classes (1, 2, 3) inside the ROI.
  - `compose_three_class` can never label host inside the ROI. Truth contains a few partial-volume host voxels at the ROI boundary, so host Dice is 0 for every method in most cases, and NaN (excluded) in others.
  - `mean_dice` therefore averages 3 values in some specimens and 2 in others.
- **Evidence (`exp_A_baselines.json`):** host Dice in ROI is `[0, 0, nan, 0, 0, nan]` for all methods. For random forest, `mean_dice_roi` is 0.624 while the new/graft mean is 0.813, and similar for others.
- **Fix:** evaluate only classes 1 and 2 inside the ROI (as Exp B does). Report host Dice over the whole volume separately, and never average over a varying class set.

### Q-05 — Pseudoreplication possible in report statistics (medium)
- **Location:** `osteoquant/report/defectfill.py:60-91`; `osteoquant/api/bundle.py:42-77`; `osteoquant/study/db.py:396-402`.
- **Description:**
  - Groups are formed from **scans** (latest measurement per scan), not specimens.
  - A specimen scanned twice at one timepoint (a rescan after a QC failure, or two uploads) contributes n=2.
  - Scans without a specimen are pooled under group "—".
  - `check_pseudoreplication` exists (`stats/core.py`) but is never called.
  - The module docstring and the PDF ("Statistics are computed per group at the specimen level") are therefore not guaranteed.
- **Reproduction (check 5):** two rows with `specimen_id="R1"`, same group and timepoint, give `n: 2`.
- **Fix:**
  - Aggregate to one value per specimen × timepoint (e.g., the most recent approved scan) before `describe` and `compare_two_groups`.
  - Run `check_pseudoreplication` and refuse statistics on failure.
  - Exclude unassigned scans from group statistics.

### Q-06 — Abstention biases new-bone and graft volumes, differentially by material (medium)
- **Location:** `osteoquant/pipeline.py:129-138`; `osteoquant/morphometry/core.py:159-171`.
- **Description:**
  - Voxels below `abstain_tau` become 255. They are counted in TV but removed from new-bone and graft volumes, so BV/TV is biased **downward** by roughly the abstained fraction.
  - Uncertainty concentrates at material interfaces and in the overlap regime, so the bias differs between graft materials and groups. That biases group comparisons, not just absolute values.
  - Classical methods never abstain, so absolute values are not comparable across methods.
- **Fix:**
  - Report argmax (non-abstained) volumes as the endpoint.
  - Report the abstained volume as an uncertainty interval: lower bound excludes, upper bound includes the abstained voxels assigned to that class.

### Q-07 — "Projected defect coverage" endpoint counts residual graft as healing (medium)
- **Location:** `osteoquant/api/bundle.py:18` (endpoint `bridging_all_mineral.projected_coverage`); `osteoquant/morphometry/core.py:189-224, 271`.
- **Description:**
  - `bridging_all_mineral` uses `new | graft | host` mineral. In a graft-filled defect, coverage is about 1 at day 0, before any bone forms.
  - This is a "closure" metric that cannot distinguish healing from implanted material.
  - `bridging_new_bone` is computed but not reported.
- **Fix:** report `bridging_new_bone.projected_coverage` (or both, clearly labelled) and rename the all-mineral one "mineral coverage (bone + graft)".

### Q-08 — Web-app QC loses ingest provenance: missing slices and ingest errors always pass (medium)
- **Location:** `osteoquant/io/readers.py:127` (overwrites `vol.meta["ingest"]` on every read, including the internal zarr re-read); `osteoquant/api/app.py:40-46, 49-55`; `osteoquant/qc/engine.py` QC-D03, D04, D08.
- **Description:**
  - The QC job re-reads the scan from zarr. That replaces the original ingest report with the zarr reader's empty one, and `_load_scan` restores only `spacing_um` and `metadata_assumed`.
  - QC-D03 ("Missing slices", a **fail** check) and QC-D04 (ingest errors) therefore always pass.
  - QC-D08 metadata completeness loses vendor-log fields (kV, filter, …).
  - Separately, `read_tiff_stack` stacks slices contiguously when indices are missing, so z-geometry is compressed. Missing slices are only warned about at upload.
- **Evidence:** writing a zarr with `missing_slices=[3,4]` and `errors=["bad slice"]` and re-reading gives `{'missing_slices': [], 'errors': [], 'metadata_found': {'spacing_um': [...]}}`.
- **Fix:**
  - Keep the original ingest report under a separate key (e.g., `meta["ingest_original"]`) and have QC and `_load_scan` use the stored `scans.meta`.
  - Make missing slices an ingest error, or insert NaN slices so geometry is preserved.

### Q-09 — Corrected segmentations are measured against a different ROI and endpoint set (medium)
- **Location:** `osteoquant/api/app.py:466-469`; `app.py:81`; `bundle.py:60`.
- **Description:**
  - Edits are re-measured with `labels/roi_current` (the latest ROI written by *any* later analysis) but recorded with `roi_id = base["roi_id"]`. If the ROI changed after the base analysis, TV and fractions come from an ROI that differs from the one recorded.
  - The measurement uses `thickness=False` and drops uncertainty, so reports mix specimens with and without architecture metrics.
  - The report figure also uses `roi_current`, not the measurement's ROI.
  - A later automatic re-run silently supersedes an approved correction as the "latest measurement" (`db.py:398-399`).
- **Fix:**
  - Rasterise the recorded ROI definition (`rois.definition`) for each measurement and version the ROI mask layer.
  - Compute the same endpoint set for corrected versions.
  - Select measurements by "latest approved" rather than "latest".

### Q-10 — Thickness "edge" border convention: claim broader than behaviour, and tuned on the comparison set (medium)
- **Location:** `osteoquant/morphometry/core.py:16-19, 55-73, 120-139`; `experiments/exp_G_morphometry.py:73-75`; claim R1.
- **Description:**
  - "Edge" padding replicates only the **array** border. In the product, the VOI is a cylinder inside the array, so trabeculae and marrow spaces are still truncated at the ROI surface ("background" behaviour).
  - Tb.Sp is computed on `tv_mask & ~bone`, so the ROI wall acts as a boundary and Tb.Sp is under-estimated near it.
  - The docstring states that structures "cut by a cropped VOI are not artificially thinned", which holds only for box VOIs flush with the array.
  - The convention (and `border_pad=24`) was chosen after observing the gap on the same 8 Zenodo cubes used to report ICC 0.983 / 0.948. This is selection on the evaluation set, with n=8. ICC is inflated by between-sample range, so Bland–Altman bias and limits should be the headline.
  - The analytic verification (Part 1) uses `border="background"`, so the production default is not verified analytically.
- **Fix:**
  - Implement VOI-aware handling: compute thickness on the uncropped segmentation, then average within the VOI.
  - Pre-register the convention and validate on an independent reference set.
  - Verify "edge" on analytic objects.

### Q-11 — Experiment L/L2: longitudinal design makes day-0 propagation near-optimal by construction (medium)
- **Location:** `experiments/exp_L_longitudinal.py:32-34, 62-69`; `exp_L2_strutlike.py:114-126`; `osteoquant/longitudinal/core.py:115-125`; claim R4.
- **Description:**
  - Day-0 and later phantoms share the identical seed: same host anatomy and the same granules, which are only eroded in place. The simulated motion is exactly rigid and inside the transform family being estimated.
  - So `later_mineral ∩ day0_footprint = graft` holds by construction, except for creeping substitution. There is no swelling, settling, fragment migration, non-rigid deformation or host remodelling.
  - The registration TRE "<4 µm" at 40 µm voxels reflects identical structure, not in-vivo conditions.
  - The single-timepoint RF comparator is trained on one specimen.
- **Fix:** add non-rigid deformation, granule displacement and fragmentation, host remodelling, and different scan sessions (gain or offset). State R4 as "upper bound under rigid, in-place resorption".

### Q-12 — Experiments K/M: claims not implemented or evaluated in-sample (medium)
- **Location:** `experiments/exp_K_M_uncertainty.py:1-14, 35, 62-67, 77-79`; `osteoquant/uncertainty/core.py:192-224`.
- **Description:**
  - The docstring promises ECE "before/after temperature scaling". `T` is fitted (on non-TTA log-probabilities) but never applied, so no after-scaling ECE exists.
  - `risk_coverage` is called with the whole ROI. Its docstring says "evaluated … on mineral voxels", and easy soft-tissue voxels inflate selective accuracy and AURC.
  - The failure-flag threshold is the 90th percentile of the *same* in-distribution test set used to estimate specificity, so it is in-sample.
  - The effort model constants are assumptions (stated), but `modelled_time_reduction` is emitted as a bare number that is easily quoted as a finding.
- **Fix:**
  - Apply `T` and recompute ECE.
  - Pass `roi & (labels > 0)`.
  - Choose thresholds on validation data.
  - Drop or clearly qualify the time-reduction scalar.

### Q-13 — Exported mesh is mirrored (axis order z,y,x written as x,y,z) (medium)
- **Location:** `osteoquant/api/app.py:396-398`; `web/static/viewer.js:239`.
- **Description:** `marching_cubes` on a (z,y,x) array returns vertices in (z,y,x) order, and the viewer writes them as OBJ `v x y z`. Swapping two axes is a reflection, so exported and rendered surfaces have reversed chirality, and left and right limbs appear swapped.
- **Evidence:** a box of extent (z=16, y=6, x=2) gives vertex extents `[16, 6, 2]` per column. The first column is z.
- **Fix:** return `v[:, ::-1]` (x,y,z) from the API and document the units and handedness.

### Q-14 — DICOM z-spacing falls back to InstanceNumber difference (low–medium)
- **Location:** `osteoquant/io/readers.py:322-346`.
- **Description:**
  - When `ImagePositionPatient` is absent, `pos()` returns `InstanceNumber`. The median difference (1) is then used as z-spacing **in mm** (so 1000 µm) instead of `SpacingBetweenSlices`/`SliceThickness`, and it is recorded as `metadata_found`, so QC-D01 passes.
  - Multi-frame files use `SliceThickness` as spacing (`:316`), which is not the same as slice spacing.
- **Fix:**
  - Use `SpacingBetweenSlices`, then `SliceThickness`, and mark the result as assumed.
  - For enhanced multi-frame files, use `PerFrameFunctionalGroups` positions.

### Q-15 — Reader and geometry details that can silently mis-scale (low)
- **Location:** `osteoquant/io/readers.py`, `osteoquant/roi/engine.py`.
- **Reader issues (`readers.py`):**
  - OME units outside the small map (e.g., `cm`, or Greek `μm` U+03BC) default to a scale of 1.0 without warning (`:146-151`).
  - ImageJ TIFF ignores YResolution and assumes y = x (`:169`).
  - NRRD treats any non-µm unit string as mm (`:422-424`).
  - NIfTI and NRRD direction cosines are ignored (`Volume.direction` is always identity), so oblique or flipped acquisitions are stored un-reoriented.
  - The DICOM writer truncates rather than rounds when quantising (`writers.py:134`).
  - Exp P round-trip checks verify voxels but not spacing.
- **ROI issues (`roi/engine.py`):**
  - `detect_segmental_gap` radius uses `sqrt(area_px/π)·mean(spacing)`, which is wrong for anisotropic in-plane voxels (`:374`).
  - `detect_plate_defect` ignores `vol.origin` while `to_mask` applies it (`pipeline.py:52-54` vs `:47`). This is latent while readers set origin to 0.
  - The condyle ROI depth defaults to 85% of the remaining volume (`:306`), an arbitrary choice that sets TV, and therefore every fraction.
  - Kåsa fit on inner-edge pixels under-estimates the radius by about 0.5 voxel.
- **Fix:**
  - Warn on unknown units.
  - Carry and apply direction matrices.
  - Make ROI depth an explicit, required parameter, or detect it.
  - Add spacing to the round-trip tests.

### Q-16 — Statistics details (low)
- **Location:** `osteoquant/stats/core.py`.
- **Description:**
  - The `icc()` result carries `"note": "Koo & Li 2016 interpretation applied to the CI, not just the point estimate"`, but `interpretation_koo_li` is computed from the point estimate only (≈ lines 166-169).
  - `compare_two_groups` returns both Welch and Mann–Whitney p-values. Only Welch is Holm-adjusted, and choosing between them post hoc is a forking path. Pre-specify one.
  - Mixed-model p-values are Wald with REML and no small-sample (Kenward–Roger / Satterthwaite) correction, and are anti-conservative at n≈5–10 per group.
  - `bland_altman(log=True)` does not back-transform to ratio limits.
  - `lins_ccc` uses n−1 moments (Lin 1989 uses 1/n). This is a minor numerical difference and should be documented.
- **Checked and correct:**
  - ICC(1,1), (2,1), (2,k), (3,1), (3,k) point estimates and McGraw–Wong/Shrout–Fleiss CIs;
  - Hedges g with J correction;
  - Holm and BH adjustment;
  - repeatability coefficient 2.77·Sw;
  - Walter (1998) ICC sample size.

### Q-17 — Synthetic results could be read as real-world validation (low)
- **Location:**
  - app reports: `bundle.py:78-80` (data class forced to "customer" for app studies; the synthetic banner appears only when the model provenance string contains "synthetic");
  - `SCIENTIFIC_EVIDENCE.md` R5–R8 (Dice to 3 decimals with no CI, n=16, single seed, same generator for train and test);
  - `make_synthetic_dataset.py` (val split lacks CaSO4).
- **Description:**
  - Splits are by specimen with disjoint seed ranges (1000–1047 / 2000–2007 / 3000–3015 / 4000–4039), so there is no leakage across splits.
  - However, train, val and test come from one generator with the same three geometries and parameter ranges, so results measure interpolation within the simulator.
  - A user who analyses phantom scans uploaded through the app gets a "CUSTOMER DATA — confidential" banner with no synthetic warning when classical segmentation is used.
- **Fix:**
  - Let studies carry `data_class` through the API.
  - Report CIs and multiple training seeds.
  - Add a cross-generator test (different healing model or texture).

### Q-18 — Minor experiment inconsistencies (info)
- `exp_C_separability.py` docstring says it renders at 20 µm and degrades ×1/2/3. Phantoms are generated at `voxel_um=VOX*2=40`, so Experiment D covers 40/80/120 µm.
- Exp A `adaptive` baseline defines graft as the top 8% of ROI intensities (`exp_A_baselines.py`, the `adaptive` lambda), which is a strawman rather than a realistic workflow.
- Exp H I/O assumes NIfTI zooms in mm without checking `xyzt_units` (Exp G `part2`).

---

## Areas checked with no issue found
- **Dice, IoU, precision and recall, HD95** (max of directed 95th percentiles) and **ASSD** in `segment/metrics.py`. Anisotropic spacing is passed to the EDT. Empty-set handling returns NaN, and abstained voxels are excluded consistently with coverage reported.
- **ECE:** standard top-label binning. Note: if a truth volume contains 255 (ignore), the caller must mask it. Current callers use phantom labels 0–3, so this is not triggered.
- **Volume units:** µm³ × 1e-9 → mm³ throughout (`volume_mm3`, `class_volume_change`).
- **Surface area:** marching cubes with spacing, then mm². Euler/Conn.D uses paired 26/6 connectivity, and β1 = β0 + β2 − χ is correct (lack of edge correction is documented).
- **Writer/reader axis conventions:**
  - NIfTI: transpose to (x,y,z) with reversed spacing, and back.
  - NRRD: C order, `space directions` per file axis, reversed on read.
  - DICOM: PixelSpacing = [row = y, col = x].
  - SimpleITK `to_sitk`: spacing reversed to (x,y,z) and converted to mm.
  - TRE composition direction and point ordering in `exp_L` (`[:, ::-1] * 0.04` mm).
- **Phantom ROI coordinate conversion** from high-res to output-grid convention (`generator.py:320-325`) is consistent with the ROI rasteriser (`voxel j centre at j·spacing`) and the plate detector.
- **Density:** `density_stats` reports "uncalibrated grey value" unless a calibration record exists. The one subtlety is that it reports `vol.data` raw even when the record exists. This is consistent only because `apply_calibration` (`io/transforms.py:80-84`) converts the data at the same time. Keep the two coupled.
- **Train/val/test leakage:** none by seed or specimen. Exp J pool and test sets are disjoint (`ood[:24]` / `ood[24:40]`). Exp H uses the dataset's official split.

## Summary (≤300 words)
Eighteen scientific findings.

**High (3)**
- Q-01: the "intensity-only Bayes bound" is the accuracy-optimal rule's Dice, not a Dice bound. Stored C2 results show an intensity-only RF beating it (0.246 vs 0.0016 graft Dice), which undermines claim R3.
- Q-02: the RF distance feature and U-Net context channel are computed from the *true* ROI, whose geometry deterministically encodes the simulator's centripetal healing prior. All headline synthetic results use the oracle ROI.
- Q-03: the RF baseline was trained on 6 cases covering only beta-TCP and BCP, versus 48 cases of all materials for the U-Net. Exp J and H have similar training-data asymmetry.

**Medium (10)**
- Q-04: `mean_dice_roi` averages a structurally zero host class over a varying number of classes.
- Q-05: report statistics count scans, not specimens (pseudoreplication reproduced).
- Q-06: abstention biases BV/TV downward, and differently by material.
- Q-07: the "projected coverage" endpoint counts graft as closure.
- Q-08: web QC loses missing-slice and ingest-error provenance (reproduced).
- Q-09: corrected segmentations are re-measured with a different ROI and endpoint set.
- Q-10: the "edge" border claim does not hold for cylindrical VOIs, and the convention was tuned on the reported comparison set.
- Q-11: the longitudinal experiment makes day-0 propagation near-optimal by construction.
- Q-12: K/M temperature scaling is never applied, and thresholds and metrics are in-sample or on the wrong voxel set.
- Q-13: the exported mesh is mirrored (reproduced axis order).

**Low (4)**
- Q-14: DICOM z-spacing fallback (rated low–medium).
- Q-15: reader unit and orientation gaps, plus ROI heuristics.
- Q-16: ICC interpretation note mismatch, Welch versus Mann–Whitney forking path, small-sample mixed-model p-values.
- Q-17: synthetic results and app reports that could be misread as real validation.

**Info (1)**
- Q-18: docstring and voxel-size inconsistencies.

**Checked and correct:** core metric formulas, ICC, Hedges g, multiplicity adjustment, unit conversions, writer and reader axis order, and split hygiene.
