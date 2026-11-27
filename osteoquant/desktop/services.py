"""Application services: the desktop's only route into the OsteoQuant library.

Everything here is plain Python (no widgets) so it can be unit-tested and reused by the
self-test. Long-running functions take a ``ctx`` with ``progress(frac, msg)`` / ``check()``
(see ``jobs.JobContext``) and are executed on worker threads by ``jobs.JobManager``.

Science is never re-implemented here: reading uses ``osteoquant.io``, QC ``osteoquant.qc``,
analysis is the same job handler the web API uses (``osteoquant.api.app.job_analyze``),
reports use ``osteoquant.api.bundle`` + ``osteoquant.report.build_pdf``.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import shutil
import uuid
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from .. import LABELS, __version__
from ..io import detect_format, read_volume, sha256_file
from ..io.readers import SUFFIX_FORMATS
from ..volume import Volume

# Volumes larger than this are imported slab by slab (bounded memory) when the format allows
# reading a z-range without decoding the whole file.
SLAB_IMPORT_BYTES = int(os.environ.get("OQ_SLAB_IMPORT_BYTES", str(1 << 30)))
SLAB_FORMATS = {"tiff-stack", "image-stack", "dicom", "zarr", "txm"}
# QC runs on the full-resolution volume up to this size, otherwise on a decimated copy (recorded).
QC_FULL_RES_BYTES = int(os.environ.get("OQ_QC_FULL_RES_BYTES", str(2 << 30)))


class NullContext:
    """Stand-in job context for synchronous calls (tests, self-test)."""

    def progress(self, frac: float, msg: str = ""):
        pass

    def check(self):
        pass


# ============================================================================ import: probing
@dataclass
class SourceProbe:
    path: str
    format: str | None = None
    shape: tuple | None = None
    dtype: str | None = None
    spacing_um: list | None = None
    spacing_source: str = "missing"          # file | assumed | missing
    metadata_found: dict = field(default_factory=dict)
    metadata_assumed: dict = field(default_factory=dict)
    warnings: list = field(default_factory=list)
    error: str | None = None
    size_bytes: int | None = None

    @property
    def ok(self) -> bool:
        return self.error is None

    @property
    def spacing_needs_entry(self) -> bool:
        """True when the voxel size is not reliably in the file and the user must type it."""
        return self.spacing_source != "file"

    def summary_rows(self) -> list[tuple[str, str]]:
        rows = [("Format", self.format or "unknown"),
                ("Dimensions (z, y, x)", " x ".join(map(str, self.shape)) if self.shape else "unknown"),
                ("Data type", self.dtype or "unknown"),
                ("Estimated size", f"{self.size_bytes / 1e6:,.1f} MB" if self.size_bytes else "unknown"),
                ("Voxel spacing from file", ("%s µm" % ", ".join(f"{s:g}" for s in self.spacing_um))
                 if self.spacing_um and self.spacing_source == "file" else "not available")]
        for k, v in sorted(self.metadata_found.items()):
            if k in ("spacing_um", "affine"):
                continue
            rows.append((f"File metadata: {k}", str(v)[:120]))
        for k, v in sorted(self.metadata_assumed.items()):
            rows.append((f"ASSUMED by reader: {k}", str(v)[:120]))
        return rows


def supported_suffixes() -> list[str]:
    return sorted(SUFFIX_FORMATS)


def find_candidates(path) -> list[Path]:
    """A file or a folder that is itself one volume (DICOM series, TIFF stack, Zarr) gives
    one candidate; otherwise each readable child (one level deep) is a candidate."""
    p = Path(path)
    if p.is_file():
        return [p]
    if not p.is_dir():
        return []
    try:
        detect_format(p)
        return [p]
    except ValueError:
        pass
    out = []
    for c in sorted(p.iterdir()):
        if c.name.startswith("."):
            continue
        try:
            detect_format(c)
            out.append(c)
        except (ValueError, OSError):
            continue
    return out


def _full_depth(path: Path, fmt: str) -> tuple[tuple | None, str | None]:
    """Shape and dtype from headers only (no pixel decoding)."""
    try:
        if fmt == "nifti":
            import nibabel as nib
            img = nib.load(str(path))
            sh = img.shape[:3]
            return (sh[2], sh[1], sh[0]), str(img.get_data_dtype())
        if fmt == "nrrd":
            import nrrd
            h = nrrd.read_header(str(path))
            sz = list(h["sizes"])
            return tuple(sz[::-1]), str(h.get("type"))
        if fmt in ("tiff", "ome-tiff"):
            import tifffile
            with tifffile.TiffFile(path) as tf:
                s = tf.series[0]
                sh = tuple(d for d in s.shape if d != 1)
                sh = sh if len(sh) == 3 else (1,) + tuple(sh[-2:])
                return sh, str(s.dtype)
        if fmt == "zarr":
            import zarr
            a = zarr.open_group(str(path), mode="r")["image"]
            return tuple(a.shape), str(a.dtype)
        if fmt == "npy":
            a = np.load(path, mmap_mode="r")
            return tuple(a.shape), str(a.dtype)
        if fmt == "txm":
            from ..io import txm_metadata
            md = txm_metadata(path)
            return (md["n_images"] or md["n_image_streams"], md["height"], md["width"]), None
        if fmt == "itk":
            import SimpleITK as sitk
            r = sitk.ImageFileReader()
            r.SetFileName(str(path))
            r.ReadImageInformation()
            return tuple(r.GetSize()[::-1]), r.GetPixelIDTypeAsString()
    except Exception:  # noqa: BLE001 - probing is best-effort; the real read reports errors
        return None, None
    return None, None


def probe_source(path) -> SourceProbe:
    """Detect format and read metadata plus one slice. Never raises: errors are reported."""
    p = Path(path)
    pr = SourceProbe(str(p))
    try:
        pr.format = detect_format(p)
    except (ValueError, OSError) as e:
        pr.error = str(e)
        return pr
    shape, dtype = _full_depth(p, pr.format)
    try:
        vol, rep = read_volume(p, zrange=(0, 1), do_hash=False)
    except ModuleNotFoundError as e:
        pr.error = f"support for this format is not included in this installation ({e.name} missing)"
        return pr
    except Exception as e:  # noqa: BLE001
        pr.error = f"{type(e).__name__}: {e}"
        return pr
    pr.metadata_found = {k: v for k, v in rep.metadata_found.items()}
    pr.metadata_assumed = dict(rep.metadata_assumed)
    pr.warnings = list(rep.warnings)
    if rep.errors:
        pr.error = "; ".join(rep.errors[:3])
    if shape is None:
        if pr.format in ("tiff-stack", "image-stack", "dicom"):
            n = len([f for f in p.iterdir() if f.is_file() and not f.name.startswith(".")]) if p.is_dir() else 1
            shape = (n,) + tuple(vol.shape[1:])
        else:
            shape = tuple(vol.shape)
    pr.shape = tuple(int(s) for s in shape)
    pr.dtype = dtype or str(vol.data.dtype)
    try:
        itemsize = np.dtype(pr.dtype).itemsize
    except TypeError:
        itemsize = vol.data.dtype.itemsize
    pr.size_bytes = int(np.prod(pr.shape)) * itemsize
    sp = rep.metadata_found.get("spacing_um")
    assumed = ("spacing_um" in rep.metadata_assumed or "spatial_unit" in rep.metadata_assumed
               or "slice_spacing" in rep.metadata_assumed)
    if pr.format == "dicom":
        try:
            import pydicom
            f0 = next(f for f in (sorted(p.iterdir()) if p.is_dir() else [p]) if f.is_file())
            ds = pydicom.dcmread(f0, stop_before_pixels=True)
            if getattr(ds, "PixelSpacing", None) is None:
                assumed = True
                pr.metadata_assumed["pixel_spacing"] = "missing in DICOM header (reader default 1 mm)"
            sp = [float(s) * 1000.0 for s in vol.spacing] if sp is None else sp
        except Exception:  # noqa: BLE001
            assumed = True
    if sp is None and not assumed and pr.format in ("tiff-stack", "image-stack"):
        assumed = True
    if sp is not None:
        pr.spacing_um = [float(s) for s in sp]
    pr.spacing_source = "missing" if sp is None else ("assumed" if assumed else "file")
    return pr


def validate_spacing(values) -> tuple[float, float, float]:
    try:
        sp = tuple(float(v) for v in values)
    except (TypeError, ValueError) as e:
        raise ValueError("Voxel spacing must be three numbers in µm") from e
    if len(sp) != 3 or any((not math.isfinite(s)) or s <= 0 for s in sp):
        raise ValueError("Voxel spacing must be three positive numbers in µm")
    if any(s > 5000 for s in sp):
        raise ValueError("Voxel spacing above 5000 µm is implausible for micro-CT; check the unit (µm)")
    return sp


# ============================================================================ import: execution
@dataclass
class ImportRequest:
    source: str
    spacing_um: tuple
    spacing_confirmed: bool
    study_id: int
    specimen_id: int | None = None
    timepoint_id: int | None = None
    acquisition: dict = field(default_factory=dict)


@dataclass
class ImportOutcome:
    source: str
    status: str                 # imported | flagged | rejected
    reason: str = ""
    scan_id: int | None = None
    qc: dict | None = None
    warnings: list = field(default_factory=list)

    @property
    def qc_deterministic(self) -> list[dict]:
        return [c for c in (self.qc or {}).get("checks", []) if c.get("basis") == "deterministic"]

    @property
    def qc_heuristic(self) -> list[dict]:
        return [c for c in (self.qc or {}).get("checks", []) if c.get("basis") != "deterministic"]


def source_manifest(src: Path) -> tuple[str, list[dict]]:
    """SHA-256 of a file, or of the sorted (relative path, file SHA-256) list of a folder."""
    if src.is_file():
        h = sha256_file(src)
        return h, [{"path": str(src), "sha256": h, "bytes": src.stat().st_size}]
    files = sorted(f for f in src.rglob("*") if f.is_file())
    recs = [{"path": str(f), "sha256": sha256_file(f), "bytes": f.stat().st_size} for f in files]
    h = hashlib.sha256("\n".join(f"{Path(r['path']).relative_to(src).as_posix()}:{r['sha256']}"
                                 for r in recs).encode()).hexdigest()
    return h, recs


def _scan_store_path(store, org_id, scan_id) -> Path:
    # same layout as osteoquant.api.app._store_path so both front ends share projects
    p = store.data_dir / f"org{int(org_id)}" / "scans" / f"scan{int(scan_id)}.zarr"
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def _write_store(dest: Path, src: Path, fmt: str, spacing, shape_hint, ctx) -> tuple[dict, str, tuple, str]:
    """Read ``src`` into a Zarr store at ``dest``. Returns (ingest report dict, content sha256,
    shape, dtype). Large slab-capable sources are copied slab by slab."""
    import zarr
    from ..io import write_zarr
    from ..io.writers import _jsonable
    est = int(np.prod(shape_hint)) * 2 if shape_hint else 0
    if fmt not in SLAB_FORMATS or est <= SLAB_IMPORT_BYTES or not shape_hint:
        ctx.progress(0.1, "reading volume")
        vol, rep = read_volume(src, spacing_um=spacing, do_hash=False)
        ctx.check()
        if rep.errors:
            raise ValueError("Reader errors: " + "; ".join(rep.errors[:3]))
        ctx.progress(0.45, "writing chunked store")
        h = write_zarr(vol, dest)
        return rep.to_dict(), h, tuple(vol.shape), str(vol.data.dtype)
    n = int(shape_hint[0])
    slab = max(8, int(SLAB_IMPORT_BYTES // max(1, est // n) // 2))
    g = arr = hasher = None
    merged = None
    meta = {}
    vol0 = None
    for z0 in range(0, n, slab):
        z1 = min(n, z0 + slab)
        ctx.progress(0.05 + 0.5 * z0 / n, f"reading slices {z0}-{z1 - 1} of {n}")
        vol, rep = read_volume(src, spacing_um=spacing, zrange=(z0, z1), do_hash=False)
        if rep.errors:
            raise ValueError("Reader errors: " + "; ".join(rep.errors[:3]))
        if g is None:
            vol0 = vol
            full_shape = (n,) + tuple(vol.shape[1:])
            g = zarr.open_group(str(dest), mode="w")
            ch = tuple(min(c, s) for c, s in zip((64, 64, 64), full_shape))
            arr = g.create_array("image", shape=full_shape, chunks=ch, dtype=vol.data.dtype)
            hasher = hashlib.sha256(json.dumps({"shape": list(full_shape), "dtype": str(vol.data.dtype),
                                                "spacing": list(vol.spacing)}).encode())
            merged = rep.to_dict()
            meta = dict(vol.meta)
        else:
            merged["warnings"] += [w for w in rep.warnings if w not in merged["warnings"]]
            merged["missing_slices"] += [z0 + m for m in rep.missing_slices]
        arr[z0:z0 + vol.shape[0]] = vol.data
        hasher.update(np.ascontiguousarray(vol.data).tobytes())
        ctx.check()
    merged["zrange"] = [0, n]
    merged["slab_import"] = {"slab_slices": slab}
    h = hasher.hexdigest()
    meta["ingest"] = merged
    g.attrs.update({"spacing_um": list(vol0.spacing), "origin_um": list(vol0.origin), "meta": _jsonable(meta),
                    "content_sha256": h, "osteoquant_version": __version__})
    return merged, h, tuple(arr.shape), str(arr.dtype)


def load_scan_volume(store, user, scan_id, max_bytes: int | None = None) -> tuple:
    """Load a stored scan as a Volume with its ingest record (as the web API does). If the
    volume exceeds ``max_bytes`` it is decimated by an integer stride; the stride is returned."""
    import zarr
    sc = store.scan(user, scan_id)
    a = zarr.open_group(sc["store_path"], mode="r")["image"]
    step = 1
    if max_bytes:
        nbytes = int(np.prod(a.shape)) * a.dtype.itemsize
        while nbytes / step ** 3 > max_bytes:
            step += 1
    vol, _ = read_volume(sc["store_path"], step=step)
    stored = dict((sc["meta"] or {}).get("ingest", {}))
    stored.setdefault("metadata_found", {})["spacing_um"] = sc["spacing_um"]
    vol.meta["ingest"] = stored
    return sc, vol, step


def run_scan_qc(project, scan_id, ctx=None) -> dict:
    from ..qc import run_qc
    ctx = ctx or NullContext()
    store, user = project.store, project.require_user()
    ctx.progress(0.6, "loading for QC")
    sc, vol, step = load_scan_volume(store, user, scan_id, QC_FULL_RES_BYTES)
    ctx.check()
    ctx.progress(0.7, "running QC")
    qc = run_qc(vol)
    if step > 1:
        qc["decimated_for_qc"] = {"step": step, "note": f"QC computed on a {step}x decimated copy (memory bound)"}
    store.set_scan_qc(user, scan_id, qc)
    return qc


def import_scan(project, req: ImportRequest, ctx=None, probe: SourceProbe | None = None) -> ImportOutcome:
    """Import one volume into a study and run QC. Never drops a source silently: every
    failure is returned as a ``rejected`` outcome, written to the project's import log and to
    the audit trail."""
    ctx = ctx or NullContext()
    store, user = project.store, project.require_user()
    src = Path(req.source)

    def reject(reason, **details):
        project.log_import(req.study_id, src, "rejected", reason, details=details)
        return ImportOutcome(str(src), "rejected", reason)

    try:
        spacing = validate_spacing(req.spacing_um)
    except ValueError as e:
        return reject(str(e))
    probe = probe or probe_source(src)
    if not probe.ok:
        return reject(f"Unreadable: {probe.error}")
    if probe.spacing_needs_entry and not req.spacing_confirmed:
        return reject("Voxel spacing is not recorded reliably in the file and was not confirmed by the user")
    st = store.study(user, req.study_id)
    store.require(user, "write", st["org_id"])
    tmp = store.data_dir / "incoming" / (uuid.uuid4().hex + ".zarr")
    tmp.parent.mkdir(parents=True, exist_ok=True)
    try:
        ctx.progress(0.02, "hashing source files")
        file_sha, files = source_manifest(src)
        ctx.check()
        try:
            ingest, content_sha, shape, dtype = _write_store(tmp, src, probe.format, spacing, probe.shape, ctx)
        except Exception as e:  # noqa: BLE001
            from ..study.jobs import JobCancelled
            if isinstance(e, JobCancelled):
                raise
            return reject(f"Read failed: {type(e).__name__}: {e}")
        ingest["files"] = files
        ingest["spacing_confirmed_by_user"] = bool(req.spacing_confirmed)
        ingest["spacing_source"] = probe.spacing_source
        try:
            scan_id = store.register_scan(user, req.study_id, req.specimen_id, req.timepoint_id, "", src.name,
                                          probe.format, file_sha, content_sha, list(shape), list(spacing),
                                          {"ingest": ingest}, req.acquisition)
        except ValueError as e:
            return reject(str(e), file_sha256=file_sha)
        dest = _scan_store_path(store, st["org_id"], scan_id)
        if dest.exists():
            shutil.rmtree(dest)
        shutil.move(str(tmp), str(dest))
        store.exec("UPDATE scans SET store_path=? WHERE id=?", (str(dest), scan_id))
        ctx.check()
        qc = run_scan_qc(project, scan_id, ctx)
        ctx.progress(1.0, "done")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    if qc["verdict"] == "suitable":
        status, reason = "imported", "QC suitable"
    else:
        bad = [f"{c['id']} {c['name']} ({c['status']})" for c in qc["checks"] if c["status"] in ("fail", "warn")]
        status = "flagged"
        reason = f"QC {qc['verdict']}: " + "; ".join(bad[:6])
    project.log_import(req.study_id, src, status, reason, scan_id=scan_id, details={"verdict": qc["verdict"]})
    return ImportOutcome(str(src), status, reason, scan_id, qc, list(ingest.get("warnings", [])))


def get_or_create_specimen(project, study_id, animal_id: str, group_id=None) -> int:
    store, user = project.store, project.require_user()
    r = store.q1("SELECT id FROM specimens WHERE study_id=? AND animal_id=?", (study_id, animal_id))
    if r:
        return r["id"]
    return store.add_specimen(user, study_id, animal_id, group_id)


def get_or_create_timepoint(project, study_id, label: str, days=None) -> int:
    store, user = project.store, project.require_user()
    r = store.q1("SELECT id FROM timepoints WHERE study_id=? AND label=?", (study_id, label))
    if r:
        return r["id"]
    return store.add_timepoint(user, study_id, label, days)


# ============================================================================ analysis
ANALYSIS_DEFAULTS = {"defect_model": "condyle", "segmentation": "multiotsu", "graft_brighter": True,
                     "thickness_metrics": True, "no_graft": False, "nominal_diameter_um": None}
# graft material ids understood by the measurement-support advisor (pipeline config "material")
GRAFT_MATERIALS = [("ha", "Hydroxyapatite (HA)"), ("beta_tcp", "beta-TCP"), ("bcp", "Biphasic calcium phosphate"),
                   ("calcium_sulfate", "Calcium sulfate"), ("bioglass_45s5", "Bioglass 45S5"),
                   ("xenograft_dbbm", "Xenograft (DBBM)"), ("allograft", "Allograft"), ("dbm", "Demineralised bone matrix"),
                   ("collagen_sponge", "Collagen sponge")]


def model_dir() -> Path:
    """Where the library looks for locked models (``osteoquant.ml.train.MODEL_DIR``), computed
    without importing PyTorch: ``<package parent>/models``. In the packaged application this is
    ``<install dir>/_internal/models``."""
    import osteoquant
    return Path(osteoquant.__file__).resolve().parents[1] / "models"


def available_models() -> list[dict]:
    """Locked segmentation models usable from the desktop: ONNX exports listed in the model
    registry with a hash, whose runtime can be imported. Returns [] when none are installed."""
    import importlib.util
    d = model_dir()
    reg_p = d / "registry.json"
    if not reg_p.exists() or importlib.util.find_spec("onnxruntime") is None:
        return []
    try:
        # osteoquant.ml.runtime currently imports helpers from ml.train, which needs PyTorch
        import osteoquant.ml.runtime  # noqa: F401
    except Exception:  # noqa: BLE001
        return []
    out = []
    for name, r in json.loads(reg_p.read_text()).items():
        if r.get("onnx_sha256") and (d / f"{name}.onnx").exists():
            out.append({"id": f"onnx:{name}", "name": name, "licence_tag": r.get("licence_tag", ""),
                        "provenance": r.get("provenance", "")})
    return out


def analyze_scan(project, scan_id, config: dict | None = None, ctx=None, use_saved_roi=True) -> dict:
    """Run the DefectFill pipeline on a stored scan via the shared job handler."""
    from ..api.app import job_analyze
    ctx = ctx or NullContext()
    cfg = {k: v for k, v in {**ANALYSIS_DEFAULTS, **(config or {})}.items() if v is not None}
    seg = str(cfg.get("segmentation", ""))
    if seg.startswith("rf:"):
        raise PermissionError("Pickled random-forest models are only available from the command line")
    res = job_analyze(project.store, project.require_user(), {"scan_id": scan_id, "config": cfg,
                                                              "use_saved_roi": use_saved_roi}, ctx)
    if res.get("status") == "needs_manual_roi":
        project.store.exec("UPDATE scans SET status='needs_manual_roi' WHERE id=?", (scan_id,))
    return res


def save_cylinder_roi(project, scan_id, center_vox, radius_um, extent_um, axis=(1.0, 0.0, 0.0), reason="") -> int:
    """Manual cylindrical ROI centred at a voxel (z, y, x); ``extent_um`` = (start, end)
    signed distance along the axis from the centre."""
    from ..roi import cylinder_roi
    store, user = project.store, project.require_user()
    sc = store.scan(user, scan_id)
    sp = sc["spacing_um"]
    c = [float(i) * float(s) for i, s in zip(center_vox, sp)]
    roi = cylinder_roi(c, axis, radius_um, extent_um, method="manual-desktop")
    roi.to_mask(tuple(sc["shape"]), tuple(sp))
    rid, _ = store.save_roi(user, scan_id, roi.to_dict(), reason or "manual ROI (desktop)")
    return rid


# ============================================================================ label revisions
def class_counts(labels: np.ndarray) -> dict[int, int]:
    bc = np.bincount(labels.ravel(), minlength=256)
    return {c: int(bc[c]) for c in LABELS}


def save_label_revision(project, scan_id: int, base_segmentation_id: int, labels: np.ndarray, reason: str,
                        operations: dict | None = None, ctx=None) -> dict:
    """Store edited labels as a new 'corrected' segmentation version.

    The audit trail records user (via the store), reason, base version, per-class voxel count
    change and an operation summary; endpoints are recomputed with the base version's ROI."""
    import zarr
    from ..io import write_labels_zarr
    from ..morphometry import defect_report_metrics
    from ..pipeline import labels_hash
    ctx = ctx or NullContext()
    if not reason or len(reason.strip()) < 3:
        raise ValueError("A reason (at least 3 characters) is required to save a label revision")
    store, user = project.store, project.require_user()
    sc = store.scan(user, scan_id)
    store.require(user, "write", sc["org_id"])
    base = store.q1("SELECT * FROM segmentations WHERE id=? AND scan_id=?", (base_segmentation_id, scan_id))
    if not base:
        raise KeyError("base segmentation not found")
    labels = np.asarray(labels, dtype=np.uint8)
    if tuple(labels.shape) != tuple(sc["shape"]):
        raise ValueError("label volume shape does not match the scan")
    bad = set(np.unique(labels).tolist()) - set(LABELS)
    if bad:
        raise ValueError(f"invalid label values {sorted(bad)}")
    g = zarr.open_group(sc["store_path"], mode="r")
    ctx.progress(0.1, "comparing with base version")
    before = class_counts(np.asarray(g[f"labels/{base['labels_key']}"][:]))
    after = class_counts(labels)
    changed = {LABELS[c]: after[c] - before[c] for c in LABELS if after[c] != before[c]}
    edits = {"base_version": base["version"], "voxel_count_change": changed, "reason": reason.strip(),
             "operations": operations or {}, "editor": f"OsteoQuant Desktop {__version__}"}
    sid, v = store.save_segmentation(user, scan_id, "corrected", "", labels_hash(labels), method=base["method"],
                                     model_name=base["model_name"], model_sha256=base["model_sha256"],
                                     roi_id=base["roi_id"], parent_id=base["id"], edits=edits)
    key = f"seg_v{v}"
    store.exec("UPDATE segmentations SET labels_key=? WHERE id=?", (key, sid))
    ctx.progress(0.3, "writing labels")
    write_labels_zarr(sc["store_path"], key, labels)
    g = zarr.open_group(sc["store_path"], mode="r")
    rk = f"labels/roi_v{base['version']}"
    rk = rk if rk in g else ("labels/roi_current" if "labels/roi_current" in g else None)
    roi = np.asarray(g[rk][:]).astype(bool) if rk else np.ones(labels.shape, bool)
    base_m = store.q1("SELECT metrics FROM measurements WHERE segmentation_id=? ORDER BY id DESC LIMIT 1", (base["id"],))
    thick = json.loads(base_m["metrics"]).get("config", {}).get("thickness_metrics", True) if base_m else True
    ctx.progress(0.5, "recomputing endpoints")
    vol = Volume(np.asarray(g["image"][:]), tuple(sc["spacing_um"]))
    met = defect_report_metrics(labels, roi, vol, thickness=thick)
    write_labels_zarr(sc["store_path"], f"roi_v{v}", roi.astype(np.uint8))
    prev = json.loads(base_m["metrics"]) if base_m else {}
    record = {"metrics": met, "corrected_from": base["version"], "config": prev.get("config", {"thickness_metrics": thick}),
              "qc": prev.get("qc"), "plausibility": prev.get("plausibility"), "uncertainty": prev.get("uncertainty"),
              "roi": prev.get("roi"), "status": "corrected_unreviewed"}
    if prev.get("measurement_support"):
        # support depends on image, ROI and config (not on the labels): carry it over and
        # rebuild the reported view of the recomputed metrics
        record["measurement_support"] = prev["measurement_support"]
        try:
            from ..advisor.integration import apply_support
            record["reported_metrics"], record["suppressed_metrics"] = apply_support(met, prev["measurement_support"])
        except ImportError:
            pass
    store.save_measurement(user, scan_id, sid, base["roi_id"], record, __version__)
    store.audit.record("segmentation.edit", user["id"], user["org_id"], "segmentation", sid,
                       {"scan": scan_id, "version": v, "base_version": base["version"], "reason": reason.strip(),
                        "voxel_count_change": changed, "operations": operations or {}})
    ctx.progress(1.0, "saved")
    return {"segmentation_id": sid, "version": v, "voxel_count_change": changed, "class_volumes": met["class_volumes"]}


