# OsteoQuant — Founder Operating Manual

Written for a founder who is still learning software engineering. Read top to bottom once; afterwards use it as a
reference. Everything here was run and checked in the build session unless marked otherwise.

## 1. What exists
| Layer | Where | One-line purpose |
|---|---|---|
| Analysis library | `osteoquant/` | read scans, check quality, find the defect, segment, measure, compute statistics |
| Web app | `osteoquant/api/` + `web/static/` | multi-user study management, viewer with correction tools, reports |
| Experiments | `experiments/` | every result quoted anywhere comes from a script here → `experiments/results/*.json` |
| Tests | `tests/` | 42 automated tests (`pytest -q`) — run before every change you keep |
| Documents | root `*.md`, `docs/`, `business/`, `grants/`, `outreach/`, `validation/`, `publications/`, `investor/` | science, quality, commercial, funding |

Package map (each folder has a docstring at the top of its main file explaining the science):
`io/` ingestion · `qc/` quality checks · `phantom/` synthetic data + CT physics · `segment/` classical methods + metrics ·
`ml/` U-Net · `roi/` defect ROI · `morphometry/` measurements · `uncertainty/` confidence and abstention ·
`longitudinal/` registration + day-0 method · `histology/` 2D stain analysis · `stats/` biostatistics ·
`report/` PDF/CSV · `audit/` hash-chained log · `study/` database, users, jobs.

## 2. Install on your Mac (Apple Silicon)
```bash
git clone <repo> osteoquant && cd osteoquant
python3 -m venv .venv && source .venv/bin/activate          # Python 3.11–3.13
pip install --upgrade pip
pip install -e ".[dev]"                                      # installs everything in pyproject.toml
pytest -q                                                    # expect: all tests pass
```
PyTorch on Apple Silicon: the default `pip install torch` wheel supports the `mps` GPU backend. The code currently runs on
CPU; switching training to `mps` is a one-line device change in `osteoquant/ml/train.py` (planned, not yet tested).

## 3. Run the demo (5 minutes)
```bash
python scripts/demo_seed.py                 # creates runtime/demo.db with a synthetic study (+ public ovine study if data downloaded)
OQ_DB=runtime/demo.db osteoquant serve      # → open http://127.0.0.1:8765
```
Users: `demo_admin`, `demo_analyst`, `demo_reviewer`; password `Demo-Password-2026` (change for anything real).
Follow `founder/DEMO_SCRIPT.md` for the scripted walkthrough.

## 4. Real use (one lab, one computer)
```bash
osteoquant init-admin --org "Your Lab" --user yourname      # prompts for a password (≥10 chars, upper-case, digit)
osteoquant serve                                             # local only (127.0.0.1); nothing leaves the machine
```
In the browser: create a project → study (tick *Blinded* if group identities must be hidden from analysts) → groups,
timepoints, specimens → upload scans (NIfTI, NRRD, TIFF stack as ZIP, DICOM as ZIP, OME-TIFF, Zeiss TXM) and enter the
voxel size if the file lacks it → *Analyze* → open the viewer, correct, sign as reviewer → *Generate DefectFill report*.

Command line equivalents for quick checks: `osteoquant ingest scan.nii.gz`, `osteoquant qc scan.nii.gz`,
`osteoquant analyze scan.nii.gz --model condyle --diameter 2000`.

## 5. Daily operations
* **Backup**: `osteoquant backup backups/osteoquant-$(date +%F).db` (consistent copy + SHA-256). Scan data lives in
  `runtime/data/`; back it up with the database (e.g. Time Machine or an encrypted external drive).
* **Audit check**: `osteoquant audit-verify` → `{"ok": true}`. Export the latest `seq`/`row_hash` to a separate place
  weekly (anchor) so deletion of recent events would be detectable.
* **Users**: one account per person; never share accounts; deactivate leavers (API `POST /api/users`, admin only).
* **Models**: only use models listed in `models/registry.json`; reports record the model SHA-256. Synthetic-trained
  models produce reports watermarked "SYNTHETIC-TRAINED". Do not use them for customer study decisions.

## 6. Making changes safely
1. Create a branch. 2. Change code. 3. `pytest -q`. 4. If you changed analysis code, re-run the relevant experiment and
compare JSON outputs. 5. Commit with a message saying *why*. 6. Record user-visible or scientific changes in
`DECISIONS.md` and follow `docs/quality/CHANGE_CONTROL.md`.

## 7. Reproducing every result
`cd experiments` then: `python make_synthetic_dataset.py` (once) → `python exp_A_baselines.py`, `exp_B_unet.py`,
`exp_C_separability.py`, `exp_C2_ablation.py`, `exp_F_roi.py`, `exp_G_morphometry.py`, `exp_H_I_real.py`,
`exp_J_adaptation.py`, `exp_K_M_uncertainty.py`, `exp_L_longitudinal.py`, `exp_L2_strutlike.py`,
`exp_N_histology.py`, `exp_O_performance.py`, `exp_P_reproducibility.py`; sample reports: `python make_sample_reports.py`.
Real datasets: download commands in `DATASET_REGISTRY.md`.

## 8. When something breaks
| Symptom | Likely cause | Fix |
|---|---|---|
| Upload says spacing assumed | file has no voxel size | enter voxel µm in the upload form |
| ROI "needs manual ROI" | no clear gap/plate, hardware, unusual anatomy | define ROI by landmarks (PUT /api/scans/{id}/roi) |
| New-bone fraction ≈1.0 | threshold picked up padding/air | check QC histogram; robust thresholds handle zero padding, report others |
| QC warns "metal/hardware" | implant, fixator or holder present | mask it; expect streak artefacts |
| Audit verify fails | database edited outside the app | restore from backup; investigate |

## 9. Deployment beyond one laptop (not done; plan)
Single small server (or Mac mini) on the lab network behind HTTPS (Caddy/nginx), `osteoquant serve --host 0.0.0.0`
only behind the proxy, daily encrypted off-site backup, OS updates, disk encryption. Move to PostgreSQL only when
multiple concurrent analysts need it. Do **not** put customer data in a public cloud without a signed DPA.
