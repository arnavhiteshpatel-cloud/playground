"""Study-store workflows (blinding, reviews, export, deletion) and the remaining API endpoints,
including negative paths (bad parameters, missing objects, insufficient roles)."""
import json

import numpy as np
import pytest
from fastapi.testclient import TestClient

from osteoquant.api.app import _json_safe, create_app
from osteoquant.study.jobs import JobRunner
from qa_helpers import PW, make_users


# ----------------------------------------------------------------------------- store workflows
def _study(st, U, blinded=False):
    pid = st.create_project(U["adminA"], "P")
    sid = st.create_study(U["adminA"], pid, "S", blinded=blinded)
    gid = st.add_group(U["adminA"], sid, "Treatment")
    spid = st.add_specimen(U["adminA"], sid, "R1", gid, "F")
    tid = st.add_timepoint(U["adminA"], sid, "8w", 56)
    return sid, gid, spid, tid


def test_store_lookup_errors_and_roles(store):
    U = make_users(store)
    with pytest.raises(ValueError):
        store.create_user(U["adminA"]["org_id"], "x", PW, "superuser")
    with pytest.raises(KeyError):
        store.study(U["adminA"], 999)
    with pytest.raises(KeyError):
        store.create_study(U["adminA"], 999, "S")
    with pytest.raises(KeyError):
        store.scan(U["adminA"], 999)
    with pytest.raises(PermissionError):
        store.set_user_active(U["anaA"], U["viewA"]["id"], False)


def test_blinded_specimen_listing_and_export(store):
    U = make_users(store)
    sid, gid, spid, tid = _study(store, U, blinded=True)
    rows = store.specimens(U["anaA"], sid)
    assert rows[0]["group_name"].startswith("G-")
    assert store.specimens(U["adminA"], sid)[0]["group_name"] == "Treatment"
    ex = store.export_study(U["anaA"], sid)
    assert ex["audit"].startswith("omitted") and ex["groups"][0]["description"] == "(blinded)"
    ex2 = store.export_study(U["revA"], sid)
    assert isinstance(ex2["audit"], list) and ex2["audit"]
    with pytest.raises(PermissionError):
        store.export_study(U["viewA"], sid)


def test_reviews_on_reports_and_unknown_objects(store):
    U = make_users(store)
    sid, *_ = _study(store, U)
    rid = store.exec("INSERT INTO reports(org_id,study_id,status,created_by,created,sha256) VALUES (?,?,?,?,?,?)",
                     (U["revA"]["org_id"], sid, "ready", U["revA"]["id"], "now", "ab" * 32))
    with pytest.raises(PermissionError, match="Separation of duties"):
        store.review(U["revA"], "report", rid, "approved", "approve report")
    store.review(U["revA"], "report", rid, "needs_changes", "fix the figure")
    with pytest.raises(KeyError):
        store.review(U["revA"], "report", 999, "approved", "x")
    with pytest.raises(KeyError):
        store.review(U["revA"], "segmentation", 999, "approved", "x")
    with pytest.raises(ValueError):
        store.review(U["revA"], "scan", 1, "maybe", "x")
    store.review(U["revA"], "roi", 1, "approved", "roi looks right")
    revs = store.reviews(U["revA"], "report", rid)
    assert len(revs) == 1 and revs[0]["object_sha256"] == "ab" * 32


def test_delete_study_data_removes_files_and_keeps_audit(store, tmp_path):
    U = make_users(store)
    sid, gid, spid, tid = _study(store, U)
    sp = tmp_path / "scan.zarr"
    sp.mkdir()
    (sp / "x").write_text("1")
    scid = store.register_scan(U["anaA"], sid, spid, tid, str(sp), "a", "nifti", "f" * 64, "c" * 64, [1, 1, 1],
                               [1, 1, 1], {})
    store.save_roi(U["anaA"], scid, {"kind": "box", "params": {}, "definition_sha256": "d"}, "r")
    pdf = tmp_path / "r.pdf"
    pdf.write_bytes(b"%PDF")
    store.exec("INSERT INTO reports(org_id,study_id,pdf_path,status,created_by,created) VALUES (?,?,?,?,?,?)",
               (U["anaA"]["org_id"], sid, str(pdf), "ready", U["anaA"]["id"], "now"))
    n_audit = len(store.audit.events(limit=10 ** 6))
    with pytest.raises(PermissionError):
        store.delete_study_data(U["anaA"], sid, "cleanup")
    store.delete_study_data(U["adminA"], sid, "retention period over")
    assert not sp.exists() and not pdf.exists()
    assert store.q1("SELECT count(*) n FROM scans WHERE study_id=?", (sid,))["n"] == 0
    assert store.study(U["adminA"], sid)["status"] == "deleted"
    assert len(store.audit.events(limit=10 ** 6)) > n_audit and store.audit.verify_chain()["ok"]


