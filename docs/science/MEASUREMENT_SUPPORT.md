# Measurement Support (Identifiability) Policy

Implementation: `osteoquant/advisor/` (version **1.4.1**; every assessment records `advisor_version`). Validation: Experiments S1, S1b, S1c (`experiments/exp_S1*.py`).

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

## Decision rules (advisor 1.1.0; see PREREGISTRATION deviations log for history)
1. **Mineral endpoints** (total mineral volume, mineralised fraction): supported when noise < 0.35 of the bone–soft
   contrast.
2. **Radiolucent grafts** (collagen, PLGA/PCL, DBM: mean < 0.15 of host): graft endpoints not supported (invisible);
   new-bone endpoints supported with the condition that the graft has no mineral phase.
3. **Intensity mechanism**: the best *single-threshold* rule (the rule actually applied) must give graft Dice ≥ 0.85
   and a graft-volume ratio within ±10%, both at the graft share estimated from the scan and at half of it (volume
   error grows as residual graft becomes scarce). The Dice-optimal bin-union oracle is reported as the upper bound.
   Below 5% graft share of mineral, graft-volume endpoints are refused ("trace residual graft").
4. **Bone-derived grafts** (allograft, DBBM/xenograft, autograft): never supported by intensity alone or by the day-0 mechanism — they remodel
   towards bone intensity.
5. **Day-0 mechanism**: if intensity fails but a registered day-0 scan passes registration QC (residual
   displacement ≤ 2 voxels) and granule motion is within tolerance (default 200 µm) or tracked with ≤20% untracked
   graft volume, graft endpoints are *supported with conditions*. All four day-0 fields must be computed by the
   software; missing fields mean "not supported". For resorbable materials the condition states that bone formed
   inside the original footprint is counted as graft.
6. **Texture/morphology models**: only with material-specific validation evidence recorded in the model card
   (none exists yet).
7. **Unknown materials**: not supported until characterised (unsupported-material workflow below). Measured
   reference samples need ≥500 voxels.
7a. **Metals** (titanium, magnesium): never supported — streak/beam-hardening artefacts are not modelled.
7b. **Material profiles** come from the knowledge base (`osteoquant/knowledge/materials.json`, verified references);
    where the knowledge base and the NIST physics model disagree by >25%, intensity support requires a measured
    material reference (material-only or day-0 scan).
7b'. **Scan-vs-profile consistency** (1.3.1): if the defect's graft-like intensities (voxels brighter than mature
    bone) have a median more than 15% away from the profile's graft level, the profile does not describe this
    scanner/protocol and intensity support requires a measured reference.
7c. **Resorbable materials** (β-TCP, calcium sulfate, bioactive glasses, polymer–ceramic composites) are intensity-
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
    refused if the worst-case rim error (rim / mineral) could exceed 20%.
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
  multi-Otsu errors on supported HA specimens). The pipeline must use a method that approaches the oracle.
* Thresholds (0.85, ±10%, 0.35, 200 µm) are policy choices, to be revisited with real data.
