# Measurement Support (Identifiability) Policy

Implementation: `osteoquant/advisor/` (version **1.4.2**; every assessment records `advisor_version`). Validation: Experiments S1, S1b, S1c (`experiments/exp_S1*.py`).

## Why
Graft and new bone are both mineral. For many materials their X-ray attenuation overlaps (Experiments C, C2; the
evidence ledger rows 3–5). A segmentation method will still output a number, and that number can look plausible
while being unidentifiable. OsteoQuant therefore decides **before reporting** whether each endpoint can be measured,
by which mechanism, and under which conditions — and abstains otherwise.

## Inputs
| Input | Source | Preferred source |
|---|---|---|
| Graft material | user selection (knowledge base id) | — |
| Graft intensity distribution | material profile (physics + assumed porosity) | **measured**: day-0 scan or a scan of the material alone, same scanner/protocol |
| New-bone intensity distribution | assumed maturity range (relative units 0.60–1.00; 0.60–0.93 early healing) | **measured**: empty-defect control animals at the same timepoint |
| Noise | estimated from the scan outside the defect (MAD of soft tissue; conservative) | — |
| Grey-scale reference | soft-tissue and host-bone levels outside the defect (relative units r = (x − soft)/(host − soft)) | HA calibration phantom |
| Day-0 registration | registration result + QC | — |

## Decision rules (advisor 1.4.3; history: changelog in `osteoquant/advisor/separability.py` and the PREREGISTRATION deviations log)
1. **Mineral endpoints** (total mineral volume, mineralised fraction): supported when noise < 0.35 of the bone–soft
   contrast.
2. **Radiolucent grafts** (collagen, PLGA/PCL, DBM: mean < 0.15 of host): graft endpoints not supported (invisible);
   new-bone endpoints supported with the condition that the graft has no mineral phase.
3. **Intensity mechanism**: the best *single-threshold* rule (the rule actually applied) must give graft Dice ≥ 0.85
   and a graft-volume ratio within ±10%, both at the graft share estimated from the scan and at half of it (volume
   error grows as residual graft becomes scarce). The Dice-optimal bin-union oracle is reported as the upper bound.
   Below 5% graft share of mineral, graft-volume endpoints are refused ("trace residual graft").
4. **Bone-derived grafts** (allograft, DBBM/xenograft, autograft, DBM): never supported by intensity alone. The
   remodelling grafts (autograft, allograft, DBM) are not supported by the day-0 mechanism either — their footprint
   becomes bone; slowly resorbing DBBM may use it (1.4.2, cycle-2 review C2-SCI-10).
5. **Day-0 mechanism**: if intensity fails but a registered day-0 scan passes registration QC (residual
   displacement ≤ 2 voxels) and granule motion is within tolerance (default 200 µm) or tracked with ≤20% untracked
   graft volume, graft endpoints are *supported with conditions*. All four day-0 fields must be computed by the
   software; missing fields mean "not supported". For resorbable materials the condition states that bone formed
   inside the original footprint is counted as graft.
6. **Texture/morphology models**: only with material-specific validation evidence recorded in the model card
   (none exists yet).
7. **Unknown materials**: not supported until characterised (unsupported-material workflow below). Measured
   reference samples need ≥500 voxels; the analysis scan's noise is added to them (1.4.2, C2-SCI-08).
7a. **Metals** (titanium, magnesium): never supported, including total mineral (1.4.2, C2-SCI-09) — streak/beam-
    hardening artefacts are not modelled.
7b. **Material profiles** come from the knowledge base (`osteoquant/knowledge/materials.json`, verified references);
    where the knowledge base and the NIST physics model disagree by >25%, intensity support requires a measured
    material reference (material-only or day-0 scan).
7b'. **Scan-vs-profile consistency** (1.3.1): if the defect's graft-like intensities (voxels brighter than mature
    bone) have a median more than 15% away from the profile's graft level, the profile does not describe this
    scanner/protocol and intensity support requires a measured reference.
7c. **Resorbable materials** (β-TCP, BCP from 1.4.2, calcium sulfate, bioactive glasses, polymer–ceramic composites) are intensity-
    supported only at a known timepoint ≤4 weeks after implantation: resorbing granules become microporous and enter
    the bone intensity range.
10. **Scan-measured imaging** (1.4.0): total blur σ is estimated from host-bone/soft-tissue edges outside the defect
    (edge-spread fit; conservatively inflated above 0.6 voxel); graft granule thickness (local thickness) and the deep
    graft level are measured in the scan and drive a blur-aware partial-volume model of the graft (two-sided edge model
    Φ(δ/σ) + Φ((T−δ)/σ) − 1).
