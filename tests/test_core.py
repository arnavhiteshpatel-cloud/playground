"""Core scientific and I/O tests (fast; run with `pytest -q`)."""
import numpy as np
import pytest

from osteoquant.volume import Volume
from osteoquant import io as oio
from osteoquant.morphometry import (trabecular_morphometry, local_thickness, euler_connectivity,
                                    volume_mm3, surface_area_mm2, class_volumes, bridging)
from osteoquant.morphometry.analytic import plates, sphere, torus_count_phantom, hollow_cylinder
from osteoquant.stats import icc, bland_altman, adjust_pvalues, hedges_g, describe
from osteoquant.segment.metrics import binary_metrics, multiclass_metrics
from osteoquant.roi import cylinder_roi, cylinder_from_landmarks, ROI


# ------------------------------------------------------------------ volume
def test_volume_rejects_bad_spacing():
    with pytest.raises(ValueError):
        Volume(np.zeros((2, 2, 2)), (0, 1, 1))
    with pytest.raises(ValueError):
        Volume(np.zeros((2, 2)), (1, 1, 1))


def test_index_physical_roundtrip():
    v = Volume(np.zeros((4, 5, 6)), (10, 20, 30), origin=(1, 2, 3))
    p = v.index_to_physical([1, 2, 3])
    assert np.allclose(p, [11, 42, 93])
    assert np.allclose(v.physical_to_index(p), [1, 2, 3])


def test_content_hash_changes_with_spacing():
    a = np.arange(27, dtype=np.uint16).reshape(3, 3, 3)
    assert Volume(a, (1, 1, 1)).content_hash() != Volume(a, (2, 2, 2)).content_hash()


# ------------------------------------------------------------------ IO roundtrips
@pytest.fixture
def vol():
    rng = np.random.default_rng(0)
    return Volume(rng.integers(0, 4000, (12, 16, 20)).astype(np.uint16), (10.0, 12.0, 14.0))


def test_nifti_roundtrip(tmp_path, vol):
    p = tmp_path / "a.nii.gz"
    oio.write_nifti(vol, p)
    v2, rep = oio.read_volume(p)
    assert v2.shape == vol.shape and np.array_equal(v2.data, vol.data)
    assert np.allclose(v2.spacing, vol.spacing, rtol=1e-5)


def test_nrrd_roundtrip(tmp_path, vol):
    p = tmp_path / "a.nrrd"
    oio.write_nrrd(vol, p)
    v2, _ = oio.read_volume(p)
    assert np.array_equal(v2.data, vol.data) and np.allclose(v2.spacing, vol.spacing, rtol=1e-5)


def test_zarr_roundtrip_and_slabs(tmp_path, vol):
    p = tmp_path / "a.zarr"
    h = oio.write_zarr(vol, p, chunks=(4, 8, 8))
    v2, rep = oio.read_volume(p)
    assert np.array_equal(v2.data, vol.data) and v2.content_hash() == h
    tot = sum(s.shape[0] for _, _, s, _ in oio.iter_slabs(p, slab=5))
    assert tot == vol.shape[0]


def test_tiff_stack_missing_slice_detection(tmp_path, vol):
    d = tmp_path / "stack"
    oio.write_tiff_stack(vol, d)
    (d / "slice_00005.tif").unlink()
    v2, rep = oio.read_volume(d, spacing_um=10)
    assert rep.missing_slices == [5]
    assert any("missing" in w for w in rep.warnings)


def test_tiff_without_spacing_warns(tmp_path, vol):
    import tifffile
    p = tmp_path / "raw.tif"
    tifffile.imwrite(p, vol.data)
    v2, rep = oio.read_volume(p)
    assert "spacing_um" in rep.metadata_assumed


def test_dicom_roundtrip(tmp_path, vol):
    d = tmp_path / "dcm"
    oio.write_dicom_series(vol, d)
    v2, rep = oio.read_volume(d)
    assert v2.shape == vol.shape
    assert np.allclose(v2.spacing, vol.spacing, rtol=1e-4)
    assert np.allclose(v2.data, vol.data, atol=1)


def test_decimation_scales_spacing(tmp_path, vol):
    p = tmp_path / "a.nii.gz"
    oio.write_nifti(vol, p)
    v2, rep = oio.read_volume(p, step=2)
    assert np.allclose(v2.spacing, [20, 24, 28], rtol=1e-5)


def test_resample_and_calibration():
    v = Volume(np.ones((10, 10, 10), np.float32), (20, 10, 10))
    r = oio.resample_to_spacing(v, 10)
    assert r.shape == (20, 10, 10) and r.meta["resampling"]
    cal = oio.fit_ha_calibration([1000, 3000], [250, 750])
    assert abs(cal["slope"] - 0.25) < 1e-9 and cal["r2"] == pytest.approx(1)
    c = oio.apply_calibration(v, cal["slope"], cal["intercept"])
    assert c.meta["intensity_unit"] == "mgHA/cm3"


