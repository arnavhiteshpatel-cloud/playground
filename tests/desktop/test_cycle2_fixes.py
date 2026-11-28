"""Cycle-2 product review (docs/reviews/cycle2/REVIEW_PRODUCT.md): regression tests for the High findings
C2-PRD-01...04 and for the Medium findings fixed in the desktop (C2-PRD-05...12, 14...18)."""
import base64
import csv
import hashlib
import json
import threading
import time
from pathlib import Path

import pytest

from osteoquant.desktop import services as S
from osteoquant.desktop.project import Project, ProjectError
from osteoquant.study.jobs import JobCancelled

from desktop_helpers import DIR_PW, PW, REV_PW, login_as

ANA_PW = "Analyst-Pass-1"


def _seg(project, scan):
    return project.store.segmentations(project.user, scan)[-1]


def _acts(project):
    return [e["action"] for e in project.store.audit.events(limit=100000)]


def _reopen(window, project, user="admin", pw=PW):
    folder = project.folder
    project.close()
    assert window.open_project(str(folder), user, pw)
    return window


class CancelAt:
    """Job context that cancels when a progress message starts with ``prefix``."""

    def __init__(self, prefix):
        self.prefix = prefix
        self.seen = []

    def progress(self, frac, msg=""):
        self.seen.append(msg)
        if msg.startswith(self.prefix):
            raise JobCancelled()

    def check(self):
        pass


def _second_scan(project, sid, scan, tv_factor=2.0):
    """A second analysed scan (copy of ``scan`` with its own animal and a distinct TV), without re-running
    the analysis. Returns (scan2_id, {scan_id: TV_mm3})."""
    st = project.store
    a1 = S.get_or_create_specimen(project, sid, "RAT-01")
    a2 = S.get_or_create_specimen(project, sid, "RAT-02")
    st.exec("UPDATE scans SET specimen_id=? WHERE id=?", (a1, scan))
    s2 = st.exec("INSERT INTO scans(org_id,study_id,specimen_id,timepoint_id,store_path,source_name,format,file_sha256,"
                 "content_sha256,shape,spacing_um,meta,qc,acquisition,status,created_by,created) "
                 "SELECT org_id,study_id,?,timepoint_id,store_path,'second.nii.gz',format,'f2','c2',shape,spacing_um,"
                 "meta,qc,acquisition,status,created_by,created FROM scans WHERE id=?", (a2, scan))
    seg = _seg(project, scan)
    g2 = st.exec("INSERT INTO segmentations(scan_id,version,kind,method,model_name,model_sha256,roi_id,labels_key,"
                 "labels_sha256,edits,created_by,created) SELECT ?,1,kind,method,model_name,model_sha256,roi_id,"
                 "labels_key,labels_sha256,edits,created_by,created FROM segmentations WHERE id=?", (s2, seg["id"]))
    m = st.q1("SELECT * FROM measurements WHERE scan_id=? ORDER BY id DESC LIMIT 1", (scan,))
    met = json.loads(m["metrics"])
    tv1 = met["metrics"]["class_volumes"]["TV_mm3"]
    for k in ("metrics", "reported_metrics"):
        if met.get(k):
            met[k]["class_volumes"]["TV_mm3"] = tv1 * tv_factor
    st.exec("INSERT INTO measurements(scan_id,segmentation_id,roi_id,config_id,metrics,software_version,created) "
            "VALUES (?,?,?,?,?,?,?)", (s2, g2, m["roi_id"], m["config_id"], json.dumps(met), m["software_version"],
                                       m["created"]))
    return s2, {scan: tv1, s2: tv1 * tv_factor}


def _bundle(project, rep):
    return json.loads(Path(S.report_meta(project, rep["report_id"])["bundle_path"]).read_text(encoding="utf-8"))


