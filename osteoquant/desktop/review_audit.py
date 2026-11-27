"""Review / sign-off panel for the open scan and the audit-trail viewer."""
from __future__ import annotations

import json

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QCheckBox, QComboBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSplitter,
                               QTextEdit, QVBoxLayout, QWidget)

from . import theme
from .panels import make_table, muted, ro_item, section, set_banner


class ReviewPanel(QWidget):
    sign_requested = Signal(str, int, str)       # object type, id, decision
    blinded_toggled = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.project = None
        self.scan_id = None
        lay = QVBoxLayout(self)
        lay.setContentsMargins(10, 8, 10, 10)
        self.blind = QCheckBox("Blinded review mode")
        self.blind.setToolTip("Hide group names, animal IDs and file names in the tree, results and viewer")
        self.blind.toggled.connect(self.blinded_toggled)
        lay.addWidget(self.blind)
        lay.addWidget(muted("Blinded mode hides allocation for everyone, including administrators. Study-level "
                            "blinding stored in the project additionally applies to non-administrators."))
        lay.addWidget(section("Segmentation versions of the open scan"))
        self.table = make_table(["Version", "Kind", "Author", "Latest review", "Labels SHA-256"])
        self.table.itemSelectionChanged.connect(self._sel)
        lay.addWidget(self.table, 1)
        self.history = make_table(["Time (UTC)", "Reviewer", "Decision", "Meaning"])
        lay.addWidget(section("Review history of selected version"))
        lay.addWidget(self.history, 1)
        row = QHBoxLayout()
        self.btns = {}
        for dec, text in (("approved", "Approve..."), ("needs_changes", "Needs changes..."), ("rejected", "Reject...")):
            b = QPushButton(text)
            if dec == "approved":
                b.setProperty("role", "primary")
            b.clicked.connect(lambda _=False, d=dec: self._sign(d))
            row.addWidget(b)
            self.btns[dec] = b
        lay.addLayout(row)
        self.note = muted("")
        lay.addWidget(self.note)
        self._segs = []

    def set_scan(self, project, scan_id):
        self.project, self.scan_id = project, scan_id
        self.refresh()

    def refresh(self):
        self.table.setRowCount(0)
        self.history.setRowCount(0)
        p = self.project
        if not p or not p.user or self.scan_id is None:
            self.note.setText("Open a scan to review its segmentations.")
            for b in self.btns.values():
                b.setEnabled(False)
            return
        users = {u["id"]: u["username"] for u in p.store.q("SELECT id, username FROM users WHERE org_id=?", (p.user["org_id"],))}
        self._segs = p.store.segmentations(p.user, self.scan_id)
        for s in self._segs:
            revs = p.store.reviews(p.user, "segmentation", s["id"])
            last = revs[-1] if revs else None
            r = self.table.rowCount()
            self.table.insertRow(r)
            dec = ro_item(f"{last['decision']} ({last['username']})" if last else "not reviewed")
            dec.setForeground(theme.status_color(last["decision"] if last else ""))
            for j, it in enumerate([ro_item(f"v{s['version']}"), ro_item(s["kind"]),
                                    ro_item(users.get(s["created_by"], s["created_by"])), dec,
                                    ro_item((s["labels_sha256"] or "")[:16], tip=s["labels_sha256"])]):
                self.table.setItem(r, j, it)
        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setStretchLastSection(True)
        if self._segs:
            self.table.selectRow(len(self._segs) - 1)
        can = p.can("review")
        for b in self.btns.values():
            b.setEnabled(can and bool(self._segs))
        self.note.setText("Signing requires your password. Authors cannot approve their own segmentations "
                          "(separation of duties)." if can else
                          f"Your role ({p.user['role']}) cannot sign. Reviewer or administrator role required.")

    def selected_segmentation(self):
        rows = {i.row() for i in self.table.selectedIndexes()}
        return self._segs[min(rows)] if rows else None

    def _sel(self):
        self.history.setRowCount(0)
        s = self.selected_segmentation()
        if not s:
            return
        for rv in self.project.store.reviews(self.project.user, "segmentation", s["id"]):
            r = self.history.rowCount()
            self.history.insertRow(r)
            for j, v in enumerate([rv["created"], rv["full_name"] or rv["username"], rv["decision"], rv["meaning"]]):
                self.history.setItem(r, j, ro_item(v, tip=rv.get("comment") or None))
        self.history.resizeColumnsToContents()
        self.history.horizontalHeader().setStretchLastSection(True)

    def _sign(self, decision):
        s = self.selected_segmentation()
        if s:
            self.sign_requested.emit("segmentation", s["id"], decision)


