"""Modal dialogs: project creation, sign-in, study, analysis settings, ROI, label revision,
electronic signature, licence and About."""
from __future__ import annotations

import datetime as dt
import importlib.metadata as md
import platform
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QCheckBox, QComboBox, QDialog, QDialogButtonBox, QDoubleSpinBox, QFileDialog,
                               QFormLayout, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPlainTextEdit,
                               QPushButton, QTableWidget, QTabWidget, QVBoxLayout, QWidget)

from .. import __version__
from ..licensing import LicenceStatus
from .panels import make_table, muted, ro_item, set_banner
from .services import GRAFT_MATERIALS

APP_NAME = "OsteoQuant Desktop"


def _buttons(dlg, ok_text="OK", primary=True):
    bb = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    ok = bb.button(QDialogButtonBox.Ok)
    ok.setText(ok_text)
    if primary:
        ok.setProperty("role", "primary")
    bb.accepted.connect(dlg.accept)
    bb.rejected.connect(dlg.reject)
    return bb


class _Dialog(QDialog):
    def __init__(self, title, parent=None, width=440):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumWidth(width)
        self.lay = QVBoxLayout(self)
        self.lay.setContentsMargins(16, 14, 16, 12)
        self.lay.setSpacing(10)
        self.error = QLabel("")
        self.error.setWordWrap(True)
        self.error.hide()

    def show_error(self, msg):
        set_banner(self.error, msg, "bad")
        self.error.show()


class NewProjectDialog(_Dialog):
    def __init__(self, parent=None, default_dir: str = ""):
        super().__init__("New project", parent, 520)
        self.lay.addWidget(muted("A project is a folder holding the study database, imported scans, label revisions, "
                                 "reports and the audit trail. You become its administrator."))
        f = QFormLayout()
        self.name = QLineEdit()
        self.name.setPlaceholderText("e.g. Rabbit condyle beta-TCP 2026")
        self.folder = QLineEdit(default_dir)
        browse = QPushButton("Browse...")
        browse.clicked.connect(self._browse)
        row = QHBoxLayout()
        row.addWidget(self.folder, 1)
        row.addWidget(browse)
        self.user = QLineEdit()
        self.full = QLineEdit()
        self.pw1, self.pw2 = QLineEdit(), QLineEdit()
        for p in (self.pw1, self.pw2):
            p.setEchoMode(QLineEdit.Password)
        f.addRow("Project name", self.name)
        f.addRow("Folder", row)
        f.addRow("User name", self.user)
        f.addRow("Full name", self.full)
        f.addRow("Password", self.pw1)
        f.addRow("Repeat password", self.pw2)
        self.lay.addLayout(f)
        self.lay.addWidget(muted("Password: at least 10 characters with an upper-case letter and a digit."))
        self.lay.addWidget(self.error)
        self.lay.addWidget(_buttons(self, "Create project"))

    def _browse(self):
        d = QFileDialog.getExistingDirectory(self, "Choose a parent folder for the project")
        if d:
            name = self.name.text().strip() or "OsteoQuant project"
            safe = "".join(ch if ch.isalnum() or ch in "-_ " else "_" for ch in name).strip().replace(" ", "_")
            self.folder.setText(str(Path(d) / safe))

    def accept(self):
        if not self.name.text().strip() or not self.folder.text().strip() or not self.user.text().strip():
            return self.show_error("Project name, folder and user name are required.")
        if self.pw1.text() != self.pw2.text():
            return self.show_error("The passwords do not match.")
        super().accept()

    def values(self):
        return dict(folder=self.folder.text().strip(), name=self.name.text().strip(), username=self.user.text().strip(),
                    password=self.pw1.text(), full_name=self.full.text().strip())