# ============================================================================ C2-PRD-01 (High)
def test_c2_01_report_specimens_joined_by_scan_and_segmentation_id(analysed, monkeypatch):
    project, sid, scan = analysed
    s2, tv = _second_scan(project, sid, scan)
    rows = project.store.latest_measurements(project.user, sid)
    assert [r["scan_id"] for r in rows] == sorted(r["scan_id"] for r in rows)        # ORDER BY
    # simulate the race: the library returns the specimens in a different order than the measurement rows
    import osteoquant.api.bundle as B
    orig = B.bundle_from_store

    def reordered(*a, **k):
        b = orig(*a, **k)
        b["specimens"].reverse()
        return b
    monkeypatch.setattr(B, "bundle_from_store", reordered)
    rep = S.generate_report(project, sid, blinded=True)
    b = _bundle(project, rep)
    assert [s["scan_id"] for s in b["specimens"]] == [s2, scan]
    for spec in b["specimens"]:
        sc = project.store.scan(project.user, spec["scan_id"])
        assert spec["animal_id"] == project.animal_code(sc["specimen_id"], sid)        # codes of ITS scan
        assert spec["scan"]["source"] == project.scan_code(sc["id"], sid)
        assert spec["metrics"]["class_volumes"]["TV_mm3"] == pytest.approx(tv[spec["scan_id"]])   # numbers of ITS scan
        assert spec["segmentation_id"] == project.store.segmentations(project.user, spec["scan_id"])[-1]["id"]
    # a specimen that cannot be matched stops the report instead of mis-attributing data
    def broken(*a, **k):
        b = orig(*a, **k)
        b["specimens"][0]["segmentation_id"] = 999999
        return b
    monkeypatch.setattr(B, "bundle_from_store", broken)
    with pytest.raises(RuntimeError, match="no matching measurement"):
        S.generate_report(project, sid)


def test_c2_01_bundle_built_from_one_snapshot(project, study):
    """Writes from another thread wait until the report's read snapshot ends."""
    st = project.store
    started, done = threading.Event(), threading.Event()
    probe = {}

    def writer():
        started.set()                 # about to write (C3-PRD-19: the assertion no longer depends on scheduling)
        st.exec("INSERT INTO timepoints(study_id,label) VALUES (?,?)", (study, "w2"))
        done.set()

    def lock_probe():                 # deterministic: can another thread take the store lock right now?
        got = st.lock.acquire(blocking=False)
        probe["free"] = got
        if got:
            st.lock.release()
    with st.snapshot():
        n0 = st.q1("SELECT count(*) n FROM timepoints")["n"]
        t = threading.Thread(target=writer)
        t.start()
        assert started.wait(5)
        p = threading.Thread(target=lock_probe)
        p.start()
        p.join(5)
        assert probe == {"free": False}       # the snapshot holds the lock, so the writer cannot be inside exec
        assert not done.is_set()
        assert st.q1("SELECT count(*) n FROM timepoints")["n"] == n0
    t.join(5)
    assert done.is_set()


# ============================================================================ C2-PRD-02 (High)
def test_c2_02_idle_lock_blocks_every_window_and_dialog(qtbot, window, project):
    from PySide6.QtCore import QTimer, Qt
    from PySide6.QtWidgets import QDialog
    from osteoquant.desktop.dialogs import UserAdminDialog
    w = _reopen(window, project)
    users = UserAdminDialog(w.project, w)          # modeless window left open by an administrator
    users.show()
    clicks = []
    users.add_btn.clicked.disconnect()
    users.add_btn.clicked.connect(lambda: clicks.append(1))
    # a dialog running its own event loop (exec) when the idle timeout fires is cancelled
    modal = QDialog(w)
    QTimer.singleShot(50, lambda: w.lock_session(idle=True))
    assert modal.exec() == QDialog.Rejected
    assert w._locked and not modal.isVisible() and not users.isVisible()
    # even if a window is brought back while locked, no input reaches it
    users.show()
    qtbot.mouseClick(users.add_btn, Qt.LeftButton)
    qtbot.keyClick(users.table, Qt.Key_Space)
    assert clicks == [] and w._lock_filter.blocked > 0
    assert not w._lock_allows(users.add_btn) and w._lock_allows(w.lock_page.pw)
    users.hide()
    n_users = len(w.project.users())
    # the lock page itself still works
    qtbot.keyClicks(w.lock_page.pw, PW)
    qtbot.mouseClick(w.lock_page.unlock, Qt.LeftButton)
    assert not w._locked
    assert users.isVisible()                       # restored after unlock
    qtbot.mouseClick(users.add_btn, Qt.LeftButton)
    assert clicks == [1]
    assert len(w.project.users()) == n_users
    users.close()


