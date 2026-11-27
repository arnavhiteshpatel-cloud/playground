"""Reports: generate the DefectFill report for a study, preview it page by page, export, sign."""
from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QPointF, Qt, Signal
from PySide6.QtWidgets import (QComboBox, QFileDialog, QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
                               QMessageBox, QPushButton, QSplitter, QVBoxLayout, QWidget)

from .panels import muted, section

try:
    from PySide6.QtPdf import QPdfDocument
    from PySide6.QtPdfWidgets import QPdfView
    HAVE_QTPDF = True
except ImportError:      # pragma: no cover - QtPdf is part of PySide6 Addons
    HAVE_QTPDF = False


class PdfPreview(QWidget):
    """Single-page PDF preview with page navigation and zoom."""

    def __init__(self, parent=None):
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        bar = QHBoxLayout()
        self.prev, self.next = QPushButton("Previous"), QPushButton("Next")
        self.page_lbl = QLabel("")
        self.zoom = QComboBox()
        self.zoom.addItems(["Fit width", "Fit page", "100 %", "150 %"])
        self.zoom.currentIndexChanged.connect(self._zoom)
        bar.addWidget(self.prev)
        bar.addWidget(self.next)
        bar.addWidget(self.page_lbl)
        bar.addStretch(1)
        bar.addWidget(self.zoom)
        lay.addLayout(bar)
        if HAVE_QTPDF:
            self.doc = QPdfDocument(self)
            self.view = QPdfView(self)
            self.view.setDocument(self.doc)
            self.view.setPageMode(QPdfView.PageMode.SinglePage)
            self.view.setZoomMode(QPdfView.ZoomMode.FitToWidth)
            self.view.setPageSpacing(12)
            self.nav = self.view.pageNavigator()
            self.nav.currentPageChanged.connect(lambda *_: self._label())
            self.prev.clicked.connect(lambda: self.go(self.nav.currentPage() - 1))
            self.next.clicked.connect(lambda: self.go(self.nav.currentPage() + 1))
            lay.addWidget(self.view, 1)
        else:
            self.doc = None
            lay.addWidget(muted("PDF preview requires the QtPdf module; use Export to open the report externally."))
        self._label()

    def load(self, path: str | None):
        if self.doc is None:
            return 0
        self.doc.close()
        if path and Path(path).exists():
            self.doc.load(str(path))
        self.go(0)
        return self.page_count()

    def page_count(self) -> int:
        return self.doc.pageCount() if self.doc is not None else 0

    def go(self, page: int):
        if self.doc is None or self.page_count() == 0:
            self._label()
            return
        page = max(0, min(self.page_count() - 1, page))
        self.nav.jump(page, QPointF(), self.nav.currentZoom())
        self._label()

    def current_page(self) -> int:
        return self.nav.currentPage() if self.doc is not None else 0

    def _zoom(self, i):
        if self.doc is None:
            return
        if i == 0:
            self.view.setZoomMode(QPdfView.ZoomMode.FitToWidth)
        elif i == 1:
            self.view.setZoomMode(QPdfView.ZoomMode.FitInView)
        else:
            self.view.setZoomMode(QPdfView.ZoomMode.Custom)
            self.view.setZoomFactor(1.0 if i == 2 else 1.5)

    def _label(self):
        n = self.page_count()
        cur = self.current_page() + 1 if n else 0
        self.page_lbl.setText(f"Page {cur} of {n}" if n else "No report selected")
        self.prev.setEnabled(n > 0 and cur > 1)
        self.next.setEnabled(n > 0 and cur < n)


