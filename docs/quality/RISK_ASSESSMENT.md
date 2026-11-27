# OsteoQuant: Risk Assessment (FMEA-style)

| Field | Value |
|---|---|
| Document ID | OQ-QMS-RA-001 |
| Version | 0.2 (DRAFT), Generation-2 desktop re-baseline |
| Date | 2026-11-27 |
| Scope | Scientific-validity and data-integrity risks of OsteoQuant Desktop (offline workstation application) and its analysis library |
| Method | FMEA; risk-based approach per OECD GLP No. 17 ¶12–14 and GAMP 5 (benchmarks only) |
| Related | URS.md v0.2, FUNCTIONAL_SPEC.md v0.2, traceability_matrix.csv |

> **Status: DRAFT. Not approved. No claim of 21 CFR Part 11 compliance, GLP compliance, computerised-system validation or regulatory acceptance.**

## 1. Scoring
- **S – Severity** (impact on scientific conclusions / record integrity): 1 negligible · 2 minor, detectable cosmetic · 3 wrong secondary result · 4 wrong primary outcome or loss of attributability · 5 undetected wrong study conclusion, data loss, or undetectable falsification.
- **O – Occurrence** (without the listed controls): 1 remote … 5 frequent.
- **D – Detectability** (before results are used): 1 almost certainly detected … 5 not detectable.
- **RPN = S × O × D.** Action required if RPN ≥ 40 or S = 5.
- **Control status** is taken from `traceability_matrix.csv`: **V** all mapped FS rows VERIFIED, **P** some verification, **G** control not implemented or not tested. Residual scores assume the listed controls work; where the status is P or G that assumption is **not yet supported by evidence**.
- Patient safety is not applicable (non-clinical). "Harm" means wrong scientific conclusions, lost value of animal studies (3Rs) or loss of record integrity.

## 2. What changed for the desktop
- The workstation OS is inside the trust boundary. Users who can write the project folder can edit the SQLite file, scan stores or `models/validation_records.json` outside the application. Occurrence of RSK-20 and the new RSK-48 rises; detection relies on the hash chain, content hashes and anchors.
- There is no user-administration UI in the desktop, so additional named accounts are hard to create. Occurrence of shared-account use (RSK-23) rises.
- Workstation clocks replace a managed server clock (RSK-22). Local disks replace managed storage (RSK-30).
- RSK-25 (cross-tenant leakage) is **retired** for the desktop: one organisation per project. It applies again if a hosted service is offered.
- New risks RSK-37 to RSK-48 cover measurement support, validation records, material characterisation, longitudinal QC, licensing, workflow timing, offline operation, untrusted inputs, background jobs, editing and direct file access.

## 3. FMEA table

