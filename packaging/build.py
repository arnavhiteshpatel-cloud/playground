#!/usr/bin/env python
"""Build the OsteoQuant Desktop one-folder application and smoke-test it.

    python packaging/build.py                 # build + licences + self-test + archive
    python packaging/build.py --skip-selftest
    python packaging/build.py --no-archive

Steps
  1. PyInstaller with packaging/osteoquant_desktop.spec -> packaging/dist/OsteoQuant/
     (macOS: packaging/dist/OsteoQuant.app as well)
  2. licences: licenses/ (LGPL/GPL texts + licence files of bundled distributions),
     THIRD_PARTY_NOTICES.txt, then packaging/check_bundle_licences.py (fails on GPL-only Qt modules)
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
    mac_app = DIST / "OsteoQuant.app" / "Contents" / "MacOS" / name
    if sys.platform == "darwin" and mac_app.exists():
        return mac_app            # self-test the app bundle that is shipped, not the intermediate folder
    return app_dir() / name


FIRST_LAUNCH = """OsteoQuant Desktop for macOS (Apple silicon) - research prototype

Install: drag OsteoQuant onto the Applications folder.

First launch: this build is not signed by an Apple-registered developer, so macOS blocks a plain double-click.
  1. In Applications, Control-click (or right-click) OsteoQuant and choose Open, then choose Open again.
  2. If macOS still refuses, open System Settings > Privacy & Security and click "Open Anyway" next to OsteoQuant.
  3. If macOS says the app "is damaged", run this once in Terminal and try again:
       xattr -dr com.apple.quarantine /Applications/OsteoQuant.app

The app runs offline in evaluation mode. It is research software: not validated on real graft materials, not a
medical device, no GLP or 21 CFR Part 11 compliance claimed. Third-party licences: OsteoQuant.app/Contents/Resources
(THIRD_PARTY_NOTICES.txt and licenses/) and Help > About in the app.
"""


def macos_finish() -> dict:
    """Ad-hoc sign the app bundle when no signing identity is configured (Apple silicon refuses to run unsigned arm64
    code, and moving files into the bundle invalidates earlier per-file signatures), then verify the signature."""
    appb = DIST / "OsteoQuant.app"
    if sys.platform != "darwin" or not appb.exists():
        return {}
    res = appb / "Contents" / "Resources"          # licence notices travel inside the shipped bundle
    shutil.copy2(app_dir() / "THIRD_PARTY_NOTICES.txt", res / "THIRD_PARTY_NOTICES.txt")
    shutil.copytree(app_dir() / "licenses", res / "licenses", dirs_exist_ok=True)
    ident = os.environ.get("OQ_CODESIGN_IDENTITY") or "-"
    r = subprocess.run(["codesign", "--force", "--deep", "--sign", ident, str(appb)], capture_output=True, text=True)
    v = subprocess.run(["codesign", "--verify", "--deep", "--strict", "--verbose=2", str(appb)], capture_output=True,
                       text=True)
    print((r.stdout + r.stderr + v.stdout + v.stderr)[-3000:], flush=True)
    return {"identity": "ad-hoc" if ident == "-" else "configured", "sign_exit": r.returncode,
            "verify_exit": v.returncode}


def _provenance() -> dict:
    """Commit and advisor version the bundle was built from (cycle-3 review C3-BIZ-05: a build must say which code
    state it contains)."""
    import re
    import subprocess
    root = Path(__file__).resolve().parents[1]
    out = {}
    try:
        out["git_commit"] = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True,
                                           cwd=root).stdout.strip()
        dirty = subprocess.run(["git", "status", "--porcelain", "--", "osteoquant"], capture_output=True, text=True,
                               cwd=root).stdout.strip()
        out["osteoquant_dirty"] = bool(dirty)
    except OSError:
        pass
    m = re.search(r'ADVISOR_VERSION = "([^"]+)"', (root / "osteoquant" / "advisor" / "separability.py").read_text())
    out["advisor_version"] = m.group(1) if m else None
    return out


def dir_size(p: Path) -> int:
    return sum(f.stat().st_size for f in p.rglob("*") if f.is_file() and not f.is_symlink())


def run_pyinstaller():
    cmd = [sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", "--distpath", str(DIST),
           "--workpath", str(WORK), str(PKG / "osteoquant_desktop.spec")]
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True, cwd=ROOT)


NOTICE_HEAD = """OsteoQuant Desktop - third-party notices
=========================================