class ReportsView(QWidget):
    generate_requested = Signal(int)
    sign_requested = Signal(int, str)       # report id, decision

    def __init__(self, parent=None):
        super().__init__(parent)
        self.project = None
        lay = QHBoxLayout(self)
        lay.setContentsMargins(10, 8, 10, 8)
        split = QSplitter(Qt.Horizontal)
        left = QWidget()
        ll = QVBoxLayout(left)
        ll.setContentsMargins(0, 0, 8, 0)
        t = QLabel("Reports")
        t.setProperty("role", "heading")
        ll.addWidget(t)
        ll.addWidget(QLabel("Study"))
        self.study = QComboBox()
        self.study.currentIndexChanged.connect(self.refresh)
        ll.addWidget(self.study)
        self.gen = QPushButton("Generate DefectFill report")
        self.gen.setProperty("role", "primary")
        self.gen.clicked.connect(lambda: self.study.currentData() is not None
                                 and self.generate_requested.emit(self.study.currentData()))
        ll.addWidget(self.gen)
        self.watermark_note = muted("")
        ll.addWidget(self.watermark_note)
        ll.addWidget(section("Generated reports"))
        self.list = QListWidget()
        self.list.currentItemChanged.connect(self._selected)
        ll.addWidget(self.list, 1)
        self.info = muted("")
        ll.addWidget(self.info)
        row = QHBoxLayout()
        self.export = QPushButton("Export...")
        self.export.clicked.connect(self._export)
        self.approve = QPushButton("Approve...")
        self.approve.clicked.connect(lambda: self._sign("approved"))
        row.addWidget(self.export)
        row.addWidget(self.approve)
        ll.addLayout(row)
        split.addWidget(left)
        self.preview = PdfPreview()
        split.addWidget(self.preview)
        split.setSizes([280, 900])
        lay.addWidget(split)

    def set_project(self, project, study_id=None, watermark=None):
        self.project = project
        self.study.blockSignals(True)
        self.study.clear()
        if project and project.user:
            for s in project.store.list_studies(project.user):
                self.study.addItem(s["name"], s["id"])
                if s["id"] == study_id:
                    self.study.setCurrentIndex(self.study.count() - 1)
        self.study.blockSignals(False)
        self.watermark_note.setText(f"Reports from this installation carry the watermark '{watermark}'."
                                    if watermark else "Licensed: reports are produced without watermark.")
        self.refresh()

    def refresh(self, select_id=None):
        from .services import list_reports
        self.list.clear()
        sid = self.study.currentData()
        if not self.project or sid is None:
            self.preview.load(None)
            return
        for r in list_reports(self.project, sid):
            revs = self.project.store.reviews(self.project.user, "report", r["id"])
            sig = f"  ·  {revs[-1]['decision']} by {revs[-1]['username']}" if revs else ""
            it = QListWidgetItem(f"Report {r['id']}  ·  {r['created']}  ·  {r['status']}{sig}")
            it.setData(Qt.UserRole, r)
            self.list.addItem(it)
            if select_id == r["id"]:
                self.list.setCurrentItem(it)
        if self.list.currentItem() is None and self.list.count():
            self.list.setCurrentRow(0)
        if not self.list.count():
            self.preview.load(None)
            self.info.setText("No report yet. Analyse the study's scans, then generate a report.")
        can_review = bool(self.project and self.project.can("review"))
        self.approve.setEnabled(can_review and self.list.count() > 0)
        self.approve.setToolTip("" if can_review else "Requires the reviewer or administrator role")

    def _selected(self, cur, _prev):
        if cur is None:
            return
        r = cur.data(Qt.UserRole)
        n = self.preview.load(r["pdf_path"] if r["status"] == "ready" else None)
        self.info.setText(f"SHA-256 {r['sha256'][:16]}...  ·  {n} pages" if r.get("sha256") else r["status"])

    def current_report(self):
        it = self.list.currentItem()
        return it.data(Qt.UserRole) if it else None

    def _export(self):
        r = self.current_report()
        if not r:
            return
        d = QFileDialog.getExistingDirectory(self, "Export report to folder")
        if not d:
            return
        from .services import export_report
        try:
            files = export_report(self.project, r["id"], d)
            QMessageBox.information(self, "Report exported", "\n".join(files))
        except PermissionError as e:
            QMessageBox.warning(self, "Export not permitted", str(e))

    def _sign(self, decision):
        r = self.current_report()
        if r:
            self.sign_requested.emit(r["id"], decision)
