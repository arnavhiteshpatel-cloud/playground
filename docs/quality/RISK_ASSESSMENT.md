# OsteoQuant — Risk Assessment (FMEA-style)

| Field | Value |
|---|---|
| Document ID | OQ-QMS-RA-001 |
| Version | 0.1 (DRAFT) |
| Date | 2026-11-27 |
| Scope | Scientific-validity and data-integrity risks of the OsteoQuant research prototype |
| Method | FMEA; risk-based approach per OECD GLP No. 17 ¶12–14 and GAMP 5 (benchmark) |

> **Status: DRAFT — not validated; not a claim of Part 11 compliance or GLP validation.**

## 1. Scoring
- **S – Severity** (impact on scientific conclusions / record integrity): 1 negligible · 2 minor, detectable cosmetic · 3 wrong secondary result · 4 wrong primary outcome or loss of attributability · 5 undetected wrong study conclusion, data loss, or falsification undetectable.
- **O – Occurrence** (without new controls): 1 remote … 5 frequent.
- **D – Detectability** (before results are used): 1 almost certainly detected … 5 not detectable.
- **RPN = S × O × D.** Action required if RPN ≥ 40 or S = 5. Residual scores assume controls are implemented **and verified**; currently they are **planned**, not verified.
- Patient safety is not applicable (non-clinical); "harm" here = wrong scientific conclusions, compromised animal-study value (3Rs), loss of record integrity.

## 2. FMEA table

