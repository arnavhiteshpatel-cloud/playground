# Morphometry Standards for OsteoQuant

Status: knowledge base v1 (2026-11-27). Author role: domain scientist (bone regeneration and micro-CT).
Citation keys like [R1] point to `REFERENCES.md`.

Evidence tags:
- **[RF]**: verified against the cited source (abstract or full text read during this review).
- **[PK]**: prior knowledge of the author, consistent with the field but not re-verified against the primary text in this review. Treat it as provisional until someone checks it.
- **[UNR]**: unresolved or conflicting.
- **[ASSUMPTION]**: an engineering choice with no direct literature value.

---

## 1. Scope

This document covers three things:

1. Standard micro-CT morphometry for trabecular and cortical bone, following the ASBMR guidelines of Bouxsein et al. 2010 [R1].
2. The algorithms behind the core 3D indices: direct thickness [R2], Euler connectivity [R3], and SMI [R4, R5].
3. Histomorphometry nomenclature (Dempster et al. 2013 [R6]), plus the defect-specific endpoints used in bone-regeneration studies (new bone volume, residual graft, bridging scores, RUST/mRUST).

OsteoQuant's report generator should follow the symbols and units below exactly. Reviewers and journals check for them.

---

## 2. Bouxsein et al. 2010 (JBMR 25:1468-1486; DOI 10.1002/jbmr.141; PMID 20533309) [R1]

### 2.1 What the guideline requires [RF, abstract]

- **Methods reporting (mandatory):**
  - (1) Image acquisition: scanning medium, X-ray tube potential, voxel size, size and location of the VOI, and how trabecular and cortical regions were delineated.
  - (2) Image processing: the filtration algorithm and the segmentation approach.
- **Morphometric algorithms:** use 3D algorithms that do not assume an underlying structure (rod or plate) "whenever possible".
- **Minimal trabecular outcome set:** BV/TV, Tb.N, Tb.Th, Tb.Sp.
- **Minimal cortical outcome set:** Tt.Ar, Ct.Ar, Ct.Ar/Tt.Ar, Ct.Th.
- Other variables may be reported depending on the research question and scan quality. Standard nomenclature must be followed.

### 2.2 Variable table (symbols and units)

The symbols and units below follow the Bouxsein 2010 tables as the author knows them [PK]. The publisher full text could not be retrieved in this review (HTTP 403), so the per-row units are [PK]. The "Minimal" column is [RF], from the abstract.

| Symbol | Name | Definition | Unit | Minimal? |
|---|---|---|---|---|
| TV | Total volume | Volume of the VOI | mm³ | — |
| BV | Bone volume | Volume of voxels segmented as bone | mm³ | — |
| BS | Bone surface | Surface area of the bone phase (from a triangulated surface, e.g. marching cubes) | mm² | — |
| BV/TV | Bone volume fraction | BV ÷ TV | % | **Yes** |
| BS/BV | Specific bone surface | BS ÷ BV | mm²/mm³ (= mm⁻¹) | — |
| BS/TV | Bone surface density | BS ÷ TV | mm²/mm³ | — |
| Tb.Th | Trabecular thickness | Mean of the direct 3D local thickness (sphere fitting) of the bone phase | mm (often given in µm) | **Yes** |
| Tb.Sp | Trabecular separation | Mean of the direct 3D local thickness of the marrow/background phase | mm | **Yes** |
| Tb.N | Trabecular number | Inverse of the mean distance between mid-axes of the structure. A common approximation is BV/TV ÷ Tb.Th or 1/(Tb.Th + Tb.Sp) [PK] | mm⁻¹ | **Yes** |
| Conn.D | Connectivity density | (1 − χ) ÷ TV, edge-corrected Euler characteristic [R3] | mm⁻³ | optional |
| SMI | Structure model index | 6·(BV·BS′)/BS²; 0 = ideal plates, 3 = ideal rods, 4 = spheres [R4] | — | optional (see caveat in 2.5) |
| DA | Degree of anisotropy | Ratio of max to min eigenvalue of the fabric tensor (MIL or similar) | — (1 = isotropic) | optional |
| Tt.Ar | Total cross-sectional area | Area inside the periosteal envelope | mm² | **Yes** |
| Ct.Ar | Cortical bone area | Ct.Ar = Tt.Ar − Ma.Ar (bone area within the cortex) | mm² | **Yes** |
| Ma.Ar | Medullary (marrow) area | Area inside the endocortical envelope | mm² | — |
| Ct.Ar/Tt.Ar | Cortical area fraction | Ct.Ar ÷ Tt.Ar | % | **Yes** |
| Ct.Th | Cortical thickness | Mean direct 3D thickness of the cortex (or mean 2D thickness in slices) | mm | **Yes** |
| Ps.Pm / Ec.Pm | Periosteal / endocortical perimeter | Perimeter length | mm | — |
| Ct.Po | Cortical porosity | Pore volume ÷ cortical (bone + pore) volume | % | optional |
| Imax, Imin, J (pMOI) | Area moments of inertia | Geometric bending and torsion indices | mm⁴ | optional |
| TMD | Tissue mineral density | Mean HA-equivalent density of voxels segmented as bone only | mg HA/cm³ | optional |
| vBMD (BMD) | Volumetric bone mineral density | Mean HA-equivalent density of all voxels in the VOI (bone + marrow) | mg HA/cm³ | optional |
| BMC | Bone mineral content | vBMD × TV (or TMD × BV) | mg HA | optional |

