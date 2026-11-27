"""Material models for phantom generation and CT simulation.

Physics basis
-------------
Linear attenuation of a material at photon energy E:
    mu(E) = rho * sum_i w_i * (mu/rho)_i(E)                (mixture rule)
with elemental mass attenuation coefficients (mu/rho)_i from the NIST XCOM-derived tables
(Hubbell & Seltzer) stored in ``data/nist_xcom.json`` (retrieved 2026-11-27).
Log-log interpolation between tabulated energies; absorption edges are respected because the
tables list duplicate energies at edges.

Bone tissue is modelled as a two-phase mixture: hydroxyapatite mineral at concentration
``mineral_mgHA_cm3`` plus a water-equivalent soft-tissue matrix filling the remaining volume.
This is a deliberate simplification (collagen ≈ soft tissue; carbonate substitution ignored).

Every numeric default below is tagged in ``evidence``: "RF" = literature-supported (source in
``source``), "PHYS" = derived from stoichiometry/physics, "ASSUMPTION" = research assumption
that must be replaced by measurement (physical phantom scans). Values are cross-checked
against docs/science/phantom_parameters.json when that table is available.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import numpy as np

_DATA = Path(__file__).parent / "data" / "nist_xcom.json"
HA_DENSITY = 3.16  # g/cm3, theoretical density of stoichiometric hydroxyapatite [PHYS]


@lru_cache(maxsize=1)
def _xcom():
    return json.loads(_DATA.read_text())["elements"]


def element_mu_rho(el: str, energy_keV) -> np.ndarray:
    e = _xcom()[el]
    E = np.asarray(e["energy_MeV"]) * 1000.0
    mu = np.asarray(e["mu_rho"])
    x = np.atleast_1d(np.asarray(energy_keV, dtype=float))
    # log-log interpolation; handle edges (duplicate energies) by using searchsorted right
    lx, lE, lmu = np.log(x), np.log(E), np.log(mu)
    out = np.empty_like(x)
    for k, v in enumerate(lx):
        j = np.searchsorted(lE, v, side="right")
        j = min(max(j, 1), len(lE) - 1)
        i0, i1 = j - 1, j
        if lE[i1] == lE[i0]:
            out[k] = lmu[i1]
        else:
            t = (v - lE[i0]) / (lE[i1] - lE[i0])
            out[k] = lmu[i0] + t * (lmu[i1] - lmu[i0])
    return np.exp(out)


def mixture_mu_rho(composition: dict[str, float], energy_keV) -> np.ndarray:
    tot = sum(composition.values())
    return sum((w / tot) * element_mu_rho(el, energy_keV) for el, w in composition.items())


# Elemental mass fractions [PHYS: stoichiometry]
COMPOSITIONS = {
    "water": {"H": 0.1119, "O": 0.8881},
    # ICRU-44 soft tissue (minor elements renormalised)
    "soft_tissue": {"H": 0.102, "C": 0.143, "N": 0.034, "O": 0.708, "Na": 0.002, "P": 0.003,
                    "S": 0.003, "Cl": 0.002, "K": 0.003},
    "hydroxyapatite": {"Ca": 0.3989, "P": 0.1850, "O": 0.4141, "H": 0.0020},
    "beta_tcp": {"Ca": 0.3876, "P": 0.1997, "O": 0.4127},
    "calcium_sulfate_dihydrate": {"Ca": 0.2328, "S": 0.1862, "O": 0.5576, "H": 0.0234},
    "bioglass_45s5": {"Si": 0.2103, "Na": 0.1818, "Ca": 0.1751, "P": 0.0262, "O": 0.4066},
    "titanium": {"Ti": 1.0},
    "magnesium": {"Mg": 1.0},
    "air": {"N": 0.755, "O": 0.232, "C": 0.0001},
    "aluminium": {"Al": 1.0},
}


@dataclass
class Material:
    """A tissue or biomaterial phase.

    For bone-like tissue set ``mineral_mgHA_cm3`` (HA in a water-like matrix).
    For a solid biomaterial set ``composition`` + ``solid_density`` and ``micro_porosity``
    (sub-voxel pore fraction, assumed fluid-filled).
    """
    name: str
    label: int                      # ground-truth class (0 bg, 1 new bone, 2 graft, 3 host)
    mineral_mgHA_cm3: float | None = None
    composition: str | None = None
    solid_density: float | None = None
    micro_porosity: float = 0.0
    heterogeneity_cv: float = 0.05  # coefficient of variation of smooth density field
    evidence: str = "ASSUMPTION"
    source: str = ""
    notes: str = ""

    def mu(self, energy_keV, scale=1.0) -> np.ndarray:
        """Linear attenuation (1/cm) at energy (keV); ``scale`` multiplies mineral/solid density."""
        if self.mineral_mgHA_cm3 is not None:
            m = self.mineral_mgHA_cm3 * scale / 1000.0  # g HA / cm3
            frac_mineral_vol = m / HA_DENSITY
            matrix = max(0.0, 1.0 - frac_mineral_vol) * 1.06
            return (m * mixture_mu_rho(COMPOSITIONS["hydroxyapatite"], energy_keV)
                    + matrix * mixture_mu_rho(COMPOSITIONS["soft_tissue"], energy_keV))
        if self.composition is not None:
            rho = self.solid_density * scale * (1.0 - self.micro_porosity)
            fluid = self.micro_porosity * 1.0
            return (rho * mixture_mu_rho(COMPOSITIONS[self.composition], energy_keV)
                    + fluid * mixture_mu_rho(COMPOSITIONS["water"], energy_keV))
        raise ValueError(f"Material {self.name} has no composition")

    def ha_equivalent(self, energy_keV=40.0) -> float:
        """HA-equivalent mineral density (mg/cm3) at an effective energy: the mgHA/cm3 of a
        bone-like tissue with the same mu. Shows why non-HA materials 'look' like bone of a
        different density depending on beam energy."""
        target = float(np.ravel(self.mu(energy_keV))[0])
        water = float(np.ravel(Material("w", 0, mineral_mgHA_cm3=0.0).mu(energy_keV))[0])
        lo, hi = 0.0, 3160.0
        if target <= water:
            return 0.0
        for _ in range(60):
            mid = (lo + hi) / 2
            if float(np.ravel(Material("b", 0, mineral_mgHA_cm3=mid).mu(energy_keV))[0]) < target:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2


# --------------------------------------------------------------------------- registry
# NOTE: values marked ASSUMPTION are placeholders to be replaced from the literature table
# (docs/science/phantom_parameters.json) and ultimately by physical phantom measurements.
def default_materials() -> dict[str, Material]:
    M = {
        "marrow": Material("marrow", 0, mineral_mgHA_cm3=0.0, heterogeneity_cv=0.0, evidence="PHYS",
                           notes="Marrow/soft tissue modelled as mineral-free soft tissue"),
        "fibrous": Material("fibrous", 0, mineral_mgHA_cm3=30.0, heterogeneity_cv=0.3,
                            notes="Fibrous/granulation tissue with trace mineral (ASSUMPTION)"),
        "void": Material("void", 0, composition="air", solid_density=0.0012, heterogeneity_cv=0.0,
                         evidence="PHYS"),
        "host_cortical": Material("host_cortical", 3, mineral_mgHA_cm3=1150.0, heterogeneity_cv=0.03,
                                  notes="Mature cortical TMD; rodent/rabbit typically ~1000-1300 (ASSUMPTION pending table)"),
        "host_trabecular": Material("host_trabecular", 3, mineral_mgHA_cm3=1000.0, heterogeneity_cv=0.05),
        "new_bone_woven": Material("new_bone_woven", 1, mineral_mgHA_cm3=750.0, heterogeneity_cv=0.12,
                                   notes="Woven bone less mineralised than lamellar; matures with time"),
        # Graft materials (solid phase from stoichiometry, porosity ASSUMPTION)
        "ha": Material("ha", 2, composition="hydroxyapatite", solid_density=3.16, micro_porosity=0.30,
                       heterogeneity_cv=0.04, notes="Sintered HA granules; theoretical density 3.16 g/cm3"),
        "beta_tcp": Material("beta_tcp", 2, composition="beta_tcp", solid_density=3.07, micro_porosity=0.60,
                             heterogeneity_cv=0.10, notes="Microporous beta-TCP granules (porosity ASSUMPTION)"),
        "bcp": Material("bcp", 2, composition="hydroxyapatite", solid_density=3.10, micro_porosity=0.50,
                        heterogeneity_cv=0.08, notes="BCP approximated as HA/TCP blend with HA composition"),
        "calcium_sulfate": Material("calcium_sulfate", 2, composition="calcium_sulfate_dihydrate",
                                    solid_density=2.32, micro_porosity=0.35, heterogeneity_cv=0.06),
        "bioglass_45s5": Material("bioglass_45s5", 2, composition="bioglass_45s5", solid_density=2.70,
                                  micro_porosity=0.40, heterogeneity_cv=0.06),
        "allograft": Material("allograft", 2, mineral_mgHA_cm3=1100.0, heterogeneity_cv=0.04,
                              notes="Mineralised allograft = bone tissue: intensity-indistinguishable from host bone by construction"),
        "xenograft_dbbm": Material("xenograft_dbbm", 2, composition="hydroxyapatite", solid_density=3.0,
                                   micro_porosity=0.55, heterogeneity_cv=0.06,
                                   notes="Deproteinised bovine bone mineral; trabecular-like morphology"),
        "dbm": Material("dbm", 2, mineral_mgHA_cm3=60.0, heterogeneity_cv=0.3,
                        notes="Demineralised bone matrix: near radiolucent"),
        "magnesium": Material("magnesium", 2, composition="magnesium", solid_density=1.74, micro_porosity=0.0,
                              heterogeneity_cv=0.02),
        "titanium": Material("titanium", 2, composition="titanium", solid_density=4.51, micro_porosity=0.0,
                             heterogeneity_cv=0.0, evidence="PHYS"),
    }
    for m in M.values():
        if m.composition is not None and m.evidence == "ASSUMPTION" and m.name in ("ha", "beta_tcp"):
            m.source = "solid density: stoichiometric theoretical value; porosity: ASSUMPTION"
    return M


def material_contrast_table(energies_keV=(30, 40, 60, 80)) -> list[dict]:
    """HA-equivalent density of every material at several effective energies (pure physics)."""
    rows = []
    for name, m in default_materials().items():
        if name == "void":
            continue
        rows.append({"material": name, "label": m.label,
                     **{f"mgHA_eq_{int(e)}keV": round(m.ha_equivalent(e), 1) for e in energies_keV}})
    return rows
