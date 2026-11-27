# Bone Biology, Defect Models and Graft Materials: Knowledge Base for OsteoQuant

Status: v1, 2026-11-27. Audience: engineering (segmentation, phantom generator), science advisors, regulatory/QA.

Citation keys [Rn] refer to `REFERENCES.md`. Evidence tags:

- **[RF]**: read in the cited source (abstract or full text) during this review.
- **[RF-derived]**: computed by us from cited reference data. The method is stated.
- **[PK]**: the author's prior knowledge, standard in the field, but not re-verified against a primary text in this review.
- **[UNR]**: unresolved or not verified (e.g. seen only in a search snippet).
- **[ASSUMPTION]**: an engineering placeholder with no direct literature value.

> **Limitation of this review.** The shared web-search budget ran out partway through. Later facts were verified by DOI lookup (Europe PMC / Crossref) and direct fetches of open-access full texts only. Several numbers that would normally have a primary citation are therefore marked [PK] and should be checked in a follow-up pass. They are listed in §9.

---

## 1. Bone anatomy and microarchitecture

### 1.1 Cortical vs trabecular bone

- **Cortical (compact) bone:**
  - Dense outer shell of long bones and the inner/outer tables of the calvaria.
  - Porosity is low: Haversian/Volkmann canals and, in rodents, few or no osteons [PK].
  - Rodent cortical bone is largely primary lamellar bone without secondary osteonal remodelling [PK]. This matters because cortical porosity (Ct.Po) in rats and mice is much lower and structurally different from human or sheep bone.
- **Trabecular (cancellous) bone:**
  - A lattice of plates and rods in metaphyses, epiphyses, vertebral bodies, and the diploë of flat bones.
  - The marrow-filled spaces are what make trabecular BV/TV, Tb.Th, Tb.Sp, and Tb.N measurable.
- **Bone tissue mineral density:**
  - Human trabecular bone measured with ash gravimetry is about 1250–1300 mg HA/cm³.
  - Synchrotron μCT gives about 1150–1160 mg HA/cm³.
  - Conventional desktop μCT underestimates it at about 940–1030 mg HA/cm³ [RF: Kazakia 2008, R23].
  - The bone material has a characteristic mineralization density distribution (BMDD) that reflects matrix age and turnover. In healthy individuals its biological variance is remarkably small [RF: Roschger 2008, R57].

### 1.2 Typical trabecular microarchitecture by species

| Species / site | BV/TV | Tb.Th | Tb.Sp | Tb.N | Evidence |
|---|---|---|---|---|---|
| Mouse, C57BL/6 male 12 wk, distal femoral epiphysis | 8–12% | **21–63 µm depending on scanner** (Scanco µCT35 ≈ 37–45 µm; SkyScan 1172 ≈ 50–63 µm; GE Locus ≈ 21–29 µm) | 0.23–0.29 mm | 1.5–4.0 mm⁻¹ | [RF: Verdelis 2011, R26, Table 3] |
| Mouse, general | — | ≈ 40 µm | — | — | [RF: Kim 2021, R7] |
| Mouse, C57BL/6J, age effects | BV/TV peaks at 6–8 wk and then declines (more in females); Tb.N falls rapidly from 2–6 mo; Tb.Th rises slowly with age | | | | [RF: Glatt 2007, R55] |
| Rat (≈0.3–0.5 kg) | [PK] 15–35% (proximal tibia/distal femur metaphysis, young adult) | **≈ 100 µm** allometric estimate [RF-derived, R54]; [PK] 70–110 µm measured | [PK] 150–400 µm | [PK] 2–5 mm⁻¹ | |
| Rabbit (≈3–4 kg) | [PK] 20–40% (femoral condyle) | **≈ 140 µm** allometric estimate [RF-derived, R54]; [PK] 100–200 µm | [PK] 300–600 µm | [PK] 1.5–3 mm⁻¹ | |
| Sheep (≈60–80 kg) | [PK] 25–45% (distal femur/proximal tibia) | **≈ 220 µm** allometric estimate [RF-derived, R54]; [PK] 150–250 µm | [PK] 400–900 µm | [PK] 1–2 mm⁻¹ | |
| Human (femoral head, L2/L4, iliac crest, calcaneus; 260 biopsies from 52 donors) | [PK] ≈ 8–26% depending on site (vertebra lowest, femoral head highest) | [PK] ≈ 120–190 µm (direct 3D); allometric ≈ 220 µm [RF-derived] | [PK] ≈ 600–900 µm | [PK] ≈ 1–2 mm⁻¹ | Hildebrand 1999 [R56] (study design and the finding that low bone mass = lower plate-to-rod ratio and, to a lesser extent, thinner elements are [RF]; the site values are [PK]) |

