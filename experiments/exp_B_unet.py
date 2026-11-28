"""Experiment B — synthetic three-class 3D U-Net (and context ablation).

Hypothesis: a 3D CNN trained on synthetic phantoms segments new bone / graft / host bone on
held-out synthetic specimens better than classical baselines (Exp A), and an explicit ROI
context channel (signed distance to the defect boundary) improves host-vs-new-bone separation.
Data: synth/train (48), synth/val (8), synth/test (16). Split by specimen.
Models: unet_ctx (image + ROI signed-distance channel), unet_noctx (image only).
Metrics: per-class Dice/HD95 in ROI and whole volume, volume-fraction error vs truth, ECE.
All models are SYNTHETIC-TRAINED and labelled as such.
"""
from __future__ import annotations

import json
import sys
import time

import numpy as np

from common import load_split, save_result, mean_ci
from osteoquant.ml.train import train_model, load_model, predict_proba
from osteoquant.segment.metrics import multiclass_metrics, expected_calibration_error

ITERS = int(sys.argv[1]) if len(sys.argv) > 1 else 1500
BASE = dict(patch=(48, 48, 48), batch=2, iters=ITERS, lr=3e-3, base=12, levels=4, threads=4, log_every=100,
            val_every=500, loss={"dice": 1.0, "ce": 1.0, "boundary_w": 1.0}, eval_in_roi=False)


def evaluate(name, test, cfg):
    model, ck = load_model(name)
    rows = []
    for c in test:
        t = time.time()
        p = predict_proba(model, c, ck["cfg"], tta=False)
        dt = time.time() - t
        pred = p.argmax(0).astype(np.uint8)
        r_roi = multiclass_metrics(pred, c.labels, spacing=c.spacing, mask=c.roi, classes=(1, 2))
        r_all = multiclass_metrics(pred, c.labels, spacing=c.spacing, classes=(1, 2, 3), distances=False)
        ece = expected_calibration_error(p, c.labels, mask=c.roi)["ece"]
        tv = c.roi.sum()
        tr = c.meta["truth"]
        rows.append({"case": c.case_id, "material": c.meta["spec"]["material"], "model": c.meta["spec"]["model"],
                     "dice_new_roi": r_roi["per_class"]["new_bone"]["dice"], "dice_graft_roi": r_roi["per_class"]["graft"]["dice"],
                     "hd95_new_um": r_roi["per_class"]["new_bone"]["hd95_um"], "hd95_graft_um": r_roi["per_class"]["graft"]["hd95_um"],
                     "dice_host_all": r_all["per_class"]["host_bone"]["dice"], "dice_new_all": r_all["per_class"]["new_bone"]["dice"],
                     "dice_graft_all": r_all["per_class"]["graft"]["dice"], "ece_roi": ece, "infer_s": dt,
                     "new_frac_pred": float(((pred == 1) & c.roi).sum() / tv), "new_frac_true": tr["new_bone_fraction"],
                     "graft_frac_pred": float(((pred == 2) & c.roi).sum() / tv), "graft_frac_true": tr["graft_fraction"]})
    summ = {k: mean_ci([r[k] for r in rows]) for k in rows[0] if k not in ("case", "material", "model")}
    summ["by_material_graft_dice"] = {m: float(np.mean([r["dice_graft_roi"] for r in rows if r["material"] == m]))
                                      for m in sorted({r["material"] for r in rows})}
    return rows, summ


if __name__ == "__main__":
    train, val, test = load_split("train"), load_split("val"), load_split("test")
    out = {"experiment": "B", "n_train": len(train), "n_val": len(val), "n_test": len(test), "models": {}}
    for name, extra in [("unet_ctx_s0", {"roi_distance_channel": True, "seed": 0}),
                        ("unet_noctx_s0", {"roi_distance_channel": False, "seed": 0})]:
        cfg = dict(BASE, **extra)
        t = time.time()
        card = train_model(train, val[:4], cfg, name, log=lambda s: print(name, s, flush=True), overwrite=True)
        rows, summ = evaluate(name, test, cfg)
        out["models"][name] = {"train_seconds": time.time() - t, "sha256": card["sha256"], "n_params": card["n_params"],
                               "cfg": cfg, "history": card["history"], "summary": summ, "rows": rows}
        print(name, json.dumps({k: round(v["mean"], 3) for k, v in summ.items() if isinstance(v, dict) and "mean" in v}), flush=True)
        save_result("exp_B_unet", out)