class LoginDialog(_Dialog):
    def __init__(self, project_name: str, last_user: str = "", parent=None):
        super().__init__("Sign in", parent, 380)
        t = QLabel(project_name)
        t.setProperty("role", "heading")
        self.lay.addWidget(t)
        self.lay.addWidget(muted("Sign in with your project account. All actions are recorded in the audit trail "
                                 "under this identity."))
        f = QFormLayout()
        self.user = QLineEdit(last_user)
        self.pw = QLineEdit()
        self.pw.setEchoMode(QLineEdit.Password)
        f.addRow("User name", self.user)
        f.addRow("Password", self.pw)
        self.lay.addLayout(f)
        self.lay.addWidget(self.error)
        self.lay.addWidget(_buttons(self, "Sign in"))
        (self.pw if last_user else self.user).setFocus()


class NewStudyDialog(_Dialog):
    def __init__(self, parent=None):
        super().__init__("New study", parent)
        f = QFormLayout()
        self.name = QLineEdit()
        self.species = QComboBox()
        self.species.setEditable(True)
        self.species.addItems(["rabbit", "rat", "mouse", "sheep", "pig", "dog", "minipig"])
        self.model = QComboBox()
        self.model.addItems(["condyle", "calvarial", "segmental"])
        self.material = QLineEdit()
        self.material.setPlaceholderText("e.g. beta-TCP, HA")
        self.blinded = QCheckBox("Blinded study (group allocation hidden from non-administrators)")
        f.addRow("Name", self.name)
        f.addRow("Species", self.species)
        f.addRow("Defect model", self.model)
        f.addRow("Graft material(s)", self.material)
        f.addRow("", self.blinded)
        self.lay.addLayout(f)
        self.lay.addWidget(self.error)
        self.lay.addWidget(_buttons(self, "Create study"))

    def accept(self):
        if not self.name.text().strip():
            return self.show_error("A study name is required.")
        super().accept()

    def values(self):
        return dict(name=self.name.text().strip(), species=self.species.currentText().strip(),
                    defect_model=self.model.currentText(), graft_materials=self.material.text().strip(),
                    blinded=self.blinded.isChecked())


class AnalysisDialog(_Dialog):
    def __init__(self, n_scans: int, defect_model: str = "condyle", parent=None):
        super().__init__("Run DefectFill analysis", parent, 480)
        self.lay.addWidget(muted(f"{n_scans} scan(s) selected. Each scan runs as a background job; you can keep "
                                 "working and cancel from the Jobs panel."))
        f = QFormLayout()
        self.model = QComboBox()
        self.model.addItems(["condyle", "calvarial", "segmental"])
        if defect_model in ("condyle", "calvarial", "segmental"):
            self.model.setCurrentText(defect_model)
        self.diam = QDoubleSpinBox()
        self.diam.setRange(0, 50000)
        self.diam.setDecimals(0)
        self.diam.setSuffix(" µm")
        self.diam.setSpecialValueText("not specified")
        self.seg = QComboBox()
        self.seg.addItem("Multi-Otsu (classical, material-aware)", "multiotsu")
        from .services import SYNTHETIC_CHIP, available_models
        self._synthetic = {}
        for m in available_models():
            label = f"U-Net {m['name']} (locked model)" + (f" — {SYNTHETIC_CHIP}" if m.get("synthetic") else "")
            self.seg.addItem(label, m["id"])
            tip = m.get("provenance_text", "") + (": not validated on real tissue" if m.get("synthetic") else "")
            self.seg.setItemData(self.seg.count() - 1, tip[:300], Qt.ToolTipRole)
            self._synthetic[m["id"]] = bool(m.get("synthetic"))
        self.chip = QLabel(f"{SYNTHETIC_CHIP}: this model was trained on synthetic phantoms only and is not "
                           "validated on real tissue. Results are labelled accordingly.")
        self.chip.setProperty("role", "chip-bad")
        self.chip.setWordWrap(True)
        self.chip.hide()
        self.seg.currentIndexChanged.connect(lambda *_: self.chip.setVisible(self._synthetic.get(self.seg.currentData(), False)))
        self.material = QComboBox()
        self.material.addItem("Unspecified", None)
        for k, label in GRAFT_MATERIALS:
            self.material.addItem(label, k)
        self.material.addItem("No graft (empty defect)", "__no_graft__")
        self.bright = QCheckBox("Graft is brighter than new bone")
        self.bright.setChecked(False)
        self.bright.setToolTip("Only meaningful for radiopaque graft materials (calcium phosphates, calcium sulfate, "
                               "bioglass, xenograft). Disabled for no graft, unspecified and radiolucent materials.")
        self.material.currentIndexChanged.connect(self._material_changed)
        self.thick = QCheckBox("Compute thickness metrics (Tb.Th, Tb.Sp)")
        self.thick.setChecked(True)
        self.saved_roi = QCheckBox("Use the latest saved ROI when present")
        self.saved_roi.setChecked(True)
        f.addRow("Defect model", self.model)
        f.addRow("Nominal defect diameter", self.diam)
        f.addRow("Segmentation", self.seg)
        f.addRow("", self.chip)
        f.addRow("Graft material", self.material)
        f.addRow("", self.bright)
        f.addRow("", self.thick)
        f.addRow("", self.saved_roi)
        self.lay.addLayout(f)
        self.lay.addWidget(muted("The graft material is used by the measurement-support advisor to decide which "
                                 "endpoints can be separated reliably. Endpoints it does not support are reported as "
                                 "'not measured' with the reason."))
        self.lay.addWidget(_buttons(self, "Run analysis"))
        self._material_changed()

    RADIOPAQUE = {"ha", "beta_tcp", "bcp", "calcium_sulfate", "bioglass_45s5", "xenograft_dbbm"}

    def _material_changed(self, *_):
        on = self.material.currentData() in self.RADIOPAQUE
        self.bright.setEnabled(on)
        self.bright.setChecked(on)

    def config(self) -> dict:
        mat = self.material.currentData()
        cfg = {"defect_model": self.model.currentText(), "segmentation": self.seg.currentData(),
               "graft_brighter": self.bright.isChecked(), "thickness_metrics": self.thick.isChecked(),
               "nominal_diameter_um": self.diam.value() or None, "no_graft": mat == "__no_graft__"}
        if mat and mat != "__no_graft__":
            cfg["material"] = mat
        return cfg


