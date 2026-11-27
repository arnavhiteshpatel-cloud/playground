"""Integration / end-to-end tests of the study store, audit trail, security controls and API."""
import io
import sqlite3
import time
import zipfile

import pytest
from fastapi.testclient import TestClient

from osteoquant.study.db import Store
from osteoquant.study.jobs import JobRunner
from osteoquant.io.safe_archive import safe_extract, UnsafeArchive
from osteoquant.api.app import create_app

PW = "Correct-Horse-9"


@pytest.fixture
def store(tmp_path):
    return Store(tmp_path / "t.db", tmp_path / "data")


def _users(store):
    o1 = store.create_org("LabA")
    o2 = store.create_org("LabB")
    ids = {}
    for org, name, role in [(o1, "adminA", "admin"), (o1, "anaA", "analyst"), (o1, "revA", "reviewer"),
                            (o1, "viewA", "viewer"), (o2, "adminB", "admin")]:
        ids[name] = store.create_user(org, name, PW, role)
    return {n: store.user_for_token(store.login(n, PW)) for n in ids}


# ------------------------------------------------------------------ store-level security
def test_password_policy_and_lockout(store):
    o = store.create_org("X")
    with pytest.raises(ValueError):
        store.create_user(o, "weak", "short", "analyst")
    store.create_user(o, "u1", PW, "analyst")
    for _ in range(5):
        assert store.login("u1", "wrong") is None
    assert store.login("u1", PW) is None  # locked after 5 failures


def test_rbac_and_tenant_isolation(store):
    U = _users(store)
    pid = store.create_project(U["anaA"], "P")
    sid = store.create_study(U["anaA"], pid, "S")
    with pytest.raises(PermissionError):
        store.create_project(U["viewA"], "nope")           # viewer cannot write
    with pytest.raises(PermissionError):
        store.study(U["adminB"], sid)                      # other tenant cannot read
    with pytest.raises(PermissionError):
        store.review(U["anaA"], "segmentation", 1, "approved", "approve")   # analyst cannot sign
    assert store.list_studies(U["adminB"]) == []
    with pytest.raises(PermissionError):
        store.create_user(U["adminA"]["org_id"], "x1", PW, "admin", actor=U["anaA"])


def test_blinding(store):
    U = _users(store)
    pid = store.create_project(U["adminA"], "P")
    sid = store.create_study(U["adminA"], pid, "S", blinded=True)
    store.add_group(U["adminA"], sid, "Treatment-X")
    assert store.groups(U["anaA"], sid)[0]["name"].startswith("G-")
    assert store.groups(U["adminA"], sid)[0]["name"] == "Treatment-X"
    with pytest.raises(PermissionError):
        store.unblind(U["anaA"], sid, "curious")
    store.unblind(U["adminA"], sid, "analysis locked")
    assert store.groups(U["anaA"], sid)[0]["name"] == "Treatment-X"


def test_audit_chain_detects_tampering(tmp_path):
    st = Store(tmp_path / "a.db", tmp_path / "d")
    _users(st)
    assert st.audit.verify_chain()["ok"]
    with pytest.raises(sqlite3.IntegrityError):
        st.conn.execute("UPDATE audit_log SET action='x' WHERE seq=2")
    with pytest.raises(sqlite3.IntegrityError):
        st.conn.execute("DELETE FROM audit_log WHERE seq=2")
    anchor = st.audit.anchor()
    # simulate an attacker bypassing triggers by editing the file directly
    st.conn.execute("DROP TRIGGER audit_no_update")
    st.conn.execute("UPDATE audit_log SET details='{\"forged\":1}' WHERE seq=3")
    r = st.audit.verify_chain()
    assert not r["ok"] and r["first_bad_seq"] == 3
    assert st.audit.verify_anchor(anchor)


def test_backup_restores(store, tmp_path):
    U = _users(store)
    store.create_project(U["adminA"], "P")
    b = store.backup(tmp_path / "bk.db")
    assert len(b["sha256"]) == 64
    s2 = Store(tmp_path / "bk.db", tmp_path / "d2")
    assert s2.q1("SELECT count(*) n FROM projects")["n"] == 1
    assert s2.audit.verify_chain()["ok"]


