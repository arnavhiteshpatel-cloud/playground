"""Functional tests of classical segmentation, uncertainty, longitudinal, histology, reports, the
CLI and the analysis pipeline (correctness on constructed inputs, not just execution)."""
import json
import math

import numpy as np
import pytest

from osteoquant.volume import Volume


# ----------------------------------------------------------------------------- classical segmentation
def _three_phase(seed=0):
    """Background 100, new bone 1000 (left half of ROI), graft 2500 (right half), host 1000 outside."""
    rng = np.random.default_rng(seed)
    x = np.full((20, 32, 32), 100.0, np.float32)
    roi = np.zeros(x.shape, bool)
    roi[4:16, 8:24, 8:24] = True
    truth = np.zeros(x.shape, np.uint8)
    nb = roi.copy()
    nb[:, :, 16:] = False
    nb[:, ::2] = False
    gr = roi.copy()
    gr[:, :, :16] = False
    gr[::2] = False
    host = np.zeros_like(roi)
    host[:, :4] = True
    x[nb | host] = 1000.0
    x[gr] = 2500.0
    truth[nb] = 1
    truth[gr] = 2
    truth[host] = 3
    return x + rng.normal(0, 30, x.shape).astype(np.float32), roi, truth


def test_compose_three_class_semantics():
    from osteoquant.segment.classical import compose_three_class
    mineral = np.array([True, True, True, False])
    graft = np.array([False, True, True, True])
    roi = np.array([True, True, False, True])
    assert compose_three_class(mineral, graft, roi).tolist() == [1, 2, 3, 0]


@pytest.mark.parametrize("method", ["multiotsu", "ctan", "kmeans", "gmm"])
def test_three_class_segmenters_recover_constructed_phases(method):
    from osteoquant.segment import classical as C
    from osteoquant.segment.metrics import multiclass_metrics
    x, roi, truth = _three_phase()
    if method == "multiotsu":
        lab, th = C.seg_multiotsu(x, roi)
        assert th["t_mineral"] < th["t_graft"]
    elif method == "ctan":
        lab = C.seg_ctan_style(x, roi, 500, 1800)
    elif method == "kmeans":
        lab, _ = C.seg_kmeans(x, roi)
    elif method == "gmm":
        lab, _ = C.seg_gmm(x, roi)
    m = multiclass_metrics(lab, truth, distances=False)
    assert m["per_class"]["new_bone"]["dice"] > 0.9 and m["per_class"]["graft"]["dice"] > 0.9
    assert m["per_class"]["host_bone"]["dice"] > 0.9


def test_shape_rule_separates_compact_granules_from_irregular_dense_bone():
    from osteoquant.segment.classical import seg_morphology
    x = np.full((30, 40, 40), 100.0, np.float32)
    zz, yy, xx = np.mgrid[:30, :40, :40]
    granule = (zz - 15) ** 2 + (yy - 12) ** 2 + (xx - 12) ** 2 <= 36       # compact sphere, r = 6 vox
    cross = np.zeros_like(granule)                                          # non-convex dense "cross"
    cross[13:17, 20:36, 26:30] = True
    cross[13:17, 26:30, 20:36] = True
    x[granule | cross] = 2500.0
    roi = np.ones(x.shape, bool)
    lab = seg_morphology(x, roi, (20, 20, 20), 500, 1800)
    assert (lab[granule] == 2).mean() > 0.9
    assert (lab[cross] == 1).mean() > 0.9                                   # low solidity -> new bone


def test_darker_graft_option():
    from osteoquant.segment import classical as C
    x, roi, truth = _three_phase()
    x2 = x.copy()
    x2[truth == 2] = 600.0                      # graft between background and bone
    lab = C.seg_ctan_style(x2, roi, 400, 800, graft_brighter=False)
    assert ((lab == 2) & (truth == 2)).sum() > 0.9 * (truth == 2).sum()


