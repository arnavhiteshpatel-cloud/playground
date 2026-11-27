"""Volume readers for scientific imaging formats.

Every reader returns ``(Volume, IngestReport)``. The IngestReport records what was read,
which metadata were found vs. assumed, file hashes and any warnings — this is the
provenance record stored with each scan.

Large volumes: readers accept ``zrange=(z0, z1)`` and ``step`` (integer stride applied in all
three axes, i.e. nearest-neighbour decimation — *not* a substitute for proper resampling; it is
used for previews and memory-bounded experiments, and the resulting spacing is scaled
accordingly and recorded in the report).
"""
from __future__ import annotations

import hashlib
import os
import re
import struct
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

from ..volume import Volume

READER_VERSION = "0.1.0"


@dataclass
class IngestReport:
    source: str
    format: str
    reader_version: str = READER_VERSION
    files: list[dict] = field(default_factory=list)     # [{"path","sha256","bytes"}]
    metadata_found: dict[str, Any] = field(default_factory=dict)
    metadata_assumed: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    missing_slices: list[int] = field(default_factory=list)
    decimation_step: int = 1
    zrange: tuple[int, int] | None = None

    def to_dict(self):
        return {k: (list(v) if isinstance(v, tuple) else v) for k, v in self.__dict__.items()}


# ----------------------------------------------------------------------------- hashing
def sha256_file(path: str | os.PathLike, chunk: int = 1 << 22) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def _file_record(p: Path, do_hash: bool = True) -> dict:
    return {"path": str(p), "bytes": p.stat().st_size, "sha256": sha256_file(p) if do_hash else None}


def _natural_key(s: str):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", s)]


# ----------------------------------------------------------------------------- dispatch
SUFFIX_FORMATS = {
    ".nii": "nifti", ".nii.gz": "nifti", ".nrrd": "nrrd", ".nhdr": "nrrd",
    ".ome.tif": "ome-tiff", ".ome.tiff": "ome-tiff", ".tif": "tiff", ".tiff": "tiff",
    ".zarr": "zarr", ".txm": "txm", ".txrm": "txm", ".dcm": "dicom", ".mha": "itk", ".mhd": "itk",
    ".npy": "npy",
}


def detect_format(path: str | os.PathLike) -> str:
    p = Path(path)
    name = p.name.lower()
    if p.is_dir():
        if (p / ".zgroup").exists() or (p / "zarr.json").exists() or name.endswith(".zarr"):
            return "zarr"
        files = [f for f in p.iterdir() if f.is_file() and not f.name.startswith(".")]
        exts = {f.suffix.lower() for f in files}
        if exts & {".tif", ".tiff"}:
            return "tiff-stack"
        if ".dcm" in exts or any(_looks_like_dicom(f) for f in files[:3]):
            return "dicom"
        if ".bmp" in exts or ".png" in exts:
            return "image-stack"
        raise ValueError(f"Cannot determine format of directory {p}")
    for suf in sorted(SUFFIX_FORMATS, key=len, reverse=True):
        if name.endswith(suf):
            return SUFFIX_FORMATS[suf]
    if _looks_like_dicom(p):
        return "dicom"
    raise ValueError(f"Unsupported file type: {p}")


def _looks_like_dicom(p: Path) -> bool:
    try:
        with open(p, "rb") as f:
            f.seek(128)
            return f.read(4) == b"DICM"
    except OSError:
        return False


class UnsafeInput(ValueError):
    pass


def check_safe_input(path) -> None:
    """Reject inputs that can make a reader open OTHER files (detached headers): MetaImage
    (.mhd ElementDataFile), detached NRRD (.nhdr or 'data file' field). Used for all uploads."""
    p = Path(path)
    files = [f for f in p.rglob("*") if f.is_file()] if p.is_dir() else [p]
    for f in files:
        n = f.name.lower()
        if n.endswith((".mhd", ".nhdr", ".raw", ".mha")):
            raise UnsafeInput(f"Detached-header/raw formats are not accepted for upload: {f.name}")
        if n.endswith(".nrrd"):
            import nrrd
            hdr = nrrd.read_header(str(f))
            if any(k.replace(" ", "").lower() == "datafile" for k in hdr):
                raise UnsafeInput("NRRD files that reference external data files are not accepted")


