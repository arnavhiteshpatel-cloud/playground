# Review cycle 3: science (bone biology, micro-CT imaging, ML / computer vision, biostatistics)

This review was produced by an automated reviewer agent, not by a qualified human expert.

- **Date:** 2026-11-28 (about 00:50–01:40 UTC).
- **Commit reviewed:** `4b28a5a` (`git rev-parse --short HEAD` at the start), branch as checked out. Code line numbers
  refer to this commit.
- **The tree moved during the review.**
  - Commits dce5f71…b55c459 (00:50–01:05) changed `EXPERIMENT_REGISTRY.md`, `DEFECT_REGISTRY.md`,
    `BENCHMARK_SCORECARD.md`, and the truth-table hunk of `report/defectfill.py`. For these files I read and cite the
    later version (b55c459).
  - From about 01:30, uncommitted edits appeared in `pipeline.py`, `advisor/integration.py` and
    `ml/validation_records.py`: read-time binding, a downgrade for corrected revisions, and a boolean validation flag.
    They appear to answer a parallel product review. **They are not reviewed here.** They may address parts of
    C3-SCI-03 and C3-SCI-16 and should be verified in the next cycle.
- **Scope:**
  - the cycle-2 science dispositions (`docs/reviews/cycle2/RESPONSE_SCIENCE.md`, C2-SCI-01…23);
  - advisor 1.4.0 → 1.4.2 (`osteoquant/advisor/`, `docs/science/MEASUREMENT_SUPPORT.md`);
  - method binding (`pipeline.bind_support_to_method`) and every path that renders support (desktop, report, web API,
    bundle);
  - held-out validations S1H2 and S1H3, their pre-registration and git history;
  - `registration_qc` and the L4 and F2 re-runs;
  - group statistics in `report/defectfill.py`;
  - customer-facing science text and `scripts/check_claims.py`;
  - `EXPERIMENT_REGISTRY.md` and `DEFECT_REGISTRY.md`;
  - S2 part a.
- **Method.** This was a read-only review. I wrote only this file; all scratch scripts live outside the repository.
  Each Python check took under about 1 CPU-minute, except the probe in C3-SCI-01, which was about 2 CPU-minutes run
  at `nice 10`. No experiment was re-run, nothing was trained, and the full test suite was not run. What I ran:
  - `git log` and `git diff` on the pre-registration, the held-out scripts, the result files and the advisor
    (7a3ae70 → HEAD);
  - recounts from `exp_S1H2_heldout.json`, `exp_S1H3_heldout.json` and `exp_S2v2_sim2real_a.json`, including a
    clustering analysis (ICC, design effect);
  - `python3 scripts/material_support_table.py`, diffed by hand against `docs/user/MATERIALS_AND_SUPPORT.md`;
  - `python3 scripts/check_claims.py`, plus a scratch document fed to `check_claims.main([...])`;
  - `pytest` on two single tests: `test_pipeline_binds_support_to_method` and
    `test_group_stats_ignore_refused_values_and_uncomputable_tests` (both pass);
  - probes in scratch scripts:
    - (P1) measured-reference paths of `mineral_rule` and `intensity_separability`;
    - (P2) a voxel-level check of the resulting mineral threshold;
    - (P3) `estimate_blur` against known blur on a supersampled tube phantom at noise_rel 0.05/0.15/0.30;
    - (P4) `registration_qc` at identity and under 2–10-voxel shifts per axis, on segmental, calvarial and condyle
      phantoms;
    - (P5) the per-material and day-0 rules;
    - (P6) S1H3-generator phantoms with new seeds at higher noise;
    - (P7) S1H3-generator phantoms with new seeds 4900/4910/4920 analysed three ways: "Unspecified" material, a
      characterised profile, and `ha` at 2 weeks;
    - (P8) the planar edge model against a blurred sphere;
    - (P9) reproduction of two S1H3 rows under advisor 1.4.2.
  - Seeds 4900–4920 are not in any pre-registered set. They were used only to probe; nothing was tuned on them.

**Severity scale.**
- **Critical:** a confident, wrong customer-facing number, or a supported measurement that can fail silently.
- **High:** wrong science, or a validation flaw that changes a conclusion.
- **Medium:** a bias, design weakness or documentation error to fix before real data or before any wider claim.
- **Low:** consistency or maintenance.

## Headline

1. **The default desktop configuration can report wrong total-mineral values as "supported" (C3-SCI-01).**
   - The default is the advisor threshold method with graft material *Unspecified*, the first item in the menu and
     the documented choice for materials that are not listed.
   - The 1.4.1 ambiguous-rim gate, which fixed the S1H2 total-mineral failures, runs only when a graft threshold
     exists. For *Unspecified* there is none.
   - On 36 new phantoms (S1H3 generator), total mineral was supported in 36/36 and wrong by +21% to +38% in 11.
   - The same specimens with a characterised or knowledge-base profile were refused.
2. **Refused values reach a report as plain numbers through the web API (C3-SCI-02).**
   - A label edit through the API stores a measurement with no support record.
   - The API report then prints refused graft and new-bone values as plain numbers, which is how the report shows
     supported values.
   - The API default method is still multi-Otsu, and `advisor_threshold` cannot be selected through the API at all.
3. **The headline held-out bound counts correlated rows as independent (C3-SCI-05).**
   - The bound is "0/80 supported failures, 95% upper bound 0.045". The 80 rows come from only 9 structures
     (ICC 0.31), and the pre-registration names structures as the unit of replication.
   - With a design effect, the bound is about 0.15. With structures as the unit, it is 0.34.
   - "Residual graft passes the full criterion" is therefore not demonstrated.
4. **The aperture-aware registration QC cannot see axial misregistration in segmental defects (C3-SCI-04).**
   - A 400 µm shift along the bone axis passes QC, although phase correlation measured it.
   - The customer document says such shifts are "reported as unverifiable instead of passed".
