"""Experiments C/D/E — material-separability benchmark.

C: graft vs new-bone intensity overlap × noise. The graft is modelled as a mineral phase with
   HA-equivalent density X (mgHA/cm³) swept from far above to below the new-bone range
   (new bone: 650–1000 mgHA/cm³ depending on maturity). Noise σ swept.
D: voxel-resolution sensitivity (block-mean downsampling ×1, ×2, ×3 of the 20 µm render).
E: artefact robustness (rings, cupping, scanner gain/offset shift) at a fixed contrast.

Methods: multi-Otsu (material-aware ordering), GMM, Random Forest (trained on one phantom per
condition, tested on three others), and the **intensity-only Bayes bound**: the accuracy of the
optimal voxel-wise classifier that sees only the (noisy) intensity, fitted on the *test*
volumes' true class-conditional histograms (an oracle upper bound for any intensity-only
method). If a context-using method (RF with multi-scale texture/shape features) exceeds the
bound, spatial context carries information beyond intensity — in this simulation.
All evaluation in the true defect ROI among mineralised voxels (graft vs new bone).
"""
from __future__ import annotations

import time

import numpy as np

from common import save_result, FIG
from osteoquant.phantom import PhantomConfig, generate_phantom, ImagingConfig, render_fast, downsample_labels
from osteoquant.phantom.materials import Material
from osteoquant.segment import classical as C

SHAPE = (56, 72, 72)
VOX = 20.0  # render at 20 µm so resolution can be degraded in D


def make_structures(n=4):
    phs = []
    for s in range(n):
        cfg = PhantomConfig(model="condyle", shape=SHAPE, voxel_um=VOX * 2, supersample=2, defect_diameter_um=2000,
                            graft_material="ha", graft_diam_um=(300, 600), healing_stage=0.55, seed=500 + s)
        # generate at 40 µm then we treat fractions at 40 µm; for resolution experiment we re-render
        phs.append(generate_phantom(cfg))
    return phs


def mu_with_graft(ph, X):
    E = ph.config.effective_energy_keV
    g_old = float(np.ravel(ph.materials["ha"].mu(E))[0])
    g_new = float(np.ravel(Material("g", 2, mineral_mgHA_cm3=X).mu(E))[0])
    mf = ph.material_fractions["ha"]
    return ph.mu - mf * g_old + mf * g_new


def bayes_bound(x, y, mask, bins=128):
    """Max achievable accuracy (graft vs new bone) of any intensity-only rule on this data."""
    v, t = x[mask], y[mask]
    edges = np.linspace(np.percentile(v, 0.5), np.percentile(v, 99.5), bins + 1)
    h1, _ = np.histogram(v[t == 1], edges)
    h2, _ = np.histogram(v[t == 2], edges)
    acc = (np.maximum(h1, h2).sum()) / max(1, (h1.sum() + h2.sum()))
    # Dice-equivalent of bound classifier for graft
    pred_g = np.digitize(v, edges[1:-1])
    rule = h2 > h1
    pg = rule[np.clip(pred_g, 0, bins - 1)]
    tp = np.sum(pg & (t == 2))
    dice_g = 2 * tp / (pg.sum() + (t == 2).sum())
    tpn = np.sum(~pg & (t == 1))
    dice_n = 2 * tpn / ((~pg).sum() + (t == 1).sum())
    return float(acc), float(dice_g), float(dice_n)


def gn_scores(pred, y, mask):
    m = mask & ((y == 1) | (y == 2))
    p, t = pred[m], y[m]
    acc = float(np.mean(p == t))
    dg = 2 * np.sum((p == 2) & (t == 2)) / max(1, np.sum(p == 2) + np.sum(t == 2))
    dn = 2 * np.sum((p == 1) & (t == 1)) / max(1, np.sum(p == 1) + np.sum(t == 1))
    return acc, float(dg), float(dn)


