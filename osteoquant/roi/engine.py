"""Defect region-of-interest (ROI) engine.

An ROI is stored as an exact mathematical definition in physical micrometres (never only as
a mask), so that every reported measurement can be reproduced: ``ROI.to_mask(shape, spacing,
origin)`` is deterministic and the definition's SHA-256 is recorded in reports.

Supported definitions: cylinder (centre, unit axis, radius, extent along axis), sphere, box,
and "mask" (a hashed label volume, for hand-drawn ROIs).

Automatic detectors (semi-automatic: they propose, the analyst confirms or edits):
* ``detect_plate_defect``  — condyle / calvarial: a circular gap in a dense cortical plate.
  Uses the per-column mineral fraction inside the cortical band, finds the low-fraction
  connected region nearest the image centre and fits a circle (algebraic Kåsa fit, or centre
  only if the nominal diameter is supplied).
* ``detect_segmental_gap`` — long-bone segmental / distraction gap along an axis: slices
  where the dense cortical ring is absent.
Each returns a confidence score and diagnostics; low confidence ⇒ requires manual review.
"""
from __future__ import annotations

import copy
import hashlib
import json
import time
from dataclasses import asdict, dataclass, field

import numpy as np
from scipy import ndimage as ndi


class ROIDetectionError(RuntimeError):
    pass


@dataclass
class ROI:
    kind: str                                   # cylinder | sphere | box | mask
    params: dict                                # physical µm, axis order (z, y, x)
    method: str = "manual"
    confidence: float | None = None
    diagnostics: dict = field(default_factory=dict)
    history: list = field(default_factory=list)  # [{"time","user","action","params","reason"}]

    def definition(self) -> dict:
        return {"kind": self.kind, "params": self.params}

    def definition_hash(self) -> str:
        return hashlib.sha256(json.dumps(self.definition(), sort_keys=True, default=float).encode()).hexdigest()

    def to_dict(self):
        d = asdict(self)
        d["definition_sha256"] = self.definition_hash()
        return d

    @staticmethod
    def from_dict(d) -> "ROI":
        d = dict(d)
        d.pop("definition_sha256", None)
        return ROI(**d)

    def revise(self, new_params: dict, user: str, reason: str) -> "ROI":
        r = copy.deepcopy(self)
        r.history.append({"time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "user": user,
                          "action": "revise", "previous": self.params, "reason": reason})
        r.params = {**self.params, **new_params}
        r.method = f"{self.method}+manual-edit"
        return r

    # ------------------------------------------------------------------ rasterisation
    def to_mask(self, shape, spacing, origin=(0.0, 0.0, 0.0)) -> np.ndarray:
        sp = np.asarray(spacing, float)
        org = np.asarray(origin, float)
        if self.kind == "mask":
            m = np.asarray(self.params["_mask"], bool)
            return m
        zz, yy, xx = [np.arange(n) * s + o for n, s, o in zip(shape, sp, org)]
        if self.kind == "cylinder":
            c = np.asarray(self.params["center_um"], float)
            a = np.asarray(self.params["axis"], float)
            a = a / np.linalg.norm(a)
            r = float(self.params["radius_um"])
            h0, h1 = self.params["extent_um"]  # signed distance along axis from centre
            Z, Y, X = np.meshgrid(zz - c[0], yy - c[1], xx - c[2], indexing="ij", sparse=True)
            t = Z * a[0] + Y * a[1] + X * a[2]
            rad2 = (Z - t * a[0]) ** 2 + (Y - t * a[1]) ** 2 + (X - t * a[2]) ** 2
            return (rad2 <= r * r) & (t >= h0) & (t <= h1)
        if self.kind == "sphere":
            c = np.asarray(self.params["center_um"], float)
            r = float(self.params["radius_um"])
            Z, Y, X = np.meshgrid(zz - c[0], yy - c[1], xx - c[2], indexing="ij", sparse=True)
            return Z ** 2 + Y ** 2 + X ** 2 <= r * r
        if self.kind == "box":
            lo, hi = np.asarray(self.params["min_um"]), np.asarray(self.params["max_um"])
            Z, Y, X = np.meshgrid(zz, yy, xx, indexing="ij", sparse=True)
            return ((Z >= lo[0]) & (Z <= hi[0]) & (Y >= lo[1]) & (Y <= hi[1]) & (X >= lo[2]) & (X <= hi[2]))
        raise ValueError(self.kind)