# ============================================================================ review / sign-off
def sign_review(project, password: str, object_type: str, object_id: int, decision: str, meaning: str,
                comment: str = "") -> int:
    """Electronic sign-off with re-authentication (same rules as the web API)."""
    if not meaning or len(meaning.strip()) < 5:
        raise ValueError("State the meaning of the signature (at least 5 characters)")
    user = project.require_user()
    project.store.require(user, "review")
    if not project.reauthenticate(password, object_type, object_id):
        raise PermissionError("Re-authentication failed: password incorrect")
    return project.store.review(user, object_type, object_id, decision, meaning.strip(), comment)


# ============================================================================ reports
def generate_report(project, study_id: int, watermark: str | None = None, ctx=None) -> dict:
    """Build the DefectFill PDF + CSV for a study (as the web API's report job, plus an optional
    watermark for evaluation/test licences)."""
    from ..api.bundle import bundle_from_store
    from ..report import build_pdf
    ctx = ctx or NullContext()
    store, user = project.store, project.require_user()
    st = store.study(user, study_id)
    store.require(user, "read", st["org_id"])
    bundle = bundle_from_store(store, user, study_id, ctx)
    if not bundle["specimens"]:
        raise ValueError("This study has no analysed scans yet; run the analysis first")
    out = store.data_dir / f"org{user['org_id']}" / "reports"
    out.mkdir(parents=True, exist_ok=True)
    unblinded = int(bool(st["blinded"]) and store.can(user, "unblind"))
    rid = store.exec("INSERT INTO reports(org_id,study_id,status,created_by,created,unblinded) VALUES (?,?,?,?,datetime('now'),?)",
                     (user["org_id"], study_id, "building", user["id"], unblinded))
    pdf, csvp = out / f"report{rid}.pdf", out / f"report{rid}.csv"
    ctx.progress(0.85, "rendering PDF")
    try:
        r = build_pdf(bundle, pdf, csvp, watermark=watermark)
    except Exception:
        store.exec("UPDATE reports SET status='failed' WHERE id=?", (rid,))
        raise
    store.exec("UPDATE reports SET pdf_path=?, csv_path=?, sha256=?, status='ready' WHERE id=?",
               (str(pdf), str(csvp), r["pdf_sha256"], rid))
    store.audit.record("report.generate", user["id"], user["org_id"], "report", rid,
                       {"study": study_id, "sha256": r["pdf_sha256"], "watermark": watermark or ""})
    ctx.progress(1.0, "done")
    return {"report_id": rid, "pdf": str(pdf), "csv": str(csvp), "sha256": r["pdf_sha256"]}


def list_reports(project, study_id) -> list[dict]:
    user = project.require_user()
    project.store.study(user, study_id)
    return project.store.q("SELECT id, status, created, sha256, pdf_path, csv_path, unblinded FROM reports "
                           "WHERE study_id=? AND org_id=? ORDER BY id DESC", (study_id, user["org_id"]))


def export_report(project, report_id: int, dest_dir, kinds=("pdf", "csv")) -> list[str]:
    store, user = project.store, project.require_user()
    r = store.q1("SELECT * FROM reports WHERE id=?", (report_id,))
    if not r:
        raise KeyError("report not found")
    store.require(user, "read", r["org_id"])
    if r.get("unblinded") and not store.can(user, "unblind"):
        store.audit.record("report.blinded_download_denied", user["id"], user["org_id"], "report", report_id)
        raise PermissionError("This report contains unblinded group allocation")
    out = []
    for k in kinds:
        src = r["pdf_path"] if k == "pdf" else r["csv_path"]
        if src and Path(src).exists():
            d = Path(dest_dir) / f"defectfill_report_{report_id}.{k}"
            shutil.copyfile(src, d)
            out.append(str(d))
    store.audit.record("report.export", user["id"], user["org_id"], "report", report_id, {"files": out})
    return out
