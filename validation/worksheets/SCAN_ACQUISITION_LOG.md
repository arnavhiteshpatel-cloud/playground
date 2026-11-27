# Scan Acquisition Log: Protocol OQ-P1 (ZEISS Xradia Versa 630)

Use one row block per scan. Copy values exactly as the acquisition and reconstruction software displays them, and do not round. Transcribe to `scan_log.csv` the same day.

## Session header

| Field | Entry |
|---|---|
| Session # / date / booked hours | / / |
| Operator / trained-user status / facility staff present? | / / |
| Instrument software (acquisition) name + version | |
| Reconstruction software name + version | |
| Warm-up completed (time) | |
| HA phantom QC scan ID for this session | |
| Phantom mean GV / SD (rod 1, rod 2) | / ; / |
| Drift vs session 1 (%) / pass? | / ☐ |

## Per-scan record

| Field | Entry |
|---|---|
| Scan ID (`OQ-P1_<Spec>_<TYPE>_<VOX>um_R<rep>_<date>`) | |
| Specimen ID / scan type (PRE / POST / POSTQ (quick 40 µm) / REP / REF / PHANTOM) | / |
| Start / end time | / |
| Voltage (kV) / power (W) / current (µA) | / / |
| Filter (ID as displayed) | |
| Objective / binning / camera pixel | / / |
| Source–sample dist (mm) / detector–sample dist (mm) | / |
| Voxel size (µm) / FOV (mm) / vertical stitches | / / |
| Exposure (s) / # projections / angular range | / / |
| Reference images (count, interval) | |
| Ring-removal / drift-correction options | |
| Recon algorithm | |
| **DL / AI reconstruction used? (must be NO unless D3)** | ☐ No ☐ Yes (which) |
| Beam-hardening constant / center shift / smoothing | / / |
| Output format / bit depth | / |
| Sample conditioning (humid / immersed / dry), time since fill (h) | / |
| Specimen mass before / after scan (g) | / |
| QC: motion ☐ OK; rings ☐ OK; ROI in FOV ☐ OK; streaks ☐ OK | |
| Files + SHA-256 (projections / recon / TIFF export) | |
| Storage: CTData path / founder drive 1 / drive 2 (verified ☐) | / / |
| Notes | |
| Operator initials | |

## Facility billing record

| Date | Start | End | Hours billed | Rate category | Notes |
|---|---|---|---|---|---|
| | | | | | |
