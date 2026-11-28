"""Hostile archive handling: zip bombs, traversal, links, collisions, encryption, special files."""
import io
import stat
import tarfile
import zipfile
from pathlib import Path

import pytest

from osteoquant.io import safe_archive as sa
from osteoquant.io.safe_archive import UnsafeArchive, safe_extract


def _zip(path, members):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for m in members:
            if isinstance(m, zipfile.ZipInfo):
                z.writestr(m, b"x")
            else:
                name, data = m
                z.writestr(name, data)
    return path


def test_valid_zip_extracts_nested_folders(tmp_path):
    z = _zip(tmp_path / "ok.zip", [("a/b/c.txt", b"hello"), ("d.txt", b"x" * 1000), ("e/", b"")])
    out = safe_extract(z, tmp_path / "out")
    assert sorted(Path(p).relative_to(tmp_path / "out").as_posix() for p in out) == ["a/b/c.txt", "d.txt"]
    assert (tmp_path / "out" / "a" / "b" / "c.txt").read_bytes() == b"hello"


@pytest.mark.parametrize("name", ["../evil.txt", "a/../../evil.txt", "/etc/evil", "C:/evil.txt", "C:evil",
                                  "..\\evil.txt", "a\\..\\..\\evil.txt", ""])
def test_zip_path_traversal_rejected(tmp_path, name):
    zi = zipfile.ZipInfo(name or "placeholder")
    if not name:
        zi.filename = ""
    z = tmp_path / "t.zip"
    with zipfile.ZipFile(z, "w") as zf:
        zf.writestr(zi, b"x")
    with pytest.raises(UnsafeArchive):
        safe_extract(z, tmp_path / "out")
    assert not (tmp_path / "evil.txt").exists()


def test_zip_symlink_and_special_files_rejected(tmp_path):
    zi = zipfile.ZipInfo("link")
    zi.external_attr = (stat.S_IFLNK | 0o777) << 16
    with pytest.raises(UnsafeArchive, match="Symlink"):
        safe_extract(_zip(tmp_path / "l.zip", [zi]), tmp_path / "o1")
    fifo = zipfile.ZipInfo("fifo")
    fifo.external_attr = (stat.S_IFIFO | 0o644) << 16
    with pytest.raises(UnsafeArchive, match="Special"):
        safe_extract(_zip(tmp_path / "f.zip", [fifo]), tmp_path / "o2")


def test_zip_member_bomb_ratio(tmp_path):
    z = _zip(tmp_path / "b.zip", [("zeros.bin", b"\0" * (3 * 1024 ** 2))])
    with pytest.raises(UnsafeArchive, match="ratio"):
        safe_extract(z, tmp_path / "out")


def test_zip_many_small_members_aggregate_ratio(tmp_path, monkeypatch):
    # QA-006: each member < 1 MB escapes the per-member ratio test; the whole-archive ratio catches it
    monkeypatch.setattr(sa, "RATIO_MIN_BYTES", 4 * 1024 ** 2)
    z = _zip(tmp_path / "m.zip", [(f"s{i}.bin", b"\0" * 900_000) for i in range(8)])
    with pytest.raises(UnsafeArchive, match="overall compression ratio"):
        safe_extract(z, tmp_path / "out")


def test_zip_total_size_and_file_count_limits(tmp_path):
    z = _zip(tmp_path / "t.zip", [(f"f{i}", b"abc") for i in range(5)])
    with pytest.raises(UnsafeArchive, match="Too many"):
        safe_extract(z, tmp_path / "o1", max_files=4)
    with pytest.raises(UnsafeArchive, match="exceeds"):
        safe_extract(z, tmp_path / "o2", max_total=10)


def test_zip_member_larger_than_declared_size(tmp_path):
    # forge a central directory that under-declares the member size
    raw = io.BytesIO()
    with zipfile.ZipFile(raw, "w", zipfile.ZIP_STORED) as zf:
        zf.writestr("a.bin", b"A" * 5000)
    b = bytearray(raw.getvalue())
    cd = b.rfind(b"PK\x01\x02")
    b[cd + 24:cd + 28] = (100).to_bytes(4, "little")       # uncompressed size in central directory
    p = tmp_path / "lie.zip"
    p.write_bytes(bytes(b))
    with pytest.raises(UnsafeArchive):
        safe_extract(p, tmp_path / "out")


