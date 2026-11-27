"""Experiment A — classical baseline comparison (synthetic three-class test set).

Hypothesis: on reconstructed micro-CT with radiodense ceramic grafts, intensity-threshold
workflows separate mineral from soft tissue well, but separate graft from new bone poorly when
their attenuation distributions overlap; a multi-scale feature Random Forest recovers part of
the gap using texture/shape context.
Data: data/processed/synth/test (16 specimens; beta-TCP, BCP, HA, CaSO4; 3 defect models).
Baselines: global fixed threshold, Otsu, adaptive local mean, GMM, k-means, CTAn-style
(two global thresholds, oracle-free: Otsu + Otsu-within-ROI), multi-Otsu, intensity+morphology,
Random Forest (trained on 12 train specimens, 3 per material; the U-Net used all 48).
Metrics: mineral Dice (whole volume), per-class Dice/HD95 in the defect ROI (true ROI given to
all methods so that ROI error does not confound), runtime. Specimen-level summaries with 95% CI.
"""
from __future__ import annotations

import time

import numpy as np

from common import load_split, save_result, mean_ci
from osteoquant.segment import classical as C
from osteoquant.segment.metrics import multiclass_metrics, binary_metrics
from skimage.filters import threshold_otsu, threshold_multiotsu


def run():
    test = load_split("test")
    allt = load_split("train", limit=48)
    train = []
    for mat in ("beta_tcp", "bcp", "ha", "calcium_sulfate"):     # balanced: 3 specimens per material (review Q-03)
        train += [c for c in allt if c.meta["spec"]["material"] == mat][:3]
    sp = test[0].spacing
    # RF trained once
    t0 = time.time()
    rf = C.RFSegmenter(n_estimators=60, seed=0).fit([c.image for c in train], [c.labels for c in train],
                                                     [c.spacing for c in train], [c.roi for c in train],
                                                     n_per_class=8000)
    rf_train_s = time.time() - t0
    rf_ns = C.RFSegmenter(n_estimators=60, seed=0, feature_set="no_spatial").fit(
        [c.image for c in train], [c.labels for c in train], [c.spacing for c in train], [c.roi for c in train], n_per_class=8000)
    # fixed global threshold chosen once on training data (median Otsu) — mimics a lab SOP
    t_fixed = float(np.median([threshold_otsu(c.image[::2, ::2, ::2]) for c in train]))
    t_graft_fixed = float(np.median([threshold_multiotsu(c.image[c.roi & (c.image > t_fixed)], 2)[0]
                                     for c in train]))
    rows = []
    for c in test:
        x, y, roi = c.image, c.labels, c.roi
        mineral_true = y > 0
        mat = c.meta["spec"]["material"]
        brighter = True  # all four training materials are denser than new bone in this simulation
        methods = {}

        def timeit(name, fn):
            t = time.time()
            out = fn()
            methods[name] = (out, time.time() - t)

        timeit("global_fixed_sop", lambda: C.seg_ctan_style(x, roi, t_fixed, t_graft_fixed, brighter))
        timeit("otsu_ctan_style", lambda: (lambda m: C.seg_ctan_style(
            x, roi, m[1], float(threshold_multiotsu(x[roi & m[0]], 2)[0]), brighter))(C.threshold_otsu(x)))
        timeit("adaptive", lambda: C.compose_three_class(C.threshold_adaptive(x, 600, sp, 0) & (x > np.percentile(x, 40)),
                                                         x > np.percentile(x[roi], 92), roi))
        timeit("multiotsu", lambda: C.seg_multiotsu(x, roi, brighter)[0])
        timeit("multiotsu_smoothed", lambda: C.seg_multiotsu(x, roi, brighter, smooth_sigma=1.0)[0])
        timeit("gmm3", lambda: C.seg_gmm(x, roi, brighter)[0])
        timeit("kmeans3", lambda: C.seg_kmeans(x, roi, brighter)[0])
        timeit("intensity_morphology", lambda: C.seg_morphology(
            x, roi, sp, C.threshold_otsu(x)[1], float(threshold_multiotsu(x[roi & (x > C.threshold_otsu(x)[1])], 2)[0]),
            brighter))
        timeit("random_forest", lambda: rf.predict(x, sp, roi)[0])
        timeit("random_forest_no_spatial", lambda: rf_ns.predict(x, sp, roi)[0])
        for name, (lab, dt) in methods.items():
            r = multiclass_metrics(lab, y, spacing=sp, mask=roi, distances=True)
            mb = binary_metrics(lab > 0, mineral_true, sp, distances=False)
            rows.append({"case": c.case_id, "material": mat, "model": c.meta["spec"]["model"],
                         "stage": c.meta["spec"]["stage"], "method": name, "seconds": dt,
                         "mineral_dice": mb["dice"], "mean_dice_roi": r["mean_dice"],
                         **{f"dice_{k}": v["dice"] for k, v in r["per_class"].items()},
                         **{f"hd95_{k}": v["hd95_um"] for k, v in r["per_class"].items()},
                         **{f"volerr_{k}": v["volume_error_rel"] for k, v in r["per_class"].items()}})
        print(c.case_id, {n: round(rr["mean_dice_roi"], 3) for n, rr in zip(methods, rows[-len(methods):])}, flush=True)
    summary = {}
    for m in sorted({r["method"] for r in rows}):
        R = [r for r in rows if r["method"] == m]
        summary[m] = {k: mean_ci([r[k] for r in R]) for k in
                      ("mineral_dice", "mean_dice_roi", "dice_new_bone", "dice_graft", "seconds")}
        summary[m]["by_material_graft_dice"] = {mat: float(np.mean([r["dice_graft"] for r in R if r["material"] == mat]))
                                                for mat in sorted({r["material"] for r in R})}
    save_result("exp_A_baselines", {"experiment": "A", "n_test_specimens": len(test), "rf_train_seconds": rf_train_s,
                                    "t_fixed": t_fixed, "t_graft_fixed": t_graft_fixed,
                                    "summary": summary, "rows": rows,
                                    "notes": "True ROI supplied to all methods. Synthetic data only."})
    return summary


if __name__ == "__main__":
    s = run()
    for m, v in s.items():
        print(f"{m:24s} mineral {v['mineral_dice']['mean']:.3f}  meanDiceROI {v['mean_dice_roi']['mean']:.3f} "
              f"new {v['dice_new_bone']['mean']:.3f} graft {v['dice_graft']['mean']:.3f}  {v['seconds']['mean']:.2f}s")
