# OsteoQuant Public Dataset Registry

Compiled 2026-11-27 by the dataset-acquisition survey. Machine-readable copy: `data/manifest/datasets.json` (41 records).

**Conventions**
- `[UNR]` means the item was not verified against a primary source in this survey. Do not rely on it until someone checks it.
- File sizes are exact byte counts from repository APIs (Zenodo REST, Dryad v2, Figshare v2, IDR/EBI FTP). Where a size was confirmed by an HTTP HEAD request (or a ranged GET for Figshare/S3), the table marks it "HEAD ok".
- Licence column: **CC0 / CC-BY = commercial use allowed** (with attribution for CC-BY). **NC = research only**: usable for internal benchmarking, **not** for training weights that ship in a commercial product.
- Repositories searched: Zenodo API, Dryad API (its search endpoint rate-limits with 403 after a few queries), Figshare API, Harvard Dataverse API, EBI BioImage Archive (BioStudies API), IDR API and EBI FTP, OSF/SHARE API, TCIA, plus general web search. MorphoSource terms were checked from its documentation. Mendeley Data was not searched because the web-search quota ran out before that query (see Gaps).

---

## 1. Summary table

| # | Slug | Content | Species / site | Voxel (µm) | Labels | Licence | Size | Priority |
|---|---|---|---|---|---|---|---|---|
| 1 | dryad_bone_4j0zpc8qq | BONe 2D bone/pore DL dataset | mouse humerus+femur (6 scans), otter, leopard, capybara, sea otter | 9.1–11.3 (mouse); 30–120.7 | **Bone/pore masks (TIFF)** | CC0 | 44.6 GB | **Now (4.1 GB subset)** |
| 2 | dryad_otter_ctp_b2rbnzsq4 | Otter limb bones, raw + CTP labels | river otter limb bones | 49.99 | **Cortical / trabecular / pore** | CC0 | 72.8 GB | **Now (1 sample)**, rest later |
| 3 | zenodo_3909552_mouse_oa_knee | Kitware OA-biomarker mouse knees | mouse knee, 28 knees | 10 | **1 manual 8-class compartment map + AUTO labels for all** | CC-BY-4.0 | 35.3 GB | **Now (907-L, 1.93 GB)** |
| 4 | zenodo_11061947_trab_tbth | Binary trabecular cubes + Scanco IPL Tb.Th/Tb.Sp maps | [UNR] (8 cubes) | 16.56 (header) / 17.59 (text) | **Binary + reference distance maps** | CC-BY-4.0 | 242 MB | **Now** |
| 5 | zenodo_3608390_synthetic_trab | Synthetic cortical/trabecular phantom volumes | synthetic | – | **4-class GT** | CC-BY-4.0 | 769 MB | Now (GT done) |
| 6 | zenodo_24047383_sprout | SPROUT multi-class micro-CT (dog forelimb, skulls) | dog forelimb ×15 | [UNR] | **Per-bone reference segmentations** | CC-BY-4.0 (skulls: MorphoSource terms) | 13.2 GB | **Now (dog, 189 MB)** |
| 7 | zenodo_6108435_human_skull | Human skull micro-CT + bone seg | human ×1 | [UNR] | Bone mask | CC-BY-4.0 | 18.2 GB | Later |
| 8 | zenodo_17255310_ovine_callus | Distraction-osteogenesis callus | sheep metatarsus ×6 time points | 3.72 | none | CC-BY-4.0 | 12.5 GB | Now (already downloading) |
| 9 | zenodo_19045245_pla_bone_substitute | PLA / PLA-chitosan bone substitutes | scaffold only | [UNR] | none | CC-BY-4.0 | 7.7 GB | Later |
| 10 | zenodo_24081554_voronoi_ha_scaffold | Binarized 3D-printed HA Voronoi scaffolds | HA scaffold ×8 | 15 | binary | CC-BY-4.0 | 15 MB | Now (done) |
| 11 | zenodo_14628379_pan_chitosan_scaffold | Trabecular-mimicking polymer scaffolds | scaffold | [UNR] | none | CC-BY-4.0 | 2.4 GB | Later |
| 12 | zenodo_taox_scaffold_longitudinal | **Longitudinal in vivo** micro-CT, TaOx-PCL/PLGA scaffolds | mouse IM/IP (non-bone) | 50 | none | CC-BY-4.0 | ~272 GB (6 records) | Not useful (size) |
| 13 | zenodo_4360730_pemf_ring | In vitro mineralizing rings | mouse cells | [UNR] | none | CC0 | 40.6 GB | Not useful |
| 14 | kaggle_bone_lab_calvarial | Calvarial defect slices + defect ROI | mouse/rat [UNR] | [UNR] | defect circle ROI | **unknown** | [UNR] | Not until licence is known |
| 15 | zenodo_19404386_lumbarsr | Paired clinical CT + micro-PCCT | human vertebrae ×30 | 105 (PCCT) | Bone ROI masks | CC-BY-4.0 | 26.8 GB | Later |
| 16 | zenodo_8405457_trab_screw | Trabecular bone ± screw voxel models | [UNR] cores ×10 | 20 | **bone / screw models** | CC-BY-4.0 | 13.2 GB | Later |
| 17 | zenodo_3539508_glenoid_dvc | Repeated micro-CT, loaded/unloaded | human glenoid ×1 | [UNR] | bone-masked | CC-BY-4.0 | 15.1 GB | Later |
| 18 | zenodo_4073082_hrpqct_demo | Scanco ISQ HR-pQCT | human ×2 | [UNR] | none | **CC-BY-NC-SA-4.0** | 1.0 GB | Later (research-only) |
| 19 | zenodo_6990764_chicken_bone_dose | CBCT projections at 4 dose levels | chicken bone | [UNR] | none | CC-BY-4.0 | 7.2 GB | Later |
| 20 | zenodo_8181250_lumvbcanseg | Clinical CT cancellous masks | human L1–L5 | 1000 | masks | CC-BY-4.0 | 10.1 GB | Not useful |
| 21 | zenodo_21494458_femhals | Human femur QCT + µCT + mechanics | human ×94 | [UNR] | [UNR] | restricted | – | Later (request) |
| 22 | figshare_ovx_mouse_femur | OVX vs sham whole femur | mouse ×15 | 13.7 | none | CC0 | 86.0 GB | Later |
| 23 | figshare_oi_mouse_tibia | OI vs WT proximal tibia | mouse ×21 | [UNR] | none | CC0 | 9.8 GB + meshes | Later (1 sample optional) |
| 24 | shef_orda_mouse_tibia_invivo | Repeated in vivo/ex vivo tibia scans | mouse | [UNR] | none | CC-BY-4.0 (record) | – | Later (request) |
| 25 | miceBoneChallenge | Growth-plate annotated femurs | mouse ×83 | [UNR] | growth plate | [UNR] | – | Later (find the data) |
| 26 | hereon_mg_implant_srct | SRµCT Mg/Ti screws in rat bone | rat | [UNR] | (in papers) | – | – | Not available |
| 27 | zenodo_7558211_bone_metal_ct | Clinical CT with metal | [UNR] | [UNR] | [UNR] | CC-BY-4.0 | 1.0 GB | Not useful |
| 28 | idr0096_marrowquant | **Bone H&E whole-slide images** | mouse femur/tibia/vertebra; human iliac crest | 0.344 px | ROI per image | CC-BY-4.0 | ~353 GB (205 files) | **Now (2–3 WSIs)** |
| 29 | idr0144_jawbone_histology | Serial sections, jaw trabecular bone | human | [UNR] | [UNR] | CC-BY-4.0 | [UNR] | Later |
| 30 | zenodo_10518968_nuinsseg | H&E nuclei instance masks | human + mouse organs | – | **nuclei instances** | CC-BY-4.0 | 1.63 GB | **Now** |
| 31 | zenodo_5022015_oc_finder | Osteoclast culture images + point labels | mouse cultures | – | point labels | CC-BY-4.0 | 5.9 GB | Later |
| 32 | tcia_osteosarcoma_tumor_assessment | Osteosarcoma H&E tiles | human | – | tile classes | CC-BY-3.0 | 197 MB | Later |
| 33 | zenodo_21666670_fexhis | Cortical bone LM, manual labels (canals, lacunae, cement lines) | human ×94 femora | – | manual masks | restricted | – | Later (request) |
| 34 | zenodo_23884832_goat_cartilage | Osteochondral H&E + SR phase-contrast CT | goat | [UNR] | none | CC-BY-4.0 | 6.9 GB | Later |
| 35 | zenodo_18937854_vbmc_xrh | X-ray histology of marrow trephines | human ×6 | [UNR] | derived | CC-BY-4.0 + governance clause | 9.4 GB | Not useful |
| 36 | cellbindb | Multimodal cell segmentation (incl. H&E) | mouse + human | – | cell masks | CC0 (own part); bundled sets mixed | 8.2 GB | Later |
| 37 | nuclei_nc_family | PanNuke / Lizard / MoNuSeg | human | – | nuclei | **NC [UNR]** | – | Later (research-only) |
| 38 | noise_osteoclast | NOISe osteoclast instances | mouse | 0.78 px | instances | **none stated** | – | Not useful |
| 39 | bambo_bone_marrow | Bone-marrow biopsy segmentation | human | – | masks | restricted | – | Later (request) |
| 40 | simtk_knee_cartilage_histology | Knee cartilage H&E/SafO with grades | human ×90 | – | grades only | [UNR] | 27 GB | Not useful |
| 41 | opara_tud_calibration_phantom | Geometric calibration phantom projections | PMMA + steel balls | [UNR] | known geometry | CC-BY-4.0 [UNR] | [UNR] | Later |

