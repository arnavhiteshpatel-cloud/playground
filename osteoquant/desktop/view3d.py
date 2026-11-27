"""3D panel: surface rendering of label classes and volume rendering of a downsampled image.

Surfaces are extracted per class with ``vtkDiscreteFlyingEdges3D`` (smoothed with a windowed
sinc filter) from a strided copy of the labels, on a worker thread; actors are created on the
GUI thread. Volume rendering uses ``vtkSmartVolumeMapper`` on a strided image (voxel budget).

Two presentation backends share the same VTK scene:
  * interactive: ``QVTKRenderWindowInteractor`` (normal desktop sessions);
  * image: an off-screen ``vtkRenderWindow`` whose frames are shown in a plain QWidget, with
    mouse rotation/zoom. Used automatically on the ``offscreen``/``minimal`` Qt platforms
    (CI, self-test, screenshots) or when ``OQ_3D_BACKEND=image``.
"""
from __future__ import annotations

import os

import numpy as np
from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal
from PySide6.QtGui import QGuiApplication, QImage, QPainter
from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QSizePolicy, QToolButton, QVBoxLayout, QWidget

import vtkmodules.vtkInteractionStyle  # noqa: F401  (factory registration)
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingVolumeOpenGL2  # noqa: F401
from vtkmodules.util.numpy_support import numpy_to_vtk, vtk_to_numpy
from vtkmodules.vtkCommonDataModel import vtkImageData, vtkPiecewiseFunction
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals, vtkWindowedSincPolyDataFilter
from vtkmodules.vtkFiltersGeneral import vtkDiscreteFlyingEdges3D
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkRenderingCore import (vtkActor, vtkColorTransferFunction, vtkPolyDataMapper, vtkRenderer,
                                         vtkRenderWindow, vtkVolume, vtkVolumeProperty, vtkWindowToImageFilter)
from vtkmodules.vtkRenderingVolumeOpenGL2 import vtkSmartVolumeMapper

from . import theme
from .viewer_state import CLASS_NAMES, EDIT_LABELS, ROI_COLOR, ViewerState

SURFACE_VOXELS = int(os.environ.get("OQ_3D_SURFACE_VOXELS", str(200 ** 3)))
VOLUME_VOXELS = int(os.environ.get("OQ_3D_VOLUME_VOXELS", str(128 ** 3)))


def use_image_backend() -> bool:
    if os.environ.get("OQ_3D_BACKEND") == "image":
        return True
    if os.environ.get("OQ_3D_BACKEND") == "interactive":
        return False
    return QGuiApplication.platformName() in ("offscreen", "minimal", "vnc")


def to_vtk_image(arr: np.ndarray, spacing_mm, vtk_type=None) -> vtkImageData:
    """(z, y, x) C-ordered array -> vtkImageData with x fastest (no copy of axis order)."""
    a = np.ascontiguousarray(arr)
    img = vtkImageData()
    img.SetDimensions(a.shape[2], a.shape[1], a.shape[0])
    img.SetSpacing(spacing_mm[2], spacing_mm[1], spacing_mm[0])
    sc = numpy_to_vtk(a.ravel(), deep=True, array_type=vtk_type)
    sc.SetName("scalars")
    img.GetPointData().SetScalars(sc)
    return img


