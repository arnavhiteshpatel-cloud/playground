"""Orthogonal slice view: image + label overlay painted with QPainter from NumPy slices.

Slices are fetched lazily from the ViewerState's source; voxels are drawn with nearest-
neighbour scaling and physical aspect ratio. Interaction:

  left button      navigate: move crosshair | brush/eraser: paint stroke | grow/fill: apply at voxel
  right drag       window (horizontal) / level (vertical)
  middle drag      pan  (also Shift + left drag)
  wheel            change slice; Ctrl + wheel zooms about the pointer
  Up/Down, PgUp/PgDn  change slice;  F  fit to window
"""
from __future__ import annotations

import math

import numpy as np
from PySide6.QtCore import QPointF, QRectF, Qt, Signal
from PySide6.QtGui import QColor, QFont, QImage, QPainter, QPen
from PySide6.QtWidgets import QSizePolicy, QWidget

from . import theme
from .editing import LabelEditor
from .viewer_state import ViewerState
from .volume_source import AXIS_NAMES

AXIS_COLORS = {0: QColor(214, 94, 84), 1: QColor(98, 170, 110), 2: QColor(92, 145, 210)}
AXIS_LETTERS = {0: "z", 1: "y", 2: "x"}


def nice_length(target: float) -> float:
    if target <= 0:
        return 1.0
    e = 10 ** math.floor(math.log10(target))
    for m in (1, 2, 5, 10):
        if m * e >= target:
            return m * e
    return 10 * e


def format_length_um(um: float) -> str:
    return f"{um / 1000:g} mm" if um >= 1000 else f"{um:g} µm"


