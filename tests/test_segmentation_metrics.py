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


# ----------------------------------------------------------------------------- mutation-testing follow-ups
def _brute_surface_distances(a, b, spacing):
    """Independent oracle: exhaustive point-to-point distances between surface voxels."""
    from scipy.spatial.distance import cdist

    def surf(m):
        er = np.zeros_like(m)
        inner = m[1:-1, 1:-1, 1:-1] & m[:-2, 1:-1, 1:-1] & m[2:, 1:-1, 1:-1] & m[1:-1, :-2, 1:-1] \
            & m[1:-1, 2:, 1:-1] & m[1:-1, 1:-1, :-2] & m[1:-1, 1:-1, 2:]
        er[1:-1, 1:-1, 1:-1] = inner
        return m & ~er                    # voxels on the array border are surface (border_value=0)
    pa = np.argwhere(surf(a)) * np.asarray(spacing)
    pb = np.argwhere(surf(b)) * np.asarray(spacing)
    D = cdist(pa, pb)
    return D.min(1), D.min(0)


def test_hd95_and_assd_match_brute_force_oracle_including_border_objects():
    rng = np.random.default_rng(4)
    for k in range(3):
        a = rng.random((9, 10, 11)) > 0.55
        b = rng.random((9, 10, 11)) > 0.6
        sp = (1.0, 2.0, 0.5 + k)
        r = binary_metrics(a, b, spacing=sp)
        d1, d2 = _brute_surface_distances(a, b, sp)
        assert r["hd95_um"] == pytest.approx(max(np.percentile(d1, 95), np.percentile(d2, 95)))
        assert r["assd_um"] == pytest.approx(np.concatenate([d1, d2]).mean())


def test_default_spacing_is_one_micrometre_per_voxel():
    a = cube((16, 16, 16), 4, 9)
    b = np.roll(a, 3, axis=1)
    assert binary_metrics(a, b)["hd95_um"] == pytest.approx(3.0)
    r = multiclass_metrics(b.astype(np.uint8), a.astype(np.uint8))
    assert set(r["per_class"]) == {"new_bone", "graft", "host_bone"}
    assert r["per_class"]["new_bone"]["hd95_um"] == pytest.approx(3.0)


def test_iou_when_false_positives_equal_true_positives():
    a = np.array([True, True, False, False]).reshape(1, 1, 4)
    b = np.array([True, False, False, False]).reshape(1, 1, 4)     # tp=1, fp=1, fn=0
    r = binary_metrics(a, b, distances=False)
    assert r["iou"] == pytest.approx(0.5) and r["dice"] == pytest.approx(2 / 3)


def test_multiclass_accuracy_counts_background_errors():
    t = np.zeros((4, 4, 4), np.uint8)
    t[0] = 1
    p = t.copy()
    p[1] = 1                                   # background predicted as new bone
    r = multiclass_metrics(p, t, distances=False)
    assert r["accuracy"] == pytest.approx(48 / 64)
    assert np.array(r["confusion"])[0, 1] == 16


def test_ece_per_bin_signs_do_not_cancel_and_bin_edges():
    truth = np.array([0, 0, 1, 1])
    # two under-confident correct voxels (conf 0.3 would be impossible for argmax with 2 classes, so use 3)
    prob = np.zeros((3, 4))
    prob[:, 0] = prob[:, 1] = [0.4, 0.3, 0.3]           # predict 0 with 0.4, correct
    prob[:, 2] = prob[:, 3] = [0.9, 0.05, 0.05]         # predict 0 with 0.9, wrong
    r = expected_calibration_error(prob, truth, n_bins=10)
    assert r["ece"] == pytest.approx(0.5 * 0.6 + 0.5 * 0.9)
    assert [b["bin"] for b in r["bins"]] == pytest.approx([0.4, 0.9])
    d = expected_calibration_error(prob, truth)               # default 15 bins
    assert d["bins"][0]["bin"] == pytest.approx(6 / 15)


@pytest.mark.parametrize("axis", [0, 1, 2])
def test_default_spacing_every_axis(axis):
    a = cube((16, 16, 16), 4, 9)
    b = np.roll(a, 2, axis=axis)
    assert binary_metrics(a, b)["hd95_um"] == pytest.approx(2.0)
    r = multiclass_metrics(b.astype(np.uint8), a.astype(np.uint8), classes=(1,))
    assert r["per_class"]["new_bone"]["hd95_um"] == pytest.approx(2.0)


@pytest.mark.parametrize("swap", [False, True])
def test_hd95_asymmetric_sets_match_oracle(swap):
    a = cube((20, 20, 20), 2, 18)                 # large object
    b = np.zeros_like(a)
    b[4:7, 4:7, 4:7] = True                        # small object in one corner
    if swap:
        a, b = b, a
    d1, d2 = _brute_surface_distances(a, b, (1.0, 1.0, 1.0))
    r = binary_metrics(a, b)
    assert r["hd95_um"] == pytest.approx(max(np.percentile(d1, 95), np.percentile(d2, 95)))
    assert r["hd95_um"] != pytest.approx(max(np.percentile(d1, 96), np.percentile(d2, 96)))