def extract_surfaces(labels: np.ndarray, spacing_um, classes=EDIT_LABELS, smooth_iter: int = 15) -> dict:
    """label -> vtkPolyData, from a strided copy of ``labels`` within SURFACE_VOXELS."""
    step = 1
    while np.prod([int(np.ceil(n / step)) for n in labels.shape]) > SURFACE_VOXELS:
        step += 1
    lab = np.ascontiguousarray(labels[::step, ::step, ::step])
    lab = np.pad(lab, 1)                         # close surfaces at the volume border
    sp_mm = [s * step / 1000.0 for s in spacing_um]
    img = to_vtk_image(lab, sp_mm)
    img.SetOrigin(-sp_mm[2], -sp_mm[1], -sp_mm[0])
    present = set(np.unique(lab).tolist())
    out = {}
    for c in classes:
        if c not in present:
            continue
        fe = vtkDiscreteFlyingEdges3D()
        fe.SetInputData(img)
        fe.SetValue(0, c)
        fe.ComputeScalarsOff()
        fe.Update()
        poly = fe.GetOutput()
        if poly.GetNumberOfPoints() == 0:
            continue
        if smooth_iter:
            sm = vtkWindowedSincPolyDataFilter()
            sm.SetInputData(poly)
            sm.SetNumberOfIterations(smooth_iter)
            sm.SetPassBand(0.08)
            sm.BoundarySmoothingOff()
            sm.NonManifoldSmoothingOn()
            sm.NormalizeCoordinatesOn()
            sm.Update()
            poly = sm.GetOutput()
        nm = vtkPolyDataNormals()
        nm.SetInputData(poly)
        nm.SetFeatureAngle(60)
        nm.Update()
        out[c] = nm.GetOutput()
    return {"surfaces": out, "step": step}


def roi_surface(roi: np.ndarray, spacing_um, max_voxels: int = 40 ** 3):
    """Surface of the ROI mask (strided to ``max_voxels``) for the 3D wireframe, or None."""
    step = 1
    while np.prod([int(np.ceil(n / step)) for n in roi.shape]) > max_voxels:
        step += 1
    m = np.pad(np.ascontiguousarray(roi[::step, ::step, ::step]).astype(np.uint8), 1)
    if not m.any():
        return None
    sp_mm = [s * step / 1000.0 for s in spacing_um]
    img = to_vtk_image(m, sp_mm)
    img.SetOrigin(-sp_mm[2], -sp_mm[1], -sp_mm[0])
    fe = vtkDiscreteFlyingEdges3D()
    fe.SetInputData(img)
    fe.SetValue(0, 1)
    fe.ComputeScalarsOff()
    fe.Update()
    poly = fe.GetOutput()
    return poly if poly.GetNumberOfPoints() else None


class _SurfaceSignals(QObject):
    done = Signal(object, int)
    failed = Signal(str, int)


class _SurfaceJob(QRunnable):
    def __init__(self, labels, spacing, token):
        super().__init__()
        self.labels, self.spacing, self.token = labels, spacing, token
        self.sig = _SurfaceSignals()

    def run(self):
        try:
            self.sig.done.emit(extract_surfaces(self.labels, self.spacing), self.token)
        except Exception as e:  # noqa: BLE001
            self.sig.failed.emit(f"{type(e).__name__}: {e}", self.token)


class _ImageCanvas(QWidget):
    """Shows frames of an off-screen render window; drag rotates, wheel zooms."""

    def __init__(self, owner: "View3D"):
        super().__init__(owner)
        self.owner = owner
        self.frame: QImage | None = None
        self._last = None
        self.setMinimumSize(160, 140)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def paintEvent(self, _):
        p = QPainter(self)
        p.fillRect(self.rect(), theme.qcolor("viewport_bg"))
        if self.frame is not None:
            p.drawImage(0, 0, self.frame)
        p.end()

    def resizeEvent(self, e):
        self.owner.render()
        super().resizeEvent(e)

    def mousePressEvent(self, e):
        self._last = e.position()

    def mouseMoveEvent(self, e):
        if self._last is None:
            return
        d = e.position() - self._last
        self._last = e.position()
        cam = self.owner.renderer.GetActiveCamera()
        cam.Azimuth(-d.x() * 0.5)
        cam.Elevation(d.y() * 0.5)
        cam.OrthogonalizeViewUp()
        self.owner.render()

    def mouseReleaseEvent(self, e):
        self._last = None

    def wheelEvent(self, e):
        self.owner.renderer.GetActiveCamera().Dolly(1.1 if e.angleDelta().y() > 0 else 1 / 1.1)
        self.owner.renderer.ResetCameraClippingRange()
        self.owner.render()


