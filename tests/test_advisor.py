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


def test_validation_records_synthetic_never_qualifies(tmp_path, monkeypatch):
    import osteoquant.ml.validation_records as vr
    monkeypatch.setattr(vr, "MODEL_DIR", tmp_path)
    base = dict(model_name="m", model_sha256="abc", material="beta_tcp", n_specimens=20, voxel_um_range=(10, 40),
                scanner_class="desktop", graft_volume_abs_rel_error_p95=0.08, reference_method="gravimetric",
                evidence_location="validation/x")
    vr.add_record(vr.ValidationRecord(data_class="synthetic", **base))
    assert not vr.validated_for("m", "abc", "beta_tcp", 20)[0]
    vr.add_record(vr.ValidationRecord(data_class="physical_phantom", **base))
    assert vr.validated_for("m", "abc", "beta_tcp", 20)[0]
    assert not vr.validated_for("m", "abc", "beta_tcp", 80)[0]          # outside voxel range
    assert not vr.validated_for("m", "OTHER", "beta_tcp", 20)[0]        # different model version
    assert not vr.validated_for("m", "abc", "ha", 20)[0]                # different material


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
