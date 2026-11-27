# OQ-P1 Worksheets

These are printable logs and data-entry templates for Protocol OQ-P1 (`../PHANTOM_EXPERIMENT_PROTOCOL.md`). Paper is the primary record. CSVs are transcribed within 24 h and double-checked by a second person where possible.

| File | Use |
|---|---|
| `SPECIMEN_PREP_LOG.md` | Printable. Session header, per-core record (defects, pre-fill, filling, capping), and graft lot record. |
| `SCAN_ACQUISITION_LOG.md` | Printable. Per-session header and per-scan settings (all fields from protocol §7), plus billing record. |
| `CHAIN_OF_CUSTODY.md` | Printable. One per donor bone, graft lot or data drive. Includes the fill-map hash section for the custodian. |
| `specimen_labels.csv` | For label printers (mail-merge). Blinded IDs only. `copies` = labels per item (tube, cap, prep sheet). Test label durability in 70% ethanol first. |
| `specimen_registry.csv` | One row per specimen: core, layered core, foam, reference or phantom. |
| `gravimetric_log.csv` | One row per defect (pre-populated C01–C14 and L01–L02 × D1–D4). Tier A uses C01–C08 and L01 only. |
| `fill_map_CUSTODIAN_TEMPLATE.csv` | **Custodian only.** Generate with a seeded randomizer, balanced by geometry and blocked by donor. Hash it and keep it sealed until unblinding. Do not store it alongside the analysis data. |
| `material_reference_log.csv` | Pure-material reference tubes R01–R06. Material identity is held by the custodian. |
| `scan_log.csv` | Digital copy of the scan acquisition log. |
| `calibration_log.csv` | HA phantom fits and drift per session and setting. |
| `qc_checks.csv` | Q1–Q14 per scan (protocol §10). |
| `analysis_results.csv` | One row per defect × voxel size × scan type. `material_true` stays blank until unblinding. |
| `chain_of_custody.csv` | Digital copy of custody transfers. |

Material codes, which the custodian maps to letters on the fill sheet: HA, TCP (β-TCP), BCP, BG (45S5 bioactive glass), CS (calcium sulfate), BC (bone chips), EMPTY, and optionally pdBC.
