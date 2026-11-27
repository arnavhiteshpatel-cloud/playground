# SOP-007: Model Release, Validation Records and Version Locking

| Field | Value |
|---|---|
| SOP ID / version | SOP-007 / 0.2 (DRAFT) |
| Effective date | Not effective (draft) |
| Owner | ML Lead with Scientific Lead |
| Related requirements | URS-050, URS-051, URS-054, URS-111, URS-112, URS-150, URS-160, URS-161; FS-050-1, FS-054-2, FS-111-1/2, FS-112-1, FS-160-1/2, FS-161-1; RSK-08, RSK-09, RSK-10, RSK-11, RSK-39 |

> **Status: DRAFT. Not approved or effective. No claim of 21 CFR Part 11 compliance, GLP compliance or validation.** A validation record under this SOP is engineering evidence about one model on one material; it is not a regulatory validation.

## 1. Purpose
Ensure only evaluated, approved, hash-identified segmentation models are used for study results, that learned models support graft endpoints only with qualifying material-specific evidence, and that any change is controlled.

## 2. Definitions
- **Model version:** a unique combination of weights, architecture code, preprocessing, postprocessing/thresholds and label map; any change creates a new version with a new SHA-256.
- **Status:** EXPERIMENTAL → CANDIDATE → RELEASED → RETIRED. The software does not yet store or enforce this status (FS-112-1); it is held in the model registry record and the release CR.
- **Validation record:** an entry in `models/validation_records.json` (`osteoquant.ml.validation_records.ValidationRecord`): model name and SHA-256, material, data class, number of specimens, voxel-size range, scanner class, graft-volume error (p95), reference method, evidence location.

## 3. Procedure
1. **Data governance:** document training/validation/test data (study IDs, species, defect model, graft materials, scanners, voxel sizes), annotation protocol, annotators and data licences. Test data disjoint by animal (preferably by study). No PQ reference specimens in training data.
2. **Training record:** code commit, configuration, seeds, environment, hardware (recorded in the checkpoint by the training code).
3. **Manifest / registry:** model ID, version, SHA-256 of each artifact (PyTorch and ONNX), canonical label map, input specification, intended domain, licence tag, metrics summary, known limitations.
4. **Evaluation (CANDIDATE):** label-map equality with the canonical map (the software checks the class count only, FS-054-2); class-order sanity test on golden cases; per-class Dice and volume error on held-out data stratified by material and scanner; comparison with the current RELEASED model; determinism check; ONNX vs PyTorch agreement.
5. **Validation records:** create a record only from physical-phantom, ex-vivo or in-vivo data (synthetic never qualifies) with ≥ 8 specimens and a graft-volume p95 error ≤ 15 %, for the exact model SHA-256 and material. The evidence (report, dataset) is stored at the recorded location. Because the record file is not integrity-protected by the software (FS-161-1), each addition is made under a CR, the file's SHA-256 is recorded in the CR, and the file is checked against that hash at every release and IQ.
6. **Approval:** Change Request (major) with the evaluation report and any validation records; approval by ML Lead, Scientific Lead and Quality; PQ re-execution scope per PQ_PLAN §7.
7. **Release:** registry status RELEASED; artifacts stored write-protected; hashes published with the release; ONNX export placed in the desktop models directory (`<install dir>/_internal/models` in the packaged application) only for RELEASED models.
8. **Use:** study protocols name the model version and SHA-256. The loader verifies the hash at every load. Pickled random-forest models are not available in the desktop.
9. **Monitoring:** periodic review of correction magnitudes (SOP-003 step 8), uncertain fractions and support decisions per model version.
10. **Retirement:** set RETIRED (no new study runs); keep artifacts, manifest and validation records for as long as any result depends on them (DATA_RETENTION_POLICY).

## 4. Prohibited
Replacing an artifact file in place; using EXPERIMENTAL models for study results; editing `validation_records.json` outside a CR; changing thresholds without a new version; fine-tuning a released model per study without a new version, evaluation and CR.

## 5. Records
Manifest, training record, evaluation report, validation records with evidence, CR and approvals, registry history, record-file hashes.

## 6. Revision history
| Version | Date | Change | Author |
|---|---|---|---|
| 0.1 | 2026-11-27 | Initial draft | QA/RA |
| 0.2 | 2026-11-27 | Validation records (URS-160/161); desktop model directory; procedural release status and record-file hashing until implemented | QA/RA |
