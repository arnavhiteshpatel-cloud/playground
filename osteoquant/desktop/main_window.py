"""Main window: start page, project tree, viewer workspace, results, reports, audit, docks."""
from __future__ import annotations

from pathlib import Path

import concurrent.futures

from PySide6.QtCore import QEventLoop, QSize, Qt, QTimer
from PySide6.QtGui import QAction, QActionGroup, QKeySequence
from PySide6.QtWidgets import (QApplication, QDialog, QDockWidget, QFileDialog, QFrame, QGridLayout, QHBoxLayout,
                               QInputDialog, QLabel, QListWidget, QListWidgetItem, QMainWindow, QMenu, QMessageBox,
                               QProgressBar, QScrollArea,
                               QPushButton, QSlider, QStackedWidget, QTabWidget, QVBoxLayout, QWidget)

from .. import __version__
from ..licensing import LicenceStatus, current_status, install_licence
from . import services as S
from . import theme
from .dialogs import (AboutDialog, AnalysisDialog, ChangePasswordDialog, IdleLockDialog, LicenceDialog, LoginDialog,
                      NewProjectDialog, NewStudyDialog, RoiDialog, SaveRevisionDialog, ShortcutsDialog, SignDialog,
                      UnblindDialog, UserAdminDialog)
from .lock import IdleWatcher, LockInputFilter, LockPage
from .messages import friendly, show_error
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


class SliceCell(QWidget):
    """A slice view with a slice slider below it (UX-16)."""

    def __init__(self, view: SliceView, parent=None):
        super().__init__(parent)
        self.view = view
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        lay.addWidget(view, 1)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setFocusPolicy(Qt.StrongFocus)
        self.slider.setToolTip(f"Slice ({['axial', 'coronal', 'sagittal'][view.axis]}); also mouse wheel, Up/Down, "
                               "Page Up/Down, Home/End")
        self.slider.setAccessibleName(f"{['Axial', 'Coronal', 'Sagittal'][view.axis]} slice")
        self.slider.valueChanged.connect(lambda v: view.state.set_index(view.axis, v))
        lay.addWidget(self.slider)
        view.state.scan_changed.connect(self._range)
        view.state.cursor_changed.connect(self._value)
        self._range()

    def _range(self):
        st = self.view.state
        self.slider.blockSignals(True)
        self.slider.setRange(0, max(0, st.shape[self.view.axis] - 1) if st.loaded else 0)
        self.slider.setEnabled(st.loaded)
        self.slider.setValue(st.cursor[self.view.axis] if st.loaded else 0)
        self.slider.blockSignals(False)

    def _value(self, *_):
        self.slider.blockSignals(True)
        self.slider.setValue(self.view.state.cursor[self.view.axis])
        self.slider.blockSignals(False)


