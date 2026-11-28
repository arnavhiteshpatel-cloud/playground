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
17. **Independent adversarial review** (security + science) found 2 critical security issues (detached-header file read; unsafe model deserialisation), cross-tenant and blinding leaks, and a mislabelled "Bayes bound". All critical/high fixed with regression tests; claims corrected (intensity-only oracle 0.52–0.77, not 0.30–0.65).
18. **Experiment A rerun** with balanced RF training (12 specimens, 4 materials): graft Dice 0.888 (was 0.882); conclusions unchanged.
19. **Experiment H redefined**: SPROUT dog scans contain the thorax with only forelimb bones labelled → whole-volume bone segmentation was ill-posed; evaluation restricted to a band around labelled bones with ignore labels.
20. **Experiment K rerun**: temperature scaling worsened ECE (0.008→0.011); entropy is a weak OOD detector (AUROC 0.66) but a sensitive failure flag (4/4).
21. **Experiment O on real data** found three more defects: out-of-core Otsu included zero padding (threshold 0), DICOM reader OOM (two float copies), and a script variable collision. Fixed: DICOM 829 slices now 5 s / 4.45 GB.
22. **Report 1** silently dropped a specimen whose ROI failed → generator now lists it under Exceptions (principle: every specimen appears).
23. **Held-out series (Generation 2)**: S1H (1.3.3) and S1H2 (1.4.0) found supported measurements that failed (blur pushes graft edges into the new-bone range; one-voxel rim too narrow at σ ≈ 1 voxel); each led to a rule tested on unseen conditions. S1H3 (1.4.1) had no supported failure, but its 0.045 bound counted rows; with structures as the unit it is 0.34 (cycle-3 review).
24. **S1H4** (shipped 1.4.3, the application's material paths): no supported failure, but residual graft supported only for HA, nothing with the material Unspecified, no volume endpoint for 89% of specimens; bound 0.14 with 24 structures carrying support.
25. **S1H5** (pre-registered, HA residual graft on condyle/segmental defects, 48 structures): precision bound 0.074 met — but no graft measurement in that scope failed at all, so the advisor's refusals there only cost coverage. Lesson: a precision test must include conditions where failures occur, or it cannot show refusal.
26. **B1-blur**: the scan-measured blur collapses to ≈0.6 voxel at high noise (0.47× the true blur at relative noise 0.26); the conservative calibration does nothing there. Not reached in the held-out conditions; next advisor version.
27. **S2 part b**: domain-randomised synthetic pretraining transferred worse than the Gen-0 synthetic model on every real test scan (0.353/0.457 vs 0.377/0.513 at native/2× scale). Test-time zoom (scale matching) helped more than randomisation.
28. **CI**: had never passed before 28 Nov (Python 3.11 vs numcodecs, undeclared dependencies, Windows memmap, archive paths); after fixing, a macOS-only segfault appeared at test teardown — closing the shared SQLite connection while a job thread queried it (DF-043).
29. **Deck/report drift**: two builders still judged S1H3 with the row-level bound after the registry was corrected; documents built from code can lag the ledger, so the claims checker now also reads decks, PDFs and UI strings and runs in CI.

