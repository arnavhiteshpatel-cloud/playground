"""Experiment G — morphometry numerical verification.

Part 1 (analytic truth): plates, rods, spheres and tubes at structure sizes from 2 to 24 voxels.
  Metrics: relative error of Tb.Th / Tb.Sp (interior), BV/TV, BS (sphere), β1 (exact).
Part 2 (external reference): Zenodo 10.5281/zenodo.11061947 (CC-BY-4.0) — 8 segmented
  trabecular micro-CT cubes with Scanco IPL distance-transform thickness and separation maps.
  OsteoQuant Tb.Th/Tb.Sp computed on the same segmentations; agreement vs IPL by ICC(2,1),
  Bland–Altman and mean relative difference (n = 8 specimens).
"""
from __future__ import annotations

import glob
import time

import nibabel as nib
import numpy as np

from common import ROOT, save_result, FIG
from osteoquant.morphometry import (local_thickness, trabecular_morphometry, surface_area_mm2, volume_mm3,
                                    euler_connectivity)
from osteoquant.morphometry.analytic import plates, rods, sphere, hollow_cylinder, torus_count_phantom
from osteoquant.stats import icc, bland_altman, agreement_summary


def interior_mean(m, th, k):
    s = (slice(k, -k),) * 3
    return float(th[s][m[s]].mean())


