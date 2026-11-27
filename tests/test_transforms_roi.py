"""Spatial/intensity transforms and the ROI engine (definitions, rasterisation, detectors)."""
import math

import numpy as np
import pytest

from osteoquant.io.transforms import (apply_calibration, fit_ha_calibration, histogram_match, normalize_orientation,
                                      percentile_normalize, resample_to_spacing, to_isotropic)
from osteoquant.roi import ROI, cylinder_from_landmarks, cylinder_roi
from osteoquant.roi.engine import (ROIDetectionError, detect_plate_defect, detect_segmental_gap, kasa_circle_fit,
                                   roi_dice, roi_from_mask)
from osteoquant.volume import Volume


# ----------------------------------------------------------------------------- transforms
def test_resample_preserves_physical_extent_and_records_history():
    v = Volume(np.ones((10, 20, 30), np.float32), (20.0, 10.0, 10.0))
    r = resample_to_spacing(v, 10.0)
    assert r.shape == (20, 20, 30) and r.spacing == (10.0, 10.0, 10.0)
    assert r.meta["resampling"][-1]["from_um"] == [20.0, 10.0, 10.0]
    assert np.allclose(r.data, 1.0, atol=1e-6)


def test_resample_labels_nearest_keeps_label_set_and_dtype():
    lab = np.zeros((8, 8, 8), np.uint8)
    lab[2:6, 2:6, 2:6] = 3
    lab[3:5, 3:5, 3:5] = 1
    r = resample_to_spacing(Volume(lab, (10, 10, 10)), 5.0, labels=True)
    assert r.data.dtype == np.uint8 and set(np.unique(r.data)) <= {0, 1, 3}
    assert (r.data == 3).sum() == pytest.approx(8 * ((lab == 3).sum()), rel=0.2)


def test_downsampling_antialiases():
    rng = np.random.default_rng(0)
    v = Volume(rng.normal(0, 1, (32, 32, 32)).astype(np.float32), (1, 1, 1))
    r = resample_to_spacing(v, 4.0)
    assert r.shape == (8, 8, 8) and r.data.std() < 0.5        # prefilter suppresses noise


def test_to_isotropic_is_noop_for_isotropic():
    v = Volume(np.zeros((3, 3, 3)), (5, 5, 5))
    assert to_isotropic(v) is v
    assert to_isotropic(Volume(np.zeros((3, 6, 6)), (10, 5, 5))).spacing == (5.0, 5.0, 5.0)


def test_normalize_orientation_permutation_and_flip_preserve_geometry():
    rng = np.random.default_rng(1)
    data = rng.integers(0, 100, (3, 4, 5))
    D = np.array([[0, 0, -1], [1, 0, 0], [0, 1, 0]], float)   # index axes permuted + one flip
    v = Volume(data, (1.0, 2.0, 3.0), origin=(10.0, 20.0, 30.0), direction=D)
    n = normalize_orientation(v)
    assert np.allclose(n.direction, np.eye(3))
    for idx in [(0, 0, 0), (2, 3, 4), (1, 2, 3)]:
        p = v.index_to_physical(idx)
        j = np.round(n.physical_to_index(p)).astype(int)
        assert n.data[tuple(j)] == data[idx]
    with pytest.raises(ValueError):
        normalize_orientation(Volume(data, direction=np.array([[1, 1, 0], [1, 1, 0], [0, 0, 1]], float) / 1.4))


def test_percentile_normalize_and_histogram_match():
    x = np.linspace(0, 100, 1000).reshape(10, 10, 10)
    y, (a, b) = percentile_normalize(x, 0, 100)
    assert y.min() == pytest.approx(0) and y.max() == pytest.approx(1) and (a, b) == (0, 100)
    c, (a, b) = percentile_normalize(np.zeros((2, 2, 2)))
    assert b == a + 1                                     # constant input does not divide by zero
    ref = np.linspace(500, 600, 1000).reshape(10, 10, 10)
    m = histogram_match(x, ref)
    assert m.min() == pytest.approx(500, abs=1) and m.max() == pytest.approx(600, abs=1)


