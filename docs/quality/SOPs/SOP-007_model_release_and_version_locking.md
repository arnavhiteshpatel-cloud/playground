# SOP-007 — Model Release and Version Locking

| Field | Value |
|---|---|
| SOP ID / version | SOP-007 / 0.1 (DRAFT) |
| Effective date | Not effective (draft) |
| Owner | ML Lead with Scientific Lead |
| Related requirements | URS-050, URS-051, URS-054, URS-111, URS-112; FS-050-1, FS-054-1, FS-111-1, FS-112-1; RSK-08, RSK-09, RSK-10, RSK-11 |

> **Status: DRAFT — not validated; not a claim of Part 11 compliance or GLP validation.**

## 1. Purpose
Ensure only evaluated, approved, hash-identified segmentation models are used for study results, and that any model change is controlled.

## 2. Definitions
- **Model version:** a unique combination of weights, architecture code, preprocessing, postprocessing/thresholds and label map. Any change → new version.
- **Status:** EXPERIMENTAL → CANDIDATE → RELEASED → RETIRED.

## 3. Procedure
1. **Data governance:** document training/validation/test datasets (study IDs, species, defect model, graft materials, scanners, voxel sizes), annotation protocol and annotators. Test set disjoint by animal (preferably by study). No PQ reference specimens in training data.
2. **Training record:** code commit, configuration, random seeds, environment (lock file), hardware.
3. **Manifest:** create `model_manifest.json`: model_id, version, sha256 of artifact(s), canonical label map, input spec (voxel size range, intensity normalisation), validated domain, training-data reference, metrics summary, known limitations.
4. **Evaluation (CANDIDATE):**
   - Label-map equality check vs canonical map; class-order sanity test on golden cases (e.g., known graft-only phantom must be labelled 2).
   - Per-class Dice/volume error on held-out test set, stratified by graft material/scanner.
   - Comparison with currently RELEASED model on the golden datasets; report metric differences.
   - Determinism check.
5. **Approval:** Change Request (Major) with evaluation report; approval by ML Lead, Scientific Lead and Quality. PQ re-execution scope per PQ_PLAN §7.
6. **Release:** registry status RELEASED; artifact stored write-once; hash published in release manifest.
7. **Use:** studies specify model version in protocol; loader verifies hash every load (FS-111-1). Ongoing studies keep their model version unless a justified change is approved.
8. **Monitoring:** periodic review of correction magnitudes (SOP-003 §4.6) and uncertainty flags per model version for drift signals.
9. **Retirement:** set RETIRED (no new runs); retain artifact and manifest for as long as any results depend on it (DATA_RETENTION_POLICY).

## 4. Prohibited
Replacing an artifact file in place; using EXPERIMENTAL models for study results; changing thresholds without a new version.

## 5. Records
Manifest, training record, evaluation report, CR and approvals, registry history.

## 6. Revision history
| Version | Date | Change | Author |
|---|---|---|---|
| 0.1 | 2026-11-27 | Initial draft | QA/RA |
