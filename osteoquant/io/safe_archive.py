"""Safe extraction of uploaded archives (ZIP / TAR) containing slice stacks or DICOM series.

Defends against: path traversal ("../", absolute paths, drive letters), symlinks/hardlinks,
device files, zip bombs (total uncompressed size and compression-ratio limits), excessive file
counts, and nested archives (not extracted).
"""
from __future__ import annotations

import os
import tarfile
import zipfile
import zlib
from pathlib import Path, PurePosixPath

MAX_FILES = 20000
MAX_TOTAL_BYTES = 16 * 1024 ** 3     # 16 GB uncompressed
MAX_RATIO = 200                       # per-member compression ratio
MAX_TOTAL_RATIO = 200                 # whole-archive ratio (many small highly compressed members, QA-006)
RATIO_MIN_BYTES = 64 * 1024 ** 2      # ratio limits apply once this much would be extracted


class UnsafeArchive(ValueError):
    pass


def _safe_name(name: str) -> str:
    n = name.replace("\\", "/")
    p = PurePosixPath(n)
    if p.is_absolute() or any(part == ".." for part in p.parts) or (len(n) > 1 and n[1] == ":"):
        raise UnsafeArchive(f"Unsafe path in archive: {name!r}")
    return str(p)


def _prepare_target(target: Path, member: str) -> None:
    """Create parent folders; a member that collides with an extracted file/folder (e.g. 'a' and
    'a/b', or a duplicate name) is rejected instead of raising an OS error mid-extraction (QA-007)."""
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
    except (FileExistsError, NotADirectoryError) as e:
        raise UnsafeArchive(f"Member path collides with another member: {member}") from e
    if target.exists():
        raise UnsafeArchive(f"Duplicate or colliding member in archive: {member}")


def safe_extract(archive: str | os.PathLike, dest: str | os.PathLike, max_total=MAX_TOTAL_BYTES,
                 max_files=MAX_FILES, allow_tar: bool = False) -> list[str]:
    """Extract ``archive`` into ``dest`` or raise ``UnsafeArchive`` (a ValueError). Corrupt archives
    (bad CRC, truncated deflate stream, unsupported compression) are reported as ``UnsafeArchive``
    too, never as library-specific exceptions (QA-018)."""
    try:
        return _extract(archive, dest, max_total, max_files, allow_tar)
    except UnsafeArchive:
        raise
    except (zipfile.BadZipFile, zlib.error, EOFError, tarfile.TarError, NotImplementedError, RuntimeError) as e:
        raise UnsafeArchive(f"Corrupt or unsupported archive: {type(e).__name__}: {e}") from e


def _extract(archive, dest, max_total, max_files, allow_tar) -> list[str]:
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
            packed = sum(i.compress_size for i in infos)
            if total > RATIO_MIN_BYTES and total / max(packed, 1) > MAX_TOTAL_RATIO:
                raise UnsafeArchive(f"Suspicious overall compression ratio ({total / max(packed, 1):.0f}:1)")
            for i in infos:
                name = _safe_name(i.filename)
                if i.is_dir():
                    continue
                if i.flag_bits & 0x1:
                    raise UnsafeArchive(f"Encrypted member not supported: {i.filename}")
                mode = (i.external_attr >> 16) & 0o170000
                if mode == 0o120000:
                    raise UnsafeArchive(f"Symlink in archive: {i.filename}")
                if mode and mode not in (0o100000, 0o040000):
                    raise UnsafeArchive(f"Special file in archive: {i.filename}")
                if i.compress_size and i.file_size / max(i.compress_size, 1) > MAX_RATIO and i.file_size > 1e6:
                    raise UnsafeArchive(f"Suspicious compression ratio for {i.filename}")
                target = (dest / name).resolve()
                if not str(target).startswith(str(dest) + os.sep):
                    raise UnsafeArchive(f"Path escapes destination: {i.filename}")
                _prepare_target(target, i.filename)
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
                if not m.isfile():
                    raise UnsafeArchive(f"Unsupported member type in archive: {m.name}")
                target = (dest / name).resolve()
                if not str(target).startswith(str(dest) + os.sep):
                    raise UnsafeArchive(f"Path escapes destination: {m.name}")
                _prepare_target(target, m.name)
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
