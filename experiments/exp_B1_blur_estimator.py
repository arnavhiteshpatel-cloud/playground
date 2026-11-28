"""Experiment B1 (SYNTHETIC): accuracy of the scan-measured blur estimate used by the advisor (cycle-3 review C3-SCI-08).

The advisor measures total blur σ (PSF ⊗ voxel) from host-bone/soft-tissue edges outside the defect and inflates it
conservatively above 0.6 voxel (`integration._assess_scan`). The review found that the estimate under-reads blur at
high noise and that its calibration had no script. This experiment provides that script: known Gaussian PSF on
condyle/segmental phantoms, three noise levels, three seeds; it reports the raw estimate, the calibrated value used by
the advisor, and the reference blur √(σ_psf² + σ_vox²) with σ_vox = 1/√12 voxel for the voxel's box sampling.
"""
from __future__ import annotations

import time

import numpy as np

from common import save_result
from osteoquant.advisor.integration import estimate_blur, scan_relative_units
from osteoquant.phantom import ImagingConfig, PhantomConfig, generate_phantom, render_fast

VOX = 40.0
PSFS = (15.0, 25.0, 35.0, 50.0)
NOISE = (40.0, 80.0, 140.0)
SEEDS = (7001, 7002, 7003)
MODELS = ("condyle", "segmental")


def calibrated(raw):
    """The advisor's conservative calibration (integration._assess_scan, ≥1.4.0)."""
    return None if raw is None else raw * (1 + max(0.0, raw - 0.6) * 1.5)


def main():
    t0 = time.time()
    rows = []
    for model in MODELS:
        for seed in SEEDS:
            ph = generate_phantom(PhantomConfig(model=model, voxel_um=VOX, supersample=2, graft_material="ha",
                                                healing_stage=0.5, seed=seed, periodic_texture=False))
            for psf in PSFS:
                for s in NOISE:
                    img = render_fast(ph.mu, VOX, ImagingConfig(seed=seed, psf_sigma_um=psf, noise_sigma=s)).data
                    est = scan_relative_units(img, exclude_mask=ph.roi_mask)
                    b = estimate_blur(img, ph.roi_mask, est["soft"], est["host"])
                    ref = float(np.hypot(psf / VOX, 1 / np.sqrt(12)))
                    raw = b.get("sigma_vox")
                    rows.append({"model": model, "seed": seed, "psf_um": psf, "noise": s, "noise_rel": est["noise_rel"],
                                 "sigma_ref_vox": ref, "sigma_raw_vox": raw, "sigma_used_vox": calibrated(raw),
                                 "ratio_used_to_ref": (calibrated(raw) / ref) if raw else None})
                    print(rows[-1], flush=True)
    summ = {}
    for s in NOISE:
        r = [x["ratio_used_to_ref"] for x in rows if x["noise"] == s and x["ratio_used_to_ref"]]
        summ[f"noise_{int(s)}"] = {"n": len(r), "ratio_median": float(np.median(r)) if r else None,
                                   "ratio_min": float(min(r)) if r else None,
                                   "share_underestimated_by_20pct": float(np.mean([x < 0.8 for x in r])) if r else None}
    print(summ)
    save_result("exp_B1_blur_estimator", {"experiment": "B1", "summary": summ, "rows": rows, "seconds": time.time() - t0})


if __name__ == "__main__":
    main()
