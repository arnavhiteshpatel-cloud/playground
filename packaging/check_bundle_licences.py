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
3. FAIL if the required notices are missing (THIRD_PARTY_NOTICES.txt, licenses/LGPL-3.0.txt).
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
    for need in ("THIRD_PARTY_NOTICES.txt", "licenses/LGPL-3.0.txt", "licenses/GPL-3.0.txt"):
        if not (root / need).exists():
            violations.append(f"missing notice file: {need}")
    return {"root": str(root), "n_libraries": len(libs), "library_bytes": sum(x["bytes"] for x in libs),
            "qt_modules": sorted(qt_mods), "host_libraries_top_level": host_libs, "violations": violations,
            "libraries": libs}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root", nargs="?", default=str(Path(__file__).resolve().parent / "dist" / "OsteoQuant"))
    ap.add_argument("--report", help="write the full JSON report here")
    a = ap.parse_args(argv)
    res = scan(Path(a.root))
    if a.report:
        Path(a.report).write_text(json.dumps(res, indent=1))
    n_real = sum(not x["symlink"] for x in res["libraries"])
    print(f"shared libraries: {n_real} files + {res['n_libraries'] - n_real} symlinks ({res['library_bytes'] / 2**20:,.0f} MiB)")
    print("Qt modules: " + ", ".join(res["qt_modules"]))
    print(f"top-level host libraries: {len(res['host_libraries_top_level'])}")
    for h in res["host_libraries_top_level"]:
        print("   ", h)
    if res["violations"]:
        print(f"LICENCE CHECK FAILED ({len(res['violations'])} violations):")
        for v in res["violations"]:
            print("   ", v)
        return 1
    print("LICENCE CHECK PASSED: no GPL-only or unreviewed Qt modules; notices present.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
