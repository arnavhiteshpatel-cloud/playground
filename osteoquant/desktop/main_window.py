"""Main window: start page, project tree, viewer workspace, results, reports, audit, docks."""
from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QSize, Qt, QTimer
from PySide6.QtGui import QAction, QActionGroup, QKeySequence
from PySide6.QtWidgets import (QApplication, QDockWidget, QFileDialog, QFrame, QGridLayout, QHBoxLayout, QInputDialog,
                               QLabel, QListWidget, QListWidgetItem, QMainWindow, QMessageBox, QProgressBar, QScrollArea,
                               QPushButton, QStackedWidget, QTabWidget, QVBoxLayout, QWidget)

from .. import __version__
from ..licensing import LicenceStatus, current_status, install_licence
from . import services as S
from . import theme
from .dialogs import (AboutDialog, AnalysisDialog, LicenceDialog, LoginDialog, NewProjectDialog, NewStudyDialog,
                      RoiDialog, SaveRevisionDialog, SignDialog)
from .import_wizard import ImportWizard
from .jobs import JobManager
from .oblique import ObliqueView
from .panels import DisplayPanel, JobsPanel, QCPanel, SegmentationPanel, VoxelInfoPanel, muted
from .project import Project, ProjectError, is_project_folder
from .project_tree import ProjectTree
from .reports_view import ReportsView
from .results_view import ResultsView
from .review_audit import AuditView, ReviewPanel
from .settings import AppSettings
from .slice_view import SliceView
from .timing import ActivityFilter, TimingRecorder
from .view3d import View3D
from .viewer_state import ViewerState
from .volume_source import ZarrSource

APP_TITLE = "OsteoQuant Desktop"


class StartPage(QWidget):
    def __init__(self, win: "MainWindow"):
        super().__init__()
        self.win = win
        outer = QVBoxLayout(self)
        outer.addStretch(1)
        row = QHBoxLayout()
        row.addStretch(1)
        card = QFrame()
        card.setProperty("role", "card")
        card.setFixedWidth(620)
        cl = QVBoxLayout(card)
        cl.setContentsMargins(32, 28, 32, 26)
        cl.setSpacing(10)
        t = QLabel("OsteoQuant Desktop")
        t.setProperty("role", "title")
        cl.addWidget(t)
        cl.addWidget(muted("Micro-CT analysis of bone-defect healing: import, quality control, segmentation review, "
                           "endpoints and reports. Projects are folders on this computer; no network is used."))
        br = QHBoxLayout()
        b1 = QPushButton("New project...")
        b1.setProperty("role", "primary")
        b1.clicked.connect(win.new_project)
        b2 = QPushButton("Open project...")
        b2.clicked.connect(lambda: win.open_project())
        br.addWidget(b1)
        br.addWidget(b2)
        br.addStretch(1)
        cl.addSpacing(6)
        cl.addLayout(br)
        cl.addSpacing(10)
        lb = QLabel("RECENT PROJECTS")
        lb.setProperty("role", "section")
        cl.addWidget(lb)
        self.recent = QListWidget()
        self.recent.setMinimumHeight(150)
        self.recent.itemActivated.connect(lambda it: win.open_project(it.data(Qt.UserRole)))
        cl.addWidget(self.recent)
        self.lic = muted("")
        cl.addWidget(self.lic)
        row.addWidget(card)
        row.addStretch(1)
        outer.addLayout(row)
        outer.addStretch(2)

    def refresh(self):
        self.recent.clear()
        for p in self.win.settings.recent_projects():
            it = QListWidgetItem(f"{Path(p).name}    {p}")
            it.setData(Qt.UserRole, p)
            self.recent.addItem(it)
        if not self.recent.count():
            it = QListWidgetItem("No recent projects")
            it.setFlags(Qt.NoItemFlags)
            self.recent.addItem(it)
        self.lic.setText(f"Version {__version__}  ·  {self.win.licence.summary()}")


