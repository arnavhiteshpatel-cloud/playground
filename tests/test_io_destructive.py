"""Fuzzing / destructive tests for every reader.

Contract (QA-003/QA-004): a malformed, truncated or hostile input either reads successfully or
raises a ``ValueError`` subclass (``CorruptInput``, ``VolumeTooLarge``, ``UnsafeInput``) quickly;
it never hangs, never raises parser-specific exception types, and never allocates memory for a
header-declared size beyond ``OQ_MAX_READ_BYTES``.
"""
import gzip
import json
import os
import pickle
import random
import struct
import time
import zipfile
from pathlib import Path

import numpy as np
import pytest

from osteoquant import io as oio
from osteoquant.io.readers import (CorruptInput, UnsafeInput, VolumeTooLarge, check_safe_input, detect_format,
                                   max_read_bytes, read_volume)
from osteoquant.volume import Volume

from _cfb import write_txm

VOL = Volume(np.random.default_rng(0).integers(0, 4000, (6, 10, 12)).astype(np.uint16), (10.0, 11.0, 12.0))


@pytest.fixture
def small_limit(monkeypatch):
    monkeypatch.setenv("OQ_MAX_READ_BYTES", str(64 * 1024 ** 2))


def _seed(tmp_path, fmt):
    if fmt == "nii":
        p = tmp_path / "a.nii"
        oio.write_nifti(VOL, p)
    elif fmt == "nii.gz":
        p = tmp_path / "a.nii.gz"
        oio.write_nifti(VOL, p)
    elif fmt == "nrrd":
        p = tmp_path / "a.nrrd"
        oio.write_nrrd(VOL, p)
    elif fmt == "tif":
        p = tmp_path / "a.tif"
        oio.write_tiff(VOL, p)
    elif fmt == "txm":
        p = tmp_path / "a.txm"
        write_txm(p, VOL.data, pixel_size_um=10.0)
    elif fmt == "npy":
        p = tmp_path / "a.npy"
        np.save(p, VOL.data)
    elif fmt == "dcm":
        p = tmp_path / "dcm"
        oio.write_dicom_series(VOL, p)
    else:
        raise ValueError(fmt)
    return p


def _expect_clean(target, **kw):
    t = time.time()
    try:
        v, rep = read_volume(target, **kw)
        assert v.data.ndim == 3 and 0 not in v.shape
        out = "ok"
    except ValueError:          # CorruptInput / VolumeTooLarge / UnsafeInput are ValueErrors
        out = "rejected"
    assert time.time() - t < 20, "reader took too long on a malformed input"
    return out


FORMATS = ["nii", "nii.gz", "nrrd", "tif", "txm", "npy", "dcm"]