| Risk ID | Process step | Failure mode | Effect | Cause | S | O | D | RPN | Controls (URS / FS) | Status | Res. S/O/D/RPN |
|---|---|---|---|---|---|---|---|---|---|---|---|
| RSK-01 | Import | Wrong voxel spacing used | All volumes and thicknesses wrong by a scale factor | Missing/ambiguous header, unit confusion | 5 | 3 | 4 | 60 | URS-022/023; FS-023-1/2 explicit confirmed spacing, spacing source stored | V (FS-023), P (FS-022) | 5/1/2/10 |
| RSK-02 | Import | Anisotropic voxels treated as isotropic | Biased thickness/separation | Simplified algorithm | 4 | 2 | 4 | 32 | Per-axis spacing in morphometry and brush; anisotropic phantom tests | V | 4/1/2/8 |
| RSK-03 | Import | Specimen / time point mix-up | Data assigned to wrong animal or group | Manual entry error, file-name guessing | 5 | 3 | 4 | 60 | URS-025; FS-025-1 duplicate rejection; FS-025-2 second-scan flag; SOP-001 second-person check | P (FS-025-2 G) | 5/2/2/20 |
| RSK-04 | Import/storage | Source or stored scan altered or corrupted | Results not traceable to raw data | Disk fault, manual edit, missing chunks | 5 | 2 | 3 | 30 | URS-020/021/024; FS-020-1 hashes; FS-021-1 hash check on read; FS-021-2 on-demand check | P | 5/1/2/10 |
| RSK-05 | QC | Unsuitable scan analysed without notice | Artefact-laden results | No gating (flag only) | 4 | 3 | 3 | 36 | URS-032; FS-032-1 block with override | G | 4/3/2/24 (until FS-032-1 exists) |
| RSK-06 | ROI | Wrong ROI placement or size | Defect metrics invalid | Detection error, operator practice | 5 | 3 | 3 | 45 | URS-040/041/042; FS-040-1; FS-042-1/2 three-plane view and confirmation; SOP-002; PQ-03 | P (FS-042-2 G) | 5/2/2/20 |
| RSK-07 | ROI | ROI inconsistent across time points | Spurious change over time | Repositioning | 4 | 3 | 3 | 36 | URS-182; FS-182-1 ROI propagation with registration QC | V (library), desktop G | 4/2/2/16 |
| RSK-08 | Segmentation | Silent label-mapping error | Primary outcome inverted | Model with different class order; legend hard-coded | 5 | 2 | 5 | 50 | URS-050/054; FS-054-1 value check; FS-054-2 model label-map check | P (FS-054-2 G) | 5/1/3/15 |
| RSK-09 | Segmentation | Residual graft classified as new bone | Over-estimated bone formation | Intensity overlap, unfamiliar material | 5 | 4 | 4 | 80 | URS-150–153 measurement support with abstention; URS-160 validation records; SOP-003 review; PQ per material | V (advisor rules), PQ not executed | 5/2/2/20; **highest residual scientific risk** while PQ and physical validation are missing |
| RSK-10 | Segmentation | Wrong or altered model used | Results not comparable / unrepeatable | Unversioned swap | 5 | 3 | 4 | 60 | URS-051/111/112; FS-111-1 hash check; FS-112-1 release status; SOP-007 | V (hash), G (release status) | 5/1/2/10 |
| RSK-11 | Segmentation | Distribution shift degrades accuracy | Systematic bias | Use outside validated domain | 5 | 3 | 4 | 60 | URS-055 abstention; URS-150 advisor; URS-160 domain-bound validation records | V/P | 5/2/2/20 |
| RSK-12 | Correction | Corrections biased by group knowledge | Bias toward hypothesis | Unblinded analysts | 5 | 3 | 5 | 75 | URS-075/076; FS-075-1/3/4 masking and blinded mode; FS-075-2 unblinding; FS-076-1; SOP-009 | V (masking), P/G (unblinding, post-unblinding flag) | 5/2/3/30 |
| RSK-13 | Correction | Correction overwrites original | Loss of original | Design shortcut | 4 | 2 | 4 | 32 | URS-052/053; FS-052-1 new version per save; FS-053-1 | P/V | 4/1/2/8 |
| RSK-14 | Morphometry | Algorithm error | Biased metrics | Implementation defect | 5 | 3 | 3 | 45 | URS-062 analytic phantom suite; Experiment G | V | 5/1/2/10 |
| RSK-15 | Morphometry | Density without calibration | Meaningless BMD/TMD | Missing phantom | 4 | 3 | 3 | 36 | URS-063; FS-063-1 | V | 4/1/1/4 |
| RSK-16 | Statistics | Grouping/exclusion chosen after seeing results | False positives | Post-hoc analysis | 5 | 3 | 4 | 60 | URS-070/072 SAP lock, exclusions with reason | G (SAP), V (all scans listed) | 5/3/3/45 until SAP exists |
| RSK-17 | Statistics | Non-reproducible or wrong statistics | Results differ or are wrong | Library change; formula error | 3 | 3 | 3 | 27 | URS-071; FS-071-2 reference tests; FS-071-1 provenance | V/G | 3/1/3/9 |
| RSK-18 | Reporting | Report values do not match data / stale report | Published numbers wrong | Report before correction | 5 | 2 | 4 | 40 | URS-080/082/093; FS-093-1 hash-bound signatures; FS-082-1 regeneration | P/G | 5/2/3/30 |
| RSK-19 | Reporting | CSV locale/precision or formula corruption | Values mis-parsed; spreadsheet code execution | Locale writer; Excel | 4 | 3 | 3 | 36 | URS-083; FS-083-1/2 | P (FS-083-1 G) | 4/2/2/16 |
| RSK-20 | Audit trail | Audit trail altered by direct DB edit | Falsification undetected | OS user edits the SQLite file (desktop: every project user has file access) | 5 | 3 | 4 | 60 | URS-102/103/017; triggers; hash chain; FS-102-2 anchor export; SOP-005; OS permissions | V (chain), P (anchor in desktop), G (OS control) | 5/2/2/20 |
| RSK-21 | Audit trail | Whole chain regenerated | Tamper evidence defeated | Hash chain without external anchor | 5 | 2 | 5 | 50 | FS-102-2 anchors stored outside the project | P | 5/1/3/15 |
| RSK-22 | Audit trail | Incorrect timestamps | Contemporaneity questioned | Unsynchronised workstation clock | 3 | 3 | 3 | 27 | URS-106; FS-106-1 UTC; FS-106-2 IQ clock check | V/G | 3/2/2/12 |
| RSK-23 | Access | Shared accounts / credential sharing | Loss of attributability | No user administration in the desktop; convenience | 4 | 4 | 4 | 64 | URS-010/013/016; FS-010-3 user management; FS-013-3 idle lock; FS-092-2 re-auth lockout; SOP-008 | G (FS-010-3, FS-013-3), P (FS-092-2) | 4/3/3/36 (procedural residual) |
| RSK-24 | Access | Missing permission check | Unauthorised edits | Function lacking guard | 5 | 2 | 3 | 30 | URS-011; FS-011-1 Store.require; FS-011-2 desktop gating | V/G | 5/1/2/10 |
| RSK-25 | Access | Cross-tenant data leakage | — | — | — | — | — | — | **Retired for the desktop** (one organisation per project). Re-open for a hosted deployment. | — | — |
| RSK-26 | Signatures | Signature on changed record / repudiation | Approval does not reflect content | No hash link; no re-auth | 4 | 2 | 4 | 32 | URS-091/092/093; FS-092-1 re-auth; FS-093-1 hash binding | V/P | 4/1/2/8 |
| RSK-27 | Configuration | Parameter change not captured | Irreproducible results | Defaults changed | 4 | 3 | 4 | 48 | URS-110; FS-110-1 snapshot linked to measurement | P | 4/2/3/24 |
| RSK-28 | Computation | Non-determinism | Re-run differs | Threading, ONNX/GPU | 3 | 3 | 3 | 27 | URS-113; Experiment P | P | 3/2/2/12 |
| RSK-29 | Dependencies | Library update changes numerics or adds a vulnerability | Silent metric shift; exploit | Unpinned dependencies (QA-024) | 4 | 3 | 4 | 48 | URS-131; regression on analytic/golden tests; pip-audit | P | 4/2/2/16 |
| RSK-30 | Data management | Project lost (local disk failure, no backup) | Data loss | Local storage; no built-in backup | 5 | 3 | 4 | 60 | URS-120/121; FS-120-1; SOP-006 folder backup and restore test | P | 5/2/2/20 |
| RSK-31 | Data management | Premature deletion | Raw data lost within retention | Misconfiguration, malicious | 5 | 2 | 3 | 30 | URS-122/123; FS-122-1 retention lock (G); FS-123-1 permission + reason + audit | P/G | 5/2/2/20 |
| RSK-32 | Data management | Concurrent or interrupted writes corrupt the store | Lost/inconsistent records | Two instances on one project; network share; crash | 4 | 2 | 3 | 24 | URS-125; WAL, single locked connection, `BEGIN IMMEDIATE`; FS-125-1 corruption detection; FS-125-2 second-instance detection | V/G | 4/2/2/16 |
| RSK-33 | Archive | Data unreadable later | Study cannot be reconstructed | Proprietary formats; software obsolescence | 4 | 2 | 4 | 32 | URS-124 open-format archive with manifest; retain installers of each version | P | 4/1/3/12 |
| RSK-34 | Use | Outputs used as if validated (GLP study, submission) | Data rejected | Misunderstanding of status | 5 | 3 | 3 | 45 | URS-001; FS-001-1/2; evaluation watermark (URS-191); positioning memo | P | 5/2/2/20 |
| RSK-35 | Use | Over-reliance on automation | Systematic errors propagate | Automation bias | 4 | 3 | 4 | 48 | SOP-003 review sampling; abstention (URS-055/151); sign-off | P | 4/2/2/16 |
| RSK-36 | Orientation | Left/right or axis flip | Wrong side analysed | Format conventions | 4 | 2 | 4 | 32 | QC orientation check; three-plane view (FS-042-1) | P | 4/1/2/8 |
| RSK-37 | Measurement support | An endpoint that cannot be identified is reported as a number | Plausible but wrong primary outcome | Advisor policy wrong for a material; bypass of suppression | 5 | 3 | 4 | 60 | URS-150/151/153; FS-150-1/2, FS-151-1/2, FS-153-1 | V (in simulation; physical validation pending, STAT-04) | 5/2/3/30 |
| RSK-38 | Measurement support | Conditional or suppressed status missing from the formal report | Reader takes a conditional value as unconditional | Report omits support section (QA-REG-01) | 4 | 3 | 4 | 48 | URS-152; FS-152-1/2 | P/G (implemented, PDF content untested) | 4/2/3/24 |
| RSK-39 | Validation records | Learned model credited with validation it does not have | Graft endpoints reported for an unvalidated material | Record for another model version/material; synthetic evidence; record file edited | 5 | 2 | 4 | 40 | URS-160/161; FS-160-1 exact SHA-256 + material + voxel range; FS-161-1 protected store | V/G | 5/2/3/30 until FS-161-1 exists |
| RSK-40 | Material characterisation | Profile reused for an incompatible protocol | Wrong support decision | Different energy/voxel size/scanner | 4 | 3 | 3 | 36 | URS-170/171; FS-171-1 compatibility rule | V/P | 4/2/2/16 |
| RSK-41 | Longitudinal | Registration failure undetected | Wrong day-0 graft propagation, wrong change over time | Motion, noise, graft migration | 5 | 3 | 4 | 60 | URS-180/181/182; FS-180-1 residual-displacement QC; FS-181-1 computed inputs | V (synthetic only), desktop G | 5/2/2/20 |
| RSK-42 | Licensing | Forged licence accepted, or evaluation report mistaken for a licensed one | Commercial loss; outputs from an unlicensed copy circulate as study results | Signature check defect; missing watermark | 3 | 2 | 3 | 18 | URS-190/191/192; FS-190-1/2, FS-191-1, FS-192-1 | V | 3/1/2/6 |
| RSK-43 | Workflow timing | Timing recorded without user knowledge or leaves the site | Loss of trust; privacy complaint | Default-on; hidden export | 3 | 2 | 3 | 18 | URS-200/201; off by default, audited enable/export, local only | V/P | 3/1/2/6 |
| RSK-44 | Offline | Hidden network dependency or connection | Data leaves the site; function fails offline | Library adds telemetry or network fetch | 4 | 2 | 4 | 32 | URS-210/211; static review; FS-211-1 network-blocked self-test | P/G | 4/1/3/12 |
| RSK-45 | Input safety | Malicious or malformed file executes code or exhausts memory | Workstation compromise; crash with data loss | Pickle codecs, huge headers, archive tricks | 5 | 2 | 3 | 30 | URS-133; FS-026-2, FS-111-2, FS-133-1 | V | 5/1/2/10 |
| RSK-46 | Background jobs | Interrupted or cancelled job leaves partial records | Inconsistent results | Cancellation mid-write; crash | 4 | 3 | 3 | 36 | URS-114; FS-114-1/2 terminal state recorded first, no partial segmentation | V | 4/1/2/8 |
| RSK-47 | Editing | Tool changes voxels the user did not target; undo inexact | Silent label corruption | Brush/eraser logic; anisotropy | 4 | 2 | 4 | 32 | URS-056; FS-056-1/2 protection, exact sparse undo | V | 4/1/2/8 |
| RSK-48 | Direct file access | Study tables (scans, measurements, reviews) edited with a SQLite tool | Altered results without an audit entry | Data tables are not covered by the audit hash chain; OS-level access | 5 | 2 | 5 | 50 | URS-017 OS permissions; audit details record labels/report hashes; FS-021-2 integrity check; SOP-005 | G | 5/2/4/40, **open**: needs per-record hashing of data tables into the chain or a signed manifest |

## 4. Highest-priority actions
1. **RSK-23 / RSK-48 / RSK-20 (attributability and direct file access).** Add desktop user administration (FS-010-3), the idle lock (FS-013-3) and desktop re-authentication through `Store.reauthenticate` (FS-092-2). Cover data tables by hashes in the chain, add anchor export (FS-102-2) and specify OS permissions (FS-017-1).
2. **RSK-09 / RSK-37 / RSK-39 (graft vs new bone).** Physical-phantom and ex-vivo validation (PQ-01, PQ-05); test the PDF support section (FS-152-2); protect validation records (FS-161-1).
3. **RSK-16 / RSK-12.** SAP lock and unblinding with re-authentication in the desktop (FS-070-1, FS-075-2, FS-076-1).
4. **RSK-05.** QC gating with override (FS-032-1).
5. **RSK-30.** Project backup with manifest and restore verification (FS-120-1, FS-121-1).

## 5. Review
Re-assess at each release, for each new data domain (species, scanner, graft type), after any incident (SOP-005, CHANGE_CONTROL.md), and at least yearly. Update the Status column from `scripts/build_traceability.py` output.
