"""Experimental histomorphometry module (2D whole-slide images).

Implemented (all classical, CPU, no external services):
* WSI ingestion: OME-TIFF / pyramidal TIFF via tifffile (multi-resolution levels, tile reads).
* Tissue detection at low resolution (Otsu on optical-density saturation).
* Stain separation: Ruifrok & Johnston colour deconvolution with selectable stain matrices
  (H&E; H-E-DAB via skimage; Masson/Goldner approximate vectors — ASSUMED, calibrate per lab).
* Colour normalisation: Macenko et al. (2009) stain-vector estimation and concentration mapping.
* Region quantification: bone/osteoid (eosin- or fast-green-dense), residual graft (material-
  specific rule: e.g. unstained/void after decalcification, or strongly basophilic for some CaP),
  fibrous tissue, marrow, nuclei (haematoxylin threshold + distance-transform watershed).
* 2D–3D registration (experimental): oblique reslice of a micro-CT volume and 2D affine
  registration of its mineral map to the histology bone map (SimpleITK), with shrinkage/deformation
  explicitly modelled as an affine scale — NOT a validated correspondence.

Limitations: no deep nuclei models (Cellpose/StarDist/QuPath not bundled); no osteoclast (TRAP)
classifier without labels; histology and micro-CT measure different things (2D section area of
decalcified, stained tissue vs 3D mineral attenuation) and are not interchangeable.
"""
from __future__ import annotations

import numpy as np
from scipy import ndimage as ndi

# Stain OD vectors (rows: stains). H&E from Ruifrok & Johnston 2001 as used in skimage (rgb_from_hed).
HE = np.array([[0.65, 0.70, 0.29], [0.07, 0.99, 0.11], [0.27, 0.57, 0.78]])
# Approximate vectors for trichromes — ASSUMPTION, estimate per lab with Macenko or stain controls.
MASSON = np.array([[0.65, 0.70, 0.29], [0.10, 0.90, 0.42], [0.80, 0.50, 0.33]])  # haematoxylin, aniline blue?, fuchsin
GOLDNER = np.array([[0.65, 0.70, 0.29], [0.85, 0.30, 0.43], [0.60, 0.20, 0.77]])  # haematoxylin, light green, orange G/fuchsin


def _norm_rows(M):
    M = np.asarray(M, float)
    return M / np.linalg.norm(M, axis=1, keepdims=True)


def rgb_to_od(rgb, Io=255.0):
    return -np.log(np.maximum(rgb.astype(np.float32), 1) / Io)


def deconvolve(rgb, stains=HE):
    """Return stain concentration maps (H, W, 3) via Ruifrok–Johnston colour deconvolution."""
    M = _norm_rows(stains)
    if np.linalg.matrix_rank(M) < 3:
        M[2] = np.cross(M[0], M[1])
        M = _norm_rows(M)
    od = rgb_to_od(rgb).reshape(-1, 3)
    C = od @ np.linalg.inv(M)
    return C.reshape(rgb.shape[:2] + (3,))


def macenko_vectors(rgb, beta=0.15, alpha=1.0):
    """Estimate H and E OD vectors from an RGB tile (Macenko et al. 2009)."""
    od = rgb_to_od(rgb).reshape(-1, 3)
    od = od[(od > beta).all(1)]
    if len(od) < 100:
        return _norm_rows(HE)[:2]
    _, V = np.linalg.eigh(np.cov(od.T))
    V = V[:, [2, 1]]
    if V[0, 0] < 0:
        V[:, 0] *= -1
    if V[0, 1] < 0:
        V[:, 1] *= -1
    proj = od @ V
    phi = np.arctan2(proj[:, 1], proj[:, 0])
    lo, hi = np.percentile(phi, alpha), np.percentile(phi, 100 - alpha)
    v1 = V @ np.array([np.cos(lo), np.sin(lo)])
    v2 = V @ np.array([np.cos(hi), np.sin(hi)])
    h, e = (v1, v2) if v1[0] > v2[0] else (v2, v1)
    return _norm_rows(np.stack([h, e]))


def macenko_normalize(rgb, target_vectors=None, target_maxc=(1.9705, 1.0308)):
    """Map an image's stain concentrations onto reference stain vectors (colour normalisation)."""
    src = macenko_vectors(rgb)
    tgt = _norm_rows(HE)[:2] if target_vectors is None else target_vectors
    od = rgb_to_od(rgb).reshape(-1, 3)
    C, *_ = np.linalg.lstsq(src.T, od.T, rcond=None)
    maxc = np.percentile(C, 99, axis=1)
    C = C / maxc[:, None] * np.asarray(target_maxc)[:, None]
    out = 255 * np.exp(-(tgt.T @ C))
    return np.clip(out.T.reshape(rgb.shape), 0, 255).astype(np.uint8)