The TMD vs vBMD distinction is [RF] via Kim et al. 2021 [R7]:

- **TMD** ("Mean2" in Scanco nomenclature) is the mean density of bone voxels only and does not depend on how much bone is present.
- **vBMD** ("Mean1") averages over all voxels in TV and is usually strongly correlated with BV/TV.

### 2.3 Practical acquisition recommendations relevant to OsteoQuant

- **Mouse trabecular bone [RF via R7]:**
  - A voxel size of 6–10 µm is recommended for accurate trabecular parameters.
  - 15–20 µm is acceptable; larger voxels are not recommended.
  - Mouse Tb.Th is about 40 µm, which gives a feature-to-voxel ratio of at least 3–4:1.
- **Fracture callus [RF via R8]:** Morgan et al. suggest about 16 µm voxels for rat calluses and about 12 µm for mouse calluses.
- **Thresholds [RF via R7]:**
  - Thresholds are system- and protocol-dependent and must be verified visually.
  - Scanco starting points are about 220‰ (trabecular) and about 300‰ (cortical), and a histogram midpoint between the background and bone peaks is a reasonable starting value.
  - These per-mille units are NOT transferable between scanners.

### 2.4 Direct (model-independent) thickness: Hildebrand & Rüegsegger 1997 [R2]

- **Definition [PK, standard]:** For each point p in the structure Ω, the local thickness τ(p) is the diameter of the largest sphere that contains p and lies completely inside Ω.
- **Tb.Th** is the volume-weighted mean of τ(p) over all bone voxels. The τ distribution (mean, SD, histogram) is itself informative.
- **Tb.Sp** is the same operation applied to the marrow/background phase within the VOI.
- **Implementation:**
  1. Compute the Euclidean distance transform (EDT) of the binary structure.
  2. Reduce it to the medial axis or ridge set (centres of maximal inscribed spheres).
  3. For every ridge point with radius r, paint the sphere of diameter 2r, assigning to each covered voxel the maximum diameter that covers it.
- **Availability:** Implemented in Scanco IPL, Bruker CTAn, and BoneJ ("Thickness") [R9].
- **Contrast with the older approach:** Unlike plate-model estimates (Tb.Th = 2·BV/BS) [PK; Parfitt 1987 R10], direct thickness needs no rod/plate assumption. This is why Bouxsein 2010 prefers 3D model-independent algorithms [R1].
- **Voxel-size bias:**
  - Direct thickness is quantised to the voxel grid. Structures less than about 2–3 voxels thick are overestimated, and partial volume plus thresholding dominate the error.
  - Christiansen 2016 [R11] showed in mice that voxel size and segmentation method materially change trabecular measures. OsteoQuant must report the voxel size with every thickness value.

### 2.5 Connectivity: Euler characteristic (Odgaard & Gundersen 1993) [R3]

- **[RF, abstract]:**
  - The Euler characteristic χ of a 3D structure is a topological invariant: the number of particles plus the number of enclosed cavities minus the connectivity.
  - It can only be used as a connectivity measure when the numbers of particles and cavities are known.
  - Because of edge effects, the χ of an excised specimen is a biased estimate of the χ of the region it came from. Odgaard & Gundersen give a method that controls both problems and is free of assumptions about trabecular shape.
- **Formula [PK]:**
  - With Betti numbers β0 (particles), β1 (connectivity / handles), and β2 (enclosed cavities), χ = β0 − β1 + β2.
  - For trabecular bone with one connected bone phase and no isolated marrow cavities, β1 = 1 − χ, and Conn.D = β1 / TV.
  - χ is computed locally by voxel-based Euler–Poincaré counting (vertices − edges + faces − cubes, 26-connectivity for bone). An edge correction Δχ estimates the contribution of the VOI boundary. BoneJ implements this as "Connectivity" [R9].
- **Defect-specific caveat:** In early defects new bone is fragmented: many particles, so β0 ≫ 1. Then (1 − χ)/TV can become *negative* or uninterpretable. OsteoQuant should report β0 (particle count) alongside Conn.D, and should purify or label small particles before computing connectivity [ASSUMPTION, recommended practice].

