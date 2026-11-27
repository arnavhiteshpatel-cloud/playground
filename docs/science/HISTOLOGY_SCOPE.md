# Histology Module — Scope Decision (Generation 2)

**Decision (FA-09).** Histology is a *complementary* module. It is not marketed as automated histomorphometry and
produces no endpoint that enters a DefectFill report without a reviewer's explicit acceptance.

| Capability | Evidence (Experiment N) | Status |
|---|---|---|
| 2-D section ↔ micro-CT slice registration (overlay for visual correlation) | Dice 0.31–0.40 → 0.85–0.87 on synthetic sections | **Kept** — overlay and navigation aid |
| Graft void / residual-material area on sections | ICC 0.84 (synthetic) | **Kept** as exploratory, reviewer-accepted measure |
| Bone area fraction on H&E | ICC 0.35 (weak) | **Removed from reports**; manual or validated third-party tool required |
| Stain normalisation (Macenko) | worsened agreement | **Off by default** |
| Nuclei detection (classical) | pixel Dice 0.64, object F1 0.34 on NuInsSeg | **Not offered**; below published deep-learning tools — use those under their licences |

**Where histology is genuinely useful to the product.** (1) Resolving the cases the measurement-support advisor
refuses (bone-derived or intensity-overlapping grafts): histology distinguishes residual graft from new bone by
morphology and staining where micro-CT cannot. (2) Calibrating the new-bone intensity assumption for a material at a
timepoint. Both use the overlay and manual annotation, not automated quantification.

**Revisit when** a commercially licensable, validated bone-histology segmentation model or partner-annotated
sections become available (see docs/research/DATASET_DISCOVERY_R2.md).
