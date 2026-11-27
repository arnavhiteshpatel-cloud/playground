"""Quantitative morphometry (micro-CT), aligned with Bouxsein et al. 2010 (JBMR 25:1468).

Every function documents: definition, units, method, assumptions and limitations. Symbols
follow Bouxsein 2010 / Dempster 2013 nomenclature. All lengths are µm, volumes mm³, areas mm².

Key conventions (verified numerically in Experiment G / tests/test_morphometry.py):
* Volumes are voxel counts × voxel volume (no sub-voxel surface model).
* BS uses a marching-cubes triangulated isosurface at the binary 0.5 level (Lorensen & Cline),
  which avoids the staircase over-estimate of voxel-face counting.
* Tb.Th / Tb.Sp / Ct.Th use *direct 3D* local thickness (Hildebrand & Rüegsegger 1997):
  thickness at a point = diameter of the largest sphere that contains the point and fits
  inside the structure. Implemented as: Euclidean distance transform → distance-ridge points
  → sphere painting per quantised radius. Requires isotropic voxels (resample first).
  Discretisation: thickness = 2·d_EDT (BoneJ convention); bias 0 voxels for even and +1
  voxel for odd voxel thicknesses; residual error vs analytic phantoms is in Experiment G.
* Border convention for thickness (reported with every result): "edge" (default) replicates the
  *array* border outward so structures cut by a cropped cube are not artificially thinned;
  "background" treats the array border as the end of every structure. NOTE: the convention acts
  on the array border only — inside a cylindrical/irregular ROI, voxels outside the ROI mask are
  background regardless. The "edge" default was chosen AFTER comparing both conventions against
  Scanco IPL on the same 8 public cubes (Experiment G); that agreement is therefore not an
  independent validation and must be re-tested on new reference data (review finding Q-10).
* Tb.N = 1 / (Tb.Th + Tb.Sp)  (approximation; direct 3D Tb.N via mid-axis spacing not implemented).
* Conn.D = β1 / TV with β1 = β0 + β2 − χ (Euler–Poincaré, 26-connected foreground,
  Odgaard & Gundersen 1993). No edge correction: the ROI is treated as an isolated object,
  which differs from BoneJ's Δχ edge-corrected value for trabecular sub-volumes.
* TMD / vBMD are reported in mgHA/cm³ ONLY when the volume carries a calibration record;
  otherwise mean grey values are labelled "uncalibrated".
"""
from __future__ import annotations

import numpy as np
from scipy import ndimage as ndi

from ..volume import Volume

LABEL_NAMES = {1: "new_bone", 2: "residual_graft", 3: "host_bone"}


# ----------------------------------------------------------------------------- basic
def volume_mm3(mask, spacing) -> float:
    return float(mask.sum()) * float(np.prod(spacing)) * 1e-9


def surface_area_mm2(mask, spacing) -> float:
    """Isosurface area (marching cubes at 0.5) in mm²."""
    from skimage.measure import marching_cubes, mesh_surface_area
    if mask.sum() == 0:
        return 0.0
    m = np.pad(mask.astype(np.float32), 1)
    try:
        verts, faces, _, _ = marching_cubes(m, 0.5, spacing=tuple(spacing))
    except (ValueError, RuntimeError):
        return 0.0
    return float(mesh_surface_area(verts, faces)) * 1e-6


