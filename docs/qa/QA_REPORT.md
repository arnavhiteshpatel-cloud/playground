# OsteoQuant QA Report (Gen-2 test campaign, 2026-11-27)

> **Superseded figures (2026-11-28).** This report records the 27 November test campaign. Its test counts and coverage
> are historical. The single current source is [`test_summary.json`](test_summary.json): 611 passed, 1 skipped; 93.4%
> line+branch coverage of the `osteoquant` package (99% on critical modules) with the desktop UI code excluded (local
> full run at commit `d124ae6`). The 91% "Final" figure below comes from `coverage_final.txt` (27 Nov, 22:48 UTC), whose run recorded
> 1 failed test; do not quote it. CI passed for the first time on 2026-11-28; §7 is updated to the current workflow.

Scope: everything in `osteoquant/` except `osteoquant/desktop/` (GUI, tested separately by
`tests/desktop` and `.github/workflows/desktop-release.yml`). Commands are run from the repository root.

Related files:
- `docs/qa/DEFECTS_FOUND.md`: every defect, with its reproduction and regression test.
- `docs/security/SECURITY_REVIEW_GEN2.md`: security findings.
- `docs/qa/coverage_baseline.txt` and `docs/qa/coverage_final.txt`: raw coverage output.

## 1. Headline numbers

| | Baseline | Final |
|---|---|---|
| Tests (non-desktop) | 61 | 414 (469 including `tests/desktop`) (of which 318 new QA tests, plus 35 added by other workstreams during the campaign) |
| Suite runtime (4 CPU, shared host) | ~25 s | 2 min 28 s for the whole suite including desktop, single process, on a host at load ≈ 12 (one test marked `slow`) |
| Line+branch coverage, whole package excl. desktop | 62 % (4 752 statements) | **91 %** (6 404 statements; the package grew by ~1 650 statements during the campaign) |
| Defects found | — | 25 (21 fixed with regression tests, 4 assigned to lead) + 6 documented ambiguities |
| Security findings (Gen-2) | — | 20 (1 critical-conditional, 4 medium, 13 low, 2 info); all critical/medium fixed |

## 2. Coverage per module (branch coverage on; `pytest --cov --cov-branch`)

Critical scientific and I/O modules (target ≥ 95 %):

| Module | Baseline | Final |
|---|---|---|
| `morphometry/core.py` | 87% | 98% |
| `morphometry/analytic.py` | 72% | 100% |
| `stats/core.py` | 56% | 99% |
| `segment/metrics.py` | 73% | 100% |
| `uncertainty/core.py` | 23% | 91% | (100 % in isolation, see notes)
| `io/readers.py` | 55% | 99% |
| `io/writers.py` | 82% | 100% |
| `io/safe_archive.py` | 36% | 96% |
| `audit/log.py` | 85% | 99% |

Other modules:

| Module | Baseline | Final |
|---|---|---|
| `advisor/characterize.py` | new | 74% |
| `advisor/integration.py` | new | 84% |
| `advisor/separability.py` | new | 93% |
| `api/app.py` | 80% | 97% |
| `api/bundle.py` | 87% | 90% |
| `cli.py` | 0% | 90% |
| `histology/core.py` | 0% | 84% |
| `io/transforms.py` | 42% | 100% |
| `licensing/core.py` | new | 87% |
| `licensing/keys.py` | new | 100% |
| `longitudinal/core.py` | 0% | 84% |
| `ml/core.py` | new | 100% |
| `ml/runtime.py` | new | 72% |
| `ml/synth_dr.py` | new | 86% |
| `ml/train.py` | 65% | 93% |
| `ml/unet.py` | 83% | 77% |
| `ml/validation_records.py` | new | 93% |
| `phantom/ctsim.py` | 0% | 96% |
| `phantom/generator.py` | 76% | 78% |
| `phantom/imaging.py` | 52% | 73% |
| `phantom/materials.py` | 69% | 84% |
| `phantom/structures.py` | 84% | 87% |
| `pipeline.py` | 66% | 84% |
| `qc/engine.py` | 94% | 99% |
| `report/defectfill.py` | 77% | 91% |
| `report/figures.py` | 54% | 94% |
| `roi/engine.py` | 54% | 96% |
| `segment/classical.py` | 24% | 93% |
| `study/db.py` | 79% | 96% |
| `study/jobs.py` | 81% | 91% |
| `volume.py` | 97% | 97% |

