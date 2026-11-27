# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for OsteoQuant Desktop (one-folder build).

Build with ``python packaging/build.py`` (runs PyInstaller, adds third-party licence texts and
runs the packaged self-test). Two executables share one runtime folder:
  OsteoQuant                  windowed application (no console)
  osteoquant-desktop-console  same program with a console: --selftest output, CI, support

Environment switches (read at build time):
  OQ_BUNDLE_TORCH=1   include PyTorch (only needed for "unet:" models; ~0.8-1 GB). Default 0.
  OQ_BUNDLE_ONNX=0    leave out ONNX Runtime. Default 1 (included).
  OQ_BUNDLE_SITK=1    include SimpleITK (MetaImage .mha/.mhd import only; ~260 MB). Default 0.
"""
import os
import sys
from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

ROOT = Path(SPECPATH).resolve().parent          # noqa: F821 (SPECPATH is injected by PyInstaller)
BUNDLE_TORCH = os.environ.get("OQ_BUNDLE_TORCH", "0") == "1"
BUNDLE_ONNX = os.environ.get("OQ_BUNDLE_ONNX", "1") == "1"
BUNDLE_SITK = os.environ.get("OQ_BUNDLE_SITK", "0") == "1"

hidden = []
hidden += collect_submodules("osteoquant", filter=lambda m: not m.startswith(("osteoquant.experiments",)))
hidden += [
    "vtkmodules.vtkInteractionStyle", "vtkmodules.vtkRenderingOpenGL2", "vtkmodules.vtkRenderingVolumeOpenGL2",
    "vtkmodules.vtkRenderingVolume", "vtkmodules.vtkRenderingUI", "vtkmodules.util.numpy_support",
    "vtkmodules.qt.QVTKRenderWindowInteractor",
    "PySide6.QtPdf", "PySide6.QtPdfWidgets", "PySide6.QtOpenGL", "PySide6.QtOpenGLWidgets",
    "numcodecs", "zarr.codecs", "imagecodecs", "pydicom.pixels", "nibabel", "nrrd", "olefile",
    "reportlab.graphics.barcode", "sklearn.mixture", "sklearn.cluster", "pypdfium2",
]

datas = [(str(ROOT / "osteoquant" / "phantom" / "data"), "osteoquant/phantom/data")]
datas += collect_data_files("reportlab")
datas += collect_data_files("pydicom", includes=["**/*.json"])
datas += collect_data_files("skimage", includes=["**/*.txt"])

excludes = [
    "tkinter", "_tkinter", "IPython", "jupyter", "notebook", "pytest", "pytestqt", "sphinx", "PyQt5", "PyQt6",
    "PySide2", "matplotlib.backends.backend_tkagg", "matplotlib.backends.backend_qtagg",
    "PySide6.QtWebEngineCore", "PySide6.QtWebEngineWidgets", "PySide6.QtWebEngineQuick", "PySide6.QtWebChannel",
    "PySide6.QtWebSockets", "PySide6.Qt3DCore", "PySide6.Qt3DRender", "PySide6.Qt3DExtras", "PySide6.Qt3DInput",
    "PySide6.Qt3DLogic", "PySide6.Qt3DAnimation", "PySide6.QtQuick3D", "PySide6.QtCharts",
    "PySide6.QtDataVisualization", "PySide6.QtGraphs", "PySide6.QtGraphsWidgets", "PySide6.QtMultimedia",
    "PySide6.QtMultimediaWidgets", "PySide6.QtBluetooth", "PySide6.QtLocation", "PySide6.QtPositioning",
    "PySide6.QtSensors", "PySide6.QtSerialPort", "PySide6.QtSerialBus", "PySide6.QtNfc", "PySide6.QtRemoteObjects",
    "PySide6.QtScxml", "PySide6.QtSpatialAudio", "PySide6.QtTextToSpeech", "PySide6.QtHttpServer",
    "PySide6.QtDesigner", "PySide6.QtHelp", "PySide6.QtQuickWidgets", "PySide6.QtQuickControls2",
    "PySide6.QtWebView", "PySide6.QtNetworkAuth",
    "uvicorn", "uvloop", "httptools", "watchfiles", "websockets",     # the desktop never serves HTTP
]
if not BUNDLE_SITK:
    excludes += ["SimpleITK"]
if not BUNDLE_TORCH:
    excludes += ["torch", "torchvision", "torchaudio", "triton", "functorch"]
if not BUNDLE_ONNX:
    excludes += ["onnxruntime", "onnx"]

a = Analysis(  # noqa: F821
    [str(ROOT / "packaging" / "launcher.py")],
    pathex=[str(ROOT)],
    binaries=[],
    datas=datas,
    hiddenimports=hidden,
    hookspath=[],
    runtime_hooks=[],
    excludes=excludes,
    noarchive=False,
)
pyz = PYZ(a.pure)  # noqa: F821

_icon = ROOT / "packaging" / "icons" / ("osteoquant.ico" if sys.platform.startswith("win") else "osteoquant.icns")
icon = str(_icon) if _icon.exists() and sys.platform != "linux" else None
datas += [(str(ROOT / "osteoquant" / "desktop" / "resources"), "osteoquant/desktop/resources")]

common = dict(exclude_binaries=True, debug=False, bootloader_ignore_signals=False, strip=False, upx=False,
              icon=icon, codesign_identity=os.environ.get("OQ_CODESIGN_IDENTITY") or None,
              entitlements_file=os.environ.get("OQ_ENTITLEMENTS") or None)
exe_gui = EXE(pyz, a.scripts, [], name="OsteoQuant", console=False, **common)  # noqa: F821
exe_cli = EXE(pyz, a.scripts, [], name="osteoquant-desktop-console", console=True, **common)  # noqa: F821
coll = COLLECT(exe_gui, exe_cli, a.binaries, a.datas, strip=False, upx=False, name="OsteoQuant")  # noqa: F821

if sys.platform == "darwin":
    app = BUNDLE(  # noqa: F821
        coll, name="OsteoQuant.app", icon=icon, bundle_identifier="com.osteoquant.desktop",
        info_plist={"CFBundleShortVersionString": "0.1.0", "NSHighResolutionCapable": True,
                    "LSMinimumSystemVersion": "12.0", "NSRequiresAquaSystemAppearance": False},
    )
