"""Review / sign-off panel for the open scan and the audit-trail viewer."""
from __future__ import annotations

import json

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QCheckBox, QComboBox, QFileDialog, QFrame, QHBoxLayout, QLabel, QLineEdit,
                               QMessageBox, QPushButton, QScrollArea, QSplitter, QTextBrowser, QTextEdit, QVBoxLayout,
                               QWidget)

from . import theme
from .panels import make_table, muted, ro_item, section, set_banner


class ReviewPanel(QWidget):
    """Review of the open scan: ROI acceptance, segmentation versions with what changed, sign-off.

    The reviewer sees, for the selected version, the parent version, the editor, the reason for the
    edit, the voxel and volume change per class and every endpoint before -> after (UX-06), and can
    highlight the changed voxels in the slice views. Actions the signed-in role cannot perform are
    disabled with a tooltip that says why (UX-10)."""
    sign_requested = Signal(str, int, str)       # object type, id, decision
    blinded_toggled = Signal(bool)
    roi_edit_requested = Signal()
    compare_toggled = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.project = None
        self.scan_id = None
        self.blinded = False
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        body = QWidget()
        sa = QScrollArea()
        sa.setWidgetResizable(True)
        sa.setFrameShape(QFrame.NoFrame)
        sa.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        sa.setWidget(body)
        self._scroll = sa
        outer.addWidget(sa, 1)
        lay = QVBoxLayout(body)
        lay.setContentsMargins(10, 8, 10, 6)
        self.blind = QCheckBox("Blinded review mode")
        self.blind.setToolTip("Hide group names, animal IDs, file names and acquisition metadata in every view, "
                              "including the audit trail and report preview; random codes replace IDs")
        self.blind.toggled.connect(self.blinded_toggled)
        lay.addWidget(self.blind)
        lay.addWidget(muted("Blinded mode hides allocation and identity for everyone, including administrators. "
                            "Study-level blinding stored in the project additionally applies to non-administrators."))

        lay.addWidget(section("Analysis ROI"))
        self.roi_label = QLabel("")
        self.roi_label.setWordWrap(True)
        self.roi_label.setTextFormat(Qt.RichText)
        lay.addWidget(self.roi_label)
        rr = QHBoxLayout()
        self.accept_roi = QPushButton("Accept ROI...")
        self.accept_roi.clicked.connect(self._accept_roi)
        self.edit_roi = QPushButton("Edit ROI...")
        self.edit_roi.clicked.connect(self.roi_edit_requested)
        rr.addWidget(self.accept_roi)
        rr.addWidget(self.edit_roi)
        rr.addStretch(1)
        lay.addLayout(rr)

        lay.addWidget(section("Segmentation versions of the open scan"))
        self.table = make_table(["Version", "Kind", "Method", "Author", "Latest review"])
        self.table.setMinimumHeight(110)
        self.table.setMinimumWidth(120)
        self.table.itemSelectionChanged.connect(self._sel)
        lay.addWidget(self.table)
        lay.addWidget(section("What changed in the selected version"))
        self.detail = QTextBrowser()
        self.detail.setMinimumHeight(190)
        lay.addWidget(self.detail)
        self.compare = QCheckBox("Highlight changes vs parent (magenta)")
        self.compare.setToolTip("Highlight, in the slice views, every voxel whose label differs from the parent version")
        self.compare.toggled.connect(self.compare_toggled)
        lay.addWidget(self.compare)
        self.history = make_table(["Time (UTC)", "Reviewer", "Signature role", "Decision", "Meaning"])
        self.history.setMinimumHeight(90)
        self.history.setMinimumWidth(120)
        lay.addWidget(section("Review history of selected version"))
        lay.addWidget(self.history)

        foot = QWidget()
        fl = QVBoxLayout(foot)
        fl.setContentsMargins(10, 6, 10, 10)
        row = QHBoxLayout()
        self.btns = {}
        for dec, text in (("approved", "Approve..."), ("needs_changes", "Request changes..."), ("rejected", "Reject...")):
            b = QPushButton(text)
            if dec == "approved":
                b.setProperty("role", "primary")
            b.clicked.connect(lambda _=False, d=dec: self._sign(d))
            row.addWidget(b)
            self.btns[dec] = b
        fl.addLayout(row)
        self.note = muted("")
        fl.addWidget(self.note)
        outer.addWidget(foot)
        self._segs = []
        self._roi = None

    def set_scan(self, project, scan_id):
        self.project, self.scan_id = project, scan_id
        self.compare.blockSignals(True)
        self.compare.setChecked(False)
        self.compare.blockSignals(False)
        self.refresh()

    def set_blinded(self, on: bool):
        self.blinded = bool(on)
        self.blind.blockSignals(True)
        self.blind.setChecked(self.blinded)
        self.blind.blockSignals(False)
        self.refresh()

    def _users(self):
        p = self.project
        return {u["id"]: u for u in p.store.q("SELECT id, username, full_name, role FROM users WHERE org_id=?",
                                              (p.user["org_id"],))}

    def refresh(self, select_id=None):
        from . import services as S
        sel = select_id or (self.selected_segmentation() or {}).get("id")
        self.table.setRowCount(0)
        self.history.setRowCount(0)
        self.detail.clear()
        p = self.project
        if not p or not p.user or self.scan_id is None:
            self.note.setText("Open a scan to review its ROI and segmentations.")
            self.roi_label.setText("")
            for b in list(self.btns.values()) + [self.accept_roi, self.edit_roi, self.compare]:
                b.setEnabled(False)
            return
        users = self._users()
        self._segs = p.store.segmentations(p.user, self.scan_id)
        for s in self._segs:
            revs = p.store.reviews(p.user, "segmentation", s["id"])
            last = revs[-1] if revs else None
            r = self.table.rowCount()
            self.table.insertRow(r)
            dec = ro_item(f"{last['decision'].replace('_', ' ')} ({last['username']})" if last else "not reviewed")
            dec.setForeground(theme.status_color(last["decision"] if last else ""))
            m = S.segmentation_method_info(s)
            meth = ro_item(m["text"], tip=m["provenance"])
            if m["synthetic"]:
                meth.setForeground(theme.qcolor("bad"))
            au = users.get(s["created_by"], {})
            for j, it in enumerate([ro_item(f"v{s['version']}"), ro_item(s["kind"]), meth,
                                    ro_item(au.get("username", s["created_by"])), dec]):
                self.table.setItem(r, j, it)
        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setStretchLastSection(True)
        if self._segs:
            idx = next((i for i, s in enumerate(self._segs) if s["id"] == sel), len(self._segs) - 1)
            self.table.selectRow(idx)
        self._refresh_roi()
        self._update_buttons()

    def _refresh_roi(self):
        from . import services as S
        p = self.project
        seg = self.selected_segmentation() or (self._segs[-1] if self._segs else None)
        rs = S.roi_state(p, seg["roi_id"] if seg else None)
        self._roi = rs
        if rs["roi"] is None:
            self.roi_label.setText("No ROI stored yet. Run the analysis (automatic ROI) or define a manual ROI.")
            return
        r = rs["roi"]
        kind = "manual" if rs["manual"] else "automatic"
        conf = f", confidence {r['confidence']:.2f}" if isinstance(r.get("confidence"), (int, float)) else ""
        col = {"accepted": "ok", "awaiting acceptance": "warn", "rejected": "bad", "needs_changes": "warn"}.get(rs["status"])
        stxt = rs["status"]
        if rs["review"]:
            rv = rs["review"]
            stxt += f" — {rv['decision'].replace('_', ' ')} by {rv['full_name'] or rv['username']} at {rv['created']}"
        colour = theme.tok(col) if col else theme.tok("text_muted")
        why = ("<br>Automatic detection asks for review: check the yellow outline on the slices and the 3D "
               "wireframe, then accept it or edit it." if rs["requires_review"] and not rs["accepted"] else "")
        self.roi_label.setText(f"ROI v{r['version']} ({kind}, {r.get('method') or '-'}{conf})<br>"
                               f"<span style='color:{colour}; font-weight:600'>{stxt}</span>{why}")

    def _update_buttons(self):
        p = self.project
        can = p.can("review")
        seg = self.selected_segmentation()
        why_review = p.why_not("review")
        for d, b in self.btns.items():
            b.setEnabled(can and seg is not None)
            b.setToolTip(why_review)
        if can and seg is not None and seg["created_by"] == p.user["id"]:
            self.btns["approved"].setEnabled(False)
            self.btns["approved"].setToolTip("You created this version. Separation of duties: another reviewer "
                                             "must approve it. You can still request changes or reject.")
        rs = self._roi or {}
        roi = rs.get("roi")
        ok_roi = can and roi is not None and not rs.get("accepted")
        tip = why_review or ("" if roi is not None else "No ROI to accept")
        if roi is not None and rs.get("accepted"):
            tip = "This ROI is already accepted"
        if can and roi is not None and roi["created_by"] == p.user["id"] and not rs.get("accepted"):
            ok_roi = False
            tip = ("You created this ROI (or ran the analysis that created it). Separation of duties: another "
                   "reviewer must accept it.")
        self.accept_roi.setEnabled(ok_roi)
        self.accept_roi.setToolTip(tip)
        self.edit_roi.setEnabled(p.can("write"))
        self.edit_roi.setToolTip(p.why_not("write") or "Define a new cylindrical ROI at the crosshair (saved as a new "
                                                       "ROI version with your reason); then re-run the analysis")
        self.compare.setEnabled(seg is not None and seg.get("parent_id") is not None)
        self.note.setText("Signing requires your password. Authors cannot approve their own segmentations or ROIs "
                          "(separation of duties)." if can else why_review)

    def selected_segmentation(self):
        rows = {i.row() for i in self.table.selectedIndexes()}
        return self._segs[min(rows)] if rows and min(rows) < len(self._segs) else None

    def _sel(self):
        from . import services as S
        self.history.setRowCount(0)
        s = self.selected_segmentation()
        if not s:
            return
        for rv in self.project.store.reviews(self.project.user, "segmentation", s["id"]):
            r = self.history.rowCount()
            self.history.insertRow(r)
            role = S.SIGNATURE_ROLES.get(S.signature_role_of(self.project, rv["id"]) or "", "")
            for j, v in enumerate([rv["created"], rv["full_name"] or rv["username"], role, rv["decision"].replace("_", " "),
                                   rv["meaning"]]):
                self.history.setItem(r, j, ro_item(v, tip=rv.get("comment") or None))
        self.history.resizeColumnsToContents()
        self.history.horizontalHeader().setStretchLastSection(True)
        try:
            self.detail.setHtml(detail_html(S.version_detail(self.project, s["id"])))
        except Exception as e:  # noqa: BLE001
            self.detail.setPlainText(f"Details unavailable: {e}")
        self._refresh_roi()
        self._update_buttons()

    def _sign(self, decision):
        s = self.selected_segmentation()
        if s:
            self.sign_requested.emit("segmentation", s["id"], decision)

    def _accept_roi(self):
        rs = self._roi or {}
        if rs.get("roi") is not None:
            self.sign_requested.emit("roi", rs["roi"]["id"], "approved")