def eval_condition(phs, X, imaging, down=1, train_idx=0, new_mean=850.0):
    vols, labs, rois = [], [], []
    for i, ph in enumerate(phs):
        mu = mu_with_graft(ph, X)
        v = render_fast(mu, ph.config.voxel_um, ImagingConfig(seed=10 + i, downsample=down, **imaging)).data
        lab = downsample_labels(ph.labels, down)
        roi = downsample_labels(ph.roi_mask.astype(np.uint8), down).astype(bool)
        vols.append(v); labs.append(lab); rois.append(roi)
    sp = (ph.config.voxel_um * down,) * 3
    brighter = X > new_mean
    res = {"multiotsu": [], "gmm": [], "rf": [], "bayes_intensity_bound": []}
    rf = C.RFSegmenter(n_estimators=40, max_depth=16, seed=0,
                       scales_um=(0, 40 * down, 80 * down, 160 * down)).fit(
        [vols[train_idx]], [labs[train_idx]], [sp], [rois[train_idx]], n_per_class=20000)
    for i in range(len(phs)):
        if i == train_idx:
            continue
        x, y, roi = vols[i], labs[i], rois[i]
        mineral = roi & (y > 0)
        res["bayes_intensity_bound"].append(bayes_bound(x, y, mineral & ((y == 1) | (y == 2))))
        res["multiotsu"].append(gn_scores(C.seg_multiotsu(x, roi, brighter)[0], y, roi))
        res["gmm"].append(gn_scores(C.seg_gmm(x, roi, brighter)[0], y, roi))
        res["rf"].append(gn_scores(rf.predict(x, sp, roi)[0], y, roi))
    return {k: {"acc": float(np.mean([r[0] for r in v])), "dice_graft": float(np.mean([r[1] for r in v])),
                "dice_new": float(np.mean([r[2] for r in v])), "n_test": len(v)} for k, v in res.items()}


def main():
    t0 = time.time()
    phs = make_structures(4)
    print("structures", round(time.time() - t0, 1), "s", flush=True)
    E = phs[0].config.effective_energy_keV
    # reference HA-equivalent of new bone range for reporting
    out = {"experiment": "C/D/E", "shape": SHAPE, "voxel_um": phs[0].config.voxel_um,
           "new_bone_mineral_range_mgHA": list(phs[0].config.woven_mineral), "host_mgHA": [1000, 1150],
           "C": [], "D": [], "E": []}
    Xs = [2200, 1600, 1300, 1150, 1000, 900, 800, 650]
    sigmas = [30, 80, 150, 250]
    for X in Xs:
        for s in sigmas:
            r = eval_condition(phs, X, dict(psf_sigma_um=20, noise_sigma=s))
            out["C"].append({"graft_mgHA": X, "noise_sigma": s, **{f"{k}_{m}": v[m] for k, v in r.items()
                                                                     for m in ("acc", "dice_graft", "dice_new")}})
            print("C", X, s, {k: round(v["dice_graft"], 3) for k, v in r.items()}, flush=True)
    # D: resolution (at moderate contrast X=1300 and X=1600, noise 80)
    for X in (1600, 1300):
        for down in (1, 2, 3):
            r = eval_condition(phs, X, dict(psf_sigma_um=20, noise_sigma=80), down=down)
            out["D"].append({"graft_mgHA": X, "voxel_um": phs[0].config.voxel_um * down,
                             **{f"{k}_{m}": v[m] for k, v in r.items() for m in ("acc", "dice_graft", "dice_new")}})
            print("D", X, down, {k: round(v["dice_graft"], 3) for k, v in r.items()}, flush=True)
    # E: artefacts at X=1600, noise 80
    arts = {"none": {}, "rings_strong": dict(ring_amplitude=150), "cupping_20pct": dict(cupping=0.2),
            "gain_shift_test_only": "shift", "blur_60um": dict(psf_sigma_um=60)}
    for name, a in arts.items():
        if a == "shift":
            # RF trained on unshifted, tested on gain 1.25 / offset +150 (cross-scanner shift)
            r = eval_shift(phs, 1600)
        else:
            img = dict(psf_sigma_um=20, noise_sigma=80)
            img.update(a)
            r = eval_condition(phs, 1600, img)
        out["E"].append({"artefact": name, **{f"{k}_{m}": v[m] for k, v in r.items() for m in ("acc", "dice_graft", "dice_new")}})
        print("E", name, {k: round(v["dice_graft"], 3) for k, v in r.items()}, flush=True)
    out["seconds"] = round(time.time() - t0, 1)
    save_result("exp_C_D_E_separability", out)
    plot(out)


