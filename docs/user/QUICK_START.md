# Quick start: from first launch to first report

> **Status.** Research product: not validated on real graft materials; not a medical device; no GLP/Part 11
> compliance claimed. Check every automatic result before relying on it.

This walk-through takes about 20 minutes. It links to the [desktop user guide](../desktop/USER_GUIDE.md) for
details instead of repeating them. Installation: [INSTALLATION.md](INSTALLATION.md).

## 0. Get a scan to practise on

Use one of your own scans, or generate a synthetic phantom with known ground truth (needs a source install, see
[INSTALLATION.md](INSTALLATION.md#from-source-any-platform-for-developers-and-evaluators)):

```bash
osteoquant phantom --model condyle --material beta_tcp --out practice/R01_week4.nii.gz
```

This writes the image and a `*_labels.nii.gz` truth file. Import only the image. Synthetic phantoms are for learning
the workflow; their results say nothing about real tissue.

## 1. Start the application and check it

Start **OsteoQuant**. The start page shows *New project*, *Open project* and recent projects, plus the version and
licence state. "Evaluation mode (no licence installed)" is expected: every function works and reports are
watermarked (see [LICENSING_AND_ADMIN.md](LICENSING_AND_ADMIN.md)).

Optional: run the self-test once (`osteoquant-desktop-console --selftest`). All 8 steps should print PASS.

## 2. Create a project

*File > New project*. Give a name, a **new empty folder**, your user name, full name and a password (at least 10
characters with an upper-case letter and a digit). You become the project administrator.

A project is a folder: keep it on a local or backed-up drive ([DATA_PROTECTION.md](DATA_PROTECTION.md)).
User guide: [§2](../desktop/USER_GUIDE.md#2-create-or-open-a-project).

## 3. Create a study and groups

*Study > New study*: name, species, defect model (condyle, calvarial or segmental), graft material(s), the **data
class** (own research data, customer data, public dataset, or synthetic/demo data; printed on every report page), and
whether the study is blinded. Then *Study > Add group* for each treatment arm. Animals and timepoints are created during
import. User guide: [§3](../desktop/USER_GUIDE.md#3-organise-studies).

## 4. Import scans

*File > Import scans* opens a four-step wizard ([§4](../desktop/USER_GUIDE.md#4-import-scans)):

1. **Select scans** (files or folders).
2. **Metadata and voxel spacing.** Every physical number depends on spacing. If the source is *ASSUMED by reader*
   or *MISSING*, type the spacing in µm (z, y, x) and tick *Confirmed*; you cannot continue otherwise.
3. **Assign** animal ID, group, timepoint label and day.
4. **Import and QC.** Each scan is copied into the project with its SHA-256 and checked. Results: *imported*,
   *flagged* (QC asks for review) or *rejected* (with the reason).

Look at the QC panel: deterministic checks are facts about the file; heuristic checks use developer-chosen
thresholds and are prompts for attention, not standards.

## 5. Look at the scan

Double-click the scan. Scroll slices with the wheel, zoom with Ctrl + wheel, set window/level by right-dragging,
press **F** to fit. The voxel panel shows position (mm), grey value and label. Grey values are uncalibrated unless
an HA calibration was recorded. User guide: [§5](../desktop/USER_GUIDE.md#5-view-a-scan).

## 6. Analyse

Select the scan (or an animal, group or study) and choose **Analyse...**:

* **Defect model** and, if you know it, the **nominal defect diameter** (helps automatic ROI detection).
* **Segmentation:** the advisor threshold is the default and the only method that carries measurement support; with multi-Otsu or a model, graft and new-bone values are reported as not measured.
* **Graft material:** choose the material actually implanted, *Unspecified* if unknown, or *No graft (empty
  defect)* for empty-defect controls. The measurement-support advisor uses this to decide which endpoints can be
  reported. If you are unsure, *Unspecified* is the conservative choice: graft and new-bone endpoints will not be
  reported.
* *Graft is brighter than new bone* is ticked by default; untick it only for a graft that is darker than new bone.
* **Time since implantation:** by default taken from each scan's timepoint (its days, or a label such as "Week 4" or
  "Day 14"). Give timepoints days when you import, or enter the weeks here. Resorbable materials (β-TCP, calcium
  sulfate, bioactive glasses, composites) are separated by intensity only at a known timepoint of 4 weeks or less; an
  unknown timepoint means those endpoints are not reported. The value used is printed in the report.

The job runs in the background (**Jobs** panel). If the ROI cannot be found the scan is marked *needs ROI*: place the
crosshair at the defect centre, use *Study > Define cylindrical ROI at crosshair*, and analyse again with *Use the
latest saved ROI* ticked. User guide: [§6](../desktop/USER_GUIDE.md#6-run-the-analysis).

## 7. Read the results, including what was not measured

Open the **Results** tab. The **Support** column reads *supported*, *flagged*, *not supported* or *not
analysed*. Endpoints the advisor does not support show **not measured**; hover for the reason. This is expected for
many materials, for example β-TCP, calcium sulfate and DBBM, and for noisy or blurred scans of any material.
Bone-derived grafts (allograft, autograft, DBM) are refused by every mechanism, with or without a day-0 scan: use
histology to separate them from new bone. The desktop application has no day-0 workflow.

Total mineral volume is reported only when the scan's blur and noise allow it, so expect scans with no volume at all.
In the pre-registered held-out simulation S1H4 (SYNTHETIC, shipped advisor), new-bone volume was never supported, total
mineral volume supported in 2% of specimens (β-TCP at one imaging condition only), and no volume endpoint supported
for 89% of specimens; with the material set to Unspecified nothing was supported. See
[MATERIALS_AND_SUPPORT.md](MATERIALS_AND_SUPPORT.md).

## 8. Correct the segmentation

Open the scan, choose a tool in the **Segmentation** panel (brush **B**, eraser **E**, region grow **G**, fill holes
**H**), pick the class and edit. Ctrl+Z undoes. When done, **Save as new revision** (Ctrl+S) and enter the reason.
The original stays untouched; endpoints are recomputed with the same ROI; the change goes into the audit trail.
User guide: [§7](../desktop/USER_GUIDE.md#7-correct-the-segmentation).

## 9. Review and sign off (needs a second user)

Authors cannot approve their own segmentation, so sign-off needs a reviewer account. **The desktop application has
no user-management screen yet.** Until it does, an administrator can add a reviewer from a source install (see
[LICENSING_AND_ADMIN.md](LICENSING_AND_ADMIN.md#adding-users)). The reviewer then opens the project, opens the scan,
and in the **Review** panel chooses *Approve*, *Needs changes* or *Reject*, states the meaning of the signature and
re-enters their password. User guide: [§9](../desktop/USER_GUIDE.md#9-review-and-sign-off).

You can generate a report without sign-off; the report then records its status as unreviewed (automated) instead
of reviewed, and lists the reviewers and the meaning of their signatures when there are any.

## 10. Generate the report

**Reports** tab: choose the study and **Generate DefectFill report**. When the job finishes, page through the
preview, then **Export...** to copy the PDF and CSV to a folder. Reviewers can **Approve...** the report.

Check the report's list of endpoints that were not measured and why. In evaluation mode every page carries
"EVALUATION COPY - NOT FOR STUDY DECISIONS". User guide: [§10](../desktop/USER_GUIDE.md#10-reports).

## 11. Verify the audit trail

**Audit trail** tab (reviewers and administrators): **Verify chain** should report that every hash was recomputed
and linked, and show the head hash. Write the event count and head hash down somewhere outside the project; it lets
you detect later truncation ([DATA_PROTECTION.md](DATA_PROTECTION.md#audit-trail)).

## Next

* How the numbers are computed: [SCIENTIFIC_METHODS.md](SCIENTIFIC_METHODS.md)
* Problems: [TROUBLESHOOTING.md](TROUBLESHOOTING.md) · Questions: [FAQ.md](FAQ.md) · Terms: [GLOSSARY.md](GLOSSARY.md)
