"""Label revisions, review sign-off, reports (watermark, preview), support status, timing, project."""
import numpy as np
import pytest

from osteoquant.desktop import services as S
from osteoquant.desktop.support import FLAGGED, NOT_SUPPORTED, SUPPORTED, measurement_support, reported_value
PW = "Correct-Horse-9"


def _labels(project, scan_id):
    from osteoquant.desktop.volume_source import ZarrSource
    sc = project.store.scan(project.user, scan_id)
    seg = project.store.segmentations(project.user, scan_id)[-1]
    return seg, ZarrSource(sc["store_path"]).load_labels(seg["labels_key"])


def test_project_create_open_login(tmp_path):
    from osteoquant.desktop.project import Project, ProjectError, is_project_folder
    with pytest.raises(ProjectError):
        Project.create(tmp_path / "p0", "x", "admin", "weak", "")
    p = Project.create(tmp_path / "p", "Lab", "admin", PW)
    assert is_project_folder(tmp_path / "p") and p.user["role"] == "admin"
    p.close()
    q = Project(tmp_path / "p")
    assert not q.login("admin", "wrong") and q.login("admin", PW)
    with pytest.raises(ProjectError):
        Project.create(tmp_path / "p", "again", "admin", PW)
    q.close()


def test_label_revision_audit(analysed):
    project, sid, scan = analysed
    seg, lab = _labels(project, scan)
    with pytest.raises(ValueError):
        S.save_label_revision(project, scan, seg["id"], lab, "")
    lab2 = lab.copy()
    lab2[10, 20:24, 20:24] = 2
    lab2[11, 20:22, 20:22] = 0
    res = S.save_label_revision(project, scan, seg["id"], lab2, "graft misclassified", {"brush2d": 2})
    assert res["version"] == seg["version"] + 1
    exp = {}
    for c, name in ((0, "background"), (1, "new_bone"), (2, "residual_graft"), (3, "host_bone")):
        d = int((lab2 == c).sum() - (lab == c).sum())
        if d:
            exp[name] = d
    assert res["voxel_count_change"] == exp
    ev = [e for e in project.store.audit.events() if e["action"] == "segmentation.edit"][0]
    assert ev["details"]["reason"] == "graft misclassified" and ev["details"]["voxel_count_change"] == exp
    assert ev["user_id"] == str(project.user["id"])
    new = project.store.segmentations(project.user, scan)[-1]
    assert new["kind"] == "corrected" and new["parent_id"] == seg["id"]
    m = project.store.latest_measurements(project.user, sid)[0]["metrics"]
    assert m["corrected_from"] == seg["version"] and "measurement_support" in m
    _, stored = _labels(project, scan)
    assert np.array_equal(stored, lab2)
    with pytest.raises(ValueError):
        S.save_label_revision(project, scan, seg["id"], np.full(lab.shape, 9, np.uint8), "bad labels")


def test_review_requires_reauth_and_separation_of_duties(analysed):
    project, sid, scan = analysed
    seg = project.store.segmentations(project.user, scan)[-1]
    with pytest.raises(PermissionError):
        S.sign_review(project, "wrong-password", "segmentation", seg["id"], "approved", "approve for reporting")
    with pytest.raises(PermissionError):      # the admin created this segmentation: cannot approve it
        S.sign_review(project, PW, "segmentation", seg["id"], "approved", "approve for reporting")
    rid = S.sign_review(project, PW, "segmentation", seg["id"], "needs_changes", "corrections required")
    assert rid
    acts = [e["action"] for e in project.store.audit.events()]
    assert "review.reauth_failed" in acts and "review.needs_changes" in acts
    # a second user with reviewer role can approve
    project.store.create_user(project.user["org_id"], "rev", "Reviewer-Pass-1", "reviewer", actor=project.user)
    from osteoquant.desktop.project import Project
    p2 = Project(project.folder)
    assert p2.login("rev", "Reviewer-Pass-1")
    assert S.sign_review(p2, "Reviewer-Pass-1", "segmentation", seg["id"], "approved", "approve for reporting")
    p2.store.conn.close()
    assert project.store.audit.verify_chain()["ok"]


def test_report_with_watermark_and_preview(qtbot, analysed, tmp_path):
    project, sid, scan = analysed
    res = S.generate_report(project, sid, watermark="EVALUATION COPY - NOT FOR STUDY DECISIONS")
    pdf = res["pdf"]
    assert open(pdf, "rb").read(4) == b"%PDF"
    import pypdfium2 as pdfium
    doc = pdfium.PdfDocument(pdf)
    text = doc[0].get_textpage().get_text_range()
    assert "EVALUATION COPY" in text
    assert len(doc) >= 2
    clean = S.generate_report(project, sid, watermark=None)
    assert "EVALUATION COPY" not in pdfium.PdfDocument(clean["pdf"])[0].get_textpage().get_text_range()
    from osteoquant.desktop.reports_view import PdfPreview
    pv = PdfPreview()
    qtbot.addWidget(pv)
    assert pv.load(pdf) == len(doc)
    pv.go(1)
    assert pv.current_page() == 1
    files = S.export_report(project, res["report_id"], tmp_path)
    assert len(files) == 2 and all(open(f, "rb").read(1) for f in files)
    acts = {e["action"] for e in project.store.audit.events()}
    assert {"report.generate", "report.export"} <= acts


