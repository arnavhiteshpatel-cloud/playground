"""Crisp line icons drawn at runtime with Pillow.

Drawing the icons in code keeps the project free of third-party icon licences and
lets every icon be tinted with the application palette. Icons are rendered at a
high resolution and down-sampled by CustomTkinter, so they stay sharp on HiDPI
displays.
"""

from __future__ import annotations

import math
from functools import lru_cache
from typing import Callable

from PIL import Image, ImageDraw

S = 128  # drawing canvas size
W = 10   # default stroke width


def _rr(d: ImageDraw.ImageDraw, box, r, color, width=W, fill=None):
    d.rounded_rectangle(box, radius=r, outline=color, width=width, fill=fill)


def _line(d, pts, color, width=W):
    d.line(pts, fill=color, width=width, joint="curve")
    for x, y in (pts[0], pts[-1]):
        d.ellipse((x - width / 2, y - width / 2, x + width / 2, y + width / 2), fill=color)


def _dashboard(d, c):
    for x, y in ((18, 18), (70, 18), (18, 70), (70, 70)):
        _rr(d, (x, y, x + 40, y + 40), 10, c)


def _camera(d, c):
    _rr(d, (12, 36, 116, 106), 16, c)
    d.polygon([(44, 36), (52, 22), (76, 22), (84, 36)], outline=c, fill=None, width=W)
    d.line([(44, 36), (52, 22), (76, 22), (84, 36)], fill=c, width=W, joint="curve")
    d.ellipse((42, 48, 86, 92), outline=c, width=W)


def _camera_off(d, c):
    _camera(d, c)
    _line(d, [(16, 16), (112, 112)], c)


def _survey(d, c):
    _rr(d, (24, 20, 104, 116), 14, c)
    _rr(d, (44, 10, 84, 32), 8, c, fill=None)
    for y in (56, 76, 96):
        _line(d, [(44, y), (84, y)], c, width=8)


def _chart(d, c):
    _line(d, [(16, 16), (16, 112), (112, 112)], c)
    _line(d, [(32, 88), (56, 60), (76, 74), (108, 34)], c)


def _history(d, c):
    d.arc((14, 14, 114, 114), start=-200, end=150, fill=c, width=W)
    d.polygon([(6, 58), (30, 58), (16, 80)], fill=c)
    _line(d, [(64, 38), (64, 66), (84, 80)], c)


def _profile(d, c):
    d.ellipse((40, 14, 88, 62), outline=c, width=W)
    d.arc((18, 72, 110, 166), start=180, end=360, fill=c, width=W)


def _settings(d, c):
    cx = cy = 64
    teeth = 8
    pts = []
    for i in range(teeth * 4):
        a = 2 * math.pi * i / (teeth * 4)
        r = 52 if (i % 4) in (0, 1) else 40
        pts.append((cx + r * math.cos(a + 0.2), cy + r * math.sin(a + 0.2)))
    d.line(pts + [pts[0]], fill=c, width=W - 1, joint="curve")
    d.ellipse((46, 46, 82, 82), outline=c, width=W)


def _about(d, c):
    d.ellipse((12, 12, 116, 116), outline=c, width=W)
    d.ellipse((58, 32, 70, 44), fill=c)
    _line(d, [(64, 58), (64, 94)], c)


def _check(d, c):
    _line(d, [(22, 66), (52, 94), (106, 36)], c, width=14)


def _close(d, c):
    _line(d, [(28, 28), (100, 100)], c, width=12)
    _line(d, [(100, 28), (28, 100)], c, width=12)


def _chevron_left(d, c):
    _line(d, [(80, 22), (40, 64), (80, 106)], c, width=12)


def _chevron_right(d, c):
    _line(d, [(48, 22), (88, 64), (48, 106)], c, width=12)


def _trash(d, c):
    _line(d, [(16, 32), (112, 32)], c)
    _rr(d, (46, 12, 82, 32), 6, c)
    d.line([(28, 32), (36, 114), (92, 114), (100, 32)], fill=c, width=W, joint="curve")
    _line(d, [(54, 54), (54, 94)], c, width=8)
    _line(d, [(74, 54), (74, 94)], c, width=8)


def _download(d, c):
    _line(d, [(64, 14), (64, 82)], c)
    _line(d, [(36, 56), (64, 84), (92, 56)], c)
    _line(d, [(16, 92), (16, 112), (112, 112), (112, 92)], c)


def _calendar(d, c):
    _rr(d, (14, 24, 114, 114), 14, c)
    _line(d, [(14, 52), (114, 52)], c)
    _line(d, [(40, 12), (40, 34)], c)
    _line(d, [(88, 12), (88, 34)], c)


def _pulse(d, c):
    _line(d, [(8, 68), (36, 68), (50, 34), (70, 100), (86, 54), (94, 68), (120, 68)], c)


def _clock(d, c):
    d.ellipse((12, 12, 116, 116), outline=c, width=W)
    _line(d, [(64, 34), (64, 66), (86, 80)], c)


