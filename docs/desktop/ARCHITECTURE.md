# OsteoQuant Desktop: architecture

OsteoQuant Desktop is an offline PySide6 (Qt 6) + VTK application that calls the OsteoQuant
library directly. It has no local server, no browser component and no network access at run
time. It shares the project database format with the web prototype (`osteoquant/api/`), so a
project folder can be opened by either front end.

## Module map

| Module (`osteoquant/desktop/`) | Kind | Responsibility |
|---|---|---|
| `app.py`, `__main__.py` | entry | argument parsing, `--selftest`, `--screenshots`, theme, exception hook |
| `project.py` | model | project folder (marker + SQLite `Store` + data dir), sign-in, re-authentication, study tree, import log |
| `services.py` | service | every call into the library: probe/import/QC, analysis, manual ROI, label revisions, review sign-off, reports, model discovery |
| `support.py` | service | `measurement_support(result) -> dict`: per-endpoint *supported / flagged / not supported* |
| `editing.py` | model | `LabelEditor` operations and `SparseDiff` (compressed sparse undo records) |
| `undo.py` | Qt model | `QUndoStack` integration (`LabelEditCommand`, `EditHistory`) |
| `volume_source.py` | model | slice-lazy image access (`ZarrSource`, `ArraySource`) with a byte-bounded LRU cache |
| `viewer_state.py` | Qt model | open scan, labels, crosshair, window/level, overlay settings, active tool; routes all edits to the undo stack |
| `jobs.py` | Qt service | `JobManager` on `QThreadPool`: progress, cooperative cancellation, error capture, job table + audit |
| `timing.py` | model + filter | opt-in, local-only workflow timing (schema below) |
| `slice_view.py` | widget | axial/coronal/sagittal view: QPainter rendering of NumPy slices, crosshair, scale bar, interaction |
| `view3d.py` | widget | VTK 3D panel: label surfaces (`vtkDiscreteFlyingEdges3D`), volume rendering (`vtkSmartVolumeMapper`) |
| `oblique.py` | widget | oblique reslice through the crosshair (`vtkImageReslice`) |
| `panels.py` | widgets | display, segmentation tools, voxel readout, QC and jobs panels |
| `import_wizard.py` | model + widgets | `ImportModel` (all rules) and the four-page `ImportWizard` |
| `results_view.py` | model + widget | per-scan endpoint table (`build_rows`, `ResultsModel`), CSV export |
| `reports_view.py` | widget | report generation, QtPdf page-by-page preview, export, sign-off |
| `review_audit.py` | widgets | review/sign-off panel with blinded mode; audit-trail viewer with chain verification |
| `dialogs.py` | widgets | new project, sign-in, study, analysis settings, ROI, revision reason, signature, licence, About |
| `main_window.py` | widget | assembles everything: start page, tabs (Viewer, Results, Reports, Audit trail), docks, menus, status bar |
| `selftest.py`, `screenshots.py`, `demo.py` | tooling | headless end-to-end check; documentation screenshots; synthetic phantom data |

`osteoquant/licensing/` (independent of Qt): Ed25519 licence files, see *Licensing* below.

Rule: anything that can be expressed without a widget lives in a model/service class and is
unit-tested without a window (`tests/desktop/test_editing.py`, `test_import.py`,
`test_services.py`, `test_licensing.py`). Widgets only translate user input into calls on
those classes and render their state.

## Library reuse (no duplicated science)

| Function | Library call |
|---|---|
| format detection / reading | `osteoquant.io.detect_format`, `read_volume(path, spacing_um, zrange, step, do_hash)` |
| chunked store | `osteoquant.io.write_zarr`, `write_labels_zarr` (same layout as the web API) |
| QC | `osteoquant.qc.run_qc` |
| analysis | `osteoquant.api.app.job_analyze` (the same job handler the web API runs, which calls `osteoquant.pipeline.analyze`) |
| measurement support | `osteoquant.advisor.integration.measurement_support` (via `support._separability_assessment`) |
| manual ROI | `osteoquant.roi.cylinder_roi` + `Store.save_roi` |
| endpoints after editing | `osteoquant.morphometry.defect_report_metrics` with the base version's ROI; `advisor.integration.apply_support` |
| reports | `osteoquant.api.bundle.bundle_from_store` + `osteoquant.report.build_pdf(..., watermark=)` |
| users, RBAC, studies, reviews | `osteoquant.study.db.Store` |
| audit trail | `osteoquant.audit.AuditLog` (hash chain, `verify_chain`) |

