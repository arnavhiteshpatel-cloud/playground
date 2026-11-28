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
MIN_REFERENCE_SAMPLES = 500     # measured reference distributions need at least this many voxels
MIN_GRAFT_FRACTION = 0.05       # below this share of mineral, relative graft-volume error is unbounded
ADVISOR_VERSION = "1.4.0"
PROFILE_SCAN_MISMATCH_TOL = 0.15   # observed bright-mode vs profile graft level (relative)
RIM_TOL = 0.10                     # ≥1.4.0: max ambiguous graft-rim share of new bone / half-rim share of mineral
# Resorbable materials whose granules become microporous/fragmented and enter the bone intensity range as they
# resorb (knowledge base: beta-TCP almost fully resorbed by 8 weeks in minipig; CaSO4 and glasses similar or faster).
RESORBABLE_EARLY_ONLY = {"beta_tcp", "calcium_sulfate", "bioglass_45s5", "s53p4", "polymer_ceramic_composite"}
EARLY_WEEKS_MAX = 4.0
# Changelog: 1.0.x (pre-review, used by S1/S1b runs before cycle-1 review) → 1.1.0: decision uses the single-
# threshold rule actually applied (union oracle kept as upper bound); support must hold at the estimated graft
# share and at half of it (review IMG-01); metals refused (IMG-02); measured samples need ≥500 voxels and cannot
# bypass the bone-derived rule (IMG-03); day-0 support requires computed QC/tracking fields (IMG-04).
# 1.2.0: new-bone vs soft-tissue decision with partial-volume halos of dense phases gates new-bone and mineral
# endpoints and sets the mineral threshold (S1b re-run finding; review STAT-05).
# 1.2.1: DBM (radiolucent but bone-derived) new-bone endpoints not supported (review BIO-02).
# 1.3.0: knowledge-base material profiles (verified references); KB/physics disagreement >25% requires a measured
# material reference; resorbable materials are intensity-supported only at known timepoints ≤4 weeks.
# 1.3.1: scan-vs-profile consistency check — if the scan's observed graft-like bright mode deviates >15% from the
# profile level, support requires a measured reference (S1b 1.3.0: BCP profile 1.73 vs scan 1.43 → −42…−49% errors).
# 1.3.2: measured new-bone references (empty-defect controls) get graft-adjacent partial-volume mixing (S1c: control
# new bone is dimmer than new bone next to dense graft; threshold too low → graft +24%).
# 1.3.3: bone-derived grafts are not supported by the day-0 mechanism either (remodelling).
# 1.4.0: scan-measured imaging: blur σ from host-bone edges (edge-spread fit, conservative calibration), graft granule
# thickness (local thickness) and deep graft level replace assumed values in a blur-aware partial-volume model of the
# GRAFT; measured halo composition; new-bone/mineral partial volume unchanged from 1.3.3
# (S1H held-out failure: wider PSF + small granules → graft −21…−28%, new bone +20…+50% while supported); new-bone
# endpoints gated by propagation of graft-volume error (new bone = mineral − graft).

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


