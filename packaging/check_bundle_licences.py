#!/usr/bin/env python
"""Licence check of a built OsteoQuant Desktop folder.

    python packaging/check_bundle_licences.py [packaging/dist/OsteoQuant] [--report FILE]

1. Lists every shared library (.so/.dylib/.dll, Qt plugins included) with its size.
2. Classifies Qt 6 modules found in library names:
     * FAIL for modules Qt offers only under GPL-3 / commercial terms (not LGPL), e.g. Qt Virtual
       Keyboard, Qt Charts, Qt Data Visualization, Qt Graphs, Qt Quick 3D, Qt Network Authorization,
       Qt HTTP Server, Qt Lottie, Qt Shader Tools, Qt Wayland Compositor, Qt CoAP/MQTT/OPC UA;
     * FAIL for any Qt module not on the reviewed LGPL allow-list (unknown = not shipped until
       reviewed);
3. FAIL if the required notices are missing (THIRD_PARTY_NOTICES.txt, licenses/LGPL-3.0.txt, the PSF licence,
   licenses/BUNDLE_INVENTORY.json), if the inventory lists any library or distribution without a mapped licence,
   or if a bundled system-library package has no copyright file in licenses/system/.
4. Lists non-Python system libraries copied from the build host (informational; review list).

Exit code 0 = pass, 1 = violations. The module classification follows Qt's licensing table
(https://doc.qt.io/qt-6/licensing.html, "Qt modules / tools under GPL or commercial"); re-check
it when upgrading Qt.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Qt 6 modules available under the LGPL-3.0 (reviewed for this application)
LGPL_ALLOW = {
    "Core", "Gui", "Widgets", "OpenGL", "OpenGLWidgets", "DBus", "Network", "Svg", "SvgWidgets", "XcbQpa",
    "WaylandClient", "WaylandEglClientHwIntegration", "EglFSDeviceIntegration", "EglFsKmsSupport", "PrintSupport",
    "Pdf", "PdfWidgets", "Qml", "QmlModels", "QmlMeta", "QmlWorkerScript", "Quick", "Concurrent", "Xml", "Sql",
    "Test", "UiTools", "Help", "Positioning", "WebChannel", "WlShellIntegration",
}
# Qt 6 modules NOT available under the LGPL (GPL-3 or commercial only)
GPL_ONLY = {
    "VirtualKeyboard", "VirtualKeyboardQml", "VirtualKeyboardSettings", "Charts", "ChartsQml", "DataVisualization",
    "DataVisualizationQml", "Graphs", "GraphsWidgets", "Quick3D", "Quick3DRuntimeRender", "Quick3DUtils",
    "Quick3DAssetImport", "Quick3DAssetUtils", "Quick3DEffects", "Quick3DHelpers", "Quick3DParticles",
    "Quick3DPhysics", "Quick3DXr", "Quick3DGlslParser", "NetworkAuth", "HttpServer", "Lottie", "LottieVectorImage",
    "ShaderTools", "WaylandCompositor", "Coap", "Mqtt", "OpcUa", "QuickTimeline", "QuickTimelineBlendTrees",
    "ApplicationManager", "InsightTracker", "CanvasPainter", "LabsStyleKit",
}
QT_LIB_RE = re.compile(r"(?:lib)?Qt6([A-Za-z0-9]+?)(?:\.so|\.dylib|\.dll|$|\.)")
QT_PLUGIN_GPL = {"platforminputcontexts/libqtvirtualkeyboardplugin", "qtvirtualkeyboard"}
LIB_SUFFIX = re.compile(r"\.(so(\.\d+)*|dylib|dll|pyd)$", re.I)


def scan(root: Path) -> dict:
    libs, qt_mods, violations, host_libs = [], {}, [], []
    for f in sorted(root.rglob("*")):
        if not f.is_file() or not LIB_SUFFIX.search(f.name):
            continue
        rel = f.relative_to(root).as_posix()
        libs.append({"path": rel, "bytes": 0 if f.is_symlink() else f.stat().st_size, "symlink": f.is_symlink()})
        low = rel.lower()
        if any(k in low for k in QT_PLUGIN_GPL):
            violations.append(f"GPL-only Qt plugin: {rel}")
        if f.name.startswith(("libQt6", "Qt6")) or "/Qt6" in rel or "Qt6" in f.name:
            m = QT_LIB_RE.search(f.name)
            if m:
                mod = m.group(1)
                qt_mods.setdefault(mod, []).append(rel)
        elif "/" not in rel.replace("_internal/", "", 1) and not rel.endswith((".pyd",)) \
                and ".cpython-" not in f.name and not f.name.startswith(("libpython", "python3")):
            host_libs.append(rel)
    for mod, files in sorted(qt_mods.items()):
        if mod in GPL_ONLY:
            violations += [f"GPL-only Qt module {mod}: {p}" for p in files]
        elif mod not in LGPL_ALLOW:
            violations += [f"Qt module {mod} not on the reviewed LGPL allow-list: {p}" for p in files]
    for need in ("THIRD_PARTY_NOTICES.txt", "licenses/LGPL-3.0.txt", "licenses/GPL-3.0.txt",
                 "licenses/Python-PSF-LICENSE.txt", "licenses/BUNDLE_INVENTORY.json"):
        if not (root / need).exists():
            violations.append(f"missing notice file: {need}")
    inv_p = root / "licenses" / "BUNDLE_INVENTORY.json"
    if inv_p.exists():                       # written by packaging/bundle_inventory.py (review C2-BIZ-08)
        inv = json.loads(inv_p.read_text())
        violations += [f"library or distribution without a mapped licence: {u}" for u in inv.get("unmapped", [])]
        for pkg, info in inv.get("system_packages", {}).items():
            if not info.get("licence_file") or not (root / "licenses" / info["licence_file"]).exists():
                violations.append(f"system library package {pkg} has no licence file in licenses/system/")
    return {"root": str(root), "n_libraries": len(libs), "library_bytes": sum(x["bytes"] for x in libs),
            "qt_modules": sorted(qt_mods), "host_libraries_top_level": host_libs, "violations": violations,
            "libraries": libs}


def ldd_report(root: Path) -> dict:
    """Linux only: resolve every bundled library with ldd (bundle first on the search path).
    Returns libraries resolved from the host system (must be present on target machines) and
    unresolved ones (packaging errors)."""
    import os
    import subprocess
    internal = root / "_internal"
    env = dict(os.environ, LD_LIBRARY_PATH=str(internal))
    from_host, missing = {}, {}
    for f in root.rglob("*"):
        if not f.is_file() or f.is_symlink() or not LIB_SUFFIX.search(f.name):
            continue
        try:
            out = subprocess.run(["ldd", str(f)], capture_output=True, text=True, env=env, timeout=30).stdout
        except (OSError, subprocess.TimeoutExpired):
            continue
        for line in out.splitlines():
            line = line.strip()
            if "=> not found" in line:
                missing.setdefault(line.split()[0], []).append(f.relative_to(root).as_posix())
            elif "=>" in line:
                name, target = line.split("=>")[0].strip(), line.split("=>")[1].split("(")[0].strip()
                if target and not target.startswith(str(root)):
                    from_host.setdefault(name, target)
    return {"from_host": dict(sorted(from_host.items())), "missing": missing}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root", nargs="?", default=str(Path(__file__).resolve().parent / "dist" / "OsteoQuant"))
    ap.add_argument("--report", help="write the full JSON report here")
    ap.add_argument("--ldd", action="store_true", help="Linux: also list host libraries resolved via ldd")
    a = ap.parse_args(argv)
    res = scan(Path(a.root))
    if a.ldd and sys.platform.startswith("linux"):
        res["ldd"] = ldd_report(Path(a.root))
    if a.report:
        Path(a.report).write_text(json.dumps(res, indent=1))
    n_real = sum(not x["symlink"] for x in res["libraries"])
    print(f"shared libraries: {n_real} files + {res['n_libraries'] - n_real} symlinks ({res['library_bytes'] / 2**20:,.0f} MiB)")
    print("Qt modules: " + ", ".join(res["qt_modules"]))
    print(f"top-level libraries in _internal (system libs + links to vendored wheel libs): {len(res['host_libraries_top_level'])}")
    for h in res["host_libraries_top_level"]:
        print("   ", h)
    if "ldd" in res:
        print("libraries expected from the target system (ldd): " + ", ".join(res["ldd"]["from_host"]))
        if res["ldd"]["missing"]:
            print("UNRESOLVED (not in bundle, not on this host): " + ", ".join(res["ldd"]["missing"]))
    if res["violations"]:
        print(f"LICENCE CHECK FAILED ({len(res['violations'])} violations):")
        for v in res["violations"]:
            print("   ", v)
        return 1
    print("LICENCE CHECK PASSED: no GPL-only or unreviewed Qt modules; notices present.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