One library change was made for the desktop, and it is additive: `report.build_pdf` gained an
optional `watermark` argument. Nothing else in `study/`, `report/` or `audit/` changed; the
desktop's own tables (`desktop_import_log`, `desktop_settings`, `desktop_timing_events`) are
created by desktop code with `CREATE TABLE IF NOT EXISTS`.

## Data flow

```
 file/folder ──probe_source──> SourceProbe (format, shape, metadata found/assumed, spacing source)
      │                              │  user confirms or enters voxel spacing (mandatory if not in file)
      ▼                              ▼
 ImportModel.run ──import_scan──> read (whole, or slab-by-slab for large slab-capable formats)
      │                              │  -> temporary Zarr -> Store.register_scan (hash, duplicates) -> move
      │                              ▼
      │                         run_scan_qc -> Store.set_scan_qc       (rejections -> import log + audit)
      ▼
 Project tree ──open_scan──> ZarrSource (lazy slices) + labels (uint8) -> ViewerState -> views
      │
      ├─ Analyse (job) ── job_analyze ──> segmentation vN, ROI, measurement (+ advisor output)
      ├─ Edit ── LabelEditor -> SparseDiff -> QUndoStack ── Save revision (job) ──> corrected vN+1
      ├─ Review ── re-authentication ──> Store.review (+ audit, object hash)
      └─ Report (job) ── bundle_from_store + build_pdf(watermark) ──> PDF/CSV, QtPdf preview
```

## Threading model

* The GUI thread owns all widgets, VTK render windows and the `ViewerState`.
* Long operations (import + QC, analysis, label-revision save with endpoint recomputation,
  reports) run as `JobManager` jobs on a `QThreadPool` (2 threads). A job is a plain function
  `fn(ctx)`; `ctx.progress(frac, msg)` publishes progress through a Qt signal (queued to the GUI
  thread) and raises `JobCancelled` if cancellation was requested. The library already reports
  progress at stage boundaries, so cancellation takes effect at the next stage.
* Jobs receive copies of the data they need (e.g. the label array to save), never live
  widget state. Completion callbacks run on the GUI thread.
* A job's terminal state is written to the `jobs` table and the audit trail before
  `job.active` turns false, so observers never see a finished job without its record.
* Surface extraction for the 3D panel runs on a private single-thread pool; actors are created
  on the GUI thread. Stale results are discarded by a token.
* The SQLite store uses one connection guarded by the store's re-entrant lock; the audit log
  serialises chain updates with `BEGIN IMMEDIATE`.

## Undo design

* Labels are an in-memory `uint8` array owned by `LabelEditor` (one byte per voxel).
* Every operation computes the flat indices it may change, filters by the protection rule
  (paint over background/self only, erase only the active class), keeps only voxels whose value
  actually changes, applies the change, and returns a `SparseDiff`:
  * sorted flat indices, delta-encoded, narrowed to uint8/16/32 where possible, zlib-compressed;
  * old values and new values, zlib-compressed;
  * bounding box (for minimal view refresh) and per-class voxel delta.
* `LabelEditCommand(QUndoCommand)` stores one diff. `undo` writes the old values, `redo` the new
  values; both are exact (tested over random 40-edit sequences: undo-all restores the original
  bit-for-bit, redo-all the final state). A whole mouse stroke is one command.
* Memory is proportional to changed voxels. A 2D brush stroke typically costs a few hundred
  bytes; the panel shows the history size. The stack keeps the last 500 commands.
* Saving creates a new *corrected* segmentation version through `services.save_label_revision`:
  user (from the store session), reason (mandatory), base version, per-class voxel changes and
  per-tool operation counts are written to the segmentation record and to the audit trail
  (`segmentation.save` + `segmentation.edit`). Endpoints are recomputed with the base version's
  ROI and the advisor's support decision is carried over.

## Rendering

