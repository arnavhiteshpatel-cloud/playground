"""Material characterisation: turn a scan of a graft material into a measured advisor profile.

Inputs (one of):
* a scan of the material alone in a holder with fluid/agarose plus a reference bone sample in the same field of view
  (preferred for a new material), or
* a day-0 (implantation-day) scan of an animal: graft voxels are the mineral inside the defect ROI, host bone
  outside it provides the relative-unit anchor.

Output: a ``MaterialCharacterisation`` with the material's intensity distribution in relative units
r = (x − soft)/(host − soft), granule/strut thickness distribution (local thickness, µm), porosity proxy, and the
measured samples that ``assess_support(..., graft_samples_rel=...)`` consumes. The record carries the scan hash,
voxel size and acquisition fields so that it is only reused for compatible protocols (same scanner class, energy,
voxel size within ±25%).
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field

import numpy as np
from scipy import ndimage as ndi

from .separability import MIN_REFERENCE_SAMPLES, MaterialProfile, to_relative


@dataclass
class MaterialCharacterisation:
    material_id: str
    source: str                         # "material_only" | "day0"
    scan_sha256: str
    voxel_um: float
    acquisition: dict
    soft_level: float
    host_level: float
    rel_mean: float
    rel_sd: float
    rel_percentiles: dict
    thickness_um_median: float
    thickness_um_p10_p90: tuple
    n_voxels: int
    samples_rel: list = field(repr=False, default_factory=list)
    warnings: list = field(default_factory=list)
    version: str = "1.0.0"

    def profile(self) -> MaterialProfile:
        return MaterialProfile(id=self.material_id, rel_mean=self.rel_mean, rel_sd=self.rel_sd,
                               struct_um=self.thickness_um_median, morphology="granular",
                               radiolucent=self.rel_mean < 0.15, bone_derived=False,
                               evidence="MEASURED", source=f"characterisation of scan {self.scan_sha256[:12]}")

    def compatible_with(self, voxel_um: float, acquisition: dict | None = None) -> tuple[bool, str]:
        if abs(voxel_um - self.voxel_um) > 0.25 * self.voxel_um:
            return False, f"voxel size {voxel_um:.1f} µm differs from characterisation ({self.voxel_um:.1f} µm) by >25%"
        acq = acquisition or {}
        for k in ("kvp", "filter", "scanner_model"):
            if k in acq and k in self.acquisition and acq[k] != self.acquisition[k]:
                return False, f"acquisition '{k}' differs ({acq[k]} vs {self.acquisition[k]})"
        return True, "compatible"

    def to_json(self) -> str:
        d = asdict(self)
        return json.dumps(d, default=float)


def _levels(image, soft_mask, host_mask):
    s = image[soft_mask]
    h = image[host_mask]
    if s.size < 100 or h.size < 100:
        raise ValueError("characterisation needs ≥100 voxels of soft tissue/fluid and of reference bone")
    return float(np.median(s)), float(np.median(h))


def characterise_material(image: np.ndarray, material_mask: np.ndarray, soft_mask: np.ndarray,
                          host_mask: np.ndarray, voxel_um: float, material_id: str, source: str = "material_only",
                          acquisition: dict | None = None, max_samples: int = 50_000,
                          seed: int = 0) -> MaterialCharacterisation:
    """Measure a material's appearance. Masks define the material, fluid/soft tissue and reference bone."""
    from ..morphometry import local_thickness
    if material_mask.sum() < MIN_REFERENCE_SAMPLES:
        raise ValueError(f"material mask has {int(material_mask.sum())} voxels; need ≥{MIN_REFERENCE_SAMPLES}")
    soft, host = _levels(image, soft_mask, host_mask)
    if host - soft <= 0:
        raise ValueError("reference bone is not brighter than soft tissue/fluid")
    warnings = []
    # interior voxels only for the intensity distribution (partial volume handled by the advisor's model)
    interior = ndi.binary_erosion(material_mask, iterations=1)
    if interior.sum() < MIN_REFERENCE_SAMPLES:
        warnings.append("few interior voxels: material structures are ≤2 voxels thick; distribution includes partial volume")
        interior = material_mask
    rel = to_relative(image[interior], soft, host)
    rng = np.random.default_rng(seed)
    samples = rng.choice(rel, min(max_samples, rel.size), replace=False)
    th = local_thickness(material_mask, float(voxel_um)) if material_mask.any() else np.zeros(1)
    tv = th[material_mask] if th.shape == material_mask.shape else np.asarray(th).ravel()
    tv = tv[tv > 0]
    if tv.size == 0:
        tv = np.array([voxel_um])
    if float(np.median(tv)) < 3 * voxel_um:
        warnings.append("median structure thickness < 3 voxels: intensity is partial-volume dominated; "
                        "re-scan at smaller voxel size for a reliable profile")
    if rel.std() > 0.35 * max(abs(rel.mean()), 1e-6):
        warnings.append("heterogeneous material intensity (CV > 35%): check for mixed materials or beam hardening")
    h = hashlib.sha256(np.ascontiguousarray(image).tobytes()).hexdigest()
    return MaterialCharacterisation(
        material_id=material_id, source=source, scan_sha256=h, voxel_um=float(voxel_um),
        acquisition=dict(acquisition or {}), soft_level=soft, host_level=host,
        rel_mean=float(rel.mean()), rel_sd=float(rel.std()),
        rel_percentiles={str(q): float(np.percentile(rel, q)) for q in (1, 5, 25, 50, 75, 95, 99)},
        thickness_um_median=float(np.median(tv)),
        thickness_um_p10_p90=(float(np.percentile(tv, 10)), float(np.percentile(tv, 90))),
        n_voxels=int(material_mask.sum()), samples_rel=[float(x) for x in samples], warnings=warnings)


def characterise_from_day0(day0_image: np.ndarray, roi_mask: np.ndarray, voxel_um: float, material_id: str,
                           acquisition: dict | None = None) -> MaterialCharacterisation:
    """Day-0 scan: graft = mineral inside the ROI (no new bone yet); host = mineral outside; soft = non-mineral outside."""
    from ..segment.classical import threshold_otsu, robust_values
    keep_out = ~ndi.binary_dilation(roi_mask, iterations=3)
    v = robust_values(day0_image[keep_out])
    from skimage.filters import threshold_otsu as _otsu
    t = float(_otsu(v))
    mineral_out = (day0_image > t) & keep_out
    soft = (day0_image <= t) & keep_out
    host = ndi.binary_erosion(mineral_out, iterations=1)
    graft = ndi.binary_opening((day0_image > t) & roi_mask, iterations=1)
    return characterise_material(day0_image, graft, soft, host, voxel_um, material_id, "day0", acquisition)