def read_volume(path, spacing_um=None, zrange=None, step: int = 1, do_hash: bool = True,
                safe: bool = False, **kw) -> tuple[Volume, IngestReport]:
    """Read any supported volume. ``spacing_um`` overrides/fills missing voxel size.
    ``safe=True`` (all untrusted uploads) rejects formats that can reference external files."""
    if safe:
        check_safe_input(path)
    fmt = detect_format(path)
    fn = {
        "tiff-stack": read_tiff_stack, "image-stack": read_tiff_stack, "tiff": read_tiff,
        "ome-tiff": read_tiff, "dicom": read_dicom_series, "nifti": read_nifti,
        "nrrd": read_nrrd, "zarr": read_zarr, "txm": read_txm, "itk": read_itk, "npy": read_npy,
    }[fmt]
    vol, rep = fn(path, zrange=zrange, step=step, do_hash=do_hash, **kw)
    if spacing_um is not None:
        sp = tuple(float(s) for s in (spacing_um if np.iterable(spacing_um) else [spacing_um] * 3))
        if "spacing_um" in rep.metadata_found and not np.allclose(rep.metadata_found["spacing_um"], sp):
            rep.warnings.append(
                f"User-supplied spacing {sp} differs from file metadata {rep.metadata_found['spacing_um']}; "
                "using user-supplied value.")
        vol = Volume(vol.data, tuple(s * step for s in sp), vol.origin, vol.direction, vol.meta)
        rep.metadata_assumed.pop("spacing_um", None)
        rep.metadata_found["spacing_um_user"] = list(sp)
    vol.meta["ingest"] = rep.to_dict()
    return vol, rep


def _apply_step_spacing(spacing, step):
    return tuple(float(s) * step for s in spacing)


# ----------------------------------------------------------------------------- TIFF
def _tiff_spacing(tf) -> tuple[dict, list[str]]:
    """Extract spacing from ImageJ or OME metadata or resolution tags (µm)."""
    found, warns = {}, []
    try:
        if tf.is_ome and tf.ome_metadata:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(tf.ome_metadata)
            for el in root.iter():
                if el.tag.endswith("Pixels"):
                    a = el.attrib
                    unit_scale = {"µm": 1.0, "um": 1.0, "nm": 1e-3, "mm": 1e3}
                    def g(k):
                        if k not in a:
                            return None
                        u = a.get(k + "Unit", "µm")
                        return float(a[k]) * unit_scale.get(u, 1.0)
                    sx, sy, sz = g("PhysicalSizeX"), g("PhysicalSizeY"), g("PhysicalSizeZ")
                    if sx and sy:
                        found["spacing_um"] = [sz or sx, sy, sx]
                        if not sz:
                            warns.append("OME PhysicalSizeZ missing; assumed equal to X")
                    break
        elif tf.is_imagej and tf.imagej_metadata:
            ij = tf.imagej_metadata
            page = tf.pages[0]
            xr = page.tags.get("XResolution")
            unit = ij.get("unit", "")
            scale = {"micron": 1.0, "um": 1.0, "\\u00B5m": 1.0, "µm": 1.0, "mm": 1000.0, "nm": 1e-3}.get(unit)
            if xr is not None and scale is not None:
                num, den = xr.value
                sx = den / num * scale if num else None
                sz = float(ij.get("spacing", sx or 1)) * scale
                if sx:
                    found["spacing_um"] = [sz, sx, sx]
    except Exception as e:  # pragma: no cover - metadata parse is best effort
        warns.append(f"TIFF metadata parse failed: {e}")
    return found, warns