# ============================================================================ C2-PRD-03 (High)
@pytest.fixture
def blinded_team(team):
    project, sid, scan, rid, did = team
    spec = S.get_or_create_specimen(project, sid, "R01")
    project.store.exec("UPDATE scans SET specimen_id=?, source_name='R01_week4.nii.gz' WHERE id=?", (spec, scan))
    project.store.exec("UPDATE studies SET blinded=1 WHERE id=?", (sid,))
    return project, sid, scan, rid, did


def test_c2_03_study_blinding_enforced_for_reviewer(blinded_team, tmp_path):
    from osteoquant.desktop.results_view import build_rows
    project, sid, scan, rid, did = blinded_team
    unblinded_report = S.generate_report(project, sid)                 # admin (may unblind): identifying report
    rev = login_as(project, "rev", REV_PW)
    assert rev.blinding_forced() and rev.study_forces_blinding(sid)
    text = json.dumps(rev.study_tree(False))                           # the caller asked for the open view
    assert "R01" not in text and "R01_week4" not in text and "Scan S-" in text
    row = build_rows(rev, sid, blinded_view=False)[0]
    assert "R01" not in row["scan"] and "R01" not in row["animal"]
    with pytest.raises(PermissionError, match="blinded"):
        S.export_report(rev, unblinded_report["report_id"], tmp_path)
    assert S.generate_report(rev, sid)["blinded"]                       # reviewers always get a blinded report
    S.export_audit(rev, tmp_path / "a.json")                            # audit export is masked for them
    assert "R01_week4" not in (tmp_path / "a.json").read_text()
    # reviewers cannot unblind; the study director can, as a signed (re-authenticated) action
    with pytest.raises(PermissionError):
        S.unblind_study(rev, REV_PW, sid, "I want to see the groups")
    dr = login_as(project, "dir", DIR_PW)
    with pytest.raises(PermissionError, match="Re-authentication"):
        S.unblind_study(dr, "wrong-password", sid, "analysis locked, statistics done")
    assert rev.study_forces_blinding(sid)
    S.unblind_study(dr, DIR_PW, sid, "analysis locked, statistics done")
    ev = [e for e in project.store.audit.events(limit=10000) if e["action"] == "study.unblind"][0]
    assert ev["details"]["signed"] and ev["details"]["signer"] == "dir" and ev["details"]["reason"]
    assert not rev.study_forces_blinding(sid) and "R01_week4" in json.dumps(rev.study_tree(False))
    rev.store.conn.close()
    dr.store.conn.close()


def test_c2_03_reviewer_cannot_switch_blinded_mode_off(qtbot, window, blinded_team):
    project, sid, scan, rid, did = blinded_team
    w = _reopen(window, project, "rev", REV_PW)
    assert w.blinded_view and not w.a_blind.isEnabled() and not w.review.blind.isEnabled()
    assert "study director" in w.a_blind.toolTip()
    w.set_blinded(False)
    assert w.blinded_view and w.a_blind.isChecked()
    assert "ui.blinded_mode_denied" in _acts(w.project)
    assert not w.a_unblind.isEnabled()
    # C2-PRD-14: job titles carry blinded codes, never database scan IDs
    assert w._job_scan(scan).startswith("Scan S-")


# ============================================================================ C2-PRD-04 (High) + C2-PRD-05
@pytest.fixture
def approvable(team):
    """Team with an approved segmentation and a fresh, reviewed report generated by the admin."""
    project, sid, scan, rid, did = team
    rev = login_as(project, "rev", REV_PW)
    dr = login_as(project, "dir", DIR_PW)
    S.sign_review(rev, REV_PW, "segmentation", _seg(project, scan)["id"], "approved", "approve segmentation")
    rep = S.generate_report(project, sid)
    yield project, sid, scan, rev, dr, rep
    rev.store.conn.close()
    dr.store.conn.close()


