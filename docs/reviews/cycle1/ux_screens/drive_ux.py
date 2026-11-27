"""UX review driver (cycle 1). Drives OsteoQuant Desktop programmatically and captures
screenshots at 1600x1000 into this folder. Run from the repository root:

    QT_QPA_PLATFORM=offscreen nice -n 10 python docs/reviews/cycle1/ux_screens/drive_ux.py

Modal message boxes are intercepted and logged (they would block off-screen runs); the log and
the inspected table contents are written to ux_log.json next to the screenshots.
"""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
import time
import traceback
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent
LOG = {"messages": [], "notes": {}}


def main():
    from PySide6.QtCore import QSettings, Qt
    from PySide6.QtWidgets import QApplication, QMessageBox

    app = QApplication.instance() or QApplication(sys.argv)

    # ---- intercept modal message boxes
    def _mk(kind, ret):
        def f(parent, title, text, *a, **k):
            LOG["messages"].append({"kind": kind, "title": title, "text": text})
            print(f"[{kind}] {title}: {text}")
            return ret
        return f
    QMessageBox.warning = _mk("warning", QMessageBox.Ok)
    QMessageBox.critical = _mk("critical", QMessageBox.Ok)
    QMessageBox.information = _mk("information", QMessageBox.Ok)
    QMessageBox.question = _mk("question", QMessageBox.Yes)

    from osteoquant.desktop import theme
    from osteoquant.desktop import services as S
    from osteoquant.desktop.demo import DEMO_PASSWORD, REVIEWER_PASSWORD, write_phantom
    from osteoquant.desktop.dialogs import (AboutDialog, AnalysisDialog, LicenceDialog, LoginDialog, NewProjectDialog,
                                            NewStudyDialog, RoiDialog, SaveRevisionDialog, SignDialog)
    from osteoquant.desktop.import_wizard import ImportModel, ImportWizard
    from osteoquant.desktop.main_window import MainWindow
    from osteoquant.desktop.project import Project
    from osteoquant.desktop.results_view import build_rows
    from osteoquant.desktop.selftest import _wait
    from osteoquant.desktop.settings import AppSettings
    from osteoquant.licensing import evaluation_status

    def settle(n=10):
        for _ in range(n):
            app.processEvents()
            time.sleep(0.01)

    def shot(widget, name):
        settle(6)
        p = OUT / name
        widget.grab().save(str(p))
        print("saved", p.name)
        return str(p)

    tmp = Path(tempfile.mkdtemp(prefix="oq_ux_"))
    theme.apply_theme(app, "light")

    # ------------------------------------------------------------------ project + study
    folder = tmp / "ux_project"
    src = tmp / "sources"
    src.mkdir()
    p = Project.create(folder, "UX review study", "analyst", DEMO_PASSWORD, "A. Analyst")
    oid = p.user["org_id"]
    p.store.create_user(oid, "reviewer", REVIEWER_PASSWORD, "reviewer", "R. Reviewer", actor=p.user)
    sid = p.create_study("Condyle defect, mixed grafts (synthetic phantoms)", "rabbit", "condyle", "various", blinded=True)
    g1 = p.store.add_group(p.user, sid, "Control")
    g2 = p.store.add_group(p.user, sid, "Treatment BMP-2")
    m = ImportModel(p, sid)
    shape = (48, 72, 72)
    mats = ["beta_tcp", "beta_tcp", "beta_tcp", "beta_tcp", "beta_tcp"]
    for i in range(5):
        f = write_phantom(src / f"R{i + 1:02d}_week8.nii.gz", seed=20 + i, shape=shape, stage=0.4 + 0.1 * (i % 3),
                          diameter_um=1600.0, material=mats[i])
        c = m.add_path(f)[0]
        c.animal_id = f"R{i + 1:02d}"
        c.group_id = g1 if i % 2 == 0 else g2
        c.timepoint, c.days = "Week 8", 56
    m.run()
    p.close()

    settings = AppSettings(QSettings(str(tmp / "settings.ini"), QSettings.IniFormat))
    settings.add_recent(folder)
    lic = evaluation_status()
    w = MainWindow(settings, lic)
    w.resize(1600, 1000)
    w.show()
    settle()
    shot(w, "ux01_start_page.png")

    # new project dialog: weak password error path
    npd = NewProjectDialog(w)
    npd.name.setText("Test")
    npd.folder.setText(str(tmp / "weak"))
    npd.user.setText("x")
    npd.pw1.setText("short")
    npd.pw2.setText("short")
    npd.show()
    try:
        Project.create(tmp / "weak", "Test", "x", "short", "")
    except Exception as e:  # noqa: BLE001
        LOG["notes"]["weak_password_error"] = f"{type(e).__name__}: {e}"
        npd.show_error(str(e))
    shot(npd, "ux02_new_project_weak_password.png")
    npd.close()

    ld = LoginDialog("UX review study", "analyst", w)
    ld.show_error("Sign-in failed: wrong user name or password, inactive or temporarily locked account.")
    ld.show()
    shot(ld, "ux03_login_failed.png")
    ld.close()

    assert w.open_project(str(folder), "analyst", DEMO_PASSWORD)
    settle()
    shot(w, "ux04_project_opened.png")

    # ------------------------------------------------------------------ import wizard: bad + missing spacing
    inc = tmp / "incoming"
    inc.mkdir()
    write_phantom(inc / "R06_week8_raw.npy", seed=60, shape=shape, stage=0.6, fmt="npy")
    (inc / "R07_corrupt.nii.gz").write_bytes(b"this is not a nifti file at all")
    (inc / "notes.txt").write_text("lab notes")
    # 2D tif stack folder without resolution tags
    try:
        import tifffile
        stack = inc / "R08_tiffstack"
        stack.mkdir()
        vol = np.load(inc / "R06_week8_raw.npy")
        for k in range(vol.shape[0]):
            tifffile.imwrite(stack / f"slice_{k:04d}.tif", vol[k].astype(np.float32))
    except Exception as e:  # noqa: BLE001
        LOG["notes"]["tiff_stack"] = repr(e)
    wiz = ImportWizard(w.project, w.jobs, sid, w, [str(inc)])
    wiz.resize(1600, 1000)
    wiz.show()
    settle()
    shot(wiz, "ux05_import_sources.png")
    LOG["notes"]["import_candidates"] = [(c.path.name, c.probe.ok, c.probe.error, c.probe.spacing_source if c.probe.ok else None,
                                         c.probe.warnings if c.probe.ok else None) for c in wiz.model.candidates]
    wiz.next()
    settle()
    shot(wiz, "ux06_import_metadata_missing_spacing.png")
    LOG["notes"]["import_problems_before"] = wiz.model.problems()
    wiz.meta.all_sp.setValue(40.0)
    wiz.meta._apply_all()
    settle()
    shot(wiz, "ux07_import_metadata_confirmed.png")
    wiz.next()
    settle()
    shot(wiz, "ux08_import_assignment.png")
    wiz.next()
    wiz.runp.run()
    _wait(app, w.jobs)
    settle()
    shot(wiz, "ux09_import_results.png")
    LOG["notes"]["import_outcomes"] = [(c.path.name, c.outcome.status if c.outcome else None,
                                        c.outcome.reason if c.outcome else None) for c in wiz.model.candidates]
    wiz.accept()
    w.refresh_tree()
    settle()
    shot(w, "ux10_tree_with_rejected.png")

    # ------------------------------------------------------------------ analysis with different materials
    scans = {s["source_name"]: s["id"] for s in w.project.store.scans(w.project.user, sid)}
    LOG["notes"]["scans"] = scans
    dlg = AnalysisDialog(len(scans), "condyle", w)
    dlg.show()
    shot(dlg, "ux11_analysis_dialog.png")
    LOG["notes"]["analysis_seg_options"] = [(dlg.seg.itemText(i), dlg.seg.itemData(i, Qt.ToolTipRole))
                                            for i in range(dlg.seg.count())]
    LOG["notes"]["analysis_material_options"] = [dlg.material.itemText(i) for i in range(dlg.material.count())]
    dlg.close()
    base = {"defect_model": "condyle", "nominal_diameter_um": 1600, "graft_brighter": True,
            "thickness_metrics": True, "segmentation": "multiotsu"}
    plan = [("R01_week8.nii.gz", {}, "Unspecified"),
            ("R02_week8.nii.gz", {"no_graft": True}, "No graft"),
            ("R03_week8.nii.gz", {"material": "ha"}, "HA"),
            ("R04_week8.nii.gz", {"material": "collagen_sponge"}, "Collagen sponge"),
            ("R05_week8.nii.gz", {"material": "beta_tcp", "segmentation": "onnx:unet_noctx_s0"}, "beta-TCP + U-Net")]
    LOG["notes"]["analysis_plan"] = [(a, b, c) for a, b, c in plan]
    for name, extra, _ in plan:
        sc = scans.get(name)
        if sc is None:
            continue
        w.analyze_selected([sc], {**base, **extra}, True)
    t0 = time.time()
    # check UI responsiveness while jobs run: time processEvents round trips
    lat = []
    while w.jobs.active_jobs() and time.time() - t0 < 600:
        a = time.time()
        app.processEvents()
        lat.append(time.time() - a)
        time.sleep(0.02)
    w.jobs.wait(2000)
    settle()
    LOG["notes"]["ui_event_loop_max_ms_during_analysis"] = round(1000 * max(lat or [0]), 1)
    shot(w, "ux12_jobs_after_analysis.png")
    for j in w.jobs.jobs.values():
        LOG["notes"].setdefault("jobs", []).append((j.title, j.status, j.error[:300]))

    # results
    w.tabs.setCurrentWidget(w.results)
    w.results.set_project(w.project, sid)
    settle()
    shot(w, "ux13_results_light.png")
    rows = build_rows(w.project, sid)
    LOG["notes"]["results_rows"] = [{"scan": r["scan"], "status": r["status"], "status_tip": r["status_tip"],
                                     "values": {k: [v["value"], v["status"], v["tip"]] for k, v in r["values"].items()}}
                                    for r in rows]
    # hover tooltip text for a "not measured" cell
    w.results.view.horizontalScrollBar().setValue(w.results.view.horizontalScrollBar().maximum())
    settle()
    shot(w, "ux14_results_scrolled.png")

    # ------------------------------------------------------------------ viewer + editing
    w.tabs.setCurrentWidget(w.workspace)
    first = scans["R01_week8.nii.gz"]
    w.open_scan(first)
    try:
        w.workspace.view3d.rebuild_surfaces(synchronous=True)
    except Exception as e:  # noqa: BLE001
        LOG["notes"]["view3d"] = repr(e)
    settle(15)
    shot(w, "ux15_viewer_light.png")
    LOG["notes"]["window_presets"] = list(w.state.presets().keys())
    st = w.state
    w.d_seg.raise_()
    st.set_tool("brush")
    st.set_brush(radius_um=120, label=1, protect=True)
    z = st.cursor[0]
    st.paint_stroke(0, z, [(20, 20), (24, 30), (30, 38)])
    st.set_brush(label=2)
    st.paint_stroke(0, z, [(50, 50), (52, 54)])
    w.workspace.views[0]._hover = (40.0, 40.0)
    settle()
    shot(w, "ux16_editing.png")
    st.history.undo()
    settle()
    shot(w, "ux17_after_undo.png")
    st.history.redo()
    settle()
    LOG["notes"]["title_with_edits"] = w.windowTitle()
    srd = SaveRevisionDialog(st.editor.change_summary(), st.segmentation["version"], w)
    srd.show()
    shot(srd, "ux18_save_revision_dialog.png")
    srd.close()
    w.save_revision("Graft particle misclassified as new bone at margin", wait=True)
    _wait(app, w.jobs)
    st.set_tool("navigate")
    settle()
    w.d_display.raise_()
    shot(w, "ux19_after_save_display_panel.png")
    LOG["notes"]["seg_versions_combo"] = [w.display.seg_combo.itemText(i) for i in range(w.display.seg_combo.count())]

    # maximised axial view
    w.workspace.toggle_max(0)
    settle()
    shot(w, "ux20_viewer_maximised_axial.png")
    w.workspace.toggle_max(0)

    # ROI dialog
    rd = RoiDialog(st.cursor, st.spacing, w)
    rd.show()
    shot(rd, "ux21_roi_dialog.png")
    rd.close()

    # ------------------------------------------------------------------ review as author (should be refused)
    w.d_review.raise_()
    settle()
    shot(w, "ux22_review_panel_analyst.png")
    try:
        S.sign_review(w.project, DEMO_PASSWORD, "segmentation", st.segmentation["id"], "approved",
                      "Reviewed the segmentation and approve it for reporting")
        LOG["notes"]["analyst_self_sign"] = "accepted"
    except Exception as e:  # noqa: BLE001
        LOG["notes"]["analyst_self_sign"] = f"{type(e).__name__}: {e}"

    # ------------------------------------------------------------------ reviewer: blinded sign-off
    w.close_project()
    settle()
    assert w.open_project(str(folder), "reviewer", REVIEWER_PASSWORD)
    w.set_blinded(True)
    w.open_scan(first)
    w.d_review.raise_()
    settle()
    shot(w, "ux23_reviewer_blinded_review.png")
    sd = SignDialog(w.project.user, f"segmentation {st.segmentation['id']}", "approved", w)
    sd.show()
    shot(sd, "ux24_sign_dialog.png")
    sd.close()
    try:
        rid = w.sign("segmentation", st.segmentation["id"], "approved", password=REVIEWER_PASSWORD,
                     meaning="Reviewed the segmentation and approve it for reporting")
        LOG["notes"]["reviewer_sign"] = rid
    except Exception as e:  # noqa: BLE001
        LOG["notes"]["reviewer_sign"] = f"{type(e).__name__}: {e}"
    try:
        S.sign_review(w.project, "wrong-password", "segmentation", st.segmentation["id"], "approved", "ok")
    except Exception as e:  # noqa: BLE001
        LOG["notes"]["short_meaning_error"] = f"{type(e).__name__}: {e}"
    settle()
    shot(w, "ux25_reviewer_signed.png")
    w.tabs.setCurrentWidget(w.results)
    w.results.set_project(w.project, sid)
    settle()
    shot(w, "ux26_results_blinded.png")
    LOG["notes"]["infobar_blinded"] = w.workspace.infobar.text()
    LOG["notes"]["qc_banner_blinded"] = w.qc.banner.text()
    LOG["notes"]["jobs_titles_blinded"] = [w.jobs_panel.table.item(r, 1).text() for r in range(w.jobs_panel.table.rowCount())
                                           if w.jobs_panel.table.item(r, 1)]

    # ------------------------------------------------------------------ report (reviewer, blinded view on)
    w.generate_report(sid)
    _wait(app, w.jobs)
    settle(20)
    w.reports.preview.go(0)
    settle(10)
    shot(w, "ux27_report_preview_p1.png")
    w.reports.preview.go(1)
    settle(10)
    shot(w, "ux28_report_preview_p2.png")
    w.reports.preview.go(2)
    settle(10)
    shot(w, "ux29_report_preview_p3.png")
    rep = w.reports.current_report()
    LOG["notes"]["report"] = {k: rep.get(k) for k in ("id", "status", "pdf_path", "unblinded")} if rep else None
    if rep and rep.get("pdf_path"):
        shutil.copyfile(rep["pdf_path"], OUT / "ux_report_sample.pdf")
    # approve the report as the same reviewer who generated it
    try:
        rr = w.sign("report", rep["id"], "approved", password=REVIEWER_PASSWORD,
                    meaning="Reviewed the report and approve its release")
        LOG["notes"]["report_self_approve"] = f"accepted ({rr})"
    except Exception as e:  # noqa: BLE001
        LOG["notes"]["report_self_approve"] = f"{type(e).__name__}: {e}"
    settle()
    shot(w, "ux30_report_approved.png")

    # ------------------------------------------------------------------ audit
    w.tabs.setCurrentWidget(w.audit)
    w.audit.refresh()
    w.audit.verify_chain()
    settle()
    shot(w, "ux31_audit_blinded.png")
    # search the audit table for file names while blinded
    leaks = []
    for e in w.audit._events:
        s = json.dumps(e.get("details"), default=str)
        if any(n in s for n in ("R01_week8", "R02_week8", "Control", "Treatment BMP-2")):
            leaks.append((e["seq"], e["action"], s[:200]))
    LOG["notes"]["audit_leaks_in_blinded_mode"] = leaks[:10]
    LOG["notes"]["audit_leak_count"] = len(leaks)
    w.audit.filter.setText("segmentation.edit")
    settle()
    if w.audit._events:
        for r in range(w.audit.table.rowCount()):
            if not w.audit.table.isRowHidden(r):
                w.audit.table.selectRow(r)
                break
    settle()
    shot(w, "ux32_audit_filtered.png")
    w.audit.filter.setText("")
    w.set_blinded(False)

    # ------------------------------------------------------------------ licence / about
    ldlg = LicenceDialog(lic, w)
    ldlg.show()
    shot(ldlg, "ux33_licence.png")
    ldlg.close()
    ab = AboutDialog(lic, w)
    ab.show()
    shot(ab, "ux34_about.png")
    ab.close()

    # ------------------------------------------------------------------ cancel + failure paths
    w.tabs.setCurrentWidget(w.workspace)
    jb = w.analyze_selected([scans["R03_week8.nii.gz"]], {**base, "material": "ha"}, True)
    settle(3)
    w.jobs.cancel(jb[0].id)
    _wait(app, w.jobs)
    LOG["notes"]["cancel_job"] = (jb[0].status, jb[0].message)
    LOG["notes"]["reviewer_analyse_job"] = [(j.title, j.status, j.error) for j in w.jobs.jobs.values()][-1]
    w.close_project()
    assert w.open_project(str(folder), "analyst", DEMO_PASSWORD)
    jb = w.analyze_selected([scans["R03_week8.nii.gz"]], {**base, "material": "ha"}, True)
    settle(3)
    w.jobs.cancel(jb[0].id)
    _wait(app, w.jobs)
    LOG["notes"]["cancel_job_analyst"] = (jb[0].status, jb[0].message)
    # failing report: new empty study
    sid2 = w.project.create_study("Empty study", "rat", "calvarial", "", blinded=False)
    w.refresh_tree()
    w.generate_report(sid2)
    _wait(app, w.jobs)
    settle()
    w.d_jobs.raise_()
    settle()
    shot(w, "ux35_jobs_cancel_and_failure.png")

    # ------------------------------------------------------------------ dark theme
    w.set_theme("dark")
    w.open_scan(first)
    try:
        w.workspace.view3d.rebuild_surfaces(synchronous=True)
        w.workspace.view3d.mode.setCurrentIndex(2)
    except Exception:  # noqa: BLE001
        pass
    w.d_seg.raise_()
    settle(15)
    shot(w, "ux36_viewer_dark_segpanel.png")
    w.tabs.setCurrentWidget(w.results)
    w.results.set_project(w.project, sid)
    settle()
    shot(w, "ux37_results_dark.png")
    w.tabs.setCurrentWidget(w.reports)
    settle()
    shot(w, "ux38_reports_dark.png")
    wiz2 = ImportWizard(w.project, w.jobs, sid, w, [str(inc / "R06_week8_raw.npy")])
    wiz2.resize(1600, 1000)
    wiz2.show()
    wiz2.next()
    settle()
    shot(wiz2, "ux39_import_metadata_dark.png")
    wiz2.reject()
    ad = AnalysisDialog(3, "condyle", w)
    ad.show()
    shot(ad, "ux40_analysis_dialog_dark.png")
    ad.close()
    w.tabs.setCurrentWidget(w.audit)
    settle()
    shot(w, "ux41_audit_dark.png")
    w.set_theme("light")

    # ------------------------------------------------------------------ small window (truncation)
    w.tabs.setCurrentWidget(w.workspace)
    w.resize(1280, 760)
    settle(10)
    shot(w, "ux42_viewer_1280x760.png")
    w.resize(1600, 1000)

    (OUT / "ux_log.json").write_text(json.dumps(LOG, indent=2, default=str))
    w.close_project()
    w.close()
    shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        (OUT / "ux_log.json").write_text(json.dumps(LOG, indent=2, default=str))
        sys.exit(1)
