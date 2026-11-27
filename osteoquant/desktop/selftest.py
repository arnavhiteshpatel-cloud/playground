"""Headless end-to-end self-test used by CI and by packaging smoke tests.

Steps: synthetic phantom -> import wizard model (format detection, explicit spacing) -> QC ->
analysis on a background job -> main window opens the scan -> slice views and 3D panel render ->
label edit, undo/redo, save revision -> report (with licence watermark) -> PDF opens -> audit
chain verifies. Prints one JSON line per step; returns 0 if every step passed, else 1.
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
import time
import traceback
from pathlib import Path


def _emit(line: str, log):
    """Print if a console is attached (windowed builds have no stdout) and append to the log."""
    if sys.stdout is not None:
        try:
            print(line, flush=True)
        except OSError:
            pass
    if log is not None:
        log.write(line + "\n")
        log.flush()


def run_selftest(out_dir: str | None = None) -> int:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    t0 = time.time()
    results = []
    tmp = Path(tempfile.mkdtemp(prefix="oq_selftest_"))
    keep = out_dir is not None
    out = Path(out_dir) if out_dir else tmp
    out.mkdir(parents=True, exist_ok=True)
    log = open(out / "selftest.jsonl", "w", encoding="utf-8") if keep else None

    def step(name, fn):
        t = time.time()
        try:
            detail = fn()
            rec = {"step": name, "ok": True, "s": round(time.time() - t, 2), "detail": detail}
        except Exception as e:  # noqa: BLE001
            rec = {"step": name, "ok": False, "s": round(time.time() - t, 2), "error": f"{type(e).__name__}: {e}",
                   "traceback": traceback.format_exc(limit=6)}
        results.append(rec)
        _emit(json.dumps(rec, default=str), log)
        return rec["ok"]

    ctx = {}
    try:
        from .app import make_app
        app = make_app()
        from . import theme
        theme.apply_theme(app, "light")
        from PySide6.QtCore import QSettings
        from ..licensing import current_status
        from .demo import DEMO_PASSWORD, write_phantom
        from .import_wizard import ImportModel
        from .project import Project
        from .settings import AppSettings

        def s_phantom():
            ctx["src"] = write_phantom(tmp / "selftest_phantom.nii.gz", shape=(40, 56, 56), diameter_um=1400.0)
            return {"file": str(ctx["src"])}

        def s_import():
            p = Project.create(tmp / "project", "Self-test project", "analyst", DEMO_PASSWORD, "Self Test")
            ctx["p"] = p
            sid = p.create_study("Self-test study", "rabbit", "condyle", "beta-TCP")
            ctx["sid"] = sid
            m = ImportModel(p, sid)
            c = m.add_path(ctx["src"])[0]
            assert c.probe.format == "nifti", c.probe.format
            assert c.probe.spacing_source == "file", c.probe.spacing_source
            c.animal_id, c.timepoint, c.days = "ST01", "Week 4", 28
            assert not m.problems(), m.problems()
            o = m.run()[0]
            assert o.status in ("imported", "flagged"), o.reason
            ctx["scan"] = o.scan_id
            det, heu = o.qc_deterministic, o.qc_heuristic
            assert det and heu
            return {"status": o.status, "scan_id": o.scan_id, "qc_verdict": o.qc["verdict"],
                    "deterministic_checks": len(det), "heuristic_checks": len(heu)}

        def s_window():
            from .main_window import MainWindow
            st = AppSettings(QSettings(str(tmp / "settings.ini"), QSettings.IniFormat))
            w = MainWindow(st, current_status())
            w.resize(1400, 880)
            w.show()
            w._after_open(ctx["p"])
            app.processEvents()
            ctx["w"] = w
            return {"title": w.windowTitle(), "3d_backend": "image" if w.workspace.view3d.image_backend else "interactive"}

        def s_analyze():
            w = ctx["w"]
            jobs = w.analyze_selected([ctx["scan"]], {"defect_model": "condyle", "nominal_diameter_um": 1400,
                                                      "material": "beta_tcp"}, True)
            _wait(app, w.jobs)
            j = jobs[0]
            assert j.status == "done", f"{j.status}: {j.error}\n{j.traceback}"
            assert j.result["status"] == "complete_unreviewed", j.result
            return {"job": j.status, "result": j.result.get("status"), "segmentation_version": j.result.get("version")}

        def s_render():
            w = ctx["w"]
            assert w.open_scan(ctx["scan"])
            app.processEvents()
            w.workspace.view3d.rebuild_surfaces(synchronous=True)
            app.processEvents()
            info = {}
            for v in w.workspace.views:
                img = v.render_image()
                arr = _qimage_std(img)
                assert arr > 1.0, f"slice view {v.axis} rendered blank"
                info[f"slice{v.axis}_std"] = round(arr, 1)
            p3 = out / "selftest_3d.png"
            assert w.workspace.view3d.screenshot(p3)
            from PySide6.QtGui import QImage
            s3 = _qimage_std(QImage(str(p3)))
            assert s3 > 1.0, "3D view rendered blank"
            info["3d_std"] = round(s3, 1)
            info["surfaces"] = len(w.workspace.view3d.surface_actors)
            assert info["surfaces"] >= 1
            w.export_screenshot(str(out / "selftest_viewer.png"))
            return info

        def s_edit():
            import numpy as np
            w = ctx["w"]
            st = w.state
            before = st.editor.labels.copy()
            st.set_brush(radius_um=120, label=2, protect=False)
            z = st.cursor[0]
            assert st.paint_stroke(0, z, [(20, 20), (24, 26)])
            after = st.editor.labels.copy()
            st.history.undo()
            assert np.array_equal(st.editor.labels, before), "undo did not restore labels"
            st.history.redo()
            assert np.array_equal(st.editor.labels, after), "redo did not re-apply edit"
            ch = st.editor.change_summary()
            job = w.save_revision("self-test correction", wait=True)
            assert job.status == "done", job.error
            return {"changed": ch, "new_version": job.result["version"]}

        def s_report():
            w = ctx["w"]
            job = w.generate_report(ctx["sid"])
            _wait(app, w.jobs)
            assert job.status == "done", f"{job.status}: {job.error}"
            pdf = job.result["pdf"]
            assert Path(pdf).read_bytes()[:4] == b"%PDF"
            app.processEvents()
            n = w.reports.preview.page_count()
            assert n > 0, "PDF preview has no pages"
            shutil.copyfile(pdf, out / "selftest_report.pdf")
            return {"pages": n, "watermark": w.licence.watermark, "sha256": job.result["sha256"][:16]}

        def s_audit():
            res = ctx["p"].store.audit.verify_chain()
            assert res["ok"], res
            acts = {e["action"] for e in ctx["p"].store.audit.events(limit=10000)}
            need = {"scan.import", "scan.qc", "segmentation.save", "segmentation.edit", "report.generate"}
            assert need <= acts, need - acts
            return {"events": res["n"]}

        for name, fn in (("phantom", s_phantom), ("import_qc", s_import), ("main_window", s_window),
                         ("analysis_job", s_analyze), ("render", s_render), ("edit_undo_save", s_edit),
                         ("report", s_report), ("audit_chain", s_audit)):
            if not step(name, fn):
                break
        if "w" in ctx:
            ctx["w"].close()
    except Exception as e:  # noqa: BLE001
        results.append({"step": "startup", "ok": False, "error": f"{type(e).__name__}: {e}",
                        "traceback": traceback.format_exc()})
        _emit(json.dumps(results[-1], default=str), log)
    ok = bool(results) and all(r["ok"] for r in results) and len(results) == 8
    _emit(json.dumps({"selftest": "PASS" if ok else "FAIL", "steps": len(results), "seconds": round(time.time() - t0, 1),
                      "python": sys.version.split()[0], "frozen": bool(getattr(sys, "frozen", False))}), log)
    if log is not None:
        log.close()
    if not keep:
        shutil.rmtree(tmp, ignore_errors=True)
    return 0 if ok else 1


def _wait(app, jobs, timeout=600):
    t = time.time()
    while jobs.active_jobs() and time.time() - t < timeout:
        app.processEvents()
        time.sleep(0.02)
    jobs.wait(1000)
    for _ in range(5):
        app.processEvents()


def _qimage_std(img) -> float:
    import numpy as np
    img = img.convertToFormat(img.Format.Format_RGB32)
    ptr = img.constBits()
    arr = np.frombuffer(ptr, np.uint8, img.sizeInBytes()).reshape(img.height(), img.bytesPerLine())
    return float(arr[:, : img.width() * 4].std())
