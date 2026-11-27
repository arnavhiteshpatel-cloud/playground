# Scientific Learning Curriculum (12 weeks, ~8 h/week)

Each week: **read** (real sources; full list with DOIs in `docs/science/REFERENCES.md`, IDs R#), **do** (an exercise in
this codebase), **check** (you can explain the answer to a bone biologist without notes). Weeks 1–4 match the period
in which you should be running customer interviews; schedule reading around them.

| Wk | Topic | Read | Do in the codebase | Check |
|---|---|---|---|---|
| 1 | Bone biology & healing | Einhorn & Gerstenfeld 2015 (R45); Marsell & Einhorn 2011 (R46); docs/science/BONE_BIOLOGY_AND_GRAFTS.md §1 | Generate condyle phantoms at stages 0.2/0.5/0.8 (`osteoquant phantom --stage`) and view them in the viewer | Explain woven vs lamellar bone, osteoconduction vs osteoinduction, why defects are "critical-size" |
| 2 | Graft materials | Bohner et al. 2020 β-TCP (R33); Jones 2013 bioactive glass (R37); docs/science/SEPARABILITY_ANALYSIS.md | Run `material_contrast_table()`; explain why 45S5 equivalence changes with energy | For HA, β-TCP, CaSO4, bioglass, DBM, allograft: when is micro-CT separation easy, hard, underdetermined? |
| 3 | Micro-CT physics | Feldkamp et al. 1984 (R28); docs/science/MICROCT_IMAGING_SCIENCE.md | Run `osteoquant/phantom/ctsim.py` with and without `bh_correction`; inspect cupping | Voxel size vs resolution; partial volume; beam hardening; why grey values differ between scanners |
| 4 | Calibration & QC | MICROCT_IMAGING_SCIENCE.md calibration framework (tiers Q0–Q4) | `osteoquant qc` on a phantom with `ring_amplitude`, `cupping`, `noise_sigma` varied; read Exp E results | Which QC checks are deterministic vs heuristic, and why that distinction matters in a report |
| 5 | Morphometry standards | Bouxsein et al. 2010 (R1); Hildebrand & Rüegsegger 1997 (R2); Odgaard & Gundersen 1993 (R3); Salmon et al. 2015 on SMI (R5) | Re-run `exp_G_morphometry.py`; change `border` and see the IPL agreement move | Why Tb.Th "edge vs background" border handling changed agreement with Scanco IPL from ICC 0.61 to 0.98 |
| 6 | Histomorphometry | Dempster et al. 2013 (R6); Stalder et al. 2014 micro-CT + histology (R30) | `exp_N_histology.py`; inspect colour deconvolution outputs | Why histology area ≠ micro-CT volume fraction; what decalcification does to calcium-phosphate grafts |
| 7 | Segmentation & ML | Isensee et al. 2021 nnU-Net (Nat Methods 18:203, DOI 10.1038/s41592-020-01008-z); `osteoquant/ml/unet.py` | Train `exp_B_unet.py` with 300 iterations; compare Dice | Train/val/test split by specimen; why voxel-level metrics are not biological replicates |
| 8 | Uncertainty & generalisation | Guo et al. 2017 calibration (ICML); BONe paper (see docs/research) | `exp_K_M_uncertainty.py`; read risk–coverage curve | What ECE, AURC and abstention mean; why OOD materials need adaptation |
| 9 | Statistics for preclinical studies | Koo & Li 2016 ICC (DOI 10.1016/j.jcm.2016.02.012); Bland & Altman 1986 (Lancet 1:307) | `osteoquant/stats/core.py` — reproduce Shrout–Fleiss ICCs in tests | Choose ICC form for method agreement; avoid pseudoreplication; when to use mixed models |
| 10 | Longitudinal imaging & registration | SimpleITK registration docs; Exp L/L2 results | `exp_L_longitudinal.py`; break registration by setting physical-unit sigmas (see RESEARCH_LOG #12) | Why a day-0 scan changes what is identifiable; what creeping substitution breaks |
| 11 | Regulation & quality | docs/quality/REGULATORY_RESEARCH.md; OECD GLP No. 17; 21 CFR 58 & 11 | Walk through URS → FS → traceability_matrix.csv for 5 requirements | Why technical controls ≠ Part 11 compliance; what a CSV consultant would ask |
| 12 | Customer & market | business/INTERVIEW_GUIDE.md; business/PROSPECTS.md; I-Corps material | Conduct and code 3 interviews in `interview_log_template.csv` | State the bottom-up market estimate and which assumption most changes it |

**Practical skills alongside:** Python (NumPy/SciPy) → git/GitHub workflow → reading a FastAPI endpoint → writing a test.
Use `founder/OPERATING_MANUAL.md` §6 as your change routine.

**Optional deeper courses** (verify current availability before enrolling): I-Corps (Landuyt Center); BIOE/MechSE
graduate courses in biomedical imaging or bone mechanics (ask Mariana Kersh's lab which they recommend).
