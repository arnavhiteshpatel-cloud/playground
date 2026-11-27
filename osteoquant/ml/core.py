"""Torch-free core of the ML package: data container, input normalisation, sliding-window weights, model paths.

Separated from ``ml.train`` so that inference with ONNX Runtime (``ml.runtime``) and the desktop bundle do not
import PyTorch (desktop review: the default bundle excludes PyTorch to save ~1 GB).
"""
from __future__ import annotations

import os as _os
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

MODEL_DIR = Path(_os.environ["OQ_MODEL_DIR"]) if _os.environ.get("OQ_MODEL_DIR") else Path(__file__).resolve().parents[2] / "models"
MODEL_NAME_RE = r"^[A-Za-z0-9_\-]{1,64}$"


@dataclass
class Case:
    case_id: str
    image: np.ndarray          # float32 (z,y,x), raw grey
    labels: np.ndarray | None  # uint8, 255 = ignore
    roi: np.ndarray | None
    spacing: tuple = (40.0, 40.0, 40.0)
    # Safe defaults (cycle-1 review IP): a case is NOT commercial-eligible unless its licence is stated explicitly
    provenance: str = "unspecified"
    commercial_use: str = "unclear"
    meta: dict = field(default_factory=dict)


def normalize_image(img: np.ndarray, roi: np.ndarray | None = None, mode="percentile") -> np.ndarray:
    """Robust per-volume normalisation (cross-scanner harmonisation step)."""
    x = img.astype(np.float32)
    s = x[:: max(1, x.shape[0] // 32)]
    if mode == "percentile":
        lo, hi = np.percentile(s, [1, 99.8])
    elif mode == "zscore":
        m, sd = float(s.mean()), float(s.std()) + 1e-6
        return (x - m) / sd
    else:
        raise ValueError(mode)
    return (x - lo) / max(hi - lo, 1e-6)


def build_input(case: Case, cfg: dict) -> np.ndarray:
    chans = [normalize_image(case.image, mode=cfg.get("norm", "percentile"))]
    if cfg.get("roi_channel", False):
        r = case.roi if case.roi is not None else np.zeros(case.image.shape, bool)
        chans.append(r.astype(np.float32))
    if cfg.get("roi_distance_channel", False):
        from scipy import ndimage as ndi
        r = case.roi if case.roi is not None else np.zeros(case.image.shape, bool)
        d_in = ndi.distance_transform_edt(r, sampling=case.spacing)
        d_out = ndi.distance_transform_edt(~r, sampling=case.spacing)
        chans.append(np.tanh((d_in - d_out) / 500.0).astype(np.float32))
    return np.stack(chans).astype(np.float32)


def _gauss_window(ps, sigma_scale=0.125):
    g = [np.exp(-0.5 * ((np.arange(p) - (p - 1) / 2) / (p * sigma_scale)) ** 2) for p in ps]
    w = g[0][:, None, None] * g[1][None, :, None] * g[2][None, None, :]
    return (w / w.max()).astype(np.float32) + 1e-3