def test_report_requires_analysis(project, study):
    with pytest.raises(ValueError):
        S.generate_report(project, study)


def test_measurement_support_statuses(analysed):
    project, sid, scan = analysed
    m = project.store.latest_measurements(project.user, sid)[0]["metrics"]
    sup = measurement_support(m)
    assert sup["overall"] in (SUPPORTED, FLAGGED, NOT_SUPPORTED)
    assert set(sup["endpoints"]) >= {"TV_mm3", "new_bone_fraction", "Tb_Th_um"}
    # advisor output is honoured: beta-TCP graft/new-bone split is not supported -> value suppressed
    adv = m["measurement_support"]["endpoints"]
    if adv["new_bone_volume"]["status"] == "not_supported":
        assert sup["endpoints"]["new_bone_volume_mm3"]["status"] == NOT_SUPPORTED
        v, why = reported_value(m, "class_volumes.new_bone_volume_mm3")
        assert v is None and why
    assert measurement_support({"status": "needs_manual_roi"})["overall"] == NOT_SUPPORTED
    ok = measurement_support({"metrics": {"class_volumes": {"uncertain_fraction": 0.0},
                                          "new_bone_architecture": {"Tb_Th_um": 100}}})
    assert ok["overall"] == SUPPORTED
    hi = measurement_support({"metrics": {"class_volumes": {"uncertain_fraction": 0.5},
                                          "new_bone_architecture": {"Tb_Th_um": 100}}})
    assert hi["overall"] == NOT_SUPPORTED


def test_results_rows(analysed, phantom_file, tmp_path):
    from osteoquant.desktop.results_view import NOT_ANALYSED, build_rows
    project, sid, scan = analysed
    np.save(tmp_path / "b.npy", np.random.default_rng(1).normal(400, 30, (20, 20, 20)).astype(np.float32))
    o = S.import_scan(project, S.ImportRequest(str(tmp_path / "b.npy"), (40, 40, 40), True, sid))
    rows = build_rows(project, sid)
    by = {r["scan_id"]: r for r in rows}
    assert by[o.scan_id]["status"] == NOT_ANALYSED
    r = by[scan]
    assert r["values"]["TV_mm3"]["value"] and r["values"]["TV_mm3"]["value"] > 0
    blind = build_rows(project, sid, blinded_view=True)
    assert all(b["group"] == "(blinded)" and "nii" not in b["scan"] for b in blind)


def test_manual_roi_then_analysis(analysed):
    project, sid, scan = analysed
    sc = project.store.scan(project.user, scan)
    c = [n // 2 for n in sc["shape"]]
    rid = S.save_cylinder_roi(project, scan, c, 500, (-600, 600), reason="manual ROI test")
    assert project.store.latest_roi(project.user, scan)["id"] == rid
    r = S.analyze_scan(project, scan, {"nominal_diameter_um": 1000}, use_saved_roi=True)
    assert r["status"] == "complete_unreviewed"


def test_workflow_timing(project, study, tmp_path):
    import csv
    from osteoquant.desktop.timing import TimingRecorder
    clock = [0.0]
    rec = TimingRecorder(project, clock=lambda: clock[0])
    assert not rec.enabled
    rec.scan_opened(5, study)
    rec.edit("brush2d", {1: 10})
    assert rec.events() == []                     # off by default: nothing recorded
    rec.set_enabled(True)
    rec.scan_opened(5, study)
    for t in (1, 2, 3, 100, 101):                 # the 97 s gap is idle and excluded
        clock[0] = t
        rec.input_activity()
    rec.edit("brush2d", {1: 10, 0: -10})
    rec.edit("region_grow", {2: 5, 0: -5})
    rec.signoff("segmentation", 1, "approved")
    rec.scan_closed()
    s = rec.summary(study)[0]
    assert s["edits"] == 2 and s["first_edit_utc"] and s["signoffs"] == 1
    assert s["active_seconds"] == pytest.approx(4.0)      # 0->1->2->3 (3 s) + 100->101 (1 s); 97 s idle gap excluded
    assert s["voxels_changed"] == {"1": 10, "0": -15, "2": 5}
    a, b = rec.export_csv(tmp_path / "t.csv", study)
    rows = list(csv.DictReader(open(a)))
    assert rows[0]["edits"] == "2" and rows[0]["voxels_changed_new_bone"] == "10"
    assert len(list(csv.DictReader(open(b)))) >= 6