**Notes on the coverage numbers:**
- The 3 uncovered lines left in `io/safe_archive.py` are defensive checks that cannot be reached
  through `zipfile` or `tarfile`, which already enforce declared sizes.
- `uncertainty/core.py` reaches 100 % when its tests run alone. In the full run its `def` lines
  show as uncovered because the module is imported before measurement starts; its function bodies
  are fully covered.
- `advisor/*`, `licensing/*`, `ml/runtime.py` and `ml/synth_dr.py` were added by other workstreams
  during the campaign, so they have no baseline.

## 3. What the new tests check (beyond executing lines)

| File | Focus |
|---|---|
| `test_morphometry_analytic.py` (40) | Plates: Tb.Th, Tb.Sp, Tb.N and BV/TV exact for even thicknesses, documented +1 voxel for odd. Rods, sphere, cortical tube, marching-cubes area of cube and sphere within stated tolerances. Euler/β1 for 1–5 handles, cavities, 26-connectivity, edge-diagonal cavity. Class-volume additivity with anisotropic spacing. Bridging, BIC, density erosion. The defect endpoint set, including the anisotropic branch. |
| `test_stats_reference.py` (23) | ICC(1,1), (2,1), (3,1), (2,k) and (3,k) point estimates and 95 % CIs against Shrout & Fleiss (1979) and R `psych::ICC` (found QA-013). Bland–Altman on constructed data (bias, LoA, CI formulas, proportional bias, log scale). Hedges g closed form. Holm, Bonferroni and BH against `statsmodels`. Mixed model recovers simulated slopes. Walter (1998) ICC sample size; two-sample n. |
| `test_segmentation_metrics.py` (20) | Dice, IoU, precision and recall closed forms; empty-mask conventions; HD95 and ASSD against a brute-force `cdist` oracle on random, anisotropic and border-touching masks; symmetry; confusion orientation; abstention coverage; ECE bin arithmetic. |
| `test_properties_science.py` (18) | Hypothesis invariants: thickness invariant to permutation and translation; volume ∝ s³, area ∝ s², thickness ∝ s; class volumes partition TV; topology additive over disjoint copies; Dice symmetry and the IoU–Dice identity; confusion totals; ICC invariant to affine rescaling; Bland–Altman constant offset; Hedges g antisymmetry. QC on 7 degenerate volumes (QA-020). |
| `test_io_properties.py` (11) | Hypothesis round trips (random shape, dtype and spacing) for NIfTI, NRRD, Zarr (with content hash), ImageJ TIFF, TIFF stack, DICOM uint16 (exact) and rescaled (within quantisation), TXM (synthetic OLE2 writer `tests/_cfb.py`), NPY. `zrange`/`step` equal array slicing. User-spacing override is recorded. |
| `test_io_destructive.py` (46), `test_io_metadata.py` (22) | Truncation and byte-mutation fuzzing of 7 formats; huge declared dimensions for every format; TXM and DICOM structural faults; hostile uploads (pickle Zarr v2/v3, consolidated metadata, OME external refs, symlinks, XML entity bomb); OME/ImageJ unit handling; multi-frame DICOM. |
| `test_safe_archive.py` (29) | Traversal (8 name forms), symlink/FIFO/device/hard link, member and aggregate bombs, size and count limits, lying central directory, collisions, encryption, corruption, pre-existing symlinks in the destination, TAR policy. |
| `test_audit_properties.py` (12) | Hypothesis: any single-field tamper in any row is detected at that row or the next; deletion and reordering are detected; truncation needs an anchor; triggers; rollback; 4 concurrent writers. |
| `test_security_gen2.py` (19), `test_store_api_workflows.py` (10) | Re-auth lockout, session hygiene, security headers, hostile uploads through the API, corrupt or truncated SQLite, read-only DB, backups, RBAC and tenant checks on every remaining endpoint, job cancel and failure paths. |
| `test_transforms_roi.py` (16), `test_analysis_modules.py` (20), `test_ml_phantom.py` (13) | Resampling and orientation geometry, HA calibration, ROI rasterisation volumes and hashes, plate and segmental detectors (found QA-021). Classical segmenters on constructed 3-phase data. Uncertainty and longitudinal maths; colour deconvolution recovers known stain amounts; reports with CSV-injection neutralised; CLI. Model registry, safe loading (pickled code refused even when the hash is registered), ONNX vs Torch parity, licence guard, CT spectrum. |

