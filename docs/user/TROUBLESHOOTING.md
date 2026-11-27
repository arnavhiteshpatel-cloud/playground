# Troubleshooting

> **Status.** Research product: not validated on real graft materials; not a medical device; no GLP/Part 11
> compliance claimed.

Start with the short table in the [desktop user guide §15](../desktop/USER_GUIDE.md#15-troubleshooting). This page
adds causes and fixes. For anything unexpected, look in `error.log` in the settings folder (Linux
`~/.config/OsteoQuant`, Windows `%APPDATA%\OsteoQuant`, macOS `~/Library/Application Support/OsteoQuant`) and run the
self-test.

## Installation and start-up

| Symptom | Likely cause | What to do |
|---|---|---|
| Windows: "Windows protected your PC" | The build is not code-signed | Expected for current builds. Verify the archive checksum ([INSTALLATION.md](INSTALLATION.md#verify-the-archive)) before choosing to run it |
| macOS: "cannot be opened because the developer cannot be verified" | Not signed or notarised | Expected. After verifying the archive, allow it under *System Settings > Privacy & Security* |
| Linux: application does not start; messages about `xcb`, EGL or OpenGL | Missing system libraries | Install the OpenGL/X libraries listed in [INSTALLATION.md](INSTALLATION.md#linux-x86_64) |
| 3D panel blank or very slow | OpenGL driver problems, remote desktop or virtual machine | Use the slice views; update graphics drivers. Physical displays and GPU drivers have only been exercised through virtual displays |
| Unsure whether the installation works | — | `osteoquant-desktop-console --selftest`; all 8 steps should print PASS (exit code 0). Add `--selftest-out DIR` and keep `selftest.jsonl` for support |

## Projects and sign-in

| Symptom | Cause | What to do |
|---|---|---|
| "Choose an empty or new folder for a new project" | The folder already contains files | Pick a new or empty folder |
| "... is not an OsteoQuant project folder" | The folder lacks `osteoquant-project.json` or `osteoquant.db` | Open the project folder itself, not `data/` or a parent folder |
| Password rejected when creating a user | Policy: ≥10 characters, an upper-case letter and a digit | Choose a compliant password |
| Sign-in refused | Wrong password, inactive user, or five failed attempts (locked for 15 minutes) | Wait 15 minutes or ask an administrator. There is no password-reset screen in the desktop yet |
| Recent project missing from the start page | The folder was moved or deleted | *File > Open project* and browse to it |

## Import

| Symptom | Cause | What to do |
|---|---|---|
| Cannot continue: "Voxel spacing ... not confirmed" | Spacing is *ASSUMED by reader* or *MISSING* | Enter the spacing in µm (z, y, x) from the scanner log and tick *Confirmed*. Wrong spacing makes every physical number wrong |
| Scan *rejected*: duplicate | Same content hash as an existing scan | Expected; the earlier import is kept |
| Scan *rejected*: unreadable or reader error | Corrupt, truncated or unsupported file; or header-declared size too large for memory | Check the file in the scanner software; export to NIfTI or a TIFF stack. Header sizes above the memory limit are refused rather than allowed to exhaust memory |
| MetaImage (`.mha`, `.mhd`) not readable | SimpleITK is not in the default bundle | Use a build with `OQ_BUNDLE_SITK=1`, or convert to NIfTI |
| Scan *flagged* | QC asks for review (for example incomplete acquisition metadata or anatomy truncated by the field of view) | Read the QC panel. Heuristic checks are prompts for attention, not standards |
| Import of a very large scan is slow or runs out of memory | Analysis needs the full volume in memory | Use a machine with more RAM or crop/downsample before import. Multi-GB import is unit-tested only with small data |

## Analysis

| Symptom | Cause | What to do |
|---|---|---|
| Scan marked *needs ROI* | Automatic ROI detection failed (common for segmental defects once healing bridges the gap) | Put the crosshair at the defect centre, *Study > Define cylindrical ROI at crosshair*, then analyse with *Use the latest saved ROI* ticked |
| Automatic ROI flagged "requires review" | Low detection confidence | Inspect the ROI outline; define a manual ROI if wrong |
| Values read *not measured* | The advisor does not support the endpoint for this material and scan | Hover for the reason; see [MATERIALS_AND_SUPPORT.md](MATERIALS_AND_SUPPORT.md). Typical fixes: choose the correct material, use a lower-noise scan, or plan a day-0 scan or histology |
| Everything *not measured*, including total mineral | Noise is ≥0.35 of the bone–soft-tissue contrast, or new bone cannot be separated from soft tissue | Check scan quality (CNR in QC); rescan or reconstruct with less noise |
| Support *flagged* on every endpoint | Uncertain voxels >10% of the ROI, QC unsuitable, failed plausibility check or automatic ROI needing review | See the reasons in the tooltip; correct the cause |
| Tb.Th flagged | Thickness below 2.5 voxels: partial-volume dominated | Use smaller voxels; treat thickness as unreliable |
| Graft classified as new bone (or vice versa) everywhere | *Graft is brighter than new bone* set wrongly, or wrong material | Fix the setting and re-analyse |
| No U-Net models in the Segmentation list | Default bundle lacks PyTorch, which the ONNX path still imports; or models missing from `_internal/models/` | Build with `OQ_BUNDLE_TORCH=1` and copy `registry.json` and `.onnx` files ([INSTALLATION.md](INSTALLATION.md#build-options)) |
| Job failed | Error in a stage | Double-click the job for details; see `error.log` |
| Job does not stop immediately after *Cancel* | Cancellation takes effect at the next stage boundary | Wait for the current stage |

## Editing, review and reports

| Symptom | Cause | What to do |
|---|---|---|
| Brush does not change some voxels | *Protect other classes* is on (default): painting changes only background | Untick it, or erase first |
| Undo history lost | History is kept in memory for the open scan only (last 500 operations) | Save revisions at meaningful points |
| 3D view does not show edits | Surfaces are re-extracted on demand | Click *Update* in the 3D panel |
| Cannot approve | You are the author, or your role is analyst/viewer | A different reviewer or administrator must sign. To add one, see [LICENSING_AND_ADMIN.md](LICENSING_AND_ADMIN.md#adding-users) |
| Signature refused | Wrong password at re-entry (recorded in the audit trail) | Re-enter carefully |
| Report watermarked "EVALUATION COPY" | No valid production licence | Expected; production licences cannot be issued yet |
| Report watermarked "TEST LICENCE" | A test licence is installed and test licences are allowed | Remove it; test licences prove nothing |
| Report columns blank | Endpoints not supported for this study | Read the report's suppressed-endpoint list |

## Audit trail and data

| Symptom | Cause | What to do |
|---|---|---|
| *Verify chain* reports an altered event | The database was edited outside the application, or is corrupted | Do not continue work in that project. Preserve a copy, restore from backup and verify again ([DATA_PROTECTION.md](DATA_PROTECTION.md#backups)) |
| Chain intact but the event count is below your recorded anchor | Newest events were removed | Treat as an integrity incident; restore from backup |
| "Licence ... bound to a different machine" | Host name or network adapter changed the fingerprint | Ask the licensor for a re-issued licence with the new fingerprint |

## Getting help

When you report a problem, include the version (`--version`), operating system, the self-test output
(`selftest.jsonl`), the relevant lines of `error.log` and the job details. **Do not send scans or study data** unless a
data-processing agreement is in place.
