# OsteoQuant Science Knowledge Base

Version 1.0, 2026-11-27. This file consolidates what OsteoQuant can rely on when it separates newly formed bone, residual graft and host bone in micro-CT of animal defect models.

**How to read it**

- Citations are `[key]` entries in `docs/science/references.bib`. Every entry there was resolved against Crossref. The entry also records how far its content was checked: `verified-full-text`, `verified-abstract` or `verified-metadata-only`. Claims rest only on sources checked at the abstract or full-text level. Metadata-only entries are cited only to name a method or standard.
- `[derived]` marks our own calculation from verified inputs, for example NIST attenuation data `[hubbell_nist_xcom]`.
- `[assumption]` marks values that have no source. These must be replaced by measurement.
- The machine-readable form of section 3 is `osteoquant/knowledge/materials.json` (load it with `osteoquant.knowledge.load_materials()`).
- Earlier, longer notes are still useful background: `BONE_BIOLOGY_AND_GRAFTS.md`, `MICROCT_IMAGING_SCIENCE.md`, `MORPHOMETRY_STANDARDS.md` and `SEPARABILITY_ANALYSIS.md`. Where they disagree with this file, this file wins, because its sources were re-verified.

---

## 1. Bone healing biology and timelines

### 1.1 Mechanisms

- **Fracture repair follows two pathways.** Most fractures heal indirectly, through both intramembranous and endochondral bone formation. Direct (primary) healing occurs only when the fracture is anatomically reduced and rigidly fixed [marsell2011].
- **Repair runs through four overlapping stages:** inflammation, soft callus, hard callus, then bony union and remodelling. The stages are better seen as anabolic and catabolic processes running side by side than as discrete steps [schindeler2008].
- **Repair recapitulates embryonic skeletal development.** It differs because it happens in a post-natal mechanical and inflammatory environment [gerstenfeld2003; einhorn2015].
- **About 10% of fractures do not heal normally** [einhorn2015].
- **Mineral density tracks maturation, and it matters for imaging.**
  - Rat femoral callus at 24 days showed spatially heterogeneous tissue mineral density (TMD). TMD was highest in the gap centre and correlated with indentation modulus (R = 0.70) [leong2009].
  - In mouse fracture calluses, a "mineralised callus" threshold of 641.9 mgHA/cm³ was used. This is about 45% of the attenuation of mature cortical bone (Scanco µCT40, 12 µm voxels) [morgan2009].
  - So early new bone sits well below mature bone in density, and its density rises over weeks. Any intensity-based classifier faces a moving target.

### 1.2 Critical-size defects (CSD)

| Model | What the verified sources say | Source |
|---|---|---|
| General definition | A CSD is the smallest defect that will not heal during the animal's lifetime. Rodent and rabbit calvaria come first in the proposed testing hierarchy, then dog and monkey mandibles | [schmitz1986] |
| Practical criterion | No mineralised area ≥ 30% after 52 weeks means complete bony regeneration will never occur | [li2015] |
| FDA criterion (dental) | The smallest intraosseous wound that will not heal spontaneously, i.e. that reaches no more than 30% fill with regenerated tissue over roughly six months. It must be validated with an empty (sham) defect | [fda2025dental] |
| Rat calvaria | Protocol paper; tissue is usually collected 4–12 weeks after surgery | [spicer2012] |
| Rat calvaria size | A systematic review of 61 papers concluded that 5.0 mm defects "could be considered as a CSD". Untreated 5 and 6 mm defects occasionally closed completely. Mean %NBF, e.g. 8 mm single defect: 9.8% / 12.6% / 8.0% at 1 / 2 / 3 months | [vajgel2014] |
| Rat calvaria, in vivo µCT | Longitudinal BMC at 3, 6, 9 and 12 weeks; 80 kVp, 45 µm voxels; precision 2.5% | [umoh2009] |
| Mouse calvaria | 4 mm defects in nude mice | [li2015] |
| Rabbit | Cylindrical 7–10 mm defects; mandibular and tibial CSD variants | [li2015] |
| Rabbit calvaria | 8 mm parietal CSD, DBB vs BCP, evaluated at 15 and 45 days | [brito2021] |
| Rat femur, segmental | 8 mm defect with modular fixation and a window for longitudinal in vivo µCT (4–16 weeks). Bone formed first at the scaffold periphery; BMP-2 + TGF-β3 bridged only 2 of 6 | [oest2007] |
| Rabbit femoral condyle | Monocortical drilled defects with 3D-printed CaP scaffolds, explanted at 8 weeks for µCT and resin histology | [raymond2022] |
| Minipig mandible | Standardised defects grafted and evaluated at 1–8 weeks by histomorphometry | [jensen2006; broggini2015] |
| Large animals | Most publications describe large-animal segmental models only rudimentarily; standardisation is needed | [reichert2009] |
| Species choice | The rabbit is the most commonly used species but shows the least similarity to human bone. Pig bone is close to human. Dog and sheep/goat are promising | [pearce2007] |
| Pig vs human | Bone regeneration rate 1.2–1.5 µm/day in pig vs 1.0–1.5 µm/day in human | [li2015] |
| Dental devices (FDA) | Skeletally mature canine or porcine models are preferred over rodents; rodents keep growing bone throughout life | [fda2025dental] |

