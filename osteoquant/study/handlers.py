"""Job handlers shared by the desktop application and the optional web API.

Kept free of any web-framework import so the desktop bundle does not need FastAPI/Starlette/Pydantic
(cycle-2 finding: the desktop shipped the web stack only because these handlers lived in ``api/app.py``).
"""
from __future__ import annotations

from pathlib import Path

import numpy as np

from .. import __version__
from .db import Store


def _store_path(store: Store, org_id, scan_id) -> Path:
    p = store.data_dir / f"org{int(org_id)}" / "scans" / f"scan{int(scan_id)}.zarr"
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def _load_scan(store, user, scan_id):
    from ..io import read_volume
    sc = store.scan(user, scan_id)
    vol, _ = read_volume(sc["store_path"])
    stored = dict((sc["meta"] or {}).get("ingest", {}))   # original ingest record: missing slices, errors, assumptions
    stored.setdefault("metadata_found", {})["spacing_um"] = sc["spacing_um"]
    vol.meta["ingest"] = stored
    return sc, vol


def job_qc(store, user, params, ctx):
    from ..qc import run_qc
    sc, vol = _load_scan(store, user, params["scan_id"])
    ctx.progress(0.3, "running QC")
    qc = run_qc(vol)
    store.set_scan_qc(user, params["scan_id"], qc)
    return {"verdict": qc["verdict"], "n_warn": qc["n_warn"], "n_fail": qc["n_fail"]}


def job_analyze(store, user, params, ctx):
    from ..pipeline import analyze, public
    from ..io import write_labels_zarr
    scan_id = params["scan_id"]
    sc, vol = _load_scan(store, user, scan_id)
    roi_dict = params.get("roi")
    if roi_dict is None and params.get("use_saved_roi", True):
        r = store.latest_roi(user, scan_id)
        if r:
            roi_dict = r["definition"]
    res = analyze(vol, params.get("config", {}), roi_dict, progress=lambda f, m: ctx.progress(f, m))
    if res.get("status") == "needs_manual_roi":
        return {"status": "needs_manual_roi", "error": res.get("roi_error")}
    import uuid
    seg = res["segmentation"]
    # data first, rows last (C2-PRD-10 pattern, cycle-3 review C3-PRD-16): the labels go under a new unique key; the
    # ROI, segmentation and measurement rows and the scan status are committed in ONE transaction; on failure the
    # array is removed, so a half-written analysis never becomes the current version
    key = f"seg_a{uuid.uuid4().hex[:12]}"
    write_labels_zarr(sc["store_path"], key, res["_labels"])
    try:
        with store.transaction():
            if roi_dict is None:
                rid, _ = store.save_roi(user, scan_id, res["roi"], reason="automatic detection")
            else:
                lr = store.latest_roi(user, scan_id)
                rid = lr["id"] if lr else None
            sid, v = store.save_segmentation(user, scan_id, "automatic", key, res["labels_sha256"],
                                             method=seg["method"], model_name=seg.get("model_name"),
                                             model_sha256=seg.get("model_sha256"), roi_id=rid)
            store.exec("UPDATE segmentations SET labels_key=? WHERE id=?", (key, sid))
            store.save_measurement(user, scan_id, sid, rid, public(res), __version__)
            store.exec("UPDATE scans SET status='analyzed' WHERE id=?", (scan_id,))
    except BaseException:
        _remove_arrays(sc["store_path"], [key])
        raise
    # derived masks named by version, written after commit (an error here leaves the committed analysis intact)
    warnings = []
    try:
        write_labels_zarr(sc["store_path"], "roi_current", res["_roi_mask"].astype(np.uint8))
        write_labels_zarr(sc["store_path"], f"roi_v{v}", res["_roi_mask"].astype(np.uint8))
        if "_entropy" in res:
            write_labels_zarr(sc["store_path"], f"unc_v{v}", np.clip(res["_entropy"] * 255, 0, 255).astype(np.uint8))
    except OSError as e:
        warnings.append(f"ROI/uncertainty layers not written: {e}")
    return {"segmentation_id": sid, "version": v, "status": res["status"], "timings": res["timings"],
            "warnings": warnings}


def _remove_arrays(store_path, names):
    try:
        import zarr
        g = zarr.open_group(str(store_path), mode="a")
        for n in names:
            if f"labels/{n}" in g:
                del g[f"labels/{n}"]
    except Exception:  # noqa: BLE001 - best effort; the rows were rolled back
        pass


def job_report(store, user, params, ctx):
    from ..api.bundle import bundle_from_store
    from ..report import build_pdf
    sid = params["study_id"]
    bundle = bundle_from_store(store, user, sid, ctx)
    out = store.data_dir / f"org{user['org_id']}" / "reports"
    out.mkdir(parents=True, exist_ok=True)
    st_row = store.study(user, sid)
    unblinded = int(bool(st_row["blinded"]) and store.can(user, "unblind"))
    rid = store.exec("INSERT INTO reports(org_id,study_id,status,created_by,created,unblinded) VALUES (?,?,?,?,datetime('now'),?)",
                     (user["org_id"], sid, "building", user["id"], unblinded))
    pdf, csvp = out / f"report{rid}.pdf", out / f"report{rid}.csv"
    r = build_pdf(bundle, pdf, csvp)
    store.exec("UPDATE reports SET pdf_path=?, csv_path=?, sha256=?, status='ready' WHERE id=?",
               (str(pdf), str(csvp), r["pdf_sha256"], rid))
    store.audit.record("report.generate", user["id"], user["org_id"], "report", rid, {"study": sid, "sha256": r["pdf_sha256"]})
    return {"report_id": rid, "sha256": r["pdf_sha256"]}


HANDLERS = {"qc": job_qc, "analyze": job_analyze, "report": job_report}
