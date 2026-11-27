"""Minimal OLE2 / Compound File Binary writer used to build synthetic Zeiss TXM files for tests.

Version 3 (512-byte sectors, 64-byte mini sectors below the 4096-byte cutoff). Each storage's
children are chained through right-sibling links (all nodes black), which olefile accepts.
Only what ``osteoquant.io.readers.read_txm`` needs is implemented.
"""
from __future__ import annotations

import struct

import numpy as np

SECTOR = 512
MINI = 64
MINI_CUTOFF = 4096
ENDOFCHAIN, FREESECT, FATSECT, NOSTREAM = 0xFFFFFFFE, 0xFFFFFFFF, 0xFFFFFFFD, 0xFFFFFFFF


def _dir_entry(name, typ, child=NOSTREAM, right=NOSTREAM, start=ENDOFCHAIN, size=0):
    n = (name + "\0").encode("utf-16-le")
    e = n.ljust(64, b"\0") + struct.pack("<HBB", len(n), typ, 1)
    e += struct.pack("<III", NOSTREAM, right, child) + b"\0" * 16 + b"\0" * 4 + b"\0" * 16
    e += struct.pack("<IQ", start, size)
    assert len(e) == 128
    return e


def write_cfb(path, streams: dict[str, bytes]):
    """``streams`` maps 'Storage/Stream' (one storage level) or 'Stream' paths to bytes."""
    tree: dict[str, dict[str, bytes]] = {}
    top: dict[str, bytes] = {}
    for k, v in streams.items():
        if "/" in k:
            st, n = k.split("/", 1)
            tree.setdefault(st, {})[n] = v
        else:
            top[k] = v
    # entries: [kind, name, payload/children, right]
    entries: list[list] = [["root", "Root Entry", [], NOSTREAM]]
    for st, kids in tree.items():
        entries.append(["storage", st, [], NOSTREAM])
        si = len(entries) - 1
        for n, b in kids.items():
            entries.append(["stream", n, b, NOSTREAM])
            entries[si][2].append(len(entries) - 1)
        entries[0][2].append(si)
    for n, b in top.items():
        entries.append(["stream", n, b, NOSTREAM])
        entries[0][2].append(len(entries) - 1)

    sectors: list[bytes] = []
    fat: dict[int, int] = {}

    def alloc(blob: bytes, unit=SECTOR) -> int:
        if not blob:
            return ENDOFCHAIN
        first = len(sectors)
        n = -(-len(blob) // SECTOR)
        for j in range(n):
            sectors.append(blob[j * SECTOR:(j + 1) * SECTOR].ljust(SECTOR, b"\0"))
            fat[first + j] = first + j + 1 if j < n - 1 else ENDOFCHAIN
        return first

    # mini stream for small streams
    mini = bytearray()
    minifat: list[int] = []
    loc = {}
    for i, e in enumerate(entries):
        if e[0] != "stream":
            continue
        b = e[2]
        if len(b) < MINI_CUTOFF and b:
            first = len(mini) // MINI
            n = -(-len(b) // MINI)
            mini += b.ljust(n * MINI, b"\0")
            for j in range(n):
                minifat.append(first + j + 1 if j < n - 1 else ENDOFCHAIN)
            loc[i] = (first, len(b))
        elif b:
            loc[i] = (alloc(b), len(b))
        else:
            loc[i] = (ENDOFCHAIN, 0)
    mini_start = alloc(bytes(mini))
    minifat_blob = struct.pack(f"<{len(minifat)}I", *minifat) if minifat else b""
    if minifat:
        minifat += [FREESECT] * ((-len(minifat)) % (SECTOR // 4))
    minifat_blob = struct.pack(f"<{len(minifat)}I", *minifat) if minifat else b""
    minifat_start = alloc(minifat_blob)
    n_minifat = len(minifat_blob) // SECTOR

    for e in entries:   # sibling chains
        kids = e[2] if e[0] in ("root", "storage") else []
        for a, b in zip(kids, kids[1:]):
            entries[a][3] = b
    raw = []
    for i, e in enumerate(entries):
        if e[0] == "root":
            raw.append(_dir_entry(e[1], 5, child=e[2][0] if e[2] else NOSTREAM, start=mini_start, size=len(mini)))
        elif e[0] == "storage":
            raw.append(_dir_entry(e[1], 1, child=e[2][0] if e[2] else NOSTREAM, right=e[3]))
        else:
            st, sz = loc[i]
            raw.append(_dir_entry(e[1], 2, right=e[3], start=st, size=sz))
    dir_blob = b"".join(raw)
    pad = (-len(dir_blob)) % SECTOR
    empty = _dir_entry("", 0)
    dir_blob += (empty * (pad // 128))
    dir_start = alloc(dir_blob)
    n_fat = 1
    while len(sectors) + n_fat > n_fat * (SECTOR // 4):
        n_fat += 1
    fat_start = len(sectors)
    table = [FREESECT] * (n_fat * SECTOR // 4)
    for k, v in fat.items():
        table[k] = v
    for j in range(n_fat):
        table[fat_start + j] = FATSECT
    hdr = bytearray(SECTOR)
    hdr[0:8] = bytes.fromhex("D0CF11E0A1B11AE1")
    struct.pack_into("<HHHHH", hdr, 24, 0x3E, 3, 0xFFFE, 9, 6)
    struct.pack_into("<I", hdr, 44, n_fat)
    struct.pack_into("<I", hdr, 48, dir_start)
    struct.pack_into("<I", hdr, 56, MINI_CUTOFF)
    struct.pack_into("<I", hdr, 60, minifat_start if n_minifat else ENDOFCHAIN)
    struct.pack_into("<I", hdr, 64, n_minifat)
    struct.pack_into("<I", hdr, 68, ENDOFCHAIN)
    struct.pack_into("<I", hdr, 72, 0)
    struct.pack_into("<109I", hdr, 76, *([fat_start + j for j in range(n_fat)] + [FREESECT] * (109 - n_fat)))
    with open(path, "wb") as f:
        f.write(bytes(hdr))
        f.write(b"".join(sectors))
        f.write(struct.pack(f"<{len(table)}I", *table))


def write_txm(path, vol: np.ndarray, pixel_size_um=5.0, data_type=5, n_images=None, drop=(),
              width=None, height=None, extra=None):
    """Write a synthetic TXM volume (z, y, x). ``data_type`` 5=uint16, 10=float32, 3=uint8, 6=int16."""
    z, h, w = vol.shape
    s = {
        "ImageInfo/ImageWidth": struct.pack("<I", width if width is not None else w),
        "ImageInfo/ImageHeight": struct.pack("<I", height if height is not None else h),
        "ImageInfo/NoOfImages": struct.pack("<I", z if n_images is None else n_images),
        "ImageInfo/DataType": struct.pack("<I", data_type),
        "ImageInfo/PixelSize": struct.pack("<f", pixel_size_um),
        "ImageInfo/XrayVoltage": struct.pack("<f", 80.0),
        "ImageInfo/XrayCurrent": struct.pack("<f", 100.0),
        "ReconSettings/Voltage": struct.pack("<f", 80.0),
    }
    for i in range(z):
        if i in drop:
            continue
        s[f"ImageData{i // 100 + 1}/Image{i + 1}"] = np.ascontiguousarray(vol[i]).tobytes()
    s.update(extra or {})
    write_cfb(path, s)
