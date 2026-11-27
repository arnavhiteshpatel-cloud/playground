"""Experiment L4 — sensitivity of registration QC to graded misregistration (FA-04).

Three day-0 / later pairs (generator v2, compact HA-like granules at 900 mgHA/cm³, σ=80, no granule motion
so that misregistration is the only error source). The later scan is perfectly aligned (same frame), then a
known residual misalignment is applied: translation 0–320 µm or rotation 0–8° about the volume centre.
For each: registration QC (host-mineral Dice, NCC) and the graft Dice of day-0 footprint propagation.
A misregistration is *harmful* if graft Dice drops by >0.10 relative to the aligned case. Reported: QC pass
rate for harmless vs harmful misalignments (QC sensitivity/specificity), and the host-Dice threshold that
would separate them (for revising the 0.85 policy value).
"""
import numpy as np

from common import save_result
from exp_C_separability import mu_with_graft
from osteoquant.longitudinal import apply_rigid, day0_propagation, registration_qc
from osteoquant.phantom import PhantomConfig, generate_phantom, ImagingConfig, render_fast
from osteoquant.segment import classical as C

SP = (40.0,) * 3
BASE = dict(model="condyle", shape=(56, 72, 72), voxel_um=40, defect_diameter_um=2000, graft_material="ha",
            graft_diam_um=(300, 600), periodic_texture=False)
rows = []
for sd in (910, 911, 912):
    p0 = generate_phantom(PhantomConfig(healing_stage=0.0, seed=sd, **BASE))
    p1 = generate_phantom(PhantomConfig(healing_stage=0.5, seed=sd, **BASE))
    I0 = render_fast(mu_with_graft(p0, 900), 40, ImagingConfig(seed=sd, psf_sigma_um=20, noise_sigma=80)).data
    I1 = render_fast(mu_with_graft(p1, 900), 40, ImagingConfig(seed=sd + 1, psf_sigma_um=20, noise_sigma=80)).data
    g0 = C.clean_binary(C.threshold_otsu(I0)[0] & p0.roi_mask, 8)
    roi, y = p1.roi_mask, p1.labels
    def gd(img):
        lab = day0_propagation(C.threshold_otsu(img)[0] & (img != 0), g0, roi)
        a, b = (lab == 2) & roi, (y == 2) & roi
        return float(2 * (a & b).sum() / max(1, a.sum() + b.sum()))
    base_d = gd(I1)
    perturb = [("none", 0, (0, 0, 0), (0, 0, 0))]
    for t in (20, 40, 80, 160, 320):
        perturb.append(("trans", t, (0, 0, 0), tuple(np.array([1, 1, 1]) / np.sqrt(3) * t)))
    for r in (0.5, 1, 2, 4, 8):
        perturb.append(("rot", r, (r, r / 2, 0), (0, 0, 0)))
    for kind, mag, rot, tr in perturb:
        moved = I1 if kind == "none" else apply_rigid(I1, SP, rot, tr)[0]
        qc = registration_qc(I0, moved, exclude=p0.roi_mask)
        d = gd(moved)
        rows.append({"seed": sd, "kind": kind, "magnitude": mag, "graft_dice": d, "graft_dice_drop": base_d - d,
                     "harmful": bool(base_d - d > 0.10), **{k: qc[k] for k in ("host_dice", "host_ncc", "pass")}})
        print(sd, kind, mag, round(d, 3), "QC", round(qc["host_dice"], 3), round(qc["host_ncc"], 3), qc["pass"], flush=True)
harm = [r for r in rows if r["harmful"]]
ok = [r for r in rows if not r["harmful"]]
summ = {"n": len(rows), "n_harmful": len(harm),
        "qc_flags_harmful": float(np.mean([not r["pass"] for r in harm])) if harm else None,
        "qc_passes_harmless": float(np.mean([r["pass"] for r in ok])) if ok else None,
        "max_host_dice_among_harmful": float(max([r["host_dice"] for r in harm])) if harm else None,
        "min_host_dice_among_harmless": float(min([r["host_dice"] for r in ok])) if ok else None}
print(summ)
save_result("exp_L4_registration_qc", {"experiment": "L4", "summary": summ, "rows": rows})