**How the allometric estimate was derived [RF-derived]:**

- Doube et al. 2011 [R54] analysed femoral heads and condyles of 90 species from 3 g to 3400 kg.
- **Findings:**
  - BV/TV is essentially size-independent.
  - Tb.Th scales with body mass as Mb^0.155 (mammals).
  - Tb.Sp scales as Mb^0.147.
  - Conn.D scales as Mb^−0.486.
- **Anchor values:** shrew-sized trabeculae of about 0.052 mm (≈5 g) and elephant Tb.Th of 0.511 mm (≈3400 kg).
- **Formula:** Tb.Th ≈ 0.052 mm × (Mb/0.005 kg)^0.155, which gives:
  - mouse (25 g) ≈ 67 µm
  - rat (400 g) ≈ 102 µm
  - rabbit (3.5 kg) ≈ 143 µm
  - sheep (60 kg) ≈ 223 µm
  - human (70 kg) ≈ 226 µm
- This is an interspecies trend line. Individual sites can deviate by up to 2×: the mouse femoral epiphysis measures about 40 µm against an allometric 67 µm. **Phantom design should sample around measured values where available and use the allometric line only as a fallback.**

**Cross-scanner warning [RF]:** Verdelis 2011 [R26] measured the same mouse femora on three systems. Tb.Th differed by up to 236% and Tb.N by up to 218%. BV/TV and Tb.Sp were similar. The authors concluded that trabecular morphometry "should not be directly compared across microCT systems." This is central to the OsteoQuant value proposition: a harmonized pipeline.

### 1.3 Intramembranous vs endochondral ossification

- **Intramembranous ossification:**
  - Mesenchymal cells differentiate directly into osteoblasts without a cartilage template.
  - It forms the calvaria and most of the craniofacial skeleton [PK]. Rat calvarial defects therefore heal (if at all) mainly intramembranously, from the defect margins and the dura/periosteum [PK].
- **Endochondral ossification:**
  - A cartilage anlage or callus is formed, hypertrophies, mineralizes, is resorbed, and is replaced by bone.
  - This is typical of long bones and of fracture calluses under relative instability [RF: Einhorn & Gerstenfeld 2015, R45; Marsell & Einhorn 2011, R46].
- **Woven bone first:**
  - Woven bone is laid down first in both pathways. Mesenchymal osteoblasts "surround themselves circumferentially with collagen in a random array". Surface osteoblasts then deposit parallel-fibred lamellar bone on the woven scaffold.
  - Woven bone "initiates formation de novo at sites of no previous bone" [RF: Shapiro & Wu 2019, R58].
  - Woven bone has randomly oriented collagen and is less mineralized than mature lamellar bone. The second point is [PK]: Shapiro & Wu's abstract gives no mineral values.
- **Imaging consequence:**
  - Mineralizing calluses and new bone in defects show a broad spread of TMD that rises over time.
  - In μCT histograms the "newly formed bone with a variety of mineralization stages" forms a poorly defined peak between soft tissue and mature bone [RF: Stalder 2014, R30].

### 1.4 Fracture healing phases

- **Direct (primary) healing:** occurs only under anatomical reduction and rigid stability. Lamellar bone and Haversian systems regenerate directly, with no callus [RF: Marsell & Einhorn 2011, R46].
- **Indirect (secondary) healing:** the common pathway. It combines intramembranous (periosteal) and endochondral bone formation [RF: R46].
- **Classical four overlapping stages** (Schindeler 2008 [R47], RF):
  1. inflammation
  2. soft callus
  3. hard callus / bony union
  4. remodelling
- **Anabolic/catabolic view [R47]:** two catabolic phases are distinguished: removal of the cartilaginous soft callus, then remodelling of the bony hard callus.
- **Einhorn & Gerstenfeld [R45, RF]** frame healing as an anabolic phase followed by a catabolic phase, with three stages: inflammatory, endochondral bone formation, and coupled remodelling.
- **Rodent timing:**
  - Figure timepoints [RF from R45]: 24 h = inflammatory; day 3 = late inflammatory with early vessels; day 14 = late endochondral with osteoclast recruitment; 21-day transcriptomic window.
  - Typical rodent ranges [PK]: inflammation days 0–5, soft callus days 5–14, hard callus days 14–28, remodelling from week 4 to months.
- **Remodelling:** coupled osteoclast–osteoblast activity in five phases: activation, resorption, reversal, formation, termination [RF: Raggatt & Partridge 2010, R48].
- **Callus μCT** [RF: Morgan 2009, R21; Morgan 2014, R8]:
  - Timepoint differences in mouse calluses were associated most strongly with changes in TMD.
  - Typical global callus threshold: 25% of maximum grey value = 641.9 mg HA/cm³ on a Scanco µCT40 at 70 kVp. This was stated to be about 45% of mature cortical attenuation.
  - Suggested voxel sizes: about 12 µm for mouse calluses and about 16 µm for rat.

