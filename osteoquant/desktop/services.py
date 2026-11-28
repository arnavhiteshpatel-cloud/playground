"""Application services: the desktop's only route into the OsteoQuant library.

Everything here is plain Python (no widgets) so it can be unit-tested and reused by the
self-test. Long-running functions take a ``ctx`` with ``progress(frac, msg)`` / ``check()``
(see ``jobs.JobContext``) and are executed on worker threads by ``jobs.JobManager``.

Science is never re-implemented here: reading uses ``osteoquant.io``, QC ``osteoquant.qc``,
analysis is the same job handler the web API uses (``osteoquant.study.handlers.job_analyze``),
reports use ``osteoquant.api.bundle`` + ``osteoquant.report.build_pdf``.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import shutil
import threading
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


def _progress_after_commit(ctx, frac: float, msg: str = ""):
    """Progress report once the work is committed: a late cancellation request is ignored (the job
    either rolls back completely before its commit point or completes)."""
    from ..study.jobs import JobCancelled
    try:
        ctx.progress(frac, msg)
    except JobCancelled:
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
        try:
            if dest.exists():
                shutil.rmtree(dest)
            shutil.move(str(tmp), str(dest))
            store.exec("UPDATE scans SET store_path=? WHERE id=?", (str(dest), scan_id))
            ctx.check()
            qc = run_scan_qc(project, scan_id, ctx)
        except BaseException as e:
            # cancelled or failed after registration: remove the partial scan so that the source can be
            # imported again (C2-PRD-10); the audit trail keeps scan.import and the rollback event
            _rollback_import(project, req.study_id, src, scan_id, dest, e)
            raise
        _progress_after_commit(ctx, 1.0, "done")
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


def _rollback_import(project, study_id, src: Path, scan_id: int, dest: Path, err: BaseException):
    from ..study.jobs import JobCancelled
    store, user = project.store, project.user or {}
    cancelled = isinstance(err, JobCancelled)
    reason = "cancelled by user" if cancelled else f"{type(err).__name__}: {err}"
    try:
        with store.transaction():
            store.exec("DELETE FROM scans WHERE id=?", (scan_id,))
            store.exec("DELETE FROM desktop_blind_codes WHERE object_type='scan' AND object_id=?", (scan_id,))
            store.audit.record("scan.import_rolled_back", user.get("id"), user.get("org_id"), "scan", scan_id,
                               {"reason": reason})
        shutil.rmtree(dest, ignore_errors=True)
        if user:
            project.log_import(study_id, src, "cancelled" if cancelled else "rejected",
                               f"Import {'cancelled' if cancelled else 'failed'} before completion; nothing was kept "
                               f"({reason})")
    except Exception:  # noqa: BLE001 - never mask the original error
        pass


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
ANALYSIS_DEFAULTS = {"defect_model": "condyle", "segmentation": "advisor_threshold", "graft_brighter": True,
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


def model_registry() -> dict:
    """The locked-model registry (``models/registry.json``) or {} (no runtime imports)."""
    p = model_dir() / "registry.json"
    try:
        return json.loads(p.read_text()) if p.exists() else {}
    except (OSError, ValueError):
        return {}


def provenance_words(prov) -> str:
    """Model training provenance as words (never a Python list repr or a licence tag)."""
    items = prov if isinstance(prov, (list, tuple)) else ([prov] if prov else [])
    words = {"synthetic": "synthetic phantoms", "real": "real micro-CT scans", "public": "public micro-CT data",
             "customer": "customer micro-CT data"}
    out = [words.get(str(i).lower(), str(i).replace("_", " ")) for i in items if str(i).strip()]
    return ("trained on " + " and ".join(out)) if out else "training data not recorded"


def is_synthetic_trained(prov) -> bool:
    items = prov if isinstance(prov, (list, tuple)) else ([prov] if prov else [])
    low = [str(i).lower() for i in items]
    return bool(low) and all("synthetic" in i for i in low)


SYNTHETIC_CHIP = "SYNTHETIC-TRAINED — research only"


def segmentation_method_info(seg: dict | None, result: dict | None = None) -> dict:
    """Readable segmentation method and whether it used a model trained only on synthetic data.

    Consistent with the PDF report banner ("SYNTHETIC-TRAINED MODEL"): the chip is shown wherever
    the model is chosen or its results are shown."""
    seg = seg or {}
    method = str(seg.get("method") or ((result or {}).get("segmentation") or {}).get("method") or "")
    model = seg.get("model_name") or ((result or {}).get("segmentation") or {}).get("model_name")
    prov = ((result or {}).get("segmentation") or {}).get("model_provenance")
    if model and prov is None:
        prov = (model_registry().get(str(model).split(":")[-1]) or {}).get("provenance")
    if model or method.startswith("onnx:") or method.startswith("unet"):
        name = str(model or method).split(":")[-1]
        synth = is_synthetic_trained(prov)
        text = f"U-Net {name}" + (f" ({SYNTHETIC_CHIP})" if synth else "")
        return {"text": text, "short": f"U-Net {name}", "synthetic": synth, "provenance": provenance_words(prov)}
    if method == "advisor_threshold":
        return {"text": "Advisor threshold (carries measurement support)", "short": "Advisor threshold",
                "synthetic": False, "provenance": "thresholds from the measurement-support advisor (no trained model)"}
    if method in ("multiotsu", ""):
        return {"text": "Multi-Otsu (classical; no measurement support)" if method else "-", "short": "Multi-Otsu" if method else "-",
                "synthetic": False, "provenance": "classical thresholding (no trained model)"}
    return {"text": method, "short": method, "synthetic": False, "provenance": ""}


def available_models() -> list[dict]:
    """Locked segmentation models usable from the desktop: ONNX exports listed in the model
    registry with a hash, whose runtime can be imported. Returns [] when none are installed."""
    import importlib.util
    d = model_dir()
    reg_p = d / "registry.json"
    if not reg_p.exists() or importlib.util.find_spec("onnxruntime") is None:
        return []
    try:
        # osteoquant.ml.runtime imports torch-free helpers (ml.core); the import still fails if onnxruntime is absent
        import osteoquant.ml.runtime  # noqa: F401
    except Exception:  # noqa: BLE001
        return []
    out = []
    for name, r in json.loads(reg_p.read_text()).items():
        if r.get("onnx_sha256") and (d / f"{name}.onnx").exists():
            out.append({"id": f"onnx:{name}", "name": name, "licence_tag": r.get("licence_tag", ""),
                        "provenance": r.get("provenance", ""), "provenance_text": provenance_words(r.get("provenance")),
                        "synthetic": is_synthetic_trained(r.get("provenance"))})
    return out


# Time since implantation. The measurement-support advisor accepts intensity separation of resorbable materials
# only at a KNOWN timepoint <=4 weeks (advisor 1.3.x), so the desktop passes ``healing_weeks`` to the pipeline:
# "auto" = from the scan's timepoint (days, else a parseable label such as "Week 4"), "unknown" = explicitly unknown,
# or a number of weeks entered by the user (review C2-BIZ-04).
HEALING_AUTO = "auto"
HEALING_UNKNOWN = "unknown"
_TP_UNITS = {"d": 1 / 7, "day": 1 / 7, "days": 1 / 7, "w": 1.0, "wk": 1.0, "wks": 1.0, "week": 1.0, "weeks": 1.0,
             "m": 30.4375 / 7, "mo": 30.4375 / 7, "month": 30.4375 / 7, "months": 30.4375 / 7}


def parse_timepoint_weeks(label: str | None) -> float | None:
    """Weeks since implantation from a timepoint label, or None when it cannot be parsed unambiguously.

    Accepts e.g. "Week 4", "4 weeks", "wk4", "W4", "Day 28", "28 d", "D14", "3 months". "Day 0" gives 0.
    Labels with no unit (e.g. "T2", "Baseline") or with more than one number are not guessed."""
    import re
    if not label:
        return None
    s = str(label).strip().lower()
    nums = re.findall(r"\d+(?:\.\d+)?", s)
    if len(nums) != 1:
        return None
    m = (re.fullmatch(r"(?P<u>[a-z]+)\s*[-_ ]?\s*(?P<n>\d+(?:\.\d+)?)", s)
         or re.fullmatch(r"(?P<n>\d+(?:\.\d+)?)\s*[-_ ]?\s*(?P<u>[a-z]+)", s))
    if not m or m.group("u") not in _TP_UNITS:
        return None
    return round(float(m.group("n")) * _TP_UNITS[m.group("u")], 3)


def scan_healing_weeks(project, scan_id) -> tuple[float | None, str]:
    """(weeks, source) for a stored scan: from the timepoint's days, else its label, else (None, "unknown")."""
    store, user = project.store, project.require_user()
    sc = store.scan(user, scan_id)
    tp = store.q1("SELECT label, days FROM timepoints WHERE id=?", (sc["timepoint_id"],)) if sc.get("timepoint_id") else None
    if not tp:
        return None, "no timepoint assigned"
    if tp.get("days") is not None and float(tp["days"]) >= 0:
        return round(float(tp["days"]) / 7.0, 3), f"timepoint '{tp['label']}' ({float(tp['days']):g} days)"
    w = parse_timepoint_weeks(tp.get("label"))
    if w is not None:
        return w, f"timepoint label '{tp['label']}'"
    return None, f"timepoint '{tp['label']}' has no days and the label is not a parseable time"


