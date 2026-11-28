"""Gen-2 security review regression tests (docs/security/SECURITY_REVIEW_GEN2.md) and destructive
tests of the study store (corrupt / truncated database, read-only locations, interrupted writes)."""
import io
import json
import os
import sqlite3
import time
import zipfile

import numpy as np
import pytest
from fastapi.testclient import TestClient

from qa_helpers import PW, make_users
from osteoquant.api.app import create_app
from osteoquant.study.db import Store, check_password, hash_password


# ----------------------------------------------------------------------------- store: auth hygiene
def test_reauthentication_counts_towards_lockout(store):
    U = make_users(store)
    rev = U["revA"]
    for _ in range(5):
        assert not store.reauthenticate(rev, "wrong-password")
    assert not store.reauthenticate(rev, PW)            # locked, even with the right password
    assert store.login("revA", PW) is None
    store.exec("UPDATE users SET locked_until=0 WHERE id=?", (rev["id"],))
    assert store.reauthenticate(rev, PW)
    acts = [e["action"] for e in store.audit.events(limit=50)]
    assert "auth.reauth_failed" in acts


def test_reauthentication_inactive_user(store):
    U = make_users(store)
    store.set_user_active(U["adminA"], U["anaA"]["id"], False)
    assert not store.reauthenticate(U["anaA"], PW)


def test_deactivation_deletes_sessions_and_login_purges_expired(store):
    o = store.create_org("X")
    store.create_user(o, "a1", PW, "admin")
    store.create_user(o, "u1", PW, "analyst")
    admin = store.user_for_token(store.login("a1", PW))
    tok = store.login("u1", PW, ttl_s=3600)
    uid = store.user_for_token(tok)["id"]
    store.set_user_active(admin, uid, False)
    assert store.q1("SELECT count(*) n FROM sessions WHERE user_id=?", (uid,))["n"] == 0
    store.set_user_active(admin, uid, True)
    store.login("u1", PW, ttl_s=-10)                    # already expired
    store.login("u1", PW)                               # purges expired sessions
    assert store.q1("SELECT count(*) n FROM sessions WHERE expires < ?", (time.time(),))["n"] == 0
    store.logout(tok)


def test_malformed_password_hash_never_raises():
    assert not check_password("x", "scrypt$zz$00")
    assert not check_password("x", "garbage")
    assert not check_password("x", None)
    assert check_password("Pw-123456789", hash_password("Pw-123456789"))


def test_writes_require_write_permission(store):
    U = make_users(store)
    pid = store.create_project(U["anaA"], "P")
    sid = store.create_study(U["anaA"], pid, "S")
    scid = store.register_scan(U["anaA"], sid, None, None, "", "x", "nifti", "f" * 64, "c" * 64, [1, 1, 1],
                               [1, 1, 1], {})
    with pytest.raises(PermissionError):
        store.set_scan_qc(U["viewA"], scid, {"verdict": "pass"})
    with pytest.raises(PermissionError):
        store.save_measurement(U["revA"], scid, None, None, {"m": 1}, "0")
    store.set_scan_qc(U["anaA"], scid, {"verdict": "pass"})
    assert store.scan(U["viewA"], scid)["status"] == "qc_pass"


# ----------------------------------------------------------------------------- store: destructive
def test_corrupted_database_file_fails_clearly(tmp_path):
    p = tmp_path / "bad.db"
    p.write_bytes(b"this is not an sqlite database" * 100)
    with pytest.raises(sqlite3.DatabaseError):
        Store(p, tmp_path / "d")


