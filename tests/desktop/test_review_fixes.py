"""Cycle-1 UX review: tests for every High finding (UX-01 ... UX-10)."""
import json

import numpy as np
import pytest

from osteoquant.desktop import services as S
from osteoquant.desktop.support import FLAGGED, NOT_SUPPORTED, SUPPORTED, endpoint_value, measurement_support

from desktop_helpers import DIR_PW, PW, REV_PW, login_as


def _pdf_text(path) -> str:
    import pypdfium2 as pdfium
    doc = pdfium.PdfDocument(str(path))
    return "\n".join(doc[i].get_textpage().get_text_range() for i in range(len(doc)))


def _seg(project, scan):
    return project.store.segmentations(project.user, scan)[-1]


def _reopen(window, project, user="admin", pw=PW):
    folder = project.folder
    project.close()
    assert window.open_project(str(folder), user, pw)
    return window


# ----------------------------------------------------------------------------- UX-01 ROI shown
def test_ux01_roi_drawn_in_slice_views_and_3d(qtbot, window, analysed):
    project, sid, scan = analysed
    w = _reopen(window, project)
    assert w.open_scan(scan)
    st = w.state
    assert st.roi is not None and st.roi.any() and st.roi.shape == tuple(st.shape)
    z = int(np.argwhere(st.roi).mean(0)[0])
    st.set_cursor(z, *st.cursor[1:])
    ax = w.workspace.views[0]
    assert ax._roi_edges is not None and len(ax._roi_edges) > 20

    def yellow(img):
        a = np.array([[img.pixelColor(x, y).getRgb()[:3] for x in range(0, img.width(), 2)]
                      for y in range(0, img.height(), 2)])
        return int(((abs(a[..., 0] - 240) < 30) & (abs(a[..., 1] - 228) < 30) & (a[..., 2] < 120)).sum())

    assert yellow(ax.render_image()) > 20
    assert w.workspace.view3d.roi_actor is not None and w.workspace.view3d.roi_actor.GetVisibility()
    w.display.show_roi.setChecked(False)               # toggle (also key R)
    assert not st.show_roi and not w.workspace.view3d.roi_actor.GetVisibility()
    assert yellow(ax.render_image()) < 5


# ----------------------------------------------------------------------------- UX-02 accept ROI
def test_ux02_accept_roi_is_signed_audited_and_clears_flag(team):
    from osteoquant.desktop.results_view import build_rows
    project, sid, scan, rid, did = team
    roi_id = _seg(project, scan)["roi_id"]
    st0 = S.roi_state(project, roi_id)
    assert st0["requires_review"] and st0["status"] == "awaiting acceptance"
    row = build_rows(project, sid)[0]
    assert "awaiting acceptance" in row["roi"]
    assert any("ROI not yet accepted" in r for r in row["values"]["TV_mm3"]["reasons"])
    # the admin ran the analysis that created the ROI: separation of duties
    with pytest.raises(PermissionError, match="ROI"):
        S.sign_review(project, PW, "roi", roi_id, "approved", "accept the ROI as analysis volume")
    rev = login_as(project, "rev", REV_PW)
    S.sign_review(rev, REV_PW, "roi", roi_id, "approved", "accept the ROI as analysis volume")
    st1 = S.roi_state(project, roi_id)
    assert st1["accepted"] and st1["status"] == "accepted"
    ev = [e for e in project.store.audit.events() if e["action"] == "review.approved" and e["object_type"] == "roi"]
    assert ev and ev[0]["details"]["object_sha256"] == st1["roi"]["def_sha256"]
    row = build_rows(project, sid)[0]
    assert "accepted" in row["roi"]
    assert not any("ROI not yet accepted" in r for r in row["values"]["TV_mm3"]["reasons"])
    rev.store.conn.close()


def test_ux02_review_panel_accept_and_edit_buttons(qtbot, window, team):
    project, sid, scan, rid, did = team
    w = _reopen(window, project)
    w.open_scan(scan)
    rp = w.review
    assert not rp.accept_roi.isEnabled() and "Separation of duties" in rp.accept_roi.toolTip()
    assert rp.edit_roi.isEnabled()                       # admin may write
    assert "awaiting acceptance" in rp.roi_label.text()