def tissue_mask(rgb, min_size=500, fill=True):
    from skimage.filters import threshold_otsu
    od = rgb_to_od(rgb).sum(-1)
    t = threshold_otsu(od[:: max(1, od.shape[0] // 512), :: max(1, od.shape[1] // 512)])
    m = ndi.binary_opening(od > t, iterations=2)
    lab, n = ndi.label(m)
    if n:
        sizes = ndi.sum(m, lab, range(1, n + 1))
        m = np.isin(lab, np.flatnonzero(sizes >= min_size) + 1)
    return ndi.binary_fill_holes(m) if fill else m


def quantify_he(rgb, roi=None, graft_rule="void", pixel_um=1.0):
    """H&E region quantification in an ROI. Classes: bone (eosin-dense, low haematoxylin),
    marrow/cellular (haematoxylin-rich), fibrous (moderate eosin, low nuclei density), graft
    (rule: 'void' = unstained holes inside tissue, typical of decalcified CaP; 'basophilic' =
    haematoxylin-dense acellular), background. Thresholds are Otsu-derived per slide."""
    from skimage.filters import threshold_otsu
    tm = tissue_mask(rgb)
    roi = tm if roi is None else (roi & tm)
    C = deconvolve(rgb, HE)
    h, e = C[..., 0], C[..., 1]
    hs, es = ndi.gaussian_filter(h, 1.5), ndi.gaussian_filter(e, 1.5)
    th_h = threshold_otsu(hs[roi]) if roi.any() else 0
    th_e = threshold_otsu(es[roi]) if roi.any() else 0
    cellular = roi & (hs > th_h)
    bone = roi & (es > th_e) & ~cellular
    nuclear_density = ndi.uniform_filter((h > th_h * 1.3).astype(np.float32), 25)
    fibrous = roi & ~bone & ~cellular & (es > 0.6 * th_e) & (nuclear_density < 0.05)
    od = rgb_to_od(rgb).sum(-1)
    if graft_rule == "void":
        raw = tissue_mask(rgb, fill=False)          # unfilled: voids inside tissue remain False
        graft = tm & ~raw & (od < 0.15)
        graft &= ndi.binary_dilation(roi, iterations=3)
    else:
        graft = roi & (hs > 1.5 * th_h) & (nuclear_density < 0.05)
    area = lambda m: float(m.sum()) * pixel_um ** 2 * 1e-6  # mm²
    tv = area(roi | graft)
    out = {"tissue_area_mm2": tv, "bone_area_mm2": area(bone), "graft_area_mm2": area(graft),
           "cellular_area_mm2": area(cellular), "fibrous_area_mm2": area(fibrous)}
    for k in ("bone", "graft", "cellular", "fibrous"):
        out[f"{k}_fraction"] = out[f"{k}_area_mm2"] / tv if tv else float("nan")
    out["B.Ar/T.Ar"] = out["bone_fraction"]
    out["thresholds"] = {"hematoxylin": float(th_h), "eosin": float(th_e)}
    out["note"] = "Unvalidated classical rules; Dempster 2013 symbols used for areas only."
    masks = {"bone": bone, "graft": graft, "cellular": cellular, "fibrous": fibrous, "tissue": roi}
    return out, masks


def nuclei(h_channel, min_area_px=12, pixel_um=1.0, smooth=1.0, min_distance=3):
    from skimage.filters import threshold_otsu
    from skimage.segmentation import watershed
    from skimage.feature import peak_local_max
    hs = ndi.gaussian_filter(h_channel, smooth)
    m = hs > threshold_otsu(hs)
    m = ndi.binary_opening(m, iterations=1)
    d = ndi.gaussian_filter(ndi.distance_transform_edt(m), 1.0)
    pk = peak_local_max(d, min_distance=min_distance, labels=m.astype(int), exclude_border=False)
    mk = np.zeros(m.shape, np.int32)
    mk[tuple(pk.T)] = np.arange(1, len(pk) + 1)
    lab = watershed(-d, mk, mask=m)
    sizes = np.bincount(lab.ravel())
    keep = np.flatnonzero(sizes >= min_area_px)
    keep = keep[keep > 0]
    lab = np.where(np.isin(lab, keep), lab, 0)
    return lab, {"n_nuclei": int(len(keep)), "mean_area_um2": float(sizes[keep].mean() * pixel_um ** 2) if len(keep) else 0}


# ----------------------------------------------------------------------------- WSI access
def wsi_levels(path):
    import tifffile
    with tifffile.TiffFile(path) as t:
        s = t.series[0]
        return [lvl.shape for lvl in s.levels]


def wsi_read(path, level=-1, region=None):
    """Read a pyramid level (default: lowest resolution) or a (y0,x0,y1,x1) region of it."""
    import tifffile
    import zarr
    with tifffile.TiffFile(path) as t:
        s = t.series[0]
        lvl = s.levels[level]
        store = lvl.aszarr()
        a = zarr.open(store, mode="r")
        if region is None:
            arr = np.asarray(a[:])
        else:
            y0, x0, y1, x1 = region
            arr = np.asarray(a[y0:y1, x0:x1]) if a.ndim == 3 and a.shape[-1] in (3, 4) else np.asarray(a[..., y0:y1, x0:x1])
    if arr.ndim == 3 and arr.shape[0] in (3, 4) and arr.shape[-1] not in (3, 4):
        arr = np.moveaxis(arr, 0, -1)
    return arr[..., :3]


# ----------------------------------------------------------------------------- synthetic sections
def synthetic_section(labels2d, rng=None, stain_jitter=0.1):
    """Render a pseudo-H&E image from a 2D label map (0 marrow, 1 new bone, 2 graft (void after
    decalcification), 3 host bone, 4 fibrous) with stain-vector jitter (lab-to-lab variation)."""
    rng = rng or np.random.default_rng(0)
    M = _norm_rows(HE) * (1 + stain_jitter * rng.normal(0, 1, (3, 3)))
    M = _norm_rows(np.abs(M))
    conc = np.zeros(labels2d.shape + (3,), np.float32)
    H = {0: 0.9, 1: 0.15, 2: 0.0, 3: 0.1, 4: 0.3}
    E = {0: 0.25, 1: 0.9, 2: 0.0, 3: 1.1, 4: 0.6}
    for c in H:
        m = labels2d == c
        conc[m, 0] = H[c]
        conc[m, 1] = E[c]
    conc[..., 0] *= 1 + 0.6 * (rng.random(labels2d.shape) > 0.93) * (labels2d == 0)  # nuclei speckle
    conc = ndi.gaussian_filter(conc, (1, 1, 0)) + rng.normal(0, 0.03, conc.shape)
    od = conc.reshape(-1, 3) @ M
    rgb = 255 * np.exp(-od)
    return np.clip(rgb.reshape(labels2d.shape + (3,)), 0, 255).astype(np.uint8)


# ----------------------------------------------------------------------------- 2D–3D registration
def oblique_slice(volume, center_vox, normal, size, spacing=1.0):
    """Sample a plane through ``volume`` (z,y,x) with given normal; returns 2D image."""
    n = np.asarray(normal, float)
    n /= np.linalg.norm(n)
    a = np.array([1.0, 0, 0]) if abs(n[0]) < 0.9 else np.array([0, 1.0, 0])
    u = np.cross(n, a)
    u /= np.linalg.norm(u)
    v = np.cross(n, u)
    r = (np.arange(size) - size / 2) * spacing
    U, V = np.meshgrid(r, r, indexing="ij")
    pts = np.asarray(center_vox)[:, None, None] + u[:, None, None] * U + v[:, None, None] * V
    return ndi.map_coordinates(volume.astype(np.float32), pts, order=1, mode="constant")


def register_2d(fixed, moving, mode="affine"):
    import SimpleITK as sitk
    F = sitk.GetImageFromArray(fixed.astype(np.float32))
    M = sitk.GetImageFromArray(moving.astype(np.float32))
    R = sitk.ImageRegistrationMethod()
    R.SetMetricAsMattesMutualInformation(32)
    R.SetInterpolator(sitk.sitkLinear)
    base = sitk.AffineTransform(2) if mode == "affine" else sitk.Euler2DTransform()
    R.SetInitialTransform(sitk.CenteredTransformInitializer(F, M, base, sitk.CenteredTransformInitializerFilter.MOMENTS), inPlace=False)
    R.SetOptimizerAsRegularStepGradientDescent(2.0, 1e-4, 300, relaxationFactor=0.7)
    R.SetOptimizerScalesFromPhysicalShift()  # pixel units here (spacing 1), well conditioned
    R.SetShrinkFactorsPerLevel([4, 2, 1])
    R.SetSmoothingSigmasPerLevel([2, 1, 0])
    R.SmoothingSigmasAreSpecifiedInPhysicalUnitsOff()
    tx = R.Execute(F, M)
    out = sitk.GetArrayFromImage(sitk.Resample(M, F, tx, sitk.sitkNearestNeighbor, 0.0))
    return out, tx
