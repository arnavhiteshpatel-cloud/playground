"""Tests that close traceability gaps (scripts/build_traceability.py): each asserts an aspect of an FS item of
docs/quality/FUNCTIONAL_SPEC.md that the existing tests exercised without asserting (audit events, refusals,
report and CSV content). They test existing behaviour; none of them changes the application."""
import csv
import datetime as dt
import json
import re
from pathlib import Path

import numpy as np
import pytest

from osteoquant.desktop import services as S

from desktop_helpers import DIR_PW, PW, REV_PW, login_as

ANA_PW = "Analyst-Pass-1"
VIEW_PW = "Viewer-Pass-12"


# ============================================================================ helpers
def _seg(project, scan):
    return project.store.segmentations(project.user, scan)[-1]


def _head(project) -> int:
    ev = project.store.audit.events(limit=1)
    return int(ev[0]["seq"]) if ev else 0


def _since(project, seq0, action=None) -> list[dict]:
    """Audit events after ``seq0`` in the order they were recorded (optionally of one action)."""
    ev = [e for e in project.store.audit.events(limit=100000) if int(e["seq"]) > seq0
          and (action is None or e["action"] == action)]
    return sorted(ev, key=lambda e: int(e["seq"]))


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def _pdf_pages(path) -> list[str]:
    import pypdfium2 as pdfium
    doc = pdfium.PdfDocument(str(path))
    return [_norm(doc[i].get_textpage().get_text_range()) for i in range(len(doc))]


def _pdf_text(path) -> str:
    return " ".join(_pdf_pages(path))


def _csv_rows(path) -> tuple[list[str], list[dict]]:
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    comments = [x for x in lines if x.startswith("#")]
    return comments, list(csv.DictReader(x for x in lines if not x.startswith("#")))


def _reopen(window, project, user="admin", pw=PW):
    folder = project.folder
    project.close()
    assert window.open_project(str(folder), user, pw)
    return window


def _edited_labels(project, scan):
    from osteoquant.desktop.volume_source import ZarrSource
    sc = project.store.scan(project.user, scan)
    seg = _seg(project, scan)
    lab = ZarrSource(sc["store_path"]).load_labels(seg["labels_key"]).copy()
    lab[10, 20:24, 20:24] = 2
    lab[11, 20:22, 20:22] = 0
    return seg, lab


# ============================================================================ FS-041-1 ROI save audit
def test_manual_roi_requires_reason_and_is_audited(qtbot, analysed):
    """FS-041-1: ROI saves are audited roi.save with version, definition hash, method and reason; the manual ROI
    dialog (and the service behind it) requires a reason."""
    from PySide6.QtWidgets import QDialog
    from osteoquant.desktop.dialogs import RoiDialog
    project, sid, scan = analysed
    # the automatic ROI saved by the analysis is audited with the same fields
    auto = project.store.roi_history(project.user, scan)
    assert [r["version"] for r in auto] == [1]
    ev = [e for e in project.store.audit.events(limit=100000)
          if e["action"] == "roi.save" and e["object_id"] == str(auto[0]["id"])]
    assert len(ev) == 1
    assert ev[0]["details"] == {"scan": scan, "version": 1, "def_sha256": auto[0]["def_sha256"],
                                "method": auto[0]["method"], "reason": "automatic detection"}
    # the dialog refuses to close without a typed reason
    d = RoiDialog((20, 28, 28), (40.0, 40.0, 40.0))
    qtbot.addWidget(d)
    for txt in ("", "   ", "ab"):
        d.reason.setText(txt)
        d.accept()
        assert d.result() != QDialog.Accepted and "reason is required" in d.error.text()
    d.reason.setText("drawn from landmarks")
    d.accept()
    assert d.result() == QDialog.Accepted
    # the service refuses as well, and nothing is stored or audited
    seq0 = _head(project)
    for bad in ("", "   ", "ab"):
        with pytest.raises(ValueError, match="reason"):
            S.save_cylinder_roi(project, scan, (20, 28, 28), 500, (-600, 600), reason=bad)
    assert len(project.store.roi_history(project.user, scan)) == 1
    assert _since(project, seq0, "roi.save") == []
    rid = S.save_cylinder_roi(project, scan, (20, 28, 28), 500, (-600, 600), reason="  drawn from landmarks ")
    row = project.store.latest_roi(project.user, scan)
    assert row["id"] == rid and row["version"] == 2 and row["method"] == "manual-desktop"
    assert row["reason"] == "drawn from landmarks" and len(row["def_sha256"]) == 64
    assert row["def_sha256"] == row["definition"]["definition_sha256"]
    ev = _since(project, seq0, "roi.save")
    assert len(ev) == 1
    assert ev[0]["object_type"] == "roi" and ev[0]["object_id"] == str(rid)
    assert ev[0]["user_id"] == str(project.user["id"])
    assert ev[0]["details"] == {"scan": scan, "version": 2, "def_sha256": row["def_sha256"],
                                "method": "manual-desktop", "reason": "drawn from landmarks"}


