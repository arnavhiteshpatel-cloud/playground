# Forensic Audit of the Generation-0 Baseline

**Naming.** "Generation 0" in this mandate = the baseline delivered under the first mandate (called Generation 1 in
some earlier documents: SCIENTIFIC_EVIDENCE, DECISIONS, docs/security). Both refer to commit `ee09a70`.

**Baseline snapshot:** git commit `ee09a70` on branch `claude/osteoquant-autonomous-dev-ujqgkl` (27 Nov 2026). The
commit is the recoverable snapshot: `git checkout ee09a70` restores every file, result JSON and document exactly as
audited. Data (`data/`, 12 GB) and model weights (`models/`, 40 MB) are git-ignored; their regeneration commands are
in `DATASET_REGISTRY.md` and `experiments/`. Original results are preserved unchanged in `experiments/results/`;
reproduction outputs go to `experiments/results_gen0_repro/`.

**Method.** Every load-bearing claim in the README, handoff, evidence ledger, experiment registry, manuscripts, decks
and sample reports was traced to code and to a result file; key experiments were re-run from scratch (Section 2);
code paths were read for silent assumptions. Each finding has an ID (FA-NN), severity, evidence and a remediation
action with an owner workstream. Severity: **Critical** = would make a customer-facing number wrong or a claim false;
**High** = blocks the product thesis or misleads by omission; **Medium** = weakens evidence; **Low** = hygiene.

## 1. Executive verdict

The baseline is a well-instrumented *research prototype*, honest about most limitations, but its central product
claim — automatic separation of residual graft from new bone — is supported **only by synthetic data and an
optimistic longitudinal simulation**. The single real-data result (dog forelimb bone vs background, Dice 0.826) is a
two-class bone segmentation task, not the three-class task the product sells. The user interface is a local web
server, not a desktop application. The commercial numbers (time saving, pricing, willingness to pay) are assumptions.

## 2. Reproduction of prior results

| Experiment | Original | Reproduced | Status |
|---|---|---|---|
| G morphometry vs Scanco IPL (8 real cubes) | Tb.Th ICC 0.983, Tb.Sp 0.948 | Tb.Th 0.983, Tb.Sp 0.948 (identical to 16 digits) | **reproduced exactly** (153 s) |
| P reproducibility | all bit-identical | all checks pass | **reproduced** (89 s) |
| C separability (32 conditions) | RF/multi-Otsu graft Dice per condition | max absolute difference 0.0036 Dice across 64 values | **reproduced within 0.004** (335 s); not bit-identical — RF voxel sampling/threading; note the script still emits the superseded `bayes_*` fields, the corrected oracle comes from `recompute_intensity_oracle.py` |
| H/I real dog | U-Net 0.826; synthetic zero-shot 0.379 | 29 per-specimen rows (Otsu, GMM, RF, retrained real U-Net ×5, synthetic zero-shot ×5, fine-tuned k=1 ×4) identical to the original to 4 decimals (max difference 0.0); stopped before the last k=1 specimen and k=3 to free CPU | **reproduced exactly** (deterministic retraining, ~3 CPU-h under contention) |
| Test suite | 61 pass | **61 pass (24 s)** | reproduced |

## 3. Findings and remediation register

