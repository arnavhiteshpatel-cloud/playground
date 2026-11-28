# Release notes — Generation 2 (compared with Generation 1)

> **Status.** Research product: not validated on real graft materials; not a medical device; no GLP/Part 11
> compliance claimed. The application version is still **0.1.0**; Generation 2 is a development generation, not a
> numbered release, and no release gate is met ([RELEASE_READINESS.md](../../RELEASE_READINESS.md)).

**Baseline.** "Generation 1" here means the product audited in [FORENSIC_AUDIT.md](../../FORENSIC_AUDIT.md), which
calls it the *Generation-0 baseline* (git commit `ee09a70`, 27 November 2026): a FastAPI server with a browser
workbench, the analysis library, 16 experiments (A–P) and 61 tests. Audit findings are cited as FA-NN; tasks as T-NN
from [TASK_REGISTRY.md](../../TASK_REGISTRY.md).

## Summary

* A native **desktop application** replaces the local server and browser as the primary interface.
* The software now **refuses to report** graft and new-bone endpoints it cannot support, through a
  **measurement-support advisor** (version 1.4.3), and reports say why. Support is bound to the advisor's own
  threshold method, now the default segmentation.
* Endpoints, analysis conventions and acceptance criteria are written down and pre-registered.
* New longitudinal tools (granule tracking, registration QC, ROI propagation) and an ONNX runtime path.
* Offline licensing, packaging for three operating systems, a second security review and a larger test suite.
* Commercial claims were corrected: the time-saving figure is now labelled an assumption-derived model output, and
  pricing is restated as hypotheses.

## New

### Desktop application (FA-13, FA-14; T3.1)
* PySide6 (Qt 6) + VTK workstation calling the library in-process: no server, browser or network.
* Projects as folders; per-project users, roles and sign-in; study tree (study, group, animal, timepoint, scan).
* Four-step import wizard with mandatory voxel-spacing confirmation, SHA-256 provenance, duplicate detection,
  slab-by-slab import of large volumes, and a list of rejected imports with reasons.
* QC display separating deterministic from heuristic checks.
* Orthogonal and oblique views, 3D surfaces and volume rendering, light and dark themes.
* Editing tools that the web viewer lacked: brush and eraser in µm (2D/3D), region growing, hole filling, slice
  interpolation, exact undo/redo (500 operations), save as a new revision with a mandatory reason.
* Background jobs with progress and cancellation; Results tab with a per-endpoint **Support** column and CSV export;
  report preview, export and sign-off; audit-trail viewer with chain verification; blinded review mode.
* Opt-in, local-only workflow timing for future timed user studies (FA-06).
* `--selftest` end-to-end check (8 steps).

### Measurement support and abstention (FA-16; ADR-G2-04; T1.7)
* `osteoquant/advisor/`: per-endpoint status *supported*, *supported with conditions* or *not supported*, with
  mechanism and reason, computed from the material, the scan's noise and grey levels, and day-0 information.
* Pipeline produces `reported_metrics` in which unsupported endpoints are blank; raw values stay in the audit record.
  Study bundles, PDF and CSV reports use the reported view and list every suppressed endpoint (review STAT-01).
* Version history: 1.1.0 (single-threshold decision rule; support at the estimated graft share and half of it;
  metals refused; ≥500-voxel reference samples; bone-derived rule cannot be bypassed; computed day-0 fields required),
  1.2.0 (new bone versus soft tissue with partial-volume halos gates mineral and new-bone endpoints), 1.2.1 (DBM
  new-bone endpoints refused), 1.3.0 (knowledge-base material profiles cross-checked against the physics model; a
  >25% disagreement requires a measured reference; resorbable materials intensity-supported only at a known
  timepoint ≤4 weeks), 1.3.1 (scan-versus-profile consistency check, >15%), 1.3.2 (graft-adjacent partial-volume
  mixing for measured control references), 1.3.3 (bone-derived grafts not supported by the day-0 mechanism), 1.4.0
  (blur, granule thickness and graft level measured in the scan; new-bone error propagation; ambiguous graft rim),
  1.4.1 (rim width scaled to the measured blur), 1.4.2 (metals refuse total mineral; BCP treated as resorbable; DBBM
  allowed the day-0 mechanism; scan noise added to measured references; support bound to the segmentation method),
  1.4.3 (shipped: unspecified-material rim proxy; worst-case mineral rim gate; measured-reference noise and partial
  volume; day-0 limits for resorbable materials; support re-evaluated when results are shown or reported).
