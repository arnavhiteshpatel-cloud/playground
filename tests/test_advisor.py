import numpy as np
from scipy import ndimage as ndi
import pytest

from osteoquant.advisor import (CONDITIONAL, NOT_SUPPORTED, SUPPORTED, MaterialProfile, assess_support,
                                dice_oracle_hist, dice_oracle_samples, scan_relative_units)
from osteoquant.advisor.integration import apply_support


def test_oracle_perfectly_separable():
    g = np.array([0, 0, 0, 10, 10])
    n = np.array([10, 10, 0, 0, 0])
    r = dice_oracle_hist(g, n)
    assert r["dice_graft"] == pytest.approx(1.0)
    assert r["dice_new"] == pytest.approx(1.0)
    assert r["graft_volume_ratio"] == pytest.approx(1.0)


def test_oracle_identical_distributions_is_select_all():
    h = np.array([5, 10, 5])
    r = dice_oracle_hist(h, h, dice_slack=0.0)
    # with identical class distributions the Dice-optimal rule is "everything is graft": 2G/(2G+N)
    assert r["dice_graft"] == pytest.approx(2 * 20 / (40 + 20))


def test_oracle_is_upper_bound_for_threshold_rules():
    rng = np.random.default_rng(0)
    g = rng.normal(1.2, 0.15, 20000)
    n = rng.normal(0.9, 0.15, 20000)
    r = dice_oracle_samples(g, n)
    for t in np.linspace(0.8, 1.3, 26):
        tp = (g > t).sum()
        fp = (n > t).sum()
        dice = 2 * tp / (tp + fp + g.size)
        assert dice <= r["dice_graft_max"] + 1e-3


def test_dense_ha_low_noise_supported():
    a = assess_support("ha", noise_rel=0.05, voxel_um=20)
    assert a.status("residual_graft_volume") == SUPPORTED
    assert a.endpoints["residual_graft_volume"].mechanism == "intensity"


def test_bone_derived_never_intensity_supported():
    for m in ("allograft", "xenograft_dbbm"):
        a = assess_support(m, noise_rel=0.01, voxel_um=20)
        assert a.status("residual_graft_volume") == NOT_SUPPORTED
        assert "bone-derived" in a.endpoints["residual_graft_volume"].reason


def test_radiolucent_graft_not_visible():
    a = assess_support("collagen_sponge", noise_rel=0.05, voxel_um=20)
    assert a.status("residual_graft_volume") == NOT_SUPPORTED
    assert a.status("new_bone_volume") == CONDITIONAL


def test_unknown_material_refused():
    a = assess_support("mystery_putty", noise_rel=0.05, voxel_um=20)
    assert a.status("residual_graft_volume") == NOT_SUPPORTED
    assert "knowledge base" in a.endpoints["residual_graft_volume"].reason


def test_measured_samples_override_unknown_material():
    rng = np.random.default_rng(1)
    a = assess_support("mystery_putty", noise_rel=0.05, voxel_um=20,
                       graft_samples_rel=rng.normal(2.5, 0.05, 5000))
    assert a.status("residual_graft_volume") == SUPPORTED


def test_day0_conditions_and_displacement_limit():
    prof = MaterialProfile("x", rel_mean=0.85, rel_sd=0.05, struct_um=400)
    a = assess_support(prof, noise_rel=0.1, voxel_um=20)
    assert a.status("residual_graft_volume") == NOT_SUPPORTED
    a = assess_support(prof, noise_rel=0.1, voxel_um=20, day0={"registered": True, "qc_pass": True})
    assert a.status("residual_graft_volume") == NOT_SUPPORTED          # incomplete day-0 assessment (IMG-04)
    assert "incomplete" in a.endpoints["residual_graft_volume"].reason
    full = {"registered": True, "qc_pass": True, "untracked_fraction": 0.0, "max_displacement_um": 50.0}
    a = assess_support(prof, noise_rel=0.1, voxel_um=20, day0=full)
    assert a.status("residual_graft_volume") == CONDITIONAL
    assert any("day-0" in c for c in a.endpoints["residual_graft_volume"].conditions)
    a = assess_support(prof, noise_rel=0.1, voxel_um=20,
                       day0={**full, "max_displacement_um": 500, "tolerance_um": 200})
    assert a.status("residual_graft_volume") == NOT_SUPPORTED
    a = assess_support(prof, noise_rel=0.1, voxel_um=20, day0={**full, "qc_pass": False})
    assert a.status("residual_graft_volume") == NOT_SUPPORTED