5. **The pre-registration was not honoured on two points (C3-SCI-06).** The S1H3 numbers themselves are verified.
   - §9 declared 1.4.1 "the last advisor change of Generation 2". Advisor 1.4.2 was committed in the same commit as
     the S1H3 results, with no deviations-log entry.
   - The C2-SCI-16 acceptance amendment was written after S1H2 and S1H3 were known and then used to call S1H3 total
     mineral (0/22, bound 0.154) a pass.
   - The claim that 1.4.2 differs from 1.4.1 only on paths S1H3 does not exercise is **verified**: by the code diff,
     and by reproducing two S1H3 rows to six decimals under 1.4.2.

## (a) Verification of the cycle-2 dispositions (C2-SCI-01…23)

| ID | Claimed status | Verdict | Evidence |
|---|---|---|---|
| C2-SCI-01 | addressed | **partly agree** | The 2026-11-28 registry entry labels S1b and S1c as development (`EXPERIMENT_REGISTRY.md:61`). The S1b row still has the status "Done — advisor 1.3.3 (authoritative)" and the bold in-sample result "Every endpoint, both parts: 0 supported-but-failed" (`:45`). The L3 row still reports "all 60 failures refused, 0 supported-but-failed" for tracker v2, which was tuned on the same seeds, with no in-sample label (`:48`). `MEASUREMENT_SUPPORT.md:3` still reads "Validation: Experiments S1, S1b, S1c". No deviations-log rows exist for the post-inspection rules 1.2.0–1.4.2 (`PREREGISTRATION.md:89-98`). |
| C2-SCI-02 | fixed | **disagree (partial fix)** | Verified: `pipeline.py:189-196,208-225` binds support to `advisor_threshold`, `ANALYSIS_DEFAULTS` is `advisor_threshold` (`desktop/services.py:481`), and `test_pipeline_binds_support_to_method` passes. Not fixed: (1) the API default is still `multiotsu`, and the regex does not admit `advisor_threshold` (`api/app.py:133`); (2) the API label-edit path saves no support, so the API report prints raw refused values unmarked (C3-SCI-02); (3) desktop label revisions copy "supported" onto hand-edited labels (`services.py:717-723`, C3-SCI-03); (4) binding is applied only when a result is written, so records stored before 1.4.2 are never re-bound; (5) the method-binding text in `MATERIALS_AND_SUPPORT.md` says only graft and new-bone endpoints are refused, but the code refuses total mineral too. |
| C2-SCI-03 | fixed | **agree** | `pipeline.py:189-194` sets `day0 = None` and records why. A grep finds no product caller of `registration_qc`, `track_granules`, `day0_propagation` or `propagate_roi` outside `longitudinal/` and `experiments/`. `support_for_scan` still accepts a free `day0` dict for library callers; that is acceptable because no product path supplies one. |
| C2-SCI-04 | fixed | **disagree** | The projection removes the false alarms at identity (P4: 0–0.3 µm on all three models at σ 40/250). It also removes **true** axial shifts. Segmental, σ 80: shifts of 160, 240 and 400 µm along the bone axis all pass. The constrained maximum is 0.4–2.8 µm, while the raw block shifts were up to 280 µm. `pass` ignores `partially_unverifiable` (`longitudinal/core.py:225-226`). No test or result file contains the response's evidence ("perfect alignment passes on segmental, condyle and calvarial at σ 40/80/250; a 170 µm shift is caught in all"). It holds only for transverse shifts. L4 was re-run with the same design (condyle, σ 80, `exp_L4_registration_qc.py:20-27`), not the extended one requested in C2-SCI-21. In F2, 3/16 cases pass at exactly the 80 µm tolerance. The rounding fix was made after F2 v2 had failed and was then re-run on the same data. See C3-SCI-04. |
| C2-SCI-05 | partly addressed | **agree** | The status is stated accurately. The tolerance is still a constant (`separability.py:52`). |
| C2-SCI-06 | open (disclosed) | **agree** | Disclosed in `MEASUREMENT_SUPPORT.md:83-84`. Control references were always optional, so "optional, not the default" is not a mitigation. |
| C2-SCI-07 | partly addressed | **agree, with an additional defect** | "Partly" is correct: `mineral_rule` accepts `blur_sigma_vox` and never uses it (`separability.py:645-690`). The blur estimator is **not** conservative under noise. In P3, at noise_rel 0.30 a true total σ of about 1.28 voxels is reported as 0.80 after calibration. The calibration has no script or result in the repository: it exists only as the comment at `integration.py:262`. S1H3 never recorded the estimate: `blur_est` is `None` in all 216 rows (`exp_S1H3_heldout.py:62` reads a key that does not exist). See C3-SCI-08. |
| C2-SCI-08 | partly fixed | **partly agree** | Noise is added in `intensity_separability` (`separability.py:253-256`). It is **not** added in `mineral_rule`, which uses the new-bone samples as they are (`:674`). In P1, at noise_rel 0.30 the mineral rule passes with a low-noise control reference (Dice 0.931, predicted ratio 1.024); a voxel simulation of that threshold gives a measured/true ratio of 0.767. The customer document says the noise is "added to all measured samples" (`MATERIALS_AND_SUPPORT.md:170`). `compatible_with` is still not enforced. See C3-SCI-07. |
| C2-SCI-09 | fixed | **agree (declared metals)** | `separability.py:450-455`; titanium and magnesium are "- / - / -" in the table script's output. The second half of the recommendation is not done and not mentioned: pass QC-H08 (fixation hardware next to a ceramic graft) to the advisor. |
| C2-SCI-10 | fixed | **partly agree** | DBBM may now use the day-0 mechanism (`separability.py:549`). None of the recommended conditions were added: negligible DBBM resorption assumed and verified by histology, a timepoint limit from knowledge-base kinetics, and the intragranular-porosity caveat. In P5, DBBM with day-0 at 52 weeks is conditional with only three generic conditions. The comment at `:550` still lists DBBM among the remodelling grafts. |
| C2-SCI-11 | fixed | **disagree (1 of 4 parts)** | (a) BCP was added to `RESORBABLE_EARLY_ONLY` but not to the day-0 `resorbable` list (`separability.py:538`). In P5, BCP with day-0 at 52 weeks is conditional **without** the creeping-substitution condition, while β-TCP has it. (b) The day-0 path still has no timepoint limit. (c) S53P4 still bypasses the knowledge-base/physics cross-check and is supported at 2 weeks (table script: "S / S / S"). (d) The ≤4-week rule is still not tied to species or kinetics. |
| C2-SCI-12 | accepted | **agree** | No change; the limitation is disclosed. |
| C2-SCI-13 | accepted (disclosed) | **agree, but see C3-SCI-11** | Per-endpoint "n=k of N" is printed (`defectfill.py:329`). The "trace residual graft" rule makes missingness depend on the value itself, by construction, and the report gives no warning. |
| C2-SCI-14 | fixed | **partly agree** | Verified: (a) per-endpoint n, (c) comparisons on measured values only, and (d) Holm over computable tests (`defectfill.py:153-174,329`); the cited test passes. (b) Group cells still carry no "(c)" marker when they contain conditional values. |
| C2-SCI-15 | fixed | **partly agree** | Only (a) was fixed (`exp_S1_advisor.py:75,90`). (b) The field is still called `upper95`. (c)–(e) are unchanged. The legacy `abs_err_new_supported_*` and `abs_err_mineral_supported_*` fields are still computed over *graft*-supported rows: S1H3 stores `abs_err_new_supported_max` 0.638 and `abs_err_mineral_supported_max` 0.393, for endpoints that were refused in those rows. |
| C2-SCI-16 | accepted (amend for future) | **disagree** | The amendment ("point failure rate ≤10% regardless of n") is weaker than the recommendation, which was a "not demonstrable" verdict when n_supported < 36, per-stratum criteria and a tolerance bound. Under it, 0 failures among 3 supported cases passes. It was written after S1H2 and S1H3 were known, and immediately applied to declare "S1H3 … mineral (0/22) pass" (`PREREGISTRATION.md:98`), although the CP bound is 0.154. See C3-SCI-06. |
| C2-SCI-17 | accepted (disclosed) | **disagree with the implied remedy** | The held-out headline is still a row-level CP bound: 0.045 over 80 rows from 9 structures; signed-error ICC 0.31, design effect 3.5, effective n ≈ 23, bound ≈ 0.147. The "bootstrap over structures" returns [0, 0] whenever there are zero failures (`exp_S1H3_heldout.json`, `bootstrap_by_structure`), so it bounds nothing. See C3-SCI-05. |
| C2-SCI-18 | accepted | **disagree** | No held-out run exercises the product's knowledge-base path. Every S1H* run passes a custom `MaterialProfile` with the exact value rel_mean = X/1075 (`exp_S1H3_heldout.py:51`): no `healing_weeks`, no knowledge-base cross-check, no "Unspecified". The default "Unspecified" path fails (C3-SCI-01). |
| C2-SCI-19 | fixed (text) | **agree** | The qualification is at `EXPERIMENT_REGISTRY.md:48`. The same row still quotes "Registration QC: 100% … passed" from the superseded QC, and the tracker-v2 count without an in-sample label. |
| C2-SCI-20 | open | **agree** | Unchanged (`longitudinal/core.py:235-`). |
| C2-SCI-21 | open | **agree** | Unchanged. The L4 re-run did not extend the design: still condyle only, σ 80, no strut granules, no axial translations. |
| C2-SCI-22 | fixed | **disagree** | `save_result` still records no git SHA, dirty flag or module hash (`experiments/common.py:37-42`). The deviations log has no rows for 1.2.0–1.4.2. `MEASUREMENT_SUPPORT.md:3` still names S1, S1b and S1c as the validation. |
| C2-SCI-23 | addressed | **disagree** | S1H3 keeps the advisor's structural assumptions: Gaussian PSF (`psf_sigma_um`), an exact material profile, the same host anchor, one HA-like material, one healing stage, and smoothed white noise. Strut-like calvarial granules were already in S1H (120–250 µm, roughness 0.6), which was development data for 1.4.0. Only 7/80 graft-supported S1H3 rows are strut-like. None of the structural factors proposed in C2 §(c) was varied. The blur calibration range (PSF 10–60 µm, `integration.py:262`) also brackets S1H3's PSFs. |

