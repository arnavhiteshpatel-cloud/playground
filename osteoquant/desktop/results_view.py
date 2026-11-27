"""Results: per-scan endpoint table with units and a support status per scan and endpoint."""
from __future__ import annotations

import csv

from PySide6.QtCore import QAbstractTableModel, QModelIndex, QSortFilterProxyModel, Qt, Signal
from PySide6.QtWidgets import (QAbstractItemView, QComboBox, QFileDialog, QHBoxLayout, QLabel, QPushButton,
                               QTableView, QVBoxLayout, QWidget)

from . import theme
from .panels import muted
from .support import ENDPOINTS, FLAGGED, NOT_SUPPORTED, SUPPORTED, measurement_support, reported_value

NOT_ANALYSED = "not analysed"

FIXED_COLS = [("scan", "Scan"), ("animal", "Animal"), ("group", "Group"), ("timepoint", "Timepoint"),
              ("version", "Seg."), ("status", "Support"), ]


def _fmt(v, unit):
    if v is None:
        return "not measured"
    if isinstance(v, float):
        if unit == "%":
            return f"{v:.1f}"
        return f"{v:.4g}"
    return str(v)


def build_rows(project, study_id, blinded_view=False) -> list[dict]:
    """One row per scan with its latest measurement (or the reason there is none)."""
    store, user = project.store, project.require_user()
    specs = {s["id"]: s for s in store.specimens(user, study_id)}
    tps = {t["id"]: t["label"] for t in project.timepoints(study_id)}
    meas = {m["scan_id"]: m for m in store.latest_measurements(user, study_id)}
    rows = []
    for sc in store.scans(user, study_id):
        m = meas.get(sc["id"])
        res = m["metrics"] if m else {"status": sc["status"]}
        if m and "qc" not in res:
            full = store.scan(user, sc["id"])
            res = {**res, "qc": full.get("qc")}
        sup = measurement_support(res)
        sp = specs.get(sc["specimen_id"], {})
        seg = store.q1("SELECT version, kind FROM segmentations WHERE id=?", (m["segmentation_id"],)) if m else None
        row = {"scan_id": sc["id"], "scan": f"{sc['id']:04d}" if blinded_view else sc["source_name"],
               "animal": (f"Animal {sp['id']:03d}" if blinded_view and sp else sp.get("animal_id", "-")),
               "group": "(blinded)" if blinded_view else (sp.get("group_name") or "-"),
               "timepoint": tps.get(sc["timepoint_id"], "-"),
               "version": f"v{seg['version']} {seg['kind']}" if seg else "-",
               "status": sup["overall"] if m else NOT_ANALYSED,
               "status_tip": "\n".join(sup["reasons"]) if m else
               ("Analysis not run" if sc["status"] != "needs_manual_roi" else "ROI not detected: define a manual ROI"),
               "segmentation_id": m["segmentation_id"] if m else None, "values": {}, "support": sup}
        for key, label, unit, path, scale in ENDPOINTS:
            v, why = reported_value(res, path) if m else (None, "analysis not run")
            if isinstance(v, (int, float)) and v is not None:
                v = float(v) * scale
            e = sup["endpoints"][key]
            reasons = list(e["reasons"]) + ([why] if why and why not in e["reasons"] else [])
            row["values"][key] = {"value": v, "status": e["status"] if v is not None else NOT_SUPPORTED,
                                  "tip": "; ".join(r for r in reasons if r)}
        rows.append(row)
    return rows


class ResultsModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.rows: list[dict] = []

    def set_rows(self, rows):
        self.beginResetModel()
        self.rows = rows
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()):
        return 0 if parent.isValid() else len(self.rows)

    def columnCount(self, parent=QModelIndex()):
        return 0 if parent.isValid() else len(FIXED_COLS) + len(ENDPOINTS)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation != Qt.Horizontal:
            return None
        if section < len(FIXED_COLS):
            if role == Qt.DisplayRole:
                return FIXED_COLS[section][1]
            return None
        key, label, unit, path, _ = ENDPOINTS[section - len(FIXED_COLS)]
        if role == Qt.DisplayRole:
            return f"{label} ({unit})"
        if role == Qt.ToolTipRole:
            return f"{label} [{unit}] - metric '{path}'"
        return None

    def data(self, idx, role=Qt.DisplayRole):
        if not idx.isValid():
            return None
        row = self.rows[idx.row()]
        c = idx.column()
        if c < len(FIXED_COLS):
            key = FIXED_COLS[c][0]
            if role == Qt.DisplayRole:
                return row[key]
            if key == "status" and role == Qt.ForegroundRole:
                return theme.status_color(row["status"] if row["status"] != NOT_ANALYSED else "")
            if key == "status" and role == Qt.ToolTipRole:
                return row["status_tip"]
            if role == Qt.UserRole:
                return row[key]
            return None
        key, label, unit, *_ = ENDPOINTS[c - len(FIXED_COLS)]
        cell = row["values"][key]
        if role == Qt.DisplayRole:
            return _fmt(cell["value"], unit)
        if role == Qt.UserRole:
            return cell["value"] if cell["value"] is not None else float("-inf")
        if role == Qt.TextAlignmentRole:
            return int(Qt.AlignRight | Qt.AlignVCenter)
        if role == Qt.ForegroundRole:
            if cell["value"] is None:
                return theme.qcolor("text_disabled")
            if cell["status"] == FLAGGED:
                return theme.status_color("flagged")
            if cell["status"] == NOT_SUPPORTED:
                return theme.status_color("not supported")
        if role == Qt.ToolTipRole:
            return f"{label}: {cell['status']}" + (f"\n{cell['tip']}" if cell["tip"] else "")
        return None


