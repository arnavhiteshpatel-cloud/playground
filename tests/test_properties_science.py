"""Property-based invariants of the scientific code (hypothesis) and QC robustness on degenerate scans."""
import math
import warnings

import numpy as np
import pytest
from hypothesis import assume, given
from hypothesis import strategies as hst
from hypothesis.extra import numpy as hnp

from osteoquant.morphometry.core import (class_volumes, euler_connectivity, local_thickness, porosity,
                                         surface_area_mm2, volume_mm3)
from osteoquant.segment.metrics import binary_metrics, confusion
from osteoquant.stats.core import bland_altman, hedges_g, icc

masks = hnp.arrays(bool, hst.tuples(hst.integers(3, 9), hst.integers(3, 9), hst.integers(3, 9)))
labels = hnp.arrays(np.uint8, hst.tuples(hst.integers(2, 8), hst.integers(2, 8), hst.integers(2, 8)),
                    elements=hst.sampled_from([0, 1, 2, 3, 255]))
pos = hst.floats(0.5, 200.0, allow_nan=False)


# ----------------------------------------------------------------------------- morphometry
@given(m=masks, perm=hst.permutations([0, 1, 2]))
def test_thickness_is_invariant_to_axis_permutation(m, perm):
    a = np.sort(local_thickness(m, 2.0, border="background")[m])
    b = np.sort(local_thickness(np.transpose(m, perm), 2.0, border="background")[np.transpose(m, perm)])
    assert np.allclose(a, b)


@given(m=masks, shift=hst.tuples(hst.integers(0, 3), hst.integers(0, 3), hst.integers(0, 3)))
def test_thickness_and_topology_invariant_to_translation(m, shift):
    big = np.zeros(tuple(s + 6 for s in m.shape), bool)
    big[3:3 + m.shape[0], 3:3 + m.shape[1], 3:3 + m.shape[2]] = m
    moved = np.zeros_like(big)
    z, y, x = shift
    moved[z:z + m.shape[0], y:y + m.shape[1], x:x + m.shape[2]] = m
    t1 = np.sort(local_thickness(big, 1.0, border="background")[big])
    t2 = np.sort(local_thickness(moved, 1.0, border="background")[moved])
    assert np.allclose(t1, t2)
    assert euler_connectivity(big) == euler_connectivity(moved)


@given(m=masks, s=pos, k=hst.floats(0.5, 4.0))
def test_measures_scale_with_voxel_size(m, s, k):
    assert volume_mm3(m, (k * s,) * 3) == pytest.approx(k ** 3 * volume_mm3(m, (s,) * 3), rel=1e-9, abs=1e-30)
    assert surface_area_mm2(m, (k * s,) * 3) == pytest.approx(k ** 2 * surface_area_mm2(m, (s,) * 3), rel=1e-6,
                                                              abs=1e-30)
    assert np.allclose(local_thickness(m, k * s), k * local_thickness(m, s), rtol=1e-5)


@given(lab=labels, sp=hst.tuples(pos, pos, pos))
def test_class_volumes_partition_tv(lab, sp):
    roi = np.ones(lab.shape, bool)
    cv = class_volumes(lab, roi, sp)
    total = (cv["new_bone_volume_mm3"] + cv["residual_graft_volume_mm3"] + cv["host_bone_volume_mm3"]
             + cv["uncertain_volume_mm3"] + volume_mm3(lab == 0, sp))
    assert total == pytest.approx(cv["TV_mm3"], rel=1e-9)
    assert 0 <= cv["mineralized_fraction"] <= 1
    if cv["TV_certain_mm3"] > 0:
        s = sum(cv[f"{n}_fraction_of_certain"] for n in ("new_bone", "residual_graft", "host_bone"))
        assert 0 <= s <= 1 + 1e-9


@given(a=masks)
def test_porosity_complement(a):
    env = np.ones(a.shape, bool)
    assert porosity(a, env) == pytest.approx(1 - a.mean())


@given(m=masks)
def test_topology_is_additive_over_separated_copies(m):
    """Two copies separated by background: beta0, beta1, beta2 and chi all double."""
    e1 = euler_connectivity(m)
    two = np.zeros((m.shape[0] * 2 + 2,) + m.shape[1:], bool)
    two[: m.shape[0]] = m
    two[m.shape[0] + 2:] = m
    e2 = euler_connectivity(two)
    assert e2 == {k: 2 * v for k, v in e1.items()}