### 2.6 Structure model index (Hildebrand & Rüegsegger 1997) and its limitation

- **Definition [PK]:** SMI = 6·BV·(dBS/dr)/BS². Here dBS/dr is the surface-area derivative under a small dilation of the surface. Ideal plates give 0, ideal rods 3, and spheres 4 [R4].
- **Limitation [RF]:** Salmon et al. 2015 [R5] showed that SMI does not measure rods and plates in trabecular bone. Concave surfaces contribute negative dBS/dr, and real trabecular bone has a large fraction of concave surface.
- **OsteoQuant policy:**
  - SMI may be reported for legacy comparison only, flagged with this caveat.
  - Prefer ellipsoid factor or plate/rod segmentation when shape is the question [ASSUMPTION: product recommendation].

### 2.7 Other 3D methods

Odgaard 1997 [R12] reviews 3D methods for cancellous architecture, including volume fraction, MIL/fabric anisotropy, connectivity, and direct thickness. Use it as the background reference for the anisotropy (DA) implementation.

---

## 3. Histomorphometry nomenclature (Dempster et al. 2013, JBMR 28:2-17; DOI 10.1002/jbmr.1805; PMID 23197339; PMC3672237) [R6]

This is the 2012 update of Parfitt et al. 1987 [R10]. The rules and units below are [RF], from the PMC full text.

### 3.1 General rules

- **Referents** (BS, BV, TV, B.Pm, OS, CV) must be stated explicitly. Once the referent is named, words such as "ratio" or "relative" are redundant.
- **B.Pm** is a 2D quantity. It may be used as a referent only for number measurements (e.g. N.Oc/B.Pm).
- **2D vs 3D terms:** an article uses either 2D or 3D terms throughout, never a mix. The committee prefers 3D terms (surface, volume, thickness). Number is the exception: it is reported in 3D only if serial sections were examined.
- **Tissue area, bone area, and bone perimeter** should be reported (as ranges) so readers can judge sampling adequacy.
- **Prefixes:**
  - "Tb" denotes an individual trabecula: Tb.Th, Tb.N, Tb.Sp, Tb.Dm.
  - "Ct" denotes cortical tissue: Ct.Th, Ct.Po.
  - Full names such as Cn-BV/TV (cancellous) are permitted.

### 3.2 Core parameters

| Symbol | Meaning | Unit |
|---|---|---|
| BV/TV | Bone volume as a fraction of tissue volume (cancellous: Cn-BV/TV) | % |
| OS/BS | Osteoid surface ÷ bone surface | % |
| O.Th | Osteoid thickness | µm |
| Ob.S/BS | Osteoblast surface ÷ bone surface | % |
| Oc.S/BS | Osteoclast surface ÷ bone surface | % |
| ES/BS | Eroded surface ÷ bone surface | % |
| N.Ob/BS (or N.Ob/B.Pm) | Osteoblast number per bone surface (perimeter) | /mm |
| N.Oc/BS (or N.Oc/B.Pm); N.Oc/T.Ar | Osteoclast number per bone surface (perimeter); per tissue area | /mm; /mm² |
| MS/BS | Mineralizing surface ÷ BS = (dLS + sLS/2)/BS | % |
| MAR | Mineral apposition rate: distance between the midpoints (or corresponding edges) of two labels ÷ inter-label time (= Ir.L.Th/Ir.L.t) | µm/d |
| BFR/BS | Bone formation rate per bone surface = MAR × MS/BS | µm³/µm²/d (often given as µm³/µm²/y) |
| BFR/BV | Bone formation rate per bone volume (turnover) | %/y |
| Aj.AR | Adjusted apposition rate = MAR × (MS/OS) | µm/d |
| Mlt | Mineralization lag time = O.Th/Aj.AR | d |

### 3.3 Relevance to OsteoQuant

- **Validation against histology:** Histology is the reference standard for distinguishing new bone (osteoid, woven bone, active osteoblast surfaces) from residual graft. When OsteoQuant validates a micro-CT segmentation against co-registered histology, the histology outputs should use these symbols: e.g. "N.Bone.Ar/T.Ar" for new bone area or "Graft.Ar/T.Ar" for residual graft area.
- **Graft-specific symbols:** The Dempster nomenclature does not define graft-specific symbols [RF: none found in the PMC text]. Proposed OsteoQuant extensions [ASSUMPTION], built by analogy with the ASBMR rules:

| Proposed symbol | Meaning | Unit |
|---|---|---|
| NB.V/TV | New bone volume ÷ defect tissue volume | % |
| Gr.V/TV | Residual graft volume ÷ defect TV | % |
| Gr.V/Gr.V0 | Residual graft fraction relative to day-0 implanted graft volume (requires a day-0 scan) | % |
| BGC/Gr.S (Bone-graft contact) | Fraction of graft surface in direct contact with bone | % |
| NB.Th, Gr.Th | Direct 3D thickness of new bone and of graft | µm |

