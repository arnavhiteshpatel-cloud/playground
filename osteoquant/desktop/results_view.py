"""Results: per-scan endpoint table with units and a support status per scan and endpoint."""
from __future__ import annotations

import csv

from PySide6.QtCore import QAbstractTableModel, QModelIndex, QSortFilterProxyModel, Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QAbstractItemView, QComboBox, QFileDialog, QHBoxLayout, QLabel, QPushButton,
                               QSplitter, QTableView, QTextBrowser, QVBoxLayout, QWidget)

from . import theme
from .panels import muted
from .support import ENDPOINTS, FLAGGED, NOT_SUPPORTED, SUPPORTED, endpoint_value, measurement_support

NOT_ANALYSED = "not analysed"
NOT_MEASURED = "not measured"

FIXED_COLS = [("scan", "Scan"), ("animal", "Animal"), ("group", "Group"), ("timepoint", "Timepoint"),
              ("qc", "QC"), ("roi", "ROI"), ("method", "Method"), ("version", "Seg."), ("review", "Review"),
              ("status", "Support")]


def _fmt(v, unit):
    if v is None:
        return NOT_MEASURED
    if isinstance(v, float):
        if unit == "%":
            return f"{v:.1f}"
        return f"{v:.4g}"
    return str(v)


def build_rows(project, study_id, blinded_view=False) -> list[dict]:
    """One row per scan with its latest measurement (or the reason there is none).

    Every endpoint goes through ``support.endpoint_value``: a *not supported* endpoint never carries
    a number. QC "review"/"unsuitable" and an unaccepted automatic ROI make every endpoint *flagged*
    (never green). ROI acceptance, QC, method and review state are separate columns."""
    from . import services as S
    store, user = project.store, project.require_user()
    specs = {s["id"]: s for s in store.specimens(user, study_id)}
    tps = {t["id"]: t["label"] for t in project.timepoints(study_id)}
    meas = {m["scan_id"]: m for m in store.latest_measurements(user, study_id)}
    rows = []
    for sc in store.scans(user, study_id):
        m = meas.get(sc["id"])
        full = store.scan(user, sc["id"])
        res = m["metrics"] if m else {"status": sc["status"]}
        if m and not res.get("qc"):
            res = {**res, "qc": full.get("qc")}
        roi = S.roi_state(project, m["roi_id"]) if m else None
        sup = measurement_support(res, roi_accepted=bool(roi and roi["accepted"]))
        sp = specs.get(sc["specimen_id"], {})
        seg = store.q1("SELECT * FROM segmentations WHERE id=?", (m["segmentation_id"],)) if m else None
        revs = store.reviews(user, "segmentation", seg["id"]) if seg else []
        last = revs[-1] if revs else None
        meth = S.segmentation_method_info(seg, res) if seg else {"text": "-", "synthetic": False, "provenance": ""}
        qc_v = (full.get("qc") or {}).get("verdict") or "not run"
        if roi and roi["roi"] is not None:
            kind = "manual" if roi["manual"] else "auto"
            roi_txt = f"{kind} · {roi['status']}"
        else:
            roi_txt = "-"
        row = {"scan_id": sc["id"],
               "scan": project.scan_code(sc["id"], study_id) if blinded_view else sc["source_name"],
               "animal": (project.animal_code(sp["id"], study_id) if blinded_view and sp else
                          ("-" if blinded_view else sp.get("animal_id", "-"))),
               "group": "(blinded)" if blinded_view else (sp.get("group_name") or "-"),
               "timepoint": tps.get(sc["timepoint_id"], "-"),
               "qc": qc_v, "roi": roi_txt, "roi_status": roi["status"] if roi else "",
               "method": meth["text"], "synthetic": bool(meth.get("synthetic")),
               "method_tip": meth.get("provenance", ""),
               "version": f"v{seg['version']} {seg['kind']}" if seg else "-",
               "review": (f"{last['decision'].replace('_', ' ')} ({last['full_name'] or last['username']})" if last
                          else ("not reviewed" if seg else "-")),
               "review_decision": last["decision"] if last else "",
               "status": sup["overall"] if m else NOT_ANALYSED,
               "status_tip": "\n".join(sup["reasons"]) if m else
               ("Analysis not run" if sc["status"] != "needs_manual_roi" else "ROI not detected: define a manual ROI"),
               "segmentation_id": m["segmentation_id"] if m else None, "values": {}, "support": sup}
        for key, label, unit, path, scale in ENDPOINTS:
            if m:
                v, st, reasons = endpoint_value(res, sup, key)
            else:
                v, st, reasons = None, NOT_SUPPORTED, ["analysis not run"]
            row["values"][key] = {"value": v, "status": st, "reasons": reasons, "tip": "; ".join(reasons)}
        rows.append(row)
    return rows