def test_density_requires_calibration():
    assert assess_support("ha", noise_rel=0.05, voxel_um=20).status("tissue_mineral_density") == NOT_SUPPORTED
    assert assess_support("ha", noise_rel=0.05, voxel_um=20, calibrated=True).status("tissue_mineral_density") == SUPPORTED


def test_no_graft_design():
    a = assess_support(None, noise_rel=0.05, voxel_um=20, no_graft=True)
    assert a.status("new_bone_volume") == SUPPORTED
    assert a.status("residual_graft_volume") == NOT_SUPPORTED


def test_supported_set_shrinks_with_noise():
    order = [SUPPORTED, CONDITIONAL, NOT_SUPPORTED]
    prev = -1
    for nr in (0.02, 0.1, 0.3, 0.6):
        s = order.index(assess_support("bcp", noise_rel=nr, voxel_um=20).status("residual_graft_volume"))
        assert s >= prev
        prev = s


def test_scan_relative_units_excludes_defect():
    rng = np.random.default_rng(0)
    img = rng.normal(100, 10, (40, 40, 40)).astype(np.float32)
    img[:, :, :15] += 900          # host bone at 1000
    roi = np.zeros(img.shape, bool)
    roi[10:30, 20:35, 20:35] = True
    img[roi] = 2500                 # very dense graft inside the defect must not be taken as host
    est = scan_relative_units(img, exclude_mask=roi)
    assert est["host"] == pytest.approx(1000, abs=30)
    assert est["soft"] == pytest.approx(100, abs=10)
    assert est["noise_rel"] == pytest.approx(10 / 900, rel=0.3)


def test_apply_support_suppresses_unsupported():
    metrics = {"class_volumes": {"new_bone_volume_mm3": 1.0, "residual_graft_volume_mm3": 2.0,
                                 "residual_graft_fraction": 0.2, "new_bone_fraction": 0.1, "mineralized_fraction": 0.3}}
    support = assess_support("allograft", noise_rel=0.05, voxel_um=20).to_dict()
    rep, sup = apply_support(metrics, support)
    assert rep["class_volumes"]["residual_graft_volume_mm3"] is None
    assert rep["class_volumes"]["new_bone_volume_mm3"] is None
    assert rep["class_volumes"]["mineral_volume_mm3"] == pytest.approx(3.0)
    assert rep["class_volumes"]["mineralized_fraction"] == 0.3
    assert {s["endpoint"] for s in sup} >= {"residual_graft_volume", "new_bone_volume"}
    assert metrics["class_volumes"]["residual_graft_volume_mm3"] == 2.0      # raw metrics untouched


def test_pipeline_reports_support():
    from osteoquant.phantom import PhantomConfig, generate_phantom, ImagingConfig, render_fast
    from osteoquant.pipeline import analyze
    ph = generate_phantom(PhantomConfig(model="condyle", shape=(40, 48, 48), voxel_um=40, defect_diameter_um=1200,
                                        graft_material="ha", healing_stage=0.4, seed=3))
    vol = render_fast(ph.mu, 40, ImagingConfig(seed=1, noise_sigma=30))
    out = analyze(vol, {"defect_model": "condyle", "nominal_diameter_um": 1200, "thickness_metrics": False})
    if out.get("status") == "needs_manual_roi":
        pytest.skip("ROI not found on tiny phantom")
    assert "measurement_support" in out
    assert out["reported_metrics"]["class_volumes"]["residual_graft_volume_mm3"] is None   # material unspecified
    out2 = analyze(vol, {"defect_model": "condyle", "nominal_diameter_um": 1200, "thickness_metrics": False,
                         "material": "ha"})
    assert out2["measurement_support"]["endpoints"]["residual_graft_volume"]["status"] == SUPPORTED
    assert out2["reported_metrics"]["class_volumes"]["residual_graft_volume_mm3"] is not None


