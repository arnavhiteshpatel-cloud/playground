"""Experiment F2 — segmental ROI after bridging via propagation from an early timepoint (FA-05, B10).

Segmental phantoms (80×72×72, 40 µm, gap 2000 µm), stages: early 0.2 (gap open) and late 0.9 (bridged).
Late scan gets a random rigid motion (≤5°, ≤200 µm). Compared:
  auto_late        segmental-gap detector on the late scan (Gen-0 behaviour: often fails when bridged)
  propagated       early-timepoint ROI (true geometric ROI, i.e. as confirmed by the user at day 0/early)
                   registered onto the late scan
Truth: late phantom ROI transformed by the applied motion. Metrics: ROI Dice, failure (exception), QC pass.
4 noise levels × 4 seeds = 16 animals.
"""
import numpy as np

from common import save_result
from osteoquant.longitudinal import apply_rigid, propagate_roi
from osteoquant.phantom import PhantomConfig, generate_phantom, render_fast, ImagingConfig
from osteoquant.roi import detect_segmental_gap, ROIDetectionError

SP = (40.0,) * 3
rows = []
rng = np.random.default_rng(5)
for noise in (40, 80, 120, 250):
    for s in range(4):
        kw = dict(model="segmental", shape=(80, 72, 72), voxel_um=40, supersample=1, gap_length_um=2000,
                  graft_material="beta_tcp", seed=1500 + s + noise, periodic_texture=False)
        early = generate_phantom(PhantomConfig(healing_stage=0.2, **kw))
        late = generate_phantom(PhantomConfig(healing_stage=0.9, **kw))
        Ie = render_fast(early.mu, 40, ImagingConfig(psf_sigma_um=25, noise_sigma=noise, seed=s)).data
        Il = render_fast(late.mu, 40, ImagingConfig(psf_sigma_um=25, noise_sigma=noise, seed=s + 100)).data
        rot, tr = rng.uniform(-5, 5, 3), rng.uniform(-200, 200, 3)
        Il_m, _ = apply_rigid(Il, SP, rot, tr)
        truth, _ = apply_rigid(late.roi_mask.astype(np.uint8), SP, rot, tr, labels=True)
        truth = truth > 0
        rec = {"noise": noise, "seed": s}
        try:
            roi = detect_segmental_gap(Il_m, SP)
            m = roi.to_mask(Il_m.shape, SP, (0, 0, 0))
            rec["auto_late_dice"] = float(2 * (m & truth).sum() / max(1, m.sum() + truth.sum()))
            rec["auto_late_failed"] = False
            rec["auto_late_conf"] = float(roi.confidence)
        except ROIDetectionError as e:
            rec["auto_late_failed"] = True
            rec["auto_late_dice"] = None
            rec["auto_late_error"] = str(e)
        pr = propagate_roi(Ie, early.roi_mask, Il_m, SP)
        rec["propagated_dice"] = float(2 * (pr["roi"] & truth).sum() / max(1, pr["roi"].sum() + truth.sum()))
        rec["propagated_qc"] = pr["qc"]
        rows.append(rec)
        print(noise, s, "auto", rec.get("auto_late_dice"), rec["auto_late_failed"], "| propagated",
              round(rec["propagated_dice"], 3), "QC", pr["qc"]["pass"], round(pr["qc"]["host_dice"], 3), flush=True)
summ = {"n": len(rows), "auto_fail_rate": float(np.mean([r["auto_late_failed"] for r in rows])),
        "auto_dice_when_found": float(np.mean([r["auto_late_dice"] for r in rows if r["auto_late_dice"] is not None]))
        if any(r["auto_late_dice"] is not None for r in rows) else None,
        "propagated_dice_mean": float(np.mean([r["propagated_dice"] for r in rows])),
        "propagated_dice_min": float(np.min([r["propagated_dice"] for r in rows])),
        "propagated_qc_pass_rate": float(np.mean([r["propagated_qc"]["pass"] for r in rows])),
        "success_rate_dice_ge_0_9_and_qc": float(np.mean([r["propagated_dice"] >= 0.9 and r["propagated_qc"]["pass"] for r in rows]))}
print(summ)
save_result("exp_F2_roi_propagation", {"experiment": "F2", "summary": summ, "rows": rows})