**Timelines OsteoQuant should expect.** These are typical design choices, not biological constants:

- Rodent calvaria: 4–12 weeks [spicer2012; umoh2009].
- Rat segmental femur: 4–16 weeks [oest2007].
- Rabbit condyle: about 8 weeks [raymond2022].
- Minipig mandible: 1–8 weeks [jensen2006; broggini2015].
- FDA dental animal studies: e.g. 4, 8 and 12 weeks, optionally 2 and/or 26 weeks [fda2025dental].

A model's timepoint changes both the expected new-bone TMD (section 1.1) and the expected residual graft (section 3). The software must therefore treat the timepoint as an input, not as metadata.

---

## 2. Bone healing and grafts: what "new bone" means in each model

- **Osteoconduction, osteoinduction and osseointegration** are distinct concepts with distinct experimental tests [albrektsson2001]. This is a metadata-only source, used here only for the terminology.
- **Calvarial defects.** Host bone is the trephined edge, so mineral inside the cylinder is new or graft. The host vs new problem is mainly geometric [spicer2012].
- **Condylar and metaphyseal defects.** These are surrounded by host trabecular bone. Once new bone remodels to lamellar density, it cannot be told from host bone by intensity. A day-0 or immediate post-op scan is needed to define the original cavity. This is [derived] from section 4; no direct source was verified.
- **Segmental defects.** The cortical ends are identifiable. Bone first forms at the scaffold periphery [oest2007].

---

## 3. Graft materials

The table summarises `osteoquant/knowledge/materials.json`. HA-equivalent values for the dense solid phase are [derived] from NIST data at 30–50 keV monoenergetic, as a stand-in for a filtered 40–70 kVp lab scan [assumption]. Apparent values for porous material scale with (1 − sub-voxel porosity). Host bone is taken as 1075 mgHA/cm³, between desktop-µCT TMD (942–1027) and SRµCT TMD (1147–1161) of human trabecular bone [kazakia2008].

