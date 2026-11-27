"""Viewer model/controller shared by the slice views, the 3D view and the tool panels.

Holds the open scan (lazy image source), the editable labels, crosshair position,
window/level, overlay display settings and the active editing tool. Widgets observe it through
signals; all edits go through it so they land on the undo stack.
"""
from __future__ import annotations

import numpy as np
from PySide6.QtCore import QObject, Signal

from .. import LABEL_COLORS, LABELS
from .editing import LabelEditor
from .undo import EditHistory
from .volume_source import VolumeSource

TOOLS = ("navigate", "brush", "erase", "grow", "fill")
EDIT_LABELS = (1, 2, 3, 255)
CLASS_NAMES = {0: "Background", 1: "New bone", 2: "Residual graft", 3: "Host bone", 255: "Uncertain"}


def window_presets(stats: dict) -> dict[str, tuple[float, float]]:
    """Window presets for uncalibrated grey values are defined on the scan's own histogram."""
    p1, p50, p99, mn, mx = stats["p1"], stats["p50"], stats["p99"], stats["min"], stats["max"]
    return {"Auto (1-99.5 %)": (p1, p99), "Full range": (mn, mx), "Mineralised (median-max)": (p50, mx),
            "Soft tissue (1 % - median)": (p1, p50 + 0.25 * (p99 - p50))}


