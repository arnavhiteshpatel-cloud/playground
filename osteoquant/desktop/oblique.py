"""Oblique reslice through the crosshair, computed with ``vtkImageReslice`` on a strided copy of
the image (voxel budget) so arbitrary planes stay interactive for large scans."""
from __future__ import annotations

import os

import numpy as np
from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QImage, QPainter, QPen
from PySide6.QtWidgets import QFormLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSlider, QVBoxLayout, QWidget
from vtkmodules.util.numpy_support import vtk_to_numpy
from vtkmodules.vtkCommonMath import vtkMatrix4x4
from vtkmodules.vtkImagingCore import vtkImageReslice

from . import theme
from .slice_view import format_length_um, nice_length
from .view3d import to_vtk_image
from .viewer_state import ViewerState

OBLIQUE_VOXELS = int(os.environ.get("OQ_OBLIQUE_VOXELS", str(256 ** 3)))


def rotation(tilt_x_deg: float, tilt_y_deg: float) -> np.ndarray:
    a, b = np.radians(tilt_x_deg), np.radians(tilt_y_deg)
    rx = np.array([[1, 0, 0], [0, np.cos(a), -np.sin(a)], [0, np.sin(a), np.cos(a)]])
    ry = np.array([[np.cos(b), 0, np.sin(b)], [0, 1, 0], [-np.sin(b), 0, np.cos(b)]])
    return ry @ rx


def oblique_slice(vol_zyx: np.ndarray, spacing_zyx, center_zyx_um, tilt_x, tilt_y) -> tuple[np.ndarray, float]:
    """Resample the plane through ``center`` (µm) whose normal is the z axis rotated by the tilts.
    Returns (2D array, pixel size in µm)."""
    img = to_vtk_image(vol_zyx.astype(np.float32), spacing_zyx)
    R = rotation(tilt_x, tilt_y)
    c = [center_zyx_um[2], center_zyx_um[1], center_zyx_um[0]]
    m = vtkMatrix4x4()
    for i in range(3):
        for j in range(3):
            m.SetElement(i, j, float(R[i, j]))
        m.SetElement(i, 3, float(c[i]))
    rs = vtkImageReslice()
    rs.SetInputData(img)
    rs.SetResliceAxes(m)
    rs.SetOutputDimensionality(2)
    rs.SetInterpolationModeToLinear()
    px = float(min(spacing_zyx))
    rs.SetOutputSpacing(px, px, px)
    rs.AutoCropOutputOn()
    rs.SetBackgroundLevel(float(np.min(vol_zyx)))
    rs.Update()
    out = rs.GetOutput()
    nx, ny, _ = out.GetDimensions()
    arr = vtk_to_numpy(out.GetPointData().GetScalars()).reshape(ny, nx)
    return arr.copy(), px


class ObliqueView(QWidget):
    def __init__(self, state: ViewerState, parent=None):
        super().__init__(parent)
        self.state = state
        self._vol = None
        self._sp = None
        self._step = 1
        self._img = None
        self._buf = None
        self._px = 1.0
        lay = QVBoxLayout(self)
        lay.setContentsMargins(8, 6, 8, 8)
        f = QFormLayout()
        self.tx, self.ty = QSlider(Qt.Horizontal), QSlider(Qt.Horizontal)
        for s in (self.tx, self.ty):
            s.setRange(-90, 90)
            s.valueChanged.connect(self.update_slice)
        self.tx_lbl, self.ty_lbl = QLabel("0°"), QLabel("0°")
        r1, r2 = QHBoxLayout(), QHBoxLayout()
        r1.addWidget(self.tx, 1)
        r1.addWidget(self.tx_lbl)
        r2.addWidget(self.ty, 1)
        r2.addWidget(self.ty_lbl)
        f.addRow("Tilt about x", r1)
        f.addRow("Tilt about y", r2)
        lay.addLayout(f)
        rb = QPushButton("Reset to axial")
        rb.clicked.connect(lambda: (self.tx.setValue(0), self.ty.setValue(0)))
        lay.addWidget(rb)
        self.canvas = QWidget()
        self.canvas.setMinimumSize(200, 200)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas.paintEvent = self._paint
        lay.addWidget(self.canvas, 1)
        self.info = QLabel("")
        self.info.setProperty("role", "muted")
        lay.addWidget(self.info)
        state.scan_changed.connect(self._on_scan)
        state.cursor_changed.connect(lambda *_: self.update_slice())
        state.window_changed.connect(lambda *_: self.update_slice())

    def _on_scan(self):
        self._vol = None
        if self.state.loaded:
            self._vol, self._step = self.state.source.downsampled(OBLIQUE_VOXELS)
            self._sp = tuple(s * self._step for s in self.state.spacing)
        self.update_slice()

    def update_slice(self, *_):
        self.tx_lbl.setText(f"{self.tx.value()}°")
        self.ty_lbl.setText(f"{self.ty.value()}°")
        if self._vol is None or not self.isVisible():
            self._img = None
            self.canvas.update()
            return
        c = [i * s for i, s in zip(self.state.cursor, self.state.spacing)]
        arr, self._px = oblique_slice(self._vol, self._sp, c, self.tx.value(), self.ty.value())
        lo, hi = self.state.window
        g = np.clip((arr - lo) * (255.0 / max(hi - lo, 1e-12)), 0, 255).astype(np.uint8)
        g = np.ascontiguousarray(g[::-1])          # VTK row 0 is at the bottom
        self._buf = g
        self._img = QImage(g.data, g.shape[1], g.shape[0], g.shape[1], QImage.Format_Grayscale8)
        self.info.setText(f"Through crosshair · resampled at {self._px:g} µm"
                          + (f" (stride {self._step})" if self._step > 1 else ""))
        self.canvas.update()

    def showEvent(self, e):
        super().showEvent(e)
        self.update_slice()

    def _paint(self, _):
        p = QPainter(self.canvas)
        p.fillRect(self.canvas.rect(), theme.qcolor("viewport_bg"))
        if self._img is None:
            p.setPen(theme.qcolor("viewport_muted"))
            p.drawText(self.canvas.rect(), Qt.AlignCenter, "Oblique\nNo scan loaded")
            p.end()
            return
        w, h = self.canvas.width(), self.canvas.height()
        s = 0.95 * min(w / self._img.width(), h / self._img.height())
        tw, th = self._img.width() * s, self._img.height() * s
        r = QRectF((w - tw) / 2, (h - th) / 2, tw, th)
        p.drawImage(r, self._img)
        scale = s / self._px            # px per µm
        um = nice_length(max(50.0, w * 0.2) / scale)
        x1, y = w - 12, h - 14
        p.setPen(QPen(theme.qcolor("viewport_text"), 2))
        p.drawLine(int(x1 - um * scale), y, x1, y)
        p.drawText(QRectF(x1 - um * scale - 40, y - 18, um * scale + 40, 14), Qt.AlignRight, format_length_um(um))
        p.end()
