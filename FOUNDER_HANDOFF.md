# Founder Handoff — OsteoQuant (28 November 2026, end of Generation 2)

Written for you to act on. Every number comes from a file in this repository; SYNTHETIC results are labelled. Read §1,
§2 and §15 first. Nothing has been sent, bought, signed, submitted or incorporated. The repository is public (your
decision, `docs/ip/IP_STRATEGY.md`).

## 1. The situation in five sentences
1. OsteoQuant is now an offline desktop workstation (PySide6 + VTK) for preclinical micro-CT of bone-graft defects, with
   study management, editing with undo, two-person sign-off, a hash-chained audit trail with external anchors, offline
   licences (test keys only) and PDF/CSV reports.
2. Its scientific core is a **measurement-support advisor** (version 1.4.3) that decides, per scan, whether graft,
   new-bone and mineral volumes are identifiable before reporting them, and refuses otherwise.
3. In the final pre-registered held-out **simulation** (S1H3) no supported measurement failed, but coverage is low: new
   bone was never supported, total mineral only with sharp imaging, and for 58% of specimens no volume endpoint at all;
   with 9 phantom structures the evidence bounds the supported-failure rate only below 0.34 (`EXPERIMENT_REGISTRY.md`).
4. Nothing has been tested on real graft material; the advisor and the simulator share attenuation physics, so the
   simulation shows internal safety, not accuracy.
5. The next value comes from physical evidence (a phantom study) and ten customer conversations — not more software.

## 2. What exists and works (tested)
| Area | State | Evidence |
|---|---|---|
| Desktop app | Import (7 formats, slab-wise for large scans) → QC → linked 2D/3D views → editing with undo and audited revisions → background analysis → ROI acceptance → review and sign-off → reports | `tests/desktop/` (run in CI), `docs/desktop/USER_GUIDE.md` |
| Measurement support | Advisor 1.4.3 bound to its own threshold method; evaluated at read time (old results are "not assessed"); refused values never printed or used in statistics | `osteoquant/advisor/`, `docs/science/MEASUREMENT_SUPPORT.md` |
| Audit and integrity | Hash-chained trail; authority-bound role changes; one generation record per report; chain heads anchored outside the project and printed on reports; signatures disabled on an anchor mismatch | `tests/desktop/test_cycle3_fixes.py`, `osteoquant/desktop/anchors.py` |
| Tests and CI | 597 passed, 1 skipped (local, 2026-11-28); 90.8% line+branch coverage of the library (desktop UI excluded); CI green on Ubuntu, Windows and macOS × Python 3.12/3.13 since 2026-11-28 (earlier runs never passed) | `docs/qa/test_summary.json`, `.github/workflows/ci.yml` |
| Packaging | Linux one-folder bundle built once (27 Nov; predates advisor 1.3.1–1.4.3 — **rebuild before any use**); Windows/macOS never built | `packaging/`, `BLOCKERS.md` B-013/B-016 |
| Morphometry | Exact on analytic objects; Tb.Th ICC 0.983 vs Scanco IPL on 8 public cubes (convention chosen post hoc) | `experiments/results/exp_G_morphometry.json` |

## 3. What the experiments showed
* **Abstention works in simulation, at a high price** (SYNTHETIC). Held-out series: S1H (advisor 1.3.3) and S1H2 (1.4.0)
  found supported measurements that failed; each failure produced a rule tested on new data; S1H3 (1.4.1) had none.
  See the standard sentence in `EXPERIMENT_REGISTRY.md` and the per-material table in `docs/user/MATERIALS_AND_SUPPORT.md`.
* **New bone next to dense graft is not identifiable by intensity** at 20–40 µm voxels: every held-out run refused it.
* **Day-0 registration is fragile** under granule motion (naive footprint graft Dice 0.80 → 0.535 → 0.35 at 0/50/100 µm,
  SYNTHETIC) and registration QC cannot verify alignment along a featureless bone axis (L5). There is no desktop day-0
  workflow.
* **Synthetic → real** (REAL dog forelimb, 5 test scans): the synthetic model reaches Dice 0.377 zero-shot and 0.513 with
  2× upsampling; domain-randomised pretraining did not improve the zero-shot curve on the training scans; few-shot,
  self-supervised, ensemble/conformal and runtime results: §3a.
* **Morphometry** agrees with Scanco IPL on public cubes; graft-specific endpoints have no real reference yet.

