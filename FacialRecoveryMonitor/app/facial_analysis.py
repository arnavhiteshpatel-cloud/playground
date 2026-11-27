"""Facial landmark detection and EXPERIMENTAL geometric movement measurements.

IMPORTANT
---------
Every number produced by this module is an *experimental demonstration* of what
landmark geometry can capture. None of these calculations have been clinically
validated, and they must not be used to diagnose, grade severity, or judge
recovery. Missing data is always represented as ``None`` — never as zero.

Conventions
-----------
* Landmarks come from the MediaPipe Face Landmarker (478-point face mesh).
* "Right"/"Left" always mean the **person's own** right/left side. On an
  un-mirrored camera image the person's right side appears on the image's left.
* Distances are expressed as a percentage of the inter-ocular distance (% IOD):
  the distance between the centres of the two eyes. Normalising this way removes
  most of the effect of sitting closer to or further from the camera.
* Before measuring, landmarks are rotated so that the line between the eyes is
  horizontal, which removes in-plane head tilt (roll). Turning the head left or
  right (yaw) cannot be fully corrected, so head pose is recorded as a quality
  indicator.
"""

from __future__ import annotations

import logging
import math
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import numpy as np

from .config import HEAD_TURN_WARNING_DEG, MIN_FACE_FRAMES, MODEL_PATH
from .face_topology import ALL_CONTOURS

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Guided expression protocol
# ---------------------------------------------------------------------------
EXPRESSIONS: list[dict] = [
    {"key": "neutral", "name": "Neutral position", "short": "Neutral",
     "instruction": "Relax your facial muscles and look directly at the camera.",
     "detail": "Keep your mouth gently closed and your gaze level. This resting position is "
               "the reference that the other movements are compared against.",
     "optional": False},
    {"key": "smile", "name": "Gentle smile", "short": "Smile",
     "instruction": "Give a gentle smile without forcing the movement.",
     "detail": "Smile as you comfortably can, keeping your lips closed or slightly parted. "
               "Do not strain — a natural, gentle movement is best.",
     "optional": False},
    {"key": "brow_raise", "name": "Eyebrow movement", "short": "Eyebrows",
     "instruction": "Raise your eyebrows gently.",
     "detail": "Lift your eyebrows as if mildly surprised while keeping your eyes open and "
               "looking at the camera.",
     "optional": False},
    {"key": "eye_closure", "name": "Eye closure", "short": "Eyes closed",
     "instruction": "Gently close your eyes.",
     "detail": "Press Capture, then close your eyes softly as if falling asleep — do not "
               "squeeze. Keep them closed for about five seconds; your computer will play a "
               "short alert sound (if sound is on) when the capture has finished.",
     "optional": False},
    {"key": "pucker", "name": "Lip pucker (optional)", "short": "Pucker",
     "instruction": "Optional: gently pucker your lips as if about to whistle.",
     "detail": "This extra movement is optional. Skip it if it is uncomfortable or if your "
               "clinician has not asked you to practise it.",
     "optional": True},
]
EXPRESSION_BY_KEY = {e["key"]: e for e in EXPRESSIONS}

# ---------------------------------------------------------------------------
# Landmark indices (MediaPipe face mesh)
# ---------------------------------------------------------------------------
R_EYE_OUTER, R_EYE_INNER = 33, 133
L_EYE_OUTER, L_EYE_INNER = 263, 362
R_EYE_LID_PAIRS = ((159, 145), (158, 153), (160, 144))
L_EYE_LID_PAIRS = ((386, 374), (385, 380), (387, 373))
R_EYE_RING = (33, 160, 159, 158, 133, 153, 145, 144)
L_EYE_RING = (263, 387, 386, 385, 362, 380, 374, 373)
R_BROW = (70, 63, 105, 66, 107)
L_BROW = (300, 293, 334, 296, 336)
R_MOUTH, L_MOUTH = 61, 291
UPPER_LIP, LOWER_LIP = 13, 14
MIDLINE = (168, 6, 197)  # nose bridge points, a relatively stable midline reference
KEY_POINTS = (R_MOUTH, L_MOUTH, 105, 334, 159, 145, 386, 374, 1)