class ViewerWorkspace(QWidget):
    """Three linked slice views and the 3D panel in a 2 x 2 grid; double-click maximises."""

    def __init__(self, state: ViewerState, parent=None):
        super().__init__(parent)
        self.state = state
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        self.infobar = QLabel("No scan open. Double-click a scan in the project tree.")
        self.infobar.setProperty("role", "banner-info")
        lay.addWidget(self.infobar)
        self.grid_host = QWidget()
        self.grid = QGridLayout(self.grid_host)
        self.grid.setContentsMargins(2, 2, 2, 2)
        self.grid.setSpacing(2)
        self.views = [SliceView(state, a) for a in range(3)]
        self.view3d = View3D(state)
        self.cells = [self.views[0], self.view3d, self.views[1], self.views[2]]
        for i, w in enumerate(self.cells):
            self.grid.addWidget(w, i // 2, i % 2)
        for v in self.views:
            v.maximize_requested.connect(self.toggle_max)
        lay.addWidget(self.grid_host, 1)
        self._max = None

    def toggle_max(self, axis):
        target = self.views[axis]
        if self._max is target:
            for w in self.cells:
                w.show()
            self._max = None
        else:
            for w in self.cells:
                w.setVisible(w is target)
            self._max = target

    def set_info(self, text, kind="info"):
        from .panels import set_banner
        set_banner(self.infobar, text, kind)


class MainWindow(QMainWindow):
    def __init__(self, settings: AppSettings | None = None, licence: LicenceStatus | None = None):
        super().__init__()
        self.settings = settings or AppSettings()
        self.licence = licence or current_status()
        self.project: Project | None = None
        self.blinded_view = False
        self.current_scan_id = None
        self.setWindowTitle(APP_TITLE)
        self.resize(1480, 920)
        self.setDockOptions(QMainWindow.AnimatedDocks | QMainWindow.AllowTabbedDocks | QMainWindow.AllowNestedDocks)
        self.jobs = JobManager(self)
        self.state = ViewerState(self)
        self.state.message.connect(lambda m: self.statusBar().showMessage(m, 6000))
        self.timing: TimingRecorder | None = None
        self.activity = ActivityFilter(self)
        QApplication.instance().installEventFilter(self.activity)
        self.state.edit_applied.connect(lambda tool, delta: self.timing and self.timing.edit(tool, delta))

        # ---------------- central
        self.stack = QStackedWidget()
        self.start = StartPage(self)
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.workspace = ViewerWorkspace(self.state)
        self.results = ResultsView()
        self.reports = ReportsView()
        self.audit = AuditView()
        self.tabs.addTab(self.workspace, "Viewer")
        self.tabs.addTab(self.results, "Results")
        self.tabs.addTab(self.reports, "Reports")
        self.tabs.addTab(self.audit, "Audit trail")
        self.tabs.currentChanged.connect(self._tab_changed)
        self.stack.addWidget(self.start)
        self.stack.addWidget(self.tabs)
        self.setCentralWidget(self.stack)

        # ---------------- docks
        self.tree = ProjectTree()
        self.tree.scan_activated.connect(self.open_scan)
        self.tree.context_action.connect(self._tree_action)
        self.tree.selection_changed_.connect(self._tree_selection)
        tree_host = QWidget()
        tl = QVBoxLayout(tree_host)
        tl.setContentsMargins(6, 6, 6, 6)
        tb = QHBoxLayout()
        bi = QPushButton("Import...")
        bi.clicked.connect(lambda: self.import_scans())
        ba = QPushButton("Analyse...")
        ba.clicked.connect(lambda: self.analyze_selected())
        tb.addWidget(bi)
        tb.addWidget(ba)
        tl.addLayout(tb)
        tl.addWidget(self.tree, 1)
        self.d_project = self._dock("Project", tree_host, Qt.LeftDockWidgetArea)
        self.display = DisplayPanel(self.state)
        self.display.segmentation_selected.connect(lambda sid: self.open_scan(self.current_scan_id, sid))
        self.segpanel = SegmentationPanel(self.state)
        self.segpanel.save_requested.connect(self.save_revision)
        self.voxel = VoxelInfoPanel(self.state)
        self.review = ReviewPanel()
        self.review.sign_requested.connect(self.sign)
        self.review.blinded_toggled.connect(self.set_blinded)
        self.oblique = ObliqueView(self.state)
        self.d_display = self._dock("Display", self.display, Qt.RightDockWidgetArea, scroll=True)
        self.d_voxel = self._dock("Voxel", self.voxel, Qt.RightDockWidgetArea, scroll=True)
        self.splitDockWidget(self.d_display, self.d_voxel, Qt.Vertical)
        self.d_seg = self._dock("Segmentation", self.segpanel, Qt.RightDockWidgetArea, scroll=True)
        self.d_review = self._dock("Review", self.review, Qt.RightDockWidgetArea)
        self.d_oblique = self._dock("Oblique", self.oblique, Qt.RightDockWidgetArea)
        self.tabifyDockWidget(self.d_display, self.d_seg)
        self.tabifyDockWidget(self.d_seg, self.d_review)
        self.tabifyDockWidget(self.d_review, self.d_oblique)
        self.d_display.raise_()
        self.qc = QCPanel()
        self.jobs_panel = JobsPanel(self.jobs)
        self.d_jobs = self._dock("Jobs", self.jobs_panel, Qt.BottomDockWidgetArea)
        self.d_qc = self._dock("Quality control", self.qc, Qt.BottomDockWidgetArea)
        self.tabifyDockWidget(self.d_jobs, self.d_qc)
        self.d_qc.raise_()
        self.resizeDocks([self.d_project], [290], Qt.Horizontal)
        self.resizeDocks([self.d_display], [320], Qt.Horizontal)
        self._docks_sized = False

        self.results.open_scan.connect(self.open_scan)
        self.reports.generate_requested.connect(self.generate_report)
        self.reports.sign_requested.connect(lambda rid, dec: self.sign("report", rid, dec))
        self.jobs.job_finished.connect(self._job_finished)
        self.jobs.job_changed.connect(self._job_progress)
        self.state.history.cleanChanged.connect(lambda *_: self._update_title())
        self.state.history.indexChanged.connect(lambda *_: self._update_title())

        self._build_actions()
        self._build_status()
        self._set_project_ui(False)
        self.start.refresh()

    # ================================================================== construction
    def _dock(self, title, widget, area, scroll=False):
        d = QDockWidget(title, self)
        d.setObjectName(f"dock_{title.replace(' ', '_').lower()}")
        if scroll:
            sa = QScrollArea()
            sa.setWidgetResizable(True)
            sa.setFrameShape(QFrame.NoFrame)
            sa.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            sa.setWidget(widget)
            widget = sa
        d.setWidget(widget)
        d.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetClosable)
        self.addDockWidget(area, d)
        return d

    def _act(self, text, slot=None, shortcut=None, checkable=False, tip=None):
        a = QAction(text, self)
        if shortcut:
            a.setShortcut(QKeySequence(shortcut))
        if slot:
            a.triggered.connect(slot)
        a.setCheckable(checkable)
        if tip:
            a.setStatusTip(tip)
            a.setToolTip(tip)
        return a

    def _build_actions(self):
        mb = self.menuBar()
        f = mb.addMenu("&File")
        self.a_new = self._act("New project...", self.new_project, "Ctrl+N")
        self.a_open = self._act("Open project...", lambda: self.open_project(), "Ctrl+O")
        self.recent_menu = f.addMenu("Open recent")
        self.recent_menu.aboutToShow.connect(self._fill_recent)
        self.a_close = self._act("Close project", self.close_project)
        self.a_import = self._act("Import scans...", lambda: self.import_scans(), "Ctrl+I")
        self.a_shot = self._act("Export screenshot...", self.export_screenshot, "Ctrl+Shift+S")
        self.a_quit = self._act("Quit", self.close, "Ctrl+Q")
        f.insertAction(self.recent_menu.menuAction(), self.a_new)
        f.insertAction(self.recent_menu.menuAction(), self.a_open)
        for a in (self.a_close, None, self.a_import, self.a_shot, None, self.a_quit):
            f.addSeparator() if a is None else f.addAction(a)

        e = mb.addMenu("&Edit")
        self.a_undo = self.state.history.createUndoAction(self, "Undo")
        self.a_undo.setShortcut(QKeySequence.Undo)
        self.a_redo = self.state.history.createRedoAction(self, "Redo")
        self.a_redo.setShortcut(QKeySequence.Redo)
        e.addAction(self.a_undo)
        e.addAction(self.a_redo)
        e.addSeparator()
        self.tool_group = QActionGroup(self)
        self.tool_actions = {}
        for key, text, sc in (("navigate", "Navigate", "N"), ("brush", "Brush", "B"), ("erase", "Eraser", "E"),
                              ("grow", "Region grow", "G"), ("fill", "Fill holes", "H")):
            a = self._act(text, lambda _=False, k=key: self.state.set_tool(k), sc, checkable=True)
            self.tool_group.addAction(a)
            e.addAction(a)
            self.tool_actions[key] = a
        self.tool_actions["navigate"].setChecked(True)
        self.state.tool_changed.connect(lambda: self.tool_actions[self.state.tool].setChecked(True))
        e.addSeparator()
        self.a_save_rev = self._act("Save label revision...", self.save_revision, "Ctrl+S")
        e.addAction(self.a_save_rev)

        st = mb.addMenu("&Study")
        self.a_new_study = self._act("New study...", self.new_study)
        self.a_add_group = self._act("Add group...", lambda: self.add_group())
        self.a_roi = self._act("Define cylindrical ROI at crosshair...", self.define_roi)
        self.a_analyze = self._act("Analyse selected scans...", lambda: self.analyze_selected(), "Ctrl+R")
        self.a_cancel = self._act("Cancel all jobs", self.jobs.cancel_all)
        self.a_report = self._act("Generate report for current study", lambda: self.generate_report(self.tree.current_study_id()))
        for a in (self.a_new_study, self.a_add_group, None, self.a_roi, self.a_analyze, self.a_cancel, None, self.a_report):
            st.addSeparator() if a is None else st.addAction(a)

        v = mb.addMenu("&View")
        self.a_blind = self._act("Blinded review mode", lambda on: self.set_blinded(on), checkable=True)
        v.addAction(self.a_blind)
        tm = v.addMenu("Theme")
        tg = QActionGroup(self)
        for name in ("light", "dark"):
            a = self._act(name.capitalize(), lambda _=False, n=name: self.set_theme(n), checkable=True)
            a.setChecked(theme.current() == name)
            tg.addAction(a)
            tm.addAction(a)
        v.addSeparator()
        for d in (self.d_project, self.d_display, self.d_seg, self.d_review, self.d_oblique, self.d_voxel,
                  self.d_jobs, self.d_qc):
            v.addAction(d.toggleViewAction())

        tools = mb.addMenu("&Tools")
        self.a_timing = self._act("Record workflow timing for this project (stored locally, never transmitted)",
                                  self.set_timing, checkable=True,
                                  tip="Opt-in: records per-scan open/edit/sign-off events and active time "
                                      "(idle > 60 s excluded) in this project's database only")
        self.a_timing_export = self._act("Export workflow timing CSV...", lambda: self.export_timing())
        tools.addAction(self.a_timing)
        tools.addAction(self.a_timing_export)

        h = mb.addMenu("&Help")
        h.addAction(self._act("Licence...", self.show_licence))
        h.addAction(self._act("About OsteoQuant Desktop", self.show_about))

        tb = self.addToolBar("Main")
        tb.setObjectName("toolbar_main")
        tb.setMovable(False)
        tb.setIconSize(QSize(16, 16))
        tb.setToolButtonStyle(Qt.ToolButtonTextOnly)
        for a in (self.a_open, self.a_import, None, self.a_analyze, self.a_save_rev, None):
            tb.addSeparator() if a is None else tb.addAction(a)
        for k in ("navigate", "brush", "erase", "grow", "fill"):
            tb.addAction(self.tool_actions[k])
        tb.addSeparator()
        h = self.state.history
        self.tb_undo = self._act("Undo", h.undo)
        self.tb_redo = self._act("Redo", h.redo)
        self.tb_undo.setEnabled(False)
        self.tb_redo.setEnabled(False)
        h.canUndoChanged.connect(self.tb_undo.setEnabled)
        h.canRedoChanged.connect(self.tb_redo.setEnabled)
        h.undoTextChanged.connect(lambda t: self.tb_undo.setToolTip(f"Undo {t}"))
        h.redoTextChanged.connect(lambda t: self.tb_redo.setToolTip(f"Redo {t}"))
        tb.addAction(self.tb_undo)
        tb.addAction(self.tb_redo)
        tb.addSeparator()
        tb.addAction(self.a_shot)

    def _build_status(self):
        sb = self.statusBar()
        self.s_user = QLabel("")
        self.s_lic = QLabel("")
        self.s_job = QLabel("")
        self.s_bar = QProgressBar()
        self.s_bar.setRange(0, 1000)
        self.s_bar.setFixedWidth(160)
        self.s_bar.hide()
        self.s_mem = QLabel("")
        sb.addPermanentWidget(self.s_job)
        sb.addPermanentWidget(self.s_bar)
        sb.addPermanentWidget(self.s_mem)
        sb.addPermanentWidget(self.s_lic)
        sb.addPermanentWidget(self.s_user)
        self._mem_timer = QTimer(self)
        self._mem_timer.timeout.connect(self._update_memory)
        self._mem_timer.start(2000)
        self._update_memory()
        self._update_licence_label()

    def _update_memory(self):
        try:
            import psutil
            rss = psutil.Process().memory_info().rss
            avail = psutil.virtual_memory().available
            cache = self.state.source.cache.bytes if self.state.source else 0
            self.s_mem.setText(f"Memory {rss / 2**20:,.0f} MiB  ·  slice cache {cache / 2**20:,.0f} MiB  ·  "
                               f"free {avail / 2**30:,.1f} GiB")
        except Exception:  # noqa: BLE001
            self.s_mem.setText("")

    def _update_licence_label(self):
        st = self.licence
        self.s_lic.setText(st.summary() if st.state == "valid" else "Evaluation mode")
        self.s_lic.setToolTip(st.summary())

    def _set_project_ui(self, on: bool):
        self.stack.setCurrentIndex(1 if on else 0)
        for d in (self.d_project, self.d_display, self.d_seg, self.d_review, self.d_oblique, self.d_voxel,
                  self.d_jobs, self.d_qc):
            d.setVisible(on)
        for a in (self.a_close, self.a_import, self.a_new_study, self.a_add_group, self.a_roi, self.a_analyze,
                  self.a_report, self.a_save_rev, self.a_shot, self.a_timing, self.a_timing_export):
            a.setEnabled(on)
        self.d_oblique.hide()
        if on:
            self.d_display.raise_()
            self.d_qc.raise_()
            QTimer.singleShot(0, self._size_docks)
        self._update_title()

    def _update_title(self):
        t = APP_TITLE
        if self.project:
            t = f"{self.project.name} - {APP_TITLE}"
            if self.state.editor is not None and self.state.editor.modified:
                t = "* " + t
            u = self.project.user
            self.s_user.setText(f"{u.get('full_name') or u['username']} ({u['role']})" if u else "")
        else:
            self.s_user.setText("")
        self.setWindowTitle(t)

    # ================================================================== projects
    def new_project(self):
        dlg = NewProjectDialog(self)
        while dlg.exec():
            v = dlg.values()
            try:
                p = Project.create(v["folder"], v["name"], v["username"], v["password"], v["full_name"])
            except (ProjectError, ValueError, OSError) as e:
                dlg.show_error(str(e))
                continue
            self.settings.set_last_user(p.folder, v["username"])
            self._after_open(p)
            if not p.store.list_studies(p.user):
                self.new_study()
            return p
        return None

    def open_project(self, folder=None, username=None, password=None) -> bool:
        if folder is None:
            folder = QFileDialog.getExistingDirectory(self, "Open OsteoQuant project folder")
            if not folder:
                return False
        if not is_project_folder(folder):
            QMessageBox.warning(self, "Not a project", f"{folder}\n\nis not an OsteoQuant project folder.")
            return False
        if not self.close_project():
            return False
        try:
            p = Project(folder)
        except Exception as e:  # noqa: BLE001
            QMessageBox.critical(self, "Cannot open project", str(e))
            return False
        if username is not None:
            if not p.login(username, password or ""):
                p.close()
                return False
        else:
            dlg = LoginDialog(p.name, self.settings.last_user(folder), self)
            while True:
                if not dlg.exec():
                    p.close()
                    return False
                if p.login(dlg.user.text().strip(), dlg.pw.text()):
                    break
                dlg.show_error("Sign-in failed: wrong user name or password, inactive or temporarily locked account.")
                dlg.pw.clear()
            self.settings.set_last_user(folder, p.user["username"])
        self._after_open(p)
        return True

    def _after_open(self, p: Project):
        self.project = p
        self.jobs.set_project(p)
        self.timing = TimingRecorder(p)
        self.activity.set_recorder(self.timing)
        self.a_timing.setChecked(self.timing.enabled)
        self.settings.add_recent(p.folder)
        self._set_project_ui(True)
        self.refresh_tree()
        sid = self.tree.current_study_id()
        self.results.set_project(p, sid)
        self.reports.set_project(p, sid, self.licence.watermark)
        self.audit.set_project(p)
        self.review.set_scan(p, None)
        self.workspace.set_info(f"Project {p.name} opened. Double-click a scan in the project tree to view it.")
        self.statusBar().showMessage(f"Signed in as {p.user['username']}", 5000)

    def close_project(self) -> bool:
        if self.project is None:
            return True
        if not self._confirm_discard_edits():
            return False
        if self.jobs.active_jobs():
            if QMessageBox.question(self, "Jobs running", "Background jobs are running. Cancel them and close?") \
                    != QMessageBox.Yes:
                return False
            self.jobs.cancel_all()
            self.jobs.wait(30000)
        self.state.unload()
        self.current_scan_id = None
        self.activity.set_recorder(None)
        self.timing = None
        self.project.close()
        self.project = None
        self.jobs.set_project(None)
        self.tree.clear()
        self._set_project_ui(False)
        self.start.refresh()
        return True

    def _fill_recent(self):
        m = self.recent_menu
        m.clear()
        for p in self.settings.recent_projects():
            m.addAction(p, lambda _=False, p=p: self.open_project(p))
        if not m.actions():
            a = m.addAction("No recent projects")
            a.setEnabled(False)

    def refresh_tree(self):
        if self.project:
            self.tree.populate(self.project.study_tree(self.blinded_view))

    # ================================================================== studies / import
    def new_study(self):
        if not self.project:
            return None
        dlg = NewStudyDialog(self)
        if dlg.exec():
            try:
                sid = self.project.create_study(**dlg.values())
            except PermissionError as e:
                QMessageBox.warning(self, "Not permitted", str(e))
                return None
            self.refresh_tree()
            self.results.set_project(self.project, sid)
            self.reports.set_project(self.project, sid, self.licence.watermark)
            return sid
        return None

    def add_group(self, study_id=None):
        sid = study_id or self.tree.current_study_id()
        if not self.project or sid is None:
            return
        name, ok = QInputDialog.getText(self, "Add group", "Group name (e.g. treatment arm):")
        if ok and name.strip():
            try:
                self.project.store.add_group(self.project.user, sid, name.strip())
            except PermissionError as e:
                QMessageBox.warning(self, "Not permitted", str(e))
            self.refresh_tree()

    def import_scans(self, study_id=None, paths=()):
        if not self.project:
            return None
        if not self.project.store.list_studies(self.project.user):
            if self.new_study() is None:
                return None
        wiz = ImportWizard(self.project, self.jobs, study_id or self.tree.current_study_id(), self, paths)
        wiz.finished.connect(lambda *_: (self.refresh_tree(), self.results.refresh()))
        wiz.open()
        return wiz

    # ================================================================== viewer
    def _confirm_discard_edits(self) -> bool:
        ed = self.state.editor
        if ed is None or not ed.modified:
            return True
        r = QMessageBox.question(self, "Unsaved label edits",
                                 "The open segmentation has unsaved edits. Save them as a new revision?",
                                 QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        if r == QMessageBox.Save:
            self.save_revision()
            return False
        return r == QMessageBox.Discard

    def open_scan(self, scan_id, segmentation_id=None):
        if not self.project or scan_id is None:
            return False
        if self.current_scan_id is not None and not self._confirm_discard_edits():
            return False
        p = self.project
        sc = p.store.scan(p.user, scan_id)
        if not sc.get("store_path"):
            QMessageBox.warning(self, "Scan unavailable", "This scan has no stored image data.")
            return False
        src = ZarrSource(sc["store_path"])
        segs = p.store.segmentations(p.user, scan_id)
        seg = None
        if segs:
            seg = next((s for s in segs if s["id"] == segmentation_id), segs[-1])
        labels = src.load_labels(seg["labels_key"]) if seg and seg.get("labels_key") in src.label_layers() else None
        self.current_scan_id = scan_id
        self.state.load(src, labels, sc, seg)
        self.display.set_segmentations(segs, seg["id"] if seg else None)
        self.qc.show_qc(sc.get("qc"), self._scan_label(sc))
        self.review.set_scan(p, scan_id)
        self.tree.select_scan(scan_id)
        self.tabs.setCurrentWidget(self.workspace)
        self._update_viewer_info()
        p.store.audit.record("scan.view", p.user["id"], p.user["org_id"], "scan", scan_id, {"client": "desktop"})
        if self.timing:
            self.timing.scan_opened(scan_id, sc["study_id"])
        self._update_title()
        return True

    def _scan_label(self, sc) -> str:
        return f"Scan {sc['id']:04d}" if self.blinded_view else f"Scan {sc['id']} - {sc['source_name']}"

    def _update_viewer_info(self):
        st = self.state
        if not st.loaded:
            self.workspace.set_info("No scan open. Double-click a scan in the project tree.")
            return
        sc, seg = st.scan, st.segmentation
        sh = " x ".join(map(str, st.shape))
        sp = ", ".join(f"{s:g}" for s in st.spacing)
        segtxt = (f"segmentation v{seg['version']} ({seg['kind']}, {seg.get('method') or '-'})" if seg
                  else "no segmentation yet - run the analysis to create one, then edit it")
        kind = "info" if seg else "warn"
        self.workspace.set_info(f"{self._scan_label(sc)}   ·   {sh} voxels   ·   {sp} µm   ·   {segtxt}", kind)

    def define_roi(self):
        if not self.state.loaded or self.current_scan_id is None:
            QMessageBox.information(self, "Define ROI", "Open a scan and place the crosshair at the defect centre first.")
            return
        dlg = RoiDialog(self.state.cursor, self.state.spacing, self)
        if dlg.exec():
            try:
                rid = S.save_cylinder_roi(self.project, self.current_scan_id, self.state.cursor, dlg.radius.value(),
                                          (dlg.depth0.value(), dlg.depth1.value()), reason=dlg.reason.text().strip())
                self.statusBar().showMessage(f"ROI {rid} saved. Run the analysis to use it.", 8000)
            except (PermissionError, ValueError) as e:
                QMessageBox.warning(self, "ROI not saved", str(e))

    def save_revision(self, reason: str | None = None, wait: bool = False):
        st = self.state
        if st.editor is None or not st.editor.modified or self.current_scan_id is None:
            return None
        if reason is None:
            dlg = SaveRevisionDialog(st.editor.change_summary(), st.segmentation["version"], self)
            if not dlg.exec():
                return None
            reason = dlg.reason.toPlainText().strip()
        labels = st.editor.labels.copy()
        ops = dict(st.editor.op_counts)
        scan_id, base = self.current_scan_id, st.segmentation["id"]
        project = self.project

        def done(job):
            if job.status == "done":
                st.history.clear()
                st.editor.base_counts = dict(st.editor.counts)
                self.open_scan(scan_id, job.result["segmentation_id"])
                self.statusBar().showMessage(f"Saved segmentation v{job.result['version']}", 8000)
                self.results.refresh()
            elif job.status == "failed":
                QMessageBox.critical(self, "Revision not saved", job.error)

        job = self.jobs.submit("save_labels", f"Save label revision (scan {scan_id})",
                               lambda ctx: S.save_label_revision(project, scan_id, base, labels, reason, ops, ctx),
                               on_done=done)
        if wait:
            self.jobs.wait()
            QApplication.processEvents()
        return job

    # ================================================================== analysis / reports / review
    def analyze_selected(self, scan_ids=None, config=None, use_saved_roi=None):
        if not self.project:
            return []
        ids = scan_ids or self.tree.selected_scan_ids() or ([self.current_scan_id] if self.current_scan_id else [])
        if not ids:
            QMessageBox.information(self, "Analyse", "Select scans (or a study, group or animal) in the project tree.")
            return []
        if config is None:
            sid = self.tree.current_study_id()
            dm = self.project.store.study(self.project.user, sid).get("defect_model") if sid else "condyle"
            dlg = AnalysisDialog(len(ids), dm or "condyle", self)
            if not dlg.exec():
                return []
            config, use_saved_roi = dlg.config(), dlg.saved_roi.isChecked()
        project = self.project
        out = []
        for scan_id in ids:
            out.append(self.jobs.submit(
                "analyze", f"Analyse scan {scan_id}",
                lambda ctx, s=scan_id: S.analyze_scan(project, s, config, ctx, use_saved_roi is not False),
                on_done=lambda job, s=scan_id: self._analysis_done(job, s)))
        self.d_jobs.raise_()
        return out

    def _analysis_done(self, job, scan_id):
        self.refresh_tree()
        self.results.refresh()
        if job.status == "done" and isinstance(job.result, dict) and job.result.get("status") == "needs_manual_roi":
            self.statusBar().showMessage(f"Scan {scan_id}: ROI not detected - define a manual ROI "
                                         "(Study > Define cylindrical ROI) and re-run.", 12000)
        if scan_id == self.current_scan_id and job.status == "done":
            ed = self.state.editor
            if ed is None or not ed.modified:
                self.open_scan(scan_id)

    def generate_report(self, study_id):
        if not self.project or study_id is None:
            return None
        project, wm = self.project, self.licence.watermark

        def done(job):
            if job.status == "done":
                self.tabs.setCurrentWidget(self.reports)
                self.reports.set_project(project, study_id, wm)
                self.reports.refresh(job.result["report_id"])
            elif job.status == "failed":
                QMessageBox.warning(self, "Report not generated", job.error)
        job = self.jobs.submit("report", f"DefectFill report (study {study_id})",
                               lambda ctx: S.generate_report(project, study_id, wm, ctx), on_done=done)
        self.d_jobs.raise_()
        return job

    def sign(self, object_type, object_id, decision, password=None, meaning=None):
        if not self.project:
            return None
        desc = f"{object_type} {object_id}"
        if password is None:
            dlg = SignDialog(self.project.user, desc, decision, self)
            while dlg.exec():
                try:
                    rid = S.sign_review(self.project, dlg.pw.text(), object_type, object_id, decision,
                                        dlg.meaning.currentText(), dlg.comment.text())
                    break
                except (PermissionError, ValueError, KeyError) as e:
                    dlg.show_error(str(e))
                    dlg.pw.clear()
            else:
                return None
        else:
            rid = S.sign_review(self.project, password, object_type, object_id, decision, meaning or "approved", "")
        if self.timing:
            self.timing.signoff(object_type, object_id, decision)
        self.review.refresh()
        self.reports.refresh()
        self.audit.refresh()
        self.statusBar().showMessage(f"Signature recorded ({decision}).", 6000)
        return rid

    # ================================================================== misc
    def set_blinded(self, on: bool):
        self.blinded_view = bool(on)
        for w in (self.a_blind, self.review.blind):
            w.blockSignals(True)
            w.setChecked(self.blinded_view)
            w.blockSignals(False)
        self.refresh_tree()
        self.results.set_blinded(self.blinded_view)
        self._update_viewer_info()
        if self.project:
            u = self.project.user
            self.project.store.audit.record("ui.blinded_mode", u["id"], u["org_id"], details={"on": self.blinded_view})

    def set_theme(self, name):
        theme.apply_theme(QApplication.instance(), name)
        self.settings.theme = name
        self.workspace.view3d._apply_background()
        self.workspace.view3d.render()
        self.refresh_tree()
        self.update()

    def export_screenshot(self, path=None, what="viewer"):
        if path is None:
            path, _ = QFileDialog.getSaveFileName(self, "Export screenshot", "osteoquant_view.png", "PNG image (*.png)")
            if not path:
                return None
        if what == "3d":
            ok = self.workspace.view3d.screenshot(path)
        elif what == "window":
            ok = self.grab().save(path)
        else:
            img = self.workspace.grid_host.grab().toImage()
            v3 = self.workspace.view3d
            if v3.vtk_widget is not None:      # GL widgets do not grab: paint the VTK frame in
                from PySide6.QtGui import QPainter
                p = QPainter(img)
                p.drawImage(v3.canvas.mapTo(self.workspace.grid_host, v3.canvas.rect().topLeft()), v3.grab_frame())
                p.end()
            ok = img.save(path)
        if ok and self.project:
            u = self.project.user
            self.project.store.audit.record("screenshot.export", u["id"], u["org_id"], "scan", self.current_scan_id,
                                            {"path": str(path)})
        return path if ok else None

    def set_timing(self, on: bool):
        if self.timing is None:
            return
        self.timing.set_enabled(bool(on))
        self.activity.refresh()
        if on and self.current_scan_id is not None:
            self.timing.scan_opened(self.current_scan_id, self.state.scan.get("study_id") if self.state.scan else None)
        self.statusBar().showMessage("Workflow timing " + ("recording (local only)" if on else "off"), 6000)

    def export_timing(self, path=None, study_id=None):
        if self.timing is None:
            return None
        self.timing.flush()
        sid = study_id if study_id is not None else self.tree.current_study_id()
        if path is None:
            path, _ = QFileDialog.getSaveFileName(self, "Export workflow timing", "workflow_timing.csv", "CSV (*.csv)")
            if not path:
                return None
        out = self.timing.export_csv(path, sid)
        self.statusBar().showMessage(f"Workflow timing exported: {out[0]} (+ raw events file)", 8000)
        return out

    def show_licence(self):
        dlg = LicenceDialog(self.licence, self)
        if dlg.exec() == 2 and dlg.new_file:
            st = install_licence(dlg.new_file)
            if st.state == "valid":
                self.licence = st
                QMessageBox.information(self, "Licence installed", st.summary())
            else:
                QMessageBox.warning(self, "Licence not installed", f"The licence file was not accepted: {st.reason}")
            self._update_licence_label()
            self.reports.set_project(self.project, self.tree.current_study_id(), self.licence.watermark)

    def show_about(self):
        AboutDialog(self.licence, self).exec()

    def _tree_action(self, key, node):
        if key == "new_study":
            self.new_study()
        elif key == "import":
            self.import_scans(self.tree.current_study_id())
        elif key == "add_group":
            self.add_group(node.get("id"))
        elif key == "analyze":
            self.analyze_selected()
        elif key == "report":
            self.generate_report(node.get("id"))
        elif key == "open":
            self.open_scan(node["id"])
        elif key == "qc":
            sc = self.project.store.scan(self.project.user, node["id"])
            self.qc.show_qc(sc.get("qc"), self._scan_label(sc))
            self.d_qc.raise_()
        elif key == "show_reason":
            QMessageBox.information(self, "Rejected import", f"{node['name']}\n\n{node.get('reason', '')}")

    def _tree_selection(self):
        nodes = self.tree.selected_nodes()
        if len(nodes) == 1 and nodes[0]["kind"] == "scan" and self.project:
            sc = self.project.store.scan(self.project.user, nodes[0]["id"])
            self.qc.show_qc(sc.get("qc"), self._scan_label(sc))

    def _tab_changed(self, i):
        w = self.tabs.widget(i)
        if w is self.results:
            self.results.refresh()
        elif w is self.audit:
            self.audit.refresh()

    def _job_progress(self, job):
        act = self.jobs.active_jobs()
        if act:
            j = act[0]
            self.s_job.setText(f"{j.title}: {j.message}" + (f"  (+{len(act) - 1} more)" if len(act) > 1 else ""))
            self.s_bar.setValue(int(j.progress * 1000))
            self.s_bar.show()
        else:
            self.s_job.setText("")
            self.s_bar.hide()

    def _job_finished(self, job):
        self._job_progress(job)
        if job.status == "failed":
            self.statusBar().showMessage(f"{job.title} failed: {job.error}", 10000)
        elif job.status == "cancelled":
            self.statusBar().showMessage(f"{job.title} cancelled", 6000)

    def showEvent(self, e):
        super().showEvent(e)
        if not self._docks_sized:
            self._size_docks()

    def _size_docks(self):
        self._docks_sized = True
        self.resizeDocks([self.d_project, self.d_display], [290, 330], Qt.Horizontal)
        self.resizeDocks([self.d_jobs], [250], Qt.Vertical)
        self.resizeDocks([self.d_display, self.d_voxel], [560, 200], Qt.Vertical)

    def closeEvent(self, e):
        if not self.close_project():
            e.ignore()
            return
        self.workspace.view3d.shutdown()
        e.accept()
