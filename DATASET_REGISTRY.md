# Dataset Registry (top level)

Full survey of 41 public datasets with licences, sizes, URLs and priorities: **docs/research/DATASET_REGISTRY.md**
(machine-readable: `data/manifest/datasets.json`). This page lists what this project actually downloaded and used,
plus corrections found during use.

## Used in this project
| Dataset | DOI / record | Licence → commercial use | What we used | Experiments | Notes / corrections |
|---|---|---|---|---|---|
| Ovine metatarsal distraction callus (Zeiss Xradia .txm) | 10.5281/zenodo.17255310 (record 17255311) | CC-BY-4.0 → allowed with attribution | 18-day and 161-day volumes (2×2.1 GB), MD5 verified | O, F, sample report 2, demo | **Voxel size is 24.6 µm (file PixelSize), not 3.72 µm** as stated in the playbook and in the survey row; 60 kV per ReconSettings; 161-day scan contains saturated dense hardware/holder; no labels |
| Trabecular cubes + Scanco IPL thickness/separation maps | 10.5281/zenodo.11061947 | CC-BY-4.0 → allowed | 8 segmented cubes (100³) + IPL DT maps | G (external benchmark) | Header voxel sizes 16.56–17.59 µm vary per file; description says 17.59 µm; header values used |
| SPROUT dog forelimb micro-CT | 10.5281/zenodo.24047383 | CC-BY-4.0 → allowed (forelimb subset; skull subset keeps MorphoSource terms — not used) | 15 scans + manually corrected 4-bone labels, official 10/5 split | H, I | No voxel spacing stored → distances in voxels |
| Mouse OA knee (Kitware) | 10.5281/zenodo.3909552 | CC-BY-4.0 → allowed | 907-L DICOM series (829 slices) + manual 8-class compartment map | O (DICOM ingest) | Labels are anatomical compartments, not bone voxels |
| NuInsSeg H&E nuclei | 10.5281/zenodo.10518968 | CC-BY-4.0 → allowed | H&E tiles + manual nuclei masks | N3 | Not bone tissue; validates nuclei component only |
| HA Voronoi scaffold (binarised) | 10.5281/zenodo.24081554 | CC-BY-4.0 | downloaded (15 MB, .rar) | — | rar extraction tool not installed; not used |

## Blocked (see BLOCKERS.md)
| Dataset | Why | Founder action |
|---|---|---|
| BONe (Dryad 4j0zpc8qq, CC0) | Dryad requires API token for file download | Download `1R_1U_HF.zip` (2.0 GB, file id 4859575) in a browser |
| Otter CTP labels (Dryad b2rbnzsq4, CC0) | same | `SNM_44262_HRU.zip` (file id 3926474) |
| MarrowQuant bone H&E (IDR idr0096, CC-BY-4.0) | ftp.ebi.ac.uk TLS fails through this environment's proxy | Download `21_D21_RF (20x).ome.tiff` from EBI FTP on a normal network |

## Licence-aware use (DECISIONS D-006)
`osteoquant.ml.train.save_model` tags a model `commercial_eligible` only if *all* training cases are `commercial_use == allowed`.
Current registry (`models/registry.json`): all models trained on project-generated synthetic data or CC-BY-4.0 data →
`commercial_eligible`, but **every model is a research prototype** (synthetic-trained models carry a report watermark).
CC-BY requires attribution in product documentation (see docs/security/IP_PROVENANCE.md).

## Synthetic dataset (project-generated)
`data/processed/synth/` — 120 specimens (train 48, val 8, test 16, ood_mat 40 [bioglass, xenograft]); regenerate
deterministically with `python experiments/make_synthetic_dataset.py` (generator v1.0.0, periodic textures).
