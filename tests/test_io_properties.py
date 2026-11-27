"""Property-based reader <-> writer round trips for every supported format."""
import numpy as np
import pytest
from hypothesis import given
from hypothesis import strategies as hst
from hypothesis.extra import numpy as hnp

from osteoquant import io as oio
from osteoquant.volume import Volume

from _cfb import write_txm

shapes = hst.tuples(hst.integers(1, 6), hst.integers(2, 9), hst.integers(2, 9))
spacing = hst.tuples(*[hst.floats(0.5, 500.0, allow_nan=False, allow_infinity=False).map(lambda v: round(v, 3))] * 3)
iso = hst.floats(0.5, 500.0, allow_nan=False).map(lambda v: round(v, 3))


def arrays(dtypes, shape_st=shapes):
    return hst.sampled_from(dtypes).flatmap(
        lambda dt: shape_st.flatmap(lambda sh: hnp.arrays(dt, sh, elements=_elements(dt))))


def _elements(dt):
    dt = np.dtype(dt)
    if dt.kind == "f":
        return hst.floats(-1e4, 1e4, allow_nan=False, allow_infinity=False, width=dt.itemsize * 8)
    info = np.iinfo(dt)
    return hst.integers(int(info.min), int(info.max))


@given(arr=arrays([np.uint8, np.int16, np.uint16, np.int32, np.float32, np.float64]), sp=spacing)
def test_nifti_roundtrip(tmp_path_factory, arr, sp):
    p = tmp_path_factory.mktemp("nii") / "a.nii.gz"
    oio.write_nifti(Volume(arr, sp), p)
    v, rep = oio.read_volume(p)
    assert v.data.dtype == arr.dtype and np.array_equal(v.data, arr)
    assert np.allclose(v.spacing, sp, rtol=1e-5)
    assert rep.metadata_found["spatial_unit"] == "mm"


@given(arr=arrays([np.uint8, np.int8, np.int16, np.uint16, np.int32, np.uint32, np.int64, np.float32, np.float64]),
       sp=spacing)
def test_nrrd_roundtrip(tmp_path_factory, arr, sp):
    p = tmp_path_factory.mktemp("nrrd") / "a.nrrd"
    oio.write_nrrd(Volume(arr, sp), p)
    v, _ = oio.read_volume(p)
    assert v.data.dtype == arr.dtype and np.array_equal(v.data, arr)
    assert np.allclose(v.spacing, sp, rtol=1e-9)


@given(arr=arrays([np.uint8, np.uint16, np.int16, np.float32, np.float64, np.int32]), sp=spacing,
       origin=hst.tuples(*[hst.floats(-1e4, 1e4, allow_nan=False)] * 3))
def test_zarr_roundtrip_exact_with_hash(tmp_path_factory, arr, sp, origin):
    p = tmp_path_factory.mktemp("zarr") / "a.zarr"
    vol = Volume(arr, sp, origin=origin)
    h = oio.write_zarr(vol, p, chunks=(2, 3, 4))
    v, rep = oio.read_volume(p)
    assert np.array_equal(v.data, arr) and v.data.dtype == arr.dtype
    assert v.spacing == vol.spacing and v.origin == vol.origin
    assert v.content_hash() == h == rep.files[0]["sha256"]


@given(arr=arrays([np.uint8, np.uint16, np.float32]), sp=hst.tuples(iso, iso).map(lambda t: (t[0], t[1], t[1])))
def test_imagej_tiff_roundtrip(tmp_path_factory, arr, sp):
    p = tmp_path_factory.mktemp("tif") / "a.tif"
    oio.write_tiff(Volume(arr, sp), p)
    v, rep = oio.read_volume(p)
    assert np.array_equal(v.data, arr)
    assert np.allclose(v.spacing, sp, rtol=1e-4)      # rational resolution tags
    assert "spacing_um" not in rep.metadata_assumed


@given(arr=arrays([np.uint8, np.uint16, np.float32]), sp=spacing)
def test_tiff_stack_roundtrip_reads_sidecar_spacing(tmp_path_factory, arr, sp):
    d = tmp_path_factory.mktemp("stack") / "s"
    oio.write_tiff_stack(Volume(arr, sp), d)
    v, rep = oio.read_volume(d)
    assert np.array_equal(v.data, arr) and v.spacing == pytest.approx(sp)
    assert rep.missing_slices == [] and "spacing_um" not in rep.metadata_assumed


