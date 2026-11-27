"""Segmentation agreement metrics: edge cases, anisotropic distances, abstention, calibration."""
import math

import numpy as np
import pytest

from osteoquant.segment.metrics import (ABSTAIN, binary_metrics, confusion, expected_calibration_error,
                                        multiclass_metrics, surface_distances)


def cube(shape=(12, 12, 12), lo=3, hi=7):
    m = np.zeros(shape, bool)
    m[lo:hi, lo:hi, lo:hi] = True
    return m


def test_dice_known_values():
    a = np.zeros(10, bool)
    b = np.zeros(10, bool)
    a[:4] = True
    b[2:6] = True                         # tp=2 fp=2 fn=2
    r = binary_metrics(a.reshape(1, 1, 10), b.reshape(1, 1, 10), distances=False)
    assert r["dice"] == pytest.approx(0.5) and r["iou"] == pytest.approx(1 / 3)
    assert r["precision"] == pytest.approx(0.5) and r["recall"] == pytest.approx(0.5)
    assert r["volume_error_rel"] == 0.0 and "hd95_um" not in r


def test_identical_masks_are_perfect():
    a = cube()
    r = binary_metrics(a, a, spacing=(5, 5, 5))
    assert r["dice"] == 1.0 and r["iou"] == 1.0 and r["hd95_um"] == 0.0 and r["assd_um"] == 0.0


def test_empty_mask_conventions():
    a = cube()
    z = np.zeros_like(a)
    both = binary_metrics(z, z)
    assert math.isnan(both["dice"]) and math.isnan(both["hd95_um"])      # documented: NaN, not 1
    fp = binary_metrics(a, z)
    assert fp["dice"] == 0.0 and math.isnan(fp["recall"]) and math.isnan(fp["volume_error_rel"])
    fn = binary_metrics(z, a)
    assert fn["dice"] == 0.0 and math.isnan(fn["precision"]) and fn["volume_error_rel"] == -1.0
    d1, d2 = surface_distances(a, z, (1, 1, 1))
    assert np.isinf(d1).all() and np.isinf(d2).all()


def test_shift_distance_respects_anisotropic_spacing():
    a = cube((16, 16, 16), 4, 9)
    for axis, sp in ((0, (10.0, 1.0, 1.0)), (2, (1.0, 1.0, 7.0))):
        b = np.roll(a, 2, axis=axis)
        r = binary_metrics(a, b, spacing=sp)
        assert r["hd95_um"] == pytest.approx(2 * sp[axis])
        assert 0 < r["assd_um"] <= 2 * sp[axis]


def test_metric_symmetry():
    rng = np.random.default_rng(0)
    a = rng.random((10, 10, 10)) > 0.6
    b = rng.random((10, 10, 10)) > 0.5
    ab, ba = binary_metrics(a, b, (2, 3, 4)), binary_metrics(b, a, (2, 3, 4))
    for k in ("dice", "iou", "hd95_um", "assd_um"):
        assert ab[k] == pytest.approx(ba[k])
    assert ab["precision"] == pytest.approx(ba["recall"])


def test_confusion_matrix_rows_truth_cols_pred_and_mask():
    t = np.array([0, 0, 1, 1, 2, 2])
    p = np.array([0, 1, 1, 1, 2, 0])
    cm = confusion(p, t, (0, 1, 2))
    assert cm.tolist() == [[1, 1, 0], [0, 2, 0], [1, 0, 1]]
    m = np.array([True, True, False, False, True, True])
    assert confusion(p, t, (0, 1, 2), m).sum() == 4


def test_confusion_handles_out_of_range_and_float_labels():
    # regression QA-015
    t = np.array([0, 1, 1, 255])
    assert confusion(np.array([0, 1, 300, 255]), t, (0, 1, 255)).tolist() == [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    assert confusion(np.array([0, 1, -1, 3]), t, (0, 1, 255)).sum() == 2   # -1 is NOT class 255
    assert confusion(np.array([0.0, 1.0, 1.0, 255.0]), t, (0, 1, 255)).trace() == 4


def test_multiclass_abstention_coverage_and_exclusion():
    t = np.zeros((4, 4, 4), np.uint8)
    t[:2] = 1
    t[2:3] = 2
    p = t.copy()
    p[0] = ABSTAIN                      # abstain on 16 voxels of class 1
    r = multiclass_metrics(p, t, classes=(1, 2, 3), distances=False)
    assert r["coverage"] == pytest.approx(1 - 16 / 64)
    assert r["per_class"]["new_bone"]["dice"] == 1.0           # abstained voxels excluded
    assert r["accuracy"] == 1.0
    r2 = multiclass_metrics(p, t, classes=(1, 2, 3), distances=False, ignore_abstain=False)
    assert r2["per_class"]["new_bone"]["dice"] < 1.0
    assert math.isnan(r["per_class"]["host_bone"]["dice"])     # class absent in both
    assert r["mean_dice"] == 1.0                               # NaN classes excluded from the mean


def test_multiclass_mask_and_names():
    t = np.zeros((6, 6, 6), np.uint8)
    t[1:5, 1:5, 1:5] = 1
    m = np.zeros_like(t, bool)
    r = multiclass_metrics(t, t, classes=(1,), mask=m, names={1: "x"})
    assert r["coverage"] == 1.0 and math.isnan(r["accuracy"]) and math.isnan(r["mean_dice"])
    assert "x" in r["per_class"]


def test_expected_calibration_error():
    truth = np.array([0, 0, 1, 1])
    perfect = np.array([[1.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 1.0]])
    assert expected_calibration_error(perfect, truth)["ece"] == 0.0
    over = np.array([[0.9, 0.9, 0.9, 0.9], [0.1, 0.1, 0.1, 0.1]])   # always says class 0 with 0.9
    r = expected_calibration_error(over, truth, n_bins=10)
    assert r["ece"] == pytest.approx(0.4) and r["bins"][0]["n"] == 4
    m = np.array([True, True, False, False])
    assert expected_calibration_error(over, truth, mask=m)["ece"] == pytest.approx(0.1)
