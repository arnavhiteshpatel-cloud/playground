"""Quality-review desktop gaps: user administration, idle lock, audit export (dossier §11 D-2, D-4, D-8)."""
import csv
import json

import pytest

from osteoquant.desktop import services as S
from osteoquant.desktop.project import Project

from desktop_helpers import PW, REV_PW, login_as


def _acts(project):
    return [e["action"] for e in project.store.audit.events(limit=5000)]


def test_user_admin_add_deactivate_reset_audited(qtbot, project):
    from osteoquant.desktop.dialogs import UserAdminDialog
    d = UserAdminDialog(project)
    qtbot.addWidget(d)
    n0 = d.table.rowCount()
    uid = d.add_user({"username": "dir", "full_name": "Dora Director", "role": "study_director",
                      "password": "Director-Pass-1"})
    assert d.table.rowCount() == n0 + 1
    assert {u["username"]: u["role"] for u in project.users()}["dir"] == "study_director"
    with pytest.raises(ValueError):                                   # weak password: store policy
        project.add_user("weak", "", "analyst", "short")
    with pytest.raises(ValueError, match="already taken"):
        project.add_user("dir", "", "analyst", "Another-Pass-1")
    d.table.selectRow(n0)
    assert d.selected()["id"] == uid
    d.toggle_active()
    p2 = Project(project.folder)
    assert not p2.login("dir", "Director-Pass-1")                     # deactivated
    d.table.selectRow(n0)
    d.toggle_active()                                                 # reactivate
    d.table.selectRow(n0)
    assert d.reset_password("Director-New-2")
    assert not p2.login("dir", "Director-Pass-1") and p2.login("dir", "Director-New-2")
    with pytest.raises(PermissionError):                              # non-admins cannot administer users
        p2.users()
    p2.close()
    d.table.selectRow(0)                                              # own account cannot be deactivated
    assert not d.toggle_btn.isEnabled()
    with pytest.raises(ValueError):
        project.set_user_active(project.user["id"], False)
    acts = _acts(project)
    for a in ("user.create", "user.deactivate", "user.activate", "user.password_reset"):
        assert a in acts
    assert project.store.audit.verify_chain()["ok"]


def test_reset_password_clears_lockout(project):
    uid = project.add_user("rev", "R", "reviewer", REV_PW)
    p2 = Project(project.folder)
    for _ in range(5):
        assert not p2.login("rev", "wrong-password")
    assert not p2.login("rev", REV_PW)                                # temporarily locked
    project.reset_password(uid, "Reviewer-New-3")
    assert p2.login("rev", "Reviewer-New-3")
    p2.close()


def test_idle_lock_hides_project_and_unlock_uses_lockout(qtbot, window, project):
    folder = project.folder
    project.close()
    w = window
    assert w.open_project(str(folder), "admin", PW)
    assert w.project.idle_lock_minutes == 15                           # default
    t = [1000.0]
    w.idle.clock = lambda: t[0]
    w.idle.set_timeout_minutes(w.project.idle_lock_minutes)
    t[0] += 14 * 60
    assert not w.idle.check() and not w._locked
    t[0] += 61
    assert w.idle.check() and w._locked
    assert w.stack.currentWidget() is w.lock_page and not w.d_project.isVisible()
    assert not w.unlock_session("wrong-password") and w._locked
    assert w.unlock_session(PW) and not w._locked
    assert w.stack.currentWidget() is w.tabs and w.d_project.isVisible()
    acts = _acts(w.project)
    assert {"session.lock", "session.unlock", "session.unlock_failed", "auth.reauth_failed"} <= set(acts)
    # configurable (admin only, audited)
    w.configure_idle_lock(5)
    assert w.project.idle_lock_minutes == 5 and "settings.idle_lock" in _acts(w.project)
    # lockout policy applies to unlocking: 5 wrong passwords lock the account, then even the right one fails
    w.lock_session()
    for _ in range(5):
        assert not w.unlock_session("wrong-password")
    assert not w.unlock_session(PW)
    assert "locked" in w.lock_page.error.text()
    w.project.store.exec("UPDATE users SET locked_until=0 WHERE id=?", (w.project.user["id"],))
    assert w.unlock_session(PW)


def test_audit_export_csv_json_with_verification(tmp_path, analysed):
    project, sid, scan = analysed
    res = S.export_audit(project, tmp_path / "audit.csv")
    lines = open(tmp_path / "audit.csv", encoding="utf-8").read().splitlines()
    assert lines[0].startswith("# OsteoQuant audit trail export; chain verification: OK")
    rows = list(csv.DictReader(lines[1:]))
    assert len(rows) == res["events"] and rows[0]["seq"] == "1"
    assert any(r["action"] == "scan.import" for r in rows)
    j = S.export_audit(project, tmp_path / "audit.json")
    data = json.loads(open(tmp_path / "audit.json").read())
    assert data["chain_verification"]["ok"] and data["chain_verification"]["events_verified"] >= j["events"]
    assert len(data["events"]) == j["events"]
    assert "audit.export" in _acts(project)
    # blinded export masks file names
    S.export_audit(project, tmp_path / "blind.json", blinded=True)
    assert "ph.nii" not in open(tmp_path / "blind.json").read()
    assert "ph.nii" in open(tmp_path / "audit.json").read()
    # analysts cannot export the audit trail
    project.add_user("ana", "A", "analyst", "Analyst-Pass-1")
    ana = login_as(project, "ana", "Analyst-Pass-1")
    with pytest.raises(PermissionError):
        S.export_audit(ana, tmp_path / "x.csv")
    ana.close()


def test_audit_export_reports_broken_chain(tmp_path, analysed):
    project, sid, scan = analysed
    c = project.store.conn
    c.execute("DROP TRIGGER IF EXISTS audit_no_update")
    trig = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='trigger'")]
    for t in trig:
        c.execute(f"DROP TRIGGER {t}")
    c.execute("UPDATE audit_log SET details='{\"tampered\": 1}' WHERE seq=3")
    S.export_audit(project, tmp_path / "a.csv")
    first = open(tmp_path / "a.csv", encoding="utf-8").readline()
    assert "BROKEN at event 3" in first