### 1.5 Osteogenesis, osteoconduction, osteoinduction, osseointegration

Definitions follow Albrektsson & Johansson 2001 [RF, R49, abstract].

- **Osteogenesis:** new bone formed by living osteoprogenitor cells present in the graft. Only autograft and cell-seeded constructs have this property [PK].
- **Osteoinduction:** "the process by which osteogenesis is induced". It "implies the recruitment of immature cells and the stimulation of these cells to develop into preosteoblasts" [RF]. An example is BMPs in DBM. The standard test is ectopic (muscle pouch) bone formation [RF: Gruskin 2012, R39].
- **Osteoconduction:** "bone grows on a surface" [RF]. Most ceramics and xenografts are osteoconductive, and β-TCP is also reported to be osteoinductive [RF: Bohner 2020, R33].
- **Osseointegration:** "the stable anchorage of an implant achieved by direct bone-to-implant contact" [RF]. In μCT around metal implants this is assessed as bone-implant contact (BIC) or peri-implant BV/TV [PK].

### 1.6 Graft resorption and creeping substitution

- **Calcium phosphates:** resorbed by osteoclast-mediated (cell-mediated) and solution-mediated dissolution [RF: β-TCP "cell-mediated resorption", R33].
  - Solubility: β-TCP (−log Ksp ≈ 29.5 at 37 °C) is far more soluble than HA (−log Ksp ≈ 117) [RF: Eliaz & Metoki 2017, R32].
  - "Implants made of pure HAp often remain in the body for several years" [RF, R32].
  - CaP replacement by bone may take "3 to 36 months" [RF, R32].
- **Calcium sulfate:** "rapid and complete resorption without eliciting a significant inflammatory response" [RF: Thomas & Puleo 2009, R36].
- **Allograft / DBM:** remodelled by creeping substitution. Osteoconductive replacement of graft by host bone is "very slow" and may need years to unite a large segmental defect [RF: Gruskin 2012, R39].
- **Deproteinized bovine bone mineral (DBBM):** essentially non-resorbing over a decade in humans. Particle length and area showed no significant change between 6 months and about 11 years [RF: Mordenfeld 2010, R40].

### 1.7 Tissue-engineering scaffolds

- **Pore size [RF: Karageorgiou & Kaplan 2005, R44]:**
  - The minimum pore size is about 100 µm (cell size, migration, transport).
  - Pores larger than 300 µm are recommended for enhanced bone formation and capillary formation.
  - Small pores favour hypoxia and osteochondral formation before osteogenesis. Large, well-vascularized pores lead to direct osteogenesis.
- **Typical scaffold families:**
  - sintered CaP foams
  - 3D-printed CaP or bioactive glass lattices
  - polymer (PCL, PLGA) or polymer–ceramic composites
  - hydrogels (alginate, collagen) loaded with BMP-2 or cells
- **μCT relevance [PK]:** Polymer components are effectively radiolucent, close to soft tissue or water. Only the ceramic/glass phase and the mineralized tissue are visible.

---

## 2. Critical-size defect models

| Model | Typical dimensions | Notes | Evidence |
|---|---|---|---|
| Rat calvaria, single central | **8 mm** trephine; calvarial thickness ≈ 1 mm; skeletally mature (e.g. Fisher 344, 11–12 wk) | "8 mm is generally accepted to be of critical size". Harvest 4–12 wk. Empty defects fill with only ≈5–15% mineralized volume by μCT. Bridging score in Fig. 4 | [RF: Spicer 2012, R13] |
| Rat calvaria, bilateral | **5 mm** × 2 | A systematic review (61 papers) concluded that 5.0 mm defects "could be considered as a CSD". Mean %new bone: 5 mm central ≈ 18% (1 mo) and 21% (3 mo); 8 mm single ≈ 10%/13%/8% (1/2/3 mo). Heterogeneity is high | [RF: Vajgel 2014, R51] |
| Critical size: definition | Smallest defect that will not heal completely over the animal's natural lifetime; many studies use an experimental endpoint instead | | [RF: R13; concept from Schmitz & Hollinger 1986, R50] |
| Mouse calvaria | 4 mm, bilateral (nu/nu) | Assessed at about 5–8 wk | [RF: Li 2015 review, R53] |
| Rabbit calvaria | 10 mm × 1.2 mm; 9 mm. [PK] 15 mm single midline defects are also used | | [RF: R53 Table 1] |
| Rabbit femoral condyle (lateral, cancellous, partially load-bearing) | 6 mm Ø × 5 mm cylinder; 7 × 10 mm; 3 mm × 15 mm tunnel (osteonecrosis model). Literature commonly uses **5–6 mm Ø × ~10 mm deep** [PK] | Cancellous metaphyseal model. Graft surrounded by host trabecular bone, which makes host-vs-new bone separation hard | [RF: R53] |
| Rabbit ulna/radius segmental | 12–15 mm mid-shaft | | [RF: R53] |
| Sheep tibia segmental | 18 mm (external fixator) [RF: R53]. [PK] 30 mm (≈ 2–2.5× diameter) is the common critical-size segmental model | Segmental deficiency of more than 2–2.5× bone diameter is considered critical. "No mineralised area ≥30% after 52 weeks" is used as a criterion | [RF: R53]; review of models [R52] |
| Sheep vertebral body void | 8 mm Ø × 15 mm | | [RF: R53] |
| Minipig mandible / tibia | 10 mm × 10 mm craniofacial; 11 mm × 25 mm tibial | Broggini 2015 compared filler and new bone in minipig mandibular defects | [RF: R53, R41] |