| Material | Composition / density | Dense HA-eq (mgHA/cm³) | Resorption (verified) | Intensity-only separability |
|---|---|---|---|---|
| HA (sintered) | Ca10(PO4)6(OH)2, 3.155 g/cm³ [eliaz2017] | 3154 | "Often remain in the body for several years" [eliaz2017]; about 10% resorbed at 12 months [fernandezdegrado2018]; nano-HA filler 34.5% → 31.2% from 2 to 8 weeks in minipig [broggini2015] | **good** for dense granules when voxel ≤ ¼ granule size; partial for micro/nano-porous HA |
| β-TCP | β-Ca3(PO4)2, 3.067 g/cm³ [eliaz2017]; porosity and grain size vary with impurities [bohner2020] | 3024 | Almost completely resorbed over 8 weeks in minipig mandible [jensen2006]; ~13–20 weeks (review) and 60% at 12 months [fernandezdegrado2018]; CaP replacement 3–36 months [eliaz2017] | **partial**: good early, overlaps bone as it resorbs |
| BCP | HA/β-TCP mix; ratio and dual porosity control resorption [bouler2017] | ~3100 | 60/40 BCP filler 23.6% at both 2 and 8 weeks in minipig [broggini2015] | **partial**: intact granules give three peaks (soft tissue ≈1, new bone ≈3.8, BCP ≈7.5 cm⁻¹ at 25 keV SRµCT). Degraded material needs a joint histology–µCT histogram [stalder2014] |
| Calcium sulfate | CaSO4·2H2O (set), density 2.32 [assumption] | 1653 (energy-dependent) | "Rapid and complete resorption" [thomas2009]; 1–3 months, faster than bone deposition [fernandezdegrado2018] | **poor**: porous set material falls into the bone band; dissolving fronts grade into woven bone |
| 45S5 bioactive glass | 45 SiO2 / 24.5 Na2O / 24.5 CaO / 6 P2O5 wt% [fiume2018]; 2.7 g/cm³ [assumption] | 1688 (strongly energy-dependent) | Bonds to bone via a reaction layer [jones2013]; silica glass resorption "complete in 6 months" (single cited source in a review) [fernandezdegrado2018] | **partial**: cores are brighter, but the reaction rim is bone-like |
| S53P4 bioactive glass | 53 SiO2 / 23 Na2O / 20 CaO / 4 P2O5 wt%; granules 0.5–0.8 and 0.8–1 mm in a clinical series [vangestel2015] | 1566 | Clinical use with multi-year follow-up; no quantified residual kinetics [vangestel2015] | **partial** |
| DBBM xenograft (Bio-Oss-type) | Deproteinised bovine bone mineral; sintered variants exist [kapogianni2019] | ≈ bone tissue [inference] | No change in particle size between 6 months and 11 years in human sinus grafts [mordenfeld2010]; stable over 8 weeks in minipig [jensen2006] | **poor**: grey values similar to new bone [kapogianni2019]. In 111 human DBB sinus biopsies, µCT mineralised volume in the grafted region did not correlate with histomorphometry (r = −0.028) [lima2022] |
| Mineralised allograft | Donor bone [delloye2007] | = host bone | Creeping substitution; "very slow … may require years" for large segmental defects [gruskin2012] | **poor** (same material) |
| Autograft | Patient's own bone [sen2007] | = host bone | Filler 17.1% → 9.3% from 2 to 8 weeks, with the most new bone of all groups [broggini2015] | **poor** (same material) |
| DBM | Demineralised allograft matrix, 1–6% residual mineral, often in carriers (including CaSO4); particles 420–840 µm more osteoinductive than < 250 µm [gruskin2012] | < ~100 | Matrix degradation; not quantified | **poor**: invisible at first; remineralised or incorporated particles cannot be told from new bone |
| Collagen sponge / rhBMP-2 carrier | Type I collagen; rhBMP-2/ACS 1.5 mg/cc [mckay2007; geiger2003] | ≈ soft tissue | Not quantified | Radiolucent: mineral = bone, but residual carrier cannot be measured |
| PLGA / PLA | Polyester; hydrolysis tuned by copolymer ratio [middleton2000] | ~30 | Not quantified here | Radiolucent polymer |
| PCL | (C6H10O2)n [woodruff2010, metadata only] | ~0 | Not verified | Radiolucent polymer |
| Polymer–ceramic composite | Polymer + CaP filler | ≈ φ_ceramic × 3024 (20 vol% → ~600) [derived] | Depends on phases | **poor**: struts sit in the woven-bone band |
| Mg alloys | Mg + Zn/Ca/Al/RE [staiger2006] | ~630 | Alloy-dependent corrosion; CaP-rich corrosion layer in contact with bone [witte2005] | **poor**: metal overlaps woven bone; degradation layer is bone-like |
| Titanium | Ti / Ti6Al4V | ~10,000 (out of range) | Non-degradable | Metal is trivially separable; peri-implant voxels are corrupted by artefacts. µCT vs histomorphometry r = 0.855 for bone–implant contact in rabbit tibia [park2005] |

Notes:

- **rhBMP-2 carriers.** The approved rhBMP-2 product uses an absorbable collagen sponge [mckay2007]. For imaging, the carrier is radiolucent, so all mineral is bone. Ectopic bone outside the defect envelope must therefore be measured separately.
- **Porosity matters.** Porosity and pore size affect bone ingrowth [karageorgiou2005]. They also scale the apparent density of every ceramic linearly [derived]. Granule porosity is the single most influential unsourced number in materials.json. The product should **measure** it with a material-alone scan (section 9).

---

## 4. Micro-CT physics that controls separability

1. **Beam hardening.**
   - A polychromatic beam is preferentially stripped of low-energy photons, so attenuation is non-linear in thickness. This produces cupping and pseudo-cortex artefacts; prefiltration and linearisation correct it [brooks1976].
   - In micro-CT of mineralised tissue, beam-hardening artefacts of up to 32.6% occurred in specimen sizes of interest. Filtration reduces them. With an optimised setup, BMD correlated with ash weight (R² = 0.983) [meganck2009].
   - *Product consequence:* a graft-vs-bone threshold set on one specimen size, filter or kVp does not transfer.
