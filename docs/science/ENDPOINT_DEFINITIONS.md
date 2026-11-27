# Endpoint Definitions

Every number OsteoQuant reports is defined here: formula, unit, denominator, treatment of uncertain voxels, and
conditions under which it is reported. Code references point to the implementing function. Nomenclature follows
Bouxsein et al. 2010 (micro-CT) where an equivalent exists; graft-specific endpoints have no standard definition
and are defined by this document.

## Notation
* **ROI** — defect region of interest (`roi` mask), volume **TV** (mm³) = voxel count × voxel volume.
* Label map L with classes 1 = new bone (NB), 2 = residual graft (RG), 3 = host bone (HB), 0 = non-mineral,
  255 = uncertain (abstained: model confidence below τ, default 0.6).
* Volumes are voxel counts × voxel volume (no sub-voxel partial-volume correction). Unit mm³.
* *Certain volume* **TVc** = TV − volume of uncertain voxels in the ROI.

## Primary endpoints
| Endpoint | Formula | Unit | Notes | Reported when |
|---|---|---|---|---|
| Total mineral volume (`mineral_volume_mm3`) | V(NB) + V(RG) in ROI | mm³ | Does not require separating graft from new bone; the robust primary endpoint for most materials | mineral/soft-tissue contrast adequate (noise < 0.35 of bone–soft contrast) |
| Mineralised fraction (`mineralized_fraction`) | (V(NB)+V(RG)+V(HB in ROI)) / TV | – | Host bone inside the ROI counts (e.g. ROI touching cortex) | as above |
| New-bone volume (`new_bone_volume_mm3`) | V(NB) in ROI | mm³ | Requires graft/new-bone separation | advisor status ≠ not_supported |
| New-bone fraction (`new_bone_fraction`) | V(NB)/TV | – | Over full TV; uncertain voxels count as not-NB (conservative) | as above |
| New-bone fraction of certain (`new_bone_fraction_of_certain`) | V(NB)/TVc | – | Removes material-dependent abstention bias (review Q-06); report both | as above |
| Residual-graft volume (`residual_graft_volume_mm3`) | V(RG) in ROI | mm³ | | advisor status ≠ not_supported |
| Residual-graft fraction (`residual_graft_fraction`, `_of_certain`) | V(RG)/TV, V(RG)/TVc | – | | as above |
| Graft resorption (longitudinal) | 1 − V(RG, t)/V(RG, day 0) | – | Requires day-0 scan, registration QC pass | day-0 available + support |
| Bridging (`bridging_all_mineral`, `bridging_new_bone`) | fraction of ROI cross-sections (along defect axis) containing a connected mineral path host-to-host | – | Definition in `morphometry.core.bridging` | mineral: always; new-bone: if NB supported |
| Radial ingrowth profile | NB fraction in concentric shells by distance from ROI boundary | – | shell width max(200 µm, 4 voxels) | NB supported |

## Secondary (architecture) endpoints — computed on new bone in the ROI
| Endpoint | Definition | Unit | Notes |
|---|---|---|---|
| BV/TV | V(NB)/TV | – | |
| Tb.Th | mean local thickness of NB (Hildebrand–Rüegsegger sphere-fitting; thickness = 2 × EDT ridge radius) | µm | Border convention `edge` (pre-registered as default from Gen 2 on; both conventions available) |
| Tb.Sp | local thickness of the ROI complement of NB | µm | same convention |
| Tb.N | 1 / (Tb.Th + Tb.Sp) | 1/mm | model-independent plate approximation |
| Conn.D | (1 − χ)/TV from 26-connected Euler characteristic | 1/mm³ | |
| BS/BV | marching-cubes surface / volume | 1/mm | |
| Thickness endpoints are reported only when typical structures span ≥ 3 voxels (≈150 µm woven trabeculae). |

## Density endpoints
Tissue mineral density (TMD, mgHA/cm³) is reported **only** when the scan carries an HA-phantom calibration
(slope/intercept). Otherwise grey-value statistics are reported and labelled "uncalibrated" (D-004).

## Statistics
Specimen (animal) is the experimental unit. Repeated scans of the same animal at the same timepoint are averaged
before group statistics (D-016). Group comparisons use specimen-level values; longitudinal comparisons use
mixed models with animal as random effect. Voxel counts are never treated as replicates (D-007).

## Measurement support
Each endpoint carries a status (`supported`, `supported_with_conditions`, `not_supported`) from the measurement
support advisor (`docs/science/MEASUREMENT_SUPPORT.md`). Unsupported endpoints appear in reports as
"not measured" with the reason; their raw values remain in the audit record only.