**Imaging implications [PK/ASSUMPTION]:**

- **Calvarial defects** are thin, about 1 mm in rats, and essentially 2.5D. Partial volume at the upper and lower surfaces is significant. Host-bone margins are clear, so defect ROIs can be defined geometrically from the trephine.
- **Condylar and metaphyseal defects** sit inside host trabecular bone. The defect boundary must be registered (ideally from a day-0 scan), or new trabecular-like bone cannot be distinguished from host trabeculae.
- **Segmental defects** usually carry metal fixation (plates, nails), which causes beam-hardening and streak artifacts (see the imaging doc).

---

## 3. Graft materials: per-material profiles

### Reading the density numbers

- **Bone tissue reference:** Calibrated μCT measures mineralized bone tissue at roughly 900–1200 mg HA/cm³ (Kazakia 2008 [R23]: 940–1030 by desktop μCT, about 1150 by SRμCT, about 1250–1300 ash).
- **Physical reasoning for ceramics:**
  - A fully dense ceramic made of HA is by definition 3150–3160 mg HA/cm³ (HA density 3.155 g/cm³ [RF: R32]).
  - Any sub-voxel micro-porosity scales the apparent value down linearly with solid fraction.
  - Macro-pores larger than about 2–3 voxels are resolved as separate soft-tissue/void regions.
- **Our attenuation calculation [RF-derived]:**
  - Linear attenuation μ(E) was computed for each material from the NIST mass-attenuation tables [R59] and expressed as an *HA-equivalent density*.
  - This is the value a scanner calibrated with HA-in-resin phantoms would report under ideal monoenergetic conditions.
  - Full table and method: `MICROCT_IMAGING_SCIENCE.md` §3.

### 3.1 Autograft (autologous bone)

| Property | Content |
|---|---|
| Composition | Patient's own cortical and/or cancellous bone, often particulate (chips/bone mill) [PK] |
| Biology | Osteogenic, osteoinductive, osteoconductive; the "gold standard" [RF: Bouler 2017, R35] |
| Physical | Identical to host bone: TMD ≈ 900–1200 mg HA/cm³ (desktop μCT) [RF: R23]. Cancellous chips 1–5 mm [PK] |
| μCT appearance | Bone-like fragments with sharp, angular margins and an initially devitalized structure. No intensity contrast to host bone [RF-derived: same material] |
| Degradation | Rapid substitution. Minipig mandible: filler fraction 17.1% at 2 wk and 9.3% at 8 wk, vs 31–36% for DBBM and HA-SiO [RF: Broggini 2015, R41]. Remodelled by creeping substitution |
| Histology | Empty osteocyte lacunae in necrotic graft fragments vs populated lacunae in new bone; reversal lines; woven bone apposition [PK] |
| Endpoints | %new bone, %residual graft, % marrow (histomorphometry); μCT total BV/TV |
| Separation | **Underdetermined by intensity.** Only morphology (angular fragments, lamellar vs woven texture at ≤ 5 µm), day-0 registration, or histology (empty lacunae) can separate graft from new bone |

### 3.2 Hydroxyapatite (HA, Ca10(PO4)6(OH)2), sintered synthetic

