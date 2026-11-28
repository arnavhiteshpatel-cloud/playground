"""Model registry / safe loading, inference runtimes, domain-randomised sampler and CT simulation."""
import json
import sys

import numpy as np
import pytest

torch = pytest.importorskip("torch")


@pytest.fixture
def model_dir(tmp_path, monkeypatch):
    import osteoquant.ml.train as T
    d = tmp_path / "models"
    d.mkdir()
    monkeypatch.setattr(T, "MODEL_DIR", d)
    try:
        import osteoquant.ml.core as MC
        monkeypatch.setattr(MC, "MODEL_DIR", d)
    except ImportError:  # pragma: no cover
        pass
    try:
        import osteoquant.ml.runtime as R
        monkeypatch.setattr(R, "MODEL_DIR", d)
    except ImportError:  # pragma: no cover
        pass
    return d


def _case(seed=0, shape=(16, 16, 16)):
    from osteoquant.ml.train import Case
    rng = np.random.default_rng(seed)
    lab = np.zeros(shape, np.uint8)
    lab[4:12, 4:12, 4:12] = 1
    lab[6:10, 6:10, 6:10] = 2
    img = (lab.astype(np.float32) * 800 + rng.normal(100, 20, shape)).astype(np.float32)
    roi = lab > 0
    return Case(f"c{seed}", img, lab, roi, (40.0, 40.0, 40.0), "synthetic", "allowed")


TINY = {"iters": 2, "patch": (16, 16, 16), "batch": 1, "base": 4, "levels": 2, "n_classes": 4, "threads": 1,
        "log_every": 1, "val_every": 1}


@pytest.fixture
def tiny_model(model_dir):
    # QA-022 resolved: the registry lock is portable (fcntl / msvcrt / mkdir), so Windows runs these tests too
    from osteoquant.ml.train import train_model
    card = train_model([_case(0)], [_case(1)], TINY, "tiny", log=lambda s: None)
    return card


def test_train_save_and_registry(tiny_model, model_dir):
    reg = json.loads((model_dir / "registry.json").read_text())
    assert reg["tiny"]["sha256"] == tiny_model["sha256"] and reg["tiny"]["licence_tag"] == "commercial_eligible"
    assert (model_dir / "tiny.card.json").exists() and tiny_model["history"][-1]["iter"] == 2


def test_load_model_verifies_hash_before_deserialising(tiny_model, model_dir):
    from osteoquant.ml.train import load_model, verify_model_lock
    m, ck = load_model("tiny")
    assert ck["sha256"] == tiny_model["sha256"] and not m.training
    assert verify_model_lock("tiny", tiny_model["sha256"]) and not verify_model_lock("tiny", "0" * 64)
    p = model_dir / "tiny.pt"
    p.write_bytes(p.read_bytes() + b"\0")                 # any byte change -> refused
    with pytest.raises(RuntimeError, match="registry"):
        load_model("tiny")
    for bad in ("../tiny", "a/b", "", "x" * 65, "tiny.pt"):
        with pytest.raises(ValueError):
            load_model(bad)
    with pytest.raises(FileNotFoundError):
        load_model("absent")


def test_load_model_refuses_pickled_code_even_if_registered(model_dir):
    """A registered (hash-matching) checkpoint that contains a pickled callable must still be rejected by
    torch.load(weights_only=True) — the registry is not trusted to vouch for code."""
    import hashlib
    import pickle

    from osteoquant.ml.train import load_model, update_registry
    marker = model_dir / "PWNED"

    class Evil:
        def __reduce__(self):
            return (open, (str(marker), "w"))
    p = model_dir / "evil.pt"
    torch.save({"state_dict": {}, "hparams": {}, "x": Evil()}, p, pickle_module=pickle)
    update_registry("evil", {"sha256": hashlib.sha256(p.read_bytes()).hexdigest()})
    with pytest.raises(pickle.UnpicklingError):
        load_model("evil")
    assert not marker.exists()