The suite runs `--ignore=tests/desktop` in the main CI matrix. Hypothesis profiles:
- `default`: 25 examples per test.
- `ci`: 40 examples, derandomised.
- `thorough`: 300 examples; select with `HYPOTHESIS_PROFILE=thorough`.

## 4. Fuzzing and destructive testing summary

- **Mutation fuzzer** (`scratchpad` harness, then codified in `test_io_destructive.py`). Each case ran in a
  subprocess with a 3 GB address-space limit and a 30 s timeout. Formats: NIfTI (.nii, .nii.gz), NRRD,
  TIFF, TXM, NPY and DICOM; 16 to 41 mutations each.
  - Before the fixes, 9 distinct exception types escaped (QA-004).
  - No hang and no native crash at any point.
  - After the fixes, every malformed input either reads or raises a `ValueError` subclass.
- **Huge declared dimensions:** 10 hostile files (NIfTI ×2, NRRD ×2, TIFF, Zarr ×2, NPY, DICOM series,
  DICOM multi-frame) plus TXM.
  - Before: 4 `MemoryError`s, and one real 2.5 GB allocation from a 2 KB Zarr store (QA-003).
  - After: every case raises `VolumeTooLarge` in under 1 s, before allocating.
- **Archives:** see §3. QA-006, QA-007 and QA-018 were found here.
- **SQLite store:**
  - A garbage or truncated database file raises `sqlite3.DatabaseError` at open.
  - A read-only database rejects audit writes.
  - Reopening is idempotent and the chain survives.
  - An interrupted audit insert rolls back with the chain intact.
- **Interrupted writes:** a Zarr store with a deleted chunk was read silently as zeros (QA-017). It is now detected.
- **Read-only directories:** tested where POSIX permissions apply (skipped as root and on Windows).

## 5. Mutation testing

`mutmut` copies and instruments the whole tree for each run, which is impractical next to concurrent
workstreams. A lightweight AST mutation runner (`tests/tools/mutate.py`) was used instead.

The runner defaults to 1 worker and supports `--sample N --seed S`. At the lead's request, the final stats
run used a 120-mutant sample on 1 niced worker, so the shared host's experiment queue was not starved.

**How it works:**
- It copies the package to a scratch directory and never touches the working tree.
- Operators: arithmetic, comparison, boolean, unary, numeric constant and True/False swaps.
- A sentinel mutant must be killed before the results are trusted. This check caught a sys.path
  pitfall in the first version of the runner.
- Nodes are identified by their full source span, so nested expressions are distinct.

| Module | Mutants run | Killed (final) | Score (first run) | Score (after new tests) | Remaining survivors |
|---|---|---|---|---|---|
| `segment/metrics.py` | 92 (all) | 87 | 0.75 (first valid run, 88 mutants) | **0.946** | 5: two guard-truthiness and one and/or equivalent; 2 killed afterwards by `test_overlap_closed_forms_for_count_patterns` (not re-run) |
| `morphometry/core.py` | 162 (all) | 132 | 0.694 | **0.815** | 30, reviewed: padding/ridge tolerances, bounding-box margins, connectivity-structure constants that scipy clamps, `>`/`>=` on non-empty slices — implementation tolerances not observable on analytic phantoms |
| `stats/core.py` | 120 sampled of 526 (seed 1, 1 worker) | 113 | 0.833 | **0.942** | 7, all equivalent (BH running-min initial value, `n>1` vs `n>=1` where ddof=1 already yields NaN, Koo–Li band boundary at exact equality, curve-fit start values) |

Equivalent or immaterial survivors were reviewed and not chased:
- the guard in `if (2*tp+fp+fn)` (truthiness unchanged);
- padding widths and ridge tolerances in `local_thickness`;
- `max(1, …)` → `max(0, …)` where the second argument is ≥ 1;
- default `border_pad` 24 → 25.