BLENDSHAPE_KEYS = (
    "mouthSmileLeft", "mouthSmileRight", "browInnerUp", "browOuterUpLeft", "browOuterUpRight",
    "eyeBlinkLeft", "eyeBlinkRight", "eyeSquintLeft", "eyeSquintRight", "mouthPucker",
)

FEATURE_KEYS = (
    "eye_open_r", "eye_open_l", "brow_r", "brow_l", "corner_canthus_r", "corner_canthus_l",
    "corner_lateral_r", "corner_lateral_l", "corner_vertical_r", "corner_vertical_l",
    "mouth_width", "mouth_open",
)


@dataclass
class FrameAnalysis:
    face_detected: bool
    landmarks: Optional[np.ndarray] = None       # (N, 2) normalised [0, 1] coordinates
    features: dict = field(default_factory=dict)
    pose: dict = field(default_factory=dict)      # yaw/pitch/roll in degrees, if available
    blendshapes: dict = field(default_factory=dict)
    error: Optional[str] = None


# ---------------------------------------------------------------------------
# Pure geometry (unit-tested without a camera)
# ---------------------------------------------------------------------------
def compute_frame_features(points_px: np.ndarray) -> dict:
    """Compute per-frame geometric features from pixel-space landmarks (N >= 468)."""
    p = np.asarray(points_px, dtype=float)[:, :2]
    r_center = p[list(R_EYE_RING)].mean(axis=0)
    l_center = p[list(L_EYE_RING)].mean(axis=0)
    iod = float(np.linalg.norm(l_center - r_center))
    if not math.isfinite(iod) or iod < 1e-6:
        return {}
    # Rotate so the eye line is horizontal; origin between the eyes; units of IOD.
    angle = math.atan2(l_center[1] - r_center[1], l_center[0] - r_center[0])
    c, s = math.cos(-angle), math.sin(-angle)
    rot = np.array([[c, -s], [s, c]])
    origin = (r_center + l_center) / 2.0
    q = ((p - origin) @ rot.T) / iod
    # In aligned space the person's left eye has +x when the image is un-mirrored, so
    # "lateral" distance is measured away from the midline on each side.
    midline_x = float(q[list(MIDLINE), 0].mean())

    def ear(pairs, outer, inner):
        width = np.linalg.norm(q[outer] - q[inner])
        if width < 1e-6:
            return float("nan")
        gaps = [np.linalg.norm(q[a] - q[b]) for a, b in pairs]
        return float(np.mean(gaps) / width)

    r_ref_y = float((q[R_EYE_OUTER, 1] + q[R_EYE_INNER, 1]) / 2.0)
    l_ref_y = float((q[L_EYE_OUTER, 1] + q[L_EYE_INNER, 1]) / 2.0)
    feats = {
        "eye_open_r": ear(R_EYE_LID_PAIRS, R_EYE_OUTER, R_EYE_INNER),
        "eye_open_l": ear(L_EYE_LID_PAIRS, L_EYE_OUTER, L_EYE_INNER),
        # y grows downward, so "height above the eye line" is ref_y - brow_y
        "brow_r": float(r_ref_y - q[list(R_BROW), 1].mean()),
        "brow_l": float(l_ref_y - q[list(L_BROW), 1].mean()),
        "corner_canthus_r": float(np.linalg.norm(q[R_MOUTH] - q[R_EYE_OUTER])),
        "corner_canthus_l": float(np.linalg.norm(q[L_MOUTH] - q[L_EYE_OUTER])),
        "corner_lateral_r": float(abs(q[R_MOUTH, 0] - midline_x)),
        "corner_lateral_l": float(abs(q[L_MOUTH, 0] - midline_x)),
        "corner_vertical_r": float(q[R_MOUTH, 1]),
        "corner_vertical_l": float(q[L_MOUTH, 1]),
        "mouth_width": float(np.linalg.norm(q[L_MOUTH] - q[R_MOUTH])),
        "mouth_open": float(np.linalg.norm(q[UPPER_LIP] - q[LOWER_LIP])),
    }
    return {k: v for k, v in feats.items() if math.isfinite(v)}


