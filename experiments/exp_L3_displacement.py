"""Experiment L3 — longitudinal day-0 propagation when granules move and fracture (FORENSIC_AUDIT FA-04).

Gen-0 (Experiments L/L2) assumed residual graft only shrinks in place. Here generator v2 displaces granules
after implantation (mean translation D ∈ {0, 50, 100, 200, 400} µm; uniform 0..2D) and fractures a fraction
F ∈ {0, 0.3} of granules (fragments separated by 120 µm), with extra per-granule resorption variability
(lognormal CV 0.3). Overlap regime: graft 900 mgHA/cm³ (inside the new-bone range), strut-like granules,
noise σ=150 (as L2). Later scan receives a random rigid motion (≤5°, ≤200 µm) and is registered to day 0
(host-anatomy-masked rigid registration).

Methods (graft vs new bone in the true defect ROI):
  naive_footprint   Gen-0 method: later mineral ∩ day-0 graft footprint
  tracked_footprint per-granule template matching (fixed ±500 µm search) then footprint
  multiotsu         single-timepoint intensity
  intensity_oracle  Dice-optimal intensity-only upper bound (uses truth)
Also: registration QC (host-mineral Dice/NCC), tracking summary, and the advisor's day-0 decision computed
from QC + tracking (no ground truth). A deliberate registration failure (identity transform instead of the
registration result) tests whether QC flags gross misalignment.
3 specimens per condition (seeds 900–902). Truth: later phantom labels (registered frame = day-0 frame:
later images are moved then registered back; labels are compared in the later phantom's native frame by
resampling the registered prediction with the inverse of the applied motion composed with the estimate —
implemented simply by applying the estimated transform to bring the later image back to day-0 frame, which
equals the native frame of both phantoms).
"""
from __future__ import annotations

import time

import numpy as np
from scipy import ndimage as ndi

from common import save_result
from exp_C_separability import mu_with_graft
from osteoquant.advisor import assess_support, MaterialProfile, dice_oracle_volume
from osteoquant.longitudinal import (register, resample, apply_rigid, day0_propagation, registration_qc,
                                     track_granules)
from osteoquant.phantom import PhantomConfig, generate_phantom, ImagingConfig, render_fast
from osteoquant.segment import classical as C

SP = (40.0,) * 3
SHAPE = (56, 72, 72)
SEARCH_UM = 500.0   # tracking search radius, fixed a priori (review STAT-06)
BASE = dict(model="condyle", shape=SHAPE, voxel_um=40, defect_diameter_um=2000, graft_material="ha",
            graft_diam_um=(120, 250), graft_roughness=0.6, graft_fill=0.3, periodic_texture=False)


def scores(pred, y, roi):
    m = roi & ((y == 1) | (y == 2))
    out = {}
    for c, n in ((2, "graft"), (1, "new")):
        a, b = (pred == c) & roi, (y == c) & roi
        out[f"dice_{n}"] = float(2 * (a & b).sum() / max(1, a.sum() + b.sum()))
    vt = int(((y == 2) & roi).sum())
    out["graft_vol_err"] = float(((pred == 2) & roi).sum() / vt - 1) if vt else float("nan")
    return out