---

## 2. Priority datasets in detail

### 2.1 BONe — Dryad doi:10.5061/dryad.4j0zpc8qq (CC0)
- **Title:** Deep learning software and revised 2D model to segment bone in micro-CT scans. Version 11, published 2026-07-13, `storageSize` 44,638,405,276 B.
- **Publications:** 10.3389/fbinf.2025.1677527 (primary) and 10.1002/ar.25633 (Lee et al. 2025).
- **Access:** open (CC0). Dryad API metadata and file lists are reachable from the container. However, `GET /api/v2/files/{id}/download` returns **401 "must have current bearer token"**, and the browser stream URL `https://datadryad.org/downloads/file_stream/{id}` returns **403** to scripted curl. To fetch files, use a Dryad API account/token ([UNR] how to obtain one; ask Dryad support) or download in a browser and copy the files in.
- **Specimens and imaging:** 20 scan sets across 5 species.
  - 6 mouse sets: 2 C57BL/6 males per set, left humerus + femur, 29 weeks old. Nikon XT H 225 ST, 120–160 kV, 9.1–11.3 µm.
  - 11 river-otter sets (labels only).
  - Leopard (AMNH M-89009, 66.8 µm), capybara (AMNH M-206440, 120.7 µm, subvolume labels only), sea otter (ZMB 30740, 30 µm, labels only).
