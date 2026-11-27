"""Experiment S1b — does the advisor's own threshold approach the oracle where support is granted?

Same specimens and conditions as S1 (Part A: 56 dataset specimens; Part B: density × noise sweep).
Method: `advisor_threshold` (graft threshold = oracle threshold of the advisor's material model, mapped to
grey values via soft/host levels measured outside the defect). Compared with multi-Otsu from S1.
"""
from __future__ import annotations

import json
import time

import numpy as np

from common import load_split, save_result, RESULTS
from exp_C_separability import make_structures, mu_with_graft
from exp_S1_advisor import graft_err, summarize, endpoint_errs
from osteoquant.advisor.separability import ADVISOR_VERSION
from osteoquant.advisor import MaterialProfile, dice_oracle_volume
from osteoquant.advisor.integration import advisor_threshold_segmentation, support_for_scan
from osteoquant.phantom import ImagingConfig, render_fast


def main():
    t0 = time.time()
    rows = []
    for c in load_split("test") + load_split("ood_mat"):
        cfg = {"material": c.meta["spec"]["material"]}
        sup = support_for_scan(c.image, c.roi, c.spacing, cfg)
        lab, info = advisor_threshold_segmentation(c.image, c.roi, c.spacing, cfg)
        e, vt = graft_err(lab, c.labels, c.roi)
        tor = dice_oracle_volume(c.image, c.labels, c.roi)
        rows.append({"part": "A", "case": c.case_id, "material": cfg["material"], "method": "advisor_threshold",
                     **endpoint_errs(lab, c.labels, c.roi),
                     "err": e, "advisor_oracle_dice": sup["intensity"].get("dice_graft"),
                     "true_oracle_dice": tor["dice_graft"], "status": sup["endpoints"]["residual_graft_volume"]["status"], "graft_vox": vt})
        print("A", c.case_id, rows[-1]["status"], round(e, 3), flush=True)
    phs = make_structures(4)
    for X in (2200, 1600, 1300, 1150, 1000, 900, 800, 650):
        for s in (30, 80, 150, 250):
            for i in range(1, 4):
                ph = phs[i]
                img = render_fast(mu_with_graft(ph, X), 40, ImagingConfig(seed=10 + i, psf_sigma_um=20, noise_sigma=s)).data
                prof = MaterialProfile(id=f"char_{X}", rel_mean=X / 1075.0, rel_sd=0.04 * X / 1075.0, struct_um=450)
                cfg = {"material": prof}
                sup = support_for_scan(img, ph.roi_mask, (40.0,) * 3, cfg)
                lab, info = advisor_threshold_segmentation(img, ph.roi_mask, (40.0,) * 3, cfg)
                e, vt = graft_err(lab, ph.labels, ph.roi_mask)
                tor = dice_oracle_volume(img, ph.labels, ph.roi_mask)
                rows.append({"part": "B", "case": f"X{X}_s{s}_{i}", "graft_mgHA": X, "noise": s,
                             **endpoint_errs(lab, ph.labels, ph.roi_mask),
                             "method": "advisor_threshold_B", "err": e,
                             "advisor_oracle_dice": sup["intensity"].get("dice_graft"),
                             "true_oracle_dice": tor["dice_graft"], "true_oracle_threshold": tor.get("threshold"),
                             "advisor_threshold_grey": info.get("t_graft"),
                             "status": sup["endpoints"]["residual_graft_volume"]["status"], "graft_vox": vt})
            print("B", X, s, rows[-1]["status"], round(np.mean([r["err"] for r in rows[-3:]]), 3),
                  "adv_oracle", round(rows[-1]["advisor_oracle_dice"] or -1, 3), "true_oracle", round(rows[-1]["true_oracle_dice"], 3),
                  "t_adv", round(rows[-1]["advisor_threshold_grey"] or -1), "t_true", round(rows[-1]["true_oracle_threshold"] or -1), flush=True)
    summ = [summarize(rows, m) for m in ("advisor_threshold", "advisor_threshold_B")]
    for s_ in summ:
        print(s_)
    save_result("exp_S1b_advisor_threshold", {"experiment": "S1b", "summary": summ, "rows": rows,
                                              "seconds": time.time() - t0,
                                              "advisor_version": ADVISOR_VERSION})


if __name__ == "__main__":
    main()