def test_c2_04_signed_copy_refused_for_edited_bundle(approvable):
    from osteoquant.desktop.report_integrity import ReportIntegrityError
    project, sid, scan, rev, dr, rep = approvable
    meta = S.report_meta(project, rep["report_id"])
    ev = [e for e in project.store.audit.events(limit=10000) if e["action"] == "report.generate"][-1]
    assert meta["bundle_sha256"] == ev["details"]["bundle_sha256"] == \
        hashlib.sha256(Path(meta["bundle_path"]).read_bytes()).hexdigest()
    b = json.loads(Path(meta["bundle_path"]).read_text())
    b["specimens"][0]["metrics"]["class_volumes"]["TV_mm3"] = 999.999
    Path(meta["bundle_path"]).write_text(json.dumps(b))
    n_reviews = len(project.store.reviews(project.user, "report", rep["report_id"]))
    with pytest.raises(ReportIntegrityError, match="bundle was modified"):
        S.sign_review(dr, DIR_PW, "report", rep["report_id"], "approved", "approve the report release",
                      signature_role="study_director")
    assert len(project.store.reviews(project.user, "report", rep["report_id"])) == n_reviews     # nothing signed
    with pytest.raises(ReportIntegrityError):
        S.render_signed_report(project, rep["report_id"])
    # forging the database hash as well is caught by the audit trail
    forged = hashlib.sha256(Path(meta["bundle_path"]).read_bytes()).hexdigest()
    project.store.exec("UPDATE desktop_report_meta SET bundle_sha256=? WHERE report_id=?", (forged, rep["report_id"]))
    with pytest.raises(ReportIntegrityError, match="audit trail"):
        S.render_signed_report(project, rep["report_id"])
    assert "report.integrity_failed" in _acts(project)
    assert not S.report_meta(project, rep["report_id"]).get("signed_pdf")


def test_c2_04_05_approval_rechecks_pdf_and_fails_closed(approvable):
    project, sid, scan, rev, dr, rep = approvable
    pdf = Path(rep["pdf"])
    original = pdf.read_bytes()
    pdf.write_bytes(original + b"\n% appended")
    with pytest.raises(PermissionError, match="PDF was modified"):
        S.sign_review(dr, DIR_PW, "report", rep["report_id"], "approved", "approve the report release",
                      signature_role="study_director")
    pdf.write_bytes(original)
    # C2-PRD-05: a missing bundle fails closed (no approval of an unverifiable report)
    bp = Path(S.report_meta(project, rep["report_id"])["bundle_path"])
    data = bp.read_bytes()
    bp.unlink()
    with pytest.raises(PermissionError, match="missing"):
        S.sign_review(dr, DIR_PW, "report", rep["report_id"], "approved", "approve the report release",
                      signature_role="study_director")
    bp.write_bytes(data)
    assert S.report_meta(project, rep["report_id"])["review_status"] == "reviewed"
    S.sign_review(dr, DIR_PW, "report", rep["report_id"], "approved", "approve the report release",
                  signature_role="study_director")
    assert Path(S.report_meta(project, rep["report_id"])["signed_pdf"]).is_file()


def test_c2_05_unreviewed_report_refused_even_without_bundle(team):
    project, sid, scan, rid, did = team
    rev = login_as(project, "rev", REV_PW)
    dr = login_as(project, "dir", DIR_PW)
    early = S.generate_report(project, sid)                              # before the segmentation approval
    S.sign_review(rev, REV_PW, "segmentation", _seg(project, scan)["id"], "approved", "approve segmentation")
    assert S.report_meta(project, early["report_id"])["review_status"] == "unreviewed_automated"
    Path(S.report_meta(project, early["report_id"])["bundle_path"]).unlink()
    with pytest.raises(PermissionError):
        S.sign_review(dr, DIR_PW, "report", early["report_id"], "approved", "approve the report release",
                      signature_role="study_director")
    assert not [r for r in project.store.reviews(project.user, "report", early["report_id"]) if r["decision"] == "approved"]
    rev.store.conn.close()
    dr.store.conn.close()


