import math

import numpy as np
import pytest

from app import facial_analysis as fa
from app.config import MODEL_PATH


def synthetic_face(smile=0.0, brow=0.0, close_l=0.0, scale=100.0, angle_deg=0.0):
    """A 478-point array with the specific landmarks the features use placed sensibly."""
    p = np.zeros((478, 2))
    def put(i, x, y):
        p[i] = (x, y)
    # person's right eye on image-left (x<0), left eye on image-right
    for ring, cx, close in ((fa.R_EYE_RING, -0.5, 0.0), (fa.L_EYE_RING, 0.5, close_l)):
        outer, top1, top2, top3, inner, bot1, bot2, bot3 = ring
        sgn = -1 if cx < 0 else 1
        h = 0.06 * (1 - close)
        put(outer, cx + sgn * 0.15, 0); put(inner, cx - sgn * 0.15, 0)
        for t, b in ((top1, bot3), (top2, bot2), (top3, bot1)):  # matching lid pairs
            put(t, cx, -h)
            put(b, cx, h)
    for i in fa.R_BROW:
        put(i, -0.5, -0.35 - brow)
    for i in fa.L_BROW:
        put(i, 0.5, -0.35 - brow)
    for i in fa.MIDLINE:
        put(i, 0, 0.3)
    put(fa.R_MOUTH, -0.4 - smile, 1.0 - smile)
    put(fa.L_MOUTH, 0.4 + smile, 1.0 - smile)
    put(fa.UPPER_LIP, 0, 0.98); put(fa.LOWER_LIP, 0, 1.02)
    a = math.radians(angle_deg)
    rot = np.array([[math.cos(a), -math.sin(a)], [math.sin(a), math.cos(a)]])
    return (p @ rot.T) * scale + np.array([320, 240])


def test_features_are_scale_and_rotation_invariant():
    f1 = fa.compute_frame_features(synthetic_face(scale=100))
    f2 = fa.compute_frame_features(synthetic_face(scale=230, angle_deg=12))
    for k in fa.FEATURE_KEYS:
        assert f1[k] == pytest.approx(f2[k], abs=1e-6), k


def test_degenerate_input_returns_empty():
    assert fa.compute_frame_features(np.zeros((478, 2))) == {}


def test_session_metrics_detect_movement_and_ratio():
    n = fa.compute_frame_features(synthetic_face())
    s = fa.compute_frame_features(synthetic_face(smile=0.1))
    b = fa.compute_frame_features(synthetic_face(brow=0.08))
    e = fa.compute_frame_features(synthetic_face(close_l=0.5))
    metrics, missing = fa.compute_session_metrics(
        {"neutral": n, "smile": s, "brow_raise": b, "eye_closure": e, "pucker": None})
    m = {x["key"]: x["value"] for x in metrics}
    assert m["smile_excursion_r"] > 5 and m["smile_excursion_l"] > 5
    assert m["smile_lr_ratio"] == pytest.approx(1.0, abs=1e-6)
    assert m["brow_raise_r"] == pytest.approx(8.0, abs=1e-6)
    assert m["eye_closure_l"] == pytest.approx(50.0, abs=1e-6)
    # right eye did not close → ratio is 0 (one side moved, the other did not)
    assert m["eye_closure_r"] == pytest.approx(0.0, abs=1e-6)
    assert m["eye_closure_lr_ratio"] == pytest.approx(0.0, abs=1e-6)
    # pucker skipped → reported missing, never zero
    missing_keys = {x["key"] for x in missing}
    assert {"pucker_r", "pucker_l", "pucker_lr_ratio"} <= missing_keys
    assert "pucker_r" not in m


def test_no_neutral_means_everything_missing():
    metrics, missing = fa.compute_session_metrics({"smile": {"corner_canthus_r": 1.0}})
    assert metrics == []
    assert len(missing) == len(fa.METRIC_DEFS)


def test_tiny_movement_gives_no_ratio():
    n = fa.compute_frame_features(synthetic_face())
    metrics, missing = fa.compute_session_metrics({"neutral": n, "smile": n})
    assert "smile_lr_ratio" in {x["key"] for x in missing}


def test_summarize_requires_enough_face_frames():
    good = fa.FrameAnalysis(True, features={k: 1.0 for k in fa.FEATURE_KEYS},
                            pose={"yaw": 30.0})
    bad = fa.FrameAnalysis(False)
    out = fa.summarize_samples([good] * 3 + [bad] * 10)
    assert out["features"] is None and out["frames_with_face"] == 3
    out = fa.summarize_samples([good] * 10)
    assert out["features"]["eye_open_r"] == 1.0
    assert any("turned" in n for n in out["quality_notes"])


def test_pose_from_identity_matrix():
    pose = fa.pose_from_matrix(np.eye(4))
    assert all(abs(v) < 1e-9 for v in pose.values())
    assert fa.pose_from_matrix("garbage") == {}


def test_format_metric():
    assert fa.format_metric(None, "ratio") == "—"
    assert fa.format_metric(0.876, "ratio") == "0.88"
    assert fa.format_metric(3.21, "% IOD") == "+3.2%"


@pytest.mark.skipif(not MODEL_PATH.exists(), reason="model file missing")
def test_analyzer_runs_on_blank_frame():
    an = fa.FaceAnalyzer()
    if not an.available:
        pytest.skip(an.error)
    res = an.process(np.zeros((240, 320, 3), dtype=np.uint8))
    assert res.face_detected is False
    an.close()


def test_missing_model_degrades_gracefully(tmp_path):
    an = fa.FaceAnalyzer(tmp_path / "missing.task")
    assert an.available is False and an.error
    res = an.process(np.zeros((10, 10, 3), dtype=np.uint8))
    assert res.face_detected is False