| ID | Sev. | Finding | Evidence | Remediation (workstream) |
|---|---|---|---|---|
| FA-01 | **Critical** | No real three-class validation exists. All new-bone/graft/host numbers (R3–R8) are synthetic. | EXPERIMENT_REGISTRY A–L; R12 is 2-class bone | Never present synthetic Dice as product accuracy; scorecard separates synthetic vs real columns; build material-specific *support/abstain* logic so the product refuses unsupported 3-class measurements; physical phantom programme (validation/) remains the path to real 3-class truth. (Science, Product) |
| FA-02 | **Critical** | Synthetic-only training transfers poorly to real scans (zero-shot Dice 0.379). | exp_H_I_real.json | Phantom v2 with scanner statistics measured on real scans; domain randomisation; intensity normalisation; self-supervised/denoising pretraining on unlabeled real volumes; few-shot fine-tuning curves with multiple seeds and CIs. (Science) |
| FA-03 | High | OOD detection is weak (ID-vs-OOD AUROC 0.66, single model, max-softmax entropy). | exp_K_M_uncertainty.json | Deep ensembles + MC dropout + feature-space Mahalanobis; image-level QC features; evaluate failure-detection AUROC (predict Dice<threshold) not just OOD AUROC; conformal volume intervals with coverage tests. (Science) |
| FA-04 | **Critical** | Longitudinal day-0 result (R4, Dice 0.915/0.816) assumes graft shrinks *in place*: no migration, fragmentation, swelling, or deformation; registration failure is not detected. | exp_L / L2; review Q-11 | Phantom v2 longitudinal: granule displacement, fragmentation, non-uniform resorption, host remodelling; deformable refinement; registration-quality metrics and explicit failure flags; report how Dice degrades vs displacement magnitude. (Science) |
| FA-05 | High | Segmental ROI detection fails (50% explicit failures) once regenerate bridges the gap. | exp_F_roi.json | Use day-0/early-timepoint ROI propagation through registration; user-confirmed ROI templates; detection from fixation-hardware geometry; never silently guess. (Science, Desktop) |
| FA-06 | High | "≈78% analyst time saving" is modelled from **assumed** effort constants (20 s vs 90 s/slice), yet appears in commercial materials. | exp_K_M effort_model; investor decks | Relabel everywhere as hypothesis; desktop app records real interaction timing (opt-in, local) so a timed user study can measure it; customer-workflow benchmark protocol. (Commercial, Desktop) |
| FA-07 | Medium | Morphometry border convention ("edge") was selected *after* seeing the 8 IPL cubes; agreement 0.983 is not independent. | Review Q-10 | Pre-register the convention now; validate on held-out real data (new IPL/BoneJ datasets from research stream); report both conventions. (Science, Research) |
| FA-08 | High | Small real n: 5 real test specimens (dog), 2 real ovine scans, 8 IPL cubes; CIs wide or absent. | exp_H, exp_F | Specimen-level bootstrap CIs everywhere; leakage-free split manifests; add every openly licensed dataset found (research stream); report n beside every number. (Science, Research) |
| FA-09 | Medium | Histology module immature: bone-area ICC 0.35; Macenko normalisation worsens results; nuclei object F1 0.34. | exp_N_histology.json | Scope histology to *complementary* features only (graft-void area, registration overlay); do not market quantitative histomorphometry until validated; consider deep nuclei models only if a commercial-compatible licence exists. (Science) |
| FA-10 | **Critical** | Specimen-count inconsistency: Manuscript 1 §2.4 says the RF was trained on "6 specimens"; the code (after review fix Q-03) trains on 12 (3 per material). Other documents cite counts without stating which experiment version. | publications/MANUSCRIPT_1_separability.md:57 vs experiments/exp_A_baselines.py:30 | Automated claims checker (`scripts/check_claims.py`) that verifies counts/numbers in docs against result JSON; fix manuscript; every result JSON records n_train/n_test explicitly. (Lead) |
| FA-11 | High | Competitor comparison limited (no capability matrix, no patents). | docs/research/COMPETITOR_INTELLIGENCE.md | Exhaustive matrix + patent landscape + invention register (Competitive/IP stream). |
| FA-12 | High | Pricing ($12K/$25K/$4K/$40K) unverified; no interviews. | SCIENTIFIC_EVIDENCE §6 | New pricing hypotheses (pilot $2.5–5K, non-GLP study $8–15K, material characterisation $5–15K, academic $4–10K/yr, enterprise $30–75K/yr) with validation plan; all labelled hypothesis. (Commercial) |
| FA-13 | **Critical** | Product is a FastAPI server + browser UI; requires a terminal; not an installable desktop application. | osteoquant/api, web/static | PySide6 + VTK desktop workstation, PyInstaller packages for Windows/macOS/Linux, CI build matrix. (Desktop) |
| FA-14 | High | No segmentation editing beyond the web brush; no undo/redo; no oblique views; no volume rendering. | web/static/viewer.js | Desktop editing tools with compressed undo stack; region growing; interpolation. (Desktop) |
| FA-15 | High | Model selection uses Dice; the product sells *measurements* (graft volume, new-bone volume, BV/TV). Dice can be high while volume bias is large. | exp_B | Select/benchmark models on measurement error (absolute and relative volume error, bias, limits of agreement, ICC) with Dice secondary. (Science) |
| FA-16 | High | No separability/identifiability check at analysis time: the pipeline outputs a graft volume for any material even when the experiments show intensity-only separation is impossible. | pipeline.py | Separability advisor: per-material knowledge + measured intensity distributions + oracle-bound → supported / supported-with-day-0 / not supported; pipeline abstains and reports why. (Science, Product) |
| FA-17 | Medium | Single-seed models; no ensembles; no hyperparameter search; no variance across seeds reported. | models/registry.json | Multi-seed (≥3) training, small HP search, ensembles, report seed variance. (Science) |
| FA-18 | Medium | Test coverage unknown; no CI; no property-based, fuzz, mutation or destructive tests. | tests/ | QA stream: coverage targets 95% critical / 90% overall, hypothesis, fuzz, mutmut, CI matrix. (QA) |
| FA-19 | Low | Open low-severity security items S-15, S-16, S-20, S-21. | docs/security/REVIEW_RESPONSE.md | QA/security stream Gen-2 review. (QA) |
| FA-20 | Medium | 45 of 81 traceability rows are GAP (URS→test). | docs/quality/traceability_matrix.csv | Regenerate the matrix from tests after QA and desktop work; keep compliance language as "draft, no compliance claimed". (Lead) |
| FA-21 | Medium | Phantom v1 uses periodic textures by default (`periodic_texture=True`), simple spherical granules, uniform resorption, no scanner noise texture (only white noise). | phantom/generator.py | Phantom v2: correlated noise (NPS) and blur measured from real scans, fragmentation, displacement, non-uniform resorption, strut/irregular granules, ring/streak/beam hardening via projection model. (Science) |
| FA-22 | Medium | Projection-domain simulation (Mode B) uses skimage parallel-beam radon; cone-beam not modelled; TIGRE/ASTRA not evaluated. | phantom/ctsim.py | Investigate TIGRE/ASTRA availability (CPU builds); document decision. (Science) |
| FA-23 | Medium | U-Net CPU inference ≈49k voxels/s → ~34 min per 100 M voxels; no ONNX/quantised runtime evaluated. | exp_O_performance.json | Evaluate ONNX Runtime CPU, dynamic int8 quantisation, torch.compile, tiling; document CoreML/MPS as untested here. (Science/Perf) |
| FA-24 | Low | Ledgers required by the new mandate do not exist (task, architecture decisions, evidence ledger, model registry, benchmark scorecard, defect, review, risk, release readiness). | repo root | Created in Generation 0 (this commit). (Lead) |
| FA-25 | Medium | Endpoints not rigorously defined in one place (graft fraction of ROI vs of mineral; certain vs including uncertain voxels). | morphometry/core.py `*_fraction_of_certain` | `docs/science/ENDPOINT_DEFINITIONS.md` with formula, units, denominators, handling of uncertain voxels, supported-when conditions. (Science) |
| FA-26 | Medium | Dataset licence enforcement is documentary only; the training code does not refuse non-commercial data for commercial weights. | ml/train.py Case.licence field | Enforce licence policy in `train_model` (commercial weights require commercial-compatible data; record in model card). (Science) |
| FA-27 | Low | The day-18 ROI confidence was quoted with two different roundings in different documents. | SCIENTIFIC_EVIDENCE R10 vs EXPERIMENT_REGISTRY F | Claims checker (FA-10). |