def main():
    t0 = time.time()
    rows = []
    rng = np.random.default_rng(11)
    for D in (0, 50, 100, 200, 400):
        for F in (0.0, 0.3):
            for sd in (900, 901, 902):
                p0 = generate_phantom(PhantomConfig(healing_stage=0.0, seed=sd, **BASE))
                p1 = generate_phantom(PhantomConfig(healing_stage=0.6, seed=sd, granule_displacement_um=D,
                                                    fragment_prob=F, resorption_cv=0.3, **BASE))
                I0 = render_fast(mu_with_graft(p0, 900), 40, ImagingConfig(seed=sd, psf_sigma_um=20, noise_sigma=150)).data
                I1 = render_fast(mu_with_graft(p1, 900), 40, ImagingConfig(seed=sd + 50, psf_sigma_um=20, noise_sigma=150)).data
                roi, y = p1.roi_mask, p1.labels
                moved, tt = apply_rigid(I1, SP, rng.uniform(-5, 5, 3), rng.uniform(-200, 200, 3))
                excl = p0.roi_mask
                tx, _ = register(I0, moved, SP, "rigid", mask=~ndi.binary_dilation(excl, iterations=3))
                back = resample(moved, SHAPE, SP, tx)
                qc = registration_qc(I0, back, exclude=excl, spacing_um=SP)
                # deliberate failure: skip registration (identity)
                import SimpleITK as sitk
                bad = resample(moved, SHAPE, SP, sitk.Euler3DTransform())
                qc_bad = registration_qc(I0, bad, exclude=excl, spacing_um=SP)
                g0 = C.clean_binary(C.threshold_otsu(I0)[0] & p0.roi_mask, 8)
                later_min = C.threshold_otsu(back)[0] & (back != 0)
                naive = day0_propagation(later_min, g0, roi)
                tr = track_granules(I0, back, g0, SP, search_um=SEARCH_UM)   # fixed; independent of true motion
                tracked = day0_propagation(later_min, tr["footprint"], roi)
                mo = C.seg_multiotsu(I1, roi, True)[0]
                orc = dice_oracle_volume(I1, y, roi)
                prof = MaterialProfile("ha900", 900 / 1075, 0.04, 185, "strut")
                # advisor inputs are COMPUTED (no ground truth): naive footprint → motion estimate from tracking
                # must be within tolerance; tracked footprint → motion compensated, untracked share must be small
                day0_naive = {"registered": True, "qc_pass": qc["pass"],
                              "max_displacement_um": tr["summary"]["p90_shift_um"],
                              "untracked_fraction": tr["summary"]["untracked_volume_fraction"]}
                day0_tracked = {"registered": True, "qc_pass": qc["pass"], "max_displacement_um": 0.0,
                                "untracked_fraction": tr["summary"]["untracked_volume_fraction"]}
                adv = assess_support(prof, noise_rel=150 / 950, voxel_um=40, day0=day0_tracked)
                adv_naive = assess_support(prof, noise_rel=150 / 950, voxel_um=40, day0=day0_naive)
                base = {"D_um": D, "F": F, "seed": sd, "qc": qc, "qc_identity": qc_bad,
                        "tracking": tr["summary"], "advisor_status": adv.status("residual_graft_volume"),
                        "advisor_status_naive": adv_naive.status("residual_graft_volume"),
                        "true_motion": p1.truth.get("graft_motion")}
                for meth, pred in (("naive_footprint", naive), ("tracked_footprint", tracked), ("multiotsu", mo)):
                    rows.append({**base, "method": meth, **scores(pred, y, roi)})
                rows.append({**base, "method": "intensity_oracle", "dice_graft": orc["dice_graft"],
                             "dice_new": orc["dice_new"], "graft_vol_err": orc["graft_volume_ratio"] - 1})
                r = {m["method"]: round(m["dice_graft"], 3) for m in rows[-4:]}
                print(D, F, sd, r, "QC", round(qc["host_dice"], 3), qc["pass"], "| identity QC", round(qc_bad["host_dice"], 3),
                      qc_bad["pass"], "| untracked", round(tr["summary"]["untracked_volume_fraction"], 2),
                      "adv", base["advisor_status"], flush=True)
    summ = []
    for D in (0, 50, 100, 200, 400):
        for F in (0.0, 0.3):
            for m in ("naive_footprint", "tracked_footprint", "multiotsu", "intensity_oracle"):
                rr = [r for r in rows if r["D_um"] == D and r["F"] == F and r["method"] == m]
                summ.append({"D_um": D, "F": F, "method": m, "dice_graft": float(np.mean([r["dice_graft"] for r in rr])),
                             "abs_vol_err": float(np.mean([abs(r["graft_vol_err"]) for r in rr])), "n": len(rr)})
    def refusal(method, key):
        rr = [r for r in rows if r["method"] == method]
        fail = [abs(r["graft_vol_err"]) > 0.2 or r["dice_graft"] < 0.8 for r in rr]
        ref = [r[key] != "supported_with_conditions" and r[key] != "supported" for r in rr]
        return {"n": len(rr), "n_fail": int(sum(fail)), "failures_refused": int(sum(f and g for f, g in zip(fail, ref))),
                "supported_but_failed": int(sum(f and not g for f, g in zip(fail, ref))),
                "refused_but_ok": int(sum(g and not f for f, g in zip(fail, ref)))}
    advisor_eval = {"naive_footprint": refusal("naive_footprint", "advisor_status_naive"),
                    "tracked_footprint": refusal("tracked_footprint", "advisor_status")}
    qc_sens = float(np.mean([not r["qc_identity"]["pass"] for r in rows if r["method"] == "naive_footprint"]))
    qc_spec = float(np.mean([r["qc"]["pass"] for r in rows if r["method"] == "naive_footprint"]))
    save_result("exp_L3_displacement", {"experiment": "L3", "summary": summ, "rows": rows,
                                        "registration_failure_detection": {"flagged_identity_fraction": qc_sens,
                                                                           "passed_correct_fraction": qc_spec},
                                        "advisor_evaluation": advisor_eval, "advisor_version": adv.advisor_version,
                                        "seconds": time.time() - t0})
    for s in summ:
        print(s)
    print("QC: identity flagged", qc_sens, "correct passed", qc_spec)


if __name__ == "__main__":
    main()