def test_metals_refused():
    for m in ("titanium", "magnesium"):
        assert assess_support(m, noise_rel=0.02, voxel_um=20).status("residual_graft_volume") == NOT_SUPPORTED


def test_small_reference_samples_ignored_and_bone_rule_not_bypassed():
    rng = np.random.default_rng(0)
    a = assess_support("mystery", noise_rel=0.05, voxel_um=20, graft_samples_rel=rng.normal(2.5, 0.05, 3))
    assert a.status("residual_graft_volume") == NOT_SUPPORTED
    a = assess_support("autograft", noise_rel=0.01, voxel_um=20, graft_samples_rel=rng.normal(3.0, 0.01, 5000),
                       new_samples_rel=rng.normal(0.5, 0.01, 5000))
    assert a.status("residual_graft_volume") == NOT_SUPPORTED


def test_scarce_graft_refuses_graft_volume_only():
    a = assess_support("ha", noise_rel=0.03, voxel_um=20, graft_prior=0.02)
    assert a.status("residual_graft_volume") == NOT_SUPPORTED
    assert "scarce" in a.endpoints["residual_graft_volume"].reason
    assert a.status("new_bone_volume") == SUPPORTED


def test_support_requires_robustness_to_low_graft_share():
    # a borderline material can pass at 50% graft share but fail at 10%: the advisor must check both
    prof = MaterialProfile("borderline", rel_mean=1.35, rel_sd=0.08, struct_um=500)
    hi = assess_support(prof, noise_rel=0.05, voxel_um=20, graft_prior=0.5)
    lo = assess_support(prof, noise_rel=0.05, voxel_um=20, graft_prior=0.1)
    order = [SUPPORTED, CONDITIONAL, NOT_SUPPORTED]
    assert order.index(lo.status("residual_graft_volume")) >= order.index(hi.status("residual_graft_volume"))
    assert set(lo.intensity["by_prior"]) == {"0.100", "0.050"}


def test_assessment_records_version():
    from osteoquant.advisor.separability import ADVISOR_VERSION
    assert assess_support("ha", noise_rel=0.05, voxel_um=20).to_dict()["advisor_version"] == ADVISOR_VERSION


def test_no_graft_and_radiolucent_keep_architecture_endpoint():
    a = assess_support(None, noise_rel=0.05, voxel_um=20, no_graft=True)
    assert a.status("new_bone_thickness") == CONDITIONAL
    b = assess_support("collagen_sponge", noise_rel=0.05, voxel_um=20)
    assert b.status("new_bone_thickness") == CONDITIONAL


def test_characterise_material_and_use_in_advisor():
    from osteoquant.advisor.characterize import characterise_material
    rng = np.random.default_rng(3)
    img = rng.normal(100, 10, (40, 40, 40)).astype(np.float32)
    zz, yy, xx = np.indices(img.shape)
    host = xx < 8
    img[host] += 900                                   # host bone → relative 1
    mat = np.zeros(img.shape, bool)
    for c in ((20, 15, 20), (20, 28, 28), (10, 22, 30)):
        mat |= ((zz - c[0]) ** 2 + (yy - c[1]) ** 2 + (xx - c[2]) ** 2) <= 25
    img[mat] = 100 + 2.0 * 900 + rng.normal(0, 10, mat.sum())   # material at relative ≈2.0
    soft = ~host & ~ndi.binary_dilation(mat, iterations=2)
    ch = characterise_material(img, mat, soft, ndi.binary_erosion(host), 40.0, "new_ceramic")
    assert ch.rel_mean == pytest.approx(2.0, abs=0.05)
    assert ch.thickness_um_median > 3 * 40
    ok, _ = ch.compatible_with(42.0)
    assert ok
    assert not ch.compatible_with(80.0)[0]
    a = assess_support("new_ceramic", noise_rel=0.02, voxel_um=40, graft_samples_rel=ch.samples_rel)
    assert a.status("residual_graft_volume") == SUPPORTED


def test_characterise_rejects_tiny_mask():
    from osteoquant.advisor.characterize import characterise_material
    img = np.zeros((10, 10, 10), np.float32)
    m = np.zeros(img.shape, bool); m[5, 5, 5] = True
    with pytest.raises(ValueError):
        characterise_material(img, m, ~m, ~m, 40.0, "x")


