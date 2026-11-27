"""Procedural bone-defect phantom generator with exact voxel-level ground truth.

Three defect models
-------------------
* ``condyle``   — cancellous bone block with a cortical surface and a drilled cylindrical
                  defect (rabbit femoral-condyle-like). Defect axis = z.
* ``calvarial`` — thin plate (outer/inner tables + diploe) with a full-thickness circular defect;
                  osteogenesis from margins and from the dural side (rat/rabbit calvaria-like).
* ``segmental`` — long-bone tube (cortex + marrow) with a segmental gap (long axis = z).

Biology model (a deliberately simple, documented caricature — all rates are ASSUMPTIONS):
* healing ``stage`` s ∈ [0, 1] (0 = day of implantation).
* new bone advances from existing host-bone surfaces: front depth = s·ingrowth·R_defect with a
  spatially noisy front; woven bone forms a trabecular-like network whose local BV/TV decays
  with distance from the host surface.
* osteoconduction: new-bone coating on graft surfaces near/ahead of the front.
* resorption: each granule loses a surface shell; fraction ∝ s·resorption_rate, larger near the
  host bone (better vascular access); resorbed graft is partly replaced by new bone
  ("creeping substitution").
* new-bone mineralisation increases with local maturity (time since formation proxy).

Ground truth is computed on a supersampled grid and integrated to the output grid, so each
output voxel has exact class fractions (partial-volume truth) and a majority label.
"""
from __future__ import annotations

import time
from dataclasses import asdict, dataclass, field

import numpy as np
from scipy import ndimage as ndi

from .materials import Material, default_materials
from .structures import (block_fractions, block_mean, cylinder_mask, grf, pack_granules, shell,
                         smooth_field, erode_instances, trabecular_network)

GENERATOR_VERSION = "1.0.0"

# high-resolution tissue codes
T_MARROW, T_FIBROUS, T_VOID = 0, 1, 2
T_CORT, T_TRAB = 10, 11
T_NEW = 20
T_GRAFT = 30
CODE_TO_LABEL = {T_MARROW: 0, T_FIBROUS: 0, T_VOID: 0, T_CORT: 3, T_TRAB: 3, T_NEW: 1, T_GRAFT: 2}

# material-specific default resorption at stage 1 (fraction of initial granule volume) — ASSUMPTION,
# ordering motivated by literature: CaSO4 > beta-TCP > BCP > bioglass > HA ≈ xenograft (slow)
DEFAULT_RESORPTION = {"calcium_sulfate": 0.95, "beta_tcp": 0.7, "bcp": 0.45, "bioglass_45s5": 0.5,
                      "ha": 0.1, "xenograft_dbbm": 0.1, "allograft": 0.5, "dbm": 0.8,
                      "magnesium": 0.6, "titanium": 0.0}


@dataclass
class PhantomConfig:
    model: str = "condyle"
    shape: tuple = (96, 96, 96)
    voxel_um: float = 40.0
    supersample: int = 2
    defect_diameter_um: float = 2400.0
    defect_depth_um: float | None = None
    margin_um: float = 200.0                  # soft tissue above bone surface (condyle)
    cortical_thickness_um: float = 240.0
    plate_thickness_um: float = 1200.0        # calvarial plate
    gap_length_um: float = 2000.0             # segmental gap
    host_tb_sp_um: float = 450.0
    host_bv_tv: float = 0.25
    graft_material: str | None = "beta_tcp"
    graft_diam_um: tuple = (350.0, 700.0)
    graft_fill: float = 0.35
    graft_roughness: float = 0.15
    healing_stage: float = 0.5
    resorption_rate: float | None = None      # None -> material default
    ingrowth: float = 0.9
    new_bone_bv_tv_wall: float = 0.55         # local BV/TV of woven bone at the host surface
    new_bone_bv_tv_front: float = 0.15
    new_bone_tb_sp_um: float = 300.0
    coat_um: float = 60.0
    substitution: float = 0.5
    woven_mineral: tuple = (650.0, 1000.0)    # mgHA/cm3, immature -> mature (ASSUMPTION)
    fibrous_fraction: float = 0.35
    n_voids: int = 0
    void_diam_um: tuple = (150.0, 400.0)
    dural_osteogenesis: float = 0.5           # calvarial only
    effective_energy_keV: float = 40.0
    material_overrides: dict = field(default_factory=dict)
    periodic_texture: bool = True   # legacy default (dataset v1). False = non-periodic fields (use for registration)
    seed: int = 0

    def to_dict(self):
        d = asdict(self)
        d["shape"] = list(self.shape)
        return d


