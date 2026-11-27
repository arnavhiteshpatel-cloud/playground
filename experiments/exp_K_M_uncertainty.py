"""Experiments K and M — uncertainty-based selective segmentation and simulated human correction.

K. Hypothesis: voxel uncertainty (1 − max softmax with test-time augmentation) ranks errors, so
   deferring the least-confident voxels to a reviewer raises accuracy on the remainder; scan-level
   uncertainty flags out-of-distribution scans (held-out materials).
   Data: synth test (16, in-distribution) and ood_mat test (16). Model: unet_ctx_s0 (+4-flip TTA).
   Metrics: risk–coverage curve, AURC, ECE before/after temperature scaling (fitted on val),
   AUROC of scan-level mean entropy for ID vs OOD, failure-detection sensitivity for scans with
   graft Dice < 0.8.
M. Simulated correction: a reviewer corrects exactly the deferred voxels (best case). We report
   accuracy/Dice after review vs fraction deferred, and convert to a *modelled* reviewer effort
   using slices that contain deferred voxels. Effort model (ASSUMPTION, to be replaced by timed
   user studies): 20 s per axial slice inspected with deferred voxels, vs 90 s per slice for full
   manual delineation of the defect ROI. These constants are illustrative, not measured.
"""
import numpy as np
from common import load_split, save_result
from osteoquant.ml.train import load_model, predict_proba
from osteoquant.uncertainty import predictive_entropy, risk_coverage, temperature_scale
from osteoquant.segment.metrics import multiclass_metrics, expected_calibration_error

model, ck = load_model("unet_ctx_s0")
cfg = ck["cfg"]
SEC_REVIEW_SLICE, SEC_MANUAL_SLICE = 20.0, 90.0


def run(cases, tag):
    rows, curves = [], []
    for c in cases:
        p = predict_proba(model, c, cfg, tta=True)
        pred = p.argmax(0)
        ent = predictive_entropy(p)
        mineral = c.roi & (c.labels > 0)
        r = multiclass_metrics(pred.astype(np.uint8), c.labels, spacing=c.spacing, mask=c.roi, classes=(1, 2), distances=False)
        rc = risk_coverage(p, c.labels, c.roi, coverages=(1.0, 0.95, 0.9, 0.85, 0.8, 0.7))
        # effort model: slices (axial) containing deferred voxels at 90% coverage
        unc = 1 - p.max(0)
        thr = np.quantile(unc[c.roi], 0.9)
        deferred = c.roi & (unc > thr)
        n_slices_def = int(deferred.any(axis=(1, 2)).sum())
        n_slices_roi = int(c.roi.any(axis=(1, 2)).sum())
        rows.append({"case": c.case_id, "set": tag, "material": c.meta["spec"]["material"],
                     "dice_graft": r["per_class"]["graft"]["dice"], "dice_new": r["per_class"]["new_bone"]["dice"],
                     "mean_entropy_roi": float(ent[c.roi].mean()), "mean_entropy_mineral": float(ent[mineral].mean()),
                     "ece_roi": expected_calibration_error(p, c.labels, mask=c.roi)["ece"], "aurc": rc["aurc"],
                     "review_minutes_90cov": n_slices_def * SEC_REVIEW_SLICE / 60,
                     "manual_minutes_full": n_slices_roi * SEC_MANUAL_SLICE / 60})
        curves.append(rc["rows"])
        print(tag, c.case_id, {k: round(v, 3) for k, v in rows[-1].items() if isinstance(v, float)}, flush=True)
    return rows, curves


def auroc(neg, pos):
    neg, pos = np.asarray(neg), np.asarray(pos)
    return float(np.mean([(p > n) + 0.5 * (p == n) for p in pos for n in neg]))


if __name__ == "__main__":
    test = load_split("test")
    ood = load_split("ood_mat")[24:40]
    val = load_split("val")
    # temperature scaling on validation logits (log of probs is a valid surrogate for logits up to a constant)
    lg, ys, ms = [], [], []
    for c in val:
        p = predict_proba(model, c, cfg)
        lg.append(np.log(np.clip(p, 1e-8, 1))); ys.append(c.labels.astype(int)); ms.append(c.roi)
    T = temperature_scale(lg, ys, ms)
    r_id, c_id = run(test, "in_distribution")
    r_ood, c_ood = run(ood, "ood_material")
    def agg(curves):
        out = []
        for j in range(len(curves[0])):
            out.append({k: float(np.mean([c[j][k] for c in curves])) for k in curves[0][j]})
        return out
    fails = [r for r in r_id + r_ood if r["dice_graft"] < 0.8]
    ok = [r for r in r_id + r_ood if r["dice_graft"] >= 0.8]
    thr = np.quantile([r["mean_entropy_mineral"] for r in r_id], 0.9)  # flag scans above ID 90th percentile
    sens = float(np.mean([r["mean_entropy_mineral"] > thr for r in fails])) if fails else float("nan")
    spec = float(np.mean([r["mean_entropy_mineral"] <= thr for r in ok])) if ok else float("nan")
    res = {"experiment": "K/M", "temperature_fit_on_val": T, "rows": r_id + r_ood,
           "risk_coverage_id": agg(c_id), "risk_coverage_ood": agg(c_ood),
           "auroc_entropy_id_vs_ood": auroc([r["mean_entropy_mineral"] for r in r_id], [r["mean_entropy_mineral"] for r in r_ood]),
           "failure_detection": {"definition": "scan graft Dice < 0.8", "n_fail": len(fails), "n_ok": len(ok),
                                 "flag_threshold_entropy": float(thr), "sensitivity": sens, "specificity": spec},
           "effort_model": {"sec_per_review_slice": SEC_REVIEW_SLICE, "sec_per_manual_slice": SEC_MANUAL_SLICE,
                            "status": "ASSUMED constants — not measured",
                            "mean_review_min_90cov": float(np.mean([r["review_minutes_90cov"] for r in r_id + r_ood])),
                            "mean_manual_min": float(np.mean([r["manual_minutes_full"] for r in r_id + r_ood]))}}
    em = res["effort_model"]
    em["modelled_time_reduction"] = 1 - em["mean_review_min_90cov"] / em["mean_manual_min"]
    save_result("exp_K_M_uncertainty", res)
    print({k: v for k, v in res.items() if k not in ("rows",)})