| Property | Content |
|---|---|
| Density | Theoretical 3.155 g/cm³; Ca/P 1.67; −log Ksp 117.2 (37 °C) [RF: Eliaz & Metoki 2017, R32] |
| Forms | Dense or porous granules (≈ 0.25–2 mm [PK]); porous blocks; 3D-printed lattices; nanocrystalline HA (e.g. HA-SiO [RF: R41]) |
| Porosity | Macro 100–500 µm (designed) plus micro < 10 µm (sintering-dependent) [PK]. Pores > 300 µm recommended [RF: R44] |
| μCT appearance | **Radiopaque; brighter than bone when dense.** Dense HA → about 3160 mg HA/cm³ equivalent, ≈ 2.8× cortical bone (ICRU cortical bone ≈ 1100–1170 at 30–60 keV) [RF-derived, R59]. Jang 2017: granular HA "intrinsic density … as high as that of cortical bone", and "BMD and bone volume fraction … can be over-estimated depending on the characteristics of bone substitutes" [RF: R31]. With 50–60% sub-voxel micro-porosity, apparent density falls to about 1260–1580, overlapping dense mature bone [RF-derived] |
| Degradation | Very slow: "implants made of pure HAp often remain in the body for several years" [RF: R32]. Minipig: HA-SiO filler 34.5% (2 wk) → 31.2% (8 wk), i.e. essentially stable [RF: R41] |
| Histology | Acellular, non-staining (or dark) granules in decalcified sections, or ghost spaces where the material has been lost. Bone apposition directly on surfaces (osteoconduction); multinucleated giant cells at surfaces [PK] |
| Endpoints | %new bone, %residual material, bone-to-material contact, BV/TV (μCT, often combined bone+graft) |
| Separation | **Easy when the granules are dense/sintered and the voxel is small relative to granule size.** Bimodal histogram with HA ≫ bone. **Harder** for nano-/micro-porous HA, at granule edges (partial volume creates a bone-like rim), and for thin struts (< 3 voxels) |

### 3.3 β-Tricalcium phosphate (β-TCP, Ca3(PO4)2)

| Property | Content |
|---|---|
| Density | 3.067 g/cm³; Ca/P 1.5; −log Ksp 29.5 (37 °C) [RF: R32] |
| Forms | Granules (≈ 0.1–3 mm [PK]); porous blocks (typical total porosity 60–80% [PK]); printed scaffolds; cement-derived TCP |
| Biology | Osteoconductive and also osteoinductive, with **cell-mediated resorption** that allows full defect regeneration. Clinical outcome is sometimes "unpredictable", plausibly due to variable physico-chemistry: grain size and porosity are strongly modified by trace β-CPP or HA impurities [RF: Bohner 2020, R33] |
| μCT appearance | Dense β-TCP ≈ 3030 mg HA/cm³ equivalent, ≈ 96% of HA and almost energy-independent, because chemistry and the Ca fraction are similar [RF-derived, R59]. **At implantation, porous β-TCP granules are typically brighter than bone.** As resorption proceeds, granules become fragmented, thinned, and micro-porous, and their apparent density drops into the bone range [PK + RF-derived] |
| Degradation | Months to a few years. CaP replacement by bone "3 to 36 months"; TCP dissolves faster than HA [RF: R32]. Degradation is cell-mediated plus dissolution [RF: R33] |
| Histology | Granules with osteoclast-like cells and resorption bays; woven bone deposited directly on granule surfaces; residual granule fragments enclosed in bone [PK] |
| Separation | **Easy at early timepoints** (day 0–4 wk, intact granules). **Hard at mid/late timepoints**: remodelling bone and partially resorbed TCP have overlapping intensity, and new bone forms in direct contact with TCP. Stalder 2014 (SRμCT, 25 keV): partially degraded biphasic HA/TCP "overlaps the preliminary phase of bone" in the μCT data, and only the joint histology–μCT histogram separated them [RF: R30] |

### 3.4 Biphasic calcium phosphate (BCP; HA + β-TCP)

| Property | Content |
|---|---|
| Composition | HA/β-TCP ratios such as 60/40, 20/80, 70/30. Resorbability "is dependent on the β-TCP/HAp ratio" [RF: R32]. HA/TCP ratio, dual porosity, and interconnected architecture control progressive resorption and substitution [RF: Bouler 2017, R35] |
| Density | Mixture of 3.155 and 3.067 g/cm³ → about 3.1 g/cm³ fully dense [RF-derived] |
| Forms | Granules (e.g. 0.5–1 mm [PK]; easy-graft granules about 600 µm with PLA coating [RF: R30]); blocks (macro-pores 300–600 µm [PK]) |
| μCT appearance | SRμCT at 25 keV [RF: R30]: soft tissue/embedding ≈ 1 cm⁻¹, newly formed bone ≈ 3.8 cm⁻¹, BCP augmentation material ≈ 7.5 cm⁻¹. That is ≈ 2× new bone; dense HA at 25 keV would be ≈ 11 cm⁻¹ [RF-derived], so the clinical granules had about 30% sub-resolution porosity or partial degradation [inference] |
| Degradation | TCP phase preferentially resorbed; HA phase persistent [PK]. Minipig BCP 60/40: filler 23.6% at both 2 and 8 wk, new bone 40.2% at 8 wk [RF: R41] |
| Separation | **Easy for intact granules** (three clear peaks). **Mixed later**: the TCP-depleted HA skeleton retains contrast, while degrading/microporous zones overlap with new bone [RF: R30] |

