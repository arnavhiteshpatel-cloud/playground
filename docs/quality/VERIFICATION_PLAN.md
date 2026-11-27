# OsteoQuant — Software Verification Plan

| Field | Value |
|---|---|
| Document ID | OQ-QMS-VP-001 |
| Version | 0.2 (DRAFT), Generation-2 desktop re-baseline |
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
| High (S ≥ 4) | Voxel spacing, label map, hashing, audit chain, blinding, signatures, re-authentication, morphometry, measurement support, validation records, retention | Unit + integration tests with explicit expected values; negative/challenge tests; code review by second engineer; mutation or property-based tests where practical; 100% of FS items traced |
| Medium | QC plug-ins, exports, reporting layout | Unit/integration tests; code review |
| Low | Cosmetic UI | Exploratory test notes |

## 3. Test levels and tooling
| Level | Tooling | Location (as built, 2026-11-27) |
|---|---|---|
| Static analysis | `ruff`, `bandit`, `pip-audit` (manual runs recorded in `docs/security/`); `mypy --strict` proposed | CI (partly) |
| Unit / property | `pytest`, property-style randomised tests (hash chain, I/O round-trips, morphometry invariances) | `tests/test_*.py` |
| Integration (library + store) | `pytest`, temporary SQLite project stores, temporary scan stores | `tests/test_*.py` |
| Desktop (model/service and widget) | `pytest-qt`, `QT_QPA_PLATFORM=offscreen`; services and models tested without windows, widgets off-screen | `tests/desktop/` |
| System / end-to-end | `python -m osteoquant.desktop --selftest` (headless import → QC → analysis → edit → report → chain verification); exercised by `tests/desktop/test_main_window.py::test_selftest_entry_point` | `osteoquant/desktop/selftest.py` |
| Optional API interface | FastAPI TestClient | `tests/test_api.py`, `tests/test_store_api_workflows.py`, `tests/test_security_gen2.py` |
| Numerical / scientific experiments | Scripted experiments with recorded results (not part of the pytest suite) | `experiments/`, `experiments/results/` |

Traceability: `scripts/build_traceability.py` holds the requirement → test mapping, checks every referenced test against `pytest --collect-only -q`, checks URS/FS/protocol consistency and writes `traceability_matrix.csv`. Run it (or `--check` in CI) whenever tests or requirements change.

## 4. Coverage targets
- Requirements coverage: 100% of FS items with ≥ 1 test (or documented review for documentation FS).
- Code coverage (line/branch): ≥ 90% for `audit`, `io`, `roi`, `segment` (label handling), `morphometry`, `stats`, `study` (access control), `licensing`, `advisor`; ≥ 75% overall. The recorded baseline (`docs/qa/coverage_baseline.txt`, library only, desktop excluded) is 62% overall. Coverage is a guide, not acceptance on its own.

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
- **Role enforcement (desktop):** test that enumerates desktop actions × roles and asserts the permission matrix (FS-011-2). Organisation isolation remains tested for the optional API.
- **Label map:** tests with permuted maps, extra labels, wrong dtype; legend generation from map.
- **Blinding:** search all exports/filenames/log lines produced pre-unblinding for allocation strings.
- **Dependency drift:** golden regression run when lock file changes.
- **Security:** authentication/authorisation and re-authentication lockout tests (including the desktop path, FS-092-2); malicious-input corpus (FS-133-1); a network-blocked self-test for offline operation (FS-210-1, FS-211-1).
- **Measurement support:** tests that read the rendered PDF/CSV for support status, conditions and advisor version (FS-152-2).

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