# ============================================================================ FS-052-1 versions
def test_automatic_prediction_is_version_1_and_base_labels_unchanged(analysed):
    """FS-052-1: the automated prediction is version 1 (kind=automatic); each correction is a new version
    (kind=corrected, parent_id) under a new labels key; earlier arrays are never overwritten."""
    from osteoquant.desktop.volume_source import ZarrSource
    from osteoquant.pipeline import labels_hash
    project, sid, scan = analysed
    sc = project.store.scan(project.user, scan)
    segs = project.store.segmentations(project.user, scan)
    assert len(segs) == 1
    v1 = segs[0]
    assert v1["version"] == 1 and v1["kind"] == "automatic" and v1["parent_id"] is None
    ev = [e for e in project.store.audit.events(limit=100000)
          if e["action"] == "segmentation.save" and e["object_id"] == str(v1["id"])]
    assert len(ev) == 1 and ev[0]["details"]["kind"] == "automatic" and ev[0]["details"]["version"] == 1
    base = ZarrSource(sc["store_path"]).load_labels(v1["labels_key"]).copy()
    assert labels_hash(base) == v1["labels_sha256"]
    lab2 = base.copy()
    lab2[10, 20:24, 20:24] = 2
    r2 = S.save_label_revision(project, scan, v1["id"], lab2, "first correction")
    lab3 = lab2.copy()
    lab3[12, 20:22, 20:22] = 0
    r3 = S.save_label_revision(project, scan, r2["segmentation_id"], lab3, "second correction")
    by_v = {s["version"]: s for s in project.store.segmentations(project.user, scan)}
    assert sorted(by_v) == [1, 2, 3] and (r2["version"], r3["version"]) == (2, 3)
    assert by_v[1]["kind"] == "automatic"
    assert by_v[2]["kind"] == by_v[3]["kind"] == "corrected"
    assert by_v[2]["parent_id"] == v1["id"] and by_v[3]["parent_id"] == by_v[2]["id"]
    assert len({by_v[v]["labels_key"] for v in (1, 2, 3)}) == 3            # a new key for every version
    fresh = ZarrSource(sc["store_path"])                                     # re-read from disk
    assert np.array_equal(fresh.load_labels(v1["labels_key"]), base)        # version 1 never overwritten
    assert np.array_equal(fresh.load_labels(by_v[2]["labels_key"]), lab2)
    assert np.array_equal(fresh.load_labels(by_v[3]["labels_key"]), lab3)
    assert by_v[1]["labels_sha256"] == v1["labels_sha256"]
    assert by_v[2]["labels_sha256"] == labels_hash(lab2) and by_v[3]["labels_sha256"] == labels_hash(lab3)