* Slice views render NumPy slices with QPainter (nearest-neighbour, physical aspect ratio).
  This gives crisp voxels, exact control of overlays and editing interaction, and identical
  behaviour on and off screen. Label overlay colours/opacities are a 256-entry RGBA lookup table.
* The 3D panel uses VTK: `QVTKRenderWindowInteractor` on normal desktops; on headless Qt
  platforms (`offscreen`, CI, self-test) the same scene is rendered by an off-screen
  `vtkRenderWindow` and shown as an image with mouse rotation/zoom.
* Oblique slices use `vtkImageReslice` on a strided copy of the image (≤ 256³ voxels).

## Performance and memory

| Data | Strategy |
|---|---|
| Image for display | never loaded whole: slices read from the 64³-chunked Zarr store; LRU cache (256 MiB) |
| Window/level defaults | percentiles from a strided sample (≈ 48 samples per axis) |
| 3D surfaces | strided labels within 200³ voxels |
| Volume rendering | strided image within 128³ voxels |
| Import of large volumes | slab-by-slab when > 1 GiB and the format supports z-ranges (TIFF/PNG stacks, DICOM, Zarr, TXM); content hash computed incrementally and identical to the whole-volume hash |
| QC | full resolution up to 2 GiB, otherwise on an integer-decimated copy (recorded in the QC result) |
| Labels for editing | full `uint8` array (needed for random-access editing) |
| Analysis | full volume (the library pipeline is in-memory) |

Limits are environment-overridable (`OQ_SLAB_IMPORT_BYTES`, `OQ_QC_FULL_RES_BYTES`,
`OQ_3D_SURFACE_VOXELS`, `OQ_3D_VOLUME_VOXELS`, `OQ_OBLIQUE_VOXELS`). The status bar shows
process memory, slice-cache size and free system memory.

## Licensing

`osteoquant/licensing/` verifies offline licence files (`.oqlic`, JSON): `payload` is the
canonical JSON string {licence_id, licensee, edition (academic/commercial/evaluation),
features, issued, expiry, machine (optional fingerprint), product, test}; `signature` is a
detached Ed25519 signature over the exact payload bytes; `key_id` selects an embedded public
key. Production keys: none yet (`keys.PRODUCTION_KEYS` is empty). A test key whose private
half is published in `tools/make_test_licence.py` is accepted only when test licences are
explicitly allowed and is always labelled *TEST LICENCE*. Without a valid licence the
application runs in evaluation mode: all functions work, reports carry the watermark
"EVALUATION COPY - NOT FOR STUDY DECISIONS".

## Workflow timing (opt-in, local only)

Off by default; enabled per project from *Tools > Record workflow timing for this project*.
Events are stored only in the project's SQLite database; nothing is transmitted.

```sql
CREATE TABLE desktop_settings (key TEXT PRIMARY KEY, value TEXT);      -- 'workflow_timing' = '1' | '0'
CREATE TABLE desktop_timing_events (
  id         INTEGER PRIMARY KEY,
  session_id TEXT NOT NULL,      -- random id per application session
  study_id   INTEGER,
  scan_id    INTEGER,
  user_id    INTEGER,            -- signed-in user (users.id)
  event      TEXT NOT NULL,      -- scan_open | scan_close | first_edit | edit | review_signoff | active_time
  tool       TEXT,               -- edit tool: brush2d, eraser2d, brush3d, eraser3d, region_grow, fill_holes, interpolate
  details    TEXT,               -- JSON: edit {"voxels_changed": {label: delta}};
                                 --       review_signoff {"object_type","object_id","decision"};
                                 --       active_time {"seconds", "idle_gap_s": 60}
  ts_utc     TEXT NOT NULL);
```

Active time is the sum of intervals between consecutive user inputs (mouse, keyboard, wheel)
that are at most 60 s apart, attributed to the open scan and flushed on scan change, on
disabling, and every 5 minutes. *Tools > Export workflow timing CSV* writes one row per scan
and user (opens, first open/edit, edit count, tools, voxels changed per class, sign-offs,
active seconds) plus a raw `*_events.csv`. Enabling/disabling and exports are audit events.

## Other desktop-owned tables

`desktop_import_log` (id, study_id, source, status, reason, scan_id, user_id, details,
created): every import attempt including rejected and user-excluded sources, shown under
*Rejected imports* in the project tree.