def resolve_healing_weeks(project, scan_id, value=HEALING_AUTO) -> tuple[float | None, str]:
    """Resolve the analysis dialog's time-since-implantation setting for one scan."""
    if value is None or value == HEALING_AUTO:
        return scan_healing_weeks(project, scan_id)
    if value == HEALING_UNKNOWN:
        return None, "set to unknown by the user"
    w = float(value)
    if not (w >= 0 and w < 520):
        raise ValueError(f"time since implantation must be 0-520 weeks, got {value!r}")
    return w, "entered by the user"


ANALYSIS_MEMORY_FACTOR = 8      # peak bytes ≈ 8 × float32 volume (image, labels, probabilities, morphometry buffers)


def _memory_preflight(project, scan_id, available: int | None = None) -> tuple[int, int | None]:
    """Refuse an analysis that would not fit in memory, before loading anything (cycle-3 review C3-PRD-20: on Linux a
    too-large analysis is killed by the OS instead of raising MemoryError, and unsaved work is lost). Returns the
    estimated need and the available memory (None when it cannot be measured)."""
    sc = project.store.scan(project.require_user(), scan_id)
    shape = sc.get("shape") or []
    try:
        n = int(np.prod([int(x) for x in shape])) if shape else 0
    except (TypeError, ValueError):
        return 0, None
    need = n * 4 * ANALYSIS_MEMORY_FACTOR
    if available is None:
        try:
            import psutil
            available = int(psutil.virtual_memory().available)
        except Exception:  # noqa: BLE001 - without psutil the check is skipped
            return need, None
    if need > available:
        raise MemoryError(f"This analysis needs about {need / 2**30:.1f} GB of memory and {available / 2**30:.1f} GB is "
                          "available. Close other analyses or applications, or analyse a cropped or decimated copy.")
    return need, available


# Analyses whose estimated peak exceeds this share of the available memory run one at a time (C3-PRD-20: two large
# analyses started together could each pass the pre-flight and then exhaust memory together).
LARGE_ANALYSIS_SHARE = 0.4
_LARGE_ANALYSIS = threading.Lock()


def _large_analysis_slot(project, scan_id, need, available, ctx):
    """Wait (cancellably) for the single large-analysis slot when this analysis is large; re-check memory once it is
    obtained. Returns True when the slot is held and must be released by the caller."""
    if not need or available is None or need <= LARGE_ANALYSIS_SHARE * available:
        return False
    if not _LARGE_ANALYSIS.acquire(blocking=False):
        ctx.progress(0.0, "waiting for another large analysis to finish")
        while not _LARGE_ANALYSIS.acquire(timeout=0.5):
            ctx.check()                          # cancelling while waiting leaves nothing to roll back
    try:
        _memory_preflight(project, scan_id)      # memory may have changed while waiting
    except BaseException:
        _LARGE_ANALYSIS.release()
        raise
    return True


def analyze_scan(project, scan_id, config: dict | None = None, ctx=None, use_saved_roi=True) -> dict:
    """Run the DefectFill pipeline on a stored scan via the shared job handler.

    ``config["healing_weeks"]`` may be "auto" (default: from the scan's timepoint), "unknown", or a number
    of weeks; the resolved value and its source are recorded in the analysis configuration."""
    ctx = ctx or NullContext()
    config = dict(config or {})
    need, available = _memory_preflight(project, scan_id)
    held = _large_analysis_slot(project, scan_id, need, available, ctx)
    try:
        return _analyze_scan(project, scan_id, config, ctx, use_saved_roi)
    finally:
        if held:
            _LARGE_ANALYSIS.release()


