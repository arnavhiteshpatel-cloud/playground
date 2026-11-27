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

## Deviations log
| Date | Item | Deviation | Justification |
|---|---|---|---|
| 2026-11-27 | §4 advisor policy, S1/S1b | **The claim that the advisor policy was fixed before S1 cannot be verified**: the advisor module was first committed after S1/S1b had been run, it changed during those runs (partial-volume model, near-optimal rule, single-threshold extraction), and its version string was not incremented (cycle-1 review STAT-02, IMG-06). S1/S1b results produced before advisor 1.1.0 are retained only as *exploratory* (`exp_S1_advisor_prelim.json`). | Honest provenance. From advisor 1.1.0 onward every result records `advisor_version`; S1/S1b/S1c are re-run with 1.1.0. |
| 2026-11-27 | §4 decision rule | Advisor 1.1.0 decides on the single-threshold rule actually applied (union oracle kept as the upper bound), requires support at the estimated graft share and at half of it, refuses metals, ignores reference samples with <500 voxels, never lets measured samples bypass the bone-derived rule, and requires computed day-0 QC/tracking fields. | Cycle-1 review IMG-01…IMG-04, IMG-06. Changed before the 1.1.0 runs; frozen for them. |
| 2026-11-27 | §6 registration QC | Registration QC criterion changed from host-mineral Dice ≥ 0.85 to block-wise residual displacement ≤ 2 voxels (masked normalised cross-correlation in a peri-defect shell). | Experiment L4 (Dice criterion rejected 56% of harmless misalignments) and review IMG-07 (Dice criterion failed perfect alignment at high noise). |
| 2026-11-27 | B5 acceptance | Added: P(failure \| supported) with Clopper–Pearson 95% upper bound ≤ 0.10, and the fraction of measurements supported, reported alongside refusal sensitivity. | Review STAT-03: sensitivity alone is satisfied by refusing everything. |