def _test_signer():
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    k = Ed25519PrivateKey.generate()
    pub = k.public_key().public_bytes_raw().hex()
    return k, {"unit-test": (pub, True)}


def test_validation_records_synthetic_never_qualifies(tmp_path, monkeypatch):
    import osteoquant.ml.validation_records as vr
    monkeypatch.setattr(vr, "MODEL_DIR", tmp_path)
    key, keys = _test_signer()
    base = dict(model_name="m", model_sha256="abc", material="beta_tcp", n_specimens=20, voxel_um_range=(10, 40),
                scanner_class="desktop", graft_volume_abs_rel_error_p95=0.08, reference_method="gravimetric",
                evidence_location="validation/x")
    vr.add_record(vr.ValidationRecord(data_class="synthetic", **base), key, "unit-test", keys=keys)
    assert not vr.validated_for("m", "abc", "beta_tcp", 20, keys=keys)[0]
    vr.add_record(vr.ValidationRecord(data_class="physical_phantom", **base), key, "unit-test", keys=keys)
    ok, why = vr.validated_for("m", "abc", "beta_tcp", 20, keys=keys)               # test key: never qualifies
    assert not ok and "test key" in why                                              # (C3-PRD-05)
    ok, why = vr.validated_for("m", "abc", "beta_tcp", 20, keys=keys, accept_test_signed=True)
    assert ok and "[TEST-SIGNED]" in why
    T = {"keys": keys, "accept_test_signed": True}
    assert not vr.validated_for("m", "abc", "beta_tcp", 80, **T)[0]          # outside voxel range
    assert not vr.validated_for("m", "OTHER", "beta_tcp", 20, **T)[0]        # different model version
    assert not vr.validated_for("m", "abc", "ha", 20, **T)[0]                # different material
    assert not vr.validated_for("m", "abc", "beta_tcp", 20, keys={})[0]            # untrusted signer


def test_dbm_new_bone_not_supported():
    a = assess_support("dbm", noise_rel=0.05, voxel_um=20)
    assert a.status("new_bone_volume") == NOT_SUPPORTED
    assert a.status("residual_graft_volume") == NOT_SUPPORTED


def test_resorbable_material_needs_early_known_timepoint():
    late = assess_support("beta_tcp", noise_rel=0.03, voxel_um=20)
    assert late.status("residual_graft_volume") == NOT_SUPPORTED
    assert "timepoint" in late.endpoints["residual_graft_volume"].reason
    assert assess_support("beta_tcp", noise_rel=0.03, voxel_um=20, healing_weeks=12).status("residual_graft_volume") == NOT_SUPPORTED
    early = assess_support("beta_tcp", noise_rel=0.03, voxel_um=20, healing_weeks=2)
    assert "resorbable_timepoint_rule" not in early.intensity


def test_knowledge_base_physics_disagreement_requires_measurement():
    from osteoquant.advisor.separability import material_profile
    prof = material_profile("bioglass_45s5")
    if not prof.uncertain:
        pytest.skip("knowledge base and physics agree for this material")
    a = assess_support("bioglass_45s5", noise_rel=0.03, voxel_um=20, healing_weeks=2)
    assert a.status("residual_graft_volume") == NOT_SUPPORTED
    assert "uncertain" in a.endpoints["residual_graft_volume"].reason


def test_characterisation_undeclared_bone_status_is_conservative():
    from osteoquant.advisor.characterize import MaterialCharacterisation
    ch = MaterialCharacterisation("x", "material_only", "0" * 64, 20.0, {}, 0.0, 1.0, 2.0, 0.1, {}, 400.0, (300, 500), 1000)
    assert ch.profile().bone_derived is True
    ch.bone_derived = False
    assert ch.profile().bone_derived is False