def test_truncated_database_fails_or_detects(tmp_path):
    p = tmp_path / "t.db"
    st = Store(p, tmp_path / "d")
    make_users(st)
    st.conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    st.close()
    raw = p.read_bytes()
    p.write_bytes(raw[: len(raw) // 3])
    for f in (tmp_path / "t.db-wal", tmp_path / "t.db-shm"):
        if f.exists():
            f.unlink()
    with pytest.raises(sqlite3.DatabaseError):
        st2 = Store(p, tmp_path / "d")
        st2.audit.verify_chain()
        st2.q("SELECT * FROM users")


def test_reopen_is_idempotent_and_chain_survives(tmp_path):
    st = Store(tmp_path / "a.db", tmp_path / "d")
    make_users(st)
    head = st.audit.anchor()
    st.close()
    st2 = Store(tmp_path / "a.db", tmp_path / "d")
    from osteoquant.study.db import SCHEMA_VERSION
    assert st2.q1("SELECT max(v) v FROM schema_version")["v"] == SCHEMA_VERSION == 3   # v3: must_change_password
    assert st2.audit.verify_chain(head)["ok"]
    st2.close()


@pytest.mark.skipif((hasattr(os, "geteuid") and os.geteuid() == 0) or os.name == "nt",
                    reason="root ignores POSIX permissions; Windows has no POSIX directory modes")
def test_read_only_data_directory(tmp_path):
    ro = tmp_path / "ro"
    ro.mkdir()
    ro.chmod(0o500)
    try:
        with pytest.raises((PermissionError, sqlite3.OperationalError)):
            Store(ro / "x.db", ro / "data")
    finally:
        ro.chmod(0o700)


def test_read_only_database_file_rejects_writes(tmp_path):
    p = tmp_path / "a.db"
    st = Store(p, tmp_path / "d")
    make_users(st)
    st.close()
    ro = sqlite3.connect(f"{p.as_uri()}?mode=ro", uri=True, isolation_level=None)
    from osteoquant.audit.log import AuditLog
    with pytest.raises(sqlite3.OperationalError):
        AuditLog(ro).record("x")


def test_interrupted_backup_target(store, tmp_path):
    make_users(store)
    r = store.backup(tmp_path / "b.db")
    b = Store(tmp_path / "b.db", tmp_path / "bd")
    assert b.audit.verify_chain()["ok"] and len(r["sha256"]) == 64
    with pytest.raises((sqlite3.OperationalError, OSError)):
        store.backup(tmp_path / "missing_dir" / "b.db")


# ----------------------------------------------------------------------------- API
@pytest.fixture
def client(tmp_path):
    app = create_app(str(tmp_path / "api.db"), str(tmp_path / "data"))
    st = app.state.store
    o = st.create_org("Lab")
    for n, r in (("admin", "admin"), ("analyst", "analyst"), ("reviewer", "reviewer"), ("viewer", "viewer")):
        st.create_user(o, n, PW, r)
    c = TestClient(app)

    def auth(u):
        t = c.post("/api/auth/login", json={"username": u, "password": PW}).json()["token"]
        return {"Authorization": f"Bearer {t}"}
    c.login_as = auth
    yield c
    c.close()


def _study(client, H):
    pid = client.post("/api/projects", json={"name": "P"}, headers=H).json()["id"]
    return client.post("/api/studies", json={"project_id": pid, "name": "S"}, headers=H).json()["id"]


def test_security_headers_present(client):
    r = client.get("/api/health")
    assert r.headers["x-content-type-options"] == "nosniff"
    assert r.headers["x-frame-options"] == "DENY"
    assert "frame-ancestors 'none'" in r.headers["content-security-policy"]
    assert client.get("/api/me").headers["x-content-type-options"] == "nosniff"   # also on 401


def test_review_endpoint_cannot_bruteforce_password(client):
    R = client.login_as("reviewer")
    body = {"object_type": "scan", "object_id": 1, "decision": "approved", "meaning": "reviewed for test",
            "password": "wrong"}
    for _ in range(5):
        assert client.post("/api/reviews", json=body, headers=R).status_code == 401
    r = client.post("/api/reviews", json={**body, "password": PW}, headers=R)
    assert r.status_code == 401                          # locked: correct password refused too
    assert client.post("/api/auth/login", json={"username": "reviewer", "password": PW}).status_code == 401


def _upload(client, H, sid, name, data):
    return client.post(f"/api/studies/{sid}/scans", files={"file": (name, data)}, headers=H)


def test_dot_filenames_do_not_500(client):
    A = client.login_as("analyst")
    sid = _study(client, A)
    for name in ("..", ".", "...."):
        r = _upload(client, A, sid, name, b"junk")
        assert r.status_code == 400, (name, r.status_code, r.text)


def _zip_bytes(files):
    b = io.BytesIO()
    with zipfile.ZipFile(b, "w") as z:
        for n, d in files.items():
            z.writestr(n, d)
    return b.getvalue()


def test_zip_with_pickle_zarr_rejected_by_api(client, tmp_path):
    A = client.login_as("analyst")
    sid = _study(client, A)
    files = {
        "s.zarr/.zgroup": json.dumps({"zarr_format": 2}),
        "s.zarr/image/.zarray": json.dumps({"zarr_format": 2, "shape": [2, 2, 2], "chunks": [2, 2, 2], "dtype": "<u1",
                                            "fill_value": 0, "order": "C", "compressor": {"id": "pickle"},
                                            "filters": None}),
        "s.zarr/image/0.0.0": b"\x80\x04N.",            # pickle of None (inert)
    }
    r = _upload(client, A, sid, "s.zip", _zip_bytes(files))
    assert r.status_code == 400 and "pickle" in r.text


def test_corrupt_zip_and_malformed_volumes_are_400(client, tmp_path):
    A = client.login_as("analyst")
    sid = _study(client, A)
    good = _zip_bytes({"a.tif": b"x" * 5000})
    bad = bytearray(good)
    bad[40] ^= 0xFF
    assert _upload(client, A, sid, "c.zip", bytes(bad)).status_code == 400
    hdr = b"NRRD0004\ntype: uint16\ndimension: 3\nsizes: 30000 30000 30000\nencoding: raw\nendian: little\n\n"
    r = _upload(client, A, sid, "huge.nrrd", hdr + b"\0" * 64)
    assert r.status_code == 400 and ("read limit" in r.text or "Could not read" in r.text)
    assert _upload(client, A, sid, "t.nii.gz", b"\x1f\x8b\x08\x00garbage").status_code == 400
    assert _upload(client, A, sid, "empty.zip", _zip_bytes({})).status_code == 400
    assert not any((client.app.state.store.data_dir / "uploads").iterdir())   # temp files cleaned


def test_viewer_cannot_upload_or_analyze(client):
    V, A = client.login_as("viewer"), client.login_as("analyst")
    sid = _study(client, A)
    assert _upload(client, V, sid, "a.nii", b"x").status_code == 403
    assert client.post("/api/scans/1/analyze", json={}, headers=V).status_code in (403, 404)


def test_bearer_token_parsing(client):
    assert client.get("/api/me", headers={"Authorization": "Bearer"}).status_code == 401
    assert client.get("/api/me", headers={"Authorization": "Basic abc"}).status_code == 401
    assert client.get("/api/me", headers={"Authorization": "Bearer " + "A" * 43}).status_code == 401
    A = client.login_as("analyst")
    assert client.post("/api/auth/logout", headers=A).json()["ok"]
    assert client.get("/api/me", headers=A).status_code == 401


def test_scan_info_survives_nan_qc_values(client, tmp_path):
    """QA-019: a small scan gives an undefined (NaN) QC cupping index; GET /api/scans/{id} returned 400."""
    from osteoquant.io import write_nifti
    from osteoquant.volume import Volume
    A = client.login_as("analyst")
    sid = _study(client, A)
    p = tmp_path / "v.nii.gz"
    write_nifti(Volume(np.random.default_rng(0).integers(0, 1000, (8, 12, 12)).astype(np.uint16), (20, 20, 20)), p)
    r = _upload(client, A, sid, "v.nii.gz", p.read_bytes())
    assert r.status_code == 200, r.text
    client.app.state.runner.wait(r.json()["qc_job"], 60)
    sc = client.get(f"/api/scans/{r.json()['scan_id']}", headers=A).json()
    assert sc["shape"] == [8, 12, 12] and sc["spacing_um"] == pytest.approx([20, 20, 20])


def test_newer_schema_database_is_refused(tmp_path):
    """C3-PRD-21: an older application refuses a database written by a newer one."""
    from osteoquant.study.db import MIGRATIONS, Store
    st = Store(tmp_path / "x.db", tmp_path / "data")
    st.conn.execute("INSERT INTO schema_version VALUES (?)", (max(MIGRATIONS) + 1,))
    st.conn.commit()
    st.close()
    with pytest.raises(RuntimeError, match="newer OsteoQuant"):
        Store(tmp_path / "x.db", tmp_path / "data")