def eval_shift(phs, X):
    """Train RF on standard rendering, test on gain/offset shifted rendering (no re-normalisation)
    and with percentile re-normalisation (harmonisation)."""
    from osteoquant.ml.train import normalize_image
    vols0, volsS, labs, rois = [], [], [], []
    for i, ph in enumerate(phs):
        mu = mu_with_graft(ph, X)
        vols0.append(render_fast(mu, ph.config.voxel_um, ImagingConfig(seed=10 + i, psf_sigma_um=20, noise_sigma=80)).data)
        volsS.append(render_fast(mu, ph.config.voxel_um, ImagingConfig(seed=10 + i, psf_sigma_um=20, noise_sigma=80,
                                                                         scale=1.25, shift=150)).data)
        labs.append(ph.labels); rois.append(ph.roi_mask)
    sp = (phs[0].config.voxel_um,) * 3
    rf = C.RFSegmenter(n_estimators=40, max_depth=16, seed=0).fit([vols0[0]], [labs[0]], [sp], [rois[0]], 20000)
    rfn = C.RFSegmenter(n_estimators=40, max_depth=16, seed=0).fit([normalize_image(vols0[0])], [labs[0]], [sp], [rois[0]], 20000)
    res = {"rf_raw_shifted": [], "rf_normalized_shifted": [], "multiotsu": [], "bayes_intensity_bound": []}
    for i in range(1, len(phs)):
        x, y, roi = volsS[i], labs[i], rois[i]
        res["rf_raw_shifted"].append(gn_scores(rf.predict(x, sp, roi)[0], y, roi))
        res["rf_normalized_shifted"].append(gn_scores(rfn.predict(normalize_image(x), sp, roi)[0], y, roi))
        res["multiotsu"].append(gn_scores(C.seg_multiotsu(x, roi, True)[0], y, roi))
        res["bayes_intensity_bound"].append(bayes_bound(x, y, roi & ((y == 1) | (y == 2))))
    return {k: {"acc": float(np.mean([r[0] for r in v])), "dice_graft": float(np.mean([r[1] for r in v])),
                "dice_new": float(np.mean([r[2] for r in v])), "n_test": len(v)} for k, v in res.items()}


def plot(out):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    C_ = out["C"]
    Xs = sorted({r["graft_mgHA"] for r in C_}, reverse=True)
    sig = sorted({r["noise_sigma"] for r in C_})
    fig, axs = plt.subplots(1, len(sig), figsize=(4.2 * len(sig), 3.6), sharey=True)
    cols = {"bayes_intensity_bound": "#444444", "multiotsu": "#56B4E9", "gmm": "#009E73", "rf": "#E69F00"}
    for ax, s in zip(axs, sig):
        for k, c in cols.items():
            ys = [next(r for r in C_ if r["graft_mgHA"] == X and r["noise_sigma"] == s)[f"{k}_acc"] for X in Xs]
            ax.plot(Xs, ys, "o-", color=c, label=k.replace("_", " "), lw=2 if k == "rf" else 1.3,
                    ls="--" if k.startswith("bayes") else "-")
        ax.axvspan(650, 1000, color="#E69F00", alpha=0.12)
        ax.set_title(f"noise σ = {s}")
        ax.set_xlabel("graft HA-equivalent density (mgHA/cm³)")
        ax.invert_xaxis()
        ax.set_ylim(0.4, 1.0)
        ax.grid(alpha=0.3)
    axs[0].set_ylabel("graft-vs-new-bone accuracy (ROI)")
    axs[0].legend(fontsize=8, loc="lower left")
    fig.suptitle("Experiment C (synthetic): separability vs graft/new-bone density overlap (shaded = new-bone range)")
    fig.tight_layout()
    fig.savefig(FIG / "exp_C_separability.png", dpi=110)


if __name__ == "__main__":
    main()
