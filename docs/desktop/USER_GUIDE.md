# OsteoQuant Desktop: user guide

OsteoQuant Desktop analyses preclinical micro-CT scans of bone defects. It separates each scan
into new bone, residual graft and host bone, reports defect-fill endpoints, and keeps a
signed, hash-chained record of every step. It runs entirely on your computer and never connects
to a network.

It is research software: it is not a medical device and has not been validated for GLP or
clinical use. Check every automatic result before you rely on it.

Screenshots of each screen are in `docs/screenshots/desktop/` (for example `02_viewer_light.png`
with the ROI outline and a distance measurement, `15_review_what_changed.png`,
`18_report_signoff.png`, `19_audit_blinded.png`, `20_users.png`, `22_idle_lock.png`).

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

**More users** (*Project > Users...*, administrators only): **Add user...** (user name, full
name, role, initial password), **Deactivate** / **Reactivate**, **Reset password...** (also
clears a temporary lockout and ends the user's sessions) and **Change role...** (not your own).
Every action is recorded in the audit trail. A password set by an administrator (new user or
reset) must be replaced by its owner at the next sign-in, so only the owner knows their signing
password; *Project > Change my password...* changes it at any time (current password required;
other open sessions of the account are signed out).

Account changes reach open sessions at their next action: a deactivated user, or one whose password
was reset, is signed out with a message (unsaved label edits are discarded); a role change takes
effect immediately. Roles are checked at sign-in against the last role change recorded in the audit
trail: a role edited directly in the database is refused (`auth.user_record_mismatch`). Roles:

| Role | Can |
|---|---|
| Analyst | import, analyse, define ROIs, edit labels, generate and export reports |
| Reviewer | view, sign reviews (ROI acceptance, segmentations, reports) as *Scientific reviewer* |
| Study director | as reviewer; signs reports as approver; sees allocation of blinded studies and can unblind them (signed) |
| Administrator | everything, including user administration and unblinding (signed) |

At least two people are needed: an author cannot approve their own ROI, segmentation or report,
nobody who authored a reported segmentation or its ROI can approve the report, and each person
approves a report at most once (separation of duties). Actions your role cannot perform are disabled; hover over them to see why
and which role is required. A reviewer opening a scan sees **READ ONLY** in the Segmentation panel.

**Idle lock**: after 15 minutes without keyboard or mouse input (administrators can change this
in *Project > Idle lock...*; 0 turns it off) the window hides the project and asks for your
password. *Project > Lock now* (Ctrl+L) locks it immediately. The lock covers the whole
application: open dialogs are cancelled (for example *Users*, a signature dialog), other windows
such as the import wizard are hidden until you unlock, and no keyboard, mouse or shortcut input
reaches anything but the lock page. Five wrong passwords lock the account for 15 minutes, as at
sign-in. Unsaved label edits are kept while locked. Lock, unlock and failed attempts are audited.

## 3. Organise studies

The **Project** panel (left) shows *Study > Group > Animal > Timepoint > Scan*.

* *Study > New study*: name, species, defect model (condyle, calvarial, segmental), graft
  material(s), data class (own research, customer, public dataset, synthetic/demo; printed on
  every report page) and whether the study is blinded.
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
   *Confirmed*. The row *Spacing for all scans without file spacing* is empty until you type a
   value (no default is assumed); with *isotropic* ticked the z value is used for y and x,
   otherwise type all three. *Apply and confirm* is enabled only once the values are typed. You
   cannot continue until every scan has explicit spacing. The lower table lists the metadata found in
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
| Change slice | slider below each view, mouse wheel, arrow keys, Page Up/Down, Home/End |
| Zoom | Ctrl + wheel (about the pointer); **F** fits the slice to the view |
| Pan | middle-drag or Shift + left-drag |
| Window / level | right-drag (horizontal = width, vertical = level), or the *Display* panel presets and fields |
| Maximise a view | double-click it (again to restore) |
| Voxel readout | *Voxel* panel: voxel index, position in mm, intensity, label |
| Measure a distance | *Distance* tool (M, toolbar or *Display* panel): drag in a slice view; the length is shown in µm/mm on the line and in the status bar. Esc or *Clear* removes the lines |
| Show/hide the ROI outline | R, *View > Show ROI outline* or the *Display* panel |

Keyboard keys for tools and slices act while a viewer panel has focus (click a slice view
first), so they never interfere with typing in the project tree. *Help > Keyboard shortcuts*
(F1) lists them all. The focused control always has a visible outline.

Every slice view shows its orientation, slice number and depth in mm, the window, the zoom and
a scale bar in µm or mm. Window presets (*Auto*, *Bone*, *Graft (dense mineral)*, *Soft tissue*,
*Full range*) are defined by the same rule on each scan's own histogram, because grey values are
uncalibrated unless an HA calibration is recorded.

**Analysis ROI**: the volume the endpoints are computed in is drawn as a **yellow outline** on
every slice and as a yellow wireframe in the 3D panel, with a key in each view. Review it there
before accepting it (section 9).

**Display panel**: segmentation version, overlay on/off, for each class (new bone, residual
graft, host bone, uncertain) visibility, colour and opacity, the **palette** (*Okabe-Ito* or
*Colour-blind safe, high contrast*: blue / orange / white / black, so that no class depends on
red-green hue) and **Outline only** (draws class boundaries, for judging edges).

Saving a revision or an analysis finishing for the open scan reloads it **without** moving the
crosshair or changing window/level, zoom or the 3D camera.

**3D panel**: *Surfaces* (label classes as smoothed surfaces), *Volume* (volume rendering of a
downsampled image) or both. Drag to rotate, wheel to zoom, *Reset* to restore the view. After
editing labels, *Update* re-extracts the surfaces.

**Oblique** panel (View menu): a plane through the crosshair tilted about x and y.

**Screenshot**: *File > Export screenshot* saves the four views as PNG.

## 6. Run the analysis

Select scans, an animal, a group or a whole study in the tree and choose **Analyse...**.

* **Defect model** and **nominal defect diameter** help the automatic ROI detection.
* **Segmentation**: Multi-Otsu (classical). Locked U-Net models appear here when their ONNX
  export and runtime are installed. A model trained only on synthetic phantoms is labelled
  **SYNTHETIC-TRAINED — research only** in the list and with a red chip below it; the same chip
  appears in the viewer, in the Results *Method* column and in the Review panel whenever its
  results are shown, matching the banner of the PDF report.
* *Graft is brighter than new bone* is available (and ticked) only for radiopaque graft materials.
* **Graft material**: used by the measurement-support advisor to decide which endpoints can
  be separated reliably for this material and scan. Choose *Unspecified* if unknown, or *No graft
  (empty defect)* for empty-defect controls.
* **Time since implantation**: from each scan's timepoint (days, or a label such as "Week 4"),
  a number of weeks for all selected scans, or *Unknown*. Resorbable materials are separated by
  intensity only at a known timepoint of 4 weeks or less. The resolved weeks and their source are
  recorded with the analysis and printed in the report.

Each scan runs as a background job (**Jobs** panel; progress also in the status bar). You can
keep working, and **Cancel** stops a job at its next stage. Failed jobs show a plain-language
message; double-click for the technical details. Closing the project or the application with
jobs running cancels them and waits at most 3 seconds; a library step that is still running
finishes in the background and the project closes when it has.

A cancelled job leaves nothing half-done: a cancelled import removes the partly imported scan (the
same source can be imported again), a cancelled label revision stores no new version, and a
cancelled report leaves no report entry. Version numbers are allocated atomically, so two jobs on
the same scan never collide.

If the ROI cannot be detected the scan is marked *needs ROI*: place the crosshair at the defect
centre and use *Study > Define cylindrical ROI at crosshair* (or **Edit ROI...** in the Review
panel: radius, extent, reason). After saving you are offered to re-analyse the scan with the new
ROI.

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
* The history, the unsaved-change summary and **Save as new revision...** stay pinned at the
  bottom of the Segmentation panel, always visible.
* **Save as new revision...** (Ctrl+S): enter the reason. A new *corrected* version is stored;
  the original is never overwritten. Endpoints are recomputed with the same ROI. Your name, the
  reason and the per-class voxel changes go into the audit trail.

## 8. Results

The **Results** tab lists every scan of a study with its endpoints and units: defect TV
(mm³), new bone volume (mm³), new bone BV/TV (%), residual graft (%), mineralised (%),
uncertain (%), Tb.Th, Tb.Sp (µm), Tb.N (1/mm) and defect coverage (%). Further columns: **QC**
verdict, **ROI** (automatic/manual and its acceptance state), **Method** (with the
SYNTHETIC-TRAINED label where it applies), segmentation version and **Review** state. Rows are
sorted by scan, ascending.

The **Support** column combines every state honestly:

* **supported**: every endpoint is supported, QC is *suitable* and any automatic ROI that asked
  for review has been accepted;
* **⚠ flagged**: some endpoints need caution (orange values), for example QC verdict *review*,
  an automatic ROI not yet accepted, or an advisor condition. A scan whose QC asks for review is
  never shown as supported;
* **✖ not supported**: no endpoint can be reported (or the analysis failed);
* **not analysed**: the scan has not been analysed yet.

Per endpoint, **✖ not assessed** means that no measurement-support assessment exists for a graft
or new-bone endpoint (advisor output missing or not recognised); it is never shown as supported.
A scan without a QC result is *flagged* ("QC not run").

An endpoint that is not supported or not assessed is shown as *not measured* (italic) and **never with a
number**, whatever was stored; this is the same in the CSV export and the PDF report. Select a
row: the pane below the table lists every endpoint with its status, value and the reasons, each
reason once. Double-click a row to open the scan. **Export CSV** writes the table with the
per-endpoint support and reasons; not-measured endpoints have an empty value. In evaluation mode
the CSV starts with the evaluation notice.

## 9. Review and sign-off

The **Review** panel works on the open scan:

1. **Analysis ROI**: version, automatic or manual, confidence and state (*awaiting acceptance*,
   *accepted by ... at ...*, ...). Check the yellow outline on the slices and in 3D, then
   **Accept ROI...** (reviewer, study director or administrator; not the person who created the
   ROI or ran the analysis that created it). This is an electronic signature with your password;
   it records the ROI definition hash in the audit trail and clears the *ROI not yet accepted*
   caution from the results. **Edit ROI...** defines a new manual ROI instead; it needs a typed
   reason and, like an automatic ROI, must be accepted by a second person before results measured
   in it are free of the caution.
2. **Segmentation versions**: version, kind, method, author and latest decision.
3. **What changed in the selected version**: parent version, editor, time, the **reason for the
   edit**, the operations, the **voxel and volume (mm³) change per class**, and every endpoint
   **parent → this version** (not-measured endpoints never show a number). Tick **Highlight
   changes vs parent** to show every changed voxel in magenta in the slice views.
4. **Review history** of the selected version with signature role, decision and meaning.

**Approve**, **Request changes** or **Reject** sign the selected version: state the meaning and
re-enter your password. The signature, its meaning and the hash of the signed labels are written
to the audit trail. *Approve* is disabled, with an explanation, for a version you created.

**Blinded review mode** (Review panel or *View* menu) hides group allocation, animal IDs, file
names and acquisition metadata everywhere, for every role: in the tree, Results, viewer, QC,
Review, the **Audit trail** (details are masked) and the **report preview**. Scans and animals
are shown with random codes (for example *Scan S-7K3Q*, *Animal A-P7BK*) that are stored per study
in the project, stay the same across sessions and do not follow import or database order; the
tree and the Results table and CSV are sorted by code, job titles use the codes, and database
IDs of segmentations, ROIs and measurements are masked in the audit view.

**Study-level blinding.** For a study created as *blinded*, blinded review mode is always on for
every role that may not see allocation (analyst, reviewer, viewer): the toggle is locked, reports
they generate are blinded, unblinded reports cannot be exported by them and the audit export is
masked. Only the study director or an administrator can unblind the study, with *Study > Unblind
study...*: a signed action (reason and password) recorded as `study.unblind` in the audit trail;
it unblinds the study for everyone.

## 10. Reports

**Reports** tab: choose the study and **Generate defect-fill report** (disabled until the study
has analysed scans). The PDF (and a CSV) are built in the background and shown page by page
(*Previous*, *Next*, zoom). Endpoints that are not supported are reported as *not measured* with
the reason. **Export...** copies PDF, CSV and, when present, the signed copy to a folder.

A report generated while **blinded review mode** is on is a *blinded report*: animal IDs, file
names, groups, acquisition metadata and database IDs are replaced by the blinded codes (figures
included; the source-file hash is omitted and no unblinded figure is written). In blinded mode the
preview of a report that was not generated blinded is hidden, and *Approve* and *Export* are
disabled for it (nobody approves content they cannot see).

Before any report is approved, and before its signed copy is rendered, the PDF and the stored
report bundle are re-hashed and compared with the SHA-256 values recorded at generation (in the
project database and in the audit trail). A modified or missing file refuses the signature
(`report.integrity_failed`); generate a new report. Reports generated by earlier versions have no
bundle hash and must be regenerated before approval. Generating a report waits until running
analysis, import and save jobs have finished; the report is built from one consistent snapshot,
each specimen matched to its own scan and segmentation.

**Sign-off**: **Approve...**, **Request changes...** and **Reject...**. When signing choose the
signature role your role allows (*Scientific reviewer* or *Study director / sponsor
representative*). *Approve* is disabled, with the reason, when you generated the report, when a
reported segmentation is not yet approved, or when the report was generated before all
segmentations were approved (generate a new one). Approval is also refused when you authored a
reported segmentation or its ROI, or when you have already approved the report in another role. Each signature produces a **signed copy** of
the report: the same content with the signature rows filled from the recorded approvals (role,
name, meaning, decision, time) and a note naming the SHA-256 of the original PDF, which is never
modified. Tick *Preview the signed copy* to view it. The *Analyst* row names the report author.

Reports from an unlicensed (evaluation) installation carry the watermark
"EVALUATION COPY - NOT FOR STUDY DECISIONS".

## 11. Audit trail

**Audit trail** tab (reviewers, study directors and administrators): every event with time,
user, action and object; filter by text or object type; select an event to see its details.
**Verify chain** recomputes every hash and reports whether the trail is intact or the first
altered event. **Export...** (also *Tools > Export audit trail*) writes every event to CSV or JSON
(by file extension) together with the chain-verification result (OK, or the first broken event),
the head hash, who exported it and when. The CSV includes `org_id` and `prev_hash`, and the
details in canonical form, so every row can be re-verified from the file alone. The export is
itself audited, with the SHA-256 of the exported file. In blinded review mode the export is masked
like the view; masked rows are marked (`masked`) because their hashes cannot be reproduced from the
masked content.

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

* *View > Theme*: light or dark. Both meet WCAG AA contrast (4.5:1) for status text, including
  *not measured*; status is also given by a symbol (⚠ flagged, ✖ not supported), not by colour
  alone.
* Panels can be moved, tabbed, floated or closed; *View* lists them all. The Quality control
  panel is shown on the Viewer tab only.

## 15. Troubleshooting

| Symptom | What to do |
|---|---|
| Sign-in refused | wrong password, inactive user, or 5 failed attempts (locked for 15 minutes) |
| "Voxel spacing ... not confirmed" | enter the spacing in µm and tick *Confirmed* in the wizard |
| Scan marked *needs ROI* | define a cylindrical ROI at the crosshair and analyse again |
| Values *not measured* | the endpoint is not supported for the material/scan (advisor, uncertainty, missing thickness); select the row in Results for the reasons |
| Everything *flagged* | read the reasons: typically QC verdict *review* or an automatic ROI awaiting acceptance (Review panel > *Accept ROI*) |
| A button is greyed out | hover over it: the tooltip says which role it needs or why it cannot succeed now |
| Window shows *Locked* | idle lock: enter your password (*Close project* discards unsaved edits) |
| Unexpected error dialog | details are in `error.log` in the settings folder (Linux `~/.config/OsteoQuant`, Windows `%APPDATA%\OsteoQuant`, macOS `~/Library/Application Support/OsteoQuant`) |
| Check an installation | run `osteoquant-desktop-console --selftest` (or `python -m osteoquant.desktop --selftest`); it prints PASS/FAIL per step |