def part1():
    rows = []
    for t in (2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24):
        s = 2 * t
        n = max(60, 4 * (t + s))
        p = plates((n, n, n), t, s)
        th, sp = local_thickness(p, 1.0, border="background"), local_thickness(~p, 1.0, border="background")
        k = n // 4
        rows.append({"object": "plate", "true_um": t, "measured_um": interior_mean(p, th, k),
                     "true_sp": s, "measured_sp": interior_mean(~p, sp, k), "bvtv_true": t / (t + s),
                     "bvtv_meas": float(p.mean())})
    for d in (3, 4, 5, 6, 8, 10, 14, 20):
        n = max(64, 4 * d)
        r = rods((n, n, n), d, 2 * d + 4)
        th = local_thickness(r, 1.0, border="background")
        rows.append({"object": "rod", "true_um": d, "measured_um": interior_mean(r, th, n // 5)})
    for w in (3, 5, 8, 12):
        tb = hollow_cylinder((30, 120, 120), 50, 50 - w)
        rows.append({"object": "tube_wall", "true_um": w, "measured_um": interior_mean(tb, local_thickness(tb, 1.0, border="background"), 6)})
    for rr in (5, 10, 20, 30):
        n = 2 * rr + 10
        m = sphere((n, n, n), ((n - 1) / 2,) * 3, rr)
        rows.append({"object": "sphere", "radius_vox": rr,
                     "volume_rel_err": volume_mm3(m, (1000,) * 3) / (4 / 3 * np.pi * rr ** 3) - 1,
                     "surface_rel_err": surface_area_mm2(m, (1000,) * 3) / (4 * np.pi * rr ** 2) - 1})
    conn = [{"holes": h, "beta1": euler_connectivity(torus_count_phantom((30, 40, 80), h))["beta1"]} for h in (0, 1, 2, 5, 8)]
    for r in rows:
        if "true_um" in r:
            r["rel_err"] = r["measured_um"] / r["true_um"] - 1
    return rows, conn


def part2():
    d = ROOT / "data" / "raw" / "zenodo_11061947_trab_tbth"
    out = []
    for f in sorted(glob.glob(str(d / "*_SEG_SUB.nii"))):
        base = f[:-4]
        img = nib.load(f)
        seg = np.asanyarray(img.dataobj) > 0
        vox_um = float(img.header.get_zooms()[0]) * 1000
        ipl_th = np.asanyarray(nib.load(base + "_DT_THICK_CONVERT.nii").dataobj)
        ipl_sp = np.asanyarray(nib.load(base + "_DT_SP_CONVERT.nii").dataobj)
        t = time.time()
        r = trabecular_morphometry(seg, np.ones_like(seg), vox_um, border="edge")
        dt = time.time() - t
        rb = trabecular_morphometry(seg, np.ones_like(seg), vox_um, border="background", compute_conn=False)
        out.append({"sample": base.split("/")[-1], "voxel_um": vox_um, "BV_TV": r["BV_TV"],
                    "TbTh_oq_um": r["Tb_Th_um"], "TbTh_ipl_um": float(ipl_th[seg].mean() * 1000),
                    "TbSp_oq_um": r["Tb_Sp_um"], "TbSp_ipl_um": float(ipl_sp[~seg].mean() * 1000),
                    "TbN_oq_per_mm": r["Tb_N_per_mm"], "TbTh_oq_bgborder_um": rb["Tb_Th_um"],
                    "TbSp_oq_bgborder_um": rb["Tb_Sp_um"], "ConnD_oq": r["Conn_D_per_mm3"], "seconds": dt})
        print(out[-1], flush=True)
    th = agreement_summary([o["TbTh_ipl_um"] for o in out], [o["TbTh_oq_um"] for o in out])
    sp = agreement_summary([o["TbSp_ipl_um"] for o in out], [o["TbSp_oq_um"] for o in out])
    thb = agreement_summary([o["TbTh_ipl_um"] for o in out], [o["TbTh_oq_bgborder_um"] for o in out])
    spb = agreement_summary([o["TbSp_ipl_um"] for o in out], [o["TbSp_oq_bgborder_um"] for o in out])
    return out, {"TbTh": th, "TbSp": sp, "TbTh_background_border": thb, "TbSp_background_border": spb}


def plot(rows, ext):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 3, figsize=(14, 3.8))
    for obj, c in (("plate", "#0072B2"), ("rod", "#E69F00"), ("tube_wall", "#009E73")):
        R = [r for r in rows if r["object"] == obj]
        ax[0].plot([r["true_um"] for r in R], [100 * r["rel_err"] for r in R], "o-", color=c, label=obj)
    ax[0].axhline(0, color="k", lw=0.8); ax[0].axhspan(-10, 10, color="grey", alpha=0.12)
    ax[0].set_xlabel("true thickness (voxels)"); ax[0].set_ylabel("Tb.Th error (%)"); ax[0].legend(); ax[0].grid(alpha=.3)
    ax[0].set_title("Analytic objects: thickness error vs size")
    for k, (key, lab) in enumerate((("TbTh", "Tb.Th"), ("TbSp", "Tb.Sp"))):
        a = [o[f"{key}_ipl_um"] for o in ext]; b = [o[f"{key}_oq_um"] for o in ext]
        axx = ax[1 + k]
        axx.scatter(a, b, color="#0072B2")
        lo, hi = min(a + b) * 0.95, max(a + b) * 1.05
        axx.plot([lo, hi], [lo, hi], "k--", lw=0.8)
        axx.set_xlabel(f"Scanco IPL {lab} (µm)"); axx.set_ylabel(f"OsteoQuant {lab} (µm)"); axx.grid(alpha=.3)
        axx.set_title(f"{lab}: OsteoQuant vs IPL (n={len(a)})")
    fig.tight_layout(); fig.savefig(FIG / "exp_G_morphometry.png", dpi=110)


if __name__ == "__main__":
    rows, conn = part1()
    ext, agree = part2()
    save_result("exp_G_morphometry", {"experiment": "G", "analytic": rows, "connectivity": conn, "external_ipl": ext,
                                      "agreement_vs_ipl": agree,
                                      "dataset": "Zenodo 10.5281/zenodo.11061947 (CC-BY-4.0)"})
    plot(rows, ext)
    for k, v in agree.items():
        print(k, "ICC(2,1)", round(v["icc_2_1"]["icc"], 3), "mean rel err", round(v["mean_rel_error"], 4),
              "BA bias", round(v["bland_altman"]["bias"], 2))
