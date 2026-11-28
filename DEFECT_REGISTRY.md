# Defect Registry

Single list of defects across the project. QA-stream details: `docs/qa/DEFECTS_FOUND.md`; security:
`docs/security/`. Severity: S1 wrong result/claim or data loss · S2 feature broken · S3 degraded · S4 cosmetic.

| ID | Sev | Area | Description | Found by | Status | Fix / evidence |
|---|---|---|---|---|---|---|
| DF-001 | S1 | docs | Manuscript 1 stated RF trained on 6 specimens with 15k voxels/class; code trains on 12 (3/material), ≤8,000 voxels/class/specimen | forensic audit FA-10 | fixed | publications/MANUSCRIPT_1_separability.md §2.4 |
| DF-002 | S3 | experiments | `experiments/common.py` always overwrote `experiments/results/` during reproduction | forensic audit | fixed | `OQ_RESULTS` override (ADR-G2-07) |
| DF-003 | S1 | pipeline | Graft volume is reported for any material, even when separation is known to be impossible | FA-16 | fixed | `osteoquant/advisor`; pipeline `reported_metrics` suppress unsupported endpoints; tests/test_advisor.py |
| DF-004 | S2 | ROI | Segmental ROI fails after bridging (explicit exception, no fallback) | FA-05 | mitigated (library) | ROI propagation from an early timepoint (`longitudinal.propagate_roi`, Experiment F2: Dice 0.984, QC 16/16); no desktop longitudinal workflow yet, so the desktop still asks for a manual ROI |
| DF-005 | S3 | docs | Day-18 ROI confidence quoted with inconsistent rounding across documents | FA-27 | fixed | `scripts/check_claims.py` (8 claims, all pass) |