# ------------------------------------------------------------------ archives
def _zip(entries):
    b = io.BytesIO()
    with zipfile.ZipFile(b, "w") as z:
        for name, data in entries:
            z.writestr(name, data)
    return b.getvalue()


@pytest.mark.parametrize("name", ["../evil.txt", "/abs/evil.txt", "a/../../evil.txt", "C:/evil.txt"])
def test_zip_traversal_rejected(tmp_path, name):
    p = tmp_path / "x.zip"
    p.write_bytes(_zip([(name, b"x")]))
    with pytest.raises(UnsafeArchive):
        safe_extract(p, tmp_path / "out")
    assert not (tmp_path / "evil.txt").exists()


def test_zip_bomb_rejected(tmp_path):
    p = tmp_path / "bomb.zip"
    b = io.BytesIO()
    with zipfile.ZipFile(b, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("big.bin", b"\0" * 50_000_000)
    p.write_bytes(b.getvalue())
    with pytest.raises(UnsafeArchive):
        safe_extract(p, tmp_path / "out")


# ------------------------------------------------------------------ jobs
def test_job_cancel_and_recovery(store):
    U = _users(store)

    def slow(st, user, params, ctx):
        for i in range(100):
            time.sleep(0.02)
            ctx.progress(i / 100)
        return {"ok": True}

    r = JobRunner(store, {"slow": slow, "boom": lambda *a: 1 / 0})
    j = r.submit(U["anaA"], "slow", {})
    time.sleep(0.1)
    r.cancel(U["anaA"], j)
    assert r.wait(j, 10) == "cancelled"
    j2 = r.submit(U["anaA"], "boom", {})
    assert r.wait(j2, 10) == "failed"
    assert "ZeroDivision" in r.get(U["anaA"], j2)["message"]
    with pytest.raises(PermissionError):
        r.get(U["adminB"], j2)
    # crash recovery: a job left 'running' is marked failed on restart
    store.exec("INSERT INTO jobs(org_id,user_id,kind,params,status,created) VALUES (?,?,?,?,?,datetime('now'))",
               (U["anaA"]["org_id"], U["anaA"]["id"], "slow", "{}", "running"))
    JobRunner(store, {"slow": slow})
    assert store.q1("SELECT status FROM jobs ORDER BY id DESC LIMIT 1")["status"] == "failed"


# ------------------------------------------------------------------ end-to-end API
@pytest.fixture
def client(tmp_path):
    app = create_app(str(tmp_path / "api.db"), str(tmp_path / "data"))
    st = app.state.store
    o = st.create_org("Demo Lab")
    st.create_user(o, "admin", PW, "admin")
    st.create_user(o, "analyst", PW, "analyst")
    st.create_user(o, "reviewer", PW, "reviewer")
    o2 = st.create_org("Other Lab")
    st.create_user(o2, "outsider", PW, "admin")
    c = TestClient(app)

    def auth(u):
        t = c.post("/api/auth/login", json={"username": u, "password": PW}).json()["token"]
        return {"Authorization": f"Bearer {t}"}
    c.login_as = auth
    return c


def _phantom_nifti(tmp_path):
    from osteoquant.phantom import PhantomConfig, generate_phantom, render_fast, ImagingConfig
    from osteoquant.io import write_nifti
    ph = generate_phantom(PhantomConfig(model="condyle", shape=(40, 56, 56), voxel_um=40, supersample=1,
                                        defect_diameter_um=1400, seed=3))
    v = render_fast(ph.mu, 40, ImagingConfig(psf_sigma_um=20, noise_sigma=40))
    p = tmp_path / "ph.nii.gz"
    write_nifti(v, p)
    return p


def test_end_to_end(client, tmp_path):
    A, R, X = client.login_as("analyst"), client.login_as("reviewer"), client.login_as("outsider")
    assert client.get("/api/me").status_code == 401
    pid = client.post("/api/projects", json={"name": "Demo"}, headers=A).json()["id"]
    sid = client.post("/api/studies", json={"project_id": pid, "name": "Phantom study", "defect_model": "condyle"},
                      headers=A).json()["id"]
    gid = client.post(f"/api/studies/{sid}/groups", json={"name": "beta-TCP"}, headers=A).json()["id"]
    spid = client.post(f"/api/studies/{sid}/specimens", json={"animal_id": "R01", "group_id": gid}, headers=A).json()["id"]
    bad = client.post(f"/api/studies/{sid}/specimens", json={"animal_id": "R01; DROP TABLE"}, headers=A)
    assert bad.status_code == 422
    p = _phantom_nifti(tmp_path)
    up = client.post(f"/api/studies/{sid}/scans", files={"file": ("ph.nii.gz", p.read_bytes())},
                     data={"specimen_id": str(spid)}, headers=A)
    assert up.status_code == 200, up.text
    scan = up.json()["scan_id"]
    dup = client.post(f"/api/studies/{sid}/scans", files={"file": ("again.nii.gz", p.read_bytes())}, headers=A)
    assert dup.status_code == 400 and "Duplicate" in dup.text
    assert client.get(f"/api/scans/{scan}", headers=X).status_code == 403   # tenant isolation via API
    app_runner = client.app.state.runner
    app_runner.wait(up.json()["qc_job"], 60)
    j = client.post(f"/api/scans/{scan}/analyze", json={"config": {"defect_model": "condyle", "nominal_diameter_um": 1400}},
                    headers=A).json()["job_id"]
    assert app_runner.wait(j, 120) == "done", client.get(f"/api/jobs/{j}", headers=A).json()
    info = client.get(f"/api/scans/{scan}", headers=A).json()
    assert info["segmentations"] and info["roi"]
    img = client.get(f"/api/scans/{scan}/slice?axis=0&index=10&layer=labels/seg_v1", headers=A)
    assert img.status_code == 200 and img.headers["content-type"] == "image/png"
    assert client.get(f"/api/scans/{scan}/slice?axis=0&index=10&layer=../../etc", headers=A).status_code == 400
    ed = client.post(f"/api/scans/{scan}/segmentations/edits", headers=A, json={
        "base_version": 1, "reason": "test correction",
        "ops": [{"op": "brush", "axis": 0, "index": 20, "cy": 28, "cx": 28, "r": 4, "label": 2}]})
    assert ed.status_code == 200, ed.text
    assert ed.json()["version"] == 2
    segs = client.get(f"/api/scans/{scan}", headers=A).json()["segmentations"]
    assert segs[-1]["kind"] == "corrected" and segs[-1]["parent_id"] == segs[0]["id"]
    # analyst cannot sign; reviewer must re-authenticate
    body = {"object_type": "segmentation", "object_id": segs[-1]["id"], "decision": "approved",
            "meaning": "reviewed and approved for reporting", "password": PW}
    assert client.post("/api/reviews", json=body, headers=A).status_code == 403
    assert client.post("/api/reviews", json={**body, "password": "wrong"}, headers=R).status_code == 401
    assert client.post("/api/reviews", json=body, headers=R).status_code == 200
    m = client.get(f"/api/scans/{scan}/mesh?layer=labels/seg_v2&label=2&step=2", headers=A).json()
    assert len(m["vertices"]) > 0
    rj = client.post(f"/api/studies/{sid}/report", headers=A).json()["job_id"]
    assert app_runner.wait(rj, 180) == "done", client.get(f"/api/jobs/{rj}", headers=A).json()
    rid = client.get(f"/api/jobs/{rj}", headers=A).json()["result"]["report_id"]
    pdf = client.get(f"/api/reports/{rid}/pdf", headers=A)
    assert pdf.status_code == 200 and pdf.content[:4] == b"%PDF"
    assert client.get(f"/api/reports/{rid}/pdf", headers=X).status_code == 403
    assert client.get("/api/audit/verify", headers=A).json()["ok"]
    acts = {e["action"] for e in client.get("/api/audit", headers=R).json()}
    assert {"scan.import", "segmentation.save", "review.approved", "report.generate"} <= acts
