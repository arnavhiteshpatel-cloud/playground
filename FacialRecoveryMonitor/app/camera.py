"""Webcam access with OpenCV.

The camera is only opened when the user explicitly turns it on. Frames are read
and analysed on a background thread; the UI polls :meth:`CameraManager.latest`.
Nothing is written to disk by this module — raw frames live only in memory.
"""

from __future__ import annotations

import logging
import threading
import time
from dataclasses import dataclass
from typing import Optional

import numpy as np

from .config import ANALYSIS_MAX_WIDTH, IS_MAC, IS_WINDOWS
from .facial_analysis import FaceAnalyzer, FrameAnalysis, draw_overlay

log = logging.getLogger(__name__)

try:
    import cv2
    CV2_ERROR: Optional[str] = None
except Exception as _exc:  # noqa: BLE001
    cv2 = None  # type: ignore[assignment]
    CV2_ERROR = f"OpenCV could not be loaded ({_exc})."


def _backend() -> int:
    if cv2 is None:
        return 0
    if IS_WINDOWS:
        return cv2.CAP_DSHOW  # opens much faster than MSMF on most Windows laptops
    if IS_MAC:
        return cv2.CAP_AVFOUNDATION
    return cv2.CAP_ANY


def permission_hint() -> str:
    if IS_MAC:
        return ("On macOS, open System Settings → Privacy & Security → Camera and allow access "
                "for the app you launched this program from (for example Terminal or VS Code), "
                "then restart it.")
    if IS_WINDOWS:
        return ("On Windows, open Settings → Privacy & security → Camera and make sure "
                "“Camera access” and “Let desktop apps access your camera” are turned on.")
    return ("On Linux, make sure your user can access /dev/video* (for example by being in the "
            "“video” group) and that no other application is using the camera.")


def probe_cameras(max_index: int = 5) -> list[int]:
    """Return indices of cameras that can be opened and deliver a frame."""
    found = []
    if cv2 is None:
        return found
    for i in range(max_index):
        cap = None
        try:
            cap = cv2.VideoCapture(i, _backend())
            if cap is not None and cap.isOpened():
                ok, _ = cap.read()
                if ok:
                    found.append(i)
        except Exception:  # noqa: BLE001
            log.debug("Probe of camera %s failed", i, exc_info=True)
        finally:
            if cap is not None:
                cap.release()
    return found


@dataclass
class FramePacket:
    frame_id: int
    display: np.ndarray             # RGB, overlay drawn, mirrored if requested
    analysis: FrameAnalysis
    fps: float


