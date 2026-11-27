# Separability Analysis: Can Micro-CT Tell New Bone from Graft from Host Bone?

Status: v1, 2026-11-27. Evidence tags: [RF], [RF-derived], [PK], [UNR], [ASSUMPTION]. References are in `REFERENCES.md`. The density values come from `MICROCT_IMAGING_SCIENCE.md` §3 and `phantom_parameters.json`.

---

## 1. Framework

OsteoQuant must assign each mineralized voxel to {host bone, new bone, residual graft}. Each voxel has four sources of evidence:

1. **Intensity (I):** calibrated HA-equivalent density, and its energy dependence where dual-energy data exist.
2. **Morphology (M):** local thickness, shape, texture, granule geometry, lattice periodicity, core–rim structure.
3. **Spatial/temporal context (C):**
   - position relative to the defect boundary and host bone
   - day-0 / longitudinal registration
   - timepoint prior (expected residual graft fraction)
4. **External ground truth (H):** co-registered histology, SRμCT, labelled donors.

### 1.1 Decision categories

| Category | Definition |
|---|---|
| **EASY** | I alone separates the classes. Distributions overlap by less than about 5% after PVE, at typical voxel sizes [ASSUMPTION criterion] |
| **HARD** | I overlaps substantially. M and/or C can recover separation with quantifiable uncertainty |
| **UNDERDETERMINED** | The classes are the same material, or the same density and similar morphology. No μCT-only information identifies the class. Any μCT-only answer is a prior, not a measurement, and must be reported as such |

### 1.2 Intensity overlap is governed by three physical facts

1. **Contrast exists only when the graft's density or chemistry differs from bone mineral.** CaP ceramics are chemically HA-like, so their contrast depends entirely on packing density. Glasses, CaSO4, and Mg differ in chemistry, so their contrast is energy-dependent [RF-derived, §3 imaging doc].
2. **New bone is a moving target.** Its TMD starts low and rises with maturation, plausibly from about 600 to above 1000 mg HA/cm³. The 642 mg HA/cm³ callus "mineralized" threshold corresponds to about 45% of cortical attenuation [RF: Morgan 2009, R21]. The woven-bone values themselves are an [ASSUMPTION] anchored to this; see the JSON.
3. **Partial volume creates intermediate values at every interface.** A dense granule next to soft tissue produces a rim at bone-like values [RF-derived simulation; observed for xenograft, Kapogianni 2019, R14].

---

## 2. Per-material separability matrix

Densities are mg HA/cm³ equivalent; the energy range is 30–60 keV effective unless stated.