# ------------------------------------------------------------------ morphometry (analytic truth)
@pytest.mark.parametrize("t,s", [(4, 8), (6, 10), (8, 12)])
def test_plate_thickness_and_bvtv(t, s):
    p = plates((80, 80, 80), t, s)
    th = local_thickness(p, 1.0)
    sl = (slice(20, -20),) * 3
    assert th[sl][p[sl]].mean() == pytest.approx(t, abs=0.01)
    r = trabecular_morphometry(p, np.ones_like(p), 1.0, compute_thickness=False, compute_conn=False)
    assert r["BV_TV"] == pytest.approx(t / (t + s), abs=0.02)


def test_sphere_volume_and_surface():
    m = sphere((50, 50, 50), (24.5, 24.5, 24.5), 20)
    assert volume_mm3(m, (1000,) * 3) == pytest.approx(4 / 3 * np.pi * 20 ** 3, rel=0.01)
    assert surface_area_mm2(m, (1000,) * 3) == pytest.approx(4 * np.pi * 400, rel=0.12)


@pytest.mark.parametrize("n", [0, 1, 4])
def test_connectivity_exact(n):
    assert euler_connectivity(torus_count_phantom((30, 40, 60), n))["beta1"] == n


def test_cavity_counted():
    m = np.ones((20, 20, 20), bool)
    m[8:12, 8:12, 8:12] = False
    e = euler_connectivity(m)
    assert e["beta2"] == 1 and e["beta1"] == 0


def test_class_volumes_and_bridging():
    lab = np.zeros((10, 10, 10), np.uint8)
    lab[:, :5] = 1
    roi = np.ones_like(lab, bool)
    cv = class_volumes(lab, roi, (1000, 1000, 1000))
    assert cv["new_bone_fraction"] == pytest.approx(0.5)
    b = bridging(lab == 1, roi, axis=0)
    assert b["projected_coverage"] == pytest.approx(0.5)


# ------------------------------------------------------------------ stats (published reference)
def test_icc_shrout_fleiss():
    Y = [[9, 2, 5, 8], [6, 1, 3, 2], [8, 4, 6, 8], [7, 1, 2, 6], [10, 5, 6, 9], [6, 2, 4, 7]]
    assert icc(Y, "1,1")["icc"] == pytest.approx(0.17, abs=0.01)
    assert icc(Y, "2,1")["icc"] == pytest.approx(0.29, abs=0.01)
    assert icc(Y, "3,1")["icc"] == pytest.approx(0.71, abs=0.01)
    assert icc(Y, "2,k")["icc"] == pytest.approx(0.62, abs=0.01)
    assert icc(Y, "3,k")["icc"] == pytest.approx(0.91, abs=0.01)


def test_bland_altman_known():
    a = np.arange(10.0)
    ba = bland_altman(a, a + 2)
    assert ba["bias"] == pytest.approx(2) and ba["sd_diff"] == pytest.approx(0)


def test_pvalue_adjustment():
    assert adjust_pvalues([0.01, 0.04, 0.03, 0.2], "holm") == pytest.approx([0.04, 0.09, 0.09, 0.2])


def test_hedges_g_sign():
    assert hedges_g([3, 4, 5, 6], [1, 2, 3, 4])["g"] > 0


def test_describe_ci_contains_mean():
    d = describe([1, 2, 3, 4, 5])
    assert d["ci95_low"] < 3 < d["ci95_high"]


# ------------------------------------------------------------------ metrics
def test_dice_perfect_and_disjoint():
    a = np.zeros((10, 10, 10), bool)
    a[2:5] = True
    assert binary_metrics(a, a)["dice"] == 1.0
    b = np.zeros_like(a)
    b[6:8] = True
    assert binary_metrics(a, b, distances=False)["dice"] == 0.0


def test_hd95_shift():
    a = np.zeros((20, 20, 20), bool)
    a[5:15, 5:15, 5:15] = True
    b = np.roll(a, 2, axis=0)
    m = binary_metrics(a, b, spacing=(10, 10, 10))
    assert m["hd95_um"] == pytest.approx(20, abs=1e-6)


def test_abstain_excluded():
    t = np.ones((4, 4, 4), np.uint8)
    p = t.copy()
    p[0] = 255
    r = multiclass_metrics(p, t, classes=(1,), distances=False)
    assert r["coverage"] == pytest.approx(0.75)
    assert r["per_class"]["new_bone"]["dice"] == 1.0


# ------------------------------------------------------------------ ROI
def test_cylinder_roi_volume_and_hash():
    roi = cylinder_roi((500, 1000, 1000), (1, 0, 0), 400, (-300, 300))
    m = roi.to_mask((50, 100, 100), (20, 20, 20))
    vol = m.sum() * 20 ** 3
    assert vol == pytest.approx(np.pi * 400 ** 2 * 600, rel=0.05)
    h = roi.definition_hash()
    assert ROI.from_dict(roi.to_dict()).definition_hash() == h
    r2 = roi.revise({"radius_um": 420}, "analyst1", "edge alignment")
    assert r2.definition_hash() != h and r2.history[-1]["user"] == "analyst1"


def test_landmark_cylinder_oblique():
    roi = cylinder_from_landmarks((0, 0, 0), (300, 400, 0), 100)
    assert np.allclose(roi.params["axis"], [0.6, 0.8, 0])
