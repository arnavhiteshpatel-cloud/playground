#!/usr/bin/env python
"""Render the application icon (PNG, ICO, ICNS) with QPainter + Pillow. Run once after a
design change; the outputs are committed in packaging/icons/ and osteoquant/desktop/resources/."""
import os
import sys
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from PIL import Image  # noqa: E402
from PySide6.QtCore import QPointF, QRectF, Qt  # noqa: E402
from PySide6.QtGui import QColor, QGuiApplication, QImage, QPainter, QPen  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def render(n=1024) -> QImage:
    img = QImage(n, n, QImage.Format_ARGB32_Premultiplied)
    img.fill(Qt.transparent)
    p = QPainter(img)
    p.setRenderHint(QPainter.Antialiasing)
    p.setPen(Qt.NoPen)
    p.setBrush(QColor("#1f3a52"))
    p.drawRoundedRect(QRectF(n * 0.06, n * 0.06, n * 0.88, n * 0.88), n * 0.2, n * 0.2)
    c = QPointF(n / 2, n / 2)
    p.setPen(QPen(QColor("#d9dde2"), n * 0.075))           # cortical ring
    p.setBrush(Qt.NoBrush)
    p.drawEllipse(c, n * 0.30, n * 0.30)
    p.setPen(Qt.NoPen)
    p.setBrush(QColor("#e69f00"))                           # new bone (label colour)
    for dx, dy, r in ((-0.09, -0.07, 0.07), (0.08, -0.1, 0.05), (0.1, 0.07, 0.065), (-0.06, 0.1, 0.05)):
        p.drawEllipse(QPointF(c.x() + dx * n, c.y() + dy * n), r * n, r * n)
    p.setBrush(QColor("#56b4e9"))                           # residual graft
    p.drawEllipse(c, n * 0.06, n * 0.06)
    p.end()
    return img


def main():
    QGuiApplication(sys.argv)
    out = ROOT / "packaging" / "icons"
    out.mkdir(parents=True, exist_ok=True)
    png = out / "osteoquant.png"
    render(1024).save(str(png))
    res = ROOT / "osteoquant" / "desktop" / "resources"
    res.mkdir(parents=True, exist_ok=True)
    render(256).save(str(res / "osteoquant.png"))
    im = Image.open(png)
    im.save(out / "osteoquant.ico", sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    im.save(out / "osteoquant.icns")
    print("icons written to", out)


if __name__ == "__main__":
    main()