def test_validation_records_tamper_detected(tmp_path, monkeypatch):
    import json
    import osteoquant.ml.validation_records as vr
    monkeypatch.setattr(vr, "MODEL_DIR", tmp_path)
    key, keys = _test_signer()
    base = dict(model_name="m", model_sha256="abc", material="ha", n_specimens=20, voxel_um_range=(10, 40),
                scanner_class="desktop", graft_volume_abs_rel_error_p95=0.08, reference_method="gravimetric",
                evidence_location="x", data_class="synthetic")
    vr.add_record(vr.ValidationRecord(**base), key, "unit-test", keys=keys)
    env = json.loads((tmp_path / "validation_records.json").read_text())
    env["payload"] = env["payload"].replace("synthetic", "in_vivo")       # local edit to grant support
    (tmp_path / "validation_records.json").write_text(json.dumps(env))
    ok, why = vr.validated_for("m", "abc", "ha", 20, keys=keys)
    assert not ok and "signature" in why


def test_scan_profile_mismatch_refuses():
    ok = assess_support("ha", noise_rel=0.03, voxel_um=20, observed_graft_level=2.0)
    assert "uncertain_profile_rule" not in ok.intensity
    bad = assess_support("ha", noise_rel=0.03, voxel_um=20, observed_graft_level=1.5)
    assert bad.status("residual_graft_volume") == NOT_SUPPORTED
    assert "profile mismatch" in bad.endpoints["residual_graft_volume"].reason


def test_bone_derived_not_supported_by_day0():
    full = {"registered": True, "qc_pass": True, "untracked_fraction": 0.0, "max_displacement_um": 10.0}
    for m in ("autograft", "allograft"):                     # remodelling bone grafts
        a = assess_support(m, noise_rel=0.05, voxel_um=20, day0=full)
        assert a.status("residual_graft_volume") == NOT_SUPPORTED
    # DBBM is deproteinised and resorbs very slowly: the day-0 footprint mechanism applies (C2-SCI-10)
    d = assess_support("xenograft_dbbm", noise_rel=0.05, voxel_um=20, day0=full)
    assert d.status("residual_graft_volume") == CONDITIONAL


def test_metals_refuse_mineral_and_bcp_is_resorbable():
    m = assess_support("titanium", noise_rel=0.02, voxel_um=20)
    assert m.status("total_mineral_volume") == NOT_SUPPORTED
    b = assess_support("bcp", noise_rel=0.02, voxel_um=20)
    assert "resorbable_timepoint_rule" in b.intensity


def test_pipeline_binds_support_to_method():
    from osteoquant.pipeline import bind_support_to_method
    sup = assess_support("ha", noise_rel=0.03, voxel_um=20).to_dict()
    bind_support_to_method(sup, {"method": "multiotsu"})
    assert sup["endpoints"]["total_mineral_volume"]["status"] == NOT_SUPPORTED
    assert "not covered" in sup["endpoints"]["residual_graft_volume"]["reason"]
    sup2 = assess_support("ha", noise_rel=0.03, voxel_um=20).to_dict()
    bind_support_to_method(sup2, {"method": "advisor_threshold"})
    assert sup2["endpoints"]["residual_graft_volume"]["status"] == SUPPORTED


def test_new_bone_error_propagation_refuses_when_graft_dominates():
    a = assess_support("ha", noise_rel=0.03, voxel_um=20, graft_prior=0.7)
    assert a.status("new_bone_volume") == NOT_SUPPORTED
    assert "mineral minus graft" in a.endpoints["new_bone_volume"].reason
    b = assess_support("ha", noise_rel=0.03, voxel_um=20, graft_prior=0.15)
    assert b.intensity["new_bone_error_budget"]["propagated_rel_error"] < a.intensity["new_bone_error_budget"]["propagated_rel_error"]


def test_ambiguous_rim_refuses_new_bone_and_bounds_mineral():
    a = assess_support("ha", noise_rel=0.03, voxel_um=20, graft_prior=0.2, rim_fraction_new=0.3, rim_fraction_mineral=0.05)
    assert a.status("new_bone_volume") == NOT_SUPPORTED and "rim" in a.endpoints["new_bone_volume"].reason
    assert a.status("total_mineral_volume") != NOT_SUPPORTED
    # 1.4.3: rim_fraction_mineral is the worst-case relative error rim/(mineral − rim); the limit is the 20% failure
    # threshold (C3-SCI-10)
    b = assess_support("ha", noise_rel=0.03, voxel_um=20, graft_prior=0.2, rim_fraction_new=0.3, rim_fraction_mineral=0.15)
    assert b.status("total_mineral_volume") != NOT_SUPPORTED
    c = assess_support("ha", noise_rel=0.03, voxel_um=20, graft_prior=0.2, rim_fraction_new=0.3, rim_fraction_mineral=0.25)
    assert c.status("total_mineral_volume") == NOT_SUPPORTED and "worst case" in c.endpoints["total_mineral_volume"].reason


