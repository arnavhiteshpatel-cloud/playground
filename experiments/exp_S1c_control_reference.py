"""Experiment S1c — measured new-bone reference from empty-defect controls vs the assumed maturity range.

S1b showed the advisor is conservative: it refused 29 of 96 sweep conditions whose advisor-threshold
measurement was in fact accurate, largely because the assumed new-bone range (0.60–1.00 of host) is wide.
In a real study design, empty-defect control animals at the same timepoint provide measured new-bone
intensities. Here a control phantom (same model, stage and imaging as the treated specimen but no graft,
different seed = different animal) supplies new-bone voxel intensities (in relative units, using the
control scan's own soft/host levels); the advisor then decides with `new_samples_rel`.
Same sweep as S1b Part B (graft 650–2200 mgHA/cm³ × σ 30–250, 3 specimens). Outcome: failure refusal
sensitivity (must stay ≥95%) and number of accurate measurements refused (cost).
"""
import numpy as np

from common import save_result
from exp_C_separability import make_structures, mu_with_graft
from exp_S1_advisor import graft_err, summarize
from osteoquant.advisor import MaterialProfile, scan_relative_units, to_relative
from osteoquant.advisor.integration import advisor_threshold_segmentation, support_for_scan
from osteoquant.phantom import PhantomConfig, generate_phantom, ImagingConfig, render_fast

phs = make_structures(4)
ctrl = generate_phantom(PhantomConfig(model="condyle", shape=(56, 72, 72), voxel_um=40, supersample=2,
                                      defect_diameter_um=2000, graft_material=None, healing_stage=0.55, seed=777))
rows = []
for X in (2200, 1600, 1300, 1150, 1000, 900, 800, 650):
    for s in (30, 80, 150, 250):
        cimg = render_fast(ctrl.mu, 40, ImagingConfig(seed=99, psf_sigma_um=20, noise_sigma=s)).data
        lv = scan_relative_units(cimg, exclude_mask=ctrl.roi_mask)
        nb = to_relative(cimg[(ctrl.labels == 1) & ctrl.roi_mask], lv["soft"], lv["host"])
        for i in range(1, 4):
            ph = phs[i]
            img = render_fast(mu_with_graft(ph, X), 40, ImagingConfig(seed=10 + i, psf_sigma_um=20, noise_sigma=s)).data
            prof = MaterialProfile(id=f"char_{X}", rel_mean=X / 1075.0, rel_sd=0.04 * X / 1075.0, struct_um=450)
            for tag, cfg in (("assumed_range", {"material": prof}),
                             ("control_reference", {"material": prof, "new_bone_reference_rel": nb})):
                sup = support_for_scan(img, ph.roi_mask, (40.0,) * 3, cfg)
                lab, info = advisor_threshold_segmentation(img, ph.roi_mask, (40.0,) * 3, cfg)
                e, vt = graft_err(lab, ph.labels, ph.roi_mask)
                rows.append({"graft_mgHA": X, "noise": s, "specimen": i, "method": tag, "err": e,
                             "status": sup["endpoints"]["residual_graft_volume"]["status"],
                             "oracle": sup["intensity"].get("dice_graft")})
        print(X, s, [(r["method"][:4], r["status"][:4], round(r["err"], 3)) for r in rows[-2:]], flush=True)
summ = [summarize(rows, m) for m in ("assumed_range", "control_reference")]
for x in summ:
    print(x)
save_result("exp_S1c_control_reference", {"experiment": "S1c", "summary": summ, "rows": rows,
                                          "note": "control phantom = different animal (seed 777), same stage/imaging"})