def local_thickness(mask: np.ndarray, voxel_um: float, radius_step: float = 0.25, border: str = "background",
                    border_pad: int = 24) -> np.ndarray:
    """Direct 3D local thickness map (µm) for a binary structure (isotropic voxels).

    Convention (as in BoneJ Thickness): sphere centres are distance-ridge voxels; the sphere
    radius is the Euclidean distance d from the centre voxel to the nearest background voxel
    centre; a voxel x is covered when |x − c| < d; thickness = 2·d. The array border is treated
    as background (structures are cut by the analysed region). Expected discretisation bias:
    0 voxels for even voxel thicknesses, +1 voxel for odd (mean ≈ +0.5 voxel) — see Experiment G.
    """
    if not mask.any():
        return np.zeros(mask.shape, np.float32)
    if border == "edge":
        # structures are assumed to continue beyond the analysed region (cropped VOI): replicate
        # the boundary slice outward, compute, crop back. Closer to Scanco IPL on cropped cubes
        # (Experiment G); 'background' treats the region border as the end of every structure.
        k = int(border_pad)
        th = local_thickness(np.pad(mask, k, mode="edge"), voxel_um, radius_step, "background")
        return th[k:-k, k:-k, k:-k]
    m = np.pad(mask, 1)
    d = ndi.distance_transform_edt(m).astype(np.float32)
    ridge = (d >= ndi.maximum_filter(d, size=3) - 1e-6) & m
    pts = np.argwhere(ridge)
    radii = d[ridge]
    th = np.zeros(m.shape, np.float32)
    q = np.round(radii / radius_step) * radius_step
    for r in np.unique(q):
        sel = pts[q == r]
        seed = np.zeros(m.shape, bool)
        seed[tuple(sel.T)] = True
        R = int(np.ceil(r)) + 1
        lo = np.maximum(sel.min(0) - R, 0)
        hi = np.minimum(sel.max(0) + R + 1, m.shape)
        sl = tuple(slice(a, b) for a, b in zip(lo, hi))
        cover = ndi.distance_transform_edt(~seed[sl]) < r
        sub = th[sl]
        upd = cover & m[sl]
        sub[upd] = np.maximum(sub[upd], 2 * r)
    th = th[1:-1, 1:-1, 1:-1]
    th[mask & (th == 0)] = 1.0
    return th * voxel_um


def thickness_stats(mask, voxel_um, border="edge") -> dict:
    if not mask.any():
        return {"mean_um": float("nan"), "sd_um": float("nan"), "max_um": float("nan")}
    t = local_thickness(mask, voxel_um, border=border)[mask]
    return {"mean_um": float(t.mean()), "sd_um": float(t.std()), "max_um": float(t.max())}


def euler_connectivity(mask) -> dict:
    """β0 (components), β2 (cavities), χ (Euler), β1 (connectivity/handles)."""
    from skimage.measure import euler_number
    if not mask.any():
        return {"beta0": 0, "beta1": 0, "beta2": 0, "euler": 0}
    m = np.pad(mask, 1)
    chi = int(euler_number(m, connectivity=3))
    _, b0 = ndi.label(m, structure=np.ones((3, 3, 3)))
    bg, nbg = ndi.label(~m, structure=ndi.generate_binary_structure(3, 1))  # 6-conn background
    b2 = nbg - 1  # enclosed cavities (outer background is one component thanks to padding)
    b1 = b0 + b2 - chi
    return {"beta0": int(b0), "beta1": int(max(b1, 0)), "beta2": int(b2), "euler": chi}


# ----------------------------------------------------------------------------- trabecular set
def trabecular_morphometry(bone: np.ndarray, tv_mask: np.ndarray, voxel_um: float,
                           compute_thickness=True, compute_conn=True, border: str = "edge") -> dict:
    """Standard trabecular parameters for ``bone`` inside the tissue-volume mask ``tv_mask``."""
    sp = (voxel_um,) * 3
    b = bone & tv_mask
    tv = volume_mm3(tv_mask, sp)
    bv = volume_mm3(b, sp)
    out = {"TV_mm3": tv, "BV_mm3": bv, "BV_TV": bv / tv if tv else float("nan")}
    bs = surface_area_mm2(b, sp)
    out["BS_mm2"] = bs
    out["BS_BV_per_mm"] = bs / bv if bv else float("nan")
    out["BS_TV_per_mm"] = bs / tv if tv else float("nan")
    if compute_thickness:
        th = thickness_stats(b, voxel_um, border)
        spc = thickness_stats(tv_mask & ~b, voxel_um, border)
        out["thickness_border_convention"] = border
        out["Tb_Th_um"], out["Tb_Th_sd_um"] = th["mean_um"], th["sd_um"]
        out["Tb_Sp_um"], out["Tb_Sp_sd_um"] = spc["mean_um"], spc["sd_um"]
        s = out["Tb_Th_um"] + out["Tb_Sp_um"]
        out["Tb_N_per_mm"] = 1000.0 / s if s and np.isfinite(s) else float("nan")
    if compute_conn:
        e = euler_connectivity(b)
        out.update({f"conn_{k}": v for k, v in e.items()})
        out["Conn_D_per_mm3"] = e["beta1"] / tv if tv else float("nan")
    return out


