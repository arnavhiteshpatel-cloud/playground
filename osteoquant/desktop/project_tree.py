"""Project tree: studies -> groups -> animals -> timepoints -> scans (+ rejected imports)."""
from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QAbstractItemView, QHeaderView, QMenu, QTreeWidget, QTreeWidgetItem

from . import theme
from .panels import dot

ROLE = Qt.UserRole + 1

STATUS_TEXT = {"imported": "imported", "qc_suitable": "QC suitable", "qc_review": "QC review", "qc_unsuitable": "QC unsuitable",
               "analyzed": "analysed", "needs_manual_roi": "needs ROI", "rejected": "rejected"}


class ProjectTree(QTreeWidget):
    scan_activated = Signal(int)
    selection_changed_ = Signal()
    context_action = Signal(str, dict)      # action, node

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHeaderLabels(["Name", "Status"])
        self.setColumnCount(2)
        self.header().setSectionResizeMode(0, QHeaderView.Stretch)
        self.header().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.header().setStretchLastSection(False)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setUniformRowHeights(True)
        self.setAnimated(False)
        self.setIndentation(14)
        self.itemDoubleClicked.connect(self._activated)
        self.itemSelectionChanged.connect(self.selection_changed_)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._menu)

    def populate(self, tree: list[dict], keep_selection=True):
        sel = {(n["kind"], n["id"]) for n in self.selected_nodes()} if keep_selection else set()
        expanded = set()
        it = self._iter()
        for item in it:
            if item.isExpanded():
                n = item.data(0, ROLE)
                expanded.add((n["kind"], n["id"], n.get("name")))
        first = self.topLevelItemCount() == 0
        self.clear()

        def add(parent, node):
            item = QTreeWidgetItem([node["name"], ""])
            item.setData(0, ROLE, node)
            k = node["kind"]
            if k == "scan":
                v = node.get("qc_verdict") or ""
                item.setIcon(0, dot(theme.status_color(v or "queued")))
                item.setText(1, STATUS_TEXT.get(node["status"], node["status"]))
                item.setToolTip(0, f"{node['name'] if node.get('blinded') else 'Scan ' + str(node['id'])} · "
                                   f"{' x '.join(map(str, node['shape']))} voxels · "
                                   f"{', '.join(f'{s:g}' for s in node['spacing_um'])} µm · QC {v or 'not run'}")
                item.setForeground(1, theme.status_color(v or ""))
            elif k == "rejected":
                item.setIcon(0, dot(theme.status_color("rejected")))
                item.setText(1, "rejected")
                item.setToolTip(0, node.get("reason", ""))
                item.setForeground(1, theme.status_color("rejected"))
            elif k == "study":
                f = item.font(0)
                f.setBold(True)
                item.setFont(0, f)
                if node.get("blinded"):
                    item.setText(1, "blinded")
            elif k == "rejected_folder":
                item.setForeground(0, theme.status_color("rejected"))
            for ch in node.get("children", []):
                add(item, ch)
            if parent is None:
                self.addTopLevelItem(item)
            else:
                parent.addChild(item)
            if first or (k, node["id"], node.get("name")) in expanded:
                item.setExpanded(k not in ("rejected_folder",))
            if (k, node["id"]) in sel:
                item.setSelected(True)

        for n in tree:
            add(None, n)

    def _iter(self):
        out = []

        def walk(item):
            out.append(item)
            for i in range(item.childCount()):
                walk(item.child(i))
        for i in range(self.topLevelItemCount()):
            walk(self.topLevelItem(i))
        return out

    def selected_nodes(self) -> list[dict]:
        return [i.data(0, ROLE) for i in self.selectedItems() if i.data(0, ROLE)]

    def selected_scan_ids(self) -> list[int]:
        """Scans selected directly or contained in selected study/group/animal/timepoint nodes."""
        ids = []

        def collect(item):
            n = item.data(0, ROLE)
            if n and n["kind"] == "scan" and n["id"] not in ids:
                ids.append(n["id"])
            for i in range(item.childCount()):
                collect(item.child(i))
        for it in self.selectedItems():
            collect(it)
        return ids

    def current_study_id(self) -> int | None:
        it = self.currentItem() or (self.selectedItems()[0] if self.selectedItems() else None)
        while it is not None:
            n = it.data(0, ROLE)
            if n and n["kind"] == "study":
                return n["id"]
            it = it.parent()
        if self.topLevelItemCount():
            return self.topLevelItem(0).data(0, ROLE)["id"]
        return None

    def select_scan(self, scan_id: int):
        for it in self._iter():
            n = it.data(0, ROLE)
            if n and n["kind"] == "scan" and n["id"] == scan_id:
                self.setCurrentItem(it)
                return

    def _activated(self, item, _col):
        n = item.data(0, ROLE)
        if n and n["kind"] == "scan":
            self.scan_activated.emit(n["id"])

    def _menu(self, pos):
        item = self.itemAt(pos)
        n = item.data(0, ROLE) if item else None
        m = QMenu(self)
        acts = []
        if n is None:
            acts = [("new_study", "New study...")]
        elif n["kind"] == "study":
            acts = [("import", "Import scans into this study..."), ("add_group", "Add group..."),
                    ("analyze", "Analyse all scans..."), ("report", "Generate report"), (None, None),
                    ("new_study", "New study...")]
        elif n["kind"] == "scan":
            acts = [("open", "Open in viewer"), ("analyze", "Analyse..."), ("qc", "Show QC")]
        elif n["kind"] in ("group", "animal", "timepoint"):
            acts = [("analyze", "Analyse scans..."), ("import", "Import scans...")]
        elif n["kind"] == "rejected":
            acts = [("show_reason", "Show rejection reason")]
        for key, text in acts:
            if key is None:
                m.addSeparator()
                continue
            a = m.addAction(text)
            a.triggered.connect(lambda _=False, k=key, node=n: self.context_action.emit(k, node or {}))
        if acts:
            m.exec(self.viewport().mapToGlobal(pos))
