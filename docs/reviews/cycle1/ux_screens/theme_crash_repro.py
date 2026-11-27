"""Theme-switch crash probe. Variant given as argv[1]:
  plain   - open project + scan, dark -> light -> dark -> light
  wizard  - same, after opening/cancelling the import wizard via MainWindow.import_scans
  dialog  - same, after an un-owned closed dialog parented to the window (script artefact check)
Run: PYTHONPATH=. QT_QPA_PLATFORM=offscreen python -X faulthandler docs/reviews/cycle1/ux_screens/theme_crash_repro.py plain
"""
import sys
import tempfile
import time
from pathlib import Path

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication

from osteoquant.desktop import theme
from osteoquant.desktop.demo import DEMO_PASSWORD, build_demo_project
from osteoquant.desktop.dialogs import AnalysisDialog
from osteoquant.desktop.main_window import MainWindow
from osteoquant.desktop.settings import AppSettings
from osteoquant.licensing import evaluation_status

variant = sys.argv[1] if len(sys.argv) > 1 else "plain"
app = QApplication(sys.argv)
theme.apply_theme(app, "light")
tmp = Path(tempfile.mkdtemp(prefix="oq_theme_"))
p, sid, _ = build_demo_project(tmp / "p", n_animals=2, shape=(32, 48, 48))
folder = p.folder
p.close()
w = MainWindow(AppSettings(QSettings(str(tmp / "s.ini"), QSettings.IniFormat)), evaluation_status())
w.resize(1600, 1000)
w.show()
w.open_project(str(folder), "analyst", DEMO_PASSWORD)
scans = [s["id"] for s in w.project.store.scans(w.project.user, sid)]
w.open_scan(scans[0])


def settle():
    for _ in range(10):
        app.processEvents()
        time.sleep(0.01)


settle()
if variant == "wizard":
    wiz = w.import_scans(sid)
    settle()
    wiz.reject()
    settle()
elif variant in ("wizard_meta", "wizard_meta_nodelete"):
    from osteoquant.desktop.demo import write_phantom
    npy = write_phantom(tmp / "raw.npy", seed=5, shape=(32, 48, 48), fmt="npy")
    if variant == "wizard_meta":
        wiz = w.import_scans(sid, [str(npy)])
    else:
        from osteoquant.desktop.import_wizard import ImportWizard
        wiz = ImportWizard(w.project, w.jobs, sid, w, [str(npy)])
        wiz.show()
    settle()
    wiz.next()
    settle()
    w.set_theme("dark")
    settle()
    wiz.reject()
    settle()
elif variant == "dialog":
    d = AnalysisDialog(1, "condyle", w)
    d.show()
    settle()
    d.close()
for i, name in enumerate(("dark", "light", "dark", "light")):
    w.set_theme(name)
    settle()
    print("switched", i, name, flush=True)
print("OK", variant)
w.close_project()