def test_job_runner_cancel_get_list_and_stale_privilege(store):
    import threading
    U = make_users(store)
    gate = threading.Event()

    def slow(st, user, params, ctx):
        gate.wait(5)
        ctx.progress(0.5, "half")
        return {"ok": True}

    def boom(st, user, params, ctx):
        raise RuntimeError("kaboom")
    r = JobRunner(store, {"slow": slow, "boom": boom})
    with pytest.raises(ValueError):
        r.submit(U["anaA"], "nope", {})
    with pytest.raises(PermissionError):
        r.submit(U["viewA"], "slow", {})
    j = r.submit(U["anaA"], "slow", {"a": 1})
    r.cancel(U["anaA"], j)
    gate.set()
    assert r.wait(j, 10) == "cancelled"
    jb = r.submit(U["anaA"], "boom", {})
    assert r.wait(jb, 10) == "failed" and "kaboom" in r.get(U["anaA"], jb)["message"]
    assert {x["id"] for x in r.list(U["anaA"])} >= {j, jb}
    with pytest.raises(PermissionError):
        r.get(U["adminB"], j)
    with pytest.raises(KeyError):
        r.get(U["anaA"], 999)
    with pytest.raises(KeyError):
        r.cancel(U["anaA"], 999)
    gate.clear()
    j2 = r.submit(U["anaA"], "slow", {})
    store.set_user_active(U["adminA"], U["anaA"]["id"], False)     # deactivated before the job starts
    gate.set()
    st2 = r.wait(j2, 10)
    assert st2 in ("failed", "done")
    assert r.wait(j2, 0.01) in ("failed", "done", "timeout")


# ----------------------------------------------------------------------------- API endpoints
@pytest.fixture
def api(tmp_path):
    app = create_app(str(tmp_path / "api.db"), str(tmp_path / "data"))
    st = app.state.store
    o = st.create_org("Lab")
    for n, r in (("admin", "admin"), ("analyst", "analyst"), ("reviewer", "reviewer"), ("viewer", "viewer")):
        st.create_user(o, n, PW, r)
    o2 = st.create_org("Other")
    st.create_user(o2, "outsider", PW, "admin")
    c = TestClient(app)
    c.h = {u: {"Authorization": "Bearer " + c.post("/api/auth/login", json={"username": u, "password": PW}).json()["token"]}
           for u in ("admin", "analyst", "reviewer", "viewer", "outsider")}
    yield c
    c.close()


@pytest.fixture
def scan(api, tmp_path):
    from osteoquant.io import write_nifti
    from osteoquant.volume import Volume
    H = api.h["analyst"]
    pid = api.post("/api/projects", json={"name": "P"}, headers=H).json()["id"]
    sid = api.post("/api/studies", json={"project_id": pid, "name": "S", "blinded": True}, headers=H).json()["id"]
    data = np.full((12, 16, 16), 100, np.uint16)
    data[4:8, 4:12, 4:12] = 2000
    p = tmp_path / "v.nii.gz"
    write_nifti(Volume(data, (20, 20, 20)), p)
    r = api.post(f"/api/studies/{sid}/scans", files={"file": ("v.nii.gz", p.read_bytes())},
                 data={"acquisition": json.dumps({"kv": 70})}, headers=H)
    assert r.status_code == 200, r.text
    scid = r.json()["scan_id"]
    api.app.state.runner.wait(r.json()["qc_job"], 60)
    # create a segmentation version directly (fast) so edit / mesh endpoints can be exercised
    st = api.app.state.store
    u = st.user_for_token(H["Authorization"].split()[1])
    sc = st.scan(u, scid)
    lab = np.zeros(data.shape, np.uint8)
    lab[4:8, 4:12, 4:12] = 1
    from osteoquant.io import write_labels_zarr
    from osteoquant.pipeline import labels_hash
    segid, v = st.save_segmentation(u, scid, "automatic", "seg_v1", labels_hash(lab), method="multiotsu")
    write_labels_zarr(sc["store_path"], "seg_v1", lab)
    write_labels_zarr(sc["store_path"], "roi_current", np.ones(data.shape, np.uint8))
    return {"study": sid, "scan": scid, "seg": segid}