### 3.5 Calcium sulfate (CaSO4·½H2O → CaSO4·2H2O)

| Property | Content |
|---|---|
| Composition | Implanted as hemihydrate (plaster of Paris) that sets to dihydrate (gypsum), or as pre-set pellets/beads; antibiotic-loaded beads are common [RF: Thomas & Puleo 2009, R36, "vehicle to deliver antibiotics"]. Anhydrite density 2.96 g/cm³ [RF: NIST, R59]; dihydrate ≈ 2.32 g/cm³ [PK] |
| μCT appearance | Dihydrate ≈ 1640–1790 mg HA/cm³ equivalent; anhydrite ≈ 2610–2730. Both rise with energy because of S (Z = 16) [RF-derived, R59]. So freshly set, dense CS is moderately brighter than mature bone; porous or partially dissolved CS falls into the bone/woven-bone range |
| Degradation | "Rapid and complete resorption without eliciting a significant inflammatory response" [RF: R36]. [PK] Typically resorbed within about 4–12 weeks, often faster than bone ingrowth, leaving a radiolucent gap. Resorption proceeds by dissolution from the surface inward |
| Histology | Amorphous, crystalline remnants (often lost in processing); mild inflammation; new bone in the former implant bed [PK] |
| Separation | **Moderate.** Early: brighter than woven bone, with a smooth, featureless interior (no trabecular pattern). Mid: dissolving CS fronts become low-density and grade into woven bone. **Composite CS/HA** (e.g. the HA phase persists) is common in products; the HA phase then dominates the late signal [PK] |

### 3.6 Bioactive glasses (45S5 Bioglass®, S53P4)

| Property | Content |
|---|---|
| Composition | 45S5: 45 SiO2 / 24.5 Na2O / 24.5 CaO / 6 P2O5 wt% [PK]. S53P4: 53 SiO2 / 23 Na2O / 20 CaO / 4 P2O5 wt% [PK]. 45S5 was the first artificial material found to form a chemical bond with bone [RF: Jones 2013, R37; Hench 2006, R38] |
| Density | ≈ 2.7 g/cm³ (melt-derived) [PK] |
| Forms | Particulates (e.g. 90–710 µm for 45S5 putties; S53P4 granules ≈ 0.5–0.8, 1–2, 2–3.15 mm [PK]); foams/porous scaffolds (difficult from 45S5 because it crystallizes during sintering [RF: R37]); sol-gel glasses (higher porosity, lower density) |
| μCT appearance | Lower Ca and P than CaP. HA-equivalent ≈ 1490–1520 mg HA/cm³ at 20–30 keV, rising to ≈ 1950–2010 at 80 keV (S53P4 lower than 45S5) [RF-derived, R59]. **Strongly energy-dependent relative to bone (Na and Si).** So the glass-to-bone contrast ratio changes with kVp and filtration: a direct example of why grey values aren't interchangeable |
| Degradation / reaction | Surface ion exchange → silica-gel layer → amorphous Ca-P → hydroxycarbonate apatite (HCA) layer [PK; mechanism summarized in R37]. Particle cores can persist for months to years; S53P4 granules are reported to remain for years [PK]. Dissolution products stimulate osteoprogenitors [RF: R37] |
| Histology | Glass particles with a reaction rim (Si-rich gel + Ca-P layer); bone bonding directly to the Ca-P layer; cracked or hollowed particles [PK] |
| Separation | **Moderate.** Intact cores are brighter than woven bone and similar to or brighter than mature bone depending on kVp. The reacted Ca-P rim forms a shell that resembles bone in both intensity and location. A core–rim morphology prior (a bright core surrounded by a band of different intensity) helps |

### 3.7 Demineralized bone matrix (DBM / DFDBA)