## (b) New findings

### C3-SCI-01 — Critical — Unspecified material: total mineral supported with +21…+38% error (S1H2 failure mode reintroduced)

- **Location:**
  - `advisor/integration.py:56-73`: the rim is computed only `if g.any()`, and `g` needs a graft threshold;
  - `advisor/separability.py:422-427`: an unknown or unspecified material returns before any intensity model is
    built, so there is no threshold;
  - `separability.py:730-746`: the rim gate is skipped when `rim_fraction_new is None`;
  - `desktop/dialogs.py:191`: "Unspecified" is the first and default item;
  - `MATERIALS_AND_SUPPORT.md`, row *Unspecified*: "Can measure: Total mineral".
- **Evidence (P7).**
  - Setup: three new structures (condyle 4900, segmental 4910, calvarial 4920), S1H3 generator settings, X
    1900/3000 mgHA/cm³, PSF 15/35/50 µm, correlated noise σ 40/70, `advisor_threshold` method.
  - **"Unspecified"** (`material=None`): total mineral was **supported in 36/36** specimens and was wrong by more
    than 20% in **11**: +21.4%, +21.8%, +27.9%, +29.4%, +37.6%, +38.1% (condyle); +21.4%, +30.2%, +33.1%
    (segmental); +28.2%, +31.2% (calvarial). All 11 were at PSF 35–50 µm (σ ≈ 0.9–1.25 voxel).
  - **Characterised profile** and **`ha` at 2 weeks**, same specimens: 0 supported failures. The rim gate refused
    them, with half-rim fractions of 0.18–0.37 against a limit of 0.10.
  - The halo model in `mineral_rule` under-represents blur (C2-SCI-07), and nothing else checks the halo.
  - The outcome is a "supported" Mineralised % on the desktop and a plain "Total mineral volume" value in the PDF.