def test_blur_estimator_tracks_known_psf():
    from osteoquant.advisor.integration import estimate_blur
    rng = np.random.default_rng(0)
    z = np.zeros((40, 64, 64), np.float32)
    z[:, :, 32:] = 1.0                                   # thick bone half-space, soft elsewhere
    roi = np.zeros(z.shape, bool)
    out = []
    for sig in (0.5, 0.8):
        img = ndi.gaussian_filter(z, sig) * 1000 + 100 + rng.normal(0, 10, z.shape)
        out.append(estimate_blur(img.astype(np.float32), roi, 100.0, 1100.0)["sigma_vox_raw"])
    assert out[0] == pytest.approx(0.5, abs=0.15) and out[1] == pytest.approx(0.8, abs=0.2) and out[1] > out[0]


def test_blur_own_fraction_bounds():
    from osteoquant.advisor.separability import blur_own_fraction, blur_surface_fraction
    rng = np.random.default_rng(1)
    f = blur_own_fraction(10000, rng, 0.8, 6.0)
    assert f.min() >= 0.49 and f.max() <= 1.0
    thin = blur_own_fraction(10000, rng, 0.8, 1.5)
    assert thin.mean() < f.mean()                         # thin structures lose more intensity to blur
    assert blur_surface_fraction(2.0, 0.8) == 1.0 and blur_surface_fraction(20.0, 0.5) < 0.5


def _char_scene(seed=3, mat_rel=2.0, radius2=25):
    rng = np.random.default_rng(seed)
    img = rng.normal(100, 10, (40, 40, 40)).astype(np.float32)
    zz, yy, xx = np.indices(img.shape)
    host = xx < 8
    img[host] += 900
    mat = np.zeros(img.shape, bool)
    for c in ((20, 15, 20), (20, 28, 28), (10, 22, 30)):
        mat |= ((zz - c[0]) ** 2 + (yy - c[1]) ** 2 + (xx - c[2]) ** 2) <= radius2
    img[mat] = 100 + mat_rel * 900 + rng.normal(0, 10, mat.sum())
    soft = ~host & ~ndi.binary_dilation(mat, iterations=2)
    return img, mat, soft, ndi.binary_erosion(host)


def test_characterisation_is_bound_to_its_acquisition():
    """A measured profile only transfers to scans with the same voxel size (±25%), kVp, filter and scanner model."""
    import json
    from osteoquant.advisor.characterize import characterise_material
    img, mat, soft, host = _char_scene()
    ch = characterise_material(img, mat, soft, host, 40.0, "new_ceramic", bone_derived=False,
                               acquisition={"kvp": 70, "filter": "Al 0.5 mm", "scanner_model": "S1"})
    assert ch.compatible_with(40.0, {"kvp": 70, "filter": "Al 0.5 mm"}) == (True, "compatible")
    ok, why = ch.compatible_with(40.0, {"kvp": 90})
    assert not ok and "kvp" in why
    assert not ch.compatible_with(40.0, {"scanner_model": "S2"})[0]
    assert not ch.compatible_with(52.0)[0] and ch.compatible_with(49.0)[0]
    d = json.loads(ch.to_json())
    assert d["material_id"] == "new_ceramic" and d["bone_derived"] is False and len(d["scan_sha256"]) == 64


