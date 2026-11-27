# Dataset Discovery, Round 2

Date: 2026-11-27. Machine-readable table: `docs/research/datasets_r2.csv`, with 27 rows. Round 1 (41 datasets) is in `docs/research/DATASET_REGISTRY.md`. Round-1 items are not repeated here unless new information was found.

## 1. Bottom line

1. **No openly downloadable dataset with voxel labels for residual graft vs new bone was found.** This holds across all 12 sources searched.
2. **Real-tissue implant + bone labels exist, but only on request.** These are synchrotron Mg-implant studies from Hereon:
   - rat Mg-xGd: 17 samples, four classes (bone, degradation layer, residual material, background) [baltruschat2021];
   - sheep ZX00: 8 labelled and 9 unlabelled samples [lopesmarinho2024].

   Their data statements are "available from the corresponding author on reasonable request" and "will be made available by the authors". A co-registered SRµCT/histology set of bone implants with more than 50 image pairs exists, but no data statement was found [irvine2025]. Obtaining any of these requires contacting authors, which is a founder action outside this task.
3. **The closest public match to OsteoQuant's use case** is FaceBase record 10.25550/8X-J1TW: rat 8 mm calvarial defects with mineralised collagen microgels, longitudinal in vivo µCT at 4, 8 and 12 weeks, ex vivo µCT at 12 weeks, and H&E, Masson and picrosirius histology. The DataCite metadata resolves. However, FaceBase's public ERMrest API returned no record, which points to an unreleased or access-controlled record. **Access and licence must be checked in a browser.**
4. **Downloaded this round** (openly licensed, no login, each under 3 GB): 6 datasets, 2.92 GB in total. Every file's checksum was verified against the repository (Zenodo MD5 or Mendeley SHA-256), and SHA-256 plus the licence text are recorded per folder (§4).
   - The most useful download is the **sheep iliac-crest biopsy µCT with a QRM HA phantom (0–1200 mgHA/cm³) in the field of view**. Round 1 found no open phantom scan, so this is the only open real-tissue scan with known density inserts for calibration and QC tests.

## 2. Search log (what was searched, how)

| Source | Method | Queries | Result |
|---|---|---|---|
| Zenodo | REST API `/api/records`; dataset type, then all types; 25 per page × 3 pages | 60 (dataset) + 38 (all types) + 9 targeted | 1,848 + 1,749 hits, filtered by keyword to 268 + 573; every plausible record inspected (files, licence, description). New finds: 17304175, 17303022, 4108304, 4991164, 10177428, 21281852, 6481319 |
| Figshare | API v2 `/articles/search` | 30 | 1,603 hits. Almost all are journal-figure deposits (PLOS, SciELO, Frontiers). Datasets with images: none relevant; figure/table deposits listed |
| Dryad | API v2 `/search` | 20 + 7 | 87 + 22 hits. Search throttles to HTTP 403 after a few queries, and relevance ranking is poor (palaeontology dominates). No new relevant datasets. Downloads still need a bearer token (round 1) |
| Mendeley Data | `api/research-data/search?query=` plus `public-api/datasets/<id>` for files and SHA-256 | 27 + 51 | 499 + 783 records. New finds: 3zf2zhr2z6, 7sm9wznp6d, mcyktb4mnm, txy98jt7yp, h2cnrvhg76, 5kt63rgvv2 |
| EBI BioImage Archive | BioStudies API `BioImages/search` | 19 | No bone-defect, graft or scaffold imaging studies; only bone-marrow and cell-biology entries |
| IDR | round 1 (idr0096) | – | not repeated |
| OSF | SHARE `index-card-search` | 4 | Only one systematic-review registration |
| MorphoSource | `/api/media?q=` | 6 | Museum and morphology meshes only (skulls, calvaria laser scans). Downloads need an account and a per-item use agreement (round 1) |
| TCIA | NBIA `getCollectionValues` | all 157 collection names | No preclinical bone or graft collection; only mouse cancer models and sarcoma |
| Kaggle | API needs an account | – | Not searchable from this environment; round-1 calvarial ROI set still has an unknown licence |
| Hugging Face datasets (stand-in for Papers with Data, which redirects there) | `/api/datasets?search=` | 6 | One relevant entry: SII-hz67/microCT (mouse fracture callus, MIT tag, no metadata) |
| GitHub | search API (repository level) | 13 | Code only: GMM bone/scaffold segmentation [raymond2022], a mandible biomaterial histology+µCT project, Hereon VolRAFT, and others. Repository-content API access is blocked in this session; READMEs were read via raw.githubusercontent.com |
| FaceBase | DataCite + ERMrest | 8 | 8X-J1TW found (see §1); one low-relevance suture-regeneration record |
| Paper supplements and data statements | web search + publisher/PMC pages | 8 | Hereon Mg (2 papers), arXiv virtual staining, Bone Bricks (no data), rat calvarial in vivo µCT (no data) |