def detail_html(d: dict) -> str:
    """HTML for the version detail pane (parent, editor, reason, per-class change, endpoints)."""
    from html import escape as h
    from .results_view import _fmt
    out = []
    head = f"<b>v{d['version']}</b> ({h(d['kind'])})"
    head += f" derived from <b>v{d['parent_version']}</b>" if d["parent_version"] else " (no parent: automatic result)"
    out.append(head)
    out.append(f"Editor: {h(str(d['author']))}" + (f" ({h(d['author_role'])})" if d.get("author_role") else "")
               + f" &middot; {h(str(d['created']))}")
    m = d.get("method") or {}
    chip = (f" <span style='background:{theme.tok('bad')}; color:{theme.tok('on_bad')}; font-weight:700'>"
            "&nbsp;SYNTHETIC-TRAINED — research only&nbsp;</span>" if m.get("synthetic") else "")
    out.append(f"Method: {h(m.get('short', '-'))}{chip} <span style='color:{theme.tok('text_muted')}'>"
               f"{h(m.get('provenance', ''))}</span>")
    if d["parent_version"]:
        out.append(f"Reason for edit: <b>{h(d['reason']) or '<i>not recorded</i>'}</b>")
        if d["operations"]:
            out.append("Operations: " + ", ".join(f"{h(k)} &times;{v}" for k, v in d["operations"].items()))
        if d["classes"]:
            rows = "".join(f"<tr><td>{h(c['class'])}</td><td align=right>{c['voxels']:+,}</td>"
                           f"<td align=right>{c['mm3']:+.4f}</td></tr>" for c in d["classes"])
            out.append("<table cellspacing=0 cellpadding=2><tr><th align=left>Class</th><th>&Delta; voxels</th>"
                       f"<th>&Delta; mm&sup3;</th></tr>{rows}</table>")
        else:
            out.append("No voxel changes recorded.")
    rows = []
    for e in d["endpoints"]:
        b = "<i>not measured</i>" if e["before"] is None else _fmt(e["before"], e["unit"])
        a = "<i>not measured</i>" if e["after"] is None else _fmt(e["after"], e["unit"])
        tip = h("; ".join(e["reasons"]))
        rows.append(f"<tr><td>{h(e['label'])} ({h(e['unit'])})</td><td align=right>{b}</td><td>&rarr;</td>"
                    f"<td align=right title='{tip}'>{a}</td><td>{h(e['after_status'])}</td></tr>")
    out.append("<table cellspacing=0 cellpadding=2><tr><th align=left>Endpoint</th><th>"
               + ("parent" if d["parent_version"] else "-") + "</th><th></th><th>this version</th><th>status</th></tr>"
               + "".join(rows) + "</table>")
    return "<br>".join(out)


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
        self.export_btn = QPushButton("Export...")
        self.export_btn.setToolTip("Export the audit trail to CSV or JSON together with the chain-verification result")
        self.export_btn.clicked.connect(lambda: self.export())
        top.addWidget(rb)
        top.addWidget(self.export_btn)
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
        self.blinded = False

    def set_project(self, project):
        self.project = project
        self.refresh()

    def set_blinded(self, on: bool):
        self.blinded = bool(on)
        self.refresh()

    def export(self, path=None):
        from . import services as S
        from .messages import show_error
        p = self.project
        if not p:
            return None
        if path is None:
            path, _ = QFileDialog.getSaveFileName(self, "Export audit trail", "audit_trail.csv",
                                                  "CSV (*.csv);;JSON (*.json)")
            if not path:
                return None
        try:
            res = S.export_audit(p, path, blinded=self.blinded)
        except (PermissionError, OSError) as e:
            show_error(self, "Audit trail not exported", e)
            return None
        v = res["verification"]
        set_banner(self.result, f"Exported {res['events']} events to {res['path']}. Chain verification: "
                                + ("OK" if v["ok"] else f"BROKEN at event {v['first_bad_seq']}"), "ok" if v["ok"] else "bad")
        return res

    def refresh(self):
        self.table.setRowCount(0)
        p = self.project
        if not p or not p.user:
            return
        allowed = p.can("review") or p.can("manage_users")
        self.export_btn.setEnabled(allowed)
        self.export_btn.setToolTip("Export the audit trail to CSV or JSON together with the chain-verification result"
                                   if allowed else "Requires the reviewer, study director or administrator role")
        if not allowed:
            set_banner(self.result, "Viewing the audit trail requires the reviewer, study director or administrator "
                                    "role. Chain verification is available to all users.", "warn")
            self._events = []
            return
        ot = self.otype.currentText()
        self._events = p.store.audit.events(org_id=p.user["org_id"], object_type=None if ot == "All objects" else ot,
                                            limit=5000)
        if self.blinded:      # mask file names, paths, animal IDs, acquisition metadata and scan IDs (UX-09)
            from .blinding import Masker
            mk = Masker(p)
            self._events = [mk.event(e) for e in self._events]
            set_banner(self.result, "Blinded review mode: file names, animal IDs, acquisition metadata and scan IDs "
                                    "are masked in this view.", "info")
        users = {str(u["id"]): u["username"] for u in p.store.q("SELECT id, username FROM users")}
        for e in self._events:
            r = self.table.rowCount()
            self.table.insertRow(r)
            obj = e.get("object_label") or f"{e['object_type'] or ''} {e['object_id'] or ''}".strip()
            for j, v in enumerate([e["seq"], e["ts"].replace("T", " ")[:23], users.get(e["user_id"], e["user_id"] or "system"),
                                   e["action"], obj, e["row_hash"][:16]]):
                self.table.setItem(r, j, ro_item(v))
        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setStretchLastSection(True)
        self._apply_filter()
        if self._events:
            self.table.selectRow(0)

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
