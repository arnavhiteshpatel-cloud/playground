"""Morphometry against analytically known answers (Bouxsein 2010 parameter set).

Discretisation conventions asserted here are the documented ones in morphometry/core.py:
local thickness has 0-voxel bias for even and +1 voxel for odd voxel thicknesses.
"""
import math

import numpy as np
import pytest

from osteoquant.morphometry.analytic import hollow_cylinder, rods, sphere, torus_count_phantom
from osteoquant.morphometry.core import (bone_implant_contact, bridging, class_volumes, cortical_thickness,
                                         defect_report_metrics, density_stats, euler_connectivity,
                                         local_thickness, porosity, radial_ingrowth_profile,
                                         surface_area_mm2, thickness_stats, trabecular_morphometry,
                                         volume_mm3)
from osteoquant.volume import Volume


def plate_stack(t, gap, n=4, lead=5, shape_yx=(24, 24)):
    """n plates of thickness t separated by gap, with a background lead-in/out along z."""
    nz = 2 * lead + n * t + (n - 1) * gap
    m = np.zeros((nz,) + shape_yx, bool)
    z = lead
    for _ in range(n):
        m[z:z + t] = True
        z += t + gap
    tv = np.zeros_like(m)
    tv[lead:nz - lead] = True
    return m, tv


# ----------------------------------------------------------------------------- volume / surface
def test_volume_is_voxel_count_times_voxel_volume_anisotropic():
    m = np.zeros((10, 10, 10), bool)
    m[2:5, 1:8, 3:9] = True          # 3*7*6 = 126 voxels
    assert volume_mm3(m, (10.0, 20.0, 30.0)) == pytest.approx(126 * 10 * 20 * 30 * 1e-9, rel=1e-12)
    assert volume_mm3(np.zeros((3, 3, 3), bool), (1, 1, 1)) == 0.0


def test_surface_area_cube_and_sphere_marching_cubes():
    c = np.zeros((20, 20, 20), bool)
    c[4:16, 4:16, 4:16] = True
    a = surface_area_mm2(c, (1000.0,) * 3)      # 1 mm voxels -> mm²
    assert 0.93 * 6 * 144 < a < 6 * 144          # chamfered edges: slightly below the voxel box
    s = sphere((50, 50, 50), (25, 25, 25), 20)
    a = surface_area_mm2(s, (1000.0,) * 3)
    assert a == pytest.approx(4 * math.pi * 400, rel=0.10)   # binary MC: < 10 % over-estimate
    assert surface_area_mm2(np.zeros((4, 4, 4), bool), (1, 1, 1)) == 0.0


def test_surface_area_scales_with_spacing_squared():
    c = np.zeros((12, 12, 12), bool)
    c[3:9, 3:9, 3:9] = True
    a1 = surface_area_mm2(c, (10.0, 10.0, 10.0))
    a2 = surface_area_mm2(c, (20.0, 20.0, 20.0))
    assert a2 == pytest.approx(4 * a1, rel=1e-9)


# ----------------------------------------------------------------------------- thickness
@pytest.mark.parametrize("t", [2, 4, 6, 8])
def test_plate_thickness_even_is_exact(t):
    m, _ = plate_stack(t, 8)
    th = local_thickness(m, 10.0, border="edge")
    assert np.allclose(th[m], 10.0 * t)
    assert np.all(th[~m] == 0)


@pytest.mark.parametrize("t", [3, 5, 7])
def test_plate_thickness_odd_has_documented_plus_one_voxel_bias(t):
    m, _ = plate_stack(t, 8)
    th = local_thickness(m, 10.0, border="edge")
    assert np.allclose(th[m], 10.0 * (t + 1))


def test_rod_thickness_close_to_diameter():
    m = rods((20, 40, 40), 6, 20)
    th = local_thickness(m, 1.0, border="edge")[m]
    assert abs(th.mean() - 6.0) <= 1.0


def test_sphere_max_thickness_is_diameter():
    m = sphere((41, 41, 41), (20, 20, 20), 10)
    th = local_thickness(m, 1.0, border="background")
    assert 19.0 <= th.max() <= 21.0


def test_hollow_cylinder_cortical_thickness():
    hc = hollow_cylinder((10, 60, 60), 25, 19)
    r = cortical_thickness(hc, 1.0)
    assert abs(r["Ct_Th_um"] - 6.0) <= 1.0 and r["Ct_Th_sd_um"] >= 0


def test_border_conventions_differ_for_cut_structures():
    m = np.ones((10, 10, 10), bool)                 # structure cut on every side by the VOI
    edge = local_thickness(m, 1.0, border="edge")[m].mean()
    bg = local_thickness(m, 1.0, border="background")[m].mean()
    assert bg <= 11.0 and edge > 2 * bg             # 'edge' assumes the structure continues