# ----------------------------------------------------------------------------- metrics / stats
@given(a=masks, data=hst.data())
def test_dice_symmetry_bounds_and_identity(a, data):
    b = data.draw(hnp.arrays(bool, a.shape))
    ab, ba = binary_metrics(a, b, distances=False), binary_metrics(b, a, distances=False)
    if a.any() or b.any():
        assert ab["dice"] == pytest.approx(ba["dice"]) and 0 <= ab["dice"] <= 1
        assert ab["iou"] == pytest.approx(ab["dice"] / (2 - ab["dice"]))
    if a.any():
        assert binary_metrics(a, a, distances=False)["dice"] == 1.0


@given(lab=labels, data=hst.data())
def test_confusion_total_counts(lab, data):
    pred = data.draw(hnp.arrays(np.uint8, lab.shape, elements=hst.sampled_from([0, 1, 2, 3, 255])))
    cm = confusion(pred, lab, (0, 1, 2, 3))
    ok = np.isin(pred, [0, 1, 2, 3]) & np.isin(lab, [0, 1, 2, 3])
    assert cm.sum() == ok.sum() and np.trace(cm) == (ok & (pred == lab)).sum()


finite = hst.floats(-1e3, 1e3, allow_nan=False, allow_infinity=False)


@given(Y=hnp.arrays(float, hst.tuples(hst.integers(3, 12), hst.integers(2, 5)), elements=finite),
       shift=finite, scale=hst.floats(0.1, 10))
def test_icc_affine_invariance(Y, shift, scale):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        a = icc(Y, "2,1")["icc"]
        b = icc(Y * scale + shift, "2,1")["icc"]
    assume(np.isfinite(a) and np.isfinite(b) and np.var(Y) > 1e-6)
    assert a == pytest.approx(b, abs=1e-6)
    assert a <= 1 + 1e-9


@given(a=hnp.arrays(float, hst.integers(3, 30), elements=finite), d=finite)
def test_bland_altman_constant_offset(a, d):
    r = bland_altman(a, a + d)
    assert r["bias"] == pytest.approx(d, abs=1e-6) and r["sd_diff"] == pytest.approx(0, abs=1e-6)
    assert r["loa_low"] <= r["bias"] <= r["loa_high"]


@given(a=hnp.arrays(float, hst.integers(2, 20), elements=finite),
       b=hnp.arrays(float, hst.integers(2, 20), elements=finite))
def test_hedges_g_antisymmetry(a, b):
    g1, g2 = hedges_g(a, b)["g"], hedges_g(b, a)["g"]
    if math.isnan(g1):
        assert math.isnan(g2)
    else:
        assert g1 == pytest.approx(-g2)


# ----------------------------------------------------------------------------- QC on degenerate scans (QA-020)
@pytest.mark.parametrize("name", ["zeros", "constant", "nan", "all_nan", "one_slice", "tiny", "binary"])
def test_qc_never_crashes_on_degenerate_volumes(name):
    from osteoquant.qc import run_qc
    from osteoquant.volume import Volume
    rng = np.random.default_rng(0)
    data = {
        "zeros": np.zeros((10, 20, 20), np.uint16),
        "constant": np.full((10, 20, 20), 5, np.float32),
        "nan": np.where(rng.random((10, 20, 20)) > 0.9, np.nan, rng.random((10, 20, 20))).astype(np.float32),
        "all_nan": np.full((3, 8, 8), np.nan, np.float32),
        "one_slice": rng.random((1, 30, 30)).astype(np.float32),
        "tiny": rng.random((2, 2, 2)).astype(np.float32),
        "binary": (rng.random((12, 24, 24)) > 0.5).astype(np.uint8),
    }[name]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        r = run_qc(Volume(data, (10, 10, 10)))
    ids = {c["id"]: c for c in r["checks"]}
    assert r["verdict"] in ("suitable", "review", "unsuitable")
    assert ids["QC-D10"]["status"] == ("fail" if "nan" in name else "pass")
    if name == "zeros":
        assert ids["QC-D06"]["status"] == "warn" and ids["QC-D06"]["value"] == 10