class AuditView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.project = None
        lay = QVBoxLayout(self)
        lay.setContentsMargins(10, 8, 10, 8)
        top = QHBoxLayout()
        t = QLabel("Audit trail")
        t.setProperty("role", "heading")
        top.addWidget(t)
        top.addSpacing(12)
        self.filter = QLineEdit()
        self.filter.setPlaceholderText("Filter by action, object or details")
        self.filter.textChanged.connect(self._apply_filter)
        self.otype = QComboBox()
        self.otype.addItems(["All objects", "scan", "segmentation", "report", "study", "roi", "measurement", "job", "user"])
        self.otype.currentIndexChanged.connect(self.refresh)
        top.addWidget(self.filter, 1)
        top.addWidget(self.otype)
        self.verify = QPushButton("Verify chain")
        self.verify.setProperty("role", "primary")
        self.verify.clicked.connect(self.verify_chain)
        rb = QPushButton("Refresh")
        rb.clicked.connect(self.refresh)
        top.addWidget(rb)
        top.addWidget(self.verify)
        lay.addLayout(top)
        self.result = QLabel("")
        self.result.setWordWrap(True)
        set_banner(self.result, "The audit trail is append-only and hash-chained. Verify recomputes every hash.", "info")
        lay.addWidget(self.result)
        split = QSplitter(Qt.Vertical)
        self.table = make_table(["Seq", "Time (UTC)", "User", "Action", "Object", "Row hash"])
        self.table.itemSelectionChanged.connect(self._details)
        split.addWidget(self.table)
        self.detail = QTextEdit()
        self.detail.setReadOnly(True)
        split.addWidget(self.detail)
        split.setSizes([400, 140])
        lay.addWidget(split, 1)
        self._events = []

    def set_project(self, project):
        self.project = project
        self.refresh()

    def refresh(self):
        self.table.setRowCount(0)
        p = self.project
        if not p or not p.user:
            return
        if not (p.can("review") or p.can("manage_users")):
            set_banner(self.result, "Viewing the audit trail requires the reviewer or administrator role. "
                                    "Chain verification is available to all users.", "warn")
            self._events = []
            return
        ot = self.otype.currentText()
        self._events = p.store.audit.events(org_id=p.user["org_id"], object_type=None if ot == "All objects" else ot,
                                            limit=5000)
        users = {str(u["id"]): u["username"] for u in p.store.q("SELECT id, username FROM users")}
        for e in self._events:
            r = self.table.rowCount()
            self.table.insertRow(r)
            obj = f"{e['object_type'] or ''} {e['object_id'] or ''}".strip()
            for j, v in enumerate([e["seq"], e["ts"].replace("T", " ")[:23], users.get(e["user_id"], e["user_id"] or "system"),
                                   e["action"], obj, e["row_hash"][:16]]):
                self.table.setItem(r, j, ro_item(v))
        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setStretchLastSection(True)
        self._apply_filter()

    def _apply_filter(self):
        q = self.filter.text().strip().lower()
        for r, e in enumerate(self._events):
            hay = f"{e['action']} {e['object_type']} {e['object_id']} {json.dumps(e['details'])}".lower()
            self.table.setRowHidden(r, bool(q) and q not in hay)

    def _details(self):
        rows = {i.row() for i in self.table.selectedIndexes()}
        if rows:
            e = self._events[min(rows)]
            self.detail.setPlainText(json.dumps(e, indent=2, default=str))

    def verify_chain(self) -> dict:
        p = self.project
        if not p:
            return {}
        res = p.store.audit.verify_chain()
        if res.get("ok"):
            set_banner(self.result, f"Chain verified: {res['n']} events, every hash recomputed and linked. "
                                    f"Head {res['head'][:16]}...", "ok")
        else:
            set_banner(self.result, f"CHAIN BROKEN at event {res.get('first_bad_seq')}: {res.get('reason')} "
                                    f"({res.get('n')} events verified before it).", "bad")
        u = p.user
        p.store.audit.record("audit.verify", u["id"], u["org_id"], details={"ok": bool(res.get("ok")), "n": res.get("n")})
        return res