def test_thickness_empty_and_single_voxel():
    z = np.zeros((5, 5, 5), bool)
    assert np.all(local_thickness(z, 3.0) == 0)
    s = thickness_stats(z, 1.0)
    assert all(math.isnan(v) for v in s.values())
    one = z.copy()
    one[2, 2, 2] = True
    th = local_thickness(one, 3.0, border="background")
    assert th[2, 2, 2] > 0 and th[~one].max() == 0


def test_thickness_scales_linearly_with_voxel_size():
    m, _ = plate_stack(4, 6)
    a = local_thickness(m, 1.0, border="edge")
    b = local_thickness(m, 37.5, border="edge")
    assert np.allclose(b, 37.5 * a)


# ----------------------------------------------------------------------------- trabecular set
def test_trabecular_morphometry_on_plates_exact():
    m, tv = plate_stack(4, 8)
    r = trabecular_morphometry(m, tv, 10.0)
    assert r["BV_TV"] == pytest.approx(16 / 40)
    assert r["Tb_Th_um"] == pytest.approx(40.0) and r["Tb_Th_sd_um"] == pytest.approx(0.0)
    assert r["Tb_Sp_um"] == pytest.approx(80.0)
    assert r["Tb_N_per_mm"] == pytest.approx(1000.0 / 120.0)
    assert r["conn_beta0"] == 4 and r["conn_beta1"] == 0 and r["Conn_D_per_mm3"] == 0.0
    assert r["thickness_border_convention"] == "edge"
    assert r["BS_TV_per_mm"] == pytest.approx(r["BS_mm2"] / r["TV_mm3"])
    assert r["BS_BV_per_mm"] == pytest.approx(r["BS_mm2"] / r["BV_mm3"])


def test_trabecular_morphometry_empty_tv_gives_nan_not_crash():
    z = np.zeros((6, 6, 6), bool)
    r = trabecular_morphometry(z, z, 10.0)
    assert r["TV_mm3"] == 0 and math.isnan(r["BV_TV"]) and math.isnan(r["Tb_N_per_mm"])
    assert math.isnan(r["Conn_D_per_mm3"])


def test_trabecular_morphometry_skips_optional_blocks():
    m, tv = plate_stack(2, 2)
    r = trabecular_morphometry(m, tv, 10.0, compute_thickness=False, compute_conn=False)
    assert "Tb_Th_um" not in r and "Conn_D_per_mm3" not in r


def test_bone_outside_tv_is_ignored():
    m, tv = plate_stack(4, 8)
    extra = m.copy()
    extra[0:2] = True                     # bone in the lead-in, outside TV
    a = trabecular_morphometry(m, tv, 10.0, compute_thickness=False)
    b = trabecular_morphometry(extra, tv, 10.0, compute_thickness=False)
    assert a["BV_mm3"] == b["BV_mm3"]


# ----------------------------------------------------------------------------- connectivity
@pytest.mark.parametrize("n", [1, 2, 3, 5])
def test_euler_holes(n):
    e = euler_connectivity(torus_count_phantom((12, 20, 60), n))
    assert e["beta1"] == n and e["beta0"] == 1 and e["euler"] == 1 - n


def test_euler_cavity_and_components():
    c = np.zeros((20, 20, 20), bool)
    c[4:16, 4:16, 4:16] = True
    c[8:12, 8:12, 8:12] = False
    e = euler_connectivity(c)
    assert e == {"beta0": 1, "beta1": 0, "beta2": 1, "euler": 2}
    two = np.zeros((10, 10, 10), bool)
    two[1:3, 1:3, 1:3] = True
    two[6:8, 6:8, 6:8] = True
    assert euler_connectivity(two)["beta0"] == 2
    diag = np.zeros((4, 4, 4), bool)
    diag[1, 1, 1] = diag[2, 2, 2] = True          # 26-connected foreground
    assert euler_connectivity(diag)["beta0"] == 1
    assert euler_connectivity(np.zeros((3, 3, 3), bool))["euler"] == 0


# ----------------------------------------------------------------------------- defect endpoints
def test_porosity():
    env = np.ones((4, 4, 4), bool)
    mat = np.zeros_like(env)
    mat[:2] = True
    assert porosity(mat, env) == pytest.approx(0.5)
    assert math.isnan(porosity(mat, np.zeros_like(env)))


def test_class_volumes_additivity_and_abstention():
    lab = np.zeros((10, 10, 10), np.uint8)
    lab[:2] = 1
    lab[2:5] = 2
    lab[5:6] = 3
    lab[6:7] = 255
    roi = np.ones_like(lab, bool)
    sp = (10.0, 20.0, 5.0)
    cv = class_volumes(lab, roi, sp)
    vv = 1e-9 * 10 * 20 * 5 * 100
    assert cv["new_bone_volume_mm3"] == pytest.approx(2 * vv)
    assert cv["residual_graft_volume_mm3"] == pytest.approx(3 * vv)
    assert cv["host_bone_volume_mm3"] == pytest.approx(vv)
    assert cv["uncertain_fraction"] == pytest.approx(0.1)
    assert cv["mineralized_fraction"] == pytest.approx(0.6)
    assert cv["TV_certain_mm3"] == pytest.approx(9 * vv)
    assert cv["new_bone_fraction_of_certain"] == pytest.approx(2 / 9)
    empty = class_volumes(lab, np.zeros_like(roi), sp)
    assert empty["TV_mm3"] == 0 and math.isnan(empty["new_bone_fraction"])
    assert math.isnan(empty["new_bone_fraction_of_certain"])


