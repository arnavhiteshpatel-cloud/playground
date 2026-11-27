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


MINERAL_REL_THRESHOLD = 0.30   # 50% partial-volume point between soft tissue (0) and the least mature new bone (0.6)


def _assess_scan(image: np.ndarray, roi_mask: np.ndarray, spacing, cfg: dict):
    """Shared by support_for_scan and advisor_threshold_segmentation so that the decision and the applied
    threshold come from the same assessment. The graft share among mineral voxels in the ROI is estimated from
    the scan (one fixed-point iteration from 0.5) and used for the decision (review IMG-01)."""
    est = scan_relative_units(image, exclude_mask=roi_mask)
    material = cfg.get("material")
    if material is None and not cfg.get("no_graft"):
        material = "__unspecified__"
    kw = dict(noise_rel=est["noise_rel"], voxel_um=float(np.mean(spacing)),
              graft_samples_rel=cfg.get("graft_reference_rel"), new_samples_rel=cfg.get("new_bone_reference_rel"),
              day0=cfg.get("day0"), calibrated=bool(cfg.get("calibrated", False)),
              no_graft=bool(cfg.get("no_graft", False)),
              validated_texture_model=bool(cfg.get("validated_texture_model", False)),
              new_bone_rel_range=cfg.get("new_bone_rel_range"),
              energy_keV=float(cfg.get("effective_energy_keV", 40.0)))   # from acquisition metadata (IMG-10)
    rel = to_relative(image[roi_mask], est["soft"], est["host"]) if roi_mask is not None and roi_mask.any() else None
    prior = float(cfg.get("graft_prior", 0.5))
    a = assess_support(material, graft_prior=prior, **kw)
    if "graft_prior" not in cfg and rel is not None and a.intensity.get("threshold") is not None:
        mineral = rel > MINERAL_REL_THRESHOLD
        if mineral.any():
            t = a.intensity["threshold"]
            g = (rel > t) if a.intensity.get("graft_brighter", True) else (rel < t)
            prior = float(np.clip((g & mineral).sum() / mineral.sum(), 0.005, 0.95))
            a = assess_support(material, graft_prior=prior, **kw)
    return a, est, prior, material


def support_for_scan(image: np.ndarray, roi_mask: np.ndarray, spacing, cfg: dict) -> dict:
    """Assess measurement support for one scan from the analysis config.

    Recognised config keys: ``material`` (knowledge-base id or None), ``no_graft``, ``calibrated``,
    ``day0`` ({registered, qc_pass, untracked_fraction, max_displacement_um, tolerance_um}),
    ``graft_reference_rel`` and ``new_bone_reference_rel`` (measured intensity samples in relative units),
    ``new_bone_rel_range``, ``validated_texture_model``, ``graft_prior`` (override of the estimated share).
    """
    a, est, prior, material = _assess_scan(image, roi_mask, spacing, cfg)
    d = a.to_dict()
    if material == "__unspecified__":
        for e in d["endpoints"].values():
            if e["status"] == NOT_SUPPORTED and "knowledge base" in e["reason"]:
                e["reason"] = "graft material not specified: graft/new-bone split cannot be assessed"
    d["scan_levels"] = est
    d["estimated_graft_share_of_mineral"] = prior
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
    # mineral_volume_mm3 := new bone + residual graft in the ROI (host bone inside the ROI excluded — it is in
    # mineralized_fraction). Added to the RAW metrics too so raw and reported views share definitions (ARC-07).
    cv_raw = metrics.get("class_volumes", {})
    if "new_bone_volume_mm3" in cv_raw and "residual_graft_volume_mm3" in cv_raw:
        cv_raw["mineral_volume_mm3"] = cv_raw["new_bone_volume_mm3"] + cv_raw["residual_graft_volume_mm3"]
    rep = copy.deepcopy(metrics)
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
    """Intensity segmentation that applies the advisor's own decision rule.

    Graft/new-bone threshold: the best single threshold of the advisor's class model at the scan's estimated
    graft share (relative units), mapped to grey values with the soft-tissue and host-bone levels measured
    outside the defect. Mineral/soft threshold: relative 0.30 (half-way to the least mature new bone), which,
    unlike a global Otsu threshold, is not pulled upward by dense grafts (review STAT-05). Returns
    (labels, info). Labels are produced even when the endpoint is unsupported; reporting suppression is
    applied separately (apply_support).
    """
    from ..segment import classical as C
    a, est, prior, material = _assess_scan(image, roi_mask, spacing, cfg)
    t_min = est["soft"] + MINERAL_REL_THRESHOLD * (est["host"] - est["soft"])
    mineral = image > t_min
    t_rel = a.intensity.get("threshold")
    info = {"method": "advisor_threshold", "scan_levels": est, "t_mineral": float(t_min),
            "estimated_graft_share": prior, "advisor_version": a.advisor_version}
    if t_rel is None:
        g = np.zeros(image.shape, bool)
        info["note"] = "no intensity model for this material: all mineral in ROI labelled new bone"
    else:
        brighter = bool(a.intensity.get("graft_brighter", True))
        t = est["soft"] + t_rel * (est["host"] - est["soft"])
        g = image > t if brighter else image < t
        info.update({"t_graft": float(t), "t_graft_rel": float(t_rel), "graft_brighter": brighter,
                     "threshold_rule_dice": a.intensity.get("dice_graft_threshold_rule")})
    lab = C.compose_three_class(mineral, g, roi_mask)
    return lab, info
