"""Safe extraction of uploaded archives (ZIP / TAR) containing slice stacks or DICOM series.

Defends against: path traversal ("../", absolute paths, drive letters), symlinks/hardlinks,
device files, zip bombs (total uncompressed size and compression-ratio limits), excessive file
counts, and nested archives (not extracted).
"""
from __future__ import annotations

import os
import tarfile
import zipfile
from pathlib import Path, PurePosixPath

MAX_FILES = 20000
MAX_TOTAL_BYTES = 16 * 1024 ** 3     # 16 GB uncompressed
MAX_RATIO = 200                       # per-member compression ratio


class UnsafeArchive(ValueError):
    pass


def _safe_name(name: str) -> str:
    n = name.replace("\\", "/")
    p = PurePosixPath(n)
    if p.is_absolute() or any(part == ".." for part in p.parts) or (len(n) > 1 and n[1] == ":"):
        raise UnsafeArchive(f"Unsafe path in archive: {name!r}")
    return str(p)


def safe_extract(archive: str | os.PathLike, dest: str | os.PathLike, max_total=MAX_TOTAL_BYTES,
                 max_files=MAX_FILES, allow_tar: bool = False) -> list[str]:
    dest = Path(dest).resolve()
    dest.mkdir(parents=True, exist_ok=True)
    out = []
    total_written = 0
    a = str(archive)
    if zipfile.is_zipfile(a):
        with zipfile.ZipFile(a) as z:
            infos = z.infolist()
            if len(infos) > max_files:
                raise UnsafeArchive(f"Too many files ({len(infos)})")
            total = sum(i.file_size for i in infos)
            if total > max_total:
                raise UnsafeArchive(f"Uncompressed size {total} exceeds limit")
            for i in infos:
                name = _safe_name(i.filename)
                if i.is_dir():
                    continue
                mode = (i.external_attr >> 16) & 0o170000
                if mode == 0o120000:
                    raise UnsafeArchive(f"Symlink in archive: {i.filename}")
                if i.compress_size and i.file_size / max(i.compress_size, 1) > MAX_RATIO and i.file_size > 1e6:
                    raise UnsafeArchive(f"Suspicious compression ratio for {i.filename}")
                target = (dest / name).resolve()
                if not str(target).startswith(str(dest) + os.sep):
                    raise UnsafeArchive(f"Path escapes destination: {i.filename}")
                target.parent.mkdir(parents=True, exist_ok=True)
                written = 0
                with z.open(i) as src, open(target, "wb") as dst:
                    while True:
                        b = src.read(1 << 20)
                        if not b:
                            break
                        written += len(b)
                        total_written += len(b)
                        if written > i.file_size + 1024:
                            raise UnsafeArchive("Member larger than declared size")
                        if total_written > max_total:
                            raise UnsafeArchive("Total extracted size exceeds limit")
                        dst.write(b)
                out.append(str(target))
    elif tarfile.is_tarfile(a) and not allow_tar:
        raise UnsafeArchive("TAR archives are not accepted; upload a ZIP")
    elif tarfile.is_tarfile(a):
        with tarfile.open(a) as t:
            members = t.getmembers()
            if len(members) > max_files:
                raise UnsafeArchive("Too many files")
            if sum(m.size for m in members) > max_total:
                raise UnsafeArchive("Uncompressed size exceeds limit")
            for m in members:
                name = _safe_name(m.name)
                if m.issym() or m.islnk() or m.isdev() or m.isfifo():
                    raise UnsafeArchive(f"Link/device in archive: {m.name}")
                if m.isdir():
                    continue
                target = (dest / name).resolve()
                if not str(target).startswith(str(dest) + os.sep):
                    raise UnsafeArchive(f"Path escapes destination: {m.name}")
                target.parent.mkdir(parents=True, exist_ok=True)
                f = t.extractfile(m)
                written = 0
                with open(target, "wb") as dst:
                    while True:
                        b = f.read(1 << 20)
                        if not b:
                            break
                        written += len(b)
                        if written > m.size:
                            raise UnsafeArchive("Member larger than declared size")
                        dst.write(b)
                out.append(str(target))
    else:
        raise UnsafeArchive("Not a ZIP or TAR archive")
    return out