def test_radial_ingrowth_profile_shells():
    roi = np.zeros((3, 41, 41), bool)
    roi[:, 5:36, 5:36] = True
    nb = np.zeros_like(roi)
    nb[:, 5:36, 5:8] = True                      # new bone only along one rim
    prof = radial_ingrowth_profile(nb, roi, (10.0, 10.0, 10.0), shell_um=50.0)
    assert prof[0]["from_um"] == 0.0 and prof[0]["to_um"] == 50.0
    assert sum(p["n_vox"] for p in prof) == roi.sum()      # shells partition the ROI
    assert all(0 <= p["new_bone_fraction"] <= 1 for p in prof)
    assert prof[0]["new_bone_fraction"] > 0 and prof[-1]["new_bone_fraction"] == 0


def test_bridging_closed_open_and_connected():
    roi = np.zeros((12, 10, 10), bool)
    roi[3:9, 2:8, 2:8] = True
    host = np.zeros_like(roi)
    host[:3, 2:8, 2:8] = True
    host[9:, 2:8, 2:8] = True
    full = roi.copy()
    b = bridging(full, roi, axis=0, host=host)
    assert b["projected_coverage"] == 1.0 and b["min_cross_section_fill"] == 1.0 and b["connected_bridge"]
    half = roi.copy()
    half[6:9] = False                          # gap in the middle of the defect -> no union
    b = bridging(half, roi, axis=0, host=host)
    assert b["projected_coverage"] == 1.0 and b["min_cross_section_fill"] == 0.0 and not b["connected_bridge"]
    assert b["mean_cross_section_fill"] == pytest.approx(0.5)
    none = bridging(np.zeros_like(roi), np.zeros_like(roi))
    assert math.isnan(none["projected_coverage"]) and math.isnan(none["min_cross_section_fill"])


def test_bone_implant_contact():
    imp = np.zeros((20, 20, 20), bool)
    imp[5:15, 5:15, 5:15] = True
    bone = np.zeros_like(imp)
    bone[5:15, 5:15, 15:17] = True               # bone touching one face only
    r = bone_implant_contact(imp, bone, (10.0, 10.0, 10.0))
    assert 0 < r["BIC"] < 0.35 and r["contact_margin_um"] == 10.0
    assert bone_implant_contact(imp, ~imp, (10.0,) * 3)["BIC"] == 1.0
    assert math.isnan(bone_implant_contact(np.zeros_like(imp), bone, (1, 1, 1))["BIC"])


def test_density_stats_erosion_and_fallback():
    d = np.full((7, 7, 7), 5.0, np.float32)
    d[3, 3, 3] = 50.0
    v = Volume(d, (10, 10, 10))
    m = np.zeros((7, 7, 7), bool)
    m[2:5, 2:5, 2:5] = True
    s = density_stats(v, m, erode_vox=1)
    assert s["n_vox"] == 1 and s["mean"] == 50.0
    tiny = np.zeros_like(m)
    tiny[0, 0, 0] = True                          # erodes to nothing -> falls back to the mask
    assert density_stats(v, tiny)["n_vox"] == 1


def test_defect_report_metrics_iso_and_anisotropic():
    rng = np.random.default_rng(0)
    lab = np.zeros((16, 16, 16), np.uint8)
    lab[2:14, 4:12, 4:12] = rng.choice([0, 1, 2], size=(12, 8, 8), p=[0.5, 0.3, 0.2])
    lab[:2] = 3
    lab[14:] = 3
    roi = np.zeros_like(lab, bool)
    roi[2:14, 3:13, 3:13] = True
    vol = Volume(rng.normal(100, 5, lab.shape).astype(np.float32), (20.0, 20.0, 20.0))
    r = defect_report_metrics(lab, roi, vol)
    assert r["new_bone_architecture"]["BV_TV"] == pytest.approx(((lab == 1) & roi).sum() / roi.sum())
    assert set(r["density"]) == {"new_bone", "residual_graft", "host_bone"}
    assert r["bridging_all_mineral"]["connected_bridge"] in (True, False)
    aniso = Volume(vol.data, (20.0, 20.0, 40.0))
    r2 = defect_report_metrics(lab, roi, aniso, thickness=False)
    assert "note" in r2["new_bone_architecture"]
    assert r2["class_volumes"]["TV_mm3"] == pytest.approx(2 * r["class_volumes"]["TV_mm3"])
