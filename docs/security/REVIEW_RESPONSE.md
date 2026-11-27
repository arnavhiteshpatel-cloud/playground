# Response to the Independent Security & Scientific Review (2026-11-27)

Reviews: `SECURITY_REVIEW.md` (21 findings) and `SCIENTIFIC_REVIEW.md` (18 findings), written by an independent agent
that did not modify code. Regression tests: `tests/test_security_fixes.py`, `tests/test_controls.py`.

## Security
| ID | Sev | Disposition | Where / test |
|---|---|---|---|
| S-01 detached-header file read | critical | **Fixed**: uploads use `read_volume(safe=True)`; `.mhd/.nhdr/.raw/.mha` and NRRD `data file` rejected | readers.check_safe_input; test_S01 |
| S-02 unsafe model deserialisation | critical | **Fixed**: models loaded by registered *name* only; SHA-256 checked against registry *before* loading; `torch.load(weights_only=True)`; checkpoints re-saved with JSON-plain metadata; `rf:` pickles only via trusted CLI flag; API config is a strict schema (extra keys forbidden) | ml/train.load_model; pipeline; app.AnalyzeConfig; test_S02 |
| S-03 TAR / decompression | high | **Fixed**: uploads accept ZIP only; streamed extraction with per-member and total byte limits (16 GB) | safe_archive; test_S03 |
| S-04 PDF markup injection | high | **Fixed**: user text XML-escaped before ReportLab Paragraphs | report/defectfill; test_S04 |
| S-05 cross-tenant group IDOR | high | **Fixed**: specimen group must belong to the study; violation audited | study/db.add_specimen; test_S05 |
| S-06 blinding bypass via report | high | **Fixed**: reports generated with unblinded allocation are flagged; download requires `unblind` permission | migration 2; app.get_report |
| S-07 export leaks org audit | medium | **Fixed**: audit trail included in export only for reviewer/admin | study/db.export_study |
| S-08 review binding | medium | **Fixed**: object must exist in the org; reviewed object's SHA-256 stored; self-approval blocked; reports use the *latest* decision and require hash match | study/db.review; api/bundle; test_S08, test_author_cannot_approve |
| S-09 lockout DoS / timing | medium | **Mitigated**: 15-minute temporary lock; equal-cost hash for unknown users. Residual: no CAPTCHA/IP throttling | study/db.login; test_S09 |
| S-10 audit chain concurrency | medium | **Fixed**: store-wide lock + `BEGIN IMMEDIATE` around read-last/insert | audit/log; test_S10 |
| S-11 undetectable tail truncation | medium | **Mitigated**: `verify_chain(anchor)`; operating manual requires weekly external anchor export. Residual: unkeyed chain (consider HMAC with offline key) | test_S11 |
| S-12 unaudited reads | low | **Open** (slice/scan reads not audited; downloads are) | REMAINING_WORK #11 |
| S-13 incomplete deletion | medium | **Partially fixed**: reports, report files, report reviews, configs deleted; figures directory and job records remain | study/db.delete_study_data |
| S-14 backups omit image data | low | **Open/documented**: manual says back up `runtime/data/` with the DB | founder/OPERATING_MANUAL §5 |
| S-15 unbounded compute | low–med | **Partially**: mesh step bounded 1–8, edits ≤5000 ops; no per-user rate limit | open |
| S-16 error detail leakage | low | **Open** (job error messages shown to same-org users) | open |
| S-17 stale privileges in jobs | low | **Open** (jobs run with submit-time user record) | open |
| S-18 hard-coded demo password | low | **Fixed**: random unless `OQ_DEMO_PASSWORD` set | scripts/demo_seed.py |
| S-19 CSV formula injection | low | **Fixed**: cells beginning with = + - @ are prefixed | report/defectfill._csv_safe |
| S-20 session details | low/info | **Open** (no idle timeout/rotation; 8 h tokens) | open |
| S-21 filename edge case | info | **Open** | open |

## Science
| ID | Sev | Disposition |
|---|---|---|
| Q-01 "Bayes bound" not a Dice bound | high | **Fixed and claims corrected**: Dice-optimal intensity-only oracle recomputed for C, C2, L2 (`recompute_intensity_oracle.py`, `exp_Q01_intensity_oracle.json`); figure redrawn. Overlap-regime oracle graft Dice 0.52–0.77 (was mis-stated 0.30–0.65); conclusions about RF/day-0 exceeding intensity information unchanged |
| Q-02 true-ROI geometry in features | high | **Disclosed + mitigated**: primary RF numbers now reported with `no_spatial` features; the no-context U-Net (no ROI input) is the headline model; sample report 1 uses *detected* ROIs. Residual: evaluation masks and generator geometry still couple spatial position and class |
| Q-03 unfair RF training | high | **Fixed for A** (balanced 12-specimen RF + no-spatial RF rerun), **fixed for H** (RF on all 10 training specimens). J compares pretrained-U-Net fine-tuning vs RF from scratch *by design* (states the pretraining advantage) |
| Q-04 mean_dice_roi | medium | **Disclosed**: not used in any claim; new/graft Dice reported separately |
| Q-05 pseudoreplication in reports | medium | **Fixed**: group statistics average repeated scans per animal/timepoint |
| Q-06 abstention bias | medium | **Fixed**: fractions of the confidently classified volume added |
| Q-07 coverage counts graft | medium | **Fixed**: report endpoint now new-bone projected coverage |
| Q-08 QC loses ingest provenance | medium | **Fixed**: stored ingest record reused in web QC |
| Q-09 corrected-version re-measurement | medium | **Fixed**: per-version ROI masks; same thickness setting as base |
| Q-10 edge convention post hoc | medium | **Disclosed** in code and manuscript; needs independent reference data |
| Q-11 day-0 near-optimal by construction | medium | **Disclosed**: day-0 and later phantoms share exact packing; graft only shrinks. Real granule migration/fragmentation not simulated → L/L2 are best-case; added to limitations and REMAINING_WORK |
| Q-12 K/M not applied / in-sample | medium | **Fixed**: temperature applied; failure threshold from validation split; rerun |
| Q-13 mirrored mesh | medium | **Fixed**: vertices exported x,y,z with winding preserved |
| Q-14 DICOM z-spacing fallback | low–med | **Fixed**: InstanceNumber fallback no longer used as distance; spacing from SpacingBetweenSlices/SliceThickness, flagged as assumed |
| Q-15–Q-18 | low/info | **Open**, tracked in REMAINING_WORK #11; Q-17 addressed by watermarking and evidence labels throughout |
