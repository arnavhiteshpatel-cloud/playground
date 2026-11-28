"""Library-level tests that close traceability gaps (scripts/build_traceability.py); the desktop-level ones are in
tests/desktop/test_traceability_gaps.py. They assert existing behaviour named in docs/quality/FUNCTIONAL_SPEC.md."""
import csv
import re

import numpy as np
import pytest
from scipy import ndimage as ndi

PW = "Correct-Horse-9"


# ============================================================================ FS-171-1 characterisation reuse
def _char_scene(seed=3):
    rng = np.random.default_rng(seed)
    img = rng.normal(100, 10, (40, 40, 40)).astype(np.float32)
    zz, yy, xx = np.indices(img.shape)
    host = xx < 8
    img[host] += 900
    mat = np.zeros(img.shape, bool)
    for c in ((20, 15, 20), (20, 28, 28), (10, 22, 30)):
        mat |= ((zz - c[0]) ** 2 + (yy - c[1]) ** 2 + (xx - c[2]) ** 2) <= 25
    img[mat] = 100 + 2.0 * 900 + rng.normal(0, 10, mat.sum())
    soft = ~host & ~ndi.binary_dilation(mat, iterations=2)
    return img, mat, soft, ndi.binary_erosion(host)


def test_characterisation_incompatible_filter_refused():
    """FS-171-1: compatible_with refuses reuse when the voxel size differs by > 25 % or kVp, filter or scanner
    model differ (the filter case was not asserted before)."""
    from osteoquant.advisor.characterize import characterise_material
    img, mat, soft, host = _char_scene()
    acq = {"kvp": 70, "filter": "Al 0.5 mm", "scanner_model": "S1"}
    ch = characterise_material(img, mat, soft, host, 40.0, "new_ceramic", bone_derived=False, acquisition=dict(acq))
    assert ch.compatible_with(40.0, dict(acq)) == (True, "compatible")
    ok, why = ch.compatible_with(40.0, {**acq, "filter": "Cu 0.1 mm"})
    assert not ok and why == "acquisition 'filter' differs (Cu 0.1 mm vs Al 0.5 mm)"
    assert not ch.compatible_with(40.0, {"filter": "none"})[0]                 # filter alone is enough
    for key, other in (("kvp", 90), ("scanner_model", "S2")):
        ok, why = ch.compatible_with(40.0, {**acq, key: other})
        assert not ok and f"'{key}' differs" in why
    # voxel size: within 25 % accepted on both sides, beyond refused on both sides
    assert ch.compatible_with(50.0, acq)[0] and ch.compatible_with(30.0, acq)[0]
    for vx in (50.5, 29.5):
        ok, why = ch.compatible_with(vx, acq)
        assert not ok and "by >25%" in why


# ============================================================================ FS-001-2 RUO statement (renderer)
def _bundle(data_class, review_status):
    eps = [("class_volumes.TV_mm3", "Defect TV", "mm³")]
    specs = [{"specimen_id": f"A{i}", "animal_id": f"A{i}", "group": "Ctrl", "timepoint": "Week 4",
              "metrics": {"class_volumes": {"TV_mm3": 1.0 + i / 10}}} for i in range(3)]
    return {"title": "RUO test", "study": {"name": "RUO test"}, "data_class": data_class,
            "review_status": review_status, "specimens": specs, "endpoints": eps}


@pytest.mark.parametrize("review_status", ["unreviewed_automated", "reviewed"])
@pytest.mark.parametrize("data_class", ["synthetic", "public", "research", "customer"])
def test_every_pdf_and_csv_carry_ruo_data_class_and_review_status(tmp_path, data_class, review_status):
    """FS-001-2: every page of every PDF carries the RUO / not-validated footer and the first page the full statement,
    whatever the data class and review status; the CSV header and every row carry the data class and review status."""
    import pypdfium2 as pdfium
    from osteoquant.report.defectfill import RUO_FOOTER, build_pdf
    r = build_pdf(_bundle(data_class, review_status), tmp_path / "r.pdf", tmp_path / "r.csv")
    doc = pdfium.PdfDocument(r["pdf"])
    pages = [re.sub(r"\s+", " ", doc[i].get_textpage().get_text_range()) for i in range(len(doc))]
    assert len(pages) >= 2
    assert ("Research use only. Not a medical device. Not validated for GLP studies (21 CFR 58 / OECD GLP). "
            "No claim of 21 CFR Part 11 compliance.") in pages[0]
    assert all(RUO_FOOTER in p and f"{data_class.upper()} DATA · {review_status}" in p for p in pages)
    lines = (tmp_path / "r.csv").read_text().splitlines()
    assert f"data class: {data_class} · {review_status} · {RUO_FOOTER}" in lines[0]
    rows = list(csv.DictReader(x for x in lines if not x.startswith("#")))
    assert len(rows) == 3 and all((x["data_class"], x["review_status"]) == (data_class, review_status) for x in rows)


# ============================================================================ FS-091-1 meaning rule (API)
def test_api_refuses_signature_meaning_shorter_than_5(tmp_path):
    """FS-091-1: the web API applies the same >= 5-character meaning rule as the desktop (refused before
    re-authentication; nothing is recorded as a review)."""
    from fastapi.testclient import TestClient
    from osteoquant.api.app import create_app
    app = create_app(str(tmp_path / "a.db"), str(tmp_path / "d"))
    st = app.state.store
    o = st.create_org("L")
    st.create_user(o, "rev", PW, "reviewer")
    c = TestClient(app)
    hdr = {"Authorization": "Bearer " + c.post("/api/auth/login", json={"username": "rev", "password": PW}).json()["token"]}
    body = {"object_type": "segmentation", "object_id": 1, "decision": "approved", "password": PW}
    for meaning in ("", "abcd"):
        assert c.post("/api/reviews", json={**body, "meaning": meaning}, headers=hdr).status_code == 422
    assert st.q("SELECT id FROM reviews") == []
    acts = [e["action"] for e in st.audit.events(limit=1000)]
    assert not [a for a in acts if a.startswith("review.") or a == "auth.reauth_failed"]
    st.close()
