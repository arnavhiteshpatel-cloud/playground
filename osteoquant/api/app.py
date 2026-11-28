"""OsteoQuant web API + static viewer (FastAPI).

Run locally:  ``osteoquant serve`` (or ``python -m osteoquant.cli serve``) → http://127.0.0.1:8765
Local deployment only by default (binds to 127.0.0.1). No data leaves the machine.

Auth: ``Authorization: Bearer <token>`` (token from POST /api/auth/login). All object access is
checked against the caller's organisation (tenant isolation) and role permissions.
"""
from __future__ import annotations

import io
import json
import os
import re
import shutil
import uuid
from pathlib import Path

import numpy as np
from fastapi import Depends, FastAPI, File, Form, Header, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .. import __version__
from ..study.db import Store
from ..study.jobs import JobRunner

WEB = Path(__file__).resolve().parents[2] / "web" / "static"
MAX_UPLOAD = int(os.environ.get("OQ_MAX_UPLOAD_BYTES", str(8 * 1024 ** 3)))


def _json_safe(o):
    """Replace non-finite floats (NaN/inf, e.g. an undefined QC cupping index) by null: strict JSON
    cannot carry them and Starlette refuses to serialise them (QA-019)."""
    if isinstance(o, float):
        return o if np.isfinite(o) else None
    if isinstance(o, dict):
        return {k: _json_safe(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_json_safe(v) for v in o]
    if isinstance(o, np.generic):
        return _json_safe(o.item())
    return o


class SafeJSONResponse(JSONResponse):
    def render(self, content) -> bytes:
        return super().render(_json_safe(content))


# ----------------------------------------------------------------------------- job handlers (shared module)
from ..study.handlers import (HANDLERS, _load_scan, _store_path, job_analyze, job_qc,  # noqa: E402,F401
                              job_report)





# ----------------------------------------------------------------------------- app factory
class LoginIn(BaseModel):
    username: str = Field(min_length=1, max_length=64)
    password: str = Field(min_length=1, max_length=256)


class NameIn(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)


class StudyIn(BaseModel):
    project_id: int
    name: str = Field(min_length=1, max_length=200)
    species: str = ""
    defect_model: str = ""
    graft_materials: str = ""
    blinded: bool = False


class SpecimenIn(BaseModel):
    animal_id: str = Field(min_length=1, max_length=64, pattern=r"^[A-Za-z0-9_.\-]+$")
    group_id: int | None = None
    sex: str | None = None


class TimepointIn(BaseModel):
    label: str = Field(min_length=1, max_length=64)
    days: float | None = None


class UserIn(BaseModel):
    username: str = Field(min_length=3, max_length=64, pattern=r"^[A-Za-z0-9_.\-@]+$")
    password: str
    role: str
    full_name: str = ""


class EditOp(BaseModel):
    op: str = Field(pattern=r"^(brush|fill_component)$")
    axis: int = Field(ge=0, le=2)
    index: int = Field(ge=0)
    cy: float
    cx: float
    r: float = Field(default=2.0, ge=0.5, le=64)
    label: int = Field(ge=0, le=255)
    only_from: int | None = None


class EditsIn(BaseModel):
    base_version: int
    ops: list[EditOp] = Field(min_length=1, max_length=5000)
    reason: str = Field(min_length=3, max_length=500)   # required: recorded in audit trail


class ReviewIn(BaseModel):
    object_type: str = Field(pattern=r"^(segmentation|report|roi|scan)$")
    object_id: int
    decision: str = Field(pattern=r"^(approved|rejected|needs_changes)$")
    meaning: str = Field(min_length=5, max_length=300)
    comment: str = Field(default="", max_length=2000)
    password: str  # re-authentication at signing


class ROIIn(BaseModel):
    definition: dict
    reason: str = Field(min_length=3, max_length=500)


class AnalyzeConfig(BaseModel):
    model_config = {"extra": "forbid"}
    defect_model: str = Field(default="condyle", pattern=r"^(condyle|calvarial|segmental)$")
    nominal_diameter_um: float | None = Field(default=None, gt=0, lt=1e5)
    # default and validated method: the advisor's own threshold (the only method carrying measurement support)
    segmentation: str = Field(default="advisor_threshold",
                              pattern=r"^(advisor_threshold|multiotsu|ctan_style|unet:[A-Za-z0-9_\-]{1,64}|onnx:[A-Za-z0-9_\-]{1,64})$")
    graft_brighter: bool = True
    abstain_tau: float = Field(default=0.6, ge=0, le=1)
    tta: bool = True
    thickness_metrics: bool = True
    no_graft: bool = False
    t_mineral: float | None = None
    t_graft: float | None = None
    expected_model_sha256: str | None = Field(default=None, pattern=r"^[0-9a-f]{64}$")


class AnalyzeIn(BaseModel):
    config: AnalyzeConfig = AnalyzeConfig()
    use_saved_roi: bool = True


def create_app(db_path: str | None = None, data_dir: str | None = None, workers: int = 1) -> FastAPI:
    db_path = db_path or os.environ.get("OQ_DB", str(Path.cwd() / "runtime" / "osteoquant.db"))
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    store = Store(db_path, data_dir)
    runner = JobRunner(store, HANDLERS, workers=workers)
    app = FastAPI(title="OsteoQuant (research prototype)", version=__version__, default_response_class=SafeJSONResponse)
    app.state.store, app.state.runner = store, runner

    def current_user(authorization: str | None = Header(default=None)):
        tok = authorization.split(" ", 1)[1] if authorization and authorization.lower().startswith("bearer ") else None
        u = store.user_for_token(tok)
        if not u:
            raise HTTPException(401, "Not authenticated")
        return u

    @app.middleware("http")
    async def security_headers(request, call_next):   # S-20: baseline browser hardening headers
        resp = await call_next(request)
        resp.headers.setdefault("X-Content-Type-Options", "nosniff")
        resp.headers.setdefault("X-Frame-Options", "DENY")
        resp.headers.setdefault("Referrer-Policy", "no-referrer")
        resp.headers.setdefault("Content-Security-Policy",
                                "default-src 'self'; img-src 'self' blob: data:; style-src 'self' 'unsafe-inline'; "
                                "object-src 'none'; base-uri 'self'; frame-ancestors 'none'")
        return resp

    @app.exception_handler(PermissionError)
    async def perm(_, exc):
        return JSONResponse({"detail": str(exc)}, status_code=403)

    @app.exception_handler(KeyError)
    async def nf(_, exc):
        return JSONResponse({"detail": str(exc)}, status_code=404)

    @app.exception_handler(ValueError)
    async def bad(_, exc):
        return JSONResponse({"detail": str(exc)}, status_code=400)

    # ---------------------------------------------------------------- auth
    @app.post("/api/auth/login")
    def login(b: LoginIn):
        tok = store.login(b.username, b.password)
        if not tok:
            raise HTTPException(401, "Invalid credentials or locked account")
        return {"token": tok}

    @app.post("/api/auth/logout")
    def logout(authorization: str | None = Header(default=None), u=Depends(current_user)):
        store.logout(authorization.split(" ", 1)[1])
        store.audit.record("auth.logout", u["id"], u["org_id"])
        return {"ok": True}

    @app.get("/api/me")
    def me(u=Depends(current_user)):
        from ..study.db import ROLES
        return {**u, "permissions": sorted(ROLES[u["role"]]), "version": __version__}

    @app.post("/api/users")
    def new_user(b: UserIn, u=Depends(current_user)):
        uid = store.create_user(u["org_id"], b.username, b.password, b.role, b.full_name, actor=u)
        return {"id": uid}

    @app.get("/api/users")
    def users(u=Depends(current_user)):
        store.require(u, "manage_users")
        return store.q("SELECT id,username,full_name,role,active,created FROM users WHERE org_id=?", (u["org_id"],))

    # ---------------------------------------------------------------- projects / studies
    @app.post("/api/projects")
    def new_project(b: NameIn, u=Depends(current_user)):
        return {"id": store.create_project(u, b.name, b.description)}

    @app.get("/api/projects")
    def projects(u=Depends(current_user)):
        store.require(u, "read")
        return store.q("SELECT * FROM projects WHERE org_id=?", (u["org_id"],))

    @app.post("/api/studies")
    def new_study(b: StudyIn, u=Depends(current_user)):
        return {"id": store.create_study(u, b.project_id, b.name, b.species, b.defect_model, b.graft_materials, b.blinded)}

    @app.get("/api/studies")
    def studies(u=Depends(current_user)):
        return store.list_studies(u)

    @app.get("/api/studies/{sid}")
    def study(sid: int, u=Depends(current_user)):
        return {"study": store.study(u, sid), "groups": store.groups(u, sid), "specimens": store.specimens(u, sid),
                "timepoints": store.q("SELECT * FROM timepoints WHERE study_id=?", (sid,)), "scans": store.scans(u, sid)}

    @app.post("/api/studies/{sid}/groups")
    def new_group(sid: int, b: NameIn, u=Depends(current_user)):
        return {"id": store.add_group(u, sid, b.name, b.description)}

    @app.post("/api/studies/{sid}/specimens")
    def new_specimen(sid: int, b: SpecimenIn, u=Depends(current_user)):
        return {"id": store.add_specimen(u, sid, b.animal_id, b.group_id, b.sex)}

    @app.post("/api/studies/{sid}/timepoints")
    def new_tp(sid: int, b: TimepointIn, u=Depends(current_user)):
        return {"id": store.add_timepoint(u, sid, b.label, b.days)}

    @app.post("/api/studies/{sid}/unblind")
    def unblind(sid: int, reason: str = Form(...), u=Depends(current_user)):
        store.unblind(u, sid, reason)
        return {"ok": True}

    @app.get("/api/studies/{sid}/results")
    def results(sid: int, u=Depends(current_user)):
        rows = store.latest_measurements(u, sid)
        out = []
        for r in rows:
            cv = r["metrics"].get("metrics", {}).get("class_volumes", {})
            out.append({"scan_id": r["scan_id"], "specimen_id": r["specimen_id"], "timepoint_id": r["timepoint_id"],
                        "segmentation_id": r["segmentation_id"], **cv})
        return out

    @app.get("/api/studies/{sid}/export")
    def export(sid: int, u=Depends(current_user)):
        return SafeJSONResponse(json.loads(json.dumps(store.export_study(u, sid), default=str)))

    # ---------------------------------------------------------------- scans
    @app.post("/api/studies/{sid}/scans")
    async def upload(sid: int, file: UploadFile = File(...), specimen_id: int | None = Form(None),
                     timepoint_id: int | None = Form(None), spacing_um: float | None = Form(None),
                     acquisition: str = Form("{}"), u=Depends(current_user)):
        from ..io import read_volume, write_zarr, sha256_file
        from ..io.safe_archive import safe_extract
        from ..io.readers import check_safe_input
        st = store.study(u, sid)
        store.require(u, "write", st["org_id"])
        name = re.sub(r"[^A-Za-z0-9_.\-]", "_", Path(file.filename or "upload").name)[:120] or "upload"
        if not name.strip("."):   # S-21: '.', '..' would resolve to a directory
            name = "upload"
        tmp = store.data_dir / "uploads" / uuid.uuid4().hex
        tmp.mkdir(parents=True)
        try:
            dest = tmp / name
            size = 0
            with open(dest, "wb") as f:
                while True:
                    b = await file.read(1 << 22)
                    if not b:
                        break
                    size += len(b)
                    if size > MAX_UPLOAD:
                        raise HTTPException(413, "Upload exceeds size limit")
                    f.write(b)
            fsha = sha256_file(dest)
            src = dest
            if name.lower().endswith((".tar", ".tgz", ".tar.gz")):
                raise HTTPException(400, "TAR archives are not accepted; upload a ZIP")
            if name.lower().endswith(".zip"):
                ex = tmp / "extracted"
                safe_extract(dest, ex, allow_tar=False)
                check_safe_input(ex)   # whole extracted tree, not only the folder that is read (G2-05)
                subdirs = {Path(p).parent for p in ex.rglob("*") if p.is_file()}
                src = max(subdirs, key=lambda d: len(list(d.iterdir())))
            try:
                acq = json.loads(acquisition or "{}")
            except json.JSONDecodeError:
                raise HTTPException(400, "acquisition must be JSON") from None
            vol, rep = read_volume(src, spacing_um=spacing_um, safe=True)
            if rep.errors:
                raise HTTPException(422, f"Ingest errors: {rep.errors[:3]}")
            scan_id = store.register_scan(u, sid, specimen_id, timepoint_id, "", name, rep.format, fsha,
                                          vol.content_hash(), list(vol.shape), list(vol.spacing),
                                          {"ingest": rep.to_dict()}, acq)
            p = _store_path(store, st["org_id"], scan_id)
            write_zarr(vol, p)
            store.exec("UPDATE scans SET store_path=? WHERE id=?", (str(p), scan_id))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        jid = runner.submit(u, "qc", {"scan_id": scan_id})
        return {"scan_id": scan_id, "qc_job": jid, "warnings": rep.warnings}

    @app.get("/api/scans/{scan_id}")
    def scan_info(scan_id: int, u=Depends(current_user)):
        import zarr
        sc = store.scan(u, scan_id)
        g = zarr.open_group(sc["store_path"], mode="r")
        a = g["image"]
        s = np.asarray(a[:: max(1, a.shape[0] // 16), ::4, ::4]).astype(np.float32)
        layers = sorted(k for k in g["labels"].keys()) if "labels" in g else []
        store.audit.record("scan.view", u["id"], u["org_id"], "scan", scan_id)   # review S-12: record data access
        return {**{k: sc[k] for k in ("id", "study_id", "specimen_id", "timepoint_id", "source_name", "format", "shape",
                                       "spacing_um", "status", "file_sha256", "qc")},
                "window": {"p1": float(np.percentile(s, 1)), "p99": float(np.percentile(s, 99.5)),
                           "min": float(s.min()), "max": float(s.max())},
                "layers": layers, "segmentations": store.segmentations(u, scan_id),
                "roi": store.latest_roi(u, scan_id), "roi_history": store.roi_history(u, scan_id)}

    def _slice(arr, axis, index):
        n = arr.shape[axis]
        if not 0 <= index < n:
            raise HTTPException(400, "slice index out of range")
        sl = [slice(None)] * 3
        sl[axis] = index
        return np.asarray(arr[tuple(sl)])

    @app.get("/api/scans/{scan_id}/slice")
    def get_slice(scan_id: int, axis: int = 0, index: int = 0, layer: str = "image", lo: float | None = None,
                  hi: float | None = None, u=Depends(current_user)):
        import zarr
        from PIL import Image as PImage
        if axis not in (0, 1, 2) or not re.fullmatch(r"image|labels/[A-Za-z0-9_]+", layer):
            raise HTTPException(400, "bad parameters")
        sc = store.scan(u, scan_id)
        g = zarr.open_group(sc["store_path"], mode="r")
        if layer not in g:
            raise HTTPException(404, "layer not found")
        s = _slice(g[layer], axis, index).astype(np.float32)
        if layer == "image":
            lo = s.min() if lo is None else lo
            hi = s.max() if hi is None else hi
            s = np.clip((s - lo) / max(hi - lo, 1e-6) * 255, 0, 255)
        buf = io.BytesIO()
        PImage.fromarray(s.astype(np.uint8)).save(buf, "PNG")
        return Response(buf.getvalue(), media_type="image/png", headers={"Cache-Control": "no-store"})

    @app.get("/api/scans/{scan_id}/mesh")
    def mesh(scan_id: int, layer: str, label: int, step: int = 2, u=Depends(current_user)):
        import zarr
        from skimage.measure import marching_cubes
        if not re.fullmatch(r"labels/[A-Za-z0-9_]+", layer) or not 1 <= step <= 8:
            raise HTTPException(400, "bad parameters")
        sc = store.scan(u, scan_id)
        g = zarr.open_group(sc["store_path"], mode="r")
        m = (np.asarray(g[layer][::step, ::step, ::step]) == label).astype(np.float32)
        if m.sum() < 10:
            return {"vertices": [], "faces": []}
        sp = [s * step / 1000 for s in sc["spacing_um"]]
        v, f, _, _ = marching_cubes(np.pad(m, 1), 0.5, spacing=sp)
        v = v[:, ::-1]                       # (z,y,x) -> (x,y,z) so exported OBJ is not mirrored
        f = f[:, ::-1]                       # keep outward-facing winding after the axis swap
        return {"vertices": np.round(v, 3).ravel().tolist(), "faces": f.ravel().tolist(), "units": "mm", "order": "xyz"}

    @app.post("/api/scans/{scan_id}/analyze")
    def analyze_scan(scan_id: int, b: AnalyzeIn, u=Depends(current_user)):
        store.scan(u, scan_id)
        return {"job_id": runner.submit(u, "analyze", {"scan_id": scan_id, "config": b.config.model_dump(exclude_none=True),
                                                       "use_saved_roi": b.use_saved_roi})}

    @app.put("/api/scans/{scan_id}/roi")
    def put_roi(scan_id: int, b: ROIIn, u=Depends(current_user)):
        from ..roi import ROI
        roi = ROI.from_dict(b.definition)
        if roi.kind == "mask":
            raise HTTPException(400, "mask ROIs must be uploaded as label volumes")
        sc = store.scan(u, scan_id)
        roi.to_mask(tuple(sc["shape"]), tuple(sc["spacing_um"]))  # validates parameters
        rid, v = store.save_roi(u, scan_id, roi.to_dict(), b.reason)
        return {"roi_id": rid, "version": v, "definition_sha256": roi.definition_hash()}

    @app.post("/api/scans/{scan_id}/segmentations/edits")
    def edit_seg(scan_id: int, b: EditsIn, u=Depends(current_user)):
        """Apply brush / component edits to a segmentation version → new 'corrected' version."""
        import zarr
        from ..io import write_labels_zarr
        from ..pipeline import labels_hash
        from ..morphometry import defect_report_metrics
        from ..volume import Volume
        sc = store.scan(u, scan_id)
        store.require(u, "write", sc["org_id"])
        segs = {s["version"]: s for s in store.segmentations(u, scan_id)}
        if b.base_version not in segs:
            raise HTTPException(404, "base version not found")
        base = segs[b.base_version]
        g = zarr.open_group(sc["store_path"], mode="r")
        lab = np.asarray(g[f"labels/{base['labels_key']}"][:]).copy()
        before = np.bincount(lab.ravel(), minlength=256)
        for op in b.ops:
            if op.label not in (0, 1, 2, 3, 255):
                raise HTTPException(400, "invalid label")
            if op.index >= lab.shape[op.axis]:
                raise HTTPException(400, "slice index out of range")
            sl = [slice(None)] * 3
            sl[op.axis] = op.index
            plane = lab[tuple(sl)]
            if op.op == "brush":
                yy, xx = np.ogrid[: plane.shape[0], : plane.shape[1]]
                m = (yy - op.cy) ** 2 + (xx - op.cx) ** 2 <= op.r ** 2
            else:
                from scipy import ndimage as ndi
                y0, x0 = int(round(op.cy)), int(round(op.cx))
                if not (0 <= y0 < plane.shape[0] and 0 <= x0 < plane.shape[1]):
                    raise HTTPException(400, "seed outside slice")
                cc, _ = ndi.label(plane == plane[y0, x0])
                m = cc == cc[y0, x0]
            if op.only_from is not None:
                m &= plane == op.only_from
            plane[m] = op.label
            lab[tuple(sl)] = plane
        after = np.bincount(lab.ravel(), minlength=256)
        changed = {str(c): int(after[c] - before[c]) for c in (0, 1, 2, 3, 255) if after[c] != before[c]}
        edits = {"base_version": b.base_version, "n_ops": len(b.ops), "voxel_count_change": changed, "reason": b.reason,
                 "ops": [o.model_dump() for o in b.ops[:200]]}
        sid, v = store.save_segmentation(u, scan_id, "corrected", "", labels_hash(lab), method=base["method"],
                                         model_name=base["model_name"], model_sha256=base["model_sha256"],
                                         roi_id=base["roi_id"], parent_id=base["id"], edits=edits)
        key = f"seg_v{v}"
        store.exec("UPDATE segmentations SET labels_key=? WHERE id=?", (key, sid))
        write_labels_zarr(sc["store_path"], key, lab)
        rk = f"labels/roi_v{b.base_version}"
        rk = rk if rk in g else ("labels/roi_current" if "labels/roi_current" in g else None)
        roi = np.asarray(g[rk][:]).astype(bool) if rk else np.ones(lab.shape, bool)
        base_m = store.q1("SELECT metrics FROM measurements WHERE segmentation_id=? ORDER BY id DESC LIMIT 1", (base["id"],))
        thick = json.loads(base_m["metrics"]).get("config", {}).get("thickness_metrics", True) if base_m else True
        vol = Volume(np.asarray(g["image"][:]), tuple(sc["spacing_um"]))
        met = defect_report_metrics(lab, roi, vol, thickness=thick)   # same ROI and endpoint set as the base version
        write_labels_zarr(sc["store_path"], f"roi_v{v}", roi.astype(np.uint8))
        prev = json.loads(base_m["metrics"]) if base_m else {}
        record = {"metrics": met, "corrected_from": b.base_version, "config": {"thickness_metrics": thick},
                  "segmentation": prev.get("segmentation")}
        if prev.get("measurement_support"):
            # carry the base assessment over; read time downgrades it for the manual edit (C3-SCI-02, C3-PRD-04).
            # Without it the record has no assessment and reports fail closed.
            from ..advisor.integration import apply_support
            record["measurement_support"] = prev["measurement_support"]
            record["reported_metrics"], record["suppressed_metrics"] = apply_support(met, prev["measurement_support"])
        store.save_measurement(u, scan_id, sid, base["roi_id"], record, __version__)
        return {"segmentation_id": sid, "version": v, "voxel_count_change": changed,
                "class_volumes": met["class_volumes"]}

    # ---------------------------------------------------------------- review / reports / jobs / audit
    @app.post("/api/reviews")
    def review(b: ReviewIn, u=Depends(current_user)):
        if not store.reauthenticate(u, b.password):   # counts towards lockout (Gen-2 G2-03)
            store.audit.record("review.reauth_failed", u["id"], u["org_id"], b.object_type, b.object_id)
            raise HTTPException(401, "Re-authentication failed")
        return {"id": store.review(u, b.object_type, b.object_id, b.decision, b.meaning, b.comment)}

    @app.post("/api/studies/{sid}/report")
    def make_report(sid: int, u=Depends(current_user)):
        store.study(u, sid)
        return {"job_id": runner.submit(u, "report", {"study_id": sid})}

    @app.get("/api/reports/{rid}/{kind}")
    def get_report(rid: int, kind: str, u=Depends(current_user)):
        r = store.q1("SELECT * FROM reports WHERE id=?", (rid,))
        if not r:
            raise HTTPException(404, "report not found")
        store.require(u, "read", r["org_id"])
        if r.get("unblinded") and not store.can(u, "unblind"):
            store.audit.record("report.blinded_download_denied", u["id"], u["org_id"], "report", rid)
            raise HTTPException(403, "This report contains unblinded group allocation")
        if kind not in ("pdf", "csv") or r["status"] != "ready":
            raise HTTPException(400, "not available")
        store.audit.record("report.download", u["id"], u["org_id"], "report", rid, {"kind": kind})
        p = r["pdf_path"] if kind == "pdf" else r["csv_path"]
        return FileResponse(p, media_type="application/pdf" if kind == "pdf" else "text/csv",
                            filename=f"defectfill_report_{rid}.{kind}")

    @app.get("/api/jobs")
    def jobs(u=Depends(current_user)):
        return runner.list(u)

    @app.get("/api/jobs/{jid}")
    def job(jid: int, u=Depends(current_user)):
        return runner.get(u, jid)

    @app.post("/api/jobs/{jid}/cancel")
    def cancel(jid: int, u=Depends(current_user)):
        runner.cancel(u, jid)
        return {"ok": True}

    @app.get("/api/audit")
    def audit(object_type: str | None = None, object_id: str | None = None, u=Depends(current_user)):
        if not (store.can(u, "review") or store.can(u, "manage_users")):
            raise HTTPException(403, "audit trail requires reviewer or admin role")
        return store.audit.events(org_id=u["org_id"], object_type=object_type, object_id=object_id)

    @app.get("/api/audit/verify")
    def audit_verify(u=Depends(current_user)):
        store.require(u, "read")
        return store.audit.verify_chain()

    @app.get("/api/health")
    def health():
        return {"ok": True, "version": __version__, "status": "research prototype — not validated"}

    if WEB.exists():
        app.mount("/", StaticFiles(directory=str(WEB), html=True), name="web")
    return app
