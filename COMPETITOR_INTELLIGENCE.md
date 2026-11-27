# Competitor Intelligence (top level)

Full analysis (36 competitors, evidence-tagged, sources): **docs/research/COMPETITOR_INTELLIGENCE.md** and
**docs/research/competitors.csv**. Key conclusions for decisions:

## What competitors already do (do not claim otherwise)
* **Dragonfly 3D World 2027.1** (Comet): deep-learning segmentation (incl. SAM), Bone Analysis module with Bouxsein
  indices, cortical/trabecular separation, PDF/HTML Report Builder, Bruker/Scanco raw readers [V]. Free academic licence
  **excludes fee-for-service use** [V] — OsteoQuant cannot build a service on it. *The playbook's claim "no study-endpoint
  reports" is contradicted.* No GLP package or audit trail found.
* **Amira/Avizo + BONe**: AI-assisted multi-material segmentation; BONe open DL tools [V].
* **Bruker CTAn**: de-facto morphometry standard; a threshold-based "defect healing with biomaterials" workflow [CC]; no
  learned three-class model found.
* **Charles River**: advertises Part 11-compliant custom algorithm development [CC]; **Inotiv** sells "% residual implant
  material" as a histology endpoint [CC]; **Visiopharm** has a validated healing-allograft histology algorithm [CC];
  **Bioquant** AI segmentation suite announced for Spring 2027 [CC].
* **Academic prior art**: CNN for bioactive-glass scaffold/bone/pore (Dice 90.1); nnU-Net on Mg implants (mIoU 91–94%);
  UIUC scaffold+ingrown-bone U-Net (doi:10.1007/s11517-026-03686-x, Oct/Nov 2026) [RF].

## Reuse rather than rebuild
nnU-Net / MONAI (training backbone once a GPU is available), BoneJ2 / BoneJ Headless (cross-check morphometry; CC0/BSD),
napari (desktop annotation), 3D Slicer (DICOM/registration interop), SimpleITK (registration — already used).
ITK-SNAP and QuPath are GPL: use as separate tools, do not link.

## Narrowest credible differentiation (supported by this project's results)
1. **Known-truth separability benchmarking per material** (phantom library + physics simulator) — tells a customer *before
   a study* whether micro-CT alone can separate their graft from new bone at their voxel size.
2. **Longitudinal day-0 propagation protocol** — the only approach in our simulations that kept graft Dice ≥0.8 when graft
   morphology resembled new bone (Experiment L2). Sold as study-design guidance + analysis.
3. **Audit-ready report**: locked model hashes, ROI definition hashes, hash-chained audit trail, reviewer sign-off,
   explicit exceptions — no micro-CT package found advertising Part 11 features.
4. **Per-study service pricing** for small orthobiologic firms without imaging staff.

## Threat scenarios
Dragonfly ships graft presets; CROs (Charles River) build in-house; Bruker adds DL to CTAn; a well-funded pathology-AI
company (Deciphex, Visiopharm) adds micro-CT. Mitigation: own the material/phantom reference library and multi-site
validation data; position as CRO partner.
