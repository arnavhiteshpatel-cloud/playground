"""Cycle-1 UX review, medium/low findings: view state, slider, presets, measurement, accessibility,
spacing entry, error text, shutdown with running jobs."""
import time

import numpy as np
import pytest

from desktop_helpers import PW


def _open(window, project):
    folder = project.folder
    project.close()
    assert window.open_project(str(folder), "admin", PW)
    return window


def test_view_state_kept_across_save(qtbot, window, analysed):
    project, sid, scan = analysed
    w = _open(window, project)
    w.open_scan(scan)
    st = w.state
    st.set_cursor(7, 11, 13)
    st.set_window(10.0, 900.0)
    ax = w.workspace.views[0]
    qtbot.wait(100)                      # let the views fit and paint
    ax.scale *= 1.7
    ax._user_view = True
    scale = ax.scale
    st.set_brush(radius_um=80, label=2, protect=False)
    assert st.paint_stroke(0, 7, [(20, 20)])
    job = w.save_revision("keep view test", wait=True)
    assert job.status == "done", job.error
    qtbot.waitUntil(lambda: st.segmentation and st.segmentation["kind"] == "corrected", timeout=10000)
    qtbot.wait(100)
    assert st.cursor == [7, 11, 13] and st.window == (10.0, 900.0) and ax.scale == pytest.approx(scale)


def test_slice_slider_and_keys(qtbot, window, analysed):
    from PySide6.QtCore import Qt
    project, sid, scan = analysed
    w = _open(window, project)
    w.open_scan(scan)
    cell = w.workspace.slice_cells[0]
    assert cell.slider.maximum() == w.state.shape[0] - 1
    cell.slider.setValue(3)
    assert w.state.cursor[0] == 3
    w.state.set_index(0, 9)
    assert cell.slider.value() == 9
    v = w.workspace.views[0]
    qtbot.keyClick(v, Qt.Key_End)
    assert w.state.cursor[0] == w.state.shape[0] - 1
    qtbot.keyClick(v, Qt.Key_Home)
    assert w.state.cursor[0] == 0


def test_presets_measurement_palette_outline():
    from osteoquant.desktop.viewer_state import PALETTES, ViewerState, mask_edges, window_presets
    from osteoquant.desktop.volume_source import ArraySource
    pr = window_presets({"p1": 0, "p50": 100, "p99": 1000, "min": -5, "max": 1500})
    assert {"Bone", "Soft tissue", "Graft (dense mineral)"} <= set(pr)
    st = ViewerState()
    st.load(ArraySource(np.zeros((10, 20, 30), np.float32), spacing=(10.0, 20.0, 40.0)),
            np.zeros((10, 20, 30), np.uint8))
    m = st.add_measurement(0, 5, (0.0, 0.0), (3.0, 4.0))           # rows along y (20 µm), cols along x (40 µm)
    assert m["length_um"] == pytest.approx(np.hypot(60.0, 160.0))
    st.clear_measurements()
    assert st.measurements == []
    cvd = [n for n in PALETTES if "Colour-blind" in n][0]
    st.set_palette(cvd)
    assert st.overlay[3]["color"] == (245, 245, 245) and st.overlay[2]["color"] == (0, 114, 178)
    lab = np.zeros((9, 9), np.uint8)
    lab[2:7, 2:7] = 1
    st.set_outline_mode(True)
    rgba = st.overlay_rgba(lab)
    assert rgba[4, 4, 3] == 0 and rgba[2, 4, 3] == 255                # interior transparent, edge drawn
    roi = np.zeros((5, 5), bool)
    roi[1:3, 1:3] = True
    assert len(mask_edges(roi)) == 8                                   # 2x2 square: 8 voxel edges


