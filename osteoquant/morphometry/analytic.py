"""Geometric test objects with analytically known morphometry (for Experiment G and tests)."""
from __future__ import annotations

import numpy as np


def sphere(shape, center, radius):
    zz, yy, xx = np.ogrid[: shape[0], : shape[1], : shape[2]]
    return (zz - center[0]) ** 2 + (yy - center[1]) ** 2 + (xx - center[2]) ** 2 <= radius ** 2


def plates(shape, thickness_vox: int, spacing_vox: int, axis=0):
    """Parallel plates (thickness t, gap s). Exact Tb.Th = t, Tb.Sp = s, BV/TV = t/(t+s)."""
    m = np.zeros(shape, bool)
    period = thickness_vox + spacing_vox
    idx = np.arange(shape[axis])
    on = (idx % period) < thickness_vox
    sl = [None, None, None]
    sl[axis] = slice(None)
    m[...] = np.broadcast_to(on[tuple(sl)], shape)
    return m


def rods(shape, diameter_vox: float, spacing_vox: int):
    """Square lattice of parallel cylinders along z. Exact local thickness = diameter."""
    yy, xx = np.mgrid[: shape[1], : shape[2]]
    p = spacing_vox
    cy = (yy % p) - (p - 1) / 2
    cx = (xx % p) - (p - 1) / 2
    disk = cy ** 2 + cx ** 2 <= (diameter_vox / 2) ** 2
    return np.broadcast_to(disk[None], shape).copy()


def hollow_cylinder(shape, r_out, r_in):
    """Tube along z (cortical shell analogue). Exact wall thickness = r_out - r_in."""
    yy, xx = np.mgrid[: shape[1], : shape[2]]
    r2 = (yy - (shape[1] - 1) / 2) ** 2 + (xx - (shape[2] - 1) / 2) ** 2
    ring = (r2 <= r_out ** 2) & (r2 > r_in ** 2)
    return np.broadcast_to(ring[None], shape).copy()


def torus_count_phantom(shape, n_holes: int):
    """A slab with n through-holes: β1 = n exactly (Euler: χ = 1 - n)."""
    m = np.zeros(shape, bool)
    z0, z1 = shape[0] // 3, 2 * shape[0] // 3
    m[z0:z1, 2:-2, 2:-2] = True
    xs = np.linspace(6, shape[2] - 7, n_holes).astype(int)
    for x in xs:
        m[z0:z1, shape[1] // 2 - 2: shape[1] // 2 + 2, x - 1:x + 2] = False
    return m