class View3D(QWidget):
    status = Signal(str)

    def __init__(self, state: ViewerState, parent=None):
        super().__init__(parent)
        self.state = state
        self.renderer = vtkRenderer()
        self._apply_background()
        self.image_backend = use_image_backend()
        self.surface_actors: dict[int, vtkActor] = {}
        self.volume: vtkVolume | None = None
        self.outline: vtkActor | None = None
        self.roi_actor: vtkActor | None = None
        self._token = 0
        self._stale = False
        self.pool = QThreadPool(self)
        self.pool.setMaxThreadCount(1)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        bar = QWidget(self)
        bar.setObjectName("view3dBar")
        bar.setAutoFillBackground(True)
        bar.setStyleSheet(f"#view3dBar {{ background: {theme.tok('viewport_bg')}; }}"
                          f"#view3dBar QLabel {{ color: {theme.tok('viewport_muted')}; }}")
        hb = QHBoxLayout(bar)
        hb.setContentsMargins(8, 4, 6, 4)
        hb.setSpacing(4)
        title = QLabel("3D")
        title.setStyleSheet("font-weight: 600; color: #d8dde3;")
        self.mode = QComboBox()
        self.mode.addItems(["Surfaces", "Volume", "Surfaces + volume"])
        self.mode.setToolTip("Surface rendering of label classes and/or volume rendering of the image")
        self.mode.currentIndexChanged.connect(self._apply_mode)
        self.btn_update = QToolButton()
        self.btn_update.setText("Update")
        self.btn_update.setToolTip("Re-extract label surfaces after editing")
        self.btn_update.clicked.connect(lambda: self.rebuild_surfaces())
        self.btn_reset = QToolButton()
        self.btn_reset.setText("Reset")
        self.btn_reset.setToolTip("Reset the camera")
        self.btn_reset.clicked.connect(self.reset_camera)
        for b in (self.btn_update, self.btn_reset):
            b.setStyleSheet("QToolButton { color: #d8dde3; } QToolButton:hover { background: #2a2f35; }")
        self.info = QLabel("")
        hb.addWidget(title)
        hb.addSpacing(6)
        hb.addWidget(self.mode)
        hb.addWidget(self.btn_update)
        hb.addWidget(self.btn_reset)
        hb.addStretch(1)
        hb.addWidget(self.info)
        lay.addWidget(bar)

        if self.image_backend:
            self.rw = vtkRenderWindow()
            self.rw.SetOffScreenRendering(1)
            self.rw.AddRenderer(self.renderer)
            self.canvas = _ImageCanvas(self)
            lay.addWidget(self.canvas, 1)
            self.vtk_widget = None
        else:
            import vtkmodules.qt
            vtkmodules.qt.PyQtImpl = "PySide6"          # do not probe for other Qt bindings
            from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
            from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
            self.vtk_widget = QVTKRenderWindowInteractor(self)
            lay.addWidget(self.vtk_widget, 1)
            self.rw = self.vtk_widget.GetRenderWindow()
            self.rw.AddRenderer(self.renderer)
            self.vtk_widget.GetRenderWindow().GetInteractor().SetInteractorStyle(vtkInteractorStyleTrackballCamera())
            self.vtk_widget.Initialize()
            self.canvas = self.vtk_widget

        state.scan_changed.connect(self._on_scan)
        state.labels_changed.connect(self._on_labels_changed)
        state.overlay_changed.connect(self._apply_overlay)
        state.window_changed.connect(lambda *_: self._update_volume_tf())

    # ------------------------------------------------------------------ scene
    def _apply_background(self):
        c = theme.qcolor("viewport_bg")
        self.renderer.SetBackground(c.redF(), c.greenF(), c.blueF())
        self.renderer.SetBackground2(0.16, 0.18, 0.21)
        self.renderer.GradientBackgroundOn()

    def clear(self):
        for a in self.surface_actors.values():
            self.renderer.RemoveActor(a)
        self.surface_actors.clear()
        if self.volume is not None:
            self.renderer.RemoveVolume(self.volume)
            self.volume = None
        if self.outline is not None:
            self.renderer.RemoveActor(self.outline)
            self.outline = None
        if self.roi_actor is not None:
            self.renderer.RemoveActor(self.roi_actor)
            self.roi_actor = None

    def _build_roi(self):
        st = self.state
        if st.roi is None:
            return
        try:
            poly = roi_surface(st.roi, st.spacing)
        except Exception:  # noqa: BLE001 - the ROI wireframe is an aid; never block the scan
            poly = None
        if poly is None:
            return
        m = vtkPolyDataMapper()
        m.SetInputData(poly)
        m.ScalarVisibilityOff()
        a = vtkActor()
        a.SetMapper(m)
        pr = a.GetProperty()
        pr.SetRepresentationToWireframe()
        pr.SetColor(*(c / 255 for c in ROI_COLOR))
        pr.SetOpacity(0.3)
        pr.LightingOff()
        a.SetVisibility(bool(st.show_roi))
        self.roi_actor = a
        self.renderer.AddActor(a)

    def _on_scan(self):
        cam = None
        if self.state.view_preserved:          # same scan reloaded (after a save): keep the camera
            c = self.renderer.GetActiveCamera()
            cam = (c.GetPosition(), c.GetFocalPoint(), c.GetViewUp(), c.GetParallelScale())
        self.clear()
        st = self.state
        if not st.loaded:
            self.info.setText("")
            self.render()
            return
        sh, sp = st.shape, st.spacing
        img = vtkImageData()
        img.SetDimensions(sh[2], sh[1], sh[0])
        img.SetSpacing(sp[2] / 1000, sp[1] / 1000, sp[0] / 1000)
        of = vtkOutlineFilter()
        of.SetInputData(img)
        of.Update()
        m = vtkPolyDataMapper()
        m.SetInputData(of.GetOutput())
        self.outline = vtkActor()
        self.outline.SetMapper(m)
        self.outline.GetProperty().SetColor(0.55, 0.6, 0.66)
        self.renderer.AddActor(self.outline)
        self._build_roi()
        if cam is None:
            self.reset_camera()
        else:
            c = self.renderer.GetActiveCamera()
            c.SetPosition(*cam[0])
            c.SetFocalPoint(*cam[1])
            c.SetViewUp(*cam[2])
            self.renderer.ResetCameraClippingRange()
        self._apply_mode()
        if st.editor is not None:
            self.rebuild_surfaces()

    def _on_labels_changed(self, _bbox):
        if not self._stale and self.state.editor is not None:
            self._stale = True
            self.btn_update.setText("Update *")

    def rebuild_surfaces(self, synchronous: bool = False):
        st = self.state
        if st.editor is None:
            return
        self._token += 1
        self._stale = False
        self.btn_update.setText("Update")
        self.info.setText("extracting surfaces...")
        labels = st.editor.labels.copy() if not synchronous else st.editor.labels
        if synchronous:
            self._surfaces_ready(extract_surfaces(labels, st.spacing), self._token)
            return
        job = _SurfaceJob(labels, st.spacing, self._token)
        job.sig.done.connect(self._surfaces_ready)
        job.sig.failed.connect(lambda msg, _t: self.info.setText(f"surface extraction failed: {msg}"))
        self.pool.start(job)

    def _surfaces_ready(self, res, token):
        if token != self._token:
            return
        for a in self.surface_actors.values():
            self.renderer.RemoveActor(a)
        self.surface_actors.clear()
        for c, poly in res["surfaces"].items():
            m = vtkPolyDataMapper()
            m.SetInputData(poly)
            m.ScalarVisibilityOff()
            a = vtkActor()
            a.SetMapper(m)
            pr = a.GetProperty()
            pr.SetSpecular(0.15)
            pr.SetSpecularPower(20)
            pr.SetDiffuse(0.85)
            pr.SetAmbient(0.12)
            self.surface_actors[c] = a
            self.renderer.AddActor(a)
        n = sum(p.GetNumberOfPolys() for p in res["surfaces"].values())
        self.info.setText(f"{n:,} triangles" + (f" · stride {res['step']}" if res["step"] > 1 else ""))
        self._apply_overlay()
        self._apply_mode()

    def _apply_overlay(self):
        st = self.state
        if self.roi_actor is not None:
            self.roi_actor.SetVisibility(bool(st.show_roi))
        for c, a in self.surface_actors.items():
            o = st.overlay[c]
            r, g, b = o["color"]
            a.GetProperty().SetColor(r / 255, g / 255, b / 255)
            a.GetProperty().SetOpacity(1.0 if c == 3 and o["opacity"] > 0.5 else max(0.15, min(1.0, o["opacity"] * 1.6)))
            a.SetVisibility(bool(o["visible"]) and self.mode.currentIndex() != 1)
        self.render()

    def _ensure_volume(self):
        if self.volume is not None or not self.state.loaded:
            return
        arr, step = self.state.source.downsampled(VOLUME_VOXELS)
        sp = [s * step / 1000.0 for s in self.state.spacing]
        img = to_vtk_image(arr.astype(np.float32), sp)
        mapper = vtkSmartVolumeMapper()
        mapper.SetInputData(img)
        prop = vtkVolumeProperty()
        prop.ShadeOn()
        prop.SetInterpolationTypeToLinear()
        prop.SetAmbient(0.3)
        prop.SetDiffuse(0.7)
        self.volume = vtkVolume()
        self.volume.SetMapper(mapper)
        self.volume.SetProperty(prop)
        self.renderer.AddVolume(self.volume)
        self._update_volume_tf()

    def _update_volume_tf(self):
        if self.volume is None:
            return
        lo, hi = self.state.window
        ctf = vtkColorTransferFunction()
        ctf.AddRGBPoint(lo, 0.0, 0.0, 0.0)
        ctf.AddRGBPoint(lo + 0.5 * (hi - lo), 0.75, 0.72, 0.66)
        ctf.AddRGBPoint(hi, 1.0, 0.98, 0.94)
        otf = vtkPiecewiseFunction()
        otf.AddPoint(lo, 0.0)
        otf.AddPoint(lo + 0.45 * (hi - lo), 0.0)
        otf.AddPoint(hi, 0.55)
        self.volume.GetProperty().SetColor(ctf)
        self.volume.GetProperty().SetScalarOpacity(otf)
        self.render()

    def _apply_mode(self):
        m = self.mode.currentIndex()
        if m in (1, 2):
            self._ensure_volume()
        if self.volume is not None:
            self.volume.SetVisibility(m in (1, 2))
        for c, a in self.surface_actors.items():
            a.SetVisibility(m != 1 and bool(self.state.overlay[c]["visible"]))
        self.render()

    def reset_camera(self):
        cam = self.renderer.GetActiveCamera()
        cam.SetPosition(0, -1, -0.6)
        cam.SetFocalPoint(0, 0, 0)
        cam.SetViewUp(0, 0, -1)
        self.renderer.ResetCamera()
        cam.Dolly(1.25)
        self.renderer.ResetCameraClippingRange()
        self.render()

    # ------------------------------------------------------------------ output
    def render(self):
        if self.image_backend:
            w, h = max(2, self.canvas.width()), max(2, self.canvas.height())
            self.rw.SetSize(w, h)
            self.rw.Render()
            self.canvas.frame = self.grab_frame()
            self.canvas.update()
        else:
            self.rw.Render()

    def grab_frame(self) -> QImage:
        f = vtkWindowToImageFilter()
        f.SetInput(self.rw)
        f.SetInputBufferTypeToRGB()
        f.ReadFrontBufferOff()
        f.Update()
        img = f.GetOutput()
        w, h, _ = img.GetDimensions()
        a = vtk_to_numpy(img.GetPointData().GetScalars()).reshape(h, w, 3)[::-1].copy()
        q = QImage(a.data, w, h, 3 * w, QImage.Format_RGB888)
        return q.copy()

    def screenshot(self, path) -> bool:
        if not self.image_backend:
            self.rw.Render()
        else:
            self.render()
        return self.grab_frame().save(str(path))

    def legend_text(self) -> str:
        return ", ".join(CLASS_NAMES[c] for c in self.surface_actors)

    def shutdown(self):
        self.pool.waitForDone(5000)
        if self.vtk_widget is not None:
            self.vtk_widget.Finalize()
        else:
            self.rw.Finalize()