class RoiDialog(_Dialog):
    def __init__(self, center_vox, spacing, parent=None):
        super().__init__("Define cylindrical ROI", parent)
        self.lay.addWidget(muted("Cylinder along the scan z axis, centred on the current crosshair "
                                 f"(voxel {tuple(center_vox)}). Saved as a new ROI version with your reason."))
        f = QFormLayout()
        self.radius = QDoubleSpinBox()
        self.radius.setRange(1, 1e5)
        self.radius.setValue(1000)
        self.radius.setSuffix(" µm")
        self.depth0, self.depth1 = QDoubleSpinBox(), QDoubleSpinBox()
        for sb, v in ((self.depth0, -1000), (self.depth1, 1000)):
            sb.setRange(-1e5, 1e5)
            sb.setValue(v)
            sb.setSuffix(" µm")
        self.reason = QLineEdit()
        self.reason.setPlaceholderText("e.g. automatic detection failed; drawn from landmarks")
        f.addRow("Radius", self.radius)
        f.addRow("Extent from centre (start)", self.depth0)
        f.addRow("Extent from centre (end)", self.depth1)
        f.addRow("Reason", self.reason)
        self.lay.addLayout(f)
        self.lay.addWidget(self.error)
        self.lay.addWidget(_buttons(self, "Save ROI"))

    def accept(self):
        if len(self.reason.text().strip()) < 3:
            return self.show_error("A reason is required (recorded in the audit trail).")
        if self.depth1.value() <= self.depth0.value():
            return self.show_error("The end extent must be larger than the start extent.")
        super().accept()


