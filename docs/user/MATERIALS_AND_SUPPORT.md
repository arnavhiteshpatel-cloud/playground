# Materials and measurement support

> **Status.** Research product: not validated on real graft materials; not a medical device; no GLP/Part 11
> compliance claimed. Material profiles combine NIST attenuation physics with **assumed** porosity and granule size;
> none has been measured on a real product yet.

This page tells you, per graft material, which endpoints OsteoQuant can report, which it refuses, and why. The rules
are those of the measurement-support advisor, version 1.2.1 (`osteoquant/advisor/separability.py`); the reasoning
behind them is in [SCIENTIFIC_METHODS.md](SCIENTIFIC_METHODS.md#3-measurement-support-advisor-121) and
[docs/science/MEASUREMENT_SUPPORT.md](../science/MEASUREMENT_SUPPORT.md). Material data:
`osteoquant/knowledge/materials.json`; literature: [SEPARABILITY_ANALYSIS.md](../science/SEPARABILITY_ANALYSIS.md).

## How to read the table

* **Decisions are made per scan.** The same material can be supported on a low-noise scan and refused on a noisy one,
  or refused when little graft remains. The "single scan" and "with day-0" columns below are the advisor's actual
  output for **one illustrative setting**: noise 0.08 of the bone–soft-tissue contrast, 20 µm voxels, residual graft
  30% of mineral, effective energy 40 keV. The day-0 column assumes a registered day-0 scan that passed QC, 50 µm
  granule motion and 5% untracked graft.
* **Statuses:** ✅ supported · ⚠️ supported with conditions · ❌ not supported (reported as *not measured*).
* "Graft/new bone" means residual-graft volume and fraction and new-bone volume and fraction. New-bone architecture
  (BV/TV, Tb.Th, Tb.Sp, Tb.N) follows the new-bone status and additionally needs structures ≥3 voxels.
* The day-0 mechanism is **not validated, even in simulation** (Experiment L3, see
  [SCIENTIFIC_METHODS §5](SCIENTIFIC_METHODS.md#5-longitudinal-day-0-method-and-its-limits)). Treat ⚠️ results from
  it as research read-outs.

## Per-material table

| Material (knowledge-base id) | In desktop menu | Intensity-only separability (literature) | Graft/new bone, single scan | With day-0 scan | Can measure | Cannot measure, and why |
|---|---|---|---|---|---|---|
| Sintered hydroxyapatite (`ha`) | Yes | good | ✅ | ✅ | Total mineral; graft and new bone while the scan is quiet enough | Fails at high noise; thin struts (<3 voxels) and the partial-volume rim at every granule surface take bone-like values; graft volume refused below 5% of mineral |
| Biphasic calcium phosphate (`bcp`) | Yes | partial | ✅ | ✅ | As HA for intact granules | Degraded granules overlap early bone; at noise 0.25 the advisor refuses graft and new-bone endpoints |
| Bioactive glass 45S5 (`bioglass_45s5`) | Yes | partial | ✅ | ✅ | Glass cores separable from bone at this setting | Reaction rim and bonded bone are bone-like; contrast depends on beam energy, so thresholds do not transfer across kVp or filters |
| Bioactive glass S53P4 (`s53p4`) | No (library only) | partial | ✅ | ✅ | As 45S5 | As 45S5; approaches dense mature bone at low energy |
| β-tricalcium phosphate (`beta_tcp`) | Yes | partial | ❌ | ⚠️ | Total mineral | Resorbing, microporous granules enter the bone range; new bone is laid directly on granules. Single-threshold rule fails the volume or half-share requirement. With day-0, bone formed inside the footprint is counted as graft |
| Calcium sulfate (`calcium_sulfate`) | Yes | poor | ❌ | ⚠️ | Total mineral | Porous set dihydrate sits in the bone band; dissolving fronts grade into woven bone; resorbs within weeks |
| Polymer–ceramic composite (`polymer_ceramic_composite`) | No (library only) | poor | ❌ | ⚠️ | Total mineral | Composite struts sit in the early-bone band; known print geometry or a validated model would be needed |
| Deproteinised bovine bone mineral, xenograft (`xenograft_dbbm`) | Yes | poor | ❌ | ⚠️ | Total mineral | Bone-derived: grey values similar to new bone; never supported by intensity, even with measured samples. Day-0 is the most promising route because DBBM barely resorbs |
| Mineralised allograft (`allograft`) | Yes | poor | ❌ | ⚠️ | Total mineral | Same material as host and remodelled bone |
| Autograft (`autograft`) | No (library only) | poor | ❌ | ⚠️ | Total mineral | Identical to host and new bone |
| Demineralised bone matrix (`dbm`) | Yes | poor | ❌ graft · ❌ new bone | ❌ | Total mineral (reported as mineral, not as new bone) | Residual or re-mineralised DBM particles cannot be told from new bone; use histology. Carrier minerals (e.g. CaSO₄) break the radiolucent assumption |
| Collagen sponge, incl. rhBMP-2 carrier (`collagen_sponge`) | Yes | good (for new bone) | ❌ graft · ⚠️ new bone | same | Total mineral; new bone on condition that the carrier has no mineral phase | Residual sponge is invisible on micro-CT |
| PLGA (`plga`), PCL (`pcl`) | No (library only) | good (for new bone) | ❌ graft · ⚠️ new bone | same | As collagen | Polymer volume is not measurable without contrast; a ceramic filler makes it a composite |
| Magnesium alloys (`magnesium`), titanium (`titanium`) | No (library only) | poor / good | ❌ | ❌ | Total mineral only if the scan's mineral rule passes | Metal artefacts (streaks, beam hardening) are not modelled; refused regardless |
| *Unspecified*, or any id not in the knowledge base | *Unspecified* | — | ❌ | ❌ | Total mineral | Not characterised; see the workflow below |
| *No graft (empty defect)* | Yes | — | graft n/a · ✅ new bone | — | All mineral in the ROI counted as new bone | Residual-graft endpoints do not apply |

Endpoints that are independent of the material:

| Endpoint | Needs |
|---|---|
| Total mineral volume, mineralised fraction, all-mineral bridging | Noise below 0.35 of the bone–soft-tissue contrast **and** new bone separable from soft tissue including partial-volume halos of dense phases (advisor ≥1.2.0) |
| Tissue mineral density | An HA-phantom calibration recorded for the scan |
| New-bone thickness endpoints | Supported new bone; woven trabeculae (≈150 µm) spanning ≥3 voxels, so voxels ≤50 µm. The desktop flags Tb.Th below 2.5 voxels |

Effect of the scan, for orientation (advisor 1.2.1, 20 µm voxels, 30% graft share): at noise 0.15, HA, BCP and 45S5
remain supported and β-TCP graft endpoints stay refused; at noise 0.25, mineral and new-bone endpoints are refused for all
four, graft endpoints for BCP, 45S5 and β-TCP, and only HA's residual-graft endpoints remain supported. With residual graft at 3% of mineral, HA graft volume is
refused as "trace residual graft".

## Desktop selection, and what is library-only

The analysis dialog offers: Unspecified, Hydroxyapatite (HA), beta-TCP, Biphasic calcium phosphate, Calcium sulfate,
Bioglass 45S5, Xenograft (DBBM), Allograft, Demineralised bone matrix, Collagen sponge, and No graft (empty defect).
Autograft, S53P4, PLGA, PCL, polymer–ceramic composites and metals are known to the advisor but can only be chosen
through the library (`material` in the pipeline configuration). If your material is not in the menu, choose
*Unspecified* rather than the nearest look-alike.

## Unsupported-material and material-characterisation workflow

Use this when your material is not in the knowledge base, when its profile is an assumption for the endpoint you need
(true of every material today), or when a new lot or protocol is used.

### Steps (from `osteoquant/knowledge/materials.json`, `unsupported_material_workflow`)

1. **Identify.** Record product name, lot, composition (supplier data sheet), form (granule, block, paste, strut),
   granule size, and whether it is bone-derived or contains a mineral carrier.
2. **Characterise.** Scan the material alone, in the same medium as the specimens (saline, agarose or embedding
   resin), and/or a day-0 implanted defect, with the **same** protocol as the study (kVp, filter, voxel size,
   reconstruction, beam-hardening correction), ideally with an HA calibration phantom.
3. **Measure intensity.** Exclude partial-volume rims (erode the surfaces) and record mean, SD and percentiles; record
   the rim distribution separately.
4. **Reference bone.** Measure host bone and, where available, new bone at the study's timepoints (empty-defect
   controls) on the same scale.
5. **Compute separability** with the advisor at the study's noise level and voxel size.
6. **Decide.** Intensity rule allowed if it passes; otherwise require a day-0 design or a texture model validated on
   labelled scans of this material; if neither is available, **abstain**: report total mineral only and state that new
   bone versus graft is not measurable.
7. **Record** the characterisation (scans, SHA-256, protocol, measured distributions, decision) and link it to the
   study's audit trail. Re-characterise when the protocol or lot changes.

Standing abstention rules: never report new-bone volume for a bone-derived graft from intensity alone; never transfer
a threshold across kVp or filter for energy-dependent materials (glasses, calcium sulfate, magnesium); never report
bone-to-graft contact when the voxel size exceeds a quarter of the granule size.

### Doing it with `osteoquant/advisor/characterize.py`

Characterisation is a **library function**; the desktop application does not expose it yet. From a source install:

```python
import numpy as np
from osteoquant.io import read_volume
from osteoquant.advisor import assess_support
from osteoquant.advisor.characterize import characterise_from_day0, characterise_material
from osteoquant.advisor.separability import scan_relative_units

day0, _ = read_volume("day0_scan.nii.gz")            # same scanner and protocol as the study
vox = float(np.mean(day0.spacing))
roi_mask = ...                                         # boolean defect ROI (e.g. from osteoquant.roi.cylinder_roi)

ch = characterise_from_day0(day0.data, roi_mask, vox, material_id="productX_lot42",
                            acquisition={"kvp": 70, "filter": "Al 0.5 mm", "scanner_model": "..."})
print(ch.rel_mean, ch.rel_sd, ch.thickness_um_median, ch.warnings)

# later, for a study scan:
ok, why = ch.compatible_with(voxel_um=vox, acquisition={"kvp": 70, "filter": "Al 0.5 mm"})
est = scan_relative_units(study_scan, exclude_mask=study_roi)        # soft/host levels and noise
a = assess_support(ch.profile(), noise_rel=est["noise_rel"], voxel_um=vox,
                   graft_samples_rel=np.asarray(ch.samples_rel), graft_prior=0.3)
for name, e in a.endpoints.items():
    print(name, e.status, e.reason)
```

What the functions do:

| Function | Input | Notes |
|---|---|---|
| `characterise_material(image, material_mask, soft_mask, host_mask, voxel_um, material_id, source="material_only", acquisition=None)` | A scan of the material alone with fluid/agarose and a reference bone sample in the same field of view; masks for each | Needs ≥500 material voxels and ≥100 voxels each of fluid/soft tissue and reference bone. Intensity is taken from interior voxels (one-voxel erosion) and expressed in relative units |
| `characterise_from_day0(day0_image, roi_mask, voxel_um, material_id, acquisition=None)` | A day-0 scan and the defect ROI | Graft = mineral inside the ROI; host bone and soft tissue are taken outside it (Otsu split) |
| `MaterialCharacterisation.profile()` | — | An advisor profile with `evidence="MEASURED"` |
| `MaterialCharacterisation.compatible_with(voxel_um, acquisition)` | — | Refuses reuse when voxel size differs by >25% or kVp, filter or scanner model differ |
| `MaterialCharacterisation.to_json()` | — | Record including the scan SHA-256, levels, percentiles, thickness distribution, samples and warnings |

Warnings to act on: *median structure thickness <3 voxels* (intensity is partial-volume dominated; re-scan at a
smaller voxel size) and *CV >35%* (mixed materials or beam hardening).

In the pipeline configuration the measured samples are passed as `graft_reference_rel` (and empty-defect control
samples as `new_bone_reference_rel`); fewer than 500 samples are ignored.

### Cautions

* A measured profile is always marked **not bone-derived**. Never characterise an allograft, autograft, xenograft
  or DBM product under a new id: that would bypass the rule that bone-derived grafts are never supported by
  intensity. Use the knowledge-base id and the day-0 route instead.
* A measured new-bone reference from a different control animal made the advisor over-confident in simulation
  (Experiment S1c: 18 of 24 supported conditions failed). Prefer conservative defaults until physical validation
  (stages B and C) has been run.
* Characterisation does not validate the material. It replaces an assumed intensity profile with a measured one;
  accuracy still has to be shown against physical truth.