class ViewerWorkspace(QWidget):
    """Three linked slice views and the 3D panel in a 2 x 2 grid; double-click maximises."""

    def __init__(self, state: ViewerState, parent=None):
        super().__init__(parent)
        self.state = state
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        top = QHBoxLayout()
        top.setContentsMargins(0, 0, 0, 0)
        top.setSpacing(0)
        self.infobar = QLabel("No scan open. Double-click a scan in the project tree.")
        self.infobar.setProperty("role", "banner-info")
        self.infobar.setWordWrap(True)
        top.addWidget(self.infobar, 1)
        self.chip = QLabel(S.SYNTHETIC_CHIP)
        self.chip.setProperty("role", "chip-bad")
        self.chip.setToolTip("The segmentation shown was produced by a model trained on synthetic phantoms only; "
                             "it is not validated on real tissue. The PDF report carries the same banner.")
        self.chip.hide()
        top.addWidget(self.chip, 0, Qt.AlignVCenter)
        lay.addLayout(top)
        self.grid_host = QWidget()
        self.grid = QGridLayout(self.grid_host)
        self.grid.setContentsMargins(2, 2, 2, 2)
        self.grid.setSpacing(2)
        self.views = [SliceView(state, a) for a in range(3)]
        self.slice_cells = [SliceCell(v) for v in self.views]
        self.view3d = View3D(state)
        self.cells = [self.slice_cells[0], self.view3d, self.slice_cells[1], self.slice_cells[2]]
        for i, w in enumerate(self.cells):
            self.grid.addWidget(w, i // 2, i % 2)
        for v in self.views:
            v.maximize_requested.connect(self.toggle_max)
        lay.addWidget(self.grid_host, 1)
        self._max = None

    def toggle_max(self, axis):
        target = self.slice_cells[axis]
        if self._max is target:
            for w in self.cells:
                w.show()
            self._max = None
        else:
            for w in self.cells:
                w.setVisible(w is target)
            self._max = target

    def set_info(self, text, kind="info", synthetic=False):
        from .panels import set_banner
        set_banner(self.infobar, text, kind)
        self.chip.setVisible(bool(synthetic))


class MainWindow(QMainWindow):
    def __init__(self, settings: AppSettings | None = None, licence: LicenceStatus | None = None):
        super().__init__()
        self.settings = settings or AppSettings()
        self.licence = licence or current_status()
        self.project: Project | None = None
        self.blinded_view = False
        self.current_scan_id = None
        self._dialogs = []
        self._loading = False
        self._locked = False
        self._closing = []          # projects whose store closes once their jobs have stopped
        self._loader = concurrent.futures.ThreadPoolExecutor(max_workers=1, thread_name_prefix="oq-load")
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
        self.lock_page = LockPage()
        self.lock_page.unlock_requested.connect(self.unlock_session)
        self.lock_page.close_requested.connect(self._close_from_lock)
        self.stack.addWidget(self.start)
        self.stack.addWidget(self.tabs)
        self.stack.addWidget(self.lock_page)
        self.setCentralWidget(self.stack)
        self.idle = IdleWatcher(self)
        QApplication.instance().installEventFilter(self.idle)
        self.idle.idle.connect(lambda: self.lock_session(idle=True))
        self._lock_filter = LockInputFilter(self._lock_allows, self)
        self._lock_hidden = []
        # the session is re-validated before every service call; this timer also ends it in the UI when an
        # administrator deactivates the account or resets its password (C2-PRD-07)
        self._session_timer = QTimer(self)
        self._session_timer.timeout.connect(self._check_session)
        self._session_timer.start(5000)

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
        self.btn_import, self.btn_analyse = bi, ba
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
        self.review.roi_edit_requested.connect(self.define_roi)
        self.review.compare_toggled.connect(self.set_compare)
        self.oblique = ObliqueView(self.state)
        self.d_display = self._dock("Display", self.display, Qt.RightDockWidgetArea, scroll=True)
        self.d_voxel = self._dock("Voxel", self.voxel, Qt.RightDockWidgetArea, scroll=True)
        self.splitDockWidget(self.d_display, self.d_voxel, Qt.Vertical)
        self.d_seg = self._dock("Segmentation", self.segpanel, Qt.RightDockWidgetArea)
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
        for key, text, sc, tip in (("navigate", "Navigate", "N", "Move the crosshair (N)"),
                                   ("brush", "Brush", "B", "Paint the active class (B)"),
                                   ("erase", "Eraser", "E", "Erase to background (E)"),
                                   ("grow", "Region grow", "G", "Grow from a seed within a tolerance (G)"),
                                   ("fill", "Fill holes", "H", "Fill enclosed holes of the active class (H)"),
                                   ("measure", "Distance", "M", "Measure a distance: drag in a slice view (M)")):
            a = self._act(text, lambda _=False, k=key: self.state.set_tool(k), sc, checkable=True, tip=tip)
            # tool keys act only while the viewer has focus: they never steal type-ahead in the tree (UX-27)
            a.setShortcutContext(Qt.WidgetWithChildrenShortcut)
            self.workspace.addAction(a)
            self.tool_group.addAction(a)
            e.addAction(a)
            self.tool_actions[key] = a
        self.tool_actions["navigate"].setChecked(True)
        self.state.tool_changed.connect(lambda: self.tool_actions[self.state.tool].setChecked(True))
        self.a_roi_toggle = self._act("Show ROI outline", lambda on: self.display.show_roi.setChecked(on), "R",
                                      checkable=True, tip="Show the analysis ROI outline on the slices and in 3D (R)")
        self.a_roi_toggle.setChecked(True)
        self.a_roi_toggle.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.workspace.addAction(self.a_roi_toggle)
        self.state.overlay_changed.connect(lambda: self.a_roi_toggle.setChecked(self.state.show_roi))
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
        self.a_unblind = self._act("Unblind study...", lambda: self.unblind_study(),
                                   tip="Signed action of the study director or an administrator: reveals allocation "
                                       "of a blinded study to every user")
        for a in (self.a_new_study, self.a_add_group, None, self.a_roi, self.a_analyze, self.a_cancel, None, self.a_report,
                  None, self.a_unblind):
            st.addSeparator() if a is None else st.addAction(a)
        st.setToolTipsVisible(True)
        e.setToolTipsVisible(True)

        pm = mb.addMenu("&Project")
        self.a_users = self._act("Users...", self.manage_users, tip="Add users, set roles, deactivate, reset passwords")
        self.a_idle = self._act("Idle lock...", self.configure_idle_lock, tip="Minutes without input before the window locks")
        self.a_lock = self._act("Lock now", lambda: self.lock_session(), "Ctrl+L")
        self.a_password = self._act("Change my password...", lambda: self.change_password(),
                                    tip="Replace your password (also your electronic-signature password)")
        for a in (self.a_users, self.a_idle, None, self.a_password, self.a_lock):
            pm.addSeparator() if a is None else pm.addAction(a)
        pm.setToolTipsVisible(True)

        v = mb.addMenu("&View")
        self.a_blind = self._act("Blinded review mode", lambda on: self.set_blinded(on), checkable=True)
        v.addAction(self.a_blind)
        v.addAction(self.a_roi_toggle)
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
        self.a_audit_export = self._act("Export audit trail (CSV/JSON)...", lambda: self.audit.export(),
                                        tip="Exports every audit event with the chain-verification result")
        tools.addAction(self.a_audit_export)
        tools.setToolTipsVisible(True)

        h = mb.addMenu("&Help")
        h.addAction(self._act("Keyboard shortcuts", lambda: self._own(ShortcutsDialog(self)).exec(), "F1"))
        h.addAction(self._act("Licence...", self.show_licence))
        h.addAction(self._act("About OsteoQuant Desktop", self.show_about))

        tb = self.addToolBar("Main")
        self.toolbar = tb
        tb.setObjectName("toolbar_main")
        tb.setMovable(False)
        tb.setIconSize(QSize(16, 16))
        tb.setToolButtonStyle(Qt.ToolButtonTextOnly)
        for a in (self.a_open, self.a_import, None, self.a_analyze, self.a_save_rev, None):
            tb.addSeparator() if a is None else tb.addAction(a)
        for k in ("navigate", "brush", "erase", "grow", "fill", "measure"):
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
            cache_txt = f"{cache / 2**20:,.1f} MiB" if cache >= 2**20 else f"{cache / 1024:,.0f} KiB"
            self.s_mem.setText(f"Memory {rss / 2**20:,.0f} MiB  ·  slice cache {cache_txt}  ·  "
                               f"free {avail / 2**30:,.1f} GiB")
        except Exception:  # noqa: BLE001
            self.s_mem.setText("")

    def _update_licence_label(self):
        st = self.licence
        self.s_lic.setText(st.summary() if st.state == "valid" else "Evaluation mode")
        self.s_lic.setToolTip(st.summary())

    def _set_project_ui(self, on: bool):
        self._hidden_viewer_docks = []
        self.stack.setCurrentIndex(1 if on else 0)
        self.tabs.setCurrentWidget(self.workspace)
        for d in (self.d_project, self.d_display, self.d_seg, self.d_review, self.d_oblique, self.d_voxel,
                  self.d_jobs, self.d_qc):
            d.setVisible(on)
        for a in (self.a_close, self.a_import, self.a_new_study, self.a_add_group, self.a_roi, self.a_analyze,
                  self.a_report, self.a_save_rev, self.a_shot, self.a_timing, self.a_timing_export, self.a_users,
                  self.a_idle, self.a_lock, self.a_audit_export, self.a_password, self.a_unblind,
                  *self.tool_actions.values()):
            a.setEnabled(on)
        self.d_oblique.hide()
        if on:
            self.d_display.raise_()
            self.d_qc.raise_()
            QTimer.singleShot(0, self._size_docks)
            self.apply_role_gating()
        self._update_title()

    # Actions that need a permission the signed-in role may lack, with their normal tooltips.
    def _gated(self):
        return {"write": [(self.a_import, "Import scans"), (self.a_new_study, "New study"),
                          (self.a_add_group, "Add group"), (self.a_roi, "Define a manual ROI at the crosshair"),
                          (self.a_analyze, "Analyse selected scans"), (self.a_save_rev, "Save label revision"),
                          (self.tool_actions["brush"], "Paint the active class (B)"),
                          (self.tool_actions["erase"], "Erase to background (E)"),
                          (self.tool_actions["grow"], "Grow from a seed within a tolerance (G)"),
                          (self.tool_actions["fill"], "Fill enclosed holes of the active class (H)"),
                          (self.btn_import, "Import scans into the selected study"),
                          (self.btn_analyse, "Analyse the selected scans")],
                "manage_users": [(self.a_users, "Add users, set roles, deactivate, reset passwords"),
                                 (self.a_idle, "Minutes without input before the window locks")],
                "unblind": [(self.a_unblind, "Signed action of the study director or an administrator: reveals "
                                             "allocation of a blinded study to every user")]}

    def apply_role_gating(self):
        """Disable what the signed-in role cannot do, with a tooltip that says why (UX-10)."""
        p = self.project
        if not p or not p.user:
            return
        self._gated_role = p.user["role"]
        for perm, items in self._gated().items():
            why = p.why_not(perm)
            for w, tip in items:
                w.setEnabled(not why)
                w.setToolTip(why or tip)
                if isinstance(w, QAction):
                    w.setStatusTip(why or tip)
        allowed_audit = p.can("review") or p.can("manage_users")
        self.a_audit_export.setEnabled(allowed_audit)
        self.a_audit_export.setToolTip("" if allowed_audit else "Requires the reviewer, study director or administrator role")
        self.state.set_read_only(p.why_not("write"))
        self.apply_blinding_policy()

    def apply_blinding_policy(self):
        """Study-level blinding (C2-PRD-03): while a study of the project is blinded, users who may not
        unblind stay in blinded review mode and cannot switch it off."""
        p = self.project
        forced = bool(p and p.user and p.blinding_forced())
        tip = ("A study in this project is blinded: blinded review mode stays on for your role. Only the study "
               "director or an administrator can unblind the study (Study > Unblind study, signed)." if forced else
               "Hide group names, animal IDs, file names and acquisition metadata in every view, including the audit "
               "trail and report preview; random codes replace IDs")
        for w in (self.a_blind, self.review.blind):
            w.setEnabled(not forced)
            w.setToolTip(tip)
        self.a_blind.setStatusTip(tip)
        self.reports.blinding_forced = forced
        if forced and not self.blinded_view:
            self.set_blinded(True)

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
        dlg = self._own(NewProjectDialog(self))
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
            dlg = self._own(LoginDialog(p.name, self.settings.last_user(folder), self))
            while True:
                if not dlg.exec():
                    p.close()
                    return False
                if p.login(dlg.user.text().strip(), dlg.pw.text()):
                    break
                dlg.show_error("Sign-in failed: wrong user name or password, inactive or temporarily locked account.")
                dlg.pw.clear()
            self.settings.set_last_user(folder, p.user["username"])
            # a password set by an administrator is replaced by its owner before work starts (C2-PRD-08)
            if p.password_change_required and not self._forced_password_change(p):
                p.close()
                return False
        self._after_open(p)
        return True

    def _forced_password_change(self, p: Project) -> bool:
        dlg = self._own(ChangePasswordDialog(p.user["username"], self, required=True))
        while dlg.exec():
            try:
                p.change_password(dlg.old.text(), dlg.pw1.text())
                return True
            except (PermissionError, ValueError) as e:
                dlg.show_error(str(e))
        return False

    def change_password(self, old=None, new=None) -> bool:
        if not self.project:
            return False
        if old is None:
            dlg = self._own(ChangePasswordDialog(self.project.user["username"], self))
            while dlg.exec():
                try:
                    self.project.change_password(dlg.old.text(), dlg.pw1.text())
                    break
                except (PermissionError, ValueError) as e:
                    dlg.show_error(str(e))
            else:
                return False
        else:
            self.project.change_password(old, new)
        self.statusBar().showMessage("Password changed.", 6000)
        return True

    def unblind_study(self, study_id=None, password=None, reason=None) -> bool:
        """Signed unblinding by a study director or administrator (C2-PRD-03)."""
        p = self.project
        if not p or self._denied("unblind", "Unblind study"):
            return False
        studies = p.blinded_studies()
        if not studies:
            QMessageBox.information(self, "Unblind study", "No study of this project is blinded.")
            return False
        if password is None:
            dlg = self._own(UnblindDialog(studies, p.user, self))
            while dlg.exec():
                try:
                    S.unblind_study(p, dlg.pw.text(), dlg.study.currentData(), dlg.reason.text())
                    break
                except (PermissionError, ValueError, KeyError) as e:
                    dlg.show_error(friendly(e))
                    dlg.pw.clear()
            else:
                return False
        else:
            S.unblind_study(p, password, study_id, reason or "")
        self.apply_blinding_policy()
        self.refresh_tree()
        self.results.refresh()
        self.reports.refresh()
        self.statusBar().showMessage("Study unblinded (signature recorded).", 8000)
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
        self.results.watermark = self.licence.watermark
        self.results.set_project(p, sid)
        self.reports.set_project(p, sid, self.licence.watermark)
        self.audit.set_project(p)
        self.review.set_scan(p, None)
        self.idle.set_timeout_minutes(p.idle_lock_minutes)
        self.workspace.set_info(f"Project {p.name} opened. Double-click a scan in the project tree to view it.")
        self.statusBar().showMessage(f"Signed in as {p.user['username']}", 5000)

    CLOSE_WAIT_MS = 3000

    def close_project(self, ask: bool = True, discard: bool = False) -> bool:
        if self.project is None:
            return True
        if self._loading:
            return False
        if discard and self.state.editor is not None:
            self.state.history.clear()
            self.state.editor.base_counts = dict(self.state.editor.counts)
        if not self._locked and not self._confirm_discard_edits():
            return False
        if self.jobs.active_jobs():
            if ask and QMessageBox.question(self, "Jobs running", "Background jobs are running. Cancel them and close?") \
                    != QMessageBox.Yes:
                return False
            # cancel, then wait at most 3 s; a library stage that is still running finishes in the
            # background and the project's database is closed once the pool is idle (UX-26)
            self.jobs.cancel_all()
            self.jobs.wait(self.CLOSE_WAIT_MS)
        self.state.unload()
        self.current_scan_id = None
        self.activity.set_recorder(None)
        self.timing = None
        p = self.project
        self.project = None
        if self.jobs.active_jobs():
            self._closing.append(p)
            QTimer.singleShot(500, self._finish_deferred_close)
            self.statusBar().showMessage("Waiting for a cancelled job to stop; the project closes when it has.", 8000)
        else:
            p.close()
        self.jobs.set_project(None)
        self.jobs_panel.clear_finished()
        self.tree.clear()
        self._unlock_ui()
        self._set_project_ui(False)
        self.start.refresh()
        return True

    def _finish_deferred_close(self):
        if self.jobs.active_jobs():
            QTimer.singleShot(500, self._finish_deferred_close)
            return
        while self._closing:
            self._closing.pop().close()

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
        if not self.project or self._denied("write", "New study"):
            return None
        dlg = self._own(NewStudyDialog(self))
        if dlg.exec():
            try:
                sid = self.project.create_study(**dlg.values())
            except PermissionError as e:
                QMessageBox.warning(self, "Not permitted", str(e))
                return None
            self.apply_blinding_policy()
            self.refresh_tree()
            self.results.set_project(self.project, sid)
            self.reports.set_project(self.project, sid, self.licence.watermark)
            return sid
        return None

    def add_group(self, study_id=None):
        sid = study_id or self.tree.current_study_id()
        if not self.project or sid is None or self._denied("write", "Add group"):
            return
        name, ok = QInputDialog.getText(self, "Add group", "Group name (e.g. treatment arm):")
        if ok and name.strip():
            try:
                self.project.store.add_group(self.project.require_user(), sid, name.strip())
            except PermissionError as e:
                QMessageBox.warning(self, "Not permitted", str(e))
            self.refresh_tree()

    def _denied(self, perm: str, title: str) -> bool:
        """Explain (instead of failing later) when the signed-in role lacks ``perm``."""
        if self.project and not self.project.can(perm):
            QMessageBox.information(self, title, self.project.why_not(perm))
            return True
        return False

    def import_scans(self, study_id=None, paths=()):
        if not self.project or self._denied("write", "Import scans"):
            return None
        if not self.project.store.list_studies(self.project.user):
            if self.new_study() is None:
                return None
        self._purge_dialogs()
        wiz = ImportWizard(self.project, self.jobs, study_id or self.tree.current_study_id(), self, paths)
        wiz.setAttribute(Qt.WA_DeleteOnClose)
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

    def _run_in_thread(self, fn):
        """Run ``fn`` on the loader thread while the GUI keeps repainting and processing jobs and
        timers (user input is held back until the result is in, so nothing re-enters)."""
        fut = self._loader.submit(fn)
        if not fut.done():
            loop = QEventLoop()
            t = QTimer()
            t.setInterval(10)
            t.timeout.connect(lambda: fut.done() and loop.quit())
            t.start()
            if not fut.done():
                loop.exec(QEventLoop.ExcludeUserInputEvents)
            t.stop()
        return fut.result()

    def open_scan(self, scan_id, segmentation_id=None, keep_view=False):
        if not self.project or scan_id is None or self._loading:
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
        # label volumes (1-8 GB for large scans) are read on a worker thread, not the GUI thread (UX-25)
        self._loading = True
        self.statusBar().showMessage("Loading labels and ROI...")
        QApplication.setOverrideCursor(Qt.BusyCursor)
        try:
            layers = self._run_in_thread(lambda: S.load_scan_layers(sc["store_path"], seg))
        except Exception as e:  # noqa: BLE001
            show_error(self, "Scan not opened", e)
            return False
        finally:
            QApplication.restoreOverrideCursor()
            self._loading = False
        same = keep_view and scan_id == self.current_scan_id
        self.current_scan_id = scan_id
        self.state.load(src, layers["labels"], sc, seg, roi=layers["roi"], keep_view=same)
        self.display.set_segmentations(segs, seg["id"] if seg else None)
        self.display._on_scan()
        self.qc.show_qc(sc.get("qc"), self._scan_label(sc))
        self.review.set_scan(p, scan_id)
        if seg:
            self.review.refresh(seg["id"])
        self.tree.select_scan(scan_id)
        self.tabs.setCurrentWidget(self.workspace)
        self._update_viewer_info()
        self.statusBar().clearMessage()
        p.store.audit.record("scan.view", p.user["id"], p.user["org_id"], "scan", scan_id, {"client": "desktop"})
        if self.timing:
            self.timing.scan_opened(scan_id, sc["study_id"])
        self._update_title()
        return True

    def set_compare(self, on: bool):
        """Highlight voxels changed between the selected version and its parent (UX-06)."""
        st = self.state
        if not on:
            st.set_compare(None)
            return
        sel = self.review.selected_segmentation()
        if not sel or not sel.get("parent_id") or self.current_scan_id is None:
            return
        if not st.segmentation or st.segmentation["id"] != sel["id"]:
            if not self.open_scan(self.current_scan_id, sel["id"], keep_view=True):
                return
            self.review.compare.blockSignals(True)
            self.review.compare.setChecked(True)
            self.review.compare.blockSignals(False)
        parent = self.project.store.q1("SELECT version, labels_key FROM segmentations WHERE id=?", (sel["parent_id"],))
        sc = st.scan
        layers = self._run_in_thread(lambda: S.load_scan_layers(sc["store_path"], None, parent["labels_key"]))
        st.set_compare(layers["parent"], f"changed vs v{parent['version']}")
        n = int(st.compare_mask.sum()) if st.compare_mask is not None else 0
        self.statusBar().showMessage(f"{n:,} voxels differ from v{parent['version']} (magenta)", 8000)

    def _scan_label(self, sc) -> str:
        if self.blinded_view and self.project:
            return self.project.scan_code(sc["id"], sc.get("study_id"))
        return f"Scan {sc['id']} - {sc['source_name']}"

    def _update_viewer_info(self):
        st = self.state
        if not st.loaded:
            self.workspace.set_info("No scan open. Double-click a scan in the project tree.")
            return
        sc, seg = st.scan, st.segmentation
        sh = " x ".join(map(str, st.shape))
        sp = ", ".join(f"{s:g}" for s in st.spacing)
        meth = S.segmentation_method_info(seg) if seg else {"short": "", "synthetic": False}
        segtxt = (f"segmentation v{seg['version']} ({seg['kind']}, {meth['short']})" if seg
                  else "no segmentation yet - run the analysis to create one, then edit it")
        roitxt = ""
        if seg and self.project:
            rs = S.roi_state(self.project, seg.get("roi_id"))
            if rs["roi"] is not None:
                roitxt = f"   ·   ROI {rs['status']}"
        ro = "   ·   READ ONLY" if st.read_only_reason and seg else ""
        kind = "info" if seg else "warn"
        if seg and "awaiting" in roitxt:
            kind = "warn"
        self.workspace.set_info(f"{self._scan_label(sc)}   ·   {sh} voxels   ·   {sp} µm   ·   {segtxt}{roitxt}{ro}",
                                kind, synthetic=meth["synthetic"])

    def define_roi(self):
        if self.project and not self.project.can("write"):
            QMessageBox.information(self, "Define ROI", self.project.why_not("write"))
            return
        if not self.state.loaded or self.current_scan_id is None:
            QMessageBox.information(self, "Define ROI", "Open a scan and place the crosshair at the defect centre first.")
            return
        dlg = self._own(RoiDialog(self.state.cursor, self.state.spacing, self))
        if dlg.exec():
            try:
                rid = S.save_cylinder_roi(self.project, self.current_scan_id, self.state.cursor, dlg.radius.value(),
                                          (dlg.depth0.value(), dlg.depth1.value()), reason=dlg.reason.text().strip())
                self.statusBar().showMessage(f"ROI {rid} saved. Run the analysis to use it.", 8000)
                if QMessageBox.question(self, "ROI saved", "The new ROI is used by the next analysis of this scan. "
                                        "Re-analyse the scan now?") == QMessageBox.Yes:
                    self.analyze_selected([self.current_scan_id])
            except (PermissionError, ValueError) as e:
                show_error(self, "ROI not saved", e)

    def save_revision(self, reason: str | None = None, wait: bool = False):
        st = self.state
        if st.editor is None or not st.editor.modified or self.current_scan_id is None:
            return None
        if reason is None:
            import numpy as _np
            dlg = self._own(SaveRevisionDialog(st.editor.change_summary(), st.segmentation["version"], self,
                                               float(_np.prod(st.spacing)) / 1e9))
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
                # same scan: keep crosshair, window/level and zoom (UX-19)
                self.open_scan(scan_id, job.result["segmentation_id"], keep_view=True)
                self.statusBar().showMessage(f"Saved segmentation v{job.result['version']}", 8000)
                self.results.refresh()
            elif job.status == "failed":
                show_error(self, "Revision not saved", job.error, QMessageBox.Critical)

        job = self.jobs.submit("save_labels", f"Save label revision ({self._job_scan(scan_id)})",
                               lambda ctx: S.save_label_revision(project, scan_id, base, labels, reason, ops, ctx),
                               on_done=done)
        if wait:
            self.jobs.wait()
            QApplication.processEvents()
        return job

    # ================================================================== analysis / reports / review
    def analyze_selected(self, scan_ids=None, config=None, use_saved_roi=None):
        if not self.project or self._denied("write", "Analyse"):
            return []
        ids = scan_ids or self.tree.selected_scan_ids() or ([self.current_scan_id] if self.current_scan_id else [])
        if not ids:
            QMessageBox.information(self, "Analyse", "Select scans (or a study, group or animal) in the project tree.")
            return []
        if config is None:
            sid = self.tree.current_study_id()
            st_ = self.project.store.study(self.project.user, sid) if sid else {}
            dm = st_.get("defect_model") if sid else "condyle"
            dlg = self._own(AnalysisDialog(len(ids), dm or "condyle", self,
                                           study_materials=str(st_.get("graft_materials") or "")))
            if not dlg.exec():
                return []
            config, use_saved_roi = dlg.config(), dlg.saved_roi.isChecked()
        project = self.project
        out = []
        for scan_id in ids:
            out.append(self.jobs.submit(
                "analyze", f"Analyse {self._job_scan(scan_id)}",
                lambda ctx, s=scan_id: S.analyze_scan(project, s, config, ctx, use_saved_roi is not False),
                on_done=lambda job, s=scan_id: self._analysis_done(job, s)))
        self.d_jobs.raise_()
        return out

    def _job_scan(self, scan_id) -> str:
        """Scan reference for job titles (shown in the Jobs panel and audited): the blinded code in blinded
        mode, never the database ID (C2-PRD-14)."""
        if self.project and (self.blinded_view or self.project.blinding_forced()):
            return self.project.scan_code(scan_id)
        return f"scan {scan_id}"

    def _analysis_done(self, job, scan_id):
        self.refresh_tree()
        self.results.refresh()
        if job.status == "done" and isinstance(job.result, dict) and job.result.get("status") == "needs_manual_roi":
            self.statusBar().showMessage(f"Scan {scan_id}: ROI not detected - define a manual ROI "
                                         "(Study > Define cylindrical ROI) and re-run.", 12000)
        if scan_id == self.current_scan_id and job.status == "done":
            ed = self.state.editor
            if ed is None or not ed.modified:
                self.open_scan(scan_id, keep_view=True)

    def generate_report(self, study_id):
        if not self.project or study_id is None:
            return None
        project, wm, blinded = self.project, self.licence.watermark, self.blinded_view
        if not S.study_has_analysis(project, study_id):
            QMessageBox.information(self, "Report", friendly("ValueError: This study has no analysed scans yet"))
            return None
        busy = [j for j in self.jobs.active_jobs() if j.kind in ("analyze", "save_labels", "import")]
        if busy:      # a report is a snapshot of finished work (C2-PRD-01)
            QMessageBox.information(self, "Report", f"{len(busy)} analysis, import or save job(s) are still running. "
                                                    "Generate the report when they have finished.")
            return None

        def done(job):
            if job.status == "done":
                self.tabs.setCurrentWidget(self.reports)
                self.reports.set_project(project, study_id, wm)
                self.reports.refresh(job.result["report_id"])
            elif job.status == "failed":
                show_error(self, "Report not generated", job.error)
        blinded = bool(blinded or project.study_forces_blinding(study_id))
        job = self.jobs.submit("report", f"Defect-fill report (study {study_id})" + (", blinded" if blinded else ""),
                               lambda ctx: S.generate_report(project, study_id, wm, ctx, blinded=blinded), on_done=done)
        self.d_jobs.raise_()
        return job

    def _object_desc(self, object_type, object_id) -> str:
        p = self.project
        if object_type == "segmentation":
            seg = p.store.q1("SELECT scan_id, version FROM segmentations WHERE id=?", (object_id,))
            if seg:
                sc = p.store.scan(p.user, seg["scan_id"])
                return f"segmentation v{seg['version']} of {self._scan_label(sc)}"
        if object_type == "roi":
            r = p.store.q1("SELECT scan_id, version FROM rois WHERE id=?", (object_id,))
            if r:
                sc = p.store.scan(p.user, r["scan_id"])
                return f"analysis ROI v{r['version']} of {self._scan_label(sc)}"
        if object_type == "report":
            return f"report {object_id}"
        return f"{object_type} {object_id}"

    def sign(self, object_type, object_id, decision, password=None, meaning=None, signature_role=None):
        if not self.project:
            return None
        desc = self._object_desc(object_type, object_id)
        roles = S.signature_roles_for(self.project.user) if object_type == "report" else []
        if password is None:
            dlg = self._own(SignDialog(self.project.user, desc, decision, self, object_type, roles))
            while dlg.exec():
                try:
                    rid = S.sign_review(self.project, dlg.pw.text(), object_type, object_id, decision,
                                        dlg.meaning.currentText(), dlg.comment.text(),
                                        dlg.role.currentData() if dlg.role.count() else None)
                    break
                except (PermissionError, ValueError, KeyError) as e:
                    dlg.show_error(friendly(e))
                    dlg.pw.clear()
            else:
                return None
        else:
            rid = S.sign_review(self.project, password, object_type, object_id, decision, meaning or "approved", "",
                                signature_role)
        if self.timing:
            self.timing.signoff(object_type, object_id, decision)
        self.review.refresh()
        self.reports.refresh(object_id if object_type == "report" else None)
        self.audit.refresh()
        self.results.refresh()
        self._update_viewer_info()
        self.statusBar().showMessage(f"Signature recorded ({decision.replace('_', ' ')}).", 6000)
        return rid

    # ================================================================== misc
    def set_blinded(self, on: bool):
        if not on and self.project and self.project.blinding_forced():
            # reviewers cannot switch study-level blinding off (C2-PRD-03)
            u = self.project.user
            self.project.store.audit.record("ui.blinded_mode_denied", u["id"], u["org_id"], details={"on": False})
            self.statusBar().showMessage("Blinded review mode stays on: a study is blinded and your role cannot "
                                         "unblind it.", 8000)
            on = True
            if self.blinded_view:
                for w in (self.a_blind, self.review.blind):
                    w.blockSignals(True)
                    w.setChecked(True)
                    w.blockSignals(False)
                return
        self.blinded_view = bool(on)
        for w in (self.a_blind, self.review.blind):
            w.blockSignals(True)
            w.setChecked(self.blinded_view)
            w.blockSignals(False)
        self.refresh_tree()
        self.results.set_blinded(self.blinded_view)
        self.review.set_blinded(self.blinded_view)
        self.audit.set_blinded(self.blinded_view)
        self.reports.set_blinded(self.blinded_view)
        self._update_viewer_info()
        if self.state.scan:
            self.qc.show_qc(self.state.scan.get("qc"), self._scan_label(self.state.scan))
        if self.project:
            u = self.project.user
            self.project.store.audit.record("ui.blinded_mode", u["id"], u["org_id"], details={"on": self.blinded_view})

    def _own(self, dlg):
        """Track a modal dialog so it is destroyed once closed (closed-but-alive dialogs would be
        re-polished on every theme change)."""
        self._purge_dialogs()
        self._dialogs.append(dlg)
        return dlg

    def _purge_dialogs(self):
        from PySide6.QtCore import QCoreApplication, QEvent
        keep = []
        for d in getattr(self, "_dialogs", []):
            try:
                if d.isVisible():
                    keep.append(d)
                else:
                    d.deleteLater()
            except RuntimeError:      # already deleted
                pass
        self._dialogs = keep
        QCoreApplication.sendPostedEvents(None, QEvent.DeferredDelete)

    def set_theme(self, name):
        self._purge_dialogs()
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
        dlg = self._own(LicenceDialog(self.licence, self))
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
        self._own(AboutDialog(self.licence, self)).exec()

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
        viewer_docks = [self.d_display, self.d_seg, self.d_review, self.d_oblique, self.d_voxel, self.d_qc]
        if self.project is not None:
            if w is self.workspace:
                for d in getattr(self, "_hidden_viewer_docks", []):
                    d.show()
                self._hidden_viewer_docks = []
            elif not getattr(self, "_hidden_viewer_docks", []):
                self._hidden_viewer_docks = [d for d in viewer_docks if d.toggleViewAction().isChecked()]
                for d in self._hidden_viewer_docks:
                    d.hide()
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

    # ================================================================== users, idle lock
    def manage_users(self):
        if not self.project or not self.project.can("manage_users"):
            return None
        dlg = self._own(UserAdminDialog(self.project, self))
        dlg.exec()
        self.review.refresh()
        return dlg

    def configure_idle_lock(self, minutes=None):
        if not self.project or not self.project.can("manage_users"):
            return
        if minutes is None:
            dlg = self._own(IdleLockDialog(self.project.idle_lock_minutes, self))
            if not dlg.exec():
                return
            minutes = dlg.minutes.value()
        self.project.set_idle_lock_minutes(int(minutes))
        self.idle.set_timeout_minutes(self.project.idle_lock_minutes)
        self.statusBar().showMessage(f"Idle lock: {minutes} min" if minutes else "Idle lock off", 6000)

    def _check_session(self):
        """End the project in the UI once its session has ended (deactivated account, password reset)."""
        p = self.project
        if p is None or p.user is None and p.session_end_reason is None:
            return
        if p.user is not None and p.check_session():
            if not self._locked:
                if p.user["role"] != getattr(self, "_gated_role", None):
                    self.apply_role_gating()     # a role change takes effect at once
                else:
                    self.apply_blinding_policy()   # a study blinded or unblinded in another session
            return
        reason = p.session_end_reason or "the session has ended"
        self._unlock_ui()
        self.jobs.cancel_all()
        self.close_project(ask=False, discard=True)
        QMessageBox.warning(self, "Signed out", f"You were signed out: {reason}. Unsaved label edits were discarded.")

    def _lock_allows(self, w) -> bool:
        """Widgets that may receive input while locked: the lock page and confirmation boxes it opens."""
        win = w.window()
        if win is self:
            return w is self.lock_page or self.lock_page.isAncestorOf(w)
        return isinstance(win, QMessageBox) and win not in self._lock_hidden

    def _lock_other_windows(self):
        """Close or hide every other window so that nothing stays usable over the lock (C2-PRD-02)."""
        self._lock_hidden = []
        for w in QApplication.topLevelWidgets():
            if w is self or isinstance(w, QDockWidget) or not w.isVisible():
                continue
            if isinstance(w, QDialog) and w.windowModality() == Qt.ApplicationModal:
                w.reject()          # a dialog running its own event loop (exec) is cancelled
                if w.isVisible():
                    w.hide()
                continue
            w.hide()
            if not isinstance(w, QMenu):
                self._lock_hidden.append(w)

    def lock_session(self, idle: bool = False):
        """Hide the project and require the signed-in user's password (idle lock, Ctrl+L). The lock is
        application-wide: other windows and dialogs are closed or hidden and input to them is blocked."""
        if self.project is None or self._locked:
            return
        self._locked = True
        self.idle.paused = True
        self._lock_restore = {"index": self.stack.currentIndex(),
                              "docks": [d for d in self.findChildren(QDockWidget) if d.isVisible()]}
        for d in self._lock_restore["docks"]:
            d.hide()
        self._lock_other_windows()
        QApplication.instance().installEventFilter(self._lock_filter)
        for a in self.menuBar().actions():
            a.setEnabled(False)
        self.toolbar.setEnabled(False)
        u = self.project.user
        self.lock_page.prepare(u, self.project.name, self.project.idle_lock_minutes, idle)
        self.stack.setCurrentWidget(self.lock_page)
        self.project.store.audit.record("session.lock", u["id"], u["org_id"], details={
            "reason": "idle" if idle else "manual", "idle_minutes": self.project.idle_lock_minutes})

    def unlock_session(self, password: str) -> bool:
        if not self._locked or self.project is None:
            return False
        p = self.project
        if not p.check_session():          # deactivated or reset meanwhile: say so, then sign out (C2-PRD-07)
            self.lock_page.show_error(f"Session ended: {p.session_end_reason}.")
            QTimer.singleShot(0, self._check_session)
            return False
        if not p.store.reauthenticate(p.user, password):      # lockout policy applies
            u = p.store.q1("SELECT locked_until FROM users WHERE id=?", (p.user["id"],)) or {}
            import time as _t
            locked = (u.get("locked_until") or 0) > _t.time()
            self.lock_page.show_error("Account temporarily locked after repeated wrong passwords. Try again later "
                                      "or close the project." if locked else "Wrong password.")
            p.store.audit.record("session.unlock_failed", p.user["id"], p.user["org_id"], details={"locked": locked})
            return False
        p.store.audit.record("session.unlock", p.user["id"], p.user["org_id"])
        self._unlock_ui()
        return True

    def _unlock_ui(self):
        if not self._locked:
            return
        self._locked = False
        QApplication.instance().removeEventFilter(self._lock_filter)
        self.idle.paused = False
        self.idle.last_input = self.idle.clock()
        for a in self.menuBar().actions():
            a.setEnabled(True)
        self.toolbar.setEnabled(True)
        rs = getattr(self, "_lock_restore", {})
        self.stack.setCurrentIndex(rs.get("index", 1))
        if self.project is not None:
            for d in rs.get("docks", []):
                d.show()
            import shiboken6
            for w in self._lock_hidden:
                if shiboken6.isValid(w) and not w.isVisible():
                    w.show()
        self._lock_hidden = []

    def _close_from_lock(self):
        # unsaved edits cannot be confirmed without unlocking: they are discarded (the lock page says so)
        if self.state.editor is not None and self.state.editor.modified:
            if QMessageBox.question(self, "Close project", "Unsaved label edits will be discarded. Close the project?") \
                    != QMessageBox.Yes:
                return
            self.state.history.clear()
            self.state.editor.base_counts = dict(self.state.editor.counts)
        self.close_project()

    def closeEvent(self, e):
        if self._loading:
            e.ignore()
            QTimer.singleShot(200, self.close)
            return
        if not self.close_project():
            e.ignore()
            return
        self.workspace.view3d.shutdown()
        self._loader.shutdown(wait=False)
        e.accept()
