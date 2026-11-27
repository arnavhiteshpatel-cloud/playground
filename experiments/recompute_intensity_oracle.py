"""Correct the intensity-only reference (independent review finding Q-01).

The original `bayes_bound` reported the Dice of the *accuracy*-optimal rule, which is not an upper
bound on Dice (e.g. it predicts no graft when graft is the minority class). Here we compute the
**Dice-optimal intensity-only oracle**: with the test volume's true class-conditional histograms
(256 bins), every voxel-wise intensity rule is a union of bins; the Dice-maximising union is a
superlevel set of the likelihood ratio, found by sorting bins by graft fraction and scanning.
This is an upper bound (at this binning) for ANY method using voxel intensity alone.
Volumes are regenerated from the same seeds as Experiments C, C2 and L2 and results are patched.
"""
import json

import numpy as np

from common import RESULTS, save_result
from exp_C_separability import make_structures, mu_with_graft
from osteoquant.phantom import PhantomConfig, generate_phantom, ImagingConfig, render_fast, downsample_labels


def dice_oracle(x, y, mask, bins=256):
    m = mask & ((y == 1) | (y == 2))
    v, t = x[m], y[m]
    edges = np.linspace(np.percentile(v, 0.1), np.percentile(v, 99.9), bins + 1)
    b = np.clip(np.digitize(v, edges[1:-1]), 0, bins - 1)
    g = np.bincount(b[t == 2], minlength=bins).astype(float)
    n = np.bincount(b[t == 1], minlength=bins).astype(float)
    G = g.sum()
    if G == 0:
        return float("nan"), float("nan")
    order = np.argsort(-(g / np.maximum(g + n, 1)))
    tp, pp = np.cumsum(g[order]), np.cumsum((g + n)[order])
    dice = 2 * tp / (pp + G)
    k = int(np.argmax(dice))
    # the complementary new-bone Dice for the same rule
    sel = np.zeros(bins, bool); sel[order[:k + 1]] = True
    N = n.sum()
    tn_new = n[~sel].sum(); pred_new = (g + n)[~sel].sum()
    dice_new = 2 * tn_new / (pred_new + N) if (pred_new + N) else float("nan")
    return float(dice[k]), float(dice_new)


