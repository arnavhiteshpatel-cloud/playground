"""Import wizard logic: format detection, explicit spacing, assignment, nothing silently dropped."""
import numpy as np
import pytest

from osteoquant.desktop import services as S
from osteoquant.desktop.import_wizard import ImportModel, guess_animal_id


def test_probe_formats(tmp_path, phantom_file):
    pr = S.probe_source(phantom_file)
    assert pr.ok and pr.format == "nifti" and pr.shape == (40, 56, 56)
    assert pr.spacing_source == "file" and not pr.spacing_needs_entry
    np.save(tmp_path / "a.npy", np.zeros((4, 5, 6), np.float32))
    pn = S.probe_source(tmp_path / "a.npy")
    assert pn.format == "npy" and pn.shape == (4, 5, 6) and pn.spacing_needs_entry
    (tmp_path / "bad.nii.gz").write_bytes(b"xx")
    assert not S.probe_source(tmp_path / "bad.nii.gz").ok
    (tmp_path / "notes.txt").write_text("hello")
    assert not S.probe_source(tmp_path / "notes.txt").ok


def test_tiff_stack_folder_is_one_candidate(tmp_path):
    import tifffile
    d = tmp_path / "stack"
    d.mkdir()
    for i in range(5):
        tifffile.imwrite(d / f"rec_{i:04d}.tif", np.full((8, 9), i, np.uint16))
    assert S.find_candidates(d) == [d]
    pr = S.probe_source(d)
    assert pr.format == "tiff-stack" and pr.shape == (5, 8, 9)
    assert pr.spacing_needs_entry          # plain TIFF slices carry no reliable voxel size


def test_spacing_validation():
    assert S.validate_spacing([10, 10, 10]) == (10.0, 10.0, 10.0)
    for bad in ([0, 1, 1], [1, 1], [float("nan"), 1, 1], [1, 1, 99999], ["a", 1, 1]):
        with pytest.raises(ValueError):
            S.validate_spacing(bad)


def test_guess_animal_id(tmp_path):
    assert guess_animal_id(tmp_path / "R01 week4.nii.gz") == "R01_week4"


def test_model_requires_explicit_spacing(project, study, tmp_path, phantom_file):
    np.save(tmp_path / "raw.npy", np.random.default_rng(0).normal(500, 50, (20, 30, 30)).astype(np.float32))
    m = ImportModel(project, study)
    m.add_path(phantom_file)
    m.add_path(tmp_path / "raw.npy")
    probs = m.problems()
    assert len(probs) == 1 and "raw.npy" in probs[0] and "spacing" in probs[0]
    with pytest.raises(ValueError):
        m.run()
    m.candidates[1].spacing = [20, 20, 20]
    assert m.problems() and "confirm" in m.problems()[0]
    m.candidates[1].confirmed = True
    assert not m.problems()


def test_run_assigns_and_logs_rejections(project, study, tmp_path, phantom_file):
    (tmp_path / "broken.nii.gz").write_bytes(b"not nifti")
    np.save(tmp_path / "excluded.npy", np.zeros((4, 4, 4), np.float32))
    m = ImportModel(project, study)
    m.add_path(phantom_file)
    m.add_path(tmp_path / "broken.nii.gz")
    m.add_path(tmp_path / "excluded.npy")
    assert [c.readable for c in m.candidates] == [True, False, True]
    m.candidates[0].animal_id, m.candidates[0].timepoint, m.candidates[0].days = "R01", "Week 4", 28
    m.candidates[2].include = False
    out = m.run()
    assert out[0].status in ("imported", "flagged") and out[0].scan_id
    assert out[0].qc_deterministic and out[0].qc_heuristic
    assert all(c["basis"] == "deterministic" for c in out[0].qc_deterministic)
    assert out[1].status == "rejected" and "Unreadable" in out[1].reason
    assert out[2].status == "rejected" and "excluded by the user" in out[2].reason
    sc = project.store.scan(project.user, out[0].scan_id)
    spec = project.store.q1("SELECT animal_id FROM specimens WHERE id=?", (sc["specimen_id"],))
    tp = project.store.q1("SELECT label, days FROM timepoints WHERE id=?", (sc["timepoint_id"],))
    assert spec["animal_id"] == "R01" and tp == {"label": "Week 4", "days": 28.0}
    assert sc["meta"]["ingest"]["spacing_source"] == "file"
    # rejected sources stay visible: import log, project tree and audit trail
    log = project.import_log(study)
    assert {r["status"] for r in log} >= {"rejected"}
    tree = project.study_tree()
    rej = [c for c in tree[0]["children"] if c["kind"] == "rejected_folder"]
    assert rej and len(rej[0]["children"]) == 2
    acts = [e["action"] for e in project.store.audit.events()]
    assert acts.count("scan.import_rejected") == 2