class ViewerState(QObject):
    scan_changed = Signal()
    cursor_changed = Signal(int, int, int)
    window_changed = Signal(float, float)
    labels_changed = Signal(object)          # bbox ((z0,z1),(y0,y1),(x0,x1)) or None for everything
    overlay_changed = Signal()
    tool_changed = Signal()
    hover_changed = Signal(object)           # (z, y, x) or None
    message = Signal(str)
    edit_applied = Signal(str, object)       # tool, per-class voxel delta of the edit

    def __init__(self, parent=None):
        super().__init__(parent)
        self.source: VolumeSource | None = None
        self.editor: LabelEditor | None = None
        self.history = EditHistory(self)
        self.scan: dict | None = None
        self.segmentation: dict | None = None
        self.cursor = [0, 0, 0]
        self.window = (0.0, 1.0)
        self.show_overlay = True
        self.overlay = {c: {"visible": True, "opacity": 0.55, "color": tuple(LABEL_COLORS[c][:3])} for c in EDIT_LABELS}
        self.tool = "navigate"
        self.active_label = 1
        self.brush_radius_um = 0.0
        self.brush_3d = False
        self.protect_other_classes = True
        self.grow_tolerance = 100.0
        self.grow_3d = False
        self.grow_radius_vox = 48
        self.key_slices: dict[int, list[int]] = {0: [], 1: [], 2: []}
        self._lut = None
        self._rebuild_lut()

    # ------------------------------------------------------------------ scan
    def load(self, source: VolumeSource, labels: np.ndarray | None = None, scan: dict | None = None,
             segmentation: dict | None = None):
        self.source = source
        self.scan, self.segmentation = scan, segmentation
        self.editor = LabelEditor(labels, source.spacing) if labels is not None else None
        self.history.clear()
        self.history.setClean()
        self.key_slices = {0: [], 1: [], 2: []}
        self.cursor = [n // 2 for n in source.shape]
        st = source.stats()
        self.window = (st["p1"], st["p99"])
        if self.brush_radius_um <= 0:
            self.brush_radius_um = 3 * min(source.spacing)
        self.grow_tolerance = max(1e-3, 0.08 * (st["p99"] - st["p1"]))
        self.scan_changed.emit()
        self.window_changed.emit(*self.window)
        self.cursor_changed.emit(*self.cursor)

    def unload(self):
        self.source = None
        self.editor = None
        self.scan = self.segmentation = None
        self.history.clear()
        self.scan_changed.emit()

    @property
    def loaded(self) -> bool:
        return self.source is not None

    @property
    def shape(self):
        return self.source.shape if self.source else (1, 1, 1)

    @property
    def spacing(self):
        return self.source.spacing if self.source else (1.0, 1.0, 1.0)

    def image_slice(self, axis, index) -> np.ndarray:
        return self.source.slice(axis, index)

    def label_slice(self, axis, index) -> np.ndarray | None:
        if self.editor is None:
            return None
        return self.editor.plane(axis, int(np.clip(index, 0, self.shape[axis] - 1)))

    # ------------------------------------------------------------------ navigation / display
    def set_cursor(self, z, y, x):
        c = [int(np.clip(v, 0, n - 1)) for v, n in zip((z, y, x), self.shape)]
        if c != self.cursor:
            self.cursor = c
            self.cursor_changed.emit(*c)

    def set_index(self, axis, index):
        c = list(self.cursor)
        c[axis] = index
        self.set_cursor(*c)

    def set_window(self, lo, hi):
        if hi <= lo:
            hi = lo + 1e-6
        self.window = (float(lo), float(hi))
        self.window_changed.emit(*self.window)

    def presets(self) -> dict:
        return window_presets(self.source.stats()) if self.source else {}

    def set_overlay(self, label, **kw):
        self.overlay[label].update(kw)
        self._rebuild_lut()
        self.overlay_changed.emit()

    def set_show_overlay(self, on: bool):
        self.show_overlay = bool(on)
        self.overlay_changed.emit()

    def _rebuild_lut(self):
        lut = np.zeros((256, 4), np.uint8)
        for c, o in self.overlay.items():
            if o["visible"]:
                lut[c, :3] = o["color"]
                lut[c, 3] = int(round(255 * o["opacity"]))
        self._lut = lut

    def overlay_rgba(self, lab2d: np.ndarray) -> np.ndarray:
        return self._lut[lab2d]

    def readout(self, z, y, x) -> dict:
        if not self.source:
            return {}
        z, y, x = (int(v) for v in (z, y, x))
        val = self.source.value(z, y, x)
        lab = int(self.editor.labels[z, y, x]) if self.editor is not None else None
        sp = self.spacing
        return {"voxel": (z, y, x), "mm": tuple(round(i * s / 1000.0, 4) for i, s in zip((z, y, x), sp)),
                "value": val, "label": lab, "label_name": CLASS_NAMES.get(lab, LABELS.get(lab, "")) if lab is not None else "",
                "unit": "grey value"}

    # ------------------------------------------------------------------ tools
    def set_tool(self, tool: str):
        if tool not in TOOLS:
            raise ValueError(tool)
        self.tool = tool
        self.tool_changed.emit()

    def set_brush(self, radius_um=None, three_d=None, label=None, protect=None):
        if radius_um is not None:
            self.brush_radius_um = max(0.1, float(radius_um))
        if three_d is not None:
            self.brush_3d = bool(three_d)
        if label is not None:
            if label not in EDIT_LABELS:
                raise ValueError(label)
            self.active_label = int(label)
        if protect is not None:
            self.protect_other_classes = bool(protect)
        self.tool_changed.emit()

    @property
    def can_edit(self) -> bool:
        return self.editor is not None

    def _paint_params(self, erase: bool):
        if erase:
            return 0, (self.active_label,) if self.protect_other_classes else None
        return self.active_label, (0, self.active_label) if self.protect_other_classes else None

    def _push(self, diff, text, axis=None, index=None, tool="edit"):
        if diff is None:
            return False
        if axis is not None and index is not None:
            ks = self.key_slices[axis]
            if index in ks:
                ks.remove(index)
            ks.append(index)
        self.history.push_diff(self.editor, diff, text, self._on_diff)
        self.edit_applied.emit(tool, dict(diff.class_delta))
        return True

    def _on_diff(self, diff):
        self.labels_changed.emit(diff.bbox)

    def paint_stroke(self, axis: int, index: int, points, erase: bool = False) -> bool:
        """``points`` are (row, col) voxel coordinates in the plane of ``axis``."""
        if not self.can_edit or not points:
            return False
        value, only = self._paint_params(erase)
        verb = "Erase" if erase else f"Paint {CLASS_NAMES[self.active_label]}"
        if self.brush_3d:
            a, b = LabelEditor.plane_axes(axis)
            centers = []
            for r, c in points:
                p = [0.0, 0.0, 0.0]
                p[axis], p[a], p[b] = index, r, c
                centers.append(tuple(p))
            d = self.editor.stroke_3d(centers, self.brush_radius_um, value, only)
            return self._push(d, f"{verb} (3D sphere, r={self.brush_radius_um:g} µm)", axis, index,
                              "eraser3d" if erase else "brush3d")
        d = self.editor.stroke_2d(axis, index, points, self.brush_radius_um, value, only)
        return self._push(d, f"{verb} (r={self.brush_radius_um:g} µm)", axis, index, "eraser2d" if erase else "brush2d")

    def region_grow(self, z, y, x, axis: int | None = None) -> bool:
        if not self.can_edit:
            return False
        r = self.grow_radius_vox
        lo = [max(0, v - r) for v in (z, y, x)]
        hi = [min(n, v + r + 1) for v, n in zip((z, y, x), self.shape)]
        if axis is not None and not self.grow_3d:
            lo[axis], hi[axis] = (z, y, x)[axis], (z, y, x)[axis] + 1
        block = self.source.block(lo, hi)
        _, only = self._paint_params(False)
        d = self.editor.region_grow(block, lo, (z, y, x), self.grow_tolerance, self.active_label, only,
                                    axis=None if self.grow_3d else axis)
        ax = axis if (axis is not None and not self.grow_3d) else None
        return self._push(d, f"Region grow {CLASS_NAMES[self.active_label]} (tolerance {self.grow_tolerance:.4g})",
                          ax, (z, y, x)[axis] if ax is not None else None, "region_grow")

    def fill_holes(self, axis: int, index: int) -> bool:
        if not self.can_edit:
            return False
        d = self.editor.fill_holes(axis, index, self.active_label)
        return self._push(d, f"Fill holes {CLASS_NAMES[self.active_label]}", axis, index, tool="fill_holes")

    def interpolate(self, axis: int) -> bool:
        """Interpolate the active class between the two most recently edited slices on ``axis``."""
        if not self.can_edit:
            return False
        ks = self.key_slices[axis]
        if len(ks) < 2:
            raise ValueError("Edit two slices on this orientation first (key slices)")
        i0, i1 = ks[-2], ks[-1]
        d = self.editor.interpolate(axis, i0, i1, self.active_label)
        return self._push(d, f"Interpolate {CLASS_NAMES[self.active_label]} slices {min(i0, i1)}-{max(i0, i1)}",
                          tool="interpolate")