def main():
    out = {"experiment": "Q-01 correction", "C": [], "C2": [], "L2": []}
    phs = make_structures(4)
    C = json.loads((RESULTS / "exp_C_D_E_separability.json").read_text())
    for row in C["C"]:
        X, s = row["graft_mgHA"], row["noise_sigma"]
        vals = []
        for i in range(1, 4):
            v = render_fast(mu_with_graft(phs[i], X), 40, ImagingConfig(seed=10 + i, psf_sigma_um=20, noise_sigma=s)).data
            vals.append(dice_oracle(v, phs[i].labels, phs[i].roi_mask))
        row["intensity_oracle_dice_graft"] = float(np.mean([a for a, _ in vals]))
        row["intensity_oracle_dice_new"] = float(np.mean([b for _, b in vals]))
        out["C"].append({"graft_mgHA": X, "noise": s, "oracle_graft": row["intensity_oracle_dice_graft"],
                         "rf_graft": row["rf_dice_graft"], "multiotsu_graft": row["multiotsu_dice_graft"]})
        print("C", X, s, round(row["intensity_oracle_dice_graft"], 3), "rf", round(row["rf_dice_graft"], 3), flush=True)
    C["intensity_oracle_note"] = "bayes_intensity_bound_* fields are the accuracy-optimal rule (NOT a Dice bound); use intensity_oracle_dice_* (Q-01)"
    (RESULTS / "exp_C_D_E_separability.json").write_text(json.dumps(C, indent=1))
    # C2
    C2 = json.loads((RESULTS / "exp_C2_ablation.json").read_text())
    for morph, kw in (("compact", dict(graft_diam_um=(300, 600), graft_roughness=0.15)),
                      ("strut_like", dict(graft_diam_um=(120, 250), graft_roughness=0.6, graft_fill=0.3))):
        ps = [generate_phantom(PhantomConfig(model="condyle", shape=(56, 72, 72), voxel_um=40, defect_diameter_um=2000,
                                             graft_material="ha", healing_stage=0.55, seed=700 + s, **kw)) for s in range(4)]
        vals = [dice_oracle(render_fast(mu_with_graft(ps[i], 900), 40, ImagingConfig(seed=10 + i, psf_sigma_um=20, noise_sigma=150)).data,
                            ps[i].labels, ps[i].roi_mask) for i in range(1, 4)]
        r = {"morphology": morph, "features": "intensity_oracle_dice_optimal", "dice_graft": float(np.mean([a for a, _ in vals])),
             "dice_new": float(np.mean([b for _, b in vals])), "acc": None}
        C2["rows"].append(r); out["C2"].append(r); print("C2", r, flush=True)
    (RESULTS / "exp_C2_ablation.json").write_text(json.dumps(C2, indent=1))
    # L2 (strut-like, later timepoint images)
    kw = dict(model="condyle", shape=(56, 72, 72), voxel_um=40, defect_diameter_um=2000, graft_material="ha",
              graft_diam_um=(120, 250), graft_roughness=0.6, graft_fill=0.3, periodic_texture=False)
    L2 = json.loads((RESULTS / "exp_L2_strutlike.json").read_text())
    vals = []
    for i, sd in enumerate((900, 901, 902, 903)):
        if i == 0:
            continue
        p1 = generate_phantom(PhantomConfig(healing_stage=0.6, seed=sd, **kw))
        v = render_fast(mu_with_graft(p1, 900), 40, ImagingConfig(seed=11 + i, psf_sigma_um=20, noise_sigma=150)).data
        vals.append(dice_oracle(v, p1.labels, p1.roi_mask))
    L2["summary"]["intensity_oracle_dice_optimal"] = {"dice_graft": float(np.mean([a for a, _ in vals])),
                                                      "dice_new": float(np.mean([b for _, b in vals]))}
    (RESULTS / "exp_L2_strutlike.json").write_text(json.dumps(L2, indent=1))
    out["L2"] = L2["summary"]["intensity_oracle_dice_optimal"]
    print("L2", out["L2"])
    save_result("exp_Q01_intensity_oracle", out)
    replot(C)


def replot(C):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from common import FIG
    rows = C["C"]
    Xs = sorted({r["graft_mgHA"] for r in rows}, reverse=True)
    sig = sorted({r["noise_sigma"] for r in rows})
    fig, axs = plt.subplots(1, len(sig), figsize=(4.2 * len(sig), 3.7), sharey=True)
    series = [("intensity_oracle_dice_graft", "intensity-only oracle (upper bound)", "#444444", "--"),
              ("multiotsu_dice_graft", "multi-Otsu", "#56B4E9", "-"), ("gmm_dice_graft", "GMM", "#009E73", "-"),
              ("rf_dice_graft", "RF (shape + spatial features)", "#E69F00", "-")]
    for ax, s in zip(axs, sig):
        for k, lab, c, ls in series:
            ys = [next(r for r in rows if r["graft_mgHA"] == X and r["noise_sigma"] == s)[k] for X in Xs]
            ax.plot(Xs, ys, "o-", color=c, ls=ls, lw=2 if k.startswith("rf") else 1.4, label=lab)
        ax.axvspan(650, 1000, color="#E69F00", alpha=0.12)
        ax.set_title(f"noise σ = {s}"); ax.invert_xaxis(); ax.set_ylim(0, 1.0); ax.grid(alpha=0.3)
        ax.set_xlabel("graft HA-equivalent density (mgHA/cm³)")
    axs[0].set_ylabel("graft Dice in defect ROI")
    axs[0].legend(fontsize=7.5, loc="lower left")
    fig.suptitle("Experiment C (SYNTHETIC): graft Dice vs graft/new-bone density overlap (shaded = new-bone range; compact granules)")
    fig.tight_layout(); fig.savefig(FIG / "exp_C_separability.png", dpi=110)


if __name__ == "__main__":
    main()