def test_ha_calibration_fit_and_apply():
    grey = [1000.0, 2000.0, 3000.0]
    ha = [0.0, 250.0, 500.0]
    cal = fit_ha_calibration(grey, ha)
    assert cal["slope"] == pytest.approx(0.25) and cal["intercept"] == pytest.approx(-250) and cal["r2"] == 1.0
    v = apply_calibration(Volume(np.full((2, 2, 2), 2000, np.uint16)), cal["slope"], cal["intercept"], source="P1")
    assert np.allclose(v.data, 250.0) and v.meta["calibration"]["source"] == "P1"
    assert v.meta["intensity_unit"] == "mgHA/cm3"
    with pytest.raises(ValueError):
        fit_ha_calibration([1.0], [2.0])
    assert fit_ha_calibration([1, 1], [5, 5])["r2"] == 1.0


# ----------------------------------------------------------------------------- ROI definitions
def test_cylinder_mask_volume_matches_analytic():
    roi = cylinder_roi((500, 500, 500), (1, 0, 0), 200, (-300, 300))
    m = roi.to_mask((100, 100, 100), (10, 10, 10))
    vox = m.sum() * 1000.0
    assert vox == pytest.approx(math.pi * 200 ** 2 * 600, rel=0.03)


def test_oblique_cylinder_and_axis_normalisation():
    a = cylinder_roi((250, 250, 250), (1, 1, 0), 60, (-100, 100)).to_mask((50, 50, 50), (10, 10, 10))
    b = cylinder_roi((250, 250, 250), (5, 5, 0), 60, (-100, 100)).to_mask((50, 50, 50), (10, 10, 10))
    assert np.array_equal(a, b) and a.sum() == pytest.approx(math.pi * 36 * 20, rel=0.08)


def test_sphere_and_box_and_origin():
    s = ROI("sphere", {"center_um": [50, 50, 50], "radius_um": 30}).to_mask((11, 11, 11), (10, 10, 10))
    assert s.sum() == pytest.approx(4 / 3 * math.pi * 27, rel=0.15)
    b = ROI("box", {"min_um": [0, 0, 0], "max_um": [20, 30, 40]}).to_mask((10, 10, 10), (10, 10, 10))
    assert b.sum() == 3 * 4 * 5
    shifted = ROI("box", {"min_um": [0, 0, 0], "max_um": [20, 30, 40]}).to_mask((10, 10, 10), (10, 10, 10),
                                                                                  origin=(-5, 0, 0))
    assert shifted.sum() == 2 * 4 * 5
    with pytest.raises(ValueError):
        ROI("torus", {}).to_mask((2, 2, 2), (1, 1, 1))


def test_roi_serialisation_hash_and_revision():
    r = cylinder_roi((1, 2, 3), (0, 0, 1), 5, (-1, 1))
    d = r.to_dict()
    r2 = ROI.from_dict(d)
    assert r2.definition_hash() == r.definition_hash() == d["definition_sha256"]
    rv = r.revise({"radius_um": 6.0}, "alice", "too small")
    assert rv.params["radius_um"] == 6.0 and r.params["radius_um"] == 5.0
    assert rv.history[-1]["previous"]["radius_um"] == 5.0 and rv.method.endswith("+manual-edit")
    assert rv.definition_hash() != r.definition_hash()


def test_landmarks_and_mask_rois():
    r = cylinder_from_landmarks((0, 50, 50), (100, 50, 50), 20)
    assert r.params["axis"] == [1.0, 0.0, 0.0] and r.params["extent_um"] == [-50.0, 50.0]
    with pytest.raises(ValueError):
        cylinder_from_landmarks((1, 1, 1), (1, 1, 1), 3)
    m = np.zeros((4, 4, 4), bool)
    m[1:3] = True
    mr = roi_from_mask(m)
    assert np.array_equal(mr.to_mask((4, 4, 4), (1, 1, 1)), m) and len(mr.params["mask_sha256"]) == 64
    assert roi_from_mask(m).params["mask_sha256"] != roi_from_mask(m.reshape(4, 16)).params["mask_sha256"]


