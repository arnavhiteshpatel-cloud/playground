"""Tests added to close traceability-matrix gaps (see docs/quality/traceability_matrix.csv)."""
from pathlib import Path

import numpy as np
import pytest

from osteoquant.volume import Volume
from osteoquant.morphometry import density_stats
from osteoquant.study.db import Store

ROOT = Path(__file__).resolve().parents[1]
PW = "Correct-Horse-9"


def test_ui_displays_research_prototype_banner():
    html = (ROOT / "web/static/index.html").read_text()
    assert "Research prototype" in html and "not validated" in html


def test_report_contains_ruo_and_not_validated_statements():
    src = (ROOT / "osteoquant/report/defectfill.py").read_text()
    assert "Research use only" in src and "Not validated for GLP" in src and "No claim of 21 CFR Part 11" in src


def test_density_suppressed_without_calibration():
    v = Volume(np.full((5, 5, 5), 100.0, np.float32), (10, 10, 10))
    d = density_stats(v, np.ones((5, 5, 5), bool), erode_vox=0)
    assert d["calibrated"] is False and d["unit"] == "uncalibrated grey value"
    v.meta["calibration"] = {"slope": 1, "intercept": 0, "unit": "mgHA/cm3"}
    assert density_stats(v, np.ones((5, 5, 5), bool), erode_vox=0)["unit"] == "mgHA/cm3"


def test_model_loader_rejects_hash_mismatch():
    from osteoquant.pipeline import segment
    if not (ROOT / "models/unet_ctx_s0.pt").exists():
        pytest.skip("model not trained in this checkout")
    v = Volume(np.zeros((32, 32, 32), np.float32), (40, 40, 40))
    with pytest.raises(RuntimeError, match="hash mismatch"):
        segment(v, np.ones(v.shape, bool), {"segmentation": "unet:unet_ctx_s0", "expected_model_sha256": "0" * 64})


def test_author_cannot_approve_own_segmentation(tmp_path):
    st = Store(tmp_path / "s.db", tmp_path / "d")
    o = st.create_org("L")
    st.create_user(o, "boss", PW, "admin")
    u = st.user_for_token(st.login("boss", PW))
    pid = st.create_project(u, "P")
    sid = st.create_study(u, pid, "S")
    scan = st.register_scan(u, sid, None, None, "", "x", "nifti", "h1", "c1", [1, 1, 1], [1, 1, 1], {})
    seg, _ = st.save_segmentation(u, scan, "automatic", "seg_v1", "abc")
    with pytest.raises(PermissionError, match="Separation of duties"):
        st.review(u, "segmentation", seg, "approved", "approve for reporting")
    assert any(e["action"] == "review.self_approval_denied" for e in st.audit.events())


def test_correction_requires_reason():
    from pydantic import ValidationError
    from osteoquant.api.app import EditsIn
    with pytest.raises(ValidationError):
        EditsIn(base_version=1, ops=[{"op": "brush", "axis": 0, "index": 0, "cy": 1, "cx": 1, "label": 1}])


def test_audit_timestamps_utc_monotonic(tmp_path):
    st = Store(tmp_path / "a.db", tmp_path / "d")
    for i in range(20):
        st.audit.record("x", details={"i": i})
    ts = [e["ts"] for e in reversed(st.audit.events())]
    assert all(t.endswith("Z") for t in ts) and ts == sorted(ts)