class SaveRevisionDialog(_Dialog):
    def __init__(self, summary: dict, base_version: int, parent=None):
        super().__init__("Save label revision", parent, 480)
        self.lay.addWidget(muted(f"The edited labels are stored as a new segmentation version derived from v{base_version}. "
                                 "Endpoints are recomputed with the same ROI. The audit trail records your identity, "
                                 "the reason and the voxel changes below."))
        t = make_table(["Class", "Voxel change"])
        for k, v in summary.items():
            r = t.rowCount()
            t.insertRow(r)
            t.setItem(r, 0, ro_item(k.replace("_", " ")))
            t.setItem(r, 1, ro_item(f"{v:+,}", Qt.AlignRight | Qt.AlignVCenter))
        t.setMaximumHeight(140)
        self.lay.addWidget(t)
        self.reason = QPlainTextEdit()
        self.reason.setPlaceholderText("Reason for the correction (required)")
        self.reason.setMaximumHeight(80)
        self.lay.addWidget(QLabel("Reason"))
        self.lay.addWidget(self.reason)
        self.lay.addWidget(self.error)
        self.lay.addWidget(_buttons(self, "Save revision"))

    def accept(self):
        if len(self.reason.toPlainText().strip()) < 3:
            return self.show_error("Enter a reason (at least 3 characters).")
        super().accept()


class SignDialog(_Dialog):
    MEANINGS = {
        "segmentation": {"approved": "Reviewed the segmentation and approve it for reporting",
                         "needs_changes": "Reviewed the segmentation; corrections are required before reporting",
                         "rejected": "Reviewed the segmentation and reject it"},
        "report": {"approved": "Reviewed the report and approve its release",
                   "needs_changes": "Reviewed the report; changes are required before release",
                   "rejected": "Reviewed the report and reject it"},
        "roi": {"approved": "Reviewed the analysis ROI on the slices and accept it as the analysis volume",
                "needs_changes": "Reviewed the analysis ROI; it must be redefined",
                "rejected": "Reviewed the analysis ROI and reject it"},
    }
    VERBS = {"approved": "Approve", "needs_changes": "Request changes to", "rejected": "Reject"}

    def __init__(self, user: dict, object_desc: str, decision: str, parent=None, object_type: str = "segmentation",
                 signature_roles: list | None = None):
        super().__init__("Electronic signature", parent, 540)
        verb = "Accept" if (object_type == "roi" and decision == "approved") else self.VERBS.get(decision, decision)
        head = QLabel(f"{verb} {object_desc}")
        head.setProperty("role", "heading")
        head.setWordWrap(True)
        self.lay.addWidget(head)
        self.lay.addWidget(muted(f"Signing as {user.get('full_name') or user['username']} ({user['role']}). "
                                 "Re-enter your password to sign. The signature, its meaning and the object hash are "
                                 "recorded in the hash-chained audit trail. Five wrong passwords lock the account "
                                 "for 15 minutes."))
        f = QFormLayout()
        f.setRowWrapPolicy(QFormLayout.WrapLongRows)
        f.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        from .services import SIGNATURE_ROLES
        self.role = QComboBox()
        for r in signature_roles or []:
            self.role.addItem(SIGNATURE_ROLES.get(r, r), r)
        self.meaning = QComboBox()
        self.meaning.setEditable(True)
        mm = self.MEANINGS.get(object_type, self.MEANINGS["segmentation"])
        self.meaning.addItems([mm[decision]] + [v for k, v in mm.items() if k != decision])
        self.meaning.setMinimumContentsLength(30)
        self.comment = QLineEdit()
        self.pw = QLineEdit()
        self.pw.setEchoMode(QLineEdit.Password)
        if self.role.count():
            f.addRow("Sign as", self.role)
        f.addRow("Meaning of\nsignature", self.meaning)
        f.addRow("Comment", self.comment)
        f.addRow("Password", self.pw)
        self.lay.addLayout(f)
        self.lay.addWidget(self.error)
        self.lay.addWidget(_buttons(self, "Sign"))
        self.pw.setFocus()


