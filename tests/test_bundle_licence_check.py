"""Bundle licence check recognises macOS frameworks and PySide modules and never passes vacuously (C3-PRD-10)."""
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _checker():
    spec = importlib.util.spec_from_file_location("cbl", ROOT / "packaging" / "check_bundle_licences.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _touch(root: Path, rel: str):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(b"\0")


def _notices(root: Path):
    for rel in ("THIRD_PARTY_NOTICES.txt", "licenses/LGPL-3.0.txt", "licenses/GPL-3.0.txt",
                "licenses/Python-PSF-LICENSE.txt"):
        _touch(root, rel)


def test_macos_framework_layout_detects_gpl_module(tmp_path):
    cbl = _checker()
    for fw in ("QtCore", "QtGui", "QtCharts"):
        _touch(tmp_path, f"Contents/Frameworks/PySide6/Qt/lib/{fw}.framework/Versions/A/{fw}")
    _touch(tmp_path, "Contents/Frameworks/PySide6/QtCharts.abi3.so")
    _notices(tmp_path)
    res = cbl.scan(tmp_path)
    assert "Core" in res["qt_modules"] and "Charts" in res["qt_modules"]
    assert any("Charts" in v for v in res["violations"])


def test_layout_without_qt_core_never_passes(tmp_path):
    cbl = _checker()
    _touch(tmp_path, "_internal/libsomething.so")
    _notices(tmp_path)
    res = cbl.scan(tmp_path)
    assert any("no Qt Core module detected" in v for v in res["violations"])


def test_local_linux_bundle_still_passes_if_present():
    root = ROOT / "packaging" / "dist" / "OsteoQuant"
    if not root.exists():
        pytest.skip("no local bundle")
    res = _checker().scan(root)
    assert not [v for v in res["violations"] if "Qt" in v], res["violations"][:5]
