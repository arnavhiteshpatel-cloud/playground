# OsteoQuant — Software Verification Plan

| Field | Value |
|---|---|
| Document ID | OQ-QMS-VP-001 |
| Version | 0.1 (DRAFT) |
| Date | 2026-11-27 |
| Owner | Engineering Lead |
| Related | URS, FS, RISK_ASSESSMENT.md, traceability_matrix.csv, OQ_PROTOCOL.md |

> **Status: DRAFT — not validated; not a claim of Part 11 compliance or GLP validation.**
> The companion `traceability_matrix.csv` is likewise a DRAFT template.

## 1. Purpose
Define how engineering verifies that the implementation meets the FS (design verification), producing evidence reusable in OQ. Validation for intended use (PQ, user acceptance) is separate.

## 2. Software classification and approach
- GAMP 5 (benchmark): **custom application** (Category 5) on infrastructure/standard components (Category 1/3) — highest scrutiny on custom code and the ML model [INF].
- Risk-based rigor following FDA CSA thinking (benchmark only): scripted, independently reviewed tests for high-risk functions (RSK S ≥ 4); unscripted/exploratory testing acceptable for low-risk UI conveniences, with a brief record.

| Risk tier | Examples | Required verification |
|---|---|---|
| High (S ≥ 4) | Voxel spacing, label map, hashing, audit chain, blinding, signatures, morphometry, tenant isolation, retention | Unit + integration tests with explicit expected values; negative/challenge tests; code review by second engineer; mutation or property-based tests where practical; 100% of FS items traced |
| Medium | QC plug-ins, exports, reporting layout | Unit/integration tests; code review |
| Low | Cosmetic UI | Exploratory test notes |

## 3. Test levels and tooling (proposed)
| Level | Tooling | Location (proposed) |
|---|---|---|
| Static analysis | `ruff`, `mypy --strict` on core packages, `bandit`, `pip-audit` | CI |
| Unit | `pytest`, `hypothesis` (property-based: e.g., hash-chain verification, spacing normalisation, CSV round-trip) | `tests/unit/` |
| Integration | `pytest` + FastAPI TestClient, temp SQLite, temp file store, two-tenant fixtures | `tests/integration/` |
| System / E2E | Scripted API flows; optional Playwright for browser viewer | `tests/system/` |
| Numerical regression ("golden") | Frozen golden datasets with expected metrics JSON and tolerances; run on every PR touching io/roi/segment/morphometry/stats | `tests/golden/`, data in `validation/golden/` |
| Model evaluation | Held-out test set metrics, label-map check, determinism check | `validation/model_eval/` |

Test naming: `test_<behaviour>` as proposed in traceability_matrix.csv; each test docstring cites FS ID(s), e.g. `"""FS-054-1; RSK-08"""`. A CI script shall parse docstrings to fill `test_id`/`test_file` columns and fail if any FS row lacks a test.

## 4. Coverage targets
- Requirements coverage: 100% of FS items with ≥ 1 test (or documented review for documentation FS).
- Code coverage (line/branch): ≥ 90% for `audit`, `io`, `roi`, `segment` (label handling), `morphometry`, `stats`, `api` auth layer; ≥ 75% overall. Coverage is a guide, not acceptance on its own.

## 5. Numerical tolerances (proposed, to be approved)
| Quantity | Phantom | Tolerance |
|---|---|---|
| Volume of voxelised sphere/cylinder (radius ≥ 10 voxels) | Synthetic | ≤ 1% relative vs analytic volume of the voxelised object; ≤ 3% vs continuous analytic |
| Plate thickness (distance-transform Tb.Th method) | Synthetic plates 5–20 voxels | ≤ 1 voxel absolute |
| Unit conversion | mm ↔ µm | Exact (factor 1000), float round-trip exact |
| Hash | Any file | Exact match with `hashlib`/`sha256sum` |
| CSV round-trip | Random floats | Exact `float` round-trip |
| Re-run reproducibility | Golden datasets | CPU deterministic: bitwise; GPU: per-metric tolerance documented |

## 6. Special verification topics
- **Audit chain:** property-based tests generating random sequences of tamper operations (modify, insert, delete, swap, truncate) — verification must detect 100%.
- **Tenant isolation:** generated test that enumerates all routes × object types and asserts cross-tenant access fails.
- **Label map:** tests with permuted maps, extra labels, wrong dtype; legend generation from map.
- **Blinding:** search all exports/filenames/log lines produced pre-unblinding for allocation strings.
- **Dependency drift:** golden regression run when lock file changes.
- **Security:** authentication/authorization tests; OWASP-style checks for injection on query params; secrets not logged.

## 7. Defect management
Defects tracked with ID, severity (mapped to risk tiers), affected FS/URS, fix commit, verifying test. High-severity defects block release.

## 8. Release verification criteria
1. All high-tier tests pass; no open high-severity defects.
2. Golden regression unchanged or changes explained and approved via CHANGE_CONTROL.
3. Traceability matrix regenerated; no FS without test.
4. Static analysis: no new high-severity findings; `pip-audit` critical CVEs resolved or risk-accepted.
5. Verification summary report attached to release notes (URS-141).

## 9. Records
CI logs (with commit SHA, environment, timestamp) retained per DATA_RETENTION_POLICY.md; verification summary reports under document control.
