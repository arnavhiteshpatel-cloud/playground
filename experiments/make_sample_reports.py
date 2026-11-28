"""Generate the three sample DefectFill reports from actual project computations.

Report 1 — SYNTHETIC benchmark study: 16 held-out synthetic specimens (4 materials), automatic
           ROI detection (nominal diameter), synthetic-trained U-Net (unet_ctx_s0) with TTA and
           abstention; measured vs ground-truth fractions; groups = graft material.
Report 2 — PUBLIC real data: ovine metatarsal distraction callus (Zenodo 17255310, CC-BY-4.0),
           days 18 and 161, decimated ×4 (98 µm voxels); automatic segmental-gap ROI; classical
           multi-Otsu with no-graft mode; unreviewed automated output; no ground truth.
Report 3 — SYNTHETIC longitudinal study: 3 specimens × 2 materials (beta-TCP, HA) imaged at four
           healing stages; per-timepoint analysis by the U-Net; group = material, timepoint = stage.
No customer data is used; every report is watermarked with its data class.
"""
import json

import numpy as np

from common import ROOT, load_split, FIG
from osteoquant.pipeline import analyze, public
from osteoquant.report import build_pdf, specimen_panel, group_dotplot
from osteoquant.api.bundle import ENDPOINTS, git_commit
from osteoquant.volume import Volume
from osteoquant.segment.metrics import multiclass_metrics
from osteoquant import __version__

OUT = ROOT / "reports_samples"
OUT.mkdir(exist_ok=True)
FIGD = OUT / "fig"
# Generation-1 samples are superseded (cycle-3 review, C2-BIZ-07 residual); they are written apart from current samples.
OLD = OUT / "superseded"
OLD.mkdir(exist_ok=True)
FIGD.mkdir(exist_ok=True)
LIM_SYN = ["All data are computational phantoms; performance on synthetic data does not establish performance on "
           "real tissue or real graft materials.",
           "The segmentation model was trained only on synthetic phantoms from the same generator family "
           "(optimistic: shared morphology priors).",
           "Densities are simulated HA-equivalent values; no physical calibration.",
           "Graft vs new-bone separability for any real material is untested pending physical phantom scans."]


def spec_entry(sid, group, tp, vol, res, truth=None, labels_true=None, source="", sha=""):
    fig = str(FIGD / f"{sid}.png")
    specimen_panel(vol.data, res["_labels"], res["_roi_mask"], vol.spacing, fig, title=f"{sid} — {group} · {tp}")
    e = {"specimen_id": sid, "group": group, "timepoint": tp,
         "scan": {"source": source, "sha256": sha or res["volume_content_sha256"], "shape": list(vol.shape),
                  "spacing_um": list(vol.spacing)},
         "qc": res.get("qc", {}), "roi": res.get("roi", {}), "segmentation": res["segmentation"],
         # Gen-2: reports use the measurement-support view (refused endpoints are None, conditions printed)
         "metrics": res.get("reported_metrics", res["metrics"]), "suppressed_metrics": res.get("suppressed_metrics", []),
         "measurement_support": {k: {"status": v.get("status"), "reason": v.get("reason"), "mechanism": v.get("mechanism"),
                                     "conditions": v.get("conditions", [])}
                                 for k, v in (res.get("measurement_support") or {}).get("endpoints", {}).items()},
         "advisor_version": (res.get("measurement_support") or {}).get("advisor_version"),
         "analysis_parameters": {k: v for k, v in res["segmentation"].items()
                                 if k in ("method", "t_mineral", "t_graft", "model_name", "runtime")},
         "uncertainty": res.get("uncertainty", {}), "plausibility": res["plausibility"],
         "figure": fig, "corrections": []}
    if truth is not None:
        e["truth"] = truth
        r = multiclass_metrics(res["_labels"], labels_true, spacing=vol.spacing, mask=res["_roi_mask"], classes=(1, 2),
                               distances=False)
        e["eval"] = {"dice_new": r["per_class"]["new_bone"]["dice"], "dice_graft": r["per_class"]["graft"]["dice"]}
    return e