def cortical_thickness(cortex: np.ndarray, voxel_um: float, border="edge") -> dict:
    t = thickness_stats(cortex, voxel_um, border)
    return {"Ct_Th_um": t["mean_um"], "Ct_Th_sd_um": t["sd_um"]}


def porosity(material: np.ndarray, envelope: np.ndarray) -> float:
    """Fraction of the envelope not occupied by material (e.g. Ct.Po, scaffold porosity)."""
    env = envelope.sum()
    return float(1 - (material & envelope).sum() / env) if env else float("nan")


# ----------------------------------------------------------------------------- defect endpoints
def class_volumes(labels: np.ndarray, roi: np.ndarray, spacing) -> dict:
    sp = tuple(spacing)
    tv = volume_mm3(roi, sp)
    out = {"TV_mm3": tv}
    for c, n in LABEL_NAMES.items():
        v = volume_mm3((labels == c) & roi, sp)
        out[f"{n}_volume_mm3"] = v
        out[f"{n}_fraction"] = v / tv if tv else float("nan")
    unc = volume_mm3((labels == 255) & roi, sp)
    out["uncertain_volume_mm3"] = unc
    out["uncertain_fraction"] = unc / tv if tv else float("nan")
    out["mineralized_fraction"] = sum(out[f"{n}_fraction"] for n in LABEL_NAMES.values())
    # Abstained voxels lower fractions computed over the full TV; also report fractions over the
    # confidently classified volume so material-dependent abstention does not bias comparisons (Q-06).
    tvc = tv - unc
    out["TV_certain_mm3"] = tvc
    for n in LABEL_NAMES.values():
        out[f"{n}_fraction_of_certain"] = out[f"{n}_volume_mm3"] / tvc if tvc > 0 else float("nan")
    return out


def radial_ingrowth_profile(new_bone: np.ndarray, roi: np.ndarray, spacing, shell_um=200.0) -> list[dict]:
    """New-bone fraction in concentric shells by distance from the ROI boundary (µm)."""
    d = ndi.distance_transform_edt(roi, sampling=spacing)
    out = []
    dmax = d.max()
    k = 0
    while k * shell_um < dmax:
        s = roi & (d > k * shell_um) & (d <= (k + 1) * shell_um)
        if s.any():
            out.append({"from_um": k * shell_um, "to_um": (k + 1) * shell_um,
                        "new_bone_fraction": float(new_bone[s].mean()), "n_vox": int(s.sum())})
        k += 1
    return out


