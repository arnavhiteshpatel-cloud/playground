"""Reader metadata paths (OME/ImageJ spacing, DICOM variants, TXM recon fields), writer helpers and
safe-input validation edge cases."""
import json
import struct

import numpy as np
import pytest

from osteoquant import io as oio
from osteoquant.io import readers as R
from osteoquant.io.readers import CorruptInput, UnsafeInput, VolumeTooLarge, check_safe_input, read_volume
from osteoquant.io.writers import _jsonable, iter_slabs, read_labels_zarr, write_labels_zarr
from osteoquant.volume import Volume

from _cfb import write_txm

VOL = Volume(np.arange(4 * 6 * 5, dtype=np.uint16).reshape(4, 6, 5), (8.0, 4.0, 4.0))


# ----------------------------------------------------------------------------- TIFF metadata
@pytest.mark.parametrize("unit,scale", [("µm", 1.0), ("nm", 1e-3), ("mm", 1e3)])
def test_ome_tiff_physical_size_units(tmp_path, unit, scale):
    import tifffile
    p = tmp_path / "a.ome.tif"
    tifffile.imwrite(p, VOL.data, ome=True, metadata={"axes": "ZYX", "PhysicalSizeX": 2.0, "PhysicalSizeXUnit": unit,
                                                      "PhysicalSizeY": 3.0, "PhysicalSizeYUnit": unit,
                                                      "PhysicalSizeZ": 5.0, "PhysicalSizeZUnit": unit})
    v, rep = read_volume(p)
    assert v.spacing == pytest.approx((5.0 * scale, 3.0 * scale, 2.0 * scale))
    assert rep.format == "ome-tiff"


def test_ome_tiff_missing_z_size_warns(tmp_path):
    import tifffile
    p = tmp_path / "b.ome.tif"
    tifffile.imwrite(p, VOL.data, ome=True, metadata={"axes": "ZYX", "PhysicalSizeX": 2.0, "PhysicalSizeY": 2.0})
    v, rep = read_volume(p)
    assert v.spacing == pytest.approx((2.0, 2.0, 2.0)) and any("PhysicalSizeZ" in w for w in rep.warnings)


def test_imagej_mm_units_and_multichannel_rejected(tmp_path):
    import tifffile
    p = tmp_path / "ij.tif"
    tifffile.imwrite(p, VOL.data, imagej=True, resolution=(1 / 0.004, 1 / 0.004),
                     metadata={"spacing": 0.008, "unit": "mm", "axes": "ZYX"})
    v, _ = read_volume(p)
    assert v.spacing == pytest.approx((8.0, 4.0, 4.0), rel=1e-4)
    q = tmp_path / "rgb.tif"
    tifffile.imwrite(q, np.zeros((3, 4, 5, 6, 2), np.uint8))
    with pytest.raises(CorruptInput, match="dims"):
        read_volume(q)
    s = tmp_path / "single.tif"
    tifffile.imwrite(s, np.ones((5, 6), np.uint8))
    v, rep = read_volume(s)
    assert v.shape == (1, 5, 6) and rep.metadata_assumed["spacing_um"] == [1.0, 1.0, 1.0]


def test_tiff_stack_pattern_and_bad_sidecar(tmp_path):
    d = tmp_path / "st"
    oio.write_tiff_stack(VOL, d)
    with pytest.raises(CorruptInput, match="No image slices"):
        read_volume(d, pattern="nomatch")
    v, _ = read_volume(d, pattern=r"0000[0-1]")
    assert v.shape[0] == 2
    (d / "osteoquant_stack.json").write_text(json.dumps({"spacing_um": "bad"}))
    v, rep = read_volume(d)
    assert any("unreadable" in w for w in rep.warnings) and rep.metadata_assumed["spacing_um"] == [1.0, 1.0, 1.0]


# ----------------------------------------------------------------------------- DICOM variants
def test_dicom_multiframe_and_metadata(tmp_path):
    import pydicom
    d = tmp_path / "src"
    oio.write_dicom_series(VOL, d)
    ds = pydicom.dcmread(sorted(d.iterdir())[0])
    frames = VOL.data
    ds.NumberOfFrames = frames.shape[0]
    ds.PixelData = frames.tobytes()
    ds.SliceThickness = 0.008
    ds.Manufacturer = "TestVendor"
    ds.RescaleType = "HU"
    mf = tmp_path / "mf"
    mf.mkdir()
    ds.save_as(mf / "mf.dcm")
    v, rep = read_volume(mf)
    assert v.shape == VOL.shape and np.array_equal(v.data, frames.astype(np.float32))
    assert v.spacing == pytest.approx((8.0, 4.0, 4.0)) and rep.metadata_found["Manufacturer"] == "TestVendor"


def test_dicom_irregular_spacing_missing_pixelspacing_and_negative_intercept(tmp_path):
    import pydicom
    d = tmp_path / "s"
    oio.write_dicom_series(Volume(np.ones((6, 4, 4), np.uint16), (10, 10, 10)), d)
    files = sorted(d.iterdir())
    files[3].unlink()                                   # gap -> one missing slice
    for i, f in enumerate(files):
        if i == 3:
            continue
        ds = pydicom.dcmread(f)
        if i == 5:
            ds.ImagePositionPatient = [0.0, 0.0, 0.0512]   # 1.2 % irregular step
        del ds.PixelSpacing
        ds.RescaleIntercept = -1024
        ds.RescaleType = "HU"
        ds.save_as(f)
    v, rep = read_volume(d)
    assert rep.missing_slices == [3]
    assert any("Irregular" in w for w in rep.warnings)
    assert rep.metadata_assumed["pixel_spacing"] and v.data.dtype == np.int32 and v.data.min() == -1023
    assert rep.metadata_found["RescaleType"] == "HU"


