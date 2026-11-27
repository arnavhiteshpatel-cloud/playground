"""Import wizard: source -> metadata and voxel spacing -> assignment -> import + QC.

``ImportModel`` holds all the logic (candidate discovery, spacing rules, assignment, running
the imports) and is unit-tested without widgets. ``ImportWizard`` is a thin QWizard on top.

Rules enforced here:
  * voxel spacing must be entered/confirmed explicitly whenever it is not reliably in the file;
  * nothing is silently dropped: unreadable files, user-excluded files and duplicates are
    imported as *rejected* entries in the project's import log (visible in the project tree)
    with their reason; scans failing QC are imported and *flagged*.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QAbstractItemView, QCheckBox, QComboBox, QDoubleSpinBox, QFileDialog, QHBoxLayout,
                               QHeaderView, QLabel, QMessageBox, QProgressBar, QPushButton, QSplitter,
                               QVBoxLayout, QWidget, QWizard, QWizardPage)

from . import services as S
from . import theme
from .panels import fill_qc_tables, make_table, muted, ro_item, section, set_banner

ANIMAL_RE = re.compile(r"^[A-Za-z0-9_.\-]{1,64}$")


def guess_animal_id(path: Path) -> str:
    stem = path.name
    for suf in (".nii.gz", ".ome.tiff", ".ome.tif"):
        if stem.lower().endswith(suf):
            stem = stem[: -len(suf)]
            break
    else:
        stem = path.stem if path.is_file() else path.name
    stem = re.sub(r"[^A-Za-z0-9_.\-]", "_", stem)[:64]
    return stem or "animal"


@dataclass
class Candidate:
    path: Path
    probe: S.SourceProbe
    include: bool = True
    spacing: list | None = None
    confirmed: bool = False
    animal_id: str = ""
    group_id: int | None = None
    timepoint: str = ""
    days: float | None = None
    outcome: S.ImportOutcome | None = None
    notes: list = field(default_factory=list)

    @property
    def readable(self) -> bool:
        return self.probe.ok

    @property
    def needs_spacing(self) -> bool:
        return self.probe.spacing_needs_entry


class ImportModel:
    def __init__(self, project, study_id: int | None = None):
        self.project = project
        self.study_id = study_id
        self.candidates: list[Candidate] = []

    # ------------------------------------------------------------------ sources
    def add_path(self, path) -> list[Candidate]:
        added = []
        known = {c.path.resolve() for c in self.candidates}
        found = S.find_candidates(path)
        if not found:
            found = [Path(path)]          # keep it: it will be shown and logged as unreadable
        for p in found:
            if p.resolve() in known:
                continue
            pr = S.probe_source(p)
            c = Candidate(p, pr, spacing=list(pr.spacing_um) if pr.spacing_um else None,
                          confirmed=pr.spacing_source == "file", animal_id=guess_animal_id(p))
            self.candidates.append(c)
            added.append(c)
        return added

    def remove(self, index: int):
        del self.candidates[index]

    # ------------------------------------------------------------------ spacing
    def set_spacing(self, index: int, values, confirmed: bool = True):
        c = self.candidates[index]
        c.spacing = list(S.validate_spacing(values))
        c.confirmed = bool(confirmed)

    def apply_spacing_to_all(self, values, only_missing: bool = True):
        sp = list(S.validate_spacing(values))
        for c in self.candidates:
            if c.readable and (not only_missing or c.needs_spacing):
                c.spacing = list(sp)
                c.confirmed = True

    # ------------------------------------------------------------------ validation
    def problems(self) -> list[str]:
        out = []
        if self.study_id is None:
            out.append("Choose the study to import into.")
        if not self.candidates:
            out.append("Add at least one file or folder.")
        for c in self.candidates:
            if not (c.include and c.readable):
                continue
            if not c.spacing:
                out.append(f"{c.path.name}: enter the voxel spacing (not found in the file).")
            elif c.needs_spacing and not c.confirmed:
                out.append(f"{c.path.name}: confirm the voxel spacing (the file does not record it reliably).")
            else:
                try:
                    S.validate_spacing(c.spacing)
                except ValueError as e:
                    out.append(f"{c.path.name}: {e}")
        return out

    def assignment_problems(self) -> list[str]:
        out = []
        for c in self.candidates:
            if c.include and c.readable and c.animal_id and not ANIMAL_RE.match(c.animal_id):
                out.append(f"{c.path.name}: animal ID may contain letters, digits, '.', '_' and '-' only.")
        return out

    # ------------------------------------------------------------------ execution
    def run(self, ctx=None) -> list[S.ImportOutcome]:
        ctx = ctx or S.NullContext()
        probs = self.problems() + self.assignment_problems()
        if probs:
            raise ValueError("; ".join(probs))
        n = len(self.candidates)
        outcomes = []
        for i, c in enumerate(self.candidates):
            base = i / n

            class _Sub:
                def progress(self_, f, m=""):
                    ctx.progress(base + f / n, f"{c.path.name}: {m}")

                def check(self_):
                    ctx.check()

            ctx.check()
            if not c.include:
                reason = "excluded by the user in the import wizard"
                self.project.log_import(self.study_id, c.path, "rejected", reason)
                c.outcome = S.ImportOutcome(str(c.path), "rejected", reason)
            elif not c.readable:
                reason = f"Unreadable: {c.probe.error}"
                self.project.log_import(self.study_id, c.path, "rejected", reason)
                c.outcome = S.ImportOutcome(str(c.path), "rejected", reason)
            else:
                spec = S.get_or_create_specimen(self.project, self.study_id, c.animal_id, c.group_id) if c.animal_id else None
                tp = S.get_or_create_timepoint(self.project, self.study_id, c.timepoint, c.days) if c.timepoint else None
                req = S.ImportRequest(str(c.path), tuple(c.spacing), c.confirmed or not c.needs_spacing,
                                      self.study_id, spec, tp, {"imported_with": "desktop wizard"})
                c.outcome = S.import_scan(self.project, req, _Sub(), probe=c.probe)
            outcomes.append(c.outcome)
        ctx.progress(1.0, "import finished")
        return outcomes


# ============================================================================ widgets
class SourcePage(QWizardPage):
    def __init__(self, model: ImportModel, studies: list[dict]):
        super().__init__()
        self.model = model
        self.setTitle("Select scans")
        self.setSubTitle("Choose reconstructed volumes: TXM/TXRM, DICOM series, NIfTI, NRRD, Zarr, TIFF (single file "
                         "or slice stack), MetaImage or NumPy. A folder may hold one series or several volumes.")
        lay = QVBoxLayout(self)
        row = QHBoxLayout()
        row.addWidget(QLabel("Import into study"))
        self.study = QComboBox()
        for s in studies:
            self.study.addItem(s["name"], s["id"])
            if s["id"] == model.study_id:
                self.study.setCurrentIndex(self.study.count() - 1)
        self.study.currentIndexChanged.connect(self._study)
        row.addWidget(self.study, 1)
        lay.addLayout(row)
        btns = QHBoxLayout()
        b1, b2, b3 = QPushButton("Add files..."), QPushButton("Add folder..."), QPushButton("Remove selected")
        b1.clicked.connect(self._files)
        b2.clicked.connect(self._folder)
        b3.clicked.connect(self._remove)
        for b in (b1, b2, b3):
            btns.addWidget(b)
        btns.addStretch(1)
        lay.addLayout(btns)
        self.table = make_table(["Source", "Format", "Dimensions (z, y, x)", "Size", "Status"])
        lay.addWidget(self.table, 1)
        self._study()

    def _study(self):
        self.model.study_id = self.study.currentData()
        self.completeChanged.emit()

    def _files(self):
        fs, _ = QFileDialog.getOpenFileNames(self, "Select volume files")
        for f in fs:
            self.add(f)

    def _folder(self):
        d = QFileDialog.getExistingDirectory(self, "Select a folder (series, stack or several volumes)")
        if d:
            self.add(d)

    def add(self, path):
        self.model.add_path(path)
        self.refresh()

    def _remove(self):
        rows = sorted({i.row() for i in self.table.selectedIndexes()}, reverse=True)
        for r in rows:
            self.model.remove(r)
        self.refresh()

    def refresh(self):
        t = self.table
        t.setRowCount(0)
        for c in self.model.candidates:
            r = t.rowCount()
            t.insertRow(r)
            pr = c.probe
            st = ro_item("readable" if pr.ok else f"unreadable: {pr.error}", tip=pr.error or "")
            st.setForeground(theme.status_color("suitable" if pr.ok else "rejected"))
            for j, it in enumerate([ro_item(c.path.name, tip=str(c.path)), ro_item(pr.format or "-"),
                                    ro_item(" x ".join(map(str, pr.shape)) if pr.shape else "-"),
                                    ro_item(f"{pr.size_bytes / 1e6:,.1f} MB" if pr.size_bytes else "-"), st]):
                t.setItem(r, j, it)
        t.resizeColumnsToContents()
        t.horizontalHeader().setStretchLastSection(True)
        self.completeChanged.emit()

    def isComplete(self):
        return bool(self.model.candidates) and self.model.study_id is not None


class MetadataPage(QWizardPage):
    def __init__(self, model: ImportModel):
        super().__init__()
        self.model = model
        self.setTitle("Metadata and voxel spacing")
        self.setSubTitle("Check the metadata found in each file. Voxel spacing (µm) determines every physical "
                         "measurement; where the file does not record it reliably you must enter and confirm it.")
        lay = QVBoxLayout(self)
        allrow = QHBoxLayout()
        allrow.addWidget(QLabel("Spacing for all scans without file spacing (µm):"))
        self.all_sp = QDoubleSpinBox()
        self.all_sp.setRange(0.1, 5000)
        self.all_sp.setDecimals(3)
        self.all_sp.setValue(10.0)
        b = QPushButton("Apply and confirm")
        b.clicked.connect(self._apply_all)
        allrow.addWidget(self.all_sp)
        allrow.addWidget(b)
        allrow.addStretch(1)
        lay.addLayout(allrow)
        split = QSplitter(Qt.Vertical)
        self.table = make_table(["Source", "Spacing source", "z (µm)", "y (µm)", "x (µm)", "Confirmed", "Warnings"])
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.itemSelectionChanged.connect(self._details)
        split.addWidget(self.table)
        det = QWidget()
        dl = QVBoxLayout(det)
        dl.setContentsMargins(0, 4, 0, 0)
        dl.addWidget(section("Metadata of selected scan"))
        self.meta = make_table(["Field", "Value"])
        dl.addWidget(self.meta)
        split.addWidget(det)
        split.setSizes([260, 180])
        lay.addWidget(split, 1)
        self.problems = QLabel("")
        self.problems.setWordWrap(True)
        lay.addWidget(self.problems)

    def initializePage(self):
        self.refresh()

    def refresh(self):
        t = self.table
        t.setRowCount(0)
        for i, c in enumerate(self.model.candidates):
            r = t.rowCount()
            t.insertRow(r)
            t.setItem(r, 0, ro_item(c.path.name, tip=str(c.path)))
            if not c.readable:
                it = ro_item("unreadable - will be listed as rejected")
                it.setForeground(theme.status_color("rejected"))
                t.setItem(r, 1, it)
                continue
            src = {"file": "file metadata", "assumed": "ASSUMED by reader", "missing": "MISSING"}[c.probe.spacing_source]
            it = ro_item(src)
            it.setForeground(theme.status_color("suitable" if c.probe.spacing_source == "file" else "review"))
            t.setItem(r, 1, it)
            for j in range(3):
                sb = QDoubleSpinBox()
                sb.setRange(0, 5000)
                sb.setDecimals(3)
                sb.setSpecialValueText("enter")
                sb.setValue(c.spacing[j] if c.spacing else 0)
                sb.valueChanged.connect(lambda _v, i=i: self._edited(i))
                t.setCellWidget(r, 2 + j, sb)
            cb = QCheckBox()
            cb.setChecked(c.confirmed)
            cb.setEnabled(c.needs_spacing)
            cb.toggled.connect(lambda on, i=i: self._confirm(i, on))
            t.setCellWidget(r, 5, cb)
            t.setItem(r, 6, ro_item("; ".join(c.probe.warnings)[:200], tip="\n".join(c.probe.warnings)))
        t.resizeColumnsToContents()
        t.horizontalHeader().setStretchLastSection(True)
        if self.model.candidates:
            t.selectRow(0)
        self._update_problems()

    def _values(self, i):
        return [self.table.cellWidget(i, 2 + j).value() for j in range(3)]

    def _edited(self, i):
        c = self.model.candidates[i]
        vals = self._values(i)
        if all(v > 0 for v in vals):
            changed = c.spacing is None or any(abs(a - b) > 1e-9 for a, b in zip(vals, c.spacing))
            c.spacing = vals
            if changed and c.probe.spacing_source == "file":
                c.notes.append("spacing overridden by user")
        else:
            c.spacing = None
        self._update_problems()

    def _confirm(self, i, on):
        self.model.candidates[i].confirmed = bool(on)
        self._update_problems()

    def _apply_all(self):
        self.model.apply_spacing_to_all([self.all_sp.value()] * 3)
        self.refresh()

    def _details(self):
        rows = {i.row() for i in self.table.selectedIndexes()}
        self.meta.setRowCount(0)
        if not rows:
            return
        c = self.model.candidates[min(rows)]
        items = c.probe.summary_rows() if c.readable else [("Error", c.probe.error or "")]
        for k, v in items:
            r = self.meta.rowCount()
            self.meta.insertRow(r)
            self.meta.setItem(r, 0, ro_item(k))
            self.meta.setItem(r, 1, ro_item(v, tip=v))
        self.meta.resizeColumnToContents(0)

    def _update_problems(self):
        p = self.model.problems()
        if p:
            set_banner(self.problems, "\n".join(p[:6]) + ("\n..." if len(p) > 6 else ""), "warn")
        else:
            set_banner(self.problems, "Voxel spacing is defined for every readable scan.", "ok")
        self.completeChanged.emit()

    def isComplete(self):
        return not self.model.problems()


class AssignmentPage(QWizardPage):
    def __init__(self, model: ImportModel):
        super().__init__()
        self.model = model
        self.setTitle("Assign to animals and timepoints")
        self.setSubTitle("Each scan belongs to an animal (specimen) and a timepoint in the study. New animal IDs and "
                         "timepoints are created. Unchecked scans are not imported but are listed as rejected.")
        lay = QVBoxLayout(self)
        self.table = make_table(["Import", "Source", "Animal ID", "Group", "Timepoint", "Days"])
        lay.addWidget(self.table, 1)
        self.problems = QLabel("")
        self.problems.setWordWrap(True)
        lay.addWidget(self.problems)

    def initializePage(self):
        p = self.model.project
        sid = self.model.study_id
        groups = p.store.groups(p.user, sid)
        tps = p.timepoints(sid)
        t = self.table
        t.setRowCount(0)
        for i, c in enumerate(self.model.candidates):
            r = t.rowCount()
            t.insertRow(r)
            inc = QCheckBox()
            inc.setChecked(c.include and c.readable)
            inc.setEnabled(c.readable)
            inc.toggled.connect(lambda on, c=c: (setattr(c, "include", on), self._update()))
            t.setCellWidget(r, 0, inc)
            t.setItem(r, 1, ro_item(c.path.name, tip=str(c.path)))
            if not c.readable:
                it = ro_item("unreadable - listed as rejected")
                it.setForeground(theme.status_color("rejected"))
                t.setItem(r, 2, it)
                continue
            animal = QComboBox()
            animal.setEditable(True)
            existing = [s["animal_id"] for s in p.store.specimens(p.user, sid)]
            animal.addItems(existing)
            animal.setCurrentText(c.animal_id)
            animal.currentTextChanged.connect(lambda txt, c=c: (setattr(c, "animal_id", txt.strip()), self._update()))
            t.setCellWidget(r, 2, animal)
            grp = QComboBox()
            grp.addItem("(none)", None)
            for g in groups:
                grp.addItem(g["name"], g["id"])
            grp.currentIndexChanged.connect(lambda _i, c=c, w=grp: setattr(c, "group_id", w.currentData()))
            t.setCellWidget(r, 3, grp)
            tp = QComboBox()
            tp.setEditable(True)
            tp.addItems([x["label"] for x in tps])
            tp.setCurrentText(c.timepoint)
            tp.currentTextChanged.connect(lambda txt, c=c: setattr(c, "timepoint", txt.strip()))
            t.setCellWidget(r, 4, tp)
            days = QDoubleSpinBox()
            days.setRange(-1, 10000)
            days.setDecimals(0)
            days.setSpecialValueText("-")
            days.setValue(c.days if c.days is not None else -1)
            days.valueChanged.connect(lambda v, c=c: setattr(c, "days", None if v < 0 else v))
            t.setCellWidget(r, 5, days)
        t.resizeColumnsToContents()
        t.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self._update()

    def _update(self):
        p = self.model.assignment_problems()
        excluded = sum(1 for c in self.model.candidates if not (c.include and c.readable))
        if p:
            set_banner(self.problems, "\n".join(p), "warn")
        else:
            set_banner(self.problems, f"{sum(1 for c in self.model.candidates if c.include and c.readable)} scan(s) "
                                      f"will be imported; {excluded} will be listed as rejected.", "info")
        self.completeChanged.emit()

    def isComplete(self):
        return not self.model.assignment_problems()


class RunPage(QWizardPage):
    def __init__(self, model: ImportModel, jobs):
        super().__init__()
        self.model, self.jobs = model, jobs
        self.job = None
        self.setTitle("Import and quality control")
        self.setSubTitle("Scans are copied into the project's chunked store with SHA-256 provenance, then QC runs. "
                         "Deterministic checks are facts about the file; heuristic checks use developer thresholds.")
        lay = QVBoxLayout(self)
        row = QHBoxLayout()
        self.start = QPushButton("Start import")
        self.start.setProperty("role", "primary")
        self.start.clicked.connect(self.run)
        self.cancel = QPushButton("Cancel")
        self.cancel.setEnabled(False)
        self.cancel.clicked.connect(lambda: self.job and self.jobs.cancel(self.job.id))
        self.bar = QProgressBar()
        self.bar.setRange(0, 1000)
        self.msg = muted("")
        row.addWidget(self.start)
        row.addWidget(self.cancel)
        row.addWidget(self.bar, 1)
        lay.addLayout(row)
        lay.addWidget(self.msg)
        split = QSplitter(Qt.Vertical)
        self.results = make_table(["Source", "Result", "Scan", "Reason"])
        self.results.itemSelectionChanged.connect(self._show_qc)
        split.addWidget(self.results)
        qcw = QWidget()
        ql = QHBoxLayout(qcw)
        ql.setContentsMargins(0, 4, 0, 0)
        l1, l2 = QVBoxLayout(), QVBoxLayout()
        l1.addWidget(section("Deterministic checks"))
        self.det = make_table(["ID", "Check", "Status", "Value", "Message"])
        l1.addWidget(self.det)
        l2.addWidget(section("Heuristic checks"))
        self.heu = make_table(["ID", "Check", "Status", "Value", "Message"])
        l2.addWidget(self.heu)
        ql.addLayout(l1)
        ql.addLayout(l2)
        split.addWidget(qcw)
        lay.addWidget(split, 1)
        self.finished_ok = False

    def run(self):
        self.start.setEnabled(False)
        self.cancel.setEnabled(True)
        self.job = self.jobs.submit("import", f"Import {len(self.model.candidates)} scan(s)", self.model.run,
                                    on_done=self._finished)
        self.jobs.job_changed.connect(self._progress)

    def _progress(self, job):
        if self.job is not None and job.id == self.job.id:
            self.bar.setValue(int(job.progress * 1000))
            self.msg.setText(job.message)

    def _finished(self, job):
        self.cancel.setEnabled(False)
        self.finished_ok = True
        if job.status == "failed":
            self.msg.setText(f"Import failed: {job.error}")
        elif job.status == "cancelled":
            self.msg.setText("Import cancelled. Scans completed before cancellation remain in the project.")
        else:
            self.msg.setText("Import finished.")
        self.fill()
        self.completeChanged.emit()

    def fill(self):
        t = self.results
        t.setRowCount(0)
        for c in self.model.candidates:
            o = c.outcome
            r = t.rowCount()
            t.insertRow(r)
            st = ro_item(o.status if o else "not processed")
            st.setForeground(theme.status_color(o.status if o else "cancelled"))
            for j, it in enumerate([ro_item(c.path.name, tip=str(c.path)), st, ro_item(o.scan_id if o else ""),
                                    ro_item(o.reason if o else "", tip=o.reason if o else "")]):
                t.setItem(r, j, it)
        t.resizeColumnsToContents()
        t.horizontalHeader().setStretchLastSection(True)
        if t.rowCount():
            t.selectRow(0)

    def _show_qc(self):
        rows = {i.row() for i in self.results.selectedIndexes()}
        for tb in (self.det, self.heu):
            tb.setRowCount(0)
        if rows:
            c = self.model.candidates[min(rows)]
            if c.outcome and c.outcome.qc:
                fill_qc_tables(c.outcome.qc, self.det, self.heu)

    def isComplete(self):
        return self.finished_ok


class ImportWizard(QWizard):
    def __init__(self, project, jobs, study_id=None, parent=None, initial_paths=()):
        super().__init__(parent)
        self.setWindowTitle("Import scans")
        self.setWizardStyle(QWizard.ModernStyle)
        self.setOption(QWizard.NoBackButtonOnLastPage, True)
        self.setOption(QWizard.NoCancelButtonOnLastPage, True)
        self.resize(940, 620)
        self.model = ImportModel(project, study_id)
        studies = project.store.list_studies(project.user)
        if self.model.study_id is None and studies:
            self.model.study_id = studies[0]["id"]
        self.src = SourcePage(self.model, studies)
        self.meta = MetadataPage(self.model)
        self.assign = AssignmentPage(self.model)
        self.runp = RunPage(self.model, jobs)
        for p in (self.src, self.meta, self.assign, self.runp):
            self.addPage(p)
        for pth in initial_paths:
            self.src.add(pth)

    def reject(self):
        if self.runp.job is not None and self.runp.job.active:
            QMessageBox.information(self, "Import running", "Cancel the running import first.")
            return
        super().reject()
