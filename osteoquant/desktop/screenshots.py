"""Capture documentation screenshots of the main screens (off-screen rendering).

    python -m osteoquant.desktop --screenshots docs/screenshots/desktop
"""
from __future__ import annotations

import shutil
import tempfile
import time
from pathlib import Path


def _settle(app, n=8):
    for _ in range(n):
        app.processEvents()
        time.sleep(0.01)


def _wait_jobs(app, w):
    from .selftest import _wait
    _wait(app, w.jobs)


def capture_all(out_dir, themes=("light", "dark")) -> list[str]:
    from PySide6.QtCore import QSettings
    from PySide6.QtWidgets import QApplication
    from ..licensing import evaluation_status
    from . import theme
    from .demo import build_demo_project
    from .dialogs import AboutDialog, LicenceDialog, SaveRevisionDialog
    from .import_wizard import ImportWizard
    from .main_window import MainWindow
    from .settings import AppSettings

    app = QApplication.instance()
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix="oq_shots_"))
    files = []

    def save(widget_or_image, name):
        p = out / name
        img = widget_or_image if hasattr(widget_or_image, "save") and not hasattr(widget_or_image, "grab") \
            else widget_or_image.grab()
        img.save(str(p))
        files.append(str(p))

    theme.apply_theme(app, "light")
    project, sid, _ = build_demo_project(tmp / "demo_project", n_animals=4, shape=(56, 96, 96))
    folder = project.folder
    project.close()
    settings = AppSettings(QSettings(str(tmp / "settings.ini"), QSettings.IniFormat))
    settings.add_recent(folder)
    lic = evaluation_status()
    w = MainWindow(settings, lic)
    w.resize(1600, 1000)
    w.show()
    _settle(app)
    save(w, "01_start_page.png")

    assert w.open_project(str(folder), "analyst", "Demo-Password-2026")
    _settle(app)
    scans = [s["id"] for s in w.project.store.scans(w.project.user, sid)]
    w.open_scan(scans[0])
    w.workspace.view3d.rebuild_surfaces(synchronous=True)
    w.state.set_cursor(*[n // 2 for n in w.state.shape])
    _settle(app)
    save(w, "02_viewer_light.png")

    # segmentation editing: brush stroke + region grow on the axial view
    st = w.state
    w.d_seg.raise_()
    st.set_tool("brush")
    st.set_brush(radius_um=120, label=1, protect=True)
    z = st.cursor[0]
    st.paint_stroke(0, z, [(30, 30), (34, 40), (40, 48)])
    st.set_brush(label=2)
    st.paint_stroke(0, z, [(58, 62), (62, 66)])
    w.workspace.views[0]._hover = (50.0, 30.0)
    _settle(app)
    save(w, "03_segmentation_editing.png")
    dlg = SaveRevisionDialog(st.editor.change_summary(), st.segmentation["version"], w)
    dlg.reason.setPlainText("Graft particle misclassified as new bone at the defect margin")
    dlg.show()
    _settle(app)
    save(dlg, "04_save_revision_dialog.png")
    dlg.close()
    w.save_revision("Graft particle misclassified as new bone at the defect margin", wait=True)
    _wait_jobs(app, w)
    st.set_tool("navigate")
    _settle(app)

    # import wizard: metadata page with a file lacking spacing, and the results page
    from .demo import write_phantom
    extra = tmp / "incoming"
    extra.mkdir()
    write_phantom(extra / "R20_week8.nii.gz", seed=41, shape=(48, 72, 72), stage=0.8)
    write_phantom(extra / "R21_week8_raw.npy", seed=42, shape=(48, 72, 72), stage=0.8, fmt="npy")
    wiz = ImportWizard(w.project, w.jobs, sid, w, [str(extra)])
    wiz.show()
    wiz.next()
    _settle(app)
    save(wiz, "05_import_metadata.png")
    wiz.meta.all_sp.setValue(40.0)
    wiz.meta._apply_all()
    wiz.next()
    for c in wiz.model.candidates:
        c.timepoint, c.days = "Week 8", 56
    wiz.assign.initializePage()
    wiz.next()
    wiz.runp.run()
    _wait_jobs(app, w)
    _settle(app)
    save(wiz, "06_import_qc_results.png")
    wiz.accept()
    w.refresh_tree()

    w.tabs.setCurrentWidget(w.results)
    w.results.set_project(w.project, sid)
    _settle(app)
    save(w, "07_results.png")

    w.generate_report(sid)
    _wait_jobs(app, w)
    _settle(app, 20)
    w.reports.preview.go(1)
    _settle(app, 10)
    save(w, "08_report_preview.png")

    w.tabs.setCurrentWidget(w.audit)
    w.audit.refresh()
    w.audit.verify_chain()
    _settle(app)
    save(w, "09_audit_trail.png")

    w.tabs.setCurrentWidget(w.workspace)
    w.open_scan(scans[1])
    w.set_blinded(True)
    w.d_review.raise_()
    _settle(app)
    save(w, "10_review_blinded.png")
    w.set_blinded(False)

    ab = AboutDialog(lic, w)
    ab.show()
    _settle(app)
    save(ab, "11_about.png")
    ab.close()
    ld = LicenceDialog(lic, w)
    ld.show()
    _settle(app)
    save(ld, "12_licence.png")
    ld.close()

    if "dark" in themes:
        w.set_theme("dark")
        w.tabs.setCurrentWidget(w.workspace)
        w.open_scan(scans[0])
        w.workspace.view3d.rebuild_surfaces(synchronous=True)
        w.workspace.view3d.mode.setCurrentIndex(2)
        w.d_display.raise_()
        _settle(app, 15)
        save(w, "13_viewer_dark.png")
        w.tabs.setCurrentWidget(w.results)
        _settle(app)
        save(w, "14_results_dark.png")
        w.set_theme("light")
    w.close()
    shutil.rmtree(tmp, ignore_errors=True)
    print("\n".join(files))
    return files