class LicenceDialog(_Dialog):
    def __init__(self, status: LicenceStatus, parent=None):
        super().__init__("Licence", parent, 520)
        self.status = status
        self.new_file = None
        b = QLabel()
        kind = "ok" if status.state == "valid" and not status.is_test else ("warn" if status.state in ("valid", "evaluation") else "bad")
        set_banner(b, status.summary(), kind)
        b.setWordWrap(True)
        self.lay.addWidget(b)
        f = QFormLayout()
        rows = [("State", status.state), ("Edition", status.edition), ("Licensee", status.licensee or "-"),
                ("Licence ID", status.licence_id or "-"),
                ("Expiry", status.expiry.isoformat() if status.expiry else ("perpetual" if status.state == "valid" else "-")),
                ("Features", ", ".join(sorted(status.features))), ("Signing key", status.key_id or "-"),
                ("Report watermark", status.watermark or "none"), ("Licence file", status.source or "-")]
        for k, v in rows:
            lb = QLabel(str(v))
            lb.setWordWrap(True)
            lb.setTextInteractionFlags(Qt.TextSelectableByMouse)
            f.addRow(k, lb)
        self.lay.addLayout(f)
        from ..licensing import machine_fingerprint
        fp = machine_fingerprint()
        fr = QHBoxLayout()
        fpl = muted(f"Machine fingerprint (for machine-bound licences): {fp}")
        fpl.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)
        cp = QPushButton("Copy")
        cp.clicked.connect(lambda: __import__("PySide6.QtWidgets", fromlist=["QApplication"]).QApplication.clipboard().setText(fp))
        fr.addWidget(fpl, 1)
        fr.addWidget(cp)
        self.lay.addLayout(fr)
        self.lay.addWidget(muted("Without a licence the application runs in evaluation mode: all functions work and "
                                 "reports carry an evaluation watermark. Licences are verified offline."))
        row = QHBoxLayout()
        inst = QPushButton("Install licence file...")
        inst.clicked.connect(self._install)
        row.addWidget(inst)
        row.addStretch(1)
        close = QPushButton("Close")
        close.clicked.connect(self.accept)
        row.addWidget(close)
        self.lay.addLayout(row)

    def _install(self):
        f, _ = QFileDialog.getOpenFileName(self, "Install licence", "", "OsteoQuant licence (*.oqlic);;All files (*)")
        if f:
            self.new_file = f
            self.done(2)


def third_party_components() -> list[tuple[str, str, str]]:
    comps = [("PySide6 / Qt", "PySide6", "LGPL-3.0 (Qt for Python and Qt libraries, dynamically linked)"),
             ("VTK", "vtk", "BSD-3-Clause"), ("NumPy", "numpy", "BSD-3-Clause"), ("SciPy", "scipy", "BSD-3-Clause"),
             ("scikit-image", "scikit-image", "BSD-3-Clause"), ("scikit-learn", "scikit-learn", "BSD-3-Clause"),
             ("Zarr", "zarr", "MIT"), ("numcodecs", "numcodecs", "MIT"), ("SimpleITK", "SimpleITK", "Apache-2.0"),
             ("pydicom", "pydicom", "MIT"), ("NiBabel", "nibabel", "MIT"), ("pynrrd", "pynrrd", "MIT"),
             ("tifffile", "tifffile", "BSD-3-Clause"), ("imagecodecs", "imagecodecs", "BSD-3-Clause"),
             ("olefile", "olefile", "BSD-2-Clause"), ("ReportLab", "reportlab", "BSD-3-Clause"),
             ("Matplotlib", "matplotlib", "Matplotlib licence (PSF-based)"), ("pandas", "pandas", "BSD-3-Clause"),
             ("statsmodels", "statsmodels", "BSD-3-Clause"), ("cryptography", "cryptography", "Apache-2.0 or BSD-3-Clause"),
             ("psutil", "psutil", "BSD-3-Clause"), ("Pillow", "pillow", "MIT-CMU (HPND)"),
             ("FastAPI (shared job handlers)", "fastapi", "MIT"), ("Pydantic", "pydantic", "MIT")]
    out = []
    for name, dist, lic in comps:
        try:
            v = md.version(dist)
        except md.PackageNotFoundError:
            v = "not installed"
        out.append((name, v, lic))
    return out