### 3a. ML campaign (filled from the result files when the runs finish)
See `EXPERIMENT_REGISTRY.md` rows S2, S3, U1 and O2.

## 4. Assumptions that failed
* "Intensity can separate graft from new bone for common materials" — only for dense ceramics, and never for new bone next
  to them in held-out simulation.
* "Total mineral is always a safe fallback" — supported in 10% of held-out specimens (sharp imaging only).
* "A day-0 scan rescues separation" — only without granule motion, and not for remodelling bone-derived grafts.
* "Row-level confidence bounds are enough" — with 9 phantom structures the honest bound is 0.34, not 0.045.
* "CI is configured, so it works" — it had never passed until 28 November.

## 5. What is genuinely differentiated
A separability check that refuses unsupported numbers, explains why, and binds support to the method validated, plus a
reviewable, anchored audit trail in an offline desktop tool. Competitors (38 mapped, `docs/research/COMPETITOR_MATRIX.md`)
offer segmentation and reporting; none found offers material-aware abstention. The moat is evidence, which does not
exist yet.

## 6. What only physical work can answer (validation stages B–F, `validation/VALIDATION_PROGRAM.md`)
* Stage B/C: physical phantoms with known graft fractions and characterised materials on your scanner — tests the advisor's
  profiles, blur model and refusals against truth.
* Stage D: ex vivo specimens with histology — the first real three-class truth.
* None of this may start without your authorisation, a collaborator, and (for animal tissue) the owner's permission.

## 7. Founder decisions waiting for you
`FOUNDER_DECISIONS.md` lists them with options. The most urgent: IP (public disclosures on 27–28 November start one-year
US clocks; foreign rights need counsel now), whether any evaluation on customer data is offered before incorporation and
Gate 1, and how to position the product given the S1H3 coverage.

## 8. What to learn first
`founder/LEARNING_CURRICULUM.md` (seven concepts with self-tests): partial volume and blur, why new bone is not
identifiable next to dense graft, pre-registration and held-out tests, clustered data and confidence bounds, measurement
support versus accuracy, audit trails and their limits, and what GLP/Part 11 do and do not require.

## 9. Who to talk to (nothing has been sent)
Draft messages are in `outreach/`; no email address in this repository is fabricated, and none has been contacted. Start
with an imaging scientist with a phantom-capable micro-CT and a bone biologist with histomorphometry, then ten discovery
calls by segment (`business/PROSPECT_SEGMENTATION.md`).

## 10. Money
Nothing has been spent. The first spend worth considering is a small physical-phantom study (bill of materials in
`validation/BILL_OF_MATERIALS.csv`), only after you approve it. Pricing remains a set of hypotheses (pilot $2.5–5K,
non-GLP study $8–15K, material characterisation $5–15K, academic $4–10K/yr, enterprise $30–75K/yr).

## 11. How to demonstrate it
`founder/DEMO_SCRIPT.md` (10 minutes, synthetic demo project). Show a refusal first: it is the product. Sample reports in
`reports_samples/` are watermarked and SYNTHETIC.

## 12. How to resume engineering
`EXECUTION_STATE.md` ("How to resume"); `RELEASE_READINESS.md` for gates (Gate 1 not met: Windows/macOS builds, rebuilt
Linux bundle; Gate 2 not met: no real-data validation; Gate 3 never self-declared); `BLOCKERS.md`.

## 13. Reviews
Three review cycles across twelve perspectives by **automated reviewer agents** (not human experts):
`REVIEW_REGISTRY.md`, `docs/reviews/`. Cycle 3 found two critical science issues (unspecified material; API edits) and
three high product issues; all are fixed or mitigated with tests, and the open items are listed in the response files.
Human expert review remains an open action for you.

## 14. Honest bottom line
The software is serious and its refusals are trustworthy in simulation; its usefulness on real grafts is unknown and,
by its own held-out evidence, narrow. A company built on it should sell a separability assessment and audited reporting
to a small niche first, and earn any broader claim with physical evidence.

## 15. Next actions
1. Decide the IP questions with counsel (dates in `FOUNDER_DECISIONS.md`).
2. Approve or decline a physical phantom study (stage B) and identify the collaborator.
3. Hold ten discovery conversations before any further product work.
4. Run the `desktop-build` workflow by manual dispatch when you accept public artefacts (B-013), then test on your own
   Windows/Mac machines.
5. Commission human expert review of the advisor rules.
