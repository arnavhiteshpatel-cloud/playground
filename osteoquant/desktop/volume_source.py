"""Slice-lazy access to scan images for display.

The image is never loaded as a whole for viewing: each requested slice is read from the
chunked Zarr store and kept in a byte-bounded LRU cache. 3D rendering uses a strided
(downsampled) copy limited to a voxel budget. Label volumes are loaded fully (uint8, one byte
per voxel) because editing needs random access to them.
"""
from __future__ import annotations

import threading
from collections import OrderedDict

import numpy as np

AXIS_NAMES = ("Axial", "Coronal", "Sagittal")


class LRUCache:
    def __init__(self, max_bytes: int):
        self.max_bytes = max_bytes
        self.bytes = 0
        self._d: OrderedDict = OrderedDict()
        self._lock = threading.Lock()

    def get(self, key):
        with self._lock:
            v = self._d.get(key)
            if v is not None:
                self._d.move_to_end(key)
            return v

    def put(self, key, arr: np.ndarray):
        with self._lock:
            if key in self._d:
                self.bytes -= self._d.pop(key).nbytes
            self._d[key] = arr
            self.bytes += arr.nbytes
            while self.bytes > self.max_bytes and len(self._d) > 1:
                _, old = self._d.popitem(last=False)
                self.bytes -= old.nbytes

    def clear(self):
        with self._lock:
            self._d.clear()
            self.bytes = 0


class VolumeSource:
    """Common interface. Subclasses implement ``_read(index_tuple) -> ndarray``."""

    shape: tuple
    dtype: np.dtype
    spacing: tuple
    origin: tuple = (0.0, 0.0, 0.0)

    def __init__(self, cache_bytes: int = 256 << 20):
        self.cache = LRUCache(cache_bytes)
        self._stats = None

    def _read(self, idx) -> np.ndarray:
        raise NotImplementedError

    def slice(self, axis: int, index: int) -> np.ndarray:
        index = int(np.clip(index, 0, self.shape[axis] - 1))
        key = (axis, index)
        s = self.cache.get(key)
        if s is None:
            sl = [slice(None)] * 3
            sl[axis] = index
            s = np.asarray(self._read(tuple(sl)))
            self.cache.put(key, s)
        return s

    def value(self, z, y, x) -> float:
        return float(self.slice(0, z)[y, x])

    def block(self, lo, hi) -> np.ndarray:
        return np.asarray(self._read(tuple(slice(int(a), int(b)) for a, b in zip(lo, hi))))

    def stats(self) -> dict:
        """Intensity percentiles from a strided sample (window/level defaults)."""
        if self._stats is None:
            st = [max(1, n // 48) for n in self.shape]
            s = np.asarray(self._read((slice(None, None, st[0]), slice(None, None, st[1]),
                                       slice(None, None, st[2])))).astype(np.float32)
            s = s[np.isfinite(s)]
            self._stats = {"min": float(s.min()), "max": float(s.max()), "p1": float(np.percentile(s, 1)),
                           "p50": float(np.percentile(s, 50)), "p99": float(np.percentile(s, 99.5)),
                           "hist": np.histogram(s, bins=128)}
        return self._stats

    def downsample_step(self, max_voxels: int) -> int:
        step = 1
        while np.prod([int(np.ceil(n / step)) for n in self.shape]) > max_voxels:
            step += 1
        return step

    def downsampled(self, max_voxels: int = 160 ** 3) -> tuple[np.ndarray, int]:
        step = self.downsample_step(max_voxels)
        return np.asarray(self._read((slice(None, None, step),) * 3)), step

    @property
    def nbytes(self) -> int:
        return int(np.prod(self.shape)) * np.dtype(self.dtype).itemsize


class ArraySource(VolumeSource):
    def __init__(self, data: np.ndarray, spacing=(1.0, 1.0, 1.0), origin=(0.0, 0.0, 0.0), cache_bytes=64 << 20):
        super().__init__(cache_bytes)
        self.data = data
        self.shape, self.dtype = tuple(data.shape), data.dtype
        self.spacing, self.origin = tuple(map(float, spacing)), tuple(map(float, origin))

    def _read(self, idx):
        return self.data[idx]


class ZarrSource(VolumeSource):
    """Image of a stored scan (``<scan>.zarr/image``)."""

    def __init__(self, store_path, cache_bytes: int = 256 << 20):
        import zarr
        super().__init__(cache_bytes)
        self.path = str(store_path)
        self.group = zarr.open_group(self.path, mode="r")
        self.array = self.group["image"]
        attrs = dict(self.group.attrs)
        self.shape, self.dtype = tuple(self.array.shape), np.dtype(self.array.dtype)
        self.spacing = tuple(float(s) for s in attrs.get("spacing_um", (1.0, 1.0, 1.0)))
        self.origin = tuple(float(s) for s in attrs.get("origin_um", (0.0, 0.0, 0.0)))
        self._lock = threading.Lock()

    def _read(self, idx):
        with self._lock:
            return self.array[idx]

    def label_layers(self) -> list[str]:
        return sorted(self.group["labels"].keys()) if "labels" in self.group else []

    def load_labels(self, key: str) -> np.ndarray:
        return np.ascontiguousarray(np.asarray(self.group[f"labels/{key}"][:]), dtype=np.uint8)