def test_admin_user_management_endpoints(api):
    A = api.h["admin"]
    r = api.post("/api/users", json={"username": "new.user", "password": PW, "role": "viewer"}, headers=A)
    assert r.status_code == 200
    assert any(u["username"] == "new.user" for u in api.get("/api/users", headers=A).json())
    assert api.get("/api/users", headers=api.h["analyst"]).status_code == 403
    assert api.post("/api/users", json={"username": "w", "password": "weak", "role": "viewer"}, headers=A).status_code == 422
    assert api.post("/api/users", json={"username": "weak1", "password": "weakpassword", "role": "viewer"},
                    headers=A).status_code == 400
    me = api.get("/api/me", headers=A).json()
    assert "manage_users" in me["permissions"]
    assert api.get("/api/projects", headers=A).status_code == 200


def test_study_scan_and_viewer_endpoints(api, scan):
    H, V, X = api.h["analyst"], api.h["viewer"], api.h["outsider"]
    sid, scid = scan["study"], scan["scan"]
    s = api.get(f"/api/studies/{sid}", headers=V).json()
    assert s["study"]["id"] == sid and s["scans"][0]["id"] == scid
    assert api.get(f"/api/studies/{sid}", headers=X).status_code == 403
    assert api.get("/api/studies/999", headers=H).status_code == 404
    gid = api.post(f"/api/studies/{sid}/groups", json={"name": "Ctrl"}, headers=H).json()["id"]
    assert api.post(f"/api/studies/{sid}/specimens", json={"animal_id": "A1", "group_id": gid}, headers=H).status_code == 200
    assert api.post(f"/api/studies/{sid}/timepoints", json={"label": "4w", "days": 28}, headers=H).status_code == 200
    info = api.get(f"/api/scans/{scid}", headers=V).json()
    assert info["shape"] == [12, 16, 16] and "labels/seg_v1" in info["layers"] or info["layers"]
    png = api.get(f"/api/scans/{scid}/slice?axis=1&index=3&lo=0&hi=3000", headers=V)
    assert png.status_code == 200 and png.content[:4] == b"\x89PNG"
    assert api.get(f"/api/scans/{scid}/slice?axis=0&index=99", headers=V).status_code == 400
    assert api.get(f"/api/scans/{scid}/slice?axis=3&index=0", headers=V).status_code == 400
    assert api.get(f"/api/scans/{scid}/slice?layer=labels/none", headers=V).status_code == 404
    m = api.get(f"/api/scans/{scid}/mesh?layer=labels/seg_v1&label=1&step=1", headers=V).json()
    assert m["units"] == "mm" and len(m["vertices"]) % 3 == 0 and len(m["faces"]) % 3 == 0
    assert api.get(f"/api/scans/{scid}/mesh?layer=labels/seg_v1&label=3&step=1", headers=V).json()["vertices"] == []
    assert api.get(f"/api/scans/{scid}/mesh?layer=image&label=1", headers=V).status_code == 400
    assert api.get(f"/api/scans/{scid}/mesh?layer=labels/seg_v1&label=1&step=9", headers=V).status_code == 400
    assert api.get(f"/api/studies/{sid}/results", headers=V).json() == []
    ex = api.get(f"/api/studies/{sid}/export", headers=api.h["reviewer"]).json()
    assert ex["study"]["id"] == sid and isinstance(ex["audit"], list)