# ----------------------------------------------------------------------------- UX-03 / UX-04 status semantics
def test_ux03_not_supported_never_yields_a_number():
    res = {"metrics": {"class_volumes": {"TV_mm3": 3.0, "new_bone_fraction": 0.33, "uncertain_fraction": 0.5},
                       "new_bone_architecture": {"Tb_Th_um": 100}}}
    sup = measurement_support(res)
    for key in ("TV_mm3", "new_bone_fraction"):
        v, st, reasons = endpoint_value(res, sup, key)
        assert v is None and st == NOT_SUPPORTED and any("uncertain fraction" in r for r in reasons)
    # advisor reasons appear once, with or without the "advisor:" prefix (UX-11)
    res2 = {"metrics": {"class_volumes": {"TV_mm3": 3.0, "uncertain_fraction": 0.0}},
            "reported_metrics": {"class_volumes": {"TV_mm3": 3.0, "new_bone_volume_mm3": None}},
            "suppressed_metrics": [{"metric": "class_volumes.new_bone_volume_mm3", "reason": "graft overlaps bone"}],
            "measurement_support": {"endpoints": {"new_bone_volume": {"status": "not_supported",
                                                                      "reason": "graft overlaps bone"}}}}
    v, st, reasons = endpoint_value(res2, measurement_support(res2), "new_bone_volume_mm3")
    assert v is None and sum("graft overlaps bone" in r for r in reasons) == 1


def test_ux03_results_csv_and_report_have_no_number_for_not_supported(qtbot, analysed, tmp_path):
    from osteoquant.desktop.results_view import ResultsView, build_rows
    project, sid, scan = analysed
    m = project.store.q1("SELECT id, metrics FROM measurements WHERE scan_id=? ORDER BY id DESC LIMIT 1", (scan,))
    met = json.loads(m["metrics"])
    met["metrics"]["class_volumes"]["uncertain_fraction"] = 0.6        # > 25 %: every endpoint not supported
    met["reported_metrics"]["class_volumes"]["uncertain_fraction"] = 0.6
    tv = met["reported_metrics"]["class_volumes"]["TV_mm3"]
    project.store.exec("UPDATE measurements SET metrics=? WHERE id=?", (json.dumps(met), m["id"]))
    row = build_rows(project, sid)[0]
    assert all(c["value"] is None for c in row["values"].values())
    rv = ResultsView()
    qtbot.addWidget(rv)
    rv.set_project(project, sid)
    p = rv.export_csv(str(tmp_path / "r.csv"))
    lines = open(p, encoding="utf-8").read().splitlines()
    hdr = lines[0].split(",")
    vals = lines[1].split(",")
    i = hdr.index("Defect TV (mm³)")
    assert vals[i] == "" and f"{tv:.4g}" not in lines[1]
    rep = S.generate_report(project, sid)
    bundle = json.loads(open(S.report_meta(project, rep["report_id"])["bundle_path"]).read())
    assert bundle["specimens"][0]["metrics"]["class_volumes"]["TV_mm3"] is None
    assert any(d["metric"] == "class_volumes.TV_mm3" for d in bundle["specimens"][0]["suppressed_metrics"])


def test_ux04_qc_review_is_never_green():
    base = {"metrics": {"class_volumes": {"uncertain_fraction": 0.0}, "new_bone_architecture": {"Tb_Th_um": 100}}}
    assert measurement_support(base)["overall"] == SUPPORTED
    rq = {**base, "qc": {"verdict": "review", "checks": [{"name": "Noise level", "status": "warn"}]}}
    sup = measurement_support(rq)
    assert sup["overall"] == FLAGGED
    assert all(e["status"] != SUPPORTED for e in sup["endpoints"].values())
    assert any("QC verdict 'review'" in r and "Noise level" in r for r in sup["endpoints"]["TV_mm3"]["reasons"])
    bad = {**base, "qc": {"verdict": "unsuitable", "checks": [{"name": "Spacing", "status": "fail"}]}}
    assert all(e["status"] != SUPPORTED for e in measurement_support(bad)["endpoints"].values())


