# Execution State

_Last updated: 2026-11-27 (Generation 2 in progress). Branch `claude/osteoquant-autonomous-dev-ujqgkl` (public
repository — founder decision recorded in docs/ip/IP_STRATEGY.md). Ledgers: TASK_REGISTRY.md (tasks),
FORENSIC_AUDIT.md (Gen-0 audit), REVIEW_REGISTRY.md (reviews), DEFECT_REGISTRY.md, BENCHMARK_SCORECARD.md._

## Environment
4 vCPU, 15 GB RAM, no GPU, Python 3.13, PyTorch 2.15 CPU, ONNX Runtime 1.29, PySide6 6.12, VTK 9.7.2 (EGL offscreen).

## Generation status
| Gen | Scope | Status |
|---|---|---|
| 0 | Forensic audit, reproduction (G exact, P exact, C ±0.004, H/I running), remediation register, §55 ledgers | done (H/I reproduction pending) |
| 1–2 | Science: measurement-support advisor (v1.2.0) + pipeline abstention; generator v2 (granule motion); granule tracking; displacement-based registration QC; ROI propagation; DR synthesis; ONNX runtime; experiments S1/S1b/S1c/F2/L3/L4/S2/U1/O2 | in progress (compute queue) |
| 3 | Desktop application (PySide6+VTK), licensing, packaging, CI | in progress (desktop stream) |
| 4 | QA (coverage/property/fuzz/mutation), security Gen-2, CI | in progress (QA stream) |
| 4 | Independent reviews | cycle 1 done for imaging, statistics, ML, architecture (60 findings, all critical/high closed); cycle 1 running for biology/CRO/quality and investor/IP |
| 5 | Website, documentation set, final deliverables | not started |

## Component status (Generation 2 changes)
| Component | Status | Evidence |
|---|---|---|
| Measurement-support advisor | ✅ v1.2.0, 22 unit tests; validation re-runs queued | osteoquant/advisor, tests/test_advisor.py, docs/science/MEASUREMENT_SUPPORT.md |
| Reports honour abstention | ✅ | api/bundle.py, report/defectfill.py |
| Endpoint definitions / pre-registration / histology scope | ✅ docs | docs/science/ |
| Longitudinal v2 (tracking, QC, ROI propagation) | ✅ tested; L3/L4 running | tests/test_longitudinal_v2.py |
| ONNX Runtime inference (no PyTorch needed at analysis time) | ✅ verified identical labels | osteoquant/ml/runtime.py, pipeline `onnx:` |
| Model registry safety (locked atomic writes, provenance inheritance, code version) | ✅ | osteoquant/ml/train.py |
| Claims checker | ✅ 8 claims pass | scripts/check_claims.py |
| Competitor matrix, patents, invention register, IP strategy | ✅ | docs/research, docs/ip |
| Revenue model, pricing validation, funding strategy | ✅ | business/, investor/ |
| Validation programme A–F | ✅ plan | validation/VALIDATION_PROGRAM.md |

## Generation-1 component table (history)

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