def pose_from_matrix(matrix) -> dict:
    """Approximate head yaw/pitch/roll (degrees) from MediaPipe's transformation matrix."""
    try:
        m = np.asarray(matrix, dtype=float).reshape(4, 4)
        r = m[:3, :3]
        sy = math.sqrt(r[0, 0] ** 2 + r[1, 0] ** 2)
        pitch = math.degrees(math.atan2(r[2, 1], r[2, 2]))
        yaw = math.degrees(math.atan2(-r[2, 0], sy))
        roll = math.degrees(math.atan2(r[1, 0], r[0, 0]))
        if not all(math.isfinite(v) for v in (pitch, yaw, roll)):
            return {}
        return {"yaw": yaw, "pitch": pitch, "roll": roll}
    except Exception:  # noqa: BLE001 - malformed matrix → no pose
        return {}


def summarize_samples(samples: list[FrameAnalysis]) -> dict:
    """Aggregate the frames captured for one expression using the median (robust to blinks)."""
    with_face = [s for s in samples if s.face_detected and s.features]
    out = {"frames_total": len(samples), "frames_with_face": len(with_face),
           "features": None, "blendshapes": None, "head_yaw_deg": None,
           "head_pitch_deg": None, "head_roll_deg": None, "quality_notes": []}
    if len(with_face) < MIN_FACE_FRAMES:
        if samples:
            out["quality_notes"].append(
                f"A face was detected in only {len(with_face)} of {len(samples)} frames, which "
                f"is not enough to calculate measurements.")
        return out
    feats = {}
    for k in FEATURE_KEYS:
        vals = [s.features[k] for s in with_face if k in s.features]
        if len(vals) >= MIN_FACE_FRAMES:
            feats[k] = float(np.median(vals))
    out["features"] = feats or None
    for axis in ("yaw", "pitch", "roll"):
        vals = [s.pose[axis] for s in with_face if axis in s.pose]
        if vals:
            out[f"head_{axis}_deg"] = float(np.median(vals))
    bs = {}
    for k in BLENDSHAPE_KEYS:
        vals = [s.blendshapes[k] for s in with_face if k in s.blendshapes]
        if vals:
            bs[k] = float(np.median(vals))
    out["blendshapes"] = bs or None
    yaw = out["head_yaw_deg"]
    if yaw is not None and abs(yaw) > HEAD_TURN_WARNING_DEG:
        out["quality_notes"].append(
            f"Head appeared turned by about {abs(yaw):.0f}°. Facing the camera directly "
            f"makes left/right comparisons more consistent.")
    if len(with_face) < len(samples) * 0.6:
        out["quality_notes"].append("The face was not visible in some frames.")
    return out


# ---------------------------------------------------------------------------
# Session-level experimental metrics
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class MetricDef:
    key: str
    label: str
    unit: str
    group: str
    side: str            # "R", "L", "ratio", "diff"
    requires: tuple
    description: str


GROUPS = ("Resting position", "Smile", "Eyebrow raise", "Eye closure", "Lip pucker")