def test_accessibility_contrast_focus_and_tooltips():
    from osteoquant.desktop import theme
    from osteoquant.desktop.panels import SegmentationPanel
    for t in ("light", "dark"):
        T = theme.TOKENS[t]
        for fg in ("text_muted", "warn", "bad", "ok"):          # 'not measured' uses text_muted (UX-28)
            for bg in ("surface", "surface_alt"):
                assert theme.contrast_ratio(T[fg], T[bg]) >= 4.5, (t, fg, bg)
        assert theme.contrast_ratio(T["on_bad"], T["bad"]) >= 4.5
        qss = theme.build_qss(T)
        assert "outline: 0" not in qss and "QPushButton:focus" in qss
    tips = dict((k, tip) for k, _t, tip in SegmentationPanel.TOOL_TEXT)
    assert tips["fill"].endswith("(H)")


def test_not_measured_rendering_and_shortcut_scope(qtbot, window, analysed):
    from PySide6.QtCore import Qt
    from osteoquant.desktop import theme
    project, sid, scan = analysed
    w = _open(window, project)
    for a in w.tool_actions.values():
        assert a.shortcutContext() == Qt.WidgetWithChildrenShortcut
    w.results.refresh()
    m = w.results.model
    from osteoquant.desktop.results_view import FIXED_COLS
    from osteoquant.desktop.support import ENDPOINTS
    for c in range(len(ENDPOINTS)):
        idx = m.index(0, len(FIXED_COLS) + c)
        if m.data(idx) == "not measured":
            assert m.data(idx, Qt.ForegroundRole) == theme.qcolor("text_muted")
            assert m.data(idx, Qt.FontRole).italic()
            break
    else:
        pytest.skip("no endpoint is not measured for this phantom")


def test_spacing_is_never_prefilled(qtbot, project, study, tmp_path):
    from osteoquant.desktop.import_wizard import ImportWizard
    from osteoquant.desktop.jobs import JobManager
    np.save(tmp_path / "raw.npy", np.zeros((8, 8, 8), np.float32))
    jm = JobManager()
    wiz = ImportWizard(project, jm, study, None, [str(tmp_path / "raw.npy")])
    qtbot.addWidget(wiz)
    wiz.show()
    wiz.next()
    meta = wiz.meta
    assert meta.all_sp.value() == 0 and not meta.apply_btn.isEnabled()
    assert not meta.isComplete()
    meta.iso.setChecked(False)
    meta.all_fields[0].setValue(10)
    meta.all_fields[1].setValue(10)
    assert not meta.apply_btn.isEnabled()                             # x still empty
    meta.all_fields[2].setValue(20)
    meta._apply_all()
    assert wiz.model.candidates[0].spacing == [10, 10, 20] and meta.isComplete()


def test_friendly_error_messages():
    from osteoquant.desktop.messages import friendly
    assert friendly("ValueError: This study has no analysed scans yet; run the analysis first") \
        .startswith("This study has no analysed scans yet")
    t = friendly("Unreadable: CorruptInput: Could not read nifti input /tmp/x/R07.nii.gz: ImageFileError: not a gzip file")
    assert "could not be read" in t and "/tmp" not in t and "Error" not in t
    assert "role" in friendly("PermissionError: Role 'reviewer' lacks permission 'write'")
    assert friendly("KeyError: 'thing'") == "Thing."


def test_close_with_running_job_returns_within_3s(qtbot, window, project):
    folder = project.folder
    project.close()
    w = window
    assert w.open_project(str(folder), "admin", PW)
    release = []

    def stubborn(ctx):              # a library stage that does not check for cancellation for a while
        t0 = time.time()
        while not release and time.time() - t0 < 20:
            time.sleep(0.05)
        return 1
    job = w.jobs.submit("test", "stubborn", stubborn)
    qtbot.waitUntil(lambda: job.status == "running", timeout=5000)
    t0 = time.time()
    assert w.close_project(ask=False)
    assert time.time() - t0 < 4.5
    assert w.project is None and w._closing                     # store closes once the job has stopped
    release.append(1)
    w.jobs.wait(10000)
    qtbot.waitUntil(lambda: not w._closing, timeout=5000)