11. **New-bone error propagation** (1.4.0): new bone = mineral − graft, so new-bone endpoints require
    |new-bone/soft ratio − 1| + (p/(1−p))·max(|graft ratio − 1|, 0.20) ≤ 10%, p = the scan's graft share of mineral.
12. **Ambiguous graft rim** (1.4.0; width max(1, ⌈2σ⌉) voxels from 1.4.1): mineral that is not graft-like but lies within the blur shell of graft-like voxels may be new-bone coating
    or graft halo. New-bone endpoints are refused if this rim exceeds 10% of the would-be new bone; total mineral is
    refused if the worst-case rim error could exceed 20%: from 1.4.3 that is rim / (mineral − rim), the error if the whole
    rim is graft halo (the 1.4.1 gate on half the rim admitted up to 25%; C3-SCI-10). With no graft threshold
    (unspecified or unknown material), voxels brighter than host bone are the graft proxy for this gate (1.4.3, C3-SCI-01).
14. **Measured references** (1.4.3, C3-SCI-07): measured graft samples get the analysis scan's partial-volume mixing
    (blur-aware with the measured granule thickness); measured new-bone samples get the scan's noise in the mineral rule.
15. **Day-0 for resorbable materials** (1.4.3): needs a known time since implantation ≤12 weeks (policy constant);
    BCP and polymer–ceramic composites are resorbable here too. Knowledge-base profiles without a physics cross-check
    (S53P4, polymer–ceramic composite) are uncertain and need a measured reference.
16. **Read-time evaluation** (C3-PRD-01): stored statuses are re-evaluated whenever a result is shown or reported; an
    assessment made by another advisor version or support-rule set is *not assessed* ("re-analyse"), and a manually
    corrected segmentation keeps at most *supported with conditions*.
13. **Method binding** (pipeline, 1.4.2, C2-SCI-02): support statuses apply to the method they were validated with,
    `advisor_threshold`. For any other segmentation method, tissue endpoints are set to not supported, except graft
    endpoints of a learned model whose vendor-signed validation record qualifies (none exists). Tissue mineral density
    is unaffected.
9. **New bone vs soft tissue** (advisor ≥1.2.0): the mineral threshold and the new-bone/mineral endpoints are gated by
   a partial-volume model of soft tissue next to dense phases, using the surface-shell fraction measured in the scan.
8. **Density**: only with HA calibration.

## Unsupported-material workflow
1. Scan the material alone (or the day-0 implant) on the customer's scanner and protocol.
2. OsteoQuant measures its intensity distribution in relative units and its granule/strut size.
3. With empty-defect controls (or the conservative assumption), the advisor computes the oracle.
4. If not separable: report total mineral; recommend a day-0 scan design or histology; record the decision in
   the study's audit trail.

## Known limitations
* The physics-derived profiles share the simulator's attenuation model; material porosities are assumptions.
* The oracle is an upper bound: a supported endpoint can still be mis-measured by a poor method (see S1:
  multi-Otsu errors on supported HA specimens). Rule 13 therefore binds support to `advisor_threshold`.
* Thresholds (0.85, ±10%, 0.35, 25%, 15%, 10%, 20%, 4 weeks, 200 µm, 2 voxels) are policy choices, to be revisited
  with real data.
* The control-reference mixing constant (0.2) was set on one control and is untested on held-out data (C2-SCI-06);
  the new-bone halo model still uses assumed constants (C2-SCI-07).

## Validation status (Generation 2, simulation only)
Four pre-registered held-out simulations were run, each on conditions unseen by the advisor version tested:
S1H (1.3.3: new-bone and some graft measurements failed while supported), S1H2 (1.4.0: graft passed, total mineral
failed at heavy blur), S1H3 (1.4.1): every failing measurement refused on every endpoint; residual graft 0/80
supported failures from 9 phantom structures (95% upper bound 0.34 with structures as the pre-registered unit; 0.045
only if rows were independent), total mineral 0/22, new bone never supported; and **S1H4 (1.4.3, the shipped
version, on the application's material paths: knowledge-base HA, BCP, β-TCP, xenograft DBBM and Unspecified; 720
specimens from 36 structures)**: every failing measurement refused on every endpoint (510 graft, 379 new-bone, 34
mineral failures); residual graft 0/69 supported failures from 24 structures, all HA (95% upper bound 0.14 with
structures as the unit; 0.052 if rows were independent); total mineral 0/12, all β-TCP at one imaging condition,
with supported values 7–17% low; new bone never supported; nothing supported with the material Unspecified; no volume
endpoint supported for 89% of specimens. The precision criterion (bound ≤ 0.10) is **not demonstrated** in S1H3 or
S1H4. All of this is SYNTHETIC; the advisor and simulator share physics, and no physical or in-vivo validation exists
(validation stages B–F). Results: EXPERIMENT_REGISTRY.md (S1H, S1H2, S1H3, S1H4).