METRIC_DEFS: tuple[MetricDef, ...] = (
    MetricDef("rest_eye_opening_ratio", "Resting eye opening — L/R similarity", "ratio",
              "Resting position", "ratio", ("neutral",),
              "Smaller eye opening divided by larger eye opening at rest (1.00 = equal)."),
    MetricDef("rest_brow_height_diff", "Resting brow height difference (L − R)", "% IOD",
              "Resting position", "diff", ("neutral",),
              "Left brow height minus right brow height above each eye line."),
    MetricDef("rest_mouth_corner_height_diff", "Resting mouth-corner height difference (L − R)",
              "% IOD", "Resting position", "diff", ("neutral",),
              "Positive values mean the left mouth corner sits lower than the right."),
    MetricDef("smile_excursion_r", "Smile — right mouth-corner movement", "% IOD", "Smile", "R",
              ("neutral", "smile"),
              "How much closer the right mouth corner moved toward the right outer eye corner."),
    MetricDef("smile_excursion_l", "Smile — left mouth-corner movement", "% IOD", "Smile", "L",
              ("neutral", "smile"),
              "How much closer the left mouth corner moved toward the left outer eye corner."),
    MetricDef("smile_lr_ratio", "Smile — L/R movement similarity", "ratio", "Smile", "ratio",
              ("neutral", "smile"), "Smaller side's movement divided by larger side's."),
    MetricDef("brow_raise_r", "Eyebrow raise — right side", "% IOD", "Eyebrow raise", "R",
              ("neutral", "brow_raise"), "Increase in right brow height compared with rest."),
    MetricDef("brow_raise_l", "Eyebrow raise — left side", "% IOD", "Eyebrow raise", "L",
              ("neutral", "brow_raise"), "Increase in left brow height compared with rest."),
    MetricDef("brow_lr_ratio", "Eyebrow raise — L/R movement similarity", "ratio",
              "Eyebrow raise", "ratio", ("neutral", "brow_raise"),
              "Smaller side's movement divided by larger side's."),
    MetricDef("eye_closure_r", "Eye closure — right eye", "% of resting opening", "Eye closure",
              "R", ("neutral", "eye_closure"),
              "Reduction in right eye opening compared with rest (100% = lids appear to meet)."),
    MetricDef("eye_closure_l", "Eye closure — left eye", "% of resting opening", "Eye closure",
              "L", ("neutral", "eye_closure"),
              "Reduction in left eye opening compared with rest (100% = lids appear to meet)."),
    MetricDef("eye_closure_lr_ratio", "Eye closure — L/R similarity", "ratio", "Eye closure",
              "ratio", ("neutral", "eye_closure"),
              "Smaller side's closure divided by larger side's."),
    MetricDef("pucker_r", "Lip pucker — right corner inward movement", "% IOD", "Lip pucker", "R",
              ("neutral", "pucker"), "How far the right mouth corner moved toward the midline."),
    MetricDef("pucker_l", "Lip pucker — left corner inward movement", "% IOD", "Lip pucker", "L",
              ("neutral", "pucker"), "How far the left mouth corner moved toward the midline."),
    MetricDef("pucker_lr_ratio", "Lip pucker — L/R movement similarity", "ratio", "Lip pucker",
              "ratio", ("neutral", "pucker"), "Smaller side's movement divided by larger side's."),
)
METRIC_BY_KEY = {m.key: m for m in METRIC_DEFS}

# Minimum movement (on the larger side) before a left/right ratio is meaningful.
_RATIO_MIN = {"Smile": 1.0, "Eyebrow raise": 1.0, "Eye closure": 10.0, "Lip pucker": 1.0}


def _ratio(a: Optional[float], b: Optional[float], minimum: float) -> tuple[Optional[float], str]:
    if a is None or b is None:
        return None, "One side could not be measured."
    hi = max(a, b)
    if hi < minimum:
        return None, "Movement on both sides was too small to compare reliably."
    return max(min(a, b), 0.0) / hi, ""