| Risk ID | Process step | Failure mode | Effect | Cause | S | O | D | RPN | Controls (URS / FS) | Verification | Res. S/O/D/RPN |
|---|---|---|---|---|---|---|---|---|---|---|---|
| RSK-01 | Ingestion | Wrong voxel spacing used (e.g., header default 1.0, mm vs µm) | All volumes wrong by factor up to 10⁹; thickness wrong | Missing/ambiguous header, unit confusion, rescaled export | 5 | 3 | 4 | 60 | URS-022/023; FS-022-1, FS-023-1/2; QC-SPC; spacing in report | OQ-ING-03/04; phantom tests at multiple spacings | 5/1/2/10 |
| RSK-02 | Ingestion | Anisotropic voxels treated as isotropic | Biased thickness/separation metrics | Simplified algorithm | 4 | 2 | 4 | 32 | FS-023-1 anisotropy flag; metric algorithms use per-axis spacing | Phantom anisotropic tests | 4/1/2/8 |
| RSK-03 | Ingestion | Specimen / time point / side mix-up | Data assigned to wrong animal or group | Manual entry error, duplicate file names | 5 | 3 | 4 | 60 | URS-025; FS-025-1 unique constraints, duplicate-hash detection; SOP-001 second-person check | OQ-ING-05 | 5/2/2/20 |
| RSK-04 | Ingestion/storage | Original file altered or corrupted | Results not traceable to raw data | Storage fault, manual edit on disk | 5 | 2 | 3 | 30 | URS-020/021/024; FS-020-1/2, FS-021-1 | OQ-ING-01/02 (tamper a byte) | 5/1/1/5 |
| RSK-05 | QC | QC failure ignored / silently overridden | Artefact-laden scans analysed | Time pressure, no gating | 4 | 3 | 3 | 36 | URS-032; FS-032-1 override with reason, printed in report | OQ-QC-02 | 4/2/1/8 |
| RSK-06 | ROI | Wrong ROI placement or size | Defect fill metrics invalid; host bone counted as new bone | Landmark error, inconsistent operator practice | 5 | 3 | 3 | 45 | URS-040/041/042; FS-040-1, FS-042-1 explicit ROI verification; SOP-002; PQ inter-operator study | OQ-ROI-01..03; PQ-03 | 5/2/2/20 |
| RSK-07 | ROI | ROI inconsistent across longitudinal time points | Spurious change over time | Re-positioning, registration error | 4 | 3 | 3 | 36 | FS-040-1 physical-unit ROI parameters; longitudinal registration QC (future module) | PQ-04 | 4/2/2/16 |
| RSK-08 | Segmentation | Silent label-mapping error (e.g., graft↔new bone swapped) | Primary outcome inverted; undetectable in numbers alone | Model retrained with different class order; mask import; legend hard-coded | 5 | 3 | 5 | 75 | URS-050/054; FS-050-1, FS-054-1/2 manifest equality check; legend generated from label map; golden-case regression | OQ-SEG-01/02; VER golden dataset | 5/1/2/10 |
| RSK-09 | Segmentation | Residual graft misclassified as new bone (similar attenuation) | Over-estimation of bone formation (efficacy bias) | Intrinsic ambiguity, graft material differs from training set | 5 | 4 | 4 | 80 | URS-052/053/055; human review SOP-003; per-material PQ acceptance; uncertainty flag; graft-material listed in model manifest intended-use | PQ-01/02; OQ-SEG-04 | 5/3/2/30 — **remains highest residual scientific risk** |
| RSK-10 | Segmentation | Model drift / wrong model version used | Results not comparable across study; unrepeatable | Unversioned model swap, silent retraining, dependency change | 5 | 3 | 4 | 60 | URS-051/111/112; FS-051-1, FS-111-1 hash check, FS-112-1 release status; SOP-007 | OQ-MOD-01/02 | 5/1/1/5 |
| RSK-11 | Segmentation | Distribution shift (new scanner, species, voxel size, graft type) degrades accuracy | Systematic bias without warning | Model used outside validated domain | 5 | 3 | 4 | 60 | Model manifest "validated domain"; QC flags out-of-domain acquisition parameters; uncertainty flag; PQ per new domain | OQ-SEG-05; PQ-05 | 5/2/2/20 |
| RSK-12 | Correction | Human corrections biased by knowledge of group | Bias toward hypothesis | Unblinded analysts | 5 | 3 | 5 | 75 | URS-075/076; FS-075-1/2, FS-076-1; SOP-009 | OQ-BLD-01..03 | 5/1/2/10 |
| RSK-13 | Correction | Correction overwrites original prediction | Loss of original; cannot assess correction magnitude | Design shortcut | 4 | 2 | 4 | 32 | URS-052/053; FS-052-1, FS-053-1 | OQ-SEG-03 | 4/1/1/4 |
| RSK-14 | Morphometry | Algorithm error (off-by-one, boundary handling, partial volume) | Biased metrics | Implementation defect | 5 | 3 | 3 | 45 | URS-062; FS-062-1 phantom suite; independent reference comparison in PQ | VER-MORPH suite; PQ-06 | 5/1/2/10 |
| RSK-15 | Morphometry | Density reported without valid calibration | Meaningless BMD/TMD values | Missing phantom | 4 | 3 | 3 | 36 | URS-063; FS-063-1 | OQ-MOR-03 | 4/1/1/4 |
| RSK-16 | Statistics | Wrong grouping / exclusion after seeing results | False-positive findings | Post-hoc analysis, p-hacking | 5 | 3 | 4 | 60 | URS-070/072; FS-070-1, FS-072-1 locked SAP, listed exclusions | OQ-STA-01..03 | 5/2/2/20 |
| RSK-17 | Statistics | Non-reproducible statistics (seed, library change) | Results differ on re-run | Unpinned libraries | 3 | 3 | 3 | 27 | URS-071; FS-071-1, FS-131-1 | OQ-STA-04 | 3/1/2/6 |
| RSK-18 | Reporting | Report values do not match database / stale report | Published numbers wrong | Caching; report generated before correction | 5 | 2 | 4 | 40 | URS-080/082/093; FS-080-1, FS-082-1, FS-093-1 hash-linked signatures | OQ-REP-01..03 | 5/1/1/5 |
| RSK-19 | Reporting | CSV locale/precision corruption | Values mis-parsed downstream (e.g., 1,234 vs 1.234) | Locale-dependent writer, Excel re-save | 4 | 3 | 3 | 36 | URS-083; FS-083-1 | OQ-REP-04 | 4/1/2/8 |
| RSK-20 | Audit trail | Audit trail tampered via direct DB edit | Falsification undetected | Admin/OS access to SQLite file | 5 | 2 | 5 | 50 | URS-102/103; FS-100-1 triggers, FS-102-1 hash chain, FS-102-2 external anchoring; SOP-005 periodic verification; OS access restriction | OQ-AUD-03/04 | 5/1/2/10 |
| RSK-21 | Audit trail | Entire chain regenerated by privileged attacker | Tamper evidence defeated | Hash chain without external anchor | 5 | 1 | 5 | 25 | FS-102-2 anchoring to backups / independent store; restricted OS admin (segregated from study roles) | OQ-AUD-05 | 5/1/3/15 |
| RSK-22 | Audit trail | Incorrect timestamps (clock drift, TZ errors) | Contemporaneity questioned; sequence ambiguity | No NTP, local time stored | 3 | 3 | 3 | 27 | URS-106; FS-106-1; IQ-06 | OQ-AUD-06 | 3/1/2/6 |
| RSK-23 | Access | Shared accounts / credential sharing | Loss of attributability | Convenience | 4 | 3 | 4 | 48 | URS-010/013; FS-010-2; SOP-008 training & attestation | OQ-ACC-01; access review | 4/2/3/24 (procedural residual) |
| RSK-24 | Access | Privilege escalation / missing permission check | Unauthorized edits | Endpoint lacking guard | 5 | 2 | 3 | 30 | URS-011; FS-011-2 route-permission test | OQ-ACC-02/03 | 5/1/1/5 |
| RSK-25 | Access | Cross-tenant data leakage | Confidentiality breach; contaminated datasets | Unscoped query | 5 | 2 | 4 | 40 | URS-012; FS-012-1/2 | OQ-ACC-04 (automated cross-tenant suite) | 5/1/2/10 |
| RSK-26 | Signatures | Signature applied to changed record / repudiation | Approval does not reflect content | No hash link; no re-auth | 4 | 2 | 4 | 32 | URS-091/092/093; FS-091-1, FS-092-1, FS-093-1 | OQ-SIG-01..03 | 4/1/1/4 |
| RSK-27 | Config | Parameter change not captured | Irreproducible results | Defaults changed between versions | 4 | 3 | 4 | 48 | URS-110; FS-110-1 resolved-config snapshot | OQ-CFG-01 | 4/1/2/8 |
| RSK-28 | Computation | Non-determinism (GPU, threading) | Re-run differs; reviewers lose trust | Non-deterministic kernels | 3 | 4 | 3 | 36 | URS-113; FS-113-1 deterministic mode, tolerance | OQ-CFG-02 | 3/2/2/12 |
| RSK-29 | Dependencies | Library update changes numerics (e.g., SciPy, scikit-image) | Silent shift in metrics | Unpinned/updated deps | 4 | 3 | 4 | 48 | URS-131; FS-131-1; CHANGE_CONTROL regression on golden datasets | VER golden regression | 4/1/2/8 |
| RSK-30 | Data mgmt | Backup missing/incomplete/unrestorable | Data loss | Untested backups | 5 | 2 | 4 | 40 | URS-120/121; FS-120-1, FS-121-1; SOP-006 quarterly restore test | OQ-BKP-01/02 | 5/1/2/10 |
| RSK-31 | Data mgmt | Premature deletion of records | Loss of raw data within retention period | Misconfiguration, malicious | 5 | 2 | 3 | 30 | URS-122/123; FS-122-1, FS-123-1 dual approval, legal hold | OQ-RET-01..03 | 5/1/1/5 |
| RSK-32 | Data mgmt | Concurrent writes corrupt SQLite | Lost/inconsistent records | Multi-worker writes without WAL/locking | 4 | 2 | 3 | 24 | WAL mode, single-writer queue, integrity check on startup (IQ/OQ) | OQ-DB-01 | 4/1/2/8 |
| RSK-33 | Archive | Data unreadable later (format/software obsolescence) | Study cannot be reconstructed | Proprietary formats | 4 | 2 | 4 | 32 | URS-124; FS-124-1 open formats; retain software versions (OECD 17 ¶75, ¶117) | OQ-ARC-01 | 4/1/2/8 |
| RSK-34 | Use | Prototype outputs used as if validated (e.g., in GLP study or submission) | Regulatory non-compliance; data rejected | Misunderstanding of status | 5 | 3 | 3 | 45 | URS-001; FS-001-1/2 RUO + "not validated" banner; positioning memo; customer agreements | OQ-GEN-01 | 5/2/2/20 |
| RSK-35 | Use | Over-reliance on automation; insufficient human review | Systematic errors propagate | Automation bias | 4 | 3 | 4 | 48 | SOP-003 mandatory review sampling; uncertainty flags; review sign-off | PQ-02 | 4/2/2/16 |
| RSK-36 | Orientation | Left/right or axis flip | Wrong defect side analysed; host vs defect swapped | Format orientation conventions | 4 | 2 | 4 | 32 | QC-ORI; ROI visual verification FS-042-1 | OQ-QC-03 | 4/1/2/8 |

## 3. Highest-priority actions
1. **RSK-09 (graft vs new bone confusion)** — define per-graft-material PQ acceptance criteria and require human review sampling; consider ancillary evidence (histology correlation module) before claims of new-bone quantification.
2. **RSK-08 / RSK-01** — implement label-map and voxel-spacing hard checks first; these are low-cost and high-severity.
3. **RSK-12 / RSK-16** — blinding and SAP lock before any customer pilot.
4. **RSK-20 / RSK-21** — hash chain plus external anchoring; restrict OS-level DB access.
5. **RSK-34** — RUO/not-validated labelling and customer-facing positioning.

## 4. Review
Re-assess at each major release, at each new data domain (species, scanner, graft type), after any incident (SOP-005/CHANGE_CONTROL), and at least annually.