class ResultsView(QWidget):
    open_scan = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.project = None
        self.blinded = False
        lay = QVBoxLayout(self)
        lay.setContentsMargins(10, 8, 10, 8)
        top = QHBoxLayout()
        t = QLabel("Results")
        t.setProperty("role", "heading")
        top.addWidget(t)
        top.addSpacing(12)
        top.addWidget(QLabel("Study"))
        self.study = QComboBox()
        self.study.setMinimumWidth(200)
        self.study.currentIndexChanged.connect(self.refresh)
        top.addWidget(self.study)
        top.addStretch(1)
        self.export_btn = QPushButton("Export CSV...")
        self.export_btn.clicked.connect(self.export_csv)
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh)
        top.addWidget(self.refresh_btn)
        top.addWidget(self.export_btn)
        lay.addLayout(top)
        self.model = ResultsModel(self)
        self.proxy = QSortFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)
        self.proxy.setSortRole(Qt.UserRole)
        self.view = QTableView()
        self.view.setModel(self.proxy)
        self.view.setSortingEnabled(True)
        self.view.setAlternatingRowColors(True)
        self.view.setShowGrid(False)
        self.view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.view.verticalHeader().setVisible(False)
        self.view.verticalHeader().setDefaultSectionSize(24)
        self.view.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.view.doubleClicked.connect(self._dbl)
        lay.addWidget(self.view, 1)
        self.note = muted("")
        lay.addWidget(self.note)

    def set_project(self, project, study_id=None):
        self.project = project
        self.study.blockSignals(True)
        self.study.clear()
        if project and project.user:
            for s in project.store.list_studies(project.user):
                self.study.addItem(s["name"], s["id"])
                if s["id"] == study_id:
                    self.study.setCurrentIndex(self.study.count() - 1)
        self.study.blockSignals(False)
        self.refresh()

    def set_blinded(self, on: bool):
        self.blinded = on
        self.refresh()

    def refresh(self):
        sid = self.study.currentData()
        if not self.project or sid is None:
            self.model.set_rows([])
            return
        rows = build_rows(self.project, sid, self.blinded)
        self.model.set_rows(rows)
        self.view.resizeColumnsToContents()
        n_ok = sum(r["status"] == SUPPORTED for r in rows)
        n_fl = sum(r["status"] == FLAGGED for r in rows)
        n_ns = sum(r["status"] == NOT_SUPPORTED for r in rows)
        n_na = sum(r["status"] == NOT_ANALYSED for r in rows)
        self.note.setText(f"{len(rows)} scans: {n_ok} supported, {n_fl} flagged, {n_ns} not supported, {n_na} not analysed.   "
                          "Orange values: use with caution. 'not measured': the endpoint is not supported for this scan "
                          "(hover for the reason). Values come from the latest segmentation version of each scan.")

    def _dbl(self, idx):
        r = self.model.rows[self.proxy.mapToSource(idx).row()]
        self.open_scan.emit(r["scan_id"])

    def export_csv(self, path=None):
        if not self.model.rows:
            return None
        if not path:
            path, _ = QFileDialog.getSaveFileName(self, "Export results", "results.csv", "CSV (*.csv)")
            if not path:
                return None
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow([h for _, h in FIXED_COLS] + [f"{lab} ({u})" for _, lab, u, *_ in ENDPOINTS]
                       + [f"{lab} support" for _, lab, *_ in ENDPOINTS])
            for r in self.model.rows:
                w.writerow([r[k] for k, _ in FIXED_COLS] + ["" if r["values"][k]["value"] is None else r["values"][k]["value"]
                                                            for k, *_ in ENDPOINTS]
                           + [r["values"][k]["status"] for k, *_ in ENDPOINTS])
        if self.project:
            u = self.project.user
            self.project.store.audit.record("results.export_csv", u["id"], u["org_id"], "study", self.study.currentData(),
                                            {"path": str(path), "rows": len(self.model.rows)})
        return path