## 4. Specific weaknesses named in the mandate — disposition

| Mandated topic | Finding | Status after Gen 0 |
|---|---|---|
| Synthetic-only transfer | FA-02 | Open → science campaign |
| No real 3-class validation | FA-01 | Open; mitigated by abstention design; requires physical data |
| Weak OOD | FA-03 | Open → ensembles/conformal |
| Shrink-in-place longitudinal | FA-04 | Open → phantom v2 longitudinal |
| Segmental ROI after bridging | FA-05 | Open |
| Estimated time savings | FA-06 | Open → relabel + instrumented measurement |
| Post-hoc morphometry convention | FA-07 | Open → pre-registration + held-out data |
| Small real n | FA-08 | Open → dataset round 2 |
| Immature histology | FA-09 | Re-scoped |
| Report/benchmark count inconsistencies | FA-10, FA-27 | Fix + automated checker |
| Limited competitor comparisons | FA-11 | In progress (competitive stream) |
| Unverified pricing | FA-12 | In progress (commercial stream) |

## 5. What the baseline got right (keep)
Bit-identical reproducibility (P); explicit exceptions instead of silent exclusions (report 1, segmental ROI);
hash-chained audit trail with review binding; safe model loading; honest labelling of synthetic vs real; corrected
oracle after review; morphometry exact on analytic objects.

## 6. Prioritised remediation order
1. FA-13/14 desktop application (largest product gap) — in progress in parallel.
2. FA-16 separability advisor + abstention, FA-15 measurement-based selection, FA-25 endpoint definitions.
3. FA-02 sim→real (phantom v2, domain randomisation, self-supervised pretraining), FA-17 multi-seed/ensembles.
4. FA-04/05 longitudinal v2 with displacement and registration-failure detection.
5. FA-03 OOD/failure detection and conformal intervals.
6. FA-10/27 claims checker and document fixes; FA-24 ledgers.
7. FA-18/19 QA and security; FA-20 traceability; FA-23 runtime performance.
8. FA-06/11/12 commercial evidence; FA-07/08 real data expansion.

## 7. Reproduction details
Original results are unchanged in `experiments/results/`; reproduction outputs and logs are in
`experiments/results_gen0_repro/`. The H/I reproduction retrained the real-data U-Net and the k=1 fine-tune into the shared
`models/` directory before the registry was made concurrency-safe (ARC-03); because training is deterministic the
retrained weights reproduce the original results exactly (table above). Future reproductions use `OQ_MODEL_DIR`.