This folder contains OsteoQuant Desktop together with third-party open-source components. Each
component remains under its own licence; the licence texts are in the "licenses" folder next to
this file. INDEX.json in that folder lists component, version, declared licence and files.

Qt and Qt for Python (PySide6, shiboken6) - LGPL-3.0
-----------------------------------------------------
This application uses the Qt libraries and Qt for Python under the GNU Lesser General Public
License version 3 (licenses/LGPL-3.0.txt, which incorporates licenses/GPL-3.0.txt). Qt is
Copyright (C) The Qt Company Ltd. and other contributors. Source code of Qt and Qt for Python
is available from https://download.qt.io/official_releases/ and
https://code.qt.io/cgit/pyside/pyside-setup.git/ (versions: see INDEX.json).

Replacing / relinking the LGPL libraries: this is a one-folder build. Qt and PySide6 are NOT
statically linked; they are separate shared libraries in the "_internal" folder (Windows:
_internal\\PySide6\\*.dll and _internal\\PySide6\\Qt*.dll; Linux: _internal/PySide6/Qt/lib/libQt6*.so.6
and _internal/PySide6/*.so; macOS: Contents/Frameworks/PySide6/Qt/lib/Qt*.framework). You may
replace them with modified, ABI-compatible builds of the same Qt / PySide6 version; the
application loads whatever libraries are present in that location. Nothing in the OsteoQuant
licence terms restricts modification of these libraries or reverse engineering for the purpose
of debugging such modifications, as permitted by the LGPL-3.0. Only LGPL-licensed Qt modules are
included; Qt modules offered solely under GPL/commercial terms (e.g. Qt Virtual Keyboard, Qt
Charts, Qt Quick 3D) are excluded and checked by the build (packaging/check_bundle_licences.py).

Other components (summary; full texts in licenses/)
----------------------------------------------------
"""


def write_notices():
    """licenses/ folder (LGPL/GPL texts + licence files of bundled distributions) and
    THIRD_PARTY_NOTICES.txt at the top of the application folder."""
    root = app_dir()
    out = root / "licenses"
    old = root / "THIRD_PARTY_LICENSES"
    if old.exists():
        shutil.rmtree(old)
    out.mkdir(exist_ok=True)
    for f in ("LGPL-3.0.txt", "GPL-3.0.txt"):
        shutil.copyfile(PKG / "licenses" / f, out / f)
    index = []
    for name in LICENSED:
        try:
            dist = md.distribution(name)
        except md.PackageNotFoundError:
            continue
        # match on the whole path: licence files often sit in a dist-info/licenses/ folder under SPDX names
        files = [f for f in (dist.files or []) if any(k in str(f).upper() for k in ("LICEN", "COPYING", "NOTICE"))
                 and not f.name.endswith((".py", ".pyc", ".so", ".dll", ".pyd", ".qml"))]
        meta_lic = dist.metadata.get("License-Expression") or dist.metadata.get("License") or ""
        written = []
        for f in files:
            src = Path(dist.locate_file(f))
            if src.is_file() and src.stat().st_size < 2_000_000:
                tail = str(f).split("/licenses/", 1)[-1].replace("/", "_") if "/licenses/" in str(f) else f.name
                dst = out / f"{dist.metadata['Name']}-{tail}"
                shutil.copyfile(src, dst)
                written.append(dst.name)
        if dist.metadata["Name"].lower().startswith(("pyside6", "shiboken6")):
            written += ["LGPL-3.0.txt", "GPL-3.0.txt"]
        index.append({"name": dist.metadata["Name"], "version": dist.version,
                      "license": meta_lic.splitlines()[0][:120] if meta_lic else "", "files": written})
    (out / "INDEX.json").write_text(json.dumps(index, indent=1))
    lines = [NOTICE_HEAD]
    for e in index:
        lines.append(f"{e['name']} {e['version']}: {e['license'] or 'see licence file'}"
                     + (f"  [{', '.join(e['files'][:3])}]" if e["files"] else ""))
    (root / "THIRD_PARTY_NOTICES.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    # system libraries, Python runtime (PSF), Qt third-party code, PDFium; SBOM of the built bundle (C2-BIZ-08/-10)
    r = subprocess.run([sys.executable, str(PKG / "bundle_inventory.py"), str(root), "--sbom-dir",
                        str(ROOT / "docs" / "security")], capture_output=True, text=True)
    print(r.stdout, flush=True)
    if r.returncode != 0:
        raise SystemExit("bundle inventory FAILED: a bundled library has no mapped licence (see output above)")
    return index


def check_licences() -> dict:
    r = subprocess.run([sys.executable, str(PKG / "check_bundle_licences.py"), str(app_dir()),
                        "--report", str(DIST / "licence-check.json")]
                       + (["--ldd"] if sys.platform.startswith("linux") else []), capture_output=True, text=True)
    (DIST / "licence-check.txt").write_text(r.stdout)
    print(r.stdout, flush=True)
    return {"exit_code": r.returncode}


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
        # ditto keeps the framework symlinks, permissions and signature that a Python zip would break
        out = base.with_suffix(".zip")
        out.unlink(missing_ok=True)
        subprocess.run(["ditto", "-c", "-k", "--sequesterRsrc", "--keepParent", str(DIST / "OsteoQuant.app"), str(out)],
                       check=True)
        return out
    return Path(shutil.make_archive(str(base), "gztar", DIST, "OsteoQuant"))


def macos_dmg() -> Path | None:
    """Drag-to-Applications disk image with first-launch instructions for the unsigned build."""
    appb = DIST / "OsteoQuant.app"
    if sys.platform != "darwin" or not appb.exists():
        return None
    stage = DIST / "dmg-stage"
    shutil.rmtree(stage, ignore_errors=True)
    stage.mkdir()
    subprocess.run(["ditto", str(appb), str(stage / "OsteoQuant.app")], check=True)
    (stage / "Applications").symlink_to("/Applications")
    (stage / "READ ME FIRST.txt").write_text(FIRST_LAUNCH)
    out = DIST / f"OsteoQuant-desktop-macos-{platform.machine().lower()}.dmg"
    out.unlink(missing_ok=True)
    subprocess.run(["hdiutil", "create", "-volname", "OsteoQuant", "-srcfolder", str(stage), "-ov", "-format", "UDZO",
                    str(out)], check=True)
    shutil.rmtree(stage, ignore_errors=True)
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--skip-build", action="store_true")
    ap.add_argument("--skip-selftest", action="store_true")
    ap.add_argument("--no-archive", action="store_true")
    a = ap.parse_args(argv)
    if not a.skip_build:
        run_pyinstaller()
    lic = write_notices()
    info_lic = check_licences()
    info = {"platform": platform.platform(), "python": platform.python_version(), "machine": platform.machine(),
            "bundle_torch": os.environ.get("OQ_BUNDLE_TORCH", "0") == "1",
            "bundle_simpleitk": os.environ.get("OQ_BUNDLE_SITK", "0") == "1",
            "size_bytes": dir_size(app_dir()), "licence_files": sum(len(x["files"]) for x in lic),
            "licence_check": info_lic, **_provenance()}
    print(f"bundle size: {info['size_bytes'] / 2**20:,.0f} MiB", flush=True)
    rc = 0 if info_lic["exit_code"] == 0 else 2
    if rc:
        print("licence check FAILED: see packaging/dist/licence-check.txt", flush=True)
    mac = macos_finish()
    if mac:
        info["macos_signature"] = mac
        if mac["sign_exit"] or mac["verify_exit"]:
            rc = rc or 3
            print("macOS code signature FAILED", flush=True)
    if not a.skip_selftest and rc == 0:
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
        dmg = macos_dmg()
        if dmg:
            info["dmg"] = dmg.name
            info["dmg_bytes"] = dmg.stat().st_size
            print(f"disk image: {dmg} ({dmg.stat().st_size / 2**20:,.0f} MiB)", flush=True)
    (DIST / "build-info.json").write_text(json.dumps(info, indent=1))
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
