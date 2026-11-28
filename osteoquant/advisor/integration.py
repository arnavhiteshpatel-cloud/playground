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
              energy_keV=float(cfg.get("effective_energy_keV", 40.0)),   # from acquisition metadata (IMG-10)
              healing_weeks=cfg.get("healing_weeks"))
    prior = float(cfg.get("graft_prior", 0.5))
    a = assess_support(material, graft_prior=prior, **kw)
    if roi_mask is not None and roi_mask.any():
        from scipy import ndimage as ndi
        rel_img = to_relative(image, est["soft"], est["host"])
        roi = roi_mask
        t_min = (a.intensity.get("mineral_rule") or {}).get("threshold") or MINERAL_REL_THRESHOLD
        mineral = (rel_img > t_min) & roi
        t = a.intensity.get("threshold")
        g = np.zeros_like(mineral)
        if t is not None:
            g = ((rel_img > t) if a.intensity.get("graft_brighter", True) else (rel_img < t)) & mineral
        if "graft_prior" not in cfg and t is not None and mineral.any():
            prior = float(np.clip(g.sum() / mineral.sum(), 0.005, 0.95))
        # ≥1.4.0 ambiguous graft rim: mineral that is not graft-like but touches graft-like voxels is either new bone
        # coating the granules (osteoconduction) or partial-volume halo of the graft — indistinguishable by intensity.
        if g.any():
            nb_like = mineral & ~g
            rim = nb_like & ndi.binary_dilation(g, iterations=1)
            kw["rim_fraction_new"] = float(rim.sum() / max(1, nb_like.sum()))
            kw["rim_fraction_mineral"] = float(0.5 * rim.sum() / max(1, mineral.sum()))
        # partial-volume halo and new-bone share measured from the scan (advisor ≥1.2.0)
        # surface shell of mineral structures (any phase), estimated with a conservative core threshold so that
        # the halo itself is not counted as structure; the share of non-core ROI voxels in that shell
        core = (rel_img > 0.5) & roi
        shell = ndi.binary_dilation(core, iterations=1) & ~core & roi
        halo_frac = float(shell.sum() / max(1, (roi & ~core).sum()))
        nb_share = float(((mineral & ~g).sum()) / max(1, (roi & ~g).sum()))
        kw.update(soft_halo_fraction=float(np.clip(halo_frac, 0.0, 0.6)), new_bone_share=float(np.clip(nb_share, 0.02, 0.95)))
        # scan-vs-profile consistency (advisor 1.3.1): interior voxels brighter than mature bone are graft-like;
        # their median is compared with the profile's graft level
        interior = ndi.binary_erosion(roi, iterations=1)
        bright_mask = interior & (rel_img > 1.1)
        bright = rel_img[bright_mask]
        if bright.size >= 200:
            kw["observed_graft_level"] = float(np.median(bright))
            # ≥1.4.0: deep graft-like voxels (one erosion inside the bright mask) give the material's level in THIS scan
            deep = rel_img[ndi.binary_erosion(bright_mask, iterations=1)]
            if deep.size >= 200:
                kw["graft_level_deep"] = float(np.median(deep))
            # measured graft structure thickness (µm) of the graft-like component
            try:
                from ..morphometry import local_thickness
                zz, yy, xx = np.nonzero(bright_mask)
                sl = (slice(zz.min(), zz.max() + 1), slice(yy.min(), yy.max() + 1), slice(xx.min(), xx.max() + 1))
                bm = ndi.binary_opening(bright_mask[sl], iterations=1)
                if bm.sum() >= 200:
                    th = local_thickness(bm, float(np.mean(spacing)), border="background")
                    kw["graft_struct_um"] = float(np.median(th[bm]))
            except Exception:
                pass
            # share of the soft-tissue shell around mineral that borders graft-like voxels (halo composition)
            shell_all = ndi.binary_dilation((rel_img > 0.5) & roi, iterations=1) & ~((rel_img > 0.5) & roi) & roi
            if shell_all.sum() > 0:
                kw["halo_graft_fraction"] = float((ndi.binary_dilation(bright_mask, iterations=1) & shell_all).sum()
                                                  / shell_all.sum())
        blur = estimate_blur(image, roi, est["soft"], est["host"])
        if blur.get("sigma_vox"):
            kw["blur_sigma_vox"] = float(blur["sigma_vox"])
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
    outside the defect. Mineral/soft threshold: the advisor's new-bone-vs-soft-tissue rule (≥1.2.0), which models
    partial-volume halos of dense phases (falls back to relative 0.30); unlike a global Otsu threshold it is not
    pulled upward by dense grafts (review STAT-05). Returns
    (labels, info). Labels are produced even when the endpoint is unsupported; reporting suppression is
    applied separately (apply_support).
    """
    from ..segment import classical as C
    a, est, prior, material = _assess_scan(image, roi_mask, spacing, cfg)
    t_min_rel = (a.intensity.get("mineral_rule") or {}).get("threshold") or MINERAL_REL_THRESHOLD
    t_min = est["soft"] + t_min_rel * (est["host"] - est["soft"])
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


# ----------------------------------------------------------------------------- scan-measured imaging properties (≥1.4.0)
def estimate_blur(image: np.ndarray, roi_mask: np.ndarray | None, soft: float, host: float, margin_vox: int = 3) -> dict:
    """Edge-spread estimate of the scan's total blur (PSF ⊗ voxel), in voxels, from host-bone/soft-tissue edges
    outside the defect.

    Signed distance to the thresholded host-bone surface is computed (positive inside bone); only edges between
    *thick* bone and *thick* soft tissue are used (both sides have a ≥2-voxel core within 4 voxels), so thin
    trabeculae do not bias the profile. The mean relative intensity per 0.25-voxel distance bin is fitted with a
    blurred step Φ(d/σ) by least squares over σ ∈ [0.2, 3] voxels. Returns {"sigma_vox", "n_edge_voxels", "rmse"}.
    """
    from scipy.special import ndtr
    rel = to_relative(image, soft, host)
    keep = np.ones(image.shape, bool) if roi_mask is None else ~ndi_binary_dilation(roi_mask, margin_vox)
    keep &= image != image.min()                      # drop reconstruction padding
    H = (rel > 0.5) & keep
    S = (rel <= 0.5) & keep
    if H.sum() < 500 or S.sum() < 500:
        return {"sigma_vox": None, "n_edge_voxels": 0, "rmse": None, "note": "too little bone or soft tissue outside ROI"}
    from scipy import ndimage as ndi
    core_b = ndi.binary_erosion(H, iterations=3)
    core_s = ndi.binary_erosion(S, iterations=3)
    near_b = ndi.distance_transform_edt(~core_b) <= 6
    near_s = ndi.distance_transform_edt(~core_s) <= 6
    d_in = ndi.distance_transform_edt(H)
    d_out = ndi.distance_transform_edt(~H)
    d = np.where(H, d_in - 0.5, -(d_out - 0.5))
    band = keep & near_b & near_s & (np.abs(d) <= 5.0)
    if band.sum() < 200:
        return {"sigma_vox": None, "n_edge_voxels": int(band.sum()), "rmse": None, "note": "too few thick edges"}
    dv, iv = d[band], np.clip(rel[band], -0.5, 1.5)
    bins = np.arange(-5.0, 5.01, 0.25)
    idx = np.digitize(dv, bins)
    centers, means, counts = [], [], []
    for k in range(1, len(bins)):
        m = idx == k
        if m.sum() >= 20:
            centers.append(float(dv[m].mean()))     # mean distance in the bin (distances are discrete; bin centres bias)
            means.append(float(iv[m].mean()))
            counts.append(int(m.sum()))
    centers, means, w = np.array(centers), np.array(means), np.sqrt(np.array(counts))
    best = (None, np.inf)
    for sig in np.linspace(0.2, 4.0, 77):
        pred = ndtr(centers / sig)
        err = float(np.sqrt(np.average((means - pred) ** 2, weights=w)))
        if err < best[1]:
            best = (float(sig), err)
    raw = best[0]
    # Conservative calibration (development phantoms, seed 4321, PSF 10–60 µm; not the S1H/S1H2 validation sets):
    # the edge fit under-reads heavy blur (thin structures, merged edges), so estimates above 0.6 voxel are inflated.
    cal = raw * (1.0 + max(0.0, raw - 0.6) * 1.5)
    return {"sigma_vox": cal, "sigma_vox_raw": raw, "n_edge_voxels": int(band.sum()), "rmse": best[1]}


def ndi_binary_dilation(mask, it):
    from scipy import ndimage as ndi
    return ndi.binary_dilation(mask, iterations=it)