# ============================================================================ C2-PRD-06
def test_c2_06_segmentation_author_cannot_approve_and_one_approval_per_person(approvable):
    project, sid, scan, rev, dr, rep = approvable
    by_dir = S.generate_report(dr, sid)                       # the admin authored every reported segmentation
    with pytest.raises(PermissionError, match="authored a segmentation"):
        S.sign_review(project, PW, "report", by_dir["report_id"], "approved", "approve the report release",
                      signature_role="study_director")
    S.sign_review(dr, DIR_PW, "report", rep["report_id"], "approved", "scientific review of the report",
                  signature_role="reviewer")
    with pytest.raises(PermissionError, match="already approved"):
        S.sign_review(dr, DIR_PW, "report", rep["report_id"], "approved", "approve the report release",
                      signature_role="study_director")
    signers = {r["reviewer_id"] for r in project.store.reviews(project.user, "report", rep["report_id"])
               if r["decision"] == "approved"}
    assert len(signers) == 1
    assert {"review.self_approval_denied", "review.duplicate_approval_denied"} <= set(_acts(project))


# ============================================================================ C2-PRD-07 / C2-PRD-09
def test_c2_07_deactivated_user_session_ends_at_next_action(analysed):
    project, sid, scan = analysed
    uid = project.add_user("ana", "Andy Analyst", "analyst", ANA_PW)
    ana = login_as(project, "ana", ANA_PW)
    assert ana.require_user()["role"] == "analyst"
    project.set_user_role(uid, "viewer")                      # role change: effective at the next action
    assert ana.require_user()["role"] == "viewer" and not ana.can("write")
    project.set_user_role(uid, "analyst")
    project.set_user_active(uid, False)
    with pytest.raises(ProjectError, match="deactivated"):
        S.save_cylinder_roi(ana, scan, (20, 28, 28), 500, (-600, 600), reason="should be refused")
    assert ana.user is None
    with pytest.raises(ProjectError):
        S.generate_report(ana, sid)
    assert "session.ended" in _acts(project)
    ana.store.conn.close()


def test_c2_07_window_signs_out_deactivated_user(qtbot, window, analysed, monkeypatch):
    from PySide6.QtWidgets import QMessageBox
    project, sid, scan = analysed
    uid = project.add_user("ana", "Andy Analyst", "analyst", ANA_PW)
    admin = login_as(project, "admin", PW)
    w = _reopen(window, project, "ana", ANA_PW)
    shown = []
    monkeypatch.setattr(QMessageBox, "warning", lambda *a, **k: shown.append(a[2]))
    w.lock_session()
    admin.set_user_active(uid, False)
    assert not w.unlock_session(ANA_PW) and "deactivated" in w.lock_page.error.text()
    w._check_session()
    assert w.project is None and shown and "deactivated" in shown[0]
    admin.close()


def test_c2_09_role_change_audited_and_database_edit_detected(project):
    uid = project.add_user("ana", "Andy Analyst", "analyst", ANA_PW)
    with pytest.raises(ValueError):
        project.set_user_role(project.user["id"], "viewer")              # not one's own role
    project.set_user_role(uid, "reviewer")
    ev = [e for e in project.store.audit.events(limit=1000) if e["action"] == "user.role_change"][0]
    assert ev["details"] == {"username": "ana", "old_role": "analyst", "new_role": "reviewer"}
    ana = login_as(project, "ana", ANA_PW)
    assert ana.user["role"] == "reviewer"
    # escalation by editing the database: the open session ends, the next sign-in is refused
    project.store.exec("UPDATE users SET role='admin' WHERE id=?", (uid,))
    with pytest.raises(ProjectError, match="integrity"):
        ana.require_user()
    p2 = Project(project.folder)
    assert not p2.login("ana", ANA_PW)
    assert "auth.user_record_mismatch" in _acts(project)
    assert project.store.audit.verify_chain()["ok"]
    project.store.exec("UPDATE users SET role='reviewer' WHERE id=?", (uid,))   # back to the audited state
    assert p2.login("ana", ANA_PW)
    p2.close()
    ana.store.conn.close()


