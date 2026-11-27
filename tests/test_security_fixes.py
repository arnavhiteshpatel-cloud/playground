"""Regression tests for the independent review findings (docs/security/SECURITY_REVIEW.md)."""
import io
import tarfile
import threading
import time

import numpy as np
import pytest

from osteoquant.io import read_volume
from osteoquant.io.readers import UnsafeInput
from osteoquant.io.safe_archive import safe_extract, UnsafeArchive
from osteoquant.study.db import Store

PW = "Correct-Horse-9"


def _users(st):
    o1, o2 = st.create_org("A"), st.create_org("B")
    for org, n, r in [(o1, "adm", "admin"), (o1, "ana", "analyst"), (o1, "rev", "reviewer"), (o2, "adm2", "admin")]:
        st.create_user(org, n, PW, r)
    return {n: st.user_for_token(st.login(n, PW)) for n in ("adm", "ana", "rev", "adm2")}


def test_S01_detached_nrrd_rejected(tmp_path):
    secret = tmp_path / "secret.bin"
    secret.write_bytes(b"\x01" * 64)
    hdr = tmp_path / "evil.nrrd"
    hdr.write_text(f"NRRD0004\ntype: uint8\ndimension: 3\nsizes: 4 4 4\nencoding: raw\ndata file: {secret}\n\n")
    with pytest.raises(UnsafeInput):
        read_volume(hdr, safe=True)
    mhd = tmp_path / "x.mhd"
    mhd.write_text("ObjectType = Image\nNDims = 3\nDimSize = 4 4 4\nElementType = MET_UCHAR\nElementDataFile = /etc/hosts\n")
    with pytest.raises(UnsafeInput):
        read_volume(mhd, safe=True)


def test_S02_model_paths_and_pickles_rejected():
    from osteoquant.ml.train import load_model
    from osteoquant.pipeline import segment
    from osteoquant.volume import Volume
    with pytest.raises(ValueError):
        load_model("../../tmp/evil")
    v = Volume(np.zeros((8, 8, 8), np.float32), (1, 1, 1))
    with pytest.raises(PermissionError):
        segment(v, np.ones(v.shape, bool), {"segmentation": "rf:/tmp/evil.pkl"})
    from pydantic import ValidationError
    from osteoquant.api.app import AnalyzeConfig
    with pytest.raises(ValidationError):
        AnalyzeConfig(segmentation="rf:/tmp/evil.pkl")
    with pytest.raises(ValidationError):
        AnalyzeConfig(_trusted_local=True)


def test_S03_tar_rejected_for_uploads(tmp_path):
    p = tmp_path / "a.tar"
    with tarfile.open(p, "w") as t:
        data = b"x" * 10
        ti = tarfile.TarInfo("a.txt"); ti.size = len(data)
        t.addfile(ti, io.BytesIO(data))
    with pytest.raises(UnsafeArchive):
        safe_extract(p, tmp_path / "out")


def test_S04_report_markup_escaped(tmp_path):
    from osteoquant.report import build_pdf
    bundle = {"title": '<img src="/etc/passwd" width="10" height="10"/> & <b>x</b>', "study": {"name": "<font>"},
              "data_class": "synthetic", "review_status": "unreviewed_automated",
              "specimens": [{"specimen_id": "<img src='/etc/hosts'/>", "group": "<b>g</b>", "timepoint": "t",
                             "metrics": {"class_volumes": {"TV_mm3": 1.0}}}],
              "endpoints": [("class_volumes.TV_mm3", "TV", "mm3")], "methods_text": "", "limitations": [], "reproducibility": {}}
    r = build_pdf(bundle, tmp_path / "r.pdf")
    assert (tmp_path / "r.pdf").read_bytes()[:4] == b"%PDF"


def test_S05_cross_study_group_reference_rejected(tmp_path):
    st = Store(tmp_path / "s.db", tmp_path / "d")
    U = _users(st)
    p2 = st.create_project(U["adm2"], "P2"); s2 = st.create_study(U["adm2"], p2, "S2")
    g_other = st.add_group(U["adm2"], s2, "Secret treatment")
    p1 = st.create_project(U["ana"], "P1"); s1 = st.create_study(U["ana"], p1, "S1")
    with pytest.raises(PermissionError):
        st.add_specimen(U["ana"], s1, "R1", g_other)


def test_S08_review_requires_existing_object(tmp_path):
    st = Store(tmp_path / "s.db", tmp_path / "d")
    U = _users(st)
    with pytest.raises(KeyError):
        st.review(U["rev"], "segmentation", 999, "approved", "approve future object")


def test_S09_lockout_is_temporary(tmp_path):
    st = Store(tmp_path / "s.db", tmp_path / "d")
    o = st.create_org("X"); st.create_user(o, "u", PW, "analyst")
    for _ in range(5):
        st.login("u", "bad")
    assert st.login("u", PW) is None
    st.exec("UPDATE users SET locked_until=? WHERE username='u'", (time.time() - 1,))
    assert st.login("u", PW) is not None


def test_S10_concurrent_audit_writes_keep_chain(tmp_path):
    st = Store(tmp_path / "s.db", tmp_path / "d")

    def w(i):
        for j in range(25):
            st.audit.record("concurrent", details={"t": i, "j": j})
    th = [threading.Thread(target=w, args=(i,)) for i in range(6)]
    [t.start() for t in th]; [t.join() for t in th]
    v = st.audit.verify_chain()
    assert v["ok"] and v["n"] >= 150


def test_S11_anchor_detects_truncation(tmp_path):
    st = Store(tmp_path / "s.db", tmp_path / "d")
    for i in range(5):
        st.audit.record("x", details={"i": i})
    anchor = st.audit.anchor()
    st.conn.execute("DROP TRIGGER audit_no_delete")
    st.conn.execute("DELETE FROM audit_log WHERE seq=?", (anchor["seq"],))
    assert st.audit.verify_chain()["ok"]            # tail truncation invisible without anchor...
    assert not st.audit.verify_chain(anchor)["ok"]  # ...detected with an external anchor
