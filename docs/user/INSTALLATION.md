# Installing OsteoQuant Desktop

> **Status.** Research product: not validated on real graft materials; not a medical device; no GLP/Part 11
> compliance claimed.

This page covers installation only. For day-to-day use see the [Quick start](QUICK_START.md) and the
[desktop user guide](../desktop/USER_GUIDE.md).

## What you get

OsteoQuant Desktop is distributed as a PyInstaller *one-folder* build per operating system. The folder contains:

| Item | Purpose |
|---|---|
| `OsteoQuant` (`OsteoQuant.exe` on Windows; `OsteoQuant.app` on macOS) | The application (no console window) |
| `osteoquant-desktop-console` | The same program with a console, for `--selftest`, `--version` and support |
| `THIRD_PARTY_NOTICES.txt`, `licenses/` | Third-party notices; licence texts of the bundled Python distributions, the Python runtime (PSF), ICU and the system libraries (`licenses/system/`); `INDEX.json` and `BUNDLE_INVENTORY.json` |
| `_internal/` | Python runtime, Qt, VTK, NumPy/SciPy and the analysis library |

Nothing in the build needs a network connection at run time. The default build contains ONNX Runtime but not
PyTorch or SimpleITK (see [Build options](#build-options)).

## Status per operating system

| Platform | How it is built | Tested in this project | Code signing |
|---|---|---|---|
| Linux x86_64 | `packaging/build.py`, locally and in CI (Ubuntu 22.04) | Yes: packaged self-test passed 8 of 8 steps (headless); also run from source on an X server | Not applicable; `.tar.gz` archive |
| Windows x64 | CI build matrix (`.github/workflows/desktop-release.yml`) only | **No.** The Windows build has never been run here; its first CI run is its first real test | **Not signed** (pending the publisher's code-signing certificate) |
| macOS 14, Apple silicon | CI build matrix only | **No.** Never run here; the model-folder path inside the `.app` also needs confirming | **Not signed or notarised** (pending the publisher's Apple Developer ID credentials) |

The CI workflow builds, runs the desktop tests and the packaged self-test, and uploads archives as workflow
artifacts kept for 14 days. It never publishes a release. Signing and notarisation steps exist in the workflow but
only run once the founder adds the credentials as repository secrets (`docs/desktop/PACKAGING.md`).

Unsigned builds trigger Windows SmartScreen and macOS Gatekeeper warnings. They are for internal testing only.

## Hardware

The reference environment for all measurements in this project was 4 CPU cores, 15 GB RAM and no GPU. Practical
notes:

* Analysis runs in memory on the full volume. Plan for several times the scan size in RAM.
* Display never loads the whole image: slices are read from a chunked store with a 256 MiB cache.
* Volumes over 1 GiB are imported slab by slab for slab-capable formats (TIFF/PNG stacks, DICOM, Zarr, TXM). This
  path is unit-tested with small data and lowered thresholds, not yet with real multi-GB scans.
* There is no GPU inference. Classical multi-Otsu segmentation is the default.

## Linux (x86_64)

1. Unpack the archive, for example `tar xzf OsteoQuant-desktop-linux-*.tar.gz` (the name ends in the machine architecture, e.g. `x86_64`).
2. The system needs the usual desktop OpenGL and X/Wayland libraries. On Ubuntu 22.04 the CI installs:
   `libegl1 libgl1 libopengl0 libglu1-mesa libxkbcommon0 libxkbcommon-x11-0 libfontconfig1 libdbus-1-3 libxcb-cursor0`.
3. Start `OsteoQuant/OsteoQuant`.
4. Check the installation: `OsteoQuant/osteoquant-desktop-console --selftest` (see [Self-test](#self-test)).

## Windows (x64) — untested

1. Unzip the archive to a folder you can write to, for example `C:\Program Files\OsteoQuant` (administrator) or a
   folder in your user profile.
2. Start `OsteoQuant.exe`. Because the build is unsigned, SmartScreen may show "Windows protected your PC". Proceed
   only if you obtained the archive from the project's own CI run and verified it (see [Verify the
   archive](#verify-the-archive)).
3. Run `osteoquant-desktop-console.exe --selftest` from a Command Prompt in that folder.

Please report anything that differs from this description: it has not been observed on a real Windows machine.

## macOS 14 (Apple silicon) — untested

1. Unzip the archive and move `OsteoQuant.app` to *Applications*.
2. Because the app is neither signed nor notarised, Gatekeeper blocks the first start. You can allow it for this
   app in *System Settings > Privacy & Security* ("Open Anyway"). Do this only for an archive you have verified.
3. The console executable for the self-test is inside the bundle (exact path to be confirmed on the first macOS
   build).

Please report anything that differs: the macOS build has not been observed on a real Mac.

## From source (any platform, for developers and evaluators)

Requires Python 3.10 or later (the project is developed on Python 3.13).

```bash
python3 -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -e ".[desktop]"
osteoquant-desktop                                       # or: python -m osteoquant.desktop
python -m osteoquant.desktop --selftest                  # end-to-end check
```

Note: the package currently declares PyTorch as a required dependency, so a source install downloads it even though
the desktop's default workflows do not use it. On Linux, the CPU-only wheel is smaller:
`pip install torch --index-url https://download.pytorch.org/whl/cpu` before the line above.

## Self-test

`osteoquant-desktop-console --selftest` (or `python -m osteoquant.desktop --selftest`) generates a small
synthetic phantom and runs: import, QC, analysis as a background job, slice and 3D rendering, a label edit with
undo/redo, revision save, a report with the licence watermark, PDF preview and audit-chain verification. Each step
prints one JSON line with PASS or FAIL; the exit code is 0 only if all 8 steps pass. Add
`--selftest-out DIR` to keep the artefacts and `selftest.jsonl`.

## Verify the archive

There are no signatures yet, so verify by checksum. Compute the SHA-256 of the archive and compare it with the
value from the CI run that produced it (or from whoever built it):

* Linux: `sha256sum OsteoQuant-desktop-*.tar.gz`
* macOS: `shasum -a 256 OsteoQuant-desktop-*.zip`
* Windows (PowerShell): `Get-FileHash OsteoQuant-desktop-*.zip -Algorithm SHA256`

## Build options

Builders can set these environment variables before `python packaging/build.py`:

| Variable | Default | Effect |
|---|---|---|
| `OQ_BUNDLE_TORCH` | `0` | `1` includes PyTorch (needed today for locked U-Net models; see below) |
| `OQ_BUNDLE_ONNX` | `1` | `0` leaves out ONNX Runtime |
| `OQ_BUNDLE_SITK` | `0` | `1` includes SimpleITK (MetaImage `.mha/.mhd` import only) |

**Locked models.** Models are not part of the bundle. Copy `registry.json` and the `<name>.onnx` files into
`<install folder>/OsteoQuant/_internal/models/` (Windows/Linux). In the default, PyTorch-free bundle the ONNX models
are currently *not offered*, because the ONNX runtime code still imports helpers from a module that needs PyTorch;
build with `OQ_BUNDLE_TORCH=1` if you need model inference. Never use synthetic-only models on real scans.

## Uninstall

Delete the application folder (or `OsteoQuant.app`). Your projects are separate folders and are not touched.
Per-user files live in the settings folder: Linux `~/.config/OsteoQuant`, Windows `%APPDATA%\OsteoQuant`, macOS
`~/Library/Application Support/OsteoQuant` (licence file and `error.log`), plus the operating system's settings
store for recent projects and theme.
