"""Connects the measurement-support advisor to pipeline results.

``support_for_scan`` assesses one scan; ``apply_support`` produces the *reported* metrics, in which
every endpoint that is not supported is replaced by ``None`` and listed with its reason. The raw
metrics remain available (for audit and research) but reports and exports use the reported view.
"""
from __future__ import annotations

import copy

import numpy as np

from .separability import CONDITIONAL, NOT_SUPPORTED, SUPPORTED, assess_support, scan_relative_units, to_relative

# endpoint → metric paths (dot-separated into the defect_report_metrics dict)
ENDPOINT_METRICS = {
    "residual_graft_volume": ["class_volumes.residual_graft_volume_mm3"],
    "graft_fraction_of_defect": ["class_volumes.residual_graft_fraction",
                                 "class_volumes.residual_graft_fraction_of_certain", "density.residual_graft"],
    "new_bone_volume": ["class_volumes.new_bone_volume_mm3"],
    "new_bone_fraction_of_defect": ["class_volumes.new_bone_fraction", "class_volumes.new_bone_fraction_of_certain",
                                    "bridging_new_bone", "radial_ingrowth", "density.new_bone"],
    "new_bone_thickness": ["new_bone_architecture"],
    "total_mineral_volume": ["class_volumes.mineral_volume_mm3"],
    "mineral_fraction_of_defect": ["class_volumes.mineralized_fraction", "bridging_all_mineral"],
}


def support_for_scan(image: np.ndarray, roi_mask: np.ndarray, spacing, cfg: dict) -> dict:
    """Assess measurement support for one scan from the analysis config.

    Recognised config keys: ``material`` (knowledge-base id or None), ``no_graft``, ``calibrated``,
    ``day0`` ({registered, qc_pass, max_displacement_um, tolerance_um}), ``graft_reference_rel`` and
    ``new_bone_reference_rel`` (measured intensity samples in relative units), ``new_bone_rel_range``,
    ``validated_texture_model``.
    """
    est = scan_relative_units(image, exclude_mask=roi_mask)
    material = cfg.get("material")
    if material is None and not cfg.get("no_graft"):
        material = "__unspecified__"
    a = assess_support(material, noise_rel=est["noise_rel"], voxel_um=float(np.mean(spacing)),
                       graft_samples_rel=cfg.get("graft_reference_rel"),
                       new_samples_rel=cfg.get("new_bone_reference_rel"),
                       day0=cfg.get("day0"), calibrated=bool(cfg.get("calibrated", False)),
                       no_graft=bool(cfg.get("no_graft", False)),
                       validated_texture_model=bool(cfg.get("validated_texture_model", False)),
                       new_bone_rel_range=cfg.get("new_bone_rel_range"))
    d = a.to_dict()
    if material == "__unspecified__":
        for e in d["endpoints"].values():
            if e["status"] == NOT_SUPPORTED and "knowledge base" in e["reason"]:
                e["reason"] = "graft material not specified: graft/new-bone split cannot be assessed"
    d["scan_levels"] = est
    return d


def _get(d, path):
    cur = d
    for p in path.split("."):
        if not isinstance(cur, dict) or p not in cur:
            return None, False
        cur = cur[p]
    return cur, True


def _set(d, path, value):
    parts = path.split(".")
    cur = d
    for p in parts[:-1]:
        cur = cur[p]
    cur[parts[-1]] = value


def apply_support(metrics: dict, support: dict) -> dict:
    """Return (reported_metrics, suppressed_list). Unsupported endpoint values become None."""
    rep = copy.deepcopy(metrics)
    cv = rep.get("class_volumes", {})
    if "new_bone_volume_mm3" in cv and "residual_graft_volume_mm3" in cv:
        cv["mineral_volume_mm3"] = cv["new_bone_volume_mm3"] + cv["residual_graft_volume_mm3"]
    suppressed = []
    eps = support.get("endpoints", {})
    for ep, paths in ENDPOINT_METRICS.items():
        st = eps.get(ep, {}).get("status", NOT_SUPPORTED)
        if st == NOT_SUPPORTED:
            for p in paths:
                _, ok = _get(rep, p)
                if ok:
                    _set(rep, p, None)
                    suppressed.append({"metric": p, "endpoint": ep, "reason": eps.get(ep, {}).get("reason", "")})
    rep["support_summary"] = {ep: eps.get(ep, {}).get("status", NOT_SUPPORTED) for ep in ENDPOINT_METRICS}
    return rep, suppressed


def measurement_support(result: dict) -> dict:
    """Desktop/report hook: endpoint → {status, mechanism, reason, conditions} for a pipeline result."""
    return (result.get("measurement_support") or {}).get("endpoints", {})


__all__ = ["support_for_scan", "apply_support", "measurement_support", "SUPPORTED", "CONDITIONAL", "NOT_SUPPORTED",
           "to_relative"]


def advisor_threshold_segmentation(image: np.ndarray, roi_mask: np.ndarray, spacing, cfg: dict):
    """Intensity segmentation that uses the advisor's own decision rule.

    The graft/new-bone threshold is the Dice-optimal oracle threshold computed from the material model
    (or measured reference samples) in relative units, mapped to grey values with the soft-tissue and
    host-bone levels measured outside the defect. Mineral vs soft tissue uses Otsu. Returns
    (labels, info). The labels are produced even when the endpoint is unsupported; reporting
    suppression is applied separately (apply_support).
    """
    from ..segment import classical as C
    est = scan_relative_units(image, exclude_mask=roi_mask)
    material = cfg.get("material") or "__unspecified__"
    a = assess_support(material, noise_rel=est["noise_rel"], voxel_um=float(np.mean(spacing)),
                       graft_samples_rel=cfg.get("graft_reference_rel"),
                       new_samples_rel=cfg.get("new_bone_reference_rel"),
                       new_bone_rel_range=cfg.get("new_bone_rel_range"))
    mineral, t_min = C.threshold_otsu(image)
    t_rel = a.intensity.get("threshold")
    info = {"method": "advisor_threshold", "scan_levels": est, "t_mineral": float(t_min)}
    if t_rel is None:
        g = np.zeros(image.shape, bool)
        info["note"] = "no intensity model for this material: all mineral in ROI labelled new bone"
        brighter = True
    else:
        brighter = bool(a.intensity.get("graft_brighter", True))
        t = est["soft"] + t_rel * (est["host"] - est["soft"])
        g = image > t if brighter else image < t
        info.update({"t_graft": float(t), "t_graft_rel": float(t_rel), "graft_brighter": brighter,
                     "oracle_dice_graft": a.intensity.get("dice_graft")})
    lab = C.compose_three_class(mineral, g, roi_mask)
    return lab, info
