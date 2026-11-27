# Execution State

_Last updated: 2026-11-27 (session 1). Repository: `arnavhiteshpatel-cloud/playground`, branch `claude/osteoquant-autonomous-dev-ujqgkl`._

## Environment (inspected)
Cloud Linux container: 4 vCPU Xeon @2.3 GHz, 15 GB RAM, **no GPU**, ~55 GB free disk, Python 3.13,
PyTorch 2.15 CPU, Node 22. (Founder's Apple-Silicon Mac was not available to this session.)

## Status by component
| Component | Status | Evidence |
|---|---|---|
| Ingestion (TIFF stack, OME-TIFF, DICOM, NIfTI, NRRD, MHA, Zarr, Zeiss TXM) | ✅ working, tested | tests/test_core.py; real TXM (2.1 GB) + DICOM (829 slices) read |
| Chunked/out-of-core store (Zarr), hashing, duplicate detection, missing-slice detection | ✅ | tests; Exp O |
| QC engine (deterministic + heuristic checks) | ✅ | Exp E, real ovine scan |
| Phantom generator (3 defect models, 15 materials, NIST physics) + fast & CT-physics imaging | ✅ | figures/phantom_models_overview.png |
| Classical baselines (9 methods incl. RF) | ✅ | Exp A, C |
| Morphometry (BV/TV, BS, Tb.Th/Sp/N, Conn.D, Ct.Th, bridging, ingrowth, BIC, density) | ✅ verified | Exp G (analytic + Scanco IPL reference, ICC 0.98 Tb.Th) |
| ROI engine (cylinder/sphere/box/mask, landmarks, auto plate & segmental detection, revisions) | ✅ | Exp F; tests |
| 3D U-Net (CPU), training/inference, model registry, licence guard | ✅ | Exp B, J, H/I |
| Uncertainty (entropy, TTA, temperature scaling, abstention, risk–coverage, OOD) | ✅ | Exp K |
| Longitudinal (rigid/affine/B-spline registration, day-0 propagation, change maps) | ✅ | Exp L, L2 |
| Histology module (stain deconvolution, Macenko, quantification, nuclei, 2D–3D reg) | ⚠️ experimental (Exp N: registration good; bone quantification weak; nuclei below DL tools) | Exp N |
| Study store (SQLite), RBAC, tenants, blinding, jobs, reviews, export/delete | ✅ tested | tests/test_api.py |
| Audit log (append-only, hash-chained, tamper detection, anchors) | ✅ tested | tests/test_api.py |
| Web API (FastAPI) + browser viewer (orthogonal views, correction, measure, 3D) | ✅ run in browser | investor/screenshots |
| DefectFill PDF/CSV report generator | ✅ | e2e test; sample reports pending |
| Quality docs (URS/FS/risk/IQ/OQ/PQ/SOPs) | ✅ drafts | docs/quality |
| Research docs (science, competitors, datasets) | ✅ | docs/science, docs/research |
| Commercial / grants / outreach / validation packages | ✅ drafts | business/, grants/, outreach/, validation/ |

## Experiments (see EXPERIMENT_REGISTRY.md)
All 16 (A–P) run; C/C2/L2 oracle corrected; A, K, H re-run after independent review. 60 tests pass.

## Independent review
21 security + 18 science findings; disposition in docs/security/REVIEW_RESPONSE.md (all critical/high fixed).

## How to resume
1. `pip install -e .[dev]` (or the dependency list in pyproject.toml); `pytest -q`.
2. Synthetic data: `python experiments/make_synthetic_dataset.py` (idempotent).
3. Real data: see DATASET_REGISTRY.md download commands (Zenodo IDs 17255311, 11061947, 24047383, 3909552).
4. Each experiment: `cd experiments && python exp_<X>.py` → `experiments/results/*.json` and figures.
5. Demo: `python scripts/demo_seed.py && OQ_DB=runtime/demo.db osteoquant serve`.