# ============================================================================ FS-075-2 unblinding
def test_desktop_unblind_requires_reason(qtbot, window, team):
    """FS-075-2: unblinding needs a stated reason (>= 5 characters) besides permission and password; it is
    offered in the desktop (Study > Unblind study) and audited study.unblind."""
    from PySide6.QtWidgets import QDialog
    from osteoquant.desktop.dialogs import UnblindDialog
    project, sid, scan, rid, did = team
    project.store.exec("UPDATE studies SET blinded=1 WHERE id=?", (sid,))
    dr = login_as(project, "dir", DIR_PW)
    seq0 = _head(project)
    for bad in (None, "", "     ", "abcd", "  ab c  "):
        with pytest.raises(ValueError, match="reason"):
            S.unblind_study(dr, DIR_PW, sid, bad)
    assert project.store.study(project.user, sid)["blinded"]
    acts = [e["action"] for e in _since(project, seq0)]
    assert "study.unblind" not in acts and "review.reauth_failed" not in acts    # refused before the password
    # the dialog does not accept a missing or short reason either
    d = UnblindDialog(dr.blinded_studies(), dr.user)
    qtbot.addWidget(d)
    for txt in ("", "abcd"):
        d.reason.setText(txt)
        d.accept()
        assert d.result() != QDialog.Accepted and "reason" in d.error.text()
    d.reason.setText("statistics plan executed")
    d.accept()
    assert d.result() == QDialog.Accepted
    dr.store.close()
    # available from the desktop for the study director, with the same reason rule
    w = window
    assert w.open_project(str(project.folder), "dir", DIR_PW)
    assert w.a_unblind.isEnabled()
    with pytest.raises(ValueError, match="reason"):
        w.unblind_study(sid, DIR_PW, "")
    assert [s["id"] for s in w.project.blinded_studies()] == [sid]
    assert w.unblind_study(sid, DIR_PW, "statistics plan executed")
    assert w.project.blinded_studies() == []
    ev = _since(w.project, seq0, "study.unblind")
    assert len(ev) == 1 and ev[0]["user_id"] == str(did)
    assert ev[0]["details"]["reason"] == "statistics plan executed" and ev[0]["details"]["signer"] == "dir"


# ============================================================================ FS-075-3 blinded review mode
def _visible_identity(w) -> str:
    """Text of the project tree (labels and tooltips), the Results rows and the viewer info bar."""
    parts = []

    def walk(it):
        parts.append(it.text(0) + " " + (it.toolTip(0) or ""))
        for i in range(it.childCount()):
            walk(it.child(i))
    for i in range(w.tree.topLevelItemCount()):
        walk(w.tree.topLevelItem(i))
    w.results.refresh()
    parts += [f"{r['scan']} {r['animal']} {r['group']}" for r in w.results.model.rows]
    parts.append(w.workspace.infobar.text())
    return " ".join(parts)