def dice_oracle_samples(graft_vals, new_vals, bins: int = 256, dice_slack: float = 0.02) -> dict:
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
        idx = np.flatnonzero(sel)
        r["selection_contiguous"] = bool(idx.max() - idx.min() + 1 == idx.size)
    # Best SINGLE threshold (what an intensity method can actually apply). The bin-union oracle may select
    # non-contiguous bins (e.g. partial-volume graft voxels below the new-bone range), so its extreme selected
    # bin is not a usable threshold (Experiment S1c defect). Scan contiguous cuts on the graft side.
    brighter = float(np.median(graft_vals)) >= float(np.median(new_vals))
    G = g.sum()
    if G > 0:
        gc = np.cumsum(g[::-1])[::-1] if brighter else np.cumsum(g)       # graft voxels selected by cut k
        pc = np.cumsum((g + n)[::-1])[::-1] if brighter else np.cumsum(g + n)
        dice_t = 2 * gc / (pc + G)
        kb = int(np.argmax(dice_t))
        near = np.flatnonzero(dice_t >= dice_t[kb] - dice_slack)
        k = int(near[np.argmin(np.abs(pc[near] / G - 1))])
        r["graft_brighter"] = brighter
        r["threshold"] = float(edges[k]) if brighter else float(edges[k + 1])
        r["dice_graft_threshold_rule"] = float(dice_t[k])
        r["graft_volume_ratio_threshold_rule"] = float(pc[k] / G)
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
    blur_sigma_vox: float | None = None   # ≥1.4.0: measured total blur; with thickness_vox enables the blur model
    thickness_vox: float | None = None

    def draw(self, n: int, rng: np.random.Generator, neighbors=((0.0, 1.0),)) -> np.ndarray:
        """Draw n values. ``neighbors`` = ((level, weight), ...) of adjacent phases; surface voxels mix
        towards one neighbour with own-class fraction in [0.5, 1] (majority-label truth)."""
        if self.kind == "uniform":
            v = rng.uniform(self.a, self.b, n)
        elif self.kind == "normal":
            v = rng.normal(self.a, self.b, n)
        elif self.kind == "samples":
            # measured samples already contain noise and their own partial volume; they do NOT contain mixing with
            # neighbours absent from the reference scan (e.g. dense graft next to new bone when the reference comes
            # from empty-defect controls — Experiment S1c). ``surface_fraction`` > 0 adds that mixing.
            v = rng.choice(np.asarray(self.samples, float), n, replace=True)
            if self.surface_fraction <= 0:
                return v
        else:
            raise ValueError(self.kind)
        if self.blur_sigma_vox and self.thickness_vox:
            pv = rng.random(n) < blur_surface_fraction(self.thickness_vox, self.blur_sigma_vox)
        else:
            pv = rng.random(n) < self.surface_fraction
        k = int(pv.sum())
        if k:
            levels = np.array([lv for lv, _ in neighbors], float)
            w = np.array([wt for _, wt in neighbors], float)
            nb = levels[rng.choice(len(levels), k, p=w / w.sum())]
            if self.blur_sigma_vox and self.thickness_vox:
                f = blur_own_fraction(k, rng, self.blur_sigma_vox, self.thickness_vox)
            else:
                f = rng.uniform(0.5, 1.0, k)
            v[pv] = f * v[pv] + (1 - f) * nb
        return v


def surface_fraction(struct_size_um: float, voxel_um: float) -> float:
    """Approximate fraction of a structure's voxels that straddle its surface: shell of one voxel
    over a sphere/rod of diameter d → ≈ 1 − ((d − 2v)/d)^3 for spheres, clipped to [0.05, 1]."""
    d = max(struct_size_um, 1e-6)
    inner = max(0.0, (d - 2 * voxel_um) / d)
    return float(np.clip(1 - inner ** 3, 0.05, 1.0))


def _blur_shell(sigma_vox: float) -> float:
    return max(0.5, 2.0 * sigma_vox)


def blur_surface_fraction(thickness_vox: float, sigma_vox: float) -> float:
    """Fraction of a structure's voxels within the blur shell (2σ, ≥0.5 voxel) of its surface (sphere-like)."""
    T, sh = max(thickness_vox, 1e-6), _blur_shell(sigma_vox)
    if T <= 2 * sh:
        return 1.0
    return float(1 - ((T - 2 * sh) / T) ** 3)