def report1():
    test = load_split("test")
    specs, exceptions = [], []
    for c in test:
        vol = Volume(c.image, c.spacing, meta={"ingest": {"metadata_found": {"spacing_um": list(c.spacing)}}})
        model = c.meta["spec"]["model"]
        cfg = {"defect_model": model, "nominal_diameter_um": c.meta["phantom_config"]["defect_diameter_um"] if model != "segmental" else None,
               "segmentation": "unet:unet_ctx_s0", "tta": True, "abstain_tau": 0.6,
               "material": c.meta["spec"]["material"]}            # Gen-2: the advisor needs the graft material
        res = analyze(vol, cfg)
        if res.get("status") != "complete_unreviewed":
            exceptions.append({"specimen_id": c.case_id.replace("test_", "S"), "stage": "ROI detection",
                               "reason": str(res.get("roi_error")) + " (healing has bridged the segmental gap)",
                               "action": "Define ROI from the surgical record / day-0 scan, then re-run"})
            print("ROI failed", c.case_id, res.get("roi_error")); continue
        mat = {"beta_tcp": "beta-TCP", "bcp": "BCP", "ha": "HA", "calcium_sulfate": "CaSO4"}[c.meta["spec"]["material"]]
        specs.append(spec_entry(c.case_id.replace("test_", "S"), mat, f"stage {c.meta['spec']['stage']:.2f}", vol, res,
                                c.meta["truth"], c.labels, "synthetic phantom (generator v1.0.0)"))
        print("R1", c.case_id, specs[-1]["eval"], flush=True)
    for s in specs:
        s["timepoint"] = "mixed stages"
    b = {"title": "SYNTHETIC benchmark — three-class DefectFill analysis of 16 phantoms (4 graft materials)",
         "study": {"name": "Synthetic benchmark (Experiment B test set)", "species": "in silico", "defect_model":
                   "condyle / calvarial / segmental phantoms", "graft_materials": "beta-TCP, BCP, HA, CaSO4 (simulated)", "blinded": False},
         "data_class": "synthetic", "review_status": "unreviewed_automated", "specimens": specs, "endpoints": ENDPOINTS,
         "reference_group": "HA", "exceptions": exceptions,
         "summary_text": (f"Mean Dice vs known truth in the defect ROI: new bone {np.mean([s['eval']['dice_new'] for s in specs]):.3f}, "
                          f"residual graft {np.mean([s['eval']['dice_graft'] for s in specs]):.3f} (n={len(specs)} synthetic specimens; "
                          "automatic ROI). These figures describe synthetic data only."),
         "methods_text": ("Synthetic phantoms with exact voxel ground truth were generated (procedural host anatomy, granule packing, "
                          "resorption and osteoconductive ingrowth) and rendered with blur, noise and scanner gain/offset variation. "
                          "Automatic cylindrical/segmental ROI detection used the nominal defect diameter. Segmentation used a 3D U-Net "
                          "trained on 48 separate synthetic specimens, with 4-flip test-time augmentation; voxels with max softmax < 0.6 "
                          "were labelled uncertain. Volumes are voxel counts within the ROI."),
         "limitations": LIM_SYN, "reproducibility": {"software_version": __version__, "git_commit": git_commit(),
                                                     "model": "unet_ctx_s0 (see models/registry.json for SHA-256)"},
         "max_figures": 4}
    b["group_figures"] = [group_dotplot(b, ENDPOINTS[1:5], str(FIGD / "r1_groups.png"))]
    return build_pdf(b, OLD / "DefectFill_SAMPLE1_synthetic_benchmark.pdf", OLD / "DefectFill_SAMPLE1_synthetic_benchmark.csv")


def report2():
    from osteoquant.io import read_volume
    specs, exceptions = [], []
    for f, days in (("18DAYS_recon.txm", 18), ("161DAYS_recon.txm", 161)):
        p = ROOT / "data" / "raw" / "zenodo_17255310" / f
        vol, rep = read_volume(p, step=4)
        res = analyze(vol, {"defect_model": "segmental", "segmentation": "multiotsu", "no_graft": True, "thickness_metrics": False})
        if res.get("status") != "complete_unreviewed":
            qcw = [c["name"] for c in res.get("qc", {}).get("checks", []) if c["status"] in ("warn", "fail")]
            exceptions.append({"specimen_id": f"OV-{days}d", "stage": "ROI detection",
                               "reason": f"{res.get('roi_error')}. QC warnings: {'; '.join(qcw)}. Visual review: dense hardware/holder "
                                         "at one end (saturated voxels) and a consolidated regenerate without an open gap.",
                               "action": "Analyst defines ROI manually (landmarks) and masks hardware; then re-run."})
            print("ROI failed", f); continue
        specs.append(spec_entry(f"OV-{days}d", "distraction (no graft)", f"day {days}", vol, res,
                                source=f"Zenodo 17255310 / {f} (decimated ×4)", sha=rep.files[0]["sha256"]))
        print("R2", f, res["metrics"]["class_volumes"], flush=True)
    b = {"title": "PUBLIC DATA — ovine metatarsal distraction callus, day 18 vs day 161 (Zenodo 17255310)",
         "study": {"name": "Reanalysis of public ovine bone-lengthening micro-CT", "species": "sheep (Ovis aries)",
                   "defect_model": "metatarsal distraction osteogenesis (segmental gap analogue)", "graft_materials": "none", "blinded": False},
         "data_class": "public", "review_status": "unreviewed_automated", "specimens": specs, "endpoints": ENDPOINTS[:3] + ENDPOINTS[4:6],
         "exceptions": exceptions,
         "summary_text": ("Automated reanalysis of two publicly released Zeiss Xradia scans (CC-BY-4.0; PID2020-113790RB-I00 data set). "
                          "The two timepoints come from the dataset as released; whether they are the same animal is not stated, so no "
                          "longitudinal inference is drawn. No expert segmentation exists for these scans: values are unvalidated."),
         "methods_text": ("TXM volumes (24.6 µm voxels, 60 kV per reconstruction settings) were read slice-lazily and decimated ×4 "
                          "(98.4 µm voxels) to fit the demonstration budget; this decimation degrades thin-structure measurements. "
                          "A segmental-gap ROI was detected automatically from the cortical-annulus density profile. Mineral was "
                          "segmented with multi-Otsu; with no graft present, all mineral inside the ROI is labelled new bone and mineral "
                          "outside is host bone."),
         "limitations": ["No ground truth; results are unvalidated automated output.",
                         "×4 decimation (98 µm) under-resolves trabeculae; BV/TV is resolution dependent.",
                         "ROI detection confidence was below the review threshold for at least one scan — an analyst must confirm the gap boundaries.",
                         "Grey values are uncalibrated; no density units are reported.",
                         "Distraction osteogenesis is not a graft-filled defect; this report demonstrates ingestion, ROI and reporting on real data only."],
         "reproducibility": {"software_version": __version__, "git_commit": git_commit(), "dataset": "doi:10.5281/zenodo.17255310",
                             "licence": "CC-BY-4.0"}}
    return build_pdf(b, OLD / "DefectFill_SAMPLE2_public_ovine_callus.pdf", OLD / "DefectFill_SAMPLE2_public_ovine_callus.csv")