def _analyze_scan(project, scan_id, config, ctx, use_saved_roi) -> dict:
    from ..study.handlers import job_analyze
    weeks, source = resolve_healing_weeks(project, scan_id, config.pop("healing_weeks", HEALING_AUTO))
    config["healing_weeks"] = weeks
    config["healing_weeks_source"] = source
    cfg = {k: v for k, v in {**ANALYSIS_DEFAULTS, **config}.items() if v is not None}
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
    if not reason or len(reason.strip()) < 3:     # dossier D-5 / C2-PRD-17: a typed reason, never a default
        raise ValueError("A reason (at least 3 characters) is required for a manual ROI; it is recorded in the "
                         "audit trail")
    roi.to_mask(tuple(sc["shape"]), tuple(sp))
    rid, _ = store.save_roi(user, scan_id, roi.to_dict(), reason.strip())
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
    rk = f"labels/roi_v{base['version']}"
    rk = rk if rk in g else ("labels/roi_current" if "labels/roi_current" in g else None)
    roi = np.asarray(g[rk][:]).astype(bool) if rk else np.ones(labels.shape, bool)
    base_m = store.q1("SELECT metrics FROM measurements WHERE segmentation_id=? ORDER BY id DESC LIMIT 1", (base["id"],))
    thick = json.loads(base_m["metrics"]).get("config", {}).get("thickness_metrics", True) if base_m else True
    ctx.progress(0.3, "recomputing endpoints")
    vol = Volume(np.asarray(g["image"][:]), tuple(sc["spacing_um"]))
    met = defect_report_metrics(labels, roi, vol, thickness=thick)
    prev = json.loads(base_m["metrics"]) if base_m else {}
    record = {"metrics": met, "corrected_from": base["version"], "config": prev.get("config", {"thickness_metrics": thick}),
              "qc": prev.get("qc"), "plausibility": prev.get("plausibility"), "uncertainty": prev.get("uncertainty"),
              "roi": prev.get("roi"), "status": "corrected_unreviewed",
              # the method that produced the base labels: read-time support binding needs it (C3-PRD-01/-04)
              "segmentation": prev.get("segmentation")}
    if prev.get("measurement_support"):
        # support depends on image, ROI and config (not on the labels): carry it over and
        # rebuild the reported view of the recomputed metrics
        record["measurement_support"] = prev["measurement_support"]
        try:
            from ..advisor.integration import apply_support
            record["reported_metrics"], record["suppressed_metrics"] = apply_support(met, prev["measurement_support"])
        except ImportError:
            pass
    # data first, rows last (C2-PRD-10): the labels are written under a new unique key; the version, the
    # measurement, the per-version ROI mask and the audit events are then committed in ONE transaction.
    # Cancellation is honoured only up to here; any failure afterwards removes everything written.
    ctx.progress(0.6, "writing labels")
    key = f"seg_r{uuid.uuid4().hex[:12]}"
    written = [key]
    try:
        write_labels_zarr(sc["store_path"], key, labels)
        ctx.progress(0.9, "saving revision")          # last cancellation point
        with store.transaction():
            sid, v = store.save_segmentation(user, scan_id, "corrected", key, labels_hash(labels), method=base["method"],
                                             model_name=base["model_name"], model_sha256=base["model_sha256"],
                                             roi_id=base["roi_id"], parent_id=base["id"], edits=edits)
            written.append(f"roi_v{v}")
            write_labels_zarr(sc["store_path"], f"roi_v{v}", roi.astype(np.uint8))
            store.save_measurement(user, scan_id, sid, base["roi_id"], record, __version__)
            store.audit.record("segmentation.edit", user["id"], user["org_id"], "segmentation", sid,
                               {"scan": scan_id, "version": v, "base_version": base["version"], "reason": reason.strip(),
                                "voxel_count_change": changed, "operations": operations or {}})
    except BaseException:
        _remove_label_arrays(sc["store_path"], written)
        raise
    _progress_after_commit(ctx, 1.0, "saved")
    return {"segmentation_id": sid, "version": v, "voxel_count_change": changed, "class_volumes": met["class_volumes"]}


def _remove_label_arrays(store_path, names):
    import zarr
    try:
        g = zarr.open_group(str(store_path), mode="a")
        for n in names:
            if f"labels/{n}" in g:
                del g[f"labels/{n}"]
    except Exception:  # noqa: BLE001 - cleanup is best-effort; the database rows were rolled back
        pass


# ============================================================================ review / sign-off
# The report is a non-GLP vendor report: the approving signature is the customer's, not a GLP study director's
# (review CRO-13, C2-BIZ-06). The internal role id "study_director" is kept for existing projects.
SIGNATURE_ROLES = {"analyst": "Analyst", "reviewer": "Scientific reviewer",
                   "study_director": "Customer approver"}
# which signature roles a user role may sign as (the store's role is recorded with the signature)
ROLE_SIGNATURES = {"reviewer": ["reviewer"], "study_director": ["study_director", "reviewer"],
                   "admin": ["reviewer", "study_director"]}


def signature_roles_for(user: dict) -> list[str]:
    return ROLE_SIGNATURES.get((user or {}).get("role"), [])


def unreviewed_segmentations(project, study_id) -> list[int]:
    """Scan ids whose latest (reported) segmentation has no current approval."""
    store, user = project.store, project.require_user()
    out = []
    for m in store.latest_measurements(user, study_id):
        seg = store.q1("SELECT id, labels_sha256 FROM segmentations WHERE id=?", (m["segmentation_id"],))
        revs = store.reviews(user, "segmentation", seg["id"]) if seg else []
        last = revs[-1] if revs else None
        if not last or last["decision"] != "approved" or last.get("object_sha256") not in (None, seg["labels_sha256"]):
            out.append(m["scan_id"])
    return out