| Property | Content |
|---|---|
| Composition | Allograft bone ground into particles/fibres, demineralized in about 0.5–0.6 N HCl, and freeze-dried. Retains collagen and non-collagenous proteins, including BMPs. **Residual mineral 1–6%** [RF: Gruskin 2012, R39] |
| Forms | Powder, putty, paste, sheets, gels with carriers (glycerol, sodium hyaluronate, CMC, poloxamer, gelatin, collagen, calcium sulfate) [RF: R39]. Particles: < 250 µm are reported less osteoinductive than ≈ 420–840 µm [RF: R39] |
| Biology | Osteoinductive and osteoconductive. **Osteoinductivity varies between lots, tissue banks, and donors; there is no regulatory potency standard** [RF: R39] |
| μCT appearance | Initially near-soft-tissue or water attenuation, i.e. radiolucent: residual mineral of 1–6% gives at most ≈ tens of mg HA/cm³ [RF-derived from R39 residual-Ca range; the DBM attenuation itself was not reported in R39]. Some carriers (calcium sulfate) add their own radiodensity [RF: R39 lists CS as a carrier] |
| Degradation | Matrix biodegradation releases growth factors. Osteoconductive replacement is "very slow" [RF: R39]. Particles that remineralize or become incorporated into new bone take on bone-like density [PK] |
| Histology | Acellular demineralized collagen particles (eosinophilic, empty lacunae) surrounded by or incorporated into new bone; ectopic assay explants are scored by radiopacity and histology at about 28 d [RF: R39] |
| Separation | **Underdetermined by intensity for mineralized/incorporated DBM.** Early on DBM is invisible (it counts as soft tissue). Any mineral detected later is new bone *or* remineralized DBM. μCT cannot attribute it. Histology (empty lacunae in DBM particles) or labelled donors are needed |

### 3.8 Allograft (mineralized; fresh-frozen or freeze-dried, FDBA)

| Property | Content |
|---|---|
| Composition | Human donor bone with mineral retained; cortical or cancellous chips, struts, rings [PK] |
| μCT appearance | **Same material class as host bone: TMD ≈ host bone** [RF-derived: same mineral]. Mature lamellar donor bone may be *more* mineralized than new woven bone, a weak contrast [PK] |
| Degradation | Creeping substitution; "very slow", possibly years for large defects [RF: R39 on osteoconductive replacement] |
| Histology | Necrotic graft bone with empty lacunae; cement lines; new bone apposed [PK] |
| Separation | **Underdetermined by intensity.** At best, the morphology prior (sharp cut surfaces, cortical-chip geometry, lamellar texture) plus a day-0 registration. A TMD difference may give a probabilistic separation from new woven bone early on, but not from remodelled bone |

### 3.9 Xenograft: deproteinized bovine bone mineral (DBBM, e.g. Bio-Oss®) and sintered bovine bone (e.g. cerabone®)

| Property | Content |
|---|---|
| Composition | Bovine cancellous bone with organic matter removed. Bio-Oss: heat-treated at about 300 °C plus NaOH ("non-sintered"). cerabone: heated above 800 °C, then sintered at 1250 °C [RF: Kapogianni 2019, R14] |
| Forms | Granules S = 0.25–1 mm and L = 1–2 mm (Bio-Oss) [UNR: from a search snippet; manufacturer data not fetched]; blocks |
| Porosity | Total porosity ≈ 60% by mercury intrusion, much of it sub-micron (Bio-Oss) [UNR: snippet attributed to PubMed 19904820, not read]. Crystallites ≈ 15 nm [UNR: snippet] |
| μCT appearance | Trabecular-like granules whose struts are bone mineral. **Intensity is very close to bone.** Kapogianni 2019: μCT "did not allow for a precise interface distinction" because of "similar gray values of the natural BSM and the newly formed bone", and μCT "interprets the borders of the granules as newly formed bone tissue" [RF: R14]. Stalder 2014 thresholded a Bio-Oss block as "25.7% Bio-Oss (including bone in Bio-Oss)", i.e. bone inside the xenograft pores could not be separated [RF: R30]. Physical reasoning: the strut is bone mineral at native packing, so its HA-equivalent density is about that of the source bone tissue (≈ 1000–1300 mg HA/cm³) [inference; PK]. Sintered bovine HA may be denser (crystal growth), so it may be slightly more separable [PK] |
| Degradation | **Essentially non-resorbing.** No significant change in particle length or area between 6 mo and about 11 yr in human sinus grafts; at 11 yr biopsies held 17.3 ± 13.2% DBBM, 44.7 ± 16.9% lamellar bone, and DBBM–bone contact 61.5 ± 34% [RF: Mordenfeld 2010, R40]. Minipig: DBBM filler 35.7% (2 wk) → 31.6% (8 wk) [RF: R41] |
| Histology | Acellular trabecular-shaped granules with empty lacunae (bovine) and no osteocytes; new bone bridging between granules [PK] |
| Separation | **Underdetermined by intensity; partially recoverable by morphology/registration.** DBBM vs mature bone has near-identical attenuation; DBBM vs early woven bone may differ (DBBM brighter) but with overlapping distributions. Day-0 scan registration is the strongest cue because DBBM barely resorbs, so the day-0 graft mask remains largely valid [inference from R40] |

### 3.10 Composite scaffolds (polymer–ceramic, e.g. PCL/β-TCP, PLGA/HA, collagen/HA)

