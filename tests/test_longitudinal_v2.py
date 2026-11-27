import numpy as np
import pytest
from scipy import ndimage as ndi

from osteoquant.longitudinal import apply_rigid, propagate_roi, registration_qc, track_granules
from osteoquant.phantom import PhantomConfig, generate_phantom

SP = (40.0, 40.0, 40.0)


def _scene(seed=0, shape=(40, 48, 48)):
    rng = np.random.default_rng(seed)
    img = rng.normal(100, 8, shape).astype(np.float32)
    zz, yy, xx = np.indices(shape)
    host = ((yy - 24) ** 2 + (xx - 24) ** 2 > 18 ** 2)
    img[host] += 900
    granules = np.zeros(shape, bool)
    for c in ((12, 20, 20), (20, 28, 22), (28, 20, 28)):
        granules |= ((zz - c[0]) ** 2 + (yy - c[1]) ** 2 + (xx - c[2]) ** 2) <= 9
    img[granules] += 1500
    roi = ~host & (zz > 4) & (zz < 36)
    return img, granules, roi


def test_registration_qc_passes_aligned_and_flags_shift():
    img, _, roi = _scene()
    noisy = img + np.random.default_rng(1).normal(0, 8, img.shape).astype(np.float32)
    ok = registration_qc(img, noisy, exclude=roi, spacing_um=SP)
    assert ok["pass"] and ok["residual_shift_um_max"] < 20
    shifted, _ = apply_rigid(noisy, SP, (0, 0, 0), (0, 200, 200))
    bad = registration_qc(img, shifted, exclude=roi, spacing_um=SP)
    assert bad["residual_shift_um_max"] == pytest.approx(np.hypot(200, 200), rel=0.15)
    assert not bad["pass"]


def test_track_granules_recovers_known_shift():
    img, gran, roi = _scene()
    later = ndi.shift(img, (0, 3, -2), order=0, mode="nearest")
    tr = track_granules(img, later, gran, SP, search_um=200)
    assert tr["summary"]["n_tracked"] == tr["summary"]["n_components"] >= 2
    for r in tr["components"]:
        if r.get("tracked"):
            assert r["shift_um"] == pytest.approx([0.0, 120.0, -80.0])
    moved_truth = ndi.shift(gran, (0, 3, -2), order=0)
    inter = (tr["footprint"] & moved_truth).sum()
    assert 2 * inter / (tr["footprint"].sum() + moved_truth.sum()) > 0.95


def test_track_granules_reports_untracked_when_graft_disappears():
    img, gran, roi = _scene()
    later = img.copy()
    later[gran] = 100.0          # fully resorbed → nothing to match
    tr = track_granules(img, later, gran, SP, search_um=120, min_score=0.6)
    assert tr["summary"]["untracked_volume_fraction"] > 0.5


def test_propagate_roi_after_motion():
    img, _, roi = _scene(shape=(48, 56, 56))
    moved, tx = apply_rigid(img, SP, (2, 0, 0), (0, 80, -40))
    truth, _ = apply_rigid(roi.astype(np.uint8), SP, (2, 0, 0), (0, 80, -40), labels=True)
    pr = propagate_roi(img, roi, moved, SP)
    t = truth > 0
    d = 2 * (pr["roi"] & t).sum() / (pr["roi"].sum() + t.sum())
    assert d > 0.9
    assert pr["qc"]["pass"]


def test_generator_v2_defaults_unchanged_and_motion_recorded():
    kw = dict(model="condyle", shape=(32, 40, 40), voxel_um=40, defect_diameter_um=1200, graft_material="ha",
              healing_stage=0.3, seed=5, supersample=1)
    a = generate_phantom(PhantomConfig(**kw))
    b = generate_phantom(PhantomConfig(**kw))
    assert np.array_equal(a.labels, b.labels)
    assert a.truth["graft_motion"] == {}
    c = generate_phantom(PhantomConfig(granule_displacement_um=120, fragment_prob=0.5, **kw))
    m = c.truth["graft_motion"]
    assert m["n_pieces"] >= 1
    assert m["max_shift_um"] <= 2 * 120 + 120 + 40      # displacement bound + fragment separation + rounding
    assert not np.array_equal(a.labels, c.labels)
    # host bone is untouched by graft motion
    assert np.array_equal(a.labels == 3, c.labels == 3)