# ============================================================================ C2-PRD-08
def test_c2_08_self_service_password_change(qtbot, project):
    project.add_user("ana", "Andy Analyst", "analyst", ANA_PW)
    ana = login_as(project, "ana", ANA_PW)
    other = login_as(project, "ana", ANA_PW)
    assert ana.password_change_required                          # set by an administrator
    with pytest.raises(PermissionError):
        ana.change_password("wrong-password", "Brand-New-Pass-7")
    with pytest.raises(ValueError):
        ana.change_password(ANA_PW, "short")
    with pytest.raises(ValueError, match="differ"):
        ana.change_password(ANA_PW, ANA_PW)
    ana.change_password(ANA_PW, "Brand-New-Pass-7")
    assert not ana.password_change_required and ana.require_user()            # this session continues
    with pytest.raises(ProjectError):
        other.require_user()                                                  # other sessions end
    assert "user.password_change" in _acts(project)
    p3 = Project(project.folder)
    assert not p3.login("ana", ANA_PW) and p3.login("ana", "Brand-New-Pass-7")
    assert not p3.password_change_required
    for p in (ana, other, p3):
        p.store.conn.close()
    # the dialog text no longer tells users to ask an administrator; the Users dialog changes roles
    from osteoquant.desktop.dialogs import AddUserDialog, UserAdminDialog
    d = AddUserDialog()
    qtbot.addWidget(d)
    assert "asking an administrator" not in " ".join(c.text() for c in d.findChildren(type(d.error)))
    ud = UserAdminDialog(project)
    qtbot.addWidget(ud)
    ud.table.selectRow(1)
    assert ud.role_btn.isEnabled() and ud.change_role("reviewer")
    assert {u["username"]: u["role"] for u in project.users()}["ana"] == "reviewer"


# ============================================================================ C2-PRD-10
def test_c2_10_cancelled_or_failed_revision_leaves_nothing(analysed, monkeypatch):
    import zarr
    project, sid, scan = analysed
    seg = _seg(project, scan)
    sc = project.store.scan(project.user, scan)
    lab = S.load_scan_layers(sc["store_path"], seg)["labels"].copy()
    lab[10, 20:24, 20:24] = 2

    def state():
        g = zarr.open_group(sc["store_path"], mode="r")
        return (len(project.store.segmentations(project.user, scan)),
                project.store.q1("SELECT count(*) n FROM measurements WHERE scan_id=?", (scan,))["n"],
                sorted(k for k in g["labels"].keys()))
    before = state()
    for step in ("writing labels", "saving revision"):
        with pytest.raises(JobCancelled):
            S.save_label_revision(project, scan, seg["id"], lab, "edit to cancel", ctx=CancelAt(step))
        assert state() == before
    n_events = len(_acts(project))
    monkeypatch.setattr(project.store, "save_measurement", lambda *a, **k: (_ for _ in ()).throw(OSError("disk full")))
    with pytest.raises(OSError):
        S.save_label_revision(project, scan, seg["id"], lab, "edit that fails")
    assert state() == before and len(_acts(project)) == n_events       # rows and their audit events rolled back
    monkeypatch.undo()
    r = S.save_label_revision(project, scan, seg["id"], lab, "edit that succeeds")
    assert r["version"] == seg["version"] + 1


def test_c2_10_cancelled_import_rolls_back_and_allows_reimport(project, study, phantom_file):
    req = S.ImportRequest(str(phantom_file), (40, 40, 40), True, study)
    with pytest.raises(JobCancelled):
        S.import_scan(project, req, ctx=CancelAt("running QC"))
    assert project.store.scans(project.user, study) == []
    assert "scan.import_rolled_back" in _acts(project)
    o = S.import_scan(project, req)
    assert o.scan_id and o.status in ("imported", "flagged"), o.reason


def test_c2_10_cancelled_report_leaves_no_building_row(analysed, monkeypatch):
    project, sid, scan = analysed
    with pytest.raises(JobCancelled):
        S.generate_report(project, sid, ctx=CancelAt("rendering PDF"))
    import osteoquant.report as R

    def cancelled(*a, **k):
        raise JobCancelled()
    monkeypatch.setattr(R, "build_pdf", cancelled)
    with pytest.raises(JobCancelled):
        S.generate_report(project, sid)
    assert project.store.q("SELECT id FROM reports") == []
    assert "report.cancelled" in _acts(project)


