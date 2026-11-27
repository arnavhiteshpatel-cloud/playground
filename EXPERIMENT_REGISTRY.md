# Experiment Registry

All results: `experiments/results/*.json` (machine-readable) and figures in `experiments/results/figures/`.
**SYNTHETIC** = computational phantoms with exact ground truth (generator v1.0.0); **REAL** = public datasets.
Specimen-level means with 95% CI unless stated; voxels are never treated as biological replicates.
Several experiments were corrected after an independent review (docs/security/REVIEW_RESPONSE.md); corrected values below.

| ID | Question / hypothesis | Data | Status | Key result | Result file |
|---|---|---|---|---|---|
| **A** | Do threshold workflows separate graft from new bone? Does a feature RF help? | SYNTHETIC test 16 (4 ceramics) | Done (rerun with balanced RF, 12 specimens/3 per material) | Graft Dice: CTAn-style 0.770, multi-Otsu 0.764, RF 0.888, RF without spatial feature 0.878. New bone: 0.673 / 0.673 / 0.745 / 0.705. Mineral Dice 0.91–0.93 | exp_A_baselines.json |
| **B** | Synthetic 3-class 3D U-Net; does an explicit ROI-context channel help? | SYNTHETIC train 48 / val 8 / test 16 | Done | Graft 0.918 [0.886–0.950], new bone 0.861 [0.837–0.884], host 0.960, HD95 graft 47 µm, ECE 0.008. No-context model: 0.919 / 0.866 / 0.966 → **context hypothesis not supported** | exp_B_unet.json |
| **C** | When does graft/new-bone intensity overlap make separation fail? | SYNTHETIC, 8 densities × 4 noise levels | Done (oracle corrected, Q-01) | Overlap regime (800–1000 mgHA/cm³): intensity-only Dice oracle 0.52–0.77; multi-Otsu 0.21–0.75; RF 0.85–0.92 (compact granules) | exp_C_D_E_separability.json, figure exp_C_separability.png |
| **C2** | What information lets RF exceed intensity? Morphology dependence | SYNTHETIC overlap regime | Done | Compact: oracle 0.61, raw 0.49, multiscale 0.72, +shape 0.86, +spatial 0.88. Strut-like: oracle 0.36, RF 0.65–0.70 → **context only helps when graft morphology differs** | exp_C2_ablation.json |
| **D** | Voxel-size sensitivity | SYNTHETIC 40/80/120 µm | Done | RF graft Dice 0.947 → 0.880 (1300 mgHA/cm³) from 40 to 120 µm | in exp_C_D_E |
| **E** | Artefact robustness | SYNTHETIC | Done | Rings/cupping ≤0.01 Dice; 60 µm blur −0.11 for multi-Otsu; gain/offset shift drops RF 0.962→0.810, percentile normalisation restores 0.962 | in exp_C_D_E |
| **F** | Automatic defect-ROI accuracy | SYNTHETIC 36 + REAL ovine 2 | Done | Plate defects: Dice 0.971/0.976 with nominal diameter, 0.881/0.904 automatic; segmental: 50% explicit failures when healing bridges the gap (by design: no silent wrong ROI). Real ovine: day-18 found (conf 0.56, review); day-161 exception | exp_F_roi.json |
| **G** | Morphometry numerical accuracy | analytic + REAL 8 cubes with Scanco IPL maps | Done | Plates exact (even voxels), rods ≈1 voxel thin; vs IPL: Tb.Th ICC 0.983 (−2.4%), Tb.Sp ICC 0.948 (−4.1%) with edge convention (chosen post hoc, Q-10); background convention ICC 0.61/0.55 | exp_G_morphometry.json |
| **H** | Real-data bone segmentation | REAL dog forelimb micro-CT (CC-BY-4.0), 10 train / 5 test, band around labelled bones | Done (task redefined after first run was ill-posed) | Dice: Otsu 0.508, GMM 0.607, RF(10 scans) 0.758, **U-Net(10 real scans) 0.826** (HD95 1.8 voxels) | exp_H_I_real.json |
| **I** | Synthetic→real transfer | REAL dog forelimb | Done | Synthetic U-Net zero-shot **0.379 (fails: domain gap)**; + 1 real labelled scan **0.787**; + 3 scans 0.781 (≈95% of the 10-scan real model) | exp_H_I_real.json |
| **J** | ≤10 labelled scans adapt to a new material? | SYNTHETIC held-out materials (pool 24, test 16) | Done | Zero-shot graft 0.843; k=1: 0.874, 3: 0.908, 5: 0.900, 10: 0.914, 20: 0.919; RF from scratch k=1: 0.654, 3: 0.847 → supported **in simulation only** (optimistic) | exp_J_adaptation.json |
| **K** | Uncertainty: selective segmentation, calibration, OOD flag | SYNTHETIC ID 16 + OOD 16 | Done (rerun: temperature applied, validation-derived threshold, Q-12) | Deferring 10% least-confident voxels: retained accuracy 0.940→0.973; after review new-bone Dice 0.866→0.951, graft 0.920→0.964 (20%: 0.984/0.983). Failure flag (graft Dice<0.8): sensitivity 4/4, specificity 0.75. ID-vs-OOD AUROC 0.66 (**weak OOD detector**). Temperature scaling worsened ECE 0.008→0.011 | exp_K_M_uncertainty.json |
| **L** | Day-0 registration for graft vs new bone | SYNTHETIC 3 specimens × 2 densities | Done | Rigid TRE 0.3–1 µm; overlap regime graft Dice: day-0 0.915, RF 0.887, multi-Otsu 0.558; easy regime day-0 0.893 < RF 0.955 (creeping substitution). Best case (Q-11) | exp_L_longitudinal.json |
| **L2** | Day-0 when graft mimics new bone | SYNTHETIC strut-like | Done | Day-0 **0.816** vs RF 0.663, multi-Otsu 0.318, intensity oracle 0.323 | exp_L2_strutlike.json |
| **M** | Human correction workflow (simulated) | SYNTHETIC | Done (effort constants ASSUMED) | Correcting the 10% least-confident voxels; modelled time reduction ≈78% (assumed 20 s vs 90 s per slice — not measured) | exp_K_M_uncertainty.json |
| **N** | Histology module | SYNTHETIC sections + REAL NuInsSeg nuclei (tuned on 10, evaluated on 60) | Done (partial success) | 2D–3D registration Dice 0.31–0.40 → 0.85–0.87; graft-void ICC 0.84; bone-area ICC 0.35 (weak); Macenko worsens; nuclei pixel Dice 0.64, object F1 0.34 (classical; below DL tools) | exp_N_histology.json |
| **O** | Speed and memory on real full-resolution data | REAL 2.1 GB TXM (1.04 G voxels), 829-slice DICOM | Done (3 defects found & fixed: padding in out-of-core Otsu, DICOM memory, script bug) | TXM→chunked Zarr streamed in 11 s at 386 MB peak; SHA-256 of 2.1 GB in 20 s; out-of-core threshold + mineral volume in 12 s at 726 MB; full-volume QC 4.2 s at 2.4 GB; DICOM 829 slices 5.1 s at 4.45 GB (was OOM); U-Net inference ≈49k voxels/s on 4 CPUs (≈34 min per 100 M voxels → GPU needed for full-resolution studies) | exp_O_performance.json |
| **P** | Reproducibility across runs | SYNTHETIC + format round-trips | Done | All bit-identical: pipeline labels & metrics, U-Net probabilities, fixed-seed training weights (max diff 0.0), RF, NIfTI/NRRD/Zarr/TIFF/DICOM round-trips | exp_P_reproducibility.json |
| **Q-01** | Correct intensity-only oracle | as C, C2, L2 | Done | values above | exp_Q01_intensity_oracle.json |