def _shield(d, c):
    d.line([(64, 10), (110, 28), (106, 70), (64, 118), (22, 70), (18, 28), (64, 10)],
           fill=c, width=W, joint="curve")
    _line(d, [(44, 64), (58, 80), (86, 48)], c)


def _refresh(d, c):
    d.arc((16, 16, 112, 112), start=30, end=320, fill=c, width=W)
    d.polygon([(118, 22), (114, 62), (80, 44)], fill=c)


def _face(d, c):
    d.ellipse((14, 8, 114, 120), outline=c, width=W)
    d.ellipse((38, 46, 50, 58), fill=c)
    d.ellipse((78, 46, 90, 58), fill=c)
    d.arc((40, 56, 88, 98), start=20, end=160, fill=c, width=W)


def _plus(d, c):
    _line(d, [(64, 20), (64, 108)], c, width=12)
    _line(d, [(20, 64), (108, 64)], c, width=12)


def _eye(d, c):
    d.arc((8, 30, 120, 150), start=200, end=340, fill=c, width=W)
    d.arc((8, -22, 120, 98), start=20, end=160, fill=c, width=W)
    d.ellipse((46, 44, 82, 80), outline=c, width=W)


def _lock(d, c):
    _rr(d, (22, 56, 106, 116), 12, c)
    d.arc((38, 18, 90, 76), start=180, end=360, fill=c, width=W)
    _line(d, [(38, 46), (38, 58)], c)
    _line(d, [(90, 46), (90, 58)], c)


def _folder(d, c):
    d.line([(12, 30), (50, 30), (60, 42), (116, 42), (116, 106), (12, 106), (12, 30)],
           fill=c, width=W, joint="curve")


def _skip(d, c):
    _line(d, [(24, 24), (72, 64), (24, 104)], c, width=12)
    _line(d, [(100, 24), (100, 104)], c, width=12)


def _record(d, c):
    d.ellipse((24, 24, 104, 104), fill=c)


def _warning(d, c):
    d.line([(64, 12), (120, 112), (8, 112), (64, 12)], fill=c, width=W, joint="curve")
    _line(d, [(64, 46), (64, 78)], c)
    d.ellipse((58, 90, 70, 102), fill=c)


_DRAWERS: dict[str, Callable] = {
    "dashboard": _dashboard, "camera": _camera, "camera_off": _camera_off,
    "survey": _survey, "chart": _chart, "history": _history, "profile": _profile,
    "settings": _settings, "about": _about, "check": _check, "close": _close,
    "chevron_left": _chevron_left, "chevron_right": _chevron_right, "trash": _trash,
    "download": _download, "calendar": _calendar, "pulse": _pulse, "clock": _clock,
    "shield": _shield, "refresh": _refresh, "face": _face, "plus": _plus, "eye": _eye,
    "lock": _lock, "folder": _folder, "skip": _skip, "record": _record,
    "warning": _warning,
}


def available_icons() -> list[str]:
    return sorted(_DRAWERS)


@lru_cache(maxsize=256)
def icon_image(name: str, color: str = "#FFFFFF", size: int = 64) -> Image.Image:
    """Return an RGBA Pillow image of the named icon in ``color``."""
    drawer = _DRAWERS.get(name)
    big = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    if drawer is not None:
        drawer(ImageDraw.Draw(big), color)
    return big.resize((size, size), Image.LANCZOS)


def _hex(c: str) -> tuple[int, int, int]:
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


@lru_cache(maxsize=8)
def logo_image(size: int = 256) -> Image.Image:
    """App mark: blue→teal rounded tile with a stylised face contour and pulse line."""
    n = 512
    top, bottom = _hex("#3B82F6"), _hex("#14B8A6")
    grad = Image.new("RGBA", (n, n))
    px = grad.load()
    for y in range(n):
        for x in range(n):
            t = (x + y) / (2 * n)
            px[x, y] = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)) + (255,)
    mask = Image.new("L", (n, n), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, n - 1, n - 1), radius=120, fill=255)
    tile = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    tile.paste(grad, (0, 0), mask)
    d = ImageDraw.Draw(tile)
    white = (255, 255, 255, 255)
    soft = (255, 255, 255, 150)
    # face contour (open arc so it reads as a profile of a face rather than a circle)
    d.arc((116, 70, 396, 420), start=-60, end=240, fill=soft, width=26)
    # landmark dots
    for x, y in ((196, 210), (316, 210), (256, 262)):
        d.ellipse((x - 16, y - 16, x + 16, y + 16), fill=white)
    # pulse line across the lower face
    pts = [(70, 330), (186, 330), (216, 290), (250, 372), (282, 300), (306, 330), (442, 330)]
    d.line(pts, fill=white, width=26, joint="curve")
    for x, y in (pts[0], pts[-1]):
        d.ellipse((x - 13, y - 13, x + 13, y + 13), fill=white)
    return tile.resize((size, size), Image.LANCZOS)


def write_icon_files(png_path, ico_path) -> None:
    """Write the application icon to disk (used for the window icon)."""
    img = logo_image(256)
    img.save(png_path)
    img.save(ico_path, sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