def test_binary_helpers():
    from osteoquant.segment import classical as C
    x, roi, truth = _three_phase()
    m, t = C.threshold_otsu(x)
    assert 100 < t < 2500 and m.sum() > 0
    assert np.array_equal(C.threshold_global(x, 500), x > 500)
    a = C.threshold_adaptive(x, 100, (10, 10, 10), offset=50)
    assert a.dtype == bool
    seeds = np.zeros_like(roi)
    seeds[0, 0, 0] = True                       # host bone corner
    g = C.region_grow(x, seeds, 500)
    assert g[truth == 3].all() and not g[0, 20, 20]
    blobs = np.zeros((10, 30, 30), bool)
    blobs[2:8, 3:11, 3:11] = True
    blobs[2:8, 10:18, 10:18] = True             # touching cubes
    inst = C.watershed_particles(blobs, (1, 1, 1), min_distance_um=3)
    assert len(np.unique(inst)) - 1 >= 2
    speck = np.zeros((10, 10, 10), bool)
    speck[0, 0, 0] = True
    speck[3:7, 3:7, 3:7] = True
    assert C.clean_binary(speck, 8).sum() == 64 and C.clean_binary(np.zeros_like(speck)).sum() == 0
    assert C.clean_binary(speck, 1, close_iter=1).sum() >= 64
    v = C.robust_values(np.r_[np.zeros(1000), np.arange(1.0, 101.0)])
    assert v.min() == 1.0 and C.robust_values(np.array([])).size == 0


def test_voxel_features_and_rf_segmenter():
    from osteoquant.segment.classical import RFSegmenter, voxel_features
    x, roi, truth = _three_phase()
    f, names = voxel_features(x, (10, 10, 10), roi)
    assert f.shape[0] == len(names) and f.shape[1:] == x.shape
    rf = RFSegmenter(n_estimators=10, max_depth=8, scales_um=(0, 20), feature_set="full")
    rf.fit([x], [truth], [(10, 10, 10)], [roi], n_per_class=300)
    lab, p = rf.predict(x, (10, 10, 10), roi)
    assert np.allclose(p.sum(0), 1, atol=1e-5) and (lab == truth).mean() > 0.9


# ----------------------------------------------------------------------------- uncertainty
def test_entropy_mi_abstain_and_plausibility():
    from osteoquant.uncertainty.core import (ABSTAIN, abstain, intensity_ood, mutual_information,
                                             plausibility_checks, predictive_entropy, risk_coverage,
                                             temperature_scale)
    p = np.zeros((4, 2, 1, 1), np.float32)
    p[:, 0] = 0.25                               # uniform -> entropy 1
    p[1, 1] = 1.0                                # certain -> entropy 0
    h = predictive_entropy(p)
    assert h[0, 0, 0] == pytest.approx(1.0) and h[1, 0, 0] == pytest.approx(0.0, abs=1e-6)
    lab = abstain(p, 0.5)
    assert lab[0, 0, 0] == ABSTAIN and lab[1, 0, 0] == 1
    assert abstain(p, 0.5, mask=np.zeros((2, 1, 1), bool))[0, 0, 0] != ABSTAIN
    a, b = np.zeros((2, 3)), np.zeros((2, 3))
    a[0], b[1] = 1, 1                             # members disagree completely
    mi = mutual_information([a, b])
    assert np.allclose(mi, 1.0, atol=1e-5) and np.allclose(mutual_information([a, a]), 0, atol=1e-5)
    probs = np.stack([np.r_[0.9, 0.6, 0.55, 0.99], 1 - np.r_[0.9, 0.6, 0.55, 0.99]])
    truth = np.array([0, 1, 1, 0])
    rc = risk_coverage(probs, truth, np.ones(4, bool), coverages=(1.0, 0.5), classes=(0, 1))
    assert rc["rows"][0]["accuracy"] == 0.5 and rc["rows"][1]["accuracy"] == 1.0
    assert rc["rows"][1]["accuracy_after_review"] == 1.0 and rc["n_voxels"] == 4
    logits = np.stack([np.r_[2.0, -2.0] * 3, np.r_[-2.0, 2.0] * 3])     # over-confident and correct
    T = temperature_scale([logits.reshape(2, 2, 1, 1)], [np.array([0, 1]).reshape(2, 1, 1)])
    assert 0.5 <= T <= 3.0
    ood = intensity_ood(np.linspace(0, 1, 1000), np.ones(1000, bool), np.linspace(0.01, 0.99, 9))
    assert ood["w1"] < 0.01
    assert intensity_ood(np.zeros(5), np.ones(5, bool), np.zeros(9))["flag"]
    lab = np.zeros((4, 4, 4), np.uint8)
    roi = np.zeros_like(lab, bool)
    roi[1:3] = True
    lab[1] = 3                                   # host inside ROI
    checks = {c["check"]: c for c in plausibility_checks(lab, roi)}
    assert not checks["host bone inside defect ROI"]["ok"]
    assert checks["uncertain fraction in ROI"]["ok"]


