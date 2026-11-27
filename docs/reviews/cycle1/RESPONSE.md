# Cycle 1 — Response and Remediation Log

Reviews: `REVIEW_IMAGING_STATS.md` (imaging scientist + biostatistician, 32 findings), `REVIEW_ML_ARCH.md`
(ML scientist + software architect, 28 findings). Status: **fixed** (code/doc change + test or re-run),
**re-run** (experiment re-executed with the fix), **accepted** (limitation documented, no code change possible
now), **open**. Commit `f7fbab6` and the following commit carry the fixes.

| ID | Sev | Status | Response |
|---|---|---|---|
| STAT-01 | critical | fixed | Study bundles use `reported_metrics`; PDF lists every suppressed endpoint with its reason (`api/bundle.py`, `report/defectfill.py`). |
| IMG-01 | critical | fixed | Advisor 1.1.0 estimates the graft share from the scan and requires support at that share and half of it; <5% share refuses graft-volume endpoints (tests: `test_scarce_graft_*`, `test_support_requires_robustness_*`). |
| ARC-01 | critical | fixed | Fine-tuned models inherit parent provenance/licence and record the parent (name, SHA-256); a research-only parent can never yield a commercial-eligible child. |
| IMG-02 | high | fixed | Metals refused (`test_metals_refused`). |
| IMG-03 | high | fixed | Reference samples need ≥500 voxels; bone-derived rule cannot be bypassed; autograft profile added. |
| IMG-04 | high | fixed | Day-0 support requires computed `registered`, `qc_pass`, `untracked_fraction`, `max_displacement_um`. |
| IMG-05 | high | fixed (disclosed) | Day-0 condition for resorbable materials states that creeping substitution inside the footprint is counted as graft. Method change (footprint ∩ graft-like texture) deferred: needs real data. |
| IMG-06 | high | fixed + re-run | Decision and applied threshold come from one assessment (single-threshold rule). S1b/S1c re-run with advisor 1.1.0. |
| STAT-02 | high | fixed (disclosed) | Pre-registration claim for S1/S1b withdrawn (deviations log); version stamping in all results. |
| STAT-03 | high | fixed | S1 summaries report P(fail \| supported) with Clopper–Pearson upper bound and supported fraction; acceptance amended. |
| STAT-04 | high | accepted | Simulator–advisor shared assumptions cannot be removed in simulation; physical stages B/C (validation programme) are the remedy. Stated in every S1 summary. |
| STAT-05 | high | fixed + re-run | New-bone and total-mineral errors now computed; mineral threshold moved from global Otsu to relative 0.30 in the advisor-threshold method. |
| IMG-07 | high | fixed | Registration QC = block-wise residual displacement (masked NCC) ≤ 2 voxels; Dice/NCC secondary. L4 re-run. |
| STAT-06 | high | fixed + re-run | L3: fixed 500 µm search, advisor inputs computed from tracking/QC (no hard-coded displacement). |
| STAT-07 / ML-11 | high | fixed | U1 AUROC stratified (pooled / ID-only / OOD-only) plus OOD-membership AUROC; clustering limitation stated. |
| ML-12 / STAT-08 | high/med | fixed | Gated conformal recalibrated on gated calibration scans; Clopper–Pearson CIs on coverage; acceptance to be judged by CI containing 0.90. |
| ML-01 | high | fixed | 4-class model fine-tuned with real bone mapped to host (class 3). |
| ML-02 | high | fixed | S2 arms share LR (1e-3), iterations, batch; extra scratch arm at 3e-3; head-size difference stated. |
| ML-03 | high | fixed | DR sampler emulates whole-volume normalisation (soft tissue median now spans ≈0.07–0.56). |
| ML-04 | high | fixed | Zoom chosen on training specimens only; test evaluated once at that zoom (and at 1.0). |
| ML-05 | high | fixed | Seeds averaged within specimen; bootstrap over specimens; paired arm differences. |
| ARC-02 | high | fixed | Sampler sources must be listed (`manifest`) or the model is research-only; `describe_sampler` records config + source hash. |
| ARC-03 | high | fixed | Registry writes are locked + atomic (`update_registry`); `OQ_MODEL_DIR` isolates reproduction runs. The Gen-0 reproduction of H/I that ran before the fix wrote into `models/` — registry/file hashes re-verified afterwards (see FORENSIC_AUDIT §7). |
| ARC-04 | high | fixed | DR config and source hashes stored in the model config. |
| ARC-06 | high | fixed | Pipeline refuses non-4-class models for tissue segmentation. |
| IMG-11 | medium | fixed | No-graft and radiolucent paths keep the new-bone architecture endpoint (test added). |
| IMG-13 | medium | fixed | `propagate_roi` re-registers with the defect excluded (two-pass). |
| IMG-10 | medium | fixed | Effective energy taken from config/acquisition metadata (`effective_energy_keV`). |
| ARC-05 | medium | fixed | Checkpoints record git commit, dirty flag and a hash of the package sources. |
| ARC-07 | medium | fixed | `mineral_volume_mm3` defined identically in raw and reported metrics. |
| ML-07 | medium | fixed | Isotropic DR zoom. |
| ML-09 | medium | fixed (opt-in) | Ignore-aware boundary weights (`boundary_ignore_aware`), on for all new real-data training; off for Gen-0 seeds to keep the ensemble consistent. |
| ML-13 | medium | accepted | Generator v2 defaults verified bit-identical to v1 on a test specimen; stated in U1. |
| STAT-14 | medium | open → amended | ICC lower-bound criterion infeasible at n=8; amendment proposed in PREREGISTRATION (point ICC ≥0.95 and lower bound ≥0.80 when n<20). |
| Remaining medium/low (STAT-09…16, IMG-08/09/12/14–16, ML-06/08/10/13–16, ARC-08–12) | — | open | Tracked for cycle 2; none changes a customer-facing number in the current build. |
