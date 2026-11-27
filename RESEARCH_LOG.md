# Research Log (chronological, 2026-11-27)

1. **Environment inspected**: 4 vCPU, 15 GB RAM, no GPU. Founder's Mac not attached; all work in a cloud container.
2. **Founder playbook read** (22 pp) and opportunities workbook (6 sheets). Direction A = DefectFill Report.
3. **Seven parallel research streams launched** (competitors, datasets, bone science, commercial, funding, collaborators+validation, quality). All completed; outputs in docs/, business/, grants/, outreach/, validation/.
4. **Real data**: Zenodo concept 17255310 resolves to record 17255311; first download attempt returned HTML (404) — fixed via API file links; MD5 verified. Playbook said voxel 3.72 µm; file metadata says **24.6 µm** (correction).
5. **NIST attenuation tables** fetched; page duplicates its table — de-duplicated. HA-equivalent analysis shows energy-dependent equivalence for glass/CaSO4.
6. **Phantom generator**: first version 60 s/phantom (rejection packing) → continuous-space packing, 16 s.
7. **Morphometry**: thickness bug (border voxels, conservative sphere radius) found by analytic tests and fixed; later, **external benchmark vs Scanco IPL** revealed an 18% Tb.Th under-read from the border convention → added `border="edge"` (ICC 0.983).
8. **Audit chain bug**: SQLite TEXT affinity changed hashed field types → chain verification failed; caught by test, fixed by canonicalising types.
9. **Experiment A**: RF best classical (graft Dice 0.88 vs 0.77 CTAn-style).
10. **Experiment C/C2**: intensity-only bound collapses in overlap regime; RF survives only with compact granules. Key caveat logged.
11. **Experiment B**: U-Net 0.86/0.92; context-channel ablation shows no benefit.
12. **Registration bugs** (Experiment L): (a) periodic phantom textures → aliased optimum; added non-periodic mode; (b) `SetOptimizerScalesFromPhysicalShift` diverges at sub-mm FOV → explicit scales; (c) SimpleITK pyramid sigmas default to *physical units* → blurred away the image. After fixes TRE < 4 µm.
13. **Experiment L/L2**: day-0 propagation is the only method ≥0.8 graft Dice when granules resemble new bone.
14. **Real-data robustness**: thresholds included zero padding (new-bone fraction 1.0) → robust value selection; 161-day scan has saturated hardware → metal QC check + report exception path.
15. **Downloads blocked**: EBI FTP (TLS through proxy) and Dryad (token). Substitutes: NuInsSeg (Zenodo), SPROUT dog forelimb (Zenodo).
16. **Viewer** exercised in headless Chromium: login, study, viewer, brush edit → new version, measurement, 3D surface, audit.