# ----------------------------------------------------------------------------- UX-05 synthetic-trained label
def test_ux05_synthetic_model_labelled_everywhere(qtbot, window, analysed, monkeypatch):
    from osteoquant.desktop.dialogs import AnalysisDialog
    from osteoquant.desktop.results_view import build_rows
    project, sid, scan = analysed
    info = S.segmentation_method_info({"method": "onnx:unet_noctx_s0", "model_name": "unet_noctx_s0"},
                                      {"segmentation": {"model_provenance": ["synthetic"]}})
    assert info["synthetic"] and "SYNTHETIC-TRAINED" in info["text"] and "[" not in info["provenance"]
    assert S.provenance_words(["synthetic"]) == "trained on synthetic phantoms"
    monkeypatch.setattr(S, "available_models", lambda: [{"id": "onnx:m1", "name": "m1", "licence_tag": "x",
                                                         "provenance": ["synthetic"], "synthetic": True,
                                                         "provenance_text": "trained on synthetic phantoms"}])
    d = AnalysisDialog(1)
    qtbot.addWidget(d)
    assert "SYNTHETIC-TRAINED" in d.seg.itemText(1) and "commercial" not in str(d.seg.itemData(1, 3))
    d.seg.setCurrentIndex(1)
    assert not d.chip.isHidden()
    # a stored segmentation made with a synthetic-trained model
    seg = _seg(project, scan)
    project.store.exec("UPDATE segmentations SET method='onnx:unet_noctx_s0', model_name='unet_noctx_s0' WHERE id=?",
                       (seg["id"],))
    m = project.store.q1("SELECT id, metrics FROM measurements WHERE segmentation_id=?", (seg["id"],))
    met = json.loads(m["metrics"])
    met["segmentation"]["model_provenance"] = ["synthetic"]
    project.store.exec("UPDATE measurements SET metrics=? WHERE id=?", (json.dumps(met), m["id"]))
    row = build_rows(project, sid)[0]
    assert row["synthetic"] and "SYNTHETIC-TRAINED" in row["method"]
    w = _reopen(window, project)
    w.open_scan(scan)
    assert not w.workspace.chip.isHidden() and "SYNTHETIC-TRAINED" in w.workspace.chip.text()
    assert "SYNTHETIC-TRAINED" in w.review.table.item(0, 2).text()


# ----------------------------------------------------------------------------- UX-06 what changed
def test_ux06_version_detail_and_compare_overlay(qtbot, window, analysed):
    project, sid, scan = analysed
    seg = _seg(project, scan)
    lab = S.load_scan_layers(project.store.scan(project.user, scan)["store_path"], seg)["labels"]
    lab2 = lab.copy()
    lab2[10, 20:24, 20:24] = 2
    S.save_label_revision(project, scan, seg["id"], lab2, "graft particle at the margin", {"brush2d": 1})
    new = _seg(project, scan)
    d = S.version_detail(project, new["id"])
    assert d["parent_version"] == seg["version"] and d["reason"] == "graft particle at the margin"
    by = {c["class"]: c for c in d["classes"]}
    n_changed = int((lab2 != lab).sum())
    assert by["residual graft"]["voxels"] == int((lab2 == 2).sum() - (lab == 2).sum())
    assert by["residual graft"]["mm3"] == pytest.approx(by["residual graft"]["voxels"] * 40 ** 3 / 1e9)
    assert {e["key"] for e in d["endpoints"]} >= {"TV_mm3", "new_bone_fraction"}
    w = _reopen(window, project)
    w.open_scan(scan)
    rp = w.review
    rp.table.selectRow(rp.table.rowCount() - 1)
    html = rp.detail.toPlainText()
    assert "graft particle at the margin" in html and "derived from" in html and "mm" in html
    rp.compare.setChecked(True)
    assert w.state.compare_mask is not None and int(w.state.compare_mask.sum()) == n_changed
    rp.compare.setChecked(False)
    assert w.state.compare_mask is None