class AboutDialog(_Dialog):
    def __init__(self, status: LicenceStatus, parent=None):
        super().__init__(f"About {APP_NAME}", parent, 600)
        t = QLabel("OsteoQuant Desktop")
        t.setProperty("role", "title")
        self.lay.addWidget(t)
        self.lay.addWidget(QLabel(f"Version {__version__}"))
        self.lay.addWidget(muted("Preclinical micro-CT analysis of bone-defect healing: new bone, residual graft and "
                                 "host bone. Research software; not a medical device and not validated for GLP "
                                 "or clinical use."))
        self.lay.addWidget(muted("Privacy: the application works fully offline. It sends no telemetry and makes no "
                                 "network connections. Optional workflow timing (Tools menu, off by default) is "
                                 "stored only in the project's own database and is never transmitted."))
        tabs = QTabWidget()
        lic = QWidget()
        fl = QFormLayout(lic)
        fl.addRow("Licence status", QLabel(status.summary()))
        fl.addRow("Edition", QLabel(status.edition))
        fl.addRow("Python", QLabel(platform.python_version()))
        fl.addRow("Platform", QLabel(f"{platform.system()} {platform.release()} ({platform.machine()})"))
        fl.addRow("Build date", QLabel(_build_stamp()))
        tabs.addTab(lic, "Licence")
        tp = QWidget()
        tl = QVBoxLayout(tp)
        tbl: QTableWidget = make_table(["Component", "Version", "Licence"])
        for name, v, l in third_party_components():
            r = tbl.rowCount()
            tbl.insertRow(r)
            tbl.setItem(r, 0, ro_item(name))
            tbl.setItem(r, 1, ro_item(v))
            tbl.setItem(r, 2, ro_item(l))
        tbl.resizeColumnsToContents()
        tbl.horizontalHeader().setStretchLastSection(True)
        tl.addWidget(tbl)
        tl.addWidget(muted("Licence texts of bundled components are in the 'licenses' folder and in "
                           "THIRD_PARTY_NOTICES.txt of the installed application. Qt and Qt for Python are used under "
                           "the LGPL-3.0 as separate shared libraries that you may replace with modified versions; "
                           "nothing in the OsteoQuant licence terms restricts modifying them or reverse engineering "
                           "for debugging such modifications."))
        tabs.addTab(tp, "Third-party licences")
        tabs.setMinimumHeight(300)
        self.lay.addWidget(tabs)
        bb = QDialogButtonBox(QDialogButtonBox.Close)
        bb.rejected.connect(self.reject)
        bb.accepted.connect(self.accept)
        bb.button(QDialogButtonBox.Close).clicked.connect(self.accept)
        self.lay.addWidget(bb)


def _build_stamp() -> str:
    try:
        import sys
        if getattr(sys, "frozen", False):
            return dt.datetime.fromtimestamp(Path(sys.executable).stat().st_mtime).strftime("%Y-%m-%d")
    except OSError:
        pass
    return "development build"


def ask_password_error(parent, msg):
    QMessageBox.warning(parent, "Signature not recorded", msg)


# ============================================================================ user administration
class AddUserDialog(_Dialog):
    def __init__(self, parent=None):
        super().__init__("Add user", parent, 460)
        from .project import ROLE_LABELS
        self.lay.addWidget(muted("Each person signs in with their own account; every action and signature is "
                                 "attributed to it. The new user should change the initial password by asking an "
                                 "administrator for a reset after first use."))
        f = QFormLayout()
        self.user, self.full = QLineEdit(), QLineEdit()
        self.role = QComboBox()
        for r in ("analyst", "reviewer", "study_director", "admin"):
            self.role.addItem(ROLE_LABELS[r], r)
        self.pw1, self.pw2 = QLineEdit(), QLineEdit()
        for p in (self.pw1, self.pw2):
            p.setEchoMode(QLineEdit.Password)
        f.addRow("User name", self.user)
        f.addRow("Full name", self.full)
        f.addRow("Role", self.role)
        f.addRow("Initial password", self.pw1)
        f.addRow("Repeat password", self.pw2)
        self.lay.addLayout(f)
        self.lay.addWidget(muted("Password: at least 10 characters with an upper-case letter and a digit."))
        self.lay.addWidget(self.error)
        self.lay.addWidget(_buttons(self, "Add user"))

    def accept(self):
        if not self.user.text().strip():
            return self.show_error("A user name is required.")
        if self.pw1.text() != self.pw2.text():
            return self.show_error("The passwords do not match.")
        super().accept()

    def values(self):
        return dict(username=self.user.text().strip(), full_name=self.full.text().strip(),
                    role=self.role.currentData(), password=self.pw1.text())