## 3. Ranked candidates (relevance 1–5)

Licence key: **C** = commercial-compatible (CC0, CC-BY, MIT); **NC** = non-commercial or research only; **?** = unknown or restricted.

| Rel. | Dataset | Species / model | Material | Modality, voxel | n | Labels | Size | Licence | Open download |
|---|---|---|---|---|---|---|---|---|---|
| 5 | FaceBase 8X-J1TW | rat 8 mm calvarial CSD | mineralised collagen microgels | in vivo µCT 4/8/12 wk + ex vivo µCT + histology | ? | histology (no masks stated) | ? | ? | **no** (not public via API) |
| 5 | Hereon rat Mg SRµCT [baltruschat2021] | rat | Mg-5Gd / Mg-10Gd | SRµCT 1.2–2.4 µm | 17 | 4-class voxel labels | – | not released | no (on request) |
| 5 | Hereon sheep ZX00 SRµCT [lopesmarinho2024] | sheep tibia 6/12/24 wk | ZX00 Mg | SRµCT 2.76/3.79 µm (binned) | 8 + 9 | 4-class | – | not released | no |
| 5 | Virtual-staining pairs [irvine2025] | bone-implant samples | degradable implants | SRµCT + toluidine blue, co-registered | 50+ pairs | histology | – | none stated | no |
| 3 | **Zenodo 17304175** | sheep iliac-crest biopsy | – (QRM HA phantom 0–1200 mgHA/cm³ in FOV) | µCT, Y.Cougar SMT, 22–35 µm study range | 1 | phantom inserts | 1.22 GB | CC-BY-4.0 (C) | **yes, downloaded** |
| 3 | **Zenodo 17303022** | sheep metatarsus, osteoporosis + bone transport across a 15 mm CSD | – | clinical CT 0.46–0.57 × 0.625 mm, longitudinal, QRM phantom | 1 animal × several timepoints | none | 0.43 GB | CC-BY-4.0 (C) | **yes, downloaded** |
| 3 | **Zenodo 4108304** [lovati2020] | sheep femur/tibia 1 and 3 mm implant gaps | trabecular Ti ± silk fibroin | histology overview TIFFs (5903×5683), micrographs, radiographs | ~6 sheep | none | 0.14 GB | CC-BY-4.0 (C) | **yes, downloaded** |
| 3 | **Mendeley 3zf2zhr2z6** | rabbit radial segmental defect, 4 groups × 9, 4/8/12 wk | DBM ± EPC ± vascular bundle | radiographs, µCT renders, H&E/CD31 images (2D) | 36 rabbits | none | 0.69 GB | CC-BY-4.0 (C) | **yes, downloaded** |
| 3 | HF SII-hz67/microCT | mouse fracture callus 7 and 14 d | – | µCT TIFF slices, voxel unknown | ≥ 2 | none | > 2.5 GB | MIT tag (C; provenance thin) | yes, not downloaded |
| 3 | Kaggle calvarial (round 1) | rodent | ? | µCT slices | ? | defect ROI | ? | ? | no (account) |
| 2 | **Mendeley 7sm9wznp6d** | mouse hindpaw, in vivo | – | in vivo µCT DICOM, 17.4 µm | 6 + 1 | per-bone labels (0–66) | 5.27 GB (11 MB taken) | CC-BY-4.0 (C) | **yes, labelled example downloaded** |
| 2 | **Zenodo 4991164** [brooks2015] | rabbit radial window defect, 8 wk | polymer/CaCO3–HA antibiotic void filler | serial radiographs | per table | none | 0.83 GB (0.41 GB taken) | CC0 (C) | **yes, radiographs downloaded** |
| 2 | Zenodo 10177428 | in vitro | collagen sponge, PTA contrast | µCT SkyScan 1276 | 1 | none | 8.9 GB | CC-BY-4.0 (C) | yes, too large |
| 2 | Mendeley mcyktb4mnm | scaffold only | nano-HA/chitosan/agarose | µCT images + porosity | few | none | 0.23 GB | CC-BY-4.0 (C) | yes |
| 2 | Mendeley txy98jt7yp | phantom ± metal implant | metal | µCT projections + reconstructions | 1 | none | 0.72 GB | CC-BY-4.0 (C) | yes |
| 2 | Zenodo 6481319 | rat implants | Mg-xGd/Ti/PEEK | Fiji script | – | – | small | CC-BY-4.0 (C) | yes (software) |
| 1–2 | others in CSV | | | | | | | | |

