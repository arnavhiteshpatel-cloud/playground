# OsteoQuant Desktop: packaging

The desktop application is distributed as a PyInstaller **one-folder** build per platform.
Nothing in the build needs a network connection at run time.

| File | Purpose |
|---|---|
| `packaging/osteoquant_desktop.spec` | PyInstaller spec (two executables sharing one runtime folder; macOS `.app` bundle) |
| `packaging/launcher.py` | entry script (`osteoquant.desktop.app.main`) |
| `packaging/build.py` | build, write licence notices, run the licence check, run the packaged self-test, write `build-info.json`, archive |
| `packaging/check_bundle_licences.py` | lists every shared library; fails on GPL-only or unreviewed Qt modules and missing notices; `--ldd` lists libraries expected from the target OS |
| `packaging/licenses/` | LGPL-3.0 and GPL-3.0 texts shipped in every build |
| `packaging/make_icons.py` | renders `packaging/icons/osteoquant.{png,ico,icns}` and the in-app window icon |
| `packaging/macos/entitlements.plist` | hardened-runtime exceptions needed by the embedded Python (for signing) |
| `.github/workflows/desktop-release.yml` | CI matrix: Windows x64, macOS 14 arm64, Ubuntu 22.04 x64; builds, tests, uploads artifacts; never publishes |

## Build locally

```bash
pip install -e ".[desktop]" pyinstaller pypdfium2 onnxruntime
python packaging/build.py            # -> packaging/dist/OsteoQuant/ and an archive
```

Output folder `packaging/dist/OsteoQuant/`:

```
OsteoQuant                       windowed application (OsteoQuant.exe on Windows)
osteoquant-desktop-console       same program with a console: --selftest, --version, support
THIRD_PARTY_NOTICES.txt         notices: Qt/PySide6 LGPL statement and relinking instructions, component list
licenses/                        LGPL-3.0.txt, GPL-3.0.txt, licence files of bundled distributions, INDEX.json
_internal/                       Python runtime, Qt, VTK, NumPy/SciPy, ... (shared libraries, replaceable)
```

On macOS PyInstaller additionally produces `packaging/dist/OsteoQuant.app`.

Build switches (environment variables read by the spec):

| Variable | Default | Effect |
|---|---|---|
| `OQ_BUNDLE_TORCH` | `0` | `1` includes PyTorch (only needed for `unet:` models) |
| `OQ_BUNDLE_ONNX` | `1` | `0` leaves out ONNX Runtime |
| `OQ_BUNDLE_SITK` | `0` | `1` includes SimpleITK (MetaImage `.mha/.mhd` import only) |
| `OQ_CODESIGN_IDENTITY`, `OQ_ENTITLEMENTS` | unset | passed to PyInstaller's macOS signing |

## Smoke test

`build.py` runs `osteoquant-desktop-console --selftest --selftest-out packaging/selftest-output`
with `QT_QPA_PLATFORM=offscreen`. The self-test generates a synthetic phantom and runs
import -> QC -> analysis (background job) -> slice and 3D rendering -> label edit with
undo/redo -> revision save -> report with licence watermark -> PDF preview -> audit-chain
verification. Each step is printed as JSON and written to `selftest.jsonl`; exit code 0 only if
all 8 steps pass. Users can run the same check on an installed copy.

## Results on this machine (Linux x86_64, Python 3.13, PySide6 6.12, VTK 9.7.2)

| Build | Folder size | Archive (`.tar.gz`) | Licence check | Packaged self-test |
|---|---|---|---|---|
| first build (all default Qt plugins, SimpleITK, server libs) | 1,184 MiB | 388 MiB | not yet written | PASS |
| before licence fixes (SimpleITK and uvloop excluded) | 909 MiB | 333 MiB | **FAIL**: 8 violations (Qt Virtual Keyboard libs + plugin) | PASS |
| **current default** (unneeded Qt plugins removed before dependency analysis) | **869 MiB** | **318 MiB** | **PASS** | **PASS** (8/8 steps, frozen) |
| with PyTorch and SimpleITK (`OQ_BUNDLE_TORCH=1 OQ_BUNDLE_SITK=1`, measured on the first build) | 1.9 GiB | not archived | n/a | not run |

PyTorch accounts for 680 MiB of the folder and SimpleITK for 260 MiB; neither is used by the
default desktop workflows (classical segmentation; TXM/DICOM/NIfTI/NRRD/Zarr/TIFF import).
The self-test was also run from source on a real X server (`xvfb-run`, Qt `xcb` platform) to
exercise the interactive `QVTKRenderWindowInteractor` 3D backend: PASS.

## Licence compliance of the bundle

Qt and PySide6 are used under the **LGPL-3.0**. Requirements and how the build meets them:

