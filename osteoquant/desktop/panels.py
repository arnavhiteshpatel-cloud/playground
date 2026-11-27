"""Dockable tool panels: display, segmentation tools, voxel readout, QC, jobs."""
from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QIcon, QPixmap
from PySide6.QtWidgets import (QAbstractItemView, QButtonGroup, QCheckBox, QColorDialog, QComboBox, QDoubleSpinBox,
                               QFormLayout, QGridLayout, QHBoxLayout, QHeaderView, QLabel, QMessageBox,
                               QProgressBar, QPushButton, QRadioButton, QSlider, QTableWidget, QTableWidgetItem,
                               QToolButton, QVBoxLayout, QWidget)

from . import theme
from .jobs import JobManager
from .viewer_state import CLASS_NAMES, EDIT_LABELS, ViewerState


def section(text: str) -> QLabel:
    lb = QLabel(text)
    lb.setProperty("role", "section")
    return lb


def muted(text: str = "") -> QLabel:
    lb = QLabel(text)
    lb.setProperty("role", "muted")
    lb.setWordWrap(True)
    return lb


def swatch(rgb, size=12) -> QIcon:
    pm = QPixmap(size, size)
    pm.fill(QColor(*rgb))
    return QIcon(pm)


def dot(color: QColor, size=10) -> QIcon:
    from PySide6.QtGui import QPainter
    pm = QPixmap(size, size)
    pm.fill(Qt.transparent)
    p = QPainter(pm)
    p.setRenderHint(QPainter.Antialiasing)
    p.setBrush(color)
    p.setPen(Qt.NoPen)
    p.drawEllipse(1, 1, size - 2, size - 2)
    p.end()
    return QIcon(pm)


def set_banner(label: QLabel, text: str, kind: str):
    label.setText(text)
    label.setProperty("role", f"banner-{kind}")
    label.style().unpolish(label)
    label.style().polish(label)


def ro_item(text, align=None, tip=None) -> QTableWidgetItem:
    it = QTableWidgetItem("" if text is None else str(text))
    it.setFlags(it.flags() & ~Qt.ItemIsEditable)
    if align is not None:
        it.setTextAlignment(align)
    if tip:
        it.setToolTip(tip)
    return it


def make_table(headers, stretch_last=True) -> QTableWidget:
    t = QTableWidget(0, len(headers))
    t.setHorizontalHeaderLabels(headers)
    t.verticalHeader().setVisible(False)
    t.setSelectionBehavior(QAbstractItemView.SelectRows)
    t.setEditTriggers(QAbstractItemView.NoEditTriggers)
    t.setAlternatingRowColors(True)
    t.setShowGrid(False)
    t.horizontalHeader().setStretchLastSection(stretch_last)
    t.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
    t.verticalHeader().setDefaultSectionSize(24)
    return t


