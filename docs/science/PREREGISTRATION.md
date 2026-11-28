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

## 8. Second held-out advisor validation S1H2 (registered 2026-11-28, before running; advisor 1.4.0 frozen)
Advisor 1.4.0 was designed after S1H revealed failures, using S1H conditions for development; S1H therefore no longer
validates it. S1H2 uses conditions not seen by any advisor version:
* **Phantoms:** seeds 3000–3002 (condyle), 3100–3102 (segmental), 3200–3202 (calvarial), all with compact granules
  350–650 µm, graft fill 0.30, healing stage 0.60.
* **Densities X:** 1200, 1650, 2100, 2900 mgHA/cm³.
* **Imaging:** PSF σ 25 µm and 40 µm (both, every specimen); correlated noise (white noise smoothed with a 1.2-voxel
  Gaussian) at σ ∈ {50, 100, 170}.
* **Advisor:** 1.4.0, characterised-material profile as in §7. Method: advisor threshold segmentation.
* **Outcome and acceptance:** as §7 (failure = |relative volume error| > 20%; ≥95% of failures refused per endpoint;
  P(fail | supported) upper 95% bound ≤ 0.10 where ≥30 specimens are supported). 216 specimens (9 structures × 4
  densities × 2 PSF × 3 noise); bootstrap over the 9 structures.
* No advisor change in response to S1H2; results reported as found. In-sample re-runs of S1b, S1c and S1H under 1.4.0
  are labelled development checks.

## 9. Final Generation-2 held-out advisor validation S1H3 (registered 2026-11-28, before running; advisor 1.4.1 frozen)
Advisor 1.4.1 differs from 1.4.0 only in the ambiguous-rim width (max(1, ⌈2σ⌉) voxels), motivated by S1H2. **This is
the last advisor change of Generation 2:** whatever S1H3 shows is reported as the Generation-2 result and no further
rule changes are made before human expert review and physical data.
* **Phantoms:** seeds 4000–4002 condyle (compact 300–600 µm), 4100–4102 segmental (compact 400–700 µm), 4200–4202
  calvarial (strut-like 150–300 µm, roughness 0.5); graft fill 0.30; healing stage 0.50.
* **Densities X:** 1350, 1900, 2450, 3000 mgHA/cm³.
* **Imaging:** PSF σ 15, 35 and 50 µm (every specimen); noise smoothed with a 1.0-voxel Gaussian at σ ∈ {70, 140}.
* **Advisor/method/outcome/acceptance:** as §7–§8. 216 specimens (9 structures × 4 densities × 3 PSF × 2 noise).

## 10. Held-out validation S1H4 of advisor 1.4.3 on the product's material paths (registered 2026-11-28, before running)
* **Why:** cycle-3 reviews C2-SCI-18 / C3-SCI-05 / C3-SCI-06: no held-out run had used the knowledge-base material path or
  "Unspecified" (the two paths the desktop uses), S1H3 had too few structures to bound the supported-failure rate, and
  1.4.3 changed rules after S1H3.
* **Advisor:** 1.4.3 frozen (the script asserts the version). Method: `advisor_threshold`. Failure: |relative volume error|
  > 20% per endpoint (residual graft, new bone, total mineral).
* **Structures (unseen seeds):** 36 — condyle seeds 6000–6011, segmental 6100–6111, calvarial 6200–6211 (granule sizes and
  defect geometry as S1H3 per model); healing stage 0.5.
* **Material arms:** knowledge-base ids `ha`, `bcp`, `beta_tcp` (phantoms rendered by the generator with that material;
  time since implantation given as 2 weeks for the resorbable `bcp` and `beta_tcp`), `xenograft_dbbm` (refusal arm), and
  **Unspecified** (`material=None`) on the `ha` phantoms.
* **Imaging:** 40 µm voxels; PSF 20 and 40 µm; correlated noise (σ over 1.0 voxel) 60 and 120.
* **Size:** 36 structures × 5 arms × 2 PSF × 2 noise = 720 specimens.
* **Primary analysis (structures are the unit):** per endpoint, a structure *fails* if any of its supported measurements
  fails; k = structures with ≥1 supported measurement; Clopper–Pearson 95% upper bound on the structure failure rate.
  Row-level counts, coverage and errors are reported descriptively.
* **Acceptance per endpoint:** (a) ≥95% of failing measurements refused; (b) structure-level upper bound ≤ 0.10, which
  requires k ≥ 36 with no failing structure — otherwise "not demonstrated" (not "fail") unless a supported failure occurs;
  (c) any supported failure is reported with its structure, arm and imaging condition.
* **No tuning:** the results will not be used to change 1.4.3; any later rule change needs another held-out test.