# ----------------------------------------------------------------------------- longitudinal
@pytest.mark.slow
def test_rigid_registration_recovers_known_motion():
    from osteoquant.longitudinal.core import apply_rigid, register, resample, target_registration_error
    rng = np.random.default_rng(0)
    from scipy import ndimage as ndi
    fixed = ndi.gaussian_filter(rng.random((40, 48, 48)).astype(np.float32), 3) * 1000
    moved, t_true = apply_rigid(fixed, (20, 20, 20), rot_deg=(0, 0, 3), trans_um=(0, 40, -20))
    tx, metric = register(fixed, moved, (20, 20, 20), iters=200)
    tre = target_registration_error(t_true, tx, [(0.48, 0.48, 0.4), (0.2, 0.3, 0.2)])
    assert tre["mean_um"] < 20
    back = resample(moved, fixed.shape, (20, 20, 20), tx)
    c = (slice(10, 30), slice(12, 36), slice(12, 36))
    assert np.corrcoef(back[c].ravel(), fixed[c].ravel())[0, 1] > 0.9


def test_day0_propagation_change_map_and_volumes():
    from osteoquant.longitudinal.core import change_map, class_volume_change, day0_propagation
    later = np.zeros((4, 4, 4), bool)
    later[:2] = True
    roi = np.zeros_like(later)
    roi[1:3] = True
    g0 = np.zeros_like(later)
    g0[1, :2] = True
    lab = day0_propagation(later, g0, roi)
    assert (lab[0] == 3).all() and (lab[1, :2] == 2).all() and (lab[1, 2:] == 1).all() and (lab[2:] == 0).all()
    host = np.zeros_like(later)
    host[3] = True
    assert (day0_propagation(later, g0, roi, erode_vox=1, host=host)[3] == 3).all()
    a = np.zeros((2, 2, 2), np.uint8)
    b = a.copy()
    b[0, 0, 0] = 1
    b[1, 1, 1] = 2
    assert change_map(a, b) == {"0->1": 1, "0->2": 1}
    labs = [np.full((2, 2, 2), 2, np.uint8), np.where(np.arange(8).reshape(2, 2, 2) < 4, 2, 1).astype(np.uint8)]
    rows = class_volume_change(labs, np.ones((2, 2, 2), bool), (1000, 1000, 1000), [0, 4])
    assert rows[0]["graft_mm3"] == 8.0 and rows[1]["graft_remaining_frac"] == 0.5 and rows[1]["new_bone_mm3"] == 4.0
    rows = class_volume_change([np.zeros((1, 1, 1), np.uint8)], np.ones((1, 1, 1), bool), (1, 1, 1), [0])
    assert math.isnan(rows[0]["graft_remaining_frac"])


# ----------------------------------------------------------------------------- histology
def test_colour_deconvolution_recovers_stain_amounts():
    from osteoquant.histology.core import HE, _norm_rows, deconvolve, rgb_to_od
    M = _norm_rows(HE)
    conc = np.array([[0.5, 0.2, 0.0], [0.1, 0.8, 0.0]])
    od = conc @ M
    rgb = (255 * np.exp(-od)).reshape(1, 2, 3)
    C = deconvolve(rgb, HE)
    assert np.allclose(C[0, :, :2], conc[:, :2], atol=0.02)
    assert rgb_to_od(np.full((1, 1, 3), 255)).max() == pytest.approx(0.0)


def test_synthetic_section_quantification_and_normalisation():
    from osteoquant.histology import core as H
    lab = np.zeros((96, 96), np.uint8)
    lab[10:86, 10:86] = 2                       # cellular/marrow-ish tissue
    lab[20:50, 20:76] = 1                       # bone
    lab[60:75, 30:45] = 3
    rgb = H.synthetic_section(lab, rng=np.random.default_rng(0))
    assert rgb.shape == (96, 96, 3) and rgb.dtype == np.uint8
    tm = H.tissue_mask(rgb, min_size=50)
    assert tm[50, 50] and tm.mean() > 0.8
    out, masks = H.quantify_he(rgb, pixel_um=2.0)
    assert 0 <= out["bone_fraction"] <= 1 and out["tissue_area_mm2"] > 0
    out2, _ = H.quantify_he(rgb, graft_rule="basophilic")
    assert "graft_fraction" in out2
    n = H.macenko_normalize(rgb)
    assert n.shape == rgb.shape and n.dtype == np.uint8
    assert H.macenko_vectors(np.full((4, 4, 3), 255, np.uint8)).shape == (2, 3)    # too few pixels -> default
    hmap = H.deconvolve(rgb)[..., 0]
    nl, stats = H.nuclei(hmap, min_area_px=4, pixel_um=1.0)
    assert stats["n_nuclei"] >= 0 and nl.shape == hmap.shape