def cylinder_roi(center_um, axis, radius_um, extent_um, method="manual", **kw) -> ROI:
    return ROI("cylinder", {"center_um": [float(c) for c in center_um], "axis": [float(a) for a in axis],
                            "radius_um": float(radius_um), "extent_um": [float(e) for e in extent_um]},
               method=method, **kw)


def cylinder_from_landmarks(p_top_um, p_bottom_um, radius_um) -> ROI:
    """Analyst clicks two points on the defect axis (entry and floor) and gives the radius."""
    p0, p1 = np.asarray(p_top_um, float), np.asarray(p_bottom_um, float)
    a = p1 - p0
    L = float(np.linalg.norm(a))
    if L == 0:
        raise ValueError("Landmarks coincide")
    c = (p0 + p1) / 2
    return cylinder_roi(c, a / L, radius_um, (-L / 2, L / 2), method="landmarks")


def roi_from_mask(mask: np.ndarray, method="manual-mask") -> ROI:
    h = hashlib.sha256(np.packbits(mask.astype(bool)).tobytes() + str(mask.shape).encode()).hexdigest()
    return ROI("mask", {"_mask": mask.astype(bool), "mask_sha256": h, "shape": list(mask.shape)}, method=method)


# ----------------------------------------------------------------------------- helpers
def _mineral_mask(img, spacing, smooth_um=30.0):
    from skimage.filters import threshold_otsu
    s = smooth_um / float(np.mean(spacing))
    g = ndi.gaussian_filter(img.astype(np.float32), s) if s > 0.3 else img.astype(np.float32)
    from ..segment.classical import robust_values
    v = robust_values(g[:: max(1, g.shape[0] // 48), :: 2, :: 2])
    t = float(threshold_otsu(v))
    return g > t, t


def kasa_circle_fit(pts):
    """Algebraic least-squares circle fit. pts: (N,2). Returns (cy, cx, r, rms_residual)."""
    y, x = pts[:, 0].astype(float), pts[:, 1].astype(float)
    A = np.c_[2 * y, 2 * x, np.ones_like(x)]
    b = y ** 2 + x ** 2
    (cy, cx, c), *_ = np.linalg.lstsq(A, b, rcond=None)
    r = np.sqrt(max(c + cy ** 2 + cx ** 2, 0))
    res = np.sqrt((y - cy) ** 2 + (x - cx) ** 2) - r
    return cy, cx, r, float(np.sqrt((res ** 2).mean()))


# ----------------------------------------------------------------------------- detectors
def detect_plate_defect(img: np.ndarray, spacing, model="condyle", nominal_diameter_um=None,
                        cortical_band_um=200.0, depth_um=None, origin=(0, 0, 0)) -> ROI:
    """Detect a circular defect through a cortical plate whose normal is the z axis."""
    sp = np.asarray(spacing, float)
    mineral, t = _mineral_mask(img, sp)
    Z = img.shape[0]
    zprof = mineral.mean(axis=(1, 2))
    if model == "condyle":
        # bone surface = first z (from top) where mineral fraction rises above half its max
        top = int(np.argmax(zprof > 0.5 * zprof.max()))
        band = slice(top, min(Z, top + max(1, int(round(cortical_band_um / sp[0])))))
        bands = [band]
    elif model == "calvarial":
        nz = np.where(zprof > 0.5 * zprof.max())[0]
        if len(nz) == 0:
            raise ROIDetectionError("No plate found")
        top, bot = int(nz.min()), int(nz.max())
        k = max(1, int(round(cortical_band_um / sp[0])))
        bands = [slice(top, top + k), slice(max(top, bot - k + 1), bot + 1)]
    else:
        raise ValueError(model)
    frac = np.mean([mineral[b].mean(axis=0) for b in bands], axis=0)
    frac_s = ndi.gaussian_filter(frac, 2.0)
    low = frac_s < 0.6
    lab, n = ndi.label(low)
    if n == 0:
        raise ROIDetectionError("No cortical gap detected (plate appears intact)")
    cy0, cx0 = (np.array(frac.shape) - 1) / 2
    best, bestd = None, np.inf
    objs = ndi.find_objects(lab)
    for i in range(1, n + 1):
        com = ndi.center_of_mass(lab == i)
        # exclude regions touching the border (outside of bone)
        sl = objs[i - 1]
        touches = any(s.start == 0 or s.stop == dim for s, dim in zip(sl, frac.shape))
        d = np.hypot(com[0] - cy0, com[1] - cx0)
        size = (lab == i).sum()
        if touches or size < 20:
            continue
        if d < bestd:
            best, bestd = i, d
    if best is None:
        raise ROIDetectionError("Only border-touching low-density regions found")
    reg = ndi.binary_fill_holes(lab == best)
    edge = reg & ~ndi.binary_erosion(reg)
    pts = np.argwhere(edge) * sp[1:]
    cy, cx, r, rms = kasa_circle_fit(pts)
    area_r = np.sqrt(reg.sum() * sp[1] * sp[2] / np.pi)
    if nominal_diameter_um:
        r_used = nominal_diameter_um / 2
    else:
        r_used = r
    # confidence: circularity of fit, size consistency with nominal, contrast of the gap
    inside = frac_s[reg].mean()
    outside_ring = (ndi.binary_dilation(reg, iterations=4) & ~ndi.binary_dilation(reg, iterations=1))
    contrast = float(frac_s[outside_ring].mean() - inside) if outside_ring.any() else 0.0
    circ = float(np.exp(-rms / max(r, 1e-6) * 5))
    size_ok = float(np.exp(-abs(r - r_used) / max(r_used, 1e-6) * 3)) if nominal_diameter_um else 1.0
    conf = float(np.clip(circ * size_ok * np.clip(contrast / 0.5, 0, 1), 0, 1))
    if model == "condyle":
        z_top = (band.start) * sp[0]
        depth = depth_um if depth_um else (Z - band.start) * sp[0] * 0.85
        extent = (z_top, z_top + depth)
    else:
        z_top, z_bot = bands[0].start * sp[0], (bands[-1].stop - 1) * sp[0]
        extent = (z_top, z_bot)
    c = (np.asarray(origin) + np.array([0.0, cy, cx]))
    center = [0.0 + origin[0], float(c[1]), float(c[2])]
    roi = cylinder_roi(center, (1.0, 0.0, 0.0), r_used, (extent[0], extent[1]), method=f"auto-plate-{model}",
                       confidence=conf,
                       diagnostics={"fit_radius_um": float(r), "area_radius_um": float(area_r),
                                    "fit_rms_um": rms, "gap_contrast": contrast, "mineral_threshold": t,
                                    "requires_review": conf < 0.6})
    return roi


def detect_segmental_gap(img: np.ndarray, spacing, axis=0, min_gap_um=500.0, radius_margin=1.05) -> ROI:
    """Detect a segmental / distraction gap: contiguous slices lacking dense cortical bone."""
    sp = np.asarray(spacing, float)
    x = np.moveaxis(img, axis, 0)
    spx = np.r_[sp[axis], np.delete(sp, axis)]
    from skimage.filters import threshold_multiotsu
    g = ndi.gaussian_filter(x.astype(np.float32), 1.0)
    from ..segment.classical import robust_values
    v = robust_values(g[:: max(1, g.shape[0] // 64), :: 2, :: 2])
    t_lo, t_hi = threshold_multiotsu(v, classes=3)
    metal = g > np.percentile(v, 99.95) * 1.15 if v.size else np.zeros_like(g, bool)
    g = np.where(metal, t_lo, g)  # suppress hardware/metal so it is not mistaken for cortex
    dense = g > t_hi
    # cortical envelope from the max projection of dense bone along the axis; score each slice by
    # dense occupancy of the envelope's outer annulus (cortex), so dense graft inside the cavity
    # does not masquerade as cortex.
    proj = ndi.binary_fill_holes(ndi.binary_closing(dense.mean(0) > 0.15, iterations=3))
    if not proj.any():
        raise ROIDetectionError("No dense bone found")
    lab2, n2 = ndi.label(proj)
    proj = lab2 == (1 + int(np.argmax(ndi.sum(proj, lab2, range(1, n2 + 1)))))
    r_env = np.sqrt(proj.sum() / np.pi)
    ring = proj & ~ndi.binary_erosion(proj, iterations=max(1, int(0.25 * r_env)))
    prof = dense[:, ring].mean(axis=1)
    ps = ndi.gaussian_filter1d(prof, 1.5)
    specimen = dense.mean(axis=(1, 2)) > 0.1 * dense.mean(axis=(1, 2)).max()
    level = np.percentile(ps[specimen], 75) if specimen.any() else ps.max()
    hi = level
    low = (ps < 0.6 * level) & specimen
    lab, n = ndi.label(low)
    if n == 0:
        raise ROIDetectionError("No gap: dense cortex present in all slices")
    sizes = ndi.sum(low, lab, range(1, n + 1))
    # prefer interior runs (bone on both sides)
    best, bs = None, 0
    for i, s in enumerate(sizes, 1):
        idx = np.where(lab == i)[0]
        sp_idx = np.where(specimen)[0]
        interior = idx.min() > sp_idx.min() and idx.max() < sp_idx.max()
        if interior and s > bs:
            best, bs = i, s
    if best is None:
        raise ROIDetectionError("Low-density runs only at volume ends (gap not bounded by bone)")
    idx = np.where(lab == best)[0]
    z0, z1 = int(idx.min()), int(idx.max())
    if (z1 - z0 + 1) * spx[0] < min_gap_um:
        raise ROIDetectionError(f"Gap shorter than {min_gap_um} µm")
    # cross-sectional envelope from adjacent cortical slices
    near = np.r_[max(0, z0 - 5):z0, z1 + 1:min(len(prof), z1 + 6)]
    env = ndi.binary_fill_holes(ndi.binary_closing(dense[near].any(0), iterations=3))
    if not env.any():
        raise ROIDetectionError("No cortical envelope next to gap")
    cy, cx = ndi.center_of_mass(env)
    r = np.sqrt(env.sum() / np.pi) * float(np.mean(spx[1:])) * radius_margin
    centre = np.zeros(3)
    centre[axis] = 0.0
    other = [i for i in range(3) if i != axis]
    centre[other[0]] = cy * spx[1]
    centre[other[1]] = cx * spx[2]
    ax = np.zeros(3)
    ax[axis] = 1.0
    contrast = float(1 - ps[z0:z1 + 1].mean() / hi) if hi > 0 else 0.0
    conf = float(np.clip(contrast, 0, 1))
    return cylinder_roi(centre, ax, r, (z0 * spx[0], z1 * spx[0]), method="auto-segmental", confidence=conf,
                        diagnostics={"gap_slices": [z0, z1], "gap_length_um": float((z1 - z0 + 1) * spx[0]),
                                     "dense_threshold": float(t_hi), "profile": ps.round(4).tolist(),
                                     "requires_review": conf < 0.6})


def roi_dice(a: np.ndarray, b: np.ndarray) -> float:
    s = a.sum() + b.sum()
    return float(2 * (a & b).sum() / s) if s else float("nan")