- **Fix.**
  - When no graft model exists but graft-like voxels do (`bright.size ≥ 200` in `_assess_scan`), compute the rim
    around `bright_mask` and apply the same rim gate. Otherwise, refuse the mineral endpoints for
    unspecified/unknown materials whenever voxels brighter than host bone are present.
  - Add regression tests that use these phantoms.
  - Add an "Unspecified" arm, and a knowledge-base-material arm, to the next held-out validation.
  - Until fixed, change the table row and the "choose Unspecified" advice.

### C3-SCI-02 — Critical (web API path) — refused values printed as plain numbers in API reports

- **Location:**
  - `api/app.py:460`: the edit endpoint saves `{"metrics", "corrected_from", "config"}` with no
    `measurement_support` and no `reported_metrics`;
  - `api/bundle.py:116`: `metrics = res.get("reported_metrics", res.get("metrics"))`;
  - `report/defectfill.py:190-195`: `_support` returns `None` when no support record exists;
  - `defectfill.py:202-206`: `_fmt_support(v, None)` prints the plain value;
  - `study/handlers.py:73-89`: `job_report` has no `_enforce_support` step (the desktop has one,
    `desktop/services.py:1120`);
  - `api/app.py:133`: default `multiotsu`; `advisor_threshold` is not allowed.
- **Evidence.**
  - Through the API, analysis always runs multi-Otsu or a U-Net, so binding refuses every tissue endpoint.
  - Any brush edit then creates a "corrected" measurement with no support record. The API report uses it, because
    it is the latest measurement per scan (`study/db.py:616-620`).
  - Check run: `_support(spec, 'class_volumes.residual_graft_fraction')` returned `None` and `_fmt_support(0.212, None)`
    returned `"0.212"`. That is the rendering of a supported value: supported prints plain, conditional prints
    "(c)", refused prints "n/m".
  - The values also enter the group means and the comparisons.
- **Fix.**
  - In `defectfill` (and `bundle_from_store`), treat a missing support record as "not assessed" and print "n/m". This
    is fail-closed and is what the desktop already does.
  - In the API edit endpoint, copy the base support, apply the correction rule (C3-SCI-03) and store
    `reported_metrics`.
  - Admit `advisor_threshold` in the API and make it the default.
  - Add an API-level test: analyse, edit, report, and assert that no refused endpoint prints a number.

### C3-SCI-03 — Medium — desktop label revisions keep "supported" status on hand-edited labels

