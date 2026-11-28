"""Experiment L5 (SYNTHETIC): can registration QC verify alignment along the axis of a segmental (diaphyseal) defect?

Cycle-3 review C3-SCI-04: the block-wise, structure-tensor-projected QC dropped shift components along directions no
block constrains, so axial misregistration of 160–400 µm passed on segmental phantoms. Since the fail-closed change,
a QC verdict requires every direction to be constrained by at least one block; otherwise the registration is reported
as not verifiable (pass = False) and the unverifiable direction is named.

Design: two segmental phantoms (the generic one used by the review's probe, and the bridged late-stage F2 set-up),
known shifts of 0, 160, 240 and 400 µm along each axis; record pass/fail, the measured residual shift and the reason.
"""
from __future__ import annotations

import time

import numpy as np
from scipy import ndimage as ndi

from common import save_result
from osteoquant.longitudinal import registration_qc
from osteoquant.phantom import ImagingConfig, PhantomConfig, generate_phantom, render_fast

SP = (40.0, 40.0, 40.0)
CASES = {"segmental_generic": dict(model="segmental", voxel_um=40, supersample=1, graft_material="ha",
                                   healing_stage=0.5, seed=4910),
         "segmental_bridged_F2": dict(model="segmental", voxel_um=40, supersample=1, graft_material="ha",
                                      healing_stage=0.9, seed=7)}


def main():
    t0 = time.time()
    rows = []
    for name, kw in CASES.items():
        ph = generate_phantom(PhantomConfig(**kw))
        img = render_fast(ph.mu, 40, ImagingConfig(psf_sigma_um=30, noise_sigma=40, seed=1)).data
        excl = ndi.binary_dilation(ph.roi_mask, iterations=3)
        for k in (0, 4, 6, 10):
            for ax in ((0,) if k == 0 else (0, 1, 2)):
                sh = [0, 0, 0]
                sh[ax] = k
                q = registration_qc(img, ndi.shift(img, sh, order=1, mode="nearest"), exclude=excl, spacing_um=SP)
                rows.append({"phantom": name, "shift_um": k * 40, "axis": ax, "pass": bool(q["pass"]),
                             "residual_shift_um_max": q["residual_shift_um_max"], "reason": q.get("reason"),
                             "unverifiable_direction": q.get("unverifiable_direction")})
                print(rows[-1], flush=True)
    harmful = [r for r in rows if r["shift_um"] > 80]
    summ = {"n": len(rows), "misregistrations_passed": int(sum(r["pass"] for r in harmful)),
            "n_misregistrations": len(harmful),
            "aligned_passed": {n: any(r["pass"] for r in rows if r["phantom"] == n and r["shift_um"] == 0) for n in CASES}}
    print(summ)
    save_result("exp_L5_qc_axial", {"experiment": "L5", "summary": summ, "rows": rows, "seconds": time.time() - t0})


if __name__ == "__main__":
    main()