def read_tiff(path, zrange=None, step=1, do_hash=True, **kw):
    import tifffile
    p = Path(path)
    rep = IngestReport(str(p), "ome-tiff" if ".ome." in p.name.lower() else "tiff")
    rep.files.append(_file_record(p, do_hash))
    with tifffile.TiffFile(p) as tf:
        found, warns = _tiff_spacing(tf)
        rep.metadata_found.update(found)
        rep.warnings += warns
        series = tf.series[0]
        arr = series.asarray(out="memmap") if series.dataoffset is not None else series.asarray()
    arr = np.asarray(arr)
    arr = np.squeeze(arr)
    if arr.ndim == 2:
        arr = arr[None]
    if arr.ndim != 3:
        raise ValueError(f"TIFF has {arr.ndim} dims after squeeze; expected 3 (multi-channel not supported here)")
    z0, z1 = zrange or (0, arr.shape[0])
    rep.zrange = (z0, z1)
    data = np.ascontiguousarray(arr[z0:z1:step, ::step, ::step])
    spacing = found.get("spacing_um")
    if spacing is None:
        spacing = [1.0, 1.0, 1.0]
        rep.metadata_assumed["spacing_um"] = spacing
        rep.warnings.append("No voxel spacing in TIFF metadata; assumed 1 µm. Supply spacing explicitly.")
    rep.decimation_step = step
    return Volume(data, _apply_step_spacing(spacing, step), meta={"format": rep.format}), rep


