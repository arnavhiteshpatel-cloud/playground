"""Volume writers and the internal chunked store (Zarr).

The internal store is a Zarr group::

    scan.zarr/
      image        (z,y,x) chunked, compressed (Zstd via zarr defaults)
      labels/<name>  optional label volumes (uint8)
      attrs: spacing_um, origin_um, meta, content_sha256, osteoquant_version

Chunking (64^3 by default) enables out-of-core processing: algorithms iterate over
chunks or slabs (see ``iter_slabs``) without loading the whole volume.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from .. import __version__
from ..volume import Volume


def _jsonable(o):
    if isinstance(o, dict):
        return {str(k): _jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_jsonable(v) for v in o]
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (str, int, float, bool)) or o is None:
        return o
    return str(o)


def write_zarr(vol: Volume, path, chunks=(64, 64, 64), labels: dict | None = None) -> str:
    import zarr
    p = Path(path)
    g = zarr.open_group(str(p), mode="w")
    ch = tuple(min(c, s) for c, s in zip(chunks, vol.shape))
    a = g.create_array("image", shape=vol.shape, chunks=ch, dtype=vol.data.dtype)
    for z in range(0, vol.shape[0], ch[0]):
        a[z:z + ch[0]] = vol.data[z:z + ch[0]]
    h = vol.content_hash()
    g.attrs.update({
        "spacing_um": list(vol.spacing), "origin_um": list(vol.origin),
        "meta": _jsonable(vol.meta), "content_sha256": h, "osteoquant_version": __version__,
    })
    for name, lab in (labels or {}).items():
        la = g.create_array(f"labels/{name}", shape=lab.shape, chunks=ch, dtype=np.uint8)
        la[:] = lab.astype(np.uint8)
    return h


def write_labels_zarr(path, name: str, labels: np.ndarray):
    import zarr
    g = zarr.open_group(str(path), mode="a")
    key = f"labels/{name}"
    if key in g:
        del g[key]
    ch = g["image"].chunks
    la = g.create_array(key, shape=labels.shape, chunks=ch, dtype=np.uint8)
    la[:] = labels.astype(np.uint8)


def read_labels_zarr(path, name: str) -> np.ndarray | None:
    import zarr
    g = zarr.open_group(str(path), mode="r")
    key = f"labels/{name}"
    return np.asarray(g[key][:]) if key in g else None


def iter_slabs(path, slab: int = 64, overlap: int = 0):
    """Yield (z0, z1, array) slabs from a Zarr store for out-of-core processing."""
    import zarr
    a = zarr.open_group(str(path), mode="r")["image"]
    n = a.shape[0]
    for z0 in range(0, n, slab):
        lo, hi = max(0, z0 - overlap), min(n, z0 + slab + overlap)
        yield z0, min(n, z0 + slab), np.asarray(a[lo:hi]), lo


def write_nifti(vol: Volume, path, labels=False):
    import nibabel as nib
    arr = np.transpose(vol.data, (2, 1, 0))
    sp_mm = [s / 1000.0 for s in vol.spacing[::-1]]
    aff = np.diag(sp_mm + [1.0])
    img = nib.Nifti1Image(arr.astype(np.uint8) if labels else arr, aff)
    img.header.set_xyzt_units("mm")
    nib.save(img, str(path))


def write_tiff(vol: Volume, path):
    import tifffile
    s = vol.spacing
    tifffile.imwrite(str(path), vol.data, imagej=vol.data.dtype in (np.uint8, np.uint16, np.float32),
                     resolution=(1.0 / s[2], 1.0 / s[1]),
                     metadata={"spacing": s[0], "unit": "um", "axes": "ZYX"})


def write_tiff_stack(vol: Volume, folder, prefix="slice_"):
    import tifffile
    f = Path(folder)
    f.mkdir(parents=True, exist_ok=True)
    for z in range(vol.shape[0]):
        tifffile.imwrite(str(f / f"{prefix}{z:05d}.tif"), vol.data[z])
    (f / "osteoquant_stack.json").write_text(json.dumps({"spacing_um": list(vol.spacing)}))


def write_nrrd(vol: Volume, path):
    import nrrd
    sp_mm = [s / 1000.0 for s in vol.spacing[::-1]]  # x,y,z
    hdr = {"space": "left-posterior-superior", "space directions": np.diag(sp_mm).tolist(),
           "space units": ["mm", "mm", "mm"]}
    nrrd.write(str(path), vol.data, hdr, index_order="C")


def write_dicom_series(vol: Volume, folder, series_description="OsteoQuant export"):
    """Minimal CT-like DICOM series export (research use; secondary capture semantics)."""
    import pydicom
    from pydicom.dataset import FileDataset, FileMetaDataset
    from pydicom.uid import ExplicitVRLittleEndian, generate_uid, CTImageStorage
    f = Path(folder)
    f.mkdir(parents=True, exist_ok=True)
    series_uid, study_uid, for_uid = generate_uid(), generate_uid(), generate_uid()
    data = vol.data
    if data.dtype != np.uint16:
        lo, hi = float(data.min()), float(data.max())
        scale = (hi - lo) / 65535.0 if hi > lo else 1.0
        data16 = ((data - lo) / (scale if scale else 1)).astype(np.uint16)
        slope, inter = scale, lo
    else:
        data16, slope, inter = data, 1.0, 0.0
    for z in range(data.shape[0]):
        meta = FileMetaDataset()
        meta.MediaStorageSOPClassUID = CTImageStorage
        meta.MediaStorageSOPInstanceUID = generate_uid()
        meta.TransferSyntaxUID = ExplicitVRLittleEndian
        ds = FileDataset(str(f / f"IM{z:05d}.dcm"), {}, file_meta=meta, preamble=b"\0" * 128)
        ds.SOPClassUID = CTImageStorage
        ds.SOPInstanceUID = meta.MediaStorageSOPInstanceUID
        ds.SeriesInstanceUID, ds.StudyInstanceUID, ds.FrameOfReferenceUID = series_uid, study_uid, for_uid
        ds.Modality = "CT"
        ds.SeriesDescription = series_description
        ds.PatientName, ds.PatientID = "PHANTOM", "PHANTOM"
        ds.Rows, ds.Columns = data.shape[1], data.shape[2]
        ds.PixelSpacing = [vol.spacing[1] / 1000.0, vol.spacing[2] / 1000.0]
        ds.SliceThickness = vol.spacing[0] / 1000.0
        ds.ImagePositionPatient = [0.0, 0.0, z * vol.spacing[0] / 1000.0]
        ds.ImageOrientationPatient = [1, 0, 0, 0, 1, 0]
        ds.InstanceNumber = z + 1
        ds.SamplesPerPixel, ds.PhotometricInterpretation = 1, "MONOCHROME2"
        ds.BitsAllocated, ds.BitsStored, ds.HighBit, ds.PixelRepresentation = 16, 16, 15, 0
        ds.RescaleSlope, ds.RescaleIntercept = slope, inter
        ds.PixelData = np.ascontiguousarray(data16[z]).tobytes()
        ds.save_as(str(f / f"IM{z:05d}.dcm"), enforce_file_format=True)