# ============================================================================ display
class DisplayPanel(QWidget):
    segmentation_selected = Signal(int)     # segmentation id

    def __init__(self, state: ViewerState, parent=None):
        super().__init__(parent)
        self.state = state
        lay = QVBoxLayout(self)
        lay.setContentsMargins(10, 8, 10, 10)
        lay.setSpacing(6)

        lay.addWidget(section("Window / level"))
        self.preset = QComboBox()
        self.preset.activated.connect(self._preset)
        lay.addWidget(self.preset)
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignLeft)
        self.lo, self.hi = QDoubleSpinBox(), QDoubleSpinBox()
        for sb in (self.lo, self.hi):
            sb.setRange(-1e9, 1e9)
            sb.setDecimals(1)
            sb.setKeyboardTracking(False)
            sb.valueChanged.connect(self._manual_window)
        form.addRow("Lower", self.lo)
        form.addRow("Upper", self.hi)
        lay.addLayout(form)
        lay.addWidget(muted("Right-drag in a slice view: horizontal = width, vertical = level."))

        lay.addWidget(section("Segmentation version"))
        self.seg_combo = QComboBox()
        self.seg_combo.activated.connect(lambda i: self.segmentation_selected.emit(int(self.seg_combo.itemData(i))))
        lay.addWidget(self.seg_combo)

        hl = QHBoxLayout()
        hl.addWidget(section("Label overlay"))
        hl.addStretch(1)
        self.show_ovl = QCheckBox("Show")
        self.show_ovl.setChecked(True)
        self.show_ovl.toggled.connect(state.set_show_overlay)
        hl.addWidget(self.show_ovl)
        lay.addLayout(hl)
        grid = QGridLayout()
        grid.setHorizontalSpacing(8)
        grid.setVerticalSpacing(4)
        self._rows = {}
        for r, c in enumerate(EDIT_LABELS):
            vis = QCheckBox(CLASS_NAMES[c])
            vis.setChecked(True)
            vis.toggled.connect(lambda on, c=c: state.set_overlay(c, visible=on))
            col = QToolButton()
            col.setIcon(swatch(state.overlay[c]["color"], 14))
            col.setToolTip("Change colour")
            col.clicked.connect(lambda _=False, c=c: self._pick_color(c))
            op = QSlider(Qt.Horizontal)
            op.setRange(0, 100)
            op.setValue(int(state.overlay[c]["opacity"] * 100))
            op.setToolTip("Opacity")
            op.valueChanged.connect(lambda v, c=c: state.set_overlay(c, opacity=v / 100))
            grid.addWidget(col, r, 0)
            grid.addWidget(vis, r, 1)
            grid.addWidget(op, r, 2)
            self._rows[c] = (vis, col, op)
        grid.setColumnStretch(2, 1)
        lay.addLayout(grid)
        lay.addStretch(1)
        state.scan_changed.connect(self._on_scan)
        state.window_changed.connect(self._on_window)
        self.setEnabled(False)

    def _on_scan(self):
        st = self.state
        self.setEnabled(st.loaded)
        self.preset.clear()
        if st.loaded:
            for name, (lo, hi) in st.presets().items():
                self.preset.addItem(name, (lo, hi))
            mx = max(abs(st.source.stats()["max"]), abs(st.source.stats()["min"]), 1.0)
            dec = 0 if mx > 1000 else (1 if mx > 10 else 3)
            for sb in (self.lo, self.hi):
                sb.setDecimals(dec)

    def set_segmentations(self, segs: list[dict], current_id):
        self.seg_combo.clear()
        for s in segs:
            txt = f"v{s['version']}  {s['kind']}  {s.get('method') or ''}".strip()
            self.seg_combo.addItem(txt, s["id"])
            if s["id"] == current_id:
                self.seg_combo.setCurrentIndex(self.seg_combo.count() - 1)
        if not segs:
            self.seg_combo.addItem("No segmentation (run analysis)", -1)

    def _on_window(self, lo, hi):
        for sb, v in ((self.lo, lo), (self.hi, hi)):
            sb.blockSignals(True)
            sb.setValue(v)
            sb.blockSignals(False)

    def _preset(self, i):
        lo, hi = self.preset.itemData(i)
        self.state.set_window(lo, hi)

    def _manual_window(self, *_):
        if self.lo.value() < self.hi.value():
            self.state.set_window(self.lo.value(), self.hi.value())

    def _pick_color(self, c):
        cur = QColor(*self.state.overlay[c]["color"])
        col = QColorDialog.getColor(cur, self, f"Colour for {CLASS_NAMES[c]}")
        if col.isValid():
            self.state.set_overlay(c, color=(col.red(), col.green(), col.blue()))
            self._rows[c][1].setIcon(swatch(self.state.overlay[c]["color"], 14))


