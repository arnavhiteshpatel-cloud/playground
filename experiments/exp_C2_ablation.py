"""Experiment C2 — what information lets the RF exceed the intensity-only bound?

Overlap regime: graft 900 mgHA/cm³ (inside new-bone range), noise σ=150.
Feature ablation: full | no_spatial (no distance-to-ROI prior) | intensity_scales (Gaussian-
smoothed intensities only) | raw (single voxel intensity).
Morphology stress: 'compact' granules (default 300–600 µm, roughness 0.15) vs 'strut-like'
granules (120–250 µm, roughness 0.6), the latter closer to new-bone strut scale.
"""
import numpy as np
from common import save_result
from exp_C_separability import mu_with_graft, gn_scores, bayes_bound
from osteoquant.phantom import PhantomConfig, generate_phantom, ImagingConfig, render_fast
from osteoquant.segment import classical as C

SHAPE = (56, 72, 72)


def structs(morph, n=4):
    kw = dict(graft_diam_um=(300, 600), graft_roughness=0.15) if morph == "compact" else \
        dict(graft_diam_um=(120, 250), graft_roughness=0.6, graft_fill=0.3)
    return [generate_phantom(PhantomConfig(model="condyle", shape=SHAPE, voxel_um=40, defect_diameter_um=2000,
                                           graft_material="ha", healing_stage=0.55, seed=700 + s, **kw)) for s in range(n)]


out = {"experiment": "C2", "graft_mgHA": 900, "noise_sigma": 150, "rows": []}
for morph in ("compact", "strut_like"):
    phs = structs(morph)
    vols = [render_fast(mu_with_graft(ph, 900), 40, ImagingConfig(seed=10 + i, psf_sigma_um=20, noise_sigma=150)).data
            for i, ph in enumerate(phs)]
    sp = (40.0,) * 3
    for fs in ("full", "no_spatial", "intensity_scales", "raw"):
        rf = C.RFSegmenter(40, 16, 0, feature_set=fs).fit([vols[0]], [phs[0].labels], [sp], [phs[0].roi_mask], 20000)
        sc = [gn_scores(rf.predict(vols[i], sp, phs[i].roi_mask)[0], phs[i].labels, phs[i].roi_mask) for i in range(1, 4)]
        row = {"morphology": morph, "features": fs, "acc": float(np.mean([s[0] for s in sc])),
               "dice_graft": float(np.mean([s[1] for s in sc])), "dice_new": float(np.mean([s[2] for s in sc]))}
        out["rows"].append(row); print(row, flush=True)
    bb = [bayes_bound(vols[i], phs[i].labels, phs[i].roi_mask & ((phs[i].labels == 1) | (phs[i].labels == 2))) for i in range(1, 4)]
    row = {"morphology": morph, "features": "bayes_intensity_bound", "acc": float(np.mean([b[0] for b in bb])),
           "dice_graft": float(np.mean([b[1] for b in bb])), "dice_new": float(np.mean([b[2] for b in bb]))}
    out["rows"].append(row); print(row, flush=True)
save_result("exp_C2_ablation", out)
