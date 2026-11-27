"""Mode B — physically motivated CT acquisition + reconstruction simulation.

Pipeline (per axial slice, parallel-beam geometry):
1. Polychromatic source: Kramers bremsstrahlung spectrum Φ(E) ∝ (kVp − E)/E, filtered by
   ``filter_mm_al`` of aluminium using NIST attenuation (spectral hardening by the filter).
2. For each energy bin, line integrals of μ_m(E)·A_m over every material map A_m are computed
   with the Radon transform (skimage), giving energy-resolved path lengths.
3. Detected intensity I = Σ_E Φ(E)·η(E)·exp(−Σ_m μ_m(E) L_m) with an energy-integrating detector
   (η(E) ∝ E). Poisson counting noise from ``photons_per_ray``; additive scatter as a fraction of
   the unattenuated signal; per-detector gain errors produce ring artifacts.
4. Log-normalisation (−ln I/I0) — this is where *real* beam hardening appears, because the
   polychromatic log signal is not linear in path length.
5. Optional linear "water/HA" beam-hardening correction polynomial (as scanners apply).
6. Filtered back-projection (ramp/Shepp-Logan/Hann filter) via skimage.iradon.

Limitations (documented, important): parallel-beam slice-wise (no cone-beam artefacts, no
FDK), no detector blur beyond the pixel, no photon scatter physics (constant fraction model),
no motion, simplified spectrum. Open-source cone-beam frameworks (ASTRA, TIGRE) would remove
the first limitation; TIGRE needs CUDA and ASTRA's GPU paths were unavailable here.
"""
from __future__ import annotations

import time
from dataclasses import asdict, dataclass

import numpy as np

from ..volume import Volume
from .materials import COMPOSITIONS, mixture_mu_rho


@dataclass
class CTConfig:
    kvp: float = 80.0
    filter_mm_al: float = 0.5
    n_energy_bins: int = 12
    n_angles: int = 360
    photons_per_ray: float = 2e4
    scatter_fraction: float = 0.0
    ring_gain_sd: float = 0.0          # relative per-detector gain error
    fbp_filter: str = "shepp-logan"
    bh_correction: bool = False        # single-material (HA) linearisation
    seed: int = 0
    slices: tuple | None = None        # (z0, z1) subset to simulate

    def to_dict(self):
        d = asdict(self)
        return d


def spectrum(kvp: float, filter_mm_al: float, n_bins: int):
    E = np.linspace(10.0, kvp - 1.0, n_bins)
    phi = np.clip(kvp - E, 0, None) / E          # Kramers
    mu_al = mixture_mu_rho(COMPOSITIONS["aluminium"], E) * 2.70  # 1/cm
    phi = phi * np.exp(-mu_al * filter_mm_al / 10.0)
    w = phi * E                                   # energy-integrating detector weighting
    w = w / w.sum()
    return E, w


def effective_energy(kvp, filter_mm_al, n_bins=24):
    E, w = spectrum(kvp, filter_mm_al, n_bins)
    return float((E * w).sum())


def simulate_ct(material_fractions: dict, materials: dict, voxel_um: float, cfg: CTConfig) -> Volume:
    from skimage.transform import radon, iradon
    t0 = time.time()
    rng = np.random.default_rng(cfg.seed)
    E, w = spectrum(cfg.kvp, cfg.filter_mm_al, cfg.n_energy_bins)
    names = list(material_fractions)
    mus = {n: np.ravel(materials[n].mu(E)) for n in names}  # 1/cm per energy (at full density)
    shape = next(iter(material_fractions.values())).shape
    Z, Y, X = shape
    z0, z1 = cfg.slices or (0, Z)
    theta = np.linspace(0.0, 180.0, cfg.n_angles, endpoint=False)
    pix_cm = voxel_um * 1e-4
    out = np.zeros((z1 - z0, Y, X), np.float32)
    det_gain = None
    # HA linearisation table for beam-hardening correction
    mu_ha_eff = None
    if cfg.bh_correction:
        L = np.linspace(0, 1.5, 200)  # cm of HA-equivalent bone(1000 mgHA/cm3)
        from .materials import Material
        mb = np.ravel(Material("b", 0, mineral_mgHA_cm3=1000).mu(E))
        p_poly = -np.log((w[None, :] * np.exp(-np.outer(L, mb))).sum(1))
        mu_ha_eff = (w * mb).sum()
        p_lin = L * mu_ha_eff
    for zi, z in enumerate(range(z0, z1)):
        # energy-resolved line integrals: sum over materials of mu_m(E)*radon(A_m)
        sinos = {n: radon(material_fractions[n][z], theta=theta, circle=False) * pix_cm for n in names}
        if det_gain is None:
            nd = next(iter(sinos.values())).shape[0]
            det_gain = 1.0 + cfg.ring_gain_sd * rng.standard_normal(nd)
        Iacc = 0.0
        for k in range(len(E)):
            attn = sum(mus[n][k] * sinos[n] for n in names)
            Iacc = Iacc + w[k] * np.exp(-attn)
        I = Iacc
        if cfg.scatter_fraction > 0:
            I = I + cfg.scatter_fraction
        I = I * det_gain[:, None]
        if cfg.photons_per_ray and np.isfinite(cfg.photons_per_ray):
            counts = rng.poisson(np.clip(I, 0, None) * cfg.photons_per_ray)
            I = np.maximum(counts, 1) / cfg.photons_per_ray
        p = -np.log(np.clip(I, 1e-9, None))
        if cfg.bh_correction:
            p = np.interp(p, p_poly, p_lin)
        rec = iradon(p, theta=theta, filter_name=cfg.fbp_filter, circle=False, output_size=max(Y, X))
        rec = rec[: Y, : X] / pix_cm  # back to 1/cm
        out[zi] = rec
    meta = {"provenance": "synthetic", "simulator": "ctsim-parallel-poly-v1", "ct": cfg.to_dict(),
            "effective_energy_keV": float((E * w).sum()), "seconds": round(time.time() - t0, 1),
            "intensity_unit": "reconstructed mu (1/cm), uncalibrated"}
    return Volume(out * 1000.0, (voxel_um,) * 3, meta=meta)