# ============================================================================ segmentation tools
class SegmentationPanel(QWidget):
    save_requested = Signal()

    TOOL_TEXT = [("navigate", "Navigate", "Move the crosshair (N)"),
                 ("brush", "Brush", "Paint the active class (B)"),
                 ("erase", "Eraser", "Erase to background (E)"),
                 ("grow", "Region grow", "Grow from a seed within an intensity tolerance (G)"),
                 ("fill", "Fill holes", "Fill enclosed holes of the active class on the slice (F)")]

    def __init__(self, state: ViewerState, parent=None):
        super().__init__(parent)
        self.state = state
        lay = QVBoxLayout(self)
        lay.setContentsMargins(10, 8, 10, 10)
        lay.setSpacing(6)
        lay.addWidget(section("Tool"))
        tg = QGridLayout()
        tg.setSpacing(4)
        self.tool_group = QButtonGroup(self)
        self.tool_buttons = {}
        for i, (key, text, tip) in enumerate(self.TOOL_TEXT):
            b = QPushButton(text)
            b.setCheckable(True)
            b.setToolTip(tip)
            b.clicked.connect(lambda _=False, k=key: state.set_tool(k))
            self.tool_group.addButton(b)
            self.tool_buttons[key] = b
            tg.addWidget(b, i // 2, i % 2)
        self.tool_buttons["navigate"].setChecked(True)
        lay.addLayout(tg)

        lay.addWidget(section("Class"))
        self.cls = QComboBox()
        for c in EDIT_LABELS:
            self.cls.addItem(swatch(state.overlay[c]["color"]), CLASS_NAMES[c], c)
        self.cls.currentIndexChanged.connect(lambda i: state.set_brush(label=self.cls.itemData(i)))
        lay.addWidget(self.cls)
        self.protect = QCheckBox("Protect other classes")
        self.protect.setToolTip("Brush and region grow change background voxels only; the eraser removes the active class only")
        self.protect.setChecked(True)
        self.protect.toggled.connect(lambda on: state.set_brush(protect=on))
        lay.addWidget(self.protect)

        lay.addWidget(section("Brush"))
        f = QFormLayout()
        self.radius = QDoubleSpinBox()
        self.radius.setRange(1, 5000)
        self.radius.setDecimals(0)
        self.radius.setSuffix(" µm")
        self.radius.setKeyboardTracking(False)
        self.radius.valueChanged.connect(lambda v: state.set_brush(radius_um=v))
        f.addRow("Radius", self.radius)
        mode = QHBoxLayout()
        self.m2d, self.m3d = QRadioButton("2D disk"), QRadioButton("3D sphere")
        self.m2d.setChecked(True)
        self.m3d.toggled.connect(lambda on: state.set_brush(three_d=on))
        mode.addWidget(self.m2d)
        mode.addWidget(self.m3d)
        mode.addStretch(1)
        f.addRow("Shape", mode)
        lay.addLayout(f)

        lay.addWidget(section("Region grow"))
        f2 = QFormLayout()
        self.tol = QDoubleSpinBox()
        self.tol.setRange(0, 1e9)
        self.tol.setDecimals(1)
        self.tol.setKeyboardTracking(False)
        self.tol.valueChanged.connect(lambda v: setattr(state, "grow_tolerance", float(v)))
        f2.addRow("Tolerance", self.tol)
        self.grow3d = QCheckBox("Grow in 3D (bounded to 48 voxels)")
        self.grow3d.toggled.connect(lambda on: setattr(state, "grow_3d", bool(on)))
        f2.addRow("", self.grow3d)
        lay.addLayout(f2)

        lay.addWidget(section("Slice interpolation"))
        self.interp_info = muted("Edit two slices of one orientation, then interpolate the active class between them.")
        lay.addWidget(self.interp_info)
        ib = QHBoxLayout()
        self.interp_btns = []
        for ax, name in enumerate(("Axial", "Coronal", "Sagittal")):
            b = QPushButton(name)
            b.clicked.connect(lambda _=False, a=ax: self._interpolate(a))
            ib.addWidget(b)
            self.interp_btns.append(b)
        lay.addLayout(ib)

        lay.addWidget(section("History"))
        hb = QHBoxLayout()
        self.undo_btn = QPushButton("Undo")
        self.redo_btn = QPushButton("Redo")
        self.undo_btn.clicked.connect(state.history.undo)
        self.redo_btn.clicked.connect(state.history.redo)
        hb.addWidget(self.undo_btn)
        hb.addWidget(self.redo_btn)
        lay.addLayout(hb)
        self.summary = muted("")
        lay.addWidget(self.summary)
        self.save_btn = QPushButton("Save as new revision...")
        self.save_btn.setProperty("role", "primary")
        self.save_btn.clicked.connect(self.save_requested)
        lay.addWidget(self.save_btn)
        lay.addStretch(1)
        state.history.indexChanged.connect(lambda *_: self._refresh())
        state.scan_changed.connect(self._on_scan)
        state.tool_changed.connect(self._on_tool)
        state.labels_changed.connect(lambda *_: self._refresh())
        self._on_scan()

    def _on_scan(self):
        st = self.state
        self.setEnabled(st.can_edit)
        if st.loaded:
            self.radius.blockSignals(True)
            self.radius.setValue(st.brush_radius_um)
            self.radius.blockSignals(False)
            self.tol.blockSignals(True)
            self.tol.setValue(st.grow_tolerance)
            self.tol.blockSignals(False)
        self._refresh()

    def _on_tool(self):
        b = self.tool_buttons.get(self.state.tool)
        if b and not b.isChecked():
            b.setChecked(True)

    def _interpolate(self, axis):
        try:
            if not self.state.interpolate(axis):
                self.state.message.emit("Interpolation changed no voxels")
        except ValueError as e:
            QMessageBox.information(self, "Slice interpolation", str(e))

    def _refresh(self):
        st = self.state
        h = st.history
        self.undo_btn.setEnabled(h.canUndo())
        self.redo_btn.setEnabled(h.canRedo())
        self.undo_btn.setToolTip(h.undoText())
        self.redo_btn.setToolTip(h.redoText())
        if st.editor is None:
            self.summary.setText("Open a scan with a segmentation to edit labels.")
            self.save_btn.setEnabled(False)
            return
        ch = st.editor.change_summary()
        if ch:
            txt = ", ".join(f"{k.replace('_', ' ')} {v:+,}" for k, v in ch.items())
            self.summary.setText(f"Unsaved changes (voxels): {txt}\nHistory: {h.count()} steps, "
                                 f"{h.history_bytes() / 1024:,.1f} KiB")
        else:
            self.summary.setText(f"No unsaved changes. History: {h.count()} steps.")
        self.save_btn.setEnabled(bool(ch))


# ============================================================================ voxel readout
class VoxelInfoPanel(QWidget):
    def __init__(self, state: ViewerState, parent=None):
        super().__init__(parent)
        self.state = state
        f = QFormLayout(self)
        f.setContentsMargins(10, 8, 10, 10)
        self.fields = {}
        for k, lbl in (("voxel", "Voxel (z, y, x)"), ("mm", "Position (mm)"), ("value", "Intensity"),
                       ("label", "Label"), ("spacing", "Voxel size"), ("dims", "Dimensions")):
            w = QLabel("-")
            w.setTextInteractionFlags(Qt.TextSelectableByMouse)
            f.addRow(lbl, w)
            self.fields[k] = w
        self.mode = muted("Pointer")
        f.addRow("Source", self.mode)
        state.hover_changed.connect(self._hover)
        state.cursor_changed.connect(lambda *c: self._show(c, "Crosshair"))
        state.labels_changed.connect(lambda *_: self._show(tuple(state.cursor), "Crosshair"))
        state.scan_changed.connect(self._scan)

    def _scan(self):
        st = self.state
        if not st.loaded:
            for w in self.fields.values():
                w.setText("-")
            return
        self.fields["spacing"].setText(" x ".join(f"{s:g}" for s in st.spacing) + " µm")
        self.fields["dims"].setText(" x ".join(map(str, st.shape)))

    def _hover(self, v):
        if v is None:
            self._show(tuple(self.state.cursor), "Crosshair")
        else:
            self._show(v, "Pointer")

    def _show(self, v, src):
        st = self.state
        if not st.loaded:
            return
        r = st.readout(*v)
        self.fields["voxel"].setText("%d, %d, %d" % r["voxel"])
        self.fields["mm"].setText("%.3f, %.3f, %.3f" % r["mm"])
        self.fields["value"].setText(f"{r['value']:.6g} ({r['unit']})")
        self.fields["label"].setText("-" if r["label"] is None else f"{r['label']}  {r['label_name']}")
        self.mode.setText(src)


# ============================================================================ QC
class QCPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(8, 6, 8, 8)
        self.banner = QLabel("No scan selected")
        set_banner(self.banner, "No scan selected", "info")
        lay.addWidget(self.banner)
        hl = QHBoxLayout()
        left, right = QVBoxLayout(), QVBoxLayout()
        left.addWidget(section("Deterministic checks (facts about file and metadata)"))
        self.det = make_table(["ID", "Check", "Status", "Value", "Message"])
        self.det.setMinimumHeight(110)
        left.addWidget(self.det)
        right.addWidget(section("Heuristic checks (developer-chosen thresholds; not standards)"))
        self.heu = make_table(["ID", "Check", "Status", "Value", "Message"])
        self.heu.setMinimumHeight(110)
        right.addWidget(self.heu)
        hl.addLayout(left)
        hl.addLayout(right)
        lay.addLayout(hl, 1)

    def show_qc(self, qc: dict | None, title: str = ""):
        for t in (self.det, self.heu):
            t.setRowCount(0)
        if not qc:
            set_banner(self.banner, f"{title}: QC has not been run" if title else "No QC result", "info")
            return
        v = qc.get("verdict", "?")
        kind = {"suitable": "ok", "review": "warn", "unsuitable": "bad"}.get(v, "info")
        extra = ""
        if qc.get("decimated_for_qc"):
            extra = "  " + qc["decimated_for_qc"]["note"]
        set_banner(self.banner, f"{title}   QC verdict: {v.upper()}   ({qc.get('n_fail', 0)} fail, "
                                f"{qc.get('n_warn', 0)} warn){extra}", kind)
        fill_qc_tables(qc, self.det, self.heu)


def fmt_value(v) -> str:
    if isinstance(v, float):
        return f"{v:.4g}"
    if isinstance(v, (list, tuple)):
        return ", ".join(fmt_value(x) for x in v[:6]) + (" ..." if len(v) > 6 else "")
    if isinstance(v, dict):
        return "; ".join(f"{k}={fmt_value(x)}" for k, x in list(v.items())[:4])
    return "" if v is None else str(v)


def fill_qc_tables(qc: dict, det: QTableWidget, heu: QTableWidget):
    for t in (det, heu):
        t.setRowCount(0)
    for c in qc.get("checks", []):
        t = det if c.get("basis") == "deterministic" else heu
        r = t.rowCount()
        t.insertRow(r)
        val = fmt_value(c.get("value"))
        st = ro_item(c["status"])
        st.setForeground(theme.status_color({"pass": "suitable", "warn": "review", "fail": "unsuitable"}.get(c["status"], "")))
        for j, it in enumerate([ro_item(c["id"]), ro_item(c["name"], tip=c["name"]), st, ro_item(val),
                                ro_item(c.get("message", ""), tip=c.get("message", ""))]):
            t.setItem(r, j, it)
    for t in (det, heu):
        t.resizeColumnsToContents()
        t.horizontalHeader().setStretchLastSection(True)


# ============================================================================ jobs
class JobsPanel(QWidget):
    def __init__(self, jobs: JobManager, parent=None):
        super().__init__(parent)
        self.jobs = jobs
        lay = QVBoxLayout(self)
        lay.setContentsMargins(8, 6, 8, 8)
        self.table = make_table(["#", "Job", "Status", "Progress", "Message", ""])
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.cellDoubleClicked.connect(self._details)
        lay.addWidget(self.table)
        self._rows: dict[int, int] = {}
        jobs.job_added.connect(self._add)
        jobs.job_changed.connect(self._update)
        jobs.job_finished.connect(self._update)

    def _add(self, job):
        r = self.table.rowCount()
        self.table.insertRow(r)
        self._rows[job.id] = r
        self.table.setItem(r, 0, ro_item(job.id))
        self.table.setItem(r, 1, ro_item(job.title))
        pb = QProgressBar()
        pb.setRange(0, 1000)
        pb.setTextVisible(False)
        pb.setFixedHeight(10)
        host = QWidget()
        hl = QHBoxLayout(host)
        hl.setContentsMargins(4, 0, 4, 0)
        hl.addWidget(pb)
        host.bar = pb
        self.table.setCellWidget(r, 3, host)
        b = QToolButton()
        b.setText("Cancel")
        b.clicked.connect(lambda _=False, j=job.id: self.jobs.cancel(j))
        self.table.setCellWidget(r, 5, b)
        self._update(job)
        self.table.resizeColumnToContents(1)
        self.table.scrollToBottom()

    def _update(self, job):
        r = self._rows.get(job.id)
        if r is None:
            return
        st = ro_item(job.status)
        st.setForeground(theme.status_color(job.status))
        self.table.setItem(r, 2, st)
        host = self.table.cellWidget(r, 3)
        if host:
            host.bar.setValue(int(job.progress * 1000))
            host.setToolTip(f"{job.progress:.0%}")
        msg = job.error or job.message
        self.table.setItem(r, 4, ro_item(msg, tip=job.traceback or msg))
        b = self.table.cellWidget(r, 5)
        if b:
            b.setEnabled(job.active)
            b.setVisible(job.active)

    def _details(self, row, _col):
        for jid, r in self._rows.items():
            if r == row:
                j = self.jobs.jobs[jid]
                if j.error:
                    box = QMessageBox(QMessageBox.Warning, "Job failed", f"{j.title}\n\n{j.error}", parent=self)
                    box.setDetailedText(j.traceback)
                    box.exec()
