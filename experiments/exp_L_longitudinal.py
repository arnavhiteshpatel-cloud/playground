"""Experiment L — longitudinal registration and day-0 graft propagation.

Hypothesis (playbook fallback): when graft and new bone have overlapping attenuation, a
registered day-0 (post-implantation) scan can separate residual graft from new bone at a later
timepoint better than single-timepoint intensity methods.
Design: 4 synthetic specimens; for each, a day-0 phantom (stage 0) and a later phantom
(stage 0.6) with identical host anatomy and initial granule packing (same seed). Graft density
set to 900 mgHA/cm³ (inside the new-bone range) — the hard regime of Experiment C — and also
1600 (easy regime). The later scan is moved by a random rigid motion (≤5°, ≤200 µm) and
registered back (rigid, normalised correlation, metric mask = host anatomy outside the dilated defect). Methods compared on the later scan in the ROI:
  (1) day-0 propagation with *true* alignment (upper bound),
  (2) day-0 propagation after estimated registration,
  (3) multi-Otsu single timepoint, (4) RF single timepoint (trained on another specimen),
  (5) intensity-only Bayes bound.
Metrics: graft / new-bone Dice in ROI; TRE (µm); graft-remaining fraction error.
Known limitation by construction: creeping substitution inside the original footprint.
"""
from __future__ import annotations

import numpy as np

from common import save_result
from exp_C_separability import mu_with_graft, gn_scores, bayes_bound
from osteoquant.phantom import PhantomConfig, generate_phantom, ImagingConfig, render_fast
from osteoquant.longitudinal import register, resample, apply_rigid, target_registration_error, day0_propagation
from osteoquant.segment import classical as C

SHAPE = (56, 72, 72)
SP = (40.0, 40.0, 40.0)


def pair(seed):
    kw = dict(model="condyle", shape=SHAPE, voxel_um=40, defect_diameter_um=2000, graft_material="ha", seed=seed, periodic_texture=False)
    return generate_phantom(PhantomConfig(healing_stage=0.0, **kw)), generate_phantom(PhantomConfig(healing_stage=0.6, **kw))


def main():
    rng = np.random.default_rng(42)
    seeds = [800, 801, 802, 803]
    pairs = [pair(s) for s in seeds]
    out = {"experiment": "L", "rows": [], "noise_sigma": 150}
    for X in (900, 1600):
        imgs0 = [render_fast(mu_with_graft(p0, X), 40, ImagingConfig(seed=1 + i, psf_sigma_um=20, noise_sigma=150)).data
                 for i, (p0, _) in enumerate(pairs)]
        imgs1 = [render_fast(mu_with_graft(p1, X), 40, ImagingConfig(seed=11 + i, psf_sigma_um=20, noise_sigma=150)).data
                 for i, (_, p1) in enumerate(pairs)]
        rf = C.RFSegmenter(40, 16, 0).fit([imgs1[0]], [pairs[0][1].labels], [SP], [pairs[0][1].roi_mask], 20000)
        for i in range(1, len(pairs)):
            p0, p1 = pairs[i]
            roi = p1.roi_mask
            y = p1.labels
            # day-0 graft footprint from the day-0 scan (all mineral inside ROI is graft at day 0)
            m0, t0 = C.threshold_otsu(imgs0[i])
            g0 = C.clean_binary(m0 & p0.roi_mask, 8)
            g0_true = p0.labels == 2
            # later scan: mineral by Otsu
            m1, _ = C.threshold_otsu(imgs1[i])
            res = {}
            res["day0_true_alignment"] = gn_scores(day0_propagation(m1, g0, roi), y, roi)
            res["day0_true_footprint_true_alignment"] = gn_scores(day0_propagation(m1, g0_true, roi), y, roi)
            # simulate repositioning, register back
            rot = rng.uniform(-5, 5, 3)
            tr = rng.uniform(-200, 200, 3)
            moved, t_true = apply_rigid(imgs1[i], SP, rot, tr)
            from scipy import ndimage as ndi
            reg_mask = ~ndi.binary_dilation(p0.roi_mask, iterations=3)   # register on stable host anatomy only
            reg_mask[:3], reg_mask[-3:], reg_mask[:, :3], reg_mask[:, -3:], reg_mask[:, :, :3], reg_mask[:, :, -3:] = [False] * 6
            tx, metric = register(imgs0[i], moved, SP, "rigid", mask=reg_mask)
            back = resample(moved, SHAPE, SP, tx)
            # TRE at ROI points (mm, x,y,z)
            pts = np.argwhere(roi)[:: max(1, roi.sum() // 300)][:, ::-1] * 0.04
            tre = target_registration_error(t_true, tx, pts)
            mb, _ = C.threshold_otsu(back)
            valid = back != 0
            res["day0_estimated_registration"] = gn_scores(day0_propagation(mb & valid, g0, roi), y, roi & valid)
            res["multiotsu_single_timepoint"] = gn_scores(C.seg_multiotsu(imgs1[i], roi, X > 850)[0], y, roi)
            res["rf_single_timepoint"] = gn_scores(rf.predict(imgs1[i], SP, roi)[0], y, roi)
            bb = bayes_bound(imgs1[i], y, roi & ((y == 1) | (y == 2)))
            res["bayes_intensity_bound"] = bb
            for k, v in res.items():
                out["rows"].append({"graft_mgHA": X, "specimen": seeds[i], "method": k, "acc": v[0], "dice_graft": v[1],
                                    "dice_new": v[2], "tre_mean_um": tre["mean_um"], "tre_max_um": tre["max_um"],
                                    "true_motion_rot_deg": rot.tolist(), "true_motion_trans_um": tr.tolist(),
                                    "substitution_note": "new bone inside original footprint is counted as graft by day-0 methods"})
            print(X, seeds[i], {k: round(v[1], 3) for k, v in res.items()}, "TRE", round(tre["mean_um"], 1), flush=True)
    summ = {}
    for X in (900, 1600):
        for m in sorted({r["method"] for r in out["rows"]}):
            R = [r for r in out["rows"] if r["graft_mgHA"] == X and r["method"] == m]
            summ[f"{X}/{m}"] = {"dice_graft": float(np.mean([r["dice_graft"] for r in R])),
                                "dice_new": float(np.mean([r["dice_new"] for r in R])), "n": len(R)}
    out["summary"] = summ
    out["tre_mean_um"] = float(np.mean([r["tre_mean_um"] for r in out["rows"]]))
    save_result("exp_L_longitudinal", out)
    for k, v in summ.items():
        print(k, v)


if __name__ == "__main__":
    main()