| Graft | Graft density at implantation | vs early woven bone (≈ 400–800) [ASSUMPTION] | vs mature/host bone (≈ 900–1200) [RF: R23] | Verdict: early (≤ 4 wk) | Verdict: late (≥ 12 wk) | Key extra information |
|---|---|---|---|---|---|---|
| Sintered dense HA granules/blocks | 1300–3160 (micro-porosity-dependent) [RF-derived] | Large contrast | Large contrast if solid fraction > 0.5 | **EASY** (except edge halo) | **EASY–HARD**: HA persists for years [RF: R32] but bone grows into micro-pores and the edge halo grows with the bone–HA contact area | PVE-aware edge model; voxel ≤ ¼ granule size |
| Nanocrystalline / highly microporous HA (e.g. HA-SiO) | Possibly ~1000–1600 [ASSUMPTION: solid fraction 0.3–0.5] | Moderate | Small | **HARD** | **HARD** | Granule morphology, day-0 registration (slow resorption: minipig filler 34.5% → 31.2% from 2 to 8 wk [RF: R41]) |
| β-TCP | 1200–3030 (porosity-dependent) [RF-derived] | Large when intact | Moderate | **EASY** | **HARD**: partially resorbed, micro-porous TCP overlaps remodelling bone, and bone apposes directly on TCP [RF: R30 for BCP; PK for TCP] | Day-0 registration + resorption model (CaP replacement 3–36 mo [RF: R32]); granule-shape priors; histology calibration subset |
| BCP (HA/β-TCP) | Intact granules ≈ 7.5 cm⁻¹ vs new bone ≈ 3.8 cm⁻¹ at 25 keV SRμCT, i.e. about 2× [RF: R30] | Large | Large when intact | **EASY** (three clear histogram peaks [RF: R30]) | **HARD**: "partially degraded augmentation material … overlaps the preliminary phase of bone"; separated only with the joint histology–μCT histogram [RF: R30] | Joint histogram with histology; HA-skeleton morphology |
| Calcium sulfate | Dihydrate ≈ 1640–1720; anhydrite ≈ 2615–2680 [RF-derived] | Moderate–large | Moderate | **EASY–HARD** (dense pellets easy; dissolving fronts grade into bone) | Mostly moot: "rapid and complete resorption" [RF: R36]. Remaining mineral is likely new bone [PK] | Timepoint prior (resorption within weeks [PK]); smooth featureless texture vs trabecular pattern; HA co-phase in composite products |
| Bioactive glass 45S5 / S53P4 | 1515–1850 (energy-dependent) [RF-derived] | Moderate | Small–moderate (ratio 1.4–1.65) | **EASY–HARD** (cores separable; reaction rim not) | **HARD**: Ca-P (HCA) reaction layer and bonded bone sit at the glass surface [PK mechanism, R37] | Core–rim morphology; kVp-specific calibration; **dual-energy** exploits Na/Si vs Ca/P differences [PK]; SEM-EDS/histology |
| DBM (with or without carrier) | ≈ 0–100 (residual mineral 1–6% [RF: R39] → small [RF-derived]) | DBM ≈ soft tissue | — | **EASY** in the trivial sense (DBM is invisible, so all mineral = new bone, unless the carrier is CaSO4 or similar [RF: R39]) | **UNDERDETERMINED**: mineralized/incorporated DBM particles vs new bone cannot be told apart by μCT | Histology (acellular particles, empty lacunae); state "mineral in defect" rather than "new bone" |
| Mineralized allograft (FDBA, cortical chips) | ≈ host bone (same material) [RF-derived] | Moderate (allograft more mineralized than woven bone) [PK] | **None** | **HARD** (TMD prior vs woven bone + chip geometry) | **UNDERDETERMINED** (remodelled bone vs residual allograft) | Day-0 registration; histology (empty lacunae, cement lines) |
| Autograft | ≈ host bone [RF-derived] | Small–moderate | **None** | **UNDERDETERMINED** | **UNDERDETERMINED** | Day-0 registration of graft chips; histology. Note that autograft is rapidly substituted (filler 17% → 9% from 2 to 8 wk [RF: R41]) |
| DBBM xenograft (Bio-Oss) | ≈ bone tissue (deproteinized bone mineral; inference [PK]) | Small–moderate (DBBM brighter than early woven bone) | **≈ none**: "similar gray values" [RF: R14] | **HARD** | **UNDERDETERMINED by I.** Recoverable with C: DBBM is essentially non-resorbing (no size change 6 mo → 11 yr [RF: R40]), so a day-0 mask stays valid | Day-0 scan registration (strongest); granule morphology (trabecular-pattern particles with sharp fracture faces); histology |
| Sintered bovine HA (cerabone) | Possibly denser than DBBM (1250 °C sintering [RF: R14]) [PK] | Moderate | Small–moderate | **HARD** | **HARD** | As DBBM, with somewhat better intensity contrast [PK] |
| Composite polymer/CaP scaffold | ≈ φ_ceramic × 3030 (e.g. 20 vol% → ≈ 600) [RF-derived] | **None** (same band) | Moderate | **HARD** | **HARD/UNDERDETERMINED** | Known print geometry (lattice periodicity); day-0 registration; polymer is invisible |
| Mg alloy implant | ≈ 630–780 (energy-dependent) [RF-derived] | **None** (same band) | Moderate (Mg darker than mature bone) | **HARD** | **HARD**: the CaP-enriched corrosion layer is bone-like [RF: R42]; gas voids | Known CAD geometry + registration; gas-void detection; dual-energy (Mg K-edge is too low to help at μCT energies, but the Z difference from Ca helps) [PK] |

### 2.1 Host bone vs new bone (all models)

- **Calvarial defects:** **EASY by geometry.** The defect edge is a well-defined cylinder from the trephine. New bone inside it is new [RF: defect definition R13]. The exception is bone growing in from the edges: margin voxels need a tolerance band (e.g. ±1–2 voxels) [ASSUMPTION].
- **Condylar and metaphyseal cancellous defects:** **HARD.** Host trabecular bone surrounds the defect, and new bone that has remodelled to lamellar density is indistinguishable by I. Use the drilled-cylinder geometry from day-0 or immediate post-op scans, plus TMD and texture differences in the first weeks [ASSUMPTION/PK].
- **Segmental long-bone defects:** **MODERATE.** The cortical ends are identifiable. Periosteal callus outside the original bone envelope is new by definition.