**Licences.** Every downloaded dataset is commercial-compatible: five are CC-BY-4.0 (attribution required) and one is CC0. No NC dataset was downloaded this round. The HF dataset's MIT tag comes with no author or provenance information, so treat it as unverified before any commercial training.

## 4. What was downloaded (data/raw/)

| Folder | Files | Bytes | Licence | Verification |
|---|---|---|---|---|
| `zenodo_17304175_ovine_iliac_biopsy_bmd_phantom/` | `sheep biopsy  μCT stack.rar` | 1,217,729,343 | CC-BY-4.0 | MD5 = Zenodo; SHA-256 in PROVENANCE.json |
| `zenodo_17303022_ovine_metatarsal_ct_longitudinal/` | `sheep CT stacks.rar` | 433,525,191 | CC-BY-4.0 | MD5 = Zenodo |
| `zenodo_4108304_ovine_ti_sf_bone_gap/` | 63 files (TIFF, JPG, XLSX) | 144,590,179 | CC-BY-4.0 | MD5 = Zenodo |
| `mendeley_3zf2zhr2z6_rabbit_radius_dbm_defect/` | 178 files (JPG, PNG, TIF, XLSX) | 693,855,164 | CC-BY-4.0 | SHA-256 = Mendeley |
| `mendeley_7sm9wznp6d_mouse_hindpaw_bone_labels/` | `889 2m Labels.zip`, `889 2m Processed Data.zip` | 11,118,505 | CC-BY-4.0 | SHA-256 = Mendeley |
| `zenodo_4991164_rabbit_radius_void_filler/` | `Radiographs.zip` + 2 XLSX | 414,758,603 | CC0-1.0 | MD5 = Zenodo |
| **Total** | | **2,915,576,985** | | |

Each folder contains:

- `PROVENANCE.json`: source, DOI, title, creators, record URL, licence as stated by the repository, related identifiers, and per-file bytes, SHA-256, repository checksum and URL;
- `LICENSE.txt`: the Creative Commons legal code, whose SHA-256 is also recorded.

Zenodo files were fetched from `/api/records/<id>/files/<name>/content`.

**Not extracted:**

- The two Zenodo RAR5 archives, because no RAR extractor is installed and installing one was not permitted in this session.
- The zip files, which were left as delivered; only their contents were listed.

Checked contents:

- The hindpaw labels are 520 DICOM slices at 17.4 µm, with uint8 labels (values 0–66, one value per bone).
- The 4108304 TIFFs are 300 dpi histology overview scans.

## 5. Gaps and recommended founder actions (not done here: no contact, no registration)

1. **Ask Hereon (Helmholtz-Zentrum Hereon, Institute of Metallic Biomaterials) for the labelled SRµCT Mg datasets** [baltruschat2021; lopesmarinho2024]. These are the only real voxel labels found for implant/degradation layer vs bone.
2. **Check FaceBase 8X-J1TW in a browser** for release status and terms. If it is open, it is the best public calvarial dataset (longitudinal µCT plus histology).
3. **Extract the RARs** on a machine with `unrar` or `7z`. Then confirm the biopsy voxel size and the phantom insert densities from the stack headers before using them as a calibration test.
4. **Build the labelled graft dataset internally or with a collaborator.**
   - Scan material-alone and day-0 specimens, as `osteoquant/knowledge/materials.json` → `unsupported_material_workflow` describes.
   - Collect histology-registered labels on a calibration subset [albers2021; stalder2014].