# ----------------------------------------------------------------------------- UX-07 / UX-08 report sign-off
def test_ux07_08_report_signoff_roles_gates_and_signed_rows(qtbot, team):
    project, sid, scan, rid, did = team
    rev = login_as(project, "rev", REV_PW)
    dr = login_as(project, "dir", DIR_PW)
    early = S.generate_report(project, sid)
    with pytest.raises(PermissionError, match="not approved yet"):     # segmentation not approved yet
        S.sign_review(dr, DIR_PW, "report", early["report_id"], "approved", "approve the report release",
                      signature_role="study_director")
    S.sign_review(dr, DIR_PW, "report", early["report_id"], "needs_changes", "segmentations need review first",
                  signature_role="study_director")
    seg = _seg(project, scan)
    S.sign_review(rev, REV_PW, "segmentation", seg["id"], "approved", "approve segmentation for reporting")
    with pytest.raises(PermissionError, match="generated before"):     # report content still says UNREVIEWED
        S.sign_review(dr, DIR_PW, "report", early["report_id"], "approved", "approve the report release",
                      signature_role="study_director")
    rep = S.generate_report(project, sid)
    # UX-08: the author of a report gets a report-specific message
    with pytest.raises(PermissionError, match="report you generated"):
        S.sign_review(project, PW, "report", rep["report_id"], "approved", "approve the report release")
    from osteoquant.study.db import Store
    st = Store(project.folder / "osteoquant.db", project.folder / "data")
    admin = st.q1("SELECT id, org_id, username, role FROM users WHERE username='admin'")
    rid_row = st.q1("SELECT created_by FROM reports WHERE id=?", (rep["report_id"],))
    assert rid_row["created_by"] == admin["id"]
    with pytest.raises(PermissionError, match="report you generated"):    # the store's own message
        st.review(admin, "report", rep["report_id"], "approved", "approve")
    st.conn.close()
    with pytest.raises(PermissionError):
        S.sign_review(rev, REV_PW, "report", rep["report_id"], "approved", "approve release",
                      signature_role="study_director")                 # a reviewer cannot sign as study director
    S.sign_review(rev, REV_PW, "report", rep["report_id"], "approved", "scientific review of the report")
    S.sign_review(dr, DIR_PW, "report", rep["report_id"], "approved", "approve the report release",
                  signature_role="study_director")
    meta = S.report_meta(project, rep["report_id"])
    text = _pdf_text(meta["signed_pdf"])
    assert "Dora Director" in text and "Customer approver" in text and "approve the report release" in text
    assert "Rita Reviewer" in text and "Signed copy of report" in text and rep["sha256"] in text.replace("\n", "")
    assert "Analyst" in text
    assert "Dora Director" not in _pdf_text(rep["pdf"])                 # the signed original is never modified
    acts = [e["action"] for e in project.store.audit.events(limit=1000)]
    assert "review.signature_role" in acts and "report.signed_copy" in acts and "review.needs_changes" in acts
    rev.store.conn.close()
    dr.store.conn.close()


def test_ux07_08_reports_view_buttons(qtbot, window, team):
    project, sid, scan, rid, did = team
    S.generate_report(project, sid)
    w = _reopen(window, project)
    rv = w.reports
    assert set(rv.sign_btns) == {"approved", "needs_changes", "rejected"}
    assert rv.sign_btns["needs_changes"].text().startswith("Request changes")
    assert not rv.approve.isEnabled() and "generated this report" in rv.approve.toolTip()
    assert rv.sign_btns["rejected"].isEnabled()


# ----------------------------------------------------------------------------- UX-09 blinding
def test_ux09_blind_codes_random_stable_unique(project, study):
    codes = [project.blind_code("scan", i, study) for i in range(1, 31)]
    assert len(set(codes)) == 30 and all(c.startswith("S-") and len(c) == 6 for c in codes)
    assert codes != sorted(codes)                                       # not in database-ID order
    assert [project.blind_code("scan", i, study) for i in range(1, 31)] == codes   # stable