# ============================================================================ C2-PRD-11
def _fake_scan(project, study):
    return project.store.register_scan(project.user, study, None, None, "", "x.nii.gz", "nifti", None, None,
                                       [4, 4, 4], [10, 10, 10], {})


def test_c2_11_version_allocation_is_atomic_under_concurrency(project, study):
    from osteoquant.study.db import Store
    scan = _fake_scan(project, study)
    errors, user = [], project.user
    stores = [project.store, project.store, Store(project.store.path, project.store.data_dir)]

    def worker(st, n):
        for i in range(n):
            try:
                st.save_segmentation(user, scan, "automatic", f"k{i}", "h")
                if i % 3 == 0:
                    st.save_roi(user, scan, {"method": "m", "definition_sha256": "d"}, "r")
            except Exception as e:  # noqa: BLE001
                errors.append(repr(e))
    ts = [threading.Thread(target=worker, args=(st, 40)) for st in stores]
    for t in ts:
        t.start()
    for t in ts:
        t.join(60)
    assert errors == []
    vs = [r["version"] for r in project.store.q("SELECT version FROM segmentations WHERE scan_id=?", (scan,))]
    assert sorted(vs) == list(range(1, 121))
    rv = [r["version"] for r in project.store.q("SELECT version FROM rois WHERE scan_id=?", (scan,))]
    assert sorted(rv) == list(range(1, len(rv) + 1))
    stores[2].conn.close()


# ============================================================================ C2-PRD-12
def test_c2_12_missing_or_unknown_advisor_output_is_not_assessed():
    from osteoquant.desktop.support import (FLAGGED, NOT_ASSESSED, SUPPORTED, endpoint_value, measurement_support)
    base = {"qc": {"verdict": "suitable"},
            "metrics": {"class_volumes": {"TV_mm3": 3.0, "new_bone_fraction": 0.3, "residual_graft_fraction": 0.2,
                                          "uncertain_fraction": 0.0},
                        "new_bone_architecture": {"Tb_Th_um": 100}}}
    for res in (base, {**base, "measurement_support": {"endpoints": {"residual_graft_volume": {"status": "unknown"}}}},
                {**base, "measurement_support": {"endpoints": "garbage"}}):
        sup = measurement_support(res)
        assert sup["overall"] != SUPPORTED
        for key in ("residual_graft_fraction", "new_bone_fraction", "new_bone_volume_mm3"):
            v, st, reasons = endpoint_value(res, sup, key)
            assert v is None and st == NOT_ASSESSED and any("no measurement-support assessment" in r for r in reasons)
        v, st, _ = endpoint_value(res, sup, "TV_mm3")
        assert v == 3.0 and st == SUPPORTED                      # not advisor-dependent
    no_qc = {k: v for k, v in base.items() if k != "qc"}
    sup = measurement_support(no_qc)
    assert sup["endpoints"]["TV_mm3"]["status"] == FLAGGED and "QC not run" in sup["endpoints"]["TV_mm3"]["reasons"]


# ============================================================================ C2-PRD-14 / 15 / 16 / 17
def test_c2_14_16_blinded_outputs_and_verifiable_audit_export(analysed, tmp_path):
    from osteoquant.audit.log import GENESIS, _row_hash
    from osteoquant.desktop.blinding import Masker
    project, sid, scan = analysed
    figdir = project.store.data_dir / f"org{project.user['org_id']}" / "reports" / "fig"
    before = set(figdir.glob("scan*_seg*.png")) if figdir.exists() else set()
    rep = S.generate_report(project, sid, blinded=True)
    assert set(figdir.glob("scan*_seg*.png")) == before                 # no unblinded figure written
    csv_text = Path(rep["csv"]).read_text(encoding="utf-8")
    sc = project.store.scan(project.user, scan)
    assert sc["file_sha256"] not in csv_text and "ph.nii" not in csv_text
    seg_ev = [e for e in project.store.audit.events(limit=10000) if e["object_type"] == "segmentation"][0]
    masked = Masker(project).event(seg_ev)
    assert masked["object_id"] == "(blinded)" and "(blinded)" in masked["object_label"]
    # CSV export: every row re-verifies from the file; the export's own hash is audited
    res = S.export_audit(project, tmp_path / "audit.csv")
    lines = (tmp_path / "audit.csv").read_text(encoding="utf-8").splitlines()
    prev = GENESIS
    for r in csv.DictReader(lines[1:]):
        nz = lambda v: v or None  # noqa: E731
        assert r["prev_hash"] == prev
        assert _row_hash(prev, r["ts_utc"], nz(r["user_id"]), nz(r["org_id"]), r["action"], nz(r["object_type"]),
                         nz(r["object_id"]), r["details"]) == r["row_hash"]
        prev = r["row_hash"]
    ev = [e for e in project.store.audit.events(limit=10) if e["action"] == "audit.export"][0]
    assert ev["details"]["sha256"] == res["sha256"] == hashlib.sha256((tmp_path / "audit.csv").read_bytes()).hexdigest()
    S.export_audit(project, tmp_path / "blind.json", blinded=True)
    data = json.loads((tmp_path / "blind.json").read_text())
    assert data["masked_rows"] > 0 and "not reproducible" in data["masking_note"]
    assert any(e["masked"] for e in data["events"])