def test_blinded_mode_switch_records_ui_blinded_mode_event(qtbot, window, project, study, phantom_file):
    """FS-075-3: blinded review mode hides group names, animal IDs and file names in the tree, the results and the
    viewer, for every role; each switch is audited ui.blinded_mode."""
    gid = project.store.add_group(project.user, study, "HighDose-Arm")
    spec = S.get_or_create_specimen(project, study, "RAT-55", gid)
    o = S.import_scan(project, S.ImportRequest(str(phantom_file), (40, 40, 40), True, study, specimen_id=spec))
    assert o.scan_id, o.reason
    others = [("ana", "analyst", ANA_PW), ("rita", "reviewer", REV_PW), ("dora", "study_director", DIR_PW),
              ("vic", "viewer", VIEW_PW)]
    ids = {u: project.add_user(u, u.title(), role, pw) for u, role, pw in others}
    identity = ("HighDose-Arm", "RAT-55", "ph.nii")
    w = _reopen(window, project)
    assert w.open_scan(o.scan_id)
    shown = _visible_identity(w)
    assert all(x in shown for x in identity), shown
    seq0 = _head(w.project)
    w.set_blinded(True)
    hidden = _visible_identity(w)
    assert not any(x in hidden for x in identity), hidden
    assert "Scan S-" in hidden and "Animal A-" in hidden and "(blinded)" in hidden
    w.set_blinded(False)
    assert all(x in _visible_identity(w) for x in identity)
    ev = _since(w.project, seq0, "ui.blinded_mode")
    assert [e["details"] for e in ev] == [{"on": True}, {"on": False}]
    assert all(e["user_id"] == str(w.project.user["id"]) for e in ev)
    # every other role (the study is not flagged blinded, so each may switch): same hiding, switch audited
    for user, role, pw in others:
        assert w.open_project(str(w.project.folder), user, pw)
        assert w.project.user["role"] == role and w.a_blind.isEnabled() and not w.blinded_view
        assert w.open_scan(o.scan_id)
        assert all(x in _visible_identity(w) for x in identity), role
        seq1 = _head(w.project)
        w.set_blinded(True)
        assert not any(x in _visible_identity(w) for x in identity), role
        w.set_blinded(False)
        ev = _since(w.project, seq1, "ui.blinded_mode")
        assert [(e["user_id"], e["details"]) for e in ev] == [(str(ids[user]), {"on": True}),
                                                              (str(ids[user]), {"on": False})], role


# ============================================================================ FS-075-4 / FS-132-1 denied export
def test_blinded_download_denial_is_audited(team, tmp_path):
    """FS-075-4: reports generated with unblinded allocation are marked; their export is refused to users without
    the unblind permission and the refusal is audited report.blinded_download_denied."""
    project, sid, scan, rid, did = team
    spec = S.get_or_create_specimen(project, sid, "R01")
    project.store.exec("UPDATE scans SET specimen_id=?, source_name='R01_week4.nii.gz' WHERE id=?", (spec, scan))
    early = S.generate_report(project, sid)                 # study not yet blinded: identifying, not marked
    project.store.exec("UPDATE studies SET blinded=1 WHERE id=?", (sid,))
    unbl = S.generate_report(project, sid)                  # admin may unblind: unblinded allocation, marked
    blind = S.generate_report(project, sid, blinded=True)
    marks = {r["id"]: r for r in S.list_reports(project, sid)}
    assert marks[unbl["report_id"]]["unblinded"] == 1 and not marks[unbl["report_id"]]["blinded"]
    assert marks[early["report_id"]]["unblinded"] == 0
    assert marks[blind["report_id"]]["unblinded"] == 0 and marks[blind["report_id"]]["blinded"] == 1
    rev = login_as(project, "rev", REV_PW)
    out = tmp_path / "rev"
    out.mkdir()
    seq0 = _head(project)
    with pytest.raises(PermissionError, match="unblinded group allocation"):
        S.export_report(rev, unbl["report_id"], out)
    with pytest.raises(PermissionError, match="study is blinded"):
        S.export_report(rev, early["report_id"], out)
    assert list(out.iterdir()) == []
    ev = _since(project, seq0)
    denied = [e for e in ev if e["action"] == "report.blinded_download_denied"]
    assert [(e["object_type"], e["object_id"], e["user_id"]) for e in denied] == \
        [("report", str(unbl["report_id"]), str(rid)), ("report", str(early["report_id"]), str(rid))]
    assert denied[1]["details"] == {"reason": "blinded study, report not blinded"}
    assert "report.export" not in [e["action"] for e in ev]
    # the blinded report is exportable by the reviewer; the marked one by a user who may unblind
    assert S.export_report(rev, blind["report_id"], out)
    dr = login_as(project, "dir", DIR_PW)
    assert S.export_report(dr, unbl["report_id"], tmp_path)
    exported = [(e["object_id"], e["user_id"]) for e in _since(project, seq0, "report.export")]
    assert exported == [(str(blind["report_id"]), str(rid)), (str(unbl["report_id"]), str(did))]
    rev.store.close()
    dr.store.close()


