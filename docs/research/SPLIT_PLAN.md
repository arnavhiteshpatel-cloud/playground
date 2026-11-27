# Leakage-Free Split Plan (specimen- and animal-level)

Date: 2026-11-27. Scope: every dataset under `data/raw/`, from rounds 1 and 2.

**Rules that apply to every dataset:**

1. **The split unit is the animal (or human donor), never the image, slice, patch or timepoint.** Left and right limbs, all timepoints, all sections and all patches of one animal go into the same split.
2. **Assign splits deterministically.** Sort the group IDs, take SHA-256 of `"<dataset>:<group_id>"`, and assign by the hash modulo 100: train < 70 ≤ val < 85 ≤ test. Keep any official split instead where one exists. Store the resulting manifest (group ID → split) next to the processed data and never regenerate it after a model has been evaluated.
3. **Hold out at dataset level when possible.** For generalisation claims (scanner, species, material), hold out a whole dataset. A random within-dataset split does not test domain shift.
4. **Treat single-specimen datasets as test-only.** These are 17303022, 17304175 and the 907-L knee. They are used for ingestion, calibration or QC tests and are never mixed into training.
5. **Check before every training run.** The run must assert that no group ID appears in two splits, and must log the manifest SHA-256 in the model registry.
6. **Keep synthetic and real data apart.** Synthetic phantoms may be used in training. Real held-out test sets must never contain anything derived from the same real specimen as any training item, including augmentation or synthetic data seeded from a real scan.

## Per-dataset plan

| Dataset (folder) | Group unit (where the ID comes from) | Groups available | Proposed split | Leakage risks and notes |
|---|---|---|---|---|
| Ovine distraction callus (`zenodo_17255310`) | Animal = timepoint file (one animal per timepoint, per the record and round 1) | 6 (2 on disk) | Test-only (external real-callus test). With all 6: train 18/22/47 d, val 64 d, test 112/161 d **only if** temporal extrapolation is the question; otherwise leave-one-animal-out CV | Timepoints are different animals, so there is no longitudinal leakage. The 161 d scan contains saturated hardware: mask it |
| Trabecular cubes (`zenodo_11061947_trab_tbth`) | Sample ID `BMLPL_00x` | 8 | Validation-only (morphometry reference vs Scanco IPL); not for training | Round-1 caveat Q-10: the border convention was chosen on these 8. A second independent reference set is needed before calling this validation |
| SPROUT dog forelimb (`zenodo_24047383_sprout`) | Specimen ID = file-name prefix (e.g. `241035_FB`); one dog per scan | 15 | **Use the official `train_test_split.csv`: 10 train / 5 test.** Take validation from train by group (e.g. 2 of 10) | Breed labels repeat across specimens (WHWT ×4); IDs differ, so treated as different animals. No voxel spacing in the files |
| Mouse OA knee (`zenodo_3909552_mouse_oa_knee`) | Mouse ID (numeric part of `907-L`; L and R knees share a mouse) | 14 mice / 28 knees (1 knee on disk) | Test-only now. If more are downloaded: split by mouse, so both knees of a mouse go to the same split | Only 907-L has manual labels; the AUTO labels are pseudo-labels and must never be used as test ground truth |
| NuInsSeg H&E (`zenodo_10518968_nuinsseg`) | Tissue folder (e.g. `human bladder`, `mouse femur`); the patient/animal is not encoded | 31 tissue/organ groups, 665 images | Group-level split by tissue folder (hash rule). Keep `mouse femur` (6 images) and `mouse muscle_tibia` in **test** as the closest bone-adjacent domain | Images of one tissue probably come from the same donor; splitting by image would leak donor appearance |
| MarrowQuant (`idr0096_marrowquant`) | Mouse, derived from `Image Name` (e.g. `Image8kw RT 3` = mouse 3, 8-week group; RT/RF/LT/LF = bones of one mouse) | per annotation CSV | Split by (experiment, age group, mouse number). All bones of one mouse go to the same split | Only the annotation CSV is on disk; WSIs are blocked (round 1) |
| HA Voronoi scaffold (`zenodo_24081554_voronoi_ha_scaffold`) | Scaffold | 8 | Material-alone characterisation; test-only | No biology; still unextracted RAR |
| Synthetic trabecular (`zenodo_3608390_synthetic_trab`) | Phantom volume | per GT zip | Any split; it is synthetic | Never mix with real test data |
| Trabecular screw (`zenodo_8405457_trab_screw`) | Bone core (before and after screw insertion = same core) | 10 cores | 6/2/2 by core; before/after pairs stay together | Not downloaded (13.2 GB) |
| **Sheep biopsy + HA phantom** (`zenodo_17304175_...`) | 1 biopsy | 1 | **Test-only**: calibration/QC regression test (phantom inserts 0–1200 mgHA/cm³) | One specimen; never train on it |
| **Sheep metatarsal CT** (`zenodo_17303022_...`) | 1 animal, several timepoints | 1 | **Test-only**: longitudinal registration test | All timepoints are the same animal; a split across timepoints would be leakage |
| **Ovine Ti + SF gaps** (`zenodo_4108304_...`) | Sheep ID from file names (`LIMA 095`–`100`); femur and tibia overview images from the same sheep belong together | ~6 sheep | Test-only for the histology module until labelled. If labelled: split by sheep | The overview TIFF names (`FEMUR/TIBIA TS/TT 1mm/3mm`) do not encode the sheep. **Ask before using them as independent specimens**: implants may share an animal |
| **Rabbit radius DBM** (`mendeley_3zf2zhr2z6_...`) | Rabbit number (leading integer, e.g. `24L-4W` → rabbit 24); L and R and all weeks stay together | ~36 rabbits | Split by rabbit (hash rule); stratify by group if the group mapping (in the XLSX) is used | Bilateral images and 4/8/12-week series of the same rabbit must stay together |
| **Mouse hindpaw** (`mendeley_7sm9wznp6d_...`) | Mouse (`889`, `739`, …); both paws stay together | 1 on disk (7 in the record) | Test-only now (OOD in vivo bone labels). With the full record: split by mouse | Labels exist only for the 2-month example |
| **Rabbit radial void filler** (`zenodo_4991164_...`) | Rabbit ID from file name (e.g. `11-289`); all timepoints stay together | per file names | Split by rabbit | Postoperative and later radiographs of one rabbit are a time series |
| Hugging Face mouse callus (not downloaded) | Scan (prefix `1__` vs `T2__`); the same or different mice is unknown | 2 | Test-only if used | Unknown whether the 7 d and 14 d scans are the same animal: treat them as one group |

## Graft-specific evaluation design (for future labelled data)

When labelled graft data arrives (internal, collaborator or Hereon), test the claims in this order:

1. **Within-material, new animals.** Split by animal (rule 1).
2. **Leave-one-timepoint-group-out.** This tests the time dependence of resorbing materials (β-TCP, BCP, CaSO4), and still splits by animal.
3. **Leave-one-material-out.** This tests the `unsupported_material_workflow` in `osteoquant/knowledge/materials.json`: the advisor must abstain or require characterisation.
4. **Leave-one-scanner/protocol-out.** Energy-dependent materials must not transfer thresholds across protocols.

Report each as a separate number. Never pool them into one headline Dice.