@pytest.mark.parametrize("fmt", FORMATS)
def test_truncation_never_crashes(tmp_path, fmt, small_limit):
    p = _seed(tmp_path, fmt)
    target = p
    if p.is_dir():
        p = sorted(p.iterdir())[2]
    raw = p.read_bytes()
    outcomes = set()
    for cut in sorted({0, 1, 8, 64, 128, 132, 348, 352, 512, len(raw) // 2, len(raw) - 1}):
        if cut >= len(raw):
            continue
        p.write_bytes(raw[:cut])
        outcomes.add(_expect_clean(target))
    assert "rejected" in outcomes


@pytest.mark.parametrize("fmt", FORMATS)
def test_random_byte_mutations_never_crash(tmp_path, fmt, small_limit):
    p = _seed(tmp_path, fmt)
    target = p
    if p.is_dir():
        p = sorted(p.iterdir())[1]
    raw = p.read_bytes()
    rng = random.Random(f"fuzz-{fmt}")
    for k in range(30):
        b = bytearray(raw)
        lim = min(len(b), 700) if k % 2 else len(b)      # alternate header-focused and anywhere
        for _ in range(rng.randint(1, 12)):
            i = rng.randrange(lim)
            b[i] = rng.choice([0, 0xFF, 0x7F, 0x80, rng.randrange(256)])
        if k % 5 == 0:   # plant large 32-bit integers (dimension / offset fields)
            i = rng.randrange(max(1, lim - 4))
            b[i:i + 4] = struct.pack("<I", rng.choice([0xFFFFFFFF, 0x7FFFFFFF, 65535, 100000]))
        p.write_bytes(bytes(b))
        _expect_clean(target)


# ----------------------------------------------------------------------------- huge declared dimensions
def test_huge_nifti_dims_fail_fast(tmp_path, small_limit):
    for name in ("h.nii", "h.nii.gz"):
        p = tmp_path / name
        oio.write_nifti(Volume(np.zeros((2, 2, 2), np.uint16), (1, 1, 1)), p)
        raw = p.read_bytes() if name.endswith(".nii") else gzip.decompress(p.read_bytes())
        b = bytearray(raw)
        b[40:56] = struct.pack("<8h", 3, 30000, 30000, 30000, 1, 1, 1, 1)
        p.write_bytes(bytes(b) if name.endswith(".nii") else gzip.compress(bytes(b)))
        with pytest.raises(VolumeTooLarge):
            read_volume(p)


@pytest.mark.parametrize("enc", ["raw", "gzip"])
def test_huge_nrrd_sizes_fail_fast(tmp_path, enc, small_limit):
    p = tmp_path / "h.nrrd"
    payload = b"\0" * 64 if enc == "raw" else gzip.compress(b"\0" * 64)
    p.write_bytes(f"NRRD0004\ntype: uint16\ndimension: 3\nsizes: 30000 30000 30000\nencoding: {enc}\n"
                  "endian: little\n\n".encode() + payload)
    with pytest.raises(VolumeTooLarge):
        read_volume(p)


def test_huge_zarr_shape_fail_fast(tmp_path, small_limit):
    import zarr
    p = tmp_path / "h.zarr"
    g = zarr.open_group(str(p), mode="w")
    g.create_array("image", shape=(2000, 2000, 2000), chunks=(64, 64, 64), dtype="uint16", fill_value=7)
    with pytest.raises(VolumeTooLarge, match="zrange"):
        read_volume(p)
    v, _ = read_volume(p, zrange=(0, 1), step=40)        # a bounded sub-range is still readable
    assert v.shape == (1, 50, 50) and int(v.data.max()) == 7


def test_huge_tiff_dims_fail_fast(tmp_path, small_limit):
    import tifffile
    p = tmp_path / "h.tif"
    tifffile.imwrite(p, np.zeros((8, 8), np.uint16))
    with tifffile.TiffFile(p) as tf:
        offs = {t.name: t.valueoffset for t in tf.pages[0].tags.values()}
    b = bytearray(p.read_bytes())
    for nm in ("ImageWidth", "ImageLength"):
        b[offs[nm]:offs[nm] + 4] = struct.pack("<I", 1_000_000)
    p.write_bytes(bytes(b))
    with pytest.raises(VolumeTooLarge):
        read_volume(p)


def test_huge_dicom_rows_cols_fail_fast(tmp_path, small_limit):
    import pydicom
    d = tmp_path / "dcm"
    oio.write_dicom_series(VOL, d)
    for f in d.iterdir():
        ds = pydicom.dcmread(f)
        ds.Rows = ds.Columns = 65535
        ds.save_as(f)
    with pytest.raises(VolumeTooLarge):
        read_volume(d)
    mf = tmp_path / "mf"
    mf.mkdir()
    ds = pydicom.dcmread(sorted(d.iterdir())[0])
    ds.Rows, ds.Columns, ds.NumberOfFrames = 8, 8, 2 ** 31 - 1
    ds.save_as(mf / "x.dcm")
    with pytest.raises(VolumeTooLarge):
        read_volume(mf)


def test_huge_txm_declared_size_fail_fast(tmp_path, small_limit):
    p = tmp_path / "h.txm"
    write_txm(p, np.zeros((2, 4, 4), np.uint16), width=60000, height=60000, n_images=60000, drop=(0, 1))
    with pytest.raises(VolumeTooLarge):
        read_volume(p)


def test_huge_npy_header(tmp_path, small_limit):
    p = tmp_path / "h.npy"
    hdr = b"{'descr': '<u2', 'fortran_order': False, 'shape': (30000, 30000, 30000), }"
    hdr = hdr + b" " * (118 - len(hdr) - 1) + b"\n"
    p.write_bytes(b"\x93NUMPY\x01\x00" + struct.pack("<H", len(hdr)) + hdr + b"\0" * 16)
    with pytest.raises(ValueError):
        read_volume(p)


def test_read_limit_env_and_default():
    assert max_read_bytes() > 0
    os.environ["OQ_MAX_READ_BYTES"] = "123"
    try:
        assert max_read_bytes() == 123
    finally:
        del os.environ["OQ_MAX_READ_BYTES"]


# ----------------------------------------------------------------------------- TXM structure faults
def test_txm_missing_and_short_slices(tmp_path):
    p = tmp_path / "a.txm"
    data = np.arange(4 * 5 * 6, dtype=np.uint16).reshape(4, 5, 6)
    write_txm(p, data, drop=(2,))
    v, rep = read_volume(p)
    assert rep.missing_slices == [2] and np.all(v.data[2] == 0) and np.array_equal(v.data[3], data[3])
    assert any("missing" in w for w in rep.warnings)
    write_txm(p, data, extra={"ImageData1/Image2": b"\0" * 10})
    v, rep = read_volume(p)
    assert rep.errors and "Slice 1" in rep.errors[0]


def test_txm_metadata_faults(tmp_path):
    p = tmp_path / "a.txm"
    data = np.zeros((2, 3, 3), np.uint16)
    write_txm(p, data, data_type=99)
    with pytest.raises(CorruptInput, match="DataType"):
        read_volume(p)
    write_txm(p, data, n_images=0)
    v, rep = read_volume(p)                              # falls back to the stream count
    assert v.shape == (2, 3, 3)
    write_txm(p, data, n_images=5)
    v, rep = read_volume(p)
    assert any("NoOfImages=5" in w for w in rep.warnings) and rep.missing_slices == [2, 3, 4]
    write_txm(p, data, pixel_size_um=0.0)
    v, rep = read_volume(p)
    assert rep.metadata_assumed.get("spacing_um") == [1, 1, 1]
    from _cfb import write_cfb
    write_cfb(p, {"ImageInfo/DataType": struct.pack("<I", 5)})
    with pytest.raises(CorruptInput, match="ImageWidth"):
        read_volume(p)


# ----------------------------------------------------------------------------- DICOM structure faults
def test_dicom_corrupt_slice_is_reported_not_silently_dropped(tmp_path):
    d = tmp_path / "dcm"
    oio.write_dicom_series(VOL, d)
    f = sorted(d.iterdir())[3]
    f.write_bytes(b"garbage" * 10)
    v, rep = read_volume(d)
    assert any("could not be parsed as DICOM" in w for w in rep.warnings)
    assert rep.missing_slices == [3]


def test_dicom_series_geometry_faults(tmp_path):
    import pydicom
    d = tmp_path / "dcm"
    oio.write_dicom_series(VOL, d)
    files = sorted(d.iterdir())
    for f in files:                                     # remove geometry -> InstanceNumber ordering
        ds = pydicom.dcmread(f)
        del ds.ImagePositionPatient
        ds.save_as(f)
    v, rep = read_volume(d)
    assert any("No ImagePositionPatient" in w for w in rep.warnings) and v.spacing[0] == pytest.approx(10.0)
    d2 = tmp_path / "dup"
    oio.write_dicom_series(VOL, d2)
    for f in sorted(d2.iterdir()):
        ds = pydicom.dcmread(f)
        ds.ImagePositionPatient = [0.0, 0.0, 0.0]
        ds.save_as(f)
    v, rep = read_volume(d2)
    assert "Duplicate slice positions" in rep.errors
    d3 = tmp_path / "two"
    oio.write_dicom_series(VOL, d3 / "a")
    oio.write_dicom_series(Volume(VOL.data[:2], VOL.spacing), d3 / "b")
    for f in (d3 / "b").iterdir():
        f.rename(d3 / "a" / ("b_" + f.name))
    v, rep = read_volume(d3 / "a")
    assert v.shape[0] == 6 and any("2 series" in w for w in rep.warnings)


def test_dicom_empty_and_zrange_faults(tmp_path):
    d = tmp_path / "x"
    d.mkdir()
    (d / "a.dcm").write_bytes(b"\0" * 200)
    with pytest.raises(ValueError):
        read_volume(d)
    d2 = tmp_path / "dcm"
    oio.write_dicom_series(VOL, d2)
    with pytest.raises(ValueError):
        read_volume(d2, zrange=(50, 60))


# ----------------------------------------------------------------------------- stacks / detection
def test_tiff_stack_faults(tmp_path):
    import tifffile
    d = tmp_path / "s"
    d.mkdir()
    for i in (0, 1, 2):
        tifffile.imwrite(d / f"img_{i:03d}.tif", np.full((4, 5), i, np.uint16))
    tifffile.imwrite(d / "img_003.tif", np.zeros((3, 3), np.uint16))          # wrong shape
    v, rep = read_volume(d)
    assert rep.errors and "img_003" in rep.errors[0]
    with pytest.raises(ValueError, match="selects no slices"):
        read_volume(d, zrange=(10, 20))
    (d / "img_003.tif").unlink()
    tifffile.imwrite(d / "img_002b.tif", np.zeros((4, 5), np.uint16))        # duplicate index 2
    v, rep = read_volume(d)
    assert any("Duplicate slice indices" in w for w in rep.warnings)


def test_bruker_log_spacing_and_rgb_slices(tmp_path):
    from PIL import Image
    d = tmp_path / "rec"
    d.mkdir()
    for i in range(3):
        Image.fromarray(np.full((6, 7, 3), 40 * i, np.uint8)).save(d / f"s_rec{i:08d}.png")
    (d / "s_rec.log").write_text("[System]\nScanner=SkyScan1272\nImage Pixel Size (um)=  9.0\n"
                                 "Source Voltage (kV)= 70\nFilter=Al 0.5mm\n")
    v, rep = read_volume(d)
    assert v.spacing == (9.0, 9.0, 9.0) and rep.metadata_found["Source Voltage (kV)"] == "70"
    assert any("RGB" in w for w in rep.warnings) and v.data.dtype == np.float32
    assert v.data[2].mean() == pytest.approx(80.0)


def test_large_stack_uses_manifest_hash(tmp_path):
    import tifffile
    d = tmp_path / "big"
    d.mkdir()
    for i in range(70):
        tifffile.imwrite(d / f"z{i:04d}.tif", np.zeros((2, 2), np.uint8))
    v, rep = read_volume(d)
    assert len(rep.files) == 1 and rep.files[0]["kind"] == "stack-manifest-hash" and rep.files[0]["n_files"] == 70


def test_detect_format_errors(tmp_path):
    with pytest.raises(ValueError):
        detect_format(tmp_path)                          # empty folder
    (tmp_path / "x.xyz").write_text("x")
    with pytest.raises(ValueError):
        detect_format(tmp_path / "x.xyz")
    with pytest.raises(ValueError):
        detect_format(tmp_path)
    assert detect_format(tmp_path / "a.ome.tiff") == "ome-tiff"
    dc = tmp_path / "noext"
    dc.write_bytes(b"\0" * 128 + b"DICM" + b"\0" * 10)
    assert detect_format(dc) == "dicom"


def test_npy_must_be_3d_and_step_validated(tmp_path):
    p = tmp_path / "a.npy"
    np.save(p, np.zeros((4, 4)))
    with pytest.raises(ValueError, match="3"):
        read_volume(p)
    np.save(p, np.zeros((4, 4, 4)))
    with pytest.raises(ValueError):
        read_volume(p, step=0)
    np.save(p, np.array([{"a": 1}], dtype=object))
    with pytest.raises(ValueError):                      # pickled object arrays refused
        read_volume(p)


def test_nifti_4d_and_unknown_units(tmp_path):
    import nibabel as nib
    p = tmp_path / "a.nii"
    nib.save(nib.Nifti1Image(np.zeros((3, 4, 5, 1), np.int16), np.eye(4)), str(p))
    v, rep = read_volume(p)
    assert v.shape == (5, 4, 3) and "spatial_unit" in rep.metadata_assumed
    nib.save(nib.Nifti1Image(np.zeros((3, 4, 5, 2), np.int16), np.eye(4)), str(p))
    with pytest.raises(CorruptInput, match="dims"):
        read_volume(p)


@pytest.mark.parametrize("fmt", ["nii", "npy", "tif"])
def test_reader_output_does_not_keep_source_memory_mapped(tmp_path, fmt):
    """Readers must return owned arrays: a memmap-backed Volume kept the source file mapped, so on Windows it could
    not be overwritten or deleted after import (CI failure in test_nifti_4d_and_unknown_units)."""
    import mmap
    arr = np.arange(4 * 5 * 6, dtype=np.int16).reshape(4, 5, 6)
    p = tmp_path / f"a.{fmt}"
    if fmt == "nii":
        import nibabel as nib
        nib.save(nib.Nifti1Image(np.transpose(arr, (2, 1, 0)), np.eye(4)), str(p))
    elif fmt == "npy":
        np.save(p, arr)
    else:
        import tifffile
        tifffile.imwrite(p, arr)
    v, _ = read_volume(p, spacing_um=(1.0, 1.0, 1.0)) if fmt != "nii" else read_volume(p)
    base = v.data
    while base is not None:
        assert not isinstance(base, (np.memmap, mmap.mmap)), f"{fmt}: Volume data is backed by a memory map"
        base = getattr(base, "base", None)
    assert np.array_equal(v.data, arr)
    del v
    p.unlink()                      # the source can be removed once read (fails on Windows while mapped)


def test_nrrd_units_and_missing_spacing(tmp_path):
    import nrrd
    p = tmp_path / "a.nrrd"
    nrrd.write(str(p), np.zeros((2, 3, 4), np.uint8), {"spacings": [2.0, 3.0, 4.0], "units": ["um", "um", "um"]},
               index_order="C")
    v, rep = read_volume(p)
    assert v.spacing == (4.0, 3.0, 2.0)
    nrrd.write(str(p), np.zeros((2, 3, 4), np.uint8), {}, index_order="C")
    v, rep = read_volume(p)
    assert rep.metadata_assumed["spacing_um"] == [1.0, 1.0, 1.0]
    nrrd.write(str(p), np.zeros((3, 4), np.uint8), {}, index_order="C")
    with pytest.raises(CorruptInput):
        read_volume(p)


def test_zarr_integrity_detects_deleted_chunk(tmp_path):
    p = tmp_path / "a.zarr"
    oio.write_zarr(VOL, p, chunks=(3, 5, 6))
    chunk = next(f for f in (p / "image").rglob("*") if f.is_file() and f.name != "zarr.json")
    chunk.unlink()
    with pytest.raises(CorruptInput, match="integrity"):
        read_volume(p)
    v, _ = read_volume(p, do_hash=False)                 # explicit opt-out (previews) still works
    assert v.shape == VOL.shape


def test_zarr_without_image_array(tmp_path):
    import zarr
    p = tmp_path / "e.zarr"
    zarr.open_group(str(p), mode="w").attrs["spacing_um"] = [1, 1, 1]
    with pytest.raises(CorruptInput):
        read_volume(p)


def test_itk_reader_and_unsafe_for_uploads(tmp_path):
    import SimpleITK as sitk
    img = sitk.GetImageFromArray(np.ones((3, 4, 5), np.uint8))
    img.SetSpacing((0.01, 0.02, 0.03))
    p = tmp_path / "a.mha"
    sitk.WriteImage(img, str(p))
    v, rep = read_volume(p)
    assert v.shape == (3, 4, 5) and v.spacing == pytest.approx((30.0, 20.0, 10.0))
    with pytest.raises(UnsafeInput):
        read_volume(p, safe=True)


# ----------------------------------------------------------------------------- hostile uploads (safe=True)
def _evil_zarr(root: Path, v3=False):
    root.mkdir(parents=True)
    marker = root.parent / "PWNED"

    class Evil:
        def __reduce__(self):
            return (open, (str(marker), "w"))
    if v3:
        (root / "image" / "c").mkdir(parents=True)
        (root / "zarr.json").write_text(json.dumps({"zarr_format": 3, "node_type": "group", "attributes": {}}))
        (root / "image" / "zarr.json").write_text(json.dumps({
            "zarr_format": 3, "node_type": "array", "shape": [2], "data_type": "uint8",
            "chunk_grid": {"name": "regular", "configuration": {"chunk_shape": [2]}},
            "chunk_key_encoding": {"name": "default", "configuration": {"separator": "/"}}, "fill_value": 0,
            "codecs": [{"name": "bytes"}, {"name": "numcodecs.pickle"}], "attributes": {}}))
        (root / "image" / "c" / "0").write_bytes(pickle.dumps(Evil()))
    else:
        (root / "image").mkdir()
        (root / ".zgroup").write_text(json.dumps({"zarr_format": 2}))
        (root / "image" / ".zarray").write_text(json.dumps({
            "zarr_format": 2, "shape": [2], "chunks": [2], "dtype": "<u1", "fill_value": 0, "order": "C",
            "compressor": {"id": "pickle"}, "filters": None}))
        (root / "image" / "0").write_bytes(pickle.dumps(Evil()))
    return marker


@pytest.mark.parametrize("v3", [False, True])
def test_zarr_pickle_codec_rejected_before_decoding(tmp_path, v3):
    marker = _evil_zarr(tmp_path / "up" / "evil.zarr", v3=v3)
    with pytest.raises(UnsafeInput, match="pickle"):
        read_volume(tmp_path / "up" / "evil.zarr", safe=True)
    assert not marker.exists()


def test_zarr_object_dtype_and_consolidated_metadata_rejected(tmp_path):
    root = tmp_path / "c.zarr"
    oio.write_zarr(VOL, root)
    check_safe_input(root)                               # our own stores are accepted
    (root / ".zmetadata").write_text(json.dumps({"metadata": {"image/.zarray": {"dtype": "|O", "compressor": None,
                                                                                "filters": [{"id": "pickle"}]}}}))
    with pytest.raises(UnsafeInput):
        check_safe_input(root)
    (root / ".zmetadata").unlink()
    (root / "zarr.json").write_text("{not json")
    with pytest.raises(CorruptInput):
        check_safe_input(root)


def test_ome_tiff_external_reference_rejected(tmp_path):
    import tifffile
    outside = tmp_path / "secret.ome.tif"
    tifffile.imwrite(outside, np.full((2, 4, 4), 7, np.uint16), ome=True)
    xml = ('<?xml version="1.0" encoding="UTF-8"?><OME xmlns="http://www.openmicroscopy.org/Schemas/OME/2016-06">'
           '<Image ID="Image:0"><Pixels ID="Pixels:0" DimensionOrder="XYZCT" Type="uint16" SizeX="4" SizeY="4" '
           'SizeZ="2" SizeC="1" SizeT="1"><Channel ID="Channel:0" SamplesPerPixel="1"/>'
           f'<TiffData FirstZ="0" IFD="0" PlaneCount="2"><UUID FileName="{outside}">urn:uuid:0</UUID></TiffData>'
           '</Pixels></Image></OME>')
    up = tmp_path / "up"
    up.mkdir()
    tifffile.imwrite(up / "evil.ome.tif", np.zeros((4, 4), np.uint16), description=xml.encode(), metadata=None)
    with pytest.raises(UnsafeInput, match="outside the upload"):
        read_volume(up / "evil.ome.tif", safe=True)
    ok = tmp_path / "ok.ome.tif"
    tifffile.imwrite(ok, np.zeros((2, 4, 4), np.uint16), ome=True)
    check_safe_input(ok)


@pytest.mark.skipif(not hasattr(os, "symlink"), reason="no symlinks")
def test_symlinks_rejected_in_uploads(tmp_path):
    d = tmp_path / "stack"
    oio.write_tiff_stack(VOL, d)
    try:
        os.symlink(d / "slice_00000.tif", d / "slice_00099.tif")
    except OSError:
        pytest.skip("symlink creation not permitted")
    with pytest.raises(UnsafeInput, match="Symbolic"):
        read_volume(d, safe=True)
    with pytest.raises(UnsafeInput):
        check_safe_input(d / "slice_00099.tif")


def test_malformed_nrrd_header_in_safe_mode(tmp_path):
    p = tmp_path / "x.nrrd"
    p.write_bytes(b"NRRD0004\nsizes: banana\n\n")
    with pytest.raises(CorruptInput):
        read_volume(p, safe=True)


def test_upload_zip_with_zarr_payload_rejected_end_to_end(tmp_path):
    from osteoquant.io.safe_archive import safe_extract
    marker = _evil_zarr(tmp_path / "src" / "evil.zarr")
    z = tmp_path / "u.zip"
    with zipfile.ZipFile(z, "w") as zf:
        for f in (tmp_path / "src").rglob("*"):
            if f.is_file():
                zf.write(f, f.relative_to(tmp_path / "src"))
    out = tmp_path / "ex"
    safe_extract(z, out)
    with pytest.raises(UnsafeInput):
        read_volume(out / "evil.zarr", safe=True)
    assert not marker.exists() and not (out / "PWNED").exists()


def test_ome_xml_entity_expansion_rejected_quickly(tmp_path):
    """Billion-laughs OME-XML (bandit B314): expat's amplification limit makes the safe check fail fast."""
    import tifffile
    ents = "".join(f'<!ENTITY l{i} "' + (f"&l{i - 1};" if i > 1 else "lol") * 10 + '">' for i in range(1, 10))
    xml = (f'<?xml version="1.0"?><!DOCTYPE z [{ents}]><OME xmlns="http://www.openmicroscopy.org/Schemas/OME/2016-06">'
           '<Image ID="Image:0" Name="&l9;"><Pixels ID="Pixels:0" DimensionOrder="XYZCT" Type="uint8" SizeX="4" '
           'SizeY="4" SizeZ="1" SizeC="1" SizeT="1"/></Image></OME>')
    p = tmp_path / "lol.ome.tif"
    tifffile.imwrite(p, np.zeros((4, 4), np.uint8), description=xml.encode(), metadata=None)
    t = time.time()
    with pytest.raises(ValueError):
        read_volume(p, safe=True)
    assert time.time() - t < 5