---

## 4. Defect-specific endpoints

### 4.1 Volumetric endpoints commonly reported

- **New bone volume (BV or NBV, mm³) and BV/TV (%) within a defect VOI.**
  - VOI conventions: a cylinder matching the defect diameter (e.g. 8 mm × full calvarial thickness for the rat calvarium) or a geometrically defined condyle cylinder.
  - Spicer et al. 2012 [R13] note that untreated 8 mm rat calvarial defects fill to only about 5–15% mineralized volume by micro-CT [RF].
- **Residual graft volume and bone-graft contact.**
  - Usually derived from histology. A μ-CT version is possible only when graft and bone are separable (see `SEPARABILITY_ANALYSIS.md`).
  - Kapogianni et al. 2019 [R14] state that μ-CT overestimated bone-material contact for xenografts, because granule borders were classified as new bone [RF].
- **Defect closure / bridging** (planar % closure on a top-down projection; 2D area fraction).
- **TMD of the defect bone vs host bone.** This measures maturation. It is only reportable when HA-phantom calibration and fixed acquisition settings are documented (see `MICROCT_IMAGING_SCIENCE.md` §6).

### 4.2 Bridging and union scores

**Calvarial bony bridging score (Mikos group):**

- Patel et al. 2008 [R15] (8 mm rat cranial defect, 4 and 12 wk) used a "scoring guide for extent of bony bridging and union using microCT datasets", with scores 0–4 [RF: the table exists in PMC3014108; the definitions below come from search snippets, so their wording is UNR].
- Snippet definitions: 4 = bridging across the entire defect span at its longest point (8 mm); 3 = bridging over part of the defect length; 2 = bridging only at the defect borders; 1 = few bony spicules dispersed through the defect; 0 = no bone formation in the defect [UNR for score 0].
- Watson et al. 2015 [R16] used a similar scheme. Spicer et al. 2012 [R13] reproduce it as their Fig. 4.

**RUST / mRUST:**

- RUST was introduced by Whelan et al. 2010 [R17]; mRUST was evaluated by Litrenta et al. 2015 [R18].
- **mRUST [RF via R19]:** each of 4 cortices is scored 1–4:
  - 1 = no healing
  - 2 = callus present, no bridging
  - 3 = bridging callus, fracture line visible
  - 4 = bridging callus, no fracture line visible (remodelled)
- **Total score:** sum of the 4 cortices, from 4 (not healed) to 16 (fully healed).
- **Original RUST [PK]:** scores 1–3 per cortex (callus absent / callus present with visible fracture line / bridging without fracture line), total 4–12.

**Preclinical validation:**

- **Rat (Fiset et al. 2018 [R20], RF abstract):** femoral osteotomy with a PEEK plate, endpoints 5–17 wk. RUST and mRUST were validated against micro-CT and biomechanical testing.
- **Mouse (Alentado et al. 2022 [R19], RF):** femoral fractures in 158 mice.
  - Inter-rater Gwet's AC2 was 0.51–0.86.
  - mRUST correlated with μCT TMD (r = 0.83), Tb.Th (r = 0.78), and BV/TV (r = 0.65).
  - Typical trajectory: scores of 4–6 at day 7, plateauing at 14–16 by about day 24.

**OsteoQuant implementation note:**

- RUST/mRUST were designed for orthogonal 2D radiographs. On μ-CT, generate two orthogonal pseudo-radiographs (ray-sum projections) or score 4 cortices on orthogonal multiplanar reformats.
- Report which was used. Inter-rater agreement must be measured; mRUST is not an automated metric [ASSUMPTION].

### 4.3 Recommended OsteoQuant defect report (minimum)

| Item | Unit | Notes |
|---|---|---|
| Defect VOI definition (shape, size, anchor landmarks) | mm | Required; ideally reproducible from a day-0 scan |
| TV (defect) | mm³ | |
| New bone BV, BV/TV | mm³, % | Must state the class-assignment method and its confidence (see separability) |
| Residual graft volume, Gr.V/TV; Gr.V/Gr.V0 if a day-0 scan exists | mm³, % | Flag as "UNDERDETERMINED" for DBBM/allograft without additional data |
| Total mineralized volume (bone + graft) | mm³ | Always reportable even when classes are inseparable |
| NB.Th (direct), Tb.Sp, Conn.D, β0 | µm, µm, mm⁻³, count | |
| TMD of new bone and host bone | mg HA/cm³ | Only with a calibration record (see imaging doc §6) |
| Bridging score (0–4) and/or % closure | — | Rater blinded; state the scheme |
| Voxel size, kVp, filter, reconstruction, threshold | — | Required by Bouxsein 2010 [R1] |