def read_tiff_stack(path, zrange=None, step=1, do_hash=True, pattern=None, **kw):
    """Folder of 2D slices (vendor reconstructions, e.g. Bruker *_rec00001234.bmp/.tif)."""
    import tifffile
    p = Path(path)
    rep = IngestReport(str(p), "tiff-stack")
    exts = {".tif", ".tiff", ".png", ".bmp"}
    files = sorted([f for f in p.iterdir() if f.suffix.lower() in exts and not f.name.startswith(".")],
                   key=lambda f: _natural_key(f.name))
    if pattern:
        files = [f for f in files if re.search(pattern, f.name)]
    if not files:
        raise ValueError(f"No image slices in {p}")
    # missing slice detection from trailing index in file names
    idx = []
    for f in files:
        m = re.findall(r"(\d+)", f.stem)
        idx.append(int(m[-1]) if m else None)
    if all(i is not None for i in idx) and len(idx) > 1:
        ids = np.array(idx)
        if len(np.unique(ids)) != len(ids):
            rep.warnings.append("Duplicate slice indices found in file names")
        full = set(range(ids.min(), ids.max() + 1))
        rep.missing_slices = sorted(full - set(ids.tolist()))
        if rep.missing_slices:
            rep.warnings.append(f"{len(rep.missing_slices)} slice indices missing from sequence "
                                f"(first: {rep.missing_slices[:5]})")
    z0, z1 = zrange or (0, len(files))
    rep.zrange = (z0, z1)
    sel = files[z0:z1:step]

    def load2d(f):
        if f.suffix.lower() in (".tif", ".tiff"):
            return tifffile.imread(f)
        from skimage import io as skio
        return skio.imread(f)

    first = np.asarray(load2d(sel[0]))
    if first.ndim == 3:  # RGB slice
        rep.warnings.append("RGB slices converted to luminance")
    shape2d = first.shape[:2]
    out = np.empty((len(sel), (shape2d[0] + step - 1) // step, (shape2d[1] + step - 1) // step),
                   dtype=first.dtype if first.ndim == 2 else np.float32)
    for k, f in enumerate(sel):
        a = np.asarray(load2d(f))
        if a.ndim == 3:
            a = a[..., :3].mean(-1)
        if a.shape[:2] != shape2d:
            rep.errors.append(f"Slice {f.name} has shape {a.shape}, expected {shape2d}")
            continue
        out[k] = a[::step, ::step]
    for f in sel if len(sel) <= 64 else []:
        rep.files.append(_file_record(f, do_hash))
    if len(sel) > 64:
        # hash a manifest of names+sizes plus every slice (streaming) for large stacks
        h = hashlib.sha256()
        for f in files:
            h.update(f.name.encode())
            if do_hash:
                h.update(sha256_file(f).encode())
        rep.files.append({"path": str(p), "bytes": sum(f.stat().st_size for f in files),
                          "sha256": h.hexdigest(), "n_files": len(files), "kind": "stack-manifest-hash"})
    # Bruker log file (if present) for spacing
    spacing = None
    for logf in list(p.glob("*.log"))[:1]:
        txt = logf.read_text(errors="ignore")
        m = re.search(r"Image Pixel Size \(um\)\s*=\s*([\d.]+)", txt)
        if m:
            s = float(m.group(1))
            spacing = [s, s, s]
            rep.metadata_found["spacing_um"] = spacing
            rep.metadata_found["vendor_log"] = logf.name
        for key in ("Source Voltage (kV)", "Source Current (uA)", "Filter", "Scanner", "Exposure (ms)",
                    "Rotation Step (deg)", "Frame Averaging", "Smoothing", "Ring Artifact Correction",
                    "Beam Hardening Correction (%)", "Reconstruction Program"):
            m2 = re.search(re.escape(key) + r"\s*=\s*(.+)", txt)
            if m2:
                rep.metadata_found[key] = m2.group(1).strip()
    if spacing is None:
        spacing = [1.0, 1.0, 1.0]
        rep.metadata_assumed["spacing_um"] = spacing
        rep.warnings.append("No voxel spacing found (no vendor log); assumed 1 µm. Supply spacing explicitly.")
    rep.decimation_step = step
    return Volume(out, _apply_step_spacing(spacing, step), meta={"format": "tiff-stack"}), rep


# ----------------------------------------------------------------------------- DICOM
def read_dicom_series(path, zrange=None, step=1, do_hash=True, **kw):
    import pydicom
    p = Path(path)
    rep = IngestReport(str(p), "dicom")
    files = [f for f in (p.iterdir() if p.is_dir() else [p]) if f.is_file()]
    dss = []
    for f in files:
        try:
            ds = pydicom.dcmread(f, stop_before_pixels=False)
            if "PixelData" in ds:
                dss.append((f, ds))
        except Exception:
            continue
    if not dss:
        raise ValueError("No DICOM images with pixel data found")
    series = {}
    for f, ds in dss:
        series.setdefault(getattr(ds, "SeriesInstanceUID", "unknown"), []).append((f, ds))
    if len(series) > 1:
        rep.warnings.append(f"{len(series)} series found; using the largest")
    f_ds = max(series.values(), key=len)
    ds0 = f_ds[0][1]
    # multi-frame
    if int(getattr(ds0, "NumberOfFrames", 1)) > 1 and len(f_ds) == 1:
        arr = ds0.pixel_array.astype(np.float32)
        ps = [float(v) for v in getattr(ds0, "PixelSpacing", [1, 1])]
        st = float(getattr(ds0, "SliceThickness", ps[0]) or ps[0])
        spacing_mm = [st, ps[0], ps[1]]
        rep.files.append(_file_record(f_ds[0][0], do_hash))
    else:
        iop = np.array(getattr(ds0, "ImageOrientationPatient", [1, 0, 0, 0, 1, 0]), dtype=float)
        normal = np.cross(iop[:3], iop[3:])
        def pos(ds):
            ipp = getattr(ds, "ImagePositionPatient", None)
            if ipp is not None:
                return float(np.dot(normal, np.array(ipp, dtype=float)))
            return float(getattr(ds, "InstanceNumber", 0))
        f_ds.sort(key=lambda t: pos(t[1]))
        positions = np.array([pos(ds) for _, ds in f_ds])
        d = np.diff(positions)
        if len(d):
            med = float(np.median(d))
            if med == 0:
                rep.errors.append("Duplicate slice positions")
            gaps = np.where(d > 1.5 * med)[0] if med > 0 else []
            for g in gaps:
                n_missing = int(round(d[g] / med)) - 1
                rep.missing_slices += list(range(g + 1, g + 1 + n_missing))
            if len(gaps):
                rep.warnings.append(f"Irregular slice spacing: {len(rep.missing_slices)} slice(s) appear missing")
            if med > 0 and np.std(d[d < 1.5 * med]) > 0.01 * med:
                rep.warnings.append("Slice spacing varies by >1%")
            sz = med if med > 0 else float(getattr(ds0, "SliceThickness", 1.0))
        else:
            sz = float(getattr(ds0, "SliceThickness", 1.0))
        ps = [float(v) for v in getattr(ds0, "PixelSpacing", [1, 1])]
        spacing_mm = [sz, ps[0], ps[1]]
        z0, z1 = zrange or (0, len(f_ds))
        rep.zrange = (z0, z1)
        sel = f_ds[z0:z1]
        slices = []
        for f, ds in sel:
            a = ds.pixel_array.astype(np.float32)
            slope = float(getattr(ds, "RescaleSlope", 1) or 1)
            inter = float(getattr(ds, "RescaleIntercept", 0) or 0)
            slices.append(a * slope + inter)
            if do_hash and len(sel) <= 2000:
                rep.files.append(_file_record(f, do_hash))
        arr = np.stack(slices)
        if hasattr(ds0, "RescaleType"):
            rep.metadata_found["RescaleType"] = str(ds0.RescaleType)
    if "PixelSpacing" not in ds0:
        rep.metadata_assumed["pixel_spacing"] = True
        rep.warnings.append("DICOM PixelSpacing absent; assumed 1 mm")
    spacing_um = [s * 1000.0 for s in spacing_mm]
    rep.metadata_found["spacing_um"] = spacing_um
    for tag in ("Manufacturer", "ManufacturerModelName", "KVP", "XRayTubeCurrent", "ExposureTime",
                "ConvolutionKernel", "Modality", "StudyDate", "PatientSpecies", "BodyPartExamined"):
        if hasattr(ds0, tag):
            rep.metadata_found[tag] = str(getattr(ds0, tag))
    arr = arr[:, ::step, ::step][::step] if step > 1 else arr
    rep.decimation_step = step
    return Volume(np.ascontiguousarray(arr), _apply_step_spacing(spacing_um, step),
                  meta={"format": "dicom", "intensity_unit": "rescaled"}), rep


# ----------------------------------------------------------------------------- NIfTI / NRRD / ITK
def read_nifti(path, zrange=None, step=1, do_hash=True, **kw):
    import nibabel as nib
    p = Path(path)
    rep = IngestReport(str(p), "nifti")
    rep.files.append(_file_record(p, do_hash))
    img = nib.load(str(p))
    arr = np.asanyarray(img.dataobj)
    if arr.ndim == 4 and arr.shape[3] == 1:
        arr = arr[..., 0]
    if arr.ndim != 3:
        raise ValueError(f"NIfTI with {arr.ndim} dims not supported")
    zooms = [float(z) for z in img.header.get_zooms()[:3]]
    unit = img.header.get_xyzt_units()[0] or "unknown"
    scale = {"mm": 1000.0, "micron": 1.0, "meter": 1e6}.get(unit)
    if scale is None:
        scale = 1000.0
        rep.metadata_assumed["spatial_unit"] = "mm"
        rep.warnings.append("NIfTI spatial unit unknown; assumed mm")
    rep.metadata_found["spatial_unit"] = unit
    arr = np.transpose(arr, (2, 1, 0))  # (x,y,z) -> (z,y,x)
    spacing = [zooms[2] * scale, zooms[1] * scale, zooms[0] * scale]
    rep.metadata_found["spacing_um"] = spacing
    rep.metadata_found["affine"] = img.affine.tolist()
    z0, z1 = zrange or (0, arr.shape[0])
    rep.zrange = (z0, z1)
    data = np.ascontiguousarray(arr[z0:z1:step, ::step, ::step])
    rep.decimation_step = step
    return Volume(data, _apply_step_spacing(spacing, step), meta={"format": "nifti"}), rep


def read_nrrd(path, zrange=None, step=1, do_hash=True, **kw):
    import nrrd
    p = Path(path)
    rep = IngestReport(str(p), "nrrd")
    rep.files.append(_file_record(p, do_hash))
    arr, hdr = nrrd.read(str(p), index_order="C")  # (z,y,x)
    if arr.ndim != 3:
        raise ValueError("Only 3D NRRD supported")
    sp = None
    if "space directions" in hdr and hdr["space directions"] is not None:
        sd = np.array(hdr["space directions"], dtype=float)  # rows per axis in F order (x,y,z)
        sp = list(np.linalg.norm(sd, axis=1))[::-1]
    elif "spacings" in hdr:
        sp = list(map(float, hdr["spacings"]))[::-1]
    units = hdr.get("space units") or hdr.get("units")
    scale = 1000.0
    if units and str(units[0]).lower() in ("um", "micron", "µm"):
        scale = 1.0
    elif not units:
        rep.metadata_assumed["spatial_unit"] = "mm"
        rep.warnings.append("NRRD space units missing; assumed mm")
    if sp is None:
        sp = [1.0, 1.0, 1.0]
        rep.metadata_assumed["spacing_um"] = sp
        rep.warnings.append("NRRD spacing missing; assumed 1")
        scale = 1.0
    spacing = [s * scale for s in sp]
    rep.metadata_found["spacing_um"] = spacing
    z0, z1 = zrange or (0, arr.shape[0])
    rep.zrange = (z0, z1)
    rep.decimation_step = step
    return Volume(np.ascontiguousarray(arr[z0:z1:step, ::step, ::step]),
                  _apply_step_spacing(spacing, step), meta={"format": "nrrd"}), rep


def read_itk(path, zrange=None, step=1, do_hash=True, **kw):
    import SimpleITK as sitk
    p = Path(path)
    rep = IngestReport(str(p), "itk")
    rep.files.append(_file_record(p, do_hash))
    img = sitk.ReadImage(str(p))
    arr = sitk.GetArrayFromImage(img)  # (z,y,x)
    sp = list(img.GetSpacing())[::-1]
    rep.metadata_found["spacing_raw"] = sp
    rep.metadata_assumed["spatial_unit"] = "mm"
    rep.warnings.append("MetaImage has no unit field; spacing interpreted as mm")
    spacing = [s * 1000.0 for s in sp]
    z0, z1 = zrange or (0, arr.shape[0])
    return Volume(np.ascontiguousarray(arr[z0:z1:step, ::step, ::step]),
                  _apply_step_spacing(spacing, step), meta={"format": "itk"}), rep


def read_npy(path, zrange=None, step=1, do_hash=True, **kw):
    p = Path(path)
    rep = IngestReport(str(p), "npy")
    rep.files.append(_file_record(p, do_hash))
    arr = np.load(p, mmap_mode="r")
    z0, z1 = zrange or (0, arr.shape[0])
    rep.metadata_assumed["spacing_um"] = [1.0, 1.0, 1.0]
    rep.warnings.append("NumPy arrays carry no spacing; assumed 1 µm")
    return Volume(np.ascontiguousarray(arr[z0:z1:step, ::step, ::step]), (step,) * 3,
                  meta={"format": "npy"}), rep


# ----------------------------------------------------------------------------- Zarr (internal)
def read_zarr(path, zrange=None, step=1, do_hash=False, **kw):
    import zarr
    p = Path(path)
    rep = IngestReport(str(p), "zarr")
    g = zarr.open_group(str(p), mode="r")
    a = g["image"]
    attrs = dict(g.attrs)
    spacing = attrs.get("spacing_um")
    if spacing is None:
        spacing = [1.0, 1.0, 1.0]
        rep.metadata_assumed["spacing_um"] = spacing
    else:
        rep.metadata_found["spacing_um"] = spacing
    z0, z1 = zrange or (0, a.shape[0])
    rep.zrange = (z0, z1)
    data = np.asarray(a[z0:z1:step, ::step, ::step])
    meta = attrs.get("meta", {})
    meta["format"] = "zarr"
    rep.decimation_step = step
    rep.files.append({"path": str(p), "sha256": attrs.get("content_sha256"), "kind": "zarr-store"})
    return Volume(data, _apply_step_spacing(spacing, step), tuple(attrs.get("origin_um", (0, 0, 0))),
                  meta=meta), rep


# ----------------------------------------------------------------------------- Zeiss TXM
_TXM_DTYPES = {5: np.uint16, 10: np.float32, 3: np.uint8, 6: np.int16}


def _ole_scalar(ole, name, fmt):
    if not ole.exists(name):
        return None
    b = ole.openstream(name).read()
    n = len(b) // struct.calcsize(fmt)
    vals = struct.unpack("<" + fmt * n, b[: n * struct.calcsize(fmt)])
    return vals[0] if n == 1 else vals


def txm_metadata(path) -> dict:
    import olefile
    with olefile.OleFileIO(str(path)) as ole:
        md = {
            "width": _ole_scalar(ole, "ImageInfo/ImageWidth", "I"),
            "height": _ole_scalar(ole, "ImageInfo/ImageHeight", "I"),
            "n_images": _ole_scalar(ole, "ImageInfo/NoOfImages", "I"),
            "data_type": _ole_scalar(ole, "ImageInfo/DataType", "I"),
            "pixel_size_um": _ole_scalar(ole, "ImageInfo/PixelSize", "f"),
            "voltage_kv": _ole_scalar(ole, "ImageInfo/XrayVoltage", "f"),
            "current_ua": _ole_scalar(ole, "ImageInfo/XrayCurrent", "f"),
            "optical_mag": _ole_scalar(ole, "ImageInfo/OpticalMagnification", "f"),
        }
        for k in ("voltage_kv", "current_ua", "optical_mag"):
            if isinstance(md[k], tuple):
                md[k] = md[k][0]
        streams = ["/".join(s) for s in ole.listdir()]
        md["n_streams"] = len(streams)
        md["has_recon_settings"] = any(s.startswith("ReconSettings") for s in streams)
        img_streams = [s for s in streams if re.match(r"ImageData\d+/Image\d+$", s)]
        md["n_image_streams"] = len(img_streams)
        for s in streams:
            if s.startswith("ReconSettings/") and len(md) < 60:
                try:
                    b = ole.openstream(s).read()
                    if len(b) == 4:
                        f = struct.unpack("<f", b)[0]
                        if f != 0 and abs(f) < 1e-30:  # integer field stored in 4 bytes
                            f = struct.unpack("<i", b)[0]
                        md["recon:" + s.split("/", 1)[1]] = f
                except Exception:
                    pass
    return md


def read_txm(path, zrange=None, step=1, do_hash=True, **kw):
    """Zeiss Xradia reconstructed volume (.txm, OLE2 compound file).

    Stream layout (as documented by open-source readers such as dxchange/olefile users):
    ``ImageInfo/*`` scalar metadata and one stream per slice in ``ImageData{k}/Image{i}``
    with 100 images per ``ImageData`` folder. Reading is slice-lazy, so memory is bounded
    by the selected ``zrange`` and ``step``.
    """
    import olefile
    p = Path(path)
    rep = IngestReport(str(p), "txm")
    rep.files.append(_file_record(p, do_hash))
    md = txm_metadata(p)
    rep.metadata_found.update({k: v for k, v in md.items() if v is not None})
    w, h, n = md["width"], md["height"], md["n_images"]
    dt = _TXM_DTYPES.get(md["data_type"])
    if dt is None:
        raise ValueError(f"Unsupported TXM DataType {md['data_type']}")
    if n is None or n == 0:
        n = md["n_image_streams"]
    if md["n_image_streams"] != n:
        rep.warnings.append(f"NoOfImages={n} but {md['n_image_streams']} image streams present")
    z0, z1 = zrange or (0, n)
    z1 = min(z1, n)
    rep.zrange = (z0, z1)
    zs = list(range(z0, z1, step))
    out = np.empty((len(zs), (h + step - 1) // step, (w + step - 1) // step), dtype=dt)
    with olefile.OleFileIO(str(p)) as ole:
        for k, z in enumerate(zs):
            i = z + 1
            name = f"ImageData{(i - 1) // 100 + 1}/Image{i}"
            if not ole.exists(name):
                rep.missing_slices.append(z)
                out[k] = 0
                continue
            b = ole.openstream(name).read()
            a = np.frombuffer(b, dtype=dt)
            if a.size != w * h:
                rep.errors.append(f"Slice {z}: {a.size} values, expected {w*h}")
                out[k] = 0
                continue
            out[k] = a.reshape(h, w)[::step, ::step]
    if rep.missing_slices:
        rep.warnings.append(f"{len(rep.missing_slices)} slice streams missing")
    px = md.get("pixel_size_um")
    if isinstance(px, tuple):
        px = px[0]
    if not px:
        px = 1.0
        rep.metadata_assumed["spacing_um"] = [1, 1, 1]
        rep.warnings.append("TXM PixelSize missing; assumed 1 µm")
    spacing = [float(px)] * 3
    rep.metadata_found["spacing_um"] = spacing
    rep.decimation_step = step
    meta = {"format": "txm", "scanner_vendor": "Zeiss Xradia",
            "voltage_kv": md.get("voltage_kv"), "current_ua": md.get("current_ua")}
    return Volume(out, _apply_step_spacing(spacing, step), meta=meta), rep
