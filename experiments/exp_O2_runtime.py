"""Experiment O2 — deployment runtime: PyTorch vs ONNX Runtime (fp32, static int8), patch overlap.

Model: unet_noctx_s0 (synthetic 3-class). Data: synthetic test split (16 specimens) for accuracy;
throughput on the same volumes. For each runtime/overlap: voxels per second (4 threads, wall clock,
median over specimens), agreement with the PyTorch overlap-0.5 reference (label agreement, max prob diff)
and graft-volume error vs truth (measurement-level effect, ADR-G2-05).
Int8 calibration uses 32 patches from TRAINING specimens only.
Note: wall-clock numbers depend on concurrent load on this 4-CPU machine; the run records the load average.
"""
import os
import time

import numpy as np

from common import load_split, save_result
from osteoquant.ml.runtime import OnnxSegmenter, export_onnx, quantize_int8_static
from osteoquant.ml.train import load_model, predict_proba, MODEL_DIR

NAME = "unet_noctx_s0"
if not (MODEL_DIR / f"{NAME}.onnx").exists():
    export_onnx(NAME)
if not (MODEL_DIR / f"{NAME}.int8.onnx").exists():
    quantize_int8_static(NAME, load_split("train", limit=12))
model, ck = load_model(NAME)
cfg = ck["cfg"]
fp32 = OnnxSegmenter(NAME)
int8 = OnnxSegmenter(NAME, quantized=True)
cases = load_split("test")
rows = []
for c in cases:
    t = time.time(); ref = predict_proba(model, c, cfg, overlap=0.5); t_ref = time.time() - t
    nvox = c.image.size
    variants = {"torch_ov0.5": (ref, t_ref)}
    t = time.time(); p = predict_proba(model, c, cfg, overlap=0.25); variants["torch_ov0.25"] = (p, time.time() - t)
    for nm, seg in (("ort_fp32", fp32), ("ort_int8", int8)):
        for ov in (0.5, 0.25):
            t = time.time(); p = seg.predict_proba(c, cfg, overlap=ov); variants[f"{nm}_ov{ov}"] = (p, time.time() - t)
    vt = float(((c.labels == 2) & c.roi).sum())
    for k, (p, dt) in variants.items():
        lab = p.argmax(0)
        rows.append({"case": c.case_id, "variant": k, "voxels_per_s": nvox / dt,
                     "label_agreement_vs_ref": float((lab == ref.argmax(0)).mean()),
                     "max_prob_diff_vs_ref": float(np.abs(p - ref).max()),
                     "graft_vol_err": float(((lab == 2) & c.roi).sum() / vt - 1) if vt else None})
    print(c.case_id, {r["variant"]: round(r["voxels_per_s"]) for r in rows[-6:]}, flush=True)
summ = {}
for k in {r["variant"] for r in rows}:
    rr = [r for r in rows if r["variant"] == k]
    summ[k] = {"median_voxels_per_s": float(np.median([r["voxels_per_s"] for r in rr])),
               "min_label_agreement": float(np.min([r["label_agreement_vs_ref"] for r in rr])),
               "mean_abs_graft_vol_err": float(np.mean([abs(r["graft_vol_err"]) for r in rr]))}
print(summ)
save_result("exp_O2_runtime", {"experiment": "O2", "summary": summ, "rows": rows, "loadavg": os.getloadavg(),
                               "onnx_files_mb": {p.name: round(p.stat().st_size / 1e6, 2) for p in MODEL_DIR.glob(f"{NAME}*.onnx")}})