- **Labels:** "BP" (bone vs pores) reference masks as 2D TIFF slices with `.info` files. They were made in Avizo 2024.2 with Otsu thresholding, filtering and ambient occlusion, then manually corrected where deep concavities were misclassified. The README does not state numeric class values [UNR]. These are healthy cortical/trabecular long bones: no defects, implants or callus.
- **Files** (bytes; Dryad file id):

| File | Bytes | id | Content |
|---|---|---|---|
| README.md | 30,467 | 4859595 | |
| 1R_1U_HF.zip | 2,031,389,746 | 4859575 | mouse raw slices + BP labels, 11.3 µm |
| 2R_2U_HF.zip | 4,170,762,024 | 4859576 | mouse, 9.1 µm |
| 5R_5U_HF.zip | 4,294,422,299 | 4859578 | mouse |
| 7R_7U_HF.zip | 5,017,819,508 | 4859577 | mouse |
| 12R_12U_HF.zip | 4,957,324,559 | 4859579 | mouse |
| 19R_19U_HF.zip | 12,115,604,842 | 4859580 | mouse |
| AMNH_Mammals_M-89009_F.zip | 7,986,549,084 | 4859581 | leopard scan + labels |
| AMNH_Mammals_M-206440_mixed.zip | 35,542,801 | 4859582 | capybara subvolume labels |
| OMNH_Mammals_44262_HRU.zip | 11,457,271 | 4859583 | otter labels |
| OMNH_Mammals_53994_FTFi.zip / _HRU.zip | 17,689,387 / 13,599,904 | 4859584 / 4859585 | otter labels |
| UAM_Mamm_24789_FTFi / 67696_HF / 67696_TFiRU | 17,467,240 / 25,427,790 / 19,431,995 | 4859586–88 | otter labels |
| UF_Mammals_23593-24550_HF / 31151_HRU | 30,369,184 / 12,342,435 | 4859589–90 | otter labels |
| UWBM_Mamm_78743_FTFi / 81969_FTFi / 81969_HRU | 18,278,986 / 21,723,722 / 20,057,351 | 4859591–93 | otter labels |
| ZMB_Mam_30740_HRU.zip | 71,553,769 | 4859594 | sea-otter labels (scan on MorphoSource) |
| _Models.zip | 3,749,422,956 | 4859596 | PyTorch .pth models (U-Net, UNet++, DeepLabV3+, SegFormer) |
| _BONe_Avizo.zip / _BONe_standalone.zip | 48,843 / 89,113 | 4859597 / 4859598 | code |