- **Location:** `desktop/services.py:717-723` ("support depends on image, ROI and config (not on the labels): carry
  it over"); `pipeline.py:208-225` (binding runs only inside `analyze`).
- **Evidence.**
  - The support claim was validated for **unedited** `advisor_threshold` labels (S1H*).
  - After a manual revision, the advisor's "supported" status and mechanism "intensity" are copied unchanged, and the
    revision is stored with `method=base["method"]`. The desktop and report then show "supported" for labels that the
    validation never covered.
  - The audit trail does list the edit, so the change is not silent. That is why this is Medium.
  - Separately, binding runs only when a result is written. Measurements stored before 1.4.2 with multi-Otsu keep
    their "supported" status on screen and in reports.
- **Fix.**
  - For corrected versions, downgrade supported endpoints to "supported with conditions", with the condition "labels
    manually corrected; support was validated for unedited advisor-threshold labels". Alternatively, re-run
    `bind_support_to_method` with `method="corrected"`.
  - Enforce binding at read time in `desktop/support.py` and `defectfill`, using the stored segmentation method, so
    legacy records are covered.

### C3-SCI-04 — High — registration QC passes axial misregistration in segmental defects; the customer text says the opposite

- **Location:**
  - `longitudinal/core.py:210-226`: structure-tensor projection, `ok = max_shift ≤ tol`, and
    `partially_unverifiable` is informational only;
  - `docs/user/SCIENTIFIC_METHODS.md:224-228`: "along the axis of a diaphyseal tube a shift cannot be seen, and is
    reported as unverifiable instead of passed";
  - `DEFECT_REGISTRY.md` DF-016 and DF-004; `BENCHMARK_SCORECARD.md` B10.
- **Evidence (P4).**
  - Segmental phantom (80×72×72 voxels, 40 µm, PSF 25 µm).
  - At identity, QC passes (good).
  - Along axis 0, the bone axis:
    - shifts of 80 and 160 µm pass at σ 40 and σ 250;
    - at σ 80 (seeds 7777 and 1500), shifts of 160, 240 and 400 µm pass. The constrained maximum is 0.4–2.8 µm,
      while the raw phase-correlation shifts were 40–280 µm.
  - The flag `partially_unverifiable=True` is set, and the QC still passes.
  - A 400 µm axial shift of a 2 mm gap ROI has Dice 0.80 with the true ROI. Host bone ends would then fall inside the
    ROI, where `compose_three_class` labels them new bone.
  - Transverse shifts of 160 µm are caught. Calvarial and condyle catch 160 µm on every axis.
  - Consequences:
    - F2's "QC 16/16" (and B10 "Yes") says nothing about the error direction that matters most for segmental ROI
      propagation.
    - DF-016 describes the cycle-2 defect backwards. That defect was a false alarm at perfect alignment; the "fix"
      makes axial errors invisible.
    - In F2 v3, 3/16 cases pass at exactly 80.0 µm, the tolerance.
- **Fix.**
  - If any direction is unconstrained in **all** blocks, return `pass=False` with the reason "unverifiable".
  - Better: keep the bone-end blocks. The current exclusion dilates the defect by 3 voxels and drops the end faces;
    those faces constrain the axial shift.
  - Use correlation-peak sharpness per direction instead of image gradient energy.
  - Re-run L4 with axial translations on segmental phantoms, and correct the SCIENTIFIC_METHODS text, DF-016,
    DF-004 and B10.

### C3-SCI-05 — High — held-out precision bounds treat correlated rows as independent; "passes the full criterion" is not demonstrated

- **Location:**
  - `exp_S1_advisor.py:70-90` (row-level Clopper–Pearson);
  - `exp_S1H3_heldout.py:65-77` (percentile bootstrap);
  - `PREREGISTRATION.md:60-61`, inherited by §8 and §9: "structures are the unit of replication for any CI";
  - `EXPERIMENT_REGISTRY.md:52`; `BENCHMARK_SCORECARD.md` B5 "Met for residual graft";
  - every customer page that quotes "95% upper bound … 0.045".
- **Evidence (recount from `exp_S1H3_heldout.json`).**
  - The CP arithmetic itself is correct: 1 − 0.025^(1/80) = 0.0451; 1 − 0.025^(1/22) = 0.154.
  - The units are not independent:
    - the 80 graft-supported rows lie in only 45 (structure, X, PSF) cells, and 35 of those cells appear twice, once
      per noise level on the same noiseless image;
    - signed graft error has an intraclass correlation of 0.31 within structure, giving a design effect of 3.5 and
      an effective n of 23.1, and a CP bound of **0.147**;
    - with structures as the unit (9), the bound is **0.336**.
  - Mineral: 22 supported rows in 7 structures, ICC 0.38, effective n 12, bound 0.263.
  - The pre-registered structure bootstrap gives [0, 0] for both endpoints. A percentile bootstrap cannot produce a
    non-zero upper limit when there are no events, so it is uninformative, not reassuring.
- **Fix.**
  - Report a cluster-aware upper bound: CP on the effective n, or a beta-binomial or GEE bound, with structures as
    the unit, as pre-registered.
  - Change B5 and the registry row to "not demonstrable: 9 structures".
  - Design the next validation with at least about 30 independent structures carrying supported draws, as cycle 2
    §(c) proposed.
  - The customer sentence should give the cluster-aware bound, or say "0 failures among 80 supported measurements
    from 9 simulated structures".

### C3-SCI-06 — High — pre-registration commitments broken after the "final" validation; post-hoc acceptance change used to pass an endpoint

- **Location:**
  - `PREREGISTRATION.md:79-82`: "This is the last advisor change of Generation 2 … no further rule changes";
  - `PREREGISTRATION.md:98`: the amendment;
  - `separability.py:81-84`: the changelog wording was changed after the run ("Final rule change of Generation 2
    **for the characterised-material intensity path**");
  - commit cfad464.
- **Evidence (git).**
  - 7a3ae70 at 00:30:09 pre-registered S1H3 and froze 1.4.1. The S1H3 result was saved at 00:33:21Z (runtime
    185 s, so it started at about 00:30:16, after the commit). cfad464 at 00:34:12 added the S1H3 results **and**
    advisor 1.4.2 (metals, DBBM day-0, BCP, noisy references, method binding).
  - There is no deviations-log entry for 1.4.2.
  - The S1H3 script itself is unchanged since pre-registration. The shared `summarize` changed only for the k = n
    case, which does not occur in S1H3.
  - **Verified:** 1.4.2 does not alter the S1H3 path:
    - in the diff, the only shared-code change is the noise addition, which is unconditional for non-sample models,
      with the same RNG call order;
    - P9 reproduced condyle_4002 (X 3000, PSF 15, σ 70) and calvarial_4200 (X 3000, PSF 15, σ 140) under 1.4.2:
      statuses and errors identical to six decimals.
  - The pre-registered acceptance (§7 by inheritance) makes total mineral (22 supported) "descriptive". The
    deviations log, written after the results, calls it a pass.
- **Fix.**
  - Add deviation rows for 1.2.0–1.4.2, each with the result that triggered it.
  - State in the policy and customer documents that the 1.4.2 rules (metals, DBBM day-0, BCP, noisy references,
    binding) have **no held-out evidence**.
  - Restore the pre-registered verdict for S1H3 mineral: "not demonstrable".
  - Commit acceptance changes before data, and stamp results with the git SHA (C2-SCI-22).

### C3-SCI-07 — High — measured-reference path: no scan noise in the mineral rule, and no partial volume in graft samples

- **Location:**
  - `separability.py:674`: `nb_vals = rng.choice(new_samples_rel)`, with no noise added;
  - `separability.py:472` and `:190`: graft samples use `surface_fraction=0.0` and are returned unmixed;
  - `characterize.py:91-96`: samples are interior voxels only;
  - `MATERIALS_AND_SUPPORT.md:170` and `SCIENTIFIC_METHODS.md:150`: "noise is added to all measured samples".
- **Evidence.**
  - **(P1/P2) Noise.**
    - Setup: new-bone samples U(0.6, 1.0) + N(0, 0.03) (a low-noise control), HA.
    - At noise_rel 0.25 the rule passes (Dice 0.952, threshold 0.610). At 0.30 it passes (Dice 0.931, ratio 1.024,
      threshold 0.615). The assumed-range rule refuses at both (Dice 0.841 and 0.792).
    - Applying those thresholds to voxels with the scan's noise gives a measured/true mineral ratio of **0.773** and
      **0.767**: a supported −23% error.
  - **(P1) Partial volume.**
    - Setup: graft samples N(1.9, 0.076), interior only as `characterise_*` produces them; 200 µm granules at
      40 µm; noise 0.10; 2 weeks.
    - With the measured blur at σ 1.0 voxel, the samples path is **supported** (Dice 0.998). The profile path, which
      has the 1.4.0 blur model, refuses (Dice 0.888). At σ 1.5 the result is the same (0.998 vs 0.872).
    - The samples path also skips the scan-vs-profile check. This is the S1H failure mechanism (blur plus small
      granules), re-opened for exactly the path the documentation calls "preferred".
  - Reachability: library or CLI configuration only (`graft_reference_rel`, `new_bone_reference_rel`). The workflow is
    documented for customers.
- **Fix.**
  - Add `noise_rel` to the new-bone samples in `mineral_rule`.
  - Run measured graft samples through the blur-aware partial-volume model, using the measured thickness and
    the measured blur of **this** scan, or keep the rim voxels in the characterisation and use them.
  - Enforce `compatible_with` in `_assess_scan`.
  - Correct the two documentation sentences.

### C3-SCI-08 — Medium — the blur estimator under-reads blur at high noise; its calibration cannot be reproduced; S1H3 did not record it

- **Location:** `advisor/integration.py:216-265` (the threshold-at-0.5 edge model and `cal = raw·(1 + 1.5·max(0, raw −
  0.6))`); `separability.py:626-630` (host level); `exp_S1H3_heldout.py:62`.
- **Evidence (P3).** The phantom is a 4× in-plane-supersampled tube with Gaussian blur σ. The true total σ, about
  √(σ² + 1/12), is 0.49, 0.66, 0.85, 1.04 and 1.28 voxel:

  | noise_rel | calibrated estimate at those five blurs (voxel) | verdict |
  |---|---|---|
  | 0.05 | 0.50, 0.80, 1.17, 1.60, 2.10 | conservative, as designed |
  | 0.30, white | 0.55, 0.60, 0.60, 0.70, 0.80 | blur under-read by up to 38% |

  - At high noise the estimate barely moves with the true blur.
  - Mechanism: the edge is located by thresholding the noisy image. Voxels selected as bone are biased upward and
    voxels selected as soft tissue downward, which steepens the measured edge.
  - The host anchor also drifts with noise: 1027 at noise_rel 0.05 and 1153 at 0.30, for a true value of 1000. The
    anchor scales every relative quantity.
  - Effect on the advisor (P6, S1H3 phantoms at PSF 50 µm = 1.25 voxel): calibrated 1.6 at noise_rel 0.08, but 0.55–0.60
    at noise_rel 0.30. That is inside the operating range: mineral is accepted up to 0.35.
  - In P6 the dense-graft decisions stayed safe: graft errors within ±12%, new bone and mineral refused. The flaw is
    therefore real but had not yet produced a supported failure there.
  - The calibration ("seed 4321, PSF 10–60 µm") has no script or result in the repository.
  - `test_blur_estimator_tracks_known_psf` uses noise_rel 0.01 only.
- **Fix.**
  - Locate the edge on a smoothed image.
  - Fit both plateau levels and σ, and model or remove the selection bias.
  - Use the estimate's upper confidence limit for decisions.
  - Commit the calibration script and its results over noise_rel 0.02–0.35, and add a noise sweep to the unit test.
  - Record `blur_sigma_vox` in `support_for_scan` output and in every validation row.

### C3-SCI-09 — Medium — the graft partial-volume model is planar while its shell geometry is spherical; it over-states graft contrast for small granules

- **Location:** `separability.py:219-238` (`blur_surface_fraction` uses the spherical shell
  1 − ((T − 2·sh)/T)³; `blur_own_fraction` uses the planar slab formula Φ(δ/σ) + Φ((T − δ)/σ) − 1).
- **Evidence (P8).** The table compares the mean own-class fraction of surface-shell voxels for a blurred sphere with
  the model's planar average:

  | Granule diameter | Blurred sphere | Advisor (planar) |
  |---|---|---|
  | 2σ | 0.15 | 0.61 |
  | 3σ | 0.32 | 0.73 |
  | 4σ | 0.45 | 0.80 |
  | 6σ | 0.60 | 0.81 |
  | 8σ | 0.67 | 0.81 |

  - The planar formula is exact for slabs. Compact granules and rods lose more signal to blur because of curvature.
  - The model therefore over-states how graft-like small granules remain. That is anti-conservative for struts and
    small granules under heavy blur: S1H3 struts measured 150–300 µm, about 3–8σ at PSF 35–50 µm.
  - The measured thickness, taken from a thresholded blurred mask, partly offsets this, by an unknown amount.
- **Fix.**
  - Model the partial-volume distribution directly: blur the scan's own binary graft-like mask with the measured σ
    and sample the result. This gives the correct geometry for any morphology.
  - Otherwise, use sphere or rod formulas matched to the morphology.

### C3-SCI-10 — Medium — the rim gate allows a worst-case mineral error of 25%, not the documented 20%

- **Location:**
  - `separability.py:740-746`: refuse when 0.5·rim/mineral > 0.10;
  - `MATERIALS_AND_SUPPORT.md` / `MEASUREMENT_SUPPORT.md:60-61`: "refused if the worst-case rim error (rim /
    mineral) could exceed 20%";
  - `integration.py:56-73`: the rim comes from the first-pass threshold, not the threshold finally applied.
- **Evidence.**
  - If the whole rim is halo, measured mineral M = true mineral + rim, so the relative error is rim/(M − rim). At the
    gate's limit (rim/M = 0.20) that is 0.20/0.80 = **25%**, before adding the mineral-rule's own error.
  - The gate therefore admits cases whose worst case is beyond the 20% failure threshold, and twice the advisor's
    ±10% accuracy target.
  - The rim uses 6-connected (city-block) dilation, so the "2σ" width is shorter on diagonals.
- **Fix.**
  - Refuse when rim/(M − rim) + |mineral-rule ratio − 1| > 0.10, the advisor's own target, or at least > 0.20.
  - Compute the rim from the final labels, with a Euclidean distance.
  - Correct the documentation.

### C3-SCI-11 — Medium — group statistics: value-dependent (informative) missingness, and conditional values unmarked

- **Location:**
  - `separability.py:506,545-548`: graft refused when graft share < 5% ("trace residual graft");
  - `defectfill.py:72-90`: animal means over measured scans only;
  - `defectfill.py:137-174`: group means and comparisons over measured values only;
  - `defectfill.py:325-337`: no "(c)" marker in group cells.
- **Evidence.**
  - Refusal of residual graft is triggered by a low value of the endpoint itself, so the data are missing not at
    random, by construction.
  - In the group with the most resorption, the animals with the least residual graft are the ones dropped. Its mean
    rises and the between-group difference shrinks or reverses. For example, true values 0.02, 0.03, 0.04, 0.10,
    0.12, 0.15 have a mean of 0.077; after dropping the first three, the mean is 0.123.
  - The report prints "n=k of N" but gives no warning and does not compare refusal rates between groups.
  - Group cells that pool conditional values carry no "(c)" (C2-SCI-14b).
  - The Holm family is defined by the data (only computable tests). That is acceptable, but it should be stated.
- **Fix.**
  - Report trace graft as a censored value ("< 5% of mineral") instead of missing. Include it in a rank test as the
    lowest rank (ties), or use a censored-data model.
  - Print refusal counts per group, and flag the comparison when refusal rates differ (Fisher exact test).
  - Mark conditional values in group cells, and add a footnote on informative missingness.

### C3-SCI-12 — Medium — customer-facing text differs from the code and the evidence

- **Per-material table: matches the script but is best-case.** The table in `MATERIALS_AND_SUPPORT.md` (and
  `science.html`) matches `python3 scripts/material_support_table.py` cell for cell; I checked all 16 rows.
  - The script passes none of the scan-measured gates: rim, blur, deep graft level, measured share.
  - So HA shows "Graft/new bone ✅", while new bone was **never** supported in S1H3 (0/216; 105 of those
    measurements were accurate but refused).
  - The page calls the table "the advisor's actual output". It should say that the scan-measured rules usually
    refuse new bone next to dense graft.
- **"Safe" is overstated.** `science.html:245` says "safe"; `EXPERIMENT_REGISTRY.md:52` says "All endpoints safe" and
  "safe on every endpoint under unseen conditions".
  - For new bone this is vacuous: nothing was supported.
  - For mineral it rests on 22 supported cases (bound 0.154).
  - "Unseen conditions" is overstated: strut morphology and correlated noise were in the development data, and the
    PSFs fall inside the blur-calibration range (C2-SCI-23).
- **Default method stated wrongly.** `SCIENTIFIC_METHODS.md:34` says "`multiotsu` (default in the desktop)". The code
  and the same document at `:169` say `advisor_threshold`.
- **Method binding understated.** `MATERIALS_AND_SUPPORT.md` (method binding) says other methods lose "graft and
  new-bone endpoints". The code refuses total mineral too (`pipeline.py:216-224`).
- **Bone-derived default stated backwards.** `MATERIALS_AND_SUPPORT.md:165` says "A measured profile is always marked
  **not bone-derived**". The code does the reverse (`characterize.py:49-53`: an undeclared status is treated as
  bone-derived). As a result, the documented example `assess_support(ch.profile(), …, graft_samples_rel=…)` refuses
  every graft endpoint unless `bone_derived=False` is passed.
