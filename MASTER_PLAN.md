# OsteoQuant — Master Plan

**Status:** research prototype (non-clinical, non-GLP, not validated). Started 2026-11-27.

## Mission
Turn preclinical bone-defect micro-CT (and later histology) into reproducible, auditable
quantitative reports that separate **new bone**, **residual graft** and **host bone**.

## Central hypothesis (UNTESTED on physical data)
A material-aware, context-aware computational system can distinguish new bone, residual graft
and host bone more reliably than threshold-based workflows *under appropriate acquisition
conditions*. Synthetic results can show where this is possible in principle and where it is
not; only physical phantoms / customer data can establish it for real materials.

## Architecture (single Python package + browser viewer; no microservices)

```
osteoquant/
  io/            ingestion: TIFF stack, DICOM, NIfTI, NRRD, OME-TIFF, Zarr, Zeiss TXM; hashing; provenance
  qc/            scan quality checks (validated vs heuristic flagged separately)
  phantom/       procedural 3D bone-defect phantom generator (fast + CT-physics modes)
  segment/       classical baselines (threshold, Otsu, multi-Otsu, GMM, k-means, RF, watershed, region growing)
  ml/            3D/2.5D U-Net training, inference, ensembles, adaptation
  roi/           defect ROI engine (cylinder fit, calvarial disc, segmental gap, manual)
  morphometry/   BV/TV, Tb.Th/Tb.Sp (local thickness), Tb.N, BS, Conn.D (Euler), Ct.Th, bridging, TMD (calibrated only)
  uncertainty/   entropy, ensemble/TTA disagreement, calibration (ECE), selective prediction, OOD
  longitudinal/  rigid/affine/deformable registration, change maps, day-0 graft subtraction experiments
  histology/     2D stain separation, tissue/bone/graft area, nuclei (classical), WSI tiling
  stats/         descriptive, CI, effect sizes, ICC (Koo & Li forms), Bland–Altman, mixed models, multiplicity
  report/        DefectFill PDF/CSV report generator
  audit/         append-only hash-chained audit log, file hashing, config snapshots
  study/         SQLite study store: orgs, projects, studies, groups, specimens, timepoints, scans, jobs
  api/           FastAPI app: auth, RBAC, tenant isolation, job runner, viewer endpoints
web/static/      researcher viewer (orthogonal slices, overlays, brush editing, ROI, uncertainty, 3D mesh)
experiments/     Experiments A–P (scripts + results JSON/figures)
docs/            science knowledge base, research, quality/CSV docs, security
business/ grants/ outreach/ validation/ publications/ investor/ founder/
```

## Workstreams and owners
| # | Stream | Owner | Output location |
|---|---|---|---|
| 1 | Domain science | science subagent | docs/science |
| 2 | Competitive intel | research subagent | docs/research/COMPETITOR_INTELLIGENCE.md |
| 3 | Datasets | data subagent + lead | docs/research/DATASET_REGISTRY.md, data/manifest |
| 4–9 | Ingestion, baselines, ML, phantoms, morphometry, stats | lead engineer | osteoquant/ |
| 10–11 | Frontend / backend | lead engineer | web/, osteoquant/api |
| 12 | Quality systems | quality subagent | docs/quality |
| 13 | Commercialization | commercial subagent | business/ |
| 14 | Funding | grants subagent | grants/ |
| 15 | Security & independent review | review subagent (late) | docs/security |
| — | Collaborators & physical validation | outreach subagent | outreach/, validation/ |

## Execution order (from founder directive §40)
1 environment+sources → 2 datasets → 3 ingestion → 4 phantoms → 5 baselines → 6 morphometry →
7 real-data experiments → 8 three-class model → 9 uncertainty/adaptation → 10 viewer → 11 study mgmt →
12 reports → 13 longitudinal → 14 histology/expansion → 15 benchmarking → 16 security/quality →
17 physical validation → 18 customers/collaborators → 19 grants → 20 manuscripts → 21 commercial → 22 review.

## Definition of done
See founder directive §41. Tracked item-by-item in `EXECUTION_STATE.md`.