- **Recommended subset under 6 GB (images + labels): about 4.13 GB.**
  1. `README.md` (30 KB)
  2. `1R_1U_HF.zip` (2.03 GB): in-domain rodent images with BP labels.
  3. `OMNH_Mammals_44262_HRU.zip` (11 MB): updated BP labels for the otter specimen.
  4. `SNM_44262_HRU.zip` from dryad.b2rbnzsq4 (2.09 GB): the matching raw otter scan plus its CTP labels.

  This subset gives two species, two resolutions (11 µm and 50 µm), and two label schemes (bone/pore and cortical/trabecular/pore). If the 6 GB cap is soft, an all-mouse option is `1R_1U` + `2R_2U` = 6.20 GB.
- **Caveats:**
  - Three scans (leopard, capybara, sea otter) come from MorphoSource. Check the upstream media terms before using them in commercial training. The otter and mouse data are clean CC0.
  - The `_Models.zip` weights are CC0. They could serve as a teacher or baseline.

### 2.2 Otter CTP — Dryad doi:10.5061/dryad.b2rbnzsq4 (CC0)
- 9 river otters from 4 museums: 38 limb bones in 12 scan sets (8 fitting, 4 blind test). Nikon XT H 225 ST at 49.99 µm, 79–160 kV.
- Each zip contains `_Raw` 16-bit TIFF slices with `.xtekct`/`.info` files, a `CTP-label` folder (cortical / trabecular / medullary pores), and predictions from 4 models.
- **How the ground truth was made:** sigmoid remapping, then auto-threshold with manual checking, a top-hat filter to recover thin trabeculae, ambient occlusion to find pores, and a shrink-wrap mask to split cortical from trabecular bone.
- Smallest volumes: SNM_44262_HRU 2,091,127,128 B (id 3926474); UF_31151_HRU 2,183,694,093 B (id 3926482); UF_24550_TFiRU 2,321,508,823 B (id 3926481). `_composite.zip` is 22.4 GB; skip it.
- Total 72.8 GB. Paper 10.1002/ar.25633.
- Best use: cortical/trabecular compartment segmentation and cross-species generalization tests.