def test_predict_proba_is_a_distribution_and_tta(tiny_model):
    from osteoquant.ml.train import load_model, predict_proba
    m, ck = load_model("tiny")
    c = _case(2, (20, 18, 17))
    p = predict_proba(m, c, ck["cfg"], tta=False)
    assert p.shape == (4, 20, 18, 17) and np.allclose(p.sum(0), 1, atol=1e-4)
    pt = predict_proba(m, c, ck["cfg"], tta=True, mc_dropout=2)
    assert np.allclose(pt.sum(0), 1, atol=1e-4)


def test_licence_guard_and_finetune_provenance(tiny_model, model_dir):
    from osteoquant.ml.train import Case, train_model
    rc = _case(3)
    rc = Case("r", rc.image, rc.labels, rc.roi, rc.spacing, provenance="public-nc", commercial_use="research_only")
    with pytest.raises(PermissionError):
        train_model([rc], [], {**TINY, "require_commercial_eligible": True}, "x", log=lambda s: None)
    card = train_model([rc], [], {**TINY, "roi_channel": True, "roi_distance_channel": True}, "ft",
                       log=lambda s: None)
    assert card["licence_tag"] == "research_only"
    child = train_model([_case(4)], [], {**TINY, "roi_channel": True, "roi_distance_channel": True}, "child",
                        log=lambda s: None, init_from=str(model_dir / "ft.pt"))
    assert child["licence_tag"] == "research_only" and child["parent_model"]["name"] == "ft"


def test_normalisation_and_augmentation_helpers():
    from osteoquant.ml.train import _gauss_window, _pad_to, augment, normalize_image, sample_patch
    x = np.arange(1000, dtype=np.float32).reshape(10, 10, 10)
    n = normalize_image(x)
    assert n.min() < 0.05 and n.max() > 0.95
    z = normalize_image(x, mode="zscore")
    assert abs(z.mean()) < 0.1
    with pytest.raises(ValueError):
        normalize_image(x, mode="bogus")
    rng = np.random.default_rng(0)
    xi, yi = augment(x[None].copy(), (x > 500).astype(np.int64), rng, {})
    assert xi.shape == (1, 10, 10, 10) and yi.shape == (10, 10, 10)
    xp, yp = sample_patch(x[None], np.zeros((10, 10, 10), np.int64), x > 500, (4, 4, 4), rng, fg_prob=1.0)
    assert xp.shape == (1, 4, 4, 4)
    xq, yq = _pad_to(xp, yp, (6, 6, 6))
    assert xq.shape == (1, 6, 6, 6) and (yq[4:] == 255).all()
    w = _gauss_window((5, 5, 5))
    assert w.max() == pytest.approx(1.001, abs=1e-3) and w[2, 2, 2] == w.max()


def test_update_registry_works_without_fcntl(model_dir, monkeypatch):
    from osteoquant.ml.train import update_registry
    monkeypatch.setitem(sys.modules, "fcntl", None)       # what a Windows interpreter looks like (QA-022 fixed)
    monkeypatch.setitem(sys.modules, "msvcrt", None)      # and a platform with neither: mkdir lock fallback
    update_registry("m", {"sha256": "0" * 64})
    assert json.loads((model_dir / "registry.json").read_text())["m"]["sha256"] == "0" * 64


def test_onnx_runtime_matches_torch_and_verifies_hash(tiny_model, model_dir):
    pytest.importorskip("onnxruntime")
    pytest.importorskip("onnx")
    from osteoquant.ml.runtime import OnnxSegmenter, export_onnx
    from osteoquant.ml.train import load_model, predict_proba
    info = export_onnx("tiny", patch=(16, 16, 16))
    seg = OnnxSegmenter("tiny", threads=1)
    c = _case(5)
    m, ck = load_model("tiny")
    p_t = predict_proba(m, c, ck["cfg"], tta=False, patch=(16, 16, 16))
    p_o = seg.predict_proba(c)
    assert np.allclose(p_t, p_o, atol=1e-4)
    (model_dir / "tiny.onnx").write_bytes((model_dir / "tiny.onnx").read_bytes() + b"\0")
    with pytest.raises(RuntimeError, match="hash"):
        OnnxSegmenter("tiny")
    with pytest.raises(ValueError):
        OnnxSegmenter("../x")
    assert len(info["sha256"]) == 64


