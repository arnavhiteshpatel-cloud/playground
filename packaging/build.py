#!/usr/bin/env python
"""Build the OsteoQuant Desktop one-folder application and smoke-test it.

    python packaging/build.py                 # build + licences + self-test + archive
    python packaging/build.py --skip-selftest
    python packaging/build.py --no-archive

Steps
  1. PyInstaller with packaging/osteoquant_desktop.spec -> packaging/dist/OsteoQuant/
     (macOS: packaging/dist/OsteoQuant.app as well)
  2. copy licence texts of bundled third-party distributions to THIRD_PARTY_LICENSES/
  3. run the packaged console executable with --selftest (headless) and fail on non-zero exit
  4. write build-info.json (size, platform, selftest result) and an archive for CI upload

Code signing / notarisation are NOT done here; they need the publisher's certificates. See
docs/desktop/PACKAGING.md.
"""
from __future__ import annotations

import argparse
import importlib.metadata as md
import json
import os
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "packaging"
DIST = PKG / "dist"
WORK = PKG / "build"

LICENSED = ["PySide6", "PySide6_Essentials", "PySide6_Addons", "shiboken6", "vtk", "numpy", "scipy", "scikit-image",
            "scikit-learn", "zarr", "numcodecs", "SimpleITK", "pydicom", "nibabel", "pynrrd", "tifffile", "imagecodecs",
            "olefile", "reportlab", "matplotlib", "pandas", "statsmodels", "cryptography", "psutil", "pillow",
            "fastapi", "starlette", "pydantic", "pydantic_core", "joblib", "threadpoolctl", "pypdfium2",
            "onnxruntime", "PyYAML", "openpyxl", "networkx", "imageio", "lazy_loader", "packaging", "contourpy",
            "kiwisolver", "fonttools", "cycler", "pyparsing", "python-dateutil", "pytz", "tzdata", "six", "patsy",
            "cffi", "pycparser", "anyio", "sniffio", "idna", "typing_extensions", "annotated-types", "crc32c",
            "donfig", "google-crc32c"]


def app_dir() -> Path:
    return DIST / "OsteoQuant"


def console_exe() -> Path:
    name = "osteoquant-desktop-console" + (".exe" if sys.platform.startswith("win") else "")
    return app_dir() / name


def dir_size(p: Path) -> int:
    return sum(f.stat().st_size for f in p.rglob("*") if f.is_file() and not f.is_symlink())


def run_pyinstaller():
    cmd = [sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", "--distpath", str(DIST),
           "--workpath", str(WORK), str(PKG / "osteoquant_desktop.spec")]
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True, cwd=ROOT)


def copy_licences():
    out = app_dir() / "THIRD_PARTY_LICENSES"
    out.mkdir(exist_ok=True)
    index = []
    for name in LICENSED:
        try:
            dist = md.distribution(name)
        except md.PackageNotFoundError:
            continue
        files = [f for f in (dist.files or []) if any(k in f.name.upper() for k in ("LICEN", "COPYING", "NOTICE"))]
        meta_lic = dist.metadata.get("License-Expression") or dist.metadata.get("License") or ""
        written = []
        for f in files:
            src = Path(dist.locate_file(f))
            if src.is_file():
                dst = out / f"{dist.metadata['Name']}-{f.name}"
                shutil.copyfile(src, dst)
                written.append(dst.name)
        index.append({"name": dist.metadata["Name"], "version": dist.version, "license": meta_lic.splitlines()[0][:120]
                      if meta_lic else "", "files": written})
    (out / "INDEX.json").write_text(json.dumps(index, indent=1))
    (out / "README.txt").write_text(
        "Licence texts of third-party components bundled with OsteoQuant Desktop.\n"
        "Qt / PySide6 are used under the GNU LGPL v3 as dynamically linked libraries; the Qt\n"
        "libraries in this folder's parent directory can be replaced by the user with compatible\n"
        "builds. Source code of Qt is available from https://download.qt.io/ .\n")
    return index


def run_selftest(out: Path) -> dict:
    env = dict(os.environ, QT_QPA_PLATFORM="offscreen")
    env.pop("PYTHONPATH", None)
    t = time.time()
    r = subprocess.run([str(console_exe()), "--selftest", "--selftest-out", str(out)], capture_output=True, text=True,
                       env=env, timeout=1800, cwd=str(out))
    print(r.stdout[-6000:], flush=True)
    if r.returncode != 0:
        print(r.stderr[-6000:], file=sys.stderr)
    return {"exit_code": r.returncode, "seconds": round(time.time() - t, 1)}


def archive() -> Path:
    plat = {"win32": "windows", "darwin": "macos"}.get(sys.platform, "linux")
    base = DIST / f"OsteoQuant-desktop-{plat}-{platform.machine().lower()}"
    if sys.platform.startswith("win"):
        return Path(shutil.make_archive(str(base), "zip", DIST, "OsteoQuant"))
    if sys.platform == "darwin" and (DIST / "OsteoQuant.app").exists():
        return Path(shutil.make_archive(str(base), "zip", DIST, "OsteoQuant.app"))
    return Path(shutil.make_archive(str(base), "gztar", DIST, "OsteoQuant"))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--skip-build", action="store_true")
    ap.add_argument("--skip-selftest", action="store_true")
    ap.add_argument("--no-archive", action="store_true")
    a = ap.parse_args(argv)
    if not a.skip_build:
        run_pyinstaller()
    lic = copy_licences()
    info = {"platform": platform.platform(), "python": platform.python_version(), "machine": platform.machine(),
            "bundle_torch": os.environ.get("OQ_BUNDLE_TORCH", "0") == "1",
            "bundle_simpleitk": os.environ.get("OQ_BUNDLE_SITK", "0") == "1",
            "size_bytes": dir_size(app_dir()), "licence_files": sum(len(x["files"]) for x in lic)}
    print(f"bundle size: {info['size_bytes'] / 2**20:,.0f} MiB", flush=True)
    rc = 0
    if not a.skip_selftest:
        st_out = PKG / "selftest-output"
        shutil.rmtree(st_out, ignore_errors=True)
        st_out.mkdir(parents=True)
        info["selftest"] = run_selftest(st_out)
        rc = info["selftest"]["exit_code"]
        print("packaged self-test:", "PASS" if rc == 0 else f"FAIL (exit {rc})", flush=True)
    if not a.no_archive and rc == 0:
        arc = archive()
        info["archive"] = arc.name
        info["archive_bytes"] = arc.stat().st_size
        print(f"archive: {arc} ({arc.stat().st_size / 2**20:,.0f} MiB)", flush=True)
    (DIST / "build-info.json").write_text(json.dumps(info, indent=1))
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