- **Noise sentence wrong.** "Noise added to all measured samples" is incorrect (C3-SCI-07).
- **Registration QC description wrong.** See C3-SCI-04.
- **Desktop wording.** The analysis dialog says "Advisor threshold (validated with measurement support)", and the
  results label says "measurement-support validated", without "in simulation".
- **Fix.** Correct each item. Generate the table with representative scan-measured inputs, or caveat it.

### C3-SCI-13 — Medium — `scripts/check_claims.py` can be fooled

- **Location:** `scripts/check_claims.py:248-283` (anchors; precision rule at `:269`), `:80` (frozen-run guard), `:148`
  (version allowance), `:287` (paths mode).
- **Evidence.** I gave `check_claims.main([...])` a scratch document containing:
  - "residual graft volume supported in 37% … (95% upper bound on the supported-failure rate **0.0**)";
  - "The advisor is proven safe: the supported-failure rate is at most 0.001 (95% bound), new bone is supported in
    95% of specimens".

  The result was "All checked claims match their result files", exit 0. Weaknesses:
  - (a) quoting at lower precision always passes ("0.0" for 0.045);
  - (b) rewording an anchor, or dropping the standard phrase, silently skips the check, because claims never found do
    not fail;
  - (c) qualitative claims ("safe", "every failing measurement refused", "new-bone volume never supported", "sharp
    imaging only") are never checked;
  - (d) the "frozen run" guard compares two strings that the run writes about itself (`preregistered`,
    `advisor_version`), with no git SHA or script hash;
  - (e) the per-material ✅/❌ table is not compared with the script output;
  - (f) L4 (78%), F2 (0.984, 16/16) and S2 numbers are not claims;
  - (g) `VERSION_ALLOW` exempts any line containing "since", "before", "earlier" or "history";
  - (h) passing explicit paths skips the BANNED and VERSION checks.
- **Fix.**
  - Require every claim to be found at least once in its listed files.
  - Require the quoted precision to equal the claim's precision.
  - Add banned overclaim terms ("safe", "proven", "guarantee") and add qualitative assertions as claims.
  - Verify the result's recorded git SHA against the pre-registration commit.
  - Diff the per-material table against the script output.
  - Add L4, F2 and S2 claims.
  - Always run all checks.

### C3-SCI-14 — Medium — registry wording

- **DEFECT_REGISTRY.md:**
  - DF-016 describes the cycle-2 defect backwards, and its fix creates a blind spot (C3-SCI-04).
  - DF-004 ("QC 16/16") needs the axial caveat.
  - DF-010 and DF-011 say "validated on S1H3". For new bone the "fix" is that it is never supported (0% coverage),
    and the S1H3 bound is not cluster-aware (C3-SCI-05).
  - DF-012 "fixed" ignores the API and corrected-label paths (C3-SCI-02/03).
  - DF-014 "fixed" although the "(c)" marker is missing.
  - DF-005's "8 claims" is stale.
- **EXPERIMENT_REGISTRY.md:**
  - The 2026-11-28 entry says the checker "verifies that the file is the pre-registered frozen run". It checks two
    self-reported strings.
  - The F2 row calls the two v2 QC failures "false alarms". Both were residual shifts of exactly 2 voxels (80 µm) in
    the two lowest-Dice cases (0.965 and 0.965), so they are boundary cases, not clearly false.
  - The S1b row status still reads "authoritative" (C2-SCI-01).
- **Fix.** Correct as listed. Add DF entries for C3-SCI-01, 02, 04, 07 and 08.

### C3-SCI-15 — Medium — S2 part a: the zoom selection is clean; the interpretation goes beyond the data

- **Location:** `experiments/exp_S2_sim2real.py:60-82`; `exp_S2v2_sim2real_a.json`; `EXPERIMENT_REGISTRY.md:47`.
- **Evidence.**
  - Verified: the zoom is chosen on the 10 training scans only (`pick_zoom`), and the test set is scored at zoom 1.0
    and at the chosen zoom only. No test leakage.
  - The training curve rises monotonically up to the edge of the grid: 0.316, 0.335, 0.374, 0.442, 0.512 at zoom 0.5,
    0.75, 1, 1.5 and 2. The optimum is therefore not bracketed, so "recovers part of the gap, not all" is not
    established.
  - Linear 2× upsampling also low-pass filters the noise and changes its grain, so structure scale and noise texture
    are confounded. The registry mentions noise only in passing.
  - Test: 0.377 → 0.513 on n = 5 specimens. All 5 improved (+0.078 to +0.228). No confidence interval is reported;
    a two-sided sign test gives p = 0.0625.
- **Fix.**
  - Extend the grid to 2.5, 3 and 4, on training scans only.
  - Add two controls: native-scale smoothing matched to the interpolation's noise reduction, and nearest-neighbour
    zoom.
  - Measure Tb.Th in voxels in both domains.
  - Report a paired bootstrap CI over specimens.

### C3-SCI-16 — Low — method binding uses a substring match, and labels the mechanism wrongly for validated models

- **Location:** `pipeline.py:215`; `separability.py:541-544,577-580`.
- **Evidence.**
  - `validated` is True when the reason text contains "qualifying validation record". Today's failure strings do not
    contain that phrase, so this is brittle rather than wrong now.
  - When a model does qualify, the graft endpoints keep "supported / mechanism intensity" from the intensity oracle,
    not a texture mechanism. The mechanism printed is not the one that justified support.
- **Fix.** Pass the boolean from `validated_for`. When binding keeps a learned model's graft endpoints, set
  `mechanism="validated_texture_model"`.

### C3-SCI-17 — Low — the new-bone error budget uses a share estimate that is biased low under blur

- **Location:** `separability.py:747-758`; `integration.py:60-61`.
- **Evidence.**
  - The gate p/(1 − p)·max(|g − 1|, 0.2) uses the scan's estimated graft share.
  - C2-SCI-13 showed that estimate is biased low under blur: 0.061 vs 0.167, and 0.395 vs 0.556. A low share makes the
    gate pass when it should not.
  - No harm has been observed, because new bone was never supported in S1H2 or S1H3.
- **Fix.** Use an upper confidence bound on the share, from a mixture fit or the share at the lower graft threshold.

### C3-SCI-18 — Low — documentation and comment drift

- The `estimate_blur` docstring says σ ∈ [0.2, 3] voxel; the search grid runs to 4.0 (`integration.py:223,256`).
- The rim refusal reason still says "a one-voxel rim" (`separability.py:734`).
- The comment at `separability.py:550` lists DBBM among the remodelling grafts.
- Rule numbering in `MEASUREMENT_SUPPORT.md` runs 7, 7a, 7b, 7b', 7c, 10, 11, 12, 13, 9, 8.
- `SCIENTIFIC_METHODS.md` §7 says "longitudinal comparisons use mixed models". `stats.mixed_model_longitudinal`
  exists, but the report uses per-timepoint Welch tests only.

## Questions answered

- **Can a non-validated method still produce a "supported" endpoint?**
  - Pipeline: no.
  - Desktop: yes, through a label revision (C3-SCI-03) and through legacy records.
  - API report: yes, functionally. A refused value is printed like a supported one after any edit (C3-SCI-02).
  - Desktop bundle export: protected by `_enforce_support`.
  - Separately, the validated method itself fails silently in its default configuration (C3-SCI-01).
- **Was the pre-registration honoured?**
  - S1H2 and S1H3: the scripts were committed before running, and the results are untouched since.
  - The "final change" and acceptance-rule commitments were not kept (C3-SCI-06).
- **Leakage?** No test data reached development. The "unseen conditions" claim is overstated (C2-SCI-23).
- **Does 1.4.2 differ from 1.4.1 only on paths S1H3 does not exercise?** Yes: verified by the code diff and by P9.
- **Is the CP and bootstrap analysis right?** The arithmetic is right. The unit of analysis is wrong (C3-SCI-05).
- **Is the S2 part a zoom chosen without touching the test set?** Yes. The interpretation is overstated
  (C3-SCI-15).

## Summary

| Severity | Count | Findings |
|---|---|---|
| Critical | 2 | C3-SCI-01, C3-SCI-02 |
| High | 4 | C3-SCI-04, C3-SCI-05, C3-SCI-06, C3-SCI-07 |
| Medium | 9 | C3-SCI-03, C3-SCI-08, C3-SCI-09, C3-SCI-10, C3-SCI-11, C3-SCI-12, C3-SCI-13, C3-SCI-14, C3-SCI-15 |
| Low | 3 | C3-SCI-16, C3-SCI-17, C3-SCI-18 |

**Cycle-2 dispositions:**
- I agree with 10: C2-SCI-03, 05, 06, 07 (with an added defect, C3-SCI-08), 09 (declared metals only), 12, 13 (see
  C3-SCI-11), 19, 20 and 21.
- I partly agree with 5: C2-SCI-01, 08, 10, 14 and 15.
- I disagree with 8: C2-SCI-02, 04, 11, 16, 17, 18, 22 and 23.

**Priority:**
1. C3-SCI-01 and C3-SCI-02 first: a fail-closed report path, and a rim gate for unspecified materials.
2. C3-SCI-04 and C3-SCI-07.
3. Restate the S1H3 claims with a cluster-aware bound and the pre-registered mineral verdict (C3-SCI-05, C3-SCI-06),
   before any further customer-facing use.
