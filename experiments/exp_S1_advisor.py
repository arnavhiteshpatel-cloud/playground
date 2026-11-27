"""Experiment S1 — does the measurement-support advisor predict measurement failure?

Pre-registered policy (osteoquant/advisor/separability.py, set before this experiment):
graft-specific endpoints are 'supported' by intensity only if the Dice-optimal intensity oracle,
computed from the advisor's material model + the scan's estimated noise, gives graft Dice ≥ 0.85
with volume ratio within ±10%; bone-derived grafts are never intensity-supported.

Outcome per specimen and method: graft-volume relative error in the true defect ROI,
|V_pred / V_true − 1|. A measurement is a FAILURE if the error exceeds 20% (pre-registered).

Part A — synthetic dataset specimens (test: β-TCP, BCP, HA, CaSO4 ×4 each; held-out materials:
         45S5 bioglass, DBBM xenograft ×20 each). Advisor input: material name + scan-estimated
         noise (estimated outside the defect, no ground truth used). Methods: multi-Otsu
         (pipeline default intensity method) and the synthetic 3D U-Net (unet_noctx_s0).
Part B — graft-density × noise sweep (graft HA-equivalent 650–2200 mgHA/cm³, σ 30–250) on 3 phantoms
         per condition; advisor given the graft's relative density as if the material had been
         characterised. Method: multi-Otsu.

LIMITATION (stated in every summary): the advisor's material physics and the simulator share the
same attenuation model (phantom/materials.py), so Part A partly tests self-consistency. The
independent parts are the decision rule, the new-bone maturity assumption vs the simulator's
healing model, and the noise estimate from the image. Real validation requires physical phantoms.
"""
from __future__ import annotations

import time

import numpy as np

from common import load_split, save_result
from exp_C_separability import make_structures, mu_with_graft
from osteoquant.advisor import assess_support, scan_relative_units, MaterialProfile, NOT_SUPPORTED
from osteoquant.phantom import ImagingConfig, render_fast
from osteoquant.segment import classical as C

FAIL = 0.20


def graft_err(pred_lab, true_lab, roi):
    vt = int(((true_lab == 2) & roi).sum())
    vp = int(((pred_lab == 2) & roi).sum())
    return (vp / vt - 1.0) if vt else float("nan"), vt


def summarize(rows, method):
    r = [x for x in rows if x["method"] == method and np.isfinite(x["err"])]
    fail = np.array([abs(x["err"]) > FAIL for x in r])
    refused = np.array([x["status"] == NOT_SUPPORTED for x in r])
    out = {"method": method, "n": len(r), "n_fail": int(fail.sum()), "n_refused": int(refused.sum()),
           "failures_refused": int((fail & refused).sum()),
           "sensitivity_refuse_given_fail": float((fail & refused).sum() / max(1, fail.sum())),
           "refused_but_ok": int((refused & ~fail).sum()),
           "supported_and_ok": int((~refused & ~fail).sum()),
           "supported_but_failed": int((~refused & fail).sum()),
           "abs_err_supported_median": float(np.median([abs(x["err"]) for x, f in zip(r, refused) if not f])) if (~refused).any() else None,
           "abs_err_refused_median": float(np.median([abs(x["err"]) for x, f in zip(r, refused) if f])) if refused.any() else None}
    return out


def part_a(rows):
    from osteoquant.ml.train import load_model, predict_proba
    model, ck = load_model("unet_noctx_s0")
    cases = load_split("test") + load_split("ood_mat")
    for c in cases:
        mat = c.meta["spec"]["material"]
        est = scan_relative_units(c.image, exclude_mask=c.roi)
        a = assess_support(mat, noise_rel=est["noise_rel"], voxel_um=c.spacing[0])
        st = a.status("residual_graft_volume")
        lab_mo, _ = C.seg_multiotsu(c.image, c.roi, True)
        e_mo, vt = graft_err(lab_mo, c.labels, c.roi)
        p = predict_proba(model, c, ck["cfg"], tta=False)
        e_un, _ = graft_err(p.argmax(0), c.labels, c.roi)
        true_noise_rel = c.meta["spec"]["imaging"]["noise_sigma"] / max(est["host"] - est["soft"], 1e-6)
        for meth, e in (("multiotsu", e_mo), ("unet_synth", e_un)):
            rows.append({"part": "A", "case": c.case_id, "material": mat, "method": meth, "err": e, "status": st,
                         "oracle_dice": a.intensity.get("dice_graft"), "noise_rel_est": est["noise_rel"],
                         "noise_rel_true_approx": true_noise_rel, "graft_vox": vt})
        print("A", c.case_id, st, round(e_mo, 3), round(e_un, 3), round(est["noise_rel"], 3), flush=True)


def part_b(rows):
    phs = make_structures(4)
    host = 1075.0
    for X in (2200, 1600, 1300, 1150, 1000, 900, 800, 650):
        for s in (30, 80, 150, 250):
            for i in range(1, 4):
                ph = phs[i]
                img = render_fast(mu_with_graft(ph, X), 40, ImagingConfig(seed=10 + i, psf_sigma_um=20, noise_sigma=s)).data
                est = scan_relative_units(img, exclude_mask=ph.roi_mask)
                prof = MaterialProfile(id=f"char_{X}", rel_mean=X / host, rel_sd=0.04 * X / host, struct_um=450)
                a = assess_support(prof, noise_rel=est["noise_rel"], voxel_um=40)
                lab, _ = C.seg_multiotsu(img, ph.roi_mask, X > 1000)
                e, vt = graft_err(lab, ph.labels, ph.roi_mask)
                rows.append({"part": "B", "case": f"X{X}_s{s}_{i}", "graft_mgHA": X, "noise": s, "method": "multiotsu_B",
                             "err": e, "status": a.status("residual_graft_volume"),
                             "oracle_dice": a.intensity.get("dice_graft"), "noise_rel_est": est["noise_rel"], "graft_vox": vt})
            print("B", X, s, rows[-1]["status"], round(np.mean([r["err"] for r in rows[-3:]]), 3), flush=True)


def main():
    t0 = time.time()
    rows = []
    part_a(rows)
    part_b(rows)
    summ = [summarize(rows, m) for m in ("multiotsu", "unet_synth", "multiotsu_B")]
    for s in summ:
        print(s)
    save_result("exp_S1_advisor", {
        "experiment": "S1", "failure_threshold_rel_volume_error": FAIL, "summary": summ, "rows": rows,
        "seconds": time.time() - t0,
        "limitation": "advisor material physics shares the simulator's attenuation model (partial self-consistency); "
                      "synthetic data only"})


if __name__ == "__main__":
    main()
