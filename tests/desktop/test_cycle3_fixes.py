"""Cycle-3 product review fixes: audit-trail authority, single generation record, external anchors (C3-PRD-03)."""
import json

import pytest

from osteoquant.desktop import services as S
from desktop_helpers import PW, REV_PW


def test_self_recorded_role_change_is_ignored_and_login_refused(team):
    """Probe 3 of the review: a user appends a correctly hashed role_change event for themself and edits the
    users row. The audited state ignores a change not recorded by another administrator, so sign-in is refused."""
    from osteoquant.desktop.project import Project
    project, sid, scan, rev_id, _ = team
    st = project.store
    st.audit.record("user.role_change", rev_id, project.user["org_id"], "user", rev_id,
                    {"username": "rev", "old_role": "reviewer", "new_role": "admin"})
    st.exec("UPDATE users SET role='admin' WHERE id=?", (rev_id,))
    assert st.audit.verify_chain()["ok"]                       # the chain alone cannot see an append
    assert st.audited_user_state(rev_id)["role"] == "reviewer"
    p2 = Project(project.folder)
    assert not p2.login("rev", REV_PW)
    p2.close()


def test_admin_recorded_role_change_still_counts(team):
    project, sid, scan, rev_id, _ = team
    project.store.set_user_role(project.user, rev_id, "analyst")
    assert project.store.audited_user_state(rev_id)["role"] == "analyst"


def test_appended_second_generate_event_fails_report_integrity(team):
    """Probe 4: an appended report.generate event with the hash of a forged bundle used to win (newest event)."""
    from osteoquant.desktop.report_integrity import ReportIntegrityError, verify_report
    project, sid, scan, _, _ = team
    rep = S.generate_report(project, sid)
    verify_report(project, rep["report_id"])                    # untouched report verifies
    project.store.audit.record("report.generate", project.user["id"], project.user["org_id"], "report",
                               rep["report_id"], {"sha256": "0" * 64, "bundle_sha256": "1" * 64})
    with pytest.raises(ReportIntegrityError, match="more than one generation record"):
        verify_report(project, rep["report_id"])


def test_report_prints_audit_anchor_and_anchor_file_is_written(team, tmp_path):
    import pypdfium2 as pdfium
    from osteoquant.desktop.anchors import stored_anchors
    project, sid, scan, _, _ = team
    rep = S.generate_report(project, sid)
    doc = pdfium.PdfDocument(rep["pdf"])
    text = "\n".join(doc[i].get_textpage().get_text_range() for i in range(len(doc)))
    assert "Audit trail at generation: event" in text
    anchors = stored_anchors(project.store)
    assert anchors and anchors[-1]["event"] == "report.generate"
    assert str(tmp_path / "anchors") not in str(project.folder)      # anchors live outside the project folder


def test_rewritten_trail_disables_signatures(team):
    """Truncating or rewriting the trail after an anchor was recorded is detected at sign-in; signatures refused."""
    from osteoquant.desktop.anchors import record_anchor
    from osteoquant.desktop.project import Project
    project, sid, scan, _, _ = team
    a = record_anchor(project, "test")
    project.store.audit.record("noise", project.user["id"], project.user["org_id"], "project", None, {})
    c = project.store.conn
    c.execute("DROP TRIGGER audit_no_delete")
    c.execute("DELETE FROM audit_log WHERE seq>=?", (a["seq"],))      # history rewritten from the anchor onwards
    c.commit()
    p2 = Project(project.folder)
    assert p2.login("admin", PW)
    assert p2.integrity_problems and "no longer matches the anchor" in p2.integrity_problems[0]
    seg = p2.store.segmentations(p2.user, scan)[-1]
    with pytest.raises(PermissionError, match="audit trail no longer matches"):
        S.sign_review(p2, PW, "segmentation", seg["id"], "approved", "approve for reporting")
    acts = [e["action"] for e in p2.store.audit.events()]
    assert "audit.anchor_mismatch" in acts
    p2.close()


def test_stale_and_unbound_records_show_not_assessed_in_report(team):
    """C3-PRD-01: a record stored before method binding (multi-Otsu, no rule stamp) is not reported as supported."""
    project, sid, scan, _, _ = team
    st = project.store
    m = st.q1("SELECT id, metrics FROM measurements WHERE scan_id=? ORDER BY id DESC LIMIT 1", (scan,))
    res = json.loads(m["metrics"])
    res["segmentation"] = dict(res.get("segmentation") or {}, method="multiotsu")
    ms = res["measurement_support"]
    ms.pop("support_rules", None)
    ms.pop("method_binding", None)
    for d in ms["endpoints"].values():
        d["status"] = "supported"
    st.exec("UPDATE measurements SET metrics=? WHERE id=?", (json.dumps(res), m["id"]))
    import csv as _csv
    rep = S.generate_report(project, sid)
    rows = list(_csv.DictReader(r for r in open(rep["csv"]) if not r.startswith("#")))
    assert len(rows) == 1
    row = rows[0]
    for key in ("class_volumes.residual_graft_fraction", "class_volumes.mineral_volume_mm3"):
        assert row[key + "__support"] in ("not_assessed", "not_supported"), row[key + "__support"]
        assert row[key] in ("", "None", "nan")


def test_memory_preflight_refuses_before_loading(analysed):
    """C3-PRD-20: an analysis that cannot fit in memory is refused with a clear message, not killed by the OS."""
    project, sid, scan = analysed
    with pytest.raises(MemoryError, match="needs about"):
        S._memory_preflight(project, scan, available=1024)
    S._memory_preflight(project, scan, available=10 ** 12)          # plenty: no error


def test_report_audit_excerpt_names_users(team):
    """C3-PRD-17: the audit excerpt shows who acted, not only a numeric user id."""
    import re

    import pypdfium2 as pdfium
    project, sid, scan, _, _ = team
    rep = S.generate_report(project, sid)
    doc = pdfium.PdfDocument(rep["pdf"])
    text = "\n".join(doc[i].get_textpage().get_text_range() for i in range(len(doc)))
    u = project.store.q1("SELECT username, full_name FROM users WHERE id=?", (project.user["id"],))
    name = u["full_name"] or u["username"]
    assert re.search(rf"{re.escape(name)}\s*\({project.user['id']}\)", text)


def test_schema_change_at_project_open_is_audited(tmp_path):
    """C3-PRD-21: opening a project before sign-in may add desktop tables or columns; that change is audited, and
    opening an up-to-date project changes nothing."""
    import sqlite3

    from osteoquant.desktop.project import DB_NAME, Project
    Project.create(tmp_path / "proj", "Schema", "admin", PW).close()
    p = Project(tmp_path / "proj")
    assert not [e for e in p.store.audit.events(limit=10 ** 6) if e["action"] == "project.schema_upgrade"]
    p.close()                                                       # created complete: opening changes nothing
    con = sqlite3.connect(tmp_path / "proj" / DB_NAME)
    con.execute("DROP TABLE desktop_review_meta")
    con.commit()
    con.close()
    p = Project(tmp_path / "proj")
    ev = [e for e in p.store.audit.events(limit=10 ** 6) if e["action"] == "project.schema_upgrade"]
    assert len(ev) == 1 and ev[0]["details"]["added"] == ["desktop_review_meta"]
    assert p.store.audit.verify_chain()["ok"]
    p.close()
