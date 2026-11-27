"""Experiment N — histology module evaluation.

N1 (synthetic, known truth): axial label slices from synthetic phantoms rendered as pseudo-H&E
   (decalcified: graft appears as unstained voids) with lab-to-lab stain-vector jitter. Measure
   bone area fraction (new+host) and graft (void) area fraction vs truth, with and without
   Macenko colour normalisation. Tests colour robustness only — NOT biological validity.
N2 (2D–3D registration): an oblique micro-CT plane (tilt 0–8°) of the same phantom vs its
   pseudo-histology section with simulated processing shrinkage (scale 0.85–0.95), rotation and
   translation. 2D affine registration; Dice of bone masks before/after.
N3 (real labels): NuInsSeg (Zenodo 10.5281/zenodo.10518968, CC-BY-4.0) H&E tiles with manual
   nuclei masks — classical nuclei segmentation (haematoxylin deconvolution + watershed):
   pixel Dice and object-level F1 at IoU ≥ 0.5. (Not bone tissue; validates the nuclei component.)
Optional: --wsi <ome.tiff> runs tissue detection + quantification on a real bone WSI (descriptive).
"""
import glob
import sys
import zipfile
from pathlib import Path

import numpy as np
from scipy import ndimage as ndi

from common import ROOT, save_result, FIG
from osteoquant.histology import (synthetic_section, quantify_he, macenko_normalize, oblique_slice, register_2d,
                                  deconvolve, nuclei, HE)
from osteoquant.phantom import PhantomConfig, generate_phantom

rng = np.random.default_rng(11)
out = {"experiment": "N", "N1": [], "N2": [], "N3": {}}
# ---------------------------------------------------------------- N1
phs = [generate_phantom(PhantomConfig(model="condyle", shape=(48, 96, 96), voxel_um=40, supersample=1,
                                      defect_diameter_um=2600, graft_material="beta_tcp", healing_stage=float(s),
                                      seed=1300 + i, periodic_texture=False)) for i, s in enumerate((0.3, 0.5, 0.7, 0.85))]
for i, ph in enumerate(phs):
    for z in (16, 24, 32):
        lab = ph.labels[z]
        up = np.kron(lab, np.ones((4, 4), np.uint8))   # 10 µm "histology" pixels
        roi = np.kron(ph.roi_mask[z], np.ones((4, 4), bool))
        rgb = synthetic_section(up, rng, stain_jitter=0.25)
        true_bone = float(np.isin(up[roi], (1, 3)).mean())
        true_graft = float((up[roi] == 2).mean())
        for norm in (False, True):
            img = macenko_normalize(rgb) if norm else rgb
            q, masks = quantify_he(img, roi=roi | (up == 2) & roi)
            meas_bone = float(masks["bone"][roi].mean())
            meas_graft = float(masks["graft"][roi].mean())
            out["N1"].append({"phantom": i, "z": z, "macenko": norm, "bone_true": true_bone, "bone_meas": meas_bone,
                              "graft_true": true_graft, "graft_meas": meas_graft})
from osteoquant.stats import agreement_summary
N1s = {}
for norm in (False, True):
    R = [r for r in out["N1"] if r["macenko"] == norm]
    N1s["macenko" if norm else "raw"] = {"bone": agreement_summary([r["bone_true"] for r in R], [r["bone_meas"] for r in R]),
                                         "graft": agreement_summary([r["graft_true"] for r in R], [r["graft_meas"] for r in R])}
out["N1_summary"] = {k: {c: {"icc": v[c]["icc_2_1"]["icc"], "mae": v[c]["mae"], "bias": v[c]["bland_altman"]["bias"]}
                         for c in ("bone", "graft")} for k, v in N1s.items()}
print("N1", out["N1_summary"], flush=True)