* **Only LGPL Qt modules.** Qt 6 offers some modules only under GPL-3/commercial terms (Virtual
  Keyboard, Charts, Data Visualization, Graphs, Quick 3D, Network Authorization, HTTP Server,
  Lottie, Shader Tools, Wayland Compositor, CoAP/MQTT/OPC UA, ...). PyInstaller's PySide6 hook
  collects every QtGui/QtNetwork plugin type; the `platforminputcontexts` plugins pulled in Qt
  Virtual Keyboard (and with it Qt Quick/QML). The spec now removes the plugin types the
  application does not use (`platformthemes`, `platforminputcontexts`, `egldeviceintegrations`,
  `generic`, `iconengines`, `imageformats`, `tls`, `networkinformation`) *before* dependency
  analysis, re-adds only the LGPL compose input-context plugin (dead keys) on Linux, and filters
  any remaining GPL-only Qt file names from the collected binaries and data.
* **Check in every build.** `packaging/check_bundle_licences.py` fails the build on any GPL-only
  Qt module, on any Qt module not on the reviewed LGPL allow-list, and on missing notices. The
  allow-list follows Qt's licensing table; re-check it when upgrading Qt.
* **Notices shipped.** `THIRD_PARTY_NOTICES.txt` (Qt/PySide6 statement, source locations,
  relinking instructions, component list with versions and declared licences) and `licenses/`
  (LGPL-3.0, GPL-3.0 and the licence files of 60+ bundled distributions, `INDEX.json`).
* **Replaceable libraries (relinking).** The one-folder build keeps Qt and PySide6 as separate
  shared libraries under `_internal/` (Linux `_internal/PySide6/Qt/lib/libQt6*.so.6`; Windows
  `_internal\PySide6\Qt6*.dll`; macOS `Contents/Frameworks/...`). A user can replace them with
  modified ABI-compatible builds of the same version; nothing is statically linked. The About
  dialog and the notices state that the OsteoQuant licence terms do not restrict modification of
  the LGPL libraries or reverse engineering for debugging such modifications. A future EULA must
  keep that carve-out.
* **No unneeded build-host files.** Only the two application executables are executable files in
  the folder (no compilers, Qt tools or `libexec` helpers). Dropping the GTK platform theme removed
  the host GTK/cairo/pango/ATK/ICU stack (183 -> 149 top-level library entries, most of them links
  to libraries vendored inside the Python wheels). The remaining host libraries are runtime
  dependencies of Qt's X11/Wayland platform plugins, QtNetwork (GSSAPI) and Python's standard
  library (OpenSSL, zlib, bz2, lzma, libffi, expat).

Licence-check output of the current build (`packaging/dist/licence-check.txt`; library list
abridged):

```
shared libraries: 640 files + 111 symlinks (757 MiB)
Qt modules: Core, DBus, EglFSDeviceIntegration, Gui, Network, OpenGL, OpenGLWidgets, Pdf, PdfWidgets, Svg,
            WaylandClient, Widgets, WlShellIntegration, XcbQpa
libraries expected from the target system (ldd): libEGL.so.1, libGL.so.1, libGLX.so.0, libGLdispatch.so.0,
            libc.so.6, libdl.so.2, libdrm.so.2, libm.so.6, libpthread.so.0, libresolv.so.2, librt.so.1,
            libutil.so.1, libwayland-client.so.0, libwayland-cursor.so.0, libwayland-egl.so.1, libxcb.so.1
LICENCE CHECK PASSED: no GPL-only or unreviewed Qt modules; notices present.
```

Before the fix the same check reported:

```
Qt modules: Core, DBus, EglFSDeviceIntegration, EglFsKmsSupport, Gui, Network, OpenGL, OpenGLWidgets, Pdf,
            PdfWidgets, Qml, QmlMeta, QmlModels, QmlWorkerScript, Quick, Svg, VirtualKeyboard,
            VirtualKeyboardQml, WaylandClient, Widgets, WlShellIntegration, XcbQpa
LICENCE CHECK FAILED (8 violations):
    GPL-only Qt module VirtualKeyboard: _internal/libQt6VirtualKeyboard.so.6 (+ PySide6/Qt/lib copy)
    GPL-only Qt module VirtualKeyboardQml: _internal/libQt6VirtualKeyboardQml.so.6 (+ PySide6/Qt/lib copy)
    GPL-only Qt plugin: PySide6/Qt/plugins/platforminputcontexts/libqtvirtualkeyboardplugin.so
    missing notice file: THIRD_PARTY_NOTICES.txt, licenses/LGPL-3.0.txt, licenses/GPL-3.0.txt
```

Not verified here: the Windows and macOS bundles (their plugin sets differ, e.g. `styles` on
Windows, `platforms/darwin` on macOS); the CI build runs the same check on each platform.