def sign_review(project, password: str, object_type: str, object_id: int, decision: str, meaning: str,
                comment: str = "", signature_role: str | None = None) -> int:
    """Electronic sign-off with re-authentication (same rules as the web API).

    ``signature_role`` (Scientific reviewer / Study director) is recorded with the signature and used
    for the report's signature rows. Approving a report is refused while any reported segmentation
    of the study is not approved; "needs changes" and "rejected" are always possible."""
    if not meaning or len(meaning.strip()) < 5:
        raise ValueError("State the meaning of the signature (at least 5 characters)")
    if getattr(project, "integrity_problems", None):
        raise PermissionError("Electronic signatures are disabled for this project: an integrity check at sign-in "
                              "failed (" + project.integrity_problems[0] + "). An administrator must investigate "
                              "before anything is signed.")
    user = project.require_user()
    project.store.require(user, "review")
    allowed = signature_roles_for(user)
    if signature_role is None:
        signature_role = allowed[0] if allowed else "reviewer"
    if signature_role not in allowed:
        raise PermissionError(f"Your role cannot sign as {SIGNATURE_ROLES.get(signature_role, signature_role)}")
    if object_type == "report" and decision == "approved":
        r = project.store.q1("SELECT study_id, created_by, org_id FROM reports WHERE id=?", (object_id,))
        if not r or int(r["org_id"]) != int(user["org_id"]):
            raise KeyError("report not found")
        if r["created_by"] == user["id"]:
            project.store.audit.record("review.self_approval_denied", user["id"], user["org_id"], "report", object_id)
            from ..study.db import SELF_APPROVAL_MESSAGES
            raise PermissionError(SELF_APPROVAL_MESSAGES["report"])
        # the PDF and its bundle must be exactly what was generated (C2-PRD-04/05); fails closed when a
        # file or the integrity record is missing
        from .report_integrity import review_status, verify_report
        bundle = verify_report(project, object_id, check_pdf=True)
        _check_report_duties(project, user, object_id, bundle, signature_role)
        pending = unreviewed_segmentations(project, r["study_id"])
        if pending:
            raise PermissionError(f"{len(pending)} reported segmentation(s) of this study are not approved yet. "
                                  "Approve the segmentations first (Review panel), or choose 'Request changes'.")
        if review_status(project, object_id, bundle) != "reviewed":
            raise PermissionError("This report was generated before all segmentations were approved and is marked "
                                  "UNREVIEWED. Generate a new report, then approve it (or request changes).")
    if not project.reauthenticate(password, object_type, object_id):
        raise PermissionError("Re-authentication failed: password incorrect (5 failed attempts lock the account "
                              "for 15 minutes)")
    rid = project.store.review(user, object_type, object_id, decision, meaning.strip(), comment)
    project.store.exec("INSERT OR REPLACE INTO desktop_review_meta(review_id, signature_role) VALUES (?,?)",
                       (rid, signature_role))
    project.store.audit.record("review.signature_role", user["id"], user["org_id"], object_type, object_id,
                               {"review_id": rid, "signature_role": SIGNATURE_ROLES.get(signature_role, signature_role),
                                "signature_role_key": signature_role})
    if object_type == "report":
        try:
            render_signed_report(project, object_id)
        except Exception as e:  # noqa: BLE001 - the signature is recorded; the signed copy can be re-rendered
            project.store.audit.record("report.signed_copy_failed", user["id"], user["org_id"], "report", object_id,
                                       {"error": f"{type(e).__name__}: {e}"})
    from .anchors import record_anchor
    record_anchor(project, f"review.{decision}")
    return rid


def _check_report_duties(project, user, report_id, bundle, signature_role):
    """Separation of duties for report approval (C2-PRD-06): nobody who authored a reported segmentation
    (or a version it derives from) or its ROI may approve, and each person approves a report at most
    once, so the reviewer and approver signature rows always carry two different people."""
    from .report_integrity import report_author_ids
    store = project.store
    if int(user["id"]) in report_author_ids(project, bundle):
        store.audit.record("review.self_approval_denied", user["id"], user["org_id"], "report", report_id,
                           {"reason": "author of a reported segmentation or ROI"})
        raise PermissionError("Separation of duties: you authored a segmentation or ROI included in this report, so "
                              "you cannot approve it. Another reviewer or the approver must sign.")
    for rv in store.reviews(user, "report", report_id):
        if int(rv["reviewer_id"]) == int(user["id"]) and rv["decision"] == "approved":
            prev = SIGNATURE_ROLES.get(signature_role_of(project, rv["id"]) or "", "a signer")
            store.audit.record("review.duplicate_approval_denied", user["id"], user["org_id"], "report", report_id,
                               {"previous_review": rv["id"], "requested_role": signature_role})
            raise PermissionError(f"You have already approved this report ({prev}). The second signature must come "
                                  "from a different person.")


def signature_role_of(project, review_id) -> str | None:
    r = project.store.q1("SELECT signature_role FROM desktop_review_meta WHERE review_id=?", (review_id,))
    return r["signature_role"] if r else None


# ============================================================================ ROI review
def roi_mask_key(group, seg: dict | None) -> str | None:
    """Zarr key of the analysis ROI mask used by ``seg`` (per-version, else the current one)."""
    if seg is not None and f"labels/roi_v{seg['version']}" in group:
        return f"labels/roi_v{seg['version']}"
    return "labels/roi_current" if "labels/roi_current" in group else None


def roi_state(project, roi_id) -> dict:
    """ROI definition, whether automatic detection asked for review, and its acceptance state."""
    store, user = project.store, project.require_user()
    if roi_id is None:
        return {"roi": None, "requires_review": False, "accepted": False, "review": None, "status": "no ROI"}
    r = store.q1("SELECT r.*, s.org_id FROM rois r JOIN scans s ON r.scan_id=s.id WHERE r.id=?", (roi_id,))
    if not r or int(r["org_id"]) != int(user["org_id"]):
        return {"roi": None, "requires_review": False, "accepted": False, "review": None, "status": "no ROI"}
    d = json.loads(r["definition"] or "{}")
    req = bool((d.get("diagnostics") or {}).get("requires_review"))
    revs = store.reviews(user, "roi", roi_id)
    last = revs[-1] if revs else None
    accepted = bool(last and last["decision"] == "approved" and last.get("object_sha256") in (None, r["def_sha256"]))
    manual = "manual" in str(r["method"] or "")
    if accepted:
        status = "accepted"
    elif last and last["decision"] != "approved":
        status = last["decision"]
    elif req or manual:
        # a manual ROI is accepted by someone other than its creator, like a flagged automatic one (C2-PRD-17)
        status = "awaiting acceptance"
    else:
        status = "not reviewed"
    return {"roi": r, "definition": d, "requires_review": req, "accepted": accepted, "review": last,
            "manual": manual, "status": status, "manual_pending": bool(manual and not accepted)}


def measurement_support_for(project, metrics: dict, roi_id=None) -> dict:
    """Desktop support status of a stored measurement, honouring an accepted ROI."""
    from .support import measurement_support
    rs = roi_state(project, roi_id) if roi_id is not None else {}
    return measurement_support(metrics, roi_accepted=bool(rs.get("accepted")),
                               manual_roi_pending=bool(rs.get("manual_pending")))