class CameraManager:
    def __init__(self, analyzer: Optional[FaceAnalyzer] = None):
        self.analyzer = analyzer
        self.mirror = True
        self.overlay = True
        self.camera_index: Optional[int] = None
        self.error: Optional[str] = None
        self._cap = None
        self._thread: Optional[threading.Thread] = None
        self._stop = threading.Event()
        self._lock = threading.Lock()
        self._latest: Optional[FramePacket] = None
        self._frame_id = 0
        # sampling state (explicit capture only)
        self._sampling = False
        self._sample_deadline = 0.0
        self._sample_max = 0
        self._samples: list[FrameAnalysis] = []
        self._sample_frame: Optional[np.ndarray] = None
        self._keep_frame = False

    # ------------------------------------------------------------------ control
    @property
    def running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def start(self, index: int) -> tuple[bool, str]:
        """Open camera ``index``. Must be called from the main (UI) thread."""
        self.stop()
        self.error = None
        if cv2 is None:
            self.error = CV2_ERROR or "OpenCV is unavailable."
            return False, self.error
        try:
            cap = cv2.VideoCapture(int(index), _backend())
        except Exception as exc:  # noqa: BLE001
            cap = None
            log.exception("VideoCapture raised")
            self.error = f"The camera could not be initialised ({exc})."
        if cap is None or not cap.isOpened():
            if cap is not None:
                cap.release()
            self.error = self.error or (
                f"Camera {index} could not be opened. It may be disconnected, in use by another "
                f"application, or camera permission may have been denied.\n\n{permission_hint()}")
            return False, self.error
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        ok, frame = False, None
        for _ in range(15):  # some cameras deliver a few empty frames while warming up
            ok, frame = cap.read()
            if ok and frame is not None:
                break
            time.sleep(0.05)
        if not ok or frame is None:
            cap.release()
            self.error = (f"Camera {index} opened but did not deliver any images. Camera access "
                          f"may be blocked.\n\n{permission_hint()}")
            return False, self.error
        self._cap = cap
        self.camera_index = int(index)
        self._stop.clear()
        self._thread = threading.Thread(target=self._run, name="camera-worker", daemon=True)
        self._thread.start()
        return True, f"Camera {index} is on"

    def stop(self) -> None:
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=2.0)
        self._thread = None
        if self._cap is not None:
            try:
                self._cap.release()
            except Exception:  # noqa: BLE001
                pass
        self._cap = None
        with self._lock:
            self._latest = None
            self._sampling = False
            self._sample_frame = None

    def latest(self) -> Optional[FramePacket]:
        with self._lock:
            return self._latest

    # ----------------------------------------------------------------- sampling
    def begin_sampling(self, seconds: float, max_frames: int, keep_frame: bool = False) -> None:
        with self._lock:
            self._samples = []
            self._sample_frame = None
            self._keep_frame = keep_frame
            self._sample_deadline = time.monotonic() + seconds
            self._sample_max = max_frames
            self._sampling = True

    def sampling_done(self) -> bool:
        with self._lock:
            if self._sampling and time.monotonic() >= self._sample_deadline + 0.5:
                self._sampling = False  # safety net if the worker stalled
            return not self._sampling

    def collect_samples(self) -> tuple[list[FrameAnalysis], Optional[np.ndarray]]:
        """Return the captured analyses and (only if requested) one raw RGB frame."""
        with self._lock:
            samples, frame = self._samples, self._sample_frame
            self._samples, self._sample_frame = [], None
            return samples, frame

    # ------------------------------------------------------------------- worker
    def _run(self) -> None:
        failures = 0
        last_t = time.monotonic()
        fps = 0.0
        while not self._stop.is_set():
            cap = self._cap
            if cap is None:
                break
            try:
                ok, bgr = cap.read()
            except Exception:  # noqa: BLE001
                ok, bgr = False, None
            if not ok or bgr is None:
                failures += 1
                if failures > 40:
                    self.error = ("The camera stopped sending images. It may have been "
                                  "disconnected or taken over by another application.")
                    log.warning(self.error)
                    with self._lock:
                        self._latest = None
                    break
                time.sleep(0.03)
                continue
            failures = 0
            rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
            h, w = rgb.shape[:2]
            if w > ANALYSIS_MAX_WIDTH:
                scale = ANALYSIS_MAX_WIDTH / w
                small = cv2.resize(rgb, (ANALYSIS_MAX_WIDTH, int(h * scale)),
                                   interpolation=cv2.INTER_AREA)
            else:
                small = rgb
            if self.analyzer is not None and self.analyzer.available:
                analysis = self.analyzer.process(small)
            else:
                analysis = FrameAnalysis(False, error="analysis unavailable")
            display = small.copy() if w > 960 else rgb.copy()
            if self.overlay and analysis.face_detected and analysis.landmarks is not None:
                draw_overlay(display, analysis.landmarks)
            if self.mirror:
                display = np.ascontiguousarray(display[:, ::-1])
            now = time.monotonic()
            dt = now - last_t
            last_t = now
            if dt > 0:
                fps = 0.85 * fps + 0.15 * (1.0 / dt) if fps else 1.0 / dt
            with self._lock:
                self._frame_id += 1
                self._latest = FramePacket(self._frame_id, display, analysis, fps)
                if self._sampling:
                    if now <= self._sample_deadline and len(self._samples) < self._sample_max:
                        self._samples.append(analysis)
                        if self._keep_frame and analysis.face_detected:
                            self._sample_frame = rgb  # newest face frame; never written to disk here
                    else:
                        self._sampling = False
