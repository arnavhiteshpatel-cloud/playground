"""Segmentation editing on an in-memory uint8 label volume, with compressed sparse diffs.

Every edit produces a ``SparseDiff``: the sorted flat indices of the voxels that actually
changed (delta-encoded, narrowed to the smallest integer type, zlib-compressed) plus the old
and new label values (zlib-compressed). Undo/redo applies the diff backward/forward, so memory
grows with the number of changed voxels, never with the volume size. A brush stroke of
radius 5 on a 2000^3 volume costs a few hundred bytes of history.

All operations are pure NumPy/SciPy and independent of Qt so they can be unit-tested; the
QUndoStack integration lives in ``undo.py``.
"""
from __future__ import annotations

import zlib
from dataclasses import dataclass

import numpy as np
from scipy import ndimage as ndi

from .. import LABELS

VALID_LABELS = tuple(LABELS)


def _narrow(a: np.ndarray) -> np.ndarray:
    m = int(a.max()) if a.size else 0
    for dt in (np.uint8, np.uint16, np.uint32):
        if m <= np.iinfo(dt).max:
            return a.astype(dt)
    return a.astype(np.int64)


@dataclass
class SparseDiff:
    shape: tuple
    n: int
    _idx: bytes
    _idx_dtype: str
    _old: bytes
    _new: bytes
    bbox: tuple                 # ((z0,z1),(y0,y1),(x0,x1)) inclusive-exclusive
    class_delta: dict           # label -> voxel count change (forward direction)

    @classmethod
    def build(cls, shape, flat_idx: np.ndarray, old: np.ndarray, new: np.ndarray) -> "SparseDiff":
        order = np.argsort(flat_idx, kind="stable")
        idx = flat_idx[order].astype(np.int64)
        old, new = old[order].astype(np.uint8), new[order].astype(np.uint8)
        d = np.diff(idx, prepend=0)
        dn = _narrow(d)
        zyx = np.unravel_index(idx, shape)
        bbox = tuple((int(a.min()), int(a.max()) + 1) for a in zyx) if idx.size else ((0, 0),) * 3
        delta: dict[int, int] = {}
        for lab, cnt in zip(*np.unique(new, return_counts=True)):
            delta[int(lab)] = delta.get(int(lab), 0) + int(cnt)
        for lab, cnt in zip(*np.unique(old, return_counts=True)):
            delta[int(lab)] = delta.get(int(lab), 0) - int(cnt)
        delta = {k: v for k, v in delta.items() if v}
        return cls(tuple(shape), int(idx.size), zlib.compress(dn.tobytes(), 6), str(dn.dtype),
                   zlib.compress(old.tobytes(), 6), zlib.compress(new.tobytes(), 6), bbox, delta)

    def indices(self) -> np.ndarray:
        d = np.frombuffer(zlib.decompress(self._idx), dtype=self._idx_dtype).astype(np.int64)
        return np.cumsum(d)

    def values(self, forward: bool) -> np.ndarray:
        return np.frombuffer(zlib.decompress(self._new if forward else self._old), dtype=np.uint8)

    def apply(self, labels: np.ndarray, forward: bool = True):
        if self.n:
            labels.reshape(-1)[self.indices()] = self.values(forward)

    @property
    def nbytes(self) -> int:
        return len(self._idx) + len(self._old) + len(self._new)

    def slices_touched(self, axis: int) -> range:
        lo, hi = self.bbox[axis]
        return range(lo, hi)