## Blocked experiments (need physical or external data)
| ID | Needs | Prepared |
|---|---|---|
| E2 physical separability | phantom scans of 3–5 commercial grafts (validation/) | analysis pipeline runs on any NIfTI/TIFF/TXM; `osteoquant analyze` |
| U3 real adaptation | labelled scans from ≥2 scanners/materials | `exp_J_adaptation.py` accepts any Case list |
| A7/E6 time saving & ICC vs analysts | partner retrospective scans + timed analysts | viewer logs edits; stats.icc/bland_altman ready |
| E8 micro-CT vs histology | matched sections | histology module + 2D–3D registration ready |

## Generation 2 experiments (2026-11-27 onward)
Pre-registered conventions and acceptance criteria: `docs/science/PREREGISTRATION.md`. Reproduction of Gen-0
results: `FORENSIC_AUDIT.md` §2 (G exact, P exact, C within 0.004 Dice).

| ID | Question | Data | Status | Key result | Result file |
|---|---|---|---|---|---|
| **S1** | Does the measurement-support advisor refuse the measurements that fail (graft-volume error >20%)? | SYNTHETIC: 56 dataset specimens (4 trained + 2 held-out materials) + 96 density×noise conditions | Done (rerun with final advisor queued) | Multi-Otsu: all 32/32 failures refused, 7 supported all accurate (median error 11%); synthetic U-Net: 6/6 failures refused but 43 accurate U-Net measurements also refused (advisor reasons only from intensity); sweep: 54/54 failures refused, 0 supported-but-failed | exp_S1_advisor.json |
| **S1b** | Does the advisor's own threshold approach the oracle where support is granted? | as S1 | Done | Sweep: 46/46 failures refused, 0/21 supported cases failed, median error of supported 6.6%; advisor threshold within ≈20 grey units of the true-oracle threshold for X ≤1600 mgHA/cm³; advisor oracle is conservative (lower than true oracle) → 29 accurate cases refused. Dataset specimens: 40/41 failures refused, 1/7 supported failed | exp_S1b_advisor_threshold.json |
| **F2** | Segmental ROI at a late (bridged) timepoint by propagating the early ROI through registration | SYNTHETIC 16 animals (4 noise levels), late stage 0.9 + random rigid motion | Done | Propagated ROI Dice 0.995 (min 0.993), registration QC pass 16/16; automatic detection on the late scan did not fail in this configuration (Dice 0.846) — the Gen-0 failure mode was not reproduced here, so F2 shows accuracy gain, not failure recovery | exp_F2_roi_propagation.json |
| **S2** | Closing the synthetic→real gap: rescaling diagnosis, domain-randomised pretraining, few-shot curves (3 seeds) | REAL dog forelimb (10/5) | Running | — | exp_S2_sim2real_*.json |
| **L3** | Day-0 propagation with granule displacement (0–400 µm) and fragmentation; granule tracking; registration-failure detection | SYNTHETIC generator v2 | Queued | — | exp_L3_displacement.json |
| **U1** | 5-seed variance, measurement-based selection, ensemble failure detection, conformal volume intervals | SYNTHETIC incl. new 40-specimen calibration split | Queued | — | exp_U1_ensemble_conformal.json |
| **O2** | ONNX Runtime fp32/int8 vs PyTorch, patch overlap | SYNTHETIC test | Queued (spot check done: ORT fp32 max prob diff 5×10⁻⁶, labels identical, 8.5× faster than PyTorch under the same load) | — | exp_O2_runtime.json |
