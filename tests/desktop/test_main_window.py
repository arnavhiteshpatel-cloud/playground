"""Main window smoke tests (off-screen) and the --selftest entry point."""
import subprocess
import sys

import numpy as np
import pytest
from PySide6.QtCore import QSettings

PW = "Correct-Horse-9"


@pytest.fixture
def window(qtbot, tmp_path):
    from osteoquant.desktop import theme
    from osteoquant.desktop.main_window import MainWindow
    from osteoquant.desktop.settings import AppSettings
    from osteoquant.licensing import evaluation_status
    from PySide6.QtWidgets import QApplication
    theme.apply_theme(QApplication.instance(), "light")
    w = MainWindow(AppSettings(QSettings(str(tmp_path / "s.ini"), QSettings.IniFormat)), evaluation_status())
    qtbot.addWidget(w)
    w.resize(1300, 850)
    w.show()
    yield w
    w.jobs.wait()


def test_open_project_view_scan_edit_and_save(qtbot, window, analysed):
    project, sid, scan = analysed
    folder = project.folder
    project.close()
    w = window
    assert not w.open_project(str(folder), "admin", "wrong")
    assert w.open_project(str(folder), "admin", PW)
    assert w.tree.topLevelItemCount() == 1
    assert w.open_scan(scan)
    st = w.state
    assert st.loaded and st.editor is not None
    for v in w.workspace.views:
        img = v.render_image()
        assert img.width() > 100
    # crosshair linking: clicking in the axial view moves coronal/sagittal slices
    st.set_cursor(5, 10, 12)
    assert w.workspace.views[1].index == 10 and w.workspace.views[2].index == 12
    st.set_window(0, 1000)
    assert w.display.hi.value() == 1000
    st.set_overlay(1, visible=False)
    assert st.overlay_rgba(np.array([[1]], np.uint8))[0, 0, 3] == 0
    st.set_brush(radius_um=80, label=2, protect=False)
    assert st.paint_stroke(0, 5, [(20, 20)])
    assert "*" in w.windowTitle()
    job = w.save_revision("test correction", wait=True)
    assert job.status == "done", job.error
    qtbot.waitUntil(lambda: st.segmentation and st.segmentation["kind"] == "corrected", timeout=10000)
    assert "*" not in w.windowTitle()


def test_blinded_mode_and_audit_verify(qtbot, window, analysed):
    project, sid, scan = analysed
    folder = project.folder
    project.close()
    w = window
    assert w.open_project(str(folder), "admin", PW)
    w.set_blinded(True)
    names = []

    def walk(it):
        names.append(it.text(0))
        for i in range(it.childCount()):
            walk(it.child(i))
    walk(w.tree.topLevelItem(0))
    assert not any(n.endswith(".nii.gz") for n in names)
    res = w.audit.verify_chain()
    assert res["ok"]


def test_screenshot_export(qtbot, window, analysed, tmp_path):
    project, sid, scan = analysed
    folder = project.folder
    project.close()
    w = window
    w.open_project(str(folder), "admin", PW)
    w.open_scan(scan)
    w.workspace.view3d.rebuild_surfaces(synchronous=True)
    assert w.export_screenshot(str(tmp_path / "v.png"))
    assert w.export_screenshot(str(tmp_path / "3d.png"), what="3d")
    from PySide6.QtGui import QImage
    assert QImage(str(tmp_path / "3d.png")).width() > 50
    assert len(w.workspace.view3d.surface_actors) >= 1


def test_oblique_reslice_identity():
    from osteoquant.desktop.oblique import oblique_slice
    vol = np.zeros((10, 20, 30), np.float32)
    vol[5] = np.arange(30)[None, :]
    arr, px = oblique_slice(vol, (2.0, 2.0, 2.0), (10.0, 20.0, 30.0), 0, 0)
    assert px == 2.0 and arr.shape == (20, 30)
    assert np.allclose(arr[::-1][7], np.arange(30), atol=1e-3)


def test_about_lists_third_party_licences(qtbot):
    from osteoquant.desktop.dialogs import AboutDialog, third_party_components
    from osteoquant.licensing import evaluation_status
    comps = {c[0]: c for c in third_party_components()}
    assert "VTK" in comps and "PySide6 / Qt" in comps and "LGPL" in comps["PySide6 / Qt"][2]
    d = AboutDialog(evaluation_status())
    qtbot.addWidget(d)


def test_selftest_entry_point():
    r = subprocess.run([sys.executable, "-m", "osteoquant.desktop", "--selftest"], capture_output=True, text=True,
                       timeout=600, env={**__import__("os").environ, "QT_QPA_PLATFORM": "offscreen"})
    assert r.returncode == 0, r.stdout[-3000:] + r.stderr[-3000:]
    assert '"selftest": "PASS"' in r.stdout
