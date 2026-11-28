"""Experiment S1H5 — held-out precision test of advisor 1.4.3 for HA residual graft (PREREGISTRATION §11).

Unseen seeds: condyle 6300–6323, segmental 6400–6423 (48 structures); knowledge-base material `ha`; PSF 20/40 µm;
correlated noise 60/120; healing stage 0.5. Primary analysis: residual graft with phantom structures as the unit.
Advisor 1.4.3 frozen. The analysis code is the S1H4 analysis (all endpoints are reported; only residual graft carries
the acceptance rule).
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
from scipy import ndimage as ndi
from scipy.stats import beta

from common import save_result
from exp_S1_advisor import endpoint_errs, graft_err
from osteoquant.advisor.integration import advisor_threshold_segmentation, support_for_scan
from osteoquant.advisor.separability import ADVISOR_VERSION
from osteoquant.phantom import ImagingConfig, PhantomConfig, generate_phantom, render_fast

MODELS = {"condyle": (range(6300, 6324), dict(shape=(56, 72, 72), defect_diameter_um=2000, graft_diam_um=(300, 600),
                                              graft_fill=0.30)),
          "segmental": (range(6400, 6424), dict(shape=(80, 72, 72), gap_length_um=1600, graft_diam_um=(400, 700),
                                                graft_fill=0.30))}
MATERIALS = ("ha",)
WEEKS = {"bcp": 2.0, "beta_tcp": 2.0}
PSFS = (20, 40)
NOISE = (60, 120)
EPS = (("residual_graft_volume", "err_graft", "status"), ("new_bone_volume", "err_new", "status_new"),
       ("total_mineral_volume", "err_mineral", "status_mineral"))
SUP = ("supported", "supported_with_conditions")


def correlated_noise(shape, sigma, seed):
    rng = np.random.default_rng(seed)
    n = ndi.gaussian_filter(rng.standard_normal(shape).astype(np.float32), 1.0)
    return (n / (n.std() + 1e-9) * sigma).astype(np.float32)


def cp_upper(x, n, a=0.05):
    if n == 0:
        return None
    return 1.0 if x == n else float(beta.ppf(1 - a / 2, x + 1, n - x))


def analyse(rows):
    out = {}
    for ep, ek, sk in EPS:
        fin = [r for r in rows if np.isfinite(r[ek])]
        fail = [r for r in fin if abs(r[ek]) > 0.2]
        sup = [r for r in fin if r[sk] in SUP]
        sbf = [r for r in sup if abs(r[ek]) > 0.2]
        structs = sorted({r["structure"] for r in sup})
        failing_structs = sorted({r["structure"] for r in sbf})
        k = len(structs)
        ub = cp_upper(len(failing_structs), k)
        sens = (len(fail) - len([r for r in fail if r[sk] in SUP])) / len(fail) if fail else None
        if sbf:
            verdict = "FAIL (supported failure)"
        elif sens is not None and sens < 0.95:
            verdict = "FAIL (sensitivity)"
        elif ub is not None and ub <= 0.10:
            verdict = "PASS"
        else:
            verdict = "not demonstrated (too few structures with supported measurements)"
        out[ep] = {"n": len(fin), "n_fail": len(fail), "failures_refused": len(fail) - len([r for r in fail if r[sk] in SUP]),
                   "sensitivity": sens, "n_supported": len(sup), "supported_but_failed": len(sbf),
                   "coverage": len(sup) / len(fin) if fin else None,
                   "structures_with_support": k, "failing_structures": failing_structs,
                   "structure_upper95": ub, "row_upper95": cp_upper(len(sbf), len(sup)),
                   "abs_err_supported_median": float(np.median([abs(r[ek]) for r in sup])) if sup else None,
                   "abs_err_supported_max": float(max(abs(r[ek]) for r in sup)) if sup else None,
                   "supported_failures_detail": [{k_: r[k_] for k_ in ("structure", "arm", "psf_um", "noise", ek)}
                                                 for r in sbf],
                   "verdict": verdict}
        out[ep]["by_arm"] = {}
        for arm in sorted({r["arm"] for r in rows}):
            ra = [r for r in fin if r["arm"] == arm]
            sa = [r for r in ra if r[sk] in SUP]
            out[ep]["by_arm"][arm] = {"n": len(ra), "supported": len(sa),
                                      "supported_but_failed": sum(abs(r[ek]) > 0.2 for r in sa)}
    none = sum(1 for r in rows if all(r[sk] not in SUP for _, _, sk in EPS))
    out["no_volume_endpoint_supported_fraction"] = none / len(rows) if rows else None
    return out


PARTIAL = Path(__file__).resolve().parent / "results" / "exp_S1H5_partial.jsonl"


def _load_partial():
    """Rows of structures completed before an interruption (container restarts can stop long runs). Execution only:
    rows are deterministic per structure, and nothing is analysed until all are done."""
    done = {}
    if PARTIAL.exists():
        for line in PARTIAL.read_text().splitlines():
            if line.strip():
                rec = json.loads(line)
                if rec.get("advisor_version") == ADVISOR_VERSION:
                    done[rec["structure"]] = rec["rows"]
    return done


def main():
    assert ADVISOR_VERSION == "1.4.3", "S1H5 is pre-registered for advisor 1.4.3"
    t0 = time.time()
    rows = []
    done = _load_partial()
    for model, (seeds, kw) in MODELS.items():
        for seed in seeds:
            if f"{model}_{seed}" in done:
                rows += done[f"{model}_{seed}"]
                continue
            n0 = len(rows)
            for mat in MATERIALS:
                ph = generate_phantom(PhantomConfig(model=model, voxel_um=40, supersample=2, graft_material=mat,
                                                    healing_stage=0.50, seed=seed, periodic_texture=False, **kw))
                for psf in PSFS:
                    clean = render_fast(ph.mu, 40, ImagingConfig(seed=seed, psf_sigma_um=psf, noise_sigma=0.0)).data
                    for s in NOISE:
                        img = clean + correlated_noise(clean.shape, s, seed * 100 + s + psf)
                        arms = [(mat, mat)]
                        for arm, mid in arms:
                            cfg = {"material": mid, "healing_weeks": WEEKS.get(mat)}
                            sup = support_for_scan(img, ph.roi_mask, (40.0,) * 3, cfg)
                            lab, _ = advisor_threshold_segmentation(img, ph.roi_mask, (40.0,) * 3, cfg)
                            e, vt = graft_err(lab, ph.labels, ph.roi_mask)
                            ep = sup["endpoints"]
                            rows.append({"structure": f"{model}_{seed}", "arm": arm, "psf_um": psf, "noise": s,
                                         **endpoint_errs(lab, ph.labels, ph.roi_mask), "err_graft": e, "graft_vox": vt,
                                         "status": ep["residual_graft_volume"]["status"],
                                         "status_new": ep["new_bone_volume"]["status"],
                                         "status_mineral": ep["total_mineral_volume"]["status"],
                                         "scan_measured": (sup.get("inputs") or {}).get("scan_measured")})
            with PARTIAL.open("a") as f:
                f.write(json.dumps({"structure": f"{model}_{seed}", "advisor_version": ADVISOR_VERSION,
                                    "rows": rows[n0:]}, default=float) + "\n")
            print(model, seed, len(rows), round(time.time() - t0), flush=True)
    res = analyse(rows)
    for ep, _, _ in EPS:
        print(ep, {k: v for k, v in res[ep].items() if k not in ("by_arm", "supported_failures_detail")})
    save_result("exp_S1H5_heldout", {"experiment": "S1H5", "preregistered": "docs/science/PREREGISTRATION.md §11",
                                     "advisor_version": ADVISOR_VERSION, "analysis": res, "rows": rows,
                                     "seconds": time.time() - t0})


if __name__ == "__main__":
    main()