@dataclass
class Phantom:
    config: PhantomConfig
    labels: np.ndarray                 # uint8 (0,1,2,3) majority label at output grid
    class_fractions: dict              # {label: float32 fraction map}
    material_fractions: dict           # {material name: density-weighted fraction map}
    mu: np.ndarray                     # linear attenuation (1/cm) at effective energy
    roi_mask: np.ndarray               # bool, defect ROI (exact geometric)
    roi: dict                          # mathematical ROI definition (physical µm)
    truth: dict                        # ground-truth morphometry in ROI (partial-volume exact)
    materials: dict                    # name -> Material used
    meta: dict

    @property
    def spacing(self):
        return (self.config.voxel_um,) * 3


def _materials(cfg: PhantomConfig) -> dict[str, Material]:
    M = default_materials()
    for name, over in cfg.material_overrides.items():
        if name in M:
            for k, v in over.items():
                setattr(M[name], k, v)
    return M


def generate_phantom(cfg: PhantomConfig, keep_highres: bool = False) -> Phantom:
    t0 = time.time()
    rng = np.random.default_rng(cfg.seed)
    ss = int(cfg.supersample)
    v = cfg.voxel_um / ss  # high-res voxel (µm)
    S = tuple(int(n) * ss for n in cfg.shape)
    M = _materials(cfg)
    tissue = np.full(S, T_MARROW, np.uint8)
    cz, cy, cx = (S[0] - 1) / 2, (S[1] - 1) / 2, (S[2] - 1) / 2
    R = cfg.defect_diameter_um / 2 / v

    # ---------------------------------------------------------------- host anatomy + defect
    if cfg.model == "condyle":
        m0 = int(round(cfg.margin_um / v))
        ct = max(1, int(round(cfg.cortical_thickness_um / v)))
        bone_dom = np.zeros(S, bool)
        bone_dom[m0:] = True
        cort = np.zeros(S, bool)
        cort[m0:m0 + ct] = True
        depth = cfg.defect_depth_um / v if cfg.defect_depth_um else (S[0] - m0) * 0.85
        defect = cylinder_mask(S, (cz, cy, cx), "z", R, (m0, int(m0 + depth)))
        roi = {"type": "cylinder", "axis": "z", "center_um": [None, cy * v, cx * v],
               "radius_um": cfg.defect_diameter_um / 2, "z_range_um": [m0 * v, (m0 + depth) * v]}
        dura = None
    elif cfg.model == "calvarial":
        T = cfg.plate_thickness_um / v
        z0, z1 = int(round(cz - T / 2)), int(round(cz + T / 2))
        ct = max(1, int(round(cfg.cortical_thickness_um / v)))
        bone_dom = np.zeros(S, bool)
        bone_dom[z0:z1] = True
        cort = np.zeros(S, bool)
        cort[z0:z0 + ct] = True
        cort[z1 - ct:z1] = True
        defect = cylinder_mask(S, (cz, cy, cx), "z", R, (z0, z1))
        roi = {"type": "cylinder", "axis": "z", "center_um": [None, cy * v, cx * v],
               "radius_um": cfg.defect_diameter_um / 2, "z_range_um": [z0 * v, z1 * v]}
        dura = (z1, ct)
    elif cfg.model == "segmental":
        Ro = min(S[1], S[2]) * 0.38
        ct = max(2, int(round(cfg.cortical_thickness_um / v)))
        tube = cylinder_mask(S, (cz, cy, cx), "z", Ro)
        inner = cylinder_mask(S, (cz, cy, cx), "z", Ro - ct)
        gap = cfg.gap_length_um / v
        g0, g1 = int(round(cz - gap / 2)), int(round(cz + gap / 2))
        bone_dom = tube.copy()
        cort = tube & ~inner
        defect = cylinder_mask(S, (cz, cy, cx), "z", Ro, (g0, g1))
        R = Ro
        roi = {"type": "cylinder", "axis": "z", "center_um": [None, cy * v, cx * v],
               "radius_um": Ro * v, "z_range_um": [g0 * v, g1 * v]}
        dura = None
    else:
        raise ValueError(f"Unknown model {cfg.model}")

    gmode = "wrap" if cfg.periodic_texture else "reflect"
    trab = trabecular_network(S, v, cfg.host_tb_sp_um, cfg.host_bv_tv, rng, mode=gmode)
    if cfg.model == "segmental":
        trab &= False  # diaphysis: marrow cavity without trabeculae (simplification)
    host_cort = cort & ~defect
    host_trab = trab & bone_dom & ~cort & ~defect
    tissue[host_trab] = T_TRAB
    tissue[host_cort] = T_CORT
    host = host_cort | host_trab

    # ---------------------------------------------------------------- graft
    gm = cfg.graft_material
    graft0 = np.zeros(S, bool)
    graft = np.zeros(S, bool)
    granules = []
    d_host = ndi.distance_transform_edt(~host).astype(np.float32) * v  # µm from host bone
    if gm:
        inner_def = defect & (ndi.distance_transform_edt(defect) > 1)
        inst, granules = pack_granules(inner_def, v, cfg.graft_diam_um, cfg.graft_fill, rng,
                                       roughness=cfg.graft_roughness)
        graft0 = inst > 0
        rate = cfg.resorption_rate if cfg.resorption_rate is not None else DEFAULT_RESORPTION.get(gm, 0.3)
        f_base = rate * cfg.healing_stage
        if f_base > 0 and len(granules):
            # per-granule resorption: more near host bone (vascular access)
            objs = ndi.find_objects(inst)
            fr = np.zeros(len(granules))
            for g in granules:
                sl = objs[g["id"] - 1]
                dmean = float(d_host[sl][inst[sl] == g["id"]].mean())
                w = np.exp(-dmean / max(R * v, 1))
                fr[g["id"] - 1] = np.clip(f_base * (0.6 + 0.8 * w) * rng.uniform(0.8, 1.2), 0, 1)
            inst = erode_instances(inst, fr, v, rng)
        graft = inst > 0
        tissue[graft] = T_GRAFT

    # ---------------------------------------------------------------- new bone
    s = cfg.healing_stage
    newb = np.zeros(S, bool)
    maturity = np.zeros(S, np.float32)
    if s > 0:
        front = s * cfg.ingrowth * R * v                      # µm
        front_noise = grf(S, max(2.0, 0.15 * R), rng, gmode) * 0.2 * front
        d_eff = d_host.copy()
        if dura is not None and cfg.dural_osteogenesis > 0:
            zz = np.arange(S[0], dtype=np.float32)[:, None, None]
            d_dura = np.abs(zz - (dura[0] - 1)) * v / cfg.dural_osteogenesis
            d_eff = np.minimum(d_eff, np.broadcast_to(d_dura, S))
        reach = (d_eff < front + front_noise) & defect
        # woven network with local BV/TV decaying from wall to front
        g = np.abs(_abs_field(S, v, cfg.new_bone_tb_sp_um, rng, gmode))
        rel = np.clip(d_eff / max(front, 1e-6), 0, 1)
        target_bv = cfg.new_bone_bv_tv_wall + (cfg.new_bone_bv_tv_front - cfg.new_bone_bv_tv_wall) * rel
        qs = np.linspace(0, 1, 201)
        qv = np.quantile(g[:: max(1, S[0] // 32)], qs)
        thr = np.interp(target_bv, qs, qv)
        newb = reach & (g < thr)
        # osteoconduction coating on remaining graft near/ahead of front
        if gm and cfg.coat_um > 0:
            coat = shell(graft, cfg.coat_um * s / v) & defect & (d_eff < 1.4 * front + front_noise)
            newb |= coat
        # creeping substitution of resorbed graft
        if gm and cfg.substitution > 0:
            resorbed = graft0 & ~graft & reach
            sub_field = grf(S, 1.5, rng)
            newb |= resorbed & (sub_field < np.quantile(sub_field, cfg.substitution))
        newb &= ~graft & ~host
        maturity = np.clip(s * (1.0 - 0.6 * rel), 0, 1).astype(np.float32)
        tissue[newb] = T_NEW

    # ---------------------------------------------------------------- soft tissues in defect
    free = defect & (tissue == T_MARROW)
    if cfg.fibrous_fraction > 0:
        fg = grf(S, 3.0, rng)
        fib = free & (fg < np.quantile(fg[free], cfg.fibrous_fraction) if free.any() else False)
        tissue[fib] = T_FIBROUS
    if cfg.n_voids > 0:
        coords = np.argwhere(defect & (tissue <= T_FIBROUS))
        zz, yy, xx = np.ogrid[: S[0], : S[1], : S[2]]
        for _ in range(cfg.n_voids):
            if len(coords) == 0:
                break
            c = coords[rng.integers(len(coords))]
            r = rng.uniform(*cfg.void_diam_um) / 2 / v
            sl = tuple(slice(max(0, int(c[i] - r - 1)), min(S[i], int(c[i] + r + 2))) for i in range(3))
            sub = ((zz[sl[0]] - c[0]) ** 2 + (yy[:, sl[1]] - c[1]) ** 2 + (xx[:, :, sl[2]] - c[2]) ** 2) <= r * r
            t = tissue[sl]
            t[sub & (t <= T_FIBROUS)] = T_VOID

    # ---------------------------------------------------------------- integrate to output grid
    lab_hr = np.zeros(S, np.uint8)
    for code, lab in CODE_TO_LABEL.items():
        lab_hr[tissue == code] = lab
    fr = block_fractions(lab_hr, ss, (0, 1, 2, 3))
    stack = np.stack([fr[c] for c in (0, 1, 2, 3)])
    labels = np.argmax(stack, axis=0).astype(np.uint8)
    roi_mask = block_mean(defect.astype(np.float32), ss) >= 0.5

    E = cfg.effective_energy_keV
    het_sigma = max(1.0, 100.0 / v)
    mat_by_code = {T_MARROW: "marrow", T_FIBROUS: "fibrous", T_VOID: "void",
                   T_CORT: "host_cortical", T_TRAB: "host_trabecular"}
    if gm:
        mat_by_code[T_GRAFT] = gm
    material_fracs = {}
    mu_hr_total = np.zeros(tuple(n // ss for n in S), np.float32)
    for code, name in mat_by_code.items():
        ind = tissue == code
        if not ind.any():
            continue
        het = smooth_field(S, het_sigma, rng, M[name].heterogeneity_cv)
        mf = block_mean(np.where(ind, het, 0).astype(np.float32), ss)
        material_fracs[name] = mf
        mu_hr_total += mf * float(np.ravel(M[name].mu(E))[0])
    # new bone: mineral depends on maturity -> represent as two end-member materials
    if newb.any():
        lo, hi = cfg.woven_mineral
        M["new_bone_immature"] = Material("new_bone_immature", 1, mineral_mgHA_cm3=lo, heterogeneity_cv=0.12)
        M["new_bone_mature"] = Material("new_bone_mature", 1, mineral_mgHA_cm3=hi, heterogeneity_cv=0.06)
        het = smooth_field(S, het_sigma, rng, 0.10)
        w_m = np.where(newb, maturity, 0).astype(np.float32)
        f_mat = block_mean(w_m * het, ss)
        f_imm = block_mean(np.where(newb, (1 - maturity) * het, 0).astype(np.float32), ss)
        material_fracs["new_bone_mature"] = f_mat
        material_fracs["new_bone_immature"] = f_imm
        mu_hr_total += (f_mat * float(np.ravel(M["new_bone_mature"].mu(E))[0])
                        + f_imm * float(np.ravel(M["new_bone_immature"].mu(E))[0]))

    # ---------------------------------------------------------------- ground truth morphometry
    vox_mm3 = (cfg.voxel_um / 1000.0) ** 3
    roi_frac = block_mean(defect.astype(np.float32), ss)
    tv = float(roi_frac.sum()) * vox_mm3
    truth = {"TV_mm3": tv}
    for c, nm in ((1, "new_bone"), (2, "graft"), (3, "host_bone")):
        vol = float((block_mean(((lab_hr == c) & defect).astype(np.float32), ss)).sum()) * vox_mm3
        truth[f"{nm}_volume_mm3"] = vol
        truth[f"{nm}_fraction"] = vol / tv if tv > 0 else float("nan")
    truth["BV_TV_new_bone"] = truth["new_bone_fraction"]
    truth["mineralized_fraction"] = truth["new_bone_fraction"] + truth["graft_fraction"] + truth["host_bone_fraction"]
    truth["graft_initial_volume_mm3"] = float(block_mean((graft0 & defect).astype(np.float32), ss).sum()) * vox_mm3
    truth["graft_resorbed_fraction"] = (1 - truth["graft_volume_mm3"] / truth["graft_initial_volume_mm3"]
                                        if truth["graft_initial_volume_mm3"] > 0 else float("nan"))
    truth["host_bv_tv_outside_roi"] = float(host[~defect & bone_dom].mean()) if (~defect & bone_dom).any() else float("nan")
    truth["n_granules"] = len(granules)
    # convert ROI from high-res index units to physical µm in the output-grid convention
    # (voxel j centre at j*V; high-res voxel i centre at (i+0.5)*v - V/2; edge e at e*v - V/2)
    V = cfg.voxel_um
    roi["center_um"] = [None if c is None else round((c / v + 0.5) * v - V / 2, 3) for c in roi["center_um"]]
    roi["z_range_um"] = [round(e - V / 2, 3) for e in roi["z_range_um"]]
    roi["voxel_um"] = V

    meta = {"generator_version": GENERATOR_VERSION, "seconds": round(time.time() - t0, 2),
            "highres_voxel_um": v, "provenance": "synthetic", "effective_energy_keV": E}
    if keep_highres:
        meta["tissue_highres"] = tissue
    return Phantom(cfg, labels, {c: fr[c] for c in (0, 1, 2, 3)}, material_fracs, mu_hr_total,
                   roi_mask, roi, truth, M, meta)


def _abs_field(S, v, tb_sp_um, rng, mode="wrap"):
    sigma = max(0.8, 0.30 * tb_sp_um / v)
    g = ndi.gaussian_filter(rng.standard_normal(S).astype(np.float32), sigma, mode=mode)
    g2 = ndi.gaussian_filter(rng.standard_normal(S).astype(np.float32), sigma * 2.5, mode=mode)
    return g / (g.std() + 1e-8) + 0.35 * g2 / (g2.std() + 1e-8)
