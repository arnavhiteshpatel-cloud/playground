# Execution State

_Last updated: 2026-11-28 (Generation 2, final phase). Branch `claude/osteoquant-autonomous-dev-ujqgkl` (public
repository — founder decision recorded in docs/ip/IP_STRATEGY.md). Ledgers: TASK_REGISTRY.md (tasks),
FORENSIC_AUDIT.md (Gen-0 audit), REVIEW_REGISTRY.md (reviews), DEFECT_REGISTRY.md, BENCHMARK_SCORECARD.md,
EXPERIMENT_REGISTRY.md, EVIDENCE_LEDGER.md._

## Environment
4 vCPU, 15 GB RAM, no GPU, Python 3.13, PyTorch 2.15 CPU, ONNX Runtime 1.29, PySide6 6.12, VTK 9.7.2 (EGL offscreen).

## Generation status
| Gen | Scope | Status |
|---|---|---|
| 0 | Forensic audit, reproduction (G exact, H/I 29 rows identical, C ±0.004), remediation register, §55 ledgers | done |
| 1–2 | Science: measurement-support advisor 1.4.2 bound to its validated method; three pre-registered held-out validations (S1H, S1H2, S1H3); generator v2; granule tracking v2; aperture-aware registration QC; ROI propagation; DR synthesis; ONNX runtime | advisor and longitudinal done; ML campaign (S2b/S2c, S3, U1, O2) running on CPU |
| 3 | Desktop application (PySide6+VTK), offline licensing (test keys only), PyInstaller packaging, CI for 3 OS | done (Linux bundle built locally; Windows/macOS builds only in CI, never run here) |
| 4 | QA, security Gen-2, CI | done; coverage to be re-measured on the final code |
| 4 | Reviews (automated reviewer agents, 12 perspectives) | cycle 1 done (all perspectives); cycle 2 done (68 findings, responses written); cycle 3 running |
| 5 | Website, documentation set, final deliverables | website and user docs on advisor 1.4.2 (claims checker passes); final report, workbook, decks and handoff being rebuilt |

## Component status (Generation 2)
| Component | Status | Evidence |
|---|---|---|
| Measurement-support advisor | ✅ 1.4.2; 37 unit tests; held-out S1H3: safe on every endpoint, low coverage | osteoquant/advisor, tests/test_advisor.py, EXPERIMENT_REGISTRY S1H3 |
| Method binding of support | ✅ only `advisor_threshold` (default) carries support | osteoquant/pipeline.py, test_pipeline_binds_support_to_method |
| Reports honour abstention; group statistics exclude refused values | ✅ | report/defectfill.py, tests/test_report_bounds.py |
| Longitudinal v2 (tracking, aperture-aware QC, ROI propagation) | ✅ L3, L4, F2 re-run | tests/test_longitudinal_v2.py |
| ONNX Runtime inference (no PyTorch at analysis time) | ✅ identical labels (spot check); O2 benchmark queued | osteoquant/ml/runtime.py |
| Signed validation records for learned models | ✅ format and verification; no qualifying record exists | osteoquant/ml/validation_records.py |
| Claims checker | ✅ L3, S1H3, real-data and financial claims; banned phrases; advisor-version consistency | scripts/check_claims.py |
| Full test suite | 562 passed, 1 skipped (local run 2026-11-28, before the QC rounding fix; its test file passes) | CI workflow `.github/workflows/ci.yml` |

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
Generation 1: all 16 (A–P) run; C/C2/L2 oracle corrected; A, K, H re-run after review. Generation 2: S1/S1b/S1c (in-sample), S1H/S1H2/S1H3 (held out), L3, L4, F2, S2 (part a done), S3, U1, O2 — status per row in EXPERIMENT_REGISTRY.md.

## Reviews
Generation 1: 21 security + 18 science findings (docs/security/REVIEW_RESPONSE.md). Generation 2: REVIEW_REGISTRY.md (automated reviewer agents; not human expert review).

## How to resume
1. `pip install -e .[dev]` (or the dependency list in pyproject.toml); `pytest -q`.
2. Synthetic data: `python experiments/make_synthetic_dataset.py` (idempotent).
3. Real data: see DATASET_REGISTRY.md download commands (Zenodo IDs 17255311, 11061947, 24047383, 3909552).
4. Each experiment: `cd experiments && python exp_<X>.py` → `experiments/results/*.json` and figures.
5. Desktop application: `osteoquant-desktop` (or `python -m osteoquant.desktop.app`); bundle: `python packaging/build.py`.
6. Legacy web demo (development only): `python scripts/demo_seed.py && OQ_DB=runtime/demo.db osteoquant serve`.
7. Customer-facing numbers: `python scripts/check_claims.py` must pass before any website, docs or deck change.