# ============================================================================ revision details
def version_detail(project, segmentation_id: int) -> dict:
    """What changed in a segmentation version: parent, editor, reason, voxel and volume change per
    class, and every endpoint before -> after (not supported endpoints never show a number)."""
    from .support import ENDPOINTS, endpoint_value
    store, user = project.store, project.require_user()
    seg = store.q1("SELECT * FROM segmentations WHERE id=?", (segmentation_id,))
    if not seg:
        raise KeyError("segmentation not found")
    sc = store.scan(user, seg["scan_id"])
    edits = json.loads(seg["edits"] or "{}")
    parent = store.q1("SELECT * FROM segmentations WHERE id=?", (seg["parent_id"],)) if seg["parent_id"] else None
    author = store.q1("SELECT username, full_name, role FROM users WHERE id=?", (seg["created_by"],)) or {}
    vox_mm3 = float(np.prod(sc["spacing_um"])) / 1e9
    change = edits.get("voxel_count_change") or {}
    classes = [{"class": k.replace("_", " "), "voxels": int(v), "mm3": int(v) * vox_mm3} for k, v in change.items()]

    def meas(sid):
        m = store.q1("SELECT metrics, roi_id FROM measurements WHERE segmentation_id=? ORDER BY id DESC LIMIT 1", (sid,))
        return (json.loads(m["metrics"]), m["roi_id"]) if m else (None, None)

    after, roi_a = meas(seg["id"])
    before, roi_b = meas(parent["id"]) if parent else (None, None)
    sup_a = measurement_support_for(project, after, roi_a) if after else None
    sup_b = measurement_support_for(project, before, roi_b) if before else None
    eps = []
    for key, label, unit, _path, _scale in ENDPOINTS:
        va, sa, ra = endpoint_value(after, sup_a, key) if after else (None, "not analysed", ["no measurement"])
        vb, sb, rb = endpoint_value(before, sup_b, key) if before else (None, "not analysed", ["no parent version"])
        eps.append({"key": key, "label": label, "unit": unit, "before": vb, "before_status": sb, "after": va,
                    "after_status": sa, "reasons": ra})
    return {"segmentation": seg, "version": seg["version"], "kind": seg["kind"],
            "parent_version": parent["version"] if parent else None, "parent_id": parent["id"] if parent else None,
            "author": author.get("full_name") or author.get("username") or str(seg["created_by"]),
            "author_role": author.get("role"), "created": seg["created"], "reason": edits.get("reason") or "",
            "operations": edits.get("operations") or {}, "classes": classes, "endpoints": eps,
            "method": segmentation_method_info(seg, after)}


# ============================================================================ reports
def _set_path(d: dict, path: str, value):
    cur = d
    parts = path.split(".")
    for k in parts[:-1]:
        nxt = cur.get(k)
        if not isinstance(nxt, dict):
            return
        cur = nxt
    if parts[-1] in cur:
        cur[parts[-1]] = value


def _enforce_support(project, bundle: dict, meas_rows: list[dict]):
    """Apply the desktop support rule to the report bundle: an endpoint that is *not supported*
    (desktop rule: uncertain fraction, missing thickness, no-graft, advisor) is reported without a
    number, with its reason, exactly as in the Results table."""
    from .support import ENDPOINTS, FLAGGED, NO_NUMBER, NOT_ASSESSED
    by_path = {path: (key, label) for key, label, _u, path, _s in ENDPOINTS}
    for spec, m in _specimen_rows(bundle, meas_rows):
        sup = measurement_support_for(project, m["metrics"], m["roi_id"])
        sup_paths = {d.get("metric") for d in spec.get("suppressed_metrics") or []}
        for path, (key, label) in by_path.items():
            e = sup["endpoints"][key]
            # exports carry the status the analyst saw in Results (cycle-3 review C3-PRD-08)
            if e["status"] == FLAGGED:
                spec.setdefault("metric_status", {})[path] = {"status": "flagged",
                                                              "reasons": list(e.get("reasons") or [])}
            if e["status"] not in NO_NUMBER:
                continue
            spec.setdefault("metric_status", {})[path] = {
                "status": "not_assessed" if e["status"] == NOT_ASSESSED else "not_supported",
                "reasons": list(e.get("reasons") or [])}
            _set_path(spec["metrics"], path, None)
            if key == "mineralized_fraction":
                _set_path(spec["metrics"], "class_volumes.mineral_volume_mm3", None)
            if path not in sup_paths:
                reason = "; ".join(e["reasons"]) or e["status"]
                status = "not_assessed" if e["status"] == NOT_ASSESSED else "not_supported"
                spec.setdefault("suppressed_metrics", []).append({"metric": path, "reason": reason})
                spec.setdefault("measurement_support", {})[label] = {"status": status, "reason": reason,
                                                                      "conditions": []}


def _specimen_rows(bundle: dict, meas_rows: list[dict]):
    """Pair each report specimen with ITS measurement row by stable keys (scan id, segmentation id),
    never by list position (C2-PRD-01). A specimen without a matching row stops the report."""
    by_key = {(int(m["scan_id"]), int(m["segmentation_id"])): m for m in meas_rows if m.get("segmentation_id") is not None}
    for spec in bundle["specimens"]:
        try:
            key = (int(spec["scan_id"]), int(spec["segmentation_id"]))
        except (KeyError, TypeError, ValueError) as e:
            raise RuntimeError("report specimen without scan/segmentation id; cannot attribute its data") from e
        m = by_key.get(key)
        if m is None:
            raise RuntimeError(f"report specimen for scan {key[0]} has no matching measurement in the snapshot")
        yield spec, m


def _blind_bundle(project, bundle: dict, meas_rows: list[dict]):
    """Replace identity (animal IDs, file names, group allocation, acquisition metadata, database
    IDs) with the study's blinded codes. Figures are re-rendered with the blinded code as title."""
    from .blinding import Masker
    masker = Masker(project)
    store, user = project.store, project.require_user()
    bundle["study"]["blinded"] = True
    bundle["title"] = bundle["title"] + " (blinded)"
    for spec, m in _specimen_rows(bundle, meas_rows):
        sc = store.scan(user, m["scan_id"])
        scode = project.scan_code(sc["id"], sc["study_id"])
        acode = project.animal_code(sc["specimen_id"], sc["study_id"]) if sc["specimen_id"] else scode
        spec["specimen_id"] = acode
        spec["animal_id"] = acode
        spec["group"] = MASK_GROUP
        # the source-file hash identifies the file (C2-PRD-14); the content hash stays in the audit trail
        spec["scan"] = {**spec.get("scan", {}), "source": scode, "acquisition": {}, "sha256": MASK_GROUP}
        spec.pop("truth", None)
        spec["figure_title"] = scode
    ex = []
    for e in bundle.get("audit_excerpt") or []:
        me = masker.event(e)
        if me.get("object_type") in ("scan", "specimen", "group"):
            me["object_id"] = me["object_label"]
        ex.append(me)
    bundle["audit_excerpt"] = ex