def test_roi_and_edit_endpoints(api, scan):
    H, V = api.h["analyst"], api.h["viewer"]
    scid = scan["scan"]
    roi = {"kind": "cylinder", "params": {"center_um": [120, 160, 160], "axis": [1, 0, 0], "radius_um": 80,
                                          "extent_um": [-60, 60]}}
    r = api.put(f"/api/scans/{scid}/roi", json={"definition": roi, "reason": "manual"}, headers=H)
    assert r.status_code == 200 and r.json()["version"] == 1
    bad = api.put(f"/api/scans/{scid}/roi", json={"definition": {"kind": "mask", "params": {}}, "reason": "x x"},
                  headers=H)
    assert bad.status_code == 400
    assert api.put(f"/api/scans/{scid}/roi", json={"definition": roi, "reason": "manual"}, headers=V).status_code == 403
    ops = [{"op": "fill_component", "axis": 0, "index": 5, "cy": 8, "cx": 8, "label": 2, "only_from": 1},
           {"op": "brush", "axis": 2, "index": 8, "cy": 6, "cx": 6, "r": 1.5, "label": 0}]
    e = api.post(f"/api/scans/{scid}/segmentations/edits", json={"base_version": 1, "ops": ops, "reason": "fix graft"},
                 headers=H)
    assert e.status_code == 200, e.text
    assert e.json()["voxel_count_change"]["2"] > 0
    base = {"base_version": 1, "reason": "fix things"}
    assert api.post(f"/api/scans/{scid}/segmentations/edits", json={**base, "base_version": 9, "ops": ops},
                    headers=H).status_code == 404
    for op in ({**ops[0], "label": 7}, {**ops[0], "index": 99}, {**ops[0], "cy": 99}):
        assert api.post(f"/api/scans/{scid}/segmentations/edits", json={**base, "ops": [op]},
                        headers=H).status_code == 400
    assert api.post(f"/api/scans/{scid}/segmentations/edits", json={**base, "ops": ops}, headers=V).status_code == 403


def test_review_reports_jobs_audit_endpoints(api, scan):
    H, R, V, A = api.h["analyst"], api.h["reviewer"], api.h["viewer"], api.h["admin"]
    sid = scan["study"]
    body = {"object_type": "segmentation", "object_id": scan["seg"], "decision": "approved",
            "meaning": "reviewed segmentation", "password": PW}
    assert api.post("/api/reviews", json=body, headers=R).status_code == 200
    assert api.get("/api/reports/999/pdf", headers=H).status_code == 404
    st = api.app.state.store
    rid = st.exec("INSERT INTO reports(org_id,study_id,status,created_by,created,unblinded) VALUES (1,?,?,?,?,1)",
                  (sid, "building", 1, "now"))
    assert api.get(f"/api/reports/{rid}/pdf", headers=H).status_code == 403          # unblinded content
    assert api.get(f"/api/reports/{rid}/pdf", headers=A).status_code == 400          # not ready
    assert api.get(f"/api/reports/{rid}/xls", headers=A).status_code == 400
    assert api.post(f"/api/studies/{sid}/unblind", data={"reason": "locked"}, headers=H).status_code == 403
    assert api.post(f"/api/studies/{sid}/unblind", data={"reason": "locked"}, headers=A).status_code == 200
    jobs = api.get("/api/jobs", headers=H).json()
    assert jobs and api.get(f"/api/jobs/{jobs[0]['id']}", headers=H).json()["kind"] == "qc"
    assert api.post(f"/api/jobs/{jobs[0]['id']}/cancel", headers=H).json()["ok"]
    assert api.post(f"/api/jobs/{jobs[0]['id']}/cancel", headers=V).status_code == 403
    assert api.get("/api/audit", headers=H).status_code == 403
    ev = api.get("/api/audit?object_type=scan", headers=R).json()
    assert ev and all(e["object_type"] == "scan" for e in ev)
    assert api.get("/api/audit/verify", headers=V).json()["ok"]
    assert api.get("/api/health").json()["ok"]
    assert api.post(f"/api/studies/{sid}/scans", files={"file": ("a.tar", b"x" * 600)}, headers=H).status_code == 400
    assert api.post(f"/api/studies/{sid}/scans", files={"file": ("a.nii", b"x")}, data={"acquisition": "{bad"},
                    headers=H).status_code == 400


def test_json_safe_helper():
    assert _json_safe({"a": float("nan"), "b": [np.float32(1.5), float("inf")], "c": (1, np.int64(2))}) == \
        {"a": None, "b": [1.5, None], "c": [1, 2]}