def test_duplicate_is_rejected_with_reason(project, study, phantom_file):
    r1 = S.import_scan(project, S.ImportRequest(str(phantom_file), (40, 40, 40), True, study))
    r2 = S.import_scan(project, S.ImportRequest(str(phantom_file), (40, 40, 40), True, study))
    assert r1.scan_id and r2.status == "rejected" and "Duplicate" in r2.reason


def test_qc_failure_is_flagged_not_dropped(project, study, tmp_path):
    from osteoquant.io import write_nifti
    from osteoquant.volume import Volume
    data = np.zeros((20, 30, 30), np.uint16)
    data[5:15, 5:25, 5:25] = 65535          # saturated block -> deterministic QC failure
    data[:5] = 1000
    write_nifti(Volume(data, (20, 20, 20)), tmp_path / "sat.nii.gz")
    o = S.import_scan(project, S.ImportRequest(str(tmp_path / "sat.nii.gz"), (20, 20, 20), True, study))
    assert o.scan_id is not None
    assert o.status == "flagged" and o.qc["verdict"] in ("unsuitable", "review")
    assert "QC" in o.reason


def test_slab_import_matches_full_import(project, study, tmp_path, monkeypatch):
    """Large-volume path (slab by slab) gives the same content hash as a whole-volume read."""
    import tifffile
    from osteoquant.volume import Volume
    d = tmp_path / "stack"
    d.mkdir()
    rng = np.random.default_rng(3)
    vol = rng.integers(0, 4000, (23, 16, 17)).astype(np.uint16)
    for i in range(vol.shape[0]):
        tifffile.imwrite(d / f"s_{i:04d}.tif", vol[i])
    monkeypatch.setattr(S, "SLAB_IMPORT_BYTES", 1000)
    o = S.import_scan(project, S.ImportRequest(str(d), (12, 12, 12), True, study))
    assert o.scan_id, o.reason
    sc = project.store.scan(project.user, o.scan_id)
    assert sc["meta"]["ingest"].get("slab_import")
    assert sc["content_sha256"] == Volume(vol, (12, 12, 12)).content_hash()
    import zarr
    assert np.array_equal(np.asarray(zarr.open_group(sc["store_path"], mode="r")["image"][:]), vol)


def test_wizard_pages_offscreen(qtbot, project, study, phantom_file, tmp_path):
    from osteoquant.desktop.import_wizard import ImportWizard
    from osteoquant.desktop.jobs import JobManager
    np.save(tmp_path / "raw.npy", np.random.default_rng(0).normal(500, 50, (20, 30, 30)).astype(np.float32))
    jobs = JobManager()
    jobs.set_project(project)
    wiz = ImportWizard(project, jobs, study, initial_paths=[str(phantom_file), str(tmp_path / "raw.npy")])
    qtbot.addWidget(wiz)
    wiz.show()
    assert wiz.src.isComplete()
    wiz.next()
    assert not wiz.meta.isComplete()          # npy has no spacing
    wiz.meta.all_sp.setValue(25.0)
    wiz.meta._apply_all()
    assert wiz.meta.isComplete()
    wiz.next()
    assert wiz.assign.isComplete()
    wiz.next()
    with qtbot.waitSignal(jobs.job_finished, timeout=120000):
        wiz.runp.run()
    assert wiz.runp.isComplete()
    assert {c.outcome.status for c in wiz.model.candidates} <= {"imported", "flagged"}
    assert wiz.runp.results.rowCount() == 2
    jobs.wait()
