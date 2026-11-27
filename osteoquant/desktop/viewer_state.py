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

TOOLS = ("navigate", "brush", "erase", "grow", "fill", "measure")
EDIT_TOOLS = ("brush", "erase", "grow", "fill")
EDIT_LABELS = (1, 2, 3, 255)
CLASS_NAMES = {0: "Background", 1: "New bone", 2: "Residual graft", 3: "Host bone", 255: "Uncertain"}

# Label palettes. "Okabe-Ito" is the package default (osteoquant.LABEL_COLORS). The colour-blind-safe
# high-contrast preset uses blue / orange / white / black so that no pair depends on red-green hue
# (host bone no longer turns grey under deuteranopia/protanopia, review UX-29).
PALETTES = {
    "Okabe-Ito (default)": {c: tuple(LABEL_COLORS[c][:3]) for c in EDIT_LABELS},
    "Colour-blind safe, high contrast (blue / orange / white / black)": {
        1: (230, 159, 0), 2: (0, 114, 178), 3: (245, 245, 245), 255: (0, 0, 0)},
}
ROI_COLOR = (240, 228, 66)          # Okabe-Ito yellow: ROI outline in slice views and 3D wireframe
CHANGE_COLOR = (255, 0, 255)        # changed voxels when comparing with the parent version


def window_presets(stats: dict) -> dict[str, tuple[float, float]]:
    """Window presets for uncalibrated grey values, defined on the scan's own histogram.

    Bone: median to maximum (mineralised tissue); Graft: upper part of the mineral range, for
    graft particles that are denser than bone; Soft tissue: low intensities up to just above the
    median. The same rules give the same window for every scan of a study."""
    p1, p50, p99, mn, mx = stats["p1"], stats["p50"], stats["p99"], stats["min"], stats["max"]
    return {"Auto (1-99.5 %)": (p1, p99), "Bone": (p50, mx), "Graft (dense mineral)": (p50 + 0.4 * (p99 - p50), mx),
            "Soft tissue": (p1, p50 + 0.25 * (p99 - p50)), "Full range": (mn, mx)}


def outline_mask(lab2d: np.ndarray) -> np.ndarray:
    """True where a pixel differs from one of its 4-neighbours (label boundaries)."""
    e = np.zeros(lab2d.shape, bool)
    d0 = lab2d[1:, :] != lab2d[:-1, :]
    d1 = lab2d[:, 1:] != lab2d[:, :-1]
    e[1:, :] |= d0
    e[:-1, :] |= d0
    e[:, 1:] |= d1
    e[:, :-1] |= d1
    return e


def mask_edges(m: np.ndarray) -> np.ndarray:
    """Voxel-edge segments of a 2D boolean mask's boundary, as (row0, col0, row1, col1) in continuous
    voxel coordinates (voxel i spans [i-0.5, i+0.5]). Used to draw the ROI outline."""
    m = np.pad(np.asarray(m, bool), 1)
    out = []
    v = np.argwhere(m[:, 1:] != m[:, :-1])          # boundary between col c and c+1 (padded coords)
    if len(v):
        r, c = v[:, 0] - 1, v[:, 1] - 1
        out.append(np.stack([r - 0.5, c + 0.5, r + 0.5, c + 0.5], 1))
    h = np.argwhere(m[1:, :] != m[:-1, :])
    if len(h):
        r, c = h[:, 0] - 1, h[:, 1] - 1
        out.append(np.stack([r + 0.5, c - 0.5, r + 0.5, c + 0.5], 1))
    return np.concatenate(out) if out else np.zeros((0, 4))


