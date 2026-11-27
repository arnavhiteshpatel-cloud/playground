# OsteoQuant Desktop: packaging

The desktop application is distributed as a PyInstaller **one-folder** build per platform.
Nothing in the build needs a network connection at run time.

| File | Purpose |
|---|---|
| `packaging/osteoquant_desktop.spec` | PyInstaller spec (two executables sharing one runtime folder; macOS `.app` bundle) |
| `packaging/launcher.py` | entry script (`osteoquant.desktop.app.main`) |
| `packaging/build.py` | build, add third-party licence texts, run the packaged self-test, write `build-info.json`, archive |
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
THIRD_PARTY_LICENSES/            licence texts + INDEX.json of bundled distributions
_internal/                       Python runtime, Qt, VTK, NumPy/SciPy, ...
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

| Build | Folder size | Archive (`.tar.gz`) | Packaged self-test |
|---|---|---|---|
| default (no PyTorch, no SimpleITK, with ONNX Runtime) | SIZE_DEFAULT | ARCHIVE_DEFAULT | PASS (8/8 steps, frozen) |
| with PyTorch and SimpleITK | SIZE_TORCH | not archived | not run |

PyTorch alone accounts for TORCH_SIZE of the folder and SimpleITK for SITK_SIZE; neither is used
by the default desktop workflows (classical segmentation, TXM/DICOM/NIfTI/NRRD/Zarr/TIFF import).
The self-test was also run from source on a real X server (`xvfb-run`, Qt `xcb` platform) to
exercise the interactive `QVTKRenderWindowInteractor` 3D backend: PASS.

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
