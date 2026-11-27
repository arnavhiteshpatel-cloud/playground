"""Experiment F — automatic defect-ROI detection accuracy.

Data: 36 synthetic phantoms (3 defect models × 3 noise levels × 4 seeds), supersample 1 for speed;
healing stage 0.3–0.8, beta-TCP or HA. Truth = exact geometric ROI from the generator.
Detectors: plate-gap detector (condyle, calvarial; with and without nominal diameter) and
segmental-gap detector. Metrics: ROI Dice, centre error (µm), radius error (%), extent error,
confidence, fraction requiring review (confidence < 0.6), failure rate (exception).
Also: real ovine distraction scans (no truth) — report detected gap and confidence only.
"""
import numpy as np
from common import save_result, ROOT
from osteoquant.phantom import PhantomConfig, generate_phantom, render_fast, ImagingConfig
from osteoquant.roi import detect_plate_defect, detect_segmental_gap, roi_dice, ROIDetectionError

SHAPES = {"condyle": (64, 80, 80), "calvarial": (40, 112, 112), "segmental": (80, 72, 72)}
rows = []
rng = np.random.default_rng(3)
for model in SHAPES:
    for noise in (40, 120, 250):
        for s in range(4):
            D = float(rng.choice([1600, 2000, 2400])) if model != "segmental" else 2000.0
            cfg = PhantomConfig(model=model, shape=SHAPES[model], voxel_um=40, supersample=1, defect_diameter_um=D,
                                graft_material=str(rng.choice(["beta_tcp", "ha"])), healing_stage=float(rng.uniform(0.3, 0.8)),
                                seed=1200 + s + 10 * int(noise), periodic_texture=False)
            ph = generate_phantom(cfg)
            img = render_fast(ph.mu, 40, ImagingConfig(psf_sigma_um=25, noise_sigma=noise, seed=s)).data
            variants = [("auto", None), ("nominal", D)] if model != "segmental" else [("auto", None)]
            for vname, nom in variants:
                rec = {"model": model, "noise": noise, "seed": s, "variant": vname, "true_diameter_um": D}
                try:
                    roi = detect_segmental_gap(img, (40,) * 3) if model == "segmental" else \
                        detect_plate_defect(img, (40,) * 3, model=model, nominal_diameter_um=nom)
                    m = roi.to_mask(img.shape, (40,) * 3)
                    tc = np.array(ph.roi["center_um"][1:], float)
                    ec = np.array(roi.params["center_um"][1:], float)
                    rec.update({"dice": roi_dice(m, ph.roi_mask), "center_err_um": float(np.linalg.norm(tc - ec)),
                                "radius_err_pct": 100 * (roi.params["radius_um"] / ph.roi["radius_um"] - 1),
                                "confidence": roi.confidence, "requires_review": bool(roi.diagnostics.get("requires_review")),
                                "failed": False})
                except ROIDetectionError as e:
                    rec.update({"failed": True, "error": str(e), "dice": 0.0})
                rows.append(rec)
                print(rec, flush=True)
# real data
real = []
for f in ("18DAYS_recon.txm", "161DAYS_recon.txm"):
    p = ROOT / "data" / "raw" / "zenodo_17255310" / f
    if p.exists():
        from osteoquant.io import read_volume
        v, _ = read_volume(p, step=8, do_hash=False)
        try:
            r = detect_segmental_gap(v.data, v.spacing)
            real.append({"scan": f, "gap_um": r.diagnostics["gap_length_um"], "slices": r.diagnostics["gap_slices"],
                         "radius_um": r.params["radius_um"], "confidence": r.confidence})
        except ROIDetectionError as e:
            real.append({"scan": f, "failed": str(e)})
summary = {}
for model in SHAPES:
    for vname in ("auto", "nominal"):
        R = [r for r in rows if r["model"] == model and r["variant"] == vname]
        if not R:
            continue
        ok = [r for r in R if not r["failed"]]
        summary[f"{model}/{vname}"] = {"n": len(R), "failure_rate": 1 - len(ok) / len(R),
                                       "dice_mean": float(np.mean([r["dice"] for r in R])),
                                       "dice_min": float(np.min([r["dice"] for r in R])),
                                       "center_err_um_mean": float(np.mean([r["center_err_um"] for r in ok])) if ok else None,
                                       "radius_err_pct_mean_abs": float(np.mean([abs(r["radius_err_pct"]) for r in ok])) if ok else None,
                                       "review_flag_rate": float(np.mean([r["requires_review"] for r in ok])) if ok else None}
save_result("exp_F_roi", {"experiment": "F", "rows": rows, "summary": summary, "real_ovine": real})
for k, v in summary.items():
    print(k, v)
print(real)