* The desktop has no day-0 workflow, so the day-0 rules above apply only to the analysis library.
* The desktop passes each scan's time since implantation to the advisor (from the timepoint's days or a label such as
  "Week 4"; or entered in the analysis dialog; otherwise unknown) and the report prints it with its source.
* Studies carry a data class (synthetic, public, own research, customer) chosen at creation; synthetic demo studies
  are labelled SYNTHETIC DATA in reports (previously printed as customer data).
* Report fixes: group confidence intervals clipped to the physical range and marked; no interval for n <3; specimens
  without a group excluded from group statistics; all endpoints printed; multi-Otsu thresholds printed; research-use
  line in every page footer; CSV header comment with data class and units; approving signature role renamed
  "Customer approver".
* Machine-readable materials knowledge base (`osteoquant/knowledge/materials.json`, 16 materials, with evidence tags
  and an unsupported-material workflow) (T1.2).
* Material characterisation from a material-only or day-0 scan (`osteoquant/advisor/characterize.py`), library only.

### Science documentation (FA-07, FA-09, FA-25; T1.9, T1.14)
* [ENDPOINT_DEFINITIONS.md](../science/ENDPOINT_DEFINITIONS.md): formula, unit, denominator, treatment of uncertain
  voxels and reporting condition for every endpoint, plus a glossary of accuracy thresholds.
* [PREREGISTRATION.md](../science/PREREGISTRATION.md): frozen morphometry conventions (`edge` primary) and acceptance
  criteria, with a deviations log.
* [HISTOLOGY_SCOPE.md](../science/HISTOLOGY_SCOPE.md): histology re-scoped as complementary; H&E bone-area fraction
  removed from reports.

### Longitudinal and ROI (FA-04, FA-05; T1.6, T1.11)
* Phantom generator v2 with granule displacement, fragmentation and non-uniform resorption.
* Granule tracking; registration QC based on block-wise residual displacement (≤2 voxels) instead of host-mineral Dice;
  ROI propagation from an earlier timepoint with the defect excluded from registration. Library only; no desktop
  workflow yet.

### Runtime and models (FA-23, FA-26; T1.10, T1.13)
* ONNX Runtime inference path (`onnx:<name>`), so PyTorch is not needed to run a model. The full benchmark (O2,
  SYNTHETIC, 16 specimens) found it about as fast as PyTorch (688k vs 769k voxels/s on 4 busy CPU threads; an earlier
  single-specimen spot check suggesting 8× was wrong), with ≥98% label agreement and the same volume error.
* Model registry with locked atomic writes, provenance and licence inheritance for fine-tuned models, and code
  version in checkpoints; training refuses research-only data for commercial-eligible weights.
* A learned model may support graft endpoints only with material-specific validation records (none exist).

### Licensing and packaging (ADR-G2-03, ADR-G2-06; T3.2, T3.3)
* Offline Ed25519-signed licence files, evaluation mode with watermarked reports, machine binding, test-licence tool.
  Only a published test key exists; no production key.
* PyInstaller one-folder builds; a CI build workflow for Windows x64, macOS 14 arm64 and Ubuntu 22.04. It creates no
  GitHub Release, but on a manual dispatch or a `desktop-v*` tag it uploads unsigned application archives as workflow
  artifacts that any signed-in GitHub user can download from this public repository, so starting it is a distribution
  decision for the founder (B-013). It has never run. Signing and notarisation steps are present but inactive until the
  publisher's credentials exist.
* The only packaged build is a local Linux build of 28 November 2026 (advisor 1.4.3); it passed its packaged
  self-test and licence check and is not distributed.

### Quality, security and evidence (FA-10, FA-18, FA-19, FA-27; T4.1–T4.3)
* Second security review: 20 findings; the conditional critical (pickle codec in uploaded Zarr stores), four medium and
  seven low findings fixed with regression tests; three assigned and three open (all low)
  ([SECURITY_REVIEW_GEN2.md](../security/SECURITY_REVIEW_GEN2.md)).
* Tests: from 61 tests (Generation 1) to the current suite, including property-based, fuzz and destructive tests.
  Current counts and coverage come from one file, [`docs/qa/test_summary.json`](../qa/test_summary.json): 636 passed,
  1 skipped; 93.4% line+branch coverage (98.7% on critical modules) with the desktop UI code excluded (local full run,
  28 November 2026). Earlier
  figures quoted elsewhere are superseded. CI passed for the first time on 28 November 2026.
* Claims checker (`scripts/check_claims.py`) comparing numbers in documents with result files.
* New ledgers: task, architecture decisions, evidence, model, benchmark scorecard, defect, review, risk and release
  readiness (FA-24).