## Models

Locked segmentation models are **not** part of the bundle. The library looks for them in
`osteoquant.ml.train.MODEL_DIR`, which is `<package parent>/models`; in the packaged
application that is:

| Platform | Model folder |
|---|---|
| Windows / Linux | `<install folder>/OsteoQuant/_internal/models/` |
| macOS | `OsteoQuant.app/Contents/Frameworks/models/` (PyInstaller 6 layout; verify on the first macOS build) |

Copy `registry.json` and the `<name>.onnx` files there. The analysis dialog lists a model only
if its ONNX file exists, the registry has its `onnx_sha256` (the library verifies the hash
before loading) and the runtime imports.

**Current limitation:** `osteoquant/ml/runtime.py` (ONNX inference) imports helpers from
`osteoquant/ml/train.py`, which imports PyTorch at module level. In the default (torch-free)
bundle the ONNX models are therefore not offered. Once those helpers (`MODEL_DIR`, `Case`,
`build_input`, `_gauss_window`) move to a torch-free module, ONNX inference works in the
default bundle with no packaging change. Until then build with `OQ_BUNDLE_TORCH=1` if model
inference is needed. An `OQ_MODEL_DIR` override in the library would also make the model
location independent of the install layout.

## Code signing and notarisation (requires the publisher's credentials)

No signing credentials exist yet; the CI steps for signing run only when the secrets below are
configured, and nothing in this repository imitates a signature. Unsigned builds trigger
SmartScreen (Windows) and Gatekeeper (macOS) warnings and are for internal testing only.

**Windows (Authenticode)**
1. Obtain an OV or EV code-signing certificate for the publishing company (EV avoids the
   SmartScreen reputation period; EV keys usually live on a hardware token or a cloud HSM such
   as Azure Trusted Signing, which then replaces the PFX step).
2. Repository secrets: `WINDOWS_CERT_PFX_BASE64`, `WINDOWS_CERT_PASSWORD`.
3. CI signs `OsteoQuant.exe` and `osteoquant-desktop-console.exe` with SHA-256 and an RFC 3161
   timestamp. Re-archive after signing (the workflow step order already signs before upload).
4. Optional next step: an MSI/MSIX installer (WiX or MSIX packaging tool), also signed.

**macOS (Developer ID + notarisation)**
1. Apple Developer Program membership for the company; create a *Developer ID Application*
   certificate; export it as `.p12`.
2. Secrets: `MACOS_CERT_P12_BASE64`, `MACOS_CERT_PASSWORD`, `MACOS_SIGNING_IDENTITY`
   ("Developer ID Application: <Company> (<TEAMID>)"), `MACOS_NOTARY_APPLE_ID`,
   `MACOS_NOTARY_TEAM_ID`, `MACOS_NOTARY_APP_PASSWORD` (app-specific password).
3. CI signs the `.app` with the hardened runtime and `packaging/macos/entitlements.plist`,
   submits to `notarytool`, staples the ticket and re-archives.
4. Optional: a signed `.dmg` (e.g. `create-dmg`), notarised the same way.

**Linux**: distribute the `.tar.gz`; optionally publish a SHA-256 checksum file signed with the
company's GPG key, or an AppImage.

## Licence signing key (production)

The application embeds only public keys (`osteoquant/licensing/keys.py`). No production key has
been generated. To create one:

1. On an offline machine: generate an Ed25519 keypair (e.g. `tools/make_test_licence.py
   --keygen DIR` produces the same key type; for production, store the private key in a
   hardware token or encrypted offline storage, never in the repository or CI).
2. Add the 32-byte raw public key (hex) to `PRODUCTION_KEYS` under a new key id, e.g.
   `"oq-prod-2027-01"`, and release a build.
3. Sign customer licences with that private key (same payload format as the test tool, with
   `"test": false`). Rotate by adding a new key id; keep old ids until their licences expire.

`tools/make_test_licence.py` only produces TEST licences signed with a published test key.
They are accepted only when `OSTEOQUANT_ACCEPT_TEST_LICENCES=1` and are labelled TEST LICENCE.

## Not tested here

* **Windows and macOS builds** were not built or run in this environment (Linux only). The
  workflow is written for them but its first run on GitHub Actions is the first real test;
  expect to adjust the spec for platform-specific Qt plugins or VTK OpenGL libraries.
* The macOS model-folder path above follows PyInstaller 6 conventions and needs confirming.
* Signing and notarisation steps have never run (no credentials).
* Interactive use on physical displays (high-DPI scaling, GPU drivers, multi-monitor) was only
  exercised through `xvfb` and the off-screen Qt platform.
* Volumes of several GB: the slab-import and lazy-display paths are unit-tested with small
  data and artificially low thresholds, not with real multi-GB scans.