| Property | Content |
|---|---|
| Composition | Polymer matrix (PCL, PLA, PLGA, collagen) with 10–80 wt% ceramic filler [PK] |
| μCT appearance | The polymer is close to soft tissue (PMMA ≈ 1.19 g/cm³ as a proxy; PCL/PLA are similar [PK]). The ceramic phase is visible as dispersed particles; in a filled polymer the *effective* density = ceramic volume fraction × ceramic density. Example: 20 vol% β-TCP in PCL ≈ 600 mg HA/cm³ equivalent [RF-derived], i.e. **in the woven-bone range** |
| Degradation | Polymer: hydrolysis (PLGA weeks–months; PCL 2–4 yr [PK]); ceramic: as above |
| Separation | **Hard.** A homogeneous composite strut sits right in the early-bone density band. Scaffold geometry priors (printed lattice periodicity, known strut diameter) are essential. An automated method has exploited CaP scaffold periodicity plus edge and spatial-relationship information [UNR: search snippet, Illinois Experts listing "Automated segmentation of micro-CT images of bone formation in calcium phosphate scaffolds"] |

### 3.11 Magnesium-containing materials (Mg alloys; Mg-substituted CaP; Mg-doped glasses)

| Property | Content |
|---|---|
| Composition | Mg alloys (AZ31, AZ91, WE43, LAE442, etc.) as pins, screws, or porous scaffolds. Witte 2005 implanted rods of four alloys in guinea-pig femora [RF: R42]. Lightweight, with mechanical properties similar to bone [RF: Staiger 2006, R43] |
| Density | Pure Mg 1.74 g/cm³ [PK]. Alloys ≈ 1.75–1.85 g/cm³ [PK] |
| μCT appearance | Pure Mg ≈ 630–780 mg HA/cm³ equivalent (rising with energy) [RF-derived, R59]. **Mg metal falls in the woven/immature bone intensity band.** Rare-earth alloys (WE43: Y, Nd) attenuate more [PK]. The corrosion layer accumulates biological calcium phosphates [RF: R42], so it may look bone-like. Hydrogen gas pockets appear as near-air voids [PK] |
| Degradation | Corrosion "depending on the composition of the alloying elements"; high mineral apposition rates and increased bone mass around Mg rods [RF: R42]. Timescale weeks to > 1 year depending on alloy and coating [PK] |
| Separation | **Hard by intensity alone.** The residual metal core can overlap with woven bone, and the CaP-rich corrosion layer overlaps with bone. Use the geometry prior (known implant shape, day-0 registration), the gas-void signature, and implant-specific calibration. Mg-substituted CaP ceramics behave like CaP |

---

## 4. Summary: approximate HA-equivalent densities

All values are in mg HA/cm³, for ideal monoenergetic 30–60 keV, fully dense unless noted [RF-derived from R59 unless stated].

| Class | Value |
|---|---|
| Water / marrow / fibrous tissue | 0 to ≈ +35 (soft tissue ICRU-44: +13 at 30 keV, +33 at 60 keV) |
| Adipose (fatty marrow) | ≈ −45 to −55 |
| Mg metal | ≈ 630–710 |
| Callus "mineralized" threshold (Scanco µCT40) | 642 [RF: R21] |
| Desktop-μCT trabecular bone tissue (human) | 940–1030 [RF: R23] |
| ICRU cortical bone (1.92 g/cm³) | ≈ 1100–1170 |
| SRμCT / ash-referenced bone tissue | 1150–1300 [RF: R23] |
| Bioactive glass (S53P4 / 45S5, 2.7 g/cm³) | ≈ 1515–1760 / 1645–1850 |
| CaSO4·2H2O | ≈ 1640–1720 |
| CaSO4 anhydrite | ≈ 2615–2680 |
| β-TCP (dense) | ≈ 3025–3030 |
| HA (dense) | 3160 |
| Ti | ≈ 9500–11100 (out of calibration range; artifact-generating) |

**Porous / partly resorbed materials:** multiply the dense value by the sub-voxel solid fraction.

---

## 5. Items flagged [PK] that need primary verification (next pass)

1. Per-species BV/TV, Tb.Sp, and Tb.N ranges for rat, rabbit, sheep, and human (Hildebrand 1999 table values).
2. 45S5 and S53P4 compositions, densities, and granule sizes (Hench / Jones full texts; S53P4 manufacturer literature).
3. Calcium sulfate dihydrate density (2.32 g/cm³) and in vivo resorption weeks.
4. Bio-Oss granule size, porosity, and crystallite size (manufacturer + PubMed 19904820).
5. Mg alloy densities and in vivo corrosion timescales; hydrogen gas μCT appearance.
6. Woven-bone vs lamellar-bone TMD values from SRμCT/qBEI (e.g. Roschger BMDD values).
7. Sheep 3 cm tibial segmental defect (Reichert 2009 full text).
