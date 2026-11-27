"""Measurement-support (identifiability) advisor.

Question answered: *for this material, this scan and this study design, which endpoints can be
measured, and by what mechanism?*  The answer is computed before a number is reported, so the
software abstains instead of producing a plausible but unidentifiable value.

Mechanisms considered (in order of evidence strength):

1. **Intensity** — graft and new bone occupy distinguishable grey-value ranges. Quantified by the
   Dice-optimal intensity-only oracle: with class-conditional intensity distributions, every
   voxel-wise intensity rule is a union of histogram bins; the Dice-maximising union is a
   superlevel set of the likelihood ratio (exact at the chosen binning). The oracle is an *upper
   bound* for every intensity-only method, so if the oracle fails, every threshold workflow fails.
   The volume ratio (predicted / true graft volume) of that same rule is also returned, because the
   product reports volumes, not Dice.
2. **Day-0 registration** — the graft footprint is known from an implantation-day scan and
   propagated by registration. Valid only if the registration passes QC and the graft does not
   migrate or fragment beyond the tolerance stated in the result.
3. **Morphology/texture** — learned models may use shape cues. In simulation this works only when
   graft morphology differs from new bone (Experiment C2). It is never "supported" without
   material-specific validation evidence recorded in the model card.

Intensity model.  Grey values are expressed in *relative mineral units* r = (x − soft)/(host − soft)
so that soft tissue ≈ 0 and mature host bone ≈ 1 without requiring HA calibration. New bone is a
continuum of maturity (uniform between ``new_bone_rel_range``) and the graft a material-specific
distribution. Both are convolved with the scan's noise and with partial-volume mixing towards soft
tissue for the fraction of voxels at structure surfaces.

All thresholds below are POLICY values (see docs/science/MEASUREMENT_SUPPORT.md); they were set
before Experiment S1 and S1 reports how well they predict actual measurement error.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field

import numpy as np

SUPPORTED = "supported"
CONDITIONAL = "supported_with_conditions"
NOT_SUPPORTED = "not_supported"

# Policy thresholds (pre-registered for Experiment S1)
ORACLE_DICE_MIN = 0.85          # intensity mechanism needs a near-separable oracle
ORACLE_VOLUME_TOL = 0.10        # |predicted/true − 1| of the oracle rule
RADIOLUCENT_REL = 0.15          # material mean below this (relative units) is invisible to micro-CT
MIN_STRUCT_VOXELS = 3.0         # thickness endpoints need structures ≥3 voxels thick
HOST_REL_MATURE = 1.0

# Assumed new-bone maturity range in relative units. Early/mid healing: woven 650–1000 mgHA/cm³ vs
# mature host ≈1075 → (0.60, 0.93) (SCIENTIFIC_EVIDENCE row 4, assumption anchored to a published callus
# threshold). When the timepoint is late or unknown, new bone may have matured to host density, so the
# conservative default extends to 1.0. Best practice: MEASURE it from the study's empty-defect controls.
NEW_BONE_REL_RANGE_EARLY = (0.60, 0.93)
NEW_BONE_REL_RANGE = (0.60, 1.00)

GRAFT_ENDPOINTS = ("residual_graft_volume", "graft_fraction_of_defect", "new_bone_volume",
                   "new_bone_fraction_of_defect")
MINERAL_ENDPOINTS = ("total_mineral_volume", "mineral_fraction_of_defect")


# --------------------------------------------------------------------------- oracle
def dice_oracle_hist(g: np.ndarray, n: np.ndarray, dice_slack: float = 0.02) -> dict:
    """Dice-optimal intensity-only rule given graft (g) and new-bone (n) histograms on shared bins."""
    g = np.asarray(g, float)
    n = np.asarray(n, float)
    G, N = g.sum(), n.sum()
    if G <= 0 or N <= 0:
        return {"dice_graft": float("nan"), "dice_new": float("nan"), "graft_volume_ratio": float("nan"),
                "new_volume_ratio": float("nan")}
    order = np.argsort(-(g / np.maximum(g + n, 1e-12)), kind="stable")
    tp = np.cumsum(g[order])
    pp = np.cumsum((g + n)[order])
    dice = 2 * tp / (pp + G)
    k_best = int(np.argmax(dice))
    # Among rules within `dice_slack` of the optimum, take the one with the smallest graft-volume
    # error: the bound is then on (near-optimal agreement, best achievable volume) jointly.
    near = np.flatnonzero(dice >= dice[k_best] - dice_slack)
    k = int(near[np.argmin(np.abs(pp[near] / G - 1))])
    sel = np.zeros(g.size, bool)
    sel[order[: k + 1]] = True
    pred_new = (g + n)[~sel].sum()
    tn_new = n[~sel].sum()
    return {"_selected_bins": sel, "dice_graft": float(dice[k]), "dice_graft_max": float(dice[k_best]),
            "dice_new": float(2 * tn_new / (pred_new + N)) if (pred_new + N) else float("nan"),
            "graft_volume_ratio": float(pp[k] / G),
            "new_volume_ratio": float(pred_new / N)}


def dice_oracle_samples(graft_vals, new_vals, bins: int = 256) -> dict:
    v = np.concatenate([np.ravel(graft_vals), np.ravel(new_vals)])
    lo, hi = np.percentile(v, [0.1, 99.9])
    if hi <= lo:
        hi = lo + 1e-6
    edges = np.linspace(lo, hi, bins + 1)
    g = np.histogram(np.clip(graft_vals, lo, hi), edges)[0]
    n = np.histogram(np.clip(new_vals, lo, hi), edges)[0]
    r = dice_oracle_hist(g, n)
    sel = r.pop("_selected_bins", None)
    if sel is not None and sel.any():
        # single decision threshold implied by the selected bins (graft side = brighter or darker class)
        brighter = float(np.mean(graft_vals)) >= float(np.mean(new_vals))
        idx = np.flatnonzero(sel)
        r["graft_brighter"] = brighter
        r["threshold"] = float(edges[idx.min()]) if brighter else float(edges[idx.max() + 1])
        r["selection_contiguous"] = bool(idx.max() - idx.min() + 1 == idx.size)
    return r


def dice_oracle_volume(x: np.ndarray, labels: np.ndarray, mask: np.ndarray | None = None, bins=256) -> dict:
    """Oracle on a labelled volume (labels 1 = new bone, 2 = graft)."""
    m = (labels == 1) | (labels == 2)
    if mask is not None:
        m &= mask
    return dice_oracle_samples(x[m & (labels == 2)], x[m & (labels == 1)], bins)


# --------------------------------------------------------------------------- intensity model
@dataclass
class ClassModel:
    """Distribution of a class in relative mineral units before noise."""
    kind: str                 # "uniform" | "normal" | "samples"
    a: float = 0.0            # uniform low / normal mean
    b: float = 0.0            # uniform high / normal sd
    samples: np.ndarray | None = None
    surface_fraction: float = 0.2   # fraction of voxels partially mixed with soft tissue

    def draw(self, n: int, rng: np.random.Generator, neighbors=((0.0, 1.0),)) -> np.ndarray:
        """Draw n values. ``neighbors`` = ((level, weight), ...) of adjacent phases; surface voxels mix
        towards one neighbour with own-class fraction in [0.5, 1] (majority-label truth)."""
        if self.kind == "uniform":
            v = rng.uniform(self.a, self.b, n)
        elif self.kind == "normal":
            v = rng.normal(self.a, self.b, n)
        elif self.kind == "samples":
            v = rng.choice(np.asarray(self.samples, float), n, replace=True)
            return v                                  # measured samples already contain noise & PV
        else:
            raise ValueError(self.kind)
        pv = rng.random(n) < self.surface_fraction
        k = int(pv.sum())
        if k:
            levels = np.array([lv for lv, _ in neighbors], float)
            w = np.array([wt for _, wt in neighbors], float)
            nb = levels[rng.choice(len(levels), k, p=w / w.sum())]
            f = rng.uniform(0.5, 1.0, k)
            v[pv] = f * v[pv] + (1 - f) * nb
        return v


def surface_fraction(struct_size_um: float, voxel_um: float) -> float:
    """Approximate fraction of a structure's voxels that straddle its surface: shell of one voxel
    over a sphere/rod of diameter d → ≈ 1 − ((d − 2v)/d)^3 for spheres, clipped to [0.05, 1]."""
    d = max(struct_size_um, 1e-6)
    inner = max(0.0, (d - 2 * voxel_um) / d)
    return float(np.clip(1 - inner ** 3, 0.05, 1.0))


def intensity_separability(graft: ClassModel, new: ClassModel, noise_rel: float, graft_prior: float = 0.5,
                           n: int = 200_000, seed: int = 0) -> dict:
    rng = np.random.default_rng(seed)
    ng = max(1000, int(n * graft_prior))
    nn = max(1000, n - ng)
    g_level = graft.a if graft.kind == "normal" else float(np.median(graft.samples)) if graft.kind == "samples" else (graft.a + graft.b) / 2
    n_level = (new.a + new.b) / 2 if new.kind == "uniform" else new.a if new.kind == "normal" else float(np.median(new.samples))
    # Contact assumptions (ASSUMPTION, documented in MEASUREMENT_SUPPORT.md): graft surfaces touch soft
    # tissue or new bone (osteoconduction); new-bone surfaces touch soft tissue, graft or host bone.
    g = graft.draw(ng, rng, neighbors=((0.0, 0.6), (n_level, 0.4)))
    v = new.draw(nn, rng, neighbors=((0.0, 0.5), (g_level, 0.2), (HOST_REL_MATURE, 0.3)))
    if graft.kind != "samples":
        g = g + rng.normal(0, noise_rel, g.size)
    if new.kind != "samples":
        v = v + rng.normal(0, noise_rel, v.size)
    r = dice_oracle_samples(g, v)
    r["graft_mean_rel"] = float(np.mean(g))
    r["new_mean_rel"] = float(np.mean(v))
    return r


# --------------------------------------------------------------------------- material profiles
@dataclass
class MaterialProfile:
    id: str
    rel_mean: float                  # expected mean of graft in relative units (host = 1)
    rel_sd: float                    # material heterogeneity (relative units)
    struct_um: float                 # typical granule/strut size
    morphology: str = "granular"     # granular | strut | trabecular_like | paste | membrane | solid
    radiolucent: bool = False
    bone_derived: bool = False       # allograft/xenograft: chemically bone-like
    evidence: str = "ASSUMPTION"
    source: str = ""


def _profiles_from_physics(energy_keV: float = 40.0, host_mgHA: float = 1075.0) -> dict[str, MaterialProfile]:
    from ..phantom.materials import default_materials
    M = default_materials()
    size = {"ha": 500, "beta_tcp": 500, "bcp": 500, "calcium_sulfate": 600, "bioglass_45s5": 400,
            "xenograft_dbbm": 600, "allograft": 800, "dbm": 400, "magnesium": 1000, "titanium": 1000}
    morph = {"xenograft_dbbm": "trabecular_like", "allograft": "trabecular_like", "dbm": "paste",
             "magnesium": "solid", "titanium": "solid"}
    out = {}
    for k in size:
        m = M[k]
        rel = m.ha_equivalent(energy_keV) / host_mgHA
        out[k] = MaterialProfile(
            id=k, rel_mean=float(rel), rel_sd=float(max(0.02, m.heterogeneity_cv * rel)), struct_um=size[k],
            morphology=morph.get(k, "granular"), radiolucent=rel < RADIOLUCENT_REL,
            bone_derived=k in ("allograft", "xenograft_dbbm", "dbm"),
            evidence="PHYSICS+ASSUMPTION",
            source=f"NIST XCOM mixture at {energy_keV} keV; porosity and granule size ASSUMPTION (phantom/materials.py)")
    for k, (rel, sd, s, mo) in {"collagen_sponge": (0.02, 0.02, 100, "membrane"),
                               "plga": (0.05, 0.02, 300, "solid"), "pcl": (0.05, 0.02, 300, "strut")}.items():
        out[k] = MaterialProfile(k, rel, sd, s, mo, radiolucent=True, evidence="ASSUMPTION",
                                 source="polymer/collagen ≈ soft-tissue attenuation")
    return out


def material_profile(material: str | dict | MaterialProfile, energy_keV: float = 40.0) -> MaterialProfile | None:
    if isinstance(material, MaterialProfile):
        return material
    if isinstance(material, dict):
        return MaterialProfile(**material)
    try:
        from ..knowledge import load_materials  # machine-readable knowledge base, when present
        kb = load_materials()
        e = kb.get(material) if isinstance(kb, dict) else None
        if e and e.get("advisor_profile"):
            return MaterialProfile(id=material, **e["advisor_profile"])
    except Exception:
        pass
    return _profiles_from_physics(energy_keV).get(material)


# --------------------------------------------------------------------------- assessment
@dataclass
class EndpointSupport:
    endpoint: str
    status: str
    mechanism: str | None
    reason: str
    conditions: list[str] = field(default_factory=list)


@dataclass
class SupportAssessment:
    material: str
    endpoints: dict
    intensity: dict
    inputs: dict
    policy: dict
    advisor_version: str = "1.0.0"

    def to_dict(self) -> dict:
        d = asdict(self)
        d["endpoints"] = {k: asdict(v) if isinstance(v, EndpointSupport) else v for k, v in self.endpoints.items()}
        return d

    def status(self, endpoint: str) -> str:
        e = self.endpoints.get(endpoint)
        return e.status if e else NOT_SUPPORTED


def assess_support(material, *, noise_rel: float, voxel_um: float, graft_samples_rel=None,
                   new_samples_rel=None, day0: dict | None = None, calibrated: bool = False,
                   no_graft: bool = False, validated_texture_model: bool = False,
                   graft_prior: float = 0.5, energy_keV: float = 40.0, seed: int = 0,
                   new_bone_rel_range: tuple | None = None) -> SupportAssessment:
    """Decide which endpoints can be reported.

    noise_rel          scan noise σ divided by (host − soft) grey contrast.
    graft_samples_rel  optional measured graft intensities (e.g. from a day-0 or material-only scan),
                       relative units; replaces the physics/assumption profile.
    day0               optional {"registered": bool, "qc_pass": bool, "max_displacement_um": float}.
    new_samples_rel    optional measured new-bone intensities (e.g. empty-defect control animals at the
                       same timepoint) — the preferred, data-driven input.
    new_bone_rel_range assumed maturity range when no samples are given (default conservative).
    """
    nb_range = tuple(new_bone_rel_range) if new_bone_rel_range else NEW_BONE_REL_RANGE
    inputs = {"material": material if isinstance(material, str) else getattr(material, "id", "custom"),
              "noise_rel": noise_rel, "voxel_um": voxel_um, "calibrated": calibrated, "no_graft": no_graft,
              "day0": day0, "measured_graft_samples": graft_samples_rel is not None,
              "measured_new_bone_samples": new_samples_rel is not None, "graft_prior": graft_prior}
    policy = {"oracle_dice_min": ORACLE_DICE_MIN, "oracle_volume_tol": ORACLE_VOLUME_TOL,
              "radiolucent_rel": RADIOLUCENT_REL, "min_struct_voxels": MIN_STRUCT_VOXELS,
              "new_bone_rel_range": None}
    policy["new_bone_rel_range"] = nb_range
    ep: dict[str, EndpointSupport] = {}

    # Mineral vs soft tissue: separable when noise is small relative to the bone/soft contrast.
    mineral_ok = noise_rel < 0.35
    for e in MINERAL_ENDPOINTS:
        ep[e] = EndpointSupport(e, SUPPORTED if mineral_ok else NOT_SUPPORTED, "intensity",
                                "mineral/soft-tissue contrast adequate" if mineral_ok else
                                f"noise σ is {noise_rel:.2f} of the bone/soft-tissue contrast (limit 0.35)")
    ep["tissue_mineral_density"] = EndpointSupport(
        "tissue_mineral_density", SUPPORTED if calibrated else NOT_SUPPORTED, "calibration" if calibrated else None,
        "HA phantom calibration recorded" if calibrated else "no HA calibration: grey values are not densities (D-004)")

    if no_graft:
        for e in GRAFT_ENDPOINTS:
            if e.startswith("new_bone"):
                ep[e] = EndpointSupport(e, ep["total_mineral_volume"].status, "no_graft_design",
                                        "no graft implanted: all mineral in the defect is new bone")
            else:
                ep[e] = EndpointSupport(e, NOT_SUPPORTED, None, "no graft implanted")
        return SupportAssessment(inputs["material"], ep, {}, inputs, policy)

    prof = material_profile(material, energy_keV)
    intensity = {}
    if prof is None and graft_samples_rel is None:
        reason = (f"material '{material}' is not in the knowledge base: characterise it first "
                  "(scan of the material alone or a day-0 scan), see unsupported-material workflow")
        for e in GRAFT_ENDPOINTS:
            ep[e] = EndpointSupport(e, NOT_SUPPORTED, None, reason)
        return SupportAssessment(inputs["material"], ep, intensity, inputs, policy)

    if prof is not None and prof.radiolucent and graft_samples_rel is None:
        for e in GRAFT_ENDPOINTS:
            if e.startswith("new_bone"):
                ep[e] = EndpointSupport(e, CONDITIONAL, "radiolucent_graft",
                                        f"{prof.id} is near soft-tissue attenuation: mineral in the defect is "
                                        "attributed to new bone", ["graft contains no mineral phase",
                                                                   "no mineralised debris from other sources"])
            else:
                ep[e] = EndpointSupport(e, NOT_SUPPORTED, None,
                                        f"{prof.id} is radiolucent (mean ≈{prof.rel_mean:.2f} of host bone): "
                                        "residual graft is not visible on micro-CT; use histology")
        return SupportAssessment(inputs["material"], ep, intensity, inputs, policy)

    # --- intensity mechanism
    if graft_samples_rel is not None:
        gm = ClassModel("samples", samples=np.asarray(graft_samples_rel, float))
    else:
        gm = ClassModel("normal", prof.rel_mean, prof.rel_sd,
                        surface_fraction=surface_fraction(prof.struct_um, voxel_um))
    if new_samples_rel is not None:
        nm = ClassModel("samples", samples=np.asarray(new_samples_rel, float))
    else:
        nm = ClassModel("uniform", *nb_range, surface_fraction=surface_fraction(150.0, voxel_um))
    intensity = intensity_separability(gm, nm, noise_rel, graft_prior=graft_prior, seed=seed)
    vol_err = abs(intensity["graft_volume_ratio"] - 1)
    intensity_ok = intensity["dice_graft"] >= ORACLE_DICE_MIN and vol_err <= ORACLE_VOLUME_TOL
    bone_like = prof is not None and prof.bone_derived
    if bone_like:
        # bone-derived grafts remodel and converge to bone intensity; an apparent separation at one
        # timepoint is not accepted as identifiability (SCIENTIFIC_EVIDENCE row 5)
        intensity_ok = False
        intensity["bone_derived_rule"] = True
    intensity["passes_policy"] = bool(intensity_ok)

    day0_ok = bool(day0 and day0.get("registered") and day0.get("qc_pass"))
    for e in GRAFT_ENDPOINTS:
        if intensity_ok:
            ep[e] = EndpointSupport(e, SUPPORTED, "intensity",
                                    f"intensity oracle graft Dice {intensity['dice_graft']:.2f}, "
                                    f"volume ratio {intensity['graft_volume_ratio']:.2f}")
        elif day0_ok:
            conds = ["graft footprint propagated from a registered day-0 scan",
                     f"assumes graft displacement ≤ {day0.get('tolerance_um', 200)} µm after implantation",
                     "registration quality checks passed"]
            if day0.get("untracked_fraction", 0.0) > day0.get("max_untracked_fraction", 0.2):
                ep[e] = EndpointSupport(e, NOT_SUPPORTED, None,
                                        f"{day0['untracked_fraction']:.0%} of the day-0 graft could not be tracked "
                                        "(fragmentation, overgrowth or heavy resorption)")
            elif day0.get("max_displacement_um") is not None and day0["max_displacement_um"] > day0.get("tolerance_um", 200):
                ep[e] = EndpointSupport(e, NOT_SUPPORTED, None,
                                        f"graft displacement {day0['max_displacement_um']:.0f} µm exceeds tolerance")
            else:
                ep[e] = EndpointSupport(e, CONDITIONAL, "day0_registration",
                                        f"intensity alone insufficient (oracle Dice {intensity['dice_graft']:.2f}); "
                                        "day-0 footprint used", conds)
        elif validated_texture_model and not bone_like:
            ep[e] = EndpointSupport(e, CONDITIONAL, "validated_texture_model",
                                    "material-specific model with recorded validation evidence",
                                    ["model validated for this material, scanner class and voxel size"])
        else:
            why = (f"intensity-only separation insufficient (oracle graft Dice {intensity['dice_graft']:.2f} "
                   f"< {ORACLE_DICE_MIN} or volume ratio {intensity['graft_volume_ratio']:.2f} outside "
                   f"±{ORACLE_VOLUME_TOL:.0%})")
            if bone_like:
                why += "; graft is bone-derived, so texture cues are not expected to separate it"
            why += ". Report total mineral; add a day-0 scan or histology to separate graft from new bone"
            ep[e] = EndpointSupport(e, NOT_SUPPORTED, None, why)

    # Thickness-type morphometry on new bone needs resolvable structures
    min_struct = 150.0 / max(voxel_um, 1e-6)
    ep["new_bone_thickness"] = EndpointSupport(
        "new_bone_thickness",
        CONDITIONAL if min_struct >= MIN_STRUCT_VOXELS and ep["new_bone_volume"].status != NOT_SUPPORTED else NOT_SUPPORTED,
        "local_thickness",
        f"typical woven-bone trabeculae ≈150 µm = {min_struct:.1f} voxels",
        ["depends on new-bone segmentation support", "border convention stated in report"])
    return SupportAssessment(inputs["material"], ep, intensity, inputs, policy)


def scan_relative_units(image: np.ndarray, host_mask: np.ndarray | None = None,
                        soft_mask: np.ndarray | None = None, exclude_mask: np.ndarray | None = None,
                        margin_vox: int = 3) -> dict:
    """Estimate (soft, host, noise) grey levels from a scan for relative-unit conversion.

    Uses provided masks when available; otherwise an Otsu split of robust values outside the defect
    (soft tissue vs host bone) and a MAD noise estimate from the soft-tissue class. MAD of the soft class
    includes genuine soft-tissue texture, so the noise estimate is conservative (an over-estimate).
    """
    from ..segment.classical import robust_values
    from scipy import ndimage as ndi
    from skimage.filters import threshold_otsu
    if exclude_mask is not None:
        # estimate host/soft levels away from the defect (graft would otherwise be taken as "host")
        keep = ~ndi.binary_dilation(exclude_mask, iterations=margin_vox)
        v = robust_values(image[keep])
    else:
        v = robust_values(image)
    if soft_mask is not None and host_mask is not None:
        soft = float(np.median(image[soft_mask]))
        host = float(np.median(image[host_mask]))
        s = image[soft_mask]
    else:
        t = float(threshold_otsu(v))
        soft = float(np.median(v[v < t]))
        hi = v[v >= t]
        # host level: median of the upper half of mineral voxels (excludes partial-volume edges)
        host = float(np.median(hi[hi >= np.median(hi)])) if hi.size else float(v.max())
        s = v[v < t]
    noise = float(1.4826 * np.median(np.abs(s - np.median(s))))
    contrast = max(host - soft, 1e-6)
    return {"soft": soft, "host": host, "noise_sigma": noise, "noise_rel": noise / contrast,
            "method": "masks" if host_mask is not None else "otsu_outside_defect" if exclude_mask is not None else "otsu"}


def to_relative(x, soft: float, host: float):
    return (np.asarray(x, np.float32) - soft) / max(host - soft, 1e-6)