def test_security_events_logged(project, study, tmp_path):
    """FS-132-1: sign-in success and failure and permission refusals of desktop actions are audited
    (auth.login, auth.login_failed, authz.denied); report.blinded_download_denied: see the test above."""
    from osteoquant.desktop.project import Project
    rev_id = project.add_user("rev", "Rita Reviewer", "reviewer", REV_PW)
    vic_id = project.add_user("vic", "Victor Viewer", "viewer", VIEW_PW)
    admin_id = project.user["id"]
    seq0 = _head(project)
    p = Project(project.folder)
    assert not p.login("admin", "Wrong-Password-1")
    assert not p.login("nobody", "Wrong-Password-1")
    assert p.login("rev", REV_PW)
    failed = _since(project, seq0, "auth.login_failed")
    assert [(e["user_id"], e["details"]["reason"]) for e in failed] == \
        [(str(admin_id), "bad password"), (None, "unknown/inactive/temporarily locked")]
    assert failed[1]["details"]["username"] == "nobody"
    assert [e["user_id"] for e in _since(project, seq0, "auth.login")] == [str(rev_id)]
    # permission refusals of desktop actions
    with pytest.raises(PermissionError):
        S.unblind_study(p, REV_PW, study, "a reviewer tries to unblind")
    with pytest.raises(PermissionError):
        p.create_study("Reviewer study")
    v = login_as(project, "vic", VIEW_PW)
    with pytest.raises(PermissionError):
        S.export_audit(v, tmp_path / "audit.csv")
    assert not (tmp_path / "audit.csv").exists()
    denied = [(e["user_id"], e["details"]) for e in _since(project, seq0, "authz.denied")]
    assert denied == [(str(rev_id), {"perm": "unblind"}), (str(rev_id), {"perm": "write"}),
                      (str(vic_id), {"perm": "audit.export"})]
    assert project.store.audit.verify_chain()["ok"]
    p.close()
    v.close()