### 2.3 Mouse OA knee — Zenodo 10.5281/zenodo.3909552 (CC-BY-4.0)
- 28 knees (14 mice, left and right) of factor-VIII-deficient (haemophilic arthropathy) mice and controls, at 3 and 8 weeks. Original study: Lau AG et al. 2014, Haemophilia 20(5):716–722, PMC4396845.
- `ORIG-*.zip` files hold DICOM, 0.64–1.90 GB each.
- **Labels, checked by downloading:**
  - `MAN-907-L-label.nrrd`: int16, gzip NRRD, 1392×983×829 voxels at 0.010 mm. 8 classes: 1 epiphysis, 2 growth plate, 3 spongiosa region, 4 cortical metaphysis, 5 metaphysis medullary cavity, 6 diaphysis medullary cavity, 7 diaphysis cortical shell, 8 shaft rest. Manual (Kitware HASI project).
  - `AUTO-*` labels for every knee are algorithm output; treat them as pseudo-labels.
- **Subset (1.93 GB):** `ORIG-907-L.zip` (1,896,492,641 B, HEAD ok), `MAN-907-L-label.nrrd` (3,191,848 B, downloaded), `MAN-SegmentationFinal.seg.nrrd` (11,068,200 B), `AUTO-907-L-label.nrrd` (9,797,481 B, downloaded).
- URL pattern: `https://zenodo.org/api/records/3909552/files/<name>/content`.
- Limitations: the scanner model is [UNR]; this is a disease model, not a defect model; only one knee has manual ground truth.

### 2.4 Trabecular Tb.Th/Tb.Sp reference — Zenodo 10.5281/zenodo.11061947 (CC-BY-4.0)
- 8 samples (BMLPL_001…009; REF and BML groups) of 100³ binary trabecular cubes.
- Each comes with Tb.Th and Tb.Sp distance-transform maps computed by Scanco IPL and by Python (ORMIR_XCT).
- Verified on download: NIfTI, int16 with values {0,127}, BV/TV ≈ 9.8 % for sample 005.
- The header voxel is 16.56 µm but the description says 17.59 µm. Resolve this with the author before quoting absolute values.
- **Best available open ground truth for validating OsteoQuant's thickness/separation code against Scanco IPL.**

### 2.5 Ovine distraction callus — Zenodo 17255310/17255311 (CC-BY-4.0)
- 6 Zeiss/Xradia `.txm` files (OLE2 compound documents), about 2.0–2.1 GB each, at days 18, 22, 47, 64, 112 and 161.
- Yxlon Y.Cougar SMT, 3.72 µm voxels, about 25 mm field of view. One animal per time point, so this is not longitudinal within an animal. No labels.
- `data/raw/zenodo_17255310/` already holds 18DAYS (complete, 2,097,692,672 B) and part of 161DAYS. Another process is downloading these; this survey did not start it.

### 2.6 MarrowQuant — IDR idr0096, Data DOI 10.17867/10000170 (CC-BY-4.0)
- H&E whole-slide images of entire mouse bones: femur, tibia, L4/L6 vertebrae, sternum, tail. Conditions are aging and post-irradiation aplasia time courses. Experiment B adds human iliac-crest biopsies.
- OME-TIFF, RGB, 20×, 0.344 µm/px. Paper 10.3389/fendo.2020.00480.
- 205 files of 79 MB–11 GB (~353 GB total) at `https://ftp.ebi.ac.uk/pub/databases/IDR/idr0096-tratwal-marrowquant/20210609-ftp-ome-tiffs/`.
- Example file: `21_D21_RF%20(20x).ome.tiff`, 588,331,927 B, HEAD ok. The EBI host intermittently resets TLS connections; use `--retry`.
- Labels: the IDR annotation CSV lists one ROI per image (downloaded to `data/raw/idr0096_marrowquant/`). These are ROIs, not pixel masks. The bone / adipocyte / haematopoietic quantification lives in the paper's QuPath workflow.
- **This is the only verified, commercially usable bone-specific histology source found.**