The survivors that would change results were killed with new analytic tests (listed in §3):
- the default spacing on every axis;
- the HD95 percentile;
- the IoU guard;
- background in accuracy;
- ECE per-bin signs and edges;
- sphere coverage;
- the edge-diagonal cavity;
- absolute TV;
- Conn.D;
- radial shells;
- the default bridging axis;
- density erosion and calibration;
- the endpoint set.

## 6. Static analysis

- **ruff** (`[tool.ruff]` in `pyproject.toml`; E, F, W, B with documented ignores):
  - 23 findings at baseline in the selected set.
  - Fixed in `api/`, `io/`, `qc/` and all tests.
  - Remaining: 8 unused imports in modules owned by other workstreams (QA-025). These are per-file
    ignored in the blocking CI step, and a non-blocking step lints the whole package.
- **mypy** (`[tool.mypy]`, Python 3.12 target because the numpy stubs need it): 95 errors in 21 files,
  mostly dict-value inference (`dict[str, float]` later receiving lists or strings) and the zarr
  `Array | Group` union. Non-blocking in CI. Biggest contributors: `advisor/separability.py` (18),
  `phantom/structures.py` (12), `pipeline.py` (10) and `api/app.py` (10).
- **bandit** (excluding desktop):
  - 0 high.
  - 4 medium: B314 ×2 (mitigated, tested) and B608 ×2 (false positive).
  - 16 low: try/except/pass, a fixed `git` subprocess, xml imports.
- **pip-audit:**
  - Declared runtime dependency closure (resolved to the latest versions): no known vulnerabilities.
  - Container environment: 53 advisories in 8 non-runtime packages (pypdf, pip, setuptools, soupsieve,
    httplib2, oauthlib, opentelemetry-api, wheel).
  - The dependency floors still admit vulnerable torch and numcodecs versions (QA-024).

## 7. CI (`.github/workflows/ci.yml`)

- **`lint`:** blocking ruff on the QA-owned and reviewed paths, plus non-blocking ruff on the whole
  package and non-blocking mypy.
- **`test`:**
  - Matrix: ubuntu, windows and macos × Python 3.12 and 3.13 (3.11 dropped: numcodecs>=0.17.1 requires 3.12).
  - CPU torch wheels. On Linux, `libegl1`, `libgl1` and `libxkbcommon0` are installed and
    `QT_QPA_PLATFORM=offscreen` is set.
  - The fast set (`-m "not slow"`) runs everywhere. The full set with coverage, including the desktop and licensing
    tests, runs on ubuntu/3.13 and is blocking (changed 2026-11-28, cycle-3 review C3-PRD-09).
  - Coverage gates (desktop UI code excluded): ≥ 90 % overall and ≥ 95 % for `morphometry/`, `stats/`,
    `segment/metrics.py`, `io/readers.py`, `io/writers.py`, `io/safe_archive.py` and `audit/`. (Until 2026-11-28 the
    overall gate was 85 % and the desktop tests were non-blocking.) Whether CI passes under these new gates is not yet
    recorded.
- **`audit`:** pip-audit on the declared dependencies (blocking) and bandit at medium+ (report only).
- **Windows:** the model-saving tests skip with QA-022 until `fcntl` is replaced.
- No secrets and no publishing; `permissions: contents: read`.

## 8. Items for the lead

1. QA-022: remove the POSIX-only `fcntl` from `ml/train.update_registry`. Windows CI shows the skip.
2. QA-023: pass the verified bytes to `onnxruntime.InferenceSession`.
3. QA-024: raise the dependency floors to `torch>=2.6` and `numcodecs>=0.17.1`.
4. QA-025: remove the unused imports in `ml/train.py`, `phantom/materials.py`, `advisor/characterize.py` and `desktop/*`, then make whole-package ruff blocking.
5. Decide OBS-01 (Dice of two empty masks), OBS-02 (CCC moments) and OBS-05 (blank volume should fail QC).
6. Still open from the security reviews:
   - G2-16: cross-tenant audit count.
   - G2-17: synchronous upload parsing.
   - G2-18: scrypt cost.
   - S-15: compute quotas.
   - S-20: idle timeout.