def test_characterisation_guards_and_warnings():
    from osteoquant.advisor.characterize import characterise_material
    img, mat, soft, host = _char_scene()
    with pytest.raises(ValueError, match="not brighter"):            # host darker than soft tissue: inverted scan
        characterise_material(img.max() - img, mat, soft, host, 40.0, "x", bone_derived=False)
    few = np.zeros_like(soft)
    few.flat[:50] = True
    with pytest.raises(ValueError, match="≥100 voxels"):
        characterise_material(img, mat, few, host, 40.0, "x", bone_derived=False)
    # thin structures (radius ≈1.4 voxels) at coarse voxels: partial-volume warning; undeclared bone status warning
    img2, thin, soft2, host2 = _char_scene(radius2=2)
    thin_many = thin.copy()
    zz, yy, xx = np.indices(thin.shape)
    thin_many |= ((xx % 6 == 0) & (yy % 6 == 0) & (zz > 4) & (zz < 36) & (xx > 10))   # 1-voxel rods
    img2[thin_many] = 100 + 2.0 * 900
    ch = characterise_material(img2, thin_many, soft2 & ~thin_many, host2, 40.0, "rods")
    assert any("< 3 voxels" in w for w in ch.warnings)
    assert any("not declared" in w for w in ch.warnings) and ch.profile().bone_derived is True
    # heterogeneous material (two phases) is flagged
    img3, mat3, soft3, host3 = _char_scene()
    img3[mat3 & (np.indices(img3.shape)[2] > 25)] = 100 + 0.6 * 900
    ch3 = characterise_material(img3, mat3, soft3, host3, 40.0, "mixed", bone_derived=False)
    assert any("heterogeneous" in w for w in ch3.warnings)


def test_characterise_from_day0_recovers_graft_level():
    """Day-0 scan (no new bone): graft = mineral inside the ROI; the measured level matches the simulated one."""
    from osteoquant.advisor.characterize import characterise_from_day0
    img, mat, soft, host = _char_scene(mat_rel=1.8)
    roi = ndi.binary_dilation(mat, iterations=3)
    ch = characterise_from_day0(img, roi, 40.0, "day0_ceramic", bone_derived=False)
    assert ch.source == "day0" and ch.rel_mean == pytest.approx(1.8, abs=0.08)
    assert ch.n_voxels >= 500


def test_validation_records_hostile_key_id_and_corrupt_file(tmp_path, monkeypatch):
    """C3-PRD-02/-15: an unsigned file whose key_id spells the success phrase must not unlock support, and its text
    must not appear in the reason; a corrupt file degrades to 'no record' instead of aborting the analysis."""
    import json
    import osteoquant.ml.validation_records as vr
    from osteoquant.advisor.integration import bind_support_to_method
    monkeypatch.setattr(vr, "MODEL_DIR", tmp_path)
    (tmp_path / "validation_records.json").write_text(json.dumps(
        {"format": vr.FORMAT, "key_id": "qualifying validation record", "payload": "{}", "signature": "AA=="}))
    ok, why = vr.validated_for("m", "abc", "ha", 20)
    assert not ok and "qualifying" not in why and "untrusted key" in why
    sup = {"endpoints": {"residual_graft_volume": {"status": "supported", "reason": ""},
                         "graft_fraction_of_defect": {"status": "supported", "reason": ""}}}
    bind_support_to_method(sup, {"method": "onnx:m", "validation_record": "qualifying validation record",
                                 "validation_ok": ok})
    assert {d["status"] for d in sup["endpoints"].values()} == {"not_supported"}
    sup2 = {"endpoints": {"residual_graft_volume": {"status": "supported", "reason": ""}}}
    bind_support_to_method(sup2, {"method": "onnx:m", "validation_ok": "yes"})      # only the boolean True counts
    assert sup2["endpoints"]["residual_graft_volume"]["status"] == "not_supported"
    (tmp_path / "validation_records.json").write_text("{corrupt")
    ok, why = vr.validated_for("m", "abc", "ha", 20)
    assert not ok and "unreadable" in why