def blur_own_fraction(k: int, rng: np.random.Generator, sigma_vox: float, thickness_vox: float) -> np.ndarray:
    """Effective own-class fraction of surface-shell voxels of a structure of thickness T blurred by σ (voxels):
    a voxel centred at depth δ inside sees Φ(δ/σ) + Φ((T−δ)/σ) − 1 of its own class (planar two-sided edge model).
    Calibrated against phantoms in the 1.4.0 development notes (Experiment S1H diagnosis)."""
    from scipy.special import ndtr
    T, sh = max(thickness_vox, 1e-6), _blur_shell(sigma_vox)
    d = rng.uniform(0.0, min(sh, T / 2), k)
    return np.clip(ndtr(d / sigma_vox) + ndtr((T - d) / sigma_vox) - 1.0, 0.0, 1.0)


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
    v = new.draw(nn, rng, neighbors=((g_level, 1.0),) if new.kind == "samples"
                 else ((0.0, 0.5), (g_level, 0.2), (HOST_REL_MATURE, 0.3)))
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
    uncertain: bool = False          # knowledge base and physics model disagree (>25%): measure the material


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
    out["autograft"] = MaterialProfile("autograft", 1.0, 0.06, 800, "trabecular_like", radiolucent=False,
                                       bone_derived=True, evidence="ASSUMPTION", source="autologous bone ≈ host bone")
    for k in ("magnesium", "titanium"):
        out[k].morphology = "metal"
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
    phys = _profiles_from_physics(energy_keV).get(material)
    try:
        from ..knowledge import load_materials  # machine-readable knowledge base (verified references)
        kb = load_materials()
        e = kb.get(material) if isinstance(kb, dict) else None
        if e and e.get("advisor_profile"):
            ap = {k: v for k, v in e["advisor_profile"].items() if k in MaterialProfile.__dataclass_fields__}
            prof = MaterialProfile(id=material, **ap)
            if phys is not None and not prof.radiolucent and phys.rel_mean > 0:
                rel_diff = abs(prof.rel_mean - phys.rel_mean) / phys.rel_mean
                if rel_diff > 0.25:
                    prof.uncertain = True
                    prof.source += (f" | physics model (NIST, assumed porosity) gives {phys.rel_mean:.2f} vs knowledge "
                                    f"base {prof.rel_mean:.2f}: profile uncertain")
            return prof
    except Exception:
        pass
    return phys


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
    advisor_version: str = ADVISOR_VERSION

    def to_dict(self) -> dict:
        d = asdict(self)
        d["endpoints"] = {k: asdict(v) if isinstance(v, EndpointSupport) else v for k, v in self.endpoints.items()}
        return d

    def status(self, endpoint: str) -> str:
        e = self.endpoints.get(endpoint)
        return e.status if e else NOT_SUPPORTED


def _thickness_endpoint(ep: dict, voxel_um: float) -> None:
    min_struct = 150.0 / max(voxel_um, 1e-6)
    nb = ep.get("new_bone_volume")
    ok = min_struct >= MIN_STRUCT_VOXELS and nb is not None and nb.status != NOT_SUPPORTED
    ep["new_bone_thickness"] = EndpointSupport(
        "new_bone_thickness", CONDITIONAL if ok else NOT_SUPPORTED, "local_thickness",
        f"typical woven-bone trabeculae ≈150 µm = {min_struct:.1f} voxels",
        ["depends on new-bone segmentation support", "border convention stated in report"])