def bridging(mineral: np.ndarray, roi: np.ndarray, axis: int = 0, host: np.ndarray | None = None) -> dict:
    """Defect bridging descriptors.

    * ``projected_coverage``: fraction of the ROI's projection (along ``axis``) in which at least
      one mineralised voxel lies on the ray — analogous to radiographic defect closure (%).
    * ``min_cross_section_fill``: the minimum over slices (perpendicular to axis) of the
      mineralised area fraction — the weakest cross-section (segmental gaps).
    * ``connected_bridge``: True if one 26-connected mineralised component inside ROI∪host
      touches host bone on both sides of the ROI along ``axis`` (segmental union proxy).
    Limitations: geometric descriptors only; not equivalent to mechanical union or to
    radiographic scoring scales (e.g. RUST), and depend on segmentation quality.
    """
    m = mineral & roi
    proj_roi = roi.any(axis=axis)
    proj_m = m.any(axis=axis)
    cov = float(proj_m[proj_roi].mean()) if proj_roi.any() else float("nan")
    fills = []
    idx = np.where(roi.any(axis=tuple(i for i in range(3) if i != axis)))[0]
    for i in idx:
        r = np.take(roi, i, axis=axis)
        if r.sum() > 0:
            fills.append(float(np.take(m, i, axis=axis)[r].mean()))
    out = {"projected_coverage": cov, "min_cross_section_fill": float(min(fills)) if fills else float("nan"),
           "mean_cross_section_fill": float(np.mean(fills)) if fills else float("nan")}
    if host is not None and len(idx):
        lo, hi = idx.min(), idx.max()
        comp, n = ndi.label(m | host, structure=np.ones((3, 3, 3)))
        sl_lo = [slice(None)] * 3
        sl_hi = [slice(None)] * 3
        sl_lo[axis] = slice(0, lo)
        sl_hi[axis] = slice(hi + 1, None)
        a = set(np.unique(comp[tuple(sl_lo)][host[tuple(sl_lo)]])) - {0}
        b = set(np.unique(comp[tuple(sl_hi)][host[tuple(sl_hi)]])) - {0}
        inside = set(np.unique(comp[m])) - {0}
        out["connected_bridge"] = bool(a & b & inside)
    return out


def bone_implant_contact(implant: np.ndarray, bone: np.ndarray, spacing, contact_um: float | None = None) -> dict:
    """BIC: fraction of implant surface voxels with bone within ``contact_um`` (default 1 voxel).

    Caveat: in micro-CT, metal artefacts (blooming, streaks) near the interface bias BIC; a
    dilation margin of 1–3 voxels is commonly excluded or used. Report the margin used.
    """
    from skimage.morphology import ball
    surf = implant & ~ndi.binary_erosion(implant)
    cu = contact_um if contact_um is not None else min(spacing)
    r = max(1, int(round(cu / min(spacing))))
    near_bone = ndi.binary_dilation(bone, structure=ball(r))
    n = surf.sum()
    return {"BIC": float((surf & near_bone).sum() / n) if n else float("nan"), "contact_margin_um": r * min(spacing),
            "implant_surface_vox": int(n)}


def density_stats(vol: Volume, mask: np.ndarray, erode_vox: int = 1) -> dict:
    """Mean intensity in mask (eroded to limit partial volume). Calibrated units only if the
    volume has a calibration record; else explicitly 'uncalibrated'."""
    m = ndi.binary_erosion(mask, iterations=erode_vox) if erode_vox else mask
    if not m.any():
        m = mask
    vals = vol.data[m]
    calibrated = "calibration" in vol.meta
    unit = vol.meta.get("calibration", {}).get("unit", "uncalibrated grey value") if calibrated else "uncalibrated grey value"
    return {"mean": float(vals.mean()) if vals.size else float("nan"),
            "sd": float(vals.std()) if vals.size else float("nan"),
            "unit": unit, "calibrated": calibrated, "eroded_vox": erode_vox, "n_vox": int(vals.size)}


def defect_report_metrics(labels: np.ndarray, roi: np.ndarray, vol: Volume, axis=0,
                          thickness=True) -> dict:
    """The DefectFill endpoint set for one specimen."""
    sp = vol.spacing
    out = {"class_volumes": class_volumes(labels, roi, sp)}
    new = labels == 1
    graft = labels == 2
    host = labels == 3
    mineral = new | graft | host
    iso = vol.is_isotropic
    if iso:
        out["new_bone_architecture"] = trabecular_morphometry(new, roi, sp[0], compute_thickness=thickness)
    else:
        out["new_bone_architecture"] = {"note": "anisotropic voxels: resample for thickness metrics"}
    out["bridging_all_mineral"] = bridging(mineral, roi, axis, host)
    out["bridging_new_bone"] = bridging(new, roi, axis, host)
    out["radial_ingrowth"] = radial_ingrowth_profile(new, roi, sp, shell_um=max(200.0, 4 * sp[0]))
    out["density"] = {n: density_stats(vol, (labels == c) & (roi if c != 3 else np.ones_like(roi)))
                      for c, n in LABEL_NAMES.items() if ((labels == c)).any()}
    return out