def report3():
    from osteoquant.phantom import PhantomConfig, generate_phantom, render_fast, ImagingConfig
    specs = []
    for mat, label in (("beta_tcp", "beta-TCP"), ("ha", "HA")):
        mat_id = mat
        for k in range(3):
            for stage in (0.15, 0.4, 0.65, 0.9):
                ph = generate_phantom(PhantomConfig(model="condyle", shape=(72, 80, 80), voxel_um=40, defect_diameter_um=2000,
                                                    graft_material=mat, healing_stage=stage, seed=5000 + 10 * k + (mat == "ha")))
                v = render_fast(ph.mu, 40, ImagingConfig(psf_sigma_um=25, noise_sigma=60, seed=k))
                v.meta["ingest"] = {"metadata_found": {"spacing_um": list(v.spacing)}}
                res = analyze(v, {"defect_model": "condyle", "nominal_diameter_um": 2000, "segmentation": "unet:unet_ctx_s0", "material": mat_id,
                                  "tta": False, "thickness_metrics": False, "qc": False})
                if res.get("status") != "complete_unreviewed":
                    continue
                specs.append(spec_entry(f"L-{label}-{k+1}@{stage}", label, f"stage {stage:.2f}", v, res, ph.truth, ph.labels,
                                        "synthetic longitudinal phantom"))
                print("R3", mat, k, stage, specs[-1]["eval"], flush=True)
    for s in specs[1:]:
        s["figure"] = s["figure"] if s["timepoint"] == "stage 0.90" else None
    b = {"title": "SYNTHETIC longitudinal study — graft resorption and ingrowth, beta-TCP vs HA (4 stages × 3 specimens)",
         "study": {"name": "Synthetic longitudinal design demonstration", "species": "in silico", "defect_model": "condyle phantom",
                   "graft_materials": "beta-TCP vs HA (simulated)", "blinded": False},
         "data_class": "synthetic", "review_status": "unreviewed_automated", "specimens": specs, "endpoints": ENDPOINTS[1:5],
         "reference_group": "HA",
         "summary_text": "Demonstrates per-timepoint group summaries and between-material comparisons on synthetic data with known truth.",
         "methods_text": ("For each specimen, phantoms at four healing stages share host anatomy and initial granule packing; resorption "
                          "and ingrowth rates follow the generator's assumed material-specific rules (beta-TCP resorbs faster than HA). "
                          "Each timepoint was analysed independently with the synthetic-trained U-Net."),
         "limitations": LIM_SYN + ["Group differences reflect the generator's assumed resorption rates, not material biology."],
         "reproducibility": {"software_version": __version__, "git_commit": git_commit()}, "max_figures": 2}
    b["group_figures"] = [group_dotplot(b, ENDPOINTS[2:4], str(FIGD / "r3_groups.png"))]
    return build_pdf(b, OLD / "DefectFill_SAMPLE3_synthetic_longitudinal.pdf", OLD / "DefectFill_SAMPLE3_synthetic_longitudinal.csv")


if __name__ == "__main__":
    import sys
    which = sys.argv[1:] or ["1", "2", "3"]
    for w in which:
        print({"1": report1, "2": report2, "3": report3}[w]())
