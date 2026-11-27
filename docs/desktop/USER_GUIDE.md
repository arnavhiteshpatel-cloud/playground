# OsteoQuant Desktop: user guide

OsteoQuant Desktop analyses preclinical micro-CT scans of bone defects. It separates each scan
into new bone, residual graft and host bone, reports defect-fill endpoints, and keeps a
signed, hash-chained record of every step. It runs entirely on your computer and never connects
to a network.

It is research software: it is not a medical device and has not been validated for GLP or
clinical use. Check every automatic result before you rely on it.

Screenshots of each screen are in `docs/screenshots/desktop/`.

---

## 1. Start the application

* Installed build: start **OsteoQuant** (Windows Start menu / macOS Applications / the
  `OsteoQuant` file in the Linux folder).
* From a Python installation: `osteoquant-desktop` or `python -m osteoquant.desktop`.

The start page offers **New project**, **Open project** and your recent projects.

## 2. Create or open a project

A project is a folder that holds the study database, imported scans, label revisions,
reports and the audit trail. Keep it on a local or backed-up drive.

**New project**
1. *File > New project*.
2. Enter a project name, a new empty folder, your user name, full name and a password (at least
   10 characters with an upper-case letter and a digit).
3. You become the project administrator and are asked to create the first study.

**Open project**: *File > Open project* (or a recent project), then sign in. Every action is
recorded in the audit trail under the signed-in user.

**More users**: reviewers sign off segmentations and reports; an author cannot approve their
own segmentation. Roles: administrator, analyst, reviewer, viewer.

## 3. Organise studies

The **Project** panel (left) shows *Study > Group > Animal > Timepoint > Scan*.

* *Study > New study*: name, species, defect model (condyle, calvarial, segmental), graft
  material(s), and whether the study is blinded.
* *Study > Add group* (or right-click a study): treatment arms.
* Animals and timepoints are created while importing scans.
* Scans show a coloured dot for their QC verdict (green suitable, amber review, red unsuitable)
  and their status (QC result, analysed, needs ROI).
* **Rejected imports** lists every file that was not imported, with the reason (hover or
  right-click > *Show rejection reason*).

## 4. Import scans

*File > Import scans* (or **Import...** above the tree) opens a four-step wizard.

1. **Select scans**. Choose the study, then add files or folders. Supported: Zeiss TXM/TXRM,
   DICOM series, NIfTI, NRRD, Zarr, TIFF (single multi-page file or a folder of slices), PNG/BMP
   slice folders, MetaImage and NumPy. A folder that is one series becomes one scan; a folder of
   several volumes becomes several scans.
2. **Metadata and voxel spacing**. Every scan shows where its voxel spacing comes from:
   *file metadata*, *ASSUMED by reader* or *MISSING*. Spacing drives every physical measurement,
   so for assumed or missing spacing you must type the values in µm (z, y, x) and tick
   *Confirmed*. *Apply and confirm* sets one value for all scans lacking file spacing. You cannot
   continue until every scan has explicit spacing. The lower table lists the metadata found in
   the selected file and anything the reader assumed.
3. **Assign to animals and timepoints**. Edit the animal ID (letters, digits, `.`, `_`, `-`),
   group, timepoint label and day. Unticking *Import* excludes a scan; it is still listed as
   rejected ("excluded by the user").
4. **Import and quality control**. *Start import* copies each scan into the project with
   SHA-256 provenance and runs QC in the background. The result table shows *imported*,
   *flagged* (imported, but QC asks for review or found failures) or *rejected* (with the
   reason: unreadable, duplicate of an existing scan, reader error, missing spacing). Select a
   row to see its QC checks, split into **deterministic** checks (facts about the file, such as
   missing slices or saturated voxels) and **heuristic** checks (scores with developer-chosen
   thresholds; they flag scans for attention and are not established standards).

Large volumes are imported slab by slab, so memory use stays bounded.

## 5. View a scan

Double-click a scan. The **Viewer** shows axial, coronal and sagittal slices and the 3D panel.

| Action | How |
|---|---|
| Move the crosshair (all views follow) | left-click or drag with the *Navigate* tool |
| Change slice | mouse wheel, arrow keys, Page Up/Down |
| Zoom | Ctrl + wheel (about the pointer); **F** fits the slice to the view |
| Pan | middle-drag or Shift + left-drag |
| Window / level | right-drag (horizontal = width, vertical = level), or the *Display* panel presets and fields |
| Maximise a view | double-click it (again to restore) |
| Voxel readout | *Voxel* panel: voxel index, position in mm, intensity, label |

Every slice view shows its orientation, slice number and depth in mm, the window, the zoom and
a scale bar in µm or mm. Presets are based on each scan's own histogram because grey values
are uncalibrated unless an HA calibration is recorded.

**Display panel**: segmentation version, overlay on/off, and for each class (new bone,
residual graft, host bone, uncertain) visibility, colour and opacity.

**3D panel**: *Surfaces* (label classes as smoothed surfaces), *Volume* (volume rendering of a
downsampled image) or both. Drag to rotate, wheel to zoom, *Reset* to restore the view. After
editing labels, *Update* re-extracts the surfaces.

**Oblique** panel (View menu): a plane through the crosshair tilted about x and y.

**Screenshot**: *File > Export screenshot* saves the four views as PNG.

## 6. Run the analysis

Select scans, an animal, a group or a whole study in the tree and choose **Analyse...**.

* **Defect model** and **nominal defect diameter** help the automatic ROI detection.
* **Segmentation**: Multi-Otsu (classical). Locked U-Net models appear here when their ONNX
  export and runtime are installed.