def compute_session_metrics(features_by_expr: dict[str, Optional[dict]]) -> tuple[list, list]:
    """Return ``(metrics, missing)`` for one session.

    ``features_by_expr`` maps expression keys to the aggregated feature dict (or ``None``
    when the expression was skipped or could not be analysed).
    """
    values: dict[str, Optional[float]] = {}
    reasons: dict[str, str] = {}
    f = {k: v for k, v in features_by_expr.items() if v}
    n = f.get("neutral")

    def need(*keys) -> Optional[str]:
        for k in keys:
            if k not in f:
                name = EXPRESSION_BY_KEY.get(k, {}).get("name", k)
                return f"Requires a successfully analysed “{name}” capture."
        return None

    def get(d, k):
        v = d.get(k) if d else None
        return v if v is not None and math.isfinite(v) else None

    # Resting position
    miss = need("neutral")
    if miss:
        for k in ("rest_eye_opening_ratio", "rest_brow_height_diff",
                  "rest_mouth_corner_height_diff"):
            reasons[k] = miss
    else:
        er, el = get(n, "eye_open_r"), get(n, "eye_open_l")
        if er and el:
            values["rest_eye_opening_ratio"] = min(er, el) / max(er, el)
        else:
            reasons["rest_eye_opening_ratio"] = "Eye opening could not be measured."
        br, bl = get(n, "brow_r"), get(n, "brow_l")
        if br is not None and bl is not None:
            values["rest_brow_height_diff"] = (bl - br) * 100
        else:
            reasons["rest_brow_height_diff"] = "Brow position could not be measured."
        vr, vl = get(n, "corner_vertical_r"), get(n, "corner_vertical_l")
        if vr is not None and vl is not None:
            values["rest_mouth_corner_height_diff"] = (vl - vr) * 100
        else:
            reasons["rest_mouth_corner_height_diff"] = "Mouth corners could not be measured."

    def paired(expr: str, prefix: str, ratio_key: str, group: str, fn):
        miss = need("neutral", expr)
        keys = (f"{prefix}_r", f"{prefix}_l", ratio_key)
        if miss:
            for k in keys:
                reasons[k] = miss
            return
        e = f[expr]
        for side in ("r", "l"):
            v = fn(n, e, side)
            if v is None:
                reasons[f"{prefix}_{side}"] = "The landmarks needed for this side were unavailable."
            else:
                values[f"{prefix}_{side}"] = v
        ratio, why = _ratio(values.get(keys[0]), values.get(keys[1]), _RATIO_MIN[group])
        if ratio is None:
            reasons[ratio_key] = why
        else:
            values[ratio_key] = ratio

    def smile(n_, e_, s):
        a, b = get(n_, f"corner_canthus_{s}"), get(e_, f"corner_canthus_{s}")
        return None if a is None or b is None else (a - b) * 100

    def brow(n_, e_, s):
        a, b = get(n_, f"brow_{s}"), get(e_, f"brow_{s}")
        return None if a is None or b is None else (b - a) * 100

    def closure(n_, e_, s):
        a, b = get(n_, f"eye_open_{s}"), get(e_, f"eye_open_{s}")
        if a is None or b is None or a <= 1e-6:
            return None
        return (1.0 - b / a) * 100

    def pucker(n_, e_, s):
        a, b = get(n_, f"corner_lateral_{s}"), get(e_, f"corner_lateral_{s}")
        return None if a is None or b is None else (a - b) * 100

    paired("smile", "smile_excursion", "smile_lr_ratio", "Smile", smile)
    paired("brow_raise", "brow_raise", "brow_lr_ratio", "Eyebrow raise", brow)
    paired("eye_closure", "eye_closure", "eye_closure_lr_ratio", "Eye closure", closure)
    paired("pucker", "pucker", "pucker_lr_ratio", "Lip pucker", pucker)

    metrics, missing = [], []
    for d in METRIC_DEFS:
        v = values.get(d.key)
        if v is not None and math.isfinite(v):
            metrics.append({"key": d.key, "label": d.label, "unit": d.unit, "group": d.group,
                            "side": d.side, "value": round(float(v), 4),
                            "description": d.description})
        else:
            missing.append({"key": d.key, "label": d.label, "group": d.group,
                            "reason": reasons.get(d.key, "Not available.")})
    return metrics, missing


def format_metric(value: Optional[float], unit: str) -> str:
    if value is None:
        return "—"
    if unit == "ratio":
        return f"{value:.2f}"
    if unit.startswith("%"):
        return f"{value:+.1f}%" if "IOD" in unit else f"{value:.0f}%"
    return f"{value:.2f}"


