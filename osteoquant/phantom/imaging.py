"""Mode A — fast reconstructed-volume simulation with controllable degradations.

Grey value model:  g = gain * mu_eff (1/cm) * 1000 + offset, then degradations in this order:
beam-hardening-like cupping → PSF blur → resolution change (downsample) → ring artifacts →
noise (Gaussian and/or Poisson-like signal-dependent) → scanner intensity shift → quantisation.

This mode does NOT model projection physics; it reproduces the *appearance* of common
reconstructed-volume degradations with controllable strength. Mode B (ctsim.py) is the
physically motivated alternative.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass

import numpy as np
from scipy import ndimage as ndi

from ..volume import Volume


@dataclass
class ImagingConfig:
    gain: float = 1.0
    offset: float = 0.0
    psf_sigma_um: float = 0.0          # Gaussian PSF sigma (true resolution), µm
    noise_sigma: float = 0.0           # additive Gaussian noise, in grey units (mu*1000 scale)
    poisson_scale: float = 0.0         # signal-dependent noise: var = poisson_scale * g
    cupping: float = 0.0               # fractional radial gain loss at centre (beam-hardening-like)
    ring_amplitude: float = 0.0        # grey units
    ring_count: int = 12
    shift: float = 0.0                 # additive scanner offset after noise
    scale: float = 1.0                 # multiplicative scanner gain after noise
    downsample: int = 1                # integer resolution reduction (block mean)
    dtype: str = "float32"             # or "uint16"
    seed: int = 0

    def to_dict(self):
        return asdict(self)


def render_fast(mu: np.ndarray, voxel_um: float, cfg: ImagingConfig) -> Volume:
    rng = np.random.default_rng(cfg.seed)
    g = mu.astype(np.float32) * 1000.0 * cfg.gain + cfg.offset
    Z, Y, X = g.shape
    if cfg.cupping:
        yy, xx = np.mgrid[:Y, :X]
        r = np.sqrt((yy - (Y - 1) / 2) ** 2 + (xx - (X - 1) / 2) ** 2) / (0.5 * np.hypot(Y, X))
        prof = 1.0 - cfg.cupping * (1 - np.clip(r, 0, 1) ** 2)
        g = g * prof[None].astype(np.float32)
    if cfg.psf_sigma_um > 0:
        g = ndi.gaussian_filter(g, cfg.psf_sigma_um / voxel_um)
    vox = voxel_um
    if cfg.downsample > 1:
        f = cfg.downsample
        s = [n // f for n in g.shape]
        g = g[: s[0] * f, : s[1] * f, : s[2] * f].reshape(s[0], f, s[1], f, s[2], f).mean(axis=(1, 3, 5))
        vox = voxel_um * f
        Z, Y, X = g.shape
    if cfg.ring_amplitude:
        yy, xx = np.mgrid[:Y, :X]
        r = np.sqrt((yy - (Y - 1) / 2) ** 2 + (xx - (X - 1) / 2) ** 2)
        radii = rng.uniform(2, min(Y, X) / 2, cfg.ring_count)
        amps = rng.normal(0, 1, cfg.ring_count)
        ring = np.zeros((Y, X), np.float32)
        for rr, aa in zip(radii, amps):
            ring += aa * np.exp(-0.5 * ((r - rr) / 0.7) ** 2)
        g = g + cfg.ring_amplitude * ring[None]
    if cfg.poisson_scale > 0:
        g = g + rng.standard_normal(g.shape).astype(np.float32) * np.sqrt(np.maximum(g, 0) * cfg.poisson_scale)
    if cfg.noise_sigma > 0:
        g = g + rng.standard_normal(g.shape).astype(np.float32) * cfg.noise_sigma
    g = g * cfg.scale + cfg.shift
    if cfg.dtype == "uint16":
        g = np.clip(np.round(g), 0, 65535).astype(np.uint16)
    else:
        g = g.astype(np.float32)
    vol = Volume(g, (vox, vox, vox), meta={"provenance": "synthetic", "simulator": "fast-v1",
                                          "imaging": cfg.to_dict(), "intensity_unit": "synthetic-grey",
                                          "ingest": {"metadata_found": {"spacing_um": [vox] * 3, "source": "generator"},
                                                     "metadata_assumed": {}}})
    return vol


def downsample_labels(labels: np.ndarray, f: int) -> np.ndarray:
    """Majority-vote label downsampling consistent with block-mean image downsampling."""
    if f == 1:
        return labels
    s = [n // f for n in labels.shape]
    lab = labels[: s[0] * f, : s[1] * f, : s[2] * f]
    classes = np.unique(lab)
    counts = np.stack([(lab == c).reshape(s[0], f, s[1], f, s[2], f).sum(axis=(1, 3, 5)) for c in classes])
    return classes[np.argmax(counts, axis=0)].astype(labels.dtype)


def missing_region(vol: Volume, frac: float = 0.1, rng=None) -> tuple[Volume, np.ndarray]:
    """Zero out a random slab (simulates truncated FOV / missing slices). Returns mask of removed."""
    rng = rng or np.random.default_rng(0)
    n = vol.shape[0]
    k = max(1, int(n * frac))
    z0 = int(rng.integers(0, n - k))
    d = vol.data.copy()
    d[z0:z0 + k] = 0
    m = np.zeros(vol.shape, bool)
    m[z0:z0 + k] = True
    return vol.with_data(d), m