2. **HA calibration.**
   - The conversion from µ to equivalent density depends on tube voltage, source distance, detector size and the medium around the specimen. Solid HA-resin phantoms cannot be scanned inside a different medium [nazarian2008].
   - Desktop µCT under-reads TMD by roughly 13–17% relative to SRµCT. Measured values: µCT 942–1027 vs SRµCT 1147–1161 mgHA/cm³; ash 1251–1295 [kazakia2008].
   - *Consequence:* absolute mgHA/cm³ values for grafts are protocol-specific. Separability must be computed on the study's own calibrated scale.
3. **Energy dependence of non-CaP grafts** [derived from hubbell_nist_xcom].
   - CaP ceramics have HA-equivalent values that are flat with energy, so their contrast against bone comes only from packing density.
   - Bioactive glasses (Na, Si), calcium sulfate (S) and Mg have HA-equivalents that change with energy. For 45S5 the value is 1638 → 1758 mgHA/cm³ from 30 to 50 keV.
   - So kVp/filter changes alter glass-to-bone contrast, and thresholds for these materials are protocol-locked.
4. **Partial volume and thresholds.**
   - A 0.5% threshold change altered BV/TV by 5% at BV/TV 0.2, but by only 2% at higher volume fractions [hara2002].
   - Voxel size strongly affects connectivity density, Tb.Th and TMD. Threshold methods diverge at large voxels [christiansen2016].
   - Systems agree on BV/TV but differ on Tb.Th, Tb.N and BS/BV near their resolution limit [verdelis2011].
   - Every granule surface creates a band of intermediate voxels. Kapogianni et al. attribute the 2D/3D discrepancy in material–bone contact to µCT resolution [kapogianni2019].
5. **Dual- and multi-energy µCT.**
   - Dual- and triple-energy cone-beam µCT decomposed bone from a Pb-based vascular contrast agent with > 95% accuracy [granton2008].
   - This demonstrates the principle for materials with different effective Z. It **cannot** help with CaP ceramics, DBBM, allograft or autograft, which are chemically bone-like [derived].
   - It has not been demonstrated for glass or CaSO4 vs bone in a verified source.
6. **Contrast agents for soft tissue.** Hf-POM contrast-enhanced CT shows mineralised bone, marrow vasculature and adipocytes at the same time, validated against histology [kerckhofs2018]. It does not help separate graft from bone. It is relevant to non-mineralised tissue (fibrous tissue, osteoid-rich regions) in the defect.
7. **Reconstruction and ring artefacts.** FDK cone-beam reconstruction [feldkamp1984] and ring-artefact compensation [boin2006] are named for completeness (metadata-only sources).

---

## 5. Morphometry standards (micro-CT)

Bouxsein et al. 2010 [bouxsein2010] require papers presenting µCT outcomes to report:

- the scanning medium, X-ray tube potential and voxel size;
- the size and location of the volume of interest;
- the segmentation method;
- a minimal set of outcome variables with standard terminology and units.

These requirements are checked against the abstract. Per-variable tables are in `MORPHOMETRY_STANDARDS.md`, which an earlier session wrote without full-text access.

Related method sources, named only (metadata-only):

- direct model-independent thickness [hildebrand1997];
- connectivity via the Euler characteristic [odgaard1993];
- BoneJ [doube2010].

The structure model index assumes an all-convex surface, which trabecular bone violates [salmon2015]. **Do not report SMI as a rod/plate measure.**

The FDA dental guidance requires similar µCT reporting [fda2025dental]:

- system and calibration, sample preparation, scanning medium, kVp, filtration, integration time and voxel size;
- ROI selection, filtering and segmentation (method, algorithm and threshold separating bone from device);
- artefact correction (beam hardening, rings, partial volume);
- the metrics and algorithms used.

---

## 6. Histomorphometry standards