## Deviations log
| Date | Item | Deviation | Justification |
|---|---|---|---|
| 2026-11-27 | §4 advisor policy, S1/S1b | **The claim that the advisor policy was fixed before S1 cannot be verified**: the advisor module was first committed after S1/S1b had been run, it changed during those runs (partial-volume model, near-optimal rule, single-threshold extraction), and its version string was not incremented (cycle-1 review STAT-02, IMG-06). S1/S1b results produced before advisor 1.1.0 are retained only as *exploratory* (`exp_S1_advisor_prelim.json`). | Honest provenance. From advisor 1.1.0 onward every result records `advisor_version`; S1/S1b/S1c are re-run with 1.1.0. |
| 2026-11-27 | §4 decision rule | Advisor 1.1.0 decides on the single-threshold rule actually applied (union oracle kept as the upper bound), requires support at the estimated graft share and at half of it, refuses metals, ignores reference samples with <500 voxels, never lets measured samples bypass the bone-derived rule, and requires computed day-0 QC/tracking fields. | Cycle-1 review IMG-01…IMG-04, IMG-06. Changed before the 1.1.0 runs; frozen for them. |
| 2026-11-27 | §6 registration QC | Registration QC criterion changed from host-mineral Dice ≥ 0.85 to block-wise residual displacement ≤ 2 voxels (masked normalised cross-correlation in a peri-defect shell). | Experiment L4 (Dice criterion rejected 56% of harmless misalignments) and review IMG-07 (Dice criterion failed perfect alignment at high noise). |
| 2026-11-27 | B5 acceptance | Added: P(failure \| supported) with Clopper–Pearson 95% upper bound ≤ 0.10, and the fraction of measurements supported, reported alongside refusal sensitivity. | Review STAT-03: sensitivity alone is satisfied by refusing everything. |
| 2026-11-27 | §2 morphometry acceptance | With n = 8 and k = 2 a lower 95% ICC bound ≥0.90 is unattainable even for near-perfect agreement (review STAT-14). Amended: point ICC(2,1) ≥ 0.95 **and** lower bound ≥ 0.80 when n < 20; the original criterion applies for n ≥ 20. | Feasibility; amended before any held-out morphometry data were analysed. |
| 2026-11-27 | §6 conformal acceptance | With n_test = 16 coverage can only take values k/16. Acceptance judged by the Clopper–Pearson 95% CI containing 0.90 (review STAT-08). | Feasibility; amended before U1 ran. |
| 2026-11-28 | Acceptance rule for future validations | Cycle-2 review C2-SCI-16: the "P(fail \| supported) bound only with ≥30 supported" rule let S1H graft pass with 4/16 supported failures. From now on acceptance also requires a point failure rate ≤10% among supported cases regardless of n. Applied retrospectively as a check: S1H graft fails it (25%); S1H2 graft (0/68) and S1H3 graft (0/80) and mineral (0/22) pass it. | Closes a loophole; does not change any reported number. |
| 2026-11-28 | Advisor changed after the "final" validation (1.4.2) | §9 called 1.4.1 the last change of Generation 2. 1.4.2 followed the cycle-2 review and was committed together with the S1H3 results, without an entry here at the time (cycle-3 review C3-SCI-06). Its changes (metals, DBBM day-0, BCP timepoint, noise on measured references, method binding) do not touch the S1H3 path; the review reproduced two S1H3 rows exactly under 1.4.2. | Recorded late; no S1H3 number changes. |
| 2026-11-28 | Advisor 1.4.3 (cycle-3 review) | Unspecified-material rim proxy (C3-SCI-01), measured-reference noise and partial volume (C3-SCI-07), day-0 limits for resorbable materials and uncertain profiles without a physics cross-check (C2-SCI-11), and a stricter total-mineral rim gate, rim/(mineral − rim) ≤ 0.20 (C3-SCI-10). Only the last touches the S1H3 path, in the stricter direction; the same conditions were re-run under 1.4.3 as a consistency check (`exp_S1H3_rerun_advisor_1_4_3.json`, not a held-out validation). A new pre-registered held-out test is needed for any further claim about 1.4.3. | Development after S1H3; disclosed. |
| 2026-11-28 | S1H3 analysis unit and the retrospective acceptance amendment | §7 (inherited by §9) makes structures the unit of replication for any CI. The headline P(fail \| supported) bound 0.045 treated the 80 supported rows as independent; with the 9 structures as the unit the Clopper–Pearson bound is 0.34, so the precision criterion (≤0.10) is **not demonstrated** for residual graft (cycle-3 review C3-SCI-05). The 2026-11-28 acceptance amendment (point rate ≤10%) was written after S1H3 had run and is **not** used to call any S1H3 endpoint a pass (C3-SCI-06). | Corrects an analysis deviation; S1H3 conclusions restated. |
| 2026-11-28 | §10 S1H4 execution | The first run was stopped by a container restart at 24 of 36 structures; it had printed progress counts only (no row saved, nothing analysed). It was re-run from scratch with the same code plus per-structure checkpointing (`exp_S1H4_heldout.py`, commit `2b95863`: execution only; analysis unchanged). | Infrastructure interruption; no result was seen before the complete run. |
| 2026-11-28 | §10 S1H4 result reporting | Reported as pre-registered: (a) met on every endpoint, (b) not demonstrated on any endpoint, (c) no supported failure. Descriptive additions not in §10: per-arm and per-condition coverage, the sign of the supported total-mineral errors, and scan-measured blur versus reference. | Disclosed as descriptive. |