def _csv_safe(v):
    if isinstance(v, str) and len(v) > 1 and v[:1] in ("=", "+", "-", "@", "\t", "\r"):
        return "'" + v
    return v


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
                if key == "status":
                    return theme.STATUS_PREFIX.get(row["status"], "") + row["status"]
                return row[key]
            if key == "status" and role == Qt.ForegroundRole:
                return theme.status_color(row["status"] if row["status"] != NOT_ANALYSED else "")
            if key == "status" and role == Qt.ToolTipRole:
                return row["status_tip"]
            if key == "qc" and role == Qt.ForegroundRole:
                return theme.status_color(row["qc"] if row["qc"] != "not run" else "")
            if key == "roi" and role == Qt.ForegroundRole:
                return theme.status_color({"accepted": "approved", "awaiting acceptance": "review",
                                           "rejected": "rejected", "needs_changes": "review"}.get(row["roi_status"], ""))
            if key == "roi" and role == Qt.ToolTipRole:
                return ("Automatic ROI: review the yellow outline in the viewer, then a reviewer signs 'Accept ROI' "
                        "in the Review panel." if row["roi_status"] == "awaiting acceptance" else None)
            if key == "method" and role == Qt.ForegroundRole and row.get("synthetic"):
                return theme.qcolor("bad")
            if key == "method" and role == Qt.ToolTipRole:
                return row.get("method_tip") or None
            if key == "review" and role == Qt.ForegroundRole:
                return theme.status_color(row.get("review_decision", ""))
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
                return theme.qcolor("text_muted")       # >= 4.5:1 in both themes (UX-28)
            if cell["status"] == FLAGGED:
                return theme.status_color("flagged")
            if cell["status"] == NOT_SUPPORTED:
                return theme.status_color("not supported")
        if role == Qt.FontRole and cell["value"] is None:
            f = QFont()
            f.setItalic(True)
            return f
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
        self.view.sortByColumn(0, Qt.AscendingOrder)
        split = QSplitter(Qt.Vertical)
        split.addWidget(self.view)
        self.detail = QTextBrowser()
        self.detail.setOpenLinks(False)
        self.detail.setPlaceholderText("Select a row to see why each endpoint is supported, flagged or not measured.")
        split.addWidget(self.detail)
        split.setSizes([420, 170])
        lay.addWidget(split, 1)
        self.view.selectionModel().selectionChanged.connect(lambda *_: self._show_detail())
        self.note = muted("")
        lay.addWidget(self.note)
        self.watermark = None

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
        n_syn = sum(bool(r.get("synthetic")) for r in rows)
        self.note.setText(f"{len(rows)} scans: {n_ok} supported, {n_fl} flagged (\u26a0), {n_ns} not supported (\u2716), "
                          f"{n_na} not analysed.   Orange values: use with caution. 'not measured': no number is shown "
                          "because the endpoint is not supported for this scan; select the row for the reasons. "
                          "Values come from the latest segmentation version of each scan."
                          + (f"   {n_syn} scan(s) were segmented with a model trained on synthetic data only "
                             "(SYNTHETIC-TRAINED, research only)." if n_syn else ""))
        self._show_detail()

    def selected_row(self):
        idx = self.view.selectionModel().selectedRows() if self.view.selectionModel() else []
        if not idx:
            return None
        return self.model.rows[self.proxy.mapToSource(idx[0]).row()]

    def _show_detail(self):
        r = self.selected_row()
        if r is None:
            self.detail.clear()
            return
        from html import escape as h
        parts = [f"<b>{h(str(r['scan']))}</b> &middot; {h(str(r['animal']))} &middot; {h(str(r['timepoint']))} &middot; "
                 f"QC: {h(r['qc'])} &middot; ROI: {h(r['roi'])} &middot; Method: {h(r['method'])} &middot; "
                 f"Review: {h(r['review'])}"]
        if r["status"] == NOT_ANALYSED:
            parts.append(h(r["status_tip"]))
        else:
            parts.append("<table cellspacing=0 cellpadding=2>")
            for key, label, unit, *_ in ENDPOINTS:
                c = r["values"][key]
                st = c["status"]
                val = "<i>not measured</i>" if c["value"] is None else f"{_fmt(c['value'], unit)} {h(unit)}"
                reasons = "; ".join(h(x) for x in c["reasons"]) or "no caution"
                parts.append(f"<tr><td><b>{h(label)}</b></td><td>{theme.STATUS_PREFIX.get(st, '')}{h(st)}</td>"
                             f"<td>{val}</td><td>{reasons}</td></tr>")
            parts.append("</table>")
        self.detail.setHtml("<br>".join(parts[:1]) + "<br>" + "".join(parts[1:]))

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
            if self.watermark:
                f.write(f"# {self.watermark}\n")
            w = csv.writer(f)
            w.writerow([h for _, h in FIXED_COLS] + [f"{lab} ({u})" for _, lab, u, *_ in ENDPOINTS]
                       + [f"{lab} support" for _, lab, *_ in ENDPOINTS] + [f"{lab} reasons" for _, lab, *_ in ENDPOINTS])
            for r in self.model.rows:
                # not supported / not measured endpoints are exported without a number (UX-03)
                w.writerow([_csv_safe(r[k]) for k, _ in FIXED_COLS]
                           + ["" if r["values"][k]["value"] is None else r["values"][k]["value"] for k, *_ in ENDPOINTS]
                           + [r["values"][k]["status"] for k, *_ in ENDPOINTS]
                           + [_csv_safe("; ".join(r["values"][k]["reasons"])) for k, *_ in ENDPOINTS])
        if self.project:
            u = self.project.user
            self.project.store.audit.record("results.export_csv", u["id"], u["org_id"], "study", self.study.currentData(),
                                            {"path": str(path), "rows": len(self.model.rows)})
        return path