* **Graft material**: used by the measurement-support advisor to decide which endpoints can
  be separated reliably for this material and scan. Choose *Unspecified* if unknown, or *No graft
  (empty defect)* for empty-defect controls.

Each scan runs as a background job (**Jobs** panel; progress also in the status bar). You can
keep working, and **Cancel** stops a job at its next stage. Failed jobs show the error;
double-click for details.

If the ROI cannot be detected the scan is marked *needs ROI*: place the crosshair at the defect
centre and use *Study > Define cylindrical ROI at crosshair* (radius, extent, reason), then
analyse again with *Use the latest saved ROI* ticked.

## 7. Correct the segmentation

Open the scan and use the **Segmentation** panel (or the toolbar / keys).

| Tool | Key | Use |
|---|---|---|
| Navigate | N | move the crosshair |
| Brush | B | paint the active class; drag for a stroke |
| Eraser | E | set voxels back to background |
| Region grow | G | click a seed: voxels connected to it within the intensity tolerance get the active class (on the slice, or in 3D within 48 voxels) |
| Fill holes | H | click a slice: closes holes inside the active class on that slice |
| Interpolate | panel buttons | after editing two slices of one orientation, fills the slices between them by shape interpolation |

* Brush **radius** is in µm (round in physical space even for anisotropic voxels); **2D disk**
  paints on the slice, **3D sphere** paints a ball.
* **Protect other classes** (on by default): painting changes only background voxels and the
  eraser removes only the active class.
* **Undo/Redo**: Ctrl+Z / Ctrl+Shift+Z (or the buttons). The panel shows the unsaved voxel
  changes per class and the size of the history.
* **Save as new revision...** (Ctrl+S): enter the reason. A new *corrected* version is stored;
  the original is never overwritten. Endpoints are recomputed with the same ROI. Your name, the
  reason and the per-class voxel changes go into the audit trail.

## 8. Results

The **Results** tab lists every scan of a study with its endpoints and units: defect TV
(mm³), new bone volume (mm³), new bone BV/TV (%), residual graft (%), mineralised (%),
uncertain (%), Tb.Th, Tb.Sp (µm), Tb.N (1/mm) and defect coverage (%).

The **Support** column summarises whether the measurements can be relied on:

* **supported**: every endpoint is supported;
* **flagged**: some endpoints need caution (orange values) or are not reportable;
* **not supported**: no endpoint can be reported (or the analysis failed);
* **not analysed**: the scan has not been analysed yet.

An endpoint the advisor does not support is shown as *not measured*; hover over it for the
reason (for example, graft and new bone cannot be separated for this material). Double-click a
row to open the scan. **Export CSV** writes the table including per-endpoint support.

## 9. Review and sign-off

The **Review** panel lists the segmentation versions of the open scan with their latest
decision. Reviewers and administrators can **Approve**, mark **Needs changes** or **Reject**:
state the meaning of the signature and re-enter your password. The signature, its meaning and
the hash of the signed labels are written to the audit trail. You cannot approve a segmentation
you created.

**Blinded review mode** (Review panel or *View* menu) hides group names, animal IDs and file
names everywhere in the application, for every role. Studies created as *blinded* additionally
hide group allocation from non-administrators.

## 10. Reports

**Reports** tab: choose the study and **Generate DefectFill report**. The PDF (and a CSV) are
built in the background and shown page by page (*Previous*, *Next*, zoom). **Export...** copies
PDF and CSV to a folder; **Approve...** signs the report (reviewers). Reports from an unlicensed
(evaluation) installation carry the watermark "EVALUATION COPY - NOT FOR STUDY DECISIONS".

## 11. Audit trail

**Audit trail** tab (reviewers and administrators): every event with time, user, action and
object; filter by text or object type; select an event to see its details. **Verify chain**
recomputes every hash and reports whether the trail is intact or the first altered event.

## 12. Workflow timing (optional)

*Tools > Record workflow timing for this project* (off by default) records, for each scan,
when it was opened, the first edit, each edit (tool and voxels changed), sign-offs and active
working time (pauses over 60 s are not counted). The data stays in the project database and is
never transmitted. *Tools > Export workflow timing CSV* writes a per-scan summary and the raw
events, for timed user studies.

## 13. Licence

*Help > Licence* shows the licence state, edition, licensee, expiry and features, and this
computer's fingerprint (needed for machine-bound licences). *Install licence file...* checks
the signature offline and installs it for your user account. Without a licence the
application runs in evaluation mode with full functionality and watermarked reports.

## 14. Appearance and layout

* *View > Theme*: light or dark.
* Panels can be moved, tabbed, floated or closed; *View* lists them all.

## 15. Troubleshooting

| Symptom | What to do |
|---|---|
| Sign-in refused | wrong password, inactive user, or 5 failed attempts (locked for 15 minutes) |
| "Voxel spacing ... not confirmed" | enter the spacing in µm and tick *Confirmed* in the wizard |
| Scan marked *needs ROI* | define a cylindrical ROI at the crosshair and analyse again |
| Values *not measured* | the advisor does not support that endpoint for the material/scan; hover for the reason |
| Unexpected error dialog | details are in `error.log` in the settings folder (Linux `~/.config/OsteoQuant`, Windows `%APPDATA%\OsteoQuant`, macOS `~/Library/Application Support/OsteoQuant`) |
| Check an installation | run `osteoquant-desktop-console --selftest` (or `python -m osteoquant.desktop --selftest`); it prints PASS/FAIL per step |