class SliceView(QWidget):
    maximize_requested = Signal(int)

    def __init__(self, state: ViewerState, axis: int, parent=None):
        super().__init__(parent)
        self.state, self.axis = state, axis
        self.a, self.b = LabelEditor.plane_axes(axis)    # plane rows, plane cols (array axes)
        self.scale = 1.0          # screen px per µm
        self.offset = QPointF(0, 0)
        self._fitted = False
        self._img = self._ovl = None
        self._img_buf = self._ovl_buf = None
        self._drag = None
        self._stroke: list[tuple[float, float]] = []
        self._hover: tuple[float, float] | None = None
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setMinimumSize(160, 140)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setAttribute(Qt.WA_OpaquePaintEvent)
        state.scan_changed.connect(self._on_scan)
        state.cursor_changed.connect(self._on_cursor)
        state.window_changed.connect(lambda *_: self._refresh_image())
        state.labels_changed.connect(self._on_labels)
        state.overlay_changed.connect(self._refresh_overlay)
        state.tool_changed.connect(self.update)
        self._index = -1

    # ------------------------------------------------------------------ geometry
    @property
    def index(self) -> int:
        return self.state.cursor[self.axis]

    def plane_size_um(self):
        sh, sp = self.state.shape, self.state.spacing
        return sh[self.b] * sp[self.b], sh[self.a] * sp[self.a]   # width, height in µm

    def fit(self):
        w_um, h_um = self.plane_size_um()
        if w_um <= 0 or h_um <= 0:
            return
        self.scale = 0.94 * min(self.width() / w_um, self.height() / h_um)
        self.offset = QPointF((self.width() - w_um * self.scale) / 2, (self.height() - h_um * self.scale) / 2)
        self._fitted = True
        self.update()

    def image_rect(self) -> QRectF:
        w_um, h_um = self.plane_size_um()
        return QRectF(self.offset.x(), self.offset.y(), w_um * self.scale, h_um * self.scale)

    def to_plane(self, pos) -> tuple[float, float]:
        """Screen position -> (row, col) continuous voxel index (voxel i spans [i-0.5, i+0.5])."""
        sp = self.state.spacing
        row = (pos.y() - self.offset.y()) / (sp[self.a] * self.scale) - 0.5
        col = (pos.x() - self.offset.x()) / (sp[self.b] * self.scale) - 0.5
        return row, col

    def to_screen(self, row, col) -> QPointF:
        sp = self.state.spacing
        return QPointF(self.offset.x() + (col + 0.5) * sp[self.b] * self.scale,
                       self.offset.y() + (row + 0.5) * sp[self.a] * self.scale)

    def voxel_at(self, pos):
        row, col = self.to_plane(pos)
        r, c = int(round(row)), int(round(col))
        sh = self.state.shape
        if not (0 <= r < sh[self.a] and 0 <= c < sh[self.b]):
            return None
        v = [0, 0, 0]
        v[self.axis], v[self.a], v[self.b] = self.index, r, c
        return tuple(v)

    # ------------------------------------------------------------------ data -> images
    def _on_scan(self):
        self._fitted = False
        self._index = -1
        self._refresh_image()

    def _on_cursor(self, *_):
        if self.index != self._index:
            self._refresh_image()
        else:
            self.update()

    def _on_labels(self, bbox):
        if bbox is None or bbox[self.axis][0] <= self.index < bbox[self.axis][1]:
            self._refresh_overlay()

    def _refresh_image(self):
        st = self.state
        if not st.loaded:
            self._img = None
            self.update()
            return
        self._index = self.index
        s = st.image_slice(self.axis, self.index).astype(np.float32)
        lo, hi = st.window
        g = np.clip((s - lo) * (255.0 / max(hi - lo, 1e-12)), 0, 255).astype(np.uint8)
        self._img_buf = np.ascontiguousarray(g)
        h, w = g.shape
        self._img = QImage(self._img_buf.data, w, h, w, QImage.Format_Grayscale8)
        self._refresh_overlay()

    def _refresh_overlay(self):
        st = self.state
        lab = st.label_slice(self.axis, self.index) if st.loaded else None
        if lab is None:
            self._ovl = None
        else:
            rgba = np.ascontiguousarray(st.overlay_rgba(lab))
            self._ovl_buf = rgba
            h, w = lab.shape
            self._ovl = QImage(rgba.data, w, h, 4 * w, QImage.Format_RGBA8888)
        self.update()

    # ------------------------------------------------------------------ painting
    def resizeEvent(self, e):
        if not self._fitted or e.oldSize().width() <= 0:
            self.fit()
        else:
            # keep the image centred relative to the previous size
            dx = (e.size().width() - e.oldSize().width()) / 2
            dy = (e.size().height() - e.oldSize().height()) / 2
            self.offset += QPointF(dx, dy)
        super().resizeEvent(e)

    def paintEvent(self, _):
        p = QPainter(self)
        p.fillRect(self.rect(), theme.qcolor("viewport_bg"))
        st = self.state
        col = AXIS_COLORS[self.axis]
        if self._img is None or not st.loaded:
            p.setPen(theme.qcolor("viewport_muted"))
            p.drawText(self.rect(), Qt.AlignCenter, f"{AXIS_NAMES[self.axis]}\nNo scan loaded")
            self._frame(p, col)
            p.end()
            return
        if not self._fitted:
            self.fit()
        r = self.image_rect()
        p.setRenderHint(QPainter.SmoothPixmapTransform, False)
        p.drawImage(r, self._img)
        if self._ovl is not None and st.show_overlay:
            p.drawImage(r, self._ovl)
        p.setRenderHint(QPainter.Antialiasing, True)
        self._draw_crosshair(p)
        self._draw_stroke(p)
        self._draw_brush_cursor(p)
        p.setRenderHint(QPainter.Antialiasing, False)
        self._draw_text(p)
        self._draw_scale_bar(p)
        self._frame(p, col)
        p.end()

    def _frame(self, p, col):
        p.setPen(QPen(col, 2))
        p.drawLine(0, 1, self.width(), 1)

    def _draw_crosshair(self, p):
        st = self.state
        c = st.cursor
        pt = self.to_screen(c[self.a], c[self.b])
        r = self.image_rect()
        gap = 6
        p.setPen(QPen(AXIS_COLORS[self.b], 1, Qt.SolidLine))      # vertical line = position on col axis
        p.drawLine(QPointF(pt.x(), r.top()), QPointF(pt.x(), pt.y() - gap))
        p.drawLine(QPointF(pt.x(), pt.y() + gap), QPointF(pt.x(), r.bottom()))
        p.setPen(QPen(AXIS_COLORS[self.a], 1, Qt.SolidLine))      # horizontal line = position on row axis
        p.drawLine(QPointF(r.left(), pt.y()), QPointF(pt.x() - gap, pt.y()))
        p.drawLine(QPointF(pt.x() + gap, pt.y()), QPointF(r.right(), pt.y()))

    def _brush_radii_px(self):
        sp = self.state.spacing
        rad = self.state.brush_radius_um
        return rad * self.scale, rad * self.scale, sp

    def _draw_brush_cursor(self, p):
        st = self.state
        if self._hover is None or st.tool not in ("brush", "erase") or not st.can_edit:
            return
        rpx, _, _ = self._brush_radii_px()
        pt = self.to_screen(*self._hover)
        p.setPen(QPen(QColor(255, 255, 255, 200), 1, Qt.DashLine if st.tool == "erase" else Qt.SolidLine))
        p.setBrush(Qt.NoBrush)
        p.drawEllipse(pt, rpx, rpx)

    def _draw_stroke(self, p):
        if not self._stroke:
            return
        st = self.state
        rpx, _, _ = self._brush_radii_px()
        if st.tool == "erase":
            c = QColor(0, 0, 0, 110)
        else:
            rgb = st.overlay[st.active_label]["color"]
            c = QColor(rgb[0], rgb[1], rgb[2], 150)
        pen = QPen(c, 2 * rpx, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        p.setPen(pen)
        pts = [self.to_screen(r, cc) for r, cc in self._stroke]
        if len(pts) == 1:
            p.setBrush(c)
            p.setPen(Qt.NoPen)
            p.drawEllipse(pts[0], rpx, rpx)
        else:
            for i in range(1, len(pts)):
                p.drawLine(pts[i - 1], pts[i])

    def _draw_text(self, p):
        st = self.state
        f = QFont(self.font())
        f.setPointSizeF(8.5)
        p.setFont(f)
        shade = QColor(theme.tok("viewport_bg"))
        shade.setAlpha(170)
        p.fillRect(QRectF(4, 5, 236, 34), shade)
        p.fillRect(QRectF(4, self.height() - 24, 150, 18), shade)
        p.setPen(AXIS_COLORS[self.axis])
        p.drawText(QRectF(8, 6, 200, 16), Qt.AlignLeft | Qt.AlignVCenter, AXIS_NAMES[self.axis].upper())
        p.setPen(theme.qcolor("viewport_text"))
        n = st.shape[self.axis]
        p.drawText(QRectF(8, 22, 260, 16), Qt.AlignLeft | Qt.AlignVCenter,
                   f"{AXIS_LETTERS[self.axis]} {self.index + 1} / {n}   ·   "
                   f"{self.index * st.spacing[self.axis] / 1000:.3f} mm")
        p.setPen(theme.qcolor("viewport_muted"))
        lo, hi = st.window
        p.drawText(QRectF(8, self.height() - 22, 300, 16), Qt.AlignLeft | Qt.AlignVCenter,
                   f"W {hi - lo:.4g}   L {(hi + lo) / 2:.4g}")
        zoom = self.scale * st.spacing[self.b]
        p.drawText(QRectF(self.width() - 128, 6, 120, 16), Qt.AlignRight | Qt.AlignVCenter, f"{zoom * 100:.0f} %")

    def _draw_scale_bar(self, p):
        if self.scale <= 0:
            return
        target_px = max(60.0, self.width() * 0.18)
        um = nice_length(target_px / self.scale)
        px = um * self.scale
        x1 = self.width() - 14
        x0 = x1 - px
        y = self.height() - 16
        shade = QColor(theme.tok("viewport_bg"))
        shade.setAlpha(170)
        p.fillRect(QRectF(x0 - 8, y - 22, px + 16, 28), shade)
        pen = QPen(theme.qcolor("viewport_text"), 2)
        p.setPen(pen)
        p.drawLine(QPointF(x0, y), QPointF(x1, y))
        p.drawLine(QPointF(x0, y - 4), QPointF(x0, y + 1))
        p.drawLine(QPointF(x1, y - 4), QPointF(x1, y + 1))
        p.drawText(QRectF(x0 - 40, y - 20, px + 40, 14), Qt.AlignRight | Qt.AlignVCenter, format_length_um(um))

    # ------------------------------------------------------------------ interaction
    def _set_crosshair(self, pos):
        v = self.voxel_at(pos)
        if v is not None:
            self.state.set_cursor(*v)

    def mousePressEvent(self, e):
        st = self.state
        if not st.loaded:
            return
        self.setFocus()
        btn = e.button()
        if btn == Qt.MiddleButton or (btn == Qt.LeftButton and e.modifiers() & Qt.ShiftModifier):
            self._drag = ("pan", e.position(), QPointF(self.offset))
        elif btn == Qt.RightButton:
            self._drag = ("wl", e.position(), st.window)
        elif btn == Qt.LeftButton:
            tool = st.tool if st.can_edit else "navigate"
            if tool in ("brush", "erase"):
                self._drag = ("paint", None, None)
                self._stroke = [self.to_plane(e.position())]
                self.update()
            elif tool == "grow":
                v = self.voxel_at(e.position())
                if v is not None:
                    st.region_grow(*v, axis=self.axis)
            elif tool == "fill":
                st.fill_holes(self.axis, self.index)
            else:
                self._drag = ("nav", None, None)
                self._set_crosshair(e.position())

    def mouseMoveEvent(self, e):
        st = self.state
        if not st.loaded:
            return
        pos = e.position()
        self._hover = self.to_plane(pos)
        v = self.voxel_at(pos)
        st.hover_changed.emit(v)
        if self._drag:
            kind, p0, v0 = self._drag
            if kind == "pan":
                self.offset = v0 + (pos - p0)
            elif kind == "wl":
                lo, hi = v0
                w, lvl = hi - lo, (hi + lo) / 2
                rng = max(1e-6, st.source.stats()["max"] - st.source.stats()["min"])
                w = max(rng * 1e-4, w * math.exp((pos.x() - p0.x()) / 200.0))
                lvl = lvl - (pos.y() - p0.y()) * rng / 600.0
                st.set_window(lvl - w / 2, lvl + w / 2)
            elif kind == "paint":
                self._stroke.append(self._hover)
            elif kind == "nav":
                self._set_crosshair(pos)
        self.update()

    def mouseReleaseEvent(self, e):
        if self._drag and self._drag[0] == "paint" and self._stroke:
            pts = self._stroke
            self._stroke = []
            self.state.paint_stroke(self.axis, self.index, pts, erase=self.state.tool == "erase")
        self._drag = None
        self.update()

    def mouseDoubleClickEvent(self, e):
        if e.button() == Qt.LeftButton and self.state.tool == "navigate":
            self.maximize_requested.emit(self.axis)

    def leaveEvent(self, e):
        self._hover = None
        self.state.hover_changed.emit(None)
        self.update()

    def wheelEvent(self, e):
        st = self.state
        if not st.loaded:
            return
        d = e.angleDelta().y()
        if e.modifiers() & Qt.ControlModifier:
            pos = e.position()
            f = 1.15 if d > 0 else 1 / 1.15
            self.offset = pos + (self.offset - pos) * f
            self.scale *= f
            self.update()
        elif d:
            st.set_index(self.axis, self.index + (1 if d > 0 else -1))

    def keyPressEvent(self, e):
        st = self.state
        k = e.key()
        if k in (Qt.Key_Up, Qt.Key_Right):
            st.set_index(self.axis, self.index + 1)
        elif k in (Qt.Key_Down, Qt.Key_Left):
            st.set_index(self.axis, self.index - 1)
        elif k == Qt.Key_PageUp:
            st.set_index(self.axis, self.index + 10)
        elif k == Qt.Key_PageDown:
            st.set_index(self.axis, self.index - 10)
        elif k == Qt.Key_F:
            self.fit()
        else:
            super().keyPressEvent(e)

    def render_image(self) -> QImage:
        return self.grab().toImage()
