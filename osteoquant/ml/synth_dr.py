"""Domain-randomised synthesis of training patches from phantom partial-volume truth.

Motivation (FORENSIC_AUDIT FA-02): a U-Net trained on phantom images rendered with one physics model
failed zero-shot on real micro-CT (Dice 0.379). Following the domain-randomisation idea of
SynthSeg-style training (contrast-agnostic synthesis from label maps), images are re-synthesised on the
fly from the phantom's exact class fractions with randomised:

* class intensities (constrained only by physics ordering: mineralised classes brighter than soft tissue;
  graft may be brighter or darker than bone),
* within-class texture (smooth multiplicative random fields),
* resolution/scale (random zoom 0.6–2.0×, i.e. structure size in voxels),
* point-spread blur, white and spatially correlated noise, smooth bias field, gamma,
* flips and 90° rotations.

The label target is either the 4-class map (``target="classes"``) or mineral vs non-mineral
(``target="mineral"``) for transfer to real two-class data.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import ndimage as ndi


@dataclass
class DRConfig:
    patch: tuple = (48, 48, 48)
    scale_range: tuple = (0.6, 2.0)          # >1 = structures appear larger (zoom in)
    soft_range: tuple = (0.0, 0.35)
    mineral_contrast_min: float = 0.2        # min (mineral − soft) intensity
    bone_range: tuple = (0.45, 1.0)
    graft_range: tuple = (0.3, 1.8)
    texture_cv: tuple = (0.0, 0.15)
    blur_vox: tuple = (0.0, 1.5)
    noise_white: tuple = (0.0, 0.12)
    noise_corr: tuple = (0.0, 0.10)
    noise_corr_sigma: tuple = (0.6, 2.0)
    bias_amp: tuple = (0.0, 0.15)
    gamma: tuple = (0.75, 1.35)
    background_gap: tuple = (0.0, 0.9)       # how much darker than soft tissue the volume's 1st percentile is
    top_scale: tuple = (0.9, 1.3)            # 99.8th percentile relative to the brightest phase
    target: str = "mineral"                  # "mineral" | "classes"


def _smooth_field(shape, sigma, rng):
    f = ndi.gaussian_filter(rng.standard_normal(shape).astype(np.float32), sigma)
    return f / (f.std() + 1e-6)


class DRSampler:
    """Callable ``sampler(rng) -> (x[1,Z,Y,X] float32, y[Z,Y,X] int64)`` for ``train_model(sample_fn=...)``."""

    name = "dr_v2"

    def __init__(self, fraction_volumes: list[np.ndarray], cfg: DRConfig | None = None, manifest: list | None = None):
        # fraction_volumes: list of (4, Z, Y, X) uint8 (0..255) class-fraction arrays
        # manifest: provenance records of the source volumes (recorded in the model card; review ARC-02)
        self.fr = fraction_volumes
        self.cfg = cfg or DRConfig()
        self.manifest = manifest

    def __call__(self, rng: np.random.Generator):
        c = self.cfg
        fr = self.fr[rng.integers(len(self.fr))]
        ps = np.array(c.patch)
        s = float(np.exp(rng.uniform(*np.log(c.scale_range))))
        # keep the zoom isotropic (review ML-07): if the source crop would exceed the volume in any axis,
        # increase the scale for all axes instead of clipping one axis
        s = max(s, float(np.max(ps / np.array(fr.shape[1:]))))
        src = np.maximum(4, np.minimum(np.round(ps / s).astype(int), np.array(fr.shape[1:])))
        o = [int(rng.integers(0, fr.shape[1 + i] - src[i] + 1)) for i in range(3)]
        sl = tuple(slice(o[i], o[i] + src[i]) for i in range(3))
        f = fr[(slice(None),) + sl].astype(np.float32) / 255.0
        zoom = ps / src
        f = np.stack([ndi.zoom(f[k], zoom, order=1) for k in range(4)])
        f = f[:, : ps[0], : ps[1], : ps[2]]
        tot = f.sum(0, keepdims=True) + 1e-6
        f = f / tot
        # intensities
        soft = rng.uniform(*c.soft_range)
        bone_lo = soft + c.mineral_contrast_min
        host = rng.uniform(max(bone_lo, c.bone_range[0]), max(bone_lo + 0.05, c.bone_range[1]))
        new = rng.uniform(max(bone_lo, c.bone_range[0] * 0.9), max(bone_lo + 0.02, host))
        graft = rng.uniform(max(bone_lo, c.graft_range[0]), c.graft_range[1])
        mus = [soft, new, graft, host]
        img = np.zeros(f.shape[1:], np.float32)
        for k, mu in enumerate(mus):
            cv = rng.uniform(*c.texture_cv)
            tex = 1.0 + cv * _smooth_field(img.shape, rng.uniform(1.0, 3.0), rng) if cv > 0 else 1.0
            img += f[k] * mu * tex
        b = rng.uniform(*c.blur_vox)
        if b > 0.05:
            img = ndi.gaussian_filter(img, b)
        img += rng.normal(0, rng.uniform(*c.noise_white), img.shape).astype(np.float32)
        nc = rng.uniform(*c.noise_corr)
        if nc > 0:
            img += nc * _smooth_field(img.shape, rng.uniform(*c.noise_corr_sigma), rng)
        ba = rng.uniform(*c.bias_amp)
        if ba > 0:
            img *= 1.0 + ba * _smooth_field(img.shape, 12.0, rng)
        # Emulate WHOLE-VOLUME percentile normalisation used at inference (ml.train.normalize_image), not
        # per-patch normalisation (review ML-03): the volume's 1st percentile is usually darker than soft tissue
        # (air/holder/background) and its 99.8th percentile is near the densest mineral in the field of view, so
        # soft tissue lands anywhere in ≈[0, 0.75] after normalisation.
        lo = soft - rng.uniform(*c.background_gap)
        hi = max(host, graft if f[2].max() > 0.5 else host) * rng.uniform(*c.top_scale)
        x = (img - lo) / max(hi - lo, 1e-6)
        g = rng.uniform(*c.gamma)
        x = np.sign(x) * np.abs(x) ** g
        lab = f.argmax(0)
        y = (lab > 0).astype(np.int64) if c.target == "mineral" else lab.astype(np.int64)
        for ax in range(3):
            if rng.random() < 0.5:
                x = np.flip(x, ax)
                y = np.flip(y, ax)
        if rng.random() < 0.5:
            k = int(rng.integers(1, 4))
            x = np.rot90(x, k, axes=(1, 2))
            y = np.rot90(y, k, axes=(1, 2))
        return np.ascontiguousarray(x[None].astype(np.float32)), np.ascontiguousarray(y)


def describe_sampler(sampler: "DRSampler") -> dict:
    """Full, hashable description of a sampler for model cards (review ARC-04)."""
    import hashlib
    from dataclasses import asdict
    h = hashlib.sha256()
    for f in sampler.fr:
        h.update(np.ascontiguousarray(f).tobytes())
    return {"name": sampler.name, "config": asdict(sampler.cfg), "n_sources": len(sampler.fr),
            "sources_sha256": h.hexdigest()}