def test_oblique_slice_and_2d_registration():
    from osteoquant.histology.core import oblique_slice, register_2d
    vol = np.zeros((20, 20, 20), np.float32)
    vol[10] = 5.0
    s = oblique_slice(vol, (10, 10, 10), (1, 0, 0), 8)
    assert s.shape == (8, 8)
    assert np.allclose(s, 5.0)
    rng = np.random.default_rng(0)
    from scipy import ndimage as ndi
    fixed = ndi.gaussian_filter(rng.random((64, 64)).astype(np.float32), 2)
    moving = np.roll(fixed, (2, -3), axis=(0, 1))
    out, tx = register_2d(fixed, moving, mode="affine")
    c = (slice(8, 56), slice(8, 56))
    assert np.corrcoef(out[c].ravel(), fixed[c].ravel())[0, 1] > np.corrcoef(moving[c].ravel(), fixed[c].ravel())[0, 1]


# ----------------------------------------------------------------------------- reports
def _bundle():
    rng = np.random.default_rng(0)
    specs = []
    for g in ("Control", "=HYPERLINK(evil)"):
        for i in range(3):
            specs.append({"specimen_id": f"{g[:3]}{i}", "animal_id": f"{g[:3]}{i}", "group": g, "timepoint": "8w",
                          "metrics": {"class_volumes": {"new_bone_fraction": float(rng.random()),
                                                        "TV_mm3": 1.0}}})
    return {"title": "Study S", "study": {"name": "S", "species": "rat"}, "data_class": "synthetic",
            "review_status": "unreviewed_automated",
            "specimens": specs, "endpoints": [("class_volumes.new_bone_fraction", "New bone", "fraction")],
            "reference_group": "Control", "methods_text": "m", "limitations": ["l"], "reproducibility": {}}


def test_group_stats_comparisons_and_csv_injection(tmp_path):
    import csv
    from osteoquant.report.defectfill import group_stats, write_csv
    b = _bundle()
    table, comps = group_stats(b)
    assert {r["group"] for r in table} == {"Control", "=HYPERLINK(evil)"} and all(r["n"] == 3 for r in table)
    assert len(comps) == 1 and 0 <= comps[0]["p_holm"] <= 1
    write_csv(b, tmp_path / "r.csv")
    rows = list(csv.reader(open(tmp_path / "r.csv")))
    assert all(not c.startswith("=") for r in rows for c in r)
    assert any(c == "'=HYPERLINK(evil)" for r in rows for c in r)


def test_build_pdf_and_figures(tmp_path):
    from osteoquant.report import build_pdf
    from osteoquant.report.figures import group_dotplot, overlay_rgb, specimen_panel
    r = build_pdf(_bundle(), tmp_path / "r.pdf", tmp_path / "r.csv")
    assert (tmp_path / "r.pdf").read_bytes()[:4] == b"%PDF" and len(r["pdf_sha256"]) == 64
    img = np.random.default_rng(0).random((10, 12, 12)).astype(np.float32)
    lab = np.zeros(img.shape, np.uint8)
    lab[3:6, 3:6, 3:6] = 1
    rgb = overlay_rgb(img[5], lab[5])
    assert rgb.shape == (12, 12, 3)
    p = specimen_panel(img, lab, lab > 0, (10, 10, 10), tmp_path / "p.png", title="x")
    assert open(p, "rb").read(4) == b"\x89PNG"
    q = group_dotplot(_bundle(), [("class_volumes.new_bone_fraction", "New bone", "fraction")], tmp_path / "d.png")
    assert open(q, "rb").read(4) == b"\x89PNG"


