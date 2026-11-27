"""Procedural 3D structure primitives (all operate on voxel grids in µm units)."""
from __future__ import annotations

import numpy as np
from scipy import ndimage as ndi


def grf(shape, sigma_vox: float, rng: np.random.Generator) -> np.ndarray:
    """Zero-mean unit-variance Gaussian random field (Gaussian-filtered white noise)."""
    g = ndi.gaussian_filter(rng.standard_normal(shape).astype(np.float32), sigma_vox, mode="wrap")
    g -= g.mean()
    g /= g.std() + 1e-8
    return g


def trabecular_network(shape, voxel_um: float, tb_sp_um: float, bv_tv: float,
                       rng: np.random.Generator, anisotropy=(1.0, 1.0, 1.0)) -> np.ndarray:
    """Plate/rod network from the zero level-set of a band-limited Gaussian random field.

    ``|g| < t`` around the zero crossing of a smooth GRF yields an interconnected sheet/rod
    network whose spacing scales with the field correlation length and whose volume fraction
    is set exactly by the quantile threshold ``t``. Spacing control is approximate; measured
    Tb.Th/Tb.Sp are reported by the morphometry engine (verified in Experiment G).
    """
    sigma = max(0.8, 0.30 * tb_sp_um / voxel_um)
    sig = tuple(sigma * a for a in anisotropy)
    g = ndi.gaussian_filter(rng.standard_normal(shape).astype(np.float32), sig, mode="wrap")
    # second, coarser octave adds heterogeneity
    g2 = ndi.gaussian_filter(rng.standard_normal(shape).astype(np.float32), [s * 2.5 for s in sig], mode="wrap")
    g = g / (g.std() + 1e-8) + 0.35 * g2 / (g2.std() + 1e-8)
    a = np.abs(g)
    t = np.quantile(a[:: max(1, shape[0] // 32)], bv_tv)
    return a < t


def smooth_field(shape, sigma_vox, rng, cv=0.05) -> np.ndarray:
    """Multiplicative heterogeneity field with mean 1 and coefficient of variation ``cv``."""
    if cv <= 0:
        return np.ones(shape, np.float32)
    return (1.0 + cv * grf(shape, sigma_vox, rng)).astype(np.float32)


def cylinder_mask(shape, center_zyx, axis: str, radius_vox: float, z_range=None) -> np.ndarray:
    """Right circular cylinder; axis in {'z','y','x'}; z_range bounds along the axis (voxels)."""
    zz, yy, xx = np.ogrid[: shape[0], : shape[1], : shape[2]]
    cz, cy, cx = center_zyx
    if axis == "z":
        r2 = (yy - cy) ** 2 + (xx - cx) ** 2
        along = zz
    elif axis == "y":
        r2 = (zz - cz) ** 2 + (xx - cx) ** 2
        along = yy
    else:
        r2 = (zz - cz) ** 2 + (yy - cy) ** 2
        along = xx
    m = r2 <= radius_vox ** 2
    m = np.broadcast_to(m, shape).copy()
    if z_range is not None:
        lo, hi = z_range
        a = np.broadcast_to(along, shape)
        m &= (a >= lo) & (a < hi)
    return m


def pack_granules(region: np.ndarray, voxel_um: float, diam_um: tuple[float, float], fill_fraction: float,
                  rng: np.random.Generator, roughness: float = 0.15, min_gap_um: float = 0.0,
                  max_tries: int = 20000) -> tuple[np.ndarray, list[dict]]:
    """Random sequential addition of irregular granules inside ``region``.

    Placement is done in continuous space: candidate centres are drawn from voxels whose
    distance to the region boundary exceeds the granule's bounding radius, and overlap is
    tested analytically against already-placed bounding spheres (O(N) per try). Granules are
    then rasterised once as spheres with a low-order angular radius perturbation
    (``roughness`` = relative amplitude), mimicking crushed/sintered ceramic granules.
    Returns (instance-label array, list of granule records).
    """
    shape = region.shape
    inst = np.zeros(shape, np.int32)
    if not region.any():
        return inst, []
    d_in = ndi.distance_transform_edt(region).astype(np.float32)
    target = fill_fraction * region.sum()
    cand_all = np.argwhere(d_in > 0)
    centres, radii, recs = [], [], []
    filled = 0.0
    tries = 0
    gap = min_gap_um / voxel_um
    while filled < target and tries < max_tries:
        tries += 1
        d = rng.uniform(*diam_um)
        r = d / 2 / voxel_um
        rb = r * (1 + roughness)
        c = cand_all[rng.integers(len(cand_all))] + rng.uniform(-0.5, 0.5, 3)
        ci = np.clip(np.round(c).astype(int), 0, np.array(shape) - 1)
        if d_in[tuple(ci)] < rb:
            continue
        if centres:
            C = np.asarray(centres)
            if np.any(np.linalg.norm(C - c, axis=1) < (np.asarray(radii) + rb + gap)):
                continue
        centres.append(c)
        radii.append(rb)
        filled += 4.0 / 3.0 * np.pi * r ** 3
        recs.append({"id": len(recs) + 1, "center_vox": [float(x) for x in c], "diameter_um": float(d),
                     "_r": r})
    for rec, c in zip(recs, centres):
        r = rec.pop("_r")
        R = int(np.ceil(r * (1 + roughness))) + 1
        lo = np.maximum(np.floor(c).astype(int) - R, 0)
        hi = np.minimum(np.floor(c).astype(int) + R + 2, shape)
        zz, yy, xx = np.ogrid[lo[0]:hi[0], lo[1]:hi[1], lo[2]:hi[2]]
        dz, dy, dx = zz - c[0], yy - c[1], xx - c[2]
        dist = np.sqrt(dz ** 2 + dy ** 2 + dx ** 2) + 1e-6
        ph = rng.uniform(0, 2 * np.pi, 6)
        ang = (np.sin(3 * dz / dist + ph[0]) * np.cos(2 * dy / dist + ph[1])
               + np.sin(2 * dx / dist + ph[2]) * np.cos(3 * dz / dist + ph[3])
               + 0.5 * np.sin(4 * dy / dist + ph[4] + 2 * dx / dist))
        m = dist <= r * (1 + roughness * ang / 2.5)
        sl = tuple(slice(l, h) for l, h in zip(lo, hi))
        sub = inst[sl]
        sub[m & (sub == 0) & region[sl]] = rec["id"]
    return inst, recs


def erode_instances(inst: np.ndarray, fraction_removed: np.ndarray | float, voxel_um: float,
                    rng: np.random.Generator, irregularity: float = 0.5) -> np.ndarray:
    """Surface resorption: remove an outer shell from each instance so that approximately
    ``fraction_removed`` of its volume disappears; irregular via noisy distance map.
    ``fraction_removed`` may be per-instance array (indexed by id-1) or scalar."""
    if np.isscalar(fraction_removed) and fraction_removed <= 0:
        return inst.copy()
    mask = inst > 0
    dist = ndi.distance_transform_edt(mask).astype(np.float32)
    noise = grf(inst.shape, 2.0, rng) * irregularity
    dist_n = dist + noise * np.maximum(dist, 1) * 0.5
    out = inst.copy()
    ids = np.unique(inst[mask])
    objs = ndi.find_objects(inst)
    for i in ids:
        sl = objs[i - 1]
        if sl is None:
            continue
        sub = inst[sl] == i
        dsub = dist_n[sl][sub]
        f = float(fraction_removed if np.isscalar(fraction_removed) else fraction_removed[i - 1])
        f = min(max(f, 0.0), 1.0)
        if f >= 1.0:
            out[sl][sub] = 0
            continue
        thr = np.quantile(dsub, f)
        rem = np.zeros_like(sub)
        rem[sub] = dsub <= thr
        o = out[sl]
        o[rem] = 0
    return out


def shell(mask: np.ndarray, thickness_vox: float, outside=True) -> np.ndarray:
    """Layer of given thickness just outside (or inside) a mask."""
    if outside:
        d = ndi.distance_transform_edt(~mask)
        return (d > 0) & (d <= thickness_vox)
    d = ndi.distance_transform_edt(mask)
    return (d > 0) & (d <= thickness_vox)


def block_mean(a: np.ndarray, f: int) -> np.ndarray:
    """Downsample by integer factor using block averaging (exact partial-volume integration)."""
    if f == 1:
        return a.astype(np.float32)
    s = [n // f for n in a.shape]
    a = a[: s[0] * f, : s[1] * f, : s[2] * f]
    return a.reshape(s[0], f, s[1], f, s[2], f).mean(axis=(1, 3, 5), dtype=np.float32)


def block_fractions(lab: np.ndarray, f: int, classes) -> dict[int, np.ndarray]:
    return {c: block_mean((lab == c).astype(np.float32), f) for c in classes}