def test_dicom_float_rescale_and_single_file(tmp_path):
    import pydicom
    d = tmp_path / "s"
    oio.write_dicom_series(Volume(np.full((2, 3, 3), 10, np.uint16), (10, 10, 10)), d)
    for f in d.iterdir():
        ds = pydicom.dcmread(f)
        ds.RescaleSlope = 0.5
        ds.save_as(f)
    v, _ = read_volume(d)
    assert v.data.dtype == np.float32 and np.allclose(v.data, 5.0)
    one = sorted(d.iterdir())[0]
    v1, rep1 = read_volume(one)
    assert v1.shape == (1, 3, 3)


def test_looks_like_dicom_tolerates_unreadable_paths(tmp_path):
    assert R._looks_like_dicom(tmp_path) is False            # a directory -> OSError path
    assert R._looks_like_dicom(tmp_path / "missing") is False


# ----------------------------------------------------------------------------- TXM / Zarr / errors
def test_txm_recon_fields_and_tuple_pixel_size(tmp_path):
    p = tmp_path / "a.txm"
    data = np.ones((2, 3, 3), np.uint16)
    write_txm(p, data, extra={"ReconSettings/BinningIndex": struct.pack("<i", 2),
                              "ReconSettings/Blob": b"\x00\x01",
                              "ImageInfo/PixelSize": struct.pack("<ff", 2.5, 2.5)})
    md = oio.txm_metadata(p)
    assert md["recon:BinningIndex"] == 2 and "recon:Blob" not in md
    v, _ = read_volume(p)
    assert v.spacing == (2.5, 2.5, 2.5)


def test_zarr_non_3d_image_and_labels_helpers(tmp_path):
    import zarr
    p = tmp_path / "x.zarr"
    g = zarr.open_group(str(p), mode="w")
    g.create_array("image", shape=(4, 4), dtype="uint8")
    with pytest.raises(CorruptInput, match="dims"):
        read_volume(p)
    q = tmp_path / "y.zarr"
    oio.write_zarr(VOL, q, chunks=(2, 3, 3), labels={"init": np.ones(VOL.shape)})
    assert read_labels_zarr(q, "missing") is None and read_labels_zarr(q, "init").sum() == VOL.data.size
    write_labels_zarr(q, "init", np.zeros(VOL.shape))          # replace an existing layer
    assert read_labels_zarr(q, "init").sum() == 0
    slabs = list(iter_slabs(q, slab=3, overlap=1))
    assert [s[:2] for s in slabs] == [(0, 3), (3, 4)] and slabs[1][3] == 2


def test_jsonable_converts_numpy_and_objects():
    out = _jsonable({1: np.int16(3), "f": np.float32(1.5), "a": np.arange(2), "t": (1, None), "o": object()})
    assert out["1"] == 3 and out["f"] == 1.5 and out["a"] == [0, 1] and out["t"] == [1, None]
    assert isinstance(out["o"], str)
    json.dumps(out)


def test_memory_error_becomes_volume_too_large(tmp_path, monkeypatch):
    p = tmp_path / "a.npy"
    np.save(p, np.zeros((2, 2, 2)))

    def boom(*a, **k):
        raise MemoryError
    monkeypatch.setattr(R, "read_npy", boom)
    with pytest.raises(VolumeTooLarge, match="memory"):
        read_volume(p)


# ----------------------------------------------------------------------------- safe-input edge cases
def _zarray(tmp_path, meta, name=".zarray"):
    d = tmp_path / "z"
    (d / "image").mkdir(parents=True, exist_ok=True)
    (d / "image" / name).write_text(json.dumps(meta))
    return d


@pytest.mark.parametrize("meta", [
    {"compressor": 5},                                          # not a codec spec
    {"compressor": "pickle"},                                   # string codec id
    {"data_type": {"name": "custom"}},                          # v3 extension dtype
    {"dtype": [["a", "<i4"], ["b", "|O"]]},                     # structured dtype
    {"dtype": "not-a-dtype"},
    {"codecs": [{"name": "sharding_indexed", "configuration": {"codecs": [{"name": "numcodecs.pickle"}]}}]},
])
def test_zarr_metadata_rejections(tmp_path, meta):
    with pytest.raises(UnsafeInput):
        check_safe_input(_zarray(tmp_path, meta))


def test_zarr_metadata_accepts_safe_codecs(tmp_path):
    check_safe_input(_zarray(tmp_path, {"dtype": "<u2", "compressor": {"id": "blosc", "cname": "zstd"},
                                        "filters": [{"id": "delta", "dtype": "<u2"}], "attributes": {"x": "pickle"}}))
    check_safe_input(_zarray(tmp_path, {"data_type": "float32", "codecs": [
        {"name": "bytes", "configuration": {"endian": "little"}}, {"name": "zstd", "configuration": {"level": 0}}]},
        name="zarr.json"))


def test_safe_mode_rejects_malformed_tiff_and_ome(tmp_path):
    import tifffile
    p = tmp_path / "bad.tif"
    p.write_bytes(b"II*\x00garbage")
    with pytest.raises(CorruptInput):
        read_volume(p, safe=True)
    q = tmp_path / "x.ome.tif"
    tifffile.imwrite(q, np.zeros((4, 4), np.uint8), description=b'<?xml version="1.0"?><OME xmlns="http://www.openmicroscopy.org/Schemas/OME/2016-06"><Image', metadata=None)
    try:
        check_safe_input(q)                       # tifffile may not flag truncated XML as OME at all
    except (UnsafeInput, CorruptInput):
        pass
