"""Core in-memory representation of a 3D image volume.

Conventions (enforced everywhere in OsteoQuant):
  * array axis order is (z, y, x)
  * spacing is in micrometres (µm), ordered (z, y, x)
  * origin is in micrometres, (z, y, x)
  * direction is a 3x3 matrix mapping index axes (z,y,x) to physical axes; identity by default
  * intensity units are recorded explicitly in ``meta["intensity_unit"]``
    ("raw" grey values unless a calibration has been applied).
"""
from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass, field
from typing import Any

import numpy as np


@dataclass
class Volume:
    data: np.ndarray
    spacing: tuple[float, float, float] = (1.0, 1.0, 1.0)
    origin: tuple[float, float, float] = (0.0, 0.0, 0.0)
    direction: np.ndarray = field(default_factory=lambda: np.eye(3))
    meta: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.data.ndim != 3:
            raise ValueError(f"Volume requires 3D data, got shape {self.data.shape}")
        self.spacing = tuple(float(s) for s in self.spacing)
        if any((not np.isfinite(s)) or s <= 0 for s in self.spacing):
            raise ValueError(f"Invalid voxel spacing {self.spacing}; must be positive finite µm")
        self.origin = tuple(float(o) for o in self.origin)
        self.direction = np.asarray(self.direction, dtype=float).reshape(3, 3)
        self.meta.setdefault("intensity_unit", "raw")
        self.meta.setdefault("spacing_unit", "um")

    # ------------------------------------------------------------------ geometry
    @property
    def shape(self):
        return self.data.shape

    @property
    def voxel_volume_um3(self) -> float:
        return float(np.prod(self.spacing))

    @property
    def voxel_volume_mm3(self) -> float:
        return self.voxel_volume_um3 * 1e-9

    @property
    def is_isotropic(self) -> bool:
        s = np.array(self.spacing)
        return bool(np.allclose(s, s[0], rtol=1e-3))

    def index_to_physical(self, idx) -> np.ndarray:
        idx = np.asarray(idx, dtype=float)
        return np.asarray(self.origin) + self.direction @ (idx * np.asarray(self.spacing))

    def physical_to_index(self, p) -> np.ndarray:
        p = np.asarray(p, dtype=float) - np.asarray(self.origin)
        return np.linalg.solve(self.direction, p) / np.asarray(self.spacing)

    def physical_extent_um(self):
        return tuple(n * s for n, s in zip(self.shape, self.spacing))

    # ------------------------------------------------------------------ helpers
    def with_data(self, data: np.ndarray, **meta_updates) -> "Volume":
        m = copy.deepcopy(self.meta)
        m.update(meta_updates)
        return Volume(data, self.spacing, self.origin, self.direction.copy(), m)

    def content_hash(self) -> str:
        """SHA-256 over array bytes + shape + dtype + spacing (provenance identity)."""
        h = hashlib.sha256()
        h.update(json.dumps({"shape": list(self.shape), "dtype": str(self.data.dtype),
                             "spacing": list(self.spacing)}).encode())
        arr = np.ascontiguousarray(self.data)
        # hash in slabs to keep memory bounded
        for z in range(0, arr.shape[0], 64):
            h.update(arr[z:z + 64].tobytes())
        return h.hexdigest()

    def summary(self) -> dict:
        d = self.data
        sample = d[:: max(1, d.shape[0] // 32)]
        return {
            "shape": list(d.shape),
            "dtype": str(d.dtype),
            "spacing_um": list(self.spacing),
            "origin_um": list(self.origin),
            "isotropic": self.is_isotropic,
            "extent_mm": [round(e / 1000, 4) for e in self.physical_extent_um()],
            "intensity_unit": self.meta.get("intensity_unit"),
            "min": float(sample.min()), "max": float(sample.max()),
            "mean": float(sample.mean()), "std": float(sample.std()),
            "size_mb": round(d.nbytes / 1e6, 2),
        }