---

## 3. What additional information helps, ranked by expected value

1. **Day-0 (post-implantation) μCT with deformable/rigid registration to later timepoints.**
   - Turns graft identification into change detection: graft present at day 0 and still present later = residual graft; mineral newly present = new bone; mineral lost = resorption.
   - Most valuable for slowly resorbing materials (DBBM, HA), where the day-0 mask stays valid [RF basis: R40, R32]. It also allows Gr.V/Gr.V0.
   - Limitations: bone deposited *on* graft surfaces is spatially adjacent (partial-volume mixing), and dense grafts shift with swelling or settling (needs non-rigid registration) [PK].
2. **Material- and timepoint-specific priors.**
   - Expected residual fraction vs time: e.g. minipig mandible filler at 2 and 8 wk, DBBM 35.7% → 31.6%, BCP 23.6% → 23.7%, autograft 17.1% → 9.3% [RF: R41]; CaSO4 near zero within weeks to a few months [PK]; DBBM near-constant for years [RF: R40].
   - These priors enter a Bayesian classifier as class probabilities and are reported transparently.
3. **Morphology.**
   - Granule shape (angular, spheroidal, sintered-neck), known granule size distribution (e.g. 0.25–1 mm [UNR]), printed lattice periodicity, glass core–rim structure.
   - Trabecular texture: woven bone is irregular and thick-walled at early times [PK]. At ≤ 5 µm voxels, lamellar vs woven or osteocyte-lacuna patterns may be visible [PK].
4. **Co-registered histology on a calibration subset.**
   - Stalder 2014: the joint histology–SRμCT histogram identified "newly forming bone … and bone augmentation material … that cannot be extracted based on the histogram of the histology or the tomography slice alone" [RF: R30].
   - Use histology to fit per-material intensity/morphology likelihoods for each study (Q4 tier).
5. **Dual- or multi-energy μCT.**
   - Exploits effective-Z differences: Na/Si glass, S in CaSO4, Mg alloys vs Ca/P bone. Our table shows energy-dependent HA equivalents for these materials but flat values for CaP [RF-derived].
   - It **cannot** separate CaP ceramics or DBBM from bone, which are chemically identical apart from density.
6. **Higher resolution or SRμCT.** Reduces PVE halos and resolves micro-porosity and lacunae. SRμCT at about 4.4 µm resolution separated three phases for intact BCP [RF: R30].
7. **Ex vivo contrast agents and staining** (e.g. heavy-metal staining for soft-tissue/osteoid). Not reviewed here [PK].

---

## 4. Reporting rules for OsteoQuant

1. Always report **total mineralized volume in the defect** (bone + graft). It is robust and needs no class assignment.
2. Report class-specific volumes **with a separability label** (EASY / HARD / UNDERDETERMINED) and a confidence interval (e.g. from threshold sensitivity ±5–10%, as in Leong & Morgan's sensitivity analysis approach [RF: R22]).
3. For UNDERDETERMINED cases, never output "new bone volume" as a measurement. Output either "mineralized tissue volume", or a "model-based estimate" with the prior stated explicitly.
4. Report μCT bone–graft contact (BGC) only when the voxel is ≤ ¼ of the median granule size and an edge-halo correction has been applied. Otherwise flag it as likely overestimated [RF basis: R14].
5. Record the timepoint and material in metadata. The separability verdict depends on both.

---

## 5. Implications for the synthetic phantom generator

The phantom must generate cases spanning all three categories, with ground-truth labels, so the segmentation model's failure modes are measurable.

- **EASY cases:** intact dense HA/BCP granules at early timepoints.
- **HARD cases:**
  - Resorbing β-TCP or BCP with surface erosion, micro-porosity growth, and fragmentation, with new bone apposed directly on the surfaces.
  - Glass with a reaction rim.
  - Mg with a corrosion layer and gas.
  - Composites.
- **UNDERDETERMINED cases:**
  - DBBM or allograft whose density distribution is drawn from the *same* distribution as mature bone.
  - The model should be evaluated on whether it **abstains or flags** these cases, not on whether its accuracy exceeds chance.
- **PVE halo:** blur after labelling.
- **Scanner personalities:** grey scaling, BH, ring, noise.
- **Timepoint-dependent new bone TMD:** early ≈ 400–800, mid ≈ 700–1000, late ≈ 900–1200 [ASSUMPTION anchored to R21, R23].