class LabelEditor:
    """Holds the editable label volume and applies operations, returning SparseDiffs.

    ``labels`` must be a C-contiguous uint8 array that the editor owns. ``spacing`` is the
    voxel size (z, y, x) in µm; brush radii are physical (µm) so anisotropic voxels give
    round brushes in physical space.
    """

    def __init__(self, labels: np.ndarray, spacing=(1.0, 1.0, 1.0)):
        if labels.dtype != np.uint8 or labels.ndim != 3:
            raise ValueError("labels must be a 3D uint8 array")
        self.labels = np.ascontiguousarray(labels)
        self.spacing = tuple(float(s) for s in spacing)
        bc = np.bincount(self.labels.ravel(), minlength=256)
        self.base_counts = {c: int(bc[c]) for c in VALID_LABELS}
        self.counts = dict(self.base_counts)
        self.op_counts: dict[str, int] = {}

    @property
    def shape(self):
        return self.labels.shape

    # ------------------------------------------------------------------ core
    def commit(self, flat_idx: np.ndarray, value: int, only_from=None, tool: str = "edit") -> SparseDiff | None:
        """Set ``value`` at ``flat_idx`` (restricted to voxels whose current label is in
        ``only_from`` if given). Returns the diff, or None if nothing changed."""
        if value not in VALID_LABELS:
            raise ValueError(f"invalid label {value}")
        flat = self.labels.reshape(-1)
        idx = np.unique(np.asarray(flat_idx, dtype=np.int64))
        cur = flat[idx]
        keep = cur != value
        if only_from is not None:
            allowed = np.array(sorted({int(v) for v in np.atleast_1d(only_from)}), dtype=np.uint8)
            keep &= np.isin(cur, allowed)
        idx, cur = idx[keep], cur[keep]
        if idx.size == 0:
            return None
        new = np.full(idx.size, value, np.uint8)
        diff = SparseDiff.build(self.labels.shape, idx, cur, new)
        flat[idx] = value
        self._count(diff, True)
        self.op_counts[tool] = self.op_counts.get(tool, 0) + 1
        return diff

    def apply_diff(self, diff: SparseDiff, forward: bool):
        diff.apply(self.labels, forward)
        self._count(diff, forward)

    def _count(self, diff: SparseDiff, forward: bool):
        s = 1 if forward else -1
        for k, v in diff.class_delta.items():
            self.counts[k] = self.counts.get(k, 0) + s * v

    def change_summary(self) -> dict:
        """Per-class voxel count change since the editor was created."""
        return {LABELS[c]: self.counts[c] - self.base_counts[c] for c in VALID_LABELS
                if self.counts[c] != self.base_counts[c]}

    @property
    def modified(self) -> bool:
        return bool(self.change_summary())

    # ------------------------------------------------------------------ geometry helpers
    @staticmethod
    def plane_axes(axis: int) -> tuple[int, int]:
        return tuple(a for a in (0, 1, 2) if a != axis)  # type: ignore[return-value]

    def _plane_to_flat(self, axis: int, index: int, rows: np.ndarray, cols: np.ndarray) -> np.ndarray:
        a, b = self.plane_axes(axis)
        coords = [None, None, None]
        coords[axis] = np.full(rows.shape, index, np.int64)
        coords[a], coords[b] = rows, cols
        return np.ravel_multi_index(coords, self.labels.shape)

    def plane(self, axis: int, index: int) -> np.ndarray:
        sl = [slice(None)] * 3
        sl[axis] = index
        return self.labels[tuple(sl)]

    def disk(self, axis: int, index: int, row: float, col: float, radius_um: float) -> tuple[np.ndarray, np.ndarray]:
        a, b = self.plane_axes(axis)
        ra = max(radius_um / self.spacing[a], 0.5)
        rb = max(radius_um / self.spacing[b], 0.5)
        na, nb = self.labels.shape[a], self.labels.shape[b]
        r0, r1 = max(0, int(np.floor(row - ra))), min(na, int(np.ceil(row + ra)) + 1)
        c0, c1 = max(0, int(np.floor(col - rb))), min(nb, int(np.ceil(col + rb)) + 1)
        if r0 >= r1 or c0 >= c1 or not 0 <= index < self.labels.shape[axis]:
            return np.empty(0, np.int64), np.empty(0, np.int64)
        rr, cc = np.mgrid[r0:r1, c0:c1]
        m = ((rr - row) / ra) ** 2 + ((cc - col) / rb) ** 2 <= 1.0
        return rr[m].astype(np.int64), cc[m].astype(np.int64)

    # ------------------------------------------------------------------ tools
    def brush_2d(self, axis, index, row, col, radius_um, value, only_from=None) -> SparseDiff | None:
        rr, cc = self.disk(axis, index, row, col, radius_um)
        if rr.size == 0:
            return None
        return self.commit(self._plane_to_flat(axis, index, rr, cc), value, only_from, "brush2d")

    def stroke_2d(self, axis, index, points, radius_um, value, only_from=None) -> SparseDiff | None:
        """A whole mouse stroke (list of (row, col)) as one undoable diff; gaps between
        successive points are filled so fast strokes stay continuous."""
        pts = []
        a, b = self.plane_axes(axis)
        step = max(0.5, 0.5 * radius_um / max(self.spacing[a], self.spacing[b]))
        for i, (r, c) in enumerate(points):
            if i:
                r0, c0 = points[i - 1]
                n = int(np.ceil(np.hypot(r - r0, c - c0) / step))
                for t in np.linspace(0, 1, n + 1)[1:]:
                    pts.append((r0 + t * (r - r0), c0 + t * (c - c0)))
            else:
                pts.append((r, c))
        idx = []
        for r, c in pts:
            rr, cc = self.disk(axis, index, r, c, radius_um)
            if rr.size:
                idx.append(self._plane_to_flat(axis, index, rr, cc))
        if not idx:
            return None
        return self.commit(np.concatenate(idx), value, only_from, "brush2d")

    def sphere_indices(self, center, radius_um) -> np.ndarray:
        rz, ry, rx = (max(radius_um / s, 0.5) for s in self.spacing)
        z, y, x = center
        lo = [max(0, int(np.floor(c - r))) for c, r in zip((z, y, x), (rz, ry, rx))]
        hi = [min(n, int(np.ceil(c + r)) + 1) for c, r, n in zip((z, y, x), (rz, ry, rx), self.labels.shape)]
        if any(l >= h for l, h in zip(lo, hi)):
            return np.empty(0, np.int64)
        zz, yy, xx = np.mgrid[lo[0]:hi[0], lo[1]:hi[1], lo[2]:hi[2]]
        m = ((zz - z) / rz) ** 2 + ((yy - y) / ry) ** 2 + ((xx - x) / rx) ** 2 <= 1.0
        return np.ravel_multi_index((zz[m], yy[m], xx[m]), self.labels.shape)

    def brush_3d(self, center, radius_um, value, only_from=None) -> SparseDiff | None:
        idx = self.sphere_indices(center, radius_um)
        if idx.size == 0:
            return None
        return self.commit(idx, value, only_from, "brush3d")

    def stroke_3d(self, centers, radius_um, value, only_from=None) -> SparseDiff | None:
        idx = [self.sphere_indices(c, radius_um) for c in centers]
        idx = [i for i in idx if i.size]
        if not idx:
            return None
        return self.commit(np.concatenate(idx), value, only_from, "brush3d")

    def region_grow(self, image_block, block_origin, seed, tolerance: float, value: int, only_from=None,
                    axis: int | None = None) -> SparseDiff | None:
        """Grow from ``seed`` (z, y, x, absolute) over voxels whose intensity is within
        ``tolerance`` of the seed intensity, 6/4-connected. ``image_block`` is the image region
        starting at ``block_origin`` (bounded region supplied by the caller). With ``axis`` set
        the grow is restricted to the seed's slice on that axis (2D mode)."""
        img = np.asarray(image_block, dtype=np.float32)
        s = tuple(int(c - o) for c, o in zip(seed, block_origin))
        if any(not 0 <= v < n for v, n in zip(s, img.shape)):
            return None
        ref = float(img[s])
        cand = np.abs(img - ref) <= float(tolerance)
        if axis is not None:
            keep = np.zeros_like(cand)
            sl = [slice(None)] * 3
            sl[axis] = s[axis]
            keep[tuple(sl)] = True
            cand &= keep
        lab, _ = ndi.label(cand)
        comp = lab == lab[s]
        zz, yy, xx = np.nonzero(comp)
        idx = np.ravel_multi_index((zz + block_origin[0], yy + block_origin[1], xx + block_origin[2]), self.labels.shape)
        return self.commit(idx, value, only_from, "region_grow")

    def fill_holes(self, axis: int, index: int, value: int) -> SparseDiff | None:
        """Fill enclosed holes of class ``value`` on one slice."""
        p = self.plane(axis, index)
        m = p == value
        if not m.any():
            return None
        filled = ndi.binary_fill_holes(m) & ~m
        rr, cc = np.nonzero(filled)
        if rr.size == 0:
            return None
        return self.commit(self._plane_to_flat(axis, index, rr, cc), value, None, "fill_holes")

    @staticmethod
    def _sdt(mask: np.ndarray) -> np.ndarray:
        if not mask.any():
            return np.full(mask.shape, -1e6, np.float32)
        inside = ndi.distance_transform_edt(mask)
        outside = ndi.distance_transform_edt(~mask)
        return (inside - outside).astype(np.float32)

    def interpolate(self, axis: int, i0: int, i1: int, value: int, overwrite: bool = False) -> SparseDiff | None:
        """Shape-based interpolation of class ``value`` between slices ``i0`` and ``i1`` (both
        edited/key slices) using linearly blended signed distance maps. Only background voxels
        are changed unless ``overwrite``."""
        if i0 > i1:
            i0, i1 = i1, i0
        if i1 - i0 < 2:
            return None
        m0, m1 = self.plane(axis, i0) == value, self.plane(axis, i1) == value
        if not (m0.any() and m1.any()):
            raise ValueError("Both key slices must contain the class to interpolate")
        d0, d1 = self._sdt(m0), self._sdt(m1)
        idx = []
        for k in range(i0 + 1, i1):
            t = (k - i0) / (i1 - i0)
            m = (1 - t) * d0 + t * d1 > 0
            rr, cc = np.nonzero(m)
            if rr.size:
                idx.append(self._plane_to_flat(axis, k, rr, cc))
        if not idx:
            return None
        return self.commit(np.concatenate(idx), value, None if overwrite else (0,), "interpolate")
