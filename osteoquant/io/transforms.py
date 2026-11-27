"""Spatial transforms: resampling, orientation normalization, intensity normalization."""
from __future__ import annotations

import numpy as np
from scipy import ndimage as ndi

from ..volume import Volume


def resample_to_spacing(vol: Volume, target_um, order: int = 1, labels: bool = False) -> Volume:
    """Resample to target spacing (µm). order=0 for label maps. Records resampling factor in meta.

    Anti-aliasing: when downsampling intensity images, a Gaussian prefilter with
    sigma = 0.5 * (factor - 1) voxels (per axis) is applied, a standard heuristic.
    """
    tgt = np.array(target_um if np.iterable(target_um) else [target_um] * 3, dtype=float)
    src = np.array(vol.spacing, dtype=float)
    zoom = src / tgt
    data = vol.data
    if not labels and np.any(zoom < 1):
        sig = np.where(zoom < 1, 0.5 * (1 / zoom - 1), 0)
        data = ndi.gaussian_filter(data.astype(np.float32), sig)
    out = ndi.zoom(data, zoom, order=0 if labels else order, prefilter=order > 1)
    new = Volume(out.astype(vol.data.dtype) if labels else out, tuple(tgt), vol.origin,
                 vol.direction.copy(), dict(vol.meta))
    hist = new.meta.setdefault("resampling", [])
    hist.append({"from_um": src.tolist(), "to_um": tgt.tolist(), "order": 0 if labels else order})
    return new


def to_isotropic(vol: Volume, order=1, labels=False) -> Volume:
    if vol.is_isotropic:
        return vol
    return resample_to_spacing(vol, min(vol.spacing), order=order, labels=labels)


def normalize_orientation(vol: Volume) -> Volume:
    """Reorder/flip axes so direction ≈ identity (RAS-agnostic canonical index order).

    Uses the dominant component of each direction column. Physical geometry is preserved.
    """
    D = vol.direction
    perm = np.argmax(np.abs(D), axis=0)  # physical axis for each index axis
    if sorted(perm.tolist()) != [0, 1, 2]:
        raise ValueError("Oblique direction cosines cannot be normalized by permutation; resample instead")
    order = np.argsort(perm)
    data = np.transpose(vol.data, order)
    spacing = tuple(np.array(vol.spacing)[order])
    D2 = D[:, order]
    flips = [i for i in range(3) if D2[i, i] < 0]
    for i in flips:
        data = np.flip(data, axis=i)
    origin = np.array(vol.origin, dtype=float)
    for i in flips:
        origin = origin + D2[:, i] * (vol.data.shape[order[i]] - 1) * spacing[i]
    D3 = np.abs(np.diag(np.diag(D2)))
    out = Volume(np.ascontiguousarray(data), spacing, tuple(origin), D3 if np.allclose(np.abs(D2), D3) else np.eye(3),
                 dict(vol.meta))
    out.meta["orientation_normalized"] = {"permutation": order.tolist(), "flips": flips}
    return out


def percentile_normalize(x: np.ndarray, lo=0.5, hi=99.5, mask=None) -> tuple[np.ndarray, tuple[float, float]]:
    s = x[mask] if mask is not None else x[:: max(1, x.shape[0] // 64)]
    a, b = np.percentile(s, [lo, hi])
    if b <= a:
        b = a + 1
    return ((x.astype(np.float32) - a) / (b - a)), (float(a), float(b))


def histogram_match(x: np.ndarray, ref: np.ndarray, n_quantiles: int = 256) -> np.ndarray:
    """Piecewise-linear quantile mapping of x's histogram onto ref's (cross-scanner harmonization)."""
    q = np.linspace(0, 100, n_quantiles)
    xs = np.percentile(x[:: max(1, x.shape[0] // 64)], q)
    rs = np.percentile(ref[:: max(1, ref.shape[0] // 64)], q)
    xs, idx = np.unique(xs, return_index=True)
    return np.interp(x, xs, rs[idx]).astype(np.float32)


def apply_calibration(vol: Volume, slope: float, intercept: float, unit="mgHA/cm3", source="") -> Volume:
    """Linear grey→density calibration from an HA phantom. Records the calibration in meta."""
    out = vol.with_data(vol.data.astype(np.float32) * slope + intercept, intensity_unit=unit)
    out.meta["calibration"] = {"slope": slope, "intercept": intercept, "unit": unit, "source": source}
    return out


def fit_ha_calibration(measured_grey: list[float], known_mgHA: list[float]) -> dict:
    """Least-squares linear calibration from phantom inserts. Returns slope, intercept, r2."""
    x, y = np.asarray(measured_grey, float), np.asarray(known_mgHA, float)
    if len(x) < 2:
        raise ValueError("Need ≥2 phantom inserts")
    A = np.vstack([x, np.ones_like(x)]).T
    (m, c), res, *_ = np.linalg.lstsq(A, y, rcond=None)
    yhat = m * x + c
    ss = ((y - y.mean()) ** 2).sum()
    r2 = 1 - ((y - yhat) ** 2).sum() / ss if ss > 0 else 1.0
    return {"slope": float(m), "intercept": float(c), "r2": float(r2), "n_inserts": int(len(x))}
