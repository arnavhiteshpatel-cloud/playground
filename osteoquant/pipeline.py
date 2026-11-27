"""End-to-end DefectFill analysis for one scan: QC → ROI → segmentation → uncertainty →
plausibility → morphometry. Pure function of (volume, config); the config snapshot and every
artifact hash are returned so that results are reproducible and auditable.

Segmentation methods:
  "multiotsu"   classical, material-aware intensity split (needs graft_brighter)
  "ctan_style"  manual/global two-threshold workflow (thresholds in config)
  "advisor_threshold"  threshold implied by the measurement-support advisor (material model + scan levels)
  "rf:<path>"   pickled RFSegmenter (joblib)
  "unet:<name>" locked U-Net from models/registry.json (sha256 verified)
"""
from __future__ import annotations

import hashlib
import json
import time

import numpy as np

from . import __version__
from .volume import Volume

DEFAULT_CONFIG = {
    "defect_model": "condyle",            # condyle | calvarial | segmental | manual
    "nominal_diameter_um": None,
    "segmentation": "multiotsu",
    "graft_brighter": True,
    "abstain_tau": 0.6,                   # max-softmax below which voxels are marked uncertain
    "tta": True,
    "thickness_metrics": True,
    "qc": True,
    "no_graft": False,                    # e.g. distraction osteogenesis / empty-defect controls
    "material": None,                     # graft material id (osteoquant.knowledge); None = unspecified
    "calibrated": False,                  # HA phantom calibration recorded for this scan
    "day0": None,                         # {"registered", "qc_pass", "max_displacement_um", "tolerance_um"}
    "measurement_support": True,          # run the advisor; unsupported endpoints are not reported
}


def config_hash(cfg: dict) -> str:
    return hashlib.sha256(json.dumps(cfg, sort_keys=True, default=str).encode()).hexdigest()


def labels_hash(lab: np.ndarray) -> str:
    return hashlib.sha256(np.ascontiguousarray(lab).tobytes() + str(lab.shape).encode()).hexdigest()


def run_roi(vol: Volume, cfg: dict, roi_dict: dict | None = None):
    from .roi import ROI, detect_plate_defect, detect_segmental_gap, ROIDetectionError
    if roi_dict:
        roi = ROI.from_dict(roi_dict)
        return roi, roi.to_mask(vol.shape, vol.spacing, vol.origin), None
    try:
        if cfg["defect_model"] == "segmental":
            roi = detect_segmental_gap(vol.data, vol.spacing)
        else:
            roi = detect_plate_defect(vol.data, vol.spacing, model=cfg["defect_model"],
                                      nominal_diameter_um=cfg.get("nominal_diameter_um"))
        return roi, roi.to_mask(vol.shape, vol.spacing, vol.origin), None
    except ROIDetectionError as e:
        return None, None, str(e)


def segment(vol: Volume, roi_mask: np.ndarray, cfg: dict, progress=lambda f, m: None):
    """Returns (labels, probabilities or None, info)."""
    from .segment import classical as C
    method = cfg["segmentation"]
    info = {"method": method}
    if method == "multiotsu":
        lab, th = C.seg_multiotsu(vol.data, roi_mask, cfg.get("graft_brighter", True))
        info["thresholds"] = th
        return lab, None, info
    if method == "advisor_threshold":
        from .advisor.integration import advisor_threshold_segmentation
        lab, info2 = advisor_threshold_segmentation(vol.data, roi_mask, vol.spacing, cfg)
        info.update(info2)
        return lab, None, info
    if method == "ctan_style":
        lab = C.seg_ctan_style(vol.data, roi_mask, cfg["t_mineral"], cfg["t_graft"], cfg.get("graft_brighter", True))
        info["thresholds"] = {"t_mineral": cfg["t_mineral"], "t_graft": cfg["t_graft"]}
        return lab, None, info
    if method.startswith("rf:"):
        if not cfg.get("_trusted_local", False):
            raise PermissionError("Pickled RF models can only be used from the trusted local CLI")
        import joblib
        rf = joblib.load(method[3:])
        lab, p = rf.predict(vol.data, vol.spacing, roi_mask)
        full = np.zeros((4,) + lab.shape, np.float32)
        for i, c in enumerate(rf.clf.classes_):
            full[int(c)] = p[i]
        return lab, full, info
    if method.startswith("unet:"):
        from .ml.train import load_model, predict_proba, Case
        name = method[5:]
        model, ck = load_model(name)   # name-only, registry-hash verified before safe deserialisation
        info.update({"model_name": name, "model_sha256": ck["sha256"], "model_provenance": ck["provenance"],
                     "licence_tag": ck["licence_tag"]})
        if cfg.get("expected_model_sha256") and cfg["expected_model_sha256"] != ck["sha256"]:
            raise RuntimeError("Model hash mismatch: locked model version changed")
        case = Case("scan", vol.data, None, roi_mask, vol.spacing)
        progress(0.4, "U-Net inference")
        p = predict_proba(model, case, ck["cfg"], tta=cfg.get("tta", True))
        lab = p.argmax(0).astype(np.uint8)
        return lab, p, info
    raise ValueError(f"Unknown segmentation method {method}")