def test_onnx_small_volume_is_padded_and_int8_quantisation_registers(tiny_model, model_dir):
    pytest.importorskip("onnxruntime")
    pytest.importorskip("onnx")
    from osteoquant.ml.runtime import OnnxSegmenter, export_onnx, quantize_int8_static
    export_onnx("tiny", patch=(16, 16, 16))
    seg = OnnxSegmenter("tiny", threads=1)
    small = _case(7, shape=(10, 12, 16))                  # smaller than the patch in two axes: edge padding path
    p = seg.predict_proba(small)
    assert p.shape == (4, 10, 12, 16) and np.allclose(p.sum(0), 1, atol=1e-4)
    q = quantize_int8_static("tiny", [_case(0), _case(1)], n_patches=4)
    reg = json.loads((model_dir / "registry.json").read_text())
    assert reg["tiny"]["onnx_int8_sha256"] == q["sha256"] and (model_dir / "tiny.int8.onnx").exists()


# ----------------------------------------------------------------------------- synthetic data
def test_domain_randomised_sampler_shapes_and_determinism():
    from osteoquant.ml.synth_dr import DRConfig, DRSampler
    fr = np.zeros((4, 24, 24, 24), np.uint8)
    fr[0] = 255
    fr[0, 8:16] = 0
    fr[1, 8:16] = 255
    s = DRSampler([fr], DRConfig(patch=(12, 12, 12)))
    x1, y1 = s(np.random.default_rng(7))
    x2, y2 = s(np.random.default_rng(7))
    assert x1.shape == (1, 12, 12, 12) and y1.shape == (12, 12, 12)
    assert np.array_equal(x1, x2) and np.array_equal(y1, y2) and np.isfinite(x1).all()
    s2 = DRSampler([fr], DRConfig(patch=(12, 12, 12), target="classes"))
    _, y3 = s2(np.random.default_rng(1))
    assert set(np.unique(y3)) <= {0, 1, 2, 3}


def test_ct_spectrum_beam_hardening_and_simulation():
    from osteoquant.phantom.ctsim import CTConfig, effective_energy, simulate_ct, spectrum
    E, w = spectrum(80, 0.5, 12)
    assert w.sum() == pytest.approx(1.0) and E.min() >= 10 and E.max() < 80
    assert effective_energy(80, 2.0) > effective_energy(80, 0.0)          # filtration hardens the beam
    assert effective_energy(100, 0.5) > effective_energy(60, 0.5)
    from osteoquant.phantom import PhantomConfig, generate_phantom
    ph = generate_phantom(PhantomConfig(model="condyle", shape=(12, 40, 40), voxel_um=40, supersample=1,
                                        defect_diameter_um=600, seed=1))
    cfg = CTConfig(n_angles=60, n_energy_bins=4, slices=(4, 6), ring_gain_sd=0.01, scatter_fraction=0.02,
                   bh_correction=True)
    v = simulate_ct(ph.material_fractions, ph.materials, 40.0, cfg)
    assert v.shape[0] == 2 and np.isfinite(v.data).all()