# ----------------------------------------------------------------------------- pipeline + CLI
def _phantom(tmp_path, model="condyle"):
    from osteoquant.phantom import ImagingConfig, PhantomConfig, generate_phantom, render_fast
    ph = generate_phantom(PhantomConfig(model=model, shape=(40, 56, 56), voxel_um=40, supersample=1,
                                        defect_diameter_um=1400, seed=3))
    return ph, render_fast(ph.mu, 40, ImagingConfig(psf_sigma_um=20, noise_sigma=40))


def test_pipeline_analyze_end_to_end_and_manual_roi(tmp_path):
    from osteoquant.pipeline import analyze, config_hash, labels_hash, public, segment
    ph, v = _phantom(tmp_path)
    r = analyze(v, {"defect_model": "condyle", "nominal_diameter_um": 1400, "qc": False})
    assert r["status"] in ("ok", "review") or "metrics" in r
    pub = public(r)
    assert not any(k.startswith("_") for k in pub) and json.dumps(pub, default=str)
    assert len(config_hash({"a": 1})) == 64 and labels_hash(r["_labels"]) == r["labels_sha256"]
    roi = {"kind": "box", "params": {"min_um": [0, 0, 0], "max_um": [1e9, 1e9, 1e9]}}
    r2 = analyze(v, {"qc": False, "segmentation": "ctan_style", "t_mineral": 0.5, "t_graft": 1.5,
                     "measurement_support": False}, roi_dict=roi)
    assert r2["roi"]["kind"] == "box"
    with pytest.raises(ValueError):
        segment(v, np.ones(v.shape, bool), {"segmentation": "nope"})
    flat = Volume(np.zeros((20, 20, 20), np.float32) + np.random.default_rng(0).normal(0, 1, (20, 20, 20)), (40,) * 3)
    r3 = analyze(flat, {"qc": False, "defect_model": "condyle"})
    assert r3["status"] == "needs_manual_roi" and r3["roi_error"]


def test_cli_commands(tmp_path, monkeypatch, capsys):
    from osteoquant import cli
    from osteoquant.io import write_nifti
    monkeypatch.setattr(cli, "DB", str(tmp_path / "cli.db"))
    cli.main(["init-admin", "--org", "Lab", "--user", "boss", "--password", "Correct-Horse-9"])
    assert json.loads(capsys.readouterr().out)["user_id"] == 1
    cli.main(["audit-verify"])
    assert json.loads(capsys.readouterr().out)["ok"]
    cli.main(["backup", str(tmp_path / "b.db")])
    assert len(json.loads(capsys.readouterr().out)["sha256"]) == 64
    ph, v = _phantom(tmp_path)
    p = tmp_path / "v.nii.gz"
    write_nifti(v, p)
    cli.main(["ingest", str(p), "--out", str(tmp_path / "v.zarr")])
    assert "content_sha256" in capsys.readouterr().out
    cli.main(["qc", str(p), "--step", "2"])
    assert "verdict:" in capsys.readouterr().out
    cli.main(["analyze", str(p), "--diameter", "1400", "--json", str(tmp_path / "a.json")])
    assert json.loads((tmp_path / "a.json").read_text())["software_version"]
    assert "timings" in capsys.readouterr().out
    cli.main(["phantom", "--out", str(tmp_path / "ph.nii.gz"), "--seed", "1"])
    out = json.loads(capsys.readouterr().out)
    assert (tmp_path / "ph_labels.nii.gz").exists() and out["labels"].endswith("_labels.nii.gz")
    with pytest.raises(SystemExit):
        cli.main([])


def test_uncertainty_edge_cases():
    from osteoquant.uncertainty.core import risk_coverage, temperature_scale
    p = np.stack([np.r_[0.9, 0.2], np.r_[0.1, 0.8]])
    t = np.array([0, 1])
    rc = risk_coverage(p, t, np.zeros(2, bool), coverages=(1.0,))
    assert rc["n_voxels"] == 0 and math.isnan(rc["aurc"]) and math.isnan(rc["rows"][0]["accuracy"])
    rc2 = risk_coverage(p, t, np.ones(2, bool), score=np.array([0.5, 0.1]), coverages=(0.5,), classes=(1,))
    assert rc2["rows"][0]["accuracy"] == 1.0 and rc2["rows"][0]["n_deferred"] == 1
    logits = np.zeros((2, 4, 1, 1))
    T = temperature_scale([logits], [np.zeros((4, 1, 1), int)], mask_list=[np.ones((4, 1, 1), bool)])
    assert T == 0.5                                     # flat logits: all temperatures tie -> first grid value