# ---------------------------------------------------------------------------
# MediaPipe wrapper
# ---------------------------------------------------------------------------
class FaceAnalyzer:
    """Thin wrapper around MediaPipe Face Landmarker (VIDEO mode, processed locally)."""

    def __init__(self, model_path: Path | str = MODEL_PATH):
        self.available = False
        self.error: Optional[str] = None
        self._lock = threading.Lock()
        self._landmarker = None
        self._last_ts = 0
        try:
            import mediapipe as mp  # noqa: F401
            from mediapipe.tasks.python import BaseOptions, vision
        except Exception as exc:  # noqa: BLE001 - any import problem disables analysis
            self.error = ("MediaPipe is not installed or could not be loaded, so facial landmark "
                          f"detection is unavailable. ({exc.__class__.__name__}: {exc})")
            log.warning(self.error)
            return
        path = Path(model_path)
        if not path.is_file():
            self.error = (f"The face landmark model file is missing:\n{path}\n\n"
                          "See README → Troubleshooting to restore it.")
            log.warning(self.error)
            return
        try:
            self._mp = mp
            options = vision.FaceLandmarkerOptions(
                # Loading from bytes avoids MediaPipe path issues with non-ASCII folders.
                base_options=BaseOptions(model_asset_buffer=path.read_bytes()),
                running_mode=vision.RunningMode.VIDEO,
                num_faces=1,
                min_face_detection_confidence=0.5,
                min_face_presence_confidence=0.5,
                min_tracking_confidence=0.5,
                output_face_blendshapes=True,
                output_facial_transformation_matrixes=True,
            )
            self._landmarker = vision.FaceLandmarker.create_from_options(options)
            self.available = True
        except Exception as exc:  # noqa: BLE001
            self.error = f"The face landmark model could not be started ({exc})."
            log.exception("Face landmarker initialisation failed")

    def process(self, rgb: np.ndarray) -> FrameAnalysis:
        if not self.available or self._landmarker is None:
            return FrameAnalysis(False, error=self.error)
        with self._lock:
            ts = max(int(time.monotonic() * 1000), self._last_ts + 1)
            self._last_ts = ts
            try:
                image = self._mp.Image(image_format=self._mp.ImageFormat.SRGB,
                                       data=np.ascontiguousarray(rgb))
                result = self._landmarker.detect_for_video(image, ts)
            except Exception as exc:  # noqa: BLE001
                log.debug("Landmark detection failed", exc_info=True)
                return FrameAnalysis(False, error=str(exc))
        if not result.face_landmarks:
            return FrameAnalysis(False)
        lms = result.face_landmarks[0]
        norm = np.array([(p.x, p.y) for p in lms], dtype=float)
        h, w = rgb.shape[:2]
        feats = compute_frame_features(norm * np.array([w, h]))
        pose = {}
        mats = getattr(result, "facial_transformation_matrixes", None)
        if mats:
            pose = pose_from_matrix(mats[0])
        bs = {}
        shapes = getattr(result, "face_blendshapes", None)
        if shapes:
            for cat in shapes[0]:
                if cat.category_name in BLENDSHAPE_KEYS:
                    bs[cat.category_name] = float(cat.score)
        return FrameAnalysis(True, norm, feats, pose, bs)

    def close(self) -> None:
        with self._lock:
            if self._landmarker is not None:
                try:
                    self._landmarker.close()
                except Exception:  # noqa: BLE001
                    pass
                self._landmarker = None
            self.available = False


def draw_overlay(rgb: np.ndarray, landmarks: np.ndarray) -> None:
    """Draw a subtle contour overlay (in place) on an RGB frame of any size."""
    import cv2

    h, w = rgb.shape[:2]
    pts = (landmarks * np.array([w, h])).astype(np.int32)
    thickness = max(1, int(round(w / 640)))
    teal = (20, 184, 166)
    for contour in ALL_CONTOURS:
        for a, b in contour:
            if a < len(pts) and b < len(pts):
                cv2.line(rgb, tuple(pts[a]), tuple(pts[b]), teal, thickness, cv2.LINE_AA)
    radius = max(2, int(round(w / 320)))
    for i in KEY_POINTS:
        if i < len(pts):
            cv2.circle(rgb, tuple(pts[i]), radius + 1, (255, 255, 255), -1, cv2.LINE_AA)
            cv2.circle(rgb, tuple(pts[i]), radius, (59, 130, 246), -1, cv2.LINE_AA)