def _render_figures(project, bundle: dict, blinded: bool, ctx=None):
    """Render one figure per specimen from ITS segmentation and per-version ROI (joined by key). Blinded
    reports get randomly named figures titled with the scan code; no unblinded figure is written for
    them (C2-PRD-14)."""
    import zarr
    from ..report.defectfill import _status
    from ..report.figures import refused_classes, specimen_panel
    store, user = project.store, project.require_user()
    figdir = store.data_dir / f"org{user['org_id']}" / "reports" / "fig"
    figdir.mkdir(parents=True, exist_ok=True)
    n = len(bundle["specimens"])
    for i, spec in enumerate(bundle["specimens"]):
        if ctx is not None:
            ctx.progress(0.6 + 0.2 * i / max(1, n), f"figure {i + 1}/{n}")
        spec["figure"] = None
        try:
            sc = store.scan(user, spec["scan_id"])
            seg = store.q1("SELECT id, labels_key, version FROM segmentations WHERE id=?", (spec["segmentation_id"],))
            g = zarr.open_group(sc["store_path"], mode="r")
            rk = roi_mask_key(g, seg)
            roi = np.asarray(g[rk][:]).astype(bool) if rk else None
            if blinded:
                fig, title = figdir / f"blinded_{uuid.uuid4().hex[:12]}.png", spec.get("figure_title") or "(blinded)"
            else:
                fig, title = figdir / f"scan{sc['id']}_seg{seg['id']}.png", f"scan {sc['id']}"
            grey = refused_classes(_status(spec, "class_volumes.new_bone_volume_mm3"),
                                   _status(spec, "class_volumes.residual_graft_volume_mm3"))
            specimen_panel(np.asarray(g["image"][:]), np.asarray(g[f"labels/{seg['labels_key']}"][:]), roi,
                           sc["spacing_um"], str(fig), title=title, grey_classes=grey)
            spec["figure"] = str(fig)
        except Exception:  # noqa: BLE001 - a missing figure is shown as such; never an unblinded one
            spec["figure"] = None
        spec.pop("figure_title", None)


MASK_GROUP = "(blinded)"


def _report_signature_rows(project, report_id: int, bundle: dict) -> list[dict]:
    """Signature rows of a report: the author (Analyst), segmentation approvals (Scientific reviewer)
    and every recorded decision on the report itself, with the signer's chosen signature role."""
    store, user = project.store, project.require_user()
    rep = store.q1("SELECT created_by, created FROM reports WHERE id=?", (report_id,))
    rows = []
    if rep:
        a = store.q1("SELECT username, full_name, role FROM users WHERE id=?", (rep["created_by"],)) or {}
        rows.append({"role": "Analyst", "name": a.get("full_name") or a.get("username", ""),
                     "meaning": "Prepared the analysis and generated this report (author)", "decision": "authored",
                     "time": rep["created"]})
    rows += [r for r in bundle.get("segmentation_reviewers", bundle.get("reviewers", [])) if r.get("role") != "Analyst"][:6]
    from .report_integrity import audited_signature_roles
    audited = audited_signature_roles(store, report_id)
    for rv in store.reviews(user, "report", report_id):
        # the signature role recorded in the hash-chained audit trail wins over the editable table (C2-PRD-09)
        sr = audited.get(int(rv["id"])) or signature_role_of(project, rv["id"])
        if sr is None:
            ru = store.q1("SELECT role FROM users WHERE id=?", (rv["reviewer_id"],)) or {}
            sr = "study_director" if ru.get("role") == "study_director" else "reviewer"
        rows.append({"role": SIGNATURE_ROLES.get(sr, sr), "name": rv["full_name"] or rv["username"],
                     "meaning": rv["meaning"], "decision": rv["decision"], "time": rv["created"]})
    return rows


def _bundle_path(project, report_id: int) -> Path:
    u = project.require_user()
    return project.store.data_dir / f"org{u['org_id']}" / "reports" / f"report{report_id}_bundle.json"


def generate_report(project, study_id: int, watermark: str | None = None, ctx=None, blinded: bool = False) -> dict:
    """Build the DefectFill PDF + CSV for a study (as the web API's report job, plus an optional
    watermark for evaluation/test licences).

    Desktop rules applied to the bundle before rendering: not-supported endpoints carry no number
    (with the reason), signature rows are filled from recorded approvals, and ``blinded`` reports
    replace identity with the study's blinded codes."""
    from ..api.bundle import bundle_from_store
    from ..report import build_pdf
    from ..study.jobs import JobCancelled
    from .report_integrity import sha256_bytes
    ctx = ctx or NullContext()
    store, user = project.store, project.require_user()
    st = store.study(user, study_id)
    store.require(user, "read", st["org_id"])
    # study-level blinding: users who may not unblind always get a blinded report (C2-PRD-03)
    blinded = bool(blinded or project.study_forces_blinding(study_id))
    # ONE read snapshot for the bundle, the measurement rows, the support rule and the blinding codes:
    # an analysis finishing meanwhile cannot mix two states into one report (C2-PRD-01)
    with store.snapshot():
        meas_rows = store.latest_measurements(user, study_id)
        bundle = bundle_from_store(store, user, study_id, ctx, measurements=meas_rows, figures=False)
        if not bundle["specimens"]:
            raise ValueError("This study has no analysed scans yet; run the analysis first")
        _enforce_support(project, bundle, meas_rows)
        if blinded:
            _blind_bundle(project, bundle, meas_rows)
    _render_figures(project, bundle, blinded, ctx)
    bundle["segmentation_reviewers"] = list(bundle.get("reviewers", []))
    out = store.data_dir / f"org{user['org_id']}" / "reports"
    out.mkdir(parents=True, exist_ok=True)
    unblinded = int(bool(st["blinded"]) and store.can(user, "unblind") and not blinded)
    ctx.progress(0.85, "rendering PDF")      # last cancellation point: no row exists yet
    rid = store.exec("INSERT INTO reports(org_id,study_id,status,created_by,created,unblinded) VALUES (?,?,?,?,datetime('now'),?)",
                     (user["org_id"], study_id, "building", user["id"], unblinded))
    pdf, csvp = out / f"report{rid}.pdf", out / f"report{rid}.csv"
    bp = _bundle_path(project, rid)
    try:
        bundle["reviewers"] = _report_signature_rows(project, rid, bundle)
        bundle["_watermark"] = watermark
        # the audit chain head at generation is printed on the report: a copy held by others is an anchor the
        # project's users cannot change (C3-PRD-03)
        bundle["audit_anchor"] = store.audit.anchor()
        r = build_pdf(bundle, pdf, csvp, watermark=watermark)
        # integrity record (C2-PRD-04/05): hash of the exact bundle bytes, stored with the review status
        data = json.dumps(bundle, default=str).encode("utf-8")
        bundle_sha = sha256_bytes(data)
        bp.write_bytes(data)
        with store.transaction():
            store.exec("UPDATE reports SET pdf_path=?, csv_path=?, sha256=?, status='ready' WHERE id=?",
                       (str(pdf), str(csvp), r["pdf_sha256"], rid))
            store.exec("INSERT OR REPLACE INTO desktop_report_meta(report_id, blinded, bundle_path, bundle_sha256, "
                       "review_status) VALUES (?,?,?,?,?)",
                       (rid, int(bool(blinded)), str(bp), bundle_sha, bundle.get("review_status")))
            store.audit.record("report.generate", user["id"], user["org_id"], "report", rid,
                               {"study": study_id, "sha256": r["pdf_sha256"], "bundle_sha256": bundle_sha,
                                "review_status": bundle.get("review_status"), "watermark": watermark or "",
                                "blinded": bool(blinded)})
    except BaseException as e:
        # nothing half-built remains: a cancelled report disappears, a failed one is marked failed (C2-PRD-10)
        for f in (pdf, csvp, bp):
            try:
                Path(f).unlink(missing_ok=True)
            except OSError:
                pass
        if isinstance(e, JobCancelled):
            store.exec("DELETE FROM reports WHERE id=?", (rid,))
            store.audit.record("report.cancelled", user["id"], user["org_id"], "report", rid, {"study": study_id})
        else:
            store.exec("UPDATE reports SET status='failed' WHERE id=?", (rid,))
        raise
    from .anchors import record_anchor
    record_anchor(project, "report.generate")
    _progress_after_commit(ctx, 1.0, "done")
    return {"report_id": rid, "pdf": str(pdf), "csv": str(csvp), "sha256": r["pdf_sha256"], "blinded": bool(blinded)}