class ResetPasswordDialog(_Dialog):
    def __init__(self, username: str, parent=None):
        super().__init__("Reset password", parent, 420)
        self.lay.addWidget(muted(f"New password for '{username}'. This also clears a temporary lockout and signs the "
                                 "user out of any open session."))
        f = QFormLayout()
        self.pw1, self.pw2 = QLineEdit(), QLineEdit()
        for p in (self.pw1, self.pw2):
            p.setEchoMode(QLineEdit.Password)
        f.addRow("New password", self.pw1)
        f.addRow("Repeat password", self.pw2)
        self.lay.addLayout(f)
        self.lay.addWidget(self.error)
        self.lay.addWidget(_buttons(self, "Reset password"))

    def accept(self):
        if self.pw1.text() != self.pw2.text():
            return self.show_error("The passwords do not match.")
        super().accept()


class UserAdminDialog(_Dialog):
    """Project > Users (administrators): add users with a role, deactivate/reactivate, reset passwords.
    Every action goes through the store API and is audited (user.create / user.deactivate /
    user.activate / user.password_reset)."""

    def __init__(self, project, parent=None):
        super().__init__("Users", parent, 680)
        self.project = project
        self.lay.addWidget(muted("Separation of duties needs at least two people: an author cannot approve their own "
                                 "segmentation, ROI or report. Deactivated users cannot sign in; their records and "
                                 "signatures remain in the audit trail."))
        self.table = make_table(["User name", "Full name", "Role", "Status", "Created"])
        self.table.setMinimumHeight(220)
        self.table.itemSelectionChanged.connect(self._update)
        self.lay.addWidget(self.table, 1)
        row = QHBoxLayout()
        self.add_btn = QPushButton("Add user...")
        self.add_btn.setProperty("role", "primary")
        self.add_btn.clicked.connect(self.add_user)
        self.toggle_btn = QPushButton("Deactivate")
        self.toggle_btn.clicked.connect(self.toggle_active)
        self.reset_btn = QPushButton("Reset password...")
        self.reset_btn.clicked.connect(self.reset_password)
        for b in (self.add_btn, self.toggle_btn, self.reset_btn):
            row.addWidget(b)
        row.addStretch(1)
        close = QPushButton("Close")
        close.clicked.connect(self.accept)
        row.addWidget(close)
        self.lay.addWidget(self.error)
        self.lay.addLayout(row)
        self._users = []
        self.refresh()

    def refresh(self):
        from .project import ROLE_LABELS
        self._users = self.project.users()
        self.table.setRowCount(0)
        for u in self._users:
            r = self.table.rowCount()
            self.table.insertRow(r)
            st = "active" if u["active"] else "deactivated"
            if u.get("locked"):
                st += ", temporarily locked"
            for j, v in enumerate([u["username"], u["full_name"] or "", ROLE_LABELS.get(u["role"], u["role"]), st,
                                   u["created"]]):
                self.table.setItem(r, j, ro_item(v))
        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setStretchLastSection(True)
        self._update()

    def selected(self):
        rows = {i.row() for i in self.table.selectedIndexes()}
        return self._users[min(rows)] if rows else None

    def _update(self):
        u = self.selected()
        me = self.project.user["id"]
        self.toggle_btn.setEnabled(u is not None and u["id"] != me)
        self.toggle_btn.setToolTip("You cannot deactivate your own account" if u is not None and u["id"] == me else "")
        self.toggle_btn.setText("Reactivate" if u is not None and not u["active"] else "Deactivate")
        self.reset_btn.setEnabled(u is not None)

    def add_user(self, values=None):
        if values is None:
            dlg = AddUserDialog(self)
            while dlg.exec():
                try:
                    uid = self.project.add_user(**dlg.values())
                    break
                except (ValueError, PermissionError) as e:
                    dlg.show_error(str(e))
            else:
                return None
        else:
            uid = self.project.add_user(**values)
        self.refresh()
        return uid

    def toggle_active(self):
        u = self.selected()
        if not u:
            return
        try:
            self.project.set_user_active(u["id"], not u["active"])
        except (ValueError, PermissionError) as e:
            self.show_error(str(e))
        self.refresh()

    def reset_password(self, new_password=None):
        u = self.selected()
        if not u:
            return False
        if new_password is None:
            dlg = ResetPasswordDialog(u["username"], self)
            while dlg.exec():
                try:
                    self.project.reset_password(u["id"], dlg.pw1.text())
                    break
                except (ValueError, PermissionError) as e:
                    dlg.show_error(str(e))
            else:
                return False
        else:
            self.project.reset_password(u["id"], new_password)
        self.refresh()
        return True