### 2.7 NuInsSeg — Zenodo 10.5281/zenodo.10518968 (CC-BY-4.0)
- H&E patches from human and mouse organs with manual nuclei instance masks. `NuInsSeg.zip` is 1,627,427,342 B (HEAD ok).
- A commercially usable nuclei set for the histology module's cell-detection stage. PanNuke, Lizard and MoNuSeg are NC; see Section 3.

### 2.8 SPROUT — Zenodo 10.5281/zenodo.24047383 (CC-BY-4.0)
- `data_dog_forelimb.zip` (189,279,122 B, HEAD ok): 15 dog forelimb micro-CT scans with reference multi-class segmentations, made with SPROUT and corrected manually.
- Cheap, independently labelled micro-CT for out-of-distribution evaluation of bone foreground segmentation. The 8 MorphoSource-derived skull scans keep their original licences.

### 2.9 Other notable entries
- **8405457 trabecular bone + screw (CC-BY):** 10 cores at 20 µm, stored as MATLAB voxel models before and after screw insertion. Bone and screw are already segmented, so it suits bone-implant contact (BIC) and peri-implant ROI tests. Single 13.2 GB zip.
- **LumbarSR (CC-BY):** the only verified open multi-resolution trabecular set (clinical CT vs 105 µm photon-counting micro-CT, 30 human vertebrae, with bone masks). The 26.8 GB split zip needs all 7 parts.
- **OVX femur (Figshare, CC0):** SkyScan 1172 at 13.7 µm, 15 mice. Each RAR is ~5.5 GB and includes raw projections. Good for testing SkyScan/NRecon ingestion.
- **OI tibia (Figshare, CC0):** 21 proximal tibiae as 991 8-bit BMPs each (~0.47 GB per zip) plus PLY meshes. Disease phenotype gives a domain shift.
- **TaOx scaffolds (CC-BY):** the only open *longitudinal in vivo* micro-CT found (20 weeks, n=6 per group, 50 µm). The implants are intramuscular/intraperitoneal, not in bone, and each record is 38–50 GB.
- **HR-pQCT demo (CC-BY-NC-SA):** real Scanco `.ISQ` files, useful only for reader testing. Research-only.

---

## 3. Licensing analysis

| Class | Datasets | Implication for OsteoQuant |
|---|---|---|
| **CC0** | BONe, otter CTP, OVX femur, OI tibia, PEMF, CellBinDB (own images) | No conditions. Safe for commercial training and for test fixtures. Keep provenance records anyway. |
| **CC-BY 4.0 / 3.0** | Zenodo 3909552, 11061947, 3608390, 24047383 (dog), 6108435, 17255310, 19045245, 24081554, 14628379, TaOx series, LumbarSR, 8405457, 3539508, 6990764, IDR idr0096/idr0144, NuInsSeg, OC_Finder, TCIA osteosarcoma (CC-BY-3.0), goat cartilage | Commercial use allowed with attribution. Keep a NOTICE/attribution file listing DOIs for any weights trained on them. |
| **NC (research only)** | HR-pQCT demo (CC-BY-NC-SA-4.0); PanNuke / Lizard / MoNuSeg (reported NC-SA [UNR]); RibFrac (CC-BY-NC, clinical, not needed) | Internal benchmarking only. **Must not** be used to train or fine-tune production weights. Do not ship them as fixtures. |
| **Restricted / on request** | FEMHALS, FEXHIS, BaMBo, Sheffield tibia images | Request access and read the terms before use. |
| **No licence / unclear** | NOISe (GitHub, no licence), Kaggle bone-lab, MiceBoneChallenge (location unknown), SimTK knee histology, OPARA phantom ([UNR] CC-BY) | Treat as all-rights-reserved until clarified. |
| **Mixed upstream** | BONe (3 MorphoSource-derived scans), SPROUT skulls, CellBinDB bundled datasets | Exclude the upstream-licensed parts from commercial training unless the upstream terms are checked. MorphoSource media need an account and a per-download use agreement, and owners can prohibit commercial use per media item. |