def report_meta(project, report_id: int) -> dict:
    r = project.store.q1("SELECT * FROM desktop_report_meta WHERE report_id=?", (report_id,))
    return r or {"report_id": report_id, "blinded": 0, "bundle_path": None, "signed_pdf": None, "signed_sha256": None}


def render_signed_report(project, report_id: int) -> dict | None:
    """Render the signed copy of a report: the same stored content with the signature rows filled
    from the recorded approvals (name, signature role, time, meaning) and a note naming the
    original PDF's SHA-256. The original PDF is never modified (its hash is what was signed).

    The bundle is re-hashed and compared with the hash recorded at generation (database and audit
    trail) before anything is rendered; a mismatch raises ``ReportIntegrityError`` (C2-PRD-04)."""
    from ..report import build_pdf
    from .report_integrity import verify_report
    store, user = project.store, project.require_user()
    rep = store.q1("SELECT * FROM reports WHERE id=?", (report_id,))
    if not rep:
        return None
    bundle = verify_report(project, report_id, check_pdf=True)
    bundle["reviewers"] = _report_signature_rows(project, report_id, bundle)
    bundle["signature_note"] = (f"Signed copy of report {report_id}. Signatures apply to the original report PDF "
                                f"(SHA-256 {rep['sha256']}); each is recorded with its meaning in the hash-chained "
                                "audit trail.")
    out = Path(rep["pdf_path"]).with_name(f"report{report_id}_signed.pdf")
    r = build_pdf(bundle, out, None, watermark=bundle.get("_watermark"))
    store.exec("UPDATE desktop_report_meta SET signed_pdf=?, signed_sha256=? WHERE report_id=?",
               (str(out), r["pdf_sha256"], report_id))
    store.audit.record("report.signed_copy", user["id"], user["org_id"], "report", report_id,
                       {"sha256": r["pdf_sha256"], "original_sha256": rep["sha256"]})
    return {"pdf": str(out), "sha256": r["pdf_sha256"]}


def unblind_study(project, password: str, study_id: int, reason: str) -> None:
    """Unblind a study for everyone: a signed action of a study director or administrator (permission
    ``unblind``), with re-authentication and a stated reason, recorded in the audit trail (C2-PRD-03).
    Reviewers and analysts cannot switch blinding off."""
    user = project.require_user()
    st = project.store.study(user, study_id)
    project.store.require(user, "unblind", st["org_id"])
    if not st["blinded"]:
        raise ValueError("This study is not blinded")
    if not reason or len(reason.strip()) < 5:
        raise ValueError("State the reason for unblinding (at least 5 characters)")
    if not project.reauthenticate(password, "study", study_id):
        raise PermissionError("Re-authentication failed: password incorrect (5 failed attempts lock the account "
                              "for 15 minutes)")
    project.store.unblind(user, study_id, reason.strip(),
                          {"signed": True, "signer": user["username"], "signer_role": user["role"],
                           "meaning": "I authorise unblinding of this study for all users"})


def study_has_analysis(project, study_id) -> bool:
    return bool(project.store.latest_measurements(project.require_user(), study_id))


def list_reports(project, study_id) -> list[dict]:
    user = project.require_user()
    project.store.study(user, study_id)
    return project.store.q("SELECT r.id, r.status, r.created, r.created_by, r.sha256, r.pdf_path, r.csv_path, r.unblinded, "
                           "COALESCE(m.blinded, 0) AS blinded, m.signed_pdf FROM reports r "
                           "LEFT JOIN desktop_report_meta m ON m.report_id=r.id "
                           "WHERE r.study_id=? AND r.org_id=? ORDER BY r.id DESC", (study_id, user["org_id"]))