- The current nomenclature standard is the ASBMR 2012 update [dempster2013], which replaced the 1987 report [parfitt1987]. Both are cited here at metadata level only. Symbol-level details are in `MORPHOMETRY_STANDARDS.md` §3 from an earlier session.
- Histology is the regulatory reference for "bone formation, device resorption, presence of residual material":
  - FDA dental guidance asks for radiography, histology and histomorphometry.
  - Histology must be read by a board-certified veterinary pathologist.
  - At least 3 sections per defect should represent the whole defect.
  - Multiple stains (e.g. H&E, Masson's trichrome) should be used [fda2025dental].
  - The calcium-salt bone void filler guidance asks for radiography, histology and histomorphometry of bone formation and device resorption, plus supportive biomechanics [fda2003csbvf].
- **µCT-to-histology registration** is now practical:
  - elastic transformation of histological slices onto SRµCT [albers2021];
  - over 50 co-registered SRµCT/toluidine-blue pairs of bone implants, used to train virtual staining [irvine2025; no data availability statement].

---

## 7. Published methods for separating graft from new bone (micro-CT)

| Approach | Setting | Reported performance | Source |
|---|---|---|---|
| Global threshold on µCT vs histomorphometry | 111 human sinus biopsies grafted with DBB | Native bone: mineralised volume close to histology (threshold 90–240, r = 0.50). Grafted bone: no correlation (r = −0.028). Linear lengths agreed (r = 0.57–0.74) | [lima2022] |
| 3D µCT osteoconductivity index vs 2D histomorphometry | Human sinus biopsies, cerabone vs Bio-Oss | µCT material–bone contact systematically higher than 2D. The authors attribute this to µCT resolution not resolving the BSM–bone interface | [kapogianni2019] |
| Histogram thresholds + joint histology–SRµCT histogram | Human socket biopsies, BCP and others, SRµCT 25 keV | Intact BCP: three separable peaks. Degraded material separable only with the joint histogram | [stalder2014] |
| Gaussian mixture (4 classes: background, void, bone, scaffold) | Rabbit femoral condyle, 3D-printed CaP, 8 wk | Method published in code; accuracy vs histology not reported in the abstract | [raymond2022] |
| U-Net (3 loss functions) on scaffold + ingrown bone patches | Scaffolds with ingrown bone | Bias in bone growth fraction < 1.5 percentage points (Bland–Altman). Accuracy was the standard metric that best tracked the application error | [aboutaleb2026] |
| U-Net, multi-plane soft voting, 4 classes | Rat, Mg-5Gd/Mg-10Gd screws, SRµCT 1.2–2.4 µm resampled to 5 µm, 17 samples | IoU: bone 96.4–97.0, degradation layer 81.3, residual material 93.8–94.0. Data on request only | [baltruschat2021] |
| Comparison of U-Net / HR-Net / U²-Net / nnU-Net | Sheep tibia, ZX00 Mg screws, SRµCT (2.76/3.79 µm after binning), 6 train / 2 test | IoU/mIoU reported; prior sparse-annotation U-Net had Dice 0.541 for the corrosion layer. Data "will be made available by the authors" | [lopesmarinho2024; baltruschat2021] |
| µCT bone–implant contact vs histomorphometry | Rabbit tibia, Ti implants, 3 months | r = 0.855; needs calibration | [park2005] |
| Time-lapsed in vivo µCT with registration (formation / resorption) | Mouse in vivo loading | MAR vs histology R = 0.68, MS R = 0.78; reproducibility errors 0.9–6.6% | [schulte2011] |
| Registration of longitudinal in vivo µCT | Rat tibia | BV reproducibility error < 3%; Tb.Th error < 0.5% | [waarsing2004] |
| Multi-energy decomposition | Bone vs Pb contrast agent | > 95% decomposition accuracy | [granton2008] |
| Contrast-enhanced CT (Hf-POM) | Mouse long bones | Validated vs (immuno)histology for soft-tissue compartments | [kerckhofs2018] |

**Reading of the evidence.**

1. Every verified high-accuracy result either used a material with a large intensity contrast (intact BCP, metals) or a learned model trained on labelled scans of the same material and imaging setup (Mg on SRµCT, scaffold U-Net).
2. For bone-derived grafts, the only large verified comparison (n = 111) found no agreement between µCT and histology in grafted regions [lima2022].
3. Day-0 / time-lapse registration is the validated way to turn "which mineral is new" into change detection [schulte2011; waarsing2004]. We found no verified study that applies it specifically to graft vs new bone. Our own synthetic results (SCIENTIFIC_EVIDENCE.md R4) are not evidence about real tissue.

---

## 8. FDA guidance on preclinical evaluation (public documents)

**Resorbable calcium salt bone void filler, Class II special controls (June 2, 2003)** [fda2003csbvf]:

- An animal study is needed when the device does not share the predicate's critical specifications.
- Design: skeletally mature animals and a critical-size defect, in a model representative of the indications and anatomical sites.
- Controls: the predicate and/or autograft as positive controls; an empty defect as negative control.
- Assessments: radiography, histology and histomorphometry of bone formation and device resorption at relevant time points, plus supportive biomechanical testing.
- Duration: long enough to show healing and the effects of residual material.

**Animal studies for dental bone grafting material devices, 510(k) (final, August 22, 2025; docket FDA-2024-D-1242)** [fda2025dental]:

- Models: canine or porcine preferred over rodent.
- Group size: at least 3 animals per treatment and control group per time point; randomisation.
- Controls: a predicate or reference device, or autograft, as comparator, plus an empty CSD sham.
- CSD definition as in §1.2.
- Time points: e.g. 4, 8 and 12 weeks, plus 2 and/or 26 weeks where justified. The final time point need not show complete resorption.
- Endpoints: radiographic, histologic and histomorphometric data on bone formation, device resorption, residual material and degradation products.
- On micro-CT, the guidance:
  - recommends µCT for each animal at each time point;
  - requires validation of the modality, from a study or from the literature;
  - asks for a justification of the segmentation technique, which it calls "a critical step that can affect the interpretability and validity of microCT results";
  - asks for the same scan protocol across all samples;
  - asks for full reporting (system, calibration, medium, energy, filtration, voxel size, ROI, filtering, segmentation threshold between bone and device, artefact correction, metrics and algorithms);
  - names ASTM F2603 and ASTM F3259 (µCT of tissue-engineered scaffolds) as recognised standards for segmentation (not reviewed here).

**What this means for OsteoQuant's report.** The report should emit, by default, everything listed in the micro-CT reporting bullets above, together with:

- the segmentation method;
- its validation status for the specific material, from materials.json and the advisor;
- an explicit statement when graft vs bone separation was not validated.

This is a direct, sourced product requirement.

---

## 9. Findings that should change the product

1. **Refuse intensity-only "new bone" for bone-derived grafts.** This covers autograft, allograft, DBBM and remineralised DBM.
   - Evidence: same material by construction; DBBM grey values are similar to new bone [kapogianni2019]; no µCT–histology correlation in 111 DBB-grafted biopsies [lima2022].
   - Allowed outputs: total mineralised volume, or graft change vs day-0 with registration.
   - materials.json marks these `poor` and `bone_derived: true`.
2. **Treat calcium sulfate, composites and Mg as `poor` by intensity.**
   - Calcium sulfate: porous set CaSO4 is computed at ~1150 mgHA/cm³ eq [derived], inside the bone band, and it dissolves within 1–3 months [fernandezdegrado2018].
   - Composites: ceramic-filled polymer struts at 20 vol% read ~600 [derived].
   - Mg: ~630, and its corrosion layer is CaP-rich [witte2005].
   - Each needs day-0 registration, known geometry, or a learned model validated on labelled scans of that material.
3. **β-TCP and BCP are time-dependent.** Intensity works for intact granules (three peaks [stalder2014]) but fails as resorption proceeds. β-TCP was almost completely resorbed in 8 weeks in minipig [jensen2006]. The advisor should take the timepoint as an input and downgrade support after the early window unless a day-0 scan or a histology-calibrated model exists.
4. **Lock thresholds to the protocol for energy-dependent materials** (glasses, CaSO4, Mg). Never transfer thresholds across kVp or filtration [derived; nazarian2008; meganck2009].
5. **Bone–graft contact needs resolution.** Report BGC only when the voxel is small relative to granule size, and flag µCT BGC as likely overestimated [kapogianni2019].
6. **Characterise every new material.** Scan it alone with the study protocol and an HA phantom before measuring. See `unsupported_material_workflow` in materials.json. The FDA guidance requires the µCT modality and segmentation to be validated and justified [fda2025dental].
7. **Default report contents** must cover the FDA µCT reporting list (§8) and the Bouxsein minimal methods (§5).
8. **Do not report SMI** as rod/plate morphology [salmon2015].

---

## 10. Known gaps (not resolved by this review)

- **Densities and porosities.** Measured granule porosities for commercial products are not sourced. Dihydrate CaSO4 density, glass density, and the PCL and PLGA densities are handbook values marked `assumption`.
- **TMD of new bone.** No verified source gives a species- and time-specific woven-bone TMD series in mgHA/cm³. The 641.9 mgHA/cm³ callus threshold [morgan2009] is a segmentation choice, not a distribution.
- **Day-0 registration.** No verified real-tissue study quantifies day-0-registered residual graft against histology.
- **Open data.** No open dataset with voxel labels for graft vs new bone was found. See `docs/research/DATASET_DISCOVERY_R2.md`.