def test_render_fast_downsample_labels_and_missing_region():
    from osteoquant.phantom.imaging import ImagingConfig, downsample_labels, missing_region, render_fast
    mu = np.zeros((8, 16, 16), np.float32)
    mu[2:6, 4:12, 4:12] = 2.0
    v = render_fast(mu, 20.0, ImagingConfig(psf_sigma_um=10, noise_sigma=0.0, seed=0))
    assert v.shape == mu.shape and v.data[4, 8, 8] > v.data[0, 0, 0]
    lab = np.zeros((4, 4, 4), np.uint8)
    lab[:2] = 1
    lab[0, 0, 0] = 2
    d = downsample_labels(lab, 2)
    assert d.shape == (2, 2, 2) and (d[0] == 1).all() and (d[1] == 0).all()
    assert downsample_labels(lab, 1) is lab
    from osteoquant.volume import Volume
    out, m = missing_region(Volume(np.ones((20, 4, 4)), (1, 1, 1)), 0.2)
    assert m.sum() == 4 * 16 and (out.data[m] == 0).all() and (out.data[~m] == 1).all()


# ----------------------------------------------------------------------------- pipeline model paths
def _vol():
    from osteoquant.volume import Volume
    c = _case(6, (16, 16, 16))
    return Volume(c.image, (40.0, 40.0, 40.0)), c.roi


def test_pipeline_unet_and_onnx_paths_record_model_identity(tiny_model, model_dir):
    from osteoquant.pipeline import analyze, segment
    v, roi = _vol()
    lab, p, info = segment(v, roi, {"segmentation": "unet:tiny", "tta": False})
    assert info["model_sha256"] == tiny_model["sha256"] and p.shape[0] == 4 and lab.shape == v.shape
    with pytest.raises(RuntimeError, match="mismatch"):
        segment(v, roi, {"segmentation": "unet:tiny", "expected_model_sha256": "0" * 64})
    roi_def = {"kind": "box", "params": {"min_um": [0, 0, 0], "max_um": [1e6, 1e6, 1e6]}}
    r = analyze(v, {"segmentation": "unet:tiny", "tta": False, "qc": False, "no_graft": True,
                    "thickness_metrics": False, "measurement_support": False}, roi_dict=roi_def)
    assert r["segmentation"]["no_graft"] and not (r["_labels"] == 2).any()
    assert 0 <= r["uncertainty"]["abstained_frac_roi"] <= 1 and r["status"] == "complete_unreviewed"
    pytest.importorskip("onnxruntime")
    pytest.importorskip("onnx")
    from osteoquant.ml.runtime import export_onnx
    export_onnx("tiny", patch=(16, 16, 16))
    lab2, p2, info2 = segment(v, roi, {"segmentation": "onnx:tiny", "threads": 1})
    assert info2["runtime"] == "onnxruntime" and info2["onnx_sha256"] and np.allclose(p2.sum(0), 1, atol=1e-4)


def test_pipeline_rf_requires_trusted_local_flag(tmp_path):
    joblib = pytest.importorskip("joblib")
    from osteoquant.pipeline import segment
    from osteoquant.segment.classical import RFSegmenter
    v, roi = _vol()
    lab = np.zeros(v.shape, np.uint8)
    lab[v.data > 500] = 1
    rf = RFSegmenter(n_estimators=5, max_depth=4, scales_um=(0,), feature_set="full")
    rf.fit([v.data], [lab], [v.spacing], [roi], n_per_class=200)
    p = tmp_path / "rf.joblib"
    joblib.dump(rf, p)
    with pytest.raises(PermissionError):
        segment(v, roi, {"segmentation": f"rf:{p}"})
    out, prob, info = segment(v, roi, {"segmentation": f"rf:{p}", "_trusted_local": True})
    assert prob.shape == (4,) + v.shape and (out == lab).mean() > 0.9


def test_case_default_licence_is_unclear_and_blocks_commercial_training(model_dir):
    from osteoquant.ml.train import Case, train_model
    c = _case(7)
    unclear = Case("u", c.image, c.labels, c.roi, c.spacing)
    assert unclear.commercial_use == "unclear"
    with pytest.raises(PermissionError):
        train_model([unclear], [], {**TINY, "require_commercial_eligible": True}, "u", log=lambda s: None)
