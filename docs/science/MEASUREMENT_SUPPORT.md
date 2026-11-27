# Measurement Support (Identifiability) Policy

Implementation: `osteoquant/advisor/` (version 1.0.0). Validation: Experiment S1 (`experiments/exp_S1_advisor.py`).

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

## Decision rules (pre-registered before Experiment S1)
1. **Mineral endpoints** (total mineral volume, mineralised fraction): supported when noise < 0.35 of the bone–soft
   contrast.
2. **Radiolucent grafts** (collagen, PLGA/PCL, DBM: mean < 0.15 of host): graft endpoints not supported (invisible);
   new-bone endpoints supported with the condition that the graft has no mineral phase.
3. **Intensity mechanism**: the Dice-optimal intensity-only oracle (an upper bound for any threshold method) must
   give graft Dice ≥ 0.85, and the best near-optimal rule a graft-volume ratio within ±10%.
4. **Bone-derived grafts** (allograft, DBBM/xenograft, autograft): never supported by intensity alone — they remodel
   towards bone intensity.
5. **Day-0 mechanism**: if intensity fails but a registered day-0 scan passes registration QC and graft
   displacement is within tolerance (default 200 µm), graft endpoints are *supported with conditions*.
6. **Texture/morphology models**: only with material-specific validation evidence recorded in the model card
   (none exists yet).
7. **Unknown materials**: not supported until characterised (unsupported-material workflow below).
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