@given(arr=arrays([np.uint16], hst.tuples(hst.integers(1, 4), hst.integers(2, 8), hst.integers(2, 8))),
       sp=spacing)
def test_dicom_uint16_roundtrip(tmp_path_factory, arr, sp):
    d = tmp_path_factory.mktemp("dcm") / "s"
    oio.write_dicom_series(Volume(arr, sp), d)
    v, rep = oio.read_volume(d)
    assert np.array_equal(v.data, arr)
    if arr.shape[0] > 1:                           # z spacing from ImagePositionPatient
        assert v.spacing[0] == pytest.approx(sp[0], rel=1e-6)
    assert v.spacing[1:] == pytest.approx(sp[1:], rel=1e-6)


@given(arr=arrays([np.float32, np.int16], hst.tuples(hst.integers(1, 3), hst.integers(2, 6), hst.integers(2, 6))))
def test_dicom_rescaled_roundtrip_is_within_quantisation(tmp_path_factory, arr):
    d = tmp_path_factory.mktemp("dcmf") / "s"
    oio.write_dicom_series(Volume(arr, (10, 10, 10)), d)
    v, _ = oio.read_volume(d)
    rng = float(arr.max()) - float(arr.min())
    assert np.allclose(v.data, arr.astype(np.float64), atol=max(rng / 65535.0 * 1.01, 1e-3) + 1e-3 * abs(arr).max())


@given(arr=arrays([np.uint16, np.float32, np.uint8, np.int16],
                  hst.tuples(hst.integers(1, 5), hst.integers(1, 9), hst.integers(1, 9))),
       px=hst.floats(0.1, 100.0).map(lambda v: float(np.float32(v))))
def test_txm_roundtrip(tmp_path_factory, arr, px):
    code = {np.dtype(np.uint16): 5, np.dtype(np.float32): 10, np.dtype(np.uint8): 3, np.dtype(np.int16): 6}[arr.dtype]
    p = tmp_path_factory.mktemp("txm") / "a.txm"
    write_txm(p, arr, pixel_size_um=px, data_type=code)
    v, rep = oio.read_volume(p)
    assert np.array_equal(v.data, arr) and v.spacing == pytest.approx((px,) * 3)
    assert rep.missing_slices == []


@given(arr=arrays([np.uint16, np.float32]), step=hst.integers(1, 3), data=hst.data())
def test_zrange_and_step_equal_array_slicing(tmp_path_factory, arr, step, data):
    z0 = data.draw(hst.integers(0, arr.shape[0] - 1))
    z1 = data.draw(hst.integers(z0 + 1, arr.shape[0]))
    p = tmp_path_factory.mktemp("sl") / "a.nrrd"
    oio.write_nrrd(Volume(arr, (2.0, 3.0, 4.0)), p)
    v, rep = oio.read_volume(p, zrange=(z0, z1), step=step)
    assert np.array_equal(v.data, arr[z0:z1:step, ::step, ::step])
    assert v.spacing == pytest.approx((2.0 * step, 3.0 * step, 4.0 * step))
    assert rep.decimation_step == step


@given(arr=arrays([np.uint8, np.float32]))
def test_npy_roundtrip(tmp_path_factory, arr):
    p = tmp_path_factory.mktemp("npy") / "a.npy"
    np.save(p, arr)
    v, rep = oio.read_volume(p)
    assert np.array_equal(v.data, arr) and v.spacing == (1.0, 1.0, 1.0) and rep.warnings


@given(sp=spacing)
def test_user_spacing_override_is_recorded(tmp_path_factory, sp):
    p = tmp_path_factory.mktemp("ov") / "a.nrrd"
    oio.write_nrrd(Volume(np.zeros((2, 2, 2), np.uint8), (1.0, 1.0, 1.0)), p)
    v, rep = oio.read_volume(p, spacing_um=sp)
    assert v.spacing == pytest.approx(sp)
    assert rep.metadata_found["spacing_um_user"] == pytest.approx(list(sp))
    if not np.allclose(sp, 1.0):
        assert any("differs from file metadata" in w for w in rep.warnings)
    assert v.meta["ingest"]["format"] == "nrrd"