Other notes:
- **Dryad:** CC0 by policy. Scripted downloads currently need an authenticated API token; that is a technical barrier, not a licence restriction.
- **Clinical-origin data:** VBMC trephines and TCIA carry research-governance statements. Keep them out of commercial training unless legal review clears them.

---

## 4. Prioritized download plan (disk ~55 GB free; CPU-only)

The ovine callus (12.5 GB) is already being downloaded by another process.

| Step | What | Bytes | How |
|---|---|---|---|
| 1 | Zenodo 11061947, all 40 files | 242,264,080 | direct Zenodo URLs (morphometry validation) |
| 2 | Zenodo 3909552 subset: ORIG-907-L.zip, MAN-SegmentationFinal.seg.nrrd, AUTO-907-L-bones-label.nrrd (MAN/AUTO label maps already on disk) | ~1.92 GB | direct |
| 3 | SPROUT data_dog_forelimb.zip | 189,279,122 | direct |
| 4 | BONe subset: README, 1R_1U_HF.zip, OMNH_Mammals_44262_HRU.zip; otter SNM_44262_HRU.zip | ~4.13 GB | Dryad token or browser |
| 5 | Histology: NuInsSeg.zip + 2–3 MarrowQuant WSIs (e.g. 21_D21_RF, ~0.59 GB each) | ~2.8 GB | direct (Zenodo, EBI FTP over HTTPS) |
| 6 (optional) | OI tibia wild-type1 zip (BMP ingestion) | 538,250,253 | Figshare ndownloader |
| 7 (later) | 8405457 trab-screw Data.zip, one OVX femur RAR, LumbarSR (only if a multi-resolution study is scheduled) | 13.2 / 5.5 / 26.8 GB | direct |

Steps 1–5 total about 9.3 GB, which leaves room for the callus volumes and working copies. The small verification files listed below are already on disk.

**Already downloaded for format checks** (each in its own directory under `data/raw/`):
- `zenodo_11061947_trab_tbth/` (2 NIfTI)
- `zenodo_3909552_mouse_oa_knee/` (MAN and AUTO label NRRDs + colour table)
- `zenodo_24081554_voronoi_ha_scaffold/uCT_binarized.rar` (RAR v5, not extracted)
- `zenodo_3608390_synthetic_trab/gt.zip`
- `zenodo_24047383_sprout/README.md`
- `zenodo_8405457_trab_screw/_readMe.txt`
- `idr0096_marrowquant/idr0096-experimentA-annotation.csv`

`dryad_bone_4j0zpc8qq/` is empty because the download was refused.

---

## 5. Gaps (nothing usable found)

- **Labelled bone-defect / callus / scaffold-with-bone micro-CT.** No open dataset with bone-vs-scaffold or new-bone-in-defect labels was found on Zenodo, Dryad, Figshare, Dataverse, BioImage Archive, IDR or OSF.
  - The closest candidates are: the Hereon SRµCT Mg-implant studies (labels described in papers, no deposit found), the Kaggle calvarial-defect ROIs (licence unknown), and the Sheffield in vivo tibia scans (on request).
  - Recommendation: build an internal annotated set from the ovine callus `.txm` volumes, and seek collaborator data under a data-sharing agreement.
- **HA-density calibration phantom scans.** None found. Scan an in-house QRM/Scanco HA phantom; the chicken-bone dose series can cover noise robustness.
- **Bone histology with pixel masks for Goldner / Masson / TRAP / toluidine blue.** None open. FEXHIS and BaMBo are restricted; NOISe has no licence.
- **Unfinished searches.** The web-search quota for this session ran out before a final round of Dryad and Mendeley Data searches. A follow-up session could search Mendeley Data and Dryad more fully.