def _assess_core(material, *, noise_rel: float, voxel_um: float, graft_samples_rel=None,
                   new_samples_rel=None, day0: dict | None = None, calibrated: bool = False,
                   no_graft: bool = False, validated_texture_model: bool = False,
                   graft_prior: float = 0.5, energy_keV: float = 40.0, seed: int = 0,
                   new_bone_rel_range: tuple | None = None, healing_weeks: float | None = None,
                   observed_graft_level: float | None = None, blur_sigma_vox: float | None = None,
                   graft_struct_um: float | None = None, graft_level_deep: float | None = None,
                   halo_graft_fraction: float | None = None, rim_fraction_new: float | None = None,
                   rim_fraction_mineral: float | None = None) -> SupportAssessment:
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
        _thickness_endpoint(ep, voxel_um)
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
            if e.startswith("new_bone") and prof.bone_derived:
                # DBM: demineralised bone matrix can retain residual mineral or remineralise; mineralised DBM
                # particles are indistinguishable from new bone (cycle-1 review BIO-02)
                ep[e] = EndpointSupport(e, NOT_SUPPORTED, None,
                                        f"{prof.id} is bone-derived: residual or re-mineralised matrix cannot be "
                                        "distinguished from new bone on micro-CT; use histology")
            elif e.startswith("new_bone"):
                ep[e] = EndpointSupport(e, CONDITIONAL, "radiolucent_graft",
                                        f"{prof.id} is near soft-tissue attenuation: mineral in the defect is "
                                        "attributed to new bone", ["graft contains no mineral phase",
                                                                   "no mineralised debris from other sources"])
            else:
                ep[e] = EndpointSupport(e, NOT_SUPPORTED, None,
                                        f"{prof.id} is radiolucent (mean ≈{prof.rel_mean:.2f} of host bone): "
                                        "residual graft is not visible on micro-CT; use histology")
        _thickness_endpoint(ep, voxel_um)
        return SupportAssessment(inputs["material"], ep, intensity, inputs, policy)

    # --- metals: streak/beam-hardening artefacts are not modelled → never supported (review IMG-02)
    if prof is not None and prof.morphology == "metal":
        for e in GRAFT_ENDPOINTS:
            ep[e] = EndpointSupport(e, NOT_SUPPORTED, None,
                                    f"{prof.id} is metallic: streak and beam-hardening artefacts are not modelled; use a "
                                    "metal-artefact-reduction protocol and material-specific validation")
        return SupportAssessment(inputs["material"], ep, intensity, inputs, policy)

    # --- measured reference samples must be large enough (review IMG-03)
    notes = []
    if graft_samples_rel is not None and np.size(graft_samples_rel) < MIN_REFERENCE_SAMPLES:
        notes.append(f"graft reference ignored: {np.size(graft_samples_rel)} < {MIN_REFERENCE_SAMPLES} voxels")
        graft_samples_rel = None
    if new_samples_rel is not None and np.size(new_samples_rel) < MIN_REFERENCE_SAMPLES:
        notes.append(f"new-bone reference ignored: {np.size(new_samples_rel)} < {MIN_REFERENCE_SAMPLES} voxels")
        new_samples_rel = None
    if prof is None and graft_samples_rel is None:
        for e in GRAFT_ENDPOINTS:
            ep[e] = EndpointSupport(e, NOT_SUPPORTED, None, "; ".join(notes) or "no material model")
        return SupportAssessment(inputs["material"], ep, intensity, inputs, policy)

    # --- intensity mechanism
    if graft_samples_rel is not None:
        gm = ClassModel("samples", samples=np.asarray(graft_samples_rel, float), surface_fraction=0.0)
    else:
        # ≥1.4.0: the scan's own deep graft-like level (if consistent with the profile, checked below) and measured
        # granule thickness replace the profile's assumed values; blur from the scan drives partial volume
        level = prof.rel_mean
        if graft_level_deep is not None and prof.rel_mean > HOST_REL_MATURE and \
                abs(graft_level_deep - prof.rel_mean) / prof.rel_mean <= PROFILE_SCAN_MISMATCH_TOL:
            level = graft_level_deep
        struct = graft_struct_um if graft_struct_um else prof.struct_um
        gm = ClassModel("normal", level, prof.rel_sd * level / max(prof.rel_mean, 1e-6),
                        surface_fraction=surface_fraction(struct, voxel_um),
                        blur_sigma_vox=blur_sigma_vox, thickness_vox=struct / max(voxel_um, 1e-6) if blur_sigma_vox else None)
    if new_samples_rel is not None:
        # control-derived new bone lacks graft-adjacent blur: add it (S1c; advisor 1.3.2)
        nm = ClassModel("samples", samples=np.asarray(new_samples_rel, float), surface_fraction=0.2)
    else:
        # new-bone partial volume stays on the voxel-shell model: its trabecular thickness is not measured, and an
        # assumed-thickness blur model biased the mineral boundary in development (1.4.0 notes)
        nm = ClassModel("uniform", *nb_range, surface_fraction=surface_fraction(150.0, voxel_um))
    # Support must hold at the graft share expected in THIS scan and at half of it: the volume error of a
    # threshold rule grows as residual graft becomes scarce (review IMG-01).
    priors = sorted({float(np.clip(graft_prior, 0.01, 0.95)), float(np.clip(graft_prior / 2, 0.01, 0.95))})
    evals = {pr: intensity_separability(gm, nm, noise_rel, graft_prior=pr, seed=seed) for pr in priors}
    intensity = dict(evals[max(priors)])
    intensity["by_prior"] = {f"{pr:.3f}": {k: v for k, v in r.items() if k in (
        "dice_graft", "dice_graft_threshold_rule", "graft_volume_ratio_threshold_rule", "threshold")}
        for pr, r in evals.items()}
    intensity["notes"] = notes

    def _passes(r):
        d = r.get("dice_graft_threshold_rule", r["dice_graft"])
        v = r.get("graft_volume_ratio_threshold_rule", r["graft_volume_ratio"])
        return d >= ORACLE_DICE_MIN and abs(v - 1) <= ORACLE_VOLUME_TOL
    intensity_ok = all(_passes(r) for r in evals.values())
    scarce = graft_prior < MIN_GRAFT_FRACTION
    bone_like = prof is not None and prof.bone_derived
    if bone_like:
        # bone-derived grafts remodel and converge to bone intensity; an apparent separation at one timepoint —
        # including one computed from measured samples — is not accepted as identifiability (row 5; IMG-03)
        intensity_ok = False
        intensity["bone_derived_rule"] = True
    if prof is not None and prof.uncertain and graft_samples_rel is None:
        intensity_ok = False
        intensity["uncertain_profile_rule"] = prof.source
    obs_level = graft_level_deep if graft_level_deep is not None else observed_graft_level
    if (prof is not None and graft_samples_rel is None and obs_level is not None
            and prof.rel_mean > HOST_REL_MATURE):
        observed_graft_level = obs_level
        mism = abs(obs_level - prof.rel_mean) / prof.rel_mean
        intensity["profile_scan_mismatch"] = float(mism)
        if mism > PROFILE_SCAN_MISMATCH_TOL:
            intensity_ok = False
            intensity["uncertain_profile_rule"] = (f"the scan's graft-like intensities (median {observed_graft_level:.2f} "
                                                   f"of host) differ from the material profile ({prof.rel_mean:.2f}) by "
                                                   f"{mism:.0%}: profile mismatch for this scanner/protocol")
    if prof is not None and prof.id in RESORBABLE_EARLY_ONLY and \
            (healing_weeks is None or healing_weeks > EARLY_WEEKS_MAX):
        intensity_ok = False
        intensity["resorbable_timepoint_rule"] = (
            f"{prof.id} resorbs into the bone intensity range; intensity separation accepted only at known timepoints "
            f"≤{EARLY_WEEKS_MAX:.0f} weeks (timepoint: {'unknown' if healing_weeks is None else f'{healing_weeks:g} weeks'})")
    intensity["passes_policy"] = bool(intensity_ok)

    required = ("registered", "qc_pass", "untracked_fraction", "max_displacement_um")
    day0_complete = bool(day0) and all(k in day0 and day0[k] is not None for k in required)
    day0_ok = day0_complete and bool(day0.get("registered") and day0.get("qc_pass"))
    resorbable = prof is not None and prof.id in ("calcium_sulfate", "beta_tcp", "bioglass_45s5", "s53p4", "dbm")
    for e in GRAFT_ENDPOINTS:
        rule = intensity.get("dice_graft_threshold_rule", intensity["dice_graft"])
        if intensity_ok and not (scarce and e.startswith(("residual_graft", "graft_fraction"))):
            ep[e] = EndpointSupport(e, SUPPORTED, "intensity",
                                    f"threshold-rule graft Dice {rule:.2f} at graft share {priors[-1]:.2f} and "
                                    f"{priors[0]:.2f}; volume ratio within ±{ORACLE_VOLUME_TOL:.0%}")
        elif intensity_ok and scarce:
            ep[e] = EndpointSupport(e, NOT_SUPPORTED, None,
                                    f"residual graft is scarce (≈{graft_prior:.0%} of mineral): relative graft-volume "
                                    "error is unbounded; report as 'trace residual graft'")
        elif day0_ok and bone_like:
            # bone-derived grafts (autograft, allograft, DBBM, DBM) are remodelled into bone: bone inside the day-0
            # footprint cannot be attributed to residual graft (cycle-2 review C2-BIZ biology finding; 1.3.3)
            ep[e] = EndpointSupport(e, NOT_SUPPORTED, None,
                                    "graft is bone-derived: the day-0 footprint becomes remodelled bone, so residual "
                                    "graft cannot be separated from new bone by registration either; use histology")
        elif day0 and not day0_complete:
            ep[e] = EndpointSupport(e, NOT_SUPPORTED, None,
                                    "day-0 assessment incomplete: registration QC and granule tracking must be computed "
                                    f"({', '.join(k for k in required if day0.get(k) is None)} missing)")
        elif day0_ok:
            conds = ["graft footprint propagated from a registered day-0 scan",
                     f"granule motion ≤ {day0.get('tolerance_um', 200)} µm or tracked",
                     "registration quality checks passed"]
            if resorbable:
                conds.append("bone formed inside the original graft footprint (creeping substitution) is counted as "
                             "graft: residual graft is over-estimated for resorbable materials")
            if day0["untracked_fraction"] > day0.get("max_untracked_fraction", 0.2):
                ep[e] = EndpointSupport(e, NOT_SUPPORTED, None,
                                        f"{day0['untracked_fraction']:.0%} of the day-0 graft could not be tracked "
                                        "(fragmentation, overgrowth or heavy resorption)")
            elif day0["max_displacement_um"] > day0.get("tolerance_um", 200):
                ep[e] = EndpointSupport(e, NOT_SUPPORTED, None,
                                        f"graft displacement {day0['max_displacement_um']:.0f} µm exceeds tolerance")
            else:
                ep[e] = EndpointSupport(e, CONDITIONAL, "day0_registration",
                                        f"intensity alone insufficient (threshold-rule Dice {rule:.2f}); "
                                        "day-0 footprint used", conds)
        elif validated_texture_model and not bone_like:
            ep[e] = EndpointSupport(e, CONDITIONAL, "validated_texture_model",
                                    "material-specific model with recorded validation evidence",
                                    ["model validated for this material, scanner class and voxel size"])
        else:
            why = (f"intensity-only separation insufficient (threshold-rule graft Dice {rule:.2f}; requirement "
                   f"≥{ORACLE_DICE_MIN} and volume within ±{ORACLE_VOLUME_TOL:.0%} at graft share "
                   f"{priors[-1]:.2f} and {priors[0]:.2f})")
            extra = []
            if intensity.get("resorbable_timepoint_rule"):
                extra.append(intensity["resorbable_timepoint_rule"])
            if intensity.get("uncertain_profile_rule"):
                extra.append("material appearance is uncertain (" + intensity["uncertain_profile_rule"].split(" | ")[-1]
                             + "); measure it with a material-only or day-0 scan")
            if extra:
                why = "; ".join(extra)
            if bone_like:
                why = "graft is bone-derived and remodels towards bone intensity, so neither intensity nor texture separates it"
            why += ". Report total mineral; add a day-0 scan or histology to separate graft from new bone"
            ep[e] = EndpointSupport(e, NOT_SUPPORTED, None, why)

    # Thickness-type morphometry on new bone needs resolvable structures
    _thickness_endpoint(ep, voxel_um)
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