* Cycle-1 adversarial reviews (imaging, statistics, ML, architecture; biology/CRO/quality; investor/IP) with
  documented responses.

### Commercial and research (FA-06, FA-11, FA-12)
* "≈78% analyst time saving" relabelled everywhere as an assumption-derived model output (EVIDENCE_LEDGER G2-002).
* Pricing restated as hypotheses (pilot $2.5–5K, non-GLP study $8–15K, material characterisation $5–15K, academic
  $4–10K/yr, enterprise $30–75K/yr); the $25K GLP-study offering removed.
* Competitor capability matrix (38 competitors × 40 dimensions, evidence-tagged), patent landscape, invention register.
* Validation programme with stages A–F.

## Changed behaviour

| Area | Generation 1 | Generation 2 |
|---|---|---|
| Graft and new-bone volumes | Reported for every material | Reported only when the advisor supports them; otherwise "not measured" with the reason |
| Primary user interface | Local web server and browser | Desktop application (web API kept as an optional interface) |
| Morphometry border convention | `edge`, chosen after seeing the reference data | `edge` pre-registered as primary; `background` also reported |
| Registration QC | Host-mineral Dice | Block-wise residual displacement ≤2 voxels |
| Mineral threshold (advisor-threshold method) | Global Otsu | Relative threshold from the advisor's mineral rule (default 0.30) |
| Signature re-authentication (web API) | Unlimited password attempts | Shares the sign-in lockout |
| Reports | No licence watermark | Evaluation or test-licence watermark when not licensed |

## Generation-2 experiments

| ID | Data | Status | Key result |
|---|---|---|---|
| S1H4 | Synthetic, pre-registered, held out (shipped advisor) | Done | In the pre-registered held-out simulation S1H4 (advisor 1.4.3; 720 synthetic specimens from 36 phantom structures, knowledge-base and Unspecified material paths; a failure is a volume error above 20%): residual graft volume supported in 10% of specimens (HA only), every failing measurement refused and none of the supported ones failed (95% upper bound on the supported-failure rate 0.14 counting phantom structures as the unit; 0.052 if the 69 supported measurements were independent); supported graft volumes: median error 2.2%, maximum 11.4%; total mineral volume supported in 2% of specimens (β-TCP at PSF 40 µm only); supported mineral volumes: maximum error 16.9%; new-bone volume never supported; no volume endpoint supported for 89% of specimens. An earlier held-out test of advisor 1.4.1 (S1H3, 9 phantom structures) is recorded in the experiment registry. |
| S1H, S1H2, S1H3 | Synthetic, pre-registered, held out | Done | Earlier versions (1.3.3, 1.4.0) supported some measurements that failed; the fixes were tested on S1H3 (1.4.1: no supported failure, structure-level bound 0.34) |
| F2 | Synthetic | Done | Propagated segmental ROI Dice 0.984 (minimum 0.963), registration QC passed 16/16; the Gen-1 failure mode was not reproduced |
| L3 | Synthetic | Done | Day-0 is fragile under granule motion: naive day-0 footprint graft Dice — no motion: 0.80; 50 µm motion: 0.535; 100 µm motion: 0.35. The advisor refuses these cases |
| L4 | Synthetic | Done | Registration QC flagged all 6 harmful misalignments and passed 78% of harmless ones |
| S2 | Real | Part a done; parts b and c running | Part a only; no number from b or c |
| U1, O2 | Synthetic | Queued | — |

Details: [SCIENTIFIC_METHODS.md](SCIENTIFIC_METHODS.md), [EXPERIMENT_REGISTRY.md](../../EXPERIMENT_REGISTRY.md).

## Known issues and open items

* **No real three-class validation** (FA-01) and a large synthetic-to-real gap (FA-02) remain open.
* Out-of-distribution detection is still weak (FA-03); ensembles and conformal intervals not complete.
* Segmental ROI after bridging remains an open defect (DF-004).
* Day-0 method fails under small granule motion in simulation; bone formed inside a resorbing footprint is counted as graft.
* Desktop: no day-0 or characterisation workflow; no locked model installed by default (ONNX inference no longer
  needs PyTorch); histology not included. Users are managed under *Project > Users...*.
* Windows and macOS builds never run; the only Linux build predates the current code and must be rebuilt; no build is
  signed or notarised.
* Traceability matrix not regenerated (FA-20). Coverage in the local run recorded in `docs/qa/test_summary.json`:
  93.4% overall and 98.7% on critical modules.