def test_support_is_evaluated_at_read_time():
    """C3-PRD-01/-04: stored statuses are not trusted. A record from another advisor version or rule set (or
    stored before method binding) is refused with 're-analyse'; a non-validated method is refused; a manually
    corrected segmentation keeps at most 'supported with conditions'; tissue mineral density is untouched."""
    from osteoquant.advisor.integration import SUPPORT_RULES, effective_support, measurement_support, reported_view
    from osteoquant.advisor.separability import ADVISOR_VERSION
    eps = {"residual_graft_volume": {"status": "supported", "reason": ""},
           "total_mineral_volume": {"status": "supported", "reason": ""},
           "tissue_mineral_density": {"status": "supported", "reason": ""}}
    metrics = {"class_volumes": {"residual_graft_volume_mm3": 1.25, "mineral_volume_mm3": 2.5}}
    old = {"metrics": metrics, "segmentation": {"method": "multiotsu"},
           "measurement_support": {"endpoints": eps, "advisor_version": "1.3.3"}}          # pre-binding record
    ms = measurement_support(old)
    assert ms["residual_graft_volume"]["status"] == "not_assessed" and "re-analyse" in ms["residual_graft_volume"]["reason"]
    assert ms["tissue_mineral_density"]["status"] == "supported"
    rep, sup, eff = reported_view(old)
    assert rep["class_volumes"]["residual_graft_volume_mm3"] is None and eff["stale"]
    cur = {"advisor_version": ADVISOR_VERSION, "support_rules": SUPPORT_RULES}
    otsu = {"metrics": metrics, "segmentation": {"method": "multiotsu"}, "measurement_support": {"endpoints": eps, **cur}}
    assert measurement_support(otsu)["total_mineral_volume"]["status"] == "not_supported"
    adv = {"metrics": metrics, "segmentation": {"method": "advisor_threshold"},
           "measurement_support": {"endpoints": eps, **cur}}
    assert measurement_support(adv)["total_mineral_volume"]["status"] == "supported"
    edited = dict(adv, corrected_from=1)
    e = effective_support(edited)
    assert e["endpoints"]["residual_graft_volume"]["status"] == "supported_with_conditions"
    assert any("manually corrected" in c for c in e["endpoints"]["residual_graft_volume"]["conditions"])
    assert adv["measurement_support"]["endpoints"]["residual_graft_volume"]["status"] == "supported"   # no mutation


def test_unspecified_material_refuses_mineral_next_to_dense_blurred_graft():
    """C3-SCI-01 regression: with no material (no graft threshold), graft-like voxels brighter than host bone are the
    proxy for the ambiguous-rim gate; dense graft under heavy blur makes total mineral unidentifiable (before 1.4.3
    it was 'supported' with +21…+38% error in the review's probe)."""
    from osteoquant.advisor.integration import support_for_scan
    from osteoquant.phantom import ImagingConfig, PhantomConfig, generate_phantom, render_fast
    ph = generate_phantom(PhantomConfig(model="condyle", shape=(40, 56, 56), voxel_um=40, supersample=1,
                                        defect_diameter_um=1400, healing_stage=0.5, graft_material="ha", seed=3))
    img = render_fast(ph.mu, 40, ImagingConfig(psf_sigma_um=50, noise_sigma=40, seed=3)).data
    sup = support_for_scan(img, ph.roi_mask, (40.0,) * 3, {"material": None})
    rim = sup["intensity"].get("ambiguous_rim") or {}
    assert rim.get("worst_case_mineral_error") is not None
    assert sup["endpoints"]["total_mineral_volume"]["status"] == "not_supported"
    assert sup["endpoints"]["residual_graft_volume"]["status"] == "not_supported"


def test_measured_references_get_scan_noise_and_partial_volume():
    """C3-SCI-07: low-noise control samples must not make the mineral rule pass at noise where the assumed range fails,
    and interior-only graft samples get this scan's partial volume (blur-aware with measured thickness)."""
    from osteoquant.advisor.separability import mineral_rule
    rng = np.random.default_rng(0)
    nb = rng.uniform(0.6, 1.0, 5000) + rng.normal(0, 0.03, 5000)
    with_samples = mineral_rule("ha", noise_rel=0.30, voxel_um=20, new_samples_rel=nb)
    assumed = mineral_rule("ha", noise_rel=0.30, voxel_um=20)
    assert not with_samples["passes_policy"] and not assumed["passes_policy"]      # passed (Dice 0.93) before 1.4.3
    g = rng.normal(1.9, 0.076, 5000)
    sharp = assess_support("x_ceramic", noise_rel=0.10, voxel_um=40, graft_samples_rel=g, healing_weeks=2,
                           graft_struct_um=200, blur_sigma_vox=0.3)
    blurred = assess_support("x_ceramic", noise_rel=0.10, voxel_um=40, graft_samples_rel=g, healing_weeks=2,
                             graft_struct_um=200, blur_sigma_vox=1.5)
    assert blurred.intensity["dice_graft_threshold_rule"] < sharp.intensity["dice_graft_threshold_rule"]