def test_roi_dice_and_kasa_fit():
    a = np.zeros((5, 5), bool)
    a[:2] = True
    assert roi_dice(a, a) == 1.0 and math.isnan(roi_dice(~a & a, ~a & a))
    t = np.linspace(0, 2 * np.pi, 50, endpoint=False)
    cy, cx, r, rms = kasa_circle_fit(np.c_[10 + 7 * np.sin(t), -3 + 7 * np.cos(t)])
    assert (cy, cx, r) == pytest.approx((10, -3, 7)) and rms < 1e-9


# ----------------------------------------------------------------------------- detectors
def _plate_with_hole(shape=(40, 64, 64), sp=20.0, r_um=300.0, two_plates=False):
    img = np.full(shape, 200.0, np.float32)
    img[8:14] = 2000.0
    if two_plates:
        img[26:32] = 2000.0
    yy, xx = np.mgrid[: shape[1], : shape[2]]
    hole = (yy - 32) ** 2 + (xx - 30) ** 2 <= (r_um / sp) ** 2
    img[:, hole] = 200.0
    img += np.random.default_rng(0).normal(0, 20, shape).astype(np.float32)
    return img, (sp, sp, sp)


def test_detect_plate_defect_condyle_and_calvarial():
    img, sp = _plate_with_hole()
    roi = detect_plate_defect(img, sp, model="condyle", cortical_band_um=100)
    c = roi.params["center_um"]
    assert c[1] == pytest.approx(32 * 20, abs=40) and c[2] == pytest.approx(30 * 20, abs=40)
    assert roi.diagnostics["fit_radius_um"] == pytest.approx(300, rel=0.2)
    nom = detect_plate_defect(img, sp, model="condyle", nominal_diameter_um=600, cortical_band_um=100)
    assert nom.params["radius_um"] == 300.0 and 0 <= nom.confidence <= 1
    img2, sp = _plate_with_hole(two_plates=True)
    cal = detect_plate_defect(img2, sp, model="calvarial", cortical_band_um=100)
    assert cal.method == "auto-plate-calvarial" and cal.params["extent_um"][1] > cal.params["extent_um"][0]
    with pytest.raises(ValueError):
        detect_plate_defect(img, sp, model="nope")


def test_detect_plate_defect_intact_plate_raises():
    img = np.full((30, 48, 48), 200.0, np.float32)
    img[8:14] = 2000.0
    img += np.random.default_rng(0).normal(0, 20, img.shape).astype(np.float32)
    with pytest.raises(ROIDetectionError):
        detect_plate_defect(img, (20, 20, 20), cortical_band_um=100)


def _segmental(gap=(25, 39)):
    z, n = 64, 48
    img = np.full((z, n, n), 100.0, np.float32)
    yy, xx = np.mgrid[:n, :n]
    r = np.hypot(yy - 24, xx - 24)
    ring = (r <= 14) & (r >= 9)
    marrow = r < 9
    img[:, ring] = 2000.0
    img[:, marrow] = 600.0
    img[gap[0]:gap[1]] = 100.0
    img += np.random.default_rng(1).normal(0, 20, img.shape).astype(np.float32)
    return img


def test_detect_segmental_gap_finds_gap():
    roi = detect_segmental_gap(_segmental(), (40, 40, 40), min_gap_um=200)
    z0, z1 = roi.diagnostics["gap_slices"]
    assert abs(z0 - 25) <= 2 and abs(z1 - 38) <= 2
    assert roi.params["radius_um"] == pytest.approx(14 * 40, rel=0.25)
    with pytest.raises(ROIDetectionError):
        detect_segmental_gap(_segmental(), (40, 40, 40), min_gap_um=5000)
    with pytest.raises(ROIDetectionError):
        detect_segmental_gap(_segmental(gap=(0, 0)), (40, 40, 40))