def test_c2_15_approve_disabled_while_preview_hidden(qtbot, window, approvable):
    project, sid, scan, rev, dr, rep = approvable
    w = _reopen(window, project, "rev", REV_PW)
    w.set_blinded(True)
    w.reports.refresh(rep["report_id"])
    assert w.reports.right.currentWidget() is w.reports.hidden_note
    assert not w.reports.approve.isEnabled() and "not seen" in w.reports.approve.toolTip()
    assert not w.reports.export.isEnabled()


def test_c2_17_manual_roi_needs_reason_and_second_person(analysed):
    project, sid, scan = analysed
    with pytest.raises(ValueError, match="reason"):
        S.save_cylinder_roi(project, scan, (20, 28, 28), 500, (-600, 600))
    rid = S.save_cylinder_roi(project, scan, (20, 28, 28), 500, (-600, 600), reason="drawn from landmarks")
    st = S.roi_state(project, rid)
    assert st["manual"] and st["status"] == "awaiting acceptance" and st["manual_pending"]
    met = json.loads(project.store.q1("SELECT metrics FROM measurements WHERE scan_id=? ORDER BY id DESC LIMIT 1",
                                      (scan,))["metrics"])
    sup = S.measurement_support_for(project, met, rid)
    assert any("manual ROI not yet accepted" in r for r in sup["endpoints"]["TV_mm3"]["reasons"])
    with pytest.raises(PermissionError):
        S.sign_review(project, PW, "roi", rid, "approved", "accept my own ROI")


# ============================================================================ C2-PRD-18
def test_c2_18_malformed_licence_starts_in_evaluation_mode(qtbot, tmp_path, monkeypatch):
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from osteoquant.licensing import current_status, verify_envelope, verify_file
    from osteoquant.licensing.core import FORMAT
    bad = {"format": FORMAT, "key_id": [], "payload": "{}", "signature": "AA=="}
    assert verify_envelope(bad).state == "invalid"
    f = tmp_path / "licence.oqlic"
    f.write_text(json.dumps(bad))
    assert verify_file(f).state == "invalid"
    k = Ed25519PrivateKey.generate()
    pub = k.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw).hex()
    env = {"format": FORMAT, "key_id": "k", "payload": "[1,2]",
           "signature": base64.b64encode(k.sign(b"[1,2]")).decode()}
    st = verify_envelope(env, keys={"k": (pub, False)})
    assert st.state == "invalid" and "not a licence record" in st.reason
    monkeypatch.setenv("OSTEOQUANT_LICENCE_FILE", str(f))
    st = current_status()
    assert st.state == "invalid" and "Evaluation mode" in st.summary() and "malformed" in st.summary()
    from PySide6.QtCore import QSettings
    from osteoquant.desktop.main_window import MainWindow
    from osteoquant.desktop.settings import AppSettings
    w = MainWindow(AppSettings(QSettings(str(tmp_path / "s.ini"), QSettings.IniFormat)))
    qtbot.addWidget(w)
    assert w.licence.state == "invalid" and "Evaluation mode" in w.start.lic.text()