def format_length(um: float) -> str:
    return f"{um / 1000:.3f} mm" if um >= 1000 else f"{um:.1f} µm"


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
        self.read_only_reason = ""          # non-empty: the signed-in role cannot edit (tools disabled)
        self.roi: np.ndarray | None = None  # analysis ROI mask (bool) of the open segmentation version
        self.show_roi = True
        self.compare_mask: np.ndarray | None = None    # voxels changed vs the parent version
        self.compare_info = ""
        self.outline_mode = False
        self.palette = next(iter(PALETTES))
        self.measurements: list[dict] = []
        self.view_preserved = False         # True while a reload of the same scan keeps cursor/window/zoom
        self._lut = None
        self._rebuild_lut()

    # ------------------------------------------------------------------ scan
    def load(self, source: VolumeSource, labels: np.ndarray | None = None, scan: dict | None = None,
             segmentation: dict | None = None, roi: np.ndarray | None = None, keep_view: bool = False):
        same = bool(keep_view and self.source is not None and self.scan and scan
                    and self.scan.get("id") == scan.get("id") and tuple(self.source.shape) == tuple(source.shape))
        self.source = source
        self.scan, self.segmentation = scan, segmentation
        self.editor = LabelEditor(labels, source.spacing) if labels is not None else None
        self.roi = roi if (roi is not None and tuple(roi.shape) == tuple(source.shape)) else None
        self.compare_mask = None
        self.compare_info = ""
        self.history.clear()
        self.history.setClean()
        self.key_slices = {0: [], 1: [], 2: []}
        st = source.stats()
        if not same:
            self.cursor = [n // 2 for n in source.shape]
            self.window = (st["p1"], st["p99"])
            self.measurements = []
        if self.brush_radius_um <= 0:
            self.brush_radius_um = 3 * min(source.spacing)
        self.grow_tolerance = max(1e-3, 0.08 * (st["p99"] - st["p1"]))
        self.view_preserved = same
        try:
            self.scan_changed.emit()
            self.window_changed.emit(*self.window)
            self.cursor_changed.emit(*self.cursor)
        finally:
            self.view_preserved = False

    def unload(self):
        self.source = None
        self.editor = None
        self.roi = None
        self.compare_mask = None
        self.measurements = []
        self.scan = self.segmentation = None
        self.history.clear()
        self.scan_changed.emit()

    # ------------------------------------------------------------------ ROI / comparison / measurements
    def set_show_roi(self, on: bool):
        self.show_roi = bool(on)
        self.overlay_changed.emit()

    def roi_slice(self, axis, index) -> np.ndarray | None:
        if self.roi is None:
            return None
        sl = [slice(None)] * 3
        sl[axis] = int(np.clip(index, 0, self.shape[axis] - 1))
        return self.roi[tuple(sl)]

    def set_compare(self, parent_labels: np.ndarray | None, info: str = ""):
        """Highlight voxels that differ from ``parent_labels`` (None switches the comparison off)."""
        if parent_labels is None or self.editor is None or parent_labels.shape != self.editor.labels.shape:
            self.compare_mask, self.compare_info = None, ""
        else:
            self.compare_mask = parent_labels != self.editor.labels
            self.compare_info = info
        self.overlay_changed.emit()

    def compare_slice(self, axis, index) -> np.ndarray | None:
        if self.compare_mask is None:
            return None
        sl = [slice(None)] * 3
        sl[axis] = int(np.clip(index, 0, self.shape[axis] - 1))
        return self.compare_mask[tuple(sl)]

    def add_measurement(self, axis, index, p0, p1) -> dict:
        a, b = LabelEditor.plane_axes(axis)
        sp = self.spacing
        length = float(np.hypot((p1[0] - p0[0]) * sp[a], (p1[1] - p0[1]) * sp[b]))
        m = {"axis": int(axis), "index": int(index), "p0": tuple(map(float, p0)), "p1": tuple(map(float, p1)),
             "length_um": length}
        self.measurements.append(m)
        self.message.emit(f"Distance {format_length(length)}")
        self.overlay_changed.emit()
        return m

    def clear_measurements(self):
        self.measurements = []
        self.overlay_changed.emit()

    def set_palette(self, name: str):
        if name not in PALETTES:
            raise ValueError(name)
        self.palette = name
        for c, rgb in PALETTES[name].items():
            self.overlay[c]["color"] = tuple(rgb)
        self._rebuild_lut()
        self.overlay_changed.emit()

    def set_outline_mode(self, on: bool):
        self.outline_mode = bool(on)
        self.overlay_changed.emit()

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
        rgba = self._lut[lab2d]
        if self.outline_mode:
            rgba = rgba.copy()
            edge = outline_mask(lab2d)
            rgba[..., 3] = np.where(edge & (lab2d != 0), 255, 0).astype(np.uint8) * (rgba[..., 3] > 0)
        return rgba

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
        if tool in EDIT_TOOLS and self.read_only_reason:
            self.message.emit(self.read_only_reason)
            tool = "navigate"
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
        return self.editor is not None and not self.read_only_reason

    def set_read_only(self, reason: str):
        self.read_only_reason = reason or ""
        if self.read_only_reason and self.tool in EDIT_TOOLS:
            self.tool = "navigate"
        self.tool_changed.emit()

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