def test_corrupt_member_data_reported_as_unsafe_archive(tmp_path):
    # QA-018: bad CRC / broken deflate stream used to escape as BadZipFile / zlib.error (HTTP 500)
    raw = io.BytesIO()
    with zipfile.ZipFile(raw, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("a.bin", b"hello world" * 100)
    b = bytearray(raw.getvalue())
    b[50] ^= 0xFF
    p = tmp_path / "c.zip"
    p.write_bytes(bytes(b))
    with pytest.raises(UnsafeArchive, match="Corrupt"):
        safe_extract(p, tmp_path / "out")


def test_zip_collisions_rejected_cleanly(tmp_path):
    # QA-007: previously FileExistsError / NotADirectoryError escaped mid-extraction
    with pytest.raises(UnsafeArchive, match="collid|Duplicate"):
        safe_extract(_zip(tmp_path / "c1.zip", [("a", b"1"), ("a/b", b"2")]), tmp_path / "o1")
    with pytest.warns(UserWarning):
        p = _zip(tmp_path / "c2.zip", [("dup", b"1"), ("dup", b"2")])
    with pytest.raises(UnsafeArchive, match="Duplicate"):
        safe_extract(p, tmp_path / "o2")


def test_zip_encrypted_member_rejected(tmp_path):
    raw = io.BytesIO()
    with zipfile.ZipFile(raw, "w") as zf:
        zf.writestr("s.txt", b"secret")
    b = bytearray(raw.getvalue())
    for sig, off in ((b"PK\x03\x04", 6), (b"PK\x01\x02", 8)):     # set the 'encrypted' flag bit
        i = b.find(sig)
        b[i + off] |= 0x1
    p = tmp_path / "enc.zip"
    p.write_bytes(bytes(b))
    with pytest.raises(UnsafeArchive, match="Encrypted"):
        safe_extract(p, tmp_path / "out")


def test_not_an_archive_and_truncated_zip(tmp_path):
    p = tmp_path / "x.zip"
    p.write_bytes(b"not a zip at all")
    with pytest.raises(UnsafeArchive, match="Not a ZIP"):
        safe_extract(p, tmp_path / "o")
    good = _zip(tmp_path / "g.zip", [("a.txt", b"x" * 5000)])
    raw = good.read_bytes()
    p.write_bytes(raw[: len(raw) // 2])
    with pytest.raises(UnsafeArchive):
        safe_extract(p, tmp_path / "o2")


def _tar(path, add):
    with tarfile.open(path, "w") as t:
        add(t)
    return path


def _file(t, name, data=b"x"):
    ti = tarfile.TarInfo(name)
    ti.size = len(data)
    t.addfile(ti, io.BytesIO(data))


def test_tar_rejected_by_default_and_safe_when_allowed(tmp_path):
    p = _tar(tmp_path / "a.tar", lambda t: _file(t, "d/a.txt", b"abc"))
    with pytest.raises(UnsafeArchive, match="TAR"):
        safe_extract(p, tmp_path / "o")
    out = safe_extract(p, tmp_path / "o2", allow_tar=True)
    assert len(out) == 1 and (tmp_path / "o2" / "d" / "a.txt").read_bytes() == b"abc"


@pytest.mark.parametrize("kind", ["sym", "hard", "dev", "fifo", "traversal", "abs"])
def test_tar_links_devices_traversal(tmp_path, kind):
    def add(t):
        if kind in ("traversal", "abs"):
            _file(t, "../x" if kind == "traversal" else "/tmp/x")
            return
        ti = tarfile.TarInfo("evil")
        ti.type = {"sym": tarfile.SYMTYPE, "hard": tarfile.LNKTYPE, "dev": tarfile.CHRTYPE,
                   "fifo": tarfile.FIFOTYPE}[kind]
        ti.linkname = "/etc/passwd"
        t.addfile(ti)
    p = _tar(tmp_path / "e.tar", add)
    with pytest.raises(UnsafeArchive):
        safe_extract(p, tmp_path / "o", allow_tar=True)


def test_tar_limits_and_collisions(tmp_path):
    p = _tar(tmp_path / "m.tar", lambda t: [_file(t, f"f{i}") for i in range(4)])
    with pytest.raises(UnsafeArchive, match="Too many"):
        safe_extract(p, tmp_path / "o1", allow_tar=True, max_files=3)
    with pytest.raises(UnsafeArchive, match="exceeds"):
        safe_extract(p, tmp_path / "o2", allow_tar=True, max_total=2)
    c = _tar(tmp_path / "c.tar", lambda t: (_file(t, "a"), _file(t, "a/b")))
    with pytest.raises(UnsafeArchive):
        safe_extract(c, tmp_path / "o3", allow_tar=True)


def test_tar_directory_members_and_unknown_types(tmp_path):
    def add(t):
        d = tarfile.TarInfo("sub")
        d.type = tarfile.DIRTYPE
        t.addfile(d)
        _file(t, "sub/a.txt", b"ok")
    out = safe_extract(_tar(tmp_path / "d.tar", add), tmp_path / "o", allow_tar=True)
    assert [list(Path(p).relative_to(tmp_path / "o").parts) for p in out] == [["sub", "a.txt"]]

    def odd(t):
        ti = tarfile.TarInfo("weird")
        ti.type = b"Z"                           # unknown member type
        t.addfile(ti)
    with pytest.raises(UnsafeArchive, match="Unsupported member type"):
        safe_extract(_tar(tmp_path / "z.tar", odd), tmp_path / "o2", allow_tar=True)


@pytest.mark.parametrize("kind", ["zip", "tar"])
def test_preexisting_symlink_in_destination_cannot_be_followed(tmp_path, kind):
    import os
    outside = tmp_path / "outside"
    outside.mkdir()
    dest = tmp_path / "dest"
    dest.mkdir()
    try:
        os.symlink(outside, dest / "link")
    except OSError:
        pytest.skip("symlinks not permitted")
    if kind == "zip":
        arc = _zip(tmp_path / "a.zip", [("link/pwn.txt", b"x")])
        with pytest.raises(UnsafeArchive, match="escapes"):
            safe_extract(arc, dest)
    else:
        arc = _tar(tmp_path / "a.tar", lambda t: _file(t, "link/pwn.txt"))
        with pytest.raises(UnsafeArchive, match="escapes"):
            safe_extract(arc, dest, allow_tar=True)
    assert not (outside / "pwn.txt").exists()
