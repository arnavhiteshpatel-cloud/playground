# Cycle 3 — Science review response (REVIEW_SCIENCE.md)

Status: **fixed** (change plus test or re-run), **corrected** (claims and records restated), **open** (planned; reason
given), **accepted** (limitation stated).

## New findings

| ID | Sev | Status | Response / evidence |
|---|---|---|---|
| C3-SCI-01 | Critical | fixed | Advisor 1.4.3: with no graft threshold (unspecified or unknown material), voxels brighter than host bone are the graft proxy for the ambiguous-rim gate. On reviewer-style phantoms (dense graft, PSF 35–50 µm) total mineral is now refused in all 8 cases, including the 5 with +21…+44% error (3 accurate cases are refused too). Regression test `test_unspecified_material_refuses_mineral_next_to_dense_blurred_graft`; the material table row and the "choose Unspecified" advice were rewritten. |
| C3-SCI-02 | Critical | fixed | API label edits carry the base assessment (downgraded to conditional at read time); results with no assessment fail closed in reports (`unassessed_support`); API and CLI default to `advisor_threshold`. |
| C3-SCI-03 | Medium | fixed | Manually corrected segmentations keep at most *supported with conditions*. |
| C3-SCI-04 | High | fixed | Registration QC fails closed when some direction is constrained by no block, and names it. Experiment L5: 0/18 misregistrations (160–400 µm, all axes) pass; aligned segmental specimens without axial structure are reported as not verifiable. F2 is unchanged (16/16; its short specimens' bone ends constrain the axis). `SCIENTIFIC_METHODS.md` and DF-016 corrected (DF-033). |
| C3-SCI-05 | High | corrected | S1H3 is restated with structures as the pre-registered unit: 0/80 supported failures from 9 structures, Clopper–Pearson 95% upper bound 0.34 (0.045 only if rows were independent); **the precision criterion is not demonstrated**. The standard phrase, registry, ledger, scorecard (B5) and policy document say so; `check_claims.py` binds both bounds to the result file. |
| C3-SCI-06 | High | corrected | Deviations log: 1.4.2 after the "final" validation (recorded late; no S1H3 path touched), 1.4.3 (one stricter change on the S1H3 path; consistency re-run of the same conditions: total mineral supported 8 instead of 22, still 0 failures), and the retrospective acceptance amendment is not used to call any S1H3 endpoint a pass. A further claim about 1.4.3 needs a new pre-registered held-out test (planned, see C2-SCI-18). |
| C3-SCI-07 | High | fixed | Measured graft samples get the analysis scan's partial volume (blur-aware with measured granule thickness); measured new-bone samples get the scan's noise in the mineral rule (the review's P1 case now refuses). Test `test_measured_references_get_scan_noise_and_partial_volume`. Not done: enforcing `compatible_with` inside `_assess_scan`. |
| C3-SCI-08 | Medium | open | Blur-estimator calibration script and recording of the estimate in validation rows (`blur_est` was None in S1H3). Results now record the git commit (`experiments/common.py`). |
| C3-SCI-09 | Medium | accepted | The planar two-sided edge model overstates graft contrast for small spherical granules; stated as a limitation; to be revisited with physical phantoms (stage B). |
| C3-SCI-10 | Medium | fixed | Total mineral is refused when the worst-case error rim/(mineral − rim) could exceed 20% (was half the rim ≤10% of mineral, admitting 25%). Test updated. Not done: Euclidean rim from final labels. |
| C3-SCI-11 | Medium | partly fixed | Refused and not-assessed values never enter group statistics (renderer-enforced); per-endpoint n is shown. Open: marking conditional values in group statistics and a sensitivity analysis for informative missingness. |
| C3-SCI-12 | Medium | fixed | The per-material table is generated from the full per-scan decision on synthetic phantoms (blur, graft level, rim); website, user docs and the deck slide use it; new bone is shown as not supported for every material, as in S1H3. |
| C3-SCI-13 | Medium | fixed | The checker rejects a non-zero quantity quoted as zero, bans "proven safe" phrasing, reads decks and PDFs, and binds the structure-level bound, the row-level bound, the structure count and the no-endpoint share. |
| C3-SCI-14 | Medium | fixed | Registry wording for S1H3, L4, F2, S1b/S1c and the status entry corrected. |
| C3-SCI-15 | Medium | partly fixed | S2 part a wording softened ("consistent with"); the 5-specimen limitation is stated; no CI is quoted. |
| C3-SCI-16 | Low | fixed | Boolean binding (C3-PRD-02) and the mechanism of a validated model's graft endpoints is `validated_texture_model`. |
| C3-SCI-17 | Low | open | Bias of the share estimate under blur in the new-bone error budget. |
| C3-SCI-18 | Low | partly fixed | Documentation drift corrected where found (versions, rules, QC text, noise sentence). |

## Cycle-2 dispositions the review disputed

| ID | Response |
|---|---|
| C2-SCI-02 | Agreed; API path, carried-over support on edits and old records are now handled (C3-SCI-02/03, C3-PRD-01). |
| C2-SCI-04 | Agreed; the blind spot is closed by failing closed (C3-SCI-04, Experiment L5 in the repository). |
| C2-SCI-11 | Three of four parts now fixed in 1.4.3: BCP in the day-0 resorbable list, day-0 time limit for resorbable materials (policy constant, 12 weeks), S53P4 without physics cross-check treated as uncertain. Open: tying the ≤4-week rule to species and resorption kinetics. |
| C2-SCI-16 | Agreed; the amendment is used only for future validations (deviations log). |
| C2-SCI-17 | Agreed; the headline bound is now per structure. |
| C2-SCI-18 | Agreed; no held-out run yet uses the knowledge-base material path or "Unspecified". Planned: a pre-registered S1H4 with knowledge-base and Unspecified arms and structure-level inference with more structures. |
| C2-SCI-22 | Partly: results now record the git commit; the deviations log covers 1.4.2 and 1.4.3; earlier 1.2.0–1.4.1 changes are in the advisor changelog. |
| C2-SCI-23 | Accepted: S1H3 shares the simulator's assumptions; only physical validation removes that limitation. |