def analyze(vol: Volume, cfg: dict | None = None, roi_dict: dict | None = None, progress=lambda f, m: None) -> dict:
    from .qc import run_qc
    from .morphometry import defect_report_metrics
    from .uncertainty import predictive_entropy, abstain, plausibility_checks
    c = dict(DEFAULT_CONFIG)
    c.update(cfg or {})
    t0 = time.time()
    out = {"software_version": __version__, "config": c, "config_sha256": config_hash(c),
           "volume_content_sha256": vol.content_hash(), "timings": {}}
    if c["qc"]:
        progress(0.05, "QC")
        t = time.time()
        out["qc"] = run_qc(vol)
        out["timings"]["qc_s"] = round(time.time() - t, 2)
    progress(0.15, "ROI")
    t = time.time()
    roi, roi_mask, err = run_roi(vol, c, roi_dict)
    out["timings"]["roi_s"] = round(time.time() - t, 2)
    if roi is None:
        out["status"] = "needs_manual_roi"
        out["roi_error"] = err
        return out
    out["roi"] = roi.to_dict() if roi.kind != "mask" else {"kind": "mask", "params": {"mask_sha256": roi.params["mask_sha256"]}}
    progress(0.3, "segmentation")
    t = time.time()
    lab, prob, info = segment(vol, roi_mask, c, progress)
    if c.get("no_graft"):
        lab = np.where(lab == 2, 1, lab).astype(np.uint8)   # no graft present: all mineral in ROI is new bone
        if prob is not None:
            prob = prob.copy(); prob[1] += prob[2]; prob[2] = 0
        info["no_graft"] = True
    out["timings"]["segmentation_s"] = round(time.time() - t, 2)
    out["segmentation"] = info
    if prob is not None:
        ent = predictive_entropy(prob)
        lab_a = abstain(prob, c["abstain_tau"], mask=roi_mask)
        out["uncertainty"] = {"mean_entropy_roi": float(ent[roi_mask].mean()),
                              "abstained_frac_roi": float((lab_a[roi_mask] == 255).mean()),
                              "tau": c["abstain_tau"]}
        out["_entropy"] = ent
        lab_report = lab_a
    else:
        lab_report = lab
    out["_labels"] = lab_report
    out["_roi_mask"] = roi_mask
    out["labels_sha256"] = labels_hash(lab_report)
    out["plausibility"] = plausibility_checks(lab_report, roi_mask)
    progress(0.7, "morphometry")
    t = time.time()
    out["metrics"] = defect_report_metrics(lab_report, roi_mask, vol, axis=0, thickness=c["thickness_metrics"])
    out["timings"]["morphometry_s"] = round(time.time() - t, 2)
    if c.get("measurement_support", True):
        progress(0.9, "measurement support")
        from .advisor.integration import support_for_scan, apply_support
        t = time.time()
        out["measurement_support"] = support_for_scan(vol.data, roi_mask, vol.spacing, c)
        out["reported_metrics"], out["suppressed_metrics"] = apply_support(out["metrics"], out["measurement_support"])
        out["timings"]["support_s"] = round(time.time() - t, 2)
    out["timings"]["total_s"] = round(time.time() - t0, 2)
    out["status"] = "complete_unreviewed"
    progress(1.0, "done")
    return out


def public(result: dict) -> dict:
    """Strip in-memory arrays (keys starting with '_') for JSON storage."""
    return {k: v for k, v in result.items() if not k.startswith("_")}
