"""Experiment S1H — held-out validation of the measurement-support advisor (pre-registered, PREREGISTRATION §7).

Conditions not used in any advisor tuning: new phantom seeds and all three defect models, graft densities
950/1450/1850/2600 mgHA/cm³, PSF σ = 30 µm, spatially correlated noise. Advisor 1.3.3 frozen.
"""
from __future__ import annotations

import time

import numpy as np
from scipy import ndimage as ndi

from common import save_result
from exp_C_separability import mu_with_graft
from exp_S1_advisor import endpoint_errs, graft_err, summarize
from osteoquant.advisor import MaterialProfile
from osteoquant.advisor.integration import advisor_threshold_segmentation, support_for_scan
from osteoquant.advisor.separability import ADVISOR_VERSION
from osteoquant.phantom import ImagingConfig, PhantomConfig, generate_phantom, render_fast

assert ADVISOR_VERSION == "1.3.3", "S1H is pre-registered for advisor 1.3.3"
STRUCTS = [("condyle", s, dict(shape=(56, 72, 72), defect_diameter_um=2000, graft_diam_um=(300, 600))) for s in (2000, 2001, 2002)] + \
          [("calvarial", s, dict(shape=(40, 96, 96), defect_diameter_um=2400, graft_diam_um=(120, 250), graft_roughness=0.6,
                                 graft_fill=0.3)) for s in (2100, 2101, 2102)] + \
          [("segmental", s, dict(shape=(80, 72, 72), gap_length_um=1600, graft_diam_um=(300, 600))) for s in (2200, 2201, 2202)]
DENS = (950, 1450, 1850, 2600)
NOISE = (60, 120, 200)


def correlated_noise(shape, sigma, seed):
    rng = np.random.default_rng(seed)
    n = ndi.gaussian_filter(rng.standard_normal(shape).astype(np.float32), 0.8)
    return (n / (n.std() + 1e-9) * sigma).astype(np.float32)


def main():
    t0 = time.time()
    rows = []
    for model, seed, kw in STRUCTS:
        ph = generate_phantom(PhantomConfig(model=model, voxel_um=40, supersample=2, graft_material="ha",
                                            healing_stage=0.45, seed=seed, periodic_texture=False, **kw))
        for X in DENS:
            clean = render_fast(mu_with_graft(ph, X), 40, ImagingConfig(seed=seed, psf_sigma_um=30, noise_sigma=0.0)).data
            for s in NOISE:
                img = clean + correlated_noise(clean.shape, s, seed * 10 + s)
                prof = MaterialProfile(id=f"char_{X}", rel_mean=X / 1075.0, rel_sd=0.04 * X / 1075.0, struct_um=450)
                cfg = {"material": prof}
                sup = support_for_scan(img, ph.roi_mask, (40.0,) * 3, cfg)
                lab, info = advisor_threshold_segmentation(img, ph.roi_mask, (40.0,) * 3, cfg)
                e, vt = graft_err(lab, ph.labels, ph.roi_mask)
                ep = sup["endpoints"]
                rows.append({"part": "H", "structure": f"{model}_{seed}", "graft_mgHA": X, "noise": s, "method": "advisor_threshold_H",
                             "err": e, **endpoint_errs(lab, ph.labels, ph.roi_mask), "graft_vox": vt,
                             "status": ep["residual_graft_volume"]["status"], "status_new": ep["new_bone_volume"]["status"],
                             "status_mineral": ep["total_mineral_volume"]["status"]})
            print(model, seed, X, [(r["status"][:4], round(r["err"], 2)) for r in rows[-3:]], flush=True)
    summ = summarize(rows, "advisor_threshold_H")
    # bootstrap over structures (unit of replication) for the per-endpoint failure-among-supported rate
    rng = np.random.default_rng(0)
    structs = sorted({r["structure"] for r in rows})
    boot = {}
    for ep, ek, sk in (("residual_graft_volume", "err", "status"), ("new_bone_volume", "err_new", "status_new"),
                       ("total_mineral_volume", "err_mineral", "status_mineral")):
        vals = []
        for _ in range(2000):
            pick = rng.choice(structs, len(structs))
            rr = [r for p_ in pick for r in rows if r["structure"] == p_]
            sup_ = [r for r in rr if r[sk] != "not_supported" and np.isfinite(r[ek])]
            if sup_:
                vals.append(np.mean([abs(r[ek]) > 0.2 for r in sup_]))
        boot[ep] = {"fail_rate_among_supported_boot95": [float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))] if vals else None}
    print(summ)
    save_result("exp_S1H_heldout", {"experiment": "S1H", "preregistered": "docs/science/PREREGISTRATION.md §7",
                                    "advisor_version": ADVISOR_VERSION, "summary": [summ], "bootstrap_by_structure": boot,
                                    "rows": rows, "seconds": time.time() - t0})


if __name__ == "__main__":
    main()