# ---------------------------------------------------------------- N2
for i, ph in enumerate(phs):
    vol_bone = np.isin(ph.labels, (1, 3)).astype(np.float32)
    tilt = rng.uniform(0, 8)
    normal = [np.cos(np.deg2rad(tilt)), np.sin(np.deg2rad(tilt)), 0]
    ct = oblique_slice(vol_bone, (24, 48, 48), normal, 90) > 0.5
    histo_lab = oblique_slice(ph.labels.astype(np.float32), (24, 48, 48), normal, 90, ) .round().astype(np.uint8)
    # processing: shrink + rotate + translate the section
    s = rng.uniform(0.85, 0.95); th = rng.uniform(-10, 10); t = rng.uniform(-4, 4, 2)
    c, sn = np.cos(np.deg2rad(th)), np.sin(np.deg2rad(th))
    A = np.array([[c, -sn], [sn, c]]) / s
    centre = np.array(histo_lab.shape) / 2
    off = centre - A @ centre + t
    deformed = ndi.affine_transform(histo_lab, A, offset=off, order=0)
    rgb = synthetic_section(deformed, rng, 0.15)
    hb = deconvolve(rgb, HE)[..., 1]
    hist_bone = (hb > np.percentile(hb, 60)) & np.isin(deformed, (1, 3))  # idealised bone map from stain
    before = 2 * (ct & hist_bone).sum() / (ct.sum() + hist_bone.sum())
    reg, _ = register_2d(ct.astype(np.float32), hist_bone.astype(np.float32), "affine")
    after = 2 * (ct & (reg > 0.5)).sum() / (ct.sum() + (reg > 0.5).sum())
    out["N2"].append({"phantom": i, "tilt_deg": tilt, "shrink": s, "rot_deg": th, "dice_before": float(before), "dice_after": float(after)})
    print("N2", out["N2"][-1], flush=True)

# ---------------------------------------------------------------- N3 (real nuclei labels)
zp = ROOT / "data" / "raw" / "zenodo_10518968_nuinsseg" / "NuInsSeg.zip"
if zp.exists() and zipfile.is_zipfile(zp):
    from PIL import Image
    import io as _io
    z = zipfile.ZipFile(zp)
    names = z.namelist()
    imgs = sorted(n for n in names if "/tissue images/" in n and n.lower().endswith((".png", ".tif", ".jpg")))
    rows = []
    for n in imgs[:: max(1, len(imgs) // 60)][:60]:
        stem = Path(n).stem
        cand = [m for m in names if "/label masks" in m and Path(m).stem == stem]
        if not cand:
            continue
        rgb = np.array(Image.open(_io.BytesIO(z.read(n))).convert("RGB"))
        gt = np.array(Image.open(_io.BytesIO(z.read(cand[0]))))
        if gt.ndim == 3:
            gt = gt[..., 0]
        h = deconvolve(rgb, HE)[..., 0]
        lab, info = nuclei(h)
        p, t = lab > 0, gt > 0
        dice = 2 * (p & t).sum() / max(1, p.sum() + t.sum())
        # object-level F1 at IoU>=0.5
        tp = 0
        gids = [g for g in np.unique(gt) if g > 0]
        for g in gids:
            gm = gt == g
            ov = lab[gm]
            ov = ov[ov > 0]
            if ov.size == 0:
                continue
            k = np.bincount(ov).argmax()
            pm = lab == k
            iou = (gm & pm).sum() / (gm | pm).sum()
            tp += iou >= 0.5
        npred = len(np.unique(lab)) - 1
        f1 = 2 * tp / max(1, len(gids) + npred)
        organ = n.split("/")[1] if "/" in n else ""
        rows.append({"image": n, "organ": organ, "pixel_dice": float(dice), "object_f1_iou50": float(f1),
                     "n_true": len(gids), "n_pred": int(npred)})
    out["N3"] = {"dataset": "NuInsSeg, Zenodo 10.5281/zenodo.10518968, CC-BY-4.0", "n_images": len(rows), "rows": rows,
                 "mean_pixel_dice": float(np.mean([r["pixel_dice"] for r in rows])) if rows else None,
                 "mean_object_f1": float(np.mean([r["object_f1_iou50"] for r in rows])) if rows else None}
    print("N3", {k: v for k, v in out["N3"].items() if k != "rows"}, flush=True)
else:
    out["N3"] = {"status": "blocked: NuInsSeg not downloaded"}
if "--wsi" in sys.argv:
    from osteoquant.histology import wsi_read, wsi_levels
    f = sys.argv[sys.argv.index("--wsi") + 1]
    rgb = wsi_read(f, level=-1)
    q, _ = quantify_he(rgb)
    out["wsi"] = {"file": f, "levels": [list(l) for l in wsi_levels(f)], "quantification": q}
save_result("exp_N_histology", out)