def mineral_rule(material, *, noise_rel: float, voxel_um: float, graft_samples_rel=None, new_samples_rel=None,
                 new_bone_rel_range=None, soft_halo_fraction: float = 0.10, new_bone_share: float = 0.3,
                 energy_keV: float = 40.0, seed: int = 0, blur_sigma_vox: float | None = None,
                 halo_graft_fraction: float | None = None, graft_level: float | None = None) -> dict:
    """New bone vs soft tissue (the mineral boundary), advisor ≥1.2.0.

    S1b (advisor 1.1.0 re-run) found new-bone volume +22…60% and total mineral +15…23% on graft-supported
    specimens: soft-tissue voxels next to dense graft or host bone are partial-volume mixtures that look like
    immature new bone. The best single mineral threshold and its new-bone volume ratio are computed with soft
    tissue mixing towards its dense neighbours (fraction ``soft_halo_fraction``, measured from the scan by the
    integration layer) at the expected new-bone share of non-graft ROI voxels.
    """
    prof = material_profile(material, energy_keV) if isinstance(material, (str, dict, MaterialProfile)) else None
    nb_range = tuple(new_bone_rel_range) if new_bone_rel_range else NEW_BONE_REL_RANGE
    g_level = prof.rel_mean if (prof is not None and not prof.radiolucent) else 0.0
    if graft_samples_rel is not None and np.size(graft_samples_rel) >= MIN_REFERENCE_SAMPLES:
        g_level = float(np.median(graft_samples_rel))
    rng = np.random.default_rng(seed + 1)
    n_soft = 60_000
    soft = rng.normal(0.0, 0.03, n_soft)
    halo = rng.random(n_soft) < soft_halo_fraction
    # neighbours of soft-tissue surface voxels: mostly new-bone trabeculae, also host bone and graft
    nb_mid = float(np.mean(nb_range))
    if graft_level is not None:
        g_level = graft_level
    levels = np.array([nb_mid, HOST_REL_MATURE, max(g_level, nb_mid)])
    # ≥1.4.0: share of halo voxels bordering graft measured in the scan (default assumption 0.2)
    pg = 0.2 if halo_graft_fraction is None else float(np.clip(halo_graft_fraction, 0.0, 1.0))
    nbr = levels[rng.choice(3, int(halo.sum()), p=[0.75 * (1 - pg), 0.25 * (1 - pg), pg])]
    soft[halo] = rng.uniform(0.0, 0.5, int(halo.sum())) * nbr       # minority (<50%) mineral phase in the voxel
    soft = soft + rng.normal(0, noise_rel, n_soft)
    if new_samples_rel is not None and np.size(new_samples_rel) >= MIN_REFERENCE_SAMPLES:
        nb_vals = rng.choice(np.asarray(new_samples_rel, float), 40_000)
    else:
        nbm = ClassModel("uniform", *nb_range, surface_fraction=surface_fraction(150.0, voxel_um))
        nb_vals = nbm.draw(40_000, rng, neighbors=((0.0, 1.0),)) + rng.normal(0, noise_rel, 40_000)
    share = float(np.clip(new_bone_share, 0.02, 0.95))
    k_soft = int(len(nb_vals) * (1 - share) / share)
    soft_s = rng.choice(soft, max(1000, k_soft))
    mb = dice_oracle_samples(nb_vals, soft_s)
    out = {"threshold": mb.get("threshold"), "dice_new_vs_soft": mb.get("dice_graft_threshold_rule"),
           "new_volume_ratio": mb.get("graft_volume_ratio_threshold_rule"),
           "soft_halo_fraction": soft_halo_fraction, "new_bone_share": share}
    out["passes_policy"] = bool((out["dice_new_vs_soft"] or 0) >= ORACLE_DICE_MIN
                                and abs((out["new_volume_ratio"] or 0) - 1) <= ORACLE_VOLUME_TOL)
    return out


