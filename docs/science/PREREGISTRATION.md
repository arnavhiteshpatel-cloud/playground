# Pre-registered Analysis Conventions and Acceptance Criteria (Generation 2)

Registered 2026-11-27, **before** any of the Generation-2 held-out data (dataset discovery round 2, physical phantom
scans, partner data) were analysed. Committed to git; the commit timestamp is the registration record. Changes after
data are seen must be logged below as deviations with justification. Addresses FORENSIC_AUDIT FA-07.

## 1. Morphometry conventions (frozen)
| Item | Convention |
|---|---|
| Local thickness | Hildebrand–Rüegsegger sphere fitting on the EDT ridge; thickness = 2 × radius; `border="edge"` |
| Separation | Same algorithm on the complement within the analysis region |
| Connectivity | 26-connectivity for foreground, 6 for background; Conn.D = (1 − χ)/TV |
| Surface | marching cubes at 0.5 on the binary mask, voxel spacing applied |
| Segmentation given | reference segmentations are used as provided (no re-thresholding) |
| Reported | both `edge` and `background` conventions, `edge` primary |

## 2. Held-out morphometry validation (any new dataset with reference software values)
* Primary metric: ICC(2,1) absolute agreement, specimen level, with 95% CI; secondary: Bland–Altman bias and 95% LoA,
  mean relative difference.
* **Acceptance:** ICC(2,1) lower 95% CI bound ≥ 0.90 for Tb.Th and Tb.Sp, |mean relative difference| ≤ 5%.
* Minimum n = 8 specimens; if fewer, report descriptively without pass/fail.

## 3. Real two-class bone segmentation (dog forelimb or new datasets)
* Splits by animal; official splits used when provided; test specimens evaluated once per final model.
* Primary metric: specimen-level Dice in the evaluation band, mean with bootstrap 95% CI; secondary HD95 and relative
  volume error.
* Few-shot comparison: ≥3 seeds × subsets per k; claims of superiority require non-overlapping 95% CIs or a paired
  test across specimens×seeds with Holm correction.

## 4. Measurement support (advisor)
* Policy thresholds as in `docs/science/MEASUREMENT_SUPPORT.md` (oracle Dice ≥ 0.85, volume ±10%, noise < 0.35,
  displacement tolerance 200 µm, untracked ≤ 20%) are frozen for the first real-data evaluation.
* **Acceptance (B5):** ≥95% of scans whose graft-volume error exceeds 20% are refused or reported as conditional.
* Cost metric reported alongside: fraction of accurate measurements (error ≤ 20%) refused.

## 5. Physical phantom study (validation/ protocol, when executed by the founder's collaborators)
* Primary endpoint: graft-volume relative error versus gravimetric/known volume for each material; secondary:
  advisor decision vs observed separability.
* Acceptance for "supported" materials: |bias| ≤ 5%, 95% LoA within ±15%.

## 6. Failure detection and conformal intervals
* Failure := |graft-volume error| > 20% or graft Dice < 0.8 (per scan).
* **Acceptance (B6):** failure-detection AUROC ≥ 0.85 with lower 95% CI ≥ 0.75.
* **Acceptance (B7):** conformal 90% interval coverage 0.87–0.93 in distribution; under distribution shift coverage
  is reported, and the product must gate (abstain) rather than claim coverage.

## 7. Held-out advisor validation S1H (registered 2026-11-28, before running; advisor 1.3.3 frozen)
Motivation: advisor rules were refined after inspecting S1/S1b/S1c on the same simulator (deviations log). S1H uses
conditions that played no role in tuning:
* **Phantoms:** new seeds (2000–2002 condyle, 2100–2102 calvarial, 2200–2202 segmental; none used before), all three
  defect models; calvarial specimens use strut-like granules (120–250 µm, roughness 0.6), the others compact
  (300–600 µm); healing stage 0.45; graft material modelled as HA-like mineral of density X.
* **Densities X:** 950, 1450, 1850, 2600 mgHA/cm³ (the tuning sweep used 650, 800, 900, 1000, 1150, 1300, 1600, 2200).
* **Imaging:** PSF σ 30 µm (tuning: 20 µm); **spatially correlated noise** (white noise smoothed with a 0.8-voxel
  Gaussian, rescaled to σ ∈ {60, 120, 200}; tuning used white noise at 30/80/150/250).
* **Advisor:** version 1.3.3, material profile given as a characterised material (rel_mean = X / 1075,
  rel_sd = 0.04·rel_mean, struct 450 µm), as in the tuning sweep. Method: advisor threshold segmentation.
* **Outcome per endpoint** (residual graft, new bone, total mineral): failure = |relative volume error| > 20%.
* **Acceptance:** ≥95% of failures refused for every endpoint; P(fail | supported) Clopper–Pearson 95% upper bound
  ≤ 0.10 for endpoints with ≥30 supported specimens (descriptive otherwise). 108 specimens (9 structures × 4 densities ×
  3 noise levels); structures are the unit of replication for any CI (bootstrap over the 9 structures).
* No rule, threshold or parameter of the advisor may be changed in response to S1H; failures are reported as found.

## Deviations log
| Date | Item | Deviation | Justification |
|---|---|---|---|
| 2026-11-27 | §4 advisor policy, S1/S1b | **The claim that the advisor policy was fixed before S1 cannot be verified**: the advisor module was first committed after S1/S1b had been run, it changed during those runs (partial-volume model, near-optimal rule, single-threshold extraction), and its version string was not incremented (cycle-1 review STAT-02, IMG-06). S1/S1b results produced before advisor 1.1.0 are retained only as *exploratory* (`exp_S1_advisor_prelim.json`). | Honest provenance. From advisor 1.1.0 onward every result records `advisor_version`; S1/S1b/S1c are re-run with 1.1.0. |
| 2026-11-27 | §4 decision rule | Advisor 1.1.0 decides on the single-threshold rule actually applied (union oracle kept as the upper bound), requires support at the estimated graft share and at half of it, refuses metals, ignores reference samples with <500 voxels, never lets measured samples bypass the bone-derived rule, and requires computed day-0 QC/tracking fields. | Cycle-1 review IMG-01…IMG-04, IMG-06. Changed before the 1.1.0 runs; frozen for them. |
| 2026-11-27 | §6 registration QC | Registration QC criterion changed from host-mineral Dice ≥ 0.85 to block-wise residual displacement ≤ 2 voxels (masked normalised cross-correlation in a peri-defect shell). | Experiment L4 (Dice criterion rejected 56% of harmless misalignments) and review IMG-07 (Dice criterion failed perfect alignment at high noise). |
| 2026-11-27 | B5 acceptance | Added: P(failure \| supported) with Clopper–Pearson 95% upper bound ≤ 0.10, and the fraction of measurements supported, reported alongside refusal sensitivity. | Review STAT-03: sensitivity alone is satisfied by refusing everything. |
| 2026-11-27 | §2 morphometry acceptance | With n = 8 and k = 2 a lower 95% ICC bound ≥0.90 is unattainable even for near-perfect agreement (review STAT-14). Amended: point ICC(2,1) ≥ 0.95 **and** lower bound ≥ 0.80 when n < 20; the original criterion applies for n ≥ 20. | Feasibility; amended before any held-out morphometry data were analysed. |
| 2026-11-27 | §6 conformal acceptance | With n_test = 16 coverage can only take values k/16. Acceptance judged by the Clopper–Pearson 95% CI containing 0.90 (review STAT-08). | Feasibility; amended before U1 ran. |