def export_report(project, report_id: int, dest_dir, kinds=("pdf", "csv")) -> list[str]:
    store, user = project.store, project.require_user()
    r = store.q1("SELECT * FROM reports WHERE id=?", (report_id,))
    if not r:
        raise KeyError("report not found")
    store.require(user, "read", r["org_id"])
    if r.get("unblinded") and not store.can(user, "unblind"):
        store.audit.record("report.blinded_download_denied", user["id"], user["org_id"], "report", report_id)
        raise PermissionError("This report contains unblinded group allocation")
    if not report_meta(project, report_id).get("blinded") and project.study_forces_blinding(r["study_id"]):
        # study-level blinding (C2-PRD-03): an identifying report of a blinded study stays inside the project
        store.audit.record("report.blinded_download_denied", user["id"], user["org_id"], "report", report_id,
                           {"reason": "blinded study, report not blinded"})
        raise PermissionError("This study is blinded and this report shows animal IDs and file names. Generate a "
                              "blinded report to export, or ask the study director to unblind the study.")
    out = []
    for k in kinds:
        src = r["pdf_path"] if k == "pdf" else r["csv_path"]
        if src and Path(src).exists():
            d = Path(dest_dir) / f"defectfill_report_{report_id}.{k}"
            shutil.copyfile(src, d)
            out.append(str(d))
    signed = report_meta(project, report_id).get("signed_pdf")
    if "pdf" in kinds and signed and Path(signed).exists():
        d = Path(dest_dir) / f"defectfill_report_{report_id}_signed.pdf"
        shutil.copyfile(signed, d)
        out.append(str(d))
    store.audit.record("report.export", user["id"], user["org_id"], "report", report_id, {"files": out})
    return out


# ============================================================================ audit export
def export_audit(project, path, blinded: bool = False) -> dict:
    """Export the audit trail (CSV or JSON by file extension) with the chain-verification result.

    Requires the reviewer, study director or administrator role (as viewing the audit trail).
    In blinded mode identifying details are masked. The export itself is an audit event."""
    import csv
    store, user = project.store, project.require_user()
    if not (store.can(user, "review") or store.can(user, "manage_users")):
        store.audit.record("authz.denied", user["id"], user["org_id"], details={"perm": "audit.export"})
        raise PermissionError("Exporting the audit trail requires the reviewer, study director or administrator role")
    blinded = bool(blinded or project.blinding_forced())      # study-level blinding (C2-PRD-03)
    ver = store.audit.verify_chain()
    events = store.audit.events(org_id=None, limit=10_000_000)     # a project is one organisation: whole chain
    events = sorted(events, key=lambda e: int(e["seq"]))
    # org_id and prev_hash are inputs of row_hash: exported so that every row can be re-verified (D-4 / C2-PRD-16)
    prev = {int(r["seq"]): r["prev_hash"] for r in store.q("SELECT seq, prev_hash FROM audit_log")}
    for e in events:
        e["prev_hash"] = prev.get(int(e["seq"]), "")
    users = {str(u["id"]): u["username"] for u in store.q("SELECT id, username FROM users")}
    n_masked = 0
    if blinded:
        from .blinding import Masker
        mk = Masker(project)
        masked = []
        for e in events:
            me = mk.event(e)
            me["masked"] = (me.get("details") != e.get("details") or str(me.get("object_id")) != str(e.get("object_id")))
            n_masked += bool(me["masked"])
            masked.append(me)
        events = masked
    path = Path(path)
    from ..study.db import now
    head = {"exported_by": user["username"], "exported_utc": now(), "blinded": bool(blinded),
            "chain_verification": {"ok": bool(ver.get("ok")), "events_verified": ver.get("n"),
                                   "head_hash": ver.get("head"), "first_bad_seq": ver.get("first_bad_seq"),
                                   "reason": ver.get("reason")},
            "n_events_exported": len(events)}
    if blinded:
        head["masked_rows"] = n_masked
        head["masking_note"] = ("blinded export: rows marked masked=true had identifying content replaced; their "
                                "row_hash is not reproducible from the masked content (verify with an unblinded export)")
    if path.suffix.lower() == ".json":
        path.write_text(json.dumps({**head, "events": [{**e, "username": users.get(str(e.get("user_id")), "")}
                                                       for e in events]}, indent=1, default=str), encoding="utf-8")
    else:
        with open(path, "w", newline="", encoding="utf-8") as f:
            f.write(f"# OsteoQuant audit trail export; chain verification: "
                    f"{'OK' if ver.get('ok') else 'BROKEN at event ' + str(ver.get('first_bad_seq'))}; "
                    f"events verified: {ver.get('n')}; head hash: {ver.get('head') or '-'}; "
                    f"exported by {user['username']} at {head['exported_utc']}"
                    + (f"; blinded: {n_masked} masked rows (masked=1) cannot be re-verified from this file"
                       if blinded else "") + "\n")
            w = csv.writer(f)
            # details are written in the canonical form hashed by the audit log, so rows re-verify
            w.writerow(["seq", "ts_utc", "user_id", "username", "org_id", "action", "object_type", "object_id",
                        "details", "prev_hash", "row_hash"] + (["masked"] if blinded else []))
            for e in events:
                w.writerow([e["seq"], e["ts"], e.get("user_id") or "", users.get(str(e.get("user_id")), ""),
                            e.get("org_id") or "", e["action"], e.get("object_type") or "",
                            (e.get("object_label") if blinded else None) or e.get("object_id") or "",
                            json.dumps(e.get("details") or {}, sort_keys=True, separators=(",", ":"), default=str),
                            e.get("prev_hash", ""), e["row_hash"]] + ([int(bool(e.get("masked")))] if blinded else []))
    file_sha = hashlib.sha256(path.read_bytes()).hexdigest()    # write, hash, then record (C2-PRD-16)
    store.audit.record("audit.export", user["id"], user["org_id"],
                       details={"path": str(path), "sha256": file_sha, "events": len(events),
                                "chain_ok": bool(ver.get("ok")), "blinded": bool(blinded)})
    from .anchors import record_anchor
    record_anchor(project, "audit.export")
    return {"path": str(path), "events": len(events), "verification": head["chain_verification"], "sha256": file_sha}


# ============================================================================ label loading (worker thread)
def load_scan_layers(store_path: str, seg: dict | None, parent_key: str | None = None) -> dict:
    """Load the label volume, the analysis ROI mask and (optionally) the parent version's labels.
    Runs on a worker thread; returns plain arrays."""
    import zarr
    g = zarr.open_group(str(store_path), mode="r")
    out = {"labels": None, "roi": None, "parent": None}
    if seg and seg.get("labels_key") and f"labels/{seg['labels_key']}" in g:
        out["labels"] = np.ascontiguousarray(np.asarray(g[f"labels/{seg['labels_key']}"][:]), dtype=np.uint8)
        rk = roi_mask_key(g, seg)
        if rk:
            out["roi"] = np.asarray(g[rk][:]).astype(bool)
    if parent_key and f"labels/{parent_key}" in g:
        out["parent"] = np.ascontiguousarray(np.asarray(g[f"labels/{parent_key}"][:]), dtype=np.uint8)
    return out