def assess_support(material, *, noise_rel: float, voxel_um: float, graft_samples_rel=None,
                   new_samples_rel=None, day0: dict | None = None, calibrated: bool = False,
                   no_graft: bool = False, validated_texture_model: bool = False,
                   graft_prior: float = 0.5, energy_keV: float = 40.0, seed: int = 0,
                   new_bone_rel_range: tuple | None = None, soft_halo_fraction: float = 0.10,
                   new_bone_share: float = 0.3, healing_weeks: float | None = None,
                   observed_graft_level: float | None = None, blur_sigma_vox: float | None = None,
                   graft_struct_um: float | None = None, graft_level_deep: float | None = None,
                   halo_graft_fraction: float | None = None, rim_fraction_new: float | None = None,
                   rim_fraction_mineral: float | None = None) -> SupportAssessment:
    """Decide which endpoints can be reported (see module docstring and docs/science/MEASUREMENT_SUPPORT.md).

    noise_rel          scan noise σ divided by (host − soft) grey contrast.
    graft_samples_rel  optional measured graft intensities (day-0 or material-only scan), relative units.
    new_samples_rel    optional measured new-bone intensities (empty-defect controls) — preferred input.
    day0               {"registered", "qc_pass", "untracked_fraction", "max_displacement_um", "tolerance_um"}.
    soft_halo_fraction share of non-mineral ROI voxels adjacent to dense phases (measured by the integration).
    new_bone_share     expected new-bone share of non-graft ROI voxels (measured by the integration).
    healing_weeks      time since implantation (needed for resorbable materials).
    """
    a = _assess_core(material, noise_rel=noise_rel, voxel_um=voxel_um, graft_samples_rel=graft_samples_rel,
                     new_samples_rel=new_samples_rel, day0=day0, calibrated=calibrated, no_graft=no_graft,
                     validated_texture_model=validated_texture_model, graft_prior=graft_prior,
                     energy_keV=energy_keV, seed=seed, new_bone_rel_range=new_bone_rel_range,
                     healing_weeks=healing_weeks, observed_graft_level=observed_graft_level,
                     blur_sigma_vox=blur_sigma_vox, graft_struct_um=graft_struct_um, graft_level_deep=graft_level_deep)
    mr = mineral_rule(None if no_graft else material, noise_rel=noise_rel, voxel_um=voxel_um,
                      graft_samples_rel=graft_samples_rel, new_samples_rel=new_samples_rel,
                      new_bone_rel_range=new_bone_rel_range, soft_halo_fraction=soft_halo_fraction,
                      new_bone_share=new_bone_share, energy_keV=energy_keV, seed=seed, blur_sigma_vox=blur_sigma_vox,
                      halo_graft_fraction=halo_graft_fraction, graft_level=graft_level_deep)
    a.intensity["mineral_rule"] = mr
    a.policy["soft_halo_fraction"] = soft_halo_fraction
    # ≥1.4.0 error propagation: new bone = mineral − graft, so graft-volume error transfers into new bone scaled by
    # graft:new-bone. New-bone endpoints need |new-bone/soft ratio − 1| + (p/(1−p))·max(|graft ratio − 1|, 0.20) ≤ 10%,
    # where p is the scan's graft share of mineral and 0.20 is the failure threshold (the largest graft error that
    # still counts as "not failed"). Not applied when no graft is present.
    # ≥1.4.0 ambiguous rim (measured on the scan's own segmentation): if more than RIM_TOL of the would-be new bone, or
    # half the rim as a share of total mineral, lies in the one-voxel rim around graft-like voxels, the endpoint is not
    # identifiable (coating vs halo)
    if rim_fraction_new is not None and not no_graft:
        a.intensity["ambiguous_rim"] = {"fraction_of_new_bone": rim_fraction_new, "half_rim_fraction_of_mineral": rim_fraction_mineral}
        if rim_fraction_new > RIM_TOL:
            why = (f"{rim_fraction_new:.0%} of the would-be new bone is a one-voxel rim touching graft-like voxels: new-bone "
                   "coating cannot be told from graft partial-volume halo at this resolution")
            for e in ("new_bone_volume", "new_bone_fraction_of_defect"):
                if e in a.endpoints and a.endpoints[e].status != NOT_SUPPORTED:
                    a.endpoints[e] = EndpointSupport(e, NOT_SUPPORTED, None, why)
            _thickness_endpoint(a.endpoints, voxel_um)
        if rim_fraction_mineral is not None and rim_fraction_mineral > RIM_TOL:
            why = (f"the graft partial-volume rim makes ≈{rim_fraction_mineral:.0%} of total mineral ambiguous "
                   f"(limit {RIM_TOL:.0%})")
            for e in MINERAL_ENDPOINTS:
                if a.endpoints[e].status != NOT_SUPPORTED:
                    a.endpoints[e] = EndpointSupport(e, NOT_SUPPORTED, None, why)
    # only when a visible graft is modelled (radiolucent, unknown and metal paths return an empty intensity model)
    if not no_graft and graft_prior > 0 and a.intensity.get("dice_graft") is not None:
        p_ = float(np.clip(graft_prior, 0.0, 0.95))
        g_vr = a.intensity.get("graft_volume_ratio_threshold_rule", a.intensity.get("graft_volume_ratio"))
        g_err = max(abs((g_vr if g_vr is not None else 1.0) - 1.0), 0.20)
        nb_err = abs((mr.get("new_volume_ratio") or 1.0) - 1.0) + p_ / max(1e-6, 1 - p_) * g_err
        a.intensity["new_bone_error_budget"] = {"graft_share": p_, "propagated_rel_error": float(nb_err)}
        if nb_err > ORACLE_VOLUME_TOL:
            why = (f"new bone is derived as mineral minus graft: with graft {p_:.0%} of mineral, a graft-volume error of "
                   f"up to {g_err:.0%} propagates to ≈{nb_err:.0%} new-bone error (limit {ORACLE_VOLUME_TOL:.0%})")
            for e in ("new_bone_volume", "new_bone_fraction_of_defect"):
                if e in a.endpoints and a.endpoints[e].status != NOT_SUPPORTED:
                    a.endpoints[e] = EndpointSupport(e, NOT_SUPPORTED, None, why)
            _thickness_endpoint(a.endpoints, voxel_um)
    if not mr["passes_policy"]:
        why = (f"new bone vs soft tissue not reliably separable (threshold-rule Dice {mr['dice_new_vs_soft'] or 0:.2f}, "
               f"new-bone volume ratio {mr['new_volume_ratio'] or 0:.2f}): partial-volume halos of dense phases "
               "and immature new bone overlap at this noise level")
        for e in MINERAL_ENDPOINTS + ("new_bone_volume", "new_bone_fraction_of_defect"):
            if e in a.endpoints and a.endpoints[e].status != NOT_SUPPORTED:
                a.endpoints[e] = EndpointSupport(e, NOT_SUPPORTED, None, why)
        _thickness_endpoint(a.endpoints, voxel_um)
    return a
