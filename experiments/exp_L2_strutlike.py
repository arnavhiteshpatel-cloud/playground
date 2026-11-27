"""Experiment L2 — day-0 propagation vs single-timepoint RF when graft morphology resembles new
bone (strut-like granules, 120–250 µm, roughness 0.6), graft density 900 mgHA/cm³, noise σ=150.
Same protocol as Experiment L (random rigid motion ≤5°/≤200 µm, host-anatomy-masked rigid registration)."""
import numpy as np
from scipy import ndimage as ndi
from common import save_result
from exp_C_separability import mu_with_graft, gn_scores, bayes_bound
from osteoquant.phantom import PhantomConfig, generate_phantom, ImagingConfig, render_fast
from osteoquant.longitudinal import register, resample, apply_rigid, target_registration_error, day0_propagation
from osteoquant.segment import classical as C
SP = (40.0,) * 3; SHAPE = (56, 72, 72)
kw = dict(model="condyle", shape=SHAPE, voxel_um=40, defect_diameter_um=2000, graft_material="ha",
          graft_diam_um=(120, 250), graft_roughness=0.6, graft_fill=0.3, periodic_texture=False)
pairs = [(generate_phantom(PhantomConfig(healing_stage=0.0, seed=s, **kw)), generate_phantom(PhantomConfig(healing_stage=0.6, seed=s, **kw))) for s in (900, 901, 902, 903)]
I0 = [render_fast(mu_with_graft(a, 900), 40, ImagingConfig(seed=1 + i, psf_sigma_um=20, noise_sigma=150)).data for i, (a, b) in enumerate(pairs)]
I1 = [render_fast(mu_with_graft(b, 900), 40, ImagingConfig(seed=11 + i, psf_sigma_um=20, noise_sigma=150)).data for i, (a, b) in enumerate(pairs)]
rf = C.RFSegmenter(40, 16, 0).fit([I1[0]], [pairs[0][1].labels], [SP], [pairs[0][1].roi_mask], 20000)
rng = np.random.default_rng(7); rows = []
for i in range(1, 4):
    p0, p1 = pairs[i]; roi, y = p1.roi_mask, p1.labels
    g0 = C.clean_binary(C.threshold_otsu(I0[i])[0] & p0.roi_mask, 8)
    moved, tt = apply_rigid(I1[i], SP, rng.uniform(-5, 5, 3), rng.uniform(-200, 200, 3))
    m = ~ndi.binary_dilation(p0.roi_mask, iterations=3)
    tx, _ = register(I0[i], moved, SP, "rigid", mask=m)
    back = resample(moved, SHAPE, SP, tx)
    tre = target_registration_error(tt, tx, np.argwhere(roi)[::300][:, ::-1] * 0.04)["mean_um"]
    res = {"day0_estimated_registration": gn_scores(day0_propagation(C.threshold_otsu(back)[0] & (back != 0), g0, roi), y, roi),
           "rf_single_timepoint": gn_scores(rf.predict(I1[i], SP, roi)[0], y, roi),
           "multiotsu": gn_scores(C.seg_multiotsu(I1[i], roi, True)[0], y, roi),
           "bayes_intensity_bound": bayes_bound(I1[i], y, roi & ((y == 1) | (y == 2)))}
    for k, v in res.items():
        rows.append({"specimen": i, "method": k, "acc": v[0], "dice_graft": v[1], "dice_new": v[2], "tre_um": tre})
    print({k: round(v[1], 3) for k, v in res.items()}, "TRE", round(tre, 2), flush=True)
summ = {m: {"dice_graft": float(np.mean([r["dice_graft"] for r in rows if r["method"] == m])),
            "dice_new": float(np.mean([r["dice_new"] for r in rows if r["method"] == m]))} for m in {r["method"] for r in rows}}
save_result("exp_L2_strutlike", {"experiment": "L2", "rows": rows, "summary": summ}); print(summ)
