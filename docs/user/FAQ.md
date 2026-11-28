# Frequently asked questions

> **Status.** Research product: not validated on real graft materials; not a medical device; no GLP/Part 11
> compliance claimed.

### Is OsteoQuant validated?

No. The computational stage (A) has run on synthetic phantoms and public real data, with open items. No physical
phantom, partner or animal-study validation (stages B–F) has started, and no release gate is met. Separation of
residual graft from new bone has been tested only in simulation. See the validation programme,
[validation/VALIDATION_PROGRAM.md](../../validation/VALIDATION_PROGRAM.md).

### Can I use it in a GLP study or for a regulatory submission?

Not as delivered. No GLP or 21 CFR Part 11 compliance is claimed. The audit trail, signatures and access control are
technical controls; regulated use would need your organisation's computerised-system validation, procedures and QA.

### Is it a medical device?

No. It is research software for preclinical (animal) micro-CT. It is not intended for clinical use.

### Why does my report say "not measured" for new bone and residual graft?

Because the measurement-support advisor decided that, for this material and this scan, graft and new bone cannot be
told apart reliably. Hover over the value in the Results tab, or read the report's list of suppressed endpoints, for
the reason. This is expected for β-TCP, calcium sulfate, allograft, autograft, DBBM, DBM, composites, metals and
any *Unspecified* material without a day-0 scan, and for noisy scans of any material. See
[MATERIALS_AND_SUPPORT.md](MATERIALS_AND_SUPPORT.md).

### Can I see the value anyway?

Raw values are kept in the audit record for research and traceability, but reports and exports use the reported view,
in which unsupported endpoints are blank. A number the advisor refused is one you should not use for study
decisions.

### What is always reported?

Total mineral volume (new bone + graft) and mineralised fraction, whenever the scan's noise is acceptable and new bone
can be separated from soft tissue. These do not require telling graft from new bone.

### Which graft materials does it know?

The knowledge base holds 16 materials (HA, β-TCP, BCP, calcium sulfate, bioactive glasses 45S5 and S53P4, DBBM,
allograft, autograft, DBM, collagen sponge, PLGA, PCL, polymer–ceramic composite, magnesium, titanium). The desktop menu
offers nine of them plus *Unspecified* and *No graft*. Their profiles are physics plus assumed porosity; none is
measured yet.

### My material is not listed. What should I do?

Choose *Unspecified*. Graft and new-bone endpoints will be refused and total mineral reported. To go further, follow
the material-characterisation workflow in [MATERIALS_AND_SUPPORT.md](MATERIALS_AND_SUPPORT.md#unsupported-material-and-material-characterisation-workflow).

### Does a day-0 scan solve the problem?

Sometimes, in principle. In simulation a registered day-0 footprint works well when the graft only shrinks in place,
but its graft Dice falls from 0.80 to 0.535 with 50 µm of granule motion (Experiment L3), and bone formed inside a
resorbing graft's footprint is counted as graft. The desktop application has no day-0 workflow yet. See
[SCIENTIFIC_METHODS §5](SCIENTIFIC_METHODS.md#5-longitudinal-day-0-method-and-its-limits).

### Does it need a GPU or the internet?

Neither. It runs on CPU and makes no network connections. Classical segmentation is the default.

### Does it send my data anywhere?

No. There is no telemetry, update check or licence server. Workflow timing, if you switch it on, is stored only in the
project. See [DATA_PROTECTION.md](DATA_PROTECTION.md).

### Which file formats can I import?

Zeiss TXM/TXRM, DICOM series, NIfTI, NRRD, Zarr, TIFF (multi-page or slice folders), PNG/BMP slice folders, MetaImage
(build with SimpleITK) and NumPy. Voxel spacing must come from the file or be confirmed by you.

### Are densities in mgHA/cm³?

Only when an HA-phantom calibration is recorded for the scan. Otherwise grey values are uncalibrated and density
endpoints are not reported.

### How accurate is morphometry?

Exact on analytic test objects (plates exact for even voxel counts). On 8 public trabecular cubes, Tb.Th agreed with
Scanco IPL with ICC(2,1) 0.983 (mean −2.4%) — but the border convention was chosen after seeing those cubes, so a
held-out confirmation is still pending.

### How much analyst time does it save?

Unknown. It has not been measured. An earlier modelled figure of about 78% came from assumed effort constants and is
not a result. The application can record real interaction timing, locally and only if you enable it.

### Does it work on Windows and macOS?

Builds are produced by CI, but they have never been run in this project and are unsigned (signing and notarisation
await the publisher's credentials). Linux is the tested platform. See [INSTALLATION.md](INSTALLATION.md).

### Do I need a licence?

No, to evaluate. Without one the application runs in evaluation mode with all functions and watermarked reports.
Production licences cannot be issued yet. See [LICENSING_AND_ADMIN.md](LICENSING_AND_ADMIN.md).

### Why can't I approve my own segmentation?

Separation of duties: an author cannot approve their own work. A second user with the reviewer or administrator role
must sign. Administrators add users under *Project > Users...*; see
[LICENSING_AND_ADMIN.md](LICENSING_AND_ADMIN.md#adding-users).

### Are the trained models usable on my scans?

Not as shipped. Locked models are not included in the bundle, synthetic-trained models fail on real scans (Dice 0.379
zero-shot on real dog micro-CT, bone vs background), and no model has material-specific validation evidence, so the
advisor never accepts a texture model for graft separation.

### Is histology supported?

Not in the desktop. The histology module is experimental (section-to-slice registration overlay, graft-void area);
H&E bone-area quantification was removed from reports because agreement was weak.