Historical defects fixed in Generation 1 (S-01…S-19, Q-01…Q-14, RESEARCH_LOG errors) are recorded in
`docs/security/REVIEW_RESPONSE.md` and `RESEARCH_LOG.md`.
| DF-006 | S1 | advisor | Oracle threshold could be a non-contiguous bin union, which no threshold method can apply | Experiment S1c | fixed | best single contiguous threshold (advisor 1.1.0+) |
| DF-007 | S1 | advisor | Partial-volume halos of dense graft counted as new bone; mineral endpoints over-reported | Experiment S1b | fixed | mineral rule (1.2.0) |
| DF-008 | S1 | advisor | BCP/β-TCP profiles did not match the scanned graft level; support granted on a wrong profile | Experiment S1b | fixed | scan-vs-profile check >15% (1.3.1); KB/physics cross-check (1.3.0) |
| DF-009 | S1 | advisor | Measured control references made the advisor over-confident (no graft-adjacent blur) | Experiment S1c | fixed (constant untested on held-out data) | graft-adjacent mixing (1.3.2); C2-SCI-06 open |
| DF-010 | S1 | advisor | Supported new-bone volumes over-estimated by 20–50% and graft by 21–28% under wider blur | held-out S1H (pre-registered) | fixed | scan-measured blur, error propagation, ambiguous rim (1.4.0); validated on S1H3 |
| DF-011 | S1 | advisor | Supported total mineral over-estimated (+20–25%) when blur σ ≈ 1 voxel: one-voxel rim too narrow | held-out S1H2 (pre-registered) | fixed | rim width max(1,⌈2σ⌉) (1.4.1); validated on S1H3 |
| DF-012 | S1 | pipeline | Support decisions applied to any segmentation method, although validated only for the advisor threshold | cycle-2 review C2-SCI-02 | fixed | `pipeline.bind_support_to_method`; `advisor_threshold` is the default |
| DF-013 | S1 | advisor | Metals: total mineral could be reported despite unmodelled artefacts | C2-SCI-09 | fixed | 1.4.2 |
| DF-014 | S1 | report | Group statistics counted refused (not-measured) values and printed Holm p = 1.000 for uncomputable tests | cycle-2 review C2-SCI-14 | fixed | `report/defectfill.py`; per-endpoint n; test |
| DF-015 | S2 | longitudinal | Registration QC compared floating-point projected shifts with the tolerance exactly: an exact 2-voxel shift (80.00000000000001 µm) failed an 80 µm tolerance | F2 re-run | fixed | shifts rounded to 1 nm; `test_registration_qc_exact_tolerance_shift_passes` |
| DF-016 | S2 | longitudinal | Registration QC could not see shifts along a tube axis (aperture problem) | C2-SCI-04 | fixed | structure-tensor projection; `partially_unverifiable` |
| DF-017 | S2 | ML | Model registry writes raced; fine-tuned models lost provenance; `fcntl` lock unavailable on Windows | cycle-1 review | fixed | locked atomic registry with portable lock; parent provenance inheritance |
| DF-018 | S1 | ML | ONNX model hash verified, then file re-read (time-of-check/time-of-use) | cycle-1 security review | fixed | `ml/runtime.py` loads the verified bytes |
| DF-019 | S3 | ML | ONNX runtime path imported PyTorch | Gen-2 packaging | fixed | torch-free `ml/core.py` |
| DF-020 | S2 | longitudinal | Granule tracking v1 produced spurious ~700 µm matches that the advisor accepted | Experiment L3 | fixed | tracking v2 (distance prior, ambiguity); 0 supported-but-failed |
| DF-021 | S3 | docs | S1H2 total-mineral count misquoted as "10/141 supported failed" (141 were the supported-and-OK cases; 151 were supported) in EXPERIMENT_REGISTRY and EVIDENCE_LEDGER | report rebuild cross-check | fixed | corrected to 10/151; the Gen-2 report table reads the counts from the result file |
| DF-022 | S2 | CI / packaging | GitHub Actions CI never passed on this branch: on Python 3.11 the install failed (numcodecs>=0.17.1 requires 3.12) and on 3.13 tests failed because `cryptography` (licensing, signed validation records) and `pypdfium2` (PDF tests) were not declared dependencies. Earlier status documents described CI as configured without noting that no run had passed | GitHub Actions run logs (runs 26, 32, 38, 48) | fixed (pending CI confirmation) | `requires-python >=3.12`; `cryptography` a core dependency; `pypdfium2` in dev/desktop extras; CI matrix 3.12/3.13 |
| DF-023 | S2 | io | NIfTI, NumPy and uncompressed TIFF readers returned arrays backed by a memory map of the user's source file (`np.ascontiguousarray` does not copy a contiguous memmap slice): the source stayed mapped, so on Windows it could not be overwritten or deleted | Windows CI (`test_nifti_4d_and_unknown_units`) | fixed | `io/readers._owned`; `test_reader_output_does_not_keep_source_memory_mapped` (fails on the old code for all three formats) |
| DF-024 | S4 | tests | Archive tests split returned paths on "/", which fails with Windows paths | Windows CI | fixed | `tests/test_safe_archive.py` uses `Path.relative_to` |
| DF-025 | S2 | report | The synthetic ground-truth table ("meas / true") printed measured new-bone and graft fractions even when the endpoint was refused, so a refused value appeared as a number (phantom reports only; truth exists only for synthetic data) | coverage-driven report test | fixed | `report/defectfill.py` uses the support status there too; `test_report_prints_refused_values_as_not_measured_with_reasons` (fails on the old code) |
| DF-026 | S3 | tests | Two ML tests were still skipped on Windows for QA-022 (fcntl) after the portable registry lock was added, so Windows CI never exercised the lock | coverage review | fixed | skips removed |
| DF-027 | S3 | knowledge | `validate_materials` (citation-integrity and schema check of the materials knowledge base) had no tests | coverage review | fixed | `tests/test_knowledge.py` (shipped file valid; every reference key in references.bib) |
| DF-028 | S3 | docs | L3 advisor result quoted as "all 60 failed day-0 measurements refused"; the file has 59 failures among 60 measurements (all 60 refused) | deck rebuild cross-check | fixed | EVIDENCE_LEDGER G2-005 and the L3 registry row corrected |