# ============================================================================ FS-091-1 signatures
def test_signature_meaning_rule_and_review_panel_history(qtbot, team):
    """FS-091-1: a signature needs a meaning of at least 5 characters; the review record stores reviewer, UTC time,
    decision, meaning and comment; the Review panel lists the history of the selected version."""
    from osteoquant.desktop.review_audit import ReviewPanel
    project, sid, scan, rid, did = team
    seg = _seg(project, scan)
    rev = login_as(project, "rev", REV_PW)
    seq0 = _head(project)
    for bad in (None, "", "     ", "abcd", "  ab c  "):
        with pytest.raises(ValueError, match="meaning"):
            S.sign_review(rev, REV_PW, "segmentation", seg["id"], "approved", bad)
    assert project.store.reviews(project.user, "segmentation", seg["id"]) == []
    assert not [e for e in _since(project, seq0) if e["action"].startswith("review.")]
    t0 = dt.datetime.now(dt.timezone.utc)
    r1 = S.sign_review(rev, REV_PW, "segmentation", seg["id"], "needs_changes", "  check the graft rim  ",
                       comment="rim at slice 10")
    r2 = S.sign_review(rev, REV_PW, "segmentation", seg["id"], "approved", "approve segmentation for reporting")
    revs = project.store.reviews(project.user, "segmentation", seg["id"])
    assert [r["id"] for r in revs] == [r1, r2]
    first = revs[0]
    assert (first["reviewer_id"], first["decision"], first["meaning"], first["comment"]) == \
        (rid, "needs_changes", "check the graft rim", "rim at slice 10")
    assert re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", first["created"])          # UTC, ISO 8601
    t = dt.datetime.strptime(first["created"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    assert abs((t - t0).total_seconds()) < 600
    # Review panel: the history of the selected version, oldest first, comment on hover
    rp = ReviewPanel()
    qtbot.addWidget(rp)
    rp.set_scan(project, scan)
    assert rp.selected_segmentation()["id"] == seg["id"]
    h = rp.history
    assert [h.horizontalHeaderItem(c).text() for c in range(h.columnCount())] == \
        ["Time (UTC)", "Reviewer", "Signature role", "Decision", "Meaning"]
    cells = [[h.item(r, c).text() for c in range(h.columnCount())] for r in range(h.rowCount())]
    assert cells == [[first["created"], "Rita Reviewer", "Scientific reviewer", "needs changes", "check the graft rim"],
                     [revs[1]["created"], "Rita Reviewer", "Scientific reviewer", "approved",
                      "approve segmentation for reporting"]]
    assert h.item(0, 4).toolTip() == "rim at slice 10"
    assert rp.table.item(rp.table.rowCount() - 1, 4).text() == "approved (rev)"
    rev.store.close()


# ============================================================================ FS-111-2 pickled models
def test_desktop_refuses_pickled_rf_models(project, study, phantom_file, tmp_path, monkeypatch):
    """FS-111-2: the desktop refuses pickled random-forest models (rf:), even with the CLI's trusted-local flag;
    the analysis job is never started and nothing is stored."""
    import osteoquant.study.handlers as H
    o = S.import_scan(project, S.ImportRequest(str(phantom_file), (40, 40, 40), True, study))
    assert o.scan_id, o.reason
    model = tmp_path / "rf_model.joblib"
    model.write_bytes(b"pickled model that must never be loaded")
    started = []
    monkeypatch.setattr(H, "job_analyze", lambda *a, **k: started.append(a) or {"status": "complete_unreviewed"})
    seq0 = _head(project)
    for cfg in ({"segmentation": f"rf:{model}"}, {"segmentation": f"rf:{model}", "_trusted_local": True}):
        with pytest.raises(PermissionError, match="command line"):
            S.analyze_scan(project, o.scan_id, cfg)
    assert started == []
    assert project.store.segmentations(project.user, o.scan_id) == []
    assert project.store.q("SELECT id FROM measurements WHERE scan_id=?", (o.scan_id,)) == []
    assert not [e for e in _since(project, seq0) if e["action"] in ("segmentation.save", "measurement.save")]
    assert not any(m["id"].startswith("rf:") for m in S.available_models())   # only locked ONNX models offered


# ============================================================================ FS-001-2 RUO statement
def test_pdf_and_csv_text_contain_ruo_statement(team):
    """FS-001-2: every page of the desktop PDF carries the RUO / not-validated statement; the CSV carries the data
    class and the review status (unreviewed, then reviewed after the segmentation is approved)."""
    project, sid, scan, rid, did = team
    statement = ("Research use only. Not a medical device. Not validated for GLP studies (21 CFR 58 / OECD GLP). "
                 "No claim of 21 CFR Part 11 compliance.")
    footer = "Research use only · not a medical device · not validated for GLP or 21 CFR Part 11"
    rep = S.generate_report(project, sid)
    pages = _pdf_pages(rep["pdf"])
    assert len(pages) >= 2 and statement in pages[0] and "RESEARCH DATA" in pages[0]
    assert all(footer in p for p in pages)
    assert "UNREVIEWED AUTOMATED RESULT" in pages[0]
    comments, rows = _csv_rows(rep["csv"])
    assert "data class: research" in comments[0] and "unreviewed_automated" in comments[0] and footer in comments[0]
    assert rows and all(r["data_class"] == "research" and r["review_status"] == "unreviewed_automated" for r in rows)
    rev = login_as(project, "rev", REV_PW)
    S.sign_review(rev, REV_PW, "segmentation", _seg(project, scan)["id"], "approved", "approve segmentation")
    rep2 = S.generate_report(project, sid)
    pages2 = _pdf_pages(rep2["pdf"])
    assert statement in pages2[0] and all(footer in p for p in pages2)
    assert "see sign-off section for reviewer identity" in pages2[0] and "UNREVIEWED" not in pages2[0]
    comments2, rows2 = _csv_rows(rep2["csv"])
    assert "data class: research" in comments2[0] and "· reviewed ·" in comments2[0]
    assert rows2 and all(r["data_class"] == "research" and r["review_status"] == "reviewed" for r in rows2)
    rev.store.close()


# ============================================================================ FS-080-1 report content
def test_report_provenance_section_complete(analysed):
    """FS-080-1: the desktop PDF prints the software version, the corrections table of a corrected segmentation, the
    measurement-support section, the reproducibility block with the analysis configuration hash, and the sign-off
    table."""
    from osteoquant import __version__
    project, sid, scan = analysed
    seg, lab = _edited_labels(project, scan)
    r = S.save_label_revision(project, scan, seg["id"], lab, "graft rim relabelled")
    rep = S.generate_report(project, sid)
    bundle = json.loads(Path(S.report_meta(project, rep["report_id"])["bundle_path"]).read_text(encoding="utf-8"))
    corr = bundle["specimens"][0]["corrections"]
    assert [c["version"] for c in corr] == [r["version"]] and corr[0]["summary"] == r["voxel_count_change"]
    text = _pdf_text(rep["pdf"])
    assert "RESEARCH DATA" in text and "Research use only" in text                       # banner
    assert "1. Study overview" in text and "S1" in text and "Data class research" in text
    assert f"Software OsteoQuant {__version__}" in text                                  # software version
    assert "4. Per-specimen results" in text
    i7, i_sup = text.index("7. Human correction history"), text.index("Measurement support (identifiability)")
    corrections = text[i7:i_sup]
    assert "Edit summary" in corrections and "No manual corrections were recorded" not in corrections
    for cls in r["voxel_count_change"]:                                                  # the edit summary
        assert cls in corrections
    assert "supported with conditions" in text[i_sup:]                                   # support section legend
    i9, i10 = text.index("9. Reproducibility"), text.index("10. Review and sign-off")
    repro = text[i9:i10]
    assert "software_version" in repro and __version__ in repro and "git_commit" in repro
    # the configuration hash each specimen was analysed with (FS-080-1), without specimen identifiers
    cfg = bundle["reproducibility"]["analysis_config_sha256"]
    h = bundle["specimens"][0]["config_sha256"]
    assert h and len(h) == 64 and h in cfg and "specimen" in cfg
    assert "analysis_config_sha256" in repro and h[:24] in repro.replace("\n", "").replace("\r", "")
    signoff = text[i10:]
    assert all(role in signoff for role in ("Analyst", "Scientific reviewer", "Customer approver"))


# ============================================================================ FS-152-1 results support
def test_results_csv_contains_support_columns(qtbot, team, tmp_path):
    """FS-152-1: the Results tab shows a Support column (supported / flagged / not supported / not analysed), shows
    unsupported values as 'not measured' with the reason on hover, and the CSV has per-endpoint support columns."""
    from PySide6.QtCore import Qt
    from desktop_helpers import current_assessment
    from osteoquant.desktop.results_view import NOT_ANALYSED, NOT_MEASURED, ResultsView
    from osteoquant.desktop.support import ENDPOINTS, FLAGGED, NOT_SUPPORTED, SUPPORTED
    project, sid, scan, rid, did = team
    np.save(tmp_path / "b.npy", np.random.default_rng(1).normal(400, 30, (20, 20, 20)).astype(np.float32))
    o = S.import_scan(project, S.ImportRequest(str(tmp_path / "b.npy"), (40, 40, 40), True, sid))
    assert o.scan_id, o.reason
    rv = ResultsView()
    qtbot.addWidget(rv)
    rv.set_project(project, sid)
    m = rv.model
    headers = [m.headerData(c, Qt.Horizontal) for c in range(m.columnCount())]
    c_sup, c_tv = headers.index("Support"), headers.index("Defect TV (mm³)")

    def cell(scan_id, col, role=Qt.DisplayRole):
        row = next(i for i, r in enumerate(m.rows) if r["scan_id"] == scan_id)
        return m.data(m.index(row, col), role)
    # analysed, automatic ROI not yet accepted: flagged, the value is shown with the reason on hover
    assert cell(scan, c_sup).endswith(FLAGGED) and "ROI not yet accepted" in cell(scan, c_sup, Qt.ToolTipRole)
    assert cell(scan, c_tv) != NOT_MEASURED
    assert cell(scan, c_tv, Qt.ToolTipRole).startswith(f"Defect TV: {FLAGGED}")
    assert cell(o.scan_id, c_sup) == NOT_ANALYSED
    # ROI accepted by a reviewer, QC suitable and every endpoint supported by a current assessment: supported
    rev = login_as(project, "rev", REV_PW)
    S.sign_review(rev, REV_PW, "roi", _seg(project, scan)["roi_id"], "approved", "accept the ROI as analysis volume")
    rev.store.close()
    mr = project.store.q1("SELECT id, metrics FROM measurements WHERE scan_id=? ORDER BY id DESC LIMIT 1", (scan,))
    met = json.loads(mr["metrics"])
    adv = {ep: {"status": "supported"} for ep in ("graft_fraction_of_defect", "new_bone_volume", "residual_graft_volume",
                                                  "new_bone_fraction_of_defect", "new_bone_thickness",
                                                  "mineral_fraction_of_defect", "total_mineral_volume")}
    good = {**json.loads(mr["metrics"]), **current_assessment(adv), "qc": {"verdict": "suitable"}, "plausibility": []}
    for k in ("metrics", "reported_metrics"):
        good[k]["class_volumes"]["uncertain_fraction"] = 0.0
    good["suppressed_metrics"] = []
    project.store.exec("UPDATE measurements SET metrics=? WHERE id=?", (json.dumps(good), mr["id"]))
    rv.refresh()
    assert cell(scan, c_sup) == SUPPORTED, cell(scan, c_sup, Qt.ToolTipRole)
    assert cell(scan, c_tv) != NOT_MEASURED and cell(scan, c_tv, Qt.ToolTipRole).startswith(f"Defect TV: {SUPPORTED}")
    # every endpoint not supported (uncertain fraction > 25 %): no number, the reason on hover
    for k in ("metrics", "reported_metrics"):
        met[k]["class_volumes"]["uncertain_fraction"] = 0.6
    project.store.exec("UPDATE measurements SET metrics=? WHERE id=?", (json.dumps(met), mr["id"]))
    rv.refresh()
    assert cell(scan, c_sup).endswith(NOT_SUPPORTED)
    assert cell(scan, c_tv) == NOT_MEASURED
    tip = cell(scan, c_tv, Qt.ToolTipRole)
    assert tip.startswith(f"Defect TV: {NOT_SUPPORTED}") and "uncertain fraction" in tip
    # CSV: one support and one reasons column per endpoint
    p = rv.export_csv(str(tmp_path / "results.csv"))
    with open(p, encoding="utf-8", newline="") as f:
        rd = csv.DictReader(f)
        rows = {r["Scan"]: r for r in rd}
        hdr = rd.fieldnames
    for _, label, *_ in ENDPOINTS:
        assert f"{label} support" in hdr and f"{label} reasons" in hdr
    a = rows[project.store.scan(project.user, scan)["source_name"]]
    assert a["Support"] == NOT_SUPPORTED and a["Defect TV (mm³)"] == ""
    assert all(a[f"{label} support"] == NOT_SUPPORTED for _, label, *_ in ENDPOINTS)
    assert "uncertain fraction" in a["Defect TV reasons"]
    b = rows["b.npy"]
    assert b["Support"] == NOT_ANALYSED and b["Defect TV support"] == NOT_SUPPORTED
    assert b["Defect TV reasons"] == "analysis not run"