class IdleLockDialog(_Dialog):
    def __init__(self, minutes: int, parent=None):
        super().__init__("Idle lock", parent, 420)
        self.lay.addWidget(muted("The window locks after this many minutes without keyboard or mouse input. "
                                 "Unlocking requires the signed-in user's password; failed attempts count towards "
                                 "the account lockout. 0 turns the idle lock off (not recommended)."))
        f = QFormLayout()
        from PySide6.QtWidgets import QSpinBox
        self.minutes = QSpinBox()
        self.minutes.setRange(0, 240)
        self.minutes.setValue(int(minutes))
        self.minutes.setSuffix(" min")
        f.addRow("Lock after", self.minutes)
        self.lay.addLayout(f)
        self.lay.addWidget(_buttons(self, "Save"))


SHORTCUTS = [
    ("Navigate tool", "N"), ("Brush tool", "B"), ("Eraser tool", "E"), ("Region grow tool", "G"),
    ("Fill holes tool", "H"), ("Distance measurement tool", "M"), ("Show/hide ROI outline", "R"),
    ("Next / previous slice", "Up / Down, mouse wheel"), ("10 slices forward / back", "Page Up / Page Down"),
    ("First / last slice", "Home / End"), ("Fit view to window", "F"), ("Zoom about the pointer", "Ctrl + wheel"),
    ("Window / level", "Right-drag"), ("Pan", "Middle-drag or Shift + left-drag"), ("Clear distance lines", "Esc"),
    ("Undo / redo", "Ctrl+Z / Ctrl+Shift+Z"), ("Save label revision", "Ctrl+S"), ("Analyse selected scans", "Ctrl+R"),
    ("Import scans", "Ctrl+I"), ("Lock the window now", "Ctrl+L"), ("Open / new project", "Ctrl+O / Ctrl+N"),
]


class ShortcutsDialog(_Dialog):
    def __init__(self, parent=None):
        super().__init__("Keyboard shortcuts", parent, 480)
        self.lay.addWidget(muted("Tool and slice keys act when a viewer panel has keyboard focus (click a slice view "
                                 "first), so they never interfere with typing in the project tree or forms."))
        t = make_table(["Action", "Keys"])
        for a, k in SHORTCUTS:
            r = t.rowCount()
            t.insertRow(r)
            t.setItem(r, 0, ro_item(a))
            t.setItem(r, 1, ro_item(k))
        t.resizeColumnsToContents()
        t.setMinimumHeight(380)
        self.lay.addWidget(t)
        bb = QDialogButtonBox(QDialogButtonBox.Close)
        bb.rejected.connect(self.reject)
        bb.button(QDialogButtonBox.Close).clicked.connect(self.accept)
        self.lay.addWidget(bb)