def test_ux09_blinded_mode_hides_identity_everywhere(qtbot, window, analysed):
    project, sid, scan = analysed
    spec = S.get_or_create_specimen(project, sid, "RAT-77")
    project.store.exec("UPDATE scans SET specimen_id=?, acquisition=? WHERE id=?",
                       (spec, json.dumps({"kV": 70, "operator": "RAT-77 bench"}), scan))
    w = _reopen(window, project)
    w.set_blinded(True)
    names = []

    def walk(it):
        names.append(it.text(0) + " " + (it.toolTip(0) or ""))
        for i in range(it.childCount()):
            walk(it.child(i))
    walk(w.tree.topLevelItem(0))
    joined = " ".join(names)
    assert "ph.nii" not in joined and "RAT-77" not in joined and "Scan S-" in joined and "Animal A-" in joined
    w.open_scan(scan)
    assert "ph.nii" not in w.workspace.infobar.text() and "S-" in w.workspace.infobar.text()
    assert "ph.nii" not in w.qc.banner.text()
    # audit trail: file names, animal IDs and acquisition metadata are masked in table and details
    w.audit.refresh()
    cells = [w.audit.table.item(r, c).text() for r in range(w.audit.table.rowCount())
             for c in range(w.audit.table.columnCount())]
    details = json.dumps([e for e in w.audit._events])
    for leak in ("ph.nii", "RAT-77"):
        assert leak not in " ".join(cells) and leak not in details
    # results
    w.results.refresh()
    row = w.results.model.rows[0]
    assert "ph.nii" not in row["scan"] and "RAT-77" not in row["animal"]
    # a report generated in blinded mode is blinded (PDF, CSV); an unblinded report's preview is hidden
    unbl = S.generate_report(w.project, sid)
    job = w.generate_report(sid)
    w.jobs.wait()
    qtbot.waitUntil(lambda: job.status == "done", timeout=60000)
    assert job.result["blinded"]
    text = _pdf_text(job.result["pdf"])
    assert "RAT-77" not in text and "ph.nii" not in text and "blinded" in text
    csv_text = open(job.result["csv"], encoding="utf-8").read()
    assert "RAT-77" not in csv_text
    assert "RAT-77" in _pdf_text(unbl["pdf"])
    w.reports.refresh(unbl["report_id"])
    assert w.reports.right.currentWidget() is w.reports.hidden_note
    w.reports.refresh(job.result["report_id"])
    assert w.reports.right.currentWidget() is w.reports.preview


# ----------------------------------------------------------------------------- UX-10 role gating
def test_ux10_actions_disabled_by_role_with_reason(qtbot, window, team):
    project, sid, scan, rid, did = team
    w = _reopen(window, project, "rev", REV_PW)
    for a in (w.a_import, w.a_analyze, w.a_roi, w.a_save_rev, w.tool_actions["brush"], w.tool_actions["grow"]):
        assert not a.isEnabled() and "Your role (Reviewer) cannot" in a.toolTip()
    assert not w.btn_analyse.isEnabled() and "cannot" in w.btn_analyse.toolTip()
    assert w.tool_actions["navigate"].isEnabled() and w.tool_actions["measure"].isEnabled()
    w.open_scan(scan)
    assert w.state.editor is not None and not w.state.can_edit
    w.state.set_tool("brush")
    assert w.state.tool == "navigate"
    assert not w.segpanel.badge.isHidden() and "READ ONLY" in w.segpanel.badge.text()
    assert not w.review.edit_roi.isEnabled() and "cannot" in w.review.edit_roi.toolTip()
    assert w.review.btns["approved"].isEnabled()                     # reviewers can sign
    assert not w.a_users.isEnabled()


def test_ux10_analyst_cannot_sign(qtbot, window, analysed):
    project, sid, scan = analysed
    project.add_user("ana", "Andy Analyst", "analyst", "Analyst-Pass-1")
    w = _reopen(window, project, "ana", "Analyst-Pass-1")
    w.open_scan(scan)
    assert w.state.can_edit
    for b in w.review.btns.values():
        assert not b.isEnabled() and "cannot sign" in b.toolTip()
    assert not w.review.accept_roi.isEnabled()
